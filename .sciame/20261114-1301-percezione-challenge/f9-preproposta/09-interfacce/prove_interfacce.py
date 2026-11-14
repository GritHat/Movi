#!/usr/bin/env python3
"""Prove di sciame-interfacce (f9, S5 e uscita di S8). Solo libreria standard.

Rifare:  PYTHONDONTWRITEBYTECODE=1 timeout 120 python3 -I prove_interfacce.py > risultati_interfacce.txt

Sono conti e una simulazione a eventi dell'autore stesso della critica: generatore e
giudice condividono autore e ipotesi. Nessuna persona, nessuno schermo, nessun suono.
"""
import math
import random

SEME = 20261114


# ---------------------------------------------------------------- A. colori
def lin(c):
    c /= 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def rgb_lin(hexs):
    return [lin(int(hexs[i:i + 2], 16)) for i in (0, 2, 4)]


def lum(rgb):
    return 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]


def rapporto(l1, l2):
    a, b = max(l1, l2), min(l1, l2)
    return (a + 0.05) / (b + 0.05)


# Machado, Oliveira, Fernandes 2009, severita' 1.0 (pagina degli autori, aperta oggi)
MACHADO = {
    "protanopia": [[0.152286, 1.052583, -0.204868], [0.114503, 0.786281, 0.099216], [-0.003882, -0.048116, 1.051998]],
    "deuteranopia": [[0.367322, 0.860646, -0.227968], [0.280085, 0.672501, 0.047413], [-0.011820, 0.042940, 0.968881]],
    "tritanopia": [[1.255528, -0.076749, -0.178779], [-0.078411, 0.930809, 0.147602], [0.004733, 0.691367, 0.303900]],
}


def applica(m, rgb):
    return [min(1.0, max(0.0, sum(m[i][j] * rgb[j] for j in range(3)))) for i in range(3)]


def lab(rgb):
    x = 0.4124564 * rgb[0] + 0.3575761 * rgb[1] + 0.1804375 * rgb[2]
    y = 0.2126729 * rgb[0] + 0.7151522 * rgb[1] + 0.0721750 * rgb[2]
    z = 0.0193339 * rgb[0] + 0.1191920 * rgb[1] + 0.9503041 * rgb[2]

    def f(t):
        return t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116
    fx, fy, fz = f(x / 0.95047), f(y), f(z / 1.08883)
    return (116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz))


def delta_e(a, b):
    la, lb = lab(a), lab(b)
    return math.sqrt(sum((p - q) ** 2 for p, q in zip(la, lb)))


def prova_colori():
    print("== A. Colori (int-P1) ==")
    terne = {
        "documento v0.5 (ok, warn, todo)": {"ok/verde": "1E7A4C", "warn/ambra": "A8620A", "todo/grigio": "6B7280"},
        "semaforo (verde, ambra, rosso)": {"verde": "2E7D32", "ambra": "FFB300", "rosso": "C62828"},
    }
    for nome, terna in terne.items():
        print(f"-- terna: {nome}")
        nomi = list(terna)
        for k in nomi:
            print(f"   {k:12s} #{terna[k]}  luminanza relativa {lum(rgb_lin(terna[k])):.3f}")
        for i in range(3):
            for j in range(i + 1, 3):
                a, b = rgb_lin(terna[nomi[i]]), rgb_lin(terna[nomi[j]])
                riga = f"   {nomi[i]} / {nomi[j]}: grigio {rapporto(lum(a), lum(b)):.2f}:1"
                for vis, m in MACHADO.items():
                    sa, sb = applica(m, a), applica(m, b)
                    riga += f" | {vis} lum {rapporto(lum(sa), lum(sb)):.2f}:1, dE {delta_e(sa, sb):.0f}"
                riga += f" | vista normale dE {delta_e(a, b):.0f}"
                print(riga)
    # campitura ambra semitrasparente su fondo bianco e su fondo scuro, contro il grigio dell'ombra
    print("-- campitura piena ambra (alfa 0,35) contro grigio 'in ombra' (alfa 0,35 di 6B7280), solo luminanza")
    for fondo_nome, fondo in (("fondo bianco", "FFFFFF"), ("fondo scuro 16202B", "16202B")):
        f = rgb_lin(fondo)
        amb = [0.35 * x + 0.65 * y for x, y in zip(rgb_lin("FFB300"), f)]
        gri = [0.35 * x + 0.65 * y for x, y in zip(rgb_lin("6B7280"), f)]
        print(f"   {fondo_nome}: ambra/ombra {rapporto(lum(amb), lum(gri)):.2f}:1; ambra/fondo {rapporto(lum(amb), lum(f)):.2f}:1; ombra/fondo {rapporto(lum(gri), lum(f)):.2f}:1")


