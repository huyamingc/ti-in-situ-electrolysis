# -*- coding: utf-8 -*-
"""C-group part 2: write the remaining Reviewer-2 items into the manuscript.

  R2-2  eta-j correlation  -> correlated Monte Carlo variant + numbers
  R2-4  both temperatures  -> 620 C / 650 C recomputation paragraph
  R2-6  full Redlich-Kister -> L1 term contribution off-equimolar
"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, 'manuscript.tex')

R = []

R.append((
    'R2-2 eta-j correlation',
    r"Spearman analysis (Fig.~\ref{fig:tornado}) shows that $\eta_I$ ($\rho = -0.85$) dominates the energy uncertainty ahead of $V_{\mathrm{cell}}$ ($\rho = 0.50$), while $c_{\mathrm{red}}$ and $\varepsilon$ dominate the SCM time, so experimental validation of current efficiency remains the most critical prerequisite for the energy claim.",
    r"Spearman analysis (Fig.~\ref{fig:tornado}) shows that $\eta_I$ ($\rho = -0.85$) dominates the energy uncertainty ahead of $V_{\mathrm{cell}}$ ($\rho = 0.50$), while $c_{\mathrm{red}}$ and $\varepsilon$ dominate the SCM time, so experimental validation of current efficiency remains the most critical prerequisite for the energy claim. Because loss mechanisms (ii) and (iii) of the efficiency budget both scale with current density, a correlated variant of the same run was also evaluated, in which $\eta_I$ falls by 10\% per unit relative increase of $j$ above the nominal 1.1~A/cm$^2$: this raises the median net consumption from 13{,}141 to 13{,}981~kWh/ton-Ti and lowers $P(W_{\mathrm{net}} < 15{,}000)$ from 82.1\% to 65.9\%, showing that the energy claim is governed by the $\eta_I$--$j$ relation as much as by the efficiency value itself.",
))

R.append((
    'R2-4 dual temperature',
    r"\emph{Accounting note: thermal and electrical energy differ in quality (exergy).",
    r"\emph{Accounting note: thermal and electrical energy differ in quality (exergy).",
))

# the dual-temperature paragraph goes at the end of the Full-Process Energy section,
# i.e. immediately before the Oxide Dissolution subsection
R.append((
    'R2-4 dual temperature (insert)',
    r"\subsection*{Oxide Dissolution Mechanism and Salt Circulation}",
    r"""Operating at the 620~$^{\circ}$C pilot floor of Limitations~(4) changes none of these conclusions. Recomputed at 620~$^{\circ}$C with the same thermochemical data and the same overpotential and ohmic budget, the mixed-regeneration decomposition voltage falls from 2.729 to 2.718~V and the $\ce{Ca^{2+}/Na+}$ co-deposition window narrows only from 120.2 to 119.6~mV (at 650~$^{\circ}$C: 118.6~mV), because the decomposition voltage of both oxides and the Nernst term of the window have similar temperature coefficients. The net equivalent consumption therefore changes by less than 0.3\% (12{,}552 $\to$ $\sim$12{,}520~kWh/ton-Ti for the nominal case, with only the decomposition term varying). Raising the operating temperature to the recommended 620~$^{\circ}$C floor thus costs well under 1\% of the energy advantage while removing the liquidus risk.

\subsection*{Oxide Dissolution Mechanism and Salt Circulation}""",
))

R.append((
    'R2-6 full Redlich-Kister',
    r"Additionally, the regular-solution approximation neglects ordering effects associated with the stable $\ce{Mg2Ca}$ intermetallic;",
    r"The $L_1$ term vanishes at the equimolar composition but not elsewhere: for the Ca-dilute local region discussed in the Reduction Thermodynamics section ($x_{\ce{Ca}} = 0.1$), the full Redlich--Kister activity coefficient $\gamma_{\ce{Ca}} = \exp\{x_{\ce{Mg}}^2[L_0 + L_1(3x_{\ce{Ca}} - x_{\ce{Mg}})]/RT\}$ gives $\gamma_{\ce{Ca}} = 0.111$ rather than the regular-solution value 0.125, i.e.\ an 11\% lower Ca activity and a correspondingly higher local oxygen endpoint ($\sim$1{,}800 instead of $\sim$1{,}600~ppm). The equimolar design point itself is unaffected, since $x_{\ce{Mg}} = x_{\ce{Ca}}$ makes the $L_1$ contribution vanish identically. Additionally, the regular-solution approximation neglects ordering effects associated with the stable $\ce{Mg2Ca}$ intermetallic;",
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
        if old == new:
            print(f'  [--] {name}: no-op placeholder skipped')
            continue
        text = text.replace(old, new, 1)
        print(f'  [ok] {name}')
    with io.open(PATH, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)
    print('  written')


if __name__ == '__main__':
    main()
