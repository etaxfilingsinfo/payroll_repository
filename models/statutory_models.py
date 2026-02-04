import uuid
from sqlalchemy import (
    Column,
    String,
    TIMESTAMP,
    Date,
    UniqueConstraint,
    CheckConstraint,
    ForeignKey,
    Numeric,
    text,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID as PGUUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from payroll_system.database import Base  # Absolute import


class StatutorySetting(Base):
    __tablename__ = "statutory_settings"

    statutory_id = Column(PGUUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    organisation_id = Column(PGUUID(as_uuid=True), ForeignKey("organisations.organisation_id", ondelete="CASCADE"), nullable=False)
    statutory_type = Column(String(50), nullable=False)
    registration_no = Column(String(100))
    employer_contribution = Column(Numeric(5, 2))
    employee_contribution = Column(Numeric(5, 2))
    additional_info = Column(JSONB)
    effective_from = Column(Date, nullable=False)
    effective_to = Column(Date)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())

    __table_args__ = (
        UniqueConstraint("organisation_id", "statutory_type", "effective_from", name="ux_statutory_org_type_from"),
        CheckConstraint("employer_contribution >= 0 AND employer_contribution <= 100", name="chk_employer_contribution_range"),
        CheckConstraint("employee_contribution >= 0 AND employee_contribution <= 100", name="chk_employee_contribution_range"),
    )


class EmployeeStatutoryDetail(Base):
    __tablename__ = "employee_statutory_details"

    stat_detail_id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employee_id = Column(PGUUID(as_uuid=True), ForeignKey("employees.employee_id", ondelete="CASCADE"), nullable=False)
    pan_number = Column(String(20), unique=True)
    uan_number = Column(String(20))
    esi_number = Column(String(20))
    pt_location = Column(String(100))
    tax_regime = Column(String(50), default="Old")
    is_active = Column(String(5), nullable=False, default="True")
    effective_from = Column(Date, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())

    __table_args__ = (
        UniqueConstraint("employee_id", "effective_from", name="ux_employee_stat_effective_from"),
    )


class TaxDeclaration(Base):
    __tablename__ = "tax_declarations"

    declaration_id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employee_id = Column(PGUUID(as_uuid=True), ForeignKey("employees.employee_id", ondelete="CASCADE"), nullable=False)
    financial_year = Column(String(10), nullable=False)
    section = Column(String(50), nullable=False)
    declared_amount = Column(Numeric(18, 4), nullable=False)
    approved_amount = Column(Numeric(18, 4), default=0)
    status = Column(String(50), default="Draft")
    submitted_at = Column(TIMESTAMP(timezone=True))
    approved_by = Column(PGUUID(as_uuid=True), ForeignKey("users.user_id", ondelete="SET NULL"))
    approved_at = Column(TIMESTAMP(timezone=True))
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())


class PayrollTaxSummary(Base):
    __tablename__ = "payroll_tax_summaries"

    tax_summary_id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    payroll_run_id = Column(PGUUID(as_uuid=True), ForeignKey("payroll_runs.payroll_run_id", ondelete="CASCADE"), nullable=False)
    employee_id = Column(PGUUID(as_uuid=True), ForeignKey("employees.employee_id", ondelete="CASCADE"), nullable=False)
    tds_amount = Column(Numeric(18, 4), default=0, nullable=False)
    employee_pf = Column(Numeric(18, 4), default=0, nullable=False)
    employer_pf = Column(Numeric(18, 4), default=0, nullable=False)
    professional_tax = Column(Numeric(18, 4), default=0, nullable=False)
    employer_esi = Column(Numeric(18, 4), default=0, nullable=False)
    employee_esi = Column(Numeric(18, 4), default=0, nullable=False)
    notes = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())

    __table_args__ = (
        UniqueConstraint("payroll_run_id", "employee_id", name="ux_payroll_run_employee"),
    )
