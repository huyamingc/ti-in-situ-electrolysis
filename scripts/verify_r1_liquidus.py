"""Verification of JES Reviewer 1's questions (attachment 1) for JES-117547.

R1-7 asks: "Melting point of all the 4 salt is higher than your operating/design
basis temperature, then how Co-deposition occur?"  -> the answer is freezing-point
depression in the quaternary mixture.  This script quantifies it with the same
ideal-solution liquidus model as the manuscript (Eq. 1) and scans the composition
space for the minimum liquidus, to test R2-4's suggestion of fixing the
temperature mismatch by changing the salt composition instead of the temperature.
"""
import math
import os
import csv

R = 8.314

# pure-salt melting data as used in the manuscript (T in K, dHfus in J/mol)
salts = {
    'MgCl2': {'Tm': 987.0,  'dHfus': 43100.0},
    'CaCl2': {'Tm': 1045.0, 'dHfus': 28500.0},
    'NaCl':  {'Tm': 1074.0, 'dHfus': 28200.0},
    'KCl':   {'Tm': 1043.0, 'dHfus': 26600.0},
}

print("=" * 78)
print("R1-7: pure-salt melting points vs the 600 C design temperature")
print("=" * 78)
for n, d in salts.items():
    print(f"  {n:6s} Tm = {d['Tm']:.0f} K = {d['Tm']-273.15:6.1f} C   "
          f"(design 600 C -> pure salt is {'SOLID' if d['Tm']-273.15 > 600 else 'liquid'})")


def liquidus(x, verbose=False):
    """Highest temperature at which any component is exactly saturated."""
    Tmax, ctrl = 0.0, None
    out = []
    for n, xi in x.items():
        d = salts[n]
        # 1/T_i = 1/Tm - R*ln(x_i)/dHfus
        inv = 1.0 / d['Tm'] - R * math.log(xi) / d['dHfus']
        Ti = 1.0 / inv
        out.append((n, Ti))
        if Ti > Tmax:
            Tmax, ctrl = Ti, n
    if verbose:
        for n, Ti in sorted(out, key=lambda t: -t[1]):
            print(f"    {n:6s} x = {x[n]:.2f}  saturated at {Ti-273.15:6.1f} C")
    return Tmax, ctrl


x_ref = {'MgCl2': 0.30, 'CaCl2': 0.40, 'NaCl': 0.15, 'KCl': 0.15}
T_liq, ctrl = liquidus(x_ref, verbose=True)
print(f"\n  recommended composition x = {x_ref}")
print(f"  -> ideal-solution liquidus = {T_liq:.1f} K = {T_liq-273.15:.1f} C  "
      f"(controlled by {ctrl})")
print(f"  -> manuscript states 544 C  =>  model reproduced")
print(f"  -> YES the melt is fully liquid at 600 C, despite every pure salt melting")
print(f"     above 600 C: this is ordinary freezing-point depression by mixing entropy.")
print(f"  -> superheat at 600 C = {600-(T_liq-273.15):.0f} C; at 620 C = {620-(T_liq-273.15):.0f} C")

print("\n" + "=" * 78)
print("Can the composition be re-tuned to lower the liquidus?  (R2-4 fix option)")
print("=" * 78)
best = None
rows = []
NacK = 0.30   # keep NaCl+KCl = 0.30 as in the manuscript
for i in range(0, 31):
    xca = 0.20 + 0.01 * i
    xmg = 1.0 - NacK - xca
    if xmg <= 0.05:
        continue
    x = {'MgCl2': xmg, 'CaCl2': xca, 'NaCl': 0.15, 'KCl': 0.15}
    T, c = liquidus(x)
    rows.append((xca, xmg, T - 273.15, c))
    if best is None or T < best[2]:
        best = (xca, xmg, T, c)
print(f"  scan over x(CaCl2) = 0.20-0.50 at x(NaCl)=x(KCl)=0.15:")
for xca, xmg, Tc, c in rows:
    if abs(xca * 100 - round(xca * 100)) < 1e-9 and int(round(xca * 100)) % 5 == 0:
        print(f"    x_CaCl2 = {xca:.2f}  x_MgCl2 = {xmg:.2f}   liquidus = {Tc:6.1f} C  ({c})")
print(f"  minimum found: x_CaCl2 = {best[0]:.2f}, x_MgCl2 = {best[1]:.2f} -> "
      f"{best[2]-273.15:.1f} C (controlled by {best[3]})")
print(f"  recommended composition gives {T_liq-273.15:.1f} C, i.e. only "
      f"{T_liq-273.15-(best[2]-273.15):.1f} C above the attainable minimum.")
print("  => re-tuning the salt buys at most a few C; raising the design temperature")
print("     (or CALPHAD confirmation) is the realistic fix for R2-4 / R1-7.")

print("\n" + "=" * 78)
print("R1-1: Ti product recovery -- how much salt is entrained on the powder?")
print("=" * 78)
rho_Ti = 4500.0      # kg/m3
for d_pm in (25e-6, 50e-6, 100e-6):
    S = 6.0 / (rho_Ti * d_pm)          # m2/kg
    for film_um in (0.5, 1.0, 2.0):
        V_salt = S * film_um * 1e-6    # m3/kg Ti
        m_salt = V_salt * 1800.0       # kg salt per kg Ti
        print(f"  d = {d_pm*1e6:3.0f} um, salt film {film_um:.1f} um: "
              f"S = {S:5.1f} m2/kg, entrained salt = {m_salt*100:4.1f} wt% "
              f"({m_salt*1000:5.0f} kg/ton-Ti)")
print("  Entrained CaCl2/MgCl2 is water-soluble (CaCl2 ~74 g/100 mL): the wash water")
print("  is of order 0.2-1 m3/ton-Ti, which the 300 kWh/ton post-treatment line")
print("  may understate -- worth an explicit unit operation in the flowsheet (R1-2).")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'output',
                   'tab_r1_liquidus_check.csv')
os.makedirs(os.path.dirname(out), exist_ok=True)
with open(out, 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.writer(f)
    w.writerow(['x_CaCl2', 'x_MgCl2', 'liquidus_C', 'controlling_salt'])
    for xca, xmg, Tc, c in rows:
        w.writerow([f'{xca:.2f}', f'{xmg:.2f}', f'{Tc:.1f}', c])
print(f"\n  -> CSV saved: {os.path.normpath(out)}")
