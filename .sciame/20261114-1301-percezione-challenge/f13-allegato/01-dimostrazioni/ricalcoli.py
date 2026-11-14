#!/usr/bin/env python3
"""Ricalcoli del fascicolo «enunciati e dimostrazioni». Python puro, deterministico (semi fissi).
Uso: python -I -B ricalcoli.py   (circa 1 minuto)"""
import math, random, itertools, time
from fractions import Fraction as Fr

t0 = time.time()
def titolo(s): print("\n== " + s + " ==")

# ---------------------------------------------------------------- A. ricorsione di PI, controllo esaustivo
def dilata(mask, n, k=1):
    out = mask
    for _ in range(k):
        out = (out | (out << 1) | (out >> 1)) & ((1 << n) - 1)
    return out

def traiettorie(n, T, passo):
    """tutte le successioni x(0..T) con |x(t)-x(t-1)| <= passo, su n celle in linea"""
    out = []
    def rec(pref):
        if len(pref) == T + 1:
            out.append(tuple(pref)); return
        for y in range(max(0, pref[-1] - passo), min(n - 1, pref[-1] + passo) + 1):
            rec(pref + [y])
    for x0 in range(n):
        rec([x0])
    return out

def esaustivo(n, T, passo_vero, orizzonte=1):
    """per ogni successione F(0..T) di insiemi «visti liberi» (tutti i sottoinsiemi):
       PI(0)=tutto \\ F(0); PI(t)=dilata(PI(t-1)) \\ F(t).
       Confronta PI(T) con l'insieme delle posizioni finali delle traiettorie coerenti (x(t) non in F(t))."""
    tr = traiettorie(n, T, passo_vero)
    tutto = (1 << n) - 1
    seq = diff_fuori = diff_min = non_mono = falsi_liberi = dich = 0
    primo = None
    for Fs in itertools.product(range(1 << n), repeat=T + 1):
        seq += 1
        P = tutto & ~Fs[0]
        storia = [P]
        for t in range(1, T + 1):
            Pn = dilata(P, n) & ~Fs[t]
            if (P & ~Fs[t]) & ~Pn: non_mono += 1          # P3: PI(t) contiene PI(t-1) \ F(t)
            P = Pn; storia.append(P)
        fin = 0
        for x in tr:
            ok = True
            for t in range(T + 1):
                if (Fs[t] >> x[t]) & 1: ok = False; break
            if ok: fin |= 1 << x[T]
        if fin & ~P:
            diff_fuori += 1
            if primo is None: primo = (Fs, storia, fin)
        if P & ~fin: diff_min += 1
        # «libero adesso»: celle a distanza > orizzonte da PI(T-orizzonte) devono essere vuote al tempo T
        Pprima = storia[T - orizzonte]
        lib = tutto & ~dilata(Pprima, n, orizzonte)
        dich += bin(lib).count("1")
        if lib & fin: falsi_liberi += 1
    return seq, diff_fuori, diff_min, non_mono, falsi_liberi, dich, primo

titolo("A. Insieme di possibile presenza: controllo esaustivo su griglie 1D")
for (n, T) in ((4, 3), (5, 2)):
    s, a, b, c, d, e, _ = esaustivo(n, T, 1)
    print(f"n={n} celle, fotogrammi 0..{T}, passo vero <= 1: successioni di osservazione {s}; "
          f"con una posizione coerente fuori da PI: {a}; con una cella di PI non raggiunta da nessuna traiettoria coerente: {b}; "
          f"violazioni della monotonia: {c}; successioni con un «libero adesso» (orizzonte 1 passo) occupato: {d} (celle dichiarate {e})")
