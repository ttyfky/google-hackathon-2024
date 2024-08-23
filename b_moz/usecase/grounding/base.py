import json

from langchain_core.runnables import Runnable

from b_moz.libs.chains.mock_chain import create_mock_chain


class RagBase:
    _chain: Runnable

    def __init__(self, chain: Runnable):
        self._chain = chain

    def invoke(self, input: str) -> str:
        return self._chain.invoke(input=input)


class MockRag(RagBase):
    def __init__(self, response: dict):
        super().__init__(chain=create_mock_chain(response))

    def invoke(self, input: str) -> str:
        res = self._chain.invoke(input=input)
        return json.loads(res.replace("'", '"'))
