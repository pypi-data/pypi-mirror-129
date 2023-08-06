import errno
import os
import numpy as np
from scipy.io import mmread
from pandas import read_csv
from sklearn.preprocessing import LabelEncoder

import torch
from torch.utils.data import Dataset, DataLoader, random_split
from pyro.contrib.examples.util import get_data_directory



# transformations for single cell data
def fn_x_scdata(x, log_trans = False, use_cuda = True, use_float64 = False):
    if use_float64:
        xp = x.double()
    else:
        xp = x.float()

    if log_trans:
        xp = torch.log(xp + 1.)

    # send the data to GPU(s)
    if use_cuda:
        xp = xp.cuda()

    return xp

def fn_y_scdata(y, num_classes, use_cuda, use_float64 = False):
    yp = torch.zeros(y.shape[0], num_classes)

    # send the data to GPU(s)
    if use_cuda:
        yp = yp.cuda()
        y = y.cuda()

    # transform the label y (integer between 0 and 9) to a one-hot
    yp = yp.scatter_(1, y.view(-1, 1), 1.0)

    if use_float64:
        yp = yp.double()
    else:
        yp = yp.float()

    return yp

def split_sup_valid(X, y, validation_num=10000):
    """
    helper function for splitting the data into supervised and validation parts
    :param X: cells
    :param y: labels (digits)
    :param validation_num: what number of last examples to use for validation
    :return: splits of data 
    """
    # validation set is the last 10,000 examples
    X_valid = X[-validation_num:]
    y_valid = y[-validation_num:]

    X_sup = X[0:-validation_num]
    y_sup = y[0:-validation_num]

    return X_sup, y_sup, X_valid, y_valid

class SingleCellCached(Dataset):
    def __init__(self, data_file, label_file = None, label2class = None, mode = 'sup', log_trans = False, use_cuda = False, use_float64 = False):
        super(SingleCellCached).__init__()
        #super().__init__(**kwargs)

        self.data = mmread(data_file).todense()

        if label_file is None:
            self.labels = np.repeat(0, self.data.shape[0])
            self.num_classes = 1
        else:
            self.labels = read_csv(label_file, header=None).squeeze().to_numpy()
            self.num_classes = len(np.unique(self.labels)) if label2class is None else len(label2class.classes_)
        self.labels = transform_label2class(self.labels, label2class)
        
        self.data = torch.from_numpy(self.data)
        self.labels = torch.from_numpy(self.labels)
        self.use_cuda = use_cuda
        self.mode = mode

        # transformations on single cell data (normalization and one-hot conversion for labels)
        def transform(x):
            return fn_x_scdata(x, log_trans, use_cuda, use_float64)

        def target_transform(y, num_classes):
            return fn_y_scdata(y, num_classes, use_cuda, use_float64)

        self.data = transform(self.data)
        self.labels = target_transform(self.labels, self.num_classes)

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, index):
        xs = self.data[index]
        ys = self.labels[index]
        return xs, ys
        
            
def setup_data_loader(
    dataset, 
    data_file, label_file, label2class,
    mode, fold, log_trans, use_cuda, use_float64,
    batch_size, **kwargs
):
    """
    helper function for setting up pytorch data loaders for a semi-supervised dataset

    :param dataset: the data to use
    :param data_file: the mtx file of single cell data
    :param label_file: the file of class labels
    :param mode: mode of data usage
    :param fold: fraction of the supervised data used for validation
    :param use_cuda: use GPU(s) for training
    :param batch_size: size of a batch of data to output when iterating over the data loaders
    :param kwargs: other params for the pytorch data loader
    :return: three data loader
    """
    # instantiate the dataset as training/testing sets
    if "num_workers" not in kwargs:
        kwargs = {"num_workers": 0, "pin_memory": False}

    cached_data0 = dataset(
        data_file = data_file, label_file = label_file, label2class = label2class,
        mode = mode, log_trans = log_trans, use_cuda = use_cuda, use_float64 = use_float64
    )
    
    if mode == 'sup' and fold > 0:
        data_num = len(cached_data0)
        valid_num = int(np.round(data_num * fold))
        sup_num = data_num - valid_num
        cached_data, cached_valid = random_split(cached_data0, [sup_num, valid_num])
    else:
        cached_data = cached_data0
        cached_valid = None

    loader = DataLoader(
        cached_data, batch_size = batch_size, shuffle = True, **kwargs
    )
    if cached_valid is not None:
        loader_valid = DataLoader(
            cached_valid, batch_size = batch_size, shuffle = True, **kwargs
        )
    else:
        loader_valid = None

    return loader, loader_valid


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def label2class_encoder(labels):
    le = LabelEncoder()
    le.fit(labels)
    return le

def transform_label2class(labels, encoder):
    classes = encoder.transform(labels)
    return classes

def transform_class2label(classes, decoder):
    labels = decoder.inverse_transform(classes)
    return labels

EXAMPLE_DIR = os.path.dirname(os.path.abspath(os.path.join(__file__, os.pardir)))
DATA_DIR = os.path.join(EXAMPLE_DIR, "data")
RESULTS_DIR = os.path.join(EXAMPLE_DIR, "results")


