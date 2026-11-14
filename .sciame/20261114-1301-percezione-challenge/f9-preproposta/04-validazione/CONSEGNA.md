# Consegna — `sciame-validazione`, f9: banco indipendente su S3 + S4 e attacchi 1, 2, 5

**In testa.** Lavoro dalle 2026-11-14T15:38:49+01:00 alle 16:20 (`date -Is`). Previsioni scritte alle 15:45:56, prima del codice: `PREVISIONI.md` (in fondo gli esiti). **Esito: S3 + S4 come sono scritte non reggono (controesempio: il transito normale a 1,2 m/s); una forma corretta dà una stima per tutta l'occlusione, ma dopo circa 1 s quella stima vale quanto «è nell'ombra».** Tutto è **simulazione in pianta, a sensore fermo**.
**Cambi di stato:** delle mie otto previsioni due sono smentite (P3: la regola σ_eff con Na e con il pannello da 2 m; P8) e quattro reggono solo in parte (P1, P4, P6, P7). **Scostamenti.** (1) **Difetto del mio banco, trovato dopo i primi risultati e corretto alle 15:58:** le tracce tentative passavano davanti a quelle in occlusione; tutti i lanci sono rifatti e i primi file sovrascritti (le tabelle (b), (c), (e) già viste non sono cambiate). (2) Misure aggiunte **[dopo]**, senza previsione: identità a fine prova, confronto con il solo filtro e con il «centro del cuneo», tempi, «falso libero», velocità tripla per velocità d'ingresso. (3) Il contratto f9 chiede su S2–S5 un parere senza banco; la consegna chiede il banco: ho seguito la consegna. (4) Nessuna fonte in rete aperta: nessuna affermazione ne dipende. (5) Niente `stato.md`. (6) Lunghezza al limite delle tre pagine (circa 2600 parole, tabelle comprese). **Regole violate:** nessuna nota.
**Rifare:** `sh rifai.sh` (41 lanci con `timeout 120`, circa 12 minuti; semi fissati; `banco_s3s4.c`, md5 `ca89b51b…`; uscita identica al rilancio, tolta la riga dei tempi); tabelle: `python3 estrai.py ris_*.txt`.

## 1. Il banco e le letture

Sensore in (0,0), campo ±43,5°, 15 Hz, «libero» solo fra 1,24 e 3,0 m. Pannello da 1 m a 1,8 m, soggetto (disco di raggio 0,20 m) sulla linea a 2,3 m; pannello da 2 m a 2,2 m, soggetto a 2,6 m, portata 3,8 m (fuori dal dominio del nucleo). Misura: il centro, solo a corpo tutto visibile (C6), rumore di 3 cm, Pd 1 e 0,9; filtro del nucleo. Nove comportamenti, 400 passaggi ciascuno, 0,3–1,8 m/s. **Letture dove il testo è ambiguo:** pesi **W1** = moltiplicati per f a ogni ciclo (la lettera), **W2** = dal peso iniziale, μ ∝ μ(0)·f(t); celle ammesse **Na** = ombra e ogni «non osservato», **Nb** = sola ombra; α = d/(d + |v|·dt), cioè H2 si ferma al centro dell'ombra (con α = 0,90 fisso il transito cambia poco: 74,8 % contro 76,4 % in (c), `ris_05`); σ_eff = raggio quadratico medio della miscela ritagliata; «95 %» = disco di raggio 2σ_eff, e a parte la regione di massima densità al 95 %.

## 2. Verdetti proposti

