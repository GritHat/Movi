"""Ricalcoli del fascicolo «rilevamento, associazione e stima dello stato».

Programma autonomo: non importa nessun modulo del progetto e non legge nessun dato.
Uso: python -I -B ricalcoli.py   (numpy e scipy)
"""
import math

import numpy as np
from scipy import stats

rng = np.random.default_rng(20261114)


def titolo(t):
    print("\n== " + t + " ==")


def wilson(k, n, z=1.959964):
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return max(0.0, c - h), min(1.0, c + h)


# ---------------------------------------------------------------- A. rumore
def sigma_z(d, curva="nom"):
    if curva == "nom":                      # d^2 * sigma_d / (f b): sigma_d 0,08 px, f 424 px, b 0,05 m
        return d * d * 0.08 / (424.0 * 0.05)
    if curva == "pes":                      # pessimista: 4 cm a 2 m, quadratica
        return 0.04 * (d / 2.0) ** 2
    return 0.05 * (d / 2.0) ** 2            # severa: 5 cm a 2 m, quadratica


def sigma_t(d):                             # trasversale: cella di 1 grado, errore uniforme
    return d * math.radians(1.0) / math.sqrt(12.0)


titolo("A. rumore di profondita' e trasversale (cm) a 2 / 3 / 4 m")
for c in ("nom", "pes", "sev"):
    print(c, " / ".join("%.2f" % (100 * sigma_z(d, c)) for d in (2, 3, 4)))
print("trasversale", " / ".join("%.2f" % (100 * sigma_t(d)) for d in (2, 3, 4)))
print("distanza con sigma_z = 5 cm: nom %.2f m, pes %.2f m, sev %.2f m" % (
    math.sqrt(0.05 * 424 * 0.05 / 0.08), 2 * math.sqrt(0.05 / 0.04), 2.0))
f_px = 212.0 / math.tan(math.radians(43.5))
n_px = 0.4 * 1.7 * f_px ** 2 / 4.0
print("pixel su una sagoma 0,4 x 1,7 m a 2 m (424 px, 87 gradi): f = %.0f px, n = %.0f; sigma_z/sqrt(n) = %.3f cm"
      % (f_px, n_px, 100 * sigma_z(2) / math.sqrt(n_px)))

# ---------------------------------------------------------------- B. regola «mobile», forma chiusa
titolo("B. regola «mobile»: soglia, falso allarme, rilevamento (prova singola)")
k_s, m_f = 5.0, 3
print("sigma della differenza di due medie di %d fotogrammi: sigma*sqrt(2/%d) = %.4f sigma" % (m_f, m_f, math.sqrt(2 / m_f)))
print("soglia = %.4f sigma  (5*sqrt(2)/sqrt(3)); senza media sarebbe %.4f sigma" % (k_s * math.sqrt(2 / m_f), k_s * math.sqrt(2)))
pfa1 = 2 * stats.norm.sf(k_s)
print("falso allarme per prova e per asse: 2Q(5) = %.3e" % pfa1)
for hz in (15,):
    n_prove = hz - 2                        # prove nel primo secondo: k = 5..15 -> 11; limite superiore 13
    print("limite d'unione nel primo secondo, 2 assi, %d prove: %.2e" % (n_prove, 2 * n_prove * pfa1))
print("limite su 4000 tracce ferme: %.3f tracce attese con almeno un falso" % (4000 * 2 * 13 * pfa1))
print("sigma creduto la meta' del vero: soglia effettiva 2,5 sigma_delta -> per prova e asse %.4f" % (2 * stats.norm.sf(2.5)))

