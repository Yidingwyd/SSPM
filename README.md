# SSPM
A self-supervised probabilistic model for unlabeled crystal structures.

The package provides two major functions:
1. Train a SSPM with a customized dataset;
2. Utilize the pre-trained SSPM for materials design:
   * Unbiased atomic represetations learnt from crystal structures;
   * Predict the composition of a specific crystal structure;
   * Predict the composition of a specific crystal structure type;
   * Predict the lattice parameters of a material with specific composition and crystal structure type.

We construct SSPM based on [CGCNN](https://github.com/txie-93/cgcnn).

# Prerequisites
This package requires: pytorch, scikit-learn, pymatgen, pandas, numpy, scipy.

# Usage
## Define a customized dataset
To input crystal structures to SSPM, you will need to define a customized dataset.
You will need CIF files recording the masked crystal structures, a `id_prop.csv` file, and a `atom_init.json` file.
* For the CIF files, the masked atoms are taken as Am element.
* For the `id_prop.csv` file, there are two columns, where the first column recodes a unique ID for each crystal and the second column recodes the atomic number of the masked atoms.
* The `atom_init.json` file stores the initialization vector for each element. An example of atom_init.json is data/my_data_path/atom_init.json, which should be good for most applications.

Alternatively, if you have json files recording stable crystal structures like that in `'./data/binary.json'`, `get_my_data.py` might help you to generate your dataset automatively.


