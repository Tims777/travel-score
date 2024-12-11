from os import environ
from pathlib import Path
from dagster import Definitions, load_assets_from_modules

import project

from .assets import combined, countries, icp, inform, maps, osm, statistics
from .resources.io_manager import LocalFileSystemIOManager

all_assets = load_assets_from_modules(
    [countries, icp, inform, osm, combined, maps, statistics]
)
data_dir = environ.get("DAGSTER_HOME", Path(project.__file__).parents[1])

defs = Definitions(
    assets=all_assets,
    resources={
        "io_manager": LocalFileSystemIOManager(
            data_dir=str(data_dir),
        ),
    },
)
