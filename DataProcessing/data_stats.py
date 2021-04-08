"""
Packages
"""
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

plt.style.use('ggplot')
#print(plt.style.available)

#Import dataframe
os.chdir('/home/pando004/Desktop/BankData/FRY9')
df = pd.read_csv('frdata.csv')

# make date variable
df['date'] = pd.to_datetime( df.RSSD9999, format='%Y%m%d')


df = df.sort_values(by=['date'])


# create weight, by assets under management
asset_weight = []
for at,t in enumerate( df.date.unique() ):

    #compute total assets
    total = df[ df.date == t]['BHCK2170'].sum()
        
    #create weights assets/(total_assets)
    weight = df[ df.date == t]['BHCK2170']/total
                 
    asset_weight.append(weight)

#--------------------------#
#                          # 
#   BALANCE SHEET ITEMS    #
#                          # 
#--------------------------#

"""
    OTHER ASSET CATEGORIES AND OTHER LIABILITY CATEGORIES WAY TOO BIG (PARTICULARLY FOR BIG BANKS)
    
    FOR ASSETS, INCLUDE - FED FUNDS/REPO (BHDMB987 + BHCKB989)  (BHCK0276 + 0277 on older forms)
                        - Trading Assets (BHCK 3545)    ()
                        
    FOR LIABILITIES, INCLUDE - OTHER BORROWED MONEY (BHCK 3190) (BHCK 2332 + 2333 on older forms)
                             - SUBORDINATED NOTES (BHCK 4062 + BHCK C699)   (just 4062 no older forms)
                             
"""   
loan_other = []
loan_top = []

cash_other = []
cash_top = []

sec_other = []
sec_top = []

repo_other_beg = []
repo_other_med = []
repo_other_post = []
repo_other = []

repo_top_beg = []
repo_top_med = []
repo_top_post = []
repo_top = [] 

trade_other = []
trade_top = []

quant = .95

