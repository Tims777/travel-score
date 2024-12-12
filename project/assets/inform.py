from urllib.parse import urlencode
from dagster import asset
from pandas import DataFrame, read_json


DOWNLOAD_URL = (
    "https://drmkc.jrc.ec.europa.eu/inform-index/API/InformAPI/Countries/Scores/"
)
DOWNLOAD_ARGS = {
    "WorkflowId": 482,
    "IndicatorId": ",".join(["INFORM", "HA", "VU", "CC"]),
}


@asset
def inform_scores_url() -> str:
    return DOWNLOAD_URL + "?" + urlencode(DOWNLOAD_ARGS)


@asset(group_name="datasets")
def inform_scores(inform_scores_url: str) -> DataFrame:
    df = read_json(inform_scores_url)
    return df.pivot(index="Iso3", columns="IndicatorId", values="IndicatorScore")
