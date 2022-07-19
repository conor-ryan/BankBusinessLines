import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

## Custom Code
from Cost_Prediction_Functions import *
from GMM import *
from Estimate import *

plt.style.use('seaborn')

#Import dataframe
#os.chdir('/home/pando004/Desktop/BankData/FRY9')
os.chdir('G:/Shared drives/BankBusinessLines')

### Market Data
df = pd.read_csv('Data/estimation_data.csv')
data = df.to_numpy()

parameter_vector = np.array([4,4,4,4,4])
p = Parameter(parameter_vector,df)

#Weighting Matrix
W = np.identity(data.shape[0])/1e10

newton_raphson(data,p,W)

print('Deposits, Property, Life, Annuity, Investments')
print('Elasticities ',p.param_vec)
print('Markups ',1/(1-1/p.param_vec)-1)
