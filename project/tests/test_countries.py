from geopandas import GeoDataFrame
from pytest import mark
from project.assets.countries import world
from project.tests.mocks import MOCKED_NATURAL_EARTH
from project.utils import N_COUNTRIES_WORLD, len_as_expected


@mark.filterwarnings("ignore::DeprecationWarning")
def test_inform_scores():
    gdf = world(MOCKED_NATURAL_EARTH)
    assert isinstance(gdf, GeoDataFrame)
    assert len_as_expected(gdf, N_COUNTRIES_WORLD, 0.1)