s, a, b, c, d, e, primo = esaustivo(4, 3, 2)
print(f"BRACCIO CHE DEVE FALLIRE n=4, fotogrammi 0..3, passo vero <= 2 (PI dilata di 1): successioni {s}; con una posizione coerente fuori da PI: {a}; «libero adesso» occupato: {d}")
s2, a2, b2, c2, d2, e2, primo2 = esaustivo(3, 1, 2)
print(f"controesempio minimo cercato su n=3, fotogrammi 0..1, passo vero <= 2: successioni {s2}; fuori da PI: {a2}")
if primo2:
    Fs, st, fin = primo2
    print("  primo controesempio: F(0)=%s F(1)=%s  PI(0)=%s PI(1)=%s  posizioni coerenti a t=1: %s" %
          tuple(format(v, "03b") for v in (Fs[0], Fs[1], st[0], st[1], fin)))

# ---------------------------------------------------------------- B. «libero» con memoria: controesempio minimo
titolo("B. «Libero» con memoria di 3 fotogrammi: controesempio minimo (1 cella, 2 fotogrammi)")
# pixel della cella: 'suolo' = profondita' valida al suolo; 'corpo' = ritorno valido piu' vicino; 'nullo' = non valido
def corrente(storia): return storia[-1] == "suolo"
def memoria3(storia): return any(s == "suolo" for s in storia[-3:])
def memoria3_occ(storia):  # occupato/ombra di ora vincono sulla memoria
    return storia[-1] != "corpo" and any(s == "suolo" for s in storia[-3:])
for nome, storia, occupata in (("corpo che rimanda segnale", ["suolo", "corpo"], True),
                               ("corpo che NON rimanda segnale", ["suolo", "nullo"], True),
                               ("buco isolato su suolo vuoto", ["suolo", "nullo"], False)):
    print(f"  {nome:32s} storia={storia} cella occupata={occupata}: solo fotogramma corrente -> libero={corrente(storia)}; "
          f"memoria 3 -> {memoria3(storia)}; memoria 3 con «occupato di ora vince» -> {memoria3_occ(storia)}")

# ---------------------------------------------------------------- C. limite sul livello dopo il ritaglio
titolo("C. Livello dopo il ritaglio senza rinormalizzare: q >= 1 - (1-p)/G(S)")
for GS in (0.23, 0.08):
    print(f"  p = 0,95, G(S) = {GS}: limite = {1 - 0.05 / GS:.4f}")
print(f"  p = 0,90, G(S) = 0,23: limite = {1 - 0.10 / 0.23:.4f};  il limite e' informativo (>0) solo se G(S) > 1-p")
rnd = random.Random(20261114)
viol = 0; minscarto = 9; casi = 2000; stretti = 0
for _ in range(casi):
    # gaussiana 2D discreta su griglia 41x41 (celle 0,1 m), covarianza casuale; E = regione di massima densita' al livello p
    sx, sy = rnd.uniform(0.2, 1.2), rnd.uniform(0.2, 1.2); r = rnd.uniform(-0.8, 0.8)
    p = rnd.choice((0.5, 0.9, 0.95))
    det = sx * sx * sy * sy * (1 - r * r)
    cel = []
    for i in range(41):
        for j in range(41):
            x, y = (i - 20) * 0.1, (j - 20) * 0.1
            qf = (x * x * sy * sy - 2 * r * sx * sy * x * y + y * y * sx * sx) / det
            cel.append((math.exp(-0.5 * qf), i, j))
    tot = sum(c[0] for c in cel)
    cel.sort(reverse=True)
    E = set(); acc = 0.0
    for w, i, j in cel:
        if acc >= p * tot: break
        E.add((i, j)); acc += w
    pE = acc / tot                                   # livello effettivo di E (>= p)
    # S: semipiano o cuneo casuale (le celle ammesse)
    a = rnd.uniform(0, 2 * math.pi); off = rnd.uniform(-1.5, 1.5)
    S = {(i, j) for _, i, j in cel if ((i - 20) * 0.1) * math.cos(a) + ((j - 20) * 0.1) * math.sin(a) > off}
    GS = sum(w for w, i, j in cel if (i, j) in S) / tot
    if GS <= 0: continue
    q = sum(w for w, i, j in cel if (i, j) in S and (i, j) in E) / tot / GS
    lim = 1 - (1 - pE) / GS
    if q < lim - 1e-12: viol += 1
    minscarto = min(minscarto, q - lim)
    if q - lim < 1e-9: stretti += 1
