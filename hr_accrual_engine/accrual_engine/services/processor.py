import frappe
from frappe.utils import getdate, nowdate

from hr_accrual_engine.accrual_engine.services.utils import get_settings, months_between
from hr_accrual_engine.accrual_engine.services.validation import validate_component_accounts, prevent_duplicate_run
from hr_accrual_engine.accrual_engine.services.journal import create_accrual_jv

from hr_accrual_engine.accrual_engine.calculations import ticket, leave, eos

CALC_MAP = {
    "Ticket": ticket.calculate,
    "Leave": leave.calculate,
    "EOS": eos.calculate,
}

def build_context(emp, emp_accrual, settings, posting_date):
    # Field mappings come from Accrual Settings.
    # Developers: Do not hardcode employee fieldnames; use mapping.
    salary_field = settings.employee_salary_fieldname or "salary"
    fixed_field = settings.employee_fixed_package_fieldname or "fixed_package"
    leave_days_field = settings.employee_annual_leave_days_fieldname or "annual_leave_days"
    ticket_field = settings.employee_ticket_amount_fieldname or "ticket_amount"

    salary = frappe.utils.flt(getattr(emp, salary_field, 0) or 0)
    fixed_package = frappe.utils.flt(getattr(emp, fixed_field, 0) or (emp_accrual.fixed_package or 0))
    annual_leave_days = int(getattr(emp, leave_days_field, 0) or (emp_accrual.annual_leave_days or 0))
    ticket_amount = frappe.utils.flt(getattr(emp, ticket_field, 0) or (emp_accrual.ticket_amount or 0))

    months_in_year = int(settings.months_in_year or 12)
    salary_days_divisor = int(settings.salary_days_divisor or 30)

    daily_salary = 0
    if fixed_package:
        daily_salary = fixed_package / salary_days_divisor

    service_months = months_between(emp.date_of_joining, posting_date)

    return {
        "salary": salary,
        "fixed_package": fixed_package,
        "annual_leave_days": annual_leave_days,
        "ticket_amount": ticket_amount,
        "months_in_year": months_in_year,
        "salary_days_divisor": salary_days_divisor,
        "daily_salary": daily_salary,
        "service_months": service_months,
        # EOS rates exposed for formulas:
        "eos_first_rate": frappe.utils.flt(settings.eos_first_rate or 0.5),
        "eos_after_rate": frappe.utils.flt(settings.eos_after_rate or 1),
    }

@frappe.whitelist()
def run_accrual(company, posting_date=None):
    posting_date = getdate(posting_date or nowdate())
    settings = get_settings()
    prevent_duplicate_run(company, posting_date)

    run = frappe.new_doc("Accrual Run")
    run.company = company
    run.posting_date = posting_date
    run.status = "Draft"
    run.insert(ignore_permissions=True)

    process_monthly_accrual(company, posting_date, run.name)

    run = frappe.get_doc("Accrual Run", run.name)
    run.status = "Completed"
    run.save(ignore_permissions=True)
    run.submit()
    return run.name

def process_monthly_accrual_scheduled():
    # Default behavior: post accruals on the last day of previous month for each company having settings enabled.
    settings = get_settings()
    if not settings.enable_scheduler:
        return

    companies = frappe.get_all("Company", pluck="name")
    posting_date = frappe.utils.get_last_day(frappe.utils.add_months(getdate(nowdate()), -1))
    for c in companies:
        try:
            run_accrual(c, posting_date)
        except Exception:
            frappe.log_error(frappe.get_traceback(), f"Accrual Scheduler failed for {c} {posting_date}")

def process_monthly_accrual(company, posting_date, run_name=None):
    posting_date = getdate(posting_date)
    settings = get_settings()

    emp_accruals = frappe.get_all(
        "Employee Accrual",
        filters={"disabled": 0},
        fields=["name", "employee", "component", "ticket_amount", "annual_leave_days", "fixed_package", "cost_center"]
    )

    for ea in emp_accruals:
        emp = frappe.get_doc("Employee", ea.employee)
        component = frappe.get_doc("Accrual Component", ea.component)

        if not component.is_active:
            continue

        validate_component_accounts(component)

        context = build_context(emp, frappe.get_doc("Employee Accrual", ea.name), settings, posting_date)

        calc = CALC_MAP.get(component.accrual_type)
        if not calc:
            frappe.throw(f"Unknown accrual type: {component.accrual_type}")

        amount = calc(context, settings)

        je = create_accrual_jv(
            company=company,
            posting_date=posting_date,
            component=component,
            employee=emp,
            amount=amount,
            cost_center=ea.cost_center
        )

        if run_name:
            run = frappe.get_doc("Accrual Run", run_name)
            run.append("logs", {
                "employee": emp.name,
                "component": component.name,
                "amount": amount,
                "journal_entry": je
            })
            run.save(ignore_permissions=True)
