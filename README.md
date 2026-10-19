# Bimetallic Complementary Reduction Titanium Production Process — Computational Study

This repository contains the manuscript and every Python script, data table and figure
source behind the paper

**"Electrochemical Design Basis for Titanium Production by Mg–Ca Co-Deposition in a Quaternary Chloride Melt"**

prepared for submission to the *Journal of Sustainable Metallurgy* (Springer).

The mechanism is built around the reaction Ca + MgO → CaO + Mg, with the 1:1 and the
CaO-only limits carried through as Case II and Case I; the engineering content (flowsheet,
settled-bed reactor, semi-continuous operation, electrostatic separation) is included; the
uncertainty analysis samples eleven parameters; and results are reported at both 600 °C and
620 °C. The manuscript is typeset with the Springer Nature **`sn-jnl`** class in Basic
numeric reference style, with a BibTeX bibliography (`refs.bib`, `sn-basic.bst`) numbered in
citation order, and compiles with `pdflatex` + `bibtex`.

> Repository: <https://github.com/huyamingc/ti-in-situ-electrolysis>
> Preprint: [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21973469.svg)](https://doi.org/10.5281/zenodo.21973469)

---

## 1. Status at a glance

Single source of truth for the numbers quoted about this repository. Everything in the
table is reproducible from the commands in §14.

| Item | Value |
|---|---|
| `manuscript.tex` | 827 lines, 141,053 B |
| `manuscript.pdf` | **43 pages**, 3,292,491 B |
| Figures / tables | 15 / 10 |
| References | **35** (35 `\bibitem` entries in `manuscript.bbl`, 35 distinct `\cite` keys, none unused) |
| Abstract | **248 words** (journal limit 250) |
| Prose (body) | ≈13.7k words; 20.0k in the PDF including captions, tables and references |
| Python scripts | 18 (`.py`, `scripts/`) |
| CSV data tables | 17 (`output/`) |
| Vector figures | 17 PDF (`figures/`) → 15 EPS (`figures_eps/`) |
| Build state | 0 LaTeX warnings, 0 errors, 0 undefined references, 0 overfull hboxes (the 14 `LaTeX Font Warning` size substitutions emitted by the class for the 4 pt figure annotations are template-inherent and do not indicate a defect) |

> **Zenodo version note.** The deposited preprint is **v3 (record 21973469, 2026-09-02)**.
> It predates the Monte Carlo re-run described in §4 (entry 11): its abstract carries the
> *pre-re-run* values **13,141 kWh/ton-Ti and 82.1%**, whereas `manuscript.tex` here carries
> the *post-re-run* values **13,157 and 82.0%**. Every other number is identical between the
> two. Cite the repository, not v3, if the MC figures matter.

---

## 2. Repository structure

```
.
├── manuscript.tex                — Manuscript (sn-jnl class, Basic numeric style)
├── manuscript.pdf                — Compiled PDF (43 pages)
├── manuscript.bbl                — BibTeX output, kept so the PDF rebuilds without bibtex
├── refs.bib                      — Bibliography database (35 entries, with titles and DOIs)
├── manuscript_v1.tex             — Frozen snapshot of the manuscript as reviewed (825 lines)
├── sn-jnl.cls                    — Springer Nature class (one line patched: see §5)
├── sn-basic.bst                  — Springer Basic reference style, unmodified
├── sn-basic-reforder.bst         — Same style with citation-order numbering
├── Orcidlogo-mark.pdf            — ORCID iD mark, sized for the author block
├── submission_jsm/               — Upload package, regenerated from the current sources (§11)
├── GA_process.png                — Graphical abstract (uploaded separately)
├── README.md
├── .gitignore
├── scripts/                      — 18 Python files (§7)
│   ├── thermo_calc_v2.py            — Core thermodynamics / electrochemistry (8 CSV)
│   ├── verification_fix.py          — Overpotential and heat balance (2 CSV)
│   ├── case_baseline_mc.py          — Case I/II energy baseline (2 CSV)
│   ├── monte_carlo_v2.py            — Eleven-parameter Monte Carlo (1 CSV + Fig. 11/12)
│   ├── improvements_calc.py         — SCM kinetics, liquidus, E–pO²⁻, energy sensitivity
│   ├── supplement_calc.py           — Butler–Volmer, Cl₂ boundary, voltage split
│   ├── dual_temperature.py          — 600 / 620 / 650 °C recomputation (1 CSV)
│   ├── fig_flowsheet.py             — Fig. 1
│   ├── fig_mechanism.py             — Fig. 3, Fig. 5
│   ├── fig_current_regimes.py       — Fig. 6
│   ├── fig_ga.py                    — Graphical abstract
│   ├── verify_r1_liquidus.py        — Independent liquidus re-derivation (1 CSV)
│   ├── verify_r3_reviewer3.py       — Ca + MgO thermochemistry (1 CSV)
│   ├── verify_revision.py           — Text/number consistency sweep
│   ├── revision_r3_mechanism_numbers.py — Numbers moved by the mechanism rebuild (1 CSV)
│   ├── analyze_length.py            — Paragraph / section length audit
│   ├── crossref_titles.py           — Crossref title recovery for the bibliography
│   └── make_reforder_bst.py         — Derives sn-basic-reforder.bst from sn-basic.bst
├── figures/                      — Source vector figures written by the scripts (17 PDF)
├── figures_eps/                  — Submission EPS (15) + on-the-fly PDF conversions
└── output/                       — 17 CSV data tables (§3)
```

Neither `_archive_mmtb/` nor `review_workspace/response_and_resubmission_v1.md` exists in
this checkout; earlier revisions of this README referred to both and have been corrected.
`review_workspace/` exists locally but is excluded from git by `.gitignore` (§12).

---

## 3. Data traceability

The chain for every number in the paper is the same four links:

```
text value  ←  CSV row (full precision)  ←  script  ←  formula (equation number)  ←  literature parameter
```

Where a link is weak or absent, it is stated explicitly in §3.7.

### 3.1 Quantity → script → CSV

Paths are relative to the repository root. "Full precision" means the CSV value before the
4-significant-figure rounding used in the text; see §3.6 for the resulting last-digit
differences.

| Quantity in the text | Text | CSV file → column | Script | Equation |
|---|---|---|---|---|
| ΔG°(TiO₂+2Mg→Ti+2MgO), 600 °C | −231.0 kJ/mol | `tab_thermo.csv` → `dG(kJ/mol)`, row `R1…600` | `thermo_calc_v2.py` | Eq. 1 |
| ΔG°(TiO₂+2Ca→Ti+2CaO), 600 °C | −307.5 kJ/mol | `tab_thermo.csv` → `dG(kJ/mol)`, row `R2…600` | `thermo_calc_v2.py` | Eq. 1 |
| ΔH° of R1 / R2, 600 °C | −260.0 / −322.6 kJ/mol | `tab_thermo.csv` → `dH(kJ/mol)` | `thermo_calc_v2.py` | Eq. 1 |
| ΔS° of R1 / R2, 600 °C | −33.1 / −17.3 J mol⁻¹ K⁻¹ | `tab_thermo.csv` → `dS(J/molK)` | `thermo_calc_v2.py` | Eq. 1 |
| Deoxidation limit, Mg (pure) | 3908 ppm O | `tab_deox.csv` → `wO_eq(ppm)`, `Mg,600` | `thermo_calc_v2.py` | Eq. 8 |
| Deoxidation limit, Ca (pure) | 20.2 ppm O | `tab_deox.csv` → `wO_eq(ppm)`, `Ca,600` | `thermo_calc_v2.py` | Eq. 8 |
| Equimolar-alloy limit, Ca | ≈77 ppm O | `tab_deox.csv` → `wO_alloy(ppm)` = 76.8 | `thermo_calc_v2.py` | Eq. 8 |
| E°(MgCl₂), E°(CaCl₂), E°(NaCl) | 2.601 / 3.428 / 3.440 V | `tab_Ed.csv` → `Ed(V)` | `thermo_calc_v2.py` | Eq. 2 |
| Co-deposition window, design melt | 120.2 mV | `tab_window.csv` → `Window(mV)`, row `Ca-rich` | `thermo_calc_v2.py` | Eq. 4–5 |
| Window under γ sensitivity | 74.9–147.1 mV | `tab_window_sensitivity.csv` (18 rows) | `thermo_calc_v2.py` | Eq. 4–5 |
| ΔG_mix, ΔH_mix, γ_Ca (equimolar) | −9.69 / −4.66 kJ/mol, 0.111 | `tab_MgCa_thermo.csv` → `dG_mix`, `dH_mix`, `gamma_Ca` | `thermo_calc_v2.py` | Eq. 6–7 |
| Material balance, Case II | 508 kg Mg, 837 kg Ca, 1668 kg TiO₂ | `tab_mbalance.csv` → `Mass(kg)` | `thermo_calc_v2.py` | Table 7 |
| Net energy, Case II / Case I | 12,552 / 12,933 kWh t⁻¹ | `tab_heat_balance_revised.csv` → `Net consumption`; `tab_case_baseline.csv` → `net` | `verification_fix.py`, `case_baseline_mc.py` | energy balance (§5.8–5.9) |
| Gross electrolysis energy | 12,244 / 12,625 kWh t⁻¹ | `tab_heat_balance_revised.csv` → `Electrolysis (gross)`; `tab_r3_reconstruction.csv` → `gross_kWh_t` | `verification_fix.py`, `revision_r3_mechanism_numbers.py` | energy balance (§5.8–5.9) |
| Regeneration enthalpy | 7,173 / 7,368 kWh t⁻¹ | `tab_case_baseline.csv` → `dH_regen` = 7175.55 / 7368.8 | `case_baseline_mc.py` | energy balance (§5.8–5.9) |
| Waste heat, net absorbed | 6,761 / 5,483 kWh t⁻¹ | `tab_heat_balance_revised.csv` → `Waste heat rejected`, `Reaction enthalpy absorbed (net)` | `verification_fix.py` | heat balance (§5.9) |
| Auxiliary thermal demand | 329 / 50 / 300 kWh t⁻¹ | `tab_heat_balance_revised.csv` → `External thermal demand`, `Salt circulation pumping`, `Post-treatment` | `verification_fix.py` | Table 9 |
| Activation-overpotential difference | 370 mV | `tab_overpotential.csv` → `effective_window_act-only` = 370.2 (at 0.5 A cm⁻²) | `verification_fix.py` | Butler–Volmer (§5.4) |
| 620 °C recomputation | 119.6 mV, <0.3% energy change | `tab_dual_temperature.csv` → `window_mV`, `net_mixed_kWh_t` | `dual_temperature.py` | 620 °C case, §5.9 |
| Ideal-solution liquidus | 544 °C | `tab_r1_liquidus_check.csv` (scan) + stdout of `verify_r1_liquidus.py` (543.7 °C at the design point) | `verify_r1_liquidus.py` | Eq. 3 |
| ΔG°(Ca+MgO→CaO+Mg) | −38.25 kJ/mol, K = 194 | `tab_r3_verification.csv` → `value` = −38.23 | `verify_r3_reviewer3.py` | Eq. 9 |
| Monte Carlo, all 18 statistics | 13,157 / 82.0% / 35.1% / 13,556 / 76.4% / 13,295 / 79.9% / 0.37 / 0.75 / 1.68 / 2.70 / 89 mV / 100% / 13.6 min | `tab_monte_carlo_v2_stats.csv` (18 rows, all quantities) | `monte_carlo_v2.py` | Eq. 15 (SCM) + energy model (§5.7) |
| j_lim,Mg = 0.56, j_lim,Ca = 0.75, j = 1.31, j_eq = 1.1 A cm⁻² | — | printed by `fig_current_regimes.py` (lines 42–44); no CSV | `fig_current_regimes.py` | Eq. 12–13 |

### 3.2 Figure → generator → EPS pipeline

**EPS file names do not match the figure numbers printed in the paper.** Three figures were
inserted into the original twelve, so `figureN.eps` appears as Fig. N+1, N+2 or N+3
depending on where the insertion falls. The mapping below is the only correct one; it
follows the `\includegraphics` order in `manuscript.tex` (lines 135, 215, 365, 439, 467,
478, 494, 515, 534, 541, 548, 555, 622, 637, 721).

| Fig. | `figures_eps/` file | Source PDF in `figures/` | Generated by | Direct EPS? |
|---|---|---|---|---|
| 1 | `figure_flowsheet.eps` | `fig_flowsheet.pdf` | `fig_flowsheet.py` | yes |
| 2 | `figure1.eps` | `fig_liquidus.pdf` | `improvements_calc.py` | no (gs) |
| 3 | `figure_r3_competition.eps` | `fig_r3_competition.pdf` | `fig_mechanism.py` | yes |
| 4 | `figure2.eps` | `fig_overpotential_bv.pdf` | `supplement_calc.py` | no (gs) |
| 5 | `figure_r3_shuttle.eps` | `fig_r3_shuttle.pdf` | `fig_mechanism.py` | yes |
| 6 | `figure3.eps` | `fig_current_regimes.pdf` | `fig_current_regimes.py` | script writes `fig_current_regimes.eps`; must be renamed to `figure3.eps` |
| 7 | `figure4.eps` | `fig_E_pO2.pdf` | `improvements_calc.py` | no (gs) |
| 8 | `figure5.eps` | `fig_scm_conversion.pdf` | `improvements_calc.py` | no (gs) |
| 9 | `figure6.eps` | `fig_scm_sensitivity.pdf` | `improvements_calc.py` | no (gs) |
| 10 | `figure7.eps` | `fig_scm_time_vs_size.pdf` | `improvements_calc.py` | no (gs) |
| 11 | `figure8.eps` | `fig_monte_carlo.pdf` | `monte_carlo_v2.py` | yes |
| 12 | `figure9.eps` | `fig_sensitivity_tornado.pdf` | `monte_carlo_v2.py` | yes |
| 13 | `figure10.eps` | `fig_voltage_split.pdf` | `supplement_calc.py` | no (gs) |
| 14 | `figure11.eps` | `fig_energy_sensitivity.pdf` | `improvements_calc.py` | no (gs) |
| 15 | `figure12.eps` | `fig_cl2_boundary.pdf` | `supplement_calc.py` | no (gs) |

Two figures in `figures/` are **not** in the manuscript: `fig_heat_balance_revised.pdf` and
`fig_overpotential_window.pdf` (both from `verification_fix.py`). They are supporting
evidence for the heat balance and the window decomposition.

"no (gs)" means the script writes a PDF and the EPS was produced once with Ghostscript:

```bash
gswin64c -dNOPAUSE -dBATCH -dEPSCrop -sDEVICE=eps2write -sOutputFile=figure1.eps fig_liquidus.pdf
```

Consequence: **editing a script and re-running it does not update the submitted figure.**
Re-run the script, then repeat the Ghostscript conversion, then rebuild the PDF.

### 3.3 Table → source

Numbers below are the printed table numbers, cross-checked against `manuscript.aux`
(`tab:compare`, `tab:window_sens`, `tab:binary`, …).

| Table | Label | Content | Source |
|---|---|---|---|
| 1 | `tab:compare` | Process-route comparison | Literature, `refs.bib` only — no computation |
| 2 | `tab:window_sens` | Co-deposition window, 18 γ pairs | `output/tab_window_sensitivity.csv`; all 18 rows independently re-integrated from Eq. 4–5, maximum deviation 0.07 mV (0.05%, i.e. the rounding of the one-decimal table) |
| 3 | `tab:binary` | Binary subsystems of the quaternary salt | Primary phase-diagram papers, §3.4 |
| 4 | `tab:thermo` | ΔG°, ΔH°, ΔS° of reduction reactions | `output/tab_thermo.csv` |
| 5 | `tab:deox` | Equilibrium oxygen content | `output/tab_deox.csv` |
| 6 | `tab:Ed` | Chloride decomposition voltages | `output/tab_Ed.csv` |
| 7 | `tab:mbalance` | Material balance | `output/tab_mbalance.csv` |
| 8 | `tab:energy` | Practical energy consumption | `output/tab_energy.csv`, `output/tab_case_baseline.csv` |
| 9 | `tab:heatbal` | Full-process heat balance | `output/tab_heat_balance_revised.csv` |
| 10 | `tab:ticl` | Gibbs energies of titanium chlorides | `barin1995`, 298 K — literature only |

### 3.4 Salt phase-diagram data: primary sources

`chartrand2000` (*Can. Metall. Q.* **39** (2000) 405–420) could not be obtained: Taylor &
Francis returns 403, Semantic Scholar marks it `CLOSED`, and OpenAlex has no record for the
DOI. Its **experimental inputs** were therefore obtained directly from the primary
literature — an upgrade, not a workaround. Four of the six rows of Table 3 are now
experimental values; two remain assessed.

| Binary | Table 3 value | Primary source | Status |
|---|---|---|---|
| MgCl₂–CaCl₂ | simple eutectic, 620 °C @ 52.8 mol% MgCl₂ | Grjotheim, Holm & Malmo, *Acta Chem. Scand.* **24** (1970) 77–86, DOI 10.3891/acta.chem.scand.24-0077 — "eutectic point at 52.8 mole % (40 weight %) MgCl₂ and 620±1 °C"; solid solubility ≈17 mol% on the CaCl₂ side | experimental |
| MgCl₂–NaCl | 445 °C; NaMgCl₃, Na₂MgCl₄ both incongruent | Grjotheim, Holm & Røtnes, *Acta Chem. Scand.* **26** (1972) 3802–3803, DOI 10.3891/acta.chem.scand.26-3802 — eutectic 445 °C @ 41.5 mol% MgCl₂ | experimental |
| MgCl₂–KCl | 426 °C; KMgCl₃, K₂MgCl₄ both congruent | same 1972 paper — eutectic 426 °C @ 31.5 mol% MgCl₂ (second point 428 °C @ 36.5 mol%) | experimental |
| CaCl₂–NaCl | 500 °C; Na₄CaCl₆ reported | Seltveit & Flood, *Acta Chem. Scand.* **12** (1958) 1030–1041, DOI 10.3891/acta.chem.scand.12-1030 — "The eutectic lies at 500 ± 2 °C and 48 mole percent NaCl" | experimental |
| CaCl₂–KCl | ~600 °C | none obtained (ScienceDirect and IOP blocked) | **assessed**; independent ideal-eutectic check gives 584 °C — same direction, same magnitude |
| NaCl–KCl | ~657 °C, continuous solid solution | none obtained; assessed value confirmed by an independent open-access study | **assessed** |

All five DOIs above were re-verified against Crossref during this revision (title, volume,
pages, year). Retrieval route for the three *Acta Chemica Scandinavica* papers: the open
archive at `actachemscand.ki.ku.dk` (the journal is open 1947–1999). They are image-only
scans — `pdftotext` returns a few bytes — so the values were read from 350 dpi page
renderings. Working copies and page PNGs are under `review_workspace/_tmp/`.

Quaternary liquidus: Hattori, Igarashi & Mochinaga, *Denki Kagaku* **53** (1985) 424–425,
DOI 10.5796/kogyobutsurikagaku.53.424. DTA on 20/50/80 mol% NaCl iso-sections; the 20 mol%
section reaches **393 °C** at 43-22-15-20 and 40-20-20-20, and the design composition
(normalised onto that section: MgCl₂ 28.2 / KCl 14.1 / CaCl₂ 37.6) falls between the
460 °C and 480 °C isotherms, hence the conservative "440–520 °C" quoted in the text.
Note: Crossref indexes the title as "**Pease** Diagram…" (a typo for "Phase" in the
original) and embeds `<sub>` tags; this is a metadata artefact, not a mis-citation.

### 3.5 Physical inputs → literature

| Parameter | Value used | Source |
|---|---|---|
| T_m: MgCl₂ / CaCl₂ / NaCl / KCl | 987 / 1045 / 1074 / 1043 K | `barin1995` |
| ΔH_fus: MgCl₂ / CaCl₂ / NaCl / KCl | 43.1 / 28.5 / 28.2 / 26.6 kJ mol⁻¹ | `barin1995` |
| Cp(T) coefficients | — | `barin1995`; supplements from `kubaschewski1979` |
| Ca–Mg liquid Redlich–Kister | L₀ = −30616 + 13.72 T, L₁ = −532 + 2.70 T J/mol | `zhang2008mgce`, cross-checked against the open SGTE set `hallstedt2025` |
| ΔG_diss(O in α-Ti) | −581,000 + 92 T J/mol | `waldner1999` (valid < 882 °C) |
| D, melt | 1.0×10⁻⁹ m² s⁻¹ | `fray2000`, `yan2007` |
| D, product layer | 1–3×10⁻⁹ m² s⁻¹ | `fray2000` |
| δ, diffusion layer | 100–500 µm, nominal 200 µm | design assumption; Spearman-dominant for L_req |
| κ, melt conductivity | 1.4 S cm⁻¹ | representative value (§5.5 of the manuscript); the MgCl₂–CaCl₂ binary measurements are `sato1999` |
| ρ, melt / M_avg | 1.8 g cm⁻³ / 92.9 g mol⁻¹ | `sato1999` (density) for the binary; quaternary value adopted |
| c(MgCl₂), c(CaCl₂) at the design melt | 5.81×10³ / 7.75×10³ mol m⁻³ | derived from ρ, M_avg, composition |
| MgO solubility | 0.5–1.2 wt% | `morita2004` |
| CaO solubility | qualitative only ("appreciably more soluble than MgO") | `wang2008cao`; the numerical value was deliberately **not** transcribed because the full text was not obtained, and the paper carries a 2017 correction |
| Activity coefficients of the salt | 0.3–1.0 (γ_CaCl₂), 0.7–1.0 (γ_NaCl) | sampled prior, `chartrand2000`, `kleppa1966` |
| Current efficiency | 0.75–0.80 nominal; Tri(0.50, 0.75, 0.88) in the MC | analogy with Downs / Hall–Héroult / MgCl₂ cells, `pletcher1990`, `kvande2014` |
| Downs electrolyte, reference composition | 66.8 wt% CaCl₂ / 33.2 wt% NaCl (≈51.5 mol% CaCl₂, "roughly equimolar") | `pletcher1990`, after Hardie 1959 |

### 3.6 Rounding conventions and basis choices

Three conventions explain every numerical difference between a CSV and the text. They are
deliberate and none of them affects a conclusion.

1. **Last-digit rounding (±1–3 kWh).** The text quotes 4 significant figures from
   integer-partitioned bookkeeping; the CSV keeps one formula's full precision. Examples:
   net Case II = 12,552 (text, from 12,594 − 42) vs 12,551.45 (`tab_case_baseline.csv`);
   net Case I = 12,933 vs 12,930.99; regeneration enthalpy = 7,173 vs 7,175.55; waste heat =
   6,761 vs 6,757.89. The spread is ≤3 kWh against an MC standard deviation of ≈1,800 kWh.
2. **Cell-voltage basis.** `manuscript.tex` uses V_cell = 4.1 V for Case II (12,244 kWh
   gross) and 4.23 V for Case I. Earlier analysis passes in `tab_r3_reconstruction.csv` and
   `tab_dual_temperature.csv` use the *summed* 4.13 V (12,330 / 12,638 kWh). Both are
   internally consistent; do not mix them in one comparison. The 620 °C statement "energy
   change < 0.3%" is quoted on the 4.13 V basis (12,638 → 12,606) and holds on 4.1 V too
   (+0.43% on a much larger base is still inside the Monte Carlo spread).
3. **Standard states.** The 120.2 mV window is quoted for **pure-solid-salt standard
   states**. The liquid-reference correction (−30 mV → ≈90 mV, worst case ≈45 mV) is given
   in the Table 2 footnote and was deliberately not propagated through the manuscript; see
   §13.

### 3.7 Known weak links

| Item | Status |
|---|---|
| `chartrand2000` full text | not obtained; its experimental inputs were obtained instead (§3.4) |
| CaCl₂–KCl ~600 °C | assessed value, no primary source (§3.4) |
| `gswin64c` EPS conversion | one-off, not scripted — 10 of the 15 submitted EPS files cannot be regenerated by running a Python script alone (§3.2) |
| `fig_current_regimes.py` | prints j_lim values but writes no CSV; the 0.56 / 0.75 / 1.31 / 1.1 A cm⁻² figures in the text are traceable to its stdout only |
| Zenodo v3 | predates the MC re-run (see §1 note) |
| `submission_jsm/` | regenerated 2026-10-19 from the current sources, cover letter included (§11) |

---

## 4. Corrections made in this revision

Every entry below is a change to a claim, a number or a citation that arose from the review
round, with the reason. The full audit (in Chinese, 19 sections) is
`review_workspace/verification_check_manuscript_v1.md`; the section numbers in the last
column point into it.

| # | What was wrong | What is right | Where |
|---|---|---|---|
| 1 | Eq. 6 wrote L₁(x_Mg − x_Ca) while the γ_Ca expression of Eq. 7 expanded L₁(3x_Ca − x_Mg) — two mutually exclusive conventions | Eq. 6 rewritten as L₁(x_Ca − x_Mg) and the convention declared in the text. Strict partial-molar re-derivation plus a Gibbs–Duhem check: γ_Ca = 0.1106 (text 0.111), ≈1832 ppm (text ≈1800 ppm), −11.5% vs regular solution (text 11%) — all unchanged | §8 |
| 2 | "decomposition voltage of TiO₂ (≈2.73 V)" | 2.73 V is the **MgO + CaO regeneration** step (4 e⁻ per mol Ti); TiO₂ itself is 2.03 V at 783 kJ/mol | §8 |
| 3 | The binary-subsystem table (Table 3) called CaMg₂Cl₆ a congruently melting compound at Mg:Ca = 2:1 that raises the liquidus by 111 °C | **Retracted.** MgCl₂–CaCl₂ is a simple eutectic: 620±1 °C at 52.8 mol% MgCl₂, ≈17 mol% solid solubility, **no compound**. Ideal model gives 607 °C at the eutectic composition (≈13 °C low, not 111), and 619.5 °C at the design ratio vs ≈622 °C measured | §12.2, §13 |
| 4 | 620 °C floor presented as a *derived requirement* | Measured quaternary liquidus is *below* the ideal 544 °C, not above it, so the ±50 °C envelope is conservative. The floor is retained as a **conservative measure**, not as a demonstrated requirement | §15 |
| 5 | "MgCl₂–CaCl₂-rich local composition adjacent to the cathode" | Direction reversed: at the Mg limiting current the interfacial Mg²⁺ concentration → 0, so it is **depletion**. Replaced by the direction-agnostic "towards the higher-melting side of the MgCl₂–CaCl₂ binary" | §16.1 |
| 6 | L ≲ 1.1 cm quoted as a fixed geometric constant while the MC median was 1.68 cm | Both recomputed: 1.125 cm at δ = 200 µm; L_req ∝ δ, so 1.69 cm at the sampled median 300 µm. The text now states the δ premise and treats δ ≤ 200 µm as a **design requirement** (stirring), not an operating convenience | §12.1, §12.4 |
| 7 | K₂ = 194 suspected of being off by one | False positive: −76.5 kJ per 2 mol MgO ⇒ −38.25 per mol MgO ⇒ K = exp(38250/RT) = 194.0. The text's −38.2 was 3-s.f. rounding; all four occurrences were changed to −38.25 and K = 194 kept | §12.3 |
| 8 | "6,761 kWh of waste heat **in addition to** the 1,690 kWh reduction exotherm" read as 8,451 | Rewritten as a three-step ledger: 12,244 − 7,173 = 5,071 in-cell, + 1,690 exotherm = 6,761 total, net retained enthalpy 5,483 (= ΔH of TiO₂ → Ti + O₂) | §12.3 |
| 9 | Table 3 MgCl₂–KCl listed ~470 °C | **426 °C** at 31.5 mol% MgCl₂ — a 44 °C hard error. Also MgCl₂–NaCl ~440 → **445**, CaCl₂–NaCl ~500 → **500±2** | §14 |
| 10 | Figure text: 3910 ppm and "12 632" | 3908 ppm and 12,625; both regenerated | §8, §18 |
| 11 | Monte Carlo used one D for both the melt and the product layer; V_cell truncated; η–j correlation sign reversed; Case I computed nowhere | D split (product layer sampled, melt fixed at the design value); V_cell ~ N(4.10, 0.25) untruncated; η_eff = η[1 − β max(j/j_ref − 1, 0)]; Case I computed explicitly. Every MC number moved: 13,141 → **13,157**; 82.1 → **82.0%**; 13,536 → **13,556**; 76.6 → **76.4%**; 13,981/65.9% → **13,295/79.9%**; j_lim,Mg 0.75 → **0.37**; L_req 0.84/1.88 → **1.68/2.70** cm | §11.3 |
| 12 | "ten parameters" in one place, eleven elsewhere | Eleven everywhere, including the Fig. 11 caption | §11.3 |
| 13 | Abstract 325 words (limit 250) | **248 words**, all 20 key numbers retained | §19.3 |
| 14 | Declarations used "Conflict of interest", not the Springer Nature heading | Changed to **"Competing interests"** with matching body text | §2 |
| 15 | This README: referenced files that do not exist, 30 refs, 11 CSV, 41 pages, 6 scripts | Rewritten against the actual tree (§1–§2 of this file) | verification §7.3, §15.4 |
| 16 | The window-sensitivity table footnote gave the liquid-reference correction as "+30 mV, reinforcing the window" | The correction **narrows** the window: E_d decreases, 120.2 → ≈90 mV, worst case 74.9 → ≈45 mV | §11.1 |
| 17 | Eq. 1 was called the "Gibbs–Helmholtz relation" | Eq. 1 is the ΔG = ΔH − TΔS definition; the Gibbs–Helmholtz relation is d(ΔG/T)/dT = −ΔH/T². The same pass confirmed that 873 K lies below both melting points (Mg 923 K, Ca 1115 K), so no solid–liquid transition is crossed by the extrapolation | §11.1 |
| 18 | The text back-calculated c_s/c_b from the 816 mV gap and then called the result "consistent" (circular), with the "well before" ordering reversed | Circularity removed and the ordering corrected | §11.1 |
| 19 | `floor` was used for four different things (580 °C target, 620 °C pilot, 3 mm gap, reactor hearth), and **L131 used it for two different temperatures inside one paragraph** — "a pilot-scale operating floor of ≥620 °C" and then "a liquidus at least 30 °C below the operating floor" (which by L211 means 580 °C) | Split into `target minimum operating temperature` (580 °C), `pilot floor` (620 °C), `gap floor` (3 mm), and the physical `cell floor`. 22 occurrences reviewed one by one; a blanket replacement would have re-attached the 30 °C criterion to 620 °C and contradicted L211 | this round |
| 20 | Case II (1:1) was called the "bounding case" and the "conservative design basis", although it yields the **lower** of the two energy figures (12,552 vs 12,933) | Rewritten as the design basis "because it places the stricter demand on the cell — two regeneration paths must both operate — and it is for that reason the lower of the two energy figures, not the more conservative one". The Case numbering is now declared historical in the Table 7 note: Case I is the mechanistically favoured limit, Case II the design basis | this round |
| 21 | The impurity paragraph argued that preferential Fe/Si reduction plus a density contrast "suggests a potential pathway for physical separation", then conceded that Fe–Ti and Si–Ti are fully miscible, and concluded with "potential compatibility" with metallurgical-grade TiO₂ | Direction reversed: preferential reduction is now stated as a **purity risk** (the impurities are reduced first and then retained in solid solution), the density argument is given as conditional on immiscibility and withdrawn, and the conclusion is "**conditionally** compatible". Conclusion (4) adjusted to match | this round |
| 22 | Four smaller clarity items: (a) CaO was called "appreciably more soluble than MgO" and, two paragraphs later, "the unresolved solubility" — true (ranking vs absolute value) but never distinguished; (b) 620 °C was said to change the figures "by only a few percent" in L131 but "by less than 0.3%" in L689, and L689 described a 0.26% *decrease* as a "cost"; (c) κ = 1.4 S cm⁻¹ was cited to `sato1999`, a MgCl₂–CaCl₂ binary study; (d) the ±50 °C upper bound (594 °C) was called conservative in one place and as leaving "no margin" in another | (a) the ranking/absolute-value distinction now stated explicitly; (b) L131 gives 0.3% (energy) and 0.5% (window), L689 no longer says "costs"; (c) attributed as "a representative value (MgCl₂–CaCl₂ binary data: sato1999)"; (d) L220 now notes that 594 °C already exceeds the 580 °C target, which is why a 620 °C pilot floor is recommended | this round |
| 23 | Six residual inconsistencies found in a final read-through, one of them introduced by entry 20 itself: (a) the abstract and conclusion (6) still called the 1:1 case the "conservative basis" after entry 20 had rewritten it as the design basis; (b) the Fig. 11 caption gave $V_{cell} \sim N(4.1, 0.3)$ while the body and `monte_carlo_v2.py` use 0.25 V; (c) the Fig. 12 caption claimed the correlations "over the eleven sampled parameters" although the script plots only those with ρ > 0.02; (d) "The competition is summarized in Fig. 3" had no explicit antecedent; (e) the abstract's closing 36-word sentence was joined to the previous one by a semicolon; (f) the submission cover letter still carried 41 pages, 30 references, −38.2 kJ/mol and 13,141 kWh/ton, and credited the 350 °C temperature saving to Kroll although 600 vs 950 °C is the FFC comparison (Kroll is 1000–1200 °C, Table 1) | (a) both now read "design basis"; (b) 0.25 V; (c) caption now says "showing only those with abs($\rho$) > 0.02"; (d) "The competition between the two reduction paths"; (e) full stop, no words added; (f) 43 pages / 35 references / −38.25 kJ/mol / 13,157 kWh/ton / 82.0%, and the temperature comparison replaced by the Table 1 values | this round |

---

## 5. Compiling the Manuscript

```bash
pdflatex manuscript
bibtex   manuscript
pdflatex manuscript
pdflatex manuscript
```

`bibtex` is required because the bibliography lives in `refs.bib` (35 entries). The
committed `manuscript.bbl` lets the PDF be rebuilt with `pdflatex` alone; delete it and the
full four-step sequence is needed again.

`latexmk` is **not** usable in this environment (MiKTeX cannot find its Perl engine); use
the four commands above. Expected result: 43 pages, 0 warnings, 0 undefined references,
0 overfull hboxes.

The manuscript references EPS figures in `figures_eps/` via `\graphicspath`; `pdflatex` +
`epstopdf` converts them on the fly. The compiled `manuscript.pdf` is not tracked in this
repository; the preprint of record is on Zenodo (DOI above), with the version caveat of §1.

Two deliberate deviations from the stock Springer template are recorded so they are not
mistaken for corruption:

- **`sn-jnl.cls`, one line.** `\bibliographystyle{sn-basic}` is changed to
  `sn-basic-reforder`. The class sets the style inside its own option block, so it cannot be
  overridden from the document, and BibTeX rejects a second `\bibstyle`. The style is chosen
  because the journal's CSL definition (`springer-basic-brackets`, which
  `journal-of-sustainable-metallurgy.csl` depends on) numbers references in citation order,
  whereas `sn-basic.bst` presorts alphabetically — with the stock style the Kroll 1937
  reference that opens the Introduction came out as [9].
