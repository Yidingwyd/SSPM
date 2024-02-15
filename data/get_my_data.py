# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 17:59:48 2023

@author: Yiding Wang
"""

import json, tqdm
from pymatgen.core import Structure
from copy import deepcopy
from pymatgen.core.periodic_table import Element
import pandas as pd
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer

structures = []

with open('binary.json', 'r') as f:
    for i, d in enumerate(f.readlines()):
        # if i > 10:
        #     break
        dic = json.loads(d)
        structures.append(Structure.from_dict(dic['crystal']))
    f.close()
with open('ternary.json', 'r') as f:
    for i, d in enumerate(f.readlines()):
        # if i > 10:
        #     break
        dic = json.loads(d)
        structures.append(Structure.from_dict(dic['crystal']))
    f.close()
with open('quaternary.json', 'r') as f:
    for i, d in enumerate(f.readlines()):
        # if i > 10:
        #     break
        dic = json.loads(d)
        structures.append(Structure.from_dict(dic['crystal']))
    f.close()
    
    
    
e = Element.from_Z(95)
ids, Zs = [], []
id_prop = pd.DataFrame(columns=['id', 'Z'])


for i in tqdm.tqdm(range(len(structures)), ncols=50):
    struct = SpacegroupAnalyzer(structures[i]).get_conventional_standard_structure()
    for s in set(struct.species):
        new_struct = deepcopy(struct)
        for j, ss in enumerate(struct.species):
            if s == ss:
                new_struct.replace(j, e)
        save_name = str(i)+s.symbol
        new_struct.to(filename= ('./my_data_path/'+save_name+'.cif')) 
        ids.append(save_name)
        Zs.append(s.Z)
        # id_prop.loc[k, 'id'] = save_name
        # id_prop.loc[k, 'Z'] = s.Z
        # k += 1
    # if i >= 100:
    #     break

id_prop.loc[:,'id'] = ids
id_prop.loc[:,'Z'] = Zs
id_prop.to_csv('./my_data_path/id_prop.csv', index= False, header=None)
    
    
    
    
