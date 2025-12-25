# Configuration

## 1. Accrual Settings
Path: HR Accrual Management > Accrual Settings

Configure:
- Months In Year (default 12)
- Salary Days Divisor (default 30)
- Rounding Precision
- EOS transition months (default 60)
- EOS rates (first and after transition)
- Employee field mappings (salary, fixed package, annual leave days, ticket amount)
- Formulas (all editable)

### Default formulas
- Ticket: `ticket_amount / months_in_year`
- Leave: `(daily_salary * annual_leave_days) / months_in_year`
- EOS first: `(salary * eos_first_rate) / months_in_year`
- EOS after: `(salary * eos_after_rate) / months_in_year`

All formulas are evaluated using Frappe safe_eval with the context variables:
`salary, fixed_package, annual_leave_days, ticket_amount, months_in_year, salary_days_divisor, daily_salary, service_months, eos_first_rate, eos_after_rate`

## 2. Accrual Components
Create one record per accrual type and set Debit/Credit accounts.

## 3. Employee Accrual
Create rows per employee per component. You may store values in Employee fields and/or override per row.

## 4. Scheduler
Enable "Enable Scheduler" in Accrual Settings to auto-run monthly.
