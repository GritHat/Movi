# RIFERIMENTI — gruppo rif-4 (estensioni f7–f10 e tre file esterni)

Curatore delle fonti (`sciame-fonti`), fase f11, 14 novembre 2026. Tutto ciò che viene dalle cartelle f7–f10 è
**NON ancora vagliato dall'arbitro**: le righe «Usata per» riportano affermazioni dei ruoli, non risultati approvati.
Niente di ciò che segue è provato sull'hardware.

## 0. In testa

**Conteggio** (contato con `grep` sul campo «Verifica» di questo file). **139 voci**: 54 articoli scientifici e prestampe;
18 norme o documenti regolatori; 9 schede tecniche; 14 pagine di costruttore o comunicati; 22 fra documentazione di
software e depositi di codice; 14 insiemi di dati; 8 «altro».
- **Verificate da me oggi: 104** (102 «verificata dal curatore il 14-11-2026» più 2 «dato diverso», anch'esse aperte).
  Attenzione alla profondità, che è scritta voce per voce: in molte ho verificato solo esistenza, autori, titolo, sede
  e identificativo, oppure la frase nel riassunto; le cifre che stanno nel corpo degli articoli restano spesso «aperte
  dal ruolo, non rilette da me».
- **Già verificate dal curatore in f3: 5** (`scholler2020`, `hsieh2023`, `cao2023`, `st-vl53l7cx`, `st-vl53l8cx`),
  tutte ricontrollate anche oggi e comprese nelle 104.
- **Non verificate da me: 35**, cioè 22 «aperta dal ruolo che la cita» (per alcune ho solo controllato che la pagina
  risponda), 6 «vista solo nel riassunto di un motore di ricerca», 2 «non verificata», 5 «non raggiungibile».

**Nomi degli autori.** Dove la verifica è solo [API Crossref] o [API PubMed] ho letto cognome e iniziale: i nomi di
battesimo per esteso di quelle voci sono a memoria (non verificati alla lettera). Per le voci arXiv e per quelle con
[T] sulla pagina degli autori i nomi sono letti.

**Ore.** Primo elenco dei file alle 16:10:56 (`date -Is`): 90 file `.md` in f7–f10 (escluse `ambiente/` e
`scaricati/`) più i tre esterni. Secondo elenco alle 16:12:02: in più `f10-dati/03-infrastruttura/AMBIENTE.md`. Alle
16:18 ho trovato altri tre file scritti fra le 16:13 e le 16:14 (`f10-dati/02-sensori/MODELLO_SENSORE.md`,
`VALIDAZIONE_MODELLO.md`, `f10-dati/04-embedded/INVENTARIO_E_DECISIONE.md`): di questi ho letto solo le righe delle
fonti. Verifica in rete dalle 16:12:28 alle 16:20 circa. Ciò che i ruoli hanno scritto dopo le 16:18 non c'è.

**Come ho verificato (sigle usate nel campo «Verifica»).**
- **[API]**: dati bibliografici letti oggi nella risposta dell'interfaccia pubblica di arXiv, Crossref, PubMed/PMC o
  Zenodo (è il registro dell'editore o dell'archivio, non il PDF). Per arXiv la risposta contiene anche il riassunto:
  una frase «presente nel riassunto» è stata cercata lì con una ricerca testuale.
- **[T]**: pagina o PDF scaricato oggi con `curl` (PDF convertito con `pdftotext`) e frase o cifra trovata con una
  ricerca testuale nel testo. È la verifica più forte che ho fatto.
- **[200]**: la pagina risponde (HTTP 200) ma non ne ho riletto il contenuto.
- Sigle dei ruoli, riportate come stanno: A / [A] aperta con lo strumento che riassume; A-g / [g] frase trovata nel
  testo scaricato; R / [r] vista solo nel riassunto di un motore di ricerca.

**Indipendenza.** Condivido il modello linguistico con i ruoli che citano: l'indipendenza sta solo nelle risposte dei
server. Crossref e arXiv garantiscono autori, titolo, sede e identificativo; NON garantiscono che la cifra citata sia
nel testo, salvo dove ho scritto [T] o «presente nel riassunto».

**Regole violate o scostamenti (anche per errore).**
1. Nessuna previsione scritta prima delle verifiche (regola 3): le ho lanciate direttamente.
2. Non ho tenuto `stato.md`.
3. I file scaricati per la verifica (circa 60 MB, mai eseguiti; solo `pdftotext` e ricerche testuali) stanno nella
   cartella temporanea della sessione, non nella cartella di consegna; non li ho copiati nel progetto.
4. Estrazione dei riferimenti fatta con ricerche testuali (link, arXiv, DOI, anni, sigle di norme, nomi noti) su
   tutti i file, e lettura per intero solo dei file con più fonti (`f8-continuita/07-ricercatore/FONTI.md`,
   `f10-dati/01-ricercatore/DATI_PUBBLICI.md`, `f9-preproposta/07-lidar/CONSEGNA.md`, e le sezioni «Fonti» delle altre
   consegne). Un riferimento citato solo a parole, senza link, anno o sigla, può essermi sfuggito: **non verificato
   che l'elenco sia completo**.
5. Le copie di pagine altrui in `f10-dati/01-ricercatore/pagine/` (README di DepthTrack, DROW, HUM4D, RealSense)
   contengono molti link interni (per esempio 40 DOI Zenodo dei singoli archivi di DepthTrack, LaSOT, GOT-10k, COCO,
   TrackingNet, DenseDepth, DPT): non sono citazioni dello sciame e non hanno una voce propria.
6. dblp ha risposto con un controllo anti-automi: non l'ho aggirato (i dati di Koch 2007 vengono da Crossref).
   iso.org, sciencedirect.com e skybrary.aero hanno rifiutato o chiesto JavaScript: voci segnate «non raggiungibile».

**Voci inesistenti.** Nessuna fra quelle controllate: i 35 identificativi arXiv citati nei file (più 2 aggiunti da me
per gli insiemi di dati) esistono tutti, con titolo e autori coerenti con la citazione. Non ho potuto controllare
`hunt2013`, `weitz2013` e `sciencedirect-s0926580524005867`, che nei file non hanno titolo: per queste tre
l'esistenza resta **non verificata**.

**Voci attribuite male o imprecise (correzioni).**
- C1. `park2026` (HUM4D): citato come «CVPR 2026»; la pagina del progetto dice «IEEE/CVF CVPR 2026, 4D World Models
  Workshop»: è un articolo di workshop. Titolo vero: «A Dataset and Evaluation for Complex 4D Markerless Human Motion
  Capture» [T].
- C2. `duberg2020` (UFOMap): la frase «real-time (2 Hz) at 2 mm» sta nella didascalia di una figura del README del
  deposito [T], non nell'articolo; il riassunto dell'articolo dice «high resolution (below 1 cm)» [API].
- C3. `eurocontrol-asterix-cat062`: il ruolo ha letto l'edizione 1.18 in una copia non ufficiale; la pagina ufficiale
  elenca come ultima l'**edizione 1.21 (5 giugno 2025)** [T]. Le definizioni citate (bit CST, I062/290, I062/500) le ho
  ritrovate nella copia 1.18 [T]; sulla 1.21 non le ho rilette.
- C4. `cheraghipouria2026`: il primo autore è «Fatemeh Cheraghi Pouria» (in `FONTI.md` è scritto «Pouria»).
- C5. `kress2021`: non è solo una prestampa: IEEE Transactions on Intelligent Vehicles 8(3):2592–2603, 2023.
- C6. `hetzel2024`: «sede non indicata» in `FONTI.md`; Crossref la dà come capitolo in Lecture Notes in Computer
  Science, 2025, pp. 135–152 (quale convegno: non verificato).
- C7. `skoglar2012`: il DOI citato esiste ed è «Pedestrian tracking with an infrared sensor using road network
  information»; che tratti l'«evidenza negativa nei filtri» non è verificato (non è nel titolo; testo non letto).
- C8. `kayukawa2019` (BBeep): la stringa citata «6 blind participants» non è nel testo estratto; ci sono «six blind
  users» e «blind participants»: il numero torna, la citazione testuale no.
- C9. `joslyn2021` e `machado2009` hanno una rettifica pubblicata (corrigendum 2022; correzioni 2010): nessun ruolo la
  cita. Non ho letto che cosa correggono.
- C10. `iata-enhanced-gse-2022`: il 42 % è la riduzione del «current expected ground damage cost per turn rate» se
  il 75 % della flotta dei mezzi passa ai mezzi evoluti, stima dell'associazione [T]; in
  `f7-estensione/05-esperto-dominio/CONSEGNA.md` la condizione del 75 % non è scritta.
- C11. Parametri predefiniti di OctoMap: `f7-estensione/08-creativo/CONSEGNA.md` cita la documentazione di MRPT
  (libreria terza); la fonte primaria è il sorgente di OctoMap, dove ho ritrovato 0,7 / 0,4 / 0,1192 / 0,971 [T].

**Link morti o illeggibili oggi.** `journal-aviation-donecle` (404); il PDF di `scholl1999` su ruccs.rutgers.edu (404:
usare il DOI); `sciencedirect-s0926580524005867` (403); `skybrary-acas-ra-ta` (controllo JavaScript); iso.org (403).

**Cifre che non tornano.** Nessuna smentita fra quelle ricontrollate [T] o nel riassunto: DiffMOT 22,7 fps e 62,3 %
HOTA; PlugTrack 34 %; Khurana +11,4 % e +5,0 %; Padilla 0,70 / 0,39 / 64,15 % / 99,68 % / N = 179; zonotopi 90,9 %;
Bonxai 1165 µs contro 25 522 µs; nvblox 177×; Ahn (coefficienti 0,001063, 0,0007278, 0,003949); IATA 10 miliardi, 40 %,
42 %; NHC due terzi su 5 anni; ASTERIX 63,75 s; kernel fino al 6.14 per librealsense 2.59.1. **Passano da «solo
riassunto» a verificato:** l'RTX 3090 di DiffMOT [T]; la sede di Lindemann 2023 (RA-L), Cleaveland 2024 (AAAI),
Tokmakov 2021 (ICCV), il primo autore di TAP-Vid (Doersch). **Restano non verificate:** tutte le cifre che stanno solo
nel corpo degli articoli e che non ho riletto (lo dico voce per voce).

**Che cosa propongo dopo** (per chi unisce i gruppi e per l'arbitro).
1. Prima di portare una cifra in un documento, rileggerla nel testo per le voci dove ho scritto «non rilette da me»:
   `hetzel2024`, `mercat2019`, `lindemann2023`, `krejci2026`, `doersch2022`, le tabelle di `st-vl53l7cx` e
   `st-vl53l8cx`, la Tabella 3 di `imo-msc192-79`, la Tabella 16 di `eurocontrol-acas-guide`.
2. Non usare come sostegno: `skoglar2012`, `hunt2013`, `weitz2013`, `sciencedirect-s0926580524005867`,
   `journal-aviation-donecle`, `sick-sensori-3d`, `sofema-attrezzi-fod`, `iso-13855` (C = 0,85 m), `iso-9241-303`.
3. Sostituire i link: `scholl1999` con il DOI; i parametri di OctoMap con il sorgente; `skybrary-acas-ra-ta` con
   `eurocontrol-acas-guide`; ASTERIX con l'edizione 1.21 dopo aver riletto i tre campi.
4. Fissare versione o commit per i depositi e le pagine «latest» (oggi nessun ruolo l'ha annotato).
5. All'unione: le chiavi `scholler2020`, `cao2023`, `hsieh2023`, `octomap`, `st-vl53l7cx`, `st-vl53l8cx`,
   `marvel2017` compaiono con ogni probabilità anche negli altri gruppi (fasi f1–f6): vanno fuse, non duplicate.

**Esito sui tre file esterni.**
- `promptMare.txt`: nessun link e nessun riferimento bibliografico (solo nomi di tecniche: filtro di Kalman, IMM,
  griglia d'occupazione bayesiana). Nessuna voce.
- `prepropostaEsterna.md`: nessun link e nessun riferimento bibliografico; nomina «ABAR/ACAS», «OC-SORT-like»,
  «VL53L7CX/L8CX» senza fonte. Le fonti su questi nomi le hanno portate i ruoli di f9 (voci sotto).
- `bozza_iniziale/Proposta MLE Matrice Bayesiana (1).md`: quattro link (grid_map, Nav2, OctoMap, NavWear), voci sotto.
  Le citazioni interne del tipo `<Cite ref="turn…search…">` sono rimandi opachi dello strumento che ha prodotto la
  bozza: non ricostruibili, **non verificati**. Il link gptaha.com è una filigrana dell'esportazione, non una fonte.

---

## A. Articoli scientifici, prestampe, tesi

### hetzel2024
Tipo: articolo scientifico
Autori: Manuel Hetzel; Hannes Reichert; Konrad Doll; Bernhard Sick
Titolo: Reliable Probabilistic Human Trajectory Prediction for Autonomous Applications
Sede e anno: prestampa arXiv, v2 del 10-10-2024; Crossref: capitolo in Lecture Notes in Computer Science (Springer), 2025, pp. 135–152 (convegno: non verificato)
Identificativo: arXiv:2410.06905; DOI 10.1007/978-3-031-91585-7_9
Link: https://arxiv.org/html/2410.06905v2
Verifica: verificata dal curatore il 14-11-2026 [API] per autori, titolo, date e sede; le cifre e la frase citata NON sono nel riassunto: aperte dal ruolo che la cita (A, versione HTML), non rilette da me
Usata per: affidabilità per livello e orizzonte e nitidezza come misura; soglia R_avg ≥ 0,95 e R_min ≥ 0,90; su ETH/UCY Trajectron++ 64,9 / 30,9, Social-Implicit 82,7 / 62,5, MID 84,6 / 65,9, FlowChain 86,5 / 62,2, proposta 91,1 / 72,5; «None of the tested models can achieve suitable Reliability scores» — `f8-continuita/07-ricercatore/FONTI.md` (S1), `CONSEGNA.md` righe 27, 41, 67, `PREVISIONI.md` riga 65
Note: cifre da rileggere nel testo prima di metterle in un documento.

### cheraghipouria2026
Tipo: articolo scientifico (prestampa)
Autori: Fatemeh Cheraghi Pouria; Mahsa Golchoubian; Katherine Driggs-Campbell
Titolo: Rethinking Gaussian Trajectory Predictors: Calibrated Uncertainty for Safe Planning
Sede e anno: arXiv, v1 11-3-2026, v2 12-7-2026; sede di pubblicazione: manca
Identificativo: arXiv:2603.10407
Link: https://arxiv.org/abs/2603.10407
Verifica: verificata dal curatore il 14-11-2026 [API]: frase «…Negative Log-Likelihood loss, which is prone to predict over- or under-confident distributions» presente nel riassunto
Usata per: la perdita NLL dà distribuzioni troppo o troppo poco sicure — `f8-continuita/07-ricercatore/FONTI.md` (S2), `CONSEGNA.md` riga 41
Note: correzione C4 (cognome del primo autore). Nessun numero citato.

### kress2021
Tipo: articolo scientifico
Autori: Viktor Kress; Fabian Jeske; Stefan Zernetsch; Konrad Doll; Bernhard Sick
Titolo: Pose and Semantic Map Based Probabilistic Forecast of Vulnerable Road Users' Trajectories
Sede e anno: IEEE Transactions on Intelligent Vehicles 8(3):2592–2603, 2023; prestampa arXiv 4-6-2021
Identificativo: DOI 10.1109/TIV.2022.3149624; arXiv:2106.02598
Link: https://arxiv.org/abs/2106.02598
Verifica: verificata dal curatore il 14-11-2026 [API]: «reliability, sharpness, and positional accuracy» e orizzonte 2,52 s presenti nel riassunto; la frase sulle curve «troppo sicure» non è nel riassunto: non verificata
Usata per: previsioni valutate per affidabilità, nitidezza e accuratezza, orizzonte 2,52 s — `f8-continuita/07-ricercatore/FONTI.md` (S3)
Note: correzione C5.

### postnikov2021
Tipo: articolo scientifico (prestampa)
Autori: Aleksey Postnikov; Aleksander Gamayunov; Gonzalo Ferrer
Titolo: CovarianceNet: Conditional Generative Model for Correct Covariance Prediction in Human Motion Prediction
Sede e anno: arXiv, 7-9-2021; sede di pubblicazione: manca
Identificativo: arXiv:2109.02965
Link: https://arxiv.org/abs/2109.02965
Verifica: verificata dal curatore il 14-11-2026 [API] solo per esistenza, autori e titolo
Usata per: citata come pista, senza affermazione — `f8-continuita/07-ricercatore/FONTI.md` (riga di S3, marca R)
Note: nessun dato ne dipende.

### scholler2020
Tipo: articolo scientifico
Autori: Christoph Schöller; Vincent Aravantinos; Florian Lay; Alois Knoll
Titolo: What the Constant Velocity Model Can Teach Us About Pedestrian Motion Prediction
Sede e anno: IEEE Robotics and Automation Letters 5(2):1696–1703, 2020
Identificativo: DOI 10.1109/LRA.2020.2969925; arXiv:1903.07933
Link: https://arxiv.org/abs/1903.07933
Verifica: verificata dal curatore il 14-11-2026 [API] per i dati bibliografici; già verificata dal curatore in f3 (F14, cifre della Tabella I trovate nel testo: `f3/fonti/FONTI_VERIFICATE.md`); cifre non rilette oggi
Usata per: a 4,8 s velocità costante 0,39 / 0,83 m, miglior appreso deterministico 0,44 / 0,91, generativo a 20 campioni 0,32 / 0,60 — `f8-continuita/07-ricercatore/FONTI.md` (S7), `CONSEGNA.md` righe 56 e 93
Note: pedoni in campo aperto, senza occlusione.

### uhlemann2024
Tipo: articolo scientifico
Autori: Nico Uhlemann; Felix Fent; Markus Lienkamp
Titolo: Evaluating Pedestrian Trajectory Prediction Methods with Respect to Autonomous Driving
Sede e anno: IEEE Transactions on Intelligent Transportation Systems, 2024 (volume e pagine: non letti); arXiv v3 5-4-2024
Identificativo: DOI 10.1109/TITS.2024.3386195; arXiv:2308.05194
Link: https://arxiv.org/abs/2308.05194
Verifica: verificata dal curatore il 14-11-2026 [API]: frase «a constant velocity model (CVM) provides a good approximation of the overall dynamics in the majority of cases» presente nel riassunto
Usata per: la velocità costante è una buona approssimazione nella maggior parte dei casi — `f8-continuita/07-ricercatore/FONTI.md` (S8), `CONSEGNA.md` riga 56
Note: nessun numero citato.

### mercat2019
Tipo: articolo scientifico (prestampa)
Autori: Jean Mercat; Nicole El Zoghby; Guillaume Sandou; Dominique Beauvois; Guillermo Pita Gil
Titolo: Kinematic Single Vehicle Trajectory Prediction Baselines and Applications with the NGSIM Dataset
Sede e anno: arXiv, v4 28-10-2020; sede di pubblicazione: manca
Identificativo: arXiv:1908.11472
Link: https://ar5iv.labs.arxiv.org/html/1908.11472
Verifica: verificata dal curatore il 14-11-2026 [API] per autori, titolo e date; la tabella degli RMSE non è nel riassunto: aperta dal ruolo che la cita (A, copia ar5iv), non riletta da me
Usata per: veicoli (NGSIM): RMSE a 1–5 s del Kalman a velocità costante 0,75 / 1,81 / 3,16 / 4,80 / 6,70 m, V-LSTM 0,67 / 1,62 / 2,86 / 4,40 / 6,26, Kalman-LSTM 0,68 / 1,54 / 2,72 / 4,20 / 5,95; NLL — `f8-continuita/07-ricercatore/FONTI.md` (S9), `CONSEGNA.md` riga 58
Note: veicoli in autostrada, non pedoni; ar5iv è una copia di terzi del testo arXiv.

### kim2026
Tipo: articolo scientifico
Autori: Seungjae Kim; SeungJoon Lee; MyeongAh Cho
Titolo: PlugTrack: Multi-Perceptive Motion Analysis for Adaptive Fusion in Multi-Object Tracking
Sede e anno: Proceedings of the AAAI Conference on Artificial Intelligence 40(7):5709–5716, 2026
Identificativo: DOI 10.1609/aaai.v40i7.37491; arXiv:2511.13105
Link: https://arxiv.org/abs/2511.13105
Verifica: verificata dal curatore il 14-11-2026 [API] e [T]: «Kalman filter outperforms data-driven predictors in up to 34% of cases» nel riassunto; nel testo HTML v1: su DanceTrack il 34 % dei tracciati (1 700 su 5 000)
Usata per: il Kalman batte i predittori appresi fino al 34 % dei casi anche su moto non lineare — `f8-continuita/07-ricercatore/FONTI.md` (S10), `CONSEGNA.md` righe 57 e 80
Note: riquadri in immagini, non posizioni al suolo.

### lv2024
Tipo: articolo scientifico
Autori: Weiyi Lv; Yuhang Huang; Ning Zhang; Ruei-Sung Lin; Mei Han; Dan Zeng
Titolo: DiffMOT: A Real-time Diffusion-based Multiple Object Tracker with Non-linear Prediction
Sede e anno: IEEE/CVF CVPR 2024, pp. 19321–19330
Identificativo: DOI 10.1109/CVPR52733.2024.01828; arXiv:2403.02075
Link: https://arxiv.org/abs/2403.02075
Verifica: verificata dal curatore il 14-11-2026 [API] e [T]: 22,7 fps e 62,3 % HOTA su DanceTrack nel riassunto; «real-time at 22.7 FPS on an RTX 3090 machine» nel testo HTML v2 (in `FONTI.md` l'hardware era solo R: ora verificato)
Usata per: danza e sport, 22,7 fps con scheda grafica — `f8-continuita/07-ricercatore/FONTI.md` (riga di S10), `CONSEGNA.md` riga 59
Note: richiede GPU.

### lindemann2023
Tipo: articolo scientifico
Autori: Lars Lindemann; Matthew Cleaveland; Gihyun Shim; George J. Pappas
Titolo: Safe Planning in Dynamic Environments Using Conformal Prediction
Sede e anno: IEEE Robotics and Automation Letters 8(8):5116–5123, 2023
Identificativo: DOI 10.1109/LRA.2023.3292071; arXiv:2210.10254
Link: https://arxiv.org/abs/2210.10254
Verifica: verificata dal curatore il 14-11-2026 [API] per i dati bibliografici (la sede RA-L 2023 era solo R: confermata); le frasi e il 498 su 500 non sono nel riassunto: trovate dal ruolo nel testo estratto (A-g), non rilette da me
Usata per: ipotesi 2 (traiettorie di taratura «independently drawn from D»), nota 3 («In general only exchangeability is needed»), 498 su 500 dentro la regione al 95 % (δ = 0,05, T = 20), prudenza per l'unione dei limiti — `f8-continuita/07-ricercatore/FONTI.md` (S4), `CONSEGNA.md` righe 43–44, 108
Note: la garanzia vale solo se taratura e prova vengono dalla stessa distribuzione.

### cleaveland2024
Tipo: articolo scientifico
Autori: Matthew Cleaveland; Insup Lee; George J. Pappas; Lars Lindemann
Titolo: Conformal Prediction Regions for Time Series Using Linear Complementarity Programming
Sede e anno: Proceedings of the AAAI Conference on Artificial Intelligence 38(19):20984–20992, 2024
Identificativo: DOI 10.1609/aaai.v38i19.30089; arXiv:2304.01075
Link: https://arxiv.org/abs/2304.01075
Verifica: verificata dal curatore il 14-11-2026 [API]: «prediction regions that are not conservative» e i predittori di pedoni presenti nel riassunto; sede AAAI 2024 confermata (era R)
Usata per: regioni conformi su più passi non prudenti — `f8-continuita/07-ricercatore/FONTI.md` (S5), `CONSEGNA.md` riga 80
Note: nessun numero citato.

### dixit2022
Tipo: articolo scientifico (prestampa)
Autori: Anushri Dixit; Lars Lindemann; Skylar Wei; Matthew Cleaveland; George J. Pappas; Joel W. Burdick
Titolo: Adaptive Conformal Prediction for Motion Planning among Dynamic Agents
Sede e anno: arXiv, 1-12-2022; «L4DC 2023» secondo il ruolo: non verificata (non è in Crossref)
Identificativo: arXiv:2212.00278
Link: https://arxiv.org/abs/2212.00278
Verifica: verificata dal curatore il 14-11-2026 [API]: «distribution-free», osservazioni ritardate («delayed agent observations»), drone e frisbee presenti nel riassunto; sede non verificata
Usata per: la variante adattiva usa le osservazioni ritardate degli agenti — `f8-continuita/07-ricercatore/FONTI.md` (S6), `CONSEGNA.md` riga 46
Note: «in simulazione» non ricontrollato.

### rahaman2026
Tipo: articolo scientifico (prestampa)
Autori: Kaizer Rahaman; Jyotirmoy V. Deshmukh; Ashish R. Hota; Lars Lindemann
Titolo: When Environments Shift: Safe Planning with Generative Priors and Robust Conformal Prediction
Sede e anno: arXiv, 13-2-2026; sede: manca
Identificativo: arXiv:2602.12616
Link: https://arxiv.org/abs/2602.12616
Verifica: verificata dal curatore il 14-11-2026 [API]: esiste; «ORCA» e «distribution shift» presenti nel riassunto
Usata per: pista sulla conforme robusta sotto cambio di distribuzione — `f8-continuita/07-ricercatore/FONTI.md` (§2, marca R)
Note: nessun dato ne dipende.

### yao2025
Tipo: articolo scientifico
Autori: Jianpeng Yao; Xiaopan Zhang; Yu Xia; Zejin Wang; Amit K. Roy-Chowdhury; Jiachen Li
Titolo: Towards Generalizable Safety in Crowd Navigation via Conformal Uncertainty Handling
Sede e anno: 9th Conference on Robot Learning (CoRL 2025), secondo il commento arXiv; arXiv 7-8-2025
Identificativo: arXiv:2508.05634
Link: https://arxiv.org/abs/2508.05634
Verifica: verificata dal curatore il 14-11-2026 [API] solo per esistenza, autori, titolo
Usata per: pista sulla conforme adattiva nella navigazione fra la folla — `f8-continuita/07-ricercatore/FONTI.md` (§2, marca R)
Note: nessun dato ne dipende.

### zhang2026
Tipo: articolo scientifico (prestampa)
Autori: Zhen Zhang; Amr Alanwar
Titolo: Hybrid Probabilistic Zonotopes for Identifiable and Refinable Predictive Uncertainty
Sede e anno: arXiv, 5-8-2026; sede: manca
Identificativo: arXiv:2608.05454
Link: https://arxiv.org/abs/2608.05454
Verifica: verificata dal curatore il 14-11-2026 [API] e [T]: nel testo HTML v1 «OOD coverage holds: 90.9% ETH/UCY leave-one-out average»; il livello nominale del 90 % e «non per orizzonte» non ricontrollati
Usata per: copertura media 90,9 % al nominale 90 %, una scena di ETH/UCY tenuta fuori a turno — `f8-continuita/07-ricercatore/FONTI.md` (§2, marca R)
Note: la cifra non è nel riassunto, solo nel corpo.

### tokmakov2021
Tipo: articolo scientifico
Autori: Pavel Tokmakov; Jie Li; Wolfram Burgard; Adrien Gaidon
Titolo: Learning to Track with Object Permanence
Sede e anno: IEEE/CVF ICCV 2021, pp. 10840–10849
Identificativo: DOI 10.1109/ICCV48922.2021.01068; arXiv:2103.14258
Link: https://arxiv.org/abs/2103.14258
Verifica: verificata dal curatore il 14-11-2026 [API]: sede ICCV 2021 confermata (nel file era «a memoria»); «ground truth annotations for invisible objects» presente nel riassunto
Usata per: la verità in occlusione esiste in dati sintetici — `f8-continuita/07-ricercatore/FONTI.md` (S11), `CONSEGNA.md` riga 65, `PREVISIONI.md` riga 68
Note: —

### hsieh2023
Tipo: articolo scientifico (prestampa)
Autori: Cheng-Yen Hsieh; Kaihua Chen; Achal Dave; Tarasha Khurana; Deva Ramanan
Titolo: TAO-Amodal: A Benchmark for Tracking Any Object Amodally
Sede e anno: arXiv, v3 2-4-2024; sede: manca
Identificativo: arXiv:2312.12433
Link: https://arxiv.org/abs/2312.12433
Verifica: verificata dal curatore il 14-11-2026 [API]: «struggle to detect and track objects under heavy occlusion» presente nel riassunto; già verificata dal curatore in f3 (F20)
Usata per: riquadri amodali come verità in occlusione; i metodi faticano in occlusione pesante — `f8-continuita/07-ricercatore/FONTI.md` (S12), `CONSEGNA.md` riga 65
Note: —

### krejci2026
Tipo: articolo scientifico
Autori: Jan Krejčí; Oliver Kost; Yuxuan Xia; Lennart Svensson; Ondřej Straka
Titolo: Occlusion-Aware Multi-Object Tracking via Expected Probability of Detection
Sede e anno: IEEE Transactions on Aerospace and Electronic Systems, vol. 62, pp. 8211–8228, 2026; arXiv v3 8-4-2026
Identificativo: DOI 10.1109/TAES.2026.3676431; arXiv:2511.20239
Link: https://arxiv.org/abs/2511.20239
Verifica: verificata dal curatore il 14-11-2026 [API] per i dati bibliografici; le frasi citate sono nel corpo: trovate dal ruolo nel testo estratto (A-g), non rilette da me
Usata per: probabilità di rilevamento legata alla visibilità; prove su tre video di MOT17 con «The visibility ratio is available for each GT BB»; «computational complexities are hardly predictable»; più stime di oggetti occlusi danno più falsi positivi — `f8-continuita/07-ricercatore/FONTI.md` (S13), `CONSEGNA.md` righe 66, 68, 79
Note: —

### vanhoorick2023
Tipo: articolo scientifico
Autori: Basile Van Hoorick; Pavel Tokmakov; Simon Stent; Jie Li; Carl Vondrick
Titolo: Tracking Through Containers and Occluders in the Wild
Sede e anno: IEEE/CVF CVPR 2023, pp. 13802–13812
Identificativo: DOI 10.1109/CVPR52729.2023.01326; arXiv:2305.03052
Link: https://arxiv.org/abs/2305.03052
Verifica: verificata dal curatore il 14-11-2026 [API]: «a considerable performance gap» presente nel riassunto
Usata per: resta un divario notevole prima di una vera permanenza dell'oggetto — `f8-continuita/07-ricercatore/FONTI.md` (S14), `CONSEGNA.md` riga 62
Note: —

### doersch2022
Tipo: articolo scientifico
Autori: Carl Doersch; Ankush Gupta; Larisa Markeeva; Adrià Recasens; Lucas Smaira; Yusuf Aytar; João Carreira; Andrew Zisserman; Yi Yang
Titolo: TAP-Vid: A Benchmark for Tracking Any Point in a Video
Sede e anno: NeurIPS 2022, Datasets and Benchmarks track (dal commento arXiv)
Identificativo: arXiv:2211.03726
Link: https://arxiv.org/html/2211.03726v2
Verifica: verificata dal curatore il 14-11-2026 [API]: primo autore e sede confermati (nel file erano «a memoria»); le due frasi citate sono nel corpo: aperte dal ruolo che la cita (A), non rilette da me
Usata per: la precisione di posizione vale «only for frames where the point is visible»; in occlusione la posizione «is typically assumed to be meaningless» — `f8-continuita/07-ricercatore/FONTI.md` (S15), `CONSEGNA.md` righe 61, 65
Note: —

### khurana2021
Tipo: articolo scientifico
Autori: Tarasha Khurana; Achal Dave; Deva Ramanan
Titolo: Detecting Invisible People
Sede e anno: IEEE/CVF ICCV 2021, pp. 3154–3164; arXiv 15-12-2020
Identificativo: DOI 10.1109/ICCV48922.2021.00316; arXiv:2012.08419
Link: https://arxiv.org/abs/2012.08419
Verifica: verificata dal curatore il 14-11-2026 [API]: «a short-term forecasting challenge», 11,4 % e 5,0 % di F1 presenti nel riassunto
Usata per: l'occlusione trattata come previsione a breve termine; +11,4 % e +5,0 % di F1 — `f8-continuita/07-ricercatore/FONTI.md` (§3)
Note: `FONTI.md` non dava la sede.

### skoglar2012
Tipo: articolo scientifico
Autori: Per Skoglar; Umut Orguner; David Törnqvist; Fredrik Gustafsson
Titolo: Pedestrian tracking with an infrared sensor using road network information
Sede e anno: EURASIP Journal on Advances in Signal Processing, 2012, articolo 26
Identificativo: DOI 10.1186/1687-6180-2012-26
Link: https://doi.org/10.1186/1687-6180-2012-26
Verifica: verificata dal curatore il 14-11-2026 [API] solo per esistenza e dati bibliografici; che tratti l'evidenza negativa: non verificata (testo non letto, né da me né dal ruolo)
Usata per: evidenza negativa nei filtri — `f8-continuita/07-ricercatore/FONTI.md` (S22, marca R), `CONSEGNA.md` riga 18
Note: correzione C7. Non usare come sostegno finché il testo non è letto.

### wyffels2015
Tipo: articolo scientifico
Autori: Kevin Wyffels; Mark Campbell
Titolo: Negative Information for Occlusion Reasoning in Dynamic Extended Multiobject Tracking
Sede e anno: IEEE Transactions on Robotics 31(2):425–442, 2015
Identificativo: DOI 10.1109/TRO.2015.2409413
Link: https://doi.org/10.1109/TRO.2015.2409413
Verifica: verificata dal curatore il 14-11-2026 [API] solo per esistenza e dati bibliografici (in `FONTI.md` mancavano titolo e DOI); testo non letto
Usata per: evidenza negativa nei filtri — `f8-continuita/07-ricercatore/FONTI.md` (S22, marca R)
Note: il titolo è pertinente; nessuna cifra citata.

### koch2007
Tipo: articolo scientifico
Autori: Wolfgang Koch
Titolo: On exploiting 'negative' sensor evidence for target tracking and sensor data fusion
Sede e anno: Information Fusion 8(1):28–39, 2007
Identificativo: DOI 10.1016/j.inffus.2005.09.002
Link: https://dblp.org/rec/journals/inffus/Koch07 (oggi protetto da un controllo anti-automi); https://doi.org/10.1016/j.inffus.2005.09.002
Verifica: verificata dal curatore il 14-11-2026 [API Crossref] solo per i dati bibliografici; la formula con la probabilità di rilevamento: non verificata (lo dice anche il ruolo)
Usata per: fonte sull'evidenza negativa — `f9-preproposta/10-rovesciatore/CONSEGNA.md` riga 64
Note: —

### padilla2017
Tipo: articolo scientifico
Autori: Lace M. Padilla; Ian T. Ruginski; Sarah H. Creem-Regehr
Titolo: Effects of ensemble and summary displays on interpretations of geospatial uncertainty data
Sede e anno: Cognitive Research: Principles and Implications 2(1):40, 2017
Identificativo: DOI 10.1186/s41235-017-0076-1; PMC5626802
Link: https://pmc.ncbi.nlm.nih.gov/articles/PMC5626802
Verifica: verificata dal curatore il 14-11-2026 [API] e [T]: nel testo della pagina PMC compaiono 0,70, 0,39, 64,15, 99,68 e 179; d = 0,66 e N = 43, 35 non ricontrollati
Usata per: con il cono la quota che dice «l'uragano cresce» è 0,70 contro 0,39 con l'insieme (d = 0,66, N = 179); con l'insieme, impianto più vicino scelto nel 64,15 % invece del 99,68 % — `f8-continuita/07-ricercatore/FONTI.md` (S19), `CONSEGNA.md` righe 72, 120, 122; `f8-continuita/06-visualizzatore/CONSEGNA.md` riga 43
Note: mappe meteo e non esperti: altro dominio.

### kayukawa2019
Tipo: articolo scientifico
Autori: Seita Kayukawa; Keita Higuchi; João Guerreiro; Shigeo Morishima; Yoichi Sato; Kris Kitani; Chieko Asakawa
Titolo: BBeep: A Sonic Collision Avoidance System for Blind Travellers and Nearby Pedestrians
Sede e anno: CHI Conference on Human Factors in Computing Systems (CHI 2019), pp. 1–12
Identificativo: DOI 10.1145/3290605.3300282
Link: https://wotipati.github.io/projects/BBeep/paper/CHI'19_BBeep_preprint.pdf
Verifica: verificata dal curatore il 14-11-2026 [API] e [T]: nel PDF «…linear extrapolation is used to predict their future path», soglie a 5,0 s e 2,5 s, prova in un aeroporto internazionale con «six blind users»; la stringa «6 blind participants» come citata non c'è (correzione C8)
Usata per: previsione per estrapolazione lineare, avviso a 5 s e a 2,5 s, sei partecipanti non vedenti, nessuna incertezza in uscita — `f8-continuita/07-ricercatore/FONTI.md` (S20), `CONSEGNA.md` riga 74
Note: Crossref registra il titolo come «BBeep»; titolo completo e nomi degli autori letti nel PDF [T]. È la prestampa degli autori, non la versione dell'editore.

### haghighi2024
Tipo: articolo scientifico (prestampa)
Autori: Yasaman Haghighi; Celine Demonsant; Panagiotis Chalimourdas; Maryam Tavasoli Naeini; Jhon Kevin Munoz; Bladimir Bacca; Silvan Suter; Matthieu Gani; Alexandre Alahi
Titolo: HEADS-UP: Head-Mounted Egocentric Dataset for Trajectory Prediction in Blind Assistance Systems
Sede e anno: arXiv, 30-9-2024; sede: manca
Identificativo: arXiv:2409.20324
Link: https://arxiv.org/html/2409.20324v1
Verifica: verificata dal curatore il 14-11-2026 [API]: «Jetson» e ausilio per non vedenti presenti nel riassunto
Usata per: insieme egocentrico per la previsione di pedoni in un ausilio; nessun numero sugli utenti — `f8-continuita/07-ricercatore/FONTI.md` (S21), `CONSEGNA.md` riga 74
Note: l'assenza di numeri sugli utenti è un'assenza su ciò che il ruolo ha letto.

### hunt2013
Tipo: altro (tesi, secondo il ruolo)
Autori: Hunt (nome: manca)
Titolo: manca
Sede e anno: 2013; istituzione: manca
Identificativo: manca
Link: manca
Verifica: vista solo nel riassunto di un motore di ricerca (dal ruolo); non cercata da me: dati insufficienti
Usata per: fiducia dei controllori e incertezza della previsione — `f8-continuita/07-ricercatore/FONTI.md` (§5, marca R)
Note: non citabile così com'è.

### weitz2013
Tipo: altro (rapporto DLR, secondo il ruolo)
Autori: Weitz (nome: manca)
Titolo: manca
Sede e anno: 2013, DLR
Identificativo: manca
Link: manca
Verifica: vista solo nel riassunto di un motore di ricerca (dal ruolo); non cercata da me: dati insufficienti
Usata per: ellissoidi d'incertezza per traiettorie 4D, senza esperimento con controllori — `f8-continuita/07-ricercatore/FONTI.md` (§5, marca R)
Note: non citabile così com'è.

### angelopoulos2021
Tipo: articolo scientifico (prestampa, guida)
Autori: Anastasios N. Angelopoulos; Stephen Bates
Titolo: A Gentle Introduction to Conformal Prediction and Distribution-Free Uncertainty Quantification
Sede e anno: arXiv, v6 7-12-2022; versione a stampa: non verificata
Identificativo: arXiv:2107.07511
Link: https://arxiv.org/abs/2107.07511
Verifica: verificata dal curatore il 14-11-2026 [API] per autori e titolo; la condizione di scambiabilità non è nel riassunto: non riletta (lo dichiara anche il ruolo)
Usata per: la copertura marginale promessa dalla teoria, a fronte di 0,893–0,905 misurato nel complesso (`risultati` del ruolo) — `f8-continuita/03-kalman/CONSEGNA.md` riga 30; `f8-continuita/04-statistico/CONSEGNA.md` riga 88
Note: garantisce la copertura in media, non per comportamento.

### barber2019
Tipo: articolo scientifico (prestampa)
Autori: Rina Foygel Barber; Emmanuel J. Candès; Aaditya Ramdas; Ryan J. Tibshirani
Titolo: The limits of distribution-free conditional predictive inference
Sede e anno: arXiv, v2 15-4-2020; versione a stampa: non verificata
Identificativo: arXiv:1903.04684
Link: https://arxiv.org/abs/1903.04684
Verifica: verificata dal curatore il 14-11-2026 [API] per autori e titolo; il ruolo ha letto solo il riassunto
Usata per: la copertura condizionata esatta è impossibile senza ipotesi («Barber e altri») — `f8-continuita/04-statistico/CONSEGNA.md` righe 43 e 88
Note: l'enunciato preciso del teorema non è stato riletto da nessuno.

### gibbs2021
Tipo: articolo scientifico (prestampa)
Autori: Isaac Gibbs; Emmanuel Candès
Titolo: Adaptive Conformal Inference Under Distribution Shift
Sede e anno: arXiv, v3 28-10-2021; versione a stampa: non verificata
Identificativo: arXiv:2106.00170
Link: https://arxiv.org/abs/2106.00170
Verifica: verificata dal curatore il 14-11-2026 [API] per autori e titolo; il ruolo ha letto solo il riassunto
Usata per: conforme adattiva sotto cambio di distribuzione — `f8-continuita/04-statistico/CONSEGNA.md` riga 88
Note: —

### gneiting2007
Tipo: articolo scientifico
Autori: Tilmann Gneiting; Adrian E. Raftery
Titolo: Strictly Proper Scoring Rules, Prediction, and Estimation
Sede e anno: Journal of the American Statistical Association 102(477):359–378, 2007
Identificativo: DOI 10.1198/016214506000001437
Link: https://sites.stat.washington.edu/raftery/Research/PDF/Gneiting2007jasa.pdf
Verifica: verificata dal curatore il 14-11-2026 [API] e [T]: PDF aperto, «energy score» e «interval score» presenti; i numeri delle equazioni (21, 22, 43) non ricontrollati: letti dal ruolo
Usata per: punteggi propri (CRPS, punteggio d'energia, punteggio dell'intervallo) per valutare le previsioni — `f8-continuita/04-statistico/CONSEGNA.md` riga 88
Note: —

### joslyn2021
Tipo: articolo scientifico
Autori: Susan Joslyn; Sonia Savelli
Titolo: Visualizing Uncertainty for Non-Expert End Users: The Challenge of the Deterministic Construal Error
Sede e anno: Frontiers in Computer Science, vol. 2, articolo 590232, 18-1-2021
Identificativo: DOI 10.3389/fcomp.2020.590232
Link: https://www.frontiersin.org/journals/computer-science/articles/10.3389/fcomp.2020.590232/full
Verifica: verificata dal curatore il 14-11-2026 [API] e [T]: «deterministic construal error» presente (17 volte)
Usata per: il cono d'incertezza è letto come estensione dell'oggetto — `f8-continuita/06-visualizzatore/CONSEGNA.md` riga 43
Note: esiste un corrigendum (Frontiers in Computer Science 4, 2022, DOI 10.3389/fcomp.2022.1093379): non letto (C9).

### maceachren2012
Tipo: articolo scientifico
Autori: Alan M. MacEachren; Robert E. Roth; James O'Brien; Bonan Li; Derek Swingley; Mark Gahegan
Titolo: Visual Semiotics & Uncertainty Visualization: An Empirical Study
Sede e anno: IEEE Transactions on Visualization and Computer Graphics 18(12):2496–2505, 2012
Identificativo: DOI 10.1109/TVCG.2012.279
Link: https://ieeevis.org/year/2012/paper/infovis/visual-semiotics-uncertainty-visualization-empirical-study
Verifica: verificata dal curatore il 14-11-2026 [API] e [T] per i dati bibliografici; l'affermazione (sfocatura, posizione e valore di grigio i più intuitivi) NON è nel riassunto della pagina: non verificata
Usata per: sfocatura, posizione e valore di grigio sono i segni più intuitivi per l'incerto — `f8-continuita/06-visualizzatore/CONSEGNA.md` riga 44
Note: da rileggere nell'articolo.

### boukhelifa2012
Tipo: articolo scientifico
Autori: Nadia Boukhelifa; Anastasia Bezerianos; Tobias Isenberg; Jean-Daniel Fekete
Titolo: Evaluating Sketchiness as a Visual Variable for the Depiction of Qualitative Uncertainty
Sede e anno: IEEE Transactions on Visualization and Computer Graphics 18(12):2769–2778, 2012
Identificativo: DOI 10.1109/TVCG.2012.220
Link: https://tobias.isenberg.cc/p/Boukhelifa2012ESV
Verifica: verificata dal curatore il 14-11-2026 [API] e [T]: «people subjectively prefer dashing style over blur, grayscale and sketchiness» presente nel riassunto sulla pagina dell'autore
Usata per: il tratteggio è preferito a sfocatura e grigio — `f8-continuita/06-visualizzatore/CONSEGNA.md` riga 45
Note: preferenza soggettiva, su linee.

### scholl1999
Tipo: articolo scientifico
Autori: Brian J. Scholl; Zenon W. Pylyshyn
Titolo: Tracking Multiple Items Through Occlusion: Clues to Visual Objecthood
Sede e anno: Cognitive Psychology 38(2):259–290, 1999
Identificativo: DOI 10.1006/cogp.1998.0698
Link: https://ruccs.rutgers.edu/images/tech_rpt/tr-40/scholl.pdf (404 oggi); https://doi.org/10.1006/cogp.1998.0698
Verifica: verificata dal curatore il 14-11-2026 [API] solo per i dati bibliografici; il link citato non è raggiungibile (404) e l'affermazione non è verificata nel testo (il ruolo: solo riassunto)
Usata per: un oggetto resta «lo stesso» dietro un ostacolo solo se scompare e ricompare lungo un bordo fisso — `f8-continuita/06-visualizzatore/CONSEGNA.md` riga 46
Note: sostituire il link con il DOI.

### hullman2015
Tipo: articolo scientifico
Autori: Jessica Hullman; Paul Resnick; Eytan Adar
Titolo: Hypothetical Outcome Plots Outperform Error Bars and Violin Plots for Inferences about Reliability of Variable Ordering
Sede e anno: PLOS ONE 10(11):e0142444, 2015
Identificativo: DOI 10.1371/journal.pone.0142444
Link: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0142444
Verifica: verificata dal curatore il 14-11-2026 [API] e [T]: pagina aperta, titolo e autori presenti
Usata per: esiti possibili animati battono le barre d'errore nei confronti — `f8-continuita/06-visualizzatore/CONSEGNA.md` riga 47
Note: l'affermazione coincide con il titolo.

### vriend2025
Tipo: articolo scientifico
Autori: Sita Vriend; David Hägele; Daniel Weiskopf
Titolo: Two Empirical Studies on Audiovisual Semiotics of Uncertainty
Sede e anno: Audio Mostly 2025 (dal commento arXiv); arXiv 20-5-2025
Identificativo: arXiv:2505.14379
Link: https://arxiv.org/abs/2505.14379
Verifica: verificata dal curatore il 14-11-2026 [API]: nel riassunto «while pitch paired with brightness was preferred as a pair, it was not well suited as a mapping for uncertainty»; «volume e nitidezza i più intuitivi» NON è nel riassunto: non verificata (lo dice anche il ruolo)
Usata per: l'accoppiata altezza–luminosità piace ma non è adatta all'incertezza — `f8-continuita/06-visualizzatore/CONSEGNA.md` riga 48
Note: studi con partecipanti reclutati in rete, non con persone non vedenti.

### orzechowski2018
Tipo: articolo scientifico
Autori: Piotr Franciszek Orzechowski; Annika Meyer; Martin Lauer
Titolo: Tackling Occlusions & Limited Sensor Range with Set-based Safety Verification
Sede e anno: 21st International Conference on Intelligent Transportation Systems (ITSC), 2018
Identificativo: DOI 10.1109/ITSC.2018.8569332; arXiv:1807.01262
Link: https://arxiv.org/abs/1807.01262
Verifica: verificata dal curatore il 14-11-2026 [API]: nel riassunto «The state of occluded obstacles is unknown, but can be over-approximated by intervals over all possible states»
Usata per: stati nascosti sovrastimati con insiemi raggiungibili — `f7-estensione/01-matematico/CONSEGNA.md` riga 78
Note: guida automatica, non una mappa voxel. Nello stesso punto il ruolo dichiara «non verificato» che l'aggiornamento in log-odds presupponga una mappa ferma: resta senza fonte.

### niessner2013
Tipo: articolo scientifico
Autori: Matthias Nießner; Michael Zollhöfer; Shahram Izadi; Marc Stamminger
Titolo: Real-time 3D Reconstruction at Scale using Voxel Hashing
Sede e anno: ACM Transactions on Graphics 32(6), 2013 (Crossref: pp. 1–11)
Identificativo: DOI 10.1145/2508363.2508374
Link: https://niessnerlab.org/projects/niessner2013hashing.html
Verifica: verificata dal curatore il 14-11-2026 [API] e [T]: pagina aperta; «performed at real-time rates on commodity graphics hardware» presente
Usata per: lo schema proiettivo della fusione volumetrica da camere di profondità (lì su GPU), a fronte di 307 ms per il lancio dei raggi e 2,2 ms per il confronto proiettivo misurati dal ruolo — `f7-estensione/03-nuvole-punti/CONSEGNA.md` riga 36
Note: i tempi sono misure del ruolo, non della fonte.

### oleynikova2017
Tipo: articolo scientifico
Autori: Helen Oleynikova; Zachary Taylor; Marius Fehr; Juan Nieto; Roland Siegwart
Titolo: Voxblox: Incremental 3D Euclidean Signed Distance Fields for On-Board MAV Planning
Sede e anno: IEEE/RSJ IROS 2017
Identificativo: DOI 10.1109/IROS.2017.8202315; arXiv:1611.03631
Link: https://arxiv.org/abs/1611.03631
Verifica: verificata dal curatore il 14-11-2026 [API]: «single CPU core» e «real-time» presenti nel riassunto
Usata per: Voxblox «runs in real-time on a single CPU core» — `f7-estensione/05-esperto-dominio/CONSEGNA.md` righe 25 e 80 (S2)
Note: vedi anche `ethz-voxblox`.

### duberg2020
Tipo: articolo scientifico
Autori: Daniel Duberg; Patric Jensfelt
Titolo: UFOMap: An Efficient Probabilistic 3D Mapping Framework That Embraces the Unknown
Sede e anno: IEEE Robotics and Automation Letters 5(4):6411–6418, 2020
Identificativo: DOI 10.1109/LRA.2020.3013861; arXiv:2003.04749
Link: https://arxiv.org/abs/2003.04749
Verifica: verificata dal curatore il 14-11-2026 [API]: «explicit representation of all three states in the map, i.e., occupied, free, and unknown» presente nel riassunto; «real-time (2 Hz) at 2 mm» NON è nell'articolo ma nel README del deposito (correzione C2)
Usata per: UFOMap dichiara lo sconosciuto in modo esplicito; «real-time (2 Hz) at 2 mm» — `f7-estensione/05-esperto-dominio/CONSEGNA.md` righe 26 e 80 (S3)
Note: vedi `ufomap-deposito`.

### millane2024
Tipo: articolo scientifico
Autori: Alexander Millane; Helen Oleynikova; Emilie Wirbel; Remo Steiner; Vikram Ramasamy; David Tingdahl; Roland Siegwart
Titolo: nvblox: GPU-Accelerated Incremental Signed Distance Field Mapping
Sede e anno: IEEE ICRA 2024 (dal commento arXiv); arXiv v2 15-3-2024
Identificativo: arXiv:2311.00626
Link: https://arxiv.org/abs/2311.00626
Verifica: verificata dal curatore il 14-11-2026 [API]: «177x» presente nel riassunto
Usata per: nvblox «up to a 177x speed-up», su GPU — `f7-estensione/05-esperto-dominio/CONSEGNA.md` righe 29 e 80 (S6)
Note: richiede la GPU; la licenza è «NV» (non verificata) nel file.

### usenko2017
Tipo: articolo scientifico
Autori: Vladyslav Usenko; Lukas von Stumberg; Andrej Pangercic; Daniel Cremers
Titolo: Real-Time Trajectory Replanning for MAVs using Uniform B-splines and a 3D Circular Buffer
Sede e anno: IEEE/RSJ IROS 2017, pp. 215–222
Identificativo: DOI 10.1109/IROS.2017.8202160; arXiv:1703.01416
Link: https://arxiv.org/abs/1703.01416
Verifica: verificata dal curatore il 14-11-2026 [API]: «an occupancy grid stored in a three-dimensional circular buffer, which moves together with a drone» presente nel riassunto
Usata per: nel volo la mappa locale tipica è una griglia densa che scorre con il veicolo — `f7-estensione/05-esperto-dominio/CONSEGNA.md` righe 17 e 80 (S7)
Note: —

### williams1978
Tipo: articolo scientifico
Autori: Lance Williams
Titolo: Casting Curved Shadows on Curved Surfaces
Sede e anno: ACM SIGGRAPH Computer Graphics 12(3):270–274, 1978 (SIGGRAPH '78)
Identificativo: DOI 10.1145/965139.807402
Link: https://history.siggraph.org/?p=120268
Verifica: verificata dal curatore il 14-11-2026 [API] e [T]: pagina dell'archivio aperta, titolo e autore presenti
Usata per: la mappa d'ombra della grafica come analogia («il sensore è la lampada») — `f7-estensione/08-creativo/CONSEGNA.md` riga 51
Note: analogia, nessuna cifra.

### guibas1997
Tipo: articolo scientifico
Autori: Leonidas J. Guibas; Jean-Claude Latombe; Steven M. LaValle; David Lin; Rajeev Motwani
Titolo: Visibility-Based Pursuit-Evasion in a Polygonal Environment
Sede e anno: Lecture Notes in Computer Science (Springer), 1997, pp. 17–30 (convegno e volume: non letti); versione estesa su International Journal of Computational Geometry & Applications 9(4–5):471–493, 1999
Identificativo: DOI 10.1007/3-540-63307-3_45 (1997); DOI 10.1142/S0218195999000273 (1999)
Link: https://cw.fel.cvut.cz/b191/_media/courses/b4m36uir/lectures/guibas1997.pdf
Verifica: verificata dal curatore il 14-11-2026 [API] e [T]: PDF aperto, titolo e autori presenti; il passo usato non riletto
Usata per: la regione di «possibile presenza» come nell'inseguimento con visibilità — `f7-estensione/08-creativo/CONSEGNA.md` riga 53
Note: il link è una copia su un sito didattico, non l'editore.

### balch2019
Tipo: articolo scientifico
Autori: Michael S. Balch; Ryan Martin; Scott Ferson
Titolo: Satellite conjunction analysis and the false confidence theorem
Sede e anno: Proceedings of the Royal Society A 475(2227):20180565, 2019
Identificativo: DOI 10.1098/rspa.2018.0565; arXiv:1706.08565
Link: https://arxiv.org/abs/1706.08565
Verifica: verificata dal curatore il 14-11-2026 [API]: «lower quality data paradoxically appear to reduce the risk of collision» presente nel riassunto; «gli ellissoidi d'incertezza ne sono immuni» non ricontrollato
Usata per: la diluizione della probabilità: un dato più rumoroso abbassa la probabilità d'intrusione (conto del ruolo: da 0,75 a 0,45 a 1 s) — `f9-preproposta/06-esperto-dominio/CONSEGNA.md` riga 31 (F4)
Note: congiunzioni fra satelliti: passa il principio, non i numeri.

### marvel2017
Tipo: articolo scientifico
Autori: Jeremy A. Marvel; Rick Norcross
Titolo: Implementing Speed and Separation Monitoring in Collaborative Robot Workcells
Sede e anno: Robotics and Computer-Integrated Manufacturing 44:144–155, 2017
Identificativo: DOI 10.1016/j.rcim.2016.08.001; PMC5117641
Link: https://pmc.ncbi.nlm.nih.gov/articles/PMC5117641
Verifica: verificata dal curatore il 14-11-2026 [API] e [T]: nella pagina PMC «the time for the robot system to respond…», «operator position», 1,6 m/s presenti; la formula per intero non ricontrollata simbolo per simbolo
Usata per: forma lineare della distanza di protezione S = v_H·T_R + v_H·T_S + v_R·T_R + B + C + Z_S + Z_R, con v_H = 1,6 m/s — `f9-preproposta/06-esperto-dominio/CONSEGNA.md` riga 69 (F7); la distanza della ISO/TS 15066 somma percorsi nel caso peggiore e incertezze di posizione — `f7-estensione/05-esperto-dominio/CONSEGNA.md` riga 21 (S9)
Note: è una fonte secondaria sul testo della norma (vedi `iso-ts-15066`); i 2,80 m e 1,68 m sono conti del ruolo.

### machado2009
Tipo: articolo scientifico
Autori: Gustavo M. Machado; Manuel M. Oliveira; Leandro A. F. Fernandes
Titolo: A Physiologically-based Model for Simulation of Color Vision Deficiency
Sede e anno: IEEE Transactions on Visualization and Computer Graphics 15(6):1291–1298, 2009
Identificativo: DOI 10.1109/TVCG.2009.113
Link: https://www.inf.ufrgs.br/~oliveira/pubs_files/CVD_Simulation/CVD_Simulation.html
Verifica: verificata dal curatore il 14-11-2026 [API] e [T]: pagina degli autori aperta; le matrici non ricontrollate valore per valore (il ruolo dice di averle verificate lì)
Usata per: matrici per simulare i difetti della visione dei colori nella prova delle interfacce — `f9-preproposta/09-interfacce/CONSEGNA.md` righe 77 e 80
Note: esistono correzioni pubblicate (TVCG 16(2):352, 2010, DOI 10.1109/TVCG.2010.10): non lette (C9). L'uso in RGB lineare è una scelta del ruolo.

### cao2023
Tipo: articolo scientifico
Autori: Jinkun Cao; Jiangmiao Pang; Xinshuo Weng; Rawal Khirodkar; Kris Kitani
Titolo: Observation-Centric SORT: Rethinking SORT for Robust Multi-Object Tracking
Sede e anno: IEEE/CVF CVPR 2023, pp. 9686–9696
Identificativo: DOI 10.1109/CVPR52729.2023.00934; arXiv:2203.14360
Link: https://arxiv.org/abs/2203.14360
Verifica: verificata dal curatore il 14-11-2026 [API]: dati bibliografici; «700+ FPS on a single CPU» nel riassunto; già verificata dal curatore in f3 (F16); il passo di recupero (OCR) è citato dal ruolo a memoria: non verificato
Usata per: riassociazione «alla OC-SORT» alla ricomparsa; braccio `cor3` (recupero sull'ultima osservazione) — `f9-preproposta/05-tracciamento/CONSEGNA.md` riga 3, `PREVISIONI.md` riga 64; nominata in `prepropostaEsterna.md` riga 91
Note: nel piano immagine; il ruolo la porta sul piano del suolo.

### dossantos2025
Tipo: articolo scientifico
Autori: A. D. P. Dos Santos; M. Loureiro; F. Machado; A. Frizera; F. O. Medola
Titolo: NavWear: design and evaluation of a wearable device for obstacle detection for blind and visually impaired people
Sede e anno: Disability and Rehabilitation: Assistive Technology 20(6):1800–1814, 2025
Identificativo: DOI 10.1080/17483107.2025.2477681; PMID 40100749
Link: https://pubmed.ncbi.nlm.nih.gov/40100749/
Verifica: verificata dal curatore il 14-11-2026 [API PubMed] per i dati bibliografici; contenuto non letto
Usata per: esempio di ausilio indossabile con RGB-D e riscontro aptico, per impostare la valutazione con gli utenti — `bozza_iniziale/Proposta MLE Matrice Bayesiana (1).md` riga 2934
Note: la bozza non ne trae cifre.

### ahn2019
Tipo: articolo scientifico
Autori: Min Sung Ahn; Hosik Chae; Donghun Noh; Hyunwoo Nam; Dennis Hong (nomi per esteso: non verificati; Crossref dà Ahn M, Chae H, Noh D, Nam H, Hong D)
Titolo: Analysis and Noise Modeling of the Intel RealSense D435 for Mobile Robots
Sede e anno: 16th International Conference on Ubiquitous Robots (UR), 2019, pp. 707–711
Identificativo: DOI 10.1109/URAI.2019.8768489
Link: https://ucla.box.com/shared/static/gqxwr2vvqsf22oi9dqtn50hr0xkruzie.pdf
Verifica: verificata dal curatore il 14-11-2026 [API] e [T]: nel PDF σz(z, θ) = 0,001063 + 0,0007278·z + 0,003949·z² + 0,022·z^(3/2)·θ/(π/2 − θ)²; «the left edge of the planar target noticeably worsens»; la soglia dei 60° e 75° non ricontrollata
Usata per: rumore assiale misurato della D435 (σz = 0,0011 + 0,0007·z + 0,0039·z², 1,83 cm a 2 m), ombra sul bordo sinistro, rumore piatto fino a 60° d'incidenza — `f10-dati/02-sensori/MODELLO_SENSORE.md` righe 18 e 90 (S3), `PREVISIONI.md` righe 31 e 35
Note: parete bianca, 0,4–2,1 m: a 3 m è un'estrapolazione (lo dice il ruolo). Copia messa in rete dagli autori; diritti IEEE.

### nguyen2012
Tipo: articolo scientifico
Autori: Chuong V. Nguyen; Shahram Izadi; David Lovell
Titolo: Modeling Kinect Sensor Noise for Improved 3D Reconstruction and Tracking
Sede e anno: Second International Conference on 3D Imaging, Modeling, Processing, Visualization & Transmission (3DIMPVT), 2012, pp. 524–530
Identificativo: DOI 10.1109/3DIMPVT.2012.84
Link: https://doi.org/10.1109/3DIMPVT.2012.84
Verifica: verificata dal curatore il 14-11-2026 [API] solo per esistenza e dati bibliografici; il ruolo la cita a memoria
Usata per: esistono modelli di rumore assiale e laterale per il Kinect, non per lo stereo attivo — `f10-dati/02-sensori/PREVISIONI.md` riga 15 (sensori-P7)
Note: Kinect v1 (luce strutturata).

### zhang2023
Tipo: articolo scientifico
Autori: Xiaoshuai Zhang; Rui Chen; Ang Li; Fanbo Xiang; Yuzhe Qin; Jiayuan Gu; Zhan Ling; Minghua Liu; Peiyu Zeng; Songfang Han; Zhiao Huang; Tongzhou Mu; Jing Xu; Hao Su
Titolo: Close the Optical Sensing Domain Gap by Physics-Grounded Active Stereo Sensor Simulation
Sede e anno: IEEE Transactions on Robotics (dal commento arXiv: «will appear»); volume, pagine, anno di stampa: non letti; arXiv 28-1-2022
Identificativo: arXiv:2201.11924
Link: https://arxiv.org/abs/2201.11924
Verifica: verificata dal curatore il 14-11-2026 [API] per autori, titolo e sede dichiarata
Usata per: SimSense e SAPIEN simulano lo stereo attivo ma chiedono CUDA o una GPU — `f10-dati/02-sensori/MODELLO_SENSORE.md` riga 68
Note: la chiave porta l'anno presunto di stampa; da correggere quando si legge il DOI.

### starr2016
Tipo: altro (tesi di dottorato)
Autori: Joseph Wesley Starr
Titolo: Rangefinding in Fire Smoke Environments
Sede e anno: Virginia Polytechnic Institute and State University, tesi di dottorato in ingegneria meccanica, 7-1-2016
Identificativo: manca (scheda VTechWorks d7fdffcf-494d-40bb-a54a-6315de467ef3)
Link: https://vtechworks.lib.vt.edu/items/d7fdffcf-494d-40bb-a54a-6315de467ef3/full
Verifica: verificata dal curatore il 14-11-2026 [T]: nel riassunto «…the ability of LWIR stereo vision to rangefind in dense smoke when LIDAR and visual stereo vision fail»
Usata per: in fumo denso LiDAR e stereo visibile falliscono, radar e infrarosso termico reggono — `f7-estensione/05-esperto-dominio/CONSEGNA.md` righe 35 e 80 (S11)
Note: fumo d'incendio, non nebbia; nessuna misura sullo stereo attivo a infrarossi (lo dice il ruolo).

### sciencedirect-s0926580524005867
Tipo: articolo scientifico (titolo e autori: mancano)
Autori: manca
Titolo: manca
Sede e anno: rivista con ISSN 0926-5805 (dal codice dell'articolo; a memoria «Automation in Construction»: non verificato), 2024
Identificativo: PII S0926580524005867
Link: https://www.sciencedirect.com/science/article/pii/S0926580524005867
Verifica: non raggiungibile (403 oggi); dal ruolo: vista solo nel riassunto di un motore di ricerca
Usata per: la profondità delle camere RGB-D in polvere è «heavily distorted» — `f7-estensione/05-esperto-dominio/CONSEGNA.md` righe 35 e 80 (S12, marca R)
Note: non citabile finché non si leggono titolo, autori e frase.

---

## B. Norme e documenti regolatori

### eurocontrol-asterix-cat062
Tipo: norma o documento regolatorio
Autori: EUROCONTROL
Titolo: EUROCONTROL Specification for Surveillance Data Exchange — ASTERIX Part 9, Category 062: System Track Data
Sede e anno: EUROCONTROL; edizione 1.18 (quella letta dal ruolo, in copia strutturata non ufficiale); ultima edizione sulla pagina ufficiale: 1.21, 5-6-2025
Identificativo: ASTERIX CAT062
Link: https://www.eurocontrol.int/publication/cat062-eurocontrol-specification-surveillance-data-exchange-asterix-part-9-category-062 (ufficiale); https://zoranbosnjak.github.io/asterix-specs/specs/cat062/cats/cat1.18/definition.html (copia)
Verifica: dato diverso: l'edizione corrente è la 1.21 (5 giugno 2025) [T sulla pagina ufficiale]; nella copia 1.18 ho ritrovato [T] «Age of the last received track update is higher than system dependent threshold (coasting)», il tetto 63,75 s e «Estimated Accuracies»; il PDF ufficiale non l'ha aperto nessuno
Usata per: una traccia estrapolata resta in uscita con l'età (I062/290, passo 0,25 s, tetto 63,75 s), l'accuratezza stimata (I062/500) e il bit di coasting (I062/080 CST) — `f8-continuita/07-ricercatore/FONTI.md` (S16), `CONSEGNA.md` righe 26, 30, 78, 117
Note: correzione C3. Sorveglianza aerea: passa il principio, non le soglie.

### imo-msc192-79
Tipo: norma o documento regolatorio
Autori: International Maritime Organization, Maritime Safety Committee
Titolo: Resolution MSC.192(79) — Adoption of the revised performance standards for radar equipment
Sede e anno: IMO, 2004
Identificativo: MSC.192(79)
Link: https://law.resource.org/pub/us/cfr/ibr/inc/imo/imo.msc.192.2004.pdf
Verifica: verificata dal curatore il 14-11-2026 [T]: nel PDF «Tracked Target Accuracy» e «…last position should be clearly indicated on the display» presenti; i valori della Tabella 3 (11°, 1,0 NM; 3°, 0,3 NM) non ricontrollati: trovati dal ruolo (A-g)
Usata per: accuratezza dichiarata di una traccia al 95 % e avviso di perdita con l'ultima posizione — `f8-continuita/07-ricercatore/FONTI.md` (S17), `CONSEGNA.md` righe 78 e 117
Note: copia su un archivio di terzi, non il sito IMO. Nel PDF il titolo è «ADOPTION OF THE REVISED PERFORMANCE STANDARDS…» [T]; il seguito («for radar equipment») è a memoria.

### eurocontrol-acas-guide
Tipo: norma o documento regolatorio (guida)
Autori: EUROCONTROL
Titolo: ACAS Guide — Airborne Collision Avoidance Systems, versione 5.0
Sede e anno: EUROCONTROL, aprile 2025 (dal frontespizio [T]; il file è nella cartella 2025-09 del sito)
Identificativo: versione 5.0 (dal nome del file)
Link: https://www.eurocontrol.int/sites/default/files/2025-09/eurocontrol-safety-acas-guide-5-0.pdf
Verifica: verificata dal curatore il 14-11-2026 [T]: nel PDF «No manoeuvres are permitted in response to a TA», «pilots shall respond immediately», «does not detect non-transponder equipped aircraft», «does not support operations on the ground», «assumes the worst-case», «14 NM» presenti; numeri di paragrafo e Tabella 16 (20–48 s, 15–35 s, 0,20–1,10 NM, 600–800 ft) non ricontrollati
Usata per: TA e RA sono due atti diversi; ACAS è di bordo e non aeroportuale; scale del TCAS II; il TCAS non usa probabilità — `f9-preproposta/06-esperto-dominio/CONSEGNA.md` righe 23–31 (F3)
Note: frontespizio letto [T]: «ACAS Guide — Airborne Collision Avoidance Systems, April 2025». Aviazione civile: passa il principio, non le soglie.

### colreg-regola7
Tipo: norma o documento regolatorio
Autori: International Maritime Organization
Titolo: Convention on the International Regulations for Preventing Collisions at Sea (COLREG), 1972 — Rule 7, Risk of collision
Sede e anno: IMO, 1972; letta in una riproduzione di terzi
Identificativo: COLREG, regola 7(d)(i)–(ii)
Link: https://ialacolreg.com/en/colreg/rule-7
Verifica: verificata dal curatore il 14-11-2026 [T]: «does not appreciably change» e «even when an appreciable bearing change is evident» presenti nella pagina
Usata per: rilevamento costante come segno di rischio di collisione, e avvertenza che il rischio può esistere anche con rilevamento che cambia a breve distanza — `f9-preproposta/06-esperto-dominio/CONSEGNA.md` riga 33 (F5)
Note: riproduzione non ufficiale del testo.

### faa-aim-2-1-6
Tipo: norma o documento regolatorio
Autori: Federal Aviation Administration
Titolo: Aeronautical Information Manual, capitolo 2, sezione 1, paragrafo 2-1-6 (Runway Status Light System)
Sede e anno: FAA; edizione: non letta; letta in una riproduzione di terzi (faa.gov ha risposto 403 al ruolo)
Identificativo: AIM 2-1-6
Link: https://www.angleofattack.com/aim/chapter-2/2-1-6/
Verifica: verificata dal curatore il 14-11-2026 [T]: «Two aircraft, or a surface vehicle and an aircraft, are required», «this is not clearance», «does not substitute for or convey» presenti nella riproduzione
Usata per: le luci di stato della pista si accendono per traffico osservato e non danno un'autorizzazione — `f9-preproposta/06-esperto-dominio/CONSEGNA.md` riga 37 (F6), `PREVISIONI.md` riga 27
Note: non verificata sul sito FAA; l'edizione dell'AIM riprodotta non è nota.

### faa-ac-150-5220-25
Tipo: norma o documento regolatorio (circolare), letta su una pagina di costruttore
Autori: Federal Aviation Administration (pagina: Accipiter Radar)
Titolo: Advisory Circular 150/5220-25, Airport Avian Radar Systems
Sede e anno: FAA; data: non letta
Identificativo: AC 150/5220-25
Link: https://www.accipiterradar.com/faa-advisory-circular-1505220-25-airport-avian-radar
Verifica: verificata dal curatore il 14-11-2026 [T] solo per la presenza di «avian radar» e del numero della circolare sulla pagina del costruttore; il testo della circolare non l'ha aperto nessuno
Usata per: la FAA parla di «avian radar» a supporto della gestione della fauna, non di avvisi ai piloti — `f9-preproposta/06-esperto-dominio/CONSEGNA.md` riga 23 (F2), `PREVISIONI.md` riga 11
Note: fonte secondaria e di parte (un costruttore).

### faa-ac-150-5220-24
Tipo: norma o documento regolatorio (circolare), letta in un articolo di rivista
Autori: Federal Aviation Administration (articolo: Flight Safety Foundation, AeroSafety World, «Clean Sweep»)
Titolo: Advisory Circular 150/5220-24, sistemi di rilevamento degli oggetti estranei sulle piste (titolo esatto: non letto)
Sede e anno: FAA; data: non letta
Identificativo: AC 150/5220-24
Link: https://flightsafety.org/asw-article/clean-sweep/
Verifica: verificata dal curatore il 14-11-2026 [T]: nell'articolo compaiono «150/5220-24», una sfera, un cilindro, «1.7 in» e «4.3»; le misure esatte del cilindro (3 × 3,8 cm) non ricontrollate
Usata per: oggetti estranei di riferimento sulle piste (sfera di 4,3 cm, cilindro di 3 × 3,8 cm), sotto i 7 cm di quota minima del nucleo — `f7-estensione/05-esperto-dominio/CONSEGNA.md` righe 37 e 80 (S13)
Note: fonte secondaria; la circolare non è stata aperta.

### faa-ordine-7110-65
Tipo: norma o documento regolatorio
Autori: Federal Aviation Administration
Titolo: Order JO 7110.65, Air Traffic Control
Sede e anno: FAA; edizione: manca
Identificativo: JO 7110.65
Link: manca (faa.gov ha risposto 403 al ruolo)
Verifica: non verificata (né dal ruolo né da me)
Usata per: regole sulle tracce in coasting nei sistemi del controllo del traffico — `f8-continuita/07-ricercatore/FONTI.md` (§4), `CONSEGNA.md` righe 18 e 129
Note: nessuna affermazione ne dipende; la «guida amatoriale ai simboli ERAM» citata accanto non è una fonte primaria e non ha una voce.

### iso-ts-15066
Tipo: norma o documento regolatorio
Autori: International Organization for Standardization
Titolo: ISO/TS 15066 — Robots and robotic devices — Collaborative robots; ISO 10218-2:2025 (in cui, secondo il ruolo, è confluita)
Sede e anno: ISO; ISO/TS 15066: 2016 (a memoria, non verificato); ISO 10218-2: 2025
Identificativo: ISO/TS 15066; ISO 10218-2:2025
Link: manca (testi a pagamento)
Verifica: non raggiungibile (iso.org ha risposto 403 oggi); dal ruolo: vista solo nel riassunto di un motore di ricerca, contenuto letto tramite `marvel2017`
Usata per: sorveglianza di velocità e separazione come concetto consolidato per aree condivise; «confluita in ISO 10218-2:2025» — `f9-preproposta/06-esperto-dominio/CONSEGNA.md` righe 69 e 87, `PREVISIONI.md` riga 12; `f7-estensione/05-esperto-dominio/PREVISIONI.md` riga 15 e `CONSEGNA.md` riga 21
Note: la confluenza nella 10218-2:2025 non è verificata su una fonte primaria.

### iso-13855
Tipo: norma o documento regolatorio
Autori: International Organization for Standardization
Titolo: ISO 13855 — Safety of machinery — Positioning of safeguards with respect to the approach of the human body (titolo a memoria: non verificato)
Sede e anno: ISO; edizione 2024 secondo il ruolo
Identificativo: ISO 13855:2024
Link: manca (testo a pagamento)
Verifica: vista solo nel riassunto di un motore di ricerca (dal ruolo); non cercata da me
Usata per: v_H = 1,6 m/s; C = 0,85 m e il termine d'incertezza — `f9-preproposta/06-esperto-dominio/CONSEGNA.md` righe 69 e 87
Note: 1,6 m/s è confermato in `marvel2017` [T]; C = 0,85 m resta non verificato, e con esso i 2,80 m e 1,68 m calcolati dal ruolo.

### iso-9241-303
Tipo: norma o documento regolatorio
Autori: International Organization for Standardization
Titolo: ISO 9241-303 — Ergonomics of human-system interaction — Requirements for electronic visual displays (titolo a memoria: non verificato)
Sede e anno: ISO; edizione: manca
Identificativo: ISO 9241-303
Link: manca (a pagamento)
Verifica: non verificata (il ruolo dichiara «a pagamento, non aperta»)
Usata per: altezza dei caratteri di 16–22 minuti d'arco — `f9-preproposta/09-interfacce/CONSEGNA.md` riga 77
Note: la cifra è a memoria del ruolo.

### iec-60601-1-8
Tipo: norma o documento regolatorio
Autori: International Electrotechnical Commission
Titolo: IEC 60601-1-8 — allarmi nei dispositivi elettromedicali; sottoclausola 6.3.3.1, caratteristiche dei segnali d'allarme acustici, codifica della priorità
Sede e anno: IEC; edizione: non letta (la copia è del 2008)
Identificativo: IEC 60601-1-8, 6.3.3.1 a)
Link: https://standards.har-el.com/Projects/181701/60601-1-8/html/A2SubCl-6-3-3-1-a-priority-encoded.htm
Verifica: verificata dal curatore il 14-11-2026 [T] solo per la presenza della sottoclausola 6.3.3.1 «priority encoded» sulla pagina; è una copia non ufficiale di un documento di lavoro
Usata per: precedente per codificare la priorità nel suono (regola 7 della specifica delle interfacce) — `f9-preproposta/09-interfacce/CONSEGNA.md` riga 80
Note: non è il testo della norma in vigore.

### w3c-wcag22-uso-del-colore
Tipo: norma o documento regolatorio (documento esplicativo)
Autori: W3C, Web Accessibility Initiative
Titolo: Understanding Success Criterion 1.4.1: Use of Color (WCAG 2.2)
Sede e anno: W3C; data della pagina: non letta
Identificativo: WCAG 2.2, criterio 1.4.1
Link: https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html
Verifica: verificata dal curatore il 14-11-2026 [T]: «not used as the only visual means» presente
Usata per: il colore non deve essere l'unico mezzo per distinguere gli stati — `f9-preproposta/09-interfacce/CONSEGNA.md` riga 80
Note: scritta per il web; qui usata per analogia.

### w3c-wcag22-contrasto-non-testuale
Tipo: norma o documento regolatorio (documento esplicativo)
Autori: W3C, Web Accessibility Initiative
Titolo: Understanding Success Criterion 1.4.11: Non-text Contrast (WCAG 2.2)
Sede e anno: W3C; data della pagina: non letta
Identificativo: WCAG 2.2, criterio 1.4.11
Link: https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html
Verifica: verificata dal curatore il 14-11-2026 [T]: rapporto «3:1» presente
Usata per: contrasto minimo 3:1 per gli elementi grafici — `f9-preproposta/09-interfacce/CONSEGNA.md` riga 80
Note: come sopra.

### codice-strada-reg-art162
Tipo: norma o documento regolatorio
Autori: Repubblica Italiana
Titolo: Regolamento di esecuzione e di attuazione del Codice della strada (D.P.R. 495/1992: numero a memoria, non verificato), articolo 162
Sede e anno: letto su un sito di divulgazione giuridica
Identificativo: art. 162 del regolamento
Link: https://leggeinchiaro.it/articolo-162-regolamento-codice-strada/
Verifica: aperta dal ruolo che la cita; dal curatore solo [200] e presenza di «162» nella pagina; il contenuto usato non ricontrollato
Usata per: precedente per i segnali — `f9-preproposta/09-interfacce/CONSEGNA.md` riga 80
Note: sito non ufficiale; preferire Normattiva.

### rtca-do-365
Tipo: norma o documento regolatorio
Autori: RTCA
Titolo: DO-365 — norme minime per i sistemi «detect and avoid» (titolo esatto: manca)
Sede e anno: RTCA; edizione: manca
Identificativo: DO-365
Link: manca
Verifica: vista solo nel riassunto di un motore di ricerca (dal ruolo); sulla pagina di `nasa-wellclear` la sigla non compare [T]
Usata per: tempi degli avvisi per i velivoli senza equipaggio — `f9-preproposta/06-esperto-dominio/CONSEGNA.md` riga 87
Note: nessuna cifra citata.

### noaa-nhc-cono
Tipo: norma o documento regolatorio (definizione ufficiale di un prodotto)
Autori: NOAA, National Hurricane Center
Titolo: Definition of the NHC Track Forecast Cone
Sede e anno: NHC; pagina con i raggi del 2026
Identificativo: manca
Link: https://www.nhc.noaa.gov/aboutcone.shtml
Verifica: verificata dal curatore il 14-11-2026 [T]: «…the area swept out by a set of circles… two-thirds of historical official forecast errors over a 5-year sample fall within the circle» presente
Usata per: il cono come area spazzata da cerchi tarati sui due terzi degli errori storici — `f8-continuita/09-creativo/CONSEGNA.md` riga 84
Note: il «cerchio di massimo allontanamento» e la verifica a posteriori dei meteorologi restano non verificati (lo dice il ruolo).

### chs-carta1-abbreviazioni
Tipo: norma o documento regolatorio (simboli cartografici)
Autori: Canadian Hydrographic Service
Titolo: Chart 1 — Symbols, Abbreviations and Terms; sezione W, abbreviazioni
Sede e anno: Governo del Canada; edizione: non letta
Identificativo: manca
Link: https://cartes-charts.gc.ca/publications/chart1-carte1/sections/w-abbrs/abbrev-eng.html
Verifica: verificata dal curatore il 14-11-2026 [T]: «Position approximate» e «Position doubtful» presenti
Usata per: le carte nautiche marcano ciò che è approssimato o dubbio (PA, PD), come modello per la legenda — `f7-estensione/08-creativo/CONSEGNA.md` riga 68
Note: analogia.

### skybrary-acas-ra-ta
Tipo: altro (enciclopedia di settore)
Autori: SKYbrary (EUROCONTROL e altri)
Titolo: ACAS Resolution and Traffic Advisories (dal percorso del link)
Sede e anno: manca
Identificativo: manca
Link: https://skybrary.aero/articles/acas-resolution-and-traffic-advisories
Verifica: non raggiungibile (la pagina risponde con un controllo JavaScript; anche il ruolo dichiara «pagina non aperta»)
Usata per: in ACAS l'avviso di risoluzione raccomanda una manovra all'equipaggio — `f9-preproposta/12-avversario/CONSEGNA.md` riga 48; `f9-preproposta/06-esperto-dominio/CONSEGNA.md` riga 87 e `PREVISIONI.md` riga 11
Note: la stessa affermazione è sostenuta da `eurocontrol-acas-guide` [T]: citare quella.

---

## C. Schede tecniche e documenti di costruttore

### st-vl53l7cx
Tipo: scheda tecnica
Autori: STMicroelectronics
Titolo: VL53L7CX — Time-of-Flight 8x8 multizone ranging sensor with 90° FoV (titolo a memoria: non verificato alla lettera)
Sede e anno: STMicroelectronics, DS13865 Rev 6
Identificativo: DS13865 Rev 6
Link: https://www.pololu.com/file/0J1992/vl53l7cx.pdf
Verifica: verificata dal curatore il 14-11-2026 [T]: PDF aperto, «DS13865 Rev 6», 940 (nm), «crosstalk», AVDD presenti; tabelle 17–18 non ricontrollate cifra per cifra; già verificata dal curatore in f3 (punto 1 di `f3/fonti/FONTI_VERIFICATE.md`)
Usata per: emissione a 940 nm; portata in 8×8 su grigio 17 % a 5 klx 0,35 m tipici (0,25 m minimi, tab. 18); nessun ingresso di trigger (B1 è AVDD); «crosstalk» è il riflesso del vetro di copertura; interfaccia I2C a 0x52 — `f9-preproposta/07-lidar/CONSEGNA.md` ([1]); `f10-dati/04-embedded/PREVISIONI.md` (E10); `f10-dati/02-sensori/MODELLO_SENSORE.md` (S7); `f10-dati/03-infrastruttura/PREVISIONI.md` (infra-P4), `AMBIENTE.md` riga 78; `f9-preproposta/01-architetto/CONSEGNA.md` riga 14
Note: copia di un rivenditore, non st.com; forse non è l'ultima revisione (lo dice il ruolo). Le estrapolazioni sul nero al 5 % (0,38 m, 0,30 m) sono conti del ruolo.

### st-vl53l8cx
Tipo: scheda tecnica
Autori: STMicroelectronics
Titolo: VL53L8CX — sensore a tempo di volo multizona (titolo esatto: non letto)
Sede e anno: STMicroelectronics, DS14161 Rev 7
Identificativo: DS14161 Rev 7
Link: https://www.pololu.com/file/0J2029/vl53l8cx.pdf
Verifica: verificata dal curatore il 14-11-2026 [T]: PDF aperto, «DS14161 Rev 7», 940, SYNC presenti; portate non ricontrollate; già verificata dal curatore in f3 (punto 2)
Usata per: 940 nm; campo 45°; a 5 klx in 8×8 1,55 m (bianco), in 4×4 grigio 17 % 1,65 m tipici; piedino SYNC; alimentazione del nucleo a 1,8 V — `f9-preproposta/07-lidar/CONSEGNA.md` ([2]); `f10-dati/04-embedded/PREVISIONI.md` (E10); `f10-dati/02-sensori/MODELLO_SENSORE.md` (S9)
Note: copia di un rivenditore.

### st-um3038
Tipo: scheda tecnica (manuale d'uso)
Autori: STMicroelectronics
Titolo: UM3038 — A guide to using the VL53L7CX Time-of-Flight multizone ranging sensor with 90° FoV
Sede e anno: STMicroelectronics, UM3038 Rev 2
Identificativo: UM3038 Rev 2
Link: https://www.pololu.com/file/0J1993/um3038-a-guide-to-using-the-vl53l7cx-timeofflight-multizone-ranging-sensor-with-90-fov-stmicroelectronics.pdf
Verifica: verificata dal curatore il 14-11-2026 [T]: stato 10 = «Range valid, but no target detected at previous range»; «status 5 is considered as 100 % valid. A status of 6 or 9 … confidence value of 50 %. All other statuses are below 50 %»; `set_i2c_address` e LPn presenti
Usata per: il primo campione dopo «nessun bersaglio» ha stato 10, fiducia sotto il 50 % (§5.5); procedura per cambiare l'indirizzo I2C con LPn (§2.3) — `f9-preproposta/07-lidar/CONSEGNA.md` ([3]); `f10-dati/02-sensori/MODELLO_SENSORE.md` (S8), `PREVISIONI.md` riga 14
Note: numeri di paragrafo non ricontrollati.

### realsense-d400-scheda
Tipo: scheda tecnica
Autori: RealSense (già Intel RealSense)
Titolo: RealSense D400 Series Product Family Datasheet
Sede e anno: revisione di marzo 2026 (in `f10-dati/02-sensori/PREVISIONI.md`: «rev. 023»)
Identificativo: manca (numero del documento non letto)
Link: https://www.realsenseai.com/wp-content/uploads/2026/03/RealSense-D400-Series-Datasheet-Mar-2026.pdf
Verifica: verificata dal curatore il 14-11-2026 [T]: PDF aperto (5,4 MB); 850 (nm), 360 (mW), «All pass», «Filter Type» presenti; base stereo e RMS non ricontrollati
Usata per: proiettore 850 ± 10 nm, 360 mW massimi, campo 90° × 63°; imager senza filtro («Filter Type: None», «Depth Filter: All pass») — `f9-preproposta/07-lidar/CONSEGNA.md` ([4]); base 50 mm (D430) e 95 mm (D450), RMS ≤ 2 % entro 2 m (D43x) ed entro 4 m (D455) — `f10-dati/02-sensori/PREVISIONI.md` righe 9 e 24, `MODELLO_SENSORE.md` (S1)
Note: che «rev. 023» e «Mar 2026» siano lo stesso documento non è verificato.

### orbbec-gemini-330-scheda
Tipo: scheda tecnica
Autori: Orbbec
Titolo: Gemini 330 series Datasheet
Sede e anno: Orbbec, V1.6
Identificativo: V1.6
Link: https://download.kamami.pl/p1203693-Gemini-330-series-Datasheet-V1.6.pdf
Verifica: verificata dal curatore il 14-11-2026 [T]: PDF aperto; «V1.6», 850, «All-Pass» presenti
Usata per: Gemini 335: 850 ± 6 nm, imager «All-Pass»; filtri di post-elaborazione attivi come impostazione predefinita (tab. 4-13-1) — `f9-preproposta/07-lidar/CONSEGNA.md` ([5]); `f10-dati/02-sensori/PREVISIONI.md` riga 33, `MODELLO_SENSORE.md` (S6)
Note: copia di un rivenditore.

### realsense-bkm-taratura
Tipo: scheda tecnica (documento del costruttore)
Autori: Intel RealSense (ora RealSense)
Titolo: BKMs for Tuning Intel RealSense D4xx Cameras (titolo dal nome del file)
Sede e anno: 2019 (dal percorso); revisione: non letta
Identificativo: manca
Link: https://realsenseai.com/wp-content/uploads/2019/11/BKMs_Tuning_RealSense_D4xx_Cam.pdf
Verifica: verificata dal curatore il 14-11-2026 [T]: «a well-calibrated camera should produce a Subpixel RMS error of less than 0.1», «subpixel=0.08», «By default we do not do any post-processing of the depth» presenti
Usata per: errore di disparità s < 0,1 px (0,08 per la curva della D435), da cui σz = z²·s/(fx·B); nessun filtro predefinito nell'SDK — `f10-dati/02-sensori/MODELLO_SENSORE.md` righe 18 e 90 (S2), `PREVISIONI.md` riga 33
Note: —

### realsense-taratura-web
Tipo: pagina di costruttore o comunicato
Autori: RealSense
Titolo: Tuning depth cameras for best performance
Sede e anno: documentazione in rete; data: non letta
Identificativo: manca
Link: https://dev.realsenseai.com/docs/tuning-depth-cameras-for-best-performance
Verifica: verificata dal curatore il 14-11-2026 [T]: «Hallucinations», «much worse than no depth» e «High Accuracy» presenti (il ruolo l'aveva solo in riassunto, [r])
Usata per: «false depth, aka. Hallucinations, are much worse than no depth»; preset «High Accuracy» — `f9-preproposta/07-lidar/CONSEGNA.md` critica 6 ([10])
Note: non dice che cosa succede sul tessuto nero: resta non verificato.

### st-community-interferenza
Tipo: pagina di costruttore o comunicato (forum del costruttore)
Autori: STMicroelectronics Community (risposte di dipendenti ST, secondo il ruolo)
Titolo: «Will multiple ToF sensors (VL53L series)… in close…»; «VL53L5CX mutual influence of multiple sensors»
Sede e anno: forum ST; date: non lette
Identificativo: m-p/61090; td-p/197217
Link: https://community.st.com/t5/imaging-sensors/will-multiple-tof-sensors-vl53l-series-specifically-in-close/m-p/61090 ; https://community.st.com/t5/imaging-sensors/vl53l5cx-mutual-influence-of-multiple-sensors/td-p/197217
Verifica: aperta dal ruolo che la cita (solo riassunto, [r]); dal curatore [T] parziale: nella prima «ambient light» c'è, nella seconda la parola «ambient» non compare nel testo scaricato (la discussione può essere caricata da script)
Usata per: ogni sensore vede gli altri «as ambient light»; il disturbo compare come bersaglio in più con stato non valido — `f9-preproposta/07-lidar/CONSEGNA.md` critica 3 ([7])
Note: un forum non è una scheda: va confermato con la prova T3 sull'hardware.

### st-community-940nm
Tipo: pagina di costruttore o comunicato (forum del costruttore)
Autori: STMicroelectronics Community
Titolo: VL53L5CX emitter 940nm light
Sede e anno: forum ST; data: non letta
Identificativo: discussione 11515
Link: https://community.st.com/imaging-sensors-49/vl53l5cx-emitter-940nm-light-11515
Verifica: verificata dal curatore il 14-11-2026 [T]: «940 +/- 10nm is what we are shooting for» e «filter is not absolute» presenti (il ruolo l'aveva solo in riassunto, [r])
Usata per: banda del filtro a 940 nm non dichiarata nella scheda — `f9-preproposta/07-lidar/CONSEGNA.md` critica 1 ([8])
Note: riguarda il VL53L5CX; l'estensione a L7CX e L8CX è un'ipotesi. Che chi scrive sia un dipendente ST non l'ho verificato.

### st-community-trigger
Tipo: pagina di costruttore o comunicato (forum del costruttore)
Autori: STMicroelectronics Community
Titolo: External trigger
Sede e anno: forum ST; data: non letta
Identificativo: discussione 155090
Link: https://community.st.com/imaging-sensors-49/external-trigger-155090
Verifica: verificata dal curatore il 14-11-2026 [T] solo per la presenza di «SYNC», «autonomous» e «trigger» nella pagina; l'affermazione «solo in modo autonomo» non riletta nel contesto
Usata per: il VL53L8CX ha il piedino SYNC, solo in modo autonomo — `f9-preproposta/07-lidar/CONSEGNA.md` critica 2 ([9])
Note: da provare sull'hardware.

### espressif-vl53l7cx-libreria
Tipo: documentazione di software (libreria di terzi)
Autori: grrtzm (registro dei componenti Espressif)
Titolo: v53l7cx-library, versione 1.0.6, esempio `example_02_get_set_params`
Sede e anno: components.espressif.com; data: non letta
Identificativo: versione 1.0.6
Link: https://components.espressif.com/components/grrtzm/v53l7cx-library/versions/1.0.6/examples/example_02_get_set_params
Verifica: verificata dal curatore il 14-11-2026 [T] solo per la presenza di «B1» e «sync» nella pagina
Usata per: una libreria di terzi elenca una funzione di sincronia su «B1», che la scheda Rev 6 non ha — `f9-preproposta/07-lidar/CONSEGNA.md` §6 ([11])
Note: contraddice la scheda: il ruolo la tiene «non verificato», giustamente.

### stm32duino-vl53l7cx
Tipo: deposito di codice
Autori: stm32duino
Titolo: VL53L7CX (libreria Arduino) e VL53L8CX
Sede e anno: GitHub; il ruolo cita il driver 1.2.3
Identificativo: manca (commit non annotato)
Link: https://github.com/stm32duino/VL53L7CX ; https://github.com/stm32duino/VL53L8CX
Verifica: aperta dal ruolo che la cita ([g]); dal curatore solo [200]
Usata per: nessuna funzione di trigger nel driver 1.2.3; firmware da caricare di 86 016 byte per sensore a ogni avvio; SYNC sull'L8CX — `f9-preproposta/07-lidar/CONSEGNA.md` critica 2 e §5 ([6])
Note: versione e licenza non ricontrollate.

### hilink-ld2410
Tipo: scheda tecnica (manuale del protocollo)
Autori: Hi-Link
Titolo: HLK-LD2410 Serial Communication Protocol, v1.02
Sede e anno: Hi-Link; copia su un sito di terzi
Identificativo: v1.02
Link: https://www.sudo.is/docs/esphome/components/ld2410/HLK-LD2410_Serial_Communication_Protocol_v1.02.pdf
Verifica: aperta dal ruolo che la cita ([g], `pdftotext`); dal curatore solo [200]
Usata per: 256 000 baud predefiniti; nessun angolo in uscita; porte di distanza da 0,75 m — `f10-dati/04-embedded/PREVISIONI.md` (E9), `INVENTARIO_E_DECISIONE.md` riga 75 ([17])
Note: copia non ufficiale.

### hilink-ld2450
Tipo: scheda tecnica
Autori: Hi-Link
Titolo: HLK-LD2450, manuale v1.00
Sede e anno: Hi-Link; copia di un rivenditore
Identificativo: v1.00
Link: https://www.elemon.com.ar/images/productos/hojas-de-datos/radar-modulos/hlk-ld2450.pdf
Verifica: aperta dal ruolo che la cita ([g]); dal curatore solo [200]
Usata per: fino a tre bersagli con x, y in mm e velocità, ±60° in azimut, 6 m — `f10-dati/04-embedded/PREVISIONI.md` (E9), `INVENTARIO_E_DECISIONE.md` riga 75 ([18])
Note: copia non ufficiale.

### ldrobot-ld19
Tipo: scheda tecnica
Autori: LDROBOT
Titolo: LD19, scheda V2.5
Sede e anno: copia di un rivenditore (Botland)
Identificativo: V2.5
Link: https://botland.com.pl/img/art/inne/21991_Karta%20katalogowa.pdf
Verifica: aperta dal ruolo che la cita; dal curatore solo [200]
Usata per: accuratezza ±45 mm (media di 100 misure), scarto tipo 10 mm; nessuna portata sul nero — `f10-dati/02-sensori/PREVISIONI.md` riga 32, `MODELLO_SENSORE.md` (S11)
Note: copia non ufficiale.

### slamtec-rplidar-c1
Tipo: pagina di costruttore o comunicato
Autori: Slamtec
Titolo: RPLIDAR C1, specifiche
Sede e anno: pagina del costruttore; data: non letta
Identificativo: manca
Link: https://www.slamtec.com/en/C1/Spec
Verifica: aperta dal ruolo che la cita; dal curatore solo [200]
Usata per: accuratezza ±30 mm — `f10-dati/02-sensori/PREVISIONI.md` riga 32, `MODELLO_SENSORE.md` (S10); SDK: `INVENTARIO_E_DECISIONE.md` ([15], https://github.com/Slamtec/rplidar_sdk, [200])
Note: —

### dxomark-rapporto-camera3d
Tipo: altro (rapporto di prova campione)
Autori: DXOMARK
Titolo: rapporto campione su una camera 3D stereo (titolo esatto: non letto)
Sede e anno: 2025 (dal percorso)
Identificativo: manca
Link: https://corp.dxomark.com/wp-content/uploads/2025/02/DXOMARK_Report_Sample_3Dcamera_stereos.pdf
Verifica: aperta dal ruolo che la cita; dal curatore solo [200]
Usata per: fonte S12 del modello del sensore (uso preciso non riletto) — `f10-dati/02-sensori/MODELLO_SENSORE.md` riga 90
Note: porta la dicitura «Confidential» pur essendo sul sito pubblico (annotazione del ruolo): solo consultazione.

### navtech-witness-coasting
Tipo: documentazione di software (prodotto di un costruttore)
Autori: Navtech Radar
Titolo: documentazione del tracciatore «Witness», pagina «Coasting Tracks»
Sede e anno: wiki del costruttore; data: non letta
Identificativo: pagina 255164634
Link: https://navtechradar.atlassian.net/wiki/spaces/TUN/pages/255164634
Verifica: verificata dal curatore il 14-11-2026 [T] solo per la presenza di «Coasting» (10 volte) nella pagina; i parametri non ricontrollati
Usata per: il coasting riporta posizioni previste finché il radar rivede il bersaglio, con età minima e massima e numero di previsioni consecutive, poi la traccia è cancellata — `f8-continuita/07-ricercatore/FONTI.md` (S18)
Note: prassi di un prodotto, non una norma.

### detect-merlin-abar
Tipo: pagina di costruttore o comunicato (presentazione a un convegno)
Autori: J. Lewis (dal nome del file; DeTect, secondo il ruolo)
Titolo: manca (presentazione TS5-P19)
Sede e anno: birdstrike.org; caricata nel 2024; convegno: non letto
Identificativo: TS5-P19
Link: https://birdstrike.org/wp-content/uploads/2024/04/TS5-P19-J.Lewis_.pdf
Verifica: verificata dal curatore il 14-11-2026 [T]: «Aircraft-Birdstrike Avoidance Radar», «Green = LOW» e «location, size, mass» presenti
Usata per: «ABAR» è la sigla di un prodotto di un solo costruttore, che dà un rischio per zona in tre colori calcolato da posizione, dimensione, massa e numero — `f9-preproposta/06-esperto-dominio/CONSEGNA.md` riga 23 (F1); `f9-preproposta/12-avversario/CONSEGNA.md` riga 48 (lì «non verificato»)
Note: materiale del costruttore. Che ABAR sia la sigla di «un solo» costruttore è un'assenza su un campione.

### therobotreport-veo
Tipo: pagina di costruttore o comunicato (articolo di rivista, autrice del costruttore)
Autori: manca (autrice di Veo Robotics, secondo il ruolo)
Titolo: dal percorso: «Advanced vision: the future of robot safety in manufacturing»
Sede e anno: The Robot Report; data: non letta
Identificativo: manca
Link: https://www.therobotreport.com/advanced-vision-future-robot-safety-manufacturing/
Verifica: verificata dal curatore il 14-11-2026 [T]: «something can be seen behind it» e «treated as occupied» presenti
Usata per: un sistema 3D di sorveglianza di velocità e separazione classifica i volumi in vuoto, occupato o sconosciuto, e ciò che nessun sensore vede è trattato come occupato — `f7-estensione/05-esperto-dominio/CONSEGNA.md` righe 21 e 80 (S8)
Note: fonte di parte.

### sick-sensori-3d
Tipo: pagina di costruttore o comunicato
Autori: SICK
Titolo: pagina di categoria (g568562)
Sede e anno: sito del costruttore
Identificativo: manca
Link: https://www.sick.com/in/en/c/g568562
Verifica: vista solo nel riassunto di un motore di ricerca (dal ruolo); dal curatore: la pagina risponde ma il contenuto è caricato da script (3,7 kB): non letta
Usata per: i sensori 3D certificati lavorano a campi di protezione — `f7-estensione/05-esperto-dominio/CONSEGNA.md` righe 21 e 80 (S10, marca R)
Note: non verificata.

### iata-enhanced-gse-2022
Tipo: pagina di costruttore o comunicato (comunicato di un'associazione)
Autori: IATA
Titolo: comunicato del 6 dicembre 2022 sui mezzi di rampa evoluti (titolo esatto: non letto)
Sede e anno: IATA, 6-12-2022 (dal percorso)
Identificativo: 2022-12-06-04
Link: https://www.iata.org/en/pressroom/2022-releases/2022-12-06-04/
Verifica: verificata dal curatore il 14-11-2026 [T]: «could double to nearly $10 billion by 2035», «cause 40% of total incidents», «by 42% (IATA estimate)», «anti-collision and inching technology» presenti
Usata per: danno a terra fino a quasi 10 miliardi di dollari l'anno entro il 2035; nastri, caricatori, scale e pontili causano il 40 % degli incidenti; riduzione del 42 % — `f7-estensione/05-esperto-dominio/CONSEGNA.md` righe 54 e 80 (S14)
Note: correzione C10. Stima dell'associazione.

### journal-aviation-donecle
Tipo: pagina di costruttore o comunicato (notizia)
Autori: manca
Titolo: dal percorso: «Donecle sets its drone to work for maintenance with AFI KLM E&M»
Sede e anno: Le Journal de l'Aviation; data: manca
Identificativo: 37578
Link: https://www.journal-aviation.com/en/news/37578-donecle-sets-its-drone-to-work-for-maintenance-with-afi-klm-e-m
Verifica: non raggiungibile (404 oggi); dal ruolo: vista solo nel riassunto di un motore di ricerca
Usata per: in hangar i droni da ispezione si guidano con il LiDAR — `f7-estensione/05-esperto-dominio/CONSEGNA.md` righe 41 e 80 (S15, marca R)
Note: non citabile.

### aviationweek-ispezioni-droni
Tipo: pagina di costruttore o comunicato (articolo di rivista)
Autori: manca
Titolo: dal percorso: «Aircraft inspections: drones accelerate toward next evolution»
Sede e anno: Aviation Week; data: non letta
Identificativo: manca
Link: https://aviationweek.com/mro/emerging-technologies/aircraft-inspections-drones-accelerate-toward-next-evolution
Verifica: aperta dal ruolo che la cita; dal curatore [T] parziale: nella pagina compaiono FAA, Boeing, Airbus e Delta; la frase sull'accettazione non riletta (l'articolo può essere tagliato per i non abbonati)
Usata per: ispezione visiva con drone in hangar accettata dall'autorità statunitense per un vettore e approvata dai due maggiori costruttori — `f7-estensione/05-esperto-dominio/CONSEGNA.md` righe 56 e 80 (S16)
Note: —

### sofema-attrezzi-fod
Tipo: altro (blog di un ente di formazione)
Autori: Sofema Online
Titolo: dal percorso: «EASA Part 145 tooling store management and control procedures considering the problem of foreign object debris (FOD)»
Sede e anno: data: non letta
Identificativo: manca
Link: https://sofemaonline.com/about/blog/entry/easa-part-145-tooling-store-management-and-control-procedures-considering-the-problem-of-foreign-object-debris-fod-1
Verifica: aperta dal ruolo che la cita; dal curatore: la pagina risponde, ma nel testo scaricato non ho trovato «FOD» né «tool control» (contenuto forse caricato da script): non verificata
Usata per: in hangar un attrezzo non ritrovato resta in conto — `f7-estensione/08-creativo/CONSEGNA.md` riga 67
Note: il ruolo stesso la chiama «fonte debole» e dichiara la procedura non verificata. Un blog non conta come fonte primaria.

### microsoft-azure-kinect-specifiche
Tipo: pagina di costruttore o comunicato
Autori: Microsoft
Titolo: Azure Kinect DK hardware specifications
Sede e anno: learn.microsoft.com, sezione delle versioni precedenti
Identificativo: manca
Link: https://learn.microsoft.com/en-us/previous-versions/azure/kinect-dk/hardware-specification
Verifica: aperta dal ruolo che la cita; dal curatore solo [200]
Usata per: caratteristiche dell'Azure Kinect nell'inventario — `f10-dati/04-embedded/INVENTARIO_E_DECISIONE.md` riga 75 ([8])
Note: la fine della produzione (annuncio del 17 agosto 2023) è marcata [r] dal ruolo: non verificata.

### orbbec-astra-pagina
Tipo: pagina di costruttore o comunicato
Autori: Orbbec
Titolo: Astra Series
Sede e anno: sito del costruttore
Identificativo: manca
Link: https://www.orbbec.com/products/structured-light-camera/astra-series/
Verifica: aperta dal ruolo che la cita; dal curatore solo [200]
Usata per: campo 58,4° × 45,5°, 0,6–8 m, USB 2.0 — `f10-dati/04-embedded/PREVISIONI.md` (note in fondo), `INVENTARIO_E_DECISIONE.md` ([11])
Note: —

### wikipedia-kinect
Tipo: altro (enciclopedia)
Autori: Wikipedia
Titolo: Kinect
Sede e anno: versione del 14-11-2026 non annotata
Identificativo: manca
Link: https://en.wikipedia.org/wiki/Kinect
Verifica: aperta dal ruolo che la cita ([g], testo grezzo); dal curatore solo [200]
Usata per: campo e distanza minima del Kinect v1 (57° × 43°, circa 0,8 m) — `f10-dati/04-embedded/PREVISIONI.md` (note in fondo), `INVENTARIO_E_DECISIONE.md` ([6])
Note: fonte secondaria (lo dice il ruolo).

### wikipedia-tcas
Tipo: altro (enciclopedia)
Autori: Wikipedia
Titolo: Traffic collision avoidance system
Sede e anno: versione non annotata
Identificativo: manca
Link: https://en.wikipedia.org/wiki/Traffic_collision_avoidance_system
Verifica: aperta dal ruolo che la cita; dal curatore solo [200]
Usata per: a un TA non si manovra, a un RA si risponde subito — `f9-preproposta/09-interfacce/CONSEGNA.md` righe 31 e 80; `f9-preproposta/06-esperto-dominio/PREVISIONI.md` riga 27
Note: fonte secondaria; la primaria è `eurocontrol-acas-guide`.

### nasa-wellclear
Tipo: documentazione di software
Autori: NASA
Titolo: DAIDALUS / Well-Clear (pagina del progetto)
Sede e anno: nasa.github.io; data: non letta
Identificativo: manca
Link: https://nasa.github.io/WellClear
Verifica: verificata dal curatore il 14-11-2026 [T]: «preventive», «corrective» e «warning» presenti; «DO-365» non compare
Usata per: i velivoli senza equipaggio hanno una scala propria di avvisi (preventivo, correttivo, d'allarme) — `f9-preproposta/06-esperto-dominio/CONSEGNA.md` riga 73 (F8)
Note: —

### record3d-funzioni
Tipo: pagina di costruttore o comunicato
Autori: Record3D
Titolo: Features
Sede e anno: sito dell'applicazione
Identificativo: manca
Link: https://record3d.app/features
Verifica: vista solo nel riassunto di un motore di ricerca (marca [r] del ruolo); dal curatore [T] parziale: «USB», «Wi-Fi» e «purchase» compaiono nella pagina, le condizioni precise non rilette
Usata per: flusso via USB solo dopo l'acquisto; flusso Wi-Fi a pagamento, in rete locale, con compressione con perdita — `f10-dati/04-embedded/PREVISIONI.md` (E8), `INVENTARIO_E_DECISIONE.md` ([12])
Note: la risoluzione non è stata trovata (lo dice il ruolo).

---

## D. Documentazione di software e depositi di codice

### octomap
Tipo: documentazione di software
Autori: Kai M. Wurm; Armin Hornung (sviluppatori, dalla pagina)
Titolo: OctoMap — An Efficient Probabilistic 3D Mapping Framework Based on Octrees (sito e sorgente)
Sede e anno: octomap.github.io; ramo `devel` del deposito, commit non annotato
Identificativo: manca
Link: https://octomap.github.io/ ; https://github.com/OctoMap/octomap/blob/devel/octomap/src/AbstractOccupancyOcTree.cpp ; https://github.com/OctoMap/octomap/blob/devel/octomap/include/octomap/OccupancyOcTreeBase.h
Verifica: verificata dal curatore il 14-11-2026 [T]: sul sito «Unknown areas of the environment are implicitly encoded in the map», licenza «New BSD», visualizzatore `octovis` GPL v2; nel sorgente `setProbHit(0.7)`, `setProbMiss(0.4)`, 0,1192 e 0,971
Usata per: lo sconosciuto è implicito; parametri predefiniti 0,7 / 0,4 / 0,1192 / 0,971 (3 colpi per passare da libero a occupato: conto del ruolo); regola «libero esplicito, sconosciuto implicito» — `f7-estensione/01-matematico/CONSEGNA.md` riga 78; `f7-estensione/03-nuvole-punti/CONSEGNA.md` riga 38; `f7-estensione/05-esperto-dominio/CONSEGNA.md` righe 24 e 80 (S1); `bozza_iniziale/Proposta MLE Matrice Bayesiana (1).md` righe 1696 e 2932
Note: l'articolo di riferimento (Hornung, Wurm, Bennewitz, Stachniss, Burgard, Autonomous Robots 34(3):189–206, 2013, DOI 10.1007/s10514-012-9321-0) è già verificato per i soli dati bibliografici in f3; confermato oggi [API].

### mrpt-octomap-opzioni
Tipo: documentazione di software
Autori: MRPT (Mobile Robot Programming Toolkit)
Titolo: `mrpt::maps::COctoMapBase::TInsertionOptions`
Sede e anno: docs.mrpt.org, versione «latest» (non fissata)
Identificativo: manca
Link: https://docs.mrpt.org/reference/latest/struct_mrpt_maps_COctoMapBase_TInsertionOptions.html
Verifica: verificata dal curatore il 14-11-2026 [T]: 0,7, 0,4, 0,1192 e 0,971 presenti
Usata per: parametri predefiniti di OctoMap — `f7-estensione/08-creativo/CONSEGNA.md` riga 23
Note: correzione C11: è la documentazione di una libreria terza; citare `octomap`.

### ethz-voxblox
Tipo: deposito di codice
Autori: ETH Zürich, Autonomous Systems Lab
Titolo: voxblox
Sede e anno: GitHub; commit non annotato
Identificativo: manca
Link: https://github.com/ethz-asl/voxblox
Verifica: verificata dal curatore il 14-11-2026 [T] per la licenza: «BSD» presente nella pagina del deposito
Usata per: licenza BSD-3, distanza con segno troncata a strati — `f7-estensione/05-esperto-dominio/CONSEGNA.md` righe 25 e 80 (S2)
Note: la frase sul tempo reale è in `oleynikova2017`.

### ufomap-deposito
Tipo: deposito di codice
Autori: Daniel Duberg e altri (organizzazione UnknownFreeOccupied)
Titolo: UFOMap
Sede e anno: GitHub, ramo `master`; commit non annotato
Identificativo: manca
Link: https://github.com/UnknownFreeOccupied/ufomap
Verifica: verificata dal curatore il 14-11-2026 [T]: nel README «Colored UFOMap constructed in real-time (2 Hz) at 2 mm voxel size»; la licenza BSD-2 non è nel README: non ricontrollata
Usata per: «real-time (2 Hz) at 2 mm»; licenza BSD-2 — `f7-estensione/05-esperto-dominio/CONSEGNA.md` righe 26 e 80 (S3)
Note: correzione C2.

### bonxai
Tipo: deposito di codice
Autori: Davide Faconti
Titolo: Bonxai
Sede e anno: GitHub, ramo `main`; commit non annotato
Identificativo: manca
Link: https://github.com/facontidavide/Bonxai
Verifica: verificata dal curatore il 14-11-2026 [T]: nel README «Bonxai_Create 1165 us», «Octomap_Create 25522 us», «Benchmark (preliminary)», «Sparse», «Unbounded»; «MPL» presente nella pagina del deposito
Usata per: creazione 1165 µs contro 25 522 di OctoMap («preliminary»); struttura «Sparse» e «Unbounded»; licenza MPL-2.0 — `f7-estensione/05-esperto-dominio/CONSEGNA.md` righe 17, 28 e 80 (S4)
Note: l'autore stesso avverte: «Take these numbers with a grain of salt».

### openvdb
Tipo: deposito di codice
Autori: Academy Software Foundation
Titolo: OpenVDB
Sede e anno: GitHub; commit non annotato
Identificativo: manca
Link: https://github.com/AcademySoftwareFoundation/openvdb
Verifica: verificata dal curatore il 14-11-2026 [T] per la licenza: «Apache» e «MPL» presenti nella pagina del deposito
Usata per: albero gerarchico sparso; licenza Apache 2.0 (era MPL 2.0) — `f7-estensione/05-esperto-dominio/CONSEGNA.md` righe 27 e 80 (S5)
Note: —

### anybotics-grid-map
Tipo: deposito di codice
Autori: ANYbotics (in origine P. Fankhauser, ETH: a memoria, non verificato)
Titolo: grid_map
Sede e anno: GitHub; commit non annotato
Identificativo: manca
Link: https://github.com/ANYbotics/grid_map
Verifica: verificata dal curatore il 14-11-2026 [T]: «BSD» e «circular buffer» presenti nella pagina del deposito
Usata per: mappe a più strati con memoria circolare, come riferimento vicino alla struttura dati della bozza — `bozza_iniziale/Proposta MLE Matrice Bayesiana (1).md` righe 1891, 1966, 2048, 2689, 2932
Note: la bozza non ne trae cifre.

### nav2
Tipo: documentazione di software
Autori: Open Navigation / comunità Nav2
Titolo: Nav2 (documentazione)
Sede e anno: docs.nav2.org; versione non annotata
Identificativo: manca
Link: https://docs.nav2.org/
Verifica: aperta dal ruolo che la cita (la bozza); dal curatore solo [200] (la pagina è un rinvio di 378 byte)
Usata per: mappe di costo scorrevoli e strato degli ostacoli da sensori 3D — `bozza_iniziale/Proposta MLE Matrice Bayesiana (1).md` righe 542, 1970, 2932
Note: —

### librealsense
Tipo: documentazione di software
Autori: RealSense (già Intel RealSense)
Titolo: librealsense — `rs_frame.h`, `doc/frame_metadata.md`, `doc/sample-data.md`, `doc/post-processing-filters.md`, note della versione v2.59.1
Sede e anno: GitHub, ramo `master` (commit non annotato); v2.59.1 dell'11-10-2026 secondo il ruolo
Identificativo: v2.59.1
Link: https://github.com/IntelRealSense/librealsense/blob/master/include/librealsense2/h/rs_frame.h ; https://github.com/IntelRealSense/librealsense/blob/master/doc/frame_metadata.md ; https://github.com/realsenseai/librealsense/blob/master/doc/sample-data.md ; https://github.com/realsenseai/librealsense/releases/tag/v2.59.1
Verifica: verificata dal curatore il 14-11-2026 [T]: in `rs_frame.h` «Timestamp of the middle of sensor's exposure calculated by device» e `RS2_TIMESTAMP_DOMAIN_GLOBAL_TIME` («…converted to OS system clock…»); nelle note della v2.59.1 «Ubuntu 26.04/24.04/22.04/20.04», «Kernel versions: 6.[2, 5, 8, 11, 14]», «L515 … v2.50.0 validated, v2.54.2 supports but not validated»; in `frame_metadata.md` «kernel» e «patch» presenti
Usata per: marca di metà esposizione e dominio dell'orologio — `f9-preproposta/02-tempo-reale/CONSEGNA.md` riga 64; supporto dell'L515 e dei kernel (il 7.3 della macchina non è in elenco) — `f10-dati/04-embedded/PREVISIONI.md` (E4), `INVENTARIO_E_DECISIONE.md` ([2]); file di esempio — `f10-dati/01-ricercatore/DATI_PUBBLICI.md` §2; `f10-dati/02-sensori/MODELLO_SENSORE.md` (S4, S5)
Note: il deposito è passato da `IntelRealSense` a `realsenseai` (rinvio). Lo stato odierno dei metadati su Linux è «non verificato» per il ruolo. Licenza Apache-2.0 non riletta.

### pyrealsense2-pypi
Tipo: documentazione di software (registro dei pacchetti)
Autori: RealSense
Titolo: pyrealsense2 su PyPI
Sede e anno: PyPI; versione 2.59.1.11053
Identificativo: 2.59.1.11053
Link: https://pypi.org/pypi/pyrealsense2/json
Verifica: aperta dal ruolo che la cita ([g]); dal curatore solo [200]
Usata per: ruote cp39–cp314 per Linux x86_64 e aarch64 e Windows; la 2.54.2.5684 solo cp37–cp311 — `f10-dati/04-embedded/PREVISIONI.md` (E5), `INVENTARIO_E_DECISIONE.md` ([1]); `f10-dati/02-sensori/MODELLO_SENSORE.md` riga 63
Note: —

### orbbec-sdk-v2
Tipo: deposito di codice
Autori: Orbbec
Titolo: OrbbecSDK_v2 (README) e pyorbbecsdk2 su PyPI
Sede e anno: GitHub e PyPI; SDK v2.10.6, pyorbbecsdk2 2.1.3 secondo il ruolo
Identificativo: v2.10.6; 2.1.3
Link: https://github.com/orbbec/OrbbecSDK_v2 ; https://pypi.org/pypi/pyorbbecsdk2/json
Verifica: aperta dal ruolo che la cita ([g]); dal curatore [T] parziale: «Astra» e «not supported» presenti nel README; versioni non ricontrollate
Usata per: quali modelli Astra sono supportati dalla v2 e a quali condizioni (aggiornamento del firmware) — `f10-dati/04-embedded/PREVISIONI.md` (E6), `INVENTARIO_E_DECISIONE.md` ([3])
Note: l'aggiornamento del firmware è una scrittura sul dispositivo (avviso del ruolo).

### luxonis-depthai
Tipo: documentazione di software
Autori: Luxonis
Titolo: depthai su PyPI; USB deployment guide
Sede e anno: depthai 3.12.1 dell'11-11-2026 secondo il ruolo
Identificativo: 3.12.1
Link: https://pypi.org/pypi/depthai/json ; https://docs.luxonis.com/hardware/platform/deploy/usb-deployment-guide/
Verifica: aperta dal ruolo che la cita ([g]); dal curatore [T] parziale: «03e7» e «USB3» presenti nella guida; versione non ricontrollata
Usata per: regola udev per il produttore 03e7, cavo USB 3, alimentazione — `f10-dati/04-embedded/PREVISIONI.md` (E7), `INVENTARIO_E_DECISIONE.md` ([4], [5])
Note: —

### openkinect-libfreenect
Tipo: deposito di codice
Autori: OpenKinect
Titolo: libfreenect (v0.6.4) e libfreenect2 (v0.2.1)
Sede e anno: GitHub; v0.6.4 del 20-9-2022 e v0.2.1 del 6-8-2021 secondo il ruolo
Identificativo: v0.6.4; v0.2.1
Link: https://github.com/OpenKinect/libfreenect ; https://github.com/OpenKinect/libfreenect2/releases/tag/v0.2.1
Verifica: aperta dal ruolo che la cita ([g]); dal curatore [T] parziale: «v0.2.1» presente nella pagina della versione; date non ricontrollate
Usata per: stato dei driver liberi per Kinect v1 e v2; USB 3 obbligatorio per il v2 — `f10-dati/04-embedded/PREVISIONI.md` (E1, E2), `INVENTARIO_E_DECISIONE.md` ([7], [10])
Note: licenza Apache 2.0 / GPL 2 secondo il ruolo.

### microsoft-azure-kinect-sdk
Tipo: deposito di codice
Autori: Microsoft
Titolo: Azure-Kinect-Sensor-SDK
Sede e anno: GitHub; archiviato il 22-8-2024, ultima versione v1.4.2
Identificativo: v1.4.2
Link: https://github.com/microsoft/Azure-Kinect-Sensor-SDK/releases
Verifica: verificata dal curatore il 14-11-2026 [T]: «archived» e «v1.4.2» presenti nella pagina
Usata per: deposito archiviato, pacchetti solo per Ubuntu 18.04 — `f10-dati/04-embedded/PREVISIONI.md` (E3), `INVENTARIO_E_DECISIONE.md` ([9])
Note: la data dell'archiviazione e «Ubuntu 18.04» non ricontrollate.

### linux-gspca-kinect
Tipo: deposito di codice
Autori: sviluppatori del kernel Linux
Titolo: `drivers/media/usb/gspca/kinect.c`
Sede e anno: ramo `master` di torvalds/linux; commit non annotato
Identificativo: manca
Link: https://raw.githubusercontent.com/torvalds/linux/master/drivers/media/usb/gspca/kinect.c
Verifica: verificata dal curatore il 14-11-2026 [T]: `Y10BPACK` (3 volte) e `depth_mode` (4 volte) presenti
Usata per: il driver del kernel dà profondità grezza a 10 bit impacchettata, non millimetri — `f10-dati/04-embedded/PREVISIONI.md` (E11)
Note: GPL.

### strayrobots-scanner-formato
Tipo: documentazione di software
Autori: Stray Robots
Titolo: Stray Scanner — `docs/format.md`
Sede e anno: GitHub, ramo `main`
Identificativo: manca
Link: https://github.com/strayrobots/scanner/blob/main/docs/format.md
Verifica: verificata dal curatore il 14-11-2026 [T]: 256, 192 e «millimeters» presenti
Usata per: profondità PNG a 16 bit in millimetri, 256 × 192 — `f10-dati/04-embedded/PREVISIONI.md` (E8), `INVENTARIO_E_DECISIONE.md` ([13])
Note: il convertitore del ruolo è provato solo su una cartella finta.

### rosbags
Tipo: documentazione di software (pacchetto)
Autori: Ternaris
Titolo: rosbags 0.11.9
Sede e anno: PyPI; progetto su GitLab (ternaris/rosbags)
Identificativo: 0.11.9; sha256 `2d0df7de565dc13abd444a3c2681911fc6ef88095da3faced5c99719e5dc0fa4` (dal ruolo)
Link: https://files.pythonhosted.org/packages/eb/f8/84529aea85bec7395bb5aa7f4401ea2d7e6135cb367e36493851b859917b/rosbags-0.11.9.tar.gz
Verifica: aperta dal ruolo che la cita (impronta confrontata con quella di PyPI); non ricontrollata da me
Usata per: lettura dei file `.bag` in Python puro; prova dell'infrastruttura di scaricamento — `f10-dati/03-infrastruttura/PREVISIONI.md` (infra-P1, P8), `AMBIENTE.md` righe 33 e 83; `f10-dati/01-ricercatore/DATI_PUBBLICI.md` §4
Note: licenza Apache-2.0 dai metadati di PyPI. Le altre librerie dell'ambiente (numpy 2.5.4, scipy 1.18.1, opencv, pillow) sono strumenti, non fonti: stanno in `AMBIENTE.md`.

### simulatori-di-profondita
Tipo: deposito di codice (voce di gruppo: otto strumenti esaminati)
Autori: vari
Titolo: Open3D (`RaycastingScene`); Habitat-Sim (modello Redwood); simkinect; SimSense e SAPIEN; BlenderProc; Gazebo `gz-sensors`; Isaac Sim
Sede e anno: GitHub, rami principali; commit non annotati
Identificativo: manca
Link: https://raw.githubusercontent.com/isl-org/Open3D/main/ ; https://raw.githubusercontent.com/facebookresearch/habitat-sim/main/ ; https://raw.githubusercontent.com/ankurhanda/simkinect/master/README.md ; https://raw.githubusercontent.com/angli66/simsense/main/ ; https://raw.githubusercontent.com/haosulab/SAPIEN/master/ ; https://raw.githubusercontent.com/DLR-RM/BlenderProc/main/ ; https://raw.githubusercontent.com/gazebosim/gz-sensors/main/
Verifica: aperta dal ruolo che la cita (copie in `f10-dati/02-sensori/scaricati/`, con `PROVENIENZA.md`); non ricontrollata da me; Isaac Sim: vista solo nel riassunto di un motore di ricerca
Usata per: nessuno strumento su sola CPU riproduce buchi e occlusione di una D4xx con un profilo pronto (regge su 8 strumenti: non è una prova universale); licenze MIT, Apache-2.0, GPL-3.0, assente per simkinect — `f10-dati/02-sensori/MODELLO_SENSORE.md` righe 60–70, `PREVISIONI.md` righe 15 e 30
Note: zero strumenti trovati su un campione non prova che non esistano.

---

## E. Insiemi di dati

### tum-rgbd
Tipo: insieme di dati
Autori: Jürgen Sturm; Nikolas Engelhard; Felix Endres; Wolfram Burgard; Daniel Cremers
Titolo: TUM RGB-D Benchmark, sequenza `freiburg3_walking_static`; articolo associato: «A benchmark for the evaluation of RGB-D SLAM systems»
Sede e anno: IEEE/RSJ IROS 2012, pp. 573–580
Identificativo: DOI 10.1109/IROS.2012.6385773
Link: https://cvg.cit.tum.de/data/datasets/rgbd-dataset/download ; https://cvg.cit.tum.de/rgbd/dataset/freiburg3/rgbd_dataset_freiburg3_walking_static.tgz
Verifica: verificata dal curatore il 14-11-2026 [API] per l'articolo (aggiunto da me: il ruolo cita solo la pagina) e [T] per la presenza della sequenza nella pagina; la licenza «CC BY 4.0» NON l'ho trovata nella pagina dei file: non verificata
Usata per: sequenza minima di 474 074 105 byte, Kinect v1, 640×480, 30 Hz; scelta n. 1 per le ipotesi 1, 2, 5, 6 del contratto dei dati — `f10-dati/01-ricercatore/DATI_PUBBLICI.md` §1, §4, §5
Note: luce strutturata, non stereo attivo; solo la posa della camera come verità. La licenza va riletta nella pagina principale dell'insieme.

### friburgo-rgbd-people
Tipo: insieme di dati
Autori: Luciano Spinello; Matthias Luber; Kai O. Arras
Titolo: RGB-D People Dataset; articoli associati: «People Detection in RGB-D Data» (IROS 2011, pp. 3838–3843) e «People Tracking in RGB-D Data With On-line Boosted Target Models» (IROS 2011, pp. 3844–3849)
Sede e anno: Università di Friburgo, 2011
Identificativo: DOI 10.1109/IROS.2011.6095074; DOI 10.1109/IROS.2011.6095075
Link: http://www2.informatik.uni-freiburg.de/~spinello/RGBD-dataset.html ; http://www2.informatik.uni-freiburg.de/~spinello/sw/rgbd_people_unihall.tar.gz
Verifica: verificata dal curatore il 14-11-2026 [T] e [API]: nella pagina «3000+ RGB-D frames», tre Kinect montati in verticale, licenza «Creative Commons Attribution-Noncommercial-Share Alike 3.0 Unported», «visibility»; articoli confermati su Crossref
Usata per: archivio di 2 805 714 553 byte; visibilità annotata (0, 1, 2); scelta n. 3 per le ipotesi 4, 5 e 3 — `f10-dati/01-ricercatore/DATI_PUBBLICI.md` §1, §5
Note: uso non commerciale; profondità grezza a 11 bit, non metrica. Il link di scaricamento scritto nella pagina (`www.informatik…`) è rotto secondo il ruolo.

### bonn-rgbd-dynamic
Tipo: insieme di dati
Autori: Emanuele Palazzolo; Jens Behley; Philipp Lottes; Philippe Giguère; Cyrill Stachniss
Titolo: Bonn RGB-D Dynamic Dataset; articolo associato: «ReFusion: 3D Reconstruction in Dynamic Environments for RGB-D Cameras Exploiting Residuals»
Sede e anno: IEEE/RSJ IROS 2019, pp. 7855–7862
Identificativo: DOI 10.1109/IROS40897.2019.8967590
Link: https://www.ipb.uni-bonn.de/data/rgbd-dynamic-dataset/
Verifica: verificata dal curatore il 14-11-2026 [T] e [API]: pagina aperta, `moving_obstructing_box` presente, articolo indicato nella pagina; nessuna licenza nel testo della pagina (coerente con «non dichiarata»)
Usata per: ripiego se il primo insieme non risponde (320 845 314 byte) — `f10-dati/01-ricercatore/DATI_PUBBLICI.md` §1, §5
Note: camera in moto; senza licenza dichiarata l'uso va chiesto.

### princeton-tracking-benchmark
Tipo: insieme di dati
Autori: Shuran Song; Jianxiong Xiao
Titolo: Princeton Tracking Benchmark; articolo associato: «Tracking Revisited Using RGBD Camera: Unified Benchmark and Baselines»
Sede e anno: IEEE ICCV 2013, pp. 233–240
Identificativo: DOI 10.1109/ICCV.2013.36
Link: https://tracking.cs.princeton.edu/dataset.html
Verifica: verificata dal curatore il 14-11-2026 [T] e [API]: nella pagina profondità PNG a 16 bit «with the first 3 bit swap to the last», `frames.json` con K; licenza non dichiarata
Usata per: ripiego: `ValidationSet.zip` (631 649 593 byte, 5 sequenze) — `f10-dati/01-ricercatore/DATI_PUBBLICI.md` §1, §5
Note: scene ravvicinate, un bersaglio.

### depthtrack
Tipo: insieme di dati
Autori: Song Yan; Jinyu Yang; Jani Käpylä; Feng Zheng; Aleš Leonardis; Joni-Kristian Kämäräinen
Titolo: DepthTrack Test Set (ICCV2021); articolo associato: «DepthTrack: Unveiling the Power of RGBD Tracking»
Sede e anno: IEEE/CVF ICCV 2021, pp. 10705–10713; Zenodo, 19-12-2021
Identificativo: DOI 10.5281/zenodo.5792146; DOI 10.1109/ICCV48922.2021.01055
Link: https://zenodo.org/records/5792146
Verifica: verificata dal curatore il 14-11-2026 [API Zenodo e Crossref]: 50 sequenze RGB-D, licenza CC BY 4.0
Usata per: ripiego: `human02_indoor.zip` (578 368 987 byte, 1740 fotogrammi) — `f10-dati/01-ricercatore/DATI_PUBBLICI.md` §1, §5
Note: il sensore (una RealSense D415 «a memoria») non è stato trovato nelle pagine lette: non verificato.

### park2026
Tipo: insieme di dati (con articolo di workshop)
Autori: Yeeun Park; Miqdad Naduthodi; Suryansh Kumar
Titolo: HUM4D — «A Dataset and Evaluation for Complex 4D Markerless Human Motion Capture»
Sede e anno: IEEE/CVF CVPR 2026, 4D World Models Workshop
Identificativo: manca
Link: https://parkyeeun23.github.io/HUM4D/ ; https://github.com/ParkYeeun23/hum4d-processing
Verifica: dato diverso: è un articolo di workshop, non della conferenza principale (correzione C1) [T]; confermati [T]: 44 sequenze, 6 camere RGB-D sincronizzate, RealSense D455, altezza 1,45 m, raggio 3 m, Vicon, CC BY 4.0, 83 768 fotogrammi
Usata per: «il più vicino al sensore della squadra»; proposta ricercatore-1 (scaricare una cartella dal browser) — `f10-dati/01-ricercatore/DATI_PUBBLICI.md` §1, §6
Note: nessun archivio scaricabile con `curl` (cartelle di Google Drive).

### oxford-ihm
Tipo: insieme di dati
Autori: Mark Nicholas Finean; Luka Petrović; Wolfgang Merkt; Ivan Marković; Ioannis Havoutis
Titolo: Oxford Indoor Human Motion Dataset; articolo associato: «Motion planning in dynamic environments using context-aware human trajectory prediction»
Sede e anno: Robotics and Autonomous Systems 166:104450, 2023
Identificativo: DOI 10.1016/j.robot.2023.104450
Link: https://articulated.robots.ox.ac.uk/oxford-indoor-human-motion-dataset/
Verifica: verificata dal curatore il 14-11-2026 [T] e [API]: «~60 minutes of rosbag data», cattura del moto a 100 Hz, camere RGB-D ferme e sul robot; «D435», «CC BY-NC-SA» e l'accesso su richiesta NON sono nel testo della pagina che ho scaricato: non verificati
Usata per: ideale ma non ottenibile in 14 ore; da chiedere per il dopo-hackathon — `f10-dati/01-ricercatore/DATI_PUBBLICI.md` §1, §6
Note: licenza e modello della camera da rileggere nella pagina di scaricamento.

### thor
Tipo: insieme di dati
Autori: Andrey Rudenko; Tomasz P. Kucner; Chittaranjan S. Swaminathan; Ravi T. Chadalavada; Kai O. Arras; Achim J. Lilienthal
Titolo: THÖR — people tracks; articolo associato: «THÖR: Human-Robot Navigation Data Collection and Accurate Motion Trajectories Dataset»
Sede e anno: IEEE Robotics and Automation Letters 5(2):676–682, 2020; Zenodo, 10-9-2019
Identificativo: DOI 10.5281/zenodo.3382145; DOI 10.1109/LRA.2020.2965416; arXiv:1909.04403
Link: https://zenodo.org/records/3382145
Verifica: verificata dal curatore il 14-11-2026 [API Zenodo, arXiv, Crossref]: autori, licenza CC BY 4.0, legame con l'articolo; i 100 Hz e i 339 s non ricontrollati
Usata per: traiettorie vere di persone al chiuso a 100 Hz; scelta n. 2 per l'ipotesi 4 (errore della previsione contro il tempo d'occlusione), 99 517 196 byte — `f10-dati/01-ricercatore/DATI_PUBBLICI.md` §3, §5
Note: nessuna camera di profondità: parte da posizioni perfette.

### drow
Tipo: insieme di dati
Autori: Lucas Beyer; Alexander Hermans; Bastian Leibe (2016); con Timm Linder e Kai O. Arras (2018)
Titolo: DROW; articoli associati: «DROW: Real-Time Deep Learning based Wheelchair Detection in 2D Range Data» e «Deep Person Detection in Two-Dimensional Range Data»
Sede e anno: arXiv 2016 (sede a stampa: non verificata); IEEE Robotics and Automation Letters 3(3):2726–2733, 2018
Identificativo: arXiv:1603.02636; DOI 10.1109/LRA.2018.2835510
Link: https://github.com/VisualComputingInstitute/DROW ; https://github.com/VisualComputingInstitute/DROW/releases/download/v2/DROWv2-data.zip
Verifica: verificata dal curatore il 14-11-2026 [API] e [T]: nella pagina del deposito «MIT», «S300», «450» presenti; il 5 % delle scansioni annotate non ricontrollato
Usata per: LiDAR 2D SICK S300 a 37 cm, 225° in 450 punti, persone annotate sul 5 % delle scansioni; 197 970 996 byte — `f10-dati/01-ricercatore/DATI_PUBBLICI.md` §3; copia del README in `f10-dati/01-ricercatore/pagine/drow_readme.md`
Note: il ruolo scrive il link come `RWTHVision/DROW` (rinvia a `VisualComputingInstitute`).

### frog
Tipo: insieme di dati
Autori: Fernando Amodeo; Noé Pérez-Higueras; Luis Merino; Fernando Caballero
Titolo: FROG: a new people detection dataset for knee-high 2D range finders
Sede e anno: Frontiers in Robotics and AI, vol. 12, 2025
Identificativo: DOI 10.3389/frobt.2025.1671673
Link: https://robotics.upo.es/datasets/frog/laser2d_people/
Verifica: verificata dal curatore il 14-11-2026 [T] e [API]: pagina aperta, articolo indicato; nessuna licenza nel testo (coerente con «non dichiarata»); il nome del file `.h5` non ricontrollato
Usata per: scansioni da 720 punti con persone annotate su tutte, robot in moto; 148 746 736 byte — `f10-dati/01-ricercatore/DATI_PUBBLICI.md` §3
Note: —

### zenodo-radar-mmwave-occlusione
Tipo: insieme di dati
Autori: Tao Wang
Titolo: The mmWave radar point cloud dataset for person identification under various occluded conditions
Sede e anno: Zenodo, 26-9-2023
Identificativo: DOI 10.5281/zenodo.8377254
Link: https://zenodo.org/records/8377254
Verifica: verificata dal curatore il 14-11-2026 [API Zenodo]: 9 persone che camminano dietro l'ostacolo, radar FMCW più camera RGB-D, CC BY 4.0
Usata per: radar a onde millimetriche con persone dietro un ostacolo; 508 208 132 byte — `f10-dati/01-ricercatore/DATI_PUBBLICI.md` §3
Note: nessuna posizione vera dichiarata.

### zenodo-tof-vl53l5cx
Tipo: insieme di dati
Autori: Giammarco Caroleo; Alessandro Albini; Perla Maiolino
Titolo: DS.ToFInitialCharacterization_InChToF.1.0; articolo associato: «Tiny LiDARs for Manipulator Self-Awareness: Sensor Characterization and Initial Localization Experiments» (Caroleo, Albini, De Martini, Barfoot, Maiolino)
Sede e anno: Zenodo, 24-9-2025; arXiv 5-3-2025 (IROS secondo il commento arXiv: anno non letto)
Identificativo: DOI 10.5281/zenodo.17190312; arXiv:2503.03449
Link: https://zenodo.org/records/17190312
Verifica: verificata dal curatore il 14-11-2026 [API Zenodo e arXiv]: tre VL53L5CX su un braccio robotico davanti a una lavagna in posizione nota, CC BY 4.0
Usata per: unico insieme pubblico trovato per il tempo di volo multizona, senza persone (lacuna dichiarata) — `f10-dati/01-ricercatore/DATI_PUBBLICI.md` §3
Note: VL53L5CX, non L7CX né L8CX.

### realsense-file-di-esempio
Tipo: insieme di dati (file di esempio del costruttore)
Autori: RealSense
Titolo: Sample Data (`doc/sample-data.md`): `D435i_Depth_and_IMU_Stands_still.bag`, `stairs.bag`, `structured.bag`, `outdoors.bag`
Sede e anno: librealsense; date: non lette
Identificativo: manca
Link: https://github.com/realsenseai/librealsense/blob/master/doc/sample-data.md ; https://librealsense.realsenseai.com/rs-tests/
Verifica: aperta dal ruolo che la cita (dimensioni e indici letti dai file); dal curatore solo [200] sulla pagina
Usata per: registrazioni grezze di stereo attivo (107–423 MB, 4–8 s) per le ipotesi 1, 2 e 6, senza verità di riferimento — `f10-dati/01-ricercatore/DATI_PUBBLICI.md` §2, §5; `f10-dati/02-sensori/MODELLO_SENSORE.md` riga 63
Note: licenza dei file non dichiarata; se contengano persone non è verificato.

### insiemi-non-raggiungibili
Tipo: insieme di dati (voce di gruppo)
Autori: vari
Titolo: Kinect Tracking Precision (KTP); pedoni RGB-D dell'EPFL; JRDB; CDTB
Sede e anno: manca
Identificativo: manca
Link: manca (il ruolo non riporta gli indirizzi)
Verifica: non raggiungibile (KTP ed EPFL: 404 secondo il ruolo; JRDB chiede un conto; CDTB non approfondito); non ricontrollata da me
Usata per: esclusi dalla scelta — `f10-dati/01-ricercatore/DATI_PUBBLICI.md` §1
Note: nessun dato ne dipende.
