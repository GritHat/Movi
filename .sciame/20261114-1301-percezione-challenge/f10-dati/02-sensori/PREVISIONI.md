# Previsioni di sciame-sensori (f10, 02-sensori)

Scritte alle 2026-11-14T15:58:04+01:00, PRIMA di aprire le schede tecniche scaricate e prima di ogni ricerca in rete.
Letti fin qui: CONTRATTO_DATI.md, FONTI_VERIFICATE.md, f1/985ccd9bca46/CONSEGNA.md, settimo addendum, righe B1/B3 del nucleo.
Fonte delle previsioni: la mia memoria delle schede (non verificata). Esiti in fondo, aggiunti dopo.

| Id | Previsione | Misura | Soglia di smentita |
|---|---|---|---|
| sensori-P1 | La scheda RealSense D400 dichiara base stereo 95 mm (D455) e 50 mm (D435i), ed errore RMS di profondità <= 2 % a 4 m (D455) e <= 2 % a 2 m (D435i) | ricerca testuale in rs.txt | un valore diverso nella scheda |
| sensori-P2 | Distanza minima a 848x480: circa 0,2 m (D435i) e circa 0,35-0,4 m (D455); a 1280x720: 0,28 m e 0,52 m | rs.txt, tabella Min-Z | scarto > 20 % |
| sensori-P3 | Gemini 335: base stereo 50 mm; accuratezza dichiarata <= 2 % a 2 m | g330.txt | base diversa da 50 mm o percentuale > 2 % a 2 m |
| sensori-P4 | La scheda RealSense dà la formula della banda senza dato sul bordo sinistro: larghezza in pixel = HRES*B/(2*Z*tan(HFOV/2)) | rs.txt | formula assente o banda sul bordo destro |
| sensori-P5 | Il sottopixel nominale dei documenti RealSense è 0,08 px; almeno una misura di terzi dà a 3 m un rumore fra 1 e 3 volte la formula con 0,08 px | documento di taratura RealSense + un articolo di terzi | sottopixel nominale diverso; misura di terzi fuori da [1x, 3x] |
| sensori-P6 | VL53L7CX/L8CX: stato del bersaglio 5 = valido, 9 = valido con impulso largo, 255 = nessun bersaglio; la scheda dà un'accuratezza in percentuale per fasce di distanza (ordine +-5 %) | vl53l7cx_ds.txt, um3038.txt | codici diversi o nessuna tabella di accuratezza |
| sensori-P7 | Nessuno strumento pubblico installabile con pip e usabile su sola CPU in pochi minuti riproduce i buchi e la banda d'occlusione di uno stereo attivo D4xx per profili di camera: esistono modelli per Kinect (assiale/laterale di Nguyen 2012, simkinect/Handa) e simulatori che richiedono GPU (Isaac Sim, SAPIEN/simsense); il modello va scritto a mano | ricerca in rete | trovo uno strumento con licenza permissiva, CPU, pip, che fa stereo attivo con profilo D435/D455 |
| sensori-P8 | Larghezza della banda senza dato dietro il bordo di un ostacolo (occlusione stereo), proiettata sullo sfondo: w = B*(z_sfondo - z_ostacolo)/z_ostacolo; nel caso peggiore della scena del nucleo (ostacolo a 1 m, sfondo a 3 m) vale 19 cm per la D455 e 10 cm per D435i e Gemini 335: quindi dello stesso ordine dei +-20 cm assunti per la maschera d'ombra, ma da un lato solo | calcolo + conferma del lato e della formula in un documento del costruttore | il documento dà una geometria diversa |
| sensori-P9 | RPLIDAR C1: accuratezza dichiarata +-30 mm; LD19: +-45 mm fino a qualche metro; nessuna delle due schede dà la portata sul nero per l'LD19 | schede/pagine dei costruttori | valori diversi |
| sensori-P10 | I filtri di post-elaborazione RealSense (decimazione, spaziale, temporale, riempimento dei buchi) NON sono applicati dal flusso grezzo dell'SDK: vanno istanziati; nel visualizzatore alcuni sono attivi; nel nodo ROS sono spenti di norma. Orbbec Gemini 335: nel dispositivo/SDK alcuni filtri sono attivi di norma (rimozione del rumore) | documentazione dei due SDK | la documentazione dice che il riempimento dei buchi è attivo di norma nel flusso grezzo RealSense |

## Esiti (aggiunti alle 2026-11-14T16:10:49+01:00, dopo le prove)

