import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from . import tools

def solver(m_balance_slope, m_balance_limiter, mean_height, data):
    # physics
    ρg = 910.0 * 9.81    # ice density x gravity
    dt = 0.1             # time step [yr]
    # numerics
    B = tools.bedrock_elevation(data, mean_height)
    ELA = tools.eq_line_altitude(data)
    nx, ny = B.shape      # numerical grid resolution
    nt = 1e4              # number of time steps
    nout = 1e3            # visu and error checking interval
    ϵ = 1e-4             # steady state tolerance
    # preprocess
    a1 = 1.9e-24 * pow(ρg,3) * 31557600
    a2 = 5.7e-20 * pow(ρg,3) * 31557600
    # initialise
    S = np.zeros((nx, ny))#,np.float128)
    dSdx = np.zeros((nx-1, ny))#,np.float128)
    dSdy = np.zeros((nx, ny-1))#,np.float128)
    Snorm = np.zeros((nx-1, ny-1))#,np.float128)
    D = np.zeros((nx-1, ny-1))#,np.float128)
    qx = np.zeros((nx-1, ny-2))#,np.float128)
    qy = np.zeros((nx-2, ny-1))#,np.float128)
    H = np.zeros((nx, ny))#,np.float128)
    M = np.zeros((nx, ny))#,np.float128)
    H0 = np.zeros((nx, ny))#,np.float128)
    # time loop
    for it in range(int(nt)):
        np.copyto(H0, H)
        S = B + H
        M = np.minimum(m_balance_slope * (S - ELA), m_balance_limiter)
        tools.compute_D(D, H, S, dSdx, dSdy, Snorm, a1, a2, data.dx, data.dy)
        qx[:] = tools.avy(D) * np.diff(S[:, 1:-1], axis=0) / data.dx
        qy[:] = tools.avx(D) * np.diff(S[1:-1, :], axis=1) / data.dy
        H[1:-1, 1:-1] = np.maximum(H[1:-1, 1:-1] + dt * (np.diff(qx, axis=0) + np.diff(qy, axis=1) + M[1:-1, 1:-1]), 0.0)
        if it % nout == 0:
            # error checking
            #print(H[2,3:10])
            err = np.max(np.abs(H - H0))
            print(f"it = {it}, err = {err:.3e}")
            if err < ϵ:
                break
    return H, S
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



