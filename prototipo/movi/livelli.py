"""Livello per settore: UNO, il più alto fra «attenzione», «zona non verificata», «suolo visto libero fino a d»
(SOLUZIONE_V3 §1.10). Con affidabilità persa: tutti «affidabilita_persa».

«Visto libero fino a d» si scrive solo se tutte le celle del settore dal bordo vicino fino a d sono «libero»
nel ciclo corrente; una sola cella «non osservato» o «in ombra» ferma d lì. Con l'interruttore
«libero_dal_fotogramma» il «libero» della cella viene da riuso/libero/libero.py (Regole.tutte, settori)."""


def per_settore(stati, possibile_presenza, griglia, settori, tracce, affidabilita="ok"):
    """Rende la lista dei settori nella forma del registro. `stati`: matrice (azimut, distanza) 0–3."""
    raise NotImplementedError("passo 1")
