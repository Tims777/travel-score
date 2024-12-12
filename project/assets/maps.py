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


@asset(group_name="visuals")
def map_of_america(americas: GeoDataFrame) -> Figure:
    return americas.plot().get_figure()


@asset(group_name="visuals")
def price_map(combined_dataset: GeoDataFrame) -> Figure:
    return combined_dataset.plot(column="total consumption").get_figure()


@asset(group_name="visuals")
def risk_map(combined_dataset: GeoDataFrame) -> Figure:
    return combined_dataset.plot(column="inform").get_figure()


@multi_asset(
    outs={
        f"{key}_map": AssetOut(
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
        fig = gdf.plot(column=count_col, legend=True, markersize=2).get_figure()
        yield Output(fig, output_name=asset_name)
