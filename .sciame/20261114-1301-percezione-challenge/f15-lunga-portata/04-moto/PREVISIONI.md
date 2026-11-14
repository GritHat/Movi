# PREVISIONI — sciame-tracciamento, f15/04-moto

Scritte alle **2026-11-15T00:02:43+01:00** (uscita di `date -Is`), PRIMA di scrivere ed eseguire `movi_lp.py` e `prove_movi_lp.py`.
Tutto è simulazione o conto: niente è provato su un sensore fisico. Esiti possibili: regge, smentita, non risolta.

| id | misura | soglia di smentita |
|---|---|---|
| tracciamento-P1 | Regola del «libero» con radar Swerling 1 (Pd=0,9 a 5 km su 1 m², Pfa 1e-6), 5 passate, soglia Pd cumulata 0,99: una cella a 4 km in vista | smentita se risulta «libera» per il multirotore da 0,01 m², o se NON risulta «libera» per l'aereo da 20 m² |
| tracciamento-P2 | Stessa regola: distanza massima a cui la cella è «libera» per 0,01 m² in 5 passate (conto a mano: circa 2,36 km; in 1 passata circa 0,88 km) | smentita se il modulo dà valori fuori da ±5 % |
| tracciamento-P3 | Nessuna cella mai illuminata, o in ombra, o scaduta, risulta «libera» (controllo esaustivo su tutte le celle della griglia di prova) | smentita con 1 sola cella |
| tracciamento-P4 | Inseguitore a più modelli, radar 1 Hz + ottico 5 Hz + cooperativa 2 Hz, aereo in avvicinamento con virata: errore quadratico medio di posizione con fusione < del solo radar; con la cooperativa spenta a metà la traccia resta la stessa (0 cambi d'identità su 20 semi) | smentita se RMSE fuso >= RMSE solo radar, o se c'è 1 cambio d'identità |
| tracciamento-P5 | Due bersagli che s'incrociano a 100 m di quota di separazione, 20 semi: 0 scambi d'identità | smentita con >= 2 scambi su 20 (1 = non risolta) |
| tracciamento-P6 | Insieme di possibile presenza: contiene il 100 % di 2000 traiettorie simulate per classe con |v|<=v_max e |a|<=a_max a 5, 10 e 30 s; il treno resta sul binario | smentita con 1 sola uscita (è una proprietà del conto, non una frequenza) |
| tracciamento-P7 | Regione di previsione al livello 0,90 tarata su traiettorie SIMULATE (2000 di taratura, 2000 di prova per classe e orizzonte): copertura sulla prova con limite inferiore di Wilson al 95 % >= 0,87 in tutte le celle classe×orizzonte | smentita se una cella ha limite inferiore < 0,87 |
| tracciamento-P8 | «Nessuna etichetta riduce l'avviso»: il raggio dell'inviluppo >= raggio di ogni classe ammessa per ogni tau in 0..60 s a passi di 0,5 s e ogni v0 in griglia (controllo esaustivo sulla griglia) | smentita con 1 solo caso |
| tracciamento-P9 | Le prove girano in meno di 20 s in tutto | smentita se > 20 s |

Nota: P7 verifica la PROCEDURA di taratura su un generatore di manovre, non il mondo: su traiettorie pubbliche vere (ADS-B, registri di volo di droni) resta **non verificato** in questa cartella.

## Esiti (scritti DOPO le prove, alle 2026-11-15T00:16+01:00)

Comando: `timeout 120 <venv>/bin/python -I -u prove_movi_lp.py` (registri: `prove_prima_esecuzione.log`, `prove.log`; numeri: `risultati.json`).

| id | esito | prova |
|---|---|---|
| P1 | regge | a 4 km dopo 5 passate: «non osservato» per 0,01 m², «libero» per 20 m² |
| P2 | regge | 2360 m in 5 passate, 877 m in 1 passata; dalla griglia 2300 m (un anello in meno per la regola delle celle vicine) |
| P3 | regge (verificato sulla griglia di prova) | 0 celle «libere» senza diritto su 12 960 controlli |
| P4 | **smentita alla prima esecuzione**, poi regge dopo una correzione | prima: 37 cambi d'identità su 20 semi, tracce doppie (1 o 2 confermate). Causa trovata: le misure appena fuori dalla porta al 99,9 % (7 su circa 8400, cioè la frequenza attesa) aprivano una traccia doppia. Correzione, notata DOPO: «porta del dubbio» (quantile 1−1e-6) e tracce tentative che scadono. Rifatta su 40 semi (i 20 di prima più 20 nuovi, 1000–1019): 0 cambi, 1 traccia; RMSE 39,9 m solo radar contro 4,4 m fuso, migliore in 40 semi su 40 |
| P5 | **smentita alla prima esecuzione**, poi regge dopo la stessa correzione | prima: 30 scambi, 7 semi su 20. Dopo, su 40 semi (20 nuovi): 0 semi con scambio, Wilson 95 %: 0–0,088 |
| P6 | regge | 0 uscite su 60 000 |
| P7 | regge, di misura | limite inferiore di Wilson peggiore 0,8703 (soglia 0,87), 40 celle, n = 2000 ciascuna; traiettorie SIMULATE |
| P8 | regge (verificato sulla griglia) | 0 casi su 27 951 |
| P9 | **smentita** | 34,5 s (soglia 20 s): le prove non girano «in pochi secondi»; il grosso è P4–P5 (120 inseguimenti da 60 s) |

Notato dopo, non previsto: (a) la prima stesura cumulava le passate per 5 s qualunque fosse la classe: per un oggetto veloce è sbagliato (cambia cella fra due passate). Corretto prima della consegna: finestra per classe = min(5 s, lato della cella / v_max) e minimo sulle celle vicine. (b) Con questa regola il radar segnaposto dà «libero» per l'aereo di linea fino a 10,6 km (2 passate), non 15,8 km.
