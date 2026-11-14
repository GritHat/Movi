#!/usr/bin/env python3
"""f12, 06-identita — passa le sequenze nella COPIA corretta della catena, una configurazione alla volta, e misura.

Uso: <python> -I -B prova.py <blocco> [processi]   → risultati/<blocco>.jsonl (una riga per sequenza e configurazione)
Blocchi: disco (424, sequenze di f10, sola lettura) | nuovi424 | nuovi848 | due424 | due848 | z21_424 | z21_848\n(semi nuovi, in memoria).
La misura dei passaggi è `misura_passaggi.misura` di f10/20-validazione (importata, non modificata); la catena
importata è quella di ./catena (caricata PRIMA di `comune`, così i moduli di f10 non vengono presi)."""
import dataclasses
import json
import math
import os
import shutil
import sys
import time

for _n in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_n, "1")
sys.dont_write_bytecode = True
QUI = os.path.dirname(os.path.abspath(__file__))
F10 = os.path.normpath(os.path.join(QUI, "..", "..", "f10-dati"))
sys.path.insert(0, os.path.join(QUI, "catena"))
import catena as _cat                                          # noqa: E402,F401  (la copia: prima di tutto il resto)
import parametri as _par                                       # noqa: E402
assert os.path.dirname(_cat.__file__) == os.path.join(QUI, "catena")
sys.path.insert(1, os.path.join(F10, "20-validazione"))
sys.path.insert(2, os.path.join(F10, "11-simulatore"))
import numpy as np                                             # noqa: E402
import comune as K                                             # noqa: E402
assert K.Parametri is _par.Parametri, "comune.py ha caricato la catena di f10 invece della copia"
import misura_passaggi as MP                                   # noqa: E402
import misura_ostacoli as MO                                   # noqa: E402

TUTTE = dict(soglia_proporzionale=True, riaggancio_rifiuta_tagliati=True, riaggancio_rifiuta_occlusore=True,
             riparti_al_riaggancio=True, strato_resta=True)
CONFIG = {
    "prima": {},
    "f401": dict(soglia_proporzionale=True),
    "f402": dict(riaggancio_rifiuta_tagliati=True, riaggancio_rifiuta_occlusore=True),
    "f408": dict(riparti_al_riaggancio=True),
    "f409": dict(strato_resta=True),
    "tutte": dict(TUTTE),
    "f401p": dict(gruppi_per_picco=True),                      # tracciamento-1 al posto della soglia sui pixel attesi
    "tutte_p": dict(TUTTE, soglia_proporzionale=False, gruppi_per_picco=True),
    "tutte_p2": dict(TUTTE, soglia_proporzionale=False, gruppi_per_picco=True, tagliato_su_componente=True),
}
EXTRA = json.loads(os.environ.get("F12_EXTRA", "{}"))          # parametri in più per «f401» e «tutte» (taratura dichiarata)
for _c in ("f401", "tutte", "f401p", "tutte_p", "tutte_p2"):
    CONFIG[_c].update(EXTRA)
SOLO = [c for c in os.environ.get("F12_CONFIG", "").split(",") if c] or [c for c in CONFIG if c != "tutte_p2"]
RIS = os.path.join(QUI, "risultati")
TMP = os.path.join(QUI, "tmp")


def genera(spec, larghezza):
    import genera as G
    tempi, quadri, vers, extra = [], [], [], None
    for i, t, f, ver, extra in G.simula(spec, larghezza=larghezza):
        tempi.append(t)
        quadri.append(f)
        vers.append(ver)
    meta, verita = G.meta_e_verita(spec, extra["prof"], extra["cam"], extra["scena"], extra["tracce"], vers)
    return meta, tempi, quadri, verita


