# Conti dell'esperto di dominio (f15/03-scenari). Solo conti su valori di fonte o ipotesi: nessun sensore fisico.
# Uso: python -I conti.py  -> scrive scenari.json e conti_esito.txt nella stessa cartella.
import json, math, os
QUI = os.path.dirname(os.path.abspath(__file__))
KN = 0.514444
def rett(x0, x1, y0, y1): return [[x0, y0], [x1, y0], [x1, y1], [x0, y1]]

# stato dei valori: F = fonte aperta oggi (vedi SCENARI_E_REQUISITI.md), C = classi.json (f14), I = ipotesi, M = a memoria non verificato
SC = [
 dict(id="A1", nome="Multirotore piccolo verso un sito, passa dietro un edificio", centrale=True,
  sensori=[dict(id="s_sito", tipo="da scegliere in 02-sensori (radar di sorveglianza a corto raggio + ottico)", pos=[0, 0, 10])],
  ostacoli=[dict(id="edificio", poligono=rett(150, 230, 280, 320), altezza=15)],
  oggetti=[dict(id="drone1", classe="multirotore", tipo="multirotore piccolo (< 1,1 kg, tipo Mavic 3E)", etichetta="a mano",
       t0=0, punti=[[700, 700, 60], [300, 340, 12], [100, 340, 12], [0, 60, 10]], v=[15, 15, 15], v_max=21.0, a_max=6.9, ingombro=[0.35, 0.28, 0.11])],
  avviso=dict(a_chi="operatore di sito (piazzale o varco dell'hangar)", bersaglio="drone1", v_rel=21.0, latenza=1.0, reazione=5.0, t_azione=30.0, spazio_manovra=None, margine=50.0,
       note="v_rel = v_max del multirotore (F: 75,6 km/h); latenza 1 s (I: un giro di aggiornamento a 1 Hz); reazione 5 s (I); 30 s per mettere in sicurezza l'area, sospendere un'operazione o avvertire (I); margine 50 m (I)")),
 dict(id="A2", nome="Aereo in rullaggio dietro un hangar, mezzo di servizio e persona sul piazzale", centrale=True,
  sensori=[dict(id="s_torre", tipo="da scegliere in 02-sensori (radar di superficie o lidar a lunga portata, su palo)", pos=[0, 0, 25])],
  ostacoli=[dict(id="hangar", poligono=rett(100, 160, 150, 210), altezza=18)],
  oggetti=[dict(id="aereo1", classe="aereo_rullaggio", tipo="aereo di linea a corridoio singolo in rullaggio", etichetta="a mano",
       t0=0, punti=[[350, 260, 3], [-100, 260, 3]], v=[9.0], v_max=15.4, a_max=1.0, ingombro=[37.6, 35.8, 11.8]),
     dict(id="mezzo1", classe="mezzo_piazzale", tipo="veicolo di servizio", etichetta="a mano",
       t0=13.0, punti=[[60, 100, 1], [60, 300, 1]], v=[8.3], v_max=8.3, a_max=1.5, ingombro=[5, 2, 2]),
     dict(id="persona1", classe="persona_a_piedi", tipo="operatore a piedi", etichetta="a mano",
       t0=0, punti=[[40, 200, 0.9], [40, 255, 0.9]], v=[1.4], v_max=2.5, a_max=3.0, ingombro=[0.5, 0.5, 1.8])],
  avviso=dict(a_chi="conducente del mezzo e operatore di sito (avviso diretto); in alternativa operatore di torre via radio", bersaglio="aereo1",
       v_rel=9.0 + 8.3, latenza=1.0, reazione=2.5, t_azione=None, spazio_manovra=9.0**2 / (2 * 1.0) + 8.3**2 / (2 * 1.5), margine=18.0 + 5.0,
       note="v_rel = rullaggio tipico 9,0 (C, F6) + mezzo 8,3 (C); reazione 2,5 s (F: AASHTO, presa in prestito dalla strada: I per il piazzale); frenata 1,0 e 1,5 m/s^2 (C); margine = mezza apertura alare 18 m (M) + 5 m (I)",
       variante=dict(nome="via operatore di torre", reazione=10.0, nota="vedere, decidere, parlare in radio, ricevere: 10 s (I)"))),
 dict(id="A3", nome="Aereo in avvicinamento finale e drone che scende sotto la copertura", centrale=True,
  sensori=[dict(id="s_radar", tipo="da scegliere in 02-sensori (radar di sorveglianza; cooperativi: ADS-B per l'aereo, identificazione remota per il drone)", pos=[0, 0, 10])],
  ostacoli=[dict(id="fascia_alberi_edifici", poligono=rett(50, 450, -1200, -1100), altezza=25)],
  oggetti=[dict(id="aereo2", classe="aereo_avvicinamento", tipo="aereo di linea, categoria di avvicinamento C, sentiero a 3 gradi", etichetta="a mano",
       t0=0, punti=[[200, -6000, 6000 * math.tan(math.radians(3))], [200, 0, 0]], v=[70.0], v_max=141 * KN, a_max=1.0, ingombro=[37.6, 35.8, 11.8]),
     dict(id="drone2", classe="multirotore", tipo="multirotore piccolo", etichetta="a mano",
       t0=0, punti=[[350, -2500, 120], [250, -2500, 30], [200, -2500, 30]], v=[10, 10], v_max=21.0, a_max=6.9, ingombro=[0.35, 0.28, 0.11])],
  avviso=dict(a_chi="operatore di torre, che avverte l'equipaggio (riattaccata); mai un comando automatico", bersaglio="drone2",
       v_rel=70.0 + 21.0, latenza=4.0, reazione=10.0 + 12.5, t_azione=10.0, spazio_manovra=None, margine=610.0,
       note="v_rel = 70 m/s (F: categoria C 121-141 nodi) + 21 m/s; latenza 4 s (M: un giro d'antenna di un radar d'aeroporto); operatore 10 s (I) + equipaggio 12,5 s (M: FAA AC 90-48, pagina non aperta: 403); 10 s perche' la riattaccata separi in quota (I); margine 610 m = 2000 piedi (M: 'well clear' ASTM F3442, non aperto)")),
 dict(id="A4", nome="Mezzo senza pilota che porta il sensore (volo stazionario): SOLO ANALISI", centrale=True, solo_analisi=True,
  sensori=[dict(id="s_bordo", tipo="da scegliere in 02-sensori (sensore di bordo: radar a onde millimetriche, lidar, ottico)", pos=[0, 0, 30], portatore="multirotore in volo stazionario, posa supposta nota")],
  ostacoli=[dict(id="torre_edificio", poligono=rett(60, 90, 40, 80), altezza=45)],
  oggetti=[dict(id="drone3", classe="multirotore", tipo="multirotore piccolo", etichetta="a mano",
       t0=0, punti=[[300, 20, 35], [-50, 120, 30]], v=[15], v_max=21.0, a_max=6.9, ingombro=[0.35, 0.28, 0.11])],
  avviso=dict(a_chi="pilota remoto", bersaglio="drone3", v_rel=21.0, latenza=0.5, reazione=3.0, t_azione=2.0, spazio_manovra=None, margine=10.0,
       note="portatore fermo: v_rel = 21 m/s; collegamento 0,5 s (I); pilota remoto 3 s (I); scarto laterale di 10 m con 5 m/s^2: 2 s (I); margine 10 m (I)",
       variante=dict(nome="sistema di bordo (solo avviso e arresto, I)", reazione=0.2, latenza=0.2, nota="0,2 + 0,2 s (I)"))),
 dict(id="S1", nome="Auto nascosta da un camion a un incrocio", centrale=False,
  sensori=[dict(id="s_palo", tipo="da scegliere in 02-sensori (radar a 77 GHz o lidar su palo)", pos=[0, 0, 6])],
  ostacoli=[dict(id="camion_fermo", poligono=rett(8, 24.5, 4, 6.6), altezza=4)],
  oggetti=[dict(id="auto1", classe="auto_strada_urbana", tipo="auto", etichetta="a mano",
       t0=0, punti=[[120, 9, 0.75], [-30, 9, 0.75]], v=[13.9], v_max=13.9, a_max=3.0, ingombro=[4.5, 1.8, 1.5])],
  avviso=dict(a_chi="conducente dell'altro veicolo (o sistema di bordo)", bersaglio="auto1", v_rel=13.9, latenza=0.1, reazione=2.5, t_azione=None,
       spazio_manovra=13.9**2 / (2 * 3.4), margine=2.0,
       note="50 km/h (C); reazione 2,5 s e 3,4 m/s^2 (F: AASHTO, Stopping sight distance); latenza 0,1 s (I); margine 2 m (I)",
       variante=dict(nome="sistema di bordo", reazione=0.5, spazio_manovra=13.9**2 / (2 * 6.9), nota="0,5 s (I); 6,9 m/s^2 (C)"))),
 dict(id="S2", nome="Treno dietro un convoglio fermo in stazione (a) o in galleria (b)", centrale=False,
  sensori=[dict(id="s_banchina", tipo="da scegliere in 02-sensori (radar o lidar a fine banchina)", pos=[0, 0, 5])],
  ostacoli=[dict(id="convoglio_fermo", poligono=rett(20, 220, 6, 9), altezza=4.3)],
  oggetti=[dict(id="treno1", classe="treno_banchina", tipo="treno in ingresso", etichetta="a mano",
       t0=0, punti=[[600, 12, 2], [50, 12, 2]], v=[16.7], v_max=16.7, a_max=1.0, ingombro=[200, 3, 4.3])],
  avviso=dict(a_chi="personale di stazione e macchinista", bersaglio="treno1", v_rel=16.7, latenza=1.0, reazione=3.0, t_azione=None,
       spazio_manovra=16.7**2 / (2 * 0.8), margine=20.0,
       note="60 km/h e frenata di servizio 0,8 m/s^2 (C); reazione 3 s (I); latenza 1 s (I); margine 20 m (I)",
       variante=dict(nome="b: piena linea a 160 km/h verso una galleria, frenata d'emergenza", v_rel=44.4, spazio_manovra=600.0,
           nota="600 m da 160 km/h in emergenza (F: Emergency brake (train))"))),
]

