from dagster import asset
from geopandas import GeoDataFrame
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from numpy import array
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


@asset(group_name="visuals")
def benchmark(combined_dataset: GeoDataFrame, ttdi: DataFrame):
    joined = combined_dataset.merge(ttdi, on="iso", how="left")

    comparisons = [
        ("Price Competitiveness pillar", "Actual Individual Consumption"),
        ("Safety and Security pillar", "Hazard & Exposure"),
        ("Health and Hygiene pillar", "Lack of Coping Capacity"),
        ("Natural Resources pillar", "Natural score"),
        ("Cultural Resources pillar", "Historic score"),
        ("Tourist Services and Infrastructure pillar", "Tourism score"),
    ]

    nplots = array([3, 2])
    fig = plt.figure(figsize=nplots * 4, frameon=False)
    axs = fig.subplots(ncols=nplots[0], nrows=nplots[1])

    for ax, (x_col, y_col) in zip(axs.reshape(-1), comparisons):
        make_scatter_plot(
            ax=ax,
            df=joined,
            x_col=x_col,
            y_col=y_col,
            index_col="iso",
        )

    fig.tight_layout()

    return fig


def make_scatter_plot(ax: Axes, df: DataFrame, x_col: str, y_col: str, index_col: str):
    x = df[x_col.lower()]
    y = df[y_col.lower()]
    labels = df[index_col.lower()]

    corr = x.corr(y)
    txt = f"Correlation: {corr:.3f}"
    ax.text(
        x=0.95,
        horizontalalignment="right",
        y=0.95,
        verticalalignment="top",
        s=txt,
        transform=ax.transAxes,
    )
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.scatter(x, y, label=labels)

    for i, txt in enumerate(labels):
        ax.annotate(txt, (x[i], y[i]))
