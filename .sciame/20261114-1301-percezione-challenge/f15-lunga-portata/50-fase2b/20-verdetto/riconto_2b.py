import json, math, sys, collections, statistics
B=sys.argv[1]
def w(k,n,z=1.96):
    if n==0: return (float('nan'),)*2
    p=k/n; d=1+z*z/n; c=(p+z*z/(2*n))/d; h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return round(max(0,c-h),3), round(min(1,c+h),3)
def rd(f): return [json.loads(l) for l in open(f) if l.strip()]
def pr(lbl,k,n): print(f"{lbl}: {k}/{n} {w(k,n)}")
for nome,f,fa in [("riprova",B+"/10-riprova/riprova_passaggi.jsonl","fuori_avviso"),("diagnosi",B+"/10-riprova/riprova_passaggi_diagnosi_A1_aeroporto.jsonl","fuori_avviso"),("controprova",B+"/11-controprova/cp_A_passaggi.jsonl","nasc_fuori_avviso")]:
    g=collections.defaultdict(list)
    for r in rd(f): g[(r["scen"],r["cfg"])].append(r)
    for (s,c),L in sorted(g.items()):
        n=len(L)
        pr(f"{nome} {s} {c} tempestivi",sum(bool(r.get("tempestivo")) for r in L),n)
        pr(f"{nome} {s} {c} fuori avviso",sum((r.get(fa) or 0)>0 for r in L),n)
        sr=[r.get("senza_regione",r.get("nasc_senza_regione",0)) for r in L]
        pr(f"{nome} {s} {c} senza regione",sum((x or 0)>0 for x in sr),n)
        nc=[r for r in L if not r.get("c0")]
        lv=lambda r: sum(v for kk,v in (r.get("libero_viol") or {}).items() if "C0" not in kk)
        pr(f"{nome} {s} {c} libero su oggetto non C0",sum(lv(r)>0 for r in nc),len(nc))
        pr(f"{nome} {s} {c} con fase nascosta",sum((r.get("nasc_tot") or 0)>0 for r in L),n)
        fc=[r.get("falsi_confermati") for r in L if r.get("falsi_confermati") is not None]
        if fc: print(f"   falsi confermati mediana {statistics.median(fc)}")
        if s=="A1" and c=="min":
            cnt=collections.Counter(r.get("comportamento") for r in L if (r.get(fa) or 0)>0); print("   comportamento fuori:",dict(cnt))
for nome,f in [("riprova_eventi",B+"/10-riprova/riprova_eventi_passaggi.jsonl"),("cp_E",B+"/11-controprova/cp_E_passaggi.jsonl"),("eventi_v2(nucleo v1)",B+"/02-eventi/passaggi_v2.jsonl")]:
    g=collections.defaultdict(list)
    for r in rd(f): g[(r["scenario"],r["cfg"])].append(r)
    for (s,c),L in sorted(g.items()):
        n=len(L)
        rit=[r.get("ritardo_evento_s") for r in L]
        pr(f"{nome} {s} {c} evento 0<=rit<=2",sum(x is not None and 0<=x<=2.0+1e-9 for x in rit),n)
        pr(f"{nome} {s} {c} falso evento",sum(bool(r.get("falso_evento")) for r in L),n)
        R=[(r.get("evento") or {}).get("R_imp_m") for r in L]; R=[x for x in R if x is not None]
        if R: print(f"   R_imp: n {len(R)} mediana {statistics.median(R):.0f} max {max(R):.0f}; >=10 km {sum(x>=10000 for x in R)}/{n} {w(sum(x>=10000 for x in R),n)}")
        fv=[r.get("frammenti_dentro_V") for r in L if r.get("frammenti_dentro_V")]
        if fv and sum(b for a,b in fv): print(f"   frammenti dentro V {sum(a for a,b in fv)}/{sum(b for a,b in fv)}={sum(a for a,b in fv)/sum(b for a,b in fv):.4f}")
        lf=[r.get("libero_su_frammento_in_impronta") for r in L if r.get("libero_su_frammento_in_impronta")]
        if lf: pr(f"   passaggi con libero su frammento",sum(a>0 for a,b in lf),n)
        am=[r.get("avviso_mezzo1") for r in L if r.get("avviso_mezzo1")]
        if s=="E2": pr("   mezzo avvisato a >=140 m dal frammento vero",sum((a.get("dist_dal_frammento_vero_piu_vicino_al_avviso_m") or -1)>=140 for a in am),n); pr("   mezzo avvisato a >=140 m dall'impronta",sum((a.get("dist_zona_al_avviso_m") or -1)>=140 for a in am),n)
        ta=[r.get("tracce_avvisate") for r in L if r.get("tracce_avvisate") is not None]
        if ta: print(f"   tracce avvisate {min(ta)}-{max(ta)}")
