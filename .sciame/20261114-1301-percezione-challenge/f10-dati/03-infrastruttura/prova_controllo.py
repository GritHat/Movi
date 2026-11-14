"""Prova di controlla_sequenza.py: una sequenza valida e le sue varianti difettose.

    f10-dati/ambiente/venv/bin/python -I prova_controllo.py

Lavora in 03-infrastruttura/prove-tmp-sequenze/ (creata e cancellata dalla prova). Esce con 0 se le varianti
valide passano, le difettose sono rifiutate (uscita 1) e quelle «sospette» danno un avviso.
Limite dichiarato: le varianti le ha scritte lo stesso autore del programma di controllo."""
import json
import os
import pickle
import shutil
import subprocess
import sys

import numpy as np

QUI = os.path.dirname(os.path.abspath(__file__))
BANCO = os.path.join(QUI, "prove-tmp-sequenze")
CONTROLLO = os.path.join(QUI, "controlla_sequenza.py")
shutil.rmtree(BANCO, ignore_errors=True)
os.makedirs(BANCO)
BASE = os.path.join(BANCO, "base")
subprocess.run([sys.executable, "-I", os.path.join(QUI, "crea_esempio_sequenza.py"), BASE],
               check=True, capture_output=True, timeout=120)


def carica_json(c, nome):
    with open(os.path.join(c, nome), encoding="utf-8") as f:
        return json.load(f)


def salva_json(c, nome, dati):
    with open(os.path.join(c, nome), "w", encoding="utf-8") as f:
        json.dump(dati, f)


def cambia_meta(**nuovo):
    def f(c):
        m = carica_json(c, "meta.json")
        for k, v in nuovo.items():
            if v is ...:
                m.pop(k)
            else:
                m[k] = v
        salva_json(c, "meta.json", m)
    return f


def tutti_i_fotogrammi(trasforma):
    def f(c):
        d = os.path.join(c, "profondita")
        for nome in os.listdir(d):
            a = np.load(os.path.join(d, nome), allow_pickle=False)
            np.save(os.path.join(d, nome), trasforma(a), allow_pickle=False)
    return f


def righe_tempi(trasforma):
    def f(c):
        p = os.path.join(c, "tempi.csv")
        righe = open(p, encoding="utf-8").read().splitlines()
        open(p, "w", encoding="utf-8").write("\n".join(trasforma(righe)) + "\n")
    return f


def cambia_verita(trasforma):
    def f(c):
        v = carica_json(c, "verita.json")
        trasforma(v)
        salva_json(c, "verita.json", v)
    return f


def con_pickle(c):
    with open(os.path.join(c, "profondita", "000004.npy"), "wb") as f:
        np.save(f, np.array([{"a": 1}, None], dtype=object), allow_pickle=True)


