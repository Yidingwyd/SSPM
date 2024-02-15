# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 10:55:58 2023

@author: Yiding Wang
"""

from pymatgen.core.structure import Structure
from pymatgen.core.periodic_table import Element
import pandas as pd
import csv


def create_B2_structs_diff_sizes(species, coords, lattice_range, path):
    """
    Create a list of structures with different lattice parameters and save them
    to path.

    Parameters
    ----------
    species : list
        list of atomic species.
        Possible kinds of input include a list of dict of elements/species and 
        occupancies, a List of elements/specie specified as actual Element/Species,
        Strings (“Fe”, “Fe2+”) or atomic numbers (1,56).
    coords : list
        list of Cartesian coordinates of each species.
    lattice_range : numpy arange
        A range of lattice parameters.
    path : str
        save path.

    Returns
    -------

    """
    
    save_name = ''
    species_new = list(set(species))
    species_new.sort()
    for z in species_new:
        e = Element.from_Z(z)
        save_name += e.symbol
    for i, l in enumerate(lattice_range):
        lattice=[[l,0,0],[0,l,0],[0,0,l]]
        s = Structure(lattice, species, coords)
        s.to(filename= path + save_name + str(l) + '.cif', fmt = 'cif')
    return       

def create_B2_csv(lattice_range, path):
    with open(path+'id_prop.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        for z in range(1, 95):  
            for i, l in enumerate(lattice_range):
                name = ''
                name += Element.from_Z(z).symbol
                name += Element.from_Z(95).symbol
                name += str(l)
                writer.writerow((name, z))
        f.close()

def B2_dataset(lattice_range, path):
    coords = [[0,0,0],[0.5,0.5,0.5]]
    for i in range(1, 95):
        species = [i, 95]
        create_B2_structs_diff_sizes(species, coords, lattice_range, path)
    create_B2_csv(lattice_range, path)

def create_D03_structs_diff_sizes(z, coords, lattice_range, path):
    for i, l in enumerate(lattice_range):
        save_name = ''
        lattice=[[l,0,0],[0,l,0],[0,0,l]]
        
        species = [z] * 4 + [95] * 12
        s = Structure(lattice, species, coords)
        save_name += Element.from_Z(z).symbol
        save_name += Element.from_Z(95).symbol
        save_name += '3-'
        s.to(filename= path + save_name + str(l) + '.cif', fmt = 'cif')
        
        save_name = ''
        species = [95] * 4 + [z] * 12
        s = Structure(lattice, species, coords)
        save_name += Element.from_Z(95).symbol
        save_name += Element.from_Z(z).symbol
        save_name += '3-'
        s.to(filename= path + save_name + str(l) + '.cif', fmt = 'cif')
    return       


def create_D03_csv(lattice_range, path):
    with open(path+'id_prop.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        for z in range(1, 95):  
            for i, l in enumerate(lattice_range):
                name = ''
                name += Element.from_Z(z).symbol
                name += Element.from_Z(95).symbol
                name += '3-'
                name += str(l)
                writer.writerow((name, z))
                name = ''
                name += Element.from_Z(95).symbol
                name += Element.from_Z(z).symbol
                name += '3-'
                name += str(l)
                writer.writerow((name, z))
        f.close()

def D03_dataset(lattice_range, path):
    coords = [[0,0,0],
              [0,0.5,0.5],
              [0.5,0,0.5],
              [0.5,0.5,0],
              [0.5,0.5,0.5],
              [0.5,0,0],
              [0,0.5,0],
              [0,0,0.5],
              [0.25,0.25,0.25],
              [0.75,0.75,0.75],
              [0.75,0.75,0.25],
              [0.25,0.25,0.75],
              [0.75,0.25,0.75],
              [0.25,0.75,0.25],
              [0.25,0.75,0.75],
              [0.75,0.25,0.25]]
    for i in range(1, 95):
        create_D03_structs_diff_sizes(i, coords, lattice_range, path)
    create_D03_csv(lattice_range, path)
    
def create_L12_structs_diff_sizes(z, coords, lattice_range, path):
    for i, l in enumerate(lattice_range):
        save_name = ''
        lattice=[[l,0,0],[0,l,0],[0,0,l]]
        
        species = [z] + [95] * 3
        s = Structure(lattice, species, coords)
        save_name += Element.from_Z(z).symbol
        save_name += Element.from_Z(95).symbol
        save_name += '3-'
        s.to(filename= path + save_name + str(l) + '.cif', fmt = 'cif')
        
        save_name = ''
        species = [95] + [z] * 3
        s = Structure(lattice, species, coords)
        save_name += Element.from_Z(95).symbol
        save_name += Element.from_Z(z).symbol
        save_name += '3-'
        s.to(filename= path + save_name + str(l) + '.cif', fmt = 'cif')
    return       


def create_L12_csv(lattice_range, path):
    with open(path+'id_prop.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        for z in range(1, 95):  
            for i, l in enumerate(lattice_range):
                name = ''
                name += Element.from_Z(z).symbol
                name += Element.from_Z(95).symbol
                name += '3-'
                name += str(l)
                writer.writerow((name, z))
                name = ''
                name += Element.from_Z(95).symbol
                name += Element.from_Z(z).symbol
                name += '3-'
                name += str(l)
                writer.writerow((name, z))
        f.close()

def L12_dataset(lattice_range, path):
    coords = [[0,0,0],
              [0,0.5,0.5],
              [0.5,0,0.5],
              [0.5,0.5,0]]
    for i in range(1, 95):
        create_L12_structs_diff_sizes(i, coords, lattice_range, path)
    create_L12_csv(lattice_range, path)     
    
def Fm_3m_dataset(lattice_range, path):
    coords = [[0,0,0],[0,0.5,0.5],[0.5,0,0.5],[0.5,0.5,0],
              [0,0,0.5],[0.5,0,0],[0,0.5,0],[0.5,0.5,0.5]]
    for i in range(1, 95):
    # for i in [7]:
        species = [i, i, i, i, 95, 95, 95, 95]
        create_B2_structs_diff_sizes(species, coords, lattice_range, path)
    create_B2_csv(lattice_range, path)


def create_cmcm_structs_diff_sizes(species, coords, lattice_range, path):
    save_name = ''
    species_new = list(set(species))
    species_new.sort()
    for z in species_new:
        print(z)
        e = Element.from_Z(z)
        save_name += e.symbol
    for i, l in enumerate(lattice_range):
        # print(l)
        lattice=[[l[0],0,0],[0,l[1],0],[0,0,l[2]]]
        s = Structure(lattice, species, coords)
        s.to(filename= path + save_name + str(l) + '.cif', fmt = 'cif')
    return       

##Create a B2 dataset
# lattice_range = [round(x*0.01, 2) for x in range(250, 450)]
# path = './B2-structure/'
# B2_dataset(lattice_range, path)

##Create a D03 dataset
# lattice_range = [round(x*0.01, 2) for x in range(482, 868)]
# path = './D03-structure/'
# D03_dataset(lattice_range, path)

#Create a L12 dataset
lattice_range = [round(x*0.01, 2) for x in range(312, 535)]
path = './L12-structure/'
L12_dataset(lattice_range, path)








