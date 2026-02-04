# payroll_system/models/__init__.py
# Central import point for models package

from payroll_system.database import Base

# Core reference tables
from .org_models import Organisation, Department, Designation, WorkLocation

# Users, roles, and access control
from .user_models import User, Role, UserRole

# Employees and related
from .employee_models import (
    Employee,
    EmployeeDocument,
    EmployeeSalaryAssignment
)

# Salary templates and components
from .salary_models import (
    SalaryComponent,
    SalaryTemplate,
    SalaryTemplateComponent,
    PayStructure
)

# Payroll periods, runs, and entries
from .payroll_models import PayPeriod, PayrollRun, PayrollEntry

# Loans and salary advances
from .loan_models import LoanType, LoanRequest, EmployeeLoan, LoanInstallment

# Statutory, tax, and compliance
from .statutory_models import (
    StatutorySetting,
    EmployeeStatutoryDetail,
    TaxDeclaration,
    PayrollTaxSummary
)

# Bank and payment integration
from .bank_models import EmployeeBankDetail, BankFileFormat, PaymentBatch

# Attendance and leaves
from .attendance_models import Attendance, Leave

# Audit logs
from .audit_models import AuditLog


__all__ = [
    "Base",

    # Core reference
    "Organisation", "Department", "Designation", "WorkLocation",

    # Users and roles
    "User", "Role", "UserRole",

    # Employees
    "Employee", "EmployeeDocument", "EmployeeSalaryAssignment",

    # Salary
    "SalaryComponent", "SalaryTemplate", "SalaryTemplateComponent", "PayStructure",

    # Payroll
    "PayPeriod", "PayrollRun", "PayrollEntry",

    # Loans
    "LoanType", "LoanRequest", "EmployeeLoan", "LoanInstallment",

    # Statutory & Tax
    "StatutorySetting", "EmployeeStatutoryDetail", "TaxDeclaration", "PayrollTaxSummary",

    # Bank & Payment
    "EmployeeBankDetail", "BankFileFormat", "PaymentBatch",

    # Attendance & Leaves
    "Attendance", "Leave",

    # Audit Logs
    "AuditLog",
]
