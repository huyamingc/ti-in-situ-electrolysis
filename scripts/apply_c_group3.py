# -*- coding: utf-8 -*-
"""Update the captions of the two Monte Carlo figures (C group)."""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, 'manuscript.tex')

R = [
    (
        'Fig 8 caption',
        r"\caption{Monte Carlo global uncertainty analysis ($N = 10^5$): (left) SCM reduction time distribution with lognormal fit; (right) net energy consumption distribution. Dashed lines indicate nominal values. The analysis simultaneously sampled five parameters: diffusion coefficient $D$, porosity $\varepsilon$, tortuosity $\tau$, current efficiency $\eta_I \sim \mathrm{Tri}(0.50, 0.75, 0.88)$, and cell voltage $V_{\mathrm{cell}} \sim \mathcal{N}(4.1, 0.3)$. The $\eta_I$ lower bound of 0.50 encompasses the worst-case FFC-like scenario.}",
        r"\caption{Monte Carlo global uncertainty analysis ($N = 10^5$, ten parameters): (a) SCM reduction time, with the nominal 6.3~min value marked (it corresponds to the upper end of the reductant-concentration range); (b) net energy consumption with the FFC lower bound; (c) probabilities that the co-deposition window exceeds 50~mV, that the liquidus lies below 600 and 620~$^{\circ}$C, and that the required interelectrode gap exceeds a 3~mm engineering floor, together with their joint probability at the 620~$^{\circ}$C operating floor; (d) Spearman rank correlation of each sampled parameter with the net energy. The sampled parameters are $D$, $\varepsilon$, $\tau$, $\eta_I \sim \mathrm{Tri}(0.50, 0.75, 0.88)$, $V_{\mathrm{cell}} \sim \mathcal{N}(4.1, 0.3)$, $\gamma_{\ce{CaCl2}}$, $\gamma_{\ce{NaCl}}$, the liquidus, the MgO solubility, the diffusion-layer thickness $\delta$ and the dissolved-reductant concentration $c_{\mathrm{red}}$.}",
    ),
    (
        'Fig 9 caption',
        r"\caption{Global parameter sensitivity (Spearman rank correlation): (left) SCM reduction time; (right) net energy consumption.}",
        r"\caption{Global parameter sensitivity (Spearman rank correlation) over the ten sampled parameters: (left) SCM reduction time; (right) net energy consumption.}",
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
