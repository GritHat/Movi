# Moto proprio: che cosa serve al nucleo quando il sensore si muove (`sciame-slam`, f6)

**In testa.**
- **Tutto è conto o modello** (`bilancio_posa.py`, Python puro, 6 s, seme fisso; `risultati.txt`): nessun sensore vero, nessuna posa vera. Gli errori delle sorgenti di posa sono **ipotesi mie**. Nessuna soglia del nucleo è provata in moto.
- **Previsioni** scritte alle 14:41:38 e 14:41:49 (`PREVISIONI.md`), prova alle 14:44:10. **Smentite: P1, P3, P10, metà di P2 e di P7.** Causa unica: avevo letto la regola «mobile» dal testo (soglia uguale sui due assi). Il codice della validazione (`f4/H-012/03-validazione/sim_v2.py`, righe 449 e 496–499) usa sull'asse trasversale σ = z·1°/√12 e divide per √3: **la soglia trasversale è un angolo, 1,18°, uguale a ogni distanza.** Lo script segue il codice; le previsioni non le ho riscritte. Reggono P4 (a 30 m al limite: scansione rada), P5, P6, P8, P9, P11.
- **Scostamenti.** Lunghezza: circa quattro pagine, non tre. Rumore del LiDAR: 5 cm nelle previsioni, 3 cm radiali nello script. Lo strumento di lettura ha salvato da solo un PDF fuori dalla cartella (`~/.claude/projects/.../tool-results/webfetch-1794663857371-y81ee7.pdf`): non l'ho aperto. Le pagine in rete le riassume un modello ausiliario: le frasi fra «» vanno ricontrollate. **[A]** pagina aperta oggi; **[R]** solo risultato di ricerca; **NV** non verificato.
- **Indipendenza.** Lo script condivide con il nucleo la regola «mobile» e le curve di rumore, e con me l'autore: vale per la geometria, non per il sensore.

## 1. Che cosa cambia nel nucleo, blocco per blocco

Tre riferimenti: **S** (sensore, a ogni fotogramma), **L** (S livellato sul piano del suolo), **O** (odometria locale: fermo rispetto al mondo per qualche secondo; può derivare piano, non deve saltare).

