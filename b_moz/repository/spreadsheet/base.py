import os
from abc import abstractmethod

import pandas as pd

from b_moz.libs.io.exporter import GoogleSpreadSheetExporter
from b_moz.repository.base import RepositoryBase


class SSRepoBase(RepositoryBase):
    sheet_name: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._exporter = GoogleSpreadSheetExporter(
            file_id=os.environ.get("DRIVE_SS_ID", "")
        )

    def save_df(self, data: pd.DataFrame, **kwargs):
        self._exporter.export(data, sheet_name=self.sheet_name, **kwargs)

    @abstractmethod
    def save(self, data: dict, **kwargs):
        raise NotImplementedError
