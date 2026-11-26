"""Diffuse photon flux from domain-boundary annihilation (CDG eqs. 12-14)."""
from pathlib import Path

import numpy as np
from scipy.integrate import cumulative_trapezoid, trapezoid

DATA = Path(__file__).resolve().parents[2] / "data"
C_CM_S = 2.99792458e10
MPC_CM = 3.0857e24
R_E_CM = 2.8179403e-13
SIGMA_T = 6.6524587e-25
ALPHA = 1 / 137.036
M_E_MEV = 0.5109989
N_GAMMA0 = 410.7          # CMB photons per cm^3 today
Y_MIN, Y_MAX = 20.0, 1100.0

CDG_1998 = dict(h=0.75, omega_m=1.0, omega_l=0.0, eta=2e-10)


def hubble(y, h, omega_m, omega_l):
    """H in 1/s (CDG eq. 15; no radiation term)."""
    h0 = h * 100 / 3.0857e19
    return h0 * np.sqrt((1 - omega_m - omega_l) * y**2 + omega_m * y**3 + omega_l)


def photon_cross_section(E):
    """Per electron: Klein-Nishina Compton plus unscreened pair production."""
    k = np.asarray(E, dtype=float) / M_E_MEV
    a = 1 + 2 * k
    kn = 0.75 * SIGMA_T * ((1 + k) / k**2 * (2 * (1 + k) / a - np.log(a) / k)
                           + np.log(a) / (2 * k) - (1 + 3 * k) / a**2)
    pair = ALPHA * R_E_CM**2 * (28 / 9 * np.log(2 * k) - 218 / 27)
    return kn + np.clip(pair, 0, None)


def load(name):
    return np.loadtxt(DATA / name, delimiter=",", skiprows=2).T


def cdg_J(y):
    """Annihilations per cm^2 per s, from CDG Fig. 3 (log-log interpolation)."""
    yy, jj = load("cdg_fig3_J.csv")
    return np.exp(np.interp(np.log(y), np.log(yy), np.log(jj)))


def flux(E_obs, d0_mpc, spectrum, J=cdg_J, h=0.75, omega_m=1.0, omega_l=0.0,
         eta=2e-10, n=3000, attenuate=True):
    """Photons / (cm^2 s MeV sr) today. J must belong to the same cosmology."""
    E_obs = np.atleast_1d(np.asarray(E_obs, dtype=float))
    ly = np.linspace(0.0, np.log(Y_MAX), n)
    y_all = np.exp(ly)
    y = np.exp(np.linspace(np.log(Y_MIN), np.log(Y_MAX), n))
    H = hubble(y, h, omega_m, omega_l)
    source = J(y) * y / (d0_mpc * MPC_CM)          # J / d(y)
    out = []
    for E in E_obs:
        if attenuate:
            g = (C_CM_S * photon_cross_section(E * y_all) * eta * N_GAMMA0
                 * y_all**3 / hubble(y_all, h, omega_m, omega_l))
            tau = np.interp(np.log(y), ly, cumulative_trapezoid(g, ly, initial=0))
        else:
            tau = 0.0
        # dy / y^3 = d(ln y) / y^2
        f = C_CM_S / (4 * np.pi) * source * spectrum(E * y) * np.exp(-tau) / (H * y**2)
        out.append(trapezoid(f, np.log(y)))
    return np.array(out)
