# -*- coding: utf-8 -*-
"""
Graphical Abstract (GA) for JES submission - mandatory since 2025-04-01
Format: PNG, >= 300 dpi, filename prefixed GA_

Design: left = process schematic (closed-loop cell), right = four key numbers,
bottom = net reaction banner.
Run: python scripts/fig_ga.py  ->  GA_process.png at repo root
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch, Rectangle

fig = plt.figure(figsize=(12, 5.5), facecolor='white')
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 12)
ax.set_ylim(0, 5.5)
ax.axis('off')

C_MELT = '#f5efe0'
C_CATH = '#1d5fa2'
C_AN = '#455a64'
C_TI = '#90a4ae'
C_TIO2 = '#b4541c'
C_O2 = '#2e7d4f'
C_TXT = '#1c2430'
C_MUT = '#5b6b7c'

# ===================== left panel: cell schematic =====================
cell = FancyBboxPatch((0.35, 0.55), 5.5, 4.0, boxstyle='round,pad=0.08',
                      fc=C_MELT, ec=C_TXT, lw=2.0, zorder=1)
ax.add_patch(cell)

# cathode (left)
ax.add_patch(Rectangle((0.62, 1.0), 0.42, 3.1, fc=C_CATH, ec='none', zorder=3))
ax.text(0.83, 4.35, 'Cathode', ha='center', fontsize=13, color=C_CATH, fontweight='bold')
# anode (right)
ax.add_patch(Rectangle((5.16, 1.0), 0.42, 3.1, fc=C_AN, ec='none', zorder=3))
ax.text(5.30, 4.35, 'Inert anode', ha='center', fontsize=13, color=C_AN, fontweight='bold')

# Mg-Ca droplets at cathode
rng = np.random.default_rng(7)
for _ in range(7):
    y = rng.uniform(1.3, 3.6)
    r = rng.uniform(0.07, 0.12)
    ax.add_patch(Circle((1.28 + rng.uniform(0, 0.18), y), r, fc='#7fb3e0', ec=C_CATH,
                        lw=0.8, zorder=3))
ax.text(1.85, 3.85, 'Mg + Ca\nco-deposition', ha='left', va='center',
        fontsize=12.5, color=C_CATH, fontweight='bold')

# O2 bubbles at anode
for _ in range(7):
    y = rng.uniform(1.35, 3.7)
    r = rng.uniform(0.06, 0.11)
    ax.add_patch(Circle((4.92 - rng.uniform(0, 0.18), y), r, fc='none', ec=C_O2,
                        lw=1.6, zorder=3))
ax.text(4.45, 3.85, 'O$_2$ evolution', ha='right', va='center',
        fontsize=12.5, color=C_O2, fontweight='bold')

# TiO2 particles (left-center) -> Ti particles (right-center)
for _ in range(9):
    ax.add_patch(Circle((2.35 + rng.uniform(0, 0.7), rng.uniform(1.35, 3.0)), 0.085,
                        fc=C_TIO2, ec='none', zorder=3))
for _ in range(9):
    ax.add_patch(Circle((3.55 + rng.uniform(0, 0.7), rng.uniform(1.35, 3.0)), 0.085,
                        fc=C_TI, ec=C_TXT, lw=0.6, zorder=3))
ax.annotate('', xy=(3.62, 2.2), xytext=(2.95, 2.2),
            arrowprops=dict(arrowstyle='-|>', color=C_TXT, lw=2.2))
ax.text(3.28, 1.02, 'TiO$_2$ $\\rightarrow$ Ti powder', ha='center', fontsize=12.5,
        color=C_TXT, fontweight='bold')
ax.text(3.28, 0.72, 'MgO/CaO dissolve $\\rightarrow$ electrolytic regeneration',
        ha='center', fontsize=10.5, color=C_MUT)

# loop arrows
ax.add_patch(FancyArrowPatch((0.83, 4.15), (0.83, 4.15), color=C_CATH))  # placeholder
ax.annotate('', xy=(1.05, 4.12), xytext=(4.9, 4.12),
            arrowprops=dict(arrowstyle='-', color='none'))
ax.text(3.28, 4.78, '600 °C  MgCl$_2$–CaCl$_2$–NaCl–KCl melt', ha='center',
        fontsize=12, color=C_TXT, style='italic')
ax.annotate('', xy=(5.05, 4.95), xytext=(1.0, 4.95),
            arrowprops=dict(arrowstyle='-|>', color=C_MUT, lw=1.6,
                            connectionstyle='arc3,rad=-0.12'))
ax.annotate('', xy=(1.0, 4.95), xytext=(5.05, 4.95),
            arrowprops=dict(arrowstyle='-|>', color=C_MUT, lw=1.6,
                            connectionstyle='arc3,rad=-0.12'))
ax.text(3.05, 5.30, 'closed salt loop', ha='center', fontsize=10.5, color=C_MUT)

# ===================== right panel: four key numbers =====================
stats = [
    ('Ca$^{2+}$/Na$^+$ co-deposition window', '74.9–147.1 mV', '#1d5fa2'),
    ('Ca deoxidation limit (alloy)', '≈77 ppm O', '#b4541c'),
    ('100 μm particle reduction', '6.3 min', '#2e7d4f'),
    ('Net energy ($\\eta_I > 0.70$)', '12,552 kWh t$^{-1}$-Ti', '#455a64'),
]
y0 = 4.35
for i, (lab, val, col) in enumerate(stats):
    y = y0 - i * 1.02
    box = FancyBboxPatch((6.55, y - 0.42), 5.1, 0.86, boxstyle='round,pad=0.06',
                         fc='white', ec=col, lw=2.0, zorder=2)
    ax.add_patch(box)
    ax.text(6.85, y + 0.13, lab, ha='left', va='center', fontsize=11.5, color=C_MUT)
    ax.text(6.85, y - 0.20, val, ha='left', va='center', fontsize=17,
            color=col, fontweight='bold')

# ===================== bottom banner =====================
ax.add_patch(FancyBboxPatch((0.35, 0.02), 11.3, 0.42, boxstyle='round,pad=0.05',
                            fc='#eceff1', ec=C_MUT, lw=1.2, zorder=1))
ax.text(6.0, 0.23, 'Net reaction:  TiO$_2$ $\\rightarrow$ Ti + O$_2$   |   '
        'in-situ electrolytic Mg–Ca co-deposition, quaternary chloride melt, 600 °C',
        ha='center', va='center', fontsize=11.5, color=C_TXT)

fig.savefig('GA_process.png', dpi=300, facecolor='white')
print('saved GA_process.png')
