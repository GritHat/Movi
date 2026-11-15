#!/usr/bin/env python3
"""MoVi video v3 finale: dai registri veri (simulati) di prototipo/uscite/video_volo a assets/data/volo_finale.js.
F1, F3, F4, F5 come volo_a_js_v3.py (che resta); in piu' F7 «scorta» dal registro registro_F7r_davanti.jsonl
(radar accecato fino a 2 s, modello pessimista; 0 violazioni del validatore convalida_volo.py), e le curve tarate
(f20-chiusura/02-taratura/curva_video.json) e F7 (f20-chiusura/05-scorta/curva_F7.json) copiate senza modifiche.
Non inventa niente. Non sovrascrive. Uso (da progetto_v3): python3 -I strumenti/volo_finale.py"""
import json, os, sys

QUI = os.path.dirname(os.path.abspath(__file__)); P = os.path.dirname(QUI)
REG = os.path.normpath(os.path.join(P, "..", "..", "prototipo", "uscite", "video_volo"))
F20 = os.path.normpath(os.path.join(P, "..", "..", ".sciame", "20261114-1301-percezione-challenge", "f20-chiusura"))
FIN = {"F1": (40.0, 92.0), "F3": (0.1, 45.0), "F4": (24.0, 60.0), "F5": (34.0, 52.0)}
F7 = "registro_F7r_davanti.jsonl"
OUT = os.path.join(P, "assets", "data", "volo_finale.js")
if os.path.exists(OUT): sys.exit(f"esiste gia': {OUT}")
r1 = lambda x: round(x, 1)
dati = {}
for sc, (t0, t1) in FIN.items():
    righe = [json.loads(l) for l in open(os.path.join(REG, f"registro_{sc}.jsonl"), encoding="utf-8")]
    intest = righe[0]["intestazione"]; fot = []
    for r in righe[1:]:
        if r["t"] < t0 - 1e-9 or r["t"] > t1 + 1e-9: continue
        tr = [[k["id"], r1(k["pos"][0]), r1(k["pos"][1]), r1(k["pos"][2]), round(k["non_vista_da_s"], 2),
               1 if k["parola"] == "vista" else 0, r1(k["insieme_presenza_r_m"])] for k in r["tracce"]]
        ev = r.get("evento")
        if ev:
            ev = {"tipo": ev.get("tipo"), "t": ev.get("t_dichiarato"), "rV": ev.get("volume_V", {}).get("r_pianta_m"),
                  "zmin": ev.get("volume_V", {}).get("z_min_m"), "zmax": ev.get("volume_V", {}).get("z_max_m"),
                  "R": ev.get("impronta", {}).get("R_m"), "c": ev.get("impronta", {}).get("centro")}
        fot.append({"t": r["t"], "tr": tr, "v": {k: [r1(a) for a in v] for k, v in r["verita"].items()}, "ev": ev,
                    "af": {k.split("#")[0]: (0 if "persa" in v else 1) for k, v in r["affidabilita_sensori"].items()},
                    "fr": r.get("frammenti_veri_in_aria", 0), "ap": r.get("avviso_prossimita")})
    dati[sc] = {"nome": intest["nome"], "stato": intest["stato"], "fotogrammi": fot, "fonte": f"prototipo/uscite/video_volo/registro_{sc}.jsonl"}
    print(sc, len(fot), "fotogrammi")
# F7r davanti: coordinate assolute; il motore le porta nel riferimento del portatore con la posa STIMATA
righe = [json.loads(l) for l in open(os.path.join(REG, F7), encoding="utf-8")]
intest = righe[0]["intestazione"]; fot = []
RU = {"bersaglio": "b", "frammento_possibile": "f", "non_classificata": "n"}
for r in righe[1:]:
    tr = [[k["id"], RU.get(k["ruolo"], "n"), r1(k["pos"][0]), r1(k["pos"][1]), r1(k["pos"][2]), round(k["non_vista_da_s"], 2),
           1 if k["parola"] == "vista" else 0, r1(k["insieme_presenza_r_m"]), k.get("identita"), k.get("confidenza_C")] for k in r["tracce"]]
    ev = r.get("evento")
    if ev: ev = {"a": [r1(x) for x in ev["volume"]["apice"]], "r": r1(ev["volume"]["raggio_m"]), "parola": ev["parola"]}
    fot.append({"t": r["t"], "tr": tr, "v": {k: [r1(a) for a in v] for k, v in r["verita"].items()}, "ev": ev,
                "af": r["affidabilita_sensori"], "fr": r.get("frammenti_veri_in_aria", 0), "ap": r.get("avviso_portatore"),
                "pz": [r1(x) for x in r["posa_stimata"]]})
dati["F7"] = {"nome": intest["scenario"], "stato": intest["stato"], "configurazione": intest["configurazione"],
              "riassunto": intest["riassunto"], "fotogrammi": fot, "fonte": "prototipo/uscite/video_volo/" + F7}
print("F7", len(fot), "fotogrammi")
cv = json.load(open(os.path.join(F20, "02-taratura", "curva_video.json"), encoding="utf-8"))
c7 = json.load(open(os.path.join(F20, "05-scorta", "curva_F7.json"), encoding="utf-8"))
with open(OUT, "w", encoding="utf-8") as f:
    f.write("/* GENERATO da strumenti/volo_finale.py dai registri veri (simulati) e dalle curve del verdetto finale. */\n")
    f.write("window.__VOLO = " + json.dumps(dati, ensure_ascii=False, separators=(",", ":")) + ";\n")
    f.write("window.__CURVA = " + json.dumps(cv["mezzi"]["aereo_210"], ensure_ascii=False, separators=(",", ":")) + ";\n")
    f.write("window.__CURVA_F7 = " + json.dumps(c7["perdita_totale"], ensure_ascii=False, separators=(",", ":")) + ";\n")
print("scritto", OUT, os.path.getsize(OUT))
