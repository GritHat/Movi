# sim_classe.py -- sciame-tracciamento, f14/02-uso. Simulatore piccolo, numpy, un autore, nessun sensore.
# Uso: python -I -B sim_classe.py   (seme fisso; stampa le tabelle di USO_DELLA_CLASSE.md)
# MODELLO DICHIARATO: piano aperto (nessun ritaglio sulla maschera), ingresso nell'origine con rotta +x,
# passo 1/15 s, soggetto puntiforme. I valori delle classi sono VALORI DI LAVORO (ipotesi senza fonte).
import numpy as np

DT = 1.0 / 15.0
NS = 45  # 3 s
CELL = 0.10
rng = np.random.default_rng(20261114)

# profilo cinematico: v_max, a_max (accel.), b_max (frenata), k_max (curvatura, 1/m; None = olonomo), gdl
PROF = {
    "pedone":   dict(vmax=2.5, a=2.5, b=2.5, k=None, gdl="2, olonomo"),
    "carrello": dict(vmax=5.0, a=1.0, b=2.0, k=0.5, gdl="2, non olonomo, R>=2 m"),
    "treno":    dict(vmax=5.0, a=0.3, b=0.5, k=0.0, gdl="1, sul binario"),
}


def gen(cls, n, v0, noise=True):
    """Traiettorie 'vere' della classe: (n, NS+1, 2). Stato d'ingresso: origine, rotta +x, velocita' v0."""
    p = PROF[cls]
    th = (np.deg2rad(3.0) * rng.standard_normal(n)) if noise else np.zeros(n)
    v = v0 + (0.06 * rng.standard_normal(n) if noise else 0.0)
    v = np.clip(v, 0.05, p["vmax"])
    vref = v.copy()
    x = np.zeros(n); y = np.zeros(n)
    out = np.zeros((n, NS + 1, 2))
    u = rng.random(n)
    tev = rng.uniform(0.0, 3.0, n)            # istante dell'evento
    sgn = rng.choice([-1.0, 1.0], n)
    if cls == "pedone":   # 45 prosegue, 25 si ferma, 15 inverte, 15 svolta
        mode = np.digitize(u, [0.45, 0.70, 0.85])
        dth = sgn * rng.uniform(np.pi / 4, 2 * np.pi / 3, n); turned = np.zeros(n)
        d = np.ones(n)                         # verso (per chi inverte)
        for k in range(1, NS + 1):
            t = k * DT; ev = t >= tev
            th += 0.25 * np.sqrt(DT) * rng.standard_normal(n) * (mode == 0)
            v += (mode == 0) * (0.5 * (vref - v) * DT + 0.15 * np.sqrt(DT) * rng.standard_normal(n))
            stop = ev & (mode == 1); v = np.where(stop, np.maximum(v - 1.5 * DT, 0.0), v)
            inv = ev & (mode == 2)
            flip = inv & (v <= 1e-9) & (d > 0)
            d = np.where(flip, -1.0, d)
            v = np.where(inv & (d > 0), np.maximum(v - 1.5 * DT, 0.0), v)
            v = np.where(inv & (d < 0), np.minimum(v + 1.0 * DT, vref), v)
            tr = ev & (mode == 3) & (np.abs(turned) < np.abs(dth))
            w = np.minimum(2.0, 2.0 / np.maximum(v, 0.3)) * np.sign(dth)
            th = np.where(tr, th + w * DT, th); turned = np.where(tr, turned + w * DT, turned)
            v = np.clip(v, 0.0, p["vmax"])
            x += d * v * np.cos(th) * DT; y += d * v * np.sin(th) * DT
            out[:, k, 0] = x; out[:, k, 1] = y
    elif cls == "carrello":  # 55 prosegue, 20 frena, 15 svolta, 10 accelera; mai laterale
        mode = np.digitize(u, [0.55, 0.75, 0.90])
        kap = 0.03 * rng.standard_normal(n)
        ktg = sgn * rng.uniform(0.2, 0.5, n)
        for k in range(1, NS + 1):
            t = k * DT; ev = t >= tev
            kap += (mode != 2) * (-0.5 * kap * DT + 0.03 * np.sqrt(DT) * rng.standard_normal(n))
            kap = np.where(ev & (mode == 2), ktg, kap)
            v += (mode == 0) * 0.10 * np.sqrt(DT) * rng.standard_normal(n)
            v = np.where(ev & (mode == 1), v - 1.5 * DT, v)
            v = np.where(ev & (mode == 3), v + 1.0 * DT, v)
            vlat = np.sqrt(2.0 / np.maximum(np.abs(kap), 1e-6))     # a_lat <= 2 m/s^2
            v = np.where(v > vlat, np.maximum(v - 2.0 * DT, vlat), v)
            v = np.clip(v, 0.0, p["vmax"])
            th += v * kap * DT
            x += v * np.cos(th) * DT; y += v * np.sin(th) * DT
            out[:, k, 0] = x; out[:, k, 1] = y
    else:  # treno: 60 costante, 25 frena 0,5, 15 accelera 0,3; y = 0 (rotta del binario nota: nessun errore di rotta)
        mode = np.digitize(u, [0.60, 0.85])
        for k in range(1, NS + 1):
            t = k * DT; ev = t >= tev
            v += (mode == 0) * 0.03 * np.sqrt(DT) * rng.standard_normal(n)
            v = np.where(ev & (mode == 1), v - 0.5 * DT, v)
            v = np.where(ev & (mode == 2), v + 0.3 * DT, v)
            v = np.clip(v, 0.0, p["vmax"])
            x += v * DT
            out[:, k, 0] = x
    return out


