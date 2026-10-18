# -*- coding: utf-8 -*-
"""Monte Carlo, extended to eleven parameters (Reviewer 2, items 3 and 6).

Additions over the original five-parameter run (six further parameters, so the
sampler draws eleven in total):
  * gamma_CaCl2 ~ U(0.3, 1.0), gamma_NaCl ~ U(0.7, 1.0)   -> co-deposition window
  * liquidus    ~ N(544, 25) truncated to [494, 594] C     -> operable temperature
  * MgO solubility ~ U(0.5, 1.2) wt%                       -> salt inventory
  * diffusion-layer thickness delta ~ U(100, 500) um       -> j_lim,Mg, hence the
        equimolar design current density j = 2 j_lim,Mg and the required
        interelectrode gap L_req = 0.9*kappa/j at the fixed 0.9 V ohmic budget
  * dissolved reductant concentration c_red ~ U(0.5, 3.0) mol% -> SCM time

The ohmic budget is held fixed (as in the paper) and the *design consequence* of
delta is reported as the required gap, not as an unphysical cell voltage.

Outputs:
  figures/fig_monte_carlo.pdf         + figures_eps/figure8.eps   (4 panels)
  figures/fig_sensitivity_tornado.pdf + figures_eps/figure9.eps   (2 panels)
  output/tab_monte_carlo_v2_stats.csv
"""
import os
import csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG = os.path.join(ROOT, 'figures')
EPS = os.path.join(ROOT, 'figures_eps')
OUT = os.path.join(ROOT, 'output')
for d in (FIG, EPS, OUT):
    os.makedirs(d, exist_ok=True)

np.random.seed(42)
N = 100000

F, Rg, T = 96485.0, 8.314, 873.15
n_Ti = 1.0e6 / 47.867

# ------------------------------------------------------------------ parameters
D = np.random.uniform(1.0e-9, 3.0e-9, N)
eps = np.random.uniform(0.10, 0.50, N)
tau = np.random.uniform(1.5, 5.0, N)
eta = np.random.triangular(0.50, 0.75, 0.88, N)
V_cell = np.clip(np.random.normal(4.10, 0.30, N), 3.5, 4.5)
gamma_Ca = np.random.uniform(0.30, 1.00, N)
gamma_Na = np.random.uniform(0.70, 1.00, N)
T_liq = np.clip(543.7 + np.random.normal(0.0, 25.0, N), 494.0, 594.0)
S_MgO = np.random.uniform(0.5, 1.2, N)
delta = np.random.uniform(100e-6, 500e-6, N)
x_red = np.random.uniform(0.005, 0.030, N)

# ------------------------------------------------------------------ SCM time
c_O, R_p = 1.06e5, 50e-6
c_red = x_red * 1.938e4
D_eff = D * eps / tau
t_scm = c_O * R_p**2 / (6.0 * D_eff * c_red) / 60.0        # min

# ------------------------------------------------------------------ energy
W_net = 4 * F * n_Ti * V_cell / (eta * 3.6e6) + 350.0 - 42.0

# ------------------------------------- equimolar design point and required gap
c_b = 0.30 * 1.94e4
j_lim = 2 * F * D * c_b / delta / 1e4                      # A/cm2
j_design = 2.0 * j_lim                                     # equimolar deposit
L_req = 0.9 * 1.4 / j_design                               # cm, 0.9 V budget

# ------------------------- current efficiency correlated with current density
# eta falls as j rises above the nominal co-deposition point (back-reaction and
# Na co-deposition both scale with j, as noted in the text); beta is the
# fractional loss per unit relative increase in j.
BETA, J_REF = 0.10, 1.10
eta_eff = np.clip(eta * (1.0 - BETA * (j_design / J_REF - 1.0)), 0.40, 0.95)
W_corr = 4 * F * n_Ti * V_cell / (eta_eff * 3.6e6) + 350.0 - 42.0

# ------------------------------------------------------------ feasibility
E_Ca = -3.428 + Rg * T / (2 * F) * np.log(gamma_Ca * 0.40)
E_Na = -3.440 + Rg * T / F * np.log(gamma_Na * 0.15)
dE = (E_Ca - E_Na) * 1000.0

ok_win = dE > 50.0
ok_liq600 = T_liq < 600.0
ok_liq620 = T_liq < 620.0
ok_gap = L_req >= 0.30                                     # >= 3 mm engineering floor
ok_all = ok_win & ok_liq620 & ok_gap
ok_all_strict = ok_win & ok_liq600 & ok_gap


def pct(a, p):
    return float(np.percentile(a, p))


