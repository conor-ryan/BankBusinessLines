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
os.chdir('G:/Shared drives/BankBusinessLines')
df = pd.read_csv('Data/frdata.csv')

# make date variable
df['date'] = pd.to_datetime( df.RSSD9999, format='%Y%m%d')

df = df.sort_values(by=['date'])

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

#### Limit to only banks of a certain size ####
##  20 Largest Banks in total assets at the end of 2020
## Is it okay that these banks have some attrition in the older years?
## We are missing Q4 2019, need to download data. 
top10_idx = df[df.date == '2020-12-31T00:00:00.000000000']['total_assets'].nlargest(20).index
for i in range(len(top10_idx)):
    idx =  df[df.index == top10_idx[i] ]['RSSD9001'].unique()[0]
    if i ==0:
        temp_df = df[df.RSSD9001 == idx]
    else:
        temp_df = temp_df.append( df[df.RSSD9001 == idx] )

# re-write the dataframe with the smaller subset of banks
df = temp_df.copy()
        
#---------------------# 
#                     #  
#   Consumer Loans    #
#                     #  
#---------------------#

# create consumer loan net charge-off (NCO) and total consumer lending
df['consumer_loan_nco']   =   (( df['BHCK5411'] + df['BHCKC234'] + df['BHCKC235'] ) -
                               ( df['BHCK5412'] + df['BHCKC217'] + df['BHCKC218'] ))

df['consumer_loans'] = df['BHDM1797'] + df['BHDM5367'] + df['BHDM5368']

df['new_consumer_loans'] = np.nan
df['consumer_rate']      = np.nan
df['consumer_revenue']   = np.nan
df['consumer_default_rate']   = np.nan

df['consumer_rate_lagged']      = np.nan

am_rate = 1/10 

# first compute quartlery revenue for each bank, each quarter
for idx, bank in enumerate( df.RSSD9001.unique() ):
    
    quart = 3
    
    for at, t in enumerate( df.date.unique() ):
        if at ==0:
            try:
                df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'consumer_revenue']   = (1/3)*np.float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4435'])
            except:
                pass
        else:
            if quart == 0:
                try:
                    df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'consumer_revenue']   = np.float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4435'])
                except:
                    pass 
            else:
                try:
                    df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'consumer_revenue']   = np.float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4435']) - np.float(df[ (df.date==df.date.unique()[at-1]) & (df.RSSD9001 == bank) ]['BHCK4435'])
                except:
                    pass
                
            if quart < 3:
                quart = quart + 1
            else:
                quart = 0


# for each bank
for idx, bank in enumerate( df.RSSD9001.unique() ):

    print('Bank ',idx,' out of ',len(df.RSSD9001.unique()) )

    # initialize multiplier
    quart = 3  # first observed quarter is Q3 for 1986
    
    # for each time period 
    for at, t in enumerate( df.date.unique() ):
            
        # compute default rate
            # sum of charge-offs (time t)/ sum of loans (t-1)
        if at == 0:  # first period observed is 1986 Q3; can only use contemporaneous values
        
            try:
                # default rate 
                default_rate = (1/3)*( np.float(df[ (df.date ==t) & (df.RSSD9001 == bank)]['consumer_loan_nco'])/
                                       np.float(df[ (df.date ==t) & (df.RSSD9001 == bank)]['consumer_loans']) )
                
                # new lending 
                new_lending = ( np.float(df[ (df.date ==t) & (df.RSSD9001 == bank)]['consumer_loans']) -
                                (1-am_rate)*(1-default_rate)*np.float(df[ (df.date ==t) & (df.RSSD9001 == bank)]['consumer_loans']) )  
    
                # new rate
                agg_rev = (1/3)*np.float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4435'])
                
                new_rate =  (agg_rev - ( (1/3)*(1-am_rate)*(1-default_rate) )*np.float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4435']))/new_lending  
                lag_rate =  (np.float(df[ (df.date==df.date.unique()[at+1]) & (df.RSSD9001 == bank) ]['consumer_revenue']) - ( (1-am_rate)*(1-default_rate) )*np.float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['consumer_revenue']))/new_lending  
            except:
                new_lending = np.nan
                new_rate = np.nan
                lag_rate = np.nan
                default_rate = 0
                
            # record new lending, rate and period revenues                                                                                                                       
            df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'new_consumer_loans'] = new_lending
            df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'consumer_rate']      = new_rate
            df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'consumer_rate_lagged']      = lag_rate
            df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'consumer_default_rate']   = default_rate
            
        else:

            if quart == 0:
                
                try:
                    default_rate = ( np.float(df[ (df.date ==t) & (df.RSSD9001 == bank)]['consumer_loan_nco'])/
                                     np.float(df[ (df.date ==df.date.unique()[at-1]) & (df.RSSD9001 == bank)]['consumer_loans']) )
        
                    new_lending = ( np.float(df[ (df.date ==t) & (df.RSSD9001 == bank)]['consumer_loans']) -
                                    (1-am_rate)*(1-default_rate)*np.float(df[ (df.date ==df.date.unique()[at-1]) & (df.RSSD9001 == bank)]['consumer_loans']) )  
                    
                    # new rate
                    agg_rev = np.float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4435'])
                    
                    new_rate =  (agg_rev - ( (1-am_rate)*(1-default_rate) )*np.float(df[ (df.date==df.date.unique()[at-1]) & (df.RSSD9001 == bank) ]['consumer_revenue']))/new_lending  
                    lag_rate =  (np.float(df[ (df.date==df.date.unique()[at+1]) & (df.RSSD9001 == bank) ]['consumer_revenue']) - ( (1-am_rate)*(1-default_rate) )*np.float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['consumer_revenue']))/new_lending  
                
                except:
                    new_lending = np.nan
                    new_rate = np.nan
                    lag_rate = np.nan
                    default_rate = 0

                # record new lending, rate and period revenues                                                                                                                       
                df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'new_consumer_loans'] = new_lending
                df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'consumer_rate']      = new_rate
                df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'consumer_rate_lagged']      = lag_rate
                df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'consumer_default_rate']   = default_rate

            else:
                
                try:
                    default_rate = ( (np.float(df[ (df.date ==t) & (df.RSSD9001 == bank)]['consumer_loan_nco']) -
                                      np.float(df[ (df.date ==df.date.unique()[at-1]) & (df.RSSD9001 == bank)]['consumer_loan_nco']))/
                                               np.float(df[ (df.date ==df.date.unique()[at-1]) & (df.RSSD9001 == bank)]['consumer_loans']) )
        
                    new_lending = ( np.float(df[ (df.date ==t) & (df.RSSD9001 == bank)]['consumer_loans']) -
                                    (1-am_rate)*(1-default_rate)*np.float(df[ (df.date ==df.date.unique()[at-1]) & (df.RSSD9001 == bank)]['consumer_loans']) )  
                    
                    # new rate
                    agg_rev = np.float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4435']) - np.float(df[ (df.date==df.date.unique()[at-1]) & (df.RSSD9001 == bank) ]['BHCK4435'])
                    
                    new_rate =  (agg_rev - ( (1-am_rate)*(1-default_rate) )*np.float(df[ (df.date==df.date.unique()[at-1]) & (df.RSSD9001 == bank) ]['consumer_revenue']))/new_lending  
                    lag_rate =  (np.float(df[ (df.date==df.date.unique()[at+1]) & (df.RSSD9001 == bank) ]['consumer_revenue']) - ( (1-am_rate)*(1-default_rate) )*np.float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['consumer_revenue']))/new_lending  
                
                except:
                    new_lending = np.nan
                    new_rate = np.nan
                    lag_rate = np.nan
                    agg_rev = 0
                    default_rate = 0
    
                # record new lending, rate and period revenues                                                                                                                       
                df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'new_consumer_loans'] = new_lending
                df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'consumer_rate']      = new_rate
                df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'consumer_rate_lagged']      = lag_rate
                df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'consumer_default_rate']   = default_rate

            #if not last quarter of fiscal year
            if quart < 3:
                quart = quart + 1
            else:
                quart = 0

