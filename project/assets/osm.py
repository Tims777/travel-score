from ast import literal_eval
from collections import defaultdict
from io import BytesIO
from os import environ
from zipfile import ZipFile
from geopandas import GeoDataFrame, read_file
from hashlib import md5
from pathlib import Path
from typing import Dict, Set, Tuple
from urllib.parse import urljoin
from urllib.request import Request, urlopen

from dagster import (
    AssetExecutionContext,
    AssetSpec,
    Config,
    EventLogEntry,
    MaterializeResult,
    MetadataValue,
    ResourceParam,
    asset,
    multi_asset,
)
from numpy import mean
from osmium import FileProcessor
from osmium.filter import KeyFilter
from osmium.osm import NODE
from pandas import DataFrame, NamedAgg
from shapely import Polygon

from project.utils import CHUNK_SIZE, YES
from project.resources.io_manager import ENCODING, LocalFileSystemIOManager
from project.tests.mocks import PRECOMPUTED_PBF_ANALYSIS


REGIONS = [
    "north-america",
    "central-america",
    "south-america",
]
VERSION = "latest"
SERVER = "https://download.geofabrik.de/"

PBF_ASSETS = {"_".join(["pbf"] + region.split("-")): region for region in REGIONS}

OSM_KEYS = "amenity", "historic", "leisure", "natural", "shop", "tourism"
DEFAULT_RESOLUTION = 2


def _get_local_checksum(latest_materialization: EventLogEntry | None) -> str | None:
    if not latest_materialization:
        return None
    metadata = latest_materialization.asset_materialization.metadata
    if "checksum" not in metadata:
        return None
    return metadata["checksum"].value


def _get_online_checksum(region: str, version: str) -> str:
    filename = f"{region}-{version}.osm.pbf.md5"
    with urlopen(urljoin(SERVER, filename)) as resp:
        data = resp.read()
        checksum, _ = data.split(maxsplit=1)
        return checksum.decode()


def _download_pbf(
    region: str,
    version: str,
    outdir: str = ".",
    replace: bool = False,
) -> Tuple[Path, int, bytes]:
    filename = f"{region}-{version}.osm.pbf"
    url = urljoin(SERVER, filename)
    outfile = Path(outdir).joinpath(filename)

    with outfile.open("ab+") as fd:
        # Continue download unless replace is True
        start = 0 if replace else fd.tell()
        fd.truncate(start)

        # Calculate checksum of existing data
        checksum = md5()
        fd.seek(0)
        while chunk := fd.read(CHUNK_SIZE):
            checksum.update(chunk)

        # HEAD
        req = Request(url, method="HEAD")
        with urlopen(req) as resp:
            content_length = int(resp.headers.get("Content-Length"))
            accept_ranges = resp.headers.get("Accept-Ranges")
        if start == content_length:
            return outfile, 0, checksum.digest().hex()

        # GET
        req = Request(url, method="GET")
        if accept_ranges == "bytes":
            req.add_header("Range", f"bytes={start}-")
        with urlopen(req) as resp:
            while chunk := resp.read(CHUNK_SIZE):
                fd.write(chunk)
                checksum.update(chunk)
            assert content_length == fd.tell()

        # Return amount of written bytes and checksum
        written = content_length - start
        return outfile, written, checksum.digest().hex()


type Coords = Tuple[int, int]
type Features = Dict[set, Set[str]]
type GeoBins = Dict[Coords, Features]


def _process_pbf(pbf_file: str, bins: GeoBins, res: float) -> GeoBins:
    fp = FileProcessor(pbf_file, NODE).with_filter(KeyFilter(*OSM_KEYS))
    for obj in fp:
        coords = tuple(
            round(c * res) / res for c in (obj.location.lon, obj.location.lat)
        )
        for key in OSM_KEYS:
            if key not in obj.tags:
                continue
            bins[coords][key].add(obj.tags[key])


def _square(coords: Coords, res: float):
    x, y = coords
    d = 1 / (res * 2)
    return ((x - d, y - d), (x + d, y - d), (x + d, y + d), (x - d, y + d))


def _load_precomputed_analysis() -> GeoDataFrame:
    with urlopen(PRECOMPUTED_PBF_ANALYSIS) as resp:
        data = resp.read()
    with ZipFile(BytesIO(data)) as zip:
        [file] = zip.filelist
        with zip.open(file) as fd:
            return read_file(fd, encoding=ENCODING)


