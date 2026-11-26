import numpy as np
import pytest

from bau import conservative as c


def test_data_upper_envelope():
    assert c.obs_upper(5.0) == pytest.approx(1.45e-4)
    assert c.obs_upper(2.0) > 1.45e-4 * (2 / 5) ** -2.4
    assert c.obs_upper(10.0) > 1.45e-4 * 2.0 ** -2.4


def test_least_favourable_rate_still_exceeds_data():
    """The run with the lowest J over much of the range must give the same
    verdict as the committed result."""
    J = c.solve(1, "H1 uniform heating", c.MODERN)
    assert c.R(J, 1000) > 3
