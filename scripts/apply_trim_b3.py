# -*- coding: utf-8 -*-
"""Editorial batch B3: the two remaining Reviewer-3 presentation items.

  R3-2: state the recommended quaternary composition and the criteria behind it at
        its first appearance (Process Description).
  R3-6: quantify the temperature advantage against the high-temperature molten-salt
        routes (Process Comparison).
"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, 'manuscript.tex')

B = [
    (
        'R3-2 composition criteria at first mention',
        r"The melt is a quaternary $\ce{MgCl2-CaCl2-NaCl-KCl}$ mixture. $\ce{MgCl2}$ serves as the primary salt and magnesium source; $\ce{CaCl2}$ enhances oxide solubility and lowers the melting point; NaCl and KCl act as fluxes to improve ionic conductivity and reduce viscosity \cite{sato1999}.",
        r"The melt is a quaternary $\ce{MgCl2-CaCl2-NaCl-KCl}$ mixture. $\ce{MgCl2}$ serves as the primary salt and magnesium source; $\ce{CaCl2}$ enhances oxide solubility and lowers the melting point; NaCl and KCl act as fluxes to improve ionic conductivity and reduce viscosity \cite{sato1999}. The recommended composition ($x_{\ce{MgCl2}} = 0.30$, $x_{\ce{CaCl2}} = 0.40$, $x_{\ce{NaCl}} = x_{\ce{KCl}} = 0.15$) is derived in the Salt Composition Design section from three requirements: a liquidus at least 30~$^{\circ}$C below the operating floor, a $\ce{Ca^{2+}/Na+}$ co-deposition window above 50~mV, and sufficient $\ce{CaCl2}$ to dissolve the by-product oxides.",
    ),
    (
        'R3-6 temperature advantage vs high-temperature melts',
        r"this process uses electrolysis to regenerate the reductant in situ while leveraging a liquid Mg--Ca alloy in which Ca supplies the thermodynamic deoxidation depth and Mg keeps the reductant molten at 600~$^{\circ}$C, where both pure metals are solid.",
        r"this process uses electrolysis to regenerate the reductant in situ while leveraging a liquid Mg--Ca alloy in which Ca supplies the thermodynamic deoxidation depth and Mg keeps the reductant molten at 600~$^{\circ}$C, where both pure metals are solid. The 600~$^{\circ}$C operating temperature is 300--350~$^{\circ}$C below the FFC route ($\sim$950~$^{\circ}$C) and the OS process ($\sim$900~$^{\circ}$C); that reduction is what the liquid alloy buys, and it lowers thermal losses and material corrosion without changing the thermodynamically required decomposition voltage.",
    ),
]


def main():
    with io.open(PATH, encoding='utf-8') as f:
        text = f.read()
    problems = [f'{n}: anchor found {text.count(o)} times' for n, o, _ in B if text.count(o) != 1]
    if problems:
        print('ABORTED - no changes written:')
        for p in problems:
            print('   ', p)
        sys.exit(1)
    for name, old, new in B:
        text = text.replace(old, new, 1)
        print(f'  [ok] {name}')
    with io.open(PATH, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)
    print(f'  written: {PATH}')


if __name__ == '__main__':
    main()
