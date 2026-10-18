# -*- coding: utf-8 -*-
"""R3-1 reconstruction, batch 2: material/energy tables and companion sections.

  * Table tab:mbalance -> two cases (Case II 1:1, Case I CaO-only)
  * Material and Energy Balance: add the Case I decomposition-voltage paragraph
  * Full-Process Energy Balance: add the Case I gross demand
  * Cathode Mass Transport: add the deposit-ratio / Mg-inventory paragraph
  * Oxide Dissolution: add the CaO-regeneration + a_MgO framing
  * Process Description: refine the four-step cycle wording
  * Process Comparison: refine the key-distinction sentence
  * Limitations (6): add the CaO-vs-MgO re-framing

Anchors are uniqueness-checked; nothing is written unless every anchor matches once.
"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, 'manuscript.tex')

R = []

# ---------------------------------------------------------------- Table 6
OLD_T6 = r"""\caption{Material balance (basis: 1 ton Ti, pure $\ce{TiO2}$)}
\label{tab:mbalance}
\begin{tabular}{llc}
\toprule
Category & Item & Mass (kg) \\
\midrule
Input & $\ce{TiO2}$ (pure) & 1668 \\
 & Mg (cyclic) & 508 \\
 & Ca (cyclic) & 837 \\
\midrule
Output & Ti metal & 1000 \\
 & $\ce{MgO}$ (to regeneration) & 842 \\
 & $\ce{CaO}$ (to regeneration) & 1171 \\
\midrule
Check & Input total & 3013 \\
 & Output total & 3013 \\
\midrule
Net & $\ce{TiO2} \to \ce{Ti} + \ce{O2}$ & 1668 = 1000 + 668 \\
\bottomrule
\end{tabular}
\end{table}"""

NEW_T6 = r"""\caption{Material balance (basis: 1 ton Ti, pure $\ce{TiO2}$). Case~II is the design point used in this work, in which MgO and CaO are both regenerated electrolytically so that Mg and Ca each carry about half of the oxygen; Case~I is the limit in which Ca acts as the sole net oxygen carrier and the regenerated species is CaO (Eq.~\ref{eq:camgo}). The two cases differ only in which oxide is returned to the cell.}
\label{tab:mbalance}
\begin{tabular}{llcc}
\toprule
Category & Item & Case~II (kg) & Case~I (kg) \\
\midrule
Input & $\ce{TiO2}$ (pure) & 1668 & 1668 \\
 & Mg (cyclic) & 508 & $\le$1016 (net zero)$^{\mathrm{a}}$ \\
 & Ca (cyclic) & 837 & 1675 \\
\midrule
Output & Ti metal & 1000 & 1000 \\
 & $\ce{MgO}$ (to regeneration) & 842 & --- \\
 & $\ce{CaO}$ (to regeneration) & 1171 & 2343 \\
\midrule
Net & $\ce{TiO2} \to \ce{Ti} + \ce{O2}$ & \multicolumn{2}{c}{1668 = 1000 + 668} \\
\bottomrule
\end{tabular}

