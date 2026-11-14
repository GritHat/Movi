#!/usr/bin/env python3
"""tabelle.py — legge risultati/*.tsv del banco e stampa le tabelle e gli esiti delle soglie del triage.
Python puro. Uso: python3 tabelle.py > risultati/TABELLE.txt"""
import math, os, sys

R = 'risultati'
ONPATH = ['prosegue', 'rallenta', 'sosta', 'torna', 'sostalunga']
OFF = ['svolta', 'lontano']
BEH6 = ['prosegue', 'rallenta', 'sosta', 'torna', 'svolta', 'lontano']
W = {'squadra': dict(zip(BEH6, [60, 10, 10, 10, 5, 5])), 'giurato': dict(zip(BEH6, [30, 10, 20, 20, 10, 10]))}
TAUS = ['0.5', '1.0', '2.0', '3.0', '5.0']
PRED = ['L0-nucleo', 'L1-fermo', 'L2-filtro', 'L2r-filtro-ritagliato', 'L2q-q0.01', 'L3-raggiungibile', 'C-005', 'C-005b',
        'C-004', 'C-004m', 'C-001+C-008', 'C-001+C-009', 'C-EST-A', 'C-EST-B', 'C-EST-A-senzafascia', 'C-EST-B-senzafascia']
REG = [p for p in PRED if p not in ('L1-fermo', 'C-005b', 'C-004m', 'C-001+C-009')]


def kv(fields):
    d = {}
    last = None
    for x in fields:
        if '=' in x:
            k, v = x.split('=', 1)
            if k == 'pass':  # chiavi ripetute «pass=»: prendono il nome della chiave precedente
                k = last + '_pass'
            d[k] = v
            last = k
    return d


def load(name):
    H, P, G, E, M, D = {}, {}, {}, {}, {}, {}
    path = os.path.join(R, name)
    if not os.path.exists(path):
        return None
    for l in open(path):
        f = l.rstrip('\n').split('\t')
        if f[0] == 'H':
            H[(f[3], f[2], f[4])] = kv(f[5:])
        elif f[0] == 'P':
            P[(f[3], f[2])] = kv(f[4:])
        elif f[0] == 'G':
            G[f[2]] = kv(f[3:])
        elif f[0] == 'E':
            E[(f[3], f[2])] = kv(f[4:])
        elif f[0] == 'M':
            M[(f[3], f[2], f[4])] = kv(f[5:])
        elif f[0] == 'D':
            D = kv(f[3:])
    return dict(H=H, P=P, G=G, E=E, M=M, D=D)


def wilson(k, n, z=1.96):
    if n == 0:
        return (float('nan'), float('nan'))
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (c - h, c + h)


def esito_cella(k, n, soglia=0.85):
    if n < 30:
        return 'vuota'
    lo, hi = wilson(k, n)
    if n >= 200:
        return 'regge' if k / n >= soglia else 'smentita'
    if hi < 0.90:
        return 'smentita'
    if lo >= 0.80:
        return 'regge'
    return 'non risolta'


def mix_cov(X, pred, tau, key, mix, denom='n'):
    num = den = 0.0
    for b, w in W[mix].items():
        h = X['H'].get((pred, b, tau))
        nb = int(X['G'][b]['validi']) if b in X['G'] else 0
        if not h or nb == 0:
            continue
        num += w / nb * int(h[key])
        den += w / nb * (int(h[denom]) - int(h['fuori_griglia']))
    return (num / den if den > 0 else float('nan')), den


def fnum(x, fmt='%.2f'):
    return '  -  ' if x != x else fmt % x


def sezione(t):
    print('\n' + '=' * 110 + '\n' + t + '\n' + '=' * 110)


