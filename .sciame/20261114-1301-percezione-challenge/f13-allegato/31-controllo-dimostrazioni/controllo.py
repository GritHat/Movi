#!/usr/bin/env python3
# Controllo finale delle dimostrazioni: programmi indipendenti (Python puro, sola libreria standard: numpy non e' installato e la rete non e' ammessa).
import itertools, math, random
from fractions import Fraction

def titolo(s): print("\n== " + s)

# ---------- A. Ricorsione dell'insieme di possibile presenza, griglia 1D, esaustivo ----------
def dil(S, n, r=1):
    return {x for x in range(n) if any(abs(x - y) <= r for y in S)}

def pres_seq(obs_seq, n, r=1, erodi=0):
    P = set(range(n)); out = []
    for O in obs_seq:
        if erodi:  # sottrae solo i punti il cui intorno di raggio erodi sta in O (fuori griglia = non libero)
            O = {x for x in O if all((0 <= x + d < n) and (x + d) in O for d in range(-erodi, erodi + 1))}
        P = dil(P, n, r) - O
        out.append(set(P))
    return out

def raggiungibili(obs_seq, n, passo=1):
    # posizioni finali (e a ogni fotogramma) delle traiettorie coerenti: mai in una cella vista libera
    R = set(range(n)); out = []   # istante 0: nessun vincolo
    for O in obs_seq:
        R = {x for x in range(n) if any(abs(x - y) <= passo for y in R)} - O
        out.append(set(R))
    return out

def sottoinsiemi(n):
    return [set(i for i in range(n) if m >> i & 1) for m in range(1 << n)]

titolo("A1. Contenimento e minimalita' a posa esatta (esaustivo)")
for n, T in ((4, 4), (5, 3)):
    subs = sottoinsiemi(n); tot = diff = viol_mono = 0
    for seq in itertools.product(subs, repeat=T):
        tot += 1
        P = pres_seq(seq, n); R = raggiungibili(seq, n)
        if any(P[t] != R[t] for t in range(T)): diff += 1
        prev = set(range(n))
        for t in range(T):
            if not (P[t] >= prev - seq[t]): viol_mono += 1
            prev = P[t]
    print(f"celle={n} fotogrammi={T}: successioni={tot}, differenze Pres/raggiungibile={diff}, violazioni monotonia={viol_mono}")

titolo("A2. Controesempio di velocita' (passo vero 2, dichiarato 1)")
for n, T in ((3, 2), (4, 4)):
    subs = sottoinsiemi(n); tot = ult = qual = 0
    for seq in itertools.product(subs, repeat=T):
        tot += 1
        P = pres_seq(seq, n); R2 = raggiungibili(seq, n, passo=2)
        if not R2[-1] <= P[-1]: ult += 1
        if any(not R2[t] <= P[t] for t in range(T)): qual += 1
    print(f"celle={n} fotogrammi={T}: {tot} successioni; violazione all'ultimo fotogramma={ult}; a un fotogramma qualsiasi={qual}")

titolo("A3. Errore di posa di una cella: il sensore vede il mondo spostato (esaustivo su traiettorie)")
# mondo vero: un oggetto puntiforme su n celle, traiettoria a passo <=1; il sensore vede libero tutto tranne l'oggetto,
# ma la mappa e' scritta nel riferimento stimato, spostato di +1 cella.
n, T = 7, 3
ist = fuori = fuori_er = 0
for x0 in range(n):
    for passi in itertools.product((-1, 0, 1), repeat=T):
        xs = []; x = x0; ok = True
        for p in passi:
            x += p
            if not (0 <= x < n): ok = False; break
            xs.append(x)
        if not ok: continue
        obs = [{c for c in range(n) if c != min(n - 1, xt + 1)} if xt + 1 < n else set(range(n)) for xt in xs]
        P = pres_seq(obs, n); Pe = pres_seq(obs, n, erodi=1)
        for t in range(T):
            ist += 1
            fuori += xs[t] not in P[t]
            fuori_er += xs[t] not in Pe[t]
print(f"istanti={ist}; posizione vera fuori da Pres (ricorsione scritta)={fuori}; con il libero eroso di 1 cella={fuori_er}")

