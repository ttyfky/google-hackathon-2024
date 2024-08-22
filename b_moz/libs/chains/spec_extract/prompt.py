# TODO: Verify the template.
from langchain_core.prompts import ChatPromptTemplate

template_extract_new_models = """You are specialist of mobile phone catalog who knows manufacturer, 
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
SPEC_EXTRACT_PROMPT = ChatPromptTemplate.from_template(template_extract_new_models)
