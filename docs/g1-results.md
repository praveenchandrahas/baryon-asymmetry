# G1 results

## G1a: flux integral with CDG's J(y) (26 November 2026)

Ours divided by the published curve at 2, 3, 5, 7, 10 MeV:

| Photon spectrum shape | d₀ = 20 Mpc | d₀ = 1000 Mpc |
|---|---|---|
| k = 2 (default, set before running) | 0.92–0.94 | 0.69–0.71 |
| k = 1 | 0.86–0.99 | 0.65–0.74 |
| k = 3 | 0.91–0.97 | 0.69–0.72 |

Pass needs 0.67–1.5. With the default spectrum both curves pass, **the second
only narrowly**. With k = 1 it fails narrowly at 7 and 10 MeV.

**Inconsistency in the published figure.** The flux scales as 1/d₀, so curves
for 20 and 1000 Mpc should differ by 50. In the vector data of Figure 5 they
differ by 37.5 at every energy checked, which corresponds to d₀ = 750 Mpc for
the lower curve if the upper one is right. 750 = 1000 × h, so a units slip
involving h is a possible cause, but that is a guess.

## G1b: computing J(y) (26 November 2026): **FAIL**

Our J divided by CDG Figure 3. Pass needed 0.67-1.5 at every point.

| y | 20 | 25 | 40 | 100 | 200 | 400 | 1000 |
|---|---|---|---|---|---|---|---|
| p = nT (judged) | 1.01 | 0.76 | **0.52** | **0.57** | 0.74 | 0.74 | 0.89 |
| p = 2nT (reported) | **2.03** | **1.54** | 1.07 | 1.11 | 1.24 | 1.10 | 1.26 |

Flux from our own J divided by Figure 5, at 2-10 MeV:

| | d0 = 20 Mpc | d0 = 1000 Mpc |
|---|---|---|
| p = nT (judged) | 0.56-0.65 | 0.42-0.48 |
| p = 2nT (reported) | 1.13-1.31 | 0.85-0.98 |

**G1 therefore fails, and no updated bound is claimed.** The p = 2nT run is
closer, but it was not the judged run and also misses at y = 20 and 25.

### What was checked

* Flux into vacuum matches (3/4)^4 n c_s to 0.5 %.
* The strong-drag limit matches CDG eq. 7 to about 1 % once nu*t is above about
  10^4. At y = 1000 (nu*t = 64) J is 19 % below eq. 7. The test in
  `criteria.md` did not say at what drag it applied; we chose the limit.
* Halving the grid spacing changes J by at most 1.4 %.
* An independent finite-volume solver (`godunov.py`), started at y = 400,
  agrees within 1 % at y = 100, 40 and 20.
* Driven by CDG's J, our heating and cooling terms reproduce their Figure 2
  temperature to 1-3 %.

### Where the difference lies (not settled)

The heating and cooling match, so the difference is in the relation between J
and temperature. At y = 40-100 their J is 0.97-0.98 of (3/4)^4 n c_s (p = nT);
ours is about 0.7. Diagnostics run afterwards ([diagnostics.md](diagnostics.md))
changed the heating profile, wall speed, Hubble drag and grid one at a time.
**None accounts for the gap.** A semi-analytic solution of a simplified case
supports the lower coefficient, with limits described there.

### Two points about the paper

* They define T = p/(n_p+n_e), but eqs. 6 and 8 and the Compton term in eq. 3
  correspond to p = nT, not 2nT.
* Their Figure 2 corresponds to a heat capacity of 3nT, counting both species.

## Limits

* The photon spectrum is a stand-in model, not the measured one CDG used.
* J(y) and the comparison curves are digitised from the paper's figures.
* The pair-production cross-section is the unscreened high-energy formula.