# plot quantities of new lending
agg_issuance = []
spot_rate = []
agg_issuance_rate = []
default_rate = []
total_lending= []

spot_rate_lagged = []

for at,t in enumerate(df.date.unique()):
    
    agg_issuance.append( np.nansum(df[df.date==t]['new_consumer_loans'])/(1000*1000) )
    agg_issuance_rate.append( 100*np.nansum(df[df.date==t]['new_consumer_loans'])/np.nansum(df[df.date==t]['consumer_loans']) )
    total_lending.append( np.nansum(df[df.date==t]['consumer_loans'])/(1000*1000) )

    # record average default rate, weighted by market share
    temp_default = 0 
    temp_agg     = 0
    agg_loans = np.nansum(df[df.date==t]['new_consumer_loans'])
    
    if agg_loans <= 0:
        default_rate.append(0)
    else: 
        for idx, bank in enumerate( df.RSSD9001.unique() ):                
            try:
                if (np.float(df[(df.date==t) & (df.RSSD9001 == bank)]['new_consumer_loans'])*0 == 0): # not handling ==np.nan well
                    
                    if np.float(df[(df.date==t) & (df.RSSD9001 == bank)]['new_consumer_loans']) > 0:
                        temp_default = temp_default + np.float(df[(df.date==t) & (df.RSSD9001 == bank)]['consumer_default_rate'])*np.float(df[(df.date==t) & (df.RSSD9001 == bank)]['new_consumer_loans'])
                        temp_agg     = temp_agg     + np.float(df[(df.date==t) & (df.RSSD9001 == bank)]['new_consumer_loans'])
            except:
                pass 
        default_rate.append( 100*temp_default/temp_agg )
        
    # record average spot rate, weighted by market share
    temp_rate = 0 
    temp_agg     = 0
    agg_loans = np.nansum(df[df.date==t]['new_consumer_loans'])
    
    if (agg_loans <= 0) or (np.nansum(df[(df.date==t)]['consumer_rate']) <= 0):
        spot_rate.append(0)
    else: 
        for idx, bank in enumerate( df.RSSD9001.unique() ):                
            try:
                if (np.float(df[(df.date==t) & (df.RSSD9001 == bank)]['new_consumer_loans'])*0 == 0) and (np.float(df[(df.date==t) & (df.RSSD9001 == bank)]['consumer_rate'])*0 == 0): # not handling ==np.nan well
                    
                    if np.float(df[(df.date==t) & (df.RSSD9001 == bank)]['new_consumer_loans']) > 0:
                        temp_rate = temp_rate + np.float(df[(df.date==t) & (df.RSSD9001 == bank)]['consumer_rate'])*np.float(df[(df.date==t) & (df.RSSD9001 == bank)]['new_consumer_loans'])
                        temp_agg  = temp_agg     + np.float(df[(df.date==t) & (df.RSSD9001 == bank)]['new_consumer_loans'])
            except:
                pass 
        spot_rate.append( temp_rate/temp_agg )

    # record average spot rate, weighted by market share
    temp_rate = 0 
    temp_agg     = 0
    agg_loans = np.nansum(df[df.date==t]['new_consumer_loans'])
    
    if (agg_loans <= 0) or (np.nansum(df[(df.date==t)]['consumer_rate_lagged']) <= 0):
        spot_rate_lagged.append(0)
    else: 
        for idx, bank in enumerate( df.RSSD9001.unique() ):                
            try:
                if (np.float(df[(df.date==t) & (df.RSSD9001 == bank)]['new_consumer_loans'])*0 == 0) and (np.float(df[(df.date==t) & (df.RSSD9001 == bank)]['consumer_rate_lagged'])*0 == 0): # not handling ==np.nan well
                    
                    if np.float(df[(df.date==t) & (df.RSSD9001 == bank)]['new_consumer_loans']) > 0:
                        temp_rate = temp_rate + np.float(df[(df.date==t) & (df.RSSD9001 == bank)]['consumer_rate_lagged'])*np.float(df[(df.date==t) & (df.RSSD9001 == bank)]['new_consumer_loans'])
                        temp_agg  = temp_agg     + np.float(df[(df.date==t) & (df.RSSD9001 == bank)]['new_consumer_loans'])
            except:
                pass 
        spot_rate_lagged.append( temp_rate/temp_agg )

# create market shares for consumer loan issuance (treat negative issuance as zero)
df['consumer_market_share'] = 0

