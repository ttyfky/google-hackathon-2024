from b_moz.domain.query.query import ExtractException
from b_moz.repository.base import RepoBase
from ...domain.spec.source import ModelSource


class ExtractExceptionRepo(RepoBase):
    table_name = "exception"

    def save(self, data: dict, **kwargs):
        with ExtractException() as obj:
            obj.append_map(data)
            self.save_df(obj.get_dataframe(), **kwargs)


class ModelSourceRepo(RepoBase):
    table_name = "model_source"

    def save(self, data: dict, **kwargs):
        with ModelSource() as obj:
            obj.append_map(data, kwargs["links"])
            self.save_df(obj.get_dataframe(), **kwargs)
