from log import logging

logger = logging.getLogger('capex.py')

class Capex:
    def __init__(self):
        pass


    def calc_component_costs(self, capex):
        property_components = capex["property_components"]
        totals = {"replacement_cost_total": 0, "cost_per_year_total": 0, "cost_per_month_total": 0}
        for c in property_components:
            property_components[c]["cost_per_year"] = property_components[c]["replacement_cost_amt"] / max((property_components[c]["lifespan"] - property_components[c]["current_age"]), 1)
            property_components[c]["cost_per_month"] = property_components[c]["cost_per_year"] / 12
            totals["replacement_cost_total"] = totals["replacement_cost_total"] + property_components[c]["replacement_cost_amt"]
            totals["cost_per_year_total"] = totals["cost_per_year_total"] + property_components[c]["cost_per_year"]
            totals["cost_per_month_total"] = totals["cost_per_month_total"] + property_components[c]["cost_per_month"]
        capex["totals"] = totals
        capex["property_components"] = property_components
        return capex
    