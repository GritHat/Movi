# Fonti verificate — percezione-challenge, f3 (`sciame-fonti`), 14 novembre 2026

**Metodo e limiti.** Ogni pagina è stata aperta oggi. **[g]** = il dato è stato trovato con una ricerca testuale nel testo grezzo scaricato (pagina o PDF); **[r]** = letto solo attraverso lo strumento di lettura, che riassume: più debole. Condivido con gli autori il modello linguistico; l'indipendenza sta nel testo delle fonti. **Scostamenti:** (1) il sito st.com non risponde (timeout, connessione chiusa): le schede ST sono state lette nelle copie PDF ospitate da Pololu e SparkFun (documenti ST originali, con numero e revisione; la revisione può non essere l'ultima); (2) i file scaricati stanno nella cartella temporanea della sessione, non in questa; (3) non controllati per tempo: i prezzi (salvo Femto Bolt), F4, F10–F13, F25–F28, F30, Arducam, Unitree L2, Livox Mid-360, OAK-D Pro W, depth_clustering, MATR, 49 CFR 236.205, ST UM2884. **Previsioni scritte prima** (in `stato.md`): P1 nessun ToF citato con ≥ 130° e ≥ 4 m: **regge**; P2 licenze come dichiarate: **regge con una precisazione** (RF-DETR, punto 5); P3 almeno tre numeri diversi nella fonte primaria: **regge** (punti 3, 4, 6, 7).

## 1. Correzioni che contano

1. **K-012, Femto Bolt: i due numeri sono entrambi giusti, sono due modi.** 0,25–2,88 m = campo largo 2×2 raggruppato (512×512, fino a 30 fps); 0,25–2,21 m = campo largo pieno (1024×1024, solo 5 o 15 fps). Campo stretto: 0,5–3,86 m (640×576) e 0,5–5,46 m (320×288 raggruppato). [g] pagina prodotto e scheda PDF.
2. **K-012, VL53L7CX: anche qui due modi.** 3,5 m = 4×4 a 30 Hz, al buio, bersaglio bianco 88 %; 2,0 m = 8×8 a 15 Hz, stesse condizioni. Con luce ambiente di 5 klx: 0,65 m (4×4) e 0,5 m (8×8); grigio 17 % in 8×8: 0,8 m al buio. [g] ST DS13865 Rev 6, tabelle 17 e 18. I numeri di `lidar` sono tutti confermati.
3. **Nessun sensore citato cambia la conclusione di F-001** (controllo sui soli sensori citati, non una ricerca esaustiva). Il più largo è la Femto Bolt (120°×120°, 2,88 m); il più lungo fra i multizona è il VL53L8CX (4 m, ma 45°×45°). **Dato nuovo utile:** a 5 klx il VL53L8CX tiene 2,85 m in 4×4 a 30 Hz e 1,55 m in 8×8 a 15 Hz (bianco 88 %), contro 0,65/0,5 m dell'L7CX e 1,7 m dell'L5CX in 4×4. 5 klx è la condizione di prova della scheda («equivalent to 5 kLux daylight»), non il sole pieno, che le schede non caratterizzano.
4. **LD19: la tenuta alla luce è 30 klx, non 60.** La pagina Waveshare dell'LD19 dà 30 klx, 4500 Hz, 0,02–12 m, 5–13 Hz [r]; i 60 klx sono dell'STL-19P (kit D500), pagina del rivenditore openelab [g]. RPLIDAR C1 (pagina Slamtec [r]): 12 m sul bianco 70 %, 6 m sul nero 10 %, 5 kHz, 10 Hz tipici, 0,72°, 40 klx: confermati. La risoluzione angolare 0,8° dell'LD19: non trovata.
5. **RF-DETR: Apache 2.0 vale per il codice e per i modelli N, S, M, L, per tutta la segmentazione e per i punti chiave; i modelli di rilevamento Atto, Femto, Pico, XL e 2XL sono sotto PML 1.0.** [g] README del deposito. Per RF-DETR-N la licenza dichiarata regge: 2,3 ms su T4 (TensorRT, FP16, lotto 1), AP 48,4. Il README stesso ricorda che YOLO26 è AGPL-3.0.
6. **TAPNext: «1024 punti a 348 fps su H100» non è nell'articolo.** La Tabella 2 (v1 e v2) dà, con 1024 punti, 187 fps su H100 e 42 su V100 (TAPNext-B, latenza 5,33 ms su H100) [g]. La conclusione (GPU da centro di calcolo) non cambia.
7. **Attribuzioni da correggere.** (a) Koschi e Althoff: IEEE T-IV vol. 6(2), pp. 249–265, **2021** (in linea 2020), DOI 10.1109/TIV.2020.3017385; il link mediatum respinge i lettori automatici. (b) arXiv 2008.08063 è il riassunto esteso di AB3DMOT per i Workshop di ECCV 2020; l'articolo intero è Weng, Wang, Held, Kitani, «3D Multi-Object Tracking: A Baseline and New Evaluation Metrics», IROS 2020, DOI 10.1109/IROS45743.2020.9341164. (c) F8 è Lupu e altri, Sensors 20(20):5821, 2020. (d) F7: il PDF del KIT dà 404; la frase è nel riassunto su Springer (DOI 10.1007/978-3-319-08599-9_20).
8. **Femto Bolt, ambiente: le due fonti Orbbec non coincidono.** La pagina prodotto di oggi scrive «Indoor»; la scheda PDF v01 (agosto 2023) scrive «Indoor/Semi-Outdoor». Ogni autore ha citato bene la sua fonte. **K-009 resta una discordanza vera fra costruttori, non un errore di citazione:** Luxonis scrive davvero «<1% indoors, <2% outdoors», senza dire a quale illuminamento.
9. **F29: «fattore medio 1,68» non è scritto nell'articolo:** è exp(0,519) dell'ALDE di Tabella 1, calcolato dal ricercatore; va dichiarato come derivato. 0,665 e 1,066 (APE su image2mass) e 0,980 contro 0,976 (su ABO-500) sono confermati [r].
10. **Ultralytics: il tracciatore predefinito è TrackTrack** (`tracker: tracktrack.yaml` in `default.yaml` [g]). `track_buffer: 30` è il valore di `bytetrack.yaml` [g]: giusto come «predefinito di ByteTrack», non come predefinito del tracciatore che parte se non si sceglie niente (`tracktrack.yaml` non letto).

