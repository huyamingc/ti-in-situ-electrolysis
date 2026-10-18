# -*- coding: utf-8 -*-
"""Tighten the newly added Reviewer-1 material and shrink the flowsheet figure."""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, 'manuscript.tex')

R = [
    (
        'flowsheet width',
        r"\includegraphics[width=0.98\linewidth]{figure_flowsheet.eps}",
        r"\includegraphics[width=0.86\linewidth]{figure_flowsheet.eps}",
    ),
    (
        'feedstock',
        r"\textbf{Feedstock.} All material and energy figures in this work use pure $\ce{TiO2}$ as the balance basis. The industrially relevant metallurgical-grade feedstock ($\geq$90~wt\% $\ce{TiO2}$, i.e.\ $\sim$186~kg of Fe/Si impurities per ton Ti) is treated as an extension in the E--$p\ce{O^{2-}}$ section, and the impurity-separation energy that is deliberately \emph{excluded} from the energy balance is quantified in Limitations~(7).",
        r"\textbf{Feedstock.} All figures use pure $\ce{TiO2}$ as the balance basis; the metallurgical-grade case ($\geq$90~wt\% $\ce{TiO2}$, $\sim$186~kg of Fe/Si impurities per ton Ti) is treated in the E--$p\ce{O^{2-}}$ section, with the deliberately excluded impurity-separation energy quantified in Limitations~(7).",
    ),
    (
        'reactor concept',
        r"\textbf{Reactor concept.} The cell is a single sealed vessel held at 600~$^{\circ}$C under dry argon, with the $\ce{TiO2}$ particles suspended in the quaternary melt by gentle circulation. Cathode and anode must be closely spaced ($L \lesssim 1$~cm): the 0.9~V ohmic budget of the voltage balance is satisfied only for $L \lesssim 1.1$~cm at $j \approx 1.1$~A/cm$^2$ and $\kappa = 1.4$~S/cm (Fig.~\ref{fig:current_regimes}b), so a close-spaced or diaphragm-integrated electrode assembly is a design requirement rather than an option. The anode must evolve $\ce{O2}$ rather than $\ce{Cl2}$ (the oxoacidity boundary of Fig.~\ref{fig:cl2}) while surviving attack by $\ce{O^{2-}}$ and $\ce{Cl^-}$ (Limitations~(8)). Because Mg has an appreciable vapour pressure at 600~$^{\circ}$C ($\approx$180~Pa), the freeboard must be sealed and the Mg vapour condensed and returned; the same balance keeps the Mg inventory of the alloy in steady state (Cathode Mass Transport section).",
        r"\textbf{Reactor concept.} The cell is a single sealed vessel at 600~$^{\circ}$C under dry argon, with $\ce{TiO2}$ particles suspended by gentle circulation. Cathode and anode must be closely spaced: the 0.9~V ohmic budget is met only for $L \lesssim 1.1$~cm at $j \approx 1.1$~A/cm$^2$ and $\kappa = 1.4$~S/cm (Fig.~\ref{fig:current_regimes}b), making a close-spaced or diaphragm-integrated assembly a requirement rather than an option. The anode must evolve $\ce{O2}$ rather than $\ce{Cl2}$ (Fig.~\ref{fig:cl2}) while resisting $\ce{O^{2-}}$ and $\ce{Cl^-}$ attack (Limitations~(8)). Because Mg has an appreciable vapour pressure at 600~$^{\circ}$C ($\approx$180~Pa), the freeboard must be sealed and the Mg vapour condensed and returned, which also keeps the alloy's Mg inventory in steady state (Cathode Mass Transport section).",
    ),
    (
        'product recovery',
        r"\textbf{Product recovery.} The reduction product is Ti powder suspended in the melt rather than a coherent cathode deposit, so recovery is a solid--liquid separation, not the electrochemical product handling of FFC-type cells. A 1~$\mu$m surface salt film on 25--100~$\mu$m powder corresponds to 9.6~wt\% (25~$\mu$m) down to 1.2~wt\% (100~$\mu$m) of entrained salt; since $\ce{CaCl2}$ and $\ce{MgCl2}$ are highly water-soluble, counter-current water washing followed by drying and screening suffices, consuming of order 0.2--1~m$^3$ of wash water per ton Ti. The wash liquor is evaporated or crystallised and the salt returned to the cell, which is why the ``post-treatment'' line of the energy balance is essentially a pumping and drying duty (Limitations~(7) distinguishes it from impurity removal).",
        r"\textbf{Product recovery.} The product is Ti powder suspended in the melt rather than a coherent cathode deposit, so recovery is a solid--liquid separation. A 1~$\mu$m salt film on 25--100~$\mu$m powder corresponds to 9.6~wt\% (25~$\mu$m) down to 1.2~wt\% (100~$\mu$m) of entrained salt; as $\ce{CaCl2}$ and $\ce{MgCl2}$ are highly water-soluble, counter-current washing, drying and screening suffice, at of order 0.2--1~m$^3$ of wash water per ton Ti. The wash liquor is evaporated and the salt returned to the cell, so the ``post-treatment'' line of the energy balance is a pumping and drying duty (Limitations~(7) distinguishes it from impurity removal).",
    ),
    (
        'melt state',
        r"\textbf{Melt state at the design temperature.} All four pure salts melt above 600~$^{\circ}$C ($\ce{MgCl2}$ 714~$^{\circ}$C, $\ce{CaCl2}$ 772~$^{\circ}$C, KCl 770~$^{\circ}$C, NaCl 801~$^{\circ}$C), so the design temperature might appear to lie below the melting range of every constituent. In a quaternary mixture the liquidus is depressed by the entropy of mixing: applying the ideal-solution liquidus condition of Eq.~\ref{eq:liquidus} component by component gives 543.7~$^{\circ}$C, controlled by $\ce{CaCl2}$, so the melt is fully liquid at 600~$^{\circ}$C with 56~$^{\circ}$C of superheat, and the calculation reproduces the 544~$^{\circ}$C quoted in the Salt Composition Design section. The open question is therefore not whether the melt is liquid at the design temperature, but by how much the ideal-solution liquidus underestimates the real one (Limitations~(4)).",
        r"\textbf{Melt state at the design temperature.} All four pure salts melt above 600~$^{\circ}$C ($\ce{MgCl2}$ 714, $\ce{CaCl2}$ 772, KCl 770, NaCl 801~$^{\circ}$C), so the design temperature appears to lie below the melting range of every constituent. In a quaternary mixture, however, the liquidus is depressed by the entropy of mixing: applying the liquidus condition of Eq.~\ref{eq:liquidus} component by component gives 543.7~$^{\circ}$C, controlled by $\ce{CaCl2}$---the value quoted in the Salt Composition Design section---so the melt is fully liquid at 600~$^{\circ}$C with 56~$^{\circ}$C of superheat. The open question is therefore not whether the melt is liquid, but by how much the ideal-solution liquidus underestimates the real one (Limitations~(4)).",
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
        print(f'  [ok] {name}: {len(old)} -> {len(new)}')
    with io.open(PATH, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)
    print('  written')


if __name__ == '__main__':
    main()
