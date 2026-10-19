# -*- coding: utf-8 -*-
"""Mechanism figures for the R3-1 reconstruction.

  (A) fig_r3_competition : driving force of Ca + [O] -> CaO and Mg + [O] -> MgO vs the
      oxygen content in Ti, against the constant driving force of the cross reaction
      Ca + MgO -> CaO + Mg.  Shows that the crossover is identically the Mg-only
      deoxidation limit (3908 ppm), and marks the a_MgO ceiling below it.
  (B) fig_r3_shuttle : the two oxygen-transfer channels at a TiO2 particle /
      liquid Mg-Ca alloy / melt interface.
"""
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG = os.path.join(ROOT, 'figures')
EPS = os.path.join(ROOT, 'figures_eps')
for d in (FIG, EPS):
    os.makedirs(d, exist_ok=True)

R, T = 8.314, 873.15
RT = R * T
DG_CA, DG_MG, DG_CROSS = -45016.0, -6816.0, -38200.0
W_CROSS = 3908.0

# ==================================================== (A) competition diagram
w_ppm = np.logspace(1, 5.4, 600)
wf = w_ppm / 1e4
dG_Ca = (DG_CA - RT * np.log(wf)) / 1000.0
dG_Mg = (DG_MG - RT * np.log(wf)) / 1000.0

fig, ax = plt.subplots(figsize=(6.8, 4.6))
ax.plot(w_ppm, dG_Ca, color='#c44e52', lw=2.2, label=r'Ca + [O]$_{\rm Ti}\rightarrow$ CaO')
ax.plot(w_ppm, dG_Mg, color='#55a868', lw=2.2, label=r'Mg + [O]$_{\rm Ti}\rightarrow$ MgO')
ax.axhline(DG_CROSS / 1000.0, color='#4c72b0', lw=2.2, ls='--',
           label=r'Ca + MgO $\rightarrow$ CaO + Mg  (std. states)')
ax.axhline(0.0, color='k', lw=0.8)
ax.axvline(W_CROSS, color='0.4', lw=1.1, ls=':')

ax.set_xscale('log')
ax.set_xlim(1, 2.5e5)
ax.set_ylim(-72, 78)
ax.set_xlabel(r'oxygen content in Ti,  $w_{[\rm O]}$  (ppm)')
ax.set_ylabel(r'$\Delta G$  (kJ mol$^{-1}$)')

ax.text(W_CROSS, 74, '3908 ppm\n= Mg-only limit\n= crossover', ha='center', va='top', fontsize=7.4,
        bbox=dict(boxstyle='round,pad=0.28', fc='white', ec='0.65'))
ax.text(70, 14, 'Ca attacks\ndissolved MgO', fontsize=8.2, ha='center', color='#2f4c7a')
ax.text(2.6e4, -24, 'Ca attacks\nthe Ti oxygen', fontsize=8.2, ha='center', color='#8c2f33')
ax.text(1.3, 74,
        r'below 3908 ppm, continuing to the Ca endpoint requires'
        '\n'
        r'$a_{\rm MgO} < 5\times10^{-3}$   (Eq. 11)',
        fontsize=7.4, va='top',
        bbox=dict(boxstyle='round,pad=0.32', fc='#fffbe6', ec='#c9b458'))
ax.legend(fontsize=7.2, loc='lower left', framealpha=0.96)
ax.set_title('Competing reduction paths at 600 $^{\\circ}$C', fontsize=10.5)
plt.tight_layout()
fig.savefig(os.path.join(FIG, 'fig_r3_competition.pdf'), bbox_inches='tight')
fig.savefig(os.path.join(EPS, 'figure_r3_competition.eps'), bbox_inches='tight')
fig.savefig(os.path.join(EPS, 'figure_r3_competition.png'), dpi=140, bbox_inches='tight')
print('saved fig_r3_competition')

# ==================================================== (B) two-channel scheme
fig2, ax2 = plt.subplots(figsize=(7.0, 5.0))
ax2.set_xlim(0, 100)
ax2.set_ylim(0, 100)
ax2.axis('off')

# electrode bar
ax2.add_patch(FancyBboxPatch((4, 91), 92, 7.5, boxstyle='round,pad=0.5,rounding_size=1.5',
                             fc='#e8f2e6', ec='#4a7a45', lw=1.0))
ax2.text(50, 94.7, 'cathode deposits liquid Mg--Ca   |   anode evolves O$_2$',
         ha='center', fontsize=7.8, color='#2f5b2c')

# melt
ax2.add_patch(FancyBboxPatch((2, 16), 96, 73, boxstyle='round,pad=0.5,rounding_size=2',
                             fc='#eef4fb', ec='#7f9dc0', lw=1.0))
ax2.text(50, 85.5, 'molten MgCl$_2$--CaCl$_2$--NaCl--KCl   (600 $^{\\circ}$C)',
         ha='center', fontsize=8.2, color='#33506e')

