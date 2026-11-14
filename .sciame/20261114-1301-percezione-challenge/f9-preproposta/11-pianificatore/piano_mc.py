#!/usr/bin/env python3
"""Monte Carlo del calendario per la strategia S12 (sciame-pianificatore, f9). MODELLO v2.

Python puro, seme fissato. Rifare:
    timeout 120 python3 -I piano_mc.py > risultati_v2.txt
(il modello v1, con le previsioni PR1-PR6, e' in piano_mc_v1.py -> risultati_v1.txt)

Differenze dal v1, scritte in PREVISIONI.md prima del lancio:
- ordine «a gradini»: prima l'hardware (N1, A1), poi l'uscita con i dati finti, poi le corsie;
- una sola sessione di registrazione con la camera, poi taratura e accettazione in parallelo;
- tappe misurate una per una. Le stime a tre punti dei compiti sono invariate.

Modello (tutto dichiarato, niente misurato):
- compiti con stima a tre punti (ottimista, probabile, pessimista) in ore-persona,
  un compito = una persona alla volta; durata estratta da una triangolare;
- N persone uguali; una sola camera: i compiti marcati «camera» non si sovrappongono;
- ordine: fra i compiti pronti parte quello della classe piu' bassa (0 hardware, 1 uscita con
  dati finti, 2 corsie, 3 innesto e aggiunte, 4 dal vivo) e, a parita', con il cammino residuo piu' lungo;
- ore utili di lavoro W(D) per persona, triangolari; ore di chiusura F (prove generali,
  video di ripiego, presentazione), triangolari; il piano «sta» se finisce entro W - F;
- fattore di velocita' k: tutte le durate per k. Il calendario scala in modo lineare,
  quindi P(sta | k) = P(W - F >= k * M) e k* (80 %) = 20-esimo percentile di (W - F) / M.
"""
import random
import statistics

SEME = 20261114
N_ESTRAZIONI = 4000

ORE_UTILI = {24: (13, 16, 19), 36: (18, 22, 26), 48: (22, 27, 32)}  # (min, moda, max)
CHIUSURA = (2, 3, 4)  # (min, moda, max)

# nome: (O, P, Pess, predecessori, usa_camera, gradino)
COMUNI = {
    "X0a interfacce e formato dei messaggi": (0.5, 1, 2, [], False, 1),
    "X0b dati finti dal simulatore + riproduttore": (1, 1.5, 3, ["X0a"], False, 1),
    "N8a uscita a schermo (mappa, stati, eta')": (2, 3, 6, ["X0a"], False, 1),
    "N8b suoni brevi + affidabilita' persa": (2, 3, 6, ["X0a"], False, 1),
    "N7 tabella delle regole": (2, 3, 6, ["X0a"], False, 1),
    "A1 filtri spenti + controllo all'avvio": (1, 2, 4, ["N1"], True, 2),
    "N9a prima ora con l'hardware (H0-H6)": (2, 2.5, 4, ["A1"], True, 2),
    "N2 mappa a quattro stati": (4, 6, 12, ["X0a", "N1"], False, 2),
}

SENSORE = {
    "posseduto": {"N1 sensore, montaggio, registrazione": (2, 3, 6, [], True, 2)},
    "nuovo": {"N1 sensore, montaggio, registrazione": (3, 5, 12, [], True, 2)},
    "assente": {
        "N1 dati di ripiego (registrazioni o profondita' sintetica)": (3, 5, 10, [], False, 2),
    },
}

