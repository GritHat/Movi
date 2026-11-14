#!/usr/bin/env python3
# riconta.py — sciame-statistico, f8, fase f4. Sola lettura dei grezzi; Python 3 puro (niente numpy).
# Ricalcola dai CONTEGGI (righe H, P, G dei .tsv del banco e delle modifiche; tabelle del torneo) coperture al 50 e al 90 %,
# intervalli di Wilson, nitidezza (area / ombra), punteggio, esiti delle soglie del triage, eterogeneita' fra lanci,
# spostamento della distribuzione, numerosita' per l'hardware.
# DUE DEFINIZIONI del denominatore della copertura, perche' i file a monte ne usano due:
#   griglia = nascosti a tau e dentro l'area osservata (n - fuori_griglia): e' quella del banco (11-misure/tabelle.py);
#   tutti   = tutti i nascosti a tau (n): e' quella delle modifiche (13-soluzione/leggi.py).
# Uso (dalla cartella 15-statistica):  PYTHONDONTWRITEBYTECODE=1 timeout 120 python3 riconta.py griglia > ris/TABELLE_STATISTICO_griglia.txt
#                                       PYTHONDONTWRITEBYTECODE=1 timeout 120 python3 riconta.py tutti   > ris/TABELLE_STATISTICO_tutti.txt
import math, os, sys
QUI = os.path.dirname(os.path.abspath(__file__))
F8 = os.path.dirname(QUI)
BANCO = os.path.join(F8, '11-misure', 'risultati')
MODIF = os.path.join(F8, '13-soluzione', 'ris')
TORNEO = os.path.join(F8, '12-torneo', 'ris')
MIEI = os.path.join(QUI, 'ris')
ONPATH = ['prosegue', 'rallenta', 'sosta', 'torna', 'sostalunga']
OFF = ['svolta', 'lontano']
BEH6 = ['prosegue', 'rallenta', 'sosta', 'torna', 'svolta', 'lontano']
W = {'squadra': dict(zip(BEH6, [60, 10, 10, 10, 5, 5])), 'giurato': dict(zip(BEH6, [30, 10, 20, 20, 10, 10]))}
TAUS = [0.5, 1.0, 2.0, 3.0, 5.0]
Z = 1.959964
MODO = sys.argv[1] if len(sys.argv) > 1 else 'griglia'
assert MODO in ('griglia', 'tutti')


# ---------------------------------------------------------------- statistica di base
def wilson(k, n, z=Z):
    if n == 0: return (float('nan'), float('nan'))
    p = k / n; den = 1 + z * z / n; c = p + z * z / (2 * n); h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - h) / den, (c + h) / den)

def lbin(n, k): return math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)

def binom_cdf(k, n, p):  # P(X <= k)
    if k < 0: return 0.0
    if k >= n: return 1.0
    if p <= 0: return 1.0
    if p >= 1: return 0.0
    return min(1.0, sum(math.exp(lbin(n, i) + i * math.log(p) + (n - i) * math.log(1 - p)) for i in range(0, k + 1)))

def clopper(k, n, a=0.05):
    def solve(f, lo, hi):
        for _ in range(60):
            m = (lo + hi) / 2
            if f(m): lo = m
            else: hi = m
        return (lo + hi) / 2
    lo = 0.0 if k == 0 else solve(lambda p: 1 - binom_cdf(k - 1, n, p) < a / 2, 0.0, 1.0)
    hi = 1.0 if k == n else solve(lambda p: binom_cdf(k, n, p) > a / 2, 0.0, 1.0)
    return (lo, hi)

def fisher2(k1, n1, k2, n2):  # test esatto di Fisher a due code (somma delle tabelle non piu' probabili di quella vista)
    K = k1 + k2; N = n1 + n2
    def lp(x): return lbin(n1, x) + lbin(n2, K - x) - lbin(N, K)
    l0 = lp(k1); s = 0.0
    for x in range(max(0, K - n2), min(n1, K) + 1):
        l = lp(x)
        if l <= l0 + 1e-9: s += math.exp(l)
    return min(1.0, s)

def chi2_omog(celle):  # celle = [(k, n), ...]; omogeneita' delle proporzioni; ritorna (chi2, gradi, p) con p esatto solo per 1 o 2 gradi
    K = sum(k for k, n in celle); N = sum(n for k, n in celle); p = K / N
    if p in (0.0, 1.0): return (0.0, len(celle) - 1, 1.0)
    x = sum((k - n * p) ** 2 / (n * p * (1 - p)) for k, n in celle if n > 0); g = len(celle) - 1
    pv = math.exp(-x / 2) if g == 2 else (math.erfc(math.sqrt(x / 2)) if g == 1 else float('nan'))
    return (x, g, pv)

def esito_soglia(k, n, soglia, verso='>='):
    lo, hi = wilson(k, n)
    if verso == '>=':
        return 'regge' if lo >= soglia else ('smentita' if hi < soglia else 'non risolta')
    return 'regge' if hi <= soglia else ('smentita' if lo > soglia else 'non risolta')


# ---------------------------------------------------------------- lettura dei grezzi
def kv(fields):
    d = {}
    for f in fields:
        if '=' in f:
            k, v = f.split('=', 1); d.setdefault(k, []).append(v)
    return d

def leggi_tsv(*paths, modo=None):
    """Somma piu' lanci (semi disgiunti) della stessa geometria. Ritorna H[(pred,beh,tau)] = dict, P[(pred,beh)] = dict, G[beh] = dict."""
    modo = modo or MODO
    H, P, G = {}, {}, {}
    for path in paths:
        for line in open(path):
            f = line.rstrip('\n').split('\t')
            if f[0] == 'H':
                d = kv(f[5:]); key = (f[3], f[2], float(f[4]))
                n, nreg, fg = int(d['n'][0]), int(d['nreg'][0]), int(d['fuori_griglia'][0])
                r = dict(n=(n - fg if modo == 'griglia' else n), ntot=n, fg=fg, nreg=nreg, in50=int(d['in50'][0]), in90=int(d['in90'][0]), in100=int(d['in100'][0]),
                         a50=float(d['area50'][0]) * nreg, a90=float(d['area90'][0]) * nreg, ombra=float(d['ombra'][0]),
                         sc=(float(d['punteggio'][0]) * n if d['punteggio'][0] != 'nan' else 0.0))
                if key in H:
                    o = H[key]
                    for c in ('n', 'ntot', 'fg', 'nreg', 'in50', 'in90', 'in100', 'a50', 'a90', 'sc'): o[c] += r[c]
                else: H[key] = r
            elif f[0] == 'P':
                d = kv(f[4:]); key = (f[3], f[2])
                r = dict(npass=int(d['npass'][0]), pass_vuoto=int(d['pass_vuoto'][0]), pass_vuoto_dopo5=int(d['pass_vuoto_dopo5'][0]),
                         cicli=int(d['cicli'][0]), cicli_regione=int(d['cicli_regione'][0]), ampio50=int(d['ampio50'][0]), ampio80=int(d['ampio80'][0]),
                         nre=int(d['nre'][0]), re40=int(d['re40'][0]), R90lib=int(d['R90_su_libero_cicli'][0]), R90fuori=int(d['R90_fuori_R100_cicli'][0]),
                         ptlib=int(d['punto_su_libero_cicli'][0]))
                if key in P:
                    for c in r: P[key][c] += r[c]
                else: P[key] = r
            elif f[0] == 'G':
                d = kv(f[3:]); r = dict(validi=int(d['validi'][0]), scartati=int(d['scartati'][0]))
                if f[2] in G:
                    for c in r: G[f[2]][c] += r[c]
                else: G[f[2]] = r
    return H, P, G

def leggi_torneo(path):
    """Tabella 1 dei file del torneo: quote a tre decimali e n; i conteggi si ricostruiscono con round(quota * n)."""
    CN = ['C004', 'C001', 'C005W', 'C005P', 'ESTA', 'ESTB']; d = {}; sez = 0
    for r in open(path):
        if r.startswith('## '): sez = int(r[3:].split('.')[0]); continue
        if sez != 1 or '|' not in r or r.startswith('comport'): continue
        parti = r.split('|'); a = parti[0].split(); beh, tau, n = a[0], float(a[1]), int(a[2])
        for i, cn in enumerate(CN):
            v = [float(x) for x in parti[1 + i].split()]
            d[(cn, beh, tau)] = dict(n=n, ntot=n, fg=0, in90=round(v[0] * n), in50=round(v[1] * n), area=v[2], noreg=v[3])
    return d

def cella(H, p, b, t): return H.get((p, b, t))

def minimo(H, p, behs, taus, campo='in90', nmin=30):
    best = None
    for b in behs:
        for t in taus:
            h = cella(H, p, b, t)
            if not h or h['n'] < nmin: continue
            c = h[campo] / h['n']
            if best is None or c < best[0]: best = (c, b, t, h[campo], h['n'])
    return best

