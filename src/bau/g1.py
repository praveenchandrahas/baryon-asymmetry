"""G1a: does the flux integral with CDG's own J(y) reproduce their Fig. 5?"""
import numpy as np

from bau.flux import flux, load
from bau.spectrum import PhotonSpectrum

ENERGIES = np.array([2.0, 3.0, 5.0, 7.0, 10.0])


def published(d0, E):
    ee, ff = load(f"cdg_fig5_d{d0}.csv")
    return np.exp(np.interp(np.log(E), np.log(ee), np.log(ff)))


def ratios(d0, k=2.0, **kwargs):
    """Ours / published at the pre-registered energies."""
    return flux(ENERGIES, d0, PhotonSpectrum(k), **kwargs) / published(d0, ENERGIES)


def main():
    for k in (2.0, 1.0, 3.0):
        for d0 in (20, 1000):
            print(f"spectrum k={k:.0f} d0={d0:4d}: ours/CDG at {ENERGIES} MeV =",
                  np.round(ratios(d0, k), 2))
    gap = published(20, ENERGIES) / published(1000, ENERGIES)
    print("published upper/lower curve ratio (1/d0 predicts 50):", np.round(gap, 1))


if __name__ == "__main__":
    main()