def spec_di(lavoro):
    import catalogo as C
    tipo, prof, liv, k = lavoro["tipo"], lavoro["profilo"], lavoro["livello"], lavoro.get("k", 0)
    C.Z_ATTORE = lavoro.get("z_attore", 2.3)                    # la linea di chi cammina (2,3 m nel catalogo di f10)
    if tipo == "a12z":                                           # attacco A8 dell'avversario: linea a 2,1 m
        return C._spec("a12", prof, liv, "pannello", f"pannello_a12z21__s{k:02d}", persone=[C._pers("a12", k)])
    if tipo in ("a12", "a05", "b", "c", "d"):
        return C._spec(tipo, prof, liv, "pannello", f"pannello_{tipo}__s{k:02d}", persone=[C._pers(tipo, k)])
    if tipo == "scatola":
        return C._spec("altre", prof, liv, "scatola15", f"scatola15_2p0m_f12n{k:02d}", {"distanza": 2.0}, n=10)
    if tipo == "pavimento":
        return C._spec("statiche", prof, liv, "pavimento", f"pavimento_vuoto_f12n{k:02d}", n=30)
    if tipo == "pannello_vuoto":
        return C._spec("statiche", prof, liv, "pannello", f"pannello_vuoto_f12n{k:02d}", n=30)
    if tipo == "due":                       # chi cammina (a12) più una persona MAI VISTA ferma nell'ombra, a z = 2,6 m
        cammina = C._pers("a12", k)
        ferma = dict(C._ferma(lavoro.get("x_ferma", 0.0), 2.6), id="s2")
        return C._spec("due", prof, liv, "pannello", f"pannello_due_f12__s{k:02d}", persone=[cammina, ferma])
    raise ValueError(tipo)


def libero_in_ombra(stati, verita):
    centro = K.classi_polari(verita)[0]
    ombra = (centro == 1) | (centro == 3)
    return int((stati[:, ombra] == K.LIBERO).sum()), int(ombra.sum()) * int(stati.shape[0])