for at, t in enumerate( df.date.unique() ):

    # total assets
    total_asset_other = df[ (df.date == t) & (df.BHCK2170 < df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK2170'].sum()
    total_asset_top = df[ (df.date == t) & (df.BHCK2170 > df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK2170'].sum()

    # loans 
    loan_other.append( 100*df[ (df.date == t) & (df.BHCK2170 < df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK2122'].sum()/total_asset_other  )
    loan_top.append( 100*df[ (df.date == t) & (df.BHCK2170 > df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK2122'].sum()/total_asset_top  )
    
    # cash
    cash_other.append( 100*(df[(df.date == t) & (df.BHCK2170 < df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK0081'] +
                           df[(df.date == t) & (df.BHCK2170 < df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK0395'] +
                           df[(df.date == t) & (df.BHCK2170 < df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK0397']).sum()/total_asset_other )
    
    cash_top.append(   100*(df[(df.date == t) & (df.BHCK2170 > df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK0081'] +
                           df[(df.date == t) & (df.BHCK2170 > df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK0395'] +
                           df[(df.date == t) & (df.BHCK2170 > df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK0397']).sum()/total_asset_top )
    
    # securities
    sec_other.append( 100*(df[(df.date == t) & (df.BHCK2170 < df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK1754'] +
                            df[(df.date == t) & (df.BHCK2170 < df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK1773']).sum()/total_asset_other  )
    
    sec_top.append(    100*(df[(df.date == t) & (df.BHCK2170 > df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK1754'] +
                            df[(df.date == t) & (df.BHCK2170 > df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK1773']).sum()/total_asset_top )
    
    # repo/fed funds as assets
    repo_other_beg.append( 100*(df[(df.date == t) & (df.BHCK2170 < df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK0276'] +
                                df[(df.date == t) & (df.BHCK2170 < df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK0277']).sum()/total_asset_other )
    
    repo_other_med.append( 100*df[(df.date == t) & (df.BHCK2170 < df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK1350'].sum()/total_asset_other  )
    
    repo_other_post.append( 100*(df[(df.date == t) & (df.BHCK2170 < df[ df.date == t]['BHCK2170'].quantile(quant))]['BHDMB987'] +
                                   df[(df.date == t) & (df.BHCK2170 < df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCKB989'] ).sum()/total_asset_other )

    repo_top_beg.append( 100*(df[(df.date == t) & (df.BHCK2170 > df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK0276'] +
                                df[(df.date == t) & (df.BHCK2170 > df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK0277']).sum()/total_asset_top )
    
    repo_top_med.append( 100*df[(df.date == t) & (df.BHCK2170 > df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK1350'].sum()/total_asset_top  )
    
    repo_top_post.append( 100*(df[(df.date == t) & (df.BHCK2170 > df[ df.date == t]['BHCK2170'].quantile(quant))]['BHDMB987'] +
                                   df[(df.date == t) & (df.BHCK2170 > df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCKB989'] ).sum()/total_asset_top )

    # trading assets
    trade_other.append( 100*(df[(df.date == t) & (df.BHCK2170 < df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK3545'] ).sum()/total_asset_other )

    trade_top.append( 100*(df[(df.date == t) & (df.BHCK2170 > df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK3545'] ).sum()/total_asset_top )
    
  
plt.close('all')
plt.figure(1)
plt.plot(df.date.unique()[:-1],loan_other[:-1],label='<Quantile %s'%quant,lw=3)
plt.plot(df.date.unique()[:-1],loan_top[:-1],label='>Quantile %s'%quant,lw=3)   
plt.title('Loans as % of Assets',fontsize=15)
plt.xlabel('Date',fontsize=15)
plt.ylabel('Loan Portfolio (%)',fontsize=15)
plt.legend(fontsize=15) 

plt.figure(2)
plt.plot(df.date.unique()[:-1],cash_other[:-1],label='<Quantile %s'%quant,lw=3)
plt.plot(df.date.unique()[:-1],cash_top[:-1],label='>Quantile %s'%quant,lw=3) 
plt.title('Cash as % of Assets',fontsize=15)
plt.xlabel('Date',fontsize=15)
plt.ylabel('Cash Portfolio (%)',fontsize=15)
plt.legend(fontsize=15) 

plt.figure(3)
plt.plot(df.date.unique()[30:-1],sec_other[30:-1],label='<Quantile %s'%quant,lw=3) 
plt.plot(df.date.unique()[30:-1],sec_top[30:-1],label='>Quantile %s'%quant,lw=3) 
plt.title('Securities as % of Assets',fontsize=15)
plt.xlabel('Date',fontsize=15)
plt.ylabel('Securities Portfolio (%)',fontsize=15)
plt.legend(fontsize=15) 

repo_other = np.concatenate(( repo_other_med[:7], repo_other_beg[7:42], repo_other_med[42:62],repo_other_post[62:]  ))
repo_top = np.concatenate(( repo_top_med[:7], repo_top_beg[7:42], repo_top_med[42:62],repo_top_post[62:]  ))

plt.figure(4)
plt.plot(df.date.unique()[:-1],repo_other[:-1],label='<Quantile %s'%quant,lw=3) 
plt.plot(df.date.unique()[:-1],repo_top[:-1],label='>Quantile %s'%quant,lw=3) 
plt.title('Repo/Fed Funds as % of Assets',fontsize=15)
plt.xlabel('Date',fontsize=15)
plt.ylabel('Repo/Fed Funds Portfolio (%)',fontsize=15)
plt.legend(fontsize=15) 

plt.figure(5)
plt.plot(df.date.unique()[30:-1],trade_other[30:-1],label='<Quantile %s'%quant,lw=3) 
plt.plot(df.date.unique()[30:-1],trade_top[30:-1],label='>Quantile %s'%quant,lw=3) 
plt.title('Trading Assets as % of Assets',fontsize=15)
plt.xlabel('Date',fontsize=15)
plt.ylabel('Trading Portfolio (%)',fontsize=15)
plt.legend(fontsize=15) 


# liabilities

dep_other = []
dep_top   = [] 

repo1_other_beg = []
repo1_other_med = []
repo1_other_post = []
repo1_other = []

repo1_top_beg    = [] 
repo1_top_med = []
repo1_top_post = []
repo1_top  =[]

trade1_other = []
trade1_top = []

eq_other = []
eq_top = []

borrow_other = []
borrow_top = []

sub_other = []
sub_top = []
liab_other_time = []
dep_other_total = []
for at,t in enumerate(df.date.unique()):
    
    total_liab_other = df[(df.date ==t) & (df.BHCK2170 < df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK3300'].sum()
    total_liab_top = df[(df.date ==t) & (df.BHCK2170 > df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK3300'].sum()
        
    # deposits
    dep_other.append( 100*(df[(df.date ==t) & (df.BHCK2170 < df[ df.date == t]['BHCK2170'].quantile(quant))]['BHDM6631'] +
                           df[(df.date ==t) & (df.BHCK2170 < df[ df.date == t]['BHCK2170'].quantile(quant))]['BHDM6636'] +
                           df[(df.date ==t) & (df.BHCK2170 < df[ df.date == t]['BHCK2170'].quantile(quant))]['BHFN6631'] +
                           df[(df.date ==t) & (df.BHCK2170 < df[ df.date == t]['BHCK2170'].quantile(quant))]['BHFN6636']).sum()/total_liab_other )
    
    dep_top.append( 100*(  df[(df.date ==t) & (df.BHCK2170 > df[ df.date == t]['BHCK2170'].quantile(quant))]['BHDM6631'] +
                           df[(df.date ==t) & (df.BHCK2170 > df[ df.date == t]['BHCK2170'].quantile(quant))]['BHDM6636'] +
                           df[(df.date ==t) & (df.BHCK2170 > df[ df.date == t]['BHCK2170'].quantile(quant))]['BHFN6631'] +
                           df[(df.date ==t) & (df.BHCK2170 > df[ df.date == t]['BHCK2170'].quantile(quant))]['BHFN6636']).sum()/total_liab_top )
    
    # fed funds and repo
    repo1_other_beg.append( 100*(df[(df.date ==t) & (df.BHCK2170 < df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK0278'] +
                                 df[(df.date ==t) & (df.BHCK2170 < df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK0279']).sum()/total_liab_other )
    
    repo1_top_beg.append( 100*(  df[(df.date ==t) & (df.BHCK2170 > df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK0278'] +
                                 df[(df.date ==t) & (df.BHCK2170 > df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK0279']).sum()/total_liab_top )


    repo1_other_med.append( 100*(df[(df.date ==t)  & (df.BHCK2170 < df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK2800']).sum()/total_liab_other )

    repo1_top_med.append(    100*(df[(df.date ==t)  & (df.BHCK2170 > df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK2800']).sum()/total_liab_top )



    repo1_other_post.append( 100*(df[(df.date ==t) & (df.BHCK2170 < df[ df.date == t]['BHCK2170'].quantile(quant))]['BHDMB993'] +
                                  df[(df.date ==t) & (df.BHCK2170 < df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCKB995']).sum()/total_liab_other )
    
    repo1_top_post.append(  100*( df[(df.date ==t) & (df.BHCK2170 > df[ df.date == t]['BHCK2170'].quantile(quant))]['BHDMB993'] +
                                  df[(df.date ==t) & (df.BHCK2170 > df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCKB995']).sum()/total_liab_top )

    # trading liabilities
    trade1_other.append( 100*(df[(df.date ==t) & (df.BHCK2170 < df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK3548']).sum()/total_liab_other )
    
    trade1_top.append(  100*(df[(df.date ==t) & (df.BHCK2170 > df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK3548']).sum()/total_liab_top )

    # borrowed money liabilities
    borrow_other.append( 100*(df[(df.date ==t) & (df.BHCK2170 < df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK2332']+
                              df[(df.date ==t) & (df.BHCK2170 < df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK2333']).sum()/total_liab_other )
    
    borrow_top.append( 100*(  df[(df.date ==t) & (df.BHCK2170 > df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK2332']+
                              df[(df.date ==t) & (df.BHCK2170 > df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK2333']).sum()/total_liab_top )
    
    
    
    # subordinated debt liabilities
    sub_other.append( 100*(df[(df.date ==t) & (df.BHCK2170 < df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK4062']).sum()/total_liab_other  ) 
    sub_top.append(  100*(df[(df.date ==t) & (df.BHCK2170 > df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK4062']).sum()/total_liab_top  ) 
    
    # equity
    eq_other.append( 100*(df[(df.date ==t) & (df.BHCK2170 < df[ df.date == t]['BHCK2170'].quantile(quant)) ]['BHCK3210']).sum()/total_liab_other )
    eq_top.append(  100*(df[(df.date ==t) & (df.BHCK2170 > df[ df.date == t]['BHCK2170'].quantile(quant)) ]['BHCK3210']).sum()/total_liab_top )   


 
plt.figure(6)
plt.plot(df.date.unique()[:-1],dep_other[:-1],label='<Quantile %s'%quant,lw=3) 
plt.plot(df.date.unique()[:-1],dep_top[:-1],label='>Quantile %s'%quant,lw=3) 
plt.title('Deposits as % of Liabilities',fontsize=15)
plt.xlabel('Date',fontsize=15)
plt.ylabel('Deposit Funding (%)',fontsize=15)
plt.legend(fontsize=15) 

repo1_other = np.concatenate(( repo1_other_med[:7], repo1_other_beg[7:42], repo1_other_med[42:62],repo1_other_post[62:]  ))
repo1_top = np.concatenate(( repo1_top_med[:7], repo1_top_beg[7:42], repo1_top_med[42:62],repo1_top_post[62:]  ))

plt.figure(7)
plt.plot(df.date.unique()[:-1],repo1_other[:-1],label='<Quantile %s'%quant,lw=3) 
plt.plot(df.date.unique()[:-1],repo1_top[:-1],label='>Quantile %s'%quant,lw=3) 
plt.title('Repo and Fed Funds as % of Liabilities',fontsize=15)
plt.xlabel('Date',fontsize=15)
plt.ylabel('Repo/Fed Funds Funding (%)',fontsize=15)
plt.legend(fontsize=15) 

plt.figure(8)
plt.plot(df.date.unique()[30:-1],trade1_other[30:-1],label='<Quantile %s'%quant,lw=3) 
plt.plot(df.date.unique()[30:-1],trade1_top[30:-1],label='>Quantile %s'%quant,lw=3) 
plt.title('Trading Liabilities as % of Liabilities',fontsize=15)
plt.xlabel('Date',fontsize=15)
plt.ylabel('Trading Liabilities Funding (%)',fontsize=15)
plt.legend(fontsize=15) 

plt.figure(9)
plt.plot(df.date.unique()[:-1],eq_other[:-1],label='<Quantile %s'%quant,lw=3) 
plt.plot(df.date.unique()[:-1],eq_top[:-1],label='>Quantile %s'%quant,lw=3) 
plt.title('Equity as % of Liabilities',fontsize=15)
plt.xlabel('Date',fontsize=15)
plt.ylabel('Equity Funding (%)',fontsize=15)
plt.legend(fontsize=15) 

plt.figure(10)
plt.plot(df.date.unique()[:-1],borrow_other[:-1],label='<Quantile %s'%quant,lw=3) 
plt.plot(df.date.unique()[:-1],borrow_top[:-1],label='>Quantile %s'%quant,lw=3) 
plt.title('Borrowed Money as % of Liabilities',fontsize=15)
plt.xlabel('Date',fontsize=15)
plt.ylabel('Borrowed Funding (%)',fontsize=15)
plt.legend(fontsize=15) 

plt.figure(11)
plt.plot(df.date.unique()[:-1],sub_other[:-1],label='<Quantile %s'%quant,lw=3) 
plt.plot(df.date.unique()[:-1],sub_top[:-1],label='>Quantile %s'%quant,lw=3) 
plt.title('Subordinated Debt as % of Liabilities',fontsize=15)
plt.xlabel('Date',fontsize=15)
plt.ylabel('Subordinated Debt Funding (%)',fontsize=15)
plt.legend(fontsize=15) 


#-------------------------------------------#
#                                           #
#   BALANCE SHEET BY TIME, BY PERCENTILE    #
#                                           #
#-------------------------------------------#

t3 = df.date.unique()[130]

p1 = .2
p2 = .4
p3 = .6
p4 = .8

balance_sheet = np.zeros(( 6,7))   # year, size group, asset/liability list

#
#   Time 3: 2019 Q1   
#

# 1st quantile group
# loans
balance_sheet[0,0] = np.nanmean( df[ (df.date == t3) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p1)) ]['BHCK2122']/
                                   df[ (df.date == t3) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p1)) ]['BHCK2170'])
# cash
balance_sheet[0,1] = np.nanmean( ( df[ (df.date == t3) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p1)) ]['BHCK0081'] +
                                     df[ (df.date == t3) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p1)) ]['BHCK0395'] +
                                     df[ (df.date == t3) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p1)) ]['BHCK0397'])/
                                     df[ (df.date == t3) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p1)) ]['BHCK2170'])
# securities
balance_sheet[0,2] = np.nanmean( ( df[ (df.date == t3) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p1)) ]['BHCK1754'] +
                                     df[ (df.date == t3) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p1)) ]['BHCK1773'])/
                                     df[ (df.date == t3) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p1)) ]['BHCK2170'])
# deposits
balance_sheet[0,3] = np.nanmean( ( df[ (df.date == t3) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p1)) ]['BHDM6631'] +
                                     df[ (df.date == t3) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p1)) ]['BHDM6636'] +
                                     df[ (df.date == t3) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p1)) ]['BHFN6631'] +
                                     df[ (df.date == t3) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p1)) ]['BHFN6636'])/
                                     df[ (df.date == t3) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p1)) ]['BHCK2170'])
# repo/fed funds
balance_sheet[0,4] = np.nanmean( ( df[ (df.date == t3) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p1)) ]['BHDMB993'] +
                                     df[ (df.date == t3) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p1)) ]['BHCKB995'])/
                                     df[ (df.date == t3) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p1)) ]['BHCK2170'])
# trading liabilities
balance_sheet[0,5] = np.nanmean( ( df[ (df.date == t3) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p1)) ]['BHCK3548'])/
                                     df[ (df.date == t3) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p1)) ]['BHCK2170'])
# equity
balance_sheet[0,6] = np.nanmean( ( df[ (df.date == t3) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p1)) ]['BHCK3210'])/
                                     df[ (df.date == t3) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p1)) ]['BHCK2170'])

# second quantile group
# loans
balance_sheet[1,0] = np.nanmean( df[ (df.date == t3) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p2)) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p1)) ]['BHCK2122']/
                                   df[ (df.date == t3) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p2)) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p1)) ]['BHCK2170'])
# cash
balance_sheet[1,1] = np.nanmean( ( df[ (df.date == t3) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p2)) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p1)) ]['BHCK0081'] +
                                     df[ (df.date == t3) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p2)) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p1)) ]['BHCK0395'] +
                                     df[ (df.date == t3) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p2)) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p1)) ]['BHCK0397'])/
                                     df[ (df.date == t3) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p2)) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p1)) ]['BHCK2170'])
# securities
balance_sheet[1,2] = np.nanmean( ( df[ (df.date == t3) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p2)) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p1)) ]['BHCK1754'] +
                                     df[ (df.date == t3) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p2)) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p1)) ]['BHCK1773'])/
                                     df[ (df.date == t3) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p2)) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p1)) ]['BHCK2170'])
# deposits
balance_sheet[1,3] = np.nanmean( ( df[ (df.date == t3) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p2)) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p1)) ]['BHDM6631'] +
                                     df[ (df.date == t3) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p2)) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p1)) ]['BHDM6636'] +
                                     df[ (df.date == t3) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p2)) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p1)) ]['BHFN6631'] +
                                     df[ (df.date == t3) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p2)) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p1)) ]['BHFN6636'])/
                                     df[ (df.date == t3) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p2)) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p1)) ]['BHCK2170'])
# repo/fed funds
balance_sheet[1,4] = np.nanmean( ( df[ (df.date == t3) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p2)) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p1)) ]['BHDMB993'] +
                                     df[ (df.date == t3) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p2)) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p1)) ]['BHCKB995'])/
                                     df[ (df.date == t3) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p2)) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p1)) ]['BHCK2170'])
# trading liabilities
balance_sheet[1,5] = np.nanmean( ( df[ (df.date == t3) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p2)) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p1)) ]['BHCK3548'])/
                                     df[ (df.date == t3) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p2)) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p1)) ]['BHCK2170'])
# equity
balance_sheet[1,6] = np.nanmean( ( df[ (df.date == t3) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p2)) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p1)) ]['BHCK3210'])/
                                     df[ (df.date == t3) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p2)) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p1)) ]['BHCK2170'])

# third quantile group
# loans
balance_sheet[2,0] = np.nanmean( df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p2)) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p3)) ]['BHCK2122']/
                                   df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p3)) ]['BHCK2170'])
