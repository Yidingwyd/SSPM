# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 17:17:18 2024

@author: Yiding Wang
"""

import numpy as np
import pandas as pd
from collections import Counter
from itertools import permutations, combinations
from pymatgen.core.periodic_table import Element

# Initialize parameters
num_variables = 3  # m, the number of variables
num_values = 94  # n, the number of different values each variable can take
iterations = 10000  # Number of iterations for Gibbs sampling

# Prepare the conditional probability tables
C_AB_df = pd.read_excel('C_AB.xlsx')
order = ['A','B'] + [str(i) for i in range(1,95)]
C_AB_df = C_AB_df.reindex(columns=order)

B_AC_df = pd.read_excel('B_AC.xlsx')
order = ['A','C'] + [str(i) for i in range(1,95)]
B_AC_df = B_AC_df.reindex(columns=order)

A_BC_df = pd.read_excel('A_BC.xlsx')
order = ['B','C'] + [str(i) for i in range(1,95)]
A_BC_df = A_BC_df.reindex(columns=order)

def get_index(i, j, df):
    col = df.columns
    c0 = col[0]
    c1 = col[1]
    index0 = set(df[df.eval(c0)==i].index.tolist())
    index1 = set(df[df.eval(c1)==j].index.tolist())
    index = list(index0&index1)[0]
    return index

# Gibbs Sampling Function
# Adjusted Gibbs Sampling Function with corrected understanding of conditional probabilities
def gibbs_sampling(A_BC_df, B_AC_df, C_AB_df, iterations):
    
    C_AB = C_AB_df.drop(C_AB_df.columns[0:2], axis=1).to_numpy()
    B_AC = B_AC_df.drop(B_AC_df.columns[0:2], axis=1).to_numpy()
    A_BC = A_BC_df.drop(A_BC_df.columns[0:2], axis=1).to_numpy()

    # Initialize the variables with random states
    A_current = np.random.randint(1, num_values+1)
    B_current = np.random.randint(1, num_values+1)
    
    samples = []
    
    for _ in range(iterations):
        print(_)
        
        index = get_index(A_current,B_current,C_AB_df)
        C_probs = C_AB[index, :]
        C_probs[A_current-1],C_probs[B_current-1]=0,0
        C_probs /= C_probs.sum()
        C_current = np.random.choice(range(1,num_values+1), p=C_probs)
        
        samples.append((A_current, B_current, C_current))
        print(A_current, B_current, C_current)
        
        index = get_index(B_current,C_current,A_BC_df)
        A_probs = A_BC[index, :]
        A_probs[B_current-1],A_probs[C_current-1]=0,0
        A_probs /= A_probs.sum()
        A_current = np.random.choice(range(1,num_values+1), p=A_probs)
        
        samples.append((A_current, B_current, C_current))
        print(A_current, B_current, C_current)
        
        index = get_index(A_current,C_current,B_AC_df)
        B_probs = B_AC[index, :]
        B_probs[A_current-1],B_probs[C_current-1]=0,0
        B_probs /= B_probs.sum()
        B_current = np.random.choice(range(1,num_values+1), p=B_probs)
        
        samples.append((A_current, B_current, C_current))
        print(A_current, B_current, C_current)
        
    return samples

# Run the corrected Gibbs Sampling
samples = gibbs_sampling(A_BC_df, B_AC_df, C_AB_df, iterations)


# 在计算joint_distribution之前修改样本的键,(A,B,C)和(B,A,C)看作相同的
sample_tuples = [tuple(sorted(sample[:2]) + [sample[2]]) for sample in samples]

# 计算每个组合的出现次数以获得联合分布
joint_distribution = Counter(sample_tuples)

# 计算联合概率分布
total_samples = len(samples)
joint_probability_distribution = {k: v / total_samples for k, v in joint_distribution.items()}

df = pd.DataFrame([joint_probability_distribution])


metal_Z = []
for i in range(1,95):
    e = Element.from_Z(i)
    if e.is_metal:
        metal_Z.append(i)

row_name=[]
for A, B in combinations(metal_Z, 2):
    for C in metal_Z:
        row_name.append(f'{A}_{B}_{C}')

data = []
for name in row_name:
    # 解析A, B, C的原子序数
    A, B, C = map(int, name.split('_'))
    # 获取对应的联合概率，如果不存在则为0
    probability = joint_probability_distribution.get((A, B, C), 0)
    data.append([name, probability])

# 转换为DataFrame
df = pd.DataFrame(data, columns=['Combination', 'Probability'])

excel_path = '6.3.xlsx'
df.to_excel(excel_path)
