#!/usr/bin/env python3
"""Falsificatori del rovesciatore, f8 (continuita' visiva). Python puro, semi fissati.
Uso (dalla cartella 08-rovesciatore):
    timeout 120 python3 -B rov_f8.py
Importa IN SOLA LETTURA la scena dell'avversario del torneo (f2/04-torneo/scena_parte3.py):
generatore `truth`, visibilita' `vis`, filtro `KF`, griglia. `-B` evita di scrivere __pycache__ la'.
"""
import math, os, random, sys
QUI = os.path.dirname(os.path.abspath(__file__))
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.normpath(os.path.join(QUI, '..', '..', 'f2', '04-torneo')))
import scena_parte3 as sp

DT = sp.DT; SIG = sp.SIG; PD = sp.PD; CELL = sp.CELL
BEHS = ('prosegue', 'sosta', 'torna', 'lontano')
TB = (0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0)          # tempi senza osservazione (s)
KB = {round(t / DT): t for t in TB}               # ciclo -> tempo
K50 = math.sqrt(1.386); K90 = math.sqrt(4.605); K95 = math.sqrt(5.991)
CAP = int(5.4 / DT)
NMIN = 30


def trial(beh, w, rng):
    """Un passaggio. Restituisce i cicli a soggetto in ombra e l'eventuale ricomparsa."""
    tr = sp.truth(beh, w, rng)
    kf = None; zp = None; kp = None; zl = None; kl = None; k0 = None
    hid = []; re = None; vin = None
    for k, (x, y) in enumerate(tr):
        vt = sp.vis(x, y, w)
        det = vt == 1 and rng.random() < PD
        z = (x + rng.gauss(0, SIG), y + rng.gauss(0, SIG)) if det else None
        if kf is None:
            if det:
                if zp is None: zp, kp = z, k
                else: kf = sp.KF(zp, z, k - kp); zl, kl = z, k
            continue
        kf.predict()
        if k0 is None and vt != 1: k0 = k
        if det:
            if k0 is not None:
                re = {'k': k, 'z': z, 'dj': math.hypot(z[0] - kf.x, z[1] - kf.y) / math.sqrt(kf.a + sp.R), 'tau': (k - kl) * DT}
                break
            kf.update(z); zl, kl = z, k; vin = math.hypot(kf.vx, kf.vy)
        elif k0 is not None and vt == 2:
            hid.append({'k': k, 'j': k - kl, 'x': x, 'y': y, 'mx': kf.x, 'my': kf.y, 'a': kf.a,
                        'dn': math.hypot(x - kf.x, y - kf.y) / math.sqrt(kf.a),
                        'dl': math.hypot(x - zl[0], y - zl[1]), 'zl': zl, 'kl': kl})
        if k0 is not None and k - k0 >= CAP: break
    return {'beh': beh, 'hid': hid, 're': re, 'k0': k0, 'vin': vin, 'zl': zl}


def run(w, n, seed):
    out = {}
    for bi, beh in enumerate(BEHS):
        rng = random.Random(seed + bi)
        out[beh] = [trial(beh, w, rng) for _ in range(n)]
    return out


def quant(v, p):
    v = sorted(v)
    if not v: return float('nan')
    i = min(len(v) - 1, max(0, math.ceil(p * (len(v) + 1)) - 1))   # quantile conforme (n+1)
    return v[i]


def wilson(k, n, z=1.96):
    if n == 0: return (float('nan'), float('nan'))
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (100 * (c - h), 100 * (c + h))


def at(rs, j):
    """Un ciclo per prova: quello con tempo senza osservazione = j cicli (se il soggetto e' ancora in ombra)."""
    return [h for r in rs for h in r['hid'] if h['j'] == j]


def shadow_share(cx, cy, rad, w):
    gt, nsh = sp.grid(w)
    n, nf, ns, _ = sp.circ(cx, cy, rad, gt)
    return ns / nsh, nf / max(n, 1)


