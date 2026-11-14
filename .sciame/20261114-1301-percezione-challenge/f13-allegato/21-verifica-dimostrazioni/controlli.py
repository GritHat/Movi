#!/usr/bin/env python3
# Verifica avversaria delle dimostrazioni dell'allegato tecnico: ricalcoli indipendenti.
# Python puro, nessun file del progetto importato. Si lancia con: timeout 120 python3 controlli.py
import itertools, math, random
from fractions import Fraction as Fr
from math import comb, sqrt, log, exp, tan, atan, sin, cos, radians, degrees, pi, erf

def Phi(x): return 0.5 * (1 + erf(x / sqrt(2)))
def Phinv(p):
    lo, hi = -10.0, 10.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if Phi(mid) < p: lo = mid
        else: hi = mid
    return (lo + hi) / 2
def wilson(k, n, z=1.959964):
    p = k / n; c = (p + z*z/(2*n)) / (1 + z*z/n); h = z*sqrt(p*(1-p)/n + z*z/(4*n*n)) / (1 + z*z/n)
    return c - h, c + h
def binpmf(n, k, p): return comb(n, k) * p**k * (1-p)**(n-k)
def bincdf(n, k, p): return sum(binpmf(n, i, p) for i in range(0, k+1))

print("== A. Ricorsione di Pi in una dimensione (esaustivo)")
def dil(S, r, n): return {j for i in S for j in range(i-r, i+r+1) if 0 <= j < n}
def esaustivo(n, T, vero=1, dich=1):
    diff = mono = fuori = 0
    sub = [set(c) for r in range(n+1) for c in itertools.combinations(range(n), r)]
    for seq in itertools.product(sub, repeat=T):
        Pi = set(range(n)); R = set(range(n)); viol = False
        for O in seq:
            nuovo = dil(Pi, dich, n) - O
            if not (nuovo >= (Pi - O)): mono += 1
            Pi = nuovo
            R = dil(R, vero, n) - O          # posizioni finali delle traiettorie coerenti (oggetto puntiforme)
            if not R <= Pi: viol = True
        if vero == dich and R != Pi: diff += 1
        if viol: fuori += 1
    return len(sub)**T, diff, mono, fuori
for n, T in ((4, 4), (5, 3)):
    tot, diff, mono, _ = esaustivo(n, T)
    print(f"  {n} celle, {T} fotogrammi: {tot} successioni; Pi != raggiungibile in {diff}; violazioni di monotonia {mono}")
for n, T in ((3, 2), (4, 4)):
    tot, _, _, fuori = esaustivo(n, T, vero=2, dich=1)
    print(f"  velocità vera doppia, {n} celle, {T} fotogrammi: oggetto possibile fuori da Pi in {fuori} successioni su {tot}")

print("== A2. Contenimento con errore di posa: O calcolato nel riferimento stimato (spostamento di s celle)")
def posa(n=7, T=3, s=1, eroso=False):
    # mondo: un oggetto puntiforme, velocità <= 1 cella/fotogramma; sensore ideale che vede libero tutto
    # tranne la cella (stimata) dell'oggetto; il riferimento stimato è spostato di s celle rispetto al vero.
    viol = tot = 0
    for traj in itertools.product(range(n), repeat=T):
        if any(abs(traj[i+1]-traj[i]) > 1 for i in range(T-1)): continue
        if any(not (0 <= x+s < n) for x in traj): continue
        Pi = set(range(n))
        for x in traj:
            Ohat = set(range(n)) - {x+s}                     # libero nel riferimento stimato
            if eroso: Ohat = {c for c in Ohat if all((c+d) in Ohat or not (0 <= c+d < n) for d in range(-s, s+1))}
            Pi = dil(Pi, 1 + s, n) - Ohat                    # ricorsione dell'allegato: raggio vmax*Delta + eps_p
            tot += 1
            if x not in Pi: viol += 1                        # x = posizione VERA dell'oggetto
    return viol, tot
