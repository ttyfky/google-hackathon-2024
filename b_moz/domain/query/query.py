from typing import Optional

import pandas as pd

from ..base import DataFrameHolder

QUERY_KEY = "query"
DATA_KEY = "data"
EXCEPTION_MESSAGE_KEY = "message"
CREATED_AT_KEY = "created_at"


class Base(DataFrameHolder):
    pass


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
