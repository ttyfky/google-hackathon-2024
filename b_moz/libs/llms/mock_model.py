from typing import List

from langchain_core.language_models import LLM, FakeListLLM


def get_langchain_model(responses: List[str] = None) -> LLM:
    if responses is None:
        responses = ["This is a test response."]
    return FakeListLLM(responses=responses)