def tab_c1(X, nome):
    sezione('C1 CONTINUITA — %s (comportamenti sul percorso: %s)' % (nome, ', '.join(ONPATH)))
    print('%-24s %9s %9s %8s %8s %8s | %8s %8s %8s | %7s %7s %9s %9s %8s' % ('predittore', 'pass', 'vuoto', 'vuoto>5c', 'cicliReg', 'vuotoMax', 'passi>.167', 'indietro%', 'cicliPt',
                                                                              're40', 're30', 'saltoMed', 'saltoP90', 'salto/r'))
    for p in PRED:
        npass = gap = late = cyc = creg = cpt = step = 0
        vmax = 0
        for b in ONPATH:
            q = X['P'].get((p, b))
            if not q:
                continue
            npass += int(q['npass']); gap += int(q['pass_vuoto']); late += int(q['pass_vuoto_dopo5']); cyc += int(q['cicli']); creg += int(q['cicli_regione'])
            cpt += int(q['cicli_punto']); step += int(q['pass_passi_oltre']); vmax = max(vmax, int(q['vuoto_max']))
        q = X['P'].get((p, 'prosegue'))
        if not q or npass == 0:
            continue
        back = 100.0 * int(q['pass_indietro']) / max(1, int(q['npass']))
        nre = sum(int(X['P'][(p, b)]['nre']) for b in ONPATH); re40 = sum(int(X['P'][(p, b)]['re40']) for b in ONPATH); re30 = sum(int(X['P'][(p, b)]['re30']) for b in ONPATH)
        print('%-24s %9d %9d %8d %7.1f%% %8d | %8d %8.1f%% %7.1f%% | %7.3f %7.3f %9s %9s %8s' % (p, npass, gap, late, 100.0 * creg / cyc, vmax, step, back, 100.0 * cpt / cyc,
                                                                                               re40 / max(1, nre), re30 / max(1, nre), q['salto_med'], q['salto_p90'], q['salto_su_raggio_med']))
    print('  (vuoto = passaggi con almeno un ciclo senza regione; vuoto>5c = dopo i primi 5 cicli; passi>.167 = passaggi con un passo del punto oltre 0,167 m;')
    print('   indietro% = quota dei «prosegue» con un passo all\'indietro oltre 5 cm; re40/re30 = prima misura entro 0,40/0,30 m dalla R90 del ciclo prima; salto: su «prosegue»)')


def tab_c1_beh(X, nome):
    sezione('C1a per comportamento — %s: quota dei cicli senza osservazione con una regione emessa (e passaggi con un vuoto / validi)' % nome)
    print('%-24s ' % 'predittore' + ' '.join('%18s' % b for b in ONPATH + OFF))
    for p in REG:
        row = []
        for b in ONPATH + OFF:
            q = X['P'].get((p, b))
            row.append('%5.1f%% (%3d/%3d)' % (100.0 * int(q['cicli_regione']) / max(1, int(q['cicli'])), int(q['pass_vuoto']), int(q['npass'])) if q else '-')
        print('%-24s ' % p + ' '.join('%18s' % r for r in row))


def tab_c2(X, nome):
    sezione('C2 EFFICACIA — %s: errore del punto, mediana (90º percentile), metri' % nome)
    for mix in ('squadra', 'giurato'):
        print('miscela «%s»' % mix)
        print('%-24s ' % 'predittore' + ' '.join('%15s' % ('τ=' + t) for t in TAUS))
        for p in PRED:
            row = []
            for t in TAUS:
                m = X['M'].get((p, mix, t))
                row.append('%5s (%5s)' % (m['err_med'], m['err_p90']) if m else '-')
            print('%-24s ' % p + ' '.join('%15s' % r for r in row))
    print('peggior rapporto con la migliore base (L1, L2) per cella comportamento × τ, n >= 30, mediana; e orizzonte del punto (primo τ in cui perde con L1 sulla «squadra»)')
    for p in PRED:
        if p in ('L1-fermo', 'L2-filtro'):
            continue
        worst = (0, '')
        for b in ONPATH + OFF:
            for t in TAUS:
                h = X['H'].get((p, b, t)); h1 = X['H'].get(('L1-fermo', b, t)); h2 = X['H'].get(('L2-filtro', b, t))
                if not h or int(h['npt']) < 30 or h['err_med'] == 'nan':
                    continue
                base = min(float(h1['err_med']), float(h2['err_med']))
                r = float(h['err_med']) / max(base, 0.05)
                if r > worst[0]:
                    worst = (r, '%s τ=%s (%.2f contro %.2f m)' % (b, t, float(h['err_med']), base))
        oriz = '-'
        for t in TAUS:
            m = X['M'].get((p, 'squadra', t)); m1 = X['M'].get(('L1-fermo', 'squadra', t))
            if m and m1 and float(m['err_med']) > float(m1['err_med']):
                oriz = t
                break
        print('  %-24s peggior rapporto %.2f in %s; perde con L1 da τ = %s' % (p, worst[0], worst[1], oriz))