def uno(lavoro):
    """Un lavoro = una sequenza; tutte le configurazioni. Restituisce la lista delle righe di risultato."""
    t0 = time.time()
    nome = lavoro.get("nome")
    radice_tmp = os.path.join(TMP, f"{lavoro['blocco']}_{os.getpid()}_{lavoro['n']}")
    righe = []
    try:
        if lavoro["tipo"] == "disco":
            cart = os.path.join(K.SEQ_SIM, nome)
            fabbrica = lambda: K.SorgenteCartella(cart)                                   # noqa: E731
            verita = K.leggi_verita(cart)
            seq_sim = K.SEQ_SIM
        else:
            spec = spec_di(lavoro)
            nome = spec["nome"]
            meta, tempi, quadri, verita = genera(spec, lavoro["larghezza"])
            fabbrica = lambda: K.SorgenteMemoria(meta, tempi, quadri)                     # noqa: E731
            seq_sim = os.path.join(radice_tmp, "_verita")
            os.makedirs(os.path.join(seq_sim, nome), exist_ok=True)
            with open(os.path.join(seq_sim, nome, "verita.json"), "w", encoding="utf-8") as f:
                json.dump(verita, f)
        ha_soggetto = bool(verita["fotogrammi"] and verita["fotogrammi"][0]["soggetti"])
        for conf in SOLO:
            base = os.path.join(radice_tmp, conf)
            par = dataclasses.replace(K.Parametri(), **CONFIG[conf])
            r, err, _ = K.corri(fabbrica(), os.path.join(base, nome), par)
            riga = {"blocco": lavoro["blocco"], "nome": nome, "tipo": lavoro["tipo"], "conf": conf, "errore": err,
                    "larghezza": lavoro.get("larghezza", 424), "profilo": lavoro.get("profilo"), "livello": lavoro.get("livello")}
            if err is None:
                g = K.leggi_griglie(os.path.join(base, nome))
                stati, pres = g["stati"], g["possibile_presenza"]
                riga.update(fotogrammi=r["fotogrammi"], ms_media=r["tempo_ciclo_ms"]["media"], ms_p95=r["tempo_ciclo_ms"]["p95"],
                            ms_max=r["tempo_ciclo_ms"]["massimo"], tracce_confermate=r["tracce_confermate"],
                            eventi=r["eventi"], avviso_acceso_alla_fine=bool(pres[-1].any()))
                riga["libero_in_ombra"], riga["celle_ombra_fot"] = libero_in_ombra(stati, verita)
                K.SEQ_SIM = seq_sim
                try:
                    if ha_soggetto and "sensore_" not in nome and "azzeramento" not in nome:
                        m = MP.misura(nome, base)
                        for c in ("nascosti", "esito_identita", "continuita_pulita", "pannello_si_muove", "tracce_fantasma",
                                  "fusione_fotogrammi_interi", "riagganci_a_soggetto_nascosto", "stato_traccia_nascosto",
                                  "cella_centro_nascosto", "fotogrammi_dopo", "id_prima", "motivi_ambigua"):
                            riga[c] = m.get(c)
                        riga["eventi_traccia"] = m.get("eventi")
                    if any(s in nome for s in ("scatola15_", "pannello_vuoto")):
                        riga["ostacoli"] = [{k_: o[k_] for k_ in ("ostacolo", "fotogrammi", "fotogrammi_visto_entro_15cm")}
                                            for o in MO.misura(nome, base)]
                    if not ha_soggetto:                          # scena senza persone: una traccia «si muove»?
                        muove = set()
                        for rg in K.leggi_righe(os.path.join(base, nome)):
                            muove.update(tr["id"] for tr in rg["tracce"] if tr["si_muove"] is True)
                        riga["tracce_si_muove"] = len(muove)
                    if lavoro["tipo"] == "due":                  # la persona ferma mai vista (soggetto 2)
                        rr = K.leggi_righe(os.path.join(base, nome))
                        fr = verita["fotogrammi"][:len(rr)]
                        nasc1 = [k for k, f_ in enumerate(fr) if f_["soggetti"][0]["frazione_visibile"] < 0.02]
                        k0 = nasc1[0] if nasc1 else len(fr)
                        primo_ri = next((k for k, rg in enumerate(rr) if any(e["tipo"] == "riaggancio" for e in rg["eventi"])), None)
                        fuori_dopo_k0 = fuori_dopo_ri = nasc_dopo_k0 = nasc_dopo_ri = 0
                        for k, f_ in enumerate(fr):
                            s2 = f_["soggetti"][1]
                            if s2["frazione_visibile"] >= 0.02 or k < k0:
                                continue
                            c = K.cella(s2["x"], s2["z"])
                            dentro = bool(c is not None and pres[k][c])
                            nasc_dopo_k0 += 1
                            fuori_dopo_k0 += not dentro
                            if primo_ri is not None and k >= primo_ri:
                                nasc_dopo_ri += 1
                                fuori_dopo_ri += not dentro
                        riga["ferma"] = {"nascosta_dopo_ingresso": nasc_dopo_k0, "fuori_avviso_dopo_ingresso": fuori_dopo_k0,
                                         "nascosta_dopo_riaggancio": nasc_dopo_ri, "fuori_avviso_dopo_riaggancio": fuori_dopo_ri,
                                         "riaggancio_al_fotogramma": primo_ri}
                finally:
                    K.SEQ_SIM = os.path.join(K.SIM, "sequenze")
            righe.append(riga)
    finally:
        shutil.rmtree(radice_tmp, ignore_errors=True)
    for riga in righe:
        riga["secondi_lavoro"] = round(time.time() - t0, 1)
    return righe


