# -*- coding: utf-8 -*-
"""R3-1 editorial trim, batch B1: compress the four most repetitive long blocks.

  * L533 (4,301 chars) current-efficiency justification  -> ~1,700
        (its loss-mechanism list and caveats are already repeated in Limitations 9)
  * L434 (4,038 chars) Monte Carlo paragraph             -> ~2,450
        (percentile details duplicated in Abstract and Conclusions)
  * L551 (2,225 chars) exergy accounting note            -> ~1,250
  * L652 (1,690 chars) moisture paragraph                -> ~730  (R3 asked to cut it)

Replacement is done by locating a unique start anchor and a unique end anchor and
replacing the span between them, so the long originals need not be reproduced
verbatim.  Nothing is written unless every anchor is found exactly once.
"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, 'manuscript.tex')

BLOCKS = []

BLOCKS.append((
    'current-efficiency justification',
    r"The assumed current efficiency range ($\eta_I = 0.75$--0.80) requires justification",
    r"the ``energy-efficient'' characterization of this process is \emph{conditional on achieving $\eta_I > 0.70$}.",
    r"""The assumed current efficiency range ($\eta_I = 0.75$--0.80) requires justification, as it significantly exceeds the FFC Cambridge process (30--50\%) \cite{fray2000}. The difference is mechanistic: FFC electro-deoxidises solid $\ce{TiO2}$ at the cathode, where slow solid-state diffusion and side reactions cause severe current leakage, whereas the present process electrolyses dissolved oxides and therefore resembles the Hall--H\'eroult process (dissolved $\ce{Al2O3}$, $\eta_I = 90$--95\% \cite{kvande2014}), the Downs process for sodium (70--90\%), and industrial $\ce{MgCl2}$ electrolysis (80--90\%) \cite{ji2026,pletcher1990}. The expected loss mechanisms are (i) electronic conduction in the melt (2--5\%), (ii) chemical back-dissolution of freshly deposited Mg/Ca by dissolved oxide species (5--10\%), (iii) Na co-deposition at high current density (3--8\%), and (iv) impurity side reactions (2--5\%); their sum, $\eta_I \approx 0.72$--0.88, centres on the assumed range. These estimates are treated as additive and independent, and mechanisms (ii) and (iii) both worsen with current density, so the attainable $\eta_I$ at the co-deposition design point ($j \approx 1.1$~A/cm$^2$) may lie below that sum. The Monte Carlo analysis propagates $\eta_I$ as an independent distribution and does not encode this $\eta_I$--$j$ correlation, which requires experimental polarization data for the quaternary melt (Limitations~(9)). The target range is therefore an \emph{unvalidated hypothesis}; if $\eta_I$ proves to be 0.50--0.60, the energy consumption rises to $\sim$15{,}200--19{,}600~kWh/ton-Ti, within the FFC range, so the energy advantage of this process is \emph{conditional on achieving $\eta_I > 0.70$}.""",
))

BLOCKS.append((
    'Monte Carlo paragraph',
    r"To propagate uncertainties globally, a Monte Carlo simulation ($N = 10^5$, fixed random seed $= 42$ for reproducibility) was performed",
    r"governed more critically by the 600~$^{\circ}$C oxide solubility and the liquidus.",
    r"""To propagate uncertainties globally, a Monte Carlo simulation ($N = 10^5$, fixed random seed $= 42$ for reproducibility) sampled five parameters simultaneously: $D \sim U(1, 3) \times 10^{-9}$~m$^2$/s, $\varepsilon \sim U(0.1, 0.5)$, $\tau \sim U(1.5, 5.0)$, $\eta_I \sim \mathrm{Tri}(0.50, 0.75, 0.88)$, and $V_{\mathrm{cell}} \sim \mathcal{N}(4.1, 0.3)$ truncated to [3.5, 4.5]~V. The $\eta_I$ prior spans the worst-case FFC-like range without presupposing a feasibility threshold, and $\varepsilon$ and $\tau$ are sampled as independent uniform variables although they are physically negatively correlated, which makes the resulting $D_{\mathrm{eff}}$ spread conservative. The results (Fig.~\ref{fig:monte_carlo}) give a lognormal SCM reduction time (median 7.2~min, P5--P95: 2.7--21.8~min) and a right-skewed net energy consumption (median 13{,}141~kWh/ton-Ti, P5--P95: 10{,}875--16{,}722~kWh/ton-Ti on the Case~II basis of Table~\ref{tab:mbalance}; the CaO-only Case~I shifts the distribution upward by $\sim$3\%). The probability of beating the nominal 12{,}552~kWh/ton-Ti is 35.8\%, and $P(W_{\mathrm{net}} < 15{,}000) = 82.1\%$; the latter threshold is the lower bound of the FFC route, so that figure largely restates the assumed $\eta_I$ prior rather than providing an independent feasibility estimate. Spearman analysis (Fig.~\ref{fig:tornado}) shows that $\eta_I$ ($\rho = -0.85$) dominates the energy uncertainty ahead of $V_{\mathrm{cell}}$ ($\rho = 0.50$), while $\varepsilon$ ($\rho = -0.67$) and $\tau$ ($\rho = 0.52$) dominate the SCM time, so experimental validation of current efficiency is the most critical prerequisite for the energy claim. The present analysis does not include uncertainties in $\gamma_{\ce{CaCl2}}$, liquidus temperature, oxide solubility, the diffusion-layer thickness $\delta$ (fixed at 200~$\mu$m), the dissolved-reductant concentration $c_{\mathrm{red}}$, or the current-density dependence of $\eta_I$. These omitted terms act principally on \emph{feasibility} rather than on the per-ton energy: the $\gamma_{\ce{CaCl2}}$ scan changes the co-deposition window by 60--75~mV but never closes it, the liquidus constrains the operable temperature (Limitations~(4)), and the oxide solubility changes the required salt inventory by a factor of 2--4. The energy prediction is therefore dominated by $\eta_I$, whereas process feasibility is governed by the 600~$^{\circ}$C oxide solubility and the liquidus.""",
))

