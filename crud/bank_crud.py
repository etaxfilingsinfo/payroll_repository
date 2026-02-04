# payroll_system/crud/bank_crud.py

from typing import Optional, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from payroll_system.models.bank_models import EmployeeBankDetail, BankFileFormat, PaymentBatch
from payroll_system.schemas.bank_schemas import (
    EmployeeBankDetailCreate, EmployeeBankDetailUpdate,
    BankFileFormatCreate, BankFileFormatUpdate,
    PaymentBatchCreate, PaymentBatchUpdate
)

# ============================================================
# EMPLOYEE BANK DETAILS
# ============================================================

async def create_employee_bank_detail(db: AsyncSession, payload: EmployeeBankDetailCreate) -> EmployeeBankDetail:
    bank_detail = EmployeeBankDetail(**payload.model_dump())
    try:
        db.add(bank_detail)
        await db.commit()
        await db.refresh(bank_detail)
        return bank_detail
    except IntegrityError:
        await db.rollback()
        raise ValueError("Employee bank detail creation failed (possible duplicate or constraint error)")

async def get_employee_bank_detail(db: AsyncSession, bank_detail_id: UUID) -> Optional[EmployeeBankDetail]:
    q = await db.execute(select(EmployeeBankDetail).filter(EmployeeBankDetail.bank_detail_id == bank_detail_id))
    return q.scalar_one_or_none()

async def update_employee_bank_detail(db: AsyncSession, bank_detail_id: UUID, payload: EmployeeBankDetailUpdate) -> Optional[EmployeeBankDetail]:
    bank_detail = await get_employee_bank_detail(db, bank_detail_id)
    if not bank_detail:
        return None
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(bank_detail, k, v)
    try:
        await db.commit()
        await db.refresh(bank_detail)
        return bank_detail
    except IntegrityError:
        await db.rollback()
        raise ValueError("Failed to update employee bank detail")

async def list_employee_bank_details(db: AsyncSession, employee_id: Optional[UUID] = None) -> List[EmployeeBankDetail]:
    q = select(EmployeeBankDetail)
    if employee_id:
        q = q.filter(EmployeeBankDetail.employee_id == employee_id)
    result = await db.execute(q)
    return result.scalars().all()

# ============================================================
# BANK FILE FORMATS
# ============================================================

async def create_bank_file_format(db: AsyncSession, payload: BankFileFormatCreate) -> BankFileFormat:
    file_format = BankFileFormat(**payload.model_dump())
    try:
        db.add(file_format)
        await db.commit()
        await db.refresh(file_format)
        return file_format
    except IntegrityError:
        await db.rollback()
        raise ValueError("Bank file format creation failed (duplicate or constraint error)")

async def get_bank_file_format(db: AsyncSession, format_id: UUID) -> Optional[BankFileFormat]:
    q = await db.execute(select(BankFileFormat).filter(BankFileFormat.format_id == format_id))
    return q.scalar_one_or_none()

async def update_bank_file_format(db: AsyncSession, format_id: UUID, payload: BankFileFormatUpdate) -> Optional[BankFileFormat]:
    file_format = await get_bank_file_format(db, format_id)
    if not file_format:
        return None
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(file_format, k, v)
    try:
        await db.commit()
        await db.refresh(file_format)
        return file_format
    except IntegrityError:
        await db.rollback()
        raise ValueError("Failed to update bank file format")

async def list_bank_file_formats(db: AsyncSession, organisation_id: Optional[UUID] = None) -> List[BankFileFormat]:
    q = select(BankFileFormat)
    if organisation_id:
        q = q.filter(BankFileFormat.organisation_id == organisation_id)
    result = await db.execute(q)
    return result.scalars().all()

# ============================================================
# PAYMENT BATCHES
# ============================================================

async def create_payment_batch(db: AsyncSession, payload: PaymentBatchCreate) -> PaymentBatch:
    batch = PaymentBatch(**payload.model_dump())
    try:
        db.add(batch)
        await db.commit()
        await db.refresh(batch)
        return batch
    except IntegrityError:
        await db.rollback()
        raise ValueError("Payment batch creation failed (duplicate or constraint error)")

async def get_payment_batch(db: AsyncSession, batch_id: UUID) -> Optional[PaymentBatch]:
    q = await db.execute(select(PaymentBatch).filter(PaymentBatch.batch_id == batch_id))
    return q.scalar_one_or_none()

async def update_payment_batch(db: AsyncSession, batch_id: UUID, payload: PaymentBatchUpdate) -> Optional[PaymentBatch]:
    batch = await get_payment_batch(db, batch_id)
    if not batch:
        return None
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(batch, k, v)
    try:
        await db.commit()
        await db.refresh(batch)
        return batch
    except IntegrityError:
        await db.rollback()
        raise ValueError("Failed to update payment batch")

async def list_payment_batches(db: AsyncSession, payroll_run_id: Optional[UUID] = None) -> List[PaymentBatch]:
    q = select(PaymentBatch)
    if payroll_run_id:
        q = q.filter(PaymentBatch.payroll_run_id == payroll_run_id)
    result = await db.execute(q)
    return result.scalars().all()
