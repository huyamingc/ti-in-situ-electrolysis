# Bimetallic Complementary Reduction Titanium Production Process — Computational Scripts

This directory contains all Python scripts used for the quantitative calculations in the paper "Thermodynamic and Kinetic Assessment of Titanium Production via In-Situ Electrolysis and Bimetallic Complementary Reduction in MgCl₂-CaCl₂-NaCl-KCl Molten Salt", as well as the English manuscript for submission to **Metallurgical and Materials Transactions B (MMTB)**.

## Project File Structure

```
d:\work\papers\ti\
├── review_workspace/
│   ├── revised_paper_v3.tex           — English manuscript (v3, MMTB submission, fully revised)
│   ├── revised_paper_v2.tex           — English manuscript (v2, partially revised, superseded by v3)
│   ├── MMTB_Ti_process.tex            — English manuscript (original version)
│   ├── review_report_MMTB_Ti_process_20260715.html — Multi-agent review report
│   ├── unfixed_issues.md              — List of issues that cannot be auto-fixed (5 items)
│   ├── modification_log_v2.md         — v2 modification log
│   └── ...                            — Other review workspace files
├── README.md                           — This documentation file
├── scripts/
│   ├── thermo_calc_v2.py              — Core thermodynamic calculation script (Cp(T) upgraded, 10 CSVs)
│   ├── improvements_calc.py           — Six improvement modules + plotting (6 PDF vector figures)
│   ├── verification_fix.py            — Review issue verification and correction (2 PDFs + 2 CSVs)
│   └── monte_carlo_uncertainty.py     — [New] Monte Carlo global uncertainty analysis (2 PDFs + 1 CSV)
├── figures/                           — 10 PDF vector figures
│   ├── fig_scm_conversion.pdf
│   ├── fig_scm_time_vs_size.pdf
│   ├── fig_scm_sensitivity.pdf
│   ├── fig_liquidus.pdf
│   ├── fig_E_pO2.pdf
│   ├── fig_energy_sensitivity.pdf
│   ├── fig_overpotential_window.pdf
│   ├── fig_heat_balance_revised.pdf
│   ├── fig_monte_carlo.pdf            — [New] Monte Carlo probability distribution
│   └── fig_sensitivity_tornado.pdf    — [New] Global sensitivity Tornado plot
└── output/                            — 11 CSV data files
    ├── tab_thermo.csv
    ├── tab_deox.csv
    ├── tab_Ed.csv
    ├── tab_window.csv
    ├── tab_window_sensitivity.csv     — Activity coefficient sensitivity (18 combinations)
    ├── tab_MgCa_thermo.csv
    ├── tab_mbalance.csv
    ├── tab_energy.csv
    ├── tab_overpotential.csv
    ├── tab_heat_balance_revised.csv
    └── tab_monte_carlo_stats.csv      — [New] Monte Carlo statistics table
```

## Requirements

- Python 3.8+
- Third-party dependencies: `numpy`, `matplotlib`, `scipy` (required by `improvements_calc.py`, `verification_fix.py`, and `monte_carlo_uncertainty.py`)
- `thermo_calc_v2.py` uses only the standard library `math` and `csv`; no third-party packages needed

Install dependencies:
```bash
pip install numpy matplotlib scipy
```

## Script Overview

| Script | Purpose | Dependencies | Output |
|--------|---------|--------------|--------|
| `thermo_calc_v2.py` | Core thermodynamic and electrochemical calculations (Cp(T) Meyer-Kelly upgraded) | None (standard library only) | Console output (7 PARTs) + 10 CSV files |
| `improvements_calc.py` | Six improvement modules + plotting | numpy, matplotlib | Console output (6 modules) + 6 PDF figures |
| `verification_fix.py` | Review issue verification and correction | numpy, matplotlib | Console output (10 verifications) + 2 PDFs + 2 CSVs |
| `monte_carlo_uncertainty.py` | Monte Carlo global uncertainty analysis (N=10⁵) | numpy, matplotlib, scipy | Console statistics + 2 PDFs + 1 CSV |

## Usage

```bash
# Run from the project root directory (scripts use relative paths, auto-locating output/ and figures/)
python scripts/thermo_calc_v2.py
python scripts/improvements_calc.py
python scripts/verification_fix.py
python scripts/monte_carlo_uncertainty.py
```

All four scripts are independent and can be run in any order.

---

## Detailed Script Descriptions

### 1. `thermo_calc_v2.py` — Core Thermodynamic and Electrochemical Calculations

**Purpose**: Computes all fundamental quantitative data for the paper using the Meyer-Kelly equation and standard thermodynamic data (Barin 1995, Waldner 1999), outputting 10 CSV files for data traceability.

