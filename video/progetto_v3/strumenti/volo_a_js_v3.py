#!/usr/bin/env python3
"""MoVi video v3: dai registri veri del volo (prototipo/uscite/video_volo/registro_F*.jsonl) a un JS compatto.
Non inventa niente: copia per fotogramma posizione, stato (vista/non vista), raggio dell'insieme di presenza,
verita' (solo per il montaggio), evento, affidabilita' dei sensori, avviso di prossimita'.
Uso: python3 -I strumenti/volo_a_js_v3.py  (dalla cartella progetto_v3). Scrive assets/data/volo_v3.js (file nuovo)."""
import json, os, sys

QUI = os.path.dirname(os.path.abspath(__file__))
P = os.path.dirname(QUI)
REG = os.path.normpath(os.path.join(P, "..", "..", "prototipo", "uscite", "video_volo"))
FIN = {"F1": (40.0, 92.0), "F3": (0.1, 45.0), "F4": (24.0, 60.0), "F5": (34.0, 52.0)}
OUT = os.path.join(P, "assets", "data", "volo_v3.js")
if os.path.exists(OUT):
    print("esiste gia':", OUT, "(nome nuovo, niente sovrascritture)"); sys.exit(3)

r1 = lambda x: round(x, 1)
dati = {}
for sc, (t0, t1) in FIN.items():
    righe = [json.loads(l) for l in open(os.path.join(REG, f"registro_{sc}.jsonl"), encoding="utf-8")]
    intest = righe[0]["intestazione"]
    fot = []
    for r in righe[1:]:
        if r["t"] < t0 - 1e-9 or r["t"] > t1 + 1e-9:
            continue
        tr = []
        for k in r["tracce"]:
            x, y, z = k["pos"]
            tr.append([k["id"], r1(x), r1(y), r1(z), round(k["non_vista_da_s"], 2),
                       1 if k["parola"] == "vista" else 0, r1(k["insieme_presenza_r_m"])])
        ev = r.get("evento")
        if ev:
            ev = {"tipo": ev.get("tipo"), "t": ev.get("t_dichiarato"),
                  "rV": ev.get("volume_V", {}).get("r_pianta_m"), "zmin": ev.get("volume_V", {}).get("z_min_m"),
                  "zmax": ev.get("volume_V", {}).get("z_max_m"), "R": ev.get("impronta", {}).get("R_m"),
                  "c": ev.get("impronta", {}).get("centro")}
        fot.append({"t": r["t"], "tr": tr, "v": {k: [r1(a) for a in v] for k, v in r["verita"].items()},
                    "ev": ev, "af": {k.split("#")[0]: (0 if "persa" in v else 1) for k, v in r["affidabilita_sensori"].items()},
                    "fr": r.get("frammenti_veri_in_aria", 0), "ap": r.get("avviso_prossimita")})
    dati[sc] = {"nome": intest["nome"], "configurazione": intest["configurazione"], "stato": intest["stato"],
                "riassunto": intest["riassunto"], "fotogrammi": fot,
                "fonte": f"prototipo/uscite/video_volo/registro_{sc}.jsonl"}
    print(sc, len(fot), "fotogrammi", t0, "->", t1)
with open(OUT, "w", encoding="utf-8") as f:
    f.write("/* GENERATO da strumenti/volo_a_js_v3.py dai registri veri (simulati) di prototipo/uscite/video_volo. */\n")
    f.write("window.__VOLO = " + json.dumps(dati, ensure_ascii=False, separators=(",", ":")) + ";\n")
print("scritto", OUT, os.path.getsize(OUT), "byte")
