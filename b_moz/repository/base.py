from abc import abstractmethod

import pandas as pd

from b_moz.libs.io.exporter import LocalCSVExporter
from b_moz.libs.o11y.trace import tracing


class RepoBase:
    table_name: str

    def __init__(self, exporter=LocalCSVExporter(), **kwargs):
        self._exporter = exporter
        self._buffer = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def buffered_save_df(self, data: pd.DataFrame, **kwargs):
        self._buffer.append(data)

    @tracing
    def flush(self, **kwargs):
        if not self._buffer:
            return
        self.save_df(pd.concat(self._buffer), **kwargs)
        self._buffer = []

    @tracing
    def save_df(self, data: pd.DataFrame, **kwargs):
        if kwargs.get("buffered", False):
            self.buffered_save_df(data, **kwargs)
            return
        self._exporter.export(data, table_name=self.table_name, **kwargs)

    @abstractmethod
    @tracing
    def save(self, data: dict, **kwargs):
        raise NotImplementedError
