from os import getenv

from langchain_openai import ChatOpenAI


def get_model():
    model = getenv("OPENAI_CHAT_MODEL")
    if not model:
        print("No model specified")
        exit(1)

    chat = ChatOpenAI(
        model_name=model,
    )
    return chat