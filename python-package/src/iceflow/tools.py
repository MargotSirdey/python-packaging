import numpy as np


# Wrapper class for data grid resolutions `nx, ny`
class Data:
    def __init__(self, nx, lx, ny, ly):
        self.lx = lx
        self.ly = ly
        self.dx = lx / nx
        self.dy = ly / ny
        self.xc = np.arange(-lx / 2 + self.dx / 2,
                            lx / 2 - self.dx / 2, self.dx)
        self.yc = np.arange(-ly / 2 + self.dy / 2,
                            ly / 2 - self.dy / 2, self.dy)
        self.Xc, self.Yc = np.meshgrid(self.xc, self.yc)

class Physics:
    def __init__(self, m_h, m_b_slope, m_b, ρg, data):
        self.mean_height = m_h
        self.m_balance_slope = m_b_slope
        self.m_balance = m_b
        self.ρg = ρg
        self.B = bedrock_elevation(data, self.mean_height)
        self.ELA = equilibrium_line_altitude(data)


# Generate the bedrock elevation for a given grid resolutions `nx, ny`
def bedrock_elevation(data, mean_height):
    result = mean_height * np.exp(-data.Xc ** 2 / 1e10 - data.Yc ** 2 / 1e9)
    result += mean_height * np.exp(-data.Xc ** 2 / 1e9 -
                                   (data.Yc - data.ly / 8) ** 2 / 1e10)
    return result


# equilibrium line altitude `ELA` data for a given grid resolutions `nx, ny`
def equilibrium_line_altitude(data):
    return 2150 + 900 * np.arctan(data.Yc / data.ly)


def av(A):
    return 0.25 * (A[:-1, :-1] + A[:-1, 1:] + A[1:, :-1] + A[1:, 1:])


def avx(A):
    return 0.5 * (A[:-1, :] + A[1:, :])


def avy(A):
    return 0.5 * (A[:, :-1] + A[:, 1:])


def compute_D(D, H, S, dSdx, dSdy, Snorm, a1, a2, dx, dy):
    dSdx = np.diff(S, axis=0) / dx
    dSdy = np.diff(S, axis=1) / dy
    Snorm = np.sqrt(avy(dSdx) ** 2 + avx(dSdy) ** 2)
    D[:] = ((a1 * av(H) ** 5) + (a2 * av(H) ** 3)) * Snorm**2
