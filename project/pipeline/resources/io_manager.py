from pathlib import Path
from dagster import AssetKey, ConfigurableIOManager, MetadataValue
from numpy import format_float_positional
from pandas import DataFrame, read_csv

FLOAT_FORMAT = lambda x: format_float_positional(x, precision=10, trim="-")


class LocalFileSystemIOManager(ConfigurableIOManager):
    """Translates between Pandas DataFrames and CSVs on the local filesystem."""

    data_dir: str

    def _get_fs_path(self, asset_key: AssetKey) -> str:
        return Path(self.data_dir).joinpath(*asset_key.path).with_suffix(".csv")

    def handle_output(self, context, obj: DataFrame):
        """This saves the dataframe as a CSV."""
        fpath = self._get_fs_path(context.asset_key)
        obj.to_csv(fpath, float_format=FLOAT_FORMAT)
        context.add_output_metadata(
            {
                "num_records": len(obj),
                "preview": MetadataValue.md(obj.head().to_markdown()),
            }
        )

    def load_input(self, context):
        """This reads a dataframe from a CSV."""
        fpath = self._get_fs_path(context.asset_key)
        return read_csv(fpath)
