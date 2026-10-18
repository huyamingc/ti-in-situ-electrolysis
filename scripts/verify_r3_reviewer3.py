"""Verification of Reviewer 3's objection for JES-117547:
   "Coexistence of Mg and Ca does not work effectively ... MgO can be reduced by Ca."

Reuses the same Barin/Kubaschewski data and Meyer-Kelly Cp model as
scripts/thermo_calc_v2.py so the numbers are directly comparable with the
manuscript tables. Read-only with respect to the manuscript.
"""
import math
import os
import csv

R = 8.314
F = 96485.0
T = 873.15          # 600 C
M_Ti = 47.867       # g/mol

species = {
    'TiO2':  {'Hf': -944000, 'S': 50.6,  'Cp_a': 62.834, 'Cp_b': 11.882e-3, 'Cp_c': -9.782e5},
    'MgO':   {'Hf': -601600, 'S': 26.9,  'Cp_a': 48.982, 'Cp_b': 3.142e-3,  'Cp_c': -11.740e5},
    'CaO':   {'Hf': -635100, 'S': 39.7,  'Cp_a': 49.622, 'Cp_b': 4.519e-3,  'Cp_c': -6.945e5},
    'Ti':    {'Hf': 0,       'S': 30.7,  'Cp_a': 22.09,  'Cp_b': 10.46e-3,  'Cp_c': 0.0},
    'Mg':    {'Hf': 0,       'S': 32.7,  'Cp_a': 22.09,  'Cp_b': 10.46e-3,  'Cp_c': -0.418e5},
    'Ca':    {'Hf': 0,       'S': 41.6,  'Cp_a': 25.29,  'Cp_b': 3.85e-3,   'Cp_c': 0.0},
    'O2':    {'Hf': 0,       'S': 205.2, 'Cp_a': 29.96,  'Cp_b': 4.18e-3,   'Cp_c': -1.67e5},
}
transitions = {
    'Mg': {'Tm': 923,  'Hfus': 8950, 'Cp_l': 32.7},
    'Ca': {'Tm': 1115, 'Hfus': 8540, 'Cp_l': 30.0},
}


def get_H_S(name, T):
    sp = species[name]
    a, b, c = sp['Cp_a'], sp['Cp_b'], sp['Cp_c']
    T_ref = 298.0
    H, S = sp['Hf'], sp['S']
    tr = transitions.get(name)
    if tr and T > tr['Tm']:
        Tm = tr['Tm']
        H += a * (Tm - T_ref) + b / 2 * (Tm**2 - T_ref**2) - c * (1 / Tm - 1 / T_ref)
        S += a * math.log(Tm / T_ref) + b * (Tm - T_ref) - c / 2 * (1 / Tm**2 - 1 / T_ref**2)
        H += tr['Hfus']
        S += tr['Hfus'] / Tm
        H += tr['Cp_l'] * (T - Tm)
        S += tr['Cp_l'] * math.log(T / Tm)
    else:
        H += a * (T - T_ref) + b / 2 * (T**2 - T_ref**2) - c * (1 / T - 1 / T_ref)
        S += a * math.log(T / T_ref) + b * (T - T_ref) - c / 2 * (1 / T**2 - 1 / T_ref**2)
    return H, S


def reaction_GHS(rxn, T):
    dH = sum(c * get_H_S(n, T)[0] for n, c in rxn.items())
    dS = sum(c * get_H_S(n, T)[1] for n, c in rxn.items())
    return dH - T * dS, dH, dS


rows = []
print("=" * 78)
print("R3 CORE OBJECTION:  Ca + MgO -> CaO + Mg   (600 C, standard states)")
print("=" * 78)

dG_ex, dH_ex, dS_ex = reaction_GHS({'Ca': -1, 'MgO': -1, 'CaO': 1, 'Mg': 1}, T)
dG_R1 = reaction_GHS({'TiO2': -1, 'Mg': -2, 'Ti': 1, 'MgO': 2}, T)[0]
dG_R2 = reaction_GHS({'TiO2': -1, 'Ca': -2, 'Ti': 1, 'CaO': 2}, T)[0]
dG_comb = (dG_R2 - dG_R1) / 2.0
print(f"  direct:                dG = {dG_ex/1000:+.1f} kJ/mol  "
      f"(dH = {dH_ex/1000:+.1f}, dS = {dS_ex:+.1f} J/mol/K)")
print(f"  from manuscript R1-R2: dG = {dG_comb/1000:+.1f} kJ/mol  "
      f"(R1 = {dG_R1/1000:+.1f}, R2 = {dG_R2/1000:+.1f})")
