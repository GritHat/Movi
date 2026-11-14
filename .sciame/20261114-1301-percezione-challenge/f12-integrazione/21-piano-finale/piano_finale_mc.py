# Simulazione delle durate del piano finale 14 + 4 (sciame-pianificatore, f12, passo 21).
# Tutte le durate sono STIME a tre punti, non misure. Programma mio; il modello medio e il duro riprendono le
# ipotesi dichiarate dal secondo ruolo (12-piano-rifatto/PIANO_RIFATTO.md par. 2), riscritte qui.
# Uso: timeout 300 <python di f10> -I -B piano_finale_mc.py > risultati_piano_finale_mc.txt
import sys
import numpy as np

N = 20000
PERS = ['P1', 'P2', 'P3', 'P4', 'P5']

# (id, persone, predecessori) nell'ordine delle code. Calendario finale: scheletro prima, B3 diviso, F4 e F9 protetti.
GRAFO = [
    ('K0', PERS, []),
    ('A1', ['P1'], ['K0']), ('B1', ['P2'], ['K0']), ('C1', ['P3'], ['K0']), ('D1', ['P4'], ['K0']),
    ('E2', ['P5'], ['K0']),
    ('E1', ['P4'], ['D1']), ('D2a', ['P4'], ['E1']),
    ('SK', ['P3'], ['C1', 'E2']),
    ('A2', ['P1'], ['A1']), ('B2', ['P2'], ['B1']), ('F4', ['P5'], ['E2']),
    ('F9', ['P1'], ['A2']), ('B3q', ['P5'], ['F4']), ('B3p', ['P2'], ['B2']),
    # [dopo il primo lancio] A5 passa da P1 a P5 e THL da P4 a P1: P1 aveva cinque compiti in fila (0,36 sul critico)
    ('A5', ['P5'], ['B3q']), ('A3r', ['P1'], ['F9']),
    ('C2', ['P3'], ['SK']), ('C3a', ['P3'], ['C2']),
    ('D2b', ['P4'], ['D2a', 'B2']), ('THL', ['P1'], ['A3r', 'B2']),
    ('PI', ['P2', 'P5'], ['A2', 'F9', 'A5', 'A3r', 'B3p', 'B3q', 'C2', 'SK', 'F4']),
    ('TAB', ['P4'], ['PI', 'D2b', 'THL']),
    ('PG', PERS, ['TAB', 'C3a']),
]
# stime mie (quelle della prima stesura, aggiornate: A2 con la regola a meta' impronta; B1 solo step_sd; F4 dal diff)
MIE = dict(K0=(.5, .75, 1.5), A1=(.5, 1, 2), A2=(1, 2, 3.5), B1=(1, 1.5, 3), B2=(1.5, 2, 4), B3p=(1, 1.5, 3),
           B3q=(1, 1.5, 3), C1=(2, 3, 6), C2=(2, 2.5, 5), C3a=(.5, 1, 2), D1=(1, 1.5, 3), E1=(.25, .5, 1),
           D2a=(1.5, 2.5, 4.5), D2b=(1.5, 2, 4), THL=(.5, 1, 2), E2=(.5, 1, 2.5), F4=(.5, 1, 2.5), F9=(1, 1.5, 3),
           A5=(.5, 1, 2), A3r=(.9, 1.5, 3), SK=(.25, .5, 1.5), PI=(.5, 1, 2), TAB=(.5, 1, 2), PG=(.75, .75, .75))
# stime del secondo ruolo (rifai_mc.py, dizionario MIE, calendario ALT); A5 non c'era: uso la mia
RUOLO2 = dict(MIE, K0=(.5, 1, 2.5), A2=(1, 2, 4), B1=(1, 2, 4), B2=(1.5, 3, 6), B3p=(1, 2, 4), B3q=(1, 2, 4),
              C2=(2, 3, 5.5), D2a=(1.5, 2.5, 5), D2b=(1.5, 2.5, 5), F4=(1.5, 3, 6), F9=(1, 2, 4), A3r=(1, 1.5, 3),
              PI=(.25, .75, 2), TAB=(.25, .5, 1.5))
RIUSO = {'A1', 'B1', 'D1', 'B2', 'D2a', 'E2', 'F4'}

LEGGERO = dict(nome='leggero', bias=1.0, s_sq=.12, s_p=.20, eff=(.78, .88, .96), fatica=1.0, p_ril=0, p_fermo=0,
               p_sens=0, p_lenta=0, tassa=(0, 0))
MEDIO = dict(nome='medio', bias=1.0, s_sq=.15, s_p=.20, eff=(.70, .80, .90), fatica=.95, p_ril=.20, p_fermo=.30,
             p_sens=.30, p_lenta=.20, tassa=(0, .4))
DURO = dict(nome='duro', bias=1.10, s_sq=.20, s_p=.25, eff=(.62, .74, .85), fatica=.90, p_ril=.30, p_fermo=.50,
            p_sens=.50, p_lenta=.30, tassa=(.1, .6))

