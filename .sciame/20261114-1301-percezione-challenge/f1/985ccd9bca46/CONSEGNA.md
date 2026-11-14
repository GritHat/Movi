Canarino: sciame-canarino-ff229a474629e844

# sciame-lidar, f1, corsia A: il sensore di distanza

## 1. Cambi di stato e regole violate

- Nessun cambio di stato precedente (parto da zero). Previsioni P1–P9 scritte alle 13:04:44 prima di aprire le
  schede; esiti e link completi in `PREVISIONI.md`. P10–P11 (prove fisiche) scritte alle 13:07 e non eseguite.
- Da segnalare: WebFetch ha salvato un PDF (scheda ST) nella cartella dei risultati della sessione, fuori dalla mia
  cartella: l'ho solo letto con `pdftotext`. Alcuni numeri vengono dal riassunto della ricerca e non dalla pagina
  aperta da me: sono marcati «(r)». Prezzi in dollari, di rivenditori, letti oggi; disponibilità in Italia non
  verificata. Tutti i numeri sono dichiarazioni dei costruttori, non misure indipendenti.

## 2. Diagnosi: critiche all'idea «3 sensori ToF per 360°»

1. **La geometria non torna con i ToF economici.** Servono 3 × 120° orizzontali. Il ToF multizona più largo
   (VL53L7CX) ha 60° × 60°; la scheda ST scrive che tre sensori coprono 180° × 60° [1]. L5CX e L8CX: 45° × 45° (r)
   [2]. **Smentito** per questa famiglia.
2. **Troppo poche zone e troppa poca portata.** Passo 5,6°–7,5° per zona: una persona larga 0,5 m occupa 1,3 zone
   a 4 m (calcolo). L7CX in 8×8: 2,0 m al buio su bianco, 0,5 m a 5 klx, 0,8 m su grigio 17% [1]. Non basta né a
   classificare né ad associare una traccia a 3–5 m.
3. **L'unica camera ToF da 120° trovata non regge budget, portata e sole.** Femto Bolt (iToF, 850 nm): 120° × 120°
   ma 0,25–2,88 m, «Indoor / Semi-outdoor», 418 $ l'una, 1254 $ per tre (r) [3]. Con campi sovrapposti le catture
   vanno sfalsate di almeno 160 µs col cavo di sincronizzazione, altrimenti i laser interferiscono [4].
4. **Tre sensori senza sovrapposizione non si calibrano fra loro** (3 × 120° = 360° esatti): non verificato, è un
   argomento geometrico; lo decide l'esperto di fusione.
5. **Grandezze non osservabili.** Nessun sensore di distanza misura la massa: va tolta. La velocità si ricava per
   differenza: con ±30 mm [8] e 10 Hz il rumore su un passo è circa 0,4 m/s, quello dell'accelerazione circa
   7 m/s² (2,6 mediando 8 punti; calcolo, con ±30 mm preso come scarto tipo: ipotesi). L'accelerazione va dichiarata
   «non osservabile sotto il secondo»; la velocità sì, filtrata.
6. **Che cosa una mappa di profondità non contiene.** Vetro: il raggio passa e una griglia a lancio di raggi segna
   «libero» dove c'è una porta (pericolo diretto per R8). Specchi: oggetti fantasma dietro. Nero assorbente: portata
   dimezzata (C1: 12 m al 70%, 6 m al 10% [8]). Bordi: pixel misti e volanti (iToF), bordi ingrossati (stereo).
   Angoli: cammini multipli (iToF). Buchi: «nessun dato», mai «libero». Stereo: l'errore cresce con z² (D435i,
   base 50 mm, 0,1 px: 4 cm a 3 m, 11 cm a 5 m; calcolo, ipotesi sul sottopixel non verificata).

| Famiglia (esempio) | Campo | Portata | Dati | Sole | Prezzo | In 24–48 h |
|---|---|---|---|---|---|---|
| ToF 8×8 (VL53L7CX) [1] | 60°×60° | 2,0 m buio; 0,5 m a 5 klx | 64 zone, 15 Hz | no | non verificato | I2C, facile, inutile oltre 2 m |
| iToF (Femto Bolt) [3] | 120°×120° o 75°×65° | 2,9 m largo; 5,46 m stretto (r) | 512×512, 30 fps | semi-esterno | 418 $ | USB, SDK |
| Stereo attivo (D455; Gemini 335) [5][7] | 87°×58°; 90°×65° | 0,6–6 m; ottimo 0,26–3 m | 848×480 o 1280×800, 30 fps, IMU | dichiarato, senza numero | 330–417 $ | USB, SDK e ROS 2 |
| LiDAR 2D 360° (RPLIDAR C1; LD19) [8][9] | 360°, un piano | 12 m; 6 m sul nero | 5000 punti/s, 10 Hz, 0,72° | 60 klx (LD19, r) | 70–80 $ | UART, ROS 2 |
| LiDAR 3D 360° (Unitree L2; Mid-360) [10][11] | 360°×90°; 360°×59° | 30 m (15 m al 10%); 40 m (r) | 64000 punti/s a 5,55 Hz | non verificato | 419 $; 899–1092 $ (r) | Ethernet, rischioso |

