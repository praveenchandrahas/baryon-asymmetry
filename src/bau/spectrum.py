"""Model photon spectrum per p-pbar annihilation at rest.

CDG used measured spectra (their ref. 20). This is a stand-in built only from the
numbers CDG quote: mean multiplicity 3.8, peak near 70 MeV, mean near 180 MeV.
Photons are taken to come from pi0 decay, each pi0 giving a flat photon
spectrum between E_pi(1 -/+ beta)/2, with f(E_pi) ~ p^k exp(-E_pi/T).
"""
import numpy as np
from scipy.integrate import trapezoid
from scipy.optimize import brentq

M_PI0 = 134.977      # MeV
E_PI_MAX = 938.272
MULTIPLICITY = 3.8
MEAN_PHOTON_MEV = 180.0


class PhotonSpectrum:
    def __init__(self, k=2.0, n=6000):
        self.e_pi = np.linspace(M_PI0, E_PI_MAX, n)[1:]
        self.p = np.sqrt(self.e_pi**2 - M_PI0**2)
        # mean photon energy is half the mean pion energy
        self.temperature = brentq(
            lambda T: self._mean_pion(k, T) - 2 * MEAN_PHOTON_MEV, 20, 3000)
        f = self._weights(k, self.temperature)
        f /= trapezoid(f, self.e_pi)
        integrand = f / self.p
        steps = 0.5 * (integrand[1:] + integrand[:-1]) * np.diff(self.e_pi)
        # tail[i] = integral of f/p from e_pi[i] to the end point
        self.tail = np.append(np.cumsum(steps[::-1])[::-1], 0.0)

    def _weights(self, k, T):
        return self.p**k * np.exp(-(self.e_pi - M_PI0) / T)

    def _mean_pion(self, k, T):
        f = self._weights(k, T)
        return trapezoid(f * self.e_pi, self.e_pi) / trapezoid(f, self.e_pi)

    def __call__(self, E):
        """dN/dE in photons per MeV per annihilation."""
        E = np.asarray(E, dtype=float)
        e_min = E + M_PI0**2 / (4 * E)
        return MULTIPLICITY * np.interp(e_min, self.e_pi, self.tail, right=0.0)
