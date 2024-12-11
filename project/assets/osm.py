from hashlib import md5
from pathlib import Path
from typing import Tuple
from urllib.parse import urljoin
from urllib.request import Request, urlopen

from dagster import (
    AssetExecutionContext,
    AssetKey,
    AssetSpec,
    MaterializeResult,
    MetadataValue,
    ResourceParam,
    multi_asset,
)

from project.resources.io_manager import LocalFileSystemIOManager


REGIONS = [
    "north-america",
    "central-america",
    "south-america",
]
VERSION = "latest"
SERVER = "https://download.geofabrik.de/"

RANGE_REGEX = r"^bytes (\d+)-(\d+)/(\d+)$"
CHUNK_SIZE = 1024 * 8

Ctx = AssetExecutionContext


def _get_local_checksum(ctx: Ctx, asset_key: AssetKey) -> str | None:
    last_materialization = ctx.instance.get_latest_materialization_event(asset_key)
    if not last_materialization:
        return None
    metadata = last_materialization.asset_materialization.metadata
    if "checksum" not in metadata:
        return None
    return metadata["checksum"].value


def _get_online_checksum(_ctx: Ctx, region: str, version: str) -> str:
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


@multi_asset(
    specs=[
        AssetSpec(
            f"{region}-pbf",
            metadata={"region": region, "version": "latest"},
            skippable=True,
        )
        for region in REGIONS
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

        online_checksum = _get_online_checksum(context, region, version)
        local_checksum = _get_local_checksum(context, key)

        if online_checksum == local_checksum:
            context.log.info(f"{asset_name} ({version}): Already downloaded.")
            return
        else:
            context.log.info(f"{asset_name} ({version}): Needs downloading.")

        outfile, written, new_checksum = _download_pbf(
            region=region,
            version=version,
            outdir=io_manager.data_dir,
            replace=local_checksum != online_checksum,
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
