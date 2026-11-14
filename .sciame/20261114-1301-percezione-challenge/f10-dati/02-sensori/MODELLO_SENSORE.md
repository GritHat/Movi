# Specifica dell'hardware simulato — f10, `02-sensori` (`sciame-sensori`), 14 novembre 2026

**Stato e scostamenti.** Nessun cambio di stato precedente. Previsioni sensori-P1…P10 scritte alle 15:58, prima di aprire le schede (`PREVISIONI.md`): 7 reggono, 3 in parte (P5: a 3 m manca una misura di terzi; P8: la formula ai bordi resta mia; P10: nodo ROS e visualizzatore non verificati). **Nessun parametro è misurato sull'esemplare della squadra.** Scostamenti: letta `../../f9-preproposta/07-lidar/scaricati/`, come chiede la consegna; i documenti scaricati oggi stanno in `scaricati/` con `PROVENIENZA.md`; tre valori sono letti a occhio da grafici; le pagine Orbbec sui filtri non si sono aperte; la pagina sulla validazione è un file a parte. Sigle: **D** dichiarato dal costruttore, **M** misurato da terzi, **C** calcolato da D o M, **I** ipotesi mia da tarare. In `parametri_sensori.json` ogni chiave ha la provenienza (93 D, 5 M, 20 C, 32 I); `python3 -I controlla_parametri.py parametri_sensori.json` la controlla (0 errori) e ricalcola i numeri qui sotto.

## 1. Camera di profondità a stereo attivo

| | D455 | D435i | Gemini 335 | Tipo e fonte |
|---|---|---|---|---|
| Campo; flusso scelto | 87°×58°; 848×480, 30 fps (fino a 90) | 87°×58°; idem | 90°×60°; 848×480, 30 fps (fino a 60) | D [S1][S6] |
| Base B; focale fx a 848 px | 95 mm; 424 px | 50 mm; 424 px | 50 mm; 410,7 px | B: D; fx: D [S6], C dal campo di 90° dell'imager [S1][S2] |
| Distanza minima; fascia ideale | 0,35 m; 0,6–6 m | 0,195 m; 0,3–3 m | 0,18 m; 0,3–3 m | D [S1][S6][S13] |
| Sottopixel s: nominale / limite | 0,08 (I) / 0,20 px | 0,08 (D) / 0,21 px; terzi 0,097 (M) | 0,082 (C) / 0,154 px | [S2]; limite C da «RMS ≤ 2 %» a 4 e a 2 m [S1] e «≤ 1,5 % a 2 m» [S6]; [S3] |
| σz a 2 / 3 / 4 m: nominale | 0,8 / 1,8 / 3,2 cm | 1,5 / 3,4 / 6,0 cm | 1,6 / 3,6 / 6,4 cm | C |
| σz a 2 / 3 / 4 m: limite | 2,0 / 4,5 / 8,0 cm | 4 / 9 / 16 cm | 3,0 / 6,8 / 12 cm | C |
| Banda d'occlusione (ostacolo a 1 m, sfondo a 3 m) | 27 px = 19 cm | 14 px = 10 cm | 14 px = 10 cm | C |
| Otturatore; IMU | globale; marca a 50 µs | globale (colore progressivo); idem | globale IR (colore progressivo); 50–1000 Hz | D |

**Rumore assiale.** Rumore gaussiano sulla disparità d = fx·B/z, quindi σz = z²·s/(fx·B) (D [S2]). Il costruttore dà s < 0,1 px per una camera ben tarata e 0,08 per la curva della D435 [S2]. **M [S3]** (D435, 848×480, parete bianca, 0,4–2,1 m): σz = 0,0011 + 0,0007·z + 0,0039·z², cioè 1,83 cm a 2 m (1,21 volte il nominale); a 3 m è un'estrapolazione. Per la Gemini il nominale viene dal grafico di scheda (circa 1,2 % a 3 m, a occhio, a 1280×800); che a 848×480 resti uguale in metri è **I**. I valori D valgono su bersaglio bianco e frontale, nell'80 % centrale del campo.
- **Parte fissa e parte temporale.** Il rumore temporale dichiarato è metà dello spaziale (≤ 1 % contro ≤ 2 % [S1]; tipico 0,45 % contro circa 0,65 % a 2 m [S6]): quota temporale 0,6·s, quota fissa 0,8·s attaccata alla superficie (C). Il rumore è **correlato nello spazio** («bumps… like an egg carton» [S2]); lunghezza 5 px (**I**). Il centro di una persona quindi non migliora con √N.
- **Incidenza.** M [S3], fig. 9: σz piatto fino a 60°, oltre 0,1 m a 75°, con il bersaglio ruotato attorno all'asse **verticale**. Dal treppiede a 1,2 m il suolo oltre 2,08 m è visto oltre i 60° (68° a 3 m), ma è inclinato attorno all'asse orizzontale: nessuna fonte lo misura, **non verificato**. Nel modello: 1/cos (nominale), ×5 (limite).
- **Quantizzazione.** Passo di disparità 1/32 px (**I**): 7 mm a 3 m (D455), 13 mm (le altre). Uscita in unità da 1 mm.

