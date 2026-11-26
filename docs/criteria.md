# Pass/fail criteria

Written 26 November 2026, **before any gamma-ray flux was computed in this
repository**. Changes after results exist must be listed under "Amendments" with
the reason.

## H1: random survival (baseline)

Not pre-registered: a first estimate had been run before this was written.

* H1 fails if the relic n_b/n_γ is more than 100 times below the observed
  6.12×10⁻¹⁰ for every annihilation cross-section c/m_π², c = 1, 2, 3.
* Limitation: uniform mixing, constant cross-section, constant g* = 10.75.

## G1: reproduce the 1998 result first

Inputs as in CDG (astro-ph/9707087): Ω = 1, Ω_Λ = 0, H₀ = 75 km/s/Mpc,
η = 2×10⁻¹⁰, annihilation counted for 20 < y < 1100 (y = 1 + z).

* Compare with the two curves of their Figure 5 (domain size d₀ = 20 and
  1000 Mpc) at 2, 3, 5, 7 and 10 MeV, read off the figure.
* **Pass:** within a factor of 1.5 at every point.
* The flux must scale as 1/d₀ to within 1 %.
* If G1 fails, no updated bound is claimed until the discrepancy is explained.

## G2: modern cosmology

Planck 2018 parameters (arXiv:1807.06209), including radiation in H(z).

* No pass/fail. Report modern/1998 flux ratio, changing one input at a time.
* Expectation recorded in advance: the flux goes up, mainly because η is about
  three times larger. If it goes down, check the code before believing it.

## G3: comparison with data

For each domain size d₀:

    R(d₀) = max over energy bins of  Φ_predicted / (Φ_observed + 2σ)

Φ_observed is the **total** measured diffuse background. Nothing is subtracted
for astrophysical sources, which favours the hypothesis. The data set and bins
are fixed and committed before R is computed.

| Result | Verdict at that d₀ |
|---|---|
| R > 3 | excluded |
| R < 1 | not excluded |
| 1 ≤ R ≤ 3 | inconclusive |

The margin of 3 allows for modelling uncertainty (CDG quote about a factor of 2
from parameter choices). Because Φ ∝ 1/d₀, the excluded range is
d₀ < d_excl = d₀·R(d₀)/3.

* d_excl ≥ 1000 Mpc: the 1998 conclusion is confirmed.
* d_excl < 1000 Mpc: the bound is weaker than published; report by how much.

Passing G3 at some d₀ would **not** establish H2. A mechanism that makes such
domains would still be needed.

## Which data

A p p̄ annihilation at rest releases 1877 MeV, so no photon exceeds about
938 MeV. Emitted at y ≥ 20, it arrives below about 47 MeV.

* Primary: COMPTEL diffuse background, 0.8–30 MeV (Weidenspointner et al. 2000,
  AIP Conf. Proc. 510, 467). Later than the preliminary data CDG used.
* Fermi-LAT's isotropic background (arXiv:1410.3696) starts near 100 MeV and
  **cannot constrain this signal**. It would matter only for annihilation after
  y ≈ 20, which CDG did not count and which is out of scope here.

## Amendments

None.
