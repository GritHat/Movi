# Previsioni del controllo finale delle dimostrazioni

Scritte alle 2026-11-14T19:57:36+01:00, prima di aprire i capitoli corretti e prima di ogni programma. Conosco solo la consegna.

| # | Previsione | Misura | Soglia di smentita |
|---|---|---|---|
| P1 | Dopo 188 sostituzioni fatte senza rilettura, almeno 3 enunciati formali dei capitoli 2-8 hanno ancora un difetto (ipotesi mancante, dimostrazione rimasta alla versione vecchia, o richiamo altrove con ipotesi diverse). | conteggio delle voci «non torna» + «torna con una condizione in più» nella tabella di CONTROLLO.md | smentita se sono 0, 1 o 2 |
| P2 | Il contenimento nell'insieme di possibile presenza (ricorsione su griglia) regge senza errore di posa in tutte le prove esaustive/casuali su griglia piccola e cade con un errore di posa non coperto dal margine. | programma su griglia piccola: numero di violazioni | smentita se trovo una violazione senza errore di posa sotto le ipotesi dichiarate nel testo corretto, oppure nessuna violazione con errore di posa |
| P3 | Almeno un richiamo fuori capitolo (sommario, introduzione, conclusioni, cap. 8) enuncia un risultato «dimostrato» senza le ipotesi aggiunte dalla correzione nel capitolo d'origine. | confronto testuale fra enunciato e richiami | smentita se tutti i richiami portano le stesse ipotesi (o un rinvio esplicito a esse) |
| P4 | La proposizione sull'etichetta di classe è vera solo se nessun parametro che entra nell'avviso o nel «libero» (velocità massima, impronta, raggio, porta, soglie) dipende dalla classe; prevedo che nei capitoli 4, 5 o 8 almeno un parametro dipenda dalla classe o sia proposto come dipendente, e che quindi serva una condizione in più. | lettura di cap. 4, 5, 8 e del blocco di classificazione | smentita se in nessun punto del documento un parametro dell'avviso/libero dipende dalla classe e la dimostrazione lo dice |
| P5 | I conti numerici chiusi (varianza della differenza seconda, crescita della covarianza, limite del livello dopo il ritaglio, rango per la non identificabilità, fascia di guardia) tornano alla cifra scritta: al più 1 discordanza numerica. | programma mio, confronto con le cifre del testo | smentita se le discordanze numeriche sono 2 o più |

Indipendenza: non condivido il codice dei verificatori precedenti (scrivo programmi miei); condivido il testo dell'allegato, i fascicoli come fonte del modello, e il modello linguistico con autore e verificatori. Il controllo vale quindi per errori di passaggio, di ipotesi e di conto; non per errori comuni di modello che un lettore dello stesso tipo ripete.

## Esiti (scritti dopo i controlli, alle 2026-11-14T20:12:25+01:00; dettagli in CONTROLLO.md e controllo.txt)

- P1 regge: 1 «non torna» e 4 «con una condizione in più» nei capitoli 2-8, più 3 nelle conclusioni (soglia 3).
- P2 smentita a metà: sulla griglia astratta 0 violazioni senza errore di posa (65 536 e 32 768 successioni) e 447 istanti su 447 fuori con errore di posa; ma sotto le ipotesi del testo corretto (lettura del suolo con margine) c'è una violazione senza errore di posa (striscia dell'impronta letta come suolo). Notato dopo: la clausola «più alto del margine di lettura» non la ripara.
- P3 regge: t_a nei simboli e in appendice A; fascia nelle conclusioni senza l'ipotesi (ii); «la sicurezza non dipende dall'etichetta» in tre capitoli.
- P4 regge: la forma della regione dipende dalla classe ed entra nella porta del riaggancio; la fascia per scenario dipende dalla classe solo in aumento.
- P5 regge: 0 discordanze numeriche.
