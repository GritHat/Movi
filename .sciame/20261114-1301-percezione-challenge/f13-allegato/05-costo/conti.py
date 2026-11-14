# conti.py — ricalcolo delle cifre del fascicolo «rappresentazioni dello spazio e costo di calcolo».
# Solo lettura dei file d'origine; nessun codice altrui eseguito. Uso (dalla cartella del fascicolo):
#   <interprete di f10> -I -B conti.py > uscite/conti.txt
import glob, json, math, os, re, sys
import numpy as np

QUI = os.path.dirname(os.path.abspath(__file__))
RAD = os.path.normpath(os.path.join(QUI, "..", ".."))            # cartella della convocazione
F7 = os.path.join(RAD, "f7-estensione"); F8 = os.path.join(RAD, "f8-continuita"); F10 = os.path.join(RAD, "f10-dati")

def wilson(k, n, z=1.959964):
    if n == 0: return (float("nan"),) * 2
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0.0, c - h), min(1.0, c + h)
def W(k, n): a, b = wilson(k, n); return f"{k}/{n} = {100*k/n:.2f} %  Wilson 95 % [{100*a:.2f}; {100*b:.2f}] %"

print("== A. Geometria e numerosita' ==")
Lx, Ly, Lz = 6.0, 3.0, 4.0     # larghezza, quota, profondita' (m): regione 6 x 4 x 3 m
for s in (0.10, 0.05):
    n = [round(L / s) for L in (6.0, 4.0, 3.0)]; N = n[0] * n[1] * n[2]
    print(f"lato {s*100:.0f} cm: {n[0]} x {n[1]} x {n[2]} = {N} voxel; 4 B: {4*N} B = {4*N/1e6:.3f} MB; 8 B: {8*N} B = {8*N/1e6:.3f} MB; "
          f"somma n_i = {sum(n)} (tetto dei passi per raggio); blocchi 8^3: {math.ceil(n[0]/8)*math.ceil(n[1]/8)*math.ceil(n[2]/8)}")
print("griglia polare: 87 colonne da 1 grado x 30 anelli da 0,1 m =", 87 * 30, "celle (3 m);", 87 * 60, "(6 m)")
print("due fotogrammi 640x480 a 4 B:", 2 * 640 * 480 * 4, "B; tre:", 3 * 640 * 480 * 4, "B")
h, th, fh, fv = 1.2, math.radians(15), math.radians(87), math.radians(58)
f_px = 320 / math.tan(fh / 2)
print(f"focale a 640 px e 87 gradi: f = {f_px:.1f} px; passo ammesso k <= s f / Zmax: 5 cm, 6 m -> {0.05*f_px/6:.2f}; 10 cm -> {0.10*f_px/6:.2f}")
t_alto = math.tan(fv / 2 - th); t_basso = math.tan(fv / 2 + th)
print(f"bordo alto del campo: y = {h} + {t_alto:.4f} z; quota 1,8 m a z = {(1.8-h)/t_alto:.2f} m; quota 2,0 m a z = {(2.0-h)/t_alto:.2f} m")
print(f"suolo visibile da z = h / tan(theta + FOV_v/2) = {h/t_basso:.3f} m; quota 0,15 m fuori campo sotto z = {(h-0.15)/t_basso:.3f} m")
Vp = (4 / 3) * math.tan(fh / 2) * math.tan(fv / 2) * 3.0 ** 3
print(f"piramide vista fino a 3 m: {Vp:.2f} m^3 = {100*Vp/72:.1f} % di 72 m^3; rapporto 72 / V = {72/Vp:.2f}; voxel 10 cm {Vp/1e-3:.0f}, 5 cm {Vp/1.25e-4:.0f}")
print(f"periodo a 15 Hz: {1000/15:.2f} ms; 10 % = {100/15:.2f} ms; spostamento a 1,4 m/s in un periodo: {1.4/15*100:.1f} cm")
print(f"errore d'assetto: 1 grado a 3 m = {3*math.tan(math.radians(1))*100:.1f} cm; 0,5 gradi a 6 m = {6*math.tan(math.radians(0.5))*100:.1f} cm")
print(f"mezza cella (0,05 m) su due intervalli (2/15 s): {0.05/(2/15):.3f} m/s; regione 20x20x5 m a 5 cm: {400*400*100} voxel, {400*400*100*8/1e6:.0f} MB a 8 B")
lh, lm = math.log(0.7 / 0.3), math.log(0.4 / 0.6); lmin, lmax = math.log(0.1192 / 0.8808), math.log(0.971 / 0.029)
n = 0; l = lmin
while l <= 0: l += lh; n += 1
print(f"log-odds: colpo {lh:+.3f}, mancato {lm:+.3f}, saturazione [{lmin:.3f}; {lmax:.3f}]; da saturo libero servono {n} colpi ({n/15:.2f} s a 15 Hz); "
      f"da saturo occupato servono {math.ceil(lmax/-lm)} mancati ({math.ceil(lmax/-lm)/15:.2f} s)")

