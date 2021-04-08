
"""
    Objective is to look at aggregate and bank-level measures of
        volatility and correlation across lines of business (cbank and ibank)
        
    want to replicate some results from Stiroh as sanity check.  These are just on
        net interest income and non-interest income.  
        
    Then look at same measures when netting out non-interest expense across line of business
"""


"""
Packages
"""
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

plt.style.use('ggplot')
#print(plt.style.available)

os.chdir('/home/pando004/Desktop/BankData/FRY9')
df = pd.read_csv('frdata.csv')

# make date variable
df['date'] = pd.to_datetime( df.RSSD9999, format='%Y%m%d')

df = df.sort_values(by=['date'])


"""
    annualize relevant variables
"""
quart = 2
multiplier = [4,2,4/3,1]

df['cbank_rev'] = 0
df['ibank_rev'] = 0

df['labor'] = 0
df['fixed_assets'] = 0
df['other_exp'] = 0

df['inc_tax'] = 0
df['net_inc'] = 0
df['pre_tax_majority_net_inc'] = 0

# commercial bank items
df['int_inc'] = 0    # BHCK4107 - BHCK4069
df['int_exp'] = 0    # BHCK 4073 - BHCK 4185
df['service_dep'] = 0    # BHCK 4483
df['provisions'] = 0  # BHCK 4230
df['gains'] = 0   # BHCK 3521 + BHCK 3196
df['net_service'] = 0  # BHCKB492
df['other_cbank'] = 0   # BHCKC013 + BHCK C015  + BHCK C016

df['interest_base'] = 0
df['non_interest_base'] = 0

# investment bank items
df['nonint_inc'] = 0  # BHCK 4079 - BHCK 4483
df['trading'] = 0   # BHCK 4069 - BHCK 4185

df['fid'] = 0
df['trade_rev'] = 0
df['venture'] = 0
df['securitize'] = 0
df['securities_broke'] = 0
df['ibank_fees'] = 0
df['annuity'] = 0
df['insurance'] = 0
df['advisory'] = 0

head = []

for at, t in enumerate( df.date.unique() ):

    df.loc[ df.date==t, 'fid' ] =    multiplier[quart]*( df[df.date==t]['BHCK4070'] )
    df.loc[ df.date==t, 'trade_rev' ] =    multiplier[quart]*( df[df.date==t]['BHCKA220'] )
    df.loc[ df.date==t, 'venture' ] =    multiplier[quart]*( df[df.date==t]['BHCKB491'] )
    df.loc[ df.date==t, 'securitize' ] =    multiplier[quart]*(  df[df.date==t]['BHCKB493'] )
    df.loc[ df.date==t, 'securities_broke' ] =    multiplier[quart]*( df[df.date==t]['BHCKC886'] )
    df.loc[ df.date==t, 'ibank_fees' ] =    multiplier[quart]*( df[df.date==t]['BHCKC888'] )
    df.loc[ df.date==t, 'annuity' ] =    multiplier[quart]*( df[df.date==t]['BHCKC887'] )
    df.loc[ df.date==t, 'insurance' ] =    multiplier[quart]*( df[df.date==t]['BHCKC386'] + df[df.date==t]['BHCKC387'] + df[df.date==t]['BHCKKX47'] )
    df.loc[ df.date==t, 'advisory' ] =    multiplier[quart]*( df[df.date==t]['BHCKKX46'] )

	# revenues from commercial bank
    df.loc[ df.date==t, 'cbank_rev' ] =    multiplier[quart]*(df[df.date==t]['BHCK4107'] - df[df.date==t]['BHCK4069'] + df[df.date==t]['BHCK4483'] -  # + df[df.date==t]['BHCKF555'] - df[df.date==t]['BHCKF558'] + df[df.date==t]['BHCKT047'] - df[df.date==t]['BHCK4146']
                                                             df[df.date==t]['BHCK4230'] + df[df.date==t]['BHCK3521'] + df[df.date==t]['BHCK3196'] + 
                                                             df[df.date==t]['BHCKB492'] + df[df.date==t]['BHCKC013'] + df[df.date==t]['BHCKC015'] +
                                                             df[df.date==t]['BHCKC016']   + 
                                                               - df[df.date==t]['BHCK4073'] + 
                                                             df[df.date==t]['BHCK4185']
                                                             )  
     
	# revenues from investment bank 
    df.loc[ df.date==t, 'ibank_rev' ] =   multiplier[quart]*(df[df.date==t]['BHCK4079']  - df[df.date==t]['BHCK4483'] + df[df.date==t]['BHCK4069']  -  # -df[df.date==t]['BHCKF555']- df[df.date==t]['BHCKT047'] - df[df.date==t]['BHCK4146']
                                                    df[df.date==t]['BHCK4185']  - df[df.date==t]['BHCKC016'] - df[df.date==t]['BHCKC013'] -
                                                    df[df.date==t]['BHCKB492']
                                                    )    
    
    df.loc[df.date==t,'interest_base'] = multiplier[quart]*df[df.date==t]['BHCK4107']
    df.loc[df.date==t,'non_interest_base'] = multiplier[quart]*df[df.date==t]['BHCK4079']

    # other expense
    df.loc[ df.date==t, 'labor' ] =   multiplier[quart]*(df[df.date==t]['BHCK4135'] )
    df.loc[ df.date==t, 'fixed_assets' ] =   multiplier[quart]*(df[df.date==t]['BHCK4217'] )
    df.loc[ df.date==t, 'other_exp' ] =   multiplier[quart]*( df[df.date==t]['BHCKC216'] + df[df.date==t]['BHCKC232'] + df[df.date==t]['BHCK4092']#- df[df.date==t]['BHCK4146']    # - df[df.date==t]['BHCKF558']
                                                             )
	# total income tax 
    df.loc[ df.date==t,'inc_tax'] = multiplier[quart]*df[df.date==t]['BHCK4302']
	# total net income
    df.loc[ df.date==t, 'net_inc'] = multiplier[quart]*df[df.date==t]['BHCK4340']    
	# pre-tax total net income, including minority interest
    df.loc[ df.date==t, 'pre_tax_majority_net_inc'] = multiplier[quart]*df[df.date==t]['BHCK4301']  

    # individual items 
	# revenues from commercial bank
    df.loc[ df.date==t, 'int_inc'] = multiplier[quart]*( df[df.date==t]['BHCK4107'] - df[df.date==t]['BHCK4069'] )
    df.loc[ df.date==t, 'int_exp'] = multiplier[quart]*( df[df.date==t]['BHCK4073'] - df[df.date==t]['BHCK4185'] )
    df.loc[ df.date==t, 'service_dep'] = multiplier[quart]*( df[df.date==t]['BHCK4483'] )
    df.loc[ df.date==t, 'provisions'] = multiplier[quart]*( df[df.date==t]['BHCK4230'] )
    df.loc[ df.date==t, 'gains'] = multiplier[quart]*( df[df.date==t]['BHCK3521'] + df[df.date==t]['BHCK3196'] )
    df.loc[ df.date==t, 'net_service'] = multiplier[quart]*( df[df.date==t]['BHCKB492'] )
    df.loc[ df.date==t, 'other_cbank'] = multiplier[quart]*( df[df.date==t]['BHCKC013'] + df[df.date==t]['BHCKC015'] + df[df.date==t]['BHCKC016'] )
    
    # revenues from investment bank
    df.loc[ df.date==t, 'nonint_inc'] = multiplier[quart]*( df[df.date==t]['BHCK4079']  - df[df.date==t]['BHCK4483']  - df[df.date==t]['BHCKC016'] - df[df.date==t]['BHCKC013'] - df[df.date==t]['BHCKB492'] )
    df.loc[ df.date==t, 'trading'] = multiplier[quart]*( df[df.date==t]['BHCK4069'] - df[df.date==t]['BHCK4185'] )
                
    #if not last quarter of fiscal year
    if quart < 3:     
        quart = quart + 1        
    else:                         
        quart = 0
        
