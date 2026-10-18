"""Numbers required by the R3-1 mechanism reconstruction (JES-117547).

Physical picture after the reconstruction:
  * Ca is the ONLY net oxygen carrier: every O leaves the reduction step as CaO,
    because Ca + MgO -> CaO + Mg (dG = -38.2 kJ/mol, K2 = 194) makes MgO unstable
    whenever Ca is present.
  * Mg is the liquid carrier / oxygen shuttle: pure Ca (842 C) and pure Mg (650 C)
    are both SOLID at 600 C; only the Mg-Ca alloy (eutectic ~517 C) is liquid.
  * The electrolysis therefore regenerates CaO, not a MgO+CaO mixture.

This script recomputes every headline number that the reconstruction moves.
"""
import math
import os
import csv

R = 8.314
F = 96485.0
T = 873.15
M_Ti = 47.867
n_Ti = 1.0e6 / M_Ti          # mol Ti per tonne

# --- Gibbs energies of formation at 873 K, from scripts/thermo_calc_v2.py data ---
dGf_CaO = -545700.0          # J/mol
dGf_MgO = -507500.0          # J/mol
dG_diss = -581000.0 + 92.0 * T   # O in alpha-Ti, 1 wt% Henry standard state

print("=" * 80)
print("1. DECOMPOSITION VOLTAGE: which oxide is actually regenerated?")
print("=" * 80)
Ed_MgO = -dGf_MgO / (2 * F)
Ed_CaO = -dGf_CaO / (2 * F)
Ed_mix = -(dGf_MgO + dGf_CaO) / (4 * F)
Ed_new = 2 * (-dGf_CaO) / (4 * F)
print(f"  MgO only            Ed = {Ed_MgO:.3f} V")
print(f"  CaO only            Ed = {Ed_CaO:.3f} V   <-- reconstruction")
print(f"  MgO+CaO (manuscript) Ed = {Ed_mix:.3f} V  (paper quotes 2.73 V)")
print(f"  manuscript theoretical electrolysis minimum = "
      f"{(dGf_MgO+dGf_CaO)*(-1)*n_Ti/3.6e6:,.0f} kWh/ton")
print(f"  reconstruction theoretical minimum         = "
      f"{2*(-dGf_CaO)*n_Ti/3.6e6:,.0f} kWh/ton")

print("\n" + "=" * 80)
print("2. HEADLINE ENERGY NUMBERS (eta_I = 0.75, same overpotential budget)")
print("=" * 80)
eta_a, eta_c, IR = 0.30, 0.20, 0.90
V_old, V_new = Ed_mix + eta_a + eta_c + IR, Ed_new + eta_a + eta_c + IR
aux, cool = 350.0, 42.0


def gross(V):
    return 4 * F * n_Ti * V / (0.75 * 3.6e6)


def net(V):
    return gross(V) + aux - cool


rows = []
for tag, V, Wmin in (('manuscript (MgO+CaO)', V_old, (dGf_MgO + dGf_CaO) * -1 * n_Ti / 3.6e6),
                     ('reconstructed (CaO only)', V_new, 2 * -dGf_CaO * n_Ti / 3.6e6)):
    W = gross(V)
    N = net(V)
    print(f"  {tag}")
    print(f"    V_cell = {V:.2f} V   gross = {W:,.0f} kWh/t   net = {N:,.0f} kWh/t")
    print(f"    process energy efficiency (step minimum / net) = {100*Wmin/N:.1f} %")
    print(f"    second-law efficiency (4550 / net)            = {100*4550/N:.1f} %")
    print(f"    electrolysis share = {100*W/(W+aux):.1f} %")
    rows.append([tag, f'{V:.2f}', f'{W:.0f}', f'{N:.0f}',
                 f'{100*Wmin/N:.1f}', f'{100*4550/N:.1f}', f'{100*W/(W+aux):.1f}'])
delta = net(V_new) - net(V_old)
print(f"\n  => reconstruction cost: {delta:+,.0f} kWh/ton-Ti "
      f"({100*delta/net(V_old):+.1f}%) -- the energy conclusion (better than FFC's")
print("     15,000-20,000 kWh/ton) is untouched.")

print("\n" + "=" * 80)
print("3. MATERIAL BALANCE under the reconstructed picture")
print("=" * 80)
M_Ca, M_Mg, M_O, M_CaO = 40.078, 24.305, 16.00, 56.077
mol_O = 2 * n_Ti                      # 668 kg O per tonne Ti
kg_O = mol_O * M_O / 1000
kg_Ca_net = mol_O * M_Ca / 1000        # Ca oxidised to CaO (net carrier)
kg_CaO = mol_O * M_CaO / 1000
kg_Mg_shuttle = mol_O * M_Mg / 1000    # Mg oxidised then chemically regenerated
print(f"  net O to remove            : {kg_O:,.0f} kg/ton-Ti")
print(f"  NET carrier  Ca -> CaO     : {kg_Ca_net:,.0f} kg Ca  ->  {kg_CaO:,.0f} kg CaO")
print(f"  SHUTTLED     Mg (net zero) : up to {kg_Mg_shuttle:,.0f} kg Mg cycled through MgO")
print(f"  manuscript table (1:1)     :   508 kg Mg +   837 kg Ca  [to be replaced]")
print(f"  sequential picture (B)     : 1,009 kg Mg +    10 kg Ca  [kinetic extreme]")

