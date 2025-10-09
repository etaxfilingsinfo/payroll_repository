from sqlalchemy import Column, Integer, String, Date, ForeignKey, Numeric, Text, TIMESTAMP, func
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# ---------------------------
# 1. Organisation
# ---------------------------
class Organisation(Base):
    __tablename__ = "organisations"

    org_id = Column(Integer, primary_key=True, index=True)
    org_name = Column(String(100), nullable=False)
    org_type = Column(String(50))
    branch_name = Column(String(100))
    address = Column(Text)
    contact_number = Column(String(20))
    email = Column(String(100))
    created_at = Column(TIMESTAMP, server_default=func.now())

    departments = relationship("Department", back_populates="organisation")
    users = relationship("User", back_populates="organisation")


# ---------------------------
# 2. Department
# ---------------------------
class Department(Base):
    __tablename__ = "departments"

    dept_id = Column(Integer, primary_key=True, index=True)
    org_id = Column(Integer, ForeignKey("organisations.org_id"))
    dept_name = Column(String(100), nullable=False)
    description = Column(Text)

    organisation = relationship("Organisation", back_populates="departments")
    designations = relationship("Designation", back_populates="department")
    employees = relationship("Employee", back_populates="department")


# ---------------------------
# 3. Designation
# ---------------------------
class Designation(Base):
    __tablename__ = "designations"

    designation_id = Column(Integer, primary_key=True, index=True)
    dept_id = Column(Integer, ForeignKey("departments.dept_id"))
    title = Column(String(100), nullable=False)
    description = Column(Text)

    department = relationship("Department", back_populates="designations")
    employees = relationship("Employee", back_populates="designation")


# ---------------------------
# 4. Employee
# ---------------------------
class Employee(Base):
    __tablename__ = "employees"

    employee_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50))
    email = Column(String(100), unique=True, index=True)
    phone = Column(String(20))
    date_of_joining = Column(Date)
    department_id = Column(Integer, ForeignKey("departments.dept_id"))
    designation_id = Column(Integer, ForeignKey("designations.designation_id"))

    department = relationship("Department", back_populates="employees")
    designation = relationship("Designation", back_populates="employees")
    payrolls = relationship("Payroll", back_populates="employee")


# ---------------------------
# 5. Payroll
# ---------------------------
class Payroll(Base):
    __tablename__ = "payroll_records"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.employee_id"), nullable=False)
    pay_period = Column(String(20), nullable=False)  # e.g., "2025-10"
    gross_salary = Column(Numeric(10, 2))
    total_deductions = Column(Numeric(10, 2))
    net_salary = Column(Numeric(10, 2))
    created_at = Column(TIMESTAMP, server_default=func.now())

    employee = relationship("Employee", back_populates="payrolls")


    # ---------------------------
# 6. User (Authentication)
# ---------------------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(128), nullable=True)   # nullable for OAuth-only accounts
    google_id = Column(String(128), nullable=True)
    org_id = Column(Integer, ForeignKey("organisations.org_id"), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    organisation = relationship("Organisation", back_populates="users")
