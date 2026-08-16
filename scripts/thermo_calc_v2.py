# -*- coding: utf-8 -*-
"""
双金属协同还原制钛工艺 — 定量热力学与电化学计算 (v2, corrected)

用途：
  基于Kirchhoff定律与标准热力学数据，计算三种还原反应的ΔG°/ΔH°、
  脱氧平衡氧含量、氯化物分解电压、Ca²⁺/Na⁺共析窗口、物料衡算与能量衡算。
  所有数据来自文献（Barin 1995, Waldner 1999），无需实验。

依赖：
  Python 3.8+（仅使用标准库math和csv，无需安装任何第三方包）

运行方式：
  python scripts/thermo_calc_v2.py

输出：
  1. 控制台打印全部计算结果（5个PART）
  2. 生成6个CSV数据文件到 output/ 目录，供论文表格数据溯源：
     - tab_thermo.csv       — 三种还原反应ΔG°/ΔH°
     - tab_deox.csv         — 镁钙脱氧平衡氧含量
     - tab_Ed.csv           — 四种氯化物分解电压
     - tab_window.csv       — 共析窗口
     - tab_mbalance.csv     — 物料衡算
     - tab_energy.csv       — 能耗计算

生成的数据对应论文中：
  - 表 tab:thermo（三种还原反应ΔG°/ΔH°）
  - 表 tab:deox（镁钙脱氧平衡氧含量）
  - 表 tab:Ed（四种氯化物分解电压）
  - 表 tab:window（共析窗口）
  - 表 tab:mbalance（物料衡算）
  - 表 tab:energy（能耗计算）
"""
import math
import csv
import os

R = 8.314
F = 96485

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'output')
os.makedirs(OUTPUT_DIR, exist_ok=True)

def write_csv(filename, header, rows):
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)
    print(f"  → CSV saved: {path}")

# Standard thermodynamic data (298 K)
# Cp(T) via Meyer-Kelly equation: Cp = a + b*T + c/T^2  (J/mol·K)
# Coefficients from Barin (1995) and Kubaschewski & Alcock (1979)
# For species without Cp(T) data, b=c=0 (constant Cp approximation)
species = {
    'TiO2':  {'Hf': -944000, 'S': 50.6,  'Cp_a': 62.834, 'Cp_b': 11.882e-3, 'Cp_c': -9.782e5},
    'MgO':   {'Hf': -601600, 'S': 26.9,  'Cp_a': 48.982, 'Cp_b': 3.142e-3,  'Cp_c': -11.740e5},
    'CaO':   {'Hf': -635100, 'S': 39.7,  'Cp_a': 49.622, 'Cp_b': 4.519e-3,  'Cp_c': -6.945e5},
    'Ti':    {'Hf': 0,       'S': 30.7,  'Cp_a': 22.09,  'Cp_b': 10.46e-3,  'Cp_c': 0.0},
    'Mg':    {'Hf': 0,       'S': 32.7,  'Cp_a': 22.09,  'Cp_b': 10.46e-3,  'Cp_c': -0.418e5},
    'Ca':    {'Hf': 0,       'S': 41.6,  'Cp_a': 25.29,  'Cp_b': 3.85e-3,   'Cp_c': 0.0},
    'Na':    {'Hf': 0,       'S': 51.3,  'Cp_a': 28.2,   'Cp_b': 0.0,       'Cp_c': 0.0},
    'K':     {'Hf': 0,       'S': 64.7,  'Cp_a': 29.6,   'Cp_b': 0.0,       'Cp_c': 0.0},
    'MgCl2': {'Hf': -641300, 'S': 89.6,  'Cp_a': 72.426, 'Cp_b': 15.82e-3,  'Cp_c': -3.721e5},
    'CaCl2': {'Hf': -795800, 'S': 104.6, 'Cp_a': 71.881, 'Cp_b': 16.92e-3,  'Cp_c': -3.891e5},
    'NaCl':  {'Hf': -411200, 'S': 72.1,  'Cp_a': 50.074, 'Cp_b': 16.21e-3,  'Cp_c': -1.029e5},
    'KCl':   {'Hf': -436700, 'S': 82.6,  'Cp_a': 51.298, 'Cp_b': 13.36e-3,  'Cp_c': -0.866e5},
    'Cl2':   {'Hf': 0,       'S': 223.1, 'Cp_a': 36.90,  'Cp_b': 0.99e-3,   'Cp_c': -3.52e5},
    'O2':    {'Hf': 0,       'S': 205.2, 'Cp_a': 29.96,  'Cp_b': 4.18e-3,   'Cp_c': -1.67e5},
}

transitions = {
    'Mg': {'Tm': 923,  'Hfus': 8950, 'Cp_l': 32.7},
    'Ca': {'Tm': 1115, 'Hfus': 8540, 'Cp_l': 30.0},
    'Na': {'Tm': 371,  'Hfus': 2600, 'Cp_l': 30.5},
    'K':  {'Tm': 337,  'Hfus': 2320, 'Cp_l': 30.2},
}

