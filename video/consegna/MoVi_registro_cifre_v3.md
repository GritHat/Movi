# MoVi, registro delle cifre del video v3 finale

Ogni cifra che il video dice o scrive, con il suo stato e la sua fonte. Le cifre a schermo vengono **solo** da
`video/progetto_v3/cifre_finale.json`, generato da `strumenti/cifre_finale.py` copiando senza modifiche il blocco JSON del
verdetto finale (`.sciame/20261114-1301-percezione-challenge/f20-chiusura/20-verdetto/VERDETTO_FINALE.md` § 8). Lo script
controlla che ogni numero dello schermo stia nel blocco della stessa chiave (o, per 4 chiavi, nel testo del verdetto § 2 o
§ 8 di quella chiave: indicato sotto).

Stati: **dim** dimostrato nel modello · **calc** calcolato · **sim** simulato · **pub** su dati pubblici con un sensore
simulato · **ip** ipotesi. Intervalli: Wilson al 95 % **per passaggio**; dove si dice «casi», i casi sono correlati dentro
un mezzo e l'intervallo è ottimista. Nessuna cifra è «validata»; nessuna viene da un sensore fisico o da hardware.

## 1. Cifre del blocco del verdetto

| Chiave | Scena | Voce (EN) | Schermo | Intervallo | Classe | Stato | Fonte |
|---|---|---|---|---|---|---|---|
| V-1 | s3 | «never said clear… in six flight scenarios» | 0 «clear» | F6 0/200 [0; 0,019]; altre celle 0/60 [0; 0,060] | S | sim | `f19-volo/10-prove/passaggi_volo_v3i.jsonl`; `f20/20-verdetto/riconto_finale.txt` |
| V-2 | s4 | «within one second, in sixty of sixty simulated runs» | 60/60 | [0,940; 1] | I (innesco ottimista, scritto) | sim | VERDETTO_FINALE § 2.1 V-2 |
| V-3 | s4 | «fifty-eight of sixty» | 58/60 | [0,886; 0,991] | I | sim | § 2.1 V-3 |
| V-5 | s5 | «at least ten seconds ahead, in sixty of sixty runs» | 60/60, ≥ 10 s; «10 s threshold set after» | [0,940; 1] | I | sim | § 2.1 V-5 |
| V-6 | s5 | «the fragments stayed inside it in every simulated run» | 60/60; 939/939 campioni | [0,940; 1] | S (copertura) | sim | § 2.1 V-6 |
| V-11-PROVA | s5 (riga piccola grigia) | — | 57/60; 2/60 falsi eventi; «not adopted» | [0,863; 0,983]; [0,009; 0,114] | **L** | sim | `f20/01-contatto/CONTATTO.md`; § 2.1 V-11 (i due intervalli sono nel testo di V-11 e nel § 8, s5) |
| V-10 | s6 | «Radar alone keeps a region for every track, and identity is presumed» | 60/60 | [0,940; 1] | S (regione); identità presunta | sim | § 2.1 V-10 |
| C-TAR-1-2 | s7 | — | 0,89 (655/733) | [0,87; 0,91] casi correlati | I | pub | `f20/02-taratura/TARATURA.md` § 3 |
| C-TAR-BANDA | s7 | «eighty-five to eighty-nine times in a hundred, from one to thirty seconds» | 0,85–0,89; 21–30 s 0,85; 89,5 % dei casi da 4 voli di una rotta | 21–30 s [0,81; 0,88] | I | pub | VERDETTO_FINALE § 4; ATTACCO_FINALE § 4 |
| C-TAR-VIRATA | s7, s10 | «In turns, seventy-three: a declared limit» | 0,73 (161/221) | [0,67; 0,78] | **L** | pub | TARATURA § 3 |
| F7-CAM | s8 | «The cameras are declared unreliable» | 0 cicli saturi «affidabili»; falsi eventi 0/200 «without clustered clutter» | [0; 0,019] | S (innesco ottimista; controllo debole) | sim | `riconto_finale.txt` F7c |
| F7-VOL | s8 | — | 60/60 per cella; «in the model» | [0,940; 1] | S nel modello | sim, dim nel modello | `riconto_finale.txt`; `conteggi_attacco_f7.txt` |
| F7-CONT | s8 | «In sixty of sixty simulated runs, the tracked drone stayed inside its region» | 60/60 per geometria ×4, «360-degree radar, not blinded» | [0,940; 1] | S | sim | `f20/05-scorta/passaggi_valutazione.jsonl`; `riconto_finale.txt` |
| F7-LIBERO | s8 | «no fragment was ever called clear» | 0/60 per cella | [0; 0,060] | S | sim | `riconto_finale.txt` |
| F7-ID | s8 | — | 0/60; identità «presumed, doubtful» | [0; 0,060] | S | sim | `riconto_finale.txt` |
| F7R-CIECO | s8 | «Even with the radar blinded for up to two seconds, MoVi never called a fragment clear» | 0/60 «clear»; regione 59–60/60, peggiore 59/60 | [0; 0,060]; [0,911; 0,997] | S, modello di cecità pessimista | sim, ip | `f20/05-scorta/ACCECAMENTO_RADAR.md`; `riconto_f7r.txt` |
| F7-LIM-FRONTALE | s8 (riga rossa) | — | radar solo frontale: urto di lato/dietro visto 1/60 e 0/60; identità in virata 43/60 | [0,592; 0,815] | **L** | sim | `riconto_finale.txt` F7 att (1/60 e 0/60 sono nel valore del blocco) |
| LP-1 | s9 | «warned in time in two hundred of two hundred runs» | 200/200 | [0,981; 1] | S | sim | `f15-lunga-portata/60-fase2c/02-verdetto/VERDETTO_2C.md` |
| LP-4 | s9 | — | 200/200 con tre sensori fusi | [0,981; 1] | S | sim | VERDETTO_2C (intervallo dal § 2.3 del verdetto finale) |
| HW-CALC | s10 | «dedicated hardware» (senza cifre) | 0,08–1,2 ms, «estimate by analogy, not a measurement» | intervallo di stime | — | **ip** | `f19-volo/02-sensori-hw/latenza.json` (non ricontato dall'arbitro) |

## 2. Numeri a schermo che non sono cifre del blocco (dati di file, dichiarati)

| Dove | Che cosa | Stato | Fonte |
|---|---|---|---|
| s1, s3–s6 | `t = … s`, «NOT SEEN · x s · region r m»: lettura del registro del passaggio 0, idx 0, configurazione sda | sim (un passaggio) | `prototipo/uscite/video_volo/registro_F1/F3/F4/F5.jsonl` |
| s1, s3–s6, s8 | «playback ×N (accelerated/slowed)»: rapporto fra tempo del registro e tempo del video | montaggio | `tempi/scene_finale_en.js` |
| s4–s6 | titoli «135 m/s», «40 and 35 m/s»: velocità degli scenari | sim (parametri) | INDICE.md dei registri |
| s7 | curva C(τ) con sfera di 150 m e r0,9(τ) da 35 a 177 m; punti per fascia (0,89 ×4, 0,85) con Wilson | calc (curva); pub (punti) | `f20/02-taratura/curva_video.json` (`aereo_210`, `banda_osservata_copertura_0_9`) |
| s7 | «aircraft at 210 m/s, straight line: the most favourable case» | calc | curva_video.json; avvertenza di TARATURA § 4 |
| s8 | `t`, «NOT SEEN x s · region r m», barra della confidenza (C del registro, senza numero), stato dei sensori, volume dei detriti | sim (un passaggio, F7r davanti, idx 0) | `registro_F7r_davanti.jsonl` (0 violazioni di `convalida_volo.py`) |
| s9 | «drone at 15–21 m/s» | sim | VERDETTO_FINALE § 2.3 LP-1 |

## 3. Cifre tolte rispetto alla bozza (non nel blocco o «da non dire»)

V-4 (margine all'operatore), V-7, V-12, F1-AVVISO, F4-IMPRONTA (6,8 km), «16 s in this run», CONF-REALI (0,71 / 0,92–0,98,
«16 real aircraft»), CONF-ESEMPIO, LAT-BARRE (700, 620, 170 ms), LAT-CPU, LAT-ANALOGIA (74×, 8,4×), LP-2, LP-11, «for three
seconds» in F5, «within three cycles» in F4, il ritardo dell'evento in F7 e l'istante dell'evento nella console di F4.
