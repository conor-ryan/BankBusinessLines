"""
Packages
"""
import numpy as np
import pandas as pd
import re
import os
import matplotlib.pyplot as plt

plt.style.use('seaborn')

#Import dataframe

#os.chdir('/home/pando004/Desktop/BankData/FRY9')
#df = pd.read_csv('frdata.csv')
os.chdir('G:/Shared drives/BankBusinessLines')
# os.chdir('/home/ryan0463/Documents/Research/BankBusinessLines')
df = pd.read_csv('Data/frdata.csv')

# make date variable
df['date'] = pd.to_datetime( df.RSSD9999, format='%Y%m%d')
df = df.sort_values(by=['date'])

# drop dataframe dates to match market size data
df = df[ ~(df['date'] < df.date.unique()[117] ) ]  # drop all observations before 2015 Q4
first_quarter = 3
# drop all observations which report zero net income
df = df.dropna(subset=['BHCK4340'])

# set to zero certain revenue items
df[['BHCK4435','BHCK4436','BHCKF821','BHCK4059','BHCK4065','BHCK4115','BHCK4020','BHCK4518','BHCK4230','BHCK8560','BHCK8561','BHCK4042',
    'BHCKHK03','BHCKHK04','BHCK6761','BHCK4172','BHCK4180','BHCK4185','BHCK4397','BHCK4398','BHCK4483','BHCKC013','BHCKC015','BHCKC016','BHCKT047','BHCKF555',
    'BHCKC887','BHCKC386','BHCKC014','BHCKC387','BHCKKX46','BHCKKX47',
    'BHCK4070','BHCKC886','BHCKC888','BHCKB491','BHCKB492','BHCKB493',
    'BHCKB488','BHCKB489','BHCK4060','BHCK4069','BHCKA220','BHCKB496','BHCK3521','BHCK3196',
    'BHCKB497','BHCK8562','BHCK8563','BHCK8564',
    'BHCK4093','BHCKJA22',
    'BHCK5369','BHCKB529','BHDM6631','BHDM6636','BHFN6631','BHFN6636','BHDMB993','BHCKB995','BHCK3190','BHCKC244','BHCKC248','BHCK0081','BHCK0395','BHCK0397','BHCKJJ34','BHCK1773','BHDMB987','BHCKB989','BHCK3545']] = (
df[['BHCK4435','BHCK4436','BHCKF821','BHCK4059','BHCK4065','BHCK4115','BHCK4020','BHCK4518','BHCK4230','BHCK8560','BHCK8561','BHCK4042',
    'BHCKHK03','BHCKHK04','BHCK6761','BHCK4172','BHCK4180','BHCK4185','BHCK4397','BHCK4398','BHCK4483','BHCKC013','BHCKC015','BHCKC016','BHCKT047','BHCKF555',
    'BHCKC887','BHCKC386','BHCKC014','BHCKC387','BHCKKX46','BHCKKX47',
    'BHCK4070','BHCKC886','BHCKC888','BHCKB491','BHCKB492','BHCKB493',
    'BHCKB488','BHCKB489','BHCK4060','BHCK4069','BHCKA220','BHCKB496','BHCK3521','BHCK3196',
    'BHCKB497','BHCK8562','BHCK8563','BHCK8564',
    'BHCK4093','BHCKJA22',
    'BHCK5369','BHCKB529','BHDM6631','BHDM6636','BHFN6631','BHFN6636','BHDMB993','BHCKB995','BHCK3190','BHCKC244','BHCKC248','BHCK0081','BHCK0395','BHCK0397','BHCKJJ34','BHCK1773','BHDMB987','BHCKB989','BHCK3545']].fillna(0) )


#
#
#
#   Create firm-level measures of business line revenues
#
#
#   (1) Traditional Banking
#       (a) Interest revenue from lending (4435 + 4436 + F821 + 4059)
#       (b) Interest revenue from leases (4065)
#       (c) Interest revenue from lending to financial institutions (4115 + 4020)
#       (d) Other interest revenue (4518)
#       (e) LESS provisions (4230)
#       (f) Net gains on loans, leases, real estate (8560 + 8561)
#       (g) Revenue from other real estate (4042)
#       (h) Add other income with "lease" or "rent" in the description (8562)
#
#   (2) Deposits
#       (a) LESS Interest expense (HK03 + HK04 + 6761 + 4172 + 4180 + 4185 + 4397 + 4398)
#       (b) Deposit service charges (4483)
#       (c) Revenue from checks, atms, safe deposit, wire transfer (C013 + C016 + C015 + T047)
#       (d) Credit card interchange fees (F555)
#
#   (3) Property & Casualty Underwriting (Only for banks with >$10B in Reinsurance Recoverables)
#       (a) Net Income (C246)
#
#   (4) Life & Health Underwriting (Only for banks with >$10B in Reinsurance Recoverables)
#       (a) Net Income (C250)
#
#   (5) Management of Mutual Funds, Annuities, and Life Insurance
#       (a) Fees and Commissions from annuity sales (C887)
#       (b) Income from fiduciary activities (4070)
#       (c) Earnings on/increase in value of cash surrender value of life insurance (C014)
#       (d) Underwriting Income from Insurance and Reinsurance Activities (C386)
#               - For most banks in our sample, this is primarily comprised of premiums (C242, C243)
#               - It's not clear why this revenue is attached to these assets, rather than underwriting equity.
#       (e) Income from the sale and servicing of mutual funds and annuities (8431)
#       (f) LESS Benefits, losses, and expenses from insurance-related activitie (B983)
#
#   (6) Other Insurance Banking (???)
#       (c) Other revenue (C387)
#       (e) LESS Net Income from casualty/property/health/life insurance (3) & (4)
#
#   (7) Investment Banking*
#       (a) Revenue from securities brokerage (C886)
#       (b) Investment banking non-interest revenue (C888)
#       (c) Venture capital (B491)
#       (d) Net servicing fees (B492)
#       (e) Net securitization income (B493)
#
#   (8) Trading/Treasury
#       (a) Interest and dividends on securities (B488 + B489 + 4060)
#       (b) Interest revenue from trading assets (4069)
#       (c) Non-interest trading revenue (A220)
#       (d) Net gains on sales of other assets (B496)
#       (e) Realized gains on securities (3521 + 3196)
#
#   BHCK 4301 is the longer/older data series for pre-tax net income (and before discontinued operations)
#
#   * Holding companies with <$5b do not report items (3) and (4) separately, but instead report Revenue from
#       securities brokerage, investment banking, advisory and underwriting (KX46) and Revenue from insurance
#       activities (KX47).
#
#   - Hard to say whether Fiduciary Activity revenue should be Traditional Banking (as a part of the consumer branch) or Investment Banking
#
#   - 2017Q4 has a large spike in income taxes which is related to the repatriation tax from the 2017 Tax Cuts & Jobs Act
#
#   - Trading assets and trading revenue (4069) are only reported by banks with assets > $5b. IF a bank is below the threshold,
#       they report the revenue and expense in the "other" categories for interest income (4518), interest expense (4398) and noninterest income (B497)
#