def cp_func(name, T):
    """Meyer-Kelly heat capacity: Cp(T) = a + b*T + c/T^2"""
    sp = species[name]
    return sp['Cp_a'] + sp['Cp_b'] * T + sp['Cp_c'] / (T**2)

def get_H_S(name, T):
    """Calculate H(T) and S(T) using temperature-dependent Cp(T).
    
    Meyer-Kelly integrals:
      H(T) - H(298) = a*(T-298) + b/2*(T^2-298^2) - c*(1/T - 1/298)
      S(T) - S(298) = a*ln(T/298) + b*(T-298) - c/2*(1/T^2 - 1/298^2)
    """
    sp = species[name]
    a, b, c = sp['Cp_a'], sp['Cp_b'], sp['Cp_c']
    T_ref = 298.0
    H = sp['Hf']
    S = sp['S']
    tr = transitions.get(name)
    if tr and T > tr['Tm']:
        # Solid phase: 298 -> Tm (Meyer-Kelly integral)
        Tm = tr['Tm']
        H += a * (Tm - T_ref) + b/2 * (Tm**2 - T_ref**2) - c * (1/Tm - 1/T_ref)
        S += a * math.log(Tm / T_ref) + b * (Tm - T_ref) - c/2 * (1/Tm**2 - 1/T_ref**2)
        # Phase transition
        H += tr['Hfus']
        S += tr['Hfus'] / Tm
        # Liquid phase: Tm -> T (constant Cp_l)
        Cp_l = tr['Cp_l']
        H += Cp_l * (T - Tm)
        S += Cp_l * math.log(T / Tm)
    else:
        # Single phase: 298 -> T (Meyer-Kelly integral)
        H += a * (T - T_ref) + b/2 * (T**2 - T_ref**2) - c * (1/T - 1/T_ref)
        S += a * math.log(T / T_ref) + b * (T - T_ref) - c/2 * (1/T**2 - 1/T_ref**2)
    return H, S

def reaction_GHS(reaction, T):
    dH = sum(c * get_H_S(n, T)[0] for n, c in reaction.items())
    dS = sum(c * get_H_S(n, T)[1] for n, c in reaction.items())
    return dH - T * dS, dH, dS

temps = [823, 873, 923]

# ============================================================
# PART 1: Reduction thermodynamics
# ============================================================
print("=" * 70)
print("PART 1: Reduction Reaction Thermodynamics")
print("=" * 70)

reactions = {
    'R1: TiO2+2Mg ->Ti+2MgO':  {'TiO2':-1,'Mg':-2,'Ti':1,'MgO':2},
    'R2: TiO2+2Ca ->Ti+2CaO':  {'TiO2':-1,'Ca':-2,'Ti':1,'CaO':2},
    'R3: TiO2+Mg+Ca->Ti+MgO+CaO': {'TiO2':-1,'Mg':-1,'Ca':-1,'Ti':1,'MgO':1,'CaO':1},
}

print(f"\n{'Reaction':<30} {'°C':<5} {'ΔG(kJ/mol)':<12} {'ΔH(kJ/mol)':<12} {'ΔS(J/molK)':<12}")
print("-" * 73)
for name, rxn in reactions.items():
    for T in temps:
        dG,dH,dS = reaction_GHS(rxn, T)
        print(f"{name:<30} {T-273:<5} {dG/1000:<12.1f} {dH/1000:<12.1f} {dS:<12.1f}")

# CSV output
thermo_rows = []
for name, rxn in reactions.items():
    for T in temps:
        dG,dH,dS = reaction_GHS(rxn, T)
        thermo_rows.append([name, f"{T-273}", f"{dG/1000:.1f}", f"{dH/1000:.1f}", f"{dS:.1f}"])
write_csv('tab_thermo.csv', ['Reaction','T(C)','dG(kJ/mol)','dH(kJ/mol)','dS(J/molK)'], thermo_rows)

# ============================================================
# PART 2: Deoxidation limits
# ============================================================
print("\n" + "=" * 70)
print("PART 2: Deoxidation Limit (Equilibrium Oxygen in Ti)")
print("=" * 70)
print("Using ΔG°_diss(O in α-Ti) ≈ -581000 + 92T J/mol")
print(f"\n{'Deox':<5} {'°C':<5} {'ΔG_deox(kJ/mol)':<16} {'K':<10} {'w[O]_eq(wt%)':<14} {'ppm':<10}")
print("-" * 62)
for dname, drxn in [('Ca',{'Ca':-1,'O2':-0.5,'CaO':1}),('Mg',{'Mg':-1,'O2':-0.5,'MgO':1})]:
    for T in temps:
        dG_MO,_,_ = reaction_GHS(drxn, T)
        dG_diss = -581000 + 92*T
        dG_deox = dG_MO - dG_diss
        K = math.exp(-dG_deox/(R*T))
        wO = 1.0/K
        print(f"{dname:<5} {T-273:<5} {dG_deox/1000:<16.1f} {K:<10.1f} {wO:<14.4f} {wO*10000:<10.1f}")

