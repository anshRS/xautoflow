import os
import logging
from typing import Optional, List, Dict, Any
from pathlib import Path
from functools import lru_cache

from llama_index.core import (
    SimpleDirectoryReader,
    Document,
    StorageContext,
    Settings
)
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.retrievers import BM25Retriever
from llama_index.core.schema import TextNode

from app.core.config import settings

logger = logging.getLogger(__name__)

# Cache the retriever to avoid rebuilding it unnecessarily
@lru_cache(maxsize=1)
def build_bm25_retriever(force_rebuild: bool = False) -> BM25Retriever:
    """
    Build a BM25 retriever for the local knowledge base.
    
    Args:
        force_rebuild: If True, rebuild the retriever even if it's cached
        
    Returns:
        BM25Retriever: The configured BM25 retriever
    """
    logger.info("Building BM25 retriever")
    
    # Load documents from the configured directory
    documents = load_documents()
    
    # Parse documents into nodes
    parser = SentenceSplitter(chunk_size=512, chunk_overlap=50)
    nodes = []
    
    for doc in documents:
        doc_nodes = parser.get_nodes_from_documents([doc])
        nodes.extend(doc_nodes)
    
    # Create a simple storage context
    storage_context = StorageContext.from_defaults()
    
    # Add nodes to the storage context
    for node in nodes:
        storage_context.docstore.add_documents([node])
    
    # Create and configure the BM25 retriever
    retriever = BM25Retriever.from_defaults(
        docstore=storage_context.docstore,
        similarity_top_k=5
    )
    
    logger.info(f"BM25 retriever built with {len(nodes)} nodes")
    return retriever

def load_documents() -> List[Document]:
    """
    Load documents from the configured knowledge base directory.
    
    Returns:
        List[Document]: List of loaded documents
    """
    kb_path = settings.LOCAL_KB_PATH
    
    if not os.path.exists(kb_path):
        logger.warning(f"Knowledge base directory {kb_path} does not exist. Creating it.")
        os.makedirs(kb_path, exist_ok=True)
        return []
    
    logger.info(f"Loading documents from {kb_path}")
    reader = SimpleDirectoryReader(kb_path)
    documents = reader.load_data()
    logger.info(f"Loaded {len(documents)} documents")
    return documents

async def query_local_kb(query: str, top_k: int = 5) -> str:
    """
    Query the local knowledge base using BM25 retrieval.
    
    Args:
        query: The query string
        top_k: Number of results to return
        
    Returns:
        str: Concatenated context from retrieved documents
    """
    retriever = build_bm25_retriever()
    nodes = retriever.retrieve(query)
    
    # Extract and concatenate the content from the nodes
    context = "\n\n".join([node.text for node in nodes[:top_k]])
    return context 