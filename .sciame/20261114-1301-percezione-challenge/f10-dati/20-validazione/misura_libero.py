#!/usr/bin/env python3
"""Misura 1 — «libero» contro la verità del simulatore (K-014), celle per stato, copertura del suolo, falsi occupati.

Legge uscite/<etichetta>/<sequenza>/griglie.npz e fotogrammi.jsonl (uscite della catena) e verita.json (simulatore).
Scrive uscite/<etichetta>/misura_libero.json e stampa una tabella. Uso: <python> -I -B misura_libero.py [etichetta]"""
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comune as K                                             # noqa: E402
import numpy as np                                             # noqa: E402


def distanza_da_poligono(x, z, vertici):
    """Distanza (matrici x, z) dal bordo o dall'interno di un poligono convesso dato per vertici [x, z]."""
    v = np.asarray(vertici, dtype=float)
    d = np.full(x.shape, np.inf)
    dentro = np.ones(x.shape, dtype=bool)
    segno = None
    for i in range(len(v)):
        a, b = v[i], v[(i + 1) % len(v)]
        ab = b - a
        t = np.clip(((x - a[0]) * ab[0] + (z - a[1]) * ab[1]) / float(ab @ ab), 0, 1)
        d = np.minimum(d, np.hypot(x - a[0] - t * ab[0], z - a[1] - t * ab[1]))
        cr = ab[0] * (z - a[1]) - ab[1] * (x - a[0])
        s = cr >= 0
        segno = s if segno is None else segno
        dentro &= (s == segno)
    return np.where(dentro, 0.0, d)


def misura(nome, radice):
    usc = os.path.join(radice, nome)
    g = K.leggi_griglie(usc)
    stati = g["stati"]                                          # (T, 180, 30)
    ver = K.leggi_verita(os.path.join(K.SEQ_SIM, nome))
    righe = K.leggi_righe(usc)
    centro, tutta, parte, _ = K.classi_polari(ver)
    bordo = parte & ~tutta
    T = stati.shape[0]
    lib = stati == K.LIBERO
    occ = stati == K.OCCUPATO
    az = np.radians(-89.5 + np.arange(180))[:, None]
    rr = (np.arange(30) + 0.5)[None, :] * 0.1
    gx, gz = np.sin(az) * rr, np.cos(az) * rr
    # distanza di ogni cella dall'ostacolo fisso più vicino
    d_ost = np.full(gx.shape, np.inf)
    for o in ver.get("ostacoli", []):
        if o.get("tipo") == "poligono" and o.get("genere", o.get("id")) not in ("parete", "stanza") \
                and not str(o.get("id", "")).startswith("parete"):
            d_ost = np.minimum(d_ost, distanza_da_poligono(gx, gz, o["vertici"]))
    falsi_occ = 0
    libero_su_persona = 0          # fotogrammi con la cella del centro vero «libero» e il soggetto visibile
    libero_su_nascosto = 0
    for k, f in enumerate(ver["fotogrammi"][:T]):
        vicino = d_ost <= 0.15
        for s in f["soggetti"]:
            vicino = vicino | (np.hypot(gx - s["x"], gz - s["z"]) <= s.get("raggio_m", 0.2) + 0.15)
            c = K.cella(s["x"], s["z"])
            if c is not None and lib[k][c]:
                if s["frazione_visibile"] >= 0.02:
                    libero_su_persona += 1
                else:
                    libero_su_nascosto += 1
        falsi_occ += int((occ[k] & ~vicino).sum())
    vis = centro == 0
    fasce = {"1,3-2 m": (13, 20), "2-3 m": (20, 30)}
    cop = {}
    for nome_f, (a, b) in fasce.items():
        m = vis[:, a:b] & ~parte[:, a:b]
        n = int(m.sum())
        cop[nome_f] = {"celle_visibili": n,
                       "quota_libero": float(lib[:, :, a:b][:, m].mean()) if n else None,
                       "quota_occupato": float(occ[:, :, a:b][:, m].mean()) if n else None}
    conf = set()
    for r in righe:
        for tr in r["tracce"]:
            if tr["stato"] != "in_conferma":
                conf.add(tr["id"])
    cs = np.array([[r["celle"][n] for n in ("non_osservato", "libero", "occupato", "in_ombra")] for r in righe])
    return {
        "nome": nome, "fotogrammi": T,
        "celle_medie": {n: float(v) for n, v in zip(("non_osservato", "libero", "occupato", "in_ombra"), cs.mean(0))},
        "libero_min_max": [int(cs[:, 1].min()), int(cs[:, 1].max())],
        "celle_tutte_in_ombra": int(tutta.sum()), "celle_di_bordo": int(bordo.sum()),
        "libero_tutta_ombra": int(lib[:, tutta].sum()),
        "libero_bordo": int(lib[:, bordo].sum()),
        "libero_classe4_centro": int(lib[:, (centro == 4) & ~parte].sum()), "celle_classe4": int(((centro == 4) & ~parte).sum()),
        "libero_classe2_centro": int(lib[:, (centro == 2) & ~parte].sum()),
        "falsi_occupati_celle_fotogramma": falsi_occ,
        "celle_ambigue_medie": float(np.mean([r["celle_ambigue"] for r in righe])),
        "copertura": cop, "tracce_confermate": len(conf),
        "libero_su_persona_visibile": libero_su_persona, "libero_su_persona_nascosta": libero_su_nascosto,
    }