- **`sn-basic-reforder.bst`.** Identical to `sn-basic.bst` except that the two `sort.key$`
  assignments (`presort`, `bib.sort.order`) are replaced by constants, which turns both
  `SORT` calls into no-ops and leaves BibTeX's citation order intact. All formatting
  functions are inherited verbatim; `scripts/make_reforder_bst.py` regenerates the file from
  the pristine one.

---

## 6. Requirements

- Python 3.8+ with `numpy`, `matplotlib` (all plotting scripts); `scipy` additionally
  required by `verification_fix.py`, `case_baseline_mc.py` and `monte_carlo_v2.py`
- `thermo_calc_v2.py` uses only the standard library (`math`, `csv`)
- A LaTeX distribution (MiKTeX or TeX Live) with the Springer Nature `sn-jnl` class and its
  dependencies (`xcolor`, `manyfoot`, `epstopdf`, `mhchem`, `booktabs`, `tabularx`,
  `multirow`, `etoolbox`, `natbib`, `hyperref`). `sn-jnl.cls` and both `.bst` files are
  vendored here, so no separate template download is needed.
- Ghostscript, only if the EPS figures must be regenerated from the source PDFs (§3.2)

```bash
pip install numpy matplotlib scipy
```

---

## 7. Script overview

**Core computation** — these produce every number in the paper and write the 17 CSVs the text draws on. (The superseded ten-parameter run and its CSV are no longer in the repository; see §11.)

