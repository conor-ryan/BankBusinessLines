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
#os.chdir('/home/pando004/Desktop/BankData/FRY9')v
#df = pd.read_csv('frdata.csv')
os.chdir('G:/Shared drives/BankBusinessLines')

### Market Data
df = pd.read_csv('Data/estimation_data.csv')
data = df.to_numpy()

parameter_vector = np.array([2.409,2.233,61.14,2.31e5])
p = Parameter(parameter_vector,df)

cost_moment_length = data.shape[0]
W = np.identity(cost_moment_length)

print(predicted_expenses(data,p))


mom = pred_exp_moments(data,p)
print('MSE ',sum(mom**2))


mom1, d_exp = gradient_pred_exp(data,p)
mom2, d_exp1, d2_exp = hessian_pred_exp(data,p)

print('Moment Difference 1 ', sum(mom-mom1))
print('Moment Difference 2 ', sum(mom-mom2))
print('Gradient Difference 1 ', sum(d_exp-d_exp1))


mom = compute_gmm(data,p,W)
print('GMM objective value ',mom)


grad = compute_gmm_gradient(data,p,W)
mom2, grad1, hess = compute_gmm_hessian(data,p,W)

print('Obj Difference 2 ', mom-mom2)
print('Gradient Difference 1 ', sum(grad-grad1))

print('Gradient', grad)


grad_test = numerical_gradient(data,p,W)
print('Gradient Test',grad_test)
hess_test = numerical_hessian(data,p,W)
print('Hessian', hess)
print('Hessian Test',hess_test)
