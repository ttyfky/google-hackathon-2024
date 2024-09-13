from pathlib import Path
from typing import Dict, Iterator, Union

import requests
from bs4 import BeautifulSoup
from langchain.docstore.document import Document
from langchain_community.document_loaders import BSHTMLLoader

from b_moz.libs.o11y.trace import tracing


@tracing
def fetch_url_content(url):
    try:
        response = requests.get(url, timeout=10)
        response.encoding = response.apparent_encoding
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None


class CustomBSHTMLLoader(BSHTMLLoader):
    """Custom BSHTMLLoader that can handle both file paths and StringIO objects."""

    def __init__(
            self,
            file_path: str | Path,
            open_encoding: str | None = None,
            bs_kwargs: Dict | None = None,
            get_text_separator: str = "",
            as_html: bool = False,
    ) -> None:
        super().__init__(file_path, open_encoding, bs_kwargs, get_text_separator)
        self.as_html = as_html

    @tracing
    def lazy_load(self) -> Iterator[Document]:
        """Load HTML document into document objects."""
        metadata: Dict[str, Union[str, None]] = {}
        if isinstance(self.file_path, str) and self.file_path.startswith("http"):
            metadata["source"] = self.file_path
            html = fetch_url_content(self.file_path)
            if html is None:
                raise ValueError(f"Failed to fetch {self.file_path}")
            soup = BeautifulSoup(markup=html, **self.bs_kwargs)
        else:
            metadata["source"] = str(self.file_path)
            with open(self.file_path, "r", encoding=self.open_encoding) as f:
                soup = BeautifulSoup(f, **self.bs_kwargs)

        for s in soup(["script", "style"]):
            s.extract()

        if self.as_html:
            text = str(soup.body)
        else:
            text = soup.get_text(self.get_text_separator)

        if soup.title:
            title = str(soup.title.string)
        else:
            title = ""

        metadata["title"] = title

        yield Document(page_content=text, metadata=metadata)