"""
 drop observations outside time window considered (due to data limitations)
"""

df1 = df[ (df.date>=df.date.unique()[62]) & (df.date<df.date.unique()[-1]) ]
   
"""
  make sure my decompsoed net income adds up to the aggregate series
""" 

# income statement
total_netinc = []
total_exp    = []
netint       = []
nonint       = []
labor_exp    = []
fa_exp       = []
other_exp    = []

int_base = []
nonint_base = []

total_netinc_growth = []
total_exp_growth    = [] 
netint_growth       = []
nonint_growth       = []
labor_exp_growth    = []
fa_exp_growth       = []
other_exp_growth    = []
ub = .99
lb = .01

total_netinc_cost = []
total_netinc_cost_growth = []

for at,t, in enumerate(df1.date.unique()):
    
    netint.append( df1[ df1.date ==t]['cbank_rev'].sum()/(1000*1000) )
    nonint.append( df1[ df1.date ==t]['ibank_rev'].sum()/(1000*1000) )
    
    int_base.append( df1[ df1.date ==t]['interest_base'].sum()/(1000*1000) )
    nonint_base.append( df1[ df1.date ==t]['non_interest_base'].sum()/(1000*1000) )
    
    labor_exp.append( df1[ df1.date ==t]['labor'].sum()/(1000*1000) )
    fa_exp.append( df1[ df1.date ==t]['fixed_assets'].sum()/(1000*1000) )
    other_exp.append( df1[ df1.date ==t]['other_exp'].sum()/(1000*1000) )
    
    # total, not include non-interest expense
    total_netinc.append( netint[-1] + nonint[-1] )
    total_exp.append( labor_exp[-1] + fa_exp[-1] + other_exp[-1] )
    
    total_netinc_cost.append( netint[-1] + nonint[-1] - ( labor_exp[-1] + fa_exp[-1] + other_exp[-1]) )
       
    if at > 0:
        netint_growth.append(     100*(netint[-1]    -netint[-2])    /netint[-2] )
        nonint_growth.append(     100*(nonint[-1]    -nonint[-2])    /nonint[-2] )
        
        labor_exp_growth.append( 100*(labor_exp[-1]-labor_exp[-2])/labor_exp[-2] )
        fa_exp_growth.append( 100*(fa_exp[-1]-fa_exp[-2])/fa_exp[-2] )
        other_exp_growth.append( 100*(other_exp[-1]-other_exp[-2])/other_exp[-2] )
        
        total_netinc_growth.append( 100*(total_netinc[-1]-total_netinc[-2])/total_netinc[-2] )
        total_exp_growth.append( 100*(total_exp[-1]-total_exp[-2])/total_exp[-2] )
        
        total_netinc_cost_growth.append( 100*( total_netinc_cost[-1] - total_netinc_cost[-2] )/total_netinc_cost[-2]  )
             
plt.close('all')
plt.figure(1)
plt.plot(df1.date.unique(),np.asarray((total_netinc)) - np.asarray((total_exp)),label='Net Income',lw=3)
plt.ylabel('Level ($, Billions)',fontsize=15)
plt.xlabel('Date',fontsize=15)
plt.title('Aggregate Bank Net Income',fontsize=15)

plt.figure(2)
plt.subplot(2,1,1)
plt.plot(df1.date.unique(),netint,label='cbank',lw=3,marker='o')
plt.plot(df1.date.unique(),nonint,label='ibank',lw=3)
plt.ylabel('Level ($, Billions)',fontsize=15)
plt.title('Agg Revenue by Line of Business',fontsize=15)
plt.legend(fontsize=15,loc='lower right')
plt.ylim(100,700)
plt.subplot(2,1,2)
plt.plot(df1.date.unique()[1:],netint_growth,label='cbank',lw=3,marker='o')
plt.plot(df1.date.unique()[1:],nonint_growth,label='ibank',lw=3)
plt.ylabel('QQ Change (%)',fontsize=15)
plt.title('Agg Revenue Growth by Line of Business',fontsize=15)
plt.ylim(-35,55)

plt.figure(3)
plt.subplot(2,1,1)
plt.plot(df1.date.unique(),netint,label='cbank',lw=3,marker='o')
plt.plot(df1.date.unique(),nonint,label='ibank',lw=3)
plt.plot(df1.date.unique(),total_exp,label='Expense',ls='--',lw=3)
plt.ylabel('Level ($, Billions)',fontsize=15)
plt.title('Agg Revenue by Line of Business',fontsize=15)
plt.legend(fontsize=15,loc='lower right')
plt.ylim(100,700)
plt.subplot(2,1,2)
plt.plot(df1.date.unique()[1:],netint_growth,label='cbank',lw=3,marker='o')
plt.plot(df1.date.unique()[1:],nonint_growth,label='ibank',lw=3)
plt.plot(df1.date.unique()[1:],total_exp_growth,label='Expense',lw=3,ls='--')
plt.ylabel('QQ Change (%)',fontsize=15)
plt.title('Agg Revenue Growth by Line of Business',fontsize=15)
plt.ylim(-35,55)

plt.figure(4)
#plt.plot(df1.date.unique(),total_exp,label='Total',lw=3,alpha=.3)
plt.plot(df1.date.unique(),labor_exp,label='Labor',lw=3,marker='o',markersize=7)
plt.plot(df1.date.unique(),fa_exp,label='Fixed Assets',lw=3,marker='P',markersize=7)
plt.plot(df1.date.unique(),other_exp,label='Other',lw=3,marker='+',markersize=12)
plt.legend(fontsize=15)
plt.xlabel('Date',fontsize=15)
plt.title('Decomposing Agg Non-Interest Expense',fontsize=15)
plt.ylabel('Level ($, Billions)',fontsize=15)





"""
    construct new panel dataframe with growth versions of (1) cbank_rev (2) ibank_rev (3) total liabilities BHCK2750 and (4) trade liabilities + other borrowed money BHCK3548, BHCK3190
"""

df2 = df1[[ 'date','RSSD9001','cbank_rev','ibank_rev','labor','fixed_assets','other_exp','BHCK2750','BHCK2948','BHCK3548','BHCK3190','BHCK2170','interest_base','non_interest_base' ] ]

import statsmodels.api as sm
from linearmodels import PanelOLS

# create cbank liabilities
df2['cbank_liab'] =  df2['BHCK2948'] - df2['BHCK3548'] #df2['BHCK2750']

# create ibank liabilities 
df2['ibank_liab'] = df2['BHCK3548'] + df2['BHCK3190']


# initialize and create multi-index
#df2 = df2.fillna(0)
df2.set_index(['RSSD9001','date'], inplace=True )

# set exogenous variables
exog_vars = [  'cbank_rev','ibank_rev','cbank_liab','ibank_liab' ]
exog = sm.add_constant( df2[exog_vars] )

# REGRESSION 1: labor expense
mod = PanelOLS( df2['labor'], exog, entity_effects = False, time_effects = True )

res = mod.fit()
fitted_woy = (res.fitted_values['fitted_values'] + res.estimated_effects['estimated_effects'] - res.params[1]*df2['cbank_rev'] - res.params[3]*df2['cbank_liab']  
                                                                                              -res.params[2]*df2['ibank_rev']  - res.params[4]*df2['ibank_liab'] ) 
                                                                                              
# compute expected wage component for cbank
df2['cbank_labor'] = res.params[1]*df2['cbank_rev'] + res.params[3]*df2['cbank_liab'] + (fitted_woy + res.resids)/2
df2['ibank_labor'] = res.params[2]*df2['ibank_rev'] + res.params[3]*df2['ibank_liab'] + (fitted_woy + res.resids)/2

# REGRESSION 2: fixed assets expense
mod = PanelOLS( df2['fixed_assets'], exog, entity_effects = False, time_effects = True )