## 2. Tabella

| Rif. | Come risulta dalla fonte | Link | Dato citato | Stato |
|---|---|---|---|---|
| VL53L5CX | ST, scheda DS13754 Rev 2 (8/2021), copia SparkFun | sì (st.com no) | 45°×45°, 63° diag., 400 cm: sì [g]; 4×4 a 30 Hz: 4,0 m buio, 1,7 m a 5 klx | verificato |
| VL53L7CX | ST DS13865 Rev 6 (3/2023), copia Pololu | sì | 60°×60° (90° diag.), 350 cm, «three sensors can cover 180° x 60°»: sì [g]; portate: punto 2 | verificato |
| VL53L8CX | ST DS14161 Rev 7 (8/2023), copia Pololu | sì (st.com no) | 45°×45°, 65° diag., 400 cm: sì [g]; a 5 klx: punto 3 | verificato |
| Volantino ST L7CX/L8CX | st.com.cn | no | — | non verificabile (sostituito dalle schede) |
| Femto Bolt | Orbbec, pagina prodotto e scheda PDF 0816-v01 | sì | 120°×120° e 75°×65°, 850 nm: sì [g]; IMU: sì [r]; portate: punto 1; ambiente: punto 8; 418 $ nel negozio Orbbec: sì [g] | verificato |
| Sincronia Femto Bolt | Orbbec, «Synchronize Multiple Femto Bolt Devices» | sì | «offset from each other by 160us or more»; impulso 125 µs: sì [g] | verificato |
| D455, D435i | RealSense, confronto camere (realsenseai.com; intelrealsense.com non risolve) | sì | D455: 87°×58°, ideale 0,6–6 m, otturatore globale su profondità e RGB, IMU; D435i: 87°×58°, 0,3–3 m, RGB a otturatore progressivo, IMU: sì [g, colonne attribuite via r] | verificato |
| Gemini 335 | Orbbec, pagina prodotto | sì | 90°×65°, ottimale 0,26–3 m, 1280×800 a 30 fps, IMU, interno ed esterno: sì [g]; tipo di otturatore: assente | verificato |
| RPLIDAR C1, LD19 | Slamtec (solo http); Waveshare; openelab | sì | punto 4 | verificato con correzione |
| Luxonis ToF | Luxonis, «ToF Depth Perception» | sì | 640×480, 20 cm–5 m, «<1% indoors, <2% outdoors», interferenza fra più ToF: sì [g] | verificato (fonte del costruttore) |
| ISPRS 2023 (F5) | Qiu, Martínez-Sánchez, Arias, «Evaluation and comparison of different time of flight cameras for outdoor applications», ISPRS Annals X-1/W1-2023, 2023 | sì | «outdoor applications remain limited, mainly due to… sunlight interference»: sì [g]; prove su Azure Kinect e Pmd Monstar | verificato |
| YOLO26 | Ultralytics, documentazione e file LICENSE | sì | YOLO26n 640: 38,9 ± 0,7 ms CPU ONNX, 1,7 ms T4, mAP 40,9; AGPL-3.0: sì [g]; YOLOE-26 40,6 AP LVIS: è la variante x [r] | verificato |
| RF-DETR | Roboflow, README | sì | punto 5 | verificato con correzione |
| Tracciatori Ultralytics | `cfg/default.yaml`, cartella `cfg/trackers`, `bytetrack.yaml` | sì | sei tracciatori (BoT-SORT, ByteTrack, OC-SORT, Deep OC-SORT, FastTracker, TrackTrack); `track_buffer: 30`; intestazione AGPL-3.0: sì [g]; re-identificazione spenta [r] | verificato (punto 10) |
| SAM 3 | Carion e altri 37, «SAM 3: Segment Anything with Concepts», arXiv 2511.16719 v2 | sì | «30 ms for a single image with 100+ detected objects» su H200; circa 5 oggetti quasi in tempo reale: sì [g, testo intero; non nel riassunto] | verificato |
| SAM 3.1 | Meta, blog, aggiornamento 27/3/2026 | sì (solo r) | da 16 a 32 fps su una H100, video con numero medio di oggetti: sì [r] | verificato [r] |
| EdgeTAM | Zhou e altri, arXiv 2501.07256, CVPR 2025 (dal deposito) | sì | 16 fps su iPhone 15 Pro Max [g]; Apache-2.0 [g]; SAM 2 minimo «around 1 FPS» [g]; 150,9 fps su A100 [r] | verificato |
| SAMURAI | Yang, Huang, Chai, Jiang, Hwang, arXiv 2411.11922 (2024) | sì | Kalman che sceglie la maschera: sì [g, testo; non nel riassunto]; Apache-2.0; «doesn't support live/streaming video»: sì [g] | verificato |
| TAPNext | Zholus e altri, arXiv 2504.05579 (2025) | sì | punto 6 | verificato con correzione |
| Depth Anything 3 | Lin e altri, arXiv 2511.10647 (2025); numeri: post di GerdsenAI sul forum Open Robotics, 5/2/2026 | sì | 6,35 → 43+ fps su Jetson Orin NX 16 GB: sì [g]; variante «small»: assente nel post | verificato in parte; fonte di comunità |
| SORT | Bewley, Ge, Ott, Ramos, Upcroft, arXiv 1602.00763, ICIP 2016 | sì | «updates at a rate of 260 Hz»: sì [g] | verificato |
| OC-SORT (F16) | Cao, Pang, Weng, Khirodkar, Kitani, arXiv 2203.14360, CVPR 2023 | sì | rumore accumulato in occlusione, ORU, «700+ FPS on a single CPU»: sì [g]; deposito MIT [g] | verificato |
| ByteTrack (F15) | deposito FoundationVision | sì | MIT; «30 FPS… on a single V100 GPU»: sì [g] | verificato |
| AB3DMOT | punto 7b | sì | Kalman 3D più ungherese: sì [g] | verificato con correzione |
| SimpleTrack | Pang, Li, Wang, arXiv 2111.09621 (2021); sede non controllata | sì | «life cycle management» come parte a sé: sì [g] | verificato |
| HOTA | Luiten e altri, IJCV 129:548–578, DOI 10.1007/s11263-020-01375-2; arXiv 2009.07736 | sì | esiste, con questi autori | verificato |
| F14 | Schöller, Aravantinos, Lay, Knoll, RA-L 5(2):1696–1703, 2020, DOI 10.1109/LRA.2020.2969925; arXiv 1903.07933 | sì | Tabella I a 4,8 s: velocità costante 0,39/0,83; RED 0,44/0,91; SR-LSTM 0,45/0,94; S-GAN 0,32/0,60: sì [g] | verificato |
| Koschi e Althoff | punto 7a | DOI sì; mediatum no | titolo e autori: sì; testo non letto | verificato con correzione (anno) |
| Orzechowski, Meyer, Lauer | «Tackling Occlusions & Limited Sensor Range with Set-based Safety Verification», ITSC 2018, arXiv 1807.01262 | sì | ostacoli nascosti sovrastimati con intervalli di stato: sì [g] | verificato |
| Nuss e altri | IJRR 37(8):841–866, 2018, DOI 10.1177/0278364918775523; arXiv 1605.02406 | sì | «highly efficient parallel particle filter»: sì [g] | verificato |
| OctoMap | Hornung, Wurm, Bennewitz, Stachniss, Burgard, Autonomous Robots 34:189–206, 2013, DOI 10.1007/s10514-012-9321-0 | il link di Bonn dà una pagina, non il PDF | esiste; testo non letto | verificato (solo i dati bibliografici) |
| Moras e altri | Moras, Cherfaoui, Bonnifait, «Credibilist Occupancy Grids for Vehicle Perception in Dynamic Environments», ICRA 2011 (HAL hal-00615303) | sì | esiste; testo non letto | verificato (solo i dati bibliografici) |
| Ricerca bayesiana | Wikipedia, «Bayesian search theory» (fonte secondaria; rimanda a Stone 1975, non aperto) | sì | p′ = p(1−q)/(1−pq): sì [r] | verificato [r], non primaria |
| F29 | Lee, Jeong, Hong, Kim, «Physically Guided Visual Mass Estimation from a Single RGB Image», arXiv 2601.20303, IJCAI 2026 | sì | punto 9 | verificato; 1,68 è derivato |
| F6 | Kozlov e altri, «GuideTouch…», arXiv 2601.13813, HRI 2026 (lavori in corso) | sì | 92,9 % e 93,75 % (14 persone): sì [g]; 2 ToF, 4 attuatori, 22 persone: sì [r]; «28 intervistati»: non controllato | verificato (riassunto) |
| F7 | Martinez, Constantinescu, Schauerte, Koester, Stiefelhagen, ICCHP 2014, LNCS, pp. 128–135 | KIT no; DOI sì | «22 times higher cognitive load»; «not found on blindfolded users»: sì [g, riassunto] | verificato con correzione (link) |
| F8 | Lupu, Mitruț, Stan, Ungureanu, Kalimeri, Moldoveanu, Sensors 2020 | sì | 8 persone; «haptic stimuli were less intuitive than the audio ones»; carico cognitivo maggiore: sì [r] | verificato [r] |
| F9 | Romlay, Toha, Ibrahim, Venkat, BEEI 10(3), DOI 10.11591/eei.v10i3.3055 | sì | 70 articoli; 22,9 %; 1,4 %: sì [r]; anno non letto | verificato [r] |
| F22 | Kuzucu, Oksuz, Sadeghi, Dokania, ECCV 2024, LNCS pp. 185–204, DOI 10.1007/978-3-031-72664-4_11; arXiv 2405.20459 | sì | «much more powerful and effective…»; «more than 7 D-ECE»: sì [g] | verificato |
| F20, F23, F24 | TAO-Amodal (Hsieh e altri, arXiv 2312.12433); Munir e altri, CVPR 2023; Timans e altri, ECCV 2024 (arXiv 2403.07263) | sì | F20: frase e +2,1 %/+3,3 %: sì [g]; F23 e F24: esistono, affermazione non riletta | verificato (F20); solo dati bibliografici (F23, F24) |
| F21 | Ding, Yang, Shu, Chen, «TinySAM 2…», arXiv 2605.18013 (5/2026) | sì | l'articolo è questo; 25,6 fps: non nel riassunto | numero non verificato |
| Hulgard e Ratcliffe | Sci Rep 2016, «Sonar sound groups and increased terminal buzz duration reflect task complexity in hunting bats» | sì | esiste | verificato (solo i dati bibliografici) |