v, t = posa(eroso=False); print(f"  ricorsione dell'allegato (dilatazione con eps_p, O stimato): posizione vera fuori da Pi in {v} istanti su {t}")
v, t = posa(eroso=True);  print(f"  con O eroso di eps_p (Lemma del margine di posa):              posizione vera fuori da Pi in {v} istanti su {t}")

print("== B. Livello di una regione ritagliata")
random.seed(20261114); viol = 0; ugu = 0
for _ in range(2000):
    n = random.randint(3, 40); w = [random.random() for _ in range(n)]; s = sum(w); G = [x/s for x in w]
    E = {i for i in range(n) if random.random() < 0.7}; S = {i for i in range(n) if random.random() < 0.5} or {0}
    p = sum(G[i] for i in E); gs = sum(G[i] for i in S); q = sum(G[i] for i in E & S) / gs
    if q < 1 - (1-p)/gs - 1e-12: viol += 1
    S2 = (set(range(n)) - E) | {min(E)} if E else set(range(n)); gs2 = sum(G[i] for i in S2)
    q2 = sum(G[i] for i in E & S2) / gs2
    if abs(q2 - (1 - (1-p)/gs2)) < 1e-12: ugu += 1
print(f"  violazioni del limite: {viol} su 2000; uguaglianza quando S contiene il complemento di E: {ugu} su 2000")
print(f"  p=0,95: G(S)=0,23 -> {1-0.05/0.23:.4f}; G(S)=0,08 -> {1-0.05/0.08:.4f}")

print("== C. Fascia di guardia, w = 0,40 m")
D = 1/15
for ta, tau, eps in ((0, .150, 0), (0, .155, 0), (2*D, .155, 0), (2*D, .155, .20)):
    T = ta + tau + D; print(f"  t_a={ta:.3f} tau={tau:.3f} eps={eps:.2f}: tempo {T:.4f} s, v coperta {(0.40-eps)/T:.3f} m/s")
T = 2*D + .155; print(f"  senza tenuta: {T:.4f} s; v coperta {0.40/T:.4f} m/s; 1,4*T = {1.4*T:.4f} m; 2,5*T = {2.5*T:.3f} m")
print(f"  fascia per classe 0,355*vmax: " + ", ".join(f"{v}->{0.355*v:.3f}" for v in (2.5, 2.0, 4.5, 8.0, 8.3, 13.9, 15.4, 16.7, 4.0, 4.8)))
tc = 0.267
for nome, tcx in (("t_conf=0,267", 0.267), ("t_conf=4/15", 4/15)):
    k = tcx + .155 + 1.0
    print(f"  d_serve [{nome}]: " + ", ".join(f"{v}->{k*v+0.95:.3f}" for v in (1.4, 2.5, 1.0, 2.0, 2.2, 4.5, 3.0, 8.0, 1.7, 8.3, 13.9, 9.0, 15.4, 11.0, 16.7)))
    print(f"    v coperta {(3-0.95)/k:.3f} m/s (Tr=1,5: {(3-0.95)/(k+.5):.3f}); dopo il contatto oltre {3/(tcx+.155):.2f} m/s")

print("== D. Massa: informazione di Fisher in aritmetica razionale")
u, M = Fr(120), Fr(75); ts = [Fr(k, 15) for k in range(1, 31)]
g = [1/M, -u/M**2]; I = [[sum(t**4/4 for t in ts)*g[i]*g[j] for j in range(2)] for i in range(2)]
print(f"  det 2x2 = {I[0][0]*I[1][1]-I[0][1]*I[1][0]}; I*(u,M) = {[I[i][0]*u+I[i][1]*M for i in range(2)]}")
def rango(A):
    A = [r[:] for r in A]; rk = 0
    for c in range(len(A[0])):
        piv = next((r for r in range(rk, len(A)) if A[r][c] != 0), None)
        if piv is None: continue
        A[rk], A[piv] = A[piv], A[rk]
        for r in range(len(A)):
            if r != rk and A[r][c] != 0:
                f = A[r][c]/A[rk][c]; A[r] = [a-f*b for a, b in zip(A[r], A[rk])]
        rk += 1
    return rk