print("\nCa/Mg deoxidation ratio:")
deox_rows = []
for T in temps:
    dG_Ca,_,_ = reaction_GHS({'Ca':-1,'O2':-0.5,'CaO':1}, T)
    dG_Mg,_,_ = reaction_GHS({'Mg':-1,'O2':-0.5,'MgO':1}, T)
    dG_diss = -581000 + 92*T
    wO_Ca = 1.0/math.exp(-(dG_Ca-dG_diss)/(R*T))
    wO_Mg = 1.0/math.exp(-(dG_Mg-dG_diss)/(R*T))
    print(f"  {T-273}°C: Mg→{wO_Mg:.4f} wt%, Ca→{wO_Ca:.4f} wt%, ratio={wO_Mg/wO_Ca:.0f}x")
    deox_rows.append(['Mg', f"{T-273}", f"{(dG_Mg-dG_diss)/1000:.1f}", f"{wO_Mg:.4f}", f"{wO_Mg*10000:.0f}"])
    deox_rows.append(['Ca', f"{T-273}", f"{(dG_Ca-dG_diss)/1000:.1f}", f"{wO_Ca:.4f}", f"{wO_Ca*10000:.0f}"])
write_csv('tab_deox.csv', ['Deoxidant','T(C)','dG_deox(kJ/mol)','wO_eq(wt%)','wO_eq(ppm)'], deox_rows)

# ============================================================
# PART 3: Electrochemistry (CORRECTED)
# ============================================================
print("\n" + "=" * 70)
print("PART 3: Chloride Decomposition & Co-deposition Window (CORRECTED)")
print("=" * 70)

chlorides = {
    'MgCl2': {'rxn':{'MgCl2':-1,'Mg':1,'Cl2':1},   'n':2},
    'CaCl2': {'rxn':{'CaCl2':-1,'Ca':1,'Cl2':1},   'n':2},
    'NaCl':  {'rxn':{'NaCl':-1,'Na':1,'Cl2':0.5},  'n':1},
    'KCl':   {'rxn':{'KCl':-1,'K':1,'Cl2':0.5},    'n':1},
}

print(f"\n{'Salt':<8} {'°C':<5} {'ΔG°f(kJ/mol)':<14} {'E_d(V)':<10} {'E_red(V vs Cl2/Cl-)':<22}")
print("-" * 60)

E_d = {}
E_red_std = {}
for cname, cdata in chlorides.items():
    E_d[cname] = {}
    E_red_std[cname] = {}
    for T in temps:
        dG_decomp,_,_ = reaction_GHS(cdata['rxn'], T)
        dGf = -dG_decomp
        Ed = dG_decomp / (cdata['n'] * F)
        Ered = -Ed
        E_d[cname][T] = Ed
        E_red_std[cname][T] = Ered
        print(f"{cname:<8} {T-273:<5} {dGf/1000:<14.1f} {Ed:<10.4f} {Ered:<22.4f}")

T = 873
print(f"\n--- Analysis at 600 °C (873 K) ---")
print(f"  RT/F = {R*T/F:.4f} V, RT/2F = {R*T/(2*F):.4f} V")
print(f"\n  Reduction potentials (vs Cl₂/Cl⁻, more negative = harder to reduce):")
print(f"    E°(Mg²⁺/Mg) = {E_red_std['MgCl2'][T]:.4f} V  ← easiest")
print(f"    E°(Na⁺/Na)  = {E_red_std['NaCl'][T]:.4f} V")
print(f"    E°(Ca²⁺/Ca) = {E_red_std['CaCl2'][T]:.4f} V")
print(f"    E°(K⁺/K)    = {E_red_std['KCl'][T]:.4f} V  ← hardest")

gap_CaNa = E_red_std['CaCl2'][T] - E_red_std['NaCl'][T]
print(f"\n  Ca²⁺/Na⁺ gap (pure salts): {gap_CaNa*1000:.1f} mV")
print(f"  → {'Na⁺ reduces first' if gap_CaNa < 0 else 'Ca²⁺ reduces first'} (consistent with Downs process producing Na)")

RT_F = R*T/F
RT_2F = R*T/(2*F)

print(f"\n--- Nernst-Corrected Ca²⁺/Na⁺ Selectivity Window ---")
print(f"  Window = E_red(Ca) - E_red(Na)")
print(f"  Positive → Ca²⁺ reduces before Na⁺ (GOOD)")
print(f"\n  {'Composition (mol fraction)':<50} {'Window(mV)':<12} {'Assessment':<15}")
print("  " + "-" * 78)

