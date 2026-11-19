import os
from functools import lru_cache

from langchain_openai import OpenAIEmbeddings

@lru_cache #caches the return for same params
def get_embedding_model():
    embeddings = OpenAIEmbeddings(model=os.environ["OPENAI_EMBEDDING_MODEL"])
    return embeddings