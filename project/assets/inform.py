from json import loads
from urllib.parse import urlencode
from urllib.request import urlopen
from dagster import asset
from pandas import DataFrame, read_json


BASE_URL = "https://drmkc.jrc.ec.europa.eu/inform-index/API/InformAPI"
WORKFLOW_URL = f"{BASE_URL}/Workflows/Default"
DOWNLOAD_URL = f"{BASE_URL}/Countries/Scores"

TOP_LEVEL_INDICATORS = {
    "inform": "inform risk index",
    "cc": "lack of coping capacity",
    "cc.inf": "lack of coping capacity (infrastructure)",
    "cc.ins": "lack of coping capacity (institutional)",
    "ha": "hazard & exposure",
    "ha.hum": "hazard & exposure (human)",
    "ha.nat": "hazard & exposure (natural)",
    "vu": "vulnerability index",
    "vu.sev": "vulnerability index (socio-economic)",
    "vu.vgr": "vulnerability index (vulnerable groups)",
}


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
    # Lowercase all indicator ids
    df = inform_scores_raw
    df["IndicatorId"] = df["IndicatorId"].map(str.lower)

    # Drop duplicate indicator scores
    df.drop_duplicates(
        subset=["Iso3", "IndicatorId", "IndicatorScore"], keep="first", inplace=True
    )

    # Map indicator scores to indicator ids
    df = df.pivot(index="Iso3", columns="IndicatorId", values="IndicatorScore")

    # Keep selected indicators and rename columns titles
    df = df[(k for k in TOP_LEVEL_INDICATORS.keys() if k in df)]
    df.rename(columns=lambda x: TOP_LEVEL_INDICATORS.get(x), inplace=True)
    df.rename_axis("iso", inplace=True)
    return df
