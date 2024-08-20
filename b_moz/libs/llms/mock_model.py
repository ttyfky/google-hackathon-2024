from typing import List, Optional

from langchain_core.language_models import LLM, FakeListLLM


def get_langchain_model(responses: Optional[List[str]]) -> LLM:
    if not responses:
        responses = ["This is a test response."]
    return FakeListLLM(responses=responses)
