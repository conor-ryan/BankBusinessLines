import ProfitFunctions as pf
import DemandIV as iv
import numpy as np
import pandas as pd

class Parameter:
    e = 0.95

    def __init__(self,vec,X,Z):
        ## Parameters for Firm Problem
        self.alpha_dep = vec[0]
        self.alpha_cons= vec[1]
        self.alpha_comm= vec[2]
        self.alpha_inv= vec[3]
        self.alpha_ins= vec[4]

        self.gamma_cons= vec[5]
        self.gamma_comm= vec[6]
        self.gamma_inv= vec[7]
        self.gamma_ins= vec[8]

        ## Hard code these indices for now, but can relax
        self.parnum = 9 + X.shape[1]
        self.dep_index = 0
        self.foc_pars = 9
        self.beta_index = list(range(9,(9+X.shape[1])))

        ## Variables for Demand Deposit IV Estimation
        ## Annihilator matrix for exogenous covariates in demand equation
        # self.M = M
        ## Instruments
        self.Z = Z
        ## Exogenous Covariates
        self.X = X
        self.beta = vec[self.beta_index]


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


def simulate(df,parameters,X,Z):
    par = Parameter(parameters,X,Z)
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

def predict(df,parameters,X,Z):
    par = Parameter(parameters,X,Z)
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



    return moments,grad,hess

# For now, write for a identity weighting matrix
# This is much faster, but we will have to generalize for two-step GMM
def gmm_objective(moments,W):
    return np.matmul(np.transpose(moments),np.matmul(W,moments))

def gmm_gradient(moments,grad,W):
    gmm_grad = np.zeros(grad.shape[1])
    # for i in range(len(moments)):
    #     for j in range(grad.shape[1]):
    #         gmm_grad[j]+= 2*moments[i]*grad[i,j]

    gmm_grad = np.matmul(np.transpose(grad),np.matmul(W,moments)) + np.matmul(np.transpose(moments),np.matmul(W,grad))

    return gmm_grad

def gmm_hessian(moments,grad,hess,W):
    gmm_hess = np.zeros((grad.shape[1],grad.shape[1]))
    # for i in range(len(moments)):
    #     for j in range(len(moments)):
    #         for k in range(grad.shape[1]):
    #             for l in range(k+1):
    #                 gmm_hess[k,l]+= W[i,j]*(moments[i]*hess[j,k,l] + moments[j]*hess[i,k,l] + grad[i,k]*grad[j,l] + grad[i,l]*grad[j,k])
    #                 if k!=l:
    #                     gmm_hess[l,k]+= gmm_hess[k,l]
    for k in range(grad.shape[1]):
        gmm_hess[k,:] = np.matmul(np.transpose(hess[:,k,:]),np.matmul(W,moments)) + np.matmul(np.transpose(grad),np.matmul(W,grad[:,k]))+np.matmul(np.transpose(moments),np.matmul(W,hess[:,k,:]))+np.matmul(np.transpose(grad[:,k]),np.matmul(W,grad))

    return gmm_hess

### Evaluate based on data and parameter vector
def compute_gmm(df,X,Z,vec,W):
    p = Parameter(vec,X,Z)
    moments_cost = calc_cost_moments(df,p)
    moments_iv = iv.deposit_IV_moments(df,p)
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

def compute_gmm_gradient(df,X,Z,vec,W):
    p = Parameter(vec,X,Z)

    moments_cost,grad_cost,hess_cost = calc_cost_moments_withderivatives(df,p)
    moments_iv = iv.deposit_IV_moments(df,p)
    grad_iv, hess_iv = iv.dep_IV_mom_derivatives(df,p)

    moments = np.concatenate((moments_iv,moments_cost),axis=0)
    grad = np.concatenate((grad_iv,grad_cost),axis=0)

    # moments = iv.deposit_IV_moments(df,p)
    # grad, hess = iv.dep_IV_mom_derivatives(df,p)

    grad = gmm_gradient(moments,grad,W)
    return grad

def compute_gmm_hessian(df,X,Z,vec,W):
    p = Parameter(vec,X,Z)
    moments_cost,grad_cost,hess_cost = calc_cost_moments_withderivatives(df,p)
    moments_iv = iv.deposit_IV_moments(df,p)
    grad_iv, hess_iv = iv.dep_IV_mom_derivatives(df,p)
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
def numerical_gradient(df,X,Z,vec,W):
    tol = 1e-6
    grad = np.zeros(len(vec))
    orig = compute_gmm(df,X,Z,vec,W)
    for i in range(len(vec)):
        new_vec = vec.copy()
        new_vec[i]+=tol
        new_val = compute_gmm(df,X,Z,new_vec,W)
        grad[i] = (new_val-orig)/1e-6
    return grad

def numerical_hessian(df,X,Z,vec,W):
    tol = 1e-6
    hess = np.zeros((len(vec),len(vec)))
    orig = compute_gmm_gradient(df,X,Z,vec,W)
    for i in range(len(vec)):
        new_vec = vec.copy()
        new_vec[i]+=tol
        new_val = compute_gmm_gradient(df,X,Z,new_vec,W)
        hess[i,] = (new_val-orig)/1e-6
    return hess
