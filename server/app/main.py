import logging
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.data.database import get_db, Base, async_engine
from app.routers import agents, kb
from app.core.indexing import get_llamaindex_service

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Create application
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(agents.router, prefix=settings.API_V1_STR)
app.include_router(kb.router, prefix=settings.API_V1_STR)

@app.on_event("startup")
async def startup_event():
    """Perform startup initialization."""
    logging.info("Starting application...")

    # Create database tables
    async with async_engine.begin() as conn:
        # Uncomment to create tables on startup (development)
        # await conn.run_sync(Base.metadata.create_all)
        pass
    
    # Initialize LlamaIndex service
    try:
        llamaindex_service = await get_llamaindex_service()
        logging.info("LlamaIndex service initialized successfully")
    except Exception as e:
        logging.error(f"Error initializing LlamaIndex service: {e}")
        # Don't fail startup, just log the error

@app.on_event("shutdown")
async def shutdown_event():
    """Perform cleanup on shutdown."""
    logging.info("Shutting down application...")
    # Close any connections or resources

@app.get("/", status_code=200)
def root():
    """Root endpoint for health checks."""
    return {"message": "Server Running"}

@app.get(f"{settings.API_V1_STR}/health", status_code=200)
async def health_check(request: Request, db: AsyncSession = Depends(get_db)):
    """Health check endpoint that verifies database connection."""
    try:
        # Test database connection
        query = "SELECT 1"
        await db.execute(query)
        
        return {
            "status": "ok",
            "api_version": settings.API_V1_STR,
            "environment": settings.ENVIRONMENT
        }
    except Exception as e:
        logging.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Database connection failed") 