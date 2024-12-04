from pandas import DataFrame
from project.assets.inform import inform_scores
from project.utils import N_COUNTRIES_WORLD, len_as_expected


INDEX = ["Iso3"]
COLUMNS = ["CC", "HA", "VU", "INFORM"]


def test_inform_scores():
    df = inform_scores()
    assert isinstance(df, DataFrame)
    assert df.index.names == INDEX
    assert df.columns.difference(COLUMNS).empty
    assert len_as_expected(df, N_COUNTRIES_WORLD, 0.1)
