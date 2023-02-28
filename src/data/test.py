import os as os
import pathlib
from mne.io import concatenate_raws, read_raw_edf
import pandas as pd
from make_dataset import getData
import json

#https://github.com/mne-tools/mne-python/issues/5318


#path = "/Users/vv/Desktop/New Folder/codingProjects/GNN_EEG/data/refined"
#pathlib.Path(path).mkdir(mode=0o777, parents=True, exist_ok=True) 
with open('./H.json', "a") as outfile:
    outfile.write(json.dumps(getData('H'), indent = 4))
with open('./H.json', "a") as outfile:
    outfile.write(json.dumps(getData('MDD'), indent = 4))


