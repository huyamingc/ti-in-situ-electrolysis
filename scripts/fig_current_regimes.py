# -*- coding: utf-8 -*-
"""
Cathode co-deposition regime map + ohmic-drop constraint (JES revision, new figure)

Adds the missing mass-transport electrochemistry:
  j_lim,i = n F D_i c_i,b / delta   (limiting current density)
  Regime I  (j < j_lim_Mg): Mg-only deposition
  Regime II (j_lim_Mg < j < j_lim_Mg + j_lim_Ca): Mg-Ca co-deposition,
            Ca molar fraction of deposit = 1 - j_lim_Mg/j
  Regime III (j > j_lim_Mg + j_lim_Ca): Na+ co-deposition onset
  Ohmic: IR = j L / kappa

Nominal parameters (600 C, recommended melt x = 0.30/0.40/0.15/0.15):
  rho = 1.8 g/cm3, M_avg = 92.9 g/mol -> c_melt = 1.94e4 mol/m3
  c_MgCl2 = 5.81e3 mol/m3, c_CaCl2 = 7.75e3 mol/m3
  D_Mg = D_Ca = 1.0e-9 m2/s, delta = 200 um
  kappa = 1.4 S/cm

Run: python scripts/fig_current_regimes.py
Output: figures/fig_current_regimes.pdf, figures_eps/fig_current_regimes.eps
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

F = 96485.0
n = 2.0
rho = 1.8e3            # kg/m3
M_avg = 92.9e-3        # kg/mol
c_melt = rho / M_avg   # mol/m3
c_Mg = 0.30 * c_melt
c_Ca = 0.40 * c_melt
D = 1.0e-9             # m2/s
delta = 200e-6         # m

jlim_Mg = n * F * D * c_Mg / delta / 1e4   # A/cm2
jlim_Ca = n * F * D * c_Ca / delta / 1e4
jlim_tot = jlim_Mg + jlim_Ca
j_eq = 2.0 * jlim_Mg
print("c_melt = %.0f mol/m3, c_MgCl2 = %.0f, c_CaCl2 = %.0f" % (c_melt, c_Mg, c_Ca))
print("jlim_Mg = %.3f, jlim_Ca = %.3f, jlim_tot = %.3f, j_eq = %.3f A/cm2" %
      (jlim_Mg, jlim_Ca, jlim_tot, j_eq))
print("max Ca fraction (Na onset) = %.1f %%" % (100.0 * jlim_Ca / jlim_tot))

# concentration overpotential check: 816 mV gap -> c_s/c_b
RT2F = 8.314 * 873.0 / (2.0 * F)
cs_cb = np.exp(-0.816 / RT2F)
print("c_s/c_b at 816 mV concentration overpotential = %.2e" % cs_cb)

# sensitivity range of jlim_Mg: D 0.3-3e-9, delta 100-500 um
lo = n * F * 0.3e-9 * c_Mg / 500e-6 / 1e4
hi = n * F * 3.0e-9 * c_Mg / 100e-6 / 1e4
print("jlim_Mg sensitivity range: %.2f - %.2f A/cm2" % (lo, hi))

# ohmic numbers
kappa = 1.4  # S/cm
for L in [0.5, 1.0, 2.5]:
    print("IR at j_eq=%.2f, L=%.1f cm: %.2f V" % (j_eq, L, j_eq * L / kappa))
print("L required for IR=0.9 at j_eq: %.2f cm" % (0.9 * kappa / j_eq))

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.5, 4.2))

# ---------------- Panel (a): co-deposition regime map ----------------
jmax = 2.0
ax1.axvspan(0, jlim_Mg, color='#eceff1', zorder=0)
ax1.axvspan(jlim_Mg, jlim_tot, color='#dbe9f6', zorder=0)
ax1.axvspan(jlim_tot, jmax, color='#fdecea', zorder=0)

jj = np.linspace(jlim_Mg * 1.001, jmax, 400)
frac = (1.0 - jlim_Mg / jj) * 100.0
m = jj <= jlim_tot
ax1.plot(jj[m], frac[m], color='#1d5fa2', lw=2.4, zorder=3)
ax1.plot(jj[~m], frac[~m], color='#1d5fa2', lw=2.0, ls='--', zorder=3)

ax1.axvline(jlim_Mg, color='#5b6b7c', ls='--', lw=1.2, zorder=2)
ax1.axvline(jlim_tot, color='#b3261e', ls='--', lw=1.2, zorder=2)
ax1.axhline(50, color='#5b6b7c', ls=':', lw=1.0, zorder=2)
ax1.plot([j_eq], [50], 'o', color='#b4541c', ms=8, zorder=4)
ax1.annotate('equimolar alloy\n$j \\approx 2\\,j_{\\mathrm{lim,Mg}}$',
             xy=(j_eq, 50), xytext=(j_eq - 0.62, 62),
             fontsize=10, color='#b4541c',
             arrowprops=dict(arrowstyle='->', color='#b4541c', lw=1.2))

ax1.text(jlim_Mg / 2.0, 74, 'I: Mg only', ha='center', fontsize=10, color='#37474f')
ax1.text((jlim_Mg + jlim_tot) / 2.0, 74, 'II: Mg–Ca\nco-deposition', ha='center',
         fontsize=10, color='#1d5fa2')
ax1.text((jlim_tot + jmax) / 2.0, 74, 'III: + Na\nco-deposition', ha='center',
         fontsize=10, color='#b3261e')
ax1.text(jlim_Mg, 3.5, '$j_{\\mathrm{lim,Mg}}$', fontsize=10, ha='right', color='#5b6b7c')
ax1.text(jlim_tot + 0.02, 3.5, '$j_{\\mathrm{lim,Mg}} + j_{\\mathrm{lim,Ca}}$', fontsize=10,
         ha='left', color='#b3261e')

ax1.set_xlim(0, jmax)
ax1.set_ylim(0, 85)
ax1.set_xlabel('Current density $j$ (A cm$^{-2}$)', fontsize=11)
ax1.set_ylabel('Ca molar fraction of deposit (%)', fontsize=11)
ax1.tick_params(labelsize=10)

# ---------------- Panel (b): ohmic-drop constraint ----------------
kappa = 1.4
for L, col in [(0.5, '#2e7d4f'), (1.0, '#1d5fa2'), (2.5, '#b4541c')]:
    IR = jj * L / kappa
    ax2.plot(jj, IR, color=col, lw=2.2, label='$L$ = %.1f cm' % L)

ax2.axhline(0.9, color='#b3261e', ls='--', lw=1.4)
ax2.text(0.03, 0.955, '0.9 V ohmic budget (of 4.1 V cell)', fontsize=9.5,
         color='#b3261e', va='bottom')
ax2.axvline(j_eq, color='#5b6b7c', ls=':', lw=1.2)
ax2.text(j_eq + 0.03, 2.62, '$j \\approx 1.1$ A cm$^{-2}$\n(co-deposition)',
         fontsize=9.5, color='#5b6b7c')
ax2.annotate('$L \\lesssim 1.1$ cm', xy=(j_eq, 0.9), xytext=(j_eq - 0.85, 1.42),
             fontsize=10, color='#1d5fa2',
             arrowprops=dict(arrowstyle='->', color='#1d5fa2', lw=1.2))

ax2.set_xlim(0, jmax)
ax2.set_ylim(0, 3.2)
ax2.set_xlabel('Current density $j$ (A cm$^{-2}$)', fontsize=11)
ax2.set_ylabel('Ohmic drop $jL/\\kappa$ (V), $\\kappa$ = 1.4 S cm$^{-1}$', fontsize=11)
ax2.tick_params(labelsize=10)
ax2.legend(fontsize=9.5, loc='upper left', framealpha=0.95)

for ax, tag in [(ax1, '(a)'), (ax2, '(b)')]:
    ax.text(-0.14, 1.04, tag, transform=ax.transAxes, fontsize=12, fontweight='bold')

fig.tight_layout()
os.makedirs('../figures', exist_ok=True)
os.makedirs('../figures_eps', exist_ok=True)
fig.savefig('../figures/fig_current_regimes.pdf', bbox_inches='tight')
fig.savefig('../figures_eps/fig_current_regimes.eps', bbox_inches='tight', format='eps')
print("saved figures/fig_current_regimes.pdf and figures_eps/fig_current_regimes.eps")
