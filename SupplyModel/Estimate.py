import numpy as np
import GMM as gmm

def newton_raphson(df,X,Z,p0,W,ftol=1e-8):
    p_idx = list(range(0,5))
    p_idx.extend(range(9,len(p0)))
    capped_params_idx = list(range(0,5))
    # p_idx = list(range(len(p0)))
    # capped_params_idx = list(range(0,9))
    print(p0[capped_params_idx])
    # print(capped_params_idx)
    ### Print Format
    np.set_printoptions(precision=8)
    ### Initial Evaluation
    fval, G, H = gmm.compute_gmm_hessian(df,X,Z,p0,W)

    G = G[p_idx]
    H = H[np.ix_(p_idx,p_idx)]

    print('Function value at starting parameter:',"{:.8g}".format(fval))
    print('Gradient value at starting parameter:',G)
    print('hessian value at starting parameter:',H)

    grad_size = np.sqrt(np.dot(G,G))
    param_vec = p0.copy()
    param_new = p0.copy()
    itr=0

    while grad_size>ftol:
        ## Find NR step and new parameter vector
        if len(p_idx)>1:
            step = -np.matmul(G,np.linalg.inv(H))
        else:
            step = -G/H

        # Cap step change at half of parameters estimate.
        # This should effectively stop the affected parameters from changing sign
        check_cap = [(abs(step[x])/param_vec[x])<0.5 or step[x]<1.0 for x in capped_params_idx]
        if False in check_cap:
            cap = max(abs(step[capped_params_idx])/param_vec[capped_params_idx])
            step = step/cap*0.5
            print('Hit step cap of 50% parameter value on non_linear_parameters')


        param_new[p_idx] = param_vec[p_idx] + step
        print('Now trying parameter vector', param_vec[0:9])
        # print('Newton Raphson Step: ',step)
        ## Make an attempt to be descending
        new_fval = gmm.compute_gmm(df,X,Z,param_new,W)
        alpha = abs(1/np.diag(H))
        while new_fval>fval*(1+1e-5):
            step = -G*alpha
            cap = max(abs(step[capped_params_idx])/param_vec[capped_params_idx])
            if cap>0.5:
                step = step/cap*0.5
                print('Hit step cap of 50% parameter value on non_linear_parameters')

            # print("New value","{:.3g}".format(new_fval),"exceeds old value","{:.3g}".format(fval),"by too much")
            # print("Step along the gradient:",step)
            print("Gradient step")
            param_new[p_idx] = param_vec[p_idx] + step
            print('Now trying parameter vector', param_vec[0:9])
            new_fval = gmm.compute_gmm(df,X,Z,param_new,W)
            alpha = alpha/10

        param_vec[p_idx] = param_vec[p_idx] + step

        # Evaluation for next iteration
        fval, G, H = gmm.compute_gmm_hessian(df,X,Z,param_vec,W)

        ## Allow for estiamtion to finish even if it's not well identified
        check_unidentified = [x for x in capped_params_idx if (param_vec[x]>1e7) or (param_vec[x]<-1e7) ]
        print(check_unidentified)
        G[check_unidentified] = 0


        G = G[p_idx]
        H = H[np.ix_(p_idx,p_idx)]
        grad_size = np.sqrt(np.dot(G,G))
        itr+=1
        # Print Status Report
        print('Function value is',"{:.8g}".format(fval),'and gradient is',"{:.3g}".format(grad_size),'on iteration number',itr)

    print('Solution!', param_vec)
    print('Function value is ',"{:.8g}".format(fval),'and gradient is',"{:.3g}".format(grad_size),'after',itr,'iterations')
    return param_vec
