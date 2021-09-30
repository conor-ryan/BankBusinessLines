import numpy as np
import GMM as gmm

def newton_raphson(df,p0,ftol=1e-8):
    ### Print Format
    np.set_printoptions(precision=2)
    ### Initial Evaluation
    fval, G, H = gmm.compute_gmm_hessian(df,p0)
    print('Function value at starting parameter:',"{:.3g}".format(fval))
    # G = G[0:5]
    # H = H[0:5,0:5]
    grad_size = np.sqrt(np.dot(G,G))
    param_vec = p0.copy()
    itr=0

    while grad_size>ftol:
        ## Find NR step and new parameter vector
        step = -np.matmul(G,np.linalg.inv(H))

        # Cap step change at half of parameters estimate.
        # This should effectively stop the affected parameters from changing sign
        cap = max(abs(step[5:9])/param_vec[5:9])
        if cap>0.5:
            step = step/cap*0.5
            print('Hit cap on gamma, new step',step)

        param_new = param_vec + step

        print('Newton Raphson Step: ',step)
        ## Make an attempt to be descending
        new_fval = gmm.compute_gmm(df,param_new)
        alpha = abs(1/np.diag(H))
        while new_fval>fval:
            step = -G*alpha
            cap = max(abs(step[5:9])/param_vec[5:9])
            if cap>0.5:
                step = step/cap*0.5
                print('Hit cap on gamma, new step',step)

            # print("New value","{:.3g}".format(new_fval),"exceeds old value","{:.3g}".format(fval),"by too much")
            print("Step along the gradient:",step)
            param_new = param_vec + step
            new_fval = gmm.compute_gmm(df,param_new)
            alpha = alpha/10

        param_vec = param_vec + step

        # Evaluation for next iteration
        fval, G, H = gmm.compute_gmm_hessian(df,param_vec)
        # G = G[0:5]
        # H = H[0:5,0:5]
        grad_size = np.sqrt(np.dot(G,G))
        itr+=1
        # Print Status Report
        print('Function value is',"{:.3g}".format(fval),'and gradient is',"{:.3g}".format(grad_size),'on iteration number',itr)
        print('Now trying parameter vector', param_vec)

    print('Solution!', param_vec)
    print('Function value is ',"{:.3g}".format(fval),'and gradient is',"{:.3g}".format(grad_size),'after',itr,'iterations')
    return param_vec