# ---------------------------------------------------------------- B. cifre che cambiano
def prova_cifre():
    print("\n== B. Cifre che cambiano a ogni ciclo (int-P2) ==")
    dt, q = 1 / 15, 0.2
    for sigma_mis in (0.02, 0.04, 0.10):
        r = sigma_mis ** 2
        # regime del filtro CV a un asse [p, v]
        p11, p12, p22 = 1.0, 0.0, 1.0
        for _ in range(400):
            # predizione
            p11, p12, p22 = (p11 + 2 * dt * p12 + dt * dt * p22 + q * dt ** 3 / 3,
                             p12 + dt * p22 + q * dt * dt / 2,
                             p22 + q * dt)
            # aggiornamento
            s = p11 + r
            k1, k2 = p11 / s, p12 / s
            p11, p12, p22 = (1 - k1) * p11, (1 - k1) * p12, p22 - k2 * p12
        etichette, sig = [], []
        n = int(round(3.0 / dt))
        for c in range(1, n + 1):
            p11, p12, p22 = (p11 + 2 * dt * p12 + dt * dt * p22 + q * dt ** 3 / 3,
                             p12 + dt * p22 + q * dt * dt / 2,
                             p22 + q * dt)
            t = c * dt
            s1 = math.sqrt(p11)
            sig.append((t, s1))
            etichette.append((t, f"{s1:.2f}", f"{t:.1f}", f"{s1:.1f}"))
        fin = [(a, b) for a, b in zip(etichette, etichette[1:]) if 0.3 <= b[0] <= 2.0]
        camb2 = sum(1 for a, b in fin if a[1] != b[1])
        cambt = sum(1 for a, b in fin if a[2] != b[2])
        camb_et = sum(1 for a, b in fin if (a[1], a[2]) != (b[1], b[2]))
        camb1 = sum(1 for a, b in fin if a[3] != b[3])
        durata = fin[-1][1][0] - fin[0][0][0]
        val = {round(t, 2): s for t, s in sig}
        campi = ", ".join(f"{tt:.1f} s: {min(sig, key=lambda z: abs(z[0] - tt))[1]:.3f} m" for tt in (0.5, 1.0, 2.0, 3.0))
        print(f"-- rumore di misura {sigma_mis:.2f} m: sigma per asse a {campi}")
        print(f"   fra 0,3 e 2,0 s ({len(fin)} cicli): '±X.XX' cambia in {camb2}/{len(fin)} cicli ({100 * camb2 / len(fin):.1f} %); "
              f"'t_occ Y.Y' in {cambt}/{len(fin)} ({100 * cambt / len(fin):.1f} %); etichetta (due campi) {camb_et / durata:.1f} cambi/s; "
              f"con un decimale: {camb1} cambi in {durata:.2f} s ({camb1 / durata:.1f}/s)")


