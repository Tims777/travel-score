from io import BytesIO
import re
from urllib.parse import urlencode
from zipfile import ZipFile
from dagster import asset
from pandas import DataFrame, read_csv
from urllib.request import urlopen


DOWNLOAD_URL = "https://databank.worldbank.org/AjaxDownload/FileDownloadHandler.ashx"
DOWNLOAD_ARGS = {
    "filename": "P_8d54d70d-f0de-4d4e-85f5-9b3443b15ad9.zip",
    "filetype": "CSV",
    "language": "en",
    "displayfile": "P_Data_Extract_From_ICP_2021.zip",
}


def extract_csv_from_zip(zip: ZipFile, pattern: str):
    [file_name] = [n for n in zip.namelist() if re.match(pattern, n)]
    with zip.open(file_name) as csv_file:
        return read_csv(csv_file)


@asset(group_name="datasets")
def icp_metrics() -> DataFrame:
    zip_url = DOWNLOAD_URL + "?" + urlencode(DOWNLOAD_ARGS)

    with urlopen(zip_url) as resp:
        data = resp.read()

    with ZipFile(BytesIO(data)) as zip:
        df = extract_csv_from_zip(zip, r"^.*Data\.csv$")

    df.drop(df.tail(5).index, inplace=True)
    df.set_index(["Country Code", "Classification Code", "Series Code"], inplace=True)

    return df


@asset(group_name="datasets")
def icp_metrics_2021(icp_metrics: DataFrame) -> DataFrame:
    pivoted = icp_metrics.pivot(
        index=["Country Code"],
        columns=["Classification Code"],
        values=["YR2021"],
    )
    pivoted.columns = [col[1] for col in pivoted.columns]
    return pivoted
