from __future__ import annotations

import datetime as dt
import re

from functools import reduce
from operator import itemgetter
from typing import List

from langchain_core.output_parsers import SimpleJsonOutputParser
from langchain_core.runnables import (
    Runnable,
    RunnablePassthrough,
    RunnableLambda,
)
from langchain_core.runnables.base import RunnableEach

from .prompt import LATEST_MODELS_LIST_PROMPT as prompt
from ...llms.vertexai import get_langchain_model
from ...retreivers.google_search import GoogleSearchJsonResultRetriever


def filter_latest_models(models: List) -> List:
    filtered = [
        m for m in models if re.match(r"^\d{4}-\d{2}-\d{2}$", m["release_date"])
    ]
    today = dt.datetime.today()
    days_30 = dt.timedelta(days=30)
    return [
        m
        for m in filtered
        if today - days_30 < dt.datetime.strptime(m["release_date"], "%Y-%m-%d")
    ]


def create_model_release_date_extract_chain() -> Runnable:
    return (
        {"input": itemgetter("input"), "context": itemgetter("context")}
        | prompt
        | get_langchain_model()
        | SimpleJsonOutputParser()
        | RunnableLambda(filter_latest_models)
    )


def create_latest_models_collect_chain() -> Runnable:
    new_released_model_search = GoogleSearchJsonResultRetriever(
        query_tmpl="{query} 最新モデル 発売", as_html=True
    )

    return (
        {"input": RunnablePassthrough(), "docs": new_released_model_search}
        | RunnableLambda(
            lambda x: [
                {
                    "input": x["input"],
                    "context": doc.page_content,
                    "source": doc.metadata["source"],
                }
                for doc in x["docs"]
            ]
        )
        | RunnableEach(bound=create_model_release_date_extract_chain())
        | (lambda r: reduce(lambda i, e: i + e, r, []))
    )
