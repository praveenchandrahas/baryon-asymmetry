"""Energy limits on photons from p-pbar annihilation at rest."""

M_P_MEV = 938.272


def max_observed_photon_energy_mev(y_emit):
    """Upper bound on today's photon energy for emission at y = 1 + z.

    Each photon carries at most half of the 2 m_p released.
    """
    return M_P_MEV / y_emit
