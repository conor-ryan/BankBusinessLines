import ProfitFunctions as pf
import DemandIV as iv
import numpy as np
import pandas as pd


#### Class Variable: the object we are going to estimate
class Parameter:
    par_cost_index = 0
    par_prod_index = [1,2,3,4]
    par_fc_index = 5

    def __init__(self,vec,df,
                cost_spec_ind,cost_spec_dep,cost_spec_iv,
                dem_spec_ind_list,dem_spec_dep_list,dem_spec_iv_list):


        self.data_dem_dep_list = list()
        self.data_dem_endo_list = list()
        self.data_dem_exo_list = list()

        start_var = 0
        for l in range(len(dem_spec_ind_list)):
            self.data_dem_dep_list.append([i for i, val in enumerate(df.columns) if val==dem_spec_dep_list[l]][0])

            spec_endo = [i for i, val in enumerate(df.columns) if val in dem_spec_endo_list[l]][0]
            spec_exo = [i for i, val in enumerate(df.columns) if val in dem_spec_exo_list[l]]

            self.data_dem_exo_list.append(spec_exo)
            self.data_dem_endo_list.append(spec_endo)

            self.par_dem_endo.extend(start_var)
            self.par_dem_index.append([*range(start_var,start_var + 1 + len(spec_endo))])
            # start_var = start_var + + len(spec_exo) + len(spec_endo)

        self.data_cost_depvar = [i for i, val in enumerate(df.columns) if val==cost_spec_dep][0]
        self.data_cost_endovar = [i for i, val in enumerate(df.columns) if val in cost_spec_endo]
        self.data_cost_exovar = [i for i, val in enumerate(df.columns) if val in cost_spec_exo]

        self.param_vec = zeros(start_var)

    def update(self,step):
        self.param_vec = self.param_vec + step

    def set(self,vec):
        self.param_vec = vec
7