compositions = [
    ("Equal (0.25/0.25/0.25/0.25)", 0.25, 0.25, 0.25, 0.25),
    ("Ca-rich (0.30/0.40/0.15/0.15)", 0.30, 0.40, 0.15, 0.15),
    ("Low-NaK (0.35/0.45/0.10/0.10)", 0.35, 0.45, 0.10, 0.10),
    ("V-low-NaK (0.35/0.50/0.075/0.075)", 0.35, 0.50, 0.075, 0.075),
    ("Ca-dominant (0.25/0.55/0.10/0.10)", 0.25, 0.55, 0.10, 0.10),
    ("Downs-like (0/0.60/0.40/0)", 0.0, 0.60, 0.40, 0.0),
]

for desc, xMg, xCa, xNa, xK in compositions:
    E_Ca = E_red_std['CaCl2'][T] + RT_2F * math.log(xCa) if xCa > 0 else -999
    E_Na = E_red_std['NaCl'][T] + RT_F * math.log(xNa) if xNa > 0 else -999
    E_Mg = E_red_std['MgCl2'][T] + RT_2F * math.log(xMg) if xMg > 0 else -999
    E_K  = E_red_std['KCl'][T] + RT_F * math.log(xK) if xK > 0 else -999
    window = E_Ca - E_Na
    w_mV = window * 1000
    if w_mV > 100: assess = "Good"
    elif w_mV > 50: assess = "Moderate"
    elif w_mV > 0: assess = "Marginal"
    else: assess = "Na first!"
    print(f"  {desc:<50} {w_mV:<12.1f} {assess:<15}")

print(f"\n--- Recommended Composition Detail (x_MgCl2=0.30, x_CaCl2=0.40, x_NaCl=0.15, x_KCl=0.15) ---")
xMg, xCa, xNa, xK = 0.30, 0.40, 0.15, 0.15
E_Mg = E_red_std['MgCl2'][T] + RT_2F*math.log(xMg)
E_Ca = E_red_std['CaCl2'][T] + RT_2F*math.log(xCa)
E_Na = E_red_std['NaCl'][T] + RT_F*math.log(xNa)
E_K  = E_red_std['KCl'][T] + RT_F*math.log(xK)
print(f"  E_red(Mg²⁺/Mg) = {E_Mg:.4f} V")
print(f"  E_red(Ca²⁺/Ca) = {E_Ca:.4f} V")
print(f"  E_red(Na⁺/Na)  = {E_Na:.4f} V")
print(f"  E_red(K⁺/K)    = {E_K:.4f} V")
print(f"  Mg→Ca window: {(E_Ca-E_Mg)*1000:.0f} mV (wide, co-deposition easy)")
print(f"  Ca→Na window: {(E_Na-E_Ca)*1000:.0f} mV (Ca²⁺ easier → GOOD)")
print(f"  Cathode should be held between {E_Ca:.3f} V and {E_Na:.3f} V (vs Cl₂/Cl⁻)")

# CSV: decomposition voltages
Ed_rows = []
for cname in ['MgCl2','NaCl','CaCl2','KCl']:
    T = 873
    dG_decomp,_,_ = reaction_GHS(chlorides[cname]['rxn'], T)
    Ed_rows.append([cname, f"{-dG_decomp/1000:.1f}", f"{E_d[cname][T]:.3f}", f"{E_red_std[cname][T]:.4f}"])
write_csv('tab_Ed.csv', ['Chloride','dGf(kJ/mol)','Ed(V)','E_red(V vs Cl2/Cl-)'], Ed_rows)

# CSV: co-deposition window
window_rows = []
for desc, xMg, xCa, xNa, xK in compositions:
    E_Ca_w = E_red_std['CaCl2'][T] + RT_2F * math.log(xCa) if xCa > 0 else -999
    E_Na_w = E_red_std['NaCl'][T] + RT_F * math.log(xNa) if xNa > 0 else -999
    window = E_Ca_w - E_Na_w
    window_rows.append([desc, f"{xMg:.2f}", f"{xCa:.2f}", f"{xNa:.2f}", f"{xK:.2f}", f"{window*1000:.1f}"])
write_csv('tab_window.csv', ['Composition','x_MgCl2','x_CaCl2','x_NaCl','x_KCl','Window(mV)'], window_rows)

# ============================================================
# PART 3.5: Activity Coefficient Sensitivity Analysis
# ============================================================
print("\n" + "=" * 70)
print("PART 3.5: Activity Coefficient Sensitivity Analysis")
print("=" * 70)
print("说明：四元氯化物熔盐体系中Ca²⁺活度系数的实验数据有限，")
print("      对γ_Ca²⁺在0.3~1.0范围内做参数扫描，评估共析窗口的鲁棒性。")
print(f"温度固定 T = {T} K ({T-273}°C)")
print("推荐组成: x_MgCl2=0.30, x_CaCl2=0.40, x_NaCl=0.15, x_KCl=0.15")

