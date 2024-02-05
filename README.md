# SSPM
A self-supervised probabilistic model for unlabeled crystal structures.

The package provides two major functions:
1. Train a SSPM with a customized dataset;
2. Utilize the pre-trained SSPM for materials design:
   a) Unbiased atomic represetations learnt from crystal structures;
   b) Predict the composition of a specific crystal structure;
   c) Predict the composition of a specific crystal structure type;
   d) Predict the lattice parameters of a material with specific composition and crystal structure type.

This package requires: pytorch, scikit-learn, pymatgen, pandas, numpy, scipy.