def troncato(c):
    p = os.path.join(c, "profondita", "000007.npy")
    dati = open(p, "rb").read()
    open(p, "wb").write(dati[: len(dati) // 2])


def rinomina_meta(vecchia, nuova):
    def f(c):
        m = carica_json(c, "meta.json")
        m[nuova] = m.pop(vecchia)
        salva_json(c, "meta.json", m)
    return f


def scambia(righe):
    righe[5], righe[6] = righe[6], righe[5]
    return righe


def v_indice_fuori(v): v["fotogrammi"][-1]["indice"] = 999
def v_visibile_testo(v): v["fotogrammi"][3]["soggetti"][0]["visibile"] = "sì"
def v_senza_z(v): v["fotogrammi"][3]["soggetti"][0].pop("z")
def v_id_numero(v): v["fotogrammi"][0]["soggetti"][0]["id"] = 1
def v_poligono_corto(v): v["ostacoli"][0]["vertici"] = [[0, 1], [1, 1]]


# nome -> (modifica, opzioni, uscita attesa, testo che deve comparire)
VALIDE = {
    "V1 base (con verità), anche in modo rigoroso": (lambda c: None, ["--rigoroso", "--tutti"], 0, "rispetta"),
    "V2 senza verita.json": (lambda c: os.remove(os.path.join(c, "verita.json")), ["--rigoroso"], 0, "rispetta"),
    "V3 posa null": (cambia_meta(posa=None), ["--rigoroso"], 0, "rispetta"),
    "V4 chiave in più in meta.json": (cambia_meta(rumore_mm=2.5), ["--rigoroso"], 0, "chiave in più"),
}
DIFETTOSE = {
    "D1 profondità float32 in metri": (tutti_i_fotogrammi(lambda a: (a / 1000).astype(np.float32)), [], 1, "uint16"),
    "D2 profondità int16": (tutti_i_fotogrammi(lambda a: a.astype(np.int16)), [], 1, "uint16"),
    "D3 profondità uint16 a byte invertiti (>u2)": (tutti_i_fotogrammi(lambda a: a.astype(">u2")), [], 1, "uint16"),
    "D4 forma trasposta (larghezza, altezza)": (tutti_i_fotogrammi(lambda a: np.ascontiguousarray(a.T)), [], 1, "forma"),
    "D5 un fotogramma mancante": (lambda c: os.remove(os.path.join(c, "profondita", "000003.npy")), [], 1, "mancano"),
    "D6 un file in più in profondita/": (lambda c: shutil.copy(os.path.join(c, "profondita", "000000.npy"),
                                                               os.path.join(c, "profondita", "000999.npy")), [], 1, "in più"),
    "D7 tempi che non crescono": (righe_tempi(scambia), [], 1, "indici"),
    "D8 tempi uguali fra due fotogrammi": (righe_tempi(lambda r: r[:4] + ["3," + r[3].split(",")[1]] + r[5:]), [], 1, "crescere"),
    "D9 una riga in meno in tempi.csv": (righe_tempi(lambda r: r[:-1]), [], 1, "in più"),
    "D10 indici che partono da 1": (righe_tempi(lambda r: [r[0]] + [f"{k + 1},{x.split(',')[1]}" for k, x in enumerate(r[1:])]), [], 1, "indici"),
    "D11 manca fx in meta.json": (cambia_meta(fx=...), [], 1, "«fx»"),
    "D12 «width» al posto di «larghezza»": (rinomina_meta("larghezza", "width"), [], 1, "nome giusto"),
    "D13 fps = 0": (cambia_meta(fps=0), [], 1, "«fps»"),
    "D14 posa con chiavi sbagliate": (cambia_meta(posa={"altezza": 1.2, "inclinazione": 15}), [], 1, "posa"),
    "D15 manca licenza": (cambia_meta(licenza=...), [], 1, "«licenza»"),
    "D16 .npy con oggetti serializzati (pickle)": (con_pickle, [], 1, "senza pickle"),
    "D17 .npy troncato a metà": (troncato, [], 1, "illeggibile"),
    "D18 verità: indice che non esiste": (cambia_verita(v_indice_fuori), [], 1, "non esiste"),
    "D19 verità: «visibile» come testo": (cambia_verita(v_visibile_testo), [], 1, "true o false"),
    "D20 verità: manca z": (cambia_verita(v_senza_z), [], 1, "«z»"),
    "D21 verità: id numerico": (cambia_verita(v_id_numero), [], 1, "«id»"),
    "D22 verità: poligono con 2 vertici": (cambia_verita(v_poligono_corto), [], 1, "vertici"),
    "D23 manca tempi.csv": (lambda c: os.remove(os.path.join(c, "tempi.csv")), [], 1, "manca tempi.csv"),
    "D24 manca profondita/": (lambda c: shutil.rmtree(os.path.join(c, "profondita")), [], 1, "manca la cartella"),
}
SOSPETTE = {  # passano (uscita 0) ma con un avviso; con --rigoroso falliscono
    "S1 tempi.csv senza intestazione": (righe_tempi(lambda r: r[1:]), [], 0, "intestazione"),
    "S1b la stessa, in modo rigoroso": (righe_tempi(lambda r: r[1:]), ["--rigoroso"], 1, "intestazione"),
    "S2 unità 1/5000 di metro invece dei millimetri": (
        tutti_i_fotogrammi(lambda a: np.minimum(a.astype(np.uint32) * 5, 65535).astype(np.uint16)), [], 0, "AVVISO"),
    "S3 profondità in centimetri": (tutti_i_fotogrammi(lambda a: (a // 10).astype(np.uint16)), [], 0, "AVVISO"),
    "S4 inclinazione col segno sbagliato (-15°)": (cambia_meta(posa={"altezza_m": 1.2, "inclinazione_gradi": -15.0}), [], 0, "suolo previsto"),
    "S5 altezza della camera sbagliata (2,0 m)": (cambia_meta(posa={"altezza_m": 2.0, "inclinazione_gradi": 15.0}), [], 0, "suolo previsto"),
    "S6 fps dichiarati 30 con tempi a 15": (cambia_meta(fps=30), [], 0, "non corrisponde"),
    "S7 65535 al posto di 0 per «nessun dato»": (tutti_i_fotogrammi(lambda a: np.where(a == 0, 65535, a).astype(np.uint16)), [], 0, "65535"),
}

falliti = 0
for gruppo, casi in (("valida", VALIDE), ("difettosa", DIFETTOSE), ("sospetta", SOSPETTE)):
    for k, (nome, (modifica, opzioni, atteso, testo)) in enumerate(casi.items()):
        c = os.path.join(BANCO, f"{gruppo}{k}")
        shutil.copytree(BASE, c)
        modifica(c)
        r = subprocess.run([sys.executable, "-I", CONTROLLO, c, *opzioni], capture_output=True, text=True, timeout=120)
        ok = r.returncode == atteso and testo in r.stdout
        falliti += not ok
        righe = [x for x in r.stdout.splitlines() if x.startswith(("ERRORE", "AVVISO"))]
        print(f"[{'OK' if ok else 'FALLITA'}] {gruppo} {nome}: uscita {r.returncode} (attesa {atteso})"
              + (f"\n        {righe[0][:150].replace(BANCO, '…')}" if righe else ""))
        shutil.rmtree(c)

shutil.rmtree(BANCO, ignore_errors=True)
totale = len(VALIDE) + len(DIFETTOSE) + len(SOSPETTE)
print(f"ESITO: {totale - falliti}/{totale} prove passate ({len(VALIDE)} valide, {len(DIFETTOSE)} difettose, "
      f"{len(SOSPETTE)} sospette)")
sys.exit(1 if falliti else 0)
