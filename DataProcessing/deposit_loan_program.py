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

#### Limit to only banks of a certain size ####
##  Collect 20 Largest Banks in terms of (i) consumer loans (ii) commercial loans (iii) deposits and
##  (iv) insurance assets for each period.  There will be overlap but it's important to get the largest
##  firms for each product line in each period.   

# =============================================================================
# # initialize list of bank indices and threshold number N
# top_idx = []
# topN = 5 
# 
# # for each quarter
# for at,t in enumerate(df.date.unique()):
#     
#     # determine top N consumer lenders
#     con_idx = list( (df[df.date == t]['BHDM1797'] + df[df.date == t]['BHDM5367'] + df[df.date == t]['BHDM5368']).nlargest(topN).index )
#     
#     # determine top N commercial lenders
#     com_idx = list( (df[df.date == t]['BHCKF158'] + df[df.date == t]['BHCKF159'] + df[df.date == t]['BHDM1420'] + 
#                       df[df.date == t]['BHDM1975'] + df[df.date == t]['BHDM1460'] + df[df.date == t]['BHCKF160'] + 
#                       df[df.date == t]['BHCKF161'] + df[df.date == t]['BHCK1292'] + df[df.date == t]['BHCK1296'] + 
#                       df[df.date == t]['BHCK1590'] + df[df.date == t]['BHDM1766'] + df[df.date == t]['BHDMJ454'] + 
#                       df[df.date == t]['BHDM1545'] + df[df.date == t]['BHDM2165'] + df[df.date == t]['BHDMKX57']  
#                       ).nlargest(topN).index )
#         
#     # determine top N deposit takers
#     dep_idx = list( (df[df.date == t]['BHDM6631'] + df[df.date == t]['BHDM6636'] ).nlargest(topN).index )
#         
#     # determine top N insurance providers
#     ins_idx = list( (df[df.date == t]['BHCKC244'] + df[df.date == t]['BHCKC248'] ).nlargest(topN).index )
#     
#     # recover bank id's
#     con_list = []
#     com_list = []
#     dep_list = []
#     ins_list = []
#     
#     for i in range(topN):
#         try:
#             con_list.append( df[df.index == con_idx[i] ]['RSSD9001'].unique()[0] )
#         except:
#             pass 
#         
#         try:
#             com_list.append( df[df.index == com_idx[i] ]['RSSD9001'].unique()[0] )
#         except: 
#             pass
#         
#         try:
#             dep_list.append( df[df.index == dep_idx[i] ]['RSSD9001'].unique()[0] )
#         except:
#             pass
#         
#         try:
#             ins_list.append( df[df.index == ins_idx[i] ]['RSSD9001'].unique()[0] )
#         except:
#             pass 
#     
#     # append list with unique union set 
#     top_idx = list( set(con_list).union( set(com_list),set(dep_list),set(ins_list), set(top_idx) ) )
#     
# print('Collected a total of', len(top_idx),' bank IDs')
# 
# #create subset dataframe using bank id's
# for i in range(len(top_idx)):
# 
#     if i ==0:
#         temp_df = df[df.RSSD9001 == top_idx[i]]
#     else:
#         temp_df = temp_df.append( df[df.RSSD9001 == top_idx[i]] )
# 
# df = temp_df.copy()
#         
# =============================================================================
#---------------------# 
#                     #  
#   Consumer Loans    #
#                     #  
#---------------------#
print()
print()
print()
print('Consumer Loan Business Line')
print()
print()
print()

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
    
    quart = 1
    
    for at, t in enumerate( df.date.unique() ):
        if at ==0:
            try:
                df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'consumer_revenue']   = np.float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4435'])
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

    print('Consumer Bank ',idx,' out of ',len(df.RSSD9001.unique()) )

    # initialize multiplier
    quart = 1  # first observed quarter is Q1 for 2008
    
    # for each time period 
    for at, t in enumerate( df.date.unique() ):
            
        # compute default rate
            # sum of charge-offs (time t)/ sum of loans (t-1)
        if at == 0:  # first period observed is 1986 Q3; can only use contemporaneous values
        
            try:
                # default rate 
                default_rate = ( np.float(df[ (df.date ==t) & (df.RSSD9001 == bank)]['consumer_loan_nco'])/
                                       np.float(df[ (df.date ==t) & (df.RSSD9001 == bank)]['consumer_loans']) )
                
                # new lending 
                new_lending = ( np.float(df[ (df.date ==t) & (df.RSSD9001 == bank)]['consumer_loans']) -
                                (1-am_rate)*(1-default_rate)*np.float(df[ (df.date ==t) & (df.RSSD9001 == bank)]['consumer_loans']) )  
    
                # new rate
                agg_rev = np.float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4435'])
                
                new_rate =  (agg_rev - ( (1-am_rate)*(1-default_rate) )*np.float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4435']))/new_lending  
                lag_rate =  (np.float(df[ (df.date==df.date.unique()[at+1]) & (df.RSSD9001 == bank) ]['consumer_revenue']) - ( (1-am_rate)*(1-default_rate) )*np.float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['consumer_revenue']))/new_lending  
            except:
                new_lending = np.nan
                new_rate = np.nan
                lag_rate = np.nan
                default_rate = 0
                
            # don't allow negative lending
            if new_lending < 0:
                new_lending = 0
                
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

                # don't allow negative lending
                if new_lending < 0:
                    new_lending = 0

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

                # don't allow negative lending
                if new_lending < 0:
                    new_lending = 0
    
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

