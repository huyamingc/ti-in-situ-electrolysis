# -*- coding: utf-8 -*-
"""Apply the R3-1 mechanism reconstruction to manuscript.tex (stage 1).

Changes
  1. Rewrite the deoxidation-limit discussion (the long line L277) so that the
     Ca + MgO -> CaO + Mg thermochemistry, the 3908 ppm crossover identity and the
     a_MgO ceiling are stated explicitly, and the Mg/Ca division of labour is
     restated as "Ca = thermodynamic depth, Mg = liquid carrier".
  2. Update the caption of Table tab:deox to say what its two columns now mean.
  3. Add Limitation (10) on the Ca-MgO interfacial kinetics and the Mg inventory
     balance, which the new text cross-references.

Run from the repository root.  A backup exists at
review_workspace/manuscript_before_r3.tex.
"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, 'manuscript.tex')

NEW_BODY = r"""
\emph{The two reductants are not independent: Ca reduces MgO.} The endpoints above treat Mg and Ca as separate deoxidants, but in the process they coexist in one liquid alloy and one melt, and the two oxides are not equally stable. Taking the difference of the two reduction pathways of Table~\ref{tab:thermo},
\begin{equation}
\label{eq:camgo}
\ce{Ca + MgO -> CaO + Mg}, \qquad \Delta G^{\circ}(873~\mathrm{K}) = -38.2~\mathrm{kJ/mol}, \qquad K_2 \equiv \frac{a_{\ce{CaO}}\,a_{\mathrm{Mg}}}{a_{\mathrm{Ca}}\,a_{\ce{MgO}}} = 194 .
\end{equation}
This is not an additional assumption but a direct consequence of the data already used in Table~\ref{tab:thermo} (row~2 minus row~1): MgO is thermodynamically unstable whenever the alloy carries an appreciable Ca activity. Two design consequences follow.

First, the roles of the two metals must be restated. Ca is the stronger deoxidant and remains so in the alloy, whereas Mg contributes no additional deoxidation driving force. What Mg contributes is the physical state of the reductant: pure Ca melts at 842~$^{\circ}$C and pure Mg at 650~$^{\circ}$C, so at the 600~$^{\circ}$C design temperature both pure metals are solid, whereas the Mg--Ca alloy (eutectic $\approx$517~$^{\circ}$C) is liquid and can wet and penetrate the porous Ti product layer. The bimetallic rationale is therefore thermodynamic depth from Ca plus a liquid, transport-capable reductant phase from Mg, rather than a partition of the oxygen between the two metals.

Second, deep deoxidation acquires an explicit constraint on the activity of dissolved MgO. Comparing the driving force of $\ce{Ca + [O] -> CaO}$ with that of reaction~\ref{eq:camgo} at equal Ca activity gives the identity
\begin{equation}
\label{eq:cross}
\Delta G(\ce{Ca + MgO -> CaO + Mg}) - \Delta G_{\mathrm{deox}}(\ce{Ca}) = -\Delta G_{\mathrm{deox}}(\ce{Mg}),
\end{equation}
so the oxygen content separating the two regimes---above it Ca preferentially attacks the residual oxygen in Ti, below it Ca preferentially reduces dissolved MgO---is \emph{identically} the Mg-only endpoint, 3908~ppm. To continue below that level towards the Ca endpoint, the activity of dissolved MgO must satisfy
\begin{equation}
\label{eq:amgo}
a_{\ce{MgO}} < \frac{K_1}{K_2}\,w_{[\mathrm{O}]}\,a_{\mathrm{Mg}} \approx 5\times10^{-3} \qquad (w_{[\mathrm{O}]} = 77~\mathrm{ppm},\; a_{\mathrm{Mg}} = 0.263),
\end{equation}
with $K_1 = \exp[-\Delta G^{\circ}_{\mathrm{deox}}(\ce{Ca})/RT]$. A low MgO solubility is consequently not merely tolerable but \emph{required}: dissolved MgO must be continuously removed rather than accumulated (see the Oxide Dissolution section).

The alloy-state correction then applies as before: with $a_M = \gamma_{\mathrm{alloy}} x_M = 0.526 \times 0.5 = 0.263$, both endpoints rise by a factor of $\sim$3.8 ($\sim$14{,}900~ppm for Mg, $\sim$77~ppm for Ca), and the design-relevant deoxidation depth is the alloy-corrected Ca value of $\sim$77~ppm---still far below the 0.10--0.20~wt\% commercial target. The Mg rows of Table~\ref{tab:deox} are accordingly the endpoint of Mg acting alone, which by Eq.~\ref{eq:camgo} is simultaneously the crossover below which Ca begins to consume MgO, while the Ca rows give the design-relevant depth. Because $w_{[\mathrm{O}]} \propto 1/a_{\mathrm{M}}$, the depth is composition-dependent: in a Ca-dilute local region ($x_{\mathrm{Ca}} = 0.1$, $\gamma_{\mathrm{Ca(alloy)}} = 0.125$, $a_{\mathrm{Ca}} = 0.0125$) the Ca endpoint rises to $\sim$1{,}600~ppm.

