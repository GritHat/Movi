# SCELTE dell'unione — allegato tecnico (`20-unione/`)

Percorsi relativi a `.sciame/20261114-1301-percezione-challenge/`. «Capitolo N» è il file `capitoli/0N_*.tex` dell'unione; l'originale dell'autore è `f13-allegato/1N-capitolo/capitolo.tex`, non toccato.

## 1. Glossario applicato (un nome per ogni oggetto)

| Nome adottato | Che cosa indica | Nomi sostituiti o da non usare | Dove è definito |
|---|---|---|---|
| suolo | il piano su cui stanno camera e oggetti | «pavimento» (22 occorrenze sostituite nei capitoli 2–8 e nell'appendice A) | cap. 2 |
| ostacolo | l'oggetto fermo che proietta l'ombra | «occlusore» (13 occorrenze sostituite nei capitoli 4, 5, 7) | cap. 2 |
| ombra Ω(t), ombra stimata Ω̂(t) | suolo nascosto da un ostacolo osservato | — | cap. 2, cap. 5 |
| stati della cella: libero, occupato osservato, in ombra, non osservato | i quattro stati della mappa polare | «sconosciuto» resta solo come parola dell'uscita per settore, non come stato della cella | cap. 3 |
| cella di guardia | vicinato della mappa usato dalla regola del «libero» | da non confondere con la fascia di guardia | cap. 3 |
| passaggio | un soggetto attraversa il campo, scompare dietro un ostacolo e di norma ricompare: l'unità statistica | «transito» (4 occorrenze sostituite nei capitoli 5 e 7; resta «transito» solo come nome di una delle due ipotesi di moto dell'alternativa esclusa) | cap. 1, cap. 6 |
| soggetto | chi si muove nella scena di prova | «camminatore» resta solo dove si contano i soggetti distinti del generatore | cap. 6 |
| traccia | la stima dello stato di un oggetto seguito, tenuta dal filtro | il testo della sfida non è più chiamato «traccia» (5 occorrenze nel capitolo 1: ora «testo della sfida», «sfida») | cap. 4 |
| oggetto seguito | l'oggetto a cui la traccia si riferisce | — | cap. 4, cap. 7 |
| regola «mobile» | la regola che dichiara «in movimento» un gruppo | — | cap. 4 |
| insieme di possibile presenza Π(t) | dove un oggetto non osservato può trovarsi | — | cap. 5 |
| area d'avviso W(t) | ombra stimata allargata della fascia di guardia, su cui esce l'avviso | — | cap. 5 |
| fascia di guardia w | allargamento dell'ombra (0,40 m) | — | cap. 5 |
| regione di previsione 𝓡_α(t) | regione emessa a ogni ciclo per una traccia in ombra | «regione prevista» (4 occorrenze sostituite: sommario e capitolo 8); «regione mostrata» resta, nel capitolo 5, per ciò che lo schermo disegna | cap. 5 |
| «previsto» / «previsto ampio» | i due stati dell'uscita durante l'occlusione | — | cap. 5, cap. 8 |
| identità presunta | identità riassegnata alla ricomparsa | — | cap. 4 |
| affidabilità persa | segnale di sensore non in salute | — | cap. 8 |
| disposizioni di prova G₁, G₂, G₃ | G₁ pannello largo 1 m; G₂ e G₃ ostacolo largo 2 m | i capitoli 5 e 6 le definiscono allo stesso modo; i capitoli 1 e 8 scrivono «pannello largo 1 m», «ostacolo largo 2 m», «tre geometrie» | cap. 5, cap. 6 |
| modello ideale del sensore / profondità simulata dalle schede tecniche / traiettorie pubbliche di pedoni | i tre tipi di dato (I, II, III del capitolo 6; «ideale» e «da scheda» nella tabella di sintesi) | — | cap. 1, cap. 6 |

## 2. Notazione: conflitti risolti