**Rumore laterale e bordi.** M [S3]: 4,3 cm al bordo sinistro, 4,1 cm al destro (90° percentile, senza andamento con la distanza): è il limite; nominale 1,5 px (**I**; 1 px = 4,7 mm a 2 m). Lo stereo non produce pixel «volanti» come il tempo di volo: ingrossa l'oggetto vicino (2 px, **I**) e interpola i pixel a cavallo del salto (3 px misti, **I**). Sfocatura da moto = v·esposizione: 12 mm a 1,5 m/s con 8 ms, 45 mm con 30 ms (massimo dell'esposizione automatica della Gemini, D).

**Buchi** (valore 0 = nessun dato).
1. **Bordo sinistro dell'immagine**: fx·B/z pixel (D [S1] §4.5; il riferimento è l'imager sinistro): 20 px a 2 m (D455), 11 (D435i). La configurazione predefinita può allargarla [S1]; in [S3] fig. 5 appare larga il doppio (a occhio): margine 0–25 px (**I**).
2. **Occlusione stereo**: a **sinistra** di ogni bordo verticale di un oggetto vicino (lato: M [S3]) manca lo sfondo per fx·B·(1/z_ostacolo − 1/z_sfondo) pixel, cioè B·(z_sfondo − z_ostacolo)/z_ostacolo metri (C, geometria; non trovata in un documento del costruttore). È deterministica (ricetta riga per riga nel JSON). I bordi orizzontali non ne hanno.
3. **Fuori portata**: sotto la distanza minima (D).
4. **Materiale**, nominale / limite, a macchie, persistenza 0,7 fra fotogrammi: diffuso chiaro 0,005 / 0,02 (D: riempimento ≥ 99 % [S1], ≥ 99,5 % [S6]); tessuto scuro 0,05 / 0,3; nero assorbente 0,3 / 0,8; pavimento lucido radente 0,1 / 0,5, con profondità **falsa** (riflesso) nel 20 % dei casi; vetro e specchio: niente, o lo sfondo. Tutte **I** salvo la prima.
5. **Luce**: M [S12] (D435 a 0,67 m): riempimento sotto l'80 % su ogni tessera a 7770 lux e sulla più scura a 4350 lux. Sotto 1000 lux nessun effetto modellato (**I**).

**Filtri del costruttore.** RealSense: il processore D4 non filtra («By default we do not do any post-processing» [S2]); i filtri sono blocchi dell'SDK, attivi solo se il programma li crea. Se creati, valgono [S4]: decimazione 2; spaziale 2 iterazioni, α 0,5, δ 20; temporale α 0,4, δ 20, **persistenza 3** (riempie il buco con l'ultimo valore se il pixel era valido in 2 degli ultimi 4 fotogrammi); riempimento dei buchi **modo 1, copia il vicino più lontano**. Nel nodo ROS ogni filtro ha `<filtro>.enable`; lo stato predefinito lì e nel visualizzatore: non verificato. Gemini 335: «Post Processing» nel dispositivo è **attivo di norma** [S6, tab. 4-13-1]; la lista si legge con `getRecommendedFilters()` e `isEnabled()`; che cosa contiene: non verificato. **Per il nucleo: persistenza e riempimento spenti, stato dei filtri scritto nel registro all'avvio.**

**Tempo.** RealSense [S5]: `SENSOR_TIMESTAMP` = metà dell'esposizione, orologio del dispositivo; `FRAME_TIMESTAMP` = inizio della trasmissione; `TIME_OF_ARRIVAL` = arrivo al calcolatore. Gemini: marca hardware in µs, stessa sorgente per IMU e immagini [S6]. Latenza: nessuna specifica; l'unico esempio della documentazione dà 36,8 ms più 34 ms: **70 ms nominale (C, un campione), 120 ms limite (I)**.

