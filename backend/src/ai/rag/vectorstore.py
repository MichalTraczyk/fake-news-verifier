from functools import lru_cache

from langchain_core.vectorstores import InMemoryVectorStore

from ai.rag.embeddings import get_embedding_model

@lru_cache #caches the return for same params
def get_vector_store():
    vector_store = InMemoryVectorStore(get_embedding_model())
    return vector_store

