#!/usr/bin/env python3
# sciame-kalman, f9/03-kalman: S3 (due ipotesi) e S4 (informazione negativa) della preproposta.
# Python puro, semi fissati.  Uso:
#   timeout 120 python3 sim_s3s4.py <prosegue|sosta|ritorno|lontano|passo> <errore_maschera_m: 0 oppure -0.2> <L1|L2> [N]
# L1 = massa azzerata sul solo "libero" (resta su ombra e su tutto il non osservato);
# L2 = massa ammessa sulla sola ombra stimata entro la portata (aggiunta DOPO la prova di fumo: vedi PREVISIONI.md).
# Stampa una tabella e una riga "DATI ..." che aggrega_s3s4.py rilegge.
import sys, math, random, time

DT = 1.0 / 15.0
PD = 0.9
SIG = 0.03            # rumore di posizione per asse (m), circa la curva nominale a 2,3 m
QK = 0.2              # q del nucleo (m^2/s^3)
TF = math.tan(math.radians(43.5))
RMAX2 = 9.0           # portata 3 m
RMIN2 = 1.24 ** 2     # anello cieco
ZP = 1.8              # pannello a 1,8 m, largo 1 m
KW = 0.5 / ZP
HB = 0.2              # mezzo corpo: gruppo tagliato dall'ombra, nessuna misura (C6)
CK = (8, 15, 30, 45)  # 0,53 / 1 / 2 / 3 s dall'ultima misura
NON, SH, LIB = 0, 1, 2
SQ2 = math.sqrt(2.0)
erf = math.erf


def cls(x, z, e):
    if z <= 0.0:
        return NON
    r2 = x * x + z * z
    if r2 > RMAX2 or r2 < RMIN2:
        return NON
    ax = abs(x)
    if ax > TF * z:
        return NON
    if z > ZP and ax < KW * z + e:
        return SH
    return LIB


def hidden_true(x, z):
    if z > ZP and abs(x) < KW * z:
        return True
    return cls(x, z, 0.0) == NON


def detectable(x, z):
    if cls(x, z, 0.0) != LIB:
        return False
    return z <= ZP or abs(x) >= KW * z + HB


def neginfo(x, z, e, g):
    if cls(x, z, e) != LIB:
        return False
    if z > ZP:
        return abs(x) >= KW * z + e + g
    return z < ZP - g or abs(x) >= 0.5 + e + g


# ---- righe per la massa gaussiana sul "libero" (maschera stimata)
def build_rows(e):
    rows = []
    for i in range(30):
        z0 = i * 0.1
        zc = z0 + 0.05
        xf = TF * zc
        if zc * zc >= RMAX2:
            continue
        xr = math.sqrt(RMAX2 - zc * zc)
        xm = min(xf, xr)
        ints = []
        if zc > ZP:
            s = max(0.0, KW * zc + e)
            if s < xm:
                ints = [(-xm, -s), (s, xm)]
        else:
            xb = math.sqrt(RMIN2 - zc * zc) if zc * zc < RMIN2 else 0.0
            if xb < xm:
                ints = [(-xm, -xb), (xb, xm)] if xb > 0 else [(-xm, xm)]
        if ints:
            rows.append((z0, z0 + 0.1, ints))
    return rows


def build_rows_sh(e):
    rows = []
    for i in range(18, 30):
        z0 = i * 0.1
        zc = z0 + 0.05
        if zc <= ZP or zc * zc >= RMAX2:
            continue
        xm = min(TF * zc, math.sqrt(RMAX2 - zc * zc))
        s = min(max(0.0, KW * zc + e), xm)
        if s > 0:
            rows.append((z0, z0 + 0.1, [(-s, s)]))
    return rows


def libmass(rows, mx, mz, s):
    inv = 1.0 / (s * SQ2)
    tot = 0.0
    for z0, z1, ints in rows:
        wz = 0.5 * (erf((z1 - mz) * inv) - erf((z0 - mz) * inv))
        if wz < 1e-7:
            continue
        a = 0.0
        for x0, x1 in ints:
            a += 0.5 * (erf((x1 - mx) * inv) - erf((x0 - mx) * inv))
        tot += wz * a
    return tot


# ---- griglia per la miscela ritagliata (varianti A e B): celle di 0,1 m
GX0, GNX, GZ0, GNZ, GC = -2.6, 70, 0.6, 40, 0.1


