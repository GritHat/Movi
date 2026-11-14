# PREVISIONI di sciame-lidar (f1, corsia A)

Scritte alle 2026-11-14T13:04:44+01:00, PRIMA di aprire qualunque scheda tecnica o pagina di prezzo e prima dei calcoli.
Fonte delle previsioni: la mia memoria (taglio a metà 2026), quindi da smentire con le schede.
Esiti possibili: regge, smentita, non risolta. Gli esiti vanno in fondo, con l'ora.

## Falsificatori di lidar-1 (un solo sensore frontale di profondità invece di 3 ToF a 360°)

- **P1 (campo visivo dei ToF multizona).** Misura: campo visivo orizzontale dichiarato nelle schede dei ToF multizona
  economici (ST VL53L5CX, VL53L7CX, VL53L8). Previsione: nessuno arriva a 120° orizzontali; il massimo è 60°×60°
  (90° in diagonale) del VL53L7CX; L5CX e L8 stanno a circa 45°×45° (65° in diagonale). Quindi 3 sensori coprono al
  più 180°, non 360°. **Smentita se** una scheda di un ToF multizona sotto i 30 euro dichiara ≥ 120° orizzontali.
- **P2 (zone su una persona).** Misura: calcolo, larghezza angolare di una persona larga 0,5 m divisa per il passo
  angolare di una zona (45°/8 = 5,6°; 60°/8 = 7,5°). Previsione: a 4 m una persona occupa meno di 2 zone in
  orizzontale (attese circa 1,3 con 45°, circa 1,0 con 60°); a 3 m meno di 2. **Smentita se** il conto dà ≥ 3 zone
  a 4 m.
- **P3 (portata dei ToF multizona).** Misura: portata massima dichiarata in 8×8. Previsione: ≤ 4 m al buio su
  bersaglio chiaro, e sotto i 2 m in 8×8 con luce ambiente forte (ordine dei 5 klx o più) o bersaglio scuro.
  **Smentita se** la scheda dichiara ≥ 3 m in 8×8 con luce ambiente forte.
- **P4 (camera iToF a grande campo).** Misura: scheda di Orbbec Femto Bolt (o equivalente). Previsione: il modo a
  campo largo è 120°×120° ma con portata sotto i 3 m, e il prezzo è ≥ 350 euro l'una: tre unità superano le
  «poche centinaia di euro» del contratto. **Smentita se** portata nel modo largo ≥ 5 m, oppure prezzo ≤ 150 euro.
- **P5 (interferenza fra ToF attivi).** Misura: documentazione del costruttore sul funzionamento con più unità.
  Previsione: per le camere iToF il costruttore prescrive la sincronizzazione con ritardi sfalsati (ordine di 160 µs
  fra unità) per evitare l'interferenza; senza, la profondità si corrompe nelle zone sovrapposte. **Smentita se** il
  costruttore dichiara che più unità non sincronizzate con campi sovrapposti non interferiscono.
- **P6 (stereo attivo frontale).** Misura: schede di Intel RealSense D435i/D455 e Luxonis OAK-D (Lite, Pro W).
  Previsione: campo di profondità circa 87°×58° per le RealSense; portata utile dichiarata ≥ 3 m (D435i) e ≥ 6 m
  (D455); ≥ 30 fps; funzionamento al sole (stereo passivo come ripiego); prezzo fra 150 e 500 euro; IMU a bordo.
  Una persona larga 0,5 m a 4 m occupa ≥ 40 pixel in orizzontale a 640 px di larghezza. **Smentita se** la portata
  dichiarata è < 3 m, o il conto dà < 20 pixel.

## Falsificatori di lidar-2 (un LiDAR 2D rotante a 360° più una camera, se i 360° servono davvero)

- **P7 (LiDAR 2D economico).** Misura: schede di Slamtec RPLIDAR C1 e LDROBOT LD19 (o D500). Previsione: 360°,
  frequenza di scansione ≥ 10 Hz, ≥ 4000 punti/s, portata ≥ 10 m su bersaglio chiaro, classe 1 per l'occhio,
  prezzo ≤ 120 euro, interfaccia UART/USB con driver ROS 2 e Python pubblici. **Smentita se** una di queste voci
  è falsa per entrambi i sensori.
- **P8 (punti su una persona).** Misura: calcolo dal passo angolare (360° × 10 Hz / punti al secondo). Previsione:
  passo circa 0,7–0,8°; una persona larga 0,5 m a 5 m riceve fra 6 e 10 punti per giro, una gamba larga 0,12 m
  a 5 m fra 1 e 2 punti. **Smentita se** i punti sulla persona a 5 m sono < 4.