def envelope(cls, n, v0):
    """Inviluppo cinematico della classe: controlli estremi a tratti, dallo stato d'ingresso (con il suo errore)."""
    p = PROF[cls]
    th = np.deg2rad(3.0) * rng.standard_normal(n) * (cls != "treno")
    sp = np.clip(v0 + 0.06 * rng.standard_normal(n), 0.0, p["vmax"])
    out = np.zeros((n, NS + 1, 2))
    x = np.zeros(n); y = np.zeros(n)
    if p["k"] is None:  # olonomo: |a| <= a_max in ogni direzione, |v| <= v_max
        vx = sp * np.cos(th); vy = sp * np.sin(th)
        ang = rng.uniform(0, 2 * np.pi, n); mag = p["a"] * rng.choice([0.0, 1.0, 1.0], n)
        for k in range(1, NS + 1):
            sw = rng.random(n) < DT / 0.7
            ang = np.where(sw, rng.uniform(0, 2 * np.pi, n), ang)
            mag = np.where(sw, p["a"] * rng.choice([0.0, 1.0, 1.0], n), mag)
            vx += mag * np.cos(ang) * DT; vy += mag * np.sin(ang) * DT
            s = np.hypot(vx, vy); f = np.minimum(1.0, p["vmax"] / np.maximum(s, 1e-9)); vx *= f; vy *= f
            x += vx * DT; y += vy * DT
            out[:, k, 0] = x; out[:, k, 1] = y
    else:
        acc = rng.choice([-p["b"], 0.0, p["a"]], n); kap = p["k"] * rng.choice([-1.0, 0.0, 1.0], n)
        for k in range(1, NS + 1):
            sw = rng.random(n) < DT / 0.7
            acc = np.where(sw, rng.choice([-p["b"], 0.0, p["a"]], n), acc)
            kap = np.where(sw, p["k"] * rng.choice([-1.0, 0.0, 1.0], n), kap)
            sp = np.clip(sp + acc * DT, 0.0, p["vmax"])
            if p["k"] > 0:
                sp = np.minimum(sp, np.where(np.abs(kap) > 0, np.sqrt(2.0 / np.maximum(np.abs(kap), 1e-6)) + 2.0, 1e9))
            th += sp * kap * DT
            x += sp * np.cos(th) * DT; y += sp * np.sin(th) * DT
            out[:, k, 0] = x; out[:, k, 1] = y
    return out