PIOLI = [('libero', ['A2']), ('avviso', ['F9']), ('regione', ['B2', 'C2', 'SK']), ('identita', ['F4']),
         ('stati', ['B3p', 'B3q']), ('salute', ['A5', 'A3r', 'C3a']), ('tab_base', ['D2a', 'SK']),
         ('tab_regione', ['D2b', 'THL'])]
PROTETTI = ['libero', 'avviso', 'regione', 'identita']


def wilson(k, n, z=1.96):
    p = k / n
    c = p + z * z / (2 * n)
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    d = 1 + z * z / n
    return (c - h) / d, (c + h) / d


def simula(stime, ip, seme=1, n=N, grafo=GRAFO):
    rng = np.random.default_rng(seme)
    sq = ip['bias'] * np.exp(rng.normal(0, ip['s_sq'], n) - ip['s_sq'] ** 2 / 2)
    fp = {p: np.exp(rng.normal(0, ip['s_p'], n) - ip['s_p'] ** 2 / 2) for p in PERS}
    ef = {p: rng.triangular(*ip['eff'], n) for p in PERS}
    libero = {p: np.zeros(n) for p in PERS}
    chi = np.where(rng.random(n) < ip['p_fermo'], rng.integers(0, 5, n), -1)
    t0 = rng.uniform(1, 12, n)
    usato = np.zeros(n, bool)
    sens = rng.random(n) < ip['p_sens']
    ts, ds = rng.uniform(5, 7, n), rng.uniform(.5, 1.5, n)
    sens_usato = np.zeros(n, bool)
    ids = [c[0] for c in grafo]
    fine, inizio, lega, di = {}, {}, {}, {}
    for cid, chi_fa, pred in grafo:
        di[cid] = chi_fa
        a, m, b = stime[cid]
        w = np.full(n, m) if a == b else rng.triangular(a, m, b, n)
        fissa = cid == 'PG'
        if not fissa:
            w = w * sq * np.mean([fp[p] for p in chi_fa], axis=0)
            if cid in RIUSO and ip['p_ril'] > 0:
                w = w + (rng.random(n) < ip['p_ril']) * rng.uniform(.5, 2, n)
            if ip['tassa'][1] > 0 and any(di[q] != chi_fa and len(di[q]) < 5 for q in pred):
                w = w + rng.uniform(*ip['tassa'], n)
        cand = [libero[p] for p in chi_fa] + [fine[q] for q in pred]
        nomi = [-1 - PERS.index(p) for p in chi_fa] + [ids.index(q) for q in pred]
        mat = np.vstack(cand) if cand else np.zeros((1, n))
        ini = mat.max(axis=0)
        lega[cid] = np.array(nomi)[mat.argmax(axis=0)] if cand else np.full(n, -99)
        if cid == 'PG' and ip['p_lenta'] > 0:
            ini = ini + (rng.random(n) < ip['p_lenta']) * rng.uniform(.5, 2, n)
        e = np.mean([ef[p] for p in chi_fa], axis=0) * np.where(ini >= 10, ip['fatica'], 1.0)
        fin = ini + (w if fissa else w / e)
        for i, p in enumerate(PERS):
            if p in chi_fa:
                col = (chi == i) & ~usato & (fin > t0) & (ini < t0 + 2)
                fin = fin + 2.0 * col
                usato |= col
        if 'P5' in chi_fa and not fissa:
            col = sens & ~sens_usato & (fin > ts)
            fin = fin + ds * col
            sens_usato |= col
        fine[cid], inizio[cid] = fin, ini
        for p in chi_fa:
            libero[p] = fin
    return fine, inizio, lega


def critico(grafo, fine, lega, n):
    """Quota di estrazioni in cui il compito sta sulla catena che decide la fine di PG."""
    ids = [c[0] for c in grafo]
    ultimo = {p: [] for p in PERS}
    prec = {}                      # compito precedente nella coda della persona
    for cid, chi_fa, _ in grafo:
        for p in chi_fa:
            prec[(cid, p)] = ultimo[p][-1] if ultimo[p] else None
            ultimo[p].append(cid)
    conta = {c: 0 for c in ids}
    camp = min(n, 4000)
    for j in range(camp):
        cur = 'PG'
        while cur is not None:
            conta[cur] += 1
            l = int(lega[cur][j])
            if l == -99:
                cur = None
            elif l < 0:
                cur = prec[(cur, PERS[-1 - l])]
            else:
                cur = ids[l]
    return {c: conta[c] / camp for c in ids}


def piolo(fine, compiti):
    return np.maximum.reduce([fine[c] for c in compiti])


