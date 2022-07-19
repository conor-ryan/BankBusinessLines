import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

## Custom Code
from Parameters import *
from CostModel import *
from GMM import *
from Estimate import *

plt.style.use('seaborn')

#Import dataframe
#os.chdir('/home/pando004/Desktop/BankData/FRY9')
os.chdir('G:/Shared drives/BankBusinessLines')

### Market Data
df = pd.read_csv('Data/estimation_data.csv')
data = df.to_numpy()

parameter_vector = np.array([4,4,4,4,4,1e5])
p = Parameter(parameter_vector,df)
#Weighting Matrix
W = np.identity(data.shape[0])/1e3

newton_raphson(data,p,W)

print('Deposits,Annuity, Investments')
elasticity_indices = np.concatenate(([p.par_dep_index],p.par_prod_index))
print('Fixed Cost ',p.param_vec[p.par_fc_index])
print('Elasticities ',p.param_vec[elasticity_indices])
print('Markups ',1/(1-1/p.param_vec[elasticity_indices])-1)
print('Regression Coefficients: ',(1-1/p.param_vec[elasticity_indices]))