PRE24 = {
    "A2 tre fasce di quota": (2, 4, 8, ["N2"], False, 2),
    "N3 rilevamento + regola mobile": (4, 6, 12, ["N2"], False, 3),
    "N4 associazione ungherese + Kalman": (3.5, 5, 10, ["X0a"], False, 3),
    "N5 ciclo di vita + cuneo (strato 1)": (5, 7, 14, ["N4", "X0b"], False, 3),
    "A3 due ipotesi + ritaglio + pesi + previsto/perso": (5, 9, 16, ["N5"], False, 4),
    "A5 massimo avvicinamento + P intrusione + livelli": (3, 6, 10, ["N7", "A3"], False, 4),
    "A6 macchina a stati delle attivita'": (3, 5, 9, ["N5", "A3"], False, 4),
    "A7 disegno e suono per due profili": (3, 5, 9, ["N8a", "N8b", "X0b"], False, 1),
    "A8 selettore ridotto": (2, 3, 6, ["A1"], False, 2),
    "J1 percezione vera dentro le tracce": (2, 3, 6, ["N3", "N5"], False, 3),
    "LIVE dal vivo: 15 Hz, latenza, cinque atti": (
        2, 4, 8, ["J1", "N7", "N8a", "N8b", "A1", "A2", "A5", "A6", "A7", "A8"], True, 5),
    "A4 taratura della precisione dichiarata": (3, 5, 9, ["A3", "ACCa"], False, 5),
    "ACCa accettazione H7-H13, riprese": (3, 4.75, 8, ["LIVE"], True, 5),
    "ACCb accettazione, analisi delle registrazioni": (3, 4.75, 8, ["LIVE"], False, 5),
}

NUC = {  # il nucleo senza etichetta e senza area prevista (il taglio della v0.5), per confronto
    "N3 rilevamento + regola mobile": (4, 6, 12, ["N2"], False, 3),
    "N4 associazione ungherese + Kalman": (3.5, 5, 10, ["X0a"], False, 3),
    "N5 ciclo di vita + cuneo (strato 1)": (5, 7, 14, ["N4", "X0b"], False, 3),
    "J1 percezione vera dentro le tracce": (2, 3, 6, ["N3", "N5"], False, 3),
    "LIVE dal vivo: 15 Hz, latenza, cinque atti": (
        2, 4, 8, ["J1", "N7", "N8a", "N8b", "A1"], True, 5),
    "ACCa accettazione H7-H13, riprese": (3, 4.75, 8, ["LIVE"], True, 5),
    "ACCb accettazione, analisi delle registrazioni": (3, 4.75, 8, ["LIVE"], False, 5),
}

MIN = {
    "N3r gruppi + velocita' del filtro": (3, 4, 8, ["N2"], False, 3),
    "N4r una traccia al piu' vicino + Kalman": (2, 3, 6, ["X0a"], False, 3),
    "N5 ciclo di vita + cuneo (strato 1)": (5, 7, 14, ["N4r", "X0b"], False, 3),
    "C1 previsione continua a una ipotesi, ritagliata": (2, 3, 6, ["N5"], False, 4),
    "D1 disegno minimo della previsione": (1.5, 2.5, 5, ["N8a", "X0b"], False, 1),
    "EV registro degli eventi": (1, 2, 3, ["N5"], False, 4),
    "J1 percezione vera dentro le tracce": (2, 3, 6, ["N3r", "N5"], False, 3),
    "LIVE dal vivo: 15 Hz, latenza, cinque atti": (
        2, 4, 8, ["J1", "N7", "N8a", "N8b", "A1", "C1", "D1", "EV"], True, 5),
    "REG una sessione: 45 passaggi, 10 soste, latenza": (1, 1.5, 3, ["LIVE"], True, 5),
    "CAL taratura ridotta sulle registrazioni": (1.5, 2, 4, ["C1", "REG"], False, 5),
    "ACC accettazione ridotta sulle registrazioni": (1.5, 2, 3.5, ["REG"], False, 5),
}

MED = dict(MIN)
MED.update({
    "C2 seconda ipotesi (sosta) + pesi": (4, 7, 12, ["C1"], False, 4),
    "L1 livelli come rilettura della tabella": (1, 2, 4, ["N7"], False, 4),
    "P1 massimo avvicinamento (solo geometria)": (1, 1.5, 3, ["N7", "N4r"], False, 4),
    "LIVE dal vivo: 15 Hz, latenza, cinque atti": (
        2, 4, 8, ["J1", "N7", "N8a", "N8b", "A1", "C1", "D1", "EV", "C2", "L1", "P1"], True, 5),
    "CAL taratura ridotta sulle registrazioni": (1.5, 2, 4, ["C2", "REG"], False, 5),
})

AGGIUNTI_PRE24 = ["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8"]

