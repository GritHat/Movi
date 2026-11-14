# Riferimenti, gruppo rif-3 (fase f6: quadro di dominio, specializzazione, moto proprio, attacco) — `sciame-fonti`, f11

Curatore delle fonti, 14 novembre 2026. Verifiche in rete dalle 16:11 alle 16:19 (`date -Is`), scrittura dopo.

## In testa

**Conteggio.** 59 voci.

- **40 verificate da me oggi per intero** (pagina o testo aperto, tutti i dati citati presenti).
- **15 verificate da me oggi solo in parte, o con un dato diverso** (la pagina c'è, ma una cifra o un'attribuzione non torna: vedi le correzioni).
- **4 non raggiungibili oggi**, quindi non verificate: `koschi2021`, `intel-bkm-d400`, `intel-t265-fine-produzione`, `ue-2021-664`.
- **3 erano già state verificate dal curatore in f3** (`f3/fonti/FONTI_VERIFICATE.md`): `orzechowski2018`, `nuss2018`, `realsense-confronto-camere`. Le ho riaperte oggi e stanno fra le 40.
- **Nessuna voce inesistente.** Tutti i riferimenti citati nei quattro file corrispondono a un documento reale; due link sono morti o chiusi oggi (Intel) e due sono dietro una protezione contro i programmi automatici (TUM, EUR-Lex).

**File letti** (percorsi relativi alla cartella della convocazione): `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` (fonti S1–S38), `f6-specializzazione/01-esperto-dominio/SPECIALIZZAZIONE.md` (una fonte propria, il resto rimanda al quadro), `f6-specializzazione/02-slam/MOTO_PROPRIO.md` (undici link), `f6-specializzazione/03-avversario/ATTACCO_SPECIALIZZAZIONE.md` (nessuna fonte esterna propria: rimanda a S18, S23, S31 e dichiara di non aver riaperto nessuna pagina).

**Correzioni (attribuzioni sbagliate o imprecise, cifre che non tornano).** La sigla S… è quella del quadro di dominio.

1. **S21 (`liu2022`) non parla di occlusione.** Nel testo intero dell'articolo (PDF della CVF) la radice «occlu» compare 0 volte; c'è «irregular motion caused by moving camera and view change in 3D directions». La frase del quadro §2(d), «i lavori sul tracciamento da drone nominano insieme occlusione e moto irregolare della camera (S21, S22)», regge solo per S22 (`dang2024`), che nel riassunto nomina sia «occlusion» sia i movimenti complessi del drone. Pagine: 8876–8885 secondo la CVF e mlanthology, 8866–8875 secondo il registro Crossref dell'IEEE: discordanza non risolta.
2. **S20: ED-275 non è la norma europea sul «detect and avoid» in generale.** La pagina citata la intitola «Minimum Operational Performance Standards for Airborne Collision Avoidance System Xu (ACAS Xu)», EUROCAE, 1 dicembre 2020: è la norma del solo sistema anticollisione. DO-365C (RTCA, 15 settembre 2022) è invece davvero la norma sui sistemi «Detect and Avoid». **Le cifre «35 s e oltre un chilometro» non sono in nessuna delle due pagine citate: non verificate** (il quadro stesso le dava «dal riassunto del motore»).
3. **S27 (ASTM F3442-25): «esclude gli incontri fra droni» è impreciso.** Il testo dice che la norma non tratta uccelli e pericoli naturali (punto 1.5: confermato), ma al punto 1.6.1 «defines a metric to assess the mitigation of a UA-to-UA mid-air collision, with specific safety performance thresholds to be addressed in future efforts»: gli incontri fra droni hanno una metrica, non ancora le soglie.
4. **S19: i 3 m/s non sono nella pagina dell'EASA citata.** La pagina dà i 19 m/s (droni sotto 250 g) e nomina la «low-speed function» senza cifra. La cifra giusta sta nel regolamento delegato (UE) 2019/945, allegato, parte 3 (classe C2), punto 9: «limiting the ground speed to no more than 3 m/s»; i 19 m/s nelle parti 1 e 2 (classi C0 e C1). Verificato su una copia non ufficiale (vedi `ue-2019-945`). Le cifre del quadro sono quindi giuste, la fonte indicata no.
5. **S16 (`mandaokar2026`): «errori laterali fino a 0,9 m» va precisato.** Il testo dà errori *medi* di posizione «of at most 0.15 m, 0.93 m, and 0.87 m in the x, y, and z directions». I 75 ms sono la latenza di sistema «from first detection to the avoidance command» (mediana); i 14,6 m/s e i 77 GHz ci sono. In più il testo dà 14 ms di elaborazione per fotogramma radar, che il quadro non riporta.
6. **S14 (`rossi2025`): la prestampa è ora un articolo** (Sensors 25(24), 7495, 9 dicembre 2025, DOI 10.3390/s25247495): conviene citare quello. **«Prestazioni imprevedibili» non è nel riassunto**, che dice che le prestazioni all'aperto restano «weakly quantified» e dà, fra 4 e 16 m, RMSE 0,46–0,64 m e MAE 0,40–0,51 m. Il testo intero non l'ho potuto aprire (403). Il secondo link di S14 (documento Intel sulla taratura) oggi dà 404; le cifre «0,6–6 m» e «< 2 % a 4 m» le ho trovate nella pagina di confronto del costruttore (`realsense-confronto-camere`), l'errore che cresce con il quadrato della distanza nella guida alla taratura in rete.
7. **S7: «opzione per il 51 %» non è nella pagina citata**, che dice «opzione per il controllo entro 24 mesi». Il 20 %, il drone H815 e gli usi ci sono.
8. **S17 (FLIR Boson): «circa 0,6–1 W» è confermato solo per il valore basso** («starting at 600 mW»); 1 W non è nella pagina. I 7,5 g ci sono («starting at 7.5 grams»).
9. **S28: la pagina dell'EASA citata nomina i regolamenti 2019/947 e 2019/945, non il 2021/664 né la decisione 2025/018/R.** La decisione è confermata dall'intestazione di S24; il 2021/664 resta non verificato (EUR-Lex non raggiungibile).
10. **S29: «il primo a nominare le macchine mobili autonome» non è verificato** (EUR-Lex non raggiungibile). La data del 20 gennaio 2027 è confermata da una pagina della Commissione europea.
11. **S38 è un contributo di un'autrice sola in un blog accademico** (Plixavra Vogiatzoglou, Verfassungsblog, 9 dicembre 2024): fonte secondaria. La citazione fra «» c'è; l'espressione «duplice uso» nel testo non c'è: dice che se lo stesso sistema è usato anche per l'ordine pubblico deve rispettare il regolamento.
12. **S2: la pagina della società non nomina CTMAVIO né «prevalentemente nel 2026»**: questi due dati stanno in S3, S4 e S5.
13. **`MOTO_PROPRIO.md`, cuVSLAM:** la pagina conferma «GPU-accelerated library for stereo-visual-inertial SLAM and odometry»; della licenza e del «pacchetto Python non commerciale» nella pagina non c'è traccia: non verificati. **T265:** il link di Intel oggi rimanda a una pagina d'errore: «fuori produzione dal 2022» e la frase «with 3rd Party SLAM SW» restano non verificate.
14. **S36 (`shan2022`) è una fonte d'uso, non la fonte del metodo:** è un articolo sulla fusione di dati fra veicoli che *applica* l'intersezione delle covarianze (nel testo, non nel riassunto) e ne cita l'origine come suo riferimento [8], che non ho verificato.
15. **S13 (`delmerico2018`):** il quadro e il moto proprio lo danno «non letto». Oggi il testo è stato estratto: i dati bibliografici sono giusti; nessuna cifra del progetto viene da lì.

**Regole violate o scostamenti miei.**

- Regola 3: non ho scritto previsioni prima delle verifiche.
- Regola 5: lo strumento di lettura ha salvato da solo un PDF (S13) fuori dalla cartella di consegna, nella cartella dei risultati della sessione; l'ho copiato nella cartella temporanea della sessione e convertito in testo, senza eseguire niente. Tutto il materiale scaricato sta nella cartella temporanea, non nel progetto.
- I link delle fonti contengono il nome della società promotrice: li ho aperti così come sono citati. Nelle ricerche non ho messo nomi di persone del progetto né dettagli del progetto; in due ricerche compaiono cognomi di autori di articoli.
- Stati: tutte le verifiche qui sotto riguardano l'esistenza delle fonti e la presenza dei dati citati. Non cambiano lo stato di nessun enunciato tecnico: ciò che è provato resta provato solo in simulazione e a sensore fermo, niente sull'hardware.

**Come ho verificato, e l'indipendenza.** **[g]** = dato trovato con una ricerca testuale nel testo grezzo scaricato oggi (pagina o PDF); **[m]** = metadati letti dal registro Crossref o dall'interfaccia di GitHub; **[r]** = letto solo attraverso lo strumento di lettura, che riassume con un modello ausiliario: più debole. Condivido con i ruoli che citano il modello linguistico; le verifiche [g] e [m] non passano da un riassunto e valgono anche contro quell'errore. Un 403 o una protezione contro i programmi automatici non li ho aggirati: ho cercato una copia ufficiale altrove, oppure ho scritto «non raggiungibile».

**Versioni.** Le pagine di PX4 citate sono quelle del ramo `main` della documentazione (oggi la versione stabile indicata dalla pagina è la v1.17): valgono come descrizione del comportamento attuale, non di una versione fissata. Il progetto non usa PX4: lo cita come analogia.

---

## A. Articoli scientifici e prestampe

