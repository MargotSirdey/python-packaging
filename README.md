# About
This repository contains a Python packaging course which takes place on the 20th of February, 2024.

> **Note:** The Julia packaging course is available here: [julia-packaging](https://github.com/Unil-SGC/julia-packaging).

### Jupyter notebooks
Several level of notebooks are designed here. The different steps show how one should proceed to create Python scripts from an existing jupyter notebook.
- [visualize_iceflow_1.ipynb](materials/visualize_iceflow_1.ipynb) is a bad written juypter notebook.
- [visualize_iceflow_functions_2.ipynb](materials/visualize_iceflow_functions_2.ipynb) is composed of functions.
- [visualize_iceflow_class_3.ipynb](materials/visualize_iceflow_class_3.ipynb) is using some classes to include parameters easily.
- [visualize_iceflow_class_3.py](materials/visualize_iceflow_class_3.py) is the conversion of the previous notebook to a Python script, thanks to ```jupyter nbconvert --to python``` command line.
- [final_script.py](materials/final_script.py) is the improved Python script one could obtain from the first jupyter notebook.

### Run slides

To open jupyter notebooks, create a Python virtual environment and actiavte it: ```python -m venv .venv``` ```source .venv/bin/activate```.

Install requirements: ```pip install -r requirements_jupyter_notebook.txt```.

Run jupyter notebooks: ```jupyter notebook```.

### Python package
The Python package is included in ```python-package``` folder.

The design of this folder should be followed by any Python package. That is:

- ```./pyproject.toml```
- ```./LICENSE```

- ```./src/iceflow/__init__.py```
- ```./src/iceflow/solver.py``` 
- ```./src/iceflow/tools.py```
        
- ```./README.md```

where
>  ```iceflow``` is the package name,
> ```pyproject.toml``` is the meta data file to design the package,
> ```LICENSE``` and ```README.md``` should be filled in by the designer of the package,
> ```__init__.py``` is the Python script called when importing ```iceflow``` package,
> [solver.py](scripts/iceflow/solver.py) and [tools.py](scripts/iceflow/tools.py) are modules.

- solver.py is the non-linear diffusion ice flow solver. It contains a visualisation procedure as well.
- tools.py are data generation classes and some tools functions.

### Create your own package

Follow the steps in the [main presentation](materials/packaging_python.ipynb).
This presentation has some introduction slides to explain on what one should focus on prior to create a Python package.

Some examples:

- Does it make sense to package your code?

- Is your code high quality enough? (documentation, license, well-designed...)

- Should data be included or accessible out of the code?
