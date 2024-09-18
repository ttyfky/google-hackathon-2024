import json
import logging
import os
from typing import List

from b_moz.libs.o11y.trace import tracing
from b_moz.libs.project import pubsub_active
from b_moz.repository.pubsub.pubsub import PubSub
from b_moz.usecase.grounding.base import MockRag
from b_moz.usecase.grounding.catalog import SpecCollector
from b_moz.usecase.save import get_saver

_logger = logging.getLogger(__name__)


class CollectSpec:
    def __init__(self, rag, spec_repo):
        self.spec_repo = spec_repo
        self.rag = rag

    def _get_spec_topic(self):
        return os.environ.get("SPEC_TOPIC", "moz-spec-topic")

    @tracing
    def collect(self, target_query: str, category: str = "", **kwargs) -> List:
        try:
            extracted, links = self.rag.invoke(input=target_query, category=category)
            _logger.info(f"Extracted spec: {extracted}")

            if kwargs.get("mode", "") == "SS_SAVE":
                _logger.info(f"Saving spec for [{target_query}] to S/S")
                for record in extracted:
                    get_saver().save_spec(record, links, target_query, category)
            else:
                if pubsub_active():
                    _logger.info(f"Publishing spec for [{target_query}] to PubSub")
                    with PubSub() as pb:
                        for record in extracted:
                            record["category"] = category
                            record["links"] = links
                            record["query"] = target_query
                            pb.save(record, topic=self._get_spec_topic())
                else:
                    _logger.info(
                        "Saving spec was skipped on local run. If you want to save it, use mode=SS_SAVE."
                    )

            return extracted

        except ValueError as e:
            _logger.error(f"Failed to save spec for [{target_query}] with error: {e}")
            raise e

        except Exception as e:
            _logger.error(
                f"Failed to extract spec for [{target_query}] with error: {e}"
            )
            get_saver().save_exception(target_query, str(e))
            raise e


def create_target_spec_usecase(spec_repo) -> CollectSpec:
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
    _NUM_PULL_PROCESS = 5

    def __init__(self, worker: CollectSpec):
        self.worker = worker
        self._result = []

    def _call_back(self, payload: bytes):
        val = json.loads(payload)
        try:

            _target = val["model"]
            _category = val["category"]
            _logger.info(f"Collecting spec for {_target}, category: {_category}")
            res = self.worker.collect(target_query=_target, category=_category)
            self._result.extend(res)
        except Exception as e:
            _logger.error(f"Failed to collect spec for {val} with error: {e}")
            return False
        return True

    @tracing
    def collect(self, **kwargs) -> List:
        with PubSub(num_pull=10) as ps:
            for _ in range(self._NUM_PULL_PROCESS):  # 5 times, 3 messages per pull
                ps.pull_with(self._call_back)
        return self._result


def create_pubsub_target_spec_usecase(spec_repo) -> CollectSpecPubSub:
    return CollectSpecPubSub(create_target_spec_usecase(spec_repo))


class SavePubSubCollectedSpecToSS:
    _NUM_PULL_PROCESS = 20

    def __init__(self):
        pass

    def _get_spec_subscription(self):
        return os.environ.get("SPEC_SUBSCRIPTION", "moz-spec-topic-sub")

    def _call_back(self, payload: bytes):
        val = json.loads(payload)
        try:

            category = val.pop("category")
            links = val.pop("links")
            query = val.pop("query")
            get_saver().save_spec(
                extracted=val,
                links=links,
                query=query,
                category=category,
                buffered=True,
            )
        except Exception as e:
            _logger.error(f"Failed to save spec for {val} with error: {e}")
            return False

        return True

    @tracing
    def save(self, **kwargs):
        with PubSub(num_pull=50) as ps:  # 50 messages per pull.
            for _ in range(self._NUM_PULL_PROCESS):
                if not ps.pull_with(
                    callback=self._call_back,
                    postprocess=lambda: get_saver().flush(),
                    subscription_id=self._get_spec_subscription(),
                ):
                    break


def create_save_pubsub_target_spec_usecase() -> SavePubSubCollectedSpecToSS:
    return SavePubSubCollectedSpecToSS()
