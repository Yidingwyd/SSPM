# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 16:37:32 2023

给定C/D，找到最大的P(A,B|C,D)

@author: Yiding Wang
"""

import pandas as pd
from pymatgen.core import Composition

def find_largest(result_df, parameter, n, contain_nonmetal=True):
    result_df = result_df.T
    # ind = lattice_range.index(parameter)
    if not contain_nonmetal:
        for i in result_df.index:
            comp = Composition(i)
            for e in comp.elements:
                if not e.is_metal:
                    result_df = result_df.drop(i)
                    break
    res = result_df.nlargest(n, parameter, keep='last').loc[:,parameter]
    print(res)
    return res

result_path = './B2-structure/B2_struct_pred.xlsx'


# result_path = './D03-structure/D03_struct_pred.xlsx'


# result_path = './L12-structure/L12_struct_pred.xlsx'


result_df = pd.read_excel(result_path, index_col=0)

res = find_largest(result_df, parameter=2.99, n=10, contain_nonmetal=False)
