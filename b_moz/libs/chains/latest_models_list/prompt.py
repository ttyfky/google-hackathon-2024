from langchain_core.prompts import ChatPromptTemplate

template_extract_model_release_info = """{input} に関する情報を含む html を渡します。
下記の情報を取り出してください。
- 機種名
- 発売日
- メーカー
出力の形式のルールは以下です。
1. JSON 形式にすること
    [{{"model": "機種名", "release_date": "発売日", "manufacturer": "メーカー"}}]
    例:
    [{{"model": "iPhone 8", "release_date": "2020-09-21", "manufacturer": "apple"}}]
2. 発売日が不明な場合は release_date を None とすること
    例:
    [{{"model": "iPhone 8", "release_date": "None", "manufacturer": "apple"}}]
3. メーカーが不明な場合は manufacturer を None とすること
    例:
    [{{"model": "iPhone 8", "release_date": "2020-09-21", "manufacturer": "None"}}]
4. 発売日が月までしかわからない場合は 1日 を発売日とすること
    例:
    [{{"model": "iPhone 8", "release_date": "2020-09-01", "manufacturer": "apple"}}]
5. {input} の発売日に関する情報がない場合は [] を出力すること
    例:
    []
以下が {input} に関する html です。
\n {context}\n
"""

LATEST_MODELS_LIST_PROMPT = ChatPromptTemplate.from_template(
    template_extract_model_release_info
)
