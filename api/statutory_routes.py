# payroll_system/api/statutory_routes.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import Optional, List   # ✅ Add this line

from database import get_async_db
from schemas.statutory_schemas import StatutoryCreate, StatutoryOut, StatutoryUpdate
from crud.statutory_crud import (
    create_statutory_setting,
    get_statutory_setting,
    update_statutory_setting,
    list_statutory_settings
)
from utils.dependencies import get_admin_user

router = APIRouter(prefix="/statutory", tags=["Statutory"])


# ------------------------------------------------------------
# Create statutory setting
# ------------------------------------------------------------
@router.post("/", response_model=StatutoryOut, status_code=status.HTTP_201_CREATED)
async def create_statutory_setting_route(
    data: StatutoryCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user=Depends(get_admin_user)
):
    return await create_statutory_setting(db, data)


# ------------------------------------------------------------
# Get statutory setting by ID
# ------------------------------------------------------------
@router.get("/{statutory_id}", response_model=StatutoryOut)
async def get_statutory_setting_route(
    statutory_id: UUID,
    db: AsyncSession = Depends(get_async_db)
):
    setting = await get_statutory_setting(db, statutory_id)
    if not setting:
        raise HTTPException(status_code=404, detail="Statutory setting not found")
    return setting


# ------------------------------------------------------------
# Update statutory setting
# ------------------------------------------------------------
@router.put("/{statutory_id}", response_model=StatutoryOut)
async def update_statutory_setting_route(
    statutory_id: UUID,
    data: StatutoryUpdate,
    db: AsyncSession = Depends(get_async_db),
    current_user=Depends(get_admin_user)
):
    updated = await update_statutory_setting(db, statutory_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Statutory setting not found")
    return updated


# ------------------------------------------------------------
# List all statutory settings
# ------------------------------------------------------------
@router.get("/", response_model=List[StatutoryOut])
async def list_statutory_settings_route(
    db: AsyncSession = Depends(get_async_db),
    organisation_id: Optional[UUID] = None
):
    return await list_statutory_settings(db, organisation_id)
