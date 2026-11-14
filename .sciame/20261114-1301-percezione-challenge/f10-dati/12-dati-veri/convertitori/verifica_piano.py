"""Verifica empirica della convenzione «lungo l'asse ottico» su una scena piana (se lo è): per un piano, 1/Z è
lineare in (u, v). Se i valori fossero distanze lungo il raggio, lineare sarebbe 1/(valore·cosθ).
Uso: python -I -B verifica_piano.py <sequenza> <indice>"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comune, numpy as np
seq, i = sys.argv[1], int(sys.argv[2]); m = comune.leggi_meta(seq); a = comune.leggi_profondita(seq, i).astype(np.float64)
v, u = np.mgrid[0:a.shape[0], 0:a.shape[1]]
ok = (a > 0) & (a < 3000)
xn, yn = (u - m["cx"]) / m["fx"], (v - m["cy"]) / m["fy"]
cos = 1 / np.sqrt(1 + xn ** 2 + yn ** 2)
for nome, z in (("asse ottico (Z = valore)", a), ("raggio (Z = valore·cosθ)", a * cos)):
    sel = ok.copy()
    for _ in range(4):                                   # minimi quadrati con scarto dei valori lontani
        A = np.stack([xn[sel], yn[sel], np.ones(sel.sum())], 1); c, *_ = np.linalg.lstsq(A, 1 / z[sel], rcond=None)
        zf = 1 / (xn * c[0] + yn * c[1] + c[2]); r = z - zf; s = 1.4826 * np.median(np.abs(r[sel] - np.median(r[sel])))
        sel = ok & (np.abs(r) < 3 * s + 1e-9)
    print(f"{nome}: pixel usati {sel.sum()} su {ok.sum()} ({sel.sum()/ok.sum():.2f}); scarto robusto dal piano {s:.2f} mm; "
          f"residuo medio al centro {np.mean(r[sel & (cos > 0.95)]):+.2f} mm, ai bordi (cosθ < 0,8) {np.mean(r[sel & (cos < 0.8)]) if (sel & (cos < 0.8)).any() else float('nan'):+.2f} mm")
