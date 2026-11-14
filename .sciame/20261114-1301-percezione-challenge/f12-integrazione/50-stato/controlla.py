#!/usr/bin/env python3
"""Controlli testuali sulla versione 3 (previsioni R1-R5 di PREVISIONI.md). Sola lettura."""
import re, pathlib, sys
qui = pathlib.Path(__file__).resolve().parent
conv = qui.parents[1]; radice = conv.parents[1]
EST = (".md", ".py", ".json", ".jsonl", ".txt", ".tsv", ".csv", ".c", ".h", ".sh", ".bib", ".tex", ".pdf", ".diff")
def percorsi(testo):
    out = []
    for m in re.finditer(r"`([^`\n]+)`", testo):
        s = m.group(1).strip()
        if " " in s or any(c in s for c in "…*<>{}=$|"): continue
        if s.startswith("http"): continue
        if s.endswith("/") or s.lower().endswith(EST):
            out.append(s)
    return out
def risolvi(lista):
    manc, nudi, ultimo = [], [], None
    for s in lista:
        cand = [conv / s, radice / s, radice / "documentazione" / s]
        if "/" not in s.rstrip("/"):
            if ultimo is not None: cand.insert(0, ultimo / s)
            trovato = next((c for c in cand if c.exists()), None)
            if trovato is None: nudi.append(s)
            continue
        trovato = next((c for c in cand if c.exists()), None)
        if trovato is None: manc.append(s)
        else: ultimo = trovato if trovato.is_dir() else trovato.parent
    return manc, nudi
v3 = (qui / "STATO_PROGETTO.md").read_text(encoding="utf-8")
v2 = (qui / "STATO_V2_copia.md").read_text(encoding="utf-8")
m3, n3 = risolvi(percorsi(v3)); m2, n2 = risolvi(percorsi(v2))
nuovi = sorted(set(m3) - set(m2))
print(f"R1 percorsi con cartella: v3 {len(percorsi(v3))} citazioni; mancanti v3 {len(set(m3))}, già mancanti in v2 {len(set(m2))}, NUOVI mancanti {len(nuovi)}")
for s in nuovi: print("   NUOVO MANCANTE:", s)
for s in sorted(set(m3) & set(m2)): print("   ereditato:", s)
print(f"   nomi senza cartella non risolti: v3 {len(set(n3))}, v2 {len(set(n2))}; nuovi: {sorted(set(n3) - set(n2))}")
# R2 tabelle
def celle(r):
    r = re.sub(r"`[^`]*`", "", r)
    r = r.replace("\\|", "")
    return r.count("|")
rotte = 0; ntab = 0
righe = v3.split("\n"); i = 0
while i < len(righe):
    def tab(x): return re.match(r"^(> ?)?\|", x) is not None
    if tab(righe[i]):
        j = i
        while j < len(righe) and tab(righe[j]): j += 1
        blocco = righe[i:j]; ntab += 1
        conti = {celle(x) for x in blocco}
        sep = len(blocco) > 1 and re.match(r"^(> ?)?\|[\s:|-]+\|\s*$", blocco[1]) is not None
        if len(conti) != 1 or not sep:
            rotte += 1; print(f"   TABELLA ROTTA alla riga {i+1}: colonne {sorted(conti)}, separatore {sep}: {blocco[0][:70]}")
        i = j
    else: i += 1
print(f"R2 tabelle: {ntab}; rotte: {rotte}")
# R3 righe della v2 assenti
s3 = set(righe)
tolte = [x for x in v2.split("\n") if x.strip() and x not in s3]
print(f"R3 righe non vuote della v2 assenti nella v3 (tolte o riscritte): {len(tolte)}")
estese = [x for x in tolte if x.rstrip().rstrip("|").rstrip()[:160] in v3]
print(f"   di cui ESTESE (il testo della v2 c'è ancora, con un'aggiunta in coda): {len(estese)}; TOLTE O RISCRITTE: {len(tolte) - len(estese)}")
for x in tolte: print("   -", "[estesa]" if x in estese else "[tolta/riscritta]", x[:100])
# R4 frasi da non dire
def nudo(x):
    x = re.sub(r"«[^»]*»", "", x); x = re.sub(r"\"[^\"]*\"", "", x); return x
sosp = [(k+1, x) for k, x in enumerate(righe) if re.search(r"validat|via libera|garantit", nudo(x), flags=re.I)]
print(f"R4 righe con «validat», «via libera», «garantit» fuori da virgolette: {len(sosp)}")
for k, x in sosp:
    for m in re.finditer(r"validat\w*|via libera|garantit\w*", nudo(x), flags=re.I):
        c = nudo(x); a = max(0, m.start()-60); print(f"   r.{k}: …{c[a:m.end()+30]}…")
# R5 ingressi obbligati
ING = """f4/H-012/05-correzioni/SOLUZIONE_V2.md f4/H-012/09-arbitro/VERDETTO.md f5/02-audit/AUDIT.md
f7-estensione/16-verdetto/VERDETTO_ESTENSIONE.md f8-continuita/16-verdetto/VERDETTO_CONTINUITA.md
f9-preproposta/13-verdetto/VERDETTO_PREPROPOSTA.md f10-dati/23-verdetto/VERDETTO_DATI.md
f12-integrazione/20-finale/SOLUZIONE_V3.md f12-integrazione/02-prova-insieme/PROVA_INSIEME.md
f12-integrazione/03-libero/LIBERO_DELLA_CELLA.md f12-integrazione/10-attacco/ATTACCO_V3.md
f12-integrazione/11-completezza/COMPLETEZZA.md f12-integrazione/12-piano-rifatto/PIANO_RIFATTO.md
f12-integrazione/13-statistica/CONTROLLO_PROVE.md f12-integrazione/21-piano-finale/PIANO_14_4.md
f12-integrazione/22-schermo-finale/SCHERMO_E_DEMO.md f12-integrazione/30-arbitro/VERDETTO_INTEGRAZIONE.md
f5/CHIUSURA.md f12-integrazione/06-identita/IDENTITA_SU_PROFONDITA.md
f12-integrazione/07-controprova-identita/CONTROPROVA_IDENTITA.md f13-allegato/DISCORDANZE_DEI_FASCICOLI.md
f14-classificazione/20-inclusione/BLOCCO_CLASSIFICAZIONE.md f14-classificazione/CONTRATTO_CLASSIFICAZIONE.md
f14-classificazione/01-profili/PROFILI.md f14-classificazione/02-uso/USO_DELLA_CLASSE.md
f14-classificazione/03-classificatore/CLASSIFICATORE.md f14-classificazione/10-attacco/ATTACCO_CLASSIFICAZIONE.md
f12-integrazione/CONTRATTO_INTEGRAZIONE.md ADDENDUM_UTENTE.md f11-documentazione/finale/CORREZIONI_APPLICATE.md
f10-dati/CONTRATTO_DATI.md f10-dati/10-catena/CATENA.md f10-dati/11-simulatore/SIMULATORE.md
f10-dati/12-dati-veri/DATI_VERI.md f10-dati/20-validazione/VALIDAZIONE_DATI.md f10-dati/21-statistica/ANALISI_DATI.md
f10-dati/04-embedded/INVENTARIO_E_DECISIONE.md f10-dati/03-infrastruttura/AMBIENTE.md""".split()
assenti = [p for p in ING if p not in v3]
print(f"R5 ingressi della consegna: {len(ING)}; non citati: {assenti}")
print("parole:", len(v3.split()), "righe:", len(righe))
