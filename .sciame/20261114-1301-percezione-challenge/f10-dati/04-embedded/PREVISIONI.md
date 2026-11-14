# Previsioni — `sciame-embedded`, f10, tabella per l'inventario dei sensori

Scritte alle **2026-11-14T15:57:59+01:00** (`date -Is`), **prima** di aprire qualunque pagina in rete e prima di
scrivere o eseguire qualunque script. Fino a questo momento ho letto solo: `CONTRATTO_DATI.md`,
`ADDENDUM_UTENTE.md`, `SOLUZIONE_V2.md`, `f3/fonti/FONTI_VERIFICATE.md`, `f1/985ccd9bca46/CONSEGNA.md`,
`regole_challenge.md`. Le previsioni vengono dalla mia memoria (modello linguistico, conoscenza fino a metà 2026):
è proprio ciò che la verifica in rete deve controllare.

Esiti possibili: **regge**, **smentita**, **non risolta** (pagina non raggiunta o dato assente).

| # | Previsione | Misura | Soglia di smentita |
|---|---|---|---|
| E1 | Kinect v1: `libfreenect` (OpenKinect) esiste ancora, non archiviato; ultima versione pubblicata della serie 0.7.x, non più recente del 2024 | pagina delle versioni su GitHub | deposito archiviato o sparito; oppure una versione del 2026 |
| E2 | Kinect v2: `libfreenect2` non ha versioni dopo il 2017 (0.2.x); richiede un controllore USB 3 | pagina delle versioni e README | una versione successiva al 2020 |
| E3 | Azure Kinect: produzione cessata (annuncio 2023); ultimo SDK 1.4.2; pacchetti ufficiali solo per Ubuntu 18.04 (20.04 non ufficiale) | deposito Microsoft, pagina delle versioni e documento d'uso | versione ≥ 1.5 o pacchetti ufficiali per Ubuntu 22.04/24.04 |
| E4 | RealSense L515 e SR300: tolti dal ramo corrente di `librealsense`; l'ultima versione che li supporta è la 2.54.x; la serie D400 è supportata nella versione corrente | note di versione di `librealsense` | la versione corrente elenca L515 fra i dispositivi supportati |
| E5 | `pyrealsense2` su PyPI NON ha una ruota per Python 3.14 (quello di questa macchina): serve Python ≤ 3.13 | pagina dei file su PyPI | ruota `cp314` presente |
| E6 | Orbbec Astra (prima serie, protocollo OpenNI): non supportata dall'Orbbec SDK v2, serve l'SDK v1 o OpenNI2; Femto Bolt/Mega e Gemini 2/33x supportate dalla v2 | README di `OrbbecSDK_v2` | Astra (non «Astra 2») elencata come supportata dalla v2 senza condizioni |
| E7 | OAK-D: `depthai` si installa con `pip`, è alla versione 3.x, licenza MIT; su Linux chiede una regola udev (quindi `sudo`, una volta, sul calcolatore a cui è collegata) | documentazione Luxonis e PyPI | versione corrente < 3; nessuna regola udev richiesta |
| E8 | iPhone/iPad con LiDAR: l'app Record3D dà profondità 256×192 e un flusso via USB con una libreria Python; l'esportazione completa è a pagamento | pagina dell'app e deposito | risoluzione di profondità ≥ 640×480 nativa |
| E9 | Radar da presenza HLK-LD2410: seriale a 256000 baud, dà distanza di bersaglio fermo e in moto, **nessun angolo**; LD2450: fino a 3 bersagli con x, y | scheda o manuale del protocollo | LD2410 con uscita angolare |
| E10 | VL53L5CX/L7CX/L8CX: nessuna interfaccia USB; servono un microcontrollore o un Raspberry Pi (I2C) | scheda ST già scaricata (`f9-preproposta/07-lidar/scaricati/`) | scheda che dichiara USB |
| E11 | Kinect v1 nel kernel Linux: esiste il modulo `gspca_kinect` (solo video/IR, niente profondità in millimetri): per la profondità serve comunque `libfreenect` | sorgente del kernel o documentazione | il modulo dà la profondità registrata in mm |
| E12 | Flusso remoto: una profondità 640×480 a 16 bit, 15 fps, compressa senza perdita (PNG o zlib) sta sotto 3 MB/s (24 Mbit/s) su scena d'interno; non compressa sono 9,2 MB/s (conto: 640·480·2·15) | misura mia su una profondità sintetica con rumore (se l'ambiente Python con numpy è disponibile), dichiarata come sintetica | > 6 MB/s compressa |
| E13 | Lo script di registrazione che scriverò produce una sequenza conforme al formato comune al primo controllo (meta.json con tutte le chiavi, tempi.csv, `profondita/NNNNNN.npy` uint16 in mm) | controllo automatico su una sequenza sintetica | una chiave mancante, un tipo diverso da uint16, tempi non crescenti |

