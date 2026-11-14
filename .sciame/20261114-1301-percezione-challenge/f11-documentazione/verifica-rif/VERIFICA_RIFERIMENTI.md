# Verifica dell'elenco dei riferimenti e del suo uso nel documento di stato

Curatore delle fonti (`sciame-fonti`), fase f11, cartella `f11-documentazione/verifica-rif`. 14 novembre 2026, dalle 17:06 alle 17:20. I percorsi sono relativi a `.sciame/20261114-1301-percezione-challenge`. Oggetti verificati: `f11-documentazione/unione/RIFERIMENTI.md` (290 voci, chiuso alle 16:50), `unione/riferimenti.bib` (166 voci), `unione/STATO_PROGETTO.md` (versione delle 17:05). Le previsioni V1–V7 sono in `f11-documentazione/verifica-rif/stato.md`, scritte prima dei controlli.

## 0. In testa

**Esito.** L'elenco regge. Nessuna chiave orfana, nessun identificativo che porti a un altro lavoro, il `.bib` si legge, nessuna voce «verificata» senza una lettura dichiarata. Restano 23 correzioni all'elenco, 12 al `.bib` e 6 al documento di stato (§4): completamenti, tre fonti finora non identificate che ho identificato, una voce classificata troppo in alto, quattro link sbagliati nell'appendice B.

**Che cosa vale questa verifica.** Riguarda le fonti, non il sistema: niente è provato sull'hardware, e le misure dello sciame restano sostenute dai dati in simulazione, a sensore fermo. Ciò che viene da f7–f10 non è ancora vagliato dall'arbitro: nel §2 le voci del campione che vengono solo da lì sono marcate «[f7–f10]».

