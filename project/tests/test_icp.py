from pandas import DataFrame
from pytest import mark
from project.assets.icp import icp_metrics
from project.tests.mocks import MOCKED_ICP_CYCLE
from project.utils import N_COUNTRIES_WORLD, len_as_expected


@mark.filterwarnings("ignore::DeprecationWarning")
def test_icp_metrics():
    df = icp_metrics(MOCKED_ICP_CYCLE)
    assert isinstance(df, DataFrame)
    classifications = df.index.get_level_values("Classification Code").unique()
    years = df.index.get_level_values("Time Code").unique()
    expected = N_COUNTRIES_WORLD * len(classifications) * len(years)
    assert len_as_expected(df, expected, 0.1)