# regeneration arrows (left and right margins, clear of all text)
ax2.add_patch(FancyArrowPatch((12, 91), (12, 66), arrowstyle='-|>', mutation_scale=11,
                              lw=1.4, color='#2f7a45'))
ax2.add_patch(FancyArrowPatch((88, 91), (88, 66), arrowstyle='-|>', mutation_scale=11,
                              lw=1.4, color='#8c2f33'))
ax2.text(13.5, 78, 'regenerated\nMg and Ca', fontsize=6.9, color='#444444', ha='left')

# alloy pool
ax2.add_patch(FancyBboxPatch((16, 40), 68, 26, boxstyle='round,pad=0.5,rounding_size=2',
                             fc='#fdf3d8', ec='#c9a227', lw=1.2))
ax2.text(50, 63.0, 'liquid Mg--Ca alloy  (reductant)', ha='center', fontsize=8.0,
         color='#8a6d1b')

# particle
ax2.add_patch(Circle((50, 51), 8.0, fc='#d9d9d9', ec='#555555', lw=1.2))
ax2.text(50, 52.0, 'TiO$_2$', ha='center', fontsize=8.4, fontweight='bold')
ax2.text(50, 48.4, '(shrinking core)', ha='center', fontsize=6.4)
ax2.add_patch(Circle((50, 51), 11.0, fc='none', ec='#999999', lw=0.9, ls='--'))

# channel arrows
ax2.add_patch(FancyArrowPatch((32, 58), (42.5, 54.5), arrowstyle='-|>', mutation_scale=11,
                              lw=1.7, color='#55a868'))
ax2.add_patch(FancyArrowPatch((57.5, 54.5), (68, 58), arrowstyle='-|>', mutation_scale=11,
                              lw=1.7, color='#2f7a45'))
ax2.text(30, 60.5, 'Mg', fontsize=8.4, color='#2f7a45', fontweight='bold', ha='center')
ax2.text(70, 60.5, 'MgO', fontsize=8.4, color='#2f7a45', fontweight='bold', ha='center')

ax2.add_patch(FancyArrowPatch((29, 49), (41.8, 50), arrowstyle='-|>', mutation_scale=11,
                              lw=1.7, color='#c44e52'))
ax2.add_patch(FancyArrowPatch((58.2, 50), (71, 49), arrowstyle='-|>', mutation_scale=11,
                              lw=1.7, color='#8c2f33'))
ax2.text(22.5, 49, 'Ca', fontsize=8.4, color='#8c2f33', fontweight='bold', ha='center')
ax2.text(77.5, 49, 'CaO', fontsize=8.4, color='#8c2f33', fontweight='bold', ha='center')

# channel captions inside the pool, left and right of the particle
ax2.text(30, 43.0, 'channel 1\nfast, liquid Mg', fontsize=6.9, color='#2f7a45', ha='center')
ax2.text(70, 43.0, 'channel 2\ndeep deoxidation', fontsize=6.9, color='#8c2f33', ha='center')

# cross reaction box, in the melt below the alloy pool
ax2.add_patch(FancyBboxPatch((14, 22.5), 72, 13, boxstyle='round,pad=0.45,rounding_size=1.5',
                             fc='#e9eefb', ec='#4c72b0', lw=1.1))
ax2.text(50, 31.5, r'interface cross reaction:  Ca + MgO $\rightarrow$ CaO + Mg',
         ha='center', fontsize=7.6, color='#2f4c7a', fontweight='bold')
ax2.text(50, 26.0,
         r'$\Delta G^{\circ}$ = $-$38.2 kJ mol$^{-1}$,  $K$ = 194.  The kinetic competition between'
         '\n'
         r'MgO dissolution/regeneration and this reaction sets the channel split.',
         ha='center', fontsize=6.8, color='#2f4c7a', linespacing=1.6)

ax2.text(50, 9.5, 'Net reaction:  TiO$_2 \\rightarrow$ Ti + O$_2$   (Ca is the net oxygen carrier)',
         ha='center', fontsize=8.2, fontweight='bold')
ax2.text(50, 3.5, 'Mg makes the reductant liquid at 600 $^{\\circ}$C, where both pure metals are solid',
         ha='center', fontsize=7.2, color='#444444',
         bbox=dict(boxstyle='round,pad=0.3', fc='#f7f7f7', ec='0.8'))

plt.tight_layout()
fig2.savefig(os.path.join(FIG, 'fig_r3_shuttle.pdf'), bbox_inches='tight')
fig2.savefig(os.path.join(EPS, 'figure_r3_shuttle.eps'), bbox_inches='tight')
fig2.savefig(os.path.join(EPS, 'figure_r3_shuttle.png'), dpi=140, bbox_inches='tight')
print('saved fig_r3_shuttle')