def main():
    et = sys.argv[1] if len(sys.argv) > 1 else "sim"
    radice = os.path.join(K.USCITE, et)
    nomi = sorted(n for n in os.listdir(radice) if os.path.isdir(os.path.join(radice, n)))
    tutti = [misura(n, radice) for n in nomi]
    with open(os.path.join(radice, "misura_libero.json"), "w", encoding="utf-8") as f:
        json.dump(tutti, f, ensure_ascii=False, indent=1)

    def gruppo(n):
        base = n.split("__")
        scena = base[1]
        return base[0] + "__" + scena + ("__filtri" if n.endswith("__filtri") else "")
    gruppi = {}
    for m in tutti:
        gruppi.setdefault(gruppo(m["nome"]), []).append(m)
    print("gruppo; N sequenze; fotogrammi; libero medio; occupato medio; in ombra medio; non oss. medio; "
          "LIBERO tutta-ombra (celle·fot) [sequenze con ≥1]; libero bordo / celle·fot di bordo; libero classe 4; "
          "libero classe 2; falsi occupati celle·fot [per fot]; tracce confermate (min–max); copertura 1,3–2; 2–3; "
          "occupato su suolo 2–3")
    for gname, ms in sorted(gruppi.items()):
        T = sum(m["fotogrammi"] for m in ms)
        med = lambda k: np.mean([m["celle_medie"][k] for m in ms])                         # noqa: E731
        lt = sum(m["libero_tutta_ombra"] for m in ms)
        nlt = sum(1 for m in ms if m["libero_tutta_ombra"] > 0)
        lb = sum(m["libero_bordo"] for m in ms)
        nb = sum(m["celle_di_bordo"] * m["fotogrammi"] for m in ms)
        l4 = sum(m["libero_classe4_centro"] for m in ms)
        l2 = sum(m["libero_classe2_centro"] for m in ms)
        fo = sum(m["falsi_occupati_celle_fotogramma"] for m in ms)
        tc = [m["tracce_confermate"] for m in ms]
        c1 = [m["copertura"]["1,3-2 m"]["quota_libero"] for m in ms if m["copertura"]["1,3-2 m"]["quota_libero"] is not None]
        c2 = [m["copertura"]["2-3 m"]["quota_libero"] for m in ms if m["copertura"]["2-3 m"]["quota_libero"] is not None]
        o2 = [m["copertura"]["2-3 m"]["quota_occupato"] for m in ms if m["copertura"]["2-3 m"]["quota_occupato"] is not None]
        f = lambda v: f"{100 * np.mean(v):.1f} %" if v else "—"                            # noqa: E731
        print(f"{gname}; {len(ms)}; {T}; {med('libero'):.0f}; {med('occupato'):.1f}; {med('in_ombra'):.0f}; "
              f"{med('non_osservato'):.0f}; {lt} [{nlt}]; {lb} / {nb}; {l4}; {l2}; {fo} [{fo / T:.2f}]; "
              f"{min(tc)}–{max(tc)}; {f(c1)}; {f(c2)}; {f(o2)}")
    sp = sum(m["libero_su_persona_visibile"] for m in tutti)
    sn = sum(m["libero_su_persona_nascosta"] for m in tutti)
    print(f"cella del centro vero «libero»: {sp} fotogrammi a soggetto visibile, {sn} a soggetto nascosto "
          f"(su {sum(m['fotogrammi'] for m in tutti)} fotogrammi)")
    for m in tutti:
        if m["libero_su_persona_visibile"] or m["libero_su_persona_nascosta"]:
            print("   ", m["nome"], m["libero_su_persona_visibile"], m["libero_su_persona_nascosta"])


if __name__ == "__main__":
    main()