**v3 Major Upgrade: Cp(T) Temperature Dependence**
- All 14 species use the Meyer-Kelly equation: Cp(T) = a + bT + c/T²
- Coefficient sources: Barin (1995), Kubaschewski & Alcock (1979)
- `get_H_S()` function rewritten: solid phase uses integral form, liquid phase retains constant Cp_l
- Replaces the v2 constant 298 K Cp values, improving calculation accuracy at 600°C

**Calculation Contents (7 PARTs)**:

| PART | Content | CSV Output | Paper Section |
|------|---------|------------|---------------|
| PART 1 | ΔG°/ΔH°/ΔS° for three reduction reactions (550/600/650°C) | `tab_thermo.csv` | Table tab:thermo |
| PART 2 | Mg/Ca deoxidation equilibrium oxygen content (ppm level) | `tab_deox.csv` | Table tab:deox |
| PART 3 | Four chloride decomposition voltages + Ca²⁺/Na⁺ co-deposition window | `tab_Ed.csv`, `tab_window.csv` | Table tab:Ed, Table tab:window |
| PART 3.5 | Activity coefficient sensitivity analysis (γ_Ca = 0.3–1.0, 18 combinations) | `tab_window_sensitivity.csv` | §3.3 Activity coefficient sensitivity |
| PART 3.6 | Mg-Ca liquid alloy mixing thermodynamics (Zhang 2008 R-K parameters) | `tab_MgCa_thermo.csv` | §3.4 Mg-Ca alloy parameters |
| PART 4 | Material balance (1 ton Ti basis) | `tab_mbalance.csv` | Table tab:mbalance |
| PART 5 | Energy balance (theoretical/actual energy consumption) | `tab_energy.csv` | Table tab:energy |

**Key Output Results (after Cp(T) upgrade)**:
```
ΔG°(600°C): R1=-231.0, R2=-307.5, R3=-269.3 kJ/mol
Deoxidation(600°C): Mg→3908 ppm, Ca→20 ppm, ratio=194x
Decomposition voltage(600°C): MgCl₂=2.601V, NaCl=3.440V, CaCl₂=3.428V, KCl=3.675V
Ca²⁺/Na⁺ pure salt difference: +12 mV (Ca²⁺ slightly easier to reduce; in the CaCl₂-rich melt this is further amplified)
Recommended composition ideal co-deposition window: +120 mV
Activity-corrected window range: 74.9–147.1 mV (all 18 combinations >0)
Critical γ_CaCl2: ~0.02–0.04
Material balance: 3013 kg → 3013 kg (fully balanced)
Theoretical energy consumption: 6112 kWh/ton, Actual: 11200–12800 kWh/ton
```

---

### 2. `improvements_calc.py` — Six Improvement Modules

**Purpose**: Executes 6 theoretical calculation improvements requiring no experiments, generating all 6 vector PDF figures + heat balance/separation work analysis data.

**6 Module Descriptions**:

| Module | Content | Output Files | Paper Section |
|--------|---------|--------------|---------------|
| Module 1 | Shrinking core model (SCM) kinetic prediction | `fig_scm_conversion.pdf`, `fig_scm_time_vs_size.pdf`, `fig_scm_sensitivity.pdf` | §4.4 |
| Module 2 | Energy consumption sensitivity analysis (η_I vs V_cell) | `fig_energy_sensitivity.pdf` | §4.5 |
| Module 3 | Quaternary molten salt liquidus estimation | `fig_liquidus.pdf` | §3.2 |
| Module 4 | E-pO²⁻ thermodynamic stability diagram | `fig_E_pO2.pdf` | §4.3 |
| Module 5 | Full-process heat balance and exergy analysis | Console output | §4.6 |
| Module 6 | TiCl4 distillation minimum separation work | Console output | §4.6 |

**Module 1 — Shrinking Core Model Kinetics** (R = diameter/2 corrected):
- Literature diffusion coefficient: D = 2.0×10⁻⁹ m²/s (CaCl₂-based melt, 600°C, order-of-magnitude reference only)
- Effective diffusion coefficient: D_eff = 2.0×10⁻¹⁰ m²/s (porosity 0.3, tortuosity 3)
- Sensitivity analysis: D = 1.0×10⁻⁹ – 3.0×10⁻⁹ m²/s, 100 μm diameter particle reduction time 3.9–11.6 min
- Key result: 100 μm diameter particle complete reduction requires 5.8 min (600°C, baseline D)

