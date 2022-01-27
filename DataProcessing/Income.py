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
plt.figure(1)
plt.plot(df.date.unique(), net_income, label='reported net income',lw=3)
plt.plot( df.date.unique(),np.asarray(( interest_revenue )) + np.asarray(( non_interest_revenue )) + np.asarray(( gains_revenue )) - \
                           np.asarray(( interest_expense )) - np.asarray(( non_interest_expense )) - np.asarray(( provisions )) - \
                           np.asarray(( taxes )),lw=3, label='aggregated net income')
    
plt.legend(fontsize=15)
plt.xlabel('Date',fontsize=15)
plt.ylabel('$ Billion',fontsize=15)
plt.title('Total Bank Sector Net Income',fontsize=15)

plt.figure(2) 
plt.subplot(1,2,1)
plt.plot(df.date.unique(), 100*np.asarray(( interest_revenue))/( np.asarray(( interest_revenue)) + np.asarray(( non_interest_revenue)) ),lw=3, label='Interest Revenue' ) 
plt.plot(df.date.unique(), 100*np.asarray(( non_interest_revenue))/( np.asarray(( interest_revenue)) + np.asarray(( non_interest_revenue)) ),lw=3, label='Non-Interest Revenue' ) 
plt.legend(fontsize=15)
plt.xlabel('Date',fontsize=15)
plt.ylabel('%',fontsize=15)
plt.title('Revenue Shares (with Gross interest revenue)',fontsize=15)
plt.subplot(1,2,2)
plt.plot(df.date.unique(), 100*( np.asarray(( interest_revenue)) - np.asarray(( interest_expense)))/( np.asarray(( interest_revenue)) - np.asarray(( interest_expense)) + np.asarray(( non_interest_revenue)) ),lw=3, label='Interest Revenue' ) 
plt.plot(df.date.unique(), 100*np.asarray(( non_interest_revenue))/( np.asarray(( interest_revenue)) + np.asarray(( non_interest_revenue)) ),lw=3, label='Non-Interest Revenue' ) 
plt.legend(fontsize=15)
plt.xlabel('Date',fontsize=15)
plt.ylabel('%',fontsize=15)
plt.title('Revenue Shares (with net interest revenue)',fontsize=15)

plt.figure(3)
plt.subplot(1,2,1)
plt.title('Revenue Components',fontsize=15)
plt.plot( df.date.unique(), np.asarray(( interest_revenue)) - np.asarray(( interest_expense)),lw=3, label=r'interest revenue $r^{\ell} - r^{d}$' )
plt.plot( df.date.unique(), np.asarray(( non_interest_revenue)),lw=3, label=r'non-interest revenue' )
plt.plot( df.date.unique(), np.asarray(( gains_revenue)),lw=3, label=r'investment gains on securities' )
plt.legend(fontsize=15)
plt.subplot(1,2,2)
plt.title('Cost Components',fontsize=15)
plt.plot( df.date.unique(), np.asarray(( non_interest_expense)),lw=3, label='non-interest expense' )
plt.plot( df.date.unique(), provisions ,lw=3, label='provisions for loan losses' )
plt.plot( df.date.unique(), taxes ,lw=3, label='taxes' )
plt.legend(fontsize=15)


loans_leases = []
securities = []
fed_repo = []
trading = []