print(f"  {casi} casi casuali (gaussiana discreta, S = semipiano): violazioni {viol}; scarto minimo q - limite = {minscarto:.2e}; casi con uguaglianza (S contiene il complemento di E) {stretti}")
# esempio in cui il limite e' raggiunto: S = complemento di E unito a una parte di E
print("  uguaglianza: se S contiene tutto il complemento di E, G(S\\E) = 1-p e q = 1-(1-p)/G(S) esattamente")

# ---------------------------------------------------------------- D. cerchio a 1 sigma in due dimensioni
titolo("D. Contenuto del cerchio di raggio k·sigma, gaussiana isotropa")
print(f"  2D: P(r <= sigma) = 1 - exp(-1/2) = {1 - math.exp(-0.5):.4f};  P(r <= 2 sigma) = {1 - math.exp(-2):.4f}")
print(f"  2D: raggio al 95 % = sqrt(-2 ln 0,05) sigma = {math.sqrt(-2 * math.log(0.05)):.4f} sigma (quadrato {-2 * math.log(0.05):.3f}); al 99 %: quadrato {-2 * math.log(0.01):.3f}")
print(f"  1D: P(|x| <= sigma) = erf(1/sqrt 2) = {math.erf(1 / math.sqrt(2)):.4f}")
rnd = random.Random(1); N = 400000
k = sum(1 for _ in range(N) if rnd.gauss(0, 1) ** 2 + rnd.gauss(0, 1) ** 2 <= 1.0)
print(f"  Monte Carlo 2D, N = {N}: {k / N:.4f}")
rnd2 = random.Random(2); N2 = 2000000
k2 = sum(1 for _ in range(N2) if rnd2.gauss(0, 1) ** 2 + rnd2.gauss(0, 1) ** 2 <= 1.0)
print(f"  Monte Carlo 2D, secondo lancio (aggiunto dopo aver visto il primo), N = {N2}: {k2 / N2:.4f}; errore tipo {math.sqrt(0.3935*0.6065/N2):.4f}")
# ellisse a 1 sigma di una gaussiana NON isotropa: stesso contenuto (trasformazione affine)
sx, sy = 0.2, 0.9
k = sum(1 for _ in range(N) if (rnd.gauss(0, sx) / sx) ** 2 + (rnd.gauss(0, sy) / sy) ** 2 <= 1.0)
print(f"  ellisse a 1 sigma, sigma_x = {sx}, sigma_y = {sy}: {k / N:.4f}")

# ---------------------------------------------------------------- E. criterio d'accettazione a due stadi
titolo("E. Criterio a due stadi (>=28/30 regge; <=22 smentita; 23-27: altri 30 e >=52/60), composizione 21/5/4")
def pmf(n, p): return [math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(n + 1)]
def conv(a, b):
    o = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b): o[i + j] += x * y
    return o
def due_stadi(cp, cs, ct):
    d = conv(conv(pmf(21, cp), pmf(5, cs)), pmf(4, ct))
    p1 = sum(d[28:]); p2 = sum(d[a] * sum(d[b] for b in range(31) if a + b >= 52) for a in range(23, 28))
    return p1, p1 + p2, sum(d[:23])
for lab, c in (("prosegue 1, sosta 1, torna 1/2", (Fr(1), Fr(1), Fr(1, 2))),
               ("prosegue 1, sosta 1, torna 0 (mai coperto)", (Fr(1), Fr(1), Fr(0))),
               ("prosegue 1, sosta 0,93, torna 0", (Fr(1), Fr(93, 100), Fr(0))),
               ("tutti 0,90", (Fr(9, 10),) * 3), ("tutti 0,80", (Fr(8, 10),) * 3)):
    a, b, s = due_stadi(*c)
    print(f"  {lab:44s} P(regge al primo) = {float(a):.4f}  P(regge in tutto) = {float(b):.4f}{' (esattamente 1)' if b == 1 else ''}  P(smentita al primo) = {float(s):.4f}")
