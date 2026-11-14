#!/usr/bin/env python3
"""f12, 07-controprova-identita (sciame-avversario) — casi NUOVI contro le correzioni di 06-identita.

Uso: <python> -I -B attacco.py <blocco|tutti> [processi]   → risultati/att_<blocco>.jsonl (una riga per sequenza e conf)
La catena è la COPIA in ./catena (identica a 06-identita/catena: vedi DIFFERENZE.md). Il simulatore di f10 è importato
in sola lettura e pilotato da qui (pannello, linea, velocità, buchi, posa: sostituzioni in memoria, niente su disco).
Semi: k = 300… (mai usati dall'autore). Configurazioni: «prima» (catena di f10) e «tutte_p» (finale dell'autore)."""
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
import catena as _cat                                          # noqa: E402,F401
import parametri as _par                                       # noqa: E402
assert os.path.dirname(_cat.__file__) == os.path.join(QUI, "catena")
sys.path.insert(1, os.path.join(F10, "20-validazione"))
sys.path.insert(2, os.path.join(F10, "11-simulatore"))
import numpy as np                                             # noqa: E402
import comune as K                                             # noqa: E402
assert K.Parametri is _par.Parametri
import misura_passaggi as MP                                   # noqa: E402
import misura_ostacoli as MO                                   # noqa: E402
import catalogo as C                                           # noqa: E402
import simsens as S                                            # noqa: E402
import genera as G                                             # noqa: E402

TUTTE = dict(soglia_proporzionale=True, riaggancio_rifiuta_tagliati=True, riaggancio_rifiuta_occlusore=True,
             riparti_al_riaggancio=True, strato_resta=True)
CONFIG = {"prima": {}, "tutte": dict(TUTTE),
          "tutte_p": dict(TUTTE, soglia_proporzionale=False, gruppi_per_picco=True)}
RIS, TMP = os.path.join(QUI, "risultati"), os.path.join(QUI, "tmp_att")
PANNELLO0 = dict(C.PANNELLO)
MOD = {"buchi": 1.0, "posa_err": 0.0}

# ---------------------------------------------------------------- sostituzioni in memoria nel simulatore
_prof0, _scena0, _pass0 = S.carica_profilo, C.scena, C.passaggio
PERCORSI = {   # punti per il verso +1 (sinistra→destra): (x, scarto in z); la x si specchia per i passaggi dispari
    "v16": dict(v=1.6, punti=[(-1.7, 0), (1.7, 0)]),
    "bordo": dict(v=1.2, punti=[(-1.3, 0), (2.0, 0)], fine="ferma", coda=3.0, verso=1.0),
    "bordo2": dict(v=1.2, punti=[(-1.3, 0), (2.05, 0)], fine="ferma", coda=3.0, verso=1.0),
    "estA": dict(v=1.2, punti=[(-1.7, 0), (-0.28, 0)], fine="ferma", coda=6.0),
    "estB": dict(v=1.2, punti=[(0.20, 0), (0.28, 0), (1.7, 0)], soste={1: 2.2}),
}


def carica_profilo(sigla, livello="nominale", larghezza=424, **kw):
    p = _prof0(sigla, livello, larghezza, **kw)
    f = MOD["buchi"]
    if f != 1.0:
        p["p_buco_materiale"] = [q if q >= 0.95 else min(0.95, q * f) for q in p["p_buco_materiale"]]
        p["p_buco_bordo"] = min(0.95, p["p_buco_bordo"] * f)
        p["p_buco_incidenza_75"] = min(0.95, p["p_buco_incidenza_75"] * f)
    return p


def scena(nome, **a):
    if nome == "cubo":
        d, lato = float(a["distanza"]), float(a["lato"])
        return S.Scena(ostacoli=[S.Scatola("cubo", -lato / 2, lato / 2, d, d + lato, 0.0, lato, tipo="scatola")]), \
            15.0 + MOD["posa_err"]
    sc, incl = _scena0(nome, **a)
    return sc, incl + (MOD["posa_err"] if incl else 0.0)


