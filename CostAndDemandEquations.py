def cost_residual(data,par):
    X = data[:,par.data_cost_indvar]
    Y = data[:,par.data_cost_depvar]
    β = par.param_vec[par.par_cost_index]
    ω = Y - np.matmul(X,β)
    return ω

def cost_residual_gradient(data,par):
    G = -data[:,par.data_cost_indvar]
    return G
