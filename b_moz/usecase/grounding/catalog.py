from b_moz.libs.chains.spec_extract.chain import create_spec_extract_chain
from b_moz.usecase.grounding.base import RagBase


class SpecCollector(RagBase):
    def __init__(self):
        super().__init__(chain=create_spec_extract_chain())

    def invoke(self, input: str) -> str:
        return self._chain.invoke(input=input)
