# Inventario dei sensori: tabella di decisione — `sciame-embedded`, f10, 14 novembre 2026

**In testa.** Lavoro dalle 15:57 alle 16:16 (`date -Is`). Previsioni E1–E13 scritte alle 15:57:59, prima di ogni pagina e di ogni script: 10 reggono (3 con una correzione), 3 no (E2, E5, E12); esiti, comandi e scostamenti in `PREVISIONI.md`. **Scostamenti:** tre pacchetti PyPI installati in un ambiente temporaneo fuori da `ambiente/` (poi cancellato); pagine scaricate nella cartella temporanea, non in `scaricati/`; due script in più in questa cartella. **Non provato:** nessun dispositivo è mai stato collegato; i tempi al primo fotogramma sono **stime mie**; «(m)» = dalla mia memoria, **non verificato oggi**. **Indipendenza:** lo stato degli SDK viene da depositi e pagine dei costruttori (testo grezzo cercato); le mie sequenze sono ricontrollate da `03-infrastruttura/controlla_sequenza.py` (stessa specifica, altro codice e altro autore, stesso modello linguistico).

## 1. La decisione in due minuti

1. **C'è una camera di profondità densa?** Si prende la prima in quest'ordine: RealSense D435/D435i/D455/D415 → Orbbec Gemini / Astra 2 / Femto → OAK-D Pro → L515 → Kinect v1 → OAK-D, OAK-D Lite → Azure Kinect → Kinect v2 → Astra prima serie. L'utente registra le sequenze del §4. È la sola integrazione che vale le 14 ore.
2. **Uno dei cinque ha un iPhone Pro (dal 12) o un iPad Pro (dal 2020) (m)?** È profondità vera **subito**, senza aspettare 5–6 ore: si registra con Stray Scanner, il convertitore è pronto.
3. **Solo moduli da microcontrollore, webcam, radar, ultrasuoni?** Nessuna integrazione nelle 14 ore: si resta su sensore simulato e dati pubblici. Webcam e telemetro laser servono alle prove, non al nucleo.
4. **Il sensore resta a casa?** È uno strumento di **registrazione**, non di demo dal vivo (§3).

## 2. La tabella per famiglia

Limiti geometrici ricalcolati con `geometria_sensori.py` per il montaggio del nucleo (1,2 m, 15° in basso): «suolo da» = distanza da cui il pavimento è in campo (nel nucleo 1,24 m); «settori» = gradi orizzontali (nel nucleo 87). Reg. (uso da remoto): **R** = ramo pronto in `registra_sequenza.py`; **C** = convertitore pronto; **S** = da scrivere, 30–60 min.

