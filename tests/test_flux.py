import numpy as np
import pytest

from bau import flux, g1
from bau.spectrum import PhotonSpectrum


def test_spectrum_matches_quoted_numbers():
    E = np.linspace(0.5, 938, 40000)
    f = PhotonSpectrum()(E)
    assert f.sum() * (E[1] - E[0]) == pytest.approx(3.8, rel=1e-3)
    assert (E * f).sum() / f.sum() == pytest.approx(180, rel=1e-3)
    assert 50 < E[f.argmax()] < 90


def test_cross_section_tends_to_thomson():
    assert flux.photon_cross_section(1e-4) == pytest.approx(flux.SIGMA_T, rel=1e-2)


def test_scales_as_inverse_domain_size():
    s = PhotonSpectrum()
    assert flux.flux(5.0, 20, s) / flux.flux(5.0, 1000, s) == pytest.approx(50, rel=1e-2)


@pytest.mark.parametrize("d0", [20, 1000])
def test_g1a_within_factor_1_5(d0):
    r = g1.ratios(d0)
    assert np.all((r > 1 / 1.5) & (r < 1.5))
