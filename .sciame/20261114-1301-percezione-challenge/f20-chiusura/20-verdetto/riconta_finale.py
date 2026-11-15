"""riconta_finale.py (arbitro): riconto dai file grezzi di F3/F6/F1/F5/F4 (v4c e v3i), E1 (stabile e f15) e F7."""
import json, math, glob, collections, sys
B = "/home/fede/Scrivania/ed/GitHub/Movi-Hackthon/.sciame/20261114-1301-percezione-challenge"
def w(k, n, z=1.96):
    if n == 0: return "%d/0" % k
    p = k / n; d = 1 + z*z/n; c = (p + z*z/(2*n))/d; h = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n))/d
    return "%d/%d [%.3f; %.3f]" % (k, n, max(0, c-h), min(1, c+h))
def leggi(f):
    out = []
    for l in open(f, encoding="utf-8"):
        l = l.strip()
        if l: out.append(json.loads(l))
    return out
def volo(f, nome):
    rr = collections.defaultdict(list); err = 0
    for r in leggi(f):
        if "errore" in r: err += 1; continue
        rr[(r["scenario"], r["cfg"])].append(r)
    print("==", nome, "errori", err)
    for (e, c), v in sorted(rr.items()):
        n = len(v); idx = sorted(r["idx"] for r in v); dl = [r["ritardo_evento_s"] for r in v]
        s = "%s/%s n=%d idx %d-%d unici %d | falsi %s | libero_vero %s" % (e, c, n, idx[0], idx[-1], len(set(idx)),
            w(sum(bool(r["falso_evento"]) for r in v), n), w(sum(r["libero_sul_vero"][0] > 0 for r in v), n))
        if e in ("F3", "F4"):
            s += " | <=1s %s | 0..2s %s | 0..2.5s %s | prima %s | mai %s" % (
                w(sum(x is not None and 0 <= x <= 1 + 1e-9 for x in dl), n), w(sum(x is not None and 0 <= x <= 2 + 1e-9 for x in dl), n),
                w(sum(x is not None and 0 <= x <= 2.5 + 1e-9 for x in dl), n), w(sum(x is not None and x < 0 for x in dl), n), w(sum(x is None for x in dl), n))
        print(s)
volo(B + "/f20-chiusura/01-contatto/valutazione_v4c.jsonl", "v4c valutazione")
volo(B + "/f19-volo/10-prove/passaggi_volo_v3i.jsonl", "v3i (fase 3)")
print("== E1 stabile")
E = []
for f in sorted(glob.glob(B + "/f20-chiusura/01-contatto/e1_stabile_0*.jsonl")): E += leggi(f)
n = len(E); dl = [r["ritardo_evento_s"] for r in E]
print("n", n, "idx unici", len(set(r["idx"] for r in E)),
      "| 0..2 s", w(sum(x is not None and 0 <= x <= 2 + 1e-9 for x in dl), n), "| <=2 s (con negativi)", w(sum(x is not None and x <= 2 + 1e-9 for x in dl), n),
      "| prima", w(sum(x is not None and x < 0 for x in dl), n), sorted(x for x in dl if x is not None and x < 0),
      "| 0..2.5", w(sum(x is not None and 0 <= x <= 2.5 + 1e-9 for x in dl), n), "| mai", w(sum(x is None for x in dl), n),
      "| V tutti dentro", w(sum(r["frammenti_dentro_V"][0] == r["frammenti_dentro_V"][1] for r in E), n),
      "campioni", sum(r["frammenti_dentro_V"][0] for r in E), sum(r["frammenti_dentro_V"][1] for r in E))
print("== E1 f15/2c (Eulero)")
E0 = [r for r in leggi(B + "/f15-lunga-portata/60-fase2c/01-correzioni/passaggi_v3.jsonl") if r.get("scenario") == "E1" or (r.get("lavoro") or [None])[0] == "E1"]
if E0:
    n = len(E0); dl = [r.get("ritardo_evento_s") for r in E0]
    print("n", n, "| 0..2", w(sum(x is not None and 0 <= x <= 2 + 1e-9 for x in dl), n), "| prima", w(sum(x is not None and x < 0 for x in dl), n),
          "| V tutti dentro", w(sum(r["frammenti_dentro_V"][0] == r["frammenti_dentro_V"][1] for r in E0 if r.get("frammenti_dentro_V")), n))
print("== F7 valutazione")
F = leggi(B + "/f20-chiusura/05-scorta/passaggi_valutazione.jsonl")
g = collections.defaultdict(list)
for r in F: g[(r["var"], r["cfg"])].append(r)
for (v, c), rr in sorted(g.items()):
    n = len(rr); T_EV = 6.0
    inters = [r for r in rr if r["interseca_t"] is not None]
    noint = [r for r in rr if r["interseca_t"] is None]
    print("%s/%s n=%d idx unici %d | cont %s | id %s | libero_b %s | libero_fr %s | assoc_non_dich %s | dubbie %s | evento %s | falsi %s | riacq2 %s | riacqcam2 %s | camsat %d | vol %d/%d tutti %s | inters %d avvisati_prima %d | avviso_senza_inters %s | errfine_max %.1f" % (
        v, c, n, len(set(r["idx"] for r in rr)), w(sum(r["cont_ok"] for r in rr), n), w(sum(r["id_ok"] for r in rr), n),
        w(sum(r["libero"] > 0 for r in rr), n), w(sum(r["libero_fr"] > 0 for r in rr), n), w(sum(r["assoc_detriti_non_dich"] > 0 for r in rr), n),
        w(sum(r["assoc_dubbie"] > 0 for r in rr), n), w(sum(r["evento_t"] is not None for r in rr), n), w(sum(bool(r["falso_evento"]) for r in rr), n),
        w(sum(r["rit_riacq"] is not None and r["rit_riacq"] <= 2 for r in rr), n), w(sum(r["rit_riacq_cam"] is not None and r["rit_riacq_cam"] <= 2 for r in rr), n),
        sum(r["cam_sat_affid"] for r in rr), sum(r["vol_dentro"] for r in rr), sum(r["vol_tot"] for r in rr),
        w(sum(r["vol_tot"] > 0 and r["vol_dentro"] == r["vol_tot"] for r in rr), n), len(inters),
        sum(r["avviso_t"] is not None and r["avviso_t"] <= r["interseca_t"] for r in inters),
        w(sum(r["avviso_t"] is not None for r in noint), len(noint)), max(r["err_fine_m"] for r in rr)))
    ev = [round(r["evento_t"] - T_EV, 2) for r in rr if r["evento_t"] is not None and not r["falso_evento"]]
    mg = [round(r["interseca_t"] - r["avviso_t"], 2) for r in inters if r["avviso_t"] is not None]
    if ev: print("    ritardo evento min/max", min(ev), max(ev), "| margine avviso min", min(mg) if mg else None)
