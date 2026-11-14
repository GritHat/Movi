# Verifica avversaria dell'allegato — cifre, capitoli 6–8 e appendici (`sciame-validazione`)

14 novembre 2026, 19:26–19:38 (`date -Is`). Oggetto: `20-unione/capitoli/06_valutazione.tex`, `07_costo.tex`, `08_limiti.tex`, `A_parametri.tex`, `B_riproducibilita.tex`, più la tabella di sintesi di `01_introduzione.tex`, `09_conclusioni.tex` e `00_sommario.tex`. Percorsi relativi a `.sciame/20261114-1301-percezione-challenge/`.

## Esito in tre righe

- **Controllate:** 1025 cifre distinte dei cinque file (conteggio per file) setacciate contro le fonti; circa 135 righe di ricalcolo mio per il capitolo 6 (intervalli, potenze, quantili: `intervalli.txt`) e circa 70 conti in forma chiusa per i capitoli 7, 8 e B (`conti_78.txt`); circa 140 cifre lette alla fonte con la loro condizione (riga per riga, gruppi elencati in fondo).
- **Tornano:** tutte le cifre esistono in un file d'origine (nessuna inventata); tutti gli intervalli tranne tre all'ultima cifra; i 42 parametri dell'appendice A confrontati con `SOLUZIONE_V3.md` e con il blocco di classificazione (uno non trovato: la scomposizione di $C$ in $0{,}85+0{,}10\unita{m}$); tutti i conti in forma chiusa dei capitoli 7 e 8.
- **Non tornano:** 5 punti falsi, non sostenuti o incoerenti fra capitoli (correzioni 1–5); 3 valori sbagliati di un'unità sull'ultima cifra (6); 7 cifre giuste con la condizione imprecisa (7–13); 2 di forma (14–15).

**Regole violate e limiti del mio controllo.** (1) Le previsioni (`PREVISIONI.md`) portano l'ora 19:26:29 ma sono state scritte nella stessa mossa in cui aprivo il capitolo 6: non sono cieche rispetto al testo. (2) `scipy` non è installato e la rete è vietata: ho riscritto binomiale, Beta e quantile normale in Python puro (`mini.py`); l'«n stabile» è cercato solo fino a n = 419. (3) Nessun simulatore rieseguito: condivido con l'allegato i file d'origine e i loro riconteggi; un difetto dei simulatori mi resta invisibile. Non condivido l'autore né `CIFRE.md` (non usato come verità). Scritto solo in questa cartella; niente git, sudo, rete.

**Esito delle previsioni.** P1 (almeno una cifra discorde): **regge**. P2 (un intervallo diverso di più di un'unità sull'ultima cifra): **smentita** (tre differenze, tutte di una sola unità). P3 (un parametro di A diverso da `SOLUZIONE_V3.md`): **smentita** sui 42 parametri confrontati. P4 (sintesi o conclusioni diverse dalle tavole del capitolo 6): **regge** (correzioni 4 e 5).

---

## Correzioni, in ordine di gravità

### A. Falso, non sostenuto o incoerente

**1. Capitolo 6, «Forma dichiarabile» (riga 212): «lì si dichiara solo «a $1\unita{s}$ circa 9 su 10 (limite $0{,}87$)»».**
Che cosa non torna: la frase «9 su 10» per il pannello da 1 m è fra quelle da non scrivere, e contraddice il capitolo 8 (limite 5: «almeno 87 su 100») e la riga della tabella accanto (942/1045, $\ell^-=0{,}882$: soglia $0{,}90$ non raggiunta).
Prova: `f12-integrazione/30-arbitro/VERDETTO_INTEGRAZIONE.md` riga 8 («smentita con il pannello da 1 m»), riga 100 («pannello da 1 m «almeno 87 su 100» fino a 1 s»), riga 121 («la soglia di 9 su 10 è smentita»), riga 132 («Da non dire: … «9 su 10» col pannello da 1 m»); `SOLUZIONE_V3.md` riga 153. La forma «circa 9 su 10» sta solo in `13-statistica/CONTROLLO_PROVE.md` §4, che il giudizio successivo ha ristretto.
Testo corretto: `lì la soglia di $0{,}90$ non è raggiunta: si dichiara solo «almeno 87 su 100 a $1\unita{s}$» (limite $0{,}875$ sulle cinque celle giudicate insieme), poi l'uscita dice «è dietro l'ostacolo» senza livello (area relativa $0{,}95$–$1{,}00$).`

