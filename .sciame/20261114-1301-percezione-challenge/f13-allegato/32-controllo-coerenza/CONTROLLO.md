# Controllo finale di coerenza e sovraffermazioni dell'allegato tecnico (`sciame-avversario`, f13)

Lavoro del 14 novembre 2026, dalle 19:57:20 alle 20:10 circa (`date -Is`). Oggetto: `../30-finale/allegato_tecnico.tex`, `../30-finale/capitoli/*.tex` e il PDF di 70 pagine, **nel testo di ora**. Niente è stato modificato fuori da questa cartella. **Tutto ciò che l'allegato riporta è dimostrazione, conto o simulazione: nessun mio controllo lo rende «validato».**

## In testa

**Esito.** Sommario, capitolo 1, capitolo 8 e conclusioni letti per intero. Le cifre ricontate tornano tutte (25 intervalli di Wilson e 12 conti in forma chiusa, `conti_uscita.txt`). Gli 11 risultati negativi della consegna ci sono tutti, con la cifra. Le 19 + 9 correzioni delle due verifiche risultano applicate, salvo quelle dichiarate non applicate. Parole e sigle vietate (A-4): **0** nel sorgente e nel PDF. **Restano 17 correzioni** in 18 voci: 6 su frasi più forti del capitolo o dei file da cui vengono (R1–R6), 5 incoerenze fra parti (R7–R11), 4 condizioni perse o regole non dette spente (R12–R15), 2 di forma e A-4 in parafrasi (R17, R18); R16 è la conferma del frontespizio.

**Cambi di stato proposti.** (1) «Un soggetto nascosto entro 3 m non resta senza avviso» (conclusioni, tabella del cap. 1): da *sostenuto* a **sostenuto solo con l'avviso che resta dopo il riaggancio; con la configurazione di riferimento smentito (180 e 271 fotogrammi)** (R1). (2) «Prova d'ingresso sul suolo vuoto» (cap. 8): com'è scritta **non può essere superata** nella configurazione di riferimento su profondità simulata (R2).

**Regole violate e scostamenti.** (a) L'ambiente sconsiglia i file di rapporto: la consegna chiede questo file, ho seguito la consegna. (b) Più di due pagine: la consegna chiede il testo LaTeX di ogni correzione. (c) I capitoli 2–7 **non** sono letti per intero: solo le righe raggiunte dai miei schemi (proposizioni del cap. 5 e del cap. 3, tavole del cap. 6 su sicurezza, continuità, elementi mobili). (d) Tre comandi falliti per errori miei di shell, rifatti; nessun effetto. Niente git, sudo, rete; scritture solo qui.

**Indipendenza.** I programmi (`cerca_vietati.py`, `contesto.py`, `conti.py`) sono miei e non importano codice altrui. Condivido con autori e verificatori i file d'origine, il contratto e il modello linguistico: un errore già nei file d'origine non lo vedo. «538–1791» (R, sotto «che cosa torna») l'ho riscontrato su `../30-finale/CIFRE.md`, che è del redattore.

