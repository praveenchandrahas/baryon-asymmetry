"""Needs pdfplumber. Usage: digitise.py paper.pdf data

Recover the plotted curves of CDG (astro-ph/9707087v2) Figs. 3 and 5 from the PDF's vector paths."""
import sys, pdfplumber
pdf = pdfplumber.open(sys.argv[1]); out = sys.argv[2]
HEAD = "# Digitised from the vector paths of astro-ph/9707087v2, {}\n"

# Fig. 3 (page 13): ticks y=100 at x=288.71, y=1000 at x=454.31; J=1e2 at top=557.65, 1e7 at 334.98
c = [c for c in pdf.pages[12].curves if c["x1"] - c["x0"] > 100 and c["stroking_color"] == (0.0, 0.0, 0.0)]
assert len(c) == 1
with open(f"{out}/cdg_fig3_J.csv", "w") as f:
    f.write(HEAD.format("Fig. 3 solid curve") + "y,J_per_cm2_s\n")
    for x, top in sorted(c[0]["pts"]):
        f.write(f"{10**(2+(x-288.71)/(454.31-288.71)):.5g},{10**(2+(557.65-top)/((557.65-334.98)/5)):.5g}\n")

# Fig. 5 (page 18): ticks E=1 MeV at x=247.015, 10 MeV at 380.185; flux 1 at top=132.465, 1e-6 at 349.425
c = [c for c in pdf.pages[17].curves if c["x1"] - c["x0"] > 100 and c["bottom"] - c["top"] > 1.2]
assert len(c) == 4
for pick, (name, d0) in enumerate((("upper", 20), ("lower", 1000))):
    first = [k for k in c if k["x0"] < 200]; second = [k for k in c if k["x0"] > 200]
    pts = sorted(first, key=lambda k: k["top"])[pick]["pts"] + sorted(second, key=lambda k: k["top"])[pick]["pts"]
    with open(f"{out}/cdg_fig5_d{d0}.csv", "w") as f:
        f.write(HEAD.format(f"Fig. 5 {name} curve (labelled d0={d0} Mpc)") + "E_MeV,flux_per_cm2_s_MeV_sr\n")
        for x, top in sorted(set(pts)):
            f.write(f"{10**((x-247.015)/(380.185-247.015)):.5g},{10**(-(top-132.465)/((349.425-132.465)/6)):.5g}\n")

# Fig. 2 (page 12): ticks y=1 at x=172.87, 93.62 pt per decade; T=1 eV at top=207.57, 51.31 pt per decade
c = [c for c in pdf.pages[11].curves if c["stroking_color"] == (0, 0, 0) and c["x1"] - c["x0"] > 50]
assert len(c) == 1
with open(f"{out}/cdg_fig2_T.csv", "w") as f:
    f.write(HEAD.format("Fig. 2 electron-heating curve") + "y,T_eV\n")
    for x, top in sorted(set(c[0]["pts"])):
        f.write(f"{10**((x-172.87)/93.62):.5g},{10**((207.57-top)/51.31):.5g}\n")