# compute market volume of lending each period
Consumer_Loan_Market = []
for at,t in enumerate(df.date.unique()):
    
    Consumer_Loan_Market.append( np.nansum( df.loc[df.date==t]['new_consumer_loans'] ) )
    
# compute market shares 
df['consumer_market_share'] = 0

# for each time period
for at,t in enumerate(df.date.unique()):
    
    temp_share = 0
    
    # compute market shares
    if Consumer_Loan_Market[at] > 0:
        # for each bank 
        for idx,bank in enumerate(df.RSSD9001.unique()):    
        
            # if loan issuance is positive, divide lending by agg lending variable, record in dataframe
            try:                    
                df.loc[ (df.date == t) & (df.RSSD9001 == bank), 'consumer_market_share'] = 100*np.float(df[ (df.date == t) & (df.RSSD9001 == bank)]['new_consumer_loans'])/np.float(Consumer_Loan_Market[at])
                temp_share = temp_share + np.float(df[ (df.date == t) & (df.RSSD9001 == bank)]['new_consumer_loans'])/np.float(Consumer_Loan_Market[at])
            except:
                df.loc[ (df.date == t) & (df.RSSD9001 == bank), 'consumer_market_share'] = 0
                
    else:
        df.loc[(df.date == t), 'consumer_market_share' ] = 0

