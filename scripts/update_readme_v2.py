# -*- coding: utf-8 -*-
"""Sync README with the post-plan revision: Case I numbers, reactor/separation content."""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, 'README.md')

R = [
    (
        'MC both bases',
        r"- Monte Carlo, ten parameters (N = 10⁵, seed = 42): median 13,141 kWh/ton-Ti, P(W_net < 15,000) = 82.1%;",
        r"- Monte Carlo, ten parameters (N = 10⁵, seed = 42): median 13,141 kWh/ton-Ti on the 1:1 basis and 13,536 on the CaO-only basis, with P(W_net < 15,000) = 82.1% and 76.6% respectively;",
    ),
    (
        'reactor / separation note',
        r"- 620 °C (pilot floor): window 119.6 mV (from 120.2 mV), energy change < 0.3%",
        r"""- 620 °C (pilot floor): window 119.6 mV (from 120.2 mV), energy change < 0.3%
- Cell architecture: Ti (4.5 g/cm³) settles through the melt (1.8 g/cm³) at ≈5 mm/s, and the
  Mg–Ca alloy (≈1.6 g/cm³) is lighter than the melt, so the product cannot be held in
  suspension; the design uses a settled TiO₂ bed on a sloped floor as the cathode, with the
  reductant electrodeposited within the bed and retained by capillarity, a shroud-isolated anode
  and semi-continuous gravity drainage
- Separation: the product inherits the precursor particle size, so screening cannot separate Ti
  from unreacted TiO₂; dry electrostatic separation (conductor vs insulator) is the primary step,
  with the oxide fraction returned to the cell""",
    ),
    (
        'status line',
        r"This repository now holds the **post-review revision**: the mechanism has been rebuilt around the "
        r"Ca + MgO -> CaO + Mg reaction, engineering content (flowsheet, reactor concept, product recovery) has been "
        r"added, the uncertainty analysis has been expanded from five to ten parameters, and results are reported at "
        r"both 600 and 620 C.",
        r"This repository now holds the **post-review revision** (54 pages): the mechanism has been rebuilt around the "
        r"Ca + MgO -> CaO + Mg reaction with Case I / Case II carried through, engineering content (flowsheet, settled-bed "
        r"reactor, semi-continuous operation, electrostatic separation) has been added, the uncertainty analysis has "
        r"been expanded to ten parameters, and results are reported at both 600 and 620 C.",
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
    print('  README.md updated')


if __name__ == '__main__':
    main()