# cash
balance_sheet[2,1] = np.nanmean( ( df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p2)) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p3))  ]['BHCK0081'] +
                                     df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p2)) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p3))  ]['BHCK0395'] +
                                     df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p2)) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p3))  ]['BHCK0397'])/
                                     df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p2)) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p3))  ]['BHCK2170'])
# securities
balance_sheet[2,2] = np.nanmean( ( df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p2)) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p3))  ]['BHCK1754'] +
                                     df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p2)) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p3))  ]['BHCK1773'])/
                                     df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p2)) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p3))  ]['BHCK2170'])
# deposits
balance_sheet[2,3] = np.nanmean( ( df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p2)) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p3))  ]['BHDM6631'] +
                                     df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p2)) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p3))  ]['BHDM6636'] +
                                     df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p2)) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p3))  ]['BHFN6631'] +
                                     df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p2)) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p3))  ]['BHFN6636'])/
                                     df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p2)) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p3))  ]['BHCK2170'])
# repo/fed funds
balance_sheet[2,4] = np.nanmean( ( df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p2)) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p3))  ]['BHDMB993'] +
                                     df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p2)) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p3))  ]['BHCKB995'])/
                                     df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p2)) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p3))  ]['BHCK2170'])
# trading liabilities
balance_sheet[2,5] = np.nanmean( ( df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p2)) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p3))  ]['BHCK3548'])/
                                     df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p2)) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p3))  ]['BHCK2170'])
# equity
balance_sheet[2,6] = np.nanmean( ( df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p2)) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p3))  ]['BHCK3210'])/
                                     df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p2)) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p3))  ]['BHCK2170'])

# fourth quantile group
# loans
balance_sheet[3,0] = np.nanmean( df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p3)) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p4)) ]['BHCK2122']/
                                   df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p3)) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p4)) ]['BHCK2170'])
# cash
balance_sheet[3,1] = np.nanmean( ( df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p3)) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p4))]['BHCK0081'] +
                                     df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p3)) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p4)) ]['BHCK0395'] +
                                     df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p3)) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p4)) ]['BHCK0397'])/
                                     df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p3)) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p4)) ]['BHCK2170'])
# securities
balance_sheet[3,2] = np.nanmean( ( df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p3)) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p4)) ]['BHCK1754'] +
                                     df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p3)) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p4))]['BHCK1773'])/
                                     df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p3)) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p4))]['BHCK2170'])
