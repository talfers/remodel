from log import logging
import json

logger = logging.getLogger('files.py')

class Files:
    def __init__(self):
        pass

    def read_json(self, filepath):
        f = open (filepath, "r")
        j = json.loads(f.read())
        f.close()
        return j


    def convert_df_to_json(self, property_data):
        property_data["amortization_schedule"]["amort_schedule"] = None
        property_data["amortization_schedule"]["amort_schedule_df"] = json.loads(property_data["amortization_schedule"]["amort_schedule_df"].to_json())
        property_data["opex"]["total_monthly_opex_df"] = json.loads(property_data["opex"]["total_monthly_opex_df"].to_json())
        property_data["rent_roll"]["market_rent_df"] = json.loads(property_data["rent_roll"]["market_rent_df"].to_json())
        property_data["rent_roll"]["free_rent_df"] = json.loads(property_data["rent_roll"]["free_rent_df"].to_json())
        property_data["rent_roll"]["actual_rent_price_per_sqft_df"] = json.loads(property_data["rent_roll"]["actual_rent_price_per_sqft_df"].to_json())
        property_data["rent_roll"]["actual_rent_amt_df"] = json.loads(property_data["rent_roll"]["actual_rent_amt_df"].to_json())
        property_data["cashflow"]["monthly_cash_flow_df"] = json.loads(property_data["cashflow"]["monthly_cash_flow_df"].to_json())
        property_data["cashflow"]["annual_cash_flow_df"] = json.loads(property_data["cashflow"]["annual_cash_flow_df"].to_json())
        property_data["analysis"]["unleveraged_return_analysis"] = json.loads(property_data["analysis"]["unleveraged_return_analysis"].to_json())
        property_data["analysis"]["leveraged_return_analysis"] = json.loads(property_data["analysis"]["leveraged_return_analysis"].to_json())
        return property_data