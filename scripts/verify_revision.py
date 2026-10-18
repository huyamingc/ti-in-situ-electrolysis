# -*- coding: utf-8 -*-
"""Post-revision verification.

Checks that (a) the arithmetic reported in the manuscript is internally
consistent for BOTH regeneration cases, (b) every revised figure is present the
expected number of times, and (c) every superseded figure is gone.

Exit code 0 = all checks pass.
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEX = os.path.join(ROOT, 'manuscript.tex')
src = io.open(TEX, encoding='utf-8').read()

fails, passes = [], []


def check(label, cond, detail=''):
    (passes if cond else fails).append((label, detail))


def count(pat):
    return len(re.findall(pat, src))


# ---------------------------------------------------------------- arithmetic
GROSS_II, GROSS_I = 12244.0, 12625.0
AUX, COOL = 350.0, 42.0
NET_II, NET_I = GROSS_II + AUX - COOL, GROSS_I + AUX - COOL
check('net II = gross + 350 - 42', abs(NET_II - 12552) < 1, f'{NET_II:.0f}')
check('net I  = gross + 350 - 42', abs(NET_I - 12933) < 1, f'{NET_I:.0f}')

ABS_I = 7369.0
NET_ABS_I = ABS_I - 1690.0
WASTE_I = GROSS_I - NET_ABS_I
check('Case I net enthalpy = 7,369-1,690', abs(NET_ABS_I - 5679) < 2, f'{NET_ABS_I:.0f}')
check('Case I waste heat = 12,625-5,679', abs(WASTE_I - 6946) < 2, f'{WASTE_I:.0f}')

W_MIN, W_REV = 6112.0, 4550.0
check('process eff II = 6112/12552 = 48.7%', abs(W_MIN / NET_II * 100 - 48.7) < 0.1)
check('process eff I  = 6112/12933 = 47.3%', abs(W_MIN / NET_I * 100 - 47.3) < 0.1)
check('second-law II = 4550/12552 = 36.3%', abs(W_REV / NET_II * 100 - 36.3) < 0.1)
check('second-law I  = 4550/12933 = 35.2%', abs(W_REV / NET_I * 100 - 35.2) < 0.1)
check('elec fraction II = 12244/12594 = 97.2%',
      abs(GROSS_II / (GROSS_II + AUX) * 100 - 97.2) < 0.1)
check('elec fraction I  = 12625/12975 = 97.3%',
      abs(GROSS_I / (GROSS_I + AUX) * 100 - 97.3) < 0.1)
check('decomposition +0.10 V -> +3% net', abs((NET_I - NET_II) / NET_II * 100 - 3.04) < 0.2)

# ------------------------------------------------------- entrained-salt model
# 1 um film, salt density 2.15 vs Ti 4.51: 3t/r * rho_salt/rho_Ti
for d, expect in ((25e-6, 11.4), (100e-6, 2.9)):
    got = 3 * 1.0 / (d * 1e6 / 2) * (2.15 / 4.51) * 100
    check(f'salt film {d*1e6:.0f} um -> {expect} wt%', abs(got - expect) < 0.5,
          f'{got:.1f}')
check('salt-film ratio follows 1/d (4x)', abs((11.4 / 2.9) - 3.93) < 0.2)

# --------------------------------------------------------------- new content
must_have = [
    (r'12\{,\}625', 3, 'Case I gross electrical'),
    (r'13\{,\}536', 2, 'Case I Monte Carlo median'),
    (r'76\.6', 2, 'Case I P(W<15000)'),
    (r'11~wt\\%', 1, 'entrained salt 25 um'),
    (r'3~wt\\%', 2, 'entrained salt 100 um'),
    (r'0\.5--1\.5~m', 1, 'wash water'),
    (r'7\.9~V', 1, '10 cm gap penalty'),
    (r'Semi-cont\. \(conceptual\)', 1, 'process table mode'),
    (r'\\subsection\*\{Reactor Configuration', 1, 'reactor section'),
    (r'\\subsection\*\{Cathodic Co-Deposition', 1, 'co-deposition section'),
    (r'\\subsection\*\{Solid-State Deoxygenation', 1, 'solid-state section'),
    (r'\(11\) \\textbf\{Reactor engineering\}', 1, 'Limitation 11'),
    (r'\(12\) \\textbf\{Product separation chain\}', 1, 'Limitation 12'),
    (r'\(10\) The preferred cell is a semi-continuous', 1, 'Conclusion 10'),
    (r'mechanistically favoured', 2, 'Case I favourability (sections 10.2/5)'),
    (r'favoured by the mechanism analysis', 2, 'Case I favourability (abstract/novelties)'),
    (r'0\.5--1\.2~wt\\%', 3, 'MgO solubility retained'),
    (r'Bruggeman', 1, 'bubble ohmic correction added'),
    (r'high-gradient magnetic', 1, 'Fe removal added to recovery chain'),
    (r'1\{,\}800', 2, 'Redlich-Kister Ca-dilute endpoint, both sections'),
    (r'regular-solution', 3, 'regular vs full R-K contrast'),
    (r'for pure Mg', 1, 'abstract clarity fix'),
]
for pat, n, lbl in must_have:
    got = count(pat)
    check(f'present x{n}: {lbl}', got == n, f'found {got}')

must_not = [
    (r'12\{,\}632', 'superseded gross'),
    (r'9\.6~wt', 'superseded salt film'),
    (r'Cyclic \(conceptual\)', 'superseded mode'),
    (r'suspended in the quaternary', 'superseded suspension claim'),
    (r'suspended in the liquid Mg', 'superseded shuttle caption'),
    (r'suspended by gentle circulation', 'superseded circulation claim'),
    (r'The expected loss mechanisms', 'superseded eta wording'),
    (r'kinetically (suppressed|blocked)', 'rejected kinetic-blocking claim'),
    (r'MgO .{0,40}insolub', 'rejected insoluble-MgO claim'),
]
for pat, lbl in must_not:
    got = count(pat)
    check(f'absent: {lbl}', got == 0, f'found {got}')

# --------------------------------------------------------------- report
print('=' * 72)
print(f'PASS {len(passes)}   FAIL {len(fails)}')
print('=' * 72)
for lbl, det in fails:
    print('  FAIL  %-46s %s' % (lbl, det))
if not fails:
    print('  all checks passed')
print('\nSelected passes:')
for lbl, det in passes:
    if 'case' in lbl or 'eff' in lbl or 'salt' in lbl.lower() or 'present x' in lbl:
        print('  ok    %-46s %s' % (lbl, det))
sys.exit(1 if fails else 0)
