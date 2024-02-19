Run the code 

```python
    import iceflow

    resol = 256
    domainsizex = 250000
    domainsizey = 200000  # domain size [m]
    resol = 256
    data = iceflow.tools.Data(resol, domainsizex, resol, domainsizey)
    m_h = 3500
    m_b_slope = 0.01
    m_b = 2.0
    ρg = 910.0 * 9.81
    physics = iceflow.tools.Physics(m_h, m_b_slope, m_b, ρg, data)

    # numerics
    nx, ny = physics.B.shape      # numerical grid resolution
    nt = 1e4              # number of time steps
    nout = 1e3            # visu and error checking interval
    ϵ = 1e-4             # steady state tolerance
    dt = 0.1             # time step [yr]

    S, H = iceflow.solver(nx, ny, nt, nout, ϵ, dt, physics, data)

    iceflow.visualise(data, S, H, physics.B)
```