def passaggio(caso, k, scena_nome="pannello"):
    if caso not in PERCORSI:
        return _pass0(caso, k, scena_nome)
    c = PERCORSI[caso]
    rng = np.random.default_rng(S.seme_da_nome(f"percorso__{caso}__s{k:02d}"))
    verso = c.get("verso") or (1.0 if k % 2 == 0 else -1.0)
    zp = C.Z_ATTORE + rng.uniform(-0.03, 0.03)
    v = c["v"] * rng.uniform(0.9, 1.1)
    punti = [(verso * x, zp + dz) for x, dz in c["punti"]]
    x, z, vx, vz = C.campiona_percorso(punti, v, c.get("soste", {}), c.get("fine", "via"), rng, coda_s=c.get("coda", 0.0))
    return x, z, vx, vz, {"caso": caso, "passaggio": k, "velocita_crociera_ms": round(v, 4), "z_linea_m": round(zp, 4)}


S.carica_profilo, C.scena, C.passaggio = carica_profilo, scena, passaggio


def imposta(l):
    C.PANNELLO = dict(PANNELLO0, **(l.get("pannello") or {}))
    C.Z_ATTORE = l.get("z_att", 2.3)
    MOD["buchi"], MOD["posa_err"] = l.get("buchi", 1.0), l.get("posa_err", 0.0)
    P = C.PANNELLO
    MP.sul_pannello = lambda x, z: P["x0"] - 0.15 <= x <= P["x1"] + 0.15 and P["z0"] - 0.2 <= z <= P["z1"] + 0.18


def genera(spec, larghezza):
    tempi, quadri, vers, extra = [], [], [], None
    for i, t, f, ver, extra in G.simula(spec, larghezza=larghezza):
        tempi.append(t)
        quadri.append(f)
        vers.append(ver)
    meta, verita = G.meta_e_verita(spec, extra["prof"], extra["cam"], extra["scena"], extra["tracce"], vers)
    if MOD["posa_err"]:
        meta["posa"]["inclinazione_gradi"] = 15.0          # la catena crede alla posa nominale
    return meta, tempi, quadri, verita


def spec_di(l):
    prof, liv, k, g = l["profilo"], l["livello"], l.get("k", 0), l["gruppo"]
    t = l["tipo"]
    if t == "passa":
        pers = C._pers(l.get("caso", "a12"), k, materiale=l.get("materiale", S.M_CHIARO), altezza=l.get("altezza", 1.7))
        return C._spec(g, prof, liv, "pannello", f"{g}__s{k:02d}", persone=[pers])
    if t == "estraneo":
        a = C._pers("estA", k)
        b = dict(C._pers("estB", k), id="s2")
        return C._spec(g, prof, liv, "pannello", f"{g}__s{k:02d}", persone=[a, b])
    if t == "statica":
        pers = []
        if "ferma" in l:
            pers = [dict(C._ferma(*l["ferma"]), altezza=l.get("altezza", 1.7))]
        return C._spec(g, prof, liv, l["scena"], f"{g}__n{k:02d}", l.get("arg"), n=l.get("n", 10), persone=pers)
    raise ValueError(t)


def libero_in_ombra(stati, verita, fino=None):
    centro = K.classi_polari(verita)[0]
    ombra = (centro == 1) | (centro == 3)
    st = stati if fino is None else stati[:fino]
    return int((st[:, ombra] == K.LIBERO).sum()), int(ombra.sum()) * int(st.shape[0])


def vuoto_dopo(righe, pres, ver):
    """Dopo l'ombra: fotogrammi con la persona visibile ≥ 50 % e nessuna traccia «osservato» su di lei."""
    T = len(righe)
    sog = [f["soggetti"][0] for f in ver["fotogrammi"][:T]]
    fraz = np.array([s["frazione_visibile"] for s in sog])
    nasc = np.nonzero(fraz < 0.02)[0]
    if len(nasc) == 0:
        return None
    k1 = int(nasc[-1])
    dopo = [k for k in range(k1 + 1, T) if fraz[k] >= 0.5]
    con = [k for k in dopo if MP.traccia_del_soggetto(righe[k], sog[k]["x"], sog[k]["z"]) is not None]
    ids = sorted({MP.traccia_del_soggetto(righe[k], sog[k]["x"], sog[k]["z"])["id"] for k in con})
    return {"dopo": len(dopo), "senza_traccia": len(dopo) - len(con),
            "attesa_prima_traccia": (con[0] - dopo[0]) if con else None, "id_dopo": ids,
            "avviso_acceso_dopo": int(sum(bool(pres[k].any()) for k in range(k1 + 1, T))), "fotogrammi_dopo_ombra": T - k1 - 1}