def area_percorso(H, p, t):
    a = sum(cella(H, p, b, t)['a90'] for b in ONPATH); nn = sum(cella(H, p, b, t)['nreg'] for b in ONPATH)
    return a / nn / cella(H, p, 'prosegue', t)['ombra'] if nn else float('nan')

def miscela(H, G, p, t, campo, mix):
    """Copertura ripesata sulla miscela, con errore tipo (metodo delta, multinomiale per comportamento)."""
    A = B = 0.0; parts = []
    for b, w in W[mix].items():
        h = cella(H, p, b, t); N = G[b]['validi']
        if not h: continue
        pa, pn = h[campo] / N, h['n'] / N; A += w * pa; B += w * pn; parts.append((w, pa, pn, N))
    if B == 0: return (float('nan'), float('nan'))
    R = A / B; var = 0.0
    for w, pa, pn, N in parts:
        var += w * w * (pa * (1 - pa) - 2 * R * pa * (1 - pn) + R * R * pn * (1 - pn)) / N
    return (R, math.sqrt(max(var, 0.0)) / B)

def punteggio_miscela(H, G, p, t, mix='squadra'):
    num = den = 0.0
    for b, w in W[mix].items():
        h = cella(H, p, b, t); N = G[b]['validi']
        if h and h['ntot'] > 0: num += w / N * h['sc']; den += w / N * h['ntot']
    return num / den if den else float('nan')

def sez(t): print('\n' + '=' * 118 + '\n' + t + '\n' + '=' * 118)

def f3(x): return '  -  ' if x != x else '%.3f' % x


# ---------------------------------------------------------------- dati
SRC = {}
for g in 'DTL':
    SRC[('banco 9000-9399', g)] = leggi_tsv(os.path.join(BANCO, 'prova_%s_pd09.tsv' % g))
    SRC[('modifiche 12000-12399', g)] = leggi_tsv(os.path.join(MODIF, 'prova_%s.tsv' % g))
SRC[('miei 20000+', 'D')] = leggi_tsv(os.path.join(MIEI, 'nuovi_D_20000x1200.tsv'))
SRC[('miei 20000+', 'T')] = leggi_tsv(os.path.join(MIEI, 'nuovi_T_20000x800.tsv'))
SRC[('miei 20000+', 'L')] = leggi_tsv(os.path.join(MIEI, 'nuovi_L_20000x400.tsv'), os.path.join(MIEI, 'nuovi_L_20400x400.tsv'))
for g in 'DTL':
    SRC[('spostato 30000-30399', g)] = leggi_tsv(os.path.join(MIEI, 'spostato_%s_30000x400.tsv' % g))
LANCI = ['banco 9000-9399', 'modifiche 12000-12399', 'miei 20000+']
def pred_di(lancio, p): return 'C-004' if (lancio.startswith('banco') and p == 'sd-1') else ('C-005' if (lancio.startswith('banco') and p == 'sd-0') else p)

# ---------------------------------------------------------------- 0. controllo del codice
sez('0. CONTROLLO: il mio eseguibile ricompilato, sui semi del banco (D, 9000-9399), rida\' le righe H di C-004 del banco?')
def righe_H(path, pred): return [l for l in open(path) if l.startswith('H\t') and l.split('\t')[3] == pred]
a = righe_H(os.path.join(MIEI, 'controllo_D_9000.tsv'), 'C-004'); b = righe_H(os.path.join(BANCO, 'prova_D_pd09.tsv'), 'C-004')
print('righe H di C-004: mie %d, del banco %d, identiche (tutti i campi) %d' % (len(a), len(b), sum(1 for x, y in zip(a, b) if x == y)))
Hc, Pc, Gc = leggi_tsv(os.path.join(MIEI, 'controllo_D_9000.tsv'))
print('sd-1 = C-004 dove C-004 emette una regione? celle H con in90 diverso fra sd-1 e C-004 sugli stessi semi: %d su 35' % sum(1 for b_ in ONPATH + OFF for t in TAUS if Hc[('sd-1', b_, t)]['in90'] != Hc[('C-004', b_, t)]['in90']))

# ---------------------------------------------------------------- 1. tabelle per comportamento e orizzonte
sez('[denominatore: %s] ' % MODO + '1. COPERTURA per comportamento e tempo senza osservazione — dentro/n, quota [Wilson 95 %]; area R90 / ombra; R50; punteggio medio della cella')
for lancio in LANCI:
    for g in 'DTL':
        H, P, G = SRC[(lancio, g)]
        for p in (['L0-nucleo', 'C-005', 'C-004'] if lancio.startswith('banco') else ['sd-0', 'sd-1']):
            print('\n--- %s | geometria %s | %s' % (lancio, g, p))
            print('%-11s %4s | %-32s | %-32s | %7s %7s | %7s' % ('comport.', 'tau', 'R90: dentro/n quota [Wilson]', 'R50: dentro/n quota [Wilson]', 'a90/omb', 'a50/omb', 'punt.'))
            for b in ONPATH + OFF:
                for t in TAUS:
                    h = cella(H, p, b, t)
                    if not h or h['n'] == 0: continue
                    l9, u9 = wilson(h['in90'], h['n']); l5, u5 = wilson(h['in50'], h['n'])
                    a9 = h['a90'] / h['nreg'] / h['ombra'] if h['nreg'] else float('nan'); a5 = h['a50'] / h['nreg'] / h['ombra'] if h['nreg'] else float('nan')
                    print('%-11s %4.1f | %4d/%-4d %.3f [%.3f-%.3f]%s | %4d/%-4d %.3f [%.3f-%.3f] | %7s %7s | %7.2f' % (b, t, h['in90'], h['n'], h['in90'] / h['n'], l9, u9, ' *' if h['n'] < 30 else '  ',
                          h['in50'], h['n'], h['in50'] / h['n'], l5, u5, f3(a9), f3(a5), h['sc'] / h['ntot']) + ('   fuori griglia %d su %d nascosti' % (h['fg'], h['ntot']) if h['fg'] else ''))

# ---------------------------------------------------------------- 2. le cifre dichiarate tornano?
sez('2. LE CIFRE DICHIARATE TORNANO? (dichiarato | ricalcolato dai grezzi | esito)')
def riga(desc, dich, ric, ok): print('%-88s | %-28s | %-34s | %s' % (desc, dich, ric, 'TORNA' if ok else 'NON TORNA'))
Hb = {g: leggi_tsv(os.path.join(BANCO, 'prova_%s_pd09.tsv' % g), modo='griglia') for g in 'DTL'}; Hm = {g: leggi_tsv(os.path.join(MODIF, 'prova_%s.tsv' % g), modo='tutti') for g in 'DTL'}
HbT = {g: leggi_tsv(os.path.join(BANCO, 'prova_%s_pd09.tsv' % g), modo='tutti') for g in 'DTL'}; HmG = {g: leggi_tsv(os.path.join(MODIF, 'prova_%s.tsv' % g), modo='griglia') for g in 'DTL'}
print('(il banco e\' ricalcolato con la SUA definizione, «griglia»; le modifiche con la LORO, «tutti»; in coda le stesse celle con la definizione scambiata)')
for g, (kd, nd) in zip('DTL', [(86, 92), (370, 386), (357, 380)]):
    m = minimo(Hb[g][0], 'C-004', ONPATH, TAUS[:4]); lo, hi = wilson(m[3], m[4])
    riga('B §2: cella peggiore di C-004 fino a 3 s, %s' % g, '%d/%d' % (kd, nd), '%d/%d = %.3f [%.3f-%.3f] (%s, %.0f s)' % (m[3], m[4], m[0], lo, hi, m[1], m[2]), (m[3], m[4]) == (kd, nd))
m = min((minimo(Hb[g][0], 'C-004', ONPATH, TAUS) + (g,) for g in 'DTL'), key=lambda x: x[0])
riga('B §2: minimo di C-004 sul percorso a 5 s (tutte le geometrie)', '0,905 (L, rallenta, 248/274)', '%.3f (%s, %s, %d/%d)' % (m[0], m[5], m[1], m[3], m[4]), abs(m[0] - 0.905) < 0.0006 and m[5] == 'L')
for p, dich in (('L0-nucleo', (19, 38, 33)), ('C-004', (99.9, 100, 100))):
    v = []
    for g in 'DTL':
        P = Hb[g][1]; v.append(100.0 * sum(P[(p, b)]['cicli_regione'] for b in ONPATH) / sum(P[(p, b)]['cicli'] for b in ONPATH))
    riga('B §2: cicli senza osservazione con una regione, %s, %%' % p, ' / '.join(str(x) for x in dich), ' / '.join('%.1f' % x for x in v), all(abs(x - y) < 0.6 for x, y in zip(v, dich)))
