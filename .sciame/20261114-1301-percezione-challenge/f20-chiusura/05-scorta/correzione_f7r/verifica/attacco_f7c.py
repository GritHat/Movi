# Attacco: F7c (nessun urto) con radar saturato 1 s per altra causa (interferenza) a T_EV; (i) bagliore naturale, (ii) bagliore forzato a T_EV.
import sys, json, importlib.util
from multiprocessing import Pool
sys.path.insert(0, "/home/fede/Scrivania/ed/GitHub/Movi-Hackthon/.sciame/20261114-1301-percezione-challenge/f20-chiusura/05-scorta/correzione_f7r/verifica")
from riconta import wil
SRC = "/home/fede/Scrivania/ed/GitHub/Movi-Hackthon/.sciame/20261114-1301-percezione-challenge/f20-chiusura/05-scorta/correzione_f7r/scorta_f7r_c1.py"
M = None
def lav(a):
    global M
    modo, i = a
    if M is None:
        s = importlib.util.spec_from_file_location("c1", SRC); M = importlib.util.module_from_spec(s); s.loader.exec_module(M)
        orig = M.verita
        def ver(var, cfg, idx, base, _o=orig, _m=modo):
            W = _o(var, cfg, idx, base)
            W["d_rad"] = 1.0
            if _m == "forzato":
                W["ev"]["glint"] = (M.T_EV, 0.5)
            return W
        M.verita = ver
    r = M.passaggio("F7c", "att", i, 20261125)
    return (modo, i, r["falso_evento"], r["avviso_t"], r["libero"], r["cont_ok"])
if __name__ == "__main__":
    lav_ = [(m, i) for m in ("naturale", "forzato") for i in range(200)]
    with Pool(5) as p:
        out = p.map(lav_ and lav, lav_, chunksize=40)
    for m in ("naturale", "forzato"):
        rr = [o for o in out if o[0] == m]
        k = sum(1 for o in rr if o[2] or o[3] is not None)
        print(m, "falsi eventi o avvisi %d/%d %s; cont_ok %d; libero>0 %d" % (k, len(rr), wil(k, len(rr)), sum(o[5] for o in rr), sum(1 for o in rr if o[4] > 0)))