CLASSE = {
    "N1": 0, "A1": 0,
    "X0a": 1, "X0b": 1, "N8a": 1, "N8b": 1, "N7": 1, "D1": 1,
    "N2": 2, "N4": 2, "N4r": 2, "N5": 2, "C1": 2, "N9a": 2,
    "LIVE": 4, "REG": 4, "CAL": 4, "ACC": 4, "ACCa": 4, "ACCb": 4, "A4": 4,
}  # tutto il resto: classe 3

TAPPE = [
    ("uscita con dati finti", ["X0a", "X0b", "N8a", "N8b", "N7", "D1", "A7"]),
    ("mappa vera + controllo all'avvio", ["N1", "A1", "N2"]),
    ("continuita' sul simulatore", ["X0a", "X0b", "N8a", "D1", "N4", "N4r", "N5", "C1", "A3"]),
    ("catena vera (innesto)", ["J1"]),
    ("dal vivo", ["LIVE"]),
    ("fine (taratura e accettazione)", None),
]


def costruisci(specifico, sensore):
    grezzo = {}
    grezzo.update(COMUNI)
    grezzo.update(SENSORE[sensore])
    grezzo.update(specifico)
    piano = {}
    for nome, (o, p, w, pred, cam, grad) in grezzo.items():
        chiave = nome.split()[0]
        if sensore == "assente":
            cam = False
            if chiave == "N9a":
                continue  # senza hardware la prima ora di misure non esiste
            if chiave == "LIVE":
                o, p, w = 1, 2, 4  # solo riproduzione a tempo reale
        piano[chiave] = dict(nome=nome, o=o, p=p, w=w, pred=list(pred), cam=cam, grad=grad)
    for t in piano.values():
        t["pred"] = [q for q in t["pred"] if q in piano]
        for q in t["pred"]:
            assert q in piano, q
    return piano


def rango(piano):
    """Cammino residuo piu' lungo con le durate probabili (compreso il compito)."""
    succ = {k: [] for k in piano}
    for k, t in piano.items():
        for q in t["pred"]:
            succ[q].append(k)
    memo = {}

    def r(k):
        if k not in memo:
            memo[k] = piano[k]["p"] + max((r(s) for s in succ[k]), default=0.0)
        return memo[k]

    return {k: r(k) for k in piano}


def cammino_critico(piano, campo="p"):
    memo = {}
    scelta = {}

    def fine(k):
        if k not in memo:
            migliore, da = 0.0, None
            for q in piano[k]["pred"]:
                if fine(q) > migliore:
                    migliore, da = fine(q), q
            memo[k] = migliore + piano[k][campo]
            scelta[k] = da
        return memo[k]

    ultimo = max(piano, key=fine)
    catena, k = [], ultimo
    while k is not None:
        catena.append(k)
        k = scelta[k]
    return memo[ultimo], list(reversed(catena))


def calendario(piano, durate, n_persone, ranghi, camera_unica=True):
    """Programmazione a lista: restituisce l'ora di fine di ogni compito."""
    fine = {}
    in_corso = {}  # compito -> ora di fine
    da_fare = set(piano)
    t = 0.0
    camera_libera = True
    while da_fare or in_corso:
        pronti = [k for k in da_fare if all(q in fine for q in piano[k]["pred"])]
        pronti.sort(key=lambda k: (CLASSE.get(k, 3), -ranghi[k], k))
        for k in pronti:
            if len(in_corso) >= n_persone:
                break
            if piano[k]["cam"] and camera_unica:
                if not camera_libera:
                    continue
                camera_libera = False
            in_corso[k] = t + durate[k]
            da_fare.discard(k)
        assert in_corso, "stallo"
        k_fine = min(in_corso, key=lambda k: (in_corso[k], k))
        t = in_corso.pop(k_fine)
        fine[k_fine] = t
        if piano[k_fine]["cam"] and camera_unica:
            camera_libera = True
    return fine


def estrai(piano, rng):
    return {k: rng.triangular(t["o"], t["w"], t["p"]) for k, t in piano.items()}


def quantile(valori, q):
    v = sorted(valori)
    i = q * (len(v) - 1)
    lo = int(i)
    hi = min(lo + 1, len(v) - 1)
    return v[lo] + (v[hi] - v[lo]) * (i - lo)