J = [[Fr(1), t, t*t/(2*M), -u*t*t/(2*M*M)] for t in ts]
print(f"  rango dello jacobiano rispetto a (p0, v0, u, M): {rango(J)} su 4")

print("== E. Accelerazione")
for hz in (30, 15, 10): print(f"  differenza seconda, sigma_p=3 cm, {hz} Hz: {sqrt(6)*0.03*hz*hz:.2f} m/s^2")
def sigma_a_lsq(N, dt, s):
    t = [Fr(i)*Fr(dt).limit_denominator(1000) for i in range(N)]
    A = [[sum(x**(i+j) for x in t) for j in range(3)] for i in range(3)]
    # inversa 3x3 per cofattori: serve l'elemento (2,2)
    det = (A[0][0]*(A[1][1]*A[2][2]-A[1][2]*A[2][1]) - A[0][1]*(A[1][0]*A[2][2]-A[1][2]*A[2][0]) + A[0][2]*(A[1][0]*A[2][1]-A[1][1]*A[2][0]))
    c22 = (A[0][0]*A[1][1]-A[0][1]*A[1][0]) / det
    return 2*s*sqrt(float(c22))
for N in (15, 16): print(f"  minimi quadrati, accelerazione costante, {N} campioni a 30 Hz: sigma_a = {sigma_a_lsq(N, 1/30, 0.03):.3f} m/s^2")
print("  varianza della differenza seconda (Monte Carlo, 200000): ", end="")
random.seed(1); xs = [random.gauss(0, 1) - 2*random.gauss(0, 1) + random.gauss(0, 1) for _ in range(200000)]
print(f"{sum(x*x for x in xs)/len(xs):.3f} (atteso 6)")

print("== F. Filtro a velocità quasi costante: covarianza stazionaria e crescita senza misure")
def staz(q, R=0.05**2, dt=1/15):
    P = [[1.0, 0.0], [0.0, 1.0]]
    for _ in range(5000):
        a, b, d = P[0][0], P[0][1], P[1][1]
        a, b, d = a + 2*dt*b + dt*dt*d + q*dt**3/3, b + dt*d + q*dt*dt/2, d + q*dt   # previsione
        S = a + R; k0, k1 = a/S, b/S
        P = [[(1-k0)*a, (1-k0)*b], [(1-k0)*b, d - k1*b]]                               # correzione
    return P
for q in (0.2, 0.1, 0.05):
    P = staz(q); r = []
    for T in (0.5, 1, 2, 3): r.append(sqrt(P[0][0] + 2*T*P[0][1] + T*T*P[1][1] + q*T**3/3))
    print(f"  q={q}: sqrt(Ppp)={sqrt(P[0][0])*100:.2f} cm, sqrt(Pvv)={sqrt(P[1][1]):.3f} m/s; sigma_p = " + " / ".join(f"{x:.3f}" for x in r) + ("; r95 = " + " / ".join(f"{2.4477*x:.2f}" for x in r) if q == 0.2 else ""))
P = staz(0.2)
for soglia in (1.0, 2.0):
    T = 0.0
    while 2.4477*sqrt(P[0][0] + 2*T*P[0][1] + T*T*P[1][1] + 0.2*T**3/3) < soglia: T += 0.001
    print(f"  q=0,2: r95 supera {soglia} m dopo {T:.2f} s")
print(f"  raggi: {sqrt(-2*log(.5)):.4f} {sqrt(-2*log(.1)):.4f} {sqrt(-2*log(.05)):.4f}; 1-exp(-1/2) = {1-exp(-.5):.4f}; gamma99 = {-2*log(.01):.3f}")

