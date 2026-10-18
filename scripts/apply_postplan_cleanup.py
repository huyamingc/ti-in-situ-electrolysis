# -*- coding: utf-8 -*-
"""Post-plan cleanup: fix the 47.3% efficiency definition, repair an edit accident,
compress five long paragraphs (Reviewer 3's "too long"), and report both Monte
Carlo bases in the main MC paragraph.
"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, 'manuscript.tex')

R = []

# ---------------------------------------------------------------- 1. 47.3% -> 49.0%
R.append((
    'Case I process efficiency',
    r"the net consumption 12{,}933~kWh/ton, the process efficiency 47.3\%, the second-law efficiency 35.2\% and the electrolysis fraction 97.3\%.",
    r"the net consumption 12{,}933~kWh/ton, the process efficiency 49.0\% (6334/12{,}933, each case evaluated against its own electrolysis minimum), the second-law efficiency 35.2\% and the electrolysis fraction 97.3\%.",
))

# ---------------------------------------------------------------- 2. MC both bases
R.append((
    'Monte Carlo both bases',
    r"median of 13{,}141~kWh/ton-Ti (P5--P95: 10{,}875--16{,}722~kWh/ton-Ti on the Case~II basis of Table~\ref{tab:mbalance}; the CaO-only Case~I shifts the distribution upward by $\sim$3\%).",
    r"$P(W_{\mathrm{net}} < 15{,}000) = 82.1\%$;",
    r"median of 13{,}141~kWh/ton-Ti (P5--P95: 10{,}875--16{,}722~kWh/ton-Ti) on the Case~II basis of Table~\ref{tab:mbalance}, and 13{,}536~kWh/ton-Ti on the CaO-only Case~I basis. The probability of beating the nominal 12{,}552~kWh/ton-Ti is 35.8\%, and $P(W_{\mathrm{net}} < 15{,}000) = 82.1\%$ (76.6\% for Case~I);",
))

# ---------------------------------------------------------------- 3. Abstract
R.append((
    'Abstract',
    r"This work establishes an electrochemical design basis for titanium production by in situ co-deposition of Mg and Ca, cyclic complementary reductants of $\ce{TiO2}$, in a quaternary chloride melt ($\ce{MgCl2-CaCl2-NaCl-KCl}$). Thermodynamic calculations at 600~$^{\circ}$C give $\Delta G^{\circ} = -231.0$ to $-307.5$~kJ/mol for the reduction pathways, with equilibrium deoxidation limits of 3908~ppm O for pure Mg and 20.2~ppm for pure Ca, the latter rising to $\approx$77~ppm at the equimolar alloy activity. $\ce{Ca + MgO -> CaO + Mg}$ is exergonic at 600~$^{\circ}$C ($\Delta G^{\circ} = -38.2$~kJ/mol; $K = 194$), so Ca supplies the deoxidation driving force while the role of Mg is to keep the reductant liquid at the design temperature---pure Ca and pure Mg are both solid at 600~$^{\circ}$C, whereas the Mg--Ca eutectic is $\approx$517~$^{\circ}$C---and reaching the deep-deoxidation limit then requires the dissolved $\ce{MgO}$ activity to remain below $\approx 5\times10^{-3}$. The $\ce{Ca^{2+}/Na+}$ co-deposition window is 120.2~mV (ideal) and remains positive (74.9--147.1~mV) for $\gamma_{\ce{CaCl2}} = 0.3$--1.0. Mass-transport analysis yields a Mg limiting current density of 0.56~A/cm$^2$; co-deposition spans 0.56--1.31~A/cm$^2$, the equimolar deposit requires $j \approx 1.1$~A/cm$^2$, and the 0.9~V ohmic budget constrains the gap to $\lesssim$1.1~cm. The shrinking-core model predicts complete reduction of 100~$\mu$m particles in 6.3~min. At the nominal design point ($\eta_I = 0.75$, $V_{\mathrm{cell}} = 4.1$~V), the net equivalent energy consumption is 12{,}552~kWh/ton-Ti, rising to 12{,}933~kWh/ton-Ti ($+$3\%) if Ca acts as the sole net oxygen carrier (\emph{i.e.}, if CaO rather than a MgO--CaO mixture is regenerated); this CaO-only limit is the case favoured by the mechanism analysis, because $\ce{Ca + MgO -> CaO + Mg}$ generates no solid product layer, while the 1:1 balance is retained as the conservative design basis. Both figures are \emph{conditional on achieving $\eta_I > 0.70$}. Monte Carlo analysis ($\eta_I \sim \mathrm{Tri}(0.50, 0.75, 0.88)$) gives a median of 13{,}141~kWh/ton-Ti under the conservative basis (13{,}536~kWh/ton-Ti under the CaO-only basis) and $P(W < 15{,}000) = 82.1\%$ (76.6\%). All results are theoretical; viability hinges on adequate $\ce{CaO}$ solubility at 600~$^{\circ}$C (with the dissolved $\ce{MgO}$ activity held below $\approx 5\times10^{-3}$), on the interfacial kinetics that decide whether MgO leaves through electrolytic regeneration or is chemically reduced by Ca, on melt oxoacidity favoring $\ce{O2}$ over $\ce{Cl2}$ evolution, and on a durable oxygen-evolving inert anode.",
    r"This work establishes an electrochemical design basis for titanium production by in situ co-deposition of Mg and Ca, cyclic reductants of $\ce{TiO2}$, in a quaternary chloride melt ($\ce{MgCl2-CaCl2-NaCl-KCl}$). Thermodynamic calculations at 600~$^{\circ}$C give $\Delta G^{\circ} = -231.0$ to $-307.5$~kJ/mol for the reduction pathways, with equilibrium deoxidation limits of 3908~ppm O for Mg and 20.2~ppm for Ca, the latter rising to $\approx$77~ppm at the equimolar alloy activity. $\ce{Ca + MgO -> CaO + Mg}$ is exergonic at 600~$^{\circ}$C ($\Delta G^{\circ} = -38.2$~kJ/mol; $K = 194$), so Ca supplies the deoxidation driving force while Mg keeps the reductant liquid---both pure metals are solid at 600~$^{\circ}$C, the Mg--Ca eutectic melting at $\approx$517~$^{\circ}$C---and reaching the deep-deoxidation limit then requires $a_{\ce{MgO}} < 5\times10^{-3}$. The $\ce{Ca^{2+}/Na+}$ co-deposition window is 120.2~mV (ideal) and remains positive under activity-coefficient sensitivity, and mass transport limits Mg deposition to 0.56~A/cm$^2$: co-deposition spans 0.56--1.31~A/cm$^2$, the equimolar deposit requires $j \approx 1.1$~A/cm$^2$, and the 0.9~V ohmic budget constrains the gap to $\lesssim$1.1~cm. The shrinking-core model predicts complete reduction of 100~$\mu$m particles in 6.3~min. At the nominal design point ($\eta_I = 0.75$, $V_{\mathrm{cell}} = 4.1$~V) the net equivalent energy consumption is 12{,}552~kWh/ton-Ti, or 12{,}933~kWh/ton-Ti ($+$3\%) if CaO rather than a MgO--CaO mixture is regenerated---the limit favoured by the mechanism analysis, since $\ce{Ca + MgO -> CaO + Mg}$ generates no solid product layer, with the 1:1 balance retained as the conservative basis; both are \emph{conditional on achieving $\eta_I > 0.70$}. Monte Carlo analysis gives medians of 13{,}141 and 13{,}536~kWh/ton-Ti for the two bases ($P(W<15{,}000) = 82.1\%$ and 76.6\%). All results are theoretical; viability hinges on adequate $\ce{CaO}$ solubility at 600~$^{\circ}$C, on the interfacial kinetics that decide whether MgO is regenerated electrolytically or reduced chemically by Ca, on melt oxoacidity favouring $\ce{O2}$ over $\ce{Cl2}$, and on a durable inert anode.",
))

# ---------------------------------------------------------------- 4. eta paragraph (fix .; and redundancy)
R.append((
    'current-efficiency paragraph',
    r"The assumed current efficiency range ($\eta_I = 0.75$--0.80) requires justification, as it significantly exceeds the FFC Cambridge process (30--50\%) \cite{fray2000}.",
    r"so the energy advantage of this process is \emph{conditional on achieving $\eta_I > 0.70$}.",
    r"""The assumed current efficiency range ($\eta_I = 0.75$--0.80) requires justification, as it significantly exceeds the FFC Cambridge process (30--50\%) \cite{fray2000}. The difference is mechanistic: FFC electro-deoxidises a solid oxide through a growing product layer, whereas the present process electrolyses dissolved oxides and therefore resembles dissolved-salt electrolysis---Hall--H\'eroult (90--95\% \cite{kvande2014}), Downs (70--90\%) and industrial $\ce{MgCl2}$ cells (80--90\% \cite{ji2026,pletcher1990}). The faradaic losses are estimated as (i) electronic conduction (2--5\%), (ii) back-dissolution of fresh Mg/Ca by dissolved oxide species (5--10\%), (iii) Na co-deposition at high $j$ (3--8\%) and (iv) impurity side reactions (2--5\%), summing to $\eta_I \approx 0.72$--0.88. A fifth channel is excluded from the faradaic budget because it conserves both metals: $\ce{Ca + Mg^{2+} -> Ca^{2+} + Mg}$ costs voltage efficiency rather than charge and caps the attainable deoxidation depth at the Mg-only endpoint (3908~ppm); its signature scales with the boundary-layer $\ce{Mg^{2+}}$ concentration and is separable from (ii) by comparing $\eta_I$ with the measured Ca:Mg ratio of the deposit. The estimates are additive and independent, and (ii) and (iii) both worsen with $j$, so the attainable $\eta_I$ at 1.1~A/cm$^2$ may fall below that sum; the Monte Carlo propagates $\eta_I$ independently and does not encode this correlation (Limitations~(9)). The target range is an \emph{unvalidated hypothesis}: at $\eta_I = 0.50$--0.60 the energy rises to $\sim$15{,}200--19{,}600~kWh/ton-Ti, within the FFC range, so the energy advantage is \emph{conditional on achieving $\eta_I > 0.70$}.""",
))

