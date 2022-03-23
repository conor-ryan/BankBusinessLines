import ProfitFunctions as pf
import DemandIV as iv
import numpy as np
import pandas as pd


#### Class Variable: the object we are going to estimate


class Parameter:
    e = 0.05
    dep_index = 0
    cons_index = 1
    comm_index = 2
    inv_index = 3
    ins_index = 4

    beta_dep_index = None
    beta_cons_index = None
    beta_comm_index = None
    beta_ins_index = None
    beta_inv_index = None
    rownum = 0

    def __init__(self,vec,X_dep=None,X_cons=None,X_comm=None,X_ins=None,X_inv=None,Z_dep = None,Z_cons=None,Z_comm=None,Z_ins=None,Z_inv=None):
        ## Parameters for Firm Problem
        self.alpha_dep = vec[self.dep_index]
        self.alpha_cons= vec[self.cons_index]
        self.alpha_comm= vec[self.comm_index]
        self.alpha_inv= vec[self.inv_index]
        self.alpha_ins= vec[self.ins_index]

        self.gamma_cons= vec[5]
        self.gamma_comm= vec[6]
        self.gamma_inv= vec[7]
        self.gamma_ins= vec[8]

        ## Compute total number of parameters, and parameter indices
        self.parnum = 9
        self.foc_pars = 9
        for x in [X_dep,X_cons,X_comm,X_ins,X_inv]:
            if x is not None:
                self.parnum += x.shape[1]

        index_start = 9
        if X_dep is not None:
            self.beta_dep_index = list(range(index_start,(index_start+X_dep.shape[1])))
            self.rownum = X_dep.shape[0]
            index_start += X_dep.shape[1]
        if X_cons is not None:
            self.beta_cons_index = list(range(index_start,(index_start+X_cons.shape[1])))
            self.rownum = X_cons.shape[0]
            index_start += X_cons.shape[1]
        if X_comm is not None:
            self.beta_comm_index = list(range(index_start,(index_start+X_comm.shape[1])))
            self.rownum = X_comm.shape[0]
            index_start += X_comm.shape[1]
        if X_ins is not None:
            self.beta_ins_index = list(range(index_start,(index_start+X_ins.shape[1])))
            self.rownum = X_ins.shape[0]
            index_start += X_ins.shape[1]
        if X_inv is not None:
            self.beta_inv_index = list(range(index_start,(index_start+X_inv.shape[1])))
            self.rownum = X_inv.shape[0]
            index_start += X_inv.shape[1]


        ## Variables for Demand Deposit IV Estimation
        ## Annihilator matrix for exogenous covariates in demand equation
        # self.M = M
        ## Demand Instrument Variables
        self.Z_dep = Z_dep
        self.X_dep = X_dep
        if X_dep is not None:
            self.beta_dep = vec[self.beta_dep_index]

        self.Z_cons = Z_cons
        self.X_cons = X_cons
        if X_cons is not None:
            self.beta_cons = vec[self.beta_cons_index]

        self.Z_comm = Z_comm
        self.X_comm = X_comm
        if X_comm is not None:
            self.beta_comm = vec[self.beta_comm_index]

        self.Z_ins = Z_ins
        self.X_ins = X_ins
        if X_ins is not None:
            self.beta_ins = vec[self.beta_ins_index]

        self.Z_inv = Z_inv
        self.X_inv = X_inv
        if X_inv is not None:
            self.beta_inv = vec[self.beta_inv_index]


## Cost Moments
# This function takes the data frame and parameter candidate as an input
# Then applies the relevant functions to predict total cost
# It outputs the cost moments: predicted cost - total cost
def calc_cost_moments(df,par):
    # Marginal Cost Estimate
    mc_results = df.apply(lambda x: pf.implied_marginal_cost(x.r_dep,x.r_cons,x.r_comm,x.p_inv,x.p_ins,
                                                x.s_dep,x.s_cons,x.s_comm,x.s_inv,x.s_ins,par),result_type="expand",axis=1)
    mc_results.columns = ["mc_cons", "mc_comm", "mc_inv", "mc_ins"]

    # Total Cost Estimate
    df_cost = pd.concat([mc_results,df[["q_cons","q_comm","q_inv","q_ins","L_cons","L_comm","r_dep","q_dep"]]],axis="columns")
    total_cost = df_cost.apply(lambda x: pf.total_cost(x.L_cons,x.L_comm,x.r_dep,x.q_dep,
                                                x.q_cons,x.q_comm,x.q_inv,x.q_ins,
                                                x.mc_cons,x.mc_comm,x.mc_inv,x.mc_ins,par),result_type="expand",axis=1)

    # ### This line only for testing ####
    # df_cost['cost_pred'] = total_cost
    # df_cost['cost_obs'] = df['total_cost']
    # df_cost.to_csv('Data/test.csv')

    return (total_cost- df['total_cost']).to_numpy()