| Voce | Verdetto proposto | Prova |
|---|---|---|
| **S3**, due ipotesi | **approvata con correzioni** (§5), come strato d'informazione; la taratura è **da provare sull'hardware** | corretta (W2, Nb): stima mostrata nel 99,8 % dei passaggi per tutta l'occlusione (nucleo: 0,2 %); sosta: errore mediano 0,09 m a 2 s contro 1,36 m del solo filtro (`ris_04`) |
| **S4.1**, ritaglio a zero sul «libero» | **approvata con correzioni**: è già l'invariante 4 del nucleo; serve la fascia di guardia e non lo zero secco | 0 celle «libero» nella regione su 48 279 fotogrammi (per costruzione); ombra stimata 10 cm troppo larga: regione su celle davvero libere in 400 passaggi su 400 (`ris_11`); un fotogramma di falso «libero» sul cuneo azzera la stima in 289 passaggi su 400 (`ris_16_falso1_W1_Nb`) |
| **S4.2**, pesi «a ogni ciclo» | **respinta** nella forma scritta | transito normale a 1,2 m/s: sosta dominante prima della ricomparsa nell'84,4 % (Na) e 97,0 % (Nb) dei passaggi; errore mediano alla ricomparsa 0,85–0,97 m con ±0,56–0,37 m dichiarati (`ris_10_att1_prosegue_W1_*`) |
| **S4.3**, «previsto» finché σ_eff ≤ 0,8 m | **respinta** | pannello da 1 m, Nb: 0 passaggi a «perso» su 3600, anche dopo 8 s di sosta (σ_eff 0,45–0,50 m: è tutta l'ombra); con Na «perso» a 1,7 s nel 38 % dei transiti; pannello da 2 m, Nb: «perso» a 2,4 s nel 95,5 % dei transiti (`ris_03`, `ris_01`, `ris_09`) |
| **Attacco 2**, porta χ² per l'identità | **respinta** come regola d'identità; resta il riaggancio geometrico del nucleo | scambio muto 234 volte su 291; «torna indietro»: identità tenuta 63,8 % (geometrico: ammesso 100 %) |

## 3. Le misure chieste

**(a) Attacco 1** (1,2 m/s, sosta di colpo a metà pannello; `ris_10_att1_ferma_*`). Regione «previsto» su celle «libero»: **0 fotogrammi** con l'ombra esatta: è un controllo della costruzione, non un dato; il braccio senza ritaglio fallisce come deve (399 passaggi su 399, `ris_13`). Il disco ±σ_eff tocca «libero» nello 0,0–0,1 % dei fotogrammi con Nb, nel 14,4–21,5 % con Na. **Sosta dominante:** W1 a 1,13 s, cioè **0,22–0,26 s prima** del momento (1,40 s) in cui chi prosegue torna visibile; W2 con Nb a 1,40 s, +0,06 s (5 %: −0,01; 95 %: +0,10); **W2 con Na: mai (0 su 399)**.
**(b) Richiesta 2** (errore mediano / σ_eff mediana in metri; quota dentro 2σ_eff).

| Comportamento, lettura | 0,5 s | 1,0 s | 1,5 s | 2,0 s | 3,0 s |
|---|---|---|---|---|---|
| prosegue, W2 Nb | 0,10 / 0,24 · 100 % | 0,20 / 0,40 · 100 % | 0,26 / 0,46 · 100 % | 0,36 / 0,49 · 100 % | 0,46 / 0,50 · 100 % |
| prosegue, W1 Na | 0,10 / 0,24 · 100 % | 0,23 / 0,43 · 97,5 % | 0,39 / 0,72 · 99,0 % | «perso» nell'86 % | «perso» nel 100 % |
| sosta a metà, W2 Nb | 0,10 · 100 % | 0,15 · 100 % | 0,10 · 100 % | 0,09 · 100 % | 0,09 / 0,47 · 100 % |
| lato lontano, W2 Nb | 0,09 · 100 % | 0,23 · 85,7 % | 0,72 · 56,4 % | 1,19 · 40,6 % | 1,84 / 0,47 · **23,1 %** |
| velocità tripla, W2 Nb | 0,23 / 0,23 · **69,0 %** | 0,28 · 92,3 % | 0,39 · 100 % | 0,56 · 100 % | — |

Dentro 1σ_eff, «prosegue» con W2 e Nb: 97,5 → 94,8 → 80,8 → 70,3 → 58,8 %. **L'errore non resta dentro l'incertezza dichiarata per ogni comportamento** (`ris_01`, `ris_04`).
**(c) Attacco 5**, alla ricomparsa, 0,3–1,8 m/s, intervallo di Wilson al 95 %. Dentro 2σ_eff / dentro la regione al 95 %:

| Lettura | prosegue | rallenta | ferma e riparte | torna indietro | tripla |
|---|---|---|---|---|---|
| W1 Na (lettera; «prosegue»: 246 con stima, 153 già «perso») | 76,4 [70,7; 81,3] / 78,5 | 42,9 [36,5; 49,5] / 21,2 | 72,9 [65,0; 79,5] / 52,1 | 46,1 [40,1; 52,2] / 23,0 | 21,7 [17,6; 26,4] / 18,7 |
| W1 Nb, n = 399 | 49,6 [44,7; 54,5] / 45,4 | 57,4 / 34,6 | 83,5 / 49,1 | 51,4 / 38,1 | 26,0 / 4,0 |
| W2 Nb, n = 399 | **100 [99,0; 100]** / 99,7 | 98,0 [96,1; 99,0] / 99,2 | 91,7 [88,6; 94,1] / 74,4 | **46,6 [41,8; 51,5]** / 26,8 | **27,2 [23,1; 31,8]** / 14,0 |

Con W2 e Nb, «prosegue»: errore mediano 0,65 m, etichetta ±0,54 m, dentro 1σ_eff solo il 16,8 % [13,4; 20,8]. Replica con un altro seme: dentro gli intervalli (`ris_14`). I 30 passaggi reali: **non eseguibili oggi**.
**(d) Attacco 2.** Velocità tripla: porta violata nello 0 / 18,5 / 94,2 / 100 % dei casi a 0,6 / 0,9 / 1,2 / 1,8 m/s d'ingresso (`ris_15`). A porta violata nasce una traccia nuova e la possibile presenza resta (per costruzione), ma **la traccia vecchia resta «previsto» dentro l'ombra fino a fine prova in 209 casi su 209**: una persona, due oggetti a schermo. Uno entra e due escono (`ris_04`): il mai visto esce per primo in 291 passaggi su 400; **l'identità passa a lui senza alcun segnale in 234** (la porta non è violata: il conflitto non scatta); con il primo ancora nascosto la possibile presenza cade in 139 passaggi (1398 fotogrammi). Ferma e riparte **[dopo]**: porta rispettata al 100 %, ma identità a fine prova 92,2 %: riagganciato sullo stato di H2, il filtro perde di nuovo il soggetto.
**(e) Continuità.** Passaggi con una stima per tutta l'occlusione, «prosegue»: 99,8 % (Nb; 97,8 % con Pd 0,9), 62,8 % (W1, Na), 19–21 % (pannello da 2 m). Si passa a «perso» solo per σ_eff > 0,8 m: mai con 1 m e Nb; a 1,67 s (transito) e 3,17 s (sosta) con Na, perché la massa di H1 finisce sul «non osservato»; a 2,38 s con 2 m. Con Pd 0,9 lo 0,6–1,8 % dei fotogrammi non ha traccia (difetto d'ingresso del nucleo, K-014).
**(f) Confronto col nucleo, stessa scena.** L'area del nucleo è mostrata nel 99,8 % dei casi a 0,5 s e nel 6,3 % a 1,0 s; copre tutta l'occlusione nello 0,2 % dei passaggi; finché c'è contiene il soggetto in transito (100 %). **[dopo]** Sul transito il punto del solo filtro è più vicino al vero della miscela ritagliata: 0,156 contro 0,204 m a 1 s, 0,265 contro 0,363 m a 2 s; sulla sosta vince la miscela (0,09 contro 1,36 m a 2 s), che però vale quanto il punto fisso «centro del cuneo» (sosta in un punto a caso: 0,20 contro 0,22 m). Dal primo secondo in poi la regione al 95 % copre più di metà del cuneo nel 94,8–100 % dei fotogrammi: per la regola del nucleo sarebbe già «perso».

