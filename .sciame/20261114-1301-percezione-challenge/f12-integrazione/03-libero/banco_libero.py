# banco_libero.py — lo STESSO banco per le candidate del «libero» della cella (K-107, controllo C-D).
# Rifare: vedi rifai.sh. Uscite: risultati_banco.txt (una riga per condizione e regola), riepilogo_banco.txt, banco.json.
# Scene: le 8 di f7-estensione/14-attacco/av10.py (x 2 valori di k = le 16 combinazioni) + il corpo che non rimanda
# segnale di av1.py + una mia (scatola da 10 cm a 2,6-2,9 m). Buchi: modello di 15-verifica/vq3c.c (sparsi per pixel;
# chiazze = blocchi 20 x 20 pixel). Il generatore di scene (render) e' riscritto da me in numpy.
import sys, os, json, time, math, zlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from libero import *

QUI = os.path.dirname(os.path.abspath(__file__))
NF = int(sys.argv[1]) if len(sys.argv) > 1 else 30
FPS = 15.0
REGOLE = ("SC", "RP", "V17", "V18-1", "V18-m", "PR1", "PR2", "PR3", "PR4")
SEME0 = sys.argv[3] if len(sys.argv) > 3 else ""      # "" = i semi del lancio 1; altro testo = semi nuovi
SUFF = ("_" + SEME0) if SEME0 else ""
INF = np.inf

# nome, scatole (x0,x1,y0,y1,z0,z1), stanza, portata, indici che non rimandano segnale, fra le 16?
SCENE = [
    ("stanza vuota", [], True, 6.0, (), True),
    ("barra 1,40-1,50 a 2,0-2,1 m", [(-0.6, 0.6, 2.0, 2.1, 1.40, 1.50)], True, 6.0, (), True),
    ("barra sottile 1,15-1,25", [(-0.6, 0.6, 2.0, 2.1, 1.15, 1.25)], True, 6.0, (), True),
    ("tubo 3 cm a 1,20 m", [(-0.6, 0.6, 2.0, 2.03, 1.20, 1.23)], True, 6.0, (), True),
    ("scatola 0,25 m", [(-0.2, 0.2, 2.0, 2.3, 0.0, 0.25)], True, 6.0, (), True),
    ("scatola 0,10 m", [(-0.2, 0.2, 2.0, 2.3, 0.0, 0.10)], True, 6.0, (), True),
    ("senza fondale, portata 6 m", [], False, 6.0, (), True),
    ("senza fondale, portata 10 m", [], False, 10.0, (), True),
    ("[in piu'] corpo muto 1,75 m a 2 m", [(-0.225, 0.225, 2.0, 2.25, 0.0, 1.75)], True, 6.0, (0,), False),
    ("[in piu'] scatola 0,10 m a 2,6-2,9", [(-0.2, 0.2, 2.6, 2.9, 0.0, 0.10)], True, 6.0, (), False),
]
KS = (0.004, 0.0100)
BUCHI = (("nessuno", 0, 0), ("sparsi 5 %", 0.05, 0), ("sparsi 30 %", 0.30, 0), ("chiazze 5 %", 0, 0.05), ("chiazze 30 %", 0, 0.30))
ERR = (0.0, 0.5, -0.5, 1.0, -1.0)


def slab(o, d, lo, hi):
    with np.errstate(divide="ignore", invalid="ignore"):
        a, b = (lo - o) / d, (hi - o) / d
    t0, t1 = np.minimum(a, b), np.maximum(a, b)
    fermo = np.abs(d) < 1e-12
    dentro = (o >= lo) & (o <= hi)
    return np.where(fermo, np.where(dentro, -INF, INF), t0), np.where(fermo, np.where(dentro, INF, -INF), t1)


def render(cam, scatole, pitch, zmax, stanza):
    """profondita' pulita Z e identita' (-2 suolo, -3 pareti, -1 niente, b = scatola), con l'inclinazione VERA."""
    dx, dy, dz = cam.raggi(pitch)
    with np.errstate(divide="ignore", invalid="ignore"):
        best = np.where(dz < -1e-12, cam.h / -dz, INF)
        ID = np.where(dz < -1e-12, -2, -1)
        if stanza:
            for t in (np.where(dy > 1e-12, 4.0 / dy, INF), np.where(dz > 1e-12, (3.0 - cam.h) / dz, INF),
                      np.where(np.abs(dx) > 1e-12, 3.0 / np.abs(dx), INF)):
                m = t < best
                best, ID = np.where(m, t, best), np.where(m, -3, ID)
    for b, (x0, x1, y0, y1, z0, z1) in enumerate(scatole):
        ax, bx = slab(0.0, dx, x0, x1)
        ay, by = slab(0.0, dy, y0, y1)
        az, bz = slab(cam.h, dz, z0, z1)
        t0, t1 = np.maximum(np.maximum(ax, ay), az), np.minimum(np.minimum(bx, by), bz)
        m = (t0 <= t1) & (t0 > 1e-9) & (t0 < best)
        best, ID = np.where(m, t0, best), np.where(m, b, ID)
    ok = (ID != -1) & (best > 0.05) & (best <= zmax)
    return np.where(ok, best, 0.0), ID


