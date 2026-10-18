# -*- coding: utf-8 -*-
"""Dual-temperature results at the 620 C pilot floor (Reviewer 2, item 4).

Same Barin/Kubaschewski data and Meyer-Kelly Cp model as scripts/thermo_calc_v2.py.
Reports, at 600/620/650 C: the chloride decomposition voltages, the Ca2+/Na+
co-deposition window, the MgO and CaO decomposition voltages, and the resulting
cell voltages and net energies for the mixed and CaO-only regeneration cases.
"""
import math
import os
import csv

R = 8.314
F = 96485.0
n_Ti = 1.0e6 / 47.867

species = {
    'MgO':   {'Hf': -601600, 'S': 26.9,  'Cp_a': 48.982, 'Cp_b': 3.142e-3,  'Cp_c': -11.740e5},
    'CaO':   {'Hf': -635100, 'S': 39.7,  'Cp_a': 49.622, 'Cp_b': 4.519e-3,  'Cp_c': -6.945e5},
    'Mg':    {'Hf': 0,       'S': 32.7,  'Cp_a': 22.09,  'Cp_b': 10.46e-3,  'Cp_c': -0.418e5},
    'Ca':    {'Hf': 0,       'S': 41.6,  'Cp_a': 25.29,  'Cp_b': 3.85e-3,   'Cp_c': 0.0},
    'Na':    {'Hf': 0,       'S': 51.3,  'Cp_a': 28.2,   'Cp_b': 0.0,       'Cp_c': 0.0},
    'MgCl2': {'Hf': -641300, 'S': 89.6,  'Cp_a': 72.426, 'Cp_b': 15.82e-3,  'Cp_c': -3.721e5},
    'CaCl2': {'Hf': -795800, 'S': 104.6, 'Cp_a': 71.881, 'Cp_b': 16.92e-3,  'Cp_c': -3.891e5},
    'NaCl':  {'Hf': -411200, 'S': 72.1,  'Cp_a': 50.074, 'Cp_b': 16.21e-3,  'Cp_c': -1.029e5},
    'Cl2':   {'Hf': 0,       'S': 223.1, 'Cp_a': 36.90,  'Cp_b': 0.99e-3,   'Cp_c': -3.52e5},
    'O2':    {'Hf': 0,       'S': 205.2, 'Cp_a': 29.96,  'Cp_b': 4.18e-3,   'Cp_c': -1.67e5},
}
transitions = {
    'Mg': {'Tm': 923,  'Hfus': 8950, 'Cp_l': 32.7},
    'Ca': {'Tm': 1115, 'Hfus': 8540, 'Cp_l': 30.0},
    'Na': {'Tm': 371,  'Hfus': 2600, 'Cp_l': 30.5},
}


def get_H_S(name, T):
    sp = species[name]
    a, b, c = sp['Cp_a'], sp['Cp_b'], sp['Cp_c']
    Tr = 298.0
    H, S = sp['Hf'], sp['S']
    tr = transitions.get(name)
    if tr and T > tr['Tm']:
        Tm = tr['Tm']
        H += a * (Tm - Tr) + b / 2 * (Tm**2 - Tr**2) - c * (1 / Tm - 1 / Tr)
        S += a * math.log(Tm / Tr) + b * (Tm - Tr) - c / 2 * (1 / Tm**2 - 1 / Tr**2)
        H += tr['Hfus']
        S += tr['Hfus'] / Tm
        H += tr['Cp_l'] * (T - Tm)
        S += tr['Cp_l'] * math.log(T / Tm)
    else:
        H += a * (T - Tr) + b / 2 * (T**2 - Tr**2) - c * (1 / T - 1 / Tr)
        S += a * math.log(T / Tr) + b * (T - Tr) - c / 2 * (1 / T**2 - 1 / Tr**2)
    return H, S


def dG(rxn, T):
    dH = sum(k * get_H_S(n, T)[0] for n, k in rxn.items())
    dS = sum(k * get_H_S(n, T)[1] for n, k in rxn.items())
    return dH - T * dS


def formation(comp, ref, coeff, T):
    """Gibbs energy of formation of `comp` from elements (ref = Cl2 or O2)."""
    rxn = {comp: 1, ref: -coeff}
    for el in set(comp.replace('2', '').replace('Cl', ' ').replace('O', ' ').split()):
        pass
    return dG(rxn, T)


rows = []
print(f'{"T(C)":>5} | {"MgCl2":>6} {"CaCl2":>6} {"NaCl":>6} {"window":>8} | '
      f'{"MgO":>6} {"CaO":>6} | {"V_mix":>6} {"net_mix":>8} {"net_CaO":>8}')
for Tc in (600.0, 620.0, 650.0):
    T = Tc + 273.15
    dGf_MgCl2 = dG({'MgCl2': 1, 'Mg': -1, 'Cl2': -1}, T)
    dGf_CaCl2 = dG({'CaCl2': 1, 'Ca': -1, 'Cl2': -1}, T)
    dGf_NaCl = dG({'NaCl': 1, 'Na': -1, 'Cl2': -0.5}, T)
    Ed_MgCl2 = -dGf_MgCl2 / (2 * F)
    Ed_CaCl2 = -dGf_CaCl2 / (2 * F)
    Ed_NaCl = -dGf_NaCl / (1 * F)

    E_Ca = -Ed_CaCl2 + R * T / (2 * F) * math.log(0.40)
    E_Na = -Ed_NaCl + R * T / F * math.log(0.15)
    win = (E_Ca - E_Na) * 1000.0

    dGf_MgO = dG({'MgO': 1, 'Mg': -1, 'O2': -0.5}, T)
    dGf_CaO = dG({'CaO': 1, 'Ca': -1, 'O2': -0.5}, T)
    Ed_MgO = -dGf_MgO / (2 * F)
    Ed_CaO = -dGf_CaO / (2 * F)

    V_mix = (Ed_MgO + Ed_CaO) / 2 + 0.30 + 0.20 + 0.90
    V_cao = Ed_CaO + 0.30 + 0.20 + 0.90

    def W(V):
        return 4 * F * n_Ti * V / (0.75 * 3.6e6) + 350.0 - 42.0

    print(f'{Tc:5.0f} | {Ed_MgCl2:6.3f} {Ed_CaCl2:6.3f} {Ed_NaCl:6.3f} {win:8.1f} | '
          f'{Ed_MgO:6.3f} {Ed_CaO:6.3f} | {V_mix:6.2f} {W(V_mix):8.0f} {W(V_cao):8.0f}')
    rows.append([f'{Tc:.0f}', f'{Ed_MgCl2:.3f}', f'{Ed_CaCl2:.3f}', f'{Ed_NaCl:.3f}',
                 f'{win:.1f}', f'{Ed_MgO:.3f}', f'{Ed_CaO:.3f}', f'{V_mix:.2f}',
                 f'{W(V_mix):.0f}', f'{W(V_cao):.0f}'])

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'output',
                   'tab_dual_temperature.csv')
os.makedirs(os.path.dirname(out), exist_ok=True)
with open(out, 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.writer(f)
    w.writerow(['T_C', 'Ed_MgCl2_V', 'Ed_CaCl2_V', 'Ed_NaCl_V', 'window_mV',
                'Ed_MgO_V', 'Ed_CaO_V', 'V_cell_mixed', 'net_mixed_kWh_t',
                'net_CaO_only_kWh_t'])
    w.writerows(rows)
print(f'  -> {os.path.normpath(out)}')
