from typing import List, Dict, Any, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.ext.asyncio import AsyncSession
import os
import shutil
import tempfile

from app.data.database import get_db
from app.models.api_models import KnowledgeBaseQuery, KnowledgeBaseResponse, DocumentUpload, DocumentChunk
from app.tools.rag_tools import query_knowledge_base, add_document_to_kb, list_kb_documents
from app.core.config import settings

router = APIRouter(
    prefix="/kb",
    tags=["knowledge-base"],
    responses={404: {"description": "Not found"}}
)

@router.post("/query", response_model=KnowledgeBaseResponse)
async def query_kb(
    query_request: KnowledgeBaseQuery,
    db: AsyncSession = Depends(get_db)
) -> KnowledgeBaseResponse:
    """Query the knowledge base for relevant document chunks."""
    result = await query_knowledge_base(
        query=query_request.query,
        top_k=query_request.top_k,
        filters=query_request.filter_metadata
    )
    
    if result["status"] == "error":
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result["error"]
        )
    
    # Convert results to DocumentChunk model
    document_chunks = []
    for item in result["results"]:
        document_chunks.append(DocumentChunk(
            text=item["text"],
            metadata=item["metadata"],
            score=item["score"]
        ))
    
    return KnowledgeBaseResponse(
        query=query_request.query,
        results=document_chunks,
        total_results=len(document_chunks)
    )

@router.post("/documents/upload", response_model=DocumentUpload)
async def upload_document(
    file: UploadFile = File(...),
    description: Optional[str] = Form(None),
    db: AsyncSession = Depends(get_db)
) -> DocumentUpload:
    """Upload a document to the knowledge base."""
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            # Write uploaded file content to temporary file
            shutil.copyfileobj(file.file, temp_file)
            temp_path = temp_file.name
        
        # Add the document to knowledge base
        result = await add_document_to_kb(temp_path)
        
        # Remove temporary file
        try:
            os.unlink(temp_path)
        except Exception as e:
            # Just log the error, but don't fail the request
            print(f"Error removing temporary file: {str(e)}")
        
        if result["status"] == "error":
            return DocumentUpload(
                filename=file.filename,
                success=False,
                message=result["error"]
            )
        
        return DocumentUpload(
            filename=file.filename,
            success=True,
            message="Document uploaded and indexed successfully"
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error uploading document: {str(e)}"
        )

@router.get("/documents", response_model=Dict[str, Any])
async def get_kb_documents(db: AsyncSession = Depends(get_db)) -> Dict[str, Any]:
    """List all documents in the knowledge base."""
    result = await list_kb_documents()
    
    if result["status"] == "error":
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result["error"]
        )
    
    return {
        "documents": result["documents"],
        "total": result["document_count"],
        "documents_dir": result["documents_dir"]
    } 