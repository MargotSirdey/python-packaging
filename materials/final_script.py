#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl


class Data:
    def __init__(self, resolx, domainsizex, resoly, domainsizey):
        self.lx = domainsizex
        self.ly = domainsizey
        self.dx = domainsizex / resolx
        self.dy = domainsizey / resoly
        self.xc = np.arange(-domainsizex / 2 + self.dx / 2,
                            domainsizex / 2 - self.dx / 2, self.dx)
        self.yc = np.arange(-domainsizey / 2 + self.dy / 2,
                            domainsizey / 2 - self.dy / 2, self.dy)
        self.Xc, self.Yc = np.meshgrid(self.xc, self.yc)


class Physics:
    def __init__(self, m_h, m_b_slope, m_b, ρg, data):
        self.mean_height = m_h
        self.m_balance_slope = m_b_slope
        self.m_balance = m_b
        self.ρg = ρg
        self.B = bedrock_elevation(data, self.mean_height)
        self.ELA = equilibrium_line_altitude(data)


def bedrock_elevation(data, mean_height):
    B = mean_height * np.exp(-data.Xc**2 / 1e10 - data.Yc**2 / 1e9)
    B += mean_height * np.exp(-data.Xc**2 / 1e9 -
                              (data.Yc - data.ly / 8)**2 / 1e10)
    return B


def equilibrium_line_altitude(data):
    ELA = 2150 + 900 * np.arctan(data.Yc / data.ly)
    return ELA


def av(A):
    return 0.25 * (A[:-1, :-1] + A[:-1, 1:] + A[1:, :-1] + A[1:, 1:])


def avx(A):
    return 0.5 * (A[:-1, :] + A[1:, :])


def avy(A):
    return 0.5 * (A[:, :-1] + A[:, 1:])


def compute_D(D, H, S, dSdx, dSdy, Snorm, a1, a2, data):
    dSdx = np.diff(S, axis=0) / data.dx
    dSdy = np.diff(S, axis=1) / data.dy
    Snorm = np.sqrt(avy(dSdx)**2 + avx(dSdy)**2)
    D[:] = ((a1 * av(H)**5) + (a2 * av(H)**3)) * Snorm**2


# Visualize bedrock and ice elevation
def visualise(data, S, H, B):
    S_v = np.copy(S)
    S_v[H <= 0.01] = np.nan
    fig = plt.figure(figsize=(20, 12))
    axs = fig.add_subplot(121, projection='3d')
    axs.set_xlabel("x [km]")
    axs.set_ylabel("y [km]")
    axs.set_zlabel("elevation [m]")
    xic, yic = np.meshgrid(data.xc, data.yc)
    axs.set_box_aspect((4, 4, 1))
    axs.view_init(azim=25)
    axs.plot_surface(xic / 1e3, yic / 1e3, B, rstride=1, cstride=1,
                          cmap='viridis', edgecolor='none')
    axs.plot_surface(xic / 1e3, yic / 1e3, S_v, rstride=1, cstride=1,
                          cmap='viridis', edgecolor='none')
    norm = mpl.colors.Normalize(vmin=0, vmax=6000)
    fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap='viridis'),
                 ax=axs, orientation='vertical', label='H ice [m]', shrink=0.5)
    plt.tight_layout()
    plt.show()


def solver(nx, ny, nt, nout, ϵ, dt, physics, data):
    # preprocess
    a1 = 1.9e-24 * pow(physics.ρg, 3) * 31557600
    a2 = 5.7e-20 * pow(physics.ρg, 3) * 31557600

    # initialize
    S = np.zeros((nx, ny))
    dSdx = np.zeros((nx-1, ny))
    dSdy = np.zeros((nx, ny-1))
    Snorm = np.zeros((nx-1, ny-1))
    D = np.zeros((nx-1, ny-1))
    qx = np.zeros((nx-1, ny-2))
    qy = np.zeros((nx-2, ny-1))
    H = np.zeros((nx, ny))
    M = np.zeros((nx, ny))
    H0 = np.zeros((nx, ny))

    # time loop
    for it in range(int(nt)):
        np.copyto(H0, H)
        S = physics.B + H
        M = np.minimum(physics.m_balance_slope *
                       (S - physics.ELA), physics.m_balance)
        compute_D(D, H, S, dSdx, dSdy, Snorm, a1, a2, data)
        qx[:] = avy(D) * np.diff(S[:, 1:-1], axis=0) / data.dx
        qy[:] = avx(D) * np.diff(S[1:-1, :], axis=1) / data.dy
        H[1:-1, 1:-1] = np.maximum(H[1:-1, 1:-1] + dt * (np.diff(qx, axis=0)
                                   + np.diff(qy, axis=1) + M[1:-1, 1:-1]), 0.0)
        if it % nout == 0:
            # error checking
            err = np.max(np.abs(H - H0))
            print(f"it = {it}, err = {err:.3e}")
            if err < ϵ:
                break
    return S, H


if (__name__ == "__main__"):
    domainsizex = 250000
    domainsizey = 200000  # domain size [m]
    resol = 256
    data = Data(resol, domainsizex, resol, domainsizey)
    m_h = 3500
    m_b_slope = 0.01
    m_b = 2.0
    ρg = 910.0 * 9.81
    physics = Physics(m_h, m_b_slope, m_b, ρg, data)

    # numerics
    nx, ny = physics.B.shape      # numerical grid resolution
    nt = 1e4              # number of time steps
    nout = 1e3            # visu and error checking interval
    ϵ = 1e-4             # steady state tolerance
    dt = 0.1             # time step [yr]

    S, H = solver(nx, ny, nt, nout, ϵ, dt, physics, data)

    visualise(data, S, H, physics.B)
