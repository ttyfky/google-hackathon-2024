import logging
import os
from typing import Dict

from b_moz.libs.o11y.trace import tracing
from b_moz.libs.project import pubsub_active
from b_moz.repository.pubsub.pubsub import PubSub
from b_moz.repository.spreadsheet.query import ExtractExceptionRepo
from b_moz.usecase.grounding.base import MockRag
from b_moz.usecase.grounding.catalog import LatestModelsCollector

_logger = logging.getLogger(__name__)


class CollectLatestModels:
    def __init__(self, rag):
        self.rag = rag

    @tracing
    def collect(self, category_query: str):
        try:
            latests: Dict = self.rag.invoke(input=category_query)
            _logger.info(f"Collected latest models: {latests}")
            if pubsub_active():
                with PubSub() as pb:
                    for model in latests["models"]:
                        model["category"] = category_query
                        pb.save(model)
            else:
                _logger.info("Publishing to model info was skipped.")
            return latests
        except Exception as e:
            _logger.error(
                f"Failed to collect latest models for [{category_query}] with error: {e}"
            )
            with ExtractExceptionRepo() as repo:
                repo.save({"query": category_query, "message": str(e)})
            raise e


def create_latest_items_usecase() -> CollectLatestModels:
    if os.environ.get("IS_MOCK", "false") == "true":
        return CollectLatestModels(
            MockRag(
                {
                    "query": "smartphone",
                    "models": [
                        {
                            "model": "iPhone 13",
                            "release_date": "2021-09-23",
                            "manufacturer": "apple",
                        }
                    ],
                }
            )
        )

    return CollectLatestModels(LatestModelsCollector())