G0, GN = -12.0, 320  # griglia da -12 a +20 m


def cells(P):
    ij = np.floor((P - G0) / CELL).astype(int)
    return np.clip(ij, 0, GN - 1)


def dil(M):
    D = M.copy()
    D[1:, :] |= M[:-1, :]; D[:-1, :] |= M[1:, :]; D[:, 1:] |= M[:, :-1]; D[:, :-1] |= M[:, 1:]
    return D


def region90(P):
    """Celle piu' dense fino al 90 % dei membri, dopo una lisciatura 3x3."""
    H = np.zeros((GN, GN)); ij = cells(P); np.add.at(H, (ij[:, 0], ij[:, 1]), 1.0)
    S = H.copy()
    S[1:, :] += H[:-1, :]; S[:-1, :] += H[1:, :]; S[:, 1:] += H[:, :-1]; S[:, :-1] += H[:, 1:]
    o = np.argsort(-S, axis=None); c = np.cumsum(H.flat[o])
    kk = np.searchsorted(c, 0.90 * H.sum()) + 1
    M = np.zeros(GN * GN, bool); M[o[:kk]] = True
    return M.reshape(GN, GN)


def env_mask(P):
    M = np.zeros((GN, GN), bool); ij = cells(P); M[ij[:, 0], ij[:, 1]] = True
    return dil(M)


def cover(M, P):
    ij = cells(P); return M[ij[:, 0], ij[:, 1]].mean()


def tabella_regioni(v0, NL=6000, NT=6000, NE=60000):
    print(f"\n== Regioni, stato d'ingresso {v0} m/s; libreria {NL}, prova {NT} (semi distinti), inviluppo {NE} controlli ==")
    lib = {c: gen(c, NL, v0) for c in PROF}
    tru = {c: gen(c, NT, v0) for c in PROF}
    env = {c: envelope(c, NE, v0) for c in PROF}
    for ts in (1, 2, 3):
        k = ts * 15
        R = {c: region90(lib[c][:, k]) for c in PROF}
        E = {c: env_mask(env[c][:, k]) for c in PROF}
        print(f"t = {ts} s | disco prudente v_scen*t: 2,5 m/s -> {np.pi*(2.5*ts)**2:.1f} m2; 5 m/s -> {np.pi*(5*ts)**2:.1f} m2")
        for lab in PROF:
            a90 = R[lab].sum() * CELL**2; ae = E[lab].sum() * CELL**2
            s = " ".join(f"{t[:4]}: R90 {cover(R[lab], tru[t][:, k]):.3f} inv {cover(E[lab], tru[t][:, k]):.3f} |" for t in PROF)
            print(f"  etichetta {lab:8s} area R90 {a90:6.2f} m2, inviluppo {ae:6.2f} m2 | copertura del VERO -> {s}")
        # il vero entro il disco prudente
        for t in PROF:
            r = np.hypot(tru[t][:, k, 0], tru[t][:, k, 1])
            print(f"     vero {t:8s}: entro disco 2,5*t {np.mean(r <= 2.5*ts + 0.1):.3f}; entro 5*t {np.mean(r <= 5*ts + 0.1):.3f}; "
                  f"fermo o quasi (<0,3 m dall'ultimo secondo) {np.mean(np.hypot(*(tru[t][:, k] - tru[t][:, k-15]).T) < 0.3):.3f}")


