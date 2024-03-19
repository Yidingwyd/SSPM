# SSPM
A self-supervised probabilistic model for unlabeled crystal structures.

The package provides two major functions:
1. Train a SSPM with a customized dataset;
2. Utilize the pre-trained SSPM for materials design:
   * Unbiased atomic represetations learnt from crystal structures;
   * Predict the composition of a specific crystal structure;
   * Predict the composition of a specific crystal structure type;
   * Predict the lattice parameters of a material with specific composition and crystal structure type.

# Contents
* [How to cite](https://github.com/Yidingwyd/SSPM/blob/main/README.md#how-to-cite)
* [Prerequisites](https://github.com/Yidingwyd/SSPM/tree/main?tab=readme-ov-file#prerequisites)
* [Usage](https://github.com/Yidingwyd/SSPM/tree/main?tab=readme-ov-file#usage)
  * [Define a customized dataset](https://github.com/Yidingwyd/SSPM/tree/main?tab=readme-ov-file#define-a-customized-dataset)
  * [Train a SSPM model](https://github.com/Yidingwyd/SSPM/tree/main?tab=readme-ov-file#train-a-sspm-model)
  * [Get the atomic representations using the pre-trained model](https://github.com/Yidingwyd/SSPM/tree/main?tab=readme-ov-file#get-the-atomic-representations-using-the-pre-trained-model)
  * [Predict the composition of a specific crystal structure](https://github.com/Yidingwyd/SSPM/tree/main?tab=readme-ov-file#predict-the-composition-of-a-specific-crystal-structure)
  * [Predict the lattice parameters of a material with specific composition and crystal structure type](https://github.com/Yidingwyd/SSPM/tree/main?tab=readme-ov-file#predict-the-lattice-parameters-of-a-material-with-specific-composition-and-crystal-structure-type)
  * [Predict the composition of a specific crystal structure type](https://github.com/Yidingwyd/SSPM/tree/main?tab=readme-ov-file#predict-the-composition-of-a-specific-crystal-structure-type)
* [Data](https://github.com/Yidingwyd/SSPM/tree/main?tab=readme-ov-file#data)
* [Acknowledgement](https://github.com/Yidingwyd/SSPM/tree/main?tab=readme-ov-file#acknowledgement)

# How to cite
Our paper is in submission.

# Prerequisites
This package requires: pytorch, scikit-learn, pymatgen, pandas, numpy, scipy.

# Usage
## Define a customized dataset
To input crystal structures to SSPM, you will need to define a customized dataset.
You will need CIF files recording the masked crystal structures, a `id_prop.csv` file, and a `atom_init.json` file.
* For the CIF files, the masked atoms are taken as Am element.
* For the `id_prop.csv` file, there are two columns, where the first column recodes a unique ID for each crystal and the second column recodes the atomic number of the masked atoms.
* The `atom_init.json` file stores the initialization vector for each element. An example of [`atom_init.json`](https://github.com/Yidingwyd/SSPM/blob/main/data/my_data_path/atom_init.json) is [`./data/my_data_path`](https://github.com/Yidingwyd/SSPM/tree/main/data/my_data_path), which should be good for most applications.

Alternatively, if you have json files recording stable crystal structures like that in [`./data/binary.json`](https://github.com/Yidingwyd/SSPM/blob/main/data/binary.json), [`get_my_data.py`](https://github.com/Yidingwyd/SSPM/blob/main/data/get_my_data.py) might help you to generate your dataset automatively.

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
Change the parameters `h_fea_len` and `modelpath` in [`get_ele_vec.py`](https://github.com/Yidingwyd/SSPM/blob/main/get_ele_vec.py), then run `get_ele_vec.py`. You can also use our pre-trained model in [`./pre-trained`](https://github.com/Yidingwyd/SSPM/tree/main/pre-trained).

After that, you will get a `element vec.xlsx`, storing unbiased atomic representations for downstream composition-only machine learning models.

## Predict the composition of a specific crystal structure
Firstly, you need to construct a dataset of the crystal structrue with all the combinations of chemical elements and masked nodes. The requirement of this dataset is the same as [Define a customized dataset](https://github.com/Yidingwyd/SSPM/blob/main/README.md#define-a-customized-dataset).   
[`create_structure_cif.py`](https://github.com/Yidingwyd/SSPM/blob/main/data/create_structure_cif.py) in [`./data`](https://github.com/Yidingwyd/SSPM/tree/main/data) can help to create datasets with B2, D03 and L12 crystal structures of different lattice parameters.  
Then, run the following code to estimate the likelihood of different elements in given crystal structures.
```
python predict.py pre-trained_model_path dataset_path
```
After running prediction, you will get a `test_results.csv`, where the first colum is the material IDs, and the other colunmns are the probabilities of different elements in a given crystal structure environment.

Next, to solve the overdetermined equations, you need to run [`joint_probability.py`](https://github.com/Yidingwyd/SSPM/blob/main/data/joint_probability.py) in [`./data`](https://github.com/Yidingwyd/SSPM/tree/main/data). You will need to define the lattice_range, result_path, and save_path in the codes.

After solving the equations, you will get an `xlsx` file, where the first column is the different lattice parameters, and the other columns are probabilities for different compositions. Our results for B2, D03, and L12 crystal structures are stored in [`.\data\B2-structure\B2_struct_pred.xlsx`](https://github.com/Yidingwyd/SSPM/blob/main/data/B2-structure/B2_struct_pred.xlsx), `.\data\D03-structure\D03_struct_pred.xlsx`(https://github.com/Yidingwyd/SSPM/blob/main/data/D03-structure/D03_struct_pred.rar), and [`.\data\L12-structure\L12_struct_pred.xlsx`](https://github.com/Yidingwyd/SSPM/blob/main/data/L12-structure/L12_struct_pred.xlsx), respectively.

Finally, run [`AB_XY.py`](https://github.com/Yidingwyd/SSPM/blob/main/data/AB_XY.py) in [`./data`](https://github.com/Yidingwyd/SSPM/tree/main/data) to get the top k compositions of a given crystal structure.

Notably, the scripts only support cubic crystals by now. For advanced users, if you want to predict a single crystal structure, you can refer to the `equation` class in [`joint_probability.py`](https://github.com/Yidingwyd/SSPM/blob/main/data/joint_probability.py) and the `find_largest` class in [`AB_XY.py`](https://github.com/Yidingwyd/SSPM/blob/main/data/AB_XY.py).   

## Predict the lattice parameters of a material with specific composition and crystal structure type
Run [`ABX_Y.py`](https://github.com/Yidingwyd/SSPM/blob/main/data/ABX_Y.py) in [`./data`](https://github.com/Yidingwyd/SSPM/tree/main/data) to deduce p(A,B,X|Y). In this program, `miu` and `sigma` are the mean value and the standard deviation of the statistics lattice parameters by maximum likelihood estimation. You should also change the `result_path` (the path of the above results) and `save_path` (where to save the results of this step) parameters.

In the `xlsx` file you get, each column represents a different composition from the second to the last. Select the column of the composition of interest and sort them from largest to smallest. The lattice parameter corresponding to the maximum value is the predicted value.

## Predict the composition of a specific crystal structure type
Run [`AB_Y.py`](https://github.com/Yidingwyd/SSPM/blob/main/data/AB_Y.py) in [`./data`](https://github.com/Yidingwyd/SSPM/tree/main/data) to deduce P(A,B|Y). Also, you need to define the parameters of `miu`, `sigma` , `step` (the lattice parameter step defined in [`joint_probability.py`](https://github.com/Yidingwyd/SSPM/blob/main/data/joint_probability.py)), `abx_y_path`, and `save_path`. Here, approximate results are deduced by integration of miu ± 2 * sigma.

In the `xlsx` file you get, the compositions are ranked by P(A,B|Y) from largest to smallest.

## Gibbs sampling
Because of the substantial increase in time and spatial complexity when solving equations, Gibbs sampling makes a valuable tool for enhancing inference efficiency to predict the composition of a specific crystal structure.

Here is an example for Heusler compounds. Run [`get_heusler_cond.py`](https://github.com/Yidingwyd/SSPM/blob/main/data/get_heusler_cond.py) first to extract conditional probabilities from `test_results.csv`. You need to define `lattice_para` in the script. After that, you will get three `xlsx` files, `C_AB.xlsx`, `B_AC.xlsx` and `A_BC.xlsx`. Then, run [`gibbs_sampling_heusler.py`](https://github.com/Yidingwyd/SSPM/blob/main/data/gibbs_sampling_heusler.py), in which `iterations` is the number of Gibbs sampling steps you want, and `excel_path` is where to save P(A,B,C|X=lattice_para,Y=Heusler). 

# Data
The data we use is collected from [`Materials Project`](https://next-gen.materialsproject.org/). The formulas and space groups are available in [`dataset.csv`](https://github.com/Yidingwyd/SSPM/blob/main/data/dataset.csv). To reproduce our paper, you can download the corresponding dataset and convert into proper formats. Please cite the relevant papers as requested by the dataset authors.

# Acknowledgement
We developed the self-supervised learning model based on [CGCNN](https://github.com/txie-93/cgcnn).
