# payroll_system/crud/payroll_crud.py

from typing import Optional
from uuid import UUID
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from payroll_system.models.payroll_models import PayPeriod, PayrollRun, PayrollEntry
from payroll_system.models.employee_models import Employee
from payroll_system.models.salary_models import SalaryComponent
from payroll_system.schemas.payroll_schemas import (
    PayPeriodCreate, PayrollCreate, PayrollEntryCreate
)

# ============================================================
# PAY PERIOD CRUD
# ============================================================

async def create_pay_period(db: AsyncSession, payload: PayPeriodCreate) -> PayPeriod:
    """Create a new pay period ensuring no overlap within the same organisation."""
    q = await db.execute(
        select(PayPeriod).filter(
            PayPeriod.organisation_id == payload.organisation_id,
            PayPeriod.start_date <= payload.end_date,
            PayPeriod.end_date >= payload.start_date
        )
    )
    if q.scalar_one_or_none():
        raise ValueError("Overlapping pay period exists for this organisation")

    pay_period = PayPeriod(**payload.model_dump())
    try:
        db.add(pay_period)
        await db.commit()
        await db.refresh(pay_period)
        return pay_period
    except IntegrityError:
        await db.rollback()
        raise ValueError("Failed to create pay period")

async def get_pay_period(db: AsyncSession, pay_period_id: UUID) -> Optional[PayPeriod]:
    """Retrieve a pay period by ID."""
    q = await db.execute(select(PayPeriod).filter(PayPeriod.pay_period_id == pay_period_id))
    return q.scalar_one_or_none()

# ============================================================
# PAYROLL RUN (Header)
# ============================================================

async def create_payroll(db: AsyncSession, payload: PayrollCreate) -> PayrollRun:
    """Create a new payroll run for a given pay period."""
    pay_period = await get_pay_period(db, payload.pay_period_id)
    if not pay_period:
        raise ValueError("Pay period not found")
    if pay_period.status != "open":
        raise ValueError("Pay period is not open")

    payroll = PayrollRun(**payload.model_dump())
    try:
        db.add(payroll)
        await db.commit()
        await db.refresh(payroll)
        return payroll
    except IntegrityError:
        await db.rollback()
        raise ValueError("Failed to create payroll run")

async def get_payroll_by_id(db: AsyncSession, payroll_run_id: UUID) -> Optional[PayrollRun]:
    """Retrieve a payroll run by ID."""
    q = await db.execute(select(PayrollRun).filter(PayrollRun.payroll_run_id == payroll_run_id))
    return q.scalar_one_or_none()

# ============================================================
# PAYROLL ENTRIES (Detail)
# ============================================================

async def add_payroll_entry(db: AsyncSession, payload: PayrollEntryCreate) -> PayrollEntry:
    """Add an individual payroll entry (per employee, per component)."""
    # Validate payroll run exists
    payroll = await get_payroll_by_id(db, payload.payroll_run_id)
    if not payroll:
        raise ValueError("Payroll run not found")

    # Validate pay period match
    if payroll.pay_period_id != payload.pay_period_id:
        raise ValueError("Pay period mismatch with payroll run")

    # Validate employee exists and is active
    q_emp = await db.execute(select(Employee).filter(Employee.employee_id == payload.employee_id))
    employee = q_emp.scalar_one_or_none()
    if not employee:
        raise ValueError("Employee not found")
    if not employee.is_active:
        raise ValueError("Employee is inactive")

    # Validate component exists and is active
    q_comp = await db.execute(select(SalaryComponent).filter(SalaryComponent.component_id == payload.component_id))
    component = q_comp.scalar_one_or_none()
    if not component or not component.is_active:
        raise ValueError("Salary component not found or inactive")

    entry = PayrollEntry(**payload.model_dump())
    try:
        db.add(entry)
        await db.commit()
        await db.refresh(entry)
        return entry
    except IntegrityError:
        await db.rollback()
        raise ValueError("Failed to add payroll entry (possibly duplicate)")

# ============================================================
# PAYROLL SUMMARY (Utility)
# ============================================================

async def get_payroll_summary(db: AsyncSession, payroll_run_id: UUID) -> dict:
    """Compute a summary of payroll totals grouped by earnings and deductions."""
    q = await db.execute(select(PayrollEntry).filter(PayrollEntry.payroll_run_id == payroll_run_id))
    entries = q.scalars().all()

    totals = {"earnings": Decimal("0.00"), "deductions": Decimal("0.00")}
    for e in entries:
        component = getattr(e, "component", None)
        ctype = getattr(component, "component_type", None)

        if ctype in ("earning", "benefit", "reimbursement"):
            totals["earnings"] += e.amount
        else:
            totals["deductions"] += e.amount

    totals["net"] = totals["earnings"] - totals["deductions"]
    return {"totals": totals, "entries": len(entries)}
