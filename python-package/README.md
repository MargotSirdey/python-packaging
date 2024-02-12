# About
### Python scripts
[solver.py](scripts/solver.py) and [tools.py](scripts/tools.py) are modules.

solver.py is the non-linear diffusion ice flow solver.

tools.py are visualization and data generation functions.

### Jupyter notebooks
[visualize_iceflow.ipynb](scripts/visualize_iceflow.ipynb) is a bad written juypter notebook.

[visualize_iceflow_functions.ipynb](scripts/visualize_iceflow_functions.ipynb) is composed of functions.

# Installation
Create a python virtual environment and install packages with ```pip install numpy matplotlib```.

# Run the code

```python
import iceflow

resol = 256
domain_size_y = 200000 # domain size [m]
domain_size_x = 250000 # domain size [m]
m_balance_slope = 0.01
m_balance_limiter = 2.0
mean_height = 3500 # mean height [m]
data = iceflow.tools.Data(resol, resol, domain_size_x, domain_size_y)
H, S = iceflow.solver(m_balance_slope, m_balance_limiter, mean_height, data)
iceflow.visualise  (H, S, iceflow.tools.bedrock_elevation(data, mean_height), data.xc, data.yc)
```