def pct(k, n): return '   n/d' if n == 0 else '%5.1f%%' % (100.0 * k / n)


def main():
    S = 20261114
    print('# rov_f8.py  seme base %d; scena dell\'avversario (scena_parte3.py): dt 1/15 s, sigma 5 cm, Pd %.1f, q %.1f' % (S, PD, sp.Q))
    NT = 300
    tune = run(1.0, NT, S + 8100)      # taratura: pannello 1 m
    test1 = run(1.0, NT, S + 8200)     # prova: pannello 1 m, altri semi
    test2 = run(2.0, NT, S + 8300)     # prova: pannello 2 m (altra geometria)

    # ---------------- T1a: la regola del nucleo (strato 2 fino a meta' dell'ombra, poi perso) ----------------
    print('\n== T1a. Regola del nucleo V2 (cerchio 95 %% ritagliato sull\'ombra, mostrato finche\' < meta\' dell\'ombra): quota dei cicli in ombra con una stima emessa ==')
    print('pannello  comportamento  prove  cicli_in_ombra  emessi   quota   durata_previsto_mediana_s  durata_ombra_mediana_s  vuoto_mediano_s')
    for lab, w, data in (('1 m', 1.0, test1), ('2 m', 2.0, test2)):
        gt, nsh = sp.grid(w); tot_c = tot_e = 0
        for beh in BEHS:
            nc = ne = 0; durp = []; duro = []; gap = []
            for r in data[beh][:120]:
                if not r['hid']: continue
                on = True; e = 0
                for h in r['hid']:
                    if on:
                        rho = K95 * math.sqrt(h['a'])
                        n_, nf, ns, _ = sp.circ(h['mx'], h['my'], rho, gt)
                        if ns >= 0.5 * nsh: on = False
                    if on: e += 1
                nc += len(r['hid']); ne += e; durp.append(e * DT); duro.append(len(r['hid']) * DT); gap.append((len(r['hid']) - e) * DT)
            tot_c += nc; tot_e += ne
            med = lambda v: sorted(v)[len(v) // 2] if v else float('nan')
            print('%-8s  %-13s  %5d  %14d  %6d  %s   %24.2f  %22.2f  %15.2f' % (lab, beh, len(durp), nc, ne, pct(ne, nc), med(durp), med(duro), med(gap)))
        print('%-8s  %-13s         %14d  %6d  %s' % (lab, 'TUTTI', tot_c, tot_e, pct(tot_e, tot_c)))

    # ---------------- T1b: cerchio nominale tenuto acceso: copertura per comportamento e tempo ----------------
    print('\n== T1b. Cerchio nominale del Kalman (q=0,2) tenuto acceso: copertura vera al 50 %% e al 90 %% per comportamento e tempo (pannello 1 m, semi di prova) ==')
    print('t_s   ' + '   '.join('%-22s' % b for b in BEHS))
    for j, t in sorted(KB.items()):
        row = []
        for beh in BEHS:
            hs = at(test1[beh], j); n = len(hs)
            c5 = sum(h['dn'] <= K50 for h in hs); c9 = sum(h['dn'] <= K90 for h in hs)
            row.append('%s/%s n=%-3d   ' % (pct(c5, n).strip(), pct(c9, n).strip(), n))
        print('%.1f   ' % t + '   '.join('%-22s' % x for x in row))

    # ---------------- T1c/d/e: regioni tarate sul comportamento peggiore, due centri ----------------
    cal = {}
    for j, t in sorted(KB.items()):
        qa = {}; qb = {}
        for beh in BEHS:
            hs = at(tune[beh], j)
            if len(hs) >= NMIN:
                qa[beh] = (quant([h['dn'] for h in hs], .5), quant([h['dn'] for h in hs], .9))
                qb[beh] = (quant([h['dl'] for h in hs], .5), quant([h['dl'] for h in hs], .9))
        if qa:
            cal[j] = {'a50': max(v[0] for v in qa.values()), 'a90': max(v[1] for v in qa.values()),
                      'b50': max(v[0] for v in qb.values()), 'b90': max(v[1] for v in qb.values()), 'behs': sorted(qa)}
    print('\n== T1c. Taratura sul comportamento peggiore (pannello 1 m, semi di taratura). A = centro a velocita\' costante, raggio = k*sigma(t); B = centro sull\'ultima osservazione, raggio in metri ==')
    print('t_s   kA50   kA90  (nominali %.2f / %.2f)   rB50_m  rB90_m   comportamenti con n>=%d in taratura' % (K50, K90, NMIN))
    for j, t in sorted(KB.items()):
        if j in cal: c = cal[j]; print('%.1f   %5.2f  %5.2f                            %5.2f   %5.2f    %s' % (t, c['a50'], c['a90'], c['b50'], c['b90'], ','.join(c['behs'])))
        else: print('%.1f   nessun comportamento con n>=%d' % (t, NMIN))

    for lab, w, data in (('1 m (stessa geometria, altri semi)', 1.0, test1), ('2 m (ALTRA geometria)', 2.0, test2)):
        print('\n== T1c/d/e. Prova sul pannello %s: copertura vera al 90 %% per comportamento [IC 95 %% di Wilson], e quota d\'ombra coperta dalla regione al 50 / 90 %% (regione = disco ritagliato sul non osservato) ==' % lab)
        print('t_s  centro  ' + '  '.join('%-24s' % b for b in BEHS) + '  ombra50%  ombra90%  su_libero_prima_del_ritaglio90%')
        for j, t in sorted(KB.items()):
            if j not in cal: continue
            c = cal[j]
            for cen in ('A', 'B'):
                row = []; s50 = []; s90 = []; fr = []
                for beh in BEHS:
                    hs = at(data[beh], j); n = len(hs)
                    if cen == 'A': k = sum(h['dn'] <= c['a90'] for h in hs)
                    else: k = sum(h['dl'] <= c['b90'] for h in hs)
                    lo, hi = wilson(k, n)
                    row.append('%s [%3.0f-%3.0f] n=%-3d' % (pct(k, n).strip(), lo, hi, n) if n else 'n=0')
                    for h in hs[:25]:
                        if cen == 'A':
                            a5 = shadow_share(h['mx'], h['my'], c['a50'] * math.sqrt(h['a']), w); a9 = shadow_share(h['mx'], h['my'], c['a90'] * math.sqrt(h['a']), w)
                        else:
                            a5 = shadow_share(h['zl'][0], h['zl'][1], c['b50'], w); a9 = shadow_share(h['zl'][0], h['zl'][1], c['b90'], w)
                        s50.append(a5[0]); s90.append(a9[0]); fr.append(a9[1])
                mean = lambda v: 100 * sum(v) / len(v) if v else float('nan')
                print('%.1f  %s       ' % (t, cen) + '  '.join('%-24s' % x for x in row) + '  %6.1f    %6.1f    %6.1f' % (mean(s50), mean(s90), mean(fr)))

    # controllo per costruzione: regione al 100 % = disco v_max dall'ultima osservazione
    tot = bad = 0
    for data in (test1, test2):
        for beh in BEHS:
            for r in data[beh]:
                for h in r['hid']:
                    tot += 1; bad += h['dl'] > sp.VMAX * h['j'] * DT + 3 * SIG
    print('\n== Controllo per costruzione: soggetto in ombra fuori dal disco di v_max (%.1f m/s) dall\'ultima osservazione: %d cicli su %d ==' % (sp.VMAX, bad, tot))

    # ---------------- T2: taratura all'indietro dalla ricomparsa ----------------
    print('\n== T2a. Ricomparse per comportamento (pannello 1 m, semi di prova; entro %.1f s dall\'ingresso) ==' % (CAP * DT))
    print('comportamento  prove  con_ombra  ricomparsi  quota   tau_mediano_s   salto<=k50  salto<=k90 (cerchio nominale)')
    for beh in BEHS:
        rs = [r for r in test1[beh] if r['hid']]; rr = [r['re'] for r in rs if r['re']]
        taus = sorted(x['tau'] for x in rr)
        print('%-13s  %5d  %9d  %10d  %s   %13s   %s      %s' % (beh, len(test1[beh]), len(rs), len(rr), pct(len(rr), len(rs)), ('%.2f' % taus[len(taus) // 2]) if taus else 'n/d',
              pct(sum(x['dj'] <= K50 for x in rr), len(rr)), pct(sum(x['dj'] <= K90 for x in rr), len(rr))))
    dj = [r['re']['dj'] for beh in BEHS for r in tune[beh] if r['re'] and r['hid']]
    l50 = quant(dj, .5); l90 = quant(dj, .9)
    print('\n== T2b. Scala ricavata dai salti alla ricomparsa (taratura, comportamenti mescolati, n=%d): k50=%.2f k90=%.2f (nominali %.2f / %.2f). Copertura vera nei cicli in ombra, semi di prova, pannello 1 m ==' % (len(dj), l50, l90, K50, K90))
    print('t_s   ' + '   '.join('%-26s' % b for b in BEHS) + '   (50 % / 90 %)')
    for j, t in sorted(KB.items()):
        row = []
        for beh in BEHS:
            hs = at(test1[beh], j); n = len(hs)
            row.append('%s/%s n=%-3d' % (pct(sum(h['dn'] <= l50 for h in hs), n).strip(), pct(sum(h['dn'] <= l90 for h in hs), n).strip(), n))
        print('%.1f   ' % t + '   '.join('%-26s' % x for x in row))

    print('\n== T2c. Copertura durante il nascosto stimata ALL\'INDIETRO con il ponte rettilineo (ultima osservazione -> prima misura alla ricomparsa) contro la copertura VERA; cerchio nominale; solo prove con ricomparsa; tutti i cicli in ombra ==')
    print('pannello  comportamento  prove  cicli   vera50   ponte50   scarto50   vera90   ponte90   scarto90   errore_medio_del_ponte_m')
    for lab, data in (('1 m', test1), ('2 m', test2)):
        for beh in BEHS:
            n = t5 = b5 = t9 = b9 = 0; np_ = 0; eb = 0.0
            for r in data[beh]:
                if not (r['re'] and r['hid']): continue
                np_ += 1; z = r['re']['z']; kr = r['re']['k']
                for h in r['hid']:
                    f = (h['k'] - h['kl']) / (kr - h['kl']); bx = h['zl'][0] + f * (z[0] - h['zl'][0]); by = h['zl'][1] + f * (z[1] - h['zl'][1])
                    db = math.hypot(bx - h['mx'], by - h['my']) / math.sqrt(h['a'])
                    n += 1; t5 += h['dn'] <= K50; t9 += h['dn'] <= K90; b5 += db <= K50; b9 += db <= K90; eb += math.hypot(bx - h['x'], by - h['y'])
            if n == 0: print('%-8s  %-13s  %5d  %5d   nessuna ricomparsa' % (lab, beh, np_, n)); continue
            print('%-8s  %-13s  %5d  %5d   %s   %s   %+6.1f     %s   %s   %+6.1f     %.2f' % (lab, beh, np_, n, pct(t5, n), pct(b5, n), 100.0 * (b5 - t5) / n, pct(t9, n), pct(b9, n), 100.0 * (b9 - t9) / n, eb / n))

    # ---------------- T2d [dopo]: la scala dipende dalla miscela vista ----------------
    mix = {'prosegue': 0.90, 'sosta': 0.05, 'torna': 0.05}
    pts = []
    for beh, wgt in mix.items():
        v = [r['re']['dj'] for r in tune[beh] if r['re'] and r['hid']]
        pts += [(d, wgt / len(v)) for d in v]
    pts.sort()
    def wq(p):
        acc = 0.0
        for d, wg in pts:
            acc += wg
            if acc >= p: return d
        return pts[-1][0]
    m50 = wq(.5); m90 = wq(.9)
    print('\n== T2d [dopo]. Scala dai salti alla ricomparsa con miscela 90 %% prosegue, 5 %% sosta, 5 %% torna (quantile pesato): k50=%.2f k90=%.2f (nominali %.2f / %.2f). Copertura vera nei cicli in ombra, semi di prova, pannello 1 m ==' % (m50, m90, K50, K90))
    print('t_s   ' + '   '.join('%-26s' % b for b in BEHS) + '   (50 % / 90 %)')
    for j, t in sorted(KB.items()):
        row = []
        for beh in BEHS:
            hs = at(test1[beh], j); n = len(hs)
            row.append('%s/%s n=%-3d' % (pct(sum(h['dn'] <= m50 for h in hs), n).strip(), pct(sum(h['dn'] <= m90 for h in hs), n).strip(), n))
        print('%.1f   ' % t + '   '.join('%-26s' % x for x in row))

    # ---------------- T3: il danno dell'imperativo alla lettera: il punto fluido a velocita' costante ----------------
    print('\n== T3. Il punto a velocita\' costante (media del Kalman) mentre il soggetto e\' in ombra, pannello 1 m, semi di prova: quota su cella VISTA LIBERA / fuori campo o portata; distanza mediana dal soggetto (m) ==')
    print('t_s   ' + '   '.join('%-34s' % b for b in BEHS))
    for j, t in sorted(KB.items()):
        row = []
        for beh in BEHS:
            hs = at(test1[beh], j); n = len(hs)
            if n == 0: row.append('n=0'); continue
            fl = sum(sp.vis(h['mx'], h['my'], 1.0) == 1 for h in hs); no = sum(sp.vis(h['mx'], h['my'], 1.0) == 0 for h in hs)
            ds = sorted(math.hypot(h['mx'] - h['x'], h['my'] - h['y']) for h in hs)
            row.append('%s / %s  d=%.2f n=%-3d' % (pct(fl, n).strip(), pct(no, n).strip(), ds[len(ds) // 2], n))
        print('%.1f   ' % t + '   '.join('%-34s' % x for x in row))

    # ---------------- T2e [dopo]: all'indietro si etichetta il comportamento (lato e ritardo), non il percorso ----------------
    print('\n== T2e [dopo]. Etichetta del comportamento ricavata alla ricomparsa (lato; ritardo rispetto a 1,5 x larghezza dell\'ombra / velocita\' stimata all\'ingresso); semi di prova ==')
    print('pannello  vero       prove   ->prosegue  ->sosta  ->torna  ->non_ricomparso   giuste')
    for lab, w, data in (('1 m', 1.0, test1), ('2 m', 2.0, test2)):
        width = w * 4.0 / sp.YP
        for beh in BEHS:
            c = {'prosegue': 0, 'sosta': 0, 'torna': 0, 'non': 0}; n = 0
            for r in data[beh]:
                if not r['hid'] or not r['vin']: continue
                n += 1
                if r['re'] is None: c['non'] += 1; continue
                z = r['re']['z']; far = (z[0] - r['zl'][0]) > width / 2
                if not far: c['torna'] += 1
                elif r['re']['tau'] <= 1.5 * width / max(r['vin'], 0.1): c['prosegue'] += 1
                else: c['sosta'] += 1
            ok = c['non'] if beh == 'lontano' else c[beh]
            print('%-8s  %-9s  %5d   %9d  %7d  %7d  %15d   %s' % (lab, beh, n, c['prosegue'], c['sosta'], c['torna'], c['non'], pct(ok, n)))


if __name__ == '__main__':
    main()
