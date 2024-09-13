import re
from typing import Optional

import pandas as pd

from ..base import DataFrameHolder

CATEGORY_KEY = "category"
QUERY_KEY = "query"
MODEL_KEY = "model"
COLOR_KEY = "color"
STORAGE_KEY = "storage"
MANUFACTURER_KEY = "manufacturer"
SERIES_KEY = "series"
DUMP_KEY = "dump"


class Base(DataFrameHolder):
    pass


class Model(Base):
    columns = [MODEL_KEY, MANUFACTURER_KEY, SERIES_KEY, QUERY_KEY, CATEGORY_KEY]  # type: ignore

    def __init__(self, data: Optional[pd.DataFrame] = None):
        super().__init__(data)

    def append_map(self, data: dict, query: str, category: str):
        model = data.get("model")
        if not model:
            raise ValueError("model is required")
        self.append(
            [
                model,
                data.get("manufacturer", ""),
                data.get("series", ""),
                query,
                category,
            ]
        )


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
                self.append([model, ModelStorage.format(storage)])

    @staticmethod
    def format(storage: str):
        # Some Android has `8 GB + 256 GB`, `8 RAM + 256 GB memory` in storage column.
        strageli = storage.split("+")
        if len(strageli) > 1:
            storage = strageli[1].strip()
        else:
            storage = storage

        storage = re.findall(r"\d+(?:GB|TB)", storage.replace(" ", ""))[0]
        return storage


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
