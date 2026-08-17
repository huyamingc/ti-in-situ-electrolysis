# Bimetallic Complementary Reduction Titanium Production Process — Computational Study

This repository contains the manuscript and all Python scripts for the paper

**"Thermodynamic and Kinetic Assessment of Titanium Production via In-Situ Electrolysis and Bimetallic Complementary Reduction in MgCl₂–CaCl₂–NaCl–KCl Molten Salt"**

prepared for submission to *Metallurgical and Materials Transactions B (MMTB)*. The manuscript is in the Springer Nature `sn-journal` format and compiles with `pdflatex` + `bibtex`.

> Repository: <https://github.com/huyamingc/ti-in-situ-electrolysis>

---

## Repository Structure

```
.
├── manuscript.tex                — Manuscript (sn-journal format, first submission)
├── refs.bib                     — BibTeX reference database (27 entries)
├── sn-jnl.cls                   — Springer Nature LaTeX class
├── sn-mathphys.bst              — Springer math-physics BibTeX style (used, auto-loaded)
├── sn-aps.bst                   — Springer APS BibTeX style (bundled, unused)
├── README.md
├── .gitignore
├── scripts/
│   ├── thermo_calc_v2.py            — Core thermodynamic / electrochemical calculations
│   ├── improvements_calc.py         — SCM kinetics, energy sensitivity, liquidus, E–pO²⁻
│   ├── verification_fix.py          — Overpotential and heat-balance numerical verification
│   ├── monte_carlo_uncertainty.py   — Monte Carlo global uncertainty analysis (seed = 42)
│   └── supplement_calc.py           — Butler–Volmer overpotential, Cl₂ boundary, voltage split
├── figures/                        — 13 PDF vector figures (11 referenced by the manuscript + 2 verification-only)
│   ├── fig_liquidus.pdf
│   ├── fig_scm_conversion.pdf
│   ├── fig_scm_time_vs_size.pdf
│   ├── fig_scm_sensitivity.pdf
│   ├── fig_E_pO2.pdf
│   ├── fig_overpotential_bv.pdf
│   ├── fig_voltage_split.pdf
│   ├── fig_energy_sensitivity.pdf
│   ├── fig_cl2_boundary.pdf
│   ├── fig_monte_carlo.pdf
│   ├── fig_sensitivity_tornado.pdf
│   ├── fig_overpotential_window.pdf      — verification-only (not referenced)
│   └── fig_heat_balance_revised.pdf      — verification-only (not referenced)
└── output/                         — 11 CSV data tables (data traceability)
    ├── tab_thermo.csv
    ├── tab_deox.csv
    ├── tab_Ed.csv
    ├── tab_window.csv
    ├── tab_window_sensitivity.csv
    ├── tab_MgCa_thermo.csv
    ├── tab_mbalance.csv
    ├── tab_energy.csv
    ├── tab_overpotential.csv
    ├── tab_heat_balance_revised.csv
    └── tab_monte_carlo_stats.csv
└── script-verification-report/        — Two-round script-vs-manuscript verification report (HTML, self-contained)
```

---

## Compiling the Manuscript

```bash
pdflatex manuscript
bibtex    manuscript
pdflatex manuscript
pdflatex manuscript
```

The `sn-journal` class auto-loads `sn-mathphys.bst`; no explicit `\bibliographystyle` is needed.

---

## Requirements

- Python 3.8+ with `numpy`, `matplotlib` (all plotting scripts); `scipy` additionally required by `verification_fix.py` and `monte_carlo_uncertainty.py`
- `thermo_calc_v2.py` uses only the standard library (`math`, `csv`)
- A LaTeX distribution (MiKTeX or TeX Live) with the `sn-journal` class dependencies (`cuted`, `xcolor`, `manyfoot`, `textcomp`, `amsthm`, `mathrsfs`, `appendix`)

Install Python dependencies:

```bash
pip install numpy matplotlib scipy
```

---

## Script Overview

| Script | Purpose | Dependencies | Output |
|---|---|---|---|
| `thermo_calc_v2.py` | Core thermodynamics (Meyer-Kelly Cp), deoxidation limits, chloride decomposition voltages, Ca²⁺/Na⁺ window, material/energy balance | stdlib only | 8 CSVs |
| `improvements_calc.py` | SCM kinetics, energy sensitivity, liquidus estimation, E–pO²⁻ diagram, heat balance, TiCl₄ separation work | numpy, matplotlib | 6 figures |
| `verification_fix.py` | Overpotential and heat-balance numerical verification | numpy, matplotlib, scipy | 2 CSVs + 2 verification figures |
| `monte_carlo_uncertainty.py` | Monte Carlo global uncertainty analysis (N = 10⁵, seed = 42) | numpy, matplotlib, scipy | 2 figures + 1 CSV |
| `supplement_calc.py` | Butler–Volmer activation overpotential, anode O₂/Cl₂ selectivity boundary, cell-voltage split | numpy, matplotlib | 3 figures |

All scripts are independent and can be run in any order:

