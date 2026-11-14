# Attacco 4: il tetto T_g = 10 s toglie l'avviso a persona presente. Automa a stati, due letture, e la correzione.
from comune_f4 import *

TG = 10.0


def uscita_griglia(strato1, eta=None):
    """Uscita cella per cella del settore del pannello: 20 celle d'ombra."""
    if strato1:
        return tuple(('in ombra', 'possibile presenza' + ('' if eta is None else ', eta %d s' % eta)) for _ in range(20))
    return tuple(('in ombra', None) for _ in range(20))


def corsa(sosta, lettura, corretta=False):
    t_in = 1.0
    nasc_fuori = 0
    uguali_a_vuota = 0
    fot_dopo = 0
    traccia = 'osservato'
    ident = 'T1'
    k = 0
    while True:
        t = k * DT
        if t < t_in:
            k += 1
            continue
        if t >= t_in + sosta:
            break
        el = t - t_in
        if corretta:
            strato1 = True
            out = uscita_griglia(True, int(el) if el >= TG else None)
        else:
            strato1 = el < TG
            out = uscita_griglia(strato1)
            if not strato1 and lettura == 'a':
                traccia = 'chiusa'
        if not strato1:
            nasc_fuori += 1
        if el >= TG:
            fot_dopo += 1
            uguali_a_vuota += out == uscita_griglia(False)
        k += 1
    # riemersione
    if traccia == 'chiusa':
        esito = 'identita NUOVA, riaggancio non dichiarato'
    else:
        esito = 'stessa identita, riaggancio dichiarato'
    return nasc_fuori, fot_dopo, uguali_a_vuota, esito


print("Attacco 4. Sosta dietro il pannello; T_g = 10 s; 15 Hz.")
print("Lettura (a): a T_g la traccia cade con l'avviso. Lettura (b): la traccia resta 'perso' senza strato 1.")
for lett in ('a', 'b'):
    for sosta in (4, 9, 11, 12, 20, 60):
        n, fd, ug, es = corsa(sosta, lett)
        print("lettura %s, sosta %2d s: fotogrammi 'nascosto fuori dallo strato 1' = %3d; dopo T_g uscita identica alla scena vuota in %3d su %3d fotogrammi; riemersione: %s" % (
            lett, sosta, n, ug, fd, es))
print()
print("[correzione] T_g non toglie la 'possibile presenza': le aggiunge l'eta'; rilascio solo per riaggancio o per celle viste libere")
for sosta in (12, 20, 60):
    n, fd, ug, es = corsa(sosta, 'b', corretta=True)
    print("sosta %2d s: fotogrammi 'nascosto fuori dallo strato 1' = %3d; dopo T_g uscita identica alla scena vuota in %3d su %3d; riemersione: %s" % (
        sosta, n, ug, fd, es))
