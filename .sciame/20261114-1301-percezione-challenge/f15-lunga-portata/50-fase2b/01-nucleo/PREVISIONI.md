# Previsioni prima delle prove (fase 2b, 01-nucleo)

Scritte alle **2026-11-15T01:55:46+01:00** (`date -Is`), prima di scrivere `movi_lp_v2.py` e `prove_v2.py`.
Tutto è conto o simulazione; niente «validato». Le prove unitarie sono deterministiche (un caso costruito = un
passaggio): non danno frequenze, solo esistenza o assenza del difetto sul caso.

| # | Prova | Previsione | Smentita se |
|---|---|---|---|
| P1 | X1 (drone fermo che scatta a 20 e 25 m/s² fino a 45 m/s), scenari `aeroporto_e_droni` e `sito_droni_rullaggio` | v1 fuori dall'insieme ad almeno un τ; v2 dentro a ogni τ ∈ {0,5…30 s} | v2 fuori a un τ qualsiasi |
| P2 | X3, tempestività per l'operatore di sito, radar segnaposto | v2 dichiara «avviso non tempestivo» in `aeroporto_e_droni` (d_avv ≥ 3400 m contro portata del «libero» < 2400 m); in `sito_droni_rullaggio` d_avv ≤ 880 m e tempestivo con n_eff = 1 | `aeroporto` tempestivo, oppure `sito` non tempestivo |
| P3 | X4, 5 passate senza ritorno a 2360 m, multirotore 0,01 m² | v1 «libero»; v2 non «libero»; v2 «libero» a 800 m | v2 «libero» a 2360 m, o nessun «libero» a 800 m |
| P4 | X5, edificio non in pianta, mezzo a 600 m | v2 senza certificazione: non «libero»; con sfondo atteso a 1500 m e misurato a 400 m: «in ombra»; con sfondo misurato come atteso: «libero» | v2 «libero» senza certificazione |
| P5 | X6, classi escluse | `strada` dice «zona non verificata per» pedone; `aeroporto` per il drone C0 | assente |
| P6 | validazione-1: avviso con metà dell'insieme non guardata | v1 chiude la traccia; v2 no; v2 chiude quando tutto l'insieme è «libero» | v2 chiude con l'insieme non tutto «libero», o non chiude mai |
| P7 | validazione-2: ritorno a 2 celle d'azimut (entro 3σ), e radar Doppler | v1 «libero» sulla cella dell'oggetto; v2 no; il Doppler in v2 non produce «libero» e il suo mancato su un bersaglio tangenziale non conta | v2 «libero» sulla cella |
| P8 | tempo | tutte le prove in < 60 s | ≥ 60 s |
| P9 | compatibilità | un passaggio A1 di `prove_lp` gira con v2 al posto del nucleo senza eccezioni (se il tempo basta) | eccezione |

## Aggiunta: pilota A1 con v2 nel simulatore (scritta alle 2026-11-15T02:02:09+01:00, prima del lancio)

Notato dopo le prove unitarie (non era nel piano iniziale): un pilota di **40 passaggi** A1 «alta», indici 0–39, con la
chiamata **«interfaccia»** di prove_lp (quella che con v1 dava 9/200 passaggi con un ciclo senza regione e 436 istanti
«liberi» sull'oggetto), nucleo v2 e regole v2. Conteggi per passaggio, Wilson al 95 %.

| # | Misura | Previsione | Smentita se |
|---|---|---|---|
| P10 | passaggi con almeno un ciclo nascosto senza regione né avviso | 0/40 | ≥ 1 |
| P11 | passaggi con almeno un istante «libero» sulla cella vera del multirotore | 0/40 | ≥ 1 |
| P12 | passaggi tempestivi (definizione di prove_lp) | ≥ 38/40 | ≤ 37 |

## Aggiunta 2 (scritta alle 2026-11-15T02:05:15+01:00, prima del lancio)

Notato dopo il pilota: in prove_lp le griglie non portano certificazione della mappa, quindi con v2 nessuna cella è
mai «libera» e P11 = 0/40 vale **per costruzione**. Ripeto gli stessi 40 passaggi con la mappa **dichiarata completa**
(`MAPPA_CERTIFICATA_PREDEFINITA = True`: il simulatore conosce tutti gli ostacoli), così restano solo n_eff e alone.
P13: passaggi con un istante «libero» sull'oggetto: 0/40 (smentita se ≥ 1; con v1 erano 7/40). P14: passaggi con un
ciclo senza regione o fuori avviso: 0/40 (smentita se ≥ 1).