rows = [
    ['samples', N, 'seed 42'],
    ['t_SCM median (min)', '%.1f' % np.median(t_scm),
     'P5-P95 %.1f-%.1f (nominal 6.3 min at c_red = 3 mol%%)' % (pct(t_scm, 5), pct(t_scm, 95))],
    ['W_net median (kWh/t)', '{:,.0f}'.format(np.median(W_net)),
     'P5-P95 {:.0f}-{:.0f}'.format(pct(W_net, 5), pct(W_net, 95))],
    ['P(W_net < 15000)', '%.1f %%' % (100 * np.mean(W_net < 15000)), 'FFC lower bound'],
    ['W median, eta correlated with j (kWh/t)', '{:,.0f}'.format(np.median(W_corr)),
     'P5-P95 {:.0f}-{:.0f}'.format(pct(W_corr, 5), pct(W_corr, 95))],
    ['P(W < 15000), eta correlated with j', '%.1f %%' % (100 * np.mean(W_corr < 15000)),
     'beta = 0.10 per unit j/j_ref'],
    ['j_lim,Mg median (A/cm2)', '%.2f' % np.median(j_lim),
     'P5-P95 %.2f-%.2f' % (pct(j_lim, 5), pct(j_lim, 95))],
    ['j_design median (A/cm2)', '%.2f' % np.median(j_design), 'equimolar deposit'],
    ['L_req median (cm)', '%.2f' % np.median(L_req), 'P95 %.2f cm' % pct(L_req, 95)],
    ['P(window > 50 mV)', '%.1f %%' % (100 * np.mean(ok_win)), 'P5 window %.0f mV' % pct(dE, 5)],
    ['P(liquidus < 600 C)', '%.1f %%' % (100 * np.mean(ok_liq600)), ''],
    ['P(liquidus < 620 C)', '%.1f %%' % (100 * np.mean(ok_liq620)), ''],
    ['P(L_req >= 0.30 cm)', '%.1f %%' % (100 * np.mean(ok_gap)), 'gap engineering floor'],
    ['P(all feasible @620 C)', '%.1f %%' % (100 * np.mean(ok_all)), 'window + liquidus + gap'],
    ['P(all feasible @600 C)', '%.1f %%' % (100 * np.mean(ok_all_strict)), ''],
]
with open(os.path.join(OUT, 'tab_monte_carlo_v2_stats.csv'), 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.writer(f)
    w.writerow(['quantity', 'value', 'note'])
    w.writerows(rows)
for r in rows:
    print(f'  {str(r[0]):30s} {str(r[1]):>12s}  {r[2]}')

labels = ['D', r'$\varepsilon$', r'$\tau$', r'$\eta_I$', r'$V_{\rm cell}$',
          r'$\gamma_{\rm CaCl_2}$', r'$\gamma_{\rm NaCl}$', r'$T_{\rm liq}$',
          r'$S_{\rm MgO}$', r'$\delta$', r'$c_{\rm red}$']
mat = np.vstack([D, eps, tau, eta, V_cell, gamma_Ca, gamma_Na, T_liq, S_MgO, delta, c_red])
rho_t = [stats.spearmanr(mat[i], t_scm).correlation for i in range(len(labels))]
rho_w = [stats.spearmanr(mat[i], W_net).correlation for i in range(len(labels))]

# ================================================== figure 8 (four panels)
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
ax.hist(W_net, bins=140, range=(8000, 22000), color='#dd8452', alpha=0.85, density=True)
ax.axvline(15000, color='r', ls=':', lw=1.5, label='FFC lower bound')
ax.axvline(np.median(W_net), color='k', ls='--', lw=1.2,
           label='median {:,.0f} kWh/t'.format(np.median(W_net)))
ax.set_xlabel('net equivalent energy (kWh/ton-Ti)')
ax.set_ylabel('density')
ax.set_title(r'(b) Energy consumption (10 parameters)', fontsize=10)
ax.legend(fontsize=7.5)

ax = axs[1, 0]
names = ['window\n> 50 mV', 'liquidus\n< 620 $^{\\circ}$C', 'liquidus\n< 600 $^{\\circ}$C',
         'gap\n$L_{req}\\geq$3 mm', 'joint\n@620 $^{\\circ}$C']
vals = [100 * np.mean(ok_win), 100 * np.mean(ok_liq620), 100 * np.mean(ok_liq600),
        100 * np.mean(ok_gap), 100 * np.mean(ok_all)]
bars = ax.bar(names, vals, color=['#4c72b0', '#55a868', '#55a868', '#dd8452', '#8172b2'])
for b, v in zip(bars, vals):
    ax.text(b.get_x() + b.get_width() / 2, v + 1.5, '%.0f%%' % v, ha='center', fontsize=8)
ax.set_ylim(0, 112)
ax.set_ylabel('probability (%)')
ax.set_title('(c) Feasibility probabilities', fontsize=10)

ax = axs[1, 1]
o = np.argsort(np.abs(rho_w))[::-1]
sel = [i for i in o if abs(rho_w[i]) > 0.02]
yp = np.arange(len(sel))
ax.barh(yp, [rho_w[i] for i in sel], color='#dd8452', alpha=0.9)
ax.set_yticks(yp)
ax.set_yticklabels([labels[i] for i in sel], fontsize=8.5)
ax.axvline(0, color='k', lw=0.8)
ax.set_xlabel(r'Spearman $\rho$ with net energy')
ax.set_title('(d) Energy sensitivity', fontsize=10)
ax.invert_yaxis()

plt.tight_layout()
fig.savefig(os.path.join(FIG, 'fig_monte_carlo.pdf'), bbox_inches='tight')
fig.savefig(os.path.join(EPS, 'figure8.eps'), bbox_inches='tight')

# ================================================== figure 9 (tornado)
fig2, axs2 = plt.subplots(1, 2, figsize=(9.8, 4.0))
for ax, rho, ttl in ((axs2[0], rho_t, '(a) SCM reduction time'),
                     (axs2[1], rho_w, '(b) Net energy consumption')):
    o = np.argsort(np.abs(rho))[::-1]
    sel = [i for i in o if abs(rho[i]) > 0.02]
    yp = np.arange(len(sel))
    ax.barh(yp, [rho[i] for i in sel], color='#4c72b0', alpha=0.9)
    ax.set_yticks(yp)
    ax.set_yticklabels([labels[i] for i in sel], fontsize=8.5)
    ax.axvline(0, color='k', lw=0.8)
    ax.set_xlabel(r'Spearman $\rho$')
    ax.set_title(ttl, fontsize=10)
    ax.invert_yaxis()
plt.tight_layout()
fig2.savefig(os.path.join(FIG, 'fig_sensitivity_tornado.pdf'), bbox_inches='tight')
fig2.savefig(os.path.join(EPS, 'figure9.eps'), bbox_inches='tight')
print('  -> figures + output/tab_monte_carlo_v2_stats.csv written')
