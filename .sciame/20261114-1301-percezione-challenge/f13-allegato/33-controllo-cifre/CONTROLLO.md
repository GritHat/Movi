# Controllo finale delle cifre toccate dalle correzioni (allegato tecnico, `30-finale/`)

14 novembre 2026, dalle 19:57:20 alle 20:12 (`date -Is`). Oggetto: i 13 file `.tex` di `30-finale/capitoli/` come sono ORA. Programmi e uscite accanto a questo file.

## 0. In testa: esito, previsioni, regole, indipendenza

**Esito.** Le cifre introdotte dalle correzioni sono quelle dei file d'origine e sono state cambiate in tutti i punti: **0 punti rimasti al valore vecchio**. Intervalli di Wilson: **156 estremi ricalcolati, 155 coincidono**; l'unico diverso è un troncamento prudente. I **quattro punti «discutibili» sono tutti sciolti** sui file grezzi e sui programmi. Restano **8 correzioni** (R1–R8) e una facoltativa (R9, dentro R3): R1 e R6 correggono una condizione sbagliata, R2, R4 e R6 aggiungono condizioni mancanti, R3 scioglie una riserva, R5 toglie una clausola che non corrisponde al programma, R7 riguarda una riga dell'appendice A senza riscontro nei capitoli, R8 raccoglie due ritocchi minori. Le cifre su classificazione e profili tornano tutte.

