from .base import calculate_from_formula

def calculate(context, settings):
    return calculate_from_formula(settings.leave_formula, context, settings)
