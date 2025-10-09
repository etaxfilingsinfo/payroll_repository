from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import date, datetime

# ---------------------------
# Organisation Schemas
# ---------------------------
class OrganisationCreate(BaseModel):
    org_name: str
    org_type: Optional[str] = None
    branch_name: Optional[str] = None
    address: Optional[str] = None
    contact_number: Optional[str] = None
    email: Optional[EmailStr] = None


class OrganisationOut(OrganisationCreate):
    org_id: int

    model_config = ConfigDict(from_attributes=True)


# ---------------------------
# Department Schemas
# ---------------------------
class DepartmentCreate(BaseModel):
    org_id: int
    dept_name: str
    description: Optional[str] = None


class DepartmentOut(DepartmentCreate):
    dept_id: int

    model_config = ConfigDict(from_attributes=True)


# ---------------------------
# Designation Schemas
# ---------------------------
class DesignationCreate(BaseModel):
    dept_id: int
    title: str
    description: Optional[str] = None


class DesignationOut(DesignationCreate):
    designation_id: int

    model_config = ConfigDict(from_attributes=True)


# ---------------------------
# Employee Schemas
# ---------------------------
class EmployeeCreate(BaseModel):
    first_name: str
    last_name: Optional[str] = None
    email: EmailStr
    phone: Optional[str] = None
    date_of_joining: Optional[date] = None
    department_id: Optional[int] = None
    designation_id: Optional[int] = None


class EmployeeOut(EmployeeCreate):
    employee_id: int

    model_config = ConfigDict(from_attributes=True)


# ---------------------------
# Payroll Schemas
# ---------------------------
class PayrollCreate(BaseModel):
    employee_id: int
    pay_period: str
    gross_salary: float
    total_deductions: float
    net_salary: float


class PayrollOut(PayrollCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)

# ---------------------------
# User Schemas
# ---------------------------
class UserBase(BaseModel):
    username: str
    email: EmailStr
    org_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    created_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    username: str
    password: str