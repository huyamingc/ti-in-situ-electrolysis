#!/usr/bin/env python3
"""
monte_carlo_uncertainty.py
==========================
全局不确定性分析（蒙特卡洛模拟）

对论文中两个核心输出量进行全局不确定性传播分析：
1. SCM还原时间 (t_complete)
2. 全流程净能耗 (W_net)

参数分布基于论文中声明的范围，同时抽样所有参数，
输出概率分布图和统计量。

依赖：numpy, matplotlib, scipy
运行方式：python scripts/monte_carlo_uncertainty.py
输出：figures/ 目录下2张PDF图 + output/ 目录下1个CSV
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats
import csv
import os

# ============================================================
# 常数
# ============================================================
F = 96485          # C/mol
R = 8.314          # J/(mol·K)
M_Ti = 47.867      # g/mol
n_Ti = 1e6 / M_Ti  # mol Ti per ton = 20891.2

# SCM固定参数
c_O = 1.06e5       # mol/m³ (oxygen in TiO2)
c_red = 635         # mol/m³ (reductant concentration)
R_particle = 50e-6  # m (100 μm diameter particle, R=50μm)

# 输出目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', 'output')
FIGURE_DIR = os.path.join(SCRIPT_DIR, '..', 'figures')
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(FIGURE_DIR, exist_ok=True)

# ============================================================
# 蒙特卡洛模拟
# ============================================================
N_SAMPLES = 100000
np.random.seed(42)

print("=" * 70)
print("Monte Carlo Global Uncertainty Analysis")
print(f"  N = {N_SAMPLES:,} samples")
print("=" * 70)

# --- 参数分布定义 ---
# 1. 扩散系数 D: Uniform(1.0e-9, 3.0e-9) m²/s
D_samples = np.random.uniform(1.0e-9, 3.0e-9, N_SAMPLES)

# 2. 孔隙率 ε: Uniform(0.1, 0.5)
eps_samples = np.random.uniform(0.1, 0.5, N_SAMPLES)

# 3. 曲折因子 τ: Uniform(1.5, 5.0)
tau_samples = np.random.uniform(1.5, 5.0, N_SAMPLES)

# 4. 电流效率 η_I: Triangular(0.50, 0.75, 0.88)
#    众数0.75（最可能值），下限0.50（扩展保守下限），上限0.88（Downs上限）
#    论文声称使用扩展分布以覆盖更大的不确定性
eta_samples = np.random.triangular(0.50, 0.75, 0.88, N_SAMPLES)

# 5. 槽电压 V_cell: Normal(4.1, 0.3) truncated to [3.5, 4.5]
V_raw = np.random.normal(4.1, 0.3, N_SAMPLES)
V_samples = np.clip(V_raw, 3.5, 4.5)

# --- 输出量1: SCM还原时间 ---
# t = c_O * R² / (6 * D_eff * c_red)
# D_eff = D * ε / τ
D_eff_samples = D_samples * eps_samples / tau_samples
t_samples = (c_O * R_particle**2) / (6 * D_eff_samples * c_red)  # seconds
t_min_samples = t_samples / 60  # minutes

print(f"\n--- SCM Reduction Time (100 μm particles) ---")
print(f"  Mean:   {np.mean(t_min_samples):.1f} min")
print(f"  Median: {np.median(t_min_samples):.1f} min")
print(f"  Std:    {np.std(t_min_samples):.1f} min")
print(f"  P5:     {np.percentile(t_min_samples, 5):.1f} min")
print(f"  P95:    {np.percentile(t_min_samples, 95):.1f} min")
print(f"  Min:    {np.min(t_min_samples):.1f} min")
print(f"  Max:    {np.max(t_min_samples):.1f} min")

# --- 输出量2: 全流程净能耗 ---
# W_practical = 4F * n_Ti * V_cell / (η_I * 3.6e6)  [kWh/ton]
# W_net ≈ W_practical + 680 (auxiliary) - 42 (Ti cooling)
# 其中电解部分 = W_practical, 辅助能耗固定680, 回收42
W_electrolysis = (4 * F * n_Ti * V_samples) / (eta_samples * 3.6e6)  # kWh/ton
# Net equivalent consumption: gross electrolysis - reaction exotherm (1690 kWh/ton) + auxiliary (680) - Ti cooling (42)
W_net_samples = W_electrolysis - 1690 + 680 - 42  # = W_electrolysis - 1052

print(f"\n--- Net Energy Consumption ---")
print(f"  Mean:   {np.mean(W_net_samples):.0f} kWh/ton-Ti")
print(f"  Median: {np.median(W_net_samples):.0f} kWh/ton-Ti")
print(f"  Std:    {np.std(W_net_samples):.0f} kWh/ton-Ti")
print(f"  P5:     {np.percentile(W_net_samples, 5):.0f} kWh/ton-Ti")
print(f"  P95:    {np.percentile(W_net_samples, 95):.0f} kWh/ton-Ti")
print(f"  Min:    {np.min(W_net_samples):.0f} kWh/ton-Ti")
print(f"  Max:    {np.max(W_net_samples):.0f} kWh/ton-Ti")

# --- 输出量3: 过程电效率 ---
W_min_elec = 6112  # kWh/ton (electrolysis step minimum)
W_reversible = 4550  # kWh/ton (TiO2→Ti+O2 reversible work)
eff_elec_samples = W_min_elec / W_net_samples * 100  # %
eff_2nd_law_samples = W_reversible / W_net_samples * 100  # %

print(f"\n--- Process Energy Efficiency (6112/W_net) ---")
print(f"  Mean:   {np.mean(eff_elec_samples):.1f}%")
print(f"  P5:     {np.percentile(eff_elec_samples, 5):.1f}%")
print(f"  P95:    {np.percentile(eff_elec_samples, 95):.1f}%")

print(f"\n--- Second-law Efficiency (4550/W_net) ---")
print(f"  Mean:   {np.mean(eff_2nd_law_samples):.1f}%")
print(f"  P5:     {np.percentile(eff_2nd_law_samples, 5):.1f}%")
print(f"  P95:    {np.percentile(eff_2nd_law_samples, 95):.1f}%")

# --- 概率分析：低于目标值的概率 ---
targets_energy = [11192, 12000, 14000, 16000, 20000]
print(f"\n--- P(W_net < target) ---")
for target in targets_energy:
    prob = np.mean(W_net_samples < target) * 100
    print(f"  P(W_net < {target:,}) = {prob:.1f}%")

targets_time = [5, 10, 15, 20, 30]
print(f"\n--- P(t_complete < target) ---")
for target in targets_time:
    prob = np.mean(t_min_samples < target) * 100
    print(f"  P(t < {target} min) = {prob:.1f}%")

# ============================================================
# 绘图
# ============================================================

# --- 图1: SCM还原时间分布 ---
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

ax = axes[0]
ax.hist(t_min_samples, bins=100, density=True, alpha=0.7, color='steelblue',
        edgecolor='black', linewidth=0.3)
# 叠加对数正态拟合
from scipy.stats import lognorm
shape, loc, scale = lognorm.fit(t_min_samples, floc=0)
x_fit = np.linspace(0, np.percentile(t_min_samples, 99), 500)
ax.plot(x_fit, lognorm.pdf(x_fit, shape, loc, scale), 'r-', linewidth=2, label='Lognormal fit')
ax.axvline(np.median(t_min_samples), color='green', linestyle='--', linewidth=2, label=f'Median={np.median(t_min_samples):.1f} min')
ax.axvline(5.8, color='orange', linestyle='--', linewidth=2, label='Nominal (5.8 min)')
ax.set_xlabel('Complete Reduction Time (min)', fontsize=12)
ax.set_ylabel('Probability Density', fontsize=12)
ax.set_title('SCM Reduction Time Distribution\n(100 μm particles, global uncertainty)', fontsize=13)
ax.legend(fontsize=9)
ax.set_xlim(0, np.percentile(t_min_samples, 99))
ax.grid(True, alpha=0.3)

# --- 图2: 净能耗分布 ---
ax = axes[1]
ax.hist(W_net_samples, bins=100, density=True, alpha=0.7, color='coral',
        edgecolor='black', linewidth=0.3)
# 正态拟合
mu_w, sigma_w = stats.norm.fit(W_net_samples)
x_fit = np.linspace(np.percentile(W_net_samples, 0.5), np.percentile(W_net_samples, 99.5), 500)
ax.plot(x_fit, stats.norm.pdf(x_fit, mu_w, sigma_w), 'r-', linewidth=2, label=f'Normal fit\n(μ={mu_w:.0f}, σ={sigma_w:.0f})')
ax.axvline(np.median(W_net_samples), color='green', linestyle='--', linewidth=2, label=f'Median={np.median(W_net_samples):.0f}')
ax.axvline(11192, color='orange', linestyle='--', linewidth=2, label='Nominal (11,192)')
ax.axvline(20000, color='red', linestyle=':', linewidth=2, label='FFC upper (20,000)')
ax.set_xlabel('Net Energy Consumption (kWh/ton-Ti)', fontsize=12)
ax.set_ylabel('Probability Density', fontsize=12)
ax.set_title('Net Energy Consumption Distribution\n(global uncertainty, N=100k)', fontsize=13)
ax.legend(fontsize=9)
ax.set_xlim(np.percentile(W_net_samples, 0.5), np.percentile(W_net_samples, 99.5))
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(FIGURE_DIR, 'fig_monte_carlo.pdf'), bbox_inches='tight')
plt.close()
print(f"\nSaved: fig_monte_carlo.pdf")

# ============================================================
# 散点图: 参数敏感性 (Tornado plot 替代)
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# SCM时间 vs 各参数 (Spearman秩相关)
ax = axes[0]
params_scm = {
    'D (m²/s)': D_samples,
    'ε (porosity)': eps_samples,
    'τ (tortuosity)': tau_samples,
}
correlations = []
labels = []
for name, values in params_scm.items():
    rho, p = stats.spearmanr(values, t_min_samples)
    correlations.append(rho)
    labels.append(name)

colors = ['steelblue' if c < 0 else 'coral' for c in correlations]
bars = ax.barh(labels, correlations, color=colors, edgecolor='black', linewidth=0.5)
ax.set_xlabel('Spearman Rank Correlation', fontsize=12)
ax.set_title('SCM Time: Parameter Importance\n(global sensitivity)', fontsize=13)
ax.axvline(0, color='black', linewidth=0.8)
ax.grid(True, alpha=0.3, axis='x')
for bar, rho in zip(bars, correlations):
    ax.text(bar.get_width() + 0.02 * np.sign(rho), bar.get_y() + bar.get_height()/2,
            f'ρ={rho:.3f}', va='center', fontsize=10)

# 能耗 vs 各参数
ax = axes[1]
params_energy = {
    'η_I (current eff.)': eta_samples,
    'V_cell (V)': V_samples,
}
correlations_e = []
labels_e = []
for name, values in params_energy.items():
    rho, p = stats.spearmanr(values, W_net_samples)
    correlations_e.append(rho)
    labels_e.append(name)

colors_e = ['steelblue' if c < 0 else 'coral' for c in correlations_e]
bars = ax.barh(labels_e, correlations_e, color=colors_e, edgecolor='black', linewidth=0.5)
ax.set_xlabel('Spearman Rank Correlation', fontsize=12)
ax.set_title('Energy Consumption: Parameter Importance\n(global sensitivity)', fontsize=13)
ax.axvline(0, color='black', linewidth=0.8)
ax.grid(True, alpha=0.3, axis='x')
for bar, rho in zip(bars, correlations_e):
    ax.text(bar.get_width() + 0.02 * np.sign(rho), bar.get_y() + bar.get_height()/2,
            f'ρ={rho:.3f}', va='center', fontsize=10)

plt.tight_layout()
plt.savefig(os.path.join(FIGURE_DIR, 'fig_sensitivity_tornado.pdf'), bbox_inches='tight')
plt.close()
print(f"Saved: fig_sensitivity_tornado.pdf")

# ============================================================
# CSV输出
# ============================================================
csv_path = os.path.join(OUTPUT_DIR, 'tab_monte_carlo_stats.csv')
with open(csv_path, 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerow(['Metric', 'Mean', 'Median', 'Std', 'P5', 'P25', 'P75', 'P95', 'Min', 'Max'])
    
    def write_stats(name, data):
        writer.writerow([
            name,
            f'{np.mean(data):.2f}',
            f'{np.median(data):.2f}',
            f'{np.std(data):.2f}',
            f'{np.percentile(data, 5):.2f}',
            f'{np.percentile(data, 25):.2f}',
            f'{np.percentile(data, 75):.2f}',
            f'{np.percentile(data, 95):.2f}',
            f'{np.min(data):.2f}',
            f'{np.max(data):.2f}',
        ])
    
    write_stats('SCM_time(min)', t_min_samples)
    write_stats('W_net(kWh/ton)', W_net_samples)
    write_stats('eff_elec(%)', eff_elec_samples)
    write_stats('eff_2nd_law(%)', eff_2nd_law_samples)
    
    writer.writerow([])
    writer.writerow(['Probability Analysis'])
    writer.writerow(['Target', 'P(X < target)'])
    for target in targets_energy:
        prob = np.mean(W_net_samples < target) * 100
        writer.writerow([f'W_net < {target}', f'{prob:.1f}%'])
    for target in targets_time:
        prob = np.mean(t_min_samples < target) * 100
        writer.writerow([f't < {target} min', f'{prob:.1f}%'])

print(f"Saved: tab_monte_carlo_stats.csv")
print(f"\n{'='*70}")
print("Monte Carlo analysis complete.")
print(f"{'='*70}")
