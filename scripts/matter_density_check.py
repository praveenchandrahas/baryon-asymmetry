"""Post hoc check, not verdict-bearing: vary total matter at fixed ordinary matter.

Run: PYTHONPATH=src python3 scripts/matter_density_check.py
"""
from bau import conservative as c
from bau.diagnostics import VARIANTS  # noqa: F401  (variant names used below)

RUNS = {"judged run": "baseline", "uniform heating": "H1 uniform heating"}

for om in (0.049, 0.3153, 0.5625, 1.0):
    c.MODERN.update(omega_m=om, omega_l=1 - om - c.OMEGA_R)
    row = []
    for label, variant in RUNS.items():
        J = c.solve(1, variant, c.MODERN)
        row.append(f"{label}: R(20)={c.R(J, 20):.0f} R(1000)={c.R(J, 1000):.0f}")
    print(f"omega_m={om}:", "; ".join(row))
