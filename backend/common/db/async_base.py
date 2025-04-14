import json
import logging
from contextlib import asynccontextmanager
from typing import Any, Optional, AsyncGenerator

from sqlalchemy import MetaData, types
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.type_api import _T
from sqlalchemy import Dialect

# Will be imported from environment variables in a real implementation
DATABASE_URL = "sqlite+aiosqlite:///./webui.db"
DATABASE_SCHEMA = None
DATABASE_POOL_SIZE = 0
DATABASE_POOL_MAX_OVERFLOW = 10
DATABASE_POOL_RECYCLE = 3600
DATABASE_POOL_TIMEOUT = 30

log = logging.getLogger(__name__)


class JSONField(types.TypeDecorator):
    impl = types.Text
    cache_ok = True

    def process_bind_param(self, value: Optional[_T], dialect: Dialect) -> Any:
        return json.dumps(value) if value is not None else None

    def process_result_value(self, value: Optional[_T], dialect: Dialect) -> Any:
        if value is not None:
            return json.loads(value)
        return None

    def copy(self, **kw: Any) -> 'JSONField':
        return JSONField()


# Create async engine
SQLALCHEMY_DATABASE_URL = DATABASE_URL

# Ensure we're using the correct async driver
if "sqlite" in SQLALCHEMY_DATABASE_URL:
    # Default case for SQLite
    async_engine = create_async_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
elif "postgresql" in SQLALCHEMY_DATABASE_URL:
    # Replace postgresql:// with postgresql+asyncpg://
    if not "asyncpg" in SQLALCHEMY_DATABASE_URL:
        SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgresql", "postgresql+asyncpg", 1)

    if DATABASE_POOL_SIZE > 0:
        async_engine = create_async_engine(
            SQLALCHEMY_DATABASE_URL,
            pool_size=DATABASE_POOL_SIZE,
            max_overflow=DATABASE_POOL_MAX_OVERFLOW,
            pool_timeout=DATABASE_POOL_TIMEOUT,
            pool_recycle=DATABASE_POOL_RECYCLE,
            pool_pre_ping=True,
        )
    else:
        async_engine = create_async_engine(
            SQLALCHEMY_DATABASE_URL, pool_pre_ping=True
        )
else:
    # Default case for other database types
    if DATABASE_POOL_SIZE > 0:
        async_engine = create_async_engine(
            SQLALCHEMY_DATABASE_URL,
            pool_size=DATABASE_POOL_SIZE,
            max_overflow=DATABASE_POOL_MAX_OVERFLOW,
            pool_timeout=DATABASE_POOL_TIMEOUT,
            pool_recycle=DATABASE_POOL_RECYCLE,
            pool_pre_ping=True,
        )
    else:
        async_engine = create_async_engine(
            SQLALCHEMY_DATABASE_URL, pool_pre_ping=True
        )


# Create async session
AsyncSessionLocal = async_sessionmaker(
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    expire_on_commit=False,
)

metadata_obj = MetaData(schema=DATABASE_SCHEMA)
Base = declarative_base(metadata=metadata_obj)


@asynccontextmanager
async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """Get an async database session"""
    session = AsyncSessionLocal()
    try:
        yield session
    finally:
        await session.close()
