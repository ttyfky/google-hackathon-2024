from __future__ import annotations

import datetime as dt
import logging
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
from langchain_core.runnables.base import RunnableEach, RunnableParallel
from langchain_core.runnables.retry import RunnableRetry

from .prompt import LATEST_MODELS_LIST_PROMPT as prompt
from ...llms.vertexai import get_langchain_model
from ...retreivers.google_search import GoogleSearchJsonResultRetriever

_logger = logging.getLogger(__name__)


def filter_latest_models(models: List) -> List:
    _logger.info(f"Filtering latest models: {models}")
    if not isinstance(models, List):
        _logger.warning(f"models is not type List: {models}")
        return []
    filtered = [
        m for m in models if re.match(r"^\d{4}-\d{2}-\d{2}$", m.get("release_date", ""))
    ]
    days_30_before = dt.datetime.today() - dt.timedelta(days=30)
    return [
        m
        for m in filtered
        if days_30_before < dt.datetime.strptime(m["release_date"], "%Y-%m-%d")
    ]


def create_model_release_date_extract_chain() -> Runnable:
    return (
        {"input": itemgetter("input"), "context": itemgetter("context")}
        | prompt
        | get_langchain_model().bind(response_mime_type="application/json")
        | SimpleJsonOutputParser()
        | RunnableLambda(filter_latest_models)
    )


def create_latest_models_collect_chain() -> Runnable:
    new_released_model_search = GoogleSearchJsonResultRetriever(
        query_tmpl="{query} 最新モデル 発売", as_html=True
    )

    date_extract_chain = create_model_release_date_extract_chain()
    retry = RunnableRetry(
        bound=date_extract_chain,
        max_attempt_number=3,
        wait_exponential_jitter=False,
    )
    chain = (
        RunnableParallel(
            {"input": RunnablePassthrough(), "docs": new_released_model_search}
        )
        | RunnableLambda(
            lambda x: [
                {
                    "input": itemgetter("input"),
                    "context": doc.page_content,
                }
                for doc in x["docs"]  # type: ignore
            ]
        )
        | RunnableEach(bound=retry)
        | (lambda r: reduce(lambda i, e: i + e, r, []))
    )

    return RunnableParallel({"query": RunnablePassthrough(), "models": chain})
