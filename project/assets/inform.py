from json import loads
from urllib.parse import urlencode
from urllib.request import urlopen
from dagster import asset
from pandas import DataFrame, read_json


BASE_URL = "https://drmkc.jrc.ec.europa.eu/inform-index/API/InformAPI"
WORKFLOW_URL = f"{BASE_URL}/Workflows/Default"
DOWNLOAD_URL = f"{BASE_URL}/Countries/Scores"


@asset(group_name="urls")
def inform_scores_url() -> str:
    with urlopen(WORKFLOW_URL) as response:
        default_workflow = loads(response.read().decode())
        workflow_id = default_workflow["WorkflowId"]
    download_args = {"WorkflowId": workflow_id}
    return DOWNLOAD_URL + "?" + urlencode(download_args)


@asset(group_name="datasets")
def inform_scores_raw(inform_scores_url: str) -> DataFrame:
    return read_json(inform_scores_url)


@asset(group_name="datasets")
def inform_scores(inform_scores_raw: DataFrame) -> DataFrame:
    inform_scores_raw.drop_duplicates(
        subset=["Iso3", "IndicatorId", "IndicatorScore"], keep="first", inplace=True
    )
    return inform_scores_raw.pivot(
        index="Iso3", columns="IndicatorId", values="IndicatorScore"
    )
