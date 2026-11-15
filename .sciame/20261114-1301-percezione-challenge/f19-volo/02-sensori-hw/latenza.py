"""Bilancio della latenza cattura->avviso e tempestivita' (sciame-tempo-reale, f19-volo/02-sensori-hw).
Tutti i numeri sono STIME: origine in ogni voce ('misura_prototipo', 'fonte:<chiave>', 'ipotesi', 'conto').
Uso: python -I latenza.py <cartella_uscita>
"""
import json, sys, os

OUT = sys.argv[1]

# Stadi: [minimo, massimo] in ms per ogni colonna; caso peggiore = massimo.
# Scenario di riferimento: radar a scansione elettronica con traccia a 10 Hz (EchoShield) e,
# separato, rivisita a 40 Hz sul bersaglio tracciato (ipotesi AESA multifunzione).
stadi = [
  ("eta_della_misura (attesa della rivisita)", {"cpu": [0, 100], "gpu": [0, 100], "dedicato": [0, 100]},
   "fonte:ECHOSHIELD 10 Hz -> fino a 100 ms; a 40 Hz fino a 25 ms (ipotesi)"),
  ("acquisizione (integrazione coerente, CPI)", {"cpu": [5, 20], "gpu": [5, 20], "dedicato": [5, 20]},
   "ipotesi: tempo di permanenza del fascio; indipendente dal calcolo"),
  ("trasferimento dati grezzi", {"cpu": [0.5, 2], "gpu": [0.6, 2.5], "dedicato": [0.001, 0.01]},
   "ipotesi: Ethernet 10 Gb/s verso CPU, + PCIe per la GPU; in linea su FPGA"),
  ("elaborazione segnale (formazione fasci, FFT distanza-Doppler, CFAR)", {"cpu": [5, 20], "gpu": [1, 3], "dedicato": [0.05, 0.5]},
   "ipotesi CPU; GPU con lancio dei nuclei; FPGA in flusso (CFAR 10 cicli a 100 MHz: fonte:CFAR_FPGA_PREPRINT, riassunto non aperto)"),
  ("rilevamento ed estrazione dei plot", {"cpu": [0.5, 2], "gpu": [0.2, 1], "dedicato": [0.01, 0.1]}, "ipotesi"),
  ("associazione + filtro a piu' regimi + previsione e regione + regole",
   {"cpu": [0.09, 55], "gpu": [0.05, 5], "dedicato": [0.01, 0.5]},
   "misura_prototipo: Python, mediana 0,09-11 ms, p95 peggiore 55 ms (11-prove, modo interfaccia); "
   "GPU/dedicato = codice compilato e deterministico (ipotesi fattore 10-100 sul Python); "
   "FPGA non piu' veloce della CPU per un passo (725 ns contro 250 ns: fonte:CERN_KF_FPGA), guadagno solo in determinismo"),
  ("uscita: verso macchina (bus)", {"cpu": [0.1, 1], "gpu": [0.1, 1], "dedicato": [0.01, 0.1]}, "ipotesi"),
  ("uscita: verso operatore (schermo 60 Hz + rete)", {"cpu": [17, 50], "gpu": [17, 50], "dedicato": [17, 50]},
   "ipotesi: un quadro a 60 Hz piu' composizione; non dipende dal calcolo"),
]
conferma = {  # avvio della traccia M su N rivisite: costo del SENSORE, non del calcolo
  "10Hz_3su5": [300, 500], "40Hz_3su5": [75, 125], "ASR_4.8s_2su3": [9600, 14400], "ADSB_1Hz": [0, 2000],
}

def somma(col, uscita, rivisita_ms=100):
    lo = hi = 0.0
    for nome, v, _ in stadi:
        if nome.startswith("uscita") and uscita not in nome:
            continue
        a, b = v[col]
        if nome.startswith("eta"):
            b = rivisita_ms
        lo += a; hi += b
    return [round(lo, 2), round(hi, 2)]

