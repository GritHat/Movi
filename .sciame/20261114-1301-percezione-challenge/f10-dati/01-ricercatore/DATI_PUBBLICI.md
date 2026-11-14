# Dati pubblici per Q6 — ricognizione (sciame-ricercatore, f10)

Prove del 14 novembre 2026, fra le 15:58 e le 16:10; previsioni scritte prima (15:58:48) in `PREVISIONI.md`. Ogni indirizzo è stato interrogato oggi con `curl -I` (riporto codice e byte); le pagine sono in `pagine/`, gli elenchi dei file dentro gli archivi in `elenchi/`. Gli elenchi vengono dal solo indice finale degli archivi, letto con richieste a intervalli (`strumenti/`, codice mio).

## 0. Cambi di stato, scostamenti, limiti

- **Previsioni:** reggono P1, P2 (KTP sparito), P4, P6, P7 (di stretta misura: vedi HUM4D), P8 (4,04 GB), P9, P10, P11. **Smentite** P3 (EPFL sparito) e P5 (Princeton risponde).
- **Scostamenti.** Nessun insieme scaricato; ho però letto pezzi di archivi: 8 indici ZIP (3 MB l'uno, tenuto solo l'elenco), 4 indici bag (meno di 0,13 MB), 6 prove di velocità da 4 MB (scartate), le prime righe di 4 file THÖR. `pagine/` pesa 7,0 MB, ogni file sotto 5 MB. Per le pagine morte ho usato archive.org.
- **Indipendenza.** Condivido il modello linguistico con gli autori del nucleo; l'indipendenza sta nelle risposte dei server. Le licenze le ricontrolli il curatore delle fonti.
- **Non verificato:** il contenuto dei due archivi `.tgz` e `.tar.gz` (non si elencano senza scaricarli); se nei bag RealSense ci sono persone, e la loro risoluzione; l'unità della profondità in DepthTrack, HUM4D e Bonn; quanti passaggi nascosti contiene Friburgo; a quale variante di THÖR («un ostacolo», «robot in moto», «tre ostacoli») corrispondono Exp_1, 2, 3 (dedotto dall'ordine); la licenza dei file di Princeton, Bonn, FROG e dei bag RealSense (non dichiarata nelle pagine lette).

## 1. Camere di profondità con persone e occlusioni