def tab_c3(X, nome):
    sezione('C3 TARATURA — %s: copertura di R90 per comportamento e τ (dentro / n nascosti a τ e dentro la griglia); * = cella sotto soglia; vuota se n < 30' % nome)
    print('quota dei nascosti a τ che sono fuori dalla griglia («non osservato»: oltre la portata o il campo), τ = ' + ', '.join(TAUS) + ': ' + '; '.join('%s %s' % (b, ' '.join('%.2f' % (int(X['H'][('L3-raggiungibile', b, t)]['fuori_griglia']) / max(1, int(X['H'][('L3-raggiungibile', b, t)]['n']))) for t in TAUS)) for b in ONPATH + OFF))
    for p in REG:
        print(p)
        for b in ONPATH + OFF:
            row = []
            for t in TAUS:
                h = X['H'].get((p, b, t))
                if not h or int(h['n']) - int(h['fuori_griglia']) < 30:
                    row.append('%16s' % '(n<30)')
                    continue
                n = int(h['n']) - int(h['fuori_griglia']); k = int(h['in90']); e = esito_cella(k, n)
                row.append('%5.3f %3d/%3d%s' % (k / n, k, n, {'regge': ' ', 'smentita': '*', 'non risolta': '?'}[e]))
            print('   %-11s ' % b + '  '.join('%16s' % r for r in row))
    sezione('C3 riassunto — %s' % nome)
    print('%-24s | %-44s | %-23s | %-29s | %-29s | %-23s' % ('predittore', 'minimo R90 sul percorso fino a 3 s [Wilson 95 %]', 'celle<0,85 (3 s / 5 s)', 'R90 «squadra» τ=.5,1,2,3,5', 'R50 «squadra» τ=.5,1,2,3,5', 'R90 «giurato»'))
    for p in REG:
        mn = (2, None); below3 = below5 = cells3 = cells5 = 0
        for b in ONPATH:
            for t in TAUS:
                h = X['H'].get((p, b, t))
                if not h or int(h['n']) - int(h['fuori_griglia']) < 30:
                    continue
                n = int(h['n']) - int(h['fuori_griglia']); k = int(h['in90']); e = esito_cella(k, n)
                cells5 += 1; below5 += e == 'smentita'
                if t != '5.0':
                    cells3 += 1; below3 += e == 'smentita'
                    if k / n < mn[0]:
                        mn = (k / n, (b, t, k, n))
        if mn[1] is None:
            continue
        lo, hi = wilson(mn[1][2], mn[1][3])
        sq90 = ' '.join(fnum(mix_cov(X, p, t, 'in90', 'squadra')[0]) for t in TAUS)
        sq50 = ' '.join(fnum(mix_cov(X, p, t, 'in50', 'squadra')[0]) for t in TAUS)
        gi90 = ' '.join(fnum(mix_cov(X, p, t, 'in90', 'giurato')[0]) for t in TAUS)
        print('%-24s | %5.3f %-10s τ=%s %3d/%3d [%.3f-%.3f] | %2d/%2d  %2d/%2d          | %-29s | %-29s | %-23s' % (p, mn[0], mn[1][0], mn[1][1], mn[1][2], mn[1][3], lo, hi, below3, cells3, below5, cells5, sq90, sq50, gi90))
    print('\nfuori percorso: copertura di R90 e di R100 (τ = 1 / 2 / 3 / 5 s) per «svolta» e «lontano»')
    for p in REG:
        row = []
        for b in OFF:
            c90 = []; c100 = []
            for t in TAUS[1:]:
                h = X['H'].get((p, b, t))
                if h and int(h['n']) - int(h['fuori_griglia']) >= 30:
                    c90.append('%.2f' % (int(h['in90']) / (int(h['n']) - int(h['fuori_griglia'])))); c100.append('%.3f' % (int(h['in100']) / int(h['n'])))
                else:
                    c90.append(' - '); c100.append('  -  ')
            row.append('%s: R90 %s | R100 %s' % (b, ' '.join(c90), ' '.join(c100)))
        print('  %-24s %s' % (p, '   '.join(row)))
    print('\narea di R90 / ombra stimata, media sui comportamenti sul percorso con n >= 30 (massimo fra i comportamenti), per τ; e punteggio logaritmico medio sulla «squadra» (piu\' basso e\' meglio)')
    for p in REG:
        row = []; sc = []
        for t in TAUS:
            v = []
            for b in ONPATH:
                h = X['H'].get((p, b, t))
                if h and int(h['nreg']) >= 30:
                    v.append(float(h['area90']) / float(h['ombra']))
            row.append('%.2f (%.2f)' % (sum(v) / len(v), max(v)) if v else '    -      ')
            num = den = 0
            for b, w in W['squadra'].items():
                h = X['H'].get((p, b, t)); nb = int(X['G'][b]['validi'])
                if h and h['punteggio'] != 'nan' and int(h['n']) > 0:
                    num += w / nb * int(h['n']) * float(h['punteggio']); den += w / nb * int(h['n'])
            sc.append('%5.2f' % (num / den) if den else '  -  ')
        print('  %-24s area: %s   punteggio: %s' % (p, '  '.join(row), ' '.join(sc)))


