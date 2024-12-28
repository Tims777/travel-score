from os import environ
from pathlib import Path
from dagster import Definitions, load_assets_from_modules

from . import assets
from .resources.io_manager import LocalFileSystemIOManager

DEFAULT_DATA_DIR = Path(__file__).parents[1].joinpath("data")

asset_modules = (getattr(assets, name) for name in dir(assets))
data_dir = environ.get("DAGSTER_HOME", DEFAULT_DATA_DIR)

defs = Definitions(
    assets=load_assets_from_modules(asset_modules),
    resources={
        "io_manager": LocalFileSystemIOManager(
            data_dir=str(data_dir),
        ),
    },
)
