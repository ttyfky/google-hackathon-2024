import os

from b_moz.libs.project import is_local
from b_moz.repository.spreadsheet.query import ExtractExceptionRepo, ModelSourceRepo
from b_moz.repository.spreadsheet.smartphone import (
    ModelRepo,
    ModelStorageRepo,
    ModelColorRepo,
    ModelSupplementRepo,
)


class Saver:
    def __init__(self, exporter):
        self._repos = {
            "model": ModelRepo(exporter=exporter),
            "model_source": ModelSourceRepo(exporter=exporter),
            "model_storage": ModelStorageRepo(exporter=exporter),
            "model_color": ModelColorRepo(exporter=exporter),
            "supplements": ModelSupplementRepo(exporter=exporter),
            "exception": ExtractExceptionRepo(exporter=exporter),
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
if is_local() and not os.getenv("DRIVE_SS_ID"):
    from b_moz.libs.io.exporter import LocalCSVExporter

    _SAVER = Saver(exporter=LocalCSVExporter())
else:
    from b_moz.libs.io.exporter import GoogleSpreadSheetExporter

    _SAVER = Saver(GoogleSpreadSheetExporter(file_id=os.environ.get("DRIVE_SS_ID", "")))


def get_saver():
    return _SAVER
