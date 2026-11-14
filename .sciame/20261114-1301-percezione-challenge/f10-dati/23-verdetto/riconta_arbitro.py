"""Riconteggio dell'arbitro (f10, 23-verdetto). Sola lettura dei file dei risultati degli altri ruoli.
Si lancia da f10-dati/:  ambiente/venv/bin/python -I -B 23-verdetto/riconta_arbitro.py
Non importa codice di nessun altro ruolo: solo json, csv, numpy.
"""
import csv
import glob
import json
import os
import statistics as st
import sys

import numpy as np

R = sys.argv[1] if len(sys.argv) > 1 else "."
V = os.path.join(R, "20-validazione", "uscite")
SIM = os.path.join(R, "11-simulatore", "sequenze")


def wilson(k, n, z=1.959964):
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5) / d
    return (max(0.0, c - h), min(1.0, c + h))


def w(k, n):
    a, b = wilson(k, n)
    return f"{k} su {n} ({100 * a:.1f}-{100 * b:.1f} %)"


print("== C1. Sequenze simulate (11-simulatore/sequenze/INDICE.csv e cartelle) ==")
righe = list(csv.DictReader(open(os.path.join(SIM, "INDICE.csv"), encoding="utf-8")))
print("righe dell'indice:", len(righe), "; fotogrammi (somma della colonna):", sum(int(r["fotogrammi"]) for r in righe))
cart = [d for d in sorted(os.listdir(SIM)) if os.path.isdir(os.path.join(SIM, d))]
nfile = sum(len(glob.glob(os.path.join(SIM, d, "profondita", "*.npy"))) for d in cart)
print("cartelle:", len(cart), "; file .npy di profondita':", nfile)
print("con filtri:", sum(1 for r in righe if r["filtri"] == "1"), "; per livello:",
      {l: sum(1 for r in righe if r["livello"] == l) for l in sorted({r["livello"] for r in righe})})

print("\n== C2. Sequenze vere (12-dati-veri/manifesto.json e cartelle) ==")
man = json.load(open(os.path.join(R, "12-dati-veri", "manifesto.json"), encoding="utf-8"))
print("sequenze nel manifesto:", len(man["sequenze"]), "; fotogrammi:", sum(s["fotogrammi"] for s in man["sequenze"]),
      "; tracce:", len(man["tracce"]))
veri = sorted(glob.glob(os.path.join(R, "12-dati-veri", "sequenze", "*")))
print("cartelle:", len(veri), "; file di profondita':",
      sum(len(os.listdir(os.path.join(d, "profondita"))) for d in veri if os.path.isdir(os.path.join(d, "profondita"))))

print("\n== C3. K-014: celle «libero» (stato 1) il cui centro e' in ombra vera (classe 1 della maschera polare) ==")
print("   (definizione MIA, sulla maschera polare del simulatore; la validazione usa la cartesiana, «tutta in ombra»)")
for var in ("sim", "sim_p40"):
    tot = lib = 0
    nseq = 0
    geo = {}
    colpite = []
    tot_nf = lib_nf = nseq_nf = 0
    for d in sorted(glob.glob(os.path.join(V, var, "*", "griglie.npz"))):
        nome = os.path.basename(os.path.dirname(d))
        ver = json.load(open(os.path.join(SIM, nome, "verita.json"), encoding="utf-8"))
        pol = ver["ombra_suolo"]["polare"]
        m = np.array([[int(c) for c in riga] for riga in pol["celle"]], dtype=np.int8)  # [distanza, azimut]
        z = np.load(d, allow_pickle=False)
        s = z["stati"]  # [fot, azimut, distanza]
        az = z["azimut_gradi"]
        di = z["distanza_m"]
        j0 = int(round(pol["azimut_gradi_centro_prima"] - az[0]))
        assert abs(az[j0] - pol["azimut_gradi_centro_prima"]) < 1e-6 and abs(di[0] - pol["distanza_m_centro_prima"]) < 1e-6
        ombra = np.zeros(s.shape[1:], dtype=bool)
        nd = min(len(di), pol["n_distanze"])
        ombra[j0:j0 + pol["n_azimut"], :nd] = (m[:nd, :] == 1).T
        n = int(ombra.sum()) * s.shape[0]
        k = int((s[:, ombra] == 1).sum())
        if ombra.sum() == 0:
            continue
        nseq += 1
        tot += n
        lib += k
        geo[int(ombra.sum())] = geo.get(int(ombra.sum()), 0) + 1
        if k:
            colpite.append((nome, k))
        if not nome.endswith("__filtri"):
            tot_nf += n
            lib_nf += k
            nseq_nf += 1
    print(f"{var}: «libero» in ombra vera {lib} su {tot} celle·fotogramma, {nseq} sequenze con ombra; senza le __filtri: "
          f"{lib_nf} su {tot_nf}, {nseq_nf} sequenze; geometrie d'ombra distinte (celle: sequenze) {geo}; colpite {colpite}")

