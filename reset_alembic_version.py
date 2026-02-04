# reset_alembic_version.py
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from settings import settings

async def reset_alembic():
    print("⚙️  Resetting Alembic version table...")

    # Create async engine using your configured database URL
    engine = create_async_engine(settings.DATABASE_URL, echo=False)

    async with engine.begin() as conn:
        # ✅ Use SQLAlchemy `text()` wrapper for raw SQL strings
        await conn.execute(text("DROP TABLE IF EXISTS alembic_version;"))

    print("✅ Alembic version table dropped successfully.")

if __name__ == "__main__":
    asyncio.run(reset_alembic())
