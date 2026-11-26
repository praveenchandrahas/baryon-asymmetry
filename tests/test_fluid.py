import numpy as np
import pytest
from scipy.integrate import solve_ivp

from bau import flux, fluid, godunov


@pytest.mark.parametrize("kappa", [1, 2])
def test_flux_into_vacuum(kappa):
    assert fluid.vacuum_test(kappa=kappa) == pytest.approx(1, abs=0.02)


def test_strong_drag_limit():
    # CDG eq. 7 holds when nu*t >> 1, which needs y well above recombination
    r = fluid.diffusion_test(y_start=96000, y_check=16000)
    assert r == pytest.approx(1, abs=0.05)


def test_heating_and_cooling_reproduce_figure_2():
    """Far-field temperature driven by CDG's own J must follow their Figure 2."""
    f = fluid.Flow()
    yt, Tt = flux.load("cdg_fig2_T.csv")

    def rhs(tau, T):
        y = np.exp(-tau)
        H = f.hubble(y)
        k_c = 4 / 3 * fluid.SIGMA_T * fluid.U_GAMMA0 * y**4 * fluid.C / fluid.M_E
        heat = fluid.G_BAR * flux.cdg_J(y) * f.a / (6 * f.n0 * fluid.MPC_CM)
        return (-2 * H * T + k_c * (fluid.T_GAMMA0 * y - T) + heat) / H

    y = np.array([20, 40, 100, 400, 1000.0])
    sol = solve_ivp(rhs, (-np.log(1100), -np.log(19.99)),
                    [fluid.T_GAMMA0 * 1100], method="Radau", rtol=1e-8,
                    dense_output=True)
    T = sol.sol(-np.log(y))[0]
    assert T == pytest.approx(np.interp(y, yt, Tt), rel=0.05)


def test_independent_solvers_agree():
    y, J, _, _ = fluid.Flow().solve(400, 19.9)
    other = godunov.run(cells=300, x_first=4e19)
    for yy, (j, _) in other.items():
        main = np.exp(np.interp(np.log(yy), np.log(y[::-1]), np.log(J[::-1])))
        assert j == pytest.approx(main, rel=0.03)