# for each time period
for at,t in enumerate(df.date.unique()):
    
    # compute total market lending
    # initialize agg lending variable 
    temp_agg_lend = 0
    
    # for each bank
    for idx,bank in enumerate(df.RSSD9001.unique()):
    
        # if loan issuance is strictly positive, add to temp variable
        try:
            if np.float(df[ (df.date == t) & (df.RSSD9001 == bank)]['new_consumer_loans']) > 0:
                temp_agg_lend = temp_agg_lend + np.float(df[ (df.date == t) & (df.RSSD9001 == bank)]['new_consumer_loans'])
        except:
            pass 
        
    # compute market shares
    if temp_agg_lend > 0:
        # for each bank 
        for idx,bank in enumerate(df.RSSD9001.unique()):    
        
            # if loan issuance is positive, divide lending by agg lending variable, record in dataframe
            try:
                if np.float(df[ (df.date == t) & (df.RSSD9001 == bank)]['new_consumer_loans']) > 0:
                    
                    df.loc[ (df.date == t) & (df.RSSD9001 == bank), 'consumer_market_share'] = 100*np.float(df[ (df.date == t) & (df.RSSD9001 == bank)]['new_consumer_loans'])/temp_agg_lend
            except:
                df.loc[ (df.date == t) & (df.RSSD9001 == bank), 'consumer_market_share'] = 0
                
    else:
        df.loc[(df.date == t), 'consumer_market_share' ] = 0

plt.close('all')
fig,ax1 = plt.subplots()
ax2 = ax1.twinx()
ax1.plot(df.date.unique(),total_lending,lw=3,label='Total Lending')
ax2.plot(df.date.unique(),agg_issuance,lw=3,label='New Issuance',color='green',ls='--')
ax1.set_xlabel('Date',fontsize=15)
ax1.set_ylabel('Lending ($, Billion)',fontsize=15,color='blue')
ax2.set_ylabel('New Issuance ($, Billion)',fontsize=15,color='green')
ax1.set_title('Total Stock of Consumer Loans and New Issuance',fontsize=20)

plt.figure(2)
plt.plot(df.date.unique(),agg_issuance_rate,lw=3)
plt.title('New Consumer Loan Issuance as % of Loan Stock',fontsize=20)
plt.xlabel('Date',fontsize=15)
plt.ylabel('Loan Issuance %',fontsize=15)

plt.figure(3)
plt.plot(df.date.unique(),default_rate,lw=3)
plt.title('Consumer Loan Default Rate (Market Share-Weighted)',fontsize=20)
plt.xlabel('Date',fontsize=15)
plt.ylabel('Default Rate (%)',fontsize=15)

plt.figure(4)
plt.plot(df.date.unique(),spot_rate,lw=3,label='spot')
plt.plot(df.date.unique(),spot_rate_lagged,lw=3,label='lagged')
plt.title('Consumer Loan Spot Rate (Market Share-Weighted)',fontsize=20)
plt.xlabel('Date',fontsize=15)
plt.ylabel('Spot Rate',fontsize=15)
plt.legend()

# plot all cross-sectional issuance, market shares of (positive) issuance, spot rates, default rates
plt.figure(5)
[plt.plot(df[(df.RSSD9001 == bank)]['date'],df[(df.RSSD9001 == bank)]['new_consumer_loans']/(1000*1000),lw=2) for idx,bank in enumerate( df.RSSD9001.unique() )]
plt.xlabel('Date',fontsize=15)
plt.ylabel('New Consumer Issuance ($, Billion)',fontsize=15)
plt.title('Panel Series for New Consumer Loan Issuance',fontsize=20)

plt.figure(6)
plt.subplot(2,1,1)
[plt.plot(df[(df.RSSD9001 == bank)]['date'],df[(df.RSSD9001 == bank)]['consumer_rate'],lw=2) for idx,bank in enumerate( df.RSSD9001.unique() )]
plt.xlabel('Date',fontsize=15)
plt.ylabel('Spot Rates',fontsize=15)
plt.title('Consumer Loan Spot Rates',fontsize=20)
plt.subplot(2,1,2)
[plt.plot(df[(df.RSSD9001 == bank)]['date'],df[(df.RSSD9001 == bank)]['consumer_rate_lagged'],lw=2) for idx,bank in enumerate( df.RSSD9001.unique() )]
plt.xlabel('Date',fontsize=15)
plt.ylabel('Spot Rates',fontsize=15)
plt.title('Consumer Loan Spot Rates (Lagged)',fontsize=20)

plt.figure(7)
[plt.plot(df[(df.RSSD9001 == bank)]['date'],100*df[(df.RSSD9001 == bank)]['consumer_default_rate'],lw=2) for idx,bank in enumerate( df.RSSD9001.unique() )]
plt.xlabel('Date',fontsize=15)
plt.ylabel('Consumer Default Rates (%)',fontsize=15)
plt.title('Panel Series for Consumer Loan Default Rates',fontsize=20)

plt.figure(8)
[plt.plot(df[(df.RSSD9001 == bank)]['date'],df[(df.RSSD9001 == bank)]['consumer_market_share']) for idx,bank in enumerate( df.RSSD9001.unique() )]
plt.xlabel('Date',fontsize=15)
plt.ylabel('Market Shares (%)',fontsize=15)
plt.title('Panel Series for Consumer Loan Market Shares',fontsize=20)

#-----------------------#
#                       #
#   Commercial Loans    #
#                       #
#-----------------------#
# create commercial loan quantity series
df['commercial_loans'] = (df['BHCKF158'] + df['BHCKF159'] + df['BHDM1420'] + df['BHDM1975'] + df['BHDM1460'] + df['BHCKF160'] +
                          df['BHCKF161'] + df['BHCK1292'] + df['BHCK1296'] + df['BHCK1590'] + df['BHDM1766'] + df['BHDMJ454'] +
                          df['BHDM1545']  + df['BHDM2165'] + df['BHDMKX57'] )

df['commercial_loan_nco'] = ( ( df['BHCKC891'] + df['BHCKC893'] + df['BHCK3584'] + df['BHCK3588'] + df['BHCKC895'] + df['BHCKC897'] +
                                df['BHCK4655'] + df['BHCK4645'] + df['BHCKB514'] + df['BHCKK129'] + df['BHCKK205'] + df['BHCK4644'] +
                                df['BHCKF185'] + df['BHCKC880'] + df['BHCKKX50'] ) -
                              ( df['BHCKC892'] + df['BHCKC894'] + df['BHCK3585'] + df['BHCK3589'] + df['BHCKC896'] + df['BHCKC898'] +
                                df['BHCK4665'] + df['BHCK4617'] + df['BHCKB515'] + df['BHCKK133'] + df['BHCKK206'] + df['BHCK4628'] +
                                df['BHCKF187'] + df['BHCKF188'] + df['BHCKKX51'] ) )

