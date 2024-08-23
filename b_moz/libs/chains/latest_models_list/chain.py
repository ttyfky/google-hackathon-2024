from __future__ import annotations

import datetime as dt
import re

from typing import List
from langchain_core.output_parsers import SimpleJsonOutputParser
from langchain_core.runnables import (
    Runnable,
    RunnablePassthrough,
)

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


def create_latest_models_collect_chain() -> Runnable:
    search_results = GoogleSearchJsonResultRetriever(
        query_tmpl="{query} 最新モデル", format="html"
    )
    return (
        {
            "context": search_results,
            "input": RunnablePassthrough(),
        }
        | prompt
        | get_langchain_model()
        | SimpleJsonOutputParser()
    )