def leggi_rep(p):
    R = []
    for r in open(p, encoding="utf-8", errors="replace"):
        if not r.startswith("rep="): continue
        d = {}
        for kv in r.split():
            if "=" not in kv: continue
            k, v = kv.split("=", 1)
            try: d[k] = float(v)
            except ValueError: d[k] = v
        d["nome"] = d["rep"] + (str(int(d["fasce"])) if "fasce" in d else "") + (f"_{int(d['portata'])}m" if "portata" in d else "")
        R.append(d)
    return R
def cerca(R, nome, scena, res, passo):
    for d in R:
        if d["nome"] == nome and d["scena"] == scena and d["res_cm"] == res and d["passo"] == passo: return d
def rapporti(R, a, b):
    v = []
    for d in R:
        if d["nome"] != a: continue
        e = cerca(R, b, d["scena"], d["res_cm"], d["passo"])
        if e: v.append(d["agg_media_ms"] / e["agg_media_ms"])
    return v
def riga(d): return f"{d['agg_media_ms']:.2f} / {d['agg_p95_ms']:.2f} / {d['agg_max_ms']:.2f}" if d else "--"

print("\n== B. Banco delle strutture: file d'origine (nucleo veloce, nucleo lento) e rilancio in questa cartella ==")
ORI = leggi_rep(os.path.join(F7, "12-prestazioni", "risultati.txt"))
COL = leggi_rep(os.path.join(F7, "12-prestazioni", "risultati_colbit.txt"))
LEN = leggi_rep(os.path.join(F7, "12-prestazioni", "risultati_core_lento.txt"))
MIO = leggi_rep(os.path.join(QUI, "uscite", "strutture_breve_core2.txt")) if os.path.exists(os.path.join(QUI, "uscite", "strutture_breve_core2.txt")) else []
for nome, lab in (("hash8", "hash/densa"), ("octree", "octree/densa"), ("octree_pot", "octree potato/densa")):
    v = rapporti(ORI, nome, "densa"); print(f"origine  {lab}: N = {len(v)} configurazioni; min {min(v):.2f}, max {max(v):.2f}")
    if MIO: v = rapporti(MIO, nome, "densa"); print(f"rilancio {lab}: N = {len(v)}; min {min(v):.2f}, max {max(v):.2f}")