**Cambi di stato che propongo** (riguardano le voci dell'elenco; li decide l'arbitro).
1. `angelopoulos2021`, `lindemann2023`, `mercat2019`, `scholl1999`: da «verificata in parte» a «verificata» (ho trovato il dato citato nel testo o nel riassunto: §2).
2. `bogoslavskyi2016`: da «verificata» a «verificata in parte» (il metodo citato non è stato letto da nessuno: §1.5).
3. `weitz2013`, `hunt2013`: da «vista solo nel riassunto di un motore di ricerca» a «verificata in parte» (identificate da me; l'identificazione va confermata dal ruolo che le cita).
4. `sciencedirect-s0926580524005867`: da «non raggiungibile» a «verificata in parte» (identificata su Crossref dal codice dell'articolo; la frase citata resta non letta).
5. Nessun cambio di stato per gli enunciati tecnici dello sciame.

**Previsioni: esiti.** V1 regge (0 chiavi orfane). V2 regge (1 coppia non dichiarata). V3 regge sulla soglia (19 su 20 senza errori bibliografici, la ventesima è una voce senza dati), ma una sua attesa è **smentita**: prevedevo almeno uno scostamento bibliografico e non ce n'è nessuno, solo cinque completamenti. V4 regge (166 voci, 0 errori di struttura, 4 voci senza titolo). V5 regge al minimo (1 voce classificata troppo in alto, nessuna «verificata» senza lettura). V6 regge (1 identificativo arXiv assente). V7 regge (0 identificativi che portano a un altro lavoro).

**Regole violate e scostamenti, miei.**
- Lunghezza oltre le due pagine: la consegna chiede gli esiti uno per uno e le correzioni pronte.
- Prima di scrivere le previsioni avevo già letto la testa dell'elenco e i due file di stato dell'unione: l'attesa di V1 ripete ciò che dichiara il redattore.
- Un giro di 89 richieste a Crossref è fallito per un parametro mio sbagliato (risposta 400) ed è stato ripetuto: 178 richieste invece di 89.
- Due ricerche in rete (per `weitz2013` e `hunt2013`) sono passate dallo strumento che riassume; i dati che riporto li ho poi riletti nei metadati grezzi delle pagine (deposito del DLR, Crossref, deposito dell'università).
- Nelle richieste in rete solo identificativi, titoli di articoli e indirizzi pubblici: nessun nome di persona né dettaglio del progetto.
- Il materiale scaricato sta nella cartella temporanea della sessione, in una sottocartella mia (`verifica-rif-curatore/scaricati`); niente è stato eseguito dal suo interno. Niente git, niente scritture fuori da `verifica-rif`.
- Indipendenza: condivido con l'unione il modello linguistico e il ruolo; non i programmi (riscritti) né la conversazione. La parte indipendente sono i registri (arXiv, Crossref, PubMed) e i testi delle fonti.

## 1. I sei controlli

**1.1 Chiavi del documento di stato — verificato** (controllo esaustivo sulle parentesi quadre di `unione/STATO_PROGETTO.md`).
- 85 chiavi distinte citate, tutte con una voce in `unione/RIFERIMENTI.md`. **Chiavi orfane: 0.** Le altre 41 forme fra quadre sono marche della legenda (`[prel.]`, `[A]`, `[SIM]`…), non chiavi.
- Appendice B: 85 righe, una per chiave citata, nessuna di troppo. Il numero della voce coincide in 85 righe su 85; lo stato coincide in 83, e nelle altre due (`iso-10218-2`, `iso-13855`) cambia solo la dicitura («solo riassunto di ricerca»).
- **Quattro righe dell'appendice B portano un link che non è quello della voce:** `koschi2021` (riga 1515: link al documento mediaTUM 1575368, che è la voce `koschi-mediatum-1575368`), `ue-2019-945` e `ue-2019-947` (righe 1563–1564: link alla pagina dell'EASA, che è la voce `easa-drones-regole`), `librealsense` (riga 1518: link a `doc/post-processing-filters.md`, che nella voce è nel titolo ma non nel campo «Link»).
- **Voci mai citate nel documento di stato: 205 su 290** (vanno bene: l'elenco è di tutto ciò che lo sciame ha usato). Delle 85 citate: 55 verificate, 12 con un dato diverso, 8 verificate in parte, 6 aperte dal ruolo, 2 solo in un riassunto di ricerca, 2 non raggiungibili. Per gruppo: 15 articoli, 19 schede, 24 norme, 9 software, 5 insiemi di dati, 13 altre fonti.
- Le 12 voci «dato diverso» citate hanno tutte, accanto alla frase o nel riquadro 6 del §10.1, la cautela dell'elenco. La frase «in due studi l'aptico costa più dell'audio» è ancora scritta alla riga 1125, con la cautela accanto: la correzione non è applicata (lo dichiara il redattore).

**1.2 Doppioni — verificato** su DOI, identificativi arXiv, link e titoli dei campi «Identificativo», «Link» e «Titolo» delle 290 voci.
- Chiavi doppie: 0. Numeri da [1] a [290] senza buchi. Nove campi presenti in ogni voce.
- **Una sovrapposizione non dichiarata:** `librealsense` [209] e `realsense-file-di-esempio` [255] portano lo stesso file `doc/sample-data.md` (stesso link) e non si rimandano.
- Due coppie con un elemento in comune, ma fonti distinte: `hornung2013` [31] e `octomap` [220] (articolo e deposito, stesso titolo, nessun rimando reciproco); `it-legge-185-1990` [185] e `maeci-uama` [186] (la legge è citata attraverso la pagina del ministero: stesso link).
- Separazioni volute e dichiarate nel §0 dell'elenco, con rimando reciproco controllato: `realsense-taratura-profondita` e `realsense-bkm-taratura` (lo stesso testo in rete e in PDF), `ldrobot-ld19` e `ldrobot-ld19-scheda`, `koschi2021` e `koschi-mediatum-1575368`, `slamtec-rplidar-c1` e `waveshare-rplidar-c1`.
- Il problema inverso: otto voci raccolgono più fonti sotto una chiave (`insiemi-non-raggiungibili`: quattro insiemi di dati; `simulatori-di-profondita`: quattro programmi; `openkinect-libfreenect`, `stm32duino-vl53l7cx`, `st-community-interferenza`, `rivenditori-d435i-prezzi`, `rs-online-realsense`, `ldrobot-ld19`). Non sono citabili una per una.

**1.3 Campione di venti articoli:** §2.

**1.4 File `.bib` — verificato** con un programma mio (lettura a stati, non quello dell'unione).
- 166 voci (66 misc, 44 article, 40 inproceedings, 13 manual, 1 book, 1 phdthesis, 1 techreport), come dichiarato in testa al file. Graffe: 1690 aperte, 1690 chiuse. Errori di struttura: 0. Chiavi doppie: 0. Campi doppi o vuoti: 0. Caratteri speciali non protetti: 0.
- Tutte le 166 chiavi esistono nell'elenco; numero [n] e stato nel campo `note` coincidono con l'elenco in 166 su 166. Ci sono tutte le voci dei gruppi 1 (115) e 3 (38), più 13 schede del gruppo 2.
- Campi obbligatori per tipo (article, inproceedings, book, phdthesis, techreport): tutti presenti. Quattro voci `misc` senza titolo (`hunt2013`, `weitz2013`, `koschi-mediatum-1575368`, `sciencedirect-s0926580524005867`) e due senza autore: per tre di queste do i dati nel §4.2. 22 voci di norme e schede senza anno: dichiarato («edizione non letta»).
- Tre voci hanno l'anno della prima versione arXiv mentre l'elenco cita una versione successiva (`angelopoulos2021`, `barber2019`, `mercat2019`): coerente con la chiave, nessuna correzione.
- `lin2014`: il `.bib` porta i dieci autori della versione arXiv con gli atti di ECCV, dove gli autori registrati sono otto (Crossref). L'elenco lo dichiara, il `.bib` no.
- Non controllato da me: la compilazione con `bibtex` (l'ha dichiarata l'unione).

**1.5 Onestà degli stati — verificato** sulle 161 voci «verificata».
- Nessuna voce «verificata» è priva di una lettura dichiarata nel dettaglio: 158 portano una marca di lettura, le altre tre (`st-um2884`, `zenodo-radar-mmwave-occlusione`, `zenodo-tof-vl53l5cx`) descrivono la lettura a parole.
- Confronto con i quattro elenchi parziali (335 voci, 288 chiavi distinte): in nessuna voce lo stato dell'unione è più forte del più forte fra quelli dei gruppi. Le sei chiavi parziali che mancano nell'unione sono le fusioni dichiarate.
- I conteggi del §0 dell'elenco, ricontati dal mio programma, coincidono cella per cella (161 / 58 / 21 / 22 / 7 / 8 / 13).
- **Una voce classificata troppo in alto:** `bogoslavskyi2016` [9]. È «verificata», ma la nota dice «il principio si deduce dal titolo: il metodo non è stato letto». Nel LEGGIMI del deposito, che ho riaperto, «connected» ha 0 occorrenze e «range image» compare solo nel titolo dell'articolo. Per la legenda è «verificata in parte».
- **Il criterio non è uniforme fra i gruppi.** rif-4 chiama «verificata» una voce il cui dato sta nel riassunto letto nel registro (15 voci con la sola marca [API]); rif-3 chiama «verificata in parte» `dang2024`, il cui dato sta nel riassunto letto su Crossref. L'elenco lo avverte in generale («attenzione al grado»), ma lo stesso grado di lettura ha due stati diversi.
- 69 voci «verificate» hanno nel dettaglio almeno una riserva («non ricontrollato», «non è nel riassunto»): la riserva è scritta, lo stato non la mostra. Dieci voci «verificate» sono state lette solo attraverso lo strumento che riassume (marca [r]): `aharon2022`, `giudice2008`, `pololu-vl53l8cx-3419`, `unitree-l2`, `waveshare-rplidar-c1`, `us-49cfr-236-205`, `us-brevetto-11846916`, `luiten-trackeval`, `kiwibot2022`, `meta-sam3-blog`.
- Sei voci di norme sono «verificate» su una riproduzione di terzi o su una fonte secondaria, e lo dichiarano: `colreg-regola7`, `faa-aim-2-1-6`, `faa-ac-150-5220-24`, `dnv-imo-codice-mass`, `ue-2017-745`, `ue-2019-945`.

**1.6 Fonti mancanti — verificato** sui file presenti alle 17:12 (7062 file di testo della convocazione fuori da f11; 85 non leggibili come testo, saltati).
- 309 indirizzi distinti fuori dalle copie di pagine altrui; 288 presenti nell'elenco, 21 no. Dei 21: 12 sono indirizzi di scaricamento diretto di insiemi che hanno una voce; 1 è lo scaricamento di THÖR-MAGNI, che non ha una voce (vedi sotto); 3 non sono fonti (uno spazio dei nomi tecnico, un indirizzo d'esempio, un'espressione regolare); 5 sono indirizzi di fonti che hanno una voce ma non quel link (§4.1, R16–R19).
- Domini assenti dall'elenco: 0 (tolti i due che non sono fonti).
- Identificativi arXiv: 57 distinti, **1 assente**: 2108.13962, in `f10-dati/12-dati-veri/convertitori/converti_depthtrack.py` (riga 5). È l'articolo di DepthTrack (registro arXiv aperto: stessi sei autori della voce `depthtrack`, «Accepted to ICCV2021»): manca solo l'identificativo nella voce.
- DOI: 13 distinti, 0 assenti.
- Citazioni «autore e anno» senza link nei file `.md`: nessun cognome assente dall'elenco (ricerca con un'espressione regolare: trova solo le forme «Cognome e altri, anno» e simili).
- THÖR-MAGNI (Zenodo, record 7974709): confermo ciò che scrive l'unione. Compare solo in `f10-dati/01-ricercatore/elenchi/thor_magni_subset.txt` e in due pagine salvate; nessun file `.md` lo usa. Non serve una voce finché nessuno lo usa.
- Nove file `.md` di f7, f8 e f10 sono stati modificati dopo le 16:48 (per esempio `f7-estensione/13-soluzione/DECISIONE.md`, `f8-continuita/13-soluzione/MODIFICHE_CONTINUITA.md`): non contengono indirizzi né identificativi nuovi.
- Che cosa il controllo non vede: i riferimenti scritti solo a parole, senza anno; i file non di testo (PDF); ciò che i ruoli scrivono dopo le 17:12.

**1.7 Controllo in più: tutti gli identificativi** (V7) — **verificato** sull'insieme dichiarato.
- arXiv: 67 identificativi nelle voci, interrogati tutti nel registro: 67 su 67 portano al titolo e al primo autore della voce.
- Crossref: 89 DOI dei gruppi 1 e 5 (esclusi quelli di arXiv e Zenodo): 88 su 89 portano al titolo della voce. Il restante è il secondo DOI di `guibas1997`, la versione estesa su rivista, che ha un altro titolo («A Visibility-Based Pursuit-Evasion Problem»): la voce lo dichiara come versione estesa ma non ne dà il titolo.
- Vale per titolo, primo autore e anno. Non vale per il contenuto citato.

## 2. Campione: venti voci del gruppo 1, una per una

Estratte con seme fisso (20261114) dalle 115 voci del gruppo 1. «Bibl.» riguarda autori, titolo, sede, anno e identificativo, confrontati con il registro; «Uso» riguarda l'affermazione di «Usata per». Mezzi: [reg] registro arXiv o Crossref, risposta grezza; [testo] ricerca testuale nel PDF o nella pagina scaricati.

| N. | Voce | Bibl. | Uso | Che cosa ho aperto e trovato |
|---|---|---|---|---|
| 1 | `angelopoulos2021` [4] [f7–f10] | coincide; manca la versione a stampa | trovato | [reg] arXiv v6, 7-12-2022. [testo] PDF v6: «this property marginal coverage, since the probability is marginal (averaged)…»; la scambiabilità è nel testo. Versione a stampa (Crossref): «Conformal Prediction: A Gentle Introduction», Foundations and Trends in Machine Learning 16(4):494–591, 2023, DOI 10.1561/2200000101. Lo 0,893–0,905 è una misura dello sciame, non della fonte |
| 2 | `bogoslavskyi2016` [9] | coincide | **non trovato** | [reg] Crossref: IROS 2016, pp. 163–169. LEGGIMI del deposito: cita l'articolo, licenza MIT; «connected» 0 occorrenze. Il metodo non è stato letto da nessuno |
| 3 | `dang2024` [17] | coincide | trovato nel riassunto | [reg] Crossref: Drones 8(9), 480, 12-9-2024; nel riassunto «occlusion perception module» e «adaptive motion compensation module … the UAV's complex movements»; VisDrone2019 e UAVDT |
| 4 | `dixit2022` [20] [f7–f10] | coincide; **sede ora verificata** | trovato nel riassunto | [reg] arXiv v1, 1-12-2022. Pagina degli atti aperta: Learning for Dynamics and Control Conference, PMLR 211:300–314, 2023 (autrice registrata «Skylar X Wei»). Nel riassunto «delayed agent observations» e «simulation case studies where a drone avoids a flying frisbee» |
| 5 | `hornung2013` [31] | coincide | **in parte** | [reg] Crossref: Autonomous Robots 34(3):189–206, aprile 2013. Pagina Springer, riassunto: «It explicitly represents not only occupied space, but also free and unknown areas». «Mondo statico»: 0 occorrenze nella pagina (riassunto e bibliografia): non verificato |
| 6 | `lindemann2023` [54] [f7–f10] | coincide | trovato | [reg] Crossref: RA-L 8(8):5116–5123, 2023. [testo] PDF arXiv v2: «is independently drawn from D»; «In general only exchangeability is needed»; «δ := 0.05 and T := 20»; «498 of the 500 test trajectories»; disuguaglianza di Boole |
| 7 | `luiten2021` [56] | coincide; manca il fascicolo | non trovato come frase | [reg] Crossref: IJCV 129(2):548–578, febbraio 2021, in linea 8-10-2020. Che HOTA chieda sequenze annotate non è nel riassunto: resta un giudizio del ruolo |
| 8 | `lupu2020` [57] | coincide | trovato; «dato diverso» confermato | [reg] Crossref: Sensors 20(20), 5821, 15-10-2020. Riassunto: «eight visually impaired subjects»; «the haptic stimuli were less intuitive than the audio ones»; il dispositivo «increased cognitive load and working memory» |
| 9 | `martinez2014` [62] | coincide | trovato; «dato diverso» confermato | [reg] Crossref: ICCHP 2014, LNCS, pp. 128–135. Pagina Springer: «for white cane users, auditory feedback results in a 22 times higher cognitive load than haptic feedback. This discrepancy … was not found on blindfolded users»; NASA-TLX. Numero dei partecipanti: non nel riassunto |
| 10 | `mercat2019` [64] [f7–f10] | coincide; sede a stampa non verificata | trovato | [reg] arXiv v4, 28-10-2020. [testo] PDF v4: riga «ours 0.75 1.81 3.16 4.80 6.70» (velocità costante); Tabella III, «V-LSTM [4]* 0.67 1.62 2.86 4.40 6.26» e «ours 0.68 1.54 2.72 4.20 5.95». La ricerca della sede su Crossref ha risposto 429 |
| 11 | `millane2024` [65] [f7–f10] | coincide; mancano DOI e pagine | trovato nel riassunto | [reg] arXiv v2, «Accepted to ICRA 2024»; Crossref: DOI 10.1109/ICRA57147.2024.10611532, pp. 2698–2705. Riassunto: «up to a 177x speed-up in surface reconstruction» (il 177 vale per la ricostruzione della superficie) |
| 12 | `oleynikova2017` [71] [f7–f10] | coincide; mancano le pagine | trovato nel riassunto | [reg] Crossref: IROS 2017, pp. 1366–1373. Riassunto: «runs in real-time on a single CPU core» |
| 13 | `plastropoulos2026` [76] | coincide | trovato | [reg] Crossref: The Aeronautical Journal 130(1346):1037–1067, aprile 2026. [testo] pagina dell'editore: entrambe le frasi citate presenti alla lettera |
| 14 | `rahaman2026` [79] [f7–f10] | coincide | trovato nel riassunto | [reg] arXiv v1, 13-2-2026: «distribution shift», «robust CP», «ORCA simulator» |
| 15 | `scholl1999` [84] [f7–f10] | coincide; link morto | **trovato** (prima: non verificato) | [reg] Crossref e PubMed (PMID 10090804): Cognitive Psychology 38(2):259–290, marzo 1999. Riassunto su PubMed: «Unimpaired performance required the presence of accretion and deletion cues along fixed contours at the occluding boundaries»; «imploding and exploding into and out of existence» |
| 16 | `timans2024` [95] | coincide | trovato nel riassunto | [reg] Crossref: ECCV 2024, LNCS, pp. 363–398, in linea 8-11-2024; frase citata presente nel riassunto arXiv |
| 17 | `usenko2017` [98] [f7–f10] | coincide | trovato nel riassunto | [reg] Crossref: IROS 2017, pp. 215–222; frase citata presente |
| 18 | `weitz2013` [101] [f7–f10] | voce senza dati; **identificazione mia, da confermare** | in parte | Deposito del DLR (scheda 81109) e Crossref: Paul Weitz, «Determination and Visualization of Uncertainties in 4D-Trajectory Prediction», convegno ICNS 2013 (Herndon, 23–25 aprile 2013), DOI 10.1109/ICNSURV.2013.6548525. È un articolo di convegno, non un rapporto. Riassunto: «three-dimensional ellipsoids» presente; «controller» 0 occorrenze (coerente con «senza esperimento con controllori», ma un'assenza nel riassunto non lo prova) |
| 19 | `yang2025` [107] | coincide | in parte | [reg] arXiv, tre versioni (v3 dell'8-3-2026): «MATR», 71,3 HOTA su DanceTrack, oltre 9 punti su MOTR. Che il ruolo intendesse questo articolo resta un'identificazione del curatore |
| 20 | `zhang2019` [109] | coincide | non controllato | [reg] Crossref: CVPR 2019, pp. 12077–12086. Lo 0,45 / 0,94 è della tabella di `scholler2020`, non del riassunto di questo articolo: non l'ho riletto |

**Conto.** Dati bibliografici: 19 su 20 coincidono con il registro, 0 errori; la ventesima (`weitz2013`) non aveva dati. Cinque completamenti (voci 1, 4, 7, 11, 12). Affermazione di «Usata per»: trovata in 14 (voci 1, 3, 4, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17), in parte in 3 (voci 5, 18, 19), non trovata o non controllata in 3 (voci 2, 7, 20). Zero errori su venti voci non sono una prova per le altre 95 del gruppo.

## 3. Stati che propongo

- **Verificato** (controllo esaustivo sull'insieme dichiarato): ogni chiave del documento di stato ha una voce (85 su 85); il `.bib` è ben formato (166 voci); i 67 identificativi arXiv e 88 degli 89 DOI portano al lavoro della voce; i conteggi per stato dell'elenco; nessuno stato dell'unione supera quelli dei gruppi.
- **Sostenuto dai dati** (campione di 20 su 115): i dati bibliografici del gruppo 1 sono corretti; le affermazioni di «Usata per» si ritrovano nella fonte in 14 casi su 20.
- **Smentito:** «verificata» per `bogoslavskyi2016` (il dato citato non è stato letto).
- **Non risolto:** se il ruolo di f8 intendesse davvero gli scritti che ho identificato per `weitz2013` e `hunt2013` (lo decide il ruolo); la frase «heavily distorted» dell'articolo ora identificato per `sciencedirect-s0926580524005867` (lo decide una lettura del testo, che è a pagamento); «mondo statico» in `hornung2013` (lo decide la lettura dell'articolo).
- **Non verificato da me:** il contenuto delle 270 voci fuori dal campione; la compilazione del `.bib` con `bibtex`.

## 4. Correzioni pronte da applicare

### 4.1 A `unione/RIFERIMENTI.md`

- **R1 — `weitz2013` [101].** Autori: Paul Weitz. Titolo: Determination and Visualization of Uncertainties in 4D-Trajectory Prediction. Sede e anno: 2013 Integrated Communications, Navigation and Surveillance Conference (ICNS), Herndon, 23–25 aprile 2013, pp. 1–9. Identificativo: DOI 10.1109/ICNSURV.2013.6548525. Link: https://elib.dlr.de/81109/. Tipo: articolo di convegno (non «rapporto DLR»). Verifica: «verificata in parte — (verifica-rif) identificazione del curatore, da confermare dal ruolo; riassunto letto nel deposito del DLR: "three-dimensional ellipsoids" presente». Prova: metadati della scheda 81109 e Crossref.
- **R2 — `hunt2013` [35].** Autori: Sarah Marie Hunt. Titolo: The Impact of Trajectory Prediction Uncertainty on Reliance Strategy and Trust Attitude in an Automated Air Traffic Management Environment. Sede e anno: tesi di Master of Science, San José State University, 2013. Identificativo: DOI 10.31979/etd.a9t8-bwjc. Link: https://scholarworks.sjsu.edu/etd_theses/4391. Verifica: «verificata in parte — (verifica-rif) identificazione del curatore, da confermare dal ruolo; letti i metadati e l'inizio del riassunto». Prova: metadati della pagina del deposito dell'università.
- **R3 — `sciencedirect-s0926580524005867` [86].** Autori: Tyler Parsons; Fattah Hanafi Sheikhha; Jaho Seo; Hanmin Lee. Titolo: RGB-LiDAR sensor fusion for dust de-filtering in autonomous excavation applications. Sede e anno: Automation in Construction, vol. 168, articolo 105850, dicembre 2024. Identificativo: DOI 10.1016/j.autcon.2024.105850; PII S0926580524005867. Verifica: «verificata in parte — (verifica-rif) identificata su Crossref dal codice dell'articolo; "heavily distorted" non letto». Togliere «a memoria: non verificato» dalla sede. La chiave può restare.
- **R4 — `dixit2022` [20].** Sede e anno: «Learning for Dynamics and Control Conference (L4DC 2023), Proceedings of Machine Learning Research 211:300–314, 2023; arXiv 1-12-2022». Aggiungere il link https://proceedings.mlr.press/v211/dixit23a.html. Nella nota togliere «"in simulazione" non ricontrollato»: è nel riassunto.
- **R5 — `millane2024` [65].** Sede e anno: «2024 IEEE International Conference on Robotics and Automation (ICRA), pp. 2698–2705». Identificativo: aggiungere DOI 10.1109/ICRA57147.2024.10611532. Nota: il 177 vale per la ricostruzione della superficie.
- **R6 — `angelopoulos2021` [4].** Sede e anno: aggiungere «versione a stampa, con altro titolo: "Conformal Prediction: A Gentle Introduction", Foundations and Trends in Machine Learning 16(4):494–591, 2023, DOI 10.1561/2200000101». Verifica: «verificata … — (verifica-rif) "marginal coverage" e la scambiabilità trovate nel testo del PDF v6».
- **R7 — `oleynikova2017` [71].** Sede e anno: aggiungere «pp. 1366–1373».
- **R8 — `bewley2016` [8].** Sede e anno: sostituire «pagine: manca (non controllate)» con «pp. 3464–3468».
- **R9 — `uhlemann2024` [97].** Sede e anno: sostituire «2024 (volume e pagine: non letti)» con «vol. 25(10), pp. 13937–13946, ottobre 2024».
- **R10 — `luiten2021` [56].** Sede e anno: «vol. 129, n. 2, pp. 548–578».
- **R11 — `scholl1999` [84].** Link: sostituire il link morto con https://doi.org/10.1006/cogp.1998.0698 e https://pubmed.ncbi.nlm.nih.gov/10090804/. Verifica: «verificata … — (verifica-rif) riassunto su PubMed: "accretion and deletion cues along fixed contours"». Togliere la nota «sostituire il link con il DOI».
- **R12 — `lindemann2023` [54].** Verifica: «verificata … — (verifica-rif) le quattro frasi e il 498 su 500 trovati nel testo del PDF arXiv v2 (non nella versione della rivista)».
- **R13 — `mercat2019` [64].** Verifica: «verificata … — (verifica-rif) le tre righe di RMSE trovate nel testo del PDF arXiv v4». Precisare in «Usata per» che il «Kalman-LSTM» è la riga «ours» della Tabella III.
- **R14 — `bogoslavskyi2016` [9].** Verifica: da «verificata … pagina aperta e dato presente» a «verificata … in parte» (dati bibliografici e deposito; il metodo non è stato letto).
- **R15 — `hornung2013` [31] e `octomap` [220].** In `hornung2013`, Verifica: aggiungere «(verifica-rif) riassunto letto sulla pagina Springer: "not only occupied space, but also free and unknown areas"; "mondo statico" non è nel riassunto». Nelle note di entrambe aggiungere il rimando all'altra.
- **R16 — `depthtrack` [247].** Identificativo: aggiungere «arXiv:2108.13962». Usata per: aggiungere `f10-dati/12-dati-veri/convertitori/converti_depthtrack.py` (riga 5), con la marca [f7–f10: non vagliato dall'arbitro].
- **R17 — `librealsense` [209] e `realsense-file-di-esempio` [255].** In `librealsense`, Link: aggiungere https://github.com/IntelRealSense/librealsense/blob/master/doc/post-processing-filters.md (citato in `f10-dati/02-sensori/parametri_sensori.json`, riga 12) e https://github.com/IntelRealSense/librealsense/tree/master/doc (citato in `f10-dati/02-sensori/MODELLO_SENSORE.md`), e togliere `doc/sample-data.md` dal titolo e dal link, con il rimando a `realsense-file-di-esempio`.
- **R18 — `tum-rgbd` [257].** Link: aggiungere https://cvg.cit.tum.de/data/datasets/rgbd-dataset/file_formats (citato in `f10-dati/12-dati-veri/convertitori/converti_tum.py`, riga 6).
- **R19 — `drow` [248].** Link: aggiungere, come indirizzo citato, https://github.com/RWTHVision/DROW (in `f10-dati/01-ricercatore/DATI_PUBBLICI.md`).
- **R20 — `friburgo-rgbd-people` [249].** Pagine dei due articoli associati (Crossref): IROS 2011, pp. 3838–3843 (DOI …6095074) e pp. 3844–3849 (DOI …6095075).
- **R21 — `guibas1997` [27].** Aggiungere il titolo della versione estesa: «A Visibility-Based Pursuit-Evasion Problem».
- **R22 — §0, tabella dei conteggi** (dopo R1–R3, R6, R11–R14). Riga 1: verificata 66, in parte 38, dato diverso 9, aperta dal ruolo 0, solo riassunto 0, non verificata 1, non raggiungibile 1, totale 115. Totale: **164 / 58 / 21 / 22 / 5 / 8 / 12 = 290**. Nel capoverso «Fonti inesistenti» togliere `hunt2013`, `weitz2013` e `sciencedirect-s0926580524005867` dalle «non identificabili» (resta `koschi-mediatum-1575368`); toglierle anche dal §8.5, lasciando l'avvertenza che l'identificazione va confermata.
- **R23 — §0, «Controllo di completezza».** Aggiungere: «Ripetuto alle 17:12 da verifica-rif su tutti i file di testo: 309 indirizzi, 1 identificativo arXiv assente (2108.13962, ora in `depthtrack`), 0 DOI assenti».

### 4.2 A `unione/riferimenti.bib`

- **B1 — `weitz2013`:** sostituire la voce con
  `@inproceedings{weitz2013, author = {Paul Weitz}, title = {{Determination and Visualization of Uncertainties in 4D-Trajectory Prediction}}, booktitle = {2013 Integrated Communications, Navigation and Surveillance Conference (ICNS)}, pages = {1--9}, year = {2013}, doi = {10.1109/ICNSURV.2013.6548525}, url = {https://elib.dlr.de/81109/}, note = {[101] Stato di verifica: verificata dal curatore il 14-11-2026 in parte; identificazione da confermare. Citata solo nelle estensioni f7--f10 o nei file esterni: non ancora vagliata dall'arbitro.}}`
- **B2 — `hunt2013`:** sostituire con
  `@mastersthesis{hunt2013, author = {Sarah Marie Hunt}, title = {{The Impact of Trajectory Prediction Uncertainty on Reliance Strategy and Trust Attitude in an Automated Air Traffic Management Environment}}, school = {San Jos{\'e} State University}, year = {2013}, doi = {10.31979/etd.a9t8-bwjc}, url = {https://scholarworks.sjsu.edu/etd_theses/4391}, note = {[35] Stato di verifica: verificata dal curatore il 14-11-2026 in parte; identificazione da confermare. Citata solo nelle estensioni f7--f10 o nei file esterni: non ancora vagliata dall'arbitro.}}`
- **B3 — `sciencedirect-s0926580524005867`:** sostituire con
  `@article{sciencedirect-s0926580524005867, author = {Tyler Parsons and Fattah {Hanafi Sheikhha} and Jaho Seo and Hanmin Lee}, title = {{RGB-LiDAR sensor fusion for dust de-filtering in autonomous excavation applications}}, journal = {Automation in Construction}, volume = {168}, pages = {105850}, year = {2024}, doi = {10.1016/j.autcon.2024.105850}, url = {https://www.sciencedirect.com/science/article/pii/S0926580524005867}, note = {[86] Stato di verifica: verificata dal curatore il 14-11-2026 in parte. Citata solo nelle estensioni f7--f10 o nei file esterni: non ancora vagliata dall'arbitro.}}`
- **B4 — `dixit2022`:** tipo `@inproceedings`; togliere `howpublished`; aggiungere `booktitle = {Learning for Dynamics and Control Conference (L4DC), Proceedings of Machine Learning Research}`, `volume = {211}`, `pages = {300--314}`, `year = {2023}`.
- **B5 — `millane2024`:** `booktitle = {2024 IEEE International Conference on Robotics and Automation (ICRA)}`, `pages = {2698--2705}`, `doi = {10.1109/ICRA57147.2024.10611532}`.
- **B6 — `oleynikova2017`:** aggiungere `pages = {1366--1373}`.
- **B7 — `bewley2016`:** aggiungere `pages = {3464--3468}`.
- **B8 — `uhlemann2024`:** aggiungere `volume = {25}`, `number = {10}`, `pages = {13937--13946}`.
- **B9 — `luiten2021`:** aggiungere `number = {2}`.
- **B10 — `scholl1999`:** `url = {https://doi.org/10.1006/cogp.1998.0698}`; nel `note` lo stato «pagina aperta e dato presente».
- **B11 — campo `note` degli stati cambiati:** `angelopoulos2021`, `lindemann2023`, `mercat2019` → «pagina aperta e dato presente»; `bogoslavskyi2016` → «in parte». In `angelopoulos2021` aggiungere al `note` la versione a stampa (R6).
- **B12 — riga di testa del file:** dopo B1–B4 i tipi diventano 45 article, 1 book, 42 inproceedings, 13 manual, 1 mastersthesis, 62 misc, 1 phdthesis, 1 techreport (totale 166). In `lin2014` aggiungere al `note`: «autori della versione arXiv; negli atti sono otto».

### 4.3 A `unione/STATO_PROGETTO.md`

- **S1 — appendice B, riga `[koschi2021]` (1515).** Link: sostituire https://mediatum.ub.tum.de/doc/1575368/1575368.pdf con https://doi.org/10.1109/TIV.2020.3017385 (il primo è il documento della voce `koschi-mediatum-1575368`).
- **S2 — appendice B, righe `[ue-2019-945]` e `[ue-2019-947]` (1563–1564).** Per la prima il link della voce è https://www.legislation.gov.uk/eur/2019/945/annex (copia britannica); per la seconda «manca». La pagina dell'EASA oggi indicata è la voce `easa-drones-regole`: scriverlo, oppure citare quella chiave.
- **S3 — appendice B, riga `[librealsense]` (1518).** Nessun cambio se si applica R17.
- **S4 — §10.1, riquadro 6.** Sostituire «non ancora verificato: `f11-documentazione/verifica-rif/` era vuota alle 17:04» con «verificato alle 17:20 (`f11-documentazione/verifica-rif/VERIFICA_RIFERIMENTI.md`): 0 chiavi orfane, 0 identificativi sbagliati, 23 correzioni all'elenco». La stessa frase nell'introduzione dell'appendice B («non è ancora verificato»).
- **S5 — riga 1125 (§8.2), per l'arbitro perché cambia un'affermazione.** La correzione (a) è confermata dalla mia rilettura dei due riassunti. Frase pronta: «Suono o vibrazione: gli studi sono discordi. Per chi usa il bastone il sonoro dà un carico cognitivo 22 volte maggiore dell'aptico [martinez2014]; in un altro studio, con otto persone, gli stimoli aptici risultano meno intuitivi di quelli sonori [lupu2020]. Non decide (K-010, aperta).»
- **S6 — registro delle modifiche.** Una riga: «verifica dell'elenco dei riferimenti; corrette quattro righe dell'appendice B».

## 5. Proposte nuove

- **`fonti-verifica-1` — uno stato in più: «verificata sul riassunto».** Meccanismo: oggi lo stesso grado di lettura (dato trovato nel riassunto del registro) è «verificata» per rif-4 e «in parte» per rif-3; uno stato proprio toglie la differenza e mostra al lettore quante voci non sono state lette nel testo. Previsione: riclassificando, almeno 30 delle 161 «verificate» passano al nuovo stato. La smentisce un conteggio sotto 30.
- **`fonti-verifica-2` — dividere le otto voci di gruppo** (§1.2) in una voce per fonte. Meccanismo: una chiave che copre quattro insiemi di dati non si può citare né verificare. Previsione: dividendo `insiemi-non-raggiungibili`, almeno due dei quattro insiemi si trovano con un indirizzo. La smentisce una ricerca che ne trova meno di due.
- **`fonti-verifica-3` — rileggere nel testo le 10 voci «verificate» lette solo con lo strumento che riassume.** Previsione: almeno una porta una cifra diversa da quella citata. La smentisce una rilettura in cui tutte e dieci confermano.

## 6. Che cosa propongo dopo

1. Applicare R1–R23, B1–B12 e S1–S4, S6: non cambiano affermazioni tecniche. S5 e i cambi di stato del §0 vanno all'arbitro.
2. Far confermare al ricercatore di f8 (`f8-continuita/07-ricercatore/FONTI.md`, §5) le due identificazioni R1 e R2.
3. Ripetere il programma dei link e degli identificativi a ogni chiusura di un'estensione f7–f10: i ruoli stanno ancora scrivendo.
4. Allargare il campione del §2 alle altre 95 voci del gruppo 1 prima di usare l'elenco in un testo per la giuria, a partire dalle voci citate nel documento di stato.
