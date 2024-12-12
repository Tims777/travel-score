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
    EventLogEntry,
    MaterializeResult,
    MetadataValue,
    ResourceParam,
    asset,
    multi_asset,
)
from osmium import FileProcessor
from osmium.filter import KeyFilter
from osmium.osm import NODE
from shapely import Point

from project.resources.io_manager import ENCODING, LocalFileSystemIOManager
from project.tests.mocks import PRECOMPUTED_PBF_ANALYSIS


REGIONS = [
    "north-america",
    "central-america",
    "south-america",
]
VERSION = "latest"
SERVER = "https://download.geofabrik.de/"

RANGE_REGEX = r"^bytes (\d+)-(\d+)/(\d+)$"
CHUNK_SIZE = 1024 * 8

PBF_ASSETS = {"_".join(["pbf"] + region.split("-")): region for region in REGIONS}

OSM_KEYS = "amenity", "historic", "leisure", "natural", "shop", "tourism"
RESOLUTION = 0


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


def _process_pbf(pbf_file: str, bins: GeoBins) -> GeoBins:
    fp = FileProcessor(pbf_file, NODE).with_filter(KeyFilter(*OSM_KEYS))
    for obj in fp:
        coords = tuple(
            round(x, RESOLUTION) for x in (obj.location.lat, obj.location.lon)
        )
        for key in OSM_KEYS:
            if key not in obj.tags:
                continue
            bins[coords][key].add(obj.tags[key])


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
    group_name="tempfiles",
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


@asset(group_name="datasets", deps=PBF_ASSETS.keys())
def pbf_analysis(context: AssetExecutionContext) -> GeoDataFrame:
    if environ.get("SKIP_PBF_ANALYSIS"):
        return _load_precomputed_analysis()
    bins: GeoBins = defaultdict(lambda: defaultdict(set))
    for key in context.instance.get_asset_keys():
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
        _process_pbf(pbf_file, bins)
    dps = []
    for coords, features in bins.items():
        geometry = {"geometry": Point(*reversed(coords))}
        dps.append(geometry | features)
    return GeoDataFrame(dps)