def tab_c4(X, nome):
    sezione('C4 INCERTEZZA CONTROLLATA — %s (tutti i comportamenti 0-6)' % nome)
    allb = ONPATH + OFF
    print('%-24s %10s %14s %14s %14s %12s | %8s %8s %8s' % ('predittore', 'cicli', 'R90 su libero', 'punto su lib.', 'R90 fuori R100', 'reg. oltre 3s', 'ampio>1/2', 'ampio>80%', 'r>0,8 m'))
    for p in PRED:
        cyc = fr = frp = pt = ptp = n1 = n1p = w5 = w8 = w08 = creg = 0
        for b in allb:
            q = X['P'].get((p, b))
            if not q:
                continue
            cyc += int(q['cicli']); creg += int(q['cicli_regione']); fr += int(q['R90_su_libero_cicli']); frp += int(q['R90_su_libero_cicli_pass']); pt += int(q['punto_su_libero_cicli']); ptp += int(q['punto_su_libero_cicli_pass'])
            n1 += int(q['R90_fuori_R100_cicli']); n1p += int(q['R90_fuori_R100_cicli_pass']); w5 += int(q['ampio50']); w8 += int(q['ampio80']); w08 += int(q['ampio08m'])
        if cyc == 0:
            continue
        k3 = n3 = 0
        for b in allb:
            for t in ('3.0', '5.0'):
                h = X['H'].get((p, b, t))
                if h:
                    k3 += int(h['nreg']); n3 += int(h['n'])
        print('%-24s %10d %6d c %4d p %6d c %4d p %6d c %4d p %11.1f%% | %7.1f%% %7.1f%% %7.1f%%' % (p, cyc, fr, frp, pt, ptp, n1, n1p, 100.0 * k3 / max(1, n3), 100.0 * w5 / max(1, creg), 100.0 * w8 / max(1, creg), 100.0 * w08 / max(1, creg)))
    g = X['G']
    print('il ritaglio toglie il vero (passaggi con almeno un ciclo nascosto in cui la cella del vero e\' «vista libera oltre la fascia»): ' +
          ', '.join('%s %s/%s' % (b, g[b]['pass_vero_fuori_A'], g[b]['validi']) for b in allb if b in g))
    print('   lo stesso senza fascia (cella del vero fuori dall\'ombra stimata): ' + ', '.join('%s %s/%s' % (b, g[b]['pass_vero_fuori_ombra'], g[b]['validi']) for b in allb if b in g))
    print('   cicli nascosti / cicli con rilevamento mancato in vista: ' + ', '.join('%s %s/%s' % (b, g[b]['cicli_nascosti'], g[b]['cicli_mancati_in_vista']) for b in allb if b in g))
    print('   scartati (traccia non confermata prima del buio): ' + ', '.join('%s %s' % (b, g[b]['scartati']) for b in allb if b in g))