df['new_commercial_loans'] = np.nan
df['commercial_rate']      = np.nan
df['commercial_rate_lagged']      = np.nan
df['commercial_revenue']   = np.nan
df['commercial_default_rate']   = np.nan

am_rate_com = 1/10  # commercial repayment rate

# first compute quartlery revenue for each bank, each quarter
for idx, bank in enumerate( df.RSSD9001.unique() ):
    
    quart = 3
    
    for at, t in enumerate( df.date.unique() ):
        if at ==0:
            try:
                df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'commercial_revenue']   = (1/3)*( np.float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4436']) +
                                  np.float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKF821']) +
                                  np.float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4065']) +
                                  np.float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4115']) )
            except:
                pass
        else:
            if quart == 0:
                try:
                    df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'commercial_revenue']   = (   np.float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4436']) +
                                  np.float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKF821']) +
                                  np.float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4065']) +
                                  np.float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4115']) )
                except:
                    pass 
            else:
                try:
                    df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'commercial_revenue']   = ((   np.float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4436']) +
                                  np.float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKF821']) +
                                  np.float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4065']) +
                                  np.float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4115']) ) - 
                                  
                                ( np.float(df[ (df.date==df.date.unique()[at-1]) & (df.RSSD9001 == bank) ]['BHCK4436']) +
                                  np.float(df[ (df.date==df.date.unique()[at-1]) & (df.RSSD9001 == bank) ]['BHCKF821']) +
                                  np.float(df[ (df.date==df.date.unique()[at-1]) & (df.RSSD9001 == bank) ]['BHCK4065']) +
                                  np.float(df[ (df.date==df.date.unique()[at-1]) & (df.RSSD9001 == bank) ]['BHCK4115']) ) )
                except:
                    pass
                
            if quart < 3:
                quart = quart + 1
            else:
                quart = 0


# for each bank
for idx, bank in enumerate( df.RSSD9001.unique() ):

    print('Bank ',idx,' out of ',len(df.RSSD9001.unique()) )

    # initialize multiplier
    quart = 3  # first observed quarter is Q3 for 1986
    
    # for each time period 
    for at, t in enumerate( df.date.unique() ):
            
        # compute default rate
            # sum of charge-offs (time t)/ sum of loans (t-1)
        if at == 0:  # first period observed is 1986 Q3; can only use contemporaneous values
        
            try:
                # default rate 
                default_rate = (1/3)*( np.float(df[ (df.date ==t) & (df.RSSD9001 == bank)]['commercial_loan_nco'])/
                                       np.float(df[ (df.date ==t) & (df.RSSD9001 == bank)]['commercial_loans']) )
                
                # new lending 
                new_lending = ( np.float(df[ (df.date ==t) & (df.RSSD9001 == bank)]['commercial_loans']) -
                                (1-am_rate_com)*(1-default_rate)*np.float(df[ (df.date ==t) & (df.RSSD9001 == bank)]['commercial_loans']) )  
    
                # new rate
                agg_rev = (1/3)*( np.float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4436']) +
                                  np.float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKF821']) +
                                  np.float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4065']) +
                                  np.float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4115']) )
                
                new_rate =  (agg_rev - ( (1-am_rate_com)*(1-default_rate) )*agg_rev)/new_lending  
                lag_rate =  (np.float(df[ (df.date==df.date.unique()[at+1]) & (df.RSSD9001 == bank) ]['commercial_revenue']) - ( (1-am_rate_com)*(1-default_rate) )*np.float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['commercial_revenue']))/new_lending  
                
            except:
                new_lending = np.nan
                new_rate = np.nan
                lag_rate = np.nan
                agg_rev = 0
                default_rate = 0
                
            # record new lending, rate and period revenues                                                                                                                       
            df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'new_commercial_loans'] = new_lending
            df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'commercial_rate']      = new_rate
            df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'commercial_rate_lagged']      = lag_rate
            df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'commercial_revenue']   = agg_rev
            df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'commercial_default_rate']   = default_rate
            
        else:

            if quart == 0:
                
                try:
                    default_rate = ( np.float(df[ (df.date ==t) & (df.RSSD9001 == bank)]['commercial_loan_nco'])/
                                     np.float(df[ (df.date ==df.date.unique()[at-1]) & (df.RSSD9001 == bank)]['commercial_loans']) )
        
                    new_lending = ( np.float(df[ (df.date ==t) & (df.RSSD9001 == bank)]['commercial_loans']) -
                                    (1-am_rate_com)*(1-default_rate)*np.float(df[ (df.date ==df.date.unique()[at-1]) & (df.RSSD9001 == bank)]['commercial_loans']) )  
                    
                    # new rate
                    agg_rev = (   np.float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4436']) +
                                  np.float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKF821']) +
                                  np.float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4065']) +
                                  np.float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4115']) )
                    
                    new_rate =  (agg_rev - ( (1-am_rate_com)*(1-default_rate) )*np.float(df[ (df.date==df.date.unique()[at-1]) & (df.RSSD9001 == bank) ]['commercial_revenue']))/new_lending  

                    lag_rate =  (np.float(df[ (df.date==df.date.unique()[at+1]) & (df.RSSD9001 == bank) ]['commercial_revenue']) - ( (1-am_rate_com)*(1-default_rate) )*np.float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['commercial_revenue']))/new_lending  
                
                except:
                    new_lending = np.nan
                    new_rate = np.nan
                    lag_rate = np.nan
                    agg_rev = 0
                    default_rate = 0

                # record new lending, rate and period revenues                                                                                                                       
                df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'new_commercial_loans'] = new_lending
                df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'commercial_rate']      = new_rate
                df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'commercial_rate_lagged']      = lag_rate
                df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'commercial_revenue']   = agg_rev
                df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'commercial_default_rate']   = default_rate

            else:
                
                try:
                    default_rate = ( (np.float(df[ (df.date ==t) & (df.RSSD9001 == bank)]['commercial_loan_nco']) -
                                      np.float(df[ (df.date ==df.date.unique()[at-1]) & (df.RSSD9001 == bank)]['commercial_loan_nco']))/
                                               np.float(df[ (df.date ==df.date.unique()[at-1]) & (df.RSSD9001 == bank)]['commercial_loans']) )
        
                    new_lending = ( np.float(df[ (df.date ==t) & (df.RSSD9001 == bank)]['commercial_loans']) -
                                    (1-am_rate_com)*(1-default_rate)*np.float(df[ (df.date ==df.date.unique()[at-1]) & (df.RSSD9001 == bank)]['commercial_loans']) )  
                    
                    # new rate
                    agg_rev =((   np.float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4436']) +
                                  np.float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKF821']) +
                                  np.float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4065']) +
                                  np.float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4115']) ) - 
                                  
                                ( np.float(df[ (df.date==df.date.unique()[at-1]) & (df.RSSD9001 == bank) ]['BHCK4436']) +
                                  np.float(df[ (df.date==df.date.unique()[at-1]) & (df.RSSD9001 == bank) ]['BHCKF821']) +
                                  np.float(df[ (df.date==df.date.unique()[at-1]) & (df.RSSD9001 == bank) ]['BHCK4065']) +
                                  np.float(df[ (df.date==df.date.unique()[at-1]) & (df.RSSD9001 == bank) ]['BHCK4115']) ) )
                                                  
                                        
                    new_rate =  (agg_rev - ( (1-am_rate_com)*(1-default_rate) )*np.float(df[ (df.date==df.date.unique()[at-1]) & (df.RSSD9001 == bank) ]['commercial_revenue']))/new_lending  
                    
                    lag_rate =  (np.float(df[ (df.date==df.date.unique()[at+1]) & (df.RSSD9001 == bank) ]['commercial_revenue']) - ( (1-am_rate_com)*(1-default_rate) )*np.float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['commercial_revenue']))/new_lending  

                except:
                    new_lending = np.nan
                    new_rate = np.nan
                    lag_rate = np.nan
                    agg_rev = 0
                    default_rate = 0
    
                # record new lending, rate and period revenues                                                                                                                       
                df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'new_commercial_loans'] = new_lending
                df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'commercial_rate']      = new_rate
                df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'commercial_rate_lagged']      = lag_rate
                df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'commercial_revenue']   = agg_rev
                df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'commercial_default_rate']   = default_rate

            #if not last quarter of fiscal year
            if quart < 3:
                quart = quart + 1
            else:
                quart = 0

