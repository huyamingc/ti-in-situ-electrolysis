# -*- coding: utf-8 -*-
"""Replace the Monte Carlo paragraph with the ten-parameter version (C group).

Reports: ten sampled parameters, median SCM time 13.6 min, energy median
13,141 kWh/t with P(W<15,000) = 82.1%, required-gap statistics
(median 0.84 cm, P95 1.88 cm) and the joint feasibility probability 95.8%.
"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, 'manuscript.tex')

START = r"To propagate uncertainties globally, a Monte Carlo simulation ($N = 10^5$, fixed random seed $= 42$ for reproducibility) sampled five parameters simultaneously"
END = r"governed by the 600~$^{\circ}$C oxide solubility and the liquidus."

NEW = r"""To propagate uncertainties globally, a Monte Carlo simulation ($N = 10^5$, fixed random seed $= 42$ for reproducibility) sampled ten parameters simultaneously. The first five are those of the energy and kinetic models: $D \sim U(1, 3) \times 10^{-9}$~m$^2$/s, $\varepsilon \sim U(0.1, 0.5)$, $\tau \sim U(1.5, 5.0)$, $\eta_I \sim \mathrm{Tri}(0.50, 0.75, 0.88)$, and $V_{\mathrm{cell}} \sim \mathcal{N}(4.1, 0.3)$ truncated to [3.5, 4.5]~V. Five further parameters cover the quantities that the earlier sensitivity discussion had left outside the sampling: $\gamma_{\ce{CaCl2}} \sim U(0.3, 1.0)$ and $\gamma_{\ce{NaCl}} \sim U(0.7, 1.0)$ (co-deposition window), the liquidus $T_{\mathrm{liq}} \sim \mathcal{N}(544, 25)$~$^{\circ}$C truncated to [494, 594]~$^{\circ}$C, the MgO solubility $S_{\ce{MgO}} \sim U(0.5, 1.2)$~wt\%, the diffusion-layer thickness $\delta \sim U(100, 500)$~$\mu$m, and the dissolved-reductant concentration $c_{\mathrm{red}} \sim U(0.5, 3.0)$~mol\%. The $\eta_I$ prior spans the worst-case FFC-like range without presupposing a feasibility threshold, and $\varepsilon$ and $\tau$ are sampled as independent uniform variables although they are physically negatively correlated, which makes the resulting $D_{\mathrm{eff}}$ spread conservative. In the energy calculation the cell voltage retains its nominal distribution, as in the energy balance; $\delta$ instead propagates into a \emph{design} consequence, because the equimolar deposit requires $j = 2j_{\mathrm{lim,Mg}}$ and the 0.9~V ohmic budget then fixes a required gap $L_{\mathrm{req}} = 0.9\kappa/j$.

The results (Fig.~\ref{fig:monte_carlo}) give a lognormal SCM reduction time with a median of 13.6~min (P5--P95: 4.0--55.2~min; the nominal 6.3~min corresponds to the upper end of the $c_{\mathrm{red}}$ range, 3~mol\%) and a right-skewed net energy consumption with a median of 13{,}141~kWh/ton-Ti (P5--P95: 10{,}875--16{,}722~kWh/ton-Ti on the Case~II basis of Table~\ref{tab:mbalance}; the CaO-only Case~I shifts the distribution upward by $\sim$3\%). The probability of beating the nominal 12{,}552~kWh/ton-Ti is 35.8\%, and $P(W_{\mathrm{net}} < 15{,}000) = 82.1\%$; the latter threshold is the lower bound of the FFC route, so that figure largely restates the assumed $\eta_I$ prior rather than providing an independent feasibility estimate. Spearman analysis (Fig.~\ref{fig:tornado}) shows that $\eta_I$ ($\rho = -0.85$) dominates the energy uncertainty ahead of $V_{\mathrm{cell}}$ ($\rho = 0.50$), while $c_{\mathrm{red}}$ and $\varepsilon$ dominate the SCM time, so experimental validation of current efficiency remains the most critical prerequisite for the energy claim. $L_{\mathrm{req}}$ has a median of 0.84~cm and a 95th percentile of 1.88~cm, falling below a 3~mm engineering floor in only 4.2\% of the samples.

The added parameters act on \emph{feasibility} rather than on the per-ton energy (Fig.~\ref{fig:monte_carlo}c): the co-deposition window stays above the 50~mV threshold in every sample (5th percentile 89~mV), the ideal-solution liquidus is below 600~$^{\circ}$C throughout the sampled $\pm$50~$^{\circ}$C interval, and the joint probability that the window, the liquidus at the 620~$^{\circ}$C operating floor and the 3~mm gap floor are all satisfied is 95.8\%. Process feasibility is therefore not limited by any of these quantities individually, but by the two that cannot be computed at all---the 600~$^{\circ}$C CaO solubility and the Ca--MgO interfacial kinetics of Eq.~\ref{eq:camgo}."""


def main():
    with io.open(PATH, encoding='utf-8') as f:
        text = f.read()
    if text.count(START) != 1:
        sys.exit(f'ERROR: start anchor found {text.count(START)} times')
    if text.count(END) != 1:
        sys.exit(f'ERROR: end anchor found {text.count(END)} times')
    i = text.index(START)
    j = text.index(END, i) + len(END)
    old_len = j - i
    text = text[:i] + NEW + text[j:]
    with io.open(PATH, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)
    print(f'  [ok] Monte Carlo paragraph: {old_len} -> {len(NEW)} chars '
          f'({100*(len(NEW)-old_len)/old_len:+.0f}%)')


if __name__ == '__main__':
    main()
