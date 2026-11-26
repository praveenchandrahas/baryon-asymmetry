"""Writes docs/index.html. Chart values are the judged and reported G1b ratios."""
import math

Y = [20, 25, 40, 100, 200, 400, 1000]
JUDGED = [1.01, 0.76, 0.52, 0.57, 0.74, 0.74, 0.89]
REPORTED = [2.03, 1.54, 1.07, 1.11, 1.24, 1.10, 1.26]

W, H, L, R, T, B = 640, 340, 46, 14, 14, 46
def px(y): return L + (math.log10(y) - math.log10(17)) / (math.log10(1200) - math.log10(17)) * (W - L - R)
def py(r): return T + (math.log(2.5) - math.log(r)) / (math.log(2.5) - math.log(0.4)) * (H - T - B)

svg = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Our result divided by the published result at seven times. The first run falls below the allowed band at two of them.">']
svg.append(f'<rect class="band" x="{L}" y="{py(1.5):.1f}" width="{W-L-R}" height="{py(1/1.5)-py(1.5):.1f}"/>')
for r, lab in [(0.5, "0.5×"), (1, "1×"), (1.5, "1.5×"), (2, "2×")]:
    svg.append(f'<line class="{"one" if r == 1 else "grid"}" x1="{L}" x2="{W-R}" y1="{py(r):.1f}" y2="{py(r):.1f}"/>')
    svg.append(f'<text x="{L-6}" y="{py(r)+4:.1f}" text-anchor="end">{lab}</text>')
for y in Y:
    svg.append(f'<text x="{px(y):.1f}" y="{H-B+18}" text-anchor="middle">{y}</text>')
svg.append(f'<text x="{(L+W-R)/2:.0f}" y="{H-8}" text-anchor="middle">1 + redshift (further right means earlier in the universe)</text>')
for data, cls, name in [(JUDGED, "s1", "Judged run"), (REPORTED, "s2", "Second run")]:
    pts = " ".join(f"{px(y):.1f},{py(r):.1f}" for y, r in zip(Y, data))
    svg.append(f'<polyline class="{cls}" points="{pts}"/>')
    for y, r in zip(Y, data):
        tip = f"{name}, 1+z = {y}: {r:.2f} × published"
        if cls == "s1":
            mark = f'<circle class="{cls}d" cx="{px(y):.1f}" cy="{py(r):.1f}" r="5"/>'
        else:
            mark = f'<rect class="{cls}d" x="{px(y)-4.5:.1f}" y="{py(r)-4.5:.1f}" width="9" height="9"/>'
        svg.append(f'<g class="pt" tabindex="0" data-tip="{tip}"><circle class="hit" cx="{px(y):.1f}" cy="{py(r):.1f}" r="13"/>{mark}</g>')
svg.append("</svg>")
SVG = "\n".join(svg)

rows = "".join(f"<tr><td>{y}</td><td>{a:.2f}</td><td>{b:.2f}</td></tr>" for y, a, b in zip(Y, JUDGED, REPORTED))