# ---------------------------------------------------------------- 5. oxide dissolution
R.append((
    'oxide dissolution paragraph',
    r"A critical feature of the process is the dissolution of $\ce{MgO}$ and $\ce{CaO}$ in the $\ce{CaCl2}$-containing melt.",
    r"together with the melt oxoacidity (see below), one of the two most critical experimental uncertainties in the present process concept.}",
    r"""A critical feature of the process is the dissolution of $\ce{MgO}$ and $\ce{CaO}$ in the $\ce{CaCl2}$-containing melt. Ito and Morita \cite{morita2004} measured a $\ce{MgO}$ solubility of 2.35~wt\% in $\ce{MgCl2-CaCl2}$ at 800~$^{\circ}$C, increasing with $\ce{CaCl2}$ content; because the operating window (580--650~$^{\circ}$C) is 150--250~$^{\circ}$C lower and oxide solubility falls with temperature, a single-point Arrhenius extrapolation gives $\approx$0.5--1.2~wt\% at 600~$^{\circ}$C. The activation energy is not independently determined and the range carries a factor-of-2.4 uncertainty. Within that range the reduced solubility raises the required salt circulation rate by 2--4$\times$ relative to the 800~$^{\circ}$C baseline: at 1~wt\% the inventory needed to hold the 2013~kg of MgO+CaO per ton Ti is $\sim$201~t of salt (117~t for CaO, 84~t for MgO), rising to $\sim$400~t at 0.5~wt\%. This is large but not unphysical---comparable to the cryolite inventory of Hall--H\'eroult cells---and the \emph{circulation rate} is set by the production rate rather than by the inventory. If the actual 600~$^{\circ}$C solubility falls below 0.5~wt\%, inventory and circulation rise by more than 4$\times$, potentially invalidating the closed-loop design. \textbf{Closed-loop circulation is therefore a theoretical hypothesis pending experimental validation of the 600~$^{\circ}$C oxide solubility---together with the melt oxoacidity (see below), one of the two most critical experimental uncertainties in the present process concept.}""",
))