| Script | Purpose | Dependencies | Output |
|---|---|---|---|
| `thermo_calc_v2.py` | Meyer–Kelly Cp, reduction thermodynamics, deoxidation limits, chloride decomposition voltages, window, material/energy balance | stdlib only | 8 CSVs |
| `verification_fix.py` | Concentration overpotential, heat balance, revised energy ledger | numpy, matplotlib, scipy | 2 CSVs + 2 figures |
| `case_baseline_mc.py` | Case I / II energy baseline with uncertainty | numpy, matplotlib, scipy | 2 CSVs (+ **overwrites Fig. 11/12 EPS with the old version** — see warning below) |
| `monte_carlo_v2.py` | Eleven-parameter Monte Carlo (N = 10⁵, seed 42); Case I, correlated variant, L_req, feasibility probabilities | numpy, matplotlib, scipy | 1 CSV + Fig. 11 + Fig. 12 |
| `improvements_calc.py` | SCM kinetics, energy sensitivity, ideal liquidus, E–pO²⁻, heat balance | numpy, matplotlib | Figs. 2, 7, 8, 9, 10, 14 |
| `supplement_calc.py` | Butler–Volmer overpotential, anode O₂/Cl₂ boundary, voltage split | numpy, matplotlib | Figs. 4, 13, 15 |
| `dual_temperature.py` | 600 / 620 / 650 °C recomputation | numpy | 1 CSV |
| `verify_r1_liquidus.py` | Independent re-derivation of the liquidus (reproduces 543.7 °C) and the salt-entrainment estimate | numpy | 1 CSV |
| `verify_r3_reviewer3.py` | Ca + MgO → CaO + Mg thermochemistry and design criteria | numpy | 1 CSV |
| `revision_r3_mechanism_numbers.py` | Numbers moved by the mechanism rebuild | numpy | 1 CSV |
| `verify_revision.py` | Text/number consistency sweep | stdlib | stdout |