# deposits
balance_sheet[3,3] = np.nanmean( ( df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p3)) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p4))]['BHDM6631'] +
                                     df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p3)) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p4)) ]['BHDM6636'] +
                                     df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p3)) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p4))]['BHFN6631'] +
                                     df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p3)) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p4))]['BHFN6636'])/
                                     df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p3)) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p4)) ]['BHCK2170'])
# repo/fed funds
balance_sheet[3,4] = np.nanmean( ( df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p3)) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p4)) ]['BHDMB993'] +
                                     df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p3)) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p4)) ]['BHCKB995'])/
                                     df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p3)) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p4)) ]['BHCK2170'])
# trading liabilities
balance_sheet[3,5] = np.nanmean( ( df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p3)) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p4)) ]['BHCK3548'])/
                                     df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p3)) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p4)) ]['BHCK2170'])
# equity
balance_sheet[3,6] = np.nanmean( ( df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p3)) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p4)) ]['BHCK3210'])/
                                     df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p3)) & (df.BHCK2170 < df[ df.date == t3]['BHCK2170'].quantile(p4)) ]['BHCK2170'])

# fifth quantile group
# loans
balance_sheet[4,0] = np.nanmean( df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p4)) ]['BHCK2122']/
                                   df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p4)) ]['BHCK2170'])
# cash
balance_sheet[4,1] = np.nanmean( ( df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p4)) ]['BHCK0081'] +
                                     df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p4)) ]['BHCK0395'] +
                                     df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p4)) ]['BHCK0397'])/
                                     df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p4)) ]['BHCK2170'])
# securities
balance_sheet[4,2] = np.nanmean( ( df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p4)) ]['BHCK1754'] +
                                     df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p4)) ]['BHCK1773'])/
                                     df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p4)) ]['BHCK2170'])
# deposits
balance_sheet[4,3] = np.nanmean( ( df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p4)) ]['BHDM6631'] +
                                     df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p4)) ]['BHDM6636'] +
                                     df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p4)) ]['BHFN6631'] +
                                     df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p4)) ]['BHFN6636'])/
                                     df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p4)) ]['BHCK2170'])
# repo/fed funds
balance_sheet[4,4] = np.nanmean( ( df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p4)) ]['BHDMB993'] +
                                     df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p4)) ]['BHCKB995'])/
                                     df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p4)) ]['BHCK2170'])
# trading liabilities
balance_sheet[4,5] = np.nanmean( ( df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p4)) ]['BHCK3548'])/
                                     df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p4)) ]['BHCK2170'])
# equity
balance_sheet[4,6] = np.nanmean( ( df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p4)) ]['BHCK3210'])/
                                     df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(p4)) ]['BHCK2170'])

# sixth quantile group
# loans
balance_sheet[5,0] = np.nanmean( df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(.99)) ]['BHCK2122']/
                                   df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(.99)) ]['BHCK2170'])
# cash
balance_sheet[5,1] = np.nanmean( ( df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(.99)) ]['BHCK0081'] +
                                     df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(.99)) ]['BHCK0395'] +
                                     df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(.99)) ]['BHCK0397'])/
                                     df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(.99)) ]['BHCK2170'])
# securities
balance_sheet[5,2] = np.nanmean( ( df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(.99)) ]['BHCK1754'] +
                                     df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(.99)) ]['BHCK1773'])/
                                     df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(.99)) ]['BHCK2170'])
# deposits
balance_sheet[5,3] = np.nanmean( ( df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(.99)) ]['BHDM6631'] +
                                     df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(.99)) ]['BHDM6636'] +
                                     df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(.99)) ]['BHFN6631'] +
                                     df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(.99)) ]['BHFN6636'])/
                                     df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(.99)) ]['BHCK2170'])
# repo/fed funds
balance_sheet[5,4] = np.nanmean( ( df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(.99)) ]['BHDMB993'] +
                                     df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(.99)) ]['BHCKB995'])/
                                     df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(.99)) ]['BHCK2170'])
# trading liabilities
balance_sheet[5,5] = np.nanmean( ( df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(.99)) ]['BHCK3548'])/
                                     df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(.99)) ]['BHCK2170'])
# equity
balance_sheet[5,6] = np.nanmean( ( df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(.99)) ]['BHCK3210'])/
                                     df[ (df.date == t3) & (df.BHCK2170 > df[ df.date == t3]['BHCK2170'].quantile(.95)) ]['BHCK2170'])


print()
print('Time Period:',t3)
print('Quantile Group:',p1)
print()
print('|-------------------------------------------------|')
print('|       Assets       |        Liabilities         |')
print('|--------------------|----------------------------|')
print('| Loans:',     round(balance_sheet[0,0],2),'       |    Deposits:',       round(balance_sheet[0,3],2),'         |')
print('| Cash:',      round(balance_sheet[0,1],2),'        |    Repo/Fed Funds:',round(balance_sheet[0,4],2),'   |')
print('| Securities:',round(balance_sheet[0,2],2),'  |    Trading:',             round(balance_sheet[0,5],2),'           |')
print('| Other:',     round(1-sum(balance_sheet[0,:3]),2),'       |    Equity:', round(balance_sheet[0,6],2),'           |')
print('|                    |    Other:',                                          round(1-sum(balance_sheet[0,3:]),2),'            |')
print('|--------------------|----------------------------|')
print()

print()
print('Time Period:',t3)
print('Quantile Group:',p2)
print()
print('|-------------------------------------------------|')
print('|       Assets       |        Liabilities         |')
print('|--------------------|----------------------------|')
print('| Loans:',     round(balance_sheet[1,0],2),'       |    Deposits:',       round(balance_sheet[1,3],2),'         |')
print('| Cash:',      round(balance_sheet[1,1],2),'        |    Repo/Fed Funds:',round(balance_sheet[1,4],2),'   |')
print('| Securities:',round(balance_sheet[1,2],2),'  |    Trading:',             round(balance_sheet[1,5],2),'           |')
print('| Other:',     round(1-sum(balance_sheet[1,:3]),2),'       |    Equity:', round(balance_sheet[1,6],2),'           |')
print('|                    |    Other:',                                          round(1-sum(balance_sheet[1,3:]),2),'            |')
print('|--------------------|----------------------------|')
print()

print()
print('Time Period:',t3)
print('Quantile Group:',p3)
print()
print('|-------------------------------------------------|')
print('|       Assets       |        Liabilities         |')
print('|--------------------|----------------------------|')
print('| Loans:',     round(balance_sheet[2,0],2),'       |    Deposits:',       round(balance_sheet[2,3],2),'         |')
print('| Cash:',      round(balance_sheet[2,1],2),'        |    Repo/Fed Funds:',round(balance_sheet[2,4],2),'   |')
print('| Securities:',round(balance_sheet[2,2],2),'  |    Trading:',             round(balance_sheet[2,5],2),'           |')
print('| Other:',     round(1-sum(balance_sheet[2,:3]),2),'       |    Equity:', round(balance_sheet[2,6],2),'           |')
print('|                    |    Other:',                                          round(1-sum(balance_sheet[2,3:]),2),'            |')
print('|--------------------|----------------------------|')
print()

print()
print('Time Period:',t3)
print('Quantile Group:',p4)
print()
print('|-------------------------------------------------|')
print('|       Assets       |        Liabilities         |')
print('|--------------------|----------------------------|')
print('| Loans:',     round(balance_sheet[3,0],2),'       |    Deposits:',       round(balance_sheet[3,3],2),'         |')
print('| Cash:',      round(balance_sheet[3,1],2),'        |    Repo/Fed Funds:',round(balance_sheet[3,4],2),'   |')
print('| Securities:',round(balance_sheet[3,2],2),'  |    Trading:',             round(balance_sheet[3,5],2),'           |')
print('| Other:',     round(1-sum(balance_sheet[3,:3]),2),'       |    Equity:', round(balance_sheet[3,6],2),'           |')
print('|                    |    Other:',                                          round(1-sum(balance_sheet[3,3:]),2),'            |')
print('|--------------------|----------------------------|')
print()

