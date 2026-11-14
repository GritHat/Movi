# Sezione D — Sensori e hardware

*Bozza di `sciame-sensori` per `STATO_PROGETTO.md` (fase f11). Fotografia dei file alle 16:16 del 14 novembre 2026. Percorsi relativi alla cartella della convocazione.*

**Avvertenza per tutta la sezione.** Nessun sensore è mai stato acceso e nessun fotogramma di una camera vera è stato elaborato (`VER` §5, punto 10). Ogni cifra è una **dichiarazione del costruttore**, un **conto** su quelle dichiarazioni, o un risultato **in simulazione a sensore fermo**: nessuna è misurata su un esemplare della squadra.

**Come leggere.** *Stati:* dimostrato (in un modello), verificato (controllo esaustivo su un insieme dichiarato), sostenuto dai dati (in simulazione), smentito, non risolto, non verificato fino all'hardware, **non vagliato** (viene dalle estensioni f9–f10, che l'arbitro non ha ancora giudicato). *Lettura delle fonti esterne:* **[g]** dato cercato nel testo scaricato; **[r]** letto con uno strumento che riassume; **(r)** visto solo nel riassunto di una ricerca. *Marche mie:* **[ries.]** cifra ristampata oggi rieseguendo `controlla_parametri.py` (0 errori) o `geometria_sensori.py`; **[ricontr.]** frase ritrovata oggi nella copia locale della scheda; **[sens.]** conto mio. Dei 24 indirizzi citati ho controllato oggi solo che rispondano, non il contenuto. Le chiavi provvisorie delle fonti (per esempio st-vl53l7cx, ahn2019) sono collegamenti: nel sorgente la chiave sta fra parentesi quadre, seguita dal link; l'elenco è in coda. Non ho eseguito prove nuove, quindi non ci sono previsioni mie. *Scostamenti:* nel controllo finale ho lanciato un `git status` (sola lettura, nessuna modifica), contro il «niente git» della consegna; per contare le pagine ho impaginato una copia nella cartella temporanea della sessione. *Sigle interne:* R1–R8 requisiti della challenge; B1–B9 blocchi del sistema; H-0xx ipotesi in gara; F-0xx fatti consolidati; K-0xx contraddizioni fra ruoli; H0–H13 prove da fare sull'hardware; P… previsioni scritte prima di una prova. **Q1–Q6** qui sono i requisiti sulla posa del sensore in moto (§D.6), non la «domanda Q6» del contratto di f10.

**Sigle dei file** (solo in questa sezione). `LID` = `f1/985ccd9bca46/CONSEGNA.md` e `PREVISIONI.md` (esperto di LiDAR) · `T1` = `f2/04-torneo/TORNEO_parte1.md`, `esito_attacchi_parte1.txt`, `esito_attacchi2_parte1.txt` · `TRI` = `f2/03-triage/TRIAGE.md` · `SEL` = `f2/05-selezione/SELEZIONE.md` · `FV` = `f3/fonti/FONTI_VERIFICATE.md` (curatore delle fonti) · `VRF` = `f3/H-012/02-validazione/VERIFICA.md` · `PM` = `f3/H-012/03-metrologo/PIANO_MISURE.md` · `A12` = `f4/H-012/01-avversario/risultati_a12.txt` · `V2` = `f4/H-012/05-correzioni/SOLUZIONE_V2.md` · `VER` = `f4/H-012/09-arbitro/VERDETTO.md` · `AUD` = `f5/02-audit/AUDIT.md` · `MOTO` = `f6-specializzazione/02-slam/MOTO_PROPRIO.md` e `risultati.txt` · `ATT6` = `f6-specializzazione/03-avversario/ATTACCO_SPECIALIZZAZIONE.md`. **Non vagliati:** `L9` = `f9-preproposta/07-lidar/CONSEGNA.md` · `PIA9` = `f9-preproposta/11-pianificatore/CONSEGNA.md` · `MS`, `PS`, `SP` = `f10-dati/02-sensori/MODELLO_SENSORE.md`, `parametri_sensori.json`, `PREVISIONI.md` · `RIC` = `f10-dati/01-ricercatore/DATI_PUBBLICI.md` · `INF` = `f10-dati/03-infrastruttura/AMBIENTE.md` e `formato_sequenza.md` · `EMB` = `f10-dati/04-embedded/PREVISIONI.md` e `geometria_sensori.py`.

## D.1 In breve

- **Sensore principale:** una camera di profondità a *stereo attivo* (due camere a infrarossi e un proiettore di trama: la distanza viene dallo scarto fra le due immagini) con unità inerziale (IMU), ferma su treppiede a 1,2 m, inclinata di 15° in basso (`V2`, B1). È l'ipotesi H-001, **adottata** (`SEL`).
- **Il modello non è deciso.** Il nucleo dice «quella posseduta dalla squadra» fra D455, D435i e Gemini 335; il settimo addendum dice che oggi la squadra non ha sensori e che l'inventario di quelli di casa arriva fra 5–6 ore. **Non risolto.**
- **Tre sensori a tempo di volo non danno 360°**, ma al più 180° (§D.3): verificato sulle fonti, per i soli sensori citati (`VER` §5, punto 8).
- I limiti del sensore principale sono **dichiarati, non misurati** (§D.4); in moto **nessuna soglia vale** (§D.6); le prime ore si fanno su registrazioni e su un sensore simulato (§D.7).

