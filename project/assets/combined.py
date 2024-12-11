from dagster import asset
from pandas import DataFrame
from geopandas import GeoDataFrame


@asset(group_name="datasets")
def combined_dataset(
    americas: GeoDataFrame, inform_scores: DataFrame, price_level: DataFrame
) -> GeoDataFrame:
    result = americas
    result = result.merge(inform_scores, left_on="iso_a3", right_on="Iso3", how="left")
    result = result.merge(price_level, left_on="iso_a3", right_on="country code", how="left")
    return result
