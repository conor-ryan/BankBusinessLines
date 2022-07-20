import statsmodels
import numpy as np

### General Prediction Error
def lm_residual(data,par,spec):
    Y = data[:,spec['dep_var']]
    X = data[:,spec['ind_var']]
    beta = par.param_vec[spec['param']]
    residuals =  np.matmul(X,beta) - Y
    return residuals

def demandIV(data,par):
    K = len(par.dem_spec_list)
    N = par.rownum
    # dem_residual_matrix = zeros(N,K)
    mom = np.empty(shape=(0,))
    for k in range(K):
        spec = par.dem_spec_list[k]
        res = lm_residual(data,par,spec)
        Z = data[:,spec['inst_var']]
        mom = np.append(mom,np.matmul(res,Z))
        # dem_residual_matrix[:,k] = res
    return mom

def demand_residuals(data,par):
    K = len(par.dem_spec_list)
    N = par.rownum
    dem_residual_matrix = np.zeros(N,K)
    for k in range(K):
        spec = par.dem_spec_list[k]
        res = lm_residual(data,par,spec)
        dem_residual_matrix[:,k] = res
    return dem_residual_matrix

def demandIV_moment_derivatives(data,par):
        K = length(par.dem_spec_list)
        N = par.rownum
        IVmoments = demandIV(data,par)
        grad = np.empty(shape = (0,par.parnum,))
        hess = np.zeros(len(IV_moments),par.parnum,par.parnum)
        for k in range(K):
            spec = par.dem_spec_list[k]
            grad_residual = np.zeros((par.rownum,par.parnum))
            grad_residual[:,spec['param']] = data[:,spec['ind_var']]
            Z = data[:,spec['inst_var']]
            grad = np.concatenate((grad,np.matmul(Z,grad_residual)),axis=0)
        return IVmoments, grad, hess

def cost_moments(data,par):
    res_mat = np.transpose(demand_residuals(data,par))
    cost_res = lm_residual(data,par,par.cost_spec)
    moments = np.matmul(res_mat,cost_res)
    return moments

def cost_moments_derivatives(data,par):
    res_mat = np.transpose(demand_residuals(data,par))
    cost_res = lm_residual(data,par,par.cost_spec)
    moments = np.matmul(res_mat,cost_res)

    grad = np.zeros(len(moments),par.parnum)
    hess = np.zeros(len(IV_moments),par.parnum,par.parnum)
    K = length(par.dem_spec_list)

    for k in range(K):
        spec = par.dem_spec_list[k]
        grad[k,spec['param']] = np.matmul(np.transpose(cost_res),data[:,spec['ind_var']])
        grad[k,par.cost_spec['param']] = np.matmul(np.transpose(data[:,par.cost_spec['ind_var']]),np.transpose(res_mat[k,:]))
        hess[k,spec['param'],par.cost_spec['param']] =np.matmul(np.transpose(data[:,par.cost_spec['ind_var']]),data[:,spec['ind_var']])
        hess[k,par.cost_spec['param'],spec['param']] =np.matmul(np.transpose(data[:,spec['ind_var']]),data[:,par.cost_spec['ind_var']])
    return moments
    


# Derive the non-price product quality from structural demand equation
# log(s_ij) - log(s_i0) = alpha*p + beta*X + epsilon
def product_deltas(s,s_0,r,alpha):
    delta = np.log(s) - np.log(s_0) - alpha*r
    return delta

### Functions to compute the demand residuals for each product category
def deposit_demand_residuals(df,par):
    # Get Demand Deltas
    deltas = df.apply(lambda x: product_deltas(x.s_dep,x.s_dep_0,x.r_dep,par.alpha_dep),result_type="expand",axis=1)
    deltas = deltas.to_numpy()
    # Output Residuals
    residuals = deltas - np.matmul(par.X_dep,par.beta_dep)
    return residuals

def consumer_demand_residuals(df,par):
    # Get Demand Deltas
    deltas = df.apply(lambda x: product_deltas(x.s_cons,x.s_cons_0,x.r_cons,par.alpha_cons),result_type="expand",axis=1)
    deltas = deltas.to_numpy()
    # Output Residuals
    residuals = deltas - np.matmul(par.X_cons,par.beta_cons)
    return residuals

def commerical_demand_residuals(df,par):
    # Get Demand Deltas
    deltas = df.apply(lambda x: product_deltas(x.s_comm,x.s_comm_0,x.r_comm,par.alpha_comm),result_type="expand",axis=1)
    deltas = deltas.to_numpy()
    # Output Residuals
    residuals = deltas - np.matmul(par.X_comm,par.beta_comm)
    return residuals

def insurance_demand_residuals(df,par):
    # Get Demand Deltas
    deltas = df.apply(lambda x: product_deltas(x.s_ins,x.s_ins_0,x.p_ins,par.alpha_ins),result_type="expand",axis=1)
    deltas = deltas.to_numpy()
    # Output Residuals
    residuals = deltas - np.matmul(par.X_ins,par.beta_ins)
    return residuals

