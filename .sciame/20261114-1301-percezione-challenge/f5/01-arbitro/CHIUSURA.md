# Chiusura della convocazione «percezione-challenge» (`sciame-arbitro`, fase f5)

14 novembre 2026, scritta fra le 18:55 e le 19:10 (`date -Is`). Percorsi relativi a `.sciame/20261114-1301-percezione-challenge/`. Il verdetto completo, con i riconteggi, è `f12-integrazione/30-arbitro/VERDETTO_INTEGRAZIONE.md`; qui c'è solo la chiusura secondo la pipeline. **Tutto ciò che la convocazione ha prodotto è simulazione, conto o lettura di schede tecniche, a sensore fermo: nessun fotogramma di una camera della squadra è passato da una prova. «Chiuso» non vuol dire «validato».** Questo file è identico in `f5/CHIUSURA.md` e in `f5/01-arbitro/CHIUSURA.md`.

## 1. L'ipotesi provata, e in che senso

**H-012, riformulata nella versione 3** (`f12-integrazione/20-finale/SOLUZIONE_V3.md` più `f14-classificazione/20-inclusione/BLOCCO_CLASSIFICAZIONE.md`), **è provata solo in simulazione, a sensore fermo**, clausola per clausola:

- **(a) Continuità.** Per ogni persona vista almeno 4 fotogrammi che entra nell'ombra di un ostacolo fermo, a ogni ciclo esce una zona distinta da «osservato», fino a una chiusura. *Per costruzione, e sostenuta dai dati in simulazione su sensore ideale:* 0 interruzioni su 23 402 passaggi (meno di 6,4 su 10 000), ricontato.
- **(b) Precisione dichiarata.** Con ostacolo largo 2 m, bordo dell'ombra noto e persona sul proprio percorso: dentro la zona in almeno 9 casi su 10 fino a 2 s e in almeno 85 su 100 fino a 3 s. *Sostenuta dai dati in simulazione* (30 celle su 30). Col pannello da 1 m: 87 su 100 a 1 s, poi nessuna cifra.
- **(c) Sicurezza.** Ciò che non è osservato non è mai «libero»: *dimostrazione condizionata* (posa nota entro 0,5°, ostacolo che rimanda segnale). L'avviso di possibile presenza non si toglie per identità, tempo od operatore: *per costruzione*, e 0 fotogrammi senza avviso su 4 324 e su 3 608 a persona nascosta entro i 3 m della griglia, su profondità simulata dalle schede (ricontato).

**H-501** (`nuvole-1`, il «libero» della cella dal solo fotogramma) è **verificata sull'insieme dichiarato, solo in simulazione, a camera ideale ferma**: 0 celle libere sopra un ostacolo in 300 condizioni, due lanci, ricontato.

**Che cosa non è provato e non fa parte dell'ipotesi chiusa.** La «stessa identità al ritorno» della H-012 originaria: **smentita** su profondità realistica coi parametri del nucleo (0 su 90), sostenuta come tasso (176 e 174 su 180) solo in un dominio stretto e dietro un interruttore: l'identità esce sempre come «presunta». Il classificatore su più classi: **richiesto, non realizzato, non valutato**. Ogni classe diversa da «persona a piedi», due persone nella stessa ombra, l'occlusore mobile, il sensore in moto, qualunque sensore vero.

**Il senso di «provata».** È quello del contratto d'integrazione (C-F: «solo in simulazione»). Nel senso più stretto dei miei verdetti precedenti (correttezza verificata sul dominio d'uso) **nessuna ipotesi è provata**, e la versione 3 resta «adottabile come progetto di prototipo, non come sistema validato». La versione 3, poi, è una specifica composta: **non è mai stata eseguita come insieme**.

## 2. Contraddizioni su conclusioni adottate

**Nessuna resta aperta su una conclusione adottata, ma solo perché sei conclusioni sono riformulate nel loro dominio.** Le scrivo:

1. **Continuità:** vale sul banco a sensore ideale. Su profondità simulata da scheda **non è ancora eseguita**: nella catena che oggi gira lì, a persona nascosta la traccia è «perso» in 2 983 fotogrammi su 4 552 (ricontato). Decide: regione e «previsto ampio» innestati nella catena, 0 cicli senza regione.
2. **«L'avviso finisce solo guardando» (K-505):** è adottata la sola metà di sicurezza, *non finisce se non guardando*. Che guardando finisca **non è provato**: tolto l'ostacolo resta acceso in 10 prove su 10. Decide: la diagnosi sul seme 301 e il blocco `rotto` di `f12-integrazione/07-controprova-identita/attacco.py`.
3. **Identità ed estraneo (K-016, K-219):** nessuna conclusione sull'identità oltre «presunta, con un soggetto per ombra»; l'avviso non ne dipende. Decide: il braccio «estraneo» di `02-prova-insieme/insieme.c` con l'avviso che resta (0 rilasci).
4. **Precisione e bordo dell'ombra (K-215):** la cifra vale «col bordo noto». Decide: sul sensore, la quota dei cicli in cui il bordo si riconosce.
5. **«Libero» nell'ombra vera (K-014, K-107):** la conclusione è H-501 su camera ideale; le 5 celle·fotogramma «libero» trovate sulla catena di partenza non sono spiegate. Decide: H-501 sulle sequenze di f10, poi il pannello sul suolo segnato, 150 fotogrammi.
6. **Velocità coperta (K-015):** 1,13 m/s con la fascia di 0,40 m, non 1,4. Decide: la latenza misurata.

