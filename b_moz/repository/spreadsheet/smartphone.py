from b_moz.domain.spec.smartphone import (
    Model,
    ModelStorage,
    ModelColor,
    ModelSupplement,
)
from .base import SSRepoBase


class ModelRepo(SSRepoBase):
    sheet_name = "model"

    def save(self, data: dict, **kwargs):
        with Model() as obj:
            obj.append_map(data, kwargs["query"], kwargs["category"])
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
