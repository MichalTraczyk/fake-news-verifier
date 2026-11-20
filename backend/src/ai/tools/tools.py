from datetime import datetime, timezone

from langchain_core.documents import Document
from langchain_core.tools import tool

from ai.rag.embeddings import get_embedding_model
from ai.rag.vectorstore import get_vector_store

@tool(response_format="content_and_artifact")
def retrieve_info(query: str):
    """Search internal documents."""
    docs = get_vector_store().similarity_search(query, k=3)
    if not docs:
        return "No relevant documents found.", []
    content = "\n\n".join(f"[{d.metadata.get('source')}]\n{d.page_content}" for d in docs)
    return content, docs

@tool
def save_info(fact: str, topic: str) -> str:
    """Save a new fact to the knowledge base when you are fairly confident that it's reliabke"""
    existing = get_vector_store().similarity_search(fact, k=1)
    if existing and existing[0].page_content.strip() == fact.strip():
        return f"Already in the knowledge base, not saved again: {fact}"

    get_vector_store().add_documents([
        Document(
            page_content=fact,
            metadata={
                "source": "user",
                "topic": topic,
                "added_at": datetime.now(timezone.utc).isoformat(),
            },
        )
    ])
    return f"Saved: {fact}"