**Criteri di rigetto della preproposta.** *Attacco 1, celle libere:* **non scattato** con l'ombra esatta (per costruzione); **scattato** con l'ombra stimata 10 cm troppo larga. *Attacco 1, μ1 dominante oltre l'uscita attesa:* **non scattato** con W1 e con W2-Nb; **scattato** con W2-Na e, a velocità miste, con W1-Na (sosta dominante in 305 passaggi su 399). W1 lo supera per il motivo sbagliato: dichiara la sosta anche a chi prosegue. *Attacco 2:* **scattato** (234 identità forzate senza segnale). *Attacco 5:* **scattato** nella lettera (76,4 %; 49,6 %); con W2-Nb passano solo «prosegue» e «rallenta». *Richiesta 2:* **non soddisfatta** (lato lontano, tripla, ritorno).

## 4. Critiche numerate

1. **I pesi «a ogni ciclo» contano la stessa evidenza quindici volte al secondo.** f(t) è già la probabilità cumulata di «non ancora visto»; moltiplicarla a ogni fotogramma senza troncare la gaussiana porta μ1 a 0,09 alla ricomparsa di un transito regolare (traccia: dopo la compilazione di `rifai.sh`, `./banco -np 1 -beh 0 -v 1.2 -trace 0`), e la posizione mostrata si ferma a metà ombra.
2. **«(o non osservato contigue)» decide il risultato e non è definito.** Con Na la regola finisce a «perso» in 1,4–3,2 s e con W2 la sosta non vince mai; con Nb non finisce mai.
3. **La soglia di 0,8 m non è legata all'ostacolo.** Con l'ombra larga 1,3 m σ_eff si ferma a 0,45–0,50 m (mediana; mai oltre 0,8 in 3600 passaggi); con una larga 2,4 m supera 0,8 durante un transito normale.
4. **L'attacco 1 è il caso che H2 assume** (sosta al centro dell'ombra). Fuori dal modello: lato lontano 23 % dentro 2σ_eff a 3 s con 1,84 m d'errore; ritorno 47 % alla ricomparsa.
5. **Alla ricomparsa l'errore è strutturale, e «±σ_eff» non è una precisione.** Il soggetto riappare dove il sensore vede, cioè dove il ritaglio ha messo zero (0,65 m nella lettura migliore); dopo 1 s σ_eff è la semilarghezza dell'ombra: copre al 100 % perché dice «è nell'ombra».
6. **La porta χ² cresce con l'incertezza:** dopo un'occlusione lunga accetta chiunque, dopo una corta respinge il soggetto giusto che ha cambiato passo. Il fantasma «previsto» non ha una regola che lo chiuda.
7. **Lo zero secco non perdona:** un fotogramma di falso «libero» azzera la massa (289 su 400) o, con W1 e Na, uccide l'ipotesi sosta (dominante in 202 passaggi su 399 invece di 305; con tre fotogrammi, 25).