#
#
#   Deflate relevant series
#
#

# next steps (1) defalte series (3) less than 5 billion for ibank and insurance, (4) check the accounting identity on pre-tax net income


#
#
#
#   Only keep banks which show up in FR Y-15
#
#

# merge FR Y-15 data with FR Y-9C data
#os.chdir('/home/pando004/Desktop/BankData/FRY15')
#df15 = pd.read_csv('fr15data.csv')
df15 = pd.read_csv('Data/fr15data.csv')

print("Data Read In")

df15['date'] = df15['date'].apply(lambda x: pd.to_datetime(str(x), format='%Y%m%d'))
df15 = df15.sort_values(by=['date'])

# drop 2015 Q4 observations
#df15 = df15[ ~(df15['date'] <= df15.date.unique()[0] ) ]

# collect number of unique IDs in FRY15 data, see how many match with FRY9
fry15_ids = df15.id.unique()
fry9_ids = set( df.RSSD9001.unique() )
it = 0
collect_idx = []
for at,idx in enumerate(df15.id.unique()):
    if idx in fry9_ids:
        collect_idx.append( idx )
        it = it + 1
print(100*it/len(fry15_ids),'% of FRY15 banks in FRY9 dataset')
print()



df_temp = df[ df.RSSD9001 == df15.id.unique()[0] ]

for i in range(1,len(df15.id.unique())):
    df_temp1 = df[ df.RSSD9001 == df15.id.unique()[i] ]

    df_temp = df_temp.append( df_temp1, ignore_index = True )
df = df_temp.copy()



# #
# #
# #   Filter out smaller banks
# #
# #
# # initialize list of bank indices and threshold number N
# top_idx = []
# topN = 50

# # for each quarter
# for at,t in enumerate(df.date.unique()):

#     # determine top N firms by revenue
#     rev_idx = list( (  df[ df.date ==t ]['BHCK4107'] - df[ df.date ==t ]['BHCK4230'] + df[ df.date ==t ]['BHCK4079'] + df[ df.date ==t ]['BHCK3521'] + df[ df.date ==t ]['BHCK3196'] ).nlargest(topN).index )

#     # recover bank id's
#     rev_list = []

#     for i in range(topN):
#         try:
#             rev_list.append( df[df.index == rev_idx[i] ]['RSSD9001'].unique()[0] )
#         except:
#             pass

#     # append list with unique union set
#     top_idx = list( set(rev_list).union( set(top_idx) ) )
#     #top_idx = list( set(con_list).union( set(com_list),set(dep_list),set(ins_list), set(top_idx) ) )

# print('Collected a total of', len(top_idx),' bank IDs')

# #create subset dataframe using bank id's
# for i in range(len(top_idx)):

#     if i ==0:
#         temp_df = df[df.RSSD9001 == top_idx[i]]
#     else:
#         temp_df = temp_df.append( df[df.RSSD9001 == top_idx[i]] )

# df = temp_df.copy()
# df = df.sort_values(by=['date'])




#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#                                      #
#   Bank Business Line Segmentation    #
#                                      #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

df['traditional_revenue'] = 0
df['deposit_revenue'] = 0
df['prop_underwriting_revenue'] = 0
df['life_underwriting_revenue'] = 0
df['annuity_revenue'] = 0
df['othins_revenue'] = 0
df['investment_revenue'] = 0
df['treasury_revenue'] = 0
df['othernonint_revenue'] = 0

df['lease_nonint_revenue'] = 0

### Matching Text Phrase for Operating Lease Revenue
lease_match_pattern = re.compile('Lease|LEASE|lease|Rent|RENT|rent',re.IGNORECASE)

dates = df.date.unique()
dates.sort()
# print(dates)