def simulate(df,parameters,X_dep=None,X_cons=None,X_comm=None,X_ins=None,X_inv=None,Z_dep = None,Z_cons=None,Z_comm=None,Z_ins=None,Z_inv=None):
    par = Parameter(parameters,X_dep=X_dep,X_cons=X_cons,X_comm=X_comm,X_ins=X_ins,X_inv=X_inv,Z_dep = Z_dep,Z_cons=Z_cons,Z_comm=Z_comm,Z_ins=Z_ins,Z_inv=Z_inv)
    # Marginal Cost Estimate
    mc_results = df.apply(lambda x: pf.implied_marginal_cost(x.r_dep,x.r_cons,x.r_comm,x.p_inv,x.p_ins,
                                                x.s_dep,x.s_cons,x.s_comm,x.s_inv,x.s_ins,par),result_type="expand",axis=1)
    mc_results.columns = ["mc_cons", "mc_comm", "mc_inv", "mc_ins"]

    # Total Cost Estimate
    df_cost = pd.concat([mc_results,df],axis="columns")
    total_cost = df_cost.apply(lambda x: pf.total_cost(x.L_cons,x.L_comm,x.r_dep,x.q_dep,
                                                x.q_cons,x.q_comm,x.q_inv,x.q_ins,
                                                x.mc_cons,x.mc_comm,x.mc_inv,x.mc_ins,par),result_type="expand",axis=1)
    df['total_cost'] = total_cost
    return df

def predict(df,parameters,X_dep=None,X_cons=None,X_comm=None,X_ins=None,X_inv=None,Z_dep = None,Z_cons=None,Z_comm=None,Z_ins=None,Z_inv=None):
    par = Parameter(parameters,X_dep=X_dep,X_cons=X_cons,X_comm=X_comm,X_ins=X_ins,X_inv=X_inv,Z_dep = Z_dep,Z_cons=Z_cons,Z_comm=Z_comm,Z_ins=Z_ins,Z_inv=Z_inv)
    # Marginal Cost Estimate
    mc_results = df.apply(lambda x: pf.implied_marginal_cost(x.r_dep,x.r_cons,x.r_comm,x.p_inv,x.p_ins,
                                                x.s_dep,x.s_cons,x.s_comm,x.s_inv,x.s_ins,par),result_type="expand",axis=1)
    mc_results.columns = ["mc_cons", "mc_comm", "mc_inv", "mc_ins"]

    mkup_results = df.apply(lambda x: pf.markups(x.r_dep,x.r_cons,x.r_comm,x.p_inv,x.p_ins,
                                                    x.s_dep,x.s_cons,x.s_comm,x.s_inv,x.s_ins,par),result_type="expand",axis=1)
    mkup_results.columns = ["mkup_dep","mkup_cons", "mkup_comm", "mkup_inv", "mkup_ins"]

    df = pd.concat([df,mc_results],axis="columns")
    df = pd.concat([df,mkup_results],axis="columns")
    # Total Cost Estimate

    total_cost = df.apply(lambda x: pf.total_cost(x.L_cons,x.L_comm,x.r_dep,x.q_dep,
                                                x.q_cons,x.q_comm,x.q_inv,x.q_ins,
                                                x.mc_cons,x.mc_comm,x.mc_inv,x.mc_ins,par),result_type="expand",axis=1)
    df['predicted_cost'] = total_cost
    return df


