from pathlib import Path
from sqlite3 import connect
from typing import List, Mapping, TypeAlias
from dagster import (
    AssetKey,
    ConfigurableIOManager,
    InputContext,
    MetadataValue,
    OutputContext,
)
from matplotlib.figure import Figure
from pandas import DataFrame, read_sql
from geopandas import GeoDataFrame, read_file

ENCODING = "utf-8"
DB_SUFFIX = ".sqlite"
DB_DRIVER = "SQLite"
FIG_SUFFIX = ".svg"
TXT_SUFFIX = ".txt"
LICENSE_SUFFIX = ".license"

LICENSE_FILE_HEADER = (
    "# License Information\n\n"
    "The dataset '{0}' contains data from the following sources.\n"
)

AssetType: TypeAlias = None | DataFrame | GeoDataFrame | Figure | str


class LocalFileSystemIOManager(ConfigurableIOManager):
    """Translates between Pandas DataFrames and CSVs on the local filesystem."""

    data_dir: str

    def _get_fs_path(self, asset_key: AssetKey) -> Path:
        return Path(self.data_dir).joinpath(*asset_key.path)

    def _get_table_name(self, asset_key: AssetKey) -> str:
        return "_".join(asset_key.path)

    def handle_output(self, context: OutputContext, obj: AssetType):
        table = self._get_table_name(context.asset_key)
        path = self._get_fs_path(context.asset_key)
        meta = {}
        if obj is None:
            pass
        elif isinstance(obj, GeoDataFrame):
            outfile = path.with_suffix(DB_SUFFIX)
            obj.to_file(outfile, driver=DB_DRIVER, encoding=ENCODING)
            meta["num_records"] = len(obj)
            geo_col = obj.active_geometry_name
            df = DataFrame(obj)
            df[geo_col] = df[geo_col].map(lambda x: f"*{type(x).__name__}*")
            meta["preview"] = MetadataValue.md(df.head().to_markdown())
        elif isinstance(obj, DataFrame):
            outfile = path.with_suffix(DB_SUFFIX)
            with connect(outfile) as con:
                obj.to_sql(table, con, if_exists="replace")
            meta["num_records"] = len(obj)
            meta["preview"] = MetadataValue.md(obj.head().to_markdown())
        elif isinstance(obj, Figure):
            outfile = path.with_suffix(FIG_SUFFIX)
            obj.savefig(outfile)
        elif isinstance(obj, str):
            outfile = path.with_suffix(TXT_SUFFIX)
            outfile.write_text(obj)
            meta["preview"] = obj[:255]
        else:
            raise NotImplementedError(f"Cannot handle {type}")
        context.add_output_metadata(meta)

        if "sources" in context.definition_metadata:
            self.write_license_file(outfile, context.definition_metadata["sources"])

    def write_license_file(self, basefile: Path, sources: List[Mapping[str, str]]):
        licensefile = basefile.with_suffix(basefile.suffix + LICENSE_SUFFIX)
        with licensefile.open("w") as fd:
            fd.write(LICENSE_FILE_HEADER.format(basefile.name))
            for source in sources:
                fd.write("\n")
                fd.write(f"## {source.get("name", "DataSource")}\n")
                for key, val in source.items():
                    if key == "name":
                        continue
                    fd.write(f"{key.upper()}: {val}\n")

    def load_input(self, context: InputContext) -> AssetType:
        table = self._get_table_name(context.asset_key)
        path = self._get_fs_path(context.asset_key)
        type = context.dagster_type.typing_type
        if type == GeoDataFrame:
            infile = path.with_suffix(DB_SUFFIX)
            return read_file(infile, encoding=ENCODING)
        elif type == DataFrame:
            infile = path.with_suffix(DB_SUFFIX)
            with connect(infile) as con:
                query = f"SELECT * FROM {table}"
                return read_sql(sql=query, con=con)
        elif type == str:
            infile = path.with_suffix(TXT_SUFFIX)
            return infile.read_text()
        else:
            raise NotImplementedError(f"Cannot load {type}")