DT = 1 / 15.0
print("\nprova singola alla finestra massima (13 passi = %.3f s), 0,5 m/s, spostamento %.3f m" % (13 * DT, 0.5 * 13 * DT))
for c in ("nom", "pes", "sev"):
    for d0 in (2.0, 3.0):
        delta = 0.5 * 13 * DT
        s1, s2 = sigma_z(d0 - 0.5 * DT, c), sigma_z(d0 - 0.5 * 14 * DT, c)   # centro delle due medie
        sd = math.sqrt((s1 ** 2 + s2 ** 2) / m_f)
        soglia = k_s * sigma_z(d0, c) * math.sqrt(2 / m_f)
        pd = stats.norm.sf((soglia - delta) / sd) + stats.norm.sf((soglia + delta) / sd)
        print("  avvicinamento %s da %.0f m: soglia %.3f m, sigma_delta %.4f m, Pd(prova singola) = %.4f" % (c, d0, soglia, sd, pd))
print("velocita' minima (Pd 0,5 e 0,9 alla finestra massima, rumore uguale ai due capi):")
for c in ("nom", "pes", "sev"):
    for d0 in (2.0, 3.0):
        s = sigma_z(d0, c) * math.sqrt(2 / m_f)
        print("  %s %.0f m radiale: %.3f / %.3f m/s" % (c, d0, k_s * s / (13 * DT), (k_s + 1.2816) * s / (13 * DT)))
for d0 in (2.0, 3.0):
    s = sigma_t(d0) * math.sqrt(2 / m_f)
    print("  trasversale %.0f m: %.3f / %.3f m/s" % (d0, k_s * s / (13 * DT), (k_s + 1.2816) * s / (13 * DT)))

# ---------------------------------------------------------------- C. modello a velocita' quasi costante
titolo("C. velocita' quasi costante: Q in forma chiusa, crescita senza misure")


def F1(dt):
    return np.array([[1.0, dt], [0.0, 1.0]])


def Q1(dt, q):
    return q * np.array([[dt ** 3 / 3, dt ** 2 / 2], [dt ** 2 / 2, dt]])


# controllo numerico di Q: integrale di e^{As} G q G' e^{A's} su [0, dt]
dt, q = DT, 0.2
ss = (np.arange(200000) + 0.5) * dt / 200000
Qnum = np.zeros((2, 2))
for s in ss[::20]:
    g = np.array([[s], [1.0]])
    Qnum += q * (g @ g.T) * (dt / (200000 / 20))
print("Q chiusa - Q numerica, massimo scarto relativo: %.2e" % np.max(np.abs(Qnum - Q1(dt, q)) / Q1(dt, q)))
# semigruppo: Q(2dt) = F Q(dt) F' + Q(dt)
print("proprieta' di composizione, scarto: %.2e" % np.max(np.abs(F1(dt) @ Q1(dt, q) @ F1(dt).T + Q1(dt, q) - Q1(2 * dt, q))))


def regime(q, sig, dt=DT, n=4000):
    P = np.diag([sig ** 2, 2.5 ** 2])
    for _ in range(n):
        P = F1(dt) @ P @ F1(dt).T + Q1(dt, q)
        K = P[:, :1] / (P[0, 0] + sig ** 2)
        P = (np.eye(2) - K @ np.array([[1.0, 0.0]])) @ P
    return P


def sigma_p(P, tau, q):
    return math.sqrt(P[0, 0] + 2 * tau * P[0, 1] + tau ** 2 * P[1, 1] + q * tau ** 3 / 3)


C90, C95, C50, C99 = (stats.chi2.ppf(a, 2) for a in (0.90, 0.95, 0.50, 0.99))
print("chi quadrato a 2 gdl: 50 %% %.4f, 90 %% %.4f, 95 %% %.4f, 99 %% %.4f; -2 ln(0,01) = %.4f"
      % (C50, C90, C95, C99, -2 * math.log(0.01)))
print("rapporto dei raggi 90 %% / 50 %% di una gaussiana isotropa: %.3f" % math.sqrt(C90 / C50))

print("\nsolo termine di processo sqrt(q tau^3 / 3), m:")
for q in (0.2, 0.1, 0.05):
    print("  q = %.2f: " % q + " / ".join("%.3f" % math.sqrt(q * t ** 3 / 3) for t in (0.5, 1, 2, 3)))