v = [sum(Hb[g][1][('L0-nucleo', b)]['pass_vuoto'] for b in ONPATH) for g in 'DTL']; nn = [sum(Hb[g][1][('L0-nucleo', b)]['npass'] for b in ONPATH) for g in 'DTL']
riga('B §2 e M §1: passaggi con un vuoto, nucleo (5 comportamenti sul percorso)', '1958 / 1991 / 1999 su ~2000', ' / '.join('%d su %d' % (a_, b_) for a_, b_ in zip(v, nn)), v == [1958, 1991, 1999])
v6 = [sum(Hb[g][1][('L0-nucleo', b)]['pass_vuoto'] for b in ONPATH + OFF) for g in 'DTL']; n6 = [sum(Hb[g][1][('L0-nucleo', b)]['npass'] for b in ONPATH + OFF) for g in 'DTL']
print('    (nota: sui sette comportamenti: %s)' % ' / '.join('%d su %d' % (a_, b_) for a_, b_ in zip(v6, n6)))
sc = [punteggio_miscela(Hb['T'][0], Hb['T'][2], 'C-004', t) for t in (1.0, 2.0, 3.0)]
riga('B §2: punteggio logaritmico di C-004, «squadra», T, a 1 / 2 / 3 s', '-0,19 0,97 1,40', ' '.join('%.2f' % x for x in sc), all(abs(x - y) < 0.011 for x, y in zip(sc, (-0.19, 0.97, 1.40))))
sc = [punteggio_miscela(Hb['T'][0], Hb['T'][2], 'L0-nucleo', t) for t in (1.0, 2.0, 3.0)]
riga('B §2: punteggio del nucleo (L0), «squadra», T, a 1 / 2 / 3 s', '0,80 2,52 2,53', ' '.join('%.2f' % x for x in sc), all(abs(x - y) < 0.011 for x, y in zip(sc, (0.80, 2.52, 2.53))))
r5 = [miscela(Hb['T'][0], Hb['T'][2], 'C-004', t, 'in50', 'squadra')[0] for t in (1.0, 2.0, 3.0)]
riga('B §2: R50 di C-004 sulla «squadra», T, a 1 / 2 / 3 s', '0,85 0,68 0,65', ' '.join('%.2f' % x for x in r5), all(abs(x - y) < 0.006 for x, y in zip(r5, (0.85, 0.68, 0.65))))
for p, d3, d5 in (('sd-1', ((101, 119), (252, 262), (357, 388)), ((42, 57), (51, 55), (259, 302))), ('sd-0', ((103, 119), None, None), None)):
    for i, g in enumerate('DTL'):
        m = minimo(Hm[g][0], p, ONPATH, TAUS[:4]); dich = d3[i]; cl = {'sd-1': (0.849, 0.962, 0.920), 'sd-0': (0.866, 0.911, 0.953)}[p][i]
        riga('M §2.1: %s, minimo sul percorso fino a 3 s, %s' % (p, g), '%.3f%s' % (cl, ' (%d/%d)' % dich if dich else ''), '%.3f (%d/%d, %s a %.0f s)' % (m[0], m[3], m[4], m[1], m[2]), abs(m[0] - cl) < 0.0006 and (dich is None or (m[3], m[4]) == dich))
    for i, g in enumerate('DTL'):
        m = minimo(Hm[g][0], p, ONPATH, TAUS); cl = {'sd-1': (0.737, 0.927, 0.858), 'sd-0': (0.737, 0.911, 0.898)}[p][i]
        riga('M §2.1: %s, minimo sul percorso fino a 5 s, %s' % (p, g), '%.3f' % cl, '%.3f (%d/%d, %s a %.0f s)' % (m[0], m[3], m[4], m[1], m[2]), abs(m[0] - cl) < 0.0006)
for g, dich in (('D', (0.65, 0.89, 0.98)), ('T', (0.13, 0.27, 0.35)), ('L', (0.07, 0.18, 0.30))):
    v = [area_percorso(Hm[g][0], 'sd-1', t) for t in (1.0, 2.0, 3.0)]
    riga('M §2.1: sd-1, area R90 / ombra sul percorso a 1 / 2 / 3 s, %s' % g, ' '.join('%.2f' % x for x in dich), ' '.join('%.2f' % x for x in v), all(abs(x - y) < 0.011 for x, y in zip(v, dich)))
for g, dich in (('D', (1.22, 1.54, 1.57)), ('T', (0.18, 1.06, 1.23))):
    v = [area_percorso(Hm[g][0], 'sd-0', t) for t in (1.0, 2.0, 3.0)]
    riga('M §2.1: sd-0, area R90 / ombra sul percorso a 1 / 2 / 3 s, %s' % g, ' '.join('%.2f' % x for x in dich), ' '.join('%.2f' % x for x in v), all(abs(x - y) < 0.011 for x, y in zip(v, dich)))
for p, dich in (('sd-1', (0.31, 0.76)), ('sd-0', (0.39, 0.98))):
    v = [cella(Hm[g][0], p, b, 2.0)['in90'] / cella(Hm[g][0], p, b, 2.0)['n'] for g in 'DTL' for b in OFF]
    riga('M §2.1: %s, chi svolta o esce lontano a 2 s (minimo-massimo su D, T, L)' % p, '%.2f-%.2f' % dich, '%.2f-%.2f' % (min(v), max(v)), abs(min(v) - dich[0]) < 0.006 and abs(max(v) - dich[1]) < 0.006)
v = [sum(Hm[g][1][('sd-1', b)]['pass_vuoto'] for b in ONPATH + OFF) for g in 'DTL']; nn = [sum(Hm[g][1][('sd-1', b)]['npass'] for b in ONPATH + OFF) for g in 'DTL']
riga('M §2.1: sd-1, passaggi con un ciclo senza regione', '0 / 0 / 0 su 2716 / 2800 / 2798', ' / '.join('%d su %d' % (a_, b_) for a_, b_ in zip(v, nn)), v == [0, 0, 0] and nn == [2716, 2800, 2798])
m2 = [minimo(Hm[g][0], 'sd-1', ONPATH, [0.5, 1.0, 2.0]) for g in 'TL']; m1 = minimo(Hm['D'][0], 'sd-1', ONPATH, [0.5, 1.0])
riga('M §2.1 enunciato: «fino a 2 s con ombre larghe (T, L): >= 0,96»', '>= 0,96', 'T %.3f (%d/%d, %s %.1f s); L %.3f (%d/%d, %s %.1f s)' % (m2[0][0], m2[0][3], m2[0][4], m2[0][1], m2[0][2], m2[1][0], m2[1][3], m2[1][4], m2[1][1], m2[1][2]), min(m2[0][0], m2[1][0]) >= 0.96)
riga('M §2.1 enunciato: «fino a 1 s in demo (D): >= 0,955»', '>= 0,955', '%.3f (%d/%d, %s a %.1f s)' % (m1[0], m1[3], m1[4], m1[1], m1[2]), m1[0] >= 0.955)
for i, (g, dich) in enumerate(zip('DTL', ((1136, 1149), (1044, 1046), (503, 508)))):
    k = sum(Hm[g][1][('sd-1', b)]['re40'] for b in ONPATH); n = sum(Hm[g][1][('sd-1', b)]['nre'] for b in ONPATH)
    riga('M §2.6: prima misura entro 0,40 m da R90, sul percorso, %s' % g, '%d/%d' % dich, '%d/%d = %.3f' % (k, n, k / n), (k, n) == dich)
v = [100.0 * sum(Hm[g][1][('sd-1', b)]['ampio80'] for b in ONPATH + OFF) / sum(Hm[g][1][('sd-1', b)]['cicli'] for b in ONPATH + OFF) for g in 'DTL']
riga('M §2.4: «ampio» (area > 80 % dell\'ombra), quota dei cicli, D / T / L', '50,4 / 0,0 / 0,0 %', ' / '.join('%.1f' % x for x in v), abs(v[0] - 50.4) < 0.06 and v[1] < 0.06 and v[2] < 0.06)
v = [cella(Hm[g][0], 'sd-1', 'torna', t)['in90'] / cella(Hm[g][0], 'sd-1', 'torna', t)['n'] for g in 'DTL' for t in TAUS[:4]]
riga('M §4 cond. 5: «torna 0,95-1,00 fino a 3 s»', '0,95-1,00', '%.3f-%.3f' % (min(v), max(v)), min(v) >= 0.9495)
v = [sum(cella(Hm[g][0], 'sd-1', b, t)['in100'] for b in ONPATH + OFF for t in TAUS) for g in 'DTL']; nn = [sum(cella(Hm[g][0], 'sd-1', b, t)['ntot'] for b in ONPATH + OFF for t in TAUS) for g in 'DTL']
riga('M §1: R100 contiene il nascosto (campioni)', '10883, 11772, 13236 su altrettanti', ' / '.join('%d su %d' % (a_, b_) for a_, b_ in zip(v, nn)), v == nn == [10883, 11772, 13236])

