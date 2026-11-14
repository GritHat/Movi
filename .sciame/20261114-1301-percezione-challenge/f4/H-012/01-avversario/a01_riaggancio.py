# Attacco 1: il riaggancio rubato da chi non era tracciato. Con la correzione (prima e dopo).
from comune_f4 import *

G = 0.40
VMAX = 2.5
ZP, WP = 1.5, 0.5
HS = math.atan((WP / 2) / ZP)


def dist_bordo_ombra(px, pz):
    """Distanza laterale dal bordo dell'ombra del pannello (solo per punti oltre il pannello)."""
    r = math.hypot(px, pz)
    b = abs(math.atan2(px, pz))
    if r <= ZP:
        return 9.0
    return r * math.sin(max(0.0, b - HS))


def dist_altri_bordi(px, pz):
    """Distanza dal resto del non osservato: oltre portata, bordo del campo, anello vicino."""
    r = math.hypot(px, pz)
    b = abs(math.atan2(px, pz))
    return min(RMAX - r, r * math.sin(max(0.0, FOV - b)), r - RNEAR)


def scena(rng, tau, z=2.5):
    v = min(1.6, max(0.8, rng.gauss(1.2, 0.15)))
    xe = -z * math.tan(HS) - 0.2  # ultimo punto col corpo tutto visibile
    kx, kz = KF1(-1.6 + rng.gauss(0, SIG)), KF1(z + rng.gauss(0, SIG))
    x = -1.6
    ult = (x, z)
    while x < xe:
        x += v * DT
        kx.pred(); kz.pred()
        if rng.random() < PD:
            ult = (x + rng.gauss(0, SIG), z + rng.gauss(0, SIG))
            kx.upd(ult[0]); kz.upd(ult[1])
    for _ in range(int(round(tau / DT))):  # l'attore si ferma nascosto; il filtro prosegue
        kx.pred(); kz.pred()
    if rng.random() < 0.5:  # entra da oltre portata
        while True:
            b = rng.uniform(-FOV, FOV)
            if abs(b) > HS:
                break
        r = 2.95
    else:  # entra dal bordo laterale del campo
        b = rng.choice((-1, 1)) * (FOV - math.radians(1))
        r = rng.uniform(1.3, 2.95)
    nx, nz = r * math.sin(b) + rng.gauss(0, SIG), r * math.cos(b) + rng.gauss(0, SIG)
    dist = math.hypot(nx - ult[0], nz - ult[1])
    entro = dist <= VMAX * tau + 3 * SIG * math.sqrt(2)
    L1 = entro  # "bordo dell'ombra" = bordo dello strato 1 (tutto il non osservato contiguo)
    L2 = entro and dist_bordo_ombra(nx, nz) <= G  # bordo dell'ombra del pannello, entro la fascia
    d2 = ((nx - kx.x[0]) ** 2 + (nz - kz.x[0]) ** 2) / (kx.P[0][0] + SIG ** 2)
    L3 = L2 and d2 <= CHI99  # in piu' la porta di Mahalanobis al 99 %
    corr = L2 and dist_altri_bordi(nx, nz) > G  # correzione: lontano da ogni altro bordo del non osservato
    return L1, L2, L3, corr


rng = random.Random(SEME + 1)
N = 200
print("Attacco 1. Attore fermo nell'ombra, traccia pendente unica; un nuovo arrivato compare dopo tau.")
print("Quota di scene con riaggancio SBAGLIATO e MUTO (N = %d per riga); ogni riaggancio rilascia lo strato 1" % N)
print("tau_s  L1_bordo=strato1  L2_bordo=ombra+fascia  L3=L2+porta99  CORREZIONE")
for tau in (0.5, 1.0, 2.0, 5.0):
    rs = [scena(rng, tau) for _ in range(N)]
    print("%4.1f   %6.1f %%          %6.1f %%               %6.1f %%        %6.1f %%" % (
        tau, quota(r[0] for r in rs), quota(r[1] for r in rs), quota(r[2] for r in rs), quota(r[3] for r in rs)))
print("Fotogrammi 'nascosto fuori dallo strato 1' per scena rubata, se l'attore resta nascosto altri 3 s: %d" % int(3 / DT))

print()
print("Costo della correzione: riemersioni LEGITTIME (attore che prosegue) riagganciate, N = 300 per riga")
for z in (2.0, 2.3, 2.5, 2.8):
    ok_prima = ok_dopo = n = 0
    for _ in range(300):
        o = transito(rng, z)
        if not (o['traccia'] and o['riemerge']):
            continue
        n += 1
        # punto di riemersione: bordo d'uscita dell'ombra piu' meta' della parte visibile
        px = z * math.tan(HS) + 0.05 + rng.gauss(0, SIG)
        pz = z + rng.gauss(0, SIG)
        if dist_bordo_ombra(px, pz) <= G:
            ok_prima += 1
            if dist_altri_bordi(px, pz) > G:
                ok_dopo += 1
    print("z = %.1f m: transiti con traccia e riemersione %3d; riagganciati prima %5.1f %%, dopo la correzione %5.1f %% (il resto: 'identita' ambigua', strato 1 tenuto)" % (
        z, n, 100 * ok_prima / max(1, n), 100 * ok_dopo / max(1, n)))