def lavori(blocco):
    L = []
    if blocco == "disco":
        import re
        buoni = re.compile(r"pannello_(a12|a05|b|c|d)(_scuro|_nero|_alta185)?__s\d\d$|pavimento_vuoto$|scatola15_2p0m$|pannello_vuoto$")
        for n in sorted(os.listdir(K.SEQ_SIM)):
            if os.path.isdir(os.path.join(K.SEQ_SIM, n)) and buoni.search(n):
                L.append({"tipo": "disco", "nome": n})
    elif blocco in ("nuovi424", "nuovi848"):
        w = int(blocco[-3:])
        P = [("d435i", "nominale", 30), ("d455", "nominale", 10), ("g335", "nominale", 10), ("d435i", "limite", 10)]
        for prof, liv, n in P:
            for caso in ("a12", "a05", "b"):
                quanti = n if (prof, liv) == ("d435i", "nominale") or caso == "a12" else 0
                L += [{"tipo": caso, "profilo": prof, "livello": liv, "k": 100 + k, "larghezza": w} for k in range(quanti)]
            L += [{"tipo": "scatola", "profilo": prof, "livello": liv, "k": k, "larghezza": w} for k in range(10 if n == 30 else 3)]
            L += [{"tipo": "pavimento", "profilo": prof, "livello": liv, "k": k, "larghezza": w} for k in range(3)]
            L += [{"tipo": "pannello_vuoto", "profilo": prof, "livello": liv, "k": k, "larghezza": w} for k in range(3)]
        L += [{"tipo": "c", "profilo": "d435i", "livello": "nominale", "k": 100 + k, "larghezza": w} for k in range(20)]
        L += [{"tipo": "d", "profilo": "d435i", "livello": "nominale", "k": 100 + k, "larghezza": w} for k in range(10)]
    elif blocco in ("due424", "due848"):
        w = int(blocco[-3:])
        L += [{"tipo": "due", "profilo": "d435i", "livello": "nominale", "k": 100 + k, "larghezza": w,
               "x_ferma": (-0.3, 0.0, 0.3)[k % 3]} for k in range(12)]
    elif blocco in ("ultimi424", "ultimi848"):                    # semi mai usati (k = 200…) per «tutte_p2»
        w = int(blocco[-3:])
        for caso in ("a12", "a05", "b"):
            L += [{"tipo": caso, "profilo": "d435i", "livello": "nominale", "k": 200 + k, "larghezza": w} for k in range(30)]
        L += [{"tipo": "c", "profilo": "d435i", "livello": "nominale", "k": 200 + k, "larghezza": w} for k in range(10)]
        L += [{"tipo": "a12z", "profilo": "d435i", "livello": "nominale", "k": 200 + k, "larghezza": w, "z_attore": 2.1}
              for k in range(10)]
        for prof in ("d455", "g335"):
            L += [{"tipo": "a12", "profilo": prof, "livello": "nominale", "k": 200 + k, "larghezza": w} for k in range(5)]
    elif blocco in ("z21_424", "z21_848"):
        w = int(blocco[-3:])
        L += [{"tipo": "a12z", "profilo": "d435i", "livello": "nominale", "k": 100 + k, "larghezza": w, "z_attore": 2.1}
              for k in range(10)]
    else:
        raise SystemExit("blocco sconosciuto")
    for n, l in enumerate(L):
        l.update(blocco=blocco, n=n)
    return L


def main():
    blocco = sys.argv[1]
    proc = min(8, int(sys.argv[2])) if len(sys.argv) > 2 else 8
    suff = os.environ.get("F12_ETICHETTA", "")
    os.makedirs(RIS, exist_ok=True)
    L = lavori(blocco)
    import multiprocessing as mp
    t0 = time.time()
    with mp.get_context("fork").Pool(proc) as pool, open(os.path.join(RIS, f"{blocco}{suff}.jsonl"), "w", encoding="utf-8") as f:
        for righe in pool.imap_unordered(uno, L, chunksize=1):
            for r in righe:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
    shutil.rmtree(TMP, ignore_errors=True)
    print(f"{blocco}{suff}: {len(L)} sequenze, {len(SOLO)} configurazioni, {time.time() - t0:.0f} s, parametri in più {EXTRA}")


if __name__ == "__main__":
    main()
