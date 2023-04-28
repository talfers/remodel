from log import logging
import numpy as np
import pandas as pd
from amortization.schedule import amortization_schedule

logger = logging.getLogger('amort.py')

class Amort:
    def __init__(self):
        pass

    def create_amort_schedule(self, purchase_price, interest_rate, years):
        amort_schedule = amortization_schedule(purchase_price, interest_rate, years*12) # NEEDS FIXED!!!
        # for number, amount, interest, principal, balance in amort_schedule:
        #     print(number, amount, interest, principal, balance)
        return amort_schedule

    def create_amort_schedule_df(self, amort_schedule):
        indices = ["amount", "interest", "principal", "balance"]
        df = pd.DataFrame()
        df = df.set_axis(indices)
        for number, amount, interest, principal, balance in amort_schedule:
            df.loc["amount", number] = amount
            df.loc["interest", number] = interest
            df.loc["principal", number] = principal
            df.loc["balance", number] = balance
        return df
    