res = mod.fit()
fitted_woy = (res.fitted_values['fitted_values'] + res.estimated_effects['estimated_effects'] - res.params[1]*df2['cbank_rev'] - res.params[3]*df2['cbank_liab']  
                                                                                              -res.params[2]*df2['ibank_rev']  - res.params[4]*df2['ibank_liab'] ) 
                                                                                              
# compute expected wage component for cbank
df2['cbank_fa'] = res.params[1]*df2['cbank_rev'] + res.params[3]*df2['cbank_liab'] + (fitted_woy + res.resids)/2
df2['ibank_fa'] = res.params[2]*df2['ibank_rev'] + res.params[3]*df2['ibank_liab'] + (fitted_woy + res.resids)/2

# REGRESSION 3: other expense
mod = PanelOLS( df2['other_exp'], exog, entity_effects = False, time_effects = True )

res = mod.fit()
fitted_woy = (res.fitted_values['fitted_values'] + res.estimated_effects['estimated_effects'] - res.params[1]*df2['cbank_rev'] - res.params[3]*df2['cbank_liab']  
                                                                                              -res.params[2]*df2['ibank_rev']  - res.params[4]*df2['ibank_liab'] ) 
                                                                                              
# compute expected wage component for cbank
df2['cbank_other'] = res.params[1]*df2['cbank_rev'] + res.params[3]*df2['cbank_liab'] + (fitted_woy + res.resids)/2
df2['ibank_other'] = res.params[2]*df2['ibank_rev'] + res.params[3]*df2['ibank_liab'] + (fitted_woy + res.resids)/2


# create total non-interest expense variable for (1) cbank and (2) ibank
df2['cbank_nonint_exp'] = df2['cbank_labor'] + df2['cbank_fa'] + df2['cbank_other']
df2['ibank_nonint_exp'] = df2['ibank_labor'] + df2['ibank_fa'] + df2['ibank_other']

# create net income measure for (1) cbank and (2) ibank
df2['cbank_netinc'] = df2['cbank_rev'] - df2['cbank_nonint_exp']
df2['ibank_netinc'] = df2['ibank_rev'] - df2['ibank_nonint_exp']

df2['ibank_rat'] = df2['ibank_rev']/df2['ibank_nonint_exp']
df2['cbank_rat'] = df2['cbank_rev']/df2['cbank_nonint_exp']
df2['bank_rat'] =  (df2['ibank_rev']+ df2['cbank_rev'])/(df2['ibank_nonint_exp'] + df2['cbank_nonint_exp'])


# income statement
ibank_labor = []
ibank_fa    = []  
ibank_other = []
ibank_labor_gr = []
ibank_fa_gr    = []  
ibank_other_gr = []

cbank_labor = []
cbank_fa    = []
cbank_other = []
cbank_labor_gr = []
cbank_fa_gr    = []
cbank_other_gr = []

total_labor = []
total_fa = []
total_other = []
total_labor_gr = []
total_fa_gr = []
total_other_gr = []


ibank_exp = []
cbank_exp = []

ibank_rat = []
cbank_rat = []
bank_rat  = []

ibank_rat_weight = []
cbank_rat_weight = []
bank_rat_weight  = []

ibank_netinc    = []
cbank_netinc    = []
total_netinc1    = []

ibank_netinc_small   = []
cbank_netinc_small   = []
total_netinc_small    = []

ibank_netinc_big   = []
cbank_netinc_big   = []
total_netinc_big    = []

ibank_netinc_growth    = []
cbank_netinc_growth    = []
total_netinc1_growth    = []

for at,t, in enumerate(df2.index.get_level_values('date').unique()):
    
    ibank_labor.append( df2.iloc[df2.index.get_level_values('date') == t]['ibank_labor'].sum()/(1000*1000) )
    ibank_fa.append( df2.iloc[df2.index.get_level_values('date') == t]['ibank_fa'].sum()/(1000*1000) )
    ibank_other.append( df2.iloc[df2.index.get_level_values('date') == t]['ibank_other'].sum()/(1000*1000) )

    cbank_labor.append( df2.iloc[df2.index.get_level_values('date') == t]['cbank_labor'].sum()/(1000*1000) )
    cbank_fa.append( df2.iloc[df2.index.get_level_values('date') == t]['cbank_fa'].sum()/(1000*1000) )
    cbank_other.append( df2.iloc[df2.index.get_level_values('date') == t]['cbank_other'].sum()/(1000*1000) )

    total_labor.append( ibank_labor[-1] + cbank_labor[-1] )
    total_fa.append( ibank_fa[-1] + cbank_fa[-1] )
    total_other.append( ibank_other[-1] + cbank_other[-1] )
    
    ibank_exp.append( (df2.iloc[df2.index.get_level_values('date') == t]['ibank_labor'].sum() + df2.iloc[df2.index.get_level_values('date') == t]['ibank_fa'].sum() + df2.iloc[df2.index.get_level_values('date') == t]['ibank_other'].sum())/(1000*1000) )
    cbank_exp.append( (df2.iloc[df2.index.get_level_values('date') == t]['cbank_labor'].sum() + df2.iloc[df2.index.get_level_values('date') == t]['cbank_fa'].sum() + df2.iloc[df2.index.get_level_values('date') == t]['cbank_other'].sum())/(1000*1000) )
                
    ibank_netinc.append( df2.iloc[df2.index.get_level_values('date') == t]['ibank_netinc'].sum()/(1000*1000) )
    cbank_netinc.append( df2.iloc[df2.index.get_level_values('date') == t]['cbank_netinc'].sum()/(1000*1000) )
    total_netinc1.append( ibank_netinc[-1]+cbank_netinc[-1] ) 

    ibank_netinc_small.append( df2[ (df2.index.get_level_values('date') == t) & (df2.BHCK2170 < 50*1000*1000)]['ibank_netinc'].sum()/(1000*1000) )
    cbank_netinc_small.append( df2[ (df2.index.get_level_values('date') == t) & (df2.BHCK2170 < 50*1000*1000)]['cbank_netinc'].sum()/(1000*1000) )
    total_netinc_small.append( ibank_netinc_small[-1]+cbank_netinc_small[-1] )

    ibank_netinc_big.append( df2[ (df2.index.get_level_values('date') == t) & (df2.BHCK2170 > 50*1000*1000)]['ibank_netinc'].sum()/(1000*1000) )
    cbank_netinc_big.append( df2[ (df2.index.get_level_values('date') == t) & (df2.BHCK2170 > 50*1000*1000)]['cbank_netinc'].sum()/(1000*1000) )
    total_netinc_big.append( ibank_netinc_big[-1]+cbank_netinc_big[-1] )

    ibank_rat.append( df2.iloc[df2.index.get_level_values('date') == t]['ibank_rat'].mean() )
    cbank_rat.append( df2.iloc[df2.index.get_level_values('date') == t]['cbank_rat'].mean() )
    bank_rat.append( df2.iloc[df2.index.get_level_values('date') == t]['bank_rat'].mean() )

    weight_i = df2.iloc[df2.index.get_level_values('date') == t]['ibank_rev']/df2.iloc[df2.index.get_level_values('date') == t]['ibank_rev'].sum()
    weight_c = df2.iloc[df2.index.get_level_values('date') == t]['cbank_rev']/df2.iloc[df2.index.get_level_values('date') == t]['cbank_rev'].sum()
    weight = (df2.iloc[df2.index.get_level_values('date') == t]['ibank_rev']+df2.iloc[df2.index.get_level_values('date') == t]['cbank_rev'])/(df2.iloc[df2.index.get_level_values('date') == t]['ibank_rev'].sum()+df2.iloc[df2.index.get_level_values('date') == t]['cbank_rev'].sum())
    
    ibank_rat_weight.append( (weight_i*df2.iloc[df2.index.get_level_values('date') == t]['ibank_rat']).sum() )
    cbank_rat_weight.append( (weight_c*df2.iloc[df2.index.get_level_values('date') == t]['cbank_rat']).sum() )
    bank_rat_weight.append(  (weight*df2.iloc[df2.index.get_level_values('date') == t]['bank_rat']).sum() )
         
    if at > 0:
        ibank_netinc_growth.append(     100*(ibank_netinc[-1]    -ibank_netinc[-2])    /ibank_netinc[-2] )
        cbank_netinc_growth.append(     100*(cbank_netinc[-1]    -cbank_netinc[-2])    /cbank_netinc[-2] )
        total_netinc1_growth.append(     100*(total_netinc1[-1]    -total_netinc1[-2])    /total_netinc1[-2] )
        
        ibank_labor_gr.append(  100*( ibank_labor[-1] - ibank_labor[-2] )/ibank_labor[-2] )
        cbank_labor_gr.append(  100*( cbank_labor[-1] - cbank_labor[-2] )/cbank_labor[-2] )
        total_labor_gr.append(  100*( total_labor[-1] - total_labor[-2] )/total_labor[-2] )

        ibank_fa_gr.append(  100*( ibank_fa[-1] - ibank_fa[-2] )/ibank_fa[-2] )
        cbank_fa_gr.append(  100*( cbank_fa[-1] - cbank_fa[-2] )/cbank_fa[-2] )
        total_fa_gr.append(  100*( total_fa[-1] - total_fa[-2] )/total_fa[-2] )

        ibank_other_gr.append(  100*( ibank_other[-1] - ibank_other[-2] )/ibank_other[-2] )
        cbank_other_gr.append(  100*( cbank_other[-1] - cbank_other[-2] )/cbank_other[-2] )
        total_other_gr.append(  100*( total_other[-1] - total_other[-2] )/total_other[-2] )

