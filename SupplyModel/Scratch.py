import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

## Custom Code
from ProfitFunctions import *
from GMM import *
from Estimate import *

plt.style.use('seaborn')

#Import dataframe
#os.chdir('/home/pando004/Desktop/BankData/FRY9')
#df = pd.read_csv('frdata.csv')
os.chdir('G:/Shared drives/BankBusinessLines')
df = pd.read_csv('Data/GMMSample.csv')

parameter_vector = [1000.,-800.,-700.,-80.,-120.,0.5,0.8,0.6,0.9]

df = simulate(df,parameter_vector)


deviations = [10.,10.,10.,10.,10.,0.1,0.1,0.1,0.1]
p0 = parameter_vector + np.random.rand(len(parameter_vector))*deviations - deviations

p_est = newton_raphson(df,p0)


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
# moments,G,H = calc_cost_moments_withderivatives(df,p)
# grad = gmm_gradient(moments,G)
# print(grad)
#
# grad_test = numerical_gradient(df,parameter_vector)
# print(grad_test)
# print((grad-grad_test)/grad)
# #
# print("Hessian Test")
# hess = gmm_hessian(moments,G,H)
# print(hess)
#
#
# hess_test = numerical_hessian(df,parameter_vector)
# print(hess_test)
#
# print((hess-hess_test)/hess)