for sig in (0.05, 0.015):
    print("\nsigma_p(tau_occ) per asse a regime (15 Hz, sigma misura %.1f cm), m, a 0,5 / 1 / 2 / 3 s; poi raggi 90 %% e 95 %%:" % (100 * sig))
    for q in (0.2, 0.1, 0.05):
        P = regime(q, sig)
        sp = [sigma_p(P, t, q) for t in (0.5, 1, 2, 3)]
        print("  q = %.2f: regime sigma_pos %.4f m, sigma_vel %.4f m/s, cov %.5f" % (q, math.sqrt(P[0, 0]), math.sqrt(P[1, 1]), P[0, 1]))
        print("     sigma_p: " + " / ".join("%.3f" % s for s in sp))
        print("     r90:     " + " / ".join("%.2f" % (s * math.sqrt(C90)) for s in sp))
        print("     r95:     " + " / ".join("%.2f" % (s * math.sqrt(C95)) for s in sp))
P = regime(0.2, 0.05)
print("\nraggio al 90 %% a 1 / 2 / 3 / 5 s (q 0,2, sigma 5 cm, regime): " + " / ".join("%.2f" % (sigma_p(P, t, 0.2) * math.sqrt(C90)) for t in (1, 2, 3, 5)))
print("raggio al 95 %% a 0,5 / 1 / 2 / 3 s (stesso caso): " + " / ".join("%.2f" % (sigma_p(P, t, 0.2) * math.sqrt(C95)) for t in (0.5, 1, 2, 3)))
for soglia in (1.0, 1.5, 2.0):
    t = 0.0
    while sigma_p(P, t, 0.2) * math.sqrt(C95) < soglia:
        t += 0.001
    print("raggio al 95 %% > %.1f m dopo %.2f s" % (soglia, t))


def rincorsa(q, sig, n_pre=15, dt=DT, sv=2.5):
    P = np.diag([sig ** 2, sv ** 2])
    for _ in range(1, n_pre):
        P = F1(dt) @ P @ F1(dt).T + Q1(dt, q)
        K = P[:, :1] / (P[0, 0] + sig ** 2)
        IKH = np.eye(2) - K @ np.array([[1.0, 0.0]])
        P = IKH @ P @ IKH.T + K @ K.T * sig ** 2
    return P


print("\nraggio al 95 %% con rincorsa di 1 s (15 misure, sigma 2 cm, sigma_v iniziale 2,5 m/s), m a 0,5 / 1 / 2 / 3 s:")
for q in (0.2, 0.1, 0.05, 0.01):
    P = rincorsa(q, 0.02)
    print("  q = %.2f: " % q + " / ".join("%.2f" % (sigma_p(P, t, q) * math.sqrt(C95)) for t in (0.5, 1, 2, 3))
          + "   sigma_p a 1/2/3 s: " + " / ".join("%.3f" % sigma_p(P, t, q) for t in (1, 2, 3)))

# ---------------------------------------------------------------- D. accelerazione
titolo("D. accelerazione: differenza seconda e limite dei minimi quadrati")
for sp_, hz in ((0.03, 30), (0.03, 15), (0.03, 10), (0.015, 30), (0.05, 15)):
    print("sigma_p %.1f cm, %d Hz: sigma_a = sqrt(6) sigma_p / Delta^2 = %.1f m/s^2; sigma_v (differenza prima) = %.2f m/s"
          % (100 * sp_, hz, math.sqrt(6) * sp_ * hz * hz, math.sqrt(2) * sp_ * hz))
