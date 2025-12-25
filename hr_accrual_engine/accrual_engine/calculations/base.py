from frappe.utils import flt
from hr_accrual_engine.accrual_engine.services.utils import eval_formula, round_amt

def calculate_from_formula(formula, context, settings):
    amt = eval_formula(formula, context)
    return round_amt(amt, int(settings.rounding_precision or 2))