## D.2 I sensori considerati

**Tempo di volo multizona (ST, famiglia VL53).** Misurano la distanza dal tempo di andata e ritorno di un impulso di luce a 940 nm (`L9` [g]), su 4×4 o 8×8 zone. Solo I2C, niente USB: serve un microcontrollore (`EMB`, E10 [g]).

| | VL53L5CX | VL53L7CX | VL53L8CX | File |
|---|---|---|---|---|
| Campo (diagonale) | 45°×45° (63°) | 60°×60° (90°) | 45°×45° (65°) | `FV` [g] |
| 4×4 a 30 Hz, bianco 88 %: buio / 5 klx | 4,0 / 1,7 m | 3,5 / 0,65 m | 4,0 / 2,85 m | `FV` p. 2–3 [g]; `PS` |
| 8×8 a 15 Hz, bianco 88 %: buio / 5 klx | manca | 2,0 / 0,5 m | 4,0 / 1,55 m | `FV` p. 2–3 [g]; `PS` |
| 8×8 a 15 Hz, grigio 17 %: buio / 5 klx | manca | 0,8 / 0,35 m | 2,45 / 1,15 m | `LID` P3; `PS` |
| Accuratezza in 8×8 oltre 0,2 m | manca | ±5 % buio; ±9–14 % a 5 klx | ±5 % buio; ±5–8 % a 5 klx | `MS` §2 |
| Zona in 8×8: passo; lato a 2 m | 5,6°; manca | 7,5°; 13 cm | 5,6°; 10 cm | `LID` P2; `MS` [ries.] |

