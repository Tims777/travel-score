from urllib.parse import urlencode
from urllib.request import urlopen
from dagster import asset
from pandas import DataFrame, read_json


DOWNLOAD_URL = (
    "https://drmkc.jrc.ec.europa.eu/inform-index/API/InformAPI/Countries/Scores/"
)
DOWNLOAD_ARGS = {
    "WorkflowId": 482,
    "IndicatorId": ",".join(["INFORM", "HA", "VU", "CC"]),
}


@asset(group_name="datasets")
def inform_scores() -> DataFrame:
    url = DOWNLOAD_URL + "?" + urlencode(DOWNLOAD_ARGS)
    with urlopen(url) as resp:
        df = read_json(resp)
    return df.pivot(index="Iso3", columns="IndicatorId", values="IndicatorScore")
