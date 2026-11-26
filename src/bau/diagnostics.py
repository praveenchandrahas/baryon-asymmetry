"""Run the G1b diagnostics listed in docs/diagnostics.md."""
import numpy as np

from bau.flux import load
from bau.fluid import Flow, isothermal_test
from bau.g1b import Y

BASE = dict(cells=150, x_first=3e18)
VARIANTS = {
    "baseline": {},
    "H1 uniform heating": dict(heat_profile="uniform"),
    "H2 a=20": dict(a_ev_mpc=20.0),
    "B1 speed x0.5": dict(boundary_speed=0.5),
    "B2 speed x0.775": dict(boundary_speed=0.775),
    "B3 speed x2": dict(boundary_speed=2.0),
    "E1 no Hubble drag": dict(hubble_drag=False),
    "N1 40 cells": dict(cells=40, x_first=3e18 * 150 / 40),
    "N2 20 cells": dict(cells=20, x_first=3e18 * 150 / 20),
}


def ratios(**kwargs):
    """(J / Figure 3, far-field T / Figure 2) at the criterion redshifts."""
    y, J, T, _ = Flow(**{**BASE, **kwargs}).solve()
    o = np.argsort(y)
    ly = np.log(y[o])
    yj, jj = load("cdg_fig3_J.csv")
    yt, tt = load("cdg_fig2_T.csv")
    mine = np.exp(np.interp(np.log(Y), ly, np.log(J[o])))
    pub = np.exp(np.interp(np.log(Y), np.log(yj), np.log(jj)))
    return mine / pub, np.interp(Y, y[o], T[o]) / np.interp(Y, yt, tt)


def main():
    for kappa in (1, 2):
        for speed in (0.775, 1.0, 2.0):
            r = isothermal_test(kappa=kappa, boundary_speed=speed)
            print(f"V0 kappa={kappa} boundary x{speed}: J/(n c_iso/e) = {r:.3f}")
    print("y =", Y.astype(int))
    for kappa in (1, 2):
        for name, kw in VARIANTS.items():
            j, t = ratios(kappa=kappa, **kw)
            ok = np.all(np.abs(np.log(j)) < np.log(1.5)) and np.all(
                np.abs(np.log(t)) < np.log(1.5))
            print(f"kappa={kappa} {name:20s} J {np.round(j, 2)}  T {np.round(t, 2)}"
                  f"  {'MEETS' if ok else 'does not meet'}", flush=True)


if __name__ == "__main__":
    main()