tot = {}
for riv, conf in ((100, "10Hz_3su5"), (25, "40Hz_3su5")):
    for col in ("cpu", "gpu", "dedicato"):
        for u in ("macchina", "operatore"):
            per_agg = somma(col, u, riv)
            c = conferma[conf]
            tot[f"{col}|riv{riv}ms|{u}"] = {
                "per_aggiornamento_ms": per_agg,
                "primo_avviso_ms (con conferma)": [round(per_agg[0] + c[0], 1), round(per_agg[1] + c[1], 1)],
                "quota_calcolo_nel_peggiore": round(sum(v[col][1] for n, v, _ in stadi
                    if n.startswith(("elaborazione", "rilevamento", "associazione", "trasferimento"))) / per_agg[1], 3),
            }
# modo prudente del prototipo: p95 340 ms (misura)
prud = somma("cpu", "operatore") ; prud_hi = prud[1] - 55 + 340

# Tempestivita': distanza minima d = v * (L_avviso + t_risposta + t_ritardo_mezzo)
risposte = {
  "umano_senza_ausilio_AC90-48": 12.5,   # fonte:AC9048 (tabella; riassunto di ricerca, PDF non aperto: 403)
  "umano_con_avviso_che_da_direzione": 5.4,  # conto dalla tabella AC 90-48: 1,0 riconoscere + 4,0 decidere + 0,4 muscoli (il 5,0 'capire la rotta di collisione' lo fa il sistema)
  "umano_addestrato_procedura_fissa": 1.5,   # ipotesi (intervallo 0,75-2,5)
  "macchina": 0.0,
}
ritardo_mezzo = {"aereo": 2.0, "drone": 0.5}  # aereo: fonte:AC9048 'aircraft lag' 2,0 s; drone: ipotesi
L = {"cpu_10Hz": tot["cpu|riv100ms|operatore"]["primo_avviso_ms (con conferma)"][1] / 1000,
     "dedicato_10Hz": tot["dedicato|riv100ms|macchina"]["primo_avviso_ms (con conferma)"][1] / 1000,
     "dedicato_40Hz": tot["dedicato|riv25ms|macchina"]["primo_avviso_ms (con conferma)"][1] / 1000,
     "cpu_prudente_10Hz": (prud_hi + conferma["10Hz_3su5"][1]) / 1000}
tab = []
for mezzo, vs in (("aereo", [70, 120, 180, 250]), ("drone", [20, 45, 70, 90])):
    for v in vs:
        r = {"mezzo": mezzo, "v_m_s": v}
        for cat, latk in (("umano_senza_ausilio_AC90-48", "cpu_10Hz"), ("umano_con_avviso_che_da_direzione", "cpu_10Hz"),
                          ("umano_con_avviso_che_da_direzione", "dedicato_10Hz"), ("umano_addestrato_procedura_fissa", "dedicato_10Hz"),
                          ("macchina", "cpu_10Hz"), ("macchina", "dedicato_10Hz"), ("macchina", "dedicato_40Hz")):
            t = L[latk] + risposte[cat] + ritardo_mezzo[mezzo]
            r[f"{cat}@{latk}_m"] = round(v * t)
        r["quota_catena_dedicata_su_umano_addestrato"] = round(L["dedicato_10Hz"] / (L["dedicato_10Hz"] + risposte["umano_addestrato_procedura_fissa"] + ritardo_mezzo[mezzo]), 3)
        tab.append(r)

out = {"_meta": {"stato": "stime (calcolato da ipotesi, fonti e misure del prototipo); nessuna misura su hardware",
                 "formula_tempestivita": "d_min = v_avvicinamento * (L_primo_avviso + t_risposta + t_ritardo_mezzo); v_avvicinamento = v del bersaglio verso un punto fermo; frontale fra due mezzi: somma delle velocita'"},
       "stadi": [{"stadio": n, "ms": v, "origine": o} for n, v, o in stadi],
       "conferma_traccia_ms": conferma, "totali": tot,
       "cpu_modo_prudente_peggiore_per_aggiornamento_ms": round(prud_hi, 1),
       "latenze_primo_avviso_s": L, "risposte_s": risposte, "ritardo_mezzo_s": ritardo_mezzo,
       "tempestivita": tab}
json.dump(out, open(os.path.join(OUT, "latenza.json"), "w"), ensure_ascii=False, indent=1)
for k, v in tot.items(): print(k, v)
print("prudente", prud_hi, "L", L)
for r in tab: print(r)
