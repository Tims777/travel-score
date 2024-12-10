from dagster import asset
from geopandas import GeoDataFrame
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from pandas import DataFrame


@asset(group_name="visuals")
def correlation(combined_dataset: GeoDataFrame) -> Figure:
    price = combined_dataset["px.wl"]
    risk = combined_dataset["inform"]
    corr = price.corr(risk)
    fig = plt.figure()
    ax = fig.gca()
    txt = f"Correlation: {corr:.3f}"
    ax.text(
        x=0.95,
        horizontalalignment="right",
        y=0.95,
        verticalalignment="top",
        s=txt,
        transform=ax.transAxes,
    )
    ax.scatter(price, risk)
    return fig


@asset(group_name="visuals")
def pricelevel_histogram(icp_metrics_2021: DataFrame) -> Figure:
    ax = icp_metrics_2021.plot.hist(column="PX.WL")
    return ax.get_figure()


@asset(group_name="visuals")
def risk_histogramm(inform_scores: DataFrame) -> Figure:
    ax = inform_scores.plot.hist(column="INFORM")
    return ax.get_figure()
