"""Cerca parole e sigle interne vietate nel testo visibile dei .tex (commenti tolti). Uso: python -I controlla_parole.py <cartella>"""
import re, sys, pathlib
VIETATE = [r"sciame", r"\bagent[ei]\b", r"\bruol[oi]\b", r"\bfas[ei]\b", r"verdett", r"\bK-?\d{3}\b", r"\bX[1-7]b?\b",
           r"\b[HF]\d+\b", r"\.md\b", r"validat", r"in tempo reale", r"certificabil", r"detect and avoid", r"zero falsi",
           r"122 droni", r"counter", r"minacci", r"bersagli", r"\bv[12]\b", r"riprova", r"controprova", r"\bnucleo\b",
           r"\b2[bc]\b", r"stato dei lavori", r"\bin corso\b", r"arbitro", r"coordinatore", r"consegna", r"addendum",
           r"neutralizz", r"abbatt", r"intercett", r"anti-drone", r"C-UAS", r"\bE[1-5]\b", r"\b[AS][1-4]\b", r"famiglia"]
def testo(p):
    righe = []
    for i, r in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
        r = re.sub(r"(?<!\\)%.*", "", r)
        righe.append((i, r))
    return righe
tot = 0
for p in sorted(pathlib.Path(sys.argv[1]).glob("**/*.tex")):
    if "_prima" in p.name: continue
    for i, r in testo(p):
        for v in VIETATE:
            for m in re.finditer(v, r, flags=re.I if v not in (r"\b[HF]\d+\b",) else 0):
                tot += 1
                print(f"{p.name}:{i}: [{v}] …{r[max(0,m.start()-40):m.end()+40]}…")
print("TOTALE", tot)
