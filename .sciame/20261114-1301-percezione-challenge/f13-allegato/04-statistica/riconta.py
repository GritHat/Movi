# riconta.py -- sciame-statistico, f13/04-statistica.
# Riconta dai file grezzi dello sciame le cifre della tavola dei risultati. Sola lettura; nessun codice altrui importato.
# Uso: python -I -B riconta.py > ricontato.txt
import glob, json, math, os, re, sys

BASE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
F4 = os.path.join(BASE, 'f4', 'H-012', '03-validazione')
F8 = os.path.join(BASE, 'f8-continuita')
F10 = os.path.join(BASE, 'f10-dati')
Z = 1.959963984540054
NT = [0, 0]


def wilson(k, n, z=Z):
    if n == 0:
        return (float('nan'), float('nan'))
    p = k / n
    c = (p + z * z / (2 * n)) / (1 + z * z / n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return (c - h, c + h)


def W(k, n):
    lo, hi = wilson(k, n)
    return '%d su %d = %.4f [%.4f-%.4f]' % (k, n, k / n if n else float('nan'), lo, hi)


def riga(nome, scritto, mio, ok):
    NT[0 if ok else 1] += 1
    print('[%s] %s\n      scritto nei file: %s\n      ricontato:        %s' % ('TORNA' if ok else 'NON TORNA', nome, scritto, mio))


def kv(campi):
    d = {}
    for c in campi:
        if '=' in c:
            a, b = c.split('=', 1)
            d.setdefault(a, []).append(b)
    return d


def leggi_tsv(percorsi):
    """Somma piu' lanci. H[(pred, comp, tau)] = [n, in90, in100, fuori_griglia, area90*n, ombra*n]; P[(pred, comp)] = [npass, pass_vuoto, R90lib, R90fuori]."""
    H, P = {}, {}
    for p in percorsi:
        for l in open(p, encoding='utf-8'):
            c = l.rstrip('\n').split('\t')
            if c[0] == 'H':
                d = kv(c[5:])
                n = int(d['n'][0])
                a = H.setdefault((c[3], c[2], float(c[4])), [0, 0, 0, 0, 0.0, 0.0])
                a[0] += n; a[1] += int(d['in90'][0]); a[2] += int(d['in100'][0]); a[3] += int(d['fuori_griglia'][0])
                a[4] += float(d['area90'][0]) * n; a[5] += float(d['ombra'][0]) * n
            elif c[0] == 'P':
                d = kv(c[4:])
                a = P.setdefault((c[3], c[2]), [0, 0, 0, 0])
                a[0] += int(d['npass'][0]); a[1] += int(d['pass_vuoto'][0]); a[2] += int(d['R90_su_libero_cicli'][0])
                a[3] += int(d.get('R90_fuori_R100_cicli', ['0'])[0])
    return H, P


PERC = ['prosegue', 'rallenta', 'sosta', 'torna', 'sostalunga']
FUORI = ['svolta', 'lontano']
print('=' * 100 + '\nA. CONTINUITA E REGIONE (f8): file TSV, righe P (passaggi) e H (istanti nascosti per tempo dall\'ultima osservazione)\n' + '=' * 100)

# A1: predittore finale (sd-1), prova della soluzione
v = []
for g in 'DTL':
    H, P = leggi_tsv([os.path.join(F8, '13-soluzione', 'ris', 'prova_%s.tsv' % g)])
    v.append((sum(P[('sd-1', b)][1] for b in set(b for (p_, b) in P if p_ == 'sd-1')), sum(P[(p_, b)][0] for (p_, b) in P if p_ == 'sd-1')))
riga('A1 passaggi con almeno un ciclo senza regione, regione tarata, D/T/L (13-soluzione/ris/prova_*.tsv)', '0 su 2716 / 2800 / 2798',
     ' / '.join('%d su %d' % x for x in v), v == [(0, 2716), (0, 2800), (0, 2798)])
print('      limiti superiori: Wilson z^2/(N+z^2) = ' + ', '.join('%.5f' % wilson(0, n)[1] for _, n in v) + '; esatto a una coda 1-0.05^(1/N) = ' + ', '.join('%.5f' % (1 - 0.05 ** (1 / n)) for _, n in v) + '; 3/N = ' + ', '.join('%.5f' % (3 / n) for _, n in v))

# A2: semi riparati
SEMI = {g: sorted(glob.glob(os.path.join(F8, '15-statistica', 'ris', 'semi_%s_*.tsv' % g))) for g in 'DTL'}
HS, PS = {}, {}
for g in 'DTL':
    HS[g], PS[g] = leggi_tsv(SEMI[g])
for pred in ('sd-1', 'sd-0'):
    v = [(sum(PS[g][k][1] for k in PS[g] if k[0] == pred), sum(PS[g][k][0] for k in PS[g] if k[0] == pred)) for g in 'DTL']
    riga('A2 %s, semi riparati: passaggi con un vuoto (15-statistica/ris/semi_*.tsv; file %s)' % (pred, [len(SEMI[g]) for g in 'DTL']), '0 su 13 638 / 5600 / 5597',
         ' / '.join('%d su %d' % x for x in v), v == [(0, 13638), (0, 5600), (0, 5597)])
tot = sum(n for _, n in v)
print('      insieme: 0 su %d; limite superiore esatto a una coda %.6f, Wilson %.6f, 3/N %.6f' % (tot, 1 - 0.05 ** (1 / tot), wilson(0, tot)[1], 3 / tot))

# A3: nucleo prima della modifica
v5, v7 = [], []
for g in 'DTL':
    H, P = leggi_tsv([os.path.join(F8, '11-misure', 'risultati', 'prova_%s_pd09.tsv' % g)])
    v5.append((sum(P[('L0-nucleo', b)][1] for b in PERC), sum(P[('L0-nucleo', b)][0] for b in PERC)))
    v7.append((sum(P[k][1] for k in P if k[0] == 'L0-nucleo'), sum(P[k][0] for k in P if k[0] == 'L0-nucleo')))
riga('A3 sistema prima della modifica: passaggi con un vuoto, 5 comportamenti sul percorso (11-misure/risultati/prova_*_pd09.tsv)',
     '1958 / 1991 / 1999 su 1958 / 2000 / 2000', ' / '.join('%d su %d' % x for x in v5), v5 == [(1958, 1958), (1991, 2000), (1999, 2000)])
print('      su 7 comportamenti: ' + ' / '.join('%d su %d' % x for x in v7))

# A4: celle sopra soglia, semi riparati
for pred, atteso in (('sd-1', (45, 60, 12)), ('sd-0', (37, 60, 14))):
    c90 = c85 = c90_3 = 0; peggio = None; tutte = []
    for g in 'DTL':
        for b in PERC:
            for t in (0.5, 1.0, 2.0, 3.0):
                n, k = HS[g][(pred, b, t)][0], HS[g][(pred, b, t)][1]
                lo = wilson(k, n)[0]
                c85 += lo > 0.85
                if t <= 2.0:
                    c90 += lo > 0.90; tutte.append((g, b, t, k, n))
                    if peggio is None or lo < peggio[0]:
                        peggio = (lo, g, b, t, k, n)
                else:
                    c90_3 += lo > 0.90
    riga('A4 %s semi riparati, denominatore «tutti i nascosti»: celle con limite inferiore di Wilson > 0,90 fino a 2 s; > 0,85 fino a 3 s; > 0,90 a 3 s' % pred,
         '%d su 45; %d su 60; %d su 15' % atteso + ('; peggiore 826/879, limite 0,922' if pred == 'sd-1' else '; peggiore 715/800'),
         '%d su 45; %d su 60; %d su 15; peggiore %s %s %.1f s %d/%d = %.4f, limite inferiore %.4f' % (c90, c85, c90_3, peggio[1], peggio[2], peggio[3], peggio[4], peggio[5], peggio[4] / peggio[5], peggio[0]),
         (c90, c85, c90_3) == atteso)
    if pred == 'sd-1':
        for m, nome in ((45, 'Bonferroni'),):
            zb = None
            # quantile normale per 1 - 0.05/(2m): bisezione su erf
            lo_, hi_ = 0.0, 10.0
            target = 1 - 0.05 / (2 * m)
            for _ in range(200):
                mid = (lo_ + hi_) / 2
                if 0.5 * (1 + math.erf(mid / math.sqrt(2))) < target: lo_ = mid
                else: hi_ = mid
            zb = (lo_ + hi_) / 2
            cb = sum(1 for (g, b, t, k, n) in tutte if wilson(k, n, zb)[0] > 0.90)
            pb = min(wilson(k, n, zb)[0] for (g, b, t, k, n) in tutte)
            print('      correzione simultanea (%s, m = %d, z = %.4f): celle con limite inferiore > 0,90: %d su 45; peggior limite inferiore %.4f' % (nome, m, zb, cb, pb))
        lo_, hi_ = 0.0, 10.0
        for _ in range(200):
            mid = (lo_ + hi_) / 2
            if 0.5 * (1 + math.erf(mid / math.sqrt(2))) < 1 - 0.05 / 24: lo_ = mid
            else: hi_ = mid
        print('      controllo: z per 12 celle giudicate insieme = %.3f (nei file 2,87); 90 su 100 con quel z: [%.3f-%.3f] (nei file 0,78-0,96)' % ((lo_ + hi_) / 2, *wilson(90, 100, (lo_ + hi_) / 2)))

# A5: tabella per comportamento
print('\n   A5 tabella, regione tarata (sd-1), semi riparati, denominatore «tutti i nascosti»: dentro/n = quota [Wilson 95 %]')
for g in 'DTL':
    for b in PERC + FUORI:
        print('     %s %-10s ' % (g, b) + '  '.join('%.0fs %d/%d=%.3f[%.3f-%.3f]' % ((t, HS[g][('sd-1', b, t)][1], HS[g][('sd-1', b, t)][0], HS[g][('sd-1', b, t)][1] / HS[g][('sd-1', b, t)][0]) + wilson(HS[g][('sd-1', b, t)][1], HS[g][('sd-1', b, t)][0])) for t in (1.0, 2.0, 3.0, 5.0)))
    for pred in ('sd-1', 'sd-0'):
        ar = []
        for t in (1.0, 2.0, 3.0):
            a = sum(HS[g][(pred, b, t)][4] for b in PERC); o = sum(HS[g][(pred, b, t)][5] for b in PERC)
            ar.append(a / o)
        print('     %s %s area regione / ombra, media pesata sui 5 comportamenti sul percorso, a 1/2/3 s: %.2f %.2f %.2f' % (g, pred, *ar))
h = HS['D'][('sd-1', 'prosegue', 5.0)]
riga('A5b D «prosegue» a 5 s', '174/221 = 0,787 [0,729-0,836]', W(h[1], h[0]), (h[1], h[0]) == (174, 221))
h = HS['D'][('sd-1', 'prosegue', 3.0)]
riga('A5c D «prosegue» a 3 s, due denominatori', '461/513 (tutti); 461/480 (dentro l\'area osservata)', '%d/%d; %d/%d (fuori griglia %d)' % (h[1], h[0], h[1], h[0] - h[3], h[3]), (h[1], h[0], h[0] - h[3]) == (461, 513, 480))
for g, at in (('D', (86, 98, 92)),):
    Hb, _ = leggi_tsv([os.path.join(F8, '11-misure', 'risultati', 'prova_D_pd09.tsv')])
    hb = Hb[('C-004', 'prosegue', 3.0)]
    Hm, _ = leggi_tsv([os.path.join(F8, '13-soluzione', 'ris', 'prova_D.tsv')])
    hm = Hm[('sd-1', 'prosegue', 3.0)]
    riga('A5d una cella, due denominatori (D, «prosegue», 3 s; semi originali)', '86/92 e 86/98; 101/105 e 101/119',
         '%d/%d e %d/%d; %d/%d e %d/%d' % (hb[1], hb[0] - hb[3], hb[1], hb[0], hm[1], hm[0] - hm[3], hm[1], hm[0]),
         (hb[1], hb[0] - hb[3], hb[0], hm[1], hm[0] - hm[3], hm[0]) == (86, 92, 98, 101, 105, 119))

# A6: avviso contiene il nascosto
sol = 0; sol_f = 0
for g in 'DTL':
    Hm, _ = leggi_tsv([os.path.join(F8, '13-soluzione', 'ris', 'prova_%s.tsv' % g)])
    sol += sum(Hm[k][0] for k in Hm if k[0] == 'sd-1'); sol_f += sum(Hm[k][0] - Hm[k][2] for k in Hm if k[0] == 'sd-1')
sem = sum(HS[g][k][0] for g in 'DTL' for k in HS[g] if k[0] == 'sd-1'); sem_f = sum(HS[g][k][0] - HS[g][k][2] for g in 'DTL' for k in HS[g] if k[0] == 'sd-1')
ban = 0; ban_f = 0; ban_tutti = 0; npred = set()
for g in 'DTL':
    Hb, _ = leggi_tsv([os.path.join(F8, '11-misure', 'risultati', 'prova_%s_pd09.tsv' % g)])
    preds = sorted(set(k[0] for k in Hb)); npred.add(len(preds))
    ban += sum(Hb[k][0] for k in Hb if k[0] == preds[0]); ban_f += sum(Hb[k][0] - Hb[k][2] for k in Hb)
    ban_tutti += sum(Hb[k][0] for k in Hb)
tot = ban + sol + sem
riga('A6 istanti con il soggetto nascosto fuori dall\'area d\'avviso', '0 su 175 802 (35 780 + 35 891 + 104 131)',
     '%d su %d (%d + %d + %d); righe-campione del banco %d con %s predittori' % (ban_f + sol_f + sem_f, tot, ban, sol, sem, ban_tutti, sorted(npred)),
     (ban_f + sol_f + sem_f, ban, sol, sem) == (0, 35780, 35891, 104131))
print('      limite superiore con 0 su %d SE gli istanti fossero indipendenti: esatto %.2e; NON lo sono (istanti dello stesso passaggio): per passaggio vale A2' % (tot, 1 - 0.05 ** (1 / tot)))
r90lib = sum(PS[g][k][2] for g in 'DTL' for k in PS[g] if k[0] == 'sd-1'); r90f = sum(PS[g][k][3] for g in 'DTL' for k in PS[g] if k[0] == 'sd-1')
riga('A6b cicli con la regione su suolo visto libero oltre la fascia; cicli con la regione fuori dall\'area d\'avviso (semi riparati, sd-1)', '0 e 0', '%d e %d' % (r90lib, r90f), (r90lib, r90f) == (0, 0))

# A7: popolazione diversa dalla taratura
Hsp, _ = leggi_tsv([os.path.join(F8, '15-statistica', 'ris', 'semi_spostato_L_90000x400.tsv')])
m = {}
for tmax in (1.0, 2.0, 3.0):
    m[tmax] = min(((Hsp[('sd-1', b, t)][1] / (Hsp[('sd-1', b, t)][0] - Hsp[('sd-1', b, t)][3]), Hsp[('sd-1', b, t)][1], Hsp[('sd-1', b, t)][0] - Hsp[('sd-1', b, t)][3], b, t) for b in PERC for t in (0.5, 1.0, 2.0, 3.0) if t <= tmax and Hsp[('sd-1', b, t)][0] >= 30))
riga('A7 camminatori meno regolari della taratura, ombra larga (L): minimo sul percorso fino a 1/2/3 s (denominatore «dentro l\'area osservata»)',
     '0,944 / 0,835 [0,79-0,87] / 0,801 [0,75-0,84]', ' / '.join('%d/%d=%.3f [%.3f-%.3f] (%s, %.0f s)' % ((m[t][1], m[t][2], m[t][0]) + wilson(m[t][1], m[t][2]) + (m[t][3], m[t][4])) for t in (1.0, 2.0, 3.0)),
     [round(m[t][0], 3) for t in (1.0, 2.0, 3.0)] == [0.944, 0.835, 0.801])

# A8: blocchi di semi contigui
BL = []
for p in [os.path.join(F8, '11-misure', 'risultati', 'prova_D_pd09.tsv'), os.path.join(F8, '13-soluzione', 'ris', 'prova_D.tsv')] + sorted(glob.glob(os.path.join(F8, '15-statistica', 'ris', 'blocco_D_*.tsv'))):
    Hb, _ = leggi_tsv([p]); BL.append((os.path.basename(p), Hb))


def chi2gl(pred_di, b, t, idx):
    xs = []
    for nome, Hb in BL:
        h = Hb[(pred_di(nome), b, t)]
        xs.append((h[1], h[0] if idx == 1 else h[0] - h[3]))
    K = sum(x[0] for x in xs); Nn = sum(x[1] for x in xs); pm = K / Nn
    if pm in (0.0, 1.0):
        return None, xs
    return sum((k - n * pm) ** 2 / (n * pm * (1 - pm)) for k, n in xs) / (len(xs) - 1), xs


pd_ = lambda nome: 'C-004' if nome.startswith('prova_D_pd09') else 'sd-1'
for nome, idx in (('tutti', 1), ('dentro l\'area osservata', 2)):
    r3, xs = chi2gl(pd_, 'prosegue', 3.0, idx)
    ps = [k / n for k, n in xs]
    tutti = [chi2gl(pd_, b, t, idx)[0] for b in PERC for t in (0.5, 1.0, 2.0, 3.0)]
    tutti = [x for x in tutti if x is not None]
    print('   A8 %d blocchi di 400 semi contigui in D, denominatore «%s»: «prosegue» a 3 s da %.3f a %.3f, chi2/gl = %.2f; sulle %d celle sul percorso fino a 3 s: media %.2f, mediana %.2f, minimo %.2f, massimo %.2f; radice di media e massimo: %.2f e %.2f'
          % (len(BL), nome, min(ps), max(ps), r3, len(tutti), sum(tutti) / len(tutti), sorted(tutti)[len(tutti) // 2], min(tutti), max(tutti), math.sqrt(sum(tutti) / len(tutti)), math.sqrt(max(tutti))))
print('      scritto nei file: «prosegue» a 3 s da 0,726 a 0,977; rapporto 2,67 («tutti») e 1,62 (denominatore del banco); massimo 6,0; intervalli stretti di 1,3-2,5 volte (radice di 1,62 e di 6,0 = %.2f e %.2f)' % (math.sqrt(1.62), math.sqrt(6.0)))
# gli stessi comportamenti a semi riparati: 5 lanci D da 400 semi
BLR = [(os.path.basename(p), leggi_tsv([p])[0]) for p in SEMI['D']]
BL_salva = BL; BL = BLR
tr = [chi2gl(lambda n_: 'sd-1', b, t, 1)[0] for b in PERC for t in (0.5, 1.0, 2.0, 3.0)]
tr = [x for x in tr if x is not None]
print('      a semi riparati (%d lanci D): chi2/gl medio sulle %d celle sul percorso fino a 3 s = %.2f (nei file 0,94); massimo %.2f' % (len(BLR), len(tr), sum(tr) / len(tr), max(tr)))
BL = BL_salva

# A9: generatore, semi contigui (mio splitmix64, dalla lettura di gen.h)
M64 = (1 << 64) - 1
G = 0x9E3779B97F4A7C15


def mix(z):
    z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & M64
    z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & M64
    return z ^ (z >> 31)


def flusso(seme, n, riparato=False, geo=1, beh=0, stream=0):
    s = (seme * G + geo * 0xD1B54A32D192ED03 + beh * 0x8CB92BA72F3D8DD7 + stream * 0xABCDEF1234567) & M64
    if riparato:
        s = mix(s)
    out = []
    for _ in range(n + 2):
        s = (s + G) & M64
        out.append(mix(s))
    return out[2:]


a = flusso(9000, 1001); b = flusso(9001, 1000)
ug = sum(1 for i in range(1000) if a[i + 1] == b[i])
ar_ = flusso(9000, 1001, True); br_ = flusso(9001, 1000, True)
ugr = sum(1 for i in range(1000) if ar_[i + 1] == br_[i]) + sum(1 for i in range(1000) if ar_[i] == br_[i])
riga('A9 generatore: flusso del seme 9001 = flusso del seme 9000 avanzato di 1 (mio splitmix64)', '1000 uguali su 1000', '%d su 1000; con lo stato iniziale mescolato (riparazione): %d coincidenze' % (ug, ugr), ug == 1000 and ugr == 0)

# A10: costo del predittore
t_py = open(os.path.join(F8, '14-attacco', 'ris', 'tempo_py.txt'), encoding='utf-8').read()
t_c = open(os.path.join(F8, '14-attacco', 'ris', 'tempo_C.txt'), encoding='utf-8').read()
mp = re.findall(r'tracce=(\d+) .*?mediana=([\d.]+) ms p95=([\d.]+) ms', t_py); mc = re.findall(r'tracce=(\d+) .*?mediana=([\d.]+) ms p95=([\d.]+) ms', t_c)
riga('A10 costo del predittore per ciclo (14-attacco/ris/tempo_*.txt; cifre lette, non rimisurate)', 'Python puro 10 tracce: 5,3 ms mediana, 6,2 al 95o; C 120 tracce: 5,4 ms al 95o',
     'py %s; C %s' % (mp, mc), ('10', '5.3', '6.2') in mp and any(x[0] == '120' and x[2].startswith('5.4') for x in mc))

# A11: passaggi «scoperti» (traccia chiusa prima dell'ombra) con rilevamento 0,7 e corpo esteso
tx = open(os.path.join(F8, '14-attacco', 'ris', 'tutto_T_e0_pd07.txt'), encoding='utf-8').read()
sc = sum(int(x) for x in re.findall(r'scoperti=(\d+)', tx)); va = sum(int(x) for x in re.findall(r'validi=(\d+)', tx)); fu = sum(int(x) for x in re.findall(r'fuori_R100=(\d+)', tx)); vu = sum(int(x) for x in re.findall(r' vuoti=(\d+)', tx))
riga('A11 passaggi in cui la traccia si chiude prima dell\'ombra, rilevamento 0,7, corpo esteso, maschera esatta (14-attacco/ris/tutto_T_e0_pd07.txt)', '130 su 1581',
     '%s; in quei lanci: centro nascosto fuori dall\'area d\'avviso %d, cicli senza regione %d' % (W(sc, va), fu, vu), (sc, va) == (130, 1581))
tb = open(os.path.join(F8, '14-attacco', 'ris', 'tutto_T.txt'), encoding='utf-8').read()
m1 = re.search(r'prosegue .*?R90 grezza a 1/2/3/5 s: (\d+)/(\d+)=[\d.]+ (\d+)/(\d+)=', tb)
if m1:
    print('      «tutto insieme» (corpo esteso, ombra a -20 cm, rilevamento 0,7), «prosegue», regione a 1 e 2 s: %s/%s e %s/%s (nei file 136/364 e 43/152)' % m1.groups())

# A12: quota di cicli senza osservazione con una regione emessa; nucleo a semi riparati; errore del punto
def cicli(percorsi, pred, comps):
    c = r = 0
    for p in percorsi:
        for l in open(p, encoding='utf-8'):
            f = l.rstrip('\n').split('\t')
            if f[0] == 'P' and f[3] == pred and f[2] in comps:
                d = kv(f[4:]); c += int(d['cicli'][0]); r += int(d['cicli_regione'][0])
    return r, c


v0 = [cicli([os.path.join(F8, '11-misure', 'risultati', 'prova_%s_pd09.tsv' % g)], 'L0-nucleo', PERC) for g in 'DTL']
v1 = [cicli(SEMI[g], 'sd-1', PERC + FUORI) for g in 'DTL']
riga('A12 cicli senza osservazione in cui e\' emessa una regione: prima della modifica (5 comportamenti sul percorso) e dopo (semi riparati, 7 comportamenti)',
     'prima 19 / 38 / 33 %; dopo 100 %', 'prima ' + ' / '.join('%d su %d = %.1f %%' % (r, c, 100 * r / c) for r, c in v0) + '; dopo ' + ' / '.join('%d su %d' % x for x in v1),
     [round(100 * r / c) for r, c in v0] == [19, 38, 33] and all(r == c for r, c in v1))
vn = []
for g in 'DTL':
    Hn, Pn = leggi_tsv(SEMI[g])
    vn.append((sum(Pn[('L0-nucleo', b)][1] for b in PERC), sum(Pn[('L0-nucleo', b)][0] for b in PERC)))
riga('A12b sistema prima della modifica, semi riparati: passaggi con un vuoto (5 comportamenti sul percorso)', '9715 su 9735; 3981 su 4000; 3997 su 3999', ' / '.join('%d su %d' % x for x in vn), vn == [(9715, 9735), (3981, 4000), (3997, 3999)])
print('   A12c errore mediano del punto, miscela di riferimento, geometria T, righe M dei file (letto, non ricalcolato dai passaggi):')
for p in [os.path.join(F8, '13-soluzione', 'ris', 'prova_T.tsv')] + SEMI['T']:
    for l in open(p, encoding='utf-8'):
        f = l.rstrip('\n').split('\t')
        if f[0] == 'M' and f[2] == 'squadra' and f[3] in ('sd-1', 'L1-fermo') and f[4] in ('1.0', '2.0', '3.0'):
            print('      %-28s %-9s tau %s %s %s' % (os.path.basename(p), f[3], f[4], f[5], f[6]))

print('\n' + '=' * 100 + '\nB. NUCLEO (f4): file di testo dei lanci\n' + '=' * 100)


def righe_r8(nome):
    out = []
    for l in open(os.path.join(F4, nome), encoding='utf-8'):
        m = re.match(r'\s*(\S+)\s+(principale|BRACCIO)\s+fascia ([\d.]+) errore ([+-][\d.]+) (\S+)\s*: falliti (\d+)/(\d+) ;.*?riemersioni (\d+) riagganciate ([\d.nan]+)%', l)
        if m:
            out.append(dict(geo=m.group(1), tipo=m.group(2), fascia=float(m.group(3)), err=float(m.group(4)), comp=m.group(5), k=int(m.group(6)), n=int(m.group(7)), riem=int(m.group(8)), riag=m.group(9)))
    return out


r = [x for x in righe_r8('v2_R8.txt') if x['tipo'] == 'principale']
riga('B1 avviso, rilevamento certo: passaggi falliti (v2_R8.txt, righe «principale»)', '0 su 14 400 in 36 celle', '%d su %d in %d celle' % (sum(x['k'] for x in r), sum(x['n'] for x in r), len(r)),
     (sum(x['k'] for x in r), sum(x['n'] for x in r), len(r)) == (0, 14400, 36))
cr = [x for x in r if x['riem'] > 0]
tutte100 = all(x['riag'] == '100.0' for x in cr)
riga('B2 identita\' al ritorno, modello ideale, una persona: celle con riemersioni e quota riagganciata', '100 % in 27 celle (N = 400 per cella; limite inferiore 99,25 %)',
     '%d celle con riemersioni; tutte al 100,0 %%: %s; riemersioni per cella min %d max %d; somma %d' % (len(cr), tutte100, min(x['riem'] for x in cr), max(x['riem'] for x in cr), sum(x['riem'] for x in cr)),
     len(cr) == 27 and tutte100)
print('      limite inferiore con 400 su 400: 1 - 3/400 = %.4f; esatto a una coda 0.05^(1/400) = %.4f; Wilson %.4f' % (1 - 3 / 400, 0.05 ** (1 / 400), wilson(400, 400)[0]))
r = [x for x in righe_r8('v2_R8_pd09.txt') if x['tipo'] == 'principale']
a = [x for x in r if x['err'] == -0.2]; b = [x for x in r if x['err'] != -0.2]
riga('B3 avviso, probabilita\' di rilevamento 0,9: falliti con ombra stimata a -20 cm; a 0 e +20 cm (v2_R8_pd09.txt)', '13 su 4800 in 8 celle su 12; 0 su 9600',
     '%s, in %d celle su %d; %d su %d' % (W(sum(x['k'] for x in a), sum(x['n'] for x in a)), sum(1 for x in a if x['k'] > 0), len(a), sum(x['k'] for x in b), sum(x['n'] for x in b)),
     (sum(x['k'] for x in a), sum(x['n'] for x in a), sum(1 for x in a if x['k'] > 0), sum(x['k'] for x in b), sum(x['n'] for x in b)) == (13, 4800, 8, 0, 9600))
s = open(os.path.join(F4, 'v2_SECOND.txt'), encoding='utf-8').read()
m = re.findall(r'campo (\d+)/(\d+) ; portata (\d+)/(\d+) ; ombra (\d+)/(\d+)', s)
om = (sum(int(x[4]) for x in m), sum(int(x[5]) for x in m)); po = (sum(int(x[2]) for x in m), sum(int(x[3]) for x in m)); ca = (sum(int(x[0]) for x in m), sum(int(x[1]) for x in m))
riga('B4 secondo soggetto mai tracciato che esce dalla stessa ombra: identita\' assegnata per errore (v2_SECOND.txt)', '2400 su 2400; 2 su 1200 (dalla portata)',
     'ombra %d su %d; portata %d su %d; campo %d su %d' % (om + po + ca), om == (2400, 2400) and po[0] == 2)
print('      nota: il denominatore «1200» della portata nei file e\' la meta\' delle righe; qui le righe sommate danno %d' % po[1])
for nome in ('v2_WALLP.txt', 'v2_MOB.txt'):
    print('   --- %s (prime righe, lette) ---' % nome)
    for l in open(os.path.join(F4, nome), encoding='utf-8').read().splitlines()[:14]:
        print('      ' + l[:230])

print('\n' + '=' * 100 + '\nC. PROFONDITA\' SIMULATA DA SCHEDA TECNICA E DATI PUBBLICI (f10): json e jsonl\n' + '=' * 100)
U = os.path.join(F10, '20-validazione', 'uscite')
for var, att in (('sim', (0, 2907032)), ('sim_p40', (2, 2907032))):
    L = json.load(open(os.path.join(U, var, 'misura_libero.json'), encoding='utf-8'))
    con = [x for x in L if x.get('celle_tutte_in_ombra', 0) > 0]
    k = sum(x['libero_tutta_ombra'] for x in con); n = sum(x['celle_tutte_in_ombra'] * x['fotogrammi'] for x in con)
    kb = sum(x['libero_bordo'] for x in con); nb = sum(x['celle_di_bordo'] * x['fotogrammi'] for x in con)
    nf = sum(1 for x in con if x['nome'].endswith('__filtri'))
    forme = sorted(set(x['celle_tutte_in_ombra'] for x in con))
    riga('C1 [%s] celle «libero» interamente dentro l\'ombra vera (misura_libero.json)' % var, '%d su 2 907 032 celle·fotogramma; 135 sequenze (131 + 4 con filtri)' % att[0],
         '%d su %d; sequenze con ombra %d (di cui con filtri %d); al bordo %d su %d; valori distinti di celle d\'ombra %s; sequenze colpite %d' % (k, n, len(con), nf, kb, nb, forme, sum(1 for x in con if x['libero_tutta_ombra'] > 0)),
         (k, n) == att and len(con) == 135)
    if var == 'sim':
        ns = len(con) - nf
        print('      per sequenza: 0 su %d -> limite superiore Wilson %.4f; esatto a una coda %.4f; 3/N %.4f (nei file 2,9 %%)' % (ns, wilson(0, ns)[1], 1 - 0.05 ** (1 / ns), 3 / ns))
        print('      per cella·fotogramma il limite 3/N = %.1e NON e\' lecito: le celle di una sequenza non sono indipendenti' % (3 / n))

for var, att in (('sim', dict(cont=(0, 90), disp=(0, 45), pm=79, reg=(36, 46))), ('sim_p40', dict(cont=(80, 90), disp=(41, 45), pm=5, reg=(83, 90)))):
    P = json.load(open(os.path.join(U, var, 'misura_passaggi.json'), encoding='utf-8'))
    ps = [p for p in P if re.match(r'd435i_nom__pannello_(a12|a05|b)__s\d+$', p['nome'])]
    disp = [p for p in ps if int(p['nome'][-2:]) % 2 == 1]
    cont = sum(1 for p in ps if p['continuita_pulita']); cd = sum(1 for p in disp if p['continuita_pulita'])
    pm = sum(1 for p in ps if p['pannello_si_muove'])
    cc = {}
    for p in ps:
        for kk, vv in p['cella_centro_nascosto'].items():
            cc[kk] = cc.get(kk, 0) + vv
    rg = [p for p in ps if p.get('copertura90') is not None]
    rk = sum(1 for p in rg if p['copertura90'] >= 1.0)
    fus = sum(1 for p in ps if p.get('fusione_fotogrammi', 0) > 0)
    ok = (cont, len(ps)) == att['cont'] and (cd, len(disp)) == att['disp'] and pm == att['pm'] and (att['reg'] is None or (rk, len(rg)) == att['reg'])
    riga('C2 [%s] passaggi dietro il pannello, profilo D435i nominale, tre geometrie x 30 semi (misura_passaggi.json)' % var,
         'stessa identita\' %d su %d; semi dispari %d su %d; pannello «in movimento» %d su 90%s' % (att['cont'] + att['disp'] + (att['pm'],) + (('; regione %d su %d' % att['reg']) if att['reg'] else '',)),
         'stessa identita\' %s; semi dispari %s; pannello «in movimento» %s; soggetto sempre nella regione %s; passaggi con fusione persona-pannello %d' % (W(cont, len(ps)), W(cd, len(disp)), W(pm, len(ps)), W(rk, len(rg)) if rg else '-', fus), ok)
    tot = sum(cc.values())
    print('      NOTA D\'ATTRIBUZIONE: «regione 83 su 90» sta nella variante a soglia di punti corretta (sim_p40); con i parametri di partenza (sim) solo %d passaggi su 90 hanno una previsione e la verita\' resta sempre nella regione in %d di essi. Al primo lancio di questo programma l\'attesa «83 su 90» era messa su sim e dava NON TORNA.' % (len(rg), rk) if var == 'sim' else '      cella del centro nascosto [sim_p40]: %s' % cc)
    if var == 'sim':
        riga('C3 [sim] cella del centro del soggetto nascosto, per fotogramma', '2939 su 3038 nell\'avviso; 99 in ombra senza avviso; 0 «libero»',
             '%s; in ombra senza avviso %d; libero %d; occupato %d; non osservato %d' % (W(cc['possibile_presenza'], tot), cc['in_ombra_senza_avviso'], cc['libero'], cc['occupato'], cc['non_osservato']),
             (cc['possibile_presenza'], tot, cc['in_ombra_senza_avviso'], cc['libero']) == (2939, 3038, 99, 0))
        pv = sum(1 for p in ps if p['cella_centro_nascosto']['in_ombra_senza_avviso'] > 0)
        print('      per passaggio (unita\' indipendente): passaggi con almeno un fotogramma senza avviso %s; con una cella «libero» 0 su %d (limite superiore Wilson %.4f)' % (W(pv, len(ps)), len(ps), wilson(0, len(ps))[1]))

O = json.load(open(os.path.join(U, 'sim', 'misura_ombra.json'), encoding='utf-8'))
nom = [x for x in O if '_nom__' in x['nome'] and not x['nome'].endswith('__filtri')]
lim = [x for x in O if '_lim__' in x['nome'] and not x['nome'].endswith('__filtri')]


def estremi(xs):
    mi = min(min(x['sinistra_cm'][0], x['destra_cm'][0]) for x in xs); ma = max(max(x['sinistra_cm'][4], x['destra_cm'][4]) for x in xs)
    med = sorted([x['sinistra_cm'][2] for x in xs] + [x['destra_cm'][2] for x in xs])
    dentro = sum(1 for x in xs if min(x['sinistra_cm'][0], x['destra_cm'][0]) >= -20 and max(x['sinistra_cm'][4], x['destra_cm'][4]) <= 20)
    return mi, ma, med[len(med) // 2], dentro


try:
    mi, ma, med, de = estremi(nom); mil, mal, medl, del_ = estremi(lim)
    riga('C4 errore del bordo dell\'ombra stimata, condizioni nominali (misura_ombra.json)', 'da +2,0 a +14,6 cm, mediana +6,2; 115 sequenze su 115 entro ±20 cm; al limite 0 su 8, da -65 a +73 cm',
         'nominale: da %+.1f a %+.1f cm, mediana delle mediane di lato %+.1f; entro ±20 cm %s; al limite: da %+.1f a %+.1f cm, entro ±20 cm %d su %d' % (mi, ma, med, W(de, len(nom)), mil, mal, del_, len(lim)),
         (round(mi, 1), round(ma, 1), de, len(nom), del_, len(lim)) == (2.0, 14.6, 115, 115, 0, 8))
except Exception as e:
    riga('C4 errore del bordo dell\'ombra', '115 su 115', 'non ricontato: %r' % e, False)

Os = json.load(open(os.path.join(U, 'sim', 'misura_ostacoli.json'), encoding='utf-8'))
d = {x['sequenza']: (x['fotogrammi_visto_entro_15cm'], x['fotogrammi']) for x in Os}
riga('C5 ostacoli fermi visti entro 15 cm (misura_ostacoli.json)', 'cassa 84 su 84; scatola di 15 cm a 2 m 10 su 10',
     'cassa %d su %d; scatola a 2 m %d su %d; scatola a 0,8 m %d su %d; vetro %d su %d; sospeso a 2,0 m %d su %d' % (d['d435i_nom__cassa_persona__s00'] + d['d435i_nom__scatola15_2p0m'] + d['d435i_nom__scatola15_0p8m'] + d['d435i_nom__vetro_sfondo'] + d['d435i_nom__sospeso_2p0m']),
     d['d435i_nom__cassa_persona__s00'] == (84, 84) and d['d435i_nom__scatola15_2p0m'] == (10, 10))
print('      limite inferiore di Wilson: 84 su 84 -> %.3f (fotogrammi di UNA sequenza, non indipendenti); 10 su 10 -> %.3f' % (wilson(84, 84)[0], wilson(10, 10)[0]))
fant = {}
for nome in ('d435i_nom__pavimento_vuoto', 'd455_nom__pavimento_vuoto', 'g335_nom__pavimento_vuoto', 'd435i_lim__pavimento_vuoto'):
    try:
        rj = json.load(open(os.path.join(U, 'sim', nome, 'riassunto.json'), encoding='utf-8'))
        fant[nome] = rj.get('tracce_confermate', rj.get('tracce', None))
    except Exception as e:
        fant[nome] = 'non letto (%s)' % type(e).__name__
riga('C6 tracce confermate su pavimento vuoto, 30 fotogrammi (riassunto.json)', '28 (D435i) / 0 (D455) / 26 (Gemini 335) / 43 (D435i al limite)', str(fant),
     [fant.get(k) for k in ('d435i_nom__pavimento_vuoto', 'd455_nom__pavimento_vuoto', 'g335_nom__pavimento_vuoto', 'd435i_lim__pavimento_vuoto')] == [28, 0, 26, 43])

# costo per ciclo
ts = []; nseq = 0
for dname in sorted(os.listdir(os.path.join(U, 'sim'))):
    fp = os.path.join(U, 'sim', dname, 'fotogrammi.jsonl')
    if os.path.isfile(fp):
        nseq += 1
        for l in open(fp, encoding='utf-8'):
            if l.strip():
                ts.append(json.loads(l)['tempo_ciclo_ms'])
ts.sort()
riga('C7 costo per ciclo della catena, 424x240, un filo di CPU da portatile (fotogrammi.jsonl di %d sequenze)' % nseq, 'media 6,35 ms; 95o 18,6; massimo 105; 4 cicli su 9152 oltre 66 ms',
     'cicli %d; media %.2f ms; mediana %.2f; 95o %.1f; massimo %.1f; oltre 66,7 ms: %d; oltre 66 ms: %d' % (len(ts), sum(ts) / len(ts), ts[len(ts) // 2], ts[int(0.95 * len(ts))], ts[-1], sum(1 for t in ts if t > 66.7), sum(1 for t in ts if t > 66)),
     len(ts) == 9152 and round(sum(ts) / len(ts), 2) == 6.35 and sum(1 for t in ts if t > 66) == 4)
try:
    rv = [json.loads(l) for l in open(os.path.join(U, 'vere', 'RIEPILOGO.jsonl'), encoding='utf-8') if l.strip()]
    print('   C7b registrazioni pubbliche (vere/RIEPILOGO.jsonl; cifre lette da un riepilogo, non ricontabili):')
    for x in rv:
        print('      ' + json.dumps(x, ensure_ascii=False)[:260])
except Exception as e:
    print('   C7b vere/RIEPILOGO.jsonl non letto: %r' % e)

# THOR
T = json.load(open(os.path.join(U, 'banco_thor.json'), encoding='utf-8'))
q = T['prova']['q0.2_tutti']
cop = [q[t]['copertura90'] for t in ('1.0', '2.0', '3.0')]; err = [q[t]['errore_mediano'] for t in ('1.0', '2.0', '3.0')]
riga('C8 tracciati pubblici di pedoni (cattura del moto): regione al 90 % del filtro con q = 0,2; N tratti e persone (banco_thor.json, riassunto)',
     '219 tratti, 9 persone; copertura 0,977 / 1,000 / 1,000; errore mediano 0,21 / 0,49 / 0,81 m',
     'N %d, persone %d; copertura %s -> conteggi %s; Wilson %s; errore mediano %s; IC nel file a 1 s %s' % (q['N'], q['persone'], ['%.3f' % c for c in cop], [round(c * q['N']) for c in cop], ['[%.3f-%.3f]' % wilson(round(c * q['N']), q['N']) for c in cop], ['%.2f' % e for e in err], q['1.0'].get('ic95')),
     q['N'] == 219 and q['persone'] == 9 and [round(c, 3) for c in cop] == [0.977, 1.0, 1.0])
for qq in ('q0.05_tutti', 'q0.01_tutti'):
    if qq in T['prova']:
        x = T['prova'][qq]
        print('      %s: copertura a 1/2/3 s %s' % (qq, ['%.3f' % x[t]['copertura90'] for t in ('1.0', '2.0', '3.0')]))
print('      taratura su exp1 (227 tratti): ' + '; '.join('q=%s -> %s' % (k, ['%.3f' % c for c in v['copertura']]) for k, v in T['taratura'].items()))
T2 = json.load(open(os.path.join(F10, '21-statistica', 'tabelle', 'thor.json'), encoding='utf-8'))
print('      ricalcolo indipendente gia\' nei file (21-statistica/tabelle/thor.json): tratti exp3 %d; per persona %s; q=0,2 con altri sfasamenti %s' % (T2['exp3']['tratti'], T2['exp3']['per_persona'], T2['sens_q0.2']['sfasamenti'][0]))
pp = list(T2['exp3']['per_persona'].values())
neff = sum(pp) ** 2 / sum(x * x for x in pp)
print('      tratti per persona: min %d max %d; numerosita\' efficace se i tratti di una persona fossero uno solo: 9; indice (somma)^2/somma dei quadrati = %.1f' % (min(pp), max(pp), neff))

print('\n' + '=' * 100 + '\nESITO: tornano %d, non tornano %d\n' % (NT[0], NT[1]) + '=' * 100)
