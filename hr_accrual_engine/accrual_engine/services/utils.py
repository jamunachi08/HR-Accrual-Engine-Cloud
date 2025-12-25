import frappe
from frappe.utils import flt, getdate
from frappe.safe_eval import safe_eval

def get_settings():
    return frappe.get_single("Accrual Settings")

def months_between(from_date, to_date):
    """Return service months (integer) between two dates."""
    from_date = getdate(from_date)
    to_date = getdate(to_date)
    return (to_date.year - from_date.year) * 12 + (to_date.month - from_date.month) + 1

def eval_formula(formula: str, context: dict):
    if not formula:
        frappe.throw("Formula is empty in Accrual Settings.")
    return safe_eval(formula, None, context)

def round_amt(amount, precision):
    return flt(amount, precision)