**Aperte su regole adottate, nominate con la prova** (verdetto, §4): K-504, K-506, K-514 (la prova d'ingresso del rumore va eseguita nella configurazione che si vuole accendere), K-403, K-017, K-109, K-515 (il blocco di classificazione non è ancora fuso nei testi della versione 3, del piano e dello schermo). **All'utente:** K-503 e K-507. Se l'utente scegliesse l'avviso che scade col tempo, la clausola (c) andrebbe riscritta.

## 3. Previsioni

**Risolte.** Soglie della prova d'insieme (C-C): nessun vuoto, **regge**; nessuno scoperto, **smentita** (24 su 23 402); regione, **regge** con l'ostacolo da 2 m e **smentita** col pannello da 1 m; ombra stretta, **smentita** senza riconoscere il bordo; estraneo, **smentita** con c1. Soglie del «libero» (C-D): 0 celle, **smentita** per le due candidate del contratto e **regge** per H-501; mediana di 2,7 m, **regge** a posa esatta (3,0 m); a +0,5° col rumore al limite scende a 2,4 m. Criterio del verdetto sui dati per l'identità (28 su 30 per caso): **smentita** alla replica. «Il minimo chiude entro l'ora 14»: **non provato** (0,04–0,43) e tolto come obiettivo. Le previsioni delle prove A, B, C di H-012 sono risolte nel verdetto del nucleo. Le mie otto di questo passo reggono (`f12-integrazione/30-arbitro/PREVISIONI.md`).

**Non risolte, con la prova che le deciderebbe.**
- Continuità su profondità: l'innesto del punto 1.
- Causa dei 24 passaggi scoperti: il registro dell'ultima misura in quei passaggi.
- Rilascio dell'avviso: il punto 2.
- Errore del bordo d'ombra (A4 del verdetto sui dati) e «libero» dentro l'ombra vera: il pannello sul suolo segnato, col sensore.
- Rumore del centro con la distanza: un metro a terra accanto alla persona.
- Latenza (95° percentile sotto 150 ms): la misura sull'hardware.
- Chi svolta, 0,57–0,70 contro 0,13–0,52: lo stesso lancio col corpo puntiforme.
- La regola «un'etichetta non restringe l'avviso» sulla catena: la prova differenziale con le etichette permutate.
- Quale lettura del piano vale: il minuto in cui la quinta macchina ha le 25 prove verdi.

## 4. Le quattro verifiche dei risultati fondanti

1. **Rilettura:** `f3/H-012/02-validazione/VERIFICA.md` (nucleo); per questo passo `f12-integrazione/13-statistica/CONTROLLO_PROVE.md` (riconteggio delle due prove nuove), `f12-integrazione/11-completezza/COMPLETEZZA.md` (sulla prima stesura) e il rifacimento identico in `f12-integrazione/07-controprova-identita/`. **Manca** una rilettura indipendente della versione 3 finale e del blocco di classificazione.
2. **Audit delle ipotesi nascoste:** `f5/02-audit/AUDIT.md` (dodici ipotesi, sul nucleo versione 2). **Non rifatto sulla versione 3**; lo coprono in parte `f12-integrazione/12-piano-rifatto/PIANO_RIFATTO.md` e `f13-allegato/DISCORDANZE_DEI_FASCICOLI.md`.
3. **Controesempi:** `f4/H-012/01-avversario/CONTROPROVE.md`; `f12-integrazione/10-attacco/ATTACCO_V3.md`; `f12-integrazione/07-controprova-identita/CONTROPROVA_IDENTITA.md`; `f14-classificazione/10-attacco/ATTACCO_CLASSIFICAZIONE.md`.
4. **Consolidamento:** `f12-integrazione/30-arbitro/VERDETTO_INTEGRAZIONE.md`, sopra i cinque verdetti precedenti (nucleo, estensione, continuità, preproposta, dati).

## 5. Esito

Le tre condizioni della pipeline: (1) almeno una H# provata: **sì**, H-012 riformulata e H-501, solo in simulazione, a sensore fermo; (2) nessuna contraddizione aperta su una conclusione adottata: **sì, dopo le sei riformulazioni del §2**; (3) ogni previsione risolta o dichiarata non risolta con la sua prova: **sì**, §3.

Esito: chiuso

Chiusa è la domanda di progetto: quale soluzione costruire e con quale piano. Non è chiusa nessuna domanda sul sensore. Chi chiede «provata sul dominio d'uso» deve leggere questa chiusura come «non chiuso»: lo decideranno le tre misure della prima ora con un sensore.

## 6. Decisioni che spettano all'utente

1. **La classificazione nelle 18 ore:** dichiarata, più scenario e portatore nella configurazione nelle 14 ore e le etichette a mano nelle 4 ore (raccomandata); oppure tutto nelle 14 ore, col minimo che scende da 0,43 a 0,20–0,26; oppure la sola dichiarazione.
2. **Chi toglie l'avviso residuo:** solo lo sguardo, col costo che dietro un ostacolo fermo resta acceso (raccomandata, è la priorità 2); oppure una scadenza a tempo, con cui una persona ferma più a lungo esce senza avviso.
3. **Che cosa si promette:** la scala col gelo all'ora 12 e l'identità «presunta, in correzione», con l'ambiente preparato prima dell'ora 0 e la domanda su sensore, telefono e pannello fatta subito (raccomandata); oppure «il minimo chiuso all'ora 14», che ha probabilità fra 0,04 e 0,43.

Controfirma: arbitro
