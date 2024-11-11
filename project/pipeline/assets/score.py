from dagster import asset
from pandas import DataFrame


@asset
def travel_score(inform_scores: DataFrame) -> DataFrame:
    return inform_scores