BLOCKS.append((
    'exergy accounting note',
    r"\emph{Accounting note: thermal and electrical energy differ in quality (exergy).",
    r"which is itself part of that same thermal demand.",
    r"""\emph{Accounting note: thermal and electrical energy differ in quality (exergy). The heat-integration credit adopted above is capped at the 329~kWh/ton external thermal demand and requires no conversion of heat to work; no Carnot-limited work recovery from the $\sim$6{,}761~kWh/ton of rejected waste heat is credited.} The process energy efficiency---the ratio of the electrolysis step's theoretical minimum (6{,}112~kWh/ton) to the net equivalent external energy consumption (12{,}552~kWh/ton)---is 48.7\%, reflecting the combined irreversibilities of electrolysis (voltage efficiency $\approx$67\%, current efficiency 75--80\%) and thermal losses. The true second-law (exergetic) efficiency is lower: the net reaction $\ce{TiO2 -> Ti + O2}$ has a reversible work of $\sim$4{,}550~kWh/ton-Ti ($\Delta G^{\circ}_{\ce{TiO2}} \approx 783$~kJ/mol at 873~K), giving 36.3\%. The two differ because the electrolysis step must also regenerate the Mg/Ca mediators, whose decomposition energy exceeds the reversible work of the net reaction. The electrolysis energy fraction of 97.2\% indicates that electrolysis dominates the external energy budget; it is \emph{not} a thermodynamic efficiency.""",
))

BLOCKS.append((
    'moisture paragraph',
    r"A third chemical constraint on the salt cycle, distinct from the anode-side chlorine chemistry discussed above, is the moisture sensitivity",
    r"but it must be met before the assumed $\eta_I = 0.75$--0.80 can be pursued experimentally.",
    r"""A final constraint is the moisture sensitivity of the $\ce{MgCl2}$-bearing salt: anhydrous $\ce{MgCl2}$ cannot be obtained by open thermal dehydration (hydrolysis above $\sim$200--300~$^{\circ}$C gives $\ce{MgOHCl}$ + HCl), so improperly dried salt opens a parasitic hydrogen-evolution channel and releases HCl that re-chlorinates the freshly deposited reductant \cite{song2024}. Industrial $\ce{MgCl2}$ electrolysis controls this by vacuum dehydration or chlorinating pretreatment under a dry atmosphere \cite{pletcher1990}; these standard measures are assumed here, and the dehydration energy of the small makeup-salt stream is not itemised in Table~\ref{tab:heatbal}. Moisture is therefore an avoidable engineering requirement rather than an intrinsic limitation, but it must be met before the assumed $\eta_I = 0.75$--0.80 can be pursued experimentally.""",
))


def main():
    with io.open(PATH, encoding='utf-8') as f:
        text = f.read()

    # verify uniqueness of every anchor first
    problems = []
    for name, start, end, _new in BLOCKS:
        if text.count(start) != 1:
            problems.append(f'{name}: start anchor found {text.count(start)} times')
        if text.count(end) != 1:
            problems.append(f'{name}: end anchor found {text.count(end)} times')
    if problems:
        print('ABORTED - no changes written:')
        for p in problems:
            print('   ', p)
        sys.exit(1)

    # apply from the end backwards so earlier offsets stay valid
    for name, start, end, new in BLOCKS:
        i = text.index(start)
        j = text.index(end, i) + len(end)
        old_len = j - i
        text = text[:i] + new + text[j:]
        print(f'  [ok] {name}: {old_len} -> {len(new)} chars '
              f'({100*(len(new)-old_len)/old_len:+.0f}%)')

    with io.open(PATH, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)
    print(f'  written: {PATH}')


if __name__ == '__main__':
    main()
