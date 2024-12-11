from io import BytesIO
from re import match, sub
from urllib.parse import urlencode
from zipfile import ZipFile
from dagster import AssetExecutionContext, asset
from pandas import DataFrame, IndexSlice, read_csv, to_numeric
from urllib.request import Request, urlopen

PREPARE_URL = "https://databank.worldbank.org/AjaxDownload/FileInfoHandler.ashx"
DOWNLOAD_URL = "https://databank.worldbank.org/AjaxDownload/FileDownloadHandler.ashx"
PREPARE_ARGS = {
    "reqtype": "csv",
    "from": "widget-preview",
    "reportid": "153619",
    "reporttype": "Table",
    "internal": "",
    "lang": "en",
}

INDEX_COLS = ["Classification Code", "Time Code", "Country Code"]
NAME_COLS = ["Classification Name", "Time", "Country Name"]


def extract_csv_from_zip(zip: ZipFile, pattern: str):
    [file_name] = [n for n in zip.namelist() if match(pattern, n)]
    with zip.open(file_name) as csv_file:
        return read_csv(csv_file)


def extract_name(title: str):
    return sub(r"(\d+):(.+) \[(\d+)\]$", lambda y: y[2], title)


@asset(group_name="urls")
def icp_metrics_url() -> str:
    request = Request(PREPARE_URL, data=urlencode(PREPARE_ARGS).encode(), method="POST")
    with urlopen(request) as response:
        download_args = response.read()
    return DOWNLOAD_URL + "?" + download_args.decode()


@asset(group_name="datasets")
def icp_metrics(icp_metrics_url: str) -> DataFrame:

    # Download and extract data
    with urlopen(icp_metrics_url) as resp:
        data = resp.read()
    with ZipFile(BytesIO(data)) as zip:
        df = extract_csv_from_zip(zip, r"^.*Data\.csv$")

    # Configure index
    df.set_index(INDEX_COLS, inplace=True)

    # Drop metadata
    df.drop(df.head(1).index, inplace=True)
    df.drop(df.tail(5).index, inplace=True)
    df.drop(columns=NAME_COLS, inplace=True)

    # Drop empty columns
    df.dropna(axis="columns", how="all", inplace=True)

    # Fix data types (all non-index columns are numeric)
    df = df.apply(to_numeric)

    return df


@asset(group_name="datasets")
def price_level(context: AssetExecutionContext, icp_metrics: DataFrame) -> DataFrame:

    # Restore index
    icp_metrics.set_index(INDEX_COLS, inplace=True)

    # Select price level data for latest available year
    year = 2021
    df = icp_metrics.loc[IndexSlice["PX.WL", f"YR{year}", :], :]
    df = df.droplevel(INDEX_COLS[0:2])
    context.add_output_metadata({"year": year})

    # Drop empty columns
    df.dropna(axis="columns", how="all", inplace=True)

    # Rename columns to be more human readable
    df.rename(columns=lambda x: extract_name(x).lower(), inplace=True)
    df.rename_axis(INDEX_COLS[2].lower(), axis=0, inplace=True)

    return df