quart = 0
for at, t in enumerate( df.date.unique() ):

    # if first quarter, just report the accumulated flows
    if quart == 0:
        loans_leases.append(  np.nansum( df[ df.date ==t ]['BHCK4435'] + df[ df.date ==t ]['BHCK4436'] + df[ df.date ==t ]['BHCKF821'] + \
                                         df[ df.date ==t ]['BHCK4059'] + df[ df.date ==t ]['BHCK4065'] )/(1000*1000) )

        securities.append(  np.nansum( df[ df.date ==t ]['BHCKB488'] + df[ df.date ==t ]['BHCKB489'] + df[ df.date ==t ]['BHCK4060'] )/(1000*1000) )

        fed_repo.append(  np.nansum( df[ df.date ==t ]['BHCK4115'] + df[ df.date ==t ]['BHCK4020']  )/(1000*1000) )

        trading.append(  np.nansum( df[ df.date ==t ]['BHCK4069']  )/(1000*1000) )


    # if not first quarter, compute difference in flows from last period        
    else:        
        loans_leases.append( np.nansum(  df[ df.date ==t ]['BHCK4435'] + df[ df.date ==t ]['BHCK4436'] + df[ df.date ==t ]['BHCKF821'] + \
                                         df[ df.date ==t ]['BHCK4059'] + df[ df.date ==t ]['BHCK4065'] )/(1000*1000) -  \
                            np.nansum(  df[ df.date == df.date.unique()[at-1] ]['BHCK4435'] + df[ df.date == df.date.unique()[at-1] ]['BHCK4436'] + df[ df.date == df.date.unique()[at-1] ]['BHCKF821'] + \
                                         df[ df.date == df.date.unique()[at-1] ]['BHCK4059'] + df[ df.date == df.date.unique()[at-1] ]['BHCK4065'] )/(1000*1000) )

        securities.append( np.nansum(  df[ df.date ==t ]['BHCKB488'] + df[ df.date ==t ]['BHCKB489'] + df[ df.date ==t ]['BHCK4060']  )/(1000*1000) -  \
                            np.nansum(  df[ df.date == df.date.unique()[at-1] ]['BHCKB488'] + df[ df.date == df.date.unique()[at-1] ]['BHCKB489'] + \
                                         df[ df.date == df.date.unique()[at-1] ]['BHCK4060']  )/(1000*1000) )

        fed_repo.append( np.nansum(  df[ df.date ==t ]['BHCK4115'] + df[ df.date ==t ]['BHCK4020']  )/(1000*1000) -  \
                            np.nansum(  df[ df.date == df.date.unique()[at-1] ]['BHCK4115'] + df[ df.date == df.date.unique()[at-1] ]['BHCK4020'] )/(1000*1000) )

        trading.append( np.nansum(  df[ df.date ==t ]['BHCK4069'] )/(1000*1000) - np.nansum(  df[ df.date == df.date.unique()[at-1] ]['BHCK4069'] )/(1000*1000) )

    if quart < 3:
        quart = quart + 1
    else:
        quart = 0


plt.close('all')
plt.figure(1)
plt.plot(df.date.unique(), np.asarray(trading) + np.asarray(( loans_leases )) + np.asarray(( securities )) + np.asarray(( fed_repo )),lw=3, label='aggregated interest revenue' )
plt.plot(df.date.unique(), np.asarray(trading) + np.asarray(( loans_leases )) + np.asarray(( securities )) + np.asarray(( fed_repo )) - np.asarray((provisions)) ,lw=3,ls='--', label='aggregated net of provisions' )
plt.plot(df.date.unique(), interest_revenue,lw=3, label='reported interest revenue')
plt.legend(fontsize=15)
plt.title('Interest Revenue',fontsize=15)
plt.xlabel('Date',fontsize=15)
plt.ylabel('$ Billion',fontsize=15)

plt.figure(3)
plt.plot(df.date.unique(), 100*( np.asarray((loans_leases)) - np.asarray((provisions)) )/( np.asarray((loans_leases)) + np.asarray((securities)) + np.asarray((fed_repo)) + np.asarray((trading)) - np.asarray((provisions)) ),lw=3, label='loans + leases net provisions' )
plt.plot(df.date.unique(), 100*np.asarray((securities))/( np.asarray((loans_leases)) + np.asarray((securities)) + np.asarray((fed_repo)) + np.asarray((trading)) - np.asarray((provisions)) ),lw=3, label='securities' )
plt.plot(df.date.unique(), 100*np.asarray((fed_repo))/( np.asarray((loans_leases)) + np.asarray((securities)) + np.asarray((fed_repo)) + np.asarray((trading)) - np.asarray((provisions)) ),lw=3, label='financial lending' )
plt.plot(df.date.unique(), 100*np.asarray((trading))/( np.asarray((loans_leases)) + np.asarray((securities)) + np.asarray((fed_repo)) + np.asarray((trading)) - np.asarray((provisions)) ),lw=3, label='trading assets' )
plt.title('Breakdown of Interest Revenue Sources',fontsize=15)
plt.ylabel('%',fontsize=15)
plt.xlabel('Date',fontsize=15)
plt.legend(fontsize=15)


# breakdown of non-interest revenues
fiduciary = []
trading_rev = []
deposit_charge = []
securities_broke = []
ibank = []

