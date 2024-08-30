# TODO: Verify the template.
from langchain_core.prompts import ChatPromptTemplate

extract_instruction = """Input can be Japanese or English.
Extract following information from the given context document, and return the data as JSON object.
The JSON object must use double quotes for keys and values.
You can use own knowledge to provide the information, but do not make hallucination. 
"""

smartphone_prefix = """You are specialist of mobile phone catalog who knows manufacturer, 
series, available storages, colors and other details.
"""

template_extract_smartphone_spec = (
    smartphone_prefix
    + extract_instruction
    + """Fields to extract:
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
)

SMARTPHONE_SPEC_EXTRACT_PROMPT = ChatPromptTemplate.from_template(
    template_extract_smartphone_spec
)

pc_prefix = """You are specialist of PC who knows 
manufacturer, series, available CPU, RAM, storages, colors and other details.
"""

template_extract_pc_spec = (
    pc_prefix
    + extract_instruction
    + """
Fields to extract:
- Model name
- Storages
- CPUs
- RAMs
- Size
- Colors
  - This can be `仕上げ` if model is for Apple
- Manufacturer
- Series
Response format:
- The value is official name which is extracted from the context.
Example:
Input: MacBook Pro (14インチ, 2023) 
Answer: {{ "query":'MacBook Pro (14インチ, 2023) ", 
            "model": "MacBook Pro (14インチ, 2023) ", 
            "manufacturer": "Apple", 
            "series": "MacBook Pro",
            "storages":["512GB", "1TB", "2TB","4TB","8TB"],
            "colors":["シルバー", "スペースグレイ"],
            "cpus": ["Apple M2 Proチップ","Apple M2 Maxチップ"],
            "rams": ["16GB", "32GB"],
        }} 
Context: \n {context}\n
Input Model: \n {input} \n
Answer:
"""
)

PC_SPEC_EXTRACT_PROMPT = ChatPromptTemplate.from_template(template_extract_pc_spec)

if __name__ == "__main__":
    print(ChatPromptTemplate.from_template(template_extract_pc_spec))