print('\nLA STESSA CELLA CON LE DUE DEFINIZIONI (minimo sul percorso fino a 3 s; D e\' l\'unica geometria dove cambiano)')
for g in 'DTL':
    for nome, A, B_, p in (('banco, C-004', Hb, HbT, 'C-004'), ('modifiche, sd-1', HmG, Hm, 'sd-1'), ('modifiche, sd-0', HmG, Hm, 'sd-0')):
        a = minimo(A[g][0], p, ONPATH, TAUS[:4]); b = minimo(B_[g][0], p, ONPATH, TAUS[:4])
        print('  %s %-16s | griglia: %d/%d = %.3f [%.3f-%.3f] (%s %.0f s) | tutti: %d/%d = %.3f [%.3f-%.3f] (%s %.0f s)' % ((g, nome, a[3], a[4], a[0]) + wilson(a[3], a[4]) + (a[1], a[2], b[3], b[4], b[0]) + wilson(b[3], b[4]) + (b[1], b[2])))
for g in 'D':
    for nome, A, B_, p in (('banco, C-004', Hb, HbT, 'C-004'), ('modifiche, sd-1', HmG, Hm, 'sd-1')):
        for t in (2.0, 3.0, 5.0):
            a = cella(A[g][0], p, 'prosegue', t); b = cella(B_[g][0], p, 'prosegue', t)
            print('  D %-16s «prosegue» %.0f s | griglia %d/%d = %.3f | tutti %d/%d = %.3f | fuori griglia %d' % (nome, t, a['in90'], a['n'], a['in90'] / a['n'], b['in90'], b['n'], b['in90'] / b['n'], b['fg']))

# ---------------------------------------------------------------- 3. soglie del triage con l'intervallo
sez('[denominatore: %s] ' % MODO + '3. SOGLIE FISSATE PRIMA (triage §6) — esito con l\'intervallo: regge = limite inferiore di Wilson >= soglia; smentita = limite superiore < soglia; altrimenti non risolta')
print('C3: R90 >= 0,85 in ogni cella sul percorso (5 comportamenti x tau; n >= 30). Per lancio: celle che reggono / non risolte / smentite; e la peggiore.')
for lim, taus in (('fino a 3 s', TAUS[:4]), ('fino a 5 s', TAUS)):
    for lancio in LANCI:
        for p in ('sd-1', 'sd-0'):
            out = []
            for g in 'DTL':
                H = SRC[(lancio, g)][0]; pp = pred_di(lancio, p); c = dict(regge=0, smentita=0); c['non risolta'] = 0; sotto = 0
                for b in ONPATH:
                    for t in taus:
                        h = cella(H, pp, b, t)
                        if h and h['n'] >= 30:
                            c[esito_soglia(h['in90'], h['n'], 0.85)] += 1; sotto += (h['in90'] / h['n'] < 0.85)
                m = minimo(H, pp, ONPATH, taus); lo, hi = wilson(m[3], m[4])
                out.append('%s: %2d/%2d/%2d (punto < 0,85: %d); peggiore %d/%d = %.3f [%.3f-%.3f] %s %.0f s' % (g, c['regge'], c['non risolta'], c['smentita'], sotto, m[3], m[4], m[0], lo, hi, m[1][:5], m[2]))
            print('  %-10s %-22s %-5s | %s' % (lim, lancio, pred_di(lancio, p), ' | '.join(out)))
print('\nRegola del triage per 30 <= n <= 199: «smentita se il limite superiore < 0,90; regge se l\'inferiore >= 0,80». Applicata alla cella peggiore di D (modifiche): 101/119')
lo, hi = wilson(101, 119); print('  Wilson [%.3f-%.3f]: superiore >= 0,90 -> non smentita; inferiore < 0,80 -> non regge: NON RISOLTA (le modifiche la danno «non superata per un millesimo» usando la regola per n = 400)' % (lo, hi))
print('  La regola non dice nulla per 200 <= n <= 399 e ammette insieme «regge» e «smentita» (esempio 170/199: [%.3f-%.3f])' % wilson(170, 199))

print('\nC3: sulle miscele R90 fra 0,85 e 0,97; R50 sulla «squadra» fra 0,40 e 0,60 (quota ripesata ± 1,96 errori tipo, metodo delta)')
for lancio in LANCI:
    for g in 'DTL':
        H, P, G = SRC[(lancio, g)]
        for p in ('sd-1', 'sd-0'):
            pp = pred_di(lancio, p); r = []
            for mix, campo in (('squadra', 'in90'), ('giurato', 'in90'), ('squadra', 'in50')):
                r.append('%s %s: ' % (mix, 'R90' if campo == 'in90' else 'R50') + ' '.join('%.3f±%.3f' % (lambda x: (x[0], 1.96 * x[1]))(miscela(H, G, pp, t, campo, mix)) for t in TAUS[:4]))
            print('  %-22s %s %-5s | %s' % (lancio, g, pp, ' | '.join(r)))

print('\nC3: area di R90 <= 0,60 dell\'ombra fino a 3 s in T e L (media sul percorso, per tau = 0,5 / 1 / 2 / 3 / 5 s); D riportata')
for lancio in LANCI:
    for p in ('sd-1', 'sd-0'):
        print('  %-22s %-5s | ' % (lancio, pred_di(lancio, p)) + ' | '.join('%s: ' % g + ' '.join('%.2f' % area_percorso(SRC[(lancio, g)][0], pred_di(lancio, p), t) for t in TAUS) for g in 'DTL'))

print('\nC1a (0 passaggi con un vuoto), C4 (0 cicli di R90 su visto libero oltre la fascia; R90 dentro R100), R100 = 100 %; limite superiore al 95 % della quota vera con 0 su n (regola del tre: 3/n)')
for lancio in LANCI:
    for p in ('sd-1', 'sd-0'):
        out = []
        for g in 'DTL':
            H, P, G = SRC[(lancio, g)]; pp = pred_di(lancio, p); bb = ONPATH + OFF
            np_ = sum(P[(pp, b)]['npass'] for b in bb); vu = sum(P[(pp, b)]['pass_vuoto'] for b in bb); v5 = sum(P[(pp, b)]['pass_vuoto_dopo5'] for b in bb)
            lib = sum(P[(pp, b)]['R90lib'] for b in bb); fu = sum(P[(pp, b)]['R90fuori'] for b in bb)
            k100 = sum(cella(H, pp, b, t)['in100'] for b in bb for t in TAUS); n100 = sum(cella(H, pp, b, t)['ntot'] for b in bb for t in TAUS)
            out.append('%s: vuoti %d (dopo 5 cicli %d) su %d [<= %.4f]; R90 su libero %d cicli; fuori R100 %d; R100 %d/%d' % (g, vu, v5, np_, clopper(vu, np_)[1], lib, fu, k100, n100))
        print('  %-22s %-5s | %s' % (lancio, pred_di(lancio, p), ' | '.join(out)))

# ---------------------------------------------------------------- 4. tre lanci dello stesso codice: eterogeneita' e riunione
sez('[denominatore: %s] ' % MODO + '4. STESSO CODICE, SEMI DIVERSI (banco C-004 = sd-1 dove c\'e\' una regione; modifiche; miei): eterogeneita\' e conteggi riuniti, sd-1 / C-004')
print('%-3s %-11s %4s | %-13s %-13s %-13s | chi2(2) p     | riuniti: dentro/n quota [Wilson]            | esito >= 0,85 | esito >= 0,90' % ('geo', 'comport.', 'tau', 'banco', 'modifiche', 'miei'))
npv = 0; nsig = 0; riun = {}
for g in 'DTL':
    for b in ONPATH + OFF:
        for t in TAUS:
            cc = []
            for lancio in LANCI:
                h = cella(SRC[(lancio, g)][0], pred_di(lancio, 'sd-1'), b, t); cc.append((h['in90'], h['n']))
            K = sum(k for k, n in cc); N = sum(n for k, n in cc); x, gr, pv = chi2_omog(cc); lo, hi = wilson(K, N); riun[(g, b, t)] = (K, N)
            if b in ONPATH: npv += 1; nsig += (pv < 0.05)
            print('%-3s %-11s %4.1f | %s | %6.2f %.4f%s | %5d/%-5d %.3f [%.3f-%.3f] | %-13s | %s' % (g, b, t, ' '.join('%4d/%-4d %.3f' % (k, n, k / n if n else float('nan')) for k, n in cc), x, pv, '*' if pv < 0.05 else ' ', K, N, K / N, lo, hi,
                  esito_soglia(K, N, 0.85) if b in ONPATH else '(fuori perc.)', esito_soglia(K, N, 0.90) if b in ONPATH else ''))
