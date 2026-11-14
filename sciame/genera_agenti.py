#!/usr/bin/env python3
"""Genera gli agenti dello sciame e le skill di convocazione per Claude Code, dalle schede di `sciame/AGENTI.md`.

Le schede e i documenti di questa cartella sono la fonte unica. Da loro vengono, nella radice del progetto (la
cartella che contiene `sciame/`):
- il catalogo, `sciame/catalogo.json`: i ruoli, i profili e i testi, per `convoca.py` e per chi orchestra da sé;
- gli agenti, `.claude/agents/sciame-<sigla>.md`;
- le skill di convocazione, `.claude/skills/<nome>/SKILL.md`, una per strategia: `sciame`, `sciame-singolo`,
  `sciame-classica`, `sciame-completa`.

    python3 -I sciame/genera_agenti.py                    # rigenera tutto nel progetto
    python3 -I sciame/genera_agenti.py --controlla        # esce con 1 se qualcosa non è allineato alle schede
    python3 -I sciame/genera_agenti.py --installa RADICE  # copia questa cartella in un altro progetto e vi genera tutto
    python3 -I sciame/genera_agenti.py --istruzioni [CLAUDE.md]
                                                          # aggiunge (o aggiorna) il paragrafo sullo sciame in quel file
    python3 -I sciame/genera_agenti.py --togli-istruzioni [CLAUDE.md]
    python3 -I sciame/genera_agenti.py --elenco           # stampa i ruoli e i profili

Ogni scheda comincia con `### N. Nome — `sciame-sigla`` e ha le righe `- **In breve:** …`, `- **Nucleo:** …` e
`- **Parole chiave:** …`. Solo libreria standard, niente rete. Di norma lo lancia `sciame/sciame.sh`.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path

QUI = Path(__file__).resolve().parent
RADICE = QUI.parent
FONTI = ["AGENTI.md", "PREAMBOLO.md", "PIPELINE.md", "ISTRUZIONI_COORDINATORE.md", "SCHEDA_IPOTESI.md"]
# Ciò che `--installa` copia in un altro progetto, oltre a ciò che genera; `sciame.sh` se c'è.
DOCUMENTI = FONTI + ["README.md", "convoca.py", "genera_agenti.py"]
VERSIONE = "3.1"
TITOLO = re.compile(r"^### (\d+)\. (.+?) — `sciame-([a-z-]+)`\s*$")
NUCLEO = re.compile(r"^## Nucleo (.+)$")
BLOCCO = re.compile(r"<!-- ([a-z-]+(?::[a-z-]+)?) -->\n(.*?)\n<!-- /\1 -->", re.S)
NUCLEI = {
    "teorico e formale": "teorico",
    "ia e modelli": "modelli",
    "sperimentale e delle misure": "sperimentale",
    "software e sistemi": "software",
    "conoscenza e comunicazione": "conoscenza",
    "progetto e decisione": "decisione",
    "critico e divergente": "critico",
    "percezione, stima e movimento": "percezione",
}
STRATEGIE = ("singolo", "classica", "completa", "auto")
# La skill di ogni strategia. Nessun ruolo può avere una di queste sigle.
SKILL = {"auto": "sciame", "singolo": "sciame-singolo", "classica": "sciame-classica", "completa": "sciame-completa"}
DESCRIZIONI_SKILL = {
    "auto": "Convoca lo sciame di agenti lasciando al coordinatore la scelta della strategia (singolo, classica o "
            "completa) e dei ruoli, con le regole di sciame/PIPELINE.md. Usala solo quando l'utente chiede lo sciame "
            "senza dire quale convocazione.",
    "singolo": "Esperto singolo dello sciame: un solo specialista, il più adatto o quello nominato, con una consegna "
               "completa (1 agente). Per una domanda chiara di un campo o un compito piccolo. Usala solo quando "
               "l'utente chiede lo sciame o un suo esperto.",
    "classica": "Convocazione classica dello sciame: contratto, due corsie cieche, triage, torneo dei falsificatori, "
                "una squadra per ipotesi, prove e verdetti (da 6 a 15 agenti). Per decidere, progettare, correggere, "
                "dimostrare o misurare. Usala solo quando l'utente chiede la convocazione classica.",
    "completa": "Convocazione completa dello sciame: tutti i ruoli in una tornata cieca, il consolidamento "
                "dell'arbitro, poi la classica (tutti i ruoli più una classica: costosa). Per domande strategiche o "
                "aperte che toccano molti campi. Usala solo quando l'utente chiede la convocazione completa.",
}
TITOLI_SKILL = {"auto": "la strategia la sceglie il coordinatore", "singolo": "esperto singolo",
                "classica": "convocazione classica", "completa": "convocazione completa"}
CARTELLA_AGENTI = ".claude/agents"
CARTELLA_SKILL = ".claude/skills"
AMBIENTE_PROGETTO = """## Dove sei

