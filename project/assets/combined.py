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
    min = 0
    max = df[col].mean() * 2
    df[col] = (df[col] - min) / (max - min)
    df[col].clip(upper=1.0, inplace=True)


@asset(group_name="datasets")
def travel_score(combined_dataset: GeoDataFrame) -> GeoDataFrame:
    # Prepare dataframes
    df = combined_dataset
    df.set_index("iso", inplace=True)
    gdf = df[[df.active_geometry_name, "name", "continent"]]

    # Calculate base indicators
    gdf["safety"] = 1 / (df["hazard & exposure"] + df["lack of coping capacity"])
    gdf["affordability"] = 1 / (df["actual individual consumption"])
    gdf["attractiveness"] = (
        df["natural score"] + df["historic score"] + df["tourism score"]
    )

    # Normalize base indicators
    for col in ("safety", "affordability", "attractiveness"):
        _normalize(gdf, col)

    # Calculate and normalize total score
    gdf["total score"] = gdf["safety"] * gdf["affordability"] * gdf["attractiveness"]
    _normalize(gdf, "total score")

    return gdf
