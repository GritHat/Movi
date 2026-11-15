"""riconto_2c.py (sciame-arbitro): riconto indipendente dell'aggregazione dai file grezzi di 01-correzioni e delle scene _v3."""
import json, math, os, sys, statistics as st, glob
C = sys.argv[1]; V = sys.argv[2]
def wil(k, n, z=1.96):
    p = k/n; den = 1+z*z/n; m = (p+z*z/(2*n))/den; h = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n))/den
    return "%d/%d [%.3f; %.3f]" % (k, n, max(0, m-h), min(1, m+h))
def jl(f): return [json.loads(l) for l in open(os.path.join(C, f)) if l.strip()]
for f in ("riprova_passaggi_v3.jsonl", "riprova_passaggi_v3_letterale.jsonl"):
    R = jl(f)
    for cfg in ("alta", "min"):
        rs = [r for r in R if r["scen"] == "A1" and r["cfg"] == cfg]
        if not rs: continue
        nc0 = [r for r in rs if not r.get("c0")]
        viol = [r for r in nc0 if any(v > 0 for k, v in r["libero_viol"].items() if "C0" not in k)]
        print(f, cfg, "n", len(rs), "nonC0 libero", wil(len(viol), len(nc0)),
              "tempestivi", wil(sum(bool(r["tempestivo"]) for r in rs), len(rs)),
              "fuori_avviso", wil(sum(r["fuori_avviso"] > 0 for r in rs), len(rs)),
              "fa per comp", {c: sum(1 for r in rs if r["fuori_avviso"] > 0 and r["comportamento"] == c) for c in sorted({r["comportamento"] for r in rs})},
              "nasc>0", sum(r["nasc_tot"] > 0 for r in rs), "falsi_conf med", st.median(r["falsi_confermati"] for r in rs),
              "libero_tot nonC0", sum(sum(v for k, v in r["libero_tot"].items() if "C0" not in k) for r in nc0))
    print(f, "scen presenti", sorted({(r["scen"], r["cfg"]) for r in R}))
E = jl("passaggi_v3.jsonl")
print("lavori", sorted({(r["lavoro"][0], r["lavoro"][1]) for r in E}), "errori", sum("errore" in r for r in E))
for eid in ("E1", "E2", "E5"):
    rs = [r for r in E if r["lavoro"][0] == eid and "errore" not in r]
    if not rs: continue
    n = len(rs); rit = [r["ritardo_evento_s"] for r in rs if r.get("ritardo_evento_s") is not None]
    ev = [r for r in rs if r.get("evento")]
    s = "%s n=%d evento %s falsi %s" % (eid, n, wil(len(ev), n), wil(sum(bool(r.get("falso_evento")) for r in rs), n))
    if rit:
        s += " entro2s(0..2) %s neg %d rit min/med/max %.2f/%.2f/%.2f" % (wil(sum(0 <= x <= 2.0 for x in rit), n), sum(x < 0 for x in rit), min(rit), st.median(rit), max(rit))
    if ev:
        Rr = sorted(r["evento"]["R_residuo_m"] for r in ev); Ri = sorted(r["evento"]["R_imp_m"] for r in ev)
        isp = sum(1 for r in ev if r["evento"].get("ispezionati", [0])[0] > 0)
        s += " Rres min/med/max %.0f/%.0f/%.0f >=10km %d; Rimp med %.0f; ispezione tolse punti in %d/%d; libero_su_fram>0 %d" % (
            Rr[0], st.median(Rr), Rr[-1], sum(x >= 10000 for x in Rr), st.median(Ri), isp, len(ev),
            sum(1 for r in ev if (r.get("libero_su_frammento_in_impronta") or [0])[0] > 0))
    if eid == "E2":
        s += " tracce_avvisate med %s" % st.median(r.get("tracce_avvisate", 0) for r in rs)
    print(s)
x = json.load(open(os.path.join(C, "cp_X5b_v3_esito.json")))
for c in ("predefinito", "True"):
    for p in ("False", "True"):
        ks = [k for k in x if k.startswith("cert=%s " % c) and k.endswith("in_pianta=%s" % p)]
        print("cp_X5b cert=%s in_pianta=%s: stato0(libero) %d/%d valori %s" % (c, p, sum(x[k] == 0 for k in ks), len(ks), [x[k] for k in ks]))
for d in sorted(glob.glob(os.path.join(V, "*_v3"))):
    cv = open(os.path.join(d, "convalida.txt")).read().strip().splitlines()
    vc = open(os.path.join(d, "valida_video_controprova.txt")).read().strip().splitlines()
    print("==", os.path.basename(d), "| convalida:", cv[-1][:150], "| controprova:", " / ".join(vc[-3:])[:300])
