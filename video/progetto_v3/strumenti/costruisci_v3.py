#!/usr/bin/env python3
"""MoVi video v3: scene, tempi e sottotitoli dalla voce misurata (<voce>.wav.tempi.json di kokoro_tts.py).
Uso (da progetto_v3): python3 -I strumenti/costruisci_v3.py <voce.wav> <uscita_tempi.js>
Una scena per paragrafo della voce (pausa fra frasi > 0,6 s = paragrafo nuovo). Durata scena = anticipo + voce + coda."""
import json, sys, os

voce, out = sys.argv[1], sys.argv[2]
if os.path.exists(out):
    print("esiste gia':", out); sys.exit(3)
cf = json.load(open("cifre.json", encoding="utf-8"))
fr = json.load(open(voce + ".tempi.json", encoding="utf-8"))
par, cur, prev = [], [], None
for x in fr:
    if prev is not None and x["inizio"] - prev > 0.6:
        par.append(cur); cur = []
    cur.append(x); prev = x["fine"]
par.append(cur)
assert len(par) == 10, f"attesi 10 paragrafi, trovati {len(par)}"

S = lambda k: cf[k]["testo_schermo"]
AMB, COR, GR = "#F5A524", "#FF6B6B", "#AEB8C5"
scene = [
 dict(id="s1", tipo="dati", registro="F3", onesta="sim", titolo="Two fast drones, then contact", anticipo=3.0, coda=0.6, titolone=3.0,
      cfg=dict(t0=14.0, t1=28.0, bbxy=[-800, -700, 550, 120], bbxz=[-800, 0, 550, 170], scala=[200, "200 m"])),
 dict(id="s2", tipo="tre", onesta="schema", titolo="Three answers per track", anticipo=0.5, coda=0.8),
 dict(id="s3", tipo="dati", registro="F1", onesta="sim", titolo="F1 · aircraft on approach, non-cooperative drone", anticipo=0.5, coda=0.6,
      cfg=dict(t0=44.0, t1=88.0, bbxy=[-6100, -400, -1900, 900], bbxz=[-6100, 0, -1900, 420], scala=[1000, "1 km"]),
      contatore=[dict(s=S("F1-AVVISO"), da=3.0, size=24), dict(s=S("V-1"), da=8.0, size=24), dict(s=S("V-7"), da=11.0, size=22, c=GR)]),
 dict(id="s4", tipo="dati", registro="F4", onesta="sim", titolo="F4 · engine failure with low-energy debris, 135 m/s", anticipo=0.5, coda=0.6,
      cfg=dict(t0=27.0, t1=55.0, bbxy=[3200, -900, 7700, 900], bbxz=[3200, 0, 7700, 650], scala=[1000, "1 km"]),
      contatore=[dict(s=S("V-2"), da=7.0, size=24), dict(s=S("V-3"), da=15.0, size=24), dict(s=S("V-4") , da=19.0, size=20, c=GR)]),
 dict(id="s5", tipo="dati", registro="F3", onesta="sim", titolo="F3 · fast drones colliding at 40 and 35 m/s", anticipo=0.5, coda=0.6,
      cfg=dict(t0=0.5, t1=42.0, bbxy=[-800, -700, 550, 120], bbxz=[-800, 0, 550, 170], scala=[200, "200 m"],
               extra=[dict(s="collision not yet recognised as an event:", treg=23.6, c=AMB), dict(s="region kept", treg=23.6, c=AMB)]),
      contatore=[dict(s=S("V-5"), da=3.0, size=24), dict(s=S("V-6"), da=11.0, size=24), dict(s=S("V-11"), da=13.0, size=24, c=COR)]),
 dict(id="s6", tipo="dati", registro="F5", onesta="sim", titolo="F5 · a flash blinds every optical sensor for 3 s", anticipo=0.5, coda=0.6,
      cfg=dict(t0=37.5, t1=46.0, bbxy=[-600, -450, 1100, 600], bbxz=[-600, 0, 1100, 650], scala=[200, "200 m"],
               extra=[dict(s="RADAR ONLY · identity PRESUMED", treg=39.4, c=AMB)]),
      contatore=[dict(s=S("V-10"), da=2.5, size=24)]),
 dict(id="s7", tipo="curva", onesta="computed in the model · checked on ADS-B with a simulated sensor", titolo="When continuity is lost: confidence over time", anticipo=0.5, coda=1.0),
 dict(id="s8", tipo="barre", onesta="estimates by analogy, no measurement", titolo="Sensors and dedicated hardware: latency", anticipo=0.5, coda=0.8),
 dict(id="s9", tipo="schede", onesta="schema", titolo="Also: the site with taxiing aircraft and drones, and other uses", anticipo=0.5, coda=0.8),
 dict(id="s10", tipo="chiusura", onesta="schema", titolo="Limits, and what comes next", anticipo=0.5, coda=1.2),
]
t, sotto, tempi = 0.0, [], []
for sc, p in zip(scene, par):
    v0, v1 = p[0]["inizio"], p[-1]["fine"]
    sc["inizio"] = round(t, 3)
    sc["voce_da"] = sc["anticipo"]
    sc["durata"] = round(sc["anticipo"] + (v1 - v0) + sc["coda"], 3)
    if sc["id"] == "s10":
        sc["durata"] = round(max(sc["durata"], sc["anticipo"] + (v1 - v0) + 1.2), 3)
    if "cfg" in sc:
        sc["cfg"]["vel"] = (sc["cfg"]["t1"] - sc["cfg"]["t0"]) / sc["durata"]
    for x in p:
        sotto.append(dict(a=round(t + sc["anticipo"] + x["inizio"] - v0, 3), b=round(t + sc["anticipo"] + x["fine"] - v0 + 0.25, 3), s=x["testo"]))
    tempi.append(dict(id=sc["id"], inizio=sc["inizio"], durata=sc["durata"], voce_da=sc["voce_da"], voce_wav_da=v0, voce_wav_a=v1))
    t += sc["durata"]
tot = round(t, 3)
with open(out, "w", encoding="utf-8") as f:
    f.write(f"/* GENERATO da strumenti/costruisci_v3.py dalla voce {voce} */\n")
    f.write("window.__SCENE_V3 = " + json.dumps(scene, ensure_ascii=False) + ";\n")
    f.write("window.__SOTTO = " + json.dumps(sotto, ensure_ascii=False) + ";\n")
    f.write(f"window.__DURATA_V3 = {tot};\n")
json.dump(dict(voce=voce, totale=tot, scene=tempi), open(out.replace(".js", ".json"), "w"), indent=1)
# sottotitoli SRT
def ts(x):
    h, m = int(x // 3600), int(x % 3600 // 60); s = x % 60
    return f"{h:02d}:{m:02d}:{int(s):02d},{int(round((s - int(s)) * 1000)):03d}"
with open(out.replace(".js", ".srt"), "w", encoding="utf-8") as f:
    for i, q in enumerate(sotto, 1):
        f.write(f"{i}\n{ts(q['a'])} --> {ts(min(q['b'], tot))}\n{q['s']}\n\n")
for x in tempi: print(x["id"], x["inizio"], x["durata"])
print("TOTALE", tot)
