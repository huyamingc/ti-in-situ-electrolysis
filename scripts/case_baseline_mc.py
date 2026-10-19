# -*- coding: utf-8 -*-
"""Baseline heat/material balance and Monte Carlo on the single-potential basis.

Purpose
-------
The manuscript reports ONE net energy, 12,933 kWh/ton-Ti, because the cathode
potential is set by the more demanding regeneration step (CaO, 2.8277 V) whichever
oxide is returned to the cell. The earlier version of this script treated Case II
(MgO + CaO co-regenerated) as a cheaper baseline at 2.73 V; that mixed value is the
average of the two separate equilibrium potentials and cannot be held by a single
cathode, so it is recorded here as an unattainable energy-equivalent bound only.

What the script does:
  1. builds the full-process balance for both material-balance cases at the SAME
     cell voltage, showing that only the split between regeneration enthalpy and
     rejected heat changes between them;
  2. reproduces the published figures as a self-check;
  3. re-runs the 11-parameter Monte Carlo (one distribution, since both cases share
     the cell voltage);
  4. writes tab_case_baseline.csv and tab_monte_carlo_case.csv;
  5. optionally redraws figures 8 and 9.

Usage
-----
    py scripts/case_baseline_mc.py            # numbers + tables
    py scripts/case_baseline_mc.py --figures  # also redraw figures 8 and 9
"""
import os
import sys
import csv
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'output')
os.makedirs(OUT, exist_ok=True)

# ------------------------------------------------------------------ constants
F = 96485.0
Rg = 8.314
T = 873.15
M_Ti = 47.867
n_Ti = 1.0e6 / M_Ti                 # mol Ti per metric ton

ETA = 0.75                          # nominal current efficiency
ETA_AN, ETA_CA, OHM = 0.30, 0.20, 0.90
AUX = 50.0 + 300.0                  # salt pumping + post-treatment
TI_COOL = 42.0                      # Ti powder cooling recovery

# formation enthalpies at 298 K (Barin); Cp correction neglected, as in the paper
dHf_MgO = 601.6e3                   # J/mol
dHf_CaO = 634.9e3                   # J/mol

# reduction exotherms, kWh/ton-Ti, from Delta H of the two reduction paths
EXO_MIX = 1690.0                    # TiO2 + Mg + Ca -> Ti + MgO + CaO, -291.3 kJ/mol
EXO_CA = 1872.0                     # TiO2 + 2 Ca -> Ti + 2 CaO,       -322.6 kJ/mol

# single-potential decomposition voltage (CaO step) and adopt cell voltage
E_DECOMP = 2.8277
V_CELL = E_DECOMP + ETA_AN + ETA_CA + OHM      # 4.2277 V
W_REVERSIBLE = 4550.0               # TiO2 -> Ti + O2 reversible work, kWh/ton

# reversible minima: mixed is an unattainable bound, CaO is the realised path
W_MIN_MIXED = 6112.0                # 4F n_Ti * 2.729 / 3.6e6
W_MIN_CAO = 6334.0                  # 4F n_Ti * 2.8277 / 3.6e6


def balance(tag, dH_regen, exo, note):
    """Full-process balance for one material-balance case at the shared V_cell."""
    gross = 4.0 * F * n_Ti * V_CELL / (ETA * 3.6e6)
    total_in = gross + AUX
    net = total_in - TI_COOL

    dH_reg = dH_regen * n_Ti / 3.6e6          # kWh/ton absorbed by regeneration
    net_abs = dH_reg - exo                    # net reaction enthalpy absorbed
    waste = gross - net_abs                   # rejected as heat
    V_thermo = dH_regen / (4.0 * F)

    return dict(
        case=tag,
        E_decomp=E_DECOMP,
        V_thermoneutral=V_thermo,
        V_cell=V_CELL,
        gross=gross,
        total_input=total_in,
        net=net,
        dH_regen=dH_reg,
        net_absorbed=net_abs,
        waste_heat=waste,
        eff_process=W_MIN_CAO / net * 100.0,
        eff_second_law=W_REVERSIBLE / net * 100.0,
        elec_fraction=gross / total_in * 100.0,
        exotherm=exo,
        w_min=W_MIN_CAO,
    )