def mis_estraneo(righe, pres, stati, ver):
    T = len(righe)
    A = [f["soggetti"][0] for f in ver["fotogrammi"][:T]]
    B = [f["soggetti"][1] for f in ver["fotogrammi"][:T]]
    nascA = [k for k in range(T) if A[k]["frazione_visibile"] < 0.02]
    out = {"A_nascosta": len(nascA)}
    if not nascA:
        return out
    k0 = nascA[0]
    votiA, votiB = {}, {}
    for k in range(k0):
        tr = MP.traccia_del_soggetto(righe[k], A[k]["x"], A[k]["z"])
        if tr is not None and A[k]["frazione_visibile"] >= 0.98:
            votiA[tr["id"]] = votiA.get(tr["id"], 0) + 1
    visB = [k for k in range(k0, T) if B[k]["frazione_visibile"] >= 0.5]
    for k in visB:
        tr = MP.traccia_del_soggetto(righe[k], B[k]["x"], B[k]["z"])
        if tr is not None and B[k]["frazione_visibile"] >= 0.98:
            votiB[tr["id"]] = votiB.get(tr["id"], 0) + 1
    idA = max(votiA, key=lambda i: (votiA[i], -i)) if votiA else None
    idB = max(votiB, key=lambda i: (votiB[i], -i)) if votiB else None
    ri = [(k, e) for k, r in enumerate(righe) for e in r["eventi"] if e["tipo"] == "riaggancio"]
    kB = visB[0] if visB else T
    kR = ri[0][0] if ri else T
    f_tot = f_dopoB = f_dopoR = lib = n_dopoB = n_dopoR = 0
    for k in nascA:
        c = K.cella(A[k]["x"], A[k]["z"])
        dentro = bool(c is not None and pres[k][c])
        f_tot += not dentro
        lib += bool(c is not None and stati[k][c] == K.LIBERO)
        if k >= kB:
            n_dopoB += 1
            f_dopoB += not dentro
        if k >= kR:
            n_dopoR += 1
            f_dopoR += not dentro
    out.update(idA=idA, idB=idB, identita_passata_a_B=bool(idA is not None and idA == idB), B_visibile=len(visB),
               riagganci=len(ri), riaggancio_presunto=[e.get("identita") for _, e in ri][:3],
               A_fuori_avviso=f_tot, A_nascosta_dopo_B=n_dopoB, A_fuori_avviso_dopo_B=f_dopoB,
               A_nascosta_dopo_riaggancio=n_dopoR, A_fuori_avviso_dopo_riaggancio=f_dopoR, A_cella_libero=lib)
    return out


