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

The margin of 3 allows for modelling uncertainty (CDG: other cosmologies lower
the flux by at most about 2; a shorter electron range by at most about 3). Because Φ ∝ 1/d₀, the excluded range is
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

26 November 2026, after reading the paper itself and **after seeing the G1a
result**:

1. G1 is split. **G1a**: the flux integral using CDG's own J(y), taken from
   their Figure 3. **G1b**: computing J(y) ourselves from their eqs. 1–3 and
   reproducing Figure 3. G1 passes only if both do. G1b is needed because J
   depends on cosmology, so G2 cannot be run without it.
2. The reason for G3's margin was misstated. CDG say other cosmologies cannot
   *lower* the flux by more than about 2; they put no such limit on increases.
   The thresholds are unchanged. No G3 quantity has been computed.

## G1b criterion (set 26 November 2026, before any J(y) was computed here)

The published figures had been seen and compared with CDG's own formulas; no
solver output existed.

**Pass:** our self-consistent J(y) is within a factor of 1.5 of CDG Figure 3
(solid curve) at y = 20, 25, 40, 100, 200, 400 and 1000, and halving the grid
spacing changes it by less than 5 %.

**Solver checks required first:** flux into vacuum = (3/4)⁴ n c_s to 2 %; the
strong-drag limit reproduces CDG eq. 7 to 5 %.

**Pressure convention, fixed in advance.** CDG define T = p/(n_p + n_e), which
gives p = 2nT. Their eqs. 6 and 8, the Compton term in eq. 3 and the dashed
curve of Figure 3 instead correspond to p = nT. Their temperature figure
corresponds to a heat capacity of both species (3nT per proton).

* Judged run: pressure p = nT in the momentum equation (what their formulas
  use), heat capacity 3nT.
* Also reported: p = 2nT, which we believe is physically correct.

Other choices: electron heating only, a = 10 eV/Mpc (their value), UV heating
neglected, annihilation treated as a perfectly absorbing boundary.

3. 26 November 2026, **after G1b had failed**: a conservative comparison with
   data is run although the "no updated bound until explained" rule of G1 is not
   met. See below. This changes a rule after seeing a failure.

## Conservative comparison (set 26 November 2026, before any modern-cosmology J or flux was computed here)

Approved by the project owner. **Not blind**: G1 results were known, CDG's
Figure 5 already shows their prediction against preliminary COMPTEL data, and we
had recorded an expectation that modern inputs raise the flux.

**Question.** With current cosmology, is even the lowest flux we have too bright?

**Annihilation rate.** At each y, the smallest J among:

* our solver in all nine variants of `diagnostics.md` (baseline, H1, H2, B1-B3,
  E1, N1, N2), for both pressure conventions; and
* CDG's Figure 3 J multiplied by (our modern J / our 1998 J) for each of those 18.
  Applying our ratio to their curve is an assumption.

**Cosmology.** h = 0.6736, Omega_m = 0.3153, flat, radiation density
Omega_r h^2 = 4.18e-5, eta = 6.12e-10 (Planck 2018). The electron energy loss
a y^3 is proportional to electron density (CDG eq. 30), so a is multiplied by
eta/2e-10. Annihilation counted for 20 < y < 1100 only. Helium is ignored.

**Photon spectrum.** At each energy, the smallest flux among k = 1, 2, 3.

**Data.** COMPTEL cosmic diffuse background, power-law fit from S. C. Kappadath,
PhD thesis (University of New Hampshire, 1998), abstract:
(1.05 +- 0.2) x 10^-4 (E/5 MeV)^(-2.4 +- 0.2) photons / (cm^2 s sr MeV).
Phi_obs + 2 sigma is taken generously: normalisation 1.45e-4, and at each energy
the more favourable of index -2.8 and -2.0. This replaces the Weidenspointner
et al. (2000) bins named earlier, whose values we could not retrieve. Nothing is
subtracted for other sources.

**Statistic.** R(d0) = max over 2, 3, 5, 7, 10 MeV of Phi_pred / (Phi_obs + 2 sigma),
for d0 = 20 and 1000 Mpc; d_excl = d0 R / 3.

**Verdict** (thresholds as in G3): R > 3 excluded; R < 1 or 1 <= R <= 3:
**inconclusive** until the G1b gap is settled (a lowest-case flux below the data
cannot show that a domain size is allowed). d_excl >= 1000 Mpc: the 1998
conclusion survives this test.

**What a pass would not show.** The smallest of our runs is not a proven lower
limit: the runs share assumptions (CDG's fluid model, one dimension, complete
ionisation, no magnetic fields, domains in contact).