def pos(o, t):
    t -= o["t0"]; P = o["punti"]
    if t <= 0: return P[0], [0, 0, 0]
    for i, v in enumerate(o["v"]):
        a, b = P[i], P[i + 1]; L = math.dist(a, b); T = L / v
        if t <= T:
            f = t / T
            return [a[k] + f * (b[k] - a[k]) for k in range(3)], [(b[k] - a[k]) / T for k in range(3)]
        t -= T
    return P[-1], [0, 0, 0]
def durata(o): return o["t0"] + sum(math.dist(o["punti"][i], o["punti"][i + 1]) / v for i, v in enumerate(o["v"]))
def nascosto(s, p, ost):
    xs = [q[0] for q in ost["poligono"]]; ys = [q[1] for q in ost["poligono"]]
    t0, t1 = 0.0, 1.0
    for a, d, lo, hi in ((s[0], p[0] - s[0], min(xs), max(xs)), (s[1], p[1] - s[1], min(ys), max(ys))):
        if abs(d) < 1e-12:
            if a < lo or a > hi: return False
        else:
            u, w = (lo - a) / d, (hi - a) / d
            t0, t1 = max(t0, min(u, w)), min(t1, max(u, w))
    if t0 > t1: return False
    z = lambda t: s[2] + t * (p[2] - s[2])
    return min(z(t0), z(t1)) < ost["altezza"]