print("  -> Ca does reduce MgO; the objection is CORRECT and the paper's own")
print("     Table 2 already contains the evidence (difference of two lines).")

K2 = math.exp(-dG_ex / (R * T))
print(f"\n  K2 = a_CaO*a_Mg /(a_Ca*a_MgO) = {K2:,.0f}")
print(f"  MgO is unstable whenever a_Mg/a_Ca < {K2:,.0f} x (a_MgO/a_CaO).")
rows.append(['dG(Ca+MgO->CaO+Mg) at 600 C, kJ/mol', f'{dG_ex/1000:.2f}',
             f'{dG_comb/1000:.2f}', 'reviewer 3 correct; both routes agree'])

print("\n" + "=" * 78)
print("CONSEQUENCE 1: which oxide must the electrolysis regenerate?")
print("=" * 78)
dGf_MgO = reaction_GHS({'Mg': -1, 'O2': -0.5, 'MgO': 1}, T)[0]
dGf_CaO = reaction_GHS({'Ca': -1, 'O2': -0.5, 'CaO': 1}, T)[0]
for nm, dGf in [('MgO', dGf_MgO), ('CaO', dGf_CaO)]:
    print(f"  {nm}: dGf(873 K) = {dGf/1000:+7.1f} kJ/mol   Ed = {-dGf/(2*F):.3f} V")
mix_Ed = -(dGf_MgO + dGf_CaO) / (4 * F)
cao_Ed = -2 * dGf_CaO / (4 * F)
print(f"  manuscript mixed regeneration   Ed = {mix_Ed:.3f} V  (paper: 2.73 V)")
print(f"  all-CaO regeneration            Ed = {cao_Ed:.3f} V  ({1000*(cao_Ed-mix_Ed):+.0f} mV)")

n_Ti = 1.0e6 / M_Ti


def W(V, eta=0.75):
    return 4 * F * n_Ti * V / (eta * 3.6e6)


V_cao = 4.10 + (cao_Ed - mix_Ed)
print(f"\n  gross energy, eta = 0.75:  mixed V = 4.10 V -> {W(4.10):,.0f} kWh/t (paper 12,244)")
print(f"                             all-CaO V = {V_cao:.2f} V -> {W(V_cao):,.0f} kWh/t "
      f"({100*(W(V_cao)/W(4.10)-1):+.1f}%)")

print("\n" + "=" * 78)
print("CONSEQUENCE 2: deoxidation limits (wt% -> ppm is x1e4, alloy divides by a_M)")
print("=" * 78)
dG_diss = -581000 + 92 * T
aM = 0.263
for nm, dGf in [('Mg', dGf_MgO), ('Ca', dGf_CaO)]:
    dG_deox = dGf - dG_diss
    w_pure = 1.0 / math.exp(-dG_deox / (R * T))          # wt fraction
    w_alloy = w_pure / aM
    print(f"  {nm}: dG_deox = {dG_deox/1000:+.1f} kJ/mol   "
          f"w[O] = {w_pure*1e4:8,.0f} ppm (a_M=1)   {w_alloy*1e4:9,.0f} ppm (a_M=0.263)")
print("  (matches Table 4: 3908 / 14859 ppm for Mg, 20.2 / 76.8 ppm for Ca)")

print("\n  Competition at the deep-deoxidation front, Ca + [O] vs Ca + MgO:")
dG_deox_Ca = dGf_CaO - dG_diss
dG_deox_Mg = dGf_MgO - dG_diss
w_cross = math.exp(-(dG_ex - dG_deox_Ca) / (R * T))      # wt% numeric
print(f"    Ca + [O] wins only while w[O] > {w_cross:.4f} wt% = {w_cross*1e4:,.0f} ppm")
print(f"    (identity: this crossover equals the Mg-only deoxidation limit,")
print(f"     {math.exp(dG_deox_Mg/(R*T))*1e4:,.0f} ppm, because dG(Ca+MgO->CaO+Mg) - dG_deox(Ca)"
      f" = -dG_deox(Mg))")
print("    Below that, Ca preferentially reduces dissolved MgO, NOT the residual")
print("    oxygen in Ti.  Deep deoxidation therefore requires the dissolved MgO")
print("    activity to be kept below a threshold:")
for w_ppm in (77, 20):
    w = w_ppm * 1e-4
    a_MgO_max = (math.exp(-dG_deox_Ca / (R * T)) / K2) * w * aM
    print(f"      to reach {w_ppm:3d} ppm O in Ti:  a_MgO < {a_MgO_max:.2e}")