#-----------------------#
#                       #
#   Commercial Loans    #
#                       #
#-----------------------#
print()
print()
print()
print('Commercial Loan Business Line')
print()
print()
print()

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
    
    quart = 1
    
    for at, t in enumerate( df.date.unique() ):
        if at ==0:
            try:
                df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'commercial_revenue']   = ( np.float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4436']) +
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

    print('Commercial Bank ',idx,' out of ',len(df.RSSD9001.unique()) )

    # initialize multiplier
    quart = 1  # first observed quarter is Q3 for 1986
    
    # for each time period 
    for at, t in enumerate( df.date.unique() ):
            
        # compute default rate
            # sum of charge-offs (time t)/ sum of loans (t-1)
        if at == 0:  # first period observed is 1986 Q3; can only use contemporaneous values
        
            try:
                # default rate 
                default_rate = ( np.float(df[ (df.date ==t) & (df.RSSD9001 == bank)]['commercial_loan_nco'])/
                                       np.float(df[ (df.date ==t) & (df.RSSD9001 == bank)]['commercial_loans']) )
                
                # new lending 
                new_lending = ( np.float(df[ (df.date ==t) & (df.RSSD9001 == bank)]['commercial_loans']) -
                                (1-am_rate_com)*(1-default_rate)*np.float(df[ (df.date ==t) & (df.RSSD9001 == bank)]['commercial_loans']) )  
    
                # new rate
                agg_rev = ( np.float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4436']) +
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
             
            # don't allow negative lending
            if new_lending < 0:
                new_lending = 0

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

                # don't allow negative lending
                if new_lending < 0:
                    new_lending = 0

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

                # don't allow negative lending
                if new_lending < 0:
                    new_lending = 0

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

# compute market volume of lending each period
Commercial_Loan_Market = []
for at,t in enumerate(df.date.unique()):
    
    Commercial_Loan_Market.append( np.nansum( df.loc[df.date==t]['new_commercial_loans'] ) )
    
# compute market shares 
df['commercial_market_share'] = 0

# for each time period
for at,t in enumerate(df.date.unique()):
    
    temp_share = 0
    
    # compute market shares
    if Commercial_Loan_Market[at] > 0:
        # for each bank 
        for idx,bank in enumerate(df.RSSD9001.unique()):    
        
            # if loan issuance is positive, divide lending by agg lending variable, record in dataframe
            try:                    
                df.loc[ (df.date == t) & (df.RSSD9001 == bank), 'commercial_market_share'] = 100*np.float(df[ (df.date == t) & (df.RSSD9001 == bank)]['new_commercial_loans'])/np.float(Commercial_Loan_Market[at])
                temp_share = temp_share + np.float(df[ (df.date == t) & (df.RSSD9001 == bank)]['new_commercial_loans'])/np.float(Commercial_Loan_Market[at])
            except:
                df.loc[ (df.date == t) & (df.RSSD9001 == bank), 'commercial_market_share'] = 0
                
    else:
        df.loc[(df.date == t), 'commercial_market_share' ] = 0


#----------------------------------#
#                                  #
#   Deposits and Other Expenses    #
#                                  #
#----------------------------------#

print()
print()
print()
print('Deposit Business Line')
print()
print()
print()

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

    print('Deposit Bank ',idx,' out of ',len(df.RSSD9001.unique()) )

    # initialize multiplier
    quart = 1  # first observed quarter is Q3 for 1986

    for at, t in enumerate( df.date.unique() ):

        if at == 0:  # first period observed is 1986 Q3; annualize by multiplying by 4/3
            df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'deposit_expense' ] = ( df[ (df.date ==t) & (df.RSSD9001 == bank) ]['BHCK4174' ] +
                                                                                        df[ (df.date ==t) & (df.RSSD9001 == bank) ]['BHCK6760' ] +
                                                                                        df[ (df.date ==t) & (df.RSSD9001 == bank) ]['BHCK4176' ] +
                                                                                        df[ (df.date ==t) & (df.RSSD9001 == bank) ]['BHCK6761' ] )


            df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'salaries' ] = df[ (df.date==t) & (df.RSSD9001 == bank) ]['salaries_cum']
            df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'premises_cost' ] = df[ (df.date==t) & (df.RSSD9001 == bank) ]['premises_cost_cum']

            df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'other_cost' ] = df[ (df.date==t) & (df.RSSD9001 == bank) ]['other_cost_cum']
            df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'total_cost' ] = df[ (df.date==t) & (df.RSSD9001 == bank) ]['total_cost_cum']

        else:

            if quart == 0: # if Q1, annualize by multiplying by 4

                if t <= np.datetime64('1996-12-31T00:00:00.000000000'):
                    df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'deposit_expense' ] =( df[ (df.date ==t) & (df.RSSD9001 == bank) ]['BHCK4174' ] +
                                                                                           df[ (df.date ==t) & (df.RSSD9001 == bank) ]['BHCK6760' ] +
                                                                                           df[ (df.date ==t) & (df.RSSD9001 == bank) ]['BHCK4176' ] +
                                                                                           df[ (df.date ==t) & (df.RSSD9001 == bank) ]['BHCK6761' ] )

                elif t <= np.datetime64('2016-12-31T00:00:00.000000000'):
                    df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'deposit_expense' ] =( df[ (df.date ==t) & (df.RSSD9001 == bank) ]['BHCKA517' ] +
                                                                                           df[ (df.date ==t) & (df.RSSD9001 == bank) ]['BHCKA518' ] +
                                                                                           df[ (df.date ==t) & (df.RSSD9001 == bank) ]['BHCK6761' ] )
                else:
                    df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'deposit_expense' ] =( df[ (df.date ==t) & (df.RSSD9001 == bank) ]['BHCKHK03' ] +
                                                                                           df[ (df.date ==t) & (df.RSSD9001 == bank) ]['BHCKHK04' ] +
                                                                                           df[ (df.date ==t) & (df.RSSD9001 == bank) ]['BHCK6761' ] )

                df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'salaries' ] = df[ (df.date==t) & (df.RSSD9001 == bank) ]['salaries_cum']
                df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'premises_cost' ] = df[ (df.date==t) & (df.RSSD9001 == bank) ]['premises_cost_cum']

                df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'other_cost' ] = df[ (df.date==t) & (df.RSSD9001 == bank) ]['other_cost_cum']
                df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'total_cost' ] = df[ (df.date==t) & (df.RSSD9001 == bank) ]['total_cost_cum']

            else: # if (Q2,Q3,Q4), compute newly accrued expenses, then multiply by 4

                if t <= np.datetime64('1996-12-31T00:00:00.000000000'):
                    try:
                        df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'deposit_expense' ] =( np.float( df[ (df.date ==t) & (df.RSSD9001 == bank) ]['BHCK4174' ] +
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
                        df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'deposit_expense' ] =( np.float( df[ (df.date ==t) & (df.RSSD9001 == bank) ]['BHCKA517' ] +
                                                                                                 df[ (df.date ==t) & (df.RSSD9001 == bank) ]['BHCKA518' ] +
                                                                                                 df[ (df.date ==t) & (df.RSSD9001 == bank) ]['BHCK6761' ] ) -
                                                                       np.float( df[ (df.date == df.date.unique()[at-1]) & (df.RSSD9001 == bank) ]['BHCKA517' ] +
                                                                         df[ (df.date == df.date.unique()[at-1]) & (df.RSSD9001 == bank) ]['BHCKA518' ] +
                                                                         df[ (df.date == df.date.unique()[at-1]) & (df.RSSD9001 == bank) ]['BHCK6761' ] ) )
                    except:
                        df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'deposit_expense' ] = np.nan
                else:
                    try:
                        df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'deposit_expense' ] =( np.float( df[ (df.date ==t) & (df.RSSD9001 == bank) ]['BHCKHK03' ] +
                                                                                                 df[ (df.date ==t) & (df.RSSD9001 == bank) ]['BHCKHK04' ] +
                                                                                                 df[ (df.date ==t) & (df.RSSD9001 == bank) ]['BHCK6761' ] ) -
                                                                        np.float( df[ (df.date == df.date.unique()[at-1]) & (df.RSSD9001 == bank) ]['BHCKHK03' ] +
                                                                          df[ (df.date == df.date.unique()[at-1]) & (df.RSSD9001 == bank) ]['BHCKHK04' ] +
                                                                          df[ (df.date == df.date.unique()[at-1]) & (df.RSSD9001 == bank) ]['BHCK6761' ] )   )
                    except:
                        df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'deposit_expense' ] = np.nan


                try:
                    df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'salaries' ] = (np.float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['salaries_cum']) - np.float(df[ (df.date==df.date.unique()[at-1]) & (df.RSSD9001 == bank) ]['salaries_cum']) )
                    df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'premises_cost' ] = (np.float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['premises_cost_cum']) - np.float(df[ (df.date==df.date.unique()[at-1]) & (df.RSSD9001 == bank) ]['premises_cost_cum']) )
                    df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'other_cost' ] = (np.float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['other_cost_cum']) - np.float(df[ (df.date==df.date.unique()[at-1]) & (df.RSSD9001 == bank) ]['other_cost_cum']) )
                    df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'total_cost' ] = (np.float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['total_cost_cum']) - np.float(df[ (df.date==df.date.unique()[at-1]) & (df.RSSD9001 == bank) ]['total_cost_cum']) )

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