**Braccio che deve fallire (per E13):** il controllo di conformità, dato in pasto a una sequenza volutamente
sbagliata (float32 in metri), deve dire «non conforme». Se la accetta, il controllo è cieco.

**Che cosa NON prevedo perché non lo so:** lo stato di RealSense come società dopo lo scorporo da Intel (so di
`realsenseai.com` solo da `FONTI_VERIFICATE.md`); la versione corrente esatta di ogni SDK; i prezzi.

## Esiti

Verifiche fatte fra le 15:58:37 e le 16:09:00 del 14 novembre 2026 (`date -Is` dopo ogni blocco di comandi).
**[g]** = testo grezzo scaricato con `curl` e cercato con `grep` o con Python; **[r]** = letto con lo strumento
che riassume la pagina (più debole). I file scaricati stanno nella cartella temporanea della sessione
(`…/scratchpad/web/`), non in `scaricati/`, che il compito non mi assegna: si rifanno dai link.

| # | Esito | Che cosa ho trovato | Fonte (aperta oggi) |
|---|---|---|---|
| E1 | **regge con una correzione** | `libfreenect` non archiviato, ultimo invio 2024-08-05, ultima versione **v0.6.4 del 2022-09-20** (avevo scritto «serie 0.7.x»: sbagliato il numero). Licenza Apache 2.0 / GPL 2. Pacchetto nell'AUR per Arch; regole udev da installare | API GitHub `repos/OpenKinect/libfreenect` e `/releases` [g]; README [g] |
| E2 | **smentita** | `libfreenect2`: l'ultima versione è la **v0.2.1 del 2021-08-06**, oltre la soglia che avevo fissato (2020). Resta vero: «USB 3.0 controller. USB 2 is not supported»; «Intel and NEC… known to work. ASMedia… known to not work»; «Virtual machines likely do not work» | https://github.com/OpenKinect/libfreenect2/releases/tag/v0.2.1 [g]; README [g] |
| E3 | **regge** | Deposito Microsoft «archived by the owner on Aug 22, 2024», ultima versione v1.4.2; `docs/usage.md`: «debian packages available for Ubuntu 18.04»; motore di profondità a sorgente chiuso. Fine della produzione annunciata il 17 agosto 2023 (vendite fino a ottobre) [r, ricerca] | https://github.com/microsoft/Azure-Kinect-Sensor-SDK/releases [g]; `docs/usage.md` [g] |
| E4 | **regge** | Note della v2.59.1 (2026-10-11): «L515 … v2.50.0 validated, v2.54.2 supports but not validated»; note della v2.55.1: «SDK version 2.54.2 supported the cameras but was not validated». Il deposito ora è `realsenseai/librealsense` (reindirizzamento). La v2.59.1 dichiara Ubuntu 20.04–26.04 e kernel fino al 6.14: **il 7.3 di questa macchina non è in elenco** | https://github.com/realsenseai/librealsense/releases/tag/v2.59.1 e `/v2.55.1`, `/v2.54.2` [g] |
| E5 | **smentita** (buona notizia) | `pyrealsense2` 2.59.1.11053 su PyPI ha ruote cp39–**cp314**, Linux x86_64 e aarch64, Windows. Per l'L515: `pyrealsense2==2.54.2.5684` ha ruote solo cp37–cp311 | https://pypi.org/pypi/pyrealsense2/json [g] |
| E6 | **regge con una precisazione** | README dell'SDK v2: Astra+ e Astra Pro Plus «not supported» dalla v2 (solo v1, «limited maintenance»); Astra 2, Femto Bolt/Mega, Gemini 2 e 33x supportate; **Astra Mini Pro / Mini S Pro supportate dalla v2 solo dopo l'aggiornamento del firmware da 1.x a 2.x** (cambio di protocollo da OpenNI a UVC: è una scrittura sul dispositivo). La prima Astra «senza suffisso» **non compare** nella tabella: non verificato. SDK v2 v2.10.6; `pyorbbecsdk2` 2.1.3 con ruote cp38–cp314 | https://github.com/orbbec/OrbbecSDK_v2 (README) [g]; https://pypi.org/pypi/pyorbbecsdk2/json [g] |
| E7 | **regge** | `depthai` 3.12.1 (2026-11-11), MIT, ruote cp39–cp315 per Linux, macOS, Windows. Regola udev con `sudo` per il produttore `03e7`; «Use a USB3 USB-C cable»; alimentazione esterna raccomandata (500–900 mA; i modelli Pro fino a 15 W di picco); con cavo o porta USB 2 si forza `maxUsbSpeed=dai.UsbSpeed.HIGH` | https://pypi.org/pypi/depthai/json [g]; https://docs.luxonis.com/hardware/platform/deploy/usb-deployment-guide/ [g] |
| E8 | **regge per la risoluzione, da un'altra fonte** | Stray Scanner (app gratuita): profondità PNG a 16 bit in millimetri, **256 × 192**, con tempi e intrinseche per fotogramma. Record3D: flusso via USB solo dopo l'acquisto; il flusso Wi-Fi è un'estensione a pagamento, solo in rete locale e con compressione con perdita [r]; la sua risoluzione non l'ho trovata | https://github.com/strayrobots/scanner/blob/main/docs/format.md [g]; https://record3d.app/features [r] |
| E9 | **regge** | LD2410: «default baud rate of the serial port is 256000»; nel manuale del protocollo la parola «angle» compare 0 volte (stato del bersaglio, distanza del bersaglio in moto e di quello fermo, energia; porte di distanza da 0,75 m). LD2450: fino a tre bersagli con x, y in mm e velocità, ±60° in azimut, 6 m | manuali Hi-Link v1.02 e LD2450 v1.00, copie su sudo.is e elemon.com.ar [g, `pdftotext`] |
| E10 | **regge** | Schede VL53L7CX e VL53L8CX: la parola «USB» compare 0 volte; interfaccia I2C (indirizzo 0x52) | `f9-preproposta/07-lidar/scaricati/vl53l7cx_ds.txt`, `vl53l8cx_ds.txt` [g] |
| E11 | **regge** | `drivers/media/usb/gspca/kinect.c` del kernel: modo di profondità `V4L2_PIX_FMT_Y10BPACK` (valori grezzi a 10 bit impacchettati, non millimetri) dietro il parametro `depth_mode` | https://raw.githubusercontent.com/torvalds/linux/master/drivers/media/usb/gspca/kinect.c [g] |
| E12 | **non regge; smentita al livello 1, sotto la soglia al livello 3** | Su una sequenza **sintetica** (640×480, rumore 4 mm·z², 3 % di buchi, 45 fotogrammi): grezzo 9,22 MB/s a 15 fps; zlib livello 1: 7,50 MB/s (60 Mbit/s); zlib livello 3: **5,32 MB/s (42,6 Mbit/s)**, 6,0 ms a fotogramma per comprimere e 1,4 ms per aprire; PNG a 16 bit: 5,62 MB/s; metà risoluzione più zlib: 1,97 MB/s (15,8 Mbit/s). La previsione «sotto 3 MB/s» è falsa su questi dati; ho sbagliato a lasciare una fascia fra la previsione (3) e la soglia (6). Su profondità vera: **non misurato** (nessun dato vero era ancora in `scaricati/`) | `misura_codec.py` nella cartella temporanea, su `registra_sequenza.py sintetica` (uscita riportata qui) |
| E13 | **regge** | `sintetica` → «conforme» al primo controllo; i quattro bracci che devono fallire falliscono tutti (float32 in metri; un fotogramma mancante; chiave `fx` tolta; due righe di `tempi.csv` scambiate): codice d'uscita 1 su 4 su 4. Il convertitore di Stray Scanner dà una sequenza conforme su una cartella **finta** costruita secondo la documentazione dell'app (mai su una registrazione vera) | `registra_sequenza.py` con l'interprete di `f10-dati/ambiente/venv`, ore 16:05:58–16:06:32 |

