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


def _plot(gdf: GeoDataFrame, column: str) -> Figure:
    ax = gdf.plot.geo(
        column=column,
        missing_kwds=MISSING_VALUES_STYLE,
        legend=True,
    )
    ax.set_axis_off()
    return ax.get_figure()


@asset(group_name="visuals")
def affordability_map(travel_score: GeoDataFrame) -> Figure:
    return _plot(travel_score, "affordability")


@asset(group_name="visuals")
def safety_map(travel_score: GeoDataFrame) -> Figure:
    return _plot(travel_score, "safety")


@asset(group_name="visuals")
def attractiveness_map(travel_score: GeoDataFrame) -> Figure:
    return _plot(travel_score, "attractiveness")


@asset(group_name="visuals")
def travel_score_map(travel_score: GeoDataFrame) -> Figure:
    return _plot(travel_score, column="total score")


@asset(group_name="visuals")
def map_of_america(americas: GeoDataFrame) -> Figure:
    return _plot(americas, "continent")


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
        fig = _plot(gdf, count_col)
        yield Output(fig, output_name=asset_name)


@asset(group_name="visuals")
def geobinning_test_map(pbf_analysis: GeoDataFrame, world: GeoDataFrame) -> Figure:
    gdf = pbf_analysis.sjoin(world, how="left")
    return _plot(gdf, "mapcolor7")
