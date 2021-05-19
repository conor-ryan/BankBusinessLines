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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#                                                           #
#   Create Deposit and Loans Quantity and Expense Series    #
#                                                           #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

"""
Deposit Quantity
    Looking at total non-interest-bearing deposits (BHDM6631) + interest-bearing deposits (BHDM6636)
        in domestic branches only.  To include foreign branches, as well, also use BHFN6631 + BHFN 6636

Deposit Expense

    Categorical recording of interest expense items has changed over time and there is no
        aggregated number (that I could find) for total interest expense on all deposits.

    From 1981 Q2 to 1996 Q4, interest expense = CDs ge 100k (BHCK4174) + time deposits ge 100k (BHCK6760) + other deposits (BHCK6761 or 4176)

    From 1997 Q1 to 2016 Q4, interest expense = time deposits ge 100k (BHCKA517) + time deposits < 100k (BHCK A518) + other deposits (BHCK6761)

    From 2017 Q1 to Present, interest expense = time deposits < 250k (BHCKHK03) + time deposits ge 250k (BHCKHK04) + other deposits (BHCK6761)

    *NEED TO CHECK THAT 'OTHER DEPOSITS' IS A PROPER RESIDUAL FOR ALL OTHER INTEREST EXPENSE, OVER THE SAMPLE PERIOD

An aside on mnemonics: BHCK relate to consolidated financial statements of bank holding companies, whereas BHDM refers to
    the domestic BHC and BHFN refers to the foreign branches of the BHC

Loan Quantity
    Total consumer lending = loans to individuals for personal epense (BHDM1975) + home equity credit lines (BHDM1797) +
            first-lien loans secured by 1-4 family real estate (BHDM5367) + junior-lient loans secured by 1-4 family
            real estate (BHDM5368)

    - Issue: do not separately observe interest & fee income for loans to individuals, so re-define consumer lending to
        simply be BHDM1797 + BHDM5367 + BHDM5368

    - Given this, define commercial lending to be all loans & leases minus consumer lending:
            commercial lending = construction/land loans (BHCKF158, BHCKF159) +
                                 secured by farmland (BHDM1420) +
                                 loans to individuals (BHDM1975) +
                                 secured by multifamily properties (BHDM1460) +
                                 secured by nonfarm/non-res properties (BHCKF160, BHCKF161) +
                                 loans to other banks (BHCK1292, BHCK1296) +
                                 loans to farmers (BHCK1590) +
                                 commercial & industrial loans (BHDM1766) +
                                 loans to financial institutions (BHDMJ454, BHDM1545, BHDMKX57) +
                                 lease financing receivables (BHDM2165)

    - Again, note that there are individual-type loans which are in the lease financing receivables and individual
        loans but we are limited on data.  As a second pass, develop way to infer how the interest income is split
        across these

    - Note, I am excluding loans to foreign governments and (when possible) use the domestic time series BHDM
        instead of BHCK to think of the domestic market and not foreign consumers.


    - data issue: most of these quantity series only start in 1991 Q1

    - other: there is a leases category, as well, but it does delineate how it is split between personal and commercial/business use

Loan Price/Return

    - Interest/Fee Income from Consumer Loans = BHCK4435 (essentially covering mortgage lending to consumers)

        - BHCK4435 covers lines of credit, first- and junior-lien BUT no income item for 'loans to individuals'. Those cashflows
            are likely lumped into Interest/Fee Income from Other Loans (BHCKF821)

    - Issue: series only goes from 2008 Q1 to Present

    - Interest/Fee Income for Commercial Loans is everything else:
        = other loans secured by real estate (BHCK4436) + all other loans (BHCKF821) +
          lease financing receivables (BHCK4065) +
          interest income from other banks (BHCK4115)

    - data issue/question: other interest income (BHCK4518) includes "interest received on other assets not specified elsewhere"
        and "interest attributed to transactions not directly associated with balance sheet, such as interest rate swaps and Forex
        transactions".  Kinda vague.  I'm not going to include it as commercial lending interest.

    - For both consumer and commercial lending income, need to account for charge-offs (loans being written off due to default)
        plus recoveries (recovered valued of delinquet loans which are unexpected)

    - Consumer lending net charge-off (NCO) = (BHCK5411 + BHCKC234 + BHCKC235) - (BHCK5412 + BHCKC217 + BHCKC218)

    - Commercial lending net charge-off = (BHCKC891 + BHCKC893 + BHCK3584 + BHCK3588 + BHCKC895 + BHCKC897 + BHCK4655 + BHCK4645 + BHCKB514 + BHCKK129 + BHCKK205 + BHCK4644 + BHCKF158 + BHCKC880 + BHCKKX50)
                                             -
                                          (BHCKC892 + BHCKC894 + BHCK3585 + BHCK3589 + BHCKC896 + BHCKC898 + BHCK4665 + BHCK4617 + BHCKB515 + BHCKK133 + BHCKK206 + BHCK4628 + BHCKF187 + BHCKF188 + BHCKKX51)

    - Then, return on lending is ( interest return - NCO )/lending

    Cost Variables
    - Salaries: BHCK4135
    - Premises: BHCK4217
    - Other: BHCK4092
    - Total: BHCK4093

    Measuring bank size to normalize costs, using Total Assets BHCK2170
"""
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



