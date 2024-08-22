import logging

from b_moz.libs.chains.spec_extract.chain import create_spec_extract_chain

_logger = logging.getLogger(__name__)


class CollectSpec:
    def __init__(self, spec_repo):
        self.spec_repo = spec_repo
        self.chain = create_spec_extract_chain()

    def collect(self, target_query: str) -> str:
        try:
            extracted = self.chain.invoke(input=target_query)
            _logger.info(f"Extracted spec: {extracted}")
            # TODO: save extracted.

            return extracted
        except Exception as e:
            _logger.error(
                f"Failed to extract spec for [{target_query}] with error: {e}"
            )
            raise e


def create_target_spec_usecase(spec_repo):
    return CollectSpec(spec_repo)
