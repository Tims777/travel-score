from pathlib import Path
from dagster import Definitions, load_assets_from_modules

from .assets import inform, icp, score
from .resources.io_manager import LocalFileSystemIOManager

all_assets = load_assets_from_modules([inform, icp, score])
data_dir = Path(__file__).parents[2].joinpath("data")

defs = Definitions(
    assets=all_assets,
    resources={
        "io_manager": LocalFileSystemIOManager(
            data_dir=str(data_dir),
        ),
    },
)