# ------------------------------------------------------------------ two cases
case_II = balance('II (MgO+CaO co-regenerated, 1:1 O partition)',
                  dHf_MgO + dHf_CaO, EXO_MIX,
                  'regeneration enthalpy 7,175 kWh/t; gross and net unchanged')
case_I = balance('I (CaO-only, Ca sole net oxygen carrier)',
                 2.0 * dHf_CaO, EXO_CA,
                 'regeneration enthalpy 7,369 kWh/t; gross and net unchanged')
cases = [case_II, case_I]

hdr = ('case', 'E_decomp', 'V_thermoneutral', 'V_cell', 'gross', 'total_input',
       'net', 'dH_regen', 'net_absorbed', 'waste_heat', 'exotherm',
       'eff_process', 'eff_second_law', 'elec_fraction')
with open(os.path.join(OUT, 'tab_case_baseline.csv'), 'w', newline='',
          encoding='utf-8-sig') as f:
    w = csv.writer(f)
    w.writerow(hdr)
    for c in cases:
        w.writerow([c[k] if isinstance(c[k], str) else round(c[k], 2) for k in hdr])

print('=' * 78)
print('FULL-PROCESS BALANCE, both material cases (eta=0.75, V_cell=%.4f V)' % V_CELL)
print('=' * 78)
print('%-46s %10s %10s' % ('quantity', 'Case II', 'Case I'))
for k, lbl in (('E_decomp', 'decomposition voltage (V)'),
               ('V_thermoneutral', 'thermoneutral voltage (V)'),
               ('V_cell', 'cell voltage (V)'),
               ('gross', 'gross electrical (kWh/t)'),
               ('total_input', 'total external input (kWh/t)'),
               ('net', 'NET consumption (kWh/t)'),
               ('dH_regen', 'regen enthalpy absorbed (kWh/t)'),
               ('exotherm', 'reduction exotherm (kWh/t)'),
               ('net_absorbed', 'net enthalpy absorbed (kWh/t)'),
               ('waste_heat', 'rejected as waste heat (kWh/t)'),
               ('eff_process', 'process efficiency (%)'),
               ('eff_second_law', 'second-law efficiency (%)'),
               ('elec_fraction', 'electrolysis fraction (%)')):
    fmt = '%10.3f %10.3f' if k in ('E_decomp', 'V_thermoneutral', 'V_cell') \
        else '%10.1f %10.1f'
    print('%-46s ' % lbl + fmt % (case_II[k], case_I[k]))

print('\nSelf-check against the manuscript (single-potential basis):')
checks = [('gross electrical 12,625', case_I['gross'], 12625.0, 3),
          ('net consumption 12,933', case_I['net'], 12933.0, 3),
          ('regen absorbed 7,369', case_I['dH_regen'], 7369.0, 15),
          ('reduction exotherm 1,872', case_I['exotherm'], 1872.0, 1),
          ('net absorbed 5,497', case_I['net_absorbed'], 5497.0, 15),
          ('waste heat 7,128', case_I['waste_heat'], 7128.0, 15),
          ('process eff 49.0', case_I['eff_process'], 49.0, 0.15),
          ('second law 35.2', case_I['eff_second_law'], 35.2, 0.15),
          ('elec fraction 97.3', case_I['elec_fraction'], 97.3, 0.15),
          ('Case II gross identical', abs(case_II['gross'] - case_I['gross']), 0.0, 0.01),
          ('Case II net identical', abs(case_II['net'] - case_I['net']), 0.0, 0.01)]
for lbl, got, ref, tol in checks:
    ok = abs(got - ref) <= tol
    print('  %-28s got %9.2f  ref %9.2f  %s' % (lbl, got, ref, 'OK' if ok else 'DIFF'))

# ------------------------------------------------------------------ Monte Carlo
N = 100000
np.random.seed(42)
D = np.random.uniform(1.0e-9, 3.0e-9, N)
eps = np.random.uniform(0.10, 0.50, N)
tau = np.random.uniform(1.5, 5.0, N)
eta = np.random.triangular(0.50, 0.75, 0.88, N)
V_noise = np.clip(np.random.normal(0.0, 0.30, N), -0.6, 0.4)
gamma_Ca = np.random.uniform(0.30, 1.00, N)
gamma_Na = np.random.uniform(0.70, 1.00, N)
T_liq = np.clip(543.7 + np.random.normal(0.0, 25.0, N), 494.0, 594.0)
S_MgO = np.random.uniform(0.5, 1.2, N)
delta = np.random.uniform(100e-6, 500e-6, N)
x_red = np.random.uniform(0.005, 0.030, N)

