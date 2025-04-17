from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import StaticPool

from app.models import UserModel
from app.models.base import ORMBase

DB_URI = "sqlite+aiosqlite:///test.db"

# Shared test engine
test_engine: AsyncEngine = create_async_engine(
    DB_URI,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

# Shared sessionmaker
TestingSessionLocal = async_sessionmaker(
    bind=test_engine,
    autoflush=False,
    expire_on_commit=False,
)


async def init_test_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(ORMBase.metadata.create_all)


async def get_test_db_session() :
    async with TestingSessionLocal() as session:
        yield session


async def drop_test_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(ORMBase.metadata.drop_all)
    await test_engine.dispose()
