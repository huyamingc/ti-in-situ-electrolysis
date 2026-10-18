# -*- coding: utf-8 -*-
"""R3-1 reconstruction, batch 3: two small consistency notes.

  * Table tab:heatbal caption: state that its values are the Case II basis and
    give the Case I gross/net figures.
  * Monte Carlo paragraph: state that the reported energy distribution is the
    Case II basis and that Case I shifts it by ~3%.
"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, 'manuscript.tex')

R = [
    (
        'Table 7 caption: case basis',
        r"\caption{Full-process heat balance (basis: 1 ton Ti, 600~$^{\circ}$C)}",
        r"\caption{Full-process heat balance (basis: 1 ton Ti, 600~$^{\circ}$C). All values are for Case~II of "
        r"Table~\ref{tab:mbalance}; in the CaO-only Case~I the gross electrical demand is 12{,}632~kWh/ton and the net "
        r"consumption 12{,}933~kWh/ton, the remaining items being unchanged.}",
    ),
    (
        'Monte Carlo: case basis',
        r"median 13{,}141~kWh/ton-Ti (P5--P95: 10{,}875--16{,}722~kWh/ton-Ti).",
        r"median 13{,}141~kWh/ton-Ti (P5--P95: 10{,}875--16{,}722~kWh/ton-Ti) on the Case~II energy basis of "
        r"Table~\ref{tab:mbalance}; the CaO-only Case~I shifts this distribution upward by $\sim$3\%.",
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