## 3. Le dodici fonti più utili da citare

1. ST, scheda VL53L7CX, DS13865 Rev 6 — campo 60°×60° e portate per modo: https://www.pololu.com/file/0J1992/vl53l7cx.pdf
2. ST, scheda VL53L8CX, DS14161 Rev 7 — 45°×45°, 4 m, portata a 5 klx: https://www.pololu.com/file/0J2029/vl53l8cx.pdf
3. Orbbec, Femto Bolt — campo e portata per modo: https://www.orbbec.com/products/tof-camera/femto-bolt/
4. RealSense, confronto delle camere — D455 e D435i: https://www.realsenseai.com/compare-depth-cameras/
5. Luxonis, ToF in interno e in esterno, interferenza: https://docs.luxonis.com/hardware/platform/depth/ToF-depth
6. Qiu e altri 2023, ToF in esterno: https://isprs-annals.copernicus.org/articles/X-1-W1-2023/17/2023/
7. Schöller e altri 2020, velocità costante sui pedoni: https://arxiv.org/abs/1903.07933
8. Cao e altri 2023, OC-SORT, errore del Kalman in occlusione: https://arxiv.org/abs/2203.14360
9. Ultralytics, YOLO26 (latenza, AGPL-3.0) e tracciatori: https://docs.ultralytics.com/models/yolo26/ e https://docs.ultralytics.com/modes/track/
10. Roboflow, RF-DETR (latenza, licenze per modello): https://github.com/roboflow/rf-detr
11. Lee e altri 2026, massa dalla visione: https://arxiv.org/abs/2601.20303
12. Martinez e altri 2014, feedback aptico contro sonoro: https://doi.org/10.1007/978-3-319-08599-9_20

**Dopo.** Se il documento finale cita un prezzo, o una fonte dell'elenco «non controllati», va verificata a parte. Per K-009 nessuna fonte decide: serve la prova al sole sul sensore che la squadra possiede.
