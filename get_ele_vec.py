# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 15:47:17 2022

@author: Yiding Wang
"""

from sspm.model import CrystalGraphConvNet
from pymatgen.core.periodic_table import Element
import torch
import pandas as pd

orig_atom_fea_len = 92
nbr_fea_len = 81
atom_fea_len = 64
n_conv = 3
h_fea_len = 128
n_h = 1
modelpath = './pretrained/checkpoint.pth.tar'

model = CrystalGraphConvNet(orig_atom_fea_len, nbr_fea_len,
                                atom_fea_len=atom_fea_len,
                                n_conv=n_conv,
                                h_fea_len=h_fea_len,
                                n_h=n_h,
                                classification=True)

model.cuda()
checkpoint = torch.load(modelpath, map_location=lambda storage, loc: storage)
model.load_state_dict(checkpoint['state_dict'])

ele_vecs=model.fc_out.weight.cpu().detach().numpy()
df = pd.DataFrame()
for i, vec in enumerate(ele_vecs):
    if i == 0:
        continue
    df.loc[i, 'Z'] = i
    df.loc[i, 'Element'] = Element.from_Z(i).symbol
    for j, v in enumerate(vec):
        df.loc[i, j] = v
    # print(vec)

df.to_excel('element vec.xlsx')
