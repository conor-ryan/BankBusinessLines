import numpy as np
import GMM as gmm

def newton_raphson(data,par,W,ftol=1e-3):
    p_idx = list(range(len(par.param_vec)))
    # p_idx.extend(range(9,len(p0)))
    capped_params_idx = list(range(len(par.param_vec)))
    # p_idx = list(range(len(p0)))
    # capped_params_idx = list(range(0,9))
    # print(p0[capped_params_idx])
    # print(capped_params_idx)
    ### Print Format
    np.set_printoptions(precision=4)
    ### Initial Evaluation
    fval, G, H = gmm.compute_gmm_hessian(data,par,W)

    G = G[p_idx]
    H = H[np.ix_(p_idx,p_idx)]

    print('Function value at starting parameter:',"{:.8g}".format(fval))
    # print('Gradient value at starting parameter:',G)
    # print('hessian value at starting parameter:',H)

    grad_size = np.sqrt(np.dot(G,G))

    itr=0

    while grad_size>ftol:
        ## Current Parameter Vector
        param_cur = par.param_vec.copy()
        ## Candidate New Parameter Vector (Updated)
        param_new = par.param_vec.copy()
        ## Find NR step and new parameter vector
        if len(p_idx)>1:
            step = -np.matmul(G,np.linalg.inv(H))
        else:
            step = -G/H

        # Cap step change at half of parameters estimate.
        # This should effectively stop the affected parameters from changing sign
        check_cap = [(abs(step[x])/param_cur[x])<0.5 or abs(step[x])<0.25 for x in capped_params_idx]
        if False in check_cap:
            # print(step[capped_params_idx])
            cap = max(abs(step[capped_params_idx])/param_cur[capped_params_idx])
            step = step/cap*0.5
            # print(step[capped_params_idx])
            print('Hit step cap of 50% parameter value on non_linear_parameters')


        param_new[p_idx] = param_cur[p_idx] + step
        # print('Newton Raphson Step: ',step)
        ## Make an attempt to be descending
        par.set(param_new)
        print('Now trying parameter vector', par.param_vec)
        new_fval = gmm.compute_gmm(data,par,W)

        # alpha = abs(1/np.diag(H))
        # while new_fval>fval*(1+1e-5):
        #     step = -G*alpha
        #     cap = max(abs(step[capped_params_idx])/param_cur[capped_params_idx])
        #     if cap>0.5:
        #         step = step/cap*0.5
        #         print('Hit step cap of 50% parameter value on non_linear_parameters')
        #
        #     # print("New value","{:.3g}".format(new_fval),"exceeds old value","{:.3g}".format(fval),"by too much")
        #     # print("Step along the gradient:",step)
        #     print("Gradient step")
        #     param_new[p_idx] = param_cur[p_idx] + step
        #     par.set(param_new)
        #     print('Now trying parameter vector', par.param_vec)
        #     new_fval = gmm.compute_gmm(data,par,W)
        #     alpha = alpha/10

        # Final Parameter Update
        par.set(param_cur)
        par.update(step)

        # Evaluation for next iteration
        fval, G, H = gmm.compute_gmm_hessian(data,par,W)

        ## Allow for estiamtion to finish even if it's not well identified
        check_unidentified = [x for x in capped_params_idx if (param_cur[x]>1e7) or (param_cur[x]<-1e7) ]
        if len(check_unidentified)>0:
            print('Parameters running off to infinity: ', check_unidentified)
        G[check_unidentified] = 0


        G = G[p_idx]
        H = H[np.ix_(p_idx,p_idx)]
        grad_size = np.sqrt(np.dot(G,G))
        itr+=1
        # Print Status Report
        print('Function value is',"{:.8g}".format(fval),'and gradient is',"{:.3g}".format(grad_size),'on iteration number',itr)

    print('Solution!', par.param_vec)
    print('Function value is ',"{:.8g}".format(fval),'and gradient is',"{:.3g}".format(grad_size),'after',itr,'iterations')
    return