# first compute quartlery revenue for each bank, each quarter
for idx, bank in enumerate( df.RSSD9001.unique() ):

    print('Traditional Bank:',bank,' ',idx,' out of ',len(df.RSSD9001.unique()))
    quart = first_quarter

    for at, t in enumerate( dates ):
        # print('Quarter ',quart,' at date ',t)
        if at ==0:
            try:
                temp_val = (float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4435']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4436']) +
                            float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKF821']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4059']) +
                            float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4065']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4115']) +
                            float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4020']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4518']) -
                            float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4230']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK8560']) +
                            float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK8561']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4042']))

                temp_val_dep = (float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4483']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC013']) +
                                float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC015']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC016']) +
                                float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKT047']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKF555']) -
                                float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKHK03']) - float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKHK04']) -
                                float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK6761']) - float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4172']) -
                                float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4180']) - float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4185']) -
                                float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4397']) - float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4398']))

                # Small Banks, Ignore at the Moment
                # if float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK2170']) < 5000000:
                #     temp_val_ins = (float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKKX46']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKKX47']))
                #
                #     # there are circumstances in the data where they keep reporting the other categories when assets < 5b
                #     if temp_val_ins ==0:
                #         temp_val_ins = (float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC887']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC386']) +
                #                         float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC014']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC387']))
                # else:
                temp_val_prop = float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC246'])
                temp_val_life = float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC250'])
                temp_val_annu = float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC887']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC014']) +\
                                float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4070']) +\
                                float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC386']) + \
                                float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK8431']) - float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKB983'])
                temp_val_othins = float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC387']) - \
                                float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC246']) - float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC250'])
                temp_val_inv =  float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC886']) +\
                                float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC888']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKB491']) +\
                                float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKB492']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKB493'])

                temp_val_treas = (float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKB488']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKB489']) +\
                                  float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4060']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4069']) +\
                                  float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKA220']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKB496']) +\
                                  float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK3521']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK3196']))


                #print(t,': ',temp_val)
                #print('final:',temp_val)
                # print(temp_val_ins)
                df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'traditional_revenue']   = temp_val
                df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'deposit_revenue']       = temp_val_dep
                df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'prop_underwriting_revenue']     = temp_val_prop
                df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'life_underwriting_revenue']     = temp_val_life
                df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'annuity_revenue']     = temp_val_annu
                df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'othins_revenue']     = temp_val_othins
                df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'investment_revenue']    = temp_val_inv
                df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'treasury_revenue']      = temp_val_treas

            except:
                pass
        else:
            if quart == 0:
                try:
                    temp_val = float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4435']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4436']) + \
                               float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKF821']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4059']) + \
                               float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4065']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4115']) + \
                               float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4020']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4518']) - \
                               float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4230']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK8560']) + \
                               float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK8561']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4042'])

                    temp_val_dep = (float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4483']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC013']) +
                                    float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC015']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC016']) +
                                    float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKT047']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKF555']) -
                                    float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKHK03']) - float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKHK04']) -
                                    float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK6761']) - float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4172']) -
                                    float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4180']) - float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4185']) -
                                    float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4397']) - float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4398']))
                    # if float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK2170']) < 5000000:
                    #     temp_val_ins = (float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKKX46']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKKX47']))
                    #     if temp_val_ins ==0:
                    #         temp_val_ins =  float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC386']) +float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC014'])
                    #         # temp_val_ins = (float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC887']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC386']) +
                    #         #                 float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC014']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC387']))
                    # else:
                    temp_val_prop = float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC246'])
                    temp_val_life = float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC250'])
                    temp_val_annu = float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC887']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC014']) +\
                                    float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4070']) +\
                                    float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC386']) + \
                                    float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK8431']) - float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKB983'])

                    temp_val_othins = float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC387']) - \
                                    float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC246']) - float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC250'])

                    temp_val_inv =  float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC886']) +\
                                    float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC888']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKB491']) +\
                                    float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKB492']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKB493'])

                    temp_val_treas = (float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKB488']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKB489']) +\
                                      float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4060']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4069']) +\
                                      float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKA220']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKB496']) +\
                                      float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK3521']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK3196']))

                    #print(t,': ',temp_val)
                    #print('final:',temp_val)
                    #print()
                    # print(temp_val_ins)
                    df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'traditional_revenue']   = temp_val
                    df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'deposit_revenue']       = temp_val_dep
                    df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'prop_underwriting_revenue']     = temp_val_prop
                    df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'life_underwriting_revenue']     = temp_val_life
                    df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'annuity_revenue']     = temp_val_annu
                    df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'othins_revenue']     = temp_val_othins
                    df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'investment_revenue']    = temp_val_inv
                    df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'treasury_revenue']      = temp_val_treas

                except:
                    pass
            else:

                # determine if bank was operating in previous period before using difference formula
                if df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCK4340'].empty == True:

                    try:
                        temp_val =  float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4435']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4436']) + \
                                    float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKF821']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4059']) + \
                                    float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4065']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4115']) + \
                                    float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4020']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4518']) - \
                                    float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4230']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK8560']) + \
                                    float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK8561']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4042'])

                        temp_val_dep = (float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4483']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC013']) +
                                        float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC015']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC016']) +
                                        float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKT047']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKF555']) -
                                        float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKHK03']) - float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKHK04']) -
                                        float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK6761']) - float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4172']) -
                                        float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4180']) - float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4185']) -
                                        float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4397']) - float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4398']))

                        # if float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK2170']) < 5000000:
                        #     temp_val_ins = (float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKKX46']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKKX47']))
                        #     if temp_val_ins ==0:
                        #         temp_val_ins =  float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC386']) +float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC014'])
                        #         # temp_val_ins = (float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC887']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC386']) +
                        #         #                 float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC014']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC387']))
                        # else:
                        temp_val_prop = float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC246'])
                        temp_val_life = float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC250'])
                        temp_val_annu = float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC887']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC014']) +\
                                        float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4070']) +\
                                        float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC386']) + \
                                        float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK8431']) - float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKB983'])

                        temp_val_othins = float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC387']) - \
                                        float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC246']) - float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC250'])

                        temp_val_inv =  float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC886']) +\
                                        float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC888']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKB491']) +\
                                        float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKB492']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKB493'])

                        temp_val_treas = (float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKB488']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKB489']) +\
                                          float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4060']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4069']) +\
                                          float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKA220']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKB496']) +\
                                          float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK3521']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK3196']))

                        #print(t,': ',temp_val)
                        #print('final:',temp_val)
                        #print()
                        # print(temp_val_ins)
                        df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'traditional_revenue']   = temp_val
                        df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'deposit_revenue']       = temp_val_dep
                        df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'prop_underwriting_revenue']     = temp_val_prop
                        df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'life_underwriting_revenue']     = temp_val_life
                        df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'annuity_revenue']     = temp_val_annu
                        df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'othins_revenue']     = temp_val_othins
                        df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'investment_revenue']    = temp_val_inv
                        df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'treasury_revenue']      = temp_val_treas

                    except:
                        pass

                else:
                    try:
                        temp_val_one =  float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4435']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4436']) + \
                                        float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKF821']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4059']) + \
                                        float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4065']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4115']) + \
                                        float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4020']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4518']) - \
                                        float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4230']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK8560']) + \
                                        float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK8561']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4042'])

                        temp_val_two =  float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCK4435']) + float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCK4436']) + \
                                        float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCKF821']) + float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCK4059']) + \
                                        float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCK4065']) + float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCK4115']) + \
                                        float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCK4020']) + float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCK4518']) - \
                                        float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCK4230']) + float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCK8560']) + \
                                        float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCK8561']) + float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCK4042'])

                        temp_val_dep_one = (float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4483']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC013']) +
                                            float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC015']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC016']) +
                                            float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKT047']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKF555']) -
                                            float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKHK03']) - float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKHK04']) -
                                            float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK6761']) - float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4172']) -
                                            float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4180']) - float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4185']) -
                                            float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4397']) - float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4398']))

                        temp_val_dep_two = (float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCK4483']) + float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCKC013']) +
                                            float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCKC015']) + float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCKC016']) +
                                            float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCKT047']) + float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCKF555']) -
                                            float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCKHK03']) - float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCKHK04']) -
                                            float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCK6761']) - float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCK4172']) -
                                            float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCK4180']) - float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCK4185']) -
                                            float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCK4397']) - float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCK4398']))

                        # if float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK2170']) < 5000000:
                        #     temp_val_ins_one = (float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKKX46']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKKX47']))
                        #     temp_val_ins_two = (float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCKKX46']) + float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCKKX47']))
                        #     if temp_val_ins_one ==0:
                        #         temp_val_ins_one =  float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC386']) +float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC014'])
                        #         # temp_val_ins = (float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC887']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC386']) +
                        #         #                 float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC014']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC387']))
                        #         temp_val_ins_two =  float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCKC386']) +float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCKC014'])
                        #         # temp_val_ins_two = (float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCKC887']) + float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCKC386']) +
                        #         #                     float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCKC014']) + float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCKC387']))
                        # else:
                        temp_val_prop_one = float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC246'])
                        temp_val_life_one = float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC250'])
                        temp_val_annu_one = float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC887']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC014']) +\
                                        float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4070']) +\
                                        float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC386']) + \
                                        float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK8431']) - float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKB983'])

                        temp_val_othins_one = float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC387']) - \
                                        float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC246']) - float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC250'])

                        temp_val_inv_one =  float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC886']) +\
                                        float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC888']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKB491']) +\
                                        float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKB492']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKB493'])

                        temp_val_treas_one = (float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKB488']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKB489']) +\
                                          float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4060']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4069']) +\
                                          float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKA220']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKB496']) +\
                                          float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK3521']) + float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK3196']))

                        temp_val_prop_two = float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCKC246'])
                        temp_val_life_two = float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCKC250'])
                        temp_val_annu_two = float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCKC887']) + float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCKC014']) +\
                                        float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCK4070']) +\
                                        float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCKC386']) + \
                                        float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCK8431']) - float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCKB983'])

                        temp_val_othins_two = float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCKC387']) - \
                                        float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCKC246']) - float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCKC250'])

                        temp_val_inv_two =  float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCKC886']) +\
                                        float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCKC888']) + float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCKB491']) +\
                                        float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCKB492']) + float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCKB493'])

                        temp_val_treas_two = (float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCKB488']) + float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCKB489']) +\
                                          float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCK4060']) + float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCK4069']) +\
                                          float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCKA220']) + float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCKB496']) +\
                                          float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCK3521']) + float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCK3196']))
                        #print(t,': ',temp_val_one)
                        #print('final:',temp_val_one-temp_val_two)
                        # print(temp_val_ins_one)
                        df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'traditional_revenue']   = temp_val_one - temp_val_two
                        df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'deposit_revenue']       = temp_val_dep_one - temp_val_dep_two
                        df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'prop_underwriting_revenue']     = temp_val_prop_one - temp_val_prop_two
                        df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'life_underwriting_revenue']     = temp_val_life_one - temp_val_life_two
                        df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'annuity_revenue']     = temp_val_annu_one - temp_val_annu_two
                        df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'othins_revenue']     = temp_val_othins_one - temp_val_othins_two
                        df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'investment_revenue']    = temp_val_inv_one - temp_val_inv_two
                        df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'treasury_revenue']      = temp_val_treas_one - temp_val_treas_two

                    except:
                        pass

        if quart < 3:
            quart = quart + 1
        else:
            quart = 0

