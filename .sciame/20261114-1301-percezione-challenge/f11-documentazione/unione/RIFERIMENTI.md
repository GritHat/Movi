# Riferimenti del progetto — elenco unico (percezione-challenge)

Curatore delle fonti (`sciame-fonti`), fase f11 (documentazione), unione dei quattro elenchi parziali. 14 novembre 2026; unione chiusa alle 16:50. I percorsi dei file dello sciame sono relativi a `.sciame/20261114-1301-percezione-challenge`. Il file BibTeX con le stesse chiavi è `f11-documentazione/unione/riferimenti.bib` (166 voci).

## 0. In testa

**A che cosa serve.** È l'elenco di tutti gli articoli scientifici e delle altre fonti esterne che lo sciame ha citato nelle fasi f1–f6 (chiuse) e nelle estensioni f7–f10 (in corso), con i dati bibliografici, il link, lo stato di verifica e, per ogni fonte, le affermazioni che le sono state appoggiate e il file che la cita. Serve a tre cose: (1) citare nel documento di stato e nei testi per la giuria solo ciò che una fonte dice davvero; (2) sapere, per ogni cifra presa da fuori, chi l'ha letta e come; (3) tenere in un posto solo le correzioni (attribuzioni sbagliate, cifre diverse dalla fonte). Va aggiornato a ogni nuova valutazione: una fonte nuova entra con una voce nel formato qui sotto, una fonte riletta cambia il campo «Verifica».

**Da dove viene.** Dai quattro elenchi parziali scritti oggi da quattro curatori: `f11-documentazione/rif-1/RIFERIMENTI_rif-1.md` (f1 e la verifica di f3: 84 voci), `rif-2/RIFERIMENTI_rif-2.md` (f2, f3, f4, f5: 53 voci), `rif-3/RIFERIMENTI_rif-3.md` (f6: 59 voci), `rif-4/RIFERIMENTI_rif-4.md` (f7–f10 e tre file esterni: 139 voci). In tutto 335 voci, contate dal programma che ha letto i quattro file; dopo l'unione **290 voci distinte**: 287 dalla fusione dei doppioni, una separata a mano (`iso-10218-2`) e due che mancavano in tutti e quattro gli elenchi e che ho aggiunto io dopo il controllo di completezza (`thipphavong2016`, `ldrobot-ldlidar-stl-sdk`). 42 voci sono citate da più di un gruppo. Dove una voce viene da più gruppi, il campo «Verifica» riporta ciò che ha accertato ciascuno, con la sigla del gruppo fra parentesi, e lo stato in testa al campo è il più forte fra quelli accertati; se però un gruppo ha trovato un dato diverso dalla fonte, lo stato è «dato diverso», perché è la cosa che chi cita deve sapere.

**Che cosa vuol dire «verificata» qui.** Riguarda la fonte: esiste, con questi autori e questa sede, e il dato citato c'è. Non riguarda il sistema: una scheda verificata dice che cosa dichiara il costruttore, non che il prototipo funzioni. Nel progetto **niente è provato sull'hardware**; le misure dello sciame restano «sostenute dai dati in simulazione», a sensore fermo. Tutto ciò che viene dalle estensioni f7–f10 **non è ancora vagliato dall'arbitro**: gli usi sono marcati riga per riga con «[f7–f10: non vagliato dall'arbitro]». La fase f6, pur chiusa, non è passata dall'arbitro (lo annota la sezione C del documento di stato, `f11-documentazione/sez-c/SEZIONE.md`).

**Legenda degli stati di verifica** (la dicitura apre il campo «Verifica» di ogni voce; dopo il trattino c'è il dettaglio, gruppo per gruppo).
- **verificata dal curatore il 14-11-2026: pagina aperta e dato presente** — almeno un curatore (quello di f3 o uno dei quattro di f11, tutti oggi) ha aperto la fonte e vi ha trovato il dato citato. Il dettaglio dice con quale mezzo (vedi le sigle) e che cosa non è stato riletto.
- **verificata dal curatore il 14-11-2026 in parte** — il curatore ha confermato che la fonte esiste e i suoi dati bibliografici, oppure solo una parte dei dati citati; il contenuto citato non è stato riletto da un curatore (di solito l'ha letto il ruolo che cita, o sta nel corpo dell'articolo).
- **dato diverso** — la fonte è stata aperta e una cifra o un'attribuzione scritta nei file dello sciame non coincide con ciò che la fonte dice; il dettaglio dà il dato giusto.
- **aperta dal ruolo che la cita** — l'ha letta solo il ruolo; il curatore al più ha controllato che la pagina risponda.
- **vista solo nel riassunto di un motore di ricerca** — nessuno ha aperto la pagina.
- **non verificata** — non aperta da nessuno (di solito testi a pagamento o pagine di rivenditori).
- **non raggiungibile** — qualcuno ha provato ad aprirla oggi e non ci è riuscito (errore 403 o 404, protezioni contro i programmi automatici, dominio che non risolve).

**Sigle dentro il dettaglio.** [g] dato trovato con una ricerca testuale nel testo grezzo scaricato (pagina, PDF, registro); [T] lo stesso, nel gruppo rif-4; [r] letto attraverso lo strumento di lettura che riassume (più debole); [m] metadati da Crossref o dall'interfaccia di GitHub (rif-3); [API] dati bibliografici, e a volte il riassunto, letti nel registro di arXiv, Crossref, PubMed o Zenodo (rif-4); [200] la pagina risponde, contenuto non riletto. A, A-g, R sono le marche dei ruoli (aperta con lo strumento che riassume; frase trovata nel testo; solo riassunto di ricerca). F1–F30 e S1–S38 sono i numeri delle fonti nei file dei ruoli. «f3» è la verifica del curatore in `f3/fonti/FONTI_VERIFICATE.md`, fatta oggi. I registri bibliografici valgono per autori, sede, pagine e DOI, non per il contenuto.

**Conteggi** (contati dal programma dell'unione sulle voci di questo file).

| Tipo | verificata | verificata in parte | dato diverso | aperta dal ruolo | solo riassunto di ricerca | non verificata | non raggiungibile | Totale |
|---|---|---|---|---|---|---|---|---|
| 1. Articoli scientifici e prestampe (con tesi, libri e rapporti) | 63 | 38 | 9 | 0 | 2 | 1 | 2 | 115 |
| 2. Schede tecniche e documenti dei costruttori (con le pagine dei rivenditori) | 24 | 1 | 3 | 5 | 3 | 4 | 6 | 46 |
| 3. Norme e documenti regolatori | 16 | 10 | 4 | 1 | 2 | 3 | 2 | 38 |
| 4. Documentazione di software e depositi di codice | 32 | 4 | 1 | 9 | 0 | 0 | 0 | 46 |
| 5. Insiemi di dati | 8 | 3 | 1 | 1 | 0 | 0 | 1 | 14 |
| 6. Comunicati e altre fonti (stampa, blog, forum, enciclopedie) | 18 | 2 | 3 | 6 | 0 | 0 | 2 | 31 |
| **Totale** | **161** | **58** | **21** | **22** | **7** | **8** | **13** | **290** |

- Per stato: 161 verificate, 58 verificate in parte, 21 con un dato diverso, 22 aperte solo dal ruolo, 7 viste solo in un riassunto di ricerca, 8 non verificate, 13 non raggiungibili.
- 129 voci sono citate solo nelle estensioni f7–f10 o nei file esterni (non vagliate dall'arbitro); altre 13 hanno usi sia nelle fasi chiuse sia nelle estensioni.
- Attenzione al grado: «verificata» copre letture del testo intero, letture del solo riassunto e letture attraverso lo strumento che riassume. Il grado è scritto nel dettaglio di ogni voce e non va appiattito.

**Cambi di stato proposti dai gruppi** (li decide l'arbitro; riguardano le fonti e le etichette, non gli enunciati tecnici, che restano con lo stato che hanno: al più dimostrati in un modello dichiarato o sostenuti dai dati in simulazione, mai provati sull'hardware).
1. La frase «in due studi l'aptico costa più dell'audio» (`f2/05-selezione/SELEZIONE.md`, riga K-010; `f3/H-012/01-scene-dinamiche/SOLUZIONE.md`, §5): da «fonti» a **smentita come scritta** (`martinez2014`, `lupu2020`).
2. `f2/04-torneo/TORNEO.md`, «D435i ≤ 2 % fino a 2 m»: da «non aperta (403)» a verificata sulla fonte (`realsense-d400-accuratezza`).
3. `f2/01-traduzione/SCHEDE.md`, `creativo-4`, «modo 4×4 a 60 Hz del VL53L5CX non verificato sul testo»: verificato sulla fonte (`st-um2884`, Tabella 2).
4. `f5/02-audit/AUDIT.md`, ipotesi 1 (filtri dell'SDK): da «letto il riassunto della ricerca» a verificata sulla pagina (`realsense-filtri-post`); ipotesi 11 («69°×42°»): trovato nella pagina di confronto, con riserva sull'attribuzione della colonna (`realsense-confronto-camere`).
5. Il secondo aggancio per il giurato (`f6-specializzazione/01-esperto-dominio/SPECIALIZZAZIONE.md`, §6): da «non riverificabile in rete» a sostenuto dalle fonti per la sola parte documentale (`px4-collision-prevention`, `px4-obstacle-distance`); che il prototipo produca quel messaggio resta non provato.
6. Nel bilancio della latenza (circa 155 ms) la riga del sensore va chiamata «limite superiore del sistema di prova del costruttore»; R7 resta **non risolta** fino alla prova H12 (`realsense-alta-velocita-d435`).

**Regole violate e scostamenti** (miei e dei gruppi, anche per errore).
- All'unione **non ho riaperto le fonti**: gli stati sono quelli accertati dai quattro curatori e da f3. Ho fatto solo tre controlli in rete (16:33, una decina di secondi) per sciogliere tre discordanze fra gruppi o fra un gruppo e una sezione (`zhou2025`, `therobotreport-veo`, `park2026`), e alle 16:45 ho aperto il rapporto NASA che mancava in tutti gli elenchi (`thipphavong2016`). Le previsioni erano scritte prima in `f11-documentazione/unione/stato_riferimenti.md`: U1, U2, U3 e U5 reggono; U4 (fra 285 e 300 voci dopo l'unione) regge, 290. Nelle richieste nessun nome di persona né dettaglio del progetto.
- Regola 3: i gruppi rif-1, rif-3 e rif-4 non hanno scritto previsioni prima delle verifiche; rif-2 sì (sei, in `rif-2/stato.md`).
- Regola 5: il materiale scaricato dai curatori sta nelle cartelle temporanee delle sessioni, non nel progetto; niente è stato eseguito dal suo interno. A rif-1 e a rif-3 lo strumento di lettura ha salvato da solo un PDF fuori dalla cartella di consegna. Le pagine e il PDF che ho scaricato io sono nella cartella temporanea della sessione.
- **Un errore mio, senza effetti sul progetto.** La cartella temporanea della sessione è condivisa fra i ruoli: un altro ruolo di f11 (quello che compone il documento di stato) ha usato una sottocartella con lo stesso nome della mia e alle 16:45 il suo programma ha preso il posto del mio. Alle 16:46 ho quindi eseguito per errore il suo programma, senza l'opzione di scrittura: ha scritto solo due file di lavoro nella cartella temporanea (`anteprima.md`, vuoto, e `usate.json`), niente nella cartella del progetto (controllato: nella cartella di consegna c'erano solo i miei tre file, con le ore invariate). Ho spostato i miei file in una sottocartella mia e riscritto il programma. Chi compone il documento di stato deve rigenerare quei due file di lavoro.
- Nella cartella di consegna, che è condivisa con quel ruolo, il mio file di stato si chiama `stato_riferimenti.md` e non `stato.md`, per non confonderlo con il suo.
- La consegna dice «niente git»: alle 16:50 ho eseguito una volta `git status`, in sola lettura, per controllare di aver scritto solo nella cartella di consegna (è così: tre file, `RIFERIMENTI.md`, `riferimenti.bib`, `stato_riferimenti.md`). Nessuna modifica al deposito.
- Alcuni link delle fonti contengono il nome della società promotrice: rif-3 li ha aperti così come sono citati.
- Lettura parziale: rif-2 e rif-4 hanno letto parte dei file dello sciame solo con ricerche testuali per parole chiave; un riferimento scritto a parole, senza link, anno o sigla, può mancare. rif-4 ha chiuso l'estrazione alle 16:18: ciò che i ruoli di f7–f10 hanno scritto dopo non c'è.
- Indipendenza: i curatori, io e i ruoli che citano condividiamo il modello linguistico. L'indipendenza sta nel testo delle fonti e nelle risposte dei registri; vale meno dove la lettura è passata dallo strumento che riassume ([r]).
- Per la classificazione: lo stato in testa a ogni voce l'ho assegnato io: per le voci di un solo gruppo con una regola scritta applicata al campo «Verifica» del gruppo (più otto correzioni a mano), per le 42 voci di più gruppi a mano; il testo dei gruppi è riportato intero nel dettaglio, così l'assegnazione si può ricontrollare.

**Correzioni importanti.**

*Fonti inesistenti.* **Nessuna** fra quelle che hanno un link o un identificativo: i quattro gruppi le hanno trovate tutte (compresi i 35 identificativi arXiv delle estensioni). Restano **non identificabili**, quindi di esistenza non verificata: `hunt2013`, `weitz2013`, `sciencedirect-s0926580524005867` (citate senza titolo) e `koschi-mediatum-1575368` (documento dietro una protezione). Senza alcun riferimento: le prove NEES/NIS, Glidance Glide, biped NOA, e i rimandi opachi `<Cite ref=…>` della bozza della squadra (vedi §8.4).

*Attribuite male o in modo impreciso.*
1. `martinez2014`, `lupu2020` — «in due studi l'aptico costa più dell'audio» non è ciò che dicono. Martinez e altri: per chi usa il bastone è il **sonoro** a dare un carico cognitivo 22 volte maggiore dell'aptico, e l'effetto non c'è nei vedenti bendati. Lupu e altri (otto persone): stimoli aptici «less intuitive» di quelli sonori; il carico maggiore è del dispositivo rispetto al bastone. La frase giusta è «studi discordi».
2. `realsense-alta-velocita-d435` — i 95 ms «esposizione → fotogramma» a 30 fps sono nella fonte, ma misurano un ciclo completo con GPU, schermo a 120 Hz e USB: sono un limite superiore del sistema di prova, non la latenza del sensore. La somma di circa 155 ms è un conto giusto su un addendo che sovrastima.
3. `realsense-forum-latenza` — i «35 ms a 90 fps» sono del flusso infrarosso di una D455, non della profondità.
4. `liu2022` — non parla di occlusione (0 occorrenze nel testo); la frase su occlusione e moto della camera insieme regge solo con `dang2024`.
5. `eurocae-ed-275`, `rtca-do-365` — ED-275 è la norma del sistema anticollisione ACAS Xu, non una norma generale sul «detect and avoid»; DO-365C lo è. Le cifre «35 s e oltre un chilometro» non sono in nessuna delle due pagine citate: **non verificate**. Una fonte aperta per quell'ordine di grandezza esiste, ma il quadro di dominio non la cita: `thipphavong2016` (rapporto della NASA: 35 s e 4000 piedi, circa 1,2 km, portati a 0,75 miglia nautiche con un margine per l'incertezza), letta all'unione.
6. `astm-f3442-25` — «esclude gli incontri fra droni» è impreciso: la norma definisce una metrica per le collisioni fra droni e rinvia le soglie.
7. `easa-faq-open-category`, `ue-2019-945` — i 3 m/s del modo lento non sono nella pagina dell'EASA citata, ma nel regolamento delegato (UE) 2019/945 (parte 3, punto 9); i 19 m/s ci sono in entrambe. Cifre giuste, fonte indicata sbagliata.
8. `mandaokar2026` — «errori laterali fino a 0,9 m» va scritto «errori medi di posizione di al più 0,15, 0,93 e 0,87 m sui tre assi»; è una prestampa in revisione.
9. `rossi2025` — la prestampa è ora un articolo su Sensors; «prestazioni imprevedibili» non è nel riassunto, che dà errori dell'ordine del mezzo metro fra 4 e 16 m.
10. `teleborsa-nido-2026` — «opzione per il 51 %» non è nella pagina: c'è «opzione per il controllo entro 24 mesi».
11. `maregroup-ordine-uncrewed-2026` — la pagina della società non nomina CTMAVIO né «prevalentemente nel 2026»: stanno nelle tre voci di stampa.
12. `vogiatzoglou2024` — è un contributo di un'autrice sola in un blog accademico; «duplice uso» non è nel testo. La fonte primaria è `ue-2024-1689`.
13. `easa-drones-regole` — la pagina non nomina il regolamento 2021/664 né la decisione 2025/018/R.
14. `shan2022` — applica l'intersezione delle covarianze, non ne è la fonte originale.
15. `koschi2021` — non «IEEE T-IV 2020» ma vol. 6(2), pp. 249–265, 2021. Il quadro di dominio (S33) cita un altro documento, non identificato (`koschi-mediatum-1575368`).
16. `weng2020` — l'articolo è a IROS 2020; arXiv 2008.08063 è il riassunto esteso per i Workshop di ECCV 2020.
17. `adamides2025` — è la fonte F26, citata senza autori né titolo; l'affermazione che le si appoggia (distanza protettiva con incertezza e latenza) **non** è nel riassunto: non verificata. Vale anche per `iso-ts-15066`, mai letta.
18. `zhang2026a` — «derivato da SAM 2» non è verificato: il riassunto dice «leverages SAM».
19. `gulf-times-ally-solos` — l'articolo non dice dove avviene l'elaborazione; la frase sulla navigazione riguarda gli occhiali intelligenti in generale.
20. `pololu-vl53l8cx-3419` — il link porta alla scheda del VL53L8CX, non del VL53L7CX.
21. `park2026` — articolo di un workshop di CVPR 2026, non della conferenza principale.
22. `duberg2020`, `ufomap-deposito` — «real-time (2 Hz) at 2 mm» sta nel README del deposito, non nell'articolo.
23. `eurocontrol-asterix-cat062` — l'edizione letta è la 1.18, in una trascrizione non ufficiale; quella corrente è la 1.21 (5 giugno 2025).
24. `cheraghipouria2026` (cognome del primo autore: Cheraghi Pouria), `kress2021` (non solo prestampa: IEEE T-IV 8(3), 2023), `hetzel2024` (capitolo in Lecture Notes in Computer Science, 2025).
25. `skoglar2012` — il DOI esiste, ma che l'articolo tratti l'evidenza negativa non è verificato.
26. `kayukawa2019` — la citazione testuale «6 blind participants» non c'è; c'è «six blind users».
27. `iata-enhanced-gse-2022` — il 42 % vale se il 75 % della flotta passa ai mezzi evoluti: la condizione manca nel file che cita.
28. `mrpt-octomap-opzioni` — è la documentazione di una libreria terza; la fonte primaria dei parametri è il sorgente di `octomap`.
29. `standley2017`, `lee2026` — i «circa 150 000 prodotti» sono nel testo dell'articolo del 2017; l'errore 1,066 attribuito a image2mass viene dalla Tabella 1 di Lee e altri.
30. `flir-boson` («1 W» non è nella pagina), `nvidia-cuvslam` (licenza e pacchetto non commerciale non sono nella pagina), `intel-t265-fine-produzione` (anno e frase citata non verificati).
31. `joslyn2021`, `machado2009` — esiste una rettifica pubblicata che nessun ruolo cita; non letta.
32. `kozlov2026` — non confondere i due gruppi: 92,9 % su 22 partecipanti senza disabilità visiva, 93,75 % su 14 con disabilità visiva.

*Cifre diverse dalla fonte.*
1. `zholus2025` — con 1024 punti 187 fps su H100 (42 su V100), non 348.
2. `ldrobot-ld19` — tenuta alla luce 30 klx, non 60 (i 60 klx sono dell'STL-19P); risoluzione angolare «≤1°», lo 0,8° è derivato.
3. `ultralytics-yolo26` — «YOLOE-26 40,6 AP su LVIS» è della variante x, non di un modello leggero; i 38,9 ms sono su una CPU da server.
4. `lee2026` — il «fattore medio 1,68» non è nell'articolo: è exp(0,519), calcolato dal ricercatore.
5. `ding2026` — 25,6 fps confermati, ma su una GPU da centro di calcolo (colonna «FPS V100»).
6. `roboticscenter-d455` — prezzo oggi 650 $, non 399–417 $; `livox-mid-360` — prezzo non verificato. **Tutti i prezzi** vanno ricontrollati a mano prima di scriverli.
7. `orbbec-femto-bolt` — la pagina porta sia «Indoor» sia «Indoor/Semi-Outdoor»: la discordanza K-009 fra costruttori resta.
8. Completamenti che non cambiano le conclusioni: `scholler2020` (la velocità costante campionata, 0,28 / 0,56, sta sotto S-GAN a parità di valutazione); `st-um2884` (4×4 fino a 60 Hz, 8×8 fino a 15 Hz: confermato).

*Discordanze fra i gruppi, sciolte all'unione* (la differenza è annotata nella voce). `zhou2025` (sede CVPR 2025: confermata su Crossref); `st-um2884` (non raggiungibile per rif-1, letta da rif-2); `zhang2026` (una chiave per due articoli: ora `zhang2026a` e `zhang2026b`); `schoeller2020` e `scholler2020` (una voce); `livox-mid-360` (rivenditore o costruttore); `slamtec-rplidar-c1` e `waveshare-rplidar-c1`, `ldrobot-ld19` e `ldrobot-ld19-scheda` (pagine diverse, voci separate); `realsense-taratura-profondita` e `realsense-bkm-taratura` (la stessa guida in rete e in PDF, più un link morto dei forum Intel); `koschi2021` (articolo o altro documento); `iso-ts-15066` e `iso-10218-2` (separate); `rtca-do-365`, `eurocontrol-asterix-cat062` (edizioni); `therobotreport-veo` (autrice e data: Clara Vu, 1 luglio 2020, confermate oggi).

*Link morti o da sostituire.* Il dominio intelrealsense.com non risolve più (usare realsenseai.com); `intel-000030012`, `intel-t265-fine-produzione` e il link dei forum Intel alla guida di taratura sono morti; il PDF di `martinez2014` sul sito del KIT e quello di `scholl1999` danno 404 (usare il DOI); `journal-aviation-donecle` dà 404; st.com, EUR-Lex, iso.org, mediaTUM, skybrary.aero e mdpi.com hanno rifiutato le letture automatiche (dove c'era, è stata usata una copia, e la voce lo dice).

**Controllo di completezza sui link.** Ho estratto con una ricerca testuale tutti gli indirizzi di rete scritti nei file `.md` della convocazione fuori da f11 (escluse le cartelle `scaricati/`, `pagine/`, `ambiente/`, cioè le copie di pagine altrui) e nei tre file esterni: alle 16:48, 215 file più 3, **293 indirizzi distinti**. Al primo giro (16:44, sull'unione dei soli quattro elenchi) 282 erano in questo file e 11 no; due erano fonti senza voce in tutti e quattro gli elenchi, e le ho aggiunte: un rapporto della NASA citato in `f9-preproposta/03-kalman/CONSEGNA.md` (`thipphavong2016`) e un deposito di codice citato in `f10-dati/04-embedded/INVENTARIO_E_DECISIONE.md` (`ldrobot-ldlidar-stl-sdk`). Dopo l'aggiunta: **284 presenti, 9 assenti, nessuno dei 9 è una fonte senza voce**: cinque sono indirizzi di scaricamento diretto di insiemi di dati che hanno la loro voce (`bonn-rgbd-dynamic`, `princeton-tracking-benchmark`, `thor` due volte, `depthtrack`); uno è il vecchio nome del deposito di `drow`; uno è la cartella `doc` del deposito di `librealsense`; due non sono fonti (uno spazio dei nomi tecnico nella bozza e la filigrana dello strumento che l'ha esportata). Stato: **verificato** sull'insieme dichiarato (gli indirizzi scritti in quei file a quell'ora), non oltre. Che cosa il controllo non vede: (a) i riferimenti citati a parole, senza indirizzo (per quelli vale la lettura dei quattro curatori, che due di loro dichiarano parziale); (b) ciò che i ruoli di f7–f10 scrivono dopo le 16:48; (c) i file che non sono `.md`. Su questi ultimi ho fatto un secondo giro (programmi, elenchi e file di dati: 43 indirizzi distinti, 23 presenti): i 20 assenti sono indirizzi di scaricamento di insiemi che hanno già una voce, indirizzi d'esempio dei programmi di prova, e **un insieme di dati che non ha una voce**, THÖR-MAGNI (Zenodo, record 7974709), nominato solo in un file di elenco di `f10-dati/01-ricercatore/elenchi/`: va aggiunto se qualcuno lo usa. Il controllo condivide con l'unione il programma che estrae gli indirizzi, ma non i quattro elenchi: per questo ha trovato ciò che a tutti e quattro era sfuggito.

---

## 1. Articoli scientifici e prestampe (con tesi, libri e rapporti)

115 voci, da [1] a [115].

### adamides2025 [1]
Tipo: articolo scientifico (rassegna)
Autori: Odysseus Adamides, Karthik Subramanian, Sarthak Arora, Ferat Sahin
Titolo: Perception and Computation for Speed and Separation Monitoring Architectures
Sede e anno: Robotics (MDPI), vol. 14(4), articolo 41, 2025 (31-3-2025)
Identificativo: DOI 10.3390/robotics14040041
Link: https://mdpi.com/2218-6581/14/4/41
Verifica: verificata dal curatore il 14-11-2026 in parte — (rif-1) solo nei dati bibliografici [g] (Crossref e Semantic Scholar): esiste con questi autori e questo titolo. L'affermazione citata non è nel riassunto; il testo intero non è raggiungibile (403): affermazione non verificata.
Usata per: F26: nella sorveglianza di velocità e separazione (ISO/TS 15066) la distanza protettiva si calcola con l'incertezza di misura e la latenza — `f1/3fff79e9c3ea/FONTI.md`, `f1/3fff79e9c3ea/CONSEGNA.md` (§1.8)
Note: il riassunto parla di architetture di percezione per la sorveglianza di velocità e separazione, non della formula. Che la formula della norma contenga termini di incertezza di posizione e di tempo di reazione lo ricordo a memoria: non verificato oggi.

### aharon2022 [2]
Tipo: articolo scientifico (prestampa)
Autori: Nir Aharon, Roy Orfaig, Ben-Zion Bobrovsky
Titolo: BoT-SORT: Robust Associations Multi-Pedestrian Tracking
Sede e anno: prestampa arXiv, v1 del 29 giugno 2022, v2 del 7 luglio 2022; la pagina non indica una sede pubblicata
Identificativo: arXiv:2206.14651; DOI 10.48550/arXiv.2206.14651
Link: https://arxiv.org/abs/2206.14651
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-2) per i soli dati bibliografici (pagina arXiv). Testo non letto. ‖ (rif-3) [r] — nel riassunto: «camera-motion compensation, and a more accurate Kalman filter state vector». Il ruolo che la cita l'aveva aperta.
Usata per: tracciatore «BoT-SORT o ByteTrack» — `f2/01-traduzione/SCHEDE.md` (`visione-1`).
Usata per: compensazione del moto della camera nel filtro di tracciamento — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §3, S35
Note: (rif-2) solo nominato nei file. (rif-3) la compensazione è nel piano dell'immagine e si misura sull'identità dei pedoni; non dà garanzie su «mai libero dove non è osservato».

### ahn2019 [3]
Tipo: articolo scientifico
Autori: Min Sung Ahn; Hosik Chae; Donghun Noh; Hyunwoo Nam; Dennis Hong (nomi per esteso: non verificati; Crossref dà Ahn M, Chae H, Noh D, Nam H, Hong D)
Titolo: Analysis and Noise Modeling of the Intel RealSense D435 for Mobile Robots
Sede e anno: 16th International Conference on Ubiquitous Robots (UR), 2019, pp. 707–711
Identificativo: DOI 10.1109/URAI.2019.8768489
Link: https://ucla.box.com/shared/static/gqxwr2vvqsf22oi9dqtn50hr0xkruzie.pdf
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-4) [API] e [T]: nel PDF σz(z, θ) = 0,001063 + 0,0007278·z + 0,003949·z² + 0,022·z^(3/2)·θ/(π/2 − θ)²; «the left edge of the planar target noticeably worsens»; la soglia dei 60° e 75° non ricontrollata
Usata per: rumore assiale misurato della D435 (σz = 0,0011 + 0,0007·z + 0,0039·z², 1,83 cm a 2 m), ombra sul bordo sinistro, rumore piatto fino a 60° d'incidenza — `f10-dati/02-sensori/MODELLO_SENSORE.md` righe 18 e 90 (S3), `PREVISIONI.md` righe 31 e 35 **[f7–f10: non vagliato dall'arbitro]**
Note: parete bianca, 0,4–2,1 m: a 3 m è un'estrapolazione (lo dice il ruolo). Copia messa in rete dagli autori; diritti IEEE. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### angelopoulos2021 [4]
Tipo: articolo scientifico (prestampa, guida)
Autori: Anastasios N. Angelopoulos; Stephen Bates
Titolo: A Gentle Introduction to Conformal Prediction and Distribution-Free Uncertainty Quantification
Sede e anno: arXiv, v6 7-12-2022; versione a stampa: non verificata
Identificativo: arXiv:2107.07511
Link: https://arxiv.org/abs/2107.07511
Verifica: verificata dal curatore il 14-11-2026 in parte — (rif-4) [API] per autori e titolo; la condizione di scambiabilità non è nel riassunto: non riletta (lo dichiara anche il ruolo)
Usata per: la copertura marginale promessa dalla teoria, a fronte di 0,893–0,905 misurato nel complesso (`risultati` del ruolo) — `f8-continuita/03-kalman/CONSEGNA.md` riga 30; `f8-continuita/04-statistico/CONSEGNA.md` riga 88 **[f7–f10: non vagliato dall'arbitro]**
Note: garantisce la copertura in media, non per comportamento. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### balch2019 [5]
Tipo: articolo scientifico
Autori: Michael S. Balch; Ryan Martin; Scott Ferson
Titolo: Satellite conjunction analysis and the false confidence theorem
Sede e anno: Proceedings of the Royal Society A 475(2227):20180565, 2019
Identificativo: DOI 10.1098/rspa.2018.0565; arXiv:1706.08565
Link: https://arxiv.org/abs/1706.08565
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-4) [API]: «lower quality data paradoxically appear to reduce the risk of collision» presente nel riassunto; «gli ellissoidi d'incertezza ne sono immuni» non ricontrollato
Usata per: la diluizione della probabilità: un dato più rumoroso abbassa la probabilità d'intrusione (conto del ruolo: da 0,75 a 0,45 a 1 s) — `f9-preproposta/06-esperto-dominio/CONSEGNA.md` riga 31 (F4) **[f7–f10: non vagliato dall'arbitro]**
Note: congiunzioni fra satelliti: passa il principio, non i numeri. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### barber2019 [6]
Tipo: articolo scientifico (prestampa)
Autori: Rina Foygel Barber; Emmanuel J. Candès; Aaditya Ramdas; Ryan J. Tibshirani
Titolo: The limits of distribution-free conditional predictive inference
Sede e anno: arXiv, v2 15-4-2020; versione a stampa: non verificata
Identificativo: arXiv:1903.04684
Link: https://arxiv.org/abs/1903.04684
Verifica: verificata dal curatore il 14-11-2026 in parte — (rif-4) [API] per autori e titolo; il ruolo ha letto solo il riassunto
Usata per: la copertura condizionata esatta è impossibile senza ipotesi («Barber e altri») — `f8-continuita/04-statistico/CONSEGNA.md` righe 43 e 88 **[f7–f10: non vagliato dall'arbitro]**
Note: l'enunciato preciso del teorema non è stato riletto da nessuno. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### becker2018 [7]
Tipo: articolo scientifico
Autori: Stefan Becker, Ronny Hug, Wolfgang Hübner, Michael Arens
Titolo: RED: A Simple but Effective Baseline Predictor for the TrajNet Benchmark (su arXiv con il titolo «An Evaluation of Trajectory Prediction Approaches and Notes on the TrajNet Benchmark»)
Sede e anno: Computer Vision – ECCV 2018 Workshops, Lecture Notes in Computer Science, Springer, pp. 138–153 (atti usciti nel 2019)
Identificativo: DOI 10.1007/978-3-030-11015-4_13; arXiv:1805.07663
Link: https://arxiv.org/abs/1805.07663
Verifica: verificata dal curatore il 14-11-2026 in parte — (rif-2) per i soli dati bibliografici (pagina arXiv, registro Crossref, e voce [14] nell'elenco dei riferimenti di `scholler2020`). Il testo non l'ho letto.
Usata per: «RED 0,44 / 0,91» come miglior predittore appreso deterministico — `f2/05-selezione/SELEZIONE.md` (riga H-011); `f3/H-012/01-scene-dinamiche/SOLUZIONE.md` §8.
Note: nei file dello sciame è solo nominato («RED»), senza riferimento. La cifra 0,44 / 0,91 non è di questo articolo: è la riesecuzione di Schöller e altri.

### bewley2016 [8]
Tipo: articolo scientifico
Autori: Alex Bewley, Zongyuan Ge, Lionel Ott, Fabio Ramos, Ben Upcroft
Titolo: Simple Online and Realtime Tracking
Sede e anno: IEEE International Conference on Image Processing (ICIP) 2016; pagine: manca (non controllate)
Identificativo: DOI 10.1109/ICIP.2016.7533003; arXiv 1602.00763
Link: https://arxiv.org/abs/1602.00763
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-1) già verificata dal curatore in f3 [g]: «updates at a rate of 260 Hz». Ricontrollati oggi su arXiv [g]: autori, DOI, «Presented at ICIP 2016», e nel riassunto Kalman più algoritmo ungherese e i 260 Hz. ‖ (rif-2) Pagina arXiv (autori, titolo, «Presented at ICIP 2016», DOI). Nel riassunto: «the tracker updates at a rate of 260 Hz». Già in f3/fonti.
Usata per: ordine «rilevatore → Kalman e ungherese» e 260 Hz (SORT) — `f1/21d3813ca7e1/CONSEGNA.md` (§1.1)
Usata per: «calcolo trascurabile (SORT, stessa famiglia: 260 Hz)» — `f3/H-012/01-scene-dinamiche/SOLUZIONE.md` (B4).
Usata per: associazione «alla SORT» come schema — `f3/H-012/01-scene-dinamiche/SOLUZIONE.md` §8; `f4/H-012/05-correzioni/SOLUZIONE_V2.md` §8.
Note: (rif-1) i 260 Hz sono del solo tracciatore, date le rilevazioni, sull'hardware del 2016. (rif-2) i 260 Hz sono del solo tracciatore (Kalman più ungherese) su riquadri 2D già rilevati, sull'hardware degli autori: non sono una misura del blocco B4 dello sciame.

### bogoslavskyi2016 [9]
Tipo: articolo scientifico e deposito di codice
Autori: Igor Bogoslavskyi, Cyrill Stachniss
Titolo: Fast range image-based segmentation of sparse 3D laser scans for online operation
Sede e anno: IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS) 2016, pp. 163–169
Identificativo: DOI 10.1109/IROS.2016.7759050
Link: https://github.com/PRBonn/depth_clustering
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-1) deposito aperto [r]: «Fast and robust clustering of point clouds generated with a Velodyne sensor», licenza MIT, articolo da citare; pagine e DOI su Crossref [g].
Usata per: raggruppamento per componenti connesse sulle celle occupate, «stesso principio» di un metodo nato per LiDAR rotanti (trasferimento alle camere di profondità non verificato) — `f1/dfac83300259/CONSEGNA.md` (§4.3)
Note: il README cita anche un secondo articolo degli stessi autori (PFG, 2017), non citato dallo sciame. Il principio (immagine di distanza) si deduce dal titolo: il metodo non è stato letto.

### boukhelifa2012 [10]
Tipo: articolo scientifico
Autori: Nadia Boukhelifa; Anastasia Bezerianos; Tobias Isenberg; Jean-Daniel Fekete
Titolo: Evaluating Sketchiness as a Visual Variable for the Depiction of Qualitative Uncertainty
Sede e anno: IEEE Transactions on Visualization and Computer Graphics 18(12):2769–2778, 2012
Identificativo: DOI 10.1109/TVCG.2012.220
Link: https://tobias.isenberg.cc/p/Boukhelifa2012ESV
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-4) [API] e [T]: «people subjectively prefer dashing style over blur, grayscale and sketchiness» presente nel riassunto sulla pagina dell'autore
Usata per: il tratteggio è preferito a sfocatura e grigio — `f8-continuita/06-visualizzatore/CONSEGNA.md` riga 45 **[f7–f10: non vagliato dall'arbitro]**
Note: preferenza soggettiva, su linee. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### cao2023 [11]
Tipo: articolo scientifico e deposito di codice
Autori: Jinkun Cao, Jiangmiao Pang, Xinshuo Weng, Rawal Khirodkar, Kris Kitani
Titolo: Observation-Centric SORT: Rethinking SORT for Robust Multi-Object Tracking
Sede e anno: IEEE/CVF CVPR 2023, pp. 9686–9696
Identificativo: DOI 10.1109/CVPR52729.2023.00934; arXiv 2203.14360
Link: https://arxiv.org/abs/2203.14360 ; https://github.com/noahcao/OC_SORT
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-1) già verificata dal curatore in f3 [g]: errore che si accumula in occlusione, modulo ORU, «700+ FPS on a single CPU», deposito MIT. Ricontrollati oggi: autori e frase «This leads to the accumulation of errors during a period of occlusion» (arXiv [g]); pagine e DOI (Crossref [g]); file LICENSE del deposito «MIT License» [g]. ‖ (rif-2) Pagina arXiv (autori, titolo, «Accepted by CVPR 2023») e registro Crossref (pagine, DOI). Nel riassunto: «This leads to the accumulation of errors during a period of occlusion»; «OC-SORT runs at 700+ FPS on a single CPU». Già in f3/fonti. ‖ (rif-4) [API]: dati bibliografici; «700+ FPS on a single CPU» nel riassunto; già verificata dal curatore in f3 (F16); il passo di recupero (OCR) è citato dal ruolo a memoria: non verificato
Usata per: F16: errore del Kalman che si accumula in occlusione; ORU; oltre 700 FPS su CPU date le rilevazioni; MIT — `f1/3fff79e9c3ea/FONTI.md`, `f1/3fff79e9c3ea/CONSEGNA.md` (§1.4)
Usata per: «senza misure gli errori del Kalman si accumulano» — `f1/21d3813ca7e1/CONSEGNA.md` (§1.4); «OC-SORT nasce dall'errore che il Kalman accumula in occlusione» — `f1/992c41c8860e/CONSEGNA.md` (§1.3)
Usata per: l'articolo descrive il rumore che il Kalman accumula in occlusione; associazione «alla SORT / OC-SORT» come schema — `f3/H-012/01-scene-dinamiche/SOLUZIONE.md` §8; `f4/H-012/05-correzioni/SOLUZIONE_V2.md` §8.
Usata per: associazione «tipo ByteTrack/OC-SORT» — `f2/01-traduzione/SCHEDE.md` (`ricercatore-1`).
Usata per: riassociazione «alla OC-SORT» alla ricomparsa; braccio `cor3` (recupero sull'ultima osservazione) — `f9-preproposta/05-tracciamento/CONSEGNA.md` riga 3, `PREVISIONI.md` riga 64; nominata in `prepropostaEsterna.md` riga 91 **[f7–f10: non vagliato dall'arbitro]**
Note: (rif-1) il file LICENSE porta «Copyright (c) 2021 Yifu Zhang» (ereditato da ByteTrack): è MIT in ogni caso. (rif-2) il deposito `noahcao/OC_SORT` è sotto licenza MIT (file LICENSE aperto oggi). L'articolo misura la velocità con rilevamenti già dati: i 700 fps non comprendono il rilevatore. Non garantisce niente sui pedoni dietro un pannello con un sensore di profondità. (rif-4) nel piano immagine; il ruolo la porta sul piano del suolo. Alcuni usi vengono dalle estensioni f7–f10: NON ancora vagliati dall'arbitro (marcati riga per riga).

### carion2025 [12]
Tipo: articolo scientifico (prestampa)
Autori: Nicolas Carion, Laura Gustafson, Yuan-Ting Hu, Shoubhik Debnath, Ronghang Hu, Didac Suris, Chaitanya Ryali, Kalyan Vasudev Alwala, Haitham Khedr, Andrew Huang, Jie Lei, Tengyu Ma, Baishan Guo, Arpit Kalla, Markus Marks, Joseph Greer, Meng Wang, Peize Sun, Roman Rädle, Triantafyllos Afouras, Effrosyni Mavroudi, Katherine Xu, Tsung-Han Wu, Yu Zhou, Liliane Momeni, Rishi Hazra, Shuangrui Ding, Sagar Vaze, Francois Porcher, Feng Li, Siyuan Li, Aishwarya Kamath, Ho Kei Cheng, Piotr Dollár, Nikhila Ravi, Kate Saenko, Pengchuan Zhang, Christoph Feichtenhofer
Titolo: SAM 3: Segment Anything with Concepts
Sede e anno: arXiv, v1 20-11-2025, v2 28-03-2026; sede a stampa: manca (non controllata)
Identificativo: arXiv:2511.16719
Link: https://arxiv.org/abs/2511.16719 ; anche (rif-1): https://arxiv.org/html/2511.16719v2
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-1) già verificata dal curatore in f3 [g, testo intero]: «30 ms for a single image with 100+ detected objects» su H200; circa 5 oggetti quasi in tempo reale. Ricontrollati oggi su arXiv [g] titolo, numero di autori e date. ‖ (rif-2) Pagina arXiv (38 autori, titolo). La cifra non è nel riassunto arXiv; oggi l'ho trovata nella pagina di Meta (`meta-sam31`): «SAM 3 runs in 30 milliseconds for a single image with more than 100 detected objects on an H200 GPU… near real-time performance for approximately five concurrent objects». Nel testo intero dell'articolo l'ha trovata il curatore in f3; oggi non l'ho riaperto.
Usata per: «SAM 3 30 ms a immagine su H200, video quasi in tempo reale per circa 5 oggetti» — `f1/c85dbcc51ea6/CONSEGNA.md` (§1.2, rif. [4])
Usata per: SAM 3 fuori dall'ipotesi portatile o Jetson (dal riassunto di ricerca) — `f1/992c41c8860e/CONSEGNA.md` (§1.4)
Usata per: «SAM 3 dà 30 ms a immagine su una H200»: resta fuori dalla catena — `f3/H-012/01-scene-dinamiche/SOLUZIONE.md` §8; `f4/H-012/05-correzioni/SOLUZIONE_V2.md` §8.
Note: (rif-1) i dati non sono nel riassunto dell'articolo ma nel testo. GPU da centro di calcolo. (rif-2) H200 è una GPU da centro di calcolo; la fonte non dà tempi su CPU o su schede piccole. Differenza fra i gruppi: rif-1 elencava 12 autori «e altri 26»; l'elenco completo dei 38 è di rif-2.

### chen2024 [13]
Tipo: articolo scientifico
Autori: Kaihua Chen, Deva Ramanan, Tarasha Khurana
Titolo: Using Diffusion Priors for Video Amodal Segmentation
Sede e anno: IEEE/CVF CVPR 2025, pp. 22890–22900 (prestampa arXiv del 5-12-2024)
Identificativo: DOI 10.1109/CVPR52734.2025.02131; arXiv 2412.04623
Link: https://arxiv.org/abs/2412.04623
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-1) [g]: registro arXiv e Crossref aperti; nel riassunto: la segmentazione amodale su video è formulata «as a conditional generation task», sfruttando modelli generativi di video.
Usata per: «lo stato dell'arte amodale su video è generativo (diffusione [12])» — `f1/c85dbcc51ea6/CONSEGNA.md` (§1.6)
Note: `visione` dà solo il link; autori, titolo e sede li ho aggiunti oggi. Che sia «lo stato dell'arte» è un giudizio del ruolo, non verificato; tempi di esecuzione: non verificati.

### cheraghipouria2026 [14]
Tipo: articolo scientifico (prestampa)
Autori: Fatemeh Cheraghi Pouria; Mahsa Golchoubian; Katherine Driggs-Campbell
Titolo: Rethinking Gaussian Trajectory Predictors: Calibrated Uncertainty for Safe Planning
Sede e anno: arXiv, v1 11-3-2026, v2 12-7-2026; sede di pubblicazione: manca
Identificativo: arXiv:2603.10407
Link: https://arxiv.org/abs/2603.10407
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-4) [API]: frase «…Negative Log-Likelihood loss, which is prone to predict over- or under-confident distributions» presente nel riassunto
Usata per: la perdita NLL dà distribuzioni troppo o troppo poco sicure — `f8-continuita/07-ricercatore/FONTI.md` (S2), `CONSEGNA.md` riga 41 **[f7–f10: non vagliato dall'arbitro]**
Note: correzione C4 (cognome del primo autore). Nessun numero citato. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### cleaveland2024 [15]
Tipo: articolo scientifico
Autori: Matthew Cleaveland; Insup Lee; George J. Pappas; Lars Lindemann
Titolo: Conformal Prediction Regions for Time Series Using Linear Complementarity Programming
Sede e anno: Proceedings of the AAAI Conference on Artificial Intelligence 38(19):20984–20992, 2024
Identificativo: DOI 10.1609/aaai.v38i19.30089; arXiv:2304.01075
Link: https://arxiv.org/abs/2304.01075
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-4) [API]: «prediction regions that are not conservative» e i predittori di pedoni presenti nel riassunto; sede AAAI 2024 confermata (era R)
Usata per: regioni conformi su più passi non prudenti — `f8-continuita/07-ricercatore/FONTI.md` (S5), `CONSEGNA.md` riga 80 **[f7–f10: non vagliato dall'arbitro]**
Note: nessun numero citato. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### clopper1934 [16]
Tipo: articolo scientifico (metodo statistico)
Autori: C. J. Clopper, E. S. Pearson (cognomi dal registro; iniziali a memoria, non verificate)
Titolo: The Use of Confidence or Fiducial Limits Illustrated in the Case of the Binomial
Sede e anno: Biometrika, vol. 26, n. 4, pp. 404–413, 1934
Identificativo: DOI 10.1093/biomet/26.4.404
Link: https://doi.org/10.1093/biomet/26.4.404
Verifica: verificata dal curatore il 14-11-2026 in parte — (rif-2) per i soli dati bibliografici (registro Crossref). Testo non letto.
Usata per: «Limiti di Clopper-Pearson unilaterali al 95 %» come regola di decisione delle prove (300 passaggi per la soglia del 99 %, 2000 per l'85 %) — `f3/H-012/03-metrologo/PIANO_MISURE.md` (parte 1); «binomiale esatta» — `f3/H-012/02-validazione/VERIFICA.md` (§3b); «limite inferiore 99,25 %» con N = 400 — `f4/H-012/05-correzioni/SOLUZIONE_V2.md` (§1).
Note: il metodo è nominato nei file senza riferimento: la voce è aggiunta da me. Due conti ricontrollati oggi: 0,95^59 = 0,0485 e 0,99^299 = 0,0495 (tornano con «59» e «299» del piano).

### dang2024 [17]
Tipo: articolo scientifico
Autori: Zhaoyang Dang, Xiaoyong Sun, Bei Sun, Runze Guo, Can Li
Titolo: OMCTrack: Integrating Occlusion Perception and Motion Compensation for UAV Multi-Object Tracking
Sede e anno: Drones 8(9), articolo 480, 12 settembre 2024 (MDPI)
Identificativo: DOI 10.3390/drones8090480
Link: https://mdpi.com/2504-446X/8/9/480
Verifica: verificata dal curatore il 14-11-2026 in parte — (rif-3) in parte: la pagina dell'editore non è raggiungibile (403, come già al ruolo che la cita); autori, titolo, rivista e riassunto letti nel registro Crossref [m]. Nel riassunto: «occlusion perception module» e «adaptive motion compensation module … to handle the UAV's complex movements». Il testo intero non è stato letto.
Usata per: i lavori sul tracciamento da drone nominano insieme occlusione e moto irregolare della camera — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §2(d), S22
Usata per: tracciatori per drone, fra i riferimenti di ricerca — stesso file, §3
Note: è questa, non `liu2022`, la fonte che regge la frase su occlusione e moto insieme. Misurato su VisDrone2019 e UAVDT, nel piano dell'immagine.

### delmerico2018 [18]
Tipo: articolo scientifico
Autori: Jeffrey Delmerico, Davide Scaramuzza
Titolo: A Benchmark Comparison of Monocular Visual-Inertial Odometry Algorithms for Flying Robots
Sede e anno: 2018 IEEE International Conference on Robotics and Automation (ICRA), pp. 2502–2509, maggio 2018
Identificativo: DOI 10.1109/ICRA.2018.8460664
Link: https://rpg.ifi.uzh.ch/docs/ICRA18_Delmerico.pdf
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-3) [g sul testo estratto dal PDF per titolo, autori e riassunto; m per sede, pagine e DOI]. I due ruoli che la citano non erano riusciti a leggerla.
Usata per: «confronto di riferimento» sulla qualità del moto proprio, citato come non letto; nessuna cifra presa — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §2(a), S13
Usata per: lo stesso, «non si è lasciato leggere»; le cifre d'errore delle sorgenti restano ipotesi — `f6-specializzazione/02-slam/MOTO_PROPRIO.md` §2
Note: confronta sei catene di odometria visuale-inerziale monoculare (MSCKF, OKVIS, ROVIO, VINS-Mono, SVO+MSF, SVO+GTSAM) su calcolatori di bordo. Non contiene gli errori relativi su 1–2 s che servirebbero al bilancio della posa: le cifre di `MOTO_PROPRIO.md` restano ipotesi del ruolo.

### ding2026 [19]
Tipo: articolo scientifico (prestampa)
Autori: Zhaoyuan Ding, Yijing Yang, Han Shu, Xinghao Chen
Titolo: TinySAM 2: Extreme Memory Compression for Efficient Track Anything Model
Sede e anno: arXiv, 18-5-2026 (12 pagine, 6 figure); sede a stampa: manca
Identificativo: arXiv 2605.18013
Link: https://arxiv.org/abs/2605.18013 ; https://arxiv.org/html/2605.18013
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-1) titolo e autori [g, arXiv]; testo HTML aperto [r]: «can run in real-time at 25.6 FPS on a single GPU for 1000 image frames from three videos» (§ 4.2); «FPS is measured on a single GPU with 32GB memory» (§ 4.1); in Tabella 1 il valore sta sotto «FPS V100».
Usata per: F21: «TinySAM 2: 25,6 FPS, hardware non identificato» — `f1/3fff79e9c3ea/FONTI.md`
Note: il numero è giusto e l'articolo è questo (dubbio di FONTI.md chiuso); l'hardware è una GPU da centro di calcolo (V100 secondo l'intestazione della tabella), quindi non sposta P2(b). Prestampa.

### dixit2022 [20]
Tipo: articolo scientifico (prestampa)
Autori: Anushri Dixit; Lars Lindemann; Skylar Wei; Matthew Cleaveland; George J. Pappas; Joel W. Burdick
Titolo: Adaptive Conformal Prediction for Motion Planning among Dynamic Agents
Sede e anno: arXiv, 1-12-2022; «L4DC 2023» secondo il ruolo: non verificata (non è in Crossref)
Identificativo: arXiv:2212.00278
Link: https://arxiv.org/abs/2212.00278
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-4) [API]: «distribution-free», osservazioni ritardate («delayed agent observations»), drone e frisbee presenti nel riassunto; sede non verificata
Usata per: la variante adattiva usa le osservazioni ritardate degli agenti — `f8-continuita/07-ricercatore/FONTI.md` (S6), `CONSEGNA.md` riga 46 **[f7–f10: non vagliato dall'arbitro]**
Note: «in simulazione» non ricontrollato. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### doersch2022 [21]
Tipo: articolo scientifico
Autori: Carl Doersch; Ankush Gupta; Larisa Markeeva; Adrià Recasens; Lucas Smaira; Yusuf Aytar; João Carreira; Andrew Zisserman; Yi Yang
Titolo: TAP-Vid: A Benchmark for Tracking Any Point in a Video
Sede e anno: NeurIPS 2022, Datasets and Benchmarks track (dal commento arXiv)
Identificativo: arXiv:2211.03726
Link: https://arxiv.org/html/2211.03726v2
Verifica: verificata dal curatore il 14-11-2026 in parte — (rif-4) [API]: primo autore e sede confermati (nel file erano «a memoria»); le due frasi citate sono nel corpo: aperte dal ruolo che la cita (A), non rilette da me
Usata per: la precisione di posizione vale «only for frames where the point is visible»; in occlusione la posizione «is typically assumed to be meaningless» — `f8-continuita/07-ricercatore/FONTI.md` (S15), `CONSEGNA.md` righe 61, 65 **[f7–f10: non vagliato dall'arbitro]**
Note: Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### dossantos2025 [22]
Tipo: articolo scientifico
Autori: A. D. P. Dos Santos, M. Loureiro, F. Machado, A. Frizera, F. O. Medola (forma di PubMed: «Dos Santos ADP, Loureiro M, Machado F, Frizera A, Medola FO»)
Titolo: NavWear: design and evaluation of a wearable device for obstacle detection for blind and visually impaired people
Sede e anno: Disability and Rehabilitation: Assistive Technology, vol. 20(6), pp. 1800–1814, agosto 2025 (in linea 18-3-2025)
Identificativo: DOI 10.1080/17483107.2025.2477681; PMID 40100749
Link: https://pubmed.ncbi.nlm.nih.gov/40100749/
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-1) [g]: registro PubMed aperto (servizio E-utilities); nel riassunto «The system is based on an RGB-D camera and haptic feedback, integrated into a backpack»; «Ten blindfolded participants». ‖ (rif-4) [API PubMed] per i dati bibliografici; contenuto non letto
Usata per: F13: NavWear 2025 (RGB-D + aptico, zaino), citato dalla bozza — `f1/3fff79e9c3ea/FONTI.md`
Usata per: esempio di ausilio indossabile con RGB-D e riscontro aptico, per impostare la valutazione con gli utenti — `bozza_iniziale/Proposta MLE Matrice Bayesiana (1).md` riga 2934 **[file esterno alla convocazione]**
Note: (rif-1) i nomi propri per esteso degli autori non sono nel registro letto (solo iniziali): manca. La prova è con dieci partecipanti bendati, non con persone con disabilità visiva. (rif-4) la bozza non ne trae cifre. Alcuni usi vengono dalle estensioni f7–f10: NON ancora vagliati dall'arbitro (marcati riga per riga).

### duberg2020 [23]
Tipo: articolo scientifico
Autori: Daniel Duberg; Patric Jensfelt
Titolo: UFOMap: An Efficient Probabilistic 3D Mapping Framework That Embraces the Unknown
Sede e anno: IEEE Robotics and Automation Letters 5(4):6411–6418, 2020
Identificativo: DOI 10.1109/LRA.2020.3013861; arXiv:2003.04749
Link: https://arxiv.org/abs/2003.04749
Verifica: dato diverso — (rif-4) [API]: «explicit representation of all three states in the map, i.e., occupied, free, and unknown» presente nel riassunto; «real-time (2 Hz) at 2 mm» NON è nell'articolo ma nel README del deposito (correzione C2)
Usata per: UFOMap dichiara lo sconosciuto in modo esplicito; «real-time (2 Hz) at 2 mm» — `f7-estensione/05-esperto-dominio/CONSEGNA.md` righe 26 e 80 (S3) **[f7–f10: non vagliato dall'arbitro]**
Note: vedi `ufomap-deposito`. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### gibbs2021 [24]
Tipo: articolo scientifico (prestampa)
Autori: Isaac Gibbs; Emmanuel Candès
Titolo: Adaptive Conformal Inference Under Distribution Shift
Sede e anno: arXiv, v3 28-10-2021; versione a stampa: non verificata
Identificativo: arXiv:2106.00170
Link: https://arxiv.org/abs/2106.00170
Verifica: verificata dal curatore il 14-11-2026 in parte — (rif-4) [API] per autori e titolo; il ruolo ha letto solo il riassunto
Usata per: conforme adattiva sotto cambio di distribuzione — `f8-continuita/04-statistico/CONSEGNA.md` riga 88 **[f7–f10: non vagliato dall'arbitro]**
Note: Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### giudice2008 [25]
Tipo: articolo scientifico (atti di conferenza)
Autori: Nicholas A. Giudice, James R. Marston, Roberta L. Klatzky, Jack M. Loomis, Reginald G. Golledge
Titolo: Environmental learning without vision: Effects of cognitive load on interface design
Sede e anno: Proceedings of the 9th International Conference on Low Vision (Vision 2008), Montréal, 2008; pagine: manca
Identificativo: manca
Link: https://umaine.edu/vemi/publication/environmental-learning-without-vision-effects-cognitive-load-interface-design
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-1) [r]: pagina aperta; nel riassunto «the secondary task had no effect on cognitive map performance for guidance by spatialized audio» ma «led to significantly worse homing errors for guidance by spatial language»; «Blindfolded participants».
Usata per: F11: la guida con suono spazializzato regge un compito secondario meglio del linguaggio spaziale (vedenti bendati) — `f1/3fff79e9c3ea/FONTI.md`
Note: il riassunto dice «blindfolded», non dice che fossero vedenti: «vedenti bendati» è non verificato su questa fonte. Pagina dell'istituto dell'autore, non degli atti.

### gneiting2007 [26]
Tipo: articolo scientifico
Autori: Tilmann Gneiting; Adrian E. Raftery
Titolo: Strictly Proper Scoring Rules, Prediction, and Estimation
Sede e anno: Journal of the American Statistical Association 102(477):359–378, 2007
Identificativo: DOI 10.1198/016214506000001437
Link: https://sites.stat.washington.edu/raftery/Research/PDF/Gneiting2007jasa.pdf
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-4) [API] e [T]: PDF aperto, «energy score» e «interval score» presenti; i numeri delle equazioni (21, 22, 43) non ricontrollati: letti dal ruolo
Usata per: punteggi propri (CRPS, punteggio d'energia, punteggio dell'intervallo) per valutare le previsioni — `f8-continuita/04-statistico/CONSEGNA.md` riga 88 **[f7–f10: non vagliato dall'arbitro]**
Note: Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### guibas1997 [27]
Tipo: articolo scientifico
Autori: Leonidas J. Guibas; Jean-Claude Latombe; Steven M. LaValle; David Lin; Rajeev Motwani
Titolo: Visibility-Based Pursuit-Evasion in a Polygonal Environment
Sede e anno: Lecture Notes in Computer Science (Springer), 1997, pp. 17–30 (convegno e volume: non letti); versione estesa su International Journal of Computational Geometry & Applications 9(4–5):471–493, 1999
Identificativo: DOI 10.1007/3-540-63307-3_45 (1997); DOI 10.1142/S0218195999000273 (1999)
Link: https://cw.fel.cvut.cz/b191/_media/courses/b4m36uir/lectures/guibas1997.pdf
Verifica: verificata dal curatore il 14-11-2026 in parte — (rif-4) [API] e [T]: PDF aperto, titolo e autori presenti; il passo usato non riletto
Usata per: la regione di «possibile presenza» come nell'inseguimento con visibilità — `f7-estensione/08-creativo/CONSEGNA.md` riga 53 **[f7–f10: non vagliato dall'arbitro]**
Note: il link è una copia su un sito didattico, non l'editore. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### gupta2018 [28]
Tipo: articolo scientifico
Autori: Agrim Gupta, Justin Johnson, Li Fei-Fei, Silvio Savarese, Alexandre Alahi
Titolo: Social GAN: Socially Acceptable Trajectories with Generative Adversarial Networks
Sede e anno: IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR) 2018, pp. 2255–2264
Identificativo: DOI 10.1109/CVPR.2018.00240; arXiv:1803.10892
Link: https://arxiv.org/abs/1803.10892
Verifica: verificata dal curatore il 14-11-2026 in parte — (rif-2) per i soli dati bibliografici (pagina arXiv, registro Crossref, voce [3] di `scholler2020`). Il testo non l'ho letto.
Usata per: «il generativo S-GAN sta a 0,32 / 0,60» — `f2/01-traduzione/SCHEDE.md` (`ricercatore-2`); `f2/05-selezione/SELEZIONE.md` (riga H-011); `f3/H-012/01-scene-dinamiche/SOLUZIONE.md` §8.
Note: solo nominato nei file. Lo 0,32 / 0,60 viene da un modello preaddestrato rieseguito da Schöller e altri («an improved version compared to what the authors report in their paper»), migliore di 20 campioni.

### haghighi2024 [29]
Tipo: articolo scientifico (prestampa)
Autori: Yasaman Haghighi; Celine Demonsant; Panagiotis Chalimourdas; Maryam Tavasoli Naeini; Jhon Kevin Munoz; Bladimir Bacca; Silvan Suter; Matthieu Gani; Alexandre Alahi
Titolo: HEADS-UP: Head-Mounted Egocentric Dataset for Trajectory Prediction in Blind Assistance Systems
Sede e anno: arXiv, 30-9-2024; sede: manca
Identificativo: arXiv:2409.20324
Link: https://arxiv.org/html/2409.20324v1
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-4) [API]: «Jetson» e ausilio per non vedenti presenti nel riassunto
Usata per: insieme egocentrico per la previsione di pedoni in un ausilio; nessun numero sugli utenti — `f8-continuita/07-ricercatore/FONTI.md` (S21), `CONSEGNA.md` riga 74 **[f7–f10: non vagliato dall'arbitro]**
Note: l'assenza di numeri sugli utenti è un'assenza su ciò che il ruolo ha letto. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### hetzel2024 [30]
Tipo: articolo scientifico
Autori: Manuel Hetzel; Hannes Reichert; Konrad Doll; Bernhard Sick
Titolo: Reliable Probabilistic Human Trajectory Prediction for Autonomous Applications
Sede e anno: prestampa arXiv, v2 del 10-10-2024; Crossref: capitolo in Lecture Notes in Computer Science (Springer), 2025, pp. 135–152 (convegno: non verificato)
Identificativo: arXiv:2410.06905; DOI 10.1007/978-3-031-91585-7_9
Link: https://arxiv.org/html/2410.06905v2
Verifica: verificata dal curatore il 14-11-2026 in parte — (rif-4) [API] per autori, titolo, date e sede; le cifre e la frase citata NON sono nel riassunto: aperte dal ruolo che la cita (A, versione HTML), non rilette da me
Usata per: affidabilità per livello e orizzonte e nitidezza come misura; soglia R_avg ≥ 0,95 e R_min ≥ 0,90; su ETH/UCY Trajectron++ 64,9 / 30,9, Social-Implicit 82,7 / 62,5, MID 84,6 / 65,9, FlowChain 86,5 / 62,2, proposta 91,1 / 72,5; «None of the tested models can achieve suitable Reliability scores» — `f8-continuita/07-ricercatore/FONTI.md` (S1), `CONSEGNA.md` righe 27, 41, 67, `PREVISIONI.md` riga 65 **[f7–f10: non vagliato dall'arbitro]**
Note: cifre da rileggere nel testo prima di metterle in un documento. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### hornung2013 [31]
Tipo: articolo scientifico
Autori: Armin Hornung, Kai M. Wurm, Maren Bennewitz, Cyrill Stachniss, Wolfram Burgard
Titolo: OctoMap: an efficient probabilistic 3D mapping framework based on octrees
Sede e anno: Autonomous Robots, vol. 34(3), pp. 189–206, aprile 2013 (in linea 7-2-2013)
Identificativo: DOI 10.1007/s10514-012-9321-0
Link: https://www.hrl.uni-bonn.de/papers/hornung13auro-preprint.pdf (dà una pagina, non il PDF)
Verifica: verificata dal curatore il 14-11-2026 in parte — (rif-1) già verificata dal curatore in f3 solo nei dati bibliografici. Ricontrollati oggi su Crossref [g] (numero del fascicolo aggiunto). Testo NON letto: Springer reindirizza a un accesso, la copia degli autori ha restituito una pagina HTML e non il PDF.
Usata per: voxel e octree «distinguono libero, occupato e ignoto, ma con raggi in 3D e ipotesi di mondo statico» — `f1/dfac83300259/CONSEGNA.md` (§1.6)
Note: l'affermazione sul contenuto non è verificata sul testo (il ruolo l'aveva dal riassunto di ricerca). Rilevante per l'estensione f7 (mappa voxel 3D): va letta prima di citarla lì.

### hsieh2023 [32]
Tipo: articolo scientifico (prestampa) e insieme di dati
Autori: Cheng-Yen Hsieh, Kaihua Chen, Achal Dave, Tarasha Khurana, Deva Ramanan
Titolo: TAO-Amodal: A Benchmark for Tracking Any Object Amodally
Sede e anno: arXiv, v1 19-12-2023, v3 2-4-2024; sede a stampa: non controllata
Identificativo: arXiv 2312.12433
Link: https://arxiv.org/abs/2312.12433
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-1) già verificata dal curatore in f3 [g]: la frase «…struggle to detect and track objects under heavy occlusion» e i guadagni +2,1 % e +3,3 %. Ricontrollati oggi su arXiv [g] titolo, autori e date. ‖ (rif-4) [API]: «struggle to detect and track objects under heavy occlusion» presente nel riassunto; già verificata dal curatore in f3 (F20)
Usata per: F20: la percezione amodale è acerba; guadagni di 2–3 punti con la messa a punto — `f1/3fff79e9c3ea/FONTI.md`, `f1/3fff79e9c3ea/CONSEGNA.md` (§1.5)
Usata per: riquadri amodali come verità in occlusione; i metodi faticano in occlusione pesante — `f8-continuita/07-ricercatore/FONTI.md` (S12), `CONSEGNA.md` riga 65 **[f7–f10: non vagliato dall'arbitro]**
Note: (rif-1) solo riassunto; il titolo citato in FONTI.md («TAO-Amodal») è abbreviato. Alcuni usi vengono dalle estensioni f7–f10: NON ancora vagliati dall'arbitro (marcati riga per riga).

### hulgard2016 [33]
Tipo: articolo scientifico
Autori: Katrine Hulgard, John M. Ratcliffe
Titolo: Sonar sound groups and increased terminal buzz duration reflect task complexity in hunting bats
Sede e anno: Scientific Reports, vol. 6, articolo 21500, 2016 (9-2-2016)
Identificativo: DOI 10.1038/srep21500; PMC4746672
Link: https://pmc.ncbi.nlm.nih.gov/articles/PMC4746672 ; anche (rif-2): https://doi.org/10.1038/srep21500
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-1) già verificata dal curatore in f3 solo nei dati bibliografici. Completata oggi [g]: Crossref (volume, numero d'articolo) e testo intero da Europe PMC: «At the onset of buzz I, the bat… begin to produce calls at rates >90 calls/s»; «In buzz II, bats… produce calls at rates >160 calls/s». ‖ (rif-2) per i soli dati bibliografici (registro Crossref). Testo non letto. Già in f3/fonti (solo dati bibliografici).
Usata per: analogia di creativo-4: il pipistrello alza il ritmo dei richiami in avvicinamento, oltre 90 e poi oltre 160 al secondo — `f1/e30f9e2dd4d7/CONSEGNA.md`
Usata per: l'analogia del «ronzio terminale» (uno «sguardo costoso» alla traccia più minacciosa) — `f2/01-traduzione/SCHEDE.md` (`creativo-4`); `f2/03-triage/TRIAGE.md` e `f2/05-selezione/SELEZIONE.md` (H-020, esclusa).
Note: (rif-1) nel testo la seconda frase porta un rimando bibliografico (nota 9): i due valori sono ripresi dalla letteratura, non misurati in questo studio. Aperta anche dal ruolo. (rif-2) nei file del gruppo c'è solo il nome dell'idea; il legame con questo articolo viene da f1 e da f3. È un'analogia biologica: non sostiene nessuna cifra, e l'idea è stata esclusa dal ramo. Differenza fra i gruppi: rif-2 ha verificato i soli dati bibliografici; rif-1 ha letto il testo intero su Europe PMC: tenuta la verifica di rif-1.

### hullman2015 [34]
Tipo: articolo scientifico
Autori: Jessica Hullman; Paul Resnick; Eytan Adar
Titolo: Hypothetical Outcome Plots Outperform Error Bars and Violin Plots for Inferences about Reliability of Variable Ordering
Sede e anno: PLOS ONE 10(11):e0142444, 2015
Identificativo: DOI 10.1371/journal.pone.0142444
Link: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0142444
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-4) [API] e [T]: pagina aperta, titolo e autori presenti
Usata per: esiti possibili animati battono le barre d'errore nei confronti — `f8-continuita/06-visualizzatore/CONSEGNA.md` riga 47 **[f7–f10: non vagliato dall'arbitro]**
Note: l'affermazione coincide con il titolo. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### hunt2013 [35]
Tipo: altro (tesi, secondo il ruolo)
Autori: Hunt (nome: manca)
Titolo: manca
Sede e anno: 2013; istituzione: manca
Identificativo: manca
Link: manca
Verifica: vista solo nel riassunto di un motore di ricerca — (rif-4) (dal ruolo); non cercata da me: dati insufficienti
Usata per: fiducia dei controllori e incertezza della previsione — `f8-continuita/07-ricercatore/FONTI.md` (§5, marca R) **[f7–f10: non vagliato dall'arbitro]**
Note: non citabile così com'è. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### joslyn2021 [36]
Tipo: articolo scientifico
Autori: Susan Joslyn; Sonia Savelli
Titolo: Visualizing Uncertainty for Non-Expert End Users: The Challenge of the Deterministic Construal Error
Sede e anno: Frontiers in Computer Science, vol. 2, articolo 590232, 18-1-2021
Identificativo: DOI 10.3389/fcomp.2020.590232
Link: https://www.frontiersin.org/journals/computer-science/articles/10.3389/fcomp.2020.590232/full
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-4) [API] e [T]: «deterministic construal error» presente (17 volte)
Usata per: il cono d'incertezza è letto come estensione dell'oggetto — `f8-continuita/06-visualizzatore/CONSEGNA.md` riga 43 **[f7–f10: non vagliato dall'arbitro]**
Note: esiste un corrigendum (Frontiers in Computer Science 4, 2022, DOI 10.3389/fcomp.2022.1093379): non letto (C9). Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### kalman1960 [37]
Tipo: articolo scientifico (metodo)
Autori: R. E. Kalman (cognome dal registro; iniziali a memoria, non verificate)
Titolo: A New Approach to Linear Filtering and Prediction Problems
Sede e anno: Journal of Basic Engineering (Transactions of the ASME), vol. 82, n. 1, pp. 35–45, 1960
Identificativo: DOI 10.1115/1.3662552
Link: https://doi.org/10.1115/1.3662552
Verifica: verificata dal curatore il 14-11-2026 in parte — (rif-2) per i soli dati bibliografici (registro Crossref). Testo non letto.
Usata per: il filtro di Kalman lineare a velocità quasi costante [x, y, vx, vy], q = 0,2 m²/s³ — `f2/01-traduzione/SCHEDE.md` (`kalman-1`, `kalman-2`); `f3/H-012/01-scene-dinamiche/SOLUZIONE.md` (B4); `f4/H-012/05-correzioni/SOLUZIONE_V2.md` (B4) e tutti i file del torneo.
Note: metodo nominato senza riferimento: voce aggiunta da me. Le soglie χ² usate nei file sono algebra, ricontrollata oggi: 9,21 = −2·ln(0,01) e 18,42 = −2·ln(0,0001), due gradi di libertà.

### kayukawa2019 [38]
Tipo: articolo scientifico
Autori: Seita Kayukawa; Keita Higuchi; João Guerreiro; Shigeo Morishima; Yoichi Sato; Kris Kitani; Chieko Asakawa
Titolo: BBeep: A Sonic Collision Avoidance System for Blind Travellers and Nearby Pedestrians
Sede e anno: CHI Conference on Human Factors in Computing Systems (CHI 2019), pp. 1–12
Identificativo: DOI 10.1145/3290605.3300282
Link: https://wotipati.github.io/projects/BBeep/paper/CHI'19_BBeep_preprint.pdf
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-4) [API] e [T]: nel PDF «…linear extrapolation is used to predict their future path», soglie a 5,0 s e 2,5 s, prova in un aeroporto internazionale con «six blind users»; la stringa «6 blind participants» come citata non c'è (correzione C8)
Usata per: previsione per estrapolazione lineare, avviso a 5 s e a 2,5 s, sei partecipanti non vedenti, nessuna incertezza in uscita — `f8-continuita/07-ricercatore/FONTI.md` (S20), `CONSEGNA.md` riga 74 **[f7–f10: non vagliato dall'arbitro]**
Note: Crossref registra il titolo come «BBeep»; titolo completo e nomi degli autori letti nel PDF [T]. È la prestampa degli autori, non la versione dell'editore. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### khurana2021 [39]
Tipo: articolo scientifico
Autori: Tarasha Khurana; Achal Dave; Deva Ramanan
Titolo: Detecting Invisible People
Sede e anno: IEEE/CVF ICCV 2021, pp. 3154–3164; arXiv 15-12-2020
Identificativo: DOI 10.1109/ICCV48922.2021.00316; arXiv:2012.08419
Link: https://arxiv.org/abs/2012.08419
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-4) [API]: «a short-term forecasting challenge», 11,4 % e 5,0 % di F1 presenti nel riassunto
Usata per: l'occlusione trattata come previsione a breve termine; +11,4 % e +5,0 % di F1 — `f8-continuita/07-ricercatore/FONTI.md` (§3) **[f7–f10: non vagliato dall'arbitro]**
Note: `FONTI.md` non dava la sede. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### kim2026 [40]
Tipo: articolo scientifico
Autori: Seungjae Kim; SeungJoon Lee; MyeongAh Cho
Titolo: PlugTrack: Multi-Perceptive Motion Analysis for Adaptive Fusion in Multi-Object Tracking
Sede e anno: Proceedings of the AAAI Conference on Artificial Intelligence 40(7):5709–5716, 2026
Identificativo: DOI 10.1609/aaai.v40i7.37491; arXiv:2511.13105
Link: https://arxiv.org/abs/2511.13105
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-4) [API] e [T]: «Kalman filter outperforms data-driven predictors in up to 34% of cases» nel riassunto; nel testo HTML v1: su DanceTrack il 34 % dei tracciati (1 700 su 5 000)
Usata per: il Kalman batte i predittori appresi fino al 34 % dei casi anche su moto non lineare — `f8-continuita/07-ricercatore/FONTI.md` (S10), `CONSEGNA.md` righe 57 e 80 **[f7–f10: non vagliato dall'arbitro]**
Note: riquadri in immagini, non posizioni al suolo. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### klatzky2006 [41]
Tipo: articolo scientifico
Autori: Roberta L. Klatzky, James R. Marston, Nicholas A. Giudice, Reginald G. Golledge, Jack M. Loomis
Titolo: Cognitive load of navigating without vision when guided by virtual sound versus spatial language
Sede e anno: Journal of Experimental Psychology: Applied, vol. 12(4), pp. 223–232, dicembre 2006
Identificativo: DOI 10.1037/1076-898X.12.4.223
Link: https://doi.org/10.1037/1076-898X.12.4.223
Verifica: verificata dal curatore il 14-11-2026 in parte — (rif-1) solo nei dati bibliografici [g] (Crossref): esiste con questi autori, titolo e sede. Il contenuto non è stato letto.
Usata per: F11 («Giudice et al. 2008 / Klatzky et al. 2006»): stessa affermazione di `giudice2008` — `f1/3fff79e9c3ea/FONTI.md`
Note: in FONTI.md è citato solo per nome e anno; titolo e sede li ho trovati oggi cercando per titolo. L'affermazione è verificata su `giudice2008`, non qui.

### koch2007 [42]
Tipo: articolo scientifico
Autori: Wolfgang Koch
Titolo: On exploiting 'negative' sensor evidence for target tracking and sensor data fusion
Sede e anno: Information Fusion 8(1):28–39, 2007
Identificativo: DOI 10.1016/j.inffus.2005.09.002
Link: https://dblp.org/rec/journals/inffus/Koch07 (oggi protetto da un controllo anti-automi); https://doi.org/10.1016/j.inffus.2005.09.002
Verifica: verificata dal curatore il 14-11-2026 in parte — (rif-4) [API Crossref] solo per i dati bibliografici; la formula con la probabilità di rilevamento: non verificata (lo dice anche il ruolo)
Usata per: fonte sull'evidenza negativa — `f9-preproposta/10-rovesciatore/CONSEGNA.md` riga 64 **[f7–f10: non vagliato dall'arbitro]**
Note: Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### koschi-mediatum-1575368 [43]
Tipo: altro (documento di mediaTUM non identificato: forse una tesi di dottorato)
Autori: non verificato per il documento citato; probabile Markus Koschi (tesi) o Markus Koschi, Matthias Althoff (articolo)
Titolo: non verificato per il documento citato. Titolo probabile, dal riassunto di un motore di ricerca: «Set-based Prediction of Traffic Participants and its Applications to Safe Motion Planning» (tesi di dottorato, Technische Universität München, 2021)
Sede e anno: non verificato
Identificativo: mediaTUM, documento 1575368
Link: https://mediatum.ub.tum.de/doc/1575368/1575368.pdf
Verifica: non raggiungibile — (rif-3) il sito risponde con una pagina di protezione contro i programmi automatici (Anubis), sia sul PDF sia sulla scheda. Vista solo nel riassunto di un motore di ricerca, come già dal ruolo che la cita.
Usata per: oggetti fantasma fuori dall'area osservata, come precedente dello strato 1 — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §3, S33
Note: l'articolo di rivista collegato esiste e l'ho verificato sul registro Crossref [m]: Markus Koschi, Matthias Althoff, «Set-Based Prediction of Traffic Participants Considering Occlusions and Traffic Rules», IEEE Transactions on Intelligent Vehicles 6(2), pp. 249–265, giugno 2021, DOI 10.1109/TIV.2020.3017385. Se serve una citazione sicura conviene usare questa, dopo averne letto il testo (non letto oggi). All'unione: tenuta separata da `koschi2021` (l'articolo di rivista, mediaTUM 1575358), perché l'identità del documento 1575368 non è accertata; nel gruppo rif-3 la chiave era `koschi2021`.

### koschi2021 [44]
Tipo: articolo scientifico
Autori: Markus Koschi, Matthias Althoff
Titolo: Set-Based Prediction of Traffic Participants Considering Occlusions and Traffic Rules
Sede e anno: IEEE Transactions on Intelligent Vehicles, vol. 6(2), pp. 249–265, giugno 2021 (in linea 2020)
Identificativo: DOI 10.1109/TIV.2020.3017385
Link: https://mediatum.ub.tum.de/1575358 (respinge i lettori automatici)
Verifica: dato diverso — (rif-1) già verificata dal curatore in f3, con correzione dell'anno (testo non letto). Ricontrollati oggi: volume, pagine e data su Crossref [g]; riassunto su Semantic Scholar [g]: «a formal set-based prediction that contains all acceptable future behaviors of both detected and potentially hidden traffic participants», con analisi di raggiungibilità per veicoli, pedoni e ciclisti.
Usata per: fonte di rovesciatore-2 (insieme raggiungibile v_max·τ per chi è nascosto), dichiarata «testi non riletti» — `f1/8f275a60e807/CONSEGNA.md`
Note: dato diverso: «IEEE T-IV 2020» va scritto 2021. Il trasferimento da veicoli a pedoni e ausili è del ruolo («non verificato»); il riassunto nomina però anche i pedoni. All'unione: il quadro di dominio (S33) cita un altro documento di mediaTUM, non identificato: vedi `koschi-mediatum-1575368`. Nella sezione E la chiave [koschi2021] indica questo articolo.

### kozlov2026 [45]
Tipo: articolo scientifico (prestampa; lavori in corso)
Autori: Timofei Kozlov, Artem Trandofilov, Georgii Gazaryan, Issatay Tokmurziyev, Miguel Altamirano Cabrera, Dzmitry Tsetserukou
Titolo: GuideTouch: An Obstacle Avoidance Device with Tactile Feedback for Visually Impaired
Sede e anno: accettato fra i Late-Breaking Reports di HRI 2026 (commento arXiv); arXiv v1 20-1-2026, v2 21-1-2026; pagine: manca
Identificativo: arXiv 2601.13813
Link: https://arxiv.org/abs/2601.13813 ; https://arxiv.org/html/2601.13813
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-1) già verificata dal curatore in f3 sul riassunto. Completata oggi: autori e sede (arXiv [g]); testo HTML aperto [r]: «we interviewed 28 visually impaired participants (17 male, 11 female, aged 16–60)»; sostituire il bastone «which our user study indicates is highly undesirable»; 92,9 % per i motivi primari su 22 partecipanti senza disabilità visiva; 93,75 % con 14 utenti con disabilità visiva (§ 3.4: 93,7 %).
Usata per: F6: due ToF in verticale, quattro attuatori; 92,9 % (22 partecipanti), 93,75 % (14 utenti con disabilità visiva); 28 intervistati; sostituire il bastone è «highly undesirable» — `f1/3fff79e9c3ea/FONTI.md`, `f1/3fff79e9c3ea/CONSEGNA.md` (§1.7, §3)
Note: lavoro preliminare, campioni piccoli (14 e 22). Non confondere i due gruppi.

### krejci2026 [46]
Tipo: articolo scientifico
Autori: Jan Krejčí; Oliver Kost; Yuxuan Xia; Lennart Svensson; Ondřej Straka
Titolo: Occlusion-Aware Multi-Object Tracking via Expected Probability of Detection
Sede e anno: IEEE Transactions on Aerospace and Electronic Systems, vol. 62, pp. 8211–8228, 2026; arXiv v3 8-4-2026
Identificativo: DOI 10.1109/TAES.2026.3676431; arXiv:2511.20239
Link: https://arxiv.org/abs/2511.20239
Verifica: verificata dal curatore il 14-11-2026 in parte — (rif-4) [API] per i dati bibliografici; le frasi citate sono nel corpo: trovate dal ruolo nel testo estratto (A-g), non rilette da me
Usata per: probabilità di rilevamento legata alla visibilità; prove su tre video di MOT17 con «The visibility ratio is available for each GT BB»; «computational complexities are hardly predictable»; più stime di oggetti occlusi danno più falsi positivi — `f8-continuita/07-ricercatore/FONTI.md` (S13), `CONSEGNA.md` righe 66, 68, 79 **[f7–f10: non vagliato dall'arbitro]**
Note: Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### kress2021 [47]
Tipo: articolo scientifico
Autori: Viktor Kress; Fabian Jeske; Stefan Zernetsch; Konrad Doll; Bernhard Sick
Titolo: Pose and Semantic Map Based Probabilistic Forecast of Vulnerable Road Users' Trajectories
Sede e anno: IEEE Transactions on Intelligent Vehicles 8(3):2592–2603, 2023; prestampa arXiv 4-6-2021
Identificativo: DOI 10.1109/TIV.2022.3149624; arXiv:2106.02598
Link: https://arxiv.org/abs/2106.02598
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-4) [API]: «reliability, sharpness, and positional accuracy» e orizzonte 2,52 s presenti nel riassunto; la frase sulle curve «troppo sicure» non è nel riassunto: non verificata
Usata per: previsioni valutate per affidabilità, nitidezza e accuratezza, orizzonte 2,52 s — `f8-continuita/07-ricercatore/FONTI.md` (S3) **[f7–f10: non vagliato dall'arbitro]**
Note: correzione C5. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### kuhn1955 [48]
Tipo: articolo scientifico (metodo)
Autori: H. W. Kuhn (cognome dal registro; iniziali a memoria, non verificate)
Titolo: The Hungarian method for the assignment problem
Sede e anno: Naval Research Logistics Quarterly, vol. 2, n. 1–2, pp. 83–97, 1955
Identificativo: DOI 10.1002/nav.3800020109
Link: https://doi.org/10.1002/nav.3800020109
Verifica: verificata dal curatore il 14-11-2026 in parte — (rif-2) per i soli dati bibliografici (registro Crossref). Testo non letto.
Usata per: assegnazione «ungherese» dopo la porta di Mahalanobis — `f2/01-traduzione/SCHEDE.md` (`tracciamento-1`); `f2/04-torneo/TORNEO.md` (parte 2, H-013); `f3/H-012/01-scene-dinamiche/SOLUZIONE.md` (B4); `f4/H-012/05-correzioni/SOLUZIONE_V2.md` (B4).
Note: metodo nominato senza riferimento: voce aggiunta da me.

### kuzucu2024 [49]
Tipo: articolo scientifico
Autori: Selim Kuzucu, Kemal Oksuz, Jonathan Sadeghi, Puneet K. Dokania
Titolo: On Calibration of Object Detectors: Pitfalls, Evaluation and Baselines
Sede e anno: Computer Vision – ECCV 2024, Lecture Notes in Computer Science, Springer, pp. 185–204 (in linea 26-10-2024)
Identificativo: DOI 10.1007/978-3-031-72664-4_11; arXiv 2405.20459
Link: https://arxiv.org/abs/2405.20459
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-1) già verificata dal curatore in f3 [g]: «much more powerful and effective than the recent train-time calibration methods»; «more than 7 D-ECE». Ricontrollati oggi autori (arXiv [g]), pagine e DOI (Crossref [g]).
Usata per: F22: Platt e regressione isotonica battono i metodi d'addestramento recenti (oltre 7 punti di D-ECE su COCO, D-DETR contro Cal-DETR) — `f1/3fff79e9c3ea/FONTI.md`, `f1/3fff79e9c3ea/CONSEGNA.md` (§1.6)
Note: vale per rilevatori su COCO; che «si può fare in poche ore» è un giudizio del ruolo.

### lee2026 [50]
Tipo: articolo scientifico
Autori: Sungjae Lee, Junhan Jeong, Yeonjoo Hong, Kwang In Kim
Titolo: Physically Guided Visual Mass Estimation from a Single RGB Image
Sede e anno: IJCAI 2026 (Main Track), secondo il commento arXiv; arXiv v1 28-1-2026, v2 5-5-2026; pagine degli atti: manca
Identificativo: arXiv 2601.20303
Link: https://arxiv.org/abs/2601.20303 ; https://arxiv.org/html/2601.20303v1
Verifica: dato diverso — (rif-1) già verificata dal curatore in f3 [r]: APE su image2mass 0,665 (loro) e 1,066 (image2mass); su ABO-500 0,980 contro 0,976. Dato diverso: «fattore medio 1,68» non è nell'articolo, è exp(0,519) dell'ALDE di Tabella 1, calcolato dal ricercatore. Ricontrollati oggi su arXiv [g]: autori e «Accepted to IJCAI 2026 (Main Track)». ‖ (rif-2) per dati bibliografici e riassunto («mass prediction from pixels is ill-posed»; prove su image2mass e ABO-500). Le cifre (ALDE 0,519; 0,665 e 1,066) oggi non le ho rilette: valgono con la verifica di f3, letta attraverso un riassunto.
Usata per: F29: errore percentuale medio 0,665 e fattore medio 1,68; riferimento del 2017 a 1,066; su un secondo insieme entrambi a 0,98; «la massa non è osservabile» — `f1/3fff79e9c3ea/FONTI.md`, `f1/3fff79e9c3ea/CONSEGNA.md` (§1.3, §3), `f1/3fff79e9c3ea/PREVISIONI.md` (P3: ALDE 0,655 e 0,519)
Usata per: F-002, «la massa non è osservabile… sostenuto dalla letteratura (ricercatore)» — `f2/03-triage/TRIAGE.md` (§2); «F-002: fonte confermata; il "fattore 1,68" è derivato» — `f2/05-selezione/SELEZIONE.md` (§3).
Note: (rif-1) oggetti da catalogo; il ruolo ha letto la v1, oggi esiste la v2 (non confrontate). 1,68 va dichiarato come derivato. (rif-2) i file del gruppo non nominano l'articolo; l'identificazione viene da `f3/fonti/FONTI_VERIFICATE.md` (F29). «Fattore 1,68» = exp(0,519), calcolato dal ricercatore, non scritto nell'articolo. L'articolo stima la massa da un'immagine con un errore grande: sostiene «non affidabile», non «impossibile»; la non osservabilità in senso stretto è dimostrata dallo sciame solo nel modello del punto materiale con forza ignota.

### lerner2007 [51]
Tipo: insieme di dati (articolo che lo descrive: dati «UCY»)
Autori: A. Lerner, Y. Chrysanthou, D. Lischinski (iniziali dall'elenco dei riferimenti di `scholler2020`)
Titolo: Crowds by Example
Sede e anno: Computer Graphics Forum, vol. 26, n. 3, pp. 655–664, 2007
Identificativo: DOI 10.1111/j.1467-8659.2007.01089.x
Link: https://doi.org/10.1111/j.1467-8659.2007.01089.x
Verifica: verificata dal curatore il 14-11-2026 in parte — (rif-2) per i soli dati bibliografici (registro Crossref; voce [31] di `scholler2020`). Testo non letto.
Usata per: come `pellegrini2009` — `f2/01-traduzione/SCHEDE.md` (`ricercatore-2`, rischi).
Note: nei file è solo la sigla «UCY».

### lin2014 [52]
Tipo: insieme di dati (articolo che lo descrive: COCO)
Autori: Tsung-Yi Lin, Michael Maire, Serge Belongie, Lubomir Bourdev, Ross Girshick, James Hays, Pietro Perona, Deva Ramanan, C. Lawrence Zitnick, Piotr Dollár (elenco della versione arXiv; negli atti ECCV gli autori registrati sono otto, senza Bourdev e Girshick)
Titolo: Microsoft COCO: Common Objects in Context
Sede e anno: Computer Vision – ECCV 2014, Lecture Notes in Computer Science, Springer, pp. 740–755, 2014
Identificativo: DOI 10.1007/978-3-319-10602-1_48; arXiv:1405.0312
Link: https://arxiv.org/abs/1405.0312
Verifica: verificata dal curatore il 14-11-2026 in parte — (rif-2) per i soli dati bibliografici (pagina arXiv, registro Crossref). L'elenco delle 80 classi è verificato sulla voce `ultralytics-coco-yaml`, non sull'articolo.
Usata per: «0 su 7 categorie d'ostacolo fra le 80 classi COCO» — `f2/01-traduzione/SCHEDE.md` (`visione-1`, P1); `f2/03-triage/TRIAGE.md` (H-006); `f2/04-torneo/TORNEO.md` (parte 1, H-006); `f2/05-selezione/SELEZIONE.md` (H-006); `f3/H-012/01-scene-dinamiche/SOLUZIONE.md` (B6, §7).
Note: i file citano «COCO» senza riferimento. L'articolo descrive 91 categorie; le 80 sono quelle usate per il rilevamento.

### lin2025 [53]
Tipo: articolo scientifico (prestampa)
Autori: Haotong Lin, Sili Chen, Junhao Liew, Donny Y. Chen, Zhenyu Li, Guang Shi, Jiashi Feng, Bingyi Kang
Titolo: Depth Anything 3: Recovering the Visual Space from Any Views
Sede e anno: arXiv, 13-11-2025; sede a stampa: manca
Identificativo: arXiv 2511.10647
Link: https://arxiv.org/abs/2511.10647
Verifica: verificata dal curatore il 14-11-2026 in parte — (rif-1) già verificata dal curatore in f3 nei dati bibliografici. Ricontrollati oggi su arXiv [g] titolo, autori e data. I numeri citati non vengono dall'articolo ma da `gerdsenai-da3-ros2`. ‖ (rif-2) per i soli dati bibliografici. La cifra dei 43 fps non è dell'articolo: vedi `gerdsenai-da3-jetson`.
Usata per: ripiego senza camera di profondità: profondità monoculare «Depth Anything 3 small» — `f1/c85dbcc51ea6/CONSEGNA.md` (visione-1)
Usata per: profondità monoculare come ripiego senza camera di profondità, lasciata fuori — `f3/H-012/01-scene-dinamiche/SOLUZIONE.md` §8; `f4/H-012/05-correzioni/SOLUZIONE_V2.md` §8 (senza cifra).
Note: (rif-1) l'articolo non è citato direttamente da `visione` (che cita il post di comunità): l'ha aggiunto f3. (rif-2) l'articolo non dà velocità su hardware da campo.

### lindemann2023 [54]
Tipo: articolo scientifico
Autori: Lars Lindemann; Matthew Cleaveland; Gihyun Shim; George J. Pappas
Titolo: Safe Planning in Dynamic Environments Using Conformal Prediction
Sede e anno: IEEE Robotics and Automation Letters 8(8):5116–5123, 2023
Identificativo: DOI 10.1109/LRA.2023.3292071; arXiv:2210.10254
Link: https://arxiv.org/abs/2210.10254
Verifica: verificata dal curatore il 14-11-2026 in parte — (rif-4) [API] per i dati bibliografici (la sede RA-L 2023 era solo R: confermata); le frasi e il 498 su 500 non sono nel riassunto: trovate dal ruolo nel testo estratto (A-g), non rilette da me
Usata per: ipotesi 2 (traiettorie di taratura «independently drawn from D»), nota 3 («In general only exchangeability is needed»), 498 su 500 dentro la regione al 95 % (δ = 0,05, T = 20), prudenza per l'unione dei limiti — `f8-continuita/07-ricercatore/FONTI.md` (S4), `CONSEGNA.md` righe 43–44, 108 **[f7–f10: non vagliato dall'arbitro]**
Note: la garanzia vale solo se taratura e prova vengono dalla stessa distribuzione. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### liu2022 [55]
Tipo: articolo scientifico
Autori: Shuai Liu, Xin Li, Huchuan Lu, You He
Titolo: Multi-Object Tracking Meets Moving UAV
Sede e anno: 2022 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), giugno 2022; pagine 8876–8885 secondo la CVF e mlanthology, 8866–8875 secondo Crossref
Identificativo: DOI 10.1109/CVPR52688.2022.00867
Link: https://mlanthology.org/cvpr/2022/liu2022cvpr-multiobject (testo: https://openaccess.thecvf.com/content/CVPR2022/html/Liu_Multi-Object_Tracking_Meets_Moving_UAV_CVPR_2022_paper.html)
Verifica: dato diverso — (rif-3) l'articolo esiste con questi autori e titolo [m, g], ma nel testo intero la parola «occlusion» non compare (0 occorrenze di «occlu» nel PDF della CVF); c'è «irregular motion caused by moving camera and view change in 3D directions» [g]. Il ruolo che la cita l'aveva vista solo in un risultato di ricerca.
Usata per: i lavori sul tracciamento da drone nominano insieme occlusione e moto irregolare della camera — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §2(d), S21
Usata per: tracciatori per drone, fra i riferimenti di ricerca — stesso file, §3
Note: correzione 1. Sostiene «moto irregolare della camera», non «occlusione». Discordanza sulle pagine non risolta: la deciderebbe la scheda dell'IEEE.

### luiten2021 [56]
Tipo: articolo scientifico
Autori: Jonathon Luiten, Aljoša Ošep, Patrick Dendorfer, Philip Torr, Andreas Geiger, Laura Leal-Taixé, Bastian Leibe
Titolo: HOTA: A Higher Order Metric for Evaluating Multi-Object Tracking
Sede e anno: International Journal of Computer Vision, vol. 129, pp. 548–578, 2021 (in linea 2020)
Identificativo: DOI 10.1007/s11263-020-01375-2; arXiv 2009.07736
Link: https://arxiv.org/abs/2009.07736
Verifica: verificata dal curatore il 14-11-2026 in parte — (rif-1) già verificata dal curatore in f3 (esiste, con questi autori; volume e pagine). Ricontrollati oggi su arXiv [g]: autori, DOI, rivista. Volume e pagine: da f3, non riletti oggi (Crossref ha risposto 429).
Usata per: «HOTA e IDF1 chiedono sequenze annotate: non sono la misura giusta per la demo» — `f1/992c41c8860e/CONSEGNA.md` (§1.7)
Note: che HOTA chieda annotazioni è implicito nella definizione; la frase non è stata letta nel testo.

### lupu2020 [57]
Tipo: articolo scientifico
Autori: Robert-Gabriel Lupu, Oana Mitruț, Andrei Stan, Florina Ungureanu, Kyriaki Kalimeri, Alin Moldoveanu
Titolo: Cognitive and Affective Assessment of Navigation and Mobility Tasks for the Visually Impaired via Electroencephalography and Behavioral Signals
Sede e anno: Sensors, vol. 20(20), articolo 5821, 2020 (15-10-2020)
Identificativo: DOI 10.3390/s20205821; PMID 33076251; PMCID PMC7602506
Link: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7602506/ ; anche (rif-2): https://doi.org/10.3390/s20205821
Verifica: dato diverso — (rif-1) già verificata dal curatore in f3 [r]. Rafforzata oggi [g] sul riassunto registrato in Crossref: «eight visually impaired subjects»; «the haptic stimuli were less intuitive than the audio ones»; la navigazione col dispositivo «increased cognitive load and working memory». ‖ (rif-2) con una precisazione. La pagina MDPI dà 403; dati bibliografici dal registro Crossref e riassunto dal registro Europe PMC: «eight visually impaired subjects»; «the haptic stimuli were less intuitive than the audio ones and that the navigation with the Sound of Vision device increased cognitive load and working memory». Dato diverso: il carico cognitivo maggiore è del dispositivo rispetto al bastone, non dell'aptico rispetto all'audio. Già in f3/fonti (letta là attraverso un riassunto).
Usata per: F8: 8 partecipanti ciechi; stimoli aptici meno intuitivi di quelli sonori; il dispositivo aumenta il carico cognitivo — `f1/3fff79e9c3ea/FONTI.md`, `f1/3fff79e9c3ea/CONSEGNA.md` (§1.7, §3)
Usata per: la stessa frase di `martinez2014` — `f2/05-selezione/SELEZIONE.md` (riga K-010); `f3/H-012/01-scene-dinamiche/SOLUZIONE.md` (§5).
Note: (rif-1) il riassunto dice «visually impaired», non «ciechi»; otto soggetti. (rif-2) otto persone, un solo dispositivo (Sound of Vision). Sostiene «aptico meno intuitivo del sonoro», non «aptico più costoso». Differenza fra i gruppi: rif-2 ha letto nel registro Europe PMC solo cognomi e iniziali; i nomi per esteso sono quelli di rif-1 (da f3 e Crossref).

### lv2024 [58]
Tipo: articolo scientifico
Autori: Weiyi Lv; Yuhang Huang; Ning Zhang; Ruei-Sung Lin; Mei Han; Dan Zeng
Titolo: DiffMOT: A Real-time Diffusion-based Multiple Object Tracker with Non-linear Prediction
Sede e anno: IEEE/CVF CVPR 2024, pp. 19321–19330
Identificativo: DOI 10.1109/CVPR52733.2024.01828; arXiv:2403.02075
Link: https://arxiv.org/abs/2403.02075
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-4) [API] e [T]: 22,7 fps e 62,3 % HOTA su DanceTrack nel riassunto; «real-time at 22.7 FPS on an RTX 3090 machine» nel testo HTML v2 (in `FONTI.md` l'hardware era solo R: ora verificato)
Usata per: danza e sport, 22,7 fps con scheda grafica — `f8-continuita/07-ricercatore/FONTI.md` (riga di S10), `CONSEGNA.md` riga 59 **[f7–f10: non vagliato dall'arbitro]**
Note: richiede GPU. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### maceachren2012 [59]
Tipo: articolo scientifico
Autori: Alan M. MacEachren; Robert E. Roth; James O'Brien; Bonan Li; Derek Swingley; Mark Gahegan
Titolo: Visual Semiotics & Uncertainty Visualization: An Empirical Study
Sede e anno: IEEE Transactions on Visualization and Computer Graphics 18(12):2496–2505, 2012
Identificativo: DOI 10.1109/TVCG.2012.279
Link: https://ieeevis.org/year/2012/paper/infovis/visual-semiotics-uncertainty-visualization-empirical-study
Verifica: verificata dal curatore il 14-11-2026 in parte — (rif-4) [API] e [T] per i dati bibliografici; l'affermazione (sfocatura, posizione e valore di grigio i più intuitivi) NON è nel riassunto della pagina: non verificata
Usata per: sfocatura, posizione e valore di grigio sono i segni più intuitivi per l'incerto — `f8-continuita/06-visualizzatore/CONSEGNA.md` riga 44 **[f7–f10: non vagliato dall'arbitro]**
Note: da rileggere nell'articolo. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### machado2009 [60]
Tipo: articolo scientifico
Autori: Gustavo M. Machado; Manuel M. Oliveira; Leandro A. F. Fernandes
Titolo: A Physiologically-based Model for Simulation of Color Vision Deficiency
Sede e anno: IEEE Transactions on Visualization and Computer Graphics 15(6):1291–1298, 2009
Identificativo: DOI 10.1109/TVCG.2009.113
Link: https://www.inf.ufrgs.br/~oliveira/pubs_files/CVD_Simulation/CVD_Simulation.html
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-4) [API] e [T]: pagina degli autori aperta; le matrici non ricontrollate valore per valore (il ruolo dice di averle verificate lì)
Usata per: matrici per simulare i difetti della visione dei colori nella prova delle interfacce — `f9-preproposta/09-interfacce/CONSEGNA.md` righe 77 e 80 **[f7–f10: non vagliato dall'arbitro]**
Note: esistono correzioni pubblicate (TVCG 16(2):352, 2010, DOI 10.1109/TVCG.2010.10): non lette (C9). L'uso in RGB lineare è una scelta del ruolo. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### mandaokar2026 [61]
Tipo: articolo scientifico (prestampa)
Autori: Dnyandeep Mandaokar, Bernhard Rinner
Titolo: RADAR Perception for Dynamic Obstacle Avoidance onboard small-scale Quadrotor UAVs
Sede e anno: prestampa arXiv, v1 del 3 agosto 2026, v2 del 6 novembre 2026; «submitted for possible publication and is currently under review»; nessuna sede pubblicata
Identificativo: arXiv:2608.01855 (cs.RO); DOI 10.48550/arXiv.2608.01855
Link: https://arxiv.org/abs/2608.01855
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-3) [g, sul testo del PDF v2] — «Raspberry Pi 4B», «approximately 14 ms per RADAR frame», «a system latency of 75 ms from first detection to the avoidance command», «closing speeds up to 14.6 m/s», portante «77 GHz», «mean position errors of at most 0.15 m, 0.93 m, and 0.87 m in the x, y, and z directions». Il ruolo che la cita l'aveva aperta.
Usata per: radar a 77 GHz su quadrirotore; tracciatore su Raspberry Pi 4B; 75 ms fino al comando; avvicinamenti fino a 14,6 m/s; errori fino a 0,9 m — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §2(b), S16
Usata per: una catena radar con tracciatore gira su un Raspberry Pi 4B — stesso file, §2(f)
Usata per: tracciamento da piattaforma in moto con radar a bordo — stesso file, §3
Note: correzione 5: gli 0,93 m e 0,87 m sono errori *medi* di posizione sugli assi y e z, non «errori laterali fino a». È una prestampa non ancora passata da una revisione; 300 lanci di palle e 90 prove nel fumo, quindi non garantisce niente su persone o veicoli.

### martinez2014 [62]
Tipo: articolo scientifico
Autori: Manuel Martinez, Angela Constantinescu, Boris Schauerte, Daniel Koester, Rainer Stiefelhagen
Titolo: Cognitive Evaluation of Haptic and Audio Feedback in Short Range Navigation Tasks
Sede e anno: Computers Helping People with Special Needs (ICCHP 2014), Lecture Notes in Computer Science, Springer, pp. 128–135, 2014
Identificativo: DOI 10.1007/978-3-319-08599-9_20
Link: https://doi.org/10.1007/978-3-319-08599-9_20 (il PDF https://cvhci.iar.kit.edu/~dkoester/publications/martinezICCHP2014tlx.pdf dà 404)
Verifica: dato diverso — (rif-1) già verificata dal curatore in f3 [g, sul riassunto Springer]: «22 times higher cognitive load»; «not found on blindfolded users». Ricontrollati oggi su Crossref [g]: titolo, autori, pagine, anno. ‖ (rif-2) l'articolo dice il contrario di ciò che gli si attribuisce. Pagina Springer aperta oggi (metadati e riassunto; il testo intero è a pagamento): «for white cane users, auditory feedback results in a 22 times higher cognitive load than haptic feedback. This discrepancy in cognitive load was not found on blindfolded users, thus we argue against evaluating navigation systems solely with blindfolded users». Già in f3/fonti, dove la frase è riportata senza il verso.
Usata per: F7: per chi usa il bastone il feedback sonoro dà un carico NASA-TLX 22 volte maggiore dell'aptico; l'effetto non c'è nei vedenti bendati — `f1/3fff79e9c3ea/FONTI.md`, `f1/3fff79e9c3ea/CONSEGNA.md` (§1.7, §3)
Usata per: «Fonti: in due studi l'aptico costa più dell'audio; non decide fra battito e messaggi» — `f2/05-selezione/SELEZIONE.md` (riga K-010); `f3/H-012/01-scene-dinamiche/SOLUZIONE.md` (§5, riga «Feedback (K-010)»).
Note: (rif-1) letto il solo riassunto, non il testo; la numerosità del campione non è stata letta: manca. (rif-2) correzione 1 in testa. Per chi usa il bastone è il sonoro a costare 22 volte di più (protocollo NASA-TLX). L'articolo avverte anche che i vedenti bendati non valgono come sostituti: tocca la prova «tre persone bendate» prevista per K-010. Numero dei partecipanti non letto.

### marvel2017 [63]
Tipo: articolo scientifico
Autori: Jeremy A. Marvel; Rick Norcross
Titolo: Implementing Speed and Separation Monitoring in Collaborative Robot Workcells
Sede e anno: Robotics and Computer-Integrated Manufacturing 44:144–155, 2017
Identificativo: DOI 10.1016/j.rcim.2016.08.001; PMC5117641
Link: https://pmc.ncbi.nlm.nih.gov/articles/PMC5117641
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-4) [API] e [T]: nella pagina PMC «the time for the robot system to respond…», «operator position», 1,6 m/s presenti; la formula per intero non ricontrollata simbolo per simbolo
Usata per: forma lineare della distanza di protezione S = v_H·T_R + v_H·T_S + v_R·T_R + B + C + Z_S + Z_R, con v_H = 1,6 m/s — `f9-preproposta/06-esperto-dominio/CONSEGNA.md` riga 69 (F7); la distanza della ISO/TS 15066 somma percorsi nel caso peggiore e incertezze di posizione — `f7-estensione/05-esperto-dominio/CONSEGNA.md` riga 21 (S9) **[f7–f10: non vagliato dall'arbitro]**
Note: è una fonte secondaria sul testo della norma (vedi `iso-ts-15066`); i 2,80 m e 1,68 m sono conti del ruolo. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### mercat2019 [64]
Tipo: articolo scientifico (prestampa)
Autori: Jean Mercat; Nicole El Zoghby; Guillaume Sandou; Dominique Beauvois; Guillermo Pita Gil
Titolo: Kinematic Single Vehicle Trajectory Prediction Baselines and Applications with the NGSIM Dataset
Sede e anno: arXiv, v4 28-10-2020; sede di pubblicazione: manca
Identificativo: arXiv:1908.11472
Link: https://ar5iv.labs.arxiv.org/html/1908.11472
Verifica: verificata dal curatore il 14-11-2026 in parte — (rif-4) [API] per autori, titolo e date; la tabella degli RMSE non è nel riassunto: aperta dal ruolo che la cita (A, copia ar5iv), non riletta da me
Usata per: veicoli (NGSIM): RMSE a 1–5 s del Kalman a velocità costante 0,75 / 1,81 / 3,16 / 4,80 / 6,70 m, V-LSTM 0,67 / 1,62 / 2,86 / 4,40 / 6,26, Kalman-LSTM 0,68 / 1,54 / 2,72 / 4,20 / 5,95; NLL — `f8-continuita/07-ricercatore/FONTI.md` (S9), `CONSEGNA.md` riga 58 **[f7–f10: non vagliato dall'arbitro]**
Note: veicoli in autostrada, non pedoni; ar5iv è una copia di terzi del testo arXiv. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### millane2024 [65]
Tipo: articolo scientifico
Autori: Alexander Millane; Helen Oleynikova; Emilie Wirbel; Remo Steiner; Vikram Ramasamy; David Tingdahl; Roland Siegwart
Titolo: nvblox: GPU-Accelerated Incremental Signed Distance Field Mapping
Sede e anno: IEEE ICRA 2024 (dal commento arXiv); arXiv v2 15-3-2024
Identificativo: arXiv:2311.00626
Link: https://arxiv.org/abs/2311.00626
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-4) [API]: «177x» presente nel riassunto
Usata per: nvblox «up to a 177x speed-up», su GPU — `f7-estensione/05-esperto-dominio/CONSEGNA.md` righe 29 e 80 (S6) **[f7–f10: non vagliato dall'arbitro]**
Note: richiede la GPU; la licenza è «NV» (non verificata) nel file. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### moras2011 [66]
Tipo: articolo scientifico
Autori: Julien Moras, Véronique Cherfaoui, Philippe Bonnifait
Titolo: Credibilist Occupancy Grids for Vehicle Perception in Dynamic Environments
Sede e anno: IEEE International Conference on Robotics and Automation (ICRA) 2011, pp. 84–89
Identificativo: DOI 10.1109/ICRA.2011.5980298; HAL hal-00615303
Link: https://hal.archives-ouvertes.fr/hal-00615303
Verifica: verificata dal curatore il 14-11-2026 in parte — (rif-1) già verificata dal curatore in f3 solo nei dati bibliografici. Completata oggi [g]: pagine e DOI (Crossref); riassunto dal registro HAL: «uncertainty arises from ignorance and errors… A credibilist approach is used to model the sensor information and to do a global fusion with the world-fixed map».
Usata per: griglie evidenziali: «l'idea giusta (l'ignoranza ha una sua massa)» — `f1/dfac83300259/CONSEGNA.md` (§1.6)
Note: il riassunto conferma che l'ignoranza è trattata come sorgente d'incertezza a sé; la formulazione «ha una sua massa» (funzioni di credenza) è coerente ma non letta nel testo.

### munir2023 [67]
Tipo: articolo scientifico
Autori: Muhammad Akhtar Munir, Muhammad Haris Khan, Salman Khan, Fahad Shahbaz Khan
Titolo: Bridging Precision and Confidence: A Train-Time Loss for Calibrating Object Detection
Sede e anno: IEEE/CVF CVPR 2023, pp. 11474–11483
Identificativo: DOI 10.1109/CVPR52729.2023.01104; arXiv 2303.14404
Link: https://openaccess.thecvf.com/content/CVPR2023/papers/Munir_Bridging_Precision_and_Confidence_A_Train-Time_Loss_for_Calibrating_Object_CVPR_2023_paper.pdf (403 oggi) ; https://arxiv.org/abs/2303.14404
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-1) [g]: dati bibliografici su arXiv e Crossref; nel PDF arXiv: «Post-hoc calibration methods are simple and effective, however, they require hold-out validation data, and are dependent on architecture [25]».
Usata per: F23: i metodi a posteriori chiedono dati di validazione messi da parte e dipendono dall'architettura — `f1/3fff79e9c3ea/FONTI.md`, `f1/3fff79e9c3ea/CONSEGNA.md` (§1.6)
Note: in f3 erano verificati solo i dati bibliografici; oggi anche la frase. La frase è nella versione arXiv; quella CVF non è stata aperta (403).

### nguyen2012 [68]
Tipo: articolo scientifico
Autori: Chuong V. Nguyen; Shahram Izadi; David Lovell
Titolo: Modeling Kinect Sensor Noise for Improved 3D Reconstruction and Tracking
Sede e anno: Second International Conference on 3D Imaging, Modeling, Processing, Visualization & Transmission (3DIMPVT), 2012, pp. 524–530
Identificativo: DOI 10.1109/3DIMPVT.2012.84
Link: https://doi.org/10.1109/3DIMPVT.2012.84
Verifica: verificata dal curatore il 14-11-2026 in parte — (rif-4) [API] solo per esistenza e dati bibliografici; il ruolo la cita a memoria
Usata per: esistono modelli di rumore assiale e laterale per il Kinect, non per lo stereo attivo — `f10-dati/02-sensori/PREVISIONI.md` riga 15 (sensori-P7) **[f7–f10: non vagliato dall'arbitro]**
Note: Kinect v1 (luce strutturata). Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### niessner2013 [69]
Tipo: articolo scientifico
Autori: Matthias Nießner; Michael Zollhöfer; Shahram Izadi; Marc Stamminger
Titolo: Real-time 3D Reconstruction at Scale using Voxel Hashing
Sede e anno: ACM Transactions on Graphics 32(6), 2013 (Crossref: pp. 1–11)
Identificativo: DOI 10.1145/2508363.2508374
Link: https://niessnerlab.org/projects/niessner2013hashing.html
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-4) [API] e [T]: pagina aperta; «performed at real-time rates on commodity graphics hardware» presente
Usata per: lo schema proiettivo della fusione volumetrica da camere di profondità (lì su GPU), a fronte di 307 ms per il lancio dei raggi e 2,2 ms per il confronto proiettivo misurati dal ruolo — `f7-estensione/03-nuvole-punti/CONSEGNA.md` riga 36 **[f7–f10: non vagliato dall'arbitro]**
Note: i tempi sono misure del ruolo, non della fonte. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### nuss2018 [70]
Tipo: articolo scientifico
Autori: Dominik Nuss, Stephan Reuter, Markus Thom, Ting Yuan, Gunther Krehl, Michael Maile, Axel Gern, Klaus Dietmayer
Titolo: A random finite set approach for dynamic occupancy grid maps with real-time application
Sede e anno: The International Journal of Robotics Research, vol. 37(8), pp. 841–866, luglio 2018
Identificativo: DOI 10.1177/0278364918775523; arXiv 1605.02406
Link: https://arxiv.org/abs/1605.02406
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-1) già verificata dal curatore in f3 [g]: «highly efficient parallel particle filter». Ricontrollati oggi autori (arXiv [g]), volume, pagine e riassunto (Crossref [g]). ‖ (rif-3) [r per arXiv; m per rivista, volume, pagine, riassunto]. Già verificata dal curatore in `f3/fonti/FONTI_VERIFICATE.md`.
Usata per: griglia dinamica con velocità per cella: filtro a particelle in parallelo, «troppo per un hackathon» — `f1/dfac83300259/CONSEGNA.md` (§1.6)
Usata per: griglie dinamiche d'occupazione come riferimento di ricerca — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §3, S34
Note: (rif-1) «troppo per un hackathon» è un giudizio del ruolo. (rif-3) dati laser e radar da veicolo stradale; non riguarda camere di profondità.

### oleynikova2017 [71]
Tipo: articolo scientifico
Autori: Helen Oleynikova; Zachary Taylor; Marius Fehr; Juan Nieto; Roland Siegwart
Titolo: Voxblox: Incremental 3D Euclidean Signed Distance Fields for On-Board MAV Planning
Sede e anno: IEEE/RSJ IROS 2017
Identificativo: DOI 10.1109/IROS.2017.8202315; arXiv:1611.03631
Link: https://arxiv.org/abs/1611.03631
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-4) [API]: «single CPU core» e «real-time» presenti nel riassunto
Usata per: Voxblox «runs in real-time on a single CPU core» — `f7-estensione/05-esperto-dominio/CONSEGNA.md` righe 25 e 80 (S2) **[f7–f10: non vagliato dall'arbitro]**
Note: vedi anche `ethz-voxblox`. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### orzechowski2018 [72]
Tipo: articolo scientifico
Autori: Piotr Franciszek Orzechowski, Annika Meyer, Martin Lauer
Titolo: Tackling Occlusions & Limited Sensor Range with Set-based Safety Verification
Sede e anno: 21st International Conference on Intelligent Transportation Systems (ITSC) 2018, pp. 1729–1736
Identificativo: DOI 10.1109/ITSC.2018.8569332; arXiv 1807.01262
Link: https://arxiv.org/pdf/1807.01262 ; anche (rif-3): https://arxiv.org/abs/1807.01262 ; anche (rif-4): https://arxiv.org/abs/1807.01262
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-1) già verificata dal curatore in f3 [g]: ostacoli nascosti sovrastimati con intervalli di stato. Ricontrollati oggi autori e sede (arXiv [g]), pagine e DOI (Crossref [g]). ‖ (rif-3) [r per la pagina arXiv; m per sede, pagine e DOI]. Già verificata dal curatore in `f3/fonti/FONTI_VERIFICATE.md` («ostacoli nascosti sovrastimati con intervalli di stato: sì»). ‖ (rif-4) [API]: nel riassunto «The state of occluded obstacles is unknown, but can be over-approximated by intervals over all possible states»
Usata per: fonte di rovesciatore-2 (verifica di sicurezza insiemistica sotto occlusione) — `f1/8f275a60e807/CONSEGNA.md`
Usata per: lo strato 1 viene dalla guida automatica: ostacoli nascosti ai bordi del campo visivo, con stati sovrastimati per intervalli — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §3, S32
Usata per: stati nascosti sovrastimati con insiemi raggiungibili — `f7-estensione/01-matematico/CONSEGNA.md` riga 78 **[f7–f10: non vagliato dall'arbitro]**
Note: (rif-1) ambito: guida automatica. (rif-3) garantisce che l'idea ha un precedente in letteratura; non garantisce niente sul nucleo, che è un'altra realizzazione. (rif-4) guida automatica, non una mappa voxel. Nello stesso punto il ruolo dichiara «non verificato» che l'aggiornamento in log-odds presupponga una mappa ferma: resta senza fonte. Alcuni usi vengono dalle estensioni f7–f10: NON ancora vagliati dall'arbitro (marcati riga per riga).

### padilla2017 [73]
Tipo: articolo scientifico
Autori: Lace M. Padilla; Ian T. Ruginski; Sarah H. Creem-Regehr
Titolo: Effects of ensemble and summary displays on interpretations of geospatial uncertainty data
Sede e anno: Cognitive Research: Principles and Implications 2(1):40, 2017
Identificativo: DOI 10.1186/s41235-017-0076-1; PMC5626802
Link: https://pmc.ncbi.nlm.nih.gov/articles/PMC5626802
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-4) [API] e [T]: nel testo della pagina PMC compaiono 0,70, 0,39, 64,15, 99,68 e 179; d = 0,66 e N = 43, 35 non ricontrollati
Usata per: con il cono la quota che dice «l'uragano cresce» è 0,70 contro 0,39 con l'insieme (d = 0,66, N = 179); con l'insieme, impianto più vicino scelto nel 64,15 % invece del 99,68 % — `f8-continuita/07-ricercatore/FONTI.md` (S19), `CONSEGNA.md` righe 72, 120, 122; `f8-continuita/06-visualizzatore/CONSEGNA.md` riga 43 **[f7–f10: non vagliato dall'arbitro]**
Note: mappe meteo e non esperti: altro dominio. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### pang2021 [74]
Tipo: articolo scientifico
Autori: Ziqi Pang, Zhichao Li, Naiyan Wang
Titolo: SimpleTrack: Understanding and Rethinking 3D Multi-object Tracking
Sede e anno: Computer Vision – ECCV 2022 Workshops, Lecture Notes in Computer Science, Springer, pp. 680–696, 2023 (prestampa arXiv del 18-11-2021)
Identificativo: DOI 10.1007/978-3-031-25056-9_43; arXiv 2111.09621
Link: https://arxiv.org/abs/2111.09621
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-1) già verificata dal curatore in f3 [g] («life cycle management» come parte a sé; sede non controllata). Completata oggi: sede, pagine e DOI su Crossref [g]; nel riassunto arXiv le quattro parti «pre-processing of detection, association, motion model, and life cycle management» [g].
Usata per: «SimpleTrack isola la gestione della vita delle tracce come modulo a sé» — `f1/992c41c8860e/CONSEGNA.md` (§1.4)
Note: la chiave tiene l'anno della prestampa; l'anno di stampa è 2023.

### pellegrini2009 [75]
Tipo: insieme di dati (articolo che lo descrive: dati «ETH»)
Autori: S. Pellegrini, A. Ess, K. Schindler, L. Van Gool (iniziali dall'elenco dei riferimenti di `scholler2020`)
Titolo: You'll never walk alone: Modeling social behavior for multi-target tracking
Sede e anno: IEEE 12th International Conference on Computer Vision (ICCV) 2009, pp. 261–268
Identificativo: DOI 10.1109/ICCV.2009.5459260
Link: https://doi.org/10.1109/ICCV.2009.5459260
Verifica: verificata dal curatore il 14-11-2026 in parte — (rif-2) per i soli dati bibliografici (registro Crossref; voce [6] di `scholler2020`, che lo indica come fonte dei dati ETH). Testo non letto.
Usata per: «Prova da camere fisse dall'alto (ETH/UCY, 2020)» — `f2/01-traduzione/SCHEDE.md` (`ricercatore-2`, rischi).
Note: nei file è solo la sigla «ETH». Il «2020» della scheda è l'anno dell'articolo di Schöller, non dei dati (2009).

### plastropoulos2026 [76]
Tipo: articolo scientifico
Autori: A. Plastropoulos, N. P. Avdelidis, A. Zolotas
Titolo: Techno-economic analysis for smart hangar inspection operations through sensing and localisation at scale
Sede e anno: The Aeronautical Journal, vol. 130, n. 1346, pp. 1037–1067, aprile 2026 (in linea 22-12-2025)
Identificativo: DOI 10.1017/aer.2025.10116
Link: https://www.cambridge.org/core/product/288076BC0C6F624BBBBD0A752587762E/core-reader
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-1) dati bibliografici su Crossref [g]; pagina dell'articolo aperta [r, primi 100 000 caratteri]: «no studies have presented a holistic side-by-side evaluation of MoCap, UWB and vision-based solutions»; «little empirical evidence on their robustness to the full spectrum of hangar-specific challenges such as dynamic occlusion».
Usata per: F25: negli hangar manca un confronto fra soluzioni e manca evidenza sulla robustezza all'occlusione dinamica — `f1/3fff79e9c3ea/FONTI.md`, `f1/3fff79e9c3ea/CONSEGNA.md` (§1.8)
Note: riguarda la localizzazione in hangar, non il monitoraggio di persone: il trasferimento è del ruolo. Pagine aggiunte oggi.

### postnikov2021 [77]
Tipo: articolo scientifico (prestampa)
Autori: Aleksey Postnikov; Aleksander Gamayunov; Gonzalo Ferrer
Titolo: CovarianceNet: Conditional Generative Model for Correct Covariance Prediction in Human Motion Prediction
Sede e anno: arXiv, 7-9-2021; sede di pubblicazione: manca
Identificativo: arXiv:2109.02965
Link: https://arxiv.org/abs/2109.02965
Verifica: verificata dal curatore il 14-11-2026 in parte — (rif-4) [API] solo per esistenza, autori e titolo
Usata per: citata come pista, senza affermazione — `f8-continuita/07-ricercatore/FONTI.md` (riga di S3, marca R) **[f7–f10: non vagliato dall'arbitro]**
Note: nessun dato ne dipende. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### qiu2023 [78]
Tipo: articolo scientifico
Autori: Z. Qiu, J. Martínez-Sánchez, P. Arias
Titolo: Evaluation and comparison of different time of flight cameras for outdoor applications
Sede e anno: ISPRS Annals of the Photogrammetry, Remote Sensing and Spatial Information Sciences, X-1/W1-2023, pp. 17–23, 2023 (pubblicato il 5-12-2023)
Identificativo: DOI 10.5194/isprs-annals-X-1-W1-2023-17-2023
Link: https://isprs-annals.copernicus.org/articles/X-1-W1-2023/17/2023/
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-1) già verificata dal curatore in f3 [g]. Ricontrollata oggi su Crossref [g]: autori, pagine, e nel riassunto «their outdoor applications remain limited, mainly due to challenges like sunlight interference»; prove su Azure Kinect e Pmd Monstar.
Usata per: F5: l'uso esterno del ToF resta limitato dall'interferenza solare — `f1/3fff79e9c3ea/FONTI.md`, `f1/3fff79e9c3ea/CONSEGNA.md` (§1.2, §3)
Usata per: «al sole l'iToF è limitato» — `f1/c85dbcc51ea6/CONSEGNA.md` (rif. [9])
Note: è una prova su due camere e tre casi ad alta riflettività, non una rassegna (FONTI.md la chiama «rassegna» nella consegna: impreciso).

### rahaman2026 [79]
Tipo: articolo scientifico (prestampa)
Autori: Kaizer Rahaman; Jyotirmoy V. Deshmukh; Ashish R. Hota; Lars Lindemann
Titolo: When Environments Shift: Safe Planning with Generative Priors and Robust Conformal Prediction
Sede e anno: arXiv, 13-2-2026; sede: manca
Identificativo: arXiv:2602.12616
Link: https://arxiv.org/abs/2602.12616
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-4) [API]: esiste; «ORCA» e «distribution shift» presenti nel riassunto
Usata per: pista sulla conforme robusta sotto cambio di distribuzione — `f8-continuita/07-ricercatore/FONTI.md` (§2, marca R) **[f7–f10: non vagliato dall'arbitro]**
Note: nessun dato ne dipende. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### ravi2024 [80]
Tipo: articolo scientifico (prestampa)
Autori: Nikhila Ravi, Valentin Gabeur, Yuan-Ting Hu, Ronghang Hu, Chaitanya Ryali, Tengyu Ma, Haitham Khedr, Roman Rädle, Chloe Rolland, Laura Gustafson, Eric Mintun, Junting Pan, Kalyan Vasudev Alwala, Nicolas Carion, Chao-Yuan Wu, Ross Girshick, Piotr Dollár, Christoph Feichtenhofer
Titolo: SAM 2: Segment Anything in Images and Videos
Sede e anno: arXiv, v1 01-08-2024, v2 28-10-2024; sede a stampa: non controllata
Identificativo: arXiv:2408.00714
Link: https://arxiv.org/abs/2408.00714 ; anche (rif-1): https://raw.githubusercontent.com/facebookresearch/sam2/main/LICENSE
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-1) [g]: registro arXiv aperto; nel riassunto «a simple transformer architecture with streaming memory for real-time video processing»; nessun FPS né hardware nel riassunto. Licenza del deposito: «Apache License Version 2.0» [g]. ‖ (rif-2) per i soli dati bibliografici (pagina arXiv). Testo non letto.
Usata per: F17: «streaming memory for real-time video processing»; licenza segnata [M] non verificata — `f1/3fff79e9c3ea/FONTI.md`; P2(b) «i 30-44 FPS di SAM 2 sono su GPU da datacenter» — `f1/3fff79e9c3ea/PREVISIONI.md`
Usata per: «SAM 2 e trasformatori di visione solo in asincrono (classe, riaggancio), mai a decidere un allarme» — `f2/01-traduzione/SCHEDE.md` (`ricercatore-2`).
Note: (rif-1) la licenza [M] di FONTI.md si chiude: Apache 2.0 per il codice. I «30–44 FPS su A100» della previsione P2(b) vengono dalla memoria del ruolo: non verificati (non sono nel riassunto). (rif-2) solo nominato nei file; nessuna cifra citata. Differenza fra i gruppi: rif-1 elencava 12 autori «e altri 6»; l'elenco completo dei 18 è di rif-2. La licenza Apache 2.0 del deposito è stata letta da rif-1.

### ristic2013 [81]
Tipo: articolo scientifico (metodo)
Autori: Ristic, Vo, Vo, Farina (cognomi dal registro Crossref; nomi non verificati)
Titolo: A Tutorial on Bernoulli Filters: Theory, Implementation and Applications
Sede e anno: IEEE Transactions on Signal Processing, vol. 61, n. 13, pp. 3406–3430, luglio 2013
Identificativo: DOI 10.1109/TSP.2013.2257765
Link: https://doi.org/10.1109/TSP.2013.2257765
Verifica: verificata dal curatore il 14-11-2026 in parte — (rif-2) per i soli dati bibliografici (registro Crossref). Testo non letto.
Usata per: «filtro di Bernoulli, circa 200 particelle per traccia in volo cieco» — `f2/01-traduzione/SCHEDE.md` (`tracciamento-2`); H-015 nel torneo — `f2/04-torneo/TORNEO.md` (parte 3).
Note: i file nominano il metodo senza fonte; questo è il riferimento d'uso corrente, proposto da me. Che l'autore dell'idea avesse in mente questo testo: non verificato.

### romlay2021 [82]
Tipo: articolo scientifico (rassegna)
Autori: Muhammad Rabani Mohd Romlay, Siti Fauziah Toha, Azhar Mohd Ibrahim, Ibrahim Venkat
Titolo: Methodologies and evaluation of electronic travel aids for the visually impaired people: a review
Sede e anno: Bulletin of Electrical Engineering and Informatics, vol. 10(3), pp. 1747–1758, giugno 2021
Identificativo: DOI 10.11591/eei.v10i3.3055
Link: https://beei.org/index.php/EEI/article/view/3055
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-1) già verificata dal curatore in f3 [r] (anno non letto). Completata oggi [g] su Crossref: anno, pagine, e nel riassunto «From 70 selected research articles, 51.4% accounts for simulation evaluation, 24.3% involve blindfolded-sighted humans, 22.9% involve visually impaired people and only 1.4% makes it into production and commercialization».
Usata per: F9: rassegna di 70 articoli; valutazioni con persone con disabilità visiva solo nel 22,9 %; l'1,4 % arriva alla produzione — `f1/3fff79e9c3ea/FONTI.md`, `f1/3fff79e9c3ea/CONSEGNA.md` (§1.7)
Note: nessuna

### rossi2025 [83]
Tipo: articolo scientifico (citato come prestampa; ora pubblicato)
Autori: Pierluigi Rossi, Elisa Cioccolo, Maurizio Cutini, Danilo Monarca, Daniele Puri, Davide Gattamelata, Leonardo Vita
Titolo: Outdoor Characterization and Geometry-Aware Error Modelling of an RGB-D Stereo Camera for Safety-Related Obstacle Detection
Sede e anno: prestampa su Preprints.org, 7 novembre 2025; poi Sensors 25(24), articolo 7495, 9 dicembre 2025 (MDPI)
Identificativo: DOI 10.20944/preprints202511.0498.v1 (prestampa); DOI 10.3390/s25247495 (articolo)
Link: https://www.preprints.org/manuscript/202511.0498
Verifica: dato diverso — (rif-3) la pagina non è raggiungibile (403); autori, titolo, date e riassunto letti nel registro Crossref [m], che dichiara la prestampa «is-preprint-of» dell'articolo su Sensors. Nel riassunto «prestazioni imprevedibili» non c'è: c'è che le prestazioni all'aperto a media e lunga distanza restano «weakly quantified», con prove fra 4 e 16 m su una D455 e un modello che predice l'errore di profondità con RMSE 0,46–0,64 m e MAE 0,40–0,51 m. Il ruolo che la cita l'aveva vista solo in un risultato di ricerca.
Usata per: stereo attiva (D455) all'aperto con luce forte: «un preprint del 2025 trova prestazioni imprevedibili» — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §2(b), S14
Note: correzione 6. Da citare come articolo su Sensors. La parola «imprevedibili» resta non verificata finché qualcuno non legge il testo intero; il riassunto sostiene un'affermazione più debole e più utile: errori dell'ordine del mezzo metro fra 4 e 16 m, cioè oltre la zona del nucleo (fino a 3 m).

### scholl1999 [84]
Tipo: articolo scientifico
Autori: Brian J. Scholl; Zenon W. Pylyshyn
Titolo: Tracking Multiple Items Through Occlusion: Clues to Visual Objecthood
Sede e anno: Cognitive Psychology 38(2):259–290, 1999
Identificativo: DOI 10.1006/cogp.1998.0698
Link: https://ruccs.rutgers.edu/images/tech_rpt/tr-40/scholl.pdf (404 oggi); https://doi.org/10.1006/cogp.1998.0698
Verifica: verificata dal curatore il 14-11-2026 in parte — (rif-4) [API] solo per i dati bibliografici; il link citato non è raggiungibile (404) e l'affermazione non è verificata nel testo (il ruolo: solo riassunto)
Usata per: un oggetto resta «lo stesso» dietro un ostacolo solo se scompare e ricompare lungo un bordo fisso — `f8-continuita/06-visualizzatore/CONSEGNA.md` riga 46 **[f7–f10: non vagliato dall'arbitro]**
Note: sostituire il link con il DOI. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### scholler2020 [85]
Tipo: articolo scientifico
Autori: Christoph Schöller, Vincent Aravantinos, Florian Lay, Alois Knoll
Titolo: What the Constant Velocity Model Can Teach Us About Pedestrian Motion Prediction
Sede e anno: IEEE Robotics and Automation Letters, vol. 5, n. 2, pp. 1696–1703, aprile 2020 (presentato a ICRA 2020)
Identificativo: DOI 10.1109/LRA.2020.2969925; arXiv:1903.07933
Link: https://arxiv.org/abs/1903.07933
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-1) già verificata dal curatore in f3 [g]: Tabella I a 4,8 s (ADE/FDE in metri): velocità costante 0,39/0,83; RED 0,44/0,91; SR-LSTM 0,45/0,94; S-GAN 0,32/0,60. Ricontrollati oggi autori e commento di accettazione (arXiv [g]), volume, pagine e DOI (Crossref [g]). ‖ (rif-2) Pagina arXiv, registro Crossref e PDF intero (Tabella I, medie sui cinque scenari, previsione a 4,8 s, errore medio / finale in metri): velocità costante (OUR) 0,39 / 0,83; RED 0,44 / 0,91; SR-LSTM 0,45 / 0,94; S-GAN 0,32 / 0,60; velocità costante campionata (OUR-S) 0,28 / 0,56. Nel testo: «S-GAN and SoPhie were evaluated by drawing 20 samples and taking the predicted trajectories with minimum ADE and FDE». Già in f3/fonti. ‖ (rif-4) [API] per i dati bibliografici; già verificata dal curatore in f3 (F14, cifre della Tabella I trovate nel testo: `f3/fonti/FONTI_VERIFICATE.md`); cifre non rilette oggi
Usata per: F14: velocità costante 0,39/0,83 m contro 0,44/0,91 del miglior appreso deterministico e 0,32/0,60 di S-GAN a 20 campioni, media ETH/UCY a 4,8 s — `f1/3fff79e9c3ea/FONTI.md`, `f1/3fff79e9c3ea/CONSEGNA.md` (§1.4, ricercatore-2, §3), `f1/3fff79e9c3ea/PREVISIONI.md` (P2a: anche LSTM 0,99/2,08, SoPhie 0,54/1,15, velocità costante con campionamento 0,28/0,56)
Usata per: a 4,8 s, 0,39 / 0,83 m contro 0,44 / 0,91 del miglior appreso deterministico; 0,32 / 0,60 un generativo — `f2/01-traduzione/SCHEDE.md` (`ricercatore-2`, P2(a); coda, (b) 12).
Usata per: «fonti: 0,39/0,83 contro RED 0,44/0,91 confermati; S-GAN 0,32/0,60 sta sotto» — `f2/05-selezione/SELEZIONE.md` (riga H-011).
Usata per: la velocità costante regge contro RED e SR-LSTM; S-GAN «migliore di 20 campioni, non confrontabile (non riletto)» — `f3/H-012/01-scene-dinamiche/SOLUZIONE.md` §8.
Usata per: a 4,8 s velocità costante 0,39 / 0,83 m, miglior appreso deterministico 0,44 / 0,91, generativo a 20 campioni 0,32 / 0,60 — `f8-continuita/07-ricercatore/FONTI.md` (S7), `CONSEGNA.md` righe 56 e 93 **[f7–f10: non vagliato dall'arbitro]**
Note: (rif-1) camere fisse dall'alto, insiemi ETH/UCY (citati solo per nome: nessun riferimento nei file), lavoro del 2020: non dice niente della camera indossata. I valori LSTM, SoPhie e «con campionamento» non sono nell'elenco verificato da f3: aperti dal ruolo, non riletti dal curatore. (rif-2) completamento: OUR-S (0,28 / 0,56) sta sotto S-GAN a parità di valutazione; il «non riletto» si può togliere. Limiti: dati ETH e UCY, camere fisse dall'alto, pedoni in spazi aperti; orizzonte 4,8 s con 3,2 s di storia; errore medio di spostamento, non una regione di confidenza. Non dice niente sull'occlusione dietro un pannello né su un sensore indossato. (rif-4) pedoni in campo aperto, senza occlusione. All'unione: nel gruppo rif-1 la chiave era `schoeller2020`. Alcuni usi vengono dalle estensioni f7–f10: NON ancora vagliati dall'arbitro (marcati riga per riga).

### sciencedirect-s0926580524005867 [86]
Tipo: articolo scientifico (titolo e autori: mancano)
Autori: manca
Titolo: manca
Sede e anno: rivista con ISSN 0926-5805 (dal codice dell'articolo; a memoria «Automation in Construction»: non verificato), 2024
Identificativo: PII S0926580524005867
Link: https://www.sciencedirect.com/science/article/pii/S0926580524005867
Verifica: non raggiungibile — (rif-4) (403 oggi); dal ruolo: vista solo nel riassunto di un motore di ricerca
Usata per: la profondità delle camere RGB-D in polvere è «heavily distorted» — `f7-estensione/05-esperto-dominio/CONSEGNA.md` righe 35 e 80 (S12, marca R) **[f7–f10: non vagliato dall'arbitro]**
Note: non citabile finché non si leggono titolo, autori e frase. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### shan2022 [87]
Tipo: articolo scientifico (prestampa)
Autori: Mao Shan, Karan Narula, Stewart Worrall, Yung Fei Wong, Julie Stephany Berrio Perez, Paul Gray, Eduardo Nebot
Titolo: A Novel Probabilistic V2X Data Fusion Framework for Cooperative Perception
Sede e anno: prestampa arXiv, una sola versione del 31 marzo 2022; sede pubblicata: non indicata nella pagina, non verificata
Identificativo: arXiv:2203.16964; DOI 10.48550/arXiv.2203.16964
Link: https://arxiv.org/pdf/2203.16964
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-3) [g, sul testo del PDF] — «the covariance intersection (CI) algorithm [8]», «fusing tracks information from two or more sources without knowing the cross-correlation information between them». Il riassunto non nomina il metodo, dice solo «considers the presence of cross-correlation». Il ruolo che la cita l'aveva vista solo in un risultato di ricerca.
Usata per: scambio di tracce fra veicoli con correlazioni ignote: intersezione delle covarianze — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §5, S36
Usata per: fusione prudente fra più veicoli (tappa 3 degli sviluppi) — `f6-specializzazione/01-esperto-dominio/SPECIALIZZAZIONE.md` §5
Note: correzione 14: è un'applicazione del metodo, non la sua fonte originale (il suo riferimento [8], non verificato da me).

### shan2025 [88]
Tipo: articolo scientifico (rassegna)
Autori: Jingfeng Shan, Lapo Miccinesi, Alessandra Beni, Lorenzo Pagnini, Andrea Cioncolini, Massimiliano Pieraccini
Titolo: A Review of Foreign Object Debris Detection on Airport Runways: Sensors and Algorithms
Sede e anno: Remote Sensing (MDPI), vol. 17(2), articolo 225, 2025 (9-1-2025)
Identificativo: DOI 10.3390/rs17020225
Link: https://www.mdpi.com/2072-4292/17/2/225/htm
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-1) [g]: Crossref aperto; nel riassunto «challenges such as limited datasets and high computational demands persist». La pagina MDPI dà 403.
Usata per: F28: rilevamento di detriti sulle piste: pochi dati, calcolo pesante — `f1/3fff79e9c3ea/FONTI.md`
Note: la frase riguarda gli approcci con intelligenza artificiale, non tutti i metodi. Citata in FONTI.md ma non usata nella consegna.

### skoglar2012 [89]
Tipo: articolo scientifico
Autori: Per Skoglar; Umut Orguner; David Törnqvist; Fredrik Gustafsson
Titolo: Pedestrian tracking with an infrared sensor using road network information
Sede e anno: EURASIP Journal on Advances in Signal Processing, 2012, articolo 26
Identificativo: DOI 10.1186/1687-6180-2012-26
Link: https://doi.org/10.1186/1687-6180-2012-26
Verifica: verificata dal curatore il 14-11-2026 in parte — (rif-4) [API] solo per esistenza e dati bibliografici; che tratti l'evidenza negativa: non verificata (testo non letto, né da me né dal ruolo)
Usata per: evidenza negativa nei filtri — `f8-continuita/07-ricercatore/FONTI.md` (S22, marca R), `CONSEGNA.md` riga 18 **[f7–f10: non vagliato dall'arbitro]**
Note: correzione C7. Non usare come sostegno finché il testo non è letto. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### standley2017 [90]
Tipo: articolo scientifico
Autori: Trevor Standley, Ozan Sener, Dawn Chen, Silvio Savarese
Titolo: image2mass: Estimating the Mass of an Object from Its Image
Sede e anno: Proceedings of the 1st Annual Conference on Robot Learning (CoRL), Proceedings of Machine Learning Research, vol. 78, pp. 324–333, 2017
Identificativo: PMLR v78 (standley17a); DOI: manca
Link: https://proceedings.mlr.press/v78/standley17a.html
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-1) dati bibliografici dalla pagina PMLR [r]; nel PDF [g]: «We obtain the product information for ∼3 million Amazon…» e «…we produce a dataset with ∼150k products that have highly accurate mass and size information».
Usata per: F30: image2mass, circa 150 000 prodotti Amazon (articolo non aperto dal ruolo) — `f1/3fff79e9c3ea/FONTI.md`; riferimento del 2017 per la massa — `f1/3fff79e9c3ea/CONSEGNA.md` (§1.3)
Note: nei file mancavano autori, titolo e sede. L'errore 1,066 attribuito a image2mass viene da `lee2026` (Tabella 1), non da questo articolo.

### starr2016 [91]
Tipo: altro (tesi di dottorato)
Autori: Joseph Wesley Starr
Titolo: Rangefinding in Fire Smoke Environments
Sede e anno: Virginia Polytechnic Institute and State University, tesi di dottorato in ingegneria meccanica, 7-1-2016
Identificativo: manca (scheda VTechWorks d7fdffcf-494d-40bb-a54a-6315de467ef3)
Link: https://vtechworks.lib.vt.edu/items/d7fdffcf-494d-40bb-a54a-6315de467ef3/full
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-4) [T]: nel riassunto «…the ability of LWIR stereo vision to rangefind in dense smoke when LIDAR and visual stereo vision fail»
Usata per: in fumo denso LiDAR e stereo visibile falliscono, radar e infrarosso termico reggono — `f7-estensione/05-esperto-dominio/CONSEGNA.md` righe 35 e 80 (S11) **[f7–f10: non vagliato dall'arbitro]**
Note: fumo d'incendio, non nebbia; nessuna misura sullo stereo attivo a infrarossi (lo dice il ruolo). Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### stone1975 [92]
Tipo: altro (libro)
Autori: Lawrence D. Stone
Titolo: Theory of Optimal Search
Sede e anno: Academic Press, 1975 (dati a memoria e da f3: non verificati oggi)
Identificativo: manca
Link: manca
Verifica: non verificata — (rif-1) (non aperto né in f3 né oggi; f3 lo nomina come la fonte primaria a cui rimanda Wikipedia).
Usata per: fonte primaria della ricerca bayesiana, citata indirettamente — `f3/fonti/FONTI_VERIFICATE.md` (riga «Ricerca bayesiana»)
Note: nessun ruolo di f1 lo cita direttamente.

### sun2022 [93]
Tipo: articolo scientifico e insieme di dati
Autori: Peize Sun, Jinkun Cao, Yi Jiang, Zehuan Yuan, Song Bai, Kris Kitani, Ping Luo
Titolo: DanceTrack: Multi-Object Tracking in Uniform Appearance and Diverse Motion
Sede e anno: IEEE/CVF CVPR 2022, pp. 20961–20970
Identificativo: DOI 10.1109/CVPR52688.2022.02032; arXiv 2111.14690
Link: https://arxiv.org/abs/2111.14690
Verifica: verificata dal curatore il 14-11-2026 in parte — (rif-1) solo nei dati bibliografici [g] (arXiv e Crossref): esiste con questi autori, titolo e sede. Nessuna cifra è citata da questa fonte.
Usata per: insieme di dati su cui sono valutati i tracciatori appresi di fine corsa («MATR su DanceTrack») — `f1/992c41c8860e/CONSEGNA.md` (§1.4)
Note: licenza dell'insieme di dati non controllata.

### thipphavong2016 [94]
Tipo: articolo scientifico (rapporto tecnico della NASA)
Autori: David Thipphavong; Andrew Cone; Chunki Park; Seung Man Lee; Confesor Santiago
Titolo: Defining the Collision Avoidance Region for DAA Systems
Sede e anno: NASA Ames Research Center, documento per il comitato SC-228 (dall'intestazione), 12 agosto 2016; tipo di documento nel registro NTRS: «Other»
Identificativo: NTRS 20160010603; numero di rapporto ARC-E-DAA-TN35178
Link: https://ntrs.nasa.gov/api/citations/20160010603/downloads/20160010603.pdf ; registro: https://ntrs.nasa.gov/api/citations/20160010603
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (unione, 16:45) scheda del registro NTRS e PDF scaricati; titolo, autori, data e numero di rapporto dalla scheda; nel testo del PDF [g]: «A buffer of about 0.09 NM was added to the well clear DMOD and HMD* thresholds of 4000 ft to model what a DAA system might use to guard against the effects of uncertainty» e, per l'avviso «DAA Warning», «τ*mod = 35 sec, DMOD = 0.75 NM, HMD = 0.75 NM, and h = 450 ft». Aperta anche dal ruolo che la cita (pagine 1–4). Non era in nessuno dei quattro elenchi parziali: trovata dal controllo di completezza sui link.
Usata per: in uno studio NASA per lo standard «rilevare ed evitare», τ_mod < 35 s e distanza orizzontale minima < 0,75 miglia, con 0,09 miglia aggiunte «per l'incertezza»: la pratica vera è una soglia su tempo e distanza con un margine — `f9-preproposta/03-kalman/CONSEGNA.md` riga 40 **[f7–f10: non vagliato dall'arbitro]**
Note: Le soglie sono quelle dell'avviso «DAA Warning» usate in questo studio (simulazione senza manovre), non il testo di una norma; le miglia sono nautiche (0,75 NM ≈ 1,39 km; 4000 ft ≈ 1,22 km). È una fonte aperta per l'ordine di grandezza «35 s e oltre un chilometro» che il quadro di dominio (S20) appoggia a `rtca-do-365` senza una fonte letta: il collegamento è una proposta del curatore, il quadro non la cita. Citata solo nelle estensioni f7–f10: NON ancora vagliata dall'arbitro.

### timans2024 [95]
Tipo: articolo scientifico
Autori: Alexander Timans, Christoph-Nikolas Straehle, Kaspar Sakmann, Eric Nalisnick
Titolo: Adaptive Bounding Box Uncertainties via Two-Step Conformal Prediction
Sede e anno: Computer Vision – ECCV 2024, Lecture Notes in Computer Science, Springer, pp. 363–398 (in linea 8-11-2024)
Identificativo: DOI 10.1007/978-3-031-73223-2_21; arXiv 2403.07263
Link: https://arxiv.org/pdf/2403.07263
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-1) [g]: arXiv e Crossref; nel riassunto «a novel two-step conformal approach that propagates uncertainty in predicted class labels into the uncertainty intervals of bounding boxes».
Usata per: F24: previsione conforme a due passi per i riquadri di rilevamento — `f1/3fff79e9c3ea/FONTI.md`
Note: citata come pista, senza cifre. In f3: solo dati bibliografici.

### tokmakov2021 [96]
Tipo: articolo scientifico
Autori: Pavel Tokmakov; Jie Li; Wolfram Burgard; Adrien Gaidon
Titolo: Learning to Track with Object Permanence
Sede e anno: IEEE/CVF ICCV 2021, pp. 10840–10849
Identificativo: DOI 10.1109/ICCV48922.2021.01068; arXiv:2103.14258
Link: https://arxiv.org/abs/2103.14258
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-4) [API]: sede ICCV 2021 confermata (nel file era «a memoria»); «ground truth annotations for invisible objects» presente nel riassunto
Usata per: la verità in occlusione esiste in dati sintetici — `f8-continuita/07-ricercatore/FONTI.md` (S11), `CONSEGNA.md` riga 65, `PREVISIONI.md` riga 68 **[f7–f10: non vagliato dall'arbitro]**
Note: Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### uhlemann2024 [97]
Tipo: articolo scientifico
Autori: Nico Uhlemann; Felix Fent; Markus Lienkamp
Titolo: Evaluating Pedestrian Trajectory Prediction Methods with Respect to Autonomous Driving
Sede e anno: IEEE Transactions on Intelligent Transportation Systems, 2024 (volume e pagine: non letti); arXiv v3 5-4-2024
Identificativo: DOI 10.1109/TITS.2024.3386195; arXiv:2308.05194
Link: https://arxiv.org/abs/2308.05194
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-4) [API]: frase «a constant velocity model (CVM) provides a good approximation of the overall dynamics in the majority of cases» presente nel riassunto
Usata per: la velocità costante è una buona approssimazione nella maggior parte dei casi — `f8-continuita/07-ricercatore/FONTI.md` (S8), `CONSEGNA.md` riga 56 **[f7–f10: non vagliato dall'arbitro]**
Note: nessun numero citato. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### usenko2017 [98]
Tipo: articolo scientifico
Autori: Vladyslav Usenko; Lukas von Stumberg; Andrej Pangercic; Daniel Cremers
Titolo: Real-Time Trajectory Replanning for MAVs using Uniform B-splines and a 3D Circular Buffer
Sede e anno: IEEE/RSJ IROS 2017, pp. 215–222
Identificativo: DOI 10.1109/IROS.2017.8202160; arXiv:1703.01416
Link: https://arxiv.org/abs/1703.01416
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-4) [API]: «an occupancy grid stored in a three-dimensional circular buffer, which moves together with a drone» presente nel riassunto
Usata per: nel volo la mappa locale tipica è una griglia densa che scorre con il veicolo — `f7-estensione/05-esperto-dominio/CONSEGNA.md` righe 17 e 80 (S7) **[f7–f10: non vagliato dall'arbitro]**
Note: Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### vanhoorick2023 [99]
Tipo: articolo scientifico
Autori: Basile Van Hoorick; Pavel Tokmakov; Simon Stent; Jie Li; Carl Vondrick
Titolo: Tracking Through Containers and Occluders in the Wild
Sede e anno: IEEE/CVF CVPR 2023, pp. 13802–13812
Identificativo: DOI 10.1109/CVPR52729.2023.01326; arXiv:2305.03052
Link: https://arxiv.org/abs/2305.03052
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-4) [API]: «a considerable performance gap» presente nel riassunto
Usata per: resta un divario notevole prima di una vera permanenza dell'oggetto — `f8-continuita/07-ricercatore/FONTI.md` (S14), `CONSEGNA.md` riga 62 **[f7–f10: non vagliato dall'arbitro]**
Note: Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### vriend2025 [100]
Tipo: articolo scientifico
Autori: Sita Vriend; David Hägele; Daniel Weiskopf
Titolo: Two Empirical Studies on Audiovisual Semiotics of Uncertainty
Sede e anno: Audio Mostly 2025 (dal commento arXiv); arXiv 20-5-2025
Identificativo: arXiv:2505.14379
Link: https://arxiv.org/abs/2505.14379
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-4) [API]: nel riassunto «while pitch paired with brightness was preferred as a pair, it was not well suited as a mapping for uncertainty»; «volume e nitidezza i più intuitivi» NON è nel riassunto: non verificata (lo dice anche il ruolo)
Usata per: l'accoppiata altezza–luminosità piace ma non è adatta all'incertezza — `f8-continuita/06-visualizzatore/CONSEGNA.md` riga 48 **[f7–f10: non vagliato dall'arbitro]**
Note: studi con partecipanti reclutati in rete, non con persone non vedenti. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### weitz2013 [101]
Tipo: altro (rapporto DLR, secondo il ruolo)
Autori: Weitz (nome: manca)
Titolo: manca
Sede e anno: 2013, DLR
Identificativo: manca
Link: manca
Verifica: vista solo nel riassunto di un motore di ricerca — (rif-4) (dal ruolo); non cercata da me: dati insufficienti
Usata per: ellissoidi d'incertezza per traiettorie 4D, senza esperimento con controllori — `f8-continuita/07-ricercatore/FONTI.md` (§5, marca R) **[f7–f10: non vagliato dall'arbitro]**
Note: non citabile così com'è. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### weng2020 [102]
Tipo: articolo scientifico
Autori: Xinshuo Weng, Jianren Wang, David Held, Kris Kitani
Titolo: 3D Multi-Object Tracking: A Baseline and New Evaluation Metrics (riassunto esteso su arXiv: «AB3DMOT: A Baseline for 3D Multi-Object Tracking and New Evaluation Metrics»)
Sede e anno: IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS) 2020, pp. 10359–10366; il riassunto esteso arXiv 2008.08063 è per i Workshop di ECCV 2020
Identificativo: DOI 10.1109/IROS45743.2020.9341164; arXiv 2008.08063 (riassunto esteso)
Link: https://arxiv.org/abs/2008.08063
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-1) già verificata dal curatore in f3 [g], con correzione di attribuzione. Ricontrollati oggi: riassunto arXiv «a straightforward combination of a 3D Kalman filter and the Hungarian algorithm» [g]; pagine e DOI su Crossref [g].
Usata per: «lo schema da copiare è AB3DMOT, Kalman 3D più ungherese» — `f1/992c41c8860e/CONSEGNA.md` (§1.4)
Note: citare l'articolo IROS, non il riassunto esteso.

### williams1978 [103]
Tipo: articolo scientifico
Autori: Lance Williams
Titolo: Casting Curved Shadows on Curved Surfaces
Sede e anno: ACM SIGGRAPH Computer Graphics 12(3):270–274, 1978 (SIGGRAPH '78)
Identificativo: DOI 10.1145/965139.807402
Link: https://history.siggraph.org/?p=120268
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-4) [API] e [T]: pagina dell'archivio aperta, titolo e autore presenti
Usata per: la mappa d'ombra della grafica come analogia («il sensore è la lampada») — `f7-estensione/08-creativo/CONSEGNA.md` riga 51 **[f7–f10: non vagliato dall'arbitro]**
Note: analogia, nessuna cifra. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### wyffels2015 [104]
Tipo: articolo scientifico
Autori: Kevin Wyffels; Mark Campbell
Titolo: Negative Information for Occlusion Reasoning in Dynamic Extended Multiobject Tracking
Sede e anno: IEEE Transactions on Robotics 31(2):425–442, 2015
Identificativo: DOI 10.1109/TRO.2015.2409413
Link: https://doi.org/10.1109/TRO.2015.2409413
Verifica: verificata dal curatore il 14-11-2026 in parte — (rif-4) [API] solo per esistenza e dati bibliografici (in `FONTI.md` mancavano titolo e DOI); testo non letto
Usata per: evidenza negativa nei filtri — `f8-continuita/07-ricercatore/FONTI.md` (S22, marca R) **[f7–f10: non vagliato dall'arbitro]**
Note: il titolo è pertinente; nessuna cifra citata. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### xu2023 [105]
Tipo: articolo scientifico (rassegna sistematica)
Autori: Peijie Xu, Gerard A. Kennedy, Fei-Yi Zhao, Wen-Jing Zhang, Ron Van Schyndel
Titolo: Wearable Obstacle Avoidance Electronic Travel Aids for Blind and Visually Impaired Individuals: A Systematic Review
Sede e anno: IEEE Access, vol. 11, pp. 66587–66613, 2023
Identificativo: DOI 10.1109/ACCESS.2023.3285396
Link: https://doaj.org/article/69f50f5aa56e4c9fb3f54d8d3d05cf83 (403 allo strumento di lettura; letto il registro DOAJ)
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-1) [g]: Crossref e registro DOAJ aperti; nel riassunto «The PRISMA 2020 and APISSER guidelines were followed», «Eighty-nine studies were included for analysis», «According to user experience, the efficacy and safety of the device was usually their primary concern».
Usata per: F10: rassegna PRISMA di 89 studi; efficacia e sicurezza sono la prima preoccupazione degli utenti — `f1/3fff79e9c3ea/FONTI.md`
Note: in f3 non controllata. Letto il riassunto, non il testo.

### yang2024 [106]
Tipo: articolo scientifico (prestampa) e deposito di codice
Autori: Cheng-Yen Yang, Hsiang-Wei Huang, Wenhao Chai, Zhongyu Jiang, Jenq-Neng Hwang
Titolo: SAMURAI: Adapting Segment Anything Model for Zero-Shot Visual Tracking with Motion-Aware Memory
Sede e anno: arXiv, v1 18-11-2024, v2 30-11-2024; sede a stampa: manca (non trovata su Crossref oggi)
Identificativo: arXiv 2411.11922
Link: https://arxiv.org/abs/2411.11922 ; https://github.com/yangchris11/samurai
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-1) già verificata dal curatore in f3 [g]: il Kalman sceglie la maschera (testo); Apache-2.0; «The existing code doesn't support live/streaming video». Ricontrollati oggi su arXiv [g] titolo, autori e date. ‖ (rif-2) Pagina arXiv (autori, titolo) e README del deposito: «Does SAMURAI support streaming input (e.g. webcam)? Not yet. The existing code doesn't support live/streaming video». Già in f3/fonti.
Usata per: la posizione prevista dal Kalman sceglie la maschera dentro SAM 2 (unica freccia sensata dal Kalman alla rete) — `f1/c85dbcc51ea6/CONSEGNA.md` (§1.1, rif. [1])
Usata per: F19: Apache-2.0; il codice non accetta flussi dal vivo — `f1/3fff79e9c3ea/FONTI.md`, `f1/3fff79e9c3ea/CONSEGNA.md` (§1.5), `f1/3fff79e9c3ea/PREVISIONI.md` (P2b)
Usata per: «SAMURAI non lavora su video dal vivo» — `f3/H-012/01-scene-dinamiche/SOLUZIONE.md` §8; `f4/H-012/05-correzioni/SOLUZIONE_V2.md` §8.
Note: (rif-1) prestampa, non rivista fra pari per quanto verificato. (rif-2) il limite è del codice pubblicato («not yet»), non del metodo: può cambiare. La licenza del deposito oggi non l'ho riletta (Apache-2.0 secondo f3).

### yang2025 [107]
Tipo: articolo scientifico (prestampa)
Autori: Xu Yang, Gady Agam
Titolo: Motion-Aware Transformer for Multi-Object Tracking
Sede e anno: arXiv, v1 26-9-2025 (tre versioni); sede a stampa: manca
Identificativo: arXiv 2509.21715
Link: https://arxiv.org/abs/2509.21715
Verifica: verificata dal curatore il 14-11-2026 in parte — (rif-1) [g], con riserva: `tracciamento` scrive solo «MATR», senza link; che intendesse questo articolo è un'identificazione mia (ricerca per nome). Registro arXiv aperto: su DanceTrack 71,3 HOTA con dati supplementari, oltre 9 punti sopra MOTR senza dati aggiuntivi.
Usata per: «i tracciatori appresi di fine corsa (es. MATR su DanceTrack) chiedono addestramento: prestazioni attuali non verificate» — `f1/992c41c8860e/CONSEGNA.md` (§1.4)
Note: l'attribuzione va confermata dal ruolo. Che il metodo «chieda addestramento» è coerente col riassunto (modello DETR addestrato), non una frase letta.

### yao2025 [108]
Tipo: articolo scientifico
Autori: Jianpeng Yao; Xiaopan Zhang; Yu Xia; Zejin Wang; Amit K. Roy-Chowdhury; Jiachen Li
Titolo: Towards Generalizable Safety in Crowd Navigation via Conformal Uncertainty Handling
Sede e anno: 9th Conference on Robot Learning (CoRL 2025), secondo il commento arXiv; arXiv 7-8-2025
Identificativo: arXiv:2508.05634
Link: https://arxiv.org/abs/2508.05634
Verifica: verificata dal curatore il 14-11-2026 in parte — (rif-4) [API] solo per esistenza, autori, titolo
Usata per: pista sulla conforme adattiva nella navigazione fra la folla — `f8-continuita/07-ricercatore/FONTI.md` (§2, marca R) **[f7–f10: non vagliato dall'arbitro]**
Note: nessun dato ne dipende. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### zhang2019 [109]
Tipo: articolo scientifico
Autori: Pu Zhang, Wanli Ouyang, Pengfei Zhang, Jianru Xue, Nanning Zheng
Titolo: SR-LSTM: State Refinement for LSTM towards Pedestrian Trajectory Prediction
Sede e anno: IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR) 2019, pp. 12077–12086
Identificativo: DOI 10.1109/CVPR.2019.01236; arXiv:1903.02793
Link: https://arxiv.org/abs/1903.02793
Verifica: verificata dal curatore il 14-11-2026 in parte — (rif-2) per i soli dati bibliografici (pagina arXiv, registro Crossref, voce [1] di `scholler2020`). Il testo non l'ho letto.
Usata per: «regge contro RED e SR-LSTM» (0,45 / 0,94 nella tabella di Schöller) — `f2/05-selezione/SELEZIONE.md` (riga H-011); `f3/H-012/01-scene-dinamiche/SOLUZIONE.md` §8.
Note: solo nominato nei file. Schöller e altri riportano per SR-LSTM i risultati dell'articolo originale.

### zhang2022 [110]
Tipo: articolo scientifico e deposito di codice
Autori: Yifu Zhang, Peize Sun, Yi Jiang, Dongdong Yu, Fucheng Weng, Zehuan Yuan, Ping Luo, Wenyu Liu, Xinggang Wang
Titolo: ByteTrack: Multi-Object Tracking by Associating Every Detection Box
Sede e anno: Computer Vision – ECCV 2022, Lecture Notes in Computer Science, Springer, pp. 1–21, 2022
Identificativo: DOI 10.1007/978-3-031-20047-2_1; arXiv:2110.06864
Link: https://arxiv.org/abs/2110.06864
Verifica: verificata dal curatore il 14-11-2026 in parte — (rif-2) per i soli dati bibliografici (pagina arXiv, registro Crossref). Il deposito (licenza MIT, «30 FPS… on a single V100 GPU») l'ha verificato il curatore in f3; oggi non l'ho riaperto.
Usata per: tracciatore «BoT-SORT o ByteTrack» nel percorso asincrono — `f2/01-traduzione/SCHEDE.md` (`visione-1`); associazione «tipo ByteTrack/OC-SORT» — `f2/01-traduzione/SCHEDE.md` (`ricercatore-1`).
Note: solo nominato nei file. Tracciatore su riquadri 2D nell'immagine, non sul piano del suolo.

### zhang2023 [111]
Tipo: articolo scientifico
Autori: Xiaoshuai Zhang; Rui Chen; Ang Li; Fanbo Xiang; Yuzhe Qin; Jiayuan Gu; Zhan Ling; Minghua Liu; Peiyu Zeng; Songfang Han; Zhiao Huang; Tongzhou Mu; Jing Xu; Hao Su
Titolo: Close the Optical Sensing Domain Gap by Physics-Grounded Active Stereo Sensor Simulation
Sede e anno: IEEE Transactions on Robotics (dal commento arXiv: «will appear»); volume, pagine, anno di stampa: non letti; arXiv 28-1-2022
Identificativo: arXiv:2201.11924
Link: https://arxiv.org/abs/2201.11924
Verifica: verificata dal curatore il 14-11-2026 in parte — (rif-4) [API] per autori, titolo e sede dichiarata
Usata per: SimSense e SAPIEN simulano lo stereo attivo ma chiedono CUDA o una GPU — `f10-dati/02-sensori/MODELLO_SENSORE.md` riga 68 **[f7–f10: non vagliato dall'arbitro]**
Note: la chiave porta l'anno presunto di stampa; da correggere quando si legge il DOI. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### zhang2026a [112]
Tipo: articolo scientifico (prestampa)
Autori: Bo Zhang, Zhuotao Tian, Xin Tao, Songlin Tang, Jun Yu, Wenjie Pei
Titolo: Amodal SAM: A Unified Amodal Segmentation Framework with Generalization
Sede e anno: arXiv, 22-4-2026; sede a stampa: manca
Identificativo: arXiv 2604.20748
Link: https://arxiv.org/abs/2604.20748
Verifica: dato diverso — (rif-1) [g] in parte: registro arXiv aperto; il riassunto dice «leverages SAM (Segment Anything Model) for both amodal image and amodal video segmentation». Dato diverso: «SAM 2» non compare nel riassunto.
Usata per: «…o derivato da SAM 2 [13]; tempi reali: non verificati» — `f1/c85dbcc51ea6/CONSEGNA.md` (§1.6)
Note: scrivere «derivato da SAM», oppure leggere il testo intero per sapere se la parte video usa SAM 2. All'unione: la chiave `zhang2026` era usata da due gruppi per due articoli diversi; questo (rif-1) diventa `zhang2026a`, l'altro `zhang2026b`.

### zhang2026b [113]
Tipo: articolo scientifico (prestampa)
Autori: Zhen Zhang; Amr Alanwar
Titolo: Hybrid Probabilistic Zonotopes for Identifiable and Refinable Predictive Uncertainty
Sede e anno: arXiv, 5-8-2026; sede: manca
Identificativo: arXiv:2608.05454
Link: https://arxiv.org/abs/2608.05454
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-4) [API] e [T]: nel testo HTML v1 «OOD coverage holds: 90.9% ETH/UCY leave-one-out average»; il livello nominale del 90 % e «non per orizzonte» non ricontrollati
Usata per: copertura media 90,9 % al nominale 90 %, una scena di ETH/UCY tenuta fuori a turno — `f8-continuita/07-ricercatore/FONTI.md` (§2, marca R) **[f7–f10: non vagliato dall'arbitro]**
Note: la cifra non è nel riassunto, solo nel corpo. All'unione: la chiave `zhang2026` era usata da due gruppi per due articoli diversi; questo (rif-4) diventa `zhang2026b`, l'altro `zhang2026a`. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### zholus2025 [114]
Tipo: articolo scientifico (prestampa)
Autori: Artem Zholus, Carl Doersch, Yi Yang, Skanda Koppula, Viorica Patraucean, Xu Owen He, Ignacio Rocco, Mehdi S. M. Sajjadi, Sarath Chandar, Ross Goroshin
Titolo: TAPNext: Tracking Any Point (TAP) as Next Token Prediction
Sede e anno: arXiv, v1 8-4-2025, v2 14-4-2025; sede a stampa: non controllata
Identificativo: arXiv 2504.05579
Link: https://arxiv.org/abs/2504.05579
Verifica: dato diverso — (rif-1) già verificata dal curatore in f3 [g], con correzione. Dato diverso: la Tabella 2 dà, con 1024 punti, 187 fps su H100 e 42 su V100 (TAPNext-B, latenza 5,33 ms su H100); «348 fps» non è nell'articolo. Ricontrollati oggi su arXiv [g] titolo e autori. ‖ (rif-2) Pagina arXiv e PDF, Tabella 2: TAPNext-B con 1024 punti, 187 fps su H100 e 42 su V100, latenza 5,33 ms e 23 ms; con 256 punti 197 e 70 fps. Già in f3/fonti.
Usata per: «TAPNext: 1024 punti a 348 fps, ma su H100» — `f1/c85dbcc51ea6/CONSEGNA.md` (§1.6, rif. [14])
Usata per: «TAPNext dà 187 fps su H100» — `f3/H-012/01-scene-dinamiche/SOLUZIONE.md` §8; `f4/H-012/05-correzioni/SOLUZIONE_V2.md` §8.
Note: (rif-1) la conclusione del ruolo (serve una GPU da centro di calcolo) non cambia; la cifra va corretta in 187 fps. (rif-2) «348 fps», circolato in f1, non è nell'articolo (correzione già fatta in f3). Segue punti, non oggetti; nessuna misura su CPU.

### zhou2025 [115]
Tipo: articolo scientifico e deposito di codice
Autori: Chong Zhou, Chenchen Zhu, Yunyang Xiong, Saksham Suri, Fanyi Xiao, Lemeng Wu, Raghuraman Krishnamoorthi, Bo Dai, Chen Change Loy, Vikas Chandra, Bilge Soran
Titolo: EdgeTAM: On-Device Track Anything Model
Sede e anno: IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR) 2025, pp. 13832–13842
Identificativo: DOI 10.1109/CVPR52734.2025.01291; arXiv 2501.07256
Link: https://arxiv.org/abs/2501.07256 ; https://github.com/facebookresearch/EdgeTAM
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-1) già verificata dal curatore in f3: 16 fps su iPhone 15 Pro Max [g]; Apache-2.0 [g]; SAM 2 minimo «around 1 FPS» [g]; 150,9 fps su A100 [r]. Ricontrollati oggi autori (arXiv [g]), pagine e DOI (Crossref [g]). ‖ (rif-2) Riassunto arXiv: «running at 16 FPS on iPhone 15 Pro Max»; README: «The EdgeTAM model checkpoints and code are licensed under Apache 2.0». Già in f3/fonti. Dato diverso: la sede «CVPR 2025» non compare né nella pagina arXiv né nel README letto oggi. ‖ All'unione (16:33): Crossref aperto sul DOI: «EdgeTAM: On-Device Track Anything Model», «2025 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)», pp. 13832–13842: la sede è confermata.
Usata per: F18: 16 FPS su iPhone 15 Pro Max, 150,9 su A100, Apache 2.0; SAM 2 piccolo circa 1 FPS sullo stesso telefono — `f1/3fff79e9c3ea/FONTI.md`, `f1/3fff79e9c3ea/CONSEGNA.md` (§1.5), `f1/3fff79e9c3ea/PREVISIONI.md` (P2b)
Usata per: «EdgeTAM: 16 fps su iPhone 15 Pro Max» — `f1/c85dbcc51ea6/CONSEGNA.md` (§1.2, rif. [6])
Usata per: «EdgeTAM (16 fps su iPhone 15 Pro Max, Apache 2.0) è il solo candidato leggero» — `f3/H-012/01-scene-dinamiche/SOLUZIONE.md` §8.
Note: (rif-1) nessuna misura su Jetson o CPU: non verificato (lo dichiarano i ruoli). (rif-2) i 16 fps sono su un telefono con acceleratore neurale, non su una CPU di portatile. Differenza fra i gruppi: rif-2 dava «CVPR 2025» come non confermato (non compare nella pagina arXiv né nel README); rif-1 l'aveva letto su Crossref; tenuto il dato di rif-1, riconfermato all'unione.


---

## 2. Schede tecniche e documenti dei costruttori (con le pagine dei rivenditori)

46 voci, da [116] a [161].

### adorama-d455 [116]
Tipo: pagina di costruttore o comunicato (rivenditore)
Autori: Adorama
Titolo: Intel RealSense D455 (pagina del rivenditore; titolo esatto: manca)
Sede e anno: adorama.com; data: manca
Identificativo: manca
Link: https://www.adorama.com/in82635dsd45.html
Verifica: non verificata — (rif-1) (non aperta né in f3 né oggi); letta dal ruolo attraverso uno strumento che riassume.
Usata per: D455 con otturatore globale su profondità e RGB — `f1/c85dbcc51ea6/CONSEGNA.md` (§1.7, rif. [17])
Note: il dato è confermato da una fonte migliore, `realsense-confronto-camere` (f3 [g]): citare quella.

### arducam-tof [117]
Tipo: pagina di costruttore o comunicato
Autori: Arducam
Titolo: Time-of-Flight Camera for Raspberry Pi (titolo esatto: manca)
Sede e anno: arducam.com; data: manca
Identificativo: manca
Link: https://www.arducam.com/product/time-of-flight-camera-for-raspberry-pi/ ; https://www.arducam.com/time-of-flight-camera-for-raspberry-pi.html
Verifica: non raggiungibile — (rif-1) (403 oggi); i ruoli l'hanno vista solo nel riassunto di un motore di ricerca.
Usata per: tre camere ToF 240×180 coprono circa 174° (campo dichiarato non verificato) — `f1/dfac83300259/CONSEGNA.md` (§1.1)
Usata per: «Arducam ToF sotto 70° (modello T2: 64°)» fra i 7 sensori di P1 — `f1/b8262bfed263/CONSEGNA.md` (requisiti-1)
Note: campo e risoluzione non verificati: i due usi poggiano su un riassunto di ricerca.

### botland-oak-d-lite [118]
Tipo: pagina di costruttore o comunicato (rivenditore)
Autori: Botland
Titolo: OAK-D Lite (pagina del rivenditore; titolo esatto: manca)
Sede e anno: botland.store; data: manca
Identificativo: manca
Link: https://botland.store/modules-smart-cameras/20955-oak-d-lite.html
Verifica: non verificata — (rif-1) (non aperta né in f3 né oggi).
Usata per: OAK-D Lite 73°×58°, data fuori produzione da un rivenditore europeo — `f1/985ccd9bca46/PREVISIONI.md` (P6)
Note: citata solo in PREVISIONI.md.

### flir-boson [119]
Tipo: pagina di costruttore o comunicato
Autori: Teledyne FLIR
Titolo: Boson (modulo termico a onda lunga)
Sede e anno: sito del costruttore, letto il 14-11-2026
Identificativo: manca
Link: https://www.oem.flir.com/products/boson/
Verifica: verificata dal curatore il 14-11-2026 in parte — (rif-3) in parte: pagina aperta [g]; ci sono «starting at 7.5 grams and <4.9 cm³», «Low power consumption, starting at 600 mW», «640 and 320 resolutions». Il valore «1 W» non c'è. Il ruolo che la cita l'aveva vista solo in un risultato di ricerca.
Usata per: termico (Boson 640): nucleo da 7,5 g, circa 0,6–1 W; dà la direzione, non la distanza — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §2(b), S17
Note: correzione 8. I 7,5 g e i 600 mW sono i valori minimi della famiglia («starting at»), non per forza quelli del modello 640.

### hilink-ld2410 [120]
Tipo: scheda tecnica (manuale del protocollo)
Autori: Hi-Link
Titolo: HLK-LD2410 Serial Communication Protocol, v1.02
Sede e anno: Hi-Link; copia su un sito di terzi
Identificativo: v1.02
Link: https://www.sudo.is/docs/esphome/components/ld2410/HLK-LD2410_Serial_Communication_Protocol_v1.02.pdf
Verifica: aperta dal ruolo che la cita — (rif-4) ([g], `pdftotext`); dal curatore solo [200]
Usata per: 256 000 baud predefiniti; nessun angolo in uscita; porte di distanza da 0,75 m — `f10-dati/04-embedded/PREVISIONI.md` (E9), `INVENTARIO_E_DECISIONE.md` riga 75 ([17]) **[f7–f10: non vagliato dall'arbitro]**
Note: copia non ufficiale. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### hilink-ld2450 [121]
Tipo: scheda tecnica
Autori: Hi-Link
Titolo: HLK-LD2450, manuale v1.00
Sede e anno: Hi-Link; copia di un rivenditore
Identificativo: v1.00
Link: https://www.elemon.com.ar/images/productos/hojas-de-datos/radar-modulos/hlk-ld2450.pdf
Verifica: aperta dal ruolo che la cita — (rif-4) ([g]); dal curatore solo [200]
Usata per: fino a tre bersagli con x, y in mm e velocità, ±60° in azimut, 6 m — `f10-dati/04-embedded/PREVISIONI.md` (E9), `INVENTARIO_E_DECISIONE.md` riga 75 ([18]) **[f7–f10: non vagliato dall'arbitro]**
Note: copia non ufficiale. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### intel-000030012 [122]
Tipo: pagina di costruttore o comunicato (articolo dell'assistenza)
Autori: Intel
Titolo: non verificato (articolo dell'assistenza Intel sulle superfici trasparenti e le camere RealSense, secondo il torneo)
Sede e anno: Intel Support, articolo 000030012; data non verificata
Identificativo: articolo 000030012
Link: https://intel.com/content/www/us/en/support/articles/000030012.html
Verifica: non raggiungibile — (rif-2) oggi lo scaricamento diretto dà 403; lo strumento di lettura riceve un 301 verso un indirizzo «404Redirector», cioè con ogni probabilità l'articolo non è più in linea a quell'indirizzo. Nel torneo era visto solo nel riassunto di un motore di ricerca.
Usata per: «l'infrarosso cade sul primo oggetto opaco dietro la superficie trasparente»: premessa fisica del falso «libero» sul vetro — `f2/04-torneo/TORNEO.md` (parte 1, «Fonti», e riga H-008).
Note: la conclusione sul vetro non dipende da questa pagina: nei file è una premessa fisica dichiarata e un limite aperto («Vetro: smentito, limite dichiarato», `SOLUZIONE_V2.md` §7), da decidere con la prova H2 davanti a una porta a vetri. Nei documenti finali la frase va scritta senza citazione, oppure con una fonte nuova da cercare.

### intel-negozio-d455 [123]
Tipo: pagina di costruttore o comunicato
Autori: Intel RealSense (negozio)
Titolo: Intel RealSense Depth Camera D455 (pagina del negozio)
Sede e anno: store.intelrealsense.com; data: manca
Identificativo: manca
Link: https://store.intelrealsense.com/buy-intel-realsense-depth-camera-d455.html
Verifica: non raggiungibile — (rif-1) (f3: il dominio intelrealsense.com non risolve); letta dal ruolo attraverso uno strumento che riassume.
Usata per: D455: campo 87°×58°, portata 0,6–6 m, errore «< 2 % a 4 m» (da cui σ_pos ≈ 3 cm) — `f1/c85dbcc51ea6/CONSEGNA.md` (§1.5, visione-1, rif. [11])
Note: campo e portata sono confermati da `realsense-confronto-camere` (f3); «±2 % a 4 m» è confermato oggi solo sulla pagina di un rivenditore (`roboticscenter-d455` [r]). La σ_pos di 3 cm è un'ipotesi del ruolo, non un dato della scheda.

### intel-t265-fine-produzione [124]
Tipo: pagina di costruttore o comunicato
Autori: Intel
Titolo: manca (articolo di supporto 000087450)
Sede e anno: sito di supporto di Intel; data non verificata
Identificativo: articolo 000087450
Link: https://intel.com/content/www/us/en/support/articles/000087450/emerging-technologies/intel-realsense-technology.html
Verifica: non raggiungibile — (rif-3) oggi il link rimanda (301) a una pagina d'errore di Intel; con una richiesta diretta risponde 403. Vista solo nel riassunto di un motore di ricerca, come già dal ruolo che la cita.
Usata per: il modulo T265 è fuori produzione dal 2022 e il costruttore indica D455 o D435i «with 3rd Party SLAM SW» — `f6-specializzazione/02-slam/MOTO_PROPRIO.md` §2(b)
Note: correzione 13. L'anno e la frase fra «» restano non verificati; serve un'altra fonte del costruttore.

### ldrobot-ld19 [125]
Tipo: pagina di costruttore o comunicato
Autori: LDROBOT (pagine di Waveshare e OpenELAB)
Titolo: DTOF LIDAR LD19 (Waveshare); LDROBOT D500 DTOF LiDAR Kit, STL-19P (OpenELAB); scheda «LDROBOT STL-19P Datasheet EN v1.0»
Sede e anno: date: manca
Identificativo: STL-19P Datasheet v1.0
Link: https://www.waveshare.com/dtof-lidar-ld19.htm ; https://openelab.io/products/ldrobot-d500-dtof-lidar-kit ; https://files.waveshare.com/wiki/D500-LiDAR-Kit/LDROBOT_STL-19P_Datasheet_EN_v1.0(1).pdf ; anche (rif-2): https://www.waveshare.com/wiki/DTOF_LIDAR_LD19
Verifica: dato diverso — (rif-1, pagina prodotto Waveshare e pagina OpenELAB) già verificata dal curatore in f3, con correzione: LD19 (Waveshare [r]) 30 klx, 4500 Hz, 0,02–12 m, 5–13 Hz; i 60 klx sono dell'STL-19P (OpenELAB [g]); risoluzione angolare 0,8°: non trovata. Dato diverso: 30 klx e non 60 per l'LD19. Non riaperta oggi. ‖ (rif-2, wiki Waveshare) risoluzione angolare «≤1°», non «0,8°». Pagina aperta oggi: «Measuring radius 12m»; «30K Lux anti-glare interference»; «4500Hz measurement frequency»; «Typical measuring range 0.02~12m»; «Sweep frequency 10 Hz»; «Angular resolution ≤1°». «5–13 Hz»: non trovato nelle righe lette. Già in f3/fonti (letta là attraverso un riassunto; 0,8° «non trovata»).
Usata per: «LD19: 0,8°, 5–13 Hz, 12 m» (ricerca), 8,9 fasci su un pedone a 4 m — `f1/dfac83300259/CONSEGNA.md` (nuvole-punti-2)
Usata per: «60 klx (LD19, r)», 12 m, 69–70 $ — `f1/985ccd9bca46/CONSEGNA.md` (tabella, rif. [9]), `f1/985ccd9bca46/PREVISIONI.md` (P7)
Usata per: «LD19: 0,8°, 5–13 Hz, 12 m»; 8,9 fasci su un pedone a 4 m — `f2/01-traduzione/SCHEDE.md` (`nuvole-punti-2`); «RPLIDAR C1 o LD19, 70–80 $» — `f2/01-traduzione/SCHEDE.md` (`lidar-2`).
Usata per: «Fonti: LD19 tiene 30 klx, non 60» — `f2/05-selezione/SELEZIONE.md` (H-003).
Note: (rif-1) LD19 e STL-19P (kit D500) sono due prodotti: non scambiare le cifre. Prezzo non verificato. (rif-2) correzione 4 in testa. 0,8° = 360° / 450 punti per giro a 10 Hz: derivato, da dichiarare così. È la pagina di un rivenditore, non la scheda del costruttore (non cercata). Prezzo non verificato. All'unione: la scheda LD19 V2.5 letta in f10 ha una voce sua, `ldrobot-ld19-scheda`. Differenza fra le pagine: «5–13 Hz» letto da f3 sulla pagina prodotto Waveshare [r], non trovato da rif-2 nel wiki Waveshare («Sweep frequency 10 Hz»).

### ldrobot-ld19-scheda [126]
Tipo: scheda tecnica
Autori: LDROBOT
Titolo: LD19, scheda V2.5
Sede e anno: copia di un rivenditore (Botland)
Identificativo: V2.5
Link: https://botland.com.pl/img/art/inne/21991_Karta%20katalogowa.pdf
Verifica: aperta dal ruolo che la cita — (rif-4) dal curatore solo [200]
Usata per: accuratezza ±45 mm (media di 100 misure), scarto tipo 10 mm; nessuna portata sul nero — `f10-dati/02-sensori/PREVISIONI.md` riga 32, `MODELLO_SENSORE.md` (S11) **[f7–f10: non vagliato dall'arbitro]**
Note: copia non ufficiale. All'unione: separata da `ldrobot-ld19` (pagine di rivenditori), perché è un altro documento; nel gruppo rif-4 la chiave era `ldrobot-ld19`. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### livox-mid-360 [127]
Tipo: scheda tecnica (pagina delle specifiche del costruttore)
Autori: Livox
Titolo: Mid-360, Specs
Sede e anno: sito del costruttore, letto il 14-11-2026
Identificativo: manca
Link: https://www.livoxtech.com/mid-360/specs ; anche (rif-1): https://www.roboticscenter.ai/es/store/product/livox-dji-livox-mid-360 ; https://dronexl.co/2026/09/21/livox-mid-360l-lidar-half-point-rate-robots/
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-1, sulla pagina di un rivenditore) [r] in parte: pagina aperta; campo 360° × (−7°…52°), cioè 59°; 40 m al 10 % e 70 m all'80 % di riflettività. Dato diverso: nessun prezzo sulla pagina («Contact for pricing»); gli 899–1092 $ non sono verificati. ‖ (rif-2, sulla pagina del costruttore) «Laser Wavelength 905 nm»; «Detection Range (@ 100 klx) 40 m @ 10% reflectivity, 70 m @ 80% reflectivity»; «FOV Horizontal: 360°, Vertical: -7°~52°»; «Frame Rate 10 Hz (typical)»; 200 000 punti/s. Aperta anche dal ruolo che la cita. In f3 era fra i «non controllati». ‖ (rif-3, sulla pagina del costruttore) [g] — «Detection Range (@ 100 klx) 40 m @ 10% reflectivity, 70 m @ 80% reflectivity»; «Close Proximity Blind Zone 0.1 m»; «FOV Horizontal: 360°, Vertical: -7°~52°» (59° in tutto); «Frame Rate 10 Hz (typical)»; «Power 6.5 W (average)»; «Weight 265 g». Aperta anche dal ruolo che la cita.
Usata per: Mid-360: 360°×59°, 40 m (r), 899–1092 $ (r) — `f1/985ccd9bca46/CONSEGNA.md` (tabella, rif. [11]), `f1/985ccd9bca46/PREVISIONI.md` (P9)
Usata per: «Livox Mid-360: 360°, 40 m al 10 % a 100 klx, 905 nm»: i 360° si hanno con un LiDAR a scansione, non con tre ToF — `f2/04-torneo/TORNEO.md` (parte 1, H-007 e «Fonti»); `f2/05-selezione/SELEZIONE.md` (§3, F-001: «prezzo non verificato»).
Usata per: LiDAR a stato solido: portata, campo, 10 Hz, 265 g, 6,5 W, zona cieca 0,1 m — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §2(b), S15
Usata per: alla scala reale un LiDAR da 10–40 m, da provare — `f6-specializzazione/01-esperto-dominio/SPECIALIZZAZIONE.md` §1
Note: (rif-1) pagina di rivenditore, non la scheda Livox. La pagina DroneXL (979 $ di listino) non è stata aperta. (rif-2) principio di misura e prezzo non sono nella pagina: restano non verificati, come scrive il torneo. (rif-3) la stessa pagina dà la precisione radiale: ≤ 2 cm a 10 m e ≤ 3 cm a 0,2 m (1σ). `MOTO_PROPRIO.md` usa «3 cm radiali» come ipotesi senza citare la fonte: è coerente con la scheda, per eccesso. Vetro e pioggia: la scheda non li tratta. Differenza fra i gruppi: rif-1 aveva letto la pagina di un rivenditore (nessun prezzo: «Contact for pricing»); rif-2 e rif-3 la pagina delle specifiche del costruttore, tenuta come fonte. Il prezzo (899–1092 $ in f1; 979 $ di listino su una pagina DroneXL mai aperta) resta NON verificato.

### lucid-helios2-wide [128]
Tipo: pagina di costruttore o comunicato
Autori: LUCID Vision Labs
Titolo: Helios2 Wide Time-of-Flight (ToF) IP67 3D Camera (pagina prodotto)
Sede e anno: LUCID Vision Labs, pagina prodotto letta il 14-11-2026
Identificativo: manca
Link: https://thinklucid.com/product/helios2-wide-time-of-flight-tof-ip67-3d-camera/
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-2) «wide-angle lens providing a 108º angle of view»; «Lens Field of View 108° x 78° (nominal)»; «4 x VCSEL laser diodes, Class 1, @ 850nm». Nel torneo era vista solo nel riassunto della ricerca.
Usata per: «Helios2 Wide 108°» — `f2/04-torneo/TORNEO.md` (parte 1, H-007).
Note: il torneo non nominava il costruttore né l'indirizzo: li ho trovati io. Portata e comportamento al sole non letti.

### luxonis-oak-d-pro-w [129]
Tipo: pagina di costruttore o comunicato (rivenditore)
Autori: Luxonis (pagina di Arducam)
Titolo: OAK-D Pro W (pagina del rivenditore; titolo esatto: manca)
Sede e anno: arducam.com; data: manca
Identificativo: manca
Link: https://www.arducam.com/oak-d-pro-w.html
Verifica: non raggiungibile — (rif-1) (403 oggi, con lo strumento di lettura e con una richiesta diretta); il ruolo l'ha vista solo nel riassunto di un motore di ricerca.
Usata per: tre OAK-D Pro W, stereo attivo, 127° orizzontali, 499–529 $ l'una — `f1/985ccd9bca46/CONSEGNA.md` (§2, rif. [12])
Note: campo e prezzo non verificati. È l'unico «tre sensori per 360°» geometricamente valido secondo `lidar`: prima di ripeterlo va letta la scheda Luxonis.

### luxonis-tof [130]
Tipo: pagina di costruttore o comunicato (documentazione dell'hardware)
Autori: Luxonis
Titolo: ToF Depth Perception
Sede e anno: Luxonis, documentazione dell'hardware, pagina letta il 14-11-2026
Identificativo: manca
Link: https://docs.luxonis.com/hardware/platform/depth/ToF-depth
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-1) già verificata dal curatore in f3 [g]: 640×480, 20 cm–5 m, «<1% indoors, <2% outdoors», «Issues when using multiple ToFs (interference)». Non riaperta oggi. ‖ (rif-2) «20cm - 5m»; «ToF sensors have a depth error of <1% indoors, <2% outdoors»; «Issues when using multiple ToFs (interference)»; «Limited resolution: 640x480». Già in f3/fonti.
Usata per: F3: ToF Luxonis 5 m, «<2% outdoors»; interferenza fra più ToF — `f1/3fff79e9c3ea/FONTI.md`, `f1/3fff79e9c3ea/CONSEGNA.md` (§1.1, §1.2), `f1/3fff79e9c3ea/PREVISIONI.md` (P1)
Usata per: K-009, sole non risolto: Luxonis «<2% outdoors» contro Orbbec «Indoor» — `f2/01-traduzione/SCHEDE.md` (`ricercatore-1`); `f2/03-triage/TRIAGE.md` (K-009); `f2/05-selezione/SELEZIONE.md` (K-009).
Note: (rif-1) fonte del costruttore; non dice a quale illuminamento vale «outdoors». La discordanza con Orbbec («Indoor») è vera fra costruttori (K-009 di f3): la decide una prova al sole sul sensore posseduto. (rif-2) fonte del costruttore; «outdoors» senza illuminamento dichiarato. Non decide K-009: decide la prova al sole sul sensore posseduto.

### microsoft-azure-kinect-specifiche [131]
Tipo: pagina di costruttore o comunicato
Autori: Microsoft
Titolo: Azure Kinect DK hardware specifications
Sede e anno: learn.microsoft.com, sezione delle versioni precedenti
Identificativo: manca
Link: https://learn.microsoft.com/en-us/previous-versions/azure/kinect-dk/hardware-specification
Verifica: aperta dal ruolo che la cita — (rif-4) dal curatore solo [200]
Usata per: caratteristiche dell'Azure Kinect nell'inventario — `f10-dati/04-embedded/INVENTARIO_E_DECISIONE.md` riga 75 ([8]) **[f7–f10: non vagliato dall'arbitro]**
Note: la fine della produzione (annuncio del 17 agosto 2023) è marcata [r] dal ruolo: non verificata. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### nvidia-jetson-orin-nano [132]
Tipo: pagina di costruttore o comunicato (pagina di un rivenditore)
Autori: Kiwi Electronics (rivenditore)
Titolo: NVIDIA Jetson Orin Nano Super Developer Kit
Sede e anno: sito del rivenditore, letto il 14-11-2026
Identificativo: manca
Link: https://www.kiwi-electronics.com/en/single-board-computers-390/nvidia-jetson-orin-nano-super-developer-kit-11461
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-3) [g] — «Flexible power modes: 7W, 15W, 25W, and MAXN-Super». Il ruolo che la cita l'aveva vista solo in un risultato di ricerca.
Usata per: una Jetson Orin Nano lavora a 7, 15 o 25 W — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §2(f), S26
Note: è la pagina di un rivenditore, non del costruttore: per un documento destinato alla giuria conviene la scheda di NVIDIA (non aperta).

### orbbec-astra-pagina [133]
Tipo: pagina di costruttore o comunicato
Autori: Orbbec
Titolo: Astra Series
Sede e anno: sito del costruttore
Identificativo: manca
Link: https://www.orbbec.com/products/structured-light-camera/astra-series/
Verifica: aperta dal ruolo che la cita — (rif-4) dal curatore solo [200]
Usata per: campo 58,4° × 45,5°, 0,6–8 m, USB 2.0 — `f10-dati/04-embedded/PREVISIONI.md` (note in fondo), `INVENTARIO_E_DECISIONE.md` ([11]) **[f7–f10: non vagliato dall'arbitro]**
Note: Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### orbbec-femto-bolt [134]
Tipo: scheda tecnica (pagina prodotto e scheda PDF v01)
Autori: Orbbec
Titolo: Femto Bolt (pagina prodotto) e scheda «ORBBEC Datasheet Femto Bolt», v01
Sede e anno: Orbbec; scheda PDF 0816-v01, agosto 2023; pagina letta il 14-11-2026 (in f1 e f3)
Identificativo: ORBBEC_Datasheet_Femto-Bolt-0816-v01
Link: https://www.orbbec.com/products/tof-camera/femto-bolt/ ; https://www.orbbec.com/products/femto-bolt/ ; https://www.orbbec.com/wp-content/uploads/2023/08/ORBBEC_Datasheet_Femto-Bolt-0816-v01.pdf
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-1) già verificata dal curatore in f3 [g]: 120°×120° (largo) e 75°×65° (stretto), 850 nm; largo raggruppato 0,25–2,88 m (512×512, fino a 30 fps); largo pieno 0,25–2,21 m (1024×1024, 5 o 15 fps); stretto 0,5–3,86 m e 0,5–5,46 m (raggruppato); IMU [r]. Ambiente: la pagina scrive «Indoor», la scheda v01 «Indoor/Semi-Outdoor». Non riaperta oggi. ‖ (rif-2) «H 120° V 120° (WFOV), H 75° V 65° (NFOV)»; «WFOV 2x2 binned 0.25 - 2.88 m»; «WFOV unbinned 0.25 - 2.21 m»; «NFOV 2x2 binned 0.5 - 5.46 m»; ambiente: «Indoor» nelle specifiche e «Indoor/Semi-Outdoor» nella tabella di confronto con Azure Kinect. Già in f3/fonti.
Usata per: F1: 120°×120°, 0,25–2,88 m, «Indoor» — `f1/3fff79e9c3ea/FONTI.md`, `f1/3fff79e9c3ea/CONSEGNA.md` (§1.1, §1.2), `f1/3fff79e9c3ea/PREVISIONI.md` (P1)
Usata per: «portata 0,25–2,88 m in modo largo» — `f1/c85dbcc51ea6/CONSEGNA.md` (rif. [8])
Usata per: «0,25–2,21 m, 15 fps, 418–559 $ l'una» (ricerca) — `f1/dfac83300259/CONSEGNA.md` (§1.1)
Usata per: 120°×120°, 0,25–2,88 m, «Indoor / Semi-outdoor», 5,46 m stretto — `f1/985ccd9bca46/CONSEGNA.md` (§2.3, tabella, rif. [3])
Usata per: 75° e 120°, portata al più 2,88 m — `f1/b8262bfed263/CONSEGNA.md` (requisiti-1)
Usata per: caso limite «Femto Bolt, 120° esatti»: nessun ToF con campo orizzontale ≥ 130° — `f2/01-traduzione/SCHEDE.md` (`requisiti-1`, P1); `f2/04-torneo/TORNEO.md` (parte 1, H-007: «massimo 120° (Femto…)»); `f2/05-selezione/SELEZIONE.md` (H-007).
Usata per: K-012, 0,25–2,88 m contro 0,25–2,21 m: due modi — `f2/01-traduzione/SCHEDE.md` (coda, (b) 12); `f2/03-triage/TRIAGE.md` (K-012); `f2/05-selezione/SELEZIONE.md` (K-012).
Usata per: K-009, Orbbec «Indoor» o «Indoor/Semi-Outdoor» contro Luxonis «<2% outdoors» — `f2/01-traduzione/SCHEDE.md` (`ricercatore-1`); `f2/03-triage/TRIAGE.md` (K-009); `f2/05-selezione/SELEZIONE.md` (K-009).
Note: (rif-1) 2,88 e 2,21 m sono due modi, entrambi giusti (f3, punto 1). Il prezzo di 559 $ citato da `nuvole-punti` non è verificato. Classe laser: non verificata. (rif-2) correzione 5 in testa. Prezzo non verificato oggi. La pagina può cambiare: conviene conservarne una copia con la data. Differenza fra i gruppi: per rif-2 il tipo era «pagina di costruttore» (solo la pagina prodotto); rif-1 e f3 hanno letto anche la scheda PDF v01.

### orbbec-femto-bolt-sincronia [135]
Tipo: documentazione di software
Autori: Orbbec
Titolo: Synchronize Multiple Femto Bolt Devices
Sede e anno: Orbbec, documentazione in linea; revisione: manca
Identificativo: manca
Link: https://doc.orbbec.com/documentation/Orbbec%20Femto%20Bolt%20Documentation/Synchronize%20Multiple%20Femto%20Bolt%20Devices
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-1) già verificata dal curatore in f3 [g]: «offset from each other by 160us or more»; impulso di 125 µs. Aperta anche dal ruolo che la cita. Non riaperta oggi.
Usata per: catture sfalsate di almeno 160 µs col cavo di sincronizzazione — `f1/985ccd9bca46/CONSEGNA.md` (§2.3, rif. [4]), `f1/985ccd9bca46/PREVISIONI.md` (P5)
Note: vale per la Femto Bolt; per i multizona ST nessun enunciato sull'interferenza è stato trovato (non verificato).

### orbbec-gemini-330-scheda [136]
Tipo: scheda tecnica
Autori: Orbbec
Titolo: Gemini 330 series Datasheet
Sede e anno: Orbbec, V1.6
Identificativo: V1.6
Link: https://download.kamami.pl/p1203693-Gemini-330-series-Datasheet-V1.6.pdf
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-4) [T]: PDF aperto; «V1.6», 850, «All-Pass» presenti
Usata per: Gemini 335: 850 ± 6 nm, imager «All-Pass»; filtri di post-elaborazione attivi come impostazione predefinita (tab. 4-13-1) — `f9-preproposta/07-lidar/CONSEGNA.md` ([5]); `f10-dati/02-sensori/PREVISIONI.md` riga 33, `MODELLO_SENSORE.md` (S6) **[f7–f10: non vagliato dall'arbitro]**
Note: copia di un rivenditore. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### orbbec-gemini-335 [137]
Tipo: pagina di costruttore o comunicato
Autori: Orbbec
Titolo: Gemini 335 (pagina prodotto)
Sede e anno: Orbbec, pagina prodotto letta il 14-11-2026
Identificativo: manca
Link: https://www.orbbec.com/products/stereo-vision-camera/gemini-335/
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-1) già verificata dal curatore in f3 [g]: 90°×65°, ottimale 0,26–3 m, 1280×800 a 30 fps, IMU, interno ed esterno; tipo di otturatore: assente. Non riaperta oggi. ‖ (rif-2) «It has a 50mm baseline»; «Depth FOV H90° V65°»; «Spatial Precision: ≤ 1.5% (1280 x 800 @ 2m & 90% x 90% ROI)»; «Depth Range 0.10 - 20m+ (Optimal Range: 0.26 - 3m)»; «Indoor/Outdoor»; IMU. Aperta anche dal ruolo che la cita (avversario, torneo) e già in f3/fonti.
Usata per: 90°×65°, 0,26–3 m, 1280×800 a 30 fps, IMU — `f1/985ccd9bca46/CONSEGNA.md` (tabella, rif. [7]); prezzo 330–369 $ da rivenditori — `f1/985ccd9bca46/PREVISIONI.md` (P6)
Usata per: errore al limite dichiarato a 4 m: 12 cm; tocca 15 cm a 4,5 m; base 50 mm; «90°×65°, non 87°×58°» — `f2/04-torneo/TORNEO.md` (parte 1, H-001 e «Fonti»); `f2/05-selezione/SELEZIONE.md` (H-001); `f3/H-012/03-metrologo/PIANO_MISURE.md` (critica 9: «Gemini 335 12»).
Usata per: una delle camere candidate, 90°×65° — `f2/01-traduzione/SCHEDE.md` (`lidar-1`); `f3/H-012/01-scene-dinamiche/SOLUZIONE.md` (B1); `f4/H-012/05-correzioni/SOLUZIONE_V2.md` (B1).
Note: (rif-1) il prezzo 330–369 $ non è verificato (nessun link del rivenditore nei file). (rif-2) l'1,5 % è «Spatial Precision» (RMSE), cioè rumore spaziale a 2 m; i 12 cm a 4 m sono una estrapolazione con z² fatta dall'avversario, non un dato di scheda. Tipo di otturatore non indicato (f3).

### orbbec-negozio-femto-bolt [138]
Tipo: pagina di costruttore o comunicato
Autori: Orbbec
Titolo: Femto Bolt (negozio in linea)
Sede e anno: Orbbec Store, letta il 14-11-2026 (in f3)
Identificativo: manca
Link: https://store.orbbec.com/products/femto-bolt
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-1) già verificata dal curatore in f3 [g]: 418 $. Non riaperta oggi (in f1 il negozio aveva risposto 429 a `lidar`).
Usata per: 418 $ l'una, 1254 $ per tre — `f1/985ccd9bca46/CONSEGNA.md` (§2.3), `f1/985ccd9bca46/PREVISIONI.md` (P4)
Note: prezzo in dollari, del giorno; disponibilità in Italia non verificata.

### pololu-vl53l8cx-3419 [139]
Tipo: pagina di costruttore o comunicato
Autori: Pololu
Titolo: VL53L8CX Time-of-Flight 8×8-Zone Distance Sensor Carrier with Voltage Regulators, 400cm Max (articolo 3419)
Sede e anno: Pololu, pagina prodotto, letta il 14-11-2026
Identificativo: Pololu #3419
Link: https://www.pololu.com/product/3419
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-1) [r]: pagina aperta; 65° in diagonale (45° orizzontali e verticali), 4 m, 4×4 o 8×8 zone; tabella di confronto: VL53L5CX 400 cm e 65° diag., VL53L7CX 350 cm e 90° diag., VL53L8CX 400 cm e 65° diag.
Usata per: «VL53L8CX 45°×45°, 4 m; VL53L7CX 60°×60°» — `f1/c85dbcc51ea6/CONSEGNA.md` (rif. [7]); «4 m al buio (confronto Pololu)» — `f1/985ccd9bca46/PREVISIONI.md` (P3)
Note: è la pagina di un rivenditore; il «60°×60°» del 7CX non è scritto così qui (c'è «90° diagonal»): per quel dato vale `st-vl53l7cx`.

### realsense-alta-velocita-d435 [140]
Tipo: pagina di costruttore o comunicato (documento tecnico)
Autori: RealSense (già Intel RealSense); autori del documento non letti
Titolo: High-speed capture mode of RealSense Depth Camera D435
Sede e anno: RealSense, documentazione per sviluppatori, pagina letta il 14-11-2026; data e revisione non indicate nel testo letto
Identificativo: manca
Link: https://dev.realsenseai.com/docs/high-speed-capture-mode-of-intel-realsense-depth-camera-d435
Verifica: dato diverso — (rif-2) le cifre ci sono, ma misurano il sistema di prova e non il solo sensore. Pagina aperta oggi (e dal ruolo che la cita, attraverso un'estrazione automatica). Tabella 4, «Measured latencies of each frame rate»: 848×100 a 15 fps 127 ms; 30 fps 95 ms; 60 fps 47 ms; 90 fps 39 ms; 400 fps 25 ms. §4.5: misura fatta con `rs-latency-tool` puntando la camera su uno schermo da 120 Hz; «The GPU adds latency in displaying an image, and the LCD screen has refresh rate and LCD limitations, and USB data packet transport introduces latency… this experiment does not allow us to parse out the latency of the depth camera directly, it does provide a system-level upper limit». E ancora: «capturing motion for a global shutter camera should in worst case introduce a latency of a little over a single frame time».
Usata per: «esposizione → fotogramma nell'applicazione: media 95 ms a 30 fps; 127 a 15; 47 a 60; 39 a 90… che cosa includa la misura: non verificato» — `f3/H-012/02-validazione/VERIFICA.md` (§3c).
Usata per: «le sole voci note sommano circa 155 ms in media» contro la soglia di 150 ms — `f3/H-012/02-validazione/VERIFICA.md` (§3c); `f4/H-012/05-correzioni/SOLUZIONE_V2.md` (§7, R7); `f5/02-audit/AUDIT.md` (ipotesi 3: 0,288 s, 0,72 m); `f4/H-012/09-arbitro/VERDETTO.md` (costo; K-015).
Usata per: «flusso a 60 o 90 fps usando l'ultimo fotogramma» — `f4/H-012/05-correzioni/SOLUZIONE_V2.md` (B8); «i 47 e 39 ms vengono dai modi 848×100» — `f5/02-audit/AUDIT.md` (ipotesi 7).
Note: correzione 2 in testa: scioglie il «non verificato» di `VERIFICA.md`. Una camera (D435), un calcolatore, medie senza percentili, modi 848×100 (il documento dice che questi modi scambiano campo verticale con frequenza; i «circa 12°» dell'audit sono un suo conto, coerente con 58° × 100/480, non una cifra letta). I conti che ne discendono (0,72 m a 2,5 m/s; velocità massima coperta circa 1,4 m/s) usano un limite superiore: sono prudenti, non misurati. Decide la prova H12.

### realsense-bkm-taratura [141]
Tipo: scheda tecnica (documento del costruttore)
Autori: Intel RealSense (ora RealSense); autori secondo il riassunto di un motore di ricerca (non verificato): Anders Grunnet-Jepsen, John N. Sweetser, John Woodfill
Titolo: BKMs for Tuning Intel RealSense D4xx Cameras (titolo dal nome del file)
Sede e anno: 2019 (dal percorso del file); «revisione 1.9» secondo il riassunto di un motore di ricerca: non verificato
Identificativo: manca
Link: https://realsenseai.com/wp-content/uploads/2019/11/BKMs_Tuning_RealSense_D4xx_Cam.pdf ; anche (rif-3): https://forums.intel.com/cipcp26785/attachments/cipcp26785/feeditem_no_topic/6364/1/BKMs_Tuning_RealSense_D4xx_Cam.pdf
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-3, sul link dei forum Intel) non raggiungibile — oggi il link risponde 404, e la pagina di Intel che ospita lo stesso documento risponde 403. Vista solo nel riassunto di un motore di ricerca, come già dal ruolo che la cita. ‖ (rif-4, sulla copia di realsenseai.com) [T]: «a well-calibrated camera should produce a Subpixel RMS error of less than 0.1», «subpixel=0.08», «By default we do not do any post-processing of the depth» presenti
Usata per: stereo attiva: errore crescente con z² — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §2(b), S14
Usata per: errore di disparità s < 0,1 px (0,08 per la curva della D435), da cui σz = z²·s/(fx·B); nessun filtro predefinito nell'SDK — `f10-dati/02-sensori/MODELLO_SENSORE.md` righe 18 e 90 (S2), `PREVISIONI.md` riga 33 **[f7–f10: non vagliato dall'arbitro]**
Note: (rif-3) l'affermazione sul quadrato della distanza l'ho trovata oggi [g] nella versione in rete della stessa guida, sul sito attuale del marchio (https://dev.realsenseai.com/docs/tuning-depth-cameras-for-best-performance): «The depth error scales as the square of the distance away». Conviene sostituire il link. All'unione: fusa con la voce `intel-bkm-d400` di rif-3 (stesso file PDF, citato nel quadro di dominio da un indirizzo dei forum Intel che oggi dà 404: https://forums.intel.com/cipcp26785/attachments/cipcp26785/feeditem_no_topic/6364/1/BKMs_Tuning_RealSense_D4xx_Cam.pdf). La versione in rete della stessa guida è `realsense-taratura-profondita`. Alcuni usi vengono dalle estensioni f7–f10: NON ancora vagliati dall'arbitro (marcati riga per riga).

### realsense-confronto-camere [142]
Tipo: pagina di costruttore o comunicato
Autori: RealSense
Titolo: Compare Depth Cameras (tabella di confronto delle camere D400)
Sede e anno: RealSense, pagina letta il 14-11-2026
Identificativo: manca
Link: https://www.realsenseai.com/compare-depth-cameras/ ; anche (rif-1): https://www.intelrealsense.com/compare-depth-cameras ; https://realsenseai.com/cn/compare-depth-cameras/
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-1) già verificata dal curatore in f3 [g, colonne attribuite via r]: D455 87°×58°, ideale 0,6–6 m, otturatore globale su profondità e RGB, IMU; D435i 87°×58°, 0,3–3 m, RGB a otturatore progressivo, IMU. Non riaperta oggi. ‖ (rif-2) con una riserva. Nel testo estratto ci sono le colonne «D455 / D455f», «D435 / D435i», «D435f / D435if», le righe sugli otturatori (globale e progressivo) e tre celle «69° × 42°»; la conversione in testo perde l'allineamento delle colonne, quindi l'attribuzione di ogni cella al suo modello non è certa. Già in f3/fonti (D435i: 87°×58°, 0,3–3 m, RGB a otturatore progressivo). ‖ (rif-3) [g] — riga «Ideal Range»: «.6 m to 6 m»; riga «Depth Accuracy»: «<2% at 4 m»; l'attribuzione delle colonne alla D455 non è leggibile dal testo grezzo e viene dalla verifica di f3. Già verificata dal curatore in `f3/fonti/FONTI_VERIFICATE.md` (voce 4).
Usata per: «D435: ideale 0,3–3 m, 87°×58°» (ricerca) — `f1/dfac83300259/CONSEGNA.md` (§1.4)
Usata per: RealSense D435 e D455 a 87° in P1 — `f1/b8262bfed263/CONSEGNA.md`
Usata per: D435i fra le camere candidate, 87°×58° — `f2/01-traduzione/SCHEDE.md` (`lidar-1`; «classe D435» in `nuvole-punti-2`); `f3/H-012/01-scene-dinamiche/SOLUZIONE.md` (B1); `f4/H-012/05-correzioni/SOLUZIONE_V2.md` (B1).
Usata per: «allineando la profondità all'RGB, sulla D435i il campo scende a circa 69°×42° (non verificato in rete)» — `f5/02-audit/AUDIT.md` (ipotesi 11).
Usata per: D455: campo ideale 0,6–6 m; errore < 2 % a 4 m — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §2(b) (lì attribuita a S14)
Note: (rif-1) il dominio intelrealsense.com non risolve più: usare realsenseai.com. (rif-2) il valore 69°×42° c'è; resta da leggere sulla pagina a occhio che sia la riga del campo RGB della D435i. Le conseguenze dell'audit (suolo visto da 1,65 m, ostacolo invisibile sotto 1,45 m) sono conti suoi, non della fonte. (rif-3) voce aggiunta da me: i quattro file non citano questo link, ma è qui che stanno le due cifre che il quadro attribuisce a S14. Sono valori di catalogo, non misure nelle condizioni del progetto.

### realsense-d400-accuratezza [143]
Tipo: pagina di costruttore o comunicato (articolo dell'assistenza)
Autori: RealSense Help Center (articolo firmato Jesus Garcia)
Titolo: Depth accuracy for Intel RealSense D400 Series Cameras
Sede e anno: RealSense Help Center, articolo 360059129453, 12-11-2020 (poi aggiornato)
Identificativo: articolo 360059129453
Link: https://support.realsenseai.com/hc/en-us/articles/360059129453-Depth-accuracy-for-Intel-RealSense-D400-Series-Cameras
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-2) Nel torneo era «non aperta (errore 403), solo riassunto»; oggi risponde. Tabella: D420/D430/D435/D435i «up to 2 Meters and 80% ROI, HD Resolution», D455 «up to 4 Meters»: Z-accuracy ≤ 2 %, RMS Error ≤ 2 %, Fill rate ≥ 99 %, Temporal Noise ≤ 1 %. Rimanda alla Tabella 4-9 della scheda della famiglia D400 (non aperta).
Usata per: D435i «≤ 2 % fino a 2 m»; al limite dichiarato 16 cm a 4 m, tocca 15 cm a 3,9 m — `f2/04-torneo/TORNEO.md` (parte 1, H-001 e «Fonti»); `f3/H-012/03-metrologo/PIANO_MISURE.md` (critica 9: «D435i 16»).
Usata per: curva «pessimista» del rumore, «2 % a 2 m» scalato con z² (4 / 9 / 16 cm a 2 / 3 / 4 m) — `f3/H-012/02-validazione/VERIFICA.md` (§4); `f4/H-012/05-correzioni/SOLUZIONE_V2.md` (B1).
Note: la specifica vale fino a 2 m per la D435i: i 16 cm a 4 m sono fuori dall'intervallo dichiarato (estrapolazione dello sciame). Vale per moduli integrati e tarati, sull'80 % della regione.

### realsense-d400-scheda [144]
Tipo: scheda tecnica
Autori: RealSense (già Intel RealSense)
Titolo: RealSense D400 Series Product Family Datasheet
Sede e anno: revisione di marzo 2026 (in `f10-dati/02-sensori/PREVISIONI.md`: «rev. 023»)
Identificativo: manca (numero del documento non letto)
Link: https://www.realsenseai.com/wp-content/uploads/2026/03/RealSense-D400-Series-Datasheet-Mar-2026.pdf
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-4) [T]: PDF aperto (5,4 MB); 850 (nm), 360 (mW), «All pass», «Filter Type» presenti; base stereo e RMS non ricontrollati
Usata per: proiettore 850 ± 10 nm, 360 mW massimi, campo 90° × 63°; imager senza filtro («Filter Type: None», «Depth Filter: All pass») — `f9-preproposta/07-lidar/CONSEGNA.md` ([4]); base 50 mm (D430) e 95 mm (D450), RMS ≤ 2 % entro 2 m (D43x) ed entro 4 m (D455) — `f10-dati/02-sensori/PREVISIONI.md` righe 9 e 24, `MODELLO_SENSORE.md` (S1) **[f7–f10: non vagliato dall'arbitro]**
Note: che «rev. 023» e «Mar 2026» siano lo stesso documento non è verificato. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### realsense-d455 [145]
Tipo: pagina di costruttore o comunicato
Autori: RealSense (già Intel RealSense)
Titolo: RealSense Depth Camera D455 / D455f (pagina prodotto)
Sede e anno: RealSense, pagina prodotto letta il 14-11-2026
Identificativo: manca
Link: https://realsenseai.com/products/real-sense-depth-camera-d455f/
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-2) «FOV 87° × 58°»; «Ideal Range .6 m to 6 m»; «Global Shutter»; «The D455 extends the distance between the depth sensors to 95 mm which improves the depth error to less than 2% at 4 m». Aperta anche dal ruolo che la cita (avversario, torneo).
Usata per: D455: 87°×58°, otturatore globale, IMU, 0,6–6 m — `f2/01-traduzione/SCHEDE.md` (`visione-1`, `lidar-1`); `f3/H-012/01-scene-dinamiche/SOLUZIONE.md` (B1); `f4/H-012/05-correzioni/SOLUZIONE_V2.md` (B1).
Usata per: errore al limite dichiarato a 4 m: 8 cm; tocca 15 cm a 5,5 m (da «<2% at 4 m», base 95 mm) — `f2/04-torneo/TORNEO.md` (parte 1, H-001); `f3/H-012/03-metrologo/PIANO_MISURE.md` (critica 9).
Usata per: banda senza dato accanto all'ombra, 9,5 cm con base 95 mm — `f5/02-audit/AUDIT.md` (ipotesi 10).
Note: «<2% at 4 m» è una dichiarazione del costruttore, in condizioni di prova sue (vedi `realsense-d400-accuratezza`: 80 % della regione, risoluzione HD). La presenza dell'IMU oggi non l'ho cercata nella pagina (confermata in f3).

### realsense-taratura-profondita [146]
Tipo: pagina di costruttore o comunicato (documento tecnico)
Autori: RealSense (già Intel RealSense); autori del documento non letti
Titolo: Tuning depth cameras for best performance
Sede e anno: RealSense, documentazione per sviluppatori, pagina letta il 14-11-2026; data e revisione non indicate nel testo letto
Identificativo: manca
Link: https://dev.realsenseai.com/docs/tuning-depth-cameras-for-best-performance
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-2) «The depth error scales as the square of the distance away»; «D435 with HFOV=90deg, Xres=848, and baseline=50mm. Both are for subpixel=0.08»; «For a well-textured target you can expect to see Subpixel < 0.1 and even approaching 0.05». La formula è un'immagine: non letta (come dichiarato dal ruolo che la cita). Conto rifatto con σ = z²·s/(f·B), f = 424 px, B = 50 mm, s = 0,08: 1,5 / 3,4 / 6,0 cm a 2 / 3 / 4 m. ‖ (rif-4) [T]: «Hallucinations», «much worse than no depth» e «High Accuracy» presenti (il ruolo l'aveva solo in riassunto, [r])
Usata per: curva «nominale» del rumore radiale R(z) nelle prove A e B — `f3/H-012/02-validazione/VERIFICA.md` (§4); `f4/H-012/05-correzioni/SOLUZIONE_V2.md` (B1: «1,5 / 3,4 / 6,0 cm (nominale, documento del costruttore)»); `f4/H-012/03-validazione/MISURE.md` (prova B: usa la curva nominale 1,5 / 3,4 / 6,0 cm, senza citare la fonte).
Usata per: base 50 mm della D435i (banda senza dato di 5 cm) — `f5/02-audit/AUDIT.md` (ipotesi 10).
Usata per: «false depth, aka. Hallucinations, are much worse than no depth»; preset «High Accuracy» — `f9-preproposta/07-lidar/CONSEGNA.md` critica 6 ([10]) **[f7–f10: non vagliato dall'arbitro]**
Note: (rif-2) 0,08 pixel è il valore con cui il costruttore traccia una curva teorica su un bersaglio ben tessuto, non una garanzia: è il rumore di un piano interpolato localmente, non quello del centro di una persona che cammina (che è la grandezza R del filtro e va misurata, prova H1). Il documento parla della D435; per la D435i la base è la stessa secondo f3, non riletto oggi. (rif-4) non dice che cosa succede sul tessuto nero: resta non verificato. All'unione: fusa con la voce `realsense-taratura-web` di rif-4 (stesso indirizzo). Il PDF della stessa guida è `realsense-bkm-taratura`. Alcuni usi vengono dalle estensioni f7–f10: NON ancora vagliati dall'arbitro (marcati riga per riga).

### record3d-funzioni [147]
Tipo: pagina di costruttore o comunicato
Autori: Record3D
Titolo: Features
Sede e anno: sito dell'applicazione
Identificativo: manca
Link: https://record3d.app/features
Verifica: vista solo nel riassunto di un motore di ricerca — (rif-4) (marca [r] del ruolo); dal curatore [T] parziale: «USB», «Wi-Fi» e «purchase» compaiono nella pagina, le condizioni precise non rilette
Usata per: flusso via USB solo dopo l'acquisto; flusso Wi-Fi a pagamento, in rete locale, con compressione con perdita — `f10-dati/04-embedded/PREVISIONI.md` (E8), `INVENTARIO_E_DECISIONE.md` ([12]) **[f7–f10: non vagliato dall'arbitro]**
Note: la risoluzione non è stata trovata (lo dice il ruolo). Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### rivenditori-d435i-prezzi [148]
Tipo: pagina di costruttore o comunicato (rivenditori)
Autori: Wamatek; RoboticsCenter
Titolo: pagine prodotto RealSense D435i; titoli esatti: manca
Sede e anno: data: manca
Identificativo: manca
Link: https://wamatek.com/products/intel-realsense-d435i-webcam-2-megapixel-30-fps-usb-3-2 ; https://www.roboticscenter.ai/store/product/realsense-d435i
Verifica: non verificata — (rif-1) (non aperte né in f3 né oggi).
Usata per: prezzi della D435i fra 362 e 550 $ — `f1/985ccd9bca46/PREVISIONI.md` (P6), ripresi in `f1/985ccd9bca46/CONSEGNA.md` (§2)
Note: citate solo in PREVISIONI.md; prezzo non verificato.

### roboticscenter-d455 [149]
Tipo: pagina di costruttore o comunicato (rivenditore)
Autori: RoboticsCenter
Titolo: RealSense D455 (pagina del rivenditore)
Sede e anno: roboticscenter.ai, letta il 14-11-2026
Identificativo: manca
Link: https://www.roboticscenter.ai/store/product/intel-realsense-d455
Verifica: dato diverso — (rif-1) [r]: pagina aperta; 87°×58° (±3°), 0,6–6 m, «±2% at 4m», IMU BMI085, otturatore globale (profondità e RGB). Dato diverso: il prezzo oggi è 650 $ («Backorder»), non 399–417 $.
Usata per: D455 87°×58°, IMU BMI085, 0,6–6 m, da 399 a 417 $ — `f1/985ccd9bca46/CONSEGNA.md` (tabella, rif. [5]), `f1/985ccd9bca46/PREVISIONI.md` (P6)
Note: prezzo cambiato o diverso dal citato: non usare la cifra 399–417 $ senza ricontrollo.

### rs-online-realsense [150]
Tipo: pagina di costruttore o comunicato (rivenditore)
Autori: RS Components
Titolo: pagine prodotto RealSense D435if (0155773) e D455 (0155774); titoli esatti: manca
Sede e anno: rs-online.com; data: manca
Identificativo: codici RS 0155773 e 0155774
Link: https://uk.rs-online.com/web/p/depth-cameras/0155773 ; https://nl.rs-online.com/web/p/depth-cameras/0155774
Verifica: non verificata — (rif-1) (prezzi esclusi dal controllo di f3; non aperta oggi).
Usata per: D435i fra 362 e 550 $; D435if «0.3 m, 3 m Max Range» — `f1/985ccd9bca46/CONSEGNA.md` (rif. [6]), `f1/985ccd9bca46/PREVISIONI.md` (P6)
Note: prezzo non verificato.

### sick-sensori-3d [151]
Tipo: pagina di costruttore o comunicato
Autori: SICK
Titolo: pagina di categoria (g568562)
Sede e anno: sito del costruttore
Identificativo: manca
Link: https://www.sick.com/in/en/c/g568562
Verifica: vista solo nel riassunto di un motore di ricerca — (rif-4) (dal ruolo); dal curatore: la pagina risponde ma il contenuto è caricato da script (3,7 kB): non letta
Usata per: i sensori 3D certificati lavorano a campi di protezione — `f7-estensione/05-esperto-dominio/CONSEGNA.md` righe 21 e 80 (S10, marca R) **[f7–f10: non vagliato dall'arbitro]**
Note: non verificata. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### slamtec-rplidar-c1 [152]
Tipo: pagina di costruttore o comunicato
Autori: Slamtec
Titolo: RPLIDAR C1 (pagina prodotto e pagina delle specifiche)
Sede e anno: Slamtec, pagine lette il 14-11-2026
Identificativo: manca
Link: https://www.slamtec.com/en/c1/spec ; anche (rif-4): https://www.slamtec.com/en/C1/Spec
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-2) «White: 0.05~12m (70% Reflectivity)»; «Black: 0.05~6m (10% Reflectivity)»; «5KHz»; «8~12Hz, 10Hz (Typical)»; «0.72°»; «40,000lux». Già in f3/fonti (letta là attraverso un riassunto). ‖ (rif-4) aperta dal ruolo che la cita; dal curatore solo [200]
Usata per: LiDAR 2D rotante: «360° a 10 Hz, 5000 punti/s, 12 m, 6 m sul nero»; 8 punti su una persona a 5 m, 2 su una gamba — `f2/01-traduzione/SCHEDE.md` (`lidar-2`); smentita della variante al petto (1,7–1,9 punti su una gamba a 5 m, dal passo angolare) — `f2/04-torneo/TORNEO.md` (parte 1, H-003); `f2/05-selezione/SELEZIONE.md` (H-003).
Usata per: accuratezza ±30 mm — `f10-dati/02-sensori/PREVISIONI.md` riga 32, `MODELLO_SENSORE.md` (S10); SDK: `INVENTARIO_E_DECISIONE.md` ([15], https://github.com/Slamtec/rplidar_sdk, [200]) **[f7–f10: non vagliato dall'arbitro]**
Note: (rif-2) prezzo «70–80 $»: non verificato. I conti dei punti sono dello sciame. All'unione: la pagina del rivenditore Waveshare (prezzo, «±30 mm», «FDA Class 1») ha una voce sua, `waveshare-rplidar-c1`. Alcuni usi vengono dalle estensioni f7–f10: NON ancora vagliati dall'arbitro (marcati riga per riga).

### st-um2884 [153]
Tipo: scheda tecnica (manuale d'uso del driver)
Autori: STMicroelectronics
Titolo: UM2884 — A guide to using the VL53L5CX multizone Time-of-Flight ranging sensor with wide field of view Ultra Lite Driver (ULD)
Sede e anno: STMicroelectronics, manuale d'uso UM2884, Rev 2, agosto 2021
Identificativo: UM2884 Rev 2
Link: https://core-electronics.com.au/attachments/localcontent/um2884-a-guide_75701dc7b2e.pdf (copia ospitata da un rivenditore) ; anche (rif-1): https://st.com/resource/en/user_manual/um2884-a-guide-to-using-the-vl53l5cx-multizone-timeofflight-ranging-sensor-with-a-wide-field-of-view-ultra-lite-driver-uld-stmicroelectronics.pdf
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-1, su st.com) non raggiungibile (st.com: connessione interrotta, oggi e in f3); il ruolo la dichiara «non verificata sul testo». ‖ (rif-2, sulla copia di un rivenditore) Tabella 2, «Minimum and maximum ranging frequencies»: 4x4 da 1 a 60 Hz; 8x8 da 1 a 15 Hz. In f3 era fra i «non controllati».
Usata per: «il passaggio 8×8 a 15 Hz → 4×4 a 60 Hz del VL53L5CX» (creativo-4) — `f1/e30f9e2dd4d7/CONSEGNA.md`
Usata per: scioglie «modo 4×4 a 60 Hz del VL53L5CX non verificato sul testo» — `f2/01-traduzione/SCHEDE.md` (`creativo-4`, rischi).
Note: (rif-1) conferma parziale da `st-vl53l5cx` (60 Hz di capacità massima [g]); il legame 60 Hz ↔ solo 4×4 resta non verificato. (rif-2) l'idea che lo usava (H-020) è esclusa dal ramo. Revisione del 2021, forse non l'ultima. Differenza fra i gruppi: per rif-1 il manuale era «non raggiungibile» (st.com) e il legame «60 Hz solo in 4×4» non verificato; rif-2 l'ha letto su una copia di un rivenditore (Tabella 2): il dubbio è sciolto. Per rif-1 il tipo era «documentazione di software».

### st-um3038 [154]
Tipo: scheda tecnica (manuale d'uso)
Autori: STMicroelectronics
Titolo: UM3038 — A guide to using the VL53L7CX Time-of-Flight multizone ranging sensor with 90° FoV
Sede e anno: STMicroelectronics, UM3038 Rev 2
Identificativo: UM3038 Rev 2
Link: https://www.pololu.com/file/0J1993/um3038-a-guide-to-using-the-vl53l7cx-timeofflight-multizone-ranging-sensor-with-90-fov-stmicroelectronics.pdf
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-4) [T]: stato 10 = «Range valid, but no target detected at previous range»; «status 5 is considered as 100 % valid. A status of 6 or 9 … confidence value of 50 %. All other statuses are below 50 %»; `set_i2c_address` e LPn presenti
Usata per: il primo campione dopo «nessun bersaglio» ha stato 10, fiducia sotto il 50 % (§5.5); procedura per cambiare l'indirizzo I2C con LPn (§2.3) — `f9-preproposta/07-lidar/CONSEGNA.md` ([3]); `f10-dati/02-sensori/MODELLO_SENSORE.md` (S8), `PREVISIONI.md` riga 14 **[f7–f10: non vagliato dall'arbitro]**
Note: numeri di paragrafo non ricontrollati. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### st-vl53l5cx [155]
Tipo: scheda tecnica
Autori: STMicroelectronics
Titolo: VL53L5CX — Time-of-Flight 8x8 multizone ranging sensor with wide field of view (scheda tecnica)
Sede e anno: STMicroelectronics, DS13754 Rev 2, agosto 2021 (la revisione può non essere l'ultima)
Identificativo: DS13754 Rev 2
Link: https://cdn.sparkfun.com/assets/6/e/3/0/6/vl53l5cx-datasheet.pdf (copia SparkFun; st.com non risponde)
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-1) già verificata dal curatore in f3 [g]: 45°×45°, 63° in diagonale, 400 cm; 4×4 a 30 Hz: 4,0 m al buio, 1,7 m a 5 klx. Ricontrollata oggi [g]: intestazione «DS13754 - Rev 2 - August 2021», «60 Hz frame rate capability», tabelle con 8×8 a 15 Hz e 4×4 a 30 Hz. ‖ (rif-2) Nel PDF: «63° diagonal square FoV»; «Up to 400 cm ranging»; «60 Hz frame rate capability»; «Sample rate: Up to 60 Hz». Il campo «45° × 45°» oggi non l'ho cercato (confermato in f3). Già in f3/fonti.
Usata per: campo 45°×45° (63° diag.), 400 cm; tre unità = 135° — `f1/dfac83300259/CONSEGNA.md` (§1.1, prova P-np2)
Usata per: campo orizzontale 45° fra i 7 sensori di P1 — `f1/b8262bfed263/CONSEGNA.md`
Usata per: «L5CX e L8CX: 45°×45° (r)» — `f1/985ccd9bca46/CONSEGNA.md` (§2.1)
Usata per: «45°×45° (63–65° in diagonale): tre coprono 135°», dichiarato non verificato sul testo — `f1/e30f9e2dd4d7/CONSEGNA.md` (critica 4)
Usata per: F-001, «multizona 8×8 (45°–60°)» — `f2/03-triage/TRIAGE.md` (F-001).
Usata per: «modo 4×4 a 60 Hz del VL53L5CX non verificato sul testo» — `f2/01-traduzione/SCHEDE.md` (`creativo-4`, rischi): vedi `st-um2884`.
Note: (rif-1) i numeri sono dichiarazioni del costruttore; 5 klx è la condizione di prova della scheda, non il sole pieno (f3, punto 3). (rif-2) esiste almeno una revisione più recente (un motore di ricerca indica una Rev 13 presso un distributore: non aperta).

### st-vl53l7cx [156]
Tipo: scheda tecnica
Autori: STMicroelectronics
Titolo: VL53L7CX — Time-of-Flight 8x8 multizone ranging sensor with 90° FoV
Sede e anno: STMicroelectronics, scheda DS13865, Rev 6, marzo 2023
Identificativo: DS13865 Rev 6
Link: https://www.pololu.com/file/0J1992/vl53l7cx.pdf (copia ospitata da Pololu; st.com oggi non risponde) ; anche (rif-1): https://www.st.com/en/imaging-and-photonics-solutions/vl53l7cx.html
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-1) già verificata dal curatore in f3 [g]: 60°×60° (90° diag.), 350 cm, «three sensors can cover 180° x 60°»; 3,5 m = 4×4 a 30 Hz al buio su bianco 88 %; 2,0 m = 8×8 a 15 Hz; a 5 klx 0,65 m (4×4) e 0,5 m (8×8); grigio 17 % in 8×8: 0,8 m al buio (tabelle 17 e 18). Non riaperta oggi. ‖ (rif-2) Nel PDF: «60° x 60° square field of view (FoV) (90° diagonal)»; «Up to 350 cm ranging»; «(three sensors can cover 180° x 60° FoV)»; Tabella 17 (30 Hz): bianco 88 %, al buio 3500 mm tipici, a 5 klx 650 mm tipici; Tabella 18 (15 Hz): 2000 mm al buio, 500 mm a 5 klx. Già in f3/fonti. ‖ (rif-4) [T]: PDF aperto, «DS13865 Rev 6», 940 (nm), «crosstalk», AVDD presenti; tabelle 17–18 non ricontrollate cifra per cifra; già verificata dal curatore in f3 (punto 1 di `f3/fonti/FONTI_VERIFICATE.md`)
Usata per: «60° x 60° (90° diag.), 4x4 o 8x8 zone, fino a 350 cm» (F2, marcata R) — `f1/3fff79e9c3ea/FONTI.md`, `f1/3fff79e9c3ea/CONSEGNA.md` (§1.1)
Usata per: 60°×60°, tre sensori 180°×60°; 8×8: 2,0 m al buio, 0,5 m a 5 klx, 0,8 m su grigio 17 % — `f1/985ccd9bca46/CONSEGNA.md` (§2.1, §2.2, tabella, rif. [1])
Usata per: «VL53L7CX 60°×60°» — `f1/c85dbcc51ea6/CONSEGNA.md` (§1.3, rif. [7])
Usata per: campo orizzontale 60° in P1 — `f1/b8262bfed263/CONSEGNA.md`
Usata per: F-001, tre ToF multizona non coprono 360° (135°–180°); «three sensors can cover 180° x 60°» — `f2/03-triage/TRIAGE.md` (F-001); `f2/05-selezione/SELEZIONE.md` (K-009, F-001); `f3/H-012/01-scene-dinamiche/SOLUZIONE.md` (§6, §7); `f4/H-012/05-correzioni/SOLUZIONE_V2.md` (§8); `f4/H-012/09-arbitro/VERDETTO.md` (punto 8: «scheda del costruttore: 180°»).
Usata per: K-012, «VL53L7CX 2,0 m contro 3,5 m: due modi» — `f2/01-traduzione/SCHEDE.md` (coda, (b) 12); `f2/03-triage/TRIAGE.md` (K-012); `f2/05-selezione/SELEZIONE.md` (K-012).
Usata per: «a 5 klx il VL53L7CX tiene 0,5–0,65 m» — `f3/H-012/01-scene-dinamiche/SOLUZIONE.md` (§7); `f4/H-012/05-correzioni/SOLUZIONE_V2.md` (§8).
Usata per: emissione a 940 nm; portata in 8×8 su grigio 17 % a 5 klx 0,35 m tipici (0,25 m minimi, tab. 18); nessun ingresso di trigger (B1 è AVDD); «crosstalk» è il riflesso del vetro di copertura; interfaccia I2C a 0x52 — `f9-preproposta/07-lidar/CONSEGNA.md` ([1]); `f10-dati/04-embedded/PREVISIONI.md` (E10); `f10-dati/02-sensori/MODELLO_SENSORE.md` (S7); `f10-dati/03-infrastruttura/PREVISIONI.md` (infra-P4), `AMBIENTE.md` riga 78; `f9-preproposta/01-architetto/CONSEGNA.md` riga 14 **[f7–f10: non vagliato dall'arbitro]**
Note: (rif-1) titolo esatto della scheda non riletto oggi (formulazione mia sul modello ST): controllarlo sul PDF prima di citarlo alla lettera. «350 cm» e «2,0 m» sono due modi diversi (f3, punto 2), non una discordanza. Classe laser 1 dichiarata da ST secondo `lidar`: non ricontrollata. (rif-2) che la Tabella 17 sia il modo 4×4 e la 18 il modo 8×8 lo dice f3; oggi ho letto le intestazioni «30 Hz» e «15 Hz», non la risoluzione. La revisione può non essere l'ultima. 5 klx è la condizione di prova della scheda, non il sole pieno. Valori tipici su bersaglio bianco: sul grigio e ai bordi del campo sono più bassi. (rif-4) copia di un rivenditore, non st.com; forse non è l'ultima revisione (lo dice il ruolo). Le estrapolazioni sul nero al 5 % (0,38 m, 0,30 m) sono conti del ruolo. Alcuni usi vengono dalle estensioni f7–f10: NON ancora vagliati dall'arbitro (marcati riga per riga).

### st-vl53l8cx [157]
Tipo: scheda tecnica
Autori: STMicroelectronics
Titolo: VL53L8CX — Low-power high-performance 8x8 multizone Time-of-Flight sensor (scheda tecnica)
Sede e anno: STMicroelectronics, DS14161 Rev 7, agosto 2023
Identificativo: DS14161 Rev 7
Link: https://www.pololu.com/file/0J2029/vl53l8cx.pdf (copia Pololu); citato come https://www.st.com/resource/en/datasheet/vl53l8cx.pdf (st.com non risponde)
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-1) già verificata dal curatore in f3 [g]: 45°×45°, 65° diag., 400 cm; a 5 klx 2,85 m in 4×4 a 30 Hz e 1,55 m in 8×8 a 15 Hz (bianco 88 %). Non riaperta oggi. ‖ (rif-4) [T]: PDF aperto, «DS14161 Rev 7», 940, SYNC presenti; portate non ricontrollate; già verificata dal curatore in f3 (punto 2)
Usata per: «VL53L8CX 45°×45°, 4 m» — `f1/c85dbcc51ea6/CONSEGNA.md` (§1.3, rif. [7])
Usata per: campo orizzontale 45° in P1 — `f1/b8262bfed263/CONSEGNA.md`; «L8CX: 45°×45° (r)» — `f1/985ccd9bca46/CONSEGNA.md`
Usata per: 940 nm; campo 45°; a 5 klx in 8×8 1,55 m (bianco), in 4×4 grigio 17 % 1,65 m tipici; piedino SYNC; alimentazione del nucleo a 1,8 V — `f9-preproposta/07-lidar/CONSEGNA.md` ([2]); `f10-dati/04-embedded/PREVISIONI.md` (E10); `f10-dati/02-sensori/MODELLO_SENSORE.md` (S9) **[f7–f10: non vagliato dall'arbitro]**
Note: (rif-1) titolo esatto della scheda non riletto oggi (formulazione mia sul modello ST): controllare sul PDF prima di citarlo alla lettera. (rif-4) copia di un rivenditore. Alcuni usi vengono dalle estensioni f7–f10: NON ancora vagliati dall'arbitro (marcati riga per riga).

### st-volantino-vl53l7cx-vl53l8cx [158]
Tipo: pagina di costruttore o comunicato
Autori: STMicroelectronics
Titolo: volantino VL53L7CX / VL53L8CX (titolo esatto: manca)
Sede e anno: STMicroelectronics; anno: manca
Identificativo: manca
Link: https://www.st.com.cn/resource/en/flyer/vl53l7cx-vl53l8cx-flyer.pdf
Verifica: non raggiungibile — (rif-1) (f3: «non verificabile, sostituito dalle schede»); i ruoli l'hanno vista solo nel riassunto di un motore di ricerca.
Usata per: L5CX e L8CX a 45°×45° — `f1/985ccd9bca46/CONSEGNA.md` (rif. [2]); campi dei multizona ST — `f1/b8262bfed263/CONSEGNA.md` (Fonti)
Note: non citarla; usare `st-vl53l7cx` e `st-vl53l8cx`.

### sunny-mars07a [159]
Tipo: pagina di costruttore o comunicato
Autori: Sunny Optical (identificazione dal solo riassunto del motore di ricerca)
Titolo: Mars07A (camera ToF)
Sede e anno: non verificati
Identificativo: manca
Link: https://www.sunnyaiot.com/en/product/ToF/Mars07A.html (oggi dà 404)
Verifica: vista solo nel riassunto di un motore di ricerca — (rif-2) il riassunto di oggi attribuisce alla pagina: campo ToF 120° × 56°, 224×109 a 10 fps, 0,1–2,5 m al 90 % di riflettanza, 940 nm. La pagina, aperta direttamente con due strumenti, dà 404.
Usata per: «Camere ToF: massimo 120° (Femto; Mars07A 120°×56°; Helios2 Wide 108°)» — `f2/04-torneo/TORNEO.md` (parte 1, H-007; «Non aperte»).
Note: il torneo non nominava il costruttore; «Sunny Optical» è da confermare. La conclusione (nessuna camera ToF con ≥ 130°) non dipende da questa voce: è una ricerca dichiarata non esaustiva.

### unitree-l2 [160]
Tipo: pagina di costruttore o comunicato
Autori: Unitree Robotics
Titolo: Unitree 4D LiDAR L2 (pagina prodotto)
Sede e anno: Unitree, pagina prodotto letta il 14-11-2026
Identificativo: manca
Link: https://www.unitree.com/L2
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-1) [r]: pagina aperta e dato presente: 360°×90° (96° nel modo ad angolo negativo), 30 m al 90 %, 15 m al 10 % (attribuzione della colonna dedotta dall'impaginazione), 64000 punti/s utili, 5,55 Hz, «Class 1 (IEC60825-1:2014)», ENET UDP e TTL UART, IMU a 6 assi, 419 $. ‖ (rif-2) «$419»; «360°×96°»; «Circumferential scanning frequency 5.55Hz (Customizable adjustment)»; 64 000 punti/s; «30m @90% reflectivity»; «Near blind spot 0.05m». In f3 era fra i «non controllati».
Usata per: 360°×90°, 30 m (15 m al 10 %), 64000 punti/s a 5,55 Hz, 419 $, classe 1 IEC 60825-1:2014 — `f1/985ccd9bca46/CONSEGNA.md` (tabella, lidar-2, «Sicurezza ottica», rif. [10]), `f1/985ccd9bca46/PREVISIONI.md` (P9)
Usata per: «Con 420 $ in più: Unitree L2, 3D a 360°, 5,55 Hz» — `f2/01-traduzione/SCHEDE.md` (`lidar-2`).
Note: (rif-1) dichiarazioni del costruttore; il prezzo è quello del giorno. (rif-2) prezzo di listino del costruttore al 14-11-2026, in dollari, senza spedizione né dazi: può cambiare. La pagina dichiara la tenuta a 100 klx; non verificata da nessuno. Differenza fra i gruppi: campo verticale «90° (96° nel modo ad angolo negativo)» per rif-1, «360°×96°» nella citazione di rif-2: la stessa pagina, due righe.

### waveshare-rplidar-c1 [161]
Tipo: pagina di costruttore o comunicato (rivenditore)
Autori: Waveshare (rivenditore; il sensore è di Slamtec)
Titolo: RPLIDAR C1 (pagina prodotto Waveshare, SKU 26535)
Sede e anno: waveshare.com, letta il 14-11-2026
Identificativo: Waveshare SKU 26535
Link: https://www.waveshare.com/rplidar-c1.htm
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-1) già verificata dal curatore in f3 [r] sulla pagina Slamtec (12 m al 70 %, 6 m al 10 %, 5 kHz, 10 Hz tipici, 0,72°, 40 klx). Ricontrollata oggi [r] sulla pagina Waveshare: 0,05–12 m (70 %), 0,05–6 m (10 %), 5000 Hz, 8–12 Hz (tipico 10), 0,72°, ±30 mm, «FDA Class 1», 79,99 $; la tenuta alla luce non è sulla pagina Waveshare.
Usata per: 12 m al 70 %, 6 m al 10 %; ±30 mm (da cui rumore di velocità 0,4 m/s e di accelerazione 7 m/s², calcolo del ruolo); classe 1 FDA; 5000 punti/s, 10 Hz, 0,72°; 70–80 $ — `f1/985ccd9bca46/CONSEGNA.md` (§2.5, §2.6, tabella, lidar-2, rif. [8])
Note: «±30 mm» usato come scarto tipo è un'ipotesi dichiarata del ruolo. La classe FDA è una dichiarazione del costruttore. All'unione: separata da `slamtec-rplidar-c1` (pagina delle specifiche del costruttore); nel gruppo rif-1 la chiave era `slamtec-rplidar-c1`.


---

## 3. Norme e documenti regolatori

38 voci, da [162] a [199].

### astm-f3442-25 [162]
Tipo: norma o documento regolatorio
Autori: ASTM International
Titolo: F3442-25 — Standard Specification for Detect and Avoid System Performance Requirements
Sede e anno: ASTM International, edizione 2025
Identificativo: ASTM F3442-25
Link: https://store.astm.org/f3442-25.html
Verifica: dato diverso — (rif-3) pagina aperta [g]; c'è «does not address avoidance of birds or natural hazards (for example, weather, clouds, terrain/obstacles)» e l'ambito «smaller unmanned aircraft (UA) encountering crewed aircraft»; ma al punto 1.6.1 la norma «defines a metric to assess the mitigation of a UA-to-UA mid-air collision, with specific safety performance thresholds to be addressed in future efforts». Il ruolo che la cita l'aveva vista solo in un risultato di ricerca.
Usata per: norma per velivoli piccoli, «che esclude uccelli e incontri fra droni» — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §3, S27
Note: correzione 3. Letto solo l'ambito pubblicato nella pagina del negozio; il testo della norma è a pagamento.

### chs-carta1-abbreviazioni [163]
Tipo: norma o documento regolatorio (simboli cartografici)
Autori: Canadian Hydrographic Service
Titolo: Chart 1 — Symbols, Abbreviations and Terms; sezione W, abbreviazioni
Sede e anno: Governo del Canada; edizione: non letta
Identificativo: manca
Link: https://cartes-charts.gc.ca/publications/chart1-carte1/sections/w-abbrs/abbrev-eng.html
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-4) [T]: «Position approximate» e «Position doubtful» presenti
Usata per: le carte nautiche marcano ciò che è approssimato o dubbio (PA, PD), come modello per la legenda — `f7-estensione/08-creativo/CONSEGNA.md` riga 68 **[f7–f10: non vagliato dall'arbitro]**
Note: analogia. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### codice-strada-reg-art162 [164]
Tipo: norma o documento regolatorio
Autori: Repubblica Italiana
Titolo: Regolamento di esecuzione e di attuazione del Codice della strada (D.P.R. 495/1992: numero a memoria, non verificato), articolo 162
Sede e anno: letto su un sito di divulgazione giuridica
Identificativo: art. 162 del regolamento
Link: https://leggeinchiaro.it/articolo-162-regolamento-codice-strada/
Verifica: aperta dal ruolo che la cita — (rif-4) dal curatore solo [200] e presenza di «162» nella pagina; il contenuto usato non ricontrollato
Usata per: precedente per i segnali — `f9-preproposta/09-interfacce/CONSEGNA.md` riga 80 **[f7–f10: non vagliato dall'arbitro]**
Note: sito non ufficiale; preferire Normattiva. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### colreg-regola7 [165]
Tipo: norma o documento regolatorio
Autori: International Maritime Organization
Titolo: Convention on the International Regulations for Preventing Collisions at Sea (COLREG), 1972 — Rule 7, Risk of collision
Sede e anno: IMO, 1972; letta in una riproduzione di terzi
Identificativo: COLREG, regola 7(d)(i)–(ii)
Link: https://ialacolreg.com/en/colreg/rule-7
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-4) [T]: «does not appreciably change» e «even when an appreciable bearing change is evident» presenti nella pagina
Usata per: rilevamento costante come segno di rischio di collisione, e avvertenza che il rischio può esistere anche con rilevamento che cambia a breve distanza — `f9-preproposta/06-esperto-dominio/CONSEGNA.md` riga 33 (F5) **[f7–f10: non vagliato dall'arbitro]**
Note: riproduzione non ufficiale del testo. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### dnv-imo-codice-mass [166]
Tipo: norma o documento regolatorio (notizia tecnica di una società di classifica)
Autori: DNV
Titolo: IMO MSC 111: New MASS Code adopted
Sede e anno: DNV, Technical and Regulatory News, 22 maggio 2026
Identificativo: manca
Link: https://www.dnv.com/news/2026/imo-mcs-111-new-mass-code-adopted/
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-3) [g] — «The new MASS Code was adopted as a non-mandatory instrument, with an entry into effect date of 1 July 2026»; «Applies to cargo ships only». Il ruolo che la cita l'aveva vista solo in un risultato di ricerca.
Usata per: in mare, codice MASS dell'IMO, non obbligatorio, dal 1° luglio 2026, solo navi da carico — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §3, S30
Note: fonte secondaria autorevole; il testo dell'IMO non è stato aperto.

### easa-amc-gm-2019-947 [167]
Tipo: norma o documento regolatorio
Autori: EASA
Titolo: Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 — Issue 1, Amendment 3 (allegato alla decisione ED 2025/018/R)
Sede e anno: EASA, 2025; 204 pagine
Identificativo: Annex to ED Decision 2025/018/R
Link: https://www.easa.europa.eu/sites/default/files/dfu/annex_to_ed_decision_2025-018-r_1_2.pdf
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-3) [g, sul testo del PDF] — «Detect and avoid — DAA — The capability to see, sense or detect conflicting traffic or other hazards and take the appropriate action…»; «TMPRs address the functions of detect, decide, command, execute and feedback loop»; «identify the modes of deterioration of the 'external systems' (e.g. complete loss of GNSS, GDOP/PDOP, latency issues, etc.)»; «SC-228 and/or EUROCAE WG-105»; «Specific Operations Risk Assessment (SORA) (Source: JARUS SORA v2.5)». Aperta anche dal ruolo che la cita.
Usata per: l'EASA chiede di individuare i modi di deterioramento dei sistemi esterni e i mezzi per rilevarli — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §2(e), S24
Usata per: definizione di «detect and avoid» e le sue cinque funzioni; rinvio a RTCA SC-228 ed EUROCAE WG-105; SORA 2.5 — stesso file, §3
Usata per: «detect and avoid» nelle norme è il traffico con equipaggio: da non dire per il prototipo — `f6-specializzazione/01-esperto-dominio/SPECIALIZZAZIONE.md` §6
Note: la definizione è alla voce I.53 del glossario e coincide parola per parola con la citazione del quadro, compresa la chiusa «to comply with the acceptable rules of flight». Il documento riguarda la categoria «specifica» dei droni: il prototipo non è un'operazione di volo, quindi vale come vocabolario, non come requisito applicabile.

### easa-drones-regole [168]
Tipo: norma o documento regolatorio (pagina dell'autorità)
Autori: EASA
Titolo: Drones & Air Mobility, Rules & Standards
Sede e anno: sito dell'EASA, letto il 14-11-2026
Identificativo: manca
Link: https://www.easa.europa.eu/domains/drones-air-mobility/rules-standards
Verifica: verificata dal curatore il 14-11-2026 in parte — (rif-3) in parte: pagina aperta [g]; nomina i regolamenti 2019/947 e 2019/945. Non nomina il 2021/664 né la decisione 2025/018/R. Il ruolo che la cita l'aveva vista solo in un risultato di ricerca.
Usata per: quadro europeo: regolamenti 2019/947 e 2019/945, U-space 2021/664, SORA 2.5 nella decisione 2025/018/R — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §3, S28
Usata per: le regole europee valgono per chi vola davvero — stesso file, §6
Note: correzione 9.

### easa-faq-open-category [169]
Tipo: norma o documento regolatorio (pagina di domande e risposte dell'autorità)
Autori: Agenzia dell'Unione europea per la sicurezza aerea (EASA)
Titolo: FAQ, Open Category
Sede e anno: sito dell'EASA, letto il 14-11-2026
Identificativo: manca
Link: https://www.easa.europa.eu/en/the-agency/faqs/open-category
Verifica: dato diverso — (rif-3) pagina aperta [g]; ci sono «MTOM … less than 250 g and the maximum speed is less than 19 m/s» e «drones with a speed higher than 19 m/s are only allowed to operate in open subcategory A3»; per la C2 c'è la «low-speed function» senza cifra. I «3 m/s» nella pagina non ci sono: stanno in `ue-2019-945`. Il ruolo che la cita aveva letto le cifre «in guide secondarie».
Usata per: 19 m/s tetto delle classi C0 e C1 della categoria aperta; 3 m/s modo lento della C2 — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §2(c), S19
Usata per: v_max del piccolo drone fino a 19 m/s — stesso file, §2(c); e `f6-specializzazione/01-esperto-dominio/SPECIALIZZAZIONE.md` §1 e §3.3 (fascia di 2,5 m e 3,8 m)
Note: correzione 4. Le cifre sono giuste, la fonte primaria è il regolamento.

### eurocae-ed-275 [170]
Tipo: norma o documento regolatorio (scheda di un catalogo di norme)
Autori: EUROCAE
Titolo: ED-275 — Minimum Operational Performance Standards for Airborne Collision Avoidance System Xu (ACAS Xu), Volume I e Volume II (Algorithm Design Description)
Sede e anno: EUROCAE, 1 dicembre 2020; 1.810 pagine (dalla scheda del catalogo)
Identificativo: EUROCAE ED-275
Link: https://standards.globalspec.com/std/14356966/eurocae-ed-275
Verifica: dato diverso — (rif-3) scheda aperta [g]; ED-275 è la norma del sistema anticollisione ACAS Xu, non una norma generale sul «detect and avoid». Le cifre «35 s» e «oltre un chilometro» non ci sono. Il ruolo che la cita l'aveva vista solo in un risultato di ricerca.
Usata per: norme tecniche sul «detect and avoid», insieme a DO-365 — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §3, S20
Usata per: le cifre del «restare ben distanti» — stesso file, §2(c)
Note: correzione 2. Scrivere «ED-275 (anticollisione ACAS Xu)».

### eurocontrol-acas-guide [171]
Tipo: norma o documento regolatorio (guida)
Autori: EUROCONTROL
Titolo: ACAS Guide — Airborne Collision Avoidance Systems, versione 5.0
Sede e anno: EUROCONTROL, aprile 2025 (dal frontespizio [T]; il file è nella cartella 2025-09 del sito)
Identificativo: versione 5.0 (dal nome del file)
Link: https://www.eurocontrol.int/sites/default/files/2025-09/eurocontrol-safety-acas-guide-5-0.pdf
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-4) [T]: nel PDF «No manoeuvres are permitted in response to a TA», «pilots shall respond immediately», «does not detect non-transponder equipped aircraft», «does not support operations on the ground», «assumes the worst-case», «14 NM» presenti; numeri di paragrafo e Tabella 16 (20–48 s, 15–35 s, 0,20–1,10 NM, 600–800 ft) non ricontrollati
Usata per: TA e RA sono due atti diversi; ACAS è di bordo e non aeroportuale; scale del TCAS II; il TCAS non usa probabilità — `f9-preproposta/06-esperto-dominio/CONSEGNA.md` righe 23–31 (F3) **[f7–f10: non vagliato dall'arbitro]**
Note: frontespizio letto [T]: «ACAS Guide — Airborne Collision Avoidance Systems, April 2025». Aviazione civile: passa il principio, non le soglie. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### eurocontrol-asterix-cat062 [172]
Tipo: norma o documento regolatorio
Autori: EUROCONTROL
Titolo: EUROCONTROL Specification for Surveillance Data Exchange — ASTERIX Part 9, Category 062: System Track Data
Sede e anno: EUROCONTROL; edizione 1.18 (quella letta dal ruolo, in copia strutturata non ufficiale); ultima edizione sulla pagina ufficiale: 1.21, 5-6-2025
Identificativo: ASTERIX CAT062
Link: https://www.eurocontrol.int/publication/cat062-eurocontrol-specification-surveillance-data-exchange-asterix-part-9-category-062 (ufficiale); https://zoranbosnjak.github.io/asterix-specs/specs/cat062/cats/cat1.18/definition.html (copia)
Verifica: dato diverso — (rif-3, trascrizione non ufficiale dell'edizione 1.18) [g] — voce I062/080: CST «Age of the last received track update is higher than system dependent threshold (coasting)»; CNF «0: Confirmed track, 1: Tentative track»; I062/290 «System Track Update Ages»; I062/500 «Estimated Accuracy Of Track Position». Aperta anche dal ruolo che la cita. ‖ (rif-4, pagina ufficiale e trascrizione) l'edizione corrente è la 1.21 (5 giugno 2025) [T sulla pagina ufficiale]; nella copia 1.18 ho ritrovato [T] «Age of the last received track update is higher than system dependent threshold (coasting)», il tetto 63,75 s e «Estimated Accuracies»; il PDF ufficiale non l'ha aperto nessuno
Usata per: nei dati di sorveglianza lo stato di traccia ha il bit di «coasting», confermata o provvisoria, età e accuratezze: è il vocabolario del nucleo — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §3, S31
Usata per: scambio di stato ed età della traccia fra più veicoli — `f6-specializzazione/01-esperto-dominio/SPECIALIZZAZIONE.md` §5
Usata per: primo dei due agganci sull'uscita per il giurato della società — `f6-specializzazione/01-esperto-dominio/SPECIALIZZAZIONE.md` §6; ripreso in `f6-specializzazione/03-avversario/ATTACCO_SPECIALIZZAZIONE.md` S5
Usata per: una traccia estrapolata resta in uscita con l'età (I062/290, passo 0,25 s, tetto 63,75 s), l'accuratezza stimata (I062/500) e il bit di coasting (I062/080 CST) — `f8-continuita/07-ricercatore/FONTI.md` (S16), `CONSEGNA.md` righe 26, 30, 78, 117 **[f7–f10: non vagliato dall'arbitro]**
Note: (rif-3) è una trascrizione di terzi: per un uso formale va confrontata con il documento di EUROCONTROL (non aperto). Garantisce che il vocabolario esiste; non dice che il nucleo lo rispetti: «ispirato a», mai «conforme a». (rif-4) correzione C3. Sorveglianza aerea: passa il principio, non le soglie. Differenza fra i gruppi: rif-3 descrive la trascrizione non ufficiale dell'edizione 1.18 (13 agosto 2018; trascrizione di Zoran Bosnjak, asterix-specs), rif-4 la pagina ufficiale, dove l'ultima edizione è la 1.21: tenuti titolo e link ufficiali, con la copia letta accanto. Alcuni usi vengono dalle estensioni f7–f10: NON ancora vagliati dall'arbitro (marcati riga per riga).

### faa-ac-150-5220-24 [173]
Tipo: norma o documento regolatorio (circolare), letta in un articolo di rivista
Autori: Federal Aviation Administration (articolo: Flight Safety Foundation, AeroSafety World, «Clean Sweep»)
Titolo: Advisory Circular 150/5220-24, sistemi di rilevamento degli oggetti estranei sulle piste (titolo esatto: non letto)
Sede e anno: FAA; data: non letta
Identificativo: AC 150/5220-24
Link: https://flightsafety.org/asw-article/clean-sweep/
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-4) [T]: nell'articolo compaiono «150/5220-24», una sfera, un cilindro, «1.7 in» e «4.3»; le misure esatte del cilindro (3 × 3,8 cm) non ricontrollate
Usata per: oggetti estranei di riferimento sulle piste (sfera di 4,3 cm, cilindro di 3 × 3,8 cm), sotto i 7 cm di quota minima del nucleo — `f7-estensione/05-esperto-dominio/CONSEGNA.md` righe 37 e 80 (S13) **[f7–f10: non vagliato dall'arbitro]**
Note: fonte secondaria; la circolare non è stata aperta. Nella sezione E la chiave provvisoria è [flightsafety-fod]: la pagina letta è l'articolo della Flight Safety Foundation, non la circolare. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### faa-ac-150-5220-25 [174]
Tipo: norma o documento regolatorio (circolare), letta su una pagina di costruttore
Autori: Federal Aviation Administration (pagina: Accipiter Radar)
Titolo: Advisory Circular 150/5220-25, Airport Avian Radar Systems
Sede e anno: FAA; data: non letta
Identificativo: AC 150/5220-25
Link: https://www.accipiterradar.com/faa-advisory-circular-1505220-25-airport-avian-radar
Verifica: verificata dal curatore il 14-11-2026 in parte — (rif-4) [T] solo per la presenza di «avian radar» e del numero della circolare sulla pagina del costruttore; il testo della circolare non l'ha aperto nessuno
Usata per: la FAA parla di «avian radar» a supporto della gestione della fauna, non di avvisi ai piloti — `f9-preproposta/06-esperto-dominio/CONSEGNA.md` riga 23 (F2), `PREVISIONI.md` riga 11 **[f7–f10: non vagliato dall'arbitro]**
Note: fonte secondaria e di parte (un costruttore). Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### faa-aim-2-1-6 [175]
Tipo: norma o documento regolatorio
Autori: Federal Aviation Administration
Titolo: Aeronautical Information Manual, capitolo 2, sezione 1, paragrafo 2-1-6 (Runway Status Light System)
Sede e anno: FAA; edizione: non letta; letta in una riproduzione di terzi (faa.gov ha risposto 403 al ruolo)
Identificativo: AIM 2-1-6
Link: https://www.angleofattack.com/aim/chapter-2/2-1-6/
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-4) [T]: «Two aircraft, or a surface vehicle and an aircraft, are required», «this is not clearance», «does not substitute for or convey» presenti nella riproduzione
Usata per: le luci di stato della pista si accendono per traffico osservato e non danno un'autorizzazione — `f9-preproposta/06-esperto-dominio/CONSEGNA.md` riga 37 (F6), `PREVISIONI.md` riga 27 **[f7–f10: non vagliato dall'arbitro]**
Note: non verificata sul sito FAA; l'edizione dell'AIM riprodotta non è nota. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### faa-ordine-7110-65 [176]
Tipo: norma o documento regolatorio
Autori: Federal Aviation Administration
Titolo: Order JO 7110.65, Air Traffic Control
Sede e anno: FAA; edizione: manca
Identificativo: JO 7110.65
Link: manca (faa.gov ha risposto 403 al ruolo)
Verifica: non verificata — (rif-4) (né dal ruolo né da me)
Usata per: regole sulle tracce in coasting nei sistemi del controllo del traffico — `f8-continuita/07-ricercatore/FONTI.md` (§4), `CONSEGNA.md` righe 18 e 129 **[f7–f10: non vagliato dall'arbitro]**
Note: nessuna affermazione ne dipende; la «guida amatoriale ai simboli ERAM» citata accanto non è una fonte primaria e non ha una voce. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### iec-60601-1-8 [177]
Tipo: norma o documento regolatorio
Autori: International Electrotechnical Commission
Titolo: IEC 60601-1-8 — allarmi nei dispositivi elettromedicali; sottoclausola 6.3.3.1, caratteristiche dei segnali d'allarme acustici, codifica della priorità
Sede e anno: IEC; edizione: non letta (la copia è del 2008)
Identificativo: IEC 60601-1-8, 6.3.3.1 a)
Link: https://standards.har-el.com/Projects/181701/60601-1-8/html/A2SubCl-6-3-3-1-a-priority-encoded.htm
Verifica: verificata dal curatore il 14-11-2026 in parte — (rif-4) [T] solo per la presenza della sottoclausola 6.3.3.1 «priority encoded» sulla pagina; è una copia non ufficiale di un documento di lavoro
Usata per: precedente per codificare la priorità nel suono (regola 7 della specifica delle interfacce) — `f9-preproposta/09-interfacce/CONSEGNA.md` riga 80 **[f7–f10: non vagliato dall'arbitro]**
Note: non è il testo della norma in vigore. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### iec-60825-1 [178]
Tipo: norma o documento regolatorio
Autori: International Electrotechnical Commission
Titolo: IEC 60825-1:2014 — Safety of laser products – Part 1: Equipment classification and requirements (titolo a memoria, non verificato oggi)
Sede e anno: IEC, edizione 3.0, 2014
Identificativo: IEC 60825-1:2014
Link: manca (nei file è citata solo attraverso la pagina `unitree-l2`)
Verifica: non verificata — (rif-1) (testo della norma a pagamento, non aperto; che la pagina Unitree la citi è verificato oggi [r]).
Usata per: «tutti i sensori citati sono dichiarati classe 1 (ST, C1 FDA, L2 IEC 60825-1:2014; Femto Bolt e RealSense: non verificato)» — `f1/985ccd9bca46/CONSEGNA.md` («Sicurezza ottica»)
Note: citazione indiretta: prova che il costruttore dichiara la classe, non che il prodotto la rispetti. La «classe 1 FDA» rimanda al regolamento statunitense sui laser, che nessun file cita con un identificativo: manca.

### imo-msc192-79 [179]
Tipo: norma o documento regolatorio
Autori: International Maritime Organization, Maritime Safety Committee
Titolo: Resolution MSC.192(79) — Adoption of the revised performance standards for radar equipment
Sede e anno: IMO, 2004
Identificativo: MSC.192(79)
Link: https://law.resource.org/pub/us/cfr/ibr/inc/imo/imo.msc.192.2004.pdf
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-4) [T]: nel PDF «Tracked Target Accuracy» e «…last position should be clearly indicated on the display» presenti; i valori della Tabella 3 (11°, 1,0 NM; 3°, 0,3 NM) non ricontrollati: trovati dal ruolo (A-g)
Usata per: accuratezza dichiarata di una traccia al 95 % e avviso di perdita con l'ultima posizione — `f8-continuita/07-ricercatore/FONTI.md` (S17), `CONSEGNA.md` righe 78 e 117 **[f7–f10: non vagliato dall'arbitro]**
Note: copia su un archivio di terzi, non il sito IMO. Nel PDF il titolo è «ADOPTION OF THE REVISED PERFORMANCE STANDARDS…» [T]; il seguito («for radar equipment») è a memoria. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### iso-10218-2 [180]
Tipo: norma o documento regolatorio
Autori: International Organization for Standardization
Titolo: ISO 10218-2:2025 (titolo: manca)
Sede e anno: ISO; 2025 secondo il ruolo: non verificato
Identificativo: ISO 10218-2:2025
Link: manca (testo a pagamento)
Verifica: vista solo nel riassunto di un motore di ricerca — (rif-4) iso.org ha risposto 403 al curatore; dal ruolo: vista solo nel riassunto di un motore di ricerca
Usata per: «ISO/TS 15066 è confluita in ISO 10218-2:2025» — `f9-preproposta/06-esperto-dominio/CONSEGNA.md` righe 69 e 87 **[f7–f10: non vagliato dall'arbitro]**
Note: All'unione: voce separata da `iso-ts-15066`, dove rif-4 la teneva. La confluenza non è verificata su una fonte primaria. Nella sezione E la chiave provvisoria è [iso-10218-2], «non letta». Citata solo nelle estensioni f7–f10: NON ancora vagliata dall'arbitro.

### iso-13855 [181]
Tipo: norma o documento regolatorio
Autori: International Organization for Standardization
Titolo: ISO 13855 — Safety of machinery — Positioning of safeguards with respect to the approach of the human body (titolo a memoria: non verificato)
Sede e anno: ISO; edizione 2024 secondo il ruolo
Identificativo: ISO 13855:2024
Link: manca (testo a pagamento)
Verifica: vista solo nel riassunto di un motore di ricerca — (rif-4) (dal ruolo); non cercata da me
Usata per: v_H = 1,6 m/s; C = 0,85 m e il termine d'incertezza — `f9-preproposta/06-esperto-dominio/CONSEGNA.md` righe 69 e 87 **[f7–f10: non vagliato dall'arbitro]**
Note: 1,6 m/s è confermato in `marvel2017` [T]; C = 0,85 m resta non verificato, e con esso i 2,80 m e 1,68 m calcolati dal ruolo. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### iso-3691-4 [182]
Tipo: norma o documento regolatorio (scheda di un catalogo di norme)
Autori: ISO (recepita come EN ISO dal CEN)
Titolo: EN ISO 3691-4:2023 — Industrial trucks — Safety requirements and verification — Part 4: Driverless industrial trucks and their systems
Sede e anno: ISO, 2023
Identificativo: ISO 3691-4:2023
Link: https://genorma.com/en/standards/en-iso-3691-4-2023
Verifica: verificata dal curatore il 14-11-2026 in parte — (rif-3) [g], per il solo titolo. Il ruolo che la cita l'aveva vista solo in un risultato di ricerca.
Usata per: norma di riferimento per i veicoli terrestri senza conducente — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §3, S29
Note: catalogo di terzi; il contenuto della norma non è stato letto. Riguarda i carrelli industriali senza conducente, non i rover in generale.

### iso-9241-303 [183]
Tipo: norma o documento regolatorio
Autori: International Organization for Standardization
Titolo: ISO 9241-303 — Ergonomics of human-system interaction — Requirements for electronic visual displays (titolo a memoria: non verificato)
Sede e anno: ISO; edizione: manca
Identificativo: ISO 9241-303
Link: manca (a pagamento)
Verifica: non verificata — (rif-4) (il ruolo dichiara «a pagamento, non aperta»)
Usata per: altezza dei caratteri di 16–22 minuti d'arco — `f9-preproposta/09-interfacce/CONSEGNA.md` riga 77 **[f7–f10: non vagliato dall'arbitro]**
Note: la cifra è a memoria del ruolo. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### iso-ts-15066 [184]
Tipo: norma o documento regolatorio
Autori: International Organization for Standardization
Titolo: ISO/TS 15066 — Robots and robotic devices — Collaborative robots (titolo ed edizione a memoria: non verificati)
Sede e anno: ISO; edizione 2016 secondo un ruolo, a memoria: non verificato
Identificativo: ISO/TS 15066
Link: manca nei file (testo a pagamento); la pagina di `therobotreport-veo` rimanda a https://www.iso.org/standard/62996.html (indirizzo letto il 14-11-2026 nel sorgente di quella pagina; non aperto)
Verifica: non raggiungibile — (rif-1) non verificata (testo a pagamento, non aperto; citata nei file solo attraverso F26). ‖ (rif-4) (iso.org ha risposto 403 oggi); dal ruolo: vista solo nel riassunto di un motore di ricerca, contenuto letto tramite `marvel2017`
Usata per: F26: distanza protettiva con incertezza di misura e latenza — `f1/3fff79e9c3ea/FONTI.md`, `f1/3fff79e9c3ea/CONSEGNA.md` (§1.8)
Usata per: sorveglianza di velocità e separazione come concetto consolidato per aree condivise; «confluita in ISO 10218-2:2025» — `f9-preproposta/06-esperto-dominio/CONSEGNA.md` righe 69 e 87, `PREVISIONI.md` riga 12; `f7-estensione/05-esperto-dominio/PREVISIONI.md` riga 15 e `CONSEGNA.md` riga 21 **[f7–f10: non vagliato dall'arbitro]**
Note: (rif-1) citazione indiretta. Se l'affermazione entra nel documento finale va letta la norma, non la rassegna. (rif-4) la confluenza nella 10218-2:2025 non è verificata su una fonte primaria. All'unione: ISO 10218-2:2025, che rif-4 teneva in questa voce, ha una voce sua (`iso-10218-2`). Anno 2016: a memoria di un ruolo, non verificato. Alcuni usi vengono dalle estensioni f7–f10: NON ancora vagliati dall'arbitro (marcati riga per riga).

### it-legge-185-1990 [185]
Tipo: norma o documento regolatorio
Autori: Repubblica Italiana
Titolo: Legge 9 luglio 1990, n. 185 (controllo dell'esportazione, importazione e transito dei materiali di armamento)
Sede e anno: 1990
Identificativo: legge 185/1990
Link: manca nei file (citata tramite S37: https://www.esteri.it/it/ministero/struttura/uama/)
Verifica: verificata dal curatore il 14-11-2026 in parte — (rif-3) per la sola esistenza e l'oggetto [g, dalla pagina del Ministero]. Il testo della legge non è stato aperto.
Usata per: esportazione di materiali d'armamento — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §6, S37
Note: il titolo fra parentesi è una descrizione, non il titolo ufficiale.

### maeci-uama [186]
Tipo: norma o documento regolatorio (pagina dell'autorità)
Autori: Ministero degli Affari Esteri e della Cooperazione Internazionale
Titolo: Autorità Nazionale UAMA: Materiali d'Armamento e a Duplice Uso
Sede e anno: sito del Ministero, letto il 14-11-2026
Identificativo: manca
Link: https://www.esteri.it/it/ministero/struttura/uama/
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-3) [g] — titolo dell'autorità; «Il controllo dell'esportazione e importazione di materiali d'armamento è disciplinato dalla Legge 9 luglio 1990, n.185»; sezione sul duplice uso. Il regolamento 2021/821 non è nominato in questa pagina. Il ruolo che la cita l'aveva vista solo in un risultato di ricerca.
Usata per: esportazione e duplice uso: l'autorità italiana è l'UAMA — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §6, S37
Note: dice chi vigila; non dice se un prototipo di componenti commerciali rientri nelle voci controllate (nel quadro: non verificato, lo valuta la società).

### noaa-nhc-cono [187]
Tipo: norma o documento regolatorio (definizione ufficiale di un prodotto)
Autori: NOAA, National Hurricane Center
Titolo: Definition of the NHC Track Forecast Cone
Sede e anno: NHC; pagina con i raggi del 2026
Identificativo: manca
Link: https://www.nhc.noaa.gov/aboutcone.shtml
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-4) [T]: «…the area swept out by a set of circles… two-thirds of historical official forecast errors over a 5-year sample fall within the circle» presente
Usata per: il cono come area spazzata da cerchi tarati sui due terzi degli errori storici — `f8-continuita/09-creativo/CONSEGNA.md` riga 84 **[f7–f10: non vagliato dall'arbitro]**
Note: il «cerchio di massimo allontanamento» e la verifica a posteriori dei meteorologi restano non verificati (lo dice il ruolo). Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### rtca-do-365 [188]
Tipo: norma o documento regolatorio (scheda di un catalogo di norme)
Autori: RTCA
Titolo: DO-365C — Minimum Operational Performance Standards (MOPS) for Detect and Avoid (DAA) Systems
Sede e anno: RTCA, 15 settembre 2022; 840 pagine (dalla scheda del catalogo)
Identificativo: RTCA DO-365C
Link: https://standards.globalspec.com/std/14562761/do-365c
Verifica: verificata dal curatore il 14-11-2026 in parte — (rif-3, scheda di catalogo di DO-365C) in parte: scheda aperta [g]; titolo, ente, data e stato («active, Most Current») ci sono. Le cifre «35 s» e «oltre un chilometro» nella scheda non ci sono: non verificate. Il ruolo che la cita l'aveva vista solo in un risultato di ricerca. ‖ (rif-4, sola sigla DO-365) vista solo nel riassunto di un motore di ricerca (dal ruolo); sulla pagina di `nasa-wellclear` la sigla non compare [T]
Usata per: il «restare ben distanti» dal traffico con equipaggio ragiona su 35 s e oltre un chilometro: un'altra scala — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §2(c), S20
Usata per: norme tecniche sul «detect and avoid» — stesso file, §3
Usata per: tempi degli avvisi per i velivoli senza equipaggio — `f9-preproposta/06-esperto-dominio/CONSEGNA.md` riga 87 **[f7–f10: non vagliato dall'arbitro]**
Note: (rif-3) correzione 2. La norma è a pagamento: la scheda garantisce che esiste e di che cosa tratta, non il contenuto. Le due cifre non vanno scritte in un documento per la giuria finché non hanno una fonte aperta. (rif-4) nessuna cifra citata. Differenza fra i gruppi: rif-4 l'aveva solo come sigla «DO-365» vista in un riassunto di ricerca; rif-3 ha aperto la scheda di catalogo dell'edizione DO-365C: tenuti i dati di rif-3. Alcuni usi vengono dalle estensioni f7–f10: NON ancora vagliati dall'arbitro (marcati riga per riga).

### ue-2017-745 [189]
Tipo: norma o documento regolatorio
Autori: Parlamento europeo e Consiglio
Titolo: Regolamento (UE) 2017/745 relativo ai dispositivi medici, articolo 2 (definizioni), punto 1
Sede e anno: Gazzetta ufficiale dell'Unione europea, 2017; letto nella versione del 31-01-2020 della copia britannica
Identificativo: regolamento (UE) 2017/745
Link: https://www.legislation.gov.uk/eur/2017/745/article/2/2020-01-31
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-3) [g] — «'medical device' means any instrument, apparatus, appliance, software … intended by the manufacturer to be used … for … diagnosis, monitoring, treatment, alleviation of, or compensation for, an injury or disability». Aperta anche dal ruolo che la cita.
Usata per: cautela sul profilo assistivo: dispositivo medico è ciò che il fabbricante destina, fra l'altro, a «compensation for, an injury or disability»; se un ausilio all'orientamento vi rientri è non verificato — `f6-specializzazione/01-esperto-dominio/SPECIALIZZAZIONE.md` §1
Note: copia non ufficiale e ferma al 2020 (lo dice anche il ruolo). La citazione prova la definizione, non la classificazione del prototipo: quella resta non risolta e la decide un esperto regolatorio.

### ue-2019-945 [190]
Tipo: norma o documento regolatorio
Autori: Commissione europea
Titolo: Regolamento delegato (UE) 2019/945 relativo ai sistemi aeromobili senza equipaggio e agli operatori di paesi terzi di sistemi aeromobili senza equipaggio
Sede e anno: Gazzetta ufficiale dell'Unione europea, 2019; allegato, parti 1–3
Identificativo: regolamento delegato (UE) 2019/945
Link: https://www.legislation.gov.uk/eur/2019/945/annex (copia britannica, non ufficiale per l'Unione; EUR-Lex oggi non raggiungibile)
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-3) [g, sulla copia britannica] — parte 1 e parte 2: «have a maximum speed in level flight of 19 m/s»; parte 3, punto 9: «be equipped with a low-speed mode selectable by the remote pilot and limiting the ground speed to no more than 3 m/s». Non citata con un link dai ruoli: è la fonte primaria delle cifre di S19.
Usata per: 19 m/s (classi C0 e C1) e 3 m/s (modo lento della C2) — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §2(c) (lì attribuite a S19)
Usata per: fra i regolamenti del quadro europeo sui droni — stesso file, §3
Note: la copia britannica è il testo «conservato» dopo l'uscita dall'Unione ed è stata emendata nel Regno Unito (la pagina cita un atto del 2025): le tre frasi vanno riconfermate sul testo consolidato dell'Unione prima di un uso formale. Il titolo italiano qui sopra è una mia resa, non trascritto dalla Gazzetta.

### ue-2019-947 [191]
Tipo: norma o documento regolatorio
Autori: Commissione europea
Titolo: Regolamento di esecuzione (UE) 2019/947 relativo a norme e procedure per l'esercizio di aeromobili senza equipaggio
Sede e anno: Gazzetta ufficiale dell'Unione europea, 2019
Identificativo: regolamento di esecuzione (UE) 2019/947
Link: manca nei file (citato tramite S28 e S24)
Verifica: verificata dal curatore il 14-11-2026 in parte — (rif-3) per la sola esistenza e il ruolo [g] — l'intestazione di S24 è «AMC & GM to Regulation (EU) 2019/947 — Issue 1, Amendment 3» e la pagina dell'EASA dice che le regole per i droni civili stanno «in EU Regulations 2019/947 and 2019/945». Il testo del regolamento non è stato aperto.
Usata per: quadro europeo sui droni — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §3 e §6 («le regole europee valgono per chi vola davvero»)
Note: nessuna cifra del progetto viene da qui. Il titolo italiano è una mia resa.

### ue-2021-664 [192]
Tipo: norma o documento regolatorio
Autori: Commissione europea
Titolo: Regolamento di esecuzione (UE) 2021/664 (quadro normativo per lo U-space)
Sede e anno: Gazzetta ufficiale dell'Unione europea, 2021; il link punta alla versione consolidata del 22-02-2026
Identificativo: regolamento di esecuzione (UE) 2021/664
Link: https://eur-lex.europa.eu/eli/reg_impl/2021/664/2026-02-22/eng/pdf
Verifica: non raggiungibile — (rif-3) EUR-Lex oggi risponde senza contenuto alle richieste automatiche (codice 202), sia in lettura diretta sia con lo strumento di lettura. Vista solo nel riassunto di un motore di ricerca, come già dal ruolo che la cita.
Usata per: quadro europeo: U-space — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §3, S28
Note: nessuna cifra del progetto ne dipende. Il titolo fra parentesi è una mia descrizione, non il titolo ufficiale.

### ue-2021-821 [193]
Tipo: norma o documento regolatorio
Autori: Parlamento europeo e Consiglio
Titolo: Regolamento (UE) 2021/821 (regime dell'Unione di controllo delle esportazioni dei prodotti a duplice uso)
Sede e anno: Gazzetta ufficiale dell'Unione europea, 2021
Identificativo: regolamento (UE) 2021/821
Link: https://eur-lex.europa.eu/EN/legal-content/summary/dual-use-export-controls.html
Verifica: verificata dal curatore il 14-11-2026 in parte — (rif-3) in parte: la sintesi di EUR-Lex non è raggiungibile; il numero e l'oggetto sono confermati [g] da una pagina della Commissione europea (https://policy.trade.ec.europa.eu/help-exporters-and-importers/exporting-dual-use-items_en): «Regulation (EU) 2021/821 governs the EU's export control regime». Il ruolo che la cita l'aveva vista solo in un risultato di ricerca.
Usata per: esportazione e duplice uso — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §6, S37
Note: le voci per droni e camere termiche restano non verificate, come nel quadro. Il titolo fra parentesi è una descrizione.

### ue-2023-1230 [194]
Tipo: norma o documento regolatorio
Autori: Parlamento europeo e Consiglio
Titolo: Regolamento (UE) 2023/1230 relativo alle macchine (il link punta a una rettifica del 4 luglio 2023)
Sede e anno: Gazzetta ufficiale dell'Unione europea, 2023
Identificativo: regolamento (UE) 2023/1230
Link: https://eur-lex.europa.eu/eli/reg/2023/1230/corrigendum/2023-07-04/oj/eng
Verifica: verificata dal curatore il 14-11-2026 in parte — (rif-3) in parte: EUR-Lex non è raggiungibile; la data è confermata [g] da una pagina della Commissione europea (https://single-market-economy.ec.europa.eu/sectors/mechanical-engineering/machinery_en): «All machinery placed on the EU market before 20 January 2027 must comply with the current Machinery Directive 2006/42/EC». «Il primo a nominare le macchine mobili autonome»: non verificato. Il ruolo che la cita l'aveva vista solo in un risultato di ricerca.
Usata per: a terra nessuna norma dedicata; regolamento macchine dal 20 gennaio 2027, il primo a nominare le macchine mobili autonome — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §3, S29
Note: correzione 10. Il link citato porta a una rettifica, non al testo: per citare il regolamento conviene il suo indirizzo proprio.

### ue-2024-1689 [195]
Tipo: norma o documento regolatorio
Autori: Parlamento europeo e Consiglio
Titolo: Regolamento sull'intelligenza artificiale, articolo 2 (ambito di applicazione)
Sede e anno: Gazzetta ufficiale dell'Unione europea, 2024
Identificativo: regolamento (UE) 2024/1689 — numero non letto oggi su una pagina: da riconfermare
Link: manca nei file (citato tramite S38); testo dell'articolo letto su una copia non ufficiale: https://artificialintelligenceact.eu/article/2/
Verifica: verificata dal curatore il 14-11-2026 in parte — (rif-3) in parte: copia non ufficiale aperta [g] — «This Regulation does not apply to AI systems where and in so far they are placed on the market, put into service, or used with or without modification exclusively for military, defence or national security purposes, regardless of the type of entity carrying out those activities». Il testo ufficiale (EUR-Lex) non è raggiungibile; il numero del regolamento non l'ho letto oggi.
Usata per: il regolamento esclude i sistemi a uso esclusivamente militare, di difesa o di sicurezza nazionale — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §6 (lì attribuito a S38)
Note: voce aggiunta da me come fonte primaria di ciò che il quadro prende da un blog. «Il duplice uso resta dentro» è la lettura corrente di «exclusively», non una frase del testo.

### us-49cfr-236-205 [196]
Tipo: norma o documento regolatorio
Autori: Stati Uniti, Federal Railroad Administration
Titolo: 49 CFR § 236.205 — Signal control circuits; requirements
Sede e anno: Code of Federal Regulations, titolo 49, parte 236; 33 FR 19684 (25-12-1968), modificato da 49 FR 3385 (26-1-1984)
Identificativo: 49 CFR 236.205
Link: citato come https://www.customsmobile.com/regulations/49/236.205 (non aperto); letto su https://www.law.cornell.edu/cfr/text/49/236.205 (ecfr.gov reindirizza a un controllo anti-automa)
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-1) [r]: pagina del Legal Information Institute aperta; il segnale che governa l'ingresso in un blocco deve mostrare l'aspetto più restrittivo quando, fra l'altro, il relè di binario è diseccitato o il circuito di comando del segnale è senza energia.
Usata per: analogia di creativo-1: il relè di binario diseccitato dà l'aspetto più restrittivo; il «via libera» esiste solo finché arriva energia — `f1/e30f9e2dd4d7/CONSEGNA.md`
Note: il testo regolatorio sostiene l'analogia; «il via libera esiste solo finché arriva energia» è la lettura del ruolo. Copia non ufficiale del testo (l'edizione ufficiale non è stata raggiunta).

### us-brevetto-11846916 [197]
Tipo: norma o documento regolatorio (brevetto)
Autori: Scott Denenberg, Clara Vu, Patrick Sobalvarro, Lev Persits, Ilya A. Kriveshko, Elliot Simon, Alberto Moel, Patrick J. Foy, Justin Bronder (inventori); titolare originario Veo Robotics, Inc.
Titolo: System architecture for safety applications
Sede e anno: brevetto degli Stati Uniti US 11846916 B2, depositato il 22-11-2022, concesso il 19-12-2023
Identificativo: US 11846916 B2
Link: https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11846916 ; letto su https://patents.google.com/patent/US11846916B2/en
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-1) [r]: pagina di Google Patents aperta (primi 100 000 caratteri); nel sommario e nelle rivendicazioni 6 e 22: «marking as occupied the volumes corresponding to a terminus of the ray path, and marking as unknown any volumes beyond the occlusion along the ray path»; volumi occupati, non occupati o sconosciuti.
Usata per: F27: voxel occupati, non occupati o sconosciuti oltre un'occlusione («tre stati per i voxel») — `f1/3fff79e9c3ea/FONTI.md`, `f1/3fff79e9c3ea/CONSEGNA.md` (§1.8)
Note: è una rivendicazione di brevetto, non un metodo validato (lo dice già FONTI.md). Possibili vincoli di proprietà intellettuale sull'idea dei tre stati in ambito industriale: da portare all'analista normativo. Il PDF dell'ufficio brevetti non è stato aperto.

### w3c-wcag22-contrasto-non-testuale [198]
Tipo: norma o documento regolatorio (documento esplicativo)
Autori: W3C, Web Accessibility Initiative
Titolo: Understanding Success Criterion 1.4.11: Non-text Contrast (WCAG 2.2)
Sede e anno: W3C; data della pagina: non letta
Identificativo: WCAG 2.2, criterio 1.4.11
Link: https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-4) [T]: rapporto «3:1» presente
Usata per: contrasto minimo 3:1 per gli elementi grafici — `f9-preproposta/09-interfacce/CONSEGNA.md` riga 80 **[f7–f10: non vagliato dall'arbitro]**
Note: scritta per il web; qui usata per analogia. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### w3c-wcag22-uso-del-colore [199]
Tipo: norma o documento regolatorio (documento esplicativo)
Autori: W3C, Web Accessibility Initiative
Titolo: Understanding Success Criterion 1.4.1: Use of Color (WCAG 2.2)
Sede e anno: W3C; data della pagina: non letta
Identificativo: WCAG 2.2, criterio 1.4.1
Link: https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-4) [T]: «not used as the only visual means» presente
Usata per: il colore non deve essere l'unico mezzo per distinguere gli stati — `f9-preproposta/09-interfacce/CONSEGNA.md` riga 80 **[f7–f10: non vagliato dall'arbitro]**
Note: scritta per il web; qui usata per analogia. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.


---

## 4. Documentazione di software e depositi di codice

46 voci, da [200] a [245].

### anybotics-grid-map [200]
Tipo: deposito di codice
Autori: ANYbotics (in origine P. Fankhauser, ETH: a memoria, non verificato)
Titolo: grid_map
Sede e anno: GitHub; commit non annotato
Identificativo: manca
Link: https://github.com/ANYbotics/grid_map
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-4) [T]: «BSD» e «circular buffer» presenti nella pagina del deposito
Usata per: mappe a più strati con memoria circolare, come riferimento vicino alla struttura dati della bozza — `bozza_iniziale/Proposta MLE Matrice Bayesiana (1).md` righe 1891, 1966, 2048, 2689, 2932 **[file esterno alla convocazione]**
Note: la bozza non ne trae cifre. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### basalt [201]
Tipo: deposito di codice
Autori: Vladyslav Usenko e collaboratori (TU München)
Titolo: Basalt (copia speculare su GitHub; il deposito principale è su GitLab)
Sede e anno: GitHub, ultimo aggiornamento marzo 2026
Identificativo: VladyslavUsenko/basalt
Link: https://github.com/VladyslavUsenko/basalt
Verifica: verificata dal curatore il 14-11-2026 in parte — (rif-3) in parte: pagina aperta [m, g]; licenza BSD-3-Clause («The code is provided under a BSD 3-clause license»); «Tutorial on Camera-IMU and Motion capture calibration with Realsense T265». «Anche senza IMU»: non cercato nel testo, non verificato. Aperta anche dal ruolo che la cita.
Usata per: componente aperto per l'odometria: camera più IMU, licenza BSD 3, tutorial sulla T265 — `f6-specializzazione/02-slam/MOTO_PROPRIO.md` §2(b)
Note: il LEGGIMI avverte che il codice di terzi incluso ha licenze diverse.

### bonxai [202]
Tipo: deposito di codice
Autori: Davide Faconti
Titolo: Bonxai
Sede e anno: GitHub, ramo `main`; commit non annotato
Identificativo: manca
Link: https://github.com/facontidavide/Bonxai
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-4) [T]: nel README «Bonxai_Create 1165 us», «Octomap_Create 25522 us», «Benchmark (preliminary)», «Sparse», «Unbounded»; «MPL» presente nella pagina del deposito
Usata per: creazione 1165 µs contro 25 522 di OctoMap («preliminary»); struttura «Sparse» e «Unbounded»; licenza MPL-2.0 — `f7-estensione/05-esperto-dominio/CONSEGNA.md` righe 17, 28 e 80 (S4) **[f7–f10: non vagliato dall'arbitro]**
Note: l'autore stesso avverte: «Take these numbers with a grain of salt». Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### espressif-vl53l7cx-libreria [203]
Tipo: documentazione di software (libreria di terzi)
Autori: grrtzm (registro dei componenti Espressif)
Titolo: v53l7cx-library, versione 1.0.6, esempio `example_02_get_set_params`
Sede e anno: components.espressif.com; data: non letta
Identificativo: versione 1.0.6
Link: https://components.espressif.com/components/grrtzm/v53l7cx-library/versions/1.0.6/examples/example_02_get_set_params
Verifica: verificata dal curatore il 14-11-2026 in parte — (rif-4) [T] solo per la presenza di «B1» e «sync» nella pagina
Usata per: una libreria di terzi elenca una funzione di sincronia su «B1», che la scheda Rev 6 non ha — `f9-preproposta/07-lidar/CONSEGNA.md` §6 ([11]) **[f7–f10: non vagliato dall'arbitro]**
Note: contraddice la scheda: il ruolo la tiene «non verificato», giustamente. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### ethz-voxblox [204]
Tipo: deposito di codice
Autori: ETH Zürich, Autonomous Systems Lab
Titolo: voxblox
Sede e anno: GitHub; commit non annotato
Identificativo: manca
Link: https://github.com/ethz-asl/voxblox
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-4) [T] per la licenza: «BSD» presente nella pagina del deposito
Usata per: licenza BSD-3, distanza con segno troncata a strati — `f7-estensione/05-esperto-dominio/CONSEGNA.md` righe 25 e 80 (S2) **[f7–f10: non vagliato dall'arbitro]**
Note: la frase sul tempo reale è in `oleynikova2017`. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### fast-lio [205]
Tipo: deposito di codice
Autori: HKU MaRS Lab
Titolo: FAST-LIO — A computationally efficient and robust LiDAR-inertial odometry (LIO) package
Sede e anno: GitHub, ultimo aggiornamento ottobre 2026
Identificativo: hku-mars/FAST_LIO
Link: https://github.com/hku-mars/FAST_LIO
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-3) [m, g] — licenza GPL-2.0; «Support ARM-based platforms including Khadas VIM3, Nivida TX2, Raspberry Pi 4B(8G RAM)»; nel LEGGIMI «Mid-360» non compare. Aperta anche dal ruolo che la cita.
Usata per: componente aperto: LiDAR più IMU, GPL-2.0, gira su piattaforme ARM; Mid-360 non nominato — `f6-specializzazione/02-slam/MOTO_PROPRIO.md` §2(b)
Note: «Nivida» è scritto così nel LEGGIMI.

### foundationvision-bytetrack [206]
Tipo: deposito di codice
Autori: FoundationVision (deposito ufficiale di ByteTrack; l'articolo non è citato nei file: manca)
Titolo: ByteTrack (README del deposito)
Sede e anno: GitHub, letto il 14-11-2026 (in f1 e f3)
Identificativo: manca
Link: https://github.com/FoundationVision/ByteTrack
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-1) già verificata dal curatore in f3 [g]: licenza MIT; «30 FPS running speed on a single V100 GPU» (rilevatore compreso). Aperta anche dal ruolo. Non riaperta oggi.
Usata per: F15: tracciatori classici con licenza MIT; 30 FPS su V100 — `f1/3fff79e9c3ea/FONTI.md`, `f1/3fff79e9c3ea/CONSEGNA.md` (§1.4)
Note: i 30 FPS comprendono il rilevatore e sono su GPU V100: non dicono niente della CPU.

### kiss-icp [207]
Tipo: deposito di codice
Autori: PRBonn (Università di Bonn)
Titolo: KISS-ICP — A LiDAR odometry pipeline that just works
Sede e anno: GitHub, ultimo aggiornamento giugno 2026
Identificativo: PRBonn/kiss-icp
Link: https://github.com/PRBonn/kiss-icp
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-3) [m, g] — licenza MIT; «pip install kiss-icp». Aperta anche dal ruolo che la cita.
Usata per: componente aperto: solo LiDAR, licenza MIT, installabile con `pip` — `f6-specializzazione/02-slam/MOTO_PROPRIO.md` §2(b)
Note: serve un LiDAR, che la squadra non ha nel nucleo.

### ldrobot-ldlidar-stl-sdk [208]
Tipo: deposito di codice
Autori: LDROBOT (organizzazione `ldrobotSensorTeam` su GitHub)
Titolo: ldlidar_stl_sdk (nome del deposito; titolo del README: non letto)
Sede e anno: GitHub; commit non annotato
Identificativo: manca
Link: https://github.com/ldrobotSensorTeam/ldlidar_stl_sdk
Verifica: aperta dal ruolo che la cita — (unione, 16:45) il file che la cita la mette fra le «Fonti (aperte oggi)»; dal curatore solo [200]. Non era in nessuno dei quattro elenchi parziali: trovata dal controllo di completezza sui link.
Usata per: SDK per il LiDAR LD19 nell'inventario dei sensori («SDK Slamtec (BSD) [15], LD19 [16]; seriale USB. 30–60 min») — `f10-dati/04-embedded/INVENTARIO_E_DECISIONE.md` righe 29 e 75 **[f7–f10: non vagliato dall'arbitro]**
Note: Licenza e versione non lette. L'SDK di Slamtec citato accanto ([15], https://github.com/Slamtec/rplidar_sdk) sta nella voce `slamtec-rplidar-c1`. Citata solo nelle estensioni f7–f10: NON ancora vagliata dall'arbitro.

### librealsense [209]
Tipo: documentazione di software
Autori: RealSense (già Intel RealSense)
Titolo: librealsense — `rs_frame.h`, `doc/frame_metadata.md`, `doc/sample-data.md`, `doc/post-processing-filters.md`, note della versione v2.59.1
Sede e anno: GitHub, ramo `master` (commit non annotato); v2.59.1 dell'11-10-2026 secondo il ruolo
Identificativo: v2.59.1
Link: https://github.com/IntelRealSense/librealsense/blob/master/include/librealsense2/h/rs_frame.h ; https://github.com/IntelRealSense/librealsense/blob/master/doc/frame_metadata.md ; https://github.com/realsenseai/librealsense/blob/master/doc/sample-data.md ; https://github.com/realsenseai/librealsense/releases/tag/v2.59.1
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-4) [T]: in `rs_frame.h` «Timestamp of the middle of sensor's exposure calculated by device» e `RS2_TIMESTAMP_DOMAIN_GLOBAL_TIME` («…converted to OS system clock…»); nelle note della v2.59.1 «Ubuntu 26.04/24.04/22.04/20.04», «Kernel versions: 6.[2, 5, 8, 11, 14]», «L515 … v2.50.0 validated, v2.54.2 supports but not validated»; in `frame_metadata.md` «kernel» e «patch» presenti
Usata per: marca di metà esposizione e dominio dell'orologio — `f9-preproposta/02-tempo-reale/CONSEGNA.md` riga 64; supporto dell'L515 e dei kernel (il 7.3 della macchina non è in elenco) — `f10-dati/04-embedded/PREVISIONI.md` (E4), `INVENTARIO_E_DECISIONE.md` ([2]); file di esempio — `f10-dati/01-ricercatore/DATI_PUBBLICI.md` §2; `f10-dati/02-sensori/MODELLO_SENSORE.md` (S4, S5) **[f7–f10: non vagliato dall'arbitro]**
Note: il deposito è passato da `IntelRealSense` a `realsenseai` (rinvio). Lo stato odierno dei metadati su Linux è «non verificato» per il ruolo. Licenza Apache-2.0 non riletta. Voce di gruppo: nella sezione D le chiavi provvisorie [librealsense-filtri] e [librealsense-metadati] indicano due file di questo deposito; nella sezione F [realsense-librealsense] indica le note della versione 2.59.1. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### linux-gspca-kinect [210]
Tipo: deposito di codice
Autori: sviluppatori del kernel Linux
Titolo: `drivers/media/usb/gspca/kinect.c`
Sede e anno: ramo `master` di torvalds/linux; commit non annotato
Identificativo: manca
Link: https://raw.githubusercontent.com/torvalds/linux/master/drivers/media/usb/gspca/kinect.c
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-4) [T]: `Y10BPACK` (3 volte) e `depth_mode` (4 volte) presenti
Usata per: il driver del kernel dà profondità grezza a 10 bit impacchettata, non millimetri — `f10-dati/04-embedded/PREVISIONI.md` (E11) **[f7–f10: non vagliato dall'arbitro]**
Note: GPL. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### luiten-trackeval [211]
Tipo: deposito di codice
Autori: Jonathon Luiten e collaboratori
Titolo: TrackEval — HOTA (and other) evaluation metrics for Multi-Object Tracking (MOT)
Sede e anno: GitHub, letto il 14-11-2026
Identificativo: manca
Link: https://github.com/JonathonLuiten/TrackEval
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-1) [r]: pagina aperta; licenza MIT; metriche HOTA, CLEAR MOT, Identity (IDF1, IDP, IDR) e altre; la valutazione confronta l'uscita del tracciatore con dati di riferimento in `data/gt/`.
Usata per: strumento di calcolo di HOTA e IDF1, che chiede sequenze annotate — `f1/992c41c8860e/CONSEGNA.md` (§1.7)
Note: la necessità delle annotazioni è dedotta dalla struttura dei dati, non da una frase esplicita.

### luxonis-depthai [212]
Tipo: documentazione di software
Autori: Luxonis
Titolo: depthai su PyPI; USB deployment guide
Sede e anno: depthai 3.12.1 dell'11-11-2026 secondo il ruolo
Identificativo: 3.12.1
Link: https://pypi.org/pypi/depthai/json ; https://docs.luxonis.com/hardware/platform/deploy/usb-deployment-guide/
Verifica: aperta dal ruolo che la cita — (rif-4) ([g]); dal curatore [T] parziale: «03e7» e «USB3» presenti nella guida; versione non ricontrollata
Usata per: regola udev per il produttore 03e7, cavo USB 3, alimentazione — `f10-dati/04-embedded/PREVISIONI.md` (E7), `INVENTARIO_E_DECISIONE.md` ([4], [5]) **[f7–f10: non vagliato dall'arbitro]**
Note: Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### megvii-yolox [213]
Tipo: deposito di codice
Autori: Megvii (Megvii-BaseDetection)
Titolo: YOLOX (file LICENSE del deposito)
Sede e anno: GitHub, ramo main, letto il 14-11-2026
Identificativo: manca
Link: https://github.com/Megvii-BaseDetection/YOLOX ; https://raw.githubusercontent.com/Megvii-BaseDetection/YOLOX/main/LICENSE
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-1) [g]: file LICENSE aperto: «Apache License Version 2.0».
Usata per: «YOLOX è Apache 2.0 (F16, R)» — `f1/3fff79e9c3ea/FONTI.md` (F16), `f1/3fff79e9c3ea/CONSEGNA.md` (ricercatore-1, vincoli)
Note: verificata la licenza del codice; i pesi e gli insiemi di addestramento non controllati.

### microsoft-azure-kinect-sdk [214]
Tipo: deposito di codice
Autori: Microsoft
Titolo: Azure-Kinect-Sensor-SDK
Sede e anno: GitHub; archiviato il 22-8-2024, ultima versione v1.4.2
Identificativo: v1.4.2
Link: https://github.com/microsoft/Azure-Kinect-Sensor-SDK/releases
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-4) [T]: «archived» e «v1.4.2» presenti nella pagina
Usata per: deposito archiviato, pacchetti solo per Ubuntu 18.04 — `f10-dati/04-embedded/PREVISIONI.md` (E3), `INVENTARIO_E_DECISIONE.md` ([9]) **[f7–f10: non vagliato dall'arbitro]**
Note: la data dell'archiviazione e «Ubuntu 18.04» non ricontrollate. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### mrpt-octomap-opzioni [215]
Tipo: documentazione di software
Autori: MRPT (Mobile Robot Programming Toolkit)
Titolo: `mrpt::maps::COctoMapBase::TInsertionOptions`
Sede e anno: docs.mrpt.org, versione «latest» (non fissata)
Identificativo: manca
Link: https://docs.mrpt.org/reference/latest/struct_mrpt_maps_COctoMapBase_TInsertionOptions.html
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-4) [T]: 0,7, 0,4, 0,1192 e 0,971 presenti
Usata per: parametri predefiniti di OctoMap — `f7-estensione/08-creativo/CONSEGNA.md` riga 23 **[f7–f10: non vagliato dall'arbitro]**
Note: correzione C11: è la documentazione di una libreria terza; citare `octomap`. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### nasa-wellclear [216]
Tipo: documentazione di software
Autori: NASA
Titolo: DAIDALUS / Well-Clear (pagina del progetto)
Sede e anno: nasa.github.io; data: non letta
Identificativo: manca
Link: https://nasa.github.io/WellClear
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-4) [T]: «preventive», «corrective» e «warning» presenti; «DO-365» non compare
Usata per: i velivoli senza equipaggio hanno una scala propria di avvisi (preventivo, correttivo, d'allarme) — `f9-preproposta/06-esperto-dominio/CONSEGNA.md` riga 73 (F8) **[f7–f10: non vagliato dall'arbitro]**
Note: Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### nav2 [217]
Tipo: documentazione di software
Autori: Open Navigation / comunità Nav2
Titolo: Nav2 (documentazione)
Sede e anno: docs.nav2.org; versione non annotata
Identificativo: manca
Link: https://docs.nav2.org/
Verifica: aperta dal ruolo che la cita — (rif-4) (la bozza); dal curatore solo [200] (la pagina è un rinvio di 378 byte)
Usata per: mappe di costo scorrevoli e strato degli ostacoli da sensori 3D — `bozza_iniziale/Proposta MLE Matrice Bayesiana (1).md` righe 542, 1970, 2932 **[file esterno alla convocazione]**
Note: Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### navtech-witness-coasting [218]
Tipo: documentazione di software (prodotto di un costruttore)
Autori: Navtech Radar
Titolo: documentazione del tracciatore «Witness», pagina «Coasting Tracks»
Sede e anno: wiki del costruttore; data: non letta
Identificativo: pagina 255164634
Link: https://navtechradar.atlassian.net/wiki/spaces/TUN/pages/255164634
Verifica: verificata dal curatore il 14-11-2026 in parte — (rif-4) [T] solo per la presenza di «Coasting» (10 volte) nella pagina; i parametri non ricontrollati
Usata per: il coasting riporta posizioni previste finché il radar rivede il bersaglio, con età minima e massima e numero di previsioni consecutive, poi la traccia è cancellata — `f8-continuita/07-ricercatore/FONTI.md` (S18) **[f7–f10: non vagliato dall'arbitro]**
Note: prassi di un prodotto, non una norma. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### nvidia-cuvslam [219]
Tipo: documentazione di software
Autori: NVIDIA (Isaac ROS)
Titolo: cuVSLAM (Concepts, Visual SLAM)
Sede e anno: documentazione di Isaac ROS, versione «latest», letta il 14-11-2026
Identificativo: manca
Link: https://nvidia-isaac-ros.github.io/concepts/visual_slam/cuvslam/index.html
Verifica: verificata dal curatore il 14-11-2026 in parte — (rif-3) in parte: pagina aperta [g]; c'è «cuVSLAM is a GPU-accelerated library for stereo-visual-inertial SLAM and odometry». La licenza e il «pacchetto Python non commerciale» nella pagina non compaiono: non verificati. Il ruolo che la cita l'aveva vista solo in un risultato di ricerca.
Usata per: cuVSLAM: stereo più IMU, su GPU; licenza «non confermata»; pacchetto Python non commerciale — `f6-specializzazione/02-slam/MOTO_PROPRIO.md` §2(b)
Note: correzione 13. Per la licenza serve la pagina delle licenze del progetto o il deposito del pacchetto: non aperti.

### octomap [220]
Tipo: documentazione di software
Autori: Kai M. Wurm; Armin Hornung (sviluppatori, dalla pagina)
Titolo: OctoMap — An Efficient Probabilistic 3D Mapping Framework Based on Octrees (sito e sorgente)
Sede e anno: octomap.github.io; ramo `devel` del deposito, commit non annotato
Identificativo: manca
Link: https://octomap.github.io/ ; https://github.com/OctoMap/octomap/blob/devel/octomap/src/AbstractOccupancyOcTree.cpp ; https://github.com/OctoMap/octomap/blob/devel/octomap/include/octomap/OccupancyOcTreeBase.h
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-4) [T]: sul sito «Unknown areas of the environment are implicitly encoded in the map», licenza «New BSD», visualizzatore `octovis` GPL v2; nel sorgente `setProbHit(0.7)`, `setProbMiss(0.4)`, 0,1192 e 0,971
Usata per: lo sconosciuto è implicito; parametri predefiniti 0,7 / 0,4 / 0,1192 / 0,971 (3 colpi per passare da libero a occupato: conto del ruolo); regola «libero esplicito, sconosciuto implicito» — `f7-estensione/01-matematico/CONSEGNA.md` riga 78; `f7-estensione/03-nuvole-punti/CONSEGNA.md` riga 38; `f7-estensione/05-esperto-dominio/CONSEGNA.md` righe 24 e 80 (S1); `bozza_iniziale/Proposta MLE Matrice Bayesiana (1).md` righe 1696 e 2932 **[f7–f10: non vagliato dall'arbitro]**
Note: l'articolo di riferimento (Hornung, Wurm, Bennewitz, Stachniss, Burgard, Autonomous Robots 34(3):189–206, 2013, DOI 10.1007/s10514-012-9321-0) è già verificato per i soli dati bibliografici in f3; confermato oggi [API]. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### open-vins [221]
Tipo: deposito di codice
Autori: Robot Perception and Navigation Group (Università del Delaware)
Titolo: OpenVINS — An open source platform for visual-inertial navigation research
Sede e anno: GitHub; versione 2.7 annunciata nel LEGGIMI l'11 maggio 2023, pubblicata su GitHub il 20 giugno 2023
Identificativo: rpng/open_vins
Link: https://github.com/rpng/open_vins
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-3) [m, g] — licenza GPL-3.0; ultima versione v2.7. Aperta anche dal ruolo che la cita.
Usata per: componente aperto: mono o stereo più IMU, GPL-3, versione 2.7 di maggio 2023 — `f6-specializzazione/02-slam/MOTO_PROPRIO.md` §2(b)
Note: licenza con obbligo di rilascio del codice derivato: pesa su chi vuole poi un prodotto, come dice il ruolo.

### openkinect-libfreenect [222]
Tipo: deposito di codice
Autori: OpenKinect
Titolo: libfreenect (v0.6.4) e libfreenect2 (v0.2.1)
Sede e anno: GitHub; v0.6.4 del 20-9-2022 e v0.2.1 del 6-8-2021 secondo il ruolo
Identificativo: v0.6.4; v0.2.1
Link: https://github.com/OpenKinect/libfreenect ; https://github.com/OpenKinect/libfreenect2/releases/tag/v0.2.1
Verifica: aperta dal ruolo che la cita — (rif-4) ([g]); dal curatore [T] parziale: «v0.2.1» presente nella pagina della versione; date non ricontrollate
Usata per: stato dei driver liberi per Kinect v1 e v2; USB 3 obbligatorio per il v2 — `f10-dati/04-embedded/PREVISIONI.md` (E1, E2), `INVENTARIO_E_DECISIONE.md` ([7], [10]) **[f7–f10: non vagliato dall'arbitro]**
Note: licenza Apache 2.0 / GPL 2 secondo il ruolo. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### openvdb [223]
Tipo: deposito di codice
Autori: Academy Software Foundation
Titolo: OpenVDB
Sede e anno: GitHub; commit non annotato
Identificativo: manca
Link: https://github.com/AcademySoftwareFoundation/openvdb
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-4) [T] per la licenza: «Apache» e «MPL» presenti nella pagina del deposito
Usata per: albero gerarchico sparso; licenza Apache 2.0 (era MPL 2.0) — `f7-estensione/05-esperto-dominio/CONSEGNA.md` righe 27 e 80 (S5) **[f7–f10: non vagliato dall'arbitro]**
Note: Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### orb-slam3 [224]
Tipo: deposito di codice
Autori: Carlos Campos, Richard Elvira, Juan J. Gómez Rodríguez e altri (Universidad de Zaragoza; elenco completo nel LEGGIMI, non trascritto)
Titolo: ORB-SLAM3: An Accurate Open-Source Library for Visual, Visual-Inertial and Multi-Map SLAM
Sede e anno: GitHub; «V1.0, December 22th, 2021»
Identificativo: UZ-SLAMLab/ORB_SLAM3
Link: https://github.com/UZ-SLAMLab/ORB_SLAM3
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-3) [m, g] — licenza GPL-3.0; V1.0 del dicembre 2021; «monocular, stereo and RGB-D cameras». Aperta anche dal ruolo che la cita.
Usata per: componente aperto: mono, stereo, RGB-D, con o senza IMU, GPLv3, V1.0 del dicembre 2021 — `f6-specializzazione/02-slam/MOTO_PROPRIO.md` §2(b)
Note: fermo dal 2024.

### orbbec-sdk-v2 [225]
Tipo: deposito di codice
Autori: Orbbec
Titolo: OrbbecSDK_v2 (README) e pyorbbecsdk2 su PyPI
Sede e anno: GitHub e PyPI; SDK v2.10.6, pyorbbecsdk2 2.1.3 secondo il ruolo
Identificativo: v2.10.6; 2.1.3
Link: https://github.com/orbbec/OrbbecSDK_v2 ; https://pypi.org/pypi/pyorbbecsdk2/json
Verifica: aperta dal ruolo che la cita — (rif-4) ([g]); dal curatore [T] parziale: «Astra» e «not supported» presenti nel README; versioni non ricontrollate
Usata per: quali modelli Astra sono supportati dalla v2 e a quali condizioni (aggiornamento del firmware) — `f10-dati/04-embedded/PREVISIONI.md` (E6), `INVENTARIO_E_DECISIONE.md` ([3]) **[f7–f10: non vagliato dall'arbitro]**
Note: l'aggiornamento del firmware è una scrittura sul dispositivo (avviso del ruolo). Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### pipewire-conf [226]
Tipo: documentazione di software
Autori: progetto PipeWire
Titolo: pipewire.conf(5) — The PipeWire server configuration file
Sede e anno: documentazione di PipeWire, pagina letta il 14-11-2026; versione del software non indicata nel testo letto
Identificativo: pagina di manuale `pipewire.conf(5)`
Link: https://docs.pipewire.org/page_man_pipewire_conf_5.html
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-2) «default.clock.rate = 48000»; «default.clock.quantum = 1024 — Default quantum used when no client specifies one»; «default.clock.quantum-limit = 8192». Aperta anche dal ruolo che la cita.
Usata per: «campioni → scheda audio: ≥ 21,3 ms, un quanto 1024 / 48000, default di PipeWire» — `f3/H-012/02-validazione/VERIFICA.md` (§3c); entra nei «circa 155 ms» di `SOLUZIONE_V2.md` (§7), `AUDIT.md` (ipotesi 3), `VERDETTO.md`.
Note: 1024/48000 = 21,3 ms è un valore predefinito, non una misura; vale solo se il calcolatore della demo usa PipeWire con la configurazione di fabbrica. Un cliente può chiedere un quanto più piccolo. La latenza dell'uscita (cavo, Bluetooth) resta senza fonte, come scrive la verifica.

### px4-collision-prevention [227]
Tipo: documentazione di software
Autori: PX4 Autopilot (Dronecode)
Titolo: Collision Prevention
Sede e anno: PX4 Guide, ramo `main`, letta il 14-11-2026
Identificativo: manca
Link: https://docs.px4.io/main/en/computer_vision/collision_prevention
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-3) [g] — «If there is no sensor data in a particular direction, velocity in that direction is restricted to 0»; «for longer than 0.5s … force the velocity setpoints in xy to zero. After 5 seconds of not receiving any data, the vehicle will switch into HOLD mode»; «the region covered by this sensor will be treated as uncovered, meaning you will not be able to move there»; «a vehicle moving at 4 m/s with OBSTACLE_DISTANCE messages being emitted at 10Hz»; «tracking delay is typically between 0.1 and 0.5 seconds»; un sensore con campo orizzontale «of about 35 degrees». Aperta anche dal ruolo che la cita.
Usata per: telemetri a fascio come ingressi tipici; settori stretti (esempio: 35°) — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §2(b), S18
Usata per: prevenzione delle collisioni provata a 4 m/s, messaggi a 10 Hz, ritardi di 0,1–0,5 s — stesso file, §2(c)
Usata per: senza dati in una direzione la velocità è 0; oltre 0,5 s senza dati azzera i comandi orizzontali, dopo 5 s attesa; la regione di un sensore guasto è «treated as uncovered»: «sconosciuto non è libero» — stesso file, §2(e)
Usata per: gli 0,5 s della causa «collegamento», presi per analogia (per un collegamento: non verificato) — `f6-specializzazione/01-esperto-dominio/SPECIALIZZAZIONE.md` §3.2
Usata per: secondo aggancio per il giurato: gli autopiloti aperti azzerano la velocità verso i settori senza dati — `f6-specializzazione/01-esperto-dominio/SPECIALIZZAZIONE.md` §6; ripreso in `f6-specializzazione/03-avversario/ATTACCO_SPECIALIZZAZIONE.md` S5 («S18 con la frase citata»)
Note: lo «0,1–0,5 s» è il ritardo d'inseguimento della velocità del veicolo, non un ritardo di collegamento. La stessa pagina avverte che con il parametro `CP_GO_NO_DATA=1` il veicolo può muoversi anche dove non ha dati: il comportamento prudente è quello predefinito, non una garanzia. I «4 m/s» sono una prova iniziale del costruttore, non un limite.

### px4-ekf2 [228]
Tipo: documentazione di software
Autori: PX4 Autopilot (Dronecode)
Titolo: Using PX4's Navigation Filter (EKF2)
Sede e anno: PX4 Guide, ramo `main`, letta il 14-11-2026
Identificativo: manca
Link: https://docs.px4.io/main/en/advanced_config/tuning_the_ecl_ekf
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-3) [g] — «delta angle and delta velocity data at a minimum rate of 100Hz»; «The EKF uses the IMU data for state prediction only»; magnetometro ad almeno 5 Hz; quota da «GPS, barometric pressure, range finder, external vision»; «A complementary filter is used to propagate the states forward from the 'fusion time horizon' to current time». Aperta anche dai due ruoli che la citano.
Usata per: lo stimatore di stato fonde IMU (in predizione, almeno 100 Hz), magnetometro, GNSS, barometro, telemetro e visione esterna — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §2(a), S12
Usata per: lo stimatore lavora su un orizzonte ritardato e porta gli stati al presente con l'IMU — `f6-specializzazione/02-slam/MOTO_PROPRIO.md` §2(c)
Note: descrive l'architettura, non dà nessuna accuratezza. Ramo `main`, non una versione fissata.

### px4-obstacle-distance [229]
Tipo: documentazione di software
Autori: PX4 Autopilot (Dronecode)
Titolo: ObstacleDistance (UORB message)
Sede e anno: PX4 Guide, ramo `main`, letta il 14-11-2026
Identificativo: manca
Link: https://docs.px4.io/main/en/msg_docs/ObstacleDistance
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-3) [g] — «A value of 0 means that the obstacle is right in front of the sensor. A value of max_distance +1 means no obstacle is present. A value of UINT16_MAX for unknown/not used. In a array element, one unit corresponds to 1cm.» Il ruolo che la cita l'aveva vista solo in un risultato di ricerca.
Usata per: l'interfaccia per settori: `UINT16_MAX` sconosciuto, `max_distance + 1` nessun ostacolo — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §2(e), S23
Usata per: il messaggio per settori a tre valori verso l'autopilota — `f6-specializzazione/01-esperto-dominio/SPECIALIZZAZIONE.md` §3.1
Usata per: «S23 solo da risultato di ricerca» nel giudizio sul secondo aggancio — `f6-specializzazione/03-avversario/ATTACCO_SPECIALIZZAZIONE.md` S5
Note: con la verifica di oggi cade la riserva dell'avversario su S23 («non riverificabile in rete»): i tre valori ci sono, alla lettera. Resta vero che il prototipo non ha mai generato questo messaggio. La pagina descrive il messaggio interno di PX4; il messaggio MAVLink con lo stesso nome non è stato aperto.

### px4-safety [230]
Tipo: documentazione di software
Autori: PX4 Autopilot (Dronecode)
Titolo: Safety Configuration (Failsafes)
Sede e anno: PX4 Guide, ramo `main`, letta il 14-11-2026
Identificativo: manca
Link: https://docs.px4.io/main/en/config/safety
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-3) [g] — «The Data Link Loss failsafe is triggered if the connection to the last MAVLink ground station … is lost»; tempo `COM_DL_LOSS_T`; azione `NAV_DLL_ACT`: «Disabled, Hold mode, Return mode, Land mode, Disarm, Terminate». Il ruolo che la cita l'aveva vista solo in un risultato di ricerca.
Usata per: la perdita del collegamento ha un'azione configurata — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §2(e), S25
Usata per: alla perdita del collegamento, a bordo decide l'azione già configurata nell'autopilota — `f6-specializzazione/01-esperto-dominio/SPECIALIZZAZIONE.md` §3.2
Note: la pagina non dà un valore predefinito in secondi nel passo letto: gli 0,5 s del progetto non vengono da qui.

### px4-vehicle-odometry [231]
Tipo: documentazione di software
Autori: PX4 Autopilot (Dronecode)
Titolo: VehicleOdometry (UORB message)
Sede e anno: PX4 Guide, ramo `main`, letta il 14-11-2026
Identificativo: manca
Link: https://docs.px4.io/main/en/msg_docs/VehicleOdometry
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-3) [g] — campi `timestamp_sample`, `position_variance`, `orientation_variance`, `velocity_variance`, `reset_counter` («Counts reset events on attitude, velocity and position»). Aperta anche dal ruolo che la cita.
Usata per: il messaggio d'odometria porta marca temporale, varianze e contatore dei salti; la pagina non dà alcuna accuratezza — `f6-specializzazione/02-slam/MOTO_PROPRIO.md` §2(c)
Note: confermo che la pagina non contiene cifre d'accuratezza: l'errore di 0,1 m/s usato nel conto resta un'ipotesi del ruolo.

### pyrealsense2-pypi [232]
Tipo: documentazione di software (registro dei pacchetti)
Autori: RealSense
Titolo: pyrealsense2 su PyPI
Sede e anno: PyPI; versione 2.59.1.11053
Identificativo: 2.59.1.11053
Link: https://pypi.org/pypi/pyrealsense2/json
Verifica: aperta dal ruolo che la cita — (rif-4) ([g]); dal curatore solo [200]
Usata per: ruote cp39–cp314 per Linux x86_64 e aarch64 e Windows; la 2.54.2.5684 solo cp37–cp311 — `f10-dati/04-embedded/PREVISIONI.md` (E5), `INVENTARIO_E_DECISIONE.md` ([1]); `f10-dati/02-sensori/MODELLO_SENSORE.md` riga 63 **[f7–f10: non vagliato dall'arbitro]**
Note: Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### realsense-filtri-post [233]
Tipo: documentazione di software
Autori: RealSense (già Intel RealSense)
Titolo: Post-processing filters
Sede e anno: RealSense, documentazione per sviluppatori (SDK librealsense), pagina letta il 14-11-2026; versione dell'SDK non indicata nel testo letto
Identificativo: manca
Link: https://dev.realsenseai.com/docs/post-processing-filters/
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-2) Nell'audit era letta solo nel riassunto della ricerca. Filtro temporale: «In cases where the pixel data is missing or invalid the filter uses a user-defined persistency mode to decide whether the missing value should be rectified with stored data»; «Persistency index… when missing pixels will be replace with the last valid value»; predefinito «3 (Valid in 2/last 4)». Riempimento dei buchi: «obtains the four immediate pixel "neighbors"… and selects one of them»; predefinito «1 (Farthest from around)». Anche il filtro spaziale ha un riempimento dei buchi.
Usata per: ipotesi 1, «i filtri dell'SDK cambiano un pixel senza dato in un dato» (persistenza predefinita «valido in 2 degli ultimi 4»; il riempimento copia un vicino) — `f5/02-audit/AUDIT.md` (ipotesi 1); condizione ripresa in `f4/H-012/09-arbitro/VERDETTO.md`; «filtri dell'SDK che riempiono i buchi» — `f3/H-012/02-validazione/VERIFICA.md` (§2, invariante 2).
Note: la pagina dà i valori predefiniti dei filtri quando sono usati; non dice quali filtri siano accesi in un dato programma (il flusso grezzo dell'SDK non li applica da solo; il visualizzatore del costruttore ne accende alcuni: non verificato oggi). La documentazione non è legata a una versione: va controllata su quella installata. Per la Gemini 335 (altro SDK): non verificato, come dice l'audit.

### rlabbe-filterpy [234]
Tipo: deposito di codice
Autori: Roger R. Labbe Jr
Titolo: FilterPy (file LICENSE del deposito)
Sede e anno: GitHub, ramo master, letto il 14-11-2026
Identificativo: manca
Link: https://raw.githubusercontent.com/rlabbe/filterpy/master/LICENSE
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-1) [g]: «The MIT License (MIT) Copyright (c) 2015 Roger R. Labbe Jr».
Usata per: «licenza MIT (anche filterpy)» in F16 — `f1/3fff79e9c3ea/FONTI.md`
Note: nessuna

### roboflow-rf-detr [235]
Tipo: deposito di codice
Autori: Roboflow
Titolo: RF-DETR (README del deposito)
Sede e anno: deposito `roboflow/rf-detr`, ramo `develop`, letto il 14-11-2026 (il ramo `main` dà 404)
Identificativo: manca
Link: https://github.com/roboflow/rf-detr
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-1) già verificata dal curatore in f3 [g], con correzione: Apache 2.0 per il codice e per i modelli N, S, M, L, per la segmentazione e per i punti chiave; i modelli di rilevamento Atto, Femto, Pico, XL e 2XL sono sotto PML 1.0. RF-DETR-N: 2,3 ms su T4 (TensorRT, FP16, lotto 1), AP 48,4. Non riaperta oggi. ‖ (rif-2) Tabella: RF-DETR-N, COCO AP50:95 48,4, latenza 2,3 ms, 30,5 milioni di parametri, 384×384, Apache 2.0. Testo: Nano, Small, Medium, Large, tutta la segmentazione e i punti chiave sotto Apache 2.0; Atto, Femto, Pico, XL, 2XL sotto PML 1.0; «YOLOv8, YOLO11 and YOLO26 are released under AGPL-3.0». Già in f3/fonti.
Usata per: «RF-DETR-N 2,3 ms su T4, Apache 2.0»; alternativa ad AGPL — `f1/c85dbcc51ea6/CONSEGNA.md` (§1.2, visione-1, rif. [3])
Usata per: «RF-DETR-N: 2,3 ms su T4, AP 48,4, Apache 2.0 (le varianti Atto, Femto, Pico, XL, 2XL sono sotto PML 1.0)» — `f3/H-012/01-scene-dinamiche/SOLUZIONE.md` (B6, §8); `f4/H-012/05-correzioni/SOLUZIONE_V2.md` (B6, §8); `f2/05-selezione/SELEZIONE.md` (H-006); alternativa all'AGPL — `f2/01-traduzione/SCHEDE.md` (`visione-1`).
Note: (rif-1) la licenza dipende dalla taglia del modello. Latenza su CPU: non verificata. (rif-2) che i 2,3 ms siano su T4 con TensorRT a mezza precisione lo dice f3; oggi ho letto la tabella, non le condizioni di misura. Nessun tempo su CPU nel README letto: il costo del ramo asincrono su un portatile resta da misurare.

### rosbags [236]
Tipo: documentazione di software (pacchetto)
Autori: Ternaris
Titolo: rosbags 0.11.9
Sede e anno: PyPI; progetto su GitLab (ternaris/rosbags)
Identificativo: 0.11.9; sha256 `2d0df7de565dc13abd444a3c2681911fc6ef88095da3faced5c99719e5dc0fa4` (dal ruolo)
Link: https://files.pythonhosted.org/packages/eb/f8/84529aea85bec7395bb5aa7f4401ea2d7e6135cb367e36493851b859917b/rosbags-0.11.9.tar.gz
Verifica: aperta dal ruolo che la cita — (rif-4) (impronta confrontata con quella di PyPI); non ricontrollata da me
Usata per: lettura dei file `.bag` in Python puro; prova dell'infrastruttura di scaricamento — `f10-dati/03-infrastruttura/PREVISIONI.md` (infra-P1, P8), `AMBIENTE.md` righe 33 e 83; `f10-dati/01-ricercatore/DATI_PUBBLICI.md` §4 **[f7–f10: non vagliato dall'arbitro]**
Note: licenza Apache-2.0 dai metadati di PyPI. Le altre librerie dell'ambiente (numpy 2.5.4, scipy 1.18.1, opencv, pillow) sono strumenti, non fonti: stanno in `AMBIENTE.md`. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### rtabmap [237]
Tipo: deposito di codice
Autori: Mathieu Labbé, IntRoLab, Université de Sherbrooke
Titolo: RTAB-Map library and standalone application
Sede e anno: GitHub, ultimo aggiornamento novembre 2026
Identificativo: introlab/rtabmap
Link: https://github.com/introlab/rtabmap
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-3) [m, g] — GitHub non riconosce la licenza in automatico («NOASSERTION»), ma il file LICENSE ha il testo di una licenza di tipo BSD («Redistribution and use in source and binary forms, with or without modification, are permitted provided that…»), con diritti di Mathieu Labbé, 2010–2025. Aperta anche dal ruolo che la cita.
Usata per: componente aperto: RGB-D, stereo, LiDAR (sensori non verificati dal ruolo); licenza BSD «dal distintivo» — `f6-specializzazione/02-slam/MOTO_PROPRIO.md` §2(b)
Note: la licenza ora è confermata dal file, non solo dal distintivo. I sensori supportati restano non verificati: nel LEGGIMI non ho trovato le parole cercate. Le dipendenze possono avere licenze diverse: non controllato.

### simulatori-di-profondita [238]
Tipo: deposito di codice (voce di gruppo: otto strumenti esaminati)
Autori: vari
Titolo: Open3D (`RaycastingScene`); Habitat-Sim (modello Redwood); simkinect; SimSense e SAPIEN; BlenderProc; Gazebo `gz-sensors`; Isaac Sim
Sede e anno: GitHub, rami principali; commit non annotati
Identificativo: manca
Link: https://raw.githubusercontent.com/isl-org/Open3D/main/ ; https://raw.githubusercontent.com/facebookresearch/habitat-sim/main/ ; https://raw.githubusercontent.com/ankurhanda/simkinect/master/README.md ; https://raw.githubusercontent.com/angli66/simsense/main/ ; https://raw.githubusercontent.com/haosulab/SAPIEN/master/ ; https://raw.githubusercontent.com/DLR-RM/BlenderProc/main/ ; https://raw.githubusercontent.com/gazebosim/gz-sensors/main/
Verifica: aperta dal ruolo che la cita — (rif-4) (copie in `f10-dati/02-sensori/scaricati/`, con `PROVENIENZA.md`); non ricontrollata da me; Isaac Sim: vista solo nel riassunto di un motore di ricerca
Usata per: nessuno strumento su sola CPU riproduce buchi e occlusione di una D4xx con un profilo pronto (regge su 8 strumenti: non è una prova universale); licenze MIT, Apache-2.0, GPL-3.0, assente per simkinect — `f10-dati/02-sensori/MODELLO_SENSORE.md` righe 60–70, `PREVISIONI.md` righe 15 e 30 **[f7–f10: non vagliato dall'arbitro]**
Note: zero strumenti trovati su un campione non prova che non esistano. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### stm32duino-vl53l7cx [239]
Tipo: deposito di codice
Autori: stm32duino
Titolo: VL53L7CX (libreria Arduino) e VL53L8CX
Sede e anno: GitHub; il ruolo cita il driver 1.2.3
Identificativo: manca (commit non annotato)
Link: https://github.com/stm32duino/VL53L7CX ; https://github.com/stm32duino/VL53L8CX
Verifica: aperta dal ruolo che la cita — (rif-4) ([g]); dal curatore solo [200]
Usata per: nessuna funzione di trigger nel driver 1.2.3; firmware da caricare di 86 016 byte per sensore a ogni avvio; SYNC sull'L8CX — `f9-preproposta/07-lidar/CONSEGNA.md` critica 2 e §5 ([6]) **[f7–f10: non vagliato dall'arbitro]**
Note: versione e licenza non ricontrollate. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### strayrobots-scanner-formato [240]
Tipo: documentazione di software
Autori: Stray Robots
Titolo: Stray Scanner — `docs/format.md`
Sede e anno: GitHub, ramo `main`
Identificativo: manca
Link: https://github.com/strayrobots/scanner/blob/main/docs/format.md
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-4) [T]: 256, 192 e «millimeters» presenti
Usata per: profondità PNG a 16 bit in millimetri, 256 × 192 — `f10-dati/04-embedded/PREVISIONI.md` (E8), `INVENTARIO_E_DECISIONE.md` ([13]) **[f7–f10: non vagliato dall'arbitro]**
Note: il convertitore del ruolo è provato solo su una cartella finta. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### ufomap-deposito [241]
Tipo: deposito di codice
Autori: Daniel Duberg e altri (organizzazione UnknownFreeOccupied)
Titolo: UFOMap
Sede e anno: GitHub, ramo `master`; commit non annotato
Identificativo: manca
Link: https://github.com/UnknownFreeOccupied/ufomap
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-4) [T]: nel README «Colored UFOMap constructed in real-time (2 Hz) at 2 mm voxel size»; la licenza BSD-2 non è nel README: non ricontrollata
Usata per: «real-time (2 Hz) at 2 mm»; licenza BSD-2 — `f7-estensione/05-esperto-dominio/CONSEGNA.md` righe 26 e 80 (S3) **[f7–f10: non vagliato dall'arbitro]**
Note: correzione C2. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### ultralytics-coco-yaml [242]
Tipo: documentazione di software (file di configurazione di un insieme di dati)
Autori: Ultralytics
Titolo: coco.yaml — COCO 2017 dataset (file di configurazione)
Sede e anno: deposito `ultralytics/ultralytics`, ramo `main`, letto il 14-11-2026
Identificativo: `ultralytics/cfg/datasets/coco.yaml`
Link: https://raw.githubusercontent.com/ultralytics/ultralytics/main/ultralytics/cfg/datasets/coco.yaml
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-1) [g]: file aperto; 80 nomi di classe; nessuno corrisponde a muro, porta, gradino, palo, scatola, carrello, cono (controllo mio sull'elenco: 0 su 7). ‖ (rif-2) 80 classi numerate (contate con `grep`). Ci sono: bicycle, car, fire hydrant, bench, chair, potted plant, dining table. Non ci sono: wall, door, stair, pole. Intestazione AGPL-3.0. Aperta anche dal ruolo che la cita.
Usata per: «muro, porta, gradino, palo, scatola, carrello, cono non sono fra le 80 classi COCO» (P1 di visione: 0 su 7) — `f1/c85dbcc51ea6/CONSEGNA.md` (§1.4, rif. [10])
Usata per: «0 su 7 categorie d'ostacolo fra le 80 classi COCO»; COCO contiene sedia, panca, tavolo, bicicletta, auto, idrante, pianta in vaso; non muro, porta, gradino, palo — `f2/04-torneo/TORNEO.md` (parte 1, H-006 e «Fonti»); `f2/01-traduzione/SCHEDE.md` (`visione-1`); `f2/05-selezione/SELEZIONE.md` (H-006); `f3/H-012/01-scene-dinamiche/SOLUZIONE.md` (B6, §7).
Note: (rif-1) controllo esaustivo sulle 80 classi e sulle 7 categorie dichiarate; non dice niente su altri insiemi (LVIS, Objects365). (rif-2) la lista delle sette categorie è scelta dall'autore dell'idea (lo scrive il torneo). Il file è del ramo principale: può cambiare; per la provenienza va fissato a un commit. Differenza fra i gruppi: per rif-1 il tipo era «insieme di dati»; qui è un file di configurazione in un deposito. L'articolo che descrive COCO è `lin2014`.

### ultralytics-tracciatori [243]
Tipo: documentazione di software
Autori: Ultralytics
Titolo: Multi-Object Tracking with Ultralytics YOLO (modo «track») e `cfg/default.yaml`
Sede e anno: Ultralytics, documentazione e deposito, letti il 14-11-2026
Identificativo: `ultralytics/cfg/default.yaml`
Link: https://docs.ultralytics.com/modes/track/ ; anche (rif-1): https://raw.githubusercontent.com/ultralytics/ultralytics/main/ultralytics/cfg/trackers/bytetrack.yaml
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-1) già verificata dal curatore in f3 [g]: sei tracciatori (BoT-SORT, ByteTrack, OC-SORT, Deep OC-SORT, FastTracker, TrackTrack); `track_buffer: 30` in `bytetrack.yaml`; predefinito `tracker: tracktrack.yaml`; intestazione AGPL-3.0; re-identificazione spenta in partenza [r]. Non riaperta oggi. ‖ (rif-2) Pagina: «OC-SORT, Deep OC-SORT, FastTracker, TrackTrack are available alongside BoT-SORT and ByteTrack»; «Default tracker (TrackTrack)». `default.yaml`, riga 139: `tracker: tracktrack.yaml`. Già in f3/fonti.
Usata per: `track_buffer: 30` come origine della scadenza di 1 s; sei tracciatori, predefinito TrackTrack, re-identificazione spenta; AGPL-3.0 — `f1/992c41c8860e/CONSEGNA.md` (§1.2, §1.3)
Usata per: tracciatore BoT-SORT o ByteTrack, ReID di BoT-SORT — `f1/c85dbcc51ea6/CONSEGNA.md` (visione-1, visione-2, rif. [15])
Usata per: «rilevatore "nano" con maschere + tracciatore (BoT-SORT o ByteTrack)» nel percorso asincrono — `f2/01-traduzione/SCHEDE.md` (`visione-1`); `f2/03-triage/TRIAGE.md` (H-006).
Note: (rif-1) `track_buffer: 30` è il predefinito di ByteTrack, non del tracciatore che parte senza scelta (`tracktrack.yaml` non letto). Che i tracciatori non espongano covarianza né tracce «previste»: non verificato (lo dichiara il ruolo). (rif-2) i file del gruppo non citano questa pagina: la voce documenta da dove vengono i due tracciatori nominati. Il tracciatore predefinito è TrackTrack, non ByteTrack (correzione già di f3). Codice sotto AGPL-3.0.

### ultralytics-yolo26 [244]
Tipo: documentazione di software
Autori: Ultralytics
Titolo: Ultralytics YOLO26 (pagina del modello) e file LICENSE del deposito
Sede e anno: Ultralytics, documentazione e deposito `ultralytics/ultralytics`, letti il 14-11-2026
Identificativo: manca
Link: https://docs.ultralytics.com/models/yolo26/ ; https://github.com/ultralytics/ultralytics
Verifica: dato diverso — (rif-1) già verificata dal curatore in f3 [g]: YOLO26n a 640 px 38,9 ± 0,7 ms su CPU in ONNX, 1,7 ms su T4, mAP 40,9; AGPL-3.0. Dato diverso: YOLOE-26 40,6 AP su LVIS è della variante x [r]. Non riaperta oggi. ‖ (rif-2) Riga YOLO26n, 640: mAP 40,9 (40,1 senza soppressione dei non massimi), CPU ONNX 38,9 ± 0,7 ms, T4 TensorRT 1,7 ± 0,0 ms, 2,4 milioni di parametri. File LICENSE: «GNU AFFERO GENERAL PUBLIC LICENSE Version 3». Già in f3/fonti.
Usata per: «YOLO26n 38,9 ms a 640 px in ONNX (1,7 ms su T4), AGPL-3.0»; «YOLOE-26 40,6 AP su LVIS con testo»; «circa 25 Hz il solo rilevatore» — `f1/c85dbcc51ea6/CONSEGNA.md` (§1.2, visione-1, rif. [2])
Usata per: «YOLO26n 38,9 ms su CPU, AGPL-3.0» come alternativa nel ramo asincrono — `f2/05-selezione/SELEZIONE.md` (H-006); `f3/H-012/01-scene-dinamiche/SOLUZIONE.md` (B6, §8: «38,9 ± 0,7 ms»); `f4/H-012/05-correzioni/SOLUZIONE_V2.md` (B6, §8). Rischio «AGPL-3.0 (alternativa RF-DETR)» — `f2/01-traduzione/SCHEDE.md` (`visione-1`).
Note: (rif-1) la latenza su CPU è quella della macchina di prova di Ultralytics, non del portatile della squadra (P5 non risolta). AGPL-3.0: obblighi da portare all'analista normativo. (rif-2) i 38,9 ms sono su una CPU da server (la pagina nomina un Intel Xeon a 2,00 GHz), in ONNX: non sono il tempo su un portatile. Il README di RF-DETR dà per YOLO26-N un AP di 40,3: differenza di protocollo, non controllata. L'AGPL-3.0 impone obblighi sul codice distribuito o offerto in rete: per un prototipo da hackathon conta se il codice viene pubblicato.

### vins-fusion [245]
Tipo: deposito di codice
Autori: HKUST Aerial Robotics Group
Titolo: VINS-Fusion — An optimization-based multi-sensor state estimator
Sede e anno: GitHub, ultimo aggiornamento maggio 2024
Identificativo: HKUST-Aerial-Robotics/VINS-Fusion
Link: https://github.com/HKUST-Aerial-Robotics/VINS-Fusion
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-3) [m, g] — licenza GPL-3.0; «online temporal calibration (time offset between camera and IMU)». Aperta anche dal ruolo che la cita.
Usata per: componente aperto: mono o stereo più IMU, GPLv3, taratura in linea dello scarto temporale fra camera e IMU — `f6-specializzazione/02-slam/MOTO_PROPRIO.md` §2(b)
Note: fermo dal 2024.


---

## 5. Insiemi di dati

14 voci, da [246] a [259].

### bonn-rgbd-dynamic [246]
Tipo: insieme di dati
Autori: Emanuele Palazzolo; Jens Behley; Philipp Lottes; Philippe Giguère; Cyrill Stachniss
Titolo: Bonn RGB-D Dynamic Dataset; articolo associato: «ReFusion: 3D Reconstruction in Dynamic Environments for RGB-D Cameras Exploiting Residuals»
Sede e anno: IEEE/RSJ IROS 2019, pp. 7855–7862
Identificativo: DOI 10.1109/IROS40897.2019.8967590
Link: https://www.ipb.uni-bonn.de/data/rgbd-dynamic-dataset/
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-4) [T] e [API]: pagina aperta, `moving_obstructing_box` presente, articolo indicato nella pagina; nessuna licenza nel testo della pagina (coerente con «non dichiarata»)
Usata per: ripiego se il primo insieme non risponde (320 845 314 byte) — `f10-dati/01-ricercatore/DATI_PUBBLICI.md` §1, §5 **[f7–f10: non vagliato dall'arbitro]**
Note: camera in moto; senza licenza dichiarata l'uso va chiesto. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### depthtrack [247]
Tipo: insieme di dati
Autori: Song Yan; Jinyu Yang; Jani Käpylä; Feng Zheng; Aleš Leonardis; Joni-Kristian Kämäräinen
Titolo: DepthTrack Test Set (ICCV2021); articolo associato: «DepthTrack: Unveiling the Power of RGBD Tracking»
Sede e anno: IEEE/CVF ICCV 2021, pp. 10705–10713; Zenodo, 19-12-2021
Identificativo: DOI 10.5281/zenodo.5792146; DOI 10.1109/ICCV48922.2021.01055
Link: https://zenodo.org/records/5792146
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-4) [API Zenodo e Crossref]: 50 sequenze RGB-D, licenza CC BY 4.0
Usata per: ripiego: `human02_indoor.zip` (578 368 987 byte, 1740 fotogrammi) — `f10-dati/01-ricercatore/DATI_PUBBLICI.md` §1, §5 **[f7–f10: non vagliato dall'arbitro]**
Note: il sensore (una RealSense D415 «a memoria») non è stato trovato nelle pagine lette: non verificato. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### drow [248]
Tipo: insieme di dati
Autori: Lucas Beyer; Alexander Hermans; Bastian Leibe (2016); con Timm Linder e Kai O. Arras (2018)
Titolo: DROW; articoli associati: «DROW: Real-Time Deep Learning based Wheelchair Detection in 2D Range Data» e «Deep Person Detection in Two-Dimensional Range Data»
Sede e anno: arXiv 2016 (sede a stampa: non verificata); IEEE Robotics and Automation Letters 3(3):2726–2733, 2018
Identificativo: arXiv:1603.02636; DOI 10.1109/LRA.2018.2835510
Link: https://github.com/VisualComputingInstitute/DROW ; https://github.com/VisualComputingInstitute/DROW/releases/download/v2/DROWv2-data.zip
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-4) [API] e [T]: nella pagina del deposito «MIT», «S300», «450» presenti; il 5 % delle scansioni annotate non ricontrollato
Usata per: LiDAR 2D SICK S300 a 37 cm, 225° in 450 punti, persone annotate sul 5 % delle scansioni; 197 970 996 byte — `f10-dati/01-ricercatore/DATI_PUBBLICI.md` §3; copia del README in `f10-dati/01-ricercatore/pagine/drow_readme.md` **[f7–f10: non vagliato dall'arbitro]**
Note: il ruolo scrive il link come `RWTHVision/DROW` (rinvia a `VisualComputingInstitute`). Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### friburgo-rgbd-people [249]
Tipo: insieme di dati
Autori: Luciano Spinello; Matthias Luber; Kai O. Arras
Titolo: RGB-D People Dataset; articoli associati: «People Detection in RGB-D Data» (IROS 2011, pp. 3838–3843) e «People Tracking in RGB-D Data With On-line Boosted Target Models» (IROS 2011, pp. 3844–3849)
Sede e anno: Università di Friburgo, 2011
Identificativo: DOI 10.1109/IROS.2011.6095074; DOI 10.1109/IROS.2011.6095075
Link: http://www2.informatik.uni-freiburg.de/~spinello/RGBD-dataset.html ; http://www2.informatik.uni-freiburg.de/~spinello/sw/rgbd_people_unihall.tar.gz
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-4) [T] e [API]: nella pagina «3000+ RGB-D frames», tre Kinect montati in verticale, licenza «Creative Commons Attribution-Noncommercial-Share Alike 3.0 Unported», «visibility»; articoli confermati su Crossref
Usata per: archivio di 2 805 714 553 byte; visibilità annotata (0, 1, 2); scelta n. 3 per le ipotesi 4, 5 e 3 — `f10-dati/01-ricercatore/DATI_PUBBLICI.md` §1, §5 **[f7–f10: non vagliato dall'arbitro]**
Note: uso non commerciale; profondità grezza a 11 bit, non metrica. Il link di scaricamento scritto nella pagina (`www.informatik…`) è rotto secondo il ruolo. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### frog [250]
Tipo: insieme di dati
Autori: Fernando Amodeo; Noé Pérez-Higueras; Luis Merino; Fernando Caballero
Titolo: FROG: a new people detection dataset for knee-high 2D range finders
Sede e anno: Frontiers in Robotics and AI, vol. 12, 2025
Identificativo: DOI 10.3389/frobt.2025.1671673
Link: https://robotics.upo.es/datasets/frog/laser2d_people/
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-4) [T] e [API]: pagina aperta, articolo indicato; nessuna licenza nel testo (coerente con «non dichiarata»); il nome del file `.h5` non ricontrollato
Usata per: scansioni da 720 punti con persone annotate su tutte, robot in moto; 148 746 736 byte — `f10-dati/01-ricercatore/DATI_PUBBLICI.md` §3 **[f7–f10: non vagliato dall'arbitro]**
Note: Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### insiemi-non-raggiungibili [251]
Tipo: insieme di dati (voce di gruppo)
Autori: vari
Titolo: Kinect Tracking Precision (KTP); pedoni RGB-D dell'EPFL; JRDB; CDTB
Sede e anno: manca
Identificativo: manca
Link: manca (il ruolo non riporta gli indirizzi)
Verifica: non raggiungibile — (rif-4) (KTP ed EPFL: 404 secondo il ruolo; JRDB chiede un conto; CDTB non approfondito); non ricontrollata da me
Usata per: esclusi dalla scelta — `f10-dati/01-ricercatore/DATI_PUBBLICI.md` §1 **[f7–f10: non vagliato dall'arbitro]**
Note: nessun dato ne dipende. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### oxford-ihm [252]
Tipo: insieme di dati
Autori: Mark Nicholas Finean; Luka Petrović; Wolfgang Merkt; Ivan Marković; Ioannis Havoutis
Titolo: Oxford Indoor Human Motion Dataset; articolo associato: «Motion planning in dynamic environments using context-aware human trajectory prediction»
Sede e anno: Robotics and Autonomous Systems 166:104450, 2023
Identificativo: DOI 10.1016/j.robot.2023.104450
Link: https://articulated.robots.ox.ac.uk/oxford-indoor-human-motion-dataset/
Verifica: verificata dal curatore il 14-11-2026 in parte — (rif-4) [T] e [API]: «~60 minutes of rosbag data», cattura del moto a 100 Hz, camere RGB-D ferme e sul robot; «D435», «CC BY-NC-SA» e l'accesso su richiesta NON sono nel testo della pagina che ho scaricato: non verificati
Usata per: ideale ma non ottenibile in 14 ore; da chiedere per il dopo-hackathon — `f10-dati/01-ricercatore/DATI_PUBBLICI.md` §1, §6 **[f7–f10: non vagliato dall'arbitro]**
Note: licenza e modello della camera da rileggere nella pagina di scaricamento. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### park2026 [253]
Tipo: insieme di dati (con articolo di workshop)
Autori: Yeeun Park; Miqdad Naduthodi; Suryansh Kumar
Titolo: HUM4D — «A Dataset and Evaluation for Complex 4D Markerless Human Motion Capture»
Sede e anno: IEEE/CVF CVPR 2026, 4D World Models Workshop
Identificativo: arXiv:2604.12765
Link: https://parkyeeun23.github.io/HUM4D/ ; https://github.com/ParkYeeun23/hum4d-processing ; https://arxiv.org/abs/2604.12765
Verifica: dato diverso — (rif-4) è un articolo di workshop, non della conferenza principale (correzione C1) [T]; confermati [T]: 44 sequenze, 6 camere RGB-D sincronizzate, RealSense D455, altezza 1,45 m, raggio 3 m, Vicon, CC BY 4.0, 83 768 fotogrammi ‖ All'unione (16:33): registro arXiv aperto: 2604.12765v1 del 14-04-2026, autori Yeeun Park, Miqdad Naduthodi, Suryansh Kumar, commento «Accepted for publication at CVPR 2026 4D World Models Workshop».
Usata per: «il più vicino al sensore della squadra»; proposta ricercatore-1 (scaricare una cartella dal browser) — `f10-dati/01-ricercatore/DATI_PUBBLICI.md` §1, §6 **[f7–f10: non vagliato dall'arbitro]**
Note: nessun archivio scaricabile con `curl` (cartelle di Google Drive). Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### princeton-tracking-benchmark [254]
Tipo: insieme di dati
Autori: Shuran Song; Jianxiong Xiao
Titolo: Princeton Tracking Benchmark; articolo associato: «Tracking Revisited Using RGBD Camera: Unified Benchmark and Baselines»
Sede e anno: IEEE ICCV 2013, pp. 233–240
Identificativo: DOI 10.1109/ICCV.2013.36
Link: https://tracking.cs.princeton.edu/dataset.html
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-4) [T] e [API]: nella pagina profondità PNG a 16 bit «with the first 3 bit swap to the last», `frames.json` con K; licenza non dichiarata
Usata per: ripiego: `ValidationSet.zip` (631 649 593 byte, 5 sequenze) — `f10-dati/01-ricercatore/DATI_PUBBLICI.md` §1, §5 **[f7–f10: non vagliato dall'arbitro]**
Note: scene ravvicinate, un bersaglio. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### realsense-file-di-esempio [255]
Tipo: insieme di dati (file di esempio del costruttore)
Autori: RealSense
Titolo: Sample Data (`doc/sample-data.md`): `D435i_Depth_and_IMU_Stands_still.bag`, `stairs.bag`, `structured.bag`, `outdoors.bag`
Sede e anno: librealsense; date: non lette
Identificativo: manca
Link: https://github.com/realsenseai/librealsense/blob/master/doc/sample-data.md ; https://librealsense.realsenseai.com/rs-tests/
Verifica: aperta dal ruolo che la cita — (rif-4) (dimensioni e indici letti dai file); dal curatore solo [200] sulla pagina
Usata per: registrazioni grezze di stereo attivo (107–423 MB, 4–8 s) per le ipotesi 1, 2 e 6, senza verità di riferimento — `f10-dati/01-ricercatore/DATI_PUBBLICI.md` §2, §5; `f10-dati/02-sensori/MODELLO_SENSORE.md` riga 63 **[f7–f10: non vagliato dall'arbitro]**
Note: licenza dei file non dichiarata; se contengano persone non è verificato. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### thor [256]
Tipo: insieme di dati
Autori: Andrey Rudenko; Tomasz P. Kucner; Chittaranjan S. Swaminathan; Ravi T. Chadalavada; Kai O. Arras; Achim J. Lilienthal
Titolo: THÖR — people tracks; articolo associato: «THÖR: Human-Robot Navigation Data Collection and Accurate Motion Trajectories Dataset»
Sede e anno: IEEE Robotics and Automation Letters 5(2):676–682, 2020; Zenodo, 10-9-2019
Identificativo: DOI 10.5281/zenodo.3382145; DOI 10.1109/LRA.2020.2965416; arXiv:1909.04403
Link: https://zenodo.org/records/3382145
Verifica: verificata dal curatore il 14-11-2026 in parte — (rif-4) [API Zenodo, arXiv, Crossref]: autori, licenza CC BY 4.0, legame con l'articolo; i 100 Hz e i 339 s non ricontrollati
Usata per: traiettorie vere di persone al chiuso a 100 Hz; scelta n. 2 per l'ipotesi 4 (errore della previsione contro il tempo d'occlusione), 99 517 196 byte — `f10-dati/01-ricercatore/DATI_PUBBLICI.md` §3, §5 **[f7–f10: non vagliato dall'arbitro]**
Note: nessuna camera di profondità: parte da posizioni perfette. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### tum-rgbd [257]
Tipo: insieme di dati
Autori: Jürgen Sturm; Nikolas Engelhard; Felix Endres; Wolfram Burgard; Daniel Cremers
Titolo: TUM RGB-D Benchmark, sequenza `freiburg3_walking_static`; articolo associato: «A benchmark for the evaluation of RGB-D SLAM systems»
Sede e anno: IEEE/RSJ IROS 2012, pp. 573–580
Identificativo: DOI 10.1109/IROS.2012.6385773
Link: https://cvg.cit.tum.de/data/datasets/rgbd-dataset/download ; https://cvg.cit.tum.de/rgbd/dataset/freiburg3/rgbd_dataset_freiburg3_walking_static.tgz
Verifica: verificata dal curatore il 14-11-2026 in parte — (rif-4) [API] per l'articolo (aggiunto da me: il ruolo cita solo la pagina) e [T] per la presenza della sequenza nella pagina; la licenza «CC BY 4.0» NON l'ho trovata nella pagina dei file: non verificata
Usata per: sequenza minima di 474 074 105 byte, Kinect v1, 640×480, 30 Hz; scelta n. 1 per le ipotesi 1, 2, 5, 6 del contratto dei dati — `f10-dati/01-ricercatore/DATI_PUBBLICI.md` §1, §4, §5 **[f7–f10: non vagliato dall'arbitro]**
Note: luce strutturata, non stereo attivo; solo la posa della camera come verità. La licenza va riletta nella pagina principale dell'insieme. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### zenodo-radar-mmwave-occlusione [258]
Tipo: insieme di dati
Autori: Tao Wang
Titolo: The mmWave radar point cloud dataset for person identification under various occluded conditions
Sede e anno: Zenodo, 26-9-2023
Identificativo: DOI 10.5281/zenodo.8377254
Link: https://zenodo.org/records/8377254
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-4) [API Zenodo]: 9 persone che camminano dietro l'ostacolo, radar FMCW più camera RGB-D, CC BY 4.0
Usata per: radar a onde millimetriche con persone dietro un ostacolo; 508 208 132 byte — `f10-dati/01-ricercatore/DATI_PUBBLICI.md` §3 **[f7–f10: non vagliato dall'arbitro]**
Note: nessuna posizione vera dichiarata. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### zenodo-tof-vl53l5cx [259]
Tipo: insieme di dati
Autori: Giammarco Caroleo; Alessandro Albini; Perla Maiolino
Titolo: DS.ToFInitialCharacterization_InChToF.1.0; articolo associato: «Tiny LiDARs for Manipulator Self-Awareness: Sensor Characterization and Initial Localization Experiments» (Caroleo, Albini, De Martini, Barfoot, Maiolino)
Sede e anno: Zenodo, 24-9-2025; arXiv 5-3-2025 (IROS secondo il commento arXiv: anno non letto)
Identificativo: DOI 10.5281/zenodo.17190312; arXiv:2503.03449
Link: https://zenodo.org/records/17190312
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-4) [API Zenodo e arXiv]: tre VL53L5CX su un braccio robotico davanti a una lavagna in posizione nota, CC BY 4.0
Usata per: unico insieme pubblico trovato per il tempo di volo multizona, senza persone (lacuna dichiarata) — `f10-dati/01-ricercatore/DATI_PUBBLICI.md` §3 **[f7–f10: non vagliato dall'arbitro]**
Note: VL53L5CX, non L7CX né L8CX. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.


---

## 6. Comunicati e altre fonti (stampa, blog, forum, enciclopedie)

31 voci, da [260] a [290].

### aviationweek-ispezioni-droni [260]
Tipo: pagina di costruttore o comunicato (articolo di rivista)
Autori: manca
Titolo: dal percorso: «Aircraft inspections: drones accelerate toward next evolution»
Sede e anno: Aviation Week; data: non letta
Identificativo: manca
Link: https://aviationweek.com/mro/emerging-technologies/aircraft-inspections-drones-accelerate-toward-next-evolution
Verifica: aperta dal ruolo che la cita — (rif-4) dal curatore [T] parziale: nella pagina compaiono FAA, Boeing, Airbus e Delta; la frase sull'accettazione non riletta (l'articolo può essere tagliato per i non abbonati)
Usata per: ispezione visiva con drone in hangar accettata dall'autorità statunitense per un vettore e approvata dai due maggiori costruttori — `f7-estensione/05-esperto-dominio/CONSEGNA.md` righe 56 e 80 (S16) **[f7–f10: non vagliato dall'arbitro]**
Note: Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### detect-merlin-abar [261]
Tipo: pagina di costruttore o comunicato (presentazione a un convegno)
Autori: J. Lewis (dal nome del file; DeTect, secondo il ruolo)
Titolo: manca (presentazione TS5-P19)
Sede e anno: birdstrike.org; caricata nel 2024; convegno: non letto
Identificativo: TS5-P19
Link: https://birdstrike.org/wp-content/uploads/2024/04/TS5-P19-J.Lewis_.pdf
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-4) [T]: «Aircraft-Birdstrike Avoidance Radar», «Green = LOW» e «location, size, mass» presenti
Usata per: «ABAR» è la sigla di un prodotto di un solo costruttore, che dà un rischio per zona in tre colori calcolato da posizione, dimensione, massa e numero — `f9-preproposta/06-esperto-dominio/CONSEGNA.md` riga 23 (F1); `f9-preproposta/12-avversario/CONSEGNA.md` riga 48 (lì «non verificato») **[f7–f10: non vagliato dall'arbitro]**
Note: materiale del costruttore. Che ABAR sia la sigla di «un solo» costruttore è un'assenza su un campione. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### dxomark-rapporto-camera3d [262]
Tipo: altro (rapporto di prova campione)
Autori: DXOMARK
Titolo: rapporto campione su una camera 3D stereo (titolo esatto: non letto)
Sede e anno: 2025 (dal percorso)
Identificativo: manca
Link: https://corp.dxomark.com/wp-content/uploads/2025/02/DXOMARK_Report_Sample_3Dcamera_stereos.pdf
Verifica: aperta dal ruolo che la cita — (rif-4) dal curatore solo [200]
Usata per: fonte S12 del modello del sensore (uso preciso non riletto) — `f10-dati/02-sensori/MODELLO_SENSORE.md` riga 90 **[f7–f10: non vagliato dall'arbitro]**
Note: porta la dicitura «Confidential» pur essendo sul sito pubblico (annotazione del ruolo): solo consultazione. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### gerdsenai-da3-ros2 [263]
Tipo: altro (post di comunità su un forum)
Autori: GerdsenAI
Titolo: [Release] GerdsenAI's Depth Anything 3 ROS2 Wrapper with Real-Time TensorRT for Jetson
Sede e anno: forum Open Robotics Discourse, 5 febbraio 2026
Identificativo: discussione 52364
Link: https://discourse.openrobotics.org/t/release-gerdsenais-depth-anything-3-ros2-wrapper-with-real-time-tensorrt-for-jetson/52364
Verifica: verificata dal curatore il 14-11-2026 in parte — (rif-1) già verificata dal curatore in f3 [g], in parte: da 6,35 a 43+ fps su Jetson Orin NX 16 GB; la variante «small» non è nominata nel post. Non riaperta oggi. ‖ (rif-2) aperta dal curatore in f3 il 14-11-2026 («6,35 → 43+ fps su Jetson Orin NX 16 GB: sì»; variante «small»: assente nel messaggio); oggi non riaperta.
Usata per: «Depth Anything 3 small: 6 fps in PyTorch e 43 con TensorRT su Orin NX, dati della comunità» — `f1/c85dbcc51ea6/CONSEGNA.md` (visione-1, rif. [16])
Usata per: «Depth Anything 3 arriva a 43 fps su Jetson Orin NX secondo una fonte di comunità» — `f3/H-012/01-scene-dinamiche/SOLUZIONE.md` (§8).
Note: (rif-1) misura di terzi, non indipendente né ripetuta; a quale variante del modello si riferisca non è verificato. (rif-2) fonte di comunità, non primaria; non dice quale variante del modello. La soluzione la usa solo per dire che la profondità monoculare resta fuori. All'unione: nel gruppo rif-2 la chiave era `gerdsenai-da3-jetson` (senza link né titolo); tenuti i dati di rif-1.

### gulf-times-ally-solos [264]
Tipo: altro (articolo di stampa, fonte secondaria)
Autori: manca (nessuna firma né agenzia sulla pagina)
Titolo: Smart glasses and AI advances find purpose among blind users
Sede e anno: Gulf Times, rubrica Viewpoint, 9 gennaio 2026
Identificativo: articolo 718327
Link: https://www.gulf-times.com/article/718327/opinion/smart-glasses-and-ai-advances-find-purpose-among-blind-users
Verifica: dato diverso — (rif-1) [r], con correzione: pagina aperta; c'è «We don't really recommend people use smart glasses as a primary navigation tool» (amministratore delegato di Envision). Dato diverso: l'articolo non dice dove avviene l'elaborazione (né telefono né servizi remoti); dice solo che Envision usa più modelli, fra cui uno di OpenAI.
Usata per: F12: occhiali Ally Solos: elaborazione su telefono e servizi remoti; gli sviluppatori sconsigliano di usarli come strumento principale di navigazione — `f1/3fff79e9c3ea/FONTI.md`
Note: la prima metà dell'affermazione non è sostenuta da questa fonte: toglierla o trovare la documentazione del prodotto. Stampa generalista.

### iata-enhanced-gse-2022 [265]
Tipo: pagina di costruttore o comunicato (comunicato di un'associazione)
Autori: IATA
Titolo: comunicato del 6 dicembre 2022 sui mezzi di rampa evoluti (titolo esatto: non letto)
Sede e anno: IATA, 6-12-2022 (dal percorso)
Identificativo: 2022-12-06-04
Link: https://www.iata.org/en/pressroom/2022-releases/2022-12-06-04/
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-4) [T]: «could double to nearly $10 billion by 2035», «cause 40% of total incidents», «by 42% (IATA estimate)», «anti-collision and inching technology» presenti
Usata per: danno a terra fino a quasi 10 miliardi di dollari l'anno entro il 2035; nastri, caricatori, scale e pontili causano il 40 % degli incidenti; riduzione del 42 % — `f7-estensione/05-esperto-dominio/CONSEGNA.md` righe 54 e 80 (S14) **[f7–f10: non vagliato dall'arbitro]**
Note: correzione C10. Stima dell'associazione. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### journal-aviation-donecle [266]
Tipo: pagina di costruttore o comunicato (notizia)
Autori: manca
Titolo: dal percorso: «Donecle sets its drone to work for maintenance with AFI KLM E&M»
Sede e anno: Le Journal de l'Aviation; data: manca
Identificativo: 37578
Link: https://www.journal-aviation.com/en/news/37578-donecle-sets-its-drone-to-work-for-maintenance-with-afi-klm-e-m
Verifica: non raggiungibile — (rif-4) (404 oggi); dal ruolo: vista solo nel riassunto di un motore di ricerca
Usata per: in hangar i droni da ispezione si guidano con il LiDAR — `f7-estensione/05-esperto-dominio/CONSEGNA.md` righe 41 e 80 (S15, marca R) **[f7–f10: non vagliato dall'arbitro]**
Note: non citabile. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### kiwibot2022 [267]
Tipo: altro (articolo di blog di un'azienda)
Autori: Kiwibot (testo di Rafael Rincón)
Titolo: Thinking of Buying Stereo Cameras? Read This Product Comparison.
Sede e anno: HackerNoon, 15 luglio 2022
Identificativo: manca
Link: https://hackernoon.com/thinking-of-buying-stereo-cameras-read-this-product-comparison
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-1) [r]: pagina aperta; D435i in esterno «data can be significantly affected after two meters», errore circa 38 % in una prova; D435f circa 8 %; OAK-D Pro «very noisy in some sections», errore 25 %.
Usata per: F4: D435i degradata al sole oltre 2 m, D435f molto migliore, OAK-D Pro rumorosa — `f1/3fff79e9c3ea/FONTI.md`, `f1/3fff79e9c3ea/CONSEGNA.md` (§1.2)
Note: blog aziendale, una prova informale: non è fonte primaria né confronto controllato. Vale come indizio.

### maregroup-news [268]
Tipo: pagina di costruttore o comunicato
Autori: Mare Group S.p.A.
Titolo: News (elenco delle notizie)
Sede e anno: sito della società, letto il 14-11-2026
Identificativo: manca
Link: https://www.maregroup.it/news/
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-3) [g] — «15-09-2026 Via libera "Golden Power" per l'acquisizione di CTMAVIO»; «21-10-2026 Primo ordine da cliente estero…». Nell'elenco non compaiono le parole «hackathon», «percezione», «visione artificiale». Aperta anche dal ruolo che la cita.
Usata per: via libera Golden Power del 15-09-2026 — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §1, S10
Usata per: «non trovate» linee terrestri o navali, prodotti di percezione, notizie pubbliche sull'hackathon — stesso file, §1
Usata per: il Golden Power su CTMAVIO dice che il settore è vigilato — stesso file, §6
Note: un'assenza in un elenco di titoli è una prova debole: vale per i titoli di oggi, non per il contenuto delle notizie.

### maregroup-ordine-uncrewed-2026 [269]
Tipo: pagina di costruttore o comunicato
Autori: Mare Group S.p.A.
Titolo: Primo ordine da cliente estero da 1,7 milioni di euro per sistemi uncrewed
Sede e anno: sito della società, notizia del 21-10-2026
Identificativo: manca
Link: https://www.maregroup.it/news/primo-ordine-estero-sistemi-uncrewed
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-3) [g] — titolo, data, «del valore di circa 1,7 milioni di euro». Questa pagina non nomina CTMAVIO né il 2026 come anno d'esecuzione: stanno nelle tre voci seguenti. Aperta anche dal ruolo che la cita.
Usata per: ordine del 21-10-2026 da 1,7 milioni per «sistemi uncrewed»; cliente, piattaforma e uso non verificati — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` in testa e §1, S2
Note: correzione 12. La pagina rimanda a un comunicato integrale che non ho aperto: è il documento che deciderebbe il tipo di piattaforma (non risolto nel quadro).

### maregroup-sito [270]
Tipo: pagina di costruttore o comunicato
Autori: Mare Group S.p.A.
Titolo: Mare Group — Ingegneria ad alta tecnologia (pagina iniziale)
Sede e anno: sito della società, letto il 14-11-2026
Identificativo: manca
Link: https://www.maregroup.it/
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-3) [g] — «Ingegneria ad alta tecnologia per progettare, sviluppare e produrre sistemi complessi», «quotata sul mercato Euronext Growth Milan», i tre settori, «Product Design & Digital Twin». Aperta anche dal ruolo che la cita.
Usata per: profilo della società (settori, quotazione, linee tecnologiche) — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §1, S1
Note: pagina che cambia nel tempo; non ha una data di revisione.

### meta-sam3-blog [271]
Tipo: pagina di costruttore o comunicato
Autori: Meta
Titolo: SAM 3.1: Faster and More Accessible Real-Time Video Detection and Tracking With Multiplexing and Global Reasoning (aggiornamento in testa alla pagina di SAM 3)
Sede e anno: blog di Meta AI; aggiornamento del 27-03-2026 secondo f3 (data non riletta oggi)
Identificativo: manca
Link: https://ai.meta.com/blog/segment-anything-model-3/
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-1) già verificata dal curatore in f3 [r] soltanto: da 16 a 32 fps su una H100, video con numero medio di oggetti. Non riaperta oggi. ‖ (rif-2) «doubles the processing speed for videos with a medium number of objects, increasing throughput from 16 to 32 frames per second on a single H100 GPU». Già in f3/fonti (letta là attraverso un riassunto).
Usata per: «SAM 3.1 32 fps su H100» — `f1/c85dbcc51ea6/CONSEGNA.md` (§1.2, rif. [5])
Usata per: «SAM 3.1 passa da 16 a 32 fps su una H100: non è il calcolo di un hackathon» — `f3/H-012/01-scene-dinamiche/SOLUZIONE.md` (§8).
Note: (rif-1) comunicato del produttore, letto solo attraverso lo strumento che riassume: prova debole. (rif-2) comunicato del costruttore, non un articolo. Nella stessa pagina c'è la frase sui 30 ms di SAM 3 (vedi `carion2025`). All'unione: nel gruppo rif-2 la chiave era `meta-sam31`; f3 e rif-1 l'avevano letta solo attraverso un riassunto, rif-2 sul testo.

### realsense-forum-latenza [272]
Tipo: altro (messaggio di un utente in un forum del costruttore)
Autori: un utente del forum; risposta di un moderatore
Titolo: Depth Camera Latency
Sede e anno: RealSense Help Center, sezione Community, D400 Series, 12-04-2024
Identificativo: messaggio 28370679789587
Link: https://support.realsenseai.com/hc/en-us/community/posts/28370679789587-Depth-Camera-Latency
Verifica: dato diverso — (rif-2) i 35 ms sono dell'infrarosso, non della profondità. Pagina aperta oggi (nel torneo: solo riassunto). Testo: «the mean latency for the infrared sensor on my D455 running at 90 fps is 35 ms… am I correct to assume that the depth latency is greater than the infrared latency?». La risposta dice che la profondità è costruita nella camera prima della trasmissione e rimanda allo strumento `rs-data-collect`, senza un numero.
Usata per: latenza del sensore: «circa un periodo (33 ms a 30 fps, lettura incerta di un forum) e 35 ms misurati da un utente a 90 fps» — `f2/04-torneo/TORNEO.md` (parte 1, H-006 (b) e «Fonti»); `f3/H-012/01-scene-dinamiche/PREVISIONI.md` (C2: «una lettura incerta di un forum, non aperta»).
Note: correzione 3 in testa. Una misura di un utente, senza metodo descritto: non è una fonte per un bilancio di latenza. La frase sul «periodo» va citata da `realsense-alta-velocita-d435`.

### skybrary-acas-ra-ta [273]
Tipo: altro (enciclopedia di settore)
Autori: SKYbrary (EUROCONTROL e altri)
Titolo: ACAS Resolution and Traffic Advisories (dal percorso del link)
Sede e anno: manca
Identificativo: manca
Link: https://skybrary.aero/articles/acas-resolution-and-traffic-advisories
Verifica: non raggiungibile — (rif-4) (la pagina risponde con un controllo JavaScript; anche il ruolo dichiara «pagina non aperta»)
Usata per: in ACAS l'avviso di risoluzione raccomanda una manovra all'equipaggio — `f9-preproposta/12-avversario/CONSEGNA.md` riga 48; `f9-preproposta/06-esperto-dominio/CONSEGNA.md` riga 87 e `PREVISIONI.md` riga 11 **[f7–f10: non vagliato dall'arbitro]**
Note: la stessa affermazione è sostenuta da `eurocontrol-acas-guide` [T]: citare quella. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### sofema-attrezzi-fod [274]
Tipo: altro (blog di un ente di formazione)
Autori: Sofema Online
Titolo: dal percorso: «EASA Part 145 tooling store management and control procedures considering the problem of foreign object debris (FOD)»
Sede e anno: data: non letta
Identificativo: manca
Link: https://sofemaonline.com/about/blog/entry/easa-part-145-tooling-store-management-and-control-procedures-considering-the-problem-of-foreign-object-debris-fod-1
Verifica: aperta dal ruolo che la cita — (rif-4) dal curatore: la pagina risponde, ma nel testo scaricato non ho trovato «FOD» né «tool control» (contenuto forse caricato da script): non verificata
Usata per: in hangar un attrezzo non ritrovato resta in conto — `f7-estensione/08-creativo/CONSEGNA.md` riga 67 **[f7–f10: non vagliato dall'arbitro]**
Note: il ruolo stesso la chiama «fonte debole» e dichiara la procedura non verificata. Un blog non conta come fonte primaria. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### soldionline-ordine-uncrewed-2026 [275]
Tipo: pagina di costruttore o comunicato (stampa finanziaria)
Autori: SoldiOnline (firma non rilevata)
Titolo: Mare Group, primo ordine estero per sistemi uncrewed (titolo dell'indirizzo; il titolo esatto della pagina non è stato trascritto)
Sede e anno: soldionline.it, ottobre 2026
Identificativo: manca
Link: https://www.soldionline.it/notizie/azioni-italia/mare-group-primo-ordine-estero-sistemi-uncrewed
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-3) [g] — «circa 1,7 milioni di euro e sarà eseguito prevalentemente nel 2026», «componenti e strutture di precisione per applicazioni aeronautiche, motoristiche e UAV». Aperta anche dal ruolo che la cita.
Usata per: la stampa lega l'ordine a componenti e strutture per usi aeronautici, motoristici e UAV — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §1, S4
Note: deriva dal comunicato della società.

### st-community-940nm [276]
Tipo: pagina di costruttore o comunicato (forum del costruttore)
Autori: STMicroelectronics Community
Titolo: VL53L5CX emitter 940nm light
Sede e anno: forum ST; data: non letta
Identificativo: discussione 11515
Link: https://community.st.com/imaging-sensors-49/vl53l5cx-emitter-940nm-light-11515
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-4) [T]: «940 +/- 10nm is what we are shooting for» e «filter is not absolute» presenti (il ruolo l'aveva solo in riassunto, [r])
Usata per: banda del filtro a 940 nm non dichiarata nella scheda — `f9-preproposta/07-lidar/CONSEGNA.md` critica 1 ([8]) **[f7–f10: non vagliato dall'arbitro]**
Note: riguarda il VL53L5CX; l'estensione a L7CX e L8CX è un'ipotesi. Che chi scrive sia un dipendente ST non l'ho verificato. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### st-community-interferenza [277]
Tipo: pagina di costruttore o comunicato (forum del costruttore)
Autori: STMicroelectronics Community (risposte di dipendenti ST, secondo il ruolo)
Titolo: «Will multiple ToF sensors (VL53L series)… in close…»; «VL53L5CX mutual influence of multiple sensors»
Sede e anno: forum ST; date: non lette
Identificativo: m-p/61090; td-p/197217
Link: https://community.st.com/t5/imaging-sensors/will-multiple-tof-sensors-vl53l-series-specifically-in-close/m-p/61090 ; https://community.st.com/t5/imaging-sensors/vl53l5cx-mutual-influence-of-multiple-sensors/td-p/197217
Verifica: aperta dal ruolo che la cita — (rif-4) (solo riassunto, [r]); dal curatore [T] parziale: nella prima «ambient light» c'è, nella seconda la parola «ambient» non compare nel testo scaricato (la discussione può essere caricata da script)
Usata per: ogni sensore vede gli altri «as ambient light»; il disturbo compare come bersaglio in più con stato non valido — `f9-preproposta/07-lidar/CONSEGNA.md` critica 3 ([7]) **[f7–f10: non vagliato dall'arbitro]**
Note: un forum non è una scheda: va confermato con la prova T3 sull'hardware. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### st-community-trigger [278]
Tipo: pagina di costruttore o comunicato (forum del costruttore)
Autori: STMicroelectronics Community
Titolo: External trigger
Sede e anno: forum ST; data: non letta
Identificativo: discussione 155090
Link: https://community.st.com/imaging-sensors-49/external-trigger-155090
Verifica: verificata dal curatore il 14-11-2026 in parte — (rif-4) [T] solo per la presenza di «SYNC», «autonomous» e «trigger» nella pagina; l'affermazione «solo in modo autonomo» non riletta nel contesto
Usata per: il VL53L8CX ha il piedino SYNC, solo in modo autonomo — `f9-preproposta/07-lidar/CONSEGNA.md` critica 2 ([9]) **[f7–f10: non vagliato dall'arbitro]**
Note: da provare sull'hardware. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### teleborsa-commessa-rpas-2026 [279]
Tipo: pagina di costruttore o comunicato (agenzia di stampa)
Autori: Teleborsa
Titolo: Mare Group, prima commessa per velivoli a pilotaggio remoto: valore superiore a 1 milione di euro
Sede e anno: teleborsa.it, 5 giugno 2026
Identificativo: manca
Link: https://www.teleborsa.it/News/2026/06/05/mare-group-prima-commessa-per-velivoli-a-pilotaggio-remoto-valore-superiore-a-1-milione-di-euro-53.html
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-3) [g] — «circa 1,05 milioni di euro», «velivoli a pilotaggio remoto (RPAS) di dimensioni medio-grandi», «ingegneria di sistema e lo sviluppo di sottosistemi di bordo critici per la sicurezza». Aperta anche dal ruolo che la cita.
Usata per: prime commesse del 05-06-2026 (circa 1,05 milioni) su un velivolo a pilotaggio remoto medio-grande — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §1, S6
Note: deriva dal comunicato della società.

### teleborsa-ctmavio-2026 [280]
Tipo: pagina di costruttore o comunicato (agenzia di stampa)
Autori: Teleborsa
Titolo: Mare Group acquisisce CTMAVIO e rafforza la filiera dei droni per Aerospazio e Difesa
Sede e anno: teleborsa.it, 24 luglio 2026
Identificativo: manca
Link: https://www.teleborsa.it/News/2026/07/24/mare-group-acquisisce-ctmavio-e-rafforza-la-filiera-dei-droni-per-aerospazio-e-difesa-17.html
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-3) [g] — «Il corrispettivo per il 100% del capitale sociale di CTMAVIO è pari a 9 milioni», menzione del Golden Power. Aperta anche dal ruolo che la cita.
Usata per: accordo del 24-07-2026 per comprare CTMAVIO (9 milioni) — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §1, S9
Note: la chiusura dell'operazione resta non verificata, come nel quadro.

### teleborsa-nido-2026 [281]
Tipo: pagina di costruttore o comunicato (agenzia di stampa)
Autori: Teleborsa
Titolo: Mare Group entra nel capitale di NIDO al 20% con opzione per il controllo entro 24 mesi
Sede e anno: teleborsa.it, 9 giugno 2026
Identificativo: manca
Link: https://www.teleborsa.it/News/2026/06/09/mare-group-entra-nel-capitale-di-nido-al-20percent-con-opzione-per-il-controllo-entro-24-mesi-5.html
Verifica: dato diverso — (rif-3) pagina aperta [g]; ci sono il 20 %, «il drone H815», ricarica, voli oltre la linea di vista, supervisione, «ispezione di strade e infrastrutture, monitoraggio strutturale di pipeline e reti energetiche… sorveglianza perimetrale», «architettura dual-use». Il «51 %» nella pagina non c'è: c'è «opzione per il controllo entro 24 mesi». Aperta anche dal ruolo che la cita.
Usata per: ingresso al 20 % in NIDO «con opzione per il 51 %»; descrizione della piattaforma NIDO e dei suoi usi — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §1, S7
Usata per: il profilo pubblico della società è un drone da ispezione con stazione di ricovero e supervisione remota — `f6-specializzazione/01-esperto-dominio/SPECIALIZZAZIONE.md` §2
Note: correzione 7: scrivere «opzione per il controllo», non «per il 51 %», salvo un'altra fonte.

### teleborsa-ordine-uncrewed-2026 [282]
Tipo: pagina di costruttore o comunicato (agenzia di stampa, ripresa da Borsa Italiana)
Autori: Teleborsa
Titolo: Mare Group, primo ordine da un cliente estero per sistemi uncrewed da 1,7 milioni di euro
Sede e anno: Borsa Italiana, notizie Teleborsa, 21-10-2026
Identificativo: manca
Link: https://www.borsaitaliana.it/borsa/notizie/teleborsa/finanza/mare-group-primo-ordine-da-un-cliente-estero-per-sistemi-uncrewed-da-17-milioni-di-euro-21_2026-10-21_TLB.html?lang=it
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-3) [g] — «attraverso la controllata CTMAVIO», «circa 1,7 milioni di euro, da un cliente estero, da concludersi prevalentemente nel 2026». Aperta anche dal ruolo che la cita.
Usata per: l'ordine è preso tramite CTMAVIO ed è da eseguire per lo più nel 2026 — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §1, S3
Note: deriva dal comunicato della società.

### teleborsa-propulsione-uav-2026 [283]
Tipo: pagina di costruttore o comunicato (agenzia di stampa)
Autori: Teleborsa
Titolo: Mare Group, contratto da 8,3 milioni di euro per unità di propulsione UAV
Sede e anno: teleborsa.it, 28 luglio 2026
Identificativo: manca
Link: https://www.teleborsa.it/News/2026/07/28/mare-group-contratto-da-8-3-milioni-di-euro-per-unita-di-propulsione-uav-13.html
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-3) [g] — «8,3 milioni», «fornitura di oltre 6.000 … kit per velivoli senza pilota, con ricavi distribuiti in modo uniforme sui tre esercizi». Il ruolo che la cita l'aveva vista solo in un risultato di ricerca.
Usata per: accordo quadro del 28-07-2026 da 8,3 milioni, oltre 6.000 kit motore — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §1, S11
Note: deriva dal comunicato della società.

### therobotreport-veo [284]
Tipo: pagina di costruttore o comunicato (articolo di una rivista di settore, autrice del costruttore)
Autori: Clara Vu (Veo Robotics, secondo il ruolo)
Titolo: Advanced vision and the future of robot safety in manufacturing
Sede e anno: The Robot Report, 1 luglio 2020
Identificativo: manca
Link: https://www.therobotreport.com/advanced-vision-future-robot-safety-manufacturing/
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-4) [T]: «something can be seen behind it» e «treated as occupied» presenti ‖ All'unione (16:33): pagina scaricata; nei metadati «author»: «Clara Vu» e «datePublished»: 2020-07-01; il titolo è quello dell'intestazione della pagina (il titolo per i motori di ricerca è «Safety for robots in manufacturing comes from advanced vision»). Nel gruppo rif-4 autrice e data erano «manca».
Usata per: un sistema 3D di sorveglianza di velocità e separazione classifica i volumi in vuoto, occupato o sconosciuto, e ciò che nessun sensore vede è trattato come occupato — `f7-estensione/05-esperto-dominio/CONSEGNA.md` righe 21 e 80 (S8) **[f7–f10: non vagliato dall'arbitro]**
Note: fonte di parte. Nella sezione E la chiave provvisoria è [vu2020]. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### vogiatzoglou2024 [285]
Tipo: altro (contributo in un blog accademico: fonte secondaria)
Autori: Plixavra Vogiatzoglou
Titolo: The AI Act National Security Exception: room for manoeuvres?
Sede e anno: Verfassungsblog, 9 dicembre 2024 (nel dibattito «The EU AI Act's Impact on Security Law»)
Identificativo: manca (DOI non cercato)
Link: https://verfassungsblog.de/the-ai-act-national-security-exception/
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-3) [g] — la citazione «exclusively for military, defence or national security purposes» c'è; c'è anche «if the same AI system is also used for law enforcement and public security purposes, then it must abide by» il regolamento. Il ruolo che la cita l'aveva vista solo in un risultato di ricerca.
Usata per: il regolamento sull'intelligenza artificiale esclude i sistemi a uso esclusivamente militare, di difesa o di sicurezza nazionale; il duplice uso resta dentro — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §6, S38
Note: correzione 11. Per i limiti della scheda del curatore un blog non è fonte primaria: la primaria è `ue-2024-1689`. L'espressione «duplice uso» è una lettura del ruolo, non una parola del testo. Nella sezione E la chiave provvisoria è [verfassungsblog-aiact].

### websim-ordine-uncrewed-2026 [286]
Tipo: pagina di costruttore o comunicato (stampa finanziaria)
Autori: Websim, redazione
Titolo: Mare Group - Nuovo ordine da 1,7 milioni di euro
Sede e anno: websim.it, 21-10-2026, ore 10:30
Identificativo: manca
Link: https://www.websim.it/azioni/small-mid-cap/notizie/mare-group-nuovo-ordine-da-1-7-milioni-di-euro/
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-3) [g] — «tramite la controllata CTMAVIO S.r.l., il primo ordine da un cliente estero per la fornitura di sistemi uncrewed, per un valore di circa 1,7 milioni di euro». Aperta anche dal ruolo che la cita.
Usata per: conferma dell'ordine del 21-10-2026 — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §1, S5
Note: deriva dal comunicato della società.

### websim-task-force-x-2026 [287]
Tipo: pagina di costruttore o comunicato (stampa finanziaria)
Autori: Websim, redazione
Titolo: Mare Group - Scelta dalla NATO per la Task Force X
Sede e anno: websim.it, 10-07-2026, ore 14:36
Identificativo: manca
Link: https://www.websim.it/azioni/small-mid-cap/notizie/mare-group-scelta-dalla-nato-per-la-task-force-x/
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-3) [g] — «Task Force X – Central Mediterranean, un'iniziativa NATO a guida italiana in corso presso il Poligono di Torre Veneri», «sorveglianza continua e la protezione delle infrastrutture critiche», NIDO, GMSPAZIO, CTM Avio. Aperta anche dal ruolo che la cita.
Usata per: partecipazione del 10-07-2026 alla Task Force X — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §1, S8
Usata per: sorveglianza di perimetri e infrastrutture come profilo pubblico — `f6-specializzazione/01-esperto-dominio/SPECIALIZZAZIONE.md` §2
Note: deriva dal comunicato della società; il titolo «scelta dalla NATO» è della testata.

### wikipedia-kinect [288]
Tipo: altro (enciclopedia)
Autori: Wikipedia
Titolo: Kinect
Sede e anno: versione del 14-11-2026 non annotata
Identificativo: manca
Link: https://en.wikipedia.org/wiki/Kinect
Verifica: aperta dal ruolo che la cita — (rif-4) ([g], testo grezzo); dal curatore solo [200]
Usata per: campo e distanza minima del Kinect v1 (57° × 43°, circa 0,8 m) — `f10-dati/04-embedded/PREVISIONI.md` (note in fondo), `INVENTARIO_E_DECISIONE.md` ([6]) **[f7–f10: non vagliato dall'arbitro]**
Note: fonte secondaria (lo dice il ruolo). Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

### wikipedia-ricerca-bayesiana [289]
Tipo: altro (voce di enciclopedia, fonte secondaria)
Autori: collaboratori di Wikipedia
Titolo: Bayesian search theory
Sede e anno: Wikipedia in inglese, versione letta il 14-11-2026
Identificativo: manca (identificativo della revisione non annotato)
Link: https://en.wikipedia.org/wiki/Bayesian_search_theory
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente — (rif-1) già verificata dal curatore in f3 [r]. Rafforzata oggi [g] sul testo sorgente della voce: p′ = p(1−q)/(1−pq) e r′ = r/(1−pq); il caso USS Scorpion (maggio 1968). ‖ (rif-2) aperta dal curatore in f3 il 14-11-2026, attraverso un riassunto (p′ = p(1−q)/(1−pq)); oggi non riaperta. La fonte primaria a cui rimanda (Stone, 1975) non è stata aperta da nessuno.
Usata per: analogia di creativo-2: cercare e non trovare sposta la probabilità sulle celle non cercate, p′ = p(1−q)/(1−pq), r′ = r/(1−pq) — `f1/e30f9e2dd4d7/CONSEGNA.md`
Usata per: l'idea «Il sottomarino perduto»: particelle che nelle celle viste libere pesano (1−Pd) — `f2/01-traduzione/SCHEDE.md` (`creativo-2`); H-016 nel torneo — `f2/04-torneo/TORNEO.md` (parte 3).
Note: (rif-1) non è fonte primaria; rimanda a `stone1975`. La formula è una riga di calcolo di Bayes, verificabile a mano. (rif-2) nei file del gruppo c'è solo il nome dell'idea. Una voce di enciclopedia non conta come fonte primaria: nei documenti finali va citata come tale o sostituita.

### wikipedia-tcas [290]
Tipo: altro (enciclopedia)
Autori: Wikipedia
Titolo: Traffic collision avoidance system
Sede e anno: versione non annotata
Identificativo: manca
Link: https://en.wikipedia.org/wiki/Traffic_collision_avoidance_system
Verifica: aperta dal ruolo che la cita — (rif-4) dal curatore solo [200]
Usata per: a un TA non si manovra, a un RA si risponde subito — `f9-preproposta/09-interfacce/CONSEGNA.md` righe 31 e 80; `f9-preproposta/06-esperto-dominio/PREVISIONI.md` riga 27 **[f7–f10: non vagliato dall'arbitro]**
Note: fonte secondaria; la primaria è `eurocontrol-acas-guide`. Citata solo nelle estensioni f7–f10 o nei file esterni: NON ancora vagliata dall'arbitro.

---

## 7. Chiavi provvisorie usate nelle sezioni → chiave definitiva e numero

Le chiavi fra parentesi quadre sono state estratte con una ricerca testuale dalle sei sezioni del documento di stato (`f11-documentazione/sez-a` … `sez-f`, file `SEZIONE.md`): 90 chiavi distinte. La stessa fonte ha a volte chiavi diverse in sezioni diverse (per esempio [realsense-altavelocita] e [realsense-highspeed]): nel documento finale va usata la chiave definitiva. Non sono chiavi di riferimento, e non compaiono nella tabella: [conto], [argomento], [argomenti], [dopo] (testo delle sezioni B e C), [g] e [r] (marche di lettura della sezione D).

| Chiave provvisoria | Sezioni | Chiave definitiva | N. | Stato | Nota |
|---|---|---|---|---|---|
| [ahn2019] | D, F | `ahn2019` (uguale) | [3] | verificata |  |
| [astm-f3442] | E | `astm-f3442-25` | [162] | dato diverso |  |
| [aviationweek-ispezioni] | E | `aviationweek-ispezioni-droni` | [260] | aperta dal ruolo |  |
| [balch2019] | E | `balch2019` (uguale) | [5] | verificata |  |
| [bewley2016] | B | `bewley2016` (uguale) | [8] | verificata |  |
| [cao2023] | B | `cao2023` (uguale) | [11] | verificata |  |
| [dpr-495-1992] | E | `codice-strada-reg-art162` | [164] | aperta dal ruolo | numero del D.P.R. a memoria, non verificato; letto su un sito divulgativo |
| [dxomark-stereo] | D | `dxomark-rapporto-camera3d` | [262] | aperta dal ruolo |  |
| [easa-categoria-aperta] | E | `easa-faq-open-category` | [169] | dato diverso |  |
| [easa-sora25] | E | `easa-amc-gm-2019-947` | [167] | verificata | allegato alla decisione ED 2025/018/R (contiene il rimando a SORA 2.5) |
| [eurocae-ed275] | E | `eurocae-ed-275` | [170] | dato diverso |  |
| [eurocontrol-acas] | F | `eurocontrol-acas-guide` | [171] | verificata |  |
| [eurocontrol-acasguide] | E | `eurocontrol-acas-guide` | [171] | verificata |  |
| [eurocontrol-asterix062] | E | `eurocontrol-asterix-cat062` | [172] | dato diverso | edizione letta 1.18 (copia non ufficiale); corrente 1.21 |
| [faa-aim-rwsl] | E | `faa-aim-2-1-6` | [175] | verificata |  |
| [flightsafety-fod] | E | `faa-ac-150-5220-24` | [173] | verificata | la voce porta la sigla della circolare FAA; la pagina letta è l'articolo «Clean Sweep» |
| [iata-gse2022] | E | `iata-enhanced-gse-2022` | [265] | verificata |  |
| [imo-colreg7] | E | `colreg-regola7` | [165] | verificata |  |
| [imo-mass] | E | `dnv-imo-codice-mass` | [166] | verificata | notizia tecnica di DNV, non il testo dell'IMO |
| [imo-msc192] | E | `imo-msc192-79` | [179] | verificata |  |
| [iso-10218-2] | E | `iso-10218-2` (uguale) | [180] | solo riassunto di ricerca | voce creata all'unione; norma non letta da nessuno |
| [iso-13855] | E | `iso-13855` (uguale) | [181] | solo riassunto di ricerca |  |
| [iso-3691-4] | E | `iso-3691-4` (uguale) | [182] | verificata in parte |  |
| [iso-ts-15066] | E | `iso-ts-15066` (uguale) | [184] | non raggiungibile |  |
| [kayukawa2019] | E | `kayukawa2019` (uguale) | [38] | verificata |  |
| [koschi2021] | E | `koschi2021` (uguale) | [44] | dato diverso | l'articolo di rivista; il quadro di dominio (S33) cita invece `koschi-mediatum-1575368` |
| [ldrobot-ld19-scheda] | D | `ldrobot-ld19-scheda` (uguale) | [126] | aperta dal ruolo |  |
| [lee2026] | C | `lee2026` (uguale) | [50] | dato diverso |  |
| [legge-185-1990] | E | `it-legge-185-1990` | [185] | verificata in parte | il link citato è la pagina dell'autorità (`maeci-uama`) |
| [librealsense-filtri] | D | `librealsense` | [209] | verificata | voce di gruppo: file `doc/post-processing-filters.md`; la pagina in rete sullo stesso tema è `realsense-filtri-post` |
| [librealsense-metadati] | D | `librealsense` | [209] | verificata | voce di gruppo: file `doc/frame_metadata.md` e `rs_frame.h` |
| [livox-mid360] | D, E | `livox-mid-360` | [127] | verificata |  |
| [lupu2020] | E | `lupu2020` (uguale) | [57] | dato diverso |  |
| [luxonis-tof] | D | `luxonis-tof` (uguale) | [130] | verificata |  |
| [mandaokar2026] | E | `mandaokar2026` (uguale) | [61] | verificata |  |
| [maregroup-news] | E | `maregroup-news` (uguale) | [268] | verificata |  |
| [maregroup-ordine2026] | A, E | `maregroup-ordine-uncrewed-2026` | [269] | verificata |  |
| [martinez2014] | E | `martinez2014` (uguale) | [62] | dato diverso |  |
| [marvel2017] | E | `marvel2017` (uguale) | [63] | verificata |  |
| [nuss2018] | E | `nuss2018` (uguale) | [70] | verificata |  |
| [orbbec-femtobolt] | D | `orbbec-femto-bolt` | [134] | verificata |  |
| [orbbec-femtobolt-sincronia] | D | `orbbec-femto-bolt-sincronia` | [135] | verificata |  |
| [orbbec-gemini330-scheda] | D | `orbbec-gemini-330-scheda` | [136] | verificata |  |
| [orbbec-gemini335] | B, D | `orbbec-gemini-335` | [137] | verificata |  |
| [orzechowski2018] | E | `orzechowski2018` (uguale) | [72] | verificata |  |
| [park2026] | F | `park2026` (uguale) | [253] | dato diverso |  |
| [pipewire-conf] | A, B, C | `pipewire-conf` (uguale) | [226] | verificata |  |
| [px4-collisionprevention] | E | `px4-collision-prevention` | [227] | verificata |  |
| [px4-obstacledistance] | E | `px4-obstacle-distance` | [229] | verificata |  |
| [pypi-pyrealsense2] | F | `pyrealsense2-pypi` | [232] | aperta dal ruolo |  |
| [qiu2023] | D | `qiu2023` (uguale) | [78] | verificata |  |
| [realsense-altavelocita] | A, D | `realsense-alta-velocita-d435` | [140] | dato diverso |  |
| [realsense-confronto] | B, D | `realsense-confronto-camere` | [142] | verificata |  |
| [realsense-d400-scheda] | D | `realsense-d400-scheda` (uguale) | [144] | verificata |  |
| [realsense-esempi] | F | `realsense-file-di-esempio` | [255] | aperta dal ruolo |  |
| [realsense-filtri] | C, F | `realsense-filtri-post` | [233] | verificata |  |
| [realsense-highspeed] | B, C | `realsense-alta-velocita-d435` | [140] | dato diverso |  |
| [realsense-librealsense] | F | `librealsense` | [209] | verificata | voce di gruppo: note della versione 2.59.1 |
| [realsense-postprocessing] | B | `realsense-filtri-post` | [233] | verificata |  |
| [realsense-taratura] | D | `realsense-bkm-taratura` | [141] | verificata | il PDF «BKMs»; la versione in rete è `realsense-taratura-profondita` |
| [realsense-tuning] | B, C | `realsense-taratura-profondita` | [146] | verificata | la versione in rete; il PDF è `realsense-bkm-taratura` |
| [roboflow-rfdetr] | A, B | `roboflow-rf-detr` | [235] | verificata |  |
| [rtca-do365] | E | `rtca-do-365` | [188] | verificata in parte | le cifre «35 s e oltre un chilometro» non sono in questa fonte; per l'ordine di grandezza vedi `thipphavong2016` |
| [rudenko2019] | F | `thor` | [256] | verificata in parte | voce dell'insieme di dati THÖR (articolo associato dentro la voce) |
| [scholler2020] | B, C | `scholler2020` (uguale) | [85] | verificata |  |
| [slamtec-c1] | D | `slamtec-rplidar-c1` | [152] | verificata | pagina delle specifiche del costruttore |
| [soldionline-ordine2026] | E | `soldionline-ordine-uncrewed-2026` | [275] | verificata |  |
| [spinello2011] | F | `friburgo-rgbd-people` | [249] | verificata | voce dell'insieme di dati (i due articoli del 2011 dentro la voce) |
| [st-um3038] | D | `st-um3038` (uguale) | [154] | verificata |  |
| [st-vl53l5cx] | D | `st-vl53l5cx` (uguale) | [155] | verificata |  |
| [st-vl53l7cx] | A, B, C, D, F | `st-vl53l7cx` (uguale) | [156] | verificata |  |
| [st-vl53l8cx] | D | `st-vl53l8cx` (uguale) | [157] | verificata |  |
| [teleborsa-commesse2026] | E | `teleborsa-commessa-rpas-2026` | [279] | verificata |  |
| [teleborsa-ctmavio2026] | E | `teleborsa-ctmavio-2026` | [280] | verificata |  |
| [teleborsa-kitmotore2026] | E | `teleborsa-propulsione-uav-2026` | [283] | verificata |  |
| [teleborsa-nido2026] | E | `teleborsa-nido-2026` | [281] | dato diverso |  |
| [tum-rgbd] | F | `tum-rgbd` (uguale) | [257] | verificata in parte |  |
| [ue-2017-745] | E | `ue-2017-745` (uguale) | [189] | verificata |  |
| [ue-2019-945] | E | `ue-2019-945` (uguale) | [190] | verificata |  |
| [ue-2019-947] | E | `ue-2019-947` (uguale) | [191] | verificata in parte |  |
| [ue-2021-664] | E | `ue-2021-664` (uguale) | [192] | non raggiungibile |  |
| [ue-2021-821] | E | `ue-2021-821` (uguale) | [193] | verificata in parte |  |
| [ue-2023-1230] | E | `ue-2023-1230` (uguale) | [194] | verificata in parte |  |
| [ultralytics-coco] | C | `ultralytics-coco-yaml` | [242] | verificata | file di configurazione; l'articolo su COCO è `lin2014` |
| [ultralytics-yolo26] | A, B | `ultralytics-yolo26` (uguale) | [244] | dato diverso |  |
| [unitree-l2] | D | `unitree-l2` (uguale) | [160] | verificata |  |
| [verfassungsblog-aiact] | E | `vogiatzoglou2024` | [285] | verificata | fonte secondaria; la primaria è `ue-2024-1689` |
| [vu2020] | E | `therobotreport-veo` | [284] | verificata | autrice e data confermate all'unione |
| [waveshare-c1] | D | `waveshare-rplidar-c1` | [161] | verificata | pagina del rivenditore (prezzo) |
| [websim-taskforcex2026] | E | `websim-task-force-x-2026` | [287] | verificata |  |

## 8. Da risolvere

**8.1 Chiavi usate nelle sezioni che non hanno una voce:** nessuna.

**8.2 Corrispondenze imperfette** (la chiave ha una voce, ma chi scrive il documento finale deve scegliere).
- [iso-10218-2], [iso-ts-15066], [iso-13855] — le tre norme ISO non le ha lette nessuno; `iso-10218-2` è una voce creata all'unione. Ciò che se ne dice passa da `marvel2017` (fonte secondaria, letta) e da `therobotreport-veo` (fonte di parte).
- [koschi2021] — nella sezione E indica l'articolo di rivista; il quadro di dominio (S33) cita un altro documento (`koschi-mediatum-1575368`), mai aperto.
- [librealsense-filtri], [librealsense-metadati], [realsense-librealsense] — tre chiavi per una voce di gruppo (`librealsense`); la pagina in rete sui filtri è un'altra voce (`realsense-filtri-post`, chiavi [realsense-filtri] e [realsense-postprocessing]).
- [realsense-taratura] e [realsense-tuning] — lo stesso testo del costruttore in due forme (PDF e pagina in rete): due voci.
- [flightsafety-fod] — la voce è intestata alla circolare FAA 150/5220-24, ma la pagina letta è un articolo di rivista: la circolare non l'ha aperta nessuno.
- [verfassungsblog-aiact] — fonte secondaria; per il regolamento sull'intelligenza artificiale la primaria è `ue-2024-1689`, letta su una copia non ufficiale.
- [dpr-495-1992] — il numero del decreto è a memoria e la pagina letta è un sito divulgativo: da rileggere su Normattiva.
- [eurocontrol-asterix062] — edizione letta 1.18 (trascrizione non ufficiale); corrente 1.21.
- [rudenko2019], [spinello2011], [tum-rgbd], [park2026] — voci di insiemi di dati: l'articolo associato sta dentro la voce e non ha una voce BibTeX propria.
- [legge-185-1990], [imo-mass] — citate attraverso una pagina di un'autorità o di una società di classifica, non sul testo.

**8.3 Fonti che le sezioni dichiarano mancanti.**
- Sezione A: una norma o una guida sulla qualificazione di un ausilio per persone non vedenti come dispositivo medico (qui c'è solo la definizione dell'articolo 2 in `ue-2017-745`, su una copia non ufficiale: la classificazione del prototipo resta non risolta); il regolamento dell'hackathon con criteri, pesi e condizioni della demo (non è una fonte esterna: manca fra gli ingressi).
- Sezione D: i prezzi (tutti non verificati, salvo Femto Bolt a 418 $ in f3 e Unitree L2 a 419 $ oggi); la OAK-D Pro W e la camera Arducam (le voci `luxonis-oak-d-pro-w` e `arducam-tof` ci sono, ma sono «non raggiungibili»); i programmi di odometria (le voci ci sono: `basalt`, `rtabmap`, `open-vins`, `vins-fusion`, `orb-slam3`, `kiss-icp`, `fast-lio`, `nvidia-cuvslam`: verificata la licenza, non le prestazioni).
- Sezione E: il link di `lupu2020` (c'è: DOI 10.3390/s20205821) e i link delle norme ISO (mancano: testi a pagamento).
- Sezione F: l'articolo di riferimento di TUM RGB-D (c'è, dentro la voce `tum-rgbd`: IROS 2012, DOI 10.1109/IROS.2012.6385773).

**8.4 Affermazioni e nomi rimasti senza fonte** (non vanno scritti come fatti finché non hanno una voce).
- Le prove NEES/NIS come misura standard della coerenza di un filtro (`f1/3fff79e9c3ea/FONTI.md`, `f1/21d3813ca7e1/CONSEGNA.md`): fonte **manca**. Un curatore propone, a memoria e senza averlo aperto, il manuale di Bar-Shalom, Li e Kirubarajan (Wiley, 2001): non verificato.
- Glidance Glide e biped NOA: non trovati; non citarli.
- Nomi di metodi citati senza un riferimento proprio: LVIS, Deep OC-SORT, FastTracker, TrackTrack, MOTR, Social-LSTM, SoPhie, Cal-DETR, D-DETR, JARUS SORA 2.5, il metodo originale dell'intersezione delle covarianze. (Hanno ora una voce, per i soli dati bibliografici: ETH e UCY, COCO, ByteTrack, BoT-SORT, S-GAN, SR-LSTM, RED, il filtro di Kalman, il metodo ungherese, i limiti di Clopper-Pearson, il filtro di Bernoulli.)
- La «classe 1 FDA» dei LiDAR: il regolamento statunitense non è citato; `iec-60825-1` è citata solo attraverso la pagina di un costruttore.
- Le cifre «35 s e oltre un chilometro» (S20: nelle due norme citate non ci sono; per l'ordine di grandezza c'è `thipphavong2016`, che il quadro non cita), «1 W» del termico (S17), «51 %» (S7), «il primo a nominare le macchine mobili autonome» (S29), il mezzo di piazzale a 5–8 m/s.
- La latenza della sintesi vocale e dell'uscita audio via cavo o Bluetooth; la premessa fisica sul vetro (`intel-000030012` non è raggiungibile).
- Velocità del pedone (1,2–1,4 m/s; 2,5 m/s al massimo), larghezza del corpo 40 cm, quota del sensore 1,2 m: ipotesi degli autori, senza fonte.
- «Rolling Grid» e «log-odds» come tecniche nominate senza riferimento; che l'aggiornamento in log-odds presupponga una mappa ferma.
- C = 0,85 m della ISO 13855 e, con esso, i 2,80 m e 1,68 m calcolati in f9.
- I rimandi `<Cite ref=…>` della bozza della squadra: non ricostruibili.
- Gli insiemi di dati KTP, EPFL, JRDB, CDTB (`insiemi-non-raggiungibili`): senza indirizzo.

**8.5 Voci da non usare come sostegno finché non sono rilette.** `skoglar2012`, `hunt2013`, `weitz2013`, `sciencedirect-s0926580524005867`, `journal-aviation-donecle`, `sick-sensori-3d`, `sofema-attrezzi-fod`, `iso-13855`, `iso-9241-303`, `faa-ordine-7110-65`, `koschi-mediatum-1575368`, `intel-000030012`, `intel-t265-fine-produzione`, `sunny-mars07a`, `st-volantino-vl53l7cx-vl53l8cx`, e tutte le pagine dei rivenditori usate per un prezzo. Le voci di enciclopedia (`wikipedia-ricerca-bayesiana`, `wikipedia-kinect`, `wikipedia-tcas`), i blog e i forum valgono come indizio, non come fonte primaria.

## 9. Che cosa propongo dopo

1. Nel documento di stato sostituire le chiavi provvisorie con quelle definitive della tabella del §7, e portare nelle frasi le correzioni 1–7 e 10 del primo elenco e le cifre 1–6 del secondo: sono quelle che cambiano una frase già scritta.
2. Prima di mettere una cifra in un testo per la giuria, rileggerla nella fonte se la voce è «verificata in parte» o «aperta dal ruolo»; in particolare le tabelle di `hetzel2024`, `mercat2019`, `lindemann2023`, `krejci2026`, `doersch2022`, la Tabella 3 di `imo-msc192-79`, la Tabella 16 di `eurocontrol-acas-guide`.
3. Le voci «non raggiungibili» le riapre una persona con un navigatore: `ue-2021-664` e le altre pagine di EUR-Lex, le due pagine Intel, mediaTUM, iso.org.
4. Fissare versione o commit per i depositi e per le pagine «latest» o «main» (PX4, Ultralytics, librealsense, OctoMap): oggi nessuna voce lo porta.
5. A ogni nuova valutazione: le fonti nuove entrano qui con una voce nel formato comune e nel file BibTeX con la stessa chiave; quando l'arbitro vaglia un'estensione, la marca «[f7–f10: non vagliato dall'arbitro]» si toglie dagli usi di quella estensione.
6. Previsione (`fonti-unione-1`): riaprendo a mano le 13 voci «non raggiungibili», almeno una porta un dato diverso da quello citato. La smentisce una rilettura in cui tutte e 13 confermano il dato.