print("== G. Intervalli")
for k, n in ((826, 879), (58, 90), (9, 2800), (347, 357), (174, 221), (23, 24), (21, 24), (283, 339), (226, 282), (830, 897), (132, 134), (44, 87)):
    a, b = wilson(k, n); print(f"  Wilson {k}/{n}: {k/n:.4f} [{a:.4f}; {b:.4f}]")
for n in (90, 96, 131, 300, 10, 400, 8314, 24835):
    print(f"  0 su {n}: esatto a una coda {100*(1-0.05**(1/n)):.4f} %, Wilson {100*3.8415/(n+3.8415):.4f} %, 3/N = {300/n:.4f} %")
print(f"  400 su 400: Wilson {400/403.8415:.4f}; esatto a una coda {0.05**(1/400):.4f}")
for m in (12, 45, 60): print(f"  z_{m} = {Phinv(1-0.05/(2*m)):.3f}")
print("  90 su 100: m=1 [%.3f; %.3f]; m=12 [%.3f; %.3f]" % (*wilson(90, 100), *wilson(90, 100, Phinv(1-0.05/24))))
# copertura effettiva dell'intervallo di Wilson (non è garantita >= nominale): minimo su una griglia di p, N = 100
def copertura(n, p, z=1.959964):
    return sum(binpmf(n, k, p) for k in range(n+1) if wilson(k, n, z)[0] <= p <= wilson(k, n, z)[1])
cmin = min((copertura(100, i/1000), i/1000) for i in range(5, 996))
print(f"  copertura effettiva minima dell'intervallo di Wilson al 95 %, N=100, p in [0,005; 0,995]: {cmin[0]:.4f} a p={cmin[1]}")

print("== H. Copertura realizzata Beta(k, n+1-k)")
def cdf_beta(k, n, x): return 1 - bincdf(n, k-1, x)      # P(U_(k) <= x) = P(Bin(n,x) >= k)
def quantile(k, n, pr):
    lo, hi = 0.0, 1.0
    for _ in range(80):
        mid = (lo+hi)/2
        if cdf_beta(k, n, mid) < pr: lo = mid
        else: hi = mid
    return lo
for n in (30, 100):
    k = math.ceil(0.9*(n+1) - 1e-12); print(f"  n_c={n}, k={k}: 5º percentile {quantile(k, n, 0.05):.4f}")
ok = [n for n in range(9, 400) if (lambda k: k <= n and 1 - cdf_beta(k, n, 0.85) >= 0.95)(math.ceil(0.9*(n+1) - 1e-12))]
primo = ok[0]; stabile = max(n for n in range(9, 400) if n not in ok) + 1
print(f"  primo n_c con P(C>0,85)>=0,95: {primo}; stabilmente da {stabile}; soglia infinita per n_c < {min(n for n in range(1, 40) if math.ceil(0.9*(n+1)-1e-12) <= n)}")

print("== I. Criterio d'accettazione")
def due_stadi(p_list_counts, lo, hi, tot2):
    # distribuzione esatta dei 'dentro' in uno stadio: convoluzione di binomiali
    d = {0: Fr(1)}
    for n, p in p_list_counts:
        nd = {}
        for a, pa in d.items():
            for k in range(n+1):
                nd[a+k] = nd.get(a+k, 0) + pa*comb(n, k)*p**k*(1-p)**(n-k)
        d = nd
    passa = sum(v for k, v in d.items() if k >= hi); resp1 = sum(v for k, v in d.items() if k <= lo)
    for k1, v1 in d.items():
        if lo < k1 < hi: passa += v1*sum(v2 for k2, v2 in d.items() if k1+k2 >= tot2)
    return float(passa), float(resp1)
