from os import environ
from pathlib import Path
from sqlite3 import connect
from subprocess import run
from sys import executable as python
from tempfile import TemporaryDirectory
from warnings import warn
from dagster import AssetMaterialization, DagsterInstance
from pandas import read_sql
from pytest import mark

import project
from project.tests.mocks import MOCK_ASSETS
from project.utils import N_COUNTRIES_AMERICAS, len_as_expected


RESULT_DATASET = "combined_dataset"


def _create_mock_assets(datadir: str):
    instance = DagsterInstance.from_config(datadir)
    for asset, url in MOCK_ASSETS.items():
        url_file = Path(datadir).joinpath(asset).with_suffix(".txt")
        with url_file.open("w") as fd:
            fd.write(url)
        instance.report_runless_asset_event(
            AssetMaterialization([asset], metadata={"mock": True, "filepath": url_file})
        )


def _run_pipeline(datadir: str):
    env = environ.copy()
    env["DAGSTER_HOME"] = datadir
    env["SKIP_PBF_ANALYSIS"] = "yes"
    cwd = Path(project.__file__).parents[1]
    result = run(
        executable=python,
        args=[
            "python",
            "-m",
            "dagster",
            "asset",
            "materialize",
            "-m",
            "project.definitions",
            "--select",
            f"++{RESULT_DATASET}",
        ],
        env=env,
        cwd=cwd,
        text=True,
    )
    assert result.returncode == 0


def _check_output(datadir):
    outfile = Path(datadir).joinpath(RESULT_DATASET).with_suffix(".sqlite")
    assert outfile.exists()
    with connect(outfile) as con:
        query = f"SELECT * FROM {RESULT_DATASET}"
        df = read_sql(sql=query, con=con)
    assert len_as_expected(df, N_COUNTRIES_AMERICAS, 0.25)
    assert "total consumption" in df
    assert "inform" in df


@mark.filterwarnings("ignore::dagster.ExperimentalWarning")
@mark.filterwarnings("ignore::DeprecationWarning")
def test_pipeline():
    with TemporaryDirectory(ignore_cleanup_errors=True) as tmpdir:
        _create_mock_assets(tmpdir)
        _run_pipeline(tmpdir)
        _check_output(tmpdir)

    # Automatic delete might fail, raise a warning in that case
    if Path(tmpdir).exists():
        warn(Warning(f"{tmpdir} could not be deleted."))
