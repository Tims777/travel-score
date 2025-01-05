from dagster import Config, asset
from geopandas import read_file, GeoDataFrame

from project.utils import AMERICAN_CONTINENTS, COUNTRY_CLASS, DEPENDENCY_CLASS, WESTERN_HEMISPHERE

DOWNLOAD_URL = (
    "https://naciscdn.org/naturalearth/50m/cultural/ne_50m_admin_0_countries.zip"
)

FIXES = {
    "VCT": {"fclass_iso": "Admin-0 country"},
}


def _fix(gdf: GeoDataFrame):
    for iso, fix in FIXES.items():
        for key, val in fix.items():
            gdf.loc[gdf["iso_a3"] == iso, key] = val


@asset(group_name="urls")
def world_url():
    return DOWNLOAD_URL


@asset(group_name="datasets")
def world(world_url: str) -> GeoDataFrame:
    return read_file(world_url)


class AmericasConfig(Config):
    continents: list[str] = AMERICAN_CONTINENTS
    include_dependencies: bool = False


@asset(group_name="datasets")
def americas(config: AmericasConfig, world: GeoDataFrame) -> GeoDataFrame:
    _fix(world)
    classes = [COUNTRY_CLASS]
    if config.include_dependencies:
        classes.append(DEPENDENCY_CLASS)
    americas = world[
        world["continent"].isin(config.continents) & world["fclass_iso"].isin(classes)
    ]
    americas = americas[[americas.active_geometry_name, "iso_a3", "name", "continent"]]
    americas.set_index("iso_a3", inplace=True)
    americas.rename_axis("iso", inplace=True)
    return americas.clip(WESTERN_HEMISPHERE, sort=True)
