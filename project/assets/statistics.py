from dagster import asset
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
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


def scatter_plot(ax: Axes, df: DataFrame, x_col: str, y_col: str, index_col: str):
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