**Figures** — `fig_flowsheet.py`, `fig_mechanism.py`, `fig_current_regimes.py`,
`fig_ga.py`. See §3.2 for which EPS each one owns.

**One-off / housekeeping** — `analyze_length.py`, `crossref_titles.py`,
`make_reforder_bst.py`. The 26 in-place editing scripts of the review rounds (21
`apply_*.py`, `update_readme*.py`, `fix_literal_n.py`, `patch_fig_text.py`) and the
superseded `monte_carlo_uncertainty.py` have been **moved out of the repository** into
`review_workspace/_index/legacy/`, which is not tracked. They rewrote `manuscript.tex` by
string substitution, so their embedded strings are snapshots, not the current truth;
nothing in the reproduction chain depends on them. They are retained locally only as a
record of how each edit was made.

> **⚠ Regeneration order matters.** `case_baseline_mc.py` is an earlier generation that
> *also* writes `figures_eps/figure8.eps`, `figures_eps/figure9.eps` and
> `figures/fig_monte_carlo.pdf`. Running it after `monte_carlo_v2.py` silently replaces the
> eleven-parameter figures with the ten-parameter ones. Always finish with
> `python scripts/monte_carlo_v2.py`.

---

## 8. Key results (600 °C design-basis temperature)

- Reduction thermodynamics: ΔG° = −231.0 to −307.5 kJ/mol for the three pathways (Mg, Ca,
  and combined Mg + Ca)
