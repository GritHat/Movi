# Oracolo degradato (livello b): etichette a mano con errori iniettati da una matrice di confusione dichiarata
# e con un ritardo dichiarato. Conta quante tracce ricevono una velocita' massima usata piu' bassa
# (1) della linea di base senza etichetta, (2) della velocita' massima VERA della loro classe.
# Tutte le velocita' massime per classe qui sotto sono IPOTESI di lavoro (i profili li fissa un altro ruolo):
# servono solo a ordinare le classi in lente e veloci. Uso: python -I -B oracolo_degradato.py
import numpy as np

SEME = 20261114
N = 10_000
CLASSI = ["persona", "bicicletta", "carrello_elev", "auto", "treno_tram", "multirotore", "generico"]
VMAX = np.array([1.8, 7.0, 4.0, 14.0, 14.0, 10.0, 2.0])        # m/s, IPOTESI
PRIORI = np.array([0.50, 0.08, 0.15, 0.10, 0.02, 0.05, 0.10])  # mescolanza delle prove, IPOTESI
K = len(CLASSI)
EPS = 0.02           # soglia dell'insieme credibile
SOGLIA_FIDUCIA = 0.6  # sotto: «non classificato»


def uniforme(e):
    m = np.full((K, K), e / (K - 1))
    np.fill_diagonal(m, 1 - e)
    return m


def strutturata():
    # errori soprattutto dentro la categoria o fra sagome simili
    m = np.eye(K) * 0.0
    m[0] = [0.92, 0.04, 0.00, 0.00, 0.00, 0.00, 0.04]
    m[1] = [0.10, 0.85, 0.00, 0.02, 0.00, 0.00, 0.03]
    m[2] = [0.03, 0.00, 0.75, 0.12, 0.00, 0.00, 0.10]
    m[3] = [0.00, 0.01, 0.08, 0.88, 0.02, 0.00, 0.01]
    m[4] = [0.00, 0.00, 0.02, 0.10, 0.88, 0.00, 0.00]
    m[5] = [0.02, 0.00, 0.00, 0.00, 0.00, 0.80, 0.18]
    m[6] = [0.08, 0.02, 0.05, 0.00, 0.00, 0.05, 0.80]
    return m


def avversa():
    # ogni classe veloce finisce «persona» 2 volte su 10
    m = uniforme(0.0)
    for i in range(1, K):
        m[i, i] = 0.8
        m[i, 0] = 0.2
    return m


MATRICI = {"identita' (livello a)": uniforme(0.0), "uniforme 10 %": uniforme(0.10),
           "strutturata": strutturata(), "avversa veloce->persona 20 %": avversa()}


def prova(nome, C, v_base, ritardo, rng):
    assert np.allclose(C.sum(1), 1)
    vera = rng.choice(K, size=N, p=PRIORI)
    u = rng.random(N)
    etichetta = (u[:, None] > np.cumsum(C, 1)[vera]).sum(1).clip(0, K - 1)
    durata = rng.uniform(2.0, 10.0, N)           # s di vita della traccia
    ha_etichetta = durata > ritardo
    # a posteriori dichiarata dell'oracolo degradato: P(vera = k | etichetta = j)
    post = PRIORI[:, None] * C
    post = post / np.maximum(post.sum(0, keepdims=True), 1e-12)
    fiducia = post[etichetta, etichetta]
    # regola ingenua: la classe etichettata decide la velocita'
    v_ing = np.where(ha_etichetta, VMAX[etichetta], v_base)
    # regola «solo allarga», etichetta secca
    v_all = np.where(ha_etichetta, np.maximum(v_base, VMAX[etichetta]), v_base)
    # regola «solo allarga» con insieme credibile: tutte le classi con probabilita' >= EPS;
    # sotto la soglia di fiducia l'etichetta e' «non classificato» e vale la linea di base
    v_cred_per_et = np.array([VMAX[post[:, j] >= EPS].max() if (post[:, j] >= EPS).any() else 0.0 for j in range(K)])
    v_cre = np.where(ha_etichetta, np.maximum(v_base, v_cred_per_et[etichetta]), v_base)
    riga = [nome, v_base, ritardo]
    for v in (v_ing, v_all, v_cre):
        riga += [int((v < v_base).sum()), int((v < VMAX[vera]).sum())]
    riga.append(int((fiducia < SOGLIA_FIDUCIA).sum()))
    return riga


rng = np.random.default_rng(SEME)
print(f"seme {SEME}, N = {N} tracce per braccio, EPS = {EPS}; conteggi su {N}")
print("matrice | v_base | ritardo s | ING <base | ING <vera | ALL <base | ALL <vera | CRED <base | CRED <vera | fiducia<0,6")
tot_all_base = 0
for v_base in (1.4, 4.0):
    for ritardo in (0.0, 0.5, 2.0):
        for nome, C in MATRICI.items():
            r = prova(nome, C, v_base, ritardo, rng)
            tot_all_base += r[5] + r[7]
            print(" | ".join(str(x) for x in r))
print("somma dei casi «solo allarga» (secca e credibile) sotto la linea di base, su tutti i bracci:", tot_all_base)
# conto analitico di controllo per la regola ingenua, senza ritardo: P(v etichetta < v vera)
for nome, C in MATRICI.items():
    q = sum(PRIORI[i] * C[i, j] for i in range(K) for j in range(K) if VMAX[j] < VMAX[i])
    print(f"analitico, ingenua, quota attesa <vera con «{nome}»: {q:.4f}")
print("quota a priori di tracce con v vera > v_base:", {vb: round(float(PRIORI[VMAX > vb].sum()), 3) for vb in (1.4, 4.0)})
