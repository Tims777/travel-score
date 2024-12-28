from ast import literal_eval
from dagster import asset
from pandas import DataFrame, MultiIndex, read_excel


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
    df.rename(columns=lambda x: x.replace("\n", " ").lower(), inplace=True)
    df.rename_axis("iso", inplace=True)
    return df