- **P9 (LiDAR 3D a 360° di fascia bassa).** Misura: prezzo e campo di Livox Mid-360 e Unitree L2 (o L1).
  Previsione: Mid-360 sopra i 500 euro (fuori ipotesi di budget); Unitree L2 sotto i 500 euro, 360°×90°.
  Integrazione in 24–48 ore possibile ma più rischiosa del 2D. **Smentita se** il Mid-360 costa ≤ 400 euro o
  l'Unitree L2 costa > 700 euro.

## Falsificatori fisici per la squadra (aggiunti alle 2026-11-14T13:07:34+01:00; NON eseguiti: non ho l'hardware)

Aggiunti dopo le verifiche P1–P9 ma prima di qualunque prova fisica, che nessuno ha ancora fatto.

- **P10 (lidar-1, cinque minuti con la camera in mano).** Al chiuso, vicino a una finestra, una persona con
  pantaloni scuri a 4 m misurati col metro. Misura: frazione di pixel di profondità validi dentro il riquadro della
  persona, su 30 fotogrammi. Previsione: ≥ 70% validi, larghezza ≥ 40 pixel a 640 px. **Smentita se** < 50% validi
  o larghezza < 20 pixel. Stessa prova davanti a una porta a vetri: prevedo che il vetro NON compaia nella
  profondità (si vede ciò che sta dietro, o un buco).
- **P11 (lidar-2, cinque minuti con il LiDAR 2D fermo su un tavolo).** Una persona fa un giro completo attorno al
  sensore a 3 m e poi a 5 m. Misura: frazione dei giri (10 Hz) in cui il gruppo di punti della persona ha ≥ 4 punti.
  Previsione: ≥ 90% dei giri a 5 m, in ogni direzione (nessun settore cieco a sensore fermo e libero). **Smentita
  se** < 90%, o se esiste un settore cieco > 10°.

## Esiti (scritti DOPO)

Scritti alle 2026-11-14T13:07:34+01:00. Indipendenza: i controlli condividono con ciò che controllano le schede dei costruttori (numeri
dichiarati, non misure indipendenti) e la mia memoria (da cui vengono le previsioni). I prezzi sono in dollari, di
rivenditori, letti oggi: non ho controllato la disponibilità in Italia né i tempi di consegna.

