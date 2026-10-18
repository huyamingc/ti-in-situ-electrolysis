#!/usr/bin/env python3
"""Convert manuscript.tex from the ECS `article` layout to Springer's sn-jnl.

Every edit is anchored on a literal string and asserted, so a partial or
mis-targeted conversion aborts instead of silently producing a hybrid file.
The article-class original is kept as manuscript_article.tex.

Mapping applied:
  * preamble                     -> sn-jnl + the packages the class does not load
  * \\linenumbers/\\doublespacing  -> dropped (class owns the layout)
  * \\title{\\author{\\date{\\maketitle -> \\title[short]{\\author*[1]{\\affil[1]{\\abstract{\\keywords{\\maketitle
  * 7 numbered \\section*         -> \\section
  * \\section*{Nomenclature}      -> kept unnumbered (it is front matter, not a section)
  * 19 \\subsection*              -> \\subsection
  * hand-written \\noindent\\textbf{Declarations} block -> \\backmatter + itemize
  * thebibliography              -> \\bibliography{refs} (sn-basic.bst)
"""

import io
import re
import sys

SRC = "manuscript.tex"
BAK = "manuscript_article.tex"

with io.open(SRC, encoding="utf-8") as fh:
    src = fh.read()

with io.open(BAK, encoding="utf-8") as fh:
    bak = fh.read()

if src != bak:
    print("ERROR: manuscript.tex differs from manuscript_article.tex before conversion; aborting")
    sys.exit(1)

edits = []


def must(old, new, label, count=1):
    """Replace `old` with `new`, asserting exactly `count` occurrences."""
    global src
    n = src.count(old)
    if n != count:
        print("ERROR [%s]: expected %d occurrence(s), found %d" % (label, count, n))
        sys.exit(1)
    src = src.replace(old, new)
    edits.append(label)


# ---------------------------------------------------------------- 1. abstract
m = re.search(r"\\begin\{abstract\}\n(.*?)\n\\end\{abstract\}", src, re.S)
if not m:
    print("ERROR [abstract]: environment not found")
    sys.exit(1)
abstract_body = m.group(1).strip()
if "\\begin{abstract}" in abstract_body or "\\end{abstract}" in abstract_body:
    print("ERROR [abstract]: nested environment")
    sys.exit(1)
edits.append("abstract extracted (%d chars)" % len(abstract_body))

# ------------------------------------------------------- 2. drop \newpage (3)
if src.count("\n\\newpage\n") != 3:
    print("ERROR [newpage]: expected 3, found %d" % src.count("\n\\newpage\n"))
    sys.exit(1)
src = src.replace("\n\\newpage\n", "\n")
edits.append("removed 3 \\newpage")

# ---------------------------------------------------------- 3. drop singlespace
must("\\begin{singlespace}\n\\small\n", "\\small\n", "singlespace-open")
must("\n\\end{singlespace}\n", "\n", "singlespace-close")

# ------------------------------------------------------------- 4. preamble
old_pre = """\\documentclass[11pt]{article}

\\usepackage[margin=1in]{geometry}
\\usepackage{graphicx}
\\usepackage{multirow}
\\usepackage{amsmath,amssymb,amsfonts}
\\usepackage{amsthm}
\\usepackage{xcolor}
\\usepackage{textcomp}
\\usepackage{booktabs}
\\usepackage{tabularx}
\\usepackage[version=4]{mhchem}
\\usepackage{epstopdf}
\\usepackage[mathlines]{lineno}
\\usepackage{setspace}
\\usepackage{etoolbox}
\\usepackage[colorlinks=true,allcolors=blue]{hyperref}
\\hypersetup{pdftitle={Electrochemical Design Basis for Titanium Production by Mg--Ca Co-Deposition in a Quaternary Chloride Melt}, pdfauthor={Yaming Hu}}

\\graphicspath{{figures_eps/}}

\\AtBeginEnvironment{table}{\\singlespacing}"""

new_pre = r"""\documentclass[pdflatex,sn-basic,Numbered]{sn-jnl}

%% Packages the sn-jnl class does not load itself.  xcolor must precede the
%% class's \AtBeginDocument colour definitions, epstopdf converts the 15 EPS
%% figures, and manyfoot/SetFootnoteHook are required by the class.
\usepackage{xcolor}
\usepackage{epstopdf}
\usepackage{manyfoot}
\usepackage{graphicx}
\usepackage{multirow}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{amsthm}
\usepackage{textcomp}
\usepackage{booktabs}
\usepackage{tabularx}
\usepackage[version=4]{mhchem}

\graphicspath{{figures_eps/}}
\hypersetup{pdftitle={Electrochemical Design Basis for Titanium Production by Mg--Ca Co-Deposition in a Quaternary Chloride Melt}, pdfauthor={Yaming Hu}}"""

must(old_pre, new_pre, "preamble")

# ------------------------------------------- 5. front matter (title..keywords)
old_front = re.search(
    r"\\linenumbers\n\\doublespacing\n\n\\title\{.*?\\par\}\n",
    src,
    re.S,
)
if not old_front:
    print("ERROR [frontmatter]: block not matched")
    sys.exit(1)

