# main.py

from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, engine
from models import Base, PayrollRecord # Import Base and your model

# ----------------------------------------------------
# LIFESPAN FUNCTION (Replaces @app.on_event)
# ----------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP LOGIC: Create all tables defined in models.py if they don't exist
    print("Application starting up: Creating database tables if necessary...")
    async with engine.begin() as conn:
        # conn.run_sync executes synchronous SQLAlchemy commands (like metadata.create_all) 
        # within an asynchronous context.
        await conn.run_sync(Base.metadata.create_all) 
    print("Database startup tasks complete. Server ready.")
    
    # The 'yield' pauses the function while the application runs
    yield 

    # SHUTDOWN LOGIC: (If you needed any cleanup)
    print("Application shutting down.")

# Initialize FastAPI app with the lifespan function
app = FastAPI(lifespan=lifespan) 


# ----------------------------------------------------
# API ROUTES
# ----------------------------------------------------

@app.get("/")
def home():
    """Returns the basic status message."""
    return {"message": "Payroll system running! (DB setup complete)"} 

@app.get("/test-db-connection")
async def check_db_connection(db: AsyncSession = Depends(get_db)):
    """
    Tests the database connection and model presence.
    It runs a simple query against the 'payroll_records' table.
    """
    try:
        # Try to execute a simple, non-data-modifying query
        # This confirms the connection is live and the table exists
        await db.execute(f"SELECT 1 FROM {PayrollRecord.__tablename__} WHERE 1=0")
        
        return {"status": "SUCCESS", "message": "PostgreSQL connection and session active."}
    
    except Exception as e:
        return {"status": "FAILED", "message": f"Database connection failed: {e}"}
    