```bash
python scripts/thermo_calc_v2.py
python scripts/improvements_calc.py
python scripts/verification_fix.py
python scripts/monte_carlo_uncertainty.py
python scripts/supplement_calc.py
```

---

## Key Results (600 °C design-basis temperature)

- Reduction thermodynamics: ΔG° = −231.0 to −307.5 kJ/mol for the three pathways (Mg, Ca, and combined Mg + Ca)
- Deoxidation limit: Mg → 3908 ppm O, Ca → 20.2 ppm O (193× difference)
- Ca²⁺/Na⁺ co-deposition window: +120 mV (ideal), 74.9–147.1 mV under activity-coefficient sensitivity
- Mg–Ca liquid alloy: ΔG_mix = −9.69 kJ/mol (equimolar)
- Shrinking-core kinetics: 100 μm particles reduced in 6.3 min (D = 2.0×10⁻⁹ m²/s)
- Net energy consumption: 11,191 kWh/ton-Ti (conditional on η_I > 0.70)
- Monte Carlo (N = 10⁵, seed = 42): P(W_net < 14,000 kWh/ton) = 85.8%

---

## Data Sources

All thermodynamic data are from published literature (no experimental measurements):

- Barin I. *Thermochemical Data of Pure Substances*, 3rd ed. VCH, Weinheim, 1995. — Cp(T) coefficients, standard enthalpy/entropy
- Kubaschewski O, Alcock CB. *Metallurgical Thermochemistry*, 5th ed. Pergamon, 1979. — Supplementary Cp(T) coefficients
- Waldner P, Eriksson G. Thermodynamic modelling of the system titanium–oxygen. *Calphad*, 1999, 23(2): 189–218. — O dissolution free energy in Ti
- Chen GZ, Fray DJ, Farthing TW. Direct electrochemical reduction of titanium dioxide to titanium in molten calcium chloride. *Nature*, 2000, 407: 361–364. — FFC process, diffusion coefficient reference
- Yan XY, Fray DJ. *Miner. Process. Extr. Metall.*, 2007, 116(1): 17–24. — O²⁻ diffusivity in CaCl₂-based melts
- Taninouchi Y, Hamanaka Y, Okabe TH. Electrochemical deoxidation of titanium and its alloy using molten magnesium chloride. *Metall. Mater. Trans. B*, 2016, 47(6): 3394–3404. — MgCl₂ electrochemical deoxidation
- Jiao H, Liu M, Wang Z, Lin M, Qu Z, Song J, Jiao S. Upcycling of titanium by molten salt electrorefining. *ACS Sustainable Chem. Eng.*, 2023, 11(14): 5764–5772. — USTB molten-salt electrorefining
- Chartrand P, Pelton AD. Thermodynamic evaluation and optimization of the LiCl–NaCl–KCl–RbCl–CsCl–MgCl₂–CaCl₂–SrCl₂ system using the modified quasichemical model. *Can. Metall. Q.*, 2000, 39(4): 405–420. — binary chloride thermodynamics
- Kleppa OJ, McCarty FG. Thermochemistry of charge-unsymmetrical binary fused halide systems. II. *J. Phys. Chem.*, 1966, 70(4): 1249–1255. — MgCl₂–alkali chloride mixing enthalpies
- Nayeb-Hashemi AA, Clark JB. The Ca–Mg system. *Bull. Alloy Phase Diagrams*, 1987, 8(1): 58–65.
- Zhang H, Wang Y, Shang S, Chen L-Q, Liu Z-K. Thermodynamic modeling of Mg–Ca–Ce system. *J. Alloys Compd.*, 2008, 463(1-2): 294–301. — Ca–Mg Redlich–Kister parameters
- Hallstedt B. The SGTE collection of binary datasets. *Calphad*, 2025, 89: 102833. — open-access (CC-BY) SGTE binary datasets, incl. Ca–Mg
- Pelton AD, Degterov SA, Eriksson G, Robelin C, Dessureault Y. The modified quasichemical model I—Binary solutions. *Metall. Mater. Trans. B*, 2000, 31(4): 651–659. — MQM framework
- Ito M, Morita K. The solubility of MgO in molten MgCl₂–CaCl₂ salt. *Mater. Trans.*, 2004, 45(8): 2712–2718. — MgO solubility
- Kvande H, Drabløs PA. The aluminum smelting process. *J. Occup. Environ. Med.*, 2014, 56(5 Suppl): S23–S32. — Hall–Héroult comparison

---

## Limitations

The following items cannot be resolved by computation and require specialized software or experimental data:

1. CALPHAD database validation (liquidus + exact activity coefficients)
2. Electrode kinetic parameters j₀ / α (requires cyclic voltammetry)
3. Pilot-scale experimental validation (current efficiency, product purity, anode lifetime)
4. Impurity separation energy (requires experimental impurity phase distribution)
5. Current-efficiency verification (requires pilot electrolysis cell measurement)

The current-efficiency assumption (η_I = 0.75–0.80) is an unvalidated hypothesis anchored to the Hall–Héroult, Downs, and industrial MgCl₂-electrolysis analogies, and is the dominant uncertainty in the energy estimate (Monte Carlo Spearman ρ = −0.85).