# ---------- coerenza cinematica: Kalman a velocita' quasi costante + regola ----------
def kalman_speed(Z, q, sig=0.05):
    """Z: (n, K, 2). Ritorna v stimata (n,K,2), sigma_v (K), posizione stimata."""
    n, K, _ = Z.shape
    F = np.array([[1, DT], [0, 1.0]]); Q = q * np.array([[DT**3 / 3, DT**2 / 2], [DT**2 / 2, DT]])
    P = np.diag([sig**2, 4.0]); X = np.zeros((n, 2, 2)); X[:, 0, :] = Z[:, 0]
    V = np.zeros((n, K, 2)); Ppos = np.zeros((n, K, 2)); sv = np.zeros(K)
    for k in range(K):
        if k > 0:
            X = np.einsum("ab,nbc->nac", F, X); P = F @ P @ F.T + Q
            S = P[0, 0] + sig**2; Kg = P[:, 0] / S
            X = X + Kg[None, :, None] * (Z[:, k] - X[:, 0])[:, None, :]
            P = P - np.outer(Kg, P[0, :])
        V[:, k] = X[:, 1]; Ppos[:, k] = X[:, 0]; sv[k] = np.sqrt(P[1, 1])
    return V, sv, Ppos


def coerenza(tr, lab, q=0.2, K=45, ang_off=0.0):
    """Regola: scatta se in 4 degli ultimi 6 cicli (dal 4o ciclo di misura):
       (c1) |v| - 2 sigma_v > v_max;  (c2, 1 gdl) |dist dal binario| > 0,30 m + 2*0,05;
       (c3, non olonomo) curvatura stimata su 0,4 s > 1,5*k_max con |v| > 0,5 m/s, oppure inversione del verso in < 1 s."""
    p = PROF[lab]; n = tr.shape[0]
    if ang_off:
        c, s = np.cos(ang_off), np.sin(ang_off); tr = tr @ np.array([[c, s], [-s, c]])
    Z = tr[:, :K] + 0.05 * rng.standard_normal((n, K, 2))
    V, sv, Pp = kalman_speed(Z, q)
    sp = np.hypot(V[..., 0], V[..., 1])
    viol = sp - 2 * sv[None, :] > p["vmax"]
    if p["k"] == 0.0:
        viol |= np.abs(Pp[..., 1]) > 0.30 + 0.10
    if p["k"] is not None and p["k"] > 0:
        h = np.arctan2(V[..., 1], V[..., 0]); L = 6
        dh = np.zeros_like(h); dh[:, L:] = np.angle(np.exp(1j * (h[:, L:] - h[:, :-L])))
        spm = np.minimum(sp, np.roll(sp, L, axis=1))
        kap = np.abs(dh) / (L * DT) / np.maximum(spm, 1e-3)
        viol |= (kap > 1.5 * p["k"]) & (spm > 0.5 + 2 * sv[None, :])
        L2 = 15; rev = np.zeros_like(viol)
        rev[:, L2:] = (np.sum(V[:, L2:] * V[:, :-L2], axis=2) < 0) & (sp[:, L2:] > 0.5 + 2 * sv[None, L2:]) & (sp[:, :-L2] > 0.5 + 2 * sv[None, :-L2])
        viol |= rev
    viol[:, :4] = False
    cnt = np.cumsum(viol, axis=1); win = cnt.copy(); win[:, 6:] = cnt[:, 6:] - cnt[:, :-6]
    trig = win >= 4
    any_ = trig.any(axis=1); first = np.where(any_, trig.argmax(axis=1), -1)
    return any_.mean(), (np.median(first[any_]) * DT if any_.any() else float("nan")), (np.quantile(first[any_], 0.95) * DT if any_.any() else float("nan"))


def retta(n, v, K=45):
    out = np.zeros((n, K + 1, 2)); out[:, :, 0] = np.arange(K + 1) * DT * v; return out


