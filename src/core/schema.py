"""
Core schema definitions, data types, and validation rules for LendingClub credit records.
"""

from typing import Dict, List, Any, Optional

FEATURE_COLUMNS = [
    "loan_amnt",
    "annual_inc",
    "dti",
    "fico_range_low",
    "fico_range_high",
    "int_rate",
    "installment",
    "open_acc",
    "total_acc",
    "revol_bal",
    "revol_util",
    "inq_last_6mths",
    "delinq_2yrs",
    "pub_rec"
]

CATEGORICAL_COLUMNS = [
    "term",
    "grade",
    "sub_grade",
    "emp_length",
    "home_ownership",
    "verification_status",
    "purpose",
    "addr_state",
    "application_type"
]

TARGET_COLUMN = "loan_status"

DEFAULT_STATUSES = {
    "Charged Off": 1,
    "Default": 1,
    "Late (31-120 days)": 1,
    "Late (16-30 days)": 1,
    "Does not meet the credit policy. Status:Charged Off": 1,
    "Fully Paid": 0,
    "Current": 0,
    "In Grace Period": 0,
    "Does not meet the credit policy. Status:Fully Paid": 0
}

def clean_float(val: Any, default: float = 0.0) -> float:
    if val is None:
        return default
    if isinstance(val, (int, float)):
        return float(val)
    s = str(val).strip().replace("$", "").replace("%", "").replace(",", "")
    if not s or s.lower() == "nan" or s.lower() == "none" or s == "":
        return default
    try:
        return float(s)
    except ValueError:
        return default

def clean_emp_length(val: Any) -> float:
    if not val:
        return 0.0
    s = str(val).strip()
    if "<" in s:
        return 0.5
    digits = "".join(c for c in s if c.isdigit())
    if digits:
        return float(digits)
    return 0.0
