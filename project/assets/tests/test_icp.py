from pandas import DataFrame
from project.assets.icp import icp_metrics, icp_metrics_2021


INDEX = ["Country Code", "Classification Code", "Series Code"]
N_COUNTRIES = 195
N_BENCHMARKS = 12
N_TOTAL = N_COUNTRIES + N_BENCHMARKS


def test_icp_metrics():
    df = icp_metrics()
    assert isinstance(df, DataFrame)
    assert len(df) in range(int(N_TOTAL * 0.9), N_TOTAL + 1)
