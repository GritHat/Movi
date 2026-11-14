#!/usr/bin/env python3
"""Controlli su allegato.bib: chiavi uniche, graffe bilanciate, campi obbligatori per tipo, identificativo o URL,
data di consultazione per le pagine web, parole interne vietate, coerenza con citabili.txt e con l'elenco d'origine.
Uso: controlla_bib.py <allegato.bib> <citabili.txt> <elenco.json>   (esce con 1 se trova errori)"""
import json, re, sys, collections
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from costruisci_bib import voci, campi

OBBL = {"article": ["author", "title", "journal", "year"], "inproceedings": ["author", "title", "booktitle", "year"],
        "book": ["author", "title", "publisher", "year"], "manual": ["title"], "misc": ["title"],
        "techreport": ["author", "title", "institution", "year"], "phdthesis": ["author", "title", "school", "year"],
        "mastersthesis": ["author", "title", "school", "year"]}
VIETATE = ["sciame", "arbitro", "verdetto", "ruolo", "non verific", "non lett", "manca", "a memoria", "vagliat", "stato di verifica", "f7", "f10", "curatore"]

testo = open(sys.argv[1], encoding="utf-8").read()
err = []
if testo.count("{") != testo.count("}"):
    err.append("graffe: %d aperte, %d chiuse" % (testo.count("{"), testo.count("}")))
vv = voci(testo)
if len(vv) != len(re.findall(r"^@\w+\{", testo, flags=re.M)):
    err.append("numero di voci lette diverso dal numero di righe @")
cont = collections.Counter(k for _, k, _ in vv)
err += ["chiave doppia: " + k for k, n in cont.items() if n > 1]
tipi = collections.Counter()
for t, k, c in vv:
    tipi[t] += 1
    d = dict(campi(c))
    if c.count("{") != c.count("}"): err.append(k + ": graffe non bilanciate")
    for o in OBBL.get(t, ["title"]):
        if not d.get(o, "").strip("{} "): err.append("%s: manca il campo %s" % (k, o))
    if t not in OBBL: err.append("%s: tipo non previsto %s" % (k, t))
    if not any(x in d for x in ("doi", "eprint", "url", "isbn")):
        err.append(k + ": né DOI né arXiv né URL né ISBN")
    if "doi" not in d and "eprint" not in d and "isbn" not in d and "urldate" not in d:
        err.append(k + ": pagina web senza data di consultazione")
    if t in ("misc", "manual") and not any(x in d for x in ("author", "organization", "key")):
        err.append(k + ": niente con cui ordinare (autore, ente o key)")
    for p in VIETATE:
        if p in c.lower(): err.append("%s: parola interna «%s»" % (k, p))
    if "doi" in d and not re.match(r"^\{10\.\d{4,9}/\S+\}$", d["doi"]): err.append(k + ": DOI di forma strana " + d["doi"])
    if "year" in d and not re.match(r"^\{?\d{4}\}?$", d["year"]): err.append(k + ": anno di forma strana " + d["year"])
    if "pages" in d and "–" in d["pages"]: err.append(k + ": trattino non LaTeX nelle pagine")
cit = [k for r in open(sys.argv[2], encoding="utf-8") if not r.startswith("#") and ":" in r for k in r.split(":")[1].split()]
elenco = {x["chiave"] for x in json.load(open(sys.argv[3], encoding="utf-8"))}
chiavi = set(cont)
err += ["citabile assente dal bib: " + k for k in cit if k not in chiavi]
err += ["citabile con chiave non dell'elenco: " + k for k in cit if k not in elenco]
nuove = sorted(chiavi - set(cit))
print("voci:", len(vv), dict(tipi)); print("graffe:", testo.count("{"), testo.count("}"))
print("citabili dell'elenco:", len(cit), "| voci nuove:", nuove)
print("errori:", len(err)); [print("  -", e) for e in err]
sys.exit(1 if err else 0)
