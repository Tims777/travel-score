from dagster import asset
from geopandas import GeoDataFrame
from matplotlib.figure import Figure


@asset
def map_of_america(americas: GeoDataFrame) -> Figure:
    return americas.plot().get_figure()


@asset
def price_map(combined_dataset: GeoDataFrame) -> Figure:
    return combined_dataset.plot(column="px.wl").get_figure()


@asset
def risk_map(combined_dataset: GeoDataFrame) -> Figure:
    return combined_dataset.plot(column="inform").get_figure()
