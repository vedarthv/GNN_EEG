#%%
import numpy as np
import matplotlib.pyplot as plt
import mne
import time
import glob
import pandas as pd
from pathlib import Path
from sklearn.preprocessing import MinMaxScaler
from data_methods import *
from mne.io import RawArray
from autoreject import get_rejection_threshold
#from sklearn.decomposition import FastICA, PCA


#%%
project_dir = str(Path(__file__).resolve().parents[2].joinpath('data/raw/*'))
file_list_in = glob.glob(project_dir)
list_im = [file for file in file_list_in]
list_im.sort()
print("file_list:{}".format(list_im))

#%%
# directory to save intermediate/final files to
save_dir = str(Path(__file__).resolve().parents[2].joinpath('data/processed'))

# store standard montage to populate missing location data (`dig` object)
montage = mne.channels.make_standard_montage('standard_1020')

# define time step for segmenting data
tstep = 4.


# create info objects
info = mne.create_info(ch_names=['Fp1','Fp2','F7','F3','Fz','F4','F8','T7',
                             'C3','Cz','C4','T8','P7','P3','Pz','P4','P8',
                             'O1','O2','A2', '23A', '24A'],
                    sfreq=256., ch_types='eeg')
# set montage of info object
info.set_montage(montage, on_missing = 'warn')

info2 = mne.create_info(ch_names=['Fp1','Fp2','F7','F3','Fz','F4','F8','T7',
                             'C3','Cz','C4','T8','P7','P3','Pz','P4','P8',
                             'O1','O2','A2'],
                    sfreq=256., ch_types='eeg')

info2.set_montage(montage, on_missing = 'warn')    
    
for k in list_im:
    # file name without extension
    filename = Path(k).stem
    print(f"Now creating raw (RawArray) for file {k}\n")
    raw = mne.io.read_raw_edf(k)
    data = raw.get_data()
    
    
    if(len(data) == 20):
        print(f"Now creating raw_ica (RawArray) for file {k}\n")
        raw_ica = mne.io.RawArray(data=data, info = info2)
    else:
        print(f"Now creating raw_ica (RawArray) for file {k}\n")
        raw_ica = mne.io.RawArray(data=data, info = info)
    

    
    # filtered constructed rawArray objects
    print(f"Now creating filtered_ica copy (RawArray) for file {k}\n")
    filtered_ica = filter_raw_data(raw_ica)
   
    # flatten filtered data to use sklearn MinMaxScaler for normalization
    # filtered_data_only = filtered_ica.get_data()
    # n_channels, n_times = filtered_data_only.shape
    # data_flat = filtered_data_only.reshape(n_channels, -1)
    
    # # create MinMaxScaler object
    # MinMax = MinMaxScaler()
    
    # # fit scaler object to flattened filtered data
    
    # MinMax.fit(data_flat)
    
    # # transform data
    
    # data_scaled = MinMax.transform(data_flat)
    
    # reshape data back into original shape
    
    # data_scaled = data_scaled.reshape(n_channels, n_times)
    
    if (len(filtered_ica.get_data()) == 20):
        print(f"Now creating rawArr_scaled (RawArray) for file {k}\n")
        rawArr_scaled = filter_raw_data(mne.io.RawArray(data=filtered_ica.get_data(), info = info2))
    else:
        print(f"Now creating rawArr_scaled (RawArray) for file {k}\n")
        rawArr_scaled = filter_raw_data(mne.io.RawArray(data=filtered_ica.get_data(), info = info))

    # save scaled RawArray
    scaled_file = f'{save_dir}/RawObjects/{filename}_scaled.fif'
    rawArr_scaled.save(scaled_file, overwrite=True)
    
    
    # compute ICA in MNE
    
    # this is done for the sole reason of increasing sample size and so that `get_rejection_threshold` works
    events_ica = mne.make_fixed_length_events(rawArr_scaled, duration=tstep)
    epochs_ica = mne.Epochs(rawArr_scaled, events_ica, tmin=0., tmax = tstep,
                        baseline=None,
                        preload=True)
    epochs_ica = epochs_ica.drop_channels(['23A', '24A'], on_missing='warn')
    ica_mne = mne.preprocessing.ICA(n_components=0.99, random_state=42)
    
    # automatically determine threshold above which data is considered to be excessively noisy
    # `get_rejection_threshold` requires mne.Epochs
    reject = get_rejection_threshold(epochs_ica)

    # fit ICA
    ica_mne.fit(epochs_ica,
            reject =reject,
            tstep=tstep)

    # save ICA object
    ica_file = f'{save_dir}/IC/{filename}_ica.fif'
    ica_mne.save(ica_file, overwrite=True)

    
#%%
import os
from pathlib import Path
import mne

filename = 'MDDS5EO'
data_dir = os.path.abspath('../../data')
rawsc = mne.io.read_raw_fif(str(Path(data_dir, 'processed', 'RawObjects', f'{filename}_scaled.fif').resolve()))

rawsc.info

# %%
