# Bimetallic Complementary Reduction Titanium Production Process — Computational Study

This repository contains the manuscript and all Python scripts for the paper

**"Thermodynamic and Kinetic Assessment of Titanium Production via In-Situ Electrolysis and Bimetallic Complementary Reduction in MgCl₂–CaCl₂–NaCl–KCl Molten Salt"**

prepared for submission to *Metallurgical and Materials Transactions B (MMTB)*. The manuscript is in the Springer Nature `sn-journal` format and compiles with `pdflatex` + `bibtex`.

---

## Repository Structure

```
.
├── revised_paper_v5.tex         — Manuscript (sn-journal format, main submission)
├── refs.bib                     — BibTeX reference database (27 entries)
├── sn-jnl.cls                   — Springer Nature LaTeX class
├── sn-mathphys.bst              — Springer math-physics BibTeX style
├── sn-aps.bst                   — Springer APS BibTeX style
├── README.md
├── .gitignore
├── scripts/
│   ├── thermo_calc_v2.py            — Core thermodynamic / electrochemical calculations
│   ├── improvements_calc.py         — SCM kinetics, energy sensitivity, liquidus, E–pO²⁻
│   ├── verification_fix.py          — Overpotential and heat-balance numerical verification
│   ├── monte_carlo_uncertainty.py   — Monte Carlo global uncertainty analysis (seed = 42)
│   └── supplement_calc.py           — Butler–Volmer overpotential, Cl₂ boundary, voltage split
├── figures/                        — 11 PDF vector figures (all referenced by the manuscript)
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
│   └── fig_sensitivity_tornado.pdf
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
```

---

## Compiling the Manuscript

```bash
pdflatex revised_paper_v5
bibtex    revised_paper_v5
pdflatex revised_paper_v5
pdflatex revised_paper_v5
```

The `sn-journal` class auto-loads `sn-mathphys.bst`; no explicit `\bibliographystyle` is needed.

---

## Requirements

- Python 3.8+ with `numpy`, `matplotlib`, `scipy` (required by `improvements_calc.py`, `verification_fix.py`, `monte_carlo_uncertainty.py`, `supplement_calc.py`)
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
| `verification_fix.py` | Overpotential and heat-balance numerical verification | numpy, matplotlib | 2 CSVs |
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
- Deoxidation limit: Mg → 3908 ppm O, Ca → 20 ppm O (194× difference)
- Ca²⁺/Na⁺ co-deposition window: +120 mV (ideal), 74.9–147.1 mV under activity-coefficient sensitivity
- Mg–Ca liquid alloy: ΔG_mix = −9.69 kJ/mol (equimolar)
- Shrinking-core kinetics: 100 μm particles reduced in 5.8 min (D = 2.0×10⁻⁹ m²/s)
- Net energy consumption: 11,192 kWh/ton-Ti (conditional on η_I > 0.70)
- Monte Carlo (N = 10⁵, seed = 42): P(W_net < 14,000 kWh/ton) = 85.8%

---

## Data Sources

All thermodynamic data are from published literature (no experimental measurements):

- Barin I. *Thermochemical Data of Pure Substances*, 3rd ed. VCH, Weinheim, 1995. — Cp(T) coefficients, standard enthalpy/entropy
- Kubaschewski O, Alcock CB. *Metallurgical Thermochemistry*, 5th ed. Pergamon, 1979. — Supplementary Cp(T) coefficients
- Waldner P, Eriksson A. Thermodynamic assessment of the Ti–O system. *Calphad*, 1999, 23(2): 189–218. — O dissolution free energy in Ti
- Fray DJ, Farthing TW, Chen GZ. Direct electrochemical reduction of titanium dioxide in molten salts. *Nature*, 2000, 407: 361–364. — FFC process, diffusion coefficient reference
- Yan XY, Fray DJ. *Miner. Process. Extr. Metall.*, 2007, 116(1): 17–24. — O²⁻ diffusivity in CaCl₂-based melts
- Nayeb-Hashemi AA, Clark JB. The Ca–Mg system. *Bull. Alloy Phase Diagrams*, 1988, 8(4): 362–374.
- Zhang J, Liu Y, Du Y, et al. Thermodynamic assessment of the Ca–Mg system. *J. Alloys Compd.*, 2008, 463: 294–301. — Redlich–Kister parameters L₀, L₁
- Pelton AD, Degterov SA, Eriksson G, et al. The modified quasichemical model. *Calphad*, 2000, 24(3): 295–311. — MQM framework
- Morita K, Oguchi T, Sugimoto T, et al. The solubility of MgO in molten MgCl₂–CaCl₂ salt. *Mater. Trans.*, 2004, 45(8): 2712–2718. — MgO solubility
- Kvande H, Drabløs PA. The aluminum smelting process. *JOM*, 2014, 66(2): 342–348. — Hall–Héroult comparison

---

## Limitations

The following items cannot be resolved by computation and require specialized software or experimental data:

1. CALPHAD database validation (liquidus + exact activity coefficients)
2. Electrode kinetic parameters j₀ / α (requires cyclic voltammetry)
3. Pilot-scale experimental validation (current efficiency, product purity, anode lifetime)
4. Impurity separation energy (requires experimental impurity phase distribution)
5. Current-efficiency verification (requires pilot electrolysis cell measurement)

The current-efficiency assumption (η_I = 0.75–0.80) is an unvalidated hypothesis anchored to the Hall–Héroult, Downs, and industrial MgCl₂-electrolysis analogies, and is the dominant uncertainty in the energy estimate (Monte Carlo Spearman ρ = −0.85).