print("  non stratificato 21/5/4, coperture 1/1/0:   P(supera) = %.4f" % due_stadi([(21, Fr(1)), (5, Fr(1)), (4, Fr(0))], 22, 28, 52)[0])
print("  non stratificato 21/5/4, coperture 1/1/0,5: P(supera) = %.4f" % due_stadi([(21, Fr(1)), (5, Fr(1)), (4, Fr(1, 2))], 22, 28, 52)[0])
for p in (Fr(9, 10), Fr(8, 10)): print(f"  tutti a {float(p)}: P(supera) = %.4f" % due_stadi([(30, p)], 22, 28, 52)[0])
for p in (Fr(1, 2), Fr(9, 10)):
    ps, r1 = due_stadi([(30, p)], 23, 28, 52)
    print(f"  stratificato (>=28 / <=23), copertura {float(p)}: respinto al primo stadio {r1:.4f}; respinto in tutto con il secondo stadio a 52 su 60: {1-ps:.4f}")

print("== J. Geometria")
h, th = 1.2, radians(15); bm, bp = radians(44), radians(14); Th, Tv = tan(radians(43.5)), tan(radians(29))
zmin = h/tan(bm); print(f"  z_min = {zmin:.4f}; T_h cos = {Th*cos(th):.4f}; T_h h sin = {Th*h*sin(th):.4f}; tan14 = {tan(bp):.4f}")
xs_ = Th*(zmin*cos(th)+h*sin(th)); print(f"  spigolo: x = {xs_:.3f}, phi = {degrees(atan(xs_/zmin)):.1f}, rho = {math.hypot(xs_, zmin):.3f}; rho_min(30°) = {zmin/cos(radians(30)):.3f}, (43,5°) = {zmin/cos(radians(43.5)):.3f}")
print(f"  ostacolo basso: {(h-.15)/tan(bm):.3f}, {(h-.10)/tan(bm):.3f}; testa 1,70: {0.5/tan(bp):.3f}; sospeso 1,80: {0.6/tan(bp):.3f}")
print(f"  z_min per Phi_v 55/61: {h/tan(radians(42.5)):.3f}/{h/tan(radians(45.5)):.3f}; per theta 14/16: {h/tan(radians(43)):.3f}/{h/tan(radians(45)):.3f}")
pv = 2*degrees(atan(240/424)); print(f"  f=424: Phi_v = {pv:.2f}, z_min = {h/tan(th+radians(pv/2)):.4f}; f da 87°: {424/tan(radians(43.5)):.1f}; da 58°: {240/tan(radians(29)):.1f}")
print(f"  settore d'anello: {0.5*radians(87)*(9-zmin**2):.3f} m2 = {100*0.5*radians(87)*(9-zmin**2)/(9*pi):.1f} %")
passo = 0.004; area = 0; x = -3 + passo/2
while x < 3:
    z = zmin + passo/2
    while z < 3:
        if x*x + z*z <= 9 and abs(x) <= Th*(z*cos(th) + h*sin(th)): area += passo*passo
        z += passo
    x += passo
print(f"  regione esatta nel disco (griglia di 4 mm): {area:.3f} m2 = {100*area/(9*pi):.1f} %")
print(f"  ombra: {1.7*1.2/0.9:.3f}, {1.5*1.2/0.7:.3f}, {1.5*1.2/0.2:.2f}; a_min(1,60; 1,15)={h+1.15*min(0.4/2.3, tan(bp)):.3f}; tetto(2,0)={h+2.0*tan(bp):.3f}; fascia visibile {h+0.3*2.3/1.7:.3f}, {h+0.3*2.3/1.9:.3f}")
print(f"  durata: 1 m: {(2.3/1.9-.45)/1.4:.2f}-{(2.3/1.7-.45)/1.0:.2f} s; 2 m: {(2*2.3/1.9-.45)/1.4:.2f}-{(2*2.3/1.7-.45)/1.0:.2f} s")
for d_ in (1.0,):
    for r in (2.0, 2.8, 3.0): print(f"  errore di quota 1° a {r} m: {100*(r*sin(radians(1))+h*(1-cos(radians(1)))):.2f} cm", end=";")
