# payroll_system/crud/audit_crud.py

from typing import Optional, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from payroll_system.models.audit_models import AuditLog
from payroll_system.schemas.audit_schemas import AuditLogCreate


async def log_action(db: AsyncSession, payload: AuditLogCreate) -> AuditLog:
    """
    Write a new audit log entry.
    """
    rec = AuditLog(**payload.model_dump())
    try:
        db.add(rec)
        await db.commit()
        await db.refresh(rec)
        return rec
    except IntegrityError as e:
        await db.rollback()
        raise ValueError("Failed to write audit log") from e


async def get_audit_logs(
    db: AsyncSession,
    organisation_id: Optional[UUID] = None,
    limit: int = 100
) -> List[AuditLog]:
    """
    Retrieve recent audit log entries optionally filtered by organisation.
    Results sorted by most recent first, limited by `limit`.
    """
    q = select(AuditLog)
    if organisation_id:
        q = q.filter(AuditLog.organisation_id == organisation_id)
    q = q.order_by(AuditLog.occurred_at.desc()).limit(limit)
    res = await db.execute(q)
    return res.scalars().all()