It should also be emphasized that $a_M = 0.263$ is a \emph{global} equimolar average; the cathode-surface alloy composition varies spatially and temporally, so the local equilibrium oxygen content is inhomogeneous. Which of the two limiting oxygen-transfer pictures applies---Mg and Ca each carrying roughly half of the oxygen (the 1:1 balance of Table~\ref{tab:mbalance}), or Ca acting as the sole net oxygen carrier---is decided by the competition between MgO dissolution and electrolytic regeneration on the one hand and its chemical reduction by the alloy at the alloy/salt interface on the other. That competition is kinetic rather than thermodynamic: the 1:1 material balance requires the electrolytic pathway to dominate, whereas if reaction~\ref{eq:camgo} is fast the regenerated species becomes CaO, the decomposition voltage rises from 2.73 to 2.83~V and the net energy consumption from 12{,}552 to 12{,}933~kWh/ton-Ti ($+$3\%; see the Material and Energy Balance section). Both limits lie below the FFC range, so the energy conclusion is unaffected either way. The interfacial kinetics of reaction~\ref{eq:camgo} are therefore identified as the critical unmeasured parameter of the proposed mechanism (Limitations~(10)).
"""

NEW_CAPTION = (r"\caption{Equilibrium oxygen content in titanium. Columns ``$a_M=1$'' assume pure metal; "
               r"columns ``$a_M=0.263$'' account for the Mg--Ca liquid alloy activity "
               r"($\gamma_{\mathrm{alloy}}=0.526$, $x_M=0.5$). The Mg rows give the endpoint of Mg acting alone "
               r"and, because Ca reduces MgO (Eq.~\ref{eq:camgo}), also the oxygen content below which Ca begins "
               r"to consume dissolved MgO; the Ca rows give the design-relevant deoxidation depth, subject to "
               r"$a_{\ce{MgO}} \lesssim 5\times10^{-3}$ (Eq.~\ref{eq:amgo}).}")

NEW_LIMITATION = r"""
(10) \textbf{Ca--MgO interfacial kinetics}: Ca reduces MgO thermodynamically (Eq.~\ref{eq:camgo}, $\Delta G^{\circ}(873~\mathrm{K}) = -38.2$~kJ/mol), so the steady-state partition of oxygen between Mg and Ca depends on the competition between MgO dissolution/electrolytic regeneration and its chemical reduction by the alloy at the alloy/salt interface. Neither the interfacial rate of reaction~\ref{eq:camgo} nor the MgO dissolution kinetics at 600~$^{\circ}$C is known. The 1:1 material balance of Table~\ref{tab:mbalance} assumes the electrolytic pathway dominates; the opposite limit (Ca as the sole net oxygen carrier) raises the net energy consumption from 12{,}552 to 12{,}933~kWh/ton-Ti. This kinetic competition is the most important unmeasured input for the mechanism, and the same balance governs the Mg inventory: Mg deposited at its diffusion limit must have an outlet (evaporation, entrainment, or periodic alloy withdrawal) if it is not to accumulate in the alloy pool.
"""


def main():
    with io.open(PATH, encoding='utf-8') as f:
        text = f.read()
    lines = text.split('\n')

    # ---------- 1. rewrite the long deoxidation-limit line ----------
    idx = None
    for i, ln in enumerate(lines):
        if ln.startswith('where both terms are on a 1~mol O basis') and 'Ca + MgO' not in ln:
            idx = i
            break
    if idx is None:
        sys.exit('ERROR: target line not found (already patched?)')
    old = lines[idx]
    marker = ' The equilibrium constant $K = '
    if marker not in old:
        sys.exit('ERROR: split marker not found in the target line')
    head = old[:old.index(marker)]
    tail_marker = 'The temperature-dependent dissolution free energy'
    if tail_marker not in old:
        sys.exit('ERROR: tail marker not found')
    tail = old[old.index(tail_marker):]

    new_line = (head
                + '\nThe equilibrium constant $K = \\exp(-\\Delta G^{\\circ}_{\\mathrm{deox}}/RT)$ yields '
                  '$w_{[\\mathrm{O}]} = 1/K$ (Henry\'s law, dilute solution). At 600~$^{\\circ}$C, Mg deoxidation '
                  'yields 3908~ppm O while Ca reaches 20.2~ppm---a 193$\\times$ difference (Table~\\ref{tab:deox}).\n'
                + NEW_BODY + '\n' + tail)
    lines[idx:idx + 1] = new_line.split('\n')
    print(f'  [1] deoxidation-limit line rewritten ({len(old)} -> {len(new_line)} chars, '
          f'{len(new_line.splitlines())} lines)')

    # ---------- 2. update the Table 3 caption ----------
    hit = 0
    for i, ln in enumerate(lines):
        if ln.startswith('\\caption{Equilibrium oxygen content in titanium.'):
            lines[i] = NEW_CAPTION
            hit += 1
    print(f'  [2] Table tab:deox caption updated ({hit} occurrence)')
    if hit != 1:
        sys.exit('ERROR: expected exactly one caption to replace')

    # ---------- 3. add Limitation (10) ----------
    hit = 0
    for i, ln in enumerate(lines):
        if ln.startswith('\\section*{Conclusions}'):
            lines[i:i] = NEW_LIMITATION.strip('\n').split('\n') + ['']
            hit += 1
            break
    print(f'  [3] Limitation (10) inserted before Conclusions ({hit})')
    if hit != 1:
        sys.exit('ERROR: Conclusions section not found')

    with io.open(PATH, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(lines))
    print(f'  written: {PATH}')


if __name__ == '__main__':
    main()