# plot quantities of new commercial lending
agg_issuance = []
spot_rate = []
agg_issuance_rate = []
default_rate = []
total_lending= []

spot_rate_lagged = []

for at,t in enumerate(df.date.unique()):
    
    agg_issuance.append( np.nansum(df[df.date==t]['new_commercial_loans'])/(1000*1000) )
    agg_issuance_rate.append( 100*np.nansum(df[df.date==t]['new_commercial_loans'])/np.nansum(df[df.date==t]['commercial_loans']) )
    total_lending.append( np.nansum(df[df.date==t]['commercial_loans'])/(1000*1000) )

    # record average default rate, weighted by market share
    temp_default = 0 
    temp_agg     = 0
    agg_loans = np.nansum(df[df.date==t]['new_commercial_loans'])
    
    if agg_loans <= 0:
        default_rate.append(0)
    else: 
        for idx, bank in enumerate( df.RSSD9001.unique() ):                
            try:
                if (np.float(df[(df.date==t) & (df.RSSD9001 == bank)]['new_commercial_loans'])*0 == 0): # not handling ==np.nan well
                    
                    if np.float(df[(df.date==t) & (df.RSSD9001 == bank)]['new_commercial_loans']) > 0:
                        temp_default = temp_default + np.float(df[(df.date==t) & (df.RSSD9001 == bank)]['commercial_default_rate'])*np.float(df[(df.date==t) & (df.RSSD9001 == bank)]['new_commercial_loans'])
                        temp_agg     = temp_agg     + np.float(df[(df.date==t) & (df.RSSD9001 == bank)]['new_commercial_loans'])
            except:
                pass 
        default_rate.append( 100*temp_default/temp_agg )
        
    # record average spot rate, weighted by market share
    temp_rate = 0 
    temp_agg     = 0
    agg_loans = np.nansum(df[df.date==t]['new_commercial_loans'])
    
    if (agg_loans <= 0) or (np.nansum(df[(df.date==t)]['commercial_rate']) <= 0):
        spot_rate.append(0)
    else: 
        for idx, bank in enumerate( df.RSSD9001.unique() ):                
            try:
                if (np.float(df[(df.date==t) & (df.RSSD9001 == bank)]['new_commercial_loans'])*0 == 0) and (np.float(df[(df.date==t) & (df.RSSD9001 == bank)]['commercial_rate'])*0 == 0): # not handling ==np.nan well
                    
                    if np.float(df[(df.date==t) & (df.RSSD9001 == bank)]['new_commercial_loans']) > 0:
                        temp_rate = temp_rate + np.float(df[(df.date==t) & (df.RSSD9001 == bank)]['commercial_rate'])*np.float(df[(df.date==t) & (df.RSSD9001 == bank)]['new_commercial_loans'])
                        temp_agg  = temp_agg     + np.float(df[(df.date==t) & (df.RSSD9001 == bank)]['new_commercial_loans'])
            except:
                pass 
        spot_rate.append( temp_rate/temp_agg )

    # record average spot rate, weighted by market share
    temp_rate = 0 
    temp_agg     = 0
    agg_loans = np.nansum(df[df.date==t]['new_commercial_loans'])
    
    if (agg_loans <= 0) or (np.nansum(df[(df.date==t)]['commercial_rate_lagged']) <= 0):
        spot_rate_lagged.append(0)
    else: 
        for idx, bank in enumerate( df.RSSD9001.unique() ):                
            try:
                if (np.float(df[(df.date==t) & (df.RSSD9001 == bank)]['new_commercial_loans'])*0 == 0) and (np.float(df[(df.date==t) & (df.RSSD9001 == bank)]['commercial_rate_lagged'])*0 == 0): # not handling ==np.nan well
                    
                    if np.float(df[(df.date==t) & (df.RSSD9001 == bank)]['new_commercial_loans']) > 0:
                        temp_rate = temp_rate + np.float(df[(df.date==t) & (df.RSSD9001 == bank)]['commercial_rate_lagged'])*np.float(df[(df.date==t) & (df.RSSD9001 == bank)]['new_commercial_loans'])
                        temp_agg  = temp_agg     + np.float(df[(df.date==t) & (df.RSSD9001 == bank)]['new_commercial_loans'])
            except:
                pass 
        spot_rate_lagged.append( temp_rate/temp_agg )