print("\n== C3bis. Le stesse somme dai record della validazione (misura_libero.json) ==")
for var in ("sim", "sim_p40"):
    L = json.load(open(os.path.join(V, var, "misura_libero.json"), encoding="utf-8"))
    con = [m for m in L if m.get("celle_tutte_in_ombra", 0) > 0]
    print(f"{var}: record {len(L)}; con ombra {len(con)} (di cui __filtri {sum(1 for m in con if m['nome'].endswith('__filtri'))}); "
          f"libero_tutta_ombra {sum(m['libero_tutta_ombra'] for m in con)} su "
          f"{sum(m['celle_tutte_in_ombra'] * m['fotogrammi'] for m in con)}; libero_bordo {sum(m['libero_bordo'] for m in con)} su "
          f"{sum(m['celle_di_bordo'] * m['fotogrammi'] for m in con)}; sequenze colpite "
          f"{[(m['nome'], m['libero_tutta_ombra'], m['libero_bordo']) for m in con if m['libero_tutta_ombra'] or m['libero_bordo']]}")

print("\n== C4. Bordo d'ombra (misura_ombra.json: per sequenza i percentili 0, 5, 50, 95, 100 di ciascun lato) ==")
for var in ("sim", "sim_p40"):
    O = json.load(open(os.path.join(V, var, "misura_ombra.json"), encoding="utf-8"))
    for liv in ("_nom__", "_lim__"):
        ss = [o for o in O if liv in o["nome"] and not o["nome"].endswith("__filtri") and (o["sinistra_cm"] or o["destra_cm"])]
        if not ss:
            print(var, liv, "nessun valore")
            continue
        mini = min(min(o["sinistra_cm"][0], o["destra_cm"][0]) for o in ss)
        massi = max(max(o["sinistra_cm"][4], o["destra_cm"][4]) for o in ss)
        med = st.median([o[l][2] for o in ss for l in ("sinistra_cm", "destra_cm")])
        entro = [o for o in ss if min(o["sinistra_cm"][0], o["destra_cm"][0]) >= -20 and max(o["sinistra_cm"][4], o["destra_cm"][4]) <= 20]
        prof = {}
        for o in ss:
            p = o["nome"].split("_")[0]
            prof[p] = prof.get(p, 0) + 1
        d435 = [o for o in ss if o["nome"].startswith("d435i")]
        print(f"{var} {liv}: sequenze senza filtri {len(ss)} {prof}; fotogrammi (somma del campo) {sum(o['fotogrammi'] for o in ss)}; "
              f"mediana delle mediane per sequenza {med:+.1f}, minimo assoluto {mini:+.1f}, massimo assoluto {massi:+.1f} cm; "
              f"tutte entro ±20 cm: {w(len(entro), len(ss))}; D435i: {w(sum(1 for o in d435 if o in entro), len(d435))}; "
              f"sequenze con minimo sotto 0: {sum(1 for o in ss if min(o['sinistra_cm'][0], o['destra_cm'][0]) < 0)}; sotto -10: "
              f"{sum(1 for o in ss if min(o['sinistra_cm'][0], o['destra_cm'][0]) < -10)}")

