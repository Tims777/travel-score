from dagster import Definitions, load_assets_from_modules

from .assets import inform, icp, score

all_assets = load_assets_from_modules([inform, icp, score])

defs = Definitions(
    assets=all_assets,
)