v = [d["agg_media_ms"] / cerca(ORI, "densa", d["scena"], d["res_cm"], d["passo"])["agg_media_ms"] for d in COL if cerca(ORI, "densa", d["scena"], d["res_cm"], d["passo"])]
print(f"origine  colonne di bit/densa: N = {len(v)}; min {min(v):.2f}, max {max(v):.2f}")
v = [d["agg_media_ms"] / e["agg_media_ms"] for d in LEN for e in [cerca(ORI, d["nome"], d["scena"], d["res_cm"], d["passo"])] if e]
print(f"nucleo lento / nucleo veloce (medie): N = {len(v)}; mediana {np.median(v):.2f}")
print("memoria (B), tutti i raggi: densa, hash vuota, hash densa, octree vuota, octree densa; risparmio massimo dell'hash")
for res in (10, 5):
    de = cerca(ORI, "densa", "densa", res, 1)["mem_B"]; hv = cerca(ORI, "hash8", "vuota", res, 1)["mem_B"]; hd = cerca(ORI, "hash8", "densa", res, 1)["mem_B"]
    ov = cerca(ORI, "octree", "vuota", res, 1)["mem_B"]; od = cerca(ORI, "octree", "densa", res, 1)["mem_B"]
    print(f"  {res} cm: {de:.0f}; {hv:.0f} ({100*hv/de:.0f} %); {hd:.0f} ({100*hd/de:.0f} %); {ov:.0f} ({100*ov/de:.0f} %); {od:.0f} ({100*od/de:.0f} %); "
          f"densa - hash vuota = {(de-hv)/1e6:.2f} MB; blocchi {cerca(ORI,'hash8','vuota',res,1)['unita']:.0f} e {cerca(ORI,'hash8','densa',res,1)['unita']:.0f}")
print("polare 3 m:", cerca(ORI, "polare_3m", "densa", 10, 4)["mem_B"], "B; immagine:", cerca(ORI, "immagine", "densa", 10, 4)["mem_B"], "B")
print("aggiornamento, scena densa, ms media / p95 / massimo  [origine veloce | origine lento | rilancio]")
for nome in ("polare_3m", "immagine", "colonne_bit", "fasce3", "densa", "hash8", "octree"):
    for res in (10, 5):
        for passo in (4, 1):
            o = cerca(COL if nome == "colonne_bit" else ORI, nome, "densa", res, passo); l = cerca(LEN, nome, "densa", res, passo); m = cerca(MIO, nome, "densa", res, passo)
            print(f"  {nome:12s} {res:2d} cm passo {passo}: {riga(o)} | {riga(l)} | {riga(m)}")
tutti = [d["agg_p95_ms"] for d in ORI if d["nome"] == "polare_3m"] + [d["agg_media_ms"] for d in ORI if d["nome"] == "polare_3m"]
print(f"polare 3 m, tutte le configurazioni d'origine: media min {min(d['agg_media_ms'] for d in ORI if d['nome']=='polare_3m'):.3f}, p95 max {max(d['agg_p95_ms'] for d in ORI if d['nome']=='polare_3m'):.3f} ms")
for res in (10, 5):
    for passo in (4, 1):
        d = cerca(ORI, "densa", "densa", res, passo)
        print(f"  densa {res} cm passo {passo}: raggi {d['raggi_f']:.0f}, passi {d['passi_f']:.0f}, passi/raggio {d['passi_f']/d['raggi_f']:.1f}, ns/passo {d['ns_passo']:.2f}")
d = cerca(ORI, "immagine", "densa", 10, 4)
print(f"interrogazione nell'immagine: {d['int_media_us']:.0f} us per 108000 punti = {d['int_media_us']*1000/108000:.2f} ns a punto; 1000 punti = {d['int_media_us']/108:.1f} us")
p = os.path.join(F7, "12-prestazioni", "risultati_python.txt"); print("Python puro (origine):", " | ".join(x.strip() for x in open(p, encoding="utf-8").read().splitlines()[1:]))
p = os.path.join(QUI, "uscite", "strutture_py_puro.txt")
if os.path.exists(p): print("Python puro (rilancio):", " | ".join(x.strip() for x in open(p, encoding="utf-8").read().splitlines()[1:]))

