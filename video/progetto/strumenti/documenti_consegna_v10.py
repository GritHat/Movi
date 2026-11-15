#!/usr/bin/env python3
"""v10 (consegna v2; copia di documenti_consegna_v9.py, che resta): scrive MoVi_copione_v2.md (copione EN con l'italiano accanto, parole e durata per scena) e
MoVi_registro_cifre_v2.md (ogni cifra con stato e fonte) in video/consegna/. Legge solo: testi detti delle due voci,
.tempi.json, scene_v10_en.json (e _it se c'è), cifre.json. Non sovrascrive: se il file esiste si ferma.
Uso: python3 -I strumenti/documenti_consegna_v10.py VOCE_EN.wav VOCE_IT.wav
"""
import json, os, re, sys

QUI = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(QUI); C = os.path.join(R, "..", "consegna")
ve, vi = sys.argv[1], sys.argv[2]
TE, TI = json.load(open(ve + ".tempi.json")), json.load(open(vi + ".tempi.json"))
SE = json.load(open(os.path.join(R, "scene", "scene_v10_en.json")))["scene"]
pit = os.path.join(R, "scene", "scene_v10_it.json")
SI = json.load(open(pit))["scene"] if os.path.exists(pit) else None
CF = json.load(open(os.path.join(R, "cifre.json")))
TIT = {1: "Un sito sorvegliato (lp_A1_v3)", 2: "Tre risposte (schema)", 3: "Sensori (schema)", 4: "Nebbia fitta (lp_E3_v3)",
       5: "Due droni si urtano (lp_E1_v3)", 6: "Avaria in decollo (lp_E2_v3)", 7: "Limiti e ciò che regge (schema)",
       8: "Stesso nucleo, corto raggio (resta_dietro)", 9: "Titoli"}
ON = {s["n"]: s.get("onesta") for s in SE}


def par(T, n):
    q = [x for x in T if x["scena"] == n]
    return " ".join(x["testo"] for x in q), (q[-1]["fine"] - q[0]["inizio"]) if q else 0.0


out = ["# MoVi · copione del video pitch (v2, consegna dopo il controllo qualità)", "",
       "Testo DETTO, uguale ai sottotitoli; generato da `strumenti/documenti_consegna_v10.py` dalle voci "
       f"`{os.path.relpath(ve, R)}` (bm_george) e `{os.path.relpath(vi, R)}` (im_nicola). Durata della scena dal montaggio "
       "(`scene_v10_en.json`; per l'italiano `scene_v10_it.json`). Etichetta d'onestà per tutta la scena: «Simulation · sensors "
       "modelled from datasheets» (sim) o «Schematic» (schema), dal VERDETTO_2C §5.", ""]
tw = [0, 0]
for s in SE:
    n = s["n"]; en, de = par(TE, n); it, di = par(TI, n)
    we, wi = len(en.split()), len(it.split()); tw[0] += we; tw[1] += wi
    dit = next((x["durata"] for x in SI if x["n"] == n), None) if SI else None
    out += [f"## Scena {n} · {TIT[n]} · {s['durata']:.2f} s · etichetta: {ON[n]}", "",
            "| EN | IT |", "|---|---|", f"| {en} | {it} |",
            f"| {we} parole · voce {de:.1f} s · {we / de * 60 if de else 0:.0f} parole/min | {wi} parole · voce {di:.1f} s"
            + (f" · scena IT {dit:.2f} s" if dit else "") + " |", ""]
D = sum(s["durata"] for s in SE)
out += [f"**Totale:** {tw[0]} parole EN, {tw[1]} parole IT; video EN {D:.2f} s"
        + (f", video IT {sum(x['durata'] for x in SI):.2f} s" if SI else "") + ".", ""]
p = os.path.join(C, "MoVi_copione_v2.md")
if os.path.exists(p): sys.exit(f"esiste già: {p}")
open(p, "w", encoding="utf-8").write("\n".join(out))

r = ["# MoVi · registro delle cifre del video (v2, consegna dopo il controllo qualità)", "",
     "Ogni cifra detta o scritta a schermo, con lo stato e la fonte. Le cifre di frase vengono da `video/progetto/cifre.json` "
     f"(versione `{CF['versione']}`, fonte `{CF['fonte_verdetto']}`). Stati: S = sostenuto in simulazione dalle schede; "
     "limite = detto come limite; verificato = controllato sul file. Le altre (in fondo) sono **lette dal registro della scena "
     "fotogramma per fotogramma** e non sono risultati generali.", "",
     "## Cifre di frase (cifre.json)", "", "| Chiave | A schermo (EN) | Detto (EN) | Stato | Fonte | Dove |", "|---|---|---|---|---|---|"]
for k, c in CF["cifre"].items():
    if c.get("stato") not in ("sostenuto", "verificato", "limite"): continue
    esc = lambda x: (x or "—").replace("|", "/")
    r.append(f"| {k} | {esc(c.get('en'))} | {esc(c.get('voce_en'))} | {c['stato']}: {esc(c.get('stato_esteso'))} | {esc(c.get('fonte'))} | {', '.join(c.get('dove', []))} |")
r += ["", "Cifre **non usate** (superate dal verdetto 2c o vietate): " + ", ".join(f"`{k}`" for k, c in CF["cifre"].items()
      if c.get("stato") not in ("sostenuto", "verificato", "limite")) + ".", "",
      "## Valori letti dal registro a schermo (non sono risultati generali)", "",
      "| Valore a schermo | Scena | Campo del registro | Stato |", "|---|---|---|---|",
      "| `NOT SEEN · x s` (età della traccia) | 1, 5, 6 | `tracce[].non_vista_da_s` | dal registro, simulazione |",
      "| `POSSIBLE PRESENCE · N` (avvisi accesi) | 1, 5, 6 | numero di `avvisi[]` con tipo «possibile_presenza» | dal registro |",
      "| `… m declared · nominal … m` (1041/1062 m, 3915/3994 m) | 4 | `portata_dichiarata[]` | dal registro; calcolo non indipendente |",
      "| `POSSIBLE DEBRIS · radius N m` (cresce da circa 320 a 1940 m) | 5 | `detriti.raggio_volume_m` | dal registro; zona **Schematic** |",
      "| `FOOTPRINT · radius 5.0 km` (E1), `3.5 km` (E2) | 5, 6 | `detriti.impronta_raggio_m` (4972 m, 3523 m) | dal registro; zona **Schematic**; K-614 aperto per E1 |",
      "| `EVENT: CONTACT · INFERRED` (scritto a 17,5 s, dedotto a 17,2 s, urto a 15,0 s) | 5 | `eventi[]` tipo «evento_contatto», `da_s` | dal registro |",
      "| `EVENT: ENGINE FAILURE OR FLASH · INFERRED`, `RELIABILITY LOST · EO/IR` | 6 | `eventi[]`, `affidabilita_per_sensore[]` («accecato», causa «quadri saturi o nube opaca» da 16,0 s; «controllo di salute» da 21,0 s) | dal registro |",
      "| `×5 · time compressed` | 1 | tratto del montaggio (5 s di registro per 1 s di video) | montaggio |",
      "| `956 m`, `806 m` | 1 | `lunga_portata.metriche_del_passaggio.d_conf_m`, `distanza_avviso_scenario_m` | dal registro |", ""]
p = os.path.join(C, "MoVi_registro_cifre_v2.md")
if os.path.exists(p): sys.exit(f"esiste già: {p}")
open(p, "w", encoding="utf-8").write("\n".join(r))
print("scritti MoVi_copione_v2.md e MoVi_registro_cifre_v2.md;", tw, "parole")
