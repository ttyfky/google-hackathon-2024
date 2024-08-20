import logging
import os
from typing import Dict

from langchain_core.output_parsers import SimpleJsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnablePassthrough

from b_moz.libs.llms import vertexai
from b_moz.libs.retreivers.model_detail_retriever import ModelSpecDocRetriever

template = """You are specialist of mobile phone catalog who knows manufacturer, 
series, available storages, colors and other details. Input can be Japanese or English.
Extract following information from the given context document, and return the data as JSON object.
You can use own knowledge to provide the information, but do not make hallucination.
Fields to extract:
- Model name
- Storages
- Colors
  - This can be `仕上げ` if model is for Apple
- Manufacturer
- Series
Response format
Response contains the value and key.
- The value is official name which is extracted from the context.
- The key is a format suitable for system id. Based on the value, but all lower case and replace space with hyphen.
  - If the value is not english, translate it to english and apply the rule.
- Manufacturer and series can return only key, but the other fields must return a pair of key and value.
Example:
Input: iphone-7
Answer: {{ "query":'iphone-7", 
            "model": {{"key": "iphone-7",  "value": "iPhone 7"}}, 
            "manufacturer": "apple", 
            "series": "iphone",
            "storages":[{{"key": "32gb", "value": "32GB"}},
                        {{"key": "128gb", "value": "128GB"}},
                        {{"key": "256gb", "value": "256GB"}}],
            "colors":[{{"key": "black", "value": "ブラック"}}, 
                        {{ "key": "silver", "value": "シルバー"}},
                        {{ "key": "jetblack", "value": "ジェットブラック"}},] }}
            }} }}
Context: \n {context}\n
Input Model: \n {input} \n
Answer:
"""
classify_model_abstraction_prompt = ChatPromptTemplate.from_template(template)


class ModelAttributesPrediction:
    def __init__(self, llm=None):
        self._logger = logging.getLogger(__name__)
        if llm:
            self.llm = llm
        else:
            self.llm = vertexai.get_langchain_model()

        self._model_attr_chain: Runnable = (
            {"context": ModelSpecDocRetriever(), "input": RunnablePassthrough()}
            | classify_model_abstraction_prompt
            | self.llm
            | SimpleJsonOutputParser()
        )

    def predict(
        self,
        query: str,
    ) -> Dict:
        self._logger.info(f"Estimating model for [{query}] with gemini")
        try:
            res = self._model_attr_chain.with_config(
                configurable={"llm": "vertexai"}
            ).invoke(query)
        except Exception as e:
            self._logger.error(
                f"Failed to estimate model for [{query}] in gemini with error: {e}"
            )
            res = {"message": str(e)}

        return res


def build() -> ModelAttributesPrediction:
    if os.environ.get("USE_MOCK", "false").lower() == "true":
        from ...libs.llms import mock_model

        return ModelAttributesPrediction(llm=mock_model.get_langchain_model([]))

    return ModelAttributesPrediction()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    result = build().predict("iPhone 15")
    print(result)