### Quantity Series ###

# create deposit quantity series
df['total_deposits'] = df['BHDM6631'] + df['BHDM6636']

# create consumer loan quantity series
df['consumer_loans'] = df['BHDM1797'] + df['BHDM5367'] + df['BHDM5368']

# create commercial loan quantity series
df['commercial_loans'] = (df['BHCKF158'] + df['BHCKF159'] + df['BHDM1420'] + df['BHDM1975'] + df['BHDM1460'] + df['BHCKF160'] +
                          df['BHCKF161'] + df['BHCK1292'] + df['BHCK1296'] + df['BHCK1590'] + df['BHDM1766'] + df['BHDMJ454'] +
                          df['BHDM1545']  + df['BHDM2165'] + df['BHDMKX57'] )


### Output Aggregate Quantity Date by Quarter for Total Market Size ####
df[['date','total_deposits','consumer_loans','commercial_loans']].groupby('date').sum().to_csv("Data/MarketSizeByQuarter.csv")
### Income (Revenue?) Series ###

# create deposit, consumer loan and commercial loan income/expense series
df['deposit_expense']     = np.nan
df['consumer_loan_int']   = np.nan
df['commercial_loan_int'] = np.nan
df['com_nco'] = np.nan
df['con_nco'] = np.nan

# create loan net charge-off variable (NCO)
df['consumer_loan_nco']   =   (( df['BHCK5411'] + df['BHCKC234'] + df['BHCKC235'] ) -
                               ( df['BHCK5412'] + df['BHCKC217'] + df['BHCKC218'] ))

df['commercial_loan_nco'] = ( ( df['BHCKC891'] + df['BHCKC893'] + df['BHCK3584'] + df['BHCK3588'] + df['BHCKC895'] + df['BHCKC897'] +
                                df['BHCK4655'] + df['BHCK4645'] + df['BHCKB514'] + df['BHCKK129'] + df['BHCKK205'] + df['BHCK4644'] +
                                df['BHCKF185'] + df['BHCKC880'] + df['BHCKKX50'] ) -
                              ( df['BHCKC892'] + df['BHCKC894'] + df['BHCK3585'] + df['BHCK3589'] + df['BHCKC896'] + df['BHCKC898'] +
                                df['BHCK4665'] + df['BHCK4617'] + df['BHCKB515'] + df['BHCKK133'] + df['BHCKK206'] + df['BHCK4628'] +
                                df['BHCKF187'] + df['BHCKF188'] + df['BHCKKX51'] ) )

### Cost Series (cumulative) ###
df['salaries_cum'] = df['BHCK4135']
df['premises_cost_cum'] = df['BHCK4217']
df['other_cost_cum'] = df['BHCK4092']
df['total_cost_cum'] = df['BHCK4093']

