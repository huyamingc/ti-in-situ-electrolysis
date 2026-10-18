"""Second pass on the page-1 overflow.

Pass 1 trimmed the abstract but the keyword block still broke across two
lines and still fell to page 2.  Here the keyword block is set in \\small
so it fits one line, the gap above it is reduced, and a further ~10 words
come out of the abstract.
"""

from pathlib import Path

PATH = Path(__file__).resolve().parent.parent / "manuscript.tex"

EDITS = [
    (
        "\\vspace{0.5em}\n\\noindent\\textbf{Keywords:} titanium production; molten salt electrolysis; Mg--Ca co-deposition; deoxidation; process design",
        "\\vspace{0.2em}\n\\small\\noindent\\textbf{Keywords:} titanium production; molten salt electrolysis; Mg--Ca co-deposition; deoxidation; process design",
        1,
        "keywords: \\small + tighter gap",
    ),
    (
        r"the net equivalent energy consumption is 12{,}552~kWh/ton-Ti, or 12{,}933~kWh/ton-Ti ($+$3\%) if CaO rather than a MgO--CaO mixture is regenerated",
        r"the net equivalent energy is 12{,}552~kWh/ton-Ti, or 12{,}933~kWh/ton-Ti ($+$3\%) if CaO rather than MgO--CaO is regenerated",
        1,
        "abstract: drop 'consumption' and 'a mixture'",
    ),
    (
        r"on the interfacial kinetics that decide whether MgO is regenerated electrolytically or reduced chemically by Ca",
        r"on whether MgO is regenerated electrolytically or reduced chemically by Ca",
        1,
        "abstract: tighten the interfacial-kinetics clause",
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
