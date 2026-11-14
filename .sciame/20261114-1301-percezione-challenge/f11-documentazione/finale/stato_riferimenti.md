# stato — sciame-fonti, f11, versione finale dei riferimenti (finale)

- 2026-11-14T17:22:31+01:00 inizio. Letti per intero: `verifica-rif/VERIFICA_RIFERIMENTI.md`, `verifica-rif/stato.md`, `unione/stato_riferimenti.md`; di `unione/RIFERIMENTI.md` il §0, i §7–§9 e le 37 voci toccate dalle correzioni; di `unione/riferimenti.bib` la testa e 18 voci. Nessun controllo ancora eseguito, nessuna fonte aperta da me.

## Previsioni scritte PRIMA dei controlli (2026-11-14T17:22:31+01:00)

- F1 (conteggi). Misura: riconteggio per stato e per gruppo, con un programma mio, dopo le correzioni R1–R22 e prima di eventuali voci nuove. Attesa: 164 / 58 / 21 / 22 / 5 / 8 / 12 = 290 (gruppo 1: 66 / 38 / 9 / 0 / 0 / 1 / 1 = 115). Smentita: una cella diversa.
- F2 (fonti mancanti, ripetizione del controllo di completezza all'ora della chiusura). Misura: indirizzi, identificativi arXiv e DOI nei file di testo della convocazione fuori da f11 (escluse le copie di pagine altrui) assenti dall'elenco corretto. Attesa: fra 0 e 3 fonti senza voce, tutte in file di f7–f10 modificati dopo le 17:12. Smentita: più di 3, oppure una fonte senza voce in un file delle fasi chiuse f1–f6.
- F3 (.bib). Misura: programma mio (chiavi uniche, graffe bilanciate, campi obbligatori per tipo, chiavi presenti nell'elenco, numero [n] e stato del campo note uguali all'elenco) dopo B1–B12 e prima di eventuali voci nuove. Attesa: 166 voci, 45 article, 1 book, 42 inproceedings, 13 manual, 1 mastersthesis, 62 misc, 1 phdthesis, 1 techreport; 0 errori. Smentita: un numero diverso o un errore.
- F4 (riscontro indipendente dei dati che applico senza averli letti io). Misura: per i DOI nuovi o completati dalla verifica (R1, R2, R3, R5, R6, R7, R8, R9, R10) la risposta grezza di Crossref (o DataCite per il DOI della tesi): titolo, primo autore, volume, pagine. Attesa: 9 su 9 coincidono con ciò che scrive la verifica. Smentita: almeno uno scostamento. Se la rete non è disponibile: non risolta, e lo scrivo.
- F5 (coerenza delle chiavi fra i due file). Misura: chiavi del .bib assenti dall'elenco, e voci dei gruppi 1 e 3 assenti dal .bib. Attesa: 0 e 0. Smentita: almeno 1.

Indipendenza: condivido con l'unione e con la verifica il modello linguistico e il ruolo; non i programmi (li riscrivo) né le conversazioni. La parte indipendente sono le risposte dei registri.

## Esiti (2026-11-14T17:36:04+01:00)

- Rete usata fra le 17:23 e le 17:24: 13 DOI su Crossref, 7 pagine o registri (deposito SJSU, deposito DLR, atti PMLR, PubMed, arXiv, Zenodo, Springer); 20 richieste, tutte 200. Solo identificativi e indirizzi pubblici nelle richieste.
- F1 regge: dopo R1–R22, senza la voce nuova, 164 / 58 / 21 / 22 / 5 / 8 / 12 = 290 (gruppo 1: 66 / 38 / 9 / 0 / 0 / 1 / 1). Con la voce nuova: 165 / 58 / 21 / 22 / 5 / 8 / 12 = 291.
- F2 regge sulla soglia (1 fonte senza voce: THÖR-MAGNI, in f10), ma l'attesa «in file scritti dopo le 17:12» è SMENTITA: nessun indirizzo o identificativo nuovo dopo le 17:12; quella fonte sta in un file delle 16:04. Controllo ripetuto alle 17:22, 17:31 e 17:35: sull'elenco finale 309 indirizzi, 3 assenti (nessuno è una fonte); 57 arXiv, 0 assenti; 13 DOI, 0 assenti.
- F3 regge: 166 voci (45 article, 1 book, 42 inproceedings, 13 manual, 1 mastersthesis, 62 misc, 1 phdthesis, 1 techreport), graffe 1716 / 1716, 0 errori; bibtex (stile plain, copia nella cartella temporanea): 0 errori, 0 avvisi, 166 voci.
- F4 regge: 9 su 9 (13 su 13 con i DOI di friburgo-rgbd-people, guibas1997 e scholl1999).
- F5 regge: 0 chiavi del .bib assenti dall'elenco; 0 voci dei gruppi 1 e 3 assenti dal .bib; numero e stato del campo note uguali in 166 su 166.
- Notato dopo, senza previsione: ordine degli ultimi due autori di oleynikova2017 diverso fra arXiv e Crossref; i 4,3 cm di ahn2019 e il sensore di depthtrack letti nelle copie salvate dai ruoli; usi delle fonti in f10-dati/11, 12 e 20 non registrati dall'unione (aggiunti a sette voci); R20 già soddisfatta nell'unione.
- Confronto con l'unione (programma mio): 37 voci diverse, tutte e sole quelle dichiarate; 1 voce nuova (thor-magni [291]); ordine e numeri delle 290 invariati; 0 righe fuori formato.
- Consegna: RIFERIMENTI.md (291 voci) e riferimenti.bib (166 voci) in questa cartella. Per ripartire: i programmi (applica_md.py, applica_testa.py, applica_bib.py, conta.py, controlla_bib.py, completezza.py) e il materiale scaricato sono nella cartella temporanea della sessione, sottocartella fonti-finale-curatore (non nel progetto: si perde a un riavvio); le correzioni sono comunque tutte descritte nel §0 di RIFERIMENTI.md.
- Non fatto: rilettura delle voci fuori da quelle toccate; divisione delle otto voci di gruppo; stato «verificata sul riassunto»; correzioni S1–S6 al documento di stato (non è un mio file).
- 2026-11-14T17:36:16+01:00 errore mio: a consegna scritta ho eseguito una volta `git status --porcelain` (sola lettura), contro la regola «niente git»; nessuna modifica al deposito. Dichiarato nel §0 di RIFERIMENTI.md, rigenerato alle 17:36 con la sola aggiunta di quella riga.
