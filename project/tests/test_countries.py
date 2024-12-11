from geopandas import GeoDataFrame
from project.assets.countries import world
from project.utils import N_COUNTRIES_WORLD, len_as_expected


def test_inform_scores():
    gdf = world()
    assert isinstance(gdf, GeoDataFrame)
    assert len_as_expected(gdf, N_COUNTRIES_WORLD, 0.1)