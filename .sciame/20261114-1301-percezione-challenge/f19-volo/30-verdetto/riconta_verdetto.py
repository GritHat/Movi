"""riconta_verdetto.py - riconto dell'arbitro (f19-volo/30-verdetto) dai record per passaggio. Wilson 95 % mio.
Uso: python -I -B riconta_verdetto.py RADICE_SCIAME uscita.json"""
import json, math, sys
from collections import defaultdict
R, OUT = sys.argv[1], sys.argv[2]
def w(k, n, z=1.96):
    p = k/n; d = 1+z*z/n; c = p+z*z/(2*n); h = z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))
    return [k, n, round(p, 4), round((c-h)/d, 3), round((c+h)/d, 3)]
def load(p): return [json.loads(l) for l in open(p)]
E = {}
for ver in ("v3i", "v3b", "v4"):
    rr = load(f"{R}/f19-volo/10-prove/passaggi_volo_{ver}.jsonl")
    g = defaultdict(list)
    for r in rr: g[(r["scenario"], r["cfg"])].append(r)
    for (s, c), L in sorted(g.items()):
        n = len(L); k = f"{ver}/{s}/{c}"; o = {"n": n}
        o["libero_sul_vero_passaggi"] = w(sum(r["libero_sul_vero"][0] > 0 for r in L), n)
        o["falso_evento"] = w(sum(bool(r["falso_evento"]) for r in L), n)
        o["continuita_senza_buchi"] = w(sum(all(v == 0 for v in r["buchi_continuita"].values()) for r in L), n)
        if s in ("F3", "F4"):
            dl = [r["ritardo_evento_s"] for r in L]
            for t in (1, 2, 3):
                o[f"evento_entro_{t}s"] = w(sum(x is not None and x <= t + 1e-9 for x in dl), n)
            o["ritardo_min_max"] = [min([x for x in dl if x is not None], default=None), max([x for x in dl if x is not None], default=None)]
            o["libero_su_frammento"] = w(sum(r["libero_su_frammento_in_impronta"][0] > 0 for r in L), n)
            fd = [r for r in L if r["frammenti_dentro_V"][1] > 0]
            if fd:
                o["passaggi_tutti_frammenti_in_V"] = w(sum(r["frammenti_dentro_V"][0] == r["frammenti_dentro_V"][1] for r in fd), len(fd))
                o["frazione_peggiore_in_V"] = round(min(r["frammenti_dentro_V"][0]/r["frammenti_dentro_V"][1] for r in fd), 4)
        if s == "F4":
            mo = [r.get("margine_operatore_s") for r in L]
            o["tempestivo_operatore"] = w(sum(m is not None and m >= 0 for m in mo), n)
            o["margine_operatore_min"] = min(m for m in mo if m is not None)
            mb = [r.get("margine_bordo_s") for r in L]
            o["margine_bordo_min"] = min(m for m in mb if m is not None)
            o["affidabilita_persa_entro3"] = w(sum(len(r["salute_cicli"]) > 0 and all(v <= 3 for v in r["salute_cicli"].values()) for r in L), n)
        if s in ("F1", "F3"):
            T = {"F1": 80.0, "F3": 20.0}[s]
            ant = [(T - r["avviso_prossimita"][0]) if r["avviso_prossimita"] else None for r in L]
            o["prossimita_anticipo_ge20"] = w(sum(a is not None and a >= 20 for a in ant), n)
            o["prossimita_anticipo_ge10"] = w(sum(a is not None and a >= 10 for a in ant), n)
        E[k] = o
# E1 (f15 fase 2c) collisione droni lenti
e1 = [r for r in load(f"{R}/f15-lunga-portata/60-fase2c/01-correzioni/passaggi_v3.jsonl") if r["scenario"] == "E1"]
dl = [r["ritardo_evento_s"] for r in e1]
E["E1_v3"] = {t: w(sum(x is not None and x <= t + 1e-9 for x in dl), len(e1)) for t in (1.0, 1.5, 2.0, 2.5)}
E["E1_v3"]["max"] = max(x for x in dl if x is not None)
# dati reali: copertura al 90 % per fascia, casi (correlati)
FA = [(1, 2), (3, 5), (6, 10), (11, 20), (21, 30)]
for m in ("aerei_veloci", "droni_ala_fissa", "multirotori"):
    d = json.load(open(f"{R}/f19-volo/03-confidenza/casi_prova_{m}.json"))
    for f in ("cv", "imm"):
        L = d[f]
        for a, b in FA:
            cs = [c for c in L if a - 0.5 <= c["tau"] < b + 0.5]
            if cs: E[f"reale/{m}/{f}/{a}-{b}s"] = w(sum(c[f]["u"] <= 0.9 for c in cs), len(cs))
json.dump(E, open(OUT, "w"), indent=1, ensure_ascii=False)
for k, v in E.items(): print(k, v)
