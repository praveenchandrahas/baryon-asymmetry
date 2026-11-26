# baryon-asymmetry

Simulations testing a matter–antimatter symmetric ("domain") universe as an answer
to the baryon asymmetry problem.

## The hypothesis under test

The early universe had equal amounts of matter and antimatter, which annihilated
wherever they met. We observe a surviving matter-dominated region; other regions
are antimatter-dominated.

This is an existing idea (Omnès 1969, Stecker and others), not a new theory, and
**the published evidence is largely against it**. The aim here is to test it
openly, with pass/fail criteria written down first.

It is split into three claims, because they fail or survive separately:

| | Claim | Status going in |
|---|---|---|
| H1 | Random survival, no new physics | A first freeze-out estimate leaves about 10⁹ times too little matter |
| H2 | Large separated domains produced by some mechanism (new physics) | Gamma rays exclude domains much smaller than the visible universe (Cohen, De Rújula, Glashow 1998) |
| H3 | Small, distant antimatter pockets exist | Can be bounded; would not by itself explain the asymmetry |

## First target

Redo the Cohen–De Rújula–Glashow (CDG) diffuse gamma-ray bound with current
cosmological parameters and later MeV-band data. See
[docs/criteria.md](docs/criteria.md) and [docs/prior-work.md](docs/prior-work.md).

## What is here now

* `src/bau/relic.py` – freeze-out with zero net baryon number (H1 baseline)
* `src/bau/kinematics.py` – highest photon energy the CDG signal can have today
* `tests/` – checks, run by GitHub Actions
* `src/bau/flux.py` – the CDG flux integral, using their published J(y); see
  [docs/g1-results.md](docs/g1-results.md)
* `src/bau/fluid.py`, `godunov.py` – our own J(y). **It does not reproduce
  theirs within the preset tolerance**, so there is no updated bound
* `src/bau/diagnostics.py`, `similarity.py` – attempts to explain the gap; see
  [docs/diagnostics.md](docs/diagnostics.md)
* [docs/index.html](docs/index.html) – a plain-language explainer

## Run

```bash
python -m pip install -r requirements.txt
python -m pytest
PYTHONPATH=src python -m bau.relic
PYTHONPATH=src python -m bau.g1
PYTHONPATH=src python -m bau.g1b
PYTHONPATH=src python -m bau.diagnostics
```