out = []
def stampa(*a):
    r = " ".join(str(x) for x in a); print(r); out.append(r)
def dist(av, var=None):
    a = dict(av); a.update(var or {})
    sm = a["spazio_manovra"] if a.get("spazio_manovra") is not None else a["v_rel"] * a["t_azione"]
    return a["v_rel"] * (a["latenza"] + a["reazione"]) + sm + a["margine"], a["v_rel"] * (a["latenza"] + a["reazione"]), sm

stampa("== Occlusione (campionamento a 0,1 s, raggio dal sensore al centro dell'oggetto, ostacoli estrusi) ==")
for s in SC:
    S = s["sensori"][0]["pos"]
    for o in s["oggetti"]:
        T = durata(o); n = int(T / 0.1) + 1; tratti = []; prima = None
        for i in range(n):
            t = i * 0.1; p, _ = pos(o, t)
            h = any(nascosto(S, p, k) for k in s["ostacoli"])
            if h and prima is None: prima = t
            if not h and prima is not None: tratti.append([round(prima, 1), round(t, 1)]); prima = None
        if prima is not None: tratti.append([round(prima, 1), round(T, 1)])
        o["durata_s"] = round(T, 1); o["occlusioni_s"] = tratti
        extra = ""
        if tratti:
            p0, _ = pos(o, tratti[0][0]); p1, _ = pos(o, tratti[-1][1])
            extra = " distanza dal sensore all'ingresso %.0f m, all'uscita %.0f m" % (math.dist(S, p0), math.dist(S, p1))
            o["dist_ingresso_m"] = round(math.dist(S, p0)); o["dist_uscita_m"] = round(math.dist(S, p1))
        stampa(s["id"], o["id"], "durata", round(T, 1), "s; occlusioni", tratti, "; totale", round(sum(b - a for a, b in tratti), 1), "s;" + extra)