- Deoxidation limit: Mg → 3908 ppm O, Ca → 20.2 ppm O (193× difference); equimolar Mg–Ca
  alloy → ≈77 ppm O (design-relevant value)
- Ca²⁺/Na⁺ co-deposition window: +120.2 mV (ideal), 74.9–147.1 mV under activity-coefficient
  sensitivity; worst case ≈45 mV once the E° uncertainty (±20 / ±10 mV) is added, i.e. it
  falls below the 50 mV design threshold at the pessimistic corner
- Cathode mass transport: j_lim,Mg = 0.56 A/cm², co-deposition regime 0.56–1.31 A/cm²,
  equimolar-alloy design point j ≈ 1.1 A/cm², ohmic budget L ≲ 1.1 cm at δ = 200 µm
- Mg–Ca liquid alloy: ΔG_mix = −9.69 kJ/mol (equimolar)
- Shrinking-core kinetics: 100 µm particles reduced in 6.3 min (D = 2.0×10⁻⁹ m²/s,
  c_red = 3 mol%, the optimistic end of the sampled range); MC median 13.6 min
- **Ca reduces MgO**: ΔG°(Ca + MgO → CaO + Mg) = −38.25 kJ/mol at 600 °C, K = 194;
  consequently Ca is the thermodynamic deoxidation driver and Mg's role is to keep the
  reductant *liquid* at 600 °C (both pure metals are solid there; the Mg–Ca eutectic is
  ≈517 °C)
- **New design criteria**: the Ca-vs-MgO crossover is identically the Mg-only deoxidation
  limit (3908 ppm), and continuing below it requires a_MgO < 5 × 10⁻³
- Net energy consumption: 12,552 kWh/ton-Ti (Case II: MgO + CaO regenerated) or
  12,933 kWh/ton-Ti (Case I: CaO the sole regenerated species, +3%); conditional on
  η_I > 0.70. Case II is the design basis; Case I is the mechanistically favoured limit
  and is 3% more expensive, so the two bracket the energy claim rather than one being a
  conservative version of the other.
