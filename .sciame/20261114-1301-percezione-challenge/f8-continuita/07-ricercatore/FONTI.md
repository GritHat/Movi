# FONTI — sciame-ricercatore, f8 (continuità visiva), consultate il 14 novembre 2026

**Legenda.** **A** = pagina aperta oggi con lo strumento di lettura (che riassume: le frasi fra «» sono quelle che lo
strumento ha riportato come testuali). **A-g** = PDF scaricato, testo estratto con `pdftotext` e frase trovata con
una ricerca testuale (più forte). **R** = vista solo nel riassunto del motore di ricerca, NON aperta: è una pista, non
una prova. Ricerche fatte: 17 interrogazioni. I riferimenti vanno comunque passati al curatore delle fonti.

## 1. Previsione a breve termine e taratura
- **S1 [A]** Hetzel, Reichert, Doll, Sick, «Reliable Probabilistic Human Trajectory Prediction for Autonomous
  Applications», arXiv 2410.06905v2 (10/2024; sede non indicata). Misura l'affidabilità (frequenza osservata contro
  livello dichiarato, media R_avg e minima R_min su livelli e orizzonti) e la nitidezza (area delle regioni al 68 e al
  95 %). Soglia proposta: R_avg ≥ 0,95 e R_min ≥ 0,90. ETH/UCY (R_avg / R_min): Trajectron++ 64,9 / 30,9;
  Social-Implicit 82,7 / 62,5; MID 84,6 / 65,9; FlowChain 86,5 / 62,2; il loro 91,1 / 72,5. «None of the tested models
  can achieve suitable Reliability scores». Trasferimento su altri dati: R_min 71,2 % e 70,2 %. Con 100 ms di storia:
  86,7 / 68,4. https://arxiv.org/html/2410.06905v2
- **S2 [A, riassunto]** Pouria, Golchoubian, Driggs-Campbell, «Rethinking Gaussian Trajectory Predictors: Calibrated
  Uncertainty for Safe Planning», arXiv 2603.10407 (3/2026, v2 7/2026): la perdita NLL «is prone to predict over- or
  under-confident distributions»; nessun numero nel riassunto. https://arxiv.org/abs/2603.10407
- **S3 [A, riassunto]** Kress, Jeske, Zernetsch, Doll, Sick, arXiv 2106.02598 (2021): previsioni valutate per
  «reliability, sharpness, and positional accuracy», orizzonte 2,52 s. La frase sulle curve «troppo sicure» è solo
  [R]. https://arxiv.org/abs/2106.02598 — [R] CovarianceNet, arXiv 2109.02965.
- **S7 [aperta in f1, verificata in f3]** Schöller e altri, RA-L 2020, arXiv 1903.07933: a 4,8 s velocità costante
  0,39 / 0,83 m; miglior appreso deterministico 0,44 / 0,91; generativo a 20 campioni 0,32 / 0,60.
- **S8 [A, riassunto]** Uhlemann, Fent, Lienkamp, IEEE T-ITS, arXiv 2308.05194 (v3 4/2024): «a constant velocity
  model (CVM) provides a good approximation of the overall dynamics in the majority of cases». Nessun numero nel
  riassunto. https://arxiv.org/abs/2308.05194
- **S9 [A, copia ar5iv]** Mercat e altri, arXiv 1908.11472 (veicoli, NGSIM, 3 s di storia, 5 s di previsione). RMSE a
  1 / 2 / 3 / 4 / 5 s: Kalman a velocità costante 0,75 / 1,81 / 3,16 / 4,80 / 6,70 m; V-LSTM 0,67 / 1,62 / 2,86 / 4,40 /
  6,26; Kalman-LSTM 0,68 / 1,54 / 2,72 / 4,20 / 5,95. NLL medio: 0,80…4,44 contro −0,15…3,73.
  https://ar5iv.labs.arxiv.org/html/1908.11472
- **S10 [A, riassunto]** Kim, Lee, Cho, «PlugTrack», arXiv 2511.13105 (AAAI 2026): il Kalman batte i predittori
  appresi in «up to 34% of cases» anche su moto non lineare; la proposta li fonde. https://arxiv.org/abs/2511.13105
  — **[A, riassunto]** Lv e altri, «DiffMOT», CVPR 2024, arXiv 2403.02075: «real-time at 22.7FPS», 62,3 % HOTA su
  DanceTrack; l'hardware non è nel riassunto (RTX 3090: solo [R]). https://arxiv.org/abs/2403.02075