print("sigma_z = 2 %% della distanza a 4 m = %.0f cm; a 1,5 m = %.0f cm" % (100 * 0.02 * 4, 100 * 0.02 * 1.5))
print("limite dei minimi quadrati (polinomio di grado 2 su N campioni, sigma_p 3 cm, 30 Hz): sigma dell'accelerazione")
for T in (0.1, 0.2, 0.5, 1.0):
    N = int(round(T * 30)) + 1
    t = np.arange(N) / 30.0
    A = np.stack([np.ones(N), t, t * t / 2], axis=1)
    cov = np.linalg.inv(A.T @ A) * 0.03 ** 2
    A2 = A[:, :2]
    cov2 = np.linalg.inv(A2.T @ A2) * 0.03 ** 2
    print("  finestra %.1f s (N = %2d): sigma_a = %6.2f m/s^2; sigma_v con accelerazione stimata %.3f, senza %.3f m/s"
          % (T, N, math.sqrt(cov[2, 2]), math.sqrt(cov[1, 1]), math.sqrt(cov2[1, 1])))

# ---------------------------------------------------------------- E. osservabilita'
titolo("E. rango della matrice di osservabilita'")


def rango_oss(F, H):
    n = F.shape[0]
    O = np.vstack([H @ np.linalg.matrix_power(F, i) for i in range(n)])
    return np.linalg.matrix_rank(O)


F4 = np.block([[np.eye(2), DT * np.eye(2)], [np.zeros((2, 2)), np.eye(2)]])
H4 = np.hstack([np.eye(2), np.zeros((2, 2))])
print("2D, stato [p, v], misura di posizione: rango %d su 4" % rango_oss(F4, H4))
F6 = np.block([[np.eye(3), DT * np.eye(3)], [np.zeros((3, 3)), np.eye(3)]])
H6q = np.hstack([np.eye(3), np.zeros((3, 3))])
H6 = H6q[[0, 2], :]                          # (p_x, p_z): senza la quota
print("3D, stato [p, v] a 6, misura (p_x, p_z) senza quota: rango %d su 6" % rango_oss(F6, H6))
print("3D, con la quota misurata: rango %d su 6" % rango_oss(F6, H6q))
Fa = np.array([[1, DT, DT * DT / 2], [0, 1, DT], [0, 0, 1.0]])
print("1D, stato [p, v, a], misura di posizione: rango %d su 3 (osservabile in senso algebrico)" % rango_oss(Fa, np.array([[1.0, 0, 0]])))

# ---------------------------------------------------------------- F. porta e conferma
titolo("F. porta di validazione e conferma 3 su 5")
print("gamma = %.4f; probabilita' che la misura vera cada in porta: 0,99" % C99)
for sp_ in (0.05, 0.3):
    print("area della porta con S = %.3f^2 I: pi*gamma*sqrt|S| = %.4f m^2" % (sp_, math.pi * C99 * sp_ ** 2))
pd = 0.9
for n in (3, 4, 5):
    p_ok = sum(stats.binom.pmf(k, n, pd) for k in range(3, n + 1))
    print("Pd 0,9, %d fotogrammi visibili: confermata %.4f, non confermata %.4f" % (n, p_ok, 1 - p_ok))
print("ritardo di conferma dal primo rilevamento (Pd 0,9; servono altri 2 fra i 4 successivi):")
acc = 0.0
for j in (2, 3, 4):
    pj = stats.binom.pmf(1, j - 1, pd) * pd
    acc += pj
    print("  al fotogramma +%d (%.3f s a 15 Hz): %.4f (cumulata %.4f)" % (j, j * DT, pj, acc))
print("  media condizionata %.3f fotogrammi = %.3f s" % (
    sum(j * stats.binom.pmf(1, j - 1, pd) * pd for j in (2, 3, 4)) / acc,
    sum(j * stats.binom.pmf(1, j - 1, pd) * pd for j in (2, 3, 4)) / acc * DT))
print("traccia falsa: dato un primo falso, probabilita' di altri >= 2 falsi in porta nei 4 cicli seguenti (p per ciclo):")
for p in (0.001, 0.01, 0.05, 0.1, 0.3):
    pf = 1 - (1 - p) ** 4 - 4 * p * (1 - p) ** 3
    print("  p = %.3f: %.3e   (6 p^2 = %.3e)" % (p, pf, 6 * p * p))
