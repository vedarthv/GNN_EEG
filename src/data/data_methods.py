# -*- coding: utf-8 -*-
import logging
import os as os
from mne.io import read_raw_edf

# Setting the number of files for each type of patient.
HEALTHY_FILES = 30
MDD_FILES = 34


def get_raw_H_data() -> dict:
    """
    This function generates a dictionary with the raw data for each healthy patient,
    :return: A dictionary with the key being the `patient_file_number - 1`  and the value being a list of the raw data from the edf file(s): `EC`, `EO`, `Task`. 
    Shape : { patient_key :[raw_EC, raw_EO, raw_Task ]}, where `patient_key` is the patient file number - 1, with 30 healthy patients in total.
    Some patients may not have all of the files.
    """
    raw_data = {}
    for i in range(1, HEALTHY_FILES + 1):
        raw_data.setdefault(i-1, [])
        raw_data[i-1].append(get_individual_data(i, 'H'))
    return raw_data

def get_raw_MDD_data() -> dict:
    """
    This function generates a dictionary with the raw data for each MDD patient,
    :return: A dictionary with the key being the `patient_file_number - 1`  and the value being a list of the raw data from the edf file(s): `EC`, `EO`, `Task`. 
    Shape : { patient_key :[raw_EC, raw_EO, raw_Task ]}, where `patient_key` is the patient file number - 1, with 34 MDD patients in total.
    Some patients may not have all of the files.
    """
    raw_data = {}
    for i in range(1, MDD_FILES + 1):
        raw_data.setdefault(i-1, [])
        raw_data[i-1].append(get_individual_data(i, 'MDD'))
    return raw_data


def get_raw_data() -> dict:
    """
    It returns a dictionary with two keys, 'H' and 'MDD', and the values are the raw data for the healthy and MDD patients respectively.
    :return: A dictionary with two keys, 'H' and 'MDD', and the values are the raw data for the H and MDD data sets. 
    Shape  -> { 'H' : 'healthy_patient_key' : { [raw_EC, raw_EO, raw_Task ]}, 'MDD' : {'MDD_healthy_patient_key' : [raw_EC, raw_EO, raw_Task ]}}, with 30 healthy patients in total and 34 MDD patients in total.
    """
    return {'H': get_raw_H_data(), 'MDD': get_raw_MDD_data()}


def get_individual_data(index: int, patient_type: str = 'MDD') -> list:
    """
    It takes in a patient index and a patient type (either 'H' or 'MDD') and returns a list of three MNE
    Raw objects, one for each of the three files that are associated with that patient
    
    :param index: the index of the patient
    :type index: int
    :param patient_type: 'H' for healthy, 'MDD' for depressed, defaults to MDD
    :type patient_type: str (optional)
    :return: A list of MNE Raw objects.
    """
    if patient_type not in ['H', 'MDD']:
        raise ValueError('patient_type must be either "H" or "MDD"')
    if index < 1 or (index > 34) or (index > 30 and patient_type == 'H'):
        raise ValueError('Bad index {i} for {patient_type}')
    data_mne = []
    raw_files = [f'./../../data/raw/{patient_type}S{index}EC.edf',
                 f'./../../data/raw/{patient_type}S{index}EO.edf',
                 f'./../../data/raw/{patient_type}S{index}TASK.edf']
    for file in raw_files:
        try:
            data_mne.append(read_raw_edf(file, preload=False, infer_types=True, verbose=False))
        except FileNotFoundError:
            logging.info(f'{patient_type} {index} does not have {file}. Skipping...')
    return data_mne