print('celle sul percorso con p < 0,05: %d su %d (attese per caso: %.1f)' % (nsig, npv, 0.05 * npv))
print('\nRIUNITI, sul percorso: celle per esito (soglia 0,85 | soglia 0,90), per geometria e orizzonte massimo')
for g in 'DTL':
    for lim, taus in (('<= 1 s', TAUS[:2]), ('<= 2 s', TAUS[:3]), ('<= 3 s', TAUS[:4]), ('<= 5 s', TAUS)):
        c85 = {}; c90 = {}; mn = None
        for b in ONPATH:
            for t in taus:
                K, N = riun[(g, b, t)]; e = esito_soglia(K, N, 0.85); c85[e] = c85.get(e, 0) + 1; e = esito_soglia(K, N, 0.90); c90[e] = c90.get(e, 0) + 1
                if mn is None or K / N < mn[0]: mn = (K / N, K, N, b, t)
        lo, hi = wilson(mn[1], mn[2])
        print('  %s %-6s | 0,85: regge %2d, non risolta %2d, smentita %2d | 0,90: regge %2d, non risolta %2d, smentita %2d | peggiore %d/%d = %.3f [%.3f-%.3f] (%s, %.1f s)' % (g, lim, c85.get('regge', 0), c85.get('non risolta', 0), c85.get('smentita', 0),
              c90.get('regge', 0), c90.get('non risolta', 0), c90.get('smentita', 0), mn[1], mn[2], mn[0], lo, hi, mn[3], mn[4]))
print('\nConfronto diretto della cella «prosegue» a 3 s in D: banco contro modifiche (Fisher esatto, due code)')
hb = cella(SRC[('banco 9000-9399', 'D')][0], 'C-004', 'prosegue', 3.0); hm = cella(SRC[('modifiche 12000-12399', 'D')][0], 'sd-1', 'prosegue', 3.0); hn = cella(SRC[('miei 20000+', 'D')][0], 'sd-1', 'prosegue', 3.0)
print('  banco %d/%d = %.3f; modifiche %d/%d = %.3f; miei %d/%d = %.3f; Fisher banco-modifiche p = %.4f; banco-miei p = %.4f; modifiche-miei p = %.4f' % (hb['in90'], hb['n'], hb['in90'] / hb['n'], hm['in90'], hm['n'], hm['in90'] / hm['n'], hn['in90'], hn['n'], hn['in90'] / hn['n'],
      fisher2(hb['in90'], hb['n'], hm['in90'], hm['n']), fisher2(hb['in90'], hb['n'], hn['in90'], hn['n']), fisher2(hm['in90'], hm['n'], hn['in90'], hn['n'])))
mb = minimo(SRC[('banco 9000-9399', 'D')][0], 'C-004', ONPATH, TAUS[:4]); print('  la cella peggiore del banco in D era: %s a %.0f s (%d/%d): %s' % (mb[1], mb[2], mb[3], mb[4], 'stessa cella' if (mb[1], mb[2]) == ('prosegue', 3.0) else 'ALTRA cella'))
print('  «il minimo di 20 celle sta sotto 0,85» quando ogni cella vale davvero 0,90: P(k/n < 0,85) con n = 92: %.3f; n = 119: %.3f; n = 400: %.4f' % (binom_cdf(math.ceil(0.85 * 92) - 1, 92, 0.9), binom_cdf(math.ceil(0.85 * 119) - 1, 119, 0.9), binom_cdf(339, 400, 0.9)))

# ---------------------------------------------------------------- 4b. i passaggi di un lancio sono indipendenti?
sez('[denominatore: %s] ' % MODO + '4b. SOVRADISPERSIONE: i semi consecutivi di gen.h leggono lo stesso flusso spostato di uno (ris/prova_semi.txt). Dieci blocchi D da 400 semi, lontani fra loro')
def chi2_sf(x, k):  # P(chi2_k > x): gamma incompleta regolarizzata superiore, serie o frazione continua
    a = k / 2.0; x = x / 2.0
    if x <= 0: return 1.0
    if x < a + 1:
        ap = a; d = s_ = 1.0 / a
        for _ in range(500):
            ap += 1; d *= x / ap; s_ += d
            if abs(d) < abs(s_) * 1e-14: break
        return max(0.0, 1.0 - s_ * math.exp(-x + a * math.log(x) - math.lgamma(a)))
    b = x + 1 - a; c = 1e300; d = 1.0 / b; h = d
    for i in range(1, 500):
        an = -i * (i - a); b += 2; d = an * d + b; d = 1e-300 if abs(d) < 1e-300 else d; c = b + an / c; c = 1e-300 if abs(c) < 1e-300 else c; d = 1.0 / d; de = d * c; h *= de
        if abs(de - 1) < 1e-14: break
    return min(1.0, math.exp(-x + a * math.log(x) - math.lgamma(a)) * h)
BLOCCHI = [('banco 9000', leggi_tsv(os.path.join(BANCO, 'prova_D_pd09.tsv')), 'C-004'), ('modifiche 12000', leggi_tsv(os.path.join(MODIF, 'prova_D.tsv')), 'sd-1')]
for s0 in range(40000, 80000, 5000): BLOCCHI.append(('miei %d' % s0, leggi_tsv(os.path.join(MIEI, 'blocco_D_%dx400.tsv' % s0)), 'sd-1'))
print('fuori griglia fra i nascosti, «prosegue» a 3 s, per blocco: ' + ' '.join('%d/%d' % (X[0][(p, 'prosegue', 3.0)]['fg'], X[0][(p, 'prosegue', 3.0)]['ntot']) for nome, X, p in BLOCCHI))
print('%-11s %4s | %-110s | chi2(9)  p      chi2/9' % ('comport.', 'tau', 'copertura per blocco (banco, modifiche, 40000 ... 75000)'))
rapporti = {}; DEFF = {}
for b in ONPATH + OFF:
    for t in TAUS:
        cc = [(X[0][(p, b, t)]['in90'], X[0][(p, b, t)]['n']) for nome, X, p in BLOCCHI]; x, g, _ = chi2_omog(cc); pv = chi2_sf(x, g)
        K = sum(k for k, n in cc); N = sum(n for k, n in cc)
        if 0 < K < N: rapporti[(b, t)] = x / g
        print('%-11s %4.1f | %-110s | %7.2f %.4f %5.2f%s' % (b, t, ' '.join('%.3f' % (k / n) if n else '  -  ' for k, n in cc), x, pv, x / g, ' *' if pv < 0.05 else ''))
for nome, sel in (('sul percorso, fino a 3 s', lambda b, t: b in ONPATH and t <= 3.0), ('sul percorso, tau >= 2 s', lambda b, t: b in ONPATH and t >= 2.0), ('sul percorso, tau <= 1 s', lambda b, t: b in ONPATH and t <= 1.0),
                  ('«prosegue» e «rallenta»', lambda b, t: b in ('prosegue', 'rallenta')), ('fuori percorso', lambda b, t: b in OFF)):
    v = [r for (b, t), r in rapporti.items() if sel(b, t)]; DEFF[nome] = sum(v) / len(v)
    print('  effetto del disegno (media di chi2/gradi), %-26s: %.2f su %d celle (massimo %.2f)  -> 400 passaggi ne valgono circa %.0f' % (nome, DEFF[nome], len(v), max(v), 400 / max(1.0, DEFF[nome])))
d3 = max(1.0, DEFF['sul percorso, fino a 3 s']); dmax = max(r for (b, t), r in rapporti.items() if b in ONPATH and t <= 3.0)
print('\nD, undici lanci riuniti (i dieci blocchi + il mio lancio da 1200 semi): cella per cella, intervallo binomiale e intervallo allargato con l\'effetto del disegno medio (%.2f) e con il massimo (%.2f)' % (d3, dmax))
Hn = SRC[('miei 20000+', 'D')][0]
for b in ONPATH:
    for t in TAUS:
        K = sum(X[0][(p, b, t)]['in90'] for nome, X, p in BLOCCHI) + Hn[('sd-1', b, t)]['in90']; N = sum(X[0][(p, b, t)]['n'] for nome, X, p in BLOCCHI) + Hn[('sd-1', b, t)]['n']
        lo, hi = wilson(K, N); l2, h2 = wilson(K / d3, N / d3); l3, h3 = wilson(K / dmax, N / dmax)
        e = 'regge' if l3 >= 0.85 else ('smentita' if h3 < 0.85 else 'non risolta')
        print('  %-11s %4.1f | %5d/%-5d %.3f | binomiale [%.3f-%.3f] | allargato medio [%.3f-%.3f] | allargato massimo [%.3f-%.3f] -> >= 0,85: %s' % (b, t, K, N, K / N, lo, hi, l2, h2, l3, h3, e))
