# -*- coding: utf-8 -*-
"""Simulazione delle durate rifatta dal rovesciatore (f12, C-E, secondo ruolo). Solo numpy.
Rifare: timeout 300 <venv>/bin/python -I -B rifai_mc.py > risultati_rifai_mc.txt
Programma indipendente da 04-piano/piano_mc.py (non letto): condivide il grafo dei compiti del §3 di
PIANO_14_4.md e, nei casi marcati «stime del piano», le sue stime a tre punti. Tutte le durate sono STIME.
"""
import sys
import numpy as np

N = 20000
PERSONE = ['P1', 'P2', 'P3', 'P4', 'P5']

# ---- stime a tre punti (ottimista, probabile, pessimista), ore di lavoro -------------------------------
PIANO = dict(K0=(.5, .75, 1.5), A1=(.5, 1, 2), A2=(1, 1.5, 3), A3=(1.5, 2.5, 5), A3r=(.9, 1.5, 3),
             B1=(1, 1.5, 3), B2=(1.5, 2, 4), B3a=(2, 3, 5.5), B3b=(2, 3, 5.5), C1=(2, 3, 6), C2=(2, 2.5, 5),
             C3a=(.5, 1, 2), C3b=(1, 1.5, 3), D1=(1, 1.5, 3), D2=(3, 4.5, 8), D4=(.75, 1.5, 3),
             E1=(.75, 1.5, 3), E2=(1, 1.5, 3), PI=(.5, 1, 2), TAB=(.5, 1, 2), LAT=(.5, 1, 2), PG=(.75, .75, .75))
# le mie: pessimista piu' largo dove c'e' codice altrui da capire o da tradurre (comp.c: 50 kB in 635 righe)
MIE = dict(PIANO, K0=(.5, 1, 2.5), A2=(1, 2, 4), A3=(1.5, 3, 6), A3r=(1, 1.5, 3), B1=(1, 2, 4),
           B2=(1.5, 3, 6), B3a=(2, 3.5, 7), B3b=(2, 3.5, 7), C2=(2, 3, 5.5), D2=(3, 5, 9), E2=(1, 2, 4),
           PI=(1, 2, 4), TAB=(.5, 1, 2.5),
           # compiti che il piano non ha
           F4=(1.5, 3, 6),        # F-401, F-402, F-408, F-409 sul percorso protetto (VD par. 3 e 6)
           F4d=(.5, 1, 2.5),      # lo stesso, se la prova 06-identita consegna una correzione che passa (NON VERIFICATO)
           THL=(.5, 1, 2),        # THOR soltanto, sul predittore mostrato (D4 ridotto)
           # rovesciamento A
           TR=(1, 1.5, 3),        # prove rosse scritte prima, nessuna modifica alla catena
           B2s=(1.25, 2.5, 5), B2i=(.5, 1, 2), D2a=(2, 3, 5.5), D2b=(1.5, 2.5, 5),
           SK=(.25, .5, 1.5), PIr=(.25, .75, 2), TABr=(.25, .5, 1.5), C3s=(.25, .5, 1),
           # calendario alternativo (ALT): riuso misurato sul posto, compiti lunghi spezzati
           E1r=(.25, .5, 1), E2r=(.5, 1, 2.5), D2r=(1.5, 2.5, 5), B3a1=(1, 2, 4), B3a2=(1, 2, 4), F9=(1, 2, 4))
RIUSO = {'A1', 'B1', 'D1', 'B2', 'B2s', 'D2', 'D2a', 'D2r', 'E2', 'E2r'}   # la rilettura puo' non passare alla prima


