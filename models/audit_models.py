from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from payroll_system.database import Base

class AuditLog(Base):
    __tablename__ = 'audit_logs'
    log_id = Column(UUID(as_uuid=True), primary_key=True)
    organisation_id = Column(UUID(as_uuid=True), ForeignKey('organisations.organisation_id', ondelete='SET NULL'))
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id', ondelete='SET NULL'))
    action = Column(String(200), nullable=False)
    entity = Column(String(100))
    entity_id = Column(UUID(as_uuid=True))
    ip_address = Column(String(45))
    user_agent = Column(Text)
    details = Column(JSONB)
    occurred_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