print("\n== C. Sicurezza: conteggi dai file d'origine, con frequenze e intervalli ==")
def testo(*p): return open(os.path.join(*p), encoding="utf-8", errors="replace").read()
T = lambda n: testo(F7, "11-torneo", f"risultati_{n}.txt")
m = re.search(r"liberi (\d+), di cui falsi (\d+)", T("statica")); print("lettura a due stati (non allocato = libero):", W(int(m[2]), int(m[1])), "(punti di una scena: non campioni indipendenti)")
m = re.search(r"decadimento verso il libero\s+fotogrammi con un voxel del corpo «libero»: (\d+)", T("a2").split("variante 1")[1]); print("decadimento verso il libero:", W(int(m[1]), 897), "(fotogrammi)")
m = re.search(r"tetto 100 %.*?meno recente: voxel di possibile presenza scritti (\d+), persi (\d+).*?nascosto (\d+), fuori regione (\d+)", T("a3")); print("blocchi a memoria limitata: voxel persi", W(int(m[2]), int(m[1])), "; fotogrammi fuori regione", W(int(m[4]), int(m[3])))
print("sensore coperto, «attraversato = libero» (VO):", re.search(r"VO\s+(\d+)", T("a9").split("tutto non valido")[1])[1], "punti liberi al fotogramma 29, e ai successivi:", re.findall(r"\d+ \(", T("a9").split("tutto non valido")[1].split("VO ")[1].split("\n")[0]))
m = re.search(r"tetto 300 blocchi: mediana ([\d.]+) ms, p95 ([\d.]+), massimo ([\d.]+)", T("a10")); print("tetto a 300 blocchi (ms): mediana, p95, massimo =", m[1], m[2], m[3])
for r in T("scenB").splitlines():
    c = r.split()
    if c and c[0] in ("Q1", "Q3c", "VO", "VOa", "S10(B+M)", "N1-suolo"): print(f"  scena con ostacolo (147 fotogrammi) {c[0]:9s} fotogrammi con falso profondo {c[3]:>4s}; resa {c[10]} %; ms mediana/max {c[11]}/{c[12]}")
for r in T("a5c").splitlines():
    c = r.split()
    if c and c[0] in ("Q1", "Q3", "Q3c", "N1-suolo", "VOa"): print(f"  soggetto senza ritorno (87 fotogrammi) {c[0]:9s} fot. con falso profondo {c[3]:>3s}; punti falsi {c[4]}, profondi {c[7]}")
k = T("k106").split("## K-106")[2]
for r in k.splitlines():
    m = re.search(r"sparsi\s+(\d+) %, a chiazze\s+(\d+) %: Q1 ([\d.]+) % ; Q3 ([\d.]+) % ; Q3c ([\d.]+) % ; P ([\d.]+) % ; S10 ([\d.]+) %", r)
    if m: print(f"  resa con buchi sparsi {m[1]} %, chiazze {m[2]} %: lettura a un fotogramma {m[3]} %, a tre con clausola {m[5]} %, fasce {m[7]} %")
s10 = T("s10"); m = re.search(r"scena 3.*?\n.*?S10\(B\+M\) (\d+) ;.*?N1 (\d+)", s10); print("tre fasce, scatola di 10 cm: celle libere con l'oggetto nella colonna:", m[1], "(griglia polare:", m[2] + ")")
m = re.search(r"scena 0.*?S10\(B\+M\+A\) (\d+) ; S10\(B\+M\) (\d+)", s10); print("tre fasce, stanza vuota: celle libere su 2610 con la fascia alta", m[1], "; senza", m[2])
sic = testo(F7, "06-tempo-reale", "risultati_sicurezza.txt").split("scena=tipica lato_cm=5 k=4")[1].split("scena=")[0]
rif3 = 6648
for et, lab in (("a ", "somma dei log-odds senza priorita'"), ("c ", "decimazione 4x4"), ("b ", "priorita' al colpo"), ("e3", "colpi pieni + blocchi, 3 sigma"), ("p ", "proiezione")):
    m = re.search(r"\n\s+" + re.escape(et) + r".*?su rif\.3=\s*(\d+)", sic); x = int(m[1]) / 12
    print(f"  {lab:36s}: {x:8.1f} falsi liberi per fotogramma su {rif3} voxel con superficie sopra 0,10 m = {100*x/rif3:.2f} %")
