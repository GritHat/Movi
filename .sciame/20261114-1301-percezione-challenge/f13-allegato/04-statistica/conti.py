# conti.py -- sciame-statistico, f13/04-statistica.
# Rifa' i conti statistici del fascicolo: intervalli, zero eventi, numerosita', taratura conforme, tabellone.
# Uso: python -I -B conti.py > conti.txt   (serve scipy)
import math
from scipy import stats

Z = stats.norm.ppf(0.975)


def wilson(k, n, z=Z):
    p = k / n
    c = (p + z * z / (2 * n)) / (1 + z * z / n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return c - h, c + h


def cp(k, n, a=0.05):
    lo = 0.0 if k == 0 else stats.beta.ppf(a / 2, k, n - k + 1)
    hi = 1.0 if k == n else stats.beta.ppf(1 - a / 2, k + 1, n - k)
    return lo, hi


print('1. INTERVALLI per k su n: Wilson al 95 % e Clopper-Pearson (esatto) al 95 %')
for k, n in ((9, 10), (10, 10), (27, 30), (28, 30), (30, 30), (45, 50), (46, 50), (90, 100), (108, 120), (826, 879), (461, 513), (13, 4800), (41, 45), (80, 90), (79, 90), (5, 90), (83, 90), (36, 46), (2939, 3038), (214, 219), (219, 219), (115, 115), (174, 221), (283, 339), (226, 282)):
    w = wilson(k, n); c = cp(k, n)
    print('   %5d su %-5d = %.4f | Wilson [%.4f-%.4f] | esatto [%.4f-%.4f]' % (k, n, k / n, w[0], w[1], c[0], c[1]))

print('\n2. ZERO EVENTI su N: limite superiore della quota vera')
print('   N        | esatto una coda 95 %: 1-0,05^(1/N) | regola del tre 3/N | Wilson due code z^2/(N+z^2) | esatto due code 1-0,025^(1/N)')
for n in (45, 90, 131, 400, 2716, 2800, 2798, 5597, 13638, 14400, 24835):
    print('   %-8d | %.6f | %.6f | %.6f | %.6f' % (n, 1 - 0.05 ** (1 / n), 3 / n, Z * Z / (n + Z * Z), 1 - 0.025 ** (1 / n)))
print('   -ln(0,05) = %.4f (da cui «3»); z^2 = %.4f; -ln(0,025) = %.4f' % (-math.log(0.05), Z * Z, -math.log(0.025)))
print('   tutti i successi, 400 su 400: limite inferiore 1-3/400 = %.4f; esatto una coda %.4f; Wilson %.4f' % (1 - 3 / 400, 0.05 ** (1 / 400), wilson(400, 400)[0]))

print('\n3. CORREZIONE PER m CELLE GIUDICATE INSIEME (Bonferroni: z_m = quantile 1 - 0,05/(2m))')
for m in (1, 12, 15, 45, 60):
    zm = stats.norm.ppf(1 - 0.05 / (2 * m))
    print('   m = %-3d z = %.4f | 826 su 879: limite inferiore %.4f | 90 su 100: [%.3f-%.3f] | 0 su N: limite superiore z^2/(N+z^2) con N = 2716: %.5f' % (m, zm, wilson(826, 879, zm)[0], *wilson(90, 100, zm), zm * zm / (2716 + zm * zm)))
print('   0 eventi in ciascuna di m = 3 geometrie, livello congiunto 95 %% (una coda, Bonferroni): limite per geometria 1-(0,05/3)^(1/N): N = 2716 -> %.5f; regola corrispondente -ln(0,05/3)/N = %.2f/N' % (1 - (0.05 / 3) ** (1 / 2716), -math.log(0.05 / 3)))


def piano(p0, p1, alfa, potenza, nmax=1200):
    """Prova a una coda di H0: p = p0 contro H1: p = p1. Se p1 > p0 si rifiuta H0 per k >= c; se p1 < p0 per k <= c.
    Ritorna (n minimo che soddisfa, soglia c, livello vero, potenza vera, n oltre il quale vale per ogni n fino a nmax)."""
    primo = None; ultimo_fallito = 0
    for n in range(2, nmax + 1):
        if p1 > p0:
            c = int(stats.binom.isf(alfa, n, p0)) + 1  # minimo c con P(K >= c | p0) <= alfa
            while stats.binom.sf(c - 1, n, p0) > alfa: c += 1
            while c > 0 and stats.binom.sf(c - 2, n, p0) <= alfa: c -= 1
            liv = stats.binom.sf(c - 1, n, p0); pot = stats.binom.sf(c - 1, n, p1)
        else:
            c = int(stats.binom.ppf(alfa, n, p0))
            while c >= 0 and stats.binom.cdf(c, n, p0) > alfa: c -= 1
            while stats.binom.cdf(c + 1, n, p0) <= alfa: c += 1
            liv = stats.binom.cdf(c, n, p0) if c >= 0 else 0.0; pot = stats.binom.cdf(c, n, p1) if c >= 0 else 0.0
        if pot >= potenza:
            if primo is None: primo = (n, c, liv, pot)
        else:
            ultimo_fallito = n
    return primo, ultimo_fallito + 1


print('\n4. NUMEROSITA\' (binomiale esatta, prova a una coda). «n minimo» = primo n che soddisfa; «n stabile» = da li\' in poi vale per ogni n (la potenza esatta e\' a dente di sega)')
for nome, p0, p1, a, pw in (('0,80 (H0) contro 0,90', 0.80, 0.90, 0.05, 0.80), ('0,90 (H0) contro 0,80', 0.90, 0.80, 0.05, 0.80),
                            ('0,85 (H0) contro 0,90', 0.85, 0.90, 0.05, 0.80), ('0,90 (H0) contro 0,85', 0.90, 0.85, 0.05, 0.80),
                            ('0,90 (H0) contro 0,95', 0.90, 0.95, 0.05, 0.80), ('0,95 (H0) contro 0,90', 0.95, 0.90, 0.05, 0.80),
                            ('0,80 (H0) contro 0,90, due errori <= 0,10', 0.80, 0.90, 0.10, 0.90), ('0,70 (H0) contro 0,90, due errori <= 0,10', 0.70, 0.90, 0.10, 0.90),
                            ('0,85 (H0) contro 0,90, due errori <= 0,10', 0.85, 0.90, 0.10, 0.90)):
    (n, c, liv, pot), stab = piano(p0, p1, a, pw)
    print('   %-44s alfa %.2f potenza %.2f: n minimo %4d (soglia %s %d; livello vero %.4f; potenza vera %.4f); n stabile %d' % (nome, a, pw, n, '>=' if p1 > p0 else '<=', c, liv, pot, stab))
# formula normale di confronto
for p0, p1 in ((0.80, 0.90), (0.85, 0.90), (0.95, 0.90)):
    za, zb = stats.norm.ppf(0.95), stats.norm.ppf(0.80)
    n = ((za * math.sqrt(p0 * (1 - p0)) + zb * math.sqrt(p1 * (1 - p1))) / (p1 - p0)) ** 2
    print('   approssimazione normale, %.2f contro %.2f: n = %.1f' % (p0, p1, n))
n = 30
c = 0
while stats.binom.sf(c - 1, n, 0.80) > 0.05: c += 1
print('   con n = 30, H0: 0,80 contro 0,90: soglia >= %d su 30, livello vero %.4f, potenza %.3f (nei file 0,39)' % (c, stats.binom.sf(c - 1, n, 0.80), stats.binom.sf(c - 1, n, 0.90)))

print('\n5. LETTURA DI UN TABELLONE «dentro k su n»')
for p in (0.95, 0.90, 0.80, 0.70):
    print('   copertura vera %.2f: P(almeno 9 su 10) = %.3f; P(30 su 30) = %.4f; P(almeno 27 su 30) = %.3f' % (p, stats.binom.sf(8, 10, p), p ** 30, stats.binom.sf(26, 30, p)))
print('   minimo k su 30 e su 50 con limite inferiore di Wilson >= 0,80: ' + ', '.join('%d su %d (limite %.3f)' % (k, n, wilson(k, n)[0]) for n in (30, 50) for k in [min(k for k in range(n + 1) if wilson(k, n)[0] >= 0.80)]))
print('   minimo k con limite inferiore ESATTO >= 0,80: ' + ', '.join('%d su %d (limite %.3f)' % (k, n, cp(k, n)[0]) for n in (30, 50) for k in [min(k for k in range(n + 1) if cp(k, n)[0] >= 0.80)]))
print('   semiampiezza di Wilson <= 0,10: n minimo con quota osservata 0,90: %d; 0,85: %d; 0,50 (caso peggiore): %d' % tuple(
    min(n for n in range(5, 400) if (wilson(round(q * n), n)[1] - wilson(round(q * n), n)[0]) / 2 <= 0.10 and all((wilson(round(q * m), m)[1] - wilson(round(q * m), m)[0]) / 2 <= 0.10 for m in range(n, 400))) for q in (0.90, 0.85, 0.50)))
for p in (0.90, 0.85):
    pr = sum(stats.binom.pmf(k, 50, p) for k in range(51) if (wilson(k, 50)[1] - wilson(k, 50)[0]) / 2 <= 0.10)
    print('   n = 50, copertura vera %.2f: probabilita\' che la semiampiezza di Wilson sia <= 0,10: %.3f' % (p, pr))
print('   passaggi correlati: m = 10 per persona, correlazione 0,2: effetto del disegno 1+(m-1)rho = %.1f; 40 passaggi ne valgono %.1f' % (1 + 9 * 0.2, 40 / (1 + 9 * 0.2)))
print('   THOR: 219 tratti di 9 persone (in media %.1f a testa): con rho = 0,2 ne valgono %.0f; con rho = 0,05 %.0f' % (219 / 9, 219 / (1 + (219 / 9 - 1) * 0.2), 219 / (1 + (219 / 9 - 1) * 0.05)))

print('\n6. TARATURA PER QUANTILI (previsione conforme a insieme separato), livello 0,90')
print('   copertura realizzata ~ Beta(k, n+1-k), k = ceil(0,9 (n+1)); media k/(n+1)')
for n in (8, 9, 20, 30, 60, 100, 200, 500):
    k = math.ceil(0.9 * (n + 1))
    if k > n:
        print('   n = %-4d k = %d > n: la soglia e\' infinita (la regione e\' tutto lo spazio)' % (n, k)); continue
    b = stats.beta(k, n + 1 - k)
    print('   n = %-4d k = %-4d media %.4f; 5o percentile %.4f; 95o percentile %.4f; limiti teorici [0,9; 0,9 + 1/(n+1)] = [0.9000; %.4f]' % (n, k, b.mean(), b.ppf(0.05), b.ppf(0.95), 0.9 + 1 / (n + 1)))
for soglia in (0.80, 0.85, 0.87):
    n = 9
    while True:
        k = math.ceil(0.9 * (n + 1))
        if stats.beta.ppf(0.05, k, n + 1 - k) >= soglia and all(stats.beta.ppf(0.05, math.ceil(0.9 * (m + 1)), m + 1 - math.ceil(0.9 * (m + 1))) >= soglia for m in range(n, n + 60)):
            break
        n += 1
    n1 = next(m for m in range(9, 2000) if stats.beta.ppf(0.05, math.ceil(0.9 * (m + 1)), m + 1 - math.ceil(0.9 * (m + 1))) >= soglia)
    print('   copertura realizzata >= %.2f con probabilita\' 0,95: primo n %d; n stabile %d' % (soglia, n1, n))

print('\n7. ALTRI CONTROLLI')
o, p = stats.fisher_exact([[86, 92 - 86], [101, 105 - 101]])
print('   Fisher esatto, 86/92 contro 101/105 (stessa cella, due lanci, stesso denominatore): p = %.3f (nei file 0,52)' % p)
o, p = stats.fisher_exact([[86, 98 - 86], [101, 119 - 101]])
print('   Fisher esatto, 86/98 contro 101/119: p = %.3f' % p)
print('   regola per n = 119 e soglia 0,85: Wilson di 101/119 = [%.3f-%.3f] -> non risolta' % wilson(101, 119))
print('   0,288 s x 2,5 m/s = %.2f m' % (0.288 * 2.5))