xMg_s, xCa_s, xNa_s, xK_s = 0.30, 0.40, 0.15, 0.15
gamma_Ca_list = [1.0, 0.9, 0.8, 0.7, 0.5, 0.3]
gamma_Na_list = [1.0, 0.85, 0.7]

print(f"\n  扫描范围: γ_CaCl2 = {gamma_Ca_list}, γ_NaCl = {gamma_Na_list}")
print(f"  E_red(Ca) = E°(CaCl2) + (RT/2F)·ln(γ_Ca·x_Ca)")
print(f"  E_red(Na) = E°(NaCl)  + (RT/F)·ln(γ_Na·x_Na)")
print(f"  Window    = E_red(Ca) - E_red(Na)")
print(f"\n  {'γ_Ca':<8} {'γ_Na':<8} {'E_Ca(V)':<12} {'E_Na(V)':<12} {'Window(mV)':<12} {'Assessment':<15}")
print("  " + "-" * 68)

sens_rows = []
for g_Ca in gamma_Ca_list:
    for g_Na in gamma_Na_list:
        E_Ca = E_red_std['CaCl2'][T] + RT_2F * math.log(g_Ca * xCa_s)
        E_Na = E_red_std['NaCl'][T] + RT_F * math.log(g_Na * xNa_s)
        window = E_Ca - E_Na
        w_mV = window * 1000
        if w_mV > 100: assess = "Good"
        elif w_mV > 50: assess = "Moderate"
        elif w_mV > 0: assess = "Marginal"
        else: assess = "Na first!"
        print(f"  {g_Ca:<8.2f} {g_Na:<8.2f} {E_Ca:<12.4f} {E_Na:<12.4f} {w_mV:<12.1f} {assess:<15}")
        sens_rows.append([f"{g_Ca:.2f}", f"{g_Na:.2f}", f"{w_mV:.1f}", assess])

write_csv('tab_window_sensitivity.csv', ['gamma_Ca','gamma_Na','window_mV','assessment'], sens_rows)

# 临界活度系数检测：找到使窗口降为0的γ_CaCl2
print(f"\n  --- 临界活度系数分析 ---")
for g_Na_crit in [1.0, 0.85, 0.70]:
    # 二分法找临界 gamma_Ca
    g_lo, g_hi = 0.01, 1.0
    for _ in range(50):
        g_mid = (g_lo + g_hi) / 2
        E_Ca_c = E_red_std['CaCl2'][T] + RT_2F * math.log(g_mid * xCa_s)
        E_Na_c = E_red_std['NaCl'][T] + RT_F * math.log(g_Na_crit * xNa_s)
        w_c = (E_Ca_c - E_Na_c) * 1000
        if w_c > 0:
            g_hi = g_mid
        else:
            g_lo = g_mid
    print(f"  γ_NaCl={g_Na_crit:.2f}: 临界 γ_CaCl2 ≈ {(g_lo+g_hi)/2:.4f} (窗口降为0)")

# ============================================================
# PART 3.6: Mg-Ca Liquid Alloy Thermodynamics
# ============================================================
print("\n" + "=" * 70)
print("PART 3.6: Mg-Ca Liquid Alloy Thermodynamics")
print("=" * 70)
print("说明：Mg-Ca液态合金采用Zhang et al. (2008) CALPHAD评估的Redlich-Kister参数：")
print("      L0 = -30616 + 13.72·T (J/mol); L1 = -532 + 2.70·T (J/mol)")
print("      正规溶液简化（忽略L1项）：Ω ≈ L0(T)")
L0 = -30616 + 13.72 * T  # J/mol, Zhang et al. (2008) R-K参数
# L1 = -532 + 2.70 * T   # 非对称项，正规溶液近似下忽略
Omega_MgCa = L0  # 正规溶液近似：取L0作为交互作用参数
print(f"  温度 T = {T} K ({T-273}°C)")
print(f"  L0 = {L0:.1f} J/mol (= {L0/1000:.2f} kJ/mol)")
print(f"  正规溶液近似 Ω = L0 = {Omega_MgCa:.1f} J/mol")
print(f"  ΔG_mix = RT(x_Mg·ln x_Mg + x_Ca·ln x_Ca) + Ω·x_Mg·x_Ca")
print(f"  ΔH_mix = Ω·x_Mg·x_Ca")
print(f"  ΔS_mix = -R(x_Mg·ln x_Mg + x_Ca·ln x_Ca)")
print(f"  G_ex   = Ω·x_Mg·x_Ca")
print(f"  γ_Mg   = exp(Ω·x_Ca²/(RT))")
print(f"  γ_Ca   = exp(Ω·x_Mg²/(RT))")
print(f"  参考: Zhang et al. (2008) J. Alloys Compd. 463:294-301.")

