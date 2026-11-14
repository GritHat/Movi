# Previsioni di `sciame-architetto`, estensione f7, fase f3 (decisione)

Scritte alle 2026-11-14T16:45:33+01:00 (`date -Is`), PRIMA dei miei controlli e prima di leggere le otto consegne delle corsie, il verdetto, l'audit, la specializzazione e il moto proprio.
**Non sono cieche:** a quest'ora ho già letto contratto, addendum, `promptMare.txt`, `prepropostaEsterna.md`, `TRIAGE.md`, `TORNEO.md`, `BENCHMARK_INDIPENDENTE.md`, `SOLUZIONE_V2.md`, `ATTACCO_SPECIALIZZAZIONE.md` e il contratto di f8. Conosco quindi i numeri che ricalcolo: valgono come controlli di riproducibilità, non come dati nuovi.

## A. Controlli miei (decisi da un comando o da un conto)

- **PA1 — geometria del campo.** Camera a 1,2 m, inclinata di 15° verso il basso, campo verticale 58° (bordo alto +14°, bordo basso −44°). Ricalcolo: suolo visto da 1,24 m; ostacolo di 15 cm fuori campo sotto 1,09 m di DISTANZA; quota 1,8 m vista da 2,41 m; quota 2,0 m vista da 3,21 m; tetto del campo 1,2 + 0,25·r. *Regge* se le cinque cifre tornano entro 0,02 m. *Smentita* se una differisce di più.
- **PA2 — ombra bassa.** L'ombra al suolo di un occlusore alto h < H a distanza d finisce a d·H/(H−h): cassa da 1,0 m a 1,5 m → 9,0 m (oltre la portata: equivale al cuneo); pedana da 0,5 m a 1,5 m → 2,57 m; scatola da 0,3 m a 1,7 m → 2,27 m. *Smentita* se la terza cifra non è 2,27 ± 0,02 (è quella scritta nel triage).
- **PA3 — rifacimento del torneo.** Rilanciando lo scenario B del torneo (`11-torneo`, comando in `rifai.sh`, sotto `timeout 120`): Q3c 0 fotogrammi con falso libero profondo su 147 e resa 97,1 %; VOa resa 83,0 %; VO 147 su 147. *Regge* se i conteggi sono identici (i tempi no: macchina carica). *Smentita* se un conteggio differisce. *Non risolta* se il lancio non parte o supera i due minuti. Indipendenza: stesso codice, stessa macchina, stesso modello: copre solo l'errore di trascrizione.
- **PA4 — il nucleo non ha la quota.** In `f4/H-012/03-validazione/comune_f4.py` (o dove sta) l'ombra è un intervallo d'angolo senza quota dell'occlusore. *Regge* se nel calcolo dell'ombra non compare l'altezza dell'occlusore. *Smentita* se compare.
- **PA5 — lessico dei documenti dati all'utente.** In `proposta/proposta_sciame.tex`: almeno 5 occorrenze di «uncrewed», «UAV» o «drone»; la traccia (`regole_challenge.md`) ne ha 0. *Smentita* se il sorgente ne ha meno di 5 (l'elenco delle modifiche sarebbe più corto del previsto).
- **PA6 — ore.** Le aggiunte di f7 che dichiaro «indispensabili nelle 14 ore» sommano ≤ 10 ore-persona; il nucleo con i tagli più le aggiunte sta in 70 ore-persona (5 persone) ma NON in 42 (3 persone). *Smentita* se le aggiunte superano 12, o se il totale entra anche in 42. Sono somme di stime altrui non verificate: l'esito vale come coerenza del conto.

## B. Attese sulla decisione (da confrontare con ciò che scrivo dopo aver letto tutto)

