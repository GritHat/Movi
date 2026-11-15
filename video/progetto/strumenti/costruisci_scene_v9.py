#!/usr/bin/env python3
"""v9 (montaggio finale): scrive scene/scene_v9_<lingua>.json dai tempi della voce (.tempi.json, campo «scena»).
Durata di ogni scena = max(durata minima d'immagine, voce_da + voce del paragrafo + coda). Gli istanti («cue») e i
tratti dei registri sono legati alle FRASI della voce (inizio della frase i-esima del paragrafo), così che il cambio di
stato del registro cada sulla frase che lo cita. Le regole di aggancio sono scritte qui sotto, scena per scena, e
valgono per ogni lingua che ha lo stesso numero di frasi per paragrafo (lo si controlla).
Uso: python3 -I strumenti/costruisci_scene_v9.py VOCE.wav LINGUA [durate_minime_csv]
"""
import json, os, sys

QUI = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(QUI)
voce, L = sys.argv[1], sys.argv[2]
MIN = [float(x) for x in (sys.argv[3] if len(sys.argv) > 3 else "13.5,23.5,14,18.5,20.5,21.5,35.5,10,13.5").split(",")]
FRASI = [3, 6, 2, 3, 4, 4, 7, 1, 5]
CODA = [0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 1.0]
VD = [0.15, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.6]
T = json.load(open(voce + ".tempi.json", encoding="utf-8"))
P = {n: [x for x in T if x["scena"] == n] for n in range(1, 10)}
for n in range(1, 10):
    assert len(P[n]) == FRASI[n - 1], f"scena {n}: {len(P[n])} frasi, attese {FRASI[n - 1]}"
dur, f = [], {}
for n in range(1, 10):
    q = P[n]; vd = VD[n - 1]
    f[n] = [round(vd + x["inizio"] - q[0]["inizio"], 2) for x in q]          # inizio di ogni frase, s di scena
    fe = [round(vd + x["fine"] - q[0]["inizio"], 2) for x in q]
    f[(n, "fine")] = fe
    dur.append(round(max(MIN[n - 1], fe[-1] + CODA[n - 1]), 2))
