# TODO: Verify the template.
from langchain_core.prompts import ChatPromptTemplate

template_extract_new_models = """You are specialist of mobile phone catalog who knows manufacturer, 
series, available storages, colors and other details. Input can be Japanese or English.
Extract following information from the given context document, and return the data as JSON object.
The JSON object must use double quotes for keys and values.
You can use own knowledge to provide the information, but do not make hallucination.
Fields to extract:
- Model name
- Storages
- Colors
  - This can be `仕上げ` if model is for Apple
- Manufacturer
- Series
Response format:
- The value is official name which is extracted from the context.
Example:
Input: iphone-7
Answer: {{ "query":'iphone-7", 
            "model": "iPhone 7", 
            "manufacturer": "Apple", 
            "series": "iPhone",
            "storages":["32GB", "128GB", "256GB"],
            "colors":["ブラック", "ゴールド", "ローズゴールド", "シルバー", "ジェットブラック"]
        }} 
Context: \n {context}\n
Input Model: \n {input} \n
Answer:
"""
SPEC_EXTRACT_PROMPT = ChatPromptTemplate.from_template(template_extract_new_models)