print("\n" + "=" * 80)
print("4. THE a_MgO CEILING (new design criterion introduced by the reconstruction)")
print("=" * 80)
dG_open = -38200.0                      # Ca + MgO -> CaO + Mg
K1 = math.exp(-(dGf_CaO - dG_diss) / (R * T))   # Ca + [O] -> CaO
K2 = math.exp(-dG_open / (R * T))
a_Mg = 0.263
for w_ppm, label in ((77, 'equimolar alloy (a_Ca = 0.263)'),
                     (20, 'pure Ca (a_Ca = 1)')):
    w = w_ppm * 1e-4                    # wt% numeric
    aM = 0.263 if w_ppm == 77 else 1.0
    aMgO = (K1 / K2) * w * aM
    print(f"  to reach {w_ppm:3d} ppm O in Ti ({label}):  a_MgO < {aMgO:.2e}")
w_cross = math.exp(((dGf_CaO - dG_diss) - dG_open) / (R * T)) * 1e4
print(f"  identity: the Ca-vs-MgO crossover is at {w_cross:,.0f} ppm")
print("  == the Mg-only deoxidation limit; below it Ca attacks MgO, not the Ti oxygen.")

print("\n" + "=" * 80)
print("5. WHY Mg IS STILL REQUIRED: phase state at 600 C")
print("=" * 80)
print("  pure Ca   Tm = 1115 K = 842 C -> SOLID")
print("  pure Mg   Tm =  923 K = 650 C -> SOLID")
print("  Mg-Ca eutectic ~ 517 C        -> LIQUID (this is the enabler of 600 C operation)")
print(f"  Mg vapour pressure at 600 C   : ~{101325*math.exp(-(128000/R)*(1/873.15-1/1363)):.0f} Pa"
      f"  (~{101325*math.exp(-(128000/R)*(1/873.15-1/1363))/133.322:.1f} Torr)")
print("  -> Mg is lost by evaporation/entrainment and must be replenished; that,")
print("     together with the liquid-carrier function, is the engineering reason to")
print("     keep in-situ Mg-Ca co-deposition in the flowsheet.")

print("\n" + "=" * 80)
print("6. UPSIDE: the old top risk (MgO solubility) softens")
print("=" * 80)
print("  manuscript: closed loop hinges on MgO solubility >= 0.5 wt% at 600 C")
print("  reconstruction: the regenerated species is CaO, whose solubility in CaCl2-rich")
print("  melts is far higher than MgO's; and a LOW MgO solubility is now harmless")
print("  because the design requires a_MgO < 5e-3 (i.e. MgO must NOT accumulate).")

print("\n" + "=" * 80)
print("7. THE HIDDEN SELF-CONSISTENCY TRAP: Mg mass balance vs deposition ratio")
print("=" * 80)
print("  In Regime II (j > j_lim,Mg) the cathode deposits Mg at its diffusion limit and")
print("  Ca with the remainder, so the deposit ratio is fixed by j_lim,Mg/j.")
print("  Total metal deposited per tonne Ti = 2*n_Ti = 2*e- per M2+ = "
      f"{2*n_Ti:,.0f} mol")
met = 2 * n_Ti
c_melt = 1.94e4
D_melt, delta, F_ = 1.0e-9, 200e-6, F


def jlim(x_mg):
    c_b = x_mg * c_melt
    return 2 * F_ * D_melt * c_b / delta / 1e4     # A/cm2


j_op = 1.10
print(f"\n  at the manuscript design point j = {j_op} A/cm2:")
print("  x_MgCl2   j_lim,Mg   Mg share   Mg deposited   Ca deposited   Ca needed*")
for xmg in (0.30, 0.20, 0.15, 0.10, 0.05, 0.02):
    jl = jlim(xmg)
    share = min(jl / j_op, 1.0)
    Mg = met * share * M_Mg / 1000
    Ca = met * (1 - share) * 40.078 / 1000
    print(f"   {xmg:.2f}     {jl:.3f}      {share*100:5.1f}%     {Mg:6.0f} kg       "
          f"{Ca:6.0f} kg      {kg_Ca_net:,.0f} kg")
print("  * Ca needed if Ca is the ONLY net oxygen carrier = 1,675 kg/ton.")
print("\n  => With x_MgCl2 = 0.30 the deposit is ~1:1, giving only ~822 kg Ca per tonne,")
print("     barely half of the 1,675 kg that a Ca-only carrier scheme requires: under the")
print("     'Ca reduces MgO fast' picture the Ca inventory RUNS DOWN.")
print("  => To close a Ca-only scheme the MgCl2 fraction would have to fall to ~0.02")
print("     (Mg share < 4%), which contradicts using MgCl2 as the primary salt.")
print("\n  CONCLUSION: the manuscript's 1:1 material balance is ONLY self-consistent if")
print("  MgO leaves through the electrolytic regeneration path -- i.e. if Ca + MgO ->")
print("  CaO + Mg is KINETICALLY suppressed at the alloy/salt interface.  That kinetic")
print("  suppression, not the thermodynamics, is what the paper must now defend,")
print("  and it is exactly the measurement R2 item 5 asks for.  Otherwise the paper")
print("  must switch to a low-MgCl2, Ca-regeneration design (a different paper).")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'output',
                   'tab_r3_reconstruction.csv')
with open(out, 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.writer(f)
    w.writerow(['scenario', 'V_cell', 'gross_kWh_t', 'net_kWh_t',
                'process_eff_%', 'second_law_%', 'electrolysis_share_%'])
    w.writerows(rows)
print(f"\n  -> CSV saved: {os.path.normpath(out)}")
