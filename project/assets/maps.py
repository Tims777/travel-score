from dagster import asset
from geopandas import GeoDataFrame
from matplotlib.axes import Axes


@asset
def map_of_america(americas: GeoDataFrame) -> Axes:
    return americas.plot()


@asset
def price_map(combined_dataset: GeoDataFrame) -> Axes:
    return combined_dataset.plot(column="px.wl")


@asset
def risk_map(combined_dataset: GeoDataFrame) -> Axes:
    return combined_dataset.plot(column="inform")
