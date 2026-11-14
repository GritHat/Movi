# Previsioni di sciame-requisiti (f8, corsia A) — scritte prima delle prove

Scritte alle 2026-11-14T15:14:50+01:00 (`date -Is`). A quest'ora ho letto solo: il contratto f8, la traccia, gli addendum, SOLUZIONE_V2.md e VERDETTO.md. NON ho ancora aperto: f6-specializzazione, MISURE*.md, TORNEO*.md, la proposta .tex, i simulatori. Nessun calcolo eseguito.

| Id | Enunciato previsto | Misura | Soglia di smentita |
|---|---|---|---|
| P1 | Il documento per l'utente (`proposta/proposta_sciame.tex`) non contiene alcuna misura della qualità della previsione (errore per tempo senza osservazione, o copertura a livello dichiarato per tempo). | lettura integrale + `grep -n -i 'continuit\|copertura\|errore della prevision\|previs'` | smentita se trovo anche una sola riga con un errore di previsione o una copertura legati a un tempo senza osservazione ≥ 1 s |
| P2 | La specializzazione (`SPECIALIZZAZIONE.md`) e l'analisi del moto (`MOTO_PROPRIO.md`) non definiscono, per profilo, né un orizzonte di previsione né un criterio di accettazione sulla previsione (errore o taratura); al più trattano q o v_max come parametro. | lettura + grep | smentita se trovo, per almeno un profilo, una misura di accettazione dell'errore o della copertura della previsione durante l'occlusione |
| P3 | Con la regola della versione 2 (stato «previsto» lungo 0,40–0,70 s, poi «perso» assorbente) la quota dei cicli senza osservazione in cui è emessa una posizione più probabile con la sua regione è ≤ 60 % per un buio di 1,2 s, ≤ 25 % per 3 s, ≤ 15 % per 5 s. | conto: durata del «previsto» (dai file delle misure) / durata del buio, a 15 Hz | smentita se una delle tre quote supera la soglia; non risolta se nei file non trovo la durata del «previsto» per buio lungo |
| P4 | Il cerchio al 95 % del filtro [x,y,vx,vy] con q = 0,2 m²/s³, non vincolato, ha raggio > 3 m (tutta la griglia) prima di 4 s senza misura, e > 1 m prima di 1,5 s: da solo non dà «incertezza controllata» oltre 1–2 s. | conto in Python puro: propagazione di P con F, Q del modello a rumore bianco sull'accelerazione, P0 dallo stato stazionario a 15 Hz con R = (0,05 m)²; raggio = sqrt(5,991·λ_max) | smentita se il raggio a 4 s è ≤ 3 m o a 1,5 s è ≤ 1 m |
| P5 | Nessuna delle misure di accettazione R1–R8 della versione 2 misura la previsione fra la scomparsa e la ricomparsa (errore, copertura, larghezza): R3 misura solo l'identità al ritorno. Nei file di validazione (MISURE, MISURE_V2, MISURE_V2_bis) esiste al più una misura di «contenimento alla riemersione», non per tempo né per comportamento. | lettura + grep su 'copertura\|contien\|conten' | smentita se trovo una tabella copertura × tempo senza osservazione × comportamento nei file del ramo f4 |
| P6 | Verdetto complessivo atteso dell'audit: sulle parti esaminate (blocchi B1–B9, invarianti 1–9, misure R1–R8, regola «metà dell'ombra», verdetto, specializzazione, moto, demo, documento) NESSUNA parte è «rispettato» pieno sul criterio 1–4 del contratto f8; gli invarianti di sicurezza sono compatibili (non in conflitto) tranne al più due da riscrivere. | conteggio a fine audit | smentita se ≥ 2 parti risultano «rispettato» pieno sui controlli 1–4, oppure se ≥ 3 invarianti vanno riscritti |

Esiti possibili per ciascuna: regge, smentita, non risolta. Gli esiti vanno in CONSEGNA.md e in fondo a questo file, separati da ciò che è stato notato dopo.

## Aggiunta alle 2026-11-14T15:18:50+01:00 (dopo il conto A–C e la lettura degli ingressi, PRIMA del conto D)

