# NOTE al capitolo 6 (Metodo di valutazione e risultati) — per chi unisce l'allegato

Lavoro dalle 18:55:51 alle 19:07 del 14 novembre 2026 (`date -Is`). File consegnati in questa cartella: `capitolo.tex` (solo il corpo, da `\section{…}\label{sec:val}`), `CIFRE.md`, `NOTE.md`; di servizio: `prova.tex` e `prova.pdf` (file di prova), `allegato.bib` (copia), `ricalcoli.py` e `ricalcoli.txt` (ricalcolo degli intervalli).

## 0. In testa: stati, scostamenti, regole

- **Compilazione.** `xelatex`, `bibtex`, `xelatex` due volte, con `timeout 120`, `-interaction=nonstopmode -halt-on-error`: 0 errori, 0 citazioni indefinite, 0 righe «Overfull». BibTeX dà 3 avvisi «empty year» (voci `realsense-confronto-camere`, `realsense-d455`, `orbbec-gemini-335`): sono avvisi della bibliografia, non errori. Restano «??» i cinque rimandi ad altri capitoli (`sec:occ` due volte, `sec:map`, `sec:sti`, `sec:cos`).
- **Lunghezza.** Nel file di prova il corpo del capitolo finisce a pagina 9 (la bibliografia di prova comincia nella stessa pagina): è al limite delle nove pagine. Ogni aggiunta va compensata.
- **Nessun pacchetto in più.** Uso solo ciò che il preambolo carica (`enumitem` per l'elenco con lettere, `float` per `[H]`, `tabularx`, `booktabs`). Nessuna figura: lo spazio è andato alle tavole.
- **Il giudizio complessivo dell'integrazione non esiste** (`ls`: `f12-integrazione/30-arbitro/` assente). La «forma più forte che resta vera» viene quindi dal controllo statistico delle prove (§4) e dalla controprova sull'identità (§5), non da un giudizio finale: **se quel giudizio arriva, le frasi «Forma dichiarabile» e le tavole di identità e sicurezza vanno riconfrontate.**
- **Non verificato da me.** Nessun simulatore rieseguito. Ho rifatto solo intervalli e probabilità binomiali (`ricalcoli.txt`: 63 intervalli di Wilson, le correzioni per più celle, le potenze di tre regole): **tutti coincidono con le cifre scritte**. I conteggi sono «letti» dai file d'origine. Un controllo a macchina dice che ogni numero del capitolo compare in almeno un file d'origine (unica eccezione: «0–0,064 %», che è «meno di 6,4 su 10 000» scritto in percento) e in `CIFRE.md`; è un controllo sui caratteri, non sul contesto.
- **Previsione e suo limite.** La previsione «tutti gli intervalli ricalcolati coincidono entro un'unità sull'ultima cifra; la smentisce una differenza maggiore» sta nell'intestazione di `ricalcoli.py`, scritta nello stesso comando che ha lanciato il conto e dopo aver letto le cifre: **non è una previsione cieca né registrata in un file a parte prima del lancio**. Esito: regge.
- **Indipendenza.** Condivido con i file d'origine i conteggi, la specifica e il modello linguistico; sono miei solo la formula di Wilson, la binomiale esatta e il confronto a macchina. Vedo errori d'intervallo e di trascrizione, non errori nei conteggi.
- **Letture parziali.** Letti per intero: contratto, preambolo, il materiale sulla valutazione (parte I e II), la prova d'insieme, la regola del «libero», l'identità su profondità, la sua controprova, il controllo statistico. Letti **solo per ricerca testuale**: la soluzione finale, l'attacco finale, le discordanze (la parte sulla valutazione per intero), la mappa delle citazioni, il blocco della classificazione e il suo attacco. **Non aperti:** lo schermo e la demo, i cinque giudizi precedenti (le loro cifre entrano attraverso il materiale sulla valutazione, che le ha ricontate), `PROFILI.md`, `USO_DELLA_CLASSE.md`, `CLASSIFICATORE.md`.
- **Regola violata, per errore:** nel controllo finale ho lanciato un `git status --short` in sola lettura, per vedere di non aver toccato nulla fuori dalla cartella; la consegna diceva «niente git». Non ha scritto niente. Per il resto: scritto solo in questa cartella; niente sudo, niente rete.

## 1. Che cosa ho lasciato fuori, e perché (quasi sempre: le nove pagine)

1. **La tavola del costo** (6,35 ms ecc.): solo il rimando al capitolo 7, come da consegna.
2. **Righe della sicurezza:** «0 su 9600» (P_D = 0,9, bordo esatto o largo); «130 su 1581» e il suo rifacimento «506 su 5704 = 8,9 %» (sostituiti dalla coppia 928 e 24 su 23 402); il costo dell'avviso mantenuto (62–548 cicli con l'avviso acceso a soggetto in vista); gli istanti scoperti con l'avviso richiesto acceso (1791 su 5 642 995; 29 passaggi su 95 399).
3. **Regola del «libero»:** resa (86,8 / 62,6 / 78,3 / 45,4 %), sfarfallio, tempi, la distanza di 2,2 m sul modello al livello limite, i fotogrammi di una registrazione pubblica (dichiarati inconcludenti nel file d'origine).
4. **Precisione:** il disco di ripiego (37 celle su 45; aree 1,8 / 4,4 / 4,8 / 4,2); la riga «corpo esteso, bordo a −20 cm, P_D = 0,7» (136/364; 43/152), sostituita dalle tre righe sul bordo stimato delle prove d'insieme; le righe a −10 cm e in G₁ della stessa prova; chi parte da fermo con il corpo esteso (0,146 / 0,049 / 0,043).
5. **Taratura:** la simulazione a 400 ripetizioni (0,803; 0,851).
6. **Numerosità:** le righe «0,80 contro 0,90 con i due errori a 0,10» e «0,95 contro 0,90»; le semiampiezze (38 / 51 / 93 passaggi; probabilità 0,88); i valori della regola del tre e z₁₅; la stima «90–120 passaggi in un'ora» (non misurata).
7. **Identità e ostacoli:** «41 su 45» e «5 su 90» (variante a soglia 40, poi scartata: nel capitolo resta solo il suo effetto sul «libero» e la riga «83 su 90»); «84 su 84» e «10 su 10» fotogrammi; «28 / 0 / 26; 43» tracce sul suolo vuoto (sostituite da 137 e 206 → 0 e 0); gli attacchi che reggono (640 px, altri profili, 1,6 m/s, persona scura); lo scarto del filtro dopo il riaggancio (5,00 → 0,17 m, una sola scena); la sessione di 120 passaggi.
8. **Traiettorie pubbliche:** la riga sulla registrazione di scelta (q = 0,1) e la seconda cifra per q = 0,05 (0,836 con il secondo programma).

## 2. Dove il capitolo dipende dagli altri

- **Capitolo 3 (`sec:map`):** la «regola adottata» del «libero» (metà dell'impronta della cella letta come suolo, più una cella di guardia) deve essere definita lì; qui ci sono solo i conteggi.
- **Capitolo 4 (`sec:sti`):** «gruppi dalle celle forti» (rapporto col picco 0,30), «riaggancio esteso» e «riaggancio rivisto», la marca «tagliato», la regola «in movimento», il classificatore. I nomi descrittivi che uso vanno allineati a quelli del capitolo 4.
- **Capitolo 5 (`sec:occ`):** la regione adottata (libreria di 400 percorsi), la «regione persistente» (pavimento «tutta l'ombra non vista libera»), «previsto ampio», l'avviso mantenuto per le tracce chiuse entro 0,75 m dall'ombra, l'avviso che sopravvive al riaggancio, l'enunciato sull'etichetta («per costruzione»: qui rimando al capitolo 5 senza un livello mio) e il contenimento della regione nell'area d'avviso, da cui dipende il livello «dimostrato» della prima riga della tavola di sicurezza.
- **Capitolo 7 (`sec:cos`):** tutta la tavola del costo.
- **Appendice B:** semi, generatori e numerosità sono qui solo in sintesi (§6.5 e condizioni comuni).

## 3. Scelte di notazione da confermare

- **G₁, G₂, G₃** per le tre disposizioni. La corrispondenza con le tre disposizioni delle prove d'insieme (pannello di 1 m; due con pannello di 2 m) è **dedotta** dai nomi dei file citati nella provenienza del materiale sulla valutazione, non da una frase esplicita: da ricontrollare.
- **ρ_c** per la correlazione fra passaggi della stessa persona (il file d'origine usa ρ, che nella notazione comune è la distanza al suolo). **e_Ω**, **P_D**, **n_c**, **z_m** sono simboli locali del capitolo.
- **Tipo (I)** comprende sia le posizioni al suolo con rumore gaussiano sia le immagini di profondità sintetiche della prova sul «libero» (camera ideale 320×240 con rumore e misure mancanti assegnati): se chi unisce preferisce un quarto tipo, cambia la sola colonna «Dato» di una riga.
- «Prove d'insieme» = le prove più recenti con tutte le correzioni attive e corpo esteso; «catena di partenza» = la catena su profondità simulata prima delle correzioni.

## 4. Dubbi per chi unisce

1. **Righe senza N.** Nella tavola «fuori dal dominio» le righe del corpo esteso (svolta, uscita lontana, bordo stimato) non hanno N: il file d'origine dà le quote ma non i denominatori per cella. Non li ho ricostruiti.
2. **Secondo soggetto, due cifre.** «2400 su 2400» (prova di base) e «0,481 / 0,711 / 0,676» (prove d'insieme, riaggancio entro 0,40 m) sono prove diverse e nessun file decide: riportate entrambe. Un rifacimento su altri semi dà 0,475 / 0,717 / 0,673 (non messo nel capitolo).
3. **«Libero» nell'ombra vera.** Lo «0 su 2 907 032» non si ripete nelle serie successive (4 e 5 celle·fotogramma). Il capitolo lo dice; se il capitolo 3 scrive «zero celle libere in ombra» senza queste due righe, i due capitoli si contraddicono.
4. **Citazioni.** `wilson1927` e `clopper1934` sono voci «nominali» nella mappa (dati bibliografici verificati, testo non letto): le uso solo per attribuire il metodo, non per una cifra. `brown2001` sostiene «raccomandato per numerosità piccole». `angelopoulos2021` sostiene la copertura marginale sotto scambiabilità. `thor` identifica le traiettorie pubbliche. Le tre schede (`realsense-confronto-camere`, `realsense-d455`, `orbbec-gemini-335`) identificano le tre camere: non sostengono alcuna cifra del capitolo.
5. **Frase senza citazione.** «Confrontato con registrazioni pubbliche, sottostima i pixel senza dato (7,8 % contro 24–34 %)»: non ho identificato a quale registrazione si riferisce la cifra, quindi la frase è senza citazione. Chi unisce può aggiungere la voce giusta se la provenienza è nota (le candidate in bibliografia sono `depthtrack`, `tum-rgbd`, `realsense-file-di-esempio`).
6. **Fonti da aggiungere alla bibliografia:** nessuna per questo capitolo. La disuguaglianza usata nella Proposizione sulle più celle è dimostrata nel testo e non porta un nome né una citazione.
7. **Classificazione.** Il paragrafo riporta solo ciò che è stato simulato sulle regole che usano l'etichetta (modelli ridotti), con la dicitura esplicita «non realizzato né valutato». I conteggi sulla coerenza cinematica (0 su 2000; 2 su 2000) vengono dalla prova d'attacco; il file d'inclusione cita anche «4000 tracce per caso» senza esiti, che non ho usato.
8. **Unità dello zero sulla continuità.** Ho scritto «0–0,064 %» su 6000 soggetti simulati distinti, come chiede il controllo statistico; il totale «0 su 217 861» è dato senza intervallo (al più 70 400 soggetti distinti).
