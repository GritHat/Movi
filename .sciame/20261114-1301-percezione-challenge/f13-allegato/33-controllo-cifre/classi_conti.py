#!/usr/bin/env python3
"""Ricalcolo mio del dominio per classe (cap. 5) e dei profili di chi porta il sensore (cap. 8). Legge solo classi.json."""
import json,sys
tc,tau,C,R=0.267,0.155,0.95,3.0
d=json.load(open(sys.argv[1]))['classi']
def ds(v,Tr=1.0,ve=0.0,af=None): return (v+ve)*(tc+tau+Tr)+(ve*ve/(2*af) if ve else 0)+(v*ve/af if ve else 0)+C
print("classe | v tip/max | fascia 0,355*vmax | d_serve tip/max | entro 3 m tip/max | dopo il contatto tip/max")
nt=nm=ct=cm=n48=0
for c in d:
    if c['v_tip'] is None: continue
    vt,vm=c['v_tip'],c['v_max']
    et,em=ds(vt)<=R,ds(vm)<=R; kt,km=R/vt<tc+tau,R/vm<tc+tau
    nt+=et;nm+=em;ct+=kt;cm+=km;n48+=vm>=4.8
    print(f"{c['id']:22s} {vt:5.1f}/{vm:5.1f}  {0.355*vm:5.2f}  {ds(vt):6.2f}/{ds(vm):6.2f}  {et!s:5s}/{em!s:5s}  {kt!s:5s}/{km!s:5s}")
print(f"entro 3 m: tipica {nt}, massima {nm}; dopo il contatto: tipica {ct}, massima {cm}; vmax>=4,8: {n48} su 15; velocita' coperta Tr=1: {(R-C)/(tc+tau+1):.3f}; soglia contatto {R/(tc+tau):.2f} m/s")
print("profili: Tr | T_ant fermo | v coperta fermo | d_serve(0) in moto | v coperta in moto")
for nome,Tr,ve,af in (("stazione fissa",1.0,0,None),("veicolo terrestre",0.3,1.0,1.5),("operatore remoto",1.8,0,None),("multirotore",0.3,3.0,3.0),("persona con disabilita' visiva",1.5,1.0,1.0)):
    vc=(R-C)/(tc+tau+Tr)
    s=f"{nome:32s} {Tr:.1f} | {tc+tau+Tr:.2f} | {vc:.2f}"
    if ve:
        d0=ds(0,Tr,ve,af); vm=(R-d0)/((tc+tau+Tr)+ve/af)
        s+=f" | {d0:.2f} | {vm:.2f}"
    print(s)
print("latenza: ",16.7+95+22+21.3," ms; con 71 ms: ",16.7+71+22+21.3)
print("fascia: 0,40/(0,133+0,155+0,067) =",0.40/0.355,"; 0,20/0,355 =",0.20/0.355,"; 0,40/0,288 =",0.40/0.288)
