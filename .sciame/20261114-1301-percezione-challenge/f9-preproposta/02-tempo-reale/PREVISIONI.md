# Previsioni — `tempo-reale-f9` (scritte PRIMA delle prove)

Ora di scrittura: 2026-11-14T15:40:57+01:00 (`date -Is`, comando lanciato subito prima di questo file).
Nessuna simulazione né misura è stata lanciata prima di questo file. Ho letto: contratto f9, quinto addendum,
`prepropostaEsterna.md` per intero, `f5/02-audit/AUDIT.md`, `f3/H-012/02-validazione/VERIFICA.md` §3c (per `grep`),
`SOLUZIONE_V2.md` e `VERDETTO.md` (per `grep`), `proposta_sciame.tex` righe 60–135.

Macchina delle prove: portatile AMD Ryzen AI 9 HX 370, 24 fili, altri processi attivi (carico 0,96 all'inizio). NON è la
macchina di destinazione: i tempi misurati qui sono ordini di grandezza, non un bilancio.

## Modello dichiarato (ipotesi mie, non misure)

- Periodo del ciclo 66,7 ms (15 Hz). Tempo per ciclo = centro + deriva lenta AR(1) (σ 2 ms, τ 2 s) + rumore bianco (σ 3 ms) +
  punte rare (1,5 % dei cicli, +10…+30 ms) + salti di carico (±8 ms per 3–8 s, in media uno ogni 15 s).
- La configurazione ridotta costa Δ ms in meno della piena (Δ = 5, 12, 20): è questo l'anello di retroazione.
- Il selettore valuta a 2 Hz la media degli ultimi 15 cicli (come la preproposta: «1–2 Hz», «media sugli ultimi 15 cicli»).

## Previsioni

| # | Enunciato | Misura | Soglia di smentita |
|---|---|---|---|
| P1 | Senza isteresi (una soglia a 55 ms), centro 55 ms, Δ = 12: il selettore oscilla | cambi di configurazione al minuto | smentita se < 6/min (previsto ≥ 20/min) |
| P2 | L'isteresi temporale proposta (un cambio ogni 2,5 s al massimo) limita la frequenza ma non ferma l'oscillazione | cambi/min | smentita se < 6/min (previsto 12–24/min, tetto 24) |
| P3 | Due soglie 45/55: oscillazione persistente se Δ > 10 ms (la banda), quiete se Δ < 10 ms | cambi/min con Δ = 12 e Δ = 5, senza tempo minimo | smentita se Δ = 12 dà < 2/min oppure Δ = 5 dà > 6/min |
| P4 | In tutte e tre le varianti i cicli oltre 66,7 ms sono ≥ 1 % (≥ 9/min); un selettore corretto (percentile alto, discesa rapida, risalita lenta, costo previsto della configurazione di arrivo) ne dimezza il numero rispetto alla variante con isteresi temporale | quota di cicli > 66,7 ms | smentita se una variante della preproposta sta < 1 %, oppure se il corretto supera la metà della variante P2 |
| P5 | Caso stazionario con media 52 ms e rumore bianco σ 7 ms: il selettore sulla media non interviene (≤ 1 cambio/min) e i cicli fuori scadenza sono ≥ 1,5 % | cambi/min; quota di sforamenti | smentita se il selettore sulla media passa in ridotta per > 50 % del tempo, o se gli sforamenti sono < 1,5 % |
| P6 | Cambio di risoluzione della griglia (1°×0,1 m → 2°×0,2 m e ritorno): il ricampionamento «al centro» perde almeno una cella di possibile presenza; quello conservativo (una cella grossa è presenza se lo è una figlia) ne perde 0, gonfia l'area del 5–30 %, e dopo il primo giro è idempotente (10 giri = 1 giro) | celle di presenza perse; area dopo/prima; area dopo 10 giri | smentita se «al centro» perde 0 celle, o se il conservativo gonfia > 50 %, o se cresce a ogni giro |
| P7 | Compensazione della latenza (L = 155 ms), filtro q = 0,2 m²/s³, σ misura 3,4 cm, 15 Hz: a 1,4 m/s costanti l'errore RMS della posizione mostrata scende da ≈ 0,22 m (senza compensazione) a ≤ 0,06 m; a un arresto brusco la posizione compensata va oltre il vero di ≥ 0,10 m al picco (previsto 0,15–0,25 m) e resta oltre 0,10 m per ≥ 0,3 s | RMS in moto uniforme; picco e durata dell'errore dopo l'arresto | smentita se RMS > 0,08 m, o picco < 0,10 m |
| P8 | Ritaglio sulla griglia più aggiornamento dei pesi, 10 tracce × 2 ipotesi, griglia intera di 2610 celle (caso peggiore): mediana ≤ 1 ms in C (-O2, un filo); ≥ 20 ms in Python puro senza numpy | mediana, 99° percentile, massimo | smentita se C > 3 ms di mediana, o Python puro < 10 ms |
| P9 | La proiezione di un'immagine di profondità 848×480 sulla griglia polare in C costa ≤ 5 ms di mediana ed è almeno 3 volte il costo dei moduli della preproposta (P8 in C) | mediana | smentita se > 10 ms, o se < 3 volte P8 |

## Conti (non previsioni: aritmetica, li scrivo prima per confronto)

- Errore residuo di posizione con latenza stimata sbagliata di 30 ms: v·δ = 1,4 × 0,030 = 0,042 m; 2,5 × 0,030 = 0,075 m.
- Senza compensazione, con 155 ms: 1,4 × 0,155 = 0,217 m; 2,5 × 0,155 = 0,388 m.
- Margine 55 ms su 66,7 ms: 11,7 ms, cioè 17,5 % del periodo.

## Indipendenza dichiarata

Simulatori e conti sono miei: condividono con ciò che controllano l'autore (io), il modello linguistico e il modello del
tempo per ciclo scritto sopra, che è un'ipotesi e non una misura della macchina di destinazione. Valgono solo per i difetti
di logica del selettore e per gli ordini di grandezza; non valgono per i tempi veri.

## Previsione aggiunta DOPO la prima prova del selettore (ora: 2026-11-14T15:43:47+01:00)

(Nota di correzione, 15:45: in questo paragrafo due nomi di file fra apici rovesci erano stati mangiati dalla shell al
momento della scrittura; li ho rimessi a mano, il resto del testo e la tabella P10 sono quelli scritti prima del lancio.)

Notato dopo «risultati_selettore.txt»: nello scenario dell'attacco (centro 55 ms) il selettore corretto D sta in configurazione
ridotta per il 99,4 % del tempo, quindi il suo vantaggio sugli sforamenti coincide con «sempre ridotta». Per sapere se D
sa anche risalire scrivo, prima di lanciarla, una prova in più («sim_selettore_fasi.py»).

| # | Enunciato | Misura | Soglia di smentita |
|---|---|---|---|
| P10 | Carico a fasi lunghe (60 s con centro 42 ms, 60 s con centro 58 ms, alternate; Δ = 12; stesso rumore, punte e senza salti): D sta in configurazione piena per ≥ 35 % del tempo (ideale 50 %), con ≤ 2 cambi/min e con sforamenti ≤ quelli della variante B | % in piena, cambi/min, sforamenti % | smentita se D sta in piena < 35 %, o cambia > 2 volte/min, o sfora più di B |