## 2. Previsione conforme sulle traiettorie
- **S4 [A-g]** Lindemann, Cleaveland, Shim, Pappas, «Safe Planning in Dynamic Environments using Conformal
  Prediction», arXiv 2210.10254v2 (RA-L 2023: [R]). Ipotesi 2: le traiettorie di taratura sono «independently drawn
  from D»; nota 3: «In general only exchangeability is needed». Ipotesi 1: il robot non cambia la distribuzione.
  Prova: «498 of the 500 test trajectories» dentro la regione al 95 % (δ = 0,05, T = 20). Limite dichiarato:
  «potential conservatism in the prediction regions (induced by union bounding…)». https://arxiv.org/abs/2210.10254
- **S5 [A, riassunto]** Cleaveland, Lee, Pappas, Lindemann, arXiv 2304.01075 (v5 1/2024; AAAI 2024: [R]): regioni su
  più passi «not conservative» con un errore parametrizzato; prove su predittori di pedoni.
  https://arxiv.org/abs/2304.01075
- **S6 [A, riassunto]** Dixit, Lindemann e altri, arXiv 2212.00278 (L4DC 2023: [R]): previsione conforme adattiva
  «distribution-free», che usa le osservazioni **ritardate** degli agenti; prova: un drone e un frisbee, in
  simulazione. https://arxiv.org/abs/2212.00278
- **[R]** conforme robusta sotto cambio di distribuzione, arXiv 2602.12616 (simulatore ORCA); conforme adattiva nella
  navigazione fra la folla, arXiv 2508.05634; zonotopi probabilistici, arXiv 2608.05454 (copertura media 90,9 % al
  nominale 90 %, una scena di ETH/UCY tenuta fuori a turno; non per orizzonte). Non aperte.

## 3. Occlusione: posizione dell'oggetto nascosto, dati e metriche
- **S11 [A, riassunto]** Tokmakov, Li, Burgard, Gaidon, «Learning to Track with Object Permanence», arXiv 2103.14258
  (sede ICCV 2021: a memoria, non verificata oggi): insieme sintetico che «provides ground truth annotations for invisible objects».
  https://arxiv.org/abs/2103.14258
- **S12 [verificata in f3 come F20; oggi R]** Hsieh e altri, TAO-Amodal, arXiv 2312.12433: riquadri amodali; i metodi
  «struggle … under heavy occlusion».
- **S13 [A-g]** Krejčí, Kost, Xia, Svensson, Straka, «Occlusion-Aware Multi-Object Tracking via Expected Probability
  of Detection», arXiv 2511.20239v3 (8/4/2026): la probabilità di rilevamento dipende dalla visibilità; filtro a
  miscela multi-Bernoulli; prove su tre video di MOT17, dove «The visibility ratio is available for each GT BB»;
  conta veri positivi e mancati di oggetti occlusi; «computational complexities are hardly predictable»; più stime
  di oggetti occlusi danno più falsi positivi (osservazione 8). https://arxiv.org/abs/2511.20239
- **S14 [A, riassunto]** Van Hoorick e altri, TCOW, CVPR 2023, arXiv 2305.03052: resta «a considerable performance
  gap» prima di una vera permanenza dell'oggetto. https://arxiv.org/abs/2305.03052
- **S15 [A]** TAP-Vid, NeurIPS 2022 (sezione dati e banchi), arXiv 2211.03726 (primo autore Doersch: a memoria, non
  verificato oggi): la precisione di posizione vale «only for
  frames where the point is visible»; in occlusione la posizione «is typically assumed to be meaningless».
  https://arxiv.org/html/2211.03726v2
- **[A, riassunto]** Khurana, Dave, Ramanan, «Detecting Invisible People», arXiv 2012.08419: l'occlusione trattata
  come «a short-term forecasting challenge»; +11,4 % e +5,0 % di F1. https://arxiv.org/abs/2012.08419
- **S22 [R]** evidenza negativa nei filtri: Skoglar e altri, EURASIP JASP 2012 (10.1186/1687-6180-2012-26: il sito
  rimanda a un accesso, non aperta); Wyffels e Campbell, IEEE T-RO 2015 (non aperta).