Schede: [st-vl53l5cx](https://cdn.sparkfun.com/assets/6/e/3/0/6/vl53l5cx-datasheet.pdf) DS13754 Rev 2, [st-vl53l7cx](https://www.pololu.com/file/0J1992/vl53l7cx.pdf) DS13865 Rev 6, [st-vl53l8cx](https://www.pololu.com/file/0J2029/vl53l8cx.pdf) DS14161 Rev 7, guida [st-um3038](https://www.pololu.com/file/0J1993/um3038-a-guide-to-using-the-vl53l7cx-timeofflight-multizone-ranging-sensor-with-90-fov-stmicroelectronics.pdf): copie ospitate da rivenditori (st.com non risponde: `FV`), forse non l'ultima revisione. Da sapere: le portate sono «tipiche», al 90 % di misure valide (`PS`); l'accuratezza è data a **2,7 σ** ([ricontr.] DS13865, riga 883 della copia locale), quindi lo scarto tipo per zona in 8×8 al buio è 1,9 % della distanza, 3,7 cm a 2 m (`MS` §2 [ries.]); «5 klx» è la condizione di prova della scheda, non il sole pieno (`FV` p. 3); ogni zona porta un codice (5 valida, 9 valida con impulso largo, 255 nessun bersaglio: `PS`), e «nessun bersaglio» non è «libero»; l'L7CX fa al più 15 Hz in 8×8 e 60 Hz in 4×4 (`PS`). Prezzi: non verificati (`LID`). **Stato:** dichiarato dal costruttore, riscontrato nel testo delle schede.

**Camere a tempo di volo.** [orbbec-femtobolt](https://www.orbbec.com/products/tof-camera/femto-bolt/) (850 nm): campo largo 120°×120° con portata 0,25–2,88 m (512×512, fino a 30 fps) o 0,25–2,21 m (1024×1024, 5 o 15 fps); campo stretto 75°×65° con 0,5–3,86 m o 0,5–5,46 m; 418 $ nel negozio Orbbec; ambiente «Indoor» nella pagina e «Indoor/Semi-Outdoor» nella scheda PDF del 2023 (`FV` p. 1 e 8 [g]). Più unità insieme: catture sfalsate di almeno 160 µs con cavo di sincronizzazione, o i laser interferiscono ([orbbec-femtobolt-sincronia](https://doc.orbbec.com/documentation/Orbbec%20Femto%20Bolt%20Documentation/Synchronize%20Multiple%20Femto%20Bolt%20Devices); `FV` [g]). Camera ToF [luxonis-tof](https://docs.luxonis.com/hardware/platform/depth/ToF-depth): 640×480, 0,2–5 m, «<1% indoors, <2% outdoors», senza dire a quale illuminamento (`FV` [g]). All'aperto l'uso del ToF resta limitato dall'interferenza del sole ([qiu2023](https://isprs-annals.copernicus.org/articles/X-1-W1-2023/17/2023/): Qiu, Martínez-Sánchez, Arias, ISPRS Annals 2023; `FV` [g]). Camera Arducam 240×180 e camere a matrice SPAD: nessuna scheda controllata (`LID`).

**Camere a stereo attivo (la famiglia scelta).**

| | RealSense D455 | RealSense D435i | Orbbec Gemini 335 | File |
|---|---|---|---|---|
| Campo di profondità | 87°×58° | 87°×58° | 90°×65° a 1280×800; 90°×60° a 848×480 | `FV` [g]; `PS` |
| Base (distanza fra le due camere) | 95 mm | 50 mm | 50 mm | `SP` P1, P3 [g] |
| Fascia ideale; minimo a 848×480 | 0,6–6 m; 0,35 m | 0,3–3 m; 0,195 m | 0,26–3 m; 0,18 m | `FV`; `SP` P2; `PS` |
| Errore dichiarato | RMS ≤ 2 % entro 4 m | RMS ≤ 2 % entro 2 m | ≤ ±2 % a 2 m | `SP` P1, P3 [g] |
| Rumore a 2 / 3 / 4 m, nominale (conto) | 0,8 / 1,8 / 3,2 cm | 1,5 / 3,4 / 6,0 cm | 1,6 / 3,6 / 6,4 cm | `MS` §1 [ries.] |
| Rumore a 2 / 3 / 4 m, limite di scheda (conto) | 2,0 / 4,5 / 8,0 cm | 4 / 9 / 16 cm | 3,0 / 6,8 / 12 cm | `MS` §1 [ries.]; `T1` |
| Fotogrammi al secondo a 848×480 | 30, fino a 90 | 30, fino a 90 | 30, fino a 60 | `PS` |
| Otturatore globale | profondità e colore | solo profondità | solo profondità | `FV`; `PS` |
| IMU | BMI085, giroscopio 200/400 Hz | idem | 50–1000 Hz | `PS` |
| Filtri del costruttore | nessuno nel sensore | nessuno nel sensore | **attivi di norma** | `MS` §1 |
| Prezzo (dollari, rivenditori) | 399–417 | 362–550 | 330–369 | `LID` P6, **non ricontrollati** |

Il rumore «nominale» è il conto σ(z) = z²·s/(f·B) con s = 0,08 pixel, il valore che il costruttore usa per la curva della D435; applicarlo alla D455 è un'ipotesi (`MS` §1). **Una sola misura di terzi:** D435 su parete bianca fra 0,4 e 2,1 m, 1,83 cm a 2 m, cioè 1,21 volte il nominale; a 3 m solo estrapolazione (`SP` P5; [ahn2019](https://ucla.box.com/shared/static/gqxwr2vvqsf22oi9dqtn50hr0xkruzie.pdf): Ahn, Chae, Noh, Nam, Hong, UR 2019, pp. 707–711, dati bibliografici da `PS`). I valori di scheda valgono su bersaglio bianco, frontale, nell'80 % centrale del campo. Fonti: [realsense-confronto](https://www.realsenseai.com/compare-depth-cameras/), [realsense-d400-scheda](https://www.realsenseai.com/wp-content/uploads/2026/03/RealSense-D400-Series-Datasheet-Mar-2026.pdf), [realsense-taratura](https://realsenseai.com/wp-content/uploads/2019/11/BKMs_Tuning_RealSense_D4xx_Cam.pdf), [orbbec-gemini335](https://www.orbbec.com/products/stereo-vision-camera/gemini-335/), [orbbec-gemini330-scheda](https://download.kamami.pl/p1203693-Gemini-330-series-Datasheet-V1.6.pdf). Tre OAK-D Pro W (127° orizzontali, 499–529 $ l'una (r)) sarebbero l'unica terna che chiude i 360°: scartate per il costo (`LID`; non controllate dal curatore).

**LiDAR** (di competenza dell'esperto di LiDAR: qui solo i numeri).

| | RPLIDAR C1 (2D) | LD19 (2D) | File |
|---|---|---|---|
| Passo angolare; misure al secondo; giri | 0,72°; 5000; 10 Hz (8–12) | 0,8°; 4500; 10 Hz (5–13) | `FV` p. 4; `PS` |
| Portata, bersaglio chiaro / scuro | 12 m (70 %) / 6 m (10 %) | 12 m / non dichiarata | `FV` p. 4; `PS` |
| Accuratezza; luce ambiente | ±30 mm; 40 klx | ±45 mm (scarto tipo 10 mm); 30 klx | `SP` P9; `FV` p. 4 |
| Prezzo (dollari) | 79,99 | 69–70 (r) | `LID` P7 |

Un solo piano a 360°. Su una persona larga 0,5 m cadono 13 punti (C1) o 12 (LD19) a 3 m (`MS` §3 [ries.]); su una gamba di 12 cm a 5 m 1,9 o 1,7 (`T1` P3). L'ipotesi H-003 (LiDAR 2D più camera) è **esclusa** dal ramo: al petto è smentita (meno di 4 punti su una gamba; il busto copre 127°–155°), su palo resta possibile solo se l'utente vuole i 360° (`SEL`). LiDAR 3D: Unitree L2, 360°×90°, 64 000 punti/s, giro completo a 5,55 Hz, 30 m (15 m al 10 %), 419 $; Livox Mid-360, 360°×59°, 40 m (r), 899–1092 $ (r) (`LID` P9; non controllati dal curatore). Fonti: [slamtec-c1](https://www.slamtec.com/en/C1/Spec), [waveshare-c1](https://www.waveshare.com/rplidar-c1.htm), [ldrobot-ld19-scheda](https://botland.com.pl/img/art/inne/21991_Karta%20katalogowa.pdf), [unitree-l2](https://www.unitree.com/L2), [livox-mid360](https://www.livoxtech.com/mid-360/specs).

## D.3 Perché tre sensori a tempo di volo non danno 360°

1. **Geometria.** Servono tre campi da 120°. Il multizona più largo, il VL53L7CX, ne ha 60°: la sua scheda scrive «three sensors can cover 180° x 60° FoV» ([ricontr.] riga 42 della copia locale; `FV` [g]). Con L5CX o L8CX (45°) tre sensori fanno 135° (`TRI`, F-001).
2. **Risoluzione.** A 4 m una persona larga 0,5 m occupa 1,27 zone (passo 5,6°) o 0,95 (passo 7,5°): presenza sì, forma e traccia no (`LID` P2).
3. **Portata.** Il sensore più largo è anche il più corto: in 8×8 2,0 m al buio e 0,5 m a 5 klx.
4. **Camere ToF da 120°.** La Femto Bolt arriva a 2,88 m nel modo largo; tre costano 1254 $ e vanno sincronizzate; con tre campi da 120° esatti non c'è sovrapposizione per tararle fra loro (argomento geometrico, non verificato) (`LID`, critiche 3–4).

**Stati.** «Tre ToF multizona coprono 360°»: **smentito** sui sensori controllati (F-001; contraddizione K-009 risolta per i sensori citati: `SEL`). «Tre camere ToF da 120°»: **non risolto**. Non è una ricerca esaustiva del mercato (`FV` p. 3).

**Che cosa resta dei ToF.** Un canale laterale facoltativo di sola prossimità, che non dichiara mai «libero» (`V2` §8). Conto delle aree (`A12`): la camera vede il 20,0 % del disco di 3 m; tre ToF da 60° fino a 2 m aggiungono il 22,2 %; uno puntato in basso copre 0,68 dei 0,98 m² dell'anello cieco. **Non vagliato** (`L9`): a 5 klx i tre VL53L7CX aggiungono l'1,4 % (0,7 % sul grigio); restano 16,5° ciechi per lato; come «preallarme» con soglia a 0,5 m il margine a 1,4 m/s è 0,07 s: respinto; proposta corretta: VL53L8CX in 4×4 a 30 Hz, soglia a 1,5 m (margine 0,85 s), circa 9 ore-persona. L'interferenza fra il proiettore della camera (850 nm) e i ToF (940 nm) va provata sull'hardware.

## D.4 Il sensore principale: perché, e con quali limiti

**Perché una camera frontale** (`LID`, proposta lidar-1): 42–56 pixel su una persona a 4 m contro 1,3 zone; colore allineato per l'etichetta; un solo cavo USB, nessuna interferenza né taratura fra sensori; l'occlusione della demo avviene nel campo frontale. Fuori campo tutto è «non osservato» per costruzione. Costo stimato del blocco B1: 3 ore (`V2`).

- **Portata dichiarata.** Prima «0,5–3 m» (`SEL`); ora «dove il rumore radiale del centro di una persona resta ≤ 5 cm», da misurare con la prova H1; griglia fino a 3 m (`V2` B1). Curve usate nelle simulazioni, a 2 / 3 / 4 m: 1,5 / 3,4 / 6,0 cm (nominale), 4 / 9 / 16 (pessimista), 5 / 11 / 20 (torneo). *Stato:* conto da scheda, non verificato fino all'hardware. Non vagliato (`MS` §6): le prime due curve sono quelle della **D435i**; con la D455 valgono la metà.
- **Anello cieco** (suolo vicino non visto). Suolo visto solo da 1,24 m, cioè il 30 % dell'estensione 0,5–3 m; un ostacolo alto 15 cm è invisibile sotto 1,09 m (`V2` B1). Senza inclinazione: da 2,16 m; a 20°: da 1,04 m; camera in verticale a 15°: da 0,74 m (`T1`). *Stato:* conto geometrico, con l'altezza di 1,2 m ipotizzata.
- **Cono cieco in alto.** Un ostacolo a 1,8 m di quota si vede solo oltre 2,41 m (a 20° oltre 3,79 m; a 30° mai) (`T1`); quota massima vista a 3 m: 1,95 m (`EMB` [ries.]). *Stato:* conto geometrico.
- **Fuori campo.** La camera vede il 20,0 % del disco di 3 m (`A12`); il resto è sempre «non osservato».
- **Vetro.** La lastra risulta «libero» in ogni griglia provata (`f2/04-torneo/TORNEO.md`, H-008; `V2` §7). *Stato:* **smentito** (R8 sul vetro), limite dichiarato; decide H2.
- **Superfici scure.** Attesi buchi; rischio di profondità inventata. Una persona in nero vista tutta come buco toglie il 6,5 % dei pixel a 2,5 m e il 25,5 % a 1 m (`L9`, conto non vagliato). *Stato:* **non verificato**; decidono P10 di `LID` (almeno il 70 % di pixel validi a 4 m) e H1 con la giacca nera.
- **Sole.** B1 è «invalidata se: sole» (`V2`). Misura di terzi su una D435 a 0,67 m: riempimento sotto l'80 % a 7770 lux su tutte le tessere, a 4350 lux sulla più scura, letto dai grafici (`MS` §1; [dxomark-stereo](https://corp.dxomark.com/wp-content/uploads/2025/02/DXOMARK_Report_Sample_3Dcamera_stereos.pdf)). *Stato:* K-009 **aperta**, costruttori discordi (`SEL`); decide H3.
- **Filtri del costruttore che riempiono i buchi.** RealSense, se il programma li crea: il filtro temporale rimette l'ultimo valore valido se il pixel era valido in 2 degli ultimi 4 fotogrammi; il riempimento dei buchi predefinito copia il vicino **più lontano** ([librealsense-filtri](https://github.com/IntelRealSense/librealsense/blob/master/doc/post-processing-filters.md); `MS` §1; `AUD`, ipotesi 1). Gemini 335: post-elaborazione attiva di norma. Un buco diventa così sfondo, cioè «libero»: è il meccanismo della contraddizione K-014. *Stato:* sostenuto dalla documentazione, non provato (P13 di `SP`). Condizione 1 del verdetto: filtri spenti e autoverifica all'avvio (mano sul sensore: pixel validi sotto il 10 % in 3 fotogrammi, o il programma non parte) (`VER` §4).
- **Banda senza dato ai bordi.** (a) Al bordo sinistro dell'immagine: 40 / 20 / 13 pixel a 1 / 2 / 3 m (D455), 21 / 11 / 7 (D435i). (b) A sinistra di ogni bordo verticale di un oggetto vicino: 19,0 cm (D455) e 10,0 cm (D435i, Gemini 335) con ostacolo a 1 m e sfondo a 3 m (`MS` §1 [ries.]); 9,5 e 5 cm nella geometria della demo (`AUD`, ipotesi 10). Le simulazioni assumevano ±20 cm **simmetrici**, con meno di 10 cm di margine (`V2` §5). *Stato:* conto; lato confermato da [ahn2019] e dalla scheda, formula derivata (`SP` P8); **non risolto** (P11).
- **Suolo visto di striscio.** Oltre 2,08 m il suolo è visto a più di 60° d'incidenza (68,2° a 3 m); l'unica misura di terzi dà rumore piatto fino a 60° e oltre 0,1 m a 75°, su un altro asse (`SP`; `MS` §6 [ries.]). *Stato:* **non risolto** (P12): tocca il «libero» fra 2,1 e 3 m.
- **Buchi fissi del pavimento.** Con l'1 % di celle sempre senza dato, l'83,6 % dei settori da 10° contiene un buco fisso (`AUD`, ipotesi 6, conto). *Stato:* non risolto; decide H5.
- **Latenza e tempo.** Voci note: circa 155 ms in media contro la soglia di 150; dall'esposizione all'applicazione 95 ms a 30 fps, 47 a 60, 39 a 90, misurati dal costruttore nei modi 848×100 ([realsense-altavelocita](https://dev.realsenseai.com/docs/high-speed-capture-mode-of-intel-realsense-depth-camera-d435); `VRF` §3c), che coprono circa 12° in verticale (non verificato: `AUD`, ipotesi 7). *Stato:* R7 **non risolta**; decide H12. Altro numero, non vagliato: 70 ms da un solo esempio della documentazione (`MS`). La marca da usare è `SENSOR_TIMESTAMP` (metà dell'esposizione, orologio del dispositivo), non l'ora d'arrivo al calcolatore ([librealsense-metadati](https://github.com/IntelRealSense/librealsense/blob/master/doc/frame_metadata.md); `MS` §1).
- **IMU.** Il criterio «affidabilità persa se si scosta di 0,5° o supera 5°/s» (`V2` B8) vale solo a sensore fermo, con un rumore dell'IMU ipotizzato (`V2` §7).

## D.5 Montaggio e condizioni della demo

- **Montaggio:** treppiede a 1,2 m (ipotesi: si misura con H0, ±1 cm e ±1°), camera orizzontale inclinata di 15° in basso, 30 fps con elaborazione a 15 Hz (`V2` B1; `PM`). Risoluzione da fissare e stampare all'avvio: i tempi del nucleo sono a 640×480, i conti dell'audit e di f10 a 848×480. Se la profondità viene allineata al colore, sulla D435i il campo scenderebbe a circa 69°×42° (non verificato) e il suolo si vedrebbe da 1,65 m (`AUD`, ipotesi 11).
- **Scena:** al chiuso, senza sole, pavimento piano, lontano dai vetri o con nastro opaco sulla lastra (`V2`; `PM` H2). All'avvio vuota e ferma: lì si stimano il piano del suolo e la quota di pixel validi; 1,34° d'errore alzano il suolo di 7 cm a 3 m (`AUD`, ipotesi 9).
- **Pannello e attore:** pannello fermo, largo 1 m e alto almeno 1,5 m; attore a non più di 2,3 m; una sola persona dietro (`VER` §4, condizioni 3 e 6). Con la camera a 1,2 m un pannello alto 1 m lascia vedere tutto sopra 0,80 m (`AUD`, ipotesi 5).
- **Da registrare a ogni prova:** numero di serie, firmware, driver, risoluzione, frequenza, preimpostazione di profondità, filtri, altezza, inclinazione, luce (`PM`).
- **Non vagliato:** nell'atto 1 (metà campo coperta) una persona in nero a 2,5 m porta i pixel validi al 43,5 %, sotto la soglia del 50 %: scatta «affidabilità persa» (`L9`). A un'altra quota tutto cambia: a 0,25 m (drone posato) il suolo si vede da 0,26 m e la quota massima vista a 3 m è 1,00 m (`ATT6`, S7).
- **Sicurezza ottica:** classe 1 dichiarata per VL53, C1 e L2; per Femto Bolt e RealSense non verificato; vale per il prodotto integro (`LID`).

## D.6 Il sensore in moto: i requisiti sulla posa (Q1–Q6)

Per seguire gli oggetti mentre il sensore si muove serve la *posa* (dove sta e come è orientato il sensore, istante per istante). `MOTO` ricava quanto dev'essere precisa perché le soglie del nucleo tengano. **Stato:** sostenuto da un modello (N = 20 000 valutazioni nella prima tabella di `risultati.txt`); gli errori delle sorgenti sono **ipotesi**; nessuna soglia del nucleo è provata in moto.

| | Requisito | Valore a 2 / 3 / 10 / 30 m |
|---|---|---|
| Q1 | rotazione attorno alla verticale (imbardata), su 0,87 s | ≤ 0,87° a ogni distanza |
| Q2 | errore di velocità propria, trasversale / radiale (cm/s) | 3,4 / 5,2 · 5,2 / 11 · 17 / 10 · — / 10 |
| Q3 | sincronia fra posa e profondità | 20–30 ms (rover che gira a 30°/s); 73 ms (volo stazionario); 27 ms (petto); 5,6 ms (testa) |
| Q4 | inclinazione in avanti (beccheggio) rispetto al suolo | 1,68° / 1,02° / 0,32° / 0,13° |
| Q5 | scostamento non modellato nell'area prevista | 9 cm a 0,67 s, 15 cm a 1 s, 39 cm a 2 s |
| Q6 | imbardata sull'età dell'ultima misura | 2,9° / 1,9° / 0,57° / 0,19° |

**Quale sorgente li rispetta, nel modello** (`MOTO` §2 e §6):
- *treppiede o rover fermo, giroscopio tarato da fermo:* Q1 rispettato (0 falsi «in movimento» con 0,1°/s di deriva; 9 % con 1°/s);
- *rover a 0,3–0,5 m/s, ruote più giroscopio:* Q2 rispettato con errore del 3 % della distanza, al limite con il 10 % (7 % di falsi a 2 m);
- *drone con autopilota* (errore di velocità ipotizzato 0,1 m/s): Q2 **non rispettato** a 2 m (98 % di falsi);
- *indossato senza odometria:* **non rispettato** (100 % di falsi); con odometria visuale-inerziale all'1–3 % rispettato nel modello, ma ottenerla camminando è non verificato;
- *sola IMU per il beccheggio:* Q4 **non rispettato** a 10–30 m; a 2–3 m serve ristimare il piano del suolo a ogni fotogramma (non verificato).

«Ciò che non è osservato non è mai libero» non dipende dalla posa (per costruzione). La camera da sola non dà un'odometria: servono ruote, autopilota o un programma di terzi (elenco con licenze e link in `MOTO` §2). Da non promettere: il volo, il sensore sulla testa, oltre 0,5 m/s (`MOTO` §4).

## D.7 Senza sensori nelle prime ore, e che cosa prepara f10

**Che cosa cambia** (settimo addendum). Le prime 5–6 ore delle 14 si fanno su dati registrati o simulati; l'architettura deve poter cambiare sorgente (registrazione, sensore simulato, sensore vero) senza toccare il resto. **Solo il sensore della squadra** può decidere: rumore dell'esemplare e portata (H1), vetro (H2), sole (H3), nero, stato dei filtri, «libero» dentro l'ombra vera (K-014), latenza (H12). Stima non vagliata, fatta su 24 ore e non sulle 14 + 4 (`PIA9`): senza sensore si perdono la latenza, «affidabilità persa» e la prova scelta dal giurato; con una camera sola conviene **una** sessione di registrazione e poi l'analisi in parallelo.

**Già consegnato da f10 — tutto non vagliato.**
- **Parametri del sensore simulato** (`PS`, `MS` [ries.]): tre camere, due ToF, due LiDAR 2D; ogni valore con la provenienza: 93 dichiarati, 5 misurati da terzi, 20 calcolati, **32 ipotesi da tarare** (buchi per materiale, correlazione del rumore, margine della banda). Il simulatore gira sempre due volte, nominale e limite.
- **Strumenti esistenti** (`MS` §4): su otto cercati, nessuno su sola CPU riproduce buchi e occlusione di una camera D4xx: il modello va scritto a mano.
- **Previsioni aperte** (`SP`): P11 (ombra asimmetrica), P12 (suolo di striscio), P13 (filtro che crea «libero»), P14 (rumore del centro di una persona).
- **Dati pubblici scelti** (`RIC`): TUM RGB-D fr3/walking_static (Kinect v1, 474 074 105 byte), THÖR (traiettorie di persone a 100 Hz), RGB-D People di Friburgo (2,8 GB), tre registrazioni RealSense grezze: 4,04 GB. **Nessuno ha la camera a 1,2 m inclinata di 15°**; il più vicino (HUM4D, sei D455) si scarica solo dal browser.
- **Ambiente e formato comune** (`INF`): Python locale (numpy 2.5.4, scipy 1.18.1, opencv 5.0.0.93, rosbags 0.11.9); una sequenza è una cartella con `meta.json`, `tempi.csv` e profondità a 16 bit in millimetri, 0 = nessun dato; controllo automatico (24 sequenze difettose su 24 rifiutate).
- **Verso l'inventario dei sensori di casa** (`EMB`): script che registra da RealSense, OAK e Orbbec nel formato comune, **mai provato con un dispositivo**; suolo visto da 1,62 m con un Kinect v1, 1,55 m con un'Astra, 1,46 m con un'OAK-D [ries.]. Avvisi: `pyrealsense2` 2.59.1 ha i pacchetti per Python 3.14, ma dichiara il supporto fino al kernel 6.14 (la macchina di sviluppo ha il 7.3); OAK chiede un cavo USB 3 e una regola di sistema da installare con privilegi.

Alle 16:16 l'archivio TUM è scaricato; le cartelle della catena, del simulatore, della validazione e del verdetto di f10 sono vuote: **nessun risultato su dati veri esiste ancora.** Un risultato ottenuto con un altro sensore non diventa «validato sul sensore della squadra» (`f10-dati/CONTRATTO_DATI.md`, criterio 5).

## D.8 Dove due file dicono cose diverse

1. **LD19, luce ambiente:** 60 klx (`LID` P7) contro 30 klx (`FV` p. 4; `PS`). I 60 klx sono del modello STL-19P: vale 30.
2. **LD19, passo di 0,8°:** «non trovato» (`FV` p. 4) contro «è nella scheda V2.5» (`SP`).
3. **Gemini 335, campo:** 90°×65° (`FV`, `V2`, `EMB`) contro 90°×60° a 848×480 (`PS`): due risoluzioni. `geometria_sensori.py` usa però 65° con 848 pixel e dà il suolo da 1,10 m; con 60° viene 1,20 m [sens.].
4. **Banda d'occlusione:** 9,5 e 5 cm (`AUD`) contro 19 e 10 cm (`MS`): geometrie diverse (sfondo al doppio oppure al triplo della distanza dell'ostacolo), giuste entrambe.
5. **Copertura dei ToF laterali:** 22,2 % (`A12`: al buio, sul bianco) contro 1,4 % (`L9`: a 5 klx, non vagliato).
6. **Latenza della camera:** 95 ms (`VRF`) contro 70 ms (`MS`): fonti diverse, nessuna è una specifica.
7. **Rumore nominale a 4 m, base 50 mm:** 5,7 cm con focale 446,8 pixel (`T1`) contro 6,0 cm con 424 (`MS`).
8. **Femto Bolt:** «Indoor» contro «Indoor/Semi-Outdoor» (`FV` p. 8); 418 $ (`FV`) contro 418–559 $ (`f1/dfac83300259/CONSEGNA.md`, da ricerca).
9. **Portata dichiarata:** «0,5–3 m» (`SEL`) contro «dove il rumore è ≤ 5 cm, da misurare» (`V2`): vale la seconda.

## D.9 Le prime misure quando arriva un sensore

(1) Autoverifica dei filtri, due minuti (`AUD`, ipotesi 1). (2) H0–H6 nella prima ora: possono cambiare sensore, portata e luogo della demo (`PM`). (3) Celle per stato su 150 fotogrammi della sala vuota; «libero» dentro l'ombra vera del pannello, con la banda senza dato misurata sui due lati (`VER` §3 e §6). (4) H12 per la latenza. Proposta non vagliata di f10: parete piana a 1, 2 e 3 m, suolo e un bordo verticale, 15 minuti, per tarare le 32 ipotesi del simulatore (`MS`).

---

## File letti

**Per intero:** `ADDENDUM_UTENTE.md`; `f1/985ccd9bca46/CONSEGNA.md` e `PREVISIONI.md`; `f3/fonti/FONTI_VERIFICATE.md`; `f4/H-012/05-correzioni/SOLUZIONE_V2.md`; `f4/H-012/09-arbitro/VERDETTO.md`; `f5/02-audit/AUDIT.md`; `f6-specializzazione/01-esperto-dominio/SPECIALIZZAZIONE.md`; `f6-specializzazione/02-slam/MOTO_PROPRIO.md`; `f9-preproposta/07-lidar/CONSEGNA.md`; `f10-dati/CONTRATTO_DATI.md`; `f10-dati/01-ricercatore/DATI_PUBBLICI.md`; `f10-dati/02-sensori/MODELLO_SENSORE.md`, `parametri_sensori.json`, `PREVISIONI.md`, `scaricati/PROVENIENZA.md`; `f10-dati/03-infrastruttura/AMBIENTE.md`, `formato_sequenza.md`; `f10-dati/04-embedded/PREVISIONI.md`, `geometria_sensori.py`.

**In parte** (ricerca per parole, o le prime righe): `f1/3fff79e9c3ea/FONTI.md`; le `CONSEGNA.md` di `f1/b8262bfed263`, `f1/c85dbcc51ea6`, `f1/dfac83300259`, `f1/e30f9e2dd4d7`; `f2/03-triage/TRIAGE.md`; `f2/04-torneo/TORNEO.md`, `TORNEO_parte1.md`, `esito_attacchi_parte1.txt`, `esito_attacchi2_parte1.txt`; `f2/05-selezione/SELEZIONE.md`; `f3/H-012/01-scene-dinamiche/SOLUZIONE.md`; `f3/H-012/02-validazione/VERIFICA.md`; `f3/H-012/03-metrologo/PIANO_MISURE.md`; `f4/H-012/01-avversario/risultati_a12.txt`; `f6-specializzazione/02-slam/risultati.txt`; `f6-specializzazione/03-avversario/ATTACCO_SPECIALIZZAZIONE.md`; `f9-preproposta/CONTRATTO_PREPROPOSTA.md`; `f9-preproposta/11-pianificatore/CONSEGNA.md` e `PREVISIONI.md`; `f10-dati/04-embedded/registra_sequenza.py`; `f10-dati/12-dati-veri/PREVISIONI.md`; nelle copie locali delle schede (`f9-preproposta/07-lidar/scaricati/`, `f10-dati/02-sensori/scaricati/`) solo ricerche di singole frasi.

**Eseguiti, non letti riga per riga:** `f10-dati/02-sensori/controlla_parametri.py` e `f10-dati/04-embedded/geometria_sensori.py` (sola stampa, nessun file scritto).

**Non letti:** le cartelle di f7 e f8; gli altri ruoli di f9; `CONTRATTO.md`; `regole_challenge.md`. Se contengono affermazioni sui sensori, qui mancano.

## Chiavi di riferimento usate

I link sono nel testo, attaccati alla prima citazione di ogni chiave. «Aperta da» dice chi nello sciame ha aperto la fonte e come; io ho controllato oggi solo che l'indirizzo risponda (codice 200 o 206, ore 16:13).

| Chiave | Che cos'è | Aperta da |
|---|---|---|
| [st-vl53l5cx] | ST, scheda VL53L5CX, DS13754 Rev 2 (copia SparkFun) | curatore [g] |
| [st-vl53l7cx] | ST, scheda VL53L7CX, DS13865 Rev 6 (copia Pololu) | curatore [g]; copia locale in f9 |
| [st-vl53l8cx] | ST, scheda VL53L8CX, DS14161 Rev 7 (copia Pololu) | curatore [g]; copia locale in f9 |
| [st-um3038] | ST, guida UM3038 Rev 2 al VL53L7CX (copia Pololu) | esperto di LiDAR, f9 [g] |
| [orbbec-femtobolt] | Orbbec, Femto Bolt: pagina prodotto e scheda PDF 0816-v01 | curatore [g] |
| [orbbec-femtobolt-sincronia] | Orbbec, «Synchronize Multiple Femto Bolt Devices» | curatore [g] |
| [luxonis-tof] | Luxonis, «ToF Depth Perception» | curatore [g] |
| [qiu2023] | Qiu, Martínez-Sánchez, Arias, «Evaluation and comparison of different time of flight cameras for outdoor applications», ISPRS Annals X-1/W1-2023 | curatore [g] |
| [realsense-confronto] | RealSense, confronto delle camere | curatore [g] |
| [realsense-d400-scheda] | RealSense D400 Series Datasheet, rev. 023, marzo 2026 | f9 e f10, sulla copia locale [g] |
| [realsense-taratura] | RealSense, «BKMs Tuning RealSense D4xx Cam» | f10 [g] |
| [realsense-altavelocita] | RealSense, modo di cattura ad alta velocità della D435 | validazione, f3 (modo di lettura non trovato nelle righe lette) |
| [librealsense-filtri] | librealsense, `doc/post-processing-filters.md` | f10 [g]; l'audit cita un'altra pagina sullo stesso tema (https://dev.realsenseai.com/docs/post-processing-filters/), letta solo dal riassunto di una ricerca |
| [librealsense-metadati] | librealsense, `doc/frame_metadata.md` e `rs_frame.h` | f10 [g] |
| [orbbec-gemini335] | Orbbec, Gemini 335, pagina prodotto | curatore [g] |
| [orbbec-gemini330-scheda] | Orbbec, Gemini 330 Series Datasheet v1.6 (copia di un rivenditore) | f9 e f10, sulla copia locale [g] |
| [ahn2019] | Ahn, Chae, Noh, Nam, Hong, «Analysis and Noise Modeling of the Intel RealSense D435 for Mobile Robots», UR 2019 | f10 [g]; non passato dal curatore |
| [dxomark-stereo] | DXOMARK, rapporto campione su camere stereo | f10 (numeri solo nei grafici) |
| [slamtec-c1] | Slamtec, RPLIDAR C1, specifiche | curatore [r]; f10 [g] |
| [waveshare-c1] | Waveshare, pagina del RPLIDAR C1 (prezzo) | esperto di LiDAR, f1 |
| [ldrobot-ld19-scheda] | LDROBOT, LD19 Datasheet V2.5 (copia di un rivenditore) | f10 [g] |
| [unitree-l2] | Unitree, L2 | esperto di LiDAR, f1; non controllata dal curatore |
| [livox-mid360] | Livox, Mid-360, specifiche | aperta nel torneo f2 (non dà principio di misura né prezzo); campo, portata e prezzo solo (r) |

**Mancano** una chiave e una verifica per: i prezzi (tutti, salvo Femto Bolt), la OAK-D Pro W, la camera Arducam, i programmi di odometria elencati in `MOTO` §2.