## 2. Tempo di volo multizona [S7][S8][S9] — tutto D

| | VL53L7CX | VL53L8CX |
|---|---|---|
| Campo; zona in 8×8 / 4×4 | 60°×60°; 7,5° / 15° | 45°×45°; 5,6° / 11,25° |
| Frequenza | 8×8 fino a 15 Hz, 4×4 fino a 60; all'accensione 1 Hz | provato a 15 e 30 Hz (massimi non riletti) |
| Portata 8×8 a 15 Hz, bianco 88 % / grigio 17 % | buio 2,0 / 0,8 m; 5 klx 0,5 / 0,35 m | buio 4,0 / 2,45 m; 5 klx 1,55 / 1,15 m |
| Portata 4×4 a 30 Hz | buio 3,5 / 1,4 m; 5 klx 0,65 / 0,55 m | buio 4,0 / 4,0 m; 5 klx 2,85 / 1,65 m |
| Accuratezza 8×8 oltre 0,2 m, a **2,7 σ** | ±5 % buio; ±9–14 % a 5 klx | ±5 % buio; ±5–8 % a 5 klx |

Rumore per zona: σ = accuratezza/2,7 (C): 1,9 % in 8×8 al buio, 3,7 cm a 2 m. La portata è definita al 90 % di misure valide. Stati del bersaglio: 5 valido, 9 valido con impulso largo (bersagli fusi), 6 prima misura, 255 nessun bersaglio, gli altri non validi (lista nel JSON). La matrice esce capovolta nei due sensi. Una zona a 2 m è larga 13 cm (L7CX) o 10 cm (L8CX). Come una zona sceglie fra due bersagli: **I**.

## 3. LiDAR 2D a scansione [S10][S11] — D salvo dove segnato

| | RPLIDAR C1 | LD19 |
|---|---|---|
| Passo angolare; campioni; giri | 0,72°; 5 kHz; 10 Hz (8–12) | 0,8° a 10 Hz; 4,5 kHz; 10 Hz (5–13) |
| Portata sul bianco 70 % / sul nero 10 % | 0,05–12 m / 6 m | 0,02–12 m / non dichiarata (**I**: 6 m) |
| Accuratezza; scarto tipo; risoluzione | ±30 mm; non dichiarato (**I**: 10 mm); 15 mm | ±45 mm (media di 100 misure, da 0,3 m); 10 mm; 15 mm |
| Luce ambiente | 40 klx | 30 klx |

Un solo piano; 12–13 punti su una persona a 3 m (C); ogni punto ha il suo istante (un giro dura 100 ms).

## 4. Simulatori e modelli di rumore (verificato oggi)

| Strumento | Licenza | Che cosa fa | Su sola CPU, in minuti? |
|---|---|---|---|
| Open3D `RaycastingScene` (`open3d-cpu` 0.20.0, ruote per Python 3.14) | MIT | profondità ideale dalla geometria | **sì**; senza rumore: ci va sopra il nostro modello |
| Riproduzione di registrazioni D4xx: `pyrealsense2` 2.59.1 (`enable_device_from_file`), `rosbags` in Python puro | Apache-2.0 | il programma legge un file come fosse la camera | **sì** (installazione non provata); campioni pubblici `stairs.bag` (D435, 409 MB), `d435i_sample_data.zip` (472 MB) |
| Modello Redwood in Habitat-Sim (versione CPU) | MIT | rumore in disparità, quantizzazione a 1/8 px, scambio di pixel; tarato sul **Kinect** | la struttura sì (40 righe), i parametri no |
| simkinect (modello ICL-NUIM) | assente nel deposito | rumore Kinect su profondità pulita | no (licenza) |
| BlenderProc (`stereo_global_matching` con SGBM di OpenCV) | GPL-3.0 | resa stereo con Blender e accoppiamento vero | pochi fotogrammi; tempo non provato |
| SimSense; SAPIEN (Zhang e altri, T-RO, arXiv 2201.11924) | MIT; Apache-2.0 | stereo attivo come nei sensori veri | **no**: CUDA o GPU obbligatoria |
| Gazebo `gz-sensors` | Apache-2.0 | solo rumore gaussiano | no: né buchi né occlusione |
| Isaac Sim | proprietaria | rumore stereo annunciato nella 5.0 | **no**: GPU RTX (solo dal riassunto di ricerca) |

