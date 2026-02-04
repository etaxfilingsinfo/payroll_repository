# payroll_system/schemas/loan_schemas.py

from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID
from datetime import datetime, date
from decimal import Decimal

# ============================================================
# LOAN TYPE SCHEMAS
# ============================================================

class LoanTypeBase(BaseModel):
    organisation_id: UUID
    name: str
    max_amount: Optional[Decimal] = None
    max_installments: Optional[int] = None
    interest_rate: Optional[Decimal] = Decimal("0.000")
    is_interest_applicable: Optional[bool] = False
    is_salary_advance: Optional[bool] = False
    description: Optional[str] = None

class LoanTypeCreate(LoanTypeBase):
    pass

class LoanTypeUpdate(BaseModel):
    name: Optional[str] = None
    max_amount: Optional[Decimal] = None
    max_installments: Optional[int] = None
    interest_rate: Optional[Decimal] = None
    is_interest_applicable: Optional[bool] = None
    is_salary_advance: Optional[bool] = None
    description: Optional[str] = None

class LoanTypeOut(LoanTypeBase):
    loan_type_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

# ============================================================
# LOAN REQUEST SCHEMAS
# ============================================================

class LoanRequestBase(BaseModel):
    organisation_id: UUID
    employee_id: UUID
    loan_type_id: UUID
    requested_amount: Decimal
    requested_installments: int
    purpose: Optional[str] = None
    status: Optional[str] = "Pending"  # Pending, Active, Completed, Cancelled, Rejected
    reviewed_by: Optional[UUID] = None
    reviewed_at: Optional[datetime] = None
    remarks: Optional[str] = None

class LoanRequestCreate(LoanRequestBase):
    pass

class LoanRequestUpdate(BaseModel):
    status: Optional[str] = None
    reviewed_by: Optional[UUID] = None
    reviewed_at: Optional[datetime] = None
    remarks: Optional[str] = None

class LoanRequestOut(LoanRequestBase):
    request_id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# ============================================================
# EMPLOYEE LOAN SCHEMAS
# ============================================================

class EmployeeLoanBase(BaseModel):
    organisation_id: UUID
    employee_id: UUID
    loan_type_id: UUID
    principal_amount: Decimal
    interest_rate: Optional[Decimal] = Decimal("0.000")
    total_amount: Optional[Decimal] = None
    installment_amount: Optional[Decimal] = None
    total_installments: int
    installments_paid: Optional[int] = 0
    start_month: date
    end_month: Optional[date] = None
    status: Optional[str] = "Active"  # Pending, Active, Completed, Cancelled, Rejected
    approved_by: Optional[UUID] = None
    approved_at: Optional[datetime] = None
    remarks: Optional[str] = None

class EmployeeLoanCreate(EmployeeLoanBase):
    pass

class EmployeeLoanUpdate(BaseModel):
    status: Optional[str] = None
    installments_paid: Optional[int] = None
    approved_by: Optional[UUID] = None
    approved_at: Optional[datetime] = None
    remarks: Optional[str] = None

class EmployeeLoanOut(EmployeeLoanBase):
    loan_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

# ============================================================
# LOAN INSTALLMENT SCHEMAS
# ============================================================

class LoanInstallmentBase(BaseModel):
    loan_id: UUID
    installment_no: int
    due_date: date
    amount: Decimal
    interest_component: Optional[Decimal] = Decimal("0.00")
    principal_component: Optional[Decimal] = Decimal("0.00")
    paid: Optional[bool] = False
    paid_on: Optional[datetime] = None
    remarks: Optional[str] = None

class LoanInstallmentCreate(LoanInstallmentBase):
    pass

class LoanInstallmentUpdate(BaseModel):
    paid: Optional[bool] = None
    paid_on: Optional[datetime] = None
    remarks: Optional[str] = None

class LoanInstallmentOut(LoanInstallmentBase):
    installment_id: UUID

    model_config = ConfigDict(from_attributes=True)
