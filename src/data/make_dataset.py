# -*- coding: utf-8 -*-
import logging
from pathlib import Path
import os, os.path
import errno
import pickle

from data_methods import HEALTHY_FILES, MDD_FILES, get_individual_data

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def safe_open_w(path):
    ''' Open "path" for writing, creating any parent directories as needed.
    '''
    mkdir_p(os.path.dirname(path))
    return open(path, 'wb')

def main() -> None:
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')
    
    
    
    for index in range(1, HEALTHY_FILES + 1):
        filepath = Path(__file__).resolve().parents[2].joinpath('data/processed/H')
        person = get_individual_data(index, patient_type='H')
        with safe_open_w(filepath.joinpath(f'H{index}.pickle')) as f:
            pickle.dump(person, f)
        f.close()
    for index in range(1, MDD_FILES + 1):
        filepath = Path(__file__).resolve().parents[2].joinpath('data/processed/MDD')
        person = get_individual_data(index, patient_type='MDD')
        with safe_open_w(filepath.joinpath(f'MDDS{index}.pickle')) as f:
            pickle.dump(person, f)
        f.close()

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    main()
