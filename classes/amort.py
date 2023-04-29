from log import logging
import numpy as np
import pandas as pd

logger = logging.getLogger('amort.py')

class Amort:
    def __init__(self):
        pass

    
    def PMT(self, rate, nper,pv, fv=0, type=0):
        if rate!=0:
                pmt = (rate*(fv+pv*(1+ rate)**nper))/((1+rate*type)*(1-(1+ rate)**nper))
        else:
                pmt = (-1*(fv+pv)/nper)  
        return(pmt)


    def IPMT(self, rate, per, nper,pv, fv=0, type=0):
        ipmt = -( ((1+rate)**(per-1)) * (pv*rate + self.PMT(rate, nper,pv, fv=0, type=0)) - self.PMT(rate, nper,pv, fv=0, type=0))
        return(ipmt)


    def PPMT(self, rate, per, nper,pv, fv=0, type=0):
        ppmt = self.PMT(rate, nper,pv, fv=0, type=0) - self.IPMT(rate, per, nper, pv, fv=0, type=0)
        return(ppmt)
    

    def create_amort_schedule_df(self, amount, annualinterestrate, paymentsperyear, years, hold_period):
        new_df = pd.DataFrame()
        df = pd.DataFrame({
            'principal' :[self.PPMT(annualinterestrate/paymentsperyear, i+1, paymentsperyear*years, amount) for i in range(paymentsperyear*years)],
            'interest' :[self.IPMT(annualinterestrate/paymentsperyear, i+1, paymentsperyear*years, amount) for i in range(paymentsperyear*years)]
        })
        df['amount'] = df.principal + df.interest
        df['balance'] = amount + np.cumsum(df.principal)
        for i, row in df.iterrows():
            if i <= ((hold_period + 1) * 12):
                for col in df:
                    new_df.loc[col, i+1] = row[col]
            else:
                 break
        return new_df
    