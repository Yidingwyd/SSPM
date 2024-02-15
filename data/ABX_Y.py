# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 21:30:00 2023

@author: Yiding Wang
"""

import numpy as np
import pandas as pd
from scipy.stats import norm

def gauss(miu, sigma, lattice_range):
    normal = norm(loc=miu, scale=sigma)
    return normal.pdf(lattice_range)
    
def ABD_C(miu, sigma, lattice_range, result_df, save_path):
    p_d_c=gauss(miu,sigma,lattice_range).reshape([-1,1])
    res = np.array(result_df.iloc[:,1:])
    abd_c = res * p_d_c
    save_df = result_df.copy()
    save_df.iloc[:, 1:] = abd_c
    save_df.to_excel(save_path)
    return save_df

def find_max(save_df, top=10):
    max_comp = save_df.max().sort_values(ascending=False)
    max_index = save_df.idxmax()
    max_df = pd.DataFrame()
    for i in max_comp.index[1:top+1]:
        max_df.loc[i, 'composition_p'] = max_comp.loc[i]
        max_df.loc[i, 'lattice_parameter'] = save_df.loc[max_index.loc[i], 'lattice_parameter']
    print(max_df)
    return max_df
    
miu=3.51288     
sigma=0.38693
lattice_range = [round(x*0.01, 2) for x in range(250, 450)]
result_path = './B2-structure/B2_struct_pred.xlsx'
result_df = pd.read_excel(result_path)
save_path = './B2-structure/ABX_B2.xlsx'
save_df = ABD_C(miu, sigma, lattice_range, result_df, save_path)
max_df = find_max(save_df, top = 10)

# miu=6.81325
# sigma=0.93238
# result_path = './D03-structure/D03_struct_pred.xlsx'
# lattice_range = [round(x*0.01, 2) for x in range(482, 868)]
# result_path = './D03-structure/D03_struct_pred.xlsx'
# result_df = pd.read_excel(result_path)
# save_path = './D03-structure/ABX_D03.xlsx'
# save_df = ABD_C(miu, sigma, lattice_range, result_df, save_path)
# max_df = find_max(save_df, top = 10)

# miu=4.40666
# sigma=0.47386
# lattice_range = [round(x*0.01, 2) for x in range(312, 535)]
# result_path = './L12-structure/L12_struct_pred.xlsx'
# result_df = pd.read_excel(result_path)
# save_path = './L12-structure/ABX_L12.xlsx'
# save_df = ABD_C(miu, sigma, lattice_range, result_df, save_path)
# max_df = find_max(save_df, top = 10)