# create market shares for consumer loan issuance (treat negative issuance as zero)
df['commercial_market_share'] = 0

# for each time period
for at,t in enumerate(df.date.unique()):
    
    # compute total market lending
    # initialize agg lending variable 
    temp_agg_lend = 0
    
    # for each bank
    for idx,bank in enumerate(df.RSSD9001.unique()):
    
        # if loan issuance is strictly positive, add to temp variable
        try:
            if np.float(df[ (df.date == t) & (df.RSSD9001 == bank)]['new_commercial_loans']) > 0:
                temp_agg_lend = temp_agg_lend + np.float(df[ (df.date == t) & (df.RSSD9001 == bank)]['new_commercial_loans'])
        except:
            pass 
        
    # compute market shares
    if temp_agg_lend > 0:
        # for each bank 
        for idx,bank in enumerate(df.RSSD9001.unique()):    
        
            # if loan issuance is positive, divide lending by agg lending variable, record in dataframe
            try:
                if np.float(df[ (df.date == t) & (df.RSSD9001 == bank)]['new_commercial_loans']) > 0:
                    
                    df.loc[ (df.date == t) & (df.RSSD9001 == bank), 'commercial_market_share'] = 100*np.float(df[ (df.date == t) & (df.RSSD9001 == bank)]['new_commercial_loans'])/temp_agg_lend
            except:
                df.loc[ (df.date == t) & (df.RSSD9001 == bank), 'commercial_market_share'] = 0
                
    else:
        df.loc[(df.date == t), 'commercial_market_share' ] = 0

plt.close('all')
fig,ax1 = plt.subplots()
ax2 = ax1.twinx()
ax1.plot(df.date.unique(),total_lending,lw=3,label='Total Lending')
ax2.plot(df.date.unique(),agg_issuance,lw=3,label='New Issuance',color='green',ls='--')
ax1.set_xlabel('Date',fontsize=15)
ax1.set_ylabel('Lending ($, Billion)',fontsize=15,color='blue')
ax2.set_ylabel('New Issuance ($, Billion)',fontsize=15,color='green')
ax1.set_title('Total Stock of Commercial Loans and New Issuance',fontsize=20)

plt.figure(2)
plt.plot(df.date.unique(),agg_issuance_rate,lw=3)
plt.title('New Commercial Loan Issuance as % of Loan Stock',fontsize=20)
plt.xlabel('Date',fontsize=15)
plt.ylabel('Loan Issuance %',fontsize=15)

plt.figure(3)
plt.plot(df.date.unique(),default_rate,lw=3)
plt.title('Commercial Loan Default Rate (Market Share-Weighted)',fontsize=20)
plt.xlabel('Date',fontsize=15)
plt.ylabel('Default Rate (%)',fontsize=15)

plt.figure(4)
plt.plot(df.date.unique(),spot_rate,lw=3,label='spot')
plt.plot(df.date.unique(),spot_rate_lagged,lw=3,label='lagged')
plt.title('Commercial Loan Spot Rate (Market Share-Weighted)',fontsize=20)
plt.xlabel('Date',fontsize=15)
plt.ylabel('Spot Rate',fontsize=15)
plt.legend()

# plot all cross-sectional issuance, market shares of (positive) issuance, spot rates, default rates
plt.figure(5)
[plt.plot(df[(df.RSSD9001 == bank)]['date'],df[(df.RSSD9001 == bank)]['new_commercial_loans']/(1000*1000),lw=2) for idx,bank in enumerate( df.RSSD9001.unique() )]
plt.xlabel('Date',fontsize=15)
plt.ylabel('New Commercial Issuance ($, Billion)',fontsize=15)
plt.title('Panel Series for New Consumer Loan Issuance',fontsize=20)

plt.figure(6)
plt.subplot(2,1,1)
[plt.plot(df[(df.RSSD9001 == bank)]['date'],df[(df.RSSD9001 == bank)]['commercial_rate'],lw=2) for idx,bank in enumerate( df.RSSD9001.unique() )]
plt.xlabel('Date',fontsize=15)
plt.ylabel('Spot Rates',fontsize=15)
plt.title('Commercial Loan Spot Rates',fontsize=20)
plt.subplot(2,1,2)
[plt.plot(df[(df.RSSD9001 == bank)]['date'],df[(df.RSSD9001 == bank)]['commercial_rate_lagged'],lw=2) for idx,bank in enumerate( df.RSSD9001.unique() )]
plt.xlabel('Date',fontsize=15)
plt.ylabel('Spot Rates',fontsize=15)
plt.title('Commercial Loan Spot Rates (Lagged)',fontsize=20)

plt.figure(7)
[plt.plot(df[(df.RSSD9001 == bank)]['date'],100*df[(df.RSSD9001 == bank)]['commercial_default_rate'],lw=2) for idx,bank in enumerate( df.RSSD9001.unique() )]
plt.xlabel('Date',fontsize=15)
plt.ylabel('Commercial Default Rates (%)',fontsize=15)
plt.title('Panel Series for Commercial Loan Default Rates',fontsize=20)

plt.figure(8)
[plt.plot(df[(df.RSSD9001 == bank)]['date'],df[(df.RSSD9001 == bank)]['commercial_market_share']) for idx,bank in enumerate( df.RSSD9001.unique() )]
plt.xlabel('Date',fontsize=15)
plt.ylabel('Market Shares (%)',fontsize=15)
plt.title('Panel Series for Commercial Loan Market Shares',fontsize=20)

#----------------------------------#
#                                  #
#   Deposits and Other Expenses    #
#                                  #
#----------------------------------#
df['total_deposits'] = df['BHDM6631'] + df['BHDM6636']
df['deposit_expense']     = np.nan

### Cost Series (cumulative) ###
df['salaries_cum'] = df['BHCK4135']
df['premises_cost_cum'] = df['BHCK4217']
df['other_cost_cum'] = df['BHCK4092']
df['total_cost_cum'] = df['BHCK4093']

