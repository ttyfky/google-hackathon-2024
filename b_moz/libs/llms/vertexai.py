from langchain_core.language_models import BaseLanguageModel
from langchain_google_vertexai import ChatVertexAI, HarmBlockThreshold, HarmCategory


def get_langchain_model(model_name: str = "gemini-1.5-flash-001") -> BaseLanguageModel:
    return ChatVertexAI(
        model_name=model_name,
        convert_system_message_to_human=True,
        safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE
        },
    )