- Monte Carlo, eleven parameters (N = 10⁵, seed = 42): median 13,157 kWh/ton-Ti on the 1:1
  basis and 13,556 on the CaO-only basis, with P(W_net < 15,000) = 82.0% and 76.4%
  respectively; with the η–j correlation included, median 13,295 and P = 79.9%; the joint
  feasibility figure at 620 °C is 100% of samples, which carries no information beyond the
  gap constraint because the window and liquidus conditions are essentially always met
- Required interelectrode gap for the equimolar deposit: median 1.68 cm, P95 2.70 cm
  (proportional to δ; 1.1 cm is the nominal-δ value)
- 620 °C (pilot floor): window 119.6 mV (from 120.2 mV), energy change < 0.3%
- Cell architecture: Ti (4.5 g/cm³) settles through the melt (1.8 g/cm³) at ≈5 mm/s, and the
  Mg–Ca alloy (≈1.6 g/cm³) is lighter than the melt, so the product cannot be held in
  suspension; the design uses a settled TiO₂ bed on a sloped floor as the cathode, with the
  reductant electrodeposited within the bed and retained by capillarity, a shroud-isolated
  anode and semi-continuous gravity drainage
- Separation: the product inherits the precursor particle size, so screening cannot separate
  Ti from unreacted TiO₂; dry electrostatic separation (conductor vs insulator) is the
  primary step, with the oxide fraction returned to the cell

---

## 9. Data sources

All thermodynamic data are from published literature (no experimental measurements). The 35
entries are listed in full below in five groups — the grouping is for reading convenience
only; `refs.bib` is the single source of truth for metadata and DOIs.

**A. Phase diagrams and salt thermodynamics** (9)

| Key | Reference | Used for |
|---|---|---|
| `grjotheim1970` | Grjotheim K, Holm JL, Malmo J. The phase diagram of the system MgCl₂–CaCl₂… *Acta Chem. Scand.*, 1970, 24: 77–86 | MgCl₂–CaCl₂ eutectic 620±1 °C @ 52.8 mol% (Table 3) |
| `grjotheim1972` | Grjotheim K, Holm JL, Røtnes M. The phase diagrams of the systems NaCl–MgCl₂ and KCl–MgCl₂. *Acta Chem. Scand.*, 1972, 26: 3802–3803 | 445 °C and 426 °C eutectics; compound identities |
| `seltveit1958` | Seltveit A, Flood H. Determination of the solidus curve by a tracer technique. The system CaCl₂–NaCl. *Acta Chem. Scand.*, 1958, 12: 1030–1041 | 500±2 °C eutectic; Na₄CaCl₆ |
| `hattori1985` | Hattori T, Igarashi K, Mochinaga J. Phase diagram of quaternary KCl–NaCl–CaCl₂–MgCl₂. *Denki Kagaku*, 1985, 53: 424–425 | quaternary DTA; 393 °C minimum; 440–520 °C isotherms at the design composition |
| `chartrand2000` | Chartrand P, Pelton AD. Thermodynamic evaluation and optimization of the LiCl–NaCl–KCl–RbCl–CsCl–MgCl₂–CaCl₂–SrCl₂ system… *Can. Metall. Q.*, 2000, 39(4): 405–420 | assessed CaCl₂–KCl and NaCl–KCl values; activity-coefficient priors |
| `pelton2000mqm` | Pelton AD, Degterov SA, Eriksson G, Robelin C, Dessureault Y. The modified quasichemical model I — Binary solutions. *Metall. Mater. Trans. B*, 2000, 31(4): 651–659 | MQM framework behind the assessed diagrams |
| `kleppa1966` | Kleppa OJ, McCarty FG. Thermochemistry of charge-unsymmetrical binary fused halide systems II. *J. Phys. Chem.*, 1966, 70(4): 1249–1255 | MgCl₂–alkali chloride ΔH_mix; γ priors |
| `morita2004` | Ito M, Morita K. The solubility of MgO in molten MgCl₂–CaCl₂ salt. *Mater. Trans.*, 2004, 45(8): 2712–2718 | S_MgO = 0.5–1.2 wt% |
| `wang2008cao` | Wang S, Zhang F, Liu X, Zhang L. CaO solubility and activity coefficient in molten salts CaCl₂–x. *Thermochim. Acta*, 2008, 470: 105–107 (corrected 2017: **654**: 51–53) | CaO solubility, qualitative only (§3.5) |

**B. Thermochemical and transport data** (6)

| Key | Reference | Used for |
|---|---|---|
| `barin1995` | Barin I. *Thermochemical Data of Pure Substances*, 3rd ed. VCH, 1995 | Cp(T), ΔH°f, S°; T_m and ΔH_fus of the four salts; Table 10 |
| `kubaschewski1979` | Kubaschewski O, Alcock CB. *Metallurgical Thermochemistry*, 5th ed. Pergamon, 1979 | supplementary Cp(T) coefficients |
| `waldner1999` | Waldner P, Eriksson G. Thermodynamic modelling of the system titanium–oxygen. *Calphad*, 1999, 23(2): 189–218 | ΔG_diss(O in α-Ti), valid < 882 °C |
| `hallstedt2025` | Hallstedt B. The SGTE collection of binary datasets. *Calphad*, 2025, 89: 102833 | open-access SGTE binaries; independent cross-check of the Ca–Mg parameters |
| `littlewood1962` | Littlewood R. Diagrammatic representation of the thermodynamics of metal–fused chloride systems. *J. Electrochem. Soc.*, 1962, 109: 525–534 | E–pO²⁻ diagram construction (Fig. 7) |
| `sato1999` | Sato Y, Kuroda Y, Nagatsu T, Hoshi M, Kim J-I, Yamamura T. Density and electrical conductivity of molten MgCl₂–CaCl₂ binary melt. 1999, p. 313 | melt density 1.8 g cm⁻³ and the conductivity scale behind κ = 1.4 S cm⁻¹ |

**C. Alloy thermodynamics** (2)

| Key | Reference | Used for |
|---|---|---|
| `nayeb1987` | Nayeb-Hashemi AA, Clark JB. The Ca–Mg (calcium-magnesium) system. *Bull. Alloy Phase Diagr.*, 1987, 8: 58–65 | Ca–Mg phase diagram; Mg₂Ca; eutectic ≈517 °C |
| `zhang2008mgce` | Zhang H, Wang Y, Shang SL, Chen L-Q, Liu Z-K. Thermodynamic modeling of the Mg–Ca–Ce system… *J. Alloys Compd.*, 2008, 463: 294–301 | Ca–Mg Redlich–Kister L₀, L₁ (Eq. 6) |

**D. Titanium production routes** (13)

| Key | Reference | Used for |
|---|---|---|
| `kroll1937` | Kroll WJ. Verformbares Titan und Zirkon. *Z. Anorg. Allg. Chem.*, 1937, 234: 42–50 | the historical baseline of the Introduction |
| `ji2026` | Ji H, Guo S, Gao L, Yang L, Yan H, Zeng H. Revolutionizing titanium production: a comprehensive review… *Int. J. Miner. Metall. Mater.*, 2026, 33: 15–34 | route survey |
| `fray2000` | Chen GZ, Fray DJ, Farthing TW. Direct electrochemical reduction of TiO₂ to Ti in molten calcium chloride. *Nature*, 2000, 407: 361–364 | FFC process; D references |
| `ono2002` | Ono K, Suzuki RO. A new concept for producing Ti sponge: calciothermic reduction. *JOM*, 2002, 54: 59–61 | OS process |
| `pal2001` | Pal UB, Woolley DE, Kenney GB. Emerging SOM technology… *JOM*, 2001, 53: 32–35 | SOM route |
| `okabe1997` | Okabe TH, Waseda Y. Producing titanium through an electronically mediated reaction. *JOM*, 1997, 49: 28–32 | EMR route |
| `zhang2024` | Zhang J, Yan H, Liu Z, Guo S, et al. Review — progress in molten salt electrolysis for titanium extraction. *J. Electrochem. Soc.*, 2024, 171: 082502 | electrolysis review |
| `jiao2023` | Jiao H, Liu M, Wang Z, Lin M, Qu Z, Song J, Jiao S. Upcycling of titanium by molten salt electrorefining. *ACS Sustain. Chem. Eng.*, 2023, 11: 5764–5772 | USTB electrorefining |
| `taninouchi2016` | Taninouchi Y, Hamanaka Y, Okabe TH. Electrochemical deoxidation of titanium and its alloy using molten MgCl₂. *Metall. Mater. Trans. B*, 2016, 47: 3394–3404 | MgCl₂ electrochemical deoxidation |
| `lee2025` | Lim KS, Nersisyan H, Han SK, Park K-T, Suh H, Lee JH. Thermochemical response of TiO₂ upon heating with CaMg₂ reductant. *Next Mater.*, 2025, 8: 100803 | CaMg₂ as a reductant |
| `pang2024` | Pang J, Kong L-X, Zhu L-G, Xu B-Q, Xu J-J, Bai C-L, Yang B. Preparation of ultralow-oxygen titanium by direct reduction of TiO₂. *Trans. Nonferr. Met. Soc. China*, 2024, 34: 681–693 | low-oxygen Ti; oxygen targets |
| `xu2025` | Zhu L, Zhang Z, Kong L, Xu B, Yang B. Clean production of low-oxygen titanium powder through MSE-MR of TiO₂. *Electrochim. Acta*, 2025, 533: 146478 | combined electrolysis + magnesiothermic route |
| `tang2015` | Tang H, Ren Y, Wang S, Deng H, Cai D, Shao L, Zhao Y, Gao R, Yan Y, Zhang M. Electrochemical co-deposition of Mg–Ca alloys from KCl–CaCl₂–MgCl₂ melts. *J. Electrochem. Soc.*, 2015, 162: D520–D524 | the closest prior co-deposition work |

