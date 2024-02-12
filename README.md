# SSPM
A self-supervised probabilistic model for unlabeled crystal structures.

The package provides two major functions:
1. Train a SSPM with a customized dataset;
2. Utilize the pre-trained SSPM for materials design:
   * Unbiased atomic represetations learnt from crystal structures;
   * Predict the composition of a specific crystal structure;
   * Predict the composition of a specific crystal structure type;
   * Predict the lattice parameters of a material with specific composition and crystal structure type.

# Prerequisites
This package requires: pytorch, scikit-learn, pymatgen, pandas, numpy, scipy.

# Usage
## Define a customized dataset
To input crystal structures to SSPM, you will need to define a customized dataset.
You will need CIF files recording the masked crystal structures, a `id_prop.csv` file, and a `atom_init.json` file.
* For the CIF files, the masked atoms are taken as Am element.
* For the `id_prop.csv` file, there are two columns, where the first column recodes a unique ID for each crystal and the second column recodes the atomic number of the masked atoms.
* The `atom_init.json` file stores the initialization vector for each element. An example of `atom_init.json` is `./data/my_data_path/atom_init.json`, which should be good for most applications.

Alternatively, if you have json files recording stable crystal structures like that in `'./data/binary.json'`, `get_my_data.py` might help you to generate your dataset automatively.

## Train a SSPM model
After defining a dataset in `rootdir`, you can train a SSPM model by:
```
python main.py --task classification  rootdir
```
You can set the number of training, validation, and test data with labels `--train-size`, `--val-size`, and `--test-size`. Alternatively, you may use the flags `--train-ratio`, `--val-ratio`, `--test-ratio` instead.  
You can also set the hidden feature length, i.e., the length of atomic representations with the label `--h-fea-len`. Default is 128.

After training, you will get three files in this directory:

`model_best.pth.tar` and `test_results.csv`: Due to the development based on [CGCNN](https://github.com/txie-93/cgcnn) code, they are currently useless and need to be optimized in later versions.  
`checkpoint.pth.tar`: stores the SSPM model at the last epoch.

## Get the atomic representations using the pre-trained model
Change the parameters `h_fea_len` and `modelpath` in `get_ele_vec.py`, then run `get_ele_vec.py`. You can also use our pre-trained model in `./pretrained`.

After that, you will get a `element vec.xlsx`, storing unbiased atomic representations for downstream composition-only machine learning models.








# Acknowledgement
We developed SSPM based on [CGCNN](https://github.com/txie-93/cgcnn).