annuity = []
insurance = []
other_insurance = []

total_small_ibank = []
total_small_insurance  = []

venture_cap = []
net_servicing = []
net_securitization = []

reported = []
net_gains = []
other = []


quart = 0
for at, t in enumerate( df.date.unique() ):

    # if first quarter, just report the accumulated flows
    if quart == 0:
        annuity.append(  np.nansum( df[ df.date ==t ]['BHCKC887'] )/(1000*1000) )
        insurance.append(  np.nansum( df[ df.date ==t ]['BHCKC386'] )/(1000*1000) )
        other_insurance.append(  np.nansum( df[ df.date ==t ]['BHCKC387'] )/(1000*1000) )

        reported.append(  np.nansum( df[ df.date ==t ]['BHCK4079'] )/(1000*1000) )

        other.append(  np.nansum( df[ df.date ==t ]['BHCKB497'] )/(1000*1000) )

        net_gains.append(  np.nansum( df[ df.date ==t ]['BHCK8560'] + df[ df.date ==t ]['BHCK8561'] + df[ df.date ==t ]['BHCKB496'] )/(1000*1000) )

        fiduciary.append(  np.nansum( df[ df.date ==t ]['BHCK4070'] )/(1000*1000) )

        trading_rev.append(  np.nansum( df[ df.date ==t ]['BHCKA220'] )/(1000*1000) )

        deposit_charge.append(  np.nansum( df[ df.date ==t ]['BHCK4483'] )/(1000*1000) )

        securities_broke.append(  np.nansum( df[ df.date ==t ]['BHCKC886'] )/(1000*1000) )

        ibank.append(  np.nansum( df[ df.date ==t ]['BHCKC888'] )/(1000*1000) )

        total_small_insurance.append(  np.nansum( df[ df.date ==t ]['BHCKKX47'])/(1000*1000) )

        total_small_ibank.append(  np.nansum( df[ df.date ==t ]['BHCKKX47'] )/(1000*1000) )

        venture_cap.append(  np.nansum( df[ df.date ==t ]['BHCKB491'] )/(1000*1000) )

        net_servicing.append(  np.nansum( df[ df.date ==t ]['BHCKB492'] )/(1000*1000) )

        net_securitization.append(  np.nansum( df[ df.date ==t ]['BHCKB493'] )/(1000*1000) )


    # if not first quarter, compute difference in flows from last period        
    else:        
        annuity.append( np.nansum(  df[ df.date ==t ]['BHCKC887'] )/(1000*1000) -  \
                            np.nansum(  df[ df.date == df.date.unique()[at-1] ]['BHCKC887']  )/(1000*1000) )
        insurance.append( np.nansum(  df[ df.date ==t ]['BHCKC386'] )/(1000*1000) -  \
                            np.nansum(  df[ df.date == df.date.unique()[at-1] ]['BHCKC386']  )/(1000*1000) )
        other_insurance.append( np.nansum(  df[ df.date ==t ]['BHCKC387'] )/(1000*1000) -  \
                            np.nansum(  df[ df.date == df.date.unique()[at-1] ]['BHCKC387']  )/(1000*1000) )

        fiduciary.append( np.nansum(  df[ df.date ==t ]['BHCK4070'] )/(1000*1000) -  \
                            np.nansum(  df[ df.date == df.date.unique()[at-1] ]['BHCK4070']  )/(1000*1000) )

        trading_rev.append( np.nansum(  df[ df.date ==t ]['BHCKA220'] )/(1000*1000) -  \
                            np.nansum(  df[ df.date == df.date.unique()[at-1] ]['BHCKA220']  )/(1000*1000) )

        deposit_charge.append( np.nansum(  df[ df.date ==t ]['BHCK4483'] )/(1000*1000) -  \
                            np.nansum(  df[ df.date == df.date.unique()[at-1] ]['BHCK4483']  )/(1000*1000) )

        securities_broke.append( np.nansum(  df[ df.date ==t ]['BHCKC886'] )/(1000*1000) -  \
                            np.nansum(  df[ df.date == df.date.unique()[at-1] ]['BHCKC886']  )/(1000*1000) )

        ibank.append( np.nansum(  df[ df.date ==t ]['BHCKC888'] )/(1000*1000) -  \
                            np.nansum(  df[ df.date == df.date.unique()[at-1] ]['BHCKC888']  )/(1000*1000) )

        total_small_insurance.append( np.nansum( df[ df.date ==t ]['BHCKKX47'] )/(1000*1000) -  \
                            np.nansum( df[ df.date == df.date.unique()[at-1] ]['BHCKKX47']  )/(1000*1000) )

        total_small_ibank.append( np.nansum( df[ df.date ==t ]['BHCKKX47'] )/(1000*1000) -  \
                            np.nansum( df[ df.date == df.date.unique()[at-1] ]['BHCKKX47']  )/(1000*1000) )

        venture_cap.append( np.nansum(  df[ df.date ==t ]['BHCKB491'] )/(1000*1000) -  \
                            np.nansum(  df[ df.date == df.date.unique()[at-1] ]['BHCKB491']  )/(1000*1000) )

        net_servicing.append( np.nansum(  df[ df.date ==t ]['BHCKB492'] )/(1000*1000) -  \
                            np.nansum(  df[ df.date == df.date.unique()[at-1] ]['BHCKB492']  )/(1000*1000) )

        net_securitization.append( np.nansum(  df[ df.date ==t ]['BHCKB493'] )/(1000*1000) -  \
                            np.nansum(  df[ df.date == df.date.unique()[at-1] ]['BHCKB493']  )/(1000*1000) )

        reported.append( np.nansum(  df[ df.date ==t ]['BHCK4079'] )/(1000*1000) -  \
                            np.nansum(  df[ df.date == df.date.unique()[at-1] ]['BHCK4079']  )/(1000*1000) )

        other.append( np.nansum(  df[ df.date ==t ]['BHCKB497'] )/(1000*1000) -  \
                            np.nansum(  df[ df.date == df.date.unique()[at-1] ]['BHCKB497']  )/(1000*1000) )

        net_gains.append( np.nansum(  df[ df.date ==t ]['BHCK8560'] + df[ df.date ==t ]['BHCK8561'] + df[ df.date ==t ]['BHCKB496'] )/(1000*1000) -  \
                            np.nansum(  df[ df.date == df.date.unique()[at-1] ]['BHCK8560'] + df[ df.date == df.date.unique()[at-1] ]['BHCK8561'] + df[ df.date == df.date.unique()[at-1] ]['BHCKB496']  )/(1000*1000) )

    if quart < 3:
        quart = quart + 1
    else:
        quart = 0


