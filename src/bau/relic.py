"""Nucleon freeze-out with zero net baryon number (the H1 baseline).

Assumes uniform mixing, a constant <sigma v> = c / m_pi^2 and constant g*.
Natural units, GeV.
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.special import kve

M_N = 0.9389            # nucleon mass
M_PI = 0.138
M_PL = 1.22089e19
G_N = 4                 # p, n times two spins; antiparticles counted separately
G_STAR = 10.75
ETA_OBS = 6.12e-10      # observed n_b / n_gamma today
S_PER_PHOTON = 7.04     # entropy density / photon density today


def entropy_density(T, g_star=G_STAR):
    return 2 * np.pi**2 / 45 * g_star * T**3


def hubble(T, g_star=G_STAR):
    return 1.66 * np.sqrt(g_star) * T**2 / M_PL


def y_eq(T, g_star=G_STAR):
    """Equilibrium n_b / s (zero chemical potential, non-relativistic nucleons)."""
    x = M_N / T
    n = G_N * M_N**3 / (2 * np.pi**2) * kve(2, x) * np.exp(-x) / x
    return n / entropy_density(T, g_star)


def relic_yield(c=1.0, g_star=G_STAR, x_start=15.0, x_end=2000.0, rtol=1e-8):
    """Relic n_b / s from the Boltzmann equation."""
    sigma_v = c / M_PI**2

    def rhs(x, y):
        T = M_N / x
        rate = entropy_density(T, g_star) * sigma_v / (hubble(T, g_star) * x)
        return -rate * (y**2 - y_eq(T, g_star) ** 2)

    sol = solve_ivp(rhs, (x_start, x_end), [y_eq(M_N / x_start, g_star)],
                    method="Radau", rtol=rtol, atol=1e-30)
    if not sol.success:
        raise RuntimeError(sol.message)
    return sol.y[0, -1]


def relic_eta(c=1.0, **kwargs):
    """Relic n_b / n_gamma today (antinucleons are equally abundant)."""
    return S_PER_PHOTON * relic_yield(c, **kwargs)


def separation_deadline():
    """Temperature (GeV) where equilibrium n_b/s equals the observed value."""
    return brentq(lambda T: y_eq(T) - ETA_OBS / S_PER_PHOTON, 0.02, 0.1)


def comoving_hubble_radius_pc(T, g_star=G_STAR):
    """Present-day size, in parsec, of the Hubble radius at temperature T."""
    hbar_c = 1.97327e-16                 # GeV m
    parsec = 3.0857e16                   # m
    t0 = 2.3487e-13                      # CMB temperature today, GeV
    g_s0 = 3.909
    expansion = T / t0 * (g_star / g_s0) ** (1 / 3)
    return hbar_c / hubble(T, g_star) * expansion / parsec


def main():
    for c in (1, 2, 3):
        eta = relic_eta(c)
        print(f"c={c}: n_b/n_gamma={eta:.2e}  shortfall={ETA_OBS / eta:.1e}")
    T = separation_deadline()
    print(f"separation must act above T = {T * 1e3:.1f} MeV")
    print(f"comoving Hubble radius there = {comoving_hubble_radius_pc(T):.1f} pc")


if __name__ == "__main__":
    main()
