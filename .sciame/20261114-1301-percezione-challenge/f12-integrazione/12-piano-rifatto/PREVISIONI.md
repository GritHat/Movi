# Previsioni del rovesciatore (f12, piano rifatto) — scritte PRIMA di aprire PIANO_14_4.md e i suoi risultati

Ora di scrittura: 2026-11-14T18:09:23+01:00. A quest'ora ho letto solo CONTRATTO_INTEGRAZIONE.md e l'elenco dei file (ls).
Non ho aperto PIANO_14_4.md, piano_mc.py, risultati_piano_mc.txt, né il codice da riusare.

| Sigla | Enunciato | Misura | Soglia di smentita |
|---|---|---|---|
| rov-P1 | Con ipotesi dure e dichiarate (integrazione, rilettura che fallisce, una persona ferma 2 h, coordinamento, pause, macchina lenta) la probabilità di chiudere il minimo dimostrabile entro l'ora 14 sta fra 0,35 e 0,70 | frazione di estrazioni Monte Carlo (programma mio, almeno 20 000 estrazioni) con fine del minimo ≤ 14,0 h | smentita se fuori da [0,35; 0,70]. Lettura per il piano: «regge» se ≥ 0,80; «non regge senza correzioni» se < 0,60 |
| rov-P2 | Il compito che decide non è il sensore ma l'integrazione di punta a punta (catena + schermo sulla stessa macchina) | compito con la massima correlazione di rango fra la sua durata e la fine del minimo, e massima frequenza sul percorso critico | smentita se il primo per criticità è un altro compito |
| rov-P3 | La catena Python di f10 da riusare sta fra 800 e 2500 righe di codice; le sue prove rilanciate passano in meno di 120 s | wc -l; time con timeout 120 | smentita se righe fuori intervallo, o prova che fallisce o supera 120 s |
| rov-P4 | «Riuso con un'ora di rilettura» NON è credibile per almeno una delle stime di riuso: più di 600 righe per ora di rilettura assegnata a una persona | righe da rileggere / ore assegnate dal piano | smentita se tutte le stime di riuso verificate stanno sotto 600 righe/ora |
| rov-P5 | Rovesciamento A (partire dalla catena Python di f10, nessuna riscrittura fino all'ora 5): la probabilità del minimo all'ora 14 sale di almeno 0,10 rispetto al calendario proposto sotto le stesse ipotesi dure | differenza fra due lanci del mio programma | smentita se la differenza è < 0,10 |
| rov-P6 | Rovesciamento C (tagliare del tutto il profilo sonoro): sposta la probabilità del minimo di meno di 0,05, perché il sonoro non è sul percorso critico | differenza fra due lanci | smentita se ≥ 0,05 |
| rov-P7 | Nell'ordine dei tagli del piano almeno un taglio tocca di nascosto la continuità visiva o la sicurezza (toglie una prova, una correzione c1–c8 o una condizione di VD che le regge) | lettura dell'ordine dei tagli contro V8 §4, VD F-401…F-413 | smentita se nessun taglio le tocca |
| rov-P8 | La mediana della fine del minimo nel mio modello duro supera di almeno 1,5 h quella dichiarata dal piano | differenza delle mediane | smentita se < 1,5 h |

Esiti possibili per ciascuna: regge, smentita, non risolta. Ciò che noto dopo va in fondo a PIANO_RIFATTO.md, separato.

## Esiti (scritti alle 2026-11-14T18:20:23+01:00, dopo le prove; file: risultati_rifai_mc.txt, prove_riuso.txt)

| Sigla | Esito | Numero |
|---|---|---|
| rov-P1 | **smentita** | 0,001 [0,001; 0,002] (stime mie, modello duro); 0,013 con le stime del piano; 0,370 solo con stime e modello del piano |
| rov-P2 | **regge** (con una riserva: K0 è la radice e sta sempre sul percorso) | PI: sul percorso critico 0,97, correlazione di rango +0,68, la più alta |
| rov-P3 | **regge** | 1 868 righe (1 327 + 541 di prove); 25 su 25 in 4,6 s nella struttura di f10; 2 errori su 25 se copiata senza 03-infrastruttura |
| rov-P4 | **regge** | B1: 487 righe Python + 635 di comp.c in 1,5 h = 748 righe l'ora (comp.c: 79 caratteri per riga); A1 571 righe l'ora, sotto soglia |
| rov-P5 | **smentita** | rovesciamento A alla lettera contro piano + F4: +0,076 leggero, +0,012 medio, +0,001 duro; il cancello dell'ora 5 costa (0,097 contro 0,262) |
| rov-P6 | **regge** | +0,000 nei tre modelli |
| rov-P7 | **regge** (lettura, non misura) | quattro punti: tagli 7, 8, 9 e il criterio di B3b (PIANO_RIFATTO §4) |
| rov-P8 | **regge** | mediana 29,0 h (duro) e 14,9 h (stime e modello del piano) contro 14,25 h: +14,8 h; con le stime del piano e il modello duro 23,0 h |

Notato dopo, non previsto: (1) il calendario alternativo senza cancello è stato disegnato dopo il secondo lancio; (2) la scala al
gelo (che cosa è nel tronco all'ora 12) è una misura scelta dopo aver visto che la probabilità binaria è vicina a zero;
(3) il modello «medio» è stato aggiunto dopo il primo lancio; (4) IDENTITA_SU_PROFONDITA.md è arrivata alle 18:18, a lavoro quasi chiuso.
