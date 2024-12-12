from os import environ
from pathlib import Path
from sqlite3 import connect
from subprocess import run
from sys import executable as python
from tempfile import TemporaryDirectory
from warnings import warn
from pandas import read_sql

import project
from project.utils import N_COUNTRIES_AMERICAS, len_as_expected


RESULT_DATASET = "combined_dataset"


def test_pipeline():
    with TemporaryDirectory(ignore_cleanup_errors=True) as datadir:
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
                f"*{RESULT_DATASET}",
            ],
            env=env,
            cwd=cwd,
            # capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        # assert "RUN_SUCCESS" in result.stderr

        outfile = Path(datadir).joinpath(RESULT_DATASET).with_suffix(".sqlite")
        assert outfile.exists()
        with connect(outfile) as con:
            query = f"SELECT * FROM {RESULT_DATASET}"
            df = read_sql(sql=query, con=con)
            # con.close()
        assert len_as_expected(df, N_COUNTRIES_AMERICAS, 0.25)
        assert "total consumption" in df
        assert "inform" in df

    # Automatic delete might fail, raise a warning in that case
    if Path(datadir).exists():
        warn(Warning(f"{datadir} could not be deleted."))