| Famiglia | (1) Dà al nucleo | (2) Cambia nei limiti | (3) Su Linux; primo fotogramma (stima) | Reg. | (5) Priorità |
|---|---|---|---|---|---|
| **RealSense D435, D435i, D455, D415** | sorgente principale: è il sensore di progetto | niente (87°×58°, suolo da 1,24 m) | `pip install pyrealsense2` 2.59.1, cp39–cp314, Apache 2.0 [1]; cavo USB 3; regola udev (`sudo`, una volta, a casa); kernel dichiarati fino al 6.14 [2]. 15–30 min | R | **14 ore, prima scelta** |
| **Orbbec Gemini 33x / 2, Astra 2, Femto Bolt / Mega** | sorgente principale | Gemini 335: 90°×65°, suolo da 1,10 m. Femto (tempo di volo): 75°×65°, 0,5–3,86 m, o 120°×120° con suolo da 0,32 m ma portata 2,88 m; solo interni | `pip install pyorbbecsdk2` 2.1.3, cp38–cp314; regole udev [3]. 20–40 min | R | **14 ore** |
| **OAK-D Pro; OAK-D, OAK-D Lite** | sorgente principale (Pro); con riserva le altre | Pro 80°×55°, suolo da 1,31 m; OAK-D 72°×49°, 1,46 m; Lite 73°×58°, 1,24 m. OAK-D e Lite **senza proiettore** [4]: buchi attesi su parete e pannello uniformi (non verificato) | `pip install depthai` 3.12.1, MIT [5]; regola udev; cavo USB 3; alimentazione esterna raccomandata [4]. 20–40 min | R | **14 ore** (Pro) |
| **RealSense L515** (SR300, D405, T265: no) | sorgente principale al chiuso | 70°×55°, suolo da 1,31 m, 0,25–9 m (m) | fuori produzione: `pyrealsense2==2.54.2.5684`, «supports but not validated» [2], solo cp37–cp311 [1]. 30–60 min | R | 14 ore se è l'unica |
| **Kinect v1** (Xbox 360) | sorgente principale | 57°×43°, da 0,8 m [6]: **suolo da 1,62 m**, a 3 m vede fino a 1,54 m di quota, 57 settori; solo interni (m) | `libfreenect` v0.6.4 (2022), AUR o compilazione; modo `DEPTH_MM`: uint16 in mm, 0 = nessun dato [7]; **serve il suo alimentatore** [6]. 1–2 ore | S | 14 ore se è l'unica |
| **Azure Kinect DK** | sorgente principale | come Femto Bolt [8] | SDK archiviato il 22-8-2024, pacchetti solo per Ubuntu 18.04, motore chiuso [9]; alimentatore. 1–3 ore, può fallire | S | raffinamento |
| **Kinect v2** (Xbox One) | sorgente principale, a rischio | 70°×60°, 0,5–4,5 m (m); suolo da 1,20 m | `libfreenect2` v0.2.1 (2021); controllore USB 3 Intel o NEC, ASMedia no, niente macchine virtuali [10]; compilazione. 2–4 ore | S | raffinamento, o no |
| **Orbbec Astra prima serie** | sorgente di ripiego | 58,4°×45,5°, 0,6–8 m, USB 2 [11]: suolo da 1,55 m | l'SDK v2 non supporta Astra+ e Pro Plus; le Mini Pro solo dopo un **aggiornamento del firmware** [3]: non si fa (scrittura sul dispositivo senza ritorno provato) → SDK v1. 1–2 ore | S | 14 ore se è l'unica |
| **iPhone / iPad con LiDAR** | profondità vera **registrata**; dal vivo solo con un'app a pagamento [12] (serve il sì dell'utente) | 256×192, 60 fps [13]: circa 41 pixel su una persona a 3 m (se il campo è 60°: ipotesi); telefono fermo su un supporto; bordi ricostruiti dal telefono (m) | Stray Scanner, gratuita: PNG a 16 bit in mm, tempi e intrinseche per fotogramma [13]. 15 min | C | **14 ore: dati**, non demo |
| **Webcam, moduli camera** (Raspberry Pi, ESP32) | etichetta persona / non persona; **video di verità** dietro il pannello | niente: senza profondità misurata non nasce nessun «libero» | UVC. 5 min | — | verità: 14 ore; etichetta: raffinamento |
| **VL53 multizona** (L5CX, L7CX, L8CX); a punto singolo; ultrasuoni | canale laterale di sola prossimità, mai «libero» | i multizona coprono parte dell'anello cieco (2 m al buio, 0,5 m a 5 klx) [14] | solo I2C [14]: microcontrollore più firmware. 1–2 ore | S | multizona: raffinamento, se il firmware gira già; gli altri: no |
| **LiDAR 2D; telemetro laser** | LiDAR: non è una sorgente (un piano solo, non vede il pavimento: nessun «libero»); è una **verità da un secondo punto di vista**. Telemetro: il metro delle prove | niente | SDK Slamtec (BSD) [15], LD19 [16]; seriale USB. 30–60 min | S | telemetro: subito; LiDAR: raffinamento |
| **Radar a onde millimetriche** | LD2410: presenza a porte di 0,75 m, **nessun angolo** [17]: niente. LD2450: 3 bersagli con x, y, ±60°, 6 m [18]: vedi embedded-2 | niente | seriale a 256000 baud. 30–60 min | S | no |
| **Unità inerziale** | «il sensore si è mosso» per le camere senza IMU; inclinazione per `meta.json` | niente; non rende valido il sensore in moto | microcontrollore. 30–60 min | S | raffinamento |
| **Raspberry Pi, Jetson** | ospite di cattura a casa; banco per i cicli al secondo | niente | ruote aarch64 [1][3][5]; USB del Pi: 1,2 A in tutto [4] | — | no nelle 14 ore |