### mandaokar2026
Tipo: articolo scientifico (prestampa)
Autori: Dnyandeep Mandaokar, Bernhard Rinner
Titolo: RADAR Perception for Dynamic Obstacle Avoidance onboard small-scale Quadrotor UAVs
Sede e anno: prestampa arXiv, v1 del 3 agosto 2026, v2 del 6 novembre 2026; «submitted for possible publication and is currently under review»; nessuna sede pubblicata
Identificativo: arXiv:2608.01855 (cs.RO); DOI 10.48550/arXiv.2608.01855
Link: https://arxiv.org/abs/2608.01855
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente [g, sul testo del PDF v2] — «Raspberry Pi 4B», «approximately 14 ms per RADAR frame», «a system latency of 75 ms from first detection to the avoidance command», «closing speeds up to 14.6 m/s», portante «77 GHz», «mean position errors of at most 0.15 m, 0.93 m, and 0.87 m in the x, y, and z directions». Il ruolo che la cita l'aveva aperta.
Usata per: radar a 77 GHz su quadrirotore; tracciatore su Raspberry Pi 4B; 75 ms fino al comando; avvicinamenti fino a 14,6 m/s; errori fino a 0,9 m — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §2(b), S16
Usata per: una catena radar con tracciatore gira su un Raspberry Pi 4B — stesso file, §2(f)
Usata per: tracciamento da piattaforma in moto con radar a bordo — stesso file, §3
Note: correzione 5: gli 0,93 m e 0,87 m sono errori *medi* di posizione sugli assi y e z, non «errori laterali fino a». È una prestampa non ancora passata da una revisione; 300 lanci di palle e 90 prove nel fumo, quindi non garantisce niente su persone o veicoli.

### orzechowski2018
Tipo: articolo scientifico
Autori: Piotr Franciszek Orzechowski, Annika Meyer, Martin Lauer
Titolo: Tackling Occlusions & Limited Sensor Range with Set-based Safety Verification
Sede e anno: 2018 21st International Conference on Intelligent Transportation Systems (ITSC), pp. 1729–1736, novembre 2018
Identificativo: DOI 10.1109/ITSC.2018.8569332; arXiv:1807.01262
Link: https://arxiv.org/abs/1807.01262
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente [r per la pagina arXiv; m per sede, pagine e DOI]. Già verificata dal curatore in `f3/fonti/FONTI_VERIFICATE.md` («ostacoli nascosti sovrastimati con intervalli di stato: sì»).
Usata per: lo strato 1 viene dalla guida automatica: ostacoli nascosti ai bordi del campo visivo, con stati sovrastimati per intervalli — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §3, S32
Note: garantisce che l'idea ha un precedente in letteratura; non garantisce niente sul nucleo, che è un'altra realizzazione.

### koschi2021
Tipo: articolo scientifico (o tesi: identificazione incerta)
Autori: non verificato per il documento citato; probabile Markus Koschi (tesi) o Markus Koschi, Matthias Althoff (articolo)
Titolo: non verificato per il documento citato. Titolo probabile, dal riassunto di un motore di ricerca: «Set-based Prediction of Traffic Participants and its Applications to Safe Motion Planning» (tesi di dottorato, Technische Universität München, 2021)
Sede e anno: non verificato
Identificativo: mediaTUM, documento 1575368
Link: https://mediatum.ub.tum.de/doc/1575368/1575368.pdf
Verifica: non raggiungibile — il sito risponde con una pagina di protezione contro i programmi automatici (Anubis), sia sul PDF sia sulla scheda. Vista solo nel riassunto di un motore di ricerca, come già dal ruolo che la cita.
Usata per: oggetti fantasma fuori dall'area osservata, come precedente dello strato 1 — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §3, S33
Note: l'articolo di rivista collegato esiste e l'ho verificato sul registro Crossref [m]: Markus Koschi, Matthias Althoff, «Set-Based Prediction of Traffic Participants Considering Occlusions and Traffic Rules», IEEE Transactions on Intelligent Vehicles 6(2), pp. 249–265, giugno 2021, DOI 10.1109/TIV.2020.3017385. Se serve una citazione sicura conviene usare questa, dopo averne letto il testo (non letto oggi).

### nuss2018
Tipo: articolo scientifico
Autori: Dominik Nuss, Stephan Reuter, Markus Thom, Ting Yuan, Gunther Krehl, Michael Maile, Axel Gern, Klaus Dietmayer
Titolo: A Random Finite Set Approach for Dynamic Occupancy Grid Maps with Real-Time Application
Sede e anno: The International Journal of Robotics Research 37(8), pp. 841–866, luglio 2018 (prestampa arXiv del 9 maggio 2016, v2 del 10 settembre 2016)
Identificativo: DOI 10.1177/0278364918775523; arXiv:1605.02406
Link: https://arxiv.org/abs/1605.02406
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente [r per arXiv; m per rivista, volume, pagine, riassunto]. Già verificata dal curatore in `f3/fonti/FONTI_VERIFICATE.md`.
Usata per: griglie dinamiche d'occupazione come riferimento di ricerca — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §3, S34
Note: dati laser e radar da veicolo stradale; non riguarda camere di profondità.

### aharon2022
Tipo: articolo scientifico (prestampa)
Autori: Nir Aharon, Roy Orfaig, Ben-Zion Bobrovsky
Titolo: BoT-SORT: Robust Associations Multi-Pedestrian Tracking
Sede e anno: prestampa arXiv, v1 del 29 giugno 2022, v2 del 7 luglio 2022; la pagina non indica una sede pubblicata
Identificativo: arXiv:2206.14651; DOI 10.48550/arXiv.2206.14651
Link: https://arxiv.org/abs/2206.14651
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente [r] — nel riassunto: «camera-motion compensation, and a more accurate Kalman filter state vector». Il ruolo che la cita l'aveva aperta.
Usata per: compensazione del moto della camera nel filtro di tracciamento — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §3, S35
Note: la compensazione è nel piano dell'immagine e si misura sull'identità dei pedoni; non dà garanzie su «mai libero dove non è osservato».

### shan2022
Tipo: articolo scientifico (prestampa)
Autori: Mao Shan, Karan Narula, Stewart Worrall, Yung Fei Wong, Julie Stephany Berrio Perez, Paul Gray, Eduardo Nebot
Titolo: A Novel Probabilistic V2X Data Fusion Framework for Cooperative Perception
Sede e anno: prestampa arXiv, una sola versione del 31 marzo 2022; sede pubblicata: non indicata nella pagina, non verificata
Identificativo: arXiv:2203.16964; DOI 10.48550/arXiv.2203.16964
Link: https://arxiv.org/pdf/2203.16964
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente [g, sul testo del PDF] — «the covariance intersection (CI) algorithm [8]», «fusing tracks information from two or more sources without knowing the cross-correlation information between them». Il riassunto non nomina il metodo, dice solo «considers the presence of cross-correlation». Il ruolo che la cita l'aveva vista solo in un risultato di ricerca.
Usata per: scambio di tracce fra veicoli con correlazioni ignote: intersezione delle covarianze — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §5, S36
Usata per: fusione prudente fra più veicoli (tappa 3 degli sviluppi) — `f6-specializzazione/01-esperto-dominio/SPECIALIZZAZIONE.md` §5
Note: correzione 14: è un'applicazione del metodo, non la sua fonte originale (il suo riferimento [8], non verificato da me).

### liu2022
Tipo: articolo scientifico
Autori: Shuai Liu, Xin Li, Huchuan Lu, You He
Titolo: Multi-Object Tracking Meets Moving UAV
Sede e anno: 2022 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), giugno 2022; pagine 8876–8885 secondo la CVF e mlanthology, 8866–8875 secondo Crossref
Identificativo: DOI 10.1109/CVPR52688.2022.00867
Link: https://mlanthology.org/cvpr/2022/liu2022cvpr-multiobject (testo: https://openaccess.thecvf.com/content/CVPR2022/html/Liu_Multi-Object_Tracking_Meets_Moving_UAV_CVPR_2022_paper.html)
Verifica: dato diverso: l'articolo esiste con questi autori e titolo [m, g], ma nel testo intero la parola «occlusion» non compare (0 occorrenze di «occlu» nel PDF della CVF); c'è «irregular motion caused by moving camera and view change in 3D directions» [g]. Il ruolo che la cita l'aveva vista solo in un risultato di ricerca.
Usata per: i lavori sul tracciamento da drone nominano insieme occlusione e moto irregolare della camera — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §2(d), S21
Usata per: tracciatori per drone, fra i riferimenti di ricerca — stesso file, §3
Note: correzione 1. Sostiene «moto irregolare della camera», non «occlusione». Discordanza sulle pagine non risolta: la deciderebbe la scheda dell'IEEE.

### dang2024
Tipo: articolo scientifico
Autori: Zhaoyang Dang, Xiaoyong Sun, Bei Sun, Runze Guo, Can Li
Titolo: OMCTrack: Integrating Occlusion Perception and Motion Compensation for UAV Multi-Object Tracking
Sede e anno: Drones 8(9), articolo 480, 12 settembre 2024 (MDPI)
Identificativo: DOI 10.3390/drones8090480
Link: https://mdpi.com/2504-446X/8/9/480
Verifica: verificata dal curatore il 14-11-2026 in parte: la pagina dell'editore non è raggiungibile (403, come già al ruolo che la cita); autori, titolo, rivista e riassunto letti nel registro Crossref [m]. Nel riassunto: «occlusion perception module» e «adaptive motion compensation module … to handle the UAV's complex movements». Il testo intero non è stato letto.
Usata per: i lavori sul tracciamento da drone nominano insieme occlusione e moto irregolare della camera — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §2(d), S22
Usata per: tracciatori per drone, fra i riferimenti di ricerca — stesso file, §3
Note: è questa, non `liu2022`, la fonte che regge la frase su occlusione e moto insieme. Misurato su VisDrone2019 e UAVDT, nel piano dell'immagine.