# compute market volume of lending each period
Deposit_Market = []
for at,t in enumerate(df.date.unique()):
    
    Deposit_Market.append( np.nansum( df.loc[df.date==t]['total_deposits'] ) )


# compute deposit market shares 
df['deposit_market_share'] = 0

# for each time period
for at,t in enumerate(df.date.unique()):
    
    temp_share = 0
        
    # compute market shares
    if Deposit_Market[at] > 0:
        # for each bank 
        for idx,bank in enumerate(df.RSSD9001.unique()):    
        
            # if loan issuance is positive, divide lending by agg lending variable, record in dataframe
            try:                    
                df.loc[ (df.date == t) & (df.RSSD9001 == bank), 'deposit_market_share'] = 100*np.float(df[ (df.date == t) & (df.RSSD9001 == bank)]['total_deposits'])/np.float(Deposit_Market[at])
                temp_share = temp_share + np.float(df[ (df.date == t) & (df.RSSD9001 == bank)]['total_deposits'])/np.float(Deposit_Market[at])
            except:
                df.loc[ (df.date == t) & (df.RSSD9001 == bank), 'deposit_market_share'] = 0
                
    else:
        df.loc[(df.date == t), 'deposit_market_share' ] = 0
        

#-------------------------#
#                         #
#   Insurance Products    #
#                         #
#-------------------------#
print()
print()
print()
print('Insurance Business Line')
print()
print()
print()