| Insieme | File minimo (byte) | Sensore e montaggio | Verità di riferimento | Licenza, ostacoli | Differenza dal sensore della squadra |
|---|---|---|---|---|---|
| **TUM RGB-D, fr3/walking_static** ([pagina](https://cvg.cit.tum.de/data/datasets/rgbd-dataset/download), 200) | [`.tgz`](https://cvg.cit.tum.de/rgbd/dataset/freiburg3/rgbd_dataset_freiburg3_walking_static.tgz), 474 074 105; 4,4 MB/s | Kinect v1, 640×480, 30 Hz, quasi ferma (0,282 m in 24,83 s). Dal file della posa: quota 1,38–1,43 m, asse ottico in media 8,5° sotto l'orizzonte (3,8–14,5°) | Solo la posa della camera (cattura del moto) | CC BY 4.0 | Luce strutturata; campo verticale 48,0°: suolo visto solo da 2,2 m (squadra: 1,24 m). Pochi passaggi in 25 s |
| **RGB-D People, Friburgo** ([pagina](http://www2.informatik.uni-freiburg.de/~spinello/RGBD-dataset.html), 200) | [`.tar.gz`](http://www2.informatik.uni-freiburg.de/~spinello/sw/rgbd_people_unihall.tar.gz), 2 805 714 553; 1,6 MB/s (29 min). Il collegamento nella pagina (`www.informatik…`) è rotto: serve `www2` | Tre Kinect v1 fermi, in verticale, su una torre a circa 1,50 m; atrio; 30 Hz; oltre 3000 fotogrammi | Per traccia: riquadro per fotogramma, identità, **visibilità (0 nascosto, 1 visibile, 2 parziale)**; parametri nella pagina | CC BY-NC-SA 3.0 | Profondità **grezza a 11 bit, non metrica**: va convertita (e la pagina avverte di un possibile scambio dei byte). Nessuna posizione metrica vera. Suolo visto da circa 2,8 m |
| **Bonn RGB-D Dynamic** ([pagina](https://www.ipb.uni-bonn.de/data/rgbd-dynamic-dataset/), 200) | [`moving_obstructing_box.zip`](https://www.ipb.uni-bonn.de/html/projects/rgbd_dynamic2019/rgbd_bonn_moving_obstructing_box.zip), 320 845 314; 7,1 MB/s | Camera in moto, formato TUM, fx = 542,8 | Posa della camera; nuvola di punti della scena ferma | Non dichiarata | Camera in moto; niente sulle persone |
| **Princeton Tracking Benchmark** ([pagina](https://tracking.cs.princeton.edu/dataset.html), 200) | [`ValidationSet.zip`](https://tracking.cs.princeton.edu/ValidationSet.zip), 631 649 593: 5 sequenze | Kinect, profondità in mm con 3 bit ruotati, matrice K in `frames.json` | Riquadro del bersaglio per fotogramma | Non dichiarata | Scene ravvicinate, un bersaglio |
| **DepthTrack, prova** ([Zenodo](https://zenodo.org/records/5792146), 200) | [`human02_indoor.zip`](https://zenodo.org/api/records/5792146/files/human02_indoor.zip/content), 578 368 987: 1740 fotogrammi | 50 archivi separati. Sensore: a memoria una RealSense D415, **non trovato nelle pagine lette** | Riquadro e attributi per fotogramma | CC BY 4.0 | Bersagli generici |
| **HUM4D** ([pagina](https://parkyeeun23.github.io/HUM4D/), 200; CVPR 2026) | Cartella di Google Drive: un PNG di profondità per fotogramma (603 899 quello provato, circa 15 Hz), verità in `.npz` (17,6 MB) | **Sei RealSense D455 ferme a 1,45 m**, a 3 m dal centro; calibrazione letta: 1280×800, fx = 642, base 94,96 mm; 44 sequenze, fino a 3 persone | Vicon, anche durante l'occlusione | CC BY 4.0. **Ostacolo:** nessun archivio; senza browser si vedono solo i primi 50 file per cartella (3,3 s) | **Il più vicino al sensore della squadra.** Inclinazione non dichiarata; le persone si nascondono fra loro |
| **Oxford-IHM** ([pagina](https://articulated.robots.ox.ac.uk/oxford-indoor-human-motion-dataset/), 200) | circa 60 min di rosbag | RealSense D435 ferma; ostacoli (tavolo, pianta) | Vicon a 100 Hz sulla testa | CC BY-NC-SA 4.0. **Ostacolo: accesso su richiesta motivata** | Ideale, ma non ottenibile in 14 ore |
| Kinect Tracking Precision | — | Pagina e archivi: **404** (resta solo la pagina in archive.org) | — | — | Non raggiungibile |
| Pedoni RGB-D dell'EPFL | — | Pagina e archivio: **404** | — | — | Non raggiungibile |

JRDB chiede un conto (letto oggi). CDTB non approfondito.

## 2. Stereo attivo grezzo del costruttore

File di esempio RealSense ([pagina](https://github.com/realsenseai/librealsense/blob/master/doc/sample-data.md)), ROS bag 2.0, profondità non filtrata, 15 MB/s. Base: `https://librealsense.realsenseai.com/rs-tests/`.

| File | Byte | Dall'indice |
|---|---|---|
| `D435i_Depth_and_IMU_Stands_still.bag` | 107 375 642 | D435i ferma: 229 immagini di profondità in 7,64 s, più IMU; non compresso |
| `TestData/stairs.bag` (D435, una scala) | 409 209 452 | 146 di profondità, 75 di colore; compresso lz4 |
| `TestData/structured.bag` | 140 920 932 | 127 di profondità, 105 di colore, 4,21 s |
| `TestData/outdoors.bag` (D415) | 422 868 878 | 181 di profondità, 8,10 s |

Nessuna verità di riferimento e pochi secondi: misure solo descrittive. Per Orbbec Gemini 335 e Luxonis OAK-D una ricerca non ha trovato registrazioni pubbliche: **non risolto**.

## 3. Altri sensori

| Fonte | File (byte) | Contenuto | Licenza |
|---|---|---|---|
| **THÖR, tracce delle persone** ([Zenodo](https://zenodo.org/records/3382145), 200) | `Exp_1_run_1_6D.tsv` 50 448 813; `Exp_3_run_1_6D.tsv` 49 068 383; 2,6 MB/s | Traiettorie vere di persone al chiuso fra ostacoli, cattura del moto a **100 Hz**: 339 s, 10 caschi, posizione e orientamento. Nessuna camera di profondità | CC BY 4.0 |
| LiDAR 2D, **DROW v2** ([deposito](https://github.com/RWTHVision/DROW), 200) | [`DROWv2-data.zip`](https://github.com/VisualComputingInstitute/DROW/releases/download/v2/DROWv2-data.zip), 197 970 996 | SICK S300 a 37 cm, 225° in 450 punti; persone annotate sul 5 % delle scansioni | MIT |
| LiDAR 2D, **FROG** ([pagina](https://robotics.upo.es/datasets/frog/laser2d_people/), 200) | `frog_16-41_test.h5`, 148 746 736 | HDF5: scansioni da 720 punti, persone annotate su tutte; robot in moto | Non dichiarata |
| Radar a onde millimetriche ([Zenodo](https://zenodo.org/records/8377254), 200) | `PointCloudData.zip`, 508 208 132 | 9 persone che camminano **dietro un ostacolo**; nessuna posizione vera dichiarata | CC BY 4.0 |
| ToF multizona ([Zenodo](https://zenodo.org/records/17190312), 200) | un archivio, 96 302 013 | Tre VL53L5CX davanti a una lavagna in posizioni note: serve al modello del sensore, **senza persone** | CC BY 4.0 |

ToF multizona con persone e verità: niente trovato (indice di Zenodo, 6 schede; una ricerca in rete). **Lacuna.**

## 4. Lettura senza codice altrui

Archivi: `tarfile` (con `filter="data"`) e `zipfile`, in una cartella nuova. TUM: PNG a 16 bit, valore/5000 = metri, 0 = nessun dato; parametri «Freiburg 3»: fx 535,4, fy 539,2, cx 320,1, cy 247,6. Friburgo: PGM a 16 bit, lettore proprio. Bag: formato semplice (il mio lettore dell'indice è di 42 righe); per i messaggi serve lz4, oppure la libreria Python `rosbags`. THÖR: 11 righe d'intestazione, poi colonne con tabulazioni.

## 5. LA SCELTA

In ordine; 4,04 GB in tutto (limite 6 GB). `S` è la cartella `f10-dati/scaricati`. Ogni comando rilanciato riprende da dove era arrivato; il file è completo quando la dimensione coincide con quella scritta qui (forma del comando provata su un file TUM da 173 kB: rilanciata, esce con 0 senza riscaricare; la ripresa su Friburgo e Zenodo non è provata, ma tutti rispondono 206 alle richieste a intervalli).

```sh
prendi(){ curl -L --fail --connect-timeout 20 --max-time 590 -C - -o "$1" "$2"; }
# 1. TUM fr3/walking_static: 474 074 105 byte, circa 2 minuti
mkdir -p $S/tum_fr3_walking_static
prendi $S/tum_fr3_walking_static/walking_static.tgz https://cvg.cit.tum.de/rgbd/dataset/freiburg3/rgbd_dataset_freiburg3_walking_static.tgz
# 2. THÖR, una registrazione per tarare e una per provare: 99 517 196 byte, circa 1 minuto
mkdir -p $S/thor
prendi $S/thor/Exp_1_run_1_6D.tsv https://zenodo.org/api/records/3382145/files/Exp_1_run_1_6D.tsv/content
prendi $S/thor/Exp_3_run_1_6D.tsv https://zenodo.org/api/records/3382145/files/Exp_3_run_1_6D.tsv/content
# 3. Friburgo: 2 805 714 553 byte, da rilanciare 3 o 4 volte (10 minuti l'una)
mkdir -p $S/friburgo_rgbd_people
prendi $S/friburgo_rgbd_people/rgbd_people_unihall.tar.gz http://www2.informatik.uni-freiburg.de/~spinello/sw/rgbd_people_unihall.tar.gz
# In più, prima del 3: tre bag RealSense, 657 506 026 byte, circa 1 minuto
mkdir -p $S/realsense_bag; B=https://librealsense.realsenseai.com/rs-tests
prendi $S/realsense_bag/stands_still.bag $B/D435i_Depth_and_IMU_Stands_still.bag
prendi $S/realsense_bag/stairs.bag $B/TestData/stairs.bag
prendi $S/realsense_bag/structured.bag $B/TestData/structured.bag
```

| Fonte | Ipotesi del contratto che permette di decidere | Che cosa NON dice |
|---|---|---|
| 1. TUM | **1** (quattro stati da una profondità vera, con montaggio simile), **2** e **5** in forma descrittiva, **6** | Niente sullo stereo attivo né sulle posizioni delle persone |
| 2. THÖR | **4**: errore della previsione contro il tempo d'occlusione, copertura, valore di q su pedoni veri, nascondendo tratti di traiettorie vere | Niente sul rilevamento: parte da posizioni perfette |
| 3. Friburgo | **4** (identità alla ricomparsa, con la visibilità annotata), **5** (camera ferma: falsi «in movimento»), **3** solo come limite superiore | Nessun errore metrico; conversione della profondità da tarare |
| In più: RealSense | **1** e **2** sul sensore della classe giusta (buchi, banda senza dato, la scala contro «pavimento piano»), **6** | Senza verità; persone non verificate; 4–8 s |

**Ripiego se il primo non risponde:** `rgbd_bonn_moving_obstructing_box.zip` (320 845 314 byte, stesso formato). **Se Friburgo è troppo lento:** `ValidationSet.zip` di Princeton più `human02_indoor.zip` di DepthTrack (1,21 GB).

## 6. Che cosa resta aperto, e che cosa propongo

- **ricercatore-1.** L'ipotesi 3 e l'errore metrico dell'ipotesi 4 **su profondità vera** non si decidono con ciò che si scarica via `curl`: serve HUM4D. Proposta: una persona della squadra scarica dal browser una cartella di camera di `Group_Hide_Each_Other…take001` e il suo `.npz`. Previsione: meno di 1 GB; smentita se supera 2 GB o se l'`.npz` non dà posizioni riportabili alla camera.
- **ricercatore-2.** Nessuna fonte ha la camera a 1,2 m inclinata di 15°: l'anello cieco e il suolo vicino li decide solo il sensore simulato o quello della squadra.
- **ricercatore-3.** L'accesso a Oxford-IHM va chiesto solo per il dopo-hackathon.
