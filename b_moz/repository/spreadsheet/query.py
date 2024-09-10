from .base import SSRepoBase
from b_moz.domain.query.query import ExtractException


class ExtractExceptionRepo(SSRepoBase):
    sheet_name = "exception"

    def save(self, data: dict, **kwargs):
        with ExtractException() as obj:
            obj.append_map(data)
            self.save_df(obj.get_dataframe(), **kwargs)
