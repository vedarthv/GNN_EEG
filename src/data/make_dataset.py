# -*- coding: utf-8 -*-
import click
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv

import os as os
from mne.io import concatenate_raws, read_raw_edf



def getData(type: str = 'MDD') -> dict:
    """ Get the healthy control data from the .edf files.
    Args:
        type (str): 'H' for healthy control, 'MDD' for depressed individuals. Default: 'MDD'.
        returns: A dict with with the raw data.
    """
    if type not in ['H', 'MDD']:
        raise ValueError('type must be either "H" or "MDD"')
    
    files_amount = 30 if type == 'H' else 34
    
    data_mne = {}
    
    for i in range(1, files_amount + 1):
        raw_files = [f'./../../data/raw/{type}S{i}EC.edf', f'./../../data/raw/{type}S{i}EO.edf', f'./../../data/raw/{type}S{i}TASK.edf']
        for f in raw_files:
            try:
                data_mne[i] = (read_raw_edf(f, preload=True, infer_types=True, verbose=False))
            except FileNotFoundError:
                logging.info(f'{type} {i} does not have {f}. Skipping...')
    return data_mne

def getIndividualData( index: int, type: str = 'MDD') -> list:
    if type not in ['H', 'MDD']:
        raise ValueError('type must be either "H" or "MDD"')
    if index < 1 or (index > 34) or (index > 30 and type == 'H'):
        raise ValueError('Bad index {i} for {type}')
    
    data_mne = []
    
    raw_files = [f'./../../data/raw/{type}S{i}EC.edf', f'./../../data/raw/{type}S{i}EO.edf', f'./../../data/raw/{type}S{i}TASK.edf']
    for f in raw_files:
        try:
            data_mne.append(read_raw_edf(f, preload=True, infer_types=True, verbose=False))
        except FileNotFoundError:
            logging.info(f'{type} {i} does not have {f}. Skipping...')
    return data_mne

def main() -> None:
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')



if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())
    main()
