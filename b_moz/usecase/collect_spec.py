import logging
import os
from typing import List
import json

from b_moz.repository.pubsub.pubsub import PubSub
from b_moz.repository.spreadsheet.query import ExtractExceptionRepo, ModelSourceRepo
from b_moz.repository.spreadsheet.smartphone import (
    ModelRepo,
    ModelStorageRepo,
    ModelColorRepo,
    ModelSupplementRepo,
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
            extracted, links = self.rag.invoke(input=target_query, category=category)
            _logger.info(f"Extracted spec: {extracted}")

            for record in extracted:
                self._save(record, links, target_query, category)
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

    def _save(self, extracted: dict, links: list, query: str, category: str = ""):

        with ModelRepo() as repo:
            repo.save(extracted, query=query, category=category)

        with ModelSourceRepo() as repo:
            repo.save(extracted, links=links)

        with ModelStorageRepo() as repo:
            repo.save(extracted)

        with ModelColorRepo() as repo:
            repo.save(extracted)

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


class CollectSpecPubSub:
    _NUM_PULL_PROCESS = 1

    def __init__(self, worker: CollectSpec):
        self.worker = worker
        self._result = []

    def _call_back(self, payload: bytes):
        val = json.loads(payload)
        try:

            _target = val["model"]
            _category = val["category"]
            logging.info(f"Collecting spec for {_target}, category: {_category}")
            res = self.worker.collect(target_query=_target, category=_category)
            self._result.extend(res)
        except Exception as e:
            _logger.error(f"Failed to collect spec for {val} with error: {e}")
            return False
        return True

    def collect(self, **kwargs) -> List:
        with PubSub() as ps:
            for _ in range(self._NUM_PULL_PROCESS):  # 5 times, 3 messages per pull
                ps.pull_with(self._call_back)
        return self._result


def create_pubsub_target_spec_usecase(spec_repo):
    return CollectSpecPubSub(create_target_spec_usecase(spec_repo))
