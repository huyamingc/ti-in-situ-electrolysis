# -*- coding: utf-8 -*-
"""R3-1 reconstruction, batch 1: narrative layer.

Abstract, Introduction (key-innovation paragraph + bullets 1 and 4), Conclusions
(1), (5), (7), and the Process Comparison table for the proposed route.

All replacements are checked for uniqueness before anything is written; if any
anchor fails, the script exits without touching the file.
"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, 'manuscript.tex')

R = []

R.append((
    'abstract: deoxidation limits + Ca/MgO + a_MgO',
    r"with equilibrium deoxidation limits of 3908~ppm O (Mg), 20.2~ppm (Ca), and $\approx$77~ppm (equimolar alloy).",
    r"with equilibrium deoxidation limits of 3908~ppm O (Mg) and 20.2~ppm (Ca), the latter corresponding to "
    r"$\approx$77~ppm at the equimolar alloy activity. $\ce{Ca + MgO -> CaO + Mg}$ is exergonic at 600~$^{\circ}$C "
    r"($\Delta G^{\circ} = -38.2$~kJ/mol; $K = 194$), so Ca supplies the deoxidation driving force while the role of Mg "
    r"is to keep the reductant liquid at the design temperature---pure Ca and pure Mg are both solid at 600~$^{\circ}$C, "
    r"whereas the Mg--Ca eutectic is $\approx$517~$^{\circ}$C---and reaching the deep-deoxidation limit then requires the "
    r"dissolved $\ce{MgO}$ activity to remain below $\approx 5\times10^{-3}$.",
))

R.append((
    'abstract: energy dual case',
    r"At the nominal design point ($\eta_I = 0.75$, $V_{\mathrm{cell}} = 4.1$~V), the net equivalent energy consumption "
    r"is 12{,}552~kWh/ton-Ti, \emph{conditional on achieving $\eta_I > 0.70$}.",
    r"At the nominal design point ($\eta_I = 0.75$, $V_{\mathrm{cell}} = 4.1$~V), the net equivalent energy consumption "
    r"is 12{,}552~kWh/ton-Ti, rising to 12{,}933~kWh/ton-Ti ($+$3\%) if Ca acts as the sole net oxygen carrier "
    r"(\emph{i.e.}, if CaO rather than a MgO--CaO mixture is regenerated); both figures are "
    r"\emph{conditional on achieving $\eta_I > 0.70$}.",
))

R.append((
    'abstract: closing viability sentence',
    r"All results are theoretical; viability hinges on $\ce{MgO}$/$\ce{CaO}$ solubility $\geq$0.5~wt\% at 600~$^{\circ}$C, "
    r"melt oxoacidity favoring $\ce{O2}$ over $\ce{Cl2}$ evolution, and a durable oxygen-evolving inert anode.",
    r"All results are theoretical; viability hinges on adequate $\ce{CaO}$ solubility at 600~$^{\circ}$C (with the "
    r"dissolved $\ce{MgO}$ activity held below $\approx 5\times10^{-3}$), on the interfacial kinetics that decide whether "
    r"MgO leaves through electrolytic regeneration or is chemically reduced by Ca, on melt oxoacidity favoring $\ce{O2}$ "
    r"over $\ce{Cl2}$ evolution, and on a durable oxygen-evolving inert anode.",
))

R.append((
    'intro: key-innovation sentence',
    r"The key innovation is an electrochemical-thermochemical coupling: the co-deposited Mg--Ca alloy serves as a cyclic "
    r"liquid reductant in which Mg, deposited preferentially, carries the bulk of the reduction while Ca delivers deep "
    r"deoxidation.",
    r"The key innovation is an electrochemical-thermochemical coupling: the co-deposited Mg--Ca alloy serves as a cyclic "
    r"liquid reductant, in which the alloy provides a liquid reductant phase at 600~$^{\circ}$C---both pure metals are "
    r"solid at that temperature---while Ca supplies the thermodynamic driving force for deep deoxidation, CaO being the "
    r"stable oxide.",
))

R.append((
    'intro: novelty bullet 1',
    r"combining Mg's kinetic advantage with Ca's thermodynamic deoxidation depth in a single closed-loop process.",
    r"combining a liquid Mg--Ca reductant phase---which is what allows operation at 600~$^{\circ}$C, where both pure "
    r"metals are solid---with Ca's thermodynamic deoxidation depth in a single closed-loop process.",
))

R.append((
    'intro: novelty bullet 4 (energy)',
    r"Full-process energy balance analysis (12{,}552~kWh/ton-Ti net equivalent consumption at the nominal design point, "
    r"\emph{theoretical prediction conditional on achieving $\eta_I > 0.70$}; process energy efficiency 48.7\%, "
    r"second-law efficiency 36.3\%, electrolysis energy fraction 97.2\%)",
    r"Full-process energy balance analysis (12{,}552~kWh/ton-Ti net equivalent consumption at the nominal design point, "
    r"or 12{,}933~kWh/ton-Ti if Ca is the sole net oxygen carrier; \emph{both theoretical predictions conditional on "
    r"achieving $\eta_I > 0.70$}; process energy efficiency 48.7\%, second-law efficiency 36.3\%, electrolysis energy "
    r"fraction 97.2\%)",
))

R.append((
    'conclusions (1)',
    r"the process would combine fast Mg-based bulk reduction with Ca's deep deoxidation: equilibrium limits are "
    r"3908~ppm O for pure Mg versus 20.2~ppm for pure Ca (193$\times$ difference), and $\approx$77~ppm for the equimolar "
    r"Mg--Ca alloy of the material balance---far below the 0.10--0.20~wt\% commercial target.",
    r"the process combines Ca as the thermodynamic deoxidation driver ($\ce{Ca + MgO -> CaO + Mg}$, "
    r"$\Delta G^{\circ}(600~^{\circ}\mathrm{C}) = -38.2$~kJ/mol, Eq.~\ref{eq:camgo}) with Mg as the component that keeps "
    r"the reductant liquid at 600~$^{\circ}$C, where both pure metals are solid: the equilibrium limits are 3908~ppm O "
    r"for Mg acting alone versus 20.2~ppm for Ca (193$\times$), the latter becoming $\approx$77~ppm at the equimolar "
    r"alloy activity---far below the 0.10--0.20~wt\% commercial target, provided the dissolved MgO activity is held "
    r"below $\approx 5\times10^{-3}$ (Eq.~\ref{eq:amgo}).",
))

R.append((
    'conclusions (5): insert dual-case energy',
    r"The electrolysis energy fraction is 97.2\%.",
    r"The electrolysis energy fraction is 97.2\%. If Ca acts as the sole net oxygen carrier (CaO regeneration, "
    r"Eq.~\ref{eq:camgo}), the decomposition voltage rises from 2.73 to 2.83~V and the net equivalent consumption to "
    r"12{,}933~kWh/ton-Ti ($+$3\%).",
))

R.append((
    'conclusions (7): close the loop on CaO vs MgO',
    r"\textbf{(b)} the closed-loop salt circulation depends on adequate MgO/CaO solubility at 600~$^{\circ}$C "
    r"($\geq$0.5~wt\%), which is currently estimated by Arrhenius extrapolation from 800~$^{\circ}$C data without "
    r"confidence intervals---if the actual solubility falls below 0.5~wt\%, the salt circulation rate would need to "
    r"increase by more than 4$\times$, potentially invalidating the closed-loop design.",
    r"\textbf{(b)} the closed-loop salt circulation depends on adequate oxide solubility at 600~$^{\circ}$C, currently "
    r"estimated by Arrhenius extrapolation from 800~$^{\circ}$C data without confidence intervals---if the actual "
    r"solubility falls below 0.5~wt\%, the salt circulation rate would need to increase by more than 4$\times$, "
    r"potentially invalidating the closed-loop design. Under the reconstructed mechanism, however, the species that "
    r"must be dissolved and regenerated is predominantly CaO (Eq.~\ref{eq:camgo}), whose solubility in "
    r"$\ce{CaCl2}$-rich melts exceeds that of $\ce{MgO}$, while a \emph{low} MgO solubility is itself a design "
    r"requirement ($a_{\ce{MgO}} \lesssim 5\times10^{-3}$; Eq.~\ref{eq:amgo}); the pivotal missing measurements are "
    r"therefore the CaO solubility and the interfacial kinetics of Eq.~\ref{eq:camgo}.",
))

R.append((
    'process comparison: proposed route row',
    r"  Proposed & In-situ electrolysis + Mg-Ca complementary reduction & Cyclic (conceptual) & 580--650$^{b}$ & Moderate$^{a}$ & High (target) & Anode corrosion, unvalidated $\eta_I$ \\",
    r"  Proposed & In-situ Mg--Ca co-deposition; liquid Mg--Ca reductant with Ca as thermodynamic deoxidizer & Cyclic (conceptual) & 580--650$^{b}$ & Moderate$^{a}$ & High (target) & Anode corrosion, unvalidated $\eta_I$, Ca--MgO kinetics \\",
))

R.append((
    'process comparison: footnote a',
    r"$^{a}$Theoretical prediction conditional on $\eta_I > 0.70$; industrial/pilot values shown for Kroll/FFC/USTB are not directly equivalent.",
    r"$^{a}$Theoretical prediction conditional on $\eta_I > 0.70$. 12{,}552~kWh/ton-Ti assumes a MgO--CaO regeneration "
    r"mixture; 12{,}933~kWh/ton-Ti assumes CaO as the sole regenerated species (Eq.~\ref{eq:camgo}). Industrial/pilot "
    r"values shown for Kroll/FFC/USTB are not directly equivalent.",
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
