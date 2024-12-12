from pandas import DataFrame
from pytest import mark
from project.assets.inform import inform_scores, inform_scores_raw
from project.tests.mocks import MOCKED_INFORM_RISK
from project.utils import N_COUNTRIES_WORLD, len_as_expected


INDEX = ["Iso3"]
COLUMNS = ["CC", "HA", "VU", "INFORM"]


@mark.filterwarnings("ignore::DeprecationWarning")
def test_inform_scores():
    raw = inform_scores_raw(MOCKED_INFORM_RISK)
    df = inform_scores(raw)
    assert isinstance(df, DataFrame)
    assert df.index.names == INDEX
    assert df.columns.difference(COLUMNS).empty
    assert len_as_expected(df, N_COUNTRIES_WORLD, 0.1)