print()
print('Time Period:',t3)
print('Quantile Group >:',p4)
print()
print('|-------------------------------------------------|')
print('|       Assets       |        Liabilities         |')
print('|--------------------|----------------------------|')
print('| Loans:',     round(balance_sheet[4,0],2),'       |    Deposits:',       round(balance_sheet[4,3],2),'         |')
print('| Cash:',      round(balance_sheet[4,1],2),'        |    Repo/Fed Funds:',round(balance_sheet[4,4],2),'   |')
print('| Securities:',round(balance_sheet[4,2],2),'  |    Trading:',             round(balance_sheet[4,5],2),'           |')
print('| Other:',     round(1-sum(balance_sheet[4,:3]),2),'       |    Equity:', round(balance_sheet[4,6],2),'           |')
print('|                    |    Other:',                                          round(1-sum(balance_sheet[4,3:]),2),'            |')
print('|--------------------|----------------------------|')
print()




print()
print('Time Period:',t3)
print('Quantile Group >.99')
print()
print('|-------------------------------------------------|')
print('|       Assets       |        Liabilities         |')
print('|--------------------|----------------------------|')
print('| Loans:',     round(balance_sheet[5,0],2),'       |    Deposits:',       round(balance_sheet[5,3],2),'         |')
print('| Cash:',      round(balance_sheet[5,1],2),'        |    Repo/Fed Funds:',round(balance_sheet[5,4],2),'   |')
print('| Securities:',round(balance_sheet[5,2],2),'  |    Trading:',             round(balance_sheet[5,5],2),'           |')
print('| Other:',     round(1-sum(balance_sheet[5,:3]),2),'       |    Equity:', round(balance_sheet[5,6],2),'           |')
print('|                    |    Other:',                                          round(1-sum(balance_sheet[5,3:]),2),'            |')
print('|--------------------|----------------------------|')
print()

"""
    OTHER ASSET CATEGORIES AND OTHER LIABILITY CATEGORIES WAY TOO BIG (PARTICULARLY FOR BIG BANKS)
    
    FOR ASSETS, INCLUDE - FED FUNDS/REPO (BHDMB987 + BHCKB989)  (BHCK0276 + 0277 on older forms)
                        - Trading Assets (BHCK 3545)    ()
                        
    FOR LIABILITIES, INCLUDE - OTHER BORROWED MONEY (BHCK 3190) (BHCK 2332 + 2333 on older forms)
                             - SUBORDINATED NOTES (BHCK 4062 + BHCK C699)   (just 4062 no older forms)
                             
"""

#----------------------------------------#
#                                        #
#   BALANCE SHEET ITEM DECOMPOSITIONS    #
#                                        #
#----------------------------------------#

# loans (mbs,consumer,C&I,...)

# securities (US treasury, GNMA & FreddieMac, agency, other,...)

#-------------------#
#                   #
#   INCOME ITEMS    #
#                   #
#-------------------#
roe_top_weight = []
roe_other_weight = []
roe_int_top_weight = []
roe_int_other_weight = []
roe_nonint_top_weight = []
roe_nonint_other_weight = []
int_ratio_top_weight = []
int_ratio_other_weight = []

roe_top = []
roe_other = []
roe_int_top = []
roe_int_other = []
roe_nonint_top = []
roe_nonint_other = []


quart = 2
multiplier = [4,2,4/3,1]