# ---------- B. Margine di lettura e lettura per punto: il passo «un punto occupato non e' letto come suolo» ----------
titolo("B. Lettura per punto con il margine m(z): striscia dell'impronta letta come suolo")
h, th = 1.2, math.radians(15)
def z0(rho): return h * math.sin(th) + rho * math.cos(th)      # profondita' del suolo lungo il raggio (asse ottico)
def m(z, k): return 0.03 + 3 * k * z * z
def striscia(rho, k): return rho * m(z0(rho), k) / z0(rho)        # in pianta, dietro la faccia vista
def quota(rho, k): return h * m(z0(rho), k) / z0(rho)
for k in (0.004, 0.010):
    print("k=%.3f: " % k + "; ".join(f"rho={r}: striscia={100*striscia(r,k):.1f} cm, quota={100*quota(r,k):.1f} cm" for r in (1.5, 2.0, 2.5, 3.0)))
# sezione verticale: oggetto [a, a+L] x [0, H]; il raggio verso il punto del suolo x incontra la faccia a frazione a/x
def letto_suolo(x, a, L, H, k):
    if x < a: return True
    s = a / x                              # frazione del raggio alla faccia vicina
    if h * (1 - s) > H: return True        # passa sopra l'oggetto (oggetto basso): qui non interessa oltre
    return (1 - s) * z0(x) <= m(z0(x), k)  # la profondita' misurata e' entro il margine dal suolo atteso
a, L, H = 2.30, 0.45, 1.7
for k in (0.004, 0.010):
    xs = [a + i * 0.001 for i in range(int(L * 1000) + 1)]
    occ_letti = [x for x in xs if letto_suolo(x, a, L, H, k)]
    print(f"k={k}: persona larga {L} m con faccia a {a} m: punti dell'impronta letti come suolo fino a {max(occ_letti)-a:.3f} m dalla faccia "
          f"({100*len(occ_letti)/len(xs):.0f}% dell'impronta in sezione): al fotogramma 1, Pres = X \\ Oss non li contiene")
# ricorsione nel tempo: oggetto che si avvicina; la striscia fuori da Pres resta quella della distanza piu' lontana
k = 0.004; dx = 0.005; N = int(3.2 / dx); vmaxD = 2.5 / 15
grid = [i * dx for i in range(N)]
P = set(range(N)); a_t = 2.60; peggio = 0.0
for t in range(8):
    O = {i for i, x in enumerate(grid) if x >= 1.25 and x <= 3.0 and letto_suolo(x, a_t, L, H, k)}
    r = int(round(vmaxD / dx))
    Pn = set()
    for i in P:
        Pn.update(range(max(0, i - r), min(N, i + r + 1)))
    P = Pn - O
    occ = [i for i, x in enumerate(grid) if a_t <= x <= a_t + L]
    fuori = [grid[i] for i in occ if i not in P]
    peggio = max(peggio, (max(fuori) - a_t) if fuori else 0.0)
    a_t -= 1.4 / 15
print(f"oggetto in avvicinamento a 1,4 m/s da 2,6 m, 8 fotogrammi, k={k}: profondita' massima dell'impronta fuori da Pres = {100*peggio:.1f} cm")
print("con m=0 (lettura esatta):", end=" ")
def letto_esatto(x, a): return x <= a
P = set(range(N)); a_t = 2.60; peggio = 0
for t in range(8):
    O = {i for i, x in enumerate(grid) if 1.25 <= x <= 3.0 and x < a_t - 1e-9}
    Pn = set()
    for i in P: Pn.update(range(max(0, i - r), min(N, i + r + 1)))
    P = Pn - O
    peggio += sum(1 for i, x in enumerate(grid) if a_t <= x <= a_t + L and i not in P)
    a_t -= 1.4 / 15
print(f"punti occupati fuori da Pres = {peggio}")

# ---------- C. Fascia di guardia ----------
titolo("C. Fascia di guardia: tabella e caso peggiore")
D = 1 / 15; w = 0.40
for ta, tau, eps, tenuta in ((0, .150, 0, True), (.133, .155, 0, False), (.133, .155, 0, True), (.133, .155, .20, True), (2 / 15, .155, 0, True), (4/15, .155, 0, True)):
    Ttot = ta + tau + (D if tenuta else 0)
    print(f"t_a={ta:.3f} tau={tau} eps={eps} tenuta={tenuta}: tempo={Ttot:.4f} s, vmax coperta={(w-eps)/Ttot:.3f} m/s; 1,4*T={1.4*Ttot:.3f} m; 2,5*T={2.5*Ttot:.3f} m")