D = dict(zip(range(1, 10), dur))
REG = {
    "A1v3": {"file": "../../prototipo/uscite/video/lp_A1_v3/registro.jsonl", "stato": "definitivo", "fonte": "VERDETTO_2C §5: Simulation"},
    "E3v3": {"file": "../../prototipo/uscite/video/lp_E3_v3/registro.jsonl", "stato": "definitivo", "fonte": "VERDETTO_2C §5: Simulation"},
    "E1v3": {"file": "../../prototipo/uscite/video/lp_E1_v3/registro.jsonl", "stato": "definitivo", "fonte": "VERDETTO_2C §5: Simulation per evento e avviso; zona dei detriti Schematic"},
    "E2v3": {"file": "../../prototipo/uscite/video/lp_E2_v3/registro.jsonl", "stato": "definitivo", "fonte": "VERDETTO_2C §5: Simulation solo per le camere non affidabili; detriti e avviso al mezzo Schematic"},
    "Rc9": {"file": "../../prototipo/uscite/resta_dietro/registro.jsonl", "stato": "provvisorio", "etichetta_sensore": "SIMULATED DEPTH CAMERA" if L == "en" else "CAMERA DI PROFONDITÀ SIMULATA", "fonte": "corto raggio, come nell'animatic"},
}
# scena 5: il fotogramma dell'evento (t = 17,5 s nel registro) cade 0,6 s dopo l'inizio della frase 2 («MoVi infers contact…»)
ev5 = f[5][1] + 0.6; t5 = round(17.5 - ev5, 2)
# scena 6: il primo fotogramma con le camere non affidabili (t = 16,0 s) cade 0,3 s prima della fine della frase 1 («…with a flash»)
fl6 = round(f[(6, "fine")][0] - 0.3, 2); t6 = round(16.0 - fl6, 2)
S = {
 "nota": "v9 (montaggio finale, 2026-11-15) generato da strumenti/costruisci_scene_v9.py dalla voce " + os.path.relpath(voce, R) + ". 'onesta' = etichetta per tutta la scena (sim | schema), dal VERDETTO_2C §5.",
 "fps": 30, "lingua": L, "registri": REG,
 "scene": [
  {"n": 1, "id": "s1", "durata": D[1], "tipo": "dati", "onesta": "sim", "vista": [-250, -100, 850, 615],
   "segmenti": [{"da": 0, "a": 3.0, "registro": "A1v3", "t_reg": 0.0, "velocita": 1}, {"da": 3.0, "a": D[1], "registro": "A1v3", "t_reg": 3.0, "velocita": 5}],
   "dominio": "domain.s1", "camera": [{"t": 0, "vista": [-250, -100, 850, 615]}], "voce_da": VD[0], "cue": {"conf": f[1][1] + 0.5},
   "console_tracce": [3, 26]},
  {"n": 2, "id": "s2", "durata": D[2], "tipo": "schema", "onesta": "schema", "dominio": "domain.s2", "voce_da": VD[1],
   "cue": {"testa": f[2][0], "segno1": f[2][1], "segno2": f[2][2], "segno3": f[2][3], "fila": round(f[2][4] - 0.4, 2), "zona": f[2][4],
           "vuoto": round(f[2][4] + 0.7, 2), "barra": round(f[2][4] + 1.4, 2), "presenza": f[2][5], "carrello": D[2]}},
  {"n": 3, "id": "s3", "durata": D[3], "tipo": "schema", "onesta": "schema", "dominio": "domain.s3", "vista": [-1300, -1250, 1300, 1450], "intest_da": "A1v3",
   "voce_da": VD[2], "cue": {"terra": 0.4, "sensori_da": 0.6, "sensori_passo": round(max(0.8, (f[3][1] - 1.0) / 4), 2), "archi": f[3][1], "riga2": round(f[3][1] + 2.5, 2)}},
  {"n": 4, "id": "s4", "durata": D[4], "tipo": "dati", "onesta": "sim", "vista": [-5300, -3300, 1900, 1380],
   "segmenti": [{"da": 0, "a": D[4], "registro": "E3v3", "t_reg": 40.0, "velocita": 1}], "dominio": "domain.s4",
   "camera": [{"t": 0, "vista": [-5300, -3300, 1900, 1380]}, {"t": f[4][2], "vista": [-5300, -3300, 1900, 1380]}, {"t": f[4][2] + 2.0, "vista": [-2400, -1900, 2000, 960]}],
   "voce_da": VD[3], "cue": {"portata": f[4][2]}},
  {"n": 5, "id": "s5", "durata": D[5], "tipo": "dati", "onesta": "sim", "vista": [-160, 60, 440, 450],
   "segmenti": [{"da": 0, "a": D[5], "registro": "E1v3", "t_reg": t5, "velocita": 1}], "tieni_ultimo_fino_a": D[5] + 1,
   "dominio": "domain.s5",
   "camera": [{"t": 0, "vista": [-160, 60, 440, 450]}, {"t": round(ev5 + 1.0, 2), "vista": [-160, 60, 440, 450]},
              {"t": round(ev5 + 3.5, 2), "vista": [-2300, -1300, 2700, 1950]}, {"t": f[5][2], "vista": [-2300, -1300, 2700, 1950]},
              {"t": round(f[5][2] + 2.5, 2), "vista": [-7600, -4900, 8000, 5250]}],
   "voce_da": VD[4], "cue": {"rit": round(ev5, 2), "zona": f[5][2]},
   "etichette_tracce": [1, 2, 4], "console_tracce": [1, 2, 4], "max_et_presenza": 0},
  {"n": 6, "id": "s6", "durata": D[6], "tipo": "dati", "onesta": "sim", "vista": [250, -600, 1450, 180],
   "segmenti": [{"da": 0, "a": D[6], "registro": "E2v3", "t_reg": t6, "velocita": 1}], "tieni_ultimo_fino_a": D[6] + 1,
   "dominio": "domain.s6",
   "camera": [{"t": 0, "vista": [250, -600, 1450, 180]}, {"t": f[6][3], "vista": [250, -600, 1450, 180]}, {"t": round(f[6][3] + 2.5, 2), "vista": [-4400, -3700, 5500, 2730]}],
   "voce_da": VD[5], "silenzi_musica": [fl6], "cue": {"camere": f[6][1], "avviso": f[6][3]},
   "etichette_tracce": [1, 2], "console_tracce": [1, 2], "max_et_presenza": 0},
  {"n": 7, "id": "s7", "durata": D[7], "tipo": "schema", "onesta": "schema", "voce_da": VD[6],
   "cue": {"righe": [f[7][1], f[7][2], f[7][3], f[7][4], f[7][5], round(f[7][5] + 2.4, 2)], "pagina": f[7][4], "regge": f[7][6],
           "contatori": [round(f[7][6] + 0.6, 2), round(f[7][6] + 5.0, 2), round(f[7][6] + 8.5, 2)]}},
  {"n": 8, "id": "s8", "durata": D[8], "tipo": "dati", "onesta": "sim", "vista": [-3.2, -0.3, 3.2, 3.4],
   "segmenti": [{"da": 1.5, "a": 6.8, "registro": "Rc9", "t_reg": 0, "velocita": 1}], "tieni_ultimo_fino_a": 11, "dominio": "domain.s8",
   "camera": [{"t": 0, "vista": [-3.2, -0.3, 3.2, 3.4]}], "voce_da": VD[7]},
  {"n": 9, "id": "s9", "durata": D[9], "tipo": "titoli", "onesta": "schema", "voce_da": VD[8],
   "cue": {"simbolo": 0, "wordmark": f[9][0], "tagline": f[9][1], "perimetro": f[9][2], "coda": round(f[9][4] - 1.5, 2)}},
 ]}
out = os.path.join(R, "scene", f"scene_v9_{L}.json")
json.dump(S, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(out, "durate", dur, "totale", round(sum(dur), 2), "| s5 t_reg", t5, "evento a", round(ev5, 2), "| s6 t_reg", t6, "lampo a", fl6)
