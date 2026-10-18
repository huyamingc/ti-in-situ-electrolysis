#!/usr/bin/env python3
"""Query CrossRef for titles/DOIs of the 30 references in manuscript.tex.

The existing \\bibitem entries carry author / journal / volume / page / year but
no article titles.  Springer's Basic reference style renders a title, so the
titles must be recovered before the bibliography can be regenerated with
sn-basic.bst.  Each entry is looked up with a bibliographic query built from
exactly the data already in the manuscript, so a hit is evidence that the
recovered title belongs to that reference and not to a similarly cited one.
"""

import json
import time
import urllib.parse
import urllib.request

# key -> (author_surnames, journal, volume, page, year, kind)
REFS = {
    "kroll1937": ("Kroll", "Zeitschrift fur anorganische und allgemeine Chemie", "234", "42", "1937", "article"),
    "ji2026": ("Ji Guo Gao Yang Yan Zeng", "International Journal of Minerals Metallurgy and Materials", "33", "15", "2026", "article"),
    "fray2000": ("Chen Fray Farthing", "Nature", "407", "361", "2000", "article"),
    "jiao2023": ("Jiao Liu Wang Lin Qu Song Jiao", "ACS Sustainable Chemistry & Engineering", "11", "5764", "2023", "article"),
    "ono2002": ("Ono Suzuki", "JOM", "54", "59", "2002", "article"),
    "pal2001": ("Pal Woolley Kenney", "JOM", "53", "32", "2001", "article"),
    "okabe1997": ("Okabe Waseda", "JOM", "49", "28", "1997", "article"),
    "zhang2024": ("Zhang Yan Liu Guo Yang Yang Xia Hu Li", "Journal of The Electrochemical Society", "171", "082502", "2024", "article"),
    "taninouchi2016": ("Taninouchi Hamanaka Okabe", "Metallurgical and Materials Transactions B", "47", "3394", "2016", "article"),
    "lee2025": ("Lim Nersisyan Han Park Suh Lee", "Next Materials", "8", "100803", "2025", "article"),
    "pang2024": ("Pang Kong Zhu Xu Xu Bai Yang", "Transactions of Nonferrous Metals Society of China", "34", "681", "2024", "article"),
    "xu2025": ("Zhu Zhang Kong Xu Yang", "Electrochimica Acta", "533", "146478", "2025", "article"),
    "waldner1999": ("Waldner Eriksson", "Calphad", "23", "189", "1999", "article"),
    "zhang2008mgce": ("Zhang Wang Shang Chen Liu", "Journal of Alloys and Compounds", "463", "294", "2008", "article"),
    "chartrand2000": ("Chartrand Pelton", "Canadian Metallurgical Quarterly", "39", "405", "2000", "article"),
    "kleppa1966": ("Kleppa McCarty", "Journal of Physical Chemistry", "70", "1249", "1966", "article"),
    "pelton2000mqm": ("Pelton Degterov Eriksson Robelin Dessureault", "Metallurgical and Materials Transactions B", "31", "651", "2000", "article"),
    "nayeb1987": ("Nayeb-Hashemi Clark", "Bulletin of Alloy Phase Diagrams", "8", "58", "1987", "article"),
    "hallstedt2025": ("Hallstedt", "Calphad", "89", "102833", "2025", "article"),
    "tang2015": ("Tang Ren Wang Deng Cai Shao Zhao Gao Yan Zhang", "Journal of The Electrochemical Society", "162", "D520", "2015", "article"),
    "yan2007": ("Yan Fray", "Mineral Processing and Extractive Metallurgy", "116", "17", "2007", "article"),
    "littlewood1962": ("Littlewood", "Journal of The Electrochemical Society", "109", "525", "1962", "article"),
    "kvande2014": ("Kvande Drablos", "Journal of Occupational and Environmental Medicine", "56", "S23", "2014", "article"),
    "morita2004": ("Ito Morita", "Materials Transactions", "45", "2712", "2004", "article"),
    "song2024": ("Song Zhao He Lu", "Journal of The Electrochemical Society", "171", "062501", "2024", "article"),
}

BASE = "https://api.crossref.org/works"
UA = "ti-ref-verifier/1.0 (mailto:64687555@qq.com)"


def query(key, info):
    surnames, journal, vol, page, year, kind = info
    q = f"{surnames} {journal} {vol} {page} {year}"
    url = BASE + "?" + urllib.parse.urlencode(
        {"query.bibliographic": q, "rows": "3", "select": "DOI,title,container-title,volume,page,issued,author,type"}
    )
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=45) as fh:
            data = json.load(fh)
    except Exception as exc:  # network hiccup: report, do not guess
        return {"key": key, "error": str(exc), "candidates": []}

    out = []
    for it in data.get("message", {}).get("items", []):
        title = (it.get("title") or [""])[0]
        cont = (it.get("container-title") or [""])[0]
        yr = ""
        try:
            yr = str(it["issued"]["date-parts"][0][0])
        except Exception:
            pass
        out.append(
            {
                "title": title,
                "journal": cont,
                "volume": it.get("volume", ""),
                "page": it.get("page", ""),
                "year": yr,
                "doi": it.get("DOI", ""),
                "type": it.get("type", ""),
            }
        )
    return {"key": key, "query": q, "candidates": out}


def main():
    results = []
    for key, info in REFS.items():
        r = query(key, info)
        results.append(r)
        n = len(r.get("candidates", []))
        print(f"{key:18s} -> {n} candidate(s)" + (f"  ERROR {r['error']}" if "error" in r else ""))
        time.sleep(0.4)  # be polite to the API
    with open("crossref_results.json", "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=2, ensure_ascii=False)
    print("\nwritten crossref_results.json")


if __name__ == "__main__":
    main()