print("    -> the design must specify a melt-cleanup / MgO-activity floor; this is a")
print("       NEW quantitative design constraint that the manuscript does not state.")
rows.append(['a_MgO ceiling for 77 ppm O (Ca-couple)', 'see text', '-',
             'new constraint forced by R3 objection'])

print("\n" + "=" * 78)
print("CONSEQUENCE 3: why keep Mg at all?  (melting-point / phase argument)")
print("=" * 78)
print("  pure Ca  Tm = 1115 K = 842 C -> SOLID at the 600 C design point")
print("  pure Mg  Tm =  923 K = 650 C -> solid at 600 C as well")
print("  Mg-Ca eutectic ~517 C        -> LIQUID at 600 C")
print("  => Mg's defensible role is making the reductant liquid at 600 C (and")
print("     carrying the electrodeposition), not a 'faster Mg reduction kinetics'.")

print("\n" + "=" * 78)
print("CONSEQUENCE 4: material balance if CaO is the sole oxygen carrier")
print("=" * 78)
M_CaO, M_Ca, M_MgO = 56.077, 40.078, 40.304
mol_Ti = 1.0e6 / M_Ti
kg_CaO = 2 * mol_Ti * M_CaO / 1000
kg_Ca = 2 * mol_Ti * M_Ca / 1000
kg_MgO = mol_Ti * M_MgO / 1000
print(f"  paper (mixed): MgO {kg_MgO:,.0f} + CaO {kg_CaO/2:,.0f} = {kg_MgO+kg_CaO/2:,.0f} kg")
print(f"  all-CaO:       CaO {kg_CaO:,.0f} kg  (circulating Ca {kg_Ca:,.0f} kg)")
print("  Charge transferred is unchanged (4 e-/Ti): the energy penalty is only the")
print(f"  {1000*(cao_Ed-mix_Ed):+.0f} mV decomposition shift shown above (~+2.4%).")
print("  UPSIDE: CaO solubility in CaCl2 is much higher than MgO solubility, so the")
print("  closed loop is EASIER under the CaO-only picture.  Re-framing is feasible.")

print("\n" + "=" * 78)
print("CONSEQUENCE 5: reductant flux per tonne Ti under three mechanism pictures")
print("=" * 78)
M_Mg = 24.305
mol_O_total = mol_Ti * 2.0                     # 668 kg O per tonne Ti
w_Mg_limit = math.exp(dG_deox_Mg / (R * T)) / 100.0   # fractional, 0.00391 (O/Ti)
w_target = 77e-6                                      # fractional, alloy-corrected Ca endpoint


def o_mass(w):
    """kg O still dissolved in 1 t Ti for a given w[O] (O/Ti mass ratio)."""
    return 1000.0 * w


O_mg = o_mass(66.8e-2) - o_mass(w_Mg_limit)    # O removed by Mg in picture B
O_ca = o_mass(w_Mg_limit) - o_mass(w_target)   # O removed by Ca in picture B
print(f"  picture A (manuscript, 1 Mg + 1 Ca per mol O):  Mg  508 kg + Ca  837 kg")
print(f"  picture B (sequential, Mg down to its limit):   Mg {O_mg/16*M_Mg:,.0f} kg "
      f"+ Ca {O_ca/16*40.078:,.0f} kg")
print(f"  picture C (CaO sole carrier, Mg recycled):      Mg    0 kg + Ca "
      f"{mol_O_total*40.078/1000:,.0f} kg  (CaO {mol_O_total*M_CaO/1000:,.0f} kg)")
print("  The manuscript's 1:1 table sits between B and C and is not the")
print("  thermodynamically selected state: K2 = 194 pushes the system toward C.")
rows.append(['reductant flux A (paper), kg Mg / kg Ca', '508 / 837', '-', '1:1 assumption'])
rows.append(['reductant flux B (sequential), kg Mg / kg Ca',
             f'{O_mg/16*M_Mg:.0f} / {O_ca/16*40.078:.0f}', '-', 'Mg to its own limit, then Ca'])
rows.append(['reductant flux C (CaO sole carrier), kg Mg / kg Ca',
             f'0 / {mol_O_total*40.078/1000:.0f}', '-', 'Mg only a liquid carrier'])

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'output', 'tab_r3_verification.csv')
os.makedirs(os.path.dirname(out), exist_ok=True)
with open(out, 'w', newline='', encoding='utf-8-sig') as f:
    wr = csv.writer(f)
    wr.writerow(['quantity', 'value', 'cross-check', 'note'])
    wr.writerows(rows)
print(f"\n  -> CSV saved: {os.path.normpath(out)}")
