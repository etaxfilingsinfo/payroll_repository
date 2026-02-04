# payroll_system/schemas/enums.py
from enum import Enum

class PayrollStatus(str, Enum):
    open = "open"
    closed = "closed"

class RunStatus(str, Enum):
    draft = "draft"
    processed = "processed"
    approved = "approved"
    locked = "locked"

class ComponentType(str, Enum):
    earning = "earning"
    deduction = "deduction"
    benefit = "benefit"
    reimbursement = "reimbursement"

class CalcType(str, Enum):
    fixed = "fixed"
    percentage = "percentage"

class UserStatus(str, Enum):
    active = "active"
    inactive = "inactive"
    suspended = "suspended"

class EmployeeStatus(str, Enum):
    active = "active"
    terminated = "terminated"
    resigned = "resigned"
    on_leave = "on_leave"