Sei nel progetto dell'utente, con gli strumenti che la sessione ti concede. I documenti dello sciame sono nella
cartella `sciame/`, alla radice del progetto: `PIPELINE.md` (le strategie e le fasi), `PREAMBOLO.md` (le regole
estese), `AGENTI.md` (le schede di tutti i ruoli). Scrivi solo nella cartella che ti dà la consegna; il resto del
progetto lo leggi soltanto. Se uno strumento ti manca o ti è negato, non aggirarlo: dillo nella consegna, e segna
«non verificato» ciò che non hai potuto provare."""
# Per chi interroga i ruoli uno per uno con un modello raggiunto per API: non eseguono niente.
AMBIENTE_SENZA_STRUMENTI = """## Dove sei

Non hai strumenti: niente file, niente shell, niente rete. Lavori sul testo della consegna, e la tua risposta è la
consegna. Ciò che andrebbe provato lo dici con la prova che servirebbe, e lo segni «non verificato»."""
SEGNO_INIZIO = "<!-- sciame:inizio (scritto da sciame/genera_agenti.py --istruzioni: non modificare a mano) -->"
SEGNO_FINE = "<!-- sciame:fine -->"
NOTA_SKILL = "<!-- Generato da sciame/genera_agenti.py dai documenti di sciame/: non modificare a mano. -->"


class Errore(Exception):
    pass


def leggi(nome: str) -> str:
    return (QUI / nome).read_text(encoding="utf-8")


def _campo(righe: list[str], nome: str) -> str:
    """Il testo del punto `- **nome:** …`, con le righe di continuazione (rientrate di due spazi)."""
    for i, r in enumerate(righe):
        if r.startswith(f"- **{nome}:**"):
            testo = [r[len(f"- **{nome}:**"):].strip()]
            for s in righe[i + 1:]:
                if not s.startswith("  ") or s.lstrip().startswith("- "):
                    break
                testo.append(s.strip())
            return " ".join(testo)
    raise Errore(f"scheda senza «{nome}»: {righe[0]}")


def schede(testo: str) -> list[dict]:
    righe = testo.splitlines()
    ruoli, nucleo_corrente = [], None
    inizi = []
    for i, r in enumerate(righe):
        m = NUCLEO.match(r)
        if m:
            nucleo_corrente = m.group(1).strip()
        if TITOLO.match(r):
            inizi.append((i, nucleo_corrente))
    # Una scheda finisce alla successiva, o al primo titolo di livello due (un nucleo, il coordinatore).
    for i, nucleo_titolo in inizi:
        fine = len(righe)
        for j in range(i + 1, len(righe)):
            if TITOLO.match(righe[j]) or righe[j].startswith("## ") or righe[j] == "---":
                fine = j
                break
        n, nome, sigla = TITOLO.match(righe[i]).groups()
        blocco = righe[i:fine]
        nucleo_testo = _campo(blocco, "Nucleo").rstrip(".").strip()
        chiave = NUCLEI.get(nucleo_testo.lower())
        if not chiave:
            raise Errore(f"«{nome}»: nucleo sconosciuto «{nucleo_testo}»")
        if nucleo_titolo and nucleo_titolo.lower() != nucleo_testo.lower():
            raise Errore(f"«{nome}» dice nucleo «{nucleo_testo}» ma sta sotto «{nucleo_titolo}»")
        if sigla in STRATEGIE:
            raise Errore(f"«{nome}»: la sigla «{sigla}» è il nome di una strategia")
        parole = [p.strip() for p in _campo(blocco, "Parole chiave").rstrip(".").split(",") if p.strip()]
        ruoli.append({
            "n": int(n),
            "sigla": sigla,
            "nome": nome,
            "nucleo": chiave,
            "breve": _campo(blocco, "In breve"),
            "parole": parole,
            "scheda": "\n".join(blocco).strip(),
        })
    numeri = [r["n"] for r in ruoli]
    if numeri != list(range(1, len(ruoli) + 1)):
        raise Errore(f"schede numerate male: {numeri}")
    sigle = [r["sigla"] for r in ruoli]
    if len(set(sigle)) != len(sigle):
        raise Errore("due schede con la stessa sigla")
    return ruoli


def blocchi(testo: str) -> dict[str, str]:
    return {m.group(1): m.group(2).strip() for m in BLOCCO.finditer(testo)}


def profili(testo: str, sigle: set[str]) -> dict[str, dict]:
    """La tabella dei profili di PIPELINE.md: per ogni profilo i ruoli di ogni fase, come sigle."""
    trovati = {}
    for riga in testo.splitlines():
        m = re.match(r"^\| `([a-z]+)` \|(.*)\|\s*$", riga)
        if not m:
            continue
        celle = [c.strip() for c in m.group(2).split("|")]
        if len(celle) != 6:
            raise Errore(f"profilo {m.group(1)}: {len(celle)} colonne invece di 6")
        per, a, b, traduce, f3, f4 = celle

        def ruoli_di(cella):
            nomi = re.findall(r"[a-z]+(?:-[a-z]+)*", cella)
            return [n for n in dict.fromkeys(nomi) if n in sigle]

        if m.group(1) in trovati:
            raise Errore(f"due profili con il nome {m.group(1)}")
        trovati[m.group(1)] = {"per": per, "A": ruoli_di(a), "B": ruoli_di(b), "traduce": ruoli_di(traduce),
                               "f3": ruoli_di(f3), "f4": ruoli_di(f4)}
    if "generale" not in trovati:
        raise Errore("manca il profilo generale")
    return trovati


def prompt_ruolo(ruolo: dict, regole: str) -> str:
    """Il testo dell'agente; l'ambiente lo aggiunge chi lo scrive."""
    return f"""Sei il ruolo «{ruolo['nome']}» (scheda {ruolo['n']}) dello sciame di agenti: {ruolo['breve']}