plt.figure(9)
plt.subplot(3,1,1)
plt.plot(df2.index.get_level_values('date').unique(),np.asarray((cbank_labor))/( np.asarray((netint))+np.asarray((nonint)) ),lw=3,label='cbank')
plt.plot(df2.index.get_level_values('date').unique(),np.asarray((ibank_labor))/( np.asarray((netint))+np.asarray((nonint)) ),lw=3,label='ibank',ls='--')
plt.legend(fontsize=15)
plt.title('Labor')
plt.subplot(3,1,2)
plt.plot(df2.index.get_level_values('date').unique(),np.asarray((cbank_fa))/( np.asarray((netint))+np.asarray((nonint)) ),lw=3,label='cbank')
plt.plot(df2.index.get_level_values('date').unique(),np.asarray((ibank_fa))/( np.asarray((netint))+np.asarray((nonint)) ),lw=3,label='ibank',ls='--')
plt.title('Fixed Assets')
plt.ylabel('Fraction',fontsize=15)
plt.subplot(3,1,3)
plt.plot(df2.index.get_level_values('date').unique(),np.asarray((cbank_other))/( np.asarray((netint))+np.asarray((nonint)) ),lw=3,label='cbank')
plt.plot(df2.index.get_level_values('date').unique(),np.asarray((ibank_other))/( np.asarray((netint))+np.asarray((nonint)) ),lw=3,label='ibank',ls='--')
plt.title('Other')
plt.xlabel('Date',fontsize=15)
plt.suptitle('Expense as Fraction of Total Income, by Line of Business',fontsize=20)

plt.figure(10)
plt.plot(df2.index.get_level_values('date').unique(),np.asarray((cbank_labor))/( np.asarray((cbank_labor))+np.asarray((cbank_fa)) + np.asarray((cbank_other)) ),lw=3,label='labor')
plt.plot(df2.index.get_level_values('date').unique(),np.asarray((cbank_fa))/( np.asarray((cbank_labor))+np.asarray((cbank_fa)) + np.asarray((cbank_other)) ),lw=3,label='fixed assets',marker='o',markersize=7)
plt.plot(df2.index.get_level_values('date').unique(),np.asarray((cbank_other))/( np.asarray((cbank_labor))+np.asarray((cbank_fa)) + np.asarray((cbank_other)) ),lw=3,label='other',marker='+',markersize=12)
plt.legend(fontsize=15)
plt.xlabel('Date',fontsize=15)
plt.title('Distribution of Commercial Bank Expense')
plt.ylabel('Fraction of Total Expense',fontsize=15)

plt.figure(11)
plt.plot(df2.index.get_level_values('date').unique(),np.asarray((ibank_labor))/( np.asarray((ibank_labor))+np.asarray((ibank_fa)) + np.asarray((ibank_other)) ),lw=3,label='labor')
plt.plot(df2.index.get_level_values('date').unique(),np.asarray((ibank_fa))/( np.asarray((ibank_labor))+np.asarray((ibank_fa)) + np.asarray((ibank_other)) ),lw=3,label='fixed assets',marker='o',markersize=7)
plt.plot(df2.index.get_level_values('date').unique(),np.asarray((ibank_other))/( np.asarray((ibank_labor))+np.asarray((ibank_fa)) + np.asarray((ibank_other)) ),lw=3,label='other',marker='+',markersize=12)
plt.legend(fontsize=15)
plt.xlabel('Date',fontsize=15)
plt.title('Distribution of Investment Bank Expense')
plt.ylabel('Fraction of Total Expense',fontsize=15)


plt.figure(10)
plt.plot(df2.index.get_level_values('date').unique(),np.asarray((cbank_exp))/( np.asarray((netint))+np.asarray((nonint)) ),label='cbank',lw=3)
plt.plot(df2.index.get_level_values('date').unique(),np.asarray((ibank_exp))/( np.asarray((netint))+np.asarray((nonint)) ),label='ibank',lw=3,ls='--')
plt.ylabel('Fraction',fontsize=15)
plt.title('Total Expense as Fraction of Total Income, by Line of Business',fontsize=15)
plt.legend(fontsize=15,loc='lower right')

plt.figure(11)
plt.plot(df2.index.get_level_values('date').unique(),cbank_netinc,label='cbank',lw=3)
plt.plot(df2.index.get_level_values('date').unique(),ibank_netinc,label='ibank',lw=3,ls='--')
plt.ylabel('Level ($, Billions)',fontsize=15)
plt.title('Agg Net Income by Line of Business',fontsize=15)
plt.legend(fontsize=15,loc='best')

plt.figure(12)
plt.plot(df2.index.get_level_values('date').unique(),int_base,label='interest income',lw=3)
plt.plot(df2.index.get_level_values('date').unique(),nonint_base,label='non-interest income',lw=3,ls='--')
plt.ylabel('Level ($, Billions)',fontsize=15)
plt.title('Agg Revenue by Interest Category',fontsize=15)
plt.legend(fontsize=15,loc='best')




"""
    Biz Cycles
"""
# import fdp series
GDP_series = pd.read_csv('GDP.csv')
gdp_lev = GDP_series.GDPC1.unique()[:-1]

import statsmodels.api as sm

cycle_gdp, trend_gdp = sm.tsa.filters.hpfilter(gdp_lev,1600)

# expense items
cycle_total, trend_total = sm.tsa.filters.hpfilter(np.asarray((total_labor)) + np.asarray((total_fa)) + np.asarray((total_other)),1600)
cycle_totali, trend_totali = sm.tsa.filters.hpfilter(np.asarray((ibank_labor)) + np.asarray((ibank_fa)) + np.asarray((ibank_other)),1600)
cycle_totalc, trend_totalc = sm.tsa.filters.hpfilter(np.asarray((cbank_labor)) + np.asarray((cbank_fa)) + np.asarray((cbank_other)),1600)

np.corrcoef([ cycle_gdp, cycle_total, cycle_totali, cycle_totalc ])

# income items
cycle_rev, trend_rev = sm.tsa.filters.hpfilter(np.asarray((netint)) + np.asarray((nonint)),1600)
cycle_revi, trend_revi = sm.tsa.filters.hpfilter(nonint,1600)
cycle_revc, trend_revc = sm.tsa.filters.hpfilter(netint,1600)

np.corrcoef([ cycle_gdp, cycle_rev, cycle_revi, cycle_revc ])

