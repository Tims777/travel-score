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