Ti convoca un coordinatore con una consegna: eseguila nel tuo ruolo e consegna come dice la consegna. Non vedi la
conversazione del coordinatore né il lavoro degli altri ruoli, salvo ciò che la consegna ti dà. Rispondi nella lingua
dell'utente, di norma l'italiano.

{regole}

## La tua scheda

{ruolo['scheda']}
"""


def descrizione(ruolo: dict) -> str:
    return f"{ruolo['nome']}: {ruolo['breve']} Agente dello sciame (nucleo {ruolo['nucleo']}); lo convoca il coordinatore."


def catalogo() -> dict:
    testi = {nome: leggi(nome) for nome in FONTI}
    ruoli = schede(testi["AGENTI.md"])
    sigle = {r["sigla"] for r in ruoli}
    pre = blocchi(testi["PREAMBOLO.md"])
    pipe = blocchi(testi["PIPELINE.md"])
    istr = blocchi(testi["ISTRUZIONI_COORDINATORE.md"])
    if "regole-in-breve" not in pre:
        raise Errore("PREAMBOLO.md senza il blocco regole-in-breve")
    for s in STRATEGIE:
        if f"strategia:{s}" not in pipe:
            raise Errore(f"PIPELINE.md senza il blocco strategia:{s}")
    if "profili" not in pipe:
        raise Errore("PIPELINE.md senza il blocco profili")
    for chiave in ("coordinatore", "claude-code", "ambiente:progetto"):
        if chiave not in istr:
            raise Errore(f"ISTRUZIONI_COORDINATORE.md senza il blocco {chiave}")
    regole = pre["regole-in-breve"]
    for r in ruoli:
        r["descrizione"] = descrizione(r)
        r["prompt"] = prompt_ruolo(r, regole)
    tabella = profili(pipe["profili"], sigle)
    for nome, p in tabella.items():
        for fase, chi in p.items():
            if fase != "per" and not chi and fase not in ("B",):
                raise Errore(f"profilo {nome}: nessun ruolo noto in {fase}")
    usati = {r["nucleo"] for r in ruoli}
    impronta = hashlib.sha256("\0".join(testi[n] for n in FONTI).encode()).hexdigest()
    return {
        "versione": VERSIONE,
        "impronta": impronta,
        "nuclei": [{"id": chiave, "nome": nome[0].upper() + nome[1:]} for nome, chiave in NUCLEI.items() if chiave in usati],
        "ruoli": ruoli,
        "profili": tabella,
        "testi": {
            "regole": regole,
            "coordinatore": istr["coordinatore"],
            "strategie": {s: pipe[f"strategia:{s}"] for s in STRATEGIE},
            "profili": pipe["profili"],
            "claude_code": istr["claude-code"],
            "ambienti": {"progetto": istr["ambiente:progetto"]},
            "ambienti_agenti": {"progetto": AMBIENTE_PROGETTO, "senza-strumenti": AMBIENTE_SENZA_STRUMENTI},
        },
    }


def testo_catalogo(dati: dict) -> str:
    return json.dumps(dati, ensure_ascii=False, indent=1) + "\n"


# --- Gli agenti ---


def agente(ruolo: dict, ambiente: str) -> str:
    return f"""---