# ---------------------------------------------------------------- C. che cosa vuol dire ±
def prova_sigma():
    print("\n== C. Che cosa contiene '±sigma' (int-P3) ==")
    print(f"   1 dimensione, entro 1 sigma: {100 * math.erf(1 / math.sqrt(2)):.1f} %")
    print(f"   2 dimensioni (isotropa), entro il cerchio di raggio sigma: {100 * (1 - math.exp(-0.5)):.1f} %")
    for p in (0.5, 0.9, 0.95):
        k = math.sqrt(-2 * math.log(1 - p))
        print(f"   raggio al {int(p * 100)} %: {k:.3f} sigma; con sigma = 0,8 m: {0.8 * k:.2f} m (area {math.pi * (0.8 * k) ** 2:.1f} m2)")


# ---------------------------------------------------------------- D. il cuneo della demo
def prova_cuneo():
    print("\n== D. Scarto della massa stesa sul cuneo d'ombra (int-P4) ==")
    passo = 0.01
    for dist in (1.7, 1.8, 1.9):
        for largh in (1.0,):
            mezzo = math.atan2(largh / 2, dist)
            celle = []
            n = int(3.0 / passo)
            for ix in range(-n, n + 1):
                x = ix * passo
                for iz in range(0, n + 1):
                    z = iz * passo
                    r = math.hypot(x, z)
                    if r > 3.0 or z <= dist:
                        continue
                    if abs(math.atan2(x, z)) <= mezzo:
                        celle.append((x, z))
            # fascia di 0,40 m: dilatazione approssimata allargando l'angolo e arretrando di 0,40 m
            def stat(cs):
                m = len(cs)
                mx = sum(c[0] for c in cs) / m
                mz = sum(c[1] for c in cs) / m
                vx = sum((c[0] - mx) ** 2 for c in cs) / m
                vz = sum((c[1] - mz) ** 2 for c in cs) / m
                return m * passo * passo, math.sqrt(vx), math.sqrt(vz), math.sqrt(vx + vz)
            a, sx, sz, sr = stat(celle)
            # insieme dilatato di 0,40 m (entro la griglia): punti a meno di 0,40 m dal cuneo
            # approssimazione conservativa per eccesso: settore allargato di 0,40 m ai lati e in avanti
            dil = []
            for ix in range(-n, n + 1):
                x = ix * passo
                for iz in range(0, n + 1):
                    z = iz * passo
                    r = math.hypot(x, z)
                    if r > 3.0 or z <= dist - 0.40:
                        continue
                    # distanza laterale dal bordo del cuneo: bordo = retta per l'origine con angolo 'mezzo'
                    ang = abs(math.atan2(x, z))
                    if ang <= mezzo:
                        dil.append((x, z))
                    else:
                        d_lat = r * math.sin(ang - mezzo)
                        if d_lat <= 0.40:
                            dil.append((x, z))
            a2, sx2, sz2, sr2 = stat(dil)
            print(f"   pannello {largh:.1f} m a {dist:.1f} m: cuneo {a:.2f} m2, scarto per asse {sx:.2f} / {sz:.2f} m, radiale {sr:.2f} m | "
                  f"con fascia 0,40 m (per eccesso) {a2:.2f} m2, per asse {sx2:.2f} / {sz2:.2f} m, radiale {sr2:.2f} m")


# ---------------------------------------------------------------- E. quanti decimali regge la taratura
def wilson(k, n, z=1.959964):
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return c - h, c + h


def prova_decimali():
    print("\n== E. Quanti decimali regge la taratura (int-P5) ==")
    kr = lambda p: math.sqrt(-2 * math.log(1 - p))
    for k, n in ((27, 30), (28, 30), (360, 400), (380, 400)):
        lo, hi = wilson(k, n)
        p = k / n
        r0, rl, rh = kr(p), kr(lo), kr(hi)
        print(f"   {k}/{n} = {100 * p:.1f} %: Wilson 95 % [{100 * lo:.1f}; {100 * hi:.1f}] %; il raggio che darebbe quella copertura va da "
              f"{rl / r0:.2f} a {rh / r0:.2f} volte il dichiarato: su 0,80 m, da {0.8 * rl / r0:.2f} a {0.8 * rh / r0:.2f} m")


