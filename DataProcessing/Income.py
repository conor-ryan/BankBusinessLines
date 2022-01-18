"""
Packages
"""
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

plt.style.use('seaborn')

#Import dataframe

#os.chdir('/home/pando004/Desktop/BankData/FRY9')
#df = pd.read_csv('frdata.csv')
# os.chdir('G:/Shared drives/BankBusinessLines')
os.chdir('/home/ryan0463/Documents/Research/BankBusinessLines')
df = pd.read_csv('Data/frdata.csv')

# make date variable
df['date'] = pd.to_datetime( df.RSSD9999, format='%Y%m%d')
df = df.sort_values(by=['date'])

# drop dataframe dates to match market size data
df = df[ ~(df['date'] < df.date.unique()[86] ) ]

# replace nan entries in data with zero value
df[['BHCK4174','BHCK6760','BHCK4176','BHCK6761','BHCKA517','BHCKA518','BHCKHK03','BHCKHK04','BHDM1797','BHDM5367',
    'BHDM5368','BHCKF158','BHCKF159','BHDM1420','BHDM1975','BHDM1460','BHCKF160','BHCKF161','BHCK1292','BHCK1296',
    'BHCK1590','BHDM1766','BHDMJ454','BHDM1545','BHDM2165','BHDMKX57','BHCK5411','BHCKC234','BHCKC235','BHCK5412',
    'BHCKC217','BHCKC218','BHCKC891','BHCKC893','BHCK3584','BHCK3588','BHCKC895','BHCKC897','BHCK4655','BHCK4645',
    'BHCKB514','BHCKK129','BHCKK205','BHCK4644','BHCKF158','BHCKC880','BHCKKX50','BHCKC892','BHCKC894','BHCK3585',
    'BHCK3589','BHCKC896','BHCKC898','BHCK4665','BHCK4617','BHCKB515','BHCKK133','BHCKK206','BHCK4628','BHCKF187',
    'BHCKF188','BHCKKX51',
    'BHCK4135','BHCK4217','BHCK4092','BHCK4093',
    'BHCK2170']] = (

        df[['BHCK4174','BHCK6760','BHCK4176','BHCK6761','BHCKA517','BHCKA518','BHCKHK03','BHCKHK04','BHDM1797','BHDM5367',
            'BHDM5368','BHCKF158','BHCKF159','BHDM1420','BHDM1975','BHDM1460','BHCKF160','BHCKF161','BHCK1292','BHCK1296',
            'BHCK1590','BHDM1766','BHDMJ454','BHDM1545','BHDM2165','BHDMKX57','BHCK5411','BHCKC234','BHCKC235','BHCK5412',
            'BHCKC217','BHCKC218','BHCKC891','BHCKC893','BHCK3584','BHCK3588','BHCKC895','BHCKC897','BHCK4655','BHCK4645',
            'BHCKB514','BHCKK129','BHCKK205','BHCK4644','BHCKF158','BHCKC880','BHCKKX50','BHCKC892','BHCKC894','BHCK3585',
            'BHCK3589','BHCKC896','BHCKC898','BHCK4665','BHCK4617','BHCKB515','BHCKK133','BHCKK206','BHCK4628','BHCKF187',
            'BHCKF188','BHCKKX51',
            'BHCK4135','BHCK4217','BHCK4092','BHCK4093',
            'BHCK2170']].fillna(0) )

### Bank Size ###
df['total_assets'] = df['BHCK2170']

# total revenue = interest revenue + non-interest revenue + realized gains on securitie
df['interest_revenue'] = df['BHCK4107']
df['non_interest_revenue'] = df['BHCK4079']
df['securities_gain'] = df['BHCK3521'] + df['BHCK3196']

# total expense = interest expense + non-interest expense + provisions for loan losses
df['interest_expense'] = df['BHCK4073']
df['non_interest_expense'] = df['BHCK4093']
df['provisions'] = df['BHCK4230']
df['taxes'] = df['BHCK4302']

# net income attributed to holding company less minority interests
df['net_income'] = df['BHCK4340']

# net income including minority interests
df['net_income_min'] = df['BHCKG104']


# compute industry aggregates
interest_revenue = []
non_interest_revenue = []
gains_revenue = []
interest_expense = []
non_interest_expense = []
provisions = []
taxes = []
net_income = []
net_income_min = []

equity_gains = []
disc_op  = []