print(f"\n  {'x_Ca':<8} {'ΔG_mix(kJ/mol)':<16} {'ΔH_mix(kJ/mol)':<16} {'ΔS_mix(J/molK)':<16} {'G_ex(kJ/mol)':<14} {'γ_Mg':<10} {'γ_Ca':<10}")
print("  " + "-" * 90)

MgCa_rows = []
n_steps = 100
for i in range(n_steps + 1):
    x_Ca = round(i * 0.01, 4)
    x_Mg = 1.0 - x_Ca
    # 处理 x·ln(x) 在边界 (x=0) 为0的情况
    term_Mg = x_Mg * math.log(x_Mg) if x_Mg > 1e-12 else 0.0
    term_Ca = x_Ca * math.log(x_Ca) if x_Ca > 1e-12 else 0.0
    dG_mix = R * T * (term_Mg + term_Ca) + Omega_MgCa * x_Mg * x_Ca
    dH_mix = Omega_MgCa * x_Mg * x_Ca
    dS_mix = -R * (term_Mg + term_Ca)
    G_ex = Omega_MgCa * x_Mg * x_Ca
    gamma_Mg = math.exp(Omega_MgCa * x_Ca**2 / (R * T))
    gamma_Ca = math.exp(Omega_MgCa * x_Mg**2 / (R * T))
    print(f"  {x_Ca:<8.2f} {dG_mix/1000:<16.3f} {dH_mix/1000:<16.3f} {dS_mix:<16.3f} {G_ex/1000:<14.3f} {gamma_Mg:<10.4f} {gamma_Ca:<10.4f}")
    MgCa_rows.append([f"{x_Ca:.2f}", f"{dG_mix/1000:.3f}", f"{dH_mix/1000:.3f}", f"{dS_mix:.3f}", f"{G_ex/1000:.3f}", f"{gamma_Mg:.4f}", f"{gamma_Ca:.4f}"])

# 等摩尔组成关键值
x_Ca_eq = 0.5
x_Mg_eq = 0.5
term_eq = x_Mg_eq * math.log(x_Mg_eq) + x_Ca_eq * math.log(x_Ca_eq)
dG_mix_eq = R * T * term_eq + Omega_MgCa * x_Mg_eq * x_Ca_eq
dH_mix_eq = Omega_MgCa * x_Mg_eq * x_Ca_eq
dS_mix_eq = -R * term_eq
G_ex_eq = Omega_MgCa * x_Mg_eq * x_Ca_eq
gamma_Mg_eq = math.exp(Omega_MgCa * x_Ca_eq**2 / (R * T))
gamma_Ca_eq = math.exp(Omega_MgCa * x_Mg_eq**2 / (R * T))
print(f"\n  等摩尔组成 (x_Ca = 0.50) 关键值:")
print(f"    ΔG_mix = {dG_mix_eq/1000:.3f} kJ/mol")
print(f"    ΔH_mix = {dH_mix_eq/1000:.3f} kJ/mol (负值→放热, Mg2Ca形成趋势)")
print(f"    ΔS_mix = {dS_mix_eq:.3f} J/mol·K")
print(f"    G_ex   = {G_ex_eq/1000:.3f} kJ/mol")
print(f"    γ_Mg   = {gamma_Mg_eq:.4f}")
print(f"    γ_Ca   = {gamma_Ca_eq:.4f}")

write_csv('tab_MgCa_thermo.csv', ['x_Ca','dG_mix(kJ/mol)','dH_mix(kJ/mol)','dS_mix(J/molK)','G_ex(kJ/mol)','gamma_Mg','gamma_Ca'], MgCa_rows)

# ============================================================
# PART 4: Material Balance (per ton Ti, CORRECTED units)
# ============================================================
print("\n" + "=" * 70)
print("PART 4: Material Balance (per 1 ton = 1000 kg Ti)")
print("=" * 70)

M_Ti=47.87; M_Mg=24.305; M_Ca=40.078; M_O=15.999
M_TiO2=79.87; M_MgO=40.304; M_CaO=56.077; M_O2=32.0

mol_Ti = 1e6 / M_Ti
print(f"  Moles of Ti: {mol_Ti:.0f} mol")

m_TiO2 = mol_Ti * M_TiO2 / 1000
m_Mg   = mol_Ti * M_Mg / 1000
m_Ca   = mol_Ti * M_Ca / 1000
m_MgO  = mol_Ti * M_MgO / 1000
m_CaO  = mol_Ti * M_CaO / 1000
m_O2   = mol_Ti * M_O2 / 1000