random.seed(7); viol_c = viol_corpo = prove = 0
for _ in range(200000):
    v = random.uniform(0.2, 1.13); ta = .133; tau = .155; eps = random.uniform(0, 0.0)
    # 1D: ombra vera = (-inf, 0]; il centro esce in 0 al tempo 0 e si allontana a velocita' v
    rc = 0.225
    # (ii) per il centro: rilevato entro t_a da quando il CENTRO e' fuori; uscita non lo riporta fino a t_a+tau+D
    s = random.uniform(0, ta + tau + D); prove += 1
    viol_c += (v * s > w + 1e-12)
    # (ii) per il corpo: rilevato entro t_a da quando TUTTO il corpo e' fuori (centro a rc dal bordo)
    viol_corpo += (rc + v * s > w + 1e-12)
print(f"centro fuori da W: {viol_c} su {prove} se (ii) vale per il centro; {viol_corpo} su {prove} se (ii) vale per il corpo intero (raggio 0,225 m): serve aggiungere r_c")
print("velocita' coperta se (ii) vale per il corpo intero, r_c=0,225:", round((w - 0.225) / (0.133 + 0.155 + D), 3), "m/s")
p81 = 0.9**2
print("P(conferma entro +2 cicli | P_D=0,9) =", p81, "-> t_a=0,133 s come limite certo non e' il modello di rilevamento del cap. 4")


# ---------- strumenti in Python puro ----------
def binom_pmf(k, n, p): return math.comb(n, k) * p**k * (1 - p)**(n - k)
def binom_cdf(k, n, p): return sum(binom_pmf(i, n, p) for i in range(0, k + 1))
def binom_sf(k, n, p): return sum(binom_pmf(i, n, p) for i in range(k + 1, n + 1))   # P(X > k)
def Phi(x): return 0.5 * math.erfc(-x / math.sqrt(2))
def Phi_inv(p):
    lo, hi = -10.0, 10.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if Phi(mid) < p: lo = mid
        else: hi = mid
    return lo
def beta_cdf(x, a, b):  # a, b interi: Beta(a,b) = a-esima statistica d'ordine di a+b-1 uniformi
    return binom_sf(a - 1, a + b - 1, x)
def beta_ppf(pr, a, b):
    lo, hi = 0.0, 1.0
    for _ in range(100):
        mid = (lo + hi) / 2
        if beta_cdf(mid, a, b) < pr: lo = mid
        else: hi = mid
    return lo
def rango(Mx):
    Mx = [r[:] for r in Mx]; rg = 0
    for c in range(len(Mx[0])):
        piv = next((r for r in range(rg, len(Mx)) if Mx[r][c] != 0), None)
        if piv is None: continue
        Mx[rg], Mx[piv] = Mx[piv], Mx[rg]
        for r in range(len(Mx)):
            if r != rg and Mx[r][c] != 0:
                f = Mx[r][c] / Mx[rg][c]; Mx[r] = [x - f * y for x, y in zip(Mx[r], Mx[rg])]
        rg += 1
    return rg
def mm(A, B): return [[sum(a * b for a, b in zip(r, c)) for c in zip(*B)] for r in A]
def tr(A): return [list(r) for r in zip(*A)]

# ---------- D. Livello dopo il ritaglio ----------
titolo("D. Livello di una regione ritagliata: G(E∩S)/G(S) >= 1-(1-p)/G(S)")
random.seed(3); viol = ugu = n_ugu = casi = 0
for _ in range(20000):
    n = random.randint(3, 11); g = [random.expovariate(1) for _ in range(n)]; tot = sum(g); g = [x / tot for x in g]
    E = [random.random() < 0.7 for _ in range(n)]; S = [random.random() < 0.5 for _ in range(n)]
    GS = sum(x for x, s_ in zip(g, S) if s_)
    if GS <= 0: continue
    casi += 1
    GE = sum(x for x, e in zip(g, E) if e); p = GE * random.uniform(0.5, 1.0)
    GES = sum(x for x, e, s_ in zip(g, E, S) if e and s_)
    viol += GES / GS < 1 - (1 - p) / GS - 1e-12
    S2 = [s_ or not e for s_, e in zip(S, E)]; GS2 = sum(x for x, s_ in zip(g, S2) if s_)
    GES2 = sum(x for x, e, s_ in zip(g, E, S2) if e and s_); n_ugu += 1
    ugu += abs(GES2 / GS2 - (1 - (1 - GE) / GS2)) < 1e-12
