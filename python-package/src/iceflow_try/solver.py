import numpy as np
from . import tools

def hello_world():
    print("Hello world !")

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

def iceflow_solver(B, ELA, β, c, dx, dy, xc, yc):
    # physics
    ρg = 910.0 * 9.81    # ice density x gravity
    dt = 0.1             # time step [yr]
    # numerics
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
        M = np.minimum(β * (S - ELA), c)
        compute_D(D, H, S, dSdx, dSdy, Snorm, a1, a2, dx, dy)
        qx[:] = avy(D) * np.diff(S[:, 1:-1], axis=0) / dx
        qy[:] = avx(D) * np.diff(S[1:-1, :], axis=1) / dy
        H[1:-1, 1:-1] = np.maximum(H[1:-1, 1:-1] + dt * (np.diff(qx, axis=0) + np.diff(qy, axis=1) + M[1:-1, 1:-1]), 0.0)
        if it % nout == 0:
            # error checking
            #print(H[2,3:10])
            err = np.max(np.abs(H - H0))
            print(f"it = {it}, err = {err:.3e}")
            if err < ϵ:
                break
    return H, S, B, xc, yc

if __name__ == "__main__":
    # run the code and visualize the output
    resol = 256
    tools.visualise(*iceflow_solver(*tools.create_data(resol, resol)))