long_title = (
    "Electrochemical Design Basis for Titanium Production by "
    "Mg--Ca Co-Deposition in a Quaternary Chloride Melt"
)
short_title = "Electrochemical Design Basis for Ti by Mg--Ca Co-Deposition"

new_front = (
    "\\title[%s]{%s}\n\n"
    "\\author*[1]{\\fnm{Yaming}\\sur{Hu}\\email{64687555@qq.com}"
    "\\orcid{https://orcid.org/0009-0003-1406-0485}}\n\n"
    "\\affil[1]{\\orgname{Independent Researcher}, \\city{Guiyang}, "
    "\\state{Guizhou}, \\country{China}}\n\n"
    "\\abstract{%s}\n\n"
    "\\keywords{titanium production, molten salt electrolysis, "
    "Mg--Ca co-deposition, deoxidation, process design}\n\n"
    "\\maketitle\n"
) % (short_title, long_title, abstract_body)

src = src[: old_front.start()] + new_front + src[old_front.end():]
edits.append("front matter rebuilt")

# ------------------------------------------------------- 6. numbered sections
numbered = [
    ("Introduction", "sec:intro"),
    ("Process Description", "sec:process"),
    ("Process Comparison", "sec:comparison"),
    ("Thermodynamic Framework", "sec:thermo"),
    ("Results and Discussion", "sec:results"),
    ("Uncertainties and Limitations", "sec:limitations"),
    ("Conclusions", "sec:conclusions"),
]
for name, label in numbered:
    must(
        "\\section*{%s}" % name,
        "\\section{%s}\\label{%s}" % (name, label),
        "section:%s" % name,
    )

# Nomenclature stays unnumbered: it is front matter, not a numbered section.
must(
    "\\section*{Nomenclature}",
    "\\section*{Nomenclature}",
    "section:Nomenclature (kept unnumbered)",
)

# ------------------------------------------------------------ 7. subsections
n_sub = src.count("\\subsection*{")
if n_sub != 16:
    print("ERROR [subsections]: expected 16, found %d" % n_sub)
    sys.exit(1)
src = src.replace("\\subsection*{", "\\subsection{")
edits.append("16 subsections unstarred")

# ------------------------------------------------------- 8. declarations block
old_decl = r"""\noindent\textbf{Declarations}

\noindent\textbf{Data Availability}: All thermodynamic data are from the cited literature. The Python scripts used for calculations and figure generation are publicly available at \url{https://github.com/huyamingc/ti-in-situ-electrolysis}. A preprint version of this work has been deposited on Zenodo (DOI: \href{https://doi.org/10.5281/zenodo.21973469}{10.5281/zenodo.21973469}).

\noindent\textbf{Conflict of Interest}: The author declares no conflict of interest.

\noindent\textbf{Ethics Approval}: Not applicable (no human or animal subjects).

\noindent\textbf{Consent to Participate}: Not applicable.

\noindent\textbf{Consent for Publication}: Not applicable.

\noindent\textbf{Author Contributions}: Yaming Hu: Conceptualization, Methodology, Formal analysis, Investigation, Writing---original draft, Writing---review \& editing, Visualization.

\noindent\textbf{Funding}: This research did not receive any specific grant from funding agencies in the public, commercial, or not-for-profit sectors."""

new_decl = r"""\backmatter

\section*{Declarations}

\begin{itemize}
\item[{Data availability}] All thermodynamic data are from the cited literature. The Python scripts used for calculations and figure generation are publicly available at \url{https://github.com/huyamingc/ti-in-situ-electrolysis}. A preprint version of this work has been deposited on Zenodo (DOI: \href{https://doi.org/10.5281/zenodo.21973469}{10.5281/zenodo.21973469}).

\item[{Conflict of interest}] The author declares no conflict of interest.

\item[{Ethics approval}] Not applicable (no human or animal subjects).

\item[{Consent to participate}] Not applicable.

\item[{Consent for publication}] Not applicable.

\item[{Author contributions}] Yaming Hu: Conceptualization, Methodology, Formal analysis, Investigation, Writing---original draft, Writing---review \& editing, Visualization.

\item[{Funding}] This research did not receive any specific grant from funding agencies in the public, commercial, or not-for-profit sectors.
\end{itemize}"""

must(old_decl, new_decl, "declarations")

# ---------------------------------------------------------- 9. bibliography
i = src.find("\\begin{thebibliography}{99}")
if i < 0:
    print("ERROR [bib]: thebibliography not found")
    sys.exit(1)
j = src.find("\\end{thebibliography}", i)
if j < 0:
    print("ERROR [bib]: \\end{thebibliography} not found")
    sys.exit(1)
j += len("\\end{thebibliography}")
removed = src[i:j]
n_bib = removed.count("\\bibitem{")
if n_bib != 30:
    print("ERROR [bib]: expected 30 \\bibitem, found %d" % n_bib)
    sys.exit(1)
src = src[:i] + "\\bibliography{refs}" + src[j:]
edits.append("thebibliography (30 entries) -> \\bibliography{refs}")

# ---------------------------------------------------------------- write back
with io.open(SRC, "w", encoding="utf-8", newline="\n") as fh:
    fh.write(src)

print("conversion OK -- %d edits:" % len(edits))
for e in edits:
    print("  -", e)
print("\nnew size: %d chars (%d lines)" % (len(src), src.count("\n") + 1))
