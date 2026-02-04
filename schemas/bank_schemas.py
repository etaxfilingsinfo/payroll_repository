# payroll_system/schemas/bank_schemas.py

from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID
from datetime import date, datetime
from decimal import Decimal

# ------------------------------------------------------------
# Employee Bank Details
# ------------------------------------------------------------

class EmployeeBankDetailCreate(BaseModel):
    employee_id: UUID
    bank_name: str
    account_number: str
    ifsc_code: str
    is_primary: Optional[bool] = True
    effective_from: date
    effective_to: Optional[date] = None

class EmployeeBankDetailUpdate(BaseModel):
    bank_name: Optional[str] = None
    account_number: Optional[str] = None
    ifsc_code: Optional[str] = None
    is_primary: Optional[bool] = None
    effective_from: Optional[date] = None
    effective_to: Optional[date] = None

class EmployeeBankDetailOut(EmployeeBankDetailCreate):
    bank_detail_id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# ------------------------------------------------------------
# Bank File Formats
# ------------------------------------------------------------

class BankFileFormatCreate(BaseModel):
    organisation_id: UUID
    bank_code: str
    name: str
    bank_name: Optional[str] = None
    branch_code: Optional[str] = None
    file_type: str  # CSV, TXT, XML
    header_line: Optional[str] = None
    data_line_config: Optional[dict] = None
    is_active: Optional[bool] = True

class BankFileFormatUpdate(BaseModel):
    bank_code: Optional[str] = None
    name: Optional[str] = None
    bank_name: Optional[str] = None
    branch_code: Optional[str] = None
    file_type: Optional[str] = None
    header_line: Optional[str] = None
    data_line_config: Optional[dict] = None
    is_active: Optional[bool] = None

class BankFileFormatOut(BankFileFormatCreate):
    format_id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# ------------------------------------------------------------
# Payment Batches
# ------------------------------------------------------------

class PaymentBatchCreate(BaseModel):
    payroll_run_id: UUID
    format_id: UUID
    file_name: str
    upload_path: Optional[str] = None
    total_employees: int
    total_amount: Decimal
    status: Optional[str] = "Generated"  # Generated, Uploaded, Rejected, Paid
    uploaded_by: Optional[UUID] = None
    paid_at: Optional[datetime] = None
    transaction_ref: Optional[str] = None
    rejection_reason: Optional[str] = None

class PaymentBatchUpdate(BaseModel):
    status: Optional[str] = None
    uploaded_by: Optional[UUID] = None
    paid_at: Optional[datetime] = None
    transaction_ref: Optional[str] = None
    rejection_reason: Optional[str] = None

class PaymentBatchOut(PaymentBatchCreate):
    batch_id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
