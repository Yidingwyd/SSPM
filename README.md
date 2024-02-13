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
`model_best.pth.tar` and `test_results.csv`: Due to the development based on the [CGCNN](https://github.com/txie-93/cgcnn) codes, they are currently useless and need to be optimized in later versions.  
`checkpoint.pth.tar`: Stores the SSPM model at the last epoch.

## Get the atomic representations using the pre-trained model
Change the parameters `h_fea_len` and `modelpath` in `get_ele_vec.py`, then run `get_ele_vec.py`. You can also use our pre-trained model in `./pre-trained`.

After that, you will get a `element vec.xlsx`, storing unbiased atomic representations for downstream composition-only machine learning models.

## Predict the composition of a specific crystal structure
Firstly, you need to construct a dataset of the crystal structrue with all the combinations of chemical elements and masked nodes. The requirement of this dataset is the same as [Define a customized dataset](https://github.com/Yidingwyd/SSPM/blob/main/README.md#define-a-customized-dataset).   
`create_structure_cif.py` in `./data` can help to create datasets with B2, D03 and L12 crystal structures of different lattice parameters.  
Then, run the following code to estimate the likelihood of different elements in given crystal structures.
```
python predict.py pre-trained_model_path dataset_path
```
After running prediction, you will get a `test_results.csv`, where the first colum is the material IDs, and the other colunmns are the probabilities of different elements in a given crystal structure environment.

Next, to solve the overdetermined equations, you need to run `joint_probability.py` in `./data`. You will need to define the lattice_range, result_path, and save_path in the codes.

After solving the equations, you will get a `xlsx` file, where the first column is the different lattice parameters, and the other columns are probabilities for different compositions. Our results for B2, D03, and L12 crystal structures are stored in `.\data\B2-structure\B2_struct_pred.xlsx`, `.\data\D03-structure\D03_struct_pred.xlsx`, and `.\data\L12-structure\L12_struct_pred.xlsx`, respectively.

Finally, run `AB_XY.py` in `./data` to get the top k compositions of a given crystal structure.

Notably, the scripts only support cubic crystals by now. For advanced users, if you want to predict a single crystal structure, you can refer to the `equation` class in `joint_probability.py` and the `find_largest` class in `AB_XY.py`.   

## Predict the composition of a specific crystal structure type
Firstly, run `ABX_Y.py` in `./data` to deduce p(A,B,X|Y). In this program, miu and sigma are the mean value and the standard deviation of the 

# Acknowledgement
We developed SSPM based on [CGCNN](https://github.com/txie-93/cgcnn).
