Neural Networks Group
==============================

A project emulating a GNN model which uses EEG data to classify depression in individuals.

Quick Start Guide
------------
>**Pre-requities:** Install `Makefile` on your machine. If you have a windows machine, see https://stackoverflow.com/questions/2532234/how-to-run-a-makefile-in-windows for multiple ways to install `Makefile`. 

After cloning the directory, run `make create_environment` to create a conda environemnt with all the dependancies automatically installed. 

Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   ├── notebooks      <- Notebooks are primarily for exploration and will be temorarily stored in the src directory.
    │   │   └── Exploration.ipynb
    │   │
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io

--------

## ICA preprocessing for EEG data

This code outlines how to load in Independent Component Analysis (ICA) objects from `.fif` files and applies them to preprocessed Electroencephalogram (EEG) data. 

To use this code, follow these steps:

1.  Download or clone the repository to your local machine.
2.  Install the required dependencies, including MNE-Python (a Python package for EEG analysis).
3.  Ensure that you have already run the `preprocess.py` script to construct the ICA object and preprocessed data and save them to `.fif` files.
4.  Organize your `.fif` files in a directory and note the format of the file names (e.g., "HS1EC_scaled.fif", "MDDS1EO_ica.fif", "HS9TASK_ica.fif" etc.).
5.  Modify the `patient_status`, `subject_number`, and `state` variables in the code to match the format of your file names.
6.  Modify the `data_path` variable to match the path to the directory where your `.fif` files are located.
7.  Run the code to load the ICA object and preprocessed data, and apply the ICA object to the data.
8.  Use the resulting processed data for further EEG analysis.

By applying ICA to EEG data, we can effectively remove the sources of noise that can obscure or confound the brain signals of interest. This preprocessing step is critical for obtaining reliable and accurate EEG results. Note that the ICA object and preprocessed data loaded in by this code were both constructed using the `preprocess.py` script.


```
import mne

# Define the patient status, subject number, and state for the files you want to load
patient_status = 'H'  # or 'MDDS'
subject_number = 1  # or any other integer
state = 'EC'  # or 'EO' or 'TASK'

# Define the path to the directory where the files are located
data_path = '/path/to/data/directory'

# Construct the file names for the processed_data and ica objects
data_file_name = '{}{}{}_scaled.fif'.format(patient_status, subject_number, state)
ica_file_name = '{}{}{}_ica.fif'.format(patient_status, subject_number, state)

# Load the ICA object from the appropriate file
ica = mne.preprocessing.read_ica('{}/{}'.format(data_path, ica_file_name))

# Load the processed data from the appropriate file
processed_data = mne.io.read_raw('{}/{}'.format(data_path, data_file_name), preload=True)
```

```
# apply ICA object to RawArray object to clean data.
ica.apply(processed_data)
```

--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>.</small></p>