CSS = """
/* layout: one reading column; the claim-by-claim status sits near the top */
:root{--bg:#ffffff;--fg:#191919;--mute:#5d6470;--line:#dde1e8;--panel:#f4f6f9;--accent:#3c3f8f;
--series-1:#2a78d6;--series-2:#eb6834;--band:#e6e9f0;
--serif:'Source Serif 4',Georgia,serif;--sans:'IBM Plex Sans',system-ui,sans-serif;color-scheme:light}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#191919;--fg:#efefef;--mute:#a3a8b3;--line:#363a42;--panel:#22242a;--accent:#b4b7f2;--series-1:#3987e5;--series-2:#d95926;--band:#2c2f37;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#191919;--fg:#efefef;--mute:#a3a8b3;--line:#363a42;--panel:#22242a;--accent:#b4b7f2;--series-1:#3987e5;--series-2:#d95926;--band:#2c2f37;color-scheme:dark}
body{margin:0;background:var(--bg);color:var(--fg);font:17px/1.62 var(--sans)}
main{max-width:42rem;margin:0 auto;padding:2.5rem 1.1rem 4rem}
h1,h2,h3{font-family:var(--serif);line-height:1.2;text-wrap:balance}
h1{font-size:2.3rem;margin:0 0 .6rem}
h2{font-size:1.5rem;margin:2.8rem 0 .6rem;padding-top:1.4rem;border-top:1px solid var(--line)}
h3{font-size:1.12rem;margin:1.6rem 0 .3rem}
a{color:var(--accent)}
.lede{font-size:1.15rem;color:var(--mute)}
.note{background:var(--panel);border-left:4px solid var(--accent);padding:.8rem 1rem;margin:1.4rem 0}
.scroll{overflow-x:auto}
table{border-collapse:collapse;width:100%;font-size:.93rem;font-variant-numeric:tabular-nums}
th,td{text-align:left;padding:.45rem .6rem .45rem 0;border-bottom:1px solid var(--line);vertical-align:top}
.big{font-family:var(--serif);font-size:1.9rem;line-height:1.1;display:block}
.pair{display:grid;grid-template-columns:repeat(auto-fit,minmax(15rem,1fr));gap:1rem;margin:1.2rem 0}
.pair div{background:var(--panel);padding:.9rem 1rem}
figure{margin:1.4rem 0}
figcaption{font-size:.9rem;color:var(--mute)}
svg{width:100%;height:auto;display:block}
svg text{fill:var(--mute);font:12px var(--sans)}
.band{fill:var(--band)}.grid{stroke:var(--line)}.one{stroke:var(--mute);stroke-dasharray:4 4}
.s1,.s2{fill:none;stroke-width:2}.s1{stroke:var(--series-1)}.s2{stroke:var(--series-2)}
.s1d{fill:var(--series-1);stroke:var(--bg);stroke-width:2}.s2d{fill:var(--series-2);stroke:var(--bg);stroke-width:2}
.hit{fill:transparent}.pt:focus{outline:none}.pt:focus .hit{stroke:var(--fg)}
.legend{display:flex;flex-wrap:wrap;gap:1.2rem;font-size:.9rem;margin-bottom:.5rem}
.legend span::before{content:"";display:inline-block;width:.7rem;height:.7rem;margin-right:.4rem;background:var(--series-1);border-radius:50%}
.legend span+span::before{background:var(--series-2);border-radius:0}
#tip{min-height:1.5em;font-size:.9rem;font-variant-numeric:tabular-nums}
summary{cursor:pointer}
@media (max-width:520px){svg text{font-size:19px}}
footer{margin-top:3rem;font-size:.88rem;color:var(--mute)}
"""