def uno(l):
    t0 = time.time()
    radice = os.path.join(TMP, f"{l['gruppo']}_{os.getpid()}_{l['n_lavoro']}")
    righe_out = []
    try:
        imposta(l)
        spec = spec_di(l)
        nome = spec["nome"]
        meta, tempi, quadri, verita = genera(spec, l["larghezza"])
        n1 = len(quadri)
        if l.get("rimozione"):                 # dopo il passaggio il pannello sparisce: 30 fotogrammi di pavimento vuoto
            sp2 = C._spec(l["gruppo"], l["profilo"], l["livello"], "pavimento", f"{l['gruppo']}_vuoto__s{l['k']:02d}", n=30)
            _, _, q2, _ = genera(sp2, l["larghezza"])
            quadri = quadri + q2
            tempi = tempi + [tempi[-1] + (i + 1) / C.FPS for i in range(len(q2))]
        seq_sim = os.path.join(radice, "_verita")
        os.makedirs(os.path.join(seq_sim, nome), exist_ok=True)
        with open(os.path.join(seq_sim, nome, "verita.json"), "w", encoding="utf-8") as f:
            json.dump(verita, f)
        for conf in l.get("conf", ("prima", "tutte_p")):
            base = os.path.join(radice, conf)
            par = dataclasses.replace(K.Parametri(), **CONFIG[conf])
            r, err, _ = K.corri(K.SorgenteMemoria(meta, tempi, quadri), os.path.join(base, nome), par)
            riga = {k_: l.get(k_) for k_ in ("gruppo", "tipo", "profilo", "livello", "larghezza", "k")}
            riga.update(nome=nome, conf=conf, errore=err)
            if err is None:
                g = K.leggi_griglie(os.path.join(base, nome))
                stati, pres = g["stati"], g["possibile_presenza"]
                rr = K.leggi_righe(os.path.join(base, nome))
                riga.update(fotogrammi=r["fotogrammi"], ms_media=r["tempo_ciclo_ms"]["media"],
                            tracce_confermate=r["tracce_confermate"], eventi=r["eventi"])
                riga["libero_in_ombra"], riga["celle_ombra_fot"] = libero_in_ombra(stati, verita, n1)
                K.SEQ_SIM = seq_sim
                try:
                    if l.get("rimozione"):
                        acc = [bool(pres[k].any()) for k in range(len(rr))]
                        dopo = acc[n1:]
                        riga["rimozione"] = {"acceso_alla_rimozione": bool(acc[n1 - 1]), "fotogrammi_acceso_dopo": int(sum(dopo)),
                                             "ultimo_acceso": max([i for i, a in enumerate(dopo) if a], default=-1),
                                             "acceso_alla_fine": bool(dopo[-1])}
                    elif l["tipo"] == "passa":
                        m = MP.misura(nome, base)
                        for c in ("nascosti", "esito_identita", "continuita_pulita", "pannello_si_muove", "tracce_fantasma",
                                  "riagganci_a_soggetto_nascosto", "stato_traccia_nascosto", "cella_centro_nascosto",
                                  "fotogrammi_dopo", "id_prima", "motivi_ambigua"):
                            riga[c] = m.get(c)
                        riga["eventi_traccia"] = m.get("eventi")
                        riga["vuoto"] = vuoto_dopo(rr, pres, verita)
                    elif l["tipo"] == "estraneo":
                        riga["estraneo"] = mis_estraneo(rr, pres, stati, verita)
                    elif l["tipo"] == "statica":
                        if verita["ostacoli"] and l["scena"] != "pavimento":
                            riga["ostacoli"] = [{k_: o[k_] for k_ in ("ostacolo", "fotogrammi", "fotogrammi_visto_entro_15cm")}
                                                for o in MO.misura(nome, base)]
                        if "bersaglio" in l:   # (x, z, raggio, larghezza massima): un gruppo PROPRIO sul bersaglio
                            bx, bz, rag, lmax = l["bersaglio"]
                            riga["gruppo_sul_bersaglio"] = int(sum(
                                any(math.hypot(g_["x"] - bx, g_["z"] - bz) <= rag and g_["larghezza_m"] <= lmax
                                    for g_ in rg["gruppi"]) for rg in rr))
                            riga["traccia_sul_bersaglio"] = int(sum(
                                any(tr["stato"] == "osservato" and math.hypot(tr["ultima_misura"][0] - bx, tr["ultima_misura"][1] - bz) <= rag
                                    for tr in rg["tracce"]) for rg in rr))
                finally:
                    K.SEQ_SIM = os.path.join(K.SIM, "sequenze")
            righe_out.append(riga)
    finally:
        shutil.rmtree(radice, ignore_errors=True)
    for riga in righe_out:
        riga["secondi_lavoro"] = round(time.time() - t0, 1)
    return righe_out