print("\n== C5-C7, C11. Passaggi D435i nominale a12 / a05 / b (misura_passaggi.json) ==")
for var in ("sim", "sim_p40"):
    P = json.load(open(os.path.join(V, var, "misura_passaggi.json"), encoding="utf-8"))
    tutti = 0
    for caso in ("a12", "a05", "b"):
        ps = [p for p in P if p["nome"].startswith(f"d435i_nom__pannello_{caso}__s") and not p["nome"].endswith("__filtri")]
        ps = [p for p in ps if p["nome"].split("__")[2][1:].isdigit()]
        n = len(ps)
        cp = sum(1 for p in ps if p["continuita_pulita"])
        disp = [p for p in ps if int(p["nome"].split("__s")[1]) % 2 == 1]
        cpd = sum(1 for p in disp if p["continuita_pulita"])
        pm = sum(1 for p in ps if p["pannello_si_muove"])
        cc = {}
        for p in ps:
            for k, v in p["cella_centro_nascosto"].items():
                cc[k] = cc.get(k, 0) + v
        reg = sum(1 for p in ps if p.get("copertura90") is not None and p["copertura90"] >= 1.0)
        nprev = sum(1 for p in ps if p.get("copertura90") is not None)
        tutti += n
        print(f"{var} {caso}: N {n}; continuita' pulita {w(cp, n)}; dispari {cpd} su {len(disp)}; pannello «si muove» {pm}; "
              f"cella del centro nascosto {cc}; verita' sempre nella regione al 90 %: {reg} su {nprev} con previsione; "
              f"fantasmi per passaggio min-max {min(p['tracce_fantasma'] for p in ps)}-{max(p['tracce_fantasma'] for p in ps)}; "
              f"osservato a soggetto nascosto in {sum(1 for p in ps if p['stato_traccia_nascosto']['osservato'] > 0)} passaggi")
    ps = [p for p in P if any(p["nome"].startswith(f"d435i_nom__pannello_{c}__s") for c in ("a12", "a05", "b"))
          and not p["nome"].endswith("__filtri")]
    cc = {}
    for p in ps:
        for k, v in p["cella_centro_nascosto"].items():
            cc[k] = cc.get(k, 0) + v
    disp = [p for p in ps if int(p["nome"].split("__s")[1]) % 2 == 1]
    pari = [p for p in ps if int(p["nome"].split("__s")[1]) % 2 == 0]
    print(f"{var} INSIEME: N {len(ps)}; continuita' {w(sum(1 for p in ps if p['continuita_pulita']), len(ps))}; dispari "
          f"{w(sum(1 for p in disp if p['continuita_pulita']), len(disp))}; pari {sum(1 for p in pari if p['continuita_pulita'])} su {len(pari)}; "
          f"pannello «si muove» {w(sum(1 for p in ps if p['pannello_si_muove']), len(ps))}; centro nascosto {cc} (totale {sum(cc.values())}); "
          f"regione: {w(sum(1 for p in ps if p.get('copertura90') is not None and p['copertura90'] >= 1.0), sum(1 for p in ps if p.get('copertura90') is not None))}")
    lim = [p for p in P if p["nome"].startswith("d435i_lim__pannello_") and "continuita_pulita" in p]
    print(f"{var} LIMITE: {sum(1 for p in lim if p['continuita_pulita'])} su {len(lim)}")
    alt = [p for p in P if p["nome"].startswith(("d455_nom", "g335_nom")) and "fusione_fotogrammi" in p]
    print(f"{var} D455+Gemini: N {len(alt)}; continuita' {sum(1 for p in alt if p['continuita_pulita'])}; "
          f"con fusione {sum(1 for p in alt if p['fusione_fotogrammi'] > 0)}")
    if var == "sim":
        fus = [p for p in P if "fusione_fotogrammi" in p and p["nome"].startswith("d435i_nom__pannello_") and
               p["nome"].split("__")[1] in ("pannello_a12", "pannello_a05", "pannello_b") and not p["nome"].endswith("__filtri")]
        print(f"sim: passaggi con almeno un fotogramma di fusione persona-pannello: {sum(1 for p in fus if p['fusione_fotogrammi'] > 0)} su {len(fus)}")

print("\n== C8. THOR (banco_thor.json) ==")
T = json.load(open(os.path.join(V, "banco_thor.json"), encoding="utf-8"))
print("finestre", T["finestre"], "persone", T["persone"], "q scelto su exp1", T["q_scelto"])
for q in ("q0.2_tutti", "q0.05_tutti", "q0.01_tutti"):
    p = T["prova"][q]
    print(q, "N", p["N"], "persone", p["persone"], "; copertura90 a 1/2/3 s:",
          " / ".join(f"{p[t]['copertura90']:.3f}" for t in ("1.0", "2.0", "3.0")),
          "; errore mediano:", " / ".join(f"{p[t]['errore_mediano']:.2f}" for t in ("1.0", "2.0", "3.0")),
          "; p90:", " / ".join(f"{p[t]['errore_p90']:.2f}" for t in ("1.0", "2.0", "3.0")),
          "; raggio95:", " / ".join(f"{p[t]['raggio95_mediano']:.2f}" for t in ("1.0", "2.0", "3.0")),
          "; fermo:", " / ".join(f"{p[t]['fermo_mediano']:.2f}" for t in ("1.0", "2.0", "3.0")))
print("taratura exp1:", {q: [round(x, 3) for x in T["taratura"][q]["copertura"]] for q in ("0.05", "0.1", "0.2")})

print("\n== C9. Costo per ciclo, dai fotogrammi.jsonl (campo tempo_ciclo_ms) ==")
for var in ("sim", "sim_p40"):
    tt = []
    for f in sorted(glob.glob(os.path.join(V, var, "*", "fotogrammi.jsonl"))):
        for riga in open(f, encoding="utf-8"):
            tt.append(json.loads(riga)["tempo_ciclo_ms"])
    a = np.array(tt)
    print(f"{var}: cicli {len(a)}; media {a.mean():.2f} ms; 95° {np.percentile(a, 95):.1f}; massimo {a.max():.1f}; oltre 66 ms: {(a > 66).sum()}")
print("(il tempo per ciclo delle sequenze vere sta solo in vere/RIEPILOGO.jsonl: letto in C12, non ricontabile)")

