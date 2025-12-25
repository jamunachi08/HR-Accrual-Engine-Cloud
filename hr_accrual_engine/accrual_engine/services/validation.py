import frappe

def validate_component_accounts(component):
    if not component.debit_account or not component.credit_account:
        frappe.throw(f"Debit/Credit accounts are required for Accrual Component: {component.name}")

def prevent_duplicate_run(company, posting_date):
    existing = frappe.get_all("Accrual Run", filters={"company": company, "posting_date": posting_date, "docstatus": ["!=", 2]}, pluck="name")
    if existing:
        frappe.throw(f"Accrual Run already exists for {company} on {posting_date}: {', '.join(existing)}")
