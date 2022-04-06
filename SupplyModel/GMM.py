# import ProfitFunctions as pf
import Cost_Prediction_Functions as cp
import numpy as np
import pandas as pd



#
# def simulate(df,parameters,X_dep=None,X_cons=None,X_comm=None,X_ins=None,X_inv=None,Z_dep = None,Z_cons=None,Z_comm=None,Z_ins=None,Z_inv=None):
#     par = Parameter(parameters,X_dep=X_dep,X_cons=X_cons,X_comm=X_comm,X_ins=X_ins,X_inv=X_inv,Z_dep = Z_dep,Z_cons=Z_cons,Z_comm=Z_comm,Z_ins=Z_ins,Z_inv=Z_inv)
#     # Marginal Cost Estimate
#     mc_results = df.apply(lambda x: pf.implied_marginal_cost(x.r_dep,x.r_cons,x.r_comm,x.p_inv,x.p_ins,
#                                                 x.s_dep,x.s_cons,x.s_comm,x.s_inv,x.s_ins,par),result_type="expand",axis=1)
#     mc_results.columns = ["mc_cons", "mc_comm", "mc_inv", "mc_ins"]
#
#     # Total Cost Estimate
#     df_cost = pd.concat([mc_results,df],axis="columns")
#     total_cost = df_cost.apply(lambda x: pf.total_cost(x.L_cons,x.L_comm,x.r_dep,x.q_dep,
#                                                 x.q_cons,x.q_comm,x.q_inv,x.q_ins,
#                                                 x.mc_cons,x.mc_comm,x.mc_inv,x.mc_ins,par),result_type="expand",axis=1)
#     df['total_cost'] = total_cost
#     return df


### Compute GMM Objective based on a weighting matrix W
def gmm_objective(moments,W):
    return np.matmul(np.transpose(moments),np.matmul(W,moments))

### Translate moment gradients into GMM objective function gradient
def gmm_gradient(moments,grad,W):
    gmm_grad = np.zeros(grad.shape[1])

    gmm_grad = np.matmul(np.transpose(grad),np.matmul(W,moments)) + np.matmul(np.transpose(moments),np.matmul(W,grad))

    return gmm_grad

### Translate moment gradients and hessian in to GMM objective function gradients and hessian
def gmm_hessian(moments,grad,hess,W):
    gmm_hess = np.zeros((grad.shape[1],grad.shape[1]))
    for k in range(grad.shape[1]):
        gmm_hess[k,:] = np.matmul(np.transpose(hess[:,k,:]),np.matmul(W,moments)) + np.matmul(np.transpose(grad),np.matmul(W,grad[:,k]))+np.matmul(np.transpose(moments),np.matmul(W,hess[:,k,:]))+np.matmul(np.transpose(grad[:,k]),np.matmul(W,grad))

    return gmm_hess

### Evaluate GMM Objective function based on data and parameter vector
def compute_gmm(data,par,W):
    # Cost moments
    moments_cost = cp.pred_exp_moments(data,par)
    total_val = gmm_objective(moments_cost,W)

    # # IV moments
    # moments_iv = iv.IV_moments(df,p)
    # moments = np.concatenate((moments_iv,moments_cost),axis=0)

    ## Temporary Monitoring
    # total_val = gmm_objective(moments,W)
    # # IV Moment Component
    # idx = list(range(len(moments_iv)))
    # IV_comp = np.matmul(np.transpose(moments_iv),np.matmul(W[np.ix_(idx,idx)],moments_iv))
    # cost_comp = total_val - IV_comp
    # print('IV component is',"{:.5g}".format(IV_comp),'and cost component is',"{:.5g}".format(cost_comp))
    # # moments = iv.deposit_IV_moments(df,p)
    return total_val

def compute_gmm_gradient(data,par,W):

    moments_cost,grad_cost = cp.gradient_pred_exp(data,par)
    # moments_iv = iv.IV_moments(df,p)
    # grad_iv, hess_iv = iv.IV_mom_derivatives(df,p)
    # moments = np.concatenate((moments_iv,moments_cost),axis=0)
    # grad = np.concatenate((grad_iv,grad_cost),axis=0)

    # moments = iv.deposit_IV_moments(df,p)
    # grad, hess = iv.dep_IV_mom_derivatives(df,p)

    grad = gmm_gradient(moments_cost,grad_cost,W)
    return grad

def compute_gmm_hessian(data,par,W):
    moments_cost,grad_cost,hess_cost = cp.hessian_pred_exp(data,par)
    # moments_iv = iv.IV_moments(df,p)
    # grad_iv, hess_iv = iv.IV_mom_derivatives(df,p)
    # #
    # moments = np.concatenate((moments_iv,moments_cost),axis=0)
    # grad = np.concatenate((grad_iv,grad_cost),axis=0)
    # hess = np.concatenate((hess_iv,hess_cost),axis=0)

    # moments = iv.deposit_IV_moments(df,p)
    # grad, hess = iv.dep_IV_mom_derivatives(df,p)

    f = gmm_objective(moments_cost,W)
    G = gmm_gradient(moments_cost,grad_cost,W)
    H = gmm_hessian(moments_cost,grad_cost,hess_cost,W)
    return f, G, H

## Numerical Derivative test functions
def numerical_gradient(data,par,W):
    tol =1e-6
    grad = np.zeros(len(par.param_vec))
    orig = compute_gmm(data,par,W)
    orig_vec = par.param_vec.copy()

    for i in range(len(par.param_vec)):
        update_vec = np.zeros(len(par.param_vec))
        update_vec[i]+=tol
        par.update(update_vec)
        new_val = compute_gmm(data,par,W)
        grad[i] = (new_val-orig)/tol
        par.set(orig_vec)
    return grad

def numerical_hessian(data,par,W):
    tol = 1e-6
    hess = np.zeros((len(par.param_vec),len(par.param_vec)))
    orig = compute_gmm_gradient(data,par,W)
    orig_vec = par.param_vec.copy()

    for i in range(len(par.param_vec)):
        update_vec = np.zeros(len(par.param_vec))
        update_vec[i]+=tol
        par.update(update_vec)
        new_val = compute_gmm_gradient(data,par,W)
        hess[i,] = (new_val-orig)/tol
        par.set(orig_vec)
    return hess
