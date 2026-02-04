# payroll_system/api/payroll_routes.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from database import get_async_db
from schemas.payroll_schemas import PayrollCreate, PayrollOut
from crud.payroll_crud import (
    create_payroll,
    get_payroll_by_id,
)
from utils.dependencies import get_admin_user


router = APIRouter(
    prefix="/payrolls",
    tags=["Payroll"],
)


# ============================================================
# CREATE PAYROLL RUN
# ============================================================

@router.post(
    "/",
    response_model=PayrollOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new payroll run",
    description="Creates a payroll run for a given pay period and organisation.",
)
async def create_new_payroll(
    data: PayrollCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user=Depends(get_admin_user)
):
    """Endpoint to create a new payroll run."""
    try:
        payroll = await create_payroll(db, data)
        return payroll
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# GET PAYROLL BY ID
# ============================================================

@router.get(
    "/{payroll_id}",
    response_model=PayrollOut,
    summary="Get a payroll run by ID",
    description="Fetch details of a specific payroll run by its UUID.",
)
async def get_payroll(
    payroll_id: UUID,
    db: AsyncSession = Depends(get_async_db),
    current_user=Depends(get_admin_user)
):
    """Retrieve payroll run by ID."""
    payroll = await get_payroll_by_id(db, payroll_id)
    if not payroll:
        raise HTTPException(status_code=404, detail="Payroll record not found")
    return payroll


# ============================================================
# LIST PAYROLL RUNS (OPTIONAL)
# ============================================================

# You can optionally implement this later once the corresponding CRUD exists.
# Example for completeness:

# from crud.payroll_crud import list_all_payrolls
#
# @router.get("/", response_model=list[PayrollOut], summary="List all payroll runs")
# async def list_all_payrolls(db: AsyncSession = Depends(get_async_db)):
#     """List all payroll runs."""
#     return await list_all_payrolls(db)