print(f"violazioni={viol} su {casi}; uguaglianza nel caso S⊇X\\E, G(E)=p: {ugu} su {n_ugu}")
print("p=0,95: G(S)=0,23 ->", round(1 - .05 / .23, 4), "; G(S)=0,08 ->", round(1 - .05 / .08, 4))

# ---------- E. Massa: rango ----------
titolo("E. Non identificabilita' della massa: rango dell'informazione di Fisher (razionali esatti)")
u, M = Fraction(120), Fraction(75)
ts = [Fraction(kk, 15) for kk in range(30)]
J2 = [[t * t / (2 * M), -u * t * t / (2 * M * M)] for t in ts]
J4 = [[Fraction(1), t, t * t / (2 * M), -u * t * t / (2 * M * M)] for t in ts]
I2 = mm(tr(J2), J2); I4 = mm(tr(J4), J4)
print("parametri (u,M): rango =", rango(I2), "; det =", I2[0][0] * I2[1][1] - I2[0][1] * I2[1][0], "; I·(u,M)^T =", [r[0] * u + r[1] * M for r in I2])
print("parametri (p0,v0,u,M): rango =", rango(I4), "su 4; I·(0,0,u,M)^T =", [r[2] * u + r[3] * M for r in I4])

# ---------- F. Differenza seconda e minimi quadrati ----------
titolo("F. Varianza della differenza seconda; minimi quadrati su 0,5 s")
print("coefficiente 1+4+1 =", 6, "-> sigma_a = sqrt(6) sigma_p / D^2")
for f in (30, 15, 10): print(f"{f} Hz: sigma_a = {math.sqrt(6)*0.03*f*f:.2f} m/s^2")
random.seed(1); acc = []
for _ in range(300000):
    a_, b_, c_ = (random.gauss(0, 0.03) for _ in range(3)); acc.append((c_ - 2 * b_ + a_) * 225)
mu = sum(acc) / len(acc); print("Monte Carlo a 15 Hz (N=300000):", round(math.sqrt(sum((x - mu)**2 for x in acc) / len(acc)), 2))
def inv3(A):
    (a, b, c), (d, e, f), (g, h_, i) = A
    det = a * (e * i - f * h_) - b * (d * i - f * g) + c * (d * h_ - e * g)
    return [[(e * i - f * h_) / det, (c * h_ - b * i) / det, (b * f - c * e) / det],
            [(f * g - d * i) / det, (a * i - c * g) / det, (c * d - a * f) / det],
            [(d * h_ - e * g) / det, (b * g - a * h_) / det, (a * e - b * d) / det]]
for npt in (15, 16):
    tt = [Fraction(i, 30) for i in range(npt)]; A = [[Fraction(1), t, t * t / 2] for t in tt]
    C = inv3(mm(tr(A), A))
    print(f"minimi quadrati, {npt} campioni a 30 Hz ({float(tt[-1]):.3f} s): sigma_a = {0.03*math.sqrt(float(C[2][2])):.3f} m/s^2")
D_ = Fraction(1, 15); print("rango osservabilita' [p,v,a]:", rango([[Fraction(1), k * D_, (k * D_)**2 / 2] for k in range(3)]))

# ---------- G. Crescita della covarianza ----------
titolo("G. Q in forma chiusa, composizione, covarianza stazionaria e sigma_p(t_occ)")
def Fm(d): return [[1, d], [0, 1]]
def Qm(d, q=1): return [[q * d**3 / 3, q * d**2 / 2], [q * d**2 / 2, q * d]]
random.seed(5); peggior = Fraction(0)
for _ in range(200):
    d1 = Fraction(random.randint(1, 50), random.randint(1, 50)); d2 = Fraction(random.randint(1, 50), random.randint(1, 50))
    lhs = Qm(d1 + d2); rhs = mm(mm(Fm(d2), Qm(d1)), tr(Fm(d2))); rhs = [[rhs[i][j] + Qm(d2)[i][j] for j in range(2)] for i in range(2)]
    peggior = max(peggior, max(abs(lhs[i][j] - rhs[i][j]) for i in range(2) for j in range(2)))
