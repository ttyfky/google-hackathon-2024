from __future__ import annotations

from langchain_core.output_parsers import SimpleJsonOutputParser
from langchain_core.runnables import Runnable, RunnablePassthrough

from .prompt import SMARTPHONE_SPEC_EXTRACT_PROMPT, PC_SPEC_EXTRACT_PROMPT
from ...llms.vertexai import get_langchain_model
from ...retreivers.google_search import GoogleSearchJsonResultRetriever


def create_spec_extract_chain(category: str = "smartphone") -> Runnable:
    if category == "smartphone":
        prompt = SMARTPHONE_SPEC_EXTRACT_PROMPT
    elif category == "pc":
        prompt = PC_SPEC_EXTRACT_PROMPT
    else:
        prompt = SMARTPHONE_SPEC_EXTRACT_PROMPT

    return (
        {
            "context": GoogleSearchJsonResultRetriever(query_tmpl="{query} 仕様"),
            "input": RunnablePassthrough(),
        }
        | prompt
        | get_langchain_model()
        | SimpleJsonOutputParser()
    )
