# Attacco f14: regole d'uso dell'etichetta, coerenza cinematica, conti di portata. numpy, seme fisso.
import json, sys, numpy as np
rng = np.random.default_rng(20261114)
K = 0.355            # eta' + latenza + tenuta (s), dalla v3
W0 = 0.40            # fascia di base v3
TAU, TCONF = 0.155, 0.267
# v_max per classe (PROFILI.md, tabella 1)
VM = {"persona": 2.5, "corsa": 8.0, "carrello": 4.5, "agv": 2.0, "auto_lav": 8.3, "treno_man": 8.3, "traino": 4.2}
CL = list(VM)
w = lambda v: max(W0, v * K)

def seq(n=45):
    """Sequenza di etichette per ciclo (15 Hz, 3 s): None = assente; cambia a istanti a caso."""
    lab = [None] * n
    t = int(rng.integers(0, n)); cur = None
    k = 0
    while k < n:
        d = int(rng.integers(3, 25))
        cur = None if rng.random() < 0.25 else CL[int(rng.integers(len(CL)))]
        lab[k:k + d] = [cur] * min(d, n - k); k += d
    return lab

def prova_regole(N=20000):
    viol = {"P_C2 (max con la base; senza etichetta = inviluppo)": 0, "U (massimo che non torna, pavimento w_scen)": 0}
    cali = {"P_C2": 0, "U": 0}; peggio = (0, None)
    for _ in range(N):
        amm = list(rng.choice(CL, size=int(rng.integers(1, 4)), replace=False))   # classi ammesse nel sito
        v_env = max(VM[c] for c in amm)
        L = seq()
        w_senza = w(v_env)                         # nessuna etichetta: inviluppo del sito (PROFILI §1, CLASSIFICATORE §1)
        wP = [w(v_env) if l is None else max(W0, VM[l] * K) for l in L]   # esperto-dominio-1 / C-2 con etichetta secca
        wU = []; m = w(v_env)
        for l in L:
            if l is not None: m = max(m, w(VM[l]))
            wU.append(m)
        if min(wP) < w_senza - 1e-12:
            viol["P_C2 (max con la base; senza etichetta = inviluppo)"] += 1
            d = w_senza - min(wP)
            if d > peggio[0]: peggio = (d, (amm, [l for i, l in enumerate(L) if i == 0 or L[i - 1] != l]))
        if min(wU) < w_senza - 1e-12: viol["U (massimo che non torna, pavimento w_scen)"] += 1
        cali["P_C2"] += any(wP[i + 1] < wP[i] - 1e-12 for i in range(len(L) - 1))   # la fascia cala nel tempo per un'etichetta
        cali["U"] += any(wU[i + 1] < wU[i] - 1e-12 for i in range(len(L) - 1))
    print("== A1. Sequenze di etichette a caso (N=%d): quota con almeno un ciclo w_con < w_senza" % N)
    for k_, v_ in viol.items(): print("   %-58s %6d  (%.3f)" % (k_, v_, v_ / N))
    print("   quota con fascia che CALA nel tempo per un cambio d'etichetta: P_C2 %.3f ; U %.3f" % (cali["P_C2"] / N, cali["U"] / N))
    print("   caso peggiore P_C2: perde %.2f m di fascia; sito=%s; etichette=%s" % (peggio[0], peggio[1][0], peggio[1][1]))
    # caso a mano: sito {persona, carrello}; carrello vero a 4 m/s; etichetta «persona» arriva a 0,5 s
    print("   caso a mano: sito {persona, carrello}; senza etichetta w=%.2f m; con «persona» sicura (regola P_C2) w=%.2f m; "
          "carrello vero a 4,0 m/s chiede %.2f m -> scoperto di %.2f m" % (w(4.5), w(2.5), 4.0 * K, 4.0 * K - w(2.5)))

def prova_attenzione():
    print("== A2. USO §5: v_obj <- min(v_max(classe), v + a_max*T_ant), d_serve = v_obj*(t_conf+tau+T_r), T_r=1,0, stazione fissa")
    Tant = TCONF + TAU + 1.0
    amax = {"pedone": 2.5, "carrello": 1.0, "auto": 2.5}; vmax = {"pedone": 2.5, "carrello": 5.0, "auto": 8.0}
    for vero, lab, v in [("carrello", "pedone", 4.0), ("auto", "pedone", 6.0), ("auto", "pedone", 0.0), ("auto", "carrello", 0.0)]:
        s2 = 0.2                                               # 2 sigma_v, ordine di grandezza
        base = v + s2                                          # traccia in vista, senza classe
        con = min(vmax[lab], v + amax[lab] * Tant)
        giusta = min(vmax[vero], v + amax[vero] * Tant)
        print("   vero %-8s a %.1f m/s, etichetta «%s»: v_obj senza classe %.2f | con l'etichetta %.2f | con la classe vera %.2f"
              "  -> d_serve %.2f | %.2f | %.2f m ; etichetta - osservato = %+.2f m"
              % (vero, v, lab, base, con, giusta, base * Tant, con * Tant, giusta * Tant, (con - base) * Tant))

def kf_speed(Z, q=0.2, sig=0.05, dt=1 / 15):
    F = np.array([[1, dt], [0, 1]]); Q = q * np.array([[dt**3 / 3, dt**2 / 2], [dt**2 / 2, dt]])
    H = np.array([[1.0, 0]]); x = np.array([Z[0], 0.0]); P = np.diag([sig**2, 4.0]); out = []
    for z in Z:
        x = F @ x; P = F @ P @ F.T + Q
        S = (H @ P @ H.T)[0, 0] + sig**2; Kg = (P @ H.T)[:, 0] / S
        x = x + Kg * (z - x[0]); P = P - np.outer(Kg, H @ P)
        out.append((abs(x[1]), np.sqrt(P[1, 1])))
    return out