- **PB1.** La risposta a Q1 sarà NO per le 14 + 4 ore (nessun beneficio che sia proprio della mappa voxel) e «non risolto» solo per la memoria dell'occupato con sensore in moto. *Smentita* se una delle otto consegne porta una misura di un beneficio che l'interrogazione nel fotogramma non dà.
- **PB2.** S10 alla lettera: NO come sostituto; resta come frase d'uscita con la quota. S11: sì solo come registro con la colonna «come lo so», «sosta in ombra» rinominata.
- **PB3.** Dove le prove tirano in versi opposti (da dichiarare senza scegliere): finestra di 3 fotogrammi (robustezza al rado) contro lettura del solo fotogramma corrente (nessun falso); cuneo (semplice, provato nel nucleo) contro regione ricorsiva «rec» (un solo autore).

## Esiti (compilati dopo)

- **PA7 (aggiunta alle 2026-11-14T16:46:42+01:00, prima dei tre lanci).** Rifacendo `pp`, `k102` e `scenC` del torneo con lo stesso sorgente: PP3 fuori regione 60 / 60 / 0 su 60 (cuneo / V12 / rec), PP4 146 / 146 / 0 su 192, PP2 area 170 / 90 / 94; K-102: adulto «osservato» 0 su 31 col cuneo e 31 su 31 con Q1; scenario C a chiazze 50 %: Q3 15 fotogrammi con falso libero profondo, Q3c 0. *Smentita* se un conteggio differisce.

## C. Previsioni per l'attacco successivo (scritte alle 2026-11-14T16:52:14+01:00, prima di ogni prova che le decide; nessuna è stata eseguita da me)

- **PD1 — la clausola sul suolo.** Usando Q3c (memoria di 2 fotogrammi valida solo se il pixel centrale è valido ora e nessun pixel del 3 × 3 è più vicino del punto) come sola fonte del «suolo visto libero» della griglia polare, nel banco del torneo (scenari B, C sparso 50 %, C a chiazze 50 %, A5c «soggetto che non rimanda segnale»): 0 fotogrammi con un punto del suolo dato per libero a più di 5 cm dentro un corpo (oggi N1 in A5c: 87 fotogrammi su 87, 1 186 punti occupati). *Smentita:* un solo fotogramma. *Utilità:* nello scenario B senza buchi la resa del suolo resta ≥ 60 % (N1: 73,8 %); *smentita* sotto il 50 %.
- **PD2 — lo sfarfallio.** Con il 5 % di pixel non validi sparsi, una cella della griglia cambia stato fra «libero» e «non osservato» in media non più di 3 volte al secondo (stima a mano: 2·p·(1−p)·15 con p ≈ 0,93 → circa 2). *Smentita:* oltre 5 al secondo. Se smentita, la stabilità va messa sul messaggio (stato stabile prima di parlare, già in B8 del nucleo), non sul predicato.
- **PD3 — rec con un secondo autore.** Riscritta da un altro ruolo dalle due righe del meccanismo, negli scenari PP1–PP4 del torneo: 0 fotogrammi col soggetto nascosto fuori regione sotto 1,5 m/s; area ≤ 1,5 volte l'ombra vera in PP1 e PP2. *Smentita:* un fotogramma fuori, o area oltre 1,5 volte. In campo aperto con un rilevamento mancato su dieci: regioni accese a vuoto in non più del 20 % dei passaggi (il cuneo: 12,8–14,3 %); *smentita* oltre il 20 %.
- **PD4 — il pannello.** Nel modello a foro (camera a 1,2 m, 15°, 58°), con un pannello alto 1,5 m a 1,7 m e un soggetto alto 1,75 m a 2,3 m, la testa rimanda pixel validi (fascia visibile 1,61–1,75 m: almeno 100 pixel a 320 × 240); con un pannello alto 1,70 m: 0. *Smentita:* 0 pixel col pannello da 1,5 m.
- **PD5 — il costo sul prototipo.** Griglia polare più 2 610 letture Q3c più 1 000 letture per l'area prevista: p95 ≤ 2 ms in C sulla macchina della demo a 640 × 480. *Smentita:* oltre 5 ms. In Python: non previsto (nessuna misura con le librerie vere).
- **PD6 — il registro.** Con la riga «non ricomparso da n s (dedotto)» al posto di `SOSTA_IN_OMBRA`: 0 righe «osservato» senza una misura nel fotogramma su 600 scene; eventi mancati ancora sopra il 10 % delle scene finché le zone non stanno ad almeno 0,37 m dal bordo del campo. *Smentita:* una riga «osservato» a soggetto nascosto.

