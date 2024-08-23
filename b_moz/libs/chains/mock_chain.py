from langchain_core.runnables import Runnable

from ..llms.mock_model import get_langchain_model


def create_mock_chain(data: dict) -> Runnable:
    return get_langchain_model(responses=[str(data)])
