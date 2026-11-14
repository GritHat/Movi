# Torneo dei falsificatori, estensione f7 — `sciame-avversario`

Lavoro dalle 2026-11-14T16:06:59+01:00. File accanto: `PREVISIONI.md` (16:14:21, prima del codice; sei aggiunte, ciascuna con l'ora prima del lancio che decide), `torneo.c`, `prova7.py`, `s11.py`, `risultati_*.txt`, `rifai.sh` (rifà tutto, semi fissi). Tutto è **simulazione a sensore fermo**: camera ideale a 1,2 m inclinata di 15°, 87° × 58°, 320 × 240, rumore 0,004·z², stanza 6 × 4 × 3 m, 15 fotogrammi al secondo. Niente è verificato su una camera vera.

## 0. In testa: cambi di stato, scostamenti, regole violate

- **Cambi di stato proposti.** (1) «Finestra di 3 fotogrammi più clausola *non contraddetto ora*» (V-013 come scritta): **smentita** con buchi a chiazze e con un soggetto che non ritorna segnale. (2) «Il profilo per cella è l'uscita di V-002» (V-003): **smentito** come utilità con buchi sparsi. (3) «Libero col margine v·h» (V-011 minima) come filtro del libero: **smentito** come utilità. (4) S10 «copertura completa»: **smentita**. (5) V-012 «ombra chiusa = è ancora lì»: **smentita** dopo una copertura del sensore. (6) Criterio «celle valide sotto metà» per l'affidabilità persa (nucleo, C10, provato su campioni e non su celle proiettate): **smentito** con buchi sparsi nel mio modello. (7) K-102: **decisa**, il cuneo ostacola la continuità dietro un occlusore basso.
- **Previsioni smentite: quindici.** A2 col pannello fermo; A3 con l'espulsione «più lontano»; A4 per Q in parte (7 su 25 nel «bordo»); A5b col rado; A6 per Q3 e N1; A7 con la porta; A10 per Q3; S10-b a 1,5 m; PP5; «Q3 cede col rado»; «N1 a zero» (celle viste in parte); «N oltre il 95 % di resa» (70 %); ombra visibile del nucleo (23,5 %, previsto > 30 %); libero conservato col margine (0,4 %, previsto 45–75 %); profilo su Q3c (0,8 %, previsto ≥ 25 %). **Non risolta:** A10 per Q1 (una ripetizione su tre a 1,58). Le altre reggono.
- **Scostamenti e regole violate.** (a) Quattro difetti del mio banco corretti dopo il primo lancio (registro in coda a `PREVISIONI.md`): A2 campionava voxel interni mai visti; in A3 il tetto era messo dopo la scrittura; in PP1 il braccio di controllo non falliva; A4 aveva 7 fotogrammi utili (rifatta come `k102`). (b) `rifai.sh` nel suo insieme supera i due minuti (ogni lancio no): eseguito una volta in un solo comando; i `risultati_*.txt` sono di quel rifacimento (stessi conteggi dei primi lanci, tempi un poco diversi). (c) Ho letto per intero quattro consegne (nuvole-punti, creativo, requisiti, matematico); le altre solo attraverso il triage; nessun sorgente delle corsie. (d) Il settimo addendum dà la squadra a 5 persone; ragiono comunque per 3, 4 e 5. (e) Tempi presi con altri processi sulla macchina (carico 2,5): indicativi. (f) Non misurati: identità al ritorno e quota di cicli con la stima emessa (non ho un inseguitore); il passaggio automatico di S10 attorno a 45 ms (nessun codice).
- **Indipendenza.** Candidate, scena e verità sono dello stesso autore e dello stesso modello di camera; le candidate sono riscritte dalle descrizioni, non dal codice dei ruoli. Il controllo vale per i difetti delle regole, non per quelli del sensore (pixel misti, buchi veri, vetro vero).

**Sigle.** N0, N1: griglia del nucleo senza e con la clausola «occupato e ombra di ora vincono sul libero recente». Q1: stato di un punto letto in un fotogramma (V-002). Q3: Q1 con finestra di 3 fotogrammi e clausola (V-013). **Q3c: Q3 più «il pixel centrale è valido ora»** (mia correzione). P: profilo (V-003). S10: tre fasce da Q1. VO: voxel da 10 cm, log-odds, «attraversato = libero». VOa: VO più età, clausola e prudenza sul voxel visto in parte. VH: blocchi 8³ da 5 cm con tetto. Regioni di possibile presenza: cuneo (nucleo), V12 (V-012), **rec** (mia, §4). «Profondo» = a più di 5 cm dentro un corpo, o nascosto anche spostando il punto di 3 cm.

## 1. Le dieci prove (più l'undicesima), una per una

Per ogni prova: nucleo (N), V-002 (Q), S10, voxel; poi il verdetto. File: `risultati_statica`, `_a2`, `_a3`, `_a4`, `_a5`, `_a5c`, `_a6`, `_a8`, `_a9`, `_a10`, `_prova7` (`.txt`).

1. **Non allocato = libero?** N: 0 celle mai viste. Q: 0 su 149 200 punti (braccio «non valido = libero»: 1 267 falsi). S10 prudente 0; a maschera (bit a zero = libero) 109 celle con la barra dentro. Voxel a tre vie 0; a due vie 80 505 falsi su 146 901. **Regge solo con l'interrogazione a tre stati.**
2. **Ombra libera per decadimento?** N, Q: 0 su 944 e 897 fotogrammi. Voxel: dietro un pannello fermo resta «sconosciuto» (previsione smentita); con un pannello che scorre davanti a un soggetto già visto, il decadimento verso il libero lo libera in 830 fotogrammi su 897. **Smentita solo per quel decadimento.**
3. **Rimozione di un blocco.** VH col tetto sotto la domanda (442 blocchi su 477) ed espulsione del meno recente: persi 14 448 voxel di possibile presenza su 22 240, soggetto fuori regione in 132 fotogrammi su 134. Con i blocchi fissati: 0 persi e 1,0 milioni di espulsioni. Regione fuori dalla mappa: non toccata. **Smentita in mappa.**
4. **Nascosto dato per osservato?** N: 0 su 25; **nel verso opposto, l'adulto visibile (2 552 pixel) è dato per nascosto in 31 fotogrammi su 31**. Q: 0 dal corpo; 7 su 25 cadono nel «bordo» entro 8 cm dietro il pannello (va etichettato bordo). VO: «occupato» fantasma in ombra in 144 fotogrammi su 150. **N alla lettera smentita (K-102).**
5. **Dato vecchio su occlusione nuova.** Scatola che compare: N0 438 punti per 2 fotogrammi, N1 0; Q3 senza clausola 12 755; VO 15 805 per sempre (base 3 735). **Attacco nuovo:** con chiazze al 30 % Q3 dà liberi punti profondi in 43 fotogrammi su 87, VOa in 40; con un soggetto che non ritorna segnale Q3 in 44 su 87, VOa in 45, N1 dà liberi 1 186 punti al suolo sotto il corpo. Q1 e Q3c: 0 profondi. **Q3, VOa, VO, N0 smentite, N1 col soggetto che non ritorna segnale; Q1 e Q3c reggono.**
6. **Errore di posa** (1° non segnalato, riferimento del mondo). N1 37 (14 profondi; base 11); Q 1 225 (278); S10 65 (1); VO +836 (+708); VOa 94 (20). **Smentita per tutte: non discrimina; difende solo il controllo IMU.**
7. **Scambio muto d'identità** (logica, 200 corse). «Una traccia pendente per ombra d'ingresso»: 200 scambi muti; con la porta al 99 %: 64; regola globale del nucleo: 0. **Regge solo la regola globale.**
8. **Vetro.** Punti della lastra dati liberi a 2 m: Q 654 su 800, S10 580, VO 680; N 24–28 celle. **Smentita per tutte; non risolto.**
9. **Sensore coperto.** Tutto non valido: Q1, Q3c, P, S10 0 subito; N, Q3, VOa liberi ancora 2 fotogrammi (Q3: 61 194 punti); VO 71 006 per sempre. Fotogramma congelato: tutte, finché non scatta «3 identici». **VO smentita.**
10. **Carico improvviso** (soglia: massimo ≤ 1,35 × mediana). N 1,05 ms (1,04–1,48); Q1 0,29 ms per 18 640 punti (1,06–1,58; massimo 0,46 ms); Q3 0,59 ms (2,0–2,1); P 4,95 ms; VO 4,3 ms (1,25–1,46); VH 9,8 ms, col tetto a 300 blocchi 33 ms e massimo 70. **VH col tetto smentita; Q1 e N non risolte sul rapporto (macchina carica), limitate in assoluto.**
11. **Visto in parte = libero?** N: 10 punti al suolo (celle a cavallo dell'anello cieco). Q: 0 (senza 3 × 3 e margine: 104). S10 alla lettera: 10,5 % dei suoi liberi. VO: 12,0 % (7,0 % profondi); VOa 0. **VO e S10 alla lettera smentite.**

Prova 9, in più: con il **10 % di pixel validi sparsi le celle note del nucleo restano 1 444 su 1 460** (finestra di 3 fotogrammi; `risultati_scenA.txt`): il criterio «celle valide sotto metà» non scatta mai col rado, e a chiazze solo al 10 % (717 celle). Va contato sui pixel.

**S10 (V-005), prove sue** (`risultati_s10.txt`). Con la fascia alta pertinente: 0 celle libere su 2 610. Con bassa e media: 1 040 celle, nessuna fra 1,24 e 1,61 m. Barra a 1,7–1,9 m di quota: a 1,5 m 0 celle (previsione smentita: lì S10 non dice mai libero), **a 2,0 m 75 celle libere con la barra sopra, a 2,5 m 67 celle libere con la barra vista da 3 170 pixel**. Scatola alta 10 cm: 32 celle libere sopra la scatola; N1 e P 0. 

## 2. I tre scenari degradati

Reticolo a 10 cm, 18 640 punti; i tempi sono quelli dello scenario B (`risultati_scenB.txt`, `risultati_scenC.txt`). F = fotogrammi con un falso libero profondo; S = soggetto-fotogrammi con un punto del corpo dato per libero (fra parentesi: soggetto del tutto nascosto); resa = quota del libero vero dichiarata.

| Candidata | B, 147 fot.: F / S / resa | C sparso 50 %, 87 fot. | C a chiazze 50 % | ms mediana / max |
|---|---|---|---|---|
| N1 (suolo) | 147 (2 punti a fot., celle viste in parte) / 2 (0) / 73,8 % | 68 / 0 (0) | 71 / 1 (0) | 1,05 / 1,59 |
| N0 | 147 / 20 (0) | 85 / 68 (4) | 87 / 62 (4) | = |
| Q1 | 0 / 0 / 97,1 % | 0 / 0 | 0 / 0 | 0,29 / 0,31 |
| Q3 | 0 / 0 / 97,1 % | 2 / 3 (0) | **15 / 55 (4)** | 0,50 / 0,58 |
| Q3c | 0 / 0 / 97,1 % | 0 / 0 | 0 / 0 | 0,48 / 0,55 |
| P | 2 / 60 (0) / 42,2 % | 0 / 10 | 0 / 14 | 4,97 / 7,54 |
| S10 (bassa + media) | 0 / 0 / 30,6 % | 0 / 0 | 0 / 0 | = |
| VO | 147 / 200 (2) / 97,6 % | 87 / 342 (50) | 87 / 349 (52) | 4,87 / 7,09 |
| VOa | 0 / 0 / 83,0 % | 1 / 1 (0) | **15 / 84 (5)** | 6,24 / 9,03 |

**A, azzeramento progressivo** (`risultati_scenA.txt`). Sparso: Q1, Q3, Q3c 0 falsi a ogni passo; la resa di Q1 cade a 37,5 % al 90 % di validi e a 0,2 % al 50 %; Q3 74,2 %, Q3c 68,2 % al 90 %; P e S10 a 0,0 % già al 90 %; N resta al 70 % fino al 10 % (una cella «si vede» con un solo pixel: robusta, e per lo stesso motivo cieca agli oggetti piccoli). A chiazze: Q1 85,0 → 6,0 %, Q3c 86,9 → 6,6 %, 0 falsi; Q3 falsi in 16–32 fotogrammi su 57 a ogni passo; VOa in 54–57. «Affidabilità persa» contata sui pixel validi (sotto metà) scatta, per definizione, al passo del 40 %.

## 3. Contraddizioni decise

- **K-102: decisa, sì.** Il nucleo non ha codice con la quota (`comune_f4.py`, righe 44–58: l'ombra è un intervallo d'angolo), quindi decido sul mio. Adulto dietro una cassa da 1 m: «osservato» in 0 fotogrammi su 31 con «oltre il primo ritorno = ombra»; con «ogni ritorno è occupato» 31 su 31, ma il gruppo sta tutto nel cuneo e la regola C6 lo toglie al filtro. Q1 e P: 31 su 31 (`risultati_k102.txt`).
- **K-104.** Barra a 1,5 m: 68 celle N1 «libero» con la barra nella colonna; P dichiara al più 1,55 m. L'uscita deve dire «suolo» o portare la quota.
- **K-105: sì, sul mio codice.** I simulatori della validazione non hanno una regola del libero per cella (`grep -i libero`): conto sul mio N1. 537 celle-fotogramma libere e occupate entro 0,20 s; 31 da un soggetto che alla dichiarazione non aveva pixel validi. Col margine 0,33 m: 0, ma il libero scende allo 0,4 % (`risultati_k105.txt`).
- **K-106.** 5 % sparso: Q1 61,1 % (no), Q3c 87,7 %. Chiazze 20 × 20 al 5 %: Q1 90,9 %, Q3c 92,0 % (sì). P: 0,1 % e 30,0 %; costruito su Q3c 0,8 %.
- **K-101.** Un altro codice: 4,4 ns per passo di raggio (968 850 passi in 4,3 ms, compreso il giro sui 72 000 voxel); l'ombra memorizzata costa +23 % di passi (`risultati_a10.txt`).

## 4. Regione nascosta e continuità visiva

| Prova (`risultati_pp.txt`) | cuneo | V12 | rec |
|---|---|---|---|
| PP1 sosta 60 s, pannello alto: fotogrammi fuori regione su 900 | 0 | 0 | 0 |
| PP1 area (celle; ombra vera 154) | 161 | 164 | 168 |
| PP2 pedana da 0,5 m: area (ombra vera 90, chiusa) | 170 | 90 | 94 |
| PP3 sensore coperto 2 s, il carrello cambia ombra: fuori su 60 | 60 | 60 (e dice «ombra chiusa») | 0 |
| PP4 occlusore mobile a 0,5 m/s: fuori su 192 | 146 | 146 | 0 |

Bracci di controllo: timer di 10 s 750 su 900; sagoma ristretta 900 su 900; rec con un salto in un solo fotogramma coperto 7 fotogrammi fuori (PP5, a 3 m/s, non l'ha rotta: fra le due ombre c'erano 0,16 m).

**avversario-1, «rec».** *Meccanismo:* sul piano, celle da 10 cm: Π(t) = Π(t−1) dilatata di una cella, tolte le celle il cui punto a 10 cm di quota è visto libero ora da Q; seme all'ingresso della traccia nell'ombra; nessun timer, nessuna sagoma. È V-011 usata come regione, non come filtro del libero. *Previsione:* 0 fotogrammi fuori regione con occlusore fermo, mobile o sensore coperto, per soggetti sotto 1,5 m/s. *La smentisce:* un fotogramma fuori a velocità ammessa; oppure un'area oltre 1,5 volte l'ombra vera a occlusore fermo. *Limiti visti:* fonde ombre separate da meno di 0,2 m; dipende dal suolo visto oltre 3 m. Costo: 30 righe di C qui; 2–3 ore (stima mia, non verificata).

**Effetto di ogni scelta sulla continuità.** Cuneo con occlusore basso: **ostacola** (K-102). Q3c: **aiuta**, dà alla previsione «dove vedo vuoto» in tre dimensioni con 0 falsi profondi in tutte le mie prove, salvo l'errore di posa. Q3 come scritto: **ostacola**, taglierebbe la previsione proprio dove passa un corpo che non ritorna segnale. V12: aiuta per la forma, **non regge** copertura e occlusore mobile. rec: **aiuta**. S10: non tocca. Mappa voxel: non tocca fuori dal percorso critico; dentro **ostacola** (fantasmi in ombra, regione persa con l'espulsione). Margine di V-011: ostacola se filtra il libero.

## 5. Q2: attacco a T-001, T-002, S11

1. **Coperte solo a parole:** «oggetti» (nessun evento su un oggetto fermo: lo dice requisiti stesso), «ispezione» (non è una funzione), «aerospaziali» (una stanza a 3 m), «bassa latenza» (155 ms contro 150, non risolta), «Intelligenza Artificiale» (se si taglia l'etichetta asincrona non resta alcun modello appreso: va detto).
2. **Tre frasi dell'apertura proposta sono false nella mia simulazione delle regole del nucleo.** «Ciò che non è osservato non è mai dato per libero»: col «libero» a 3 fotogrammi del nucleo, 1 186 punti al suolo dentro un corpo che non ritorna segnale sono dati per liberi in 47 fotogrammi (`risultati_a5c.txt`); più vetro e fotogramma congelato. «La perdita di affidabilità è dichiarata»: non col 90 % di pixel persi sparsi. «Seguirli quando un ostacolo li nasconde»: non dietro un occlusore più basso del sensore, che in un ambiente industriale è la norma.
3. **Un giurato esterno crederebbe provati** camera vera, più persone, casse e carrelli, registro. I fatti: simulazione, una persona, un pannello più alto del sensore, registro non costruito (16–52 % di eventi mancati nella sua prova).
4. **S11 (T-005)** (`risultati_s11.txt`, mia lettura dell'aggiornamento a ogni ciclo). `SOSTA_IN_OMBRA` esce in 200 corse su 200 se il soggetto si ferma, **in 200 su 200 se se ne va in profondità dentro l'ombra senza fermarsi**, e in 153 transiti normali su 200 prima della ricomparsa. L'evento va rinominato «non ricomparso da n s (dedotto)».

## 6. Stati proposti, ore e momento

| Scelta | Stato | Ore-persona | Quando |
|---|---|---|---|
| N1 al posto di N0; frase «suolo visto libero, in quota fino a 1,2 + 0,25·r» | sostenuto dai dati | 0,5 | **14 h, indispensabile** |
| Affidabilità contata sui pixel validi | sostenuto dai dati | 0,5 | **14 h, indispensabile** |
| Dopo una copertura le possibili presenze restano e diventano «non più localizzate» | sostenuto dai dati (PP3) | 0,5–1 | **14 h, indispensabile** |
| V-002 nella forma Q3c | sostenuto dai dati | 2–3 | 14 h se la demo ha un occlusore più basso del sensore; altrimenti 4 h |
| rec | sostenuto dai dati, un solo autore | 2–3 | 4 h (chiede Q) |
| V-012 | forma: regge; chiusura: smentita | 2–3 | dopo: col pannello alto è il cuneo (164 contro 161 celle) |
| V-003, S10 | utilità smentita con i buchi; S10 **NO** come sostituto | — | dopo; l'etichetta di quota la dà la frase sopra |
| V-011 come filtro del libero | utilità smentita | — | scartata; resta limite dichiarato |
| Mappa voxel (V-006, V-007, V-009), passaggio automatico di S10 | VO o VH smentite nelle prove 1–5, 9, 10, 11, nelle varianti dette | 6–10 (triage) | dopo l'hackathon |
| T-001 con le tre frasi corrette; T-002 minimo con «come lo so» | non risolto fino al lettore esterno | 1 + 3–4 | 14 h |
| S11 cinematica | smentita senza etichetta | — | dopo f8 e f9 |

Le voci «14 h» sommano 5,5–7 ore-persona (7,5–10 con Q3c), divisibili fra chi fa la griglia e chi fa registro e testo: il 13–17 % di 42 ore (3 persone), il 10–13 % di 56, l'8–10 % di 70 (ore: stime, non verificate). A parità di prove la via più semplice è: pannello più alto del soggetto, cuneo del nucleo, N1, le tre regole da mezz'ora.

**Che cosa è sopravvissuto della mappa voxel.** Niente che sia suo: quote diverse, ombra bassa e libero prudente li dà Q3c senza mappa, con 0 falsi profondi, resa 97,1 % contro 83,0 % della variante voxel migliore (VOa) e 0,48 ms contro 6,24. Non sopravvivono: memoria (437–525 blocchi su 1 200, e col tetto 33 ms a ciclo), libero da log-odds, possibile presenza nei blocchi, continuità. **Non attaccato**, quindi non risolto: la memoria dell'occupato fra più punti di vista con il sensore in moto. Dal mio lato Q1 è **NO** per le 14 ore e per le 4.

## 7. Dopo

1. Rifare Q3c e rec con un secondo autore e, appena c'è, 60 s di profondità vera con una persona vestita di scuro: decide se i buchi veri sono chiazze (Q3c tiene) o rado (cade).
2. La validazione porti la quota nei simulatori del nucleo: oggi K-102 è decisa solo sul mio codice.
3. All'utente: pannello della demo più alto del soggetto, sì o no; e le tre frasi dell'apertura.