#df[ df.RSSD9001 == df.RSSD9001.unique()[0] ][['RSSD9017','RSSD9001','date','traditional_revenue']]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#                                           #
#   Filtering Other Non-Interest Revenue    #
#                                           #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

# simple version (split other non-interest equally across all the activities)


# trad_keyword = [ 'Loan', 'Lease', 'Mortgage','Auto','Commitment','LOAN', 'LEASE', 'MORTGAGE','AUTO','COMMITMENT' ]
# dep_keyword = [ 'Deposit', 'Card','Acceptance','DEPOSIT', 'CARD','ACCEPTANCE']
# ins_keyword = ['Insurance','INSURANCE']
# inv_keyword = ['Ipo', 'Offering', 'Derivative', 'Management','Spread','IPO', 'OFFERING', 'DERIVATIVE', 'MANAGEMENT','SPREAD']
# treas_keyword = ['Investment','INVESTMENT']

# first compute quartlery revenue for each bank, each quarter
for idx, bank in enumerate( df.RSSD9001.unique() ):

    # print('Traditional Bank:',idx,' out of ',len(df.RSSD9001.unique()))
    quart = first_quarter
    for at, t in enumerate( dates ):
        # print('Quarter ',quart,' at date ',t)
        if at ==0:
            try:
                temp_val = float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKB497']) - \
                           float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC013']) - \
                           float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC014']) - \
                           float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC016']) - \
                           float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4042']) - \
                           float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC015']) - \
                           float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKF555']) - \
                           float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKT047'])

                df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'othernonint_revenue']   = temp_val


                text_value = df[ (df.date==t) & (df.RSSD9001 == bank) ]['TEXT8562']
                if lease_match_pattern.search(text_value):
                    temp_val_lease = float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK8562'])
                else:
                    temp_val_lease= 0

                df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'lease_nonint_revenue']   = temp_val_lease

            except:
                pass

        else:
            if quart == 0:
                try:
                    temp_val = float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKB497']) - \
                               float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC013']) - \
                               float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC014']) - \
                               float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC016']) - \
                               float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4042']) - \
                               float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC015']) - \
                               float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKF555']) - \
                               float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKT047'])

                    df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'othernonint_revenue']   = temp_val

                    text_value = df.loc[ (df.date==dates[at-1]) & (df.RSSD9001 == bank), 'TEXT8562'].item()

                    # print(text_value,' at time ',t)
                    if lease_match_pattern.search(text_value):
                        # print("Lease Revenue Found")
                        temp_val_lease = float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK8562'])
                    else:
                        temp_val_lease= 0

                    df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'lease_nonint_revenue']   = temp_val_lease

                except:
                    pass

            else:

                # determine if bank was operating in previous period before using difference formula
                if df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCK4340'].empty == True:

                    try:
                        temp_val = float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKB497']) - \
                                   float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC013']) - \
                                   float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC014']) - \
                                   float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC016']) - \
                                   float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4042']) - \
                                   float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC015']) - \
                                   float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKF555']) - \
                                   float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKT047'])

                        df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'othernonint_revenue']   = temp_val

                        text_value = df.loc[ (df.date==dates[at-1]) & (df.RSSD9001 == bank), 'TEXT8562'].item()
                        if lease_match_pattern.search(text_value):
                            temp_val_lease = float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK8562'])
                        else:
                            temp_val_lease= 0

                        df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'lease_nonint_revenue']   = temp_val_lease


                    except:
                        pass

                else:
                    try:
                        temp_val_one = float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKB497']) - \
                                       float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC013']) - \
                                       float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC014']) - \
                                       float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC016']) - \
                                       float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4042']) - \
                                       float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKC015']) - \
                                       float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKF555']) - \
                                       float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCKT047'])

                        temp_val_two = float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCKB497']) - \
                                       float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCKC013']) - \
                                       float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCKC014']) - \
                                       float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCKC016']) - \
                                       float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCK4042']) - \
                                       float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCKC015']) - \
                                       float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCKF555']) - \
                                       float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCKT047'])

                        df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'othernonint_revenue']   = (temp_val_one-temp_val_two)

                        text_value = df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'TEXT8562'].item()
                        if lease_match_pattern.search(text_value):
                            temp_val_lease_one = float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK8562'])
                        else:
                            temp_val_lease_one = 0


                        text_value = df.loc[ (df.date==dates[at-1]) & (df.RSSD9001 == bank), 'TEXT8562'].item()
                        if lease_match_pattern.search(text_value):
                            temp_val_lease_two = float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCK8562'])
                        else:
                            temp_val_lease_two= 0

                        df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'lease_nonint_revenue']   = temp_val_lease_one - temp_val_lease_two

                    except:
                        pass

        if quart < 3:
            quart = quart + 1
        else:
            quart = 0

