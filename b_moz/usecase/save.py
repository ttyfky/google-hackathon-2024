from b_moz.repository.spreadsheet.query import ExtractExceptionRepo, ModelSourceRepo
from b_moz.repository.spreadsheet.smartphone import (
    ModelRepo,
    ModelStorageRepo,
    ModelColorRepo,
    ModelSupplementRepo,
)


class SaveSS:
    def __init__(
        self,
    ):
        self._repos = {
            "model": ModelRepo(),
            "model_source": ModelSourceRepo(),
            "model_storage": ModelStorageRepo(),
            "model_color": ModelColorRepo(),
            "supplements": ModelSupplementRepo(),
            "exception": ExtractExceptionRepo(),
        }

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def save_spec(
        self, extracted: dict, links: list, query: str, category: str = "", **kwargs
    ):
        self._repos["model"].save(extracted, query=query, category=category, **kwargs)
        self._repos["model_source"].save(extracted, links=links, **kwargs)
        self._repos["model_storage"].save(extracted, **kwargs)
        self._repos["model_color"].save(extracted, **kwargs)
        self._repos["supplements"].save(extracted, **kwargs)

    def save_exception(self, query: str, message: str):
        self._repos["exception"].save({"query": query, "message": message})

    def flush(self):
        for repo in self._repos.values():
            repo.flush()


# To prevent race condition, we need to use a single instance of SaveSS.
_SAVE_SS = SaveSS()


def get_saver():
    return _SAVE_SS