V_cell = np.clip(V_CELL + V_noise, V_CELL - 0.6, V_CELL + 0.4)
W = 4.0 * F * n_Ti * V_cell / (eta * 3.6e6) + AUX - TI_COOL


def pct(a, p):
    return float(np.percentile(a, p))


print('\n' + '=' * 78)
print('MONTE CARLO, 11 parameters, seed 42, N = %d' % N)
print('=' * 78)
mc_row = dict(case='single-potential', median=np.median(W), p5=pct(W, 5), p95=pct(W, 95),
              p_lt_15000=100.0 * np.mean(W < 15000),
              p_lt_12933=100.0 * np.mean(W < 12933))
print('  %-42s median %8.0f   P5-P95 %6.0f-%6.0f   P(<15000) %5.1f%%'
      % ('single-potential basis', mc_row['median'], mc_row['p5'], mc_row['p95'],
         mc_row['p_lt_15000']))

with open(os.path.join(OUT, 'tab_monte_carlo_case.csv'), 'w', newline='',
          encoding='utf-8-sig') as f:
    w = csv.writer(f)
    w.writerow(['case', 'median_kWh_t', 'p5', 'p95', 'P_lt_15000_pct', 'P_lt_12933_pct'])
    w.writerow([mc_row['case'], round(mc_row['median']), round(mc_row['p5']),
                round(mc_row['p95']), round(mc_row['p_lt_15000'], 1),
                round(mc_row['p_lt_12933'], 1)])

# sigma / rho for the net energy
from scipy import stats  # noqa: E402
mat = [D, eps, tau, eta, V_noise, gamma_Ca, gamma_Na, T_liq, S_MgO, delta, x_red]
names = ['D', 'eps', 'tau', 'eta_I', 'V_cell', 'gamma_CaCl2', 'gamma_NaCl',
         'T_liq', 'S_MgO', 'delta', 'c_red']
rho = [(names[i], float(stats.spearmanr(mat[i], W).correlation))
       for i in range(len(names))]
rho.sort(key=lambda t: -abs(t[1]))
print('\n  Spearman rho with net energy (top 5):')
for n, r in rho[:5]:
    print('    %-14s %+.3f' % (n, r))