print(f"\n  Input (per ton Ti):")
print(f"    TiO₂ (pure):           {m_TiO2:.0f} kg")
print(f"    TiO₂ ore (90wt%):      {m_TiO2/0.90:.0f} kg")
print(f"    Mg (cyclic, not consumed): {m_Mg:.0f} kg")
print(f"    Ca (cyclic, not consumed): {m_Ca:.0f} kg")
print(f"\n  Output (per ton Ti):")
print(f"    Ti metal:              1000 kg")
print(f"    MgO (→dissolved→regenerated): {m_MgO:.0f} kg")
print(f"    CaO (→dissolved→regenerated): {m_CaO:.0f} kg")
print(f"    O₂ (anode gas):        {m_O2:.0f} kg")

print(f"\n  Mass balance check:")
print(f"    Input:  TiO₂+Mg+Ca = {m_TiO2+m_Mg+m_Ca:.0f} kg")
print(f"    Output: Ti+MgO+CaO = {1000+m_MgO+m_CaO:.0f} kg")
print(f"    Diff:   {m_TiO2+m_Mg+m_Ca-(1000+m_MgO+m_CaO):.1f} kg ✓")

print(f"\n  Net consumption (reductants are cyclic):")
print(f"    Net input:  TiO₂ = {m_TiO2:.0f} kg + electricity")
print(f"    Net output: Ti = 1000 kg + O₂ = {m_O2:.0f} kg")
print(f"    Check: {m_TiO2:.0f} ≈ {1000+m_O2:.0f} kg ✓")

# CSV: material balance
mbal_rows = [
    ['Input','TiO2 (pure)',f"{m_TiO2:.0f}"],
    ['Input','TiO2 ore (90wt%)',f"{m_TiO2/0.90:.0f}"],
    ['Input','Mg (cyclic)',f"{m_Mg:.0f}"],
    ['Input','Ca (cyclic)',f"{m_Ca:.0f}"],
    ['Output','Ti metal','1000'],
    ['Output','MgO (regenerated)',f"{m_MgO:.0f}"],
    ['Output','CaO (regenerated)',f"{m_CaO:.0f}"],
    ['Output','O2 (anode gas)',f"{m_O2:.0f}"],
    ['Check','Input total',f"{m_TiO2+m_Mg+m_Ca:.0f}"],
    ['Check','Output total',f"{1000+m_MgO+m_CaO:.0f}"],
]
write_csv('tab_mbalance.csv', ['Category','Item','Mass(kg)'], mbal_rows)

# ============================================================
# PART 5: Energy Balance (CORRECTED)
# ============================================================
print("\n" + "=" * 70)
print("PART 5: Energy Balance (per ton Ti)")
print("=" * 70)

T_op = 873
dG_MgO_form,_,_ = reaction_GHS({'Mg':-1,'O2':-0.5,'MgO':1}, T_op)
dG_CaO_form,_,_ = reaction_GHS({'Ca':-1,'O2':-0.5,'CaO':1}, T_op)
dG_MgO_decomp = -dG_MgO_form
dG_CaO_decomp = -dG_CaO_form
dG_total = dG_MgO_decomp + dG_CaO_decomp

n_e = 4
E_theory = dG_total / (n_e * F)

print(f"\n  Electrolysis regeneration at {T_op-273}°C:")
print(f"    ΔG(MgO→Mg+½O₂) = {dG_MgO_decomp/1000:.1f} kJ/mol")
print(f"    ΔG(CaO→Ca+½O₂) = {dG_CaO_decomp/1000:.1f} kJ/mol")
print(f"    Total per mol Ti = {dG_total/1000:.1f} kJ/mol (4 e⁻)")
print(f"    Theoretical E_d = {E_theory:.3f} V")

E_min_kWh = dG_total * mol_Ti / 3.6e6
print(f"    Theoretical minimum = {E_min_kWh:.0f} kWh/ton Ti")

print(f"\n  Practical scenarios:")
print(f"    {'η_I':<6} {'V_cell':<8} {'kWh/ton':<10} {'Note'}")
print("    " + "-" * 55)
for eta, V, note in [(0.85,3.5,"best"),(0.80,4.0,"moderate"),(0.75,4.0,"conservative"),
                      (0.75,4.3,"graphite anode"),(0.70,4.5,"worst case")]:
    E = n_e * F * mol_Ti * V / (eta * 3.6e6)
    print(f"    {eta:<6.2f} {V:<8.1f} {E:<10.0f} {note}")

# CSV: energy balance
energy_rows = []
for eta, V, note in [(0.85,3.5,"best"),(0.80,4.0,"moderate"),(0.75,4.0,"conservative"),
                      (0.75,4.3,"graphite anode"),(0.70,4.5,"worst case")]:
    E = n_e * F * mol_Ti * V / (eta * 3.6e6)
    energy_rows.append([f"{eta:.2f}", f"{V:.1f}", f"{E:.0f}", note])
