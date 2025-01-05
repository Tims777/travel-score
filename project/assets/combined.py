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
    df[col] = ((df[col] - min) / (max - min)).clip(upper=1.0)


@asset(group_name="datasets")
def travel_score(combined_dataset: GeoDataFrame) -> GeoDataFrame:
    # Prepare dataframes
    cdf = combined_dataset
    cdf.set_index("iso", inplace=True)
    rdf = GeoDataFrame(cdf[[cdf.active_geometry_name, "name", "continent"]])

    # Calculate base indicators
    rdf["safety"] = 1 / (cdf["hazard & exposure"] + cdf["lack of coping capacity"])
    rdf["affordability"] = 1 / (cdf["actual individual consumption"])
    rdf["attractiveness"] = (
        cdf["natural score"] + cdf["historic score"] + cdf["tourism score"]
    )

    # Normalize base indicators
    for col in ("safety", "affordability", "attractiveness"):
        _normalize(rdf, col)

    # Calculate and normalize total score
    rdf["total score"] = rdf["safety"] * rdf["affordability"] * rdf["attractiveness"]
    _normalize(rdf, "total score")

    return rdf
