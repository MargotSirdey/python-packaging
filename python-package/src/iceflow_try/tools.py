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


    
def av(A):
    return 0.25 * (A[:-1, :-1] + A[:-1, 1:] + A[1:, :-1] + A[1:, 1:])

def avx(A):
    return 0.5 * (A[:-1, :] + A[1:, :])

def avy(A):
    return 0.5 * (A[:, :-1] + A[:, 1:])

def compute_D(D, H, S, dSdx, dSdy, Snorm, a1, a2, dx, dy):
    dSdx = np.diff(S, axis=0) / dx
    dSdy = np.diff(S, axis=1) / dy
    Snorm = np.sqrt(avy(dSdx)**2 + avx(dSdy)**2)
    D[:] = ((a1 * av(H)**5) + (a2 * av(H)**3)) * Snorm**2

