# -*- coding: utf-8 -*-
"""R3-1 reconstruction, batch 4: remove the last two stale narrative fragments.

  * E-pO2- section: "...complementary roles of Mg for rapid bulk reduction and Ca
    for deep deoxidation" -> the reconstructed division of labour.
  * Mg-Ca alloy section: "...favorable for sustained complementary reduction" ->
    the liquid-phase framing.
"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, 'manuscript.tex')

R = [
    (
        'E-pO2 section: division of labour',
        r"Such a shift would be favorable for the proposed complementary mechanism, reinforcing the complementary roles of Mg for rapid bulk reduction and Ca for deep deoxidation.",
        r"Such a shift would be favorable for the proposed mechanism, reinforcing the division of labour adopted here: Ca provides the deoxidation depth, while the Mg--Ca alloy provides the liquid reductant phase and the transport path at the design temperature (see the Reduction Thermodynamics section).",
    ),
    (
        'Mg-Ca alloy section: liquid phase framing',
        r"The strong negative deviation ($\gamma \ll 1$) suggests that the Mg--Ca liquid alloy is thermodynamically stable, which is favorable for sustained complementary reduction.",
        r"The strong negative deviation ($\gamma \ll 1$) suggests that the Mg--Ca liquid alloy is thermodynamically stable, which is what keeps the reductant in a liquid state at the 600~$^{\circ}$C design temperature, where both pure metals are solid.",
    ),
]


def main():
    with io.open(PATH, encoding='utf-8') as f:
        text = f.read()
    problems = [f'{n}: anchor found {text.count(o)} times' for n, o, _ in R if text.count(o) != 1]
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
    print(f'  written: {PATH}')


if __name__ == '__main__':
    main()