for at, t in enumerate( df.date.unique() ):
      
    temp = (df[ (df.date == t) & (df.BHCK2170 > df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK4107']+
                                        df[ (df.date == t) & (df.BHCK2170 > df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK4079']-
                                        df[ (df.date == t) & (df.BHCK2170 > df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK4073']-
                                        df[ (df.date == t) & (df.BHCK2170 > df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK4093'])/df[ (df.date == t) & (df.BHCK2170 > df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK3210']
    temp[ temp > np.quantile(temp,.975) ] = np.quantile(temp,.975)
    temp[ temp < np.quantile(temp,.025) ] = np.quantile(temp,.025)
    
    roe_top.append(  multiplier[quart]*np.nanmean(temp) )

    temp = (df[ (df.date == t) & (df.BHCK2170 < df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK4107']+
                                          df[ (df.date == t) & (df.BHCK2170 < df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK4079']-
                                          df[ (df.date == t) & (df.BHCK2170 < df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK4073']-
                                          df[ (df.date == t) & (df.BHCK2170 < df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK4093'])/df[ (df.date == t) & (df.BHCK2170 < df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK3210']
    temp[ temp > np.quantile(temp,.975) ] = np.quantile(temp,.975)
    temp[ temp < np.quantile(temp,.025) ] = np.quantile(temp,.025)
    
    roe_other.append(  multiplier[quart]*np.nanmean(temp ))
    
    temp = (df[ (df.date == t) & (df.BHCK2170 > df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK4107']-
                                           df[ (df.date == t) & (df.BHCK2170 > df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK4073'])/df[ (df.date == t) & (df.BHCK2170 > df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK3210']
    temp[ temp > np.quantile(temp,.975) ] = np.quantile(temp,.975)
    temp[ temp < np.quantile(temp,.025) ] = np.quantile(temp,.025)
    
    roe_int_top.append( multiplier[quart]*np.nanmean(temp ))

    temp = (df[ (df.date == t) & (df.BHCK2170 < df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK4107']-
                                           df[ (df.date == t) & (df.BHCK2170 < df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK4073'])/df[ (df.date == t) & (df.BHCK2170 < df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK3210'] 
    temp[ temp > np.quantile(temp,.975) ] = np.quantile(temp,.975)
    temp[ temp < np.quantile(temp,.025) ] = np.quantile(temp,.025)    
    roe_int_other.append( multiplier[quart]*np.nanmean(temp))
    
    
    temp = (df[ (df.date == t) & (df.BHCK2170 > df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK4079']-
                                              df[ (df.date == t) & (df.BHCK2170 > df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK4093'])/df[ (df.date == t) & (df.BHCK2170 > df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK3210']
    temp[ temp > np.quantile(temp,.975) ] = np.quantile(temp,.975)
    temp[ temp < np.quantile(temp,.025) ] = np.quantile(temp,.025)    
    
    roe_nonint_top.append( multiplier[quart]*np.nanmean(temp ))
    
    temp = (df[ (df.date == t) & (df.BHCK2170 < df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK4079']-
                                                df[ (df.date == t) & (df.BHCK2170 < df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK4093'])/df[ (df.date == t) & (df.BHCK2170 < df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK3210'] 
    temp[ temp > np.quantile(temp,.975) ] = np.quantile(temp,.975)
    temp[ temp < np.quantile(temp,.025) ] = np.quantile(temp,.025)      
    roe_nonint_other.append( multiplier[quart]*np.nanmean(temp))
    

    # WEIGHTED MEASURES (weighted by equity holdings)
      
    # total assets
    total_equity_other = df[ (df.date == t) & (df.BHCK2170 < df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK3210'].sum()
    total_equity_top = df[ (df.date == t) & (df.BHCK2170 > df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK3210'].sum()

    roe_top_weight.append(  multiplier[quart]*(df[ (df.date == t) & (df.BHCK2170 > df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK4107']+
                                        df[ (df.date == t) & (df.BHCK2170 > df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK4079']-
                                        df[ (df.date == t) & (df.BHCK2170 > df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK4073']-
                                        df[ (df.date == t) & (df.BHCK2170 > df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK4093']).sum()/total_equity_top )

    roe_other_weight.append(  multiplier[quart]*(df[ (df.date == t) & (df.BHCK2170 < df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK4107']+
                                          df[ (df.date == t) & (df.BHCK2170 < df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK4079']-
                                          df[ (df.date == t) & (df.BHCK2170 < df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK4073']-
                                          df[ (df.date == t) & (df.BHCK2170 < df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK4093']).sum()/total_equity_other )
    
    roe_int_top_weight.append( multiplier[quart]*(df[ (df.date == t) & (df.BHCK2170 > df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK4107']-
                                           df[ (df.date == t) & (df.BHCK2170 > df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK4073']).sum()/total_equity_top )

    roe_int_other_weight.append( multiplier[quart]*(df[ (df.date == t) & (df.BHCK2170 < df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK4107']-
                                           df[ (df.date == t) & (df.BHCK2170 < df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK4073']).sum()/total_equity_other )
    
    roe_nonint_top_weight.append( multiplier[quart]*(df[ (df.date == t) & (df.BHCK2170 > df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK4079']-
                                              df[ (df.date == t) & (df.BHCK2170 > df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK4093']).sum()/total_equity_top )

    roe_nonint_other_weight.append( multiplier[quart]*(df[ (df.date == t) & (df.BHCK2170 < df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK4079']-
                                                df[ (df.date == t) & (df.BHCK2170 < df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK4093']).sum()/total_equity_other )
    
    total_inc_top = df[ (df.date == t) & (df.BHCK2170 > df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK4079'] .sum()
    total_inc_other = df[ (df.date == t) & (df.BHCK2170 < df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK4079'].sum() 
    
    int_ratio_top_weight.append( df[ (df.date == t) & (df.BHCK2170 > df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK4107'].sum()/total_inc_top )
    int_ratio_other_weight.append( df[ (df.date == t) & (df.BHCK2170 < df[ df.date == t]['BHCK2170'].quantile(quant))]['BHCK4107'].sum()/total_inc_other )    
    
    #if not last quarter of fiscal year
    if quart < 3:     
        quart = quart + 1        
    else:                         
        quart = 0

plt.figure(14)
plt.plot(df.date.unique()[:-1],100*np.asarray((roe_top_weight))[:-1]       ,label='>Quantile %s'%quant,lw=3,c='red',alpha=.5)
plt.plot(df.date.unique()[:-1],100*np.asarray((roe_other_weight))[:-1]       ,label='<Quantile %s'%quant,lw=3,c='blue',alpha=.5,ls='--')
plt.title('Bank Return on Equity',fontsize=15)
plt.legend(fontsize=15)
plt.xlabel('Date',fontsize=15)
plt.ylabel('Return on Equity (%, Annualized)',fontsize=15)


plt.figure(15)
plt.plot(df.date.unique()[:-1],100*np.asarray((roe_int_top_weight))[:-1]   ,label='>Quantile %s'%quant,lw=3)
plt.plot(df.date.unique()[:-1],100*np.asarray((roe_int_other_weight))[:-1]   ,label='<Quantile %s'%quant,lw=3)
plt.title('Net Interest Income over Equity',fontsize=15)
plt.legend(fontsize=15)
plt.xlabel('Date',fontsize=15)
plt.ylabel('Net Interest Income over Equity (%, Annualized)',fontsize=15)


plt.figure(16) 
plt.plot(df.date.unique()[:-1],100*np.asarray((roe_nonint_top_weight))[:-1],label='>Quantile %s'%quant,lw=3)
plt.plot(df.date.unique()[:-1],100*np.asarray((roe_nonint_other_weight))[:-1],label='<Quantile %s'%quant,lw=3)
plt.title('Net Non-Interest Income over Equity',fontsize=15)
plt.legend(fontsize=15)
plt.xlabel('Date',fontsize=15)
plt.ylabel('Net Non-Int Income over Equity (%, Annualized)',fontsize=15)

plt.figure(17)
plt.plot(df.date.unique()[:-1],100*np.asarray((roe_int_top_weight))[:-1]       ,label='ROE Int, >Quantile %s'%quant,lw=3,c='red',alpha=.5)
plt.plot(df.date.unique()[:-1],100*np.asarray((roe_nonint_top_weight))[:-1],label='ROE Non-Int, >Quantile %s'%quant,lw=3,c='red',alpha=.5)
plt.plot(df.date.unique()[:-1],100*np.asarray((roe_int_other_weight))[:-1]       ,label='ROE Int, <Quantile %s'%quant,lw=3,c='blue',alpha=.5,ls='--')
plt.plot(df.date.unique()[:-1],100*np.asarray((roe_nonint_other_weight))[:-1],label='ROE Non-Int, <Quantile %s'%quant,lw=3,c='blue',alpha=.5,ls='--')
plt.title('Decomposing ROE by Net Int and Net Non-Int',fontsize=15)
plt.xlabel('Date',fontsize=15)
plt.ylabel('(%, Annualized)',fontsize=15)
plt.legend()


plt.figure(18)
plt.plot(df.date.unique()[:-1],int_ratio_top_weight[:-1],label='>Quantile %s'%quant,lw=3)
plt.plot(df.date.unique()[:-1],int_ratio_other_weight[:-1],label='<Quantile %s'%quant,lw=3)
plt.title('Ratio of Interest Income to Non-Interest Income',fontsize=15)
plt.xlabel('Date',fontsize=15)
plt.ylabel('Ratio',fontsize=15)
plt.legend(fontsize=15)



roe_500 = []
roe_50_500 = []
roe_50 = []
roe_all = []

quart = 2
multiplier = [4,2,4/3,1]

for at, t in enumerate( df.date.unique() ):
          
    # total assets
    total_equity_500 = df[ (df.date == t) & (df.BHCK2170 >= 500000000)]['BHCK3210'].sum()
    total_equity_50_500 = df[ (df.date == t) & (df.BHCK2170 < 500000000) & (df.BHCK2170 > 50000000)]['BHCK3210'].sum()
    total_equity_50 = df[ (df.date == t)  & (df.BHCK2170 < 50000000)]['BHCK3210'].sum()
    total_equity_all = df[ (df.date == t) ]['BHCK3210'].sum()

    roe_500.append(  multiplier[quart]*(df[ (df.date == t) & (df.BHCK2170 >= 500000000)]['BHCK4340']).sum()/total_equity_500 )

    roe_50_500.append(  multiplier[quart]*(df[ (df.date == t) & (df.BHCK2170 < 500000000) & (df.BHCK2170 >= 50000000)]['BHCK4340']).sum()/total_equity_50_500 )

    roe_50.append(  multiplier[quart]*(df[ (df.date == t) & (df.BHCK2170 < 50000000)]['BHCK4340']).sum()/total_equity_50 )

    roe_all.append(  multiplier[quart]*(df[ (df.date == t) ]['BHCK4340']).sum()/total_equity_all )
    
    # count number of firms
    count_500.append( np.shape(df[(df.date == t) & (df.BHCK2170 >= 500000000)])[0] )
    count_50_500.append( np.shape(df[(df.date == t) & (df.BHCK2170 < 500000000) & (df.BHCK2170 > 50000000)])[0] )
        
    #if not last quarter of fiscal year
    if quart < 3:     
        quart = quart + 1        
    else:                         
        quart = 0

plt.figure(4)
plt.plot(df.date.unique()[:-1],100*np.asarray((roe_500))[:-1]       ,label='>500b',lw=3,c='red',alpha=.5)
plt.plot(df.date.unique()[:-1],100*np.asarray((roe_50_500))[:-1]       ,label='[50b,500b)',lw=3,c='blue',alpha=.5,ls='--')
plt.plot(df.date.unique()[:-1],100*np.asarray((roe_50))[:-1]       ,label='<50b',lw=3,c='green',alpha=.5,ls='--')
plt.plot(df.date.unique()[:-1],100*np.asarray((roe_all))[:-1]       ,label='all',lw=3,c='black',alpha=.5,ls='--')
plt.title('Bank Return on Equity',fontsize=15)
plt.legend(fontsize=15)
plt.xlabel('Date',fontsize=15)
plt.ylabel('Return on Equity (%, Annualized)',fontsize=15)


#----------------------------------#
#                                  #
#   INCOME ITEMS DECOMPOSITIONS    #
#                                  # 
#----------------------------------#

# interest income (...)
    # loans and leases : 4435 + 4436 + F821 + 4059 + 4065  or ( just 4010 + 4059 + 4065 pre-2008)
    # balanes from dep inst: 4115
    # US treasury securities and agency : B488
    # MBS : B489
    # other securities : 4060
    # trading assets : 4069 
    # fed funds and repo : 4020
    # other : 4518
    # total: 4107
    
loan_int1 = []
loan_int2 = []
dep_int  = []
us_int   = []
mbs_int  = []
other_sec_int = []
trade_int = []
repo_int = []
other_int = []

for at, t in enumerate( df.date.unique() ):
        
    total_int_income = df[ df.date == t]['BHCK4107'].sum()
    
    loan_int1.append( (df[ df.date ==t]['BHCK4010']+df[ df.date == t]['BHCK4059']+df[ df.date == t]['BHCK4065']).sum()/total_int_income  )
    
    loan_int2.append( (df[ df.date == t]['BHCK4435']+df[ df.date == t]['BHCK4436']+df[ df.date == t]['BHCKF821']+df[ df.date == t]['BHCK4059']+df[ df.date == t]['BHCK4065']).sum()/total_int_income )
    
    dep_int.append( df[ df.date == t]['BHCK4115'].sum()/total_int_income )
    
    us_int.append( df[ df.date == t]['BHCKB488'].sum()/total_int_income )
    
    mbs_int.append( df[ df.date == t]['BHCKB489'].sum()/total_int_income )
    
    other_sec_int.append( df[ df.date == t]['BHCK4060'].sum()/total_int_income )

    trade_int.append( df[ df.date == t]['BHCK4069'].sum()/total_int_income )
    
    repo_int.append( df[ df.date == t]['BHCK4020'].sum()/total_int_income )
    
    other_int.append( df[ df.date == t]['BHCK4518'].sum()/total_int_income )    

loan_int = np.concatenate(( loan_int1[:86], loan_int2[86:] ))

plt.figure(19)
plt.plot(df.date.unique()[58:-1],loan_int[58:-1],label='loan/lease',lw=3)
plt.plot(df.date.unique()[58:-1],dep_int[58:-1],label='depository',lw=3)
plt.plot(df.date.unique()[58:-1],us_int[58:-1],label='US/Agency',lw=3)
plt.plot(df.date.unique()[58:-1],mbs_int[58:-1],label='MBS',lw=3)
plt.plot(df.date.unique()[58:-1],other_sec_int[58:-1],label='Other Securities',lw=3)
plt.plot(df.date.unique()[58:-1],trade_int[58:-1],label='Trading',lw=3)
plt.plot(df.date.unique()[58:-1],repo_int[58:-1],label='Repo/Fed Funds',lw=3)
plt.plot(df.date.unique()[58:-1],other_int[58:-1],label='Other',lw=3)
plt.title('Interest Income Item Decomposition',fontsize=15)
plt.xlabel('Date',fontsize=15)
plt.ylabel('Ratio',fontsize=15)
plt.legend(fontsize=15)

plt.figure(20)
plt.plot(df.date.unique()[58:-1],dep_int[58:-1],label='depository',lw=3)
plt.plot(df.date.unique()[58:-1],us_int[58:-1],label='US/Agency',lw=3)
plt.plot(df.date.unique()[58:-1],mbs_int[58:-1],label='MBS',lw=3)
plt.plot(df.date.unique()[58:-1],other_sec_int[58:-1],label='Other Securities',lw=3)
plt.plot(df.date.unique()[58:-1],trade_int[58:-1],label='Trading',lw=3)
plt.plot(df.date.unique()[58:-1],repo_int[58:-1],label='Repo/Fed Funds',lw=3)
plt.plot(df.date.unique()[58:-1],other_int[58:-1],label='Other',lw=3)
plt.title('Interest Income Item Decomposition \n Excluding Loans',fontsize=15)
plt.xlabel('Date',fontsize=15)
plt.ylabel('Ratio',fontsize=15)
plt.legend(fontsize=15)

# now averages according to the percentiles 


# interest expense (...)
    # deposit interest (HK03 + HK04 + 6761 + 4172)  ( or just A517 + A518 + 6761 + 4172 pre-2017)
    # fed funds/repo (4180)
    # trading liabilities and borrowed money (4185)
    # subrodinated debt (4397)
    # other (4398)
    # total (4073)
    
dep_exp1 = []
dep_exp2 = []
repo_exp = []
trade_exp = []
sub_exp = []
other_exp = []


for at, t in enumerate( df.date.unique() ):
        
    total_int_expense = df[ df.date == t]['BHCK4073'].sum()

    dep_exp1.append( (df[ df.date == t]['BHCKA517']+df[ df.date == t]['BHCKA518']+df[ df.date == t]['BHCK6761']+df[ df.date == t]['BHCK4172']).sum()/total_int_expense )    
    dep_exp2.append( (df[ df.date == t]['BHCKHK03']+df[ df.date == t]['BHCKHK04']+df[ df.date == t]['BHCK6761']+df[ df.date == t]['BHCK4172']).sum()/total_int_expense )

    repo_exp.append( (df[ df.date ==t]['BHCK4180'].sum()/total_int_expense ) )

    trade_exp.append( (df[ df.date ==t]['BHCK4185'].sum()/total_int_expense ) )

    sub_exp.append( (df[ df.date ==t]['BHCK4397'].sum()/total_int_expense ) )

    other_exp.append( (df[ df.date ==t]['BHCK4398'].sum()/total_int_expense ) )

dep_exp = np.concatenate(( dep_exp1[:122], dep_exp2[122:] ))

plt.figure(21)
plt.plot(df.date.unique()[58:-1],dep_exp[58:-1],label='Depository',lw=3)
plt.plot(df.date.unique()[58:-1],repo_exp[58:-1],label='Repo/Fed Funds',lw=3)
plt.plot(df.date.unique()[58:-1],trade_exp[58:-1],label='Trading',lw=3)
plt.plot(df.date.unique()[58:-1],sub_exp[58:-1],label='Subordinated Debt',lw=3)
plt.plot(df.date.unique()[58:-1],other_exp[58:-1],label='Other',lw=3)
plt.title('Interest Expense Item Decomposition',fontsize=15)
plt.xlabel('Date',fontsize=15)
plt.ylabel('Ratio',fontsize=15)
plt.legend(fontsize=15)

# non-interest income (...)
    # fiduciary activities: 4070
    #trading revenue: A220
    # deposit accounts : 4483
    # venture cap: B491
    # net servicing: B492 
    # net securitization income : B493
    # other: B4987
        
    # invest banking and brokereage: C886 + C888 + KX46 + C887 + C386 + C387 + KX47  (need B490 for pre-2007 )
    # total : 4079
    
ibank1_non = []
ibank2_non = []
trade_non = []
dep_non = []

ibank1_non_top5 = []
ibank2_non_top5 = []
trade_non_top5 = []
dep_non_top5 = []

ibank1_non_other = []
ibank2_non_other = []
trade_non_other = []
dep_non_other = []

for at,t in enumerate(df.date.unique()):
    
    total_nonint = df[ df.date == t]['BHCK4079'].sum()

    # investment banking
    ibank1_non.append( (df[ df.date == t]['BHCKB490']+df[ df.date == t]['BHCKB491']+df[ df.date == t]['BHCK4070']).sum()/total_nonint )

    ibank2_non.append( (df[ df.date == t]['BHCKC886'] + df[ df.date == t]['BHCKC887'] + df[ df.date == t]['BHCKC888']+df[ df.date == t]['BHCKB491'] +df[ df.date == t]['BHCK4070']).sum()/total_nonint )
    # trading activity
    trade_non.append( (df[ df.date == t]['BHCKA220']+df[ df.date == t]['BHCKB493']).sum()/total_nonint )      
    # deposit and payment services
    dep_non.append( (df[ df.date == t]['BHCK4483']+df[ df.date == t]['BHCKB492']).sum()/total_nonint )  
    
    
    # investment banking
    total_top5 = df[ (df.date == t) & (df.BHCK2170 > df[ df.date == t]['BHCK2170'].quantile(.95))]['BHCK4079'].sum()
    
    ibank1_non_top5.append( 
                       ( df[ (df.date == t) & (df.BHCK2170 > df[ df.date == t]['BHCK2170'].quantile(.90))]['BHCKB490']+
                         df[ (df.date == t) & (df.BHCK2170 > df[ df.date == t]['BHCK2170'].quantile(.90))]['BHCKB491']+
                         df[ (df.date == t) & (df.BHCK2170 > df[ df.date == t]['BHCK2170'].quantile(.90))]['BHCK4070']).sum()/total_top5 )
    
    ibank2_non_top5.append( 
                      ( df[ (df.date == t) & (df.BHCK2170 > df[ df.date == t]['BHCK2170'].quantile(.90))]['BHCKC886'] +
                        df[ (df.date == t) & (df.BHCK2170 > df[ df.date == t]['BHCK2170'].quantile(.90))]['BHCKC887'] +
                        df[ (df.date == t) & (df.BHCK2170 > df[ df.date == t]['BHCK2170'].quantile(.90))]['BHCKC888'] +
                        df[ (df.date == t) & (df.BHCK2170 > df[ df.date == t]['BHCK2170'].quantile(.90))]['BHCKB491'] + 
                        df[ (df.date == t) & (df.BHCK2170 > df[ df.date == t]['BHCK2170'].quantile(.90))]['BHCK4070']).sum()/total_top5)
    # trading activity
    trade_non_top5.append( 
                     ( df[ (df.date == t) & (df.BHCK2170 > df[ df.date == t]['BHCK2170'].quantile(.90))]['BHCKA220']+
                       df[ (df.date == t) & (df.BHCK2170 > df[ df.date == t]['BHCK2170'].quantile(.90))]['BHCKB493']).sum()/total_top5 )  
    # deposit and payment services
    dep_non_top5.append( 
                    ( df[ (df.date == t) & (df.BHCK2170 > df[ df.date == t]['BHCK2170'].quantile(.90))]['BHCK4483']+
                      df[ (df.date == t) & (df.BHCK2170 > df[ df.date == t]['BHCK2170'].quantile(.90))]['BHCKB492']).sum()/total_top5   )    

    total_other = df[ (df.date == t) & (df.BHCK2170 < df[ df.date == t]['BHCK2170'].quantile(.90))]['BHCK4079'].sum()

    # investment banking
    ibank1_non_other.append( 
                       ( df[ (df.date == t) & (df.BHCK2170 < df[ df.date == t]['BHCK2170'].quantile(.90))]['BHCKB490']+
                         df[ (df.date == t) & (df.BHCK2170 < df[ df.date == t]['BHCK2170'].quantile(.90))]['BHCKB491']+
                         df[ (df.date == t) & (df.BHCK2170 < df[ df.date == t]['BHCK2170'].quantile(.90))]['BHCK4070']).sum()/total_other ) 
    
    ibank2_non_other.append( 
                      ( df[ (df.date == t) & (df.BHCK2170 < df[ df.date == t]['BHCK2170'].quantile(.90))]['BHCKC886'] +
                        df[ (df.date == t) & (df.BHCK2170 < df[ df.date == t]['BHCK2170'].quantile(.90))]['BHCKC887'] +
                        df[ (df.date == t) & (df.BHCK2170 < df[ df.date == t]['BHCK2170'].quantile(.90))]['BHCKC888'] +
                        df[ (df.date == t) & (df.BHCK2170 < df[ df.date == t]['BHCK2170'].quantile(.90))]['BHCKB491'] + 
                        df[ (df.date == t) & (df.BHCK2170 < df[ df.date == t]['BHCK2170'].quantile(.90))]['BHCK4070']).sum()/total_other ) 
    # trading activity
    trade_non_other.append(
                     ( df[ (df.date == t) & (df.BHCK2170 < df[ df.date == t]['BHCK2170'].quantile(.90))]['BHCKA220']+
                       df[ (df.date == t) & (df.BHCK2170 < df[ df.date == t]['BHCK2170'].quantile(.90))]['BHCKB493']).sum()/total_other )   
    # deposit and payment services
    dep_non_other.append(
                    ( df[ (df.date == t) & (df.BHCK2170 < df[ df.date == t]['BHCK2170'].quantile(.90))]['BHCK4483']+
                      df[ (df.date == t) & (df.BHCK2170 < df[ df.date == t]['BHCK2170'].quantile(.90))]['BHCKB492']).sum()/total_other)        

ibank_non = np.concatenate(( ibank1_non[:82], ibank2_non[82:]))
ibank_non_top5 = np.concatenate(( ibank1_non_top5[:82], ibank2_non_top5[82:]))
ibank_non_other = np.concatenate(( ibank1_non_other[:82], ibank2_non_other[82:]))

plt.figure(22)
plt.plot(df.date.unique()[58:-1],100*np.asarray((ibank_non[58:-1])),label='Investment Banking',lw=3)
plt.plot(df.date.unique()[58:-1],100*np.asarray((trade_non[58:-1])),label='Trading',lw=3)
plt.plot(df.date.unique()[58:-1],100*np.asarray((dep_non[58:-1])),label='Deposits',lw=3)
plt.title('Non-Interest Income Decomposition',fontsize=20)
plt.xlabel('Date',fontsize=20)
plt.ylabel('% of Total Non-Interest Income',fontsize=20)
plt.legend(fontsize=20)

plt.figure(28)
plt.plot(df.date.unique()[58:-1],100*np.asarray((ibank_non_other[58:-1])),label='Bottom 90',lw=3)
plt.plot(df.date.unique()[58:-1],100*np.asarray((ibank_non_top5[58:-1])),label='Top 10',lw=3)
plt.legend()

plt.figure(29)
plt.plot(df.date.unique()[58:-1],100*np.asarray((trade_non_other[58:-1])),label='Bottom 90',lw=3)
plt.plot(df.date.unique()[58:-1],100*np.asarray((trade_non_top5[58:-1])),label='Top 10',lw=3)
plt.legend()

plt.figure(30)
plt.plot(df.date.unique()[58:-1],100*np.asarray((dep_non_other[58:-1])),label='Bottom 90',lw=3)
plt.plot(df.date.unique()[58:-1],100*np.asarray((dep_non_top5[58:-1])),label='Top 10',lw=3)
plt.legend()

# non-interest expense (...)
    # salaries and benefits: 4135
    # premises and fixed assets : 4217
    # impairment loss : C216 + C232
    # other: 4092
    # total: 4093

#------------------------------#
#                              # 
#   STATISTISTICAL ANALYSIS    #
#                              # 
#------------------------------#


# relationship of size, roe, cap ratios, interest, non-interest, securities

# scatterplot graphics

# do correlation table for main variables (for a sample over the last few years, then for pre-crisis)

# other tests?

