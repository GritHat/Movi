# Ultime correzioni dell'allegato tecnico (cartella `40-definitivo`)

14 novembre 2026. Partenza: copia di `30-finale` senza i file ausiliari. Sigle: **D** = controllo delle dimostrazioni (`31-…`), **C** = controllo di coerenza (`32-…`), **N** = controllo delle cifre (`33-…`). Le sostituzioni sono in `strumenti/applica_ultime_1…4.py` (90 in tutto, ciascuna trovata una volta sola), più due ritocchi a mano dopo la rilettura.

## In testa

- **Numero di pagine: 71** (erano 70). Le correzioni aggiungono condizioni e limiti: 8 054 caratteri netti nei capitoli (da 326 751 a 334 805). Alla prima compilazione le pagine erano 72; ho accorciato i testi introdotti e lasciato flottare due tabelle (`tab:occ-dominio`, `tab:val-mobili`: da `[H]` a `[!htb]`) che lasciavano mezza pagina bianca. Tornare a 70 chiede di togliere contenuto: non l'ho fatto.
- **Compilazione** (xelatex, bibtex, xelatex, xelatex): 0 errori, 0 riferimenti o citazioni indefiniti, 0 avvisi di BibTeX, 0 «Overfull \hbox» (`strumenti/esito_compilazione.txt`). **Riferimenti interni** (`controlla_interni.py`): 0 occorrenze, 0 eccezioni; nel testo del PDF nessuna delle parole vietate. Frontespizio: resta il segnaposto «[nomi degli autori]». `allegato.bib`, `preambolo.tex` e `allegato_tecnico.tex` sono identici a quelli di `30-finale`.
- **Cambio di stato.** `prop:occ-contenimento`: «dimostrato» solo per la lettura per punto esatta (margine di lettura e tolleranza di misura nulli); con il margine di lettura il contenimento dell'intera impronta è **non dimostrato** (controesempio di D-R1, che ho rifatto: striscia larga ρ·m(z₀)/z₀ = 10,9 cm a 2,5 m e 14,4 cm a 3 m con k = 0,004).
- **Regole.** Scritto solo in questa cartella; niente git, sudo, rete. Non verificato da me: i simulatori, i file grezzi delle cifre (mi sono affidato ai riconti di N, salvo dove dico «riscontrato»), la conformità dei programmi alle regole. Indipendenza: condivido con i tre controlli il testo, i file d'origine e il modello linguistico.
- **Previsioni** (`PREVISIONI.md`): P1 regge; P2 smentita (0 «Overfull»); P3 regge (71); P4 regge; P5 regge; P6 regge.

## D — dimostrazioni

| N. | Oggetto | Esito |
|---|---|---|
| D-R1 | contenimento falso con il margine di lettura (cap. 5; richiami cap. 1 e 9) | **applicata, con due modifiche**: nell'enunciato ho aggiunto «tolleranza di misura nulla nella (i)» (la stessa striscia nasce da qualunque tolleranza positiva); delle quattro larghezze tengo le due con k = 0,004, rifatte da me, e tolgo le due con k = 0,0100. Aggiunta nel sommario la condizione «per una lettura esatta del suolo, senza il margine che il sistema usa» |
| D-R2 | fascia di guardia: (ii) per il centro; «riportato come osservato» | **applicata, con modifiche**: la (ii) ora dice «fuori dall'ombra, in campo e in portata *da un tempo* $t_a$» (è ciò che la dimostrazione usa); la frase su $P_D<1$ è entrata senza la cifra 0,81, che nel cap. 4 non c'è |
| D-R3 | $t_a$ nei simboli e in appendice A | applicata; adeguata anche la voce «fascia di guardia» dei simboli, che diceva «età del dato» |
| D-R4 | lo zero di «nascosto fuori da $W$» non viene dalla Proposizione della fascia (cap. 6) | applicata, accorciata |
| D-R5 | etichetta: «la sicurezza non dipende dall'etichetta» | applicata nei cap. 4, 5, 8, 9 **e nel riquadro del cap. 1**, che D non elencava; forma unica: «non produce un «libero» né riduce un avviso acceso; può cambiare l'esito di un riaggancio, e quindi gli ingressi successivi» |
| D-R6 | regione di ripiego: Definizione e testo dicevano due insiemi | applicata: decide la descrizione di progetto («tutta la maschera dentro il cuneo», `SOLUZIONE_V3.md` r. 147 e 157). Quale insieme usi il programma: non verificato |
| D-R7 | riquadro del cap. 3, parte (b) a posa esatta | applicata |
| D-R8 | conclusioni, fascia: manca la (ii) | applicata, fusa con C-R9 |
| D-R9 | tabella del cap. 1, prima riga | applicata |