Nessuno strumento su sola CPU riproduce buchi e occlusione di una D4xx con un profilo pronto (P7 regge sugli strumenti in tabella: non è una prova universale). **Due passi:** (1) il modello analitico di questa specifica sopra una profondità ideale, 30–60 minuti; (2) se avanza tempo, coppia IR sinistra-destra con trama proiettata e SGBM di OpenCV con controllo sinistra-destra, da cui occlusione e bordi nascono da soli (2–3 ore, non provato).

## 5. Validare il modello contro registrazioni vere

Pagina a parte: `VALIDAZIONE_MODELLO.md`. Undici statistiche, ciascuna con il valore atteso e la soglia che smentisce il modello: quota di pixel validi, banda al bordo sinistro, residuo dal piano su parete e suolo per distanza, rapporto temporale/spaziale, correlazione, banda d'occlusione per lato, instabilità dei bordi, buchi per materiale, quantizzazione, filtri, tempi.

## 6. Critiche al nucleo, stati, proposte

1. **Le curve del nucleo sono quelle della D435i.** «Nominale» 1,5 / 3,4 / 6,0 cm e «pessimista» 4 / 9 / 16 cm coincidono con il nominale e con il limite di scheda della D435i; con la D455 valgono la metà. La portata «rumore ≤ 5 cm» va dichiarata per profilo.
2. **La banda d'occlusione è sistematica e da un lato solo**: fino a 19 cm (D455) o 10 cm (le altre); con il rumore laterale, 23 e 14 cm. I ±20 cm simmetrici assunti per la maschera d'ombra hanno l'ordine giusto e la forma sbagliata: **non risolto**, lo decide P11. Chi riappare a sinistra dell'ostacolo si vede 0,16 s dopo a 1,2 m/s (C).
3. **K-014 ha un meccanismo concreto**: il riempimento predefinito copia il vicino più lontano e trasforma la banda in sfondo, cioè in «libero»; la persistenza tiene la profondità vecchia. **Sostenuto dalla documentazione [S4], non provato**: lo decide P13.
4. **Il «libero» oltre 2,1 m poggia su suolo visto oltre i 60°**, dove l'unica misura (su un altro asse) vede il rumore esplodere: **non risolto** (P12).
5. **K-007**: per un oggetto fermo conta la sola quota temporale (0,6·σz), per uno in moto tutta σz; il centro non si media come √N (P14). **Non risolto.**

**Proposte.** *sensori-1:* il simulatore applica i sette passi del JSON e gira sempre due volte, nominale e limite; un'ipotesi «regge» solo se regge in entrambe (la smentisce un caso in cui il limite cambia la decisione). *sensori-2:* la sorgente del prototipo è un'interfaccia «profondità + marca temporale + stato dei filtri», servita da simulatore, file o camera. *sensori-3:* le ipotesi I più pesanti (buchi per materiale, correlazione, margine della banda) si tarano sulle prime registrazioni vere, e il JSON cambia versione.

**Dopo.** All'arrivo dell'inventario: confronto dei sensori posseduti con questi profili e tre misure sull'esemplare (parete piana a 1, 2, 3 m; suolo; un bordo verticale), 15 minuti.

**Fonti** (tutti gli indirizzi in `parametri_sensori.json`, `meta.fonti`). Aperte oggi: S2 RealSense, «BKMs Tuning D4xx» (https://realsenseai.com/wp-content/uploads/2019/11/BKMs_Tuning_RealSense_D4xx_Cam.pdf); S3 Ahn e altri, UR 2019 (https://ucla.box.com/shared/static/gqxwr2vvqsf22oi9dqtn50hr0xkruzie.pdf); S4, S5 librealsense (https://github.com/IntelRealSense/librealsense/tree/master/doc); S10 https://www.slamtec.com/en/C1/Spec; S11 scheda LD19 V2.5 (copia di un rivenditore); S12 rapporto DXOMARK. Lette nelle copie locali: S1 scheda RealSense D400 rev. 023; S6 scheda Gemini 330 v1.6; S7–S9 ST DS13865, UM3038, DS14161. Non riaperta: S13.