def lavori(blocco):
    L = []
    D = dict(profilo="d435i", livello="nominale", larghezza=424)

    def passi(gruppo, n=10, **kw):
        return [dict(D, tipo="passa", gruppo=gruppo, k=300 + k, **kw) for k in range(n)]

    def statiche(gruppo, n=3, **kw):
        return [dict(D, tipo="statica", gruppo=gruppo, k=k, **kw) for k in range(n)]

    if blocco in ("geometria", "tutti"):
        L += passi("A1_pann21_pers28", pannello=dict(z0=2.10, z1=2.12), z_att=2.8)
        L += passi("A1b_pann15_pers20", pannello=dict(z0=1.50, z1=1.52), z_att=2.0)
        L += passi("A2_640px", larghezza=640)
        L += passi("A2_d455_a05", profilo="d455", caso="a05")
        L += passi("A2_g335_a05", profilo="g335", caso="a05")
        L += passi("A5_v16", caso="v16")
        L += passi("A5_a05", caso="a05")
        L += passi("B3_bordo_campo", caso="bordo", pannello=dict(x0=0.2, x1=1.2))
    if blocco in ("rumore", "tutti"):
        L += passi("A3_limite", livello="limite")
        L += passi("A3_limite_buchi35", livello="limite", buchi=3.5)
        L += passi("A3_nominale_buchi35", buchi=3.5)
        L += passi("A6_posa_piu05", posa_err=0.5)
        L += passi("A6_posa_meno05", posa_err=-0.5)
        L += statiche("A6_pavimento_piu05", scena="pavimento", n=30, posa_err=0.5)
        L += statiche("A6_pavimento_meno05", scena="pavimento", n=30, posa_err=-0.5)
        L += statiche("A3_scatola20_limite_buchi35", scena="scatola15", arg={"distanza": 2.0}, livello="limite", buchi=3.5,
                      bersaglio=(0.0, 2.075, 0.25, 0.6))
        L += statiche("A3_pavimento_limite_buchi35", scena="pavimento", n=30, livello="limite", buchi=3.5)
    if blocco in ("persona", "tutti"):
        L += passi("A4_alta120", altezza=1.2)
        L += passi("A4_bambino100", altezza=1.0)
        L += passi("A4_scura", materiale=S.M_SCURO)
        L += passi("A4_nera", materiale=S.M_NERO)
    if blocco in ("rotto", "tutti"):
        for w in (424, 848):
            L += statiche(f"B1_scatola15_2p0m_{w}", scena="scatola15", arg={"distanza": 2.0}, larghezza=w, bersaglio=(0.0, 2.075, 0.25, 0.6))
            L += statiche(f"B1_scatola15_2p8m_{w}", scena="scatola15", arg={"distanza": 2.8}, larghezza=w, bersaglio=(0.0, 2.875, 0.25, 0.6))
            L += statiche(f"B2_cubo10_2p0m_{w}", scena="cubo", arg={"distanza": 2.0, "lato": 0.10}, larghezza=w, bersaglio=(0.0, 2.05, 0.25, 0.6))
        L += statiche("B2_bambino_aperto", scena="pavimento", n=20, ferma=(0.0, 2.5), altezza=1.0, bersaglio=(0.0, 2.5, 0.3, 0.8))
        L += statiche("B2_bambino_al_pannello", scena="pannello", n=20, ferma=(0.72, 1.95), altezza=1.0, bersaglio=(0.72, 1.95, 0.3, 0.8))
        L += statiche("B2_adulto_al_pannello", scena="pannello", n=20, ferma=(0.72, 1.95), altezza=1.7, bersaglio=(0.72, 1.95, 0.3, 0.8))
        L += passi("B4_rimozione", rimozione=True)
    if blocco in ("bordo2", "tutti"):     # aggiunto alle 18:27 dopo l'esito di B3 (vedi PREVISIONI.md)
        L += passi("B3b_bordo_campo_stretto", caso="bordo2", pannello=dict(x0=0.5, x1=1.5))
    if blocco in ("estraneo", "tutti"):
        for w in (424, 848):
            L += [dict(D, tipo="estraneo", gruppo=f"E_estraneo_{w}", k=300 + k, larghezza=w) for k in range(10)]
    if not L:
        raise SystemExit("blocco sconosciuto")
    for n, l in enumerate(L):
        l["n_lavoro"] = n
    return L


def main():
    blocco = sys.argv[1]
    proc = min(8, int(sys.argv[2])) if len(sys.argv) > 2 else 8
    os.makedirs(RIS, exist_ok=True)
    L = lavori(blocco)
    import multiprocessing as mp
    t0 = time.time()
    with mp.get_context("fork").Pool(proc) as pool, open(os.path.join(RIS, f"att_{blocco}.jsonl"), "w", encoding="utf-8") as f:
        for righe in pool.imap_unordered(uno, L, chunksize=1):
            for r in righe:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
    shutil.rmtree(TMP, ignore_errors=True)
    print(f"att_{blocco}: {len(L)} sequenze, {time.time() - t0:.0f} s")


if __name__ == "__main__":
    main()
