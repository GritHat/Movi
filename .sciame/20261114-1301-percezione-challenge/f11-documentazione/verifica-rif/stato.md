# stato — sciame-fonti, f11, verifica dei riferimenti (verifica-rif)

- 2026-11-14T17:06:08+01:00 inizio. Letti: la testa di unione/RIFERIMENTI.md (§0), unione/stato_riferimenti.md, unione/stato.md, le prime voci del .bib. Nessun controllo ancora eseguito, nessuna fonte ancora aperta.

## Previsioni scritte PRIMA dei controlli (2026-11-14T17:06:08+01:00)

- V1 (chiavi orfane). Misura: chiavi fra parentesi quadre di unione/STATO_PROGETTO.md che non hanno una voce «### chiave [n]» in unione/RIFERIMENTI.md. Attesa: 0 (il redattore dichiara 85 su 85). Smentita: almeno 1.
- V2 (doppioni). Misura: coppie di voci con lo stesso DOI, lo stesso identificativo arXiv o lo stesso link normalizzato. Attesa: almeno 1 coppia non dichiarata come separazione voluta nel §0. Smentita: 0 coppie non dichiarate.
- V3 (campione di 20 articoli, estratto con seme fisso 20261114 dal gruppo 1). Misura: voci in cui autori, titolo, sede, anno e identificativo coincidono con il registro (arXiv, Crossref) o la pagina. Attesa: almeno 17 su 20 senza scostamenti bibliografici; almeno 1 con uno scostamento; almeno 2 in cui l'affermazione di «Usata per» non si ritrova nel testo che riesco ad aprire (riassunto). Smentita: meno di 17 corrette, oppure 0 scostamenti di qualunque tipo.
- V4 (.bib). Misura: programma mio (parentesi bilanciate, chiavi uniche, campi obbligatori per tipo). Attesa: 166 voci, 0 errori di struttura, qualche campo obbligatorio mancante dichiarato (il file dice «dove non letto, il campo manca»): fra 1 e 15 voci. Smentita: errori di struttura, chiavi doppie, o un numero di voci diverso da 166.
- V5 (onestà degli stati). Misura: voci con stato «verificata … pagina aperta e dato presente» il cui dettaglio contiene solo [200], solo «riassunto di ricerca», o «non riletto/non aperta» senza alcuna lettura. Attesa: fra 1 e 10 voci sospette. Smentita: 0 oppure più di 10.
- V6 (fonti mancanti). Misura: identificativi arXiv, DOI e domini presenti nei file della convocazione (fuori da f11) e assenti da RIFERIMENTI.md. Attesa: almeno 1 identificativo assente, per i file scritti da f7–f10 dopo le 16:48. Smentita: 0.

Indipendenza: condivido con l'unione il modello linguistico e il ruolo (un'altra mia istanza), non i programmi (li riscrivo) né la conversazione. I registri (arXiv, Crossref) e le pagine sono la parte indipendente.

## Avanzamento (2026-11-14T17:13:04+01:00)

- Fatti i controlli locali (V1, V2, V4, V5, V6) e il campione di 20 (V3): esiti nel rapporto. Rete usata finora: registro arXiv (1 richiesta, 12 identificativi), Crossref (13 DOI più 5 ricerche per titolo), 3 PDF di arXiv, pagine di Springer (2), Cambridge (1), PMLR (1), elib DLR (1), GitHub API (2), PubMed (2), OpenAlex (1), una ricerca in rete (Weitz 2013). Nessun nome di persona del progetto né dettaglio del progetto nelle richieste.
- Previsione V7, scritta PRIMA del controllo esteso (2026-11-14T17:13:04+01:00): interrogo Crossref per TUTTI i DOI (non arXiv, non Zenodo) delle voci dei gruppi 1 e 5 e il registro arXiv per TUTTI gli identificativi arXiv dell'elenco; misura: titolo del registro uguale (a meno di maiuscole e punteggiatura) al campo «Titolo» o contenuto in esso, e cognome del primo autore presente nel campo «Autori». Attesa: almeno il 95 % coincide; al più 3 scostamenti veri (identificativo che porta a un altro lavoro). Smentita: più di 3 identificativi che portano a un altro lavoro.

## Esiti (2026-11-14T17:20:56+01:00)

- V1 regge: 85 chiavi citate, 0 orfane; 205 voci mai citate; 4 link dell'appendice B non sono quelli della voce.
- V2 regge: 1 sovrapposizione non dichiarata (librealsense / realsense-file-di-esempio, stesso file doc/sample-data.md).
- V3 regge sulla soglia (19 su 20 senza errori bibliografici; weitz2013 senza dati), ma l'attesa «almeno uno scostamento bibliografico» è SMENTITA: 0 errori, 5 completamenti. «Usata per»: trovata in 14, in parte in 3, non trovata o non controllata in 3.
- V4 regge: 166 voci, 0 errori di struttura, 4 misc senza titolo.
- V5 regge al minimo: 1 voce classificata troppo in alto (bogoslavskyi2016); nessuna «verificata» senza lettura dichiarata.
- V6 regge: 1 identificativo arXiv assente (2108.13962, DepthTrack); 0 DOI; 0 domini.
- V7 regge: arXiv 67 su 67; Crossref 88 su 89 (il restante è la versione estesa di guibas1997, dichiarata).
- Notato dopo, senza previsione: identificati weitz2013, hunt2013 e l'articolo con PII S0926580524005867; criterio di «verificata» non uniforme fra rif-3 e rif-4.
- Errore mio: primo giro di 89 richieste a Crossref fallito (parametro sbagliato, 400), ripetuto.
- Consegna: VERIFICA_RIFERIMENTI.md in questa cartella. Per ripartire: i programmi e il materiale scaricato sono nella cartella temporanea della sessione, sottocartella verifica-rif-curatore (non nel progetto).
