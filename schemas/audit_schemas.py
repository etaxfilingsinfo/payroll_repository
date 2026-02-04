# payroll_system/schemas/audit_schemas.py

from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID
from datetime import datetime


class AuditLogCreate(BaseModel):
    organisation_id: Optional[UUID] = None
    user_id: Optional[UUID] = None
    action: str
    entity: Optional[str] = None
    entity_id: Optional[UUID] = None
    details: Optional[dict] = None


class AuditLogOut(AuditLogCreate):
    log_id: UUID
    occurred_at: datetime

    model_config = ConfigDict(from_attributes=True)
