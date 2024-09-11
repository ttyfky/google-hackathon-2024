from b_moz.domain.query.query import ExtractException
from .base import SSRepoBase
from ...domain.spec.source import ModelSource


class ExtractExceptionRepo(SSRepoBase):
    sheet_name = "exception"

    def save(self, data: dict, **kwargs):
        with ExtractException() as obj:
            obj.append_map(data)
            self.save_df(obj.get_dataframe(), **kwargs)


class ModelSourceRepo(SSRepoBase):
    sheet_name = "model_source"

    def save(self, data: dict, **kwargs):
        with ModelSource() as obj:
            obj.append_map(data, kwargs["links"])
            self.save_df(obj.get_dataframe(), **kwargs)
