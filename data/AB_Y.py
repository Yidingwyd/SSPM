# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 19:17:19 2023

@author: Yiding Wang
"""

import pandas as pd
import numpy as np
from pymatgen.core import Composition

def integral(abd_c, miu, sigma, step, save_path, contain_nonmetal=True):
    # start = round(miu-2*sigma, 2)
    # end = round(miu+2*sigma, 2)
    start = round(miu-2*sigma, 1)
    end = round(miu+2*sigma, 1)
    start_index = abd_c[abd_c.lattice_parameter==start].index[0]
    end_index = abd_c[abd_c.lattice_parameter==end].index[0]
    integral_part = np.array(abd_c.iloc[start_index:end_index, 1:])
    results = sum(integral_part)*step
    integral_df = pd.DataFrame()
    for i, r in enumerate(results):
        integral_df.loc[abd_c.columns[i+1], 'P(A,B|C)'] = r
        index = abd_c.loc[start_index:end_index, abd_c.columns[i+1]].idxmax()
        integral_df.loc[abd_c.columns[i+1], 'lattice_parameter'] = abd_c.loc[index, 'lattice_parameter']
    integral_df = integral_df.sort_values('P(A,B|C)', ascending=False)
    if not contain_nonmetal:
        for i in integral_df.index:
            comp = Composition(i)
            for e in comp.elements:
                if not e.is_metal:
                    integral_df = integral_df.drop(i)
                    break
    integral_df.to_excel(save_path)
    return integral_df

abx_y_path = './B2-structure/ABX_B2.xlsx'
save_path = './B2-structure/AB_B2.xlsx'
miu = 3.51288
sigma = 0.38693
step = 0.01
abx_y = pd.read_excel(abx_y_path, index_col=0)
integral_df = integral(abx_y, miu, sigma, step, save_path, contain_nonmetal=False)


# abx_y_path = './D03-structure/ABD_D03.xlsx'
# save_path = './D03-structure/AB_D03.xlsx'
# miu=6.81325
# sigma=0.93238
# step = 0.01
# abx_y = pd.read_excel(abx_y_path, index_col=0)
# integral_df = integral(abx_y, miu, sigma, step, save_path, contain_nonmetal=False)

# abx_y_path = './L12-structure/ABD_L12.xlsx'
# save_path = './L12-structure/AB_L12.xlsx'
# miu=4.40666
# sigma=0.47386
# step = 0.01
# abx_y = pd.read_excel(abx_y_path, index_col=0)
# integral_df = integral(abx_y, miu, sigma, step, save_path, contain_nonmetal=False)