def tab_est(X, nome):
    sezione('C-EST — %s: stati per ciclo e per passaggio' % nome)
    for b in ONPATH + OFF + ['attacco1', 'tripla', 'due']:
        for v in ('C-EST-A', 'C-EST-B', 'C-EST-A-senzafascia', 'C-EST-B-senzafascia'):
            e = X['E'].get((v, b))
            if e:
                tot = int(e['cicli_previsto']) + int(e['cicli_perso']) + int(e['cicli_vuoto'])
                print('  %-11s %-22s previsto %5.1f%%  perso %5.1f%%  vuoto %5.2f%% | passaggi con «perso» %s, con regione vuota %s, con transito dominante oltre 0,5 s dopo l\'uscita attesa %s (cicli %s) | n=%s' % (
                    b, v, 100.0 * int(e['cicli_previsto']) / tot, 100.0 * int(e['cicli_perso']) / tot, 100.0 * int(e['cicli_vuoto']) / tot, e['pass_perso'], e['pass_vuoto'], e['pass_transito_dominante_tardi'], e['cicli_dominante_tardi'], X['G'][b]['validi']))


def tab_att5(X, nome):
    sezione('ATTACCO 5 — %s: la prima misura alla ricomparsa sta nella regione al 95 %% dichiarata? (L2: innovazione normalizzata del filtro; C-EST: ellisse dei momenti ritagliati)' % nome)
    for p in ('L2-filtro', 'L2q-q0.01', 'C-EST-A', 'C-EST-B', 'C-EST-A-senzafascia', 'C-EST-B-senzafascia'):
        row = []
        num = den = 0.0
        for b in BEH6:
            q = X['P'].get((p, b))
            if not q:
                continue
            k, n = q['porta95'].split('/')
            k = int(k); n = int(n)
            lo, hi = wilson(k, n)
            row.append('%s %d/%d=%.3f' % (b, k, n, k / max(1, n)))
            nb = int(X['G'][b]['validi'])
            num += W['squadra'][b] / nb * k; den += W['squadra'][b] / nb * n
        q = X['P'].get((p, 'prosegue')); k, n = [int(x) for x in q['porta95'].split('/')]; lo, hi = wilson(k, n)
        print('  %-22s «prosegue» %.3f [%.3f-%.3f]  «squadra» %.3f | %s' % (p, k / max(1, n), lo, hi, num / den if den else float('nan'), '; '.join(row)))


