# Seguito di S1 [notato dopo]: la distanza del pannello decide che cosa dice il messaggio per settori.
import math, importlib.util, io, contextlib
spec = importlib.util.spec_from_file_location("c", "conti_spec.py")
m = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(m)
for zp in (1.15, 1.5, 1.7, 1.9):
    m.ZP = zp; m.HS = math.degrees(math.atan(0.5 / zp))
    for pp in (False, True):
        s = m.settori(pp)
        n = len(s)
        sc = sum(1 for _, v in s if v == 'sconosciuto'); no = sum(1 for _, v in s if v == 'nessun ostacolo')
        ds = [v for _, v in s if not isinstance(v, str)]
        print("pannello 1 m a %.2f m, possibile presenza %s: su %d settori sconosciuto %d, distanza valida %d (%s), nessun ostacolo %d" % (
            zp, "accesa" if pp else "spenta", n, sc, len(ds), ("%.2f-%.2f m" % (min(ds), max(ds))) if ds else "-", no))
