from __future__ import annotations
from operator import itemgetter

from langchain_core.runnables import (
    Runnable,
    RunnablePassthrough,
    RunnableParallel,
    RunnableLambda,
)

from b_moz.libs.io.parser import JsonOutputParserWithErrorCatch
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

    chain = prompt | get_langchain_model() | JsonOutputParserWithErrorCatch()

    def coalesce_result(result):
        result_json = result["result"]
        query = result["input"]
        if type(result_json) is dict and "error" in result_json:
            return {"query": query, "error": result_json["error"], "result": "failed"}
        return result_json | {"result": "success"}

    return (
        {
            "context": GoogleSearchJsonResultRetriever(query_tmpl="{query} 仕様"),
            "input": RunnablePassthrough(),
        }
        | RunnableParallel(
            result=chain,
            input=itemgetter("input"),
        )
        | RunnableLambda(coalesce_result)
        | RunnableLambda(lambda r: [r] if type(r) is dict else r)
    )