df['insurance_revenue'] = 0 
df['insurance_assets'] = df['BHCKC244'] + df['BHCKC248'] 

# compute quarterly deposit interest expense
for idx, bank in enumerate( df.RSSD9001.unique() ):

    print('Insurance Bank ',idx,' out of ',len(df.RSSD9001.unique()) )

    # initialize multiplier
    quart = 1  # first observed quarter is Q3 for 1986

    for at, t in enumerate( df.date.unique() ):

        if at == 0:  # first period observed is 1986 Q3; annualize by multiplying by 4/3
            try:
                df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'insurance_revenue' ] = np.float( df[ (df.date ==t) & (df.RSSD9001 == bank) ]['BHCKC386' ] +
                                                                                            df[ (df.date ==t) & (df.RSSD9001 == bank) ]['BHCKC387' ] ) 
            except:
                pass 
            
        else:

            if quart == 0: # if Q1, annualize by multiplying by 4

                try:
                    df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'insurance_revenue' ] = np.float( df[ (df.date ==t) & (df.RSSD9001 == bank) ]['BHCKC386' ] +
                                                                                            df[ (df.date ==t) & (df.RSSD9001 == bank) ]['BHCKC387' ] ) 
                except: 
                    pass 
                
            else: # if (Q2,Q3,Q4), compute newly accrued expenses, then multiply by 4

                try:
                    df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'insurance_revenue' ] =(np.float( df[ (df.date ==t) & (df.RSSD9001 == bank) ]['BHCKC386' ] +
                                                                                            df[ (df.date ==t) & (df.RSSD9001 == bank) ]['BHCKC387' ]  ) -
                                                                                           np.float( 
                                                                                            df[ (df.date == df.date.unique()[at-1]) & (df.RSSD9001 == bank) ]['BHCKC386' ] +
                                                                                            df[ (df.date == df.date.unique()[at-1]) & (df.RSSD9001 == bank) ]['BHCKC387' ] 
                                                                                               ) )
                except:
                    pass 
                
            #if not last quarter of fiscal year
            if quart < 3:
                quart = quart + 1
            else:
                quart = 0

df['insurance_price'] = df['insurance_revenue']/df['insurance_assets']

# compute insurance market volume 
Insurance_Market = []
for at,t in enumerate(df.date.unique()):
    
    Insurance_Market.append( np.nansum( df.loc[df.date==t]['insurance_assets'] ) )

# compute insurance market shares
df['insurance_market_share'] = 0

for at,t in enumerate(df.date.unique()):
    
    # compute total market 
    temp_share = 0
    
    for idx,bank in enumerate(df.RSSD9001.unique()):
        
        try:
            df.loc[(df.date==t) & (df.RSSD9001==bank), 'insurance_market_share'] = 100*np.float(df[(df.date==t) & (df.RSSD9001==bank)]['insurance_assets'])/np.float(Insurance_Market[at])
            temp_share = temp_share + np.float(df[(df.date==t) & (df.RSSD9001==bank)]['insurance_assets'])/np.float(Insurance_Market[at])
            
        except:
            df.loc[(df.date==t) & (df.RSSD9001==bank), 'insurance_market_share'] = 0
                
#------------------#
#                  # 
#   Data Output    #
#                  # 
#------------------#

# output a refined dataframe
    # this one now has spot rates and new issuance for loans and deposits (measured by market share)
df[['date','RSSD9001','total_assets',
    'deposit_rate','consumer_rate','commercial_rate','insurance_price',
    'deposit_market_share','consumer_market_share','commercial_market_share','insurance_market_share',
    'total_deposits','new_consumer_loans','new_commercial_loans','insurance_assets',
    'salaries','premises_cost','other_cost','total_cost']].to_csv('Data/frdata_refined.csv')

# export total market volumes 
test = pd.DataFrame({ 'date':df.date.unique(),
                      'Commercial_Loan_Market':Commercial_Loan_Market,
                      'Insurance_Market':Insurance_Market,
                      'Deposit_Market':Deposit_Market,
                      'Consumer_Loan_Market':Consumer_Loan_Market})