vec = testo(F7, "06-tempo-reale", "risultati_vecchi.txt").split("mappa=che integra")[1]
m = re.search(r"f=74\s+dentro=\s*(\d+)\s+L=\s*(\d+)\s+M3=\s*(\d+)\s+M1=\s*(\d+)", vec); print("log-odds letto come stato corrente, 14 fotogrammi dopo la comparsa:", W(int(m[2]), int(m[1])), "; lettura del fotogramma corrente:", m[4])
m60 = re.search(r"f=60\s+dentro=\s*(\d+)\s+L=\s*(\d+)\s+M3=\s*(\d+)\s+M1=\s*(\d+)\s+M3c=\s*(\d+)", vec); print("  finestra di 3 fotogrammi al fotogramma della comparsa:", m60[3], "; con clausola di contraddizione:", m60[5])
def vq(p):
    t = open(p, encoding="utf-8", errors="replace").read(); cond = t.split("\n## ")[1:]; out = []
    for c in cond:
        nome = c.split("\n")[0]; r = {}
        for q in ("Q1", "Q3", "Q3c"):
            m = re.search(r"\n\s+" + q + r"\s+F\s+(\d+) su (\d+) ; prof\s+(\d+) ; bordo\s+(\d+) ; resa\s+([\d.]+) %", c)
            if m: r[q] = (int(m[1]), int(m[2]), int(m[3]), int(m[4]), float(m[5]))
        if r: out.append((nome, r))
    return out
for et, p in (("origine", os.path.join(F7, "15-verifica", "risultati_vq3c.txt")), ("rilancio", os.path.join(QUI, "uscite", "lettura_vq3c.txt"))):
    if not os.path.exists(p): continue
    V = vq(p); nf = sum(r["Q3c"][1] for _, r in V if "Q3c" in r); kf = sum(r["Q3c"][0] for _, r in V if "Q3c" in r)
    print(f"lettura del punto, secondo programma ({et}): condizioni {len(V)}; fotogrammi con un punto profondo dato per libero: Q3c {W(kf, nf)}; "
          f"Q1 {sum(r['Q1'][0] for _, r in V)}/{sum(r['Q1'][1] for _, r in V)}; Q3 {sum(r['Q3'][0] for _, r in V)}/{sum(r['Q3'][1] for _, r in V)}; bordo massimo Q3c {max(r['Q3c'][3] for _, r in V)}")
    for nome, r in V: print(f"    {nome[:60]:60s} resa Q1 {r['Q1'][4]:5.1f} %  Q3c {r['Q3c'][4]:5.1f} %  falsi profondi Q3 {r['Q3'][2]}")

print("\n== D. Previsione durante l'occlusione: tempi per ciclo ==")
for p in (os.path.join(F8, "14-attacco", "ris", "tempo_C.txt"), os.path.join(F8, "14-attacco", "ris", "tempo_py.txt"), os.path.join(QUI, "uscite", "previsione_C.txt"), os.path.join(QUI, "uscite", "previsione_py.txt")):
    if not os.path.exists(p): continue
    print(" ", os.path.relpath(p, RAD))
    for r in open(p, encoding="utf-8", errors="replace"):
        m = re.search(r"tracce=(\d+).*?mediana=([\d.]+) ms p95=([\d.]+) ms max=([\d.]+)", r)
        if m: print(f"    tracce {m[1]:>3s}: mediana {m[2]} ms, p95 {m[3]} ms, massimo {m[4]} ms; p95 per traccia {float(m[3])/int(m[1]):.3f} ms; p95 / periodo = {100*float(m[3])/(1000/15):.1f} %")
for r in open(os.path.join(F8, "13-soluzione", "ris", "tempi.txt"), encoding="utf-8"):
    if "\t10\t" in r and ("C-004" in r or "sd-1" in r): print("    seconda implementazione, 10 tracce:", r.strip().replace("\t", " | "))

