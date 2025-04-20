from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.api import api_router
from app.core.config import settings
from app.core.logging import setup_logging

app = FastAPI(title="XAutoFlow API")

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up logging
setup_logging()

# Include routers
app.include_router(api_router, prefix="/api/v1")


@app.on_event("startup")
async def startup_event():
    # Initialize BM25 retriever
    from app.core.indexing import build_bm25_retriever
    build_bm25_retriever(force_rebuild=True)
    
    # Verify database connection
    from app.db.session import engine
    from app.db.base import Base
    Base.metadata.create_all(bind=engine)

@app.on_event("shutdown")
async def shutdown_event():
    # Close any open connections
    from app.db.session import engine
    engine.dispose()