# annualize the non-interest expense category and reported net income
df['Expense'] = 0
df['Net_Income'] = 0

for idx, bank in enumerate( df.RSSD9001.unique() ):
    quart = first_quarter

    for at, t in enumerate( dates ):

        # print('Quarter ',quart,' at date ',t)
        if at ==0:
            try:
                df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'Expense']   = float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4093'])
                df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'Net_Income']   = float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4301'])
            except:
                pass

        else:
            if quart == 0:
                try:
                    df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'Expense']   =  float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4093'])
                    df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'Net_Income']   =  float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4301'])
                except:
                    pass

            else:

                # determine if bank was operating in previous period before using difference formula
                if df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCK4340'].empty == True:

                    try:
                        df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'Expense']   =  float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4093'])
                        df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'Net_Income']   =  float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4301'])
                    except:
                        pass

                else:
                    try:
                        df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'Expense']      =  float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4093']) -  float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCK4093'])
                        df.loc[ (df.date==t) & (df.RSSD9001 == bank), 'Net_Income']      =  float(df[ (df.date==t) & (df.RSSD9001 == bank) ]['BHCK4301']) -  float(df[ (df.date==dates[at-1]) & (df.RSSD9001 == bank) ]['BHCK4301'])
                    except:
                        pass

        if quart < 3:
            quart = quart + 1
        else:
            quart = 0




#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#                                              #
#   Compute Business Line Quantities/Stocks    #
#                                              #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


#
#
#   Create firm-level measures of business line quantities
#
#
#   (1) Traditional Banking
#       (a) Loans and leases (5369 + B529)
#
#   (2) Deposits
#       (a) deposits (BHDM 6631 + BHDM 6636 + BHFN 6631 + BHFN 6636)
#       (b) fed funds and repo (BHDM B993 + BHCK B995)
#       (c) Other borrowed money (BHCK 3190)
#
#   (3) Property and Casualty Underwriting
#       (a) Property and casualty underwriting equity (C245)
#
#   (4) Life and Health Underwriting
#       (a) Life and health underwriting equity (C249)
#
#   (5) Mutual Funds, Annuities, Life Insurance Management
#       (a) Cash-surrender value of life insurance policies (K201, K202, K270)
#       (b) Proprietary mutual funds and annuities (B570)
#
#   (6) Investment Banking*
#       (a) Underwriting volume (RISK M408 from FR Y-15)
#
#   (7) Trading/Treasury
#       (a) cash (0081 + 0395 + 0397)
#       (b) securities (JJ34 + 1773 + JA22)
#       (c) fed funds and reverse repo (BHDM B987 + B989)
#       (d) trading assets (3545)