## C — coerenza

| N. | Oggetto | Esito |
|---|---|---|
| C-R1 | avviso da scheda: lo zero senza la configurazione | applicata (cap. 1 e 9), nella forma di N-R2 («con i gruppi a celle forti e l'avviso che resta dopo il riaggancio»; 180 e 271 con la configurazione di riferimento) |
| C-R2 | prova d'ingresso (5) | applicata, accorciata |
| C-R3 | frase per settori mai generata | applicata. **Non applicata** l'aggiunta al paragrafo «Uso» del profilo: che non sia mai stato eseguito non è verificato |
| C-R4 | «8 su 90 / 1 su 140» | applicata (cap. 1 e 8), nominando la grandezza: «riagganci a soggetto ancora nascosto in 11 e 6 / 1 e 1 passaggi su 140» (riscontrato su `IDENTITA_SU_PROFONDITA.md` r. 52). Che «8 su 90» misuri la stessa grandezza: non verificato, e il testo ora non lo afferma |
| C-R5 | ostacoli fermi: 84 su 84 e 10 su 10 | applicata: riga aggiunta a `tab:val-mobili` (riscontrata sul fascicolo di valutazione, r. 221) |
| C-R6 | regola «mobile»: 5 su 90 senza il costo | applicata, accorciata |
| C-R7 | altezza dell'ostacolo: 1,61 e 1,65 m | applicata (riscontrata su `tab:geo-amin`) |
| C-R8 | due «velocità coperte» | applicata, accorciata |
| C-R9 | fascia: «contiene il soggetto» | applicata (cap. 1, 8, 9) |
| C-R10 | soglia della continuità | **applicata in altra forma**: «la soglia 0 è rispettata solo dove l'ingresso è riconosciuto». Non scrivo «23 378 con la regola aggiuntiva»: la regola accende l'avviso, non risulta che emetta una regione (incompatibile con N-R6, che conta 22 474; decide il riconto sul grezzo). Non scrivo «su tutti i passaggi la soglia non è raggiunta»: 248 dei 928 sono tracce non confermate, e non è verificato che stiano nella base della soglia |
| C-R11 | «corpo esteso» per tutti i 23 402 passaggi | applicata (cap. 6, condizioni comuni e riga della tabella) |
| C-R12 | sommario | applicata, fusa con N-R6 e D-R1 |
| C-R13 | secondo soggetto: «l'avviso resta» | applicata (0 su 336 è la cifra del cap. 5; il cap. 6 riporta un'altra scena, 0 su 264: non riconciliate) |
| C-R14 | intervalli dell'identità e regola d'arrotondamento | applicata (cap. 1, 4, 8; Wilson rifatto: 94,43–99,13 e 92,92–98,46). La regola dichiarata nomina l'unica eccezione trovata da N (0,875 scritto 0,87) |
| C-R15 | regole attive solo dopo le prove d'ingresso | applicata (cap. 1, 8, 9), accorciata |
| C-R16 | frontespizio | nessuna modifica: resta il segnaposto |
| C-R17 | cinque parafrasi dello stato dei lavori | applicate; adeguata anche la frase d'apertura dell'appendice A, che rimandava alla marca «da misurare» |
| C-R18 | (a) «principio analogo»; (b) virgola; (c) «24–34 %» | (a) e (b) applicate; (c) sciolta con N-R4 |

