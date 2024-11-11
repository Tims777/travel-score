from dagster import (
    AssetExecutionContext,
    MetadataValue,
    asset,
)
from pandas import DataFrame, read_json


@asset
def inform_scores(context: AssetExecutionContext) -> DataFrame:
    df = read_json(
        "https://drmkc.jrc.ec.europa.eu/inform-index/API/InformAPI/Countries/Scores/?WorkflowId=482&IndicatorId=INFORM,HA,VU,CC"
    )

    df = df.pivot(index="Iso3", columns="IndicatorId", values="IndicatorScore")

    context.add_output_metadata(
        {
            "num_records": len(df),
            "preview": MetadataValue.md(df.head().to_markdown()),
        }
    )

    return df
