from pathlib import Path
from sqlite3 import connect
from dagster import AssetKey, ConfigurableIOManager, MetadataValue
from matplotlib.axes import Axes
from pandas import DataFrame, read_sql
from geopandas import GeoDataFrame, read_file

ENCODING = "utf-8"
DB_SUFFIX = ".sqlite"
DB_DRIVER = "SQLite"
FIG_SUFFIX = ".svg"


class LocalFileSystemIOManager(ConfigurableIOManager):
    """Translates between Pandas DataFrames and CSVs on the local filesystem."""

    data_dir: str

    def _get_fs_path(self, asset_key: AssetKey) -> Path:
        return Path(self.data_dir).joinpath(*asset_key.path)

    def _get_table_name(self, asset_key: AssetKey) -> str:
        return "_".join(asset_key.path)

    def handle_output(self, context, obj: None | DataFrame | GeoDataFrame | Axes):
        table = self._get_table_name(context.asset_key)
        path = self._get_fs_path(context.asset_key)
        meta = {}
        if obj is None:
            pass
        elif isinstance(obj, GeoDataFrame):
            outfile = path.with_suffix(DB_SUFFIX)
            obj.to_file(outfile, driver=DB_DRIVER, encoding=ENCODING)
            meta["num_records"] = len(obj)
        elif isinstance(obj, DataFrame):
            outfile = path.with_suffix(DB_SUFFIX)
            with connect(outfile) as con:
                obj.to_sql(table, con, if_exists="replace")
            meta["num_records"] = len(obj)
            meta["preview"] = MetadataValue.md(obj.head().to_markdown())
        elif isinstance(obj, Axes):
            outfile = path.with_suffix(FIG_SUFFIX)
            obj.get_figure().savefig(outfile)
        else:
            raise NotImplementedError(f"Cannot handle {type}")
        context.add_output_metadata(meta)

    def load_input(self, context):
        table = self._get_table_name(context.asset_key)
        path = self._get_fs_path(context.asset_key)
        type = context.dagster_type.typing_type
        db_file = path.with_suffix(DB_SUFFIX)
        query = f"SELECT * FROM {table}"
        if type == GeoDataFrame:
            return GeoDataFrame(read_file(db_file, sql=query, encoding=ENCODING))
        elif type == DataFrame:
            with connect(db_file) as con:
                return read_sql(sql=query, con=con)
        else:
            raise NotImplementedError(f"Cannot load {type}")