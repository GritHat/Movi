#!/usr/bin/env python3
"""MoVi video v3b (correzioni QA_V3/GIURATO_V3; copia di costruisci_finale.py, che resta): sigle interne tolte dalle righe a schermo.
MoVi video v3 FINALE: scene, tempi e sottotitoli dalla voce misurata (<voce>.wav.tempi.json di kokoro_tts.py).
Derivato da costruisci_v3.py (che resta). Ordine voluto dall'utente: s1..s7 (volo veloce, curva) -> s8 F7 «scorta»
(scena chiave) -> s9 sito e altri usi -> s10 limiti e titoli. Cifre a schermo SOLO da cifre_finale.json.
Uso (da progetto_v3): python3 -I strumenti/costruisci_finale.py <voce.wav> <uscita_tempi.js> [--max 176.0]
Si ferma (codice 4) se la durata totale supera --max: si taglia testo, mai si accelera la voce."""
import json, sys, os

voce, out = sys.argv[1], sys.argv[2]
MAX = float(sys.argv[sys.argv.index("--max") + 1]) if "--max" in sys.argv else 176.0
if os.path.exists(out): print("esiste gia':", out); sys.exit(3)
cf = json.load(open("cifre_finale.json", encoding="utf-8"))
fr = json.load(open(voce + ".tempi.json", encoding="utf-8"))
par, cur, prev = [], [], None
for x in fr:
    if prev is not None and x["inizio"] - prev > 0.6: par.append(cur); cur = []
    cur.append(x); prev = x["fine"]
par.append(cur)
assert len(par) == 10, f"attesi 10 paragrafi, trovati {len(par)}"
S = lambda k: cf[k]["testo_schermo"].replace("limit · forward-only radar:", "limit · with a forward-only radar instead:")
AMB, COR, GR = "#F5A524", "#FF6B6B", "#AEB8C5"
# voce: istante (dall'inizio del paragrafo) di ogni frase, per agganciare i contatori alla voce
def frase(n, k): return par[n][k]["inizio"] - par[n][0]["inizio"]
scene = [
 dict(id="s1", tipo="dati", registro="F3", onesta="sim", titolo="Fast drones on a collision course", anticipo=3.0, coda=0.6, titolone=3.0,
      cfg=dict(t0=14.0, t1=28.0, bbxy=[-800, -700, 550, 120], bbxz=[-800, 0, 550, 170], scala=[200, "200 m"])),
 dict(id="s2", tipo="tre", onesta="schema", titolo="Three answers per track", anticipo=0.5, coda=0.8),
 dict(id="s3", tipo="dati", registro="F1", onesta="sim", titolo="F1 · aircraft on approach, non-cooperative drone", anticipo=0.5, coda=1.0,
      cfg=dict(t0=44.0, t1=88.0, bbxy=[-6100, -400, -1900, 900], bbxz=[-6100, 0, -1900, 420], scala=[1000, "1 km"]),
      contatore=[dict(s=S("V-1"), da=1.5)]),
 dict(id="s4", tipo="dati", registro="F4", onesta="sim", titolo="F4 · failure with low-energy debris, 135 m/s", anticipo=0.5, coda=0.8,
      cfg=dict(t0=27.0, t1=55.0, bbxy=[3200, -900, 7700, 900], bbxz=[3200, 0, 7700, 650], scala=[1000, "1 km"]),
      contatore=[dict(s=S("V-2"), da=0.5 + frase(3, 1)), dict(s=S("V-3"), da=0.5 + frase(3, 2))]),
 dict(id="s5", tipo="dati", registro="F3", onesta="sim", titolo="F3 · fast drones colliding at 40 and 35 m/s", anticipo=0.5, coda=0.8,
      cfg=dict(t0=0.5, t1=42.0, bbxy=[-800, -700, 550, 120], bbxz=[-800, 0, 550, 170], scala=[200, "200 m"],
               extra=[dict(s="collision not yet declared as an event:", treg=23.6, c=AMB), dict(s="region kept", treg=23.6, c=AMB)]),
      contatore=[dict(s=S("V-5"), da=0.5 + frase(4, 1)), dict(s=S("V-6"), da=0.5 + frase(4, 2)),
                 dict(s=S("V-11-PROVA"), da=0.5 + frase(4, 2) + 3.0, c=GR, size=20)]),
 dict(id="s6", tipo="dati", registro="F5", onesta="sim", titolo="F5 · a flash blinds every optical sensor", anticipo=0.5, coda=1.0,
      cfg=dict(t0=37.5, t1=46.0, bbxy=[-600, -450, 1100, 600], bbxz=[-600, 0, 1100, 650], scala=[200, "200 m"],
               extra=[dict(s="RADAR ONLY · identity PRESUMED", treg=39.4, c=AMB)]),
      contatore=[dict(s=S("V-10"), da=2.0)]),
 dict(id="s7", tipo="curva", onesta="SCHEMATIC + PUBLIC TRAJECTORIES|curve computed in the model · points: public flight tracks, simulated sensor",
      titolo="When continuity is lost: confidence over time", anticipo=0.8, coda=1.2,
      contatore=[dict(s=S("C-TAR-VIRATA"), da=0.8 + frase(6, 2), c=COR)]),
 dict(id="s8", tipo="scorta", onesta="sim", titolo="F7 · on board a moving drone: a collision nearby", anticipo=1.5, coda=2.0),
 dict(id="s9", tipo="schede", onesta="SIMULATION (site) · SCHEMATIC (short range)|Simulated · state-of-the-art sensor parameters assumed · no physical sensor",
      titolo="Also: the site with taxiing aircraft and drones, and other uses", anticipo=0.5, coda=0.8),
 dict(id="s10", tipo="chiusura", onesta="SCHEMATIC · ESTIMATE|limits from the verdicts · hardware figure is an estimate by analogy",
      titolo="Limits, and what comes next", anticipo=0.5, coda=3.4),
]
# F7: tempo di scena -> tempo del registro (lineare a tratti): urto (5,9 s) sulla frase «Nearby, two drones collide»,
# perdita e riacquisizione rallentate sotto la frase sulla regione. La velocita' di riproduzione e' scritta a schermo.
sc8 = scene[7]; a8 = sc8["anticipo"]; d8 = a8 + (par[7][-1]["fine"] - par[7][0]["inizio"]) + sc8["coda"]
tc = a8 + frase(7, 1) + 0.4
sc8["cfg"] = dict(mappa=[[0.0, 2.6], [tc, 5.9], [a8 + frase(7, 3) + 3.0, 8.6], [d8, 13.0]])
sc8["contatore"] = [dict(s=S("F7-CAM"), da=a8 + frase(7, 2), a=a8 + frase(7, 3) - 0.2, size=20),
                    dict(s=S("F7-VOL"), da=a8 + frase(7, 2) + 1.0, a=a8 + frase(7, 3) - 0.2, size=20),
                    dict(s=S("F7-CONT"), da=a8 + frase(7, 3)), dict(s=S("F7-LIBERO"), da=a8 + frase(7, 3) + 4.0),
                    dict(s=S("F7-ID"), da=a8 + frase(7, 3) + 6.0, a=a8 + frase(7, 4) - 0.2, size=20, c=GR),
                    dict(s=S("F7R-CIECO"), da=a8 + frase(7, 4), size=20, c=AMB),
                    dict(s=S("F7-LIM-FRONTALE"), da=a8 + frase(7, 4) + 4.0, size=18, c=COR)]
