# Quanto costa al piano finale (variante C2) un compito «etichette a mano» (ET). Carica il modello del pianificatore senza modificarlo.
import importlib.util, sys
spec = importlib.util.spec_from_file_location("pm", sys.argv[1]); m = importlib.util.module_from_spec(spec)
import contextlib, io
with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(m)   # il modulo stampa i suoi risultati all'import: li scarto
def base():
    g = []
    for cid, chi, pred in m.GRAFO:
        if cid == 'C2': g.append(('C2a', ['P3'], ['SK'])); g.append(('C2b', ['P3'], ['C2a']))
        else: g.append((cid, chi, ['C2b' if q == 'C2' else q for q in pred]))
    return g
MIE = dict(m.MIE, C2a=(.75, 1, 2), C2b=(1.25, 1.5, 3)); R2 = dict(m.RUOLO2, C2a=(.75, 1.25, 2.25), C2b=(1.25, 1.75, 3.25))
m.PIOLI = [(p, ['B2', 'C2a', 'SK'] if p == 'regione' else ['A5', 'A3r', 'C3a'] if p == 'salute' else c) for p, c in m.PIOLI]
def con_et(g, chi, dopo, in_pi):
    out = []
    for cid, c, pred in g:
        if cid == 'PI' and in_pi: pred = pred + ['ET']
        if cid == 'PG' and not in_pi: pred = pred + ['ET']
        if cid == 'C2b' and chi == 'P3' : pred = pred  # C2b resta dopo C2a; ET usa la stessa persona
        out.append((cid, c, pred))
    i = [k for k, x in enumerate(out) if x[0] == dopo][0]
    out.insert(i + 1, ('ET', [chi], [dopo]))
    return out
for nome, et in (("minimo 2,5 h", (2, 2.5, 4)), ("tutto 5,5 h", (4, 5.5, 8))):
    for st_n, st, ip in (("mie/leggero", MIE, m.LEGGERO), ("ruolo2/medio", R2, m.MEDIO)):
        print("--- ET %s, %s" % (nome, st_n))
        m.riga("senza ET", st, ip, grafo=base())
        m.riga("ET su P3 dopo C2a, fuori dal tronco (solo prima della prova generale)", dict(st, ET=et), ip, grafo=con_et(base(), 'P3', 'C2a', False))
        m.riga("ET su P3 dopo C2a, nel tronco (PI la aspetta)", dict(st, ET=et), ip, grafo=con_et(base(), 'P3', 'C2a', True))
        m.riga("ET su P4 dopo D2a, nel tronco", dict(st, ET=et), ip, grafo=con_et(base(), 'P4', 'D2a', True))