# net income items 
cycle_netinc, trend_netinc = sm.tsa.filters.hpfilter(total_netinc1,1600)
cycle_netinci, trend_netinci = sm.tsa.filters.hpfilter(ibank_netinc,1600)
cycle_netincc, trend_netincc = sm.tsa.filters.hpfilter(cbank_netinc,1600)

np.corrcoef([ cycle_gdp, cycle_netinc, cycle_netinci, cycle_netincc ])  

# baseline revenue items
cycle_total_inc, trend_total_inc = sm.tsa.filters.hpfilter(np.asarray((int_base)) + np.asarray((nonint_base)),1600)
cycle_int_base, trend_int_base = sm.tsa.filters.hpfilter(int_base,1600)
cycle_nonint_base, trend_nonint_base = sm.tsa.filters.hpfilter(nonint_base,1600)

np.corrcoef([ cycle_gdp, cycle_total_inc, cycle_nonint_base, cycle_int_base ])  


"""
    time-varying correlation of activities
"""

#----------------------------------------#
#                                        #
#   Do it first for the revenue items    #
#                                        #
#----------------------------------------#

time_corr = []

for at,t in enumerate(df1.date.unique()):
            
    temp_df = df1[ df1.date ==t ][[ 'cbank_rev','ibank_rev' ]]
    time_corr.append( np.asarray(( temp_df.corr() ))[0,1] )
    

time_corr_adj = []

for at,t in enumerate(df2.index.get_level_values('date').unique()):
            
    temp_df = df2.iloc[df2.index.get_level_values('date') == t][[ 'cbank_netinc','ibank_netinc' ]]
            
    time_corr_adj.append( np.asarray(( temp_df.corr() ))[0,1] )

time_corr_base = []

for at,t in enumerate(df1.date.unique()):
            
    temp_df = df1[ df1.date ==t ][[ 'interest_base','non_interest_base' ]]
    
    time_corr_base.append( np.asarray(( temp_df.corr() ))[0,1] )
    

plt.figure(13)
plt.plot(df1.date.unique(),time_corr,label='revenue',lw=3)
#plt.plot(df1.date.unique(),time_corr_base,label='baseline',lw=3)
plt.plot(df1.date.unique(),time_corr_adj,label='net income',lw=3,marker='X')
plt.axhline(0,ls='--',lw=3,color='black',alpha=.5)
plt.xlabel('Date',fontsize=15)
plt.ylabel('Correlation',fontsize=15)
plt.legend(fontsize=15)
plt.title('Agg Cross-Section Correlation for Ibank & Cbank',fontsize=15)


"""
 intra-bank correlations
"""

rev_corr_base = []
rev_corr = []
net_corr = []

import numpy.ma as ma

for at,t in enumerate(df2.index.get_level_values('RSSD9001').unique()):
    
    if at % 1000 ==0:
        print('iteration',at)
    
    temp_df = df2.iloc[ (df2.index.get_level_values('RSSD9001') == t) ][[ 'ibank_rev','cbank_rev','ibank_netinc','cbank_netinc','BHCK2170','non_interest_base','interest_base' ]]
    
    if (np.shape(temp_df)[0]-temp_df['ibank_rev'].isna().sum()) > 24:

        rev_corr_base.append( ma.corrcoef( ma.masked_invalid(temp_df['non_interest_base']), ma.masked_invalid(temp_df['interest_base']) )[0][1] )                
        rev_corr.append( ma.corrcoef( ma.masked_invalid(temp_df['ibank_rev']), ma.masked_invalid(temp_df['cbank_rev']) )[0][1] )
        net_corr.append( ma.corrcoef( ma.masked_invalid(temp_df['ibank_netinc']), ma.masked_invalid(temp_df['cbank_netinc']) )[0][1] )
        
    

# now do it for growth
rev_corr_growth_base = []
rev_corr_growth = []
net_corr_growth = []

for at,t in enumerate(df2.index.get_level_values('RSSD9001').unique()):
    
    if at % 500 ==0:
        print('iteration',at)
    
    temp_df = df2.iloc[ (df2.index.get_level_values('RSSD9001') == t) ][[ 'ibank_rev','cbank_rev','ibank_netinc','cbank_netinc','BHCK2170','non_interest_base','interest_base' ]]

    temp_df['ibank_rev_gr'] = temp_df['ibank_rev'].pct_change()
    temp_df['cbank_rev_gr'] = temp_df['cbank_rev'].pct_change()
    temp_df['ibank_netinc_gr'] = temp_df['ibank_netinc'].pct_change()
    temp_df['cbank_netinc_gr'] = temp_df['cbank_netinc'].pct_change()
    temp_df['non_interest_base_gr'] = temp_df['non_interest_base'].pct_change()
    temp_df['interest_base_gr'] = temp_df['interest_base'].pct_change()


    if (np.shape(temp_df)[0]-temp_df['ibank_rev'].isna().sum()) > 24:

        rev_corr_growth_base.append( ma.corrcoef( ma.masked_invalid(temp_df['non_interest_base_gr']), ma.masked_invalid(temp_df['interest_base_gr']) )[0][1] )        
        rev_corr_growth.append( ma.corrcoef( ma.masked_invalid(temp_df['ibank_rev_gr']), ma.masked_invalid(temp_df['cbank_rev_gr']) )[0][1] )
        net_corr_growth.append( ma.corrcoef( ma.masked_invalid(temp_df['ibank_netinc_gr']), ma.masked_invalid(temp_df['cbank_netinc_gr']) )[0][1] )

plt.figure(17)
plt.subplot(1,2,1)
#plt.hist(rev_corr_base,bins=25,alpha=.8,label='base')
plt.hist(rev_corr,bins=25,alpha=.8,label='revenue')
plt.hist(net_corr,bins=25,alpha=.8,label='net income')
plt.xlabel('Correlation',fontsize=15)
plt.legend(fontsize=15)
plt.title('Level Correlations',fontsize=15)
plt.subplot(1,2,2)
#plt.hist(rev_corr_growth_base,bins=25,alpha=.8,label='base')
plt.hist(rev_corr_growth,bins=25,alpha=.8,label='revenue')
plt.hist(net_corr_growth,bins=25,alpha=.8,label='net income')
plt.legend(fontsize=15)
plt.xlabel('Correlation',fontsize=15)
plt.title('Growth Correlations',fontsize=15)
plt.suptitle('Intra-Bank Correlation by Business Line',fontsize=20)




























"""

(1) decomposition should be an identity.  use individual growth rate volatilities to imply total volatility


(3) look at cross-section correlation.  why is it so much lower than without adjustment?  revenues versus net income.  

(4) identification in regression.  Think deeper!

(5) why can't i focus on level instead of growth??

(6) use the 10ks.  look at a few banks over time.  
"""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#                                           #
#   Decomposing individual revenue items    #
#                                           #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
int_inc =[]
int_exp = []
serv_dep = []
prov = []
gains = []
net_serv = []
other_c = []

nonint_inc = []
trading = []

fid = []
trade_rev = []
venture = []
securitize = []
sec_broke = []
ibank_fees = []
annuity = []
insurance = []
advisory = []

