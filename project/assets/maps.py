from ast import literal_eval
from typing import Generator
from dagster import (
    AssetExecutionContext,
    AssetOut,
    Output,
    asset,
    multi_asset,
)
from geopandas import GeoDataFrame
from matplotlib.figure import Figure

from project.assets.osm import OSM_KEYS

MISSING_VALUES_STYLE = {
    "color": "lightgrey",
    "label": "Missing values",
}


@asset(group_name="visuals")
def map_of_america(americas: GeoDataFrame) -> Figure:
    return americas.plot().get_figure()


@asset(group_name="visuals")
def price_map(combined_dataset: GeoDataFrame) -> Figure:
    return combined_dataset.plot(
        column="total consumption",
        missing_kwds=MISSING_VALUES_STYLE,
        legend=True,
    ).get_figure()


@asset(group_name="visuals")
def risk_map(combined_dataset: GeoDataFrame) -> Figure:
    return combined_dataset.plot(
        column="inform",
        missing_kwds=MISSING_VALUES_STYLE,
        legend=True,
    ).get_figure()


@asset(group_name="visuals")
def tourism_map(combined_dataset: GeoDataFrame) -> Figure:
    return combined_dataset.plot(
        column="tourism_score",
        missing_kwds=MISSING_VALUES_STYLE,
        legend=True,
    ).get_figure()


@asset(group_name="visuals")
def travel_score_map(travel_score: GeoDataFrame) -> Figure:
    return travel_score.plot(
        column="travel_score",
        missing_kwds=MISSING_VALUES_STYLE,
        legend=True,
    ).get_figure()


@multi_asset(
    outs={
        f"pbf_{key}_map": AssetOut(
            dagster_type=Figure,
            metadata={"osm_key": key},
            is_required=False,
        )
        for key in OSM_KEYS
    },
    can_subset=True,
    group_name="visuals",
)
def pbf_maps(
    context: AssetExecutionContext, pbf_analysis: GeoDataFrame
) -> Generator[Figure, None, None]:
    gdf = pbf_analysis
    for key in context.op_execution_context.selected_asset_keys:
        metadata = context.assets_def.metadata_by_key[key]
        [asset_name] = key.parts
        set_col = metadata["osm_key"]
        count_col = f"{set_col}_count"

        # Deserialize sets and count elements
        gdf[set_col] = gdf[set_col].map(literal_eval, na_action="ignore")
        gdf[count_col] = gdf[set_col].apply(lambda x: len(x) if x else 0)

        # Create map
        fig = gdf.plot(
            column=count_col,
            legend=True,
            markersize=1,
        ).get_figure()
        yield Output(fig, output_name=asset_name)


@asset(group_name="visuals")
def geobinning_test_map(pbf_analysis: GeoDataFrame, world: GeoDataFrame) -> Figure:
    gdf = pbf_analysis.sjoin(world, how="left")
    fig = gdf.plot(
        column="iso_a3",
        legend=True,
        markersize=1,
    ).get_figure()
    return fig