## Esiti (scritti alle 17:03 del 14 novembre 2026, dopo i controlli)

- **PA1 regge.** 1,243 m; 1,087 m; 2,406 m; 3,209 m; tetto 1,2 + 0,2493·r (`conti.txt`).
- **PA2 regge.** 2,27 m per la scatola da 0,3 m a 1,7 m; 2,57 m per la pedana; 9,0 m per la cassa da 1 m.
- **PA3 regge.** `rifatto_scenB.txt`: conteggi identici a `11-torneo/risultati_scenB.txt` (Q3c 0 fotogrammi con falso profondo su 147, resa 97,1 %; VOa 83,0 %; VO 147 su 147); differiscono solo i tempi. 10,3 s.
- **PA4 regge.** `f4/H-012/01-avversario/comune_f4.py`, funzioni `osservabile` e `in_ombra_griglia`: l'ombra è `b <= hs and r > zp`, senza quota dell'occlusore. Il file non sta in `03-validazione/`, come avevo scritto, ma in `01-avversario/`.
- **PA5 smentita.** Nel sorgente v0.6 «uncrewed» compare in 1 riga (la 143), «UAV» e «drone» in 0: il titolo e la testata usano già le parole della traccia. L'elenco delle modifiche riguarda altro (definizione di «libero», pannello, riga 158, verdetti).
- **PA6 regge sul limite.** Aggiunte «14 ore»: 8–10,5 ore-persona (attese ≤ 10; soglia di smentita 12). Totale 58–60,5: sta in 70, non in 42; non sta nemmeno in 56.
- **PA7 regge.** `rifatto_pp.txt`, `rifatto_k102.txt`, `rifatto_scenC.txt`: conteggi identici agli originali.
- **PB1 regge.** Nessuna delle otto consegne porta la misura di un beneficio che la lettura nel fotogramma non dia; resta non risolta la memoria fra punti di vista in moto.
- **PB2 regge.** **PB3 regge**, e se ne aggiunge una terza che non avevo previsto: la correzione C6 del nucleo contro la contraddizione K-102 (gruppo tagliato dall'ombra).

**Notato dopo, senza previsione.** (1) Con un pannello alto 1,5 m a 1,7–1,9 m, un attore a 2,3 m resta in vista sopra 1,56–1,61 m di quota (il tetto del campo lì è 1,77 m): le due condizioni della demo, prese da due file diversi, non stanno insieme (`conti.txt`). (2) La riga 158 del sorgente della proposta mette «si ferma dietro il pannello» e «mano sul sensore» sotto lo stesso esito «affidabilità persa». (3) In `risultati_a5c.txt` Q3c ha 0 falsi profondi ma 495 punti di bordo in 36 fotogrammi.

**Lunghezza della decisione.** Composta con pandoc e xelatex (A4, corpo 10, margini 1,8 cm): 5 pagine, l'ultima a tre quarti. Per stare nel limite la tabella dei requisiti R1–R8 è diventata un elenco in un paragrafo.

**Per rifare.** `python3 -I conti.py > conti.txt`; `gcc -O2 -o torneo_rifatto ../11-torneo/torneo.c -lm` e poi, uno alla volta, `timeout 120 ./torneo_rifatto scenB > rifatto_scenB.txt` (lo stesso per `pp`, `k102`, `scenC`; 10 s il più lungo). L'eseguibile non è conservato.