## N — cifre

| N. | Oggetto | Esito |
|---|---|---|
| N-R1 | i due denominatori dell'avviso (cap. 6) | applicata |
| N-R2 | avviso: configurazione dello zero | applicata (vedi C-R1) |
| N-R3 | «prova singola» della regola «mobile» | applicata, in forma più breve; la variante facoltativa (11 prove invece di «al più 13») **non applicata**: il limite superiore scritto è vero |
| N-R4 | origine del «24–34 %» | applicata nei cap. 1, 6, 8 e in appendice B (24,1 %, 34,4 % e 6,3 % riscontrati su `confronto_profondita.txt`). **Tolto** «con un esemplare di pre-produzione» e «una scala ripresa da vicino»: non li ho ritrovati. La registrazione del costruttore resta senza voce di bibliografia |
| N-R5 | definizione di «occupato» nel cap. 4 | applicata |
| N-R6 | continuità: condizioni | applicata (sommario, cap. 1, 5, 6, 8, 9), **con una scelta**: il limite è scritto «meno di 7 su 10 000», con le due letture (6,4 e 6,8) nel cap. 5 e nel cap. 6; rifatto: 3,84/6003,84 = 0,064 % e 3,84/5622,3 = 0,068 %. Nel sommario non entra la ripartizione per $P_D$ (sta nei cap. 1, 5, 6, 9). Adeguato anche l'invariante 10 del cap. 8, che nessun controllo elencava |
| N-R7 | appendice A, libreria dei percorsi | applicata |
| N-R8 | velocità di classe ipotizzate; intestazione | applicate |

## Punti discutibili

**Sciolti** (da `NOTE_FINALI.md`): 1 «prova singola» (N-R3); 2 «24–34 %» (N-R4); 3 due definizioni di «occupato» (N-R5); 5 denominatori dell'avviso (N-R1); 9 «10 classi dopo il contatto» (ricontato da N).

**Rimasti.**
1. Contenimento con il margine di lettura: vale una forma più debole (impronta contenuta in $\Pres$ dilatato della striscia)? Non risolto; lo decide una dimostrazione con il raggio aumentato o un controesempio.
2. Limite della continuità fra 6,4 e 6,8 su 10 000: lo decide un conteggio per camminatore, che chiede di rieseguire la simulazione.
3. Regione di ripiego, insieme «nascosto» dello zero di $W$, paragrafo «Uso» del profilo: la conformità dei programmi non è verificata.
4. «8 su 90» e «11 e 6 su 140» sono la stessa grandezza? «0 su 336» e «0 su 264» sono due scene? Non verificato.
5. Cifre mai ricontate dal grezzo («87 su 2800», «9 su 2800», «193 su 193», «11 946 289 istanti»); condizioni aggiunte dalla verifica delle citazioni; segno dell'errore d'inclinazione; la «linea a 2,1 m»; voci di bibliografia mancanti; anno di una voce: come in `NOTE_FINALI.md`.
6. Lunghezza: 71 pagine contro «una trentina» del contratto. Decide l'utente.
7. I nomi degli autori: riga 3 di `allegato_tecnico.tex`.

## Rilettura a freddo (sommario, capitolo 1, conclusioni nel PDF)

Letti per intero nel testo estratto dal PDF (`strumenti/definitivo.txt`: pagine 2, 5–10 e 61–63 del file), con la pagina dei simboli. Corretto: nei contributi, la regione «non si svuota» ora porta anche «e l'ostacolo è fermo», come la Proposizione; nella dimostrazione della fascia un pronome senza antecedente. Capitoli 2, 3, 6, 7 e 8 **non** riletti per intero: solo i passi toccati.
