from os import environ
from pathlib import Path
from sqlite3 import connect
from subprocess import run
from sys import executable as python
from tempfile import TemporaryDirectory

from pandas import read_sql
import project
from project.utils import N_COUNTRIES_AMERICAS, len_as_expected


RESULT_DATASET = "combined_dataset"


def test_pipeline():
    with TemporaryDirectory() as datadir:
        env = environ.copy()
        env["DAGSTER_HOME"] = datadir
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
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "RUN_SUCCESS" in result.stderr

        outfile = Path(datadir).joinpath(RESULT_DATASET).with_suffix(".sqlite")
        assert outfile.exists()
        with connect(outfile) as con:
            query = f"SELECT * FROM {RESULT_DATASET}"
            df = read_sql(sql=query, con=con)
        assert len_as_expected(df, N_COUNTRIES_AMERICAS, 0.25)
        assert "total consumption" in df
        assert "inform" in df
