from log import logging
import numpy as np
import pandas as pd

logger = logging.getLogger('cashflow.py')

class Cashflow:
    def __init__(self):
        pass


    def create_monthly_cashflow_df(self, property_data):
        indices = ["potential_gross_revenue", "absorption_and_turnover_vacancy", "free_rent", "general_vacancy", "effective_gross_revenue", "operating_expenses", "net_operating_income", "principal", "interest", "total_debt_service", "cash_flow_after_debt_service"]
        df = pd.DataFrame()
        df = df.set_axis(indices)
        for i in range(72):
            df[i+1] = np.nan
        for i, r in df.iterrows():
            for col in df:
                v = -1

                if i=="potential_gross_revenue":
                    v = property_data["rent_roll"]["actual_rent_amt_df"].loc["potential_rent_price", col]

                if i=="absorption_and_turnover_vacancy":
                    v = property_data["rent_roll"]["actual_rent_amt_df"].loc["absorption_and_turnover_vacancy", col]
                
                if i=="free_rent":
                    v = property_data["rent_roll"]["actual_rent_amt_df"].loc["free_rent", col]
                # NEEDS FIXED!!!
                if i=="general_vacancy":
                    if ((df.loc["potential_gross_revenue", col] * -property_data["assumptions"]["inputs"]["general_vacancy"]) - df.loc["absorption_and_turnover_vacancy", col] > 0):
                        v = 0
                    else:
                        (df.loc["potential_gross_revenue", col] * -property_data["assumptions"]["inputs"]["general_vacancy"]) - df.loc["absorption_and_turnover_vacancy", col]
                
                if i=="effective_gross_revenue":
                    v = df.loc["potential_gross_revenue", col] + df.loc["absorption_and_turnover_vacancy", col] + df.loc["free_rent", col] + df.loc["general_vacancy", col]
                
                if i=="operating_expenses":
                    v = property_data["opex"]["total_monthly_opex_df"][col].sum()

                if i=="net_operating_income":
                    v = df.loc["effective_gross_revenue", col] - df.loc["operating_expenses", col]
                
                if i=="principal":
                    v = property_data["amortization_schedule"]["amort_schedule_df"].loc["principal", col]
                
                if i=="interest":
                    v = property_data["amortization_schedule"]["amort_schedule_df"].loc["interest", col]
                
                if i=="total_debt_service":
                    v = df.loc["principal", col] + df.loc["interest", col]
                
                if i=="cash_flow_after_debt_service":
                    v = df.loc["net_operating_income", col] - df.loc["total_debt_service", col]
                
                df.loc[i, col] = v
        
        return df

    
    def create_annual_cashflow_df(self, monthly_cashflow_df):
        indices = ["potential_gross_revenue", "absorption_and_turnover_vacancy", "free_rent", "general_vacancy", "effective_gross_revenue", "operating_expenses", "net_operating_income", "principal", "interest", "total_debt_service", "cash_flow_after_debt_service"]
        df = pd.DataFrame()
        df = df.set_axis(indices)
        for i in range(6):
            df[i+1] = np.nan
        df[1] = monthly_cashflow_df[[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]].sum(axis=1)
        df[2] = monthly_cashflow_df[[13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]].sum(axis=1)
        df[3] = monthly_cashflow_df[[25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36]].sum(axis=1)
        df[4] = monthly_cashflow_df[[37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48]].sum(axis=1)
        df[5] = monthly_cashflow_df[[49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60]].sum(axis=1)
        df[6] = monthly_cashflow_df[[61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72]].sum(axis=1)
        return df