plt.close('all')
plt.figure(1)
plt.plot(df.date.unique(),reported,lw=3,label='reported')
plt.plot(df.date.unique(),np.asarray((deposit_charge))+np.asarray((trading_rev))+np.asarray((fiduciary))+np.asarray((total_small_ibank))+np.asarray((total_small_insurance))+np.asarray((venture_cap))+np.asarray((net_servicing))+
                          np.asarray((net_securitization)) + np.asarray((net_gains)) + np.asarray((other))+ np.asarray((annuity))
                         + np.asarray((insurance))+ np.asarray((other_insurance))+ np.asarray((securities_broke))+ np.asarray((ibank)),lw=3,ls='--',label='aggregated')
plt.legend(fontsize=15)
plt.title('Total Non-interest Revenue',fontsize=15)
plt.xlabel('$ Billion',fontsize=15)

plt.figure(2)
plt.plot(df.date.unique(), np.asarray((fiduciary)),label='fiduciary',lw=3 )
plt.plot(df.date.unique(), np.asarray((deposit_charge)),label='deposit charge',lw=3 )
plt.plot(df.date.unique(), np.asarray((trading_rev)),label='trading revenue',lw=3,ls='--' )
plt.plot(df.date.unique(), (np.asarray((ibank))+np.asarray((securities_broke))+np.asarray((total_small_ibank)) ),label='ibank',lw=3,ls=':' )
plt.plot(df.date.unique(), (np.asarray((insurance))+np.asarray((other_insurance))+np.asarray((annuity))+np.asarray((total_small_insurance)) ),label='insurance',lw=3 )
plt.plot(df.date.unique(), np.asarray((venture_cap)),label='venture cap',lw=3)
plt.plot(df.date.unique(), np.asarray((net_servicing)),label='net servicing',lw=3 )
plt.plot(df.date.unique(), np.asarray((net_securitization)),label='net securitization',lw=3 )
plt.plot(df.date.unique(), np.asarray((net_gains)),label='net gains',lw=3 )
plt.plot(df.date.unique(), np.asarray((other)),label='other',lw=3,ls='--' )
plt.legend(fontsize=15)
plt.title('Decomposing Non-Interest Revenue Sources',fontsize=15)
plt.xlabel('$ Billion',fontsize=15)

