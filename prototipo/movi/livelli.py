"""Livello per settore: UNO, il più alto fra «attenzione», «zona non verificata», «suolo visto libero fino a d»
(SOLUZIONE_V3 §1.10). Con affidabilità persa: tutti «affidabilita_persa».

«Visto libero fino a d»: nella direzione PEGGIORE del settore, d è la distanza fin dove tutte le celle, dalla prima
distanza osservabile `r_da` in poi, sono «libero» nella griglia DICHIARATA di questo ciclo (dopo la regola del libero
e la salute del sensore). Una sola cella «non osservato», «in ombra» o «occupato» ferma d lì. Se d non supera r_da il
settore è «zona non verificata». Convenzione di r_da (1,3 m) presa da riuso/libero/libero.py, `settori(…, r_da=13)`.

Le etichette di classe NON entrano qui (principio 3): la funzione non le riceve."""
import numpy as np

LIBERO, OCCUPATO = 1, 2


def per_settore(stati, possibile_presenza, settori, passo_m, affidabilita="ok", r_da=13):
    """`stati`: matrice (azimut, distanza) 0–3 dichiarata; `possibile_presenza`: maschera; `settori`: [(a0, a1, az)].
    Rende la lista dei settori nella forma del registro."""
    fuori = []
    for k, (a0, a1, az) in enumerate(settori):
        s = stati[a0:a1]
        pp = int(possibile_presenza[a0:a1].sum())
        occ = (s == OCCUPATO)
        if affidabilita != "ok":
            fuori.append({"id": k, "azimut_gradi": az, "livello": "affidabilita_persa", "d_m": None,
                          "motivo": "sensore non in salute: niente si dichiara visto"})
            continue
        if occ.any() or pp:
            primo = None
            if occ.any():
                primo = round(float(np.nonzero(occ.any(axis=0))[0].min() * passo_m), 2)
            fuori.append({"id": k, "azimut_gradi": az, "livello": "attenzione", "d_m": primo,
                          "motivo": "occupato" if occ.any() else "possibile presenza"})
            continue
        sub = s[:, r_da:] == LIBERO
        primo_non = np.where(sub.all(axis=1), sub.shape[1], (~sub).argmax(axis=1))
        d = (r_da + int(primo_non.min())) * passo_m
        if primo_non.min() > 0:
            fuori.append({"id": k, "azimut_gradi": az, "livello": "visto_libero_fino_a", "d_m": round(d, 2),
                          "motivo": "suolo visto libero in questo fotogramma"})
        else:
            fuori.append({"id": k, "azimut_gradi": az, "livello": "zona_non_verificata", "d_m": None,
                          "motivo": "suolo non visto libero oltre la prima distanza osservabile"})
    return fuori