Telefoni Android con sensore di profondità: nessuna app verificata → no.

## 3. Da remoto, e la demo

- **Registrare e spedire (la via da usare).** `registra_sequenza.py` scrive il formato comune e lo controlla. Le sequenze del §4 pesano 2,4 GB grezzi (3900 fotogrammi da 0,61 MB) e **circa 1,4 GB impacchettate, se vale il 58 % misurato su dati sintetici** (su profondità vera: non misurato): 9 minuti d'invio a 20 Mbit/s (banda dell'utente: non verificata).
- **Flusso in rete.** Senza perdita, a 640×480 e 15 fps: **42,6 Mbit/s** (zlib 3; 6,0 ms per comprimere, 1,4 per aprire); 15,8 a metà risoluzione. Misura su sintetico (E12). Ritardo di rete: non misurato. La latenza dalla cattura al suono attraverso Internet non è dimostrabile: non si costruisce nelle 14 ore.
- **Demo.** Con il sensore a casa restano: (a) la **riproduzione** in tempo reale delle sequenze attraverso la stessa catena, dichiarata come tale (è già il modo d'accettazione del nucleo); (b) la catena sul calcolatore di casa con lo schermo condiviso: latenza misurata là, utente fuori sala. Una demo in sala chiede un sensore **in sala**.

## 4. Per l'utente: dieci minuti di registrazione

**Prima.** `pip install numpy` e il pacchetto del sensore. Sensore fermo, ottica a **1,20 m** da terra, **15° in basso** (inclinometro del telefono): passa al comando i valori veri. Nastro a terra a 1, 2, 3 m dalla lente; 4 m di pavimento sgombro.

Comando: `python registra_sequenza.py registra --sorgente realsense --altezza-camera 1.20 --inclinazione 15 --scena "…" --uscita NOME --durata S` (per le sequenze da 30 e 90 s aggiungi `--fps 15`; se il sensore lo rifiuta, toglilo). Parte dopo 1–2 secondi, si ferma da solo e deve finire con «conforme». Provalo prima con `--durata 3`.

| Nome | Durata | Che cosa fare |
|---|---|---|
| `parete_1m`, `_2m`, `_3m` | 5 s l'una | Parete chiara con la lente a 1,00, 2,00, 3,00 m misurati; nessuno in campo. La «distanza al centro» stampata deve valere circa la distanza × 1,035 |
| `passa_dietro` | 90 s | Pannello opaco alto ≥ 1,5 m e largo 1 m, a 1,5 m dal sensore. Cammina su una linea a 2,0–2,3 m, passando dietro il pannello: **10 passaggi**, alternando il verso |
| `ferma_dietro` | 90 s | Uguale, ma dietro il pannello ti fermi: 5 volte per 3–8 s, una per 12 s; due volte torni indietro |
| `mano` | 30 s | Scena vuota; a 10 s e a 20 s copri la lente con la mano per 3 s |
| `vetro_fronte`, `vetro_45` | 5 s l'una | Porta a vetri chiusa a 1,5 m, di fronte e a 45° |

Annota le misure vere (distanze, posizione del pannello, durata delle soste); se puoi, un telefono riprende da dietro il pannello. Poi `python registra_sequenza.py impacchetta NOME` e manda i `.tar.gz` con il mezzo che la squadra usa già. Con iPhone o iPad: stesse scene con Stray Scanner, telefono fermo; converte la squadra (`converti-stray`).

## 5. Modulo d'inventario (una riga per dispositivo)

`modello esatto (etichetta) | codice USB (lsusb o Gestione dispositivi) | cavo dati: USB 2 o 3 | alimentatore: c'è? | supporto o treppiede | modulo nudo: su quale scheda, il firmware gira? | calcolatore a cui è collegato: sistema e versione, porte USB 3, Python, diritti d'amministratore | funzionava l'ultima volta?`

Una volta sola: banda in salita; pannello ≥ 1,5 × 1 m, porta a vetri, 4 m di pavimento libero; il sensore si può portare in sala?; iPhone Pro o iPad Pro fra i cinque?

## 6. Critiche, stati, proposte

1. **Il sensore a casa non dà una demo dal vivo** (§3). Stato: **non risolto** (lo decidono la banda vera e la compressione su profondità vera); nel piano vale come no.
2. **Solo le prime nove righe possono alimentare il nucleo**: «libero» chiede il pavimento visto. Kinect v1 e Astra spostano l'anello cieco da 1,24 a 1,55–1,62 m: la zona di valutazione va scritta per sensore (calcolo, non misura).
3. **`registra_sequenza.py`**: formato **verificato** sull'insieme dichiarato (2 sequenze accettate, 4 difettose respinte, da due controlli di autori diversi); nomi delle funzioni verificati sui pacchetti installati; registrazione da un dispositivo vero: **non verificata**.

**embedded-1. Il telefono di un membro come prima profondità vera.** Previsione (16:13): la prima registrazione convertita passa `controlla_sequenza.py` senza errori e dà ≥ 30 pixel su una persona a 3 m. La smentisce: un errore di formato, o meno di 20 pixel.
**embedded-2. Radar LD2450 come testimone dietro il pannello** (solo se c'è). Meccanismo: i 24 GHz attraversano i pannelli sottili non metallici (m). Previsione: vede la persona dietro un cartone a 2 m in ≥ 8 passaggi su 10, entro 0,5 m. La smentisce: < 5 su 10.

**Dopo.** Chiedere **ora** ai cinque del telefono. All'arrivo dell'inventario: una riga della tabella, il primo fotogramma, poi il §4.

**Fonti (aperte oggi).** [1] https://pypi.org/pypi/pyrealsense2/json · [2] https://github.com/realsenseai/librealsense/releases (v2.59.1, v2.55.1, v2.54.2) · [3] https://github.com/orbbec/OrbbecSDK_v2 · [4] https://docs.luxonis.com/hardware/platform/deploy/usb-deployment-guide/ e `/hardware/products/OAK-D` · [5] https://pypi.org/pypi/depthai/json · [6] https://en.wikipedia.org/wiki/Kinect (secondaria) · [7] https://github.com/OpenKinect/libfreenect · [8] https://learn.microsoft.com/en-us/previous-versions/azure/kinect-dk/hardware-specification · [9] https://github.com/microsoft/Azure-Kinect-Sensor-SDK · [10] https://github.com/OpenKinect/libfreenect2 · [11] https://www.orbbec.com/products/structured-light-camera/astra-series/ · [12] https://record3d.app/features (in riassunto) · [13] https://github.com/strayrobots/scanner/blob/main/docs/format.md · [14] `../../f3/fonti/FONTI_VERIFICATE.md` · [15] https://github.com/Slamtec/rplidar_sdk · [16] https://github.com/ldrobotSensorTeam/ldlidar_stl_sdk · [17] https://www.sudo.is/docs/esphome/components/ld2410/HLK-LD2410_Serial_Communication_Protocol_v1.02.pdf · [18] https://www.elemon.com.ar/images/productos/hojas-de-datos/radar-modulos/hlk-ld2450.pdf