# ---------------------------------------------------------------- 6. SCM parameters
R.append((
    'SCM parameter paragraph',
    r"where $c_{\mathrm{O}} \approx 1.06\times10^5$~mol/m$^3$",
    r"require 6.3~min for complete reduction (Fig.~\ref{fig:scm}).",
    r"""where $c_{\mathrm{O}} \approx 1.06\times10^5$~mol/m$^3$ (oxygen concentration in $\ce{TiO2}$), $c_{\mathrm{red}} \approx 581$~mol/m$^3$ (3~mol\% dissolved Mg/Ca, from a melt density of 1.8~g/cm$^3$ \cite{sato1999} and $M_{\mathrm{avg}} \approx 92.9$~g/mol; dissolved-metal solubilities in the quaternary melt are not reported and single-salt values span 0.5--3~mol\%, so $t_{\mathrm{complete}} \propto 1/c_{\mathrm{red}}$ maps that range to 6.3--38~min), and $D_{\mathrm{eff}} = D\varepsilon/\tau$ with porosity $\varepsilon = 0.3$ and tortuosity $\tau = 3.0$ \cite{fray2000}. Here $D$ denotes the intrinsic diffusivity of the rate-limiting species through the porous Ti layer. Two mechanisms are possible---outward diffusion of O$^{2-}$ or inward diffusion of Mg/Ca---and $D = 2.0\times10^{-9}$~m$^2$/s is adopted as a representative value consistent with measured O$^{2-}$ diffusivities of 1--3$\times10^{-9}$~m$^2$/s in $\ce{CaCl2}$-based FFC melts \cite{fray2000,yan2007}; the range bounds either mechanism, so the nominal value does not presuppose which one controls. With these parameters, 100~$\mu$m particles ($R = 50~\mu$m) require 6.3~min for complete reduction (Fig.~\ref{fig:scm}).""",
))