**Previsioni** (`PREVISIONI.md`, 19:57, prima di ogni lettura): P1 **regge** (R1, R4–R6, R9, R12); P2 **smentita** (gli 11 negativi ci sono tutti; mancano due negativi fuori dall'elenco, R1 e R2); P3 **regge in parte** (28 applicate o dichiarate; due non propagate a tutti i luoghi: R15 e R18a; una applicata a metà e dichiarata: R5); P4 **regge** (R2, R3, R15); P5 **regge** (0 sigle; 5 parafrasi, R17); P6 **regge** (un solo segnaposto, evidente); P7 **regge** (R7, R8, R4).

Fonti citate: **VI** `f12-integrazione/30-arbitro/VERDETTO_INTEGRAZIONE.md`; **V3** `f12-integrazione/20-finale/SOLUZIONE_V3.md`; **PI** `f12-integrazione/02-prova-insieme/PROVA_INSIEME.md`; **ID** `f12-integrazione/06-identita/IDENTITA_SU_PROFONDITA.md`; **F04** `f13-allegato/04-statistica/FASCICOLO_VALUTAZIONE.md`; **G** `f13-allegato/02-geometria/FASCICOLO_GEOMETRIA.md`. Righe dei capitoli: numeri di riga del file di ora. Tutti i testi corretti sono in `correzioni_prova.tex` e compilano con il preambolo (`prova_compilazione/`, XeLaTeX, 0 errori, 3 pagine).

---

## A. Più forte del capitolo o dei file da cui viene

**R1. Avviso su profondità simulata: lo zero è dato senza la configurazione, e la cifra contraria è omessa.**
*Dove:* `01_introduzione.tex` r. 98 («Da scheda: soggetto nascosto entro $3\unita{m}$ senza avviso in 0 fotogrammi su 4324…»); `09_conclusioni.tex` r. 19 («Un soggetto nascosto entro $3\unita{m}$ non resta senza avviso (0 fotogrammi su 4324…»).
*Che cosa non torna.* `06_valutazione.tex` r. 149: «configurazione di riferimento / con l'avviso che resta dopo il riaggancio: 180 e 271 / 0 e 0» sugli stessi 4324 e 4325 fotogrammi; r. 148: prima serie, 99 fotogrammi su 3038 e 15 passaggi su 90. VI, cambio 7: «contro 180 e 271 della catena di partenza». Il cap. 1 (r. 79) promette che «ogni riga delle tabelle dice da quale [catena] viene»: questa non lo dice.
*Testo (cap. 1, al posto della frase «Da scheda: … in una replica.»):*
```latex
Da scheda, con l'avviso che resta dopo il riaggancio: soggetto nascosto entro $3\unita{m}$ senza avviso in 0 fotogrammi su 4324 a 424 pixel di larghezza e in 0 su 4325 a 848, e in 0 su 3608 per risoluzione in una replica; con la configurazione di riferimento, in 180 e 271 degli stessi fotogrammi.
```
*Testo (conclusioni, al posto di «Un soggetto nascosto entro … in una replica).»):*
```latex
Con l'avviso che resta dopo il riaggancio, un soggetto nascosto entro $3\unita{m}$ non resta senza avviso (0 fotogrammi su 4324 a 424 pixel di larghezza e 0 su 4325 a 848, e 0 su 3608 per risoluzione in una replica); con la configurazione di riferimento restava senza avviso in 180 e 271 di quei fotogrammi (\S\ref{sec:val}).
```

**R2. Cap. 8, controllo all'avvio, prova (5): manca la configurazione in cui si esegue.**
*Dove:* `08_limiti.tex` r. 59, «(5) sul suolo vuoto, in $30\unita{s}$, non devono nascere gruppi né tracce confermate. […] se cade la quinta restano spenti l'avviso senza traccia e l'identità al ritorno».
*Che cosa non torna.* `04_stima.tex` r. 71 e `06_valutazione.tex` r. 276: sul suolo vuoto, con i gruppi per componenti connesse (la configurazione di riferimento), nascono 137 e 206 tracce confermate in 9 sequenze; 0 e 0 con i gruppi a celle forti. Com'è scritta, su profondità simulata la prova cade sempre nella configurazione di riferimento. VI §4 (riga «K-506, K-514») e condizione 5: «la prova d'ingresso si esegue nella configurazione che si vuole accendere; se cade: [avviso senza traccia], gruppi per picco e identità spenti e nominati».
*Testo (al posto delle due frasi citate):*
```latex
(5) sul suolo vuoto, in $30\unita{s}$, non devono nascere gruppi né tracce confermate; la prova si esegue nella configurazione che si vuole attivare, cioè con i gruppi a celle forti (\S\ref{sec:sti-mobile}): con i gruppi per componenti connesse della configurazione di riferimento, su profondità simulata dalle schede tecniche, sul suolo vuoto nascono 137 e 206 tracce confermate in 9 sequenze (a 424 e 848 pixel di larghezza), e la prova non sarebbe superata \prova{S}. Se cade una delle prime quattro prove il sistema non parte; se cade la quinta restano spenti i gruppi a celle forti, le condizioni aggiuntive del riaggancio, l'avviso senza traccia e l'identità al ritorno, e l'uscita lo dichiara.
```

**R3. Cap. 8, «Parole per settore»: una regola mai generata è descritta come comportamento.**
*Dove:* `08_limiti.tex` r. 47, «La frase per settori è una regola di progetto: l'ordine fra i primi due livelli non è stato provato \prova{N}.»
*Che cosa non torna.* V3 r. 244: «il messaggio per settori **non è mai stato generato**»; VI §2, riga «Completezza»: «Regole per settori, registro, misura sul posto: mai eseguiti». Il testo dichiara non provato solo l'ordine dei livelli.
*Testo:*
```latex
La frase per settori è una regola di progetto: non è stata generata in alcuna prova, e l'ordine fra i primi due livelli non è stato provato \prova{N}.
```
*Non verificato:* il paragrafo «Uso» del profilo di chi porta il sensore (r. 78: conto all'avvio, parola «tardivo») non porta un livello di prova; nei file letti non ho trovato una sua esecuzione. Se non è mai stato eseguito, aggiungere in coda: `Regola di progetto, non eseguita nella catena \prova{N}.`

**R4. «Osservato» con il soggetto nascosto: «8 su 90 / 1 su 140» non ha riscontro nei capitoli 2–7, dove la stessa grandezza vale «11 e 6 / 1 e 1 su 140».**
*Dove:* `01_introduzione.tex` r. 116; `08_limiti.tex` r. 127 (invariante 3). Il cap. 1 rimanda a \S 6, che non ha la riga.
*Prova.* `04_stima.tex` r. 211: «i riagganci a persona ancora nascosta scendono da 11 e 6 a 1 e 1 su 140 passaggi»; ID r. 52: «Riaggancio a persona nascosta (140) | 11 · 6 | … | **1 · 1**». «8 su 90» sta solo in V3 r. 269, su un'altra serie. «1 su 140» è per risoluzione, non in tutto.
*Testo (cap. 1, colonne «Valore» e «Dove»):*
```latex
uscita «osservato» con il soggetto nascosto in 8 passaggi su 90 in una prima serie e in 11 e 6 su 140 in una seconda (a 424 e 848 pixel di larghezza) / in 1 e 1 su 140: la soglia 0 non è rispettata & \prova{S} & \S\ref{sec:sti}\\
```
*Testo (invariante 3, al posto di «8 passaggi su 90 … 1 su 140 con i gruppi a celle forti»):*
```latex
8 passaggi su 90 e, in una seconda serie, 11 e 6 su 140 con la configurazione di riferimento su profondità simulata dalle schede tecniche; 1 e 1 su 140 con i gruppi a celle forti
```
*Non verificato:* «8 su 90» non l'ho ricontato sul file grezzo.

**R5. Cap. 1, riga «Ostacoli fermi»: 84 su 84 e 10 su 10 non stanno in nessun capitolo.**
*Dove:* `01_introduzione.tex` r. 115, con rimando a \S 6. `06_valutazione.tex`, Tabella `tab:val-mobili`, ha solo i casi limite (r. 279). La correzione 16 della lettura da commissario è dichiarata «applicata in parte».
*Prova.* F04 r. 221: «cassa alta 1 m a 1,68 m; scatola di 15 cm a 2,0 m | 84; 10 | 84; 10 fotogrammi (una sequenza ciascuno)».
*Testo (riga da aggiungere a `tab:val-mobili`, prima di «Ostacolo entro 15 cm dalla posizione vera, casi limite»):*
```latex
Ostacolo fermo entro 15 cm dalla posizione vera & cassa alta $1\unita{m}$ a $1{,}68\unita{m}$; scatola di 15 cm a $2{,}0\unita{m}$ & 84; 10 & 84; 10 fotogrammi (una sequenza ciascuno) & — & II \prova{S}\\
```

**R6. Cap. 1, riga «Regola «mobile»»: «in 5 su 90 con la soglia adattata alla risoluzione» è dato come rimedio, senza il costo.**
*Dove:* `01_introduzione.tex` r. 114.
*Prova.* `04_stima.tex` r. 69, titolo «Una soglia di punti assoluta non rimedia»: con $n_{\min}=40$ «una scatola alta 15 cm a 2 m è vista in 3 prove su 10 anziché 10 su 10», e a $848\times480$ la stessa soglia dà l'identità in 0 passaggi su 10.
*Testo (colonna «Valore»):*
```latex
«in movimento» entro $1\unita{s}$: 100\,\% ($\ell^-=99{,}81\,\%$); pannello fermo dichiarato mobile in 79 su 90 $[79{,}4;\,93{,}0\,\%]$; in 5 su 90 con la soglia minima di punti portata da 3 a 40, non adottata perché una scatola alta $15\unita{cm}$ a $2\unita{m}$ è allora vista in 3 prove su 10 anziché in 10 su 10; con i gruppi a celle forti in 0 su 140 nel dominio dell'identità al ritorno e in 7 su 10 fuori da esso
```

## B. Incoerenze fra parti del documento

**R7. Altezza dell'ostacolo che nasconde: 1,61 m e «circa 1,65 m» nel cap. 8, 1,59 m nella tabella del cap. 2.**
*Dove:* `08_limiti.tex` r. 155 (condizione 6: «Per una persona alta $1{,}70\unita{m}$ servono $1{,}61\unita{m}$ d'ostacolo nella geometria provata») e r. 167 (limite 3: «più basso di circa $1{,}65\unita{m}$»).
*Prova.* `02_geometria.tex`, Tabella `tab:geo-amin` (persona a 2,3 m): statura 1,70 m → 1,57 / 1,59 / 1,61 m con il pannello a 1,7 / 1,8 / 1,9 m; statura 1,75 m → 1,65 m a 1,9 m. Mio riconto: $1{,}2+0{,}5\cdot1{,}8/2{,}3=1{,}591$; $1{,}2+0{,}5\cdot1{,}9/2{,}3=1{,}613$; $1{,}2+0{,}55\cdot1{,}9/2{,}3=1{,}654$. G r. 84 dà «fra 1,61 m (statura 1,75 m) e 1,67 m». «Geometria provata» non è definita.
*Testo (condizione 6):*
```latex
\item \textbf{Ostacolo che nasconde per intero.} Per una persona alta $1{,}70\unita{m}$ a $2{,}3\unita{m}$ dal sensore servono da $1{,}57$ a $1{,}61\unita{m}$ d'ostacolo con il pannello fra $1{,}7$ e $1{,}9\unita{m}$ ($1{,}59\unita{m}$ a $1{,}8\unita{m}$), e $1{,}65\unita{m}$ per una statura di $1{,}75\unita{m}$ con il pannello a $1{,}9\unita{m}$ (Tabella~\ref{tab:geo-amin}).
```
*Testo (limite 3, al posto di «Dietro un ostacolo più basso di circa $1{,}65\unita{m}$»):*
```latex
Dietro un ostacolo più basso dell'altezza minima della Tabella~\ref{tab:geo-amin} (circa $1{,}65\unita{m}$ per una statura di $1{,}75\unita{m}$ con il pannello a $1{,}9\unita{m}$)
```

**R8. «Velocità coperta»: lo stesso nome per 1,13 m/s (fascia) e 1,44 m/s (avviso tempestivo); il passo normale «rientra nel dominio» in un punto e «non è coperto» in un altro.**
*Dove:* `08_limiti.tex` r. 95, (a): «una persona a passo normale rientra nel dominio con $6\unita{cm}$ di margine»; r. 154, condizione 5: limite $1{,}13\unita{m/s}$; `05_occlusione.tex` r. 111: «il passo d'uomo ($1{,}4\unita{m/s}$) non è coperto».
*Prova.* Mio riconto: $2{,}05/1{,}422=1{,}442$; $1{,}4\cdot1{,}422+0{,}95=2{,}941$ (margine 5,9 cm); $0{,}40/0{,}355=1{,}127$. VI §3, riserva (b). Le due cifre sono giuste; il testo non dice che sono due grandezze.
*Testo (al posto delle prime due frasi del punto (a)):*
```latex
(a) A sensore fermo del profilo conta solo $T_r$. Con $T_r=1{,}0\unita{s}$ la velocità coperta dall'avviso tempestivo è $1{,}44\unita{m/s}$: una persona a passo normale ($1{,}4\unita{m/s}$) vi rientra con $6\unita{cm}$ di margine sulla distanza, il passo svelto no. È una grandezza diversa dalla velocità coperta dalla fascia di guardia ($1{,}13\unita{m/s}$, condizione~5 del \S\ref{sec:lim-validita}), che il passo normale supera: a $1{,}4\unita{m/s}$ l'avviso è tempestivo per calcolo, ma il contenimento nella fascia non è dimostrato (\S\ref{sec:occ}).
```

**R9. Fascia di guardia: «contiene il soggetto» nelle conclusioni, «$c(s)\in W$» (il centro) nella proposizione.**
*Dove:* `09_conclusioni.tex` r. 9; stessa forma in `01_introduzione.tex` r. 93 («copre $\vmax=1{,}13$») e in `08_limiti.tex` r. 154.
*Prova.* `05_occlusione.tex` r. 84–90: la tesi è sul centro $c(s)$; «Per contenere l'intero corpo di raggio $r_c$ si aggiunge $r_c$ al secondo membro». Con il disco di $0{,}45\unita{m}$ delle prove d'insieme ($r_c=0{,}225$) il mio conto dà $(0{,}40-0{,}225)/0{,}355=0{,}49\unita{m/s}$: cifra **mia, non presente nei file**, e per questo non messa nel testo.
*Testo (conclusioni):*
```latex
\item La fascia di guardia $w$ contiene il centro del soggetto se vale la condizione~\eqref{eq:occ-fascia}, l'ostacolo è fermo e il soggetto resta nel campo e in portata; con $w=0{,}40\unita{m}$ la velocità coperta, per calcolo, è $1{,}13\unita{m/s}$, e $0{,}56\unita{m/s}$ se il bordo dell'ombra sbaglia di $0{,}20\unita{m}$; per contenere l'intero corpo, di raggio $r_c$, la condizione chiede $r_c$ in più e la velocità coperta è minore (Proposizione~\ref{prop:occ-fascia}) \prova{C}.
```
Nel cap. 1 (r. 93) e nella condizione 5 del cap. 8: «copre» → «copre, per il centro del soggetto,».

**R10. Continuità: la soglia della Tabella dei requisiti è su tutti i passaggi, lo zero è sui soli passaggi con l'ingresso riconosciuto.**
*Dove:* `01_introduzione.tex` r. 24 (soglia «0 passaggi con un'interruzione», «sui passaggi con almeno 4 misure prima della scomparsa») e r. 94 (esito «0 … su $23\,402$»).
*Prova.* `06_valutazione.tex` r. 11 definisce il vuoto senza la premessa; r. 170: «se la traccia si chiude prima non c'è regione». PI r. 19–20: a1 «regge» con la premessa «traccia entrata nell'ombra», a2 «**cade**» (928; 24 con la regola). VI §1, C-C: «scoperti 24 (cade la soglia 0)». Per le altre soglie mancate il cap. 1 lo scrive («la soglia 0 non è rispettata»); qui no. Mio conto: $23\,402-928=22\,474$; $23\,402-24=23\,378$.
*Testo (da aggiungere in r. 94 dopo «…sul suolo vuoto.»):*
```latex
Rispetto alla soglia della Tabella~\ref{tab:intro-requisiti} (0 passaggi con un'interruzione), lo zero vale fra i passaggi con l'ingresso riconosciuto ($22\,474$ su $23\,402$; $23\,378$ con la regola aggiuntiva): negli altri non c'è regione, e su tutti i passaggi la soglia non è raggiunta.
```
*Non verificato:* che i 928 passaggi abbiano tutti almeno 4 misure prima della scomparsa.

**R11. Prove d'insieme: «corpo esteso» per tutti i $23\,402$ passaggi.**
*Dove:* `06_valutazione.tex` r. 165 («corpo esteso; 12 configurazioni $\times$ 5 comportamenti») e r. 128.
*Prova.* PI r. 20: «0,7: 22 su 11 701 (esteso 17, puntiforme 5)»; `06_valutazione.tex` r. 143: corpo esteso con $P_D=0{,}9$, $N=5704$, cioè circa metà degli $11\,701$ passaggi con quel $P_D$. Le 12 configurazioni sono 3 disposizioni per 2 valori di $P_D$ per 2 modelli del corpo.
*Testo (r. 165, colonna «Condizioni»):* `corpo esteso e soggetto puntiforme; 12 configurazioni $\times$ 5 comportamenti`. Nel sommario la condizione «ostacolo largo $2\unita{m}$» precede anche la continuità, che è contata su tutte e tre le disposizioni: lo corregge il testo di R12.

## C. Condizioni perse, regole non dette «attive solo dopo le prove d'ingresso»

**R12. Sommario.** (a) «l'avviso di possibile presenza termina solo per osservazione diretta»: VI §4 (riga K-505) adotta «la sola metà di sicurezza: non finisce se non guardando», e §7 vieta «l'avviso si spegne quando rivede il suolo». (b) Il sommario non dice che l'avviso resta acceso dopo la rimozione dell'ostacolo (cap. 1 r. 98, 10 prove su 10). (c) «una regola aggiuntiva» senza dire che è attiva solo dopo una prova d'ingresso (V3 r. 129). (d) R11.
*Testo (al posto del tratto che va da «Lo stato «libero» è scritto solo…» a «…questa regola non è stata eseguita.»; le frasi sul classificatore e sul sensore fisico restano come sono):*
```latex
Lo stato «libero» è scritto solo per il suolo osservato nel fotogramma corrente; l'avviso di possibile presenza non termina senza osservazione diretta. Nelle ipotesi dichiarate sono dimostrati che ciò che non è osservato non è mai «libero», il contenimento del soggetto nascosto nell'insieme di possibile presenza e la condizione sulla fascia di guardia. In simulazione, con modello ideale del sensore e un soggetto alla volta, la regione di previsione è emessa a ogni ciclo dell'occlusione una volta riconosciuto l'ingresso nell'ombra (0 interruzioni su $23\,402$ passaggi; l'ingresso non è riconosciuto in 928 di essi, in 24 con una regola aggiuntiva, attiva solo dopo una prova d'ingresso); con un ostacolo fermo largo $2\unita{m}$, il bordo dell'ombra noto e il soggetto sul proprio percorso, la regione contiene il soggetto in almeno 9 casi su 10 fino a $2\unita{s}$ e in almeno 85 su 100 fino a $3\unita{s}$; con un ostacolo largo $1\unita{m}$ la soglia di 9 su 10 non è raggiunta, e su profondità simulata dalle schede tecniche questa regola non è stata eseguita. Con un ostacolo fermo l'avviso resta acceso, e nella realizzazione provata resta acceso anche dopo la rimozione dell'ostacolo.
```

**R13. Secondo soggetto: «l'avviso resta» senza il livello di prova.**
*Dove:* `01_introduzione.tex` r. 112.
*Prova.* `05_occlusione.tex` r. 236: «rilasci senza osservazione zero per costruzione; la verifica sul caso del secondo soggetto con modello ideale del sensore non è stata eseguita \prova{N}»; da scheda 0 fotogrammi su 336 in una scena costruita; `06_valutazione.tex` r. 262: «le due regole non sono state eseguite insieme nello stesso programma \prova{N}».
*Testo (al posto di «…2400 su 2400 con modello ideale); l'avviso resta», con la colonna «Prova» portata a `\prova{S}\prova{N}`):*
```latex
Un secondo soggetto nella stessa ombra riceve l'identità del primo (19 casi su 20 da scheda; 2400 su 2400 con modello ideale). L'avviso resta per costruzione; da scheda, in una scena con due persone, 0 fotogrammi su 336 con il primo soggetto fuori dall'avviso; con modello ideale la verifica non è stata eseguita
```

**R14. Intervalli dell'identità e regola d'arrotondamento.**
*Dove:* `01_introduzione.tex` r. 79 («gli estremi superiori sono arrotondati per eccesso») e r. 112 («$[94;\,99\,\%]$», «$[93;\,98\,\%]$»); `08_limiti.tex` r. 173; `04_stima.tex` r. 211.
*Prova.* `conti_uscita.txt`: 176/180 → $[94{,}43;\,99{,}13]$; 174/180 → $[92{,}92;\,98{,}46]$. «Per eccesso» darebbe 100 e 99; e 92,9 scritto 93 alza l'estremo inferiore di un tasso favorevole. VI, cambio 6, scrive 94,4–99,1 e 92,9–98,5. La regola dichiarata vale solo per gli zeri.
*Testo (r. 79):*
```latex
Gli intervalli fra parentesi quadre sono di Wilson al 95\,\%; gli estremi superiori degli intervalli per zero eventi sono arrotondati per eccesso ($2{,}85\,\%$ è scritto $2{,}9\,\%$ e $0{,}0155\,\%$ è scritto $0{,}016\,\%$), gli altri estremi al valore più vicino.
```
*Testo (r. 112, e gli stessi numeri nei cap. 4 e 8):* `176 su 180 $[94{,}4;\,99{,}1\,\%]$ a 424 pixel di larghezza e 174 su 180 $[92{,}9;\,98{,}5\,\%]$ a 848`.
Nella stessa r. 79, «tre camere a stereo attivo a $424\times240$ pixel» contro le cifre «a 848» delle tabelle: `a $424\times240$ pixel e, dove indicato, a $848\times480$, a posa nota`.

**R15. Regole attive solo dopo le prove d'ingresso, date come risultato del sistema nelle parti di sintesi.**
*Dove:* `01_introduzione.tex` r. 79 e r. 112, 114, 116; `09_conclusioni.tex` r. 19; `08_limiti.tex` r. 173. La nota c'è solo in `04_stima.tex` r. 71 e 207 e nell'appendice A.
*Prova.* V3 r. 24: gruppi e riaggancio «restano spenti di norma e si accendono solo dopo le due prove d'ingresso»; VI, condizione 13: «solo dietro interruttore, spento di norma».
*Testo (da aggiungere in fondo a r. 79 del cap. 1; la stessa frase dopo «…rumore nominale (\S\ref{sec:sti}, \S\ref{sec:val}).» nelle conclusioni):*
```latex
I gruppi a celle forti, le condizioni aggiuntive del riaggancio e l'avviso per le tracce chiuse vicino a un'ombra non fanno parte della configurazione di riferimento: si attivano all'avvio solo se le prove d'ingresso del \S\ref{sec:lim-salute} sono superate, e l'uscita dichiara quali sono attive.
```

## D. Forma e tracce del modo di lavorare (A-4)

**R16. Frontespizio.** «Autori: [nomi degli autori]» è un segnaposto evidente (fra parentesi quadre), l'unico; «novembre 2026» è una data, non uno stato. Il PDF non ha titolo né autore nei metadati (`pdfinfo.txt`). A posto: resta da compilare la riga 3 di `allegato_tecnico.tex`.

**R17. Parafrasi dello stato dei lavori** (il programma non le vede: lette a occhio).
- `A_parametri.tex` r. 56, «da rifissare con $60\unita{s}$ di conteggio a vuoto e sotto carico» → `valore di progetto, non misurato; va fissato con $60\unita{s}$ di conteggio a vuoto e sotto carico`.
- `A_parametri.tex` r. 61, «il legame fra i due numeri non è documentato» → `il legame fra i due numeri non è derivato in questo documento`.
- `A_parametri.tex` r. 13, 20, 25, «da misurare» (tre volte) → `non misurato` (r. 20: `non misurato sul suolo`).
- `06_valutazione.tex` r. 124, «con i semi riparati il rapporto torna a $0{,}94$ […] non sono stati rifatti con semi riparati» → `con lo stato iniziale mescolato il rapporto torna a $0{,}94$` e `non sono stati ripetuti con lo stato iniziale mescolato`.
- `07_costo.tex` r. 99, didascalia, «La terza riga è riportata senza ricalcolo dai dati per ciclo.» → `La terza riga non è stata ricalcolata dai dati per ciclo.` (marginale: dichiara una provenienza, non uno stato).

**R18. Minori.** (a) `03_mappa.tex` r. 201, «dichiarano lo stesso principio» → `dichiarano un principio analogo`, come la correzione già applicata al cap. 1 (in `07_costo.tex` r. 164 «lo stesso principio» lega due fonti fra loro, e subito dopo il testo dice che il sistema «ne riprende due principi»: accettabile). (b) `08_limiti.tex` r. 172: «10 prove su 10, (72--100\,\%)» ha una virgola di troppo. (c) Cap. 1 r. 130 e limite 9, «24–34\,\% in registrazioni pubbliche»: senza citazione e senza un file che dica quali; lo dichiara già il redattore, resta aperto.

---

## Che cosa torna (una riga per parte)

- **Sommario:** condizioni e cifre giuste; restano R12.
- **Cap. 1:** tabella dei requisiti, idea, contributi, riquadro dei limiti e ambiti d'uso a posto; tabelle di sintesi a posto salvo R1, R4–R6, R10, R13–R15. Riscontrate nei capitoli 3–7: 135 e 381 sequenze, $2\,907\,032$ e $3\,992\,186$; 30 combinazioni su 30, $2125/2279$ e $1754/1922$; $942/1045$; $826/879$; $0$ su $24\,835$ ($13\,638+5600+5597$); 29 su $95\,399$ e 15 su 2000; le tre quote dell'identità; 79 su 90; 7 su 10; $16{,}5$ e $0{,}67\unita{m/s^2}$; 9152 cicli, $6{,}35$ e $18{,}6\unita{ms}$, 4 cicli; «$N$ da 538 a 1791» (a 2 e $3\unita{s}$: `CIFRE.md` r. 843–844).
- **Cap. 8:** contratto d'uscita, registro, salute, formule e tabella dei profili (ricontate), latenza ($155$, 138–172, $170$, $131\unita{ms}$; flusso a 30 fotogrammi al secondo e ciclo a $15\unita{Hz}$ sono detti nell'appendice A), invarianti, condizioni, limiti 1, 2, 4–11, sensore in moto, protocollo: a posto salvo R2–R4, R7–R9.
- **Conclusioni:** i tre livelli di prova sono tenuti separati; il primo punto del «dimostrato» ora coincide con la Proposizione; a posto salvo R1, R9, R15.
- **Confronto con VI:** nessuna delle frasi «da non dire» di VI §7 compare come affermazione; le 16 affermazioni di §7 non sono superate in forza, salvo R1, R10 e R12a. Gli 11 negativi della consegna: tutti presenti nel cap. 1 e nelle conclusioni con la cifra (secondo soggetto; 0 su 90; 79 su 90 e 7 su 10; avviso acceso 10 su 10; continuità non eseguita su profondità simulata, con 2983 fotogrammi «perso» su 4552 nel cap. 8; fuori dominio; posa; vetro; latenza; classificatore e classi; 3 classi su 15).
- **Le 19 + 9 correzioni:** applicate tutte nel testo di ora, controllate una per una; non applicate e dichiarate: 25/19 (lunghezza), 26/16 in parte (R5), 25/18 (segnaposto degli autori, cambiato e ancora da compilare). Propagazione mancante: 26/8 (R15), 25/14a (R18a).
- **Contraddizioni cercate e non trovate:** latenza ($0{,}155$ ovunque; $0{,}150$ in una riga del cap. 5 che lo dice); numero di sequenze e di celle; quote dell'identità; soglie di copertura ($0{,}90$ e $0{,}85$); $w=0{,}40\unita{m}$ e $0{,}355\unita{s}$.

## Che cosa non ho controllato

Capitoli 2–7 e appendice A non letti riga per riga; dimostrazioni e citazioni fuori dalla mia parte; figure non guardate in immagine; nessun simulatore rieseguito; «8 su 90», «538–1791» e «24–34 %» non ricontati sui file grezzi; il paragrafo «Uso» del profilo (R3) e l'appartenenza dei 928 passaggi alla base della soglia (R10) restano «non verificato».

## Che cosa propongo dopo

1. Applicare R1–R15 e ricompilare. Previsione: 70–71 pagine, 0 errori. Smentita: un rimando irrisolto fra quelli usati qui (`sec:sti-mobile`, `sec:lim-validita`, `sec:lim-salute`, `tab:geo-amin`, `tab:intro-requisiti`, `tab:val-mobili`: esistono tutti, una volta ciascuno).
2. Far dire al programma d'origine se «8 su 90» e «11 e 6 su 140» misurano la stessa grandezza (R4).

## File accanto

`PREVISIONI.md`; `cerca_vietati.py` → `uscita_vietati.txt`, `totali_vietati.txt` (419 riscontri grezzi, 0 veri fra parole e sigle del contratto: gli «orari» sono coordinate dei disegni, i «percorsi» frazioni e unità, `c1` è il nome di un LiDAR in bibliografia); `contesto.py`; `conti.py` → `conti_uscita.txt`; `allegato_testo.txt` (`pdftotext -layout`), `pdfinfo.txt`; `correzioni_prova.tex` e `prova_compilazione/` (prova di compilazione dei testi corretti).