# ---------------------------------------------------------------- F. leggibilita' da sala
def prova_sala():
    print("\n== F. Etichetta a leggibilita' da sala (int-P6; schermo 2,0 m e 1920 punti, giurato a 6 m: ipotesi) ==")
    etichetta = "PREVISTO ±0.42 m | t_occ 1.3s | conf 72%"
    corta = "n.2 PREVISTO entro 0,5 m"
    px_mm = 1920 / 2000.0
    px_m_mappa = 1080 / 3.0  # la mappa usa tutta l'altezza per 3 m di profondita'
    print(f"   etichetta della preproposta: {len(etichetta)} caratteri; corretta: {len(corta)} caratteri; scala mappa {px_m_mappa:.0f} punti/m; "
          f"ombra del pannello larga 1,0 m = {px_m_mappa:.0f} punti al pannello, {px_m_mappa * 3.0 / 1.8:.0f} punti a 3 m")
    for arcmin in (16, 20, 22):
        for d in (4.0, 6.0, 8.0):
            h_mm = d * 1000 * math.tan(math.radians(arcmin / 60))
            cap_px = h_mm * px_mm
            corpo = cap_px / 0.70      # altezza delle maiuscole = 0,70 del corpo (ipotesi)
            passo = 0.55 * corpo       # avanzamento medio = 0,55 del corpo (ipotesi)
            w = len(etichetta) * passo
            wc = len(corta) * passo
            print(f"   {arcmin}' a {d:.0f} m: maiuscola {h_mm:.0f} mm = {cap_px:.0f} punti, corpo {corpo:.0f} punti; etichetta {w:.0f} punti "
                  f"({w / px_m_mappa:.1f} volte l'ombra al pannello); tre etichette {3 * w:.0f} punti su 1920; corretta {wc:.0f} punti")


# ---------------------------------------------------------------- G. canale sonoro con tre oggetti nascosti
PRI = {"visto": 3, "previsto": 2, "nessuno": 0}
SEGN, PAUSA = 0.3, 0.1


def scena(rng, n_ogg, stesso_settore):
    ogg = []
    for i in range(n_ogg):
        t_in = rng.uniform(0.0, 2.0)
        dur = rng.uniform(0.7, 2.0)
        sett = 0 if stesso_settore else rng.randrange(3)
        ogg.append((t_in, t_in + dur, sett))
    return ogg


def stato_ogg(o, t):
    return "previsto" if o[0] <= t < o[1] else "visto"


def coda_per_oggetto(ogg):
    """Un segnale per ogni cambio di stato di ogni oggetto, in ordine d'arrivo."""
    ev = []
    for i, o in enumerate(ogg):
        ev.append((o[0], i, "previsto"))
        ev.append((o[1], i, "visto"))
    ev.sort()
    libero = 0.0
    ritardi, scaduti = [], 0
    detti = set()
    for t, i, s in ev:
        inizio = max(t, libero)
        ritardi.append(inizio - t)
        if stato_ogg(ogg[i], inizio) != s:
            scaduti += 1
        else:
            detti.add((i, s))
        libero = inizio + SEGN + PAUSA
    # stati 'previsto' mai detti mentre valgono
    mai = sum(1 for i in range(len(ogg)) if (i, "previsto") not in detti)
    return ritardi, scaduti, mai, len(ogg)


def stato_settore(ogg, sett, t):
    st = [stato_ogg(o, t) for o in ogg if o[2] == sett]
    if not st:
        return "nessuno"
    # regola corretta proposta: il settore dice 'previsto' se almeno un oggetto e' nascosto
    return "previsto" if "previsto" in st else "visto"