def build_libgrid(e, lett):
    # True = cella VIETATA alla massa.  L1: vietato il solo "libero".  L2: ammessa la sola ombra stimata.
    if lett == 'L1':
        return [[cls(GX0 + (ix + 0.5) * GC, GZ0 + (iz + 0.5) * GC, e) == LIB for ix in range(GNX)] for iz in range(GNZ)]
    return [[cls(GX0 + (ix + 0.5) * GC, GZ0 + (iz + 0.5) * GC, e) != SH for ix in range(GNX)] for iz in range(GNZ)]


def axis_w(m, s, g0, n):
    inv = 1.0 / (s * SQ2)
    out = []
    prev = erf((g0 - m) * inv)
    for i in range(1, n + 1):
        cur = erf((g0 + i * GC - m) * inv)
        out.append(0.5 * (cur - prev))
        prev = cur
    return out


def mixture_cells(libg, comps):
    # comps: lista di (peso, mx, mz, sigma); peso gia' diviso per f.  Ritorna dict cella -> prob (normalizzata)
    cells = {}
    for w, mx, mz, s in comps:
        if w <= 0.0:
            continue
        wx = axis_w(mx, s, GX0, GNX)
        wz = axis_w(mz, s, GZ0, GNZ)
        xs = [(ix, v) for ix, v in enumerate(wx) if v > 1e-6]
        for iz, vz in enumerate(wz):
            if vz <= 1e-6:
                continue
            lrow = libg[iz]
            wv = w * vz
            base = iz * GNX
            for ix, vx in xs:
                if not lrow[ix]:
                    k = base + ix
                    cells[k] = cells.get(k, 0.0) + wv * vx
    tot = sum(cells.values())
    if tot <= 0.0:
        return {}
    for k in cells:
        cells[k] /= tot
    return cells


def region_stats(cells, cellsize, nx, x0, z0, tx, tz):
    # ritorna (sigma_eff, mx, mz, hpd95_set, area95)
    mx = mz = 0.0
    for k, p in cells.items():
        iz, ix = divmod(k, nx)
        mx += p * (x0 + (ix + 0.5) * cellsize)
        mz += p * (z0 + (iz + 0.5) * cellsize)
    vx = vz = 0.0
    for k, p in cells.items():
        iz, ix = divmod(k, nx)
        dx = x0 + (ix + 0.5) * cellsize - mx
        dz = z0 + (iz + 0.5) * cellsize - mz
        vx += p * dx * dx
        vz += p * dz * dz
    se = math.sqrt(0.5 * (vx + vz))
    items = sorted(cells.items(), key=lambda kv: -kv[1])
    acc = 0.0
    s95 = set()
    for k, p in items:
        s95.add(k)
        acc += p
        if acc >= 0.95:
            break
    return se, mx, mz, s95, len(s95) * cellsize * cellsize


def cell_of(x, z, x0, z0, c, nx, nz):
    ix = int(math.floor((x - x0) / c))
    iz = int(math.floor((z - z0) / c))
    if 0 <= ix < nx and 0 <= iz < nz:
        return iz * nx + ix
    return -1


# ---- generatore del vero (non e' il modello dei predittori)
class Truth:
    def __init__(self, rng, beh):
        self.rng = rng
        self.beh = beh
        self.z0 = rng.uniform(2.2, 2.4)
        self.sp = rng.uniform(0.5, 1.4)
        a = math.radians(rng.uniform(-5.0, 5.0))
        self.x, self.z = -1.6, self.z0
        self.vx, self.vz = self.sp * math.cos(a), self.sp * math.sin(a)
        half = KW * self.z0
        self.xtrig = -half + rng.uniform(0.1, 0.9) * 2 * half
        self.done = False
        self.stop_left = 0.0
        self.saved = None
        self.far = False

    def step(self):
        rng = self.rng
        if not self.done and self.beh != 'prosegue' and self.x >= self.xtrig:
            self.done = True
            if self.beh == 'sosta':
                self.saved = (self.vx, self.vz)
                self.vx = self.vz = 0.0
                self.stop_left = rng.uniform(2.0, 6.0)
            elif self.beh == 'ritorno':
                f = rng.uniform(0.8, 1.2)
                self.vx, self.vz = -self.vx * f, -self.vz * f
            elif self.beh == 'lontano':
                a = math.radians(rng.uniform(-20.0, 20.0))
                self.vx, self.vz = self.sp * math.sin(a), self.sp * math.cos(a)
                self.far = True
            elif self.beh == 'passo':
                f = rng.uniform(0.4, 0.7) if rng.random() < 0.5 else rng.uniform(1.4, 1.8)
                self.vx *= f
                self.vz *= f
        if self.stop_left > 0.0:
            self.stop_left -= DT
            if self.stop_left <= 0.0:
                self.vx, self.vz = self.saved
        elif self.far and self.x * self.x + self.z * self.z > 4.4 ** 2:
            pass
        else:
            self.vx += rng.gauss(0.0, 0.02)
            self.vz += rng.gauss(0.0, 0.02)
            self.x += self.vx * DT
            self.z += self.vz * DT


