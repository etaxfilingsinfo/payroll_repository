"""
reset_db.py
Drops and recreates all tables using the Async SQLAlchemy engine.
"""

import asyncio
import sys
import os

# ✅ Fix import path (ensures script runs from anywhere)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from payroll_system.database import engine, Base


async def reset_database():
    print("⚙️  Resetting database schema...")

    async with engine.begin() as conn:
        # Drop all existing tables
        await conn.run_sync(Base.metadata.drop_all)
        print("🗑️  All existing tables dropped successfully.")

        # Recreate all tables
        await conn.run_sync(Base.metadata.create_all)
        print("✅ All tables recreated successfully.")

    await engine.dispose()
    print("🎉 Database reset completed!")


if __name__ == "__main__":
    asyncio.run(reset_database())