def compiti_piano(tagli=True, f4=None, thl=False, lat=True, suono=True):
    """Lista ordinata (coerente con le code delle persone): (id, persone, predecessori)."""
    c = [('K0', PERSONE, []),
         ('A1', ['P1'], ['K0']), ('B1', ['P2'], ['K0']), ('C1', ['P3'], ['K0']), ('D1', ['P4'], ['K0']),
         ('E1', ['P5'], ['K0']),
         ('A2', ['P1'], ['A1']), ('B2', ['P2'], ['B1']), ('D2', ['P4'], ['D1']), ('E2', ['P5'], ['E1'])]
    if f4:
        c.append((f4, ['P1'], ['A2']))
    c += [('A3r' if tagli else 'A3', ['P1'], ['A2'] + ([f4] if f4 else [])),
          ('B3a', ['P2'], ['B2'] + ([f4] if f4 else [])), ('B3b', ['P5'], ['B2', 'E2']),
          ('C2', ['P3'], ['C1']), ('C3a' if suono else 'C3s', ['P3'], ['C2'])]
    a3 = 'A3r' if tagli else 'A3'
    if not tagli:
        c += [('C3b', ['P1'], [a3]), ('D4', ['P4'], ['D2', 'B2', 'A2'])]
    if thl:
        c.append(('THL', ['P4'], ['D2', 'B2']))
    c.append(('PI', ['P2', 'P5'], ['A2', a3, 'B3a', 'B3b', 'C2', 'E2']))
    c.append(('TAB', ['P4'], ['PI', 'D2'] + ([] if tagli else ['D4']) + (['THL'] if thl else [])))
    fine = ['TAB', 'C3a' if suono else 'C3s'] + ([] if tagli else ['C3b'])
    if lat:
        c.append(('LAT', ['P5'], ['PI']))
        fine.append('LAT')
    c.append(('PG', PERSONE, fine))
    return c


def compiti_rovescio_A(f4='F4'):
    """Nessuna modifica alla catena f10 prima dell'ora 5; scheletro di punta a punta (SK) come cancello."""
    g = ['ORA5']
    return [('K0', PERSONE, []),
            ('A1', ['P1'], ['K0']), ('B1', ['P2'], ['K0']), ('C1', ['P3'], ['K0']), ('D1', ['P4'], ['K0']),
            ('E1', ['P5'], ['K0']),
            ('TR', ['P1'], ['A1']), ('B2s', ['P2'], ['B1']), ('D2a', ['P4'], ['D1']), ('E2', ['P5'], ['E1']),
            ('SK', ['P5'], ['C1', 'D2a', 'E2']),
            (f4, ['P1'], ['TR'] + g), ('A2', ['P1'], [f4]), ('A3r', ['P1'], ['A2']),
            ('B2i', ['P2'], ['B2s'] + g), ('B3a', ['P2'], ['B2i', f4]), ('B3b', ['P5'], ['B2i', 'SK']),
            ('C2', ['P3'], ['C1']), ('C3a', ['P3'], ['C2']),
            ('D2b', ['P4'], ['D2a', 'B2s']),
            ('PIr', ['P2', 'P5'], ['A2', 'A3r', 'B3a', 'B3b', 'C2', 'SK']),
            ('TABr', ['P4'], ['PIr', 'D2b']),
            ('PG', PERSONE, ['TABr', 'C3a'])]


def compiti_alt(f4='F4', cancello=True):
    """Calendario alternativo: scheletro (catena f10 com'e' -> schermo) prima di ogni modifica; B3a spezzato fra
    P2 e P5; l'avviso che finisce solo guardando (F-409, forma di c1) a P1; tabellone sul tronco dall'inizio."""
    g = ['ORA5'] if cancello else []
    return [('K0', PERSONE, []),
            ('A1', ['P1'], ['K0']), ('B1', ['P2'], ['K0']), ('C1', ['P3'], ['K0']), ('D1', ['P4'], ['K0']),
            ('E2r', ['P5'], ['K0']),
            ('E1r', ['P4'], ['D1']), ('D2r', ['P4'], ['E1r']),
            ('SK', ['P3'], ['C1', 'E2r']),      # [dopo il secondo lancio] lo scheletro lo chiude chi fa lo schermo
            ('A2', ['P1'], ['A1'] + g), ('B2', ['P2'], ['B1'] + g), (f4, ['P5'], ['E2r'] + g),
            ('F9', ['P1'], ['A2']), ('B3a1', ['P5'], [f4]), ('B3a2', ['P2'], ['B2']),
            ('A3r', ['P1'], ['F9']),
            ('C2', ['P3'], ['C1']), ('C3a', ['P3'], ['C2']),
            ('D2b', ['P4'], ['D2r', 'B2']),
            ('PIr', ['P2', 'P5'], ['A2', 'F9', 'A3r', 'B3a1', 'B3a2', 'C2', 'SK']),
            ('TABr', ['P4'], ['PIr', 'D2b']),
            ('PG', PERSONE, ['TABr', 'C3a'])]


MEDIO = dict(nome='medio', bias=1.0, s_sq=.15, s_p=.20, eff=(.70, .80, .90), fatica=.95,
             p_ril=.20, p_fermo=.30, p_sens=.30, p_lenta=.20, tassa=(0, .4))


