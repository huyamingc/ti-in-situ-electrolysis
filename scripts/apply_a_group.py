# -*- coding: utf-8 -*-
"""Reviewer-1 completeness batch.

  R1-2  overall process flowsheet            -> new figure + caption
  R1-8  reactor / cell concept               -> new subsection
  R1-1  Ti product recovery                  -> new subsection
  R1-7  "all four salts melt above the design temperature" -> answered quantitatively
  R1-4  feedstock grade                      -> stated explicitly
  R1-6  why the shrinking-core model         -> model-selection paragraph
"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, 'manuscript.tex')

FLOWSHEET = r"""\begin{figure}[!ht]
\centering
\includegraphics[width=0.98\linewidth]{figure_flowsheet.eps}
\caption{Process flowsheet of the proposed route. Case~II material and energy figures are given, with the CaO-only Case~I values in brackets. Metallurgical-grade $\ce{TiO2}$ powder is suspended in the quaternary chloride melt; the cathode co-deposits the liquid Mg--Ca reductant, which reduces the particles in situ; the by-product oxides dissolve and are electrolytically regenerated at the anode with oxygen evolution; the Ti powder is recovered by water washing and the salt is recycled.}
\label{fig:flowsheet}
\end{figure}

\subsection*{Feedstock, Reactor Concept and Product Recovery}

\textbf{Feedstock.} All material and energy figures in this work use pure $\ce{TiO2}$ as the balance basis. The industrially relevant metallurgical-grade feedstock ($\geq$90~wt\% $\ce{TiO2}$, i.e.\ $\sim$186~kg of Fe/Si impurities per ton Ti) is treated as an extension in the E--$p\ce{O^{2-}}$ section, and the impurity-separation energy that is deliberately \emph{excluded} from the energy balance is quantified in Limitations~(7).

\textbf{Reactor concept.} The cell is a single sealed vessel held at 600~$^{\circ}$C under dry argon, with the $\ce{TiO2}$ particles suspended in the quaternary melt by gentle circulation. Cathode and anode must be closely spaced ($L \lesssim 1$~cm): the 0.9~V ohmic budget of the voltage balance is satisfied only for $L \lesssim 1.1$~cm at $j \approx 1.1$~A/cm$^2$ and $\kappa = 1.4$~S/cm (Fig.~\ref{fig:current_regimes}b), so a close-spaced or diaphragm-integrated electrode assembly is a design requirement rather than an option. The anode must evolve $\ce{O2}$ rather than $\ce{Cl2}$ (the oxoacidity boundary of Fig.~\ref{fig:cl2}) while surviving attack by $\ce{O^{2-}}$ and $\ce{Cl^-}$ (Limitations~(8)). Because Mg has an appreciable vapour pressure at 600~$^{\circ}$C ($\approx$180~Pa), the freeboard must be sealed and the Mg vapour condensed and returned; the same balance keeps the Mg inventory of the alloy in steady state (Cathode Mass Transport section).

\textbf{Product recovery.} The reduction product is Ti powder suspended in the melt rather than a coherent cathode deposit, so recovery is a solid--liquid separation, not the electrochemical product handling of FFC-type cells. A 1~$\mu$m surface salt film on 25--100~$\mu$m powder corresponds to 9.6~wt\% (25~$\mu$m) down to 1.2~wt\% (100~$\mu$m) of entrained salt; since $\ce{CaCl2}$ and $\ce{MgCl2}$ are highly water-soluble, counter-current water washing followed by drying and screening suffices, consuming of order 0.2--1~m$^3$ of wash water per ton Ti. The wash liquor is evaporated or crystallised and the salt returned to the cell, which is why the ``post-treatment'' line of the energy balance is essentially a pumping and drying duty (Limitations~(7) distinguishes it from impurity removal).

\textbf{Melt state at the design temperature.} All four pure salts melt above 600~$^{\circ}$C ($\ce{MgCl2}$ 714~$^{\circ}$C, $\ce{CaCl2}$ 772~$^{\circ}$C, KCl 770~$^{\circ}$C, NaCl 801~$^{\circ}$C), so the design temperature might appear to lie below the melting range of every constituent. In a quaternary mixture the liquidus is depressed by the entropy of mixing: applying the ideal-solution liquidus condition of Eq.~\ref{eq:liquidus} component by component gives 543.7~$^{\circ}$C, controlled by $\ce{CaCl2}$, so the melt is fully liquid at 600~$^{\circ}$C with 56~$^{\circ}$C of superheat, and the calculation reproduces the 544~$^{\circ}$C quoted in the Salt Composition Design section. The open question is therefore not whether the melt is liquid at the design temperature, but by how much the ideal-solution liquidus underestimates the real one (Limitations~(4)).
"""

SCM_MODEL = r"""\textbf{Model selection.} A shrinking-core formulation is adopted because the reduction proceeds by inward transport through a growing product layer around a shrinking unconverted core, which is the geometry of a solid--liquid reaction with a coherent product shell. The alternatives are less appropriate: pseudo-homogeneous (Avrami--Erofeev/JMAK) models assume reaction throughout the particle volume and describe nucleation-and-growth or gas--solid systems, whereas here the reductant is a liquid metal advancing from the particle surface inward; mixed-control formulations collapse to the shrinking-core result when internal diffusion through the product layer dominates, as argued below; and purely empirical rate laws would carry no predictive content for the $t \propto R^2$ particle-size scaling on which the process design depends. The weakest assumption of the model---diffusion control with a constant effective diffusivity---is examined below.

"""


def main():
    with io.open(PATH, encoding='utf-8') as f:
        text = f.read()

    # ---- 1. flowsheet + new subsection, inserted at the end of Process Description
    anchor = r"The net reaction is $\ce{TiO2 -> Ti + O2}$, driven by electrical energy, with Mg and Ca acting as cyclic mediators."
    if text.count(anchor) != 1:
        sys.exit(f'ERROR: process-description anchor found {text.count(anchor)} times')
    text = text.replace(anchor, anchor + '\n\n' + FLOWSHEET.strip('\n'), 1)
    print('  [ok] flowsheet figure + Feedstock/Reactor/Recovery subsection inserted')

    # ---- 2. SCM model-selection paragraph
    anchor2 = r"The reduction kinetics are modeled using the shrinking core model (SCM) with diffusion control through the porous Ti product layer"
    if text.count(anchor2) != 1:
        sys.exit(f'ERROR: SCM anchor found {text.count(anchor2)} times')
    text = text.replace(anchor2, SCM_MODEL + anchor2, 1)
    print('  [ok] SCM model-selection paragraph inserted')

    with io.open(PATH, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)
    print(f'  written: {PATH}')


if __name__ == '__main__':
    main()
