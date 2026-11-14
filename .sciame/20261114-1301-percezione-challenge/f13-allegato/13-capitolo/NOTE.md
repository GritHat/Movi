# NOTE al capitolo 3 (map) — per chi unisce

Lavoro del 14 novembre 2026, 18:55–19:05 (`date -Is`). Esito della compilazione (XeLaTeX, BibTeX, XeLaTeX due volte): nessun errore, nessuna citazione indefinita, nessuna riga fuori margine; 6 pagine con il riquadro e la bibliografia di prova (il corpo finisce a un terzo della sesta). I soli riferimenti «??» sono quelli agli altri capitoli (`sec:geo`, `sec:occ`, `sec:cos`, `sec:lim`, `sec:par`).

## Regole e scostamenti
- **Regola violata per omissione:** la previsione sulla compilazione (compila, sei pagine al più) non l'ho scritta su file prima di compilare; l'esito qui sopra è quindi un'osservazione, non una previsione che regge.
- Scritto solo in questa cartella; niente git, sudo, rete.
- `preambolo.tex` e `allegato.bib` qui dentro sono **copie** per la prova di compilazione (`prova.tex`, `prova.pdf`).
- Le immagini di controllo del PDF stanno nello scratchpad della sessione, in una sottocartella mia; al primo tentativo ho scritto sei `pag-*.png` nella radice dello scratchpad, che è condivisa: se un altro lavoro aveva file con quel nome, li ho sovrascritti.
- Indipendenza: ho composto, non ricalcolato. Condivido con le fonti i file, la specifica e il modello linguistico; i conti rifatti a mano sono solo 87·30, i limiti di Wilson per 0 su 300 e 0 su 10, e le differenze di resa (23 e 19 punti).

## Precisazioni mie (non sono misure nuove; da vagliare)
1. **Proposizione, parte (b).** Nel fascicolo la tesi è «nessuna superficie interseca i raggi che ne raggiungono il suolo». Con la regola a metà impronta la dimostrazione copre solo i raggi dei pixel che leggono il suolo: ho scritto così, e nell'osservazione (ii) ho detto che la sicurezza della cella intera è verificata in simulazione, non dimostrata. È coerente con la discordanza D8 delle dimostrazioni.
2. **Definizione degli stati.** «In ombra» è scritto con «non è occupata e sta oltre la prima cella occupata»; «non osservato» è il complemento, e comprende la cella di guardia (riga 6 dello pseudocodice finale). Nella figura la guardia è disegnata come «non osservato».
3. **Controesempio dell'ostacolo che non rimanda segnale:** la frase «protegge solo dove i pixel risultano non validi su più di metà dell'impronta» è la lettura diretta della riga 4 della regola, non una misura.
4. **Nomi descrittivi dati alle regole candidate** (tabella 1): «punto sopra il centro della cella (a 0,10 m)», «punto a 0,20 m», «lettura a 0,20 m con veto delle celle occupate e quota verificata», «impronta: un pixel», «impronta: metà», «impronta: metà e cella di guardia». La terza descrizione l'ho ricostruita dal testo della prova («soglia 3 pixel», «punto a 0,20 m», «quota verificata»): chi ha il codice controlli che sia fedele.
5. **Il termine k·z²**: scritto come «segue la crescita quadratica del rumore di profondità (cap. 2)». Nei file k è «dal modello del sensore»; l'identità k = σ_d/(f·b) non l'ho trovata scritta e non l'ho affermata. Il capitolo 2 dovrebbe dire da dove vengono 0,004 e 0,0100.

## Dubbi sulle cifre
- **43–47 % di settori «sconosciuto»**: nel file segue «chiazze 30 %»; non è chiaro se l'intervallo copra anche il 30 % sparso. Ho scritto «con il 30 % di pixel non validi».
- **Sfarfallio**: i valori 5,72 / 2,72 / 6,66 del file non dicono a quale regola si riferiscono; ho usato «fino a 6–7 cambi al secondo» (testo del §3 della prova) e 0,01 col 5 % sparso.
- **Colonne «dentro un corpo»** della tabella della prova: portano due numeri senza intestazione distinta; ho riportato solo i fotogrammi con violazione e i 15 648 del testo.
- **Palo di 3 cm**: il file non dice se la scena è costruita a mano o simulata dalle schede; ho scritto «in una scena di prova letta con una regola precedente».
- **Livello [C] dei «9 settori su 17»**: viene dal banco in simulazione, ma è geometria; scelto [C].
- **Livello [P]** usato una sola volta, per i 6 fotogrammi della sequenza pubblica: è un'elaborazione senza riferimento, e il testo lo dice («non è risolto»).

## Lasciato fuori, e perché
- Tempi per fotogramma della regola (0,88 ms di mediana) e complessità delle rappresentazioni: capitolo 7.
- I lemmi sul numero di voxel, sui passi di raggio e sul guadagno delle strutture sparse; la mappa a tre fasce di quota (30,6 %, 32 celle): capitolo 7.
- Corollario «libero adesso» e fascia di guardia: capitolo 5 (qui solo il rimando e i 537 su 88 418).
- Vetro su profondità simulata (420 celle·fotogramma su 420) e ostacolo sospeso al 97,5 %: non è chiaro il denominatore; restano i dati del modello ideale.
- Le tre varianti prudenti cadute senza cifre complete (guardia sulle sole occupate, tutta l'impronta, le due regole insieme).
- Lo «0 su 3 149 352» con la seconda definizione d'ombra, le 98 e 91 celle·fotogramma con la soglia sui pixel per cella (riguardano il capitolo 4), il limite geometrico della decimazione dei raggi, i 14 448 voxel persi su 22 240.
- La prova d'ingresso della posa all'avvio e l'autoverifica del sensore coperto: capitolo 8.

## Dipendenze da altri capitoli
- `sec:geo`: h, θ, campo, da dove si vede il suolo (1,24 m al centro, circa 1,7 m ai lati), legge del rumore e valori di k.
- `sec:occ`: Π(t), fascia di guardia w = 0,40 m, «libero» all'istante d'uso, perché la possibile presenza nasce sull'ombra.
- `sec:cos`: costi e memoria delle rappresentazioni; lavori correlati (qui cito solo `elfes1989`, `hornung2013`, `niessner2013`, `octomap`, `therobotreport-veo`, `us-brevetto-11846916`, `wilson1927`, `tum-rgbd`, ciascuna per ciò che la mappa delle citazioni le attribuisce).
- `sec:lim`: parole dell'uscita, sensore in moto, suolo non piano. `sec:par`: tabella dei parametri.
- **Ipotesi.** Ho dichiarato qui tre ipotesi (profondità valida = giusta; posa nota; pavimento piano) con le etichette `ip:map-valida`, `ip:map-posa`, `ip:map-piano`. Se il capitolo 5 dichiara l'elenco completo delle sei, conviene un solo elenco e un rimando.
- Il capitolo usa «cella di guardia» (vicinato della mappa) e cita la «fascia di guardia» (0,40 m, capitolo 5): sono due cose diverse, da non fondere.
- Titolo dell'uscita: la consegna dice «fino a d», la soluzione finale «da 1,3 m a d m»: ho usato la seconda.

## Forma
- Nessun pacchetto in più. La figura usa `[H]` (pacchetto `float`, già nel preambolo); le tre tabelle `[t]`.
- BibTeX dà un avviso che non dipende dal capitolo: «empty year in octomap».
- Controllo delle parole vietate: `grep` sull'elenco della consegna, zero occorrenze. «Piano» compare solo come aggettivo o come piano geometrico.
