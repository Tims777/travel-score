from ast import literal_eval
from dagster import asset
from geopandas import GeoDataFrame
from matplotlib.figure import Figure


@asset(group_name="visuals")
def map_of_america(americas: GeoDataFrame) -> Figure:
    return americas.plot().get_figure()


@asset(group_name="visuals")
def price_map(combined_dataset: GeoDataFrame) -> Figure:
    return combined_dataset.plot(column="total consumption").get_figure()


@asset(group_name="visuals")
def risk_map(combined_dataset: GeoDataFrame) -> Figure:
    return combined_dataset.plot(column="inform").get_figure()


@asset(group_name="visuals")
def tourism_map(pbf_analysis: GeoDataFrame) -> Figure:
    gdf = pbf_analysis

    # Deserialize sets and count elements
    gdf["tourism"] = gdf["tourism"].map(literal_eval, na_action="ignore")
    gdf["tourism_count"] = gdf["tourism"].apply(lambda x: len(x) if x else 0)

    # Create map
    fig = gdf.plot(column="tourism_count", legend=True, markersize=2).get_figure()
    return fig