df['salaries'] =  np.nan
df['premises_cost'] = np.nan
df['other_cost'] = np.nan
df['total_cost'] = np.nan

# compute quarterly deposit interest expense
for idx, bank in enumerate( df.RSSD9001.unique() ):

    print('Bank ',idx,' out of ',len(df.RSSD9001.unique()) )

    # initialize multiplier
    quart = 3  # first observed quarter is Q3 for 1986

    for at, t in enumerate( df.date.unique() ):

        if at == 0:  # first period observed is 1986 Q3; annualize by multiplying by 4/3
            df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'deposit_expense' ] = (4/3)*( df[ (df.date ==t) & (df.RSSD9001 == bank) ]['BHCK4174' ] +
                                                                                        df[ (df.date ==t) & (df.RSSD9001 == bank) ]['BHCK6760' ] +
                                                                                        df[ (df.date ==t) & (df.RSSD9001 == bank) ]['BHCK4176' ] +
                                                                                        df[ (df.date ==t) & (df.RSSD9001 == bank) ]['BHCK6761' ] )


            df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'salaries' ] = (4/3)*df[ (df.date==t) & (df.RSSD9001 == bank) ]['salaries_cum']
            df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'premises_cost' ] = (4/3)*df[ (df.date==t) & (df.RSSD9001 == bank) ]['premises_cost_cum']

            df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'other_cost' ] = (4/3)*df[ (df.date==t) & (df.RSSD9001 == bank) ]['other_cost_cum']
            df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'total_cost' ] = (4/3)*df[ (df.date==t) & (df.RSSD9001 == bank) ]['total_cost_cum']

        else:

            if quart == 0: # if Q1, annualize by multiplying by 4

                if t <= np.datetime64('1996-12-31T00:00:00.000000000'):
                    df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'deposit_expense' ] =4*( df[ (df.date ==t) & (df.RSSD9001 == bank) ]['BHCK4174' ] +
                                                                                           df[ (df.date ==t) & (df.RSSD9001 == bank) ]['BHCK6760' ] +
                                                                                           df[ (df.date ==t) & (df.RSSD9001 == bank) ]['BHCK4176' ] +
                                                                                           df[ (df.date ==t) & (df.RSSD9001 == bank) ]['BHCK6761' ] )

                elif t <= np.datetime64('2016-12-31T00:00:00.000000000'):
                    df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'deposit_expense' ] =4*( df[ (df.date ==t) & (df.RSSD9001 == bank) ]['BHCKA517' ] +
                                                                                           df[ (df.date ==t) & (df.RSSD9001 == bank) ]['BHCKA518' ] +
                                                                                           df[ (df.date ==t) & (df.RSSD9001 == bank) ]['BHCK6761' ] )
                else:
                    df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'deposit_expense' ] =4*( df[ (df.date ==t) & (df.RSSD9001 == bank) ]['BHCKHK03' ] +
                                                                                           df[ (df.date ==t) & (df.RSSD9001 == bank) ]['BHCKHK04' ] +
                                                                                           df[ (df.date ==t) & (df.RSSD9001 == bank) ]['BHCK6761' ] )

                df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'salaries' ] = 4*df[ (df.date==t) & (df.RSSD9001 == bank) ]['salaries_cum']
                df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'premises_cost' ] = 4*df[ (df.date==t) & (df.RSSD9001 == bank) ]['premises_cost_cum']

                df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'other_cost' ] = 4*df[ (df.date==t) & (df.RSSD9001 == bank) ]['other_cost_cum']
                df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'total_cost' ] = 4*df[ (df.date==t) & (df.RSSD9001 == bank) ]['total_cost_cum']

            else: # if (Q2,Q3,Q4), compute newly accrued expenses, then multiply by 4

                if t <= np.datetime64('1996-12-31T00:00:00.000000000'):
                    try:
                        df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'deposit_expense' ] =4*( np.float( df[ (df.date ==t) & (df.RSSD9001 == bank) ]['BHCK4174' ] +
                                                                                                  df[ (df.date ==t) & (df.RSSD9001 == bank) ]['BHCK6760' ] +
                                                                                                  df[ (df.date ==t) & (df.RSSD9001 == bank) ]['BHCK4176' ] +
                                                                                                  df[ (df.date ==t) & (df.RSSD9001 == bank) ]['BHCK6761' ] ) -
                                                                        np.float( df[ (df.date == df.date.unique()[at-1]) & (df.RSSD9001 == bank) ]['BHCK4174' ] +
                                                                          df[ (df.date == df.date.unique()[at-1]) & (df.RSSD9001 == bank) ]['BHCK6760' ] +
                                                                          df[ (df.date == df.date.unique()[at-1]) & (df.RSSD9001 == bank) ]['BHCK4176' ] +
                                                                          df[ (df.date == df.date.unique()[at-1]) & (df.RSSD9001 == bank) ]['BHCK6761' ] ) )
                    except:
                        df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'deposit_expense' ] = np.nan

                elif t <= np.datetime64('2016-12-31T00:00:00.000000000'):
                    try:
                        df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'deposit_expense' ] =4*( np.float( df[ (df.date ==t) & (df.RSSD9001 == bank) ]['BHCKA517' ] +
                                                                                                 df[ (df.date ==t) & (df.RSSD9001 == bank) ]['BHCKA518' ] +
                                                                                                 df[ (df.date ==t) & (df.RSSD9001 == bank) ]['BHCK6761' ] ) -
                                                                       np.float( df[ (df.date == df.date.unique()[at-1]) & (df.RSSD9001 == bank) ]['BHCKA517' ] +
                                                                         df[ (df.date == df.date.unique()[at-1]) & (df.RSSD9001 == bank) ]['BHCKA518' ] +
                                                                         df[ (df.date == df.date.unique()[at-1]) & (df.RSSD9001 == bank) ]['BHCK6761' ] ) )
                    except:
                        df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'deposit_expense' ] = np.nan
                else:
                    try:
                        df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'deposit_expense' ] =4*( np.float( df[ (df.date ==t) & (df.RSSD9001 == bank) ]['BHCKHK03' ] +
                                                                                                 df[ (df.date ==t) & (df.RSSD9001 == bank) ]['BHCKHK04' ] +
                                                                                                 df[ (df.date ==t) & (df.RSSD9001 == bank) ]['BHCK6761' ] ) -
                                                                        np.float( df[ (df.date == df.date.unique()[at-1]) & (df.RSSD9001 == bank) ]['BHCKHK03' ] +
                                                                          df[ (df.date == df.date.unique()[at-1]) & (df.RSSD9001 == bank) ]['BHCKHK04' ] +
                                                                          df[ (df.date == df.date.unique()[at-1]) & (df.RSSD9001 == bank) ]['BHCK6761' ] )   )
                    except:
                        df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'deposit_expense' ] = np.nan


                try:
                    df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'salaries' ] = 4*(np.float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['salaries_cum']) - np.float(df[ (df.date==df.date.unique()[at-1]) & (df.RSSD9001 == bank) ]['salaries_cum']) )
                    df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'premises_cost' ] = 4*(np.float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['premises_cost_cum']) - np.float(df[ (df.date==df.date.unique()[at-1]) & (df.RSSD9001 == bank) ]['premises_cost_cum']) )
                    df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'other_cost' ] = 4*(np.float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['other_cost_cum']) - np.float(df[ (df.date==df.date.unique()[at-1]) & (df.RSSD9001 == bank) ]['other_cost_cum']) )
                    df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'total_cost' ] = 4*(np.float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['total_cost_cum']) - np.float(df[ (df.date==df.date.unique()[at-1]) & (df.RSSD9001 == bank) ]['total_cost_cum']) )

                except:
                    df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'salaries' ] = np.nan
                    df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'premises_cost' ] = np.nan
                    df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'other_cost' ] = np.nan
                    df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'total_cost' ] = np.nan

            #if not last quarter of fiscal year
            if quart < 3:
                quart = quart + 1
            else:
                quart = 0

