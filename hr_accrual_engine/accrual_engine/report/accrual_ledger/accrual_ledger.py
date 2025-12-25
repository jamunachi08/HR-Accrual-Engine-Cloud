import frappe

def execute(filters=None):
    filters = filters or {}
    columns = [
        {"label":"Posting Date","fieldname":"posting_date","fieldtype":"Date","width":110},
        {"label":"Company","fieldname":"company","fieldtype":"Link","options":"Company","width":140},
        {"label":"Employee","fieldname":"employee","fieldtype":"Link","options":"Employee","width":140},
        {"label":"Component","fieldname":"component","fieldtype":"Link","options":"Accrual Component","width":160},
        {"label":"Amount","fieldname":"amount","fieldtype":"Currency","width":120},
        {"label":"Journal Entry","fieldname":"journal_entry","fieldtype":"Link","options":"Journal Entry","width":140},
    ]
    data = frappe.db.sql(
        """
        SELECT ar.posting_date, ar.company, log.employee, log.component, log.amount, log.journal_entry
        FROM `tabAccrual Run` ar
        JOIN `tabAccrual Run Log` log ON log.parent = ar.name
        WHERE ar.docstatus = 1
        ORDER BY ar.posting_date DESC
        """,
        as_dict=True
    )
    return columns, data
