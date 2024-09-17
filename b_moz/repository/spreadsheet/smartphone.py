from b_moz.domain.spec.smartphone import (
    Model,
    ModelStorage,
    ModelColor,
    ModelSupplement,
)
from b_moz.repository.base import RepoBase


class ModelRepo(RepoBase):
    table_name = "model"

    def save(self, data: dict, **kwargs):
        with Model() as obj:
            obj.append_map(data, kwargs["query"], kwargs["category"])
            self.save_df(obj.get_dataframe(), **kwargs)


class ModelStorageRepo(RepoBase):
    table_name = "model_storage"

    def save(self, data: dict, **kwargs):
        with ModelStorage() as obj:
            obj.append_map(data)
            self.save_df(obj.get_dataframe(), **kwargs)


class ModelColorRepo(RepoBase):
    table_name = "model_color"

    def save(self, data: dict, **kwargs):
        with ModelColor() as obj:
            obj.append_map(data)
            self.save_df(obj.get_dataframe(), **kwargs)


class ModelSupplementRepo(RepoBase):
    table_name = "supplements"

    def save(self, data: dict, **kwargs):
        with ModelSupplement() as obj:
            obj.append_map(data)
            self.save_df(obj.get_dataframe(), **kwargs)
