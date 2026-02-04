from sqlalchemy import Column, String, Text, Boolean, DateTime, Date, SmallInteger, ForeignKey, Numeric, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy.sql import func
from payroll_system.database import Base

loan_status = ENUM('Pending', 'Active', 'Completed', 'Cancelled', 'Rejected', name='loan_status_t')

class LoanType(Base):
    __tablename__ = 'loan_types'
    loan_type_id = Column(UUID(as_uuid=True), primary_key=True)
    organisation_id = Column(UUID(as_uuid=True), ForeignKey('organisations.organisation_id', ondelete='CASCADE'), nullable=False)
    name = Column(String(100), nullable=False)
    max_amount = Column(Numeric(18, 2))
    max_installments = Column(SmallInteger)
    interest_rate = Column(Numeric(6, 3), default=0)
    is_interest_applicable = Column(Boolean, default=False, nullable=False)
    is_salary_advance = Column(Boolean, default=False, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    __table_args__ = (UniqueConstraint('organisation_id', 'name', name='uq_loan_type_org_name'),)


class LoanRequest(Base):
    __tablename__ = 'loan_requests'
    request_id = Column(UUID(as_uuid=True), primary_key=True)
    organisation_id = Column(UUID(as_uuid=True), ForeignKey('organisations.organisation_id', ondelete='CASCADE'), nullable=False)
    employee_id = Column(UUID(as_uuid=True), ForeignKey('employees.employee_id', ondelete='CASCADE'), nullable=False)
    loan_type_id = Column(UUID(as_uuid=True), ForeignKey('loan_types.loan_type_id', ondelete='RESTRICT'), nullable=False)
    requested_amount = Column(Numeric(18, 2), nullable=False)
    requested_installments = Column(SmallInteger, nullable=False)
    purpose = Column(Text)
    status = Column(String(50), default='Pending')
    reviewed_by = Column(UUID(as_uuid=True), ForeignKey('users.user_id', ondelete='SET NULL'))
    reviewed_at = Column(DateTime(timezone=True))
    remarks = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class EmployeeLoan(Base):
    __tablename__ = 'employee_loans'
    loan_id = Column(UUID(as_uuid=True), primary_key=True)
    organisation_id = Column(UUID(as_uuid=True), ForeignKey('organisations.organisation_id', ondelete='CASCADE'), nullable=False)
    employee_id = Column(UUID(as_uuid=True), ForeignKey('employees.employee_id', ondelete='CASCADE'), nullable=False)
    loan_type_id = Column(UUID(as_uuid=True), ForeignKey('loan_types.loan_type_id', ondelete='RESTRICT'), nullable=False)
    principal_amount = Column(Numeric(18, 2), nullable=False)
    interest_rate = Column(Numeric(6, 3), default=0)
    total_amount = Column(Numeric(18, 2))
    installment_amount = Column(Numeric(18, 2))
    total_installments = Column(SmallInteger, nullable=False)
    installments_paid = Column(SmallInteger, default=0)
    start_month = Column(Date, nullable=False)
    end_month = Column(Date)
    status = Column(loan_status, default='Active')
    approved_by = Column(UUID(as_uuid=True), ForeignKey('users.user_id', ondelete='SET NULL'))
    approved_at = Column(DateTime(timezone=True))
    remarks = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    __table_args__ = (UniqueConstraint('employee_id', 'loan_type_id', 'start_month', name='uq_loan_employee_type_month'),)


class LoanInstallment(Base):
    __tablename__ = 'loan_installments'
    installment_id = Column(UUID(as_uuid=True), primary_key=True)
    loan_id = Column(UUID(as_uuid=True), ForeignKey('employee_loans.loan_id', ondelete='CASCADE'), nullable=False)
    installment_no = Column(SmallInteger, nullable=False)
    due_date = Column(Date, nullable=False)
    amount = Column(Numeric(18, 2), nullable=False)
    interest_component = Column(Numeric(18, 2), default=0)
    principal_component = Column(Numeric(18, 2), default=0)
    paid = Column(Boolean, default=False, nullable=False)
    paid_on = Column(DateTime(timezone=True))
    remarks = Column(Text)
    __table_args__ = (UniqueConstraint('loan_id', 'installment_no', name='uq_loan_installment_no'),)
