#!/usr/bin/env python3
"""V23 — due soglie della catena (min_punti_ostacolo, min_celle_gruppo) contro fantasmi, ponti e ostacoli piccoli.
Taratura su: scene vuote, scatola15_2p0m, sospeso_2p8m, cassa_persona, passaggi PARI di a12, a05, b (D435i nominale).
Uso: <python> -I -B taratura.py tara        (le 8 coppie sull'insieme di taratura)
     <python> -I -B taratura.py prova P C   (la coppia scelta sui passaggi DISPARI e sul resto)"""
import dataclasses
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comune as K                                             # noqa: E402
import misura_libero                                           # noqa: E402
import misura_ostacoli                                         # noqa: E402
import misura_passaggi                                         # noqa: E402

TARA = r"(pavimento_vuoto$|pannello_vuoto$|scatola15_2p0m|sospeso_2p8m|cassa_persona|d435i_nom__pannello_(a12|a05|b)__s\d[02468]$)"
PROVA = r"(d435i_nom__pannello_(a12|a05|b)__s\d[13579]$)"


def corri(regex, etichetta, **par):
    radice = os.path.join(K.USCITE, etichetta)
    nomi = sorted(n for n in os.listdir(K.SEQ_SIM) if os.path.isdir(os.path.join(K.SEQ_SIM, n)) and re.search(regex, n))
    for n in nomi:
        _, err, _ = K.corri(K.SorgenteCartella(os.path.join(K.SEQ_SIM, n)), os.path.join(radice, n),
                            dataclasses.replace(K.Parametri(), **par))
        if err:
            print("ERRORE", n, err)
    return radice, nomi


def riga(radice, nomi):
    vuote = {n: misura_libero.misura(n, radice) for n in nomi if n.endswith("_vuoto")}
    fant = {n.replace("__pavimento_vuoto", "/pav").replace("__pannello_vuoto", "/pan"):
            m["tracce_confermate"] - (1 if "pannello" in n else 0) for n, m in vuote.items()}
    ost = {}
    for n in nomi:
        if "scatola15" in n or "sospeso" in n or "cassa_persona" in n:
            for m in misura_ostacoli.misura(n, radice):
                ost[m["ostacolo"]] = f"{m['fotogrammi_visto_entro_15cm']}/{m['fotogrammi']}"
    pas = {}
    for caso in ("a12", "a05", "b"):
        ms = [misura_passaggi.misura(n, radice) for n in nomi if f"d435i_nom__pannello_{caso}__" in n]
        if ms:
            pas[caso] = (f"pulita {sum(1 for m in ms if m.get('continuita_pulita'))}/{len(ms)}, stessa "
                         f"{sum(1 for m in ms if m.get('esito_identita') == 'stessa')}, fusione "
                         f"{sum(1 for m in ms if m.get('fusione_fotogrammi_interi', 0) > 0)}, riagg. falsi "
                         f"{sum(1 for m in ms if m.get('riagganci_a_soggetto_nascosto', 0) > 0)}, «si muove» prima "
                         f"{sum(1 for m in ms if m.get('soggetto_si_muove_prima'))}, pannello «si muove» "
                         f"{sum(1 for m in ms if m['pannello_si_muove'])}")
    return fant, ost, pas


if __name__ == "__main__":
    if sys.argv[1] == "tara":
        for p in (3, 8, 20, 40):
            for c in (1, 3):
                radice, nomi = corri(TARA, f"tara_p{p}_c{c}", min_punti_ostacolo=p, min_celle_gruppo=c)
                fant, ost, pas = riga(radice, nomi)
                print(f"min_punti_ostacolo={p} min_celle_gruppo={c}\n   tracce fantasma sulle scene vuote: {fant}\n"
                      f"   ostacoli visti: {ost}\n   passaggi pari: {json.dumps(pas, ensure_ascii=False)}", flush=True)
    else:
        p, c = int(sys.argv[2]), int(sys.argv[3])
        radice, nomi = corri(PROVA, f"prova_p{p}_c{c}", min_punti_ostacolo=p, min_celle_gruppo=c)
        print(f"PROVA sui dispari, min_punti_ostacolo={p} min_celle_gruppo={c}: {json.dumps(riga(radice, nomi)[2], ensure_ascii=False)}")
