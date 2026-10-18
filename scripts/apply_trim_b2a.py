# -*- coding: utf-8 -*-
"""Editorial trim, batch B2a: condense six Limitations entries that duplicate the
main text (R2 item 7 / R3 item 4).

Each entry is replaced over its full span using unique start/end anchors.
Limitations (1), (5), (6) and (10) are untouched.
"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, 'manuscript.tex')

B = []

B.append((
    'Limitation (2)',
    r"(2) \textbf{Electrode overpotentials and Mg/Ca co-deposition ratio}: The co-deposition window analysis is based on equilibrium Nernst equations.",
    r"Concentration polarization at high current densities and ohmic losses also require detailed electrode-kinetic modeling for definitive assessment.",
    r"(2) \textbf{Electrode overpotentials and Mg/Ca co-deposition ratio}: The window analysis rests on equilibrium Nernst equations; activation overpotentials, concentration polarization and ohmic drop all modify the effective window, and the \emph{sign} of the kinetic correction is not established---the Downs cell deposits Na from a $\ce{CaCl2}$-majority melt, which suggests that $\ce{Ca^{2+}}$ reduction may instead be kinetically slower and therefore \emph{narrow} the window. Quantifying this requires exchange current densities and transfer coefficients that are unavailable for the quaternary melt. A larger uncertainty is the Mg/Ca ratio of the deposit: because Mg reduces $\sim$816~mV earlier than Ca, the equimolar alloy assumed in the material balance can only be approached when Mg deposition reaches its diffusion limit, and $D$ and $\delta$ are themselves uncertain by about an order of magnitude ($j_{\mathrm{lim,Mg}} = 0.07$--3.4~A/cm$^2$; Fig.~\ref{fig:current_regimes}), so the design current density must be established electrochemically."
))

B.append((
    'Limitation (3)',
    r"(3) \textbf{SCM kinetics}: The model assumes pure diffusion control with constant $D$",
    r"however, wetting, pore-clogging, and morphology evolution remain unquantified and require dedicated study.",
    r"(3) \textbf{SCM kinetics}: The model assumes pure diffusion control with constant $D$, neglecting convection and electromigration, and the nominal $D = 2.0\times10^{-9}$~m$^2$/s is an order-of-magnitude estimate from FFC literature data \cite{fray2000,yan2007}; the rate-limiting species (Mg/Ca inward versus O$^{2-}$ outward) remains unidentified. Multi-parameter sensitivity ($D$, $\varepsilon$, $\tau$) gives 1.3--63~min, so product-layer microstructure dominates the uncertainty. The model further assumes the porous Ti layer stays open and wetted by the liquid reductant; if the alloy blocks the pores or the layer coarsens at 600~$^{\circ}$C, $D_{\mathrm{eff}}$ could fall towards the solid-state value ($\sim$10$^{-12}$~m$^2$/s) and the reduction time lengthen from minutes to hours. Mg and Ca are essentially immiscible with Ti (no Mg--Ti or Ca--Ti intermetallics in the assessed binaries \cite{hallstedt2025}), so interfacial compound formation is not expected, but wetting, pore clogging and morphology evolution remain unquantified."
))

B.append((
    'Limitation (4)',
    r"(4) \textbf{Liquidus calculation}: The ideal solution model neglects intermediate compounds",
    r"rather than treating 580--600~$^{\circ}$C as a recommended window.",
    r"(4) \textbf{Liquidus calculation}: The ideal-solution model neglects intermediate compounds; the $\pm$50~$^{\circ}$C uncertainty allows an actual liquidus up to $\sim$594~$^{\circ}$C, leaving only $\sim$6~$^{\circ}$C below the 600~$^{\circ}$C design point---insufficient for the $\pm$10--20~$^{\circ}$C fluctuations typical of industrial electrolytic cells. If the liquidus lies near 594~$^{\circ}$C the operable window shrinks to $\sim$620--650~$^{\circ}$C (the ceiling being set by Mg melting and accelerated corrosion), and local freezing or short-circuiting becomes a pilot-fatal risk. A hard operating floor of $\geq$620~$^{\circ}$C---or CALPHAD/DSC confirmation of a substantially lower liquidus---should therefore be adopted as a design requirement."
))

B.append((
    'Limitation (7)',
    r"(7) \textbf{Impurity separation}: The Fe--Ti and Si--Ti systems form intermetallic compounds at 600~$^{\circ}$C",
    r"and should be addressed in future cradle-to-gate analyses.",
    r"(7) \textbf{Impurity separation}: Fe--Ti and Si--Ti form intermetallic compounds at 600~$^{\circ}$C, which may complicate gravity-based separation. The ``post-treatment'' item (300~kWh/ton, Table~\ref{tab:heatbal}) covers only salt washing, drying and screening and is \emph{distinct from} impurity removal: if metallurgical-grade $\ce{TiO2}$ ($\geq$90~wt\%) is used, $\sim$5--10~wt\% impurity metals (mainly Fe and Si) must be separated, and acid leaching of 100~$\mu$m Ti powder typically costs $\sim$200--500~kWh/ton-Ti ($\sim$2--4\% of the net energy). This is not included in the present figure and belongs in a future cradle-to-gate analysis."
))

B.append((
    'Limitation (8)',
    r"(8) \textbf{Engineering factors}: Anode lifetime, current efficiency degradation, and impurity accumulation require pilot-scale testing.",
    r"also requires long-duration testing.",
    r"(8) \textbf{Engineering factors}: Anode lifetime, current-efficiency degradation and impurity accumulation all require pilot-scale testing. Anode corrosion is the key challenge: at 600~$^{\circ}$C in chloride melts containing dissolved oxides, candidate inert anodes (SnO$_2$, RuO$_2$-coated Ti, dimensionally stable anodes, $\ce{NiFe2O4}$, $\ce{CeO2}$-coated Ni alloys) face attack by O$^{2-}$ and Cl$^-$ and degradation by the oxygen-evolution reaction. A consumable graphite anode is the fallback, at the cost of carbon contamination, $\ce{CO2}$/CO evolution, a $\sim$0.3~V higher cell voltage ($\approx$4.3~V) and a net consumption rising from 12{,}552 to $\sim$13{,}100~kWh/ton-Ti ($\sim$5\%), which would break the ``green $\ce{O2}$'' narrative while preserving the cathodic mechanism. Anode-material screening should therefore precede any commitment to the inert-anode energy balance."
))

B.append((
    'Limitation (9)',
    r"(9) \textbf{Current efficiency assumption}: The assumed $\eta_I = 0.75$--0.80 is based on analogy with the Downs process",
    r"and confirming the high sensitivity of the energy conclusion to this unvalidated parameter.",
    r"(9) \textbf{Current efficiency assumption}: The assumed $\eta_I = 0.75$--0.80 rests on analogy with dissolved-salt electrolysis (Downs, Hall--H\'eroult, industrial $\ce{MgCl2}$ electrolysis) rather than on measurement, and the loss estimates given in the Material and Energy Balance section are rough. If $\eta_I$ is only 0.50--0.60 the energy consumption rises to 15{,}200--19{,}600~kWh/ton-Ti, within the FFC range, so the Monte Carlo median of 13{,}141~kWh/ton-Ti and $P(W_{\mathrm{net}} < 15{,}000) = 82.1\%$ largely restate the assumed prior. Current efficiency is the dominant uncertainty ($\rho = -0.85$) and its measurement is the most critical prerequisite for the energy claim."
))


def main():
    with io.open(PATH, encoding='utf-8') as f:
        text = f.read()

    problems = []
    for name, start, end, _new in B:
        if text.count(start) != 1:
            problems.append(f'{name}: start anchor found {text.count(start)} times')
        if text.count(end) != 1:
            problems.append(f'{name}: end anchor found {text.count(end)} times')
    if problems:
        print('ABORTED - no changes written:')
        for p in problems:
            print('   ', p)
        sys.exit(1)

    for name, start, end, new in B:
        i = text.index(start)
        j = text.index(end, i) + len(end)
        old_len = j - i
        text = text[:i] + new + text[j:]
        print(f'  [ok] {name}: {old_len} -> {len(new)} chars ({100*(len(new)-old_len)/old_len:+.0f}%)')

    with io.open(PATH, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)
    print(f'  written: {PATH}')


if __name__ == '__main__':
    main()
