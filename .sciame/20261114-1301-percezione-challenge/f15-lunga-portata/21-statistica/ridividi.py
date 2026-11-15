"""Rifà 12-traiettorie/prove_traiettorie.py (non modificato) con la sola divisione per MEZZO invece che per scena.
Uso: python -I ridividi.py <f15> <cartella uscita>. Stesso seme. Conto su dati pubblici, nessun sensore fisico."""
import sys, os, re, importlib.util
import numpy as np
F15, OUT = sys.argv[1], sys.argv[2]
spec = importlib.util.spec_from_file_location("prove_traiettorie", os.path.join(F15, "12-traiettorie", "prove_traiettorie.py"))
pt = importlib.util.module_from_spec(spec); sys.modules["prove_traiettorie"] = pt
sys.argv = [sys.argv[0], F15, OUT]
spec.loader.exec_module(pt)

def mezzo(sc):
    for pat, f in [(r"atl_([0-9a-f]{6})$", lambda m: "icao:" + m.group(1)),
                   (r"lhrzrh_TRAIN_\d{4}-\d\d-\d\d_(\w+?)_(avv|dec)$", lambda m: "nvolo:" + m.group(1)),
                   (r"trajair_\d+_(\d+)_\d+$", lambda m: "icao:%06x" % int(m.group(1))),
                   (r"(cmu_m100_volo\d+)$", lambda m: m.group(1)),
                   (r"alfa_(\d{14})", lambda m: "T28:" + m.group(1)),
                   (r"ngsim_us101_v(\d+)_\d+$", lambda m: "veicolo:" + m.group(1)),
                   (r"fi_treno(\d+)_\d+$", lambda m: "treno:" + m.group(1))]:
        m = re.match(pat, sc)
        if m: return f(m)
    return sc

def dividi(sc):
    rng = np.random.default_rng(pt.SEME)
    met = {}
    for cl in sorted({c for c, _, _ in sc}):
        idx = [i for i, x in enumerate(sc) if x[0] == cl]
        g = sorted({mezzo(os.path.basename(sc[i][2])) for i in idx})
        p = rng.permutation(len(g))
        lato = {g[k]: ("taratura" if j < len(g) // 2 else "prova") for j, k in enumerate(p)}
        for i in idx:
            met[sc[i][2]] = lato[mezzo(os.path.basename(sc[i][2]))]
    return met

if __name__ == "__main__":
    import multiprocessing as mp
    mp.set_start_method("fork")
    pt.dividi = dividi
    pt.main()
