# conti del blocco classificazione (f14, 20-inclusione). Solo lettura di ../01-profili/classi.json. numpy, seme fisso.
import json, sys, numpy as np
cl = [c for c in json.load(open(sys.argv[1]))['classi'] if c['v_tip'] is not None]
TC, TAU, PORT = 0.267, 0.155, 3.0
KW = 0.133 + 0.155 + 0.067          # eta del dato + latenza + tenuta = 0,355 s
def d_serve(v, vego=0.0, Tr=1.0, afr=None, C=0.95):
    d = (v + vego) * (TC + TAU + Tr) + C
    if vego > 0: d += vego**2 / (2*afr) + v*vego/afr
    return d
def v_cop(vego=0.0, Tr=1.0, afr=None, C=0.95):
    k = TC + TAU + Tr; fisso = vego*k + C + (vego**2/(2*afr) if vego > 0 else 0)
    return (PORT - fisso) / (k + (vego/afr if vego > 0 else 0))
print("== 1. Dominio per classe, stazione fissa, T_r 1,0 s, C 0,95 m")
print("classe | v_tip v_max | w(v_max) | d_serve tip / max | dentro 3 m tip/max | 3 m in s (tip/max) | dopo il contatto tip/max")
nt = nm = dt = dm = nw = 0
for c in cl:
    a, b = d_serve(c['v_tip']), d_serve(c['v_max']); w = c['v_max']*KW
    it, im = a <= PORT, b <= PORT; ct, cm = PORT/c['v_tip'] < TC+TAU, PORT/c['v_max'] < TC+TAU
    nt += it; nm += im; dt += ct; dm += cm; nw += w >= 1.7
    print(f"{c['id']:22s} | {c['v_tip']:5.1f} {c['v_max']:5.1f} | {w:5.2f} | {a:6.2f} / {b:6.2f} | {'si' if it else 'no'}/{'si' if im else 'no'} | {PORT/c['v_tip']:.2f}/{PORT/c['v_max']:.2f} | {'si' if ct else 'no'}/{'si' if cm else 'no'}")
print(f"dentro a v_tip {nt}/15, a v_max {nm}/15; dopo il contatto a v_tip {dt}/15, a v_max {dm}/15; w(v_max)>=1,7 m: {nw}/15; soglia dopo il contatto {PORT/(TC+TAU):.2f} m/s")
print("== 2. Velocita' coperta, stazione fissa:", " ".join(f"C={C}: {v_cop(C=C):.3f}" for C in (0.95, 0.40, 0.0)), f"| col prodotto del fascicolo (1,425 s): {(3-0.95)/1.425:.3f}")
print("== 3. Profili di chi porta il sensore (C 0,95): v coperta m/s ; d_serve per ostacolo fermo / 1,4 / 2,5 m/s")
for nome, vego, Tr, afr in [("veicolo terrestre, fermo, arresto autom.", 0, 0.3, None), ("veicolo terrestre, fermo, operatore remoto", 0, 1.8, None),
        ("veicolo terrestre a 1,0 m/s, arresto autom. [non provato]", 1.0, 0.3, 1.5), ("velivolo in volo stazionario", 0, 0.3, None),
        ("velivolo a 3,0 m/s [non provato]", 3.0, 0.3, 3.0), ("persona non vedente ferma", 0, 1.5, None),
        ("persona non vedente in cammino 1,0 m/s [non provato]", 1.0, 1.5, 1.0), ("stazione fissa, persona vicina", 0, 1.0, None)]:
    print(f"   {nome:55s} T_ant {TC+TAU+Tr+(vego/afr if vego>0 else 0):.2f} s | v coperta {v_cop(vego,Tr,afr):6.2f} | {d_serve(0,vego,Tr,afr):.2f} / {d_serve(1.4,vego,Tr,afr):.2f} / {d_serve(2.5,vego,Tr,afr):.2f}")
print("== 4. Regola composta con etichette iniettate (N=20000 sequenze, 45 cicli = 3 s, seme 20261114)")
rng = np.random.default_rng(20261114); N, Tn = 20000, 45
vmax = np.array([c['v_max'] for c in cl]); K = len(cl)
viol = dict(w_stretta=0, w_cala=0, v_bassa=0, ril_in_piu=0, d_sett=0); neg = 0; fuori = 0
celle = np.arange(0.05, 3.0, 0.1)            # distanza di celle viste libere dal bordo dell'ombra
for _ in range(N):
    sito = rng.choice(K, size=rng.integers(1, 4), replace=False); vscen = vmax[sito].max(); wscen = max(0.40, vscen*KW)
    veri = int(rng.choice(sito)); vero_v = rng.uniform(0, vmax[veri]); sig = 0.1
    t0 = rng.integers(0, Tn+10); lab = None; smentita = False; seq = []
    for t in range(Tn):                       # etichetta: assente, in ritardo, sbagliata (anche fuori sito), che cambia
        if t >= t0 and rng.random() < 0.08: lab = None if rng.random() < 0.15 else (veri if rng.random() < 0.5 else int(rng.integers(0, K)))
        seq.append(lab)
    w_o = wscen; w_prev = wscen; bad = dict.fromkeys(viol, False); negbad = False; usc = False
    for t in range(Tn):
        l = seq[t]
        if l is not None and vero_v - 2*sig > vmax[l]: smentita = True       # coerenza c1: l'etichetta decade e non torna
        l_eff = None if smentita else l
        v_oss = vero_v + rng.normal(0, sig)
        # senza etichette
        w_s = wscen; vobj_s = max(v_oss + 2*sig, vscen); ril_s = celle > w_s; d_s = PORT - wscen
        # con etichette, regola composta
        if l_eff is not None:
            w_o = max(w_o, vmax[l_eff]*KW)
            if l_eff not in sito: usc = True
        vobj_c = max(v_oss + 2*sig, vscen, vmax[l_eff] if l_eff is not None else 0.0); ril_c = celle > w_o; d_c = PORT - wscen
        bad['w_stretta'] |= w_o < w_s; bad['w_cala'] |= w_o < w_prev; bad['v_bassa'] |= vobj_c < vobj_s
        bad['ril_in_piu'] |= bool(np.any(ril_c & ~ril_s)); bad['d_sett'] |= d_c != d_s; w_prev = w_o
        # controllo negativo: «max(base, classe)» con «senza etichetta = inviluppo»
        w_neg = max(0.40, (vmax[l]*KW) if l is not None else vscen*KW); negbad |= w_neg < w_s
    for k in viol: viol[k] += bad[k]
    neg += negbad; fuori += usc
print("   regola composta, sequenze con almeno una violazione:", viol)
print(f"   controllo negativo (regola «max con la base»): {neg} su {N} ({neg/N:.3f}); sequenze con una classe fuori scenario entrata: {fuori}")
print(f"   limite superiore al 95 % con 0 su {N}: {3/N:.5f} (regola del tre)")
