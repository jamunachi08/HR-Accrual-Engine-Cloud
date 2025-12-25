from .base import calculate_from_formula

def calculate(context, settings):
    # decide which EOS formula based on service months threshold (configurable)
    threshold = int(settings.eos_transition_months or 60)
    service_months = int(context.get("service_months") or 0)
    if service_months <= threshold:
        return calculate_from_formula(settings.eos_formula_first, context, settings)
    return calculate_from_formula(settings.eos_formula_after, context, settings)
