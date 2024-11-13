from io import BytesIO
import re
from zipfile import ZipFile
from dagster import asset
from pandas import DataFrame, read_csv
from urllib.request import urlopen


DOWNLOAD_URL = "https://databank.worldbank.org/AjaxDownload/FileDownloadHandler.ashx"
PREPARE_URL = "https://databank.worldbank.org/AjaxDownload/FileInfoHandler.ashx"
PREPARE_ARGS = {
    "reqtype": "data",
    "data-option-radio": "data-download",
    "down-radio": "csv",
    "ddl-text-delimiter": "undefined",
    "ddl-export-range": "full",
    "ddl-data-format": "Table",
    "ddl-variable-format": "Codes",
    "ddl-na-preference": "NA",
    "hdnEditMode": "undefined",
    "ddl-export-notes": "N",
    "dataset-name": "undefined",
    "chk-scale-precision": "N",
}


def prepare_download():
    # req = Request(PREPARE_URL, data=urlencode(PREPARE_ARGS).encode())
    # req.headers.update(
    #     {
    #         "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    #         "ADRUM": "isAjax:true",
    #     }
    # )
    # with urlopen(req) as resp:
    #     zip_url = DOWNLOAD_URL + "?" + resp.read().decode()
    # return zip_url
    return "https://databank.worldbank.org/AjaxDownload/FileDownloadHandler.ashx?filename=P_264b2820-c9ea-47b0-afd9-023bed6b537f.zip&filetype=CSV&language=en&displayfile=P_Data_Extract_From_ICP_2021.zip"


def extract_csv_from_zip(zip: ZipFile, pattern: str):
    [file_name] = [n for n in zip.namelist() if re.match(pattern, n)]
    with zip.open(file_name) as csv_file:
        return read_csv(csv_file)


@asset
def icp_metrics() -> DataFrame:
    zip_url = prepare_download()

    with urlopen(zip_url) as resp:
        data = resp.read()

    with ZipFile(BytesIO(data)) as zip:
        df = extract_csv_from_zip(zip, r"^.*Data\.csv$")

    df.drop(df.tail(5).index, inplace=True)
    df.set_index(["Country Code", "Classification Code", "Series Code"], inplace=True)

    return df


@asset
def icp_metrics_2021(icp_metrics: DataFrame) -> DataFrame:
    pivoted = icp_metrics.pivot(
        index=["Country Code"],
        columns=["Classification Code", "Series Code"],
        values=["YR2021"],
    )
    pivoted.columns = [":".join(map(str, col[1:])) for col in pivoted.columns]
    return pivoted