print("p da una frequenza beta per cella e per ciclo e una porta di n_c celle: 1-(1-beta)^n_c")
for beta, nc in ((1e-4, 30), (1e-3, 30), (1e-2, 30)):
    p = 1 - (1 - beta) ** nc
    print("  beta = %.0e, n_c = %d: p = %.4f, traccia falsa per innesco %.2e" % (beta, nc, p, 1 - (1 - p) ** 4 - 4 * p * (1 - p) ** 3))

# ---------------------------------------------------------------- G. copertura
titolo("G. copertura attesa con il modello esatto, e confronto con i pedoni veri")
N = 20000
q, sig = 0.2, 0.02
n_pre = 15
Fm, Qm = F1(DT), Q1(DT, q)
Lq = np.linalg.cholesky(Qm)
dentro = {1: 0, 2: 0, 3: 0}
dentro50 = {1: 0, 2: 0, 3: 0}
err = {1: [], 2: [], 3: []}
# verita' generata dal modello stesso (accelerazione bianca di densita' q), due assi indipendenti
x = np.zeros((N, 2, 2))
x[:, :, 1] = rng.normal(0, 1.0, (N, 2))
est = None
P = np.diag([sig ** 2, 2.5 ** 2])
xs = np.zeros((N, 2, 2))
z = x[:, :, 0] + rng.normal(0, sig, (N, 2))
xs[:, :, 0] = z
for i in range(1, n_pre):
    x = x @ Fm.T + rng.normal(0, 1, (N, 2, 2)) @ Lq.T
    xs = xs @ Fm.T
    P = Fm @ P @ Fm.T + Qm
    K = P[:, 0] / (P[0, 0] + sig ** 2)
    z = x[:, :, 0] + rng.normal(0, sig, (N, 2))
    xs = xs + (z - xs[:, :, 0])[:, :, None] * K[None, None, :]
    IKH = np.eye(2) - np.outer(K, [1.0, 0.0])
    P = IKH @ P @ IKH.T + np.outer(K, K) * sig ** 2
for h in (1, 2, 3):
    steps = 15 * h
    xt = x.copy()
    for _ in range(steps):
        xt = xt @ Fm.T + rng.normal(0, 1, (N, 2, 2)) @ Lq.T
    tau = steps * DT
    pred = xs[:, :, 0] + tau * xs[:, :, 1]
    var = sigma_p(P, tau, q) ** 2
    e = pred - xt[:, :, 0]
    d2 = (e ** 2).sum(axis=1) / var
    c90, c50 = (d2 <= C90).mean(), (d2 <= C50).mean()
    print("orizzonte %d s: copertura 90 %% = %.4f (Wilson %.3f-%.3f), 50 %% = %.4f; errore mediano %.3f m (teorico %.3f)"
          % (h, c90, *wilson(int((d2 <= C90).sum()), N), c50, np.median(np.sqrt((e ** 2).sum(axis=1))), math.sqrt(var * C50)))
print("\nse il modello fosse esatto, su N = 219 tratti indipendenti al livello 0,90:")
print("  attesi %.1f dentro, scarto tipo %.2f; intervallo centrale al 95 %%: %d-%d su 219 (%.3f-%.3f)" % (
    219 * 0.9, math.sqrt(219 * 0.09), stats.binom.ppf(0.025, 219, 0.9), stats.binom.ppf(0.975, 219, 0.9),
    stats.binom.ppf(0.025, 219, 0.9) / 219, stats.binom.ppf(0.975, 219, 0.9) / 219))
for k in (214, 215, 218, 219):
    print("  P(X >= %d | p = 0,90) = %.2e; quota %.3f, Wilson %.3f-%.3f" % (k, stats.binom.sf(k - 1, 219, 0.9), k / 219, *wilson(k, 219)))