BODY = f"""
<main>
<h1>Where did the antimatter go?</h1>
<p class="lede">The universe should have destroyed almost all of its matter. It did not. This page explains the puzzle, one old idea for solving it, and what our computer simulations have and have not shown so far.</p>
<div class="note"><strong>The short answer.</strong> We have not solved the puzzle. With current numbers for the universe, our calculation counts strongly against the idea we are testing: the separate regions it needs would produce far more gamma rays than are seen.</div>

<h2>The puzzle</h2>
<p>Every kind of matter particle has a mirror twin, an antiparticle, with the opposite charge. When a proton meets an antiproton, both are destroyed and their mass turns into lighter particles and radiation. This is called <em>annihilation</em>.</p>
<p>In the first fraction of a second the universe was hot enough to keep making particle and antiparticle pairs. As far as well-tested physics tells us, matter and antimatter are made together in equal amounts. As the universe cooled they should have wiped each other out, leaving a bath of light and almost nothing else.</p>
<p>Yet we are here. Today there are about 6 matter particles (protons and neutrons) for every 10 billion particles of light, and no sign of a matching amount of antimatter. Physicists call this the <em>baryon asymmetry problem</em>. Baryons are particles such as protons and neutrons.</p>
<p>Most physicists think some not-yet-discovered process made slightly more matter than antimatter, and the small excess is what survived. Several such processes have been proposed. None has been confirmed.</p>

<h2>The idea we are testing</h2>
<p>Perhaps there never was an excess. The early universe had equal amounts of both, and they annihilated wherever they met. Some regions were left with matter and others with antimatter. We live in a matter region, and antimatter regions lie too far away to have noticed.</p>
<p>This is not a new theory. Roland Omnès proposed a version in 1969, and Floyd Stecker and others developed it. The weight of published evidence is against it. Our aim is to test it openly and to write down what counts as failure before running anything.</p>
<p>The idea comes in three versions, which can fail separately.</p>
<div class="scroll"><table>
<tr><th>Version</th><th>What it claims</th><th>Where it stands</th></tr>
<tr><td>Luck alone</td><td>Random unevenness, with no new physics, left enough survivors.</td><td>Our first estimate says no, by a wide margin.</td></tr>
<tr><td>Large separate regions</td><td>Something not yet known pushed matter and antimatter far apart.</td><td>A 1998 study says the regions would have to be about as large as everything we can see. Our updated comparison agrees as far as we tested it.</td></tr>
<tr><td>Small pockets</td><td>A few antimatter pockets exist far away.</td><td>Not tested here. Even if true, they would not explain the puzzle.</td></tr>
</table></div>

<h2>Simulation 1: could luck be enough?</h2>
<p>We started with equal amounts, mixed evenly, and let them annihilate as the universe expanded and cooled.</p>
<div class="pair">
<div><span class="big">2 to 6</span>survivors for every 10,000,000,000,000,000,000 particles of light, in our calculation</div>
<div><span class="big">6</span>for every 10,000,000,000 particles of light, in the real universe</div>
</div>
<p>That is one to three billion times too few. So something would have had to separate matter from antimatter, and early: within about the first thousandth of a second. In that time, light could have linked only patches that would today be about 7.5 light-years across. The nearest star is a bit over 4 light-years away, so these patches are tiny compared with a galaxy.</p>
<p>This estimate is simple. It assumes even mixing and a fixed annihilation strength.</p>

<h2>The test that matters: gamma rays</h2>
<p>If matter and antimatter regions exist, they must touch somewhere, unless something empties the space between them. Along each border, annihilation would produce gamma rays, a very energetic form of light. Those rays would still be arriving today as a faint glow across the whole sky.</p>
<p>In 1998 Andrew Cohen, Álvaro De Rújula and Sheldon Glashow calculated that glow. They concluded it would be brighter than what telescopes see unless our matter region is about as large as the visible universe.</p>
<p>Their calculation used the picture of the universe accepted then. We now know it differently, for example that its expansion is speeding up. So we planned to redo it with current numbers. First we tried to reproduce their 1998 result.</p>

<h2>Simulation 2: can we reproduce the 1998 result?</h2>
<h3>Step one: from annihilation rate to glow. Passed.</h3>
<p>Taking their published annihilation rate as given, we computed the glow ourselves. We had agreed beforehand to accept anything within 1.5 times their answer. For small regions we got 0.92 to 0.94 times theirs. For very large regions we got 0.69 to 0.71, which passes only narrowly.</p>
<h3>Step two: computing the rate ourselves. Failed.</h3>
<p>Next we simulated how gas flows into a border and is destroyed there. The chart shows our rate divided by theirs at seven moments in cosmic history. All seven points of the judged run had to fall inside the shaded band. Two fell below it.</p>
<figure>
<div class="legend"><span>Judged run (the rule fixed in advance)</span><span>Second run (the rule we think is physically right)</span></div>
{SVG}
<div id="tip" aria-live="polite">Point at or tab to a mark to read its value.</div>
<figcaption>Shaded: within 1.5 times the published value. Dashed line: exact agreement. The two runs differ in how the gas pressure is defined; the paper's definition and its formulas do not match.</figcaption>
<details><summary>Show the numbers</summary><div class="scroll"><table><tr><th>1 + redshift</th><th>Judged run</th><th>Second run</th></tr>{rows}</table></div></details>
</figure>
<p>The second run is closer but also misses, at the two latest moments. We cannot switch to it after seeing the answer. So the verdict is <strong>failed</strong>.</p>
<h3>Why the difference?</h3>
<p>We changed our assumptions one at a time: how the heat is spread, how the border is treated, how fine the computer grid is, and how expansion slows the gas. No single change closed the gap.</p>
<p>We then solved a simplified version of the problem by a separate mathematical route. It agreed with our simulation to within about 7 per cent. This hints that the published rate may be somewhat high in part of its range. It does not prove it: the simplified version leaves out parts of the full problem, and no outside expert has checked our work. The mistake could still be ours.</p>
<p>We also found two inconsistencies in the paper. Two curves in one figure differ by 37.5 times where its own scaling rule requires 50. Its definition of temperature does not match its formulas. Neither finding by itself overturns its conclusion.</p>

<h2>Simulation 3: even our lowest estimate against telescope data</h2>
<p>We could not settle which annihilation rate is right. So we asked a safer question: if we always take the lowest rate we have, is the predicted glow still too bright? We wrote down this rule before computing it. It does change our earlier plan, which was to stop until the difference was explained.</p>
<p>We used current numbers for the universe and compared with measurements from COMPTEL, a gamma-ray telescope. To be fair to the idea, we raised the measured values by their uncertainty and assumed that none of the observed glow comes from anything else. The rule was that more than 3 times too bright means ruled out.</p>
<div class="scroll"><table>
<tr><th>Size of each region</th><th>Predicted compared with observed</th><th>Verdict</th></tr>
<tr><td>20 Mpc (about 65 million light-years)</td><td>2,600 times brighter</td><td>Ruled out</td></tr>
<tr><td>1,000 Mpc (about 3 billion light-years)</td><td>52 times brighter</td><td>Ruled out</td></tr>
</table></div>
<p>The glow came out brighter than in 1998, mainly because we now know there is about three times as much ordinary matter as assumed then.</p>
<p>We include dark energy and dark matter in how fast the universe expanded. We did not simulate the gravity of dark matter; we estimate it matters little.</p>
<p>The larger size depends on one assumption: that particles flying out of the annihilations heat the gas, which makes it flow into the border faster. With no such heating at all, which we looked at afterwards, the result for the larger size would be undecided.</p>

<h2>What this does not show</h2>
<ul>
<li>It rests on one model of how matter and antimatter meet. All our simulations share its assumptions.</li>
<li>It does not cover regions about as large as everything we can see, small isolated pockets, or any arrangement that keeps matter and antimatter apart.</li>
<li>No outside expert has checked our work.</li>
</ul>

<h2>Speculations we have not tested</h2>
<p>These came up in our discussions. They are open questions and guesses, <strong>not results</strong>.</p>
<h3>Could many of the galaxies we see be antimatter?</h3>
<p>Their light would not tell us, because antimatter atoms should shine just like ordinary ones. Their borders would. Gas between and inside <a href="https://arxiv.org/abs/0808.1122">clusters of galaxies shows no sign of annihilation</a>, and our comparison counts against large touching regions. So a large number of antimatter galaxies looks very unlikely. A rare, well-isolated one is not ruled out.</p>
<h3>Could something have kept the two apart?</h3>
<p>This is the natural escape. But the early universe was filled with gas almost perfectly evenly, so there were no empty gaps. Something else would be needed, and we have no candidate. If we find one, we will write down what would rule it out before simulating it.</p>
<h3>Could there be a few antimatter stars?</h3>
<p>A 2021 study flagged <a href="https://arxiv.org/abs/2103.10073">14 gamma-ray sources as possible antistars</a>. None is confirmed. A few would not solve the puzzle.</p>
<h3>Could the antimatter be hiding as dark matter?</h3>
<p>Dark matter is the unseen mass that makes up most of the matter in the universe. One proposal says the missing antimatter is packed into <a href="https://arxiv.org/abs/2105.08719">small, very dense nuggets</a> that make it up. This is a different idea from ours. It needs particles not yet found, our simulations do not test it, and we have not yet checked what observations or critics say.</p>

<h2>Words used here</h2>
<div class="scroll"><table>
<tr><td>Antimatter</td><td>Particles with the opposite charge to ordinary ones.</td></tr>
<tr><td>Annihilation</td><td>A particle and its antiparticle destroying each other.</td></tr>
<tr><td>Redshift</td><td>How much the universe has stretched since light set out. At 1 + redshift = 100 it was 100 times smaller in every direction.</td></tr>
<tr><td>Gamma ray</td><td>Light of very high energy, invisible to the eye.</td></tr>
</table></div>

<footer>
<p>A project by Praveen Chandrahas. The code and analysis were produced with help from an AI system (Claude) and have not been peer reviewed. Status as of 26 November 2026, evening.</p>
<p><a href="https://github.com/praveenchandrahas/baryon-asymmetry">Code, data and pass/fail rules</a> · <a href="https://arxiv.org/abs/astro-ph/9707087">The 1998 study</a></p>
</footer>
</main>
<script>
const tip=document.getElementById('tip');
document.querySelectorAll('.pt').forEach(p=>['pointerenter','focus','click'].forEach(e=>p.addEventListener(e,()=>tip.textContent=p.dataset.tip)));
</script>
"""

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Where did the antimatter go?</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;600&family=Source+Serif+4:wght@600&display=swap">
<style>{CSS}</style>
</head>
<body>{BODY}</body>
</html>
"""
import pathlib
(pathlib.Path(__file__).resolve().parents[1] / "docs" / "index.html").write_text(html, encoding="utf-8")
