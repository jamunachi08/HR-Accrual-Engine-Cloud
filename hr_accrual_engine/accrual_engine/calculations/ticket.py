from .base import calculate_from_formula

def calculate(context, settings):
    # uses settings.ticket_formula
    return calculate_from_formula(settings.ticket_formula, context, settings)
