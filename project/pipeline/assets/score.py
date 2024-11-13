from dagster import asset
from pandas import DataFrame


@asset
def travel_score(inform_scores: DataFrame, icp_metrics_2021: DataFrame) -> DataFrame:
    inform_scores.set_index("Iso3", inplace=True)
    icp_metrics_2021.set_index("Country Code", inplace=True)
    df = inform_scores.join(icp_metrics_2021)
    # df["TRAVEL"] = df["INFORM"] + 0.7
    # result = df[["Iso3", "TRAVEL"]]
    # result.set_index("Iso3", inplace=True)
    return df
