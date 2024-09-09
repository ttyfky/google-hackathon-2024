from typing import Optional

import pandas as pd
from pandas._typing import Axes

MODEL_KEY = "model"
COLOR_KEY = "color"
STORAGE_KEY = "storage"
MANUFACTURER_KEY = "manufacturer"
SERIES_KEY = "series"
DUMP_KEY = "dump"
QUERY_KEY = "query"
DATA_KEY = "data"
EXCEPTION_MESSAGE_KEY = "message"
CREATED_AT_KEY = "created_at"


class Base:
    _df: pd.DataFrame
    columns: Axes

    def __init__(self, data: Optional[pd.DataFrame] = None):
        if data is not None:
            self._df = data
        else:
            self._df = pd.DataFrame(columns=self.columns)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def append_df(self, data: pd.DataFrame):
        self._df = pd.concat([self._df, data], ignore_index=True)

    def get_dataframe(self):
        return self._df

    def append(self, data):
        self._df = pd.concat(
            [
                self._df,
                pd.DataFrame(data=[data], columns=self.columns),
            ],
            ignore_index=True,
        )


class Model(Base):
    columns = [MODEL_KEY, SERIES_KEY, MANUFACTURER_KEY]  # type: ignore

    def __init__(self, data: Optional[pd.DataFrame] = None):
        super().__init__(data)

    def append_map(self, data: dict):
        model = data.get("model")
        if not model:
            raise ValueError("model is required")
        self.append([model, data.get("manufacturer", ""), data.get("series", "")])


class ModelStorage(Base):
    columns = [MODEL_KEY, STORAGE_KEY]  # type: ignore

    def __init__(self, data: Optional[pd.DataFrame] = None):
        super().__init__(data)

    def append_map(self, data: dict):
        model = data.get("model")
        if not model:
            raise ValueError("model is required")
        storages = data.get("storages", [])
        if storages:
            for storage in storages:
                self.append([model, storage])


class ModelColor(Base):
    columns = [MODEL_KEY, COLOR_KEY]  # type: ignore

    def __init__(self, data: Optional[pd.DataFrame] = None):
        super().__init__(data)

    def append_map(self, data: dict):
        model = data.get("model")
        if not model:
            raise ValueError("model is required")
        colors = data.get("colors", [])
        if colors:
            for color in colors:
                self.append([model, color])


class ModelSupplement(Base):
    columns = [MODEL_KEY, DUMP_KEY]  # type: ignore

    def __init__(self, data: Optional[pd.DataFrame] = None):
        super().__init__(data)

    def append_map(self, data: dict):
        model = data.get("model")
        if not model:
            raise ValueError("model is required")
        self.append([model, str(data)])


# TODO change dir
class ExtractException(Base):
    columns = [QUERY_KEY, DATA_KEY, EXCEPTION_MESSAGE_KEY, CREATED_AT_KEY]  # type: ignore

    def __init__(self, data: Optional[pd.DataFrame] = None):
        super().__init__(data)

    def append_map(self, data: dict):
        query = data.get("query")
        if not query:
            raise ValueError("query is required")
        self.append(
            [query, data.get("data", ""), data.get("message", ""), pd.Timestamp.now()]
        )