Camere dToF a matrice SPAD: nessuna scheda controllata, non verificato. D435i: 362–550 $ [6]. Tre OAK-D Pro W
(stereo attivo, 127° orizzontali, 499–529 $ l'una (r) [12]) sono l'unico «3 sensori per 360°» geometricamente
valido che ho trovato: fuori budget.

## 3. Stati proposti

- «3 ToF economici coprono 360°»: **smentito** (schede [1][2], calcolo P2).
- «3 camere iToF da 120° nel budget e con portata 3–5 m»: **smentito** sulla Femto Bolt [3]; **non risolto** per
  altri modelli (lo deciderebbe una scheda con ≥ 120° e ≥ 4 m sotto i 150 $).
- «Stima della massa dal sensore»: **smentito** (non è nella misura). «Accelerazione»: **non risolto**, serve la
  misura del rumore reale su una traccia.
- «Un sensore frontale dà ≥ 40 pixel su una persona a 4 m»: **sostenuto dal calcolo** (42–56 px), da misurare (P10).

## 4. Proposte

**lidar-1. Un solo sensore frontale buono, e i 360° dichiarati come limite.** Camera stereo attiva con IMU (D455,
D435i o Gemini 335, o quella già posseduta), circa 87° × 58°, 30 fps. Tutto ciò che è fuori dal campo è
«sconosciuto» per costruzione: è la risposta onesta a R4, R6 e R8.
- *Meccanismo e guadagno:* 42–56 pixel su una persona a 4 m contro 1,3 zone; colore allineato per la
  classificazione; un cavo USB, nessuna interferenza fra sensori, nessuna calibrazione estrinseca. L'occlusione
  della demo (R3) avviene comunque nel campo frontale.
- *Vincoli:* niente retro; portata utile 3–6 m; vetro e nero come al punto 6; al sole pieno non verificato.
- *Chi la prova:* la squadra con la camera; esperto di sensori e di fusione per i limiti.
- *Falsificatore (5 min):* P6 (fatto: regge) e P10 (persona con pantaloni scuri a 4 m: prevedo ≥ 70% di pixel
  validi; smentita sotto il 50%). Se il budget è zero e non c'è camera: questa proposta cade, resta lidar-2.

**lidar-2. Se i 360° servono davvero: un LiDAR 2D rotante più la camera frontale di lidar-1.** RPLIDAR C1 o
LD19 (70–80 $): un solo emettitore, quindi nessuna diafonia; 360° a 10 Hz.
- *Meccanismo e guadagno:* il lancio di raggi dà per ogni direzione «occupato», «libero fin qui» o «sconosciuto
  oltre»: R4 e R8 su tutto il giro; 5000 punti/s costano quasi niente alla CPU (R7). Avvisa di ciò che arriva da
  dietro, senza classificarlo.
- *Vincoli:* un solo piano (non vede gradini, tavoli, ostacoli bassi o sospesi); 8 punti su una persona a 5 m,
  2 su una gamba (P8); vetro invisibile; un giro dura 100 ms: se chi lo indossa ruota a 90°/s, a 5 m la scansione
  si deforma di 0,8 m (calcolo) e va corretta con IMU e tempo per punto; addosso, il corpo copre circa metà giro
  (non verificato). Rende molto meglio fermo su un palo: favorisce l'applicazione industriale.
- *Chi la prova:* la squadra; esperto di nuvole di punti e di tracciamento.
- *Falsificatore (5 min):* P7–P8 (fatti: reggono) e P11 (una persona gira attorno a 5 m: prevedo ≥ 4 punti nel
  90% dei giri; smentita sotto). Con 420 $ in più l'Unitree L2 dà il 3D a 360°, ma a 5,55 Hz [10].

**Sicurezza ottica, da dichiarare.** Tutti i sensori citati sono dichiarati classe 1 (ST [1], C1 FDA [8], L2
IEC 60825-1:2014 [10]; Femto Bolt e RealSense: non verificato). La classe vale per il prodotto integro: non si
tolgono coperture, non si aggiungono ottiche, non si modifica il firmware. Non verificato: il comportamento a
motore fermo dei LiDAR rotanti e la somma di più emettitori verso lo stesso occhio.

## 5. Che cosa propongo dopo

Scegliere lidar-1 come base e lidar-2 come estensione opzionale; far eseguire P10 e P11 appena c'è l'hardware;
chiedere all'utente quali sensori la squadra possiede già (cambia tutta la scelta).

**Fonti.** [1] https://www.pololu.com/file/0J1992/vl53l7cx.pdf · [2]
https://www.st.com.cn/resource/en/flyer/vl53l7cx-vl53l8cx-flyer.pdf · [3]
https://www.orbbec.com/wp-content/uploads/2023/08/ORBBEC_Datasheet_Femto-Bolt-0816-v01.pdf e
https://store.orbbec.com/products/femto-bolt · [4]
https://doc.orbbec.com/documentation/Orbbec%20Femto%20Bolt%20Documentation/Synchronize%20Multiple%20Femto%20Bolt%20Devices
· [5] https://www.roboticscenter.ai/store/product/intel-realsense-d455 · [6]
https://uk.rs-online.com/web/p/depth-cameras/0155773 · [7]
https://www.orbbec.com/products/stereo-vision-camera/gemini-335/ · [8] https://www.waveshare.com/rplidar-c1.htm ·
[9] https://openelab.io/products/ldrobot-d500-dtof-lidar-kit · [10] https://www.unitree.com/L2 · [11]
https://www.roboticscenter.ai/es/store/product/livox-dji-livox-mid-360 · [12] https://www.arducam.com/oak-d-pro-w.html