name: sciame-{ruolo['sigla']}
description: {json.dumps(ruolo['descrizione'], ensure_ascii=False)}
model: inherit
---

<!-- Generato da sciame/genera_agenti.py dalla scheda «{ruolo['n']}. {ruolo['nome']}» di sciame/AGENTI.md: non modificare a mano. -->

{ruolo['prompt']}
{ambiente}
"""


def file_agenti(dati: dict) -> dict[str, str]:
    """Percorso relativo alla radice del progetto → testo, per ogni ruolo."""
    ambiente = dati["testi"]["ambienti_agenti"]["progetto"]
    return {f"{CARTELLA_AGENTI}/sciame-{r['sigla']}.md": agente(r, ambiente) for r in dati["ruoli"]}


# --- Le skill di convocazione ---


def indice_ruoli(dati: dict) -> str:
    nomi = {n["id"]: n["nome"] for n in dati["nuclei"]}
    righe = ["## I ruoli dello sciame", "",
             "Un ruolo si convoca con il nome della prima colonna. Le parole chiave servono a scegliere: aggiungi ai "
             "ruoli del profilo quelli le cui parole chiave compaiono nella richiesta.", "",
             "| agente | ruolo | nucleo | parole chiave |", "|---|---|---|---|"]
    for r in dati["ruoli"]:
        righe.append(f"| `sciame-{r['sigla']}` | {r['nome']} | {nomi[r['nucleo']].lower()} | {', '.join(r['parole'])} |")
    return "\n".join(righe)


def skill(dati: dict, strategia: str) -> str:
    """Il testo della skill di una strategia: basta da solo a chi fa il coordinatore."""
    testi = dati["testi"]
    testa = ["---", f"name: {SKILL[strategia]}",
             f"description: {json.dumps(DESCRIZIONI_SKILL[strategia], ensure_ascii=False)}",
             'argument-hint: "[profilo=<profilo>] [ruoli=<sigla,sigla>] <la richiesta>"', "---"]
    parti = ["\n".join(testa), NOTA_SKILL, f"# Sciame: {TITOLI_SKILL[strategia]}", testi["coordinatore"]]
    if strategia == "auto":
        parti += ["**La strategia di questa convocazione la scegli tu**, con le regole qui sotto; poi segui il "
                  "paragrafo della strategia scelta.", testi["strategie"]["auto"], testi["strategie"]["singolo"],
                  testi["strategie"]["classica"], testi["strategie"]["completa"]]
    elif strategia == "completa":
        parti += ["**La strategia di questa convocazione è la completa**, che dopo il consolidamento prosegue come la "
                  "classica.", testi["strategie"]["completa"], testi["strategie"]["classica"]]
    else:
        parti += [f"**La strategia di questa convocazione è: {strategia}.**", testi["strategie"][strategia]]
    if strategia != "singolo":
        parti.append(testi["profili"])
    parti += [indice_ruoli(dati), testi["claude_code"], testi["ambienti"]["progetto"],
              "## La richiesta\n\n$ARGUMENTS\n\n(Se qui sopra non c'è testo, la richiesta è l'ultimo messaggio "
              "dell'utente.)"]
    return "\n\n".join(parti) + "\n"


def file_skill(dati: dict) -> dict[str, str]:
    return {f"{CARTELLA_SKILL}/{nome}/SKILL.md": skill(dati, strategia) for strategia, nome in SKILL.items()}


def file_generati(dati: dict) -> dict[str, str]:
    """Tutto ciò che si scrive nella radice del progetto: percorso relativo → testo."""
    file = {"sciame/catalogo.json": testo_catalogo(dati), "sciame/VERSIONE": f"{dati['versione']} {dati['impronta'][:12]}\n"}
    file.update(file_agenti(dati))
    file.update(file_skill(dati))
    return file


def vecchi(radice: Path, file: dict[str, str]) -> list[Path]:
    """Gli agenti dello sciame che non hanno più una scheda: solo i file `sciame-*` nella cartella degli agenti."""
    cartella = radice / CARTELLA_AGENTI
    return [p for p in (sorted(cartella.glob("sciame-*")) if cartella.is_dir() else [])
            if p.is_file() and not p.is_symlink() and p.relative_to(radice).as_posix() not in file]


def _senza_collegamenti(radice: Path, relativo: str) -> Path:
    percorso = radice / relativo
    for p in [percorso, *percorso.parents]:
        if p == radice:
            break
        if p.is_symlink():
            raise Errore(f"{p} è un collegamento: non lo seguo")
    return percorso


def scrivi(radice: Path, dati: dict) -> list[str]:
    file = file_generati(dati)
    fatti = []
    for p in vecchi(radice, file):
        p.unlink()
        fatti.append(f"tolto {p.relative_to(radice).as_posix()}")
    for relativo, testo in file.items():
        percorso = _senza_collegamenti(radice, relativo)
        percorso.parent.mkdir(parents=True, exist_ok=True)
        percorso.write_text(testo, encoding="utf-8")
        fatti.append(relativo)
    return fatti


def controlla(radice: Path, dati: dict) -> list[str]:
    """Ciò che non è allineato alle schede."""
    file = file_generati(dati)
    diversi = []
    for relativo, testo in file.items():
        p = radice / relativo
        if not p.is_file():
            diversi.append(f"manca {relativo}")
        elif p.read_text(encoding="utf-8") != testo:
            diversi.append(f"diverso {relativo}")
    return diversi + [f"di troppo {p.relative_to(radice).as_posix()}" for p in vecchi(radice, file)]


def installa(radice: Path, dati: dict) -> list[str]:
    """Questa cartella in un altro progetto, con tutto ciò che se ne genera."""
    if not radice.is_dir():
        raise Errore(f"non c'è la cartella {radice}")
    cartella = _senza_collegamenti(radice, "sciame")
    if cartella.resolve() != QUI:
        cartella.mkdir(exist_ok=True)
        for nome in DOCUMENTI + (["sciame.sh"] if (QUI / "sciame.sh").is_file() else []):
            shutil.copyfile(QUI / nome, _senza_collegamenti(radice, f"sciame/{nome}"))
    return scrivi(radice, dati)


def togli(radice: Path) -> list[str]:
    """Toglie ciò che questo script genera fuori da `sciame/`: gli agenti e le skill, riconosciuti dalla loro nota."""
    tolti = []
    cartella = radice / CARTELLA_AGENTI
    for p in sorted(cartella.glob("sciame-*.md")) if cartella.is_dir() else []:
        if p.is_file() and not p.is_symlink() and "Generato da sciame/genera_agenti.py" in p.read_text(encoding="utf-8"):
            p.unlink()
            tolti.append(p.relative_to(radice).as_posix())
    for nome in SKILL.values():
        p = radice / CARTELLA_SKILL / nome / "SKILL.md"
        if p.is_file() and not p.is_symlink() and NOTA_SKILL in p.read_text(encoding="utf-8"):
            p.unlink()
            tolti.append(p.relative_to(radice).as_posix())
            if not any(p.parent.iterdir()):
                p.parent.rmdir()
    return tolti


# --- Il paragrafo per il file di istruzioni del progetto ---


def paragrafo(dati: dict) -> str:
    righe = [
        SEGNO_INIZIO,
        "## Sciame di agenti",
        "",
        f"Questo progetto ha uno sciame di {len(dati['ruoli'])} ruoli specialistici, in `sciame/`: gli agenti si chiamano "
        "`sciame-<sigla>`. Lo sciame si convoca solo quando l'utente lo chiede, con una di queste strategie:",
        "- **singolo** (skill `sciame-singolo`): un solo specialista, per una domanda chiara di un campo;",
        "- **classica** (skill `sciame-classica`): contratto, due corsie cieche, triage, torneo, squadre per ipotesi, prove e "
        "verdetti, per decidere, progettare, correggere, dimostrare o misurare;",
        "- **completa** (skill `sciame-completa`): tutti i ruoli in una tornata cieca, poi la classica, per le domande "
        "strategiche o aperte;",
        "- **auto** (skill `sciame`): la strategia la sceglie il coordinatore e la dichiara.",
        "",
        "Per convocarlo usa la skill della strategia. Le regole degli agenti sono in `sciame/PREAMBOLO.md`, le schede dei "
        "ruoli in `sciame/AGENTI.md`, le strategie in `sciame/PIPELINE.md`.",
        SEGNO_FINE,
    ]
    return "\n".join(righe) + "\n"


def _tratto(testo: str, percorso: Path) -> tuple[int, int] | None:
    inizio, fine = testo.find("<!-- sciame:inizio"), testo.find(SEGNO_FINE)
    if inizio < 0 and fine < 0:
        return None
    if inizio < 0 or fine < inizio:
        raise Errore(f"{percorso}: i segni del paragrafo dello sciame sono rovinati, sistemali a mano")
    fine += len(SEGNO_FINE)
    return inizio, fine + (1 if testo[fine:fine + 1] == "\n" else 0)


def istruzioni(percorso: Path, dati: dict) -> str:
    """Aggiunge il paragrafo in fondo al file, o lo sostituisce se c'è già. Il resto del file non si tocca."""
    if percorso.is_symlink():
        raise Errore(f"{percorso} è un collegamento: non lo seguo")
    nuovo = paragrafo(dati)
    testo = percorso.read_text(encoding="utf-8") if percorso.exists() else ""
    tratto = _tratto(testo, percorso)
    if tratto:
        testo, fatto = testo[:tratto[0]] + nuovo + testo[tratto[1]:], "aggiornato"
    else:
        testo, fatto = (testo.rstrip("\n") + "\n\n" if testo.strip() else "") + nuovo, "aggiunto"
    percorso.write_text(testo, encoding="utf-8")
    return fatto


