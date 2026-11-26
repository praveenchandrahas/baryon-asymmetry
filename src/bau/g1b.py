"""G1b: is our own J(y) consistent with CDG Figure 3? (docs/criteria.md)"""
import numpy as np

from bau.flux import flux, load
from bau.fluid import Flow
from bau.g1 import ENERGIES, published
from bau.spectrum import PhotonSpectrum

Y = np.array([20, 25, 40, 100, 200, 400, 1000.0])


def solve(kappa, cells=300):
    """Return J(y) as a function, from our own solution."""
    y, J, _, _ = Flow(kappa=kappa, cells=cells,
                      x_first=3e18 * 150 / cells).solve()
    o = np.argsort(y)
    ly, lJ = np.log(y[o]), np.log(J[o])
    return lambda yy: np.exp(np.interp(np.log(yy), ly, lJ))


def main():
    yy, jj = load("cdg_fig3_J.csv")
    pub = np.exp(np.interp(np.log(Y), np.log(yy), np.log(jj)))
    for kappa, label in ((1, "judged run"), (2, "reported run")):
        J, coarse = solve(kappa), solve(kappa, 150)
        print(f"kappa={kappa} ({label})")
        print("  y                ", Y.astype(int))
        print("  J ours/CDG       ", np.round(J(Y) / pub, 2))
        print("  grid change      ", f"{np.max(np.abs(coarse(Y) / J(Y) - 1)):.1%}")
        for d0 in (20, 1000):
            r = flux(ENERGIES, d0, PhotonSpectrum(), J=J) / published(d0, ENERGIES)
            print(f"  flux ours/CDG d0={d0:4d}", np.round(r, 2), "at", ENERGIES, "MeV")


if __name__ == "__main__":
    main()
