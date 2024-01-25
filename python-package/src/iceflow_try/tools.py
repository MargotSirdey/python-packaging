import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

"""
    create_data(nx, ny)

Generate the bedrock elevation `B` and the equilibrium line altitude `ELA` data for a given grid resolutions `nx, ny`.

The function returns `B, ELA, β, c, dx, dy`.
"""
def create_data(nx, ny):
    # physics
    lx = 250000
    ly = 200000  # domain size [m]
    B0 = 3500            # mean height [m]
    β = 0.01            # mass-balance slope (data)
    c = 2.0             # mass-balance limiter
    
    # numerics
    dx, dy = lx / nx, ly / ny
    
    # initial conditions (data)
    xc = np.arange(-lx / 2 + dx / 2, lx / 2 - dx / 2, dx)
    yc = np.arange(-ly / 2 + dy / 2, ly / 2 - dy / 2, dy)
    
    Xc, Yc = np.meshgrid(xc, yc)
    
    B = B0 * np.exp(-Xc**2 / 1e10 - Yc**2 / 1e9) + B0 * np.exp(-Xc**2 / 1e9 - (Yc - ly / 8)**2 / 1e10)
    ELA = 2150 + 900 * np.arctan(Yc / ly)
    
    return B, ELA, β, c, dx, dy, xc, yc


"""
    visualise(H, S, B, xc, yc)

Visualise bedrock and ice elevation.
"""
def visualise(H, S, B, xc, yc):
    S_v = np.copy(S)
    S_v[H <= 0.01] = np.nan
    fig = plt.figure(figsize=(100, 45))
    axs = fig.add_subplot(121, projection='3d')
    axs.set_xlabel("x [km]")
    axs.set_ylabel("y [km]")
    axs.set_zlabel("elevation [m]")
    xic, yic = np.meshgrid(xc, yc)
    axs.set_box_aspect((4, 4, 1))
    axs.view_init(azim=25)
    p1 = axs.plot_surface(xic / 1e3, yic / 1e3, B, rstride=1, cstride=1, cmap='viridis', edgecolor='none')
    p2 = axs.plot_surface(xic / 1e3, yic / 1e3, S_v, rstride=1, cstride=1, cmap='viridis', edgecolor='none')
    norm = mpl.colors.Normalize(vmin=0, vmax=6000)
    fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap='viridis'),
             ax=axs, orientation='vertical', label='H ice [m]', shrink=0.5)

    plt.tight_layout()
    plt.show()
