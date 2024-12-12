from pandas import DataFrame
from project.assets.icp import icp_metrics
from project.utils import N_COUNTRIES_WORLD, len_as_expected


INDEX = ["Country Code", "Classification Code", "Series Code"]

SELF_HOSTED_ICP_METRICS = (
    "https://gist.github.com/Tims777/c213bbfd354ae27628651937062b2acb/raw/5452aa642b1e595462e7dbdd378044693d31aba5/"
    "P_ICP-2021-Cycle.zip"
)


def test_icp_metrics():
    df = icp_metrics(SELF_HOSTED_ICP_METRICS)
    assert isinstance(df, DataFrame)
    classifications = df.index.get_level_values("Classification Code").unique()
    years = df.index.get_level_values("Time Code").unique()
    expected = N_COUNTRIES_WORLD * len(classifications) * len(years)
    assert len_as_expected(df, expected, 0.1)