- **P1: regge.** VL53L7CX: 60° × 60°, 90° in diagonale (scheda ST DS13865 rev 6, tabella 2,
  https://www.pololu.com/file/0J1992/vl53l7cx.pdf). La stessa scheda scrive «three sensors can cover 180° x 60°
  FoV». VL53L5CX e VL53L8CX a 45° × 45°: letto nel volantino ST
  (https://www.st.com.cn/resource/en/flyer/vl53l7cx-vl53l8cx-flyer.pdf) attraverso il riassunto della ricerca, la
  tabella non l'ho aperta io.
- **P2: regge.** Calcolo: persona larga 0,5 m; a 4 m 1,27 zone (passo 5,6°) e 0,95 zone (passo 7,5°); a 3 m 1,69 e
  1,27; a 5 m 1,02 e 0,76.
- **P3: regge, ed è peggio del previsto.** VL53L7CX in 8×8 a 15 Hz (tabella 18 della stessa scheda): bianco 88%
  tipico 2,0 m al buio e 0,5 m a 5 klx; grigio 17% tipico 0,8 m al buio e 0,35 m a 5 klx. Per L5CX/L8CX: 4 m al buio
  (confronto Pololu) e 1,7 m / 2,85 m con luce ambiente (presentazione ST): letti nel riassunto della ricerca, modo
  e condizioni non verificati.
- **P4: regge.** Femto Bolt: iToF a 850 nm; modo largo 120° × 120° con portata 0,25–2,21 m (1024×1024) e
  0,25–2,88 m (512×512, fino a 30 fps); 418 dollari sul negozio Orbbec; ambiente «Indoor / Semi-outdoor»
  (https://www.orbbec.com/wp-content/uploads/2023/08/ORBBEC_Datasheet_Femto-Bolt-0816-v01.pdf,
  https://store.orbbec.com/products/femto-bolt: letti nel riassunto della ricerca; il negozio ha poi risposto 429
  alla mia lettura diretta). Tre unità: 1254 dollari.
- **P5: regge.** Guida Orbbec, letta direttamente: «To prevent interference between lasers, the camera captures
  should be offset from each other by 160us or more»; impulso di 125 µs, 9 impulsi per cattura
  (https://doc.orbbec.com/documentation/Orbbec%20Femto%20Bolt%20Documentation/Synchronize%20Multiple%20Femto%20Bolt%20Devices).
  Richiede il cavo di sincronizzazione fra le unità. Per i ToF multizona ST non ho trovato un enunciato del
  costruttore sull'interferenza fra sensori: non verificato.
- **P6: regge sulla soglia (portata e pixel); prezzo e sole non risolti.** D455: 87° × 58°, IMU BMI085, portata
  0,6–6 m, da 399 a 417 dollari (https://www.roboticscenter.ai/store/product/intel-realsense-d455,
  https://nl.rs-online.com/web/p/depth-cameras/0155774). D435i: 87° × 58°, 848×480 a 90 fps; variante D435if
  «0.3 m, 3 m Max Range» (https://uk.rs-online.com/web/p/depth-cameras/0155773); prezzi letti fra 362 e 550
  dollari (https://wamatek.com/products/intel-realsense-d435i-webcam-2-megapixel-30-fps-usb-3-2,
  https://www.roboticscenter.ai/store/product/realsense-d435i): il tetto di 500 che avevo previsto è superato da
  un rivenditore. Orbbec Gemini 335: stereo attivo e passivo, 90° × 65°, ottimo 0,26–3 m, 1280×800 a 30 fps, IMU,
  «Outdoor and indoor» (https://www.orbbec.com/products/stereo-vision-camera/gemini-335/, letta direttamente),
  330–369 dollari da rivenditori. OAK-D Lite: 73° × 58°, un rivenditore europeo la dà fuori produzione
  (https://botland.store/modules-smart-cameras/20955-oak-d-lite.html). Calcolo: a 4 m una persona larga 0,5 m
  occupa 42 pixel (640 px, 87°) o 56 pixel (848 px). Nessun numero di tenuta al sole trovato: non verificato.
- **P7: regge.** RPLIDAR C1: 360°, 8–12 Hz (tipico 10), 5000 misure/s, passo 0,72°, 12 m al 70% e 6 m al 10% di
  riflettività, 905 nm, classe 1 FDA, UART, 5 V e 230 mA, SDK con ROS e ROS 2, 79,99 dollari
  (https://www.waveshare.com/rplidar-c1.htm, letta direttamente). LD19/D500 (STL-19P): 12 m, 4500–5000 misure/s,
  60 klx dichiarati (ricordavo 30: memoria sbagliata), classe 1 FDA, 69–70 dollari
  (https://files.waveshare.com/wiki/D500-LiDAR-Kit/LDROBOT_STL-19P_Datasheet_EN_v1.0(1).pdf,
  https://openelab.io/products/ldrobot-d500-dtof-lidar-kit: riassunto della ricerca). Driver Python pubblici: non
  verificato.
- **P8: regge.** Calcolo: C1 passo 0,72°: 8,0 punti su una persona a 5 m, 1,9 su una gamba; a 3 m 13,2 e 3,2.
  LD19 passo 0,8°: 7,2 e 1,7 a 5 m.
- **P9: regge.** Livox Mid-360: 899–1092 dollari da rivenditori, 979 riportati come listino
  (https://www.roboticscenter.ai/es/store/product/livox-dji-livox-mid-360,
  https://dronexl.co/2026/09/21/livox-mid-360l-lidar-half-point-rate-robots/: riassunto della ricerca). Unitree L2:
  419 dollari, 360° × 90° (96° in un modo particolare), 64000 punti/s utili, 30 m al 90% e 15 m al 10%, classe 1
  IEC 60825-1:2014, Ethernet UDP e UART, IMU (https://www.unitree.com/L2, letta direttamente).
- **P10, P11: non risolte.** Non eseguite: manca l'hardware. Le decide la squadra in cinque minuti ciascuna.

### Notato DOPO (non era nelle previsioni)

- Il ToF multizona col campo più largo (L7CX, 60°) è anche quello con la portata più corta in 8×8: 2 m al buio.
- Unitree L2: il giro completo è a 5,55 Hz (https://www.unitree.com/L2): 180 ms per vedere tutto l'orizzonte.
- Femto Bolt dichiarata per interni o semi-esterni: tre iToF al sole non sono una configurazione prevista.