print("composizione Q(d1+d2) = F(d2)Q(d1)F(d2)^T + Q(d2), 200 coppie razionali: scarto massimo =", peggior)
# integrale: l'integrando e' q[[s^2,s],[s,1]]: primitive s^3/3, s^2/2, s  (controllo per quadratura)
Nq = 20000; d = 0.3; qs = [sum(((i + .5) * d / Nq)**e for i in range(Nq)) * d / Nq for e in (2, 1, 0)]
print("quadratura con d=0,3:", [round(x, 6) for x in qs], "contro", [round(d**3 / 3, 6), round(d**2 / 2, 6), d])
def staz(qv, Rv=0.05**2, D=1/15):
    Ppp, Ppv, Pvv = 1.0, 0.0, 1.0
    for _ in range(20000):
        a = Ppp + 2 * D * Ppv + D * D * Pvv + qv * D**3 / 3; b = Ppv + D * Pvv + qv * D**2 / 2; c = Pvv + qv * D
        S = a + Rv; Ppp, Ppv, Pvv = a - a * a / S, b - a * b / S, c - b * b / S
    return Ppp, Ppv, Pvv
for qv in (0.2, 0.1, 0.05):
    Ppp, Ppv, Pvv = staz(qv)
    sig = [math.sqrt(Ppp + 2 * T * Ppv + T * T * Pvv + qv * T**3 / 3) for T in (0.5, 1, 2, 3)]
    print(f"q={qv}: sqrt(Ppp)={100*math.sqrt(Ppp):.2f} cm, sqrt(Pvv)={math.sqrt(Pvv):.3f} m/s; sigma_p = " + " / ".join(f"{x:.3f}" for x in sig)
          + ("; r95 = " + " / ".join(f"{2.4477*x:.2f}" for x in sig) if qv == 0.2 else ""))
Ppp, Ppv, Pvv = staz(0.2)
def r95(T): return 2.4477 * math.sqrt(Ppp + 2 * T * Ppv + T * T * Pvv + 0.2 * T**3 / 3)
for target in (1.0, 2.0):
    lo, hi = 0.0, 5.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if r95(mid) < target: lo = mid
        else: hi = mid
    print(f"r95 supera {target} m dopo {lo:.3f} s")
print("r_alfa/sigma:", [round(math.sqrt(-2 * math.log(1 - a)), 3) for a in (.5, .9, .95)], "; gamma 99%:", round(-2 * math.log(.01), 3))

# ---------- H. Binomiali e quantili ----------
titolo("H. Conti binomiali e quantili")
PD = 0.9
print("non confermato con n=3,4,5:", [round(binom_cdf(2, n, PD), 4) for n in (3, 4, 5)])
pj = {j: (j - 1) * PD**2 * (1 - PD)**(j - 2) for j in (2, 3, 4)}
# controllo per enumerazione: primo rilevamento al ciclo 0, terzo rilevamento al ciclo +j
enum = {2: 0.0, 3: 0.0, 4: 0.0}
for bits in itertools.product((0, 1), repeat=4):
    pr = 1.0
    for b in bits: pr *= PD if b else 1 - PD
    cnt = 1
    for j, b in enumerate(bits, start=1):
        cnt += b
        if cnt == 3:
            if j in enum: enum[j] += pr
            break
print("conferma a +j, formula:", {j: round(p, 5) for j, p in pj.items()}, "; enumerazione:", {j: round(p, 5) for j, p in enum.items()})
print("ritardo medio:", round(sum(j * p for j, p in pj.items()) / 15, 4), "s (non condizionato),", round(sum(j * p for j, p in pj.items()) / sum(pj.values()) / 15, 4), "s (condizionato)")
print("P_fa = 2(1-Phi(5)) =", 2 * (1 - Phi(5)) if False else math.erfc(5 / math.sqrt(2)), "; unione 2*13:", 26 * math.erfc(5 / math.sqrt(2)))
print("criterio: P(Bin(30,0.5)<=23) =", round(binom_cdf(23, 30, .5), 5), "; P(Bin(30,0.9)<=23) =", round(binom_cdf(23, 30, .9), 5))
lo95 = next(k for k in range(220) if binom_cdf(k, 219, .9) >= .025); hi95 = next(k for k in range(220) if binom_cdf(k, 219, .9) >= .975)
print("Bin(219,0.9): media", 219 * .9, "sd", round(math.sqrt(219 * .09), 2), "; centrale 95%:", lo95, hi95,
      "; P(>=214)=%.2e P(<=174)=%.2e P(>=207)=%.4f" % (binom_sf(213, 219, .9), binom_cdf(174, 219, .9), binom_sf(206, 219, .9)))
