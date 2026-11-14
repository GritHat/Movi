#!/usr/bin/env python3
"""riepilogo.py — cifre descrittive sulle sequenze scritte (nessuna soglia: non sono previsioni) e
sequenze/PASSAGGI.csv, una riga per passaggio con gli intervalli in cui il soggetto è nascosto.

  …/ambiente/venv/bin/python -I -B riepilogo.py
"""
import csv
import os
import sys

sys.dont_write_bytecode = True
QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, QUI)
sys.path.insert(0, os.path.normpath(os.path.join(QUI, "..", "03-infrastruttura")))

import numpy as np                      # noqa: E402

import catalogo as C                    # noqa: E402
import genera as G                      # noqa: E402
import simsens as S                     # noqa: E402
import controlla_sequenza as INFRA      # noqa: E402


def quadri(nome):
    cart = os.path.join(G.SEQUENZE, nome)
    idx, _ = INFRA.leggi_tempi(cart)
    return np.stack([INFRA.leggi_profondita(cart, i) for i in idx])


def passaggi():
    righe = []
    for s in C.catalogo():
        if not s["persone"] or "caso" not in s["persone"][0]:
            continue
        cart = os.path.join(G.SEQUENZE, s["nome"])
        if not os.path.isdir(cart):
            continue
        ver, meta = INFRA.leggi_verita(cart), INFRA.leggi_meta(cart)
        sg = [f["soggetti"][0] for f in ver["fotogrammi"]]
        fr = np.array([x["frazione_visibile"] for x in sg])
        px = np.array([x["pixel_visibili"] for x in sg])
        pv = np.array([x["pixel_validi"] for x in sg])
        xx = np.array([x["x"] for x in sg])
        par = meta["simulazione"]["percorsi"][0]

        def tratto(m):
            i = np.where(m)[0]
            return (int(i[0]), int(i[-1]), int(i.size)) if i.size else ("", "", 0)

        z0, z2, z50 = tratto(fr == 0), tratto(fr < 0.02), tratto(fr < 0.5)
        centro = np.abs(xx) < 0.40
        righe.append({
            "nome": s["nome"], "profilo": S.SIGLE[s["profilo"]], "livello": s["livello"], "caso": par["caso"],
            "passaggio": par["passaggio"], "verso": par["verso"], "velocita_crociera_ms": par["velocita_crociera_ms"],
            "z_linea_m": par["z_linea_m"], "altezza_persona_m": s["persone"][0]["altezza"],
            "materiale": S.MATERIALI[s["persone"][0]["materiale"]], "filtri": int(bool(s["filtri"])),
            "fotogrammi": int(fr.size),
            "nascosto_0_primo": z0[0], "nascosto_0_ultimo": z0[1], "nascosto_0_n": z0[2],
            "nascosto_2pc_primo": z2[0], "nascosto_2pc_ultimo": z2[1], "nascosto_2pc_n": z2[2],
            "sotto_50pc_primo": z50[0], "sotto_50pc_ultimo": z50[1], "sotto_50pc_n": z50[2],
            "pixel_visibili_max_dietro_il_pannello": int(px[centro].max()) if centro.any() else 0,
            "quota_validi_sul_soggetto_quando_intero": round(float(pv[fr == 1].sum() / max(px[fr == 1].sum(), 1)), 4),
        })
    with open(os.path.join(G.SEQUENZE, "PASSAGGI.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(righe[0].keys()))
        w.writeheader()
        w.writerows(righe)
    print(f"PASSAGGI.csv: {len(righe)} passaggi")
    for caso in ("a12", "a05", "b", "c", "d"):
        r = [x for x in righe if x["caso"] == caso and x["nome"].startswith("d435i_nom__pannello_" + caso + "__")
             and not x["filtri"]]
        n0, n2 = [x["nascosto_0_n"] for x in r], [x["nascosto_2pc_n"] for x in r]
        sp = sum(1 for x in r if x["pixel_visibili_max_dietro_il_pannello"] > 0)
        print(f"caso {caso}: {len(r)} passaggi; fotogrammi nascosti (frazione = 0) da {min(n0)} a {max(n0)}, mediana "
              f"{np.median(n0):.0f}; (frazione < 2 %) da {min(n2)} a {max(n2)}, mediana {np.median(n2):.0f}; passaggi in "
              f"cui la testa spunta sopra il pannello (|x| < 0,4 m): {sp}, al più "
              f"{max(x['pixel_visibili_max_dietro_il_pannello'] for x in r)} pixel")
    for et in ("pannello_a12_alta185__s00", "pannello_a12_scuro__s00", "pannello_a12_nero__s00", "pannello_a12__s00"):
        for liv in ("nom", "lim"):
            r = [x for x in righe if x["nome"] == f"d435i_{liv}__{et}"]
            if r:
                print(f"d435i_{liv}__{et}: pixel visibili al massimo dietro il pannello "
                      f"{r[0]['pixel_visibili_max_dietro_il_pannello']}; quota di pixel validi sul soggetto intero "
                      f"{100 * r[0]['quota_validi_sul_soggetto_quando_intero']:.1f} %")


def scene_fisse():
    def ideale(et, scena, arg=None):
        spec = C._spec("x", "d435i", "nominale", scena, et, arg, n=1)
        return G.prepara(spec)[3]

    for et, d in (("sospeso_2p0m", 2.0), ("sospeso_2p8m", 2.8)):
        idl = ideale(et, "sospeso", {"distanza": d})
        q = quadri(f"d435i_nom__{et}")
        m = idl.obj == S.O_OSTACOLO0
        print(f"{et}: pixel ideali dell'ostacolo {int(m.sum())}; con un dato nel primo fotogramma {int((q[0][m] > 0).sum())}")
    for et, d in (("scatola15_0p8m", 0.8), ("scatola15_2p0m", 2.0)):
        idl = ideale(et, "scatola15", {"distanza": d})
        q = quadri(f"d435i_nom__{et}")
        m = idl.obj == S.O_OSTACOLO0
        print(f"{et}: pixel ideali della scatola {int(m.sum())}; con un dato nel primo fotogramma {int((q[0][m] > 0).sum())}")
    for modo in ("sfondo", "buco"):
        idl = ideale(f"vetro_{modo}", "vetro", {"modo": modo})
        q = quadri(f"d435i_nom__vetro_{modo}")
        print(f"vetro_{modo}: pixel visti attraverso la lastra {int(idl.vetro.sum())}; di questi con un dato "
              f"{100 * float((q[:, idl.vetro] > 0).mean()):.1f} % (profondità mediana {np.median(q[:, idl.vetro][q[:, idl.vetro] > 0]) / 1000 if (q[:, idl.vetro] > 0).any() else float('nan'):.2f} m: lo sfondo, la lastra è a 1,5 m)")
    for nome in ("d435i_nom__sensore_coperto", "d435i_nom__sensore_mezzo_coperto", "d435i_nom__azzeramento_progressivo"):
        q = quadri(nome)
        v = (q > 0).mean(axis=(1, 2))
        print(f"{nome}: {q.shape[0]} fotogrammi; quota di pixel validi: primo {100 * v[0]:.1f} %, minimo {100 * v.min():.1f} %, "
              f"ultimo {100 * v[-1]:.1f} %; fotogrammi tutti a zero {int((v == 0).sum())}; sotto il 50 % dal fotogramma "
              f"{int(np.argmax(v < 0.5 * v[0])) if (v < 0.5 * v[0]).any() else '—'}")
    for nome in ("d435i_nom__pavimento_vuoto", "d435i_lim__pavimento_vuoto", "d435i_nom__pavimento_lucido",
                 "d435i_lim__pavimento_lucido", "d455_nom__pavimento_vuoto", "g335_nom__pavimento_vuoto",
                 "d435i_nom__pavimento_vuoto__filtri"):
        spec = [s for s in C.catalogo() if s["nome"] == nome][0]
        prof, cam, sc, statica, _, _ = G.prepara(spec)
        q = quadri(nome).astype(np.float64) / 1000.0
        suolo = statica.obj == S.O_SUOLO
        vv, uu = np.where(suolo)
        _, _, zg = cam.al_suolo(uu.astype(float), vv.astype(float), statica.Z[vv, uu])
        riga = []
        for a, b in ((1.25, 2.0), (2.0, 3.0), (3.0, 4.0)):
            m = np.zeros(suolo.shape, dtype=bool)
            sel = (zg >= a) & (zg < b)
            m[vv[sel], uu[sel]] = True
            x = q[:, m]
            val = x > 0
            res = np.where(val, x - statica.Z[m][None, :], np.nan)
            lontano = np.nanmean(np.where(val, res > 0.10 * statica.Z[m][None, :], np.nan))
            riga.append(f"{a:g}–{b:g} m: validi {100 * val.mean():.1f} %, scarto tipo del residuo "
                        f"{1000 * np.nanstd(res):.0f} mm, oltre il suolo di più del 10 % {100 * lontano:.1f} %")
        print(f"{nome}: suolo per distanza a terra — " + "; ".join(riga))


if __name__ == "__main__":
    passaggi()
    scene_fisse()
