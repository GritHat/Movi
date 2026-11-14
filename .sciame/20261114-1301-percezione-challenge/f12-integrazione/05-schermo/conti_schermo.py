# conti_schermo.py — sciame-interfacce, f12/05-schermo. Python puro, sola lettura dei .tsv in prova_geometria/ris.
# Uso (da 05-schermo):  timeout 60 /usr/bin/python3 -I -B conti_schermo.py > risultati_schermo.txt
import math, os, re

QUI = os.path.dirname(os.path.abspath(__file__))


def wilson(k, n, z=1.959964):
    if n == 0:
        return (float('nan'), float('nan'))
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (c - h, c + h)


def binom_cdf(k, n, p):
    return sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(0, k + 1))


def clopper(k, n, a=0.05):
    def cerca(f, lo, hi):
        for _ in range(80):
            m = (lo + hi) / 2
            if f(m):
                lo = m
            else:
                hi = m
        return (lo + hi) / 2
    inf = 0.0 if k == 0 else cerca(lambda p: 1 - binom_cdf(k - 1, n, p) < a / 2, 0.0, 1.0)
    sup = 1.0 if k == n else cerca(lambda p: binom_cdf(k, n, p) > a / 2, 0.0, 1.0)
    return (inf, sup)


print('== P-int-2: intervalli del tabellone ==')
for k, n in ((27, 30), (46, 50), (45, 50), (30, 30), (28, 30), (23, 30), (54, 60), (9, 10), (10, 10), (5, 5)):
    lo, hi = wilson(k, n)
    cl, ch = clopper(k, n)
    print('%2d su %2d  Wilson 95 %% [%.3f; %.3f]   esatto [%.3f; %.3f]' % (k, n, lo, hi, cl, ch))

print()
print('== P-int-3: tempi della demo dal conto in pianta ==')
CORPO, CAMPO, PORTATA, YA = 0.45, math.radians(87.0 / 2), 3.0, 2.3
for yp in (1.7, 1.8, 1.9):
    for w in (1.0, 2.0):
        mezza = (w / 2) * YA / yp                      # mezza larghezza dell'ombra sulla linea dell'attore
        x_campo = YA * math.tan(CAMPO)                 # bordo del campo sulla linea dell'attore
        x_port = math.sqrt(PORTATA ** 2 - YA ** 2)     # bordo della portata sulla linea dell'attore
        nasc = 2 * mezza - CORPO                       # tratto in cui il corpo e' nascosto per intero
        vis_campo = x_campo - mezza - CORPO            # tratto, per lato, in cui il corpo e' in vista per intero (solo campo)
        vis_port = min(x_campo, x_port) - mezza - CORPO
        riga = 'pannello %.0f m a %.1f m: ombra %.2f m; nascosto per intero' % (w, yp, 2 * mezza)
        riga += ''.join(' %.2f s a %.1f m/s;' % (nasc / v, v) for v in (0.5, 0.8, 1.0, 1.4))
        riga += ' in vista per intero per lato a 1,0 m/s: %.2f s (solo campo), %.2f s (campo e portata 3 m)' % (vis_campo / 1.0, vis_port / 1.0)
        print(riga)
print('bordo del campo sulla linea a 2,3 m: %.2f m; bordo della portata di 3 m: %.2f m' % (YA * math.tan(CAMPO), math.sqrt(PORTATA ** 2 - YA ** 2)))

print()
print('== conti a mano messi qui: soggetto puntiforme del banco, C6 a 0,22 m dal bordo dell\'ombra, linea a 2,3 m ==')
for nome, yp, w, v in (('A (pannello 1 m a 1,9 m, 0,5 m/s)', 1.9, 1.0, 0.5), ('B (pannello 2 m a 1,9 m, 0,9 m/s)', 1.9, 2.0, 0.9)):
    mezza = (w / 2) * YA / yp
    print('%s: senza misura per %.1f s; tratto misurabile per lato fino alla portata: %.2f m' % (nome, (2 * mezza + 0.44) / v, math.sqrt(PORTATA ** 2 - YA ** 2) - mezza - 0.22))
