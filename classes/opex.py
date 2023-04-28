from log import logging
from math import floor
import numpy as np
import pandas as pd

logger = logging.getLogger('opex.py')

class Opex:
    def __init__(self):
        pass

    def calc_monthly_expenses(self, property_data):
        monthly_expenses = {}
        opex = property_data["opex"]['inputs']
        monthly_expenses["capex"] = property_data["capex"]["totals"]["cost_per_month_total"]
        for ex in opex:
            if ex == "real_estate_taxes":
                monthly_expenses[ex] = (opex[ex]/100 * property_data["assumptions"]['inputs']["purchase_price"])/12
            if ex == "insurance":
                monthly_expenses[ex] = opex[ex]/12
            if ex == "mortgage_insurance":
                monthly_expenses[ex] = opex[ex]/12
            if ex == "utilities":
                monthly_expenses[ex] = opex[ex]
            if ex == "management_fee":
                monthly_expenses[ex] = 0 # CANT DO THIS CURRENTLY!!! # NEEDS FIXED!!!
            if ex == "advertising":
                monthly_expenses[ex] = opex[ex]/12
            if ex == "tax_service":
                monthly_expenses[ex] = opex[ex]/12
            if ex == "other":
                monthly_expenses[ex] = opex[ex]
        return monthly_expenses
    

    def create_montly_opex_df(self, property_data):
        indices = [ex for ex in property_data["opex"]["total_monthly_opex"]]
        df = pd.DataFrame()
        df = df.set_axis(indices)
        for i in range(72):
            df[i+1] = np.nan
        for i, r in df.iterrows():
            for col in df:
                df.loc[i, col] = property_data["opex"]["total_monthly_opex"][i] * (1+property_data["assumptions"]["inputs"]["growth_rate_expenses"])**(floor(col/12))
        return df