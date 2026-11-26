# Conservative comparison with data (26 November 2026): domains excluded

Rules: "Conservative comparison" in [criteria.md](criteria.md), committed in
806071c before any modern-cosmology J or flux was computed. They amend the
earlier rules **after G1b had failed**.

## Verdict

Lowest flux from all runs, current cosmology, against the COMPTEL fit plus
2 sigma:

| domain size d0 | R = predicted / (observed + 2 sigma) | verdict (R > 3) |
|---|---|---|
| 20 Mpc | 2600 | excluded |
| 1000 Mpc | 52 | excluded |

R is the largest value over 2-10 MeV and occurs at 10 MeV. At 1000 Mpc the
ratio is 4, 11, 34, 45, 52 at 2, 3, 5, 7, 10 MeV, so every energy exceeds the
threshold. At 1000 Mpc the lowest flux could be 17 times too high before this
verdict changed. The G1b gap is about a factor of 2.

The formula d0 R / 3 gives 17,000 Mpc, larger than the radius of the observable
universe (about 14,000 Mpc). We do not claim that: the calculation is not meant
for domains of that size. The claim is that d0 up to 1000 Mpc is excluded within
this model.

## Why the flux went up

For the judged run, the total flux is about 19 times the 1998-input value.

* J rises about 9 times at y = 20 from eta (3 times larger). The electron heating
  per unit length is proportional to electron density, so J grows roughly as
  eta squared.
* The change of expansion history raises the flux integral about 2 times for a
  given J, and changes J itself by -20 % to +10 %.
* Attenuation changes it by about 1 %.

This agrees in direction with the expectation recorded under G2.

## Checks

* With 1998 inputs the same code reproduces G1a.
* The power-law data fit agrees by eye with the preliminary COMPTEL points
  plotted in CDG Figure 5.
* Judged run, current inputs: a tighter solver tolerance, a ten times larger box
  and twice the cells change J by 1.1 % or less.
* CDG require the depleted width to be much smaller than the electron range
  (their eq. 19). It still is: at most a few per cent of it at y = 20, 100, 400.

## Not part of the rules (looked at after the verdict)

Judged run, current inputs, with the electron heating reduced:

| heating a (eV/Mpc) | R at 20 Mpc | R at 1000 Mpc |
|---|---|---|
| 30.6 (scaled, as in the rules) | 6500 | 131 |
| 10 (not scaled with density) | 2100 | 42 |
| 3.1 | 600 | 12 |
| none | 129 | 2.6 |

**The result at 1000 Mpc depends on annihilation electrons heating the gas.**
With no such heating it would be inconclusive there (still above 1).

## Limits

* One model: CDG's fluid equations, one dimension, complete ionisation, domains
  in contact, no magnetic fields. All our runs share these.
* The smallest of our runs is not a proven lower limit.
* The data are a power-law fit from a 1998 thesis abstract, not the final
  bin-by-bin COMPTEL values, which we could not retrieve.
* The photon spectrum is a stand-in model. Helium is ignored.
* Applying our modern/1998 ratio to CDG's curve is an assumption.
* Nothing here has been checked by an outside expert.

Not covered: domains about as large as the observable universe, small isolated
pockets, and arrangements that keep matter and antimatter from touching.

## Output

```
lowest J comes from: ['CDG x ratio k1 H1 uniform heating', 'CDG x ratio k2 B3 speed x2', 'CDG x ratio k2 H2 a=20', 'ours k1 B1 speed x0.5', 'ours k1 H1 uniform heating']
VERDICT d0=  20 Mpc: R=2599.94 -> excluded; d_excl=17333 Mpc
  predicted/(obs+2sigma) at [ 2.  3.  5.  7. 10.] MeV: [ 199.86  545.14 1702.3  2265.21 2599.94]
VERDICT d0=1000 Mpc: R=52.00 -> excluded; d_excl=17333 Mpc
  predicted/(obs+2sigma) at [ 2.  3.  5.  7. 10.] MeV: [ 4.   10.9  34.05 45.3  52.  ]

for comparison only (not verdict-bearing), d_excl in Mpc:
  judged run (ours k1 baseline)    R(20)= 6544.2 R(1000)=130.88 d_excl=43628
  ours k2 baseline                 R(20)=13100.5 R(1000)=262.01 d_excl=87337
  CDG J x ratio, k1 baseline       R(20)= 9323.2 R(1000)=186.46 d_excl=62155
  ours k1 H1 uniform heating       R(20)= 2725.6 R(1000)= 54.51 d_excl=18170
```
