# payroll_system/schemas/statutory_schemas.py

from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID
from datetime import date, datetime
from decimal import Decimal

# ------------------------------------------------------------
# Statutory Settings
# ------------------------------------------------------------
class StatutorySettingCreate(BaseModel):
    organisation_id: UUID
    statutory_type: str
    registration_no: Optional[str] = None
    employer_contribution: Optional[Decimal] = None
    employee_contribution: Optional[Decimal] = None
    additional_info: Optional[dict] = None
    remarks: Optional[str] = None
    effective_from: date
    effective_to: Optional[date] = None

class StatutorySettingUpdate(BaseModel):
    registration_no: Optional[str] = None
    employer_contribution: Optional[Decimal] = None
    employee_contribution: Optional[Decimal] = None
    additional_info: Optional[dict] = None
    remarks: Optional[str] = None
    effective_from: Optional[date] = None
    effective_to: Optional[date] = None

class StatutorySettingOut(StatutorySettingCreate):
    statutory_id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# ------------------------------------------------------------
# Employee Statutory Details
# ------------------------------------------------------------
class EmployeeStatutoryDetailCreate(BaseModel):
    employee_id: UUID
    pan_number: Optional[str] = None
    uan_number: Optional[str] = None
    esi_number: Optional[str] = None
    pt_location: Optional[str] = None
    tax_regime: Optional[str] = "Old"
    is_active: Optional[bool] = True
    effective_from: date

class EmployeeStatutoryDetailUpdate(BaseModel):
    pan_number: Optional[str] = None
    uan_number: Optional[str] = None
    esi_number: Optional[str] = None
    pt_location: Optional[str] = None
    tax_regime: Optional[str] = None
    is_active: Optional[bool] = None
    effective_from: Optional[date] = None

class EmployeeStatutoryDetailOut(EmployeeStatutoryDetailCreate):
    stat_detail_id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# ------------------------------------------------------------
# Tax Declarations
# ------------------------------------------------------------
class TaxDeclarationCreate(BaseModel):
    employee_id: UUID
    financial_year: str
    section: str
    declared_amount: Decimal
    approved_amount: Optional[Decimal] = Decimal("0.00")
    status: Optional[str] = "Draft"
    submitted_at: Optional[datetime] = None
    approved_by: Optional[UUID] = None
    approved_at: Optional[datetime] = None

class TaxDeclarationUpdate(BaseModel):
    declared_amount: Optional[Decimal] = None
    approved_amount: Optional[Decimal] = None
    status: Optional[str] = None
    submitted_at: Optional[datetime] = None
    approved_by: Optional[UUID] = None
    approved_at: Optional[datetime] = None

class TaxDeclarationOut(TaxDeclarationCreate):
    declaration_id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# ------------------------------------------------------------
# Payroll Tax Summary (for reporting & compute)
# ------------------------------------------------------------
class PayrollTaxSummaryCreate(BaseModel):
    payroll_run_id: UUID
    employee_id: UUID
    tds_amount: Decimal = Decimal("0.00")
    employee_pf: Decimal = Decimal("0.00")
    employer_pf: Decimal = Decimal("0.00")
    professional_tax: Decimal = Decimal("0.00")
    employer_esi: Decimal = Decimal("0.00")
    employee_esi: Decimal = Decimal("0.00")
    notes: Optional[str] = None

class PayrollTaxSummaryOut(PayrollTaxSummaryCreate):
    tax_summary_id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