stampa("\n== Distanza d'avviso d = v_rel*(latenza+reazione) + spazio di manovra + margine ==")
for s in SC:
    a = s["avviso"]; d, d1, sm = dist(a)
    a["d_richiesta_m"] = round(d); a["spazio_manovra_m"] = round(sm, 1)
    stampa("%s  a: %s | v_rel %.1f m/s, lat %.1f s, reaz %.1f s -> %.0f m; manovra %.0f m; margine %.0f m; d = %.0f m (tempo all'arrivo a v_rel: %.1f s)" % (s["id"], a["a_chi"], a["v_rel"], a["latenza"], a["reazione"], d1, sm, a["margine"], d, d / a["v_rel"]))
    if "variante" in a:
        v = {k: x for k, x in a["variante"].items() if k not in ("nome", "nota")}
        d, d1, sm = dist(a, v); a["variante"]["d_richiesta_m"] = round(d)
        stampa("    variante %s: d = %.0f m (percorso in latenza+reazione %.0f m, manovra %.0f m)" % (a["variante"]["nome"], d, d1, sm))

stampa("\n== Insieme raggiungibile dopo t s senza osservazioni: raggio r(t) in m ==")
stampa("   r_inv = v_max*t (inviluppo, quello che la regola di sicurezza usa); r_din = da v_tip con a_max fino a v_max")
CL = [("persona_a_piedi", 1.4, 2.5, 3.0, "disco 2D"), ("mezzo_piazzale", 1.7, 8.3, 1.5, "disco 2D (articolato)"),
      ("aereo_rullaggio", 9.0, 15.4, 1.0, "corridoio lungo la via di rullaggio"), ("auto_strada_urbana", 8.3, 13.9, 3.0, "corsie"),
      ("treno (linea, 160 km/h)", 44.4, 44.4, 1.0, "segmento 1D sul binario"), ("multirotore piccolo", 15.0, 21.0, 6.9, "sfera 3D (salita 8 m/s)"),
      ("aereo in finale (cat. C)", 70.0, 141 * KN, 1.0, "tubo lungo il sentiero")]
raggi = {}
for nome, v0, vm, am, forma in CL:
    r = {}
    for t in (5, 10, 30):
        ta = min(t, (vm - v0) / am) if am > 0 else 0
        rd = v0 * ta + 0.5 * am * ta * ta + vm * (t - ta)
        r[t] = (vm * t, rd)
    raggi[nome] = dict(forma=forma, r_inviluppo_m={str(t): round(r[t][0]) for t in r}, r_dinamico_m={str(t): round(r[t][1]) for t in r})
    stampa("%-26s %-36s r_inv 5/10/30 s: %5.0f %5.0f %5.0f | r_din: %5.0f %5.0f %5.0f | area disco a 10 s: %.2g m^2" % (nome, forma, r[5][0], r[10][0], r[30][0], r[5][1], r[10][1], r[30][1], math.pi * r[10][0] ** 2))
stampa("aereo in finale: incertezza LUNGO il sentiero se la velocita' sta fra 121 e 141 nodi (62,2-72,5 m/s): +/- %.0f, %.0f, %.0f m a 5, 10, 30 s" % tuple((141 - 121) * KN / 2 * t for t in (5, 10, 30)))
stampa("camera della prima fase: portata 3 m; avviso tempestivo fino a 1,13-1,44 m/s (SOLUZIONE_V3 r.184)")

doc = dict(versione="f15-03-scenari-0.1", data="2026-11-15",
  avvertenza="Scenari NOMINALI e parametrici, scritti a mano dall'esperto di dominio: non sono dati registrati. Tutto e' simulazione o conto; niente e' provato su un sensore fisico. Etichette di classe assegnate a mano (classificatore supposto, non realizzato). Ambito: solo osservazione, monitoraggio e avviso.",
  riferimento="locale in metri, x est, y nord, z quota sul suolo; origine alla base del sensore principale",
  formato_traiettoria="oggetto: 'punti' [x,y,z] percorsi in linea retta alla velocita' 'v' (m/s) del tratto, partenza a 't0' (s); fermo sull'ultimo punto. Chi genera verita.csv puo' raccordare con a_max.",
  origine_dati="sintetico (scritto a mano)", licenza="del progetto; nessun dato di terzi dentro questo file",
  stato_valori="F = fonte aperta il 14/15-11-2026; C = classi.json di f14; I = ipotesi; M = a memoria, non verificato (vedi 'note' e SCENARI_E_REQUISITI.md)",
  insieme_raggiungibile=raggi, scenari=SC)
json.dump(doc, open(os.path.join(QUI, "scenari.json"), "w"), ensure_ascii=False, indent=1)
open(os.path.join(QUI, "conti_esito.txt"), "w").write("\n".join(out) + "\n")
