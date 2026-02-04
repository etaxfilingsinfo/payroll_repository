from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..dependencies import get_db
from ..crud import bank as bank_crud
from ..schemas import bank as bank_schemas

router = APIRouter(prefix="/banks", tags=["banks"])


@router.post("/", response_model=bank_schemas.Bank, status_code=status.HTTP_201_CREATED)
def create_bank(bank_in: bank_schemas.BankCreate, db: Session = Depends(get_db)):
    """
    Create a new bank record.
    """
    try:
        bank = bank_crud.create(db=db, obj_in=bank_in)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    return bank


@router.get("/", response_model=List[bank_schemas.Bank])
def list_banks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    List banks with pagination.
    """
    return bank_crud.get_multi(db=db, skip=skip, limit=limit)


@router.get("/{bank_id}", response_model=bank_schemas.Bank)
def get_bank(bank_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single bank by ID.
    """
    bank = bank_crud.get(db=db, id=bank_id)
    if not bank:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bank not found")
    return bank


@router.put("/{bank_id}", response_model=bank_schemas.Bank)
def update_bank(bank_id: int, bank_in: bank_schemas.BankUpdate, db: Session = Depends(get_db)):
    """
    Update an existing bank.
    """
    bank = bank_crud.get(db=db, id=bank_id)
    if not bank:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bank not found")
    try:
        updated = bank_crud.update(db=db, db_obj=bank, obj_in=bank_in)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    return updated


@router.delete("/{bank_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bank(bank_id: int, db: Session = Depends(get_db)):
    """
    Delete a bank.
    """
    bank = bank_crud.get(db=db, id=bank_id)
    if not bank:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bank not found")
    bank_crud.remove(db=db, id=bank_id)
    return None