import logging
import os

from typing import Dict

from b_moz.usecase.grounding.base import MockRag
from b_moz.usecase.grounding.catalog import LatestModelsCollector

_logger = logging.getLogger(__name__)


class CollectLatestModels:
    def __init__(self, rag):
        self.rag = rag

    def collect(self, category_query: str):
        try:
            latests: Dict = self.rag.invoke(input=category_query)
            _logger.info(f"Collected latest models: {latests}")
            return latests
        except Exception as e:
            _logger.error(
                f"Failed to collect latest models for [{category_query}] with error: {e}"
            )
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
