import logging
from typing import List

from langchain_core.callbacks.manager import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_google_community import GoogleSearchAPIWrapper

from b_moz.libs.document_loaders.custom_bs_loader import CustomBSHTMLLoader

num_results = 3
_logger = logging.getLogger(__name__)


class GoogleSearchJsonResultRetriever(BaseRetriever):
    """Google Search Retriever."""

    query_tmpl: str
    as_html: bool

    def __init__(self, query_tmpl: str, as_html: bool = False):
        super().__init__(query_tmpl=query_tmpl, as_html=as_html)  # type: ignore

    def _get_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:
        search = GoogleSearchAPIWrapper()
        results = search.results(
            query=self.query_tmpl.format(query=query), num_results=num_results
        )
        docs = []
        for r in results:
            try:
                docs.append(self._fetch_as_document(r["link"]))
            except Exception as e:
                _logger.error(f"Failed to fetch {r['link']} with error: {e}")
                continue
        return docs

    def _fetch_as_document(self, url: str) -> Document:
        _logger.info(f"Fetching {url}")

        as_html = self.as_html
        return CustomBSHTMLLoader(file_path=url, as_html=as_html).load()[0]
