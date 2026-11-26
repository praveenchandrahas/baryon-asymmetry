from bau.kinematics import max_observed_photon_energy_mev


def test_signal_lies_below_fermi_lat_diffuse_band():
    assert max_observed_photon_energy_mev(20) < 100
