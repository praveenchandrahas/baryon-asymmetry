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