print("\n== C10, C15. Pavimento vuoto: celle per stato (media per fotogramma, griglie.npz) e tracce confermate (riassunto.json) ==")
for p in ("d455_nom", "d435i_nom", "g335_nom", "d435i_lim"):
    d = os.path.join(V, "sim", f"{p}__pavimento_vuoto")
    s = np.load(os.path.join(d, "griglie.npz"), allow_pickle=False)["stati"]
    ria = json.load(open(os.path.join(d, "riassunto.json"), encoding="utf-8"))
    d40 = os.path.join(V, "sim_p40", f"{p}__pavimento_vuoto", "riassunto.json")
    t40 = json.load(open(d40, encoding="utf-8"))["tracce_confermate"] if os.path.exists(d40) else None
    print(f"{p}: fotogrammi {s.shape[0]}; libero/occupato/in ombra per fotogramma "
          f"{(s == 1).sum() / s.shape[0]:.0f} / {(s == 2).sum() / s.shape[0]:.0f} / {(s == 3).sum() / s.shape[0]:.0f}; "
          f"tracce confermate {ria['tracce_confermate']} (soglia 40: {t40})")

print("\n== C12. Vero: TUM e DepthTrack (vere/RIEPILOGO.jsonl; e griglie se ci sono) ==")
for riga in open(os.path.join(V, "vere", "RIEPILOGO.jsonl"), encoding="utf-8"):
    r = json.loads(riga)
    if r["sequenza"] in ("tum_fr3_walking_static", "depthtrack_human02_indoor") and "celle_per_fotogramma" in r:
        print(r["sequenza"], r["variante"], "fotogrammi", r["fotogrammi"], "libero min/mediana/max", r.get("libero_min_mediana_max"),
              "celle", r["celle_per_fotogramma"], "tempo", r.get("tempo_ciclo_ms"), "tracce", r.get("tracce_confermate"))
f = os.path.join(V, "vere", "tum_fr3_walking_static__posa_per_fotogramma", "fotogrammi.jsonl")
lib = [json.loads(r)["celle"]["libero"] for r in open(f, encoding="utf-8")]
print("TUM posa per fotogramma, dal jsonl: N", len(lib), "libero mediana", st.median(lib), "media", round(sum(lib) / len(lib), 1), "min", min(lib), "max", max(lib))

print("\n== C16. «Libero» su celle il cui centro sta sotto l'impronta di un ostacolo fisso (classe 3 della maschera polare) ==")
print("   (definizione MIA; aggiunta dopo aver letto misura_ostacoli.txt, quindi a posteriori)")
for var in ("sim", "sim_p40"):
    tot = lib = 0
    per = {}
    for d in sorted(glob.glob(os.path.join(V, var, "*", "griglie.npz"))):
        nome = os.path.basename(os.path.dirname(d))
        ver = json.load(open(os.path.join(SIM, nome, "verita.json"), encoding="utf-8"))
        pol = ver["ombra_suolo"]["polare"]
        m = np.array([[int(c) for c in riga] for riga in pol["celle"]], dtype=np.int8)
        z = np.load(d, allow_pickle=False)
        s = z["stati"]
        j0 = int(round(pol["azimut_gradi_centro_prima"] - z["azimut_gradi"][0]))
        imp = np.zeros(s.shape[1:], dtype=bool)
        nd = min(s.shape[2], pol["n_distanze"])
        imp[j0:j0 + pol["n_azimut"], :nd] = (m[:nd, :] == 3).T
        if imp.sum() == 0:
            continue
        k = int((s[:, imp] == 1).sum())
        tot += int(imp.sum()) * s.shape[0]
        lib += k
        if k:
            chi = nome.split("__")[1] if "vetro" in nome or "scatola" in nome or "sospeso" in nome or "cassa" in nome else nome.split("__")[0] + " (pannello)"
            a = per.setdefault(chi, [0, 0, 0])
            a[0] += 1
            a[1] += k
            a[2] += int(imp.sum()) * s.shape[0]
    print(f"{var}: «libero» con il centro sotto un'impronta: {lib} su {tot} celle·fotogramma; per gruppo [sequenze colpite, libero, celle·fot] {per}")

print("\n== C17. Chi torna indietro (pannello_c) e chi si allontana nell'ombra (pannello_d): continuita' (misura_passaggi.json) ==")
for var in ("sim", "sim_p40"):
    P = json.load(open(os.path.join(V, var, "misura_passaggi.json"), encoding="utf-8"))
    for c in ("pannello_c", "pannello_d"):
        ps = [p for p in P if f"__{c}__" in p["nome"]]
        print(f"{var} {c}: N {len(ps)}; continuita' pulita {sum(1 for p in ps if p.get('continuita_pulita'))}; esiti {[p.get('esito_identita') for p in ps]}")
