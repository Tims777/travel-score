from pandas import DataFrame
from project.assets.icp import icp_metrics
from project.utils import N_COUNTRIES_WORLD, len_as_expected


INDEX = ["Country Code", "Classification Code", "Series Code"]


def test_icp_metrics():
    df = icp_metrics()
    assert isinstance(df, DataFrame)
    assert len_as_expected(df, N_COUNTRIES_WORLD, 0.1)
