# About
This repository contains a Python packaging course designed for some UNIL courses. The course takes place on the 20th of February, 2024.

> **Note:** The Julia packaging course is available here: [julia-packaging](https://github.com/Unil-SGC/julia-packaging).

### Jupyter notebooks
Several level of notebooks are designed here. The different steps show how one should proceed to create Python scripts from a existing jupyter notebook.
- [visualize_iceflow_1.ipynb](materials/visualize_iceflow_1.ipynb) is a bad written juypter notebook.
- [visualize_iceflow_functions_2.ipynb](materials/visualize_iceflow_functions_2.ipynb) is composed of functions.
- [visualize_iceflow_class_3.ipynb](materials/visualize_iceflow_class_3.ipynb) is using some classes to include parameters easily.
- [visualize_iceflow_class_3.py](materials/visualize_iceflow_class_3.py) is the conversion of the previous notebook to a Python script, thanks to ```jupyter nbconvert --to python``` command line.
- [final_script.py](materials/final_script.py) is the improved Python script one could obtain from the first jupyter notebook.

### Run slides

To open jupyter notebook presentation, create a Python virtual environment and actiavte it: ```python -m venv .venv``` ```source .venv/bin/activate```.

Install requirements to this virtual environment: ```pip install -r requirements_jupyter_notebook.txt```.

Run jupyter notebooks thanks to ```jupyter notebook```.

### Python package
The Python package is included in ```python-package``` folder.

The designed of this folder should be followed by any Python package. That is:

- ```./pyproject.toml```
- ```./LICENSE```

- ```./src/iceflow/__init__.py```
- ```./src/iceflow/solver.py``` 
- ```./src/iceflow/tools.py```
        
- ```./README.md```
  
> [solver.py](scripts/solver.py) and [tools.py](scripts/tools.py) are modules.

- solver.py is the non-linear diffusion ice flow solver. It contains a visualisation procedure as well.
- tools.py are data generation classes and some tools functions.

### Create your own package

Please follow the steps explained in the [main presentation](materials/packaging_python.ipynb)

