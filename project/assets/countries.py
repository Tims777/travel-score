from dagster import asset
from geopandas import read_file, GeoDataFrame

DOWNLOAD_URL = (
    "https://naciscdn.org/naturalearth/50m/cultural/ne_50m_admin_0_countries.zip"
)
AMERICAS = ["North America", "South America"]
COUNTRY_OR_DEPENDENCY = ["Admin-0 country", "Admin-0 dependency"]
WESTERN_HEMISPHERE = (-180, -90, 0, 90)


@asset(group_name="urls")
def world_url():
    return DOWNLOAD_URL


@asset(group_name="datasets")
def world(world_url: str) -> GeoDataFrame:
    return read_file(world_url)


@asset(group_name="datasets")
def americas(world: GeoDataFrame) -> GeoDataFrame:
    americas = world[
        world["continent"].isin(AMERICAS)
        & world["fclass_iso"].isin(COUNTRY_OR_DEPENDENCY)
    ]
    americas = americas[[americas.active_geometry_name, "iso_a3", "name", "continent"]]
    americas.set_index("iso_a3", inplace=True)
    americas.rename_axis("iso", inplace=True)
    return americas.clip(WESTERN_HEMISPHERE, sort=True)