test.to_csv('Data/MarketSizeByQuarter.csv')

#-----------------------------------------#
#                                         #
#   Statistical and Graphical Analysis    #
#                                         #
#-----------------------------------------#

# plot quantities of new consumer lending
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
    
    if (agg_loans <= 0):# or (np.nansum(df[(df.date==t)]['consumer_rate']) <= 0):
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
    
    if (agg_loans <= 0): # or (np.nansum(df[(df.date==t)]['consumer_rate_lagged']) <= 0):
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
    
    if (agg_loans <= 0): # or (np.nansum(df[(df.date==t)]['commercial_rate']) <= 0):
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
    
    if (agg_loans <= 0): # or (np.nansum(df[(df.date==t)]['commercial_rate_lagged']) <= 0):
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


# Plot deposit quantities
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

# Plot insurance quantities
agg_assets = []
agg_revenue = []
agg_price = [] 
for at,t in enumerate(df.date.unique()):
    
    agg_assets.append( np.nansum( df[df.date == t]['insurance_assets'] )/(1000*1000) )
    
    agg_revenue.append( np.nansum( df[df.date == t]['insurance_revenue'] )/(1000*1000) )
    try:
        agg_price.append( np.nansum( df[df.date == t]['insurance_revenue'] )/np.nansum( df[df.date == t]['insurance_assets'] ) )
    except:
        agg_price.append(0)
        
plt.close('all')
# agg insurance assets
plt.figure(1)
plt.plot(df.date.unique(),agg_assets,lw=3)
plt.xlabel('Date',fontsize=15)
plt.ylabel('Assets ($, Billion)',fontsize=15)
plt.title('Aggregate Insurance Assets',fontsize=20)

# agg revenues 
plt.figure(2)
plt.plot(df.date.unique(),agg_revenue,lw=3)
plt.xlabel('Date',fontsize=15)
plt.ylabel('Revenues ($, Billion)',fontsize=15)
plt.title('Aggregate Insurance Revenues',fontsize=20)

# agg price (revenue divided by assets)
plt.figure(3)
plt.plot(df.date.unique(),agg_price,lw=3)
plt.xlabel('Date',fontsize=15)
plt.ylabel('Price',fontsize=15)
plt.title('Insurance Price (Market-weighted)',fontsize=20)

# panel series for assets
plt.figure(4)
[plt.plot(df[(df.RSSD9001 == bank)]['date'],df[(df.RSSD9001 == bank)]['insurance_assets']/(1000*1000),lw=2) for idx,bank in enumerate( df.RSSD9001.unique() )]
plt.xlabel('Date',fontsize=15)
plt.ylabel('Assets ($, Billion)',fontsize=15)
plt.title('Panel Series for Bank Insurance Assets',fontsize=20)

plt.figure(5)
[plt.plot(df[(df.RSSD9001 == bank)]['date'],df[(df.RSSD9001 == bank)]['insurance_revenue']/(1000*1000),lw=2) for idx,bank in enumerate( df.RSSD9001.unique() )]
plt.xlabel('Date',fontsize=15)
plt.ylabel('Revenues ($, Billion)',fontsize=15)
plt.title('Panel Series for Bank Insurance Revenues',fontsize=20)

# panel series for insurance prices
plt.figure(6)
[plt.plot(df[(df.RSSD9001 == bank)]['date'],df[(df.RSSD9001 == bank)]['insurance_price'],lw=2) for idx,bank in enumerate( df.RSSD9001.unique() )]
plt.xlabel('Date',fontsize=15)
plt.ylabel('Price/Premium',fontsize=15)
plt.title('Panel Series for Bank Insurance Prices',fontsize=20)

    
plt.figure(7)
[plt.plot(df[(df.RSSD9001 == bank)]['date'],df[(df.RSSD9001 == bank)]['insurance_market_share'],lw=2) for idx,bank in enumerate( df.RSSD9001.unique() )]
plt.xlabel('Date',fontsize=15)
plt.ylabel('Market Share (%)',fontsize=15)
plt.title('Bank Insurance Market Share',fontsize=20)

for at,t in enumerate(df.date.unique()):
    
    print( np.nansum( df[df.date == t]['insurance_market_share'] ) )
    
    