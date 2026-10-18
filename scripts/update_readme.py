# -*- coding: utf-8 -*-
"""Sync README.md with the post-review revision (new scripts, figures, numbers)."""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, 'README.md')

R = []

R.append((
    'header note',
    r"prepared for submission to the *Journal of The Electrochemical Society (JES)*, Electrochemical Engineering area.",
    r"prepared for submission to the *Journal of The Electrochemical Society (JES)*, Electrochemical Engineering area. "
    r"This repository now holds the **post-review revision**: the mechanism has been rebuilt around the "
    r"Ca + MgO -> CaO + Mg reaction, engineering content (flowsheet, reactor concept, product recovery) has been "
    r"added, the uncertainty analysis has been expanded from five to ten parameters, and results are reported at "
    r"both 600 and 620 C. See `review_workspace/response_and_resubmission_v1.md` for the point-by-point response.",
))

R.append((
    'scripts list',
    r"""│   └── fig_ga.py                    — Graphical abstract (GA_process.png)""",
    r"""│   ├── fig_ga.py                    — Graphical abstract (GA_process.png)
│   ├── monte_carlo_v2.py            — Ten-parameter Monte Carlo (adds gammas, liquidus, solubility,
│   │                                  delta, c_red; eta-j correlation; feasibility probabilities)
│   ├── dual_temperature.py          — 600/620/650 C recomputation of voltages, window and energy
│   ├── fig_flowsheet.py             — Process flowsheet (Figure 1 of the revision)
│   ├── fig_mechanism.py             — Ca/MgO competition diagram + two-channel scheme
│   ├── verify_r3_reviewer3.py       — Ca + MgO -> CaO + Mg thermochemistry and design criteria
│   ├── revision_r3_mechanism_numbers.py — Numbers moved by the mechanism reconstruction
│   ├── verify_r1_liquidus.py        — Quaternary liquidus check + entrained-salt estimate
│   ├── analyze_length.py            — Paragraph/section length audit for the editorial trim
│   └── apply_*_*.py                 — Scripted edits applied to manuscript.tex (anchor-checked)""",
))

R.append((
    'figures list',
    r"""├── figures_eps/                    — 12 submission EPS figures, named in citation order
│   ├── figure1.eps  … figure12.eps  (uploaded to ScholarOne in this order)""",
    r"""├── figures_eps/                    — submission EPS figures (figure8/figure9 regenerated from the
│   │                                  ten-parameter Monte Carlo)
│   ├── figure1.eps  … figure12.eps
│   ├── figure_flowsheet.eps         — process flowsheet (new)
│   ├── figure_r3_competition.eps    — competing reduction paths (new)
│   └── figure_r3_shuttle.eps        — two oxygen-transfer channels (new)""",
))

R.append((
    'key results',
    r"""- Net energy consumption: 12,552 kWh/ton-Ti at the nominal design point (η_I = 0.75, V_cell = 4.1 V; conditional on η_I > 0.70; heat-integration credit capped at 329 kWh/ton, reaction exotherm rejected as waste heat)
- Monte Carlo (N = 10⁵, seed = 42): median 13,141 kWh/ton-Ti, P(W_net < 15,000 kWh/ton) = 82.1%""",
    r"""- **Ca reduces MgO**: ΔG°(Ca + MgO → CaO + Mg) = −38.2 kJ/mol at 600 °C, K = 194; consequently Ca is the
  thermodynamic deoxidation driver and Mg's role is to keep the reductant *liquid* at 600 °C (both pure metals are
  solid there; the Mg–Ca eutectic is ≈517 °C)
- **New design criteria**: the Ca-vs-MgO crossover is identically the Mg-only deoxidation limit (3,910 ppm), and
  continuing below it requires a_MgO < 5 × 10⁻³
- Net energy consumption: 12,552 kWh/ton-Ti (Case II: MgO + CaO regenerated) or 12,933 kWh/ton-Ti (Case I: CaO the
  sole regenerated species, +3%); conditional on η_I > 0.70
- Monte Carlo, ten parameters (N = 10⁵, seed = 42): median 13,141 kWh/ton-Ti, P(W_net < 15,000) = 82.1%; with the
  η–j correlation included, median 13,981 and P = 65.9%; joint feasibility at 620 °C = 95.8%
- SCM time, ten-parameter median 13.6 min (the nominal 6.3 min corresponds to c_red = 3 mol%)
- Required interelectrode gap for the equimolar deposit: median 0.84 cm, P95 1.88 cm
- 620 °C (pilot floor): window 119.6 mV (from 120.2 mV), energy change < 0.3%""",
))

R.append((
    'limitations',
    r"""The current-efficiency assumption (η_I = 0.75–0.80) is an unvalidated hypothesis anchored to the Hall–Héroult, Downs, and industrial MgCl₂-electrolysis analogies, and is the dominant uncertainty in the energy estimate (Monte Carlo Spearman ρ = −0.85).""",
    r"""The current-efficiency assumption (η_I = 0.75–0.80) is an unvalidated hypothesis anchored to the Hall–Héroult,
Downs, and industrial MgCl₂-electrolysis analogies, and is the dominant uncertainty in the energy estimate
(Monte Carlo Spearman ρ = −0.85). Adding the η–j correlation raises the median net consumption to 13,981 kWh/ton-Ti
and lowers P(W_net < 15,000) to 65.9%.

The two quantities that cannot be computed — the 600 °C CaO solubility and the interfacial kinetics of
Ca + MgO → CaO + Mg — are identified as the pivotal measurements, and go/no-go criteria are stated so that the
design basis can be falsified by a small number of experiments.""",
))


def main():
    with io.open(PATH, encoding='utf-8') as f:
        text = f.read()
    problems = [f'{n}: anchor found {text.count(o)} times' for n, o, _ in R if text.count(o) != 1]
    if problems:
        print('ABORTED:')
        for p in problems:
            print('   ', p)
        sys.exit(1)
    for name, old, new in R:
        text = text.replace(old, new, 1)
        print(f'  [ok] {name}')
    with io.open(PATH, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)
    print('  README.md updated')


if __name__ == '__main__':
    main()
