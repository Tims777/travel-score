from dagster import asset
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from numpy import arange, pi
from pandas import DataFrame


@asset(group_name="visuals")
def histograms(combined_dataset: DataFrame) -> Figure:
    fields = [
        "hazard & exposure",
        "lack of coping capacity",
        "actual individual consumption",
        "natural score",
        "historic score",
        "tourism score",
    ]
    rows = 2
    cols = len(fields) // rows
    fig = plt.figure(figsize=(cols * 4, rows * 3), layout="tight")
    axs = fig.subplots(ncols=cols, nrows=rows)
    for ax, col in zip(axs.reshape(-1), fields):
        combined_dataset.plot.hist(column=col, ax=ax)
    return fig


@asset(group_name="visuals")
def radar_plot(travel_score: DataFrame) -> Figure:
    n = 3
    by = "total score"
    categories = ["Safety", "Affordability", "Attractiveness"]
    top_countries = travel_score.sort_values(by=by, ascending=False).head(n)
    fig, ax = plt.subplots(subplot_kw={"projection": "polar"}, figsize=(4, 3))
    theta = arange(len(categories)) * 2 * pi / len(categories)
    for idx in top_countries.index:
        country = top_countries.loc[idx]
        r = country[map(str.lower, categories)]
        ax.fill(theta, r, alpha=0.5, label=country["name"])
    ax.set_xticks(theta, categories)
    ax.set_title("Top Ranking Countries")
    fig.legend(loc="lower right")
    return fig


def scatter_plot(ax: Axes, df: DataFrame, x_col: str, y_col: str, index_col: str):
    x = df[x_col.lower()]
    y = df[y_col.lower()]
    labels = df[index_col.lower()]

    corr = x.corr(y)
    txt = f"Correlation: {corr:.3f}"
    ax.text(
        x=0.5,
        ha="center",
        y=0.95,
        va="top",
        s=txt,
        transform=ax.transAxes,
    )
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.scatter(x, y)

    for i, txt in enumerate(labels):
        ax.annotate(xy=(x[i], y[i]), text=txt, ha="center", va="bottom")
