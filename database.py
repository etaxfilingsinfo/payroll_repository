from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from settings import settings

# 1. Asynchronous Database Engine
# Ensure asyncpg driver is used for async PostgreSQL connectivity
ASYNC_DATABASE_URL = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=False,  # Set True for SQL query debug logging
)

# 2. Asynchronous Session Factory
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)

# 3. Base class for ORM models
Base = declarative_base()

# 4. Dependency function to get async DB session for FastAPI routes
async def get_async_db():
    async with AsyncSessionLocal() as session:
        yield session
