"""Lowest-flux comparison with COMPTEL, current cosmology.

Rules: "Conservative comparison" in docs/criteria.md.
"""
import numpy as np

from bau.diagnostics import BASE, VARIANTS
from bau.flux import CDG_1998, cdg_J, flux
from bau.fluid import Flow
from bau.g1 import ENERGIES
from bau.spectrum import PhotonSpectrum

H = 0.6736
OMEGA_R = 4.18e-5 / H**2
MODERN = dict(h=H, omega_m=0.3153, omega_l=1 - 0.3153 - OMEGA_R,
              omega_r=OMEGA_R, eta=6.12e-10)
D0 = (20, 1000)


def obs_upper(E):
    """COMPTEL power-law fit plus 2 sigma, in photons / (cm^2 s sr MeV)."""
    x = np.asarray(E, dtype=float) / 5
    return 1.45e-4 * np.maximum(x**-2.8, x**-2.0)


def solve(kappa, variant, cosmology):
    """J on a log grid of y for one solver variant."""
    kw = {**BASE, **VARIANTS[variant], "kappa": kappa, **cosmology}
    a = VARIANTS[variant].get("a_ev_mpc", 10.0)
    kw["a_ev_mpc"] = a * cosmology["eta"] / CDG_1998["eta"]    # CDG eq. 30
    y, J, _, sol = Flow(**kw).solve()
    if not sol.success:
        raise RuntimeError(f"{kappa} {variant}: {sol.message}")
    o = np.argsort(y)
    return lambda yy: np.exp(np.interp(np.log(yy), np.log(y[o]), np.log(J[o])))


def all_rates():
    """{name: J(y)} under current cosmology, for every run in the rules."""
    grid = np.exp(np.linspace(np.log(20), np.log(1100), 400))
    out = {}
    for kappa in (1, 2):
        for name in VARIANTS:
            new = solve(kappa, name, MODERN)(grid)
            old = solve(kappa, name, CDG_1998)(grid)
            out[f"ours k{kappa} {name}"] = new
            out[f"CDG x ratio k{kappa} {name}"] = cdg_J(grid) * new / old
    return grid, out


def as_function(grid, values):
    return lambda yy: np.exp(np.interp(np.log(yy), np.log(grid), np.log(values)))


def predicted(J, d0):
    """Smallest flux over the three photon-spectrum shapes."""
    return np.min([flux(ENERGIES, d0, PhotonSpectrum(k), J=J, **MODERN)
                   for k in (1.0, 2.0, 3.0)], axis=0)


def R(J, d0):
    return np.max(predicted(J, d0) / obs_upper(ENERGIES))


def verdict(r):
    return "excluded" if r > 3 else "inconclusive"


def main():
    grid, rates = all_rates()
    stack = np.array(list(rates.values()))
    names = list(rates)
    lowest = as_function(grid, stack.min(axis=0))
    print("lowest J comes from:",
          sorted({names[i] for i in stack.argmin(axis=0)}))
    for d0 in D0:
        r = R(lowest, d0)
        print(f"VERDICT d0={d0:4d} Mpc: R={r:.2f} -> {verdict(r)}; "
              f"d_excl={d0 * r / 3:.0f} Mpc")
        print("  predicted/(obs+2sigma) at", ENERGIES, "MeV:",
              np.round(predicted(lowest, d0) / obs_upper(ENERGIES), 2))
    print("\nfor comparison only (not verdict-bearing), d_excl in Mpc:")
    ref = {"judged run (ours k1 baseline)": "ours k1 baseline",
           "ours k2 baseline": "ours k2 baseline",
           "CDG J x ratio, k1 baseline": "CDG x ratio k1 baseline",
           "ours k1 H1 uniform heating": "ours k1 H1 uniform heating"}
    for label, key in ref.items():
        J = as_function(grid, rates[key])
        print(f"  {label:32s} R(20)={R(J, 20):7.1f} R(1000)={R(J, 1000):6.2f} "
              f"d_excl={1000 * R(J, 1000) / 3:.0f}")


if __name__ == "__main__":
    main()
