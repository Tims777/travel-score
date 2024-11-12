from dagster import asset
from pandas import DataFrame


@asset
def travel_score(inform_scores: DataFrame) -> DataFrame:
    df = inform_scores
    df["TRAVEL"] = df["INFORM"] + 0.7
    result = df[["Iso3", "TRAVEL"]].set_index("Iso3")
    return result
