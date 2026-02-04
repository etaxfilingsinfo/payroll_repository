from sqlalchemy import Column, String, Boolean, Date, DateTime, ForeignKey, Integer, Numeric, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB, ENUM
from sqlalchemy.sql import func
from payroll_system.database import Base

bank_file_type = ENUM('CSV', 'TXT', 'XML', name='bank_file_type_t')
payment_status = ENUM('Generated', 'Uploaded', 'Rejected', 'Paid', name='payment_status_t')

class EmployeeBankDetail(Base):
    __tablename__ = 'employee_bank_details'
    bank_detail_id = Column(UUID(as_uuid=True), primary_key=True)
    employee_id = Column(UUID(as_uuid=True), ForeignKey('employees.employee_id', ondelete='CASCADE'), nullable=False)
    bank_name = Column(String(100), nullable=False)
    account_number = Column(String(50), nullable=False)
    ifsc_code = Column(String(20), nullable=False)
    is_primary = Column(Boolean, default=True, nullable=False)
    effective_from = Column(Date, nullable=False)
    effective_to = Column(Date)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    __table_args__ = (
        UniqueConstraint('employee_id', 'effective_from', name='uq_bank_employee_from'),
    )


class BankFileFormat(Base):
    __tablename__ = 'bank_file_formats'
    format_id = Column(UUID(as_uuid=True), primary_key=True)
    organisation_id = Column(UUID(as_uuid=True), ForeignKey('organisations.organisation_id', ondelete='CASCADE'), nullable=False)
    bank_code = Column(String(20), nullable=False)
    bank_name = Column(String(150))
    branch_code = Column(String(50))
    name = Column(String(150), nullable=False)
    file_type = Column(bank_file_type, nullable=False)
    header_line = Column(Text)
    data_line_config = Column(JSONB)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    __table_args__ = (
        UniqueConstraint('organisation_id', 'bank_code', 'name', name='uq_bank_format'),
    )


class PaymentBatch(Base):
    __tablename__ = 'payment_batches'
    batch_id = Column(UUID(as_uuid=True), primary_key=True)
    payroll_run_id = Column(UUID(as_uuid=True), ForeignKey('payroll_runs.payroll_run_id', ondelete='CASCADE'), nullable=False)
    format_id = Column(UUID(as_uuid=True), ForeignKey('bank_file_formats.format_id', ondelete='RESTRICT'), nullable=False)
    file_name = Column(Text, nullable=False)
    upload_path = Column(Text)
    total_employees = Column(Integer, nullable=False)
    total_amount = Column(Numeric(18, 4), nullable=False)
    status = Column(payment_status, default='Generated', nullable=False)
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey('users.user_id', ondelete='SET NULL'))
    paid_at = Column(DateTime(timezone=True))
    transaction_ref = Column(Text)
    rejection_reason = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    __table_args__ = (
        UniqueConstraint('payroll_run_id', 'format_id', name='uq_payment_batch_run_format'),
    )
