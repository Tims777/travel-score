from geopandas import GeoDataFrame
from pandas import Index
from pytest import mark
from project.assets.countries import AmericasConfig, americas, world
from project.tests.mocks import MOCKED_NATURAL_EARTH
from project.utils import AMERICAN_COUNTRIES, COUNTRY_CLASS, N_COUNTRIES_WORLD, len_as_expected


@mark.filterwarnings("ignore::DeprecationWarning")
def test_world():
    gdf = world(MOCKED_NATURAL_EARTH)
    assert isinstance(gdf, GeoDataFrame)
    countries = gdf[gdf["FCLASS_ISO"] == COUNTRY_CLASS]
    assert len_as_expected(countries, N_COUNTRIES_WORLD, 0.1)


@mark.filterwarnings("ignore::DeprecationWarning")
def test_americas():
    w = world(MOCKED_NATURAL_EARTH)
    w.columns = map(str.lower, w.columns)
    config = AmericasConfig(include_dependencies=False)
    gdf = americas(world=w, config=config)
    assert isinstance(gdf, GeoDataFrame)
    diff = Index(AMERICAN_COUNTRIES).difference(gdf.index)
    print(diff)
    assert len(diff) == 0, "Countries are missing"
