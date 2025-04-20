import os
import logging
from typing import Optional, List, Dict, Any
from pathlib import Path
from functools import lru_cache
import glob

from langchain_community.retrievers import BM25Retriever
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from app.core.config import settings

logger = logging.getLogger(__name__)

@lru_cache(maxsize=1)
def get_bm25_retriever() -> BM25Retriever:
    """
    Get or create a BM25 retriever for the local knowledge base.
    Uses lru_cache to avoid rebuilding the retriever unnecessarily.
    """
    logger.info("Building BM25 retriever")
    
    # Load documents from the configured directory
    documents = load_documents()
    
    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=512,
        chunk_overlap=50
    )
    splits = text_splitter.split_documents(documents)
    
    # Create and configure the BM25 retriever
    retriever = BM25Retriever.from_documents(
        documents=splits,
        k=5
    )
    
    logger.info(f"BM25 retriever built with {len(splits)} documents")
    return retriever

def load_documents() -> List[Any]:
    """
    Load documents from the configured knowledge base directory.
    
    Returns:
        List[Any]: List of loaded documents
    """
    kb_path = settings.LOCAL_KB_PATH
    
    if not os.path.exists(kb_path):
        logger.warning(f"Knowledge base directory {kb_path} does not exist. Creating it.")
        os.makedirs(kb_path, exist_ok=True)
        return []
    
    logger.info(f"Loading documents from {kb_path}")
    documents = []
    
    # Load all text files in the directory
    for file_path in glob.glob(os.path.join(kb_path, "*.txt")):
        try:
            loader = TextLoader(file_path)
            documents.extend(loader.load())
        except Exception as e:
            logger.error(f"Error loading file {file_path}: {str(e)}")
    
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
    retriever = get_bm25_retriever()
    docs = retriever.get_relevant_documents(query)
    
    # Extract and concatenate the content from the documents
    context = "\n\n".join([doc.page_content for doc in docs[:top_k]])
    return context 