from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import NullPool

from app.core.config import settings

# Create async engine instance
# NullPool is often recommended for serverless/async environments
# to avoid issues with shared connections across event loops/processes.
async_engine = create_async_engine(
    str(settings.DATABASE_URL), # Ensure the URL is a string
    echo=settings.ENVIRONMENT == "development", # Log SQL queries in dev
    poolclass=NullPool # Avoid connection pooling issues in async/serverless
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False, # Keep objects accessible after commit
    autocommit=False,
    autoflush=False,
)

# Base class for declarative class definitions
class Base(DeclarativeBase):
    pass

# Dependency to get DB session
async def get_db() -> AsyncSession:
    """FastAPI dependency that provides an async database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            # Optionally commit here if you want automatic commit per request
            # await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close() 