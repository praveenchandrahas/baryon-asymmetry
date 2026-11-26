"""Semi-analytic check of the flux with expansion and a rising sound speed.

Isothermal flow into an absorbing wall in a matter-dominated universe
(a ~ t^(2/3), H = 2/(3t)) with sound speed c ~ t^b, no CBR drag. With
xi = (proper distance)/(c t), peculiar velocity v = c u(xi), n/n_far = N(xi), m = b + 1/3:

    (b + 2/3) u + (u - m xi) u' + N'/N = 0
    (u - m xi) N'/N + u' = 0

The disturbance front is at xi = 1/m (u = 0, N = 1). Near it u = -(b/2) s with
s = 1/m - xi, but that is only the leading term of a one-parameter family; the
member that applies is the one that is sonic at the wall, u(0) = -1. Continuity
then integrates to  J / (n c) = 1 - m * integral_0^{1/m} N dxi.
No code is shared with fluid.py or godunov.py.
"""
import numpy as np
from scipy.integrate import solve_ivp


def _shoot(b, delta, s0=1e-4):
    """Integrate from the front with initial slope b/2 + delta."""
    m = b + 1 / 3
    front = 1 / m

    def rhs(xi, y):
        u, lnN, _ = y
        w = u - m * xi
        L = -(b + 2 / 3) * u / max(1 - w * w, 1e-12)
        return [-w * L, L, np.exp(lnN)]

    def choked(xi, y):                     # w has returned to -1
        return 1 - (y[0] - m * xi) ** 2 - 1e-7

    choked.terminal, choked.direction = True, -1
    slope = b / 2 + delta
    y0 = [-slope * s0, -slope * s0, 0.0]
    return solve_ivp(rhs, (front - s0, 0.0), y0, method="Radau", rtol=1e-9,
                     atol=1e-12, events=choked)


def flux_coefficient(b, s0=1e-4, iterations=60):
    """J / (n_far c) for b > 0."""
    m = b + 1 / 3
    lo, hi = 0.0, m - b / 2 - 1e-6       # lo: reaches the wall subsonic
    for _ in range(iterations):
        mid = 0.5 * (lo + hi)
        sol = _shoot(b, mid, s0)
        if sol.status == 0:              # got to xi = 0 without choking
            lo = mid
        else:
            hi = mid
    sol = _shoot(b, lo, s0)
    integral = -sol.y[2, -1] + s0
    return 1 - m * integral, sol.y[0, -1]