def scala(nome, compiti, stime, ip, pioli, ora=12.0):
    """Probabilita' che ogni piolo (e tutti quelli prima) sia chiuso entro l'ora del gelo."""
    fine, _, _ = simula(compiti, stime, ip)
    cum = np.zeros(N)
    out = []
    for et, ids in pioli:
        t = np.vstack([fine[c] for c in ids]).max(axis=0)
        cum = np.maximum(cum, t)
        out.append(f"{et} {(t <= ora).mean():.2f}/{(cum <= ora).mean():.2f}")
    print(f"    {nome}: chiuso entro l'ora {ora:g} (da solo / con tutti i precedenti): " + "; ".join(out))


LEGGERO = dict(nome='leggero (simile al piano)', bias=1.0, s_sq=.12, s_p=.20, eff=(.78, .88, .96), fatica=1.0,
               p_ril=0, p_fermo=0, p_sens=0, p_lenta=0, tassa=(0, 0))
DURO = dict(nome='duro', bias=1.10, s_sq=.20, s_p=.25, eff=(.62, .74, .85), fatica=.90,
            p_ril=.30, p_fermo=.50, p_sens=.50, p_lenta=.30, tassa=(.1, .6))


def tri(rng, t, n):
    o, m, p = t
    return np.full(n, o) if o == p else rng.triangular(o, m, p, n)


def simula(compiti, stime, ip, seme=1, n=N, fermo_certo=False):
    rng = np.random.default_rng(seme)
    sq = ip['bias'] * np.exp(rng.normal(0, ip['s_sq'], n) - ip['s_sq'] ** 2 / 2)
    fp = {p: np.exp(rng.normal(0, ip['s_p'], n) - ip['s_p'] ** 2 / 2) for p in PERSONE}
    ef = {p: rng.triangular(*ip['eff'], n) for p in PERSONE}
    libero = {p: np.zeros(n) for p in PERSONE}
    # una persona ferma due ore: chi e quando
    pf = 1.0 if fermo_certo else ip['p_fermo']
    chi = np.where(rng.random(n) < pf, rng.integers(0, 5, n), -1)
    t0 = rng.uniform(1, 12, n)
    usato = np.zeros(n, bool)
    # il sensore arriva e distrae P5 fra l'ora 5 e la 7, anche se e' inutilizzabile
    sens = rng.random(n) < ip['p_sens']
    ts, ds = rng.uniform(5, 7, n), rng.uniform(.5, 1.5, n)
    sens_usato = np.zeros(n, bool)
    fine, dur, lega = {'ORA5': np.full(n, 5.0)}, {}, {}
    proprietario = {}
    for cid, chi_fa, pred in compiti:
        proprietario[cid] = chi_fa
        w = tri(rng, stime[cid], n)
        fissa = cid == 'PG'
        if not fissa:
            w = w * sq * np.mean([fp[p] for p in chi_fa], axis=0)
            if cid in RIUSO and ip['p_ril'] > 0:
                w = w + (rng.random(n) < ip['p_ril']) * rng.uniform(.5, 2, n)
            if any(q != 'ORA5' and proprietario[q] != chi_fa and len(proprietario[q]) < 5 for q in pred):
                w = w + rng.uniform(*ip['tassa'], n) if ip['tassa'][1] > 0 else w
        cand = [(libero[p], 'coda:' + p) for p in chi_fa] + [(fine[q], q) for q in pred]
        mat = np.vstack([x for x, _ in cand])
        ini = mat.max(axis=0)
        lega[cid] = (np.array([s for _, s in cand], dtype=object), mat.argmax(axis=0))
        if cid == 'PG' and ip['p_lenta'] > 0:      # la macchina della demo e' piu' lenta: si scopre in prova
            ini = ini + (rng.random(n) < ip['p_lenta']) * rng.uniform(.5, 2, n)
        e = np.mean([ef[p] for p in chi_fa], axis=0) * np.where(ini >= 10, ip['fatica'], 1.0)
        d = w if fissa else w / e
        fin = ini + d
        for i, p in enumerate(PERSONE):
            if p in chi_fa:
                col = (chi == i) & ~usato & (fin > t0) & (ini < t0 + 2)
                fin = fin + 2.0 * col
                usato |= col
        if 'P5' in chi_fa and not fissa:
            col = sens & ~sens_usato & (fin > ts)
            fin = fin + ds * col
            sens_usato |= col
        fine[cid], dur[cid] = fin, fin - ini
        for p in chi_fa:
            libero[p] = fin
    return fine, dur, lega