**Module 5 — Full-Process Heat Balance** (efficiency definitions corrected):
- Electrolysis energy accounts for 93.9%, auxiliary only 6.1%
- Net energy consumption: 11192 kWh/ton
- Process energy efficiency (electrolysis minimum/net consumption) = 54.6%
- Second-law efficiency (TiO₂ reversible work/net consumption) = ~40.7%
- Electrolysis energy utilization (electrolysis/total input) = 93.9%
- Reaction exotherm 1690 kWh/ton is internal heat recycling, embedded in electrolysis gross demand, not used to offset furnace wall heat loss

---

### 3. `verification_fix.py` — Review Issue Verification and Correction Script

**Purpose**: Numerical verification of P0/P1 issues identified by the multi-agent review system, generating overpotential analysis and corrected heat balance figures.

**Verification Contents (10 items)**:

| Verification Item | Content | Conclusion |
|-------------------|---------|------------|
| 1. Liquidus | Recommended composition liquidus temperature | 543.7°C ≈ 544°C ✓ |
| 2. Co-deposition window | 18-group activity coefficient sensitivity | 120.2 mV (ideal), 74.9–147.1 mV (full range) ✓ |
| 3. Overpotential analysis | Butler-Volmer equation activation overpotential | Qualitative description (no literature j₀/α values) ✓ |
| 4. SCM kinetics | R=50μm vs R=100μm | 100μm diameter (R=50μm) → 5.8 min ✓ |
| 5. Deoxidation ratio | 3908/20 | 194× ✓ |
| 6. Energy calculation | Theoretical/actual energy consumption | Deviation <1 kWh/ton ✓ |
| 7. Heat balance | 1690 kWh internal heat recycling | Net value 11192 kWh/ton ✓ |
| 8. Mg-Ca alloy | R-K parameter calculation | All match ✓ |
| 9. Decomposition voltage | ΔG°f and E_d consistency | Corrected ΔG°f to 873K values ✓ |
| 10. Corrected figures | Overpotential window + heat balance | 2 PDFs + 2 CSVs ✓ |

**Output Files**:
- `figures/fig_overpotential_window.pdf` — Effective co-deposition window at different current densities
- `figures/fig_heat_balance_revised.pdf` — Corrected energy flow decomposition bar chart
- `output/tab_overpotential.csv` — Overpotential calculation data table
- `output/tab_heat_balance_revised.csv` — Corrected heat balance data table

---

### 4. `monte_carlo_uncertainty.py` — Monte Carlo Global Uncertainty Analysis [New]

**Purpose**: Performs global uncertainty propagation analysis on two core output quantities (SCM reduction time, full-process net energy consumption), sampling all parameters simultaneously, outputting probability distributions and statistics.

**Parameter Distributions**:

| Parameter | Distribution | Range |
|-----------|--------------|-------|
| D (diffusion coefficient) | Uniform | 1.0–3.0 × 10⁻⁹ m²/s |
| ε (porosity) | Uniform | 0.1–0.5 |
| τ (tortuosity) | Uniform | 1.5–5.0 |
| η_I (current efficiency) | Triangular | 0.50(low) – 0.75(mode) – 0.88(high) |
| V_cell (cell voltage) | Normal (truncated) | μ=4.1, σ=0.3, [3.5, 4.5] |

**Key Results (N=100,000)**:

| Metric | Median | P5 | P95 |
|--------|--------|----|-----|
| SCM reduction time (min) | 6.6 | 2.5 | 19.9 |
| Net energy consumption (kWh/ton-Ti) | 11,781 | 9,515 | 15,362 |
| Process energy efficiency (%) | 51.9 | 39.8 | 64.2 |
| Second-law efficiency (%) | 38.6 | 29.6 | 47.8 |

**Probability Analysis**:
- P(W_net < 11,192 kWh/ton) = 35.8%
- P(W_net < 14,000 kWh/ton) = 85.8%
- P(t_complete < 10 min) = 73.0%

**Spearman Rank Correlation (Parameter Importance)**:
- SCM time: τ (ρ=0.81) > ε (ρ=-0.53) > D (ρ=-0.42)
- Net energy: η_I (ρ=-0.84) > V_cell (ρ=0.51)

**Output Files**:
- `figures/fig_monte_carlo.pdf` — SCM time distribution + net energy distribution (dual-panel)
- `figures/fig_sensitivity_tornado.pdf` — Tornado sensitivity plot (dual-panel)
- `output/tab_monte_carlo_stats.csv` — Complete statistics table

---

## Complete Output File List

### Figure Files (`figures/` directory, 10 PDF vector figures)

