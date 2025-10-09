from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import Organisation, Employee, Payroll, Department, Designation, User
from schemas import OrganisationCreate, EmployeeCreate, PayrollCreate, DepartmentCreate, DesignationCreate, UserCreate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# -----------------
# Organisation CRUD
# -----------------
async def create_organisation(db: AsyncSession, org: OrganisationCreate):
    db_org = Organisation(
        org_name=org.org_name,
        org_type=org.org_type,
        branch_name=org.branch_name,
        address=org.address,
        contact_number=org.contact_number,
        email=org.email,
    )
    db.add(db_org)
    await db.commit()
    await db.refresh(db_org)
    return db_org

async def get_organisation(db: AsyncSession, org_id: int):
    result = await db.execute(select(Organisation).filter(Organisation.org_id == org_id))
    return result.scalar_one_or_none()


# -----------------
# Department CRUD
# -----------------
async def create_department(db: AsyncSession, dept: DepartmentCreate):
    db_dept = Department(
        org_id=dept.org_id,
        dept_name=dept.dept_name,
        description=dept.description,
    )
    db.add(db_dept)
    await db.commit()
    await db.refresh(db_dept)
    return db_dept

async def get_department(db: AsyncSession, dept_id: int):
    result = await db.execute(select(Department).filter(Department.dept_id == dept_id))
    return result.scalar_one_or_none()


# -----------------
# Designation CRUD
# -----------------
async def create_designation(db: AsyncSession, desig: DesignationCreate):
    db_desig = Designation(
        dept_id=desig.dept_id,
        title=desig.title,
        description=desig.description,
    )
    db.add(db_desig)
    await db.commit()
    await db.refresh(db_desig)
    return db_desig

async def get_designation(db: AsyncSession, desig_id: int):
    result = await db.execute(select(Designation).filter(Designation.designation_id == desig_id))
    return result.scalar_one_or_none()


# -----------------
# Employee CRUD
# -----------------
async def create_employee(db: AsyncSession, emp: EmployeeCreate):
    db_emp = Employee(
        first_name=emp.first_name,
        last_name=emp.last_name,
        email=emp.email,
        phone=emp.phone,
        date_of_joining=emp.date_of_joining,
        department_id=emp.department_id,
        designation_id=emp.designation_id,
    )
    db.add(db_emp)
    await db.commit()
    await db.refresh(db_emp)
    return db_emp

async def get_employee(db: AsyncSession, emp_id: int):
    result = await db.execute(select(Employee).filter(Employee.employee_id == emp_id))
    return result.scalar_one_or_none()


# -----------------
# Payroll CRUD
# -----------------
async def create_payroll_record(db: AsyncSession, payroll: PayrollCreate):
    db_payroll = Payroll(
        employee_id=payroll.employee_id,
        pay_period=payroll.pay_period,
        gross_salary=payroll.gross_salary,
        total_deductions=payroll.total_deductions,
        net_salary=payroll.net_salary,
    )
    db.add(db_payroll)
    await db.commit()
    await db.refresh(db_payroll)
    return db_payroll

async def get_payroll_record(db: AsyncSession, record_id: int):
    result = await db.execute(select(Payroll).filter(Payroll.id == record_id))
    return result.scalar_one_or_none()


# -----------------
# User CRUD (hashed password)
# -----------------
async def create_user(db: AsyncSession, user: UserCreate):
    hashed_password = pwd_context.hash(user.password)  # hash password here
    db_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password,  # store hashed password
        org_id=user.org_id,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalar_one_or_none()

async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(User).filter(User.username == username))
    return result.scalar_one_or_none()

async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user_by_username(db, username)
    if not user:
        return False
    if not pwd_context.verify(password, user.password):  # verify hashed password
        return False
    return user