df['traditional_q'] = df['BHCK5369'] + df['BHCKB529']
df['deposits_q']    = df['BHDM6631'] + df['BHDM6636'] + df['BHFN6631'] + df['BHFN6636'] + df['BHDMB993'] + df['BHCKB995'] + df['BHCK3190']
df['prop_underwriting_q'] = df['BHCKC245']
df['life_underwriting_q'] = df['BHCKC249']
df['annuity_q'] = df['BHCKK201'] + df['BHCKK202'] + df['BHCKK270'] +  df['BHCKB570']
df['investment_q']  = 0
df['treasury_q']    = df['BHCK0081'] + df['BHCK0395'] + df['BHCK0397'] + df['BHCKJJ34'] + df['BHCK1773'] + df['BHCKJA22'] + df['BHDMB987'] + df['BHCKB989'] + df['BHCK3545']


# create temp dataframe
df_temp = pd.DataFrame()

# some fry 15 periods missing, relative to FR Y9
for idx,bank in enumerate(df.RSSD9001.unique()):

    print('Bank:',idx,' out of',len(df.RSSD9001.unique()))

    # find the set of dates which overlap
    keep_dates = list( set(df15[ df15.id == bank]['date']) & set(df[ df.RSSD9001 == bank]['date']) )
    keep_dates.sort()

    for i in range(len(keep_dates)):

        df.loc[ (df.RSSD9001 == bank) & (df.date == keep_dates[i]), 'investment_q'] = float(df15[ (df15.id == bank) & (df15.date == keep_dates[i]) ]['underwriting']) + float(df15[ (df15.id == bank) & (df15.date == keep_dates[i]) ]['custody']) + float(df15[ (df15.id == bank) & (df15.date == keep_dates[i]) ]['payments'])

        df_temp = df_temp.append( df[ (df.RSSD9001 == bank) & (df.date == keep_dates[i]) ])

df = df_temp.copy()


# compute prices
df['traditional_p'] = df['traditional_revenue']/df['traditional_q']
df['deposits_p']     = df['deposit_revenue']    /df['deposits_q']
df['prop_underwriting_p']   = df['prop_underwriting_revenue']  /df['prop_underwriting_q']
df['life_underwriting_p']   = df['life_underwriting_revenue']  /df['life_underwriting_q']
df['annuity_p']   = df['annuity_revenue']  /df['annuity_q']
df['investment_p']  = df['investment_revenue'] /df['investment_q']
df['treasury_p']    = df['treasury_revenue']  /df['treasury_q']

# Prices are zero if quantity is 0
df.loc[df.traditional_q == 0,'traditional_p' ] = 0
df.loc[df.deposits_q == 0 ,'deposits_p']= 0
df.loc[df.prop_underwriting_q == 0 ,'prop_underwriting_p']= 0
df.loc[df.life_underwriting_q == 0 ,'life_underwriting_p']= 0
df.loc[df.annuity_q == 0 ,'annuity_p']= 0
df.loc[df.investment_q == 0 ,'investment_p']= 0
df.loc[df.treasury_q == 0 ,'treasury_p']= 0




df['Bank_ID'] = df['RSSD9001']
df['Bank_Name'] = df['RSSD9017']
df['Assets'] = df['BHCK2170']

# check that accounting identity holds for reported net income

df['NI_computed'] = 0
df['NI_Residual'] = 0

#for each bank
for idx, bank in enumerate( df.Bank_ID.unique() ):

    # compute residual between reported net income and ( revenues - expenses )
    computed_ni = df[df.Bank_ID == bank]['traditional_revenue'] + df[df.Bank_ID == bank]['deposit_revenue'] + \
                  df[df.Bank_ID == bank]['prop_underwriting_revenue']   + df[df.Bank_ID == bank]['life_underwriting_revenue']   +\
                  df[df.Bank_ID == bank]['annuity_revenue']   + df[df.Bank_ID == bank]['othins_revenue']   +\
                  df[df.Bank_ID == bank]['investment_revenue'] + df[df.Bank_ID == bank]['othernonint_revenue'] +\
                  df[df.Bank_ID == bank]['treasury_revenue']    - df[df.Bank_ID == bank]['Expense']

    df.loc[df.Bank_ID == bank,'NI_computed'] = computed_ni
    df.loc[df.Bank_ID == bank,'NI_Residual'] = computed_ni - df[df.Bank_ID == bank]['Net_Income']

#~~~~~~~~~~~~~~~~~~#
#                  #
#   Export Data    #
#                  #
#~~~~~~~~~~~~~~~~~~#

# export dataframe
df[['Bank_ID','Bank_Name','date','Assets','Net_Income','Expense',
    'traditional_revenue','deposit_revenue','prop_underwriting_revenue','life_underwriting_revenue','annuity_revenue','othins_revenue','investment_revenue','treasury_revenue','othernonint_revenue','lease_nonint_revenue',
    'traditional_q','deposits_q','prop_underwriting_q','life_underwriting_q','annuity_q','investment_q','treasury_q',
    'traditional_p','deposits_p','prop_underwriting_p','life_underwriting_p','annuity_p','investment_p','treasury_p','NI_computed','NI_Residual']].to_csv('Data/filtered_data.csv')

print("Data Export Complete")


#### This stuff is all broken now. 

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#                                #
#   Create Data Summary Table    #
#                                #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


