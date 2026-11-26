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

## G1b: computing J(y)

Not done. This is the harder part of the calculation.

## Limits

* The photon spectrum is a stand-in model, not the measured one CDG used.
* J(y) and the comparison curves are digitised from the paper's figures.
* The pair-production cross-section is the unscreened high-energy formula.
