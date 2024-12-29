from dagster import asset
from pandas import DataFrame
from geopandas import GeoDataFrame


@asset(group_name="datasets")
def combined_dataset(
    americas: GeoDataFrame,
    inform_scores: DataFrame,
    price_level: DataFrame,
    resources_score: DataFrame,
) -> GeoDataFrame:
    result = americas
    result = result.merge(inform_scores, on="iso", how="left")
    result = result.merge(price_level, on="iso", how="left")
    result = result.merge(resources_score, on="iso", how="left")
    result.set_index("iso", inplace=True)
    return result


@asset(group_name="datasets")
def travel_score(combined_dataset: GeoDataFrame) -> GeoDataFrame:
    combined_dataset.set_index("iso", inplace=True)
    gdf = combined_dataset[[combined_dataset.active_geometry_name]]
    gdf["travel score"] = (
        1.0
        * (100 / combined_dataset["actual individual consumption"])
        * (5 / (combined_dataset["hazard & exposure"]))
        * (5 / (combined_dataset["lack of coping capacity"]))
        * (combined_dataset["tourism score"])
        * (combined_dataset["natural score"])
        * (combined_dataset["historic score"])
    )
    return gdf
