import os
from abc import abstractmethod

import pandas as pd

from b_moz.domain.spec.smartphone import (
    Model,
    ModelStorage,
    ModelColor,
    ModelSupplement,
    ExtractException,
)
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


class ModelRepo(SSRepoBase):
    sheet_name = "model"

    def save(self, data: dict, **kwargs):
        with Model() as obj:
            obj.append_map(data)
            self.save_df(obj.get_dataframe(), **kwargs)


class ModelStorageRepo(SSRepoBase):
    sheet_name = "model_storage"

    def save(self, data: dict, **kwargs):
        with ModelStorage() as obj:
            obj.append_map(data)
            self.save_df(obj.get_dataframe(), **kwargs)


class ModelColorRepo(SSRepoBase):
    sheet_name = "model_color"

    def save(self, data: dict, **kwargs):
        with ModelColor() as obj:
            obj.append_map(data)
            self.save_df(obj.get_dataframe(), **kwargs)


class ModelSupplementRepo(SSRepoBase):
    sheet_name = "supplements"

    def save(self, data: dict, **kwargs):
        with ModelSupplement() as obj:
            obj.append_map(data)
            self.save_df(obj.get_dataframe(), **kwargs)


# TODO change dir
class ExtractExceptionRepo(SSRepoBase):
    sheet_name = "exception"

    def save(self, data: dict, **kwargs):
        with ExtractException() as obj:
            obj.append_map(data)
            self.save_df(obj.get_dataframe(), **kwargs)
