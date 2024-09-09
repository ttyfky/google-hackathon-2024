import logging
import os
from typing import List

from b_moz.repository.spreadsheet.smartphone import (
    ModelRepo,
    ModelStorageRepo,
    ModelColorRepo,
    ModelSupplementRepo,
    ExtractExceptionRepo,
)
from b_moz.usecase.grounding.base import MockRag
from b_moz.usecase.grounding.catalog import SpecCollector

_logger = logging.getLogger(__name__)


class CollectSpec:
    def __init__(self, rag, spec_repo):
        self.spec_repo = spec_repo
        self.rag = rag

    def collect(self, target_query: str, category: str = "") -> List:
        try:
            extracted = self.rag.invoke(input=target_query, category=category)
            _logger.info(f"Extracted spec: {extracted}")

            if type(extracted[0]) is dict and extracted[0]["status"] == "failed":
                self._save_exception(target_query, extracted[0]["error"])
                return extracted

            for record in extracted:
                self._save(record, category)
            return extracted

        except ValueError as e:
            _logger.error(f"Failed to save spec for [{target_query}] with error: {e}")
            raise e

        except Exception as e:
            _logger.error(
                f"Failed to extract spec for [{target_query}] with error: {e}"
            )
            self._save_exception(target_query, str(e))
            raise e

    def _save(self, extracted: dict, category: str = ""):

        with ModelRepo() as repo:
            repo.save(extracted)

        with ModelStorageRepo() as repo:
            repo.save(extracted)

        with ModelColorRepo() as repo:
            repo.save(extracted)

        if category != "smartphone":
            with ModelSupplementRepo() as repo:
                repo.save(extracted)

    def _save_exception(self, query: str, message: str):
        with ExtractExceptionRepo() as repo:
            repo.save({"query": query, "message": message})


def create_target_spec_usecase(spec_repo):
    if os.environ.get("IS_MOCK", "false") == "true":
        return CollectSpec(
            MockRag(
                {
                    "query": "pixel 9",
                    "model": "Pixel 9",
                    "manufacturer": "Google",
                    "series": "Pixel",
                    "storages": ["128GB", "256GB"],
                    "colors": ["Obsidian", "Porcelain", "Peony", "Wintergreen"],
                }
            ),
            None,
        )

    return CollectSpec(SpecCollector(), spec_repo)
