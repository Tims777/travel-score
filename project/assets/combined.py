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


def _normalize(df: DataFrame, col: str):
    min = df[col].min()
    max = df[col].max()
    df[col] = 2.0 * (df[col] - min) / (max - min)


@asset(group_name="datasets")
def travel_score(combined_dataset: GeoDataFrame) -> GeoDataFrame:
    # Prepare dataframes
    df = combined_dataset
    df.set_index("iso", inplace=True)
    gdf = df[[df.active_geometry_name]]

    # Calculate base indicators
    gdf["safety"] = 1 / (df["hazard & exposure"] + df["lack of coping capacity"])
    gdf["affordability"] = 1 / (df["actual individual consumption"])
    gdf["attractiveness"] = (
        df["natural score"] + df["historic score"] + df["tourism score"]
    )

    # Normalize base indicators
    for col in ("safety", "affordability", "attractiveness"):
        _normalize(gdf, col)

    # Calculate total score
    gdf["total score"] = gdf["safety"] * gdf["affordability"] * gdf["attractiveness"]

    return gdf
