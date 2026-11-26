import pytest

from bau import relic


def test_matches_textbook_order_of_magnitude():
    # Standard result for a symmetric universe: n_b/n_gamma of order 1e-18.
    assert 2e-19 < relic.relic_eta(c=1) < 2e-18


def test_h1_criterion():
    for c in (1, 2, 3):
        assert relic.ETA_OBS / relic.relic_eta(c) > 100


def test_solver_converged():
    assert relic.relic_yield(rtol=1e-6) == pytest.approx(
        relic.relic_yield(rtol=1e-10), rel=1e-3)


def test_insensitive_to_end_point():
    assert relic.relic_yield(x_end=2000) == pytest.approx(
        relic.relic_yield(x_end=5000), rel=1e-2)


def test_separation_deadline():
    assert 0.035 < relic.separation_deadline() < 0.040
    assert 1.5 < relic.comoving_hubble_radius_pc(relic.separation_deadline()) < 3
