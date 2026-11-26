"""Independent check of fluid.py: explicit conservative finite volumes (HLL).

Same physics, different discretisation and boundary treatment (exact flux of
the Riemann problem against vacuum). Meant for y <= 400, where CBR drag is weak.
"""
import numpy as np

from bau.fluid import (C, G_BAR, M_E, M_P, MPC_CM, SIGMA_T, T_GAMMA0, U_GAMMA0,
                       Flow)

GAMMA = 5 / 3


def vacuum_flux(n, u, a):
    """State (n, u, a) to the right of vacuum; returns (n*, u*, a*) at x = 0."""
    w = -u                                   # speed towards the interface
    if w >= a:
        return n, u, a
    a_s = max((2 * a + (GAMMA - 1) * w) / (GAMMA + 1), 0.0)
    return n * (a_s / a) ** (2 / (GAMMA - 1)), -a_s, a_s


def run(kappa=1.0, y_start=400.0, y_out=(100, 40, 20), cells=400, x_max=1e24,
        x_first=2e19, cfl=0.4):
    f = Flow(kappa=kappa, cells=cells, x_first=x_first, x_max=x_max)
    dx, M = f.dx, f.M
    k = kappa / M_P * C**2                   # p/n = k T  (cm^2 s^-2)
    N = np.ones(M)                           # comoving density / n0
    v = np.zeros(M)
    T = np.full(M, T_GAMMA0 * y_start)
    y, out = y_start, {}
    targets = sorted(y_out, reverse=True)
    while targets:
        a = np.sqrt(GAMMA * k * T)
        H = f.hubble(y)
        dt = cfl * np.min(dx / y / (np.abs(v) + a))
        dt = min(dt, 0.005 / H, (1 - targets[0] / y) / (1.5 * H) + 1e3)
        nb, ub, ab = vacuum_flux(N[0], v[0], a[0])
        J = f.n0 * y**3 * nb * max(-ub, 0.0)

        # conservative variables and fluxes
        E = N * k * T / (GAMMA - 1) + 0.5 * N * v**2
        U = np.array([N, N * v, E])
        P = N * k * T
        F = np.array([N * v, N * v**2 + P, (E + P) * v])
        sl = np.minimum(v[:-1] - a[:-1], v[1:] - a[1:])
        sr = np.maximum(v[:-1] + a[:-1], v[1:] + a[1:])
        sl, sr = np.minimum(sl, 0), np.maximum(sr, 0)
        mid = (sr * F[:, :-1] - sl * F[:, 1:] + sl * sr * (U[:, 1:] - U[:, :-1])) / (sr - sl)
        pb = nb * ab**2 / GAMMA
        left = np.array([nb * ub, nb * ub**2 + pb,
                         (pb / (GAMMA - 1) + 0.5 * nb * ub**2 + pb) * ub])
        flux = np.column_stack([left, mid, F[:, -1]])
        U = U - dt * y * np.diff(flux, axis=1) / dx

        N = U[0]
        v = U[1] / N
        T = (U[2] - 0.5 * N * v**2) * (GAMMA - 1) / (N * k)

        # sources
        u_g = U_GAMMA0 * y**4
        nu = 4 / 3 * SIGMA_T * u_g * C / M_P
        k_c = 4 / 3 * SIGMA_T * u_g * C / M_E
        v *= np.exp(-(H + nu) * dt)
        rate = 2 * H + k_c
        T_eq = (k_c * T_GAMMA0 * y + G_BAR * J * f.a / (6 * f.n0 * MPC_CM)) / rate
        T = T_eq + (T - T_eq) * np.exp(-rate * dt)

        y *= np.exp(-H * dt)
        if y <= targets[0] * (1 + 1e-9):
            out[targets.pop(0)] = (J, T[-1])
    return out
