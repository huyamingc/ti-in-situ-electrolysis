# -*- coding: utf-8 -*-
"""Process flowsheet for the reconstructed manuscript (Reviewer 1, item 2).

Produces figures/fig_flowsheet.pdf, figures_eps/figure_flowsheet.eps and .png.
English labels only; material-flow numbers are the Case II design point with the
Case I values in brackets (Table 6 of the paper).
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG = os.path.join(ROOT, 'figures')
EPS = os.path.join(ROOT, 'figures_eps')
os.makedirs(FIG, exist_ok=True)
os.makedirs(EPS, exist_ok=True)

fig, ax = plt.subplots(figsize=(7.4, 5.6))
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

C_FEED = '#e8eef7'
C_CELL = '#e3f2e1'
C_PROD = '#fdeee0'
C_REC = '#f0e8f5'


def box(x, y, w, h, text, fc, fs=8.0, weight='normal', ec='#333333'):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle='round,pad=0.5,rounding_size=1.0',
                                linewidth=1.0, edgecolor=ec, facecolor=fc))
    ax.text(x + w / 2, y + h / 2, text, ha='center', va='center',
            fontsize=fs, fontweight=weight, linespacing=1.4)


def arrow(x1, y1, x2, y2, label=None, lx=0, ly=0, ha='center', va='center', fs=7.0):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle='-|>',
                                 mutation_scale=12, linewidth=1.0, color='#222222'))
    if label:
        ax.text((x1 + x2) / 2 + lx, (y1 + y2) / 2 + ly, label,
                ha=ha, va=va, fontsize=fs, color='#111111',
                bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='none', alpha=0.95))


# ---------------------------------------------------------------- feedstock
box(1.5, 79, 25, 14,
    r'$\bf{TiO_2}$ feedstock' + '\n'
    r'1668 kg per ton Ti' + '\n'
    r'metallurgical grade, $\geq$90 wt%' + '\n'
    r'(Fe, Si impurities)',
    C_FEED, 7.6)

# ---------------------------------------------------------------- cell
box(31, 60, 44, 33, '', C_CELL)
ax.text(53, 90.0, 'Electrolysis cell, 600 $^{\\circ}$C (sealed, dry Ar)',
        ha='center', va='center', fontsize=8.6, fontweight='bold')
ax.add_patch(Rectangle((33.6, 64.0), 38.8, 22.0, linewidth=0.9,
                       edgecolor='#4a7a45', facecolor='white', zorder=1))
ax.text(53, 84.2, 'quaternary chloride melt', ha='center', fontsize=7.4, style='italic')
ax.text(53, 81.9, r'$x_{\rm MgCl_2}$=0.30, $x_{\rm CaCl_2}$=0.40, $x_{\rm NaCl}$=$x_{\rm KCl}$=0.15',
        ha='center', fontsize=7.0)
ax.text(53, 79.6, r'(liquidus 544 $^{\circ}$C; fully molten at 600 $^{\circ}$C)',
        ha='center', fontsize=7.0)
ax.text(53, 76.6, r'cathode: liquid Mg--Ca alloy,  $j\approx$1.1 A/cm$^2$',
        ha='center', fontsize=7.2)
ax.text(53, 74.3, r'TiO$_2$ particles suspended in the melt', ha='center', fontsize=7.2)
ax.text(53, 71.6, r'anode: O$^{2-}\rightarrow\frac{1}{2}$O$_2$ + 2e$^-$  (inert or graphite)',
        ha='center', fontsize=7.2)
ax.text(53, 68.4, r'CaO / MgO dissolve and are regenerated', ha='center', fontsize=7.2)

# ---------------------------------------------------------------- O2 out
box(80, 80, 18.5, 12, r'$\bf{O_2}$' + '\n668 kg per ton Ti' + '\n(green by-product)',
    C_PROD, 7.6)
arrow(75, 86, 80, 86)

# ---------------------------------------------------------------- makeup salt
box(1.5, 60, 25, 14,
    r'$\bf{Makeup\ salt}$' + '\n'
    r'MgCl$_2$ / CaCl$_2$, vacuum-dried' + '\n'
    r'replaces Mg lost by evaporation' + '\n'
    r'($p_{\rm Mg}\approx$180 Pa at 600 $^{\circ}$C)',
    C_FEED, 7.4)
arrow(26.5, 67, 31, 70)

# ---------------------------------------------------------------- product recovery
box(31, 42, 47, 12,
    r'$\bf{Product\ recovery}$' + '\n'
    r'counter-current water wash $\rightarrow$ drying $\rightarrow$ screening' + '\n'
    r'entrained CaCl$_2$/MgCl$_2$ is water-soluble; the wash liquor is recycled',
    C_REC, 7.6)
arrow(53, 60, 53, 54, 'Ti powder +\nentrained salt\n(1.2--4.8 wt%)', lx=17.5, ly=0.0, fs=6.8)

# ---------------------------------------------------------------- outputs
box(34, 22, 20, 11, r'$\bf{Ti\ powder}$' + '\n1000 kg per ton Ti', C_PROD, 8.0)
arrow(44, 42, 44, 33)

box(61, 22, 25, 11,
    r'$\bf{Salt\ recovery}$' + '\n'
    r'evaporation / crystallisation' + '\n'
    r'$\rightarrow$ makeup salt returned to the cell',
    C_REC, 7.4)
arrow(72, 42, 74, 33)

# ---------------------------------------------------------------- salt recycle loop
ax.add_patch(FancyArrowPatch((86, 27.5), (94, 27.5), arrowstyle='-', linewidth=1.0,
                             color='#222222'))
ax.add_patch(FancyArrowPatch((94, 27.5), (94, 70), arrowstyle='-', linewidth=1.0,
                             color='#222222'))
arrow(94, 70, 75, 70)
ax.text(96.2, 49, 'recycled salt', rotation=90, ha='center', va='center', fontsize=7.0)

# ---------------------------------------------------------------- net reaction
box(1.5, 22, 29, 11,
    r'$\bf{Net\ reaction}$: TiO$_2 \rightarrow$ Ti + O$_2$' + '\n'
    r'1668 = 1000 + 668 kg per ton Ti' + '\n'
    r'Mg and Ca are cyclic mediators',
    '#f7f7f7', 7.4)

# ---------------------------------------------------------------- energy footer
ax.add_patch(FancyBboxPatch((1.5, 2.5), 97, 15,
                            boxstyle='round,pad=0.5,rounding_size=1.0',
                            linewidth=0.9, edgecolor='#999999', facecolor='#fbfbfb'))
ax.text(3.5, 14.0, 'Energy and cell parameters (per ton Ti; Case II with the CaO-only Case I in brackets)',
        fontsize=7.6, fontweight='bold', va='center')
ax.text(3.5, 8.6,
        'gross electrolysis 12 244 [12 625] kWh   |   net equivalent 12 552 [12 933] kWh   |   '
        'cell voltage 4.1 [4.23] V\n'
        r'$\eta_I$ = 0.75 (unvalidated)   |   interelectrode gap $L\lesssim$1.1 cm at $\kappa$ = 1.4 S/cm, $\delta \approx$ 200 $\mu$m   |   '
        r'current efficiency is the dominant uncertainty',
        fontsize=7.0, va='center', linespacing=1.7)

plt.tight_layout()
for path in (os.path.join(FIG, 'fig_flowsheet.pdf'),
             os.path.join(EPS, 'figure_flowsheet.eps'),
             os.path.join(EPS, 'figure_flowsheet.png')):
    fig.savefig(path, bbox_inches='tight', dpi=140)
    print('saved:', path)