def critico(compiti, fine, lega, n_camp=4000):
    ultimo = {}
    coda = {}
    for cid, chi_fa, _ in compiti:
        for p in chi_fa:
            coda.setdefault(p, []).append(cid)
    conta = {c[0]: 0 for c in compiti}
    for k in range(n_camp):
        cid = 'PG'
        while True:
            conta[cid] += 1
            nomi, idx = lega[cid]
            s = nomi[idx[k]]
            if s.startswith('coda:'):
                q = coda[s[5:]]
                i = q.index(cid)
                if i == 0:
                    break
                cid = q[i - 1]
            elif s == 'ORA5':
                break
            else:
                cid = s
    return {c: v / n_camp for c, v in conta.items()}


def rango(x):
    r = np.empty(len(x))
    r[np.argsort(x, kind='stable')] = np.arange(len(x))
    return r


def wilson(k, n, z=1.96):
    p = k / n
    c = p + z * z / (2 * n)
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (c - h) / (1 + z * z / n), (c + h) / (1 + z * z / n)


def riga(nome, compiti, stime, ip, dettagli=False, protetti=None, **kw):
    fine, dur, lega = simula(compiti, stime, ip, **kw)
    t = fine['PG']
    k = int((t <= 14.0).sum())
    lo, hi = wilson(k, len(t))
    print(f"{nome:<74s} P(MD<=14)={k / len(t):.3f} [{lo:.3f};{hi:.3f}]  <=15: {(t <= 15).mean():.2f}  "
          f"<=16: {(t <= 16).mean():.2f}  mediana {np.median(t):.2f} h  80o {np.percentile(t, 80):.2f} h")
    if protetti:
        tp = np.vstack([fine[c] for c in protetti]).max(axis=0)
        print(f"    continuita' e sicurezza {'+'.join(protetti)} tutte chiuse: entro l'ora 11: {(tp <= 11).mean():.2f}; "
              f"12: {(tp <= 12).mean():.2f}; 14: {(tp <= 14).mean():.2f}; 16: {(tp <= 16).mean():.2f}; "
              f"mediana {np.median(tp):.2f} h")
    if dettagli:
        cr = critico(compiti, fine, lega)
        rt = rango(t)
        rs = {c: float(np.corrcoef(rango(dur[c]), rt)[0, 1]) for c in dur if c != 'PG'}
        print("    sul percorso critico (frazione di 4000 estrazioni) | correlazione di rango durata-fine:")
        for c, v in sorted(cr.items(), key=lambda kv: -kv[1]):
            if c != 'PG':
                print(f"      {c:<5s} {v:.2f} | {rs[c]:+.2f} | fine mediana {np.median(fine[c]):.2f} h")
    return k / len(t), float(np.median(t))


