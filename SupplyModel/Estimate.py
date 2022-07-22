import numpy as np
import GMM as gmm

def newton_raphson(data,par,W,ftol=1e-3,valtol=1e-4,itr_max=2000):
    p0 = par.param_vec
    p_idx = list(range(len(p0))) #In case we want to fix some parameters, currently estimating all

    ### Print Format
    np.set_printoptions(precision=4)

    ### Initial Evaluation
    fval, G, H = gmm.compute_gmm_hessian(data,par,W)

    G = G[p_idx]
    H = H[np.ix_(p_idx,p_idx)]

    print('Function value at starting parameter:',"{:.8g}".format(fval))
    # print('Gradient value at starting parameter:',G)
    # print('hessian value at starting parameter:',H)

    # Norm for convergence tolerance
    grad_size = np.sqrt(np.dot(G,G))

    itr=0

    while (grad_size>ftol) & (fval>valtol) & (itr<itr_max):
        itr+=1
        if itr%200==0:
            deviation = np.random.rand(len(par.param_vec))*0.01 - 0.005
            par.update(deviation)
            print("Random Deviation Step")
            # Evaluation for next iteration
            fval, G, H = gmm.compute_gmm_hessian(data,par,W)

            ## New derivatives
            G = G[p_idx]
            H = H[np.ix_(p_idx,p_idx)]
            grad_size = np.sqrt(np.dot(G,G))
            # Print Status Report
            print('Function value is',"{:.8g}".format(fval),'and gradient size is',"{:.3g}".format(grad_size),'on iteration number',itr)


            continue

        ## Current Parameter Vector
        param_cur = par.param_vec.copy()
        ## Candidate New Parameter Vector (Updated)
        param_new = par.param_vec.copy()
        ## Find NR step and new parameter vector
        if len(p_idx)>1:
            step = -np.matmul(G,np.linalg.inv(H))
        else:
            step = -G/H

        # Cap step size
        # cap_size = 10000
        # check_cap = [abs(step[x])<cap_size for x in p_idx]
        # if False in check_cap:
        #     cap = max(abs(step[p_idx]))
        #     step = step/cap*cap_size
        #     # print(step[capped_params_idx])
        #     print('Hit step cap of ', cap_size)


        ## Candidate Update Vector
        param_new[p_idx] = param_cur[p_idx] + step
        par.set(param_new)
        # print('Now trying parameter vector', par.param_vec)
        # print('Step is ', step)

        ## Evaluate Function at new parameter vector
        new_fval = gmm.compute_gmm(data,par,W)

        ## If the function is not minimizing, update the parameter with a gradient step
        ## Do this anyway if the gradient is really large

        step_tol = 1.10
        if grad_size>1e5:
            print("Gradient Too Large")
            new_fval = fval*100
            alpha = abs(1/np.diag(H))
            step = -G*alpha

            step_tol = 1.00

        reduction_itr= 0
        while (new_fval>fval*step_tol):
            reduction_itr +=1
            if reduction_itr==4:
                step_tol = 1.00
                alpha = abs(1/np.diag(H))
                step = -G*alpha
                print("Switch to Gradient")
            step = step/10
            # cap = max(abs(step[capped_params_idx])/param_cur[capped_params_idx])
            # if cap>0.5:
            #     step = step/cap*0.5
            #     print('Hit step cap of 50% parameter value on non_linear_parameters')

            # print("New value","{:.3g}".format(new_fval),"exceeds old value","{:.3g}".format(fval),"by too much")
            # print("Step along the gradient:",step)
            print("Reduced step")
            ## Candidate Update Vector
            param_new[p_idx] = param_cur[p_idx] + step
            par.set(param_new)
            # print('Now trying parameter vector', par.param_vec)
            # print('Step is ', step)
            ## Evaluate Function at new parameter vector
            new_fval = gmm.compute_gmm(data,par,W)

            ## If still not moving in right direction, smaller gradient step
            #alpha = alpha/10

        # Final Parameter Update
        par.set(param_cur)
        par.update(step)

        # Evaluation for next iteration
        fval, G, H = gmm.compute_gmm_hessian(data,par,W)

        ## Allow for estiamtion to finish even if it's not well identified
        check_unidentified = [x for x in p_idx if (param_cur[x]>1e7) or (param_cur[x]<-1e7) ]
        if len(check_unidentified)>0:
            print('Parameters running off to infinity: ', check_unidentified)
        G[check_unidentified] = 0

        ## New derivatives
        G = G[p_idx]
        H = H[np.ix_(p_idx,p_idx)]
        grad_size = np.sqrt(np.dot(G,G))
        # Print Status Report
        print('Function value is',"{:.8g}".format(fval),'and gradient size is',"{:.3g}".format(grad_size),'on iteration number',itr)

    print('Solution!', par.param_vec)
    print('Function value is ',"{:.8g}".format(fval),'and gradient is',"{:.3g}".format(grad_size),'after',itr,'iterations')
    return