**E. Electrolysis engineering** (5)

| Key | Reference | Used for |
|---|---|---|
| `pletcher1990` | Pletcher D, Walsh FC. *Industrial Electrochemistry*, 2nd ed. Chapman & Hall, 1990 | Downs cell composition (66.8 wt% CaCl₂) and 70–90% current efficiency |
| `kvande2014` | Kvande H, Drabløs PA. The aluminum smelting process and innovative alternative technologies. *J. Occup. Environ. Med.*, 2014, 56: S23–S32 | Hall–Héroult comparison; η_I = 90–95% reference |
| `levenspiel1999` | Levenspiel O. *Chemical Reaction Engineering*, 3rd ed. Wiley, 1999 | shrinking-core model formulation (Eq. 15) |
| `yan2007` | Yan XY, Fray DJ. Fused salt electrolytic reduction of solid oxides and oxide mixtures… *Miner. Process. Extr. Metall.*, 2007, 116: 17–24 | O²⁻ diffusivity |
| `song2024` | Song Z, Zhao J, He Z, Lu G. Rare earth chlorides in low-hydration magnesium chloride electrolysis. *J. Electrochem. Soc.*, 2024, 171: 062501 | MgCl₂-cell electrolysis practice |

Full metadata, including DOIs, is in `refs.bib`; verification status is in §10.

---

## 10. Reference verification status

Every entry was checked at Crossref during the review round
(`review_workspace/_index/verify_refs.py`), and the five entries added late (the three
*Acta Chemica Scandinavica* papers, Hattori 1985, Wang 2008) were re-checked individually.

| Result | Count | Note |
|---|---|---|
| DOI resolves, title/volume/pages/year match | 29 | — |
| Book, no DOI | 4 | `barin1995`, `kubaschewski1979`, `pletcher1990`, `levenspiel1999` |
| Low string similarity, manually reviewed | 2 | `morita2004` (Crossref title carries `<SUB>` tags) and `chartrand2000` (Crossref truncates the title at "…LiCl–NaCl–KCl–RbCl–CsCl"; the full title includes MgCl₂–CaCl₂–SrCl₂, which covers all six binaries of Table 3). Both are metadata artefacts, not errors. |
| **Total** | **35** | 35 `\bibitem` entries, no unused key, no undefined citation |

Two further checks worth recording:

- `ji2026`: Crossref `issued` = 2025 while the bib records 2026 (volume year). Online-first
  vs volume-year difference; keep as is.
- `hattori1985`: Crossref title reads "**Pease** Diagram…" (original typo) with `<sub>`
  tags. The citation is correct.

---

## 11. Superseded or stale artifacts

Do not quote any of these as the current state.

| Artifact | Why it is stale |
|---|---|
| `review_workspace/_index/legacy/tab_monte_carlo_stats.csv` | Ten-parameter MC: 13,141 / 82.1% / 13,536 / 76.6%. Moved out of the repository with its generator (see §7) |
| `output/tab_monte_carlo_case.csv` | The same superseded run (13,141 / 13,536), but this one is rewritten by `case_baseline_mc.py`, which is retained; the file is regenerated on every run, not quoted |
| `manuscript_v1.tex` | The frozen 825-line manuscript that was reviewed, before the 22 corrections of §4. Useful for diffing only |
| `review_workspace/_index/legacy/` | The 26 one-off editing scripts and the ten-parameter MC output, kept locally but out of the repository (§7) |
| `output/tab_r3_reconstruction.csv`, `output/tab_dual_temperature.csv` | 4.13 V basis, not the 4.1 V of the text (§3.6) |
| `figures/fig_monte_carlo.pdf`, `figures/fig_sensitivity_tornado.pdf` | Overwritten by whichever MC script ran last; check the EPS, not the PDF, if in doubt |

Regenerating the submission package after any of the above:

```bash
cp manuscript.tex manuscript.bbl manuscript.pdf refs.bib sn-jnl.cls \
   sn-basic.bst sn-basic-reforder.bst Orcidlogo-mark.pdf GA_process.png submission_jsm/
cp figures_eps/figure*.eps figures_eps/figure_flowsheet.eps \
   figures_eps/figure_r3_*.eps submission_jsm/
```

As of 2026-10-19 the package **is** current and needs no hand editing: 43 pages, 35 references,
−38.25 kJ/mol, 13,157 kWh/ton-Ti and 82.0%, with the cover letter recompiled from the same
sources. Two errors were corrected in the letter while doing so — the Monte Carlo median
(13,141) and a "350 °C relative to the Kroll process" saving that had in fact been measured
against FFC (~950 °C); the letter now quotes the Table 1 values (1000–1200 °C). Re-run these
only after further edits:

```bash
cd submission_jsm && pdflatex manuscript.tex && pdflatex manuscript.tex
cd submission_jsm && pdflatex cover_letter.tex && pdflatex cover_letter.tex
```

---

## 12. Review and verification record

`review_workspace/` holds the full audit. It is excluded from git (`.gitignore`) because it
contains rendered page images, downloaded PDFs and agent reports; it is kept locally so that
every claim in §4 can be traced to evidence.

### 12.1 How the 97 review findings were adjudicated

The input was 97 deduplicated P1 findings plus 5 P0 candidates and 14 META observations.
Each was checked against the text, the CSVs and an independent recomputation. The verdict
distribution is the record of what was **not** changed and why:

| Verdict | Count | Meaning |
|---|---|---|
| Confirmed (real defect) | 41 | Direct textual or numerical evidence |
| Partly valid | 17 | Phenomenon real, severity or location overstated |
| **Rejected (reviewer misjudgement)** | 7 | Counter-evidence exists; see §12.2 |
| Already disclosed by the paper | 12 | Should be downgraded to an editorial suggestion |
| Not verifiable offline | 2 | Both later closed (§12.3) |
| Not covered individually | 17 | Duplicates of other items, or script hygiene |

One adjudication was itself reversed during the round: the finding that the Monte Carlo
used "0.75/1.49" with a second set of numbers was first rejected as a confusion of two
different physical quantities, then found to be **correct** — the MC really did use a single
sampled D for both the melt and the product layer. Entry 11 of §4 is the consequence. It is
recorded here rather than quietly fixed because the same reversal could recur.

### 12.2 Reviewer findings that were rejected

Listed so that no one re-fixes them. All seven were checked against the text. (An eighth
finding — that the Monte Carlo used one `D` for both the melt and the product layer — was
first rejected and later reinstated as partly valid; it is recorded under §4 entry 11
rather than here.)

