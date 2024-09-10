from typing import Optional

import pandas as pd
from pandas._typing import Axes


class DataFrameHolder:
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