# decomposing other non-interest revenue category
checks = []
life = []
atm = []
real_estate = []
deposit_box = []
interchange = []
wire = []

fill = []

quart = 0
for at, t in enumerate( df.date.unique() ):

    # if first quarter, just report the accumulated flows
    if quart == 0:
        checks.append(  np.nansum( df[ df.date ==t ]['BHCKC013'] )/(1000*1000) )
        life.append(  np.nansum( df[ df.date ==t ]['BHCKC014'] )/(1000*1000) )
        atm.append(  np.nansum( df[ df.date ==t ]['BHCKC016'] )/(1000*1000) )
        real_estate.append(  np.nansum( df[ df.date ==t ]['BHCK4042'] )/(1000*1000) )
        deposit_box.append(  np.nansum( df[ df.date ==t ]['BHCKC015'] )/(1000*1000) )
        interchange.append(  np.nansum( df[ df.date ==t ]['BHCKF555'] )/(1000*1000) )
        wire.append(  np.nansum( df[ df.date ==t ]['BHCKT047'] )/(1000*1000) )
        
        #fill.append(  np.nansum( df[ df.date ==t ]['BHCK8562'] )/(1000*1000) )

    # if not first quarter, compute difference in flows from last period        
    else:        
        checks.append( np.nansum(  df[ df.date ==t ]['BHCKC013'] )/(1000*1000) -  \
                            np.nansum(  df[ df.date == df.date.unique()[at-1] ]['BHCKC013']  )/(1000*1000) )

        life.append( np.nansum(  df[ df.date ==t ]['BHCKC014'] )/(1000*1000) -  \
                            np.nansum(  df[ df.date == df.date.unique()[at-1] ]['BHCKC014']  )/(1000*1000) )

        atm.append( np.nansum(  df[ df.date ==t ]['BHCKC016'] )/(1000*1000) -  \
                            np.nansum(  df[ df.date == df.date.unique()[at-1] ]['BHCKC016']  )/(1000*1000) )

        real_estate.append( np.nansum(  df[ df.date ==t ]['BHCK4042'] )/(1000*1000) -  \
                            np.nansum(  df[ df.date == df.date.unique()[at-1] ]['BHCK4042']  )/(1000*1000) )

        deposit_box.append( np.nansum(  df[ df.date ==t ]['BHCKC015'] )/(1000*1000) -  \
                            np.nansum(  df[ df.date == df.date.unique()[at-1] ]['BHCKC015']  )/(1000*1000) )

        interchange.append( np.nansum(  df[ df.date ==t ]['BHCKF555'] )/(1000*1000) -  \
                            np.nansum(  df[ df.date == df.date.unique()[at-1] ]['BHCKF555']  )/(1000*1000) )

        wire.append( np.nansum(  df[ df.date ==t ]['BHCKT047'] )/(1000*1000) -  \
                            np.nansum(  df[ df.date == df.date.unique()[at-1] ]['BHCKT047']  )/(1000*1000) )

        #fill.append( np.nansum(  df[ df.date ==t ]['BHCK8562'] )/(1000*1000) -  \
        #                    np.nansum(  df[ df.date == df.date.unique()[at-1] ]['BHCK8562']  )/(1000*1000) )

    if quart < 3:
        quart = quart + 1
    else:
        quart = 0

plt.figure(3)
plt.plot(df.date.unique(),other,lw=3,label='reported')
plt.plot(df.date.unique(),np.asarray((checks))+np.asarray((life))+np.asarray((atm))+np.asarray((real_estate))+np.asarray((deposit_box))+np.asarray((interchange))+np.asarray((wire)),lw=3,ls='--',label='aggregated')
plt.legend(fontsize=15)
plt.xlabel('Date')
plt.ylabel('$ Billion')
plt.title('Other Non-Interest Revenue Category',fontsize=15)