## 5. Dove la preproposta ha letto male, e la versione corretta

**Letture sbagliate.** (i) «Interrompe la previsione a 0,5 s»: nel nucleo non c'è un timer, c'è la regola «metà del cuneo»; qui dura fra 0,5 e 1,0 s. (ii) «Pannello da 1 m, durata 0,7–2,0 s»: a 2,3 m l'ombra è larga 1,28 m e con il corpo di 40 cm la misura manca per 1,68 m di cammino: 1,40 s a 1,2 m/s (misurato), 1,2–3,4 s fra 1,4 e 0,5 m/s (conto). (iii) «INV-3» e «INV-5» non esistono nel v0.5; nella soluzione versione 2 la possibile presenza è l'invariante 7 e la massa il 9. (iv) Il ritaglio sul «libero» non è nuovo: è l'invariante 4, **con** la fascia di 0,40 m che la preproposta omette. (v) «Sotto 1,1 m» nel v0.5 è una **distanza dal sensore**, non una quota: riguarda S10, lo segnalo soltanto.

**Versione corretta (`validazione-f9-1`).** (1) Due ipotesi come scritte, α = d/(d + |v|·dt). (2) Pesi **non cumulati**, μ_i(t) ∝ μ_i(0)·f_i(t), con f sulla sola ombra più la fascia di guardia; una cella conta «libero» solo se vista libera per 3 fotogrammi; mai massa a zero secco (pavimento ε). (3) Tre livelli a schermo: **punto** con raggio al 95 % finché la regione copre meno di metà del cuneo (qui 0,5–1 s), e il punto è quello del solo filtro; poi **zona**, senza punto né metri; sotto, sempre, la possibile presenza. Niente «±σ_eff». (4) Identità con il riaggancio geometrico del nucleo; la possibile presenza si rilascia **solo cella per cella**, mai per riaggancio; al riaggancio si reinizializza la covarianza della velocità. (5) Il raggio dichiarato viene dalla copertura misurata sulle registrazioni, per comportamento. *Previsione:* falsa sosta sul transito sotto il 10 % (misurato: 2,5–6,5 %); copertura del «punto» ≥ 28 su 30 passaggi reali. *La smentisce:* falsa sosta oltre il 30 %, o al più 22 su 30.

## 6. Costo

Calcolo: **in media 46–110 microsecondi per traccia in occlusione e per ciclo** sui lanci completi (C, `-O2`, griglia 160 × 96 celle da 5 cm, regione al 95 % compresa; massimo osservato 4,3 ms, con altri processi attivi: tempi indicativi), cioè lo 0,07–0,17 % di un ciclo a 15 Hz. In Python puro: **non misurato**. Lavoro, **stima mia non verificata**: 6–8 ore-persona per la versione corretta; sostituisce il cerchio ritagliato di B5 (circa 2 delle sue 9 ore): **4–6 ore nette**. Nel taglio a 24 ore non entra insieme a S6, S8 e S11: per farle posto si toglie il ramo dell'etichetta (B6, 4 ore).

## 7. Che cosa il banco condivide, e che cosa resta non verificato

**Condivide con la proposta, quindi non esclude difetti lì:** la specifica (le mie letture del testo), il modello linguistico (che ha scritto anche i pedoni), il rumore gaussiano con R noto al filtro, l'ombra geometrica ideale, le celle calcolate dalla geometria e non da una profondità. **Non verificato:** ogni cifra sulla camera vera; i falsi rilevamenti; l'occlusore mobile; S2 e S5; la versione corretta come insieme (provati solo W2 e Nb; fascia, pavimento ε e rilascio cella per cella non simulati); il costo in Python e le ore. **Prova che decide:** i 30 passaggi e le 20 soste già previsti per il nucleo, giudicati sulle registrazioni, con in più 10 ritorni e 10 uscite dal lato lontano, contando per comportamento i casi dentro la regione dichiarata.

**Stati proposti.** «S3 + S4 alla lettera tengono l'errore dentro l'incertezza dichiarata»: **smentito** in simulazione. «Il ritaglio non mette mai il previsto sul libero»: vale per costruzione con l'ombra esatta, **smentito** con +10 cm. «La forma corretta dà continuità per tutta l'occlusione»: **sostenuto dai dati** in simulazione (99,8 %), **non risolto** sul vero. «La precisione dichiarata è realistica»: **non risolto**; in simulazione vale solo per chi prosegue, rallenta o sosta.
