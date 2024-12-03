from pandas import DataFrame
from project.assets.inform import inform_scores


INDEX = ["Iso3"]
COLUMNS = ["CC", "HA", "VU", "INFORM"]
N_COUNTRIES = 195


def test_inform_scores():
    df = inform_scores()
    assert isinstance(df, DataFrame)
    assert df.index.names == INDEX
    assert df.columns.difference(COLUMNS).empty
    assert len(df) in range(int(N_COUNTRIES * 0.9), N_COUNTRIES + 1)
