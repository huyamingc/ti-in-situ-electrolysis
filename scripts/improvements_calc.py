# -*- coding: utf-8 -*-
"""
双金属协同还原制钛工艺 — V2改进计算（6大模块，合并修正版）

用途：
  执行6项无需实验的理论计算改进，生成6张论文图表+控制台数据。
  所有数据来自文献，无需实验室。
  本脚本已合并 fix_calc.py 的全部修正，一次运行即生成正确结果。

依赖：
  Python 3.8+
  pip install numpy matplotlib

运行方式：
  python scripts/improvements_calc.py

输出：
  1. 控制台打印全部6个模块的计算结果
  2. 生成6张PDF矢量图到 figures/ 目录：
     - fig_scm_conversion.pdf     — 缩核模型转化率曲线（Module 1）
     - fig_scm_time_vs_size.pdf   — 还原时间vs粒径曲线（Module 1）
     - fig_scm_sensitivity.pdf    — 扩散系数敏感性分析图（Module 1）
     - fig_liquidus.pdf           — 四元熔盐液相线投影图（Module 3）
     - fig_E_pO2.pdf              — E-pO²⁻稳定性图（Module 4，修正符号）
     - fig_energy_sensitivity.pdf — 能耗敏感性等高线图（Module 2，英文标签）

模块说明：
  Module 1: Shrinking Core Model 动力学预测 → 3张图（含扩散系数敏感性）
  Module 2: 能耗敏感性分析（η_I vs V_cell）→ 1张图
  Module 3: 四元熔盐液相线估算 → 1张图
  Module 4: E-pO²⁻ 热力学稳定性图 → 1张图
  Module 5: 全流程热平衡与㶲分析 → 控制台输出（对应论文表 tab:heatbal）
  Module 6: TiCl4精馏最小分离功 → 控制台输出（对应论文 5.2.3节）
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import cm
import os

# ============================================================
# Constants & paths
# ============================================================
R = 8.314
F = 96485
T = 873.15  # 600°C

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', 'figures')
os.makedirs(OUTPUT_DIR, exist_ok=True)

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 9
plt.rcParams['figure.dpi'] = 300

n_Ti_per_ton = 1e6 / 47.867

# ============================================================
# Module 1: Shrinking Core Model (SCM) Kinetics
# ============================================================
print("=" * 60)
print("Module 1: Shrinking Core Model Kinetics")
print("=" * 60)

# Literature: D(O²⁻) in CaCl2-based melt at 600°C
# Schwartz & Fray (2005): ~1.2e-9 m²/s at 850°C
# Yan & Fray (2010): ~2.5e-9 m²/s at 600-700°C
# Nernst-Einstein estimate: ~1-3e-9 m²/s
# Conservative middle value:
D_O2 = 2.0e-9  # m²/s
rho_TiO2 = 4230  # kg/m³
M_TiO2 = 79.87   # g/mol
c_O_in_TiO2 = (rho_TiO2 / (M_TiO2 / 1000)) * 2  # mol/m³
rho_melt = 1800  # kg/m³
M_melt_avg = 0.085  # kg/mol
c_reductant = 0.03 * (rho_melt / M_melt_avg)  # 3 mol%

porosity = 0.3
tortuosity = 3.0
D_eff = D_O2 * porosity / tortuosity  # m²/s

particle_sizes_um = [10, 25, 50, 75, 100, 150, 200]  # diameters in μm
t_complete = []
for s_um in particle_sizes_um:
    r = (s_um / 2) * 1e-6  # R = radius = diameter / 2
    t_c = c_O_in_TiO2 * r**2 / (6 * D_eff * c_reductant)
    t_complete.append(t_c / 60)

print(f"D = {D_O2:.1e} m²/s, D_eff = {D_eff:.1e} m²/s (rate-limiting species: O²⁻ outward or Mg/Ca inward, TBD)")
print(f"\nParticle (μm) | Complete time (min)")
for s, t in zip(particle_sizes_um, t_complete):
    print(f"  {s:>4d}          |   {t:>8.1f}")

# --- Plot 1a: Conversion vs Time ---
fig, ax = plt.subplots(figsize=(6, 4.5))
X = np.linspace(0, 0.99, 200)
colors = cm.viridis(np.linspace(0.1, 0.9, len(particle_sizes_um)))
for i, (s_um, t_c_min) in enumerate(zip(particle_sizes_um, t_complete)):
    t_frac = 1 - 3*(1-X)**(2/3) + 2*(1-X)
    ax.plot(t_frac * t_c_min, X, color=colors[i], linewidth=1.5, label=f'{s_um} μm')
ax.set_xlabel('Time (min)')
ax.set_ylabel('Conversion X')
ax.set_title('Shrinking Core Model: Reduction Conversion vs Time\n(600°C, D=2.0×10$^{-9}$ m²/s)')
ax.legend(loc='lower right', ncol=2, fontsize=8)
ax.set_xlim(0, max(t_complete) * 1.05)
ax.set_ylim(0, 1.0)
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, 'fig_scm_conversion.pdf'), bbox_inches='tight')
plt.close()
print(f"Saved: fig_scm_conversion.pdf")

# --- Plot 1b: Time vs Size ---
fig, ax = plt.subplots(figsize=(6, 4.5))
sizes_fine = np.linspace(5, 250, 200)
t_fine = [c_O_in_TiO2 * ((s/2)*1e-6)**2 / (6 * D_eff * c_reductant) / 60 for s in sizes_fine]
ax.plot(sizes_fine, t_fine, 'b-', linewidth=2)
ax.axhline(y=30, color='r', linestyle='--', alpha=0.7, label='30 min (target)')
ax.axhline(y=60, color='orange', linestyle='--', alpha=0.7, label='60 min (acceptable)')
for s_um, t_c in zip(particle_sizes_um, t_complete):
    ax.plot(s_um, t_c, 'ro', markersize=5)
    ax.annotate(f'{t_c:.1f}min', (s_um, t_c), textcoords="offset points", xytext=(5, 5), fontsize=7)
ax.set_xlabel('Particle diameter (μm)')
ax.set_ylabel('Complete reduction time (min)')
ax.set_title('Complete Reduction Time vs Particle Size\n(Diffusion-controlled SCM, 600°C)')
ax.legend()
ax.grid(True, alpha=0.3)
ax.set_xlim(0, 250)
fig.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, 'fig_scm_time_vs_size.pdf'), bbox_inches='tight')
plt.close()
print(f"Saved: fig_scm_time_vs_size.pdf")

# --- Plot 1c: D_eff sensitivity ---
D_list = [1.0e-9, 1.5e-9, 2.0e-9, 2.5e-9, 3.0e-9]
D_labels = ['1.0', '1.5', '2.0', '2.5', '3.0']
sizes_sens = np.linspace(5, 250, 200)

fig, ax = plt.subplots(figsize=(7, 5))
colors_D = cm.viridis(np.linspace(0.1, 0.9, len(D_list)))
for i, D_val in enumerate(D_list):
    D_eff_sens = D_val * porosity / tortuosity
    t_sens = [c_O_in_TiO2 * ((s/2)*1e-6)**2 / (6 * D_eff_sens * c_reductant) / 60 for s in sizes_sens]
    ax.plot(sizes_sens, t_sens, color=colors_D[i], linewidth=1.5, 
            label=f'D = {D_labels[i]}×10$^{{-9}}$ m$^2$/s')
    # Mark 100 μm diameter point (R = 50 μm)
    t100 = c_O_in_TiO2 * (50e-6)**2 / (6 * D_eff_sens * c_reductant) / 60
    ax.plot(100, t100, 'o', color=colors_D[i], markersize=5)

ax.axhspan(3.9, 11.6, alpha=0.1, color='green', label='Range for 100 μm (3.9–11.6 min)')
ax.axhline(y=30, color='r', linestyle='--', alpha=0.5, linewidth=1)
ax.set_xlabel('Particle diameter (μm)')
ax.set_ylabel('Complete reduction time (min)')
ax.set_title('SCM Sensitivity: Reduction Time vs D\n(600°C, porosity=0.3, tortuosity=3.0)')
ax.legend(loc='upper left', fontsize=8)
ax.grid(True, alpha=0.3)
ax.set_xlim(0, 250)
ax.set_ylim(0, 40)
fig.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, 'fig_scm_sensitivity.pdf'), bbox_inches='tight')
plt.close()
print(f"Saved: fig_scm_sensitivity.pdf")

print(f"\n  D (m²/s)    | D_eff (m²/s)   | t_complete(100μm diam, R=50μm) =")
for D_val in D_list:
    D_eff_sens = D_val * porosity / tortuosity
    t100 = c_O_in_TiO2 * (50e-6)**2 / (6 * D_eff_sens * c_reductant) / 60
    print(f"  {D_val:.1e}   | {D_eff_sens:.1e}   | {t100:.1f} min")

# ============================================================
# Module 2: Energy Sensitivity Analysis
# ============================================================
print("\n" + "=" * 60)
print("Module 2: Energy Sensitivity Analysis")
print("=" * 60)

eta_range = np.linspace(0.60, 0.90, 100)
Vcell_range = np.linspace(3.5, 5.0, 100)
ETA, VCELL = np.meshgrid(eta_range, Vcell_range)
W = 4 * F * n_Ti_per_ton * VCELL / (ETA * 3.6e6)  # kWh/ton Ti

fig, ax = plt.subplots(figsize=(7, 5.5))
levels = np.arange(6000, 20000, 500)
cs = ax.contourf(ETA * 100, VCELL, W, levels=levels, cmap='YlOrRd_r', extend='both')
cs2 = ax.contour(ETA * 100, VCELL, W, levels=[6112], colors='blue',
                 linewidths=2.5, linestyles='--')
ax.clabel(cs2, fmt={6112: 'Theoretical min (6112)'}, fontsize=9, colors='blue')
cs3 = ax.contour(ETA * 100, VCELL, W, levels=[10000, 12000, 15000],
                 colors=['navy','blue','royalblue'], linewidths=1.2, linestyles=':')
ax.clabel(cs3, fmt='%d', fontsize=8, colors='blue')
ax.plot(75, 4.0, 'w*', markersize=15, markeredgecolor='black', markeredgewidth=1,
        label='Recommended ($\\eta$=75%, V=4.0V)')
ax.plot(80, 4.0, 'w^', markersize=10, markeredgecolor='black', markeredgewidth=1,
        label='Optimistic ($\\eta$=80%, V=4.0V)')
cbar = fig.colorbar(cs, ax=ax, label='Energy consumption (kWh/ton Ti)')
ax.set_xlabel('Current efficiency $\\eta_I$ (%)')
ax.set_ylabel('Cell voltage $V_{cell}$ (V)')
ax.set_title('Energy Sensitivity: $\\eta_I$ vs $V_{cell}$\n(Dashed blue = theoretical minimum 6112 kWh/ton)')
ax.legend(loc='upper right', fontsize=8)
fig.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, 'fig_energy_sensitivity.pdf'), bbox_inches='tight')
plt.close()
print(f"Saved: fig_energy_sensitivity.pdf")

print(f"\nMinimum η_I for W < 12000 kWh/ton:")
for v in [3.5, 4.0, 4.5, 5.0]:
    eta_min = 4 * F * n_Ti_per_ton * v / (12000 * 3.6e6)
    print(f"  V={v}V: η_min = {eta_min*100:.1f}%")

# ============================================================
# Module 3: Quaternary Salt Liquidus
# ============================================================
print("\n" + "=" * 60)
print("Module 3: Quaternary Salt Liquidus Estimation")
print("=" * 60)

components = {
    'MgCl2': {'Tm': 987, 'dHfus': 43100},
    'CaCl2': {'Tm': 1045, 'dHfus': 28500},
    'NaCl':  {'Tm': 1074, 'dHfus': 28200},
    'KCl':   {'Tm': 1043, 'dHfus': 26600},
}

def liquidus_temp_ideal(x_dict, T_range):
    for T in T_range:
        all_liquid = True
        for comp, data in components.items():
            x = x_dict.get(comp, 0)
            if x < 1e-10:
                continue
            x_sat = np.exp(-data['dHfus'] / R * (1/T - 1/data['Tm']))
            if x > x_sat:
                all_liquid = False
                break
        if all_liquid:
            return T
    return T_range[0]

T_scan = np.arange(700, 1100, 1)

fig, ax = plt.subplots(figsize=(7, 5.5))
x_Mg_arr = np.linspace(0.10, 0.50, 80)
x_Ca_arr = np.linspace(0.15, 0.55, 80)
XM, XC = np.meshgrid(x_Mg_arr, x_Ca_arr)
T_liq_grid = np.zeros_like(XM)

for i in range(len(x_Ca_arr)):
    for j in range(len(x_Mg_arr)):
        xm = XM[i, j]; xc = XC[i, j]; xk = 0.15
        xn = 1.0 - xm - xc - xk
        if xn < 0.02 or xn > 0.40:
            T_liq_grid[i, j] = np.nan
            continue
        T_liq_grid[i, j] = liquidus_temp_ideal(
            {'MgCl2': xm, 'CaCl2': xc, 'NaCl': xn, 'KCl': xk}, T_scan)

T_liq_C = T_liq_grid - 273.15
levels_T = np.arange(450, 650, 25)
cs = ax.contourf(XM, XC, T_liq_C, levels=levels_T, cmap='YlOrRd_r')
cs2 = ax.contour(XM, XC, T_liq_C, levels=[500, 550, 600, 650], colors='black', linewidths=0.8)
ax.clabel(cs2, fmt='%d°C', fontsize=8)
cbar = fig.colorbar(cs, ax=ax, label='Liquidus temperature (°C)')
ax.plot(0.30, 0.40, 'w*', markersize=15, markeredgecolor='black', markeredgewidth=1,
        label='Recommended\n(x_MgCl₂=0.30, x_CaCl₂=0.40)')
ax.plot(0.35, 0.45, 'w^', markersize=10, markeredgecolor='black', markeredgewidth=1,
        label='Low-Na/K option')
ax.contour(XM, XC, T_liq_C, levels=[550], colors='blue', linewidths=2, linestyles='--')
ax.set_xlabel('x$_{MgCl_2}$ (mol fraction)')
ax.set_ylabel('x$_{CaCl_2}$ (mol fraction)')
ax.set_title('Quaternary Liquidus Projection (x$_{KCl}$=0.15)\nIdeal Solution Model')
ax.legend(loc='upper left', fontsize=8)
fig.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, 'fig_liquidus.pdf'), bbox_inches='tight')
plt.close()
print(f"Saved: fig_liquidus.pdf")

for comp_name, x_dict in [
    ('Equal (0.25/0.25/0.25/0.25)', {'MgCl2': 0.25, 'CaCl2': 0.25, 'NaCl': 0.25, 'KCl': 0.25}),
    ('Recommended (0.30/0.40/0.15/0.15)', {'MgCl2': 0.30, 'CaCl2': 0.40, 'NaCl': 0.15, 'KCl': 0.15}),
    ('Low-Na/K (0.35/0.45/0.10/0.10)', {'MgCl2': 0.35, 'CaCl2': 0.45, 'NaCl': 0.10, 'KCl': 0.10}),
]:
    T_l = liquidus_temp_ideal(x_dict, T_scan) - 273.15
    print(f"  {comp_name}: T_liq = {T_l:.0f}°C")

# ============================================================
# Module 4: E-pO²⁻ Diagram (CORRECTED — E_red negative)
# ============================================================
print("\n" + "=" * 60)
print("Module 4: E-pO²⁻ Thermodynamic Stability Diagram")
print("=" * 60)

# ΔG°f at 873K (J/mol) from Barin/literature
dG_f = {
    'TiO2': -748000, 'Fe2O3': -528000, 'SiO2': -680000,
    'Al2O3': -1350000, 'MgO': -506000, 'CaO': -544000,
}
n_elec = {'TiO2': 4, 'Fe2O3': 6, 'SiO2': 4, 'Al2O3': 6, 'MgO': 2, 'CaO': 2}

# E_red = ΔG°f / (n·F) — NEGATIVE (reduction potential vs O₂/O²⁻ standard state)
E0_red = {ox: dG_f[ox] / (n_elec[ox] * F) for ox in dG_f}
slope = R * T / (2 * F) * np.log(10)  # 86.6 mV per pO²⁻ unit

print(f"Nernst slope = {slope*1000:.1f} mV per pO²⁻ unit")
for ox in ['Fe2O3', 'SiO2', 'TiO2', 'Al2O3', 'MgO', 'CaO']:
    print(f"  {ox}: E_red = {E0_red[ox]:.3f} V")

pO2_range = np.linspace(0, 20, 200)
fig, ax = plt.subplots(figsize=(7, 6))

colors_lines = {'TiO2': 'blue', 'Fe2O3': 'red', 'SiO2': 'green',
                'Al2O3': 'orange', 'MgO': 'purple', 'CaO': 'brown'}
labels_lines = {'TiO2': r'TiO$_2$/Ti', 'Fe2O3': r'Fe$_2$O$_3$/Fe',
                'SiO2': r'SiO$_2$/Si', 'Al2O3': r'Al$_2$O$_3$/Al',
                'MgO': 'MgO/Mg', 'CaO': 'CaO/Ca'}

for ox in ['Fe2O3', 'SiO2', 'TiO2', 'Al2O3', 'MgO', 'CaO']:
    ax.plot(pO2_range, E0_red[ox] + slope * pO2_range,
            color=colors_lines[ox], linewidth=1.8, label=labels_lines[ox])

ax.axvspan(2, 8, alpha=0.08, color='green')
ax.axhspan(-3.5, -2.5, alpha=0.05, color='blue')
ax.plot(4, -3.0, 'k*', markersize=15, markeredgecolor='black', zorder=5, label='Operating point')
ax.annotate('Fe, Si impurities reduced\nBEFORE Ti (less negative E)\n→ preferential separation',
            xy=(6, -1.3), fontsize=8, color='darkred',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow', alpha=0.9))
ax.annotate('Ti reduction zone\n(E < TiO$_2$/Ti line)',
            xy=(12, -2.5), fontsize=8, color='blue',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='lightblue', alpha=0.5))
ax.annotate('Note: Lines based on pure oxide\nstandard states. In real molten salt,\nabsolute values shift but relative\norder is preserved.',
            xy=(1, -3.7), fontsize=7, color='gray',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow', alpha=0.7))
ax.set_xlabel(r'pO$^{2-}$ = $-$log(a$_{O^{2-}}$)')
ax.set_ylabel(r'E (V vs O$_2$/O$^{2-}$)')
ax.set_title('E–pO$^{2-}$ Stability Diagram at 600°C\n(M/MO Equilibrium Lines)')
ax.legend(loc='lower right', fontsize=8, ncol=2)
ax.set_xlim(0, 20)
ax.set_ylim(-4.0, 0.5)
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, 'fig_E_pO2.pdf'), bbox_inches='tight')
plt.close()
print(f"Saved: fig_E_pO2.pdf")

# ============================================================
# Module 5: Full Process Exergy Analysis
# ============================================================
print("\n" + "=" * 60)
print("Module 5: Full Process Exergy (Heat) Balance")
print("=" * 60)

Cp_TiO2 = 55; n_TiO2 = n_Ti_per_ton
Q_preheat_TiO2 = n_TiO2 * Cp_TiO2 * (600 - 25) / 3.6e6  # kWh/ton-Ti; Cp from Barin (1995)
Q_preheat_salt = (50 / 0.085) * 80 * (600 - 25) / 3.6e6  # kWh/ton-Ti; 50 kg salt makeup, Cp_salt~80 J/(mol·K)
W_electrolysis = 10554  # kWh/ton-Ti; net equivalent electrolysis input (see Table tab:heatbal)
A_cell = np.pi * 3.0 * 4.0 + 2 * np.pi * 1.5**2  # m²; cell surface area (3m dia × 4m height + 2 ends)
Q_loss_rate = 0.15 * A_cell * (600 - 80) / 0.3  # W; conductive heat loss, k=0.15 W/(m·K), insulation thickness 0.3m
Q_loss_kWh = Q_loss_rate * 10.23 / 1000  # kWh/ton-Ti; 10.23 h batch time
Q_reaction = -1690  # kWh/ton-Ti; exothermic, from ΔH° = -291.3 kJ/mol-Ti (Table tab:thermo, combined R1+R2)
Q_cool_Ti = n_Ti_per_ton * 25 * (600 - 25) / 3.6e6  # kWh/ton-Ti; Cp_Ti ≈ 25 J/(mol·K)
Q_pumping = 50  # kWh/ton-Ti; salt circulation pumping (estimated, ref: Pletcher & Walsh 1990)
Q_post = 300  # kWh/ton-Ti; post-treatment (salt washing/drying/screening); impurity acid-leaching is excluded (see Limitations (7))

Q_input = W_electrolysis + Q_preheat_TiO2 + Q_preheat_salt + Q_loss_kWh + Q_pumping + Q_post
W_net = Q_input - Q_cool_Ti * 0.5
exergy_eff = W_electrolysis / Q_input * 100
W_min = 6112  # theoretical minimum kWh/ton
thermo_eff = W_min / W_net * 100

print(f"INPUT:")
print(f"  Electrolysis:      {W_electrolysis:>8.0f} kWh ({W_electrolysis/Q_input*100:.1f}%)")
print(f"  TiO2 preheating:   {Q_preheat_TiO2:>8.0f} kWh ({Q_preheat_TiO2/Q_input*100:.1f}%)")
print(f"  Salt makeup:       {Q_preheat_salt:>8.1f} kWh ({Q_preheat_salt/Q_input*100:.1f}%)")
print(f"  Cell heat loss:    {Q_loss_kWh:>8.0f} kWh ({Q_loss_kWh/Q_input*100:.1f}%)")
print(f"  Pumping:           {Q_pumping:>8.0f} kWh ({Q_pumping/Q_input*100:.1f}%)")
print(f"  Post-treatment:    {Q_post:>8.0f} kWh ({Q_post/Q_input*100:.1f}%)")
print(f"  Total input:       {Q_input:>8.0f} kWh")
print(f"CREDITS:")
print(f"  Reaction heat:     {abs(Q_reaction):>8.0f} kWh (offsets heat loss)")
print(f"  Ti cooling (50%):  {Q_cool_Ti*0.5:>8.0f} kWh (recoverable)")
print(f"NET energy:          {W_net:>8.0f} kWh/ton")
print(f"Thermodynamic efficiency (W_min/W_net): {thermo_eff:.1f}%")
print(f"Electrolysis utilization ratio (W_elec/W_total): {exergy_eff:.1f}%")

# ============================================================
# Module 6: Minimum Separation Work (CORRECTED formula)
# ============================================================
print("\n" + "=" * 60)
print("Module 6: Minimum Separation Work for TiCl4 Purification")
print("=" * 60)

T_distill = 409.15  # K (TiCl4 bp = 136°C)
x_Af, x_Bf = 0.90, 0.10  # Feed
x_Ap, x_Bp = 0.999, 0.001  # Product

n_TiCl4_feed = 0.90
n_TiCl4_prod = 0.90 * 0.99  # 99% recovery
n_prod = n_TiCl4_prod / 0.999
n_waste = 1.0 - n_prod
n_TiCl4_waste = n_TiCl4_feed - n_TiCl4_prod
x_Aw = n_TiCl4_waste / n_waste
x_Bw = 1 - x_Aw

# W_min = RT * Σ_out n_k * Σ_i x_i * ln(x_i / x_feed_i)
term_prod = n_prod * (x_Ap * np.log(x_Ap / x_Af) + x_Bp * np.log(x_Bp / x_Bf))
term_waste = n_waste * (x_Aw * np.log(x_Aw / x_Af) + x_Bw * np.log(x_Bw / x_Bf))
W_min_per_mol = R * T_distill * (term_prod + term_waste)
W_min_kWh = W_min_per_mol * n_Ti_per_ton / 3.6e6

actual_distill = 300  # kWh/ton Ti (literature)
second_law_eff = W_min_kWh / actual_distill * 100

print(f"Feed: {1.0:.4f} mol, x_TiCl4 = {x_Af}")
print(f"Product: {n_prod:.4f} mol, x_TiCl4 = {x_Ap}")
print(f"Waste: {n_waste:.4f} mol, x_TiCl4 = {x_Aw:.4f}")
print(f"\nW_min = {W_min_per_mol:.1f} J/mol = {W_min_per_mol/1000:.3f} kJ/mol")
print(f"W_min = {W_min_kWh:.2f} kWh/ton Ti")
print(f"Actual distillation: ~{actual_distill} kWh/ton Ti")
print(f"Second-law efficiency: {second_law_eff:.2f}%")

print(f"\nW_min for different purification levels:")
for x_target in [0.95, 0.99, 0.999, 0.9999]:
    x_p = x_target; x_bp = 1 - x_target
    n_tp = 0.90 * 0.99; n_p = n_tp / x_p; n_w = 1 - n_p
    n_tw = 0.90 - n_tp; x_aw = n_tw / n_w if n_w > 0 else 0; x_bw = 1 - x_aw
    if x_aw > 0 and x_bw > 0 and x_bp > 0:
        tp = n_p * (x_p * np.log(x_p / x_Af) + x_bp * np.log(x_bp / x_Bf))
        tw = n_w * (x_aw * np.log(x_aw / x_Af) + x_bw * np.log(x_bw / x_Bf))
        w = R * T_distill * (tp + tw) * n_Ti_per_ton / 3.6e6
        print(f"  {x_target*100:.2f}%: W_min = {w:.2f} kWh/ton Ti")

our_total = 12638
print(f"\nComparison:")
print(f"  Kroll TiCl4 distillation (actual): {actual_distill} kWh/ton Ti")
print(f"  Kroll TiCl4 distillation (min):    {W_min_kWh:.2f} kWh/ton Ti")
print(f"  Our process total electrical:      {our_total} kWh/ton Ti")
print(f"  Kroll distillation / Our total:    {actual_distill/our_total*100:.1f}%")
print(f"  Second-law efficiency:             {second_law_eff:.2f}%")

print("\n" + "=" * 60)
print("DONE — All 6 modules computed, 6 figures saved.")
print("=" * 60)
