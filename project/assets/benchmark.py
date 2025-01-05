from ast import literal_eval
from os import environ
from dagster import asset
from matplotlib import figure
from numpy import array
from pandas import DataFrame, MultiIndex, read_excel
from geopandas import GeoDataFrame

from project.assets.statistics import scatter_plot
from project.utils import YES


if environ.get("BENCHMARK") in YES:

    DOWNLOAD_URL = "https://www3.weforum.org/docs/WEF_TTDI_2024_edition_data.xlsx"

    @asset(group_name="urls")
    def ttdi_url() -> str:
        return DOWNLOAD_URL

    @asset(group_name="datasets")
    def ttdi_raw(ttdi_url: str) -> DataFrame:
        df = read_excel(ttdi_url, header=[0, 1], index_col=0)
        return df

    @asset(group_name="datasets")
    def ttdi(ttdi_raw: DataFrame) -> DataFrame:
        df = ttdi_raw
        df.set_index(df.columns[0], inplace=True)
        df.columns = MultiIndex.from_tuples([literal_eval(x) for x in df.columns])
        df = df.loc[:, (slice(None), "2024 Value")]
        df = df.droplevel(1, axis=1)
        df.rename(columns=lambda x: x.replace("\n", " ").lower().strip(), inplace=True)
        df.rename_axis("iso", inplace=True)
        return df

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
        fig = figure(figsize=nplots * 4, frameon=False)
        axs = fig.subplots(ncols=nplots[0], nrows=nplots[1])

        for ax, (x_col, y_col) in zip(axs.reshape(-1), comparisons):
            scatter_plot(
                ax=ax,
                df=joined,
                x_col=x_col,
                y_col=y_col,
                index_col="iso",
            )

        fig.tight_layout()

        return fig
