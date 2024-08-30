from typing import Dict

from b_moz.libs.chains.latest_models_list.chain import (
    create_latest_models_collect_chain,
)
from b_moz.libs.chains.spec_extract.chain import create_spec_extract_chain
from b_moz.usecase.grounding.base import RagBase


class SpecCollector(RagBase):
    def __init__(self):
        super().__init__(chain=create_spec_extract_chain())

    def invoke(self, input: str, category: str = "") -> str:
        if category:
            return create_spec_extract_chain(category=category).invoke(input=input)
        return self._chain.invoke(input=input)


class LatestModelsCollector(RagBase):
    def __init__(self) -> None:
        super().__init__(chain=create_latest_models_collect_chain())

    def invoke(self, input: str) -> Dict:
        return self._chain.invoke(input=input)