print(f"\n  suolo occupato con 2° da {(0.07-h*(1-cos(radians(2))))/sin(radians(2)):.3f} m; soglia 10 cm: {degrees(0.03/2.5):.2f}° a 2,5 m, {degrees(0.03/3):.2f}° a 3 m")
print(f"  sigma_z nominale 2/3/4 m: " + "/".join(f"{100*d*d*0.08/(424*0.05):.2f}" for d in (2, 3, 4)) + " cm; sigma_t: " + "/".join(f"{100*d*pi/180/sqrt(12):.2f}" for d in (2, 3, 4)))

print("== K. Margine della lettura del suolo (eq. del margine): quota massima di una superficie che legge ancora 'suolo'")
for k in (0.004, 0.010):
    for rho in (2.0, 3.0):
        z0 = rho*cos(th) + h*sin(th); m = 0.03 + 3*k*z0*z0
        print(f"  k={k}, rho={rho} m: z0={z0:.3f} m, m={m:.3f} m, superficie sul raggio fino a quota {100*h*m/z0:.1f} cm sopra il suolo resta entro il margine")

print("== L. Griglia bayesiana, conferma, mobile")
print(f"  ln(0,7/0,3)={log(.7/.3):.4f}; ln(0,1192/0,8808)={log(.1192/.8808):.4f}; colpi: {math.ceil(-log(.1192/.8808)/log(.7/.3))}")
for n in (3, 4, 5): print(f"  non confermato con {n} fotogrammi, P_D=0,9: {100*bincdf(n, 2, .9):.2f} %")
pj = {j: (j-1)*.81*.1**(j-2) for j in (2, 3, 4)}; print(f"  ritardo: {pj}; media {sum(j*p for j, p in pj.items())/15:.4f} s (non condizionata), {sum(j*p for j, p in pj.items())/sum(pj.values())/15:.4f} s (condizionata)")
pfa = 2*(1-Phi(5)); sd = sqrt(2/3)
print(f"  P_fa = {pfa:.3e}; 26*P_fa = {26*pfa:.3e}; sigma_delta = {sd:.4f} sigma; soglia {5*sd:.3f} sigma")
for nome, s in (("nominale 2 m", .0151), ("nominale 3 m", .0340), ("pessimista 3 m", .09), ("severa 3 m", .1125)):
    print(f"  {nome}: v0,5 = {5*sd*s/(13/15):.3f}, v0,9 = {(5+1.2816)*sd*s/(13/15):.3f} m/s")
print(f"  spostamento apparente: 10 % per delta = {(5-Phinv(.9))*sd:.3f} sigma; 1 % per {(5-Phinv(.99))*sd:.3f} sigma")
print(f"  piramide: {4/3*Th*Tv*27:.2f} m3; {100*4/3*Th*Tv*27/72:.1f} %; 72/V = {72/(4/3*Th*Tv*27):.2f}; blocchi {math.ceil(60/8)*math.ceil(40/8)*math.ceil(30/8)}, {math.ceil(120/8)*math.ceil(80/8)*math.ceil(60/8)}")

print("== M. Aggiunte dopo il primo lancio (non cieche): convenzione del conteggio del controesempio di velocità, z_60")
def solo_finale(n, T):
    sub = [set(c) for r in range(n+1) for c in itertools.combinations(range(n), r)]; fuori = 0
    for seq in itertools.product(sub, repeat=T):
        Pi = set(range(n)); R = set(range(n))
        for O in seq: Pi = dil(Pi, 1, n) - O; R = dil(R, 2, n) - O
        if not R <= Pi: fuori += 1
    return fuori, len(sub)**T
print("  velocità doppia, 4 celle, 4 fotogrammi, violazione contata solo all'ultimo fotogramma: %d su %d" % solo_finale(4, 4))
print("  (contata a un fotogramma qualsiasi: 30288, vedi sezione A)")
print(f"  z_60 = {Phinv(1-0.05/120):.5f}; z_12 = {Phinv(1-0.05/24):.5f}; z_45 = {Phinv(1-0.05/90):.5f}")
