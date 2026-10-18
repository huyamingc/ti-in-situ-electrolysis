"""Adapt the manuscript from ECS/JES conventions to Journal of Sustainable Metallurgy (Springer).

Two independent transforms:

1. Reference style.  The bibliography is a hand-written ``thebibliography``
   in ECS form ``Journal, VOL, PAGE (YEAR).``.  Springer's numeric style is
   ``Journal VOL, PAGE (YEAR).`` for articles and
   ``Title, N edn (Publisher, City, YEAR).`` for books.  Only the
   journal/volume separator and the book tail are touched -- author lists
   and titles are left exactly as they were.

2. Front/back matter.  Springer requires an ORCID at the author affiliation
   and a full Declarations block (ethics approval and consent statements are
   mandatory even when "not applicable").

Every reference line must transform; an unconverted line aborts the run so a
silent partial migration is impossible.
"""

import re
from pathlib import Path

PATH = Path(__file__).resolve().parent.parent / "manuscript.tex"

JOURNAL = re.compile(r", (\d+), ([A-Za-z]?\d+[A-Za-z]?) \((\d{4})\)\.$")
BOOK = re.compile(r", (\d+(?:st|nd|rd|th)) ed\., (.+), ([^,]+) \((\d{4})\)\.$")

SATO_OLD = (
    "Y. Sato, Y. Kuroda, T. Nagatsu, M. Hoshi, J.-I. Kim, and T. Yamamura, "
    "in Molten Salts XII, P. C. Trulove, H. C. DeLong, G. R. Stafford, and S. Deki, "
    "Editors, PV 99-41, p. 313, The Electrochemical Society Proceedings Series, "
    "Pennington, NJ (1999)."
)
SATO_NEW = (
    "Y. Sato, Y. Kuroda, T. Nagatsu, M. Hoshi, J.-I. Kim, and T. Yamamura, "
    "in Molten Salts XII, PV 99-41 (The Electrochemical Society, Pennington, NJ, 1999), "
    "p. 313."
)


def convert_refs(text: str) -> tuple[str, list[str]]:
    start = text.index("\\begin{thebibliography}{99}")
    end = text.index("\\end{thebibliography}") + len("\\end{thebibliography}")
    block = text[start:end]

    lines = block.split("\n")
    out = []
    converted = 0
    problems = []

    for line in lines:
        if not line.startswith("\\bibitem"):
            out.append(line)
            continue

        if SATO_OLD in line:
            out.append(line.replace(SATO_OLD, SATO_NEW))
            converted += 1
            continue

        m = JOURNAL.search(line)
        if m:
            out.append(JOURNAL.sub(r" \1, \2 (\3).", line))
            converted += 1
            continue

        m = BOOK.search(line)
        if m:
            out.append(BOOK.sub(r", \1 edn (\2, \3, \4).", line))
            converted += 1
            continue

        problems.append(line[:120])
        out.append(line)

    return text[:start] + "\n".join(out) + text[end:], problems


def main() -> int:
    text = PATH.read_text(encoding="utf-8")
    original = text

    text, problems = convert_refs(text)
    total = text.count("\\bibitem")
    if problems:
        print(f"ABORTED -- {len(problems)} reference(s) did not match a rule:")
        for p in problems:
            print("  " + p)
        return 1
    print(f"OK   {total} references converted to Springer style")

    # --- ORCID on the author line ---------------------------------------
    old_author = (
        "\\author{Yaming Hu\\thanks{Independent Researcher, Guiyang, Guizhou Province, "
        "China. E-mail: 64687555@qq.com}}"
    )
    new_author = (
        "\\author{Yaming Hu\\thanks{Independent Researcher, Guiyang, Guizhou Province, "
        "China. E-mail: 64687555@qq.com. ORCID: "
        "\\href{https://orcid.org/0009-0003-1406-0485}{0009-0003-1406-0485}.}}"
    )
    assert text.count(old_author) == 1, "author line not found exactly once"
    text = text.replace(old_author, new_author)
    print("OK   ORCID added to the author affiliation")

    # --- ethics / consent declarations ----------------------------------
    anchor = (
        "\\noindent\\textbf{Conflict of Interest}: The author declares no conflict of interest."
    )
    addition = anchor + "\n\n" + (
        "\\noindent\\textbf{Ethics Approval}: Not applicable (no human or animal subjects).\n\n"
        "\\noindent\\textbf{Consent to Participate}: Not applicable.\n\n"
        "\\noindent\\textbf{Consent for Publication}: Not applicable."
    )
    assert text.count(anchor) == 1, "conflict-of-interest line not found exactly once"
    text = text.replace(anchor, addition)
    print("OK   ethics / consent declarations added")

    if text == original:
        print("No changes made.")
        return 1

    PATH.write_text(text, encoding="utf-8")
    print(f"\nWrote {PATH}  ({len(original)} -> {len(text)} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