def togli_istruzioni(percorso: Path) -> str:
    if percorso.is_symlink() or not percorso.is_file():
        return "non c'era"
    testo = percorso.read_text(encoding="utf-8")
    tratto = _tratto(testo, percorso)
    if not tratto:
        return "non c'era"
    resto = testo[:tratto[0]].rstrip("\n") + ("\n" if testo[:tratto[0]].strip() else "") + testo[tratto[1]:]
    if resto.strip():
        percorso.write_text(resto, encoding="utf-8")
        return "tolto"
    percorso.unlink()
    return "tolto (il file era tutto lì: cancellato)"


def elenco(dati: dict) -> str:
    righe = [f"Sciame {dati['versione']}: {len(dati['ruoli'])} ruoli, {len(dati['profili'])} profili.", ""]
    for nucleo in dati["nuclei"]:
        righe.append(f"Nucleo {nucleo['nome'].lower()}")
        righe += [f"  sciame-{r['sigla']}: {r['nome']}" for r in dati["ruoli"] if r["nucleo"] == nucleo["id"]]
    righe += ["", "Profili"]
    righe += [f"  {nome}: {p['per']}" for nome, p in dati["profili"].items()]
    return "\n".join(righe)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--controlla", action="store_true", help="esce con 1 se qualcosa non è allineato alle schede")
    p.add_argument("--installa", type=Path, metavar="RADICE", help="la radice di un altro progetto")
    p.add_argument("--istruzioni", type=Path, nargs="?", const=RADICE / "CLAUDE.md", metavar="FILE",
                   help="di norma CLAUDE.md nella radice del progetto")
    p.add_argument("--togli-istruzioni", type=Path, nargs="?", const=RADICE / "CLAUDE.md", metavar="FILE")
    p.add_argument("--togli", action="store_true", help="toglie gli agenti e le skill generati; sciame/ resta")
    p.add_argument("--elenco", action="store_true", help="stampa i ruoli e i profili")
    ns = p.parse_args()
    try:
        if ns.togli:
            tolti = togli(RADICE)
            print(f"Tolti {len(tolti)} file generati da {RADICE / '.claude'}")
            return
        if ns.togli_istruzioni:
            print(f"{ns.togli_istruzioni}: paragrafo dello sciame {togli_istruzioni(ns.togli_istruzioni)}")
            return
        dati = catalogo()
        if ns.elenco:
            print(elenco(dati))
        elif ns.istruzioni:
            print(f"{ns.istruzioni}: paragrafo dello sciame {istruzioni(ns.istruzioni, dati)}")
        elif ns.controlla:
            diversi = controlla(RADICE, dati)
            if diversi:
                print("\n".join(diversi))
                print("Non allineato alle schede: python3 -I sciame/genera_agenti.py")
                sys.exit(1)
            print(f"{len(dati['ruoli'])} ruoli e {len(dati['profili'])} profili: catalogo, agenti e skill allineati alle schede")
        else:
            radice = ns.installa.resolve() if ns.installa else RADICE
            fatti = installa(radice, dati) if ns.installa else scrivi(radice, dati)
            print(f"{len(dati['ruoli'])} ruoli e {len(dati['profili'])} profili per Claude Code in {radice} ({len(fatti)} file)")
    except (Errore, OSError) as e:
        print(f"genera_agenti: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