```
figures/
├── fig_scm_conversion.pdf          — SCM conversion vs. time (different particle sizes)
├── fig_scm_time_vs_size.pdf        — Complete reduction time vs. particle size
├── fig_scm_sensitivity.pdf         — SCM diffusion coefficient sensitivity (D=1–3×10⁻⁹)
├── fig_liquidus.pdf                — Quaternary molten salt liquidus projection (x_KCl=0.15 section)
├── fig_E_pO2.pdf                   — E-pO²⁻ thermodynamic stability diagram
├── fig_energy_sensitivity.pdf      — Energy consumption sensitivity contour plot
├── fig_overpotential_window.pdf    — Overpotential-corrected co-deposition window
├── fig_heat_balance_revised.pdf    — Corrected heat balance energy flow chart
├── fig_monte_carlo.pdf             — [New] Monte Carlo probability distribution
└── fig_sensitivity_tornado.pdf     — [New] Global sensitivity Tornado plot
```

### Data Files (`output/` directory, 11 CSVs)

```
output/
├── tab_thermo.csv                  — Three reduction reactions ΔG°/ΔH°/ΔS° (after Cp(T) upgrade)
├── tab_deox.csv                    — Mg/Ca deoxidation equilibrium oxygen content (after Cp(T) upgrade)
├── tab_Ed.csv                      — Four chloride decomposition voltages
├── tab_window.csv                  — Ca²⁺/Na⁺ co-deposition window (6 compositions)
├── tab_window_sensitivity.csv      — Activity coefficient sensitivity (18 γ combinations, including 0.3/0.5)
├── tab_MgCa_thermo.csv             — Mg-Ca alloy mixing thermodynamics (101 composition points)
├── tab_mbalance.csv                — Material balance
├── tab_energy.csv                  — Energy consumption calculation
├── tab_overpotential.csv           — Overpotential calculation data
├── tab_heat_balance_revised.csv    — Corrected heat balance data
└── tab_monte_carlo_stats.csv       — [New] Monte Carlo statistics table
```

---

## Review Revision History

### Round 1 Review (5-Agent Review System)

Based on 64 issues identified by the multi-agent review system (5 sub-Agents), the following key corrections were completed:

| Issue ID | Problem Description | Correction |
|----------|-------------------|------------|
| DP1-1 | Deoxidation formula symbol and basis error | Unified to 1 mol O basis, removed ½ coefficient |
| DP1-2 | SCM radius confusion (R=diameter) | Corrected R=diameter/2, 100μm→5.8min |
| DP1-3 | Heat balance arithmetic contradiction | Redefined efficiency, distinguished internal heat recovery from external heating |
| DP1-4 | Overly strong novelty claim | Limited "First proposal" scope, added literature comparison |
| DP1-5 | Efficiency definition confusion | Added TiO₂ reversible work 4550 kWh/ton, second-law efficiency ~36% |
| DP1-6 | Novelty missing condition | Added "conditional on η_I > 0.70" |
| DP1-7 | Abstract word count exceeded | Compressed to ~135 words |
| DP1-8 | Composition selection rationale missing | Added three selection criteria |
| P1-1 | Kirchhoff/Gibbs-Helmholtz confusion | Corrected text description |
| P1-3/4 | ΔG_deox basis confusion | Unified to 1 mol O basis |
| P1-5 | Nernst equation missing pO₂ premise | Added "assuming pO₂ = 1 atm" |
| P1-6 | "First proposal" wording | Changed to "To the authors' knowledge" |
| P1-7 | Operating temperature lower bound 550°C | Raised to 580°C |
| P1-13 | γ scan range insufficient | Extended to 0.3–1.0 (18 combinations) |
| P1-16 | Diffusion coefficient species ambiguous | Distinguished O²⁻ outward vs. Mg-Ca inward diffusion |
| P1-42 | multicols two-column format | Removed, changed to single column |
| P1-44 | Missing symbol table | Added Nomenclature section |
| P1-48 | References not ordered | Reordered by first citation (25 entries) |
| P1-41 | lee2024/lee2025 duplicate | Removed lee2024 |

### Round 2 Deep Revision (v2→v3)

| Modification | Content |
|-------------|---------|
| Cp(T) temperature-dependent coefficients | Implemented Meyer-Kelly equation Cp=a+bT+c/T², all 14 species updated; recalculated and updated 60+ values throughout the TeX manuscript |
| Monte Carlo global uncertainty analysis | Created monte_carlo_uncertainty.py (N=10⁵), outputting 2 PDF figures + CSV |
| Hall-Héroult process comparison | Added comparison paragraph (η_I=90-95%, 13000 kWh/ton-Al) + kvande2014 reference |
| Impurity separation energy estimate | Extended Limitations item 7, added acid leaching energy estimate 200-500 kWh/ton-Ti (~2-4%) |
| Figure format conversion | All figures changed from PNG to PDF vector output |
| table* → table | Process comparison table environment unified to single-column |

