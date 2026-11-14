"""Conti del piano delle misure (H-012, f3, sciame-metrologo). Python puro, nessun seme: tutto esatto o in forma chiusa.
Uso: PYTHONDONTWRITEBYTECODE=1 timeout 60 python3 conti_metrologo.py > conti_metrologo.txt
Limiti binomiali: Clopper-Pearson unilaterali al 95 %. Non esegue nessuna delle prove A, B, C."""
from math import lgamma, log, exp, sqrt, erf, ceil


def pmf(n, i, p):
    if p <= 0: return 1.0 if i == 0 else 0.0
    if p >= 1: return 1.0 if i == n else 0.0
    return exp(lgamma(n + 1) - lgamma(i + 1) - lgamma(n - i + 1) + i * log(p) + (n - i) * log(1 - p))


def coda(n, k, p): return sum(pmf(n, i, p) for i in range(max(k, 0), n + 1))   # P(X >= k)
def cdf(n, k, p): return sum(pmf(n, i, p) for i in range(0, k + 1))            # P(X <= k)


def bis(f):
    lo, hi = 0.0, 1.0
    for _ in range(40):
        m = (lo + hi) / 2
        if f(m): hi = m
        else: lo = m
    return (lo + hi) / 2


def inf95(x, n): return 0.0 if x == 0 else bis(lambda m: coda(n, x, m) > 0.05)
def sup95(x, n): return 1.0 if x == n else bis(lambda m: cdf(n, x, m) < 0.05)
def Phi(z): return 0.5 * (1 + erf(z / sqrt(2)))


print('== zero fallimenti ==')
print('N minimo per dire >= 99 % al 95 %:', ceil(log(0.05) / log(0.99)), '| al 97,5 %:', ceil(log(0.025) / log(0.99)),
      '| per 24 celle insieme (Bonferroni):', ceil(log(0.05 / 24) / log(0.99)), '| per >= 95 %:', ceil(log(0.05) / log(0.95)))
for n in (10, 20, 30, 59, 100, 300, 1000, 7200):
    print('0 fallimenti su %d -> quota di fallimento <= %.5f' % (n, 1 - 0.05 ** (1 / n)))
print('1 fallimento su 300 -> <= %.4f' % sup95(1, 300))

print('== soglie "almeno": regge se il limite inferiore >= soglia; smentita se il limite superiore < soglia ==')
for thr in (0.85, 0.90, 0.95):
    for n in (30, 100, 300, 1000, 2000):
        xr = next((x for x in range(int(thr * n), n + 1) if inf95(x, n) >= thr), None)
        xs = next((x for x in range(int(thr * n), -1, -1) if sup95(x, n) < thr), None)
        print('soglia >= %.2f, n = %4d: regge da %s successi; smentita fino a %s' % (thr, n, xr, xs))
print('== soglia "al piu\' 10 %" ==')
for n in (60, 120, 300):
    xr = max(x for x in range(n // 2) if sup95(x, n) <= 0.10)
    xs = min(x for x in range(n // 2) if inf95(x, n) > 0.10)
    print('n = %3d: regge fino a %d falsi; smentita da %d' % (n, xr, xs))

print('== potenza dei criteri del giorno dell\'hackathon: P(passa | quota vera p) ==')
ps = (0.95, 0.93, 0.90, 0.895, 0.85, 0.80, 0.75, 0.71)
print('26 su 30:', [(p, round(coda(30, 26, p), 3)) for p in ps])


def due_stadi(p, a=28, b=22, tot=52):
    P = 0.0
    for x1 in range(31):
        if x1 >= a: P += pmf(30, x1, p)
        elif x1 > b: P += pmf(30, x1, p) * coda(30, tot - x1, p)
    return P


print('due stadi (>= 28 passa; <= 22 bocciato; 23-27: altri 30, passa con >= 52 su 60):',
      [(p, round(due_stadi(p), 3), 'n medio %.0f' % (30 + 30 * sum(pmf(30, x, p) for x in range(23, 28)))) for p in ps])
print('9 su 10:', [(p, round(coda(10, 9, p), 3)) for p in (0.95, 0.90, 0.80, 0.75, 0.50)])
print('27 su 30:', [(p, round(coda(30, 27, p), 3)) for p in (0.95, 0.90, 0.80, 0.75)])
print('0 su 20 (passa con quota vera di guasto f):', [(f, round((1 - f) ** 20, 3)) for f in (0.01, 0.05, 0.10, 0.14, 0.25, 0.45)])
print('0 su 10:', [(f, round((1 - f) ** 10, 3)) for f in (0.05, 0.10, 0.26)])
print('p95: probabilita\' che il massimo di n campioni superi il p95 vero:', [(n, round(1 - 0.95 ** n, 3)) for n in (30, 59, 60, 100)])

print('== regola "spostamento su 1 s oltre 5 sigma(z) radice di 2", pedone a 0,5 m/s in avvicinamento ==')
print('P(visto) = Phi((0,5 - 5*sigma(z_fine)*rad2) / rad(sigma(z_inizio)^2 + sigma(z_fine)^2)); sigma(z) = limite dichiarato a 4 m scalato con z^2 (TORNEO parte 1)')
for cam, s4 in (('D455', 0.08), ('Gemini 335', 0.12), ('D435i', 0.16)):
    def s(z): return s4 * (z / 4) ** 2
    for d in (2.0, 3.0, 4.0):
        r = []
        for nome, z0, z1 in (('parte da d', d, d - 0.5), ('arriva a d', d + 0.5, d)):
            thr = 5 * s(z1) * sqrt(2)
            r.append('%s: sigma %.1f cm, soglia %.2f m, P = %.3f' % (nome, 100 * s(z1), thr, Phi((0.5 - thr) / sqrt(s(z0) ** 2 + s(z1) ** 2))))
        print('%-10s d = %.0f m | %s' % (cam, d, ' | '.join(r)))
print('sigma massima (uguale ai due estremi) perche\' P >= 0,90: %.4f m' % (0.5 / (5 * sqrt(2) + 1.2816 * sqrt(2))))
print('falsi per confronto e per asse se il rumore vero e\' k volte quello del modello:', [(k, '%.1e' % (2 * (1 - Phi(5 / k)))) for k in (1, 1.5, 2, 2.5, 3)])
print('incertezza relativa di una sigma stimata su n fotogrammi indipendenti:', [(n, round(1 / sqrt(2 * (n - 1)), 3)) for n in (30, 100, 300)])
