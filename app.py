# import json
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
        property_data = amort.build_amort_object(property_data)
        property_data = capex.build_capex_object(property_data)
        property_data = rent.build_rent_roll_object(property_data)
        property_data = opex.build_opex_object(property_data)
        property_data = cashflow.build_cashflow_object(property_data)
        property_data = analyzer.build_analysis_object(property_data)
        property_data = files.convert_df_to_json(property_data)
        return property_data

    except Exception as e:
        logger.error(e)
        exit_code = 1

    exit(exit_code)

# # TEST main()
# property_data = files.read_json('./inputs.json')
# property_data = main(property_data)
# print(property_data)
# # Serializing json
# json_object = json.dumps(property_data, indent=4)
 
# # Writing to sample.json
# with open("./property_data.json", "w") as outfile:
#     outfile.write(json_object)