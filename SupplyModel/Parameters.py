# import ProfitFunctions as pf
import LinearModel as iv
import GMM as gmm
import numpy as np
import pandas as pd


#### Class Variable: the object we are going to estimate
class Parameter:
    # par_dep_index = 0
    # par_prod_index = [1,2,3,4]
    # par_cost_index = [5,6,7,8,9]

    def __init__(self,df,dem_spec_list,cost_spec):
        # Convert data to matrix
        data = df.to_numpy()
        # Save Variable Label Names
        self.dem_spec_label_list = dem_spec_list
        self.cost_spec_label = cost_spec
        # Number of demand specs
        K = len(dem_spec_list)
        #Initialize
        self.dem_spec_list = list()
        p_len_tot = 0

        # Create data and parameter indices for each demand specification
        for k in range(K):
            spec_dict = dict()
            #Dependent variable
            spec_dict['dep_var'] = [i for i, val in enumerate(df.columns) if val==dem_spec_list[k]['dep_var'] ][0]
            #Independent variables
            spec_dict['ind_var'] = [i for i, val in enumerate(df.columns) if val in dem_spec_list[k]['ind_var'] ]
            #Instruments
            spec_dict['inst_var'] = [i for i, val in enumerate(df.columns) if val in dem_spec_list[k]['inst_var'] ]
            #Flag for valid observations
            flag_ind = [i for i, val in enumerate(df.columns) if val==dem_spec_list[k]['flag_var'] ][0]
            spec_dict['index'] = data[:,flag_ind] == 0
            #Index for relevant parameters
            p_len_new = len(spec_dict['ind_var'])
            spec_dict['param'] = np.arange(p_len_tot,p_len_tot+p_len_new)
            p_len_tot = p_len_tot + p_len_new
            #Append specification
            self.dem_spec_list.append(spec_dict)

        # Create data and parameter indices for cost specification
        self.cost_spec = dict()
        #Dependent variable
        self.cost_spec['dep_var'] = [i for i, val in enumerate(df.columns) if val==cost_spec['dep_var'] ][0]
        #Independent variables - endogenous
        self.cost_spec['ind_var_endo'] = [i for i, val in enumerate(df.columns) if val in cost_spec['ind_var_endo'] ]
        #Independent variables - exogenous
        self.cost_spec['ind_var_exo'] = [i for i, val in enumerate(df.columns) if val in cost_spec['ind_var_exo'] ]
        #Flag for valid observations - dummy vector of always true
        self.cost_spec['index'] = np.repeat(True,df.shape[0])
        #Index for relevant parameters
        #Endogenous
        p_len_new = len(cost_spec['ind_var_endo'])
        self.cost_spec['param_endo'] = np.arange(p_len_tot,p_len_tot+p_len_new)
        p_len_tot = p_len_tot + p_len_new
        #Exogenous
        p_len_new = len(cost_spec['ind_var_exo'])
        self.cost_spec['param_exo'] = np.arange(p_len_tot,p_len_tot+p_len_new)
        p_len_tot = p_len_tot + p_len_new

        # Initialize parameter vector with small random numbers
        vec = np.random.rand(p_len_tot)*0.1 - 0.05
        self.param_vec = vec
  #       self.param_vec = np.array([ 58.7245  ,17.5901  ,10.6527 ,  7.8984,   9.8879 , 13.0144 , 10.0956 ,  9.7652,
  # 11.0345 , 10.1342,  12.8248,  10.6775,   9.6027,  10.6189,  11.2543 , 12.643,
  # 10.1815 , 10.0657,   9.4387,  10.143 ,   7.626 ,  10.275 ,  10.5768 , 10.4325,
  # 10.0348 , 12.2741,  11.5651,  10.9838,  11.8441,  10.1349,  10.8854 ,  9.8517,
  # 11.0362 , 11.0812,   9.858 ,  10.1483,  10.3919,  10.0576,  10.5826 , 10.0581,
  #  8.5439 ,  8.6596,   8.6182,   8.6379,   8.6286,   8.6287,   8.6323 ,  8.6271,
  #  8.6155 ,  8.612 ,   8.6263,   8.6422,   8.6498,   8.6733,   8.6946 ,  8.7885,
  #  8.8534 ,  8.8064,  -0.7003,  -0.8152,  -0.9177,   3.4183,  -1.2205 ,  1.6386,
  #  0.8196 ,  3.3985,   0.737 ,   2.5667,  -2.0047,   2.9847,   5.6774 ,  3.0523,
  # 10.3305 , 10.2223,  10.1494,  10.1666,  10.1334,  10.1342,  10.0452 , 10.0967,
  # 10.06   , 10.084 ,   9.9779,   9.9839,   9.9932,  10.0143,   9.9694 ,  9.9794,
  # 10.0031 ,  9.9151,   0.1507,   0.3655,   1.8631,  -2.4306,  -0.2368 , -5.8065,
  #  0.3254 ,  2.0865,   7.3106,   5.0072,   2.8482,  -1.8372,   0.352  , -0.2272,
  #  2.7284 ,  9.9728,   9.881 ,   9.8912,   9.9086,   9.9068,   9.9062 ,  9.7666,
  #  9.7377 ,  9.7062,   9.7388,   9.7048,   9.7182,   9.617 ,   9.6621 ,  9.5569,
  #  9.3952 ,  9.4074,   9.3979,  75.5648,   9.6494,   9.9849,   0.7329 ,  6.203,
  # 10.9629 ,  3.5286,   3.4272,   5.867 ,   1.1847,   4.6104,   6.046  ,  1.701,
  # 10.9419 ,  8.2874,   9.6484,   1.9446,   9.3449,  -0.3571,   4.5206 ,  2.3385,
  # -2.493  ,  5.7051,   4.1138,   4.187 ,  10.7372,   4.856 ,  10.3322 ,  7.7777,
  #  7.3247 ,  3.4659,   9.8408,   1.4541,   2.8293,  -0.3624,   7.9911 ,  6.3381,
  #  9.8823 ,  9.5959,   9.8445,   9.7533,   9.7464,   9.9603,   9.6349 ,  9.5834,
  #  9.3299 ,  9.2693,   9.3137,   9.2943,   9.1787,   9.2691,   9.0989 ,  9.2002,
  #  9.4822 ,  9.2485, -26.4586,   6.9984, -16.3593,  -0.1433,  -0.1448])

        # Some useful properties
        self.rownum = df.shape[0]
        self.parnum = len(vec)

    # Update parameter vector
    def update(self,step):
        self.param_vec = self.param_vec + step

    # Set new parameter vector
    def set(self,vec):
        self.param_vec = vec

    # Check that X'X is full rank
    def check_full_rank(self,data):
            K = len(self.dem_spec_list)
            for k in range(K):
                spec = self.dem_spec_list[k]
                X = data[spec['index'],:]
                X = X[:,spec['ind_var']]
                check = np.matmul(np.transpose(X),X)
                w, v = np.linalg.eig(check)
                print('Minimum Eigen Absolute Value',min(np.absolute(w)),' Specification ',spec['dep_var'])

    # Output parameter vector with labels
    def output(self,data,W):
        ## Compute Standard Errors
        # avar = gmm.gmm_avar(data,self,W)
        # print(np.diag(avar))
        # se = np.sqrt(np.diag(avar)/self.rownum)


        parameter_labels = list()
        parameter_index = list()
        model_label = list()
        K = len(self.dem_spec_label_list)
        for k in range(K):
            parameter_labels.extend(self.dem_spec_label_list[k]['ind_var'])
            parameter_index.extend(self.dem_spec_list[k]['param'])
            mdl = np.repeat(self.dem_spec_label_list[k]['dep_var'],len(self.dem_spec_list[k]['ind_var']))
            model_label.extend(mdl)

        parameter_labels.extend(self.cost_spec_label['ind_var_endo'])
        parameter_index.extend(self.cost_spec['param_endo'])
        mdl = np.repeat(self.cost_spec_label['dep_var'],len(self.cost_spec_label['ind_var_endo']))
        model_label.extend(mdl)

        parameter_labels.extend(self.cost_spec_label['ind_var_exo'])
        parameter_index.extend(self.cost_spec['param_exo'])
        mdl = np.repeat(self.cost_spec_label['dep_var'],len(self.cost_spec_label['ind_var_exo']))
        model_label.extend(mdl)

        df = pd.DataFrame(data = {'Index_Check':parameter_index,
                                'Model':model_label,
                                'Parameter':parameter_labels,
                                'Estimate':self.param_vec})#,
                                # 'StandardErrors':se})
        df.to_csv("Estimate_Results.csv",index=False)
