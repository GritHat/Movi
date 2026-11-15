# Riconto dell'arbitro f19: rilegge i record per passaggio e ricalcola i Wilson al 95 %.
import json, math, sys, collections
B = "/home/fede/Scrivania/ed/GitHub/Movi-Hackthon/.sciame/20261114-1301-percezione-challenge/f15-lunga-portata/60-fase2c/01-correzioni/"
def wil(k, n, z=1.959964):
    p = k/n; d = 1+z*z/n; c = (p+z*z/(2*n))/d; h = z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return round(max(0,c-h),3), round(min(1,c+h),3)
out = {}
# E1, E2, E5 v3
rec = [json.loads(l) for l in open(B+"passaggi_v3.jsonl")]
for sc in ("E1","E2","E5"):
    R = [r for r in rec if r["scenario"]==sc]
    n = len(R); rit = [r.get("ritardo_evento_s") for r in R]
    ok = [x for x in rit if x is not None and 0<=x<=2]
    tipi = collections.Counter((r.get("evento") or {}).get("tipo") for r in R)
    cont2 = sum(1 for r in R if (r.get("evento") or {}).get("tipo")=="contatto" and r.get("ritardo_evento_s") is not None and 0<=r["ritardo_evento_s"]<=2)
    falsi = sum(1 for r in R if r.get("falso_evento"))
    # curva empirica P(dedotto entro t)
    curva = {t: sum(1 for x in rit if x is not None and 0<=x<=t) for t in (1.0,1.5,2.0,2.5,3.0)}
    rr = sorted((r.get("evento") or {}).get("R_residuo_m") or 0 for r in R)
    out[sc] = dict(n=n, entro2=len(ok), wil=wil(len(ok),n), contatto_entro2=cont2, wil_contatto=wil(cont2,n), tipi=dict(tipi), falsi=falsi, wil_falsi=wil(falsi,n),
                   curva={str(t):[k, wil(k,n)] for t,k in curva.items()}, Rres_min_med_max=[rr[0], rr[len(rr)//2], rr[-1]] if rr else None)
    print(sc, out[sc])
A = [json.loads(l) for l in open(B+"riprova_passaggi_v3.jsonl")]
for cfg in ("alta","min"):
    R=[r for r in A if r["cfg"]==cfg]; n=len(R)
    nc=[r for r in R if not r["c0"]]
    lv=sum(1 for r in nc if r["libero_viol"].get("multirotore",0)>0)
    t=sum(1 for r in R if r["tempestivo"]); fa=sum(1 for r in R if r["fuori_avviso"]>0); nas=sum(1 for r in R if r["nasc_tot"]>0)
    out["A1_"+cfg]=dict(n=n, tempestivi=t, wil_t=wil(t,n), nonC0=len(nc), libero_viol=lv, wil_lv=wil(lv,len(nc)), fuori_avviso=fa, wil_fa=wil(fa,n), con_fase_nascosta=nas)
    print("A1",cfg,out["A1_"+cfg])
# Wilson delle cifre lette nei verdetti
lette = {"A2_tempestivo":(200,200),"A2_solo_radar":(50,200),"A4_v2":(95,100),"A4_fuori_avviso_v2":(9,100),"S1_auto":(200,200),"S2_treni":(186,200),
 "A1_cp_v2":(100,100),"A1_cp_fuori":(9,100),"regola_ingenua":(564,2400),"prudente":(0,600),"E2_camere_v2":(60,60),"E2_v3":(30,30),"E4_v2":(0,60),"E5_v1":(0,300),
 "C0":(29,29),"X5b_mappa_sbagliata":(5,6),"X5b_predefinito":(0,6),"id_424":(176,180),"id_848":(174,180),"id_estraneo":(19,20),"id_nucleo":(0,90),
 "cr_avviso_424":(0,4324),"cr_avviso_rep":(0,3608),"cr_regione":(0,23402),"cr_persa_prima":(24,23402),"cr_libero":(0,9000),"cr_9su10_2m":(30,30),"cr_pannello1m":(942,1045),
 "cr_catena_previsto_sempre_424":(44,140),"cr_contenuta_2s_catena":(59,84),"cr_contenuta_3s_catena":(30,60),"cr_A3_prec2s":(32,42),"A1_singola_v2_libero":(163,171),
 "E1_cp_v2":(24,30),"E1_v2":(49,60),"cr_cpid_avviso":(0,2360)}
out["lette"]={k:[k2,n,wil(k2,n)] for k,(k2,n) in lette.items()}
for k,v in out["lette"].items(): print(k,v)
json.dump(out, open(sys.argv[1],"w"), ensure_ascii=False, indent=1)