print("\n== E. Catena di riferimento (Python con numpy): tempi per ciclo dai record per fotogramma ==")
for et in ("sim", "sim_p40"):
    base = os.path.join(F10, "20-validazione", "uscite", et); t = []; nt = []; ng = []; per = {}
    for d in sorted(glob.glob(os.path.join(base, "*", "fotogrammi.jsonl"))):
        seq = os.path.basename(os.path.dirname(d)); a = []
        for r in open(d, encoding="utf-8"):
            j = json.loads(r); a.append(j["tempo_ciclo_ms"]); nt.append(len(j["tracce"])); ng.append(len(j.get("gruppi", [])))
        t += a; per[seq] = (np.mean(a), len(a), max(a))
    t = np.array(t); nt = np.array(nt); ng = np.array(ng)
    print(f"  [{et}] simulata 424x240: sequenze {len(per)}, cicli N = {len(t)}; media {t.mean():.2f} ms, mediana {np.median(t):.2f}, p95 {np.percentile(t,95):.2f}, p99 {np.percentile(t,99):.2f}, massimo {t.max():.2f}")
    k = int((t > 66).sum()); k2 = int((t > 1000 / 15).sum()); print(f"  cicli oltre 66 ms: {W(k, len(t))}; oltre 66,67 ms: {k2}")
    print(f"  tracce presenti nel ciclo: min {nt.min()}, mediana {np.median(nt):.0f}, max {nt.max()}; correlazione di Pearson tempo-tracce {np.corrcoef(t, nt)[0,1]:.2f}; tempo-gruppi {np.corrcoef(t, ng)[0,1]:.2f}")
    for lo, hi in ((0, 2), (3, 5), (6, 10), (11, 20), (21, 40), (41, 80), (81, 10**6)):
        s = (nt >= lo) & (nt <= hi)
        if s.sum(): print(f"    tracce {lo:>3d}-{hi if hi < 10**6 else 'oltre':>5}: N = {int(s.sum()):5d} cicli; media {t[s].mean():6.2f} ms; p95 {np.percentile(t[s],95):6.2f}; massimo {t[s].max():6.2f}")
    A = np.vstack([np.ones_like(nt, dtype=float), nt, nt.astype(float) ** 2]).T; c, *_ = np.linalg.lstsq(A, t, rcond=None)
    print(f"  minimi quadrati t = a + b n + c n^2: a = {c[0]:.2f} ms, b = {c[1]:.3f} ms/traccia, c = {c[2]:.5f} ms/traccia^2")
    peggio = max(per.items(), key=lambda kv: kv[1][0]); print(f"  sequenza con la media piu' alta: {peggio[0]} ({peggio[1][0]:.2f} ms su {peggio[1][1]} cicli)")
rp = os.path.join(F10, "20-validazione", "uscite", "vere", "RIEPILOGO.jsonl")
src = rp if os.path.exists(rp) else os.path.join(F10, "20-validazione", "uscite", "vere", "RIEPILOGO.txt")
for r in open(src, encoding="utf-8"):
    try: j = json.loads(r)
    except Exception: continue
    if "tempo_ciclo_ms" in j and (j["sequenza"].startswith("depthtrack") or j["variante"] in ("nucleo", "posa_per_fotogramma")):
        tc = j["tempo_ciclo_ms"]; print(f"  pubblica {j['sequenza']} [{j['variante']}], {j['pixel']} pixel, {j['fotogrammi']} cicli in {j['durata_s']} s: media {tc['media']} ms, p95 {tc['p95']}, massimo {tc['massimo']}; tracce confermate {j['tracce_confermate']}")
d = os.path.join(F10, "20-validazione", "uscite", "vere", "depthtrack_human02_indoor__nucleo", "fotogrammi.jsonl")
if os.path.exists(d):
    n = [len(json.loads(r)["tracce"]) for r in open(d, encoding="utf-8")]; g = [len(json.loads(r).get("gruppi", [])) for r in open(d, encoding="utf-8")]
    print(f"  registrazione affollata: tracce presenti insieme nel ciclo: mediana {np.median(n):.0f}, massimo {max(n)}; gruppi per ciclo: mediana {np.median(g):.0f}, massimo {max(g)} (N = {len(n)} cicli)")