df['salaries'] =  np.nan
df['premises_cost'] = np.nan
df['other_cost'] = np.nan
df['total_cost'] = np.nan

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

            df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'consumer_loan_int' ] = (4/3)*( df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4435'] - df[ (df.date==t) & (df.RSSD9001 == bank) ]['consumer_loan_nco'] )

            df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'commercial_loan_int' ] = (4/3)*( df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4436'] +
                                                                                             df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKF821'] +
                                                                                             df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4065'] +
                                                                                             df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4115'] -
                                                                                             df[ (df.date==t) & (df.RSSD9001 == bank) ]['commercial_loan_nco'])

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

                # loan interest
                df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'consumer_loan_int' ] = 4*( df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4435'] - df[ (df.date==t) & (df.RSSD9001 == bank) ]['consumer_loan_nco'] )

                df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'commercial_loan_int' ] = 4*( df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4436'] +
                                                                                                 df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKF821'] +
                                                                                                 df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4065'] +
                                                                                                 df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4115'] -
                                                                                                 df[ (df.date==t) & (df.RSSD9001 == bank) ]['commercial_loan_nco'])

                df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'con_nco' ] = 4*df[ (df.date==t) & (df.RSSD9001 == bank) ]['consumer_loan_nco']
                df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'com_nco' ] = 4*df[ (df.date==t) & (df.RSSD9001 == bank) ]['commercial_loan_nco']

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

                # loan interest
                try:
                    df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'consumer_loan_int' ] = 4*(  np.float( df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4435'] - df[ (df.date==t) & (df.RSSD9001 == bank) ]['consumer_loan_nco'] ) -
                                                                                                np.float(df[ (df.date==df.date.unique()[at-1]) & (df.RSSD9001 == bank) ]['BHCK4435'] - df[ (df.date==df.date.unique()[at-1]) & (df.RSSD9001 == bank) ]['consumer_loan_nco']))
                except:
                    df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'consumer_loan_int' ] = np.nan

                try:
                    df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'commercial_loan_int' ] = 4*(np.float( df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4436'] +
                                                                                                     df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKF821'] +
                                                                                                     df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4065'] +
                                                                                                     df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4115'] -
                                                                                                     df[ (df.date==t) & (df.RSSD9001 == bank) ]['commercial_loan_nco']) -
                                                                                                np.float( df[ (df.date==df.date.unique()[at-1]) & (df.RSSD9001 == bank) ]['BHCK4436'] +
                                                                                                     df[ (df.date==df.date.unique()[at-1]) & (df.RSSD9001 == bank) ]['BHCKF821'] +
                                                                                                     df[ (df.date==df.date.unique()[at-1]) & (df.RSSD9001 == bank) ]['BHCK4065'] +
                                                                                                     df[ (df.date==df.date.unique()[at-1]) & (df.RSSD9001 == bank) ]['BHCK4115'] -
                                                                                                     df[ (df.date==df.date.unique()[at-1]) & (df.RSSD9001 == bank) ]['commercial_loan_nco']) )
                except:
                    df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'commercial_loan_int' ] = np.nan

                try:
                    df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'con_nco' ] = 4*(np.float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['consumer_loan_nco']) - np.float(df[(df.date==df.date.unique()[at-1]) & (df.RSSD9001 == bank) ]['consumer_loan_nco']) )
                    df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'com_nco' ] = 4*(np.float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['commercial_loan_nco']) - np.float(df[ (df.date==df.date.unique()[at-1]) & (df.RSSD9001 == bank) ]['commercial_loan_nco']) )

                    df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'salaries' ] = 4*(np.float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['salaries_cum']) - np.float(df[ (df.date==df.date.unique()[at-1]) & (df.RSSD9001 == bank) ]['salaries_cum']) )
                    df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'premises_cost' ] = 4*(np.float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['premises_cost_cum']) - np.float(df[ (df.date==df.date.unique()[at-1]) & (df.RSSD9001 == bank) ]['premises_cost_cum']) )
                    df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'other_cost' ] = 4*(np.float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['other_cost_cum']) - np.float(df[ (df.date==df.date.unique()[at-1]) & (df.RSSD9001 == bank) ]['other_cost_cum']) )
                    df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'total_cost' ] = 4*(np.float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['total_cost_cum']) - np.float(df[ (df.date==df.date.unique()[at-1]) & (df.RSSD9001 == bank) ]['total_cost_cum']) )

                except:
                    df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'con_nco' ] = np.nan
                    df.loc[ (df.date ==t) & (df.RSSD9001 == bank), 'com_nco' ] = np.nan
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

df['consumer_rate'] = df['consumer_loan_int']/df['consumer_loans']

df['commercial_rate'] = df['commercial_loan_int']/df['commercial_loans']

# output a refined dataframe
df[['date','RSSD9001','total_assets','deposit_rate','consumer_rate','commercial_rate','total_deposits','consumer_loans','commercial_loans','salaries','premises_cost','other_cost','total_cost']].to_csv('Data/frdata_refined.csv')


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#                                           #
#   Deposit Quantity and Cost Statistics    #
#                                           #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

# aggregate data
agg_dep = []
agg_exp = []
agg_ret = []

for at,t in enumerate(df.date.unique()):
    agg_dep.append( df[df.date == t]['total_deposits'].sum()/(1000*1000*1000) )

    agg_exp.append( df[df.date == t]['deposit_expense'].sum()/(1000*1000*1000) )

    agg_ret.append( 100*df[df.date == t]['deposit_expense'].sum()/df[df.date == t]['total_deposits'].sum() )

