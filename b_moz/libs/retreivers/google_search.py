import logging
from typing import List

from langchain_core.callbacks.manager import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_google_community import GoogleSearchAPIWrapper

from b_moz.libs.document_loaders.custom_bs_loader import CustomBSHTMLLoader

MAX_RESULTS = 10
_logger = logging.getLogger(__name__)


class GoogleSearchJsonResultRetriever(BaseRetriever):
    """Google Search Retriever."""

    query_tmpl: str
    as_html: bool
    num_results: int

    def __init__(self, query_tmpl: str, as_html: bool = False, num_results: int = 3):
        super().__init__(query_tmpl=query_tmpl, as_html=as_html, num_results=num_results)  # type: ignore

    def _get_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:
        search = GoogleSearchAPIWrapper()
        results = search.results(
            query=self.query_tmpl.format(query=query), num_results=MAX_RESULTS
        )
        docs = []
        for r in results:
            link = r["link"]
            if link.endswith(".pdf"):
                # some pdf causes invalid augument error
                _logger.info(f"Skip to fetch pdf: {link}")
                continue
            try:
                docs.append(self._fetch_as_document(link))
                if len(docs) >= self.num_results:
                    break
            except Exception as e:
                _logger.warning(f"Failed to fetch {link} with error: {e}")
                continue
        return docs

    def _fetch_as_document(self, url: str) -> Document:
        _logger.info(f"Fetching {url}")

        as_html = self.as_html
        return CustomBSHTMLLoader(file_path=url, as_html=as_html).load()[0]
