from typing import List, Dict
from app.core.indexing import get_bm25_retriever

async def query_local_kb(query: str) -> str:
    """Query the local knowledge base using BM25 retrieval."""
    try:
        retriever = get_bm25_retriever()
        nodes = retriever.retrieve(query)
        
        if not nodes:
            return "No relevant information found in the knowledge base."
        
        # Format retrieved content
        context_parts = []
        for node in nodes:
            content = node.get_content()
            metadata = node.metadata
            source = metadata.get("source", "Unknown")
            context_parts.append(f"From {source}:\n{content}\n")
        
        return "\n---\n".join(context_parts)
        
    except Exception as e:
        return f"Error querying knowledge base: {str(e)}"