print("  con torna = 0: dentro = 26 su 30 con certezza -> secondo stadio; 26 + 26 = 52 >= 52 -> regge")
# criterio stratificato: 30 passaggi per comportamento, >=28 regge, <=23 smentita
for p in (Fr(1, 2), Fr(9, 10), Fr(95, 100)):
    d = pmf(30, p)
    print(f"  stratificato, 30 per comportamento, copertura {float(p):.2f}: P(>=28) = {float(sum(d[28:])):.3f}; P(<=23) = {float(sum(d[:24])):.4f}")

# ---------------------------------------------------------------- F. massa non identificabile
titolo("F. Informazione di Fisher di (F, m), punto materiale 1D con forza costante ignota, misure di posizione")
# p(t) = p0 + v0 t + (F/m) t^2/2 ; derivate rispetto a (F, m): t^2/(2m), -F t^2/(2 m^2)
Fv, m = Fr(120), Fr(75); sig2 = Fr(9, 10000); ts = [Fr(k, 15) for k in range(1, 31)]
J = [[t * t / (2 * m), -Fv * t * t / (2 * m * m)] for t in ts]
I = [[sum(r[a] * r[b] for r in J) / sig2 for b in range(2)] for a in range(2)]
det = I[0][0] * I[1][1] - I[0][1] * I[1][0]
print(f"  F = 120 N, m = 75 kg, sigma = 3 cm, 30 misure a 15 Hz: det(I) = {det} (aritmetica razionale); traccia = {float(I[0][0] + I[1][1]):.4g}; rango = {0 if I[0][0] == 0 else (1 if det == 0 else 2)}")
print(f"  direzione nulla: (F, m) proporzionale a (F, m): I·(F,m)^T = ({I[0][0]*Fv + I[0][1]*m}, {I[1][0]*Fv + I[1][1]*m})")
# con forza nota: la massa e' identificabile
Im = sum((Fv * t * t / (2 * m * m)) ** 2 for t in ts) / sig2
print(f"  con F nota: informazione su m = {float(Im):.4g} 1/kg^2 -> scarto tipo minimo {float(Im) ** -0.5:.3f} kg (caduta libera: a = g, derivata rispetto a m nulla)")

# ---------------------------------------------------------------- G. conti geometrici e di tempo
titolo("G. Margini")
for et, dg in ((0.0, 0.5), (0.03, 1.0), (0.05, 2.0)):
    print(f"  posa: eps_t = {et*100:.0f} cm, delta = {dg} gradi, r = 3 m: m = eps_t + r·delta = {100*(et + 3*math.radians(dg)):.1f} cm  (r·tan(delta) = {100*(et + 3*math.tan(math.radians(dg))):.1f} cm)")
D = 1 / 15
print(f"  passo Delta = 1/15 s = {D:.4f} s; 2 Delta = {2*D:.3f} s (eta' del «libero» ricordato per 3 fotogrammi)")
print(f"  v_max·2Delta: 2,5 m/s -> {2.5*2*D:.3f} m ; 1,4 m/s -> {1.4*2*D:.3f} m")
for tau in (0.150, 0.155):
    print(f"  tau = {tau} s: h = tau + Delta = {tau + D:.4f} s; fascia 0,40 m / h = {0.40/(tau + D):.3f} m/s; v_max·h a 2,5 e 1,4 m/s = {2.5*(tau+D):.3f}, {1.4*(tau+D):.3f} m")