for at,t, in enumerate(df1.date.unique()):
    
    int_inc.append( df1[ df1.date ==t]['int_inc'].sum()/(1000*1000) )
    int_exp.append( df1[ df1.date ==t]['int_exp'].sum()/(1000*1000) )
    serv_dep.append( df1[ df1.date ==t]['service_dep'].sum()/(1000*1000) )
    prov.append( df1[ df1.date ==t]['provisions'].sum()/(1000*1000) )
    gains.append( df1[ df1.date ==t]['gains'].sum()/(1000*1000) )
    net_serv.append( df1[ df1.date ==t]['net_service'].sum()/(1000*1000) )
    other_c.append( df1[ df1.date ==t]['other_cbank'].sum()/(1000*1000) )

    nonint_inc.append( df1[ df1.date ==t]['nonint_inc'].sum()/(1000*1000) )
    trading.append( df1[ df1.date ==t]['trading'].sum()/(1000*1000) )

    fid.append( df1[ df1.date ==t]['fid'].sum()/(1000*1000) )
    trade_rev.append( df1[ df1.date ==t]['trade_rev'].sum()/(1000*1000) )
    venture.append( df1[ df1.date ==t]['venture'].sum()/(1000*1000) )
    securitize.append( df1[ df1.date ==t]['securitize'].sum()/(1000*1000) )
    sec_broke.append( df1[ df1.date ==t]['securities_broke'].sum()/(1000*1000) )
    ibank_fees.append( df1[ df1.date ==t]['ibank_fees'].sum()/(1000*1000) )
    annuity.append( df1[ df1.date ==t]['annuity'].sum()/(1000*1000) )
    insurance.append( df1[ df1.date ==t]['insurance'].sum()/(1000*1000) )
    advisory.append( df1[ df1.date ==t]['advisory'].sum()/(1000*1000) )
    
plt.figure(5)
plt.plot(df1.date.unique(),int_inc,label='Interest Income',lw=3)
plt.plot(df1.date.unique(),int_exp,label='Interest Expense',lw=3)
plt.plot(df1.date.unique(),serv_dep,label='Deposit Service Charge',lw=3)
plt.plot(df1.date.unique(),prov,label='Credit Loss Provisions',lw=3)
plt.ylabel('Level ($, Billions)',fontsize=15)
plt.title('Key Cbank Revenue Items',fontsize=15)
plt.legend(fontsize=15,loc='best')

plt.figure(7)
plt.plot(df1.date.unique(),fid,label='fiduciary',lw=3)
plt.plot(df1.date.unique(),trade_rev,label='trade',lw=3)
plt.plot(df1.date.unique(),venture,label='venture',lw=3)
plt.plot(df1.date.unique(),securitize,label='securitize',lw=3)
plt.plot(df1.date.unique(),sec_broke,label='sec broke',lw=3)
plt.plot(df1.date.unique(),ibank_fees,label='fees',lw=3)
plt.ylabel('Level ($, Billions)',fontsize=15)
plt.title('Key Ibank Revenue Items',fontsize=15)
plt.legend(fontsize=15,loc='best')


"""
    Stiroh Aggregate Volatility Decomposition
    
        - loosely, (comm_rev - comm_cost) = net inerest revenue and invest_rev = non-interest revenue
        
        - Stiroh works with growth rates (Q over Q)
        
        - for aggregate measures, compute for sub-periods (full sample, 2000-2010, 2010-2020)
                (1) variances of operating revenue (net interest revenue + non-interest revenue )
                (2) shares of net-int rev and non-int rev over total operating revenue
                (3) variances of (a) net interest rev and (b) non-interest revenue
                (4) covariance of (a) and (b)
"""

# truncate at 99th percentile of growth rates
total_netinc_growth = np.asarray((total_netinc_growth))
netint_growth       = np.asarray((netint_growth))
nonint_growth       = np.asarray((nonint_growth))

total_netinc_growth[ total_netinc_growth > np.quantile(total_netinc_growth,.99)] = np.quantile(total_netinc_growth,.99)
netint_growth[ netint_growth > np.quantile(netint_growth,.99)] = np.quantile(netint_growth,.99)
nonint_growth[ nonint_growth > np.quantile(nonint_growth,.99)] = np.quantile(nonint_growth,.99)

# full sample
net_share = np.sum(netint)/( np.sum(netint) + np.sum(nonint) )     
non_share = np.sum(nonint)/( np.sum(netint) + np.sum(nonint) )     

total_var = np.var( total_netinc_growth )
net_var = np.cov(netint_growth,nonint_growth)[0,0]
non_var = np.cov(netint_growth,nonint_growth)[1,1]
net_non_covar = np.cov(netint_growth,nonint_growth)[0,1]

# subset 1 (2000-2010)
net_share1 = np.sum(netint[:36])/( np.sum(netint[:36]) + np.sum(nonint[:36]) )     
non_share1 = np.sum(nonint[:36])/( np.sum(netint[:36]) + np.sum(nonint[:36]) )     

total_var1 = np.var( total_netinc_growth[:36] )
net_var1 = np.cov(netint_growth[:36],nonint_growth[:36])[0,0]
non_var1 = np.cov(netint_growth[:36],nonint_growth[:36])[1,1]
net_non_covar1 =  np.cov(netint_growth[:36],nonint_growth[:36])[0,1]

# subset 2 (2010-2020)
net_share2 = np.sum(netint[36:])/( np.sum(netint[36:]) + np.sum(nonint[36:]) )     
non_share2 = np.sum(nonint[36:])/( np.sum(netint[36:]) + np.sum(nonint[36:]) )     

total_var2 = np.var( total_netinc_growth[36:] )
net_var2 = np.cov(netint_growth[36:],nonint_growth[36:])[0,0]
non_var2 = np.cov(netint_growth[36:],nonint_growth[36:])[1,1]
net_non_covar2 =  np.cov(netint_growth[36:],nonint_growth[36:])[0,1]

print()
print('STIROH METHOD ON GROWTH RATES')
print('FULL SAMPLE')
print('                              Share (%)             Variance/Covariance            Contribution to Variance (%)')
print()
print(' Operating Revenue:                                     ',round(total_var,2),'                                             ')
print('     Net Interest :           ',round(100*net_share,3),'                  ',round(net_var,2),'                              ',round(net_share**2*net_var/total_var,2),'               ')
print('     Non-Interest :           ',round(100*non_share,3),'                  ',round(non_var,2),'                            ',round(non_share**2*non_var/total_var,2),'          ')
print('     Interaction  :                                     ',round(net_non_covar,2),'                             ',round(2*net_share*non_share*net_non_covar/total_var,2),'          ')
print('                                                                                                        ')
print() 
print('SUB-SAMPLE (2000-2010)')
print('                              Share (%)             Variance/Covariance            Contribution to Variance (%)')
print()
print(' Operating Revenue:                                     ',round(total_var1,2),'                                             ')
print('     Net Interest :           ',round(100*net_share1,3),'                  ',round(net_var1,2),'                            ',round(net_share1**2*net_var1/total_var1,2),'               ')
print('     Non-Interest :           ',round(100*non_share1,3),'                  ',round(non_var1,2),'                            ',round(non_share1**2*non_var1/total_var1,2),'          ')
print('     Interaction  :                                     ',round(net_non_covar1,2),'                             ',round(2*net_share1*non_share1*net_non_covar1/total_var1,2),'          ')
print('                                                                                                        ')
print() 
print('SUB-SAMPLE (2010-2020)')
print('                              Share (%)             Variance/Covariance            Contribution to Variance (%)')
print()
print(' Operating Revenue:                                     ',round(total_var2,2),'                                             ')
print('     Net Interest :           ',round(100*net_share2,3),'                  ',round(net_var2,2),'                             ',round(net_share2**2*net_var2/total_var2,2),'               ')
print('     Non-Interest :           ',round(100*non_share2,3),'                  ',round(non_var2,2),'                            ',round(non_share2**2*non_var2/total_var2,2),'          ')
print('     Interaction  :                                     ',round(net_non_covar2,2),'                             ',round(2*net_share2*non_share2*net_non_covar2/total_var2,2),'          ')
print('                                                                                                        ')
print() 
          
#~~~~~~~~~~~~~~~~~~~~~~~#
#                       #
#   Do it for levels    #
#                       #
#~~~~~~~~~~~~~~~~~~~~~~~#

# truncate at 99th percentile of growth rates
total_netinc = np.asarray((total_netinc))
netint       = np.asarray((netint))
nonint       = np.asarray((nonint))

total_netinc[ total_netinc > np.quantile(total_netinc,.99)] = np.quantile(total_netinc,.99)
netint[ netint > np.quantile(netint,.99)] = np.quantile(netint,.99)
nonint[ nonint > np.quantile(nonint,.99)] = np.quantile(nonint,.99)

