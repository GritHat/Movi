# prova7.py — prova 7 del contratto: riaggancio ambiguo con due ombre d'ingresso adiacenti.
# Logica pura, un asse (x lungo la corsia dietro due occlusori adiacenti: L copre [-1,0], R copre [0,1]).
# A entra in L da sinistra, B entra in R da destra; dietro si incrociano; B esce a sinistra, A a destra.
# Uso: python3 -I prova7.py   (seme fisso)
import math, random
rng = random.Random(20261114)
Q, S0, GATE = 0.2, 0.05, 3.03  # rumore di processo del nucleo, sigma iniziale, porta al 99 % (2D)
N = 200
esiti = {"per_ombra": [0, 0, 0], "per_ombra_con_porta": [0, 0, 0], "globale": [0, 0, 0]}  # muti, ambigui, giusti
largh = []
for _ in range(N):
    vA, vB = rng.uniform(0.8, 1.6), rng.uniform(0.8, 1.6)
    tA, tB = 0.0, rng.uniform(-0.5, 0.5)          # istanti d'ingresso
    # B esce dal bordo sinistro (x = -1) dopo aver percorso 2 m
    t_out = tB + 2.0 / vB
    dt = t_out - tA                                 # buio della traccia A a quell'istante
    x_pred = -1.0 + (vA + rng.gauss(0, 0.1)) * dt   # previsione di A a velocita' costante
    sig = math.sqrt(S0 ** 2 + Q * max(dt, 0) ** 3 / 3 + (0.1 * dt) ** 2)
    largh.append(GATE * sig)
    in_porta = abs(-1.0 - x_pred) <= GATE * sig
    # il rilevamento compare nella fascia dell'ombra L; pendenti con ombra d'ingresso L: solo A (B e' entrato da R)
    esiti["per_ombra"][0] += 1                      # riaggancia ad A: e' B -> scambio muto
    if in_porta: esiti["per_ombra_con_porta"][0] += 1
    else: esiti["per_ombra_con_porta"][1] += 1
    esiti["globale"][1] += 1                        # due tracce pendenti -> «identita' ambigua»
print("# prova 7: due occlusori adiacenti, due soggetti che si incrociano dietro; %d corse" % N)
for k, (m, a, g) in esiti.items():
    print("%-22s scambi muti %3d   identita' ambigua %3d   giusti %3d" % (k, m, a, g))
largh.sort()
print("semilarghezza della porta al 99 %% al momento dell'uscita: mediana %.2f m, minimo %.2f m (ombra larga 2 m)" % (largh[N // 2], largh[0]))
# controllo: un solo occlusore e una sola traccia pendente -> la regola per ombra e quella globale coincidono
print("controllo: una sola traccia pendente -> riaggancio in tutte e due le regole (per costruzione, non misurato)")
