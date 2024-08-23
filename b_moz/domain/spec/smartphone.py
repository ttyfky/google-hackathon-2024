from typing import Optional

import pandas as pd
from pandas._typing import Axes

MODEL_KEY = "model"
COLOR_KEY = "color"
STORAGE_KEY = "storage"
MANUFACTURER_KEY = "manufacturer"
SERIES_KEY = "series"


class Base:
    _data: pd.DataFrame
    columns: Axes

    def __init__(self, data: Optional[pd.DataFrame] = None):
        if data is not None:
            self._data = data
        else:
            self.data = pd.DataFrame(columns=self.columns)

    def append_df(self, data: pd.DataFrame):
        self._data = pd.concat([self._data, data], ignore_index=True)


class Model(Base):
    columns = [MODEL_KEY, SERIES_KEY, MANUFACTURER_KEY]  # type: ignore

    def __init__(self, data: Optional[pd.DataFrame] = None):
        super().__init__(data)

    def append(self, model: str, series: str, manufacturer: str):
        self._data = pd.concat(
            [
                self._data,
                pd.DataFrame(data=[model, series, manufacturer], columns=self.columns),
            ],
            ignore_index=True,
        )
