import logging
import os

import pandas as pd

from b_moz.domain.spec.smartphone import Model
from b_moz.repository.spreadsheet.smartphone import ModelRepo
from b_moz.usecase.grounding.base import MockRag
from b_moz.usecase.grounding.catalog import SpecCollector

_logger = logging.getLogger(__name__)


class CollectSpec:
    def __init__(self, rag, spec_repo):
        self.spec_repo = spec_repo
        self.rag = rag

    def collect(self, target_query: str) -> str:
        try:
            extracted = self.rag.invoke(input=target_query)
            _logger.info(f"Extracted spec: {extracted}")

            self._save(extracted)
            return extracted
        except Exception as e:
            _logger.error(
                f"Failed to extract spec for [{target_query}] with error: {e}"
            )
            raise e

    def _save(self, extracted: dict):
        model = extracted["model"]

        with ModelRepo() as repo:
            model_df = pd.DataFrame(
                data=[[model, extracted["manufacturer"], extracted["series"]]],
                columns=Model.columns,
            )
            repo.save(model_df)


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