\par\footnotesize $^{\mathrm{a}}$In Case~I the Mg shuttles oxygen between the Ti particle surface and the Ca dissolved in the alloy---Mg is oxidised to MgO and chemically reduced back to Mg by Ca (Eq.~\ref{eq:camgo})---so its net chemical consumption is zero and only the amount needed to offset evaporation and entrainment must be replenished. The value quoted is the round-trip throughput, not a net consumption.
\end{table}"""

R.append(('Table 6 -> two cases', OLD_T6, NEW_T6))

# ------------------------------------------- Material and Energy Balance text
R.append((
    'energy section: Case I decomposition voltage',
    r"The theoretical decomposition voltage for simultaneous regeneration of MgO and CaO (4~e$^-$ per mol Ti) is 2.73~V, giving a theoretical minimum electrolysis energy of 6112~kWh/ton-Ti.",
    r"The theoretical decomposition voltage for simultaneous regeneration of MgO and CaO (4~e$^-$ per mol Ti) is 2.73~V, giving a theoretical minimum electrolysis energy of 6112~kWh/ton-Ti. "
    r"In the CaO-only limit (Case~I of Table~\ref{tab:mbalance}) the corresponding values are "
    r"$2\Delta G^{\circ}_{f}(\ce{CaO})/4F = 2.83$~V and 6334~kWh/ton-Ti. Because the charge transferred per mole of Ti "
    r"is unchanged at 4~e$^-$, the only penalty of the CaO-only limit is the 99~mV higher decomposition voltage: the "
    r"gross electrolysis demand rises from 12{,}244 to 12{,}632~kWh/ton-Ti and the net equivalent consumption from "
    r"12{,}552 to 12{,}933~kWh/ton-Ti ($+$3\%). Which case applies is decided by the kinetics of Eq.~\ref{eq:camgo} "
    r"(Limitations~(10)); both are carried through this section so that the energy conclusion does not depend on that "
    r"unresolved question.",
))

# --------------------------------------------- Full-Process Energy Balance
R.append((
    'heat-balance section: Case I gross demand',
    r"The electrolysis gross electrical demand is 12{,}244~kWh/ton ($\eta_I=0.75$, $V_{\mathrm{cell}}=4.1$~V).",
    r"The electrolysis gross electrical demand is 12{,}244~kWh/ton ($\eta_I=0.75$, $V_{\mathrm{cell}}=4.1$~V), "
    r"or 12{,}632~kWh/ton at $V_{\mathrm{cell}}=4.23$~V in the CaO-only Case~I of Table~\ref{tab:mbalance}.",
))

# ------------------------------------------------ Cathode Mass Transport
R.append((
    'mass transport: Mg inventory / deposit ratio',
    r"which is precisely the condition under which Regime~II exists.",
    r"which is precisely the condition under which Regime~II exists.\n\n"
    r"Because the deposit ratio is fixed by $j_{\mathrm{lim,Mg}}/j$ rather than by the melt composition, the "
    r"equimolar design point also fixes the Mg:Ca ratio of the metal entering the alloy. Since Mg is chemically "
    r"regenerated by Ca (Eq.~\ref{eq:camgo}) and therefore has no net chemical consumption, the continuously deposited "
    r"Mg must have an outlet---evaporation (the Mg vapour pressure is $\approx$180~Pa at 600~$^{\circ}$C), entrainment "
    r"in the product, or periodic alloy withdrawal---if it is not to accumulate in the alloy pool and raise "
    r"$a_{\mathrm{Mg}}$ at the expense of $a_{\mathrm{Ca}}$. Lowering the $\ce{MgCl2}$ fraction reduces "
    r"$j_{\mathrm{lim,Mg}}$ and shifts the deposit towards Ca (at $x_{\ce{MgCl2}} = 0.10$ the Mg share falls from 51\% "
    r"to 17\%), at the cost of a higher liquidus. This inventory balance is an additional design constraint that the "
    r"present conceptual study does not resolve (Limitations~(10)).",
))

# ------------------------------------------------------- Oxide Dissolution
R.append((
    'oxide dissolution: CaO regeneration + a_MgO',
    r"A critical feature of the process is the dissolution of $\ce{MgO}$ and $\ce{CaO}$ in the $\ce{CaCl2}$-containing melt.",
    r"Under the reconstructed mechanism (Eq.~\ref{eq:camgo}) the species that must be dissolved and electrolytically "
    r"regenerated in the steady state is predominantly CaO rather than a MgO--CaO mixture, and the activity of "
    r"dissolved MgO must be held below $\approx 5\times10^{-3}$ (Eq.~\ref{eq:amgo}). A low MgO solubility is therefore "
    r"consistent with, and in fact required by, the design: MgO must leave the reaction zone as it forms rather than "
    r"accumulate. Because CaO solubility in $\ce{CaCl2}$-rich melts is substantially higher than that of MgO, the "
    r"closed-loop constraint under this picture is less severe than the MgO threshold analysed below; that analysis is "
    r"retained because it bounds the MgO side of the cycle and hence the Mg inventory.\n\n"
    r"A critical feature of the process is the dissolution of $\ce{MgO}$ and $\ce{CaO}$ in the $\ce{CaCl2}$-containing melt.",
))

# ------------------------------------------------------- Process Description
R.append((
    'process description: cycle items ii and iv',
    r"(ii) reduction of $\ce{TiO2}$ powder by the co-deposited metals; (iii) dissolution of $\ce{MgO}$ and $\ce{CaO}$ in the melt; and (iv) electrolytic regeneration of $\ce{Mg^{2+}}$ and $\ce{Ca^{2+}}$ with oxygen evolution at the anode.",
    r"(ii) reduction of $\ce{TiO2}$ powder by the co-deposited metals, with Ca supplying the thermodynamic driving "
    r"force and Mg keeping the reductant liquid (Eq.~\ref{eq:camgo}); (iii) dissolution of the by-product oxides in the "
    r"melt; and (iv) electrolytic regeneration of the reductant with oxygen evolution at the anode---MgO and CaO in "
    r"Case~II of Table~\ref{tab:mbalance}, predominantly CaO if Ca acts as the sole net oxygen carrier.",
))

# -------------------------------------------------------- Process Comparison
R.append((
    'process comparison: key distinction sentence',
    r"this process uses electrolysis to regenerate reductants in situ while leveraging bimetallic complementary reduction for both rate and purity.",
    r"this process uses electrolysis to regenerate the reductant in situ while leveraging a liquid Mg--Ca alloy in "
    r"which Ca supplies the thermodynamic deoxidation depth and Mg keeps the reductant molten at 600~$^{\circ}$C, "
    r"where both pure metals are solid.",
))

# ------------------------------------------------------------- Limitations (6)
R.append((
    'limitations (6): CaO vs MgO re-framing',
    r"the activation energy is not independently determined, and the range carries a factor-of-2.4 uncertainty.",
    r"the activation energy is not independently determined, and the range carries a factor-of-2.4 uncertainty. "
    r"Under the reconstructed mechanism, however, the design instead requires $a_{\ce{MgO}} \lesssim 5\times10^{-3}$ "
    r"(Eq.~\ref{eq:amgo}) and the regenerated species is predominantly CaO, so the unresolved solubility is that of "
    r"CaO rather than of MgO.",
))


def main():
    with io.open(PATH, encoding='utf-8') as f:
        text = f.read()

    problems = []
    for name, old, _new in R:
        n = text.count(old)
        if n != 1:
            problems.append(f'{name}: anchor found {n} times')
    if problems:
        print('ABORTED - no changes written:')
        for p in problems:
            print('   ', p)
        sys.exit(1)

    for name, old, new in R:
        text = text.replace(old, new, 1)
        print(f'  [ok] {name}')
    with io.open(PATH, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)
    print(f'  written: {PATH}  ({len(R)} replacements)')


if __name__ == '__main__':
    main()
