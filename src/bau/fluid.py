"""One-dimensional flow into a matter-antimatter interface (CDG eqs. 1-3).

The interface (x = 0) is a perfect absorber: flow leaves it at the local sound
speed, which covers both sonic outflow into vacuum and, with strong drag, the
diffusive regime. Staggered grid in comoving x; time variable is -ln y.

pressure p = kappa * n * T (n = proton density, T in eV), heat capacity 3nT,
adiabatic index 5/3. See docs/criteria.md for the choice of kappa.
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.sparse import lil_matrix

C = 2.99792458e10          # cm/s
M_P = 938.272e6            # eV
M_E = 0.5109989e6          # eV
SIGMA_T = 6.6524587e-25    # cm^2
U_GAMMA0 = 0.2606          # CMB energy density today, eV/cm^3
T_GAMMA0 = 2.3487e-4       # CMB temperature today, eV
N_GAMMA0 = 410.7           # cm^-3
MPC_CM = 3.0857e24
G_BAR = 3.8                # annihilation electrons per annihilation


class Flow:
    def __init__(self, kappa=1.0, eta=2e-10, h=0.75, omega_m=1.0, omega_l=0.0,
                 a_ev_mpc=10.0, heating=True, drag=True, compton=True,
                 expansion=True, cells=150, x_first=3e18, x_max=1e24,
                 viscosity=1.0):
        self.kappa, self.n0 = kappa, eta * N_GAMMA0
        self.h, self.om, self.ol = h, omega_m, omega_l
        self.a = a_ev_mpc if heating else 0.0
        self.drag, self.compton, self.expansion = drag, compton, expansion
        self.viscosity = viscosity
        ratio = self._ratio(cells, x_first, x_max)
        self.dx = x_first * ratio ** np.arange(cells)
        self.centres = np.cumsum(self.dx) - 0.5 * self.dx
        self.M = cells

    @staticmethod
    def _ratio(cells, first, total):
        lo, hi = 1.0 + 1e-9, 2.0
        for _ in range(100):
            mid = 0.5 * (lo + hi)
            if first * (mid**cells - 1) / (mid - 1) > total:
                hi = mid
            else:
                lo = mid
        return lo

    def hubble(self, y):
        h0 = self.h * 100 / 3.0857e19
        return h0 * np.sqrt((1 - self.om - self.ol) * y**2 + self.om * y**3 + self.ol)

    def sound_speed(self, T):
        return C * np.sqrt(5 / 3 * self.kappa * np.maximum(T, 1e-8) / M_P)

    # state: for each cell i: ln(N_i/N0), T_i, velocity at its right edge
    def unpack(self, s):
        return s[0::3], s[1::3], s[2::3]

    def J(self, y, s):
        """Annihilations per cm^2 per s (one interface)."""
        lnN, T = s[0], s[1]
        return self.n0 * y**3 * np.exp(lnN) * self.sound_speed(T)

    def rhs(self, y, s):
        """Time derivative in physical time (per second) at redshift y."""
        lnN, T, v_r = self.unpack(s)
        M, dx = self.M, self.dx
        H = self.hubble(y) if self.expansion else 0.0
        u_g = U_GAMMA0 * y**4
        nu = 4 / 3 * SIGMA_T * u_g * C / M_P if self.drag else 0.0
        k_c = 4 / 3 * SIGMA_T * u_g * C / M_E if self.compton else 0.0
        N = np.exp(lnN)

        v = np.empty(M + 1)
        v[0] = -self.sound_speed(T[0])
        v[1:] = v_r
        v[M] = 0.0                                  # undisturbed far field

        # continuity (upwind fluxes)
        N_up = np.empty(M + 1)
        N_up[0], N_up[M] = N[0], N[-1]
        N_up[1:M] = np.where(v[1:M] > 0, N[:-1], N[1:])
        flux = N_up * v
        dlnN = -y * np.diff(flux) / (dx * N)

        # temperature
        div = y * np.diff(v) / dx
        v_c = 0.5 * (v[:-1] + v[1:])
        grad = np.diff(T) / (0.5 * (dx[:-1] + dx[1:]))
        left = np.concatenate(([0.0], grad))
        right = np.concatenate((grad, [0.0]))
        advect = y * v_c * np.where(v_c > 0, left, right)
        heat = G_BAR * self.J(y, s) * self.a / (6 * self.n0 * MPC_CM)
        dT = (-2 * H * T - advect - 2 / 3 * T * div
              + k_c * (T_GAMMA0 * y - T) + heat)

        # momentum at interior edges
        face = 0.5 * (dx[:-1] + dx[1:])
        p = N * T
        # artificial viscosity, compression only
        jump = np.diff(v)
        q = np.where(jump < 0, self.viscosity * N * jump**2, 0.0) * M_P / C**2
        total = self.kappa * p + q
        N_face = 0.5 * (N[:-1] + N[1:])
        force = -y * C**2 / M_P * np.diff(total) / (face * N_face)
        vi = v[1:M]
        gl = np.diff(v)[:-1] / dx[:-1]
        gr = np.diff(v)[1:] / dx[1:]
        adv_v = y * vi * np.where(vi > 0, gl, gr)
        dv = np.zeros(M)
        dv[:-1] = force - adv_v - (H + nu) * vi

        out = np.empty_like(s)
        out[0::3], out[1::3], out[2::3] = dlnN, dT, dv
        return out

    def sparsity(self):
        n = 3 * self.M
        S = lil_matrix((n, n))
        for i in range(n):
            S[i, max(0, i - 7):min(n, i + 8)] = 1
        S[1::3, 0] = 1          # heating depends on the first cell through J
        S[1::3, 1] = 1
        return S.tocsr()

    def initial(self, y):
        s = np.zeros(3 * self.M)
        s[1::3] = T_GAMMA0 * y
        return s

    def solve(self, y_start=1100.0, y_end=19.9, rtol=1e-5):
        """Integrate in -ln y. Returns (y, J, far-field T, solver result)."""
        def f(tau, s):
            y = np.exp(-tau)
            return self.rhs(y, s) / self.hubble(y)

        atol = np.tile([1e-6, 1e-7, 1.0], self.M)
        sol = solve_ivp(f, (-np.log(y_start), -np.log(y_end)),
                        self.initial(y_start), method="BDF", rtol=rtol,
                        atol=atol, jac_sparsity=self.sparsity())
        if not sol.success:
            raise RuntimeError(sol.message)
        y = np.exp(-sol.t)
        J = np.array([self.J(yy, sol.y[:, i]) for i, yy in enumerate(y)])
        return y, J, sol.y[3 * (self.M - 1) + 1], sol


def vacuum_test(cells=200, T=1.0, kappa=1.0):
    """Static gas flowing into vacuum; returns J / ((3/4)^4 n c_s)."""
    flow = Flow(kappa=kappa, heating=False, drag=False, compton=False,
                expansion=False, cells=cells, x_first=1e17, x_max=1e22)
    y = 1.0
    c = flow.sound_speed(T)
    t_end = 1e21 / c
    s0 = flow.initial(y)
    s0[1::3] = T
    sol = solve_ivp(lambda t, s: flow.rhs(y, s), (0, t_end), s0, method="BDF",
                    rtol=1e-6, atol=np.tile([1e-7, 1e-8, 1.0], cells),
                    jac_sparsity=flow.sparsity())
    return flow.J(y, sol.y[:, -1]) / ((3 / 4) ** 4 * flow.n0 * c)


def diffusion_test(cells=150, y_start=6000.0, y_check=1000.0, kappa=1.0):
    """Strong CBR drag, no heating; returns J / CDG eq. 7."""
    flow = Flow(kappa=kappa, heating=False, cells=cells, x_first=3e17, x_max=1e23)
    y, J, _, _ = flow.solve(y_start, y_check)
    yy = y[-1]
    t = 2 / (3 * flow.hubble(yy))
    nu = 4 / 3 * SIGMA_T * U_GAMMA0 * yy**4 * C / M_P
    D = kappa * T_GAMMA0 * yy / M_P * C**2 / nu
    return J[-1] / (flow.n0 * yy**3 * np.sqrt(5 * D / (3 * np.pi * t)))
