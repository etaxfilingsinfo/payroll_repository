# payroll_system/crud/loan_crud.py

from typing import Optional, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from payroll_system.models.loan_models import LoanType, LoanRequest, EmployeeLoan, LoanInstallment
from payroll_system.schemas.loan_schemas import (
    LoanTypeCreate, LoanTypeUpdate,
    LoanRequestCreate, LoanRequestUpdate,
    EmployeeLoanCreate, EmployeeLoanUpdate,
    LoanInstallmentCreate, LoanInstallmentUpdate
)

# ============================================================
# LOAN TYPES
# ============================================================

async def create_loan_type(db: AsyncSession, payload: LoanTypeCreate) -> LoanType:
    loan_type = LoanType(**payload.model_dump())
    try:
        db.add(loan_type)
        await db.commit()
        await db.refresh(loan_type)
        return loan_type
    except IntegrityError:
        await db.rollback()
        raise ValueError("Loan type creation failed (possible duplicate or constraint error)")

async def get_loan_type(db: AsyncSession, loan_type_id: UUID) -> Optional[LoanType]:
    q = await db.execute(select(LoanType).filter(LoanType.loan_type_id == loan_type_id))
    return q.scalar_one_or_none()

async def update_loan_type(db: AsyncSession, loan_type_id: UUID, payload: LoanTypeUpdate) -> Optional[LoanType]:
    loan_type = await get_loan_type(db, loan_type_id)
    if not loan_type:
        return None
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(loan_type, k, v)
    try:
        await db.commit()
        await db.refresh(loan_type)
        return loan_type
    except IntegrityError:
        await db.rollback()
        raise ValueError("Failed to update loan type")

async def list_loan_types(db: AsyncSession, organisation_id: Optional[UUID] = None) -> List[LoanType]:
    q = select(LoanType)
    if organisation_id:
        q = q.filter(LoanType.organisation_id == organisation_id)
    result = await db.execute(q)
    return result.scalars().all()

# ============================================================
# LOAN REQUESTS
# ============================================================

async def create_loan_request(db: AsyncSession, payload: LoanRequestCreate) -> LoanRequest:
    loan_request = LoanRequest(**payload.model_dump())
    try:
        db.add(loan_request)
        await db.commit()
        await db.refresh(loan_request)
        return loan_request
    except IntegrityError:
        await db.rollback()
        raise ValueError("Loan request creation failed")

async def get_loan_request(db: AsyncSession, request_id: UUID) -> Optional[LoanRequest]:
    q = await db.execute(select(LoanRequest).filter(LoanRequest.request_id == request_id))
    return q.scalar_one_or_none()

async def update_loan_request(db: AsyncSession, request_id: UUID, payload: LoanRequestUpdate) -> Optional[LoanRequest]:
    loan_request = await get_loan_request(db, request_id)
    if not loan_request:
        return None
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(loan_request, k, v)
    try:
        await db.commit()
        await db.refresh(loan_request)
        return loan_request
    except IntegrityError:
        await db.rollback()
        raise ValueError("Failed to update loan request")

async def list_loan_requests(db: AsyncSession, organisation_id: Optional[UUID] = None) -> List[LoanRequest]:
    q = select(LoanRequest)
    if organisation_id:
        q = q.filter(LoanRequest.organisation_id == organisation_id)
    result = await db.execute(q)
    return result.scalars().all()

# ============================================================
# EMPLOYEE LOANS
# ============================================================

async def create_employee_loan(db: AsyncSession, payload: EmployeeLoanCreate) -> EmployeeLoan:
    emp_loan = EmployeeLoan(**payload.model_dump())
    try:
        db.add(emp_loan)
        await db.commit()
        await db.refresh(emp_loan)
        return emp_loan
    except IntegrityError:
        await db.rollback()
        raise ValueError("Employee loan creation failed")

async def get_employee_loan(db: AsyncSession, loan_id: UUID) -> Optional[EmployeeLoan]:
    q = await db.execute(select(EmployeeLoan).filter(EmployeeLoan.loan_id == loan_id))
    return q.scalar_one_or_none()

async def update_employee_loan(db: AsyncSession, loan_id: UUID, payload: EmployeeLoanUpdate) -> Optional[EmployeeLoan]:
    emp_loan = await get_employee_loan(db, loan_id)
    if not emp_loan:
        return None
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(emp_loan, k, v)
    try:
        await db.commit()
        await db.refresh(emp_loan)
        return emp_loan
    except IntegrityError:
        await db.rollback()
        raise ValueError("Failed to update employee loan")

async def list_employee_loans(db: AsyncSession, employee_id: Optional[UUID] = None) -> List[EmployeeLoan]:
    q = select(EmployeeLoan)
    if employee_id:
        q = q.filter(EmployeeLoan.employee_id == employee_id)
    result = await db.execute(q)
    return result.scalars().all()

# ============================================================
# LOAN INSTALLMENTS
# ============================================================

async def create_loan_installment(db: AsyncSession, payload: LoanInstallmentCreate) -> LoanInstallment:
    installment = LoanInstallment(**payload.model_dump())
    try:
        db.add(installment)
        await db.commit()
        await db.refresh(installment)
        return installment
    except IntegrityError:
        await db.rollback()
        raise ValueError("Loan installment creation failed")

async def get_loan_installment(db: AsyncSession, installment_id: UUID) -> Optional[LoanInstallment]:
    q = await db.execute(select(LoanInstallment).filter(LoanInstallment.installment_id == installment_id))
    return q.scalar_one_or_none()

async def update_loan_installment(db: AsyncSession, installment_id: UUID, payload: LoanInstallmentUpdate) -> Optional[LoanInstallment]:
    installment = await get_loan_installment(db, installment_id)
    if not installment:
        return None
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(installment, k, v)
    try:
        await db.commit()
        await db.refresh(installment)
        return installment
    except IntegrityError:
        await db.rollback()
        raise ValueError("Failed to update loan installment")

async def list_loan_installments(db: AsyncSession, loan_id: Optional[UUID] = None) -> List[LoanInstallment]:
    q = select(LoanInstallment)
    if loan_id:
        q = q.filter(LoanInstallment.loan_id == loan_id)
    result = await db.execute(q)
    return result.scalars().all()