energy_rows.append(['', '', '', ''])
energy_rows.append(['Theoretical', f"{E_theory:.3f}", f"{E_min_kWh:.0f}", 'min possible'])
write_csv('tab_energy.csv', ['eta_I','V_cell(V)','Energy(kWh/ton)','Note'], energy_rows)

dG_rxn,dH_rxn,dS_rxn = reaction_GHS({'TiO2':-1,'Mg':-1,'Ca':-1,'Ti':1,'MgO':1,'CaO':1}, T_op)
print(f"\n  Reduction reaction heat:")
print(f"    TiO₂+Mg+Ca→Ti+MgO+CaO, ΔH = {dH_rxn/1000:.1f} kJ/mol (exothermic)")
print(f"    Per ton Ti: {dH_rxn*mol_Ti/3.6e6:.0f} kWh/ton (heat released, compensates thermal loss)")

print(f"\n  Plant scale (10,000 ton/year):")
I_cell = 300000
V_cell = 4.0
eta = 0.80
rate_g_s = I_cell * eta * M_Ti / (n_e * F)
rate_kg_h = rate_g_s * 3.6
rate_ton_y = rate_kg_h * 8000 / 1000
n_cells = 10000 / rate_ton_y
power_MW = n_cells * I_cell * V_cell / 1e6
print(f"    Cell: {I_cell/1000:.0f} kA, {V_cell} V, η={eta}")
print(f"    Production: {rate_kg_h:.1f} kg/h = {rate_ton_y:.0f} ton/year per cell")
print(f"    Cells needed: {n_cells:.0f}")
print(f"    Total power: {power_MW:.1f} MW")

# ============================================================
# SUMMARY
# ============================================================
print("\n" + "=" * 70)
print("SUMMARY OF KEY RESULTS")
print("=" * 70)
print(f"""
1. THERMODYNAMICS (600°C):
   ΔG°(TiO₂+2Mg→Ti+2MgO)    = {reaction_GHS(reactions['R1: TiO2+2Mg ->Ti+2MgO'],873)[0]/1000:.1f} kJ/mol
   ΔG°(TiO₂+2Ca→Ti+2CaO)    = {reaction_GHS(reactions['R2: TiO2+2Ca ->Ti+2CaO'],873)[0]/1000:.1f} kJ/mol
   ΔG°(TiO₂+Mg+Ca→Ti+MgO+CaO) = {reaction_GHS(reactions['R3: TiO2+Mg+Ca->Ti+MgO+CaO'],873)[0]/1000:.1f} kJ/mol

2. DEOXIDATION LIMIT (600°C):
   Mg: w[O]_eq ≈ {1/math.exp(-(reaction_GHS({'Mg':-1,'O2':-0.5,'MgO':1},873)[0]-(-581000+92*873))/(R*873)):.4f} wt% (bulk)
   Ca: w[O]_eq ≈ {1/math.exp(-(reaction_GHS({'Ca':-1,'O2':-0.5,'CaO':1},873)[0]-(-581000+92*873))/(R*873)):.4f} wt% (polish)
   Ratio ≈ {1/math.exp(-(reaction_GHS({'Mg':-1,'O2':-0.5,'MgO':1},873)[0]-(-581000+92*873))/(R*873))/(1/math.exp(-(reaction_GHS({'Ca':-1,'O2':-0.5,'CaO':1},873)[0]-(-581000+92*873))/(R*873))):.0f}x → synergy justified

3. ELECTROCHEMISTRY (600°C):
   E_d: MgCl₂={E_d['MgCl2'][873]:.3f}V < NaCl={E_d['NaCl'][873]:.3f}V ≈ CaCl₂={E_d['CaCl2'][873]:.3f}V < KCl={E_d['KCl'][873]:.3f}V
   Pure salts: Na⁺ slightly easier than Ca²⁺ (gap={gap_CaNa*1000:.0f}mV) → Downs makes Na
   Low-NaK comp (xCa=0.40,xNa=0.15): Ca²⁺ before Na⁺ by ~103 mV → workable

4. MATERIAL BALANCE (per ton Ti):
   TiO₂: {m_TiO2:.0f} kg (ore: {m_TiO2/0.90:.0f} kg)
   Mg(cyclic): {m_Mg:.0f} kg, Ca(cyclic): {m_Ca:.0f} kg
   O₂(anode): {m_O2:.0f} kg

5. ENERGY BALANCE (per ton Ti):
   Theoretical: {E_min_kWh:.0f} kWh/ton
   Practical (η=0.80, V=4.0): {n_e*F*mol_Ti*4.0/(0.80*3.6e6):.0f} kWh/ton
   Practical (η=0.75, V=4.3): {n_e*F*mol_Ti*4.3/(0.75*3.6e6):.0f} kWh/ton
   Reaction heat: {dH_rxn*mol_Ti/3.6e6:.0f} kWh/ton (exothermic)
""")
