# -*- coding: utf-8 -*-
"""Insert the two mechanism figures (D group).

  fig:competition -> after the a_MgO criterion paragraph in Reduction Thermodynamics
  fig:shuttle     -> after the Mg-inventory paragraph in Cathode Mass Transport
"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, 'manuscript.tex')

FIG_A = r"""The competition is summarized in Fig.~\ref{fig:competition}.

\begin{figure}[!ht]
\centering
\includegraphics[width=0.80\linewidth]{figure_r3_competition.eps}
\caption{Competing reduction paths at 600~$^{\circ}$C. The driving forces of $\ce{Ca} + [\mathrm{O}]_{\mathrm{Ti}} \to \ce{CaO}$ (red) and $\ce{Mg} + [\mathrm{O}]_{\mathrm{Ti}} \to \ce{MgO}$ (green) both become more negative as the oxygen content rises, whereas that of the cross reaction $\ce{Ca + MgO -> CaO + Mg}$ (blue, standard states) is independent of it. The two curves cross the cross-reaction line at the same oxygen content, 3910~ppm---identically the Mg-only deoxidation limit of Eq.~\ref{eq:cross}---so below that value Ca preferentially consumes dissolved MgO unless $a_{\ce{MgO}} < 5\times10^{-3}$ (Eq.~\ref{eq:amgo}).}
\label{fig:competition}
\end{figure}"""

FIG_B = r"""The two channels are sketched in Fig.~\ref{fig:shuttle}.

\begin{figure}[!ht]
\centering
\includegraphics[width=0.82\linewidth]{figure_r3_shuttle.eps}
\caption{The two oxygen-transfer channels at a $\ce{TiO2}$ particle suspended in the liquid Mg--Ca alloy (schematic, not to scale). Channel~1: Mg reduces the particle, the MgO formed dissolves in the melt and is regenerated electrolytically. Channel~2: Ca reduces the particle and the residual oxygen, and the CaO formed is regenerated. At the alloy/melt interface the cross reaction $\ce{Ca + MgO -> CaO + Mg}$ (Eq.~\ref{eq:camgo}) returns Mg to the alloy; the steady-state split between the channels is set by the kinetics of that reaction relative to MgO dissolution and regeneration, the unmeasured quantity identified in Limitations~(10).}
\label{fig:shuttle}
\end{figure}"""

R = [
    (
        'competition figure after the a_MgO criterion',
        r"with $K_1 = \exp[-\Delta G^{\circ}_{\mathrm{deox}}(\ce{Ca})/RT]$. A low MgO solubility is consequently not merely tolerable but \emph{required}: dissolved MgO must be continuously removed rather than accumulated (see the Oxide Dissolution section).",
        r"with $K_1 = \exp[-\Delta G^{\circ}_{\mathrm{deox}}(\ce{Ca})/RT]$. A low MgO solubility is consequently not merely tolerable but \emph{required}: dissolved MgO must be continuously removed rather than accumulated (see the Oxide Dissolution section). " + FIG_A,
    ),
    (
        'shuttle figure after the Mg-inventory paragraph',
        r"This inventory balance is an additional design constraint that the present conceptual study does not resolve (Limitations~(10)).",
        r"This inventory balance is an additional design constraint that the present conceptual study does not resolve (Limitations~(10)). " + FIG_B,
    ),
]


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
    print('  written')


if __name__ == '__main__':
    main()
