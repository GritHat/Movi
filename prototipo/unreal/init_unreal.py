# Avvio del progetto MoVi: rende importabile il codice del prototipo e apre una "cassetta" per eseguire script
# nell'editor aperto: quando /home/fede/Scrivania/ed/GitHub/Movi-Hackthon/prototipo/unreal/_inbox.py cambia, viene eseguito e l'esito va in _outbox.txt.
import os, sys, io, traceback, contextlib, unreal
D = "/home/fede/Scrivania/ed/GitHub/Movi-Hackthon/prototipo/unreal"
if D not in sys.path: sys.path.insert(0, D)
_st = {"m": os.path.getmtime(D + "/_inbox.py") if os.path.exists(D + "/_inbox.py") else 0.0}
def _cassetta(dt):
    p = D + "/_inbox.py"
    try:
        m = os.path.getmtime(p)
    except OSError:
        return
    if m == _st["m"]: return
    _st["m"] = m
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            exec(compile(open(p).read(), p, "exec"), {"__name__": "__main__"})
        buf.write("\nOK\n")
    except Exception:
        buf.write("\nERRORE\n" + traceback.format_exc())
    open(D + "/_outbox.txt", "w").write(buf.getvalue())
unreal.register_slate_post_tick_callback(_cassetta)
unreal.log("MoVi: cassetta degli script attiva")