print('\nT e L: solo tre lanci (400, 400, 800 semi): media di chi2/2 sulle celle sul percorso (stima grossolana dello stesso effetto)')
for g in 'TL':
    v = []
    for b in ONPATH:
        for t in TAUS:
            cc = []
            for lancio in LANCI:
                h = cella(SRC[(lancio, g)][0], pred_di(lancio, 'sd-1'), b, t); cc.append((h['in90'], h['n']))
            K = sum(k for k, n in cc); N = sum(n for k, n in cc)
            if 0 < K < N: v.append(chi2_omog(cc)[0] / 2)
    print('  %s: %.2f su %d celle (massimo %.2f)' % (g, sum(v) / len(v), len(v), max(v)))

# ---------------------------------------------------------------- 4c. semi riparati
sez('[denominatore: %s] ' % MODO + '4c. SEMI RIPARATI (codice_semi/: stato iniziale mescolato, taratura rifatta sui semi 1000-1199, tre passate): passaggi indipendenti; semi 80000+')
# intervallo per blocchi sui dieci blocchi originali (stimatore a rapporto, t di Student a 9 gradi = 2,262)
def per_blocchi(cc, tq):
    m = len(cc); K = sum(k for k, n in cc); N = sum(n for k, n in cc); R = K / N; nb = N / m
    v = sum((k - R * n) ** 2 for k, n in cc) / (m * (m - 1)) / (nb * nb); h = tq * math.sqrt(v); return (R, R - h, R + h)
print('Semi ORIGINALI, D, dieci blocchi: intervallo per blocchi (ogni blocco di 400 semi consecutivi e\' un grappolo), sd-1')
for b in ('prosegue', 'rallenta'):
    for t in TAUS:
        cc = [(X[0][(p, b, t)]['in90'], X[0][(p, b, t)]['n']) for nome, X, p in BLOCCHI]; R, lo, hi = per_blocchi(cc, 2.262)
        print('  %-9s %.1f s: %.3f [%.3f-%.3f]  (blocchi: minimo %.3f, massimo %.3f)' % (b, t, R, lo, hi, min(k / n for k, n in cc), max(k / n for k, n in cc)))
RIP = [leggi_tsv(os.path.join(MIEI, 'semi_D_%dx400.tsv' % s0)) for s0 in (80000, 80400, 80800, 81200, 81600)]
print('\nSemi RIPARATI, D, cinque blocchi da 400: omogeneita\' (chi2 a 4 gradi)')
rr = []
for b in ONPATH:
    for t in TAUS[:4]:
        cc = [(X[0][('sd-1', b, t)]['in90'], X[0][('sd-1', b, t)]['n']) for X in RIP]; x, g, _ = chi2_omog(cc); K = sum(k for k, n in cc); N = sum(n for k, n in cc)
        if 0 < K < N: rr.append(x / g)
        print('  %-11s %.1f | %s | chi2/4 = %.2f  p = %.3f' % (b, t, ' '.join('%.3f' % (k / n) for k, n in cc), x / g, chi2_sf(x, g)))
print('  media di chi2/gradi sulle celle sul percorso fino a 3 s: %.2f su %d celle (massimo %.2f); con i semi originali era %.2f' % (sum(rr) / len(rr), len(rr), max(rr), DEFF['sul percorso, fino a 3 s']))
print('  fuori griglia fra i nascosti, «prosegue» a 3 s, per blocco: ' + ' '.join('%d/%d' % (X[0][('sd-1', 'prosegue', 3.0)]['fg'], X[0][('sd-1', 'prosegue', 3.0)]['ntot']) for X in RIP))
SRC[('riparati 80000+', 'D')] = leggi_tsv(*[os.path.join(MIEI, 'semi_D_%dx400.tsv' % s0) for s0 in (80000, 80400, 80800, 81200, 81600)])
SRC[('riparati 80000+', 'T')] = leggi_tsv(os.path.join(MIEI, 'semi_T_80000x400.tsv'), os.path.join(MIEI, 'semi_T_80400x400.tsv'))
SRC[('riparati 80000+', 'L')] = leggi_tsv(os.path.join(MIEI, 'semi_L_80000x400.tsv'), os.path.join(MIEI, 'semi_L_80400x400.tsv'))
for g in 'DTL':
    H, P, G = SRC[('riparati 80000+', g)]
    for p in ('sd-1', 'sd-0'):
        print('\n--- riparati | %s | %s | passaggi validi %s' % (g, p, ' '.join('%s %d' % (b[:5], G[b]['validi']) for b in ONPATH + OFF)))
        print('%-11s %4s | %-34s | %7s | %-12s %-12s' % ('comport.', 'tau', 'R90: dentro/n quota [Wilson 95 %]', 'a90/omb', '>= 0,85', '>= 0,90'))
        for b in ONPATH + OFF:
            for t in TAUS:
                h = cella(H, p, b, t)
                if not h or h['n'] == 0: continue
                lo, hi = wilson(h['in90'], h['n']); a9 = h['a90'] / h['nreg'] / h['ombra'] if h['nreg'] else float('nan')
                print('%-11s %4.1f | %4d/%-4d %.3f [%.3f-%.3f]%s     | %7s | %-12s %-12s%s' % (b, t, h['in90'], h['n'], h['in90'] / h['n'], lo, hi, ' *' if h['n'] < 30 else '  ', f3(a9),
                      esito_soglia(h['in90'], h['n'], 0.85) if b in ONPATH else '', esito_soglia(h['in90'], h['n'], 0.90) if b in ONPATH else '', '  fuori griglia %d' % h['fg'] if h['fg'] else ''))
        for lim, taus in (('<= 1 s', TAUS[:2]), ('<= 2 s', TAUS[:3]), ('<= 3 s', TAUS[:4]), ('<= 5 s', TAUS)):
            m = minimo(H, p, ONPATH, taus); c = {}
            for b in ONPATH:
                for t in taus:
                    h = cella(H, p, b, t)
                    if h and h['n'] >= 30: e = esito_soglia(h['in90'], h['n'], 0.85); c[e] = c.get(e, 0) + 1
            print('  minimo sul percorso %s: %d/%d = %.3f [%.3f-%.3f] (%s, %.1f s); celle >= 0,85: regge %d, non risolta %d, smentita %d' % ((lim, m[3], m[4], m[0]) + wilson(m[3], m[4]) + (m[1], m[2], c.get('regge', 0), c.get('non risolta', 0), c.get('smentita', 0))))
        bb = ONPATH + OFF
        print('  area/ombra sul percorso a 0,5/1/2/3/5 s: ' + ' '.join('%.2f' % area_percorso(H, p, t) for t in TAUS) + ' | vuoti: %d su %d passaggi | R90 su libero: %d cicli | R100: %d/%d | «ampio» >80 %%: %.1f %% dei cicli' % (
              sum(P[(p, b)]['pass_vuoto'] for b in bb), sum(P[(p, b)]['npass'] for b in bb), sum(P[(p, b)]['R90lib'] for b in bb), sum(cella(H, p, b, t)['in100'] for b in bb for t in TAUS), sum(cella(H, p, b, t)['ntot'] for b in bb for t in TAUS),
              100.0 * sum(P[(p, b)]['ampio80'] for b in bb) / sum(P[(p, b)]['cicli'] for b in bb)))
        print('  miscele R90 a 0,5/1/2/3 s: ' + ' | '.join('%s ' % mix + ' '.join('%.3f±%.3f' % (lambda x: (x[0], 1.96 * x[1]))(miscela(H, G, p, t, 'in90', mix)) for t in TAUS[:4]) for mix in ('squadra', 'giurato')))
        re = sum(P[(p, b)]['re40'] for b in ONPATH); nre = sum(P[(p, b)]['nre'] for b in ONPATH); re2 = sum(P[(p, b)]['re40'] for b in OFF); nre2 = sum(P[(p, b)]['nre'] for b in OFF)
        print('  contatore «prima misura entro 0,40 m da R90»: sul percorso %d/%d = %.3f; svolta + lontano %d/%d = %.3f' % (re, nre, re / nre, re2, nre2, re2 / nre2))

