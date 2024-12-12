from dagster import asset
from pandas import DataFrame
from geopandas import GeoDataFrame


@asset(group_name="datasets")
def combined_dataset(
    americas: GeoDataFrame,
    inform_scores: DataFrame,
    price_level: DataFrame,
    tourism_score: DataFrame,
) -> GeoDataFrame:
    result = americas
    result = result.merge(inform_scores, left_on="iso_a3", right_on="Iso3", how="left")
    result = result.merge(
        price_level, left_on="iso_a3", right_on="country code", how="left"
    )
    result = result.merge(
        tourism_score, left_on="iso_a3", right_on="iso_a3", how="left"
    )
    return result


@asset(group_name="datasets")
def travel_score(combined_dataset: GeoDataFrame) -> GeoDataFrame:
    gdf = combined_dataset[[combined_dataset.active_geometry_name, "iso_a3"]]
    gdf["travel_score"] = (
        (combined_dataset["tourism_score"])
        * (100 / combined_dataset["total consumption"])
        * (5 / (combined_dataset["inform"]))
    )
    return gdf