print("\n== F. Controlli aggiunti ==")
print("primo programma, lettura del fotogramma corrente: fotogrammi con falso profondo", W(0, 147 + 87 + 87))
for dist in ("1.5", "2.0"):
    b = T("a8").split(f"a {dist} m")[1]; m = re.search(r"Q1\s+(\d+) su (\d+)", b); m3 = re.search(r"Q3c\s+(\d+) su (\d+)", b)
    print(f"vetro a {dist} m: punti della lastra dati per liberi: un fotogramma {m[1]}/{m[2]}, con conferma {m3[1]}/{m3[2]} = {100*int(m3[1])/int(m3[2]):.1f} %")
m = re.search(r"\nQ3c\s+(\d+) \(\s*(\d+)\)\s+(\d+) \(\s*(\d+)\)", T("a6")); print(f"errore d'imbardata di 1 grado non segnalato: falsi liberi prima {m[1]}, dopo {m[3]} (profondi {m[4]})")
print(f"latenza, somma dei soli contributi noti: 33/2 + 95 + 22 + 21,3 = {33/2 + 95 + 22 + 1024/48000*1000:.1f} ms (un quanto audio = {1024/48000*1000:.1f} ms)")
if MIO:
    v = []
    for d in MIO:
        o = cerca(COL if d["nome"] == "colonne_bit" else ORI, d["nome"], d["scena"], d["res_cm"], d["passo"])
        if o and o["agg_media_ms"] >= 1.0: v.append(d["agg_media_ms"] / o["agg_media_ms"])
    print(f"rilancio / origine sulle medie (configurazioni con media >= 1 ms): N = {len(v)}; min {min(v):.2f}, mediana {np.median(v):.2f}, max {max(v):.2f}")
    print(f"p95 peggiore a un raggio su 16, origine: {max(d['agg_p95_ms'] for d in ORI if d['passo']==4):.1f} ms; nucleo lento: {max(d['agg_p95_ms'] for d in LEN if d['passo']==4):.1f} ms; rilancio: {max(d['agg_p95_ms'] for d in MIO if d['passo']==4):.1f} ms")
def campi(p):
    out = {}
    for r in open(p, encoding="utf-8", errors="replace"):
        c = r.split()
        if len(c) >= 13 and c[1].isdigit() and c[2].isdigit(): out.setdefault(c[0], []).append(tuple(c[1:11]))
    return out
for n in ("statica", "scenB", "a5c"):
    p = os.path.join(QUI, "uscite", f"torneo_{n}.txt")
    if os.path.exists(p): print(f"rilancio del primo programma, prova {n}: conteggi (tempi esclusi) identici all'origine:", campi(p) == campi(os.path.join(F7, "11-torneo", f"risultati_{n}.txt")))
for n in ("s10", "a2", "a3", "a9", "k106"):
    p = os.path.join(QUI, "uscite", f"torneo_{n}.txt")
    if os.path.exists(p): print(f"rilancio del primo programma, prova {n}: uscita identica all'origine:", open(p, encoding="utf-8", errors="replace").read() == T(n))
p = os.path.join(QUI, "uscite", "lettura_vq3c.txt")
if os.path.exists(p): print("rilancio del secondo programma: uscita identica all'origine:", open(p, encoding="utf-8", errors="replace").read() == testo(F7, "15-verifica", "risultati_vq3c.txt"))
for n, o in (("sicurezza_tipica_5_4.txt", "risultati_sicurezza.txt"), ("vecchi_5_Q.txt", "risultati_vecchi.txt")):
    p = os.path.join(QUI, "uscite", n)
    if os.path.exists(p):
        a = [r for r in open(p, encoding="utf-8", errors="replace") if r.startswith("  ")]; b = [r for r in open(os.path.join(F7, "06-tempo-reale", o), encoding="utf-8", errors="replace") if r.startswith("  ")]
        print(f"rilancio {n}: {len(a)} righe di conteggio; tutte presenti nell'origine: {all(r in b for r in a)}")
p = os.path.join(QUI, "uscite", "torneo_a10.txt")
if os.path.exists(p): print("rilancio, tempi della prova di carico:", " | ".join(r.strip() for r in open(p, encoding="utf-8", errors="replace") if "VH" in r or "rip. 0" in r)[:900])