T1 = 2 * D + 0.155
print(f"  eta' 2Delta + latenza 0,155 s = {T1:.3f} s: a 2,5 m/s {2.5*T1:.2f} m; a 1,4 m/s {1.4*T1:.3f} m; velocita' coperta da 0,40 m: {0.40/T1:.2f} m/s")
T2 = T1 + D
print(f"  con anche la tenuta dell'uscita per un passo: {T2:.3f} s -> velocita' coperta {0.40/T2:.2f} m/s; con errore del bordo 0,20 m: {0.20/T1:.2f} m/s (senza tenuta), {0.20/T2:.2f} m/s (con)")
print(f"  fascia 0,20 m, solo fotogramma corrente (eta' 0): {0.20/(0.155+D):.2f} m/s")
print(f"  soggetto nascosto a 9 cm dal volume, 1,4 m/s: {1000*0.09/1.4:.0f} ms; latenza 222 ms + un ciclo = {222 + 1000*D:.0f} ms")
print(f"  eta' utile del «libero» a distanza rho = 0,980 m (sfera inscritta): rho/v_max - h: 2,5 m/s -> {0.980/2.5 - (0.15+D):.3f} s; 1,4 m/s -> {0.980/1.4 - (0.15+D):.3f} s")

# ---------------------------------------------------------------- H. intervalli
titolo("H. Intervalli di Wilson al 95 % (z = 1,959964)")
def wilson(k, n, z=1.959964):
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0.0, c - h), min(1.0, c + h)
for lab, k, n in (("identita' al ritorno 400/400", 400, 400), ("regione al 90 %, 101/119", 101, 119),
                  ("nascosti fuori dall'avviso 0/19200", 0, 19200), ("idem 0/175802", 0, 175802),
                  ("passaggi con un vuoto 0/8314", 0, 2716 + 2800 + 2798), ("ingresso mancato 87/2800", 87, 2800),
                  ("ingresso mancato dopo la riga nuova 9/2800", 9, 2800), ("ombra -20 cm 499/600", 499, 600),
                  ("ombra -20 cm dopo 16/600", 16, 600), ("secondo soggetto 193/193", 193, 193), ("secondo soggetto 347/357", 347, 357),
                  ("memoria 3 fotogrammi, fotogrammi con falso libero 58/90", 58, 90), ("braccio velocita' doppia 23/24", 23, 24),
                  ("braccio velocita' doppia 21/24", 21, 24), ("PI: corse con falsi liberi 0/368", 0, 368)):
    lo, hi = wilson(k, n)
    print(f"  {lab:58s} {k}/{n} = {k/n:.4f}  [{lo:.4f}; {hi:.4f}]")
print(f"  400/400: limite inferiore di Clopper-Pearson unilaterale al 95 % = 0,05^(1/400) = {0.05 ** (1/400):.4f}; bilaterale = 0,025^(1/400) = {0.025 ** (1/400):.4f}")

# ---------------------------------------------------------------- I. probabilita' d'intrusione su distribuzione ritagliata
titolo("I. Probabilita' d'intrusione con la distribuzione ritagliata sull'ombra")
# griglia 1D lungo x, celle 1 cm; ombra = x in [0, 100) cm; volume protetto = [-59, -9] cm tutto in vista; soggetto fermo a x = 0..1 (9 cm dal volume)
for sig in (20.0, 32.0, 85.0):
    dens = {x: math.exp(-0.5 * ((x - 0.5) / sig) ** 2) for x in range(-300, 400)}
    tot = sum(dens.values())
    grezza = sum(v for x, v in dens.items() if -59 <= x < -9) / tot
    amm = {x: v for x, v in dens.items() if 0 <= x < 100}            # ritaglio: solo celle non viste libere
    rit = sum(v for x, v in amm.items() if -59 <= x < -9) / sum(amm.values())
    print(f"  sigma = {sig/100:.2f} m: P(intrusione) gaussiana non ritagliata = {grezza:.3f}; ritagliata sull'ombra = {rit:.1f} (supporto disgiunto dal volume)")

print(f"\ntempo totale: {time.time() - t0:.1f} s")
