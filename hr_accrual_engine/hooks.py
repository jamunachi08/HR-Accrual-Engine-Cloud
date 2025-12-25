app_name = "hr_accrual_engine"
app_title = "HR Accrual Engine"
app_publisher = "Your Company"
app_description = "Configurable HR accrual engine (Ticket, Leave, EOS) with GL postings"
app_email = "support@yourcompany.com"
app_license = "MIT"

# Fixtures: Roles, Workspace, Custom Fields (optional)
fixtures = [
    {"dt": "Role", "filters": [["name", "in", ["HR Accrual Admin", "HR Accrual Operator", "Finance Accrual Controller", "Accrual Auditor"]]]},
    {"dt": "Workspace", "filters": [["name", "=", "HR Accrual Management"]]},
]

scheduler_events = {
    "monthly": [
        "hr_accrual_engine.accrual_engine.services.processor.process_monthly_accrual_scheduled"
    ]
}

# Permissions: handled via standard Frappe role permissions in DocType JSON