print("z_m:", {m_: round(Phi_inv(1 - .05 / (2 * m_)), 3) for m_ in (12, 30, 45, 60)})
print("0 su N: esatto e Wilson (%):", {N: (round(100 * (1 - .05**(1 / N)), 4), round(100 * 3.8416 / (N + 3.8416), 4)) for N in (90, 131, 300, 400, 24835)})
print("Beta: 5o percentile n=30,k=28:", round(beta_ppf(.05, 28, 3), 3), "; n=100,k=91:", round(beta_ppf(.05, 91, 10), 3))
def kk(n): return math.ceil(round(.9 * (n + 1), 9))
ok = [n for n in range(9, 300) if 1 - beta_cdf(.85, kk(n), n + 1 - kk(n)) >= .95]
print("primo n_c con P(copertura>0,85)>=0,95:", ok[0], "; stabile da:", max(n for n in range(9, 300) if n not in ok) + 1)
print("mobile: delta/sigma per 10% e 1%:", round((5 - Phi_inv(.9)) * math.sqrt(2 / 3), 3), round((5 - Phi_inv(.99)) * math.sqrt(2 / 3), 3))
print("±sigma in 2D:", round(1 - math.exp(-.5), 4), "; k al 95%:", round(math.sqrt(-2 * math.log(.05)), 3))
print("d_serve: velocita' coperta =", round((3 - .95) / (.267 + .155 + 1.0), 3), "; dopo il contatto oltre", round(3 / (.267 + .155), 2), "m/s")

# ---------- I. Etichetta ----------
titolo("I. Etichetta: inclusione di W sotto le premesse; i «rilasci» come celle tolte non sono un sottoinsieme")
random.seed(11); n = 40; viol_incl = viol_L = viol_tolte = prove = 0
for _ in range(20000):
    w0 = random.randint(1, 4); T = 12
    lo = random.randint(8, 20); hi = lo + random.randint(2, 6)
    We = W0 = None; we = w0
    for t in range(T):
        if random.random() < .3: lo += random.choice((-1, 1)); hi += random.choice((-1, 1)); hi = max(hi, lo)
        if random.random() < .3: we = max(we, w0 + random.randint(0, 4))
        def distanza(c): return 0 if lo <= c <= hi else min(abs(c - lo), abs(c - hi))
        lib = {c for c in range(n) if (c < lo or c > hi) and random.random() < .8}
        if t == 0:
            W0 = {c for c in range(n) if distanza(c) <= w0}; We = {c for c in range(n) if distanza(c) <= we}; continue
        L0 = {c for c in lib if distanza(c) > w0}; Le = {c for c in lib if distanza(c) > we}
        tolte0 = W0 & L0; toltee = We & Le
        W0 = W0 - L0; We = We - Le; prove += 1
        viol_incl += not (We >= W0); viol_L += not (Le <= L0); viol_tolte += not (toltee <= tolte0)
print(f"passi={prove}: W_etichette ⊉ W_senza: {viol_incl}; L_etichette ⊄ L_senza: {viol_L}; celle tolte con etichette ⊄ celle tolte senza: {viol_tolte}")

# ---------- J. Geometria ----------
titolo("J. Geometria")
bm = math.radians(44); Th = math.tan(math.radians(43.5))
zmin = h / math.tan(bm); print("z_min =", round(zmin, 4), "; |x| <=", round(Th * math.cos(th), 4), "z +", round(Th * h * math.sin(th), 4))
passo = 0.004; area = 0
for iz in range(int(3 / passo)):
    z = (iz + .5) * passo
    if z < zmin: continue
    xl = min(Th * (z * math.cos(th) + h * math.sin(th)), math.sqrt(9 - z * z))
    area += 2 * xl * passo
print("area esatta =", round(area, 3), "m2; settore =", round(.5 * math.radians(87) * (9 - zmin**2), 3), "; disco =", round(math.pi * 9, 2))
print("piramide:", round(4 / 3 * Th * math.tan(math.radians(29)) * 27, 2), "m3; quota:", round(4 / 3 * Th * math.tan(math.radians(29)) * 27 / 72, 4))
