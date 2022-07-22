import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

## Custom Code
from Parameters import *
# from CostModel import *
from GMM import *
from Estimate import *
from LinearModel import *

plt.style.use('seaborn')

#Import dataframe
#os.chdir('/home/pando004/Desktop/BankData/FRY9')
#df = pd.read_csv('frdata.csv')
os.chdir('G:/Shared drives/BankBusinessLines')
dem_spec_list = [{'dep_var': 'log_q_deposit',
                  'ind_var': [ 'log_p_deposit',
                  'bankFactor1025608' , 'bankFactor1026632' , 'bankFactor1036967' , 'bankFactor1037003' ,
                  'bankFactor1039502' , 'bankFactor1068025' , 'bankFactor1068191' , 'bankFactor1069778' ,
                   'bankFactor1070345' , 'bankFactor1073757' , 'bankFactor1074156' , 'bankFactor1078529' ,
                   'bankFactor1111435' , 'bankFactor1119794' , 'bankFactor1120754' , 'bankFactor1132449' ,
                   'bankFactor1199611' , 'bankFactor1199844' , 'bankFactor1245415' , 'bankFactor1275216' ,
                   'bankFactor1378434' , 'bankFactor1562859' , 'bankFactor1574834' , 'bankFactor1575569' ,
                   'bankFactor1951350' , 'bankFactor2162966' , 'bankFactor2277860' , 'bankFactor2380443' ,
                    'bankFactor2816906' , 'bankFactor3232316' , 'bankFactor3242838' , 'bankFactor3587146' ,
                     'bankFactor3606542' , 'bankFactor3846375' , 'bankFactor3981856' , 'bankFactor4504654' ,
                     'bankFactor4846998' , 'bankFactor5006575' , 'bankFactor5280254' ,
                     'dateFactor2016-06-30' , 'dateFactor2016-09-30' , 'dateFactor2016-12-31' , 'dateFactor2017-03-31' ,
                      'dateFactor2017-06-30' , 'dateFactor2017-09-30' , 'dateFactor2017-12-31' , 'dateFactor2018-03-31' ,
                      'dateFactor2018-06-30' , 'dateFactor2018-09-30' , 'dateFactor2018-12-31' , 'dateFactor2019-03-31' ,
                      'dateFactor2019-06-30' , 'dateFactor2019-09-30' , 'dateFactor2019-12-31' , 'dateFactor2020-03-31' ,
                      'dateFactor2020-06-30' , 'dateFactor2020-09-30'],# , 'dateFactor2020-12-31'],
                    'inst_var': [ 'FEDFUNDS',
                    'bankFactor1025608' , 'bankFactor1026632' , 'bankFactor1036967' , 'bankFactor1037003' ,
                    'bankFactor1039502' , 'bankFactor1068025' , 'bankFactor1068191' , 'bankFactor1069778' ,
                     'bankFactor1070345' , 'bankFactor1073757' , 'bankFactor1074156' , 'bankFactor1078529' ,
                     'bankFactor1111435' , 'bankFactor1119794' , 'bankFactor1120754' , 'bankFactor1132449' ,
                     'bankFactor1199611' , 'bankFactor1199844' , 'bankFactor1245415' , 'bankFactor1275216' ,
                     'bankFactor1378434' , 'bankFactor1562859' , 'bankFactor1574834' , 'bankFactor1575569' ,
                     'bankFactor1951350' , 'bankFactor2162966' , 'bankFactor2277860' , 'bankFactor2380443' ,
                      'bankFactor2816906' , 'bankFactor3232316' , 'bankFactor3242838' , 'bankFactor3587146' ,
                       'bankFactor3606542' , 'bankFactor3846375' , 'bankFactor3981856' , 'bankFactor4504654' ,
                       'bankFactor4846998' , 'bankFactor5006575' , 'bankFactor5280254' ,
                       'dateFactor2016-06-30' , 'dateFactor2016-09-30' , 'dateFactor2016-12-31' , 'dateFactor2017-03-31' ,
                        'dateFactor2017-06-30' , 'dateFactor2017-09-30' , 'dateFactor2017-12-31' , 'dateFactor2018-03-31' ,
                        'dateFactor2018-06-30' , 'dateFactor2018-09-30' , 'dateFactor2018-12-31' , 'dateFactor2019-03-31' ,
                        'dateFactor2019-06-30' , 'dateFactor2019-09-30' , 'dateFactor2019-12-31' , 'dateFactor2020-03-31' ,
                        'dateFactor2020-06-30' , 'dateFactor2020-09-30'],# , 'dateFactor2020-12-31'],
                      'flag_var': 'flag_deposit'},
{'dep_var': 'log_q_propundwrt',
                  'ind_var': [ 'log_p_propundwrt',
                  'bankFactor1036967' , 'bankFactor1037003' , 'bankFactor1039502' , 'bankFactor1068191' ,
                   'bankFactor1069778' , 'bankFactor1070345' , 'bankFactor1073757' , 'bankFactor1074156' ,
                    'bankFactor1120754' , 'bankFactor1245415' , 'bankFactor1275216' , 'bankFactor1562859' ,
                     'bankFactor1951350' ,
                     'dateFactor2016-06-30' , 'dateFactor2016-09-30' , 'dateFactor2016-12-31' , 'dateFactor2017-03-31' ,
                      'dateFactor2017-06-30' , 'dateFactor2017-09-30' , 'dateFactor2017-12-31' , 'dateFactor2018-03-31' ,
                      'dateFactor2018-06-30' , 'dateFactor2018-09-30' , 'dateFactor2018-12-31' , 'dateFactor2019-03-31' ,
                      'dateFactor2019-06-30' , 'dateFactor2019-09-30' , 'dateFactor2019-12-31' , 'dateFactor2020-03-31' ,
                      'dateFactor2020-06-30' , 'dateFactor2020-09-30'],# , 'dateFactor2020-12-31'],
                    'inst_var': [ 'log_p_propundwrt',
                    'bankFactor1036967' , 'bankFactor1037003' , 'bankFactor1039502' , 'bankFactor1068191' ,
                     'bankFactor1069778' , 'bankFactor1070345' , 'bankFactor1073757' , 'bankFactor1074156' ,
                      'bankFactor1120754' , 'bankFactor1245415' , 'bankFactor1275216' , 'bankFactor1562859' ,
                       'bankFactor1951350' ,
                       'dateFactor2016-06-30' , 'dateFactor2016-09-30' , 'dateFactor2016-12-31' , 'dateFactor2017-03-31' ,
                        'dateFactor2017-06-30' , 'dateFactor2017-09-30' , 'dateFactor2017-12-31' , 'dateFactor2018-03-31' ,
                        'dateFactor2018-06-30' , 'dateFactor2018-09-30' , 'dateFactor2018-12-31' , 'dateFactor2019-03-31' ,
                        'dateFactor2019-06-30' , 'dateFactor2019-09-30' , 'dateFactor2019-12-31' , 'dateFactor2020-03-31' ,
                        'dateFactor2020-06-30' , 'dateFactor2020-09-30'],# , 'dateFactor2020-12-31'],
                      'flag_var': 'flag_propundwrt'},
{'dep_var': 'log_q_lifeundwrt',
                  'ind_var': [ 'log_p_lifeundwrt',
                   'bankFactor1037003' , 'bankFactor1039502' , 'bankFactor1068025' , 'bankFactor1068191' ,
                    'bankFactor1070345' , 'bankFactor1073757' , 'bankFactor1119794' , 'bankFactor1120754' ,
                     'bankFactor1951350' , 'bankFactor2380443' , 'bankFactor2816906' , 'bankFactor3242838' ,
                      'bankFactor3587146' , 'bankFactor4846998',
                      'dateFactor2016-06-30' , 'dateFactor2016-09-30' , 'dateFactor2016-12-31' , 'dateFactor2017-03-31' ,
                       'dateFactor2017-06-30' , 'dateFactor2017-09-30' , 'dateFactor2017-12-31' , 'dateFactor2018-03-31' ,
                       'dateFactor2018-06-30' , 'dateFactor2018-09-30' , 'dateFactor2018-12-31' , 'dateFactor2019-03-31' ,
                       'dateFactor2019-06-30' , 'dateFactor2019-09-30' , 'dateFactor2019-12-31' , 'dateFactor2020-03-31' ,
                       'dateFactor2020-06-30' , 'dateFactor2020-09-30'],# , 'dateFactor2020-12-31'],
                    'inst_var': [ 'log_p_lifeundwrt',
                     'bankFactor1037003' , 'bankFactor1039502' , 'bankFactor1068025' , 'bankFactor1068191' ,
                      'bankFactor1070345' , 'bankFactor1073757' , 'bankFactor1119794' , 'bankFactor1120754' ,
                       'bankFactor1951350' , 'bankFactor2380443' , 'bankFactor2816906' , 'bankFactor3242838' ,
                        'bankFactor3587146' , 'bankFactor4846998',
                        'dateFactor2016-06-30' , 'dateFactor2016-09-30' , 'dateFactor2016-12-31' , 'dateFactor2017-03-31' ,
                         'dateFactor2017-06-30' , 'dateFactor2017-09-30' , 'dateFactor2017-12-31' , 'dateFactor2018-03-31' ,
                         'dateFactor2018-06-30' , 'dateFactor2018-09-30' , 'dateFactor2018-12-31' , 'dateFactor2019-03-31' ,
                         'dateFactor2019-06-30' , 'dateFactor2019-09-30' , 'dateFactor2019-12-31' , 'dateFactor2020-03-31' ,
                         'dateFactor2020-06-30' , 'dateFactor2020-09-30'],# , 'dateFactor2020-12-31'],
                      'flag_var': 'flag_lifeundwrt'},
{'dep_var': 'log_q_annuity',
                  'ind_var': [ 'log_p_annuity',
                  'bankFactor1025608' , 'bankFactor1026632' , 'bankFactor1036967' , 'bankFactor1037003' ,
                   'bankFactor1039502' , 'bankFactor1068025' , 'bankFactor1068191' , 'bankFactor1069778' ,
                    'bankFactor1070345' , 'bankFactor1073757' , 'bankFactor1074156' , 'bankFactor1078529' ,
                     'bankFactor1111435' , 'bankFactor1119794' , 'bankFactor1120754' , 'bankFactor1132449' ,
                      'bankFactor1199611' , 'bankFactor1199844' , 'bankFactor1245415' , 'bankFactor1275216' ,
                       'bankFactor1378434' , 'bankFactor1574834' , 'bankFactor1575569' , 'bankFactor1951350' ,
                        'bankFactor2162966' , 'bankFactor2277860' , 'bankFactor2380443' , 'bankFactor2816906' ,
                         'bankFactor3232316' , 'bankFactor3242838' , 'bankFactor3587146' , 'bankFactor3606542' ,
                          'bankFactor3981856' , 'bankFactor4504654' , 'bankFactor4846998' , 'bankFactor5280254' ,
                          'dateFactor2016-06-30' , 'dateFactor2016-09-30' , 'dateFactor2016-12-31' , 'dateFactor2017-03-31' ,
                           'dateFactor2017-06-30' , 'dateFactor2017-09-30' , 'dateFactor2017-12-31' , 'dateFactor2018-03-31' ,
                           'dateFactor2018-06-30' , 'dateFactor2018-09-30' , 'dateFactor2018-12-31' , 'dateFactor2019-03-31' ,
                           'dateFactor2019-06-30' , 'dateFactor2019-09-30' , 'dateFactor2019-12-31' , 'dateFactor2020-03-31' ,
                           'dateFactor2020-06-30' , 'dateFactor2020-09-30'],# , 'dateFactor2020-12-31'],
                    'inst_var': [ 'log_p_annuity',
                    'bankFactor1025608' , 'bankFactor1026632' , 'bankFactor1036967' , 'bankFactor1037003' ,
                     'bankFactor1039502' , 'bankFactor1068025' , 'bankFactor1068191' , 'bankFactor1069778' ,
                      'bankFactor1070345' , 'bankFactor1073757' , 'bankFactor1074156' , 'bankFactor1078529' ,
                       'bankFactor1111435' , 'bankFactor1119794' , 'bankFactor1120754' , 'bankFactor1132449' ,
                        'bankFactor1199611' , 'bankFactor1199844' , 'bankFactor1245415' , 'bankFactor1275216' ,
                         'bankFactor1378434' , 'bankFactor1574834' , 'bankFactor1575569' , 'bankFactor1951350' ,
                          'bankFactor2162966' , 'bankFactor2277860' , 'bankFactor2380443' , 'bankFactor2816906' ,
                           'bankFactor3232316' , 'bankFactor3242838' , 'bankFactor3587146' , 'bankFactor3606542' ,
                            'bankFactor3981856' , 'bankFactor4504654' , 'bankFactor4846998' , 'bankFactor5280254' ,
                            'dateFactor2016-06-30' , 'dateFactor2016-09-30' , 'dateFactor2016-12-31' , 'dateFactor2017-03-31' ,
                             'dateFactor2017-06-30' , 'dateFactor2017-09-30' , 'dateFactor2017-12-31' , 'dateFactor2018-03-31' ,
                             'dateFactor2018-06-30' , 'dateFactor2018-09-30' , 'dateFactor2018-12-31' , 'dateFactor2019-03-31' ,
                             'dateFactor2019-06-30' , 'dateFactor2019-09-30' , 'dateFactor2019-12-31' , 'dateFactor2020-03-31' ,
                             'dateFactor2020-06-30' , 'dateFactor2020-09-30'],# , 'dateFactor2020-12-31'],
                      'flag_var': 'flag_annuity'},
{'dep_var': 'log_q_inv',
                  'ind_var': [ 'log_p_inv',
                   'bankFactor1025608' , 'bankFactor1026632' , 'bankFactor1036967' , 'bankFactor1037003' ,
                    'bankFactor1039502' , 'bankFactor1068025' , 'bankFactor1068191' , 'bankFactor1069778' ,
                     'bankFactor1070345' , 'bankFactor1073757' , 'bankFactor1074156' , 'bankFactor1078529' ,
                      'bankFactor1111435' , 'bankFactor1119794' , 'bankFactor1120754' , 'bankFactor1132449' ,
                       'bankFactor1199611' , 'bankFactor1199844' , 'bankFactor1245415' , 'bankFactor1275216' ,
                        'bankFactor1378434' , 'bankFactor1562859' , 'bankFactor1574834' , 'bankFactor1575569' ,
                         'bankFactor1951350' , 'bankFactor2162966' , 'bankFactor2277860' , 'bankFactor2380443' ,
                          'bankFactor2816906' , 'bankFactor3232316' , 'bankFactor3242838' , 'bankFactor3587146' ,
                           'bankFactor3606542' , 'bankFactor3846375' , 'bankFactor3981856' , 'bankFactor4504654' ,
                            'bankFactor4846998' , 'bankFactor5006575' , 'bankFactor5280254' ,
                            'dateFactor2016-06-30' , 'dateFactor2016-09-30' , 'dateFactor2016-12-31' , 'dateFactor2017-03-31' ,
                             'dateFactor2017-06-30' , 'dateFactor2017-09-30' , 'dateFactor2017-12-31' , 'dateFactor2018-03-31' ,
                             'dateFactor2018-06-30' , 'dateFactor2018-09-30' , 'dateFactor2018-12-31' , 'dateFactor2019-03-31' ,
                             'dateFactor2019-06-30' , 'dateFactor2019-09-30' , 'dateFactor2019-12-31' , 'dateFactor2020-03-31' ,
                             'dateFactor2020-06-30' , 'dateFactor2020-09-30'],# , 'dateFactor2020-12-31'],
                    'inst_var': [ 'log_p_inv',
                     'bankFactor1025608' , 'bankFactor1026632' , 'bankFactor1036967' , 'bankFactor1037003' ,
                      'bankFactor1039502' , 'bankFactor1068025' , 'bankFactor1068191' , 'bankFactor1069778' ,
                       'bankFactor1070345' , 'bankFactor1073757' , 'bankFactor1074156' , 'bankFactor1078529' ,
                        'bankFactor1111435' , 'bankFactor1119794' , 'bankFactor1120754' , 'bankFactor1132449' ,
                         'bankFactor1199611' , 'bankFactor1199844' , 'bankFactor1245415' , 'bankFactor1275216' ,
                          'bankFactor1378434' , 'bankFactor1562859' , 'bankFactor1574834' , 'bankFactor1575569' ,
                           'bankFactor1951350' , 'bankFactor2162966' , 'bankFactor2277860' , 'bankFactor2380443' ,
                            'bankFactor2816906' , 'bankFactor3232316' , 'bankFactor3242838' , 'bankFactor3587146' ,
                             'bankFactor3606542' , 'bankFactor3846375' , 'bankFactor3981856' , 'bankFactor4504654' ,
                              'bankFactor4846998' , 'bankFactor5006575' , 'bankFactor5280254' ,
                              'dateFactor2016-06-30' , 'dateFactor2016-09-30' , 'dateFactor2016-12-31' , 'dateFactor2017-03-31' ,
                               'dateFactor2017-06-30' , 'dateFactor2017-09-30' , 'dateFactor2017-12-31' , 'dateFactor2018-03-31' ,
                               'dateFactor2018-06-30' , 'dateFactor2018-09-30' , 'dateFactor2018-12-31' , 'dateFactor2019-03-31' ,
                               'dateFactor2019-06-30' , 'dateFactor2019-09-30' , 'dateFactor2019-12-31' , 'dateFactor2020-03-31' ,
                               'dateFactor2020-06-30' , 'dateFactor2020-09-30'],# , 'dateFactor2020-12-31'],
                      'flag_var': 'flag_inv'}   ]

cost_spec = {'dep_var':'cost_dep_var','ind_var':['rev_deposit_tilde' , 'rev_propundwrt' , 'rev_lifeundwrt' , 'rev_annuity' , 'rev_inv']}







### Read in Data
df = pd.read_csv('Data/GMMSample.csv')
data = df.to_numpy()

### Check Full Rank Condition
p = Parameter(df,dem_spec_list,cost_spec)
p.check_full_rank(data)


### Create Weighting Matrix
# Only possible because it is specified as exactly identified
# Need some more general code here...
W = np.identity(p.parnum)

### Estimate Model
newton_raphson(data,p,W,1e-6)

### Output Parameters
# Still Missing Standard Errors
p.output(data,W)
