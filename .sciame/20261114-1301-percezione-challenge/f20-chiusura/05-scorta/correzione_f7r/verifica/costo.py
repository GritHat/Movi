import json, math, sys
from riconta import wil
D = "/home/fede/Scrivania/ed/GitHub/Movi-Hackthon/.sciame/20261114-1301-percezione-challenge/f20-chiusura/05-scorta/correzione_f7r/passaggi_f7r_c1_valutazione.jsonl"
G, VT = 9.81, 40.0
def L(tau, v0=140.0, r0=115.0):
    a = G / VT
    return (VT * VT / G) * math.log(math.cosh(a * tau) + (v0 / VT) * math.sinh(a * tau)) + r0
dur = []; rad = []; nonint = [0, 0]; t_rit = []
for l in open(D):
    r = json.loads(l)
    if r["cfg"] != "att" or r["var"] == "F7c": continue
    t0 = r["avviso_nl_t"] - 0.1
    td = r["evento_t"]
    if td is None: fine = t0 + 8
    elif td < t0 + 3: fine = t0 + 3
    else: fine = min(td, t0 + 8)
    dur.append(fine - t0); rad.append(L(fine - t0))
    if r["interseca_t"] is None:
        nonint[1] += 1; nonint[0] += r["avviso_t"] is not None
    t_rit.append((r["avviso_nl_t"], r["avviso_t"], td))
dur.sort(); rad.sort()
print("passaggi con evento (att):", len(dur))
print("durata volume non localizzato s: min %.1f med %.1f max %.1f" % (dur[0], dur[len(dur)//2], dur[-1]))
print("raggio orizzontale finale m: min %.0f med %.0f max %.0f ; volume sfera eq. med %.2e m3" % (rad[0], rad[len(rad)//2], rad[-1], 4/3*math.pi*rad[len(rad)//2]**3))
print("raggio a 1 s %.0f m, 3 s %.0f m, 8 s %.0f m" % (L(1), L(3), L(8)))
print("avviso acceso in passaggi senza frammento a 10 m: %d/%d %s" % (nonint[0], nonint[1], wil(*nonint)))
print("avviso_t - avviso_nl_t (s):", sorted(set(round(a - b, 2) for b, a, _ in t_rit if a is not None)))
print("evento localizzato dichiarato:", sum(1 for *_, td in t_rit if td is not None), "/", len(t_rit))
