# -*- coding: utf-8 -*-
"""
supplement_calc.py — P0/P1 计算补充（无实验，纯案头）
生成：
  1. fig_overpotential_bv.pdf  — Butler-Volmer 活化过电位 + 有效共沉积窗口 vs 电流密度
  2. fig_cl2_boundary.pdf      — 析氯临界氧活度（参数化于氧酸度 E°）
  3. fig_voltage_split.pdf     — 槽电压构成拆分柱状图
并打印：盐循环最小流量、电压拆分明细、γ_CaCl2/溶解度敏感性
依赖：numpy, matplotlib
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

R = 8.314
F = 96485
T = 873.15  # 600 °C
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.join(SCRIPT_DIR, '..', 'figures')
os.makedirs(FIG_DIR, exist_ok=True)

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']
plt.rcParams['mathtext.fontset'] = 'stix'

# ============================================================
# P0-2: Butler-Volmer activation overpotential
# ============================================================
print("=" * 60)
print("P0-2: Butler-Volmer activation overpotential")
print("=" * 60)
alpha = 0.5
j0_Ca = 0.05   # A/cm2 (typical metal deposition, order-of-magnitude)
j0_Na = 0.03   # A/cm2 (Na+ more sluggish, order-of-magnitude)

def eta_act(j, j0, n):
    return (R * T / (alpha * n * F)) * np.arcsinh(j / (2.0 * j0))

j_grid = np.linspace(0.02, 2.0, 400)
eta_Ca = eta_act(j_grid, j0_Ca, 2)
eta_Na = eta_act(j_grid, j0_Na, 1)

# thermodynamic window (ideal) = 120 mV
win_thermo = 0.120  # V
win_eff = win_thermo + (eta_Na - eta_Ca)  # E_eff(Ca)-E_eff(Na) = thermo + (eta_Na - eta_Ca)

for j in [0.1, 0.5, 1.0, 2.0]:
    eC = eta_act(j, j0_Ca, 2) * 1000
    eN = eta_act(j, j0_Na, 1) * 1000
    we = (win_thermo + (eN - eC) / 1000) * 1000
    print(f"  j={j:4.1f} A/cm2: eta_Ca={eC:6.1f} mV, eta_Na={eN:6.1f} mV, "
          f"eta_Na-eta_Ca={eN-eC:6.1f} mV, effective window={we:6.1f} mV")

fig, ax = plt.subplots(figsize=(7, 5))
ax.plot(j_grid, eta_Ca * 1000, 'b-', lw=2, label=r'$\eta_{\mathrm{act}}$(Ca$^{2+}$), $n=2$, $j_0=0.05$ A/cm$^2$')
ax.plot(j_grid, eta_Na * 1000, 'r-', lw=2, label=r'$\eta_{\mathrm{act}}$(Na$^{+}$), $n=1$, $j_0=0.03$ A/cm$^2$')
ax.plot(j_grid, (eta_Na - eta_Ca) * 1000, 'k--', lw=1.5, label=r'$\eta_{\mathrm{Na}}-\eta_{\mathrm{Ca}}$ (window enlargement)')
ax.set_xlabel(r'Current density $j$ (A/cm$^2$)')
ax.set_ylabel('Overpotential (mV)')
ax.set_title('Butler-Volmer Activation Overpotential vs Current Density\n(600 °C, $\\alpha=0.5$, order-of-magnitude $j_0$)')
ax.legend(loc='upper left', fontsize=9)
ax.grid(True, alpha=0.3)
ax.set_xlim(0, 2.0)
fig.tight_layout()
fig.savefig(os.path.join(FIG_DIR, 'fig_overpotential_bv.pdf'), bbox_inches='tight')
plt.close()
print("Saved: fig_overpotential_bv.pdf")

# ============================================================
# P0-3: Cl2 evolution boundary (parametric in oxoacidity E°)
# ============================================================
print("\n" + "=" * 60)
print("P0-3: Cl2 evolution critical a(O2-) vs oxoacidity E°")
print("=" * 60)
# Critical condition: E°(O2/O2- vs Cl2/Cl-) - (RT/2F) ln a(O2-) = 0
#  => a(O2-)_crit = exp(2F E° / (RT))
E_deg = np.linspace(-0.8, 0.0, 400)  # oxoacidity (V), unknown for this melt
loga_crit = 2.0 * F * E_deg / (R * T * np.log(10))  # log10(a_crit)

# estimated actual free-oxide activity from MgO/CaO solubility (~1 wt% -> x(O2-)~1e-2,
# reduced by Ca2+-O2- complexation by ~1-2 orders of magnitude)
a_actual_lo = 1e-4   # log10 = -4
a_actual_hi = 1e-3   # log10 = -3

# crossing: a_crit = a_actual_lo (=1e-4)  =>  E° = (RT/2F) ln(1e-4)
E_cross_lo = (R * T / (2 * F)) * np.log(a_actual_lo)
E_cross_hi = (R * T / (2 * F)) * np.log(a_actual_hi)
print(f"  a(O2-)_crit = exp(2F E°/(RT))  [E° = oxoacidity vs Cl2/Cl-]")
print(f"  actual free a(O2-) estimate: {a_actual_lo:.0e} - {a_actual_hi:.0e}  (log10 -4 to -3)")
print(f"  crossing a_crit=1e-4 at E° = {E_cross_lo:.3f} V")
print(f"  crossing a_crit=1e-3 at E° = {E_cross_hi:.3f} V")

fig, ax = plt.subplots(figsize=(7, 5))
ax.plot(E_deg, loga_crit, 'b-', lw=2, label=r'$\log_{10} a_{\mathrm{O^{2-}},crit}$')
ax.axhspan(-4, -3, alpha=0.15, color='green', label='estimated free $a_{O^{2-}}$ (solubility-limited)')
ax.axvline(E_cross_lo, color='r', linestyle='--', lw=1.2, label=f'E° = {E_cross_lo:.2f} V (a_crit = 1e-4)')
ax.set_xlabel(r'Oxoacidity $E^{\circ}(\mathrm{O_2/O^{2-}}$ vs $\mathrm{Cl_2/Cl^-})$ (V)')
ax.set_ylabel(r'$\log_{10} a_{\mathrm{O^{2-}},crit}$')
ax.set_title(r'Anode $\mathrm{O_2}$/$\mathrm{Cl_2}$ Selectivity Boundary (600 °C)')
# annotate safe/risk regions
ax.text(-0.72, -1.3, 'O$_2$ evolution SAFE\n(actual $a_{O^{2-}}$ above critical)', fontsize=9, color='green')
ax.text(-0.22, -6.6, 'Cl$_2$ evolution RISK\n(actual $a_{O^{2-}}$ below critical)', fontsize=9, color='red')
ax.legend(loc='lower left', fontsize=9)
ax.grid(True, alpha=0.3)
ax.set_xlim(-0.8, 0.0)
ax.set_ylim(-8, 0)
fig.tight_layout()
fig.savefig(os.path.join(FIG_DIR, 'fig_cl2_boundary.pdf'), bbox_inches='tight')
plt.close()
print("Saved: fig_cl2_boundary.pdf")

# ============================================================
# P1-5: Cell voltage decomposition
# ============================================================
print("\n" + "=" * 60)
print("P1-5: Cell voltage decomposition (V_cell = E_decomp + eta + IR)")
print("=" * 60)
E_decomp = 2.729  # theoretical (MgO+CaO -> Mg+Ca+O2, 4e-, 873 K)
j_op = 0.5        # A/cm2
eta_anode = 0.30  # O2 evolution overpotential (order-of-magnitude)
eta_cathode = 0.20  # Mg/Ca deposition overpotential (order-of-magnitude)
IR_ohm = 0.90     # ohmic drop (melt conductivity + contact + busbar), order-of-magnitude
V_cell = E_decomp + eta_anode + eta_cathode + IR_ohm
print(f"  E_decomp   = {E_decomp:.2f} V")
print(f"  eta_anode  = {eta_anode:.2f} V (O2 evolution)")
print(f"  eta_cathode= {eta_cathode:.2f} V (Mg/Ca deposition)")
print(f"  IR_ohmic   = {IR_ohm:.2f} V")
print(f"  V_cell     = {V_cell:.2f} V  (~4.1 V assumed in energy balance)")

fig, ax = plt.subplots(figsize=(6, 4.5))
labels = [r'$E_{\mathrm{decomp}}$', r'$\eta_{\mathrm{anode}}$', r'$\eta_{\mathrm{cathode}}$', r'$IR_{\mathrm{ohm}}$']
vals = [E_decomp, eta_anode, eta_cathode, IR_ohm]
colors = ['#2196F3', '#FF9800', '#FF9800', '#9E9E9E']
bars = ax.bar(labels, vals, color=colors, edgecolor='black', linewidth=0.5)
for b, v in zip(bars, vals):
    ax.text(b.get_x() + b.get_width()/2, v + 0.05, f'{v:.2f}', ha='center', va='bottom', fontsize=10, fontweight='bold')
ax.set_ylabel('Voltage contribution (V)')
ax.set_title('Cell Voltage Decomposition (600 °C, order-of-magnitude)')
ax.set_ylim(0, 3.2)
ax.grid(True, alpha=0.3, axis='y')
fig.tight_layout()
fig.savefig(os.path.join(FIG_DIR, 'fig_voltage_split.pdf'), bbox_inches='tight')
plt.close()
print("Saved: fig_voltage_split.pdf")

# ============================================================
# P1-7: Minimum salt circulation
# ============================================================
print("\n" + "=" * 60)
print("P1-7: Minimum salt circulation (per ton Ti)")
print("=" * 60)
m_CaO = 1171  # kg CaO per ton Ti (from material balance)
m_MgO = 842   # kg MgO per ton Ti
for sol in [0.5, 1.0, 1.2]:  # wt% oxide solubility at 600 °C (extrapolated)
    m_salt_CaO = m_CaO / (sol / 100.0)  # kg salt to hold CaO
    m_salt_MgO = m_MgO / (sol / 100.0)
    print(f"  solubility={sol:4.1f} wt%: salt for CaO = {m_salt_CaO/1000:6.1f} t, "
          f"for MgO = {m_salt_MgO/1000:6.1f} t (per ton Ti)")
print(f"  => combined (MgO+CaO) at 1.0 wt%: {(m_CaO+m_MgO)/0.01/1000:.0f} t salt per ton Ti")

# ============================================================
# P0-4: gamma_CaCl2 + solubility sensitivity (tornado-style numbers)
# ============================================================
print("\n" + "=" * 60)
print("P0-4: gamma_CaCl2 + solubility sensitivity")
print("=" * 60)
# gamma_CaCl2 effect on window: already in Table tab:window_sens (74.9-147.1 mV)
# solubility effect on circulation: factor 2-4x (0.5-1.2 vs 2.35 wt%)
print("  gamma_CaCl2 (0.3-1.0) -> window 74.9-147.1 mV (Table tab:window_sens)")
print("  solubility (0.5-1.2 wt%) -> circulation 2.0-4.7x of 800 °C baseline (2.35 wt%)")
for sol in [0.5, 1.2, 2.35]:
    print(f"    sol={sol:4.1f} wt% -> circulation factor = {2.35/sol:.2f}x")

print("\nDONE")
