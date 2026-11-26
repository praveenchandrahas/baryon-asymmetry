# G1b diagnostics (list fixed 26 November 2026, before any of them was run)

**These do not change the G1b verdict.** G1b failed. The aim is to find out what
accounts for the gap. Each row changes one thing from the baseline, for both
pressure conventions.

| id | change |
|---|---|
| V0 | extra check: nearly isothermal flow into vacuum should give n c_iso / e |
| H1 | heating per volume independent of local density (floored at 10 % of far density), instead of proportional to it |
| H2 | a = 20 eV/Mpc, the top of CDG's quoted range |
| B1 | outflow speed at the interface x 0.5 |
| B2 | outflow speed x 0.775 (isothermal sound speed) |
| B3 | outflow speed x 2 |
| E1 | Hubble drag on the peculiar velocity omitted |
| N1 | coarse grid, 40 cells |
| N2 | very coarse grid, 20 cells |

A change "accounts for the gap" only if it brings J within 1.5 of Figure 3 at all
seven points **and** keeps the far-field temperature within 1.5 of Figure 2. Even
then it is a candidate, not proof of what CDG did.

## Results (26 November 2026): no listed change accounts for the gap

Run with `PYTHONPATH=src python -m bau.diagnostics`. The diagnostics use a
150-cell grid with a first cell of 3e18 cm, so the baseline differs from the
judged run in the second decimal place.

**V0.** Static isothermal flow gives 1.002-1.004 of n c_iso / e, for outflow
speeds x0.775, x1 and x2. The wall treatment recovers a known result and does not
depend on the speed imposed there in this case.

J / Figure 3, pressure p = nT (the judged convention):

| change | 20 | 25 | 40 | 100 | 200 | 400 | 1000 |
|---|---|---|---|---|---|---|---|
| baseline | 1.02 | 0.77 | 0.53 | 0.57 | 0.75 | 0.74 | 0.90 |
| H1 uniform heating | 0.55 | 0.35 | 0.19 | 0.26 | 0.51 | 0.66 | 0.89 |
| H2 a = 20 | 2.06 | 1.56 | 1.09 | 1.12 | 1.11 | 0.84 | 0.92 |
| B1 speed x0.5 | 0.81 | 0.62 | 0.43 | 0.50 | 0.68 | 0.70 | 0.86 |
| B2 speed x0.775 | 0.98 | 0.74 | 0.51 | 0.57 | 0.74 | 0.74 | 0.89 |
| B3 speed x2 | 1.02 | 0.77 | 0.53 | 0.58 | 0.75 | 0.75 | 0.91 |
| E1 no Hubble drag | 1.27 | 0.95 | 0.65 | 0.71 | 0.85 | 0.77 | 0.90 |
| N1 40 cells | 1.06 | 0.80 | 0.55 | 0.60 | 0.78 | 0.77 | 0.95 |
| N2 20 cells | 1.12 | 0.83 | 0.58 | 0.63 | 0.81 | 0.80 | 1.00 |

* No row meets both conditions, for either pressure convention.
* H2 brings J closer in the middle but the temperature is then 2-4 times
  Figure 2, so it is not what CDG did.
* Spreading the heating uniformly (H1) makes the gap larger.
* Omitting Hubble drag (E1) is the closest change that keeps heating as stated.
  It still misses at y = 40.
* With p = 2nT, B1 misses mainly at y = 20 (1.64). Combinations of changes were
  not tried; picking one after seeing the results would be fitting.

## A further check, not on the list (added after the results above)

`similarity.py` solves a simplified case semi-analytically, sharing no code with
the solvers: isothermal gas, expanding universe, sound speed rising as t^b, no
heating source and no CBR drag.

| b | semi-analytic J / (n c_iso) | solver / semi-analytic |
|---|---|---|
| 0.1 | 0.275 | 1.068 |
| 0.5 | 0.288 | 1.068 |
| 1.0 | 0.294 | 1.075 |

The 7 % shrinks to about 3 % when the solver's thermostat is made 100 times
stronger, and barely changes with grid size. The remaining 3 % is unexplained.

The first version of this check disagreed with the solver by a factor of 2-5.
The error was in the check: it took a solution branch that does not satisfy the
condition at the wall.

**What it suggests.** At b = 0.5, 0.288 n c_iso is about 0.70 of
(3/4)^4 n c_s, close to our solver's ratio of about 0.7 at y = 40-100. CDG's J
there is 0.97-0.98 of (3/4)^4 n c_s. This is a reason to suspect that expansion
lowers the flux below the static value CDG's curve follows.

**What it does not show.** It is an isothermal idealisation, not CDG's full
equations. It was derived within this project and has not been checked by an
outside expert. It does not establish that the published curve is wrong.