print()
print('== P-int-4, P-int-5: geometria e passo (codice dello statistico di f8, semi 120000..120399, sd-1, Pd 0,9, maschera esatta, soggetto puntiforme) ==')
SUL_PERCORSO = ('prosegue', 'rallenta', 'sosta', 'torna', 'sostalunga')
BRACCI = (('E_larga_08-10.tsv', 'E: pannello 2 m a 1,9 m, attore 2,3 m, portata 3 m; passo 0,8-1,0 m/s'),
          ('E_lento_045-055.tsv', 'E, passo 0,45-0,55 m/s (braccio di confronto, senza previsione)'),
          ('D_lento_045-055.tsv', 'D: pannello 1 m a 1,9 m, attore 2,3 m; passo 0,45-0,55 m/s'),
          ('D_normale_10-14.tsv', 'D, passo 1,0-1,4 m/s (braccio di confronto, senza previsione)'))


def campi(riga):
    return dict(m.groups() for m in re.finditer(r'(\w+)=([^\t\n]+)', riga))


for nome, titolo in BRACCI:
    G, H, P = {}, {}, {}
    testa = ''
    with open(os.path.join(QUI, 'prova_geometria', 'ris', nome), encoding='utf-8') as f:
        for riga in f:
            c = riga.rstrip('\n').split('\t')
            if riga.startswith('# griglia'):
                testa = riga.strip()
            if c[0] == 'G':
                G[c[2]] = campi(riga)
            elif c[0] == 'H' and c[3] == 'sd-1':
                H[(c[2], c[4])] = campi(riga)
            elif c[0] == 'P' and c[3] == 'sd-1':
                P[c[2]] = campi(riga)
    print('--- %s  [%s]' % (titolo, nome))
    print('   ', testa)
    g = G['prosegue']
    v, s = int(g['validi']), int(g['scartati'])
    print('    prosegue: validi %d, scartati (meno di 4 misure) %d su %d = %.1f %%' % (v, s, v + s, 100.0 * s / (v + s)))
    tv = sum(int(G[b]['validi']) for b in SUL_PERCORSO)
    ts = sum(int(G[b]['scartati']) for b in SUL_PERCORSO)
    print('    sul percorso: scartati %d su %d = %.1f %%' % (ts, tv + ts, 100.0 * ts / (tv + ts)))
    p = P['prosegue']
    print('    prosegue: passaggi con un vuoto %s su %s; cicli «ampio» (area > 80 %% dell\'ombra) %s su %s = %.1f %%; punto che arretra in %s passaggi; salto mediano alla ricomparsa %s m (ricomparsi %s)'
          % (p['pass_vuoto'], p['npass'], p['ampio80'], p['cicli'], 100.0 * int(p['ampio80']) / int(p['cicli']), p['pass_indietro'], p['salto_med'], p['nre']))
    vuoti = sum(int(P[b]['pass_vuoto']) for b in SUL_PERCORSO)
    fuori100 = sum(int(P[b]['R90_fuori_R100_cicli']) for b in SUL_PERCORSO)
    libero = sum(int(P[b]['R90_su_libero_cicli']) for b in SUL_PERCORSO)
    print('    sul percorso: passaggi con un vuoto %d; cicli della zona fuori dall\'avviso %d; cicli della zona su visto libero oltre la fascia %d' % (vuoti, fuori100, libero))
    for tau in ('1.0', '2.0', '3.0'):
        h = H[('prosegue', tau)]
        n = int(h['n']) - int(h['fuori_griglia'])
        lo, hi = wilson(int(h['in90']), n)
        k = sum(int(H[(b, tau)]['in90']) for b in SUL_PERCORSO)
        m = sum(int(H[(b, tau)]['n']) - int(H[(b, tau)]['fuori_griglia']) for b in SUL_PERCORSO)
        fg = sum(int(H[(b, tau)]['fuori_griglia']) for b in SUL_PERCORSO)
        k100 = sum(int(H[(b, tau)]['in100']) for b in SUL_PERCORSO)
        ntot = sum(int(H[(b, tau)]['n']) for b in SUL_PERCORSO)
        l2, h2 = wilson(k, m)
        print('    a %s s: zona/ombra (prosegue) %.2f, errore mediano del punto %s m; dentro la zona: prosegue %d su %d [%.3f; %.3f]; sul percorso %d su %d = %.3f [%.3f; %.3f]; usciti dall\'area osservata %d; dentro l\'avviso %d su %d'
              % (tau[0], float(h['area90']) / float(h['ombra']), h['err_med'], int(h['in90']), n, lo, hi, k, m, k / m if m else float('nan'), l2, h2, fg, k100, ntot))
