import os
import logging
from typing import Optional, List, Dict, Any, Union
from pathlib import Path

from llama_index.core import (
    VectorStoreIndex, 
    SimpleDirectoryReader,
    StorageContext,
    Settings,
    Document
)
from llama_index.core.node_parser import SentenceSplitter
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.schema import MetadataMode
import chromadb

from app.core.config import settings, get_embedding_model
from app.models.database_models import KnowledgeDocument
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)

class LlamaIndexService:
    def __init__(self, db_session: Optional[AsyncSession] = None):
        """Initialize the LlamaIndex RAG service.
        
        Args:
            db_session: SQLAlchemy async session for database operations (optional)
        """
        self.db_session = db_session
        self.persist_dir = os.path.abspath(settings.PERSIST_DIR)
        self.documents_dir = os.path.abspath(settings.DOCUMENTS_DIR)
        self.chroma_client = None
        self.index = None
        self.storage_context = None
        
        # Ensure directories exist
        os.makedirs(self.persist_dir, exist_ok=True)
        os.makedirs(self.documents_dir, exist_ok=True)
        
        # Configure LlamaIndex settings
        # In a real implementation, we would properly initialize the embedding model
        # based on the configuration in settings
        try:
            embedding_model = get_embedding_model()
            Settings.embed_model = embedding_model
            # Additional settings like chunk size
            Settings.chunk_size = settings.CHUNK_SIZE
            Settings.chunk_overlap = settings.CHUNK_OVERLAP
        except Exception as e:
            logger.error(f"Error initializing embedding model: {e}")
            # Fallback to default embedding if configured embedding fails
            logger.warning("Using default embedding model")

    async def init_vector_store(self) -> None:
        """Initialize or load the vector store."""
        # Create Chroma client and collection
        persist_path = os.path.join(self.persist_dir, "chroma")
        
        self.chroma_client = chromadb.PersistentClient(path=persist_path)
        collection_name = "financial_knowledge"
        
        # Get or create collection
        try:
            collection = self.chroma_client.get_or_create_collection(name=collection_name)
            
            # Create ChromaVectorStore
            vector_store = ChromaVectorStore(chroma_collection=collection)
            
            # Create storage context
            self.storage_context = StorageContext.from_defaults(vector_store=vector_store)
            
            # Initialize empty index or load existing data
            self.index = VectorStoreIndex.from_vector_store(
                vector_store=vector_store,
            )
            
            logger.info(f"Vector store initialized with collection: {collection_name}")
        except Exception as e:
            logger.error(f"Error initializing vector store: {e}")
            raise
  
    async def add_documents_from_directory(self, directory: Optional[str] = None) -> List[str]:
        """Add documents from a directory to the vector store.
        
        Args:
            directory: Path to directory containing documents. 
                       Defaults to the configured documents directory.
        
        Returns:
            List of document IDs added to the index
        """
        if not directory:
            directory = self.documents_dir
            
        if not os.path.exists(directory):
            logger.warning(f"Directory not found: {directory}")
            return []
            
        try:
            # Load documents
            documents = SimpleDirectoryReader(directory).load_data()
            logger.info(f"Loaded {len(documents)} documents from {directory}")
            
            # Parse nodes with configured chunk size
            node_parser = SentenceSplitter(
                chunk_size=Settings.chunk_size,
                chunk_overlap=Settings.chunk_overlap
            )
            
            # Track added documents
            doc_ids = []
            
            # Ensure index is initialized
            if not self.index:
                await self.init_vector_store()
                
            # Insert documents into index
            for doc in documents:
                # Add custom metadata if needed
                if not doc.metadata:
                    doc.metadata = {}
                    
                # Add source filename to metadata
                if hasattr(doc, 'metadata') and 'file_path' in doc.metadata:
                    filename = os.path.basename(doc.metadata['file_path'])
                    doc.metadata['filename'] = filename
                
                # Insert document
                inserted_doc_id = self.index.insert(doc)
                doc_ids.append(inserted_doc_id)
                
                # If we have a DB session, record the document in the database
                if self.db_session:
                    # This would be implemented to store document metadata in the DB
                    # using the KnowledgeDocument model
                    pass
                    
            logger.info(f"Added {len(doc_ids)} documents to vector store")
            return doc_ids
            
        except Exception as e:
            logger.error(f"Error adding documents to vector store: {e}")
            raise

    async def query_index(self, query_text: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Query the vector store for relevant document chunks.
        
        Args:
            query_text: The query text
            top_k: Number of top results to return
            
        Returns:
            List of document chunks with text and metadata
        """
        if not self.index:
            await self.init_vector_store()
            
        try:
            # Query the index
            query_engine = self.index.as_query_engine(similarity_top_k=top_k)
            response = query_engine.query(query_text)
            
            # Process and format results
            results = []
            if hasattr(response, 'source_nodes'):
                for node in response.source_nodes:
                    results.append({
                        "text": node.node.get_content(metadata_mode=MetadataMode.NONE),
                        "metadata": node.node.metadata,
                        "score": node.score if hasattr(node, 'score') else None
                    })
                    
            return results
        except Exception as e:
            logger.error(f"Error querying index: {e}")
            raise

# Singleton instance for app-wide use
_llamaindex_service = None

async def get_llamaindex_service(db_session: Optional[AsyncSession] = None) -> LlamaIndexService:
    """Get or create the LlamaIndex service singleton."""
    global _llamaindex_service
    if _llamaindex_service is None:
        _llamaindex_service = LlamaIndexService(db_session)
        await _llamaindex_service.init_vector_store()
    return _llamaindex_service 