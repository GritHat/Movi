# Previsioni di sciame-inferenza (f8, corsia A) — scritte PRIMA di ogni prova

Ora di scrittura: 2026-11-14T15:20:25+01:00 (`date -Is`). A quest'ora non esiste ancora nessuno script in questa cartella.

**Scena della prova (mia, riscritta dal solo testo del torneo; nessun codice altrui).** Sensore in (0,0), campo ±43,5°, portata 6 m, pannello a 2 m largo 1 m, pedone a circa 4 m che attraversa a 1,0–1,5 m/s, 15 Hz, rumore 5 cm, Pd 0,9. Celle da 0,1 m. Evidenza negativa solo oltre una fascia di 0,2 m dal bordo dell'ombra.
**Modello di credenza M\* (uguale per tutti gli algoritmi, fissato qui, non tarato sui dati della prova):** velocità quasi costante con q = 0,2 m²/s³; sosta con tasso 0,25/s e ripartenza 0,4/s con la velocità di prima; inversione con tasso 0,1/s. **Oracolo:** filtro a particelle su M\* con 40 000 particelle, due semi (il tetto del rumore dell'oracolo si misura fra i due semi).
**Candidati:** (PF) particelle N = 100, 250, 1000, 4000, ricampionamento multinomiale a ogni ciclo oppure sistematico sotto N/2 efficaci, regione grezza oppure lisciata 3×3; (IST) istogramma posizione × velocità discreta (passo 0,5 m/s, reticolo 7×7 più un modo «fermo»), aggiornato per traslazione e diffusione; (MG) miscela di 4 gaussiane (va, fermo, torna, fermo-dopo-inversione) con momenti ricorsivi, troncata sulle celle non viste **senza memoria** (solo il vincolo del ciclo corrente); (NUCLEO) cerchio al 95 % del Kalman ritagliato, mostrato finché copre meno di metà del cuneo.
**Regione al livello p:** insieme di massima densità sulle celle non viste libere, sulla distribuzione **rinormalizzata** su quelle celle.

| # | Misura | Previsione | Smentita se |
|---|---|---|---|
| P1 | Massa dell'oracolo (condizionata a «ancora nascosto») dentro il cerchio «95 %» ritagliato del nucleo, mediana sulle condizioni iniziali, a 1 / 2 / 3 s | < 0,85 in almeno un istante (ritagliare senza rinormalizzare cambia il livello); limite a mano: 1 − q ≤ (1 − p)/G(S), con G(S) la massa gaussiana rimasta nelle celle ammesse | ≥ 0,90 in tutti e tre gli istanti |
| P2 | Intersezione su unione (IoU) fra due semi della regione al 90 % grezza delle particelle, a 2 s | N = 250: < 0,50; N = 1000: < 0,70; N = 4000: ≥ 0,70 | N = 250 ≥ 0,60, oppure N = 4000 < 0,60 |
| P3 | Lo stesso con lisciatura 3×3 e ricampionamento sistematico, N = 1000; tremolio fra cicli successivi (celle cambiate / unione) | IoU fra semi ≥ 0,75; tremolio ≤ 2 volte quello di MG | IoU < 0,65 oppure tremolio > 3 volte |
| P4 | Livello vero della regione «90 %» grezza delle particelle (massa dell'oracolo dentro), a 2 s | N = 250: ≤ 0,80 (troppo sicura); N = 4000: ≥ 0,85 | N = 250 > 0,85 oppure N = 4000 < 0,80 |
| P5 | Sistematico-sotto-soglia contro multinomiale-a-ogni-ciclo, N = 1000, IoU fra semi (grezza) | guadagno fra +0,03 e +0,15 | guadagno < +0,03: il ricampionamento non è la leva |
| P6 | MG: massa dell'oracolo nella sua regione al 90 %; IoU con la regione al 90 % dell'oracolo; istanti 0,5–5 s, mediane | massa fra 0,80 e 0,97 in ogni istante; IoU ≥ 0,60 | un istante fuori dall'intervallo, o IoU < 0,50 |
| P7 | IST: come P6 | massa fra 0,82 e 0,96; IoU ≥ 0,65 | fuori dall'intervallo, o IoU < 0,55 |
| P8 | Tempo per ciclo e per oggetto, Python puro (indicativo, macchina condivisa) | PF 1000: 1–4 ms; PF 4000: 4–16 ms; MG: 2–8 ms; IST: 25–90 ms. Dieci oggetti in 66,7 ms: PF 1000 e MG sì, IST no | un valore fuori dall'intervallo di un fattore 2 |
| P9 | Punto mostrato, passo massimo fra due cicli (su MG e IST): media a posteriori contro massimo a posteriori (cella più probabile) | media: ≤ 0,20 m in tutte le sequenze; massimo: > 0,30 m almeno una volta in ≥ 50 % delle sequenze | media > 0,20 m in una sequenza; massimo < 20 % delle sequenze |
| P10 | Falso «vuoto»: soggetto riemerso e non rilevato per k = 5 cicli; massa entro 0,5 m dal vero | Pd 0,9 nominale: < 1 %; Pd temperata a 0,5: fra 1 e 20 %; miscela «sensore cieco su questo oggetto» con probabilità 0,05: ≥ 1 %; particelle N = 1000 nominali: nessuna particella entro 0,5 m in ≥ 50 % dei casi | nominale ≥ 5 %; miscela < 1 % |
| P11 | Copertura della regione al 90 % di MG contro il MIO generatore (sei comportamenti; indicativa: generatore e predittore hanno lo stesso autore) | complessiva fra 0,85 e 0,97 a 1–3 s; «esce dal lato lontano» < 0,70 a 3 s | complessiva fuori; «lato lontano» ≥ 0,85 |
| P12 | Quota dei cicli nascosti (fino a 5 s) in cui il NUCLEO emette una regione | < 30 % | ≥ 50 % |

Esiti possibili: regge, smentita, non risolta. Ciò che noto dopo le prove lo marco **[dopo]** in CONSEGNA.md.

**Scostamento, scritto alle 2026-11-14T15:25:19+01:00 dopo `tempi` e `oracolo` a 40 000 (nessun confronto ancora visto).** Con 40 000 particelle il tetto del rumore dell'oracolo è 0,80–0,97 di IoU fra i due semi (`risultati_oracolo_40k.txt`): troppo vicino alle soglie di P6 e P7. Porto l'oracolo a 200 000 particelle per seme (NORA=200000); le previsioni P1–P12 non cambiano. I tempi (P8) erano già stati visti quando ho scritto questa nota.
Il lancio a 200 000 è stato fermato da `timeout 120` all'ottava serie su dieci (`risultati_oracolo_200k_interrotto.txt`; `oracolo.json` non riscritto). Alle 2026-11-14T15:27:26+01:00 rilancio con NORA=120000.

## Seconda serie — scritta alle 2026-11-14T15:33:19+01:00, DOPO aver visto `risultati_{tempi,oracolo,det,pf,copertura,falso,copertura_ist}.txt` e PRIMA di scrivere `inf2.py`

Sono prove esplorative nate dai primi esiti: le previsioni sono cieche rispetto alle prove nuove, non rispetto alle prime.

| # | Misura | Previsione | Smentita se |
|---|---|---|---|
| P13 | MG più un quinto componente «svolta» (tasso 0,15/s da «va»; media a metà del tratto a velocità costante, deviazione v·t/2 lungo la marcia e v·t/√6 di lato), stesse 30 condizioni iniziali e stesso generatore: copertura della regione al 90 % a 2 s | «svolta» ≥ 0,65 (era 0,40); «lontano» ≥ 0,50 (era 0,18); gli altri quattro ≥ 0,95; area90/ombra a 2 s ≤ 0,90 (era 0,62) | «svolta» < 0,50, o «lontano» < 0,35, o area > 0,95 |
| P14 | IST con passo di velocità 0,25 m/s (13×13 + 1 = 170 modi): massa dell'oracolo nella regione al 90 % a 0,5 e 1 s (era 0,50 e 0,55) | ≥ 0,75 a tutti e due gli istanti; tempo per ciclo fra 40 e 80 ms | < 0,65 a 0,5 s |
| P15 | PF N = 1000 sistematico con due passate di lisciatura 3×3: IoU fra semi a 2 s (era 0,75), massa dell'oracolo (era 0,871), tremolio (era 0,134) | IoU ≥ 0,82; massa ≥ 0,88; tremolio ≤ 0,11 | IoU < 0,78 |
| P16 | Falso «vuoto» lungo: k = 10 e 15 cicli; massa entro 0,5 m dal vero | nominale < 0,0001 a k = 10; miscela «sensore cieco» ≥ 0,005 a k = 10 e a k = 15 (ha un pavimento); temperata < 0,001 a k = 15 | miscela < 0,002 a k = 15 |
| P17 | MG con (a) supporto limitato alle celle non viste **connesse** all'ombra d'ingresso e (b) peso dei componenti «va» e «torna» limitato dal minimo nel tempo della loro massa ammessa (euristica: P(sempre nascosto) ≤ min nel tempo di P(nascosto)): contro l'oracolo a 3 s | area ≤ 5,5 m² (era 7,27; oracolo 4,07); IoU ≥ 0,70 (era 0,56); massa dell'oracolo fra 0,86 e 0,95 in ogni istante da 2 s | massa < 0,85 in un istante (l'euristica stringe troppo), o IoU < 0,62 |
| P18 | Regione al 90 % con due o più pezzi che portano ciascuno ≥ 20 % della massa (il caso «due ipotesi»), sui cicli delle 5 condizioni iniziali | MG: < 10 % dei cicli; PF N = 4000 lisciata: < 10 %; PF N = 250 grezza: > 50 % (falsi «due ipotesi» da rumore) | MG ≥ 25 %; PF 250 grezza < 25 % |

## Terza serie — scritta alle 2026-11-14T15:36:09+01:00, dopo la seconda serie e prima della correzione

**Difetto mio in IST.** `ist_run` inizializza la velocità sui soli due nodi del reticolo vicini alla stima e ignora la varianza di velocità del Kalman (l'oracolo e MG la usano). P14 è caduta (0,545 a 0,5 s anche con passo 0,25): il difetto è dell'inizializzazione, non del passo. Correggo: tre nodi per asse con media e varianza uguali a quelle del Kalman (quando il reticolo lo permette).
| P14b | IST corretto: massa dell'oracolo nella regione al 90 % a 0,5 e 1 s, passo 0,5 e passo 0,25 | passo 0,5: ≥ 0,75 a tutti e due gli istanti, ma il massimo a posteriori salta ancora di oltre 1 m in ≥ 3 sequenze su 5 (pettine); passo 0,25: ≥ 0,82 | passo 0,5 < 0,65 a 0,5 s |

## Quarta serie — scritta alle 2026-11-14T15:38:40+01:00, dopo `risultati3_*` (P14b smentita: 0,559 e 0,619 a 0,5 s) e prima di `inf3.py`

| P19 | Ellisse contro insieme di massima densità, sull'oracolo: ellisse dei momenti della distribuzione condizionata, allargata fino a contenere davvero il 90 % della massa, poi ritagliata sulle celle ammesse; a 2 e 3 s | area dell'ellisse ritagliata / area dell'insieme di massima densità fra 1,10 e 1,50; quota dell'ellisse NON ritagliata su celle viste libere fra 10 e 40 % | rapporto < 1,05 (l'insieme di massima densità non guadagna niente) |
| P20 | Ciclo completo per dieci oggetti nascosti insieme, Python puro: particelle N = 4000 sistematico, due lisciature 3×3, regioni al 50 e al 90 %, media | fra 20 e 35 ms per ciclo (su 66,7 disponibili) | > 50 ms |