def tabella_coerenza(n=4000):
    print("\n== Coerenza cinematica: quota di tracce smentite, ritardo mediano e 95o percentile dalla prima misura (s) ==")
    casi = [
        ("pedone vero (0,8-1,8 m/s), etichetta pedone, 3 s", np.concatenate([gen("pedone", n // 4, v) for v in (0.8, 1.2, 1.5, 1.8)]), "pedone", 0.2, 45, 0),
        ("carrello vero (1-4 m/s), etichetta carrello, 3 s", np.concatenate([gen("carrello", n // 4, v) for v in (1.0, 2.0, 3.0, 4.0)]), "carrello", 1.0, 45, 0),
        ("treno vero (0,5-4 m/s), etichetta treno, 3 s", np.concatenate([gen("treno", n // 4, v) for v in (0.5, 1.5, 3.0, 4.0)]), "treno", 0.2, 45, 0),
        ("'persona' a 6 m/s costanti in linea retta (1 s visibile)", retta(n, 6.0), "pedone", 0.2, 15, 0),
        ("'persona' a 3,5 m/s costanti in linea retta (1 s visibile)", retta(n, 3.5), "pedone", 0.2, 15, 0),
        ("'persona' a 2,8 m/s costanti (1 s visibile)", retta(n, 2.8), "pedone", 0.2, 15, 0),
        ("carrello LENTO vero (1-2,2 m/s), etichetta pedone, 3 s", np.concatenate([gen("carrello", n // 3, v) for v in (1.0, 1.6, 2.2)]), "pedone", 0.2, 45, 0),
        ("pedone vero (0,8-1,8), etichetta carrello, 3 s", np.concatenate([gen("pedone", n // 4, v) for v in (0.8, 1.2, 1.5, 1.8)]), "carrello", 1.0, 45, 0),
        ("pedone vero, etichetta treno, rotta a 20 gradi dal binario, 3 s", np.concatenate([gen("pedone", n // 2, v) for v in (1.0, 1.5)]), "treno", 0.2, 45, np.deg2rad(20)),
        ("pedone vero, etichetta treno, LUNGO il binario, 3 s", np.concatenate([gen("pedone", n // 2, v) for v in (1.0, 1.5)]), "treno", 0.2, 45, 0),
        ("'treno' che esce dal binario a 10 gradi, 2 m/s, 3 s", retta(n, 2.0), "treno", 0.2, 45, np.deg2rad(10)),
    ]
    for nome, tr, lab, q, K, off in casi:
        f, med, p95 = coerenza(tr, lab, q, K, off)
        print(f"  {nome:62s} n={tr.shape[0]:5d}  smentite {f:.4f}  mediana {med:.2f}  p95 {p95:.2f}")


# ---------- fascia di guardia: uscita dall'ombra con etichetta sbagliata ----------
def tabella_fascia(n=20000):
    Tun_max = 0.133 + 0.155 + 1 / 15.0   # eta' + latenza + tenuta (fascicolo dimostrazioni, prop. 8)
    eps = 0.0
    w_di = lambda v: eps + v * Tun_max
    print(f"\n== Fascia: w(v) = eps + v*(a+tau+Delta), tempo totale {Tun_max:.3f} s, eps = {eps} ==")
    for nome, v in [("base v3", None), ("pedone 2,5", 2.5), ("corsa 6", 6.0), ("carrello 5", 5.0), ("auto 8", 8.0), ("treno 5", 5.0), ("aereo 15", 15.0)]:
        print(f"  {nome:12s} w = {0.40 if v is None else w_di(v):.2f} m" + ("" if v is None else f"   (v coperta dalla base 0,40 m: {0.40/Tun_max:.2f} m/s)"))
    veri = {"pedone": (0.3, 1.8), "corsa": (3.0, 6.0), "carrello": (1.0, 5.0), "auto": (2.0, 8.0)}
    vlab = {"pedone": 2.5, "corsa": 6.0, "carrello": 5.0, "auto": 8.0}
    print("  quota di uscite dall'ombra con almeno un istante FUORI dall'avviso (vero x regola); uscita con angolo U(-60,60) gradi dalla normale al bordo,")
    print("  eta' del dato U(0, 0,133) s; scenario dichiarato = {pedone, corsa, carrello} -> v_scen = 6 m/s")
    for t, (lo, hi) in veri.items():
        v = rng.uniform(lo, hi, n) * np.cos(rng.uniform(-np.pi / 3, np.pi / 3, n))
        d = v * (rng.uniform(0, 0.133, n) + 0.155 + 1 / 15.0)
        r = [f"base 0,40: {np.mean(d > 0.40):.3f}"]
        for lab in ("pedone", "carrello"):
            r.append(f"C (w dell'etichetta '{lab}'): {np.mean(d > w_di(vlab[lab])):.3f}")
        r.append(f"A (w dello scenario, 6 m/s): {np.mean(d > w_di(6.0)):.3f}")
        r.append(f"B (max(scenario, etichetta 'pedone')): {np.mean(d > max(w_di(6.0), w_di(2.5))):.3f}")
        print(f"   vero {t:8s} | " + " | ".join(r) + f" | scarto massimo oltre w('pedone'): {max(0, d.max()-w_di(2.5)):.2f} m")


# ---------- profilo di chi porta il sensore ----------
def tabella_portatore():
    tau, tconf, D = 0.155, 0.267, 3.0
    print(f"\n== Portatore: d_serve = (v_obj+v_ego)*(tconf+tau+T_r) + v_ego^2/(2b) + v_obj*v_ego/b + C ;  tau={tau}, tconf={tconf}, D={D} m ==")
    prof = [("stazione fissa, operatore", 0.0, 1.0, None), ("UGV lento, arresto automatico", 0.5, 0.3, 1.0), ("UGV lento, operatore remoto", 0.5, 1.5, 1.0),
            ("non vedente ferma", 0.0, 1.5, None), ("non vedente in cammino", 1.0, 1.5, 2.0)]
    for C in (0.0, 0.5):
        print(f"  C = {C} m")
        for nome, ve, Tr, b in prof:
            Tst = 0.0 if b is None else ve / b
            T = tconf + tau + Tr
            dst = 0.0 if b is None else ve**2 / (2 * b)
            vcov = (D - C - ve * T - dst) / (T + Tst)
            row = " ".join(f"{vo}: {(vo+ve)*T + dst + vo*Tst + C:5.2f}" for vo in (1.4, 2.5, 5.0, 8.0, 15.0))
            wm = (2.5 + ve) * 0.355
            print(f"   {nome:30s} v_ego {ve} T_r {Tr} b {b} | anticipo {T+Tst:.2f} s | d_serve (m) per v_obj -> {row} | v_obj coperta a 3 m: {vcov:5.2f} m/s | w(2,5+v_ego) {wm:.2f} m")


if __name__ == "__main__":
    for v0 in (1.5, 3.0):
        tabella_regioni(v0)
    tabella_coerenza()
    tabella_fascia()
    tabella_portatore()


# ---------- aggiunta DOPO la prima esecuzione (18:37): estensione di R90 lungo la rotta e di lato ----------
def tabella_estensioni(NL=6000):
    print("\n== [aggiunta dopo] Estensione di R90 (m): lungo la rotta (x min..max) e di lato (larghezza in y); quota di membri fermi nell'ultimo 0,5 s ==")
    for v0 in (1.5, 3.0):
        for c in PROF:
            if c == "pedone" and v0 > 2.5:
                continue
            L = gen(c, NL, v0)
            for ts in (1, 2, 3):
                k = ts * 15; M = region90(L[:, k]); ii, jj = np.nonzero(M)
                x0, x1 = G0 + ii.min() * CELL, G0 + (ii.max() + 1) * CELL; wy = (jj.max() - jj.min() + 1) * CELL
                fermi = np.mean(np.hypot(*(L[:, k] - L[:, k - 7]).T) < 0.05)
                ij = cells(L[:, k]); dentro = M[ij[:, 0], ij[:, 1]]
                fd = np.mean(dentro[np.hypot(*(L[:, k] - L[:, k - 7]).T) < 0.05]) if fermi > 0 else float("nan")
                print(f"  v0 {v0} {c:8s} t={ts}s  x da {x0:5.1f} a {x1:5.1f}  largh. y {wy:4.1f}  area {M.sum()*CELL**2:6.2f}  fermi {fermi:.3f}  fermi dentro R90 {fd:.3f}")


if __name__ == "__main__":
    tabella_estensioni()
