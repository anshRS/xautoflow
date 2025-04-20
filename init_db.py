import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from app.models.base import Base
from app.core.config import settings

async def init_db():
    engine = create_async_engine(str(settings.DATABASE_URL))
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()

if __name__ == "__main__":
    print("Creating database tables...")
    asyncio.run(init_db())
    print("Database tables created successfully!") 