def fotogramma(pulita, ID, k, rng, muti, sparsi, chiazze):
    D = pulita + k * pulita * pulita * rng.standard_normal(pulita.shape)
    D = np.where(pulita > 0, np.maximum(D, 0.02), 0.0)
    for b in muti:
        D[ID == b] = 0.0
    if sparsi > 0:
        D[rng.random(D.shape) < sparsi] = 0.0
    if chiazze > 0:
        H, W = D.shape
        bl = rng.random((H // 20 + 1, W // 20 + 1)) < chiazze
        D[np.kron(bl, np.ones((20, 20), bool))[:H, :W]] = 0.0
    return D


def verita(cam, reg, scatole, pitch):
    """per cella (centro): nel campo vero, profondita' dentro un corpo appoggiato, suolo visibile, base dell'ostacolo sospeso."""
    x, y = reg.cx, reg.cy
    _, _, _, infov = cam.proietta(x, y, 0.0, pitch)
    dn = np.full(x.shape, -INF)
    vis = np.ones(x.shape, bool)
    sotto = np.full(x.shape, INF)
    for (x0, x1, y0, y1, z0, z1) in scatole:
        inpianta = np.minimum(np.minimum(x - x0, x1 - x), np.minimum(y - y0, y1 - y))
        if z0 <= 0:
            dn = np.maximum(dn, inpianta)
        else:
            sotto = np.where(inpianta >= 0, np.minimum(sotto, z0), sotto)
        ax, bx = slab(0.0, x, x0, x1)
        ay, by = slab(0.0, y, y0, y1)
        az, bz = slab(cam.h, np.full(x.shape, -cam.h), z0, z1)
        t0, t1 = np.maximum(np.maximum(ax, ay), az), np.minimum(np.minimum(bx, by), bz)
        vis &= ~((t0 <= t1) & (t0 < 1 - 1e-6) & (t1 > 1e-9))
    return infov, dn, vis, sotto


def main():
    cam = camera_ideale()
    righe, rec = [], []
    t_inizio = time.time()
    for k in KS:
        reg = Regole(cam, k)
        for (nome, scatole, stanza, zmax, muti, sedici) in SCENE:
            for e in ERR:
                pulita, ID = render(cam, scatole, 15.0 + e, zmax, stanza)
                infov, dn, vis, sotto = verita(cam, reg, scatole, 15.0 + e)
                vero = infov & (dn <= 0) & vis
                aperti = settori_aperti(vero)
                for (bn, sp, ch) in BUCHI:
                    seme = zlib.crc32(("%s|%g|%g|%s%s" % (nome, k, e, bn, SEME0)).encode())
                    rng = np.random.default_rng(seme)
                    acc = {r: dict(lib=0, dentro=0, prof=0, nasc=0, qv=0, sottosp=0, cambi=0, fot_viol=0, sett=[]) for r in REGOLE}
                    prec = None
                    for f in range(NF):
                        D = fotogramma(pulita, ID, k, rng, muti, sp, ch)
                        out, qv, occ, omb = reg.tutte(D)
                        for r in REGOLE:
                            L, a = out[r], acc[r]
                            a["lib"] += int((L & vero).sum())
                            nd, npf = int((L & (dn > 0)).sum()), int((L & (dn > 0.05)).sum())
                            nn = int((L & infov & (dn <= 0) & ~vis).sum())
                            nq = int((L & (qv >= sotto)).sum()) if r == "V17" else 0
                            a["dentro"] += nd; a["prof"] += npf; a["nasc"] += nn; a["qv"] += nq
                            a["sottosp"] += int((L & np.isfinite(sotto)).sum())
                            a["fot_viol"] += 1 if (nd + nn + nq) else 0
                            a["sett"] += settori(L, aperti)
                            if prec is not None:
                                a["cambi"] += int(((L != prec[r]) & vero).sum())
                        prec = out
                    nv = int(vero.sum())
                    for r in REGOLE:
                        a = acc[r]
                        med = float(np.median(a["sett"])) if a["sett"] else float("nan")
                        scon = 100.0 * sum(1 for v in a["sett"] if v <= 1.3 + 1e-9) / len(a["sett"]) if a["sett"] else float("nan")
                        d = dict(k=k, scena=nome, sedici=sedici, err=e, buchi=bn, regola=r, celle_vere=nv, resa=100.0 * a["lib"] / (nv * NF),
                                 dentro=a["dentro"], profonde=a["prof"], nascoste=a["nasc"], qv=a["qv"], sotto_sospeso=a["sottosp"],
                                 fot_viol=a["fot_viol"], cambi_s=FPS * a["cambi"] / (nv * (NF - 1)), settori=len(aperti), mediana_m=med, sconosciuto=scon)
                        rec.append(d)
                        righe.append("k=%.4f | %-34s | err %+4.1f | %-12s | %-5s | resa %5.1f %% | dentro %4d (prof %4d) nasc %4d qv %3d | fot. con violazione %2d/%d | cambi %.2f /s | settori %2d mediana %.1f m, «sconosciuto» %5.1f %% | libere sotto il sospeso %d"
                                     % (k, nome, e, bn, r, d["resa"], d["dentro"], d["profonde"], d["nascoste"], d["qv"], d["fot_viol"], NF, d["cambi_s"], d["settori"], med, scon, d["sotto_sospeso"]))
    with open(os.path.join(QUI, "risultati_banco%s.txt" % SUFF), "w") as f:
        f.write("# banco_libero.py, NF = %d fotogrammi per condizione, %d condizioni x %d regole, %.0f s\n" % (NF, len(rec) // len(REGOLE), len(REGOLE), time.time() - t_inizio))
        f.write("\n".join(righe) + "\n")
    with open(os.path.join(QUI, "banco%s.json" % SUFF), "w") as f:
        json.dump(dict(NF=NF, righe=rec), f)
    print("condizioni %d, fotogrammi %d, %.0f s" % (len(rec) // len(REGOLE), len(rec) // len(REGOLE) * NF, time.time() - t_inizio))


def tempi():
    """tempo per fotogramma, un filo: stanza vuota, 5 % di buchi sparsi, 300 fotogrammi; mediana e 95-esimo percentile."""
    cam = camera_ideale()
    reg = Regole(cam, 0.004)
    pulita, ID = render(cam, [], 15.0, 6.0, True)
    rng = np.random.default_rng(7)
    T = {n: [] for n in ("griglia", "3x3", "leggi_1_quota", "impronta", "SC o RP", "V17", "V18", "PR4", "tutte le 9")}
    pc = time.perf_counter
    for f in range(300):
        D = fotogramma(pulita, ID, 0.004, rng, (), 0.05, 0)
        t0 = pc(); occ, r0, omb = reg.griglia(D); t1 = pc(); p3 = reg.prep3(D); t2 = pc()
        L = reg.leggi(p3, 0.2) == LIB; t3 = pc(); cnt = reg.impronta(D); t4 = pc()
        for q in QS[1:]:
            reg.leggi(p3, q)
        t5 = pc()
        g, p, l, i = t1 - t0, t2 - t1, t3 - t2, t4 - t3
        T["griglia"].append(g); T["3x3"].append(p); T["leggi_1_quota"].append(l); T["impronta"].append(i)
        T["SC o RP"].append(p + l); T["V17"].append(g + p + l + (t5 - t4)); T["V18"].append(g + i)
        t6 = pc(); vm = ~occ & ~omb & (cnt >= reg.fp_meta); pr4 = vm & ~vicine((reg.fp_tot > 0) & ~vm, False); t7 = pc()
        reg.tutte(D); t8 = pc()
        T["PR4"].append(g + i + (t7 - t6)); T["tutte le 9"].append(t8 - t7)
    out = ["# tempo per fotogramma 320 x 240, Python con numpy, un filo; mediana e p95 su 300 fotogrammi (ms)"]
    for n, v in T.items():
        v = 1000 * np.array(v[20:])
        out.append("%-14s mediana %.3f ms  p95 %.3f ms  massimo %.3f ms" % (n, np.median(v), np.percentile(v, 95), v.max()))
    open(os.path.join(QUI, "tempi.txt"), "w").write("\n".join(out) + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[2] == "tempi":
        tempi()
    else:
        main()