def riga(nome, stime, ip, seme=1, grafo=GRAFO, dettagli=False):
    fine, inizio, lega = simula(stime, ip, seme, grafo=grafo)
    n = len(fine['PG'])
    md = fine['PG']
    k = int((md <= 14).sum())
    lo, hi = wilson(k, n)
    pr = np.maximum.reduce([piolo(fine, dict(PIOLI)[p]) for p in PROTETTI])
    out = (f"{nome:<46s} {ip['nome']:<8s} P(MD<=14)={k / n:.3f} [{lo:.3f};{hi:.3f}] <=16: {(md <= 16).mean():.2f} "
           f"mediana {np.median(md):5.2f} p80 {np.percentile(md, 80):5.2f} | protetti nel tronco h12/14/16: "
           f"{(pr <= 12).mean():.3f} {(pr <= 14).mean():.3f} {(pr <= 16).mean():.3f}")
    print(out)
    if dettagli:
        print("   pioli (h12 / h14 / h16): " + "; ".join(
            f"{p} {(piolo(fine, c) <= 12).mean():.2f}/{(piolo(fine, c) <= 14).mean():.2f}/{(piolo(fine, c) <= 16).mean():.2f}"
            for p, c in PIOLI))
        print("   scheletro entro h6/h8: %.2f %.2f ; PI chiusa entro h12/13: %.2f %.2f" % (
            (fine['SK'] <= 6).mean(), (fine['SK'] <= 8).mean(), (fine['PI'] <= 12).mean(), (fine['PI'] <= 13).mean()))
        print("   mediane inizio-fine: " + " ".join(
            f"{c}:{np.median(inizio[c]):.1f}-{np.median(fine[c]):.1f}" for c in fine))
        cr = critico(grafo, fine, lega, n)
        print("   sul percorso critico: " + " ".join(f"{c}:{v:.2f}" for c, v in sorted(cr.items(), key=lambda x: -x[1])
                                                    if v >= 0.05))
        # la misura dell'ora 2: fine vera della prima rilettura di P2 (K0 + B1) / mediana attesa
        att = sum(stime[c][1] for c in ('K0', 'B1')) / ip['eff'][1]
        r = fine['B1'] / att
        for a, b in ((0, 1.0), (1.0, 1.25), (1.25, 1.5), (1.5, 1.8), (1.8, 9)):
            s = (r >= a) & (r < b)
            if s.sum() > 50:
                print(f"   rapporto ora 2 in [{a:.2f};{b:.2f}): quota {s.mean():.2f}  protetti h14 {(pr[s] <= 14).mean():.2f}"
                      f"  MD<=14 {(md[s] <= 14).mean():.2f}  (attesa K0+B1 = {att:.2f} h)")
    return k / n, (pr <= 14).mean()


def con(stime, **kw):
    return dict(stime, **kw)


if __name__ == '__main__':
    print("== 1. Calendario finale, stime mie e del secondo ruolo, tre modelli (20 000 estrazioni, seme 1)")
    for nome, st in (('FIN stime mie', MIE), ('FIN stime del secondo ruolo', RUOLO2)):
        for ip in (LEGGERO, MEDIO, DURO):
            riga(nome, st, ip, dettagli=True)
    print("== 2. Altri due semi (stime mie/leggero; stime del secondo ruolo/medio)")
    for s in (2, 3):
        riga(f'FIN stime mie, seme {s}', MIE, LEGGERO, seme=s)
        riga(f'FIN stime ruolo 2, seme {s}', RUOLO2, MEDIO, seme=s)
    print("== 3. Una ipotesi alla volta")
    k0p = (.25, .4, .75)
    for ip in (LEGGERO, MEDIO):
        riga('K0 preparato prima (mie)', con(MIE, K0=k0p), ip)
        riga('K0 preparato prima (ruolo 2)', con(RUOLO2, K0=k0p), ip)
        riga('F4 duro 1,5/3/6 (mie): controprova che cade', con(MIE, F4=(1.5, 3, 6)), ip)
        riga('F4 facile 0,5/1/2,5 (ruolo 2)', con(RUOLO2, F4=(.5, 1, 2.5)), ip)
        riga('PI 1/2/4 (mie): prima corsa insieme lenta', con(MIE, PI=(1, 2, 4)), ip)
        riga('B1 e B2 del ruolo 2 dentro le mie', con(MIE, B1=RUOLO2['B1'], B2=RUOLO2['B2']), ip)
    for nome, d in (('ore utili 0,70-0,80-0,90', dict(eff=(.70, .80, .90))), ('rilettura 20 %', dict(p_ril=.20)),
                    ('persona ferma 0,3', dict(p_fermo=.30)), ('sensore distrae 0,3', dict(p_sens=.30)),
                    ('attrito 0-0,4 h', dict(tassa=(0, .4)))):
        riga('mie + ' + nome, MIE, dict(LEGGERO, **d, nome='legg.+1'))
    print("== 4. Quattro persone (P5 assente: E2, F4, B3q a P2 e P1) - stime mie")
    g4 = []
    for cid, chi_fa, pred in GRAFO:
        if cid in ('E2', 'F4'):
            chi_fa = ['P1'] if cid == 'F4' else ['P3']
        elif cid == 'A5':
            chi_fa = ['P4']
        elif cid == 'B3q':
            chi_fa = ['P2']
        elif cid in ('K0', 'PG'):
            chi_fa = PERS[:4]
        elif cid == 'PI':
            chi_fa = ['P2', 'P1']
        g4.append((cid, chi_fa, pred))
    for ip in (LEGGERO, MEDIO):
        riga('FIN con 4 persone (mie)', MIE, ip, grafo=g4)
    print("fatto", file=sys.stderr)
