from pathlib import Path
from dagster import Definitions, load_assets_from_modules

from .assets import combined, countries, icp, inform, maps, statistics
from .resources.io_manager import LocalFileSystemIOManager

all_assets = load_assets_from_modules([countries, icp, inform, combined, maps, statistics])
data_dir = Path(__file__).parents[1].joinpath("data")

defs = Definitions(
    assets=all_assets,
    resources={
        "io_manager": LocalFileSystemIOManager(
            data_dir=str(data_dir),
        ),
    },
)