# define return/rate series
df['deposit_rate'] = df['deposit_expense']/df['total_deposits']

# compute deposit market shares 
df['deposit_market_share'] = 0

# for each time period
for at,t in enumerate(df.date.unique()):
    
    # compute total market lending
    agg_dep = np.nansum( df[ (df.date == t) ]['total_deposits'] )
            
    # compute market shares
    if agg_dep > 0:
        # for each bank 
        for idx,bank in enumerate(df.RSSD9001.unique()):    
        
            # if loan issuance is positive, divide lending by agg lending variable, record in dataframe
            try:
                if np.float(df[ (df.date == t) & (df.RSSD9001 == bank)]['total_deposits']) > 0:
                    
                    df.loc[ (df.date == t) & (df.RSSD9001 == bank), 'deposit_market_share'] = 100*np.float(df[ (df.date == t) & (df.RSSD9001 == bank)]['total_deposits'])/agg_dep
            except:
                df.loc[ (df.date == t) & (df.RSSD9001 == bank), 'deposit_market_share'] = 0
                
    else:
        df.loc[(df.date == t), 'deposit_market_share' ] = 0

total_deposits = []
for at,t in enumerate(df.date.unique()):
    try:
        total_deposits.append( np.nansum(df[df.date==t]['total_deposits'])/(1000*1000) )
    except:
        total_deposits.append(0)

plt.close('all')
plt.figure(1)
plt.plot(df.date.unique(),total_deposits,lw=3)
plt.xlabel('Date',fontsize=15)
plt.ylabel('Deposits ($, Billion)',fontsize=15)
plt.title('Total Stock of Bank Deposits',fontsize=20)

dep_spot_rate = []
for at,t in enumerate(df.date.unique()):
    try:
        dep_spot_rate.append( np.nansum(df[df.date==t]['deposit_expense'])/np.nansum(df[df.date==t]['total_deposits']) )
    except:
        dep_spot_rate.append(0)
        
plt.figure(2)
plt.plot(df.date.unique(),dep_spot_rate,lw=3,label='spot')
plt.title('Deposit Spot Rate (Market Share-Weighted)',fontsize=20)
plt.xlabel('Date',fontsize=15)
plt.ylabel('Spot Rate',fontsize=15)
plt.legend()

# plot all cross-sectional issuance, market shares of (positive) issuance, spot rates, default rates
plt.figure(3)
[plt.plot(df[(df.RSSD9001 == bank)]['date'],df[(df.RSSD9001 == bank)]['total_deposits']/(1000*1000),lw=2) for idx,bank in enumerate( df.RSSD9001.unique() )]
plt.xlabel('Date',fontsize=15)
plt.ylabel('Deposits ($, Billion)',fontsize=15)
plt.title('Panel Series for Bank Deposits',fontsize=20)

plt.figure(4)
[plt.plot(df[(df.RSSD9001 == bank)]['date'],df[(df.RSSD9001 == bank)]['deposit_rate'],lw=2) for idx,bank in enumerate( df.RSSD9001.unique() )]
plt.xlabel('Date',fontsize=15)
plt.ylabel('Deposit Spot Rates',fontsize=15)
plt.title('Bank Deposit Spot Rates',fontsize=20)

plt.figure(5)
[plt.plot(df[(df.RSSD9001 == bank)]['date'],df[(df.RSSD9001 == bank)]['deposit_market_share']) for idx,bank in enumerate( df.RSSD9001.unique() )]
plt.xlabel('Date',fontsize=15)
plt.ylabel('Market Shares (%)',fontsize=15)
plt.title('Panel Series for Deposit Market Shares',fontsize=20)

#------------------#
#                  # 
#   Data Output    #
#                  # 
#------------------#

### Output Aggregate Quantity Date by Quarter for Total Market Size ####
    # this has market shares, for quantities again it would be 'total_deposits','new_consumer_loans','new_commercial_loans'
    # but some of the loan entries will have negative values 
df[['date','deposit_market_share','consumer_market_share','commercial_market_share']].groupby('date').sum().to_csv("Data/MarketSizeByQuarter.csv")

# output a refined dataframe
    # this one now has spot rates and new issuance for loans and deposits (measured by market share)
df[['date','RSSD9001','total_assets','deposit_rate','consumer_rate','commercial_rate','deposit_market_share','consumer_market_share','commercial_market_share','salaries','premises_cost','other_cost','total_cost']].to_csv('Data/frdata_refined.csv')

#---------------------------#
#                           #
#   Statistical Analysis    #
#                           #
#---------------------------#