| Id | Esito | Prova |
|---|---|---|
| sensori-P1 | **regge** | rs.txt (scheda rev. 023): tab. 3-11 base 50 mm (D430) e 95 mm (D450); tab. 4-15 RMS <= 2 % entro 2 m (D43x) ed entro 4 m (D455) |
| sensori-P2 | **regge** | rs.txt tab. 4-12: 848x480 -> 195 mm e 350 mm; 1280x720 -> 280 mm e 520 mm |
| sensori-P3 | **regge** | g330.txt: base 50 mm; accuratezza <= +-2 % a 2 m; precisione spaziale <= 1,5 % a 2 m (1280x800) |
| sensori-P4 | **regge** | rs.txt par. 4.5: banda «at the left edge of the frame», larghezza B*F/Z pixel |
| sensori-P5 | **regge fino a 2,1 m; a 3 m non misurato** | BKM RealSense: «subpixel=0.08» per la curva della D435 a 848 px; Ahn 2019 a 2 m: 1,83 cm contro 1,51 (1,21 volte); a 3 m solo estrapolazione (1,14 volte). Una sola misura di terzi, parete bianca |
| sensori-P6 | **regge** | um3038.txt tab. 4 (5, 9, 255); DS13865 tab. 19: 8x8 +-5 % al buio sul bianco; in più: le accuratezze sono a 2,7 sigma |
| sensori-P7 | **regge sul campione cercato** (8 strumenti: non è una prova universale) | SimSense e SAPIEN chiedono la GPU (README); Redwood di Habitat-Sim è un modello Kinect; BlenderProc ha solo SGM generico e chiede Blender; Gazebo ha solo rumore gaussiano; Isaac Sim chiede una GPU RTX |
| sensori-P8 | **regge in parte** | il lato (sinistro) è confermato da Ahn 2019 («shadowing at the left edge») e dalla scheda (bordo dell'immagine); la formula ai bordi degli oggetti non l'ho trovata in un documento del costruttore: resta una mia derivazione geometrica. Valori: controlla_parametri.py (19,0 cm D455; 10,0 cm D435i e Gemini 335) |
| sensori-P9 | **regge** | pagina Slamtec C1: +-30 mm; scheda LD19 V2.5: +-45 mm (media di 100 misure), scarto tipo 10 mm; nessuna portata sul nero per l'LD19 |
| sensori-P10 | **regge per l'SDK RealSense e per la Gemini 335; non verificato** per il visualizzatore e per il nodo ROS | BKM: «By default we do not do any post-processing of the depth»; scheda Gemini 330 tab. 4-13-1: «Post Processing … Default Setting: Enable» |

Notato DOPO, non previsto: (a) Ahn 2019, fig. 9: il rumore assiale è piatto fino a 60° d'incidenza e supera 0,1 m a 75° (rotazione attorno all'asse verticale); (b) dal treppiede a 1,2 m il suolo oltre 2,08 m è visto a più di 60° d'incidenza; (c) le curve «nominale» e «pessimista» del nucleo (1,5/3,4/6,0 e 4/9/16 cm) coincidono con il nominale e con il limite di scheda della D435i, non della D455; (d) la risoluzione angolare dell'LD19 (0,8° a 10 Hz) è nella scheda V2.5; (e) l'esempio di metadati della documentazione librealsense dà 36,8 ms fra metà esposizione e inizio della trasmissione.

## Previsioni nuove per le prove a valle (scritte alle 2026-11-14T16:10:49+01:00, PRIMA che il simulatore e i dati veri siano elaborati)

| Id | Previsione | Misura | Soglia di smentita |
|---|---|---|---|
| sensori-P11 | L'errore della maschera d'ombra è asimmetrico: sul lato sinistro dell'ostacolo (nell'immagine) supera quello sul lato destro di B*(z_sfondo - z_ostacolo)/z_ostacolo, entro +-3 cm | bordo della regione senza dato contro il bordo geometrico, per lato, su profondità simulata con occlusione stereo e su registrazioni D4xx | differenza fra i lati sotto un terzo della banda prevista |
| sensori-P12 | Sul suolo fra 2,1 e 3 m (incidenza 60-68°) il sottopixel equivalente del residuo dal piano resta sotto 3 volte quello di una parete frontale alla stessa distanza (l'inclinazione attorno all'asse orizzontale pesa meno di quella misurata da Ahn) | registrazioni D4xx con suolo e parete visibili; s = sigma*fx*B/z^2 | rapporto >= 3, oppure quota di pixel validi del suolo in quella fascia sotto il 70 % su pavimento opaco |
| sensori-P13 | Con il filtro di riempimento dei buchi (modo predefinito: vicino più lontano) nascono celle «libere» dentro la banda d'occlusione stereo; senza filtri no | catena del nucleo su profondità simulata, con e senza l'emulazione del filtro; conteggio delle celle «libere» dentro la banda | con il filtro: 0 celle in più rispetto a senza filtro |
| sensori-P14 | Lo scarto tipo radiale del centro di una persona a 3 m sta fra 0,3 e 1 volta sigma_z(3 m) del singolo pixel (D435i nominale: 1,0-3,4 cm), non sigma_z/sqrt(N): rumore correlato più instabilità dei bordi | sequenze vere con una persona ferma, oppure simulate con correlazione_px = 5 | sotto 0,1 * sigma_z (rumore bianco) o sopra 1,5 * sigma_z |