| Simbolo | Prima | Scelta | Motivo |
|---|---|---|---|
| larghezza del corpo | `w` nel capitolo 2 (5 occorrenze) | `w_c` | `w` è la fascia di guardia nei capitoli 1, 3, 5, 8 e nell'appendice A |
| età del dato | `a` nel capitolo 5 (15 occorrenze, anche nell'enunciato e nella dimostrazione della proposizione sulla fascia) | `t_a` | `a` è l'altezza dell'ostacolo nel capitolo 2. Sostituzione meccanica: enunciato e dimostrazione non cambiano |
| tempo di conferma | `t_c` nel capitolo 8 e nell'appendice A; `t_{conf}` nel capitolo 5 | `t_{conf}` | un solo simbolo; `c` è già il centro del soggetto |
| velocità propria del portatore | `v_{ego}` nel capitolo 5; `v_e` nel capitolo 8 e nell'appendice A | `v_e` | il capitolo 8 è quello a cui il profilo del portatore appartiene |
| probabilità di rilevamento per fotogramma | `P_D` nei capitoli 1, 5, 6; `p_d` nel capitolo 4 | `P_D` | stessa grandezza |
| probabilità che la regola «mobile» dichiari il moto | `P_d` nel capitolo 4 | `P_{mob}` | non si confonde più con `P_D` |
| tempo dall'ultima osservazione come variabile delle misure | `τ` nel capitolo 6 (15 occorrenze) e in una riga della tabella dei requisiti del capitolo 1 | `τ_occ` (`\tocc`) | `τ` è la latenza (notazione comune) |
| errore del bordo dell'ombra | `ε_Ω` nel capitolo 5 (limite, nelle ipotesi), `e_Ω` nel capitolo 6 (errore misurato, con segno) | tenuti entrambi | sono due grandezze: la tabella dei simboli lo dice |
| coordinate d'immagine | `(ξ, η)` normalizzate nel capitolo 2; pixel `(u, v)` nel capitolo 3 (lettura di un punto); `η` con altro significato nel capitolo 4 | **lasciate** | nei capitoli 2 e 3 sono grandezze diverse (normalizzate e in pixel); la doppia `η` (capitoli 2 e 4) resta: segnalata in `NOTE.md` |

La tabella «Simboli e termini» (`capitoli/00_simboli.tex`) sta dopo l'indice e riporta i simboli comuni e dieci termini.

## 3. Cifre: dove due capitoli non concordavano

1. **Scatola di 10 cm con errore d'inclinazione di −1°.** Capitolo 3: «150 fotogrammi su 300; in una seconda esecuzione 146». Capitolo 8: «146–150». Nota del capitolo 1 e controllo delle prove: «150 e 145». Le fonti danno tre esecuzioni: 150 (primo lancio) e 145 (semi nuovi) in `f12-integrazione/03-libero/LIBERO_DELLA_CELLA.md` r. 41, confermate in `13-statistica/CONTROLLO_PROVE.md` r. 44; 146 nell'esecuzione dell'attacco (`20-finale/SOLUZIONE_V3.md` r. 61). **Scelta:** tutte e tre, ciascuna con la sua esecuzione: capitolo 3 «150; in due esecuzioni successive con altri semi 145 e 146»; capitolo 8 «145–150 (tre esecuzioni)». Nessuna è più sostenuta delle altre: sono tre lanci diversi.
2. **Chi svolta e chi esce dal lato lontano.** Il capitolo 8 dava per «chi svolta o esce lontano» le sole cifre di chi svolta (0,86 / 0,67 / 0,79 e 0,84 / 0,58 / 0,67). Capitoli 5 e 6, e `02-prova-insieme/PROVA_INSIEME.md` r. 41, danno anche chi esce lontano (0,82 / 0,61 / 0,79 e 0,76 / 0,57 / 0,70). **Scelta:** nel capitolo 8 entrambe le serie. Lo «0,57–0,79» della sintesi (ostacolo largo 2 m) e lo «0,57–0,86» delle conclusioni (tre geometrie) sono gli estremi di queste serie.
3. **Avviso dopo la rimozione dell'ostacolo.** Capitolo 5: «per una causa non determinata». Capitolo 8: «difetto noto della realizzazione, non della regola». Il giudizio complessivo (`30-arbitro/VERDETTO_INTEGRAZIONE.md`, cambio di stato 10 e §4) dice che il difetto c'è anche nella catena di partenza e che «che guardando finisca non è provato». **Scelta:** la forma del capitolo 5 anche nel capitolo 8; l'attribuzione alla sola realizzazione è tolta perché nessun file la sostiene.
4. **Continuità e copertura: due serie di cifre con condizioni diverse** (corpo puntiforme, 0 su 24 835 e 45 combinazioni su 45; corpo esteso con tutte le correzioni, 0 su 23 402 e 30 su 30 con l'ostacolo largo 2 m, soglia mancata col pannello da 1 m). Non c'è discordanza fra i capitoli: 1, 5, 6 e 8 le riportano entrambe con la condizione. **Scelta:** lasciate entrambe; nel sommario e nelle conclusioni la serie a corpo esteso, che è la forma fissata dal giudizio complessivo (§7, punti 5–7).
5. **Fascia di guardia.** Tutti i capitoli usano il conto completo (1,13 m/s; 0,56 m/s con 0,20 m d'errore del bordo). Il capitolo 5 riporta anche i conti parziali (1,85 e 1,4 m/s) con i termini che includono, come chiede `DISCORDANZE_DEI_FASCICOLI.md`. Nessun cambiamento.
6. **Latenza.** 0,155 s ovunque; 0,150 s resta solo nella prima riga della tabella della fascia del capitolo 5, dichiarata come conto parziale; 0,131 s nell'appendice A come valore con un altro dato del costruttore. Nessun cambiamento.
7. **«Libero» nell'ombra vera.** Capitoli 3 e 6 riportano lo 0 su 2 907 032 e le serie successive (4 e 5 celle·fotogramma); la sintesi del capitolo 1 dava solo lo zero. **Scelta:** aggiunta alla sintesi la serie successiva, «non risolto», come nel giudizio complessivo (cambio di stato 8).
8. **Identità su profondità simulata.** Capitoli 4, 6, 8: 176 su 180 a 424 pixel e 174 su 180 a 848; la sintesi dava solo 176. **Scelta:** entrambe nella sintesi, con «un tasso, non il superamento di una soglia per comportamento» (capitolo 6; giudizio complessivo, cambio di stato 6).

## 4. Ripetizioni: che cosa resta dove

| Contenuto | Resta in | L'altro capitolo ora |
|---|---|---|
| Argomento di sicurezza contro le mappe persistenti a sensore fermo; conto sulla griglia bayesiana | cap. 3 (osservazione, proposizione, tabella delle varianti) | cap. 7, «Mappe volumetriche»: rimando a osservazione, tabella e proposizione; restano i conti sul costo |
| Cifre delle varianti che ricordano un «libero» | cap. 3, tabella delle varianti | cap. 7, tabella delle alternative: una cifra d'esempio e il rimando |
| Richiamo alla letteratura sulle mappe (griglie, octree, hash) e sui sistemi industriali di sorveglianza | cap. 7, lavori correlati (con le citazioni) | cap. 3: rimando, senza ripetere le citazioni |
| Stato del classificatore (richiesto, non realizzato, simulato) | cap. 4 (componente), cap. 1 e cap. 8 (limiti), conclusioni | cap. 7: frase breve con rimando. Nel cap. 6 resta, perché accompagna il livello di prova di una misura |
| Risultati sulla regione (prima e dopo la regione persistente) | cap. 6 (tavole complete) | cap. 5 li richiama già con il rimando «le tavole complete sono in §6»: lasciato |
| Fascia di guardia: conto | cap. 5 | cap. 8 (condizioni di validità), appendici A e B: una riga ciascuna, lasciata perché serve all'autosufficienza delle tabelle |
| Distanza d'avviso | cap. 8 (formule complete) | cap. 5 dà la formula a sensore fermo e rimanda: lasciato |

## 5. Coerenza con il giudizio complessivo

Il giudizio (`f12-integrazione/30-arbitro/VERDETTO_INTEGRAZIONE.md`) è arrivato dopo la scrittura del capitolo 1, che lo dava per assente. Ho allineato sintesi, limiti e conclusioni alle sue «forme più forti che restano vere» (§7) e alle frasi da non scrivere:

- «continuità» sempre con «in simulazione, con modello ideale del sensore»; aggiunto che su profondità simulata la regola della regione persistente non è stata eseguita (cambio di stato 9: nessun capitolo lo diceva);
- «l'avviso non termina senza osservazione» (dimostrato) tenuto distinto da «termina quando il suolo è rivisto» (non verificato);
- «9 su 10» mai riferito al pannello da 1 m;
- lo zero su 2,9 milioni sempre con la serie successiva;
- identità: tasso in un dominio ristretto, non criterio superato;
- classificatore: richiesto, non realizzato, non valutato; nessun «riconosce», «classifica», «gestisce veicoli».

## 6. Forma

- Conclusioni come sezione 9 (`capitoli/09_conclusioni.tex`, etichetta `sec:con`), prima delle appendici; il capoverso «Struttura del documento» del capitolo 1 la nomina.
- La tabella di sintesi del capitolo 1 è divisa in due tabelle (`tab:intro-sintesi`, `tab:intro-sintesi-due`): con le righe aggiunte non stava in una pagina.
- Bibliografia: nel file principale gli indirizzi possono andare a capo anche a trattini, punti e trattini bassi (ridefinizione locale di `\UrlBreaks`, comando del pacchetto `url` già caricato da `hyperref`): toglie cinque righe fuori margine senza toccare `allegato.bib` né il preambolo.
- La parola «hackathon» non compare: il capitolo 1 dice «il testo della sfida a cui il progetto risponde».
