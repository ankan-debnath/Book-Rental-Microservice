from pydantic import with_config
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.testing import assert_warns

from app.common.settings import settings

ENGINE = create_async_engine(settings.DB_URL)

session_maker = async_sessionmaker(bind=ENGINE, class_=AsyncSession, expire_on_commit=True)

async def get_session():
    async with session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()