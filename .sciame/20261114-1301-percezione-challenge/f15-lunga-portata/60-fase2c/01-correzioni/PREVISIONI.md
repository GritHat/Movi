# Previsioni e soglie (fase 2c, 01-correzioni), scritte PRIMA delle misure

Ora: 2026-11-15T03:06:42+01:00 (date -Is). Autore: sciame-tracciamento. Tutto è simulazione: niente è «validato». Wilson 95 % per passaggio.

P1 (K-613, letterale). Nucleo v3 con la sola finestra W_c = min(t_cumulo, lato / v_max_vera), v_max_vera = v_max
dell'inviluppo delle classi ammesse dallo scenario (45 m/s nel sito), per OGNI classe. Previsione del coordinatore
(RIPROVA): «libero» sull'oggetto non C0 in A1 alta (sito) <= 2/171; smentita se >= 10/171.
MIA previsione contraria, scritta prima: la classe vincolante è già multirotore_veloce (45 m/s, 0,01 m2), quindi la
sola finestra NON cambia quasi nulla: prevedo >= 10/171 (la previsione del coordinatore è smentita). Lo dico perché
con rho = 1 (n_eff = 1) basta UNA passata mancata dopo un ritorno per dare «libero»: il difetto è la mancata
singola, non la lunghezza della finestra.
P2 (v3 completo: P1 + ritenuta del ritorno). Una cella con un ritorno (o alone) nella cella o nelle vicine (anche in
elevazione) negli ultimi T_rit = t_cumulo = 5 s non diventa «libera». Previsione: <= 2/171 in A1 alta sito; smentita
se >= 10/171. Prezzo da misurare: tempestivi A1 alta e min >= 190/200 (smentita sotto 190); fuori avviso A1 min non
peggiore di 12/200 + 6 (smentita se >= 19/200).
P3 (mappa, cp_X5b rifatto). Prototipo con v3: mappa NON dichiarata completa per predefinito. Previsione: dietro un
edificio non in pianta lo stato è «non osservato» (3) per ogni d, 0 casi «libero» su 6. Smentita con 1 solo «libero».
P4 (E1, eventi_v3: età massima della traccia d'origine, fusione dei duplicati, ispezione dell'impronta). Previsione:
mediana del raggio dell'impronta <= 5 km; smentita se >= 10 km in >= 5 passaggi su 30 (applico la stessa soglia
riscalata su 60: >= 10 passaggi su 60). «Libero» su un frammento: 0/60 (smentita con 1). Separazioni prima
dell'urto: 0/60 (smentita con 1).
P5 (avviso ai mezzi solo se il percorso previsto entra nell'impronta). E2: mezzo avvisato nei passaggi in cui il
percorso previsto entra nell'impronta, e solo in quelli: concordanza >= 29/30; smentita sotto 27/30.
P6 (E5 col v3): 0/30 falsi eventi; smentita con 1.
P7 (video): il validatore della controprova dà 0 celle «libero» dentro l'avviso e 0 discordanze di conteggio su
tutte le scene _v3; smentita con 1.
P8 (prova_tutto.sh): esito 0.
Semi per la scelta A CASO delle scene (dichiarati ora, prima di vedere): numpy default_rng(20261115), lp_A1:
indice = rng.integers(0, 200) fra i passaggi di A1 alta; lp_E1: poi indice = rng.integers(0, 60).
90 30
