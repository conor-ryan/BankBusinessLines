import ProfitFunctions as pf
import DemandIV as iv
import GMM as gmm
import numpy as np
import pandas as pd


#### Class Variable: the object we are going to estimate
class Parameter:
    # par_dep_index = 0
    # par_prod_index = [1,2,3,4]
    # par_cost_index = [5,6,7,8,9]

    def __init__(self,df,dem_spec_list,cost_spec):
        self.dem_spec_label_list = dem_spec_list
        self.cost_spec_label = cost_spec
        K = len(dem_spec_list)
        self.dem_spec_list = list()
        p_len_tot = 0
        data = df.to_numpy()
        for k in range(K):
            spec_dict = dict()
            spec_dict['dep_var'] = [i for i, val in enumerate(df.columns) if val==dem_spec_list[k]['dep_var'] ][0]
            spec_dict['ind_var'] = [i for i, val in enumerate(df.columns) if val in dem_spec_list[k]['ind_var'] ]
        
            spec_dict['inst_var'] = [i for i, val in enumerate(df.columns) if val in dem_spec_list[k]['inst_var'] ]
            flag_ind = [i for i, val in enumerate(df.columns) if val==dem_spec_list[k]['flag_var'] ][0]
            spec_dict['index'] = data[:,flag_ind] == 0

            p_len_new = len(spec_dict['ind_var'])
            spec_dict['param'] = np.arange(p_len_tot,p_len_tot+p_len_new)
            p_len_tot = p_len_tot + p_len_new
            self.dem_spec_list.append(spec_dict)

        self.cost_spec = dict()
        self.cost_spec['dep_var'] = [i for i, val in enumerate(df.columns) if val==cost_spec['dep_var'] ][0]
        self.cost_spec['ind_var'] = [i for i, val in enumerate(df.columns) if val in cost_spec['ind_var'] ]
        self.cost_spec['index'] = np.repeat(True,df.shape[0])

        p_len_new = len(cost_spec['ind_var'])
        self.cost_spec['param'] = np.arange(p_len_tot,p_len_tot+p_len_new)
        p_len_tot = p_len_tot + p_len_new


        vec = np.random.rand(p_len_tot)*0.1 - 0.05
        self.param_vec = vec
        self.rownum = df.shape[0]
        self.parnum = len(vec)

    def update(self,step):
        self.param_vec = self.param_vec + step

    def set(self,vec):
        self.param_vec = vec

    def check_full_rank(self,data):
            K = len(self.dem_spec_list)
            for k in range(K):
                spec = self.dem_spec_list[k]
                X = data[spec['index'],:]
                X = X[:,spec['ind_var']]
                check = np.matmul(np.transpose(X),X)
                w, v = np.linalg.eig(check)
                print('Minimum Eigen Absolute Value',min(np.absolute(w)),' Specification ',spec['dep_var'])

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

        parameter_labels.extend(self.cost_spec_label['ind_var'])
        parameter_index.extend(self.cost_spec_label['param'])
        mdl = np.repeat(self.cost_spec_label['dep_var'],len(self.cost_spec_label['ind_var']))
        model_label.extend(mdl)

        df = pd.DataFrame(data = {'Index_Check':parameter_index,
                                'Model':model_label,
                                'Parameter':parameter_labels,
                                'Estimate':self.param_vec})#,
                                # 'StandardErrors':se})
        df.to_csv("Estimate_Results.csv",index=False)