def regola_per_settore(ogg):
    """Un segnale per cambio di stato del settore; in coda vale solo l'ultimo stato del settore
    (i segnali scaduti si scartano); a canale libero parte il settore in attesa da piu' tempo."""
    tempi = sorted({o[0] for o in ogg} | {o[1] for o in ogg})
    cambi = []  # (t, settore, stato nuovo)
    for sett in range(3):
        prec = stato_settore(ogg, sett, -1.0)
        for t in tempi:
            s = stato_settore(ogg, sett, t)
            if s != prec:
                cambi.append((t, sett, s))
                prec = s
    cambi.sort()
    libero = 0.0
    attesa = {}  # settore -> (t del cambio, stato)
    ritardi, scaduti = [], 0
    detti_prev = set()
    i = 0
    intervalli_prev = [(t, sett) for t, sett, s in cambi if s == "previsto"]
    t_now = 0.0
    while i < len(cambi) or attesa:
        # prossimo istante utile
        if attesa:
            t_now = max(libero, min(v[0] for v in attesa.values()))
            # accoda tutti i cambi arrivati entro t_now
            while i < len(cambi) and cambi[i][0] <= t_now:
                attesa[cambi[i][1]] = (cambi[i][0], cambi[i][2])
                i += 1
            sett = min(attesa, key=lambda k: attesa[k][0])
            t_c, s = attesa.pop(sett)
            ritardi.append(t_now - t_c)
            if stato_settore(ogg, sett, t_now) != s:
                scaduti += 1
            elif s == "previsto":
                detti_prev.add((t_c, sett))
            libero = t_now + SEGN + PAUSA
        else:
            attesa[cambi[i][1]] = (cambi[i][0], cambi[i][2])
            i += 1
    mai = sum(1 for x in intervalli_prev if x not in detti_prev)
    return ritardi, scaduti, mai, len(intervalli_prev), len(cambi)


def prova_suono():
    print("\n== G. Canale sonoro seriale con oggetti nascosti (int-P7) ==")
    print(f"   segnale {SEGN} s + pausa {PAUSA} s; ingressi in ombra uniformi in 0-2 s; occlusioni uniformi 0,7-2,0 s; 20000 scene per riga; seme {SEME}")
    for n_ogg in (1, 2, 3):
        for stesso in (False, True):
            rng = random.Random(SEME + 10 * n_ogg + (1 if stesso else 0))
            ra, sa, ma, na = [], 0, 0, 0
            rb, sb, mb, nb, ncambi = [], 0, 0, 0, 0
            for _ in range(20000):
                ogg = scena(rng, n_ogg, stesso)
                r, s, m, n = coda_per_oggetto(ogg)
                ra += r; sa += s; ma += m; na += n
                r, s, m, n, c = regola_per_settore(ogg)
                rb += r; sb += s; mb += m; nb += n; ncambi += c

            def q(v, p):
                v = sorted(v)
                return v[min(len(v) - 1, int(p * len(v)))]
            dove = "stesso settore" if stesso else "settori a caso (3)"
            print(f"-- {n_ogg} oggetti, {dove}")
            print(f"   coda per oggetto : {len(ra)} segnali; partiti oltre 0,3 s: {100 * sum(1 for x in ra if x > 0.3) / len(ra):.1f} %; "
                  f"oltre 0,145 s: {100 * sum(1 for x in ra if x > 0.145) / len(ra):.1f} %; p95 del ritardo {q(ra, 0.95):.2f} s; "
                  f"massimo {max(ra):.2f} s; partiti a stato scaduto {100 * sa / len(ra):.1f} %; 'previsto' mai detto mentre vale {100 * ma / na:.1f} %")
            print(f"   regola per settore: {len(rb)} segnali ({ncambi} cambi di settore); oltre 0,3 s: {100 * sum(1 for x in rb if x > 0.3) / len(rb):.1f} %; "
                  f"oltre 0,145 s: {100 * sum(1 for x in rb if x > 0.145) / len(rb):.1f} %; p95 {q(rb, 0.95):.2f} s; massimo {max(rb):.2f} s; "
                  f"a stato scaduto {100 * sb / len(rb):.1f} %; 'previsto' di settore mai detto mentre vale {100 * mb / max(1, nb):.1f} %")


if __name__ == "__main__":
    prova_colori()
    prova_cifre()
    prova_sigma()
    prova_cuneo()
    prova_decimali()
    prova_sala()
    prova_suono()
