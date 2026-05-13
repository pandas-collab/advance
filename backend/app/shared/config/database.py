"""Database configuration with performance optimization."""
import os
from typing import AsyncGenerator
from sqlalchemy import create_engine, pool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database URL from environment
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:password@localhost:5432/age_calculator"
)

# Async database URL
ASYNC_DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

# Database configuration for performance
DB_CONFIG = {
    # Connection pool settings for performance
    "pool_size": int(os.getenv("DB_POOL_SIZE", "10")),
    "max_overflow": int(os.getenv("DB_MAX_OVERFLOW", "20")),
    "pool_timeout": int(os.getenv("DB_POOL_TIMEOUT", "30")),
    "pool_recycle": int(os.getenv("DB_POOL_RECYCLE", "3600")),  # 1 hour
    "pool_pre_ping": True,  # Validate connections before use

    # Performance settings
    "echo": os.getenv("DB_ECHO", "false").lower() == "true",
    "echo_pool": os.getenv("DB_ECHO_POOL", "false").lower() == "true",
    "future": True,
}

# Create SQLAlchemy engine with optimizations
engine = create_engine(
    DATABASE_URL,
    poolclass=pool.QueuePool,
    pool_size=DB_CONFIG["pool_size"],
    max_overflow=DB_CONFIG["max_overflow"],
    pool_timeout=DB_CONFIG["pool_timeout"],
    pool_recycle=DB_CONFIG["pool_recycle"],
    pool_pre_ping=DB_CONFIG["pool_pre_ping"],
    echo=DB_CONFIG["echo"],
    echo_pool=DB_CONFIG["echo_pool"],
    future=DB_CONFIG["future"],
)

# Create async engine for FastAPI
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    pool_size=DB_CONFIG["pool_size"],
    max_overflow=DB_CONFIG["max_overflow"],
    pool_timeout=DB_CONFIG["pool_timeout"],
    pool_recycle=DB_CONFIG["pool_recycle"],
    pool_pre_ping=DB_CONFIG["pool_pre_ping"],
    echo=DB_CONFIG["echo"],
    future=DB_CONFIG["future"],
)

# Session factories
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False  # Performance optimization
)

AsyncSessionLocal = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)

# Base class for models
Base = declarative_base()

class DatabaseManager:
    """Database manager for connection handling and performance monitoring."""

    def __init__(self):
        self.engine = engine
        self.async_engine = async_engine
        self.session_factory = SessionLocal
        self.async_session_factory = AsyncSessionLocal

    async def get_async_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get async database session with proper cleanup."""
        async with self.async_session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    def get_session(self):
        """Get synchronous database session."""
        session = self.session_factory()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    async def health_check(self) -> bool:
        """Check database health and connectivity."""
        try:
            async with self.async_engine.begin() as conn:
                result = await conn.execute("SELECT 1")
                return result.scalar() == 1
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False

    async def get_connection_info(self) -> dict:
        """Get database connection information for monitoring."""
        pool = self.async_engine.pool
        return {
            "pool_size": pool.size(),
            "checked_in": pool.checkedin(),
            "checked_out": pool.chec
