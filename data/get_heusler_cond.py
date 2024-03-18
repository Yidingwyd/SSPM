# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 15:59:32 2024

找到条件概率。

@author: Yiding Wang
"""

import pandas as pd
import numpy as np
from pymatgen.core.periodic_table import Element
from itertools import permutations

lattice_para = 6.3

test_results = pd.read_csv('test_results.csv', index_col = 0)
# test_results = pd.read_csv('test_results.csv')

C_AB, B_AC, A_BC = pd.DataFrame(columns=['A','B']),\
                    pd.DataFrame(columns=['A','C']),\
                    pd.DataFrame(columns=['B','C'])


#Heusler
k = 0
for i, j in permutations(np.arange(1,95).tolist(),2):
    index_str=Element.from_Z(i).symbol+'_'+Element.from_Z(j).symbol+'_Am2-'+str(lattice_para)
    C_AB=C_AB.append(test_results.loc[index_str].rename(k))
    C_AB.loc[k, 'A'] = i
    C_AB.loc[k, 'B'] = j
    
    index_str = Element.from_Z(i).symbol+'_Am_'+Element.from_Z(j).symbol +'2-'+str(lattice_para)
    B_AC=B_AC.append(test_results.loc[index_str].rename(k))
    B_AC.loc[k, 'A'] = i
    B_AC.loc[k, 'C'] = j
    
    index_str = 'Am_'+Element.from_Z(i).symbol+'_'+Element.from_Z(j).symbol +'2-'+str(lattice_para)
    A_BC=A_BC.append(test_results.loc[index_str].rename(k))
    A_BC.loc[k, 'B'] = i
    A_BC.loc[k, 'C'] = j
    
    k+=1
    print(k)

C_AB = C_AB.drop('0', axis=1)
B_AC = B_AC.drop('0', axis=1)
A_BC = A_BC.drop('0', axis=1)

C_AB.to_excel('C_AB.xlsx')
B_AC.to_excel('B_AC.xlsx')
A_BC.to_excel('A_BC.xlsx')