A quest'ora conosco: i risultati A–C di `risultati_conto.txt`, TORNEO parte 2 e 3, MISURE_V2, SPECIALIZZAZIONE, MOTO_PROPRIO, la proposta v0.5. Il conto D non è ancora scritto né eseguito.

| Id | Enunciato previsto | Misura | Soglia di smentita |
|---|---|---|---|
| P7 | Falsificatore di `requisiti-2` (stato «previsto» a due gradi: «informativo» finché la regione al 90 % ritagliata sul cuneo copre meno dell'80 % del cuneo in griglia, poi «saturo» ma sempre mostrato). Con il solo cerchio del filtro (q = 0,2, σ = 5 cm), nella geometria della demo (pannello 1 m a 1,8 m, attore a 2,3 m, griglia 3 m): quota dei cicli di buio in grado «saturo» (a) transito a 1,2 m/s (buio 1,06 s): ≤ 10 %; (b) transito a 0,8 m/s (buio 1,60 s): 20–50 %; (c) sosta con buio di 5 s: ≥ 60 %. | conto D in `conto_requisiti.py`: r90 = sqrt(4,605)·σ_pos(t), centro = punto previsto a velocità costante | smentita di (a) se > 10 %; di (b) se fuori da 20–50 %; di (c) se < 60 %. Lettura: se (c) regge, con il solo filtro la continuità in sosta sarebbe quasi tutta «satura», cioè nominale: il requisito chiede un predittore che usi l'evidenza, oppure un'ombra più grande |

## Esiti (scritti alle 2026-11-14T15:22:55+01:00, dopo le prove)

- **P1 regge.** Nella proposta v0.5 la sola misura per «gestire le interruzioni della visibilità» è l'identità al ritorno (riga 126); nessun errore né copertura della previsione per tempo.
- **P2 smentita a metà.** `SPECIALIZZAZIONE.md`: nessun criterio sulla previsione (§3.3: «la durata del previsto non ha un valore proposto»). `MOTO_PROPRIO.md` invece ha il requisito Q5 (copertura dell'area prevista ≥ 0,90, con lo scostamento ammesso a 0,67, 1 e 2 s) e lo valuta per i due profili: è una misura di accettazione della copertura, quindi la previsione cade per quel file.
- **P3 regge sui file, superata di poco nel mio conto.** Con le durate misurate dalla validazione (0,40–0,53 s): 33–44 % a 1,2 s, 13–18 % a 3 s, 8–11 % a 5 s. Nel mio conto B la durata è 0,67–0,87 s; con rumore di 1,5 cm le quote sono 67–72 %, 27–29 %, 16–17 %, sopra le tre soglie; con 5 cm 56 %, 22 %, 13 %, sotto. La differenza fra il mio conto e le misure della validazione non è spiegata (nel mio mancano C6, il corpo largo e i rilevamenti mancati).
- **P4 regge.** Raggio al 95 %: 1,28–1,56 m a 1,5 s; 5,25–5,69 m a 4 s (3,46–3,83 m già a 3 s).
- **P5 regge.** Nel ramo f4 la sola misura affine è «contiene alla riemersione» (un tempo, un livello). In f2 (`TORNEO_parte2.md`) c'è una copertura a 1, 2 e 3 s e per manovra, ma a un solo livello, sul cerchio non ritagliato e senza larghezza.
- **P6 smentita alla lettera nella prima metà:** B2 e B6 risultano «rispettato» (compatibili senza modifiche): sono due parti. Nessuna delle parti che emettono o misurano la previsione è «rispettato». Seconda metà: regge di misura (due invarianti da riscrivere, il 6 e il 9; uno da estendere, l'8).
- **P7:** (a) regge, 0 %; (b) regge, 46 %; (c) mista: 83 % a 0,8 m/s, 31 % a 1,2 m/s (sotto la soglia del 60 %).

**Notato dopo, senza previsione:** in sosta, con l'ingresso a 1,2 m/s, la regione al 50 % del filtro ritagliata sul cuneo è vuota a 2 e 3 s (0 % del cuneo): il punto a velocità costante è uscito dall'ombra.
