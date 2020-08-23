# hercules-challenge-publications
Code related to the Researchers and Publications track from the Hercules challenge.

## Directory layout
* __data__: Directory with the input dataset for this track.
* __notebooks__: Jupyter notebooks with the process taken for the creation and training of the topic extraction system.
* __results__: Output of the notebooks and scripts from the system. This folder contains a variety of files (pickled models, dataframes, track output...).
* __scripts__: Scripts provided to run the final system and obtain predictions for the track.
* __src__: Track-specific source code regarding the parsing and handling of publications.

## Dependencies
In order to run the code from this repository, Python 3.7 or greater is required. Experiments were executed in Python 3.7.8, and that is the preferred version for the execution of the models. 

Instructions to install Python 3.7.8 are available at the [official website](https://www.python.org/downloads/release/python-378/). 

Once Python has been installed, it is preferrable to create a [environment] before installing the dependencies. To create a new python environment, the following command can be used:
```python
python -m venv edma_env
```

This environment can be then used with the following command:
```bash
souce edma_env/bin/activate
```

Finally, we can install the dependencies of the system with pip:
```python
pip install -r requirements.txt
```

## Exploring the creation of the systems
In the notebooks directory we provide a series of Jupyter notebooks that can be executed to explore how the systems were created and get more information about them or finetune their hyperparameters. In this section we will explain how to run those notebooks and provide some advice on how they should be executed.

If you have followed the steps from the previous section to install Python and the project dependencies, the [jupyter package](https://pypi.org/project/jupyter/) should already be installed. In order to run the Jupyter client, go to the notebooks directory and run the _jupyter notebook_ command:
```bash
cd notebooks
jupyter notebook
```

This will open a new tab in your browser with the Jupyter explorer where the different files can be explored:
![]()

If the browser was not automatically opened, you can connect to the Jupyter client through localhost on port 8888 ([localhost:8888](http://localhost:8888)).

Now you can click on any of the notebooks to explore its content or even rerun and modify the cells. Instructions on how to do this are provided in the [official Notebook docs](https://jupyter-notebook.readthedocs.io/en/stable/examples/Notebook/Notebook%20Basics.html).

It is recommended to run the notebooks in a sequential manner, in the order indicated by their first filename number (i.e. notebook _1_data_fetching.ipynb_ should be run before _2_Data_Exploration.ipynb_ and so on). Non-sequential execution is not recommended and should be avoided, since the execution of one notebook may depend on outputs produced by the previous ones.

## How to run the systems
> __Note__: In order to run the systems you must first obtain the models used to perform the topic extraction. Due to size constraints, they are not included in this repositories. There are two main alternatives to obtain the models: the first one is the execution of every notebook to retrain and build the systems for scratch, but this may take some time; the second alternative is to go to the [complete_system directory](./results/7_complete_system) and follow the instructions to download the trained models.
Several scripts are provided in the _scripts_ folder to execute the systems and reproduce the results obtained for this track. In the following sections we will explain how to explain the main functionality of each script and how it can be executed.

### Obtain track results


### Predict publication topics


### Obtain author topics

