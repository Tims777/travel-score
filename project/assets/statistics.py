from dagster import asset
from geopandas import GeoDataFrame
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from pandas import DataFrame


@asset(group_name="visuals")
def correlation(combined_dataset: GeoDataFrame) -> Figure:
    price = combined_dataset["total consumption"]
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
def price_histogram(price_level: DataFrame) -> Figure:
    return price_level.plot.hist(column="total consumption").get_figure()


@asset(group_name="visuals")
def risk_histogram(inform_scores: DataFrame) -> Figure:
    return inform_scores.plot.hist(column="INFORM").get_figure()
