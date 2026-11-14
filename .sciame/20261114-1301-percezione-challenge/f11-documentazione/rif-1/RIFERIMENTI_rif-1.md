# Riferimenti — gruppo rif-1 (fase f1 e verifica f3), `sciame-fonti`, 14 novembre 2026

Fonti esaminate: le nove `f1/*/CONSEGNA.md`, `f1/3fff79e9c3ea/FONTI.md` (F1–F30), `f3/fonti/FONTI_VERIFICATE.md`; per i link completi anche `f1/985ccd9bca46/PREVISIONI.md` e `f1/3fff79e9c3ea/PREVISIONI.md`. I percorsi sono relativi a `.sciame/20261114-1301-percezione-challenge`. Le cartelle f7–f10 (estensioni in corso, non vagliate dall'arbitro) NON sono state lette per questo gruppo.

## 0. In testa: conti, cambi di stato, regole violate

**Conti** (contati con `grep` sulle righe «Verifica:» di questo file). **84 voci**, di cui 42 di tipo «articolo scientifico» (prestampe e rassegne comprese).
- **29 verificate da me oggi** (fonte aperta oggi per la prima volta da un curatore): 22 con il dato citato presente; 4 in parte, con riserva o con correzione (`livox-mid-360`, `zhang2026`, `yang2025`, `gulf-times-ally-solos`); 3 solo nei dati bibliografici (`sun2022`, `klatzky2006`, `adamides2025`).
- **43 già verificate dal curatore in f3**: per 28 ho ricontrollato o completato oggi qualcosa (autori, pagine, DOI, o la frase citata); 15 non le ho riaperte e valgono per la sola verifica di f3.
- **12 non verificate**: 7 non aperte da nessun curatore (`adorama-d455`, `rs-online-realsense`, `rivenditori-d435i-prezzi`, `botland-oak-d-lite`, `iec-60825-1`, `iso-ts-15066`, `stone1975`) e 5 non raggiungibili (`st-volantino-vl53l7cx-vl53l8cx`, `st-um2884`, `intel-negozio-d455`, `luxonis-oak-d-pro-w`, `arducam-tof`).
- Più 8 gruppi di affermazioni o nomi senza alcun riferimento (§ 6).
- Fra gli articoli scientifici, quelli il cui **contenuto citato** resta non letto sul testo: `hornung2013` (OctoMap), `klatzky2006`, `adamides2025` (F26), `sun2022` (nessuna cifra citata), più `koschi2021`, `moras2011`, `martinez2014`, `lupu2020`, `romlay2021`, `xu2023`, `giudice2008`, `shan2025`, `timans2024`, `chen2024` letti sul solo riassunto.

**Che cosa vuol dire «verificata» qui.** Riguarda la fonte (esiste, con questi autori e questa sede; il dato citato c'è), non il sistema: niente di ciò che segue è provato sull'hardware, e le misure dello sciame restano «sostenute dai dati in simulazione». Marche: **[g]** = dato trovato con una ricerca testuale nel testo grezzo scaricato oggi (pagina, PDF, file del deposito, oppure la risposta di un registro: arXiv, Crossref, PubMed, DOAJ, Europe PMC, HAL, Semantic Scholar); **[r]** = letto attraverso lo strumento di lettura che riassume (più debole). I registri bibliografici sono fonti secondarie affidabili per autori, sede, pagine e DOI, non per il contenuto. Indipendenza: condivido il modello linguistico con i ruoli che citano e con il curatore di f3; l'indipendenza sta nel testo delle fonti.

**Voci che non esistono.** Nessuna: tutti i riferimenti con un link o un identificativo corrispondono a un documento reale. Restano senza fonte (§ 6): le prove NEES/NIS, Glidance Glide e biped NOA, e «MATR», citato senza link (l'identificazione proposta è mia).

**Voci attribuite male o in modo incompleto (correzioni).**
1. `koschi2021`: non «IEEE T-IV 2020» ma vol. 6(2), pp. 249–265, giugno **2021** (già corretto in f3; riconfermato oggi su Crossref [g]).
2. `weng2020`: arXiv 2008.08063 è il riassunto esteso per i Workshop di ECCV 2020; l'articolo intero è a IROS 2020, pp. 10359–10366 (f3; pagine da Crossref oggi [g]).
3. `lupu2020` (F8): non è «lo studio Sound of Vision 2020» senza autori, ma Lupu, Mitruț, Stan, Ungureanu, Kalimeri, Moldoveanu, Sensors 20(20):5821 (f3; riassunto riletto oggi su Crossref [g]).
4. `martinez2014` (F7): il PDF del KIT dà 404; vale il DOI 10.1007/978-3-319-08599-9_20 (f3).
5. `adamides2025` (F26): nel file F26 è citata senza autori né titolo. È Adamides, Subramanian, Arora, Sahin, «Perception and Computation for Speed and Separation Monitoring Architectures», Robotics 14(4):41, 2025 [g]. È una rassegna di architetture di percezione: l'affermazione «la distanza protettiva si calcola con l'incertezza di misura e la latenza» NON è nel riassunto e il testo intero non è raggiungibile (403): **affermazione non verificata**.
6. `shan2025` (F28), `xu2023` (F10), `dossantos2025` (F13), `us-brevetto-11846916` (F27), `standley2017` (F30), `giudice2008`/`klatzky2006` (F11): nei file mancavano autori, titolo o sede; ora sono completi (vedi le voci).
7. `chen2024` e `zhang2026`: `visione` li cita solo come link ([12], [13]); sono rispettivamente «Using Diffusion Priors for Video Amodal Segmentation» (CVPR 2025) e «Amodal SAM» (arXiv, aprile 2026). Il riassunto di `zhang2026` dice «leverages SAM», non «SAM 2»: la dicitura «derivato da SAM 2» di `visione` **non è verificata**.
8. `gulf-times-ally-solos` (F12): l'articolo NON dice dove avviene l'elaborazione (telefono o servizi remoti); la frase sulla navigazione è dell'amministratore delegato di Envision e riguarda gli occhiali intelligenti in generale, non il modello Ally Solos [r].
9. `kozlov2026` (F6): il 92,9 % viene da 22 partecipanti **senza** disabilità visiva; il 93,75 % dai 14 con disabilità visiva (il testo, § 3.4, scrive 93,7 %) [r]. I «28 intervistati» e «highly undesirable» sono nel testo [r]. Sede: «LBR of HRI 2026» (commento arXiv [g]).
10. `pololu-vl53l8cx-3419`: il link [7] di `visione` porta alla scheda del **VL53L8CX** (45°, 4 m), non del VL53L7CX; il dato del 7CX (90° in diagonale, 350 cm) c'è solo nella tabella di confronto della stessa pagina [r].

**Cifre che non tornano.**
1. `zholus2025` (TAPNext): «1024 punti a 348 fps su H100» non è nell'articolo; la Tabella 2 dà 187 fps su H100 e 42 su V100 (f3 [g]).
2. `ldrobot-ld19`: tenuta alla luce 30 klx, non 60 (i 60 klx sono dell'STL-19P del kit D500); risoluzione 0,8° non trovata (f3).
3. `ultralytics-yolo26`: «YOLOE-26 40,6 AP su LVIS» è della variante x, non di un modello leggero (f3 [r]).
4. `lee2026` (F29): «fattore medio 1,68» non è scritto nell'articolo, è exp(0,519) calcolato dal ricercatore: va dichiarato come derivato (f3).
5. `ultralytics-tracciatori`: `track_buffer: 30` è il predefinito di ByteTrack, ma il tracciatore predefinito di Ultralytics è TrackTrack (f3 [g]).
6. `ding2026` (F21): 25,6 fps è confermato, ma su «a single GPU with 32GB memory», colonna «FPS V100» della Tabella 1 [r]: è una GPU da centro di calcolo, non hardware modesto. Il «hardware non identificato» di FONTI.md si chiude così.
7. `roboticscenter-d455`: `lidar` cita 399–417 $; oggi la pagina dà **650 $** («Backorder») [r]. Il prezzo citato non è più sulla pagina.
8. `livox-mid-360`: `lidar` cita 899–1092 $; oggi la pagina del rivenditore scrive «Contact for pricing» [r]: prezzo **non verificato**.
9. `standley2017` (F30): «circa 150 000 prodotti Amazon» è nel testo dell'articolo («∼150k products», da circa 3 milioni di prodotti Amazon) [g], non nel riassunto.
10. `st-um2884` / `st-vl53l5cx`: «8×8 a 15 Hz → 4×4 a 60 Hz» (creativo-4): la scheda DS13754 Rev 2 conferma «60 Hz frame rate capability» e i modi 8×8 a 15 Hz e 4×4 a 30 Hz nelle tabelle [g]; che i 60 Hz valgano solo in 4×4 non l'ho trovato nella scheda, e UM2884 non è raggiungibile: **non verificato**.

**Regole violate o scostamenti (anche per errore).**
- Regola 3: non ho scritto previsioni prima delle verifiche (25 minuti in tutto): gli esiti sono constatazioni, non previsioni rette o smentite.
- Regola 5: il materiale scaricato (risposte dei registri, PDF di ST, di image2mass) sta nella cartella temporanea della sessione, sottocartella `rif1-scaricati`, non in questa; non ho eseguito niente dal suo interno. Lo strumento di lettura ha salvato da solo un PDF (Munir e altri, arXiv 2303.14404) in `~/.claude/projects/…/tool-results/`, fuori dalla mia cartella: l'ho solo letto con `pdftotext`.
- Rete: usata solo per verificare; nelle richieste nessun nome di persona né dettaglio del progetto. Crossref ha risposto 429 a una prima raffica di richieste parallele; rifatte in sequenza.
- Tempo: verifiche in rete dalle 16:10:55 alle 16:17 circa, stesura fino alle 16:25 circa (ore da `date -Is`): dentro i 25 minuti. Per questo 15 voci di f3 non sono state riaperte e 7 pagine di rivenditori o norme non sono state aperte.
- Limite del conteggio: «verificata» copre gradi diversi (dato trovato nel testo grezzo [g], dato letto attraverso lo strumento che riassume [r], soli dati bibliografici): il grado è scritto in ogni voce e non va appiattito quando si uniscono i gruppi.
- Non raggiungibili oggi: st.com (timeout), mdpi.com, doaj.org, openaccess.thecvf.com, arducam.com (403), ecfr.gov, link.springer.com, hal.science, pmc.ncbi.nlm.nih.gov (reindirizzamenti o controlli anti-automa). Dove possibile ho usato una copia o un registro, e l'ho scritto nella voce.

**Che cosa propongo dopo.** (a) Non citare nel documento finale F26 per l'affermazione su incertezza e latenza: citare la norma (`iso-ts-15066`) solo dopo averne letto il testo, oppure togliere l'affermazione. (b) Togliere o ricontrollare a mano ogni prezzo: due su due di quelli ricontrollati oggi sono cambiati. (c) Dare una fonte alle prove NEES/NIS (§ 6) prima di scriverle come «standard». (d) Per `hornung2013`, `moras2011`, `klatzky2006`, `koschi2021` il contenuto citato poggia sul solo riassunto o sui soli dati bibliografici: bastano come «vedi anche», non come prova di una cifra.

---

## 1. Sensori e hardware

### st-vl53l5cx
Tipo: scheda tecnica
Autori: STMicroelectronics
Titolo: VL53L5CX — Time-of-Flight 8x8 multizone ranging sensor with wide field of view (scheda tecnica)
Sede e anno: STMicroelectronics, DS13754 Rev 2, agosto 2021 (la revisione può non essere l'ultima)
Identificativo: DS13754 Rev 2
Link: https://cdn.sparkfun.com/assets/6/e/3/0/6/vl53l5cx-datasheet.pdf (copia SparkFun; st.com non risponde)
Verifica: già verificata dal curatore in f3 [g]: 45°×45°, 63° in diagonale, 400 cm; 4×4 a 30 Hz: 4,0 m al buio, 1,7 m a 5 klx. Ricontrollata oggi [g]: intestazione «DS13754 - Rev 2 - August 2021», «60 Hz frame rate capability», tabelle con 8×8 a 15 Hz e 4×4 a 30 Hz.
Usata per: campo 45°×45° (63° diag.), 400 cm; tre unità = 135° — `f1/dfac83300259/CONSEGNA.md` (§1.1, prova P-np2)
Usata per: campo orizzontale 45° fra i 7 sensori di P1 — `f1/b8262bfed263/CONSEGNA.md`
Usata per: «L5CX e L8CX: 45°×45° (r)» — `f1/985ccd9bca46/CONSEGNA.md` (§2.1)
Usata per: «45°×45° (63–65° in diagonale): tre coprono 135°», dichiarato non verificato sul testo — `f1/e30f9e2dd4d7/CONSEGNA.md` (critica 4)
Note: i numeri sono dichiarazioni del costruttore; 5 klx è la condizione di prova della scheda, non il sole pieno (f3, punto 3).

### st-vl53l7cx
Tipo: scheda tecnica
Autori: STMicroelectronics
Titolo: VL53L7CX — Time-of-Flight 8x8 multizone ranging sensor with 90° FoV (scheda tecnica)
Sede e anno: STMicroelectronics, DS13865 Rev 6, marzo 2023
Identificativo: DS13865 Rev 6
Link: https://www.pololu.com/file/0J1992/vl53l7cx.pdf (copia Pololu); pagina ST: https://www.st.com/en/imaging-and-photonics-solutions/vl53l7cx.html (timeout)
Verifica: già verificata dal curatore in f3 [g]: 60°×60° (90° diag.), 350 cm, «three sensors can cover 180° x 60°»; 3,5 m = 4×4 a 30 Hz al buio su bianco 88 %; 2,0 m = 8×8 a 15 Hz; a 5 klx 0,65 m (4×4) e 0,5 m (8×8); grigio 17 % in 8×8: 0,8 m al buio (tabelle 17 e 18). Non riaperta oggi.
Usata per: «60° x 60° (90° diag.), 4x4 o 8x8 zone, fino a 350 cm» (F2, marcata R) — `f1/3fff79e9c3ea/FONTI.md`, `f1/3fff79e9c3ea/CONSEGNA.md` (§1.1)
Usata per: 60°×60°, tre sensori 180°×60°; 8×8: 2,0 m al buio, 0,5 m a 5 klx, 0,8 m su grigio 17 % — `f1/985ccd9bca46/CONSEGNA.md` (§2.1, §2.2, tabella, rif. [1])
Usata per: «VL53L7CX 60°×60°» — `f1/c85dbcc51ea6/CONSEGNA.md` (§1.3, rif. [7])
Usata per: campo orizzontale 60° in P1 — `f1/b8262bfed263/CONSEGNA.md`
Note: titolo esatto della scheda non riletto oggi (formulazione mia sul modello ST): controllarlo sul PDF prima di citarlo alla lettera. «350 cm» e «2,0 m» sono due modi diversi (f3, punto 2), non una discordanza. Classe laser 1 dichiarata da ST secondo `lidar`: non ricontrollata.

### st-vl53l8cx
Tipo: scheda tecnica
Autori: STMicroelectronics
Titolo: VL53L8CX — Low-power high-performance 8x8 multizone Time-of-Flight sensor (scheda tecnica)
Sede e anno: STMicroelectronics, DS14161 Rev 7, agosto 2023
Identificativo: DS14161 Rev 7
Link: https://www.pololu.com/file/0J2029/vl53l8cx.pdf (copia Pololu); citato come https://www.st.com/resource/en/datasheet/vl53l8cx.pdf (st.com non risponde)
Verifica: già verificata dal curatore in f3 [g]: 45°×45°, 65° diag., 400 cm; a 5 klx 2,85 m in 4×4 a 30 Hz e 1,55 m in 8×8 a 15 Hz (bianco 88 %). Non riaperta oggi.
Usata per: «VL53L8CX 45°×45°, 4 m» — `f1/c85dbcc51ea6/CONSEGNA.md` (§1.3, rif. [7])
Usata per: campo orizzontale 45° in P1 — `f1/b8262bfed263/CONSEGNA.md`; «L8CX: 45°×45° (r)» — `f1/985ccd9bca46/CONSEGNA.md`
Note: titolo esatto della scheda non riletto oggi (formulazione mia sul modello ST): controllare sul PDF prima di citarlo alla lettera.

### st-volantino-vl53l7cx-vl53l8cx
Tipo: pagina di costruttore o comunicato
Autori: STMicroelectronics
Titolo: volantino VL53L7CX / VL53L8CX (titolo esatto: manca)
Sede e anno: STMicroelectronics; anno: manca
Identificativo: manca
Link: https://www.st.com.cn/resource/en/flyer/vl53l7cx-vl53l8cx-flyer.pdf
Verifica: non raggiungibile (f3: «non verificabile, sostituito dalle schede»); i ruoli l'hanno vista solo nel riassunto di un motore di ricerca.
Usata per: L5CX e L8CX a 45°×45° — `f1/985ccd9bca46/CONSEGNA.md` (rif. [2]); campi dei multizona ST — `f1/b8262bfed263/CONSEGNA.md` (Fonti)
Note: non citarla; usare `st-vl53l7cx` e `st-vl53l8cx`.

### st-um2884
Tipo: documentazione di software
Autori: STMicroelectronics
Titolo: UM2884 — A guide to using the VL53L5CX multizone Time-of-Flight ranging sensor with a wide field of view Ultra Lite Driver (ULD) (titolo ricavato dal link, non letto)
Sede e anno: STMicroelectronics; revisione e anno: manca
Identificativo: UM2884
Link: https://st.com/resource/en/user_manual/um2884-a-guide-to-using-the-vl53l5cx-multizone-timeofflight-ranging-sensor-with-a-wide-field-of-view-ultra-lite-driver-uld-stmicroelectronics.pdf
Verifica: non raggiungibile (st.com: connessione interrotta, oggi e in f3); il ruolo la dichiara «non verificata sul testo».
Usata per: «il passaggio 8×8 a 15 Hz → 4×4 a 60 Hz del VL53L5CX» (creativo-4) — `f1/e30f9e2dd4d7/CONSEGNA.md`
Note: conferma parziale da `st-vl53l5cx` (60 Hz di capacità massima [g]); il legame 60 Hz ↔ solo 4×4 resta non verificato.

### pololu-vl53l8cx-3419
Tipo: pagina di costruttore o comunicato
Autori: Pololu
Titolo: VL53L8CX Time-of-Flight 8×8-Zone Distance Sensor Carrier with Voltage Regulators, 400cm Max (articolo 3419)
Sede e anno: Pololu, pagina prodotto, letta il 14-11-2026
Identificativo: Pololu #3419
Link: https://www.pololu.com/product/3419
Verifica: verificata dal curatore il 14-11-2026 (rif-1) [r]: pagina aperta; 65° in diagonale (45° orizzontali e verticali), 4 m, 4×4 o 8×8 zone; tabella di confronto: VL53L5CX 400 cm e 65° diag., VL53L7CX 350 cm e 90° diag., VL53L8CX 400 cm e 65° diag.
Usata per: «VL53L8CX 45°×45°, 4 m; VL53L7CX 60°×60°» — `f1/c85dbcc51ea6/CONSEGNA.md` (rif. [7]); «4 m al buio (confronto Pololu)» — `f1/985ccd9bca46/PREVISIONI.md` (P3)
Note: è la pagina di un rivenditore; il «60°×60°» del 7CX non è scritto così qui (c'è «90° diagonal»): per quel dato vale `st-vl53l7cx`.

### orbbec-femto-bolt
Tipo: scheda tecnica
Autori: Orbbec
Titolo: Femto Bolt (pagina prodotto) e scheda «ORBBEC Datasheet Femto Bolt», v01
Sede e anno: Orbbec; scheda PDF 0816-v01, agosto 2023; pagina letta il 14-11-2026 (in f1 e f3)
Identificativo: ORBBEC_Datasheet_Femto-Bolt-0816-v01
Link: https://www.orbbec.com/products/tof-camera/femto-bolt/ ; https://www.orbbec.com/products/femto-bolt/ ; https://www.orbbec.com/wp-content/uploads/2023/08/ORBBEC_Datasheet_Femto-Bolt-0816-v01.pdf
Verifica: già verificata dal curatore in f3 [g]: 120°×120° (largo) e 75°×65° (stretto), 850 nm; largo raggruppato 0,25–2,88 m (512×512, fino a 30 fps); largo pieno 0,25–2,21 m (1024×1024, 5 o 15 fps); stretto 0,5–3,86 m e 0,5–5,46 m (raggruppato); IMU [r]. Ambiente: la pagina scrive «Indoor», la scheda v01 «Indoor/Semi-Outdoor». Non riaperta oggi.
Usata per: F1: 120°×120°, 0,25–2,88 m, «Indoor» — `f1/3fff79e9c3ea/FONTI.md`, `f1/3fff79e9c3ea/CONSEGNA.md` (§1.1, §1.2), `f1/3fff79e9c3ea/PREVISIONI.md` (P1)
Usata per: «portata 0,25–2,88 m in modo largo» — `f1/c85dbcc51ea6/CONSEGNA.md` (rif. [8])
Usata per: «0,25–2,21 m, 15 fps, 418–559 $ l'una» (ricerca) — `f1/dfac83300259/CONSEGNA.md` (§1.1)
Usata per: 120°×120°, 0,25–2,88 m, «Indoor / Semi-outdoor», 5,46 m stretto — `f1/985ccd9bca46/CONSEGNA.md` (§2.3, tabella, rif. [3])
Usata per: 75° e 120°, portata al più 2,88 m — `f1/b8262bfed263/CONSEGNA.md` (requisiti-1)
Note: 2,88 e 2,21 m sono due modi, entrambi giusti (f3, punto 1). Il prezzo di 559 $ citato da `nuvole-punti` non è verificato. Classe laser: non verificata.

### orbbec-negozio-femto-bolt
Tipo: pagina di costruttore o comunicato
Autori: Orbbec
Titolo: Femto Bolt (negozio in linea)
Sede e anno: Orbbec Store, letta il 14-11-2026 (in f3)
Identificativo: manca
Link: https://store.orbbec.com/products/femto-bolt
Verifica: già verificata dal curatore in f3 [g]: 418 $. Non riaperta oggi (in f1 il negozio aveva risposto 429 a `lidar`).
Usata per: 418 $ l'una, 1254 $ per tre — `f1/985ccd9bca46/CONSEGNA.md` (§2.3), `f1/985ccd9bca46/PREVISIONI.md` (P4)
Note: prezzo in dollari, del giorno; disponibilità in Italia non verificata.

### orbbec-femto-bolt-sincronia
Tipo: documentazione di software
Autori: Orbbec
Titolo: Synchronize Multiple Femto Bolt Devices
Sede e anno: Orbbec, documentazione in linea; revisione: manca
Identificativo: manca
Link: https://doc.orbbec.com/documentation/Orbbec%20Femto%20Bolt%20Documentation/Synchronize%20Multiple%20Femto%20Bolt%20Devices
Verifica: già verificata dal curatore in f3 [g]: «offset from each other by 160us or more»; impulso di 125 µs. Aperta anche dal ruolo che la cita. Non riaperta oggi.
Usata per: catture sfalsate di almeno 160 µs col cavo di sincronizzazione — `f1/985ccd9bca46/CONSEGNA.md` (§2.3, rif. [4]), `f1/985ccd9bca46/PREVISIONI.md` (P5)
Note: vale per la Femto Bolt; per i multizona ST nessun enunciato sull'interferenza è stato trovato (non verificato).

### orbbec-gemini-335
Tipo: pagina di costruttore o comunicato
Autori: Orbbec
Titolo: Gemini 335 (pagina prodotto)
Sede e anno: Orbbec, letta il 14-11-2026 (in f1 e f3)
Identificativo: manca
Link: https://www.orbbec.com/products/stereo-vision-camera/gemini-335/
Verifica: già verificata dal curatore in f3 [g]: 90°×65°, ottimale 0,26–3 m, 1280×800 a 30 fps, IMU, interno ed esterno; tipo di otturatore: assente. Non riaperta oggi.
Usata per: 90°×65°, 0,26–3 m, 1280×800 a 30 fps, IMU — `f1/985ccd9bca46/CONSEGNA.md` (tabella, rif. [7]); prezzo 330–369 $ da rivenditori — `f1/985ccd9bca46/PREVISIONI.md` (P6)
Note: il prezzo 330–369 $ non è verificato (nessun link del rivenditore nei file).

### luxonis-tof
Tipo: documentazione di software
Autori: Luxonis
Titolo: ToF Depth Perception
Sede e anno: Luxonis, documentazione in linea; revisione: manca
Identificativo: manca
Link: https://docs.luxonis.com/hardware/platform/depth/ToF-depth
Verifica: già verificata dal curatore in f3 [g]: 640×480, 20 cm–5 m, «<1% indoors, <2% outdoors», «Issues when using multiple ToFs (interference)». Non riaperta oggi.
Usata per: F3: ToF Luxonis 5 m, «<2% outdoors»; interferenza fra più ToF — `f1/3fff79e9c3ea/FONTI.md`, `f1/3fff79e9c3ea/CONSEGNA.md` (§1.1, §1.2), `f1/3fff79e9c3ea/PREVISIONI.md` (P1)
Note: fonte del costruttore; non dice a quale illuminamento vale «outdoors». La discordanza con Orbbec («Indoor») è vera fra costruttori (K-009 di f3): la decide una prova al sole sul sensore posseduto.

### kiwibot2022
Tipo: altro (articolo di blog di un'azienda)
Autori: Kiwibot (testo di Rafael Rincón)
Titolo: Thinking of Buying Stereo Cameras? Read This Product Comparison.
Sede e anno: HackerNoon, 15 luglio 2022
Identificativo: manca
Link: https://hackernoon.com/thinking-of-buying-stereo-cameras-read-this-product-comparison
Verifica: verificata dal curatore il 14-11-2026 (rif-1) [r]: pagina aperta; D435i in esterno «data can be significantly affected after two meters», errore circa 38 % in una prova; D435f circa 8 %; OAK-D Pro «very noisy in some sections», errore 25 %.
Usata per: F4: D435i degradata al sole oltre 2 m, D435f molto migliore, OAK-D Pro rumorosa — `f1/3fff79e9c3ea/FONTI.md`, `f1/3fff79e9c3ea/CONSEGNA.md` (§1.2)
Note: blog aziendale, una prova informale: non è fonte primaria né confronto controllato. Vale come indizio.

### qiu2023
Tipo: articolo scientifico
Autori: Z. Qiu, J. Martínez-Sánchez, P. Arias
Titolo: Evaluation and comparison of different time of flight cameras for outdoor applications
Sede e anno: ISPRS Annals of the Photogrammetry, Remote Sensing and Spatial Information Sciences, X-1/W1-2023, pp. 17–23, 2023 (pubblicato il 5-12-2023)
Identificativo: DOI 10.5194/isprs-annals-X-1-W1-2023-17-2023
Link: https://isprs-annals.copernicus.org/articles/X-1-W1-2023/17/2023/
Verifica: già verificata dal curatore in f3 [g]. Ricontrollata oggi su Crossref [g]: autori, pagine, e nel riassunto «their outdoor applications remain limited, mainly due to challenges like sunlight interference»; prove su Azure Kinect e Pmd Monstar.
Usata per: F5: l'uso esterno del ToF resta limitato dall'interferenza solare — `f1/3fff79e9c3ea/FONTI.md`, `f1/3fff79e9c3ea/CONSEGNA.md` (§1.2, §3)
Usata per: «al sole l'iToF è limitato» — `f1/c85dbcc51ea6/CONSEGNA.md` (rif. [9])
Note: è una prova su due camere e tre casi ad alta riflettività, non una rassegna (FONTI.md la chiama «rassegna» nella consegna: impreciso).

### realsense-confronto-camere
Tipo: pagina di costruttore o comunicato
Autori: RealSense (già Intel RealSense)
Titolo: Compare depth cameras
Sede e anno: realsenseai.com, letta il 14-11-2026 (in f3)
Identificativo: manca
Link: https://www.realsenseai.com/compare-depth-cameras/ ; citata anche come https://www.intelrealsense.com/compare-depth-cameras (non risolve) e https://realsenseai.com/cn/compare-depth-cameras/
Verifica: già verificata dal curatore in f3 [g, colonne attribuite via r]: D455 87°×58°, ideale 0,6–6 m, otturatore globale su profondità e RGB, IMU; D435i 87°×58°, 0,3–3 m, RGB a otturatore progressivo, IMU. Non riaperta oggi.
Usata per: «D435: ideale 0,3–3 m, 87°×58°» (ricerca) — `f1/dfac83300259/CONSEGNA.md` (§1.4)
Usata per: RealSense D435 e D455 a 87° in P1 — `f1/b8262bfed263/CONSEGNA.md`
Note: il dominio intelrealsense.com non risolve più: usare realsenseai.com.

### intel-negozio-d455
Tipo: pagina di costruttore o comunicato
Autori: Intel RealSense (negozio)
Titolo: Intel RealSense Depth Camera D455 (pagina del negozio)
Sede e anno: store.intelrealsense.com; data: manca
Identificativo: manca
Link: https://store.intelrealsense.com/buy-intel-realsense-depth-camera-d455.html
Verifica: non raggiungibile (f3: il dominio intelrealsense.com non risolve); letta dal ruolo attraverso uno strumento che riassume.
Usata per: D455: campo 87°×58°, portata 0,6–6 m, errore «< 2 % a 4 m» (da cui σ_pos ≈ 3 cm) — `f1/c85dbcc51ea6/CONSEGNA.md` (§1.5, visione-1, rif. [11])
Note: campo e portata sono confermati da `realsense-confronto-camere` (f3); «±2 % a 4 m» è confermato oggi solo sulla pagina di un rivenditore (`roboticscenter-d455` [r]). La σ_pos di 3 cm è un'ipotesi del ruolo, non un dato della scheda.

### adorama-d455
Tipo: pagina di costruttore o comunicato (rivenditore)
Autori: Adorama
Titolo: Intel RealSense D455 (pagina del rivenditore; titolo esatto: manca)
Sede e anno: adorama.com; data: manca
Identificativo: manca
Link: https://www.adorama.com/in82635dsd45.html
Verifica: non verificata (non aperta né in f3 né oggi); letta dal ruolo attraverso uno strumento che riassume.
Usata per: D455 con otturatore globale su profondità e RGB — `f1/c85dbcc51ea6/CONSEGNA.md` (§1.7, rif. [17])
Note: il dato è confermato da una fonte migliore, `realsense-confronto-camere` (f3 [g]): citare quella.

### roboticscenter-d455
Tipo: pagina di costruttore o comunicato (rivenditore)
Autori: RoboticsCenter
Titolo: RealSense D455 (pagina del rivenditore)
Sede e anno: roboticscenter.ai, letta il 14-11-2026
Identificativo: manca
Link: https://www.roboticscenter.ai/store/product/intel-realsense-d455
Verifica: verificata dal curatore il 14-11-2026 (rif-1) [r]: pagina aperta; 87°×58° (±3°), 0,6–6 m, «±2% at 4m», IMU BMI085, otturatore globale (profondità e RGB). Dato diverso: il prezzo oggi è 650 $ («Backorder»), non 399–417 $.
Usata per: D455 87°×58°, IMU BMI085, 0,6–6 m, da 399 a 417 $ — `f1/985ccd9bca46/CONSEGNA.md` (tabella, rif. [5]), `f1/985ccd9bca46/PREVISIONI.md` (P6)
Note: prezzo cambiato o diverso dal citato: non usare la cifra 399–417 $ senza ricontrollo.

### rs-online-realsense
Tipo: pagina di costruttore o comunicato (rivenditore)
Autori: RS Components
Titolo: pagine prodotto RealSense D435if (0155773) e D455 (0155774); titoli esatti: manca
Sede e anno: rs-online.com; data: manca
Identificativo: codici RS 0155773 e 0155774
Link: https://uk.rs-online.com/web/p/depth-cameras/0155773 ; https://nl.rs-online.com/web/p/depth-cameras/0155774
Verifica: non verificata (prezzi esclusi dal controllo di f3; non aperta oggi).
Usata per: D435i fra 362 e 550 $; D435if «0.3 m, 3 m Max Range» — `f1/985ccd9bca46/CONSEGNA.md` (rif. [6]), `f1/985ccd9bca46/PREVISIONI.md` (P6)
Note: prezzo non verificato.

### rivenditori-d435i-prezzi
Tipo: pagina di costruttore o comunicato (rivenditori)
Autori: Wamatek; RoboticsCenter
Titolo: pagine prodotto RealSense D435i; titoli esatti: manca
Sede e anno: data: manca
Identificativo: manca
Link: https://wamatek.com/products/intel-realsense-d435i-webcam-2-megapixel-30-fps-usb-3-2 ; https://www.roboticscenter.ai/store/product/realsense-d435i
Verifica: non verificata (non aperte né in f3 né oggi).
Usata per: prezzi della D435i fra 362 e 550 $ — `f1/985ccd9bca46/PREVISIONI.md` (P6), ripresi in `f1/985ccd9bca46/CONSEGNA.md` (§2)
Note: citate solo in PREVISIONI.md; prezzo non verificato.

### slamtec-rplidar-c1
Tipo: pagina di costruttore o comunicato
Autori: Slamtec (pagina del rivenditore Waveshare)
Titolo: RPLIDAR C1 (pagina prodotto Waveshare, SKU 26535; pagina Slamtec)
Sede e anno: waveshare.com, letta il 14-11-2026
Identificativo: Waveshare SKU 26535
Link: https://www.waveshare.com/rplidar-c1.htm
Verifica: già verificata dal curatore in f3 [r] sulla pagina Slamtec (12 m al 70 %, 6 m al 10 %, 5 kHz, 10 Hz tipici, 0,72°, 40 klx). Ricontrollata oggi [r] sulla pagina Waveshare: 0,05–12 m (70 %), 0,05–6 m (10 %), 5000 Hz, 8–12 Hz (tipico 10), 0,72°, ±30 mm, «FDA Class 1», 79,99 $; la tenuta alla luce non è sulla pagina Waveshare.
Usata per: 12 m al 70 %, 6 m al 10 %; ±30 mm (da cui rumore di velocità 0,4 m/s e di accelerazione 7 m/s², calcolo del ruolo); classe 1 FDA; 5000 punti/s, 10 Hz, 0,72°; 70–80 $ — `f1/985ccd9bca46/CONSEGNA.md` (§2.5, §2.6, tabella, lidar-2, rif. [8])
Note: «±30 mm» usato come scarto tipo è un'ipotesi dichiarata del ruolo. La classe FDA è una dichiarazione del costruttore.

### ldrobot-ld19
Tipo: pagina di costruttore o comunicato
Autori: LDROBOT (pagine di Waveshare e OpenELAB)
Titolo: DTOF LIDAR LD19 (Waveshare); LDROBOT D500 DTOF LiDAR Kit, STL-19P (OpenELAB); scheda «LDROBOT STL-19P Datasheet EN v1.0»
Sede e anno: date: manca
Identificativo: STL-19P Datasheet v1.0
Link: https://www.waveshare.com/dtof-lidar-ld19.htm ; https://openelab.io/products/ldrobot-d500-dtof-lidar-kit ; https://files.waveshare.com/wiki/D500-LiDAR-Kit/LDROBOT_STL-19P_Datasheet_EN_v1.0(1).pdf
Verifica: già verificata dal curatore in f3, con correzione: LD19 (Waveshare [r]) 30 klx, 4500 Hz, 0,02–12 m, 5–13 Hz; i 60 klx sono dell'STL-19P (OpenELAB [g]); risoluzione angolare 0,8°: non trovata. Dato diverso: 30 klx e non 60 per l'LD19. Non riaperta oggi.
Usata per: «LD19: 0,8°, 5–13 Hz, 12 m» (ricerca), 8,9 fasci su un pedone a 4 m — `f1/dfac83300259/CONSEGNA.md` (nuvole-punti-2)
Usata per: «60 klx (LD19, r)», 12 m, 69–70 $ — `f1/985ccd9bca46/CONSEGNA.md` (tabella, rif. [9]), `f1/985ccd9bca46/PREVISIONI.md` (P7)
Note: LD19 e STL-19P (kit D500) sono due prodotti: non scambiare le cifre. Prezzo non verificato.

### unitree-l2
Tipo: pagina di costruttore o comunicato
Autori: Unitree Robotics
Titolo: Unitree 4D LiDAR L2 (pagina prodotto)
Sede e anno: unitree.com, letta il 14-11-2026
Identificativo: manca
Link: https://www.unitree.com/L2
Verifica: verificata dal curatore il 14-11-2026 (rif-1) [r]: pagina aperta e dato presente: 360°×90° (96° nel modo ad angolo negativo), 30 m al 90 %, 15 m al 10 % (attribuzione della colonna dedotta dall'impaginazione), 64000 punti/s utili, 5,55 Hz, «Class 1 (IEC60825-1:2014)», ENET UDP e TTL UART, IMU a 6 assi, 419 $.
Usata per: 360°×90°, 30 m (15 m al 10 %), 64000 punti/s a 5,55 Hz, 419 $, classe 1 IEC 60825-1:2014 — `f1/985ccd9bca46/CONSEGNA.md` (tabella, lidar-2, «Sicurezza ottica», rif. [10]), `f1/985ccd9bca46/PREVISIONI.md` (P9)
Note: dichiarazioni del costruttore; il prezzo è quello del giorno.

### livox-mid-360
Tipo: pagina di costruttore o comunicato (rivenditore)
Autori: Livox (pagina di RoboticsCenter); DroneXL per il listino
Titolo: Livox Mid-360 (pagina del rivenditore)
Sede e anno: roboticscenter.ai, letta il 14-11-2026
Identificativo: manca
Link: https://www.roboticscenter.ai/es/store/product/livox-dji-livox-mid-360 ; https://dronexl.co/2026/09/21/livox-mid-360l-lidar-half-point-rate-robots/ (non aperta)
Verifica: verificata dal curatore il 14-11-2026 (rif-1) [r] in parte: pagina aperta; campo 360° × (−7°…52°), cioè 59°; 40 m al 10 % e 70 m all'80 % di riflettività. Dato diverso: nessun prezzo sulla pagina («Contact for pricing»); gli 899–1092 $ non sono verificati.
Usata per: Mid-360: 360°×59°, 40 m (r), 899–1092 $ (r) — `f1/985ccd9bca46/CONSEGNA.md` (tabella, rif. [11]), `f1/985ccd9bca46/PREVISIONI.md` (P9)
Note: pagina di rivenditore, non la scheda Livox. La pagina DroneXL (979 $ di listino) non è stata aperta.

### luxonis-oak-d-pro-w
Tipo: pagina di costruttore o comunicato (rivenditore)
Autori: Luxonis (pagina di Arducam)
Titolo: OAK-D Pro W (pagina del rivenditore; titolo esatto: manca)
Sede e anno: arducam.com; data: manca
Identificativo: manca
Link: https://www.arducam.com/oak-d-pro-w.html
Verifica: non raggiungibile (403 oggi, con lo strumento di lettura e con una richiesta diretta); il ruolo l'ha vista solo nel riassunto di un motore di ricerca.
Usata per: tre OAK-D Pro W, stereo attivo, 127° orizzontali, 499–529 $ l'una — `f1/985ccd9bca46/CONSEGNA.md` (§2, rif. [12])
Note: campo e prezzo non verificati. È l'unico «tre sensori per 360°» geometricamente valido secondo `lidar`: prima di ripeterlo va letta la scheda Luxonis.

### botland-oak-d-lite
Tipo: pagina di costruttore o comunicato (rivenditore)
Autori: Botland
Titolo: OAK-D Lite (pagina del rivenditore; titolo esatto: manca)
Sede e anno: botland.store; data: manca
Identificativo: manca
Link: https://botland.store/modules-smart-cameras/20955-oak-d-lite.html
Verifica: non verificata (non aperta né in f3 né oggi).
Usata per: OAK-D Lite 73°×58°, data fuori produzione da un rivenditore europeo — `f1/985ccd9bca46/PREVISIONI.md` (P6)
Note: citata solo in PREVISIONI.md.

### arducam-tof
Tipo: pagina di costruttore o comunicato
Autori: Arducam
Titolo: Time-of-Flight Camera for Raspberry Pi (titolo esatto: manca)
Sede e anno: arducam.com; data: manca
Identificativo: manca
Link: https://www.arducam.com/product/time-of-flight-camera-for-raspberry-pi/ ; https://www.arducam.com/time-of-flight-camera-for-raspberry-pi.html
Verifica: non raggiungibile (403 oggi); i ruoli l'hanno vista solo nel riassunto di un motore di ricerca.
Usata per: tre camere ToF 240×180 coprono circa 174° (campo dichiarato non verificato) — `f1/dfac83300259/CONSEGNA.md` (§1.1)
Usata per: «Arducam ToF sotto 70° (modello T2: 64°)» fra i 7 sensori di P1 — `f1/b8262bfed263/CONSEGNA.md` (requisiti-1)
Note: campo e risoluzione non verificati: i due usi poggiano su un riassunto di ricerca.

### iec-60825-1
Tipo: norma o documento regolatorio
Autori: International Electrotechnical Commission
Titolo: IEC 60825-1:2014 — Safety of laser products – Part 1: Equipment classification and requirements (titolo a memoria, non verificato oggi)
Sede e anno: IEC, edizione 3.0, 2014
Identificativo: IEC 60825-1:2014
Link: manca (nei file è citata solo attraverso la pagina `unitree-l2`)
Verifica: non verificata (testo della norma a pagamento, non aperto; che la pagina Unitree la citi è verificato oggi [r]).
Usata per: «tutti i sensori citati sono dichiarati classe 1 (ST, C1 FDA, L2 IEC 60825-1:2014; Femto Bolt e RealSense: non verificato)» — `f1/985ccd9bca46/CONSEGNA.md` («Sicurezza ottica»)
Note: citazione indiretta: prova che il costruttore dichiara la classe, non che il prodotto la rispetti. La «classe 1 FDA» rimanda al regolamento statunitense sui laser, che nessun file cita con un identificativo: manca.

---

## 2. Modelli, software, insiemi di dati

### ultralytics-yolo26
Tipo: documentazione di software
Autori: Ultralytics
Titolo: YOLO26 (documentazione dei modelli) e file LICENSE del deposito
Sede e anno: docs.ultralytics.com, letta il 14-11-2026 (in f3)
Identificativo: manca
Link: https://docs.ultralytics.com/models/yolo26/
Verifica: già verificata dal curatore in f3 [g]: YOLO26n a 640 px 38,9 ± 0,7 ms su CPU in ONNX, 1,7 ms su T4, mAP 40,9; AGPL-3.0. Dato diverso: YOLOE-26 40,6 AP su LVIS è della variante x [r]. Non riaperta oggi.
Usata per: «YOLO26n 38,9 ms a 640 px in ONNX (1,7 ms su T4), AGPL-3.0»; «YOLOE-26 40,6 AP su LVIS con testo»; «circa 25 Hz il solo rilevatore» — `f1/c85dbcc51ea6/CONSEGNA.md` (§1.2, visione-1, rif. [2])
Note: la latenza su CPU è quella della macchina di prova di Ultralytics, non del portatile della squadra (P5 non risolta). AGPL-3.0: obblighi da portare all'analista normativo.

### ultralytics-coco-yaml
Tipo: insieme di dati
Autori: Ultralytics (configurazione); COCO è di Lin e altri (articolo non citato nei file: manca)
Titolo: `coco.yaml` — elenco delle 80 classi di COCO
Sede e anno: deposito ultralytics, ramo main, letto il 14-11-2026
Identificativo: manca
Link: https://raw.githubusercontent.com/ultralytics/ultralytics/main/ultralytics/cfg/datasets/coco.yaml
Verifica: verificata dal curatore il 14-11-2026 (rif-1) [g]: file aperto; 80 nomi di classe; nessuno corrisponde a muro, porta, gradino, palo, scatola, carrello, cono (controllo mio sull'elenco: 0 su 7).
Usata per: «muro, porta, gradino, palo, scatola, carrello, cono non sono fra le 80 classi COCO» (P1 di visione: 0 su 7) — `f1/c85dbcc51ea6/CONSEGNA.md` (§1.4, rif. [10])
Note: controllo esaustivo sulle 80 classi e sulle 7 categorie dichiarate; non dice niente su altri insiemi (LVIS, Objects365).

### ultralytics-tracciatori
Tipo: documentazione di software
Autori: Ultralytics
Titolo: Multi-Object Tracking with Ultralytics YOLO (modo «track»); file `bytetrack.yaml` e `default.yaml`
Sede e anno: docs.ultralytics.com e deposito, letti il 14-11-2026 (in f1 e f3)
Identificativo: manca
Link: https://docs.ultralytics.com/modes/track/ ; https://raw.githubusercontent.com/ultralytics/ultralytics/main/ultralytics/cfg/trackers/bytetrack.yaml
Verifica: già verificata dal curatore in f3 [g]: sei tracciatori (BoT-SORT, ByteTrack, OC-SORT, Deep OC-SORT, FastTracker, TrackTrack); `track_buffer: 30` in `bytetrack.yaml`; predefinito `tracker: tracktrack.yaml`; intestazione AGPL-3.0; re-identificazione spenta in partenza [r]. Non riaperta oggi.
Usata per: `track_buffer: 30` come origine della scadenza di 1 s; sei tracciatori, predefinito TrackTrack, re-identificazione spenta; AGPL-3.0 — `f1/992c41c8860e/CONSEGNA.md` (§1.2, §1.3)
Usata per: tracciatore BoT-SORT o ByteTrack, ReID di BoT-SORT — `f1/c85dbcc51ea6/CONSEGNA.md` (visione-1, visione-2, rif. [15])
Note: `track_buffer: 30` è il predefinito di ByteTrack, non del tracciatore che parte senza scelta (`tracktrack.yaml` non letto). Che i tracciatori non espongano covarianza né tracce «previste»: non verificato (lo dichiara il ruolo).

### roboflow-rf-detr
Tipo: deposito di codice
Autori: Roboflow
Titolo: RF-DETR (README del deposito)
Sede e anno: GitHub, letto il 14-11-2026 (in f3)
Identificativo: manca
Link: https://github.com/roboflow/rf-detr
Verifica: già verificata dal curatore in f3 [g], con correzione: Apache 2.0 per il codice e per i modelli N, S, M, L, per la segmentazione e per i punti chiave; i modelli di rilevamento Atto, Femto, Pico, XL e 2XL sono sotto PML 1.0. RF-DETR-N: 2,3 ms su T4 (TensorRT, FP16, lotto 1), AP 48,4. Non riaperta oggi.
Usata per: «RF-DETR-N 2,3 ms su T4, Apache 2.0»; alternativa ad AGPL — `f1/c85dbcc51ea6/CONSEGNA.md` (§1.2, visione-1, rif. [3])
Note: la licenza dipende dalla taglia del modello. Latenza su CPU: non verificata.

### megvii-yolox
Tipo: deposito di codice
Autori: Megvii (Megvii-BaseDetection)
Titolo: YOLOX (file LICENSE del deposito)
Sede e anno: GitHub, ramo main, letto il 14-11-2026
Identificativo: manca
Link: https://github.com/Megvii-BaseDetection/YOLOX ; https://raw.githubusercontent.com/Megvii-BaseDetection/YOLOX/main/LICENSE
Verifica: verificata dal curatore il 14-11-2026 (rif-1) [g]: file LICENSE aperto: «Apache License Version 2.0».
Usata per: «YOLOX è Apache 2.0 (F16, R)» — `f1/3fff79e9c3ea/FONTI.md` (F16), `f1/3fff79e9c3ea/CONSEGNA.md` (ricercatore-1, vincoli)
Note: verificata la licenza del codice; i pesi e gli insiemi di addestramento non controllati.

### rlabbe-filterpy
Tipo: deposito di codice
Autori: Roger R. Labbe Jr
Titolo: FilterPy (file LICENSE del deposito)
Sede e anno: GitHub, ramo master, letto il 14-11-2026
Identificativo: manca
Link: https://raw.githubusercontent.com/rlabbe/filterpy/master/LICENSE
Verifica: verificata dal curatore il 14-11-2026 (rif-1) [g]: «The MIT License (MIT) Copyright (c) 2015 Roger R. Labbe Jr».
Usata per: «licenza MIT (anche filterpy)» in F16 — `f1/3fff79e9c3ea/FONTI.md`
Note: nessuna.

### foundationvision-bytetrack
Tipo: deposito di codice
Autori: FoundationVision (deposito ufficiale di ByteTrack; l'articolo non è citato nei file: manca)
Titolo: ByteTrack (README del deposito)
Sede e anno: GitHub, letto il 14-11-2026 (in f1 e f3)
Identificativo: manca
Link: https://github.com/FoundationVision/ByteTrack
Verifica: già verificata dal curatore in f3 [g]: licenza MIT; «30 FPS running speed on a single V100 GPU» (rilevatore compreso). Aperta anche dal ruolo. Non riaperta oggi.
Usata per: F15: tracciatori classici con licenza MIT; 30 FPS su V100 — `f1/3fff79e9c3ea/FONTI.md`, `f1/3fff79e9c3ea/CONSEGNA.md` (§1.4)
Note: i 30 FPS comprendono il rilevatore e sono su GPU V100: non dicono niente della CPU.

### yang2024
Tipo: articolo scientifico (prestampa) e deposito di codice
Autori: Cheng-Yen Yang, Hsiang-Wei Huang, Wenhao Chai, Zhongyu Jiang, Jenq-Neng Hwang
Titolo: SAMURAI: Adapting Segment Anything Model for Zero-Shot Visual Tracking with Motion-Aware Memory
Sede e anno: arXiv, v1 18-11-2024, v2 30-11-2024; sede a stampa: manca (non trovata su Crossref oggi)
Identificativo: arXiv 2411.11922
Link: https://arxiv.org/abs/2411.11922 ; https://github.com/yangchris11/samurai
Verifica: già verificata dal curatore in f3 [g]: il Kalman sceglie la maschera (testo); Apache-2.0; «The existing code doesn't support live/streaming video». Ricontrollati oggi su arXiv [g] titolo, autori e date.
Usata per: la posizione prevista dal Kalman sceglie la maschera dentro SAM 2 (unica freccia sensata dal Kalman alla rete) — `f1/c85dbcc51ea6/CONSEGNA.md` (§1.1, rif. [1])
Usata per: F19: Apache-2.0; il codice non accetta flussi dal vivo — `f1/3fff79e9c3ea/FONTI.md`, `f1/3fff79e9c3ea/CONSEGNA.md` (§1.5), `f1/3fff79e9c3ea/PREVISIONI.md` (P2b)
Note: prestampa, non rivista fra pari per quanto verificato.

### carion2025
Tipo: articolo scientifico (prestampa)
Autori: Nicolas Carion, Laura Gustafson, Yuan-Ting Hu, Shoubhik Debnath, Ronghang Hu, Didac Suris, Chaitanya Ryali, Kalyan Vasudev Alwala, Haitham Khedr, Andrew Huang, Jie Lei, Tengyu Ma e altri 26 (38 autori su arXiv)
Titolo: SAM 3: Segment Anything with Concepts
Sede e anno: arXiv, v1 20-11-2025, v2 28-3-2026; sede a stampa: manca
Identificativo: arXiv 2511.16719
Link: https://arxiv.org/abs/2511.16719 ; https://arxiv.org/html/2511.16719v2
Verifica: già verificata dal curatore in f3 [g, testo intero]: «30 ms for a single image with 100+ detected objects» su H200; circa 5 oggetti quasi in tempo reale. Ricontrollati oggi su arXiv [g] titolo, numero di autori e date.
Usata per: «SAM 3 30 ms a immagine su H200, video quasi in tempo reale per circa 5 oggetti» — `f1/c85dbcc51ea6/CONSEGNA.md` (§1.2, rif. [4])
Usata per: SAM 3 fuori dall'ipotesi portatile o Jetson (dal riassunto di ricerca) — `f1/992c41c8860e/CONSEGNA.md` (§1.4)
Note: i dati non sono nel riassunto dell'articolo ma nel testo. GPU da centro di calcolo.

### meta-sam3-blog
Tipo: pagina di costruttore o comunicato
Autori: Meta AI
Titolo: Segment Anything Model 3 (blog; aggiornamento su SAM 3.1 del 27-3-2026)
Sede e anno: ai.meta.com, aggiornamento del 27 marzo 2026
Identificativo: manca
Link: https://ai.meta.com/blog/segment-anything-model-3/
Verifica: già verificata dal curatore in f3 [r] soltanto: da 16 a 32 fps su una H100, video con numero medio di oggetti. Non riaperta oggi.
Usata per: «SAM 3.1 32 fps su H100» — `f1/c85dbcc51ea6/CONSEGNA.md` (§1.2, rif. [5])
Note: comunicato del produttore, letto solo attraverso lo strumento che riassume: prova debole.

### ravi2024
Tipo: articolo scientifico (prestampa)
Autori: Nikhila Ravi, Valentin Gabeur, Yuan-Ting Hu, Ronghang Hu, Chaitanya Ryali, Tengyu Ma, Haitham Khedr, Roman Rädle, Chloe Rolland, Laura Gustafson, Eric Mintun, Junting Pan e altri 6 (18 autori su arXiv)
Titolo: SAM 2: Segment Anything in Images and Videos
Sede e anno: arXiv, v1 1-8-2024, v2 28-10-2024; sede a stampa: non controllata
Identificativo: arXiv 2408.00714
Link: https://arxiv.org/abs/2408.00714 ; licenza: https://raw.githubusercontent.com/facebookresearch/sam2/main/LICENSE
Verifica: verificata dal curatore il 14-11-2026 (rif-1) [g]: registro arXiv aperto; nel riassunto «a simple transformer architecture with streaming memory for real-time video processing»; nessun FPS né hardware nel riassunto. Licenza del deposito: «Apache License Version 2.0» [g].
Usata per: F17: «streaming memory for real-time video processing»; licenza segnata [M] non verificata — `f1/3fff79e9c3ea/FONTI.md`; P2(b) «i 30-44 FPS di SAM 2 sono su GPU da datacenter» — `f1/3fff79e9c3ea/PREVISIONI.md`
Note: la licenza [M] di FONTI.md si chiude: Apache 2.0 per il codice. I «30–44 FPS su A100» della previsione P2(b) vengono dalla memoria del ruolo: non verificati (non sono nel riassunto).

### zhou2025
Tipo: articolo scientifico e deposito di codice
Autori: Chong Zhou, Chenchen Zhu, Yunyang Xiong, Saksham Suri, Fanyi Xiao, Lemeng Wu, Raghuraman Krishnamoorthi, Bo Dai, Chen Change Loy, Vikas Chandra, Bilge Soran
Titolo: EdgeTAM: On-Device Track Anything Model
Sede e anno: IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR) 2025, pp. 13832–13842
Identificativo: DOI 10.1109/CVPR52734.2025.01291; arXiv 2501.07256
Link: https://arxiv.org/abs/2501.07256 ; https://github.com/facebookresearch/EdgeTAM
Verifica: già verificata dal curatore in f3: 16 fps su iPhone 15 Pro Max [g]; Apache-2.0 [g]; SAM 2 minimo «around 1 FPS» [g]; 150,9 fps su A100 [r]. Ricontrollati oggi autori (arXiv [g]), pagine e DOI (Crossref [g]).
Usata per: F18: 16 FPS su iPhone 15 Pro Max, 150,9 su A100, Apache 2.0; SAM 2 piccolo circa 1 FPS sullo stesso telefono — `f1/3fff79e9c3ea/FONTI.md`, `f1/3fff79e9c3ea/CONSEGNA.md` (§1.5), `f1/3fff79e9c3ea/PREVISIONI.md` (P2b)
Usata per: «EdgeTAM: 16 fps su iPhone 15 Pro Max» — `f1/c85dbcc51ea6/CONSEGNA.md` (§1.2, rif. [6])
Note: nessuna misura su Jetson o CPU: non verificato (lo dichiarano i ruoli).

### ding2026
Tipo: articolo scientifico (prestampa)
Autori: Zhaoyuan Ding, Yijing Yang, Han Shu, Xinghao Chen
Titolo: TinySAM 2: Extreme Memory Compression for Efficient Track Anything Model
Sede e anno: arXiv, 18-5-2026 (12 pagine, 6 figure); sede a stampa: manca
Identificativo: arXiv 2605.18013
Link: https://arxiv.org/abs/2605.18013 ; https://arxiv.org/html/2605.18013
Verifica: verificata dal curatore il 14-11-2026 (rif-1): titolo e autori [g, arXiv]; testo HTML aperto [r]: «can run in real-time at 25.6 FPS on a single GPU for 1000 image frames from three videos» (§ 4.2); «FPS is measured on a single GPU with 32GB memory» (§ 4.1); in Tabella 1 il valore sta sotto «FPS V100».
Usata per: F21: «TinySAM 2: 25,6 FPS, hardware non identificato» — `f1/3fff79e9c3ea/FONTI.md`
Note: il numero è giusto e l'articolo è questo (dubbio di FONTI.md chiuso); l'hardware è una GPU da centro di calcolo (V100 secondo l'intestazione della tabella), quindi non sposta P2(b). Prestampa.

### hsieh2023
Tipo: articolo scientifico (prestampa) e insieme di dati
Autori: Cheng-Yen Hsieh, Kaihua Chen, Achal Dave, Tarasha Khurana, Deva Ramanan
Titolo: TAO-Amodal: A Benchmark for Tracking Any Object Amodally
Sede e anno: arXiv, v1 19-12-2023, v3 2-4-2024; sede a stampa: non controllata
Identificativo: arXiv 2312.12433
Link: https://arxiv.org/abs/2312.12433
Verifica: già verificata dal curatore in f3 [g]: la frase «…struggle to detect and track objects under heavy occlusion» e i guadagni +2,1 % e +3,3 %. Ricontrollati oggi su arXiv [g] titolo, autori e date.
Usata per: F20: la percezione amodale è acerba; guadagni di 2–3 punti con la messa a punto — `f1/3fff79e9c3ea/FONTI.md`, `f1/3fff79e9c3ea/CONSEGNA.md` (§1.5)
Note: solo riassunto; il titolo citato in FONTI.md («TAO-Amodal») è abbreviato.

### chen2024
Tipo: articolo scientifico
Autori: Kaihua Chen, Deva Ramanan, Tarasha Khurana
Titolo: Using Diffusion Priors for Video Amodal Segmentation
Sede e anno: IEEE/CVF CVPR 2025, pp. 22890–22900 (prestampa arXiv del 5-12-2024)
Identificativo: DOI 10.1109/CVPR52734.2025.02131; arXiv 2412.04623
Link: https://arxiv.org/abs/2412.04623
Verifica: verificata dal curatore il 14-11-2026 (rif-1) [g]: registro arXiv e Crossref aperti; nel riassunto: la segmentazione amodale su video è formulata «as a conditional generation task», sfruttando modelli generativi di video.
Usata per: «lo stato dell'arte amodale su video è generativo (diffusione [12])» — `f1/c85dbcc51ea6/CONSEGNA.md` (§1.6)
Note: `visione` dà solo il link; autori, titolo e sede li ho aggiunti oggi. Che sia «lo stato dell'arte» è un giudizio del ruolo, non verificato; tempi di esecuzione: non verificati.

### zhang2026
Tipo: articolo scientifico (prestampa)
Autori: Bo Zhang, Zhuotao Tian, Xin Tao, Songlin Tang, Jun Yu, Wenjie Pei
Titolo: Amodal SAM: A Unified Amodal Segmentation Framework with Generalization
Sede e anno: arXiv, 22-4-2026; sede a stampa: manca
Identificativo: arXiv 2604.20748
Link: https://arxiv.org/abs/2604.20748
Verifica: verificata dal curatore il 14-11-2026 (rif-1) [g] in parte: registro arXiv aperto; il riassunto dice «leverages SAM (Segment Anything Model) for both amodal image and amodal video segmentation». Dato diverso: «SAM 2» non compare nel riassunto.
Usata per: «…o derivato da SAM 2 [13]; tempi reali: non verificati» — `f1/c85dbcc51ea6/CONSEGNA.md` (§1.6)
Note: scrivere «derivato da SAM», oppure leggere il testo intero per sapere se la parte video usa SAM 2.

### zholus2025
Tipo: articolo scientifico (prestampa)
Autori: Artem Zholus, Carl Doersch, Yi Yang, Skanda Koppula, Viorica Patraucean, Xu Owen He, Ignacio Rocco, Mehdi S. M. Sajjadi, Sarath Chandar, Ross Goroshin
Titolo: TAPNext: Tracking Any Point (TAP) as Next Token Prediction
Sede e anno: arXiv, v1 8-4-2025, v2 14-4-2025; sede a stampa: non controllata
Identificativo: arXiv 2504.05579
Link: https://arxiv.org/abs/2504.05579
Verifica: già verificata dal curatore in f3 [g], con correzione. Dato diverso: la Tabella 2 dà, con 1024 punti, 187 fps su H100 e 42 su V100 (TAPNext-B, latenza 5,33 ms su H100); «348 fps» non è nell'articolo. Ricontrollati oggi su arXiv [g] titolo e autori.
Usata per: «TAPNext: 1024 punti a 348 fps, ma su H100» — `f1/c85dbcc51ea6/CONSEGNA.md` (§1.6, rif. [14])
Note: la conclusione del ruolo (serve una GPU da centro di calcolo) non cambia; la cifra va corretta in 187 fps.

### lin2025
Tipo: articolo scientifico (prestampa)
Autori: Haotong Lin, Sili Chen, Junhao Liew, Donny Y. Chen, Zhenyu Li, Guang Shi, Jiashi Feng, Bingyi Kang
Titolo: Depth Anything 3: Recovering the Visual Space from Any Views
Sede e anno: arXiv, 13-11-2025; sede a stampa: manca
Identificativo: arXiv 2511.10647
Link: https://arxiv.org/abs/2511.10647
Verifica: già verificata dal curatore in f3 nei dati bibliografici. Ricontrollati oggi su arXiv [g] titolo, autori e data. I numeri citati non vengono dall'articolo ma da `gerdsenai-da3-ros2`.
Usata per: ripiego senza camera di profondità: profondità monoculare «Depth Anything 3 small» — `f1/c85dbcc51ea6/CONSEGNA.md` (visione-1)
Note: l'articolo non è citato direttamente da `visione` (che cita il post di comunità): l'ha aggiunto f3.

### gerdsenai-da3-ros2
Tipo: altro (post di comunità su un forum)
Autori: GerdsenAI
Titolo: [Release] GerdsenAI's Depth Anything 3 ROS2 Wrapper with Real-Time TensorRT for Jetson
Sede e anno: forum Open Robotics Discourse, 5 febbraio 2026
Identificativo: discussione 52364
Link: https://discourse.openrobotics.org/t/release-gerdsenais-depth-anything-3-ros2-wrapper-with-real-time-tensorrt-for-jetson/52364
Verifica: già verificata dal curatore in f3 [g], in parte: da 6,35 a 43+ fps su Jetson Orin NX 16 GB; la variante «small» non è nominata nel post. Non riaperta oggi.
Usata per: «Depth Anything 3 small: 6 fps in PyTorch e 43 con TensorRT su Orin NX, dati della comunità» — `f1/c85dbcc51ea6/CONSEGNA.md` (visione-1, rif. [16])
Note: misura di terzi, non indipendente né ripetuta; a quale variante del modello si riferisca non è verificato.

### bewley2016
Tipo: articolo scientifico
Autori: Alex Bewley, Zongyuan Ge, Lionel Ott, Fabio Ramos, Ben Upcroft
Titolo: Simple Online and Realtime Tracking
Sede e anno: IEEE International Conference on Image Processing (ICIP) 2016; pagine: manca (non controllate)
Identificativo: DOI 10.1109/ICIP.2016.7533003; arXiv 1602.00763
Link: https://arxiv.org/abs/1602.00763
Verifica: già verificata dal curatore in f3 [g]: «updates at a rate of 260 Hz». Ricontrollati oggi su arXiv [g]: autori, DOI, «Presented at ICIP 2016», e nel riassunto Kalman più algoritmo ungherese e i 260 Hz.
Usata per: ordine «rilevatore → Kalman e ungherese» e 260 Hz (SORT) — `f1/21d3813ca7e1/CONSEGNA.md` (§1.1)
Note: i 260 Hz sono del solo tracciatore, date le rilevazioni, sull'hardware del 2016.

### cao2023
Tipo: articolo scientifico e deposito di codice
Autori: Jinkun Cao, Jiangmiao Pang, Xinshuo Weng, Rawal Khirodkar, Kris Kitani
Titolo: Observation-Centric SORT: Rethinking SORT for Robust Multi-Object Tracking
Sede e anno: IEEE/CVF CVPR 2023, pp. 9686–9696
Identificativo: DOI 10.1109/CVPR52729.2023.00934; arXiv 2203.14360
Link: https://arxiv.org/abs/2203.14360 ; https://github.com/noahcao/OC_SORT
Verifica: già verificata dal curatore in f3 [g]: errore che si accumula in occlusione, modulo ORU, «700+ FPS on a single CPU», deposito MIT. Ricontrollati oggi: autori e frase «This leads to the accumulation of errors during a period of occlusion» (arXiv [g]); pagine e DOI (Crossref [g]); file LICENSE del deposito «MIT License» [g].
Usata per: F16: errore del Kalman che si accumula in occlusione; ORU; oltre 700 FPS su CPU date le rilevazioni; MIT — `f1/3fff79e9c3ea/FONTI.md`, `f1/3fff79e9c3ea/CONSEGNA.md` (§1.4)
Usata per: «senza misure gli errori del Kalman si accumulano» — `f1/21d3813ca7e1/CONSEGNA.md` (§1.4); «OC-SORT nasce dall'errore che il Kalman accumula in occlusione» — `f1/992c41c8860e/CONSEGNA.md` (§1.3)
Note: il file LICENSE porta «Copyright (c) 2021 Yifu Zhang» (ereditato da ByteTrack): è MIT in ogni caso.

### weng2020
Tipo: articolo scientifico
Autori: Xinshuo Weng, Jianren Wang, David Held, Kris Kitani
Titolo: 3D Multi-Object Tracking: A Baseline and New Evaluation Metrics (riassunto esteso su arXiv: «AB3DMOT: A Baseline for 3D Multi-Object Tracking and New Evaluation Metrics»)
Sede e anno: IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS) 2020, pp. 10359–10366; il riassunto esteso arXiv 2008.08063 è per i Workshop di ECCV 2020
Identificativo: DOI 10.1109/IROS45743.2020.9341164; arXiv 2008.08063 (riassunto esteso)
Link: https://arxiv.org/abs/2008.08063
Verifica: già verificata dal curatore in f3 [g], con correzione di attribuzione. Ricontrollati oggi: riassunto arXiv «a straightforward combination of a 3D Kalman filter and the Hungarian algorithm» [g]; pagine e DOI su Crossref [g].
Usata per: «lo schema da copiare è AB3DMOT, Kalman 3D più ungherese» — `f1/992c41c8860e/CONSEGNA.md` (§1.4)
Note: citare l'articolo IROS, non il riassunto esteso.

### pang2021
Tipo: articolo scientifico
Autori: Ziqi Pang, Zhichao Li, Naiyan Wang
Titolo: SimpleTrack: Understanding and Rethinking 3D Multi-object Tracking
Sede e anno: Computer Vision – ECCV 2022 Workshops, Lecture Notes in Computer Science, Springer, pp. 680–696, 2023 (prestampa arXiv del 18-11-2021)
Identificativo: DOI 10.1007/978-3-031-25056-9_43; arXiv 2111.09621
Link: https://arxiv.org/abs/2111.09621
Verifica: già verificata dal curatore in f3 [g] («life cycle management» come parte a sé; sede non controllata). Completata oggi: sede, pagine e DOI su Crossref [g]; nel riassunto arXiv le quattro parti «pre-processing of detection, association, motion model, and life cycle management» [g].
Usata per: «SimpleTrack isola la gestione della vita delle tracce come modulo a sé» — `f1/992c41c8860e/CONSEGNA.md` (§1.4)
Note: la chiave tiene l'anno della prestampa; l'anno di stampa è 2023.

### sun2022
Tipo: articolo scientifico e insieme di dati
Autori: Peize Sun, Jinkun Cao, Yi Jiang, Zehuan Yuan, Song Bai, Kris Kitani, Ping Luo
Titolo: DanceTrack: Multi-Object Tracking in Uniform Appearance and Diverse Motion
Sede e anno: IEEE/CVF CVPR 2022, pp. 20961–20970
Identificativo: DOI 10.1109/CVPR52688.2022.02032; arXiv 2111.14690
Link: https://arxiv.org/abs/2111.14690
Verifica: verificata dal curatore il 14-11-2026 (rif-1) solo nei dati bibliografici [g] (arXiv e Crossref): esiste con questi autori, titolo e sede. Nessuna cifra è citata da questa fonte.
Usata per: insieme di dati su cui sono valutati i tracciatori appresi di fine corsa («MATR su DanceTrack») — `f1/992c41c8860e/CONSEGNA.md` (§1.4)
Note: licenza dell'insieme di dati non controllata.

### yang2025
Tipo: articolo scientifico (prestampa)
Autori: Xu Yang, Gady Agam
Titolo: Motion-Aware Transformer for Multi-Object Tracking
Sede e anno: arXiv, v1 26-9-2025 (tre versioni); sede a stampa: manca
Identificativo: arXiv 2509.21715
Link: https://arxiv.org/abs/2509.21715
Verifica: verificata dal curatore il 14-11-2026 (rif-1) [g], con riserva: `tracciamento` scrive solo «MATR», senza link; che intendesse questo articolo è un'identificazione mia (ricerca per nome). Registro arXiv aperto: su DanceTrack 71,3 HOTA con dati supplementari, oltre 9 punti sopra MOTR senza dati aggiuntivi.
Usata per: «i tracciatori appresi di fine corsa (es. MATR su DanceTrack) chiedono addestramento: prestazioni attuali non verificate» — `f1/992c41c8860e/CONSEGNA.md` (§1.4)
Note: l'attribuzione va confermata dal ruolo. Che il metodo «chieda addestramento» è coerente col riassunto (modello DETR addestrato), non una frase letta.

### luiten2021
Tipo: articolo scientifico
Autori: Jonathon Luiten, Aljoša Ošep, Patrick Dendorfer, Philip Torr, Andreas Geiger, Laura Leal-Taixé, Bastian Leibe
Titolo: HOTA: A Higher Order Metric for Evaluating Multi-Object Tracking
Sede e anno: International Journal of Computer Vision, vol. 129, pp. 548–578, 2021 (in linea 2020)
Identificativo: DOI 10.1007/s11263-020-01375-2; arXiv 2009.07736
Link: https://arxiv.org/abs/2009.07736
Verifica: già verificata dal curatore in f3 (esiste, con questi autori; volume e pagine). Ricontrollati oggi su arXiv [g]: autori, DOI, rivista. Volume e pagine: da f3, non riletti oggi (Crossref ha risposto 429).
Usata per: «HOTA e IDF1 chiedono sequenze annotate: non sono la misura giusta per la demo» — `f1/992c41c8860e/CONSEGNA.md` (§1.7)
Note: che HOTA chieda annotazioni è implicito nella definizione; la frase non è stata letta nel testo.

### luiten-trackeval
Tipo: deposito di codice
Autori: Jonathon Luiten e collaboratori
Titolo: TrackEval — HOTA (and other) evaluation metrics for Multi-Object Tracking (MOT)
Sede e anno: GitHub, letto il 14-11-2026
Identificativo: manca
Link: https://github.com/JonathonLuiten/TrackEval
Verifica: verificata dal curatore il 14-11-2026 (rif-1) [r]: pagina aperta; licenza MIT; metriche HOTA, CLEAR MOT, Identity (IDF1, IDP, IDR) e altre; la valutazione confronta l'uscita del tracciatore con dati di riferimento in `data/gt/`.
Usata per: strumento di calcolo di HOTA e IDF1, che chiede sequenze annotate — `f1/992c41c8860e/CONSEGNA.md` (§1.7)
Note: la necessità delle annotazioni è dedotta dalla struttura dei dati, non da una frase esplicita.

### schoeller2020
Tipo: articolo scientifico
Autori: Christoph Schöller, Vincent Aravantinos, Florian Lay, Alois Knoll
Titolo: What the Constant Velocity Model Can Teach Us About Pedestrian Motion Prediction
Sede e anno: IEEE Robotics and Automation Letters, vol. 5(2), pp. 1696–1703, aprile 2020 (presentato a ICRA 2020)
Identificativo: DOI 10.1109/LRA.2020.2969925; arXiv 1903.07933
Link: https://arxiv.org/abs/1903.07933
Verifica: già verificata dal curatore in f3 [g]: Tabella I a 4,8 s (ADE/FDE in metri): velocità costante 0,39/0,83; RED 0,44/0,91; SR-LSTM 0,45/0,94; S-GAN 0,32/0,60. Ricontrollati oggi autori e commento di accettazione (arXiv [g]), volume, pagine e DOI (Crossref [g]).
Usata per: F14: velocità costante 0,39/0,83 m contro 0,44/0,91 del miglior appreso deterministico e 0,32/0,60 di S-GAN a 20 campioni, media ETH/UCY a 4,8 s — `f1/3fff79e9c3ea/FONTI.md`, `f1/3fff79e9c3ea/CONSEGNA.md` (§1.4, ricercatore-2, §3), `f1/3fff79e9c3ea/PREVISIONI.md` (P2a: anche LSTM 0,99/2,08, SoPhie 0,54/1,15, velocità costante con campionamento 0,28/0,56)
Note: camere fisse dall'alto, insiemi ETH/UCY (citati solo per nome: nessun riferimento nei file), lavoro del 2020: non dice niente della camera indossata. I valori LSTM, SoPhie e «con campionamento» non sono nell'elenco verificato da f3: aperti dal ruolo, non riletti dal curatore.

### kuzucu2024
Tipo: articolo scientifico
Autori: Selim Kuzucu, Kemal Oksuz, Jonathan Sadeghi, Puneet K. Dokania
Titolo: On Calibration of Object Detectors: Pitfalls, Evaluation and Baselines
Sede e anno: Computer Vision – ECCV 2024, Lecture Notes in Computer Science, Springer, pp. 185–204 (in linea 26-10-2024)
Identificativo: DOI 10.1007/978-3-031-72664-4_11; arXiv 2405.20459
Link: https://arxiv.org/abs/2405.20459
Verifica: già verificata dal curatore in f3 [g]: «much more powerful and effective than the recent train-time calibration methods»; «more than 7 D-ECE». Ricontrollati oggi autori (arXiv [g]), pagine e DOI (Crossref [g]).
Usata per: F22: Platt e regressione isotonica battono i metodi d'addestramento recenti (oltre 7 punti di D-ECE su COCO, D-DETR contro Cal-DETR) — `f1/3fff79e9c3ea/FONTI.md`, `f1/3fff79e9c3ea/CONSEGNA.md` (§1.6)
Note: vale per rilevatori su COCO; che «si può fare in poche ore» è un giudizio del ruolo.

### munir2023
Tipo: articolo scientifico
Autori: Muhammad Akhtar Munir, Muhammad Haris Khan, Salman Khan, Fahad Shahbaz Khan
Titolo: Bridging Precision and Confidence: A Train-Time Loss for Calibrating Object Detection
Sede e anno: IEEE/CVF CVPR 2023, pp. 11474–11483
Identificativo: DOI 10.1109/CVPR52729.2023.01104; arXiv 2303.14404
Link: https://openaccess.thecvf.com/content/CVPR2023/papers/Munir_Bridging_Precision_and_Confidence_A_Train-Time_Loss_for_Calibrating_Object_CVPR_2023_paper.pdf (403 oggi) ; https://arxiv.org/abs/2303.14404
Verifica: verificata dal curatore il 14-11-2026 (rif-1) [g]: dati bibliografici su arXiv e Crossref; nel PDF arXiv: «Post-hoc calibration methods are simple and effective, however, they require hold-out validation data, and are dependent on architecture [25]».
Usata per: F23: i metodi a posteriori chiedono dati di validazione messi da parte e dipendono dall'architettura — `f1/3fff79e9c3ea/FONTI.md`, `f1/3fff79e9c3ea/CONSEGNA.md` (§1.6)
Note: in f3 erano verificati solo i dati bibliografici; oggi anche la frase. La frase è nella versione arXiv; quella CVF non è stata aperta (403).

### timans2024
Tipo: articolo scientifico
Autori: Alexander Timans, Christoph-Nikolas Straehle, Kaspar Sakmann, Eric Nalisnick
Titolo: Adaptive Bounding Box Uncertainties via Two-Step Conformal Prediction
Sede e anno: Computer Vision – ECCV 2024, Lecture Notes in Computer Science, Springer, pp. 363–398 (in linea 8-11-2024)
Identificativo: DOI 10.1007/978-3-031-73223-2_21; arXiv 2403.07263
Link: https://arxiv.org/pdf/2403.07263
Verifica: verificata dal curatore il 14-11-2026 (rif-1) [g]: arXiv e Crossref; nel riassunto «a novel two-step conformal approach that propagates uncertainty in predicted class labels into the uncertainty intervals of bounding boxes».
Usata per: F24: previsione conforme a due passi per i riquadri di rilevamento — `f1/3fff79e9c3ea/FONTI.md`
Note: citata come pista, senza cifre. In f3: solo dati bibliografici.

### lee2026
Tipo: articolo scientifico
Autori: Sungjae Lee, Junhan Jeong, Yeonjoo Hong, Kwang In Kim
Titolo: Physically Guided Visual Mass Estimation from a Single RGB Image
Sede e anno: IJCAI 2026 (Main Track), secondo il commento arXiv; arXiv v1 28-1-2026, v2 5-5-2026; pagine degli atti: manca
Identificativo: arXiv 2601.20303
Link: https://arxiv.org/abs/2601.20303 ; https://arxiv.org/html/2601.20303v1
Verifica: già verificata dal curatore in f3 [r]: APE su image2mass 0,665 (loro) e 1,066 (image2mass); su ABO-500 0,980 contro 0,976. Dato diverso: «fattore medio 1,68» non è nell'articolo, è exp(0,519) dell'ALDE di Tabella 1, calcolato dal ricercatore. Ricontrollati oggi su arXiv [g]: autori e «Accepted to IJCAI 2026 (Main Track)».
Usata per: F29: errore percentuale medio 0,665 e fattore medio 1,68; riferimento del 2017 a 1,066; su un secondo insieme entrambi a 0,98; «la massa non è osservabile» — `f1/3fff79e9c3ea/FONTI.md`, `f1/3fff79e9c3ea/CONSEGNA.md` (§1.3, §3), `f1/3fff79e9c3ea/PREVISIONI.md` (P3: ALDE 0,655 e 0,519)
Note: oggetti da catalogo; il ruolo ha letto la v1, oggi esiste la v2 (non confrontate). 1,68 va dichiarato come derivato.

### standley2017
Tipo: articolo scientifico
Autori: Trevor Standley, Ozan Sener, Dawn Chen, Silvio Savarese
Titolo: image2mass: Estimating the Mass of an Object from Its Image
Sede e anno: Proceedings of the 1st Annual Conference on Robot Learning (CoRL), Proceedings of Machine Learning Research, vol. 78, pp. 324–333, 2017
Identificativo: PMLR v78 (standley17a); DOI: manca
Link: https://proceedings.mlr.press/v78/standley17a.html
Verifica: verificata dal curatore il 14-11-2026 (rif-1): dati bibliografici dalla pagina PMLR [r]; nel PDF [g]: «We obtain the product information for ∼3 million Amazon…» e «…we produce a dataset with ∼150k products that have highly accurate mass and size information».
Usata per: F30: image2mass, circa 150 000 prodotti Amazon (articolo non aperto dal ruolo) — `f1/3fff79e9c3ea/FONTI.md`; riferimento del 2017 per la massa — `f1/3fff79e9c3ea/CONSEGNA.md` (§1.3)
Note: nei file mancavano autori, titolo e sede. L'errore 1,066 attribuito a image2mass viene da `lee2026` (Tabella 1), non da questo articolo.

---

## 3. Ausili per la mobilità e feedback

### kozlov2026
Tipo: articolo scientifico (prestampa; lavori in corso)
Autori: Timofei Kozlov, Artem Trandofilov, Georgii Gazaryan, Issatay Tokmurziyev, Miguel Altamirano Cabrera, Dzmitry Tsetserukou
Titolo: GuideTouch: An Obstacle Avoidance Device with Tactile Feedback for Visually Impaired
Sede e anno: accettato fra i Late-Breaking Reports di HRI 2026 (commento arXiv); arXiv v1 20-1-2026, v2 21-1-2026; pagine: manca
Identificativo: arXiv 2601.13813
Link: https://arxiv.org/abs/2601.13813 ; https://arxiv.org/html/2601.13813
Verifica: già verificata dal curatore in f3 sul riassunto. Completata oggi: autori e sede (arXiv [g]); testo HTML aperto [r]: «we interviewed 28 visually impaired participants (17 male, 11 female, aged 16–60)»; sostituire il bastone «which our user study indicates is highly undesirable»; 92,9 % per i motivi primari su 22 partecipanti senza disabilità visiva; 93,75 % con 14 utenti con disabilità visiva (§ 3.4: 93,7 %).
Usata per: F6: due ToF in verticale, quattro attuatori; 92,9 % (22 partecipanti), 93,75 % (14 utenti con disabilità visiva); 28 intervistati; sostituire il bastone è «highly undesirable» — `f1/3fff79e9c3ea/FONTI.md`, `f1/3fff79e9c3ea/CONSEGNA.md` (§1.7, §3)
Note: lavoro preliminare, campioni piccoli (14 e 22). Non confondere i due gruppi.

### martinez2014
Tipo: articolo scientifico
Autori: Manuel Martinez, Angela Constantinescu, Boris Schauerte, Daniel Koester, Rainer Stiefelhagen
Titolo: Cognitive Evaluation of Haptic and Audio Feedback in Short Range Navigation Tasks
Sede e anno: Computers Helping People with Special Needs (ICCHP 2014), Lecture Notes in Computer Science, Springer, pp. 128–135, 2014
Identificativo: DOI 10.1007/978-3-319-08599-9_20
Link: https://doi.org/10.1007/978-3-319-08599-9_20 (il PDF https://cvhci.iar.kit.edu/~dkoester/publications/martinezICCHP2014tlx.pdf dà 404)
Verifica: già verificata dal curatore in f3 [g, sul riassunto Springer]: «22 times higher cognitive load»; «not found on blindfolded users». Ricontrollati oggi su Crossref [g]: titolo, autori, pagine, anno.
Usata per: F7: per chi usa il bastone il feedback sonoro dà un carico NASA-TLX 22 volte maggiore dell'aptico; l'effetto non c'è nei vedenti bendati — `f1/3fff79e9c3ea/FONTI.md`, `f1/3fff79e9c3ea/CONSEGNA.md` (§1.7, §3)
Note: letto il solo riassunto, non il testo; la numerosità del campione non è stata letta: manca.

### lupu2020
Tipo: articolo scientifico
Autori: Robert-Gabriel Lupu, Oana Mitruț, Andrei Stan, Florina Ungureanu, Kyriaki Kalimeri, Alin Moldoveanu
Titolo: Cognitive and Affective Assessment of Navigation and Mobility Tasks for the Visually Impaired via Electroencephalography and Behavioral Signals
Sede e anno: Sensors, vol. 20(20), articolo 5821, 2020 (15-10-2020)
Identificativo: DOI 10.3390/s20205821; PMC7602506
Link: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7602506/
Verifica: già verificata dal curatore in f3 [r]. Rafforzata oggi [g] sul riassunto registrato in Crossref: «eight visually impaired subjects»; «the haptic stimuli were less intuitive than the audio ones»; la navigazione col dispositivo «increased cognitive load and working memory».
Usata per: F8: 8 partecipanti ciechi; stimoli aptici meno intuitivi di quelli sonori; il dispositivo aumenta il carico cognitivo — `f1/3fff79e9c3ea/FONTI.md`, `f1/3fff79e9c3ea/CONSEGNA.md` (§1.7, §3)
Note: il riassunto dice «visually impaired», non «ciechi»; otto soggetti.

### romlay2021
Tipo: articolo scientifico (rassegna)
Autori: Muhammad Rabani Mohd Romlay, Siti Fauziah Toha, Azhar Mohd Ibrahim, Ibrahim Venkat
Titolo: Methodologies and evaluation of electronic travel aids for the visually impaired people: a review
Sede e anno: Bulletin of Electrical Engineering and Informatics, vol. 10(3), pp. 1747–1758, giugno 2021
Identificativo: DOI 10.11591/eei.v10i3.3055
Link: https://beei.org/index.php/EEI/article/view/3055
Verifica: già verificata dal curatore in f3 [r] (anno non letto). Completata oggi [g] su Crossref: anno, pagine, e nel riassunto «From 70 selected research articles, 51.4% accounts for simulation evaluation, 24.3% involve blindfolded-sighted humans, 22.9% involve visually impaired people and only 1.4% makes it into production and commercialization».
Usata per: F9: rassegna di 70 articoli; valutazioni con persone con disabilità visiva solo nel 22,9 %; l'1,4 % arriva alla produzione — `f1/3fff79e9c3ea/FONTI.md`, `f1/3fff79e9c3ea/CONSEGNA.md` (§1.7)
Note: nessuna.

### xu2023
Tipo: articolo scientifico (rassegna sistematica)
Autori: Peijie Xu, Gerard A. Kennedy, Fei-Yi Zhao, Wen-Jing Zhang, Ron Van Schyndel
Titolo: Wearable Obstacle Avoidance Electronic Travel Aids for Blind and Visually Impaired Individuals: A Systematic Review
Sede e anno: IEEE Access, vol. 11, pp. 66587–66613, 2023
Identificativo: DOI 10.1109/ACCESS.2023.3285396
Link: https://doaj.org/article/69f50f5aa56e4c9fb3f54d8d3d05cf83 (403 allo strumento di lettura; letto il registro DOAJ)
Verifica: verificata dal curatore il 14-11-2026 (rif-1) [g]: Crossref e registro DOAJ aperti; nel riassunto «The PRISMA 2020 and APISSER guidelines were followed», «Eighty-nine studies were included for analysis», «According to user experience, the efficacy and safety of the device was usually their primary concern».
Usata per: F10: rassegna PRISMA di 89 studi; efficacia e sicurezza sono la prima preoccupazione degli utenti — `f1/3fff79e9c3ea/FONTI.md`
Note: in f3 non controllata. Letto il riassunto, non il testo.

### giudice2008
Tipo: articolo scientifico (atti di conferenza)
Autori: Nicholas A. Giudice, James R. Marston, Roberta L. Klatzky, Jack M. Loomis, Reginald G. Golledge
Titolo: Environmental learning without vision: Effects of cognitive load on interface design
Sede e anno: Proceedings of the 9th International Conference on Low Vision (Vision 2008), Montréal, 2008; pagine: manca
Identificativo: manca
Link: https://umaine.edu/vemi/publication/environmental-learning-without-vision-effects-cognitive-load-interface-design
Verifica: verificata dal curatore il 14-11-2026 (rif-1) [r]: pagina aperta; nel riassunto «the secondary task had no effect on cognitive map performance for guidance by spatialized audio» ma «led to significantly worse homing errors for guidance by spatial language»; «Blindfolded participants».
Usata per: F11: la guida con suono spazializzato regge un compito secondario meglio del linguaggio spaziale (vedenti bendati) — `f1/3fff79e9c3ea/FONTI.md`
Note: il riassunto dice «blindfolded», non dice che fossero vedenti: «vedenti bendati» è non verificato su questa fonte. Pagina dell'istituto dell'autore, non degli atti.

### klatzky2006
Tipo: articolo scientifico
Autori: Roberta L. Klatzky, James R. Marston, Nicholas A. Giudice, Reginald G. Golledge, Jack M. Loomis
Titolo: Cognitive load of navigating without vision when guided by virtual sound versus spatial language
Sede e anno: Journal of Experimental Psychology: Applied, vol. 12(4), pp. 223–232, dicembre 2006
Identificativo: DOI 10.1037/1076-898X.12.4.223
Link: https://doi.org/10.1037/1076-898X.12.4.223
Verifica: verificata dal curatore il 14-11-2026 (rif-1) solo nei dati bibliografici [g] (Crossref): esiste con questi autori, titolo e sede. Il contenuto non è stato letto.
Usata per: F11 («Giudice et al. 2008 / Klatzky et al. 2006»): stessa affermazione di `giudice2008` — `f1/3fff79e9c3ea/FONTI.md`
Note: in FONTI.md è citato solo per nome e anno; titolo e sede li ho trovati oggi cercando per titolo. L'affermazione è verificata su `giudice2008`, non qui.

### gulf-times-ally-solos
Tipo: altro (articolo di stampa, fonte secondaria)
Autori: manca (nessuna firma né agenzia sulla pagina)
Titolo: Smart glasses and AI advances find purpose among blind users
Sede e anno: Gulf Times, rubrica Viewpoint, 9 gennaio 2026
Identificativo: articolo 718327
Link: https://www.gulf-times.com/article/718327/opinion/smart-glasses-and-ai-advances-find-purpose-among-blind-users
Verifica: verificata dal curatore il 14-11-2026 (rif-1) [r], con correzione: pagina aperta; c'è «We don't really recommend people use smart glasses as a primary navigation tool» (amministratore delegato di Envision). Dato diverso: l'articolo non dice dove avviene l'elaborazione (né telefono né servizi remoti); dice solo che Envision usa più modelli, fra cui uno di OpenAI.
Usata per: F12: occhiali Ally Solos: elaborazione su telefono e servizi remoti; gli sviluppatori sconsigliano di usarli come strumento principale di navigazione — `f1/3fff79e9c3ea/FONTI.md`
Note: la prima metà dell'affermazione non è sostenuta da questa fonte: toglierla o trovare la documentazione del prodotto. Stampa generalista.

### dossantos2025
Tipo: articolo scientifico
Autori: A. D. P. Dos Santos, M. Loureiro, F. Machado, A. Frizera, F. O. Medola (forma di PubMed: «Dos Santos ADP, Loureiro M, Machado F, Frizera A, Medola FO»)
Titolo: NavWear: design and evaluation of a wearable device for obstacle detection for blind and visually impaired people
Sede e anno: Disability and Rehabilitation: Assistive Technology, vol. 20(6), pp. 1800–1814, agosto 2025 (in linea 18-3-2025)
Identificativo: DOI 10.1080/17483107.2025.2477681; PMID 40100749
Link: https://pubmed.ncbi.nlm.nih.gov/40100749/
Verifica: verificata dal curatore il 14-11-2026 (rif-1) [g]: registro PubMed aperto (servizio E-utilities); nel riassunto «The system is based on an RGB-D camera and haptic feedback, integrated into a backpack»; «Ten blindfolded participants».
Usata per: F13: NavWear 2025 (RGB-D + aptico, zaino), citato dalla bozza — `f1/3fff79e9c3ea/FONTI.md`
Note: i nomi propri per esteso degli autori non sono nel registro letto (solo iniziali): manca. La prova è con dieci partecipanti bendati, non con persone con disabilità visiva.

---

## 4. Monitoraggio industriale, norme e brevetti

### plastropoulos2026
Tipo: articolo scientifico
Autori: A. Plastropoulos, N. P. Avdelidis, A. Zolotas
Titolo: Techno-economic analysis for smart hangar inspection operations through sensing and localisation at scale
Sede e anno: The Aeronautical Journal, vol. 130, n. 1346, pp. 1037–1067, aprile 2026 (in linea 22-12-2025)
Identificativo: DOI 10.1017/aer.2025.10116
Link: https://www.cambridge.org/core/product/288076BC0C6F624BBBBD0A752587762E/core-reader
Verifica: verificata dal curatore il 14-11-2026 (rif-1): dati bibliografici su Crossref [g]; pagina dell'articolo aperta [r, primi 100 000 caratteri]: «no studies have presented a holistic side-by-side evaluation of MoCap, UWB and vision-based solutions»; «little empirical evidence on their robustness to the full spectrum of hangar-specific challenges such as dynamic occlusion».
Usata per: F25: negli hangar manca un confronto fra soluzioni e manca evidenza sulla robustezza all'occlusione dinamica — `f1/3fff79e9c3ea/FONTI.md`, `f1/3fff79e9c3ea/CONSEGNA.md` (§1.8)
Note: riguarda la localizzazione in hangar, non il monitoraggio di persone: il trasferimento è del ruolo. Pagine aggiunte oggi.

### adamides2025
Tipo: articolo scientifico (rassegna)
Autori: Odysseus Adamides, Karthik Subramanian, Sarthak Arora, Ferat Sahin
Titolo: Perception and Computation for Speed and Separation Monitoring Architectures
Sede e anno: Robotics (MDPI), vol. 14(4), articolo 41, 2025 (31-3-2025)
Identificativo: DOI 10.3390/robotics14040041
Link: https://mdpi.com/2218-6581/14/4/41
Verifica: verificata dal curatore il 14-11-2026 (rif-1) solo nei dati bibliografici [g] (Crossref e Semantic Scholar): esiste con questi autori e questo titolo. L'affermazione citata non è nel riassunto; il testo intero non è raggiungibile (403): affermazione non verificata.
Usata per: F26: nella sorveglianza di velocità e separazione (ISO/TS 15066) la distanza protettiva si calcola con l'incertezza di misura e la latenza — `f1/3fff79e9c3ea/FONTI.md`, `f1/3fff79e9c3ea/CONSEGNA.md` (§1.8)
Note: il riassunto parla di architetture di percezione per la sorveglianza di velocità e separazione, non della formula. Che la formula della norma contenga termini di incertezza di posizione e di tempo di reazione lo ricordo a memoria: non verificato oggi.

### iso-ts-15066
Tipo: norma o documento regolatorio
Autori: International Organization for Standardization
Titolo: ISO/TS 15066 — Robots and robotic devices — Collaborative robots (titolo ed edizione a memoria: non verificati oggi)
Sede e anno: ISO; edizione: manca nei file
Identificativo: ISO/TS 15066
Link: manca
Verifica: non verificata (testo a pagamento, non aperto; citata nei file solo attraverso F26).
Usata per: F26: distanza protettiva con incertezza di misura e latenza — `f1/3fff79e9c3ea/FONTI.md`, `f1/3fff79e9c3ea/CONSEGNA.md` (§1.8)
Note: citazione indiretta. Se l'affermazione entra nel documento finale va letta la norma, non la rassegna.

### us-brevetto-11846916
Tipo: norma o documento regolatorio (brevetto)
Autori: Scott Denenberg, Clara Vu, Patrick Sobalvarro, Lev Persits, Ilya A. Kriveshko, Elliot Simon, Alberto Moel, Patrick J. Foy, Justin Bronder (inventori); titolare originario Veo Robotics, Inc.
Titolo: System architecture for safety applications
Sede e anno: brevetto degli Stati Uniti US 11846916 B2, depositato il 22-11-2022, concesso il 19-12-2023
Identificativo: US 11846916 B2
Link: https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11846916 ; letto su https://patents.google.com/patent/US11846916B2/en
Verifica: verificata dal curatore il 14-11-2026 (rif-1) [r]: pagina di Google Patents aperta (primi 100 000 caratteri); nel sommario e nelle rivendicazioni 6 e 22: «marking as occupied the volumes corresponding to a terminus of the ray path, and marking as unknown any volumes beyond the occlusion along the ray path»; volumi occupati, non occupati o sconosciuti.
Usata per: F27: voxel occupati, non occupati o sconosciuti oltre un'occlusione («tre stati per i voxel») — `f1/3fff79e9c3ea/FONTI.md`, `f1/3fff79e9c3ea/CONSEGNA.md` (§1.8)
Note: è una rivendicazione di brevetto, non un metodo validato (lo dice già FONTI.md). Possibili vincoli di proprietà intellettuale sull'idea dei tre stati in ambito industriale: da portare all'analista normativo. Il PDF dell'ufficio brevetti non è stato aperto.

### shan2025
Tipo: articolo scientifico (rassegna)
Autori: Jingfeng Shan, Lapo Miccinesi, Alessandra Beni, Lorenzo Pagnini, Andrea Cioncolini, Massimiliano Pieraccini
Titolo: A Review of Foreign Object Debris Detection on Airport Runways: Sensors and Algorithms
Sede e anno: Remote Sensing (MDPI), vol. 17(2), articolo 225, 2025 (9-1-2025)
Identificativo: DOI 10.3390/rs17020225
Link: https://www.mdpi.com/2072-4292/17/2/225/htm
Verifica: verificata dal curatore il 14-11-2026 (rif-1) [g]: Crossref aperto; nel riassunto «challenges such as limited datasets and high computational demands persist». La pagina MDPI dà 403.
Usata per: F28: rilevamento di detriti sulle piste: pochi dati, calcolo pesante — `f1/3fff79e9c3ea/FONTI.md`
Note: la frase riguarda gli approcci con intelligenza artificiale, non tutti i metodi. Citata in FONTI.md ma non usata nella consegna.

### us-49cfr-236-205
Tipo: norma o documento regolatorio
Autori: Stati Uniti, Federal Railroad Administration
Titolo: 49 CFR § 236.205 — Signal control circuits; requirements
Sede e anno: Code of Federal Regulations, titolo 49, parte 236; 33 FR 19684 (25-12-1968), modificato da 49 FR 3385 (26-1-1984)
Identificativo: 49 CFR 236.205
Link: citato come https://www.customsmobile.com/regulations/49/236.205 (non aperto); letto su https://www.law.cornell.edu/cfr/text/49/236.205 (ecfr.gov reindirizza a un controllo anti-automa)
Verifica: verificata dal curatore il 14-11-2026 (rif-1) [r]: pagina del Legal Information Institute aperta; il segnale che governa l'ingresso in un blocco deve mostrare l'aspetto più restrittivo quando, fra l'altro, il relè di binario è diseccitato o il circuito di comando del segnale è senza energia.
Usata per: analogia di creativo-1: il relè di binario diseccitato dà l'aspetto più restrittivo; il «via libera» esiste solo finché arriva energia — `f1/e30f9e2dd4d7/CONSEGNA.md`
Note: il testo regolatorio sostiene l'analogia; «il via libera esiste solo finché arriva energia» è la lettura del ruolo. Copia non ufficiale del testo (l'edizione ufficiale non è stata raggiunta).

---

## 5. Previsione insiemistica, mappe di occupazione, altro

### koschi2021
Tipo: articolo scientifico
Autori: Markus Koschi, Matthias Althoff
Titolo: Set-Based Prediction of Traffic Participants Considering Occlusions and Traffic Rules
Sede e anno: IEEE Transactions on Intelligent Vehicles, vol. 6(2), pp. 249–265, giugno 2021 (in linea 2020)
Identificativo: DOI 10.1109/TIV.2020.3017385
Link: https://mediatum.ub.tum.de/1575358 (respinge i lettori automatici)
Verifica: già verificata dal curatore in f3, con correzione dell'anno (testo non letto). Ricontrollati oggi: volume, pagine e data su Crossref [g]; riassunto su Semantic Scholar [g]: «a formal set-based prediction that contains all acceptable future behaviors of both detected and potentially hidden traffic participants», con analisi di raggiungibilità per veicoli, pedoni e ciclisti.
Usata per: fonte di rovesciatore-2 (insieme raggiungibile v_max·τ per chi è nascosto), dichiarata «testi non riletti» — `f1/8f275a60e807/CONSEGNA.md`
Note: dato diverso: «IEEE T-IV 2020» va scritto 2021. Il trasferimento da veicoli a pedoni e ausili è del ruolo («non verificato»); il riassunto nomina però anche i pedoni.

### orzechowski2018
Tipo: articolo scientifico
Autori: Piotr Franciszek Orzechowski, Annika Meyer, Martin Lauer
Titolo: Tackling Occlusions & Limited Sensor Range with Set-based Safety Verification
Sede e anno: 21st International Conference on Intelligent Transportation Systems (ITSC) 2018, pp. 1729–1736
Identificativo: DOI 10.1109/ITSC.2018.8569332; arXiv 1807.01262
Link: https://arxiv.org/pdf/1807.01262
Verifica: già verificata dal curatore in f3 [g]: ostacoli nascosti sovrastimati con intervalli di stato. Ricontrollati oggi autori e sede (arXiv [g]), pagine e DOI (Crossref [g]).
Usata per: fonte di rovesciatore-2 (verifica di sicurezza insiemistica sotto occlusione) — `f1/8f275a60e807/CONSEGNA.md`
Note: ambito: guida automatica.

### nuss2018
Tipo: articolo scientifico
Autori: Dominik Nuss, Stephan Reuter, Markus Thom, Ting Yuan, Gunther Krehl, Michael Maile, Axel Gern, Klaus Dietmayer
Titolo: A random finite set approach for dynamic occupancy grid maps with real-time application
Sede e anno: The International Journal of Robotics Research, vol. 37(8), pp. 841–866, luglio 2018
Identificativo: DOI 10.1177/0278364918775523; arXiv 1605.02406
Link: https://arxiv.org/abs/1605.02406
Verifica: già verificata dal curatore in f3 [g]: «highly efficient parallel particle filter». Ricontrollati oggi autori (arXiv [g]), volume, pagine e riassunto (Crossref [g]).
Usata per: griglia dinamica con velocità per cella: filtro a particelle in parallelo, «troppo per un hackathon» — `f1/dfac83300259/CONSEGNA.md` (§1.6)
Note: «troppo per un hackathon» è un giudizio del ruolo.

### hornung2013
Tipo: articolo scientifico
Autori: Armin Hornung, Kai M. Wurm, Maren Bennewitz, Cyrill Stachniss, Wolfram Burgard
Titolo: OctoMap: an efficient probabilistic 3D mapping framework based on octrees
Sede e anno: Autonomous Robots, vol. 34(3), pp. 189–206, aprile 2013 (in linea 7-2-2013)
Identificativo: DOI 10.1007/s10514-012-9321-0
Link: https://www.hrl.uni-bonn.de/papers/hornung13auro-preprint.pdf (dà una pagina, non il PDF)
Verifica: già verificata dal curatore in f3 solo nei dati bibliografici. Ricontrollati oggi su Crossref [g] (numero del fascicolo aggiunto). Testo NON letto: Springer reindirizza a un accesso, la copia degli autori ha restituito una pagina HTML e non il PDF.
Usata per: voxel e octree «distinguono libero, occupato e ignoto, ma con raggi in 3D e ipotesi di mondo statico» — `f1/dfac83300259/CONSEGNA.md` (§1.6)
Note: l'affermazione sul contenuto non è verificata sul testo (il ruolo l'aveva dal riassunto di ricerca). Rilevante per l'estensione f7 (mappa voxel 3D): va letta prima di citarla lì.

### moras2011
Tipo: articolo scientifico
Autori: Julien Moras, Véronique Cherfaoui, Philippe Bonnifait
Titolo: Credibilist Occupancy Grids for Vehicle Perception in Dynamic Environments
Sede e anno: IEEE International Conference on Robotics and Automation (ICRA) 2011, pp. 84–89
Identificativo: DOI 10.1109/ICRA.2011.5980298; HAL hal-00615303
Link: https://hal.archives-ouvertes.fr/hal-00615303
Verifica: già verificata dal curatore in f3 solo nei dati bibliografici. Completata oggi [g]: pagine e DOI (Crossref); riassunto dal registro HAL: «uncertainty arises from ignorance and errors… A credibilist approach is used to model the sensor information and to do a global fusion with the world-fixed map».
Usata per: griglie evidenziali: «l'idea giusta (l'ignoranza ha una sua massa)» — `f1/dfac83300259/CONSEGNA.md` (§1.6)
Note: il riassunto conferma che l'ignoranza è trattata come sorgente d'incertezza a sé; la formulazione «ha una sua massa» (funzioni di credenza) è coerente ma non letta nel testo.

### bogoslavskyi2016
Tipo: articolo scientifico e deposito di codice
Autori: Igor Bogoslavskyi, Cyrill Stachniss
Titolo: Fast range image-based segmentation of sparse 3D laser scans for online operation
Sede e anno: IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS) 2016, pp. 163–169
Identificativo: DOI 10.1109/IROS.2016.7759050
Link: https://github.com/PRBonn/depth_clustering
Verifica: verificata dal curatore il 14-11-2026 (rif-1): deposito aperto [r]: «Fast and robust clustering of point clouds generated with a Velodyne sensor», licenza MIT, articolo da citare; pagine e DOI su Crossref [g].
Usata per: raggruppamento per componenti connesse sulle celle occupate, «stesso principio» di un metodo nato per LiDAR rotanti (trasferimento alle camere di profondità non verificato) — `f1/dfac83300259/CONSEGNA.md` (§4.3)
Note: il README cita anche un secondo articolo degli stessi autori (PFG, 2017), non citato dallo sciame. Il principio (immagine di distanza) si deduce dal titolo: il metodo non è stato letto.

### wikipedia-ricerca-bayesiana
Tipo: altro (voce di enciclopedia, fonte secondaria)
Autori: collaboratori di Wikipedia
Titolo: Bayesian search theory
Sede e anno: Wikipedia in inglese, versione letta il 14-11-2026
Identificativo: manca (identificativo della revisione non annotato)
Link: https://en.wikipedia.org/wiki/Bayesian_search_theory
Verifica: già verificata dal curatore in f3 [r]. Rafforzata oggi [g] sul testo sorgente della voce: p′ = p(1−q)/(1−pq) e r′ = r/(1−pq); il caso USS Scorpion (maggio 1968).
Usata per: analogia di creativo-2: cercare e non trovare sposta la probabilità sulle celle non cercate, p′ = p(1−q)/(1−pq), r′ = r/(1−pq) — `f1/e30f9e2dd4d7/CONSEGNA.md`
Note: non è fonte primaria; rimanda a `stone1975`. La formula è una riga di calcolo di Bayes, verificabile a mano.

### stone1975
Tipo: altro (libro)
Autori: Lawrence D. Stone
Titolo: Theory of Optimal Search
Sede e anno: Academic Press, 1975 (dati a memoria e da f3: non verificati oggi)
Identificativo: manca
Link: manca
Verifica: non verificata (non aperto né in f3 né oggi; f3 lo nomina come la fonte primaria a cui rimanda Wikipedia).
Usata per: fonte primaria della ricerca bayesiana, citata indirettamente — `f3/fonti/FONTI_VERIFICATE.md` (riga «Ricerca bayesiana»)
Note: nessun ruolo di f1 lo cita direttamente.

### hulgard2016
Tipo: articolo scientifico
Autori: Katrine Hulgard, John M. Ratcliffe
Titolo: Sonar sound groups and increased terminal buzz duration reflect task complexity in hunting bats
Sede e anno: Scientific Reports, vol. 6, articolo 21500, 2016 (9-2-2016)
Identificativo: DOI 10.1038/srep21500; PMC4746672
Link: https://pmc.ncbi.nlm.nih.gov/articles/PMC4746672
Verifica: già verificata dal curatore in f3 solo nei dati bibliografici. Completata oggi [g]: Crossref (volume, numero d'articolo) e testo intero da Europe PMC: «At the onset of buzz I, the bat… begin to produce calls at rates >90 calls/s»; «In buzz II, bats… produce calls at rates >160 calls/s».
Usata per: analogia di creativo-4: il pipistrello alza il ritmo dei richiami in avvicinamento, oltre 90 e poi oltre 160 al secondo — `f1/e30f9e2dd4d7/CONSEGNA.md`
Note: nel testo la seconda frase porta un rimando bibliografico (nota 9): i due valori sono ripresi dalla letteratura, non misurati in questo studio. Aperta anche dal ruolo.

---

## 6. Affermazioni rimaste senza fonte, e nomi citati senza riferimento

1. **Prove NEES/NIS come misura standard della coerenza di un filtro** — `f1/3fff79e9c3ea/FONTI.md` e `CONSEGNA.md` §1.6 (marca M), usate anche in `f1/21d3813ca7e1/CONSEGNA.md` (NIS = 1,95, NEES = 3,3 su 4, valori della simulazione del ruolo). Fonte: **manca**. Proposta del curatore, non citata dallo sciame e non verificata oggi: il manuale di Bar-Shalom, Li e Kirubarajan, «Estimation with Applications to Tracking and Navigation» (Wiley, 2001), dati a memoria: da controllare prima di citarlo.
2. **Glidance Glide, biped NOA** — `f1/3fff79e9c3ea/FONTI.md`: «non trovati e non verificati». Nessun riferimento: non citarli.
3. **ETH/UCY** (insiemi di traiettorie di pedoni) — nominati con `schoeller2020`; gli articoli originali degli insiemi non sono citati: manca.
4. **COCO, LVIS** — nominati in `f1/c85dbcc51ea6/CONSEGNA.md`; gli articoli originali non sono citati: manca (per COCO c'è solo `ultralytics-coco-yaml`).
5. **BoT-SORT, Deep OC-SORT, FastTracker, TrackTrack, MOTR, Social-LSTM, Social-GAN, SoPhie, SR-LSTM, RED, Cal-DETR, D-DETR** — nominati attraverso altre fonti (`ultralytics-tracciatori`, `schoeller2020`, `kuzucu2024`, `yang2025`); nessun riferimento proprio: manca.
6. **Classe 1 FDA** per i LiDAR — dichiarazione dei costruttori riportata in `f1/985ccd9bca46/CONSEGNA.md`; il regolamento non è citato: manca.
7. **Prezzi** — tutte le cifre in dollari di `f1/985ccd9bca46` sono di rivenditori e del giorno di lettura; ricontrollate oggi tre: Unitree L2 419 $ (regge), D455 (ora 650 $), Mid-360 (ora senza prezzo). Le altre: non verificate.
8. **Bozza della squadra e `regole_challenge.md`** — citate per numero di riga da tutti i ruoli; sono ingressi del progetto, non fonti esterne: fuori da questo elenco.