### Round 3 Text Optimization (v3 final revision)

| Modification | Content |
|-------------|---------|
| B-1: E-pO²⁻ derivation | Added complete derivation steps (Nernst→pO²⁻ substitution→positive slope); caption supplemented with Ca²⁺-O²⁻ complexation explanation |
| B-2: Mg-Ca L₁ deviation | Added regular solution approximation L₁=0 deviation analysis (L₁ term = 0 at equimolar, <1 kJ/mol off-equimolar) |
| B-3: Monte Carlo limitations | Added note that γ_CaCl2, liquidus temperature, and oxide solubility uncertainties are not included |
| B-4: Comparison table temperature column | Added "Operating Temperature" column (Kroll 1000-1200°C, FFC ~950°C, USTB ~900°C, Proposed 580-650°C) |
| B-6: Nomenclature refinement | ΔG_mix qualified with "Mg-Ca alloy", ΔG_deox qualified with "per 1 mol O basis", added L₁ entry |
| C-1: Efficiency definition distinction | Added one-sentence distinction: 48.4% (electrolysis step minimum/total) vs. 36% (overall reaction reversible work/total) |
| C-2: Exotherm utilization restatement | Added in text: "exothermic heat only offsets electrolysis demand, does not compensate furnace heat loss" |

### Round 4 Review (v5, 6-Agent Review System)

| Modification | Content |
|-------------|---------|
| P0-1: Monte Carlo η_I distribution fix | `monte_carlo_uncertainty.py`: corrected η_I from Tri(0.70,0.80,0.88) to Tri(0.50,0.75,0.88) to match paper claim; re-ran N=10⁵ simulation; updated all statistics in Abstract/Sec.4.4/Conclusions (median 13,471, P<14,000=61.3%) |
| P0-2: Energy balance exergy clarification | Sec.4.7: renamed "heat balance" to "energy balance", "gross demand" to "gross electrical demand"; added explicit note that reaction-exotherm offset is a simplified accounting convention; distinguished electrical vs thermal energy quality (exergy); renamed "process electrical efficiency" to "process energy efficiency"; added table footnote |
| README sync | Updated Monte Carlo parameter table and results to reflect corrected η_I distribution |

### Round 5 Review (post-v5 numerical/consistency audit against scripts)

A full re-derivation audit of `revised_paper_v5.tex` against the four calculation scripts found that several tables still carried pre-v3 (constant-Cp) values and one energy-balance arithmetic error. Corrected items:

| Correction | Before → After |
|-----------|----------------|
| Table tab:Ed (ΔG°f / E_d / E°_red) | NaCl −329.9/3.419/−3.419 → **−331.9/3.440/−3.440**; CaCl₂ −660.7/3.424/−3.424 → **−661.5/3.428/−3.428**; MgCl₂ → −501.9/2.601; KCl → −354.6/3.675 |
| Pure-salt Ca²⁺/Na⁺ gap (sign flip) | −5 mV (Na⁺ easier) → **+12 mV (Ca²⁺ easier)** |
| Co-deposition window (ideal / range) | 103 mV / 58.0–130.1 mV → **120 mV / 74.9–147.1 mV**; Good/Moderate 7/11 → **15/3** |
| Deoxidation (Ca / Mg / ratio) | 22 ppm / 3919 ppm / 175× → **20 ppm / 3908 ppm / 194×** |
| Energy balance gross electrical demand | 13,704 → **12,244 kWh/ton** (η=0.75, V=4.1 V, consistent with Table tab:energy) |
| Reaction exotherm | ΔH° −294 → **−291.3 kJ/mol**; 1,704 → **1,690 kWh/ton** (footnote unit `/3.6×10⁶` fixed to `/3600`) |
| Net consumption / efficiencies | 12,638 → **11,192 kWh/ton**; 48.4% → **54.6%**; 36% → **40.7%**; 94.6% → **93.9%** |
| Monte Carlo (re-run with exotherm offset) | median 13,471 → **11,781 kWh/ton**; P(W<14,000) 61.3% → **85.8%**; second-law mean 33.7% → **38.6%** |
| Physical error | "Mg/Ca are liquid at 600 °C" → **"Mg–Ca alloy is liquid at 600 °C (eutectic ≈517 °C)"** (pure Mg/Ca are solid) |
| E–pO²⁻ reference electrode | "vs Cl₂/Cl⁻" → **"vs O₂/O²⁻ (pO₂=1 atm, a(O²⁻)=1)"** |

