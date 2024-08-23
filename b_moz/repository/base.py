from abc import abstractmethod

import pandas as pd


class RepositoryBase:
    def __init__(self, **kwargs):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    @abstractmethod
    def save(self, data: pd.DataFrame, **kwargs):
        pass
