import json
from log import logging
from classes.capex import Capex
from classes.opex import Opex
from classes.rent import Rent
from classes.amort import Amort
from classes.cashflow import Cashflow
from classes.analyzer import Analyzer
from classes.files import Files


logger = logging.getLogger('app.py')


files = Files()
capex = Capex()
opex = Opex()
rent = Rent()
amort = Amort()
cashflow = Cashflow()
analyzer = Analyzer()

def main(property_data):
    exit_code = 0
    try:
        orig_inputs = property_data
        amort_schedule_df = amort.create_amort_schedule_df(
            property_data['assumptions']['inputs']['purchase_price'], 
            property_data['assumptions']['inputs']['interest_rate'],
            12, 
            property_data['assumptions']['inputs']['amortization_period']
        )
        property_data["amortization_schedule"] = {"amort_schedule_df": amort_schedule_df}
        property_data["capex"] = capex.calc_component_costs(property_data["capex"])
        property_data["rent_roll"]["rent_estimates"] = rent.calc_rent_estimates(property_data)
        property_data["rent_roll"]["vacany_loss"] = rent.calc_vacancy_loss(property_data)
        property_data["rent_roll"]["market_rent_df"] = rent.create_market_rent_df(property_data)
        property_data["rent_roll"]["free_rent_df"] = rent.create_free_rent_df(property_data)
        property_data["rent_roll"]["actual_rent_price_per_sqft_df"] = rent.create_actual_rent_price_per_sqft_df(property_data)
        property_data["rent_roll"]["actual_rent_amt_df"] = rent.create_actual_rent_amt_df(property_data)
        property_data["opex"]["total_monthly_opex"] = opex.calc_monthly_expenses(property_data)
        property_data["opex"]["total_monthly_opex_df"] = opex.create_monthly_opex_df(property_data)
        property_data["cashflow"] = {"monthly_cash_flow_df": cashflow.create_monthly_cashflow_df(property_data), "annual_cashflow_df": None}
        property_data["cashflow"]["annual_cash_flow_df"] = cashflow.create_annual_cashflow_df(property_data["cashflow"]["monthly_cash_flow_df"])
        property_data["analysis"] = { 
            "valuation_at_sale": analyzer.create_valuation_at_sale(property_data),
            "unleveraged_return_analysis": None,
            "leveraged_return_analysis": None
        }
        property_data["analysis"]["unleveraged_return_analysis"] = analyzer.create_unleveraged_return_analysis_df(property_data)
        property_data["analysis"]["leveraged_return_analysis"] = analyzer.create_leveraged_return_analysis_df(property_data)
        property_data["analysis"]["irr"] = analyzer.create_return_analysis(property_data["analysis"]["unleveraged_return_analysis"], property_data["analysis"]["leveraged_return_analysis"])
        property_data = files.convert_df_to_json(property_data)
        return property_data
        

    except Exception as e:
        logger.error(e)
        exit_code = 1

    exit(exit_code)

# # TEST main()
property_data = files.read_json('./inputs.json')
property_data = main(property_data)
# Serializing json
json_object = json.dumps(property_data, indent=4)
 
# Writing to sample.json
with open("./property_data.json", "w") as outfile:
    outfile.write(json_object)