total_var_lev = np.var( total_netinc )
net_var_lev = np.cov(netint,nonint)[0,0]
non_var_lev = np.cov(netint,nonint)[1,1]
net_non_covar_lev = np.cov(netint,nonint)[0,1]

# subset 1 (2000-2010)
total_var1_lev = np.var( total_netinc[:36] )
net_var1_lev = np.cov(netint[:36],nonint[:36])[0,0]
non_var1_lev = np.cov(netint[:36],nonint[:36])[1,1]
net_non_covar1_lev =  np.cov(netint[:36],nonint[:36])[0,1]

# subset 2 (2010-2020)
total_var2_lev = np.var( total_netinc[36:] )
net_var2_lev = np.cov(netint[36:],nonint[36:])[0,0]
non_var2_lev = np.cov(netint[36:],nonint[36:])[1,1]
net_non_covar2_lev =  np.cov(netint[36:],nonint[36:])[0,1]

print()
print('STIROH METHOD ON Levels')
print('FULL SAMPLE')
print('                              Share (%)             Variance/Covariance            Contribution to Variance (%)')
print()
print(' Operating Revenue:                                     ',round(total_var_lev,2),'                                             ')
print('     Net Interest :           ',round(100*net_share,3),'                  ',round(net_var_lev,2),'                              ',round(net_share**2*net_var_lev/total_var_lev,2),'               ')
print('     Non-Interest :           ',round(100*non_share,3),'                  ',round(non_var_lev,2),'                            ',round(non_share**2*non_var_lev/total_var_lev,2),'          ')
print('     Interaction  :                                     ',round(net_non_covar_lev,2),'                             ',round(2*net_share*non_share*net_non_covar_lev/total_var_lev,2),'          ')
print('                                                                                                        ')
print() 
print('SUB-SAMPLE (2000-2010)')
print('                              Share (%)             Variance/Covariance            Contribution to Variance (%)')
print()
print(' Operating Revenue:                                     ',round(total_var1_lev,2),'                                             ')
print('     Net Interest :           ',round(100*net_share1,3),'                  ',round(net_var1_lev,2),'                            ',round(net_share1**2*net_var1_lev/total_var1_lev,2),'               ')
print('     Non-Interest :           ',round(100*non_share1,3),'                  ',round(non_var1_lev,2),'                            ',round(non_share1**2*non_var1_lev/total_var1_lev,2),'          ')
print('     Interaction  :                                     ',round(net_non_covar1_lev,2),'                             ',round(2*net_share1*non_share1*net_non_covar1_lev/total_var1_lev,2),'          ')
print('                                                                                                        ')
print() 
print('SUB-SAMPLE (2010-2020)')
print('                              Share (%)             Variance/Covariance            Contribution to Variance (%)')
print()
print(' Operating Revenue:                                     ',round(total_var2_lev,2),'                                             ')
print('     Net Interest :           ',round(100*net_share2,3),'                  ',round(net_var2_lev,2),'                             ',round(net_share2**2*net_var2_lev/total_var2_lev,2),'               ')
print('     Non-Interest :           ',round(100*non_share2,3),'                  ',round(non_var2_lev,2),'                            ',round(non_share2**2*non_var2_lev/total_var2_lev,2),'          ')
print('     Interaction  :                                     ',round(net_non_covar2_lev,2),'                             ',round(2*net_share2*non_share2*net_non_covar2_lev/total_var2_lev,2),'          ')
print('                                                                                                        ')
print() 

plt.figure(8)
plt.subplot(3,1,1)
plt.plot(df2.index.get_level_values('date').unique(),cbank_labor,lw=3,label='cbank')
plt.plot(df2.index.get_level_values('date').unique(),ibank_labor,lw=3,label='ibank',ls='--')
plt.legend(fontsize=15)
plt.title('Labor')
plt.subplot(3,1,2)
plt.plot(df2.index.get_level_values('date').unique(),cbank_fa,lw=3,label='cbank')
plt.plot(df2.index.get_level_values('date').unique(),ibank_fa,lw=3,label='ibank',ls='--')
plt.title('Fixed Assets')
plt.ylabel('Level ($, Billions)',fontsize=15)
plt.subplot(3,1,3)
plt.plot(df2.index.get_level_values('date').unique(),cbank_other,lw=3,label='cbank')
plt.plot(df2.index.get_level_values('date').unique(),ibank_other,lw=3,label='ibank',ls='--')
plt.title('Other')
plt.xlabel('Date',fontsize=15)
plt.suptitle('Agg Expense, by Line of Business',fontsize=20)



# re-do above aggregate exercise for growth rates of net income variables
# truncate at 99th percentile of growth rates
total_netinc1_growth = np.asarray((total_netinc1_growth))
cbank_netinc_growth       = np.asarray((cbank_netinc_growth))
ibank_netinc_growth       = np.asarray((ibank_netinc_growth))

total_netinc1_growth[ total_netinc1_growth > np.quantile(total_netinc1_growth,.99)] = np.quantile(total_netinc1_growth,.99)
total_netinc1_growth[ total_netinc1_growth < np.quantile(total_netinc1_growth,.01)] = np.quantile(total_netinc1_growth,.01)

cbank_netinc_growth[ cbank_netinc_growth > np.quantile(cbank_netinc_growth,.99)] = np.quantile(cbank_netinc_growth,.99)
cbank_netinc_growth[ cbank_netinc_growth < np.quantile(cbank_netinc_growth,.01)] = np.quantile(cbank_netinc_growth,.01)

ibank_netinc_growth[ ibank_netinc_growth > np.quantile(ibank_netinc_growth,.99)] = np.quantile(ibank_netinc_growth,.99)
ibank_netinc_growth[ ibank_netinc_growth < np.quantile(ibank_netinc_growth,.01)] = np.quantile(ibank_netinc_growth,.01)

# full sample
ibank_share = np.sum(ibank_netinc)/( np.sum(ibank_netinc) + np.sum(cbank_netinc) )     
cbank_share = np.sum(cbank_netinc)/( np.sum(ibank_netinc) + np.sum(cbank_netinc) )     

total_var_adj = np.var( total_netinc1_growth )
ibank_var         = np.cov(ibank_netinc_growth,cbank_netinc_growth)[0,0]
cbank_var         = np.cov(ibank_netinc_growth,cbank_netinc_growth)[1,1]
ibank_cbank_covar = np.cov(ibank_netinc_growth,cbank_netinc_growth)[0,1]

# subset 1 (2000-2010)
ibank_share1 = np.sum(ibank_netinc[:36])/( np.sum(ibank_netinc[:36]) + np.sum(cbank_netinc[:36]) )     
cbank_share1 = np.sum(cbank_netinc[:36])/( np.sum(ibank_netinc[:36]) + np.sum(cbank_netinc[:36]) )     

total_var_adj1 = np.var( total_netinc1_growth[:36] )
ibank_var1         = np.cov(ibank_netinc_growth[:36],cbank_netinc_growth[:36])[0,0]
cbank_var1         = np.cov(ibank_netinc_growth[:36],cbank_netinc_growth[:36])[1,1]
ibank_cbank_covar1 = np.cov(ibank_netinc_growth[:36],cbank_netinc_growth[:36])[0,1]

# subset 2 (2010-2020)
ibank_share2 = np.sum(ibank_netinc[36:])/( np.sum(ibank_netinc[36:]) + np.sum(cbank_netinc[36:]) )     
cbank_share2 = np.sum(cbank_netinc[36:])/( np.sum(ibank_netinc[36:]) + np.sum(cbank_netinc[36:]) )     

total_var_adj2 = np.var( total_netinc1_growth[36:] )
ibank_var2         = np.cov(ibank_netinc_growth[36:],cbank_netinc_growth[36:])[0,0]
cbank_var2         = np.cov(ibank_netinc_growth[36:],cbank_netinc_growth[36:])[1,1]
ibank_cbank_covar2 = np.cov(ibank_netinc_growth[36:],cbank_netinc_growth[36:])[0,1]