def prova_coerenza(N=2000, d0=2.5, a=3.0, vmax_lab=2.5):
    """Veicolo fermo etichettato «persona»: fermo 3 s, poi parte verso il sensore con a m/s^2 da d0 m.
       c1: |v| - 2 sigma_v > v_max(etichetta) in 4 degli ultimi 6 cicli, dal 4o ciclo (USO §3). Filtro mio (1D), non quello di USO."""
    dt = 1 / 15; n0 = 45; t_imp = np.sqrt(2 * d0 / a); n1 = int(np.ceil(t_imp / dt)) + 15
    fermi = 0; prima = 0; rit = []
    for _ in range(N):
        t = np.arange(n0 + n1) * dt
        pos = np.where(t < n0 * dt, d0, d0 - 0.5 * a * np.clip(t - n0 * dt, 0, None)**2)
        Z = pos + rng.normal(0, 0.05, len(t))
        o = kf_speed(Z); flag = [(v - 2 * s) > vmax_lab for v, s in o]
        scat = None
        for k in range(4, len(flag)):
            if sum(flag[max(0, k - 5):k + 1]) >= 4: scat = k; break
        if scat is not None and scat < n0: fermi += 1
        if scat is not None and scat >= n0:
            r = (scat - n0) * dt; rit.append(r)
            if r < t_imp: prima += 1
    print("== A4. Veicolo FERMO etichettato «persona» (fermo 3 s a %.1f m, poi parte con %.1f m/s^2; contatto dopo %.2f s; N=%d)" % (d0, a, t_imp, N))
    print("   scatti di c1 mentre e' fermo: %d su %d" % (fermi, N))
    print("   scatto prima del contatto: %d su %d (%.3f); ritardo mediano dello scatto dalla partenza: %s s; v al contatto %.2f m/s (v_max «persona» %.1f)"
          % (prima, N, prima / N, ("%.2f" % np.median(rit)) if rit else "mai", a * t_imp, vmax_lab))

def prova_portata(cart):
    C = json.load(open(cart + "/classi.json"))["classi"]
    print("== A3. Conti di portata rifatti (stazione fissa, T_r=1,0 s, margine 0,40 m, portata 3 m)")
    fuori_a = fuori_b = 0; dopo = []; righe = []
    for c in C:
        vt, vm = c.get("v_tip"), c.get("v_max")
        if vt is None: continue
        dA = vt * (TAU + 1.0) + 0.40                 # formula di PROFILI
        dB = vt * (TCONF + TAU + 1.0) + 0.40         # con il tempo di conferma (USO §5)
        fuori_a += dA > 3; fuori_b += dB > 3
        t3 = 3.0 / vt; tm = 3.0 / vm
        if t3 < TCONF + TAU: dopo.append(c["id"])
        righe.append("   %-28s v_tip %5.2f v_max %5.2f | d_avv PROFILI %5.2f | con t_conf %5.2f | 3 m in %4.2f s (v_tip) %4.2f s (v_max) | avviso emesso a %4.2f m dal contatto (v_tip)"
                     % (c["id"][:28], vt, vm, dA, dB, t3, tm, max(0.0, 3 - vt * (TCONF + TAU))))
    print("\n".join(righe))
    print("   fuori dai 3 m a v_tip: formula di PROFILI %d su %d ; con t_conf %d su %d" % (fuori_a, len(righe), fuori_b, len(righe)))
    print("   avviso EMESSO dopo il contatto a v_tip (3/v < 0,422 s, cioe' v > %.2f m/s): %s" % (3 / (TCONF + TAU), dopo))
    print("   a v_max: %s" % [c["id"] for c in C if c.get("v_max") and 3.0 / c["v_max"] < TCONF + TAU])
    print("   la reazione (T_r=1,0 s) finisce dopo il contatto sopra %.2f m/s (senza margine); con margine 0,40: %.2f m/s; PROFILI dichiara 2,25" % (3 / (TCONF + TAU + 1), 2.6 / (TCONF + TAU + 1)))
    # non vedente che cammina: v_ego 1,0, T_r 1,0, a_fr 1,0 (PROFILI) ; termine mancante v_c*v_ego/a
    ve, Tr, af = 1.0, 1.0, 1.0
    for vc in (0.0, 0.82, 1.4):
        p = (vc + ve) * (TAU + Tr) + ve**2 / (2 * af) + 0.40
        q = p + vc * ve / af
        r = (vc + ve) * (TCONF + TAU + Tr) + ve**2 / (2 * af) + vc * ve / af + 0.40
        print("   non vedente in cammino (1,0 m/s; a_fr 1,0), classe a %.2f m/s: PROFILI %.2f m | + v_c*v_ego/a %.2f m | + t_conf %.2f m" % (vc, p, q, r))
    print("   stessa persona, valori di USO (T_r 1,5; b 2,0): limite dichiarato 0,34 m/s; valori di PROFILI: 0,82 m/s. Due tabelle, due risposte.")

prova_regole(); prova_attenzione(); prova_portata(sys.argv[1]); prova_coerenza(); prova_coerenza(d0=2.5, a=1.5)
