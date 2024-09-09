from json import JSONDecodeError
import logging
from typing import Any, List

from langchain_core.exceptions import OutputParserException
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.outputs import Generation
from langchain_core.utils.json import parse_json_markdown

_logger = logging.getLogger(__name__)


class JsonOutputParserWithErrorCatch(JsonOutputParser):

    def parse_result(self, result: List[Generation], *, partial: bool = False) -> Any:
        """Parse the result of an LLM call to a JSON object.

        Args:
            result: The result of the LLM call.
            partial: Whether to parse partial JSON objects.
                If True, the output will be a JSON object containing
                all the keys that have been returned so far.
                If False, the output will be the full JSON object.
                Default is False.

        Returns:
            The parsed JSON object.

        Raises:
            OutputParserException: If the output is not valid JSON.
        """
        text = result[0].text
        text = text.strip()
        if partial:
            raise NotImplementedError("Partial JSON parsing is not supported.")
        else:
            try:
                return parse_json_markdown(text)
            except JSONDecodeError as e:
                _logger.error(e)
                msg = f"Invalid json output: {text}"
                return {
                    "error": repr(OutputParserException(msg, llm_output=text)),
                    "msg": msg,
                }