def somme(piano, chiavi=None):
    ks = list(piano) if chiavi is None else [k for k in chiavi if k in piano]
    o = sum(piano[k]["o"] for k in ks)
    p = sum(piano[k]["p"] for k in ks)
    w = sum(piano[k]["w"] for k in ks)
    pert = sum((piano[k]["o"] + 4 * piano[k]["p"] + piano[k]["w"]) / 6 for k in ks)
    tri = sum((piano[k]["o"] + piano[k]["p"] + piano[k]["w"]) / 3 for k in ks)
    return o, p, w, pert, tri


def autocontrolli():
    print("== Autocontrolli del simulatore (devono tornare) ==")
    piano = costruisci(PRE24, "posseduto")
    ranghi = rango(piano)
    dur = {k: t["p"] for k, t in piano.items()}
    serie = calendario(piano, dur, 1, ranghi)
    tot = sum(dur.values())
    print(f"1 persona: fine {max(serie.values()):.2f} h, somma delle durate {tot:.2f} h "
          f"-> {'torna' if abs(max(serie.values()) - tot) < 1e-9 else 'NON TORNA'}")
    illim = calendario(piano, dur, 99, ranghi, camera_unica=False)
    cc, _ = cammino_critico(piano)
    print(f"99 persone, camere illimitate: fine {max(illim.values()):.2f} h, cammino critico "
          f"{cc:.2f} h -> {'torna' if abs(max(illim.values()) - cc) < 1e-9 else 'NON TORNA'}")
    # braccio che deve stare: il solo gradino 1 in 24 ore
    g1 = {k: t for k, t in costruisci(MIN, "posseduto").items() if t["grad"] == 1}
    rng = random.Random(SEME)
    r1 = rango(g1)
    ok = 0
    for _ in range(2000):
        m = max(calendario(g1, estrai(g1, rng), 3, r1).values())
        a = rng.triangular(*ORE_UTILI[24][::2], ORE_UTILI[24][1]) - rng.triangular(
            CHIUSURA[0], CHIUSURA[2], CHIUSURA[1])
        ok += m <= a
    print(f"braccio che deve stare (solo gradino 1, 3 persone, 24 h): {ok}/2000")
    # braccio che deve fallire: PRE24 con 1 persona in 24 ore
    ok = 0
    for _ in range(2000):
        m = max(calendario(piano, estrai(piano, rng), 1, ranghi).values())
        a = rng.triangular(*ORE_UTILI[24][::2], ORE_UTILI[24][1]) - rng.triangular(
            CHIUSURA[0], CHIUSURA[2], CHIUSURA[1])
        ok += m <= a
    print(f"braccio che deve fallire (PRE24, 1 persona, 24 h): {ok}/2000")
    print()