def investment_demand_residuals(df,par):
    # Get Demand Deltas
    deltas = df.apply(lambda x: product_deltas(x.s_inv,x.s_inv_0,x.p_inv,par.alpha_inv),result_type="expand",axis=1)
    deltas = deltas.to_numpy()
    # Output Residuals
    residuals = deltas - np.matmul(par.X_inv,par.beta_inv)
    return residuals

### Compute IV moments. Checks which equations have instruments, then computes the moments.
def IV_moments(df,par):
    mom = np.empty(shape=(0,))
    if (par.Z_dep is not None):
         residuals = deposit_demand_residuals(df,par)
         mom = np.append(mom,np.matmul(residuals,par.Z_dep))
    if (par.Z_cons is not None):
         residuals = consumer_demand_residuals(df,par)
         mom = np.append(mom,np.matmul(residuals,par.Z_cons))
    if (par.Z_comm is not None):
         residuals = commerical_demand_residuals(df,par)
         mom = np.append(mom,np.matmul(residuals,par.Z_comm))
    if (par.Z_ins is not None):
         residuals = insurance_demand_residuals(df,par)
         mom = np.append(mom,np.matmul(residuals,par.Z_ins))
    if (par.Z_inv is not None):
         residuals = investment_demand_residuals(df,par)
         mom = np.append(mom,np.matmul(residuals,par.Z_inv))
    return mom

### Compute the instrument moments from the deposit demand equation
def deposit_IV_moments(df,par):
    residuals = deposit_demand_residuals(df,par)
    IV_mom = np.matmul(residuals,par.Z_dep)
    return IV_mom


### Compute derivatives of IV moments. Checks which equations have instruments, then computes the moments.
def IV_mom_derivatives(df,par):
    grad = np.empty(shape = (0,par.parnum,))


    hess = np.empty(shape = (0,par.parnum,par.parnum))
    if (par.Z_dep is not None):
        grad_residual = np.zeros((par.rownum,par.parnum))
        grad_residual[:,par.dep_index] = -df.r_dep
        grad_residual[:,par.beta_dep_index] = -par.X_dep
        grad = np.concatenate((grad,np.matmul(np.transpose(par.Z_dep),grad_residual)),axis=0)
        hess = np.concatenate((hess,np.zeros((par.Z_dep.shape[1],par.parnum,par.parnum))),axis=0)
    if (par.Z_cons is not None):
        grad_residual = np.zeros((par.rownum,par.parnum))
        grad_residual[:,par.cons_index] = -df.r_cons
        grad_residual[:,par.beta_cons_index] = -par.X_cons
        grad = np.concatenate((grad,np.matmul(np.transpose(par.Z_cons),grad_residual)),axis=0)
        hess = np.concatenate((hess,np.zeros((par.Z_dep.shape[1],par.parnum,par.parnum))),axis=0)
    if (par.Z_comm is not None):
        grad_residual = np.zeros((par.rownum,par.parnum))
        grad_residual[:,par.comm_index] = -df.r_comm
        grad_residual[:,par.beta_comm_index] = -par.X_comm
        grad = np.concatenate((grad,np.matmul(np.transpose(par.Z_comm),grad_residual)),axis=0)
        hess = np.concatenate((hess,np.zeros((par.Z_dep.shape[1],par.parnum,par.parnum))),axis=0)
    if (par.Z_ins is not None):
        grad_residual = np.zeros((par.rownum,par.parnum))
        grad_residual[:,par.ins_index] = -df.r_ins
        grad_residual[:,par.beta_ins_index] = -par.X_ins
        grad = np.concatenate((grad,np.matmul(np.transpose(par.Z_ins),grad_residual)),axis=0)
        hess = np.concatenate((hess,np.zeros((par.Z_dep.shape[1],par.parnum,par.parnum))),axis=0)
    if (par.Z_inv is not None):
        grad_residual = np.zeros((par.rownum,par.parnum))
        grad_residual[:,par.inv_index] = -df.r_inv
        grad_residual[:,par.beta_inv_index] = -par.X_inv
        grad = np.concatenate((grad,np.matmul(np.transpose(par.Z_inv),grad_residual)),axis=0)
        hess = np.concatenate((hess,np.zeros((par.Z_dep.shape[1],par.parnum,par.parnum))),axis=0)
    return grad, hess



def dep_IV_mom_derivatives(df,par):
    grad_residual = np.zeros((par.X.shape[0],par.parnum))
    grad_residual[:,par.dep_index] = -df.r_dep
    grad_residual[:,par.beta_index] = -par.X

    grad = np.matmul(np.transpose(par.Z),grad_residual)

    hess = np.zeros((par.Z.shape[1],par.parnum,par.parnum))

    return grad, hess

def annihilator_matrix(X):
    XX = np.matmul(np.transpose(X),X)
    XX_inv = np.linalg.inv(XX)

    return np.identity(X.shape[0]) - np.matmul(np.matmul(X,XX_inv),np.transpose(X))
