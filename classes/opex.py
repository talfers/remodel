import logging
from math import floor
import numpy as np
import pandas as pd

logger = logging.getLogger('opex.py')


class Opex:
    def __init__(self) -> None:
        pass

    def calc_monthly_expenses(self, property_data: dict) -> dict:
        monthly_expenses: dict[str, float] = {}
        opex: dict[str, float] = property_data["opex"]['inputs']
        monthly_expenses["capex"] = property_data["capex"]["totals"]["cost_per_month_total"]
        for expense in opex:
            if expense == "real_estate_taxes":
                monthly_expenses[expense] = (opex[expense]/100 * property_data["assumptions"]['inputs']["purchase_price"])/12
            if expense == "insurance":
                monthly_expenses[expense] = opex[expense]/12
            if expense == "mortgage_insurance":
                monthly_expenses[expense] = opex[expense]/12
            if expense == "utilities":
                monthly_expenses[expense] = opex[expense]
            if expense == "management_fee":
                monthly_expenses[expense] = opex[expense] * property_data["rent_roll"]["actual_rent_amt_df"].loc["egr", 1]
            if expense == "advertising":
                monthly_expenses[expense] = opex[expense]/12
            if expense == "tax_service":
                monthly_expenses[expense] = opex[expense]/12
            if expense == "other":
                monthly_expenses[expense] = opex[expense]
        return monthly_expenses


    def create_monthly_opex_df(self, property_data) -> pd.DataFrame:
        indices: List[str] = [expense for expense in property_data["opex"]["total_monthly_opex"]]
        df: pd.DataFrame = pd.DataFrame(index=indices, columns=list(range(1, 73)), dtype=np.float64).fillna(np.nan)
        for expense in df.index:
            if expense == "management_fee":
                df.loc[expense] = property_data['assumptions']['inputs']['general_vacancy'] * property_data["rent_roll"]["actual_rent_amt_df"].loc["egr"]
            else:
                df.loc[expense] = property_data["opex"]["total_monthly_opex"][expense] * (1+property_data["assumptions"]["inputs"]["growth_rate_expenses"])**(floor(1/12))
        return df