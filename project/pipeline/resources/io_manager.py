from pathlib import Path
from dagster import AssetKey, ConfigurableIOManager
from pandas import DataFrame, read_csv


class LocalFileSystemIOManager(ConfigurableIOManager):
    """Translates between Pandas DataFrames and CSVs on the local filesystem."""

    data_dir: str

    def _get_fs_path(self, asset_key: AssetKey) -> str:
        return Path(self.data_dir).joinpath(*asset_key.path).with_suffix(".csv")

    def handle_output(self, context, obj: DataFrame):
        """This saves the dataframe as a CSV."""
        fpath = self._get_fs_path(context.asset_key)
        obj.to_csv(fpath)

    def load_input(self, context):
        """This reads a dataframe from a CSV."""
        fpath = self._get_fs_path(context.asset_key)
        return read_csv(fpath)
