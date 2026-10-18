"""Reclaim the page lost when the keywords block was added.

The keywords line landed on page 2 because page 1 was already full, pushing
the whole document from 54 to 55 pages.  Two changes pull it back:

  * trim ~18 words of redundancy from the abstract (254 -> ~236 words,
    which also brings it inside the usual 200-250 word window);
  * shorten the keyword list so it typesets on one line instead of two.

Every replacement is asserted to occur exactly once.
"""

from pathlib import Path

PATH = Path(__file__).resolve().parent.parent / "manuscript.tex"

EDITS = [
    (
        r"Thermodynamic calculations at 600~$^{\circ}$C give $\Delta G^{\circ} = -231.0$ to $-307.5$~kJ/mol for the reduction pathways, with equilibrium deoxidation limits of 3908~ppm O for Mg and 20.2~ppm for Ca, the latter rising to $\approx$77~ppm at the equimolar alloy activity.",
        r"Thermodynamics at 600~$^{\circ}$C gives $\Delta G^{\circ} = -231.0$ to $-307.5$~kJ/mol for the reduction pathways, with deoxidation limits of 3908~ppm O for Mg and 20.2~ppm for Ca ($\approx$77~ppm at the equimolar alloy activity).",
        1,
        "abstract: tighten the deoxidation-limit clause",
    ),
    (
        r"---both pure metals are solid at 600~$^{\circ}$C, the Mg--Ca eutectic melting at $\approx$517~$^{\circ}$C---and reaching the deep-deoxidation limit then requires $a_{\ce{MgO}} < 5\times10^{-3}$.",
        r"(both pure metals are solid at 600~$^{\circ}$C; the Mg--Ca eutectic melts at $\approx$517~$^{\circ}$C), reaching the deep-deoxidation limit only when $a_{\ce{MgO}} < 5\times10^{-3}$.",
        1,
        "abstract: tighten the eutectic aside",
    ),
    (
        r"---the limit favoured by the mechanism analysis, since",
        r"---the mechanistically favoured limit, since",
        1,
        "abstract: tighten the Case I phrasing",
    ),
    (
        r"Monte Carlo analysis gives medians of 13{,}141 and 13{,}536~kWh/ton-Ti for the two bases",
        r"Monte Carlo gives medians of 13{,}141 and 13{,}536~kWh/ton-Ti",
        1,
        "abstract: tighten the Monte Carlo sentence",
    ),
    (
        r"a figure that mainly restates the assumed $\eta_I$ prior rather than an independent feasibility estimate",
        r"which mainly restates the assumed $\eta_I$ prior",
        1,
        "abstract: shorten the qualifier added in the previous pass",
    ),
    (
        r"\noindent\textbf{Keywords:} titanium production; molten salt electrolysis; Mg--Ca co-deposition; deoxidation thermodynamics; process design; uncertainty quantification",
        r"\noindent\textbf{Keywords:} titanium production; molten salt electrolysis; Mg--Ca co-deposition; deoxidation; process design",
        1,
        "keywords: shorten to a single typeset line",
    ),
]


def main() -> int:
    text = PATH.read_text(encoding="utf-8")
    original = text
    failures = []

    for old, new, expected, label in EDITS:
        count = text.count(old)
        if count != expected:
            failures.append(f"{label}: expected {expected}, found {count}")
            continue
        text = text.replace(old, new, expected)
        print(f"OK   {label}")

    if failures:
        print("\nABORTED -- nothing written:")
        for f in failures:
            print("  FAIL " + f)
        return 1

    PATH.write_text(text, encoding="utf-8")
    print(f"\nWrote {PATH}  ({len(original)} -> {len(text)} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