### delmerico2018
Tipo: articolo scientifico
Autori: Jeffrey Delmerico, Davide Scaramuzza
Titolo: A Benchmark Comparison of Monocular Visual-Inertial Odometry Algorithms for Flying Robots
Sede e anno: 2018 IEEE International Conference on Robotics and Automation (ICRA), pp. 2502–2509, maggio 2018
Identificativo: DOI 10.1109/ICRA.2018.8460664
Link: https://rpg.ifi.uzh.ch/docs/ICRA18_Delmerico.pdf
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente [g sul testo estratto dal PDF per titolo, autori e riassunto; m per sede, pagine e DOI]. I due ruoli che la citano non erano riusciti a leggerla.
Usata per: «confronto di riferimento» sulla qualità del moto proprio, citato come non letto; nessuna cifra presa — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §2(a), S13
Usata per: lo stesso, «non si è lasciato leggere»; le cifre d'errore delle sorgenti restano ipotesi — `f6-specializzazione/02-slam/MOTO_PROPRIO.md` §2
Note: confronta sei catene di odometria visuale-inerziale monoculare (MSCKF, OKVIS, ROVIO, VINS-Mono, SVO+MSF, SVO+GTSAM) su calcolatori di bordo. Non contiene gli errori relativi su 1–2 s che servirebbero al bilancio della posa: le cifre di `MOTO_PROPRIO.md` restano ipotesi del ruolo.

### rossi2025
Tipo: articolo scientifico (citato come prestampa; ora pubblicato)
Autori: Pierluigi Rossi, Elisa Cioccolo, Maurizio Cutini, Danilo Monarca, Daniele Puri, Davide Gattamelata, Leonardo Vita
Titolo: Outdoor Characterization and Geometry-Aware Error Modelling of an RGB-D Stereo Camera for Safety-Related Obstacle Detection
Sede e anno: prestampa su Preprints.org, 7 novembre 2025; poi Sensors 25(24), articolo 7495, 9 dicembre 2025 (MDPI)
Identificativo: DOI 10.20944/preprints202511.0498.v1 (prestampa); DOI 10.3390/s25247495 (articolo)
Link: https://www.preprints.org/manuscript/202511.0498
Verifica: dato diverso: la pagina non è raggiungibile (403); autori, titolo, date e riassunto letti nel registro Crossref [m], che dichiara la prestampa «is-preprint-of» dell'articolo su Sensors. Nel riassunto «prestazioni imprevedibili» non c'è: c'è che le prestazioni all'aperto a media e lunga distanza restano «weakly quantified», con prove fra 4 e 16 m su una D455 e un modello che predice l'errore di profondità con RMSE 0,46–0,64 m e MAE 0,40–0,51 m. Il ruolo che la cita l'aveva vista solo in un risultato di ricerca.
Usata per: stereo attiva (D455) all'aperto con luce forte: «un preprint del 2025 trova prestazioni imprevedibili» — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §2(b), S14
Note: correzione 6. Da citare come articolo su Sensors. La parola «imprevedibili» resta non verificata finché qualcuno non legge il testo intero; il riassunto sostiene un'affermazione più debole e più utile: errori dell'ordine del mezzo metro fra 4 e 16 m, cioè oltre la zona del nucleo (fino a 3 m).