Scripts synced: `verification_fix.py` (stale 6096/2.72 V/13704/−1704/12000/4745-ppm/24-ppm values + hardcoded `d:/work/论文` paths fixed); `improvements_calc.py` (6096 → 6112, E–pO²⁻ ylabel); `monte_carlo_uncertainty.py` (W_net now includes exotherm offset, 6096 → 6112, nominal 11,192). Figures and CSVs regenerated.

**Data-uncertainty note**: the pure-salt Ca²⁺/Na⁺ gap is only +12 mV, which is within the ≈±2 kJ/mol (≈±20 mV for monovalent NaCl) uncertainty of the Barin ΔG°f data; the co-deposition window is therefore robust not because of an intrinsic Ca preference but because of the concentration ratio x_CaCl₂/x_NaCl = 0.40/0.15. This caveat has been added to the manuscript (Sec. 3.1 / Sec. 4.2).

**Follow-up review (5 external criticisms)** — verdicts and fixes:

| # | Criticism | Verdict | Fix applied |
|---|-----------|---------|-------------|
| 1 | Anode O₂/Cl₂ selectivity not quantified | **Valid** | Added quantitative selectivity boundary (Cl₂ at E_red=0; O₂ favored while E°(O₂/O²⁻ vs Cl₂/Cl⁻) < (RT/2F)ln a(O²⁻)); flagged that E°(O₂/O²⁻ vs Cl₂/Cl⁻) = melt oxoacidity is unavailable and is a missing boundary condition |
| 2 | SCM "liquid channel" physical contradiction | **Partially valid** | Added wetting/pore-clogging/sintering note to Limitations (3). The specific "Mg–Ti intermetallic" claim is **incorrect** (Mg/Ca are immiscible with Ti; no intermetallics form) — not added |
| 3 | "Post-treatment 300 kWh" ambiguity / double-count with impurity separation | **Valid** | Clarified post-treatment = salt washing/drying/screening (included); impurity acid-leaching (200–500 kWh) is separate and excluded (Table + Limitations (7)); fixed script comment |
| 4 | a_M = 0.263 "averaging trap" | **Weak/minor** | Added note that 0.263 is a global average; local O content is inhomogeneous and bounded by pure-Mg (3908 ppm) / pure-Ca (20 ppm) columns of Table tab:deox |
| 5 | Liquidus uncertainty engineering significance underestimated | **Valid** | Strengthened Limitations (4): 600 °C floor = only ~6 °C margin over 594 °C upper bound; recommend hard floor ≥620 °C (or CALPHAD confirmation), noting the 620–650 °C operable-window squeeze set by the Mg melting point |

Also caught and fixed one leftover stale value (`12,638 → 11,192` in Limitations (7)) that a braces-sensitive earlier grep had missed.

**Second follow-up (exergy + accounting clarifications)**:

| # | Comment | Verdict / action |
|---|---------|------------------|
| 1 | The 1:1 exotherm→electricity offset is optimistic in exergy terms (Carnot factor 1−298/873 ≈ 0.66 ⇒ offset ≈ 1,100 not 1,690; net ≈ 11,800 kWh/ton) | **Valid, quantified**: added one sentence to the italic warning in Sec. 4.7 — crediting the 1,690 kWh/ton exotherm at its Carnot work-equivalent (~1,100 kWh/ton) raises the net equivalent consumption to ~11,800 kWh/ton |
| 2 | 85.8% vs 61.3% is an accounting-basis unification (exotherm now subtracted), not a physical energy decrease | **Agreed, no change**: the paper retains the 97.1% restricted-distribution comparison and the "significant sensitivity to η_I" warning, so readers are not misled |

### P0/P1 computational supplement (no-lab desk work)

Added a new script `scripts/supplement_calc.py` and four figures + text to deepen the analytical model per the "整体总评" priority list:

