"""Apply the verified P1/P2 fixes to manuscript.tex.

Each edit asserts an exact occurrence count so a silent no-op or a double
replacement fails loudly instead of leaving the file half-patched.

Edits
-----
P1-1  Monte Carlo parameter count: the sampler draws eleven parameters
      (D, eps, tau, eta_I, V_cell, gamma_CaCl2, gamma_NaCl, T_liq, S_MgO,
      delta, c_red -- see monte_carlo_v2.py lines 43-53 and the vstack on
      line 127), but both the paragraph and the figure caption said "ten"
      and the second group was announced as "five" while listing six.
P1-5  Abstract quoted P(W<15,000) = 82.1% without the qualifier that the
      body, Limitations (9) and Conclusions (6) all carry: the number
      restates the assumed eta_I prior rather than being independent.
P1-6  Limitations (10) said the net energy "is 3% lower" without naming the
      baseline; the 3% is relative to the 12,933 kWh/ton-Ti CaO-only value.
P2-a  Table 2 pooled six binary phase diagrams under a textbook
      (pletcher1990) as well as the actual assessment (chartrand2000);
      the textbook does not supply phase-diagram data.
P2-f  No keywords were given anywhere in the manuscript.
"""

from pathlib import Path

PATH = Path(__file__).resolve().parent.parent / "manuscript.tex"

EDITS = [
    # P1-1: Monte Carlo parameter count
    (
        "sampled ten parameters simultaneously",
        "sampled eleven parameters simultaneously",
        1,
        "P1-1 paragraph: ten -> eleven",
    ),
    (
        "Five further parameters cover the quantities",
        "Six further parameters cover the quantities",
        1,
        "P1-1 paragraph: Five -> Six further",
    ),
    (
        r"Monte Carlo global uncertainty analysis ($N = 10^5$, ten parameters)",
        r"Monte Carlo global uncertainty analysis ($N = 10^5$, eleven parameters)",
        1,
        "P1-1 figure caption: ten -> eleven",
    ),
    # P1-5: abstract qualifier on the 82.1% figure
    (
        r"($P(W<15{,}000) = 82.1\%$ and 76.6\%). All results are theoretical",
        r"($P(W<15{,}000) = 82.1\%$ and 76.6\%, a figure that mainly restates the assumed $\eta_I$ prior rather than an independent feasibility estimate). All results are theoretical",
        1,
        "P1-5 abstract: qualify the 82.1% figure",
    ),
    # P1-6: name the baseline of the 3% difference
    (
        r"if it proves slow, the 1:1 limit is recovered and the net energy is 3\% lower.",
        r"if it proves slow, the 1:1 limit is recovered and the net energy falls to 12{,}552~kWh/ton-Ti, 3\% below the 12{,}933~kWh/ton-Ti CaO-only value.",
        1,
        "P1-6 Limitations (10): name the 3% baseline",
    ),
    # P2-d: Table 2 sources -- phase diagrams come from chartrand2000 only
    (
        r"summarizes the six binary subsystems from the phase-diagram literature \cite{chartrand2000,pletcher1990}:",
        r"summarizes the six binary subsystems from the assessed phase diagrams of Chartrand and Pelton \cite{chartrand2000}:",
        1,
        "P2-d body: drop the textbook from the phase-diagram citation",
    ),
    (
        r"(literature compilation \cite{chartrand2000,pletcher1990})",
        r"(assessed phase diagrams \cite{chartrand2000})",
        1,
        "P2-d caption: drop the textbook from the phase-diagram citation",
    ),
    # P2-f: keywords block
    (
        "\\end{abstract}\n\n\\newpage",
        "\\end{abstract}\n\n\\vspace{0.5em}\n\\noindent\\textbf{Keywords:} titanium production; molten salt electrolysis; Mg--Ca co-deposition; deoxidation thermodynamics; process design; uncertainty quantification\n\n\\newpage",
        1,
        "P2-f: add a keywords line after the abstract",
    ),
]


def main() -> int:
    text = PATH.read_text(encoding="utf-8")
    original = text
    failures = []

    for old, new, expected, label in EDITS:
        count = text.count(old)
        if count != expected:
            failures.append(f"{label}: expected {expected} occurrence(s), found {count}")
            continue
        text = text.replace(old, new, expected)
        print(f"OK   {label}")

    if failures:
        print("\nABORTED -- no changes written:")
        for f in failures:
            print("  FAIL " + f)
        return 1

    if text == original:
        print("\nNo changes made.")
        return 1

    PATH.write_text(text, encoding="utf-8")
    print(f"\nWrote {PATH}  ({len(original)} -> {len(text)} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
