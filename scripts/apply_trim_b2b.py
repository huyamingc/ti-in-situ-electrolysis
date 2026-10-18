# -*- coding: utf-8 -*-
"""Editorial trim, batch B2b.

  1. Condense Conclusions (2) and (6), which repeat text already in the body and
     the Abstract.
  2. Condense the kinetic-correction paragraph of the Co-Deposition Window section
     (duplicated in Limitations 2).
  3. Move the whole Process Comparison section (with its table) from just before
     the Limitations up to just before the Thermodynamic Framework, as Reviewer 3
     requested ("the comparison ... can be shown in the Introduction, not close to
     the conclusion").
"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, 'manuscript.tex')

B = []

B.append((
    'Conclusions (2)',
    r"(2) Thermodynamic calculations indicate all three reduction pathways are strongly exergonic",
    r"dictating a close-spaced or diaphragm-integrated cell design.",
    r"(2) The $\ce{Ca^{2+}/Na+}$ co-deposition window is 120.2~mV (ideal) and remains positive (74.9--147.1~mV) for $\gamma_{\ce{CaCl2}} = 0.3$--1.0, with the critical $\gamma_{\ce{CaCl2}}$ at $\sim$0.02--0.04; the kinetic correction to this equilibrium window is not yet signed, since Downs-cell evidence suggests it may narrow rather than widen the window. A diffusion-layer analysis ($D = 1.0\times10^{-9}$~m$^2$/s, $\delta = 200~\mu$m) places Mg--Ca co-deposition between the Mg limiting current (0.56~A/cm$^2$) and the $\ce{Na+}$ onset (1.31~A/cm$^2$), with the equimolar deposit at $j \approx 1.1$~A/cm$^2$; the 0.9~V ohmic budget then constrains the interelectrode gap to $\lesssim$1.1~cm at $\kappa = 1.4$~S/cm, dictating a close-spaced or diaphragm-integrated cell."
))

B.append((
    'Conclusions (6)',
    r"(6) A Monte Carlo global uncertainty analysis ($N = 10^5$)",
    r"as the two processes differ in decomposition voltage, cathode product state, oxide solubility, and anode conditions.",
    r"(6) A Monte Carlo analysis ($N = 10^5$, $\eta_I \sim \mathrm{Tri}(0.50, 0.75, 0.88)$) gives median $W_{\mathrm{net}} = 13{,}141$~kWh/ton-Ti and $P(W_{\mathrm{net}} < 15{,}000) = 82.1\%$ relative to the FFC lower bound; that probability largely restates the assumed $\eta_I$ prior rather than providing an independent feasibility estimate. Current efficiency is the dominant uncertainty ($\rho = -0.85$), so its experimental validation is the most critical prerequisite. The Hall--H\'eroult analogy ($\eta_I = 90$--95\%) \cite{kvande2014} is a reference point, not a validation, since the two processes differ in decomposition voltage, cathode product state, oxide solubility and anode conditions."
))

B.append((
    'Co-Deposition Window: kinetic correction',
    r"The above window is an \emph{equilibrium} quantity. Under polarization, the effective deposition potentials shift",
    r"concentration polarization at very high $j$ could additionally reverse the trend by depleting $\ce{Ca^{2+}}$ at the cathode.",
    r"""The above window is an \emph{equilibrium} quantity. Under polarization the effective deposition potentials shift by the activation overpotential $\eta_{\mathrm{act}} = (RT/\alpha nF)\,\mathrm{asinh}(j/2j_0)$. Adopting order-of-magnitude values typical of chloride melts ($j_0^{\mathrm{Ca}}\approx 0.05$~A/cm$^2$, $j_0^{\mathrm{Na}}\approx 0.03$~A/cm$^2$, $\alpha = 0.5$) \cite{pletcher1990}, the overpotential of monovalent $\ce{Na+}$ grows far faster than that of divalent $\ce{Ca^{2+}}$ (Fig.~\ref{fig:overpotential}): at $j = 0.5$~A/cm$^2$, $\eta_{\mathrm{act}}^{\mathrm{Ca}} \approx 174$~mV versus $\eta_{\mathrm{act}}^{\mathrm{Na}} \approx 424$~mV, which would \emph{widen} the effective window from 120.2~mV to $\sim$370~mV. This estimate is qualitative and its sign is not established: the assumed $j_0^{\mathrm{Ca}} > j_0^{\mathrm{Na}}$ favours Ca, yet the Downs cell deposits Na from a $\ce{CaCl2}$-majority melt, indicating that $\ce{Ca^{2+}}$ reduction may instead be kinetically \emph{slower}, which would \emph{narrow} the practical window. The $j_0$ and $\alpha$ values for the quaternary melt are unknown and require cyclic-voltammetry measurement, so the direction of the kinetic correction must be established before the enlarged window of Fig.~\ref{fig:overpotential} can be relied upon; concentration polarization at very high $j$ could additionally reverse the trend by depleting $\ce{Ca^{2+}}$ at the cathode."""
))

MOVE_FROM = r"\section*{Process Comparison}"
MOVE_TO = r"\section*{Uncertainties and Limitations}"
INSERT_BEFORE = r"\section*{Thermodynamic Framework}"


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

    # ---- move the Process Comparison section ----
    if text.count(MOVE_FROM) != 1 or text.count(MOVE_TO) != 1 or text.count(INSERT_BEFORE) != 1:
        print('ABORTED (move step) - anchors not unique')
        sys.exit(1)
    i = text.index(MOVE_FROM)
    j = text.index(MOVE_TO)
    block = text[i:j]
    text = text[:i] + text[j:]
    k = text.index(INSERT_BEFORE)
    text = text[:k] + block + text[k:]
    print(f'  [ok] Process Comparison moved before Thermodynamic Framework '
          f'({len(block)} chars)')

    with io.open(PATH, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)
    print(f'  written: {PATH}')


if __name__ == '__main__':
    main()
