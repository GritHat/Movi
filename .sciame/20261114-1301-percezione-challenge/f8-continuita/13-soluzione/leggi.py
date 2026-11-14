# Legge ris/prova_{D,T,L}.tsv (uscita di comp) e stampa le misure delle previsioni P-sd-1..10. Sola lettura.
import sys, math
PRED = ['L1-fermo', 'L2-filtro', 'C-005', 'C-004', 'C-004m', 'C-001+C-008', 'C-001+C-009', 'sd-1', 'sd-0']
ONPATH = ['prosegue', 'rallenta', 'sosta', 'torna', 'sostalunga']
ALL = ONPATH[:4] + ['svolta', 'lontano', 'sostalunga']
def kv(fields):
    d = {}
    for f in fields:
        if '=' in f:
            k, v = f.split('=', 1); d.setdefault(k, []).append(v)
    return d
def wilson(k, n, z=1.96):
    if n == 0: return (float('nan'),) * 2
    p = k / n; den = 1 + z * z / n; c = p + z * z / (2 * n); h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - h) / den, (c + h) / den)
for g in sys.argv[1:] or ['D', 'T', 'L']:
    P, H, M = {}, {}, {}
    for line in open('ris/prova_%s.tsv' % g):
        f = line.rstrip('\n').split('\t')
        if f[0] == 'P': P[(f[2], f[3])] = (kv(f[4:]), f[4:])
        elif f[0] == 'H': H[(f[2], f[3], float(f[4]))] = kv(f[5:])
        elif f[0] == 'M': M[(f[2], f[3], float(f[4]))] = kv(f[5:])
    print('=' * 100); print('GEOMETRIA', g); print('=' * 100)
    print('%-13s %6s %6s %7s %9s %8s %9s %9s %10s %9s %8s %8s %8s' % ('predittore', 'pass', 'vuoto', 'vuoto>5', 'passi>.167', 'indProsg', 'ptLibCic', 'ptLib>5', 'R90libCic', 're40', 'saltoMed', 'saltoP90', 'ampio80'))
    for p in PRED:
        tot = dict(n=0, vu=0, vl=0, st=0, fpt=0, fpl=0, fr=0, nre=0, re40=0, cyc=0, w80=0)
        for b in ALL:
            d, raw = P[(b, p)]
            tot['n'] += int(d['npass'][0]); tot['vu'] += int(d['pass_vuoto'][0]); tot['vl'] += int(d['pass_vuoto_dopo5'][0]); tot['st'] += int(d['pass_passi_oltre'][0])
            tot['fpt'] += int(d['punto_su_libero_cicli'][0]); tot['fpl'] += int(d['punto_su_libero_dopo5'][0]); tot['fr'] += int(d['R90_su_libero_cicli'][0])
            tot['nre'] += int(d['nre'][0]); tot['re40'] += int(d['re40'][0]); tot['cyc'] += int(d['cicli'][0]); tot['w80'] += int(d['ampio80'][0])
        dp, _ = P[('prosegue', p)]
        print('%-13s %6d %6d %7d %9d %7.1f%% %9d %9d %10d %9.3f %8s %8s %7.1f%%' % (p, tot['n'], tot['vu'], tot['vl'], tot['st'], 100.0 * int(dp['pass_indietro'][0]) / max(1, int(dp['npass'][0])),
              tot['fpt'], tot['fpl'], tot['fr'], tot['re40'] / max(1, tot['nre']), dp['salto_med'][0], dp['salto_p90'][0], 100.0 * tot['w80'] / max(1, tot['cyc'])))
    print('salto mediano alla ricomparsa per comportamento (m):')
    for p in PRED: print('  %-13s ' % p + '  '.join('%s %s' % (b[:5], P[(b, p)][0]['salto_med'][0]) for b in ALL))
    print('COPERTURA R90 per comportamento e tau (dentro/n), area R90 / ombra; minimo sul percorso fino a 3 s e a 5 s')
    for p in ['C-005', 'C-004', 'C-001+C-008', 'sd-1', 'sd-0']:
        mn3 = (2, None); mn5 = (2, None); R100 = (0, 0)
        for b in ALL:
            row = []
            for tau in (0.5, 1.0, 2.0, 3.0, 5.0):
                h = H[(b, p, tau)]; n = int(h['n'][0]); k = int(h['in90'][0]); R100 = (R100[0] + int(h['in100'][0]), R100[1] + n)
                c = k / n if n else float('nan'); row.append('%.3f(%d)' % (c, n))
                if b in ONPATH and n >= 30:
                    if tau <= 3.0 and c < mn3[0]: mn3 = (c, (b, tau, k, n))
                    if c < mn5[0]: mn5 = (c, (b, tau, k, n))
            print('  %-12s %-10s ' % (p, b) + ' '.join(row))
        ar = []
        for tau in (0.5, 1.0, 2.0, 3.0, 5.0):
            a = sum(float(H[(b, p, tau)]['area90'][0]) * int(H[(b, p, tau)]['nreg'][0]) for b in ONPATH); nn = sum(int(H[(b, p, tau)]['nreg'][0]) for b in ONPATH)
            ar.append('%.2f' % (a / nn / float(H[('prosegue', p, tau)]['ombra'][0])) if nn else '-')
        w3 = wilson(mn3[1][2], mn3[1][3]); w5 = wilson(mn5[1][2], mn5[1][3])
        print('  -> %-12s minimo sul percorso <=3 s: %.3f %s [%.3f-%.3f]; <=5 s: %.3f %s [%.3f-%.3f]; R100 %d/%d; area/ombra (percorso) a 0,5/1/2/3/5 s: %s' % (p, mn3[0], mn3[1], w3[0], w3[1], mn5[0], mn5[1], w5[0], w5[1], R100[0], R100[1], ' '.join(ar)))
    print('ERRORE DEL PUNTO, mediana (m), miscela squadra e giurato, tau 0,5/1/2/3/5')
    for mix in ('squadra', 'giurato'):
        for p in PRED:
            print('  %-8s %-13s ' % (mix, p) + ' '.join(M[(mix, p, tau)]['err_med'][0] if (mix, p, tau) in M else '-' for tau in (0.5, 1.0, 2.0, 3.0, 5.0)))
    print('peggior rapporto con la migliore base (L1, L2) per cella comportamento x tau (n >= 30)')
    for p in PRED[2:]:
        worst = (0, None)
        for b in ALL:
            for tau in (0.5, 1.0, 2.0, 3.0, 5.0):
                h = H[(b, p, tau)]
                if int(h['npt'][0]) < 30: continue
                e = float(h['err_med'][0]); base = min(float(H[(b, 'L1-fermo', tau)]['err_med'][0]), float(H[(b, 'L2-filtro', tau)]['err_med'][0]))
                if base > 0 and e / base > worst[0]: worst = (e / base, (b, tau, e, base))
        print('  %-13s %.2f %s' % (p, worst[0], worst[1]))
