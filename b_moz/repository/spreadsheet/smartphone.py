import os

import pandas as pd

from b_moz.libs.io.exporter import GoogleSpreadSheetExporter
from b_moz.repository.base import RepositoryBase


class ModelRepo(RepositoryBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._exporter = GoogleSpreadSheetExporter(
            file_id=os.environ.get("DRIVE_SS_ID", "")
        )

    def save(self, data: pd.DataFrame, **kwargs):
        self._exporter.export(data, sheet_name="model", **kwargs)