# ------------------------------------------------------------------ figures
if '--figures' in sys.argv:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    FIG = os.path.join(ROOT, 'figures')
    EPS = os.path.join(ROOT, 'figures_eps')

    c_O, R_p = 1.06e5, 50e-6
    c_red = x_red * 1.938e4
    D_eff = D * eps / tau
    t_scm = c_O * R_p ** 2 / (6.0 * D_eff * c_red) / 60.0

    c_b = 0.30 * 1.94e4
    j_lim = 2 * F * D * c_b / delta / 1e4
    j_design = 2.0 * j_lim
    L_req = 0.9 * 1.4 / j_design

    E_Ca = -3.428 + Rg * T / (2 * F) * np.log(gamma_Ca * 0.40)
    E_Na = -3.440 + Rg * T / F * np.log(gamma_Na * 0.15)
    dE = (E_Ca - E_Na) * 1000.0
    ok_win = dE > 50.0
    ok_liq600 = T_liq < 600.0
    ok_liq620 = T_liq < 620.0
    ok_gap = L_req >= 0.30
    ok_all = ok_win & ok_liq620 & ok_gap

    fig, axs = plt.subplots(2, 2, figsize=(9.8, 6.9))
    ax = axs[0, 0]
    ax.hist(t_scm, bins=140, range=(0, 60), color='#4c72b0', alpha=0.85, density=True)
    ax.axvline(np.median(t_scm), color='k', ls='--', lw=1.3,
               label='median %.1f min' % np.median(t_scm))
    ax.axvline(6.3, color='r', ls=':', lw=1.3, label='nominal 6.3 min ($c_{red}$=3 mol%)')
    ax.set_xlabel('SCM reduction time (min)')
    ax.set_ylabel('density')
    ax.set_title(r'(a) Reduction time, 100 $\mu$m particles', fontsize=10)
    ax.legend(fontsize=7.5)

    ax = axs[0, 1]
    ax.hist(W, bins=140, range=(8000, 22000), color='#dd8452', alpha=0.85,
            density=True)
    ax.axvline(15000, color='r', ls=':', lw=1.5, label='FFC lower bound')
    ax.axvline(np.median(W), color='k', ls='--', lw=1.2,
               label='median {:,.0f} kWh/t'.format(np.median(W)))
    ax.set_xlabel('net equivalent energy (kWh/ton-Ti)')
    ax.set_ylabel('density')
    ax.set_title(r'(b) Energy consumption, single-potential basis', fontsize=10)
    ax.legend(fontsize=7.5)

    ax = axs[1, 0]
    names_b = ['window\n> 50 mV', 'liquidus\n< 620 $^{\\circ}$C',
               'liquidus\n< 600 $^{\\circ}$C', 'gap\n$L_{req}\\geq$3 mm',
               'joint\n@620 $^{\\circ}$C']
    vals = [100 * np.mean(ok_win), 100 * np.mean(ok_liq620),
            100 * np.mean(ok_liq600), 100 * np.mean(ok_gap), 100 * np.mean(ok_all)]
    bars = ax.bar(names_b, vals, color=['#4c72b0', '#55a868', '#55a868', '#dd8452', '#8172b2'])
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 1.5, '%.0f%%' % v, ha='center', fontsize=8)
    ax.set_ylim(0, 112)
    ax.set_ylabel('probability (%)')
    ax.set_title('(c) Feasibility probabilities', fontsize=10)

    ax = axs[1, 1]
    rho_w = [stats.spearmanr(mat[i], W).correlation for i in range(len(names))]
    lab = ['D', r'$\varepsilon$', r'$\tau$', r'$\eta_I$', r'$V_{\rm cell}$',
           r'$\gamma_{\rm CaCl_2}$', r'$\gamma_{\rm NaCl}$', r'$T_{\rm liq}$',
           r'$S_{\rm MgO}$', r'$\delta$', r'$c_{\rm red}$']
    o = np.argsort(np.abs(rho_w))[::-1]
    sel = [i for i in o if abs(rho_w[i]) > 0.02]
    yp = np.arange(len(sel))
    ax.barh(yp, [rho_w[i] for i in sel], color='#dd8452', alpha=0.9)
    ax.set_yticks(yp)
    ax.set_yticklabels([lab[i] for i in sel], fontsize=8.5)
    ax.axvline(0, color='k', lw=0.8)
    ax.set_xlabel(r'Spearman $\rho$ with net energy')
    ax.set_title('(d) Energy sensitivity', fontsize=10)
    ax.invert_yaxis()
    plt.tight_layout()
    fig.savefig(os.path.join(FIG, 'fig_monte_carlo.pdf'), bbox_inches='tight')
    fig.savefig(os.path.join(EPS, 'figure8.eps'), bbox_inches='tight')

    fig2, axs2 = plt.subplots(1, 2, figsize=(9.8, 4.0))
    rho_t = [stats.spearmanr(mat[i], t_scm).correlation for i in range(len(names))]
    for ax, rr, ttl in ((axs2[0], rho_t, '(a) SCM reduction time'),
                        (axs2[1], rho_w, '(b) Net energy consumption')):
        o = np.argsort(np.abs(rr))[::-1]
        sel = [i for i in o if abs(rr[i]) > 0.02]
        yp = np.arange(len(sel))
        ax.barh(yp, [rr[i] for i in sel], color='#4c72b0', alpha=0.9)
        ax.set_yticks(yp)
        ax.set_yticklabels([lab[i] for i in sel], fontsize=8.5)
        ax.axvline(0, color='k', lw=0.8)
        ax.set_xlabel(r'Spearman $\rho$')
        ax.set_title(ttl, fontsize=10)
        ax.invert_yaxis()
    plt.tight_layout()
    fig2.savefig(os.path.join(FIG, 'fig_sensitivity_tornado.pdf'), bbox_inches='tight')
    fig2.savefig(os.path.join(EPS, 'figure9.eps'), bbox_inches='tight')
    print('\n  -> figures 8 and 9 redrawn on the single-potential basis')

print('\n  -> output/tab_case_baseline.csv, output/tab_monte_carlo_case.csv')