## Controllo incrociato del formato (16:10:09)

`03-infrastruttura/controlla_sequenza.py --rigoroso --tutti` (altro autore, altro codice, stessa specifica) sulle
mie sequenze: `sintetica` → «rispetta il formato (0 errori, 0 avvisi)»; le quattro difettose → codice 1 su 4 su 4,
con lo stesso motivo trovato dal mio controllo; la sequenza senza intestazione in `tempi.csv` → un avviso (per
questo l'intestazione resta il valore predefinito); la conversione della cartella finta di Stray Scanner → 0
errori e un avviso giusto (la scena finta è una parete a 2 m senza pavimento, incompatibile con la posa
dichiarata). All'inverso, il mio `controlla` accetta `03-infrastruttura/esempio_sequenza`. I nomi delle chiavi
che avevo scelto coincidono con quelli del controllo di riferimento (`CHIAVI_META`, `CHIAVI_POSA`).

## Previsione nuova, scritta alle 2026-11-14T16:13:20+01:00 (non ancora provata)

**embedded-1.** La prima registrazione vera di Stray Scanner (iPhone o iPad con LiDAR), convertita con
`registra_sequenza.py converti-stray`, passa `controlla_sequenza.py` senza errori e dà almeno 30 pixel di
larghezza su una persona a 3 m. Smentita: un errore di formato, oppure meno di 20 pixel. Non risolta: fra 20 e 30,
o nessun telefono adatto nella squadra.

## Scostamenti dalle regole, per esteso

1. Tre pacchetti PyPI (`pyrealsense2`, `depthai`, `pyorbbecsdk2`, con le loro dipendenze) installati con `uv pip`
   in un ambiente nella cartella temporanea della sessione, fuori da `f10-dati/ambiente/`; importati una volta per
   leggere i nomi delle funzioni; ambiente e cache cancellati alle 16:11.
2. Pagine, README e due manuali PDF scaricati nella cartella temporanea della sessione, non in `scaricati/`
   (il compito non me la assegna); letti con `grep`, `pdftotext` e Python, mai eseguiti.
3. Letti, senza scrivere, `03-infrastruttura/` (controllo e sequenza d'esempio) e l'interprete di
   `ambiente/venv`.
4. Alle 15:58 l'API pubblica di GitHub ha risposto «rate limit exceeded» per l'indirizzo di questa macchina
   (in comune con gli altri ruoli) a 15 dei miei 16 depositi: ho ripiegato sulle pagine HTML delle versioni.
5. E12: fascia lasciata fra la previsione (3 MB/s) e la soglia di smentita (6 MB/s).

## Che cosa ho notato dopo (non era previsto)

- `libfreenect` (Kinect v1) offre il modo `FREENECT_DEPTH_MM`: uint16 in millimetri, 0 = nessun dato
  (`include/libfreenect.h`, righe 44–47, e `wrappers/python/freenect.pyx`) [g]: coincide con il formato comune.

- I tre pacchetti dei sensori (`pyrealsense2` 2.59.1, `depthai` 3.12.1, `pyorbbecsdk2` 2.1.3) si installano con
  `uv pip` su Python 3.14 in un ambiente temporaneo (858 MB, poi cancellato) e **ogni funzione che
  `registra_sequenza.py` chiama esiste** con la firma attesa (controllo con `hasattr` e con le stringhe di
  documentazione, 0 dispositivi collegati). Non è una prova che la registrazione funzioni.
- `pyorbbecsdk2` si porta dietro `pygame-ce`, `pynput`, `opencv-python`: pesante per un calcolatore piccolo.
- `record3d` (libreria Python per il flusso USB dell'iPhone) ha ruote solo fino a cp313 e su Linux chiede
  `libusbmuxd`; `pyk4a` 1.5.0 (2023) è solo sorgente.
- Campo e distanza minima del Kinect v1 (57° × 43°, circa 0,8 m): Wikipedia, testo grezzo [g], fonte secondaria.
  Campo dell'Astra (58,4° × 45,5°, 0,6–8 m, USB 2.0) e dell'OAK-D (72° × 49°; Pro 80° × 55°; Lite 73° × 58°;
  base 7,5 cm; proiettore solo sulla Pro): pagine dei costruttori [g]. Azure Kinect, campo stretto 640×576,
  75° × 65°, 0,5–3,86 m: pagina Microsoft [g].
- **Non verificati oggi (memoria):** campo e portata del Kinect v2 (70° × 60°, 0,5–4,5 m) e dell'L515
  (70° × 55°, 0,25–9 m, solo al chiuso); il campo del LiDAR di iPhone e iPad; il rumore del Kinect v1; tutte le
  cifre su ultrasuoni, VL53L0X/L1X e unità inerziali; tutti i «tempi al primo fotogramma» (stime mie).
- Il formato comune non fissa i **nomi delle chiavi** di `meta.json` né dice se `tempi.csv` ha una riga
  d'intestazione: nessun altro ruolo li aveva ancora scritti quando ho controllato (16:03). Ho scelto i nomi alla
  lettera dal testo del compito e li ho messi in una sola tabella in testa allo script.
