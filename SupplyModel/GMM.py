import ProfitFunctions as pf
import numpy as np
import pandas as pd

class Parameter:
    # alpha_dep
    # alpha_cons
    # alpha_comm
    # alpha_ins
    # alpha_inv
    #
    # gamma_dep
    # gamma_cons
    # gamma_comm
    # gamma_ins
    # gamma_inv
    e = 0.8

    def __init__(self,vec):
        self.alpha_dep = vec[0]
        self.alpha_cons= vec[1]
        self.alpha_comm= vec[2]
        self.alpha_inv= vec[3]
        self.alpha_ins= vec[4]

        self.gamma_cons= vec[5]
        self.gamma_comm= vec[6]
        self.gamma_inv= vec[7]
        self.gamma_ins= vec[8]
        #
        # self.gamma_cons= 0.8
        # self.gamma_comm= 0.8
        # self.gamma_inv= 0.8
        # self.gamma_ins= 0.8





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
    df_cost = pd.concat([mc_results,df[["q_cons","q_comm","q_inv","q_ins"]]],axis="columns")
    total_cost = df_cost.apply(lambda x: pf.total_cost(x.q_cons,x.q_comm,x.q_inv,x.q_ins,
                                                x.mc_cons,x.mc_comm,x.mc_inv,x.mc_ins,par),result_type="expand",axis=1)

    # ### This line only for testing ####
    # df_cost['cost_pred'] = total_cost
    # df_cost['cost_obs'] = df['total_cost']
    # df_cost.to_csv('Data/test.csv')

    return (total_cost- df['total_cost']).to_numpy()


def simulate(df,parameters):
    par = Parameter(parameters)
    # Marginal Cost Estimate
    mc_results = df.apply(lambda x: pf.implied_marginal_cost(x.r_dep,x.r_cons,x.r_comm,x.p_inv,x.p_ins,
                                                x.s_dep,x.s_cons,x.s_comm,x.s_inv,x.s_ins,par),result_type="expand",axis=1)
    mc_results.columns = ["mc_cons", "mc_comm", "mc_inv", "mc_ins"]

    # Total Cost Estimate
    df_cost = pd.concat([mc_results,df[["q_cons","q_comm","q_inv","q_ins"]]],axis="columns")
    total_cost = df_cost.apply(lambda x: pf.total_cost(x.q_cons,x.q_comm,x.q_inv,x.q_ins,
                                                x.mc_cons,x.mc_comm,x.mc_inv,x.mc_ins,par),result_type="expand",axis=1)
    df['total_cost'] = total_cost
    return df


def calc_cost_moments_withderivatives(df,par):
    # Marginal Cost Estimate
    mc_results = df.apply(lambda x: pf.implied_marginal_cost(x.r_dep,x.r_cons,x.r_comm,x.p_inv,x.p_ins,
                                                x.s_dep,x.s_cons,x.s_comm,x.s_inv,x.s_ins,par),result_type="expand",axis=1)
    mc_results.columns = ["mc_cons", "mc_comm", "mc_inv", "mc_ins"]

    # Total Cost Estimate
    df_cost = pd.concat([mc_results,df],axis="columns")
    total_cost = df_cost.apply(lambda x: pf.total_cost(x.q_cons,x.q_comm,x.q_inv,x.q_ins,
                                                x.mc_cons,x.mc_comm,x.mc_inv,x.mc_ins,par),result_type="expand",axis=1)

    grad = df_cost.apply(lambda x: pf.gradient_total_cost(x.r_dep,x.r_cons,x.r_comm,x.p_inv,x.p_ins,
                                                    x.s_dep,x.s_cons,x.s_comm,x.s_inv,x.s_ins,
                                                    x.q_cons,x.q_comm,x.q_inv,x.q_ins,
                                                    x.mc_cons,x.mc_comm,x.mc_inv,x.mc_ins,par),result_type="expand",axis=1)

    hess = df_cost.apply(lambda x: pf.hessian_total_cost(x.r_dep,x.r_cons,x.r_comm,x.p_inv,x.p_ins,
                                                    x.s_dep,x.s_cons,x.s_comm,x.s_inv,x.s_ins,
                                                    x.q_cons,x.q_comm,x.q_inv,x.q_ins,
                                                    x.mc_cons,x.mc_comm,x.mc_inv,x.mc_ins,par),axis=1)

    moments = (total_cost- df['total_cost']).to_numpy()



    return moments,grad.to_numpy(),hess.to_numpy()

# For now, write for a identity weighting matrix
# This is much faster, but we will have to generalize for two-step GMM
def gmm_objective(moments):
    return np.sum(np.square(moments/1e6))

def gmm_gradient(moments,grad):
    gmm_grad = np.zeros(grad.shape[1])
    for i in range(len(moments)):
        for j in range(grad.shape[1]):
            gmm_grad[j]+= 2*moments[i]*grad[i,j]

    return gmm_grad/(1e6)**2

def gmm_hessian(moments,grad,hess):
    gmm_hess = np.zeros((grad.shape[1],grad.shape[1]))
    for i in range(len(moments)):
        for j in range(grad.shape[1]):
            for k in range(j+1):
                gmm_hess[j,k]+= 2*(moments[i]*hess[i][j,k] + grad[i,j]*grad[i,k])
                if k!=j:
                    gmm_hess[k,j]+= 2*(moments[i]*hess[i][j,k] + grad[i,j]*grad[i,k])

    return gmm_hess/(1e6)**2

### Evaluate based on data and parameter vector
def compute_gmm(df,vec):
    p = Parameter(vec)
    moments = calc_cost_moments(df,p)
    return gmm_objective(moments)

def compute_gmm_gradient(df,vec):
    p = Parameter(vec)
    moments,grad,hess = calc_cost_moments_withderivatives(df,p)
    return gmm_gradient(moments,grad)

def compute_gmm_hessian(df,vec):
    p = Parameter(vec)
    moments,grad,hess = calc_cost_moments_withderivatives(df,p)
    f = gmm_objective(moments)
    G = gmm_gradient(moments,grad)
    H = gmm_hessian(moments,grad,hess)
    return f, G, H

## Numerical Derivative test functions
def numerical_gradient(df,vec):
    tol = 1e-6
    grad = np.zeros(len(vec))
    orig = compute_gmm(df,vec)
    for i in range(len(vec)):
        new_vec = vec.copy()
        new_vec[i]+=tol
        new_val = compute_gmm(df,new_vec)
        grad[i] = (new_val-orig)/1e-6
    return grad

def numerical_hessian(df,vec):
    tol = 1e-6
    hess = np.zeros((len(vec),len(vec)))
    orig = compute_gmm_gradient(df,vec)
    for i in range(len(vec)):
        new_vec = vec.copy()
        new_vec[i]+=tol
        new_val = compute_gmm_gradient(df,new_vec)
        hess[i,] = (new_val-orig)/1e-6
    return hess
