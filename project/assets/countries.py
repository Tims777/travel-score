from dagster import asset
from geopandas import read_file, GeoDataFrame

DOWNLOAD_URL = (
    "https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip"
)
AMERICA = ["North America", "South America"]
EXCLUDE = ["Greenland"]


@asset(group_name="datasets")
def world() -> GeoDataFrame:
    return read_file(DOWNLOAD_URL)


@asset(group_name="datasets")
def americas(world: GeoDataFrame) -> GeoDataFrame:
    americas = world[world["continent"].isin(AMERICA) & ~world["name"].isin(EXCLUDE)]
    return GeoDataFrame(americas)