def main():
    print(f"# piano_mc.py, seme {SEME}, {N_ESTRAZIONI} estrazioni per cella")
    print("# ore utili W(D) triangolari:", ORE_UTILI, "; chiusura F:", CHIUSURA)
    print()
    autocontrolli()

    piani = {"NUC": NUC, "PRE24": PRE24, "MIN": MIN, "MED": MED}

    print("== Somme (ore-persona), sensore posseduto ==")
    for nome, spec in piani.items():
        piano = costruisci(spec, "posseduto")
        o, p, w, pert, tri = somme(piano)
        cc, catena = cammino_critico(piano)
        cco, _ = cammino_critico(piano, "o")
        ccw, _ = cammino_critico(piano, "w")
        print(f"{nome}: {len(piano)} compiti; O {o:.1f}  P {p:.1f}  Pess {w:.1f}  "
              f"media PERT {pert:.1f}  media triangolare {tri:.1f}")
        print(f"   cammino critico (persone e camere illimitate): O {cco:.1f}  P {cc:.1f}  "
              f"Pess {ccw:.1f} h: {' > '.join(catena)}")
    piano = costruisci(PRE24, "posseduto")
    print("-- Moduli aggiunti dal taglio a 24 ore della preproposta --")
    for k in AGGIUNTI_PRE24:
        t = piano[k]
        print(f"   {t['nome']}: {t['o']} / {t['p']} / {t['w']}  "
              f"(PERT {(t['o'] + 4 * t['p'] + t['w']) / 6:.1f})")
    o, p, w, pert, tri = somme(piano, AGGIUNTI_PRE24)
    print(f"   somma: O {o:.1f}  P {p:.1f}  Pess {w:.1f}  PERT {pert:.1f}  triangolare {tri:.1f}")
    integ = ["X0a", "X0b", "J1", "LIVE"]
    o, p, w, pert, tri = somme(piano, integ)
    print(f"   integrazione (X0a, X0b, J1, LIVE): O {o:.1f}  P {p:.1f}  Pess {w:.1f}  PERT {pert:.1f}")
    print()

    rng = random.Random(SEME)
    disp = {}
    for d in (24, 36, 48):
        lo, moda, hi = ORE_UTILI[d]
        disp[d] = [rng.triangular(lo, hi, moda)
                   - rng.triangular(CHIUSURA[0], CHIUSURA[2], CHIUSURA[1])
                   for _ in range(N_ESTRAZIONI)]
    print("== Ore di costruzione disponibili W - F ==")
    for d in (24, 36, 48):
        print(f"D = {d} h: mediana {statistics.median(disp[d]):.1f} h, "
              f"20-esimo percentile {quantile(disp[d], 0.2):.1f} h")
    print()

    print("== Calendario: fine dei lavori M in ore di lavoro (k = 1) e probabilita' di stare ==")
    print("piano  sensore    N  M50   M80  | P(sta) 24h  36h  48h | k*(80%) 24h  36h  48h")
    tappe = {}
    for nome, spec in piani.items():
        for sens in ("posseduto", "nuovo", "assente"):
            piano = costruisci(spec, sens)
            ranghi = rango(piano)
            for n in (3, 4, 5):
                ms = []
                per_tappa = {t: [] for t, _ in TAPPE}
                for _ in range(N_ESTRAZIONI):
                    fine = calendario(piano, estrai(piano, rng), n, ranghi)
                    ms.append(max(fine.values()))
                    for t, chiavi in TAPPE:
                        ks = list(piano) if chiavi is None else [k for k in chiavi if k in piano]
                        per_tappa[t].append(max(fine[k] for k in ks))
                tappe[(nome, sens, n)] = per_tappa
                riga_p, riga_k = [], []
                for d in (24, 36, 48):
                    p_sta = sum(a >= m for a, m in zip(disp[d], ms)) / N_ESTRAZIONI
                    kstar = quantile([a / m for a, m in zip(disp[d], ms)], 0.20)
                    riga_p.append(f"{100 * p_sta:5.1f}")
                    riga_k.append(f"{kstar:4.2f}")
                print(f"{nome:6s} {sens:10s} {n}  {statistics.median(ms):4.1f}  "
                      f"{quantile(ms, 0.8):4.1f} |      {'  '.join(riga_p)} |"
                      f"       {'  '.join(riga_k)}")
        print()

    print("== Tappe: ora di lavoro a k = 1 (mediana / 80-esimo percentile) e k*(80 %) a 24, 36, 48 ore ==")
    for nome in ("MIN", "MED", "PRE24"):
        for sens in ("posseduto", "nuovo", "assente"):
            for n in (3, 4, 5):
                print(f"-- {nome}, sensore {sens}, N = {n}")
                pt = tappe[(nome, sens, n)]
                for t, _ in TAPPE:
                    ks = [quantile([a / m for a, m in zip(disp[d], pt[t])], 0.20)
                          for d in (24, 36, 48)]
                    print(f"   {t:34s} {statistics.median(pt[t]):5.1f} / {quantile(pt[t], 0.8):5.1f} h"
                          f"   k* {ks[0]:4.2f}  {ks[1]:4.2f}  {ks[2]:4.2f}")
    print()
    print("== Sensibilita': k*(80 %) del piano MIN (4 persone, posseduto) se le ore utili cambiano ==")
    pt = tappe[("MIN", "posseduto", 4)]
    for ore in (10, 13, 16, 19, 24, 30):
        riga = [f"{quantile([ore / m for m in pt[t]], 0.20):4.2f}" for t, _ in TAPPE]
        print(f"   ore di costruzione {ore:2d}: " + "  ".join(riga))


if __name__ == "__main__":
    main()