## 4. Tracce «in coasting» nella sorveglianza
- **S16 [A, copia strutturata della specifica; non il PDF ufficiale]** ASTERIX categoria 062, edizione 1.18. I062/080,
  bit CST: «Age of the last received track update is higher than system dependent threshold (coasting)»; I062/290
  età dell'ultimo aggiornamento per sensore (passo 0,25 s, tetto 63,75 s); I062/500 «Estimated Accuracies»
  (posizione con passo 0,5 m, covarianza XY, velocità 0,25 m/s); bit CNF (confermata o provvisoria).
  https://zoranbosnjak.github.io/asterix-specs/specs/cat062/cats/cat1.18/definition.html — pagina ufficiale [R]:
  https://www.eurocontrol.int/publication/cat062-eurocontrol-specification-surveillance-data-exchange-asterix-part-9-category-062
- **S17 [A-g]** IMO, risoluzione MSC.192(79), 2004, norme per i radar di bordo. §5.25.4.7.1 e Tabella 3: «Tracked
  Target Accuracy (95% probability figures)» (dopo 1 min: rotta relativa 11°, CPA 1,0 NM; dopo 3 min: 3°, 0,3 NM);
  «Accuracy may be significantly reduced during … a manoeuvre of the target». §5.29.4: «The system should alert the
  user if a tracked radar target is lost … The target's last position should be clearly indicated on the display».
  https://law.resource.org/pub/us/cfr/ibr/inc/imo/imo.msc.192.2004.pdf
- **S18 [A]** Navtech, documentazione del tracciatore «Witness», «Coasting Tracks»: il coasting riporta posizioni
  previste finché il radar rivede il bersaglio; parametri: età minima e massima, numero di previsioni consecutive,
  poi la traccia è cancellata. https://navtechradar.atlassian.net/wiki/spaces/TUN/pages/255164634
- **[R]** guida amatoriale ai simboli ERAM (traccia in coasting per 5 minuti, poi cancellata): non è una fonte
  primaria. La pagina FAA dell'ordine 7110.65 ha dato 403: **non verificato**.

## 5. Previsione mostrata a una persona; errori d'interpretazione
- **S19 [A, PMC]** Padilla, Ruginski, Creem-Regehr, Cognitive Research: Principles and Implications, 2017
  (PMC5626802). Tre esperimenti (N = 179, 43, 35). Con il cono la quota che dice «l'uragano cresce nel tempo» è 0,70
  contro 0,39 con l'insieme di traiettorie (d = 0,66). Con l'insieme, l'impianto più vicino è scelto nel 64,15 % dei
  casi invece del 99,68 % quando quello lontano cade su una traiettoria. https://pmc.ncbi.nlm.nih.gov/articles/PMC5626802
- **S20 [A-g]** Kayukawa e altri, «BBeep», CHI 2019: camera RGB-D, «linear extrapolation is used to predict their
  future path», avviso a 5 s e a 2,5 s; «6 blind participants» in aeroporto; nessuna incertezza in uscita.
  https://wotipati.github.io/projects/BBeep/paper/CHI'19_BBeep_preprint.pdf
- **S21 [A]** Haghighi e altri, «HEADS-UP», arXiv 2409.20324 (9/2024): insieme egocentrico per la previsione di
  pedoni in un ausilio; gira su Jetson; nessun numero sugli utenti né sull'incertezza comunicata.
  https://arxiv.org/html/2409.20324v1
- **[R]** Hunt 2013 (tesi, fiducia dei controllori e incertezza della previsione); Weitz 2013, DLR (ellissoidi
  d'incertezza per traiettorie 4D, senza esperimento con controllori). Non aperte.

## Ingressi del progetto letti
Per intero: `CONTRATTO_CONTINUITA.md`, `regole_challenge.md`, `ADDENDUM_UTENTE.md`, `SOLUZIONE_V2.md`, `VERDETTO.md`,
`f1/3fff79e9c3ea/CONSEGNA.md` e `FONTI.md`, `f3/fonti/FONTI_VERIFICATE.md`, `proposta/VERSIONI.md`. Solo le righe
trovate con una ricerca testuale: `f2/04-torneo/TORNEO.md` (coperture), `SPECIALIZZAZIONE.md`, `MOTO_PROPRIO.md`,
`MISURE_V2_bis.md`, `proposta/proposta_sciame.tex`. Non letti: `MISURE.md`, `MISURE_V2.md`, `CONTROPROVE.md`,
`AUDIT.md`, `ATTACCO_SPECIALIZZAZIONE.md`, i simulatori, i PDF della proposta.
