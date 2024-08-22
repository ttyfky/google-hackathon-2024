from __future__ import annotations

from langchain_core.output_parsers import SimpleJsonOutputParser
from langchain_core.runnables import Runnable, RunnablePassthrough

from .prompt import SPEC_EXTRACT_PROMPT as prompt
from ...llms.vertexai import get_langchain_model
from ...retreivers.google_search import GoogleSearchJsonResultRetriever


def create_spec_extract_chain() -> Runnable:
    return (
        {
            "context": GoogleSearchJsonResultRetriever(query_tmpl="{query} 仕様"),
            "input": RunnablePassthrough(),
        }
        | prompt
        | get_langchain_model()
        | SimpleJsonOutputParser()
    )