def calc_cost_moments_withderivatives(df,par):
    # Marginal Cost Estimate
    mc_results = df.apply(lambda x: pf.implied_marginal_cost(x.r_dep,x.r_cons,x.r_comm,x.p_inv,x.p_ins,
                                                x.s_dep,x.s_cons,x.s_comm,x.s_inv,x.s_ins,par),result_type="expand",axis=1)
    mc_results.columns = ["mc_cons", "mc_comm", "mc_inv", "mc_ins"]

    # Total Cost Estimate
    df_cost = pd.concat([mc_results,df],axis="columns")
    total_cost = df_cost.apply(lambda x: pf.total_cost(x.L_cons,x.L_comm,x.r_dep,x.q_dep,
                                                x.q_cons,x.q_comm,x.q_inv,x.q_ins,
                                                x.mc_cons,x.mc_comm,x.mc_inv,x.mc_ins,par),result_type="expand",axis=1)

    grad_temp = df_cost.apply(lambda x: pf.gradient_total_cost(x.L_cons,x.L_comm,
                                                    x.r_dep,x.r_cons,x.r_comm,x.p_inv,x.p_ins,
                                                    x.s_dep,x.s_cons,x.s_comm,x.s_inv,x.s_ins,
                                                    x.q_cons,x.q_comm,x.q_inv,x.q_ins,
                                                    x.mc_cons,x.mc_comm,x.mc_inv,x.mc_ins,par),result_type="expand",axis=1)

    hess_temp = df_cost.apply(lambda x: pf.hessian_total_cost(x.L_cons,x.L_comm,
                                                    x.r_dep,x.r_cons,x.r_comm,x.p_inv,x.p_ins,
                                                    x.s_dep,x.s_cons,x.s_comm,x.s_inv,x.s_ins,
                                                    x.q_cons,x.q_comm,x.q_inv,x.q_ins,
                                                    x.mc_cons,x.mc_comm,x.mc_inv,x.mc_ins,par),axis=1)

    ## Unpack hessian into 3-D array
    hess = np.zeros((grad_temp.shape[0],par.parnum,par.parnum))
    for i in range(grad_temp.shape[0]):
        hess[i,0:par.foc_pars,0:par.foc_pars] = hess_temp[i]
    grad = np.zeros((grad_temp.shape[0],par.parnum))
    grad[:,0:par.foc_pars] = grad_temp.to_numpy()

    moments = (total_cost- df['total_cost']).to_numpy()

    print("Total Market Costs:", sum(df['total_cost'])/1e6)
    print("Total Predicted Costs:", sum(total_cost)/1e6)





    return moments,grad,hess

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
def compute_gmm(df,vec,W,X_dep=None,X_cons=None,X_comm=None,X_ins=None,X_inv=None,Z_dep = None,Z_cons=None,Z_comm=None,Z_ins=None,Z_inv=None):
    p = Parameter(vec,X_dep=X_dep,X_cons=X_cons,X_comm=X_comm,X_ins=X_ins,X_inv=X_inv,Z_dep = Z_dep,Z_cons=Z_cons,Z_comm=Z_comm,Z_ins=Z_ins,Z_inv=Z_inv)
    # Cost moments
    moments_cost = calc_cost_moments(df,p)
    # IV moments
    moments_iv = iv.IV_moments(df,p)
    moments = np.concatenate((moments_iv,moments_cost),axis=0)

    ## Temporary Monitoring
    total_val = gmm_objective(moments,W)
    # IV Moment Component
    idx = list(range(len(moments_iv)))
    IV_comp = np.matmul(np.transpose(moments_iv),np.matmul(W[np.ix_(idx,idx)],moments_iv))
    cost_comp = total_val - IV_comp
    print('IV component is',"{:.5g}".format(IV_comp),'and cost component is',"{:.5g}".format(cost_comp))
    # moments = iv.deposit_IV_moments(df,p)
    return total_val