plt.close('all')
plt.figure(1)
plt.plot(df.date.unique(),agg_dep,lw=3)
plt.title('Aggregate Nominal Bank Deposits',fontsize=15)
plt.xlabel('Time',fontsize=15)
plt.ylabel('Trillions of Dollars',fontsize=15)

plt.figure(2)
plt.plot(df.date.unique(),agg_exp,lw=3)
plt.title('Aggregate Nominal Bank Deposit Expense',fontsize=15)
plt.xlabel('Time',fontsize=15)
plt.ylabel('Trillions of Dollars',fontsize=15)

plt.figure(3)
plt.plot(df.date.unique(),agg_ret,lw=3)
plt.title('Aggregate Deposit Interest Rate (%)',fontsize=15)
plt.xlabel('Time',fontsize=15)
plt.ylabel('Annualized Interest Return',fontsize=15)
plt.axvspan(df.date.unique()[13], df.date.unique()[18], facecolor='red', alpha=0.25,label='Recession Periods')
plt.axvspan(df.date.unique()[58], df.date.unique()[60], facecolor='red', alpha=0.25)
plt.axvspan(df.date.unique()[85], df.date.unique()[91], facecolor='red', alpha=0.25)
plt.axvspan(df.date.unique()[134], df.date.unique()[135], facecolor='red', alpha=0.25)
plt.legend(fontsize=15)

# cross-sectional dispersion in deposit interest expense

plt.figure(4)
plt.subplot(4,1,1)
t1 = df.date.unique()[0] # 1986 Q3
plt.hist( 100*df[ df.date == t1 ]['deposit_expense']/df[ df.date == t1 ]['total_deposits'],bins=80,range=(0,15) )
plt.xlim(0,10)
plt.yticks([])
plt.ylabel('1986 Q3')

plt.subplot(4,1,2)
t2 = df.date.unique()[30] # 1994 Q1
plt.hist( 100*df[ df.date == t2 ]['deposit_expense']/df[ df.date == t2 ]['total_deposits'],bins=80,range=(0,15) )
plt.xlim(0,10)
plt.yticks([])
plt.ylabel('1994 Q1')

plt.subplot(4,1,3)
t3 = df.date.unique()[60] # 2001 Q3
plt.hist( 100*df[ df.date == t3 ]['deposit_expense']/df[ df.date == t3 ]['total_deposits'],bins=80,range=(0,15) )
plt.xlim(0,10)
plt.yticks([])
plt.ylabel('2001 Q3')


plt.subplot(4,1,4)
t5 = df.date.unique()[125] # 2017 Q4
plt.hist( 100*df[ df.date == t5 ]['deposit_expense']/df[ df.date == t5 ]['total_deposits'],bins=80,range=(0,15) )
plt.xlim(0,10)
plt.yticks([])
plt.ylabel('2017 Q4')
plt.xlabel('Annualized Deposit Rate')
plt.suptitle('Cross-Section of Deposit Rates, By Year',fontsize=15)

rate_disp = []
for at,t in enumerate(df.date.unique()):

    rate_disp.append( 10*np.nanstd( df[df.date == t]['deposit_rate'] ) )

plt.figure(5)
plt.plot(df.date.unique(),rate_disp,lw=3)
plt.xlabel('Date',fontsize=15)
plt.ylabel('Annualized Standard Deviation of Rates (%)',fontsize=15)
plt.title('Standard Deviation of Deposit Rates, By Year',fontsize=15)
plt.ylim(0,.3)

total_bhc = []
for at,t in enumerate(df.date.unique()):

    total_bhc.append( len(np.where( df[df.date == t]['BHCK2170'] > 0)[0]) )

plt.figure(6)
plt.plot(df.date.unique(),total_bhc,lw=3)
plt.title('Total Number of BHCs, By Year',fontsize=15)
plt.xlabel('Date',fontsize=15)
plt.ylabel('# of BHCs',fontsize=15)
plt.axvline( df.date.unique()[79],c='k',lw=3,ls='--',alpha=.3, label='Threshold Change')
plt.axvline( df.date.unique()[115],c='k',lw=3,ls='--',alpha=.3 )
plt.axvline( df.date.unique()[128],c='k',lw=3,ls='--',alpha=.3 )
plt.legend(fontsize=15)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#                                                  #
#    Consumer and Commercial Lending Statistics    #
#                                                  #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

agg_consumer_loan = []
agg_commercial_loan = []
consumer_int = []
commercial_int = []

consumer_rate = []
commercial_rate = []

consumer_nco_rate = []
commercial_nco_rate = []

consumer_nco = []
commercial_nco = []

for at,t in enumerate(df.date.unique()):

    agg_consumer_loan.append(   np.nansum(df[df.date==t]['consumer_loans'])/(1000*1000*1000) )
    agg_commercial_loan.append( np.nansum(df[df.date==t]['commercial_loans'])/(1000*1000*1000) )

    consumer_int.append(   np.nansum(df[df.date==t]['consumer_loan_int'])/(1000*1000*1000) )
    commercial_int.append( np.nansum(df[df.date==t]['commercial_loan_int'])/(1000*1000*1000) )

    consumer_rate.append(   100*np.nansum(df[df.date==t]['consumer_loan_int'])/np.nansum(df[df.date==t]['consumer_loans']) )
    commercial_rate.append( 100*np.nansum(df[df.date==t]['commercial_loan_int'])/np.nansum(df[df.date==t]['commercial_loans']) )

    consumer_nco_rate.append( 100*100*np.nansum(df[df.date==t]['con_nco'])/np.nansum(df[df.date==t]['consumer_loans']) )
    commercial_nco_rate.append( 100*100*np.nansum(df[df.date==t]['com_nco'])/np.nansum(df[df.date==t]['commercial_loans']) )

    consumer_nco.append( np.nansum(df[df.date==t]['con_nco'])/(1000*1000*1000) )
    commercial_nco.append( np.nansum(df[df.date==t]['com_nco'])/(1000*1000*1000) )


plt.close('all')
plt.figure(1)
plt.plot(df.date.unique(),agg_consumer_loan,label='consumer',lw=3)
plt.plot(df.date.unique(),agg_commercial_loan,label='commercial',lw=3,ls='--')
plt.title('Aggregate Nominal Lending',fontsize=15)
plt.xlabel('Time',fontsize=15)
plt.ylabel('Trillions of Dollars',fontsize=15)
plt.legend(fontsize=15)

plt.figure(2)
plt.plot(df.date.unique()[80:],consumer_int[80:],lw=3,label='consumer')
plt.plot(df.date.unique()[80:],commercial_int[80:],lw=3,label='commercial',ls='--')
plt.title('Aggregate Nominal Bank Loan Interest/Fee Income',fontsize=15)
plt.xlabel('Time',fontsize=15)
plt.ylabel('Trillions of Dollars',fontsize=15)
plt.legend(fontsize=15)

plt.figure(3)
plt.plot(df.date.unique()[80:],consumer_rate[80:],lw=3,label='consumer')
plt.plot(df.date.unique()[80:],commercial_rate[80:],lw=3,label='commercial',ls='--')
plt.title('Aggregate Loan Interest Rate (%)',fontsize=15)
plt.xlabel('Time',fontsize=15)
plt.ylabel('Annualized Interest Return',fontsize=15)
#plt.axvspan(df.date.unique()[13], df.date.unique()[18], facecolor='red', alpha=0.25,label='Recession Periods')
#plt.axvspan(df.date.unique()[58], df.date.unique()[60], facecolor='red', alpha=0.25)
plt.axvspan(df.date.unique()[85], df.date.unique()[91], facecolor='red', alpha=0.25)
plt.axvspan(df.date.unique()[134], df.date.unique()[135], facecolor='red', alpha=0.25)
plt.legend(fontsize=15)

plt.figure(4)
plt.plot(df.date.unique()[80:],consumer_nco_rate[80:],lw=3,label='consumer')
plt.plot(df.date.unique()[80:],commercial_nco_rate[80:],lw=3,label='commercial',ls='--')
plt.title('Aggregate Loan NCO Rate (basis points)',fontsize=15)
plt.xlabel('Time',fontsize=15)
plt.ylabel('Annualized Rate (basis points)',fontsize=15)
#plt.axvspan(df.date.unique()[13], df.date.unique()[18], facecolor='red', alpha=0.25,label='Recession Periods')
#plt.axvspan(df.date.unique()[58], df.date.unique()[60], facecolor='red', alpha=0.25)
plt.axvspan(df.date.unique()[85], df.date.unique()[91], facecolor='red', alpha=0.25)
plt.axvspan(df.date.unique()[134], df.date.unique()[135], facecolor='red', alpha=0.25)
plt.legend(fontsize=15)
