import statsmodels
import numpy as np

def deposit_deltas(s_dep,s_dep_0,r_dep,par):
    # Derive the non-price product quality from structural demand equation
    delta = np.log(s_dep) - np.log(s_dep_0) - par.alpha_dep*r_dep
    return delta

def deposit_demand_residuals(df,par):
    # Get Demand Deltas
    deltas = df.apply(lambda x: deposit_deltas(x.s_dep,x.s_dep_0,x.r_dep,par),result_type="expand",axis=1)
    deltas = deltas.to_numpy()
    # Output Residuals
    # residuals = np.matmul(deltas,par.M)
    residuals = deltas - np.matmul(par.X,par.beta)
    return residuals

### Compute the instrument moments from the deposit demand equation
def deposit_IV_moments(df,par):
    residuals = deposit_demand_residuals(df,par)
    IV_mom = np.matmul(residuals,par.Z)
    return IV_mom

def dep_IV_mom_derivatives(df,par):
    grad_residual = np.zeros((par.X.shape[0],par.parnum))
    grad_residual[:,par.dep_index] = -df.r_dep
    grad_residual[:,par.beta_index] = -par.X
    # grad_residuals = -np.matmul(df.r_dep.to_numpy(),par.M)
    grad = np.matmul(np.transpose(par.Z),grad_residual)
    #
    # ### Alpha_Deposit is the first parameter
    # ## Create empty matrices, and fill in the zeros
    # grad = np.zeros((len(grad_iv),par.parnum))
    # grad[:,par.dep_index] = grad_iv
    hess = np.zeros((par.Z.shape[1],par.parnum,par.parnum))

    return grad, hess

def annihilator_matrix(X):
    XX = np.matmul(np.transpose(X),X)
    XX_inv = np.linalg.inv(XX)

    return np.identity(X.shape[0]) - np.matmul(np.matmul(X,XX_inv),np.transpose(X))