| Finding | Why rejected |
|---|---|
| "NaCl–KCl labelled *solid solution* is inconsistent with the usual assessment" | NaCl–KCl **is** the classic continuous-solid-solution system; the reviewer's "simple eutectic" claim is the error |
| "Al₂O₃ theoretical decomposition voltage should be 1.6–1.8 V" | ≈2.2 V is the standard value on an inert-anode/O₂ basis; the text is right |
| "ΔH = −4.66 and −7.65 coexist with an undefined basis" | Both are labelled (frozen-Ω vs Kirchhoff-corrected) and ΔS is self-consistent with them |
| "*first proposal* conflicts with `tang2015`" | The claim is hedged twice ("to the authors' knowledge", "at the process-integration level") and `tang2015` is cited where it matters |
| "Case I gross 12,632 appears in the body" | 12,632 appears only in scripts and figure text; the body says 12,625 throughout. The real defect was the figure, fixed separately |
| "The energy advantage is claimed despite unvalidated η_I" | "Conditional on η_I > 0.70" appears six times, and the text states that the 82% probability largely restates the prior |
| "Ideal-solution Eq. 3 is applied outside its validity" | The deviation direction is argued binary by binary and bounded at ±50 °C with a ≥620 °C recommendation |

Two further items were downgraded rather than rejected: Eq. 23's activity thresholds are
explicitly labelled as back-substitutions, not measured oxoacidities; and the
"oversized paragraph" finding is true for exactly one paragraph (`L131`), not several.

### 12.3 Items closed during the round

- **Zenodo DOI.** Resolves to record 21973469, v3 (2026-09-02). Title and all numbers match
  the submitted version except the MC pair noted in §1.
- **GitHub repository.** `huyamingc/ti-in-situ-electrolysis` is public and reachable (27
  commits at the time of writing).
- **`response_and_resubmission_v1.md`.** Does not exist; the earlier README reference to it
  was stale and has been removed (§4 entry 14).

### 12.4 Record structure

| File | Content |
|---|---|
| `verification_check_manuscript_v1.md` | **The primary record** (19 sections, Chinese): judgment summary, confirmed defects, reviewer misjudgements, the seven-batch fix log, the citation audit, the CaMg₂Cl₆ retraction, the Table 3 re-verification against primary phase diagrams, the quaternary-DTA re-reading, the Monte Carlo re-run, and the format/abstract compliance pass |
| `dedup_result_manuscript_v1.md` | The 97 deduplicated P1 findings that were verified |
| `review_report_manuscript_v1.html` | Rendered review report (same 97 findings) |
| `meta_review_manuscript_v1.md` | Meta-level review of the review itself |
| `agent_a…agent_f_result_manuscript_v1*.md` | The six per-aspect review shards (formulas, physics, chemistry, data, structure, scripts) |
| `agent_a_result_manuscript_v1_recovered.md` | Recovered A-shard output (18 records had been corrupted to U+FFFD and were unrecoverable; the shard was re-run) |
| `journal_requirements_manuscript_v1.md` | Journal scope, abstract limit, declarations checklist |
| `review_workspace/_index/check_format.py` | Format compliance check (abstract word count, keywords, bibitem/key match) |
| `review_workspace/_index/shorten_abstract.py` | Abstract compression with a hard 250-word guard |
| `review_workspace/_index/compress_L220.py`, `review_workspace/_index/compress_L306.py`, `review_workspace/_index/compress_lim4.py` | The three paragraph compressions (444 words saved) |
| `review_workspace/_index/mc_deltaG_check.py` | Two-arm MC showing that adding ΔG° uncertainty as a twelfth parameter changes the median by +0.4 kWh |
| `review_workspace/_index/verify_refs.py`, `scripts/crossref_titles.py`, `scripts/crossref_results.json`, `scripts/crossref_report.txt` | Crossref verification of the bibliography |
| `review_workspace/_index/a_rerun_todo.md` | Disposition of the 12 A-shard items that needed an author decision |
| `review_workspace/_tmp/` | Downloaded primary sources (`review_workspace/_tmp/acta2.pdf` = Grjotheim 1970, `review_workspace/_tmp/acta26.pdf`, `review_workspace/_tmp/acta12.pdf`, `review_workspace/_tmp/quat1985.pdf`), 350 dpi page renders, figure crops, `review_workspace/_tmp/fig2_zoom.png` |

Reproduce the checks:

```bash
python review_workspace/_index/check_format.py
python review_workspace/_index/verify_refs.py
python review_workspace/_index/mc_deltaG_check.py
python review_workspace/_index/verify_findings.py
```

---

## 13. Limitations and open items

The manuscript lists **twelve** numbered limitations (§6 of the paper); they are the
authoritative list. The five that most directly bound the computed results are:

1. CALPHAD database validation (liquidus + exact activity coefficients)
2. Electrode kinetic parameters j₀ / α (requires cyclic voltammetry)
3. Pilot-scale experimental validation (current efficiency, product purity, anode lifetime)
4. Impurity separation energy (requires experimental impurity phase distribution)
5. Current-efficiency verification (requires pilot electrolysis cell measurement)

The remaining seven — Mg–Ca interaction parameter, oxide solubility, Ca–MgO interfacial
kinetics, reactor engineering, product separation chain, engineering factors and the
current-efficiency assumption — are stated in the same section of the paper.

The current-efficiency assumption (η_I = 0.75–0.80) is an unvalidated hypothesis anchored to
the Hall–Héroult, Downs and industrial MgCl₂-electrolysis analogies, and is the dominant
uncertainty in the energy estimate (Monte Carlo Spearman ρ = −0.85). Adding the η–j
correlation raises the median net consumption to 13,295 kWh/ton-Ti and lowers
P(W_net < 15,000) to 79.9%.

Two quantities are deliberately outside the sampled set, with the reason recorded:

- **ΔG_f(MgO), ΔG_f(CaO).** ±1.5 kJ/mol each ⇒ σ = 2.12 kJ/mol-Ti ⇒ σ(E) = 5.5 mV, 45×
  smaller than the 250 mV assigned to V_cell. Added explicitly as a twelfth parameter in a
  check run, the median moves by +0.4 kWh (0.003%) and the probabilities by 0.0001 — below
  the sampling noise of 10⁵ draws. The check is reported in the manuscript rather than
  promoting the term to a twelfth sampled parameter.
- **Liquid-standard-state conversion of the co-deposition window.** Converting the whole
  chain to liquid reference states would move 120.2 mV to ≈90 mV and touch Eq. 4–5, all 18
  rows of Table 2, the abstract and conclusion (2). The current value is explicitly labelled
  "pure-solid-salt standard states" and the correction is given in the Table 2 footnote
  (window narrows ≈30 mV, worst case 74.9 → ≈45 mV), so the reader can convert. Deferred
  unless a referee asks for it.

The two quantities that cannot be computed at all — the 600 °C CaO solubility and the
interfacial kinetics of Ca + MgO → CaO + Mg — are identified as the pivotal measurements,
with go/no-go criteria stated so that the design basis can be falsified by a small number of
experiments.

---

## 14. Reproduction checklist

From a clean checkout, in this order:

```bash
# 1. Numbers (writes the 17 CSVs in output/)
python scripts/thermo_calc_v2.py                 # 8 CSV
python scripts/verification_fix.py               # 2 CSV + 2 supporting figures
python scripts/case_baseline_mc.py               # 2 CSV (energy baseline)
python scripts/dual_temperature.py               # 1 CSV
python scripts/verify_r1_liquidus.py             # 1 CSV, prints 543.7 C
python scripts/verify_r3_reviewer3.py            # 1 CSV
python scripts/revision_r3_mechanism_numbers.py  # 1 CSV

# 2. Monte Carlo LAST (it owns Fig. 11/12)
python scripts/monte_carlo_v2.py                 # 1 CSV + figure8.eps + figure9.eps

# 3. Figures
python scripts/improvements_calc.py
python scripts/supplement_calc.py
python scripts/fig_flowsheet.py
python scripts/fig_mechanism.py
python scripts/fig_current_regimes.py
python scripts/fig_ga.py

# 4. Ghostscript conversion for nine figures, plus one rename (Fig. 6) (§3.2)
#    figure1 <- fig_liquidus, figure2 <- fig_overpotential_bv,
#    figure4 <- fig_E_pO2, figure5 <- fig_scm_conversion,
#    figure6 <- fig_scm_sensitivity, figure7 <- fig_scm_time_vs_size,
#    figure10 <- fig_voltage_split, figure11 <- fig_energy_sensitivity,
#    figure12 <- fig_cl2_boundary, figure3 <- fig_current_regimes (rename)

# 5. Manuscript
pdflatex manuscript && bibtex manuscript && pdflatex manuscript && pdflatex manuscript
```

Expected: 43 pages, 3,292,491 B, 0 warnings, 0 undefined references, 0 overfull hboxes.

Check against the committed CSVs by diffing `output/` — the numbers are seeded
(`seed = 42`) and otherwise deterministic, so the CSVs should reproduce exactly except for
the drift documented in §3.6.
