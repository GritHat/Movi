#!/usr/bin/env python3
"""Seconda prova (dopo l'esito di int-P7, quindi esplorativa: NON era prevista).
Varianti della regola per settore: ordine di B7 (visto > previsto), segnale piu' corto,
fusione dei settori in attesa in un solo segnale 'piu' zone'.
Rifare: PYTHONDONTWRITEBYTECODE=1 timeout 120 python3 -I prove_interfacce_bis.py > risultati_interfacce_bis.txt
"""
import random
SEME = 20261114


def scena(rng, n_ogg, stesso):
    return [(t := rng.uniform(0.0, 2.0), t + rng.uniform(0.7, 2.0), 0 if stesso else rng.randrange(3)) for _ in range(n_ogg)]


def st_ogg(o, t):
    return "previsto" if o[0] <= t < o[1] else "visto"


def st_sett(ogg, sett, t, b7):
    st = [st_ogg(o, t) for o in ogg if o[2] == sett]
    if not st:
        return "nessuno"
    if b7:   # B7: il visto prevale sul previsto
        return "visto" if "visto" in st else "previsto"
    return "previsto" if "previsto" in st else "visto"


def regola(ogg, b7, segn, pausa, fondi):
    tempi = sorted({o[0] for o in ogg} | {o[1] for o in ogg})
    cambi = []
    for sett in range(3):
        prec = st_sett(ogg, sett, -1.0, b7)
        for t in tempi:
            s = st_sett(ogg, sett, t, b7)
            if s != prec:
                cambi.append((t, sett, s))
                prec = s
    cambi.sort()
    libero, attesa, rit, scad, i, nsegn = 0.0, {}, [], 0, 0, 0
    while i < len(cambi) or attesa:
        if attesa:
            t_now = max(libero, min(v[0] for v in attesa.values()))
            while i < len(cambi) and cambi[i][0] <= t_now:
                attesa[cambi[i][1]] = (cambi[i][0], cambi[i][2]); i += 1
            servi = list(attesa) if (fondi and len(attesa) >= 2) else [min(attesa, key=lambda k: attesa[k][0])]
            for sett in servi:
                t_c, s = attesa.pop(sett)
                rit.append(t_now - t_c)
                if st_sett(ogg, sett, t_now, b7) != s:
                    scad += 1
            nsegn += 1
            libero = t_now + segn + pausa
        else:
            attesa[cambi[i][1]] = (cambi[i][0], cambi[i][2]); i += 1
    return rit, scad, nsegn


def q(v, p):
    v = sorted(v)
    return v[min(len(v) - 1, int(p * len(v)))]


print("Varianti della regola per settore, 3 oggetti, 20000 scene per riga, seme", SEME)
for stesso in (False, True):
    for nome, b7, segn, pausa, fondi in (
        ("previsto prevale, 0,3+0,1 s", False, 0.3, 0.1, False),
        ("ordine B7 (visto prevale), 0,3+0,1 s", True, 0.3, 0.1, False),
        ("ordine B7, 0,2+0,05 s", True, 0.2, 0.05, False),
        ("ordine B7, 0,3+0,1 s, fusione 'piu zone'", True, 0.3, 0.1, True),
        ("ordine B7, 0,2+0,05 s, fusione 'piu zone'", True, 0.2, 0.05, True),
    ):
        rng = random.Random(SEME + 31 + (1 if stesso else 0))
        rit, scad, ns = [], 0, 0
        for _ in range(20000):
            r, s, n = regola(scena(rng, 3, stesso), b7, segn, pausa, fondi)
            rit += r; scad += s; ns += n
        dove = "stesso settore" if stesso else "3 settori a caso"
        print(f"  {dove:17s} | {nome:42s}: cambi {len(rit)}, segnali {ns}; oltre 0,3 s {100*sum(1 for x in rit if x>0.3)/len(rit):.1f} %; "
              f"oltre 0,145 s {100*sum(1 for x in rit if x>0.145)/len(rit):.1f} %; p95 {q(rit,0.95):.2f} s; massimo {max(rit):.2f} s; a stato scaduto {100*scad/len(rit):.2f} %")