def compute_gmm_gradient(df,vec,W,X_dep=None,X_cons=None,X_comm=None,X_ins=None,X_inv=None,Z_dep = None,Z_cons=None,Z_comm=None,Z_ins=None,Z_inv=None):
    p = Parameter(vec,X_dep=X_dep,X_cons=X_cons,X_comm=X_comm,X_ins=X_ins,X_inv=X_inv,Z_dep = Z_dep,Z_cons=Z_cons,Z_comm=Z_comm,Z_ins=Z_ins,Z_inv=Z_inv)

    moments_cost,grad_cost,hess_cost = calc_cost_moments_withderivatives(df,p)
    moments_iv = iv.IV_moments(df,p)
    grad_iv, hess_iv = iv.IV_mom_derivatives(df,p)
    moments = np.concatenate((moments_iv,moments_cost),axis=0)
    grad = np.concatenate((grad_iv,grad_cost),axis=0)

    # moments = iv.deposit_IV_moments(df,p)
    # grad, hess = iv.dep_IV_mom_derivatives(df,p)

    grad = gmm_gradient(moments,grad,W)
    return grad

def compute_gmm_hessian(df,vec,W,X_dep=None,X_cons=None,X_comm=None,X_ins=None,X_inv=None,Z_dep = None,Z_cons=None,Z_comm=None,Z_ins=None,Z_inv=None):
    p = Parameter(vec,X_dep=X_dep,X_cons=X_cons,X_comm=X_comm,X_ins=X_ins,X_inv=X_inv,Z_dep = Z_dep,Z_cons=Z_cons,Z_comm=Z_comm,Z_ins=Z_ins,Z_inv=Z_inv)
    moments_cost,grad_cost,hess_cost = calc_cost_moments_withderivatives(df,p)
    moments_iv = iv.IV_moments(df,p)
    grad_iv, hess_iv = iv.IV_mom_derivatives(df,p)
    #
    moments = np.concatenate((moments_iv,moments_cost),axis=0)
    grad = np.concatenate((grad_iv,grad_cost),axis=0)
    hess = np.concatenate((hess_iv,hess_cost),axis=0)

    # moments = iv.deposit_IV_moments(df,p)
    # grad, hess = iv.dep_IV_mom_derivatives(df,p)

    f = gmm_objective(moments,W)
    G = gmm_gradient(moments,grad,W)
    H = gmm_hessian(moments,grad,hess,W)
    return f, G, H

## Numerical Derivative test functions
def numerical_gradient(df,vec,W,X_dep=None,X_cons=None,X_comm=None,X_ins=None,X_inv=None,Z_dep = None,Z_cons=None,Z_comm=None,Z_ins=None,Z_inv=None):
    tol =1e-6
    grad = np.zeros(len(vec))
    orig = compute_gmm(df,vec,W,X_dep=X_dep,X_cons=X_cons,X_comm=X_comm,X_ins=X_ins,X_inv=X_inv,Z_dep = Z_dep,Z_cons=Z_cons,Z_comm=Z_comm,Z_ins=Z_ins,Z_inv=Z_inv)
    for i in range(len(vec)):
        new_vec = vec.copy()
        new_vec[i]+=tol
        new_val = compute_gmm(df,new_vec,W,X_dep=X_dep,X_cons=X_cons,X_comm=X_comm,X_ins=X_ins,X_inv=X_inv,Z_dep = Z_dep,Z_cons=Z_cons,Z_comm=Z_comm,Z_ins=Z_ins,Z_inv=Z_inv)
        grad[i] = (new_val-orig)/tol
    return grad

def numerical_hessian(df,vec,W,X_dep=None,X_cons=None,X_comm=None,X_ins=None,X_inv=None,Z_dep = None,Z_cons=None,Z_comm=None,Z_ins=None,Z_inv=None):
    tol = 1e-6
    hess = np.zeros((len(vec),len(vec)))
    orig = compute_gmm_gradient(df,vec,W,X_dep=X_dep,X_cons=X_cons,X_comm=X_comm,X_ins=X_ins,X_inv=X_inv,Z_dep = Z_dep,Z_cons=Z_cons,Z_comm=Z_comm,Z_ins=Z_ins,Z_inv=Z_inv)
    for i in range(len(vec)):
        new_vec = vec.copy()
        new_vec[i]+=tol
        new_val = compute_gmm_gradient(df,new_vec,W,X_dep=X_dep,X_cons=X_cons,X_comm=X_comm,X_ins=X_ins,X_inv=X_inv,Z_dep = Z_dep,Z_cons=Z_cons,Z_comm=Z_comm,Z_ins=Z_ins,Z_inv=Z_inv)
        hess[i,] = (new_val-orig)/tol
    return hess
