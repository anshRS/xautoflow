import os
import logging
from typing import Dict, Any, List, Optional
import json

from app.core.config import settings
from app.core.indexing import get_llamaindex_service

logger = logging.getLogger(__name__)

async def query_knowledge_base(query: str, top_k: int = 5, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Query the LlamaIndex knowledge base for relevant document chunks.
    
    Args:
        query: The query text
        top_k: Number of top results to return (default: 5)
        filters: Optional metadata filters to apply to the search
        
    Returns:
        Dictionary with search results
    """
    logger.info(f"Querying knowledge base: {query}")
    
    try:
        # Get the LlamaIndex service
        llamaindex_service = await get_llamaindex_service()
        
        # Query the index
        results = await llamaindex_service.query_index(query, top_k=top_k)
        
        # Apply filters if provided
        if filters and isinstance(filters, dict):
            filtered_results = []
            for result in results:
                if "metadata" in result:
                    # Check if result matches all filters
                    match = True
                    for key, value in filters.items():
                        if key not in result["metadata"] or result["metadata"][key] != value:
                            match = False
                            break
                    
                    if match:
                        filtered_results.append(result)
            results = filtered_results
        
        return {
            "status": "success",
            "query": query,
            "results": results,
            "result_count": len(results)
        }
    
    except Exception as e:
        logger.error(f"Error querying knowledge base: {e}", exc_info=True)
        return {
            "status": "error",
            "query": query,
            "error": str(e),
            "results": []
        }

async def add_document_to_kb(filepath: str) -> Dict[str, Any]:
    """Add a document to the knowledge base.
    
    Args:
        filepath: Path to the document to add
        
    Returns:
        Dictionary with status and document ID
    """
    logger.info(f"Adding document to knowledge base: {filepath}")
    
    try:
        # Check if file exists
        if not os.path.exists(filepath):
            return {
                "status": "error",
                "error": f"File not found: {filepath}",
                "filepath": filepath
            }
        
        # Get the LlamaIndex service
        llamaindex_service = await get_llamaindex_service()
        
        # Copy the file to the documents directory if it's not already there
        documents_dir = os.path.abspath(settings.DOCUMENTS_DIR)
        filename = os.path.basename(filepath)
        
        if not os.path.abspath(filepath).startswith(documents_dir):
            # Create the documents directory if it doesn't exist
            os.makedirs(documents_dir, exist_ok=True)
            
            # Copy the file
            import shutil
            dest_path = os.path.join(documents_dir, filename)
            shutil.copy2(filepath, dest_path)
            filepath = dest_path
        
        # Add document to the index
        document_ids = await llamaindex_service.add_documents_from_directory(
            directory=os.path.dirname(filepath)
        )
        
        return {
            "status": "success",
            "message": f"Document added to knowledge base: {filename}",
            "document_ids": document_ids,
            "filepath": filepath
        }
    
    except Exception as e:
        logger.error(f"Error adding document to knowledge base: {e}", exc_info=True)
        return {
            "status": "error",
            "error": str(e),
            "filepath": filepath
        }

async def list_kb_documents() -> Dict[str, Any]:
    """List all documents in the knowledge base.
    
    Returns:
        Dictionary with list of documents
    """
    logger.info("Listing knowledge base documents")
    
    try:
        # Get documents directory
        documents_dir = os.path.abspath(settings.DOCUMENTS_DIR)
        
        # Check if directory exists
        if not os.path.exists(documents_dir):
            return {
                "status": "success",
                "message": "Knowledge base directory does not exist yet",
                "documents": []
            }
        
        # List files in the documents directory
        documents = []
        for root, _, files in os.walk(documents_dir):
            for file in files:
                # Skip hidden files and system files
                if file.startswith('.'):
                    continue
                    
                # Get file path
                file_path = os.path.join(root, file)
                
                # Get relative path from documents directory
                rel_path = os.path.relpath(file_path, documents_dir)
                
                # Get file size
                file_size = os.path.getsize(file_path)
                
                # Get file extension
                _, ext = os.path.splitext(file)
                
                # Add document info
                documents.append({
                    "filename": file,
                    "path": rel_path,
                    "full_path": file_path,
                    "size": file_size,
                    "extension": ext
                })
        
        return {
            "status": "success",
            "documents_dir": documents_dir,
            "document_count": len(documents),
            "documents": documents
        }
    
    except Exception as e:
        logger.error(f"Error listing knowledge base documents: {e}", exc_info=True)
        return {
            "status": "error",
            "error": str(e)
        } 