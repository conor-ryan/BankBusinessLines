import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

## Custom Code
from ProfitFunctions import *
from GMM import *
from Estimate import *
from DemandIV import *

plt.style.use('seaborn')

#Import dataframe
#os.chdir('/home/pando004/Desktop/BankData/FRY9')
#df = pd.read_csv('frdata.csv')
os.chdir('G:/Shared drives/BankBusinessLines')

### Market Data
df = pd.read_csv('Data/GMMSample.csv')

## Exogenous Deposit Demand Covariates
X = pd.read_csv('Data/ExogenousDemandCovariates.csv').to_numpy()
M = annihilator_matrix(X)
## Deposit Demand Instruments
Z = pd.read_csv('Data/DemandInstruments.csv').to_numpy()

### Weighting Matrix
cost_moment_length = df.to_numpy().shape[0]
IV_moment_length = Z.shape[1]
print(cost_moment_length)
print(IV_moment_length)

W = np.identity(cost_moment_length+IV_moment_length)*1e-12
# W = np.identity(IV_moment_length)
Szz = np.matmul(np.transpose(Z),Z)
W[0:IV_moment_length,0:IV_moment_length] = np.linalg.inv(Szz)
print(W)
parameter_vector = np.array([3.166537e+01,-800.,-700.,-80.,-120.,0.5,0.5,0.5,0.5])
parameter_vector = np.concatenate((parameter_vector,np.zeros(X.shape[1])),axis=0)
p = Parameter(parameter_vector,X,Z)
IV_mom = deposit_IV_moments(df,p)
grad = dep_IV_mom_derivatives(df,p)

# print(IV_mom)

print("Residual Stats")
print(np.mean(IV_mom))
print(np.median(IV_mom))
print(np.max(IV_mom))
print(np.min(IV_mom))


# df = simulate(df,parameter_vector,X,Z)

#
deviations = np.concatenate(([10.,100.,100.,100.,100.,0.3,0.3,0.3,0.3],np.zeros(X.shape[1])),axis=0)

p0 = parameter_vector + np.random.rand(len(parameter_vector))*deviations - deviations
p0 = parameter_vector.copy()
#
p_est = newton_raphson(df,X,Z,p0,W)

#
# p_idx = [0]
# p_idx.extend(list(range(9,(9+X.shape[1]))))
# print("Index",p_idx)
# p_est = newton_raphson(df,X,Z,p0,W,p_idx=p_idx)


# np.set_printoptions(precision=2,suppress=True)
# ### Initial Evaluation
# fval, G, H = gmm.compute_gmm_hessian(df,p0)
# # G = G[0:5]
# # H = H[0:5,0:5]
# grad_size = np.sqrt(np.dot(G,G))
# param_vec = p0.copy()
# itr=0
# # Initialize Gradient Increment
# alpha = 0.1

# print("Gradient Test")
# # moments,G,H = calc_cost_moments_withderivatives(df,p)
# fval, grad, hess =  compute_gmm_hessian(df,M,Z,parameter_vector,W)
# print(grad)
#
# grad_test = numerical_gradient(df,M,Z,parameter_vector,W)
# print(grad_test)
# print((grad-grad_test)/grad)
#
# print("Hessian Test")
# print(hess)
#
# hess_test = numerical_hessian(df,M,Z,parameter_vector,W)
# print(hess_test)
#
# print((hess-hess_test)/hess)


# p_est = newton_raphson(df,M,Z,parameter_vector)
