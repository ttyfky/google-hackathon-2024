from __future__ import annotations

from operator import itemgetter

from langchain_core.output_parsers import SimpleJsonOutputParser
from langchain_core.runnables import (
    Runnable,
    RunnablePassthrough,
    RunnableLambda,
    RunnableParallel,
)

from .prompt import (
    SMARTPHONE_SPEC_EXTRACT_PROMPT,
    PC_SPEC_EXTRACT_PROMPT,
    SMARTWATCH_SPEC_EXTRACT_PROMPT,
)
from ...llms.vertexai import get_langchain_model
from ...retreivers.google_search import GoogleSearchJsonResultRetriever


def create_spec_extract_chain(category: str = "smartphone") -> Runnable:
    if category == "smartphone":
        prompt = SMARTPHONE_SPEC_EXTRACT_PROMPT
    elif category == "pc":
        prompt = PC_SPEC_EXTRACT_PROMPT
    elif category == "smartwatch":
        prompt = SMARTWATCH_SPEC_EXTRACT_PROMPT
    else:
        prompt = SMARTPHONE_SPEC_EXTRACT_PROMPT

    return {
        "context": GoogleSearchJsonResultRetriever(query_tmpl="{query} 仕様"),
        "input": RunnablePassthrough(),
    } | RunnableParallel(
        result=prompt
        | get_langchain_model().bind(response_mime_type="application/json")
        | SimpleJsonOutputParser()
        | RunnableLambda(lambda r: [r] if type(r) is dict else r),
        links=itemgetter("context"),
    )