| Item | What was added |
|------|----------------|
| P0-2 Overpotential | Butler–Volmer activation-overpotential estimate (η_Ca≈174 mV vs η_Na≈424 mV at j=0.5 A/cm²; kinetic window widens 120→~370 mV). Fig. `fig_overpotential_bv.pdf`, Sec. 4.2. |
| P0-3 Cl₂ boundary | Parametric critical a(O²⁻) vs oxoacidity E°; operating a(O²⁻)≈1e-4–1e-3; O₂ safe only if E° < −0.35 V. Fig. `fig_cl2_boundary.pdf`, Sec. 4.7. |
| P0-4 MC thermodynamics | Added note that γ_CaCl₂/liquidus/solubility act on feasibility (not energy); solubility dominates closed-loop feasibility. Sec. 4.4. |
| P0-1 Liquidus | Hard floor ≥620 °C recommendation (Limitations (4)) + **binary-subsystem table** `tab:binary` (MgCl₂-NaCl ~440 °C, MgCl₂-CaCl₂ ~606 °C via CaMg₂Cl₆, CaCl₂-NaCl ~500 °C, MgCl₂-KCl ~470 °C, NaCl-KCl ~657 °C); argument that Mg+Ca = 70 mol% raises the quaternary liquidus. |
| P1-5 Voltage split | V_cell = 2.73 (decomp) + 0.30 (η_anode) + 0.20 (η_cathode) + 0.90 (IR) ≈ 4.13 V. Fig. `fig_voltage_split.pdf`, Sec. 4.5. |
| P1-7 Salt circulation | Concrete inventory: ~201 t salt/ton Ti at 1 wt% solubility (~400 t at 0.5 wt%). Sec. 4.7. |
| P1-6 Ti valence cycle | Qualitative note + **TiCl thermodynamics table** `tab:ticl` (ΔG°f: TiCl₂ −464, TiCl₃ −654, TiCl₄ −727 kJ/mol; Ti+TiCl₄→2TiCl₂ ΔG ≈ −202 kJ/mol at 298 K, ≈ −80 kJ/mol at 873 K). Sec. 4.7. |

Added `\usepackage{amssymb}` to the preamble (for `\lesssim`).

### Reviewer-#2 logic hardening (risk/contingency + decision criteria)

| Item | Verdict | Fix applied (with corrected numbers) |
|------|---------|--------------------------------------|
| 1. Graphite-anode contingency | Valid | Limitations (8): graphite fallback → V_cell≈4.3 V, net 11,192→~11,800 kWh/ton (+5%), breaks green-O₂ narrative; prioritize NiFe₂O₄/CeO₂ anode screening |
| 2. Go/no-go decision criteria | Valid (numbers corrected) | Conclusions (9): abandon closed-loop if η_I<0.60 at V=4.0 (net ~13,900 kWh/ton) or solubility <0.5 wt% (salt >400 t/ton) |
| 3. 600 °C vs 620 °C contradiction | Valid | §2: 600 °C = design basis; ≥620 °C = recommended floor; 600→620 °C shifts figures by only a few % |
| 4. Abstract failure-risk balance | Partially valid | Abstract now names the two prerequisites (>0.5 wt% solubility; η_I>0.70 via inert anode) |
| 5. sn-journal migration | Correct (format) | Deferred — requires full template rewrite + .bib; pending journal decision |

Note: the reviewer's suggested absolute numbers were partly inconsistent with the paper's own accounting (graphite ~13,500–14,500 → correct ~11,800; η_I<0.60 ">16,000" → correct ~13,900), so the fixes use the internally-consistent values.

### sn-journal (Springer Nature) template migration

Migrated to the Springer Nature `sn-journal` template for MMTB submission:

- **`revised_paper_sn.tex`** — `\documentclass[sn-mathphys,Numbered]{sn-jnl}`; title/author/affil/`\abstract`/`\keywords`/`\maketitle` in Springer format; body content identical to `revised_paper_v5.tex`; declarations under a "Declarations" heading.
- **`refs.bib`** — all 27 references converted to BibTeX (article/book/incollection).
- Template files downloaded to the project root: `sn-jnl.cls`, `sn-mathphys.bst`, `sn-aps.bst` (from a public GitHub mirror of the official Springer template).
- Compiled with `pdflatex → bibtex → pdflatex ×2`, producing `revised_paper_sn.pdf` (952 KB), no errors/undefined references.

Note: the class requires `cuted`, `xcolor`, `manyfoot`, `textcomp`, `amsthm`, `mathrsfs`, `appendix` (auto-installed by MiKTeX); `sn-mathphys.bst` sets `\bibliographystyle` automatically (no explicit `\bibliographystyle` needed).

### Author metadata update

Author block updated in both `revised_paper_sn.tex` (sn-journal) and `revised_paper_v5.tex` (article):
- Yaming Hu — ORCID 0009-0003-1406-0485
- Independent Researcher, Guiyang, Guizhou Province, China
- 64687555@qq.com