# ---------------------------------------------------------------- 7. D-range paragraph
R.append((
    'D-range paragraph',
    r"It is important to note that the above $D$ range ($10^{-9}$~m$^2$/s) corresponds to the \emph{chemical diffusion control} mechanism",
    r"that are not available at the conceptual design stage.",
    r"""The $D$ range of $10^{-9}$~m$^2$/s corresponds to liquid-phase diffusion through the pores of the product layer (Mg/Ca inward or O$^{2-}$ outward) and bounds either species. If the rate-limiting step were solid-state transport of O$^{2-}$ through the Ti layer, $D$ would be 2--3 orders of magnitude lower ($\sim$10$^{-12}$--10$^{-10}$~m$^2$/s) and 100~$\mu$m particles would require hours, making single-step batch reduction impractical; the process must therefore rely on the liquid-phase mechanism, which is plausible because the alloy is liquid at 600~$^{\circ}$C but requires experimental confirmation. External film diffusion can be neglected for 25--100~$\mu$m particles under mild agitation ($\mathrm{Sh} \gg 1$), although a quantitative comparison needs melt hydrodynamics that the conceptual stage does not provide.""",
))


def main():
    with io.open(PATH, encoding='utf-8') as f:
        text = f.read()
    problems = []
    for item in R:
        if len(item) == 3:
            name, old, new = item
            if text.count(old) != 1:
                problems.append(f'{name}: anchor found {text.count(old)} times')
        else:
            name, start, end, new = item
            if text.count(start) != 1:
                problems.append(f'{name}: start anchor found {text.count(start)} times')
            if text.count(end) != 1:
                problems.append(f'{name}: end anchor found {text.count(end)} times')
    if problems:
        print('ABORTED:')
        for p in problems:
            print('   ', p)
        sys.exit(1)
    for item in R:
        if len(item) == 3:
            name, old, new = item
            i = text.index(old)
            j = i + len(old)
        else:
            name, start, end, new = item
            i = text.index(start)
            j = text.index(end, i) + len(end)
        old_len = j - i
        text = text[:i] + new + text[j:]
        print(f'  [ok] {name}: {old_len} -> {len(new)} chars ({100*(len(new)-old_len)/old_len:+.0f}%)')
    with io.open(PATH, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)
    print('  written')


if __name__ == '__main__':
    main()