for k, lab in ((174, "0,795"), (176, "0,804"), (182, "0,831"), (207, "0,945")):
    print("  %d su 219 = %.3f (file: %s), Wilson %.3f-%.3f, P(X <= k | 0,90) = %.2e" % (k, k / 219, lab, *wilson(k, 219), stats.binom.cdf(k, 219, 0.9)))
print("\nq efficace dall'errore mediano (mediana di Rayleigh = sigma_p*sqrt(2 ln 2) = %.4f sigma_p):" % math.sqrt(2 * math.log(2)))
P = rincorsa(0.2, 0.02)
for tau, med in ((1, 0.21), (2, 0.49), (3, 0.81)):
    sp_ = sigma_p(P, tau, 0.2)
    atteso = sp_ * math.sqrt(C50)
    # risolve in q': mediana(q') = med, con la stessa rincorsa
    lo, hi = 1e-4, 2.0
    for _ in range(60):
        mid = math.sqrt(lo * hi)
        Pm = rincorsa(mid, 0.02)
        if sigma_p(Pm, tau, mid) * math.sqrt(C50) < med:
            lo = mid
        else:
            hi = mid
    print("  tau %d s: sigma_p %.3f m, mediana attesa con q 0,2 = %.3f m, osservata %.2f m; q efficace %.3f; (rapporto)^2*0,2 = %.3f"
          % (tau, sp_, atteso, med, mid, 0.2 * (med / atteso) ** 2))

# ---------------------------------------------------------------- H. miscela di comportamenti
titolo("H. cerchio del filtro e miscela di comportamenti (conto illustrativo)")
P = regime(0.2, 0.05)
print("ipotesi: v0 = 1,2 m/s, manovra istantanea a un istante uniforme in [0, tau], errore di stima iniziale trascurato")
for tau in (1.0, 2.0, 3.0):
    for liv, c in ((0.90, C90), (0.50, C50)):
        r = sigma_p(P, tau, 0.2) * math.sqrt(c)
        cop_torna = min(1.0, r / (2 * 1.2) / tau)       # errore 2 v (tau - t_r) <= r
        cop_ferma = min(1.0, r / 1.2 / tau)             # errore v (tau - t_s) <= r
        mix = 0.70 * 1.0 + 0.18 * cop_ferma + 0.12 * cop_torna
        print("  tau %.0f s, livello %.2f: raggio %.2f m; prosegue 1,00; si ferma %.2f; torna %.2f; miscela 70/18/12: %.2f"
              % (tau, liv, r, cop_ferma, cop_torna, mix))

# ---------------------------------------------------------------- I. intervalli di Wilson delle frequenze citate
titolo("I. intervalli di Wilson al 95 % delle frequenze citate")
for k, n, cosa in ((79, 90, "pannello fermo detto mobile"), (5, 90, "idem, soglia di punti rialzata"), (0, 90, "identita' con soglie assolute"),
                   (41, 45, "identita' con soglia rialzata, passaggi di prova"), (0, 6, "identita' al livello limite"),
                   (2400, 2400, "secondo soggetto dalla stessa ombra"), (2000, 2000, "mobile a 2 m"),
                   (1717, 2000, "85,85 % di 2000"), (532, 2000, "26,6 % di 2000"), (0, 4000, "falsi su fermo"),
                   (400, 400, "riaggancio, una traccia pendente"), (20, 20, "attraversamento visto entro 1 s"),
                   (4, 20, "avvicinamento da 4,3 m"), (0, 20, "avvicinamento da 4,3 m, soglie assolute"),
                   (193, 193, "entra uno, escono due"), (13, 15, "13 su 15"), (28, 30, "28 su 30")):
    lo, hi = wilson(k, n)
    print("  %4d su %4d = %.4f  [%.4f; %.4f]  %s" % (k, n, k / n, lo, hi, cosa))