| Blocco | Dove vive | Che cosa cambia | Serve la posa? |
|---|---|---|---|
| Griglia del fotogramma (libero, occupato osservato, in ombra, non osservato) | L, ricalcolata sempre | solo il piano del suolo, **ristimato a ogni fotogramma** (seme: la gravità dell'IMU; accettato entro ±2° e ±5 cm dal precedente, altrimenti «affidabilità persa») | **No.** È la parte di sicurezza: «mai libero dove non è osservato» non dipende dal moto proprio |
| Memoria del «libero» (3 fotogrammi) | L | sulla griglia polare l'imbardata è uno scorrimento di colonne: si riallinea con il giroscopio. Se la traslazione nei 3 fotogrammi supera mezza cella (oltre 0,37 m/s) vale solo il fotogramma corrente. Nell'invariante 1, v_max diventa v_max + velocità propria | imbardata su 0,13 s |
| «Occupato ricordato» | O, con l'età | riproiettato in L, dilatato di r·σ_ψ(età) + σ_t(età); non genera mai «libero» | sì, su secondi |
| Tracce e Kalman | O | misura portata in O con la posa all'istante della profondità; a R si sommano (r·σ_ψ)² sull'asse trasversale e σ_t² su entrambi, con σ dell'**incremento** di posa dall'ultimo aggiornamento (la deriva assoluta è comune a tutto e si cancella) | sì, su 1–2 s |
| Regola «mobile» | O | soglia per asse = 4,08·√(σ² + 1,5·(r·σ_ψ)² + 1,5·σ_t²). «Mobile» (nel mondo) e «in avvicinamento» (velocità relativa) diventano due grandezze: un muro fermo si avvicina a un veicolo che avanza | sì: è il blocco più esigente |
| Strato 1, cuneo d'ombra | L, ricalcolato sempre | **l'ombra d'ingresso si lega all'occlusore, non alle celle** (`slam-3`): l'occlusore prende un'identità ed è seguito in O come un gruppo fermo; è visto a ogni fotogramma, quindi la deriva non si accumula. Strato 1 = cuneo *corrente* di quell'occlusore più la fascia. Le celle scoperte dalla parallasse si rilasciano con la regola che c'è già, o mostrano il soggetto. Se l'occlusore esce dal campo, il cuneo si congela in O come «non osservato» | solo per l'identità dell'occlusore |
| Riaggancio | L | rilevamento e cuneo sono dello stesso fotogramma: la posa non entra. Entra fra l'ultima misura (vecchia fino a 0,2 s) e l'ombra: fascia = 0,40 + r·(σ_ψ + ω·τ) + v·τ | incremento su 0,2 s |
| Area prevista | O | covarianza del filtro più quella dell'incremento di posa | sì |
| «Affidabilità persa» | — | la regola dell'IMU del nucleo (0,5° o 5°/s) in moto scatterebbe sempre. Diventa: posa più vecchia di un fotogramma, salto dichiarato dalla sorgente, covarianza oltre il requisito, velocità angolare oltre il limite di sincronia, piano del suolo fuori dai limiti. **Senza posa il sistema degrada alla griglia del fotogramma**: ostacoli e «non osservato» restano validi, «mobile» esce «non determinato», le tracce pendenti restano nello strato 1 | — |

**Scartate:** tracce nel riferimento del sensore (stessi conti, memoria più difficile); mappa globale con chiusura dei cicli (inutile su secondi, e introduce salti). **Non provato:** l'occlusore fermo visto da un sensore che trasla somiglia al caso «occlusore mobile», che nel nucleo invalida lo strato 1.

## 2. Da dove viene la posa, e con quale errore

Conta l'errore **relativo** su 1 s (previsione, «mobile») e su qualche secondo (memoria). Non ho trovato oggi una fonte leggibile con questi numeri (il confronto di riferimento, https://rpg.ifi.uzh.ch/docs/ICRA18_Delmerico.pdf, non si è lasciato leggere). **Le cifre d'errore delle sorgenti sono ipotesi (NV)**, da misurare sulla piattaforma; i falsi «mobile» vengono dallo script.

**(a) Ferma o in volo stazionario.** Su treppiede o rover fermo basta il giroscopio **tarato da fermo all'avvio**: con 1°/s di bias (la cifra di F-008) i falsi sono al 9 %, sulla soglia; con 0,1°/s sono 0. Il beccheggio dell'IMU non garantisce 1,0° (requisito a 3 m; errore tipico NV): il piano del suolo si ristima a ogni fotogramma. Un drone in volo stazionario **trasla**: bastano 3,4 cm/s trasversali non compensati per i falsi a 2 m. Il treppiede non simula questo caso.

**(b) Rover a 0,3–0,5 m/s.** Ruote più giroscopio (imbardata dal giroscopio): con il 3 % della distanza 0 falsi; con il 10 % (slittamento) 7 % a 2 m. **La camera da sola non dà un'odometria**: il modulo T265 è fuori produzione dal 2022 e il costruttore indica D455 o D435i «with 3rd Party SLAM SW» [R]. Componenti aperti:

| Componente | Sensori | Licenza | Nota |
|---|---|---|---|
| Basalt | camera + IMU, anche senza IMU | BSD 3 [A] | tutorial sulla T265; altre RealSense NV |
| RTAB-Map | RGB-D, stereo, LiDAR (NV oggi) | BSD, dal distintivo [A] | la via più corta con una D435i o D455 (stima mia) |
| OpenVINS | mono o stereo + IMU | GPL-3 [A] | versione 2.7, maggio 2023 |
| VINS-Fusion | mono o stereo + IMU | GPLv3 [A] | «online temporal calibration (time offset between camera and IMU)» |
| ORB-SLAM3 | mono, stereo, RGB-D, ± IMU | GPLv3 [A] | V1.0, dicembre 2021 |
| KISS-ICP | solo LiDAR | MIT [A] | `pip install kiss-icp` |
| FAST-LIO2 | LiDAR + IMU | GPL-2.0 [A] | «Khadas VIM3, Nivida TX2, Raspberry Pi 4B(8G RAM)»; Mid-360 non nominato |
| cuVSLAM | stereo + IMU, GPU | non confermata [R] | pacchetto Python non commerciale [R] |

Tempo reale sul portatile della squadra: **NV**. Le licenze GPL pesano su chi vuole poi un prodotto; Basalt, RTAB-Map e KISS-ICP no.

**(c) Drone con autopilota.** Lo stimatore di PX4 lavora su un orizzonte ritardato e porta gli stati al presente con l'IMU («propagate the states forward from the 'fusion time horizon' to current time»; IMU «at a minimum rate of 100Hz») [A]. Il messaggio d'odometria porta `timestamp_sample`, le varianze di posizione, assetto e velocità e un `reset_counter` [A]: marca temporale, covarianza e avviso di salto, ciò che serve al punto 1. **La pagina non dà alcuna accuratezza** [A]. Con 0,1 m/s d'errore di velocità (ipotesi): falsi al 98 % a 2 m, 3 % a 3 m, 7 % a 10–30 m. Sincronia fra gli orologi di autopilota e camera: NV.

**(d) Indossato, persona che cammina.** Senza ruote, con la traslazione non compensata, i falsi sono il **100 %**: il giroscopio non basta, serve l'odometria visuale-inerziale (1 % della distanza e 0,1°/s: 0 falsi; 3 % e 0,3°/s: 0,6 % a 2 m). Il vincolo vero è la **sincronia**: 5,6 ms con la testa a ±30° e 0,5 Hz, 27 ms al petto (±8° a 1 Hz). L'andatura (±3° di beccheggio, rimbalzo verticale) impone il piano ristimato a ogni fotogramma. Sincronia IMU–profondità della camera sotto 5 ms: NV. Conseguenza: **al petto, non sulla testa.**

Caso degenere di (b), (c), (d): se un oggetto mobile riempie il campo, l'odometria visuale segue l'oggetto e il mondo «si muove». Ruote e IMU non ne soffrono: tenere il confronto fra le due stime.

## 3. Il bilancio dell'errore: i requisiti sulla posa

Regola «mobile» non modificata, 15 Hz, curva di rumore nominale del nucleo; LiDAR: 3 cm radiali (ipotesi).

| Soglia del nucleo | Requisito sulla posa | A 2 / 3 / 10 / 30 m |
|---|---|---|
| «Mobile»: falsi ≤ 10 % su un gruppo fermo | **Q1** imbardata relativa ≤ 0,87° su 0,87 s (≤ 0,7° per l'1 %) | uguale a ogni distanza |
| | **Q2** errore di velocità, trasversale / radiale (cm/s) | 3,4 / 5,2 · 5,2 / 11 · 17 / 10 · — / 10 |
| | **Q3** sincronia: τ·Δω ≤ 0,87°, con Δω la variazione della velocità angolare nella finestra | giro a 30°/s con arresto brusco: 30 ms (20 ms perché sbagli al più un giro su dieci); volo stazionario ±3° a 1 Hz: 73 ms; petto: 27 ms; testa: 5,6 ms |
| Quota del suolo 0,07 m: ≤ 10 % di celle «occupato» | **Q4** beccheggio rispetto al suolo | 1,68° / 1,02° / 0,32° / 0,13°; con ±2,5 cm di rimbalzo 1,26° / 0,78° / 0,24° / 0,09° |
| Copertura dell'area prevista ≥ 0,90 (da 0,92) | **Q5** scostamento non modellato ≤ 0,46 σ: 9 cm a 0,67 s, 15 cm a 1 s, 39 cm a 2 s | su 1 s: 4,4° / 2,9° / 0,88° / 0,29° |
| Fascia di 0,40 m, di cui 0,10 m alla posa (il nucleo dichiara meno di 10 cm di margine) | **Q6** imbardata sull'età dell'ultima misura, più ω·τ | 2,9° / 1,9° / 0,57° / 0,19°; a 30°/s il ritardo che consuma il margine è 95 / 64 / 19 / 6 ms |

**Che cosa dice.**
1. Il blocco più esigente è la regola «mobile», non lo strato 1.
2. Alla scala della camera decidono traslazione e sincronia. Alla scala del LiDAR decidono il beccheggio (nessuna IMU dà 0,13°: piano dai dati, e soglia di quota che cresce con la distanza) e la fascia, che va scritta 0,40 + r·σ_ψ.
3. **Allargare la soglia con la σ di posa (`slam-2`) azzera i falsi (≤ 0,01 %) ma alza la velocità minima vista**: con 1°/s, a 3 m da 0,07 a 0,27 m/s, a 10 m da 0,24 a 0,90, a 30 m da 0,71 a 2,7. A 30 m già con 0,3°/s un pedone a 1,2 m/s è visto nel 75 % dei casi: serve ≤ 0,1°/s.
4. Un LiDAR a 10 Hz che ruota a 30°/s gira di 3° dentro una scansione, 1,6 m a 30 m (conto): la scansione va raddrizzata con l'IMU prima del resto.

## 4. Che cosa mostrare all'hackathon, in ordine di rischio

1. **Rotazione da fermi.** Muro a 2–3 m, una persona immobile; dieci rotazioni di 30° in circa 1 s. *Smentita:* muro o persona «mobile» in oltre il 10 % delle valutazioni fra l'inizio del giro e 1 s dopo la fine. Il conto prevede: regge fino a 20 ms di ritardo, 15 % a 33 ms, 83 % a 67 ms. **La prova misura anche il ritardo** (`slam-4`): spostamento apparente del muro diviso per la velocità angolare.
2. **Inclinazione.** Uno spessore di ±2° sotto una ruota: il pavimento fra 1,24 e 3 m resta «libero». *Smentita:* oltre il 10 % di celle «occupato» a 3 m. *Braccio che deve fallire:* senza ristima, a 2° il pavimento oltre 2 m è «occupato» (attacco 10). *Controllo inverso:* una scatola di 15 cm a 2 m resta «occupato» 5 volte su 5.
3. **Avanzamento lento.** Due metri a 0,3–0,5 m/s lungo un muro. *Smentita:* falsi oltre il 10 %, o distanza sbagliata di oltre il 6 % sul metro a nastro.
4. **Perdita della posa.** Staccare l'odometria: «affidabilità persa» entro 1 s, la griglia continua, nessun «libero» nuovo su celle non osservate.
5. **Occlusione con la piattaforma che avanza (rischio alto).** Nulla è provato: solo in filmato, e solo se riesce 8 volte su 10.

**Non promettere:** una mappa; una precisione di localizzazione (manca una verità di riferimento); oltre 0,5 m/s; il volo; il sensore sulla testa; che una soglia del nucleo valga in moto; la scala del LiDAR, che qui è un conto.

## 5. Gli innesti per dopo

- **Mappa locale e chiusura dei cicli.** Un riferimento M sopra O: la chiusura sposta M con un salto; tracce e strato 1 restano in O, che non salta. Nessuna mappa produce un «libero»: una chiusura falsa non toglie un avviso.
- **Più veicoli.** Allineamento da GNSS, mappa condivisa od osservazione reciproca; le tracce scambiate portano la covarianza dell'allineamento; il «libero» altrui entra solo se fresco e allineato entro mezza cella.
- **Quota e terza dimensione.** Quota nello stato, griglia a settori sferici o voxel, ombre come coni; cade il piano del suolo e Q4 diventa il requisito dominante.

## 6. Due profili, uno stesso nucleo

«Nel modello» = con l'errore di sorgente ipotizzato; sul vero è tutto NV.

| Requisito | Profilo uncrewed | Profilo indossato |
|---|---|---|
| Q1 imbardata | **rispettato nel modello** dal giroscopio tarato (0 falsi); al limite se non tarato (9 %) | **rispettato nel modello** dallo stesso giroscopio |
| Q2 traslazione | rover: **rispettato nel modello** da ruote al 3 %, al limite al 10 %. Drone con 0,1 m/s: **non rispettato** a 2 m, al limite oltre | **non rispettato** senza odometria (100 %); **rispettato nel modello** con la visuale-inerziale all'1–3 %; che la si ottenga camminando: **NV** |
| Q3 sincronia | 20–30 ms (rover), 73 ms (volo stazionario): **NV**, misurabile con la prova 1 | petto, 27 ms: **NV**; testa, 5,6 ms: **NV**, da non promettere |
| Q4 beccheggio | **non rispettato** dalla sola IMU a 10–30 m; a 2–3 m con il piano ristimato: **NV** (prova 2) | **non rispettato** senza ristima; con la ristima: **NV** |
| Q5 area prevista | a 2–3 m **rispettato per confronto di conti** (errori ipotizzati ≤ 10 cm su 1 s contro 15); a 30 m serve la covarianza di posa: **NV** | **rispettato per confronto di conti** con la visuale-inerziale; **non rispettato** senza |
| Q6 fascia | a 2–3 m **rispettato nel modello** con ritardo ≤ 60 ms; a 10–30 m **non rispettato** se la fascia non scala | petto: **NV**; testa: ritardo utile 20–30 ms, **NV** |
| «Mai libero dove non è osservato» | **non dipende dalla posa** (per costruzione) | **non dipende dalla posa** (per costruzione) |

## Stati e proposte

- **Sostenuto dal modello:** Q1–Q6. **Non risolto:** l'errore relativo vero di ogni sorgente (lo decidono le prove 1–3, con metro a nastro e goniometro); lo strato 1 con la parallasse.
- `slam-1`: residuo d'imbardata dalla correlazione fra le colonne della griglia polare di due fotogrammi. Smentita: residuo oltre 0,5° su un muro liscio.
- `slam-2`: soglia «mobile» con la covarianza di posa. Smentita: falsi oltre l'1 % con σ dichiarata onesta.
- `slam-3`: ombra d'ingresso legata all'identità dell'occlusore. Smentita: un passaggio su 30 con il centro del soggetto nascosto in una cella «libero» mentre il sensore avanza.
- `slam-4`: la rotazione come misura del ritardo. Smentita: stima che cambia di oltre 10 ms fra due serie.
- **Dopo:** all'esperto di fusione la sincronia e il raddrizzamento della scansione; all'avversario `slam-3`.

**Rifare:** in questa cartella, `PYTHONDONTWRITEBYTECODE=1 timeout 300 python3 bilancio_posa.py > risultati.txt`.

**Fonti.** https://github.com/VladyslavUsenko/basalt [A] · https://github.com/introlab/rtabmap [A] · https://github.com/rpng/open_vins [A] · https://github.com/HKUST-Aerial-Robotics/VINS-Fusion [A] · https://github.com/UZ-SLAMLab/ORB_SLAM3 [A] · https://github.com/PRBonn/kiss-icp [A] · https://github.com/hku-mars/FAST_LIO [A] · https://docs.px4.io/main/en/advanced_config/tuning_the_ecl_ekf [A, primi 100 000 caratteri] · https://docs.px4.io/main/en/msg_docs/VehicleOdometry [A] · cuVSLAM https://nvidia-isaac-ros.github.io/concepts/visual_slam/cuvslam/index.html [R] · T265 https://intel.com/content/www/us/en/support/articles/000087450/emerging-technologies/intel-realsense-technology.html [R]
