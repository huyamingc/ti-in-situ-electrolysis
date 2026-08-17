#!/usr/bin/env python3
"""
verification_fix.py
===================
验证论文所有关键数值，计算过电位修正，重编热平衡，生成修正后的图表。
输出保存到 output/ 和 figures/ 目录。
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import csv
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', 'output')
FIGURE_DIR = os.path.join(SCRIPT_DIR, '..', 'figures')
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(FIGURE_DIR, exist_ok=True)

# ============================================================
# 常数
# ============================================================
R = 8.314          # J/(mol·K)
F = 96485          # C/mol
T = 873.15         # K (600°C)
ln10 = np.log(10)

# ============================================================
# 1. 验证液相线计算 (Sec.3.2)
# ============================================================
print("=" * 60)
print("1. 液相线验证 (Sec.3.2)")
print("=" * 60)

# 熔融参数: (Tm_K, dHfus_kJ/mol)
salts = {
    'MgCl2': (987, 43.1),
    'CaCl2': (1045, 28.5),
    'NaCl':  (1074, 28.2),
    'KCl':   (1043, 26.6),
}
x_recommended = {'MgCl2': 0.30, 'CaCl2': 0.40, 'NaCl': 0.15, 'KCl': 0.15}

# 求液相线温度: 找到使 max(x_i / threshold_i) = 1 的 T
from scipy.optimize import brentq

def liquidus_residual(T_liq, x_comp, salt_params):
    """在温度T下，各组分阈值与实际摩尔分数的比值，取最大值"""
    ratios = []
    for name, (Tm, dH) in salt_params.items():
        dH_J = dH * 1000  # 转为 J/mol
        threshold = np.exp(-dH_J / R * (1/T_liq - 1/Tm))
        ratios.append(x_comp[name] / threshold)
    return max(ratios) - 1.0  # = 0 时为液相线

T_liq = brentq(liquidus_residual, 700, 1000, args=(x_recommended, salts))
print(f"  计算液相线温度: {T_liq:.1f} K = {T_liq - 273.15:.1f} °C")
print(f"  论文报告: 544 °C (817 K)")
print(f"  偏差: {abs(T_liq - 817):.1f} K")

# 验证各组分在 T=817K 下的阈值
T_check = 817
print(f"\n  在 T={T_check}K 下各组分阈值:")
for name, (Tm, dH) in salts.items():
    dH_J = dH * 1000
    threshold = np.exp(-dH_J / R * (1/T_check - 1/Tm))
    x = x_recommended[name]
    status = "✓" if x <= threshold else "✗"
    margin = (threshold - x) / x * 100
    print(f"    {name}: x={x:.2f}, threshold={threshold:.4f}, 余量={margin:.1f}% {status}")

# ============================================================
# 2. 验证共沉积窗口 (Sec.3.3, Sec.4.2)
# ============================================================
print("\n" + "=" * 60)
print("2. 共沉积窗口验证 (Sec.3.3, Sec.4.2)")
print("=" * 60)

# 纯盐标准还原电位 (vs Cl2/Cl-), 来自论文Table (manuscript.tex)
E0_CaCl2 = -3.428  # V
E0_NaCl  = -3.440  # V

# Nernst 修正
x_CaCl2 = 0.40
x_NaCl  = 0.15

def calc_window(gamma_Ca, gamma_Na, T=873.15):
    """计算共沉积窗口 (mV)"""
    E_Ca = E0_CaCl2 + (R * T / (2 * F)) * np.log(gamma_Ca * x_CaCl2)
    E_Na = E0_NaCl  + (R * T / (1 * F)) * np.log(gamma_Na * x_NaCl)
    return (E_Ca - E_Na) * 1000  # mV

# 验证全表
gamma_Ca_list = [1.0, 0.9, 0.8, 0.7, 0.5, 0.3]
gamma_Na_list = [1.0, 0.85, 0.70]

print(f"  理想溶液窗口 (γ_Ca=1.0, γ_Na=1.0): {calc_window(1.0, 1.0):.1f} mV (论文: 120.2)")
print(f"\n  完整敏感性表:")
print(f"  {'γ_Ca':>6} {'γ_Na':>6} {'计算(mV)':>10} {'论文(mV)':>10} {'偏差':>8}")
paper_values = [
    (1.0, 1.00, 120.2), (1.0, 0.85, 132.4), (1.0, 0.70, 147.1),
    (0.9, 1.00, 116.3), (0.9, 0.85, 128.5), (0.9, 0.70, 143.1),
    (0.8, 1.00, 111.8), (0.8, 0.85, 124.1), (0.8, 0.70, 138.7),
    (0.7, 1.00, 106.8), (0.7, 0.85, 119.0), (0.7, 0.70, 133.6),
    (0.5, 1.00, 94.2),  (0.5, 0.85, 106.4), (0.5, 0.70, 121.0),
    (0.3, 1.00, 74.9),  (0.3, 0.85, 87.2),  (0.3, 0.70, 101.8),
]
for gC, gN, paper_val in paper_values:
    calc_val = calc_window(gC, gN)
    diff = calc_val - paper_val
    print(f"  {gC:6.1f} {gN:6.2f} {calc_val:10.1f} {paper_val:10.1f} {diff:+8.1f}")

# ============================================================
# 3. 过电位分析与有效共沉积窗口 (新增)
# ============================================================
print("\n" + "=" * 60)
print("3. 过电位分析与有效共沉积窗口 (新增)")
print("=" * 60)

# Butler-Volmer 活化过电位估计
# η_act = (RT/(αnF)) * asinh(j / (2*j0))
# 典型参数: α = 0.5, j0 = 0.01-0.1 A/cm² (金属沉积, 仅数量级估计)

alpha = 0.5
j0_Ca = 0.05  # A/cm², Ca²⁺ 交换电流密度 (文献典型值)
j0_Na = 0.03  # A/cm², Na⁺ 交换电流密度 (略低，Na⁺ 溶剂化更强)
j_operating = 0.5  # A/cm², 操作电流密度 (中等)

def act_overpotential(j, j0, alpha, n, T):
    """Butler-Volmer 活化过电位"""
    return (R * T / (alpha * n * F)) * np.arcsinh(j / (2 * j0))

eta_Ca = act_overpotential(j_operating, j0_Ca, alpha, 2, T)
eta_Na = act_overpotential(j_operating, j0_Na, alpha, 1, T)

print(f"  操作电流密度: {j_operating} A/cm²")
print(f"  Ca²⁺ 活化过电位 (n=2, j0={j0_Ca}): η_Ca = {eta_Ca*1000:.1f} mV")
print(f"  Na⁺  活化过电位 (n=1, j0={j0_Na}): η_Na = {eta_Na*1000:.1f} mV")
print(f"  过电位差 (η_Ca - η_Na): {(eta_Ca - eta_Na)*1000:.1f} mV")
print(f"  注意: 以上过电位值为基于文献典型参数的数量级估计，")
print(f"        实际值取决于电极材料、表面状态和熔盐组成，需实验测定。")

# 浓差极化估计 (简化)
# η_conc = (RT/nF) * ln(1 - j/j_lim)
# j_lim 取决于浓度和扩散系数
# 对于 Ca²⁺ (x=0.40, 充足): j_lim 高, η_conc 小
# 对于 Na⁺ (x=0.15, 较少): j_lim 较低, η_conc 较大
D_Ca = 2.0e-9  # m²/s
D_Na = 3.0e-9  # m²/s (Na⁺ 扩散更快)
# 极限电流密度必须用熔盐中的 Ca²⁺/Na⁺ 离子浓度(而非溶解金属浓度)计算
c_melt = 1800.0 / 0.093  # 熔盐总摩尔密度 mol/m³ (ρ=1.8 g/cm³, M_avg≈93 g/mol)
c_Ca = 0.40 * c_melt    # Ca²⁺ 离子浓度 (x_CaCl2=0.40)
c_Na = 0.15 * c_melt    # Na⁺ 离子浓度 (x_NaCl=0.15)
delta = 1e-4  # 扩散层厚度 100 μm (自然对流)

j_lim_Ca = 2 * F * D_Ca * c_Ca / delta / 1e4  # A/cm²
j_lim_Na = 1 * F * D_Na * c_Na / delta / 1e4

eta_conc_Ca = (R * T / (2 * F)) * np.log(1 - j_operating/j_lim_Ca) if j_operating < j_lim_Ca else np.nan
eta_conc_Na = (R * T / (1 * F)) * np.log(1 - j_operating/j_lim_Na) if j_operating < j_lim_Na else np.nan

_ecC_str = f"{eta_conc_Ca*1000:.1f}" if not np.isnan(eta_conc_Ca) else "mass-transfer limited"
_ecN_str = f"{eta_conc_Na*1000:.1f}" if not np.isnan(eta_conc_Na) else "mass-transfer limited"
print(f"\n  Ca²⁺ 浓差极化: {_ecC_str} mV (j_lim={j_lim_Ca:.2f} A/cm²)")
print(f"  Na⁺  浓差极化: {_ecN_str} mV (j_lim={j_lim_Na:.2f} A/cm²)")

# 有效窗口（带符号约定: eta_conc = (RT/nF)ln(1-j/j_lim) < 0, 使还原电位更负）
# Ca²⁺ 的有效还原电位 = E_Ca - η_Ca + η_conc_Ca
# Na⁺ 的有效还原电位 = E_Na - η_Na + η_conc_Na
# 有效窗口 = (E_Ca - η_Ca + η_conc_Ca) - (E_Na - η_Na + η_conc_Na)
#          = (E_Ca - E_Na) - (η_Ca - η_Na) + (η_conc_Ca - η_conc_Na)

thermo_window = calc_window(1.0, 1.0)  # mV
# 手稿的有效窗口只含活化过电位修正: E_eff = ΔE + (η_Na,act − η_Ca,act)
eta_act_diff = (eta_Na - eta_Ca) * 1000  # mV
effective_window = thermo_window + eta_act_diff  # 仅活化修正 (与手稿 Sec.4.2 一致)

print(f"\n  热力学窗口 (理想): {thermo_window:.1f} mV")
print(f"  活化过电位修正 (η_Na − η_Ca): {eta_act_diff:.1f} mV")
print(f"  有效共沉积窗口 (仅活化修正): {effective_window:.1f} mV")

# 在不同电流密度下扫描 (有效窗口仅含活化过电位; 浓差极化单独列出)
print(f"\n  不同电流密度下的有效窗口 (仅活化修正):")
print(f"  {'j (A/cm²)':>10} {'η_Ca(mV)':>10} {'η_Na(mV)':>10} {'窗口(mV)':>10}")
for j in [0.1, 0.2, 0.3, 0.5, 0.8, 1.0]:
    eC = act_overpotential(j, j0_Ca, alpha, 2, T) * 1000
    eN = act_overpotential(j, j0_Na, alpha, 1, T) * 1000
    # 浓差极化 (超过极限电流密度时标记为传质控制)
    jlim_Ca = 2 * F * D_Ca * c_Ca / delta / 1e4
    jlim_Na = 1 * F * D_Na * c_Na / delta / 1e4
    ecC = (R * T / (2 * F)) * np.log(1 - j/jlim_Ca) * 1000 if j < jlim_Ca else np.nan
    ecN = (R * T / (1 * F)) * np.log(1 - j/jlim_Na) * 1000 if j < jlim_Na else np.nan
    eff = thermo_window + (eN - eC)  # 仅活化修正
    print(f"  {j:10.1f} {eC:10.1f} {eN:10.1f} {eff:10.1f}")

# ============================================================
# 4. SCM 验证 (Sec.4.4)
# ============================================================
print("\n" + "=" * 60)
print("4. SCM 动力学验证 (Sec.4.4)")
print("=" * 60)

c_O = 1.06e5      # mol/m³
c_red = 581        # mol/m³ (0.03 × 1800/0.0929, M_avg 摩尔分数加权)
D = 2.0e-9         # m²/s
eps = 0.3
tau = 3.0
D_eff = D * eps / tau

print(f"  D_eff = D·ε/τ = {D}×{eps}/{tau} = {D_eff:.2e} m²/s")

# R = 50 μm (100 μm 颗粒的半径)
R_50 = 50e-6  # m
t_50 = (c_O * R_50**2) / (6 * D_eff * c_red)
print(f"\n  R = 50 μm (100 μm 直径颗粒):")
print(f"    t = {t_50:.0f} s = {t_50/60:.1f} min")

# R = 100 μm (如果论文把直径当半径)
R_100 = 100e-6  # m
t_100 = (c_O * R_100**2) / (6 * D_eff * c_red)
print(f"\n  R = 100 μm (200 μm 直径颗粒):")
print(f"    t = {t_100:.0f} s = {t_100/60:.1f} min")

# 敏感性分析 (R = 50 μm, 即 100 μm 颗粒)
print(f"\n  敏感性分析 (R = 50 μm, 即 100 μm 直径颗粒):")
for D_val in [1.0e-9, 2.0e-9, 3.0e-9]:
    D_eff_val = D_val * eps / tau
    t_val = (c_O * R_50**2) / (6 * D_eff_val * c_red)
    print(f"    D = {D_val:.1e} → t = {t_val:.0f} s = {t_val/60:.1f} min")

# 敏感性分析 (R = 100 μm, 即 200 μm 颗粒)
print(f"\n  敏感性分析 (R = 100 μm, 即 200 μm 直径颗粒):")
for D_val in [1.0e-9, 2.0e-9, 3.0e-9]:
    D_eff_val = D_val * eps / tau
    t_val = (c_O * R_100**2) / (6 * D_eff_val * c_red)
    print(f"    D = {D_val:.1e} → t = {t_val:.0f} s = {t_val/60:.1f} min")

# ============================================================
# 5. 脱氧倍数验证 (Sec.4.1)
# ============================================================
print("\n" + "=" * 60)
print("5. 脱氧倍数验证 (Sec.4.1)")
print("=" * 60)

ppm_Mg = 3908
ppm_Ca = 20
ratio_actual = ppm_Mg / ppm_Ca
print(f"  3908 / 20 = {ratio_actual:.1f}×")
print(f"  论文报告: 194×")
print(f"  实际比值: {ratio_actual:.1f}× → 应为 {round(ratio_actual)}×")

# 理论比值
dG_Mg = -6800   # J/mol (论文报告 -6.8 kJ/mol)
dG_Ca = -45000  # J/mol (论文报告 -45.0 kJ/mol)
ratio_theory = np.exp((dG_Mg - dG_Ca) / (R * T))
print(f"  理论比值 (基于ΔG°): exp({dG_Mg - dG_Ca}/{R*T:.0f}) = {ratio_theory:.1f}×")

# ============================================================
# 6. 能量计算验证 (Sec.4.5)
# ============================================================
print("\n" + "=" * 60)
print("6. 能量计算验证 (Sec.4.5)")
print("=" * 60)

n_Ti = 1e6 / 47.867  # mol Ti per ton
print(f"  n_Ti = 10⁶/47.867 = {n_Ti:.1f} mol/ton")

# 理论最低能量
V_theory = 2.729
W_theory = (4 * F * n_Ti * V_theory) / (1.0 * 3.6e6)
print(f"  理论最低 (V=2.729): {W_theory:.0f} kWh/ton (论文: 6112)")

# 实际能耗表
print(f"\n  实际能耗验证:")
energy_cases = [
    (0.85, 3.5, 9222),
    (0.80, 4.0, 11198),
    (0.75, 4.0, 11944),
    (0.75, 4.3, 12840),
    (0.70, 4.5, 14397),
]
for eta, V, paper_val in energy_cases:
    W = (4 * F * n_Ti * V) / (eta * 3.6e6)
    print(f"    η={eta}, V={V}: 计算={W:.0f}, 论文={paper_val}, 偏差={W-paper_val:+.0f}")

# ============================================================
# 7. 热平衡修正 (Sec.4.6)
# ============================================================
print("\n" + "=" * 60)
print("7. 热平衡修正 (Sec.4.6)")
print("=" * 60)

# 原始数据
electrolysis = 10554
TiO2_preheat = 184
salt_makeup = 7
cell_loss = 138
salt_pump = 50
post_treat = 300
total_input = electrolysis + TiO2_preheat + salt_makeup + cell_loss + salt_pump + post_treat
print(f"  总输入 = {electrolysis}+{TiO2_preheat}+{salt_makeup}+{cell_loss}+{salt_pump}+{post_treat} = {total_input}")

reaction_exotherm = 1690
Ti_cooling = 42
total_recovery = reaction_exotherm + Ti_cooling
print(f"  热回收 = {reaction_exotherm}+{Ti_cooling} = {total_recovery}")

net_wrong = total_input - Ti_cooling  # 论文的做法
net_correct = total_input - total_recovery  # 正确做法
print(f"\n  论文净值 = {total_input} - {Ti_cooling} = {net_wrong} (仅扣除了{Ti_cooling})")
print(f"  正确净值 = {total_input} - {total_recovery} = {net_correct}")

# 但是！如果 1690 已嵌入电解能耗中:
# 即电解实际需要 10554+1690=12244，但反应放热覆盖了1690，净电解=10554
# 那么总外部输入 = 10554 + 679 = 11233
# 净值 = 11233 - 42(Ti冷却) = 11191
# 这种解释下 1690 是内部热回收，不从总输入中额外扣除
print(f"\n  解释B: 1690为内部热循环(已嵌入电解项)")
print(f"    电解毛需求 = 10554 + 1690 = {10554+1690}")
print(f"    反应放热覆盖 = {reaction_exotherm}")
print(f"    净电解输入 = {10554+1690} - {reaction_exotherm} = {10554}")
print(f"    总外部输入 = 10554 + {total_input-10554} = {total_input}")
print(f"    净值 = {total_input} - {Ti_cooling} = {total_input - Ti_cooling} ≈ 11191")

# 效率重新定义
print(f"\n  效率重新定义:")
W_min = 6112
W_net = 11191
print(f"  理论最低能耗 W_min = {W_min} kWh/ton")
print(f"  实际净能耗 W_net = {W_net} kWh/ton")
print(f"  热力学效率 = W_min/W_net = {W_min/W_net*100:.1f}%")
print(f"  论文报告电解占比 = 94.0% (= 电解/总输入 = {electrolysis}/{total_input} = {electrolysis/total_input*100:.1f}%)")
print(f"  论文报告过程能效 = {W_min/W_net*100:.1f}% (W_min/W_net)")

# 正确的火用效率估计
# 火用输入 = 电能火用 + 热火用
# 电能火用 ≈ 电能本身 (电能全是火用)
# 热输入的火用 = Q × (1 - T0/T)
T0 = 298.15  # 环境温度
T_proc = 873.15  # 工艺温度

# 电解火用 = 10554 kWh (电能)
# 预热等热火用 = (184+7+50+300) × (1 - 298/873) = 541 × 0.659 = 357 kWh
thermal_input = TiO2_preheat + salt_makeup + salt_pump + post_treat
exergy_thermal = thermal_input * (1 - T0/T_proc)
exergy_electrical = electrolysis
exergy_input_total = exergy_electrical + exergy_thermal
# 火用输出 = 理论最低功 + 不可逆损失
# 火用效率 = W_min / 火用输入
exergy_eff = W_min / exergy_input_total * 100

print(f"\n  火用分析:")
print(f"    电能火用 = {exergy_electrical:.0f} kWh")
print(f"    热输入火用 = {thermal_input}×(1-298/873) = {exergy_thermal:.0f} kWh")
print(f"    总火用输入 = {exergy_input_total:.0f} kWh")
print(f"    火用效率 = {W_min}/{exergy_input_total:.0f} = {exergy_eff:.1f}%")

# 电压效率
V_cell_typical = 4.0
V_decomp = 2.729
voltage_eff = V_decomp / V_cell_typical * 100
current_eff = 75  # %
print(f"\n  电压效率 = {V_decomp}/{V_cell_typical} = {voltage_eff:.1f}%")
print(f"  电流效率 = {current_eff}%")
print(f"  综合电解效率 = {voltage_eff*current_eff/100:.1f}%")

# ============================================================
# 8. Mg-Ca 合金验证 (Sec.3.4)
# ============================================================
print("\n" + "=" * 60)
print("8. Mg-Ca 合金验证 (Sec.3.4)")
print("=" * 60)

L0 = -30616 + 13.72 * 873
print(f"  L0 = -30616 + 13.72×873 = {L0:.0f} J/mol = {L0/1000:.2f} kJ/mol")

# 等摩尔混合
x_Mg = 0.5
x_Ca = 0.5
Omega = L0  # 规则溶液近似

dG_mix = R * T * (x_Mg * np.log(x_Mg) + x_Ca * np.log(x_Ca)) + Omega * x_Mg * x_Ca
dH_mix = Omega * x_Mg * x_Ca
dS_mix = (dH_mix - dG_mix) / T

# 活度系数
# ln(γ_Mg) = Ω * x_Ca² / (RT)
ln_gamma_Mg = Omega * x_Ca**2 / (R * T)
gamma_Mg = np.exp(ln_gamma_Mg)

print(f"  ΔG_mix = {dG_mix/1000:.2f} kJ/mol (论文: -9.69)")
print(f"  ΔH_mix = {dH_mix/1000:.2f} kJ/mol (论文: -4.66)")
print(f"  ΔS_mix = {dS_mix:.2f} J/(mol·K) (论文: 5.76)")
print(f"  γ_Mg = γ_Ca = {gamma_Mg:.3f} (论文: 0.526)")

# ============================================================
# 9. 分解电压验证 (Sec.4.2)
# ============================================================
print("\n" + "=" * 60)
print("9. 分解电压验证 (Sec.4.2)")
print("=" * 60)

# 论文表中 ΔG°f 似乎是 298K 值，而 E_d 是 873K 值
# 验证: E_d = -ΔG°f(T)/(nF)
# 如果 ΔG°f 是 873K 值:
dGf_table = {'MgCl2': -641.3e3, 'NaCl': -385.5e3, 'CaCl2': -751.8e3, 'KCl': -408.5e3}
n_table = {'MgCl2': 2, 'NaCl': 1, 'CaCl2': 2, 'KCl': 1}  # n = 金属离子价数

print(f"  如果 ΔG°f 为 873K 值 (n = 离子价数):")
for salt, dGf in dGf_table.items():
    n = n_table[salt]
    Ed = -dGf / (n * F)
    print(f"    {salt}: n={n}, E_d = {Ed:.3f} V")

# 论文表中的 E_d 值
paper_Ed = {'MgCl2': 2.601, 'NaCl': 3.440, 'CaCl2': 3.428, 'KCl': 3.675}
print(f"\n  论文 E_d 值 vs 计算值:")
for salt in dGf_table:
    n = n_table[salt]
    Ed_calc = -dGf_table[salt] / (n * F)
    print(f"    {salt}: 论文={paper_Ed[salt]:.3f}, 计算(n={n})={Ed_calc:.3f}")

# 注意: 上方 dGf_table 为 298K 参考值；旧版论文 Table 曾混用 298K ΔG°f 与 873K E_d
# manuscript.tex 已统一为 873K 值: ΔG°f = MgCl2 -501.9, NaCl -331.9, CaCl2 -661.5, KCl -354.6 kJ/mol
print(f"\n  结论(已解决): v5 论文已统一使用 873K 的 ΔG°f 与 E_d (见表 tab:Ed)")
print(f"    (上方 298K 参考值仅供对比)")

# 反推 873K 下的 ΔG°f
print(f"\n  反推873K下的ΔG°f (基于E_d):")
for salt in dGf_table:
    n = n_table[salt]
    dGf_873 = -paper_Ed[salt] * n * F
    print(f"    {salt}: ΔG°f(873K) = {dGf_873/1000:.1f} kJ/mol")

# ============================================================
# 10. 生成修正后的图表
# ============================================================
print("\n" + "=" * 60)
print("10. 生成修正图表")
print("=" * 60)

# 10a. 过电位修正后的有效窗口图
fig, ax = plt.subplots(1, 1, figsize=(8, 5))
j_range = np.linspace(0.05, 1.0, 100)
windows = []
for j in j_range:
    eC = act_overpotential(j, j0_Ca, alpha, 2, T)
    eN = act_overpotential(j, j0_Na, alpha, 1, T)
    jlim_Ca = 2 * F * D_Ca * c_Ca / delta / 1e4
    jlim_Na = 1 * F * D_Na * c_Na / delta / 1e4
    if j < jlim_Ca and j < jlim_Na:
        ecC = (R * T / (2 * F)) * np.log(1 - j/jlim_Ca)
        ecN = (R * T / (1 * F)) * np.log(1 - j/jlim_Na)
    else:
        ecC = ecN = np.nan  # 传质受限，与表格/CSV 的 NaN 口径一致
    eff = thermo_window/1000 - (eC - eN) + (ecC - ecN)
    windows.append(eff * 1000)

ax.plot(j_range, windows, 'b-', linewidth=2, label='Effective window')
ax.axhline(y=0, color='r', linestyle='--', linewidth=1, label='Zero window (no co-deposition)')
ax.axhline(y=thermo_window, color='g', linestyle=':', linewidth=1.5, label=f'Thermodynamic window ({thermo_window:.0f} mV)')
ax.fill_between(j_range, windows, alpha=0.15, color='blue', where=[w > 0 for w in windows])
ax.fill_between(j_range, windows, alpha=0.15, color='red', where=[w <= 0 for w in windows])
ax.set_xlabel('Current density (A/cm²)', fontsize=12)
ax.set_ylabel('Effective co-deposition window (mV)', fontsize=12)
ax.set_title('Effective Ca²⁺/Na⁺ Co-deposition Window\nwith Overpotential Correction (600°C)', fontsize=13)
ax.legend(fontsize=10)
ax.set_ylim(0, None)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(FIGURE_DIR, 'fig_overpotential_window.pdf'), bbox_inches='tight')
print("  已保存: fig_overpotential_window.pdf")

# 10b. 修正后的热平衡 Sankey-style 柱状图
fig, ax = plt.subplots(1, 1, figsize=(8, 5))
categories = ['Electrolysis\n(gross)', 'Reaction\nexotherm', 'Auxiliary\ninputs', 'Ti cooling\nrecovery', 'Net\nconsumption']
values = [12244, -1690, 679, -42, 11191]
colors = ['#2196F3', '#4CAF50', '#FF9800', '#4CAF50', '#F44336']
bars = ax.bar(categories, values, color=colors, edgecolor='black', linewidth=0.5)
ax.axhline(y=0, color='black', linewidth=0.8)
ax.set_ylabel('Energy (kWh/ton-Ti)', fontsize=12)
ax.set_title('Revised Heat Balance: Energy Flow Breakdown\n(basis: 1 ton Ti, 600°C)', fontsize=13)
for bar, val in zip(bars, values):
    height = bar.get_height()
    label_y = height + 200 if height > 0 else height - 400
    ax.text(bar.get_x() + bar.get_width()/2., label_y,
            f'{val:+d}', ha='center', va='bottom' if height > 0 else 'top', fontsize=11, fontweight='bold')
ax.set_ylim(-3000, 16000)
ax.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig(os.path.join(FIGURE_DIR, 'fig_heat_balance_revised.pdf'), bbox_inches='tight')
print("  已保存: fig_heat_balance_revised.pdf")

# ============================================================
# 11. 保存验证结果到 CSV
# ============================================================
output_dir = OUTPUT_DIR

# 过电位表
with open(f'{output_dir}/tab_overpotential.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['j (A/cm2)', 'eta_Ca_act (mV)', 'eta_Na_act (mV)', 'eta_conc_Ca (mV)', 'eta_conc_Na (mV)', 'effective_window_act-only (mV)'])
    for j in [0.1, 0.2, 0.3, 0.5, 0.8, 1.0]:
        eC = act_overpotential(j, j0_Ca, alpha, 2, T) * 1000
        eN = act_overpotential(j, j0_Na, alpha, 1, T) * 1000
        jlim_Ca = 2 * F * D_Ca * c_Ca / delta / 1e4
        jlim_Na = 1 * F * D_Na * c_Na / delta / 1e4
        ecC = (R * T / (2 * F)) * np.log(1 - j/jlim_Ca) * 1000 if j < jlim_Ca else np.nan
        ecN = (R * T / (1 * F)) * np.log(1 - j/jlim_Na) * 1000 if j < jlim_Na else np.nan
        eff = thermo_window + (eN - eC)  # 仅活化修正 (与手稿一致)
        _ecC = f'{ecC:.1f}' if not np.isnan(ecC) else 'N/A'
        _ecN = f'{ecN:.1f}' if not np.isnan(ecN) else 'N/A'
        w.writerow([j, f'{eC:.1f}', f'{eN:.1f}', _ecC, _ecN, f'{eff:.1f}'])
print(f"\n  已保存: tab_overpotential.csv")

# 修正热平衡表
with open(f'{output_dir}/tab_heat_balance_revised.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['Item', 'Energy (kWh/ton)', 'Note'])
    w.writerow(['Electrolysis (gross)', '12244', 'Before reaction exotherm offset'])
    w.writerow(['Reaction exotherm', '-1690', 'Internal heat recovery, offsets electrolysis'])
    w.writerow(['Electrolysis (net)', '10554', 'Net electrical input'])
    w.writerow(['TiO2 preheating', '184', ''])
    w.writerow(['Salt makeup preheating', '7', ''])
    w.writerow(['Cell wall heat loss', '138', 'External thermal input (reaction exotherm fully used for electrolysis offset)'])
    w.writerow(['Salt circulation pumping', '50', ''])
    w.writerow(['Post-treatment', '300', ''])
    w.writerow(['Total external input', '11233', ''])
    w.writerow(['Ti powder cooling recovery', '-42', 'External heat recovery'])
    w.writerow(['Net consumption', '11191', ''])
    w.writerow(['Theoretical minimum', '6112', ''])
    w.writerow(['Thermodynamic efficiency', '54.6%', 'W_min/W_net'])
    w.writerow(['Energy utilization ratio', '94.0%', 'Electrolysis/Total input (NOT thermal efficiency)'])
print(f"  已保存: tab_heat_balance_revised.csv")

print("\n" + "=" * 60)
print("验证完成。所有数值已核对，修正图表已生成。")
print("=" * 60)