**2. Appendice B, «Numerosità tipiche»: «(217\,861 passaggi lanciati in tutto)».**
Che cosa non torna: 217 861 sono i passaggi *confermati* di tutti i lanci; i passaggi *lanciati* sono 226 400, e i camminatori distinti al più 70 400.
Prova: `13-statistica/CONTROLLO_PROVE.md` riga 76 («226 400 passaggi lanciati sono al più 70 400 camminatori distinti») e riga 77 («217 861 (confermati), 194 861 (senza l'estraneo)»).
Testo corretto: `23\,402 passaggi nascosti di 6\,000 camminatori distinti; sull'insieme di tutti i lanci, 217\,861 passaggi confermati su 226\,400 lanciati, di al più 70\,400 camminatori distinti`.

**3. Capitolo 6, tabella `tab:val-mobili`, riga «idem, gruppi dalle celle forti | semi nuovi; 424 e 848 px | 0 e 0 | 140 passaggi».**
Che cosa non torna: lo zero è dato senza dominio e tace il controesempio; «il pannello non è mai dato per mobile» senza il dominio è fra le frasi da non scrivere.
Prova: `VERDETTO_INTEGRAZIONE.md` riga 17 («Fuori dominio … il pannello è «in movimento» in 7 passaggi su 10 alle due risoluzioni: «mai in movimento» vale solo nel dominio») e riga 132; `30-arbitro/riconteggio2.txt` righe 7 e 9 («pannello mobile 7» nei 120 passaggi della replica, a 424 e a 848 px). Lo zero su 140: `06-identita/IDENTITA_SU_PROFONDITA.md` riga 51.
Testo corretto della riga: `idem, gruppi dalle celle forti & semi nuovi; adulto solo, $0{,}5\unita{m}$ dietro il pannello, entro $2{,}6\unita{m}$, nominale; 424 e 848 px / fuori da questo dominio, in una replica & 0 e 0 / 7 e 7 & 140 passaggi / 10 passaggi & 0–2,7\,\% / 40–89\,\% & II \prova{S}\\` (intervalli di Wilson miei: 0 su 140 → 0–2,67 %; 7 su 10 → 39,7–89,2 %). Nella frase «Che cosa il risultato non dice» aggiungere: `Fuori dal dominio dell'identità al ritorno il pannello fermo torna «in movimento» (7 passaggi su 10 alle due risoluzioni).`

**4. Sintesi (capitolo 1, `tab:intro-sintesi`, riga «Avviso di possibile presenza») e conclusioni (capitolo 9) contro capitolo 6 (`tab:val-sicurezza`, ultima riga): «0 fotogrammi su 4324, e 0 su 3608 in una replica» contro «0 e 0 su 3921 e 3922 fotogrammi».**
Che cosa non torna: lo stesso risultato ha due denominatori nei due capitoli, e 4324 non compare nel capitolo 6. Le due cifre stanno entrambe nelle fonti, con condizioni diverse; nessuna delle due è scritta con la sua.
Prova: `VERDETTO_INTEGRAZIONE.md` riga 14 («0 fotogrammi su 4 324 a 424 px e 0 su 4 325 a 848 px, contro 180 e 271 della catena di partenza; replica 0 su 3 608 per risoluzione [R]. Altri 334 fotogrammi sono oltre i 3 m») e `riconteggio2.txt` righe 2–5 (150 passaggi per risoluzione); `IDENTITA_SU_PROFONDITA.md` riga 53 («3 921 · 3 922 fot., senza d», catena di partenza 157 · 251). Inoltre la riga del capitolo 6 accoppia lo «0» con «99 su 3038», che viene da un'altra serie di sequenze (`f10-dati/23-verdetto/VERDETTO_DATI.md` riga 5): non è un confronto appaiato.
Testo corretto della riga del capitolo 6: `Soggetto nascosto entro $3\unita{m}$ fuori dall'avviso & pannello; catena di partenza, prima serie / stesse sequenze nuove a 424 e 848 px: catena di partenza, poi con l'avviso che sopravvive al riaggancio & 99 / 180 e 271, poi 0 e 0 & 3038 / 4324 e 4325 fotogrammi (3921 e 3922 senza il caso in cui il soggetto non ricompare); replica: 0 su 3608 per risoluzione & 15 passaggi su 90: 10,4–25,7\,\% / — & II \prova{S}\\`
Nel capitolo 1 e nel capitolo 9: `0 fotogrammi su 4324 a 424 pixel di larghezza e 0 su 4325 a 848, e 0 su 3608 per risoluzione in una replica`.

**5. Capitolo 9, «Dove le simulazioni mostrano che il sistema cede»: «Chi svolta o esce dal lato lontano dell'ombra è nella regione in una quota di casi fra $0{,}57$ e $0{,}86$ a 2 e $3\unita{s}$».**
Che cosa non torna: la tabella `tab:val-fuori` del capitolo 6 dà, per gli stessi comportamenti e gli stessi tempi, $0{,}131$–$0{,}698$ con il soggetto puntiforme; $0{,}57$–$0{,}86$ è la sola prova con il corpo esteso. La conclusione riporta il caso migliore senza dirlo (la tabella di sintesi del capitolo 1 li dà entrambi).
Prova: capitolo 6, righe 222–224; `04-statistica/FASCICOLO_VALUTAZIONE.md` righe 191–192; `02-prova-insieme/PROVA_INSIEME.md` riga 41; `SOLUZIONE_V3.md` riga 413 («in V8 fino a 0,13»).
Testo corretto: `Chi svolta o esce dal lato lontano dell'ombra è nella regione, a 2 e $3\unita{s}$, in una quota di casi fra $0{,}57$ e $0{,}86$ nelle prove con il corpo esteso e fra $0{,}13$ e $0{,}70$ in quelle con il soggetto puntiforme;`

### B. Valori sbagliati di un'unità sull'ultima cifra

**6. Capitolo 6, tre valori** (ricalcolo in `intervalli.txt`; nel fascicolo 04 sono già così: righe 53, 79, 80; `04-statistica/conti.txt` righe 6 e 8 dà 0.8865 e 0.9685, arrotondati una seconda volta).
- Riga 50: `$z_{60}=3{,}342$` → **`$z_{60}=3{,}341$`** ($\Phi^{-1}(1-0{,}05/120)=3{,}34148$).
- `tab:val-numerosita`, «30 su 30», Wilson: `0,887–1` → **`0,886–1`** ($30/33{,}8415=0{,}88649$; il capitolo 8, ultima frase, scrive già $0{,}886$).
- `tab:val-numerosita`, «46 su 50», Wilson: `0,812–0,969` → **`0,812–0,968`** ($0{,}96845$).

### C. Cifra giusta, condizione imprecisa

**7. Capitolo 6, `tab:val-soglie`, seconda parte: valori fra parentesi «(0,946)», «(0,922)», «(0,914)», «(0,890)» e «15 su 15 (15)».**
La didascalia rimanda alla Proposizione `prop:val-celle` senza dire $m$. I valori sono giusti con $m=30$ ($z_{30}=3{,}144$: le 15 celle di $G_2$ più le 15 di $G_3$); con $m=15$, che è ciò che la riga lascia intendere, verrebbero $0{,}948$ / $0{,}925$ / $0{,}915$ / $0{,}892$.
Prova: `13-statistica/CONTROLLO_PROVE.md` §2 («correzione di Bonferroni su 30 celle (z = 3,14)»); `intervalli.txt`, righe «z 15» e «z 30».
Testo corretto della didascalia: `fra parentesi con la correzione della Proposizione~\ref{prop:val-celle}: $m=45$ nella prima parte ($z_{45}=3{,}261$), $m=30$ nella seconda ($z_{30}=3{,}144$, le 30 celle di $G_2$ e $G_3$ insieme), $m=5$ dove è scritto.` E a riga 50 aggiungere `$z_{30}=3{,}144$`.

**8. Capitolo 6, `tab:val-sicurezza`, prima riga, colonna $N$: «175\,802 istanti; 24\,835 passaggi a semi indipendenti».**
Lascia intendere che tutti gli istanti vengano da semi indipendenti; sono 104 131 su 175 802 (lo dice più avanti l'avvertenza: 71 671 non rifatti).
Prova: fascicolo 04, §6.1, prima riga; `04-statistica/ricontato.txt` righe 66–67 (35 780 + 35 891 + 104 131).
Testo corretto: `175\,802 istanti, di cui 104\,131 in 24\,835 passaggi a semi indipendenti`.

**9. Capitolo 6, «Sicurezza» (riga 129): «In 240 delle 300 condizioni della regola adottata (7200 fotogrammi) le regole del «libero» scartate danno violazioni: …».**
240 è il denominatore (16 combinazioni × 5 livelli di misure mancanti × 3 errori = 240 condizioni = 7200 fotogrammi), non il numero di condizioni con violazioni.
Prova: `03-libero/LIBERO_DELLA_CELLA.md` righe 26, 30, 33 e 10; `CONTROLLO_PROVE.md` riga 20.
Testo corretto: `Sulle 240 condizioni comuni a tutte le regole (7200 fotogrammi, delle 300 condizioni della regola adottata) le regole del «libero» scartate danno violazioni in: 932 fotogrammi la lettura al centro della cella; 98 un solo pixel sul suolo; 6 metà dell'impronta senza cella di guardia.`

**10. Capitolo 6, `tab:val-sicurezza`, riga «Celle «libero» nell'ombra vera, regola di partenza» (e la stessa riga in `tab:intro-sintesi`): «131 sequenze senza filtri del costruttore | 2\,907\,032 celle·fotogramma».**
Le 2 907 032 celle·fotogramma sono delle 135 sequenze (131 più 4 con i filtri accesi); 131 è il denominatore dell'intervallo per sequenza.
Prova: `ricontato.txt` righe 158–160; fascicolo 04, §6.1, sesta riga.
Testo corretto: condizioni `tre camere; 135 sequenze, di cui 4 con i filtri del costruttore accesi`; $N$ `2\,907\,032 celle·fotogramma`; intervallo `per sequenza, sulle 131 senza filtri: 0–2,9\,\%`.

**11. Capitolo 1 (sintesi), capitolo 8 (limite 6) e capitolo 9: «bordo stimato: $0{,}30$–$0{,}46$ a $1\unita{s}$» contro capitolo 6 (`tab:val-fuori`): $0{,}459$ ($G_2$) e $0{,}350$ ($G_3$).**
L'intervallo è nelle fonti (`SOLUZIONE_V3.md` riga 164; `VERDETTO_INTEGRAZIONE.md` riga 59), ma unisce due grandezze: $0{,}46$ è la quota dei cinque comportamenti insieme in $G_2$ a $-20\unita{cm}$; $0{,}30$ è la sola cella «prosegue» ($0{,}297$; `PROVA_INSIEME.md` riga 22: «T, «prosegue», 1 s: 0,414 e 0,297 senza c3»). Dal capitolo 6 l'estremo $0{,}30$ non si ricostruisce.
Testo corretto, capitolo 6, riga «bordo dell'ombra stimato … senza la marca», da aggiungere in coda alla cella: `; per il solo «prosegue», in $G_2$ a $1\unita{s}$: $0{,}414$ con $e_\Omega=-0{,}1\unita{m}$ e $0{,}297$ con $-0{,}2\unita{m}$`. Negli altri capitoli: `$0{,}30$–$0{,}46$ a $1\unita{s}$ (estremo basso: chi prosegue)`.

**12. Capitolo 7, `eq:cos-retta` e frase successiva: «Con $n_T=152$ la retta dà circa 50 ms».**
La retta dà $0{,}33+0{,}30\cdot152=45{,}9$ ms; 49,9 ms si ottengono solo con il termine quadratico (`conti_78.txt`). Il fascicolo 05 (riga 135) ha la stessa frase.
Testo corretto: `Con $n_T=152$ la retta dà circa 46 ms, 50 ms con il termine quadratico,`.

**13. Appendice A, riga $t_{\mathrm{conf}}$ («3 misure su 5 a $15\unita{Hz}$» → $0{,}267\unita{s}$) contro capitolo 7 («la sola conferma … chiede 4 cicli, cioè 0,27 s»).**
$0{,}267\unita{s}$ sono 4 periodi, non 3; le due descrizioni vengono entrambe dalla fonte (`f14-classificazione/20-inclusione/BLOCCO_CLASSIFICAZIONE.md` riga 68) e nessun file dice perché tre misure valgano quattro periodi. Non è un errore di trascrizione: va detto in una riga.
Testo corretto (appendice A, colonna «Origine»): `4 periodi a $15\unita{Hz}$: valore usato nei conti per la conferma «3 misure su 5»; il legame fra i due numeri non è documentato nelle fonti`.

### D. Forma

**14.** Capitolo 6, `tab:val-identita`, riga «idem, fuori dal dominio»: cinque casi e solo tre intervalli; manca quello di «1 su 10» (Wilson 1,8–40,4 %). Testo: `0–28\,\% (0 su 10); 2–40\,\% (1 su 10); 6–51\,\%; 31–83\,\%`.

**15.** Capitolo 6, riga 121: «71\,671 dei 175\,802 istanti» è corretto ($175\,802-104\,131$); con la correzione 8 le due frasi diventano coerenti e non serve altro.

---

## Che cosa torna (gruppi controllati alla fonte, con la condizione)

- **Capitolo 6, intervalli e numerosità** (ricalcolo mio, `intervalli.txt`): esempio 826/879; zero su $N$ per 90, 131, 400, 24 835, 13 638, 5600, 5597, 6000, 14 400, 264; $z_{12}$, $z_{45}$; le cinque righe di `tab:val-numerosita` (primo $n$, soglia, $n$ stabile, Wilson, esatto) salvo il punto 6; potenze 0,39, 0,86, 0,83, 0,44, 0,82; 4,2 %, 37,6 %, 73,6 %; Beta: 0,805, 0,848, 68, 110, 9; tutti gli intervalli delle tavole (sicurezza, continuità, soglie, fuori dominio, identità, mobili, bordo, traiettorie pubbliche, 0 su 20 000 a una coda).
- **Capitolo 6, tavole:** copertura per comportamento, soglie, fuori dominio, traiettorie pubbliche e continuità coincidono con il fascicolo 04 (§6.1–6.7); prove d'insieme con `PROVA_INSIEME.md` (tabelle a–g, b, c, d) e `CONTROLLO_PROVE.md` §2; «libero» della cella con `LIBERO_DELLA_CELLA.md`; profondità simulata con `IDENTITA_SU_PROFONDITA.md` righe 50–56 e 75 e `CONTROPROVA_IDENTITA.md` §0, §3, §4; classificazione con `BLOCCO_CLASSIFICAZIONE.md` righe 8, 108, 173.
- **Capitolo 7:** tabella dei tempi e della memoria, le quattro constatazioni, la catena e la dipendenza da $n_T$ coincidono con il fascicolo 05 (righe 47–69, 129–135); lemmi e conti rifatti (`conti_78.txt`); alternative escluse rintracciate nei giudizi (`f8-continuita/16-verdetto` riga 48; `f9-preproposta/13-verdetto` righe 17, 20, 22, 59, 81; `f8-continuita/11-misure/BANCO_DI_PROVA.md` riga 63 per l'ellisse).
- **Capitolo 8:** tabella del portatore (tutte le celle rifatte dalle due formule; coincide con `BLOCCO_CLASSIFICAZIONE.md` righe 74–77); latenza; condizioni di validità; limiti 1–10 contro `SOLUZIONE_V3.md` (righe 61, 81, 164–165, 187–189, 224, 248, 269, 273, 382, 427) e `VERDETTO_INTEGRAZIONE.md` riga 16; tabella del moto contro il fascicolo 02 (righe 168–181).
- **Appendice A:** 42 parametri confrontati con `SOLUZIONE_V3.md` (righe 38, 48, 60, 68–78, 89–90, 99, 104–105, 125–136, 144–160, 216–223, 234–240) e con `BLOCCO_CLASSIFICAZIONE.md` (righe 28, 36, 68): nessuna differenza; **non trovata** in questi file la scomposizione $C=0{,}85+0{,}10\unita{m}$ (il totale $0{,}95\unita{m}$ c'è: `BLOCCO_CLASSIFICAZIONE.md` riga 68). Coincide anche con i valori usati nei capitoli 6–8.
- **Setaccio** (`cerca_cifre.py`, `non_trovate_0*.txt`): capitolo 6, 2 cifre non trovate nelle fonti dirette (una larghezza di colonna; 0,064 %, che è un conto: torna); capitolo 7, 14 non trovate nel fascicolo 05 e ritrovate nei giudizi precedenti o ricalcolate; capitolo 8, A e B, nessuna. Il setaccio dice solo che la cifra esiste, non che la condizione sia giusta.

## Che cosa non ho controllato

- Le cifre dei capitoli 6–8 **non** lette riga per riga alla fonte, ma solo passate al setaccio: circa 700 delle 1025 (fra cui i lavori correlati del capitolo 7, che sono cifre di letteratura: 260 Hz, 22,9 %, 498 su 500 e simili, da controllare contro la mappa «affermazione → chiave» del fascicolo 06).
- Le citazioni e la corrispondenza con `allegato.bib`; i criteri A-4 (riferimenti interni) e A-6 (compilazione).
- Appendice B: le durate delle esecuzioni (4, 2, 12–15 minuti) e i linguaggi.
- Capitolo 8: 13 istanti su 13 del ramo del ritorno; le righe 4–6 della tabella del moto oltre al confronto con il fascicolo 02; la tabella delle misure (protocollo), salvo le potenze.
- Capitolo 6: i pesi della miscela nell'errore mediano del punto; «0,68» della regola di lettura (2); se 3 588 836 celle·fotogramma siano il totale delle due risoluzioni o di ciascuna.
- Nessun file grezzo (`.tsv`, `.json`, `.jsonl`) riaperto: mi sono fermato ai fascicoli, ai loro riconteggi e ai giudizi.

## File accanto

`PREVISIONI.md`; `intervalli.py` con `mini.py` → `intervalli.txt`; `conti_78.py` → `conti_78.txt`; `cerca_cifre.py` → `non_trovate_06.txt`, `non_trovate_07.txt`, `non_trovate_08AB.txt`; `g.py` (ricerca di una cifra nelle fonti, con il contesto).
