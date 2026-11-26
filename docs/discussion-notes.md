# Discussion notes and speculations (26 November 2026)

Questions raised after the conservative comparison. Nothing here changes any verdict.
Items marked **speculation** have not been tested by this project.

## Dark energy and dark matter in the calculation
- Dark energy is included (flat universe, matter 0.3153). At 1+z = 20 it is only
  about 0.03% of the matter term in H^2, and less earlier.
- Dark matter enters only through the expansion rate. Post hoc runs at fixed
  ordinary matter (`scripts/matter_density_check.py`), predicted / (observed + 2 sigma):

| Total matter | judged run, 20 / 1000 Mpc | uniform heating, 20 / 1000 Mpc |
|---|---|---|
| 0.049 | 16548 / 331 | 5361 / 107 |
| 0.3153 (used) | 6544 / 131 | 2726 / 55 |
| 0.5625 | 4819 / 96 | 2190 / 44 |
| 1.0 | 3533 / 71 | 1741 / 35 |

  These are single runs, not the lowest-rate envelope used for the verdict.
- Dark matter gravity is not modelled. Estimate (not simulated): it matters little.
  Gas streams past dark matter at about 30 km/s at recombination, falling with 1+z to
  about 0.5 km/s at 1+z = 20, against about 75 km/s for gas near a border at that time.
  At early times streaming is the larger of the two, but it is coherent over Mpc.
- Dark matter scattering off protons is not modelled, and limits on it were not checked.

## Speculation 1: many visible galaxies are antimatter
- Light cannot tell them apart: antihydrogen should have the same spectral lines.
- Borders can. Intergalactic and cluster gas would annihilate where kinds meet.
- Steigman (arXiv:0808.1122; read only as a summary): antimatter fraction below
  about 1e-8 in some clusters (e.g. 8e-9 Perseus), below 3e-6 in the Bullet Cluster,
  extending to scales of about 20 Mpc.
- Our comparison: domains of 20 and 1000 Mpc excluded within our model.
- So a *large number* of visible antimatter galaxies is counted against.
- Not ruled out: rare, well-isolated objects or regions.
- Neutrinos could in principle tell (stars emit neutrinos, antistars antineutrinos),
  but not from distant galaxies with current instruments.

## Speculation 2: something kept matter and antimatter apart
- Needed, because the cosmic microwave background shows gas was nearly uniform early
  on: there were no empty gaps.
- We know of no established physics that does this. **No candidate yet.**
- Rule for this project: name the mechanism for physical reasons, and write down what
  it should leave behind and what would rule it out, before any simulation.

## Speculation 3: antistars and small pockets
- A 2021 study (Dupourque, Tibaldo, von Ballmoos, arXiv:2103.10073) flagged 14
  antistar candidates among 5787 Fermi gamma-ray sources. Candidates, not detections.
- AMS-02 has reported a few possible antihelium events. Unconfirmed.
- Even if real, small pockets would not remove the asymmetry.

## Speculation 4: the antimatter is hidden as dark matter
- Axion (anti)quark nuggets (Zhitnitsky and colleagues; arXiv:1305.6318, 2105.08719,
  2603.15585): net baryon number zero, unseen antibaryon charge in dense nuggets.
- This is a **different hypothesis**, not a rescue of the domain version.
- It needs new physics (including the axion, not yet found) and must explain why more
  antimatter than matter ends up in nuggets.
- Our simulations do not test it. We have only skimmed search results, mostly from its
  proponents; observational limits and independent criticism are unchecked.
- Next step if pursued: literature check first.

## Publication
- Nothing here rebuts Cohen, De Rujula and Glashow; our comparison reaches their
  conclusion. Whether it is new enough to publish is for an expert reviewer.
- First-time arXiv authors need a personal endorsement or prior co-authorship.
- Most useful next step: an outside expert check, especially of the heating assumption.

## Candidate 1: radiation pressure from the early annihilations (judged not to work)
Proposed by Praveen. Close to Omnes's idea (1969-71), reviewed as unsuccessful
(De Rujula, astro-ph/9705045; Dolgov, hep-ph/0211260). Our assessment is an argument
and an order-of-magnitude estimate, **not a simulation**:
- Light pushes matter and antimatter alike, so it cannot sort an even mixture.
- Equilibrium estimate of nucleon+antinucleon energy / radiation energy (g*=14.25):
  3e-3 at 100 MeV, 2e-8 at 40 MeV, 4e-16 at 22 MeV.
- Pressure cannot move gas beyond the sound horizon (about 150 Mpc comoving at
  recombination). Domains of that size are inside the range counted against.