def main():
    runs = [('prova_D_pd09.tsv', 'D, rilevamento 0,9'), ('prova_T_pd09.tsv', 'T, rilevamento 0,9'), ('prova_L_pd09.tsv', 'L (mai tarata), rilevamento 0,9'),
            ('prova_D_pd10.tsv', 'D, rilevamento 1'), ('prova_T_pd10.tsv', 'T, rilevamento 1'), ('prova_L_pd10.tsv', 'L, rilevamento 1'),
            ('braccio_T_ombra-20_fascia.tsv', 'BRACCIO T, ombra stimata a -20 cm, fascia 0,20'), ('braccio_T_ombra-20_senzafascia.tsv', 'BRACCIO T, ombra stimata a -20 cm, SENZA fascia (deve fallire)'),
            ('braccio_T_pd07.tsv', 'BRACCIO T, rilevamento 0,7'), ('braccio_T_rumore_curva.tsv', 'BRACCIO T, rumore 4/9/16 cm a 2/3/4 m, filtro e taratura fermi a 5 cm'),
            ('braccio_T_rumore_curva_noto.tsv', 'BRACCIO T, rumore 4/9/16 cm, R del filtro dalla curva e taratura rifatta con quel rumore')]
    for f, nome in runs:
        X = load(f)
        if not X:
            continue
        tab_c1(X, nome); tab_c1_beh(X, nome); tab_c2(X, nome); tab_c3(X, nome); tab_c4(X, nome); tab_est(X, nome); tab_att5(X, nome)
        g = X['G'].get('prosegue')
        if g:
            sezione('K-202 / K-211 — %s' % nome)
            for b in ONPATH:
                gg = X['G'][b]
                print('  %-11s L0: «perso» prima della ricomparsa in %s su %s ricomparsi; durata del «previsto» mediana %s s (quartili %s - %s)' % (b, gg['L0_perso_prima'], gg['ricomparsi'], gg['L0_durata_previsto_med'], gg['q25'], gg['q75']))
    for g in 'DT':
        X = load('attacco1_%s.tsv' % g)
        if X:
            sezione('ATTACCO 1 — sosta improvvisa a meta\' pannello dopo l\'ingresso a 1,2 m/s, %s, 200 semi (9500-9699)' % g)
            tab_est(X, 'attacco 1, ' + g)
            print('  quota dei cicli nascosti fra 0,5 e 3 s con il vero nella R90; cicli con R90 su celle viste libere oltre la fascia; passaggi con un vuoto')
            for p in PRED:
                q = X['P'].get((p, 'attacco1'))
                if q and int(q['cicli0530']) > 0:
                    print('    %-24s %.3f (%s/%s)   R90 su libero: %s cicli   punto su libero: %s cicli   vuoti: %s/%s passaggi (dopo 5 cicli: %s)' % (p, int(q['dentro0530']) / int(q['cicli0530']), q['dentro0530'], q['cicli0530'], q['R90_su_libero_cicli'], q['punto_su_libero_cicli'], q['pass_vuoto'], q['npass'], q['pass_vuoto_dopo5']))
            print('  copertura R90 per τ: ' + ' | '.join('%s: %s' % (p, ' '.join('%.2f' % (int(X['H'][(p, 'attacco1', t)]['in90']) / max(1, int(X['H'][(p, 'attacco1', t)]['n']))) for t in TAUS)) for p in ('L0-nucleo', 'C-005', 'C-004', 'C-001+C-008', 'C-EST-A', 'C-EST-B')))
        X = load('attacco2_%s.tsv' % g)
        if X:
            sezione('ATTACCO 2 — %s, 200 semi (9700-9899)' % g)
            gg = X['G']['tripla']
            print('  «esce a velocita\' tripla»: ricomparsi %s; il nucleo (regola geometrica C1) riaggancia %s' % (gg['ricomparsi'], gg['C1_riaggancio']))
            for p in PRED:
                q = X['P'].get((p, 'tripla'))
                if q:
                    print('    %-24s prima misura entro 0,40 m dalla R90: %s/%s   porta al 95 %%: %s   salto mediano %s m' % (p, q['re40'], q['nre'], q['porta95'], q['salto_med']))
            d = X['D']
            print('  «entra uno, escono due» (il primo resta fermo nell\'ombra; uno sconosciuto mai tracciato esce dal lato lontano): eventi %s; esce prima lo sconosciuto %s; il nucleo lo riaggancia con l\'identita\' del primo %s; R100 tolta a soggetto ancora nascosto (regola del nucleo: rilascio al riaggancio) %s' % (
                d['eventi'], d['esce_prima_lo_sconosciuto'], d['nucleo_riaggancia_lo_sconosciuto'], d['R100_tolta_a_soggetto_nascosto']))
            print('    lo sconosciuto cade entro 0,40 m dalla R90 del predittore: ' + ', '.join('%s %s' % (p, d[p]) for p in PRED if p in d))
    p = os.path.join(R, 'tempi.txt')
    if os.path.exists(p):
        sezione('C6 COSTO — tempi per ciclo (C, -O2, un filo; macchina condivisa: indicativi)')
        sys.stdout.write(open(p).read())
    p = os.path.join(R, 'taratura_esito.txt')
    if os.path.exists(p):
        sezione('TARATURA (semi 1000-1199, D e T, rilevamento 0,9)')
        sys.stdout.write(open(p).read())


main()