### vogiatzoglou2024
Tipo: altro (contributo in un blog accademico: fonte secondaria)
Autori: Plixavra Vogiatzoglou
Titolo: The AI Act National Security Exception: room for manoeuvres?
Sede e anno: Verfassungsblog, 9 dicembre 2024 (nel dibattito «The EU AI Act's Impact on Security Law»)
Identificativo: manca (DOI non cercato)
Link: https://verfassungsblog.de/the-ai-act-national-security-exception/
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente [g] — la citazione «exclusively for military, defence or national security purposes» c'è; c'è anche «if the same AI system is also used for law enforcement and public security purposes, then it must abide by» il regolamento. Il ruolo che la cita l'aveva vista solo in un risultato di ricerca.
Usata per: il regolamento sull'intelligenza artificiale esclude i sistemi a uso esclusivamente militare, di difesa o di sicurezza nazionale; il duplice uso resta dentro — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §6, S38
Note: correzione 11. Per i limiti della scheda del curatore un blog non è fonte primaria: la primaria è `ue-2024-1689`. L'espressione «duplice uso» è una lettura del ruolo, non una parola del testo.

## B. La società promotrice: sito e stampa

Avvertenza comune, già scritta nel quadro: le notizie derivano tutte dai comunicati della società; più testate non sono più prove.

### maregroup-sito
Tipo: pagina di costruttore o comunicato
Autori: Mare Group S.p.A.
Titolo: Mare Group — Ingegneria ad alta tecnologia (pagina iniziale)
Sede e anno: sito della società, letto il 14-11-2026
Identificativo: manca
Link: https://www.maregroup.it/
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente [g] — «Ingegneria ad alta tecnologia per progettare, sviluppare e produrre sistemi complessi», «quotata sul mercato Euronext Growth Milan», i tre settori, «Product Design & Digital Twin». Aperta anche dal ruolo che la cita.
Usata per: profilo della società (settori, quotazione, linee tecnologiche) — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §1, S1
Note: pagina che cambia nel tempo; non ha una data di revisione.

### maregroup-ordine-uncrewed-2026
Tipo: pagina di costruttore o comunicato
Autori: Mare Group S.p.A.
Titolo: Primo ordine da cliente estero da 1,7 milioni di euro per sistemi uncrewed
Sede e anno: sito della società, notizia del 21-10-2026
Identificativo: manca
Link: https://www.maregroup.it/news/primo-ordine-estero-sistemi-uncrewed
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente [g] — titolo, data, «del valore di circa 1,7 milioni di euro». Questa pagina non nomina CTMAVIO né il 2026 come anno d'esecuzione: stanno nelle tre voci seguenti. Aperta anche dal ruolo che la cita.
Usata per: ordine del 21-10-2026 da 1,7 milioni per «sistemi uncrewed»; cliente, piattaforma e uso non verificati — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` in testa e §1, S2
Note: correzione 12. La pagina rimanda a un comunicato integrale che non ho aperto: è il documento che deciderebbe il tipo di piattaforma (non risolto nel quadro).

### teleborsa-ordine-uncrewed-2026
Tipo: pagina di costruttore o comunicato (agenzia di stampa, ripresa da Borsa Italiana)
Autori: Teleborsa
Titolo: Mare Group, primo ordine da un cliente estero per sistemi uncrewed da 1,7 milioni di euro
Sede e anno: Borsa Italiana, notizie Teleborsa, 21-10-2026
Identificativo: manca
Link: https://www.borsaitaliana.it/borsa/notizie/teleborsa/finanza/mare-group-primo-ordine-da-un-cliente-estero-per-sistemi-uncrewed-da-17-milioni-di-euro-21_2026-10-21_TLB.html?lang=it
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente [g] — «attraverso la controllata CTMAVIO», «circa 1,7 milioni di euro, da un cliente estero, da concludersi prevalentemente nel 2026». Aperta anche dal ruolo che la cita.
Usata per: l'ordine è preso tramite CTMAVIO ed è da eseguire per lo più nel 2026 — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §1, S3
Note: deriva dal comunicato della società.

### soldionline-ordine-uncrewed-2026
Tipo: pagina di costruttore o comunicato (stampa finanziaria)
Autori: SoldiOnline (firma non rilevata)
Titolo: Mare Group, primo ordine estero per sistemi uncrewed (titolo dell'indirizzo; il titolo esatto della pagina non è stato trascritto)
Sede e anno: soldionline.it, ottobre 2026
Identificativo: manca
Link: https://www.soldionline.it/notizie/azioni-italia/mare-group-primo-ordine-estero-sistemi-uncrewed
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente [g] — «circa 1,7 milioni di euro e sarà eseguito prevalentemente nel 2026», «componenti e strutture di precisione per applicazioni aeronautiche, motoristiche e UAV». Aperta anche dal ruolo che la cita.
Usata per: la stampa lega l'ordine a componenti e strutture per usi aeronautici, motoristici e UAV — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §1, S4
Note: deriva dal comunicato della società.

### websim-ordine-uncrewed-2026
Tipo: pagina di costruttore o comunicato (stampa finanziaria)
Autori: Websim, redazione
Titolo: Mare Group - Nuovo ordine da 1,7 milioni di euro
Sede e anno: websim.it, 21-10-2026, ore 10:30
Identificativo: manca
Link: https://www.websim.it/azioni/small-mid-cap/notizie/mare-group-nuovo-ordine-da-1-7-milioni-di-euro/
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente [g] — «tramite la controllata CTMAVIO S.r.l., il primo ordine da un cliente estero per la fornitura di sistemi uncrewed, per un valore di circa 1,7 milioni di euro». Aperta anche dal ruolo che la cita.
Usata per: conferma dell'ordine del 21-10-2026 — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §1, S5
Note: deriva dal comunicato della società.

### teleborsa-commessa-rpas-2026
Tipo: pagina di costruttore o comunicato (agenzia di stampa)
Autori: Teleborsa
Titolo: Mare Group, prima commessa per velivoli a pilotaggio remoto: valore superiore a 1 milione di euro
Sede e anno: teleborsa.it, 5 giugno 2026
Identificativo: manca
Link: https://www.teleborsa.it/News/2026/06/05/mare-group-prima-commessa-per-velivoli-a-pilotaggio-remoto-valore-superiore-a-1-milione-di-euro-53.html
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente [g] — «circa 1,05 milioni di euro», «velivoli a pilotaggio remoto (RPAS) di dimensioni medio-grandi», «ingegneria di sistema e lo sviluppo di sottosistemi di bordo critici per la sicurezza». Aperta anche dal ruolo che la cita.
Usata per: prime commesse del 05-06-2026 (circa 1,05 milioni) su un velivolo a pilotaggio remoto medio-grande — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §1, S6
Note: deriva dal comunicato della società.

### teleborsa-nido-2026
Tipo: pagina di costruttore o comunicato (agenzia di stampa)
Autori: Teleborsa
Titolo: Mare Group entra nel capitale di NIDO al 20% con opzione per il controllo entro 24 mesi
Sede e anno: teleborsa.it, 9 giugno 2026
Identificativo: manca
Link: https://www.teleborsa.it/News/2026/06/09/mare-group-entra-nel-capitale-di-nido-al-20percent-con-opzione-per-il-controllo-entro-24-mesi-5.html
Verifica: dato diverso: pagina aperta [g]; ci sono il 20 %, «il drone H815», ricarica, voli oltre la linea di vista, supervisione, «ispezione di strade e infrastrutture, monitoraggio strutturale di pipeline e reti energetiche… sorveglianza perimetrale», «architettura dual-use». Il «51 %» nella pagina non c'è: c'è «opzione per il controllo entro 24 mesi». Aperta anche dal ruolo che la cita.
Usata per: ingresso al 20 % in NIDO «con opzione per il 51 %»; descrizione della piattaforma NIDO e dei suoi usi — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §1, S7
Usata per: il profilo pubblico della società è un drone da ispezione con stazione di ricovero e supervisione remota — `f6-specializzazione/01-esperto-dominio/SPECIALIZZAZIONE.md` §2
Note: correzione 7: scrivere «opzione per il controllo», non «per il 51 %», salvo un'altra fonte.

### websim-task-force-x-2026
Tipo: pagina di costruttore o comunicato (stampa finanziaria)
Autori: Websim, redazione
Titolo: Mare Group - Scelta dalla NATO per la Task Force X
Sede e anno: websim.it, 10-07-2026, ore 14:36
Identificativo: manca
Link: https://www.websim.it/azioni/small-mid-cap/notizie/mare-group-scelta-dalla-nato-per-la-task-force-x/
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente [g] — «Task Force X – Central Mediterranean, un'iniziativa NATO a guida italiana in corso presso il Poligono di Torre Veneri», «sorveglianza continua e la protezione delle infrastrutture critiche», NIDO, GMSPAZIO, CTM Avio. Aperta anche dal ruolo che la cita.
Usata per: partecipazione del 10-07-2026 alla Task Force X — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §1, S8
Usata per: sorveglianza di perimetri e infrastrutture come profilo pubblico — `f6-specializzazione/01-esperto-dominio/SPECIALIZZAZIONE.md` §2
Note: deriva dal comunicato della società; il titolo «scelta dalla NATO» è della testata.

### teleborsa-ctmavio-2026
Tipo: pagina di costruttore o comunicato (agenzia di stampa)
Autori: Teleborsa
Titolo: Mare Group acquisisce CTMAVIO e rafforza la filiera dei droni per Aerospazio e Difesa
Sede e anno: teleborsa.it, 24 luglio 2026
Identificativo: manca
Link: https://www.teleborsa.it/News/2026/07/24/mare-group-acquisisce-ctmavio-e-rafforza-la-filiera-dei-droni-per-aerospazio-e-difesa-17.html
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente [g] — «Il corrispettivo per il 100% del capitale sociale di CTMAVIO è pari a 9 milioni», menzione del Golden Power. Aperta anche dal ruolo che la cita.
Usata per: accordo del 24-07-2026 per comprare CTMAVIO (9 milioni) — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §1, S9
Note: la chiusura dell'operazione resta non verificata, come nel quadro.

### maregroup-news
Tipo: pagina di costruttore o comunicato
Autori: Mare Group S.p.A.
Titolo: News (elenco delle notizie)
Sede e anno: sito della società, letto il 14-11-2026
Identificativo: manca
Link: https://www.maregroup.it/news/
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente [g] — «15-09-2026 Via libera "Golden Power" per l'acquisizione di CTMAVIO»; «21-10-2026 Primo ordine da cliente estero…». Nell'elenco non compaiono le parole «hackathon», «percezione», «visione artificiale». Aperta anche dal ruolo che la cita.
Usata per: via libera Golden Power del 15-09-2026 — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §1, S10
Usata per: «non trovate» linee terrestri o navali, prodotti di percezione, notizie pubbliche sull'hackathon — stesso file, §1
Usata per: il Golden Power su CTMAVIO dice che il settore è vigilato — stesso file, §6
Note: un'assenza in un elenco di titoli è una prova debole: vale per i titoli di oggi, non per il contenuto delle notizie.

### teleborsa-propulsione-uav-2026
Tipo: pagina di costruttore o comunicato (agenzia di stampa)
Autori: Teleborsa
Titolo: Mare Group, contratto da 8,3 milioni di euro per unità di propulsione UAV
Sede e anno: teleborsa.it, 28 luglio 2026
Identificativo: manca
Link: https://www.teleborsa.it/News/2026/07/28/mare-group-contratto-da-8-3-milioni-di-euro-per-unita-di-propulsione-uav-13.html
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente [g] — «8,3 milioni», «fornitura di oltre 6.000 … kit per velivoli senza pilota, con ricavi distribuiti in modo uniforme sui tre esercizi». Il ruolo che la cita l'aveva vista solo in un risultato di ricerca.
Usata per: accordo quadro del 28-07-2026 da 8,3 milioni, oltre 6.000 kit motore — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §1, S11
Note: deriva dal comunicato della società.

## C. Documentazione di software

### px4-ekf2
Tipo: documentazione di software
Autori: PX4 Autopilot (Dronecode)
Titolo: Using PX4's Navigation Filter (EKF2)
Sede e anno: PX4 Guide, ramo `main`, letta il 14-11-2026
Identificativo: manca
Link: https://docs.px4.io/main/en/advanced_config/tuning_the_ecl_ekf
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente [g] — «delta angle and delta velocity data at a minimum rate of 100Hz»; «The EKF uses the IMU data for state prediction only»; magnetometro ad almeno 5 Hz; quota da «GPS, barometric pressure, range finder, external vision»; «A complementary filter is used to propagate the states forward from the 'fusion time horizon' to current time». Aperta anche dai due ruoli che la citano.
Usata per: lo stimatore di stato fonde IMU (in predizione, almeno 100 Hz), magnetometro, GNSS, barometro, telemetro e visione esterna — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §2(a), S12
Usata per: lo stimatore lavora su un orizzonte ritardato e porta gli stati al presente con l'IMU — `f6-specializzazione/02-slam/MOTO_PROPRIO.md` §2(c)
Note: descrive l'architettura, non dà nessuna accuratezza. Ramo `main`, non una versione fissata.

### px4-collision-prevention
Tipo: documentazione di software
Autori: PX4 Autopilot (Dronecode)
Titolo: Collision Prevention
Sede e anno: PX4 Guide, ramo `main`, letta il 14-11-2026
Identificativo: manca
Link: https://docs.px4.io/main/en/computer_vision/collision_prevention
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente [g] — «If there is no sensor data in a particular direction, velocity in that direction is restricted to 0»; «for longer than 0.5s … force the velocity setpoints in xy to zero. After 5 seconds of not receiving any data, the vehicle will switch into HOLD mode»; «the region covered by this sensor will be treated as uncovered, meaning you will not be able to move there»; «a vehicle moving at 4 m/s with OBSTACLE_DISTANCE messages being emitted at 10Hz»; «tracking delay is typically between 0.1 and 0.5 seconds»; un sensore con campo orizzontale «of about 35 degrees». Aperta anche dal ruolo che la cita.
Usata per: telemetri a fascio come ingressi tipici; settori stretti (esempio: 35°) — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §2(b), S18
Usata per: prevenzione delle collisioni provata a 4 m/s, messaggi a 10 Hz, ritardi di 0,1–0,5 s — stesso file, §2(c)
Usata per: senza dati in una direzione la velocità è 0; oltre 0,5 s senza dati azzera i comandi orizzontali, dopo 5 s attesa; la regione di un sensore guasto è «treated as uncovered»: «sconosciuto non è libero» — stesso file, §2(e)
Usata per: gli 0,5 s della causa «collegamento», presi per analogia (per un collegamento: non verificato) — `f6-specializzazione/01-esperto-dominio/SPECIALIZZAZIONE.md` §3.2
Usata per: secondo aggancio per il giurato: gli autopiloti aperti azzerano la velocità verso i settori senza dati — `f6-specializzazione/01-esperto-dominio/SPECIALIZZAZIONE.md` §6; ripreso in `f6-specializzazione/03-avversario/ATTACCO_SPECIALIZZAZIONE.md` S5 («S18 con la frase citata»)
Note: lo «0,1–0,5 s» è il ritardo d'inseguimento della velocità del veicolo, non un ritardo di collegamento. La stessa pagina avverte che con il parametro `CP_GO_NO_DATA=1` il veicolo può muoversi anche dove non ha dati: il comportamento prudente è quello predefinito, non una garanzia. I «4 m/s» sono una prova iniziale del costruttore, non un limite.

### px4-obstacle-distance
Tipo: documentazione di software
Autori: PX4 Autopilot (Dronecode)
Titolo: ObstacleDistance (UORB message)
Sede e anno: PX4 Guide, ramo `main`, letta il 14-11-2026
Identificativo: manca
Link: https://docs.px4.io/main/en/msg_docs/ObstacleDistance
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente [g] — «A value of 0 means that the obstacle is right in front of the sensor. A value of max_distance +1 means no obstacle is present. A value of UINT16_MAX for unknown/not used. In a array element, one unit corresponds to 1cm.» Il ruolo che la cita l'aveva vista solo in un risultato di ricerca.
Usata per: l'interfaccia per settori: `UINT16_MAX` sconosciuto, `max_distance + 1` nessun ostacolo — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §2(e), S23
Usata per: il messaggio per settori a tre valori verso l'autopilota — `f6-specializzazione/01-esperto-dominio/SPECIALIZZAZIONE.md` §3.1
Usata per: «S23 solo da risultato di ricerca» nel giudizio sul secondo aggancio — `f6-specializzazione/03-avversario/ATTACCO_SPECIALIZZAZIONE.md` S5
Note: con la verifica di oggi cade la riserva dell'avversario su S23 («non riverificabile in rete»): i tre valori ci sono, alla lettera. Resta vero che il prototipo non ha mai generato questo messaggio. La pagina descrive il messaggio interno di PX4; il messaggio MAVLink con lo stesso nome non è stato aperto.

### px4-safety
Tipo: documentazione di software
Autori: PX4 Autopilot (Dronecode)
Titolo: Safety Configuration (Failsafes)
Sede e anno: PX4 Guide, ramo `main`, letta il 14-11-2026
Identificativo: manca
Link: https://docs.px4.io/main/en/config/safety
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente [g] — «The Data Link Loss failsafe is triggered if the connection to the last MAVLink ground station … is lost»; tempo `COM_DL_LOSS_T`; azione `NAV_DLL_ACT`: «Disabled, Hold mode, Return mode, Land mode, Disarm, Terminate». Il ruolo che la cita l'aveva vista solo in un risultato di ricerca.
Usata per: la perdita del collegamento ha un'azione configurata — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §2(e), S25
Usata per: alla perdita del collegamento, a bordo decide l'azione già configurata nell'autopilota — `f6-specializzazione/01-esperto-dominio/SPECIALIZZAZIONE.md` §3.2
Note: la pagina non dà un valore predefinito in secondi nel passo letto: gli 0,5 s del progetto non vengono da qui.

### px4-vehicle-odometry
Tipo: documentazione di software
Autori: PX4 Autopilot (Dronecode)
Titolo: VehicleOdometry (UORB message)
Sede e anno: PX4 Guide, ramo `main`, letta il 14-11-2026
Identificativo: manca
Link: https://docs.px4.io/main/en/msg_docs/VehicleOdometry
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente [g] — campi `timestamp_sample`, `position_variance`, `orientation_variance`, `velocity_variance`, `reset_counter` («Counts reset events on attitude, velocity and position»). Aperta anche dal ruolo che la cita.
Usata per: il messaggio d'odometria porta marca temporale, varianze e contatore dei salti; la pagina non dà alcuna accuratezza — `f6-specializzazione/02-slam/MOTO_PROPRIO.md` §2(c)
Note: confermo che la pagina non contiene cifre d'accuratezza: l'errore di 0,1 m/s usato nel conto resta un'ipotesi del ruolo.

### nvidia-cuvslam
Tipo: documentazione di software
Autori: NVIDIA (Isaac ROS)
Titolo: cuVSLAM (Concepts, Visual SLAM)
Sede e anno: documentazione di Isaac ROS, versione «latest», letta il 14-11-2026
Identificativo: manca
Link: https://nvidia-isaac-ros.github.io/concepts/visual_slam/cuvslam/index.html
Verifica: verificata dal curatore il 14-11-2026 in parte: pagina aperta [g]; c'è «cuVSLAM is a GPU-accelerated library for stereo-visual-inertial SLAM and odometry». La licenza e il «pacchetto Python non commerciale» nella pagina non compaiono: non verificati. Il ruolo che la cita l'aveva vista solo in un risultato di ricerca.
Usata per: cuVSLAM: stereo più IMU, su GPU; licenza «non confermata»; pacchetto Python non commerciale — `f6-specializzazione/02-slam/MOTO_PROPRIO.md` §2(b)
Note: correzione 13. Per la licenza serve la pagina delle licenze del progetto o il deposito del pacchetto: non aperti.

## D. Schede tecniche e pagine dei costruttori

### intel-bkm-d400
Tipo: scheda tecnica (nota applicativa del costruttore)
Autori: Anders Grunnet-Jepsen, John N. Sweetser, John Woodfill (dal riassunto di un motore di ricerca: non verificato)
Titolo: Best-Known-Methods for Tuning Intel RealSense D400 Depth Cameras for Best Performance
Sede e anno: Intel, revisione 1.9 (dal riassunto di un motore di ricerca: non verificato)
Identificativo: manca
Link: https://forums.intel.com/cipcp26785/attachments/cipcp26785/feeditem_no_topic/6364/1/BKMs_Tuning_RealSense_D4xx_Cam.pdf
Verifica: non raggiungibile — oggi il link risponde 404, e la pagina di Intel che ospita lo stesso documento risponde 403. Vista solo nel riassunto di un motore di ricerca, come già dal ruolo che la cita.
Usata per: stereo attiva: errore crescente con z² — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §2(b), S14
Note: l'affermazione sul quadrato della distanza l'ho trovata oggi [g] nella versione in rete della stessa guida, sul sito attuale del marchio (https://dev.realsenseai.com/docs/tuning-depth-cameras-for-best-performance): «The depth error scales as the square of the distance away». Conviene sostituire il link.

### realsense-confronto-camere
Tipo: pagina di costruttore o comunicato
Autori: RealSense
Titolo: Compare Depth Cameras (tabella di confronto delle camere di profondità)
Sede e anno: sito del costruttore, letto il 14-11-2026
Identificativo: manca
Link: https://www.realsenseai.com/compare-depth-cameras/
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente [g] — riga «Ideal Range»: «.6 m to 6 m»; riga «Depth Accuracy»: «<2% at 4 m»; l'attribuzione delle colonne alla D455 non è leggibile dal testo grezzo e viene dalla verifica di f3. Già verificata dal curatore in `f3/fonti/FONTI_VERIFICATE.md` (voce 4).
Usata per: D455: campo ideale 0,6–6 m; errore < 2 % a 4 m — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §2(b) (lì attribuita a S14)
Note: voce aggiunta da me: i quattro file non citano questo link, ma è qui che stanno le due cifre che il quadro attribuisce a S14. Sono valori di catalogo, non misure nelle condizioni del progetto.

### livox-mid-360
Tipo: scheda tecnica
Autori: Livox
Titolo: Mid-360, Specs
Sede e anno: sito del costruttore, letto il 14-11-2026
Identificativo: manca
Link: https://www.livoxtech.com/mid-360/specs
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente [g] — «Detection Range (@ 100 klx) 40 m @ 10% reflectivity, 70 m @ 80% reflectivity»; «Close Proximity Blind Zone 0.1 m»; «FOV Horizontal: 360°, Vertical: -7°~52°» (59° in tutto); «Frame Rate 10 Hz (typical)»; «Power 6.5 W (average)»; «Weight 265 g». Aperta anche dal ruolo che la cita.
Usata per: LiDAR a stato solido: portata, campo, 10 Hz, 265 g, 6,5 W, zona cieca 0,1 m — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §2(b), S15
Usata per: alla scala reale un LiDAR da 10–40 m, da provare — `f6-specializzazione/01-esperto-dominio/SPECIALIZZAZIONE.md` §1
Note: la stessa pagina dà la precisione radiale: ≤ 2 cm a 10 m e ≤ 3 cm a 0,2 m (1σ). `MOTO_PROPRIO.md` usa «3 cm radiali» come ipotesi senza citare la fonte: è coerente con la scheda, per eccesso. Vetro e pioggia: la scheda non li tratta.

### flir-boson
Tipo: pagina di costruttore o comunicato
Autori: Teledyne FLIR
Titolo: Boson (modulo termico a onda lunga)
Sede e anno: sito del costruttore, letto il 14-11-2026
Identificativo: manca
Link: https://www.oem.flir.com/products/boson/
Verifica: verificata dal curatore il 14-11-2026 in parte: pagina aperta [g]; ci sono «starting at 7.5 grams and <4.9 cm³», «Low power consumption, starting at 600 mW», «640 and 320 resolutions». Il valore «1 W» non c'è. Il ruolo che la cita l'aveva vista solo in un risultato di ricerca.
Usata per: termico (Boson 640): nucleo da 7,5 g, circa 0,6–1 W; dà la direzione, non la distanza — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §2(b), S17
Note: correzione 8. I 7,5 g e i 600 mW sono i valori minimi della famiglia («starting at»), non per forza quelli del modello 640.

### nvidia-jetson-orin-nano
Tipo: pagina di costruttore o comunicato (pagina di un rivenditore)
Autori: Kiwi Electronics (rivenditore)
Titolo: NVIDIA Jetson Orin Nano Super Developer Kit
Sede e anno: sito del rivenditore, letto il 14-11-2026
Identificativo: manca
Link: https://www.kiwi-electronics.com/en/single-board-computers-390/nvidia-jetson-orin-nano-super-developer-kit-11461
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente [g] — «Flexible power modes: 7W, 15W, 25W, and MAXN-Super». Il ruolo che la cita l'aveva vista solo in un risultato di ricerca.
Usata per: una Jetson Orin Nano lavora a 7, 15 o 25 W — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §2(f), S26
Note: è la pagina di un rivenditore, non del costruttore: per un documento destinato alla giuria conviene la scheda di NVIDIA (non aperta).

### intel-t265-fine-produzione
Tipo: pagina di costruttore o comunicato
Autori: Intel
Titolo: manca (articolo di supporto 000087450)
Sede e anno: sito di supporto di Intel; data non verificata
Identificativo: articolo 000087450
Link: https://intel.com/content/www/us/en/support/articles/000087450/emerging-technologies/intel-realsense-technology.html
Verifica: non raggiungibile — oggi il link rimanda (301) a una pagina d'errore di Intel; con una richiesta diretta risponde 403. Vista solo nel riassunto di un motore di ricerca, come già dal ruolo che la cita.
Usata per: il modulo T265 è fuori produzione dal 2022 e il costruttore indica D455 o D435i «with 3rd Party SLAM SW» — `f6-specializzazione/02-slam/MOTO_PROPRIO.md` §2(b)
Note: correzione 13. L'anno e la frase fra «» restano non verificati; serve un'altra fonte del costruttore.

## E. Norme e documenti regolatori

### easa-faq-open-category
Tipo: norma o documento regolatorio (pagina di domande e risposte dell'autorità)
Autori: Agenzia dell'Unione europea per la sicurezza aerea (EASA)
Titolo: FAQ, Open Category
Sede e anno: sito dell'EASA, letto il 14-11-2026
Identificativo: manca
Link: https://www.easa.europa.eu/en/the-agency/faqs/open-category
Verifica: dato diverso: pagina aperta [g]; ci sono «MTOM … less than 250 g and the maximum speed is less than 19 m/s» e «drones with a speed higher than 19 m/s are only allowed to operate in open subcategory A3»; per la C2 c'è la «low-speed function» senza cifra. I «3 m/s» nella pagina non ci sono: stanno in `ue-2019-945`. Il ruolo che la cita aveva letto le cifre «in guide secondarie».
Usata per: 19 m/s tetto delle classi C0 e C1 della categoria aperta; 3 m/s modo lento della C2 — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §2(c), S19
Usata per: v_max del piccolo drone fino a 19 m/s — stesso file, §2(c); e `f6-specializzazione/01-esperto-dominio/SPECIALIZZAZIONE.md` §1 e §3.3 (fascia di 2,5 m e 3,8 m)
Note: correzione 4. Le cifre sono giuste, la fonte primaria è il regolamento.

### ue-2019-945
Tipo: norma o documento regolatorio
Autori: Commissione europea
Titolo: Regolamento delegato (UE) 2019/945 relativo ai sistemi aeromobili senza equipaggio e agli operatori di paesi terzi di sistemi aeromobili senza equipaggio
Sede e anno: Gazzetta ufficiale dell'Unione europea, 2019; allegato, parti 1–3
Identificativo: regolamento delegato (UE) 2019/945
Link: https://www.legislation.gov.uk/eur/2019/945/annex (copia britannica, non ufficiale per l'Unione; EUR-Lex oggi non raggiungibile)
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente [g, sulla copia britannica] — parte 1 e parte 2: «have a maximum speed in level flight of 19 m/s»; parte 3, punto 9: «be equipped with a low-speed mode selectable by the remote pilot and limiting the ground speed to no more than 3 m/s». Non citata con un link dai ruoli: è la fonte primaria delle cifre di S19.
Usata per: 19 m/s (classi C0 e C1) e 3 m/s (modo lento della C2) — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §2(c) (lì attribuite a S19)
Usata per: fra i regolamenti del quadro europeo sui droni — stesso file, §3
Note: la copia britannica è il testo «conservato» dopo l'uscita dall'Unione ed è stata emendata nel Regno Unito (la pagina cita un atto del 2025): le tre frasi vanno riconfermate sul testo consolidato dell'Unione prima di un uso formale. Il titolo italiano qui sopra è una mia resa, non trascritto dalla Gazzetta.

### ue-2019-947
Tipo: norma o documento regolatorio
Autori: Commissione europea
Titolo: Regolamento di esecuzione (UE) 2019/947 relativo a norme e procedure per l'esercizio di aeromobili senza equipaggio
Sede e anno: Gazzetta ufficiale dell'Unione europea, 2019
Identificativo: regolamento di esecuzione (UE) 2019/947
Link: manca nei file (citato tramite S28 e S24)
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente, per la sola esistenza e il ruolo [g] — l'intestazione di S24 è «AMC & GM to Regulation (EU) 2019/947 — Issue 1, Amendment 3» e la pagina dell'EASA dice che le regole per i droni civili stanno «in EU Regulations 2019/947 and 2019/945». Il testo del regolamento non è stato aperto.
Usata per: quadro europeo sui droni — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §3 e §6 («le regole europee valgono per chi vola davvero»)
Note: nessuna cifra del progetto viene da qui. Il titolo italiano è una mia resa.

### easa-drones-regole
Tipo: norma o documento regolatorio (pagina dell'autorità)
Autori: EASA
Titolo: Drones & Air Mobility, Rules & Standards
Sede e anno: sito dell'EASA, letto il 14-11-2026
Identificativo: manca
Link: https://www.easa.europa.eu/domains/drones-air-mobility/rules-standards
Verifica: verificata dal curatore il 14-11-2026 in parte: pagina aperta [g]; nomina i regolamenti 2019/947 e 2019/945. Non nomina il 2021/664 né la decisione 2025/018/R. Il ruolo che la cita l'aveva vista solo in un risultato di ricerca.
Usata per: quadro europeo: regolamenti 2019/947 e 2019/945, U-space 2021/664, SORA 2.5 nella decisione 2025/018/R — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §3, S28
Usata per: le regole europee valgono per chi vola davvero — stesso file, §6
Note: correzione 9.

### ue-2021-664
Tipo: norma o documento regolatorio
Autori: Commissione europea
Titolo: Regolamento di esecuzione (UE) 2021/664 (quadro normativo per lo U-space)
Sede e anno: Gazzetta ufficiale dell'Unione europea, 2021; il link punta alla versione consolidata del 22-02-2026
Identificativo: regolamento di esecuzione (UE) 2021/664
Link: https://eur-lex.europa.eu/eli/reg_impl/2021/664/2026-02-22/eng/pdf
Verifica: non raggiungibile — EUR-Lex oggi risponde senza contenuto alle richieste automatiche (codice 202), sia in lettura diretta sia con lo strumento di lettura. Vista solo nel riassunto di un motore di ricerca, come già dal ruolo che la cita.
Usata per: quadro europeo: U-space — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §3, S28
Note: nessuna cifra del progetto ne dipende. Il titolo fra parentesi è una mia descrizione, non il titolo ufficiale.

### easa-amc-gm-2019-947
Tipo: norma o documento regolatorio
Autori: EASA
Titolo: Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 — Issue 1, Amendment 3 (allegato alla decisione ED 2025/018/R)
Sede e anno: EASA, 2025; 204 pagine
Identificativo: Annex to ED Decision 2025/018/R
Link: https://www.easa.europa.eu/sites/default/files/dfu/annex_to_ed_decision_2025-018-r_1_2.pdf
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente [g, sul testo del PDF] — «Detect and avoid — DAA — The capability to see, sense or detect conflicting traffic or other hazards and take the appropriate action…»; «TMPRs address the functions of detect, decide, command, execute and feedback loop»; «identify the modes of deterioration of the 'external systems' (e.g. complete loss of GNSS, GDOP/PDOP, latency issues, etc.)»; «SC-228 and/or EUROCAE WG-105»; «Specific Operations Risk Assessment (SORA) (Source: JARUS SORA v2.5)». Aperta anche dal ruolo che la cita.
Usata per: l'EASA chiede di individuare i modi di deterioramento dei sistemi esterni e i mezzi per rilevarli — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §2(e), S24
Usata per: definizione di «detect and avoid» e le sue cinque funzioni; rinvio a RTCA SC-228 ed EUROCAE WG-105; SORA 2.5 — stesso file, §3
Usata per: «detect and avoid» nelle norme è il traffico con equipaggio: da non dire per il prototipo — `f6-specializzazione/01-esperto-dominio/SPECIALIZZAZIONE.md` §6
Note: la definizione è alla voce I.53 del glossario e coincide parola per parola con la citazione del quadro, compresa la chiusa «to comply with the acceptable rules of flight». Il documento riguarda la categoria «specifica» dei droni: il prototipo non è un'operazione di volo, quindi vale come vocabolario, non come requisito applicabile.

### rtca-do-365
Tipo: norma o documento regolatorio (scheda di un catalogo di norme)
Autori: RTCA
Titolo: DO-365C — Minimum Operational Performance Standards (MOPS) for Detect and Avoid (DAA) Systems
Sede e anno: RTCA, 15 settembre 2022; 840 pagine (dalla scheda del catalogo)
Identificativo: RTCA DO-365C
Link: https://standards.globalspec.com/std/14562761/do-365c
Verifica: verificata dal curatore il 14-11-2026 in parte: scheda aperta [g]; titolo, ente, data e stato («active, Most Current») ci sono. Le cifre «35 s» e «oltre un chilometro» nella scheda non ci sono: non verificate. Il ruolo che la cita l'aveva vista solo in un risultato di ricerca.
Usata per: il «restare ben distanti» dal traffico con equipaggio ragiona su 35 s e oltre un chilometro: un'altra scala — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §2(c), S20
Usata per: norme tecniche sul «detect and avoid» — stesso file, §3
Note: correzione 2. La norma è a pagamento: la scheda garantisce che esiste e di che cosa tratta, non il contenuto. Le due cifre non vanno scritte in un documento per la giuria finché non hanno una fonte aperta.

### eurocae-ed-275
Tipo: norma o documento regolatorio (scheda di un catalogo di norme)
Autori: EUROCAE
Titolo: ED-275 — Minimum Operational Performance Standards for Airborne Collision Avoidance System Xu (ACAS Xu), Volume I e Volume II (Algorithm Design Description)
Sede e anno: EUROCAE, 1 dicembre 2020; 1.810 pagine (dalla scheda del catalogo)
Identificativo: EUROCAE ED-275
Link: https://standards.globalspec.com/std/14356966/eurocae-ed-275
Verifica: dato diverso: scheda aperta [g]; ED-275 è la norma del sistema anticollisione ACAS Xu, non una norma generale sul «detect and avoid». Le cifre «35 s» e «oltre un chilometro» non ci sono. Il ruolo che la cita l'aveva vista solo in un risultato di ricerca.
Usata per: norme tecniche sul «detect and avoid», insieme a DO-365 — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §3, S20
Usata per: le cifre del «restare ben distanti» — stesso file, §2(c)
Note: correzione 2. Scrivere «ED-275 (anticollisione ACAS Xu)».

### astm-f3442-25
Tipo: norma o documento regolatorio
Autori: ASTM International
Titolo: F3442-25 — Standard Specification for Detect and Avoid System Performance Requirements
Sede e anno: ASTM International, edizione 2025
Identificativo: ASTM F3442-25
Link: https://store.astm.org/f3442-25.html
Verifica: dato diverso: pagina aperta [g]; c'è «does not address avoidance of birds or natural hazards (for example, weather, clouds, terrain/obstacles)» e l'ambito «smaller unmanned aircraft (UA) encountering crewed aircraft»; ma al punto 1.6.1 la norma «defines a metric to assess the mitigation of a UA-to-UA mid-air collision, with specific safety performance thresholds to be addressed in future efforts». Il ruolo che la cita l'aveva vista solo in un risultato di ricerca.
Usata per: norma per velivoli piccoli, «che esclude uccelli e incontri fra droni» — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §3, S27
Note: correzione 3. Letto solo l'ambito pubblicato nella pagina del negozio; il testo della norma è a pagamento.

### ue-2023-1230
Tipo: norma o documento regolatorio
Autori: Parlamento europeo e Consiglio
Titolo: Regolamento (UE) 2023/1230 relativo alle macchine (il link punta a una rettifica del 4 luglio 2023)
Sede e anno: Gazzetta ufficiale dell'Unione europea, 2023
Identificativo: regolamento (UE) 2023/1230
Link: https://eur-lex.europa.eu/eli/reg/2023/1230/corrigendum/2023-07-04/oj/eng
Verifica: verificata dal curatore il 14-11-2026 in parte: EUR-Lex non è raggiungibile; la data è confermata [g] da una pagina della Commissione europea (https://single-market-economy.ec.europa.eu/sectors/mechanical-engineering/machinery_en): «All machinery placed on the EU market before 20 January 2027 must comply with the current Machinery Directive 2006/42/EC». «Il primo a nominare le macchine mobili autonome»: non verificato. Il ruolo che la cita l'aveva vista solo in un risultato di ricerca.
Usata per: a terra nessuna norma dedicata; regolamento macchine dal 20 gennaio 2027, il primo a nominare le macchine mobili autonome — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §3, S29
Note: correzione 10. Il link citato porta a una rettifica, non al testo: per citare il regolamento conviene il suo indirizzo proprio.

### iso-3691-4
Tipo: norma o documento regolatorio (scheda di un catalogo di norme)
Autori: ISO (recepita come EN ISO dal CEN)
Titolo: EN ISO 3691-4:2023 — Industrial trucks — Safety requirements and verification — Part 4: Driverless industrial trucks and their systems
Sede e anno: ISO, 2023
Identificativo: ISO 3691-4:2023
Link: https://genorma.com/en/standards/en-iso-3691-4-2023
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente [g], per il solo titolo. Il ruolo che la cita l'aveva vista solo in un risultato di ricerca.
Usata per: norma di riferimento per i veicoli terrestri senza conducente — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §3, S29
Note: catalogo di terzi; il contenuto della norma non è stato letto. Riguarda i carrelli industriali senza conducente, non i rover in generale.

### dnv-imo-codice-mass
Tipo: norma o documento regolatorio (notizia tecnica di una società di classifica)
Autori: DNV
Titolo: IMO MSC 111: New MASS Code adopted
Sede e anno: DNV, Technical and Regulatory News, 22 maggio 2026
Identificativo: manca
Link: https://www.dnv.com/news/2026/imo-mcs-111-new-mass-code-adopted/
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente [g] — «The new MASS Code was adopted as a non-mandatory instrument, with an entry into effect date of 1 July 2026»; «Applies to cargo ships only». Il ruolo che la cita l'aveva vista solo in un risultato di ricerca.
Usata per: in mare, codice MASS dell'IMO, non obbligatorio, dal 1° luglio 2026, solo navi da carico — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §3, S30
Note: fonte secondaria autorevole; il testo dell'IMO non è stato aperto.

### eurocontrol-asterix-cat062
Tipo: norma o documento regolatorio (trascrizione non ufficiale)
Autori: EUROCONTROL (specifica); trascrizione di Zoran Bosnjak (asterix-specs)
Titolo: ASTERIX, categoria 062 — SDPS Track Messages
Sede e anno: edizione 1.18, 13 agosto 2018 (dalla trascrizione)
Identificativo: ASTERIX CAT062, edizione 1.18
Link: https://zoranbosnjak.github.io/asterix-specs/specs/cat062/cats/cat1.18/definition.html
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente [g] — voce I062/080: CST «Age of the last received track update is higher than system dependent threshold (coasting)»; CNF «0: Confirmed track, 1: Tentative track»; I062/290 «System Track Update Ages»; I062/500 «Estimated Accuracy Of Track Position». Aperta anche dal ruolo che la cita.
Usata per: nei dati di sorveglianza lo stato di traccia ha il bit di «coasting», confermata o provvisoria, età e accuratezze: è il vocabolario del nucleo — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §3, S31
Usata per: scambio di stato ed età della traccia fra più veicoli — `f6-specializzazione/01-esperto-dominio/SPECIALIZZAZIONE.md` §5
Usata per: primo dei due agganci sull'uscita per il giurato della società — `f6-specializzazione/01-esperto-dominio/SPECIALIZZAZIONE.md` §6; ripreso in `f6-specializzazione/03-avversario/ATTACCO_SPECIALIZZAZIONE.md` S5
Note: è una trascrizione di terzi: per un uso formale va confrontata con il documento di EUROCONTROL (non aperto). Garantisce che il vocabolario esiste; non dice che il nucleo lo rispetti: «ispirato a», mai «conforme a».

### maeci-uama
Tipo: norma o documento regolatorio (pagina dell'autorità)
Autori: Ministero degli Affari Esteri e della Cooperazione Internazionale
Titolo: Autorità Nazionale UAMA: Materiali d'Armamento e a Duplice Uso
Sede e anno: sito del Ministero, letto il 14-11-2026
Identificativo: manca
Link: https://www.esteri.it/it/ministero/struttura/uama/
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente [g] — titolo dell'autorità; «Il controllo dell'esportazione e importazione di materiali d'armamento è disciplinato dalla Legge 9 luglio 1990, n.185»; sezione sul duplice uso. Il regolamento 2021/821 non è nominato in questa pagina. Il ruolo che la cita l'aveva vista solo in un risultato di ricerca.
Usata per: esportazione e duplice uso: l'autorità italiana è l'UAMA — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §6, S37
Note: dice chi vigila; non dice se un prototipo di componenti commerciali rientri nelle voci controllate (nel quadro: non verificato, lo valuta la società).

### it-legge-185-1990
Tipo: norma o documento regolatorio
Autori: Repubblica Italiana
Titolo: Legge 9 luglio 1990, n. 185 (controllo dell'esportazione, importazione e transito dei materiali di armamento)
Sede e anno: 1990
Identificativo: legge 185/1990
Link: manca nei file (citata tramite S37: https://www.esteri.it/it/ministero/struttura/uama/)
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente, per la sola esistenza e l'oggetto [g, dalla pagina del Ministero]. Il testo della legge non è stato aperto.
Usata per: esportazione di materiali d'armamento — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §6, S37
Note: il titolo fra parentesi è una descrizione, non il titolo ufficiale.

### ue-2021-821
Tipo: norma o documento regolatorio
Autori: Parlamento europeo e Consiglio
Titolo: Regolamento (UE) 2021/821 (regime dell'Unione di controllo delle esportazioni dei prodotti a duplice uso)
Sede e anno: Gazzetta ufficiale dell'Unione europea, 2021
Identificativo: regolamento (UE) 2021/821
Link: https://eur-lex.europa.eu/EN/legal-content/summary/dual-use-export-controls.html
Verifica: verificata dal curatore il 14-11-2026 in parte: la sintesi di EUR-Lex non è raggiungibile; il numero e l'oggetto sono confermati [g] da una pagina della Commissione europea (https://policy.trade.ec.europa.eu/help-exporters-and-importers/exporting-dual-use-items_en): «Regulation (EU) 2021/821 governs the EU's export control regime». Il ruolo che la cita l'aveva vista solo in un risultato di ricerca.
Usata per: esportazione e duplice uso — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §6, S37
Note: le voci per droni e camere termiche restano non verificate, come nel quadro. Il titolo fra parentesi è una descrizione.

### ue-2024-1689
Tipo: norma o documento regolatorio
Autori: Parlamento europeo e Consiglio
Titolo: Regolamento sull'intelligenza artificiale, articolo 2 (ambito di applicazione)
Sede e anno: Gazzetta ufficiale dell'Unione europea, 2024
Identificativo: regolamento (UE) 2024/1689 — numero non letto oggi su una pagina: da riconfermare
Link: manca nei file (citato tramite S38); testo dell'articolo letto su una copia non ufficiale: https://artificialintelligenceact.eu/article/2/
Verifica: verificata dal curatore il 14-11-2026 in parte: copia non ufficiale aperta [g] — «This Regulation does not apply to AI systems where and in so far they are placed on the market, put into service, or used with or without modification exclusively for military, defence or national security purposes, regardless of the type of entity carrying out those activities». Il testo ufficiale (EUR-Lex) non è raggiungibile; il numero del regolamento non l'ho letto oggi.
Usata per: il regolamento esclude i sistemi a uso esclusivamente militare, di difesa o di sicurezza nazionale — `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` §6 (lì attribuito a S38)
Note: voce aggiunta da me come fonte primaria di ciò che il quadro prende da un blog. «Il duplice uso resta dentro» è la lettura corrente di «exclusively», non una frase del testo.

### ue-2017-745
Tipo: norma o documento regolatorio
Autori: Parlamento europeo e Consiglio
Titolo: Regolamento (UE) 2017/745 relativo ai dispositivi medici, articolo 2 (definizioni), punto 1
Sede e anno: Gazzetta ufficiale dell'Unione europea, 2017; letto nella versione del 31-01-2020 della copia britannica
Identificativo: regolamento (UE) 2017/745
Link: https://www.legislation.gov.uk/eur/2017/745/article/2/2020-01-31
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente [g] — «'medical device' means any instrument, apparatus, appliance, software … intended by the manufacturer to be used … for … diagnosis, monitoring, treatment, alleviation of, or compensation for, an injury or disability». Aperta anche dal ruolo che la cita.
Usata per: cautela sul profilo assistivo: dispositivo medico è ciò che il fabbricante destina, fra l'altro, a «compensation for, an injury or disability»; se un ausilio all'orientamento vi rientri è non verificato — `f6-specializzazione/01-esperto-dominio/SPECIALIZZAZIONE.md` §1
Note: copia non ufficiale e ferma al 2020 (lo dice anche il ruolo). La citazione prova la definizione, non la classificazione del prototipo: quella resta non risolta e la decide un esperto regolatorio.

## F. Depositi di codice

Per tutti: licenza letta dall'interfaccia di GitHub [m] e dal file LEGGIMI [g] il 14-11-2026. Nessuno di questi componenti è stato provato dallo sciame; «tempo reale sul portatile della squadra» è non verificato in `MOTO_PROPRIO.md`. Gli articoli scientifici che i depositi indicano come propri riferimenti non sono citati nei quattro file e non li ho verificati.

### basalt
Tipo: deposito di codice
Autori: Vladyslav Usenko e collaboratori (TU München)
Titolo: Basalt (copia speculare su GitHub; il deposito principale è su GitLab)
Sede e anno: GitHub, ultimo aggiornamento marzo 2026
Identificativo: VladyslavUsenko/basalt
Link: https://github.com/VladyslavUsenko/basalt
Verifica: verificata dal curatore il 14-11-2026 in parte: pagina aperta [m, g]; licenza BSD-3-Clause («The code is provided under a BSD 3-clause license»); «Tutorial on Camera-IMU and Motion capture calibration with Realsense T265». «Anche senza IMU»: non cercato nel testo, non verificato. Aperta anche dal ruolo che la cita.
Usata per: componente aperto per l'odometria: camera più IMU, licenza BSD 3, tutorial sulla T265 — `f6-specializzazione/02-slam/MOTO_PROPRIO.md` §2(b)
Note: il LEGGIMI avverte che il codice di terzi incluso ha licenze diverse.

### rtabmap
Tipo: deposito di codice
Autori: Mathieu Labbé, IntRoLab, Université de Sherbrooke
Titolo: RTAB-Map library and standalone application
Sede e anno: GitHub, ultimo aggiornamento novembre 2026
Identificativo: introlab/rtabmap
Link: https://github.com/introlab/rtabmap
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente [m, g] — GitHub non riconosce la licenza in automatico («NOASSERTION»), ma il file LICENSE ha il testo di una licenza di tipo BSD («Redistribution and use in source and binary forms, with or without modification, are permitted provided that…»), con diritti di Mathieu Labbé, 2010–2025. Aperta anche dal ruolo che la cita.
Usata per: componente aperto: RGB-D, stereo, LiDAR (sensori non verificati dal ruolo); licenza BSD «dal distintivo» — `f6-specializzazione/02-slam/MOTO_PROPRIO.md` §2(b)
Note: la licenza ora è confermata dal file, non solo dal distintivo. I sensori supportati restano non verificati: nel LEGGIMI non ho trovato le parole cercate. Le dipendenze possono avere licenze diverse: non controllato.

### open-vins
Tipo: deposito di codice
Autori: Robot Perception and Navigation Group (Università del Delaware)
Titolo: OpenVINS — An open source platform for visual-inertial navigation research
Sede e anno: GitHub; versione 2.7 annunciata nel LEGGIMI l'11 maggio 2023, pubblicata su GitHub il 20 giugno 2023
Identificativo: rpng/open_vins
Link: https://github.com/rpng/open_vins
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente [m, g] — licenza GPL-3.0; ultima versione v2.7. Aperta anche dal ruolo che la cita.
Usata per: componente aperto: mono o stereo più IMU, GPL-3, versione 2.7 di maggio 2023 — `f6-specializzazione/02-slam/MOTO_PROPRIO.md` §2(b)
Note: licenza con obbligo di rilascio del codice derivato: pesa su chi vuole poi un prodotto, come dice il ruolo.

### vins-fusion
Tipo: deposito di codice
Autori: HKUST Aerial Robotics Group
Titolo: VINS-Fusion — An optimization-based multi-sensor state estimator
Sede e anno: GitHub, ultimo aggiornamento maggio 2024
Identificativo: HKUST-Aerial-Robotics/VINS-Fusion
Link: https://github.com/HKUST-Aerial-Robotics/VINS-Fusion
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente [m, g] — licenza GPL-3.0; «online temporal calibration (time offset between camera and IMU)». Aperta anche dal ruolo che la cita.
Usata per: componente aperto: mono o stereo più IMU, GPLv3, taratura in linea dello scarto temporale fra camera e IMU — `f6-specializzazione/02-slam/MOTO_PROPRIO.md` §2(b)
Note: fermo dal 2024.

### orb-slam3
Tipo: deposito di codice
Autori: Carlos Campos, Richard Elvira, Juan J. Gómez Rodríguez e altri (Universidad de Zaragoza; elenco completo nel LEGGIMI, non trascritto)
Titolo: ORB-SLAM3: An Accurate Open-Source Library for Visual, Visual-Inertial and Multi-Map SLAM
Sede e anno: GitHub; «V1.0, December 22th, 2021»
Identificativo: UZ-SLAMLab/ORB_SLAM3
Link: https://github.com/UZ-SLAMLab/ORB_SLAM3
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente [m, g] — licenza GPL-3.0; V1.0 del dicembre 2021; «monocular, stereo and RGB-D cameras». Aperta anche dal ruolo che la cita.
Usata per: componente aperto: mono, stereo, RGB-D, con o senza IMU, GPLv3, V1.0 del dicembre 2021 — `f6-specializzazione/02-slam/MOTO_PROPRIO.md` §2(b)
Note: fermo dal 2024.

### kiss-icp
Tipo: deposito di codice
Autori: PRBonn (Università di Bonn)
Titolo: KISS-ICP — A LiDAR odometry pipeline that just works
Sede e anno: GitHub, ultimo aggiornamento giugno 2026
Identificativo: PRBonn/kiss-icp
Link: https://github.com/PRBonn/kiss-icp
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente [m, g] — licenza MIT; «pip install kiss-icp». Aperta anche dal ruolo che la cita.
Usata per: componente aperto: solo LiDAR, licenza MIT, installabile con `pip` — `f6-specializzazione/02-slam/MOTO_PROPRIO.md` §2(b)
Note: serve un LiDAR, che la squadra non ha nel nucleo.

### fast-lio
Tipo: deposito di codice
Autori: HKU MaRS Lab
Titolo: FAST-LIO — A computationally efficient and robust LiDAR-inertial odometry (LIO) package
Sede e anno: GitHub, ultimo aggiornamento ottobre 2026
Identificativo: hku-mars/FAST_LIO
Link: https://github.com/hku-mars/FAST_LIO
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente [m, g] — licenza GPL-2.0; «Support ARM-based platforms including Khadas VIM3, Nivida TX2, Raspberry Pi 4B(8G RAM)»; nel LEGGIMI «Mid-360» non compare. Aperta anche dal ruolo che la cita.
Usata per: componente aperto: LiDAR più IMU, GPL-2.0, gira su piattaforme ARM; Mid-360 non nominato — `f6-specializzazione/02-slam/MOTO_PROPRIO.md` §2(b)
Note: «Nivida» è scritto così nel LEGGIMI.

---

## Che cosa propongo dopo

1. Portare nel documento dei riferimenti del progetto le correzioni 1–4 e 7 prima di ogni testo per la giuria: sono le sole che cambiano una frase già scritta nel quadro di dominio.
2. Per le quattro voci non raggiungibili: `koschi2021` si sostituisce con l'articolo di rivista (da leggere prima); `intel-bkm-d400` con la guida in rete del costruttore; `intel-t265-fine-produzione` e `ue-2021-664` vanno riaperte a mano da una persona, con un navigatore.
3. Le cifre ancora senza una fonte aperta, da non scrivere come fatti: «35 s e oltre un chilometro» (S20); «1 W» del termico (S17); «51 %» (S7); «il primo a nominare le macchine mobili autonome» (S29); la licenza di cuVSLAM; l'anno di fine produzione della T265; il mezzo di piazzale a 5–8 m/s (già non verificato nel quadro, senza fonte).
4. Stati: nessun enunciato tecnico cambia stato per queste verifiche. Il secondo aggancio per il giurato (`SPECIALIZZAZIONE.md` §6) passa da «non riverificabile in rete» (avversario, S5) a **sostenuto dalle fonti** per la parte documentale: le due pagine di PX4 dicono alla lettera ciò che viene loro attribuito. Che il prototipo produca davvero quel messaggio resta non provato.