t, sotto, tempi = 0.0, [], []
for sc, p in zip(scene, par):
    v0, v1 = p[0]["inizio"], p[-1]["fine"]
    sc["inizio"] = round(t, 3); sc["voce_da"] = sc["anticipo"]
    sc["durata"] = round(sc["anticipo"] + (v1 - v0) + sc["coda"], 3)
    if "cfg" in sc and "t1" in sc["cfg"]: sc["cfg"]["vel"] = (sc["cfg"]["t1"] - sc["cfg"]["t0"]) / sc["durata"]
    for x in p:
        sotto.append(dict(a=round(t + sc["anticipo"] + x["inizio"] - v0, 3), b=round(t + sc["anticipo"] + x["fine"] - v0 + 0.25, 3), s=x["testo"]))
    tempi.append(dict(id=sc["id"], inizio=sc["inizio"], durata=sc["durata"], voce_da=sc["voce_da"], voce_wav_da=v0, voce_wav_a=v1))
    t += sc["durata"]
tot = round(t, 3)
for x in tempi: print(x["id"], x["inizio"], x["durata"])
print("TOTALE", tot)
if tot > MAX: print(f"DURATA {tot} s OLTRE {MAX} s: tagliare testo o scene (mai accelerare la voce)"); sys.exit(4)
with open(out, "w", encoding="utf-8") as f:
    f.write(f"/* GENERATO da strumenti/costruisci_finale.py dalla voce {voce} */\n")
    f.write("window.__SCENE_V3 = " + json.dumps(scene, ensure_ascii=False) + ";\n")
    f.write("window.__SOTTO = " + json.dumps(sotto, ensure_ascii=False) + ";\n")
    f.write(f"window.__DURATA_V3 = {tot};\n")
json.dump(dict(voce=voce, totale=tot, scene=tempi), open(out.replace(".js", ".json"), "w"), indent=1)
def ts(x):
    h, m = int(x // 3600), int(x % 3600 // 60); s = x % 60; ms = int(round((s - int(s)) * 1000))
    if ms == 1000: ms = 999
    return f"{h:02d}:{m:02d}:{int(s):02d},{ms:03d}"
with open(out.replace(".js", ".srt"), "w", encoding="utf-8") as f:
    for i, q in enumerate(sotto, 1):
        f.write(f"{i}\n{ts(q['a'])} --> {ts(min(q['b'], tot))}\n{q['s']}\n\n")