print()
print('ADJUSTED METHOD ON GROWTH RATES')
print('FULL SAMPLE')
print('                              Share (%)             Variance/Covariance            Contribution to Variance (%)')
print()
print(' Operating Revenue:                                     ',round(total_var_adj,2),'                                             ')
print('     Net Interest :           ',round(100*cbank_share,3),'                  ',round(cbank_var,2),'                              ',round(cbank_share**2*cbank_var/total_var_adj,2),'               ')
print('     Non-Interest :           ',round(100*ibank_share,3),'                  ',round(ibank_var,2),'                            ',round(ibank_share**2*ibank_var/total_var_adj,2),'          ')
print('     Interaction  :                                     ',round(ibank_cbank_covar,2),'                             ',round(2*cbank_share*ibank_share*ibank_cbank_covar/total_var_adj,2),'          ')
print('                                                                                                        ')
print() 
print('SUB-SAMPLE (2000-2010)')
print('                              Share (%)             Variance/Covariance            Contribution to Variance (%)')
print()
print(' Operating Revenue:                                     ',round(total_var_adj1,2),'                                             ')
print('     Net Interest :           ',round(100*cbank_share1,3),'                  ',round(cbank_var1,2),'                            ',round(cbank_share1**2*cbank_var1/total_var_adj1,2),'               ')
print('     Non-Interest :           ',round(100*ibank_share1,3),'                  ',round(ibank_var1,2),'                            ',round(ibank_share1**2*ibank_var1/total_var_adj1,2),'          ')
print('     Interaction  :                                     ',round(ibank_cbank_covar1,2),'                             ',round(2*cbank_share1*ibank_share1*ibank_cbank_covar1/total_var_adj1,2),'          ')
print('                                                                                                        ')
print() 
print('SUB-SAMPLE (2010-2020)')
print('                              Share (%)             Variance/Covariance            Contribution to Variance (%)')
print()
print(' Operating Revenue:                                     ',round(total_var_adj2,2),'                                             ')
print('     Net Interest :           ',round(100*cbank_share2,3),'                  ',round(cbank_var2,2),'                             ',round(cbank_share2**2*cbank_var2/total_var_adj2,2),'               ')
print('     Non-Interest :           ',round(100*ibank_share2,3),'                  ',round(ibank_var2,2),'                            ',round(ibank_share2**2*ibank_var2/total_var_adj2,2),'          ')
print('     Interaction  :                                     ',round(ibank_cbank_covar2,2),'                             ',round(2*cbank_share2*ibank_share2*ibank_cbank_covar2/total_var_adj2,2),'          ')
print('                                                                                                        ')
print() 

#~~~~~~~~~~~~~~~~~~~~~~~~~~#
#                          #
#   Now do it on levels    #
#                          # 
#~~~~~~~~~~~~~~~~~~~~~~~~~~#
total_netinc1 = np.asarray((total_netinc1))
cbank_netinc       = np.asarray((cbank_netinc))
ibank_netinc       = np.asarray((ibank_netinc))

total_netinc1[ total_netinc1 > np.quantile(total_netinc1,.99)] = np.quantile(total_netinc1,.99)
total_netinc1[ total_netinc1 < np.quantile(total_netinc1,.01)] = np.quantile(total_netinc1,.01)

cbank_netinc[ cbank_netinc > np.quantile(cbank_netinc,.99)] = np.quantile(cbank_netinc,.99)
cbank_netinc[ cbank_netinc < np.quantile(cbank_netinc,.01)] = np.quantile(cbank_netinc,.01)

ibank_netinc[ ibank_netinc > np.quantile(ibank_netinc,.99)] = np.quantile(ibank_netinc,.99)
ibank_netinc[ ibank_netinc < np.quantile(ibank_netinc,.01)] = np.quantile(ibank_netinc,.01)

# full sample
total_var_adj_lev = np.var( total_netinc1 )
ibank_var_lev         = np.cov(ibank_netinc,cbank_netinc)[0,0]
cbank_var_lev         = np.cov(ibank_netinc,cbank_netinc)[1,1]
ibank_cbank_covar_lev = np.cov(ibank_netinc,cbank_netinc)[0,1]

# subset 1 (2000-2010)
total_var_adj1_lev = np.var( total_netinc1_growth[:36] )
ibank_var1_lev         = np.cov(ibank_netinc[:36],cbank_netinc[:36])[0,0]
cbank_var1_lev         = np.cov(ibank_netinc[:36],cbank_netinc[:36])[1,1]
ibank_cbank_covar1_lev = np.cov(ibank_netinc[:36],cbank_netinc[:36])[0,1]

# subset 2 (2010-2020)
total_var_adj2_lev = np.var( total_netinc1_growth[36:] )
ibank_var2_lev         = np.cov(ibank_netinc[36:],cbank_netinc[36:])[0,0]
cbank_var2_lev         = np.cov(ibank_netinc[36:],cbank_netinc[36:])[1,1]
ibank_cbank_covar2_lev = np.cov(ibank_netinc[36:],cbank_netinc[36:])[0,1]

print()
print('ADJUSTED METHOD ON LEVELS')
print('FULL SAMPLE')
print('                              Share (%)             Variance/Covariance            Contribution to Variance (%)')
print()
print(' Operating Revenue:                                     ',round(total_var_adj_lev,2),'                                             ')
print('     Net Interest :           ',round(100*cbank_share,3),'                  ',round(cbank_var_lev,2),'                              ',round(cbank_share**2*cbank_var_lev/total_var_adj_lev,2),'               ')
print('     Non-Interest :           ',round(100*ibank_share,3),'                  ',round(ibank_var_lev,2),'                            ',round(ibank_share**2*ibank_var_lev/total_var_adj_lev,2),'          ')
print('     Interaction  :                                     ',round(ibank_cbank_covar_lev,2),'                             ',round(2*cbank_share*ibank_share*ibank_cbank_covar_lev/total_var_adj_lev,2),'          ')
print('                                                                                                        ')
print() 
print('SUB-SAMPLE (2000-2010)')
print('                              Share (%)             Variance/Covariance            Contribution to Variance (%)')
print()
print(' Operating Revenue:                                     ',round(total_var_adj1_lev,2),'                                             ')
print('     Net Interest :           ',round(100*cbank_share1,3),'                  ',round(cbank_var1_lev,2),'                            ',round(cbank_share1**2*cbank_var1_lev/total_var_adj1_lev,2),'               ')
print('     Non-Interest :           ',round(100*ibank_share1,3),'                  ',round(ibank_var1_lev,2),'                            ',round(ibank_share1**2*ibank_var1_lev/total_var_adj1_lev,2),'          ')
print('     Interaction  :                                     ',round(ibank_cbank_covar1_lev,2),'                             ',round(2*cbank_share1*ibank_share1*ibank_cbank_covar1_lev/total_var_adj1_lev,2),'          ')
print('                                                                                                        ')
print() 
print('SUB-SAMPLE (2010-2020)')
print('                              Share (%)             Variance/Covariance            Contribution to Variance (%)')
print()
print(' Operating Revenue:                                     ',round(total_var_adj2_lev,2),'                                             ')
print('     Net Interest :           ',round(100*cbank_share2,3),'                  ',round(cbank_var2_lev,2),'                             ',round(cbank_share2**2*cbank_var2_lev/total_var_adj2_lev,2),'               ')
print('     Non-Interest :           ',round(100*ibank_share2,3),'                  ',round(ibank_var2_lev,2),'                            ',round(ibank_share2**2*ibank_var2_lev/total_var_adj2_lev,2),'          ')
print('     Interaction  :                                     ',round(ibank_cbank_covar2_lev,2),'                             ',round(2*cbank_share2*ibank_share2*ibank_cbank_covar2_lev/total_var_adj2_lev,2),'          ')
print('                                                                                                        ')
print() 