if __name__ == '__main__':
    print("N =", N, "estrazioni per riga; stime, non misure.")
    PR = ['A2', 'A3r', 'B2', 'B3a', 'B3b']
    print("\n== 0. Taratura del programma: stime e ipotesi del piano (attesi 0,46 con i tagli, 0,29 intero)")
    riga("S0  stime del piano, modello leggero, con i tagli", compiti_piano(True), PIANO, LEGGERO, protetti=PR)
    riga("S0i stime del piano, modello leggero, minimo intero", compiti_piano(False), PIANO, LEGGERO)
    print("\n== 1. Ipotesi dure sul calendario proposto (con i tagli)")
    riga("S1  stime del piano, ipotesi dure", compiti_piano(True), PIANO, DURO, protetti=PR)
    p2, m2 = riga("S2  stime mie, ipotesi dure", compiti_piano(True), MIE, DURO, dettagli=True, protetti=PR)
    for s in (2, 3):
        riga(f"S2  altro seme {s}", compiti_piano(True), MIE, DURO, seme=s)
    riga("S2i stime mie, ipotesi dure, minimo intero", compiti_piano(False), MIE, DURO)
    riga("S3  S2 con una persona ferma 2 h di sicuro", compiti_piano(True), MIE, DURO, fermo_certo=True)
    print("   una ipotesi dura alla volta sopra il modello leggero (stime mie):")
    for ch, v in (('bias', 1.10), ('eff', (.62, .74, .85)), ('p_ril', .30), ('p_fermo', .50), ('p_sens', .50),
                  ('p_lenta', .30), ('tassa', (.1, .6)), ('fatica', .90)):
        riga(f"      leggero + {ch}={v}", compiti_piano(True), MIE, dict(LEGGERO, **{ch: v}))
    riga("      leggero, stime mie", compiti_piano(True), MIE, LEGGERO)
    print("\n== 2. Il piano con F-401/402/408/409 sul percorso protetto (VD), ipotesi dure, stime mie")
    PR4 = ['A2', 'A3r', 'B2', 'B3a', 'B3b', 'F4']
    p5, _ = riga("S5  + F4 (1,5/3/6) prima di B3a, + THOR ridotto", compiti_piano(True, 'F4', thl=True), MIE, DURO,
                 dettagli=True, protetti=PR4)
    riga("S5d + F4d (0,5/1/2,5: se 06-identita passa; non verificato)", compiti_piano(True, 'F4d', thl=True), MIE, DURO,
         protetti=['A2', 'A3r', 'B2', 'B3a', 'B3b', 'F4d'])
    print("\n== 3. Rovesciamenti (ipotesi dure, stime mie); il confronto giusto e' con S5")
    pa, _ = riga("RA  catena f10 cosi' com'e' fino all'ora 5, scheletro SK, poi correzioni", compiti_rovescio_A('F4'), MIE,
                 DURO, dettagli=True, protetti=['A2', 'A3r', 'B2i', 'B3a', 'B3b', 'F4'])
    riga("RAd come RA con F4d", compiti_rovescio_A('F4d'), MIE, DURO,
         protetti=['A2', 'A3r', 'B2i', 'B3a', 'B3b', 'F4d'])
    fine, _, _ = simula(compiti_rovescio_A('F4'), MIE, DURO)
    print(f"    RA: scheletro SK chiuso entro l'ora 5: {(fine['SK'] <= 5).mean():.2f}; 6: {(fine['SK'] <= 6).mean():.2f}; "
          f"8: {(fine['SK'] <= 8).mean():.2f}; mediana {np.median(fine['SK']):.2f} h")
    fine, _, _ = simula(compiti_piano(True, 'F4', thl=True), MIE, DURO)
    sk = np.maximum(np.maximum(fine['C1'], fine['D2']), fine['E2'])
    print(f"    S5: schermo + tabellone + banco (C1, D2, E2) tutti chiusi entro l'ora 5: {(sk <= 5).mean():.2f}; "
          f"8: {(sk <= 8).mean():.2f}; mediana {np.median(sk):.2f} h")
    pb, _ = riga("RB  S5 senza LAT (il tempo per ciclo e' una riga del tabellone)", compiti_piano(True, 'F4', thl=True, lat=False),
                 MIE, DURO)
    pc, _ = riga("RC  S5 senza alcun suono (C3a 0,25/0,5/1)", compiti_piano(True, 'F4', thl=True, suono=False), MIE, DURO)
    pab, _ = riga("RA+RB+RC insieme non serve: RA non ha LAT; RA senza suono", compiti_rovescio_A('F4'),
                  dict(MIE, C3a=MIE['C3s']), DURO)
    print(f"\nDifferenze: RA-S5 = {pa - p5:+.3f}; RB-S5 = {pb - p5:+.3f}; RC-S5 = {pc - p5:+.3f}; S5-S2 = {p5 - p2:+.3f}")

    print("\n== 4. Modello medio (fra il leggero del piano e il duro), stime mie")
    riga("M2  piano con i tagli, modello medio", compiti_piano(True), MIE, MEDIO, protetti=PR)
    riga("M5  piano + F4 + THOR ridotto, modello medio", compiti_piano(True, 'F4', thl=True), MIE, MEDIO, protetti=PR4)
    riga("M1  piano con i tagli, STIME DEL PIANO, modello medio", compiti_piano(True), PIANO, MEDIO, protetti=PR)
    print("\n== 5. Calendario alternativo ALT (scheletro prima, B3a spezzato, coda corta)")
    PRA = ['A2', 'F9', 'A3r', 'B2', 'B3a1', 'B3a2']
    for nome, ip in (('leggero', LEGGERO), ('medio', MEDIO), ('duro', DURO)):
        riga(f"ALT   F4 1,5/3/6, cancello all'ora 5, modello {nome}", compiti_alt('F4'), MIE, ip, protetti=PRA + ['F4'],
             dettagli=(nome == 'medio'))
        riga(f"ALTd  F4d 0,5/1/2,5 (non verificato), modello {nome}", compiti_alt('F4d'), MIE, ip, protetti=PRA + ['F4d'])
        riga(f"ALTn  come ALT senza il cancello dell'ora 5, modello {nome}", compiti_alt('F4', False), MIE, ip)
        riga(f"ALTp  ALT con una persona ferma 2 h di sicuro, modello {nome}", compiti_alt('F4'), MIE, ip, fermo_certo=True)
    print("\n== 6. La scala: che cosa c'e' nel tronco al gelo dell'ora 12 (e all'ora 14)")
    pp = [('schermo C1', ['C1']), ('libero A2', ['A2']), ('avviso B3b', ['B3b']), ('regione B2+C2', ['B2', 'C2']),
          ('stati B3a', ['B3a']), ('identita\' F4', ['F4']), ('sensore A3r', ['A3r']), ('tabellone D2', ['D2'])]
    pa = [('scheletro SK', ['SK']), ('libero A2', ['A2']), ('avviso F9', ['F9']), ('regione B2+C2', ['B2', 'C2']),
          ('stati B3a1+B3a2', ['B3a1', 'B3a2']), ('identita\' F4', ['F4']), ('sensore A3r', ['A3r']),
          ('tabellone D2r+D2b', ['D2r', 'D2b'])]
    for nome, ip in (('medio', MEDIO), ('duro', DURO)):
        for ora in (12.0, 14.0):
            scala(f"piano+F4, {nome}", compiti_piano(True, 'F4', thl=True), MIE, ip, pp, ora)
            scala(f"ALT,      {nome}", compiti_alt('F4'), MIE, ip, pa, ora)
    for nome, ip in (('medio', MEDIO), ('duro', DURO)):
        f1, _, _ = simula(compiti_alt('F4'), MIE, ip)
        f2, _, _ = simula(compiti_piano(True, 'F4', thl=True), MIE, ip)
        print(f"    {nome}: ALT, scheletro SK entro l'ora 5: {(f1['SK'] <= 5).mean():.2f}; 8: {(f1['SK'] <= 8).mean():.2f}; "
              f"mediana {np.median(f1['SK']):.2f} h | piano: C1 entro l'ora 8: {(f2['C1'] <= 8).mean():.2f}; "
              f"prima corsa di tutto insieme (PI) entro l'ora 12: {(f2['PI'] <= 12).mean():.2f}; mediana {np.median(f2['PI']):.2f} h")

    # [aggiunto dopo il terzo lancio: confronti a parita' di modello e scala del calendario senza cancello]
    print("\n== 7. Confronti a parita' di modello; scala del calendario alternativo SENZA cancello (ALTn)")
    for nome, ip in (('leggero', LEGGERO), ('medio', MEDIO), ('duro', DURO)):
        a, _ = riga(f"piano + F4 + THOR ridotto, stime mie, modello {nome}", compiti_piano(True, 'F4', thl=True), MIE, ip)
        b, _ = riga(f"  senza LAT (rovesciamento B), modello {nome}", compiti_piano(True, 'F4', thl=True, lat=False), MIE, ip)
        c, _ = riga(f"  senza suono (rovesciamento C), modello {nome}", compiti_piano(True, 'F4', thl=True, suono=False), MIE, ip)
        d, _ = riga(f"  ALT con il cancello dell'ora 5 (rovesciamento A alla lettera), modello {nome}", compiti_alt('F4'), MIE, ip)
        e, _ = riga(f"  ALTn senza cancello, modello {nome}", compiti_alt('F4', False), MIE, ip,
                    protetti=['A2', 'F9', 'A3r', 'B2', 'B3a1', 'B3a2', 'F4'])
        print(f"    differenze sul piano+F4 ({nome}): B {b - a:+.3f}; C {c - a:+.3f}; A alla lettera {d - a:+.3f}; ALTn {e - a:+.3f}")
    pn = [('scheletro SK', ['SK']), ('libero A2', ['A2']), ('avviso F9', ['F9']), ('regione B2+C2', ['B2', 'C2']),
          ('identita\' F4', ['F4']), ('stati B3a1+B3a2', ['B3a1', 'B3a2']), ('sensore A3r', ['A3r']),
          ('tabellone base D2r', ['D2r']), ('righe della regione D2b', ['D2b'])]
    for nome, ip in (('medio', MEDIO), ('duro', DURO)):
        for ora in (12.0, 14.0, 16.0):
            scala(f"ALTn, {nome}", compiti_alt('F4', False), MIE, ip, pn, ora)