quart = 0
for at, t in enumerate( df.date.unique() ):

    # if first quarter, just report the accumulated flows
    if quart == 0:
        equity_gains.append(  np.nansum( df[ df.date ==t ]['BHCKHT70'] )/(1000*1000) )
        disc_op.append(  np.nansum( df[ df.date ==t ]['BHCKHT69'] )/(1000*1000) )

        interest_revenue.append(  np.nansum( df[ df.date ==t ]['BHCK4107'] )/(1000*1000) )
        non_interest_revenue.append(  np.nansum( df[ df.date ==t ]['BHCK4079'] )/(1000*1000) )
        gains_revenue.append(  np.nansum( df[ df.date ==t ]['BHCK3521'] + df[ df.date ==t ]['BHCK3196'])/(1000*1000) )

        interest_expense.append(  np.nansum( df[ df.date ==t ]['BHCK4073'] )/(1000*1000) )
        non_interest_expense.append(  np.nansum( df[ df.date ==t ]['BHCK4093'] )/(1000*1000) )

        provisions.append(  np.nansum( df[ df.date ==t ]['BHCK4230'] )/(1000*1000) )
        taxes.append(  np.nansum( df[ df.date ==t ]['BHCK4302'] )/(1000*1000) )
        
        net_income.append(  np.nansum( df[ df.date ==t ]['BHCK4340'] )/(1000*1000) )
        net_income_min.append(  np.nansum( df[ df.date ==t ]['BHCKG104'] )/(1000*1000) )
      

    # if not first quarter, compute difference in flows from last period        
    else:        
        equity_gains.append( np.nansum( df[ df.date ==t ]['BHCKHT70'] )/(1000*1000) - np.nansum( df[ df.date == df.date.unique()[at-1] ]['BHCKHT70'] )/(1000*1000) )
        disc_op.append( np.nansum( df[ df.date ==t ]['BHCKHT69'] )/(1000*1000) - np.nansum( df[ df.date == df.date.unique()[at-1] ]['BHCKHT69'] )/(1000*1000) )

        interest_revenue.append( np.nansum( df[ df.date ==t ]['BHCK4107'] )/(1000*1000) - np.nansum( df[ df.date == df.date.unique()[at-1] ]['BHCK4107'] )/(1000*1000) )
        non_interest_revenue.append( np.nansum( df[ df.date ==t ]['BHCK4079'] )/(1000*1000) - np.nansum( df[ df.date == df.date.unique()[at-1] ]['BHCK4079'] )/(1000*1000) )
        gains_revenue.append( np.nansum( df[ df.date ==t ]['BHCK3521'] + df[ df.date ==t ]['BHCK3196'] )/(1000*1000) - np.nansum( df[ df.date == df.date.unique()[at-1] ]['BHCK3521'] + df[ df.date == df.date.unique()[at-1] ]['BHCK3196'])/(1000*1000) )

        interest_expense.append( np.nansum( df[ df.date ==t ]['BHCK4073'] )/(1000*1000) - np.nansum( df[ df.date == df.date.unique()[at-1] ]['BHCK4073'] )/(1000*1000) )
        non_interest_expense.append( np.nansum( df[ df.date ==t ]['BHCK4093'] )/(1000*1000) - np.nansum( df[ df.date == df.date.unique()[at-1] ]['BHCK4093'] )/(1000*1000) )

        provisions.append( np.nansum( df[ df.date ==t ]['BHCK4230'] )/(1000*1000) - np.nansum( df[ df.date == df.date.unique()[at-1] ]['BHCK4230'] )/(1000*1000) )
        taxes.append( np.nansum( df[ df.date ==t ]['BHCK4302'] )/(1000*1000) - np.nansum( df[ df.date == df.date.unique()[at-1] ]['BHCK4302'] )/(1000*1000) )

        net_income.append( np.nansum( df[ df.date ==t ]['BHCK4340'] )/(1000*1000) - np.nansum( df[ df.date == df.date.unique()[at-1] ]['BHCK4340'] )/(1000*1000) )          
        net_income_min.append( np.nansum( df[ df.date ==t ]['BHCKG104'] )/(1000*1000) - np.nansum( df[ df.date == df.date.unique()[at-1] ]['BHCKG104'] )/(1000*1000) )          
        
    if quart < 3:
        quart = quart + 1
    else:
        quart = 0


# check the accounting identity
plt.close('all')
plt.plot(df.date.unique(), net_income, label='reported net income')
plt.plot( df.date.unique(),np.asarray(( interest_revenue )) + np.asarray(( non_interest_revenue )) + np.asarray(( gains_revenue )) - \
                           np.asarray(( interest_expense )) - np.asarray(( non_interest_expense )) - np.asarray(( provisions )) - \
                           np.asarray(( taxes )), label='aggregated net income')
plt.legend()





# Convert intra-year comprehensive flows into quarterly flows
# first compute quartlery revenue for each bank, each quarter
for idx, bank in enumerate( df.RSSD9001.unique() ):

    print('Bank',idx,' out of ', len(df.RSSD9001.unique()) )
    quart = 0
    
    for at, t in enumerate( df.date.unique() ):
    
        # if first quarter, just report the accumulated flows
        if quart == 0:
            df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'interest_revenue']   = df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4107']
            
        # if not first quarter, compute difference in flows from last period
        else:
            df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'interest_revenue']   = float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4107']) - float(df[ (df.date==df.date.unique()[at-1]) & (df.RSSD9001 == bank) ]['BHCK4107'])
    
        if quart < 3:
            quart = quart + 1
        else:
            quart = 0
    