def cov_step(P, a, q=QK):
    # F = [[1, a*dt],[0, a]], Q a rumore bianco d'accelerazione
    p11, p12, p22 = P
    n11 = p11 + 2 * a * DT * p12 + a * a * DT * DT * p22 + q * DT ** 3 / 3
    n12 = a * p12 + a * a * DT * p22 + q * DT * DT / 2
    n22 = a * a * p22 + q * DT
    return (n11, n12, n22)


QOCC = QK   # q delle due ipotesi DURANTE l'occlusione (argomento facoltativo; [dopo])


def run(beh, e, N, seed, lett):
    rng = random.Random(seed)
    rows = build_rows(e) if lett == 'L1' else build_rows_sh(e)
    libg = build_libgrid(e, lett)
    G = 0.40          # fascia della versione corretta
    NP = 300
    CC, CNX, CNZ, CX0, CZ0 = 0.2, 40, 24, -3.4, 0.4   # celle della versione corretta
    L_S, L_M, L_R = 0.30, 0.25, 0.20                  # tassi (1/s): transito->sosta, transito->manovra, sosta->transito
    QC = 0.05
    snv = math.sqrt(QC * DT)
    keys = ['n', 'bordo', 'Kc', 'Kr', 'A1', 'A2', 'A245', 'Ah', 'Aa', 'Ase', 'Amu', 'A08', 'Az', 'Avuota',
            'B1', 'B245', 'Bh', 'Ba', 'Bse', 'Bmu', 'B08', 'Bz', 'Ch', 'Ca', 'C50', 'Clib', 'Clibf',
            'Cpo', 'Cto', 'Cnin', 'Chin', 'Cain', 'Cpo_in', 'Cpo_out']
    st = {k: {kk: 0.0 for kk in keys} for k in CK}
    ase = {k: [] for k in CK}
    pk3 = [0, 0, 0]      # n, A<0.5, B<0.5 (prosegue: ultimo ciclo col vero in ombra)
    pk3b = [0, 0]        # sosta veloce: n, B mu1>0.5 a 3 s
    scart = 0
    tpart = 0.0
    ncyc = 0
    for trial in range(N):
        tr = Truth(rng, beh)
        # --- Kalman prima dell'occlusione
        dets = []
        xs = None
        P = None
        fr = 0
        last = -1
        ok = True
        while True:
            tr.step()
            fr += 1
            if not detectable(tr.x, tr.z):
                break
            if rng.random() < PD:
                zx = tr.x + rng.gauss(0, SIG)
                zz = tr.z + rng.gauss(0, SIG)
                if xs is None:
                    dets.append((fr, zx, zz))
                    if len(dets) == 2:
                        d = (dets[1][0] - dets[0][0]) * DT
                        xs = [zx, zz, (zx - dets[0][1]) / d, (zz - dets[0][2]) / d]
                        R = SIG * SIG
                        P = (R, R / d, 2 * R / (d * d))
                        last = fr
                        nd = 2
                else:
                    for _ in range(fr - last):
                        xs[0] += xs[2] * DT
                        xs[1] += xs[3] * DT
                        P = cov_step(P, 1.0)
                    p11, p12, p22 = P
                    S = p11 + SIG * SIG
                    k1, k2 = p11 / S, p12 / S
                    ix_, iz_ = zx - xs[0], zz - xs[1]
                    xs[0] += k1 * ix_
                    xs[1] += k1 * iz_
                    xs[2] += k2 * ix_
                    xs[3] += k2 * iz_
                    P = ((1 - k1) * p11, (1 - k1) * p12, p22 - k2 * p12)
                    last = fr
                    nd += 1
            if fr > 200:
                ok = False
                break
        if not ok or xs is None or nd < 4:
            scart += 1
            continue
        px0, pz0, vx0, vz0 = xs
        sp0 = math.hypot(vx0, vz0)
        # --- ipotesi della preproposta
        # H2: smorzamento verso il centro della corda dentro l'ombra STIMATA lungo la direzione d'ingresso
        s_in = s_out = None
        if sp0 > 1e-6:
            ux, uz = vx0 / sp0, vz0 / sp0
            s = 0.0
            while s < 4.0:
                c = cls(px0 + s * ux, pz0 + s * uz, e) == SH
                if c and s_in is None:
                    s_in = s
                if s_in is not None and not c:
                    s_out = s
                    break
                s += 0.02
        sc = 0.5 * (s_in + s_out) if (s_in is not None and s_out is not None) else 0.5
        alpha = sc / (sc + sp0 * DT) if sp0 > 1e-6 else 0.9
        m1 = [px0, pz0]
        m2 = [px0, pz0]
        v2 = [vx0, vz0]
        P1 = P
        P2 = P
        muA = [0.8, 0.2]
        muB = [0.8, 0.2]
        f1 = f2 = 1.0
        # --- particelle della versione corretta
        sp_ = math.sqrt(P[0])
        sv_ = math.sqrt(P[2])
        ppx = [px0 + rng.gauss(0, sp_) for _ in range(NP)]
        ppz = [pz0 + rng.gauss(0, sp_) for _ in range(NP)]
        pvx = [vx0 + rng.gauss(0, sv_) for _ in range(NP)]
        pvz = [vz0 + rng.gauss(0, sv_) for _ in range(NP)]
        pmo = [0] * NP
        pw = [1.0 / NP] * NP
        k = 0
        was_in = False
        lastA = lastB = None
        pend = fr - last          # cicli gia' passati senza misura
        while k < CK[-1]:
            k += 1
            if k > pend:
                tr.step()
                if detectable(tr.x, tr.z) and rng.random() < PD:
                    break
            # ---- un ciclo dei predittori
            m1[0] += vx0 * DT
            m1[1] += vz0 * DT
            P1 = cov_step(P1, 1.0, QOCC)
            v2[0] *= alpha
            v2[1] *= alpha
            m2[0] += v2[0] * DT
            m2[1] += v2[1] * DT
            P2 = cov_step(P2, alpha, QOCC)
            s1 = math.sqrt(P1[0])
            s2 = math.sqrt(P2[0])
            if lett == 'L1':
                f1 = max(1e-12, 1.0 - libmass(rows, m1[0], m1[1], s1))
                f2 = max(1e-12, 1.0 - libmass(rows, m2[0], m2[1], s2))
            else:
                f1 = max(1e-12, libmass(rows, m1[0], m1[1], s1))
                f2 = max(1e-12, libmass(rows, m2[0], m2[1], s2))
            a1, a2 = muA[0] * f1, muA[1] * f2
            sa = a1 + a2
            muA = [a1 / sa, a2 / sa] if sa > 0 else [0.5, 0.5]
            b1, b2 = 0.8 * f1, 0.2 * f2
            muB = [b1 / (b1 + b2), b2 / (b1 + b2)]
            # particelle
            t0 = time.perf_counter()
            pS, pM, pR = L_S * DT, L_M * DT, L_R * DT
            sw = 0.0
            rr = rng.random
            gg = rng.gauss
            for i in range(NP):
                mo = pmo[i]
                u = rr()
                if mo == 0:
                    if u < pS:
                        pmo[i] = mo = 1
                    elif u < pS + pM:
                        pmo[i] = mo = 2
                        spd = math.hypot(pvx[i], pvz[i]) * (0.5 + rr())
                        th = 6.283185307179586 * rr()
                        pvx[i] = spd * math.cos(th)
                        pvz[i] = spd * math.sin(th)
                elif mo == 1:
                    if u < pR:
                        pmo[i] = mo = 0
                if mo != 1:
                    pvx[i] += gg(0.0, snv)
                    pvz[i] += gg(0.0, snv)
                    ppx[i] += pvx[i] * DT
                    ppz[i] += pvz[i] * DT
                if neginfo(ppx[i], ppz[i], e, G):
                    pw[i] *= (1.0 - PD)
                sw += pw[i]
            if sw <= 0.0:
                pw = [1.0 / NP] * NP
            else:
                inv = 1.0 / sw
                ess = 0.0
                for i in range(NP):
                    pw[i] *= inv
                    ess += pw[i] * pw[i]
                if 1.0 / ess < NP / 2:
                    u0 = rr() / NP
                    c = pw[0]
                    j = 0
                    nx_, nz_, nvx, nvz, nmo = [], [], [], [], []
                    for i in range(NP):
                        u = u0 + i / NP
                        while u > c and j < NP - 1:
                            j += 1
                            c += pw[j]
                        nx_.append(ppx[j]); nz_.append(ppz[j]); nvx.append(pvx[j]); nvz.append(pvz[j]); nmo.append(pmo[j])
                    ppx, ppz, pvx, pvz, pmo = nx_, nz_, nvx, nvz, nmo
                    pw = [1.0 / NP] * NP
            tpart += time.perf_counter() - t0
            ncyc += 1
            if k <= pend:
                continue
            tx, tz = tr.x, tr.z
            hid = hidden_true(tx, tz)
            if beh == 'prosegue' and tz > ZP and abs(tx) < KW * tz and tx * tx + tz * tz <= RMAX2:
                was_in = True
                lastA, lastB = muA[0], muB[0]
            if k not in st:
                continue
            d = st[k]
            if not hid:
                d['bordo'] += 1
                continue
            d['n'] += 1
            # K: cerchio al 95 % del Kalman non ritagliato
            rK = 2.4477 * s1
            d['Kr'] += rK
            if math.hypot(tx - m1[0], tz - m1[1]) <= rK:
                d['Kc'] += 1
            # A e B
            tc = cell_of(tx, tz, GX0, GZ0, GC, GNX, GNZ)
            for tag, mu in (('A', muA), ('B', muB)):
                cells = mixture_cells(libg, [(mu[0] / f1, m1[0], m1[1], s1), (mu[1] / f2, m2[0], m2[1], s2)])
                if not cells:
                    if tag == 'A':
                        d['Avuota'] += 1
                    continue
                se, mx, mz, s95, ar = region_stats(cells, GC, GNX, GX0, GZ0, tx, tz)
                dist = math.hypot(tx - mx, tz - mz)
                if dist <= se:
                    d[tag + '1'] += 1
                if tag == 'A' and dist <= 2 * se:
                    d['A2'] += 1
                if dist <= 2.4477 * se:
                    d[tag + '245'] += 1
                if tc in s95:
                    d[tag + 'h'] += 1
                d[tag + 'a'] += ar
                d[tag + 'se'] += se
                d[tag + 'mu'] += mu[0]
                if se > 0.8:
                    d[tag + '08'] += 1
                if tc < 0 or cells.get(tc, 0.0) <= 0.0:
                    d[tag + 'z'] += 1
                if tag == 'A':
                    ase[k].append(se)
            # C
            hc = {}
            for i in range(NP):
                c = cell_of(ppx[i], ppz[i], CX0, CZ0, CC, CNX, CNZ)
                hc[c] = hc.get(c, 0.0) + pw[i]
            items = sorted(hc.items(), key=lambda kv: -kv[1])
            acc = 0.0
            s95 = set()
            s50 = set()
            for c, p in items:
                if acc < 0.5:
                    s50.add(c)
                s95.add(c)
                acc += p
                if acc >= 0.95:
                    break
            tcc = cell_of(tx, tz, CX0, CZ0, CC, CNX, CNZ)
            if tcc in s95:
                d['Ch'] += 1
            if tcc in s50:
                d['C50'] += 1
            s95.discard(-1)
            d['Ca'] += len(s95) * CC * CC
            nl = nlf = 0
            for c in s95:
                iz, ix = divmod(c, CNX)
                cx, cz = CX0 + (ix + 0.5) * CC, CZ0 + (iz + 0.5) * CC
                if cls(cx, cz, e) == LIB:
                    nl += 1
                    if neginfo(cx, cz, e, G):
                        nlf += 1
            if s95:
                d['Clib'] += nl / len(s95)
                d['Clibf'] += nlf / len(s95)
            # [dopo] C2: regione al 95 % CONDIZIONATA a "entro la portata" + quota dichiarata "fuori" (non osservato)
            hin = {}
            mout = 0.0
            for i in range(NP):
                if cls(ppx[i], ppz[i], 0.0) == NON:
                    mout += pw[i]
                else:
                    c = cell_of(ppx[i], ppz[i], CX0, CZ0, CC, CNX, CNZ)
                    hin[c] = hin.get(c, 0.0) + pw[i]
            d['Cpo'] += mout
            t_out = cls(tx, tz, 0.0) == NON
            if t_out:
                d['Cto'] += 1
                d['Cpo_out'] += mout
            else:
                d['Cnin'] += 1
                d['Cpo_in'] += mout
                tin = sum(hin.values())
                acc = 0.0
                sin = set()
                for c, p in sorted(hin.items(), key=lambda kv: -kv[1]):
                    sin.add(c)
                    acc += p
                    if acc >= 0.95 * tin:
                        break
                if tcc in sin:
                    d['Chin'] += 1
                d['Cain'] += len(sin) * CC * CC
            if k == 45 and beh == 'sosta' and sp0 >= 1.0:
                pk3b[0] += 1
                if muB[0] > 0.5:
                    pk3b[1] += 1
        if beh == 'prosegue' and was_in:
            pk3[0] += 1
            if lastA < 0.5:
                pk3[1] += 1
            if lastB < 0.5:
                pk3[2] += 1
    # --- stampa
    print(f"comportamento={beh} errore_maschera={e:+.2f} m lettura={lett} q_occlusione={QOCC} N={N} scartati={scart} seme={seed}")
    print(f"particelle: {1e3 * tpart / max(1, ncyc):.2f} ms per ciclo e per traccia ({NP} particelle, Python puro, indicativo)")
    print("tau  n(nasc) bordo | K:cop  raggio | A:cop1s cop2s cop2.45s reg95 area  sig_eff(med) mu1  >0.8m zero vuota | B:cop1s cop2.45s reg95 area sig_eff mu1 >0.8m zero | C:reg95 reg50 area  su_libero oltre_fascia")
    for k in CK:
        d = st[k]
        n = int(d['n'])
        if n == 0:
            print(f"{k * DT:4.2f} n=0 bordo={int(d['bordo'])}")
            continue
        med = sorted(ase[k])[len(ase[k]) // 2] if ase[k] else float('nan')
        nA = max(1.0, n - d['Avuota'])
        print(f"{k * DT:4.2f} {n:6d} {int(d['bordo']):5d} | {d['Kc'] / n:5.3f} {d['Kr'] / n:5.2f} | "
              f"{d['A1'] / n:5.3f} {d['A2'] / n:5.3f} {d['A245'] / n:5.3f} {d['Ah'] / n:5.3f} {d['Aa'] / nA:5.2f} {med:5.2f} {d['Amu'] / nA:5.3f} {d['A08'] / n:5.3f} {d['Az'] / n:5.3f} {int(d['Avuota']):3d} | "
              f"{d['B1'] / n:5.3f} {d['B245'] / n:5.3f} {d['Bh'] / n:5.3f} {d['Ba'] / n:5.2f} {d['Bse'] / n:5.2f} {d['Bmu'] / n:5.3f} {d['B08'] / n:5.3f} {d['Bz'] / n:5.3f} | "
              f"{d['Ch'] / n:5.3f} {d['C50'] / n:5.3f} {d['Ca'] / n:5.2f} {d['Clib'] / n:5.3f} {d['Clibf'] / n:5.3f}")
    if beh == 'prosegue':
        print(f"P-K3: transiti con il vero passato in ombra n={pk3[0]}; mu1<0,5 all'ultimo ciclo in ombra: A {pk3[1]} B {pk3[2]}")
    if beh == 'sosta':
        print(f"P-K3b: soste con velocita' d'ingresso >= 1,0 m/s ancora nascoste a 3 s n={pk3b[0]}; B con mu1>0,5: {pk3b[1]}")
    for k in CK:
        d = st[k]
        print("DATI", beh, f"{e:+.2f}", lett, QOCC, N - scart, k, " ".join(f"{kk}={d[kk]:.6g}" for kk in keys))


if __name__ == '__main__':
    beh = sys.argv[1]
    e = float(sys.argv[2])
    lett = sys.argv[3] if len(sys.argv) > 3 else 'L1'
    N = int(sys.argv[4]) if len(sys.argv) > 4 else 2000
    if len(sys.argv) > 5:
        QOCC = float(sys.argv[5])
    order = ['prosegue', 'sosta', 'ritorno', 'lontano', 'passo']
    seed = 20261114 + 1000 * order.index(beh) + (7 if e != 0.0 else 0)
    t0 = time.time()
    run(beh, e, N, seed, lett)
    print(f"tempo totale {time.time() - t0:.1f} s")
