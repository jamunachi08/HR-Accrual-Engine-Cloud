import frappe
from frappe.utils import getdate

def create_accrual_jv(company, posting_date, component, employee, amount, cost_center=None, reference_doctype="Employee"):
    if amount <= 0:
        return None

    posting_date = getdate(posting_date)

    jv = frappe.new_doc("Journal Entry")
    jv.voucher_type = "Journal Entry"
    jv.company = company
    jv.posting_date = posting_date
    jv.user_remark = f"Auto accrual: {component.name} for {employee.name} ({posting_date})"

    # Debit
    jv.append("accounts", {
        "account": component.debit_account,
        "debit_in_account_currency": amount,
        "cost_center": cost_center,
        "party_type": "Employee",
        "party": employee.name,
        "reference_type": reference_doctype,
        "reference_name": employee.name,
    })

    # Credit
    jv.append("accounts", {
        "account": component.credit_account,
        "credit_in_account_currency": amount,
        "cost_center": cost_center,
        "party_type": "Employee",
        "party": employee.name,
        "reference_type": reference_doctype,
        "reference_name": employee.name,
    })

    jv.insert(ignore_permissions=True)
    jv.submit()
    return jv.name
