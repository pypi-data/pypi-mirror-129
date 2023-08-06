# scClassifier2
 Deep bag-of-genes model for single cell classification

## Citation
Bin Zhou, Fan Yang, Ting Chen, Feng Zeng. Seeing cells as bags-of-genes: a simple deep generative model for platform-independent single cell classification. Submission. 2021

## Installation
1. Install [pytorch](https://pytorch.org/get-started/locally/) according to your computational platform
2. Install dependencies:
    `pip3 install numpy scipy pandas scikit-learn pyro-ppl matplotlib`

## Prepare matrix and label files
1. scClassifier2 accepts as input the log-transformed gene matrix in the MatrixMarket format usually end in ".mtx", where rows are cells and columns are genes. 
2. The label file can be either the CSV format or the TSV format, one label per line.
3. [Data](https://github.com/ZengFLab/scClassifier2/tree/main/data) gives some examples of matrix and label files.

## Tutorial
Please refer to the [PBMC68k](https://github.com/ZengFLab/scClassifier2/blob/main/pbmc68k_demo.ipynb) example.

## Usage
```
usage: scClassifier    [-h] [--cuda] [--jit] [-n NUM_EPOCHS] [--aux-loss] [-alm AUX_LOSS_MULTIPLIER] [-enum ENUM_DISCRETE]
                        [--sup-data-file SUP_DATA_FILE] [--sup-label-file SUP_LABEL_FILE] [--unsup-data-file UNSUP_DATA_FILE]
                        [--unsup-label-file UNSUP_LABEL_FILE] [-64] [-lt] [--cross-validation-fold CROSS_VALIDATION_FOLD] [-zd Z_DIM]
                        [-hl HIDDEN_LAYERS [HIDDEN_LAYERS ...]] [-lr LEARNING_RATE] [-dr DECAY_RATE] [-de DECAY_EPOCHS] [-b1 BETA_1]
                        [-bs BATCH_SIZE] [-rt] [-log LOGFILE] [--seed SEED] [--best-valid-model BEST_VALID_MODEL] [--best-aux-model BEST_AUX_MODEL]
```

