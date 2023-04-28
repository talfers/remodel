from log import logging
from math import floor, ceil
import numpy as np
import pandas as pd

logger = logging.getLogger('rent.py')

class Rent:
    def __init__(self):
        pass


    def calc_rent_estimates(self, property_data):
        rent_amt = {
            "new": property_data["assumptions"]["inputs"]["potential_rent"], 
            "renewal": property_data["assumptions"]["inputs"]["current_rent"]
        }
        rent_price_per_sqft = {
            "new": rent_amt["new"]/property_data["assumptions"]["inputs"]["square_feet"]*12, 
            "renewal": rent_amt["renewal"]/property_data["assumptions"]["inputs"]["square_feet"]*12
        }
        rent_price_per_sqft["weighted"] = rent_price_per_sqft["new"] * (1 - property_data["rent_roll"]["inputs"]["renew_probability_pct"]) + (rent_price_per_sqft["renewal"]*property_data["rent_roll"]["inputs"]["renew_probability_pct"])
        return {"rent_amt": rent_amt, "rent_price_per_sqft": rent_price_per_sqft}


    def calc_vacancy_loss(self, property_data):
        weighted_downtime = round(property_data["rent_roll"]["inputs"]["downtime"] * (1 - property_data["rent_roll"]["inputs"]["renew_probability_pct"])+0*(property_data["rent_roll"]["inputs"]["renew_probability_pct"]),0)
        weighted_free_rent = round(property_data["rent_roll"]["inputs"]["free_rent_new"] * (1 - property_data["rent_roll"]["inputs"]["renew_probability_pct"])+property_data["rent_roll"]["inputs"]["free_rent_renewal"]*(property_data["rent_roll"]["inputs"]["renew_probability_pct"]),2)
        return {"weighted_downtime": weighted_downtime, "weighted_free_rent": weighted_free_rent}


    def create_market_rent_df(self, property_data):
        df = pd.DataFrame()
        for i in range(72):
            df[i+1] = np.nan
        for col in df:
            df.loc["market_rent_price_per_sqft", col] = property_data["rent_roll"]["rent_estimates"]["rent_price_per_sqft"]["weighted"] * (1+property_data["assumptions"]["inputs"]["growth_rate_income"])**(floor(col/12))
        return df


    def create_free_rent_df(self, property_data):
        start_month = property_data["assumptions"]["inputs"]["lease_expiration_mo_num"] + 1
        end_month = start_month + int(round(max(property_data["rent_roll"]["inputs"]["free_rent_new"], property_data["rent_roll"]["inputs"]["free_rent_renewal"]) + property_data["rent_roll"]["inputs"]["downtime"]))
        df = pd.DataFrame()
        for i in range(start_month, end_month):
            df[i] = np.nan
        idx = 1
        for col in df:
            v = 0
            if idx<=floor(property_data["rent_roll"]["vacany_loss"]["weighted_free_rent"]):
                v = 1
            if idx==ceil(property_data["rent_roll"]["vacany_loss"]["weighted_free_rent"]):
                v = property_data["rent_roll"]["vacany_loss"]["weighted_free_rent"] - floor(property_data["rent_roll"]["vacany_loss"]["weighted_free_rent"])
            df.loc["free_rent_pct", col] = v
            idx+=1
        return df


    def create_actual_rent_price_per_sqft_df(self, property_data):
        indices = ["potential_rent_price", "absorption_and_turnover_vacancy", "free_rent"]
        df = pd.DataFrame()
        df = df.set_axis(indices)
        for i in range(72):
            df[i+1] = np.nan
        for i, r in df.iterrows():
            for col in df:
                v = -1
                if i=="potential_rent_price":
                    if col <= property_data["assumptions"]["inputs"]["lease_expiration_mo_num"]:
                        v = property_data["rent_roll"]["rent_estimates"]["rent_price_per_sqft"]["renewal"]
                    elif col > (property_data["assumptions"]["inputs"]["lease_expiration_mo_num"]+1):
                        v = property_data["rent_roll"]["market_rent_df"].loc["market_rent_price_per_sqft", col]
                    else:
                        v = property_data["rent_roll"]["market_rent_df"].loc["market_rent_price_per_sqft", property_data["assumptions"]["inputs"]["lease_expiration_mo_num"]+1]
                if i=="absorption_and_turnover_vacancy":
                    if (col>property_data["assumptions"]["inputs"]["lease_expiration_mo_num"] and col<property_data["assumptions"]["inputs"]["lease_expiration_mo_num"]+(property_data["rent_roll"]["vacany_loss"]["weighted_downtime"] + 1)):
                        v = -1 * df.loc["potential_rent_price", col]
                    else:
                        v = 0
                if i=="free_rent":
                    try:
                        v = -1 * property_data["rent_roll"]["free_rent_df"].loc["free_rent_pct", col] * df.loc["potential_rent_price", col]
                    except:
                        v = 0
                df.loc[i, col] = v
        return df
    
    def create_actual_rent_amt_df(self, property_data):
        return property_data["rent_roll"]["actual_rent_price_per_sqft_df"] * property_data["assumptions"]["inputs"]["square_feet"] / 12