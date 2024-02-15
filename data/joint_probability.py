# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 16:22:27 2023

根据自监督学习GNN解方程，获得P(A,B|C,D)

@author: Yiding Wang
"""

import numpy as np
import pandas as pd
from itertools import combinations, permutations
from pymatgen.core.periodic_table import Element
import time
from scipy.sparse.linalg import lsqr


def solve(A,b):
    #contradictory equations
    t0 = time.time()
    x = lsqr(A,b)[0]
    t1 = time.time()
    print(t1-t0)
    return x

class equation():    
    def __init__(self, conditional_A, conditional_B, joint_A, joint_B, ind):
        # assert len(conditional_A) == len(conditional_B)
        # self.conditional_A = conditional_A
        # self.conditional_B = conditional_B
        # self.ind = ind
        self.k = len(conditional_A)
        # print(self.k)
        self.marginal_A, self.marginal_B = \
            self.margin(conditional_A,conditional_B,ind)
        self.joint_A = joint_A
        self.joint_B = joint_B
        self.A = self.get_A()
        self.b = self.get_b()
    
    def margin(self, conditional_A, conditional_B, ind):
        marginal_A = np.zeros([self.k*self.k, self.k])
        marginal_B = np.zeros([self.k*self.k, self.k])
        # print(marginal_A.shape)
        # print(conditional_A.shape)
        # print(marginal_B.shape)
        # print(conditional_B.shape)
        np.put_along_axis(marginal_A, ind, conditional_A.T, axis=0)
        np.put_along_axis(marginal_B, ind, conditional_B.T, axis=0)
        return marginal_A, marginal_B
        
    def get_A(self):
        paddings = np.zeros([self.k*self.k, self.k])
        ones = np.ones([1, self.k*self.k])
        zeros = np.zeros([1, 2*self.k])
        last = np.concatenate((ones, zeros), axis=1)
        A = np.concatenate((self.joint_B, paddings, self.marginal_B), axis=1)
        AA = np.concatenate((self.joint_A, self.marginal_A, paddings), axis=1)
        A = np.concatenate((A,AA,last), axis=0)
        return A
    
    def get_b(self):
        b = np.zeros([2*self.k*self.k,])
        b = np.append(b, 1)
        return b
    
    def solve(self):
        return solve(self.A, self.b)
    
def create_B2_dict(lattice_range):
    dic = {}
    index_list = np.array([x*len(lattice_range) for x in range(94)])
    for i, l in enumerate(lattice_range):  
        dic[l] = list(index_list + i)
    return dic

def B2_pred(dic, lattice_range, result_path, save_path):
    result_df = pd.read_csv(result_path)
    pred_df = pd.DataFrame()
    for i, l in enumerate(lattice_range):
    # for i, l in enumerate([2.99, 4.09]):
        print(l)
        conditional_A = np.array(result_df.iloc[dic[l], 2:])
        conditional_B = np.array(result_df.iloc[dic[l], 2:])
        e = equation(conditional_A, conditional_B, joint_A, joint_B, ind)
        # return e
        try:
            x = e.solve()
            joint, _, _ = joint_and_marginal(x,k)
            pred_df.loc[i, 'lattice_parameter'] = l
            for a, b in combinations(range(1, 95), 2):  
                name = Element.from_Z(a).symbol + Element.from_Z(b).symbol
                pred_df.loc[i, name] = joint[a-1, b-1]
            pred_df = pred_df.copy()
        except:
            print('Error!!!')
    pred_df.to_excel(save_path, index=False)
    return pred_df

def create_D03_dict(lattice_range):
    dic = {}
    index_list = np.array([2*x*len(lattice_range) for x in range(94)])
    for i, l in enumerate(lattice_range):  
        dic[str(l)+'a'] = list(index_list + i*2)
        dic[str(l)+'b'] = list(index_list + i*2  + 1)
    return dic

def D03_pred(dic, lattice_range, result_path, save_path):
    result_df = pd.read_csv(result_path)
    pred_df = pd.DataFrame()
    for i, l in enumerate(lattice_range):
    # for i, l in enumerate([5.79, 7.22]):
        print(l)
        conditional_A = np.array(result_df.iloc[dic[str(l)+'a'], 2:])
        conditional_B = np.array(result_df.iloc[dic[str(l)+'b'], 2:])
        e = equation(conditional_A, conditional_B, joint_A, joint_B, ind)
        try:
            x = e.solve()
            joint, _, _ = joint_and_marginal(x,k)
            pred_df.loc[i, 'lattice_parameter'] = l
            for a, b in permutations(range(1, 95), 2):  
                name = Element.from_Z(b).symbol + '3' + Element.from_Z(a).symbol
                pred_df.loc[i, name] = joint[a-1, b-1]
            pred_df = pred_df.copy()
        except:
            print('Error!!!')
    pred_df.to_excel(save_path, index=False)
    return pred_df



def joint_and_marginal(x,k):
    joint = x[:k*k].reshape([k,k])
    marginal_A = x[k*k: (k*k+k)]
    marginal_B = x[(k*k+k):(k*k+2*k)]   
    return joint, marginal_A, marginal_B

    
k = 94  #总元素个数
joint_A = -np.eye(k*k,dtype=int)
joint_B = np.zeros([k*k, k*k], dtype=int)
for m in range(k*k):
    joint_B[m, (m%k)*k+(m//k)] = -1 
ind = np.arange(k*k).reshape([k,k]).T

lattice_range = [round(x*0.01, 2) for x in range(250, 450)]
dic = create_B2_dict(lattice_range)
# lattice_range = [2.99]
result_path = './B2-structure/test_results.csv'
save_path = './B2-structure/B2_struct_pred.xlsx'
pred_df = B2_pred(dic, lattice_range, result_path, save_path)

# lattice_range = [round(x*0.01, 2) for x in range(482, 868)]
# dic = create_D03_dict(lattice_range)
# # lattice_range = [6.95]
# result_path = './D03-structure/test_results.csv'
# save_path = './D03-structure/D03_struct_pred.xlsx'
# pred_df = D03_pred(dic, lattice_range, result_path, save_path)

# lattice_range = [round(x*0.01, 2) for x in range(312, 535)]
# dic = create_D03_dict(lattice_range)
# # lattice_range = [3.14]
# result_path = './L12-structure/test_results.csv'
# save_path = './L12-structure/L12_struct_pred.xlsx'
# pred_df = D03_pred(dic, lattice_range, result_path, save_path)


