import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

# Wrapper class for data grid resolutions `nx, ny`
class Data:
    def __init__(self, nx, lx, ny, ly):
        self.lx = lx
        self.ly = ly
        self.dx = lx / nx
        self.dy = ly / ny
        self.xc = np.arange(-lx / 2 + self.dx / 2, lx / 2 - self.dx / 2, self.dx)
        self.yc = np.arange(-ly / 2 + self.dy / 2, ly / 2 - self.dy / 2, self.dy)
        self.Xc, self.Yc = np.meshgrid(self.xc, self.yc)


# Generate the bedrock elevation for a given grid resolutions `nx, ny`
def bedrock_elevation(data, mean_height):
    result = mean_height * np.exp(-data.Xc ** 2 / 1e10 - data.Yc ** 2 / 1e9)
    result += mean_height * np.exp(-data.Xc ** 2 / 1e9 - (data.Yc - data.ly / 8) ** 2 / 1e10)
    return result


# equilibrium line altitude `ELA` data for a given grid resolutions `nx, ny`
def eq_line_altitude(data):
    return 2150 + 900 * np.arctan(data.Yc / data.ly)

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