# ---------------------------------------------------------------- 5. spostamento
sez('[denominatore: %s] ' % MODO + '5. SPOSTAMENTO DELLA DISTRIBUZIONE')
print('5a. MIO: camminatori meno regolari (velocita\' 15 %, rotta 8 gradi, rotta entro ±30 gradi), taratura e libreria FERME; semi 30000-30399. sd-1 e sd-0: R90 dentro/n [Wilson]; area/ombra')
for g in 'DTL': SRC[('riparati spostato 90000-90399', g)] = leggi_tsv(os.path.join(MIEI, 'semi_spostato_%s_90000x400.tsv' % g))
for fonte, g in [(f, g) for f in ('spostato 30000-30399', 'riparati spostato 90000-90399') for g in 'DTL']:
    H, P, G = SRC[(fonte, g)]
    for p in ('sd-1', 'sd-0'):
        print('  --- %s | %s %s' % (fonte, g, p))
        for b in ONPATH + OFF:
            print('    %-11s ' % b + '  '.join('%4d/%-4d %.3f [%.2f-%.2f]' % ((h['in90'], h['n'], h['in90'] / h['n']) + wilson(h['in90'], h['n'])) if (h := cella(H, p, b, t)) and h['n'] else '-' for t in TAUS))
        print('    area/ombra sul percorso: ' + ' '.join('%.2f' % area_percorso(H, p, t) for t in TAUS) + '; passaggi con un vuoto: %d; «ampio» (>80 %%): %.1f %% dei cicli; R100: %d/%d' % (sum(P[(p, b)]['pass_vuoto'] for b in ONPATH + OFF),
              100.0 * sum(P[(p, b)]['ampio80'] for b in ONPATH + OFF) / sum(P[(p, b)]['cicli'] for b in ONPATH + OFF), sum(cella(H, p, b, t)['in100'] for b in ONPATH + OFF for t in TAUS), sum(cella(H, p, b, t)['ntot'] for b in ONPATH + OFF for t in TAUS)))
        for lim, taus in (('<= 1 s', TAUS[:2]), ('<= 2 s', TAUS[:3]), ('<= 3 s', TAUS[:4])):
            m = minimo(H, p, ONPATH, taus); print('    minimo sul percorso %s: %d/%d = %.3f [%.3f-%.3f] (%s, %.1f s) -> %s' % ((lim, m[3], m[4], m[0]) + wilson(m[3], m[4]) + (m[1], m[2], esito_soglia(m[3], m[4], 0.85))))

print('\n5b. BRACCI DEL BANCO (T): C-004 e C-005, minimo sul percorso fino a 3 s, con intervallo')
for nome, f in (('rilevamento 1,0', 'prova_T_pd10.tsv'), ('rilevamento 0,7', 'braccio_T_pd07.tsv'), ('ombra -20 cm con fascia', 'braccio_T_ombra-20_fascia.tsv'), ('ombra -20 cm senza fascia', 'braccio_T_ombra-20_senzafascia.tsv'),
                ('rumore 4/9/16 cm, R e taratura ferme', 'braccio_T_rumore_curva.tsv'), ('rumore 4/9/16 cm, R e taratura rifatte', 'braccio_T_rumore_curva_noto.tsv')):
    H, P, G = leggi_tsv(os.path.join(BANCO, f)); r = []
    for p in ('C-004', 'C-005'):
        m = minimo(H, p, ONPATH, TAUS[:4]); r.append('%s %d/%d = %.3f [%.3f-%.3f] (%s %.1f s) %s' % ((p, m[3], m[4], m[0]) + wilson(m[3], m[4]) + (m[1][:5], m[2], esito_soglia(m[3], m[4], 0.85))))
    print('  %-40s | %s' % (nome, ' | '.join(r)))

print('\n5c. TORNEO (generatore, sensore e riscrittura di C-004 indipendenti; conteggi ricostruiti da quota x n). C004: minimo sul percorso fino a 3 s e a 5 s')
for nome in sorted(os.listdir(TORNEO)):
    try: d = leggi_torneo(os.path.join(TORNEO, nome))
    except Exception as e: print('  %-26s non letto (%s)' % (nome, e)); continue
    behs = sorted({b for (c, b, t) in d if c == 'C004'}); on = [b for b in behs if b not in ('svolta', 'lontano', 'versosens', 'verso')]
    if not on: continue
    r = []
    for taus in (TAUS[:4], TAUS):
        best = None
        for b in on:
            for t in taus:
                h = d.get(('C004', b, t))
                if h and h['n'] >= 30 and (best is None or h['in90'] / h['n'] < best[0]): best = (h['in90'] / h['n'], b, t, h['in90'], h['n'])
        r.append('%d/%d = %.3f [%.3f-%.3f] (%s %.1f s) %s' % ((best[3], best[4], best[0]) + wilson(best[3], best[4]) + (best[1][:9], best[2], esito_soglia(best[3], best[4], 0.85))) if best else '-')
    print('  %-26s comportamenti %-60s | <=3 s: %s | <=5 s: %s' % (nome, ','.join(behs)[:60], r[0], r[1]))
d = leggi_torneo(os.path.join(TORNEO, 'base_T.txt'))
for mix in ('squadra', 'giurato'):
    out = []
    for t in (2.0, 3.0):
        A = sum(w * d[('C004', b, t)]['in90'] / 400.0 for b, w in W[mix].items()); B = sum(w * d[('C004', b, t)]['n'] / 400.0 for b, w in W[mix].items()); out.append('%.3f' % (A / B))
    print('  torneo base_T, C004, miscela «%s» a 2 / 3 s: %s   (dichiarato per «giurato»: 0,884 / 0,809)' % (mix, ' / '.join(out)))

# ---------------------------------------------------------------- 6. il contatore dal vivo misura la copertura?
sez('[denominatore: %s] ' % MODO + '6. «RICOMPARSO DENTRO LA ZONA» (prima misura entro 0,40 m da R90) contro la COPERTURA di R90 (soggetto nascosto dentro la regione) — sd-1, lanci riuniti modifiche + miei')
for g in 'DTL':
    for grp, bb in (('sul percorso', ONPATH), ('svolta + lontano', OFF)):
        re = nre = 0
        for lancio in LANCI[1:]:
            P = SRC[(lancio, g)][1]; re += sum(P[('sd-1', b)]['re40'] for b in bb); nre += sum(P[('sd-1', b)]['nre'] for b in bb)
        cov = []
        for t in (1.0, 2.0, 3.0):
            k = sum(cella(SRC[(l, g)][0], 'sd-1', b, t)['in90'] for l in LANCI[1:] for b in bb); n = sum(cella(SRC[(l, g)][0], 'sd-1', b, t)['n'] for l in LANCI[1:] for b in bb); cov.append('%.3f (%d/%d)' % (k / n, k, n))
        print('  %s %-17s | contatore: %d/%d = %.3f [%.3f-%.3f] | copertura vera di R90 a 1 / 2 / 3 s (comportamenti in parti uguali): %s' % ((g, grp, re, nre, re / nre) + wilson(re, nre) + (' ; '.join(cov),)))
print('  cella «prosegue» in D (riuniti modifiche + miei):')
for t in (2.0, 3.0, 5.0):
    k = sum(cella(SRC[(l, 'D')][0], 'sd-1', 'prosegue', t)['in90'] for l in LANCI[1:]); n = sum(cella(SRC[(l, 'D')][0], 'sd-1', 'prosegue', t)['n'] for l in LANCI[1:]); print('    copertura a %.0f s: %d/%d = %.3f' % (t, k, n, k / n))
re = sum(SRC[(l, 'D')][1][('sd-1', 'prosegue')]['re40'] for l in LANCI[1:]); nre = sum(SRC[(l, 'D')][1][('sd-1', 'prosegue')]['nre'] for l in LANCI[1:]); print('    contatore su «prosegue» in D: %d/%d = %.3f' % (re, nre, re / nre))

# ---------------------------------------------------------------- 7. numerosita' per l'hardware
sez('7. HARDWARE: quante occlusioni per dichiarare una copertura con intervallo ±0,10 (Wilson 95 %), e che cosa si puo\' dire con n piccolo')
def semi(k, n): lo, hi = wilson(k, n); return (hi - lo) / 2
print('n minimo perche\' la semiampiezza di Wilson sia <= 0,10 se la quota osservata e\' p:')
for p in (0.50, 0.70, 0.80, 0.85, 0.90, 0.95):
    n = 5
    while semi(round(p * n), n) > 0.10 or any(semi(round(p * m), m) > 0.10 for m in range(n, n + 15)): n += 1
    print('  p osservata %.2f: n = %d   (Clopper-Pearson a n: [%.3f-%.3f])' % ((p, n) + clopper(round(p * n), n)))
print('probabilita\' che con n occlusioni la semiampiezza osservata esca <= 0,10, se la copertura vera e\' P:')
for P_ in (0.85, 0.90, 0.95):
    row = []
    for n in (20, 30, 35, 40, 45, 50, 60, 80):
        pr = sum(math.exp(lbin(n, k) + k * math.log(P_) + (n - k) * math.log(1 - P_)) for k in range(n + 1) if semi(k, n) <= 0.10); row.append('n=%d: %.2f' % (n, pr))
    print('  vera %.2f | %s' % (P_, '  '.join(row)))
