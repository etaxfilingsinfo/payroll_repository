# payroll_system/schemas/payroll_schemas.py

from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID
from datetime import date, datetime
from decimal import Decimal


# ============================================================
# PAY PERIOD SCHEMAS
# ============================================================

class PayPeriodBase(BaseModel):
    organisation_id: UUID
    start_date: date
    end_date: date
    status: Optional[str] = "open"  # 'open' or 'closed'


class PayPeriodCreate(PayPeriodBase):
    pass


class PayPeriodUpdate(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[str] = None


class PayPeriodOut(PayPeriodBase):
    pay_period_id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ============================================================
# PAYROLL RUN SCHEMAS
# ============================================================

class PayrollRunBase(BaseModel):
    organisation_id: UUID
    pay_period_id: UUID
    processed_by: Optional[UUID] = None
    processed_at: Optional[datetime] = None
    status: Optional[str] = "draft"  # 'draft', 'processed', 'approved', 'locked'
    notes: Optional[str] = None
    net_pay_total: Optional[Decimal] = Decimal("0.00")
    gross_pay_total: Optional[Decimal] = Decimal("0.00")


class PayrollRunCreate(PayrollRunBase):
    pass


class PayrollRunUpdate(BaseModel):
    processed_by: Optional[UUID] = None
    processed_at: Optional[datetime] = None
    status: Optional[str] = None
    notes: Optional[str] = None
    net_pay_total: Optional[Decimal] = None
    gross_pay_total: Optional[Decimal] = None


class PayrollRunOut(PayrollRunBase):
    payroll_run_id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ============================================================
# PAYROLL ENTRY SCHEMAS
# ============================================================

class PayrollEntryBase(BaseModel):
    payroll_run_id: UUID
    employee_id: UUID
    component_id: UUID
    pay_period_id: UUID
    amount: Decimal
    currency_code: Optional[str] = "INR"
    is_adhoc: Optional[bool] = False
    source_type: Optional[str] = "SalaryStructure"
    loan_installment_id: Optional[UUID] = None
    meta: Optional[dict] = None


class PayrollEntryCreate(PayrollEntryBase):
    pass


class PayrollEntryUpdate(BaseModel):
    amount: Optional[Decimal] = None
    currency_code: Optional[str] = None
    is_adhoc: Optional[bool] = None
    source_type: Optional[str] = None
    loan_installment_id: Optional[UUID] = None
    meta: Optional[dict] = None


class PayrollEntryOut(PayrollEntryBase):
    payroll_entry_id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
