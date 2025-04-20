import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from app.core.config import settings
from app.db.session import Base

async def init_db():
    engine = create_async_engine(
        str(settings.DATABASE_URL).replace('postgresql://', 'postgresql+asyncpg://'),
        echo=True
    )
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(init_db()) 