# row variables: Q_deposit, Q_traditional, Q_insurance, Q_investment, Q_treasury,
#                p_deposit, p_traditional, p_insurance, p_investment, p_treasury,
#                net income/equity (roe), costs/assets
#
#   column variables: N, mean, 10th, median, 90th, 99th percentile

holder  = np.zeros(( 13, 6 ))

holder[0,:] = np.array(( len(df.deposits_q), int(np.mean(df.deposits_q)/(1000*1000)), int(np.quantile(df.deposits_q,.1)/(1000*1000)), int(np.quantile(df.deposits_q,.5)/(1000*1000)), int(np.quantile(df.deposits_q,.9)/(1000*1000)), int(np.quantile(df.deposits_q,.99)/(1000*1000)) ))
holder[1,:] = np.array(( len(df.traditional_q), int(np.mean(df.traditional_q)/(1000*1000)), int(np.quantile(df.traditional_q,.1)/(1000*1000)), int(np.quantile(df.traditional_q,.5)/(1000*1000)), int(np.quantile(df.traditional_q,.9)/(1000*1000)), int(np.quantile(df.traditional_q,.99)/(1000*1000)) ))
holder[2,:] = np.array(( len(df.insurance_q), int(np.mean(df.insurance_q)/(1000*1000)), int(np.quantile(df.insurance_q,.1)/(1000*1000)), int(np.quantile(df.insurance_q,.5)/(1000*1000)), int(np.quantile(df.insurance_q,.9)/(1000*1000)), int(np.quantile(df.insurance_q,.99)/(1000*1000)) ))
holder[3,:] = np.array(( len(df.investment_q), int(np.mean(df.investment_q)/(1000*1000)), int(np.quantile(df.investment_q,.1)/(1000*1000)), int(np.quantile(df.investment_q,.5)/(1000*1000)), int(np.quantile(df.investment_q,.9)/(1000*1000)), int(np.quantile(df.investment_q,.99)/(1000*1000)) ))
holder[4,:] = np.array(( len(df.treasury_q), int(np.mean(df.treasury_q)/(1000*1000)), int(np.quantile(df.treasury_q,.1)/(1000*1000)), int(np.quantile(df.treasury_q,.5)/(1000*1000)), int(np.quantile(df.treasury_q,.9)/(1000*1000)), int(np.quantile(df.treasury_q,.99)/(1000*1000)) ))

holder[5,:] = np.array(( len(df.deposits_p), 100*100*np.mean(df.deposits_p), round(100*100*np.quantile(df.deposits_p,.1),1), round(100*100*np.quantile(df.deposits_p,.5),1), round(100*100*np.quantile(df.deposits_p,.9),1), round(100*100*np.quantile(df.deposits_p,.99),1) ))
holder[6,:] = np.array(( len(df.traditional_p), round(100*100*np.mean(df.traditional_p),1), round(100*100*np.quantile(df.traditional_p,.1),1), round(100*100*np.quantile(df.traditional_p,.5),1), round(100*100*np.quantile(df.traditional_p,.9),1), round(100*100*np.quantile(df.traditional_p,.99),1) ))
holder[7,:] = np.array(( len(df[ df.insurance_q > 0]['insurance_p']), round(100*100*np.mean(df[ df.insurance_q > 0]['insurance_p']),1), round(100*100*np.quantile(df[ df.insurance_q > 0]['insurance_p'],.1),1), round(100*100*np.quantile(df[ df.insurance_q > 0]['insurance_p'],.5),1), round(100*100*np.quantile(df[ df.insurance_q > 0]['insurance_p'],.9),1), round(100*100*np.quantile(df[ df.insurance_q > 0]['insurance_p'],.99),1) ))
holder[8,:] = np.array(( len(df[ df.investment_q > 0]['investment_p']), round(100*100*np.mean(df[ df.investment_q > 0]['investment_p']),1), round(100*100*np.quantile(df[ df.investment_q > 0]['investment_p'],.1),1), round(100*100*np.quantile(df[ df.investment_q > 0]['investment_p'],.5),1), round(100*100*np.quantile(df[ df.investment_q > 0]['investment_p'],.9),1), round(100*100*np.quantile(df[ df.investment_q > 0]['investment_p'],.99),1) ))
holder[9,:] = np.array(( len(df.treasury_p), round(100*100*np.mean(df.treasury_p),1), round(100*100*np.quantile(df.treasury_p,.1),1), round(100*100*np.quantile(df.treasury_p,.5),1), round(100*100*np.quantile(df.treasury_p,.9),1), round(100*100*np.quantile(df.treasury_p,.99),1) ))

holder[10,:] = np.array(( len(df.Net_Income/df.BHCKG105), round(100*100*np.mean(df.Net_Income/df.BHCKG105)), round(100*100**np.quantile(df.Net_Income/df.BHCKG105,.1),1),round(100*100**np.quantile(df.Net_Income/df.BHCKG105,.5),1), round(100*100**np.quantile(df.Net_Income/df.BHCKG105,.9),1), round(100*100**np.quantile(df.Net_Income/df.BHCKG105,.99),1)  ))
holder[11,:] = np.array(( len(df.Expense/df.Assets), round(100*100*np.mean(df.Expense/df.Assets)), round(100*100**np.quantile(df.Expense/df.Assets,.1),1),round(100*100**np.quantile(df.Expense/df.Assets,.5),1), round(100*100**np.quantile(df.Expense/df.Assets,.9),1), round(100*100**np.quantile(df.Expense/df.Assets,.99),1)  ))
holder[12,:] = np.array(( len(df.Assets), int(np.mean(df.Assets)/(1000*1000)), int(np.quantile(df.Assets,.1)/(1000*1000)), int(np.quantile(df.Assets,.5)/(1000*1000)), int(np.quantile(df.Assets,.9)/(1000*1000)), int(np.quantile(df.Assets,.99)/(1000*1000)) ))