**Previsioni** (`PREVISIONI.md`, ore 19:57:37, scritte dopo aver letto solo `CORREZIONI_APPLICATE.md` e `NOTE_FINALI.md`).
- validazione-P1, almeno 3 punti rimasti al valore vecchio: **smentita** (0 trovati).
- validazione-P2, almeno il 90 % degli intervalli coincide e almeno 1 no: **regge** (155 su 156; il diverso è «0,87» per 0,8751, troncato verso il basso: prudente, non un errore).
- validazione-P3, almeno 2 punti discutibili su 4 sciolti: **regge** (4 su 4).
- validazione-P4, almeno una riga dell'appendice A diversa dai capitoli: **regge** (una: R7).
- validazione-P5: prima parte **regge** (tutte le cifre tornano); seconda parte (un'ipotesi non dichiarata nei capitoli 4, 5, 8) **smentita**: lì sono tutte dichiarate; manca solo nella riga di sintesi del capitolo 1 (R8).

**Regole.** L'ambiente chiede di non scrivere rapporti `.md`; la consegna chiede questo file e `PREVISIONI.md`: ho seguito la consegna. Ho aperto in sola lettura file fuori dall'elenco della consegna, perché sono i grezzi delle cifre: `f12-integrazione/30-arbitro/riconteggio2.txt` e il suo programma, `f12-integrazione/06-identita/catena/*.py` e `risultati/*.jsonl`, `07-controprova-identita/risultati/*.jsonl`, `f10-dati/21-statistica/tabelle/`, `f10-dati/12-dati-veri/manifesto.json`, una pagina già scaricata in `06-bibliografia/scaricati/` (letta come dato), `f14-classificazione/01-profili/classi.json` e `profili_portatore.json`. Niente git, sudo, rete. Scritto solo in questa cartella. L'allegato non è stato modificato.

**Indipendenza.** I programmi sono miei e non importano niente dal progetto. Condividono con gli autori i file grezzi, il significato dei loro campi e i simulatori che li hanno prodotti: nessun simulatore è stato rieseguito. Un difetto del simulatore resta invisibile a questo controllo.

## 1. Correzioni residue

Ogni testo corretto è una riga di `prova_latex/correzioni.tex`, compilato con il preambolo dell'allegato (xelatex: 0 errori, 0 «Overfull»; riferimenti e citazioni restano indefiniti solo perché il frammento è isolato).

### R1. Capitolo 6, `tab:val-sicurezza`, ultima riga: la spiegazione dei due denominatori è incompleta (falso per omissione)

- **Dove.** `06_valutazione.tex` r. 149: «4324 e 4325 fotogrammi (3921 e 3922 senza la disposizione in cui il soggetto si allontana nell'ombra)».
- **Che cosa non torna.** La differenza di 403 fotogrammi non è la sola disposizione: è la somma di 297 fotogrammi (i 10 passaggi di quella disposizione, in cui il soggetto non ricompare) e di 106 fotogrammi (i 10 passaggi al livello limite di rumore). 4324 e 4325 sono su 150 passaggi, 3921 e 3922 su 130 al livello nominale.
- **Prova.** `riconta_avviso.py` sui grezzi `nuovi424.jsonl` e `nuovi848.jsonl`: 4324 = 786 + 106 + 552 + 1919 + 664 + 297; 4324 − 297 − 106 = 3921; 4325 − 297 − 106 = 3922; senza avviso 180 e 271 (configurazione di riferimento), 0 e 0 (con l'avviso che resta). Replica: 3608 in 120 passaggi. Il punto 5 di `NOTE_FINALI.md` è **sciolto**.
- **Testo corretto** (la riga intera).

```latex
Soggetto nascosto entro $3\unita{m}$ fuori dall'avviso, seconda serie (424 e 848 px) & configurazione di riferimento / con l'avviso che resta dopo il riaggancio & 180 e 271 / 0 e 0 & 4324 e 4325 fotogrammi in 150 passaggi (3921 e 3922 tolti i 10 passaggi al livello limite, 106 fotogrammi, e i 10 in cui il soggetto si allontana nell'ombra e non ricompare, 297 fotogrammi); replica: 0 su 3608 per risoluzione & — & II \prova{S}\\
```

### R2. Capitolo 1 (`tab:intro-sintesi`, riga «Avviso di possibile presenza») e capitolo 9: lo zero è dato senza la configurazione (più forte dei file)

- **Dove.** `01_introduzione.tex` r. 98: «Da scheda: soggetto nascosto entro $3\unita{m}$ senza avviso in 0 fotogrammi su 4324 […]». `09_conclusioni.tex` r. 19: «Un soggetto nascosto entro $3\unita{m}$ non resta senza avviso (0 fotogrammi su 4324 […])».
- **Che cosa non torna.** Lo zero vale con i gruppi a celle forti e l'avviso che resta dopo il riaggancio. Sugli stessi passaggi la configurazione di riferimento lascia il soggetto senza avviso in 180 e 271 fotogrammi (lo dice il capitolo 6). Il capitolo 1 promette che «ogni riga dice da quale catena viene».
- **Prova.** `riconta_avviso_uscita.txt`, righe «prima TOTALE» e «tutte_p TOTALE».
- **Testo corretto.** Capitolo 1, la riga intera:

```latex
Avviso di possibile presenza & ideale; un soggetto per ombra & soggetto nascosto dentro l'area d'avviso per costruzione; avviso non acceso in 29 passaggi su $95\,399$ (ombra esatta) e in 15 su 2000 (ombra stimata più stretta di $0{,}20\unita{m}$). Da scheda, con l'avviso che resta dopo il riaggancio: soggetto nascosto entro $3\unita{m}$ senza avviso in 0 fotogrammi su 4324 a 424 pixel di larghezza e in 0 su 4325 a 848 (con la configurazione di riferimento, sugli stessi 150 passaggi, in 180 e in 271), e in 0 su 3608 per risoluzione in una replica. Dietro un ostacolo fermo l'avviso resta acceso; che l'avviso termini quando il suolo è rivisto dopo la rimozione dell'ostacolo non è sostenuto: nella realizzazione provata resta acceso dopo $2\unita{s}$ in 10 prove su 10 (72--100\,\%), per una causa non determinata & \prova{D}\prova{S} & \S\ref{sec:occ}\\
```

Capitolo 9, inizio del terzo punto di «Che cosa è verificato in simulazione» (fino a «in una replica).»):

```latex
\emph{Su profondità simulata dalle schede tecniche.} Con i gruppi a celle forti e l'avviso che resta dopo il riaggancio, un soggetto nascosto entro $3\unita{m}$ non resta senza avviso (0 fotogrammi su 4324 a 424 pixel di larghezza e 0 su 4325 a 848, e 0 su 3608 per risoluzione in una replica); con la configurazione di riferimento, sugli stessi passaggi, resta senza avviso in 180 e in 271 fotogrammi.
```

### R3. Capitolo 4, didascalia di `tab:sti-mobile`: la «prova singola» si rifà (punto discutibile 1, sciolto)

- **Dove.** `04_stima.tex` r. 50: «Prova singola: valori del calcolo d'origine […] lo scarto dai valori in tabella non è spiegato.»
- **Che cosa non torna.** Lo scarto è spiegato. 0,853 e 0,371 usano la soglia a 3 m e, per la dispersione, lo scarto tipo alle distanze dei due capi della finestra (2,97 e 2,53 m); 0,815 e 0,389 usano lo scarto tipo a 3 m a entrambi i capi. Le due coppie sono giuste, ciascuna con la sua condizione. La colonna resta com'è.
- **Prova.** Programma d'origine `03-stima/ricalcoli.py` r. 64–72 (letto); `conti.py` mio: (A) 0,8151 e 0,3888; (B) 0,8527 e 0,3707.
- **Testo corretto** (la didascalia intera).

```latex
\caption{Regola «mobile», oggetto a $0{,}5\unita{m/s}$: quota di tracce etichettate entro $1\unita{s}$. In simulazione, con modello ideale del sensore (centro puntiforme, rumore gaussiano indipendente e noto, $15\unita{Hz}$) \prova{S}. Da $2\unita{m}$: di traverso o in avvicinamento, tre curve di rumore; da $3\unita{m}$: in avvicinamento. Prova singola \prova{C}: probabilità che scatti la sola prova alla finestra massima, $T_w=0{,}867\unita{s}$ (spostamento $0{,}433\unita{m}$), con la soglia \eqref{eq:sti-soglia} calcolata alla distanza di partenza, la maggiore ($0{,}367$ e $0{,}459\unita{m}$ a $3\unita{m}$ per le curve pessimista e severa), e la dispersione della differenza calcolata con lo scarto tipo alle distanze dei due capi della finestra, $2{,}97$ e $2{,}53\unita{m}$ ($\sigma_\delta=0{,}063$ e $0{,}079\unita{m}$): il soggetto si avvicina e al secondo capo il rumore è minore. Con lo scarto tipo a $3\unita{m}$ a entrambi i capi, come nella Proposizione~\ref{prop:sti-mobile} alla lettera, si ottengono $0{,}815$ e $0{,}389$. Con la curva severa la prova singola sovrastima la simulazione, perché la regola usa la maggiore delle distanze \emph{misurate}, che il rumore gonfia. Le percentuali della prima colonna sono quelle stampate dalla simulazione; i conteggi sono dedotti.}\label{tab:sti-mobile}
```

Facoltativa, stesso capitolo (r. 47, «le prove sono al più 13 per asse»): nel programma della simulazione le prove sono 11 (`sim_v2.py`, funzione `mob_final`: dal quinto al quindicesimo fotogramma); 13 è un limite superiore.

```latex
Nel primo secondo di una traccia a $15\unita{Hz}$ le prove sono 11 per asse nella regola simulata (dal quinto al quindicesimo fotogramma) e in ogni caso al più 13: per la disuguaglianza dell'unione la probabilità di almeno un'etichetta falsa è $\le2\cdot13\cdot5{,}7\cdot10^{-7}=1{,}5\cdot10^{-5}$.
```

### R4. Capitoli 1, 6, 8 e appendice B: l'origine del «24–34 %» (punto discutibile 2, sciolto)

- **Dove.** `01_introduzione.tex` r. 130; `06_valutazione.tex` r. 288; `08_limiti.tex` r. 173 («contro 24--34\,\% in registrazioni pubbliche»); `B_riproducibilita.tex`, «Tipi di prova».
- **Che cosa non torna.** Manca la condizione. Sono 24,1 % e 34,4 %: pixel senza dato fra quelli in cui la scena sta fra 0,5 e 3 m, primi 60 fotogrammi, in due registrazioni di camere a stereo attivo (una sequenza al chiuso con una persona; una registrazione di esempio del costruttore, una scala ripresa da vicino). Il termine di confronto 7,8 % è la stessa grandezza al livello limite (1,7 % al nominale). Una terza registrazione, con sensore a luce strutturata, dà 6,3 %: «registrazioni pubbliche» senza altro è più largo dei dati. L'appendice B non nomina la registrazione del costruttore, che invece produce una cifra.
- **Prova.** `f10-dati/21-statistica/tabelle/confronto_profondita.txt` r. 4, 7, 12, 13, 14 e `controlli_brevi.txt` r. 24 e 27; `manifesto.json` (voce della scala: camera della famiglia D435, 1280 × 720). Nello stesso file una seconda registrazione a luce strutturata dà 12,2 % (r. 15) e una terza a stereo attivo ha la scena a 0,35 m, fuori dall'intervallo (r. 11): per questo il testo dice «due registrazioni con cui è stato confrontato» e non «le registrazioni pubbliche».
- **Testo corretto.** Capitolo 1:

```latex
Il simulatore da scheda produce meno pixel senza dato di due registrazioni pubbliche di camere a stereo attivo con cui è stato confrontato: fra i pixel in cui la scena sta fra $0{,}5$ e $3\unita{m}$, $1{,}7\,\%$ al livello nominale e $7{,}8\,\%$ al livello limite, contro $24{,}1\,\%$ in una sequenza al chiuso con una persona \cite{depthtrack} e $34{,}4\,\%$ in una registrazione di esempio del costruttore (primi 60 fotogrammi di ciascuna; camere, risoluzioni e scene diverse da quelle simulate). Le cifre al livello nominale sono ottimistiche.
```

Capitolo 6 (da «Il simulatore è verificato» a «osservati).»):

```latex
Il simulatore è verificato contro il proprio modello, non contro una camera: confrontato con due registrazioni pubbliche di camere a stereo attivo, sottostima i pixel senza dato. Fra i pixel in cui la scena sta fra $0{,}5$ e $3\unita{m}$, nei primi 60 fotogrammi, i pixel senza dato sono 1,7\,\% al livello nominale e 7,8\,\% al livello limite, contro 24,1\,\% in una sequenza al chiuso con una persona \cite{depthtrack} e 34,4\,\% in una registrazione di esempio del costruttore (una scala ripresa da vicino, con un esemplare di pre-produzione); una registrazione con un sensore a luce strutturata \cite{tum-rgbd} dà 6,3\,\%. Camere, risoluzioni e scene non sono quelle simulate: il confronto dà il verso dello scarto, non la sua misura.
```

Capitolo 8:

```latex
Il simulatore sottostima i pixel senza dato ($7{,}8\,\%$ al livello limite contro $24{,}1\,\%$ e $34{,}4\,\%$ in due registrazioni pubbliche di camere a stereo attivo, fra i pixel in cui la scena sta fra $0{,}5$ e $3\unita{m}$ \prova{P}; \S\ref{sec:val}): le cifre al rumore nominale sono ottimistiche.
```

Appendice B (la frase «I dati pubblici sono […]»):

```latex
I dati pubblici sono traiettorie di pedoni al chiuso con verità di riferimento \cite{thor}, che non contengono profondità, sequenze di profondità registrate \cite{tum-rgbd,depthtrack} e una registrazione di esempio distribuita dal costruttore di una delle camere, fatta con un esemplare di pre-produzione e usata solo per il confronto dei pixel senza dato (\S\ref{sec:val}).
```

La voce di bibliografia della registrazione del costruttore è stata tolta dal `.bib`: se la si vuole citare va rimessa (decide chi cura la bibliografia); il testo sopra compila senza.

### R5. Capitolo 4, definizione di cella occupata: non corrisponde al programma (punto discutibile 4, sciolto)

- **Dove.** `04_stima.tex` r. 17: «[…] con quota $y\in[0{,}07;\,2]\unita{m}$ ed è il primo ritorno lungo il suo azimut.»
- **Che cosa non torna.** Nel programma che ha prodotto tutte le cifre su profondità simulata una cella è occupata se ha almeno 3 punti d'ostacolo, anche oltre la prima cella occupata del suo azimut; «in ombra» è «oltre la prima e non occupata». È la definizione del capitolo 3, che è giusta. I gruppi sono formati su tutte le celle occupate.
- **Prova.** `f12-integrazione/06-identita/catena/mappa.py` r. 117–132 (`occupato = n_ost >= soglia`; `ombra = oltre & ~occupato`; `stati[occupato] = OCCUPATO`), identico nella seconda copia della catena; `gruppi.py` r. 63.
- **Testo corretto** (la prima frase del capoverso).

```latex
Una cella $(\varphi,\rho)$ della mappa polare ($1^\circ\times0{,}1\unita{m}$, $\rho\le3\unita{m}$) è «occupata osservata» se contiene almeno $n_{\min}=3$ punti di profondità con quota $y\in[0{,}07;\,2]\unita{m}$: è la definizione del \S\ref{sec:map}, e vale anche per una cella che sta oltre la prima cella occupata del suo azimut.
```

### R6. Continuità: condizioni mancanti e una sbagliata (sommario, capitoli 1, 5, 6, 9)

- **Dove.** `06_valutazione.tex` r. 165 («idem, prove d'insieme & corpo esteso; 12 configurazioni $\times$ 5 comportamenti») e r. 142; `01_introduzione.tex` r. 94; `00_sommario.tex`; `05_occlusione.tex` r. 209; `09_conclusioni.tex` r. 17.
- **Che cosa non torna.** (a) Le 12 configurazioni non sono «corpo esteso»: sono 3 disposizioni × $P_D$ 0,9 e 0,7 × corpo esteso e puntiforme (11 408 passaggi con corpo esteso, 11 994 con corpo puntiforme). Le «condizioni comuni» del capitolo 6 dicono $P_D=0{,}9$, quindi la riga deve dire che qui non vale. (b) Il 3,97 % mescola i due valori di $P_D$: 852 dei 928 passaggi sono a $P_D=0{,}7$ (7,28 %), 76 a $P_D=0{,}9$ (0,65 %); con la regola aggiuntiva 22 e 2. (c) «0 interruzioni su 23 402 passaggi; l'ingresso non è riconosciuto in 928 di essi» è incoerente alla lettera: dove la traccia non entra non c'è regione. I vuoti sono contati dopo l'ingresso; la traccia entra nell'ombra in 22 474 passaggi. (d) Il limite «6,4 su 10 000» suppone che tutti i 6000 camminatori abbiano almeno un passaggio con la premessa: i file non hanno una riga per passaggio e non lo dicono; nel caso peggiore (tolti 598/4 camminatori mai nascosti e 928/4 senza ingresso) il limite è 6,8, cioè «meno di 7 su 10 000». **Non risolto** quale dei due valga.
- **Prova.** `riconta_continuita.py` sulle 120 righe «R» dei file `a_*` di `02-prova-insieme/ris/`: confermati 23 154, non confermati 248, vuoti 0; scoperti 928 = 506 + 346 + 40 + 36 senza la regola, 24 = 17 + 5 + 1 + 1 con la regola; 1 e 17 su 5704 (corpo esteso) tornano.
- **Testo corretto.** Capitolo 6, riga della tabella della continuità:

```latex
idem, prove d'insieme & 12 configurazioni (3 disposizioni, $P_D=0{,}9$ e $0{,}7$, corpo esteso e puntiforme) $\times$ 5 comportamenti; vuoti contati dopo l'ingresso nell'ombra & 0 & 23\,402 passaggi nascosti (6000 soggetti distinti); traccia entrata nell'ombra in 22\,474 & 0–0,064\,\% se tutti i 6000 soggetti hanno un passaggio con la traccia entrata; meno di 0,07\,\% nel caso peggiore\\
```

Capitolo 6, riga «Traccia chiusa prima dell'ombra» di `tab:val-sicurezza`:

```latex
Traccia chiusa prima dell'ombra (avviso non acceso) & senza / con l'avviso mantenuto per le tracce chiuse entro $0{,}75\unita{m}$ dall'ombra; 12 configurazioni: 3 disposizioni, $P_D=0{,}9$ e $0{,}7$, corpo esteso e puntiforme & 928 / 24 & 23\,402 passaggi nascosti (11\,701 per valore di $P_D$) & quote: 3,97\,\% / 0,10\,\%; con $P_D=0{,}9$: 76 / 2 (0,65\,\% / 0,02\,\%); con $P_D=0{,}7$: 852 / 22 (7,28\,\% / 0,19\,\%) & I \prova{S}\\
```

Capitolo 1, riga «Continuità»:

```latex
Continuità & ideale; 12 combinazioni (3 disposizioni, $P_D=0{,}9$ e $0{,}7$, corpo esteso e puntiforme) per 5 comportamenti; premessa: ingresso nell'ombra riconosciuto & 0 passaggi con un ciclo senza regione dopo l'ingresso, su $23\,402$ passaggi nascosti (6000 camminatori distinti: al più $6{,}4$ su $10\,000$, meno di 7 se si tolgono i camminatori senza un passaggio con la premessa, nel caso peggiore); premessa mancata in 928 passaggi su $23\,402$ ($3{,}97\,\%$; 852 dei 928 con $P_D=0{,}7$), in 24 ($0{,}10\,\%$) con l'avviso acceso anche per le tracce chiuse entro $0{,}75\unita{m}$ da un'ombra, regola attiva solo dopo la prova d'ingresso sul suolo vuoto. Con corpo puntiforme: 0 su $24\,835$ $[0;\,0{,}016\,\%]$. Da scheda la regola della regione persistente non è stata eseguita & \prova{D}\prova{S}\prova{N} & \S\ref{sec:occ}, \S\ref{sec:val}\\
```

Sommario (al posto di «la regione di previsione è emessa […] con una regola aggiuntiva),»):

```latex
la regione di previsione è emessa a ogni ciclo dell'occlusione, una volta riconosciuto l'ingresso nell'ombra (0 interruzioni dopo l'ingresso su $23\,402$ passaggi nascosti; l'ingresso non è riconosciuto in 928 di essi, in 24 con una regola aggiuntiva; metà dei passaggi ha probabilità di rilevamento $0{,}7$ per fotogramma, l'altra metà $0{,}9$),
```

Capitolo 9 (prime due frasi del primo punto di «Che cosa è verificato in simulazione», fino a «(\S\ref{sec:lim-salute}).»):

```latex
\emph{Con modello ideale del sensore.} La regione è emessa a ogni ciclo dell'occlusione dopo l'ingresso: 0 passaggi con un'interruzione su $23\,402$ passaggi nascosti, da 6000 soggetti distinti (12 combinazioni: 3 disposizioni, $P_D=0{,}9$ e $0{,}7$, corpo esteso e puntiforme); la premessa, cioè l'ingresso nell'ombra riconosciuto, manca in 928 passaggi su $23\,402$ ($3{,}97\,\%$; 76 con $P_D=0{,}9$ e 852 con $P_D=0{,}7$), e in 24 ($0{,}10\,\%$; 2 e 22) con l'avviso acceso anche per le tracce chiuse entro $0{,}75\unita{m}$ da un'ombra, regola attivata solo dopo la prova d'ingresso sul suolo vuoto (\S\ref{sec:lim-salute}).
```

Capitolo 5, r. 209 (da «I 23\,402 passaggi» a «(3,97\,\%);»):

```latex
I 23\,402 passaggi nascosti della prova su semi nuovi (12 combinazioni: 3 disposizioni, $P_D=0{,}9$ e $0{,}7$, corpo esteso e puntiforme) vengono da 6\,000 camminatori distinti: il limite superiore al 95\,\% è «meno di 6,4 passaggi su 10\,000», non quello che si otterrebbe trattando i passaggi come indipendenti. La premessa è l'ingresso: nella stessa prova la traccia è chiusa prima dell'ombra in 928 passaggi su 23\,402 (3,97\,\%: 76 su 11\,701 con $P_D=0{,}9$ e 852 su 11\,701 con $P_D=0{,}7$), e lo zero vale per i 22\,474 passaggi restanti;
```

### R7. Appendice A, riga «libreria di taratura dei percorsi»: non ha riscontro nei capitoli

- **Dove.** `A_parametri.tex` r. 54: «libreria di taratura dei percorsi & almeno 200 percorsi, due persone, tre andature & \S\ref{sec:val}».
- **Che cosa non torna.** Nel capitolo indicato e nel capitolo 5 la libreria è di 400 percorsi simulati; «200 percorsi, due persone, tre andature» non compare in nessun capitolo. Nel documento d'origine è un requisito per una libreria futura, non un parametro delle prove. Che cosa la fonte intenda oltre alle tre cifre: non verificato.
- **Prova.** Ricerca nei 13 file (`cerca_py.py`): le tre espressioni stanno solo nell'appendice A; `SOLUZIONE_V3.md` r. 160 e r. 374.
- **Testo corretto** (la riga).

```latex
--- & libreria di percorsi ricavata da camminate di persone (non realizzata) & almeno 200 percorsi, due persone, tre andature & requisito di progetto; nelle prove la libreria è di 400 percorsi simulati (\S\ref{sec:occ}) & scelto\\
```

### R8. Minori: una condizione nella sintesi e un'intestazione

- Capitolo 1, riga «Avviso tempestivo per classe»: «3 classi su 15» dipende dalle velocità di classe, di cui 21 su 30 sono senza fonte consultata; i capitoli 4 e 5 lo dicono, la riga di sintesi no.

```latex
Avviso tempestivo per classe & portata $3\unita{m}$, avvicinamento frontale, reazione di $1{,}0\unita{s}$ ipotizzata; velocità delle classi in parte ipotizzate (\S\ref{sec:sti}) & fino a $1{,}44\unita{m/s}$: 3 classi su 15 alla velocità tipica, 0 su 15 alla massima & \prova{C} & \S\ref{sec:occ}, \S\ref{sec:lim}\\
```

- Capitolo 4, `tab:sti-profili`, intestazione «acc. / frenata (m/s$^2$)»: i valori sono i massimi di classe (`classi.json`, campi `a_max` e `dec_max`).

```latex
Classe & $v$ tipica / massima (m/s) & acc. / frenata massime (m/s$^2$) & Gradi di libertà e modello di moto\\
```

## 2. Che cosa torna (una riga per parte)

1. **Cifre delle correzioni contro l'origine** (aperti i grezzi o i fascicoli, non `CIFRE.md`): 135 sequenze (131 + 4) e 2 907 032; 5,7 / 2,7 / 6,7 cambi al secondo; 400 su 400 con $P_D=1$; raggio al 95 % di 3,49 m; 190 su 190 in 19 sequenze, 3 al limite; 323/342, 283/339, 226/282; riga $q=0{,}1$ a posteriori; 5,3 cm (5,25 esatto); 85,85 % e 26,60 % (`v2_MOB.txt`); 0,875; 217 861, 226 400, 70 400; 0 su 140 e 7 su 10 (tipo fuori dominio: 10 passaggi per risoluzione); 176 su 180 e 174 su 180 (ricontati dal grezzo, `riconta_identita.py`); 1 e 1 riagganci a soggetto nascosto su 140; 104 131 di 175 802; 240 condizioni; 0,414 e 0,297; 46 ms; 0,32–0,52 m e $N=12$; 928 e 24. Ricerca dei valori vecchi nei 13 file: nessuno.
2. **Wilson** (`wilson.py`, `wilson_uscita.txt`): tutte le tabelle dei capitoli 1 e 6 e le conclusioni, più capitoli 2, 3, 4, 5, 7, 8; $z_{12}$, $z_{30}$, $z_{45}$, $z_{60}$; gli estremi arrotondati per eccesso sono solo i due dichiarati.
3. **Appendice A contro i capitoli**: tutte le righe confrontate coincidono, salvo R7; 1,13 e 0,56 m/s, 27,1 % e 5,2 %, 0,167 m per ciclo, $\sigma_z$ rifatti.
4. **Classificazione e profili** (`classi_conti.py`): fasce, $d_{\mathrm{serve}}$, 3 su 15, 0 su 15, 3 e **10** dopo il contatto (ricontato: il punto 9 delle note è chiuso), 11 su 15, 1,44 e 7,1 m/s, 2,11 m; tabella del portatore (1,42 / 0,72 / 2,22 / 1,92; 2,84 / 0,92 / 1,07; 2,01 m e 0,72 m/s; 4,62 m; 3,37 m); 155 ms; marche d'origine delle velocità (9 con fonte su 30) uguali a `classi.json`; 0,353, 0,791, 29,1 %, 4,8 %, 4000 su 4000, 0,47 s, 4,1 % uguali al blocco. Le ipotesi senza fonte sono dichiarate ipotesi nei capitoli 4, 5, 8.
5. **Punto discutibile 3** (i due denominatori): sciolto in R1.

## 3. Stati proposti

- «Prova singola» 0,853 e 0,371: **verificato per calcolo**, con la condizione di R3.
- «24–34 %»: **sostenuto dai dati** (due registrazioni, 60 fotogrammi ciascuna, camere diverse da quelle simulate): dice il verso, non la misura.
- Denominatori dell'avviso: **verificato** sul grezzo.
- Definizione di «occupato»: **verificato** per lettura del programma; vale quella del capitolo 3.
- Limite «6,4 su 10 000»: **non risolto** fra 6,4 e 6,8; lo decide un conteggio dei camminatori con almeno un passaggio con la traccia entrata, che chiede di rieseguire la simulazione con una riga per passaggio.

## 4. Non verificato

- Le condizioni aggiunte dalla verifica delle citazioni (rumore al limite dalle schede, modo della misura dei 95 ms, intervallo 40–70 mm): niente rete.
- «11 946 289 istanti», «87 su 2800», «9 su 2800», «193 su 193», l'errore mediano del punto, il numero di casi dietro «76,4 % [70,7; 81,3]» (compatibile con 185 su 242 o 188 su 246; il testo non dà $N$).
- Se la «linea a 2,1 m» coincida con «a 0,3 m dal pannello»: il testo non lo afferma; lasciato.
- Se le dimostrazioni del capitolo 5 usino «occupato» nel senso del primo ritorno (R5 tocca solo la definizione del capitolo 4).
- Il PDF contro i `.tex`; i capitoli 2, 3 e 7 oltre agli intervalli e ai punti toccati dalle correzioni.

## 5. Che cosa propongo dopo

1. Applicare R1–R8 e ricompilare. Previsione: 0 errori, 0 «Overfull» (la colonna $N$ di R1 e di R6 è stretta: da guardare a pagina). Smentita: una riga fuori margine.
2. Rieseguire la simulazione d'insieme con una riga per passaggio, per chiudere il limite di R6 (d). Chiede il sì di chi coordina: è l'unico processo pesante.
3. Rimettere nella bibliografia la voce della registrazione del costruttore, se si vuole citarla in R4.

## File accanto

`PREVISIONI.md`; `wilson.py`, `wilson_altri.txt` → `wilson_uscita.txt`; `conti.py` → `conti_uscita.txt`; `riconta_avviso.py`, `riconta_continuita.py`, `riconta_identita.py`, `riconta_riagganci.py` con le loro uscite; `classi_conti.py` → `classi_conti_uscita.txt`; `estrai_intervalli.py`, `cerca.sh`, `cerca_py.py`; `prova_latex/correzioni.tex` con `compila.txt`; `componi_controllo.py` e `CONTROLLO_modello.md` (da cui è composto questo file).