@multi_asset(
    specs=[
        AssetSpec(
            pbf,
            metadata={"region": region, "version": "latest"},
            skippable=True,
        )
        for pbf, region in PBF_ASSETS.items()
    ],
    can_subset=True,
    group_name="pbfs",
)
def pbfs(
    context: AssetExecutionContext, io_manager: ResourceParam[LocalFileSystemIOManager]
):
    for key in context.op_execution_context.selected_asset_keys:
        [asset_name] = key.parts
        metadata = context.assets_def.metadata_by_key[key]
        region = metadata["region"]
        version = metadata["version"]

        latest_materialization = context.instance.get_latest_materialization_event(key)
        local_checksum = _get_local_checksum(latest_materialization)
        online_checksum = _get_online_checksum(region, version)

        if not local_checksum:
            context.log.info(f"{asset_name} ({version}): Not previously materialized")
            replace = False
        elif online_checksum != local_checksum:
            context.log.info(f"{asset_name} ({version}): Checksum mismatch")
            replace = True
        else:
            context.log.info(f"{asset_name} ({version}): Checksum okay")
            return

        outfile, written, new_checksum = _download_pbf(
            region=region,
            version=version,
            outdir=io_manager.data_dir,
            replace=replace,
        )
        context.log.info(f"Downloaded {written} bytes to {outfile}")
        context.log.info(f"Online checksum: {online_checksum}, local: {new_checksum}")
        assert online_checksum == new_checksum
        yield MaterializeResult(
            asset_key=key,
            metadata={
                "filepath": MetadataValue.path(outfile),
                "checksum": MetadataValue.text(new_checksum),
                "size (bytes)": MetadataValue.int(outfile.stat().st_size),
            },
        )


class PBFAnalysisConfig(Config):
    skip_analysis: bool = environ.get("SKIP_PBF_ANALYSIS", "").lower() in YES
    resolution: float = DEFAULT_RESOLUTION


@asset(group_name="datasets", deps=PBF_ASSETS.keys())
def pbf_analysis(
    context: AssetExecutionContext, config: PBFAnalysisConfig
) -> GeoDataFrame:
    if config.skip_analysis:
        context.log.info("Loading precomputed PBF analysis.")
        return _load_precomputed_analysis()
    keys = context.instance.get_asset_keys()
    bins: GeoBins = defaultdict(lambda: defaultdict(set))
    for key in keys:
        if len(key.parts) != 1:
            continue
        [asset_name] = key.parts
        if asset_name not in PBF_ASSETS:
            continue
        materialization = context.instance.get_latest_materialization_event(key)
        if not materialization:
            context.log.warning(f"{asset_name} has not been materialized yet!")
            continue
        metadata = materialization.asset_materialization.metadata
        pbf_file = metadata["filepath"].value
        context.log.info(f"Processing {pbf_file}")
        _process_pbf(pbf_file, bins, config.resolution)
    dps = []
    for coords, features in bins.items():
        geometry = {"geometry": Polygon(_square(coords, config.resolution))}
        dps.append(geometry | features)
    return GeoDataFrame(dps)


@asset(group_name="datasets")
def resources_score(pbf_analysis: GeoDataFrame, world: GeoDataFrame) -> DataFrame:
    # Prepare pbf_analysis dataset
    non_geo = pbf_analysis.columns.difference([pbf_analysis.active_geometry_name])
    pbf_analysis[non_geo] = pbf_analysis[non_geo].map(literal_eval, na_action="ignore")

    # Prepare world dataset
    world.set_index("iso_a3", inplace=True)
    world.drop(index="-99", inplace=True)
    world.rename_axis("iso", inplace=True)
    world = world[[world.active_geometry_name]]

    # Perform spatial join to map points to countries
    gdf = pbf_analysis.sjoin(world, how="left")
    gdf = gdf[gdf["iso"].notna()]
    assert isinstance(gdf, GeoDataFrame)

    # Count values
    for key in OSM_KEYS:
        count_field = f"{key} count"
        gdf[count_field] = gdf[key].apply(lambda x: len(x) if x else 0)

    # Aggregate counts by country
    result = DataFrame(index=gdf["iso"].unique())
    grouped = gdf.groupby("iso")
    for key in OSM_KEYS:
        count_field = f"{key} count"
        score_field = f"{key} score"
        max_field = f"{key} max"
        min_field = f"{key} min"
        avg_field = f"{key} avg"
        result = result.join(
            grouped.agg(
                **{
                    max_field: NamedAgg(column=count_field, aggfunc="max"),
                    min_field: NamedAgg(column=count_field, aggfunc="min"),
                    avg_field: NamedAgg(column=count_field, aggfunc="mean"),
                }
            )
        )
        result[score_field] = result[max_field] / mean(result[max_field])

    # Rename axis and return
    result.rename_axis("iso", inplace=True)
    return result
