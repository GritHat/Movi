#!/usr/bin/env python3
"""Prova di correzione di forma su una COPIA del .bib (l'originale non si tocca):
(1) alle voci senza year aggiunge year (2022 per st-um3038, letto nel PDF; s.d. per le pagine senza data);
(2) dove la nota ripete l'indirizzo del campo url, toglie la ripetizione dalla nota."""
import re, sys
t = open(sys.argv[1], encoding="utf-8").read()
voci = re.split(r"(?=^@)", t, flags=re.M); out = []; n_anno = n_url = 0
for v in voci:
    m = re.match(r"@(\w+)\{([^,]+),", v)
    if m:
        u = re.search(r"^\s*url\s*=\s*\{(.*)\},?\s*$", v, flags=re.M)
        if u and ("\\url{" + u.group(1) + "}") in v:
            v2 = v.replace("\\url{" + u.group(1) + "}, ", "").replace("\\url{" + u.group(1) + "},", "")
            if v2 != v: n_url += 1; v = v2
        if not re.search(r"^\s*year\s*=", v, flags=re.M):
            anno = "2022" if m.group(2) == "st-um3038" else "s.d."
            v = re.sub(r"^(@\w+\{[^,]+,\n)", r"\1  year = {" + anno + "},\n", v, count=1); n_anno += 1
    out.append(v)
open(sys.argv[2], "w", encoding="utf-8").write("".join(out))
print("anni aggiunti:", n_anno, "| note senza indirizzo ripetuto:", n_url)