The sn-journal `\orcid` macro is redefined to a text-based ``iD`` superscript link (the class's default needs `Orcidlogo.eps`, which is not bundled). `revised_paper_sn.pdf` = 32 pages, no errors/undefined refs, only two negligible overfull hboxes (4.7/3.4 pt).

### Submission cleanup (first submission)

Removed all review-response / revision-history traces from `revised_paper_v5.tex` so the manuscript reads as a first submission:

- Deleted Limitations item (10) "Co-deposition window recalculation" (a reviewer-response artifact; the window values already appear in Table tab:window_sens).
- Removed "previous restricted-distribution result (97.1%)" and "deliberately extended … (rather than 0.70, the feasibility threshold)" from the Monte Carlo section and Limitations (9).
- Changed "extended current-efficiency distribution" → "broad current-efficiency distribution" (abstract, figure caption, Conclusions).
- Changed "educated guesses" → "rough estimates".

---

## Data Sources

All thermodynamic data are from the following literature (no experimental measurements required):

- Barin I. *Thermochemical Data of Pure Substances*, 3rd ed. VCH, 1995. — Cp(T) coefficients, standard enthalpy/entropy
- Kubaschewski O, Alcock CB. *Metallurgical Thermochemistry*, 5th ed. Pergamon, 1979. — Supplementary Cp(T) coefficients
- Waldner P, Eriksson A. Thermodynamic assessment of the Ti-O system. *Calphad*, 1999, 23(2):189-218. — O dissolution free energy in Ti
- Fray DJ, Farthing TW, Chen GZ. Direct electrochemical reduction of titanium dioxide in molten salts. *Nature*, 2000, 407:361-364. — FFC process parameters, diffusion coefficient reference
- Yan XY, Fray DJ. Fused salt electrolytic reduction of solid oxides and oxide mixtures for green production of metals and alloys. *Miner. Process. Extr. Metall.*, 2007, 116(1):17-24. — O²⁻ diffusivity in CaCl₂-based FFC melts (~1–3×10⁻⁹ m²/s)
- Nayeb-Hashemi AA, Clark JB. The Ca-Mg system. *Bull. Alloy Phase Diagrams*, 1988, 8(4):362-374.
- Zhang J, Liu Y, Du Y, et al. Thermodynamic assessment of the Ca-Mg system. *J. Alloys Compd.*, 2008, 463:294-301. — Redlich-Kister parameters L₀, L₁
- Pelton AD, Degterov SA, Eriksson G, et al. The modified quasichemical model. *Calphad*, 2000, 24(3):295-311. — MQM framework
- Morita K, Oguchi T, Sugimoto T, et al. The solubility of MgO in molten MgCl₂-CaCl₂ salt. *Mater. Trans.*, 2004, 45(8):2712-2718. — MgO solubility
- Kvande H, Drablos PA. The aluminum smelting process and innovative alternative technologies. *JOM*, 2014, 66(2):342-348. — Hall-Héroult process comparison data

---

## Remaining Issues That Cannot Be Auto-Fixed

The following issues require specialized software (FactSage) or experimental data and cannot be resolved via scripts/text. See `review_workspace/unfixed_issues.md` for details:

1. CALPHAD database validation (liquidus + exact activity coefficients)
2. Electrode kinetic parameters j₀/α (requires cyclic voltammetry experiments)
3. Pilot-scale experimental validation (current efficiency, product purity, anode lifetime)
4. Impurity separation energy precise calculation (requires experimental impurity phase distribution)
5. Current efficiency experimental verification (requires pilot electrolysis cell measurement)

### Status of the remaining "unvalidated" parameters (post Round 5)

| Parameter | Status | Fixable by literature? |
|-----------|--------|------------------------|
| η_I = 0.75–0.80 | Still an unvalidated hypothesis for *this* specific quaternary melt; no direct measurement exists. **Improved**: now also anchored to industrial Mg electrolysis from molten MgCl₂ (80–90%, the primary salt of the process), in addition to Hall–Héroult (90–95%) and Downs (70–90%) | Partially (analogy strengthened); final value requires pilot-cell measurement |
| D = 2.0×10⁻⁹ m²/s (SCM) | Still an order-of-magnitude estimate; rate-limiting species (O²⁻ outward vs. Mg/Ca inward) unresolved. **Improved**: now explicitly anchored to measured O²⁻ diffusivity in CaCl₂ melts (1–3×10⁻⁹ m²/s, Yan & Fray 2007) | Partially (value anchored); rate-limiting-species identification requires experiment |
| Reaction-exotherm offset (−1690 kWh/ton) | A modeling/accounting convention (thermal ≠ electrical, exergy); paper already flags this in an italic note | No — it is a modeling choice, not a data gap |
| `verification_fix.py` stale values | **Fixed** (Round 5: 6096→6112, 2.72→2.729 V, 13704→12244, −1704→−1690, 12000→10554, 4745/24 ppm→3908/20 ppm, path bug fixed) | Yes — fixed |