print('che cosa dice il tabellone con n piccolo (dentro k su n -> Wilson 95 %; «almeno 0,80» solo se il limite inferiore >= 0,80):')
for n in (5, 10, 15, 20, 30, 40, 50, 60, 100):
    kmin = next((k for k in range(n + 1) if wilson(k, n)[0] >= 0.80), None)
    r = []
    for k in sorted({n, n - 1, round(0.9 * n)}, reverse=True):
        lo, hi = wilson(k, n); r.append('%d/%d: [%.2f-%.2f]' % (k, n, lo, hi))
    pw = '-' if kmin is None else '%.2f / %.2f / %.2f' % tuple(1 - binom_cdf(kmin - 1, n, q) for q in (0.80, 0.90, 0.95))
    print('  n = %3d | %s | per dire «almeno 0,80» servono >= %s dentro | probabilita\' di poterlo dire se il vero e\' 0,80 / 0,90 / 0,95: %s' % (n, '  '.join(r), kmin, pw))
print('effetto del raggruppamento per camminatore (m passaggi a testa, correlazione intraclasse rho): n efficace = n / (1 + (m-1) rho)')
for m, rho in ((10, 0.05), (10, 0.2), (20, 0.2)): print('  m = %d, rho = %.2f: 40 passaggi valgono %.0f' % (m, rho, 40 / (1 + (m - 1) * rho)))

# ---------------------------------------------------------------- 8. tabella compatta per comportamento (semi riparati)
sez('[denominatore: %s] ' % MODO + '8. TABELLA COMPATTA per comportamento e tempo senza osservazione — semi riparati (passaggi indipendenti): quota (n) a 0,5 / 1 / 2 / 3 / 5 s')
for g in 'DTL':
    H, P, G = SRC[('riparati 80000+', g)]
    for p, campo in (('L0-nucleo', 'in90'), ('sd-0', 'in90'), ('sd-1', 'in90'), ('C-004', 'in50'), ('C-005', 'in50')):
        print('--- %s | %s | %s' % (g, p, 'R90' if campo == 'in90' else 'R50 (livello dichiarato 50 %)'))
        for b in ONPATH + OFF:
            print('   %-11s ' % b + '  '.join('%.3f (%4d)' % (h[campo] / h['n'], h['n']) if (h := cella(H, p, b, t)) and h['n'] else '     -     ' for t in TAUS))
        bb = ONPATH
        print('   cicli senza osservazione con una regione: %.1f %%; passaggi con un vuoto %d su %d (sul percorso)' % (100.0 * sum(P[(p, b)]['cicli_regione'] for b in bb) / sum(P[(p, b)]['cicli'] for b in bb), sum(P[(p, b)]['pass_vuoto'] for b in bb), sum(P[(p, b)]['npass'] for b in bb)))
    print('--- %s | punteggio logaritmico medio sulla «squadra» a 0,5/1/2/3/5 s (piu\' basso e\' meglio); area R90 / ombra sul percorso' % g)
    for p in ('L0-nucleo', 'L2q-q0.01', 'C-005', 'C-004', 'sd-0', 'sd-1'):
        print('   %-10s punteggio %s | area %s | R90 «squadra» %s | R50 «squadra» %s' % (p, ' '.join('%5.2f' % punteggio_miscela(H, G, p, t) for t in TAUS), ' '.join('%.2f' % area_percorso(H, p, t) if sum(cella(H, p, b, t)['nreg'] for b in ONPATH) else '  - ' for t in TAUS),
              ' '.join('%.3f' % miscela(H, G, p, t, 'in90', 'squadra')[0] for t in TAUS), ' '.join('%.3f' % miscela(H, G, p, t, 'in50', 'squadra')[0] for t in TAUS)))

# ---------------------------------------------------------------- 9. C-EST (candidata nominata), dal banco: le cifre dichiarate tornano?
sez('9. C-EST dal banco (semi 9000-9399, denominatore del banco): attacco 5 (prima misura nell\'ellisse al 95 % dichiarata), K-206 («sosta» a 3 s), K-201 (passaggi con cicli «perso»)')
for g in 'DTL':
    path = os.path.join(BANCO, 'prova_%s_pd09.tsv' % g); Hg, Pg, Gg = leggi_tsv(path, modo='griglia'); porta = {}; perso = {}
    for line in open(path):
        f = line.rstrip('\n').split('\t')
        if f[0] == 'P' and f[2] == 'prosegue' and f[3] in ('C-EST-A', 'C-EST-B'):
            k, n = kv(f[4:])['porta95'][0].split('/'); porta[f[3]] = (int(k), int(n))
        if f[0] == 'E' and f[3] in ('C-EST-A', 'C-EST-B') and f[2] in ONPATH:
            d = kv(f[4:]); perso[f[3]] = perso.get(f[3], 0) + int(d['pass_perso'][0])
    for v in ('C-EST-A', 'C-EST-B'):
        k, n = porta[v]; h = cella(Hg, v, 'sosta', 3.0)
        print('  %s %s | attacco 5, «prosegue»: %d/%d = %.3f [%.3f-%.3f] (soglia 0,90-0,95: %s) | «sosta» a 3 s: %d/%d = %.3f [%.3f-%.3f] (soglia 0,85: %s) | passaggi sul percorso con cicli «perso»: %d su %d' % (
            (g, v, k, n, k / n) + wilson(k, n) + (esito_soglia(k, n, 0.90),) + (h['in90'], h['n'], h['in90'] / h['n']) + wilson(h['in90'], h['n']) + (esito_soglia(h['in90'], h['n'], 0.85), perso[v], sum(Gg[b]['validi'] for b in ONPATH))))
print('  dichiarato (B §4): attacco 5 A 0,28 / 0,30 / 0,00, B 0,997 / 0,71 / 0,00; «sosta» a 3 s 0,95 e 1,00 (D), 0,72 e 0,53 (T), 0,14 e 0,00 (L); cicli «perso» 374 e 1312 su 2000 (T), 1976 e 1987 (L), 2 (D)')

# ---------------------------------------------------------------- 10. il contatore vede una regione troppo stretta?
sez('[denominatore: %s] ' % MODO + '10. IL CONTATORE ALLA RICOMPARSA VEDE UNA REGIONE TROPPO SICURA? Braccio q = 0,01 (deve fallire) contro sd-1, semi riparati, sul percorso')
for g in 'DTL':
    H, P, G = SRC[('riparati 80000+', g)]
    for p in ('L2q-q0.01', 'L2r-filtro-ritagliato', 'sd-0', 'sd-1'):
        re = sum(P[(p, b)]['re40'] for b in ONPATH); nre = sum(P[(p, b)]['nre'] for b in ONPATH); cov = []
        for t in (1.0, 2.0, 3.0):
            k = sum(cella(H, p, b, t)['in90'] for b in ONPATH); n = sum(cella(H, p, b, t)['n'] for b in ONPATH); cov.append('%.3f' % (k / n))
        mn = minimo(H, p, ONPATH, TAUS[:4])
        print('  %s %-22s | contatore (prima misura entro 0,40 m da R90): %d/%d = %.3f | copertura sul percorso a 1 / 2 / 3 s (comportamenti in parti uguali): %s | cella peggiore fino a 3 s: %.3f (%s, %.1f s)' % (g, p, re, nre, re / nre if nre else float('nan'), ' '.join(cov), mn[0], mn[1], mn[2]))
print('  Bracci del banco (T, semi 9000-9399, C-004, sul percorso): contatore alla ricomparsa contro cella peggiore fino a 3 s')
for nome, f in (('base, rilevamento 0,9', 'prova_T_pd09.tsv'), ('ombra -20 cm senza fascia', 'braccio_T_ombra-20_senzafascia.tsv'), ('ombra -20 cm con fascia', 'braccio_T_ombra-20_fascia.tsv'), ('rumore 4/9/16 cm, R e taratura ferme', 'braccio_T_rumore_curva.tsv')):
    H, P, G = leggi_tsv(os.path.join(BANCO, f)); re = sum(P[('C-004', b)]['re40'] for b in ONPATH); nre = sum(P[('C-004', b)]['nre'] for b in ONPATH); m = minimo(H, 'C-004', ONPATH, TAUS[:4])
    print('    %-38s | contatore %d/%d = %.3f | cella peggiore %d/%d = %.3f [%.3f-%.3f] (%s, %.1f s)' % ((nome, re, nre, re / nre, m[3], m[4], m[0]) + wilson(m[3], m[4]) + (m[1], m[2])))