d = {'Objects': np.array(( 'Total Deposits (billions)', 'Traditional Lending (billions)', 'Insured Assets (billions)', 'Investment Activity (billions)', 'Treasury Assets (billions)',
                            'Deposit Rate','Lending Rate','Insurance Premium','Investment Fee','Treasury Return',
                            'Return on Equity', 'Total Cost per Asset','Total Assets (billions)')),
     'N': holder[:,0],
     'Mean': holder[:,1],
     '10p': holder[:,2],
     'Median': holder[:,3],
     '90p': holder[:,4],
     '99p': holder[:,5]}

dfp = pd.DataFrame( data = d )

# os.chdir('/home/pando004/Desktop/BankData/FRY9')
os.chdir('/home/ryan0463/Documents/Research/BankBusinessLines')

with open( os.path.join(os.getcwd(), "business_line.tex"), "w"
  )  as file:
        file.write( dfp[[ 'Objects','N','Mean','10p','Median','90p','99p']].to_latex(
            float_format="%.1f",
            header= ['Objects','N','Mean','10p','Median','90p','99p'],
            index=False,
            caption="This is caption",
            label="tab:forecast_table",
            column_format = "ccccccc") )




with open( os.path.join(os.getcwd(), "forecast.tex"), "w"
  )  as file:
        file.write( df[[ 'State','15 Yr P','30 Yr P','45 Yr P',
                                 '15 Yr F','30 Yr F','45 Yr F',
                                 '15 Yr T','30 Yr T','45 Yr T',
                                 '15 Yr V','30 Yr V','45 Yr V']].to_latex(
            float_format="%.1f",
            header= ['State','15y','30y','45y','15y','30y','45y','15y','30y','45y','15y','30y','45y'],
            index=False,
            caption="This is caption",
            label="tab:forecast_table",
            column_format = "ccccccccccccc") )



































#~~~~~~~~~~~~~~~~~~~~~~#
#                      #
#   Other data work    #
#                      #
#~~~~~~~~~~~~~~~~~~~~~~#
# construct aggregate revenue, total cost and net income measures
agg_revenue = []
agg_cost = []
other_inc = []
reported_ni = []
taxes = []

quart = 0
for at, t in enumerate( df.date.unique() ):

    # if first quarter, just report the accumulated flows
    if quart == 0:
        agg_revenue.append(  np.nansum( df[ df.date ==t ]['BHCK4107'] - df[ df.date ==t ]['BHCK4230'] + df[ df.date ==t ]['BHCK4079'] +
                                       df[ df.date ==t ]['BHCK3521'] + df[ df.date ==t ]['BHCK3196'] - df[ df.date ==t ]['BHCK4230']  )/(1000*1000) )

        agg_cost.append(  np.nansum( df[ df.date ==t ]['BHCK4073'] + df[ df.date ==t ]['BHCK4093'] )/(1000*1000) )

        other_inc.append(  np.nansum( - df[ df.date ==t ]['BHCK4302'] - df[ df.date ==t ]['BHCKG103'] ) /(1000*1000) )

        reported_ni.append( np.nansum( df[ df.date ==t ]['BHCK4340'] )/(1000*1000) )

    else:
        agg_revenue.append( np.nansum( df[ df.date ==t ]['BHCK4107'] - df[ df.date ==t ]['BHCK4230'] + df[ df.date ==t ]['BHCK4079'] +
                                       df[ df.date ==t ]['BHCK3521'] + df[ df.date ==t ]['BHCK3196'] - df[ df.date ==t ]['BHCK4230']  )/(1000*1000)  -
                           np.nansum( df[ df.date == df.date.unique()[at-1] ]['BHCK4107'] - df[ df.date == df.date.unique()[at-1] ]['BHCK4230'] + df[ df.date == df.date.unique()[at-1] ]['BHCK4079'] +
                           df[ df.date == df.date.unique()[at-1] ]['BHCK3521'] + df[ df.date == df.date.unique()[at-1] ]['BHCK3196'] - df[ df.date == df.date.unique()[at-1] ]['BHCK4230'] )/(1000*1000) )

        agg_cost.append( np.nansum( df[ df.date ==t ]['BHCK4073'] + df[ df.date ==t ]['BHCK4093'] )/(1000*1000)  -
                           np.nansum( df[ df.date == df.date.unique()[at-1] ]['BHCK4073'] + df[ df.date == df.date.unique()[at-1] ]['BHCK4093'] )/(1000*1000) )

        other_inc.append( np.nansum( - df[ df.date ==t ]['BHCK4302'] - df[ df.date ==t ]['BHCKG103'] )/(1000*1000)  - np.nansum( - df[ df.date == df.date.unique()[at-1] ]['BHCK4302'] - df[ df.date == df.date.unique()[at-1] ]['BHCKG103'])/(1000*1000) )

        reported_ni.append( np.nansum( df[ df.date ==t ]['BHCK4340']  )/(1000*1000)  -
                           np.nansum( df[ df.date == df.date.unique()[at-1] ]['BHCK4340'] )/(1000*1000) )

    if quart < 3:
        quart = quart + 1
    else:
        quart = 0

# other income includes (i) income tax and net income which is attributed to minority interests
#   there are other categories (such as gains on equity securities not held for trading or discountinued operations but they only start around 2015)
plt.close('all')
cut_off = 0
plt.figure(1)
plt.plot(df.date.unique()[cut_off:],agg_revenue[cut_off:],lw=3,label='Revenue')
plt.plot(df.date.unique()[cut_off:],agg_cost[cut_off:],lw=3,label='Expenses')
plt.plot(df.date.unique()[cut_off:],other_inc[cut_off:],lw=3,label='Other Net Income')
plt.legend(fontsize=15)
plt.title('US Banking Aggregates',fontsize=15)
plt.xlabel('Date',fontsize=15)
plt.ylabel('$ Billion',fontsize=15)


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
