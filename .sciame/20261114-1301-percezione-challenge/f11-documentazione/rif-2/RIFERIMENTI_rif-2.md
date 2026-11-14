# Riferimenti, gruppo rif-2 — percezione-challenge, f11 (`sciame-fonti`), 14 novembre 2026

Gruppo: `f2/01-traduzione/SCHEDE.md`, `f2/03-triage/TRIAGE.md`, `f2/04-torneo/TORNEO.md`, `f2/05-selezione/SELEZIONE.md`, tutto `f3/H-012/`, tutto `f4/H-012/`, `f5/02-audit/AUDIT.md`. I percorsi sono relativi alla cartella della convocazione.

## In testa

**Conteggio.** 53 voci (25 fra articoli scientifici e articoli che descrivono un insieme di dati; 28 fra schede tecniche, pagine di costruttore, documentazione, depositi e altro).
- **Verificate da me oggi, pagina aperta e dato presente: 49** (di cui 7 con una correzione o una precisazione, elencate sotto; 15 per i soli dati bibliografici, come scritto nella voce).
- **Già verificate dal curatore in f3 (`f3/fonti/FONTI_VERIFICATE.md`): 27** delle 53; 25 le ho riaperte oggi, 2 no (`gerdsenai-da3-jetson`, `wikipedia-ricerca-bayesiana`) e valgono con la verifica di f3.
- **Non verificate: 2.** `intel-000030012` (non raggiungibile: 403, e il server rimanda a un indirizzo «404Redirector»); `sunny-mars07a` (vista solo nel riassunto di un motore di ricerca; la pagina del costruttore dà 404).
- Voci nuove rispetto a f3: 26 (24 verificate oggi).

**Voci che non esistono:** nessuna trovata. Tutti gli articoli citati esistono con gli autori e i titoli indicati.

**Attribuite male (da correggere nei documenti finali).**
1. **«In due studi l'aptico costa più dell'audio»** (`f2/05-selezione/SELEZIONE.md`, riga K-010; `f3/H-012/01-scene-dinamiche/SOLUZIONE.md`, tabella del §5, riga «Feedback»): **non è ciò che dicono le due fonti** (`martinez2014`, `lupu2020`). Martinez e altri scrivono il contrario per chi usa il bastone: «for white cane users, auditory feedback results in a 22 times higher cognitive load than haptic feedback», e la differenza non c'è nei vedenti bendati. Lupu e altri scrivono che gli stimoli aptici erano «less intuitive than the audio ones»; il carico cognitivo maggiore è attribuito all'uso del dispositivo rispetto al bastone, non all'aptico rispetto all'audio. La frase giusta è quella del ricercatore in f1 (`f1/3fff79e9c3ea/CONSEGNA.md`, riga 46 e riga 90): **studi discordi**. Che i «due studi» della selezione siano questi due è una mia deduzione (sono i soli due studi di confronto aptico/sonoro in `FONTI_VERIFICATE.md`): la selezione non li nomina. La conclusione operativa della selezione («non decide fra battito e messaggi») resta in piedi, anzi è rafforzata.
2. **I 95 ms «esposizione → fotogramma nell'applicazione»** (`f3/H-012/02-validazione/VERIFICA.md`, §3c; da lì i «circa 155 ms» di `SOLUZIONE_V2.md` §7, `AUDIT.md` ipotesi 3 e `VERDETTO.md`): la cifra è nella fonte (`realsense-alta-velocita-d435`, tabella 4), ma **misura un'altra cosa**: è un ciclo «motion-to-photon» fatto con `rs-latency-tool`, che comprende GPU, schermo a 120 Hz e trasporto USB. Il documento lo dice: «this experiment does not allow us to parse out the latency of the depth camera directly, it does provide a system-level upper limit». È quindi un limite superiore del sistema di prova, non la latenza del sensore. La somma 155 ms (ricontata: 16,5 + 95 + 22 + 21,3 = 154,8) resta un conto giusto su un addendo che sovrastima il tratto del sensore. Lo stato di R7 («non risolta») non cambia; cambia l'etichetta della riga.
3. **I «35 ms misurati da un utente a 90 fps»** (`f2/04-torneo/TORNEO.md`, parte 1, riga H-006): nel messaggio del forum (`realsense-forum-latenza`) sono la latenza media del flusso **infrarosso** di una D455, non della profondità; l'utente chiede appunto quanto sia in più quella della profondità, e la risposta non dà un numero. La «lettura incerta di un forum» («circa un periodo») ha una fonte primaria: lo stesso documento del punto 2, §4.5 («should in worst case introduce a latency of a little over a single frame time»).

**Cifre che non tornano o che non sono nella fonte.**
4. **LD19, risoluzione angolare 0,8°** (`SCHEDE.md`, `nuvole-punti-2`): la pagina aperta (`ldrobot-ld19`) scrive «Angular resolution ≤1°»; 0,8° è il valore derivato 360° / (4500 Hz / 10 Hz). «5–13 Hz»: nel testo letto oggi trovo solo «Sweep frequency 10 Hz» (non trovato, non smentito). Confermati 30 klx (non 60), 4500 Hz, 0,02–12 m.
5. **Femto Bolt, ambiente:** la pagina prodotto di oggi porta **tutte e due** le diciture: «Indoor» nella tabella delle specifiche e «Indoor/Semi-Outdoor» nella tabella di confronto con Azure Kinect. La discordanza K-009 fra costruttori resta; non è più «pagina contro PDF».
6. **Schöller e altri, completamento (non una correzione):** la frase «S-GAN è il migliore di 20 campioni» (`SOLUZIONE.md` §8, «non riletto») **è nell'articolo**; nella stessa Tabella I c'è anche la velocità costante campionata allo stesso modo (OUR-S), a **0,28 / 0,56**, sotto S-GAN (0,32 / 0,60). A parità di metodo di valutazione la velocità costante regge anche contro il generativo.
7. **«CVPR 2025» per EdgeTAM:** non confermato oggi né nella pagina arXiv né nel README del deposito (il curatore di f3 lo dava «dal deposito»). Da citare come prestampa arXiv salvo nuova verifica.

**Cambi di stato proposti.** (a) La frase del punto 1: da «fonti» a **smentita come scritta** (fonte primaria aperta). (b) `TORNEO.md`, parte 1, «D435i ≤ 2 % fino a 2 m» da «non aperta (403)» a **verificata** (oggi la pagina risponde: `realsense-d400-accuratezza`). (c) `SCHEDE.md`, `creativo-4`, «modo 4×4 a 60 Hz del VL53L5CX non verificato sul testo» → **verificato** (`st-um2884`, tabella 2). (d) `AUDIT.md`, ipotesi 1 (filtri dell'SDK), da «letto il riassunto della ricerca» a **verificata sulla pagina**. (e) `AUDIT.md`, ipotesi 11, «69°×42° (non verificato in rete)» → **trovato** nella pagina di confronto RealSense, con una riserva sull'attribuzione della colonna.

**Regole violate e scostamenti.** (1) I file scaricati (pagine e PDF) stanno nella cartella temporanea della sessione, non in `rif-2`; nessuno è stato eseguito. (2) `TRIAGE.md`, `SELEZIONE.md`, `ATTACCO.md`, `CONTROPROVE.md`, `MISURE*.md`, `VERDETTO.md`, `H-012.md`, `PREVISIONI.md`, gli script e i file dei risultati li ho letti con `grep` su un elenco di parole chiave (nomi di sensori, modelli, «fonte», «scheda», indirizzi), non per intero: un riferimento scritto senza nessuna di quelle parole può essermi sfuggito. Letti per intero: `SCHEDE.md`, `TORNEO.md`, `VERIFICA.md`, `PIANO_MISURE.md`, `SOLUZIONE_V2.md`, `AUDIT.md`. (3) Ho letto anche `f3/fonti/FONTI_VERIFICATE.md` e, con `grep`, `f1/3fff79e9c3ea/` per risalire alle fonti che i file del gruppo citano senza nome. (4) Per i dati bibliografici ho usato anche i registri Crossref ed Europe PMC, che sono registri e non la pagina dell'editore. (5) La verifica in rete è durata circa 6 minuti dei 25 concessi (16:12–16:18, `date -Is`); ciò che non ho controllato è scritto in ogni voce e nel §4. (6) Le cartelle f7–f10 non le ho lette.

**Indipendenza.** Condivido con gli autori il modello linguistico. L'indipendenza sta nel testo delle fonti: salvo dove è scritto altro, ogni dato «presente» è stato trovato con una ricerca testuale nel testo grezzo scaricato (pagina, PDF convertito con `pdftotext`, o registro), non in un riassunto.

**Previsioni scritte prima di aprire la rete** (`stato.md`, 16:11–16:12). P1 almeno una cifra o attribuzione diversa nella fonte primaria: **regge** (punti 1–4). P2 S-GAN migliore di 20 campioni: **regge**. P3 l'articolo Intel 000030012 esiste e parla di superfici trasparenti: **non risolta** (403; l'indirizzo viene rimandato a «404Redirector»). P4 PipeWire, quanto 1024 a 48000 Hz: **regge**. P5 persistenza predefinita «Valid in 2/last 4»: **regge**. P6 almeno un riferimento nominato senza dati non identificabile con certezza sulla pagina primaria: **regge** (Mars07A; RED, SR-LSTM, S-GAN e Helios2 Wide invece identificati). Notato dopo, non previsto: i punti 2, 3 e 6.

**Stato di tutto ciò che queste fonti sostengono.** Una fonte verificata dice che cosa scrive il costruttore o l'autore, non che il sistema dello sciame funzioni: nel progetto niente è provato sull'hardware, e le cifre di scheda sono dichiarazioni dei costruttori.

---

## 1. Articoli scientifici e articoli che descrivono insiemi di dati

### cao2023
Tipo: articolo scientifico
Autori: Jinkun Cao, Jiangmiao Pang, Xinshuo Weng, Rawal Khirodkar, Kris Kitani
Titolo: Observation-Centric SORT: Rethinking SORT for Robust Multi-Object Tracking
Sede e anno: IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR) 2023, pp. 9686–9696; prestampa arXiv del 27-03-2022
Identificativo: DOI 10.1109/CVPR52729.2023.00934; arXiv:2203.14360
Link: https://arxiv.org/abs/2203.14360
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente. Pagina arXiv (autori, titolo, «Accepted by CVPR 2023») e registro Crossref (pagine, DOI). Nel riassunto: «This leads to the accumulation of errors during a period of occlusion»; «OC-SORT runs at 700+ FPS on a single CPU». Già in f3/fonti.
Usata per: l'articolo descrive il rumore che il Kalman accumula in occlusione; associazione «alla SORT / OC-SORT» come schema — `f3/H-012/01-scene-dinamiche/SOLUZIONE.md` §8; `f4/H-012/05-correzioni/SOLUZIONE_V2.md` §8.
Usata per: associazione «tipo ByteTrack/OC-SORT» — `f2/01-traduzione/SCHEDE.md` (`ricercatore-1`).
Note: il deposito `noahcao/OC_SORT` è sotto licenza MIT (file LICENSE aperto oggi). L'articolo misura la velocità con rilevamenti già dati: i 700 fps non comprendono il rilevatore. Non garantisce niente sui pedoni dietro un pannello con un sensore di profondità.

### scholler2020
Tipo: articolo scientifico
Autori: Christoph Schöller, Vincent Aravantinos, Florian Lay, Alois Knoll
Titolo: What the Constant Velocity Model Can Teach Us About Pedestrian Motion Prediction
Sede e anno: IEEE Robotics and Automation Letters, vol. 5, n. 2, pp. 1696–1703, aprile 2020 (presentato a ICRA 2020)
Identificativo: DOI 10.1109/LRA.2020.2969925; arXiv:1903.07933
Link: https://arxiv.org/abs/1903.07933
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente. Pagina arXiv, registro Crossref e PDF intero (Tabella I, medie sui cinque scenari, previsione a 4,8 s, errore medio / finale in metri): velocità costante (OUR) 0,39 / 0,83; RED 0,44 / 0,91; SR-LSTM 0,45 / 0,94; S-GAN 0,32 / 0,60; velocità costante campionata (OUR-S) 0,28 / 0,56. Nel testo: «S-GAN and SoPhie were evaluated by drawing 20 samples and taking the predicted trajectories with minimum ADE and FDE». Già in f3/fonti.
Usata per: a 4,8 s, 0,39 / 0,83 m contro 0,44 / 0,91 del miglior appreso deterministico; 0,32 / 0,60 un generativo — `f2/01-traduzione/SCHEDE.md` (`ricercatore-2`, P2(a); coda, (b) 12).
Usata per: «fonti: 0,39/0,83 contro RED 0,44/0,91 confermati; S-GAN 0,32/0,60 sta sotto» — `f2/05-selezione/SELEZIONE.md` (riga H-011).
Usata per: la velocità costante regge contro RED e SR-LSTM; S-GAN «migliore di 20 campioni, non confrontabile (non riletto)» — `f3/H-012/01-scene-dinamiche/SOLUZIONE.md` §8.
Note: completamento: OUR-S (0,28 / 0,56) sta sotto S-GAN a parità di valutazione; il «non riletto» si può togliere. Limiti: dati ETH e UCY, camere fisse dall'alto, pedoni in spazi aperti; orizzonte 4,8 s con 3,2 s di storia; errore medio di spostamento, non una regione di confidenza. Non dice niente sull'occlusione dietro un pannello né su un sensore indossato.

### bewley2016
Tipo: articolo scientifico
Autori: Alex Bewley, Zongyuan Ge, Lionel Ott, Fabio Ramos, Ben Upcroft
Titolo: Simple Online and Realtime Tracking
Sede e anno: IEEE International Conference on Image Processing (ICIP) 2016 (pagine non controllate)
Identificativo: DOI 10.1109/ICIP.2016.7533003; arXiv:1602.00763
Link: https://arxiv.org/abs/1602.00763
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente. Pagina arXiv (autori, titolo, «Presented at ICIP 2016», DOI). Nel riassunto: «the tracker updates at a rate of 260 Hz». Già in f3/fonti.
Usata per: «calcolo trascurabile (SORT, stessa famiglia: 260 Hz)» — `f3/H-012/01-scene-dinamiche/SOLUZIONE.md` (B4).
Usata per: associazione «alla SORT» come schema — `f3/H-012/01-scene-dinamiche/SOLUZIONE.md` §8; `f4/H-012/05-correzioni/SOLUZIONE_V2.md` §8.
Note: i 260 Hz sono del solo tracciatore (Kalman più ungherese) su riquadri 2D già rilevati, sull'hardware degli autori: non sono una misura del blocco B4 dello sciame.

### carion2025
Tipo: articolo scientifico (prestampa)
Autori: Nicolas Carion, Laura Gustafson, Yuan-Ting Hu, Shoubhik Debnath, Ronghang Hu, Didac Suris, Chaitanya Ryali, Kalyan Vasudev Alwala, Haitham Khedr, Andrew Huang, Jie Lei, Tengyu Ma, Baishan Guo, Arpit Kalla, Markus Marks, Joseph Greer, Meng Wang, Peize Sun, Roman Rädle, Triantafyllos Afouras, Effrosyni Mavroudi, Katherine Xu, Tsung-Han Wu, Yu Zhou, Liliane Momeni, Rishi Hazra, Shuangrui Ding, Sagar Vaze, Francois Porcher, Feng Li, Siyuan Li, Aishwarya Kamath, Ho Kei Cheng, Piotr Dollár, Nikhila Ravi, Kate Saenko, Pengchuan Zhang, Christoph Feichtenhofer
Titolo: SAM 3: Segment Anything with Concepts
Sede e anno: arXiv, prima versione 20-11-2025, ultima 28-03-2026 (sede di pubblicazione non controllata)
Identificativo: arXiv:2511.16719
Link: https://arxiv.org/abs/2511.16719
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente. Pagina arXiv (38 autori, titolo). La cifra non è nel riassunto arXiv; oggi l'ho trovata nella pagina di Meta (`meta-sam31`): «SAM 3 runs in 30 milliseconds for a single image with more than 100 detected objects on an H200 GPU… near real-time performance for approximately five concurrent objects». Nel testo intero dell'articolo l'ha trovata il curatore in f3; oggi non l'ho riaperto.
Usata per: «SAM 3 dà 30 ms a immagine su una H200»: resta fuori dalla catena — `f3/H-012/01-scene-dinamiche/SOLUZIONE.md` §8; `f4/H-012/05-correzioni/SOLUZIONE_V2.md` §8.
Note: H200 è una GPU da centro di calcolo; la fonte non dà tempi su CPU o su schede piccole.

### yang2024
Tipo: articolo scientifico (prestampa) e deposito di codice
Autori: Cheng-Yen Yang, Hsiang-Wei Huang, Wenhao Chai, Zhongyu Jiang, Jenq-Neng Hwang
Titolo: SAMURAI: Adapting Segment Anything Model for Zero-Shot Visual Tracking with Motion-Aware Memory
Sede e anno: arXiv, 18-11-2024 (sede di pubblicazione non controllata)
Identificativo: arXiv:2411.11922
Link: https://arxiv.org/abs/2411.11922 ; deposito https://github.com/yangchris11/samurai
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente. Pagina arXiv (autori, titolo) e README del deposito: «Does SAMURAI support streaming input (e.g. webcam)? Not yet. The existing code doesn't support live/streaming video». Già in f3/fonti.
Usata per: «SAMURAI non lavora su video dal vivo» — `f3/H-012/01-scene-dinamiche/SOLUZIONE.md` §8; `f4/H-012/05-correzioni/SOLUZIONE_V2.md` §8.
Note: il limite è del codice pubblicato («not yet»), non del metodo: può cambiare. La licenza del deposito oggi non l'ho riletta (Apache-2.0 secondo f3).

### zholus2025
Tipo: articolo scientifico (prestampa)
Autori: Artem Zholus, Carl Doersch, Yi Yang, Skanda Koppula, Viorica Patraucean, Xu Owen He, Ignacio Rocco, Mehdi S. M. Sajjadi, Sarath Chandar, Ross Goroshin
Titolo: TAPNext: Tracking Any Point (TAP) as Next Token Prediction
Sede e anno: arXiv, 08-04-2025 (sede di pubblicazione non controllata)
Identificativo: arXiv:2504.05579
Link: https://arxiv.org/abs/2504.05579
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente. Pagina arXiv e PDF, Tabella 2: TAPNext-B con 1024 punti, 187 fps su H100 e 42 su V100, latenza 5,33 ms e 23 ms; con 256 punti 197 e 70 fps. Già in f3/fonti.
Usata per: «TAPNext dà 187 fps su H100» — `f3/H-012/01-scene-dinamiche/SOLUZIONE.md` §8; `f4/H-012/05-correzioni/SOLUZIONE_V2.md` §8.
Note: «348 fps», circolato in f1, non è nell'articolo (correzione già fatta in f3). Segue punti, non oggetti; nessuna misura su CPU.

### zhou2025
Tipo: articolo scientifico (prestampa) e deposito di codice
Autori: Chong Zhou, Chenchen Zhu, Yunyang Xiong, Saksham Suri, Fanyi Xiao, Lemeng Wu, Raghuraman Krishnamoorthi, Bo Dai, Chen Change Loy, Vikas Chandra, Bilge Soran
Titolo: EdgeTAM: On-Device Track Anything Model
Sede e anno: arXiv, 13-01-2025; «CVPR 2025» non confermato oggi
Identificativo: arXiv:2501.07256
Link: https://arxiv.org/abs/2501.07256 ; deposito https://github.com/facebookresearch/EdgeTAM
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente. Riassunto arXiv: «running at 16 FPS on iPhone 15 Pro Max»; README: «The EdgeTAM model checkpoints and code are licensed under Apache 2.0». Già in f3/fonti. Dato diverso: la sede «CVPR 2025» non compare né nella pagina arXiv né nel README letto oggi.
Usata per: «EdgeTAM (16 fps su iPhone 15 Pro Max, Apache 2.0) è il solo candidato leggero» — `f3/H-012/01-scene-dinamiche/SOLUZIONE.md` §8.
Note: i 16 fps sono su un telefono con acceleratore neurale, non su una CPU di portatile.

### lin2025
Tipo: articolo scientifico (prestampa)
Autori: Haotong Lin, Sili Chen, Junhao Liew, Donny Y. Chen, Zhenyu Li, Guang Shi, Jiashi Feng, Bingyi Kang
Titolo: Depth Anything 3: Recovering the Visual Space from Any Views
Sede e anno: arXiv, 13-11-2025 (sede di pubblicazione non controllata)
Identificativo: arXiv:2511.10647
Link: https://arxiv.org/abs/2511.10647
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente, per i soli dati bibliografici. La cifra dei 43 fps non è dell'articolo: vedi `gerdsenai-da3-jetson`.
Usata per: profondità monoculare come ripiego senza camera di profondità, lasciata fuori — `f3/H-012/01-scene-dinamiche/SOLUZIONE.md` §8; `f4/H-012/05-correzioni/SOLUZIONE_V2.md` §8 (senza cifra).
Note: l'articolo non dà velocità su hardware da campo.

### lee2026
Tipo: articolo scientifico
Autori: Sungjae Lee, Junhan Jeong, Yeonjoo Hong, Kwang In Kim
Titolo: Physically Guided Visual Mass Estimation from a Single RGB Image
Sede e anno: IJCAI 2026 (Main Track), secondo i commenti della pagina arXiv; prestampa del 28-01-2026 (atti e pagine non controllati)
Identificativo: arXiv:2601.20303
Link: https://arxiv.org/abs/2601.20303
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente, per dati bibliografici e riassunto («mass prediction from pixels is ill-posed»; prove su image2mass e ABO-500). Le cifre (ALDE 0,519; 0,665 e 1,066) oggi non le ho rilette: valgono con la verifica di f3, letta attraverso un riassunto.
Usata per: F-002, «la massa non è osservabile… sostenuto dalla letteratura (ricercatore)» — `f2/03-triage/TRIAGE.md` (§2); «F-002: fonte confermata; il "fattore 1,68" è derivato» — `f2/05-selezione/SELEZIONE.md` (§3).
Note: i file del gruppo non nominano l'articolo; l'identificazione viene da `f3/fonti/FONTI_VERIFICATE.md` (F29). «Fattore 1,68» = exp(0,519), calcolato dal ricercatore, non scritto nell'articolo. L'articolo stima la massa da un'immagine con un errore grande: sostiene «non affidabile», non «impossibile»; la non osservabilità in senso stretto è dimostrata dallo sciame solo nel modello del punto materiale con forza ignota.

### martinez2014
Tipo: articolo scientifico
Autori: Manuel Martinez, Angela Constantinescu, Boris Schauerte, Daniel Koester, Rainer Stiefelhagen
Titolo: Cognitive Evaluation of Haptic and Audio Feedback in Short Range Navigation Tasks
Sede e anno: Computers Helping People with Special Needs (ICCHP 2014), Lecture Notes in Computer Science, Springer, pp. 128–135, 2014 (numero del volume non controllato)
Identificativo: DOI 10.1007/978-3-319-08599-9_20
Link: https://doi.org/10.1007/978-3-319-08599-9_20
Verifica: dato diverso: l'articolo dice il contrario di ciò che gli si attribuisce. Pagina Springer aperta oggi (metadati e riassunto; il testo intero è a pagamento): «for white cane users, auditory feedback results in a 22 times higher cognitive load than haptic feedback. This discrepancy in cognitive load was not found on blindfolded users, thus we argue against evaluating navigation systems solely with blindfolded users». Già in f3/fonti, dove la frase è riportata senza il verso.
Usata per: «Fonti: in due studi l'aptico costa più dell'audio; non decide fra battito e messaggi» — `f2/05-selezione/SELEZIONE.md` (riga K-010); `f3/H-012/01-scene-dinamiche/SOLUZIONE.md` (§5, riga «Feedback (K-010)»).
Note: correzione 1 in testa. Per chi usa il bastone è il sonoro a costare 22 volte di più (protocollo NASA-TLX). L'articolo avverte anche che i vedenti bendati non valgono come sostituti: tocca la prova «tre persone bendate» prevista per K-010. Numero dei partecipanti non letto.

### lupu2020
Tipo: articolo scientifico
Autori: R. G. Lupu, O. Mitruț, A. Stan, F. Ungureanu, K. Kalimeri, A. Moldoveanu (cognomi e iniziali dal registro Europe PMC; nomi per esteso non verificati)
Titolo: Cognitive and Affective Assessment of Navigation and Mobility Tasks for the Visually Impaired via Electroencephalography and Behavioral Signals
Sede e anno: Sensors, vol. 20, n. 20, articolo 5821, 15-10-2020
Identificativo: DOI 10.3390/s20205821; PMID 33076251; PMCID PMC7602506
Link: https://doi.org/10.3390/s20205821
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente, con una precisazione. La pagina MDPI dà 403; dati bibliografici dal registro Crossref e riassunto dal registro Europe PMC: «eight visually impaired subjects»; «the haptic stimuli were less intuitive than the audio ones and that the navigation with the Sound of Vision device increased cognitive load and working memory». Dato diverso: il carico cognitivo maggiore è del dispositivo rispetto al bastone, non dell'aptico rispetto all'audio. Già in f3/fonti (letta là attraverso un riassunto).
Usata per: la stessa frase di `martinez2014` — `f2/05-selezione/SELEZIONE.md` (riga K-010); `f3/H-012/01-scene-dinamiche/SOLUZIONE.md` (§5).
Note: otto persone, un solo dispositivo (Sound of Vision). Sostiene «aptico meno intuitivo del sonoro», non «aptico più costoso».

### becker2018
Tipo: articolo scientifico
Autori: Stefan Becker, Ronny Hug, Wolfgang Hübner, Michael Arens
Titolo: RED: A Simple but Effective Baseline Predictor for the TrajNet Benchmark (su arXiv con il titolo «An Evaluation of Trajectory Prediction Approaches and Notes on the TrajNet Benchmark»)
Sede e anno: Computer Vision – ECCV 2018 Workshops, Lecture Notes in Computer Science, Springer, pp. 138–153 (atti usciti nel 2019)
Identificativo: DOI 10.1007/978-3-030-11015-4_13; arXiv:1805.07663
Link: https://arxiv.org/abs/1805.07663
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente, per i soli dati bibliografici (pagina arXiv, registro Crossref, e voce [14] nell'elenco dei riferimenti di `scholler2020`). Il testo non l'ho letto.
Usata per: «RED 0,44 / 0,91» come miglior predittore appreso deterministico — `f2/05-selezione/SELEZIONE.md` (riga H-011); `f3/H-012/01-scene-dinamiche/SOLUZIONE.md` §8.
Note: nei file dello sciame è solo nominato («RED»), senza riferimento. La cifra 0,44 / 0,91 non è di questo articolo: è la riesecuzione di Schöller e altri.

### zhang2019
Tipo: articolo scientifico
Autori: Pu Zhang, Wanli Ouyang, Pengfei Zhang, Jianru Xue, Nanning Zheng
Titolo: SR-LSTM: State Refinement for LSTM towards Pedestrian Trajectory Prediction
Sede e anno: IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR) 2019, pp. 12077–12086
Identificativo: DOI 10.1109/CVPR.2019.01236; arXiv:1903.02793
Link: https://arxiv.org/abs/1903.02793
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente, per i soli dati bibliografici (pagina arXiv, registro Crossref, voce [1] di `scholler2020`). Il testo non l'ho letto.
Usata per: «regge contro RED e SR-LSTM» (0,45 / 0,94 nella tabella di Schöller) — `f2/05-selezione/SELEZIONE.md` (riga H-011); `f3/H-012/01-scene-dinamiche/SOLUZIONE.md` §8.
Note: solo nominato nei file. Schöller e altri riportano per SR-LSTM i risultati dell'articolo originale.

### gupta2018
Tipo: articolo scientifico
Autori: Agrim Gupta, Justin Johnson, Li Fei-Fei, Silvio Savarese, Alexandre Alahi
Titolo: Social GAN: Socially Acceptable Trajectories with Generative Adversarial Networks
Sede e anno: IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR) 2018, pp. 2255–2264
Identificativo: DOI 10.1109/CVPR.2018.00240; arXiv:1803.10892
Link: https://arxiv.org/abs/1803.10892
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente, per i soli dati bibliografici (pagina arXiv, registro Crossref, voce [3] di `scholler2020`). Il testo non l'ho letto.
Usata per: «il generativo S-GAN sta a 0,32 / 0,60» — `f2/01-traduzione/SCHEDE.md` (`ricercatore-2`); `f2/05-selezione/SELEZIONE.md` (riga H-011); `f3/H-012/01-scene-dinamiche/SOLUZIONE.md` §8.
Note: solo nominato nei file. Lo 0,32 / 0,60 viene da un modello preaddestrato rieseguito da Schöller e altri («an improved version compared to what the authors report in their paper»), migliore di 20 campioni.

### pellegrini2009
Tipo: insieme di dati (articolo che lo descrive: dati «ETH»)
Autori: S. Pellegrini, A. Ess, K. Schindler, L. Van Gool (iniziali dall'elenco dei riferimenti di `scholler2020`)
Titolo: You'll never walk alone: Modeling social behavior for multi-target tracking
Sede e anno: IEEE 12th International Conference on Computer Vision (ICCV) 2009, pp. 261–268
Identificativo: DOI 10.1109/ICCV.2009.5459260
Link: https://doi.org/10.1109/ICCV.2009.5459260
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente, per i soli dati bibliografici (registro Crossref; voce [6] di `scholler2020`, che lo indica come fonte dei dati ETH). Testo non letto.
Usata per: «Prova da camere fisse dall'alto (ETH/UCY, 2020)» — `f2/01-traduzione/SCHEDE.md` (`ricercatore-2`, rischi).
Note: nei file è solo la sigla «ETH». Il «2020» della scheda è l'anno dell'articolo di Schöller, non dei dati (2009).

### lerner2007
Tipo: insieme di dati (articolo che lo descrive: dati «UCY»)
Autori: A. Lerner, Y. Chrysanthou, D. Lischinski (iniziali dall'elenco dei riferimenti di `scholler2020`)
Titolo: Crowds by Example
Sede e anno: Computer Graphics Forum, vol. 26, n. 3, pp. 655–664, 2007
Identificativo: DOI 10.1111/j.1467-8659.2007.01089.x
Link: https://doi.org/10.1111/j.1467-8659.2007.01089.x
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente, per i soli dati bibliografici (registro Crossref; voce [31] di `scholler2020`). Testo non letto.
Usata per: come `pellegrini2009` — `f2/01-traduzione/SCHEDE.md` (`ricercatore-2`, rischi).
Note: nei file è solo la sigla «UCY».

### lin2014
Tipo: insieme di dati (articolo che lo descrive: COCO)
Autori: Tsung-Yi Lin, Michael Maire, Serge Belongie, Lubomir Bourdev, Ross Girshick, James Hays, Pietro Perona, Deva Ramanan, C. Lawrence Zitnick, Piotr Dollár (elenco della versione arXiv; negli atti ECCV gli autori registrati sono otto, senza Bourdev e Girshick)
Titolo: Microsoft COCO: Common Objects in Context
Sede e anno: Computer Vision – ECCV 2014, Lecture Notes in Computer Science, Springer, pp. 740–755, 2014
Identificativo: DOI 10.1007/978-3-319-10602-1_48; arXiv:1405.0312
Link: https://arxiv.org/abs/1405.0312
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente, per i soli dati bibliografici (pagina arXiv, registro Crossref). L'elenco delle 80 classi è verificato sulla voce `ultralytics-coco-yaml`, non sull'articolo.
Usata per: «0 su 7 categorie d'ostacolo fra le 80 classi COCO» — `f2/01-traduzione/SCHEDE.md` (`visione-1`, P1); `f2/03-triage/TRIAGE.md` (H-006); `f2/04-torneo/TORNEO.md` (parte 1, H-006); `f2/05-selezione/SELEZIONE.md` (H-006); `f3/H-012/01-scene-dinamiche/SOLUZIONE.md` (B6, §7).
Note: i file citano «COCO» senza riferimento. L'articolo descrive 91 categorie; le 80 sono quelle usate per il rilevamento.

### zhang2022
Tipo: articolo scientifico e deposito di codice
Autori: Yifu Zhang, Peize Sun, Yi Jiang, Dongdong Yu, Fucheng Weng, Zehuan Yuan, Ping Luo, Wenyu Liu, Xinggang Wang
Titolo: ByteTrack: Multi-Object Tracking by Associating Every Detection Box
Sede e anno: Computer Vision – ECCV 2022, Lecture Notes in Computer Science, Springer, pp. 1–21, 2022
Identificativo: DOI 10.1007/978-3-031-20047-2_1; arXiv:2110.06864
Link: https://arxiv.org/abs/2110.06864
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente, per i soli dati bibliografici (pagina arXiv, registro Crossref). Il deposito (licenza MIT, «30 FPS… on a single V100 GPU») l'ha verificato il curatore in f3; oggi non l'ho riaperto.
Usata per: tracciatore «BoT-SORT o ByteTrack» nel percorso asincrono — `f2/01-traduzione/SCHEDE.md` (`visione-1`); associazione «tipo ByteTrack/OC-SORT» — `f2/01-traduzione/SCHEDE.md` (`ricercatore-1`).
Note: solo nominato nei file. Tracciatore su riquadri 2D nell'immagine, non sul piano del suolo.

### aharon2022
Tipo: articolo scientifico (prestampa)
Autori: Nir Aharon, Roy Orfaig, Ben-Zion Bobrovsky
Titolo: BoT-SORT: Robust Associations Multi-Pedestrian Tracking
Sede e anno: arXiv, 29-06-2022 (nessuna sede di pubblicazione verificata)
Identificativo: arXiv:2206.14651
Link: https://arxiv.org/abs/2206.14651
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente, per i soli dati bibliografici (pagina arXiv). Testo non letto.
Usata per: tracciatore «BoT-SORT o ByteTrack» — `f2/01-traduzione/SCHEDE.md` (`visione-1`).
Note: solo nominato nei file.

### ravi2024
Tipo: articolo scientifico (prestampa)
Autori: Nikhila Ravi, Valentin Gabeur, Yuan-Ting Hu, Ronghang Hu, Chaitanya Ryali, Tengyu Ma, Haitham Khedr, Roman Rädle, Chloe Rolland, Laura Gustafson, Eric Mintun, Junting Pan, Kalyan Vasudev Alwala, Nicolas Carion, Chao-Yuan Wu, Ross Girshick, Piotr Dollár, Christoph Feichtenhofer
Titolo: SAM 2: Segment Anything in Images and Videos
Sede e anno: arXiv, 01-08-2024 (sede di pubblicazione non controllata)
Identificativo: arXiv:2408.00714
Link: https://arxiv.org/abs/2408.00714
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente, per i soli dati bibliografici (pagina arXiv). Testo non letto.
Usata per: «SAM 2 e trasformatori di visione solo in asincrono (classe, riaggancio), mai a decidere un allarme» — `f2/01-traduzione/SCHEDE.md` (`ricercatore-2`).
Note: solo nominato nei file; nessuna cifra citata.

### clopper1934
Tipo: articolo scientifico (metodo statistico)
Autori: C. J. Clopper, E. S. Pearson (cognomi dal registro; iniziali a memoria, non verificate)
Titolo: The Use of Confidence or Fiducial Limits Illustrated in the Case of the Binomial
Sede e anno: Biometrika, vol. 26, n. 4, pp. 404–413, 1934
Identificativo: DOI 10.1093/biomet/26.4.404
Link: https://doi.org/10.1093/biomet/26.4.404
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente, per i soli dati bibliografici (registro Crossref). Testo non letto.
Usata per: «Limiti di Clopper-Pearson unilaterali al 95 %» come regola di decisione delle prove (300 passaggi per la soglia del 99 %, 2000 per l'85 %) — `f3/H-012/03-metrologo/PIANO_MISURE.md` (parte 1); «binomiale esatta» — `f3/H-012/02-validazione/VERIFICA.md` (§3b); «limite inferiore 99,25 %» con N = 400 — `f4/H-012/05-correzioni/SOLUZIONE_V2.md` (§1).
Note: il metodo è nominato nei file senza riferimento: la voce è aggiunta da me. Due conti ricontrollati oggi: 0,95^59 = 0,0485 e 0,99^299 = 0,0495 (tornano con «59» e «299» del piano).

### kuhn1955
Tipo: articolo scientifico (metodo)
Autori: H. W. Kuhn (cognome dal registro; iniziali a memoria, non verificate)
Titolo: The Hungarian method for the assignment problem
Sede e anno: Naval Research Logistics Quarterly, vol. 2, n. 1–2, pp. 83–97, 1955
Identificativo: DOI 10.1002/nav.3800020109
Link: https://doi.org/10.1002/nav.3800020109
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente, per i soli dati bibliografici (registro Crossref). Testo non letto.
Usata per: assegnazione «ungherese» dopo la porta di Mahalanobis — `f2/01-traduzione/SCHEDE.md` (`tracciamento-1`); `f2/04-torneo/TORNEO.md` (parte 2, H-013); `f3/H-012/01-scene-dinamiche/SOLUZIONE.md` (B4); `f4/H-012/05-correzioni/SOLUZIONE_V2.md` (B4).
Note: metodo nominato senza riferimento: voce aggiunta da me.

### kalman1960
Tipo: articolo scientifico (metodo)
Autori: R. E. Kalman (cognome dal registro; iniziali a memoria, non verificate)
Titolo: A New Approach to Linear Filtering and Prediction Problems
Sede e anno: Journal of Basic Engineering (Transactions of the ASME), vol. 82, n. 1, pp. 35–45, 1960
Identificativo: DOI 10.1115/1.3662552
Link: https://doi.org/10.1115/1.3662552
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente, per i soli dati bibliografici (registro Crossref). Testo non letto.
Usata per: il filtro di Kalman lineare a velocità quasi costante [x, y, vx, vy], q = 0,2 m²/s³ — `f2/01-traduzione/SCHEDE.md` (`kalman-1`, `kalman-2`); `f3/H-012/01-scene-dinamiche/SOLUZIONE.md` (B4); `f4/H-012/05-correzioni/SOLUZIONE_V2.md` (B4) e tutti i file del torneo.
Note: metodo nominato senza riferimento: voce aggiunta da me. Le soglie χ² usate nei file sono algebra, ricontrollata oggi: 9,21 = −2·ln(0,01) e 18,42 = −2·ln(0,0001), due gradi di libertà.

### ristic2013
Tipo: articolo scientifico (metodo)
Autori: Ristic, Vo, Vo, Farina (cognomi dal registro Crossref; nomi non verificati)
Titolo: A Tutorial on Bernoulli Filters: Theory, Implementation and Applications
Sede e anno: IEEE Transactions on Signal Processing, vol. 61, n. 13, pp. 3406–3430, luglio 2013
Identificativo: DOI 10.1109/TSP.2013.2257765
Link: https://doi.org/10.1109/TSP.2013.2257765
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente, per i soli dati bibliografici (registro Crossref). Testo non letto.
Usata per: «filtro di Bernoulli, circa 200 particelle per traccia in volo cieco» — `f2/01-traduzione/SCHEDE.md` (`tracciamento-2`); H-015 nel torneo — `f2/04-torneo/TORNEO.md` (parte 3).
Note: i file nominano il metodo senza fonte; questo è il riferimento d'uso corrente, proposto da me. Che l'autore dell'idea avesse in mente questo testo: non verificato.

### hulgard2016
Tipo: articolo scientifico
Autori: Hulgard, Ratcliffe (cognomi dal registro Crossref; nomi non verificati)
Titolo: Sonar sound groups and increased terminal buzz duration reflect task complexity in hunting bats
Sede e anno: Scientific Reports, vol. 6, articolo 21500, 09-02-2016
Identificativo: DOI 10.1038/srep21500
Link: https://doi.org/10.1038/srep21500
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente, per i soli dati bibliografici (registro Crossref). Testo non letto. Già in f3/fonti (solo dati bibliografici).
Usata per: l'analogia del «ronzio terminale» (uno «sguardo costoso» alla traccia più minacciosa) — `f2/01-traduzione/SCHEDE.md` (`creativo-4`); `f2/03-triage/TRIAGE.md` e `f2/05-selezione/SELEZIONE.md` (H-020, esclusa).
Note: nei file del gruppo c'è solo il nome dell'idea; il legame con questo articolo viene da f1 e da f3. È un'analogia biologica: non sostiene nessuna cifra, e l'idea è stata esclusa dal ramo.

---

## 2. Schede tecniche, pagine di costruttore, documentazione, depositi, altro

### st-vl53l7cx
Tipo: scheda tecnica
Autori: STMicroelectronics
Titolo: VL53L7CX — Time-of-Flight 8x8 multizone ranging sensor with 90° FoV
Sede e anno: STMicroelectronics, scheda DS13865, Rev 6, marzo 2023
Identificativo: DS13865 Rev 6
Link: https://www.pololu.com/file/0J1992/vl53l7cx.pdf (copia ospitata da Pololu; st.com oggi non risponde)
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente. Nel PDF: «60° x 60° square field of view (FoV) (90° diagonal)»; «Up to 350 cm ranging»; «(three sensors can cover 180° x 60° FoV)»; Tabella 17 (30 Hz): bianco 88 %, al buio 3500 mm tipici, a 5 klx 650 mm tipici; Tabella 18 (15 Hz): 2000 mm al buio, 500 mm a 5 klx. Già in f3/fonti.
Usata per: F-001, tre ToF multizona non coprono 360° (135°–180°); «three sensors can cover 180° x 60°» — `f2/03-triage/TRIAGE.md` (F-001); `f2/05-selezione/SELEZIONE.md` (K-009, F-001); `f3/H-012/01-scene-dinamiche/SOLUZIONE.md` (§6, §7); `f4/H-012/05-correzioni/SOLUZIONE_V2.md` (§8); `f4/H-012/09-arbitro/VERDETTO.md` (punto 8: «scheda del costruttore: 180°»).
Usata per: K-012, «VL53L7CX 2,0 m contro 3,5 m: due modi» — `f2/01-traduzione/SCHEDE.md` (coda, (b) 12); `f2/03-triage/TRIAGE.md` (K-012); `f2/05-selezione/SELEZIONE.md` (K-012).
Usata per: «a 5 klx il VL53L7CX tiene 0,5–0,65 m» — `f3/H-012/01-scene-dinamiche/SOLUZIONE.md` (§7); `f4/H-012/05-correzioni/SOLUZIONE_V2.md` (§8).
Note: che la Tabella 17 sia il modo 4×4 e la 18 il modo 8×8 lo dice f3; oggi ho letto le intestazioni «30 Hz» e «15 Hz», non la risoluzione. La revisione può non essere l'ultima. 5 klx è la condizione di prova della scheda, non il sole pieno. Valori tipici su bersaglio bianco: sul grigio e ai bordi del campo sono più bassi.

### st-vl53l5cx
Tipo: scheda tecnica
Autori: STMicroelectronics
Titolo: VL53L5CX — Time-of-Flight 8x8 multizone ranging sensor with wide field of view
Sede e anno: STMicroelectronics, scheda DS13754, Rev 2, agosto 2021
Identificativo: DS13754 Rev 2
Link: https://cdn.sparkfun.com/assets/6/e/3/0/6/vl53l5cx-datasheet.pdf (copia ospitata da SparkFun)
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente. Nel PDF: «63° diagonal square FoV»; «Up to 400 cm ranging»; «60 Hz frame rate capability»; «Sample rate: Up to 60 Hz». Il campo «45° × 45°» oggi non l'ho cercato (confermato in f3). Già in f3/fonti.
Usata per: F-001, «multizona 8×8 (45°–60°)» — `f2/03-triage/TRIAGE.md` (F-001).
Usata per: «modo 4×4 a 60 Hz del VL53L5CX non verificato sul testo» — `f2/01-traduzione/SCHEDE.md` (`creativo-4`, rischi): vedi `st-um2884`.
Note: esiste almeno una revisione più recente (un motore di ricerca indica una Rev 13 presso un distributore: non aperta).

### st-um2884
Tipo: documentazione di software (manuale del driver)
Autori: STMicroelectronics
Titolo: UM2884 — A guide to using the VL53L5CX multizone Time-of-Flight ranging sensor with wide field of view Ultra Lite Driver (ULD)
Sede e anno: STMicroelectronics, manuale d'uso UM2884, Rev 2, agosto 2021
Identificativo: UM2884 Rev 2
Link: https://core-electronics.com.au/attachments/localcontent/um2884-a-guide_75701dc7b2e.pdf (copia ospitata da un rivenditore)
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente. Tabella 2, «Minimum and maximum ranging frequencies»: 4x4 da 1 a 60 Hz; 8x8 da 1 a 15 Hz. In f3 era fra i «non controllati».
Usata per: scioglie «modo 4×4 a 60 Hz del VL53L5CX non verificato sul testo» — `f2/01-traduzione/SCHEDE.md` (`creativo-4`, rischi).
Note: l'idea che lo usava (H-020) è esclusa dal ramo. Revisione del 2021, forse non l'ultima.

### orbbec-femto-bolt
Tipo: pagina di costruttore o comunicato
Autori: Orbbec
Titolo: Femto Bolt (pagina prodotto)
Sede e anno: Orbbec, pagina prodotto letta il 14-11-2026
Identificativo: manca (pagina senza numero di documento)
Link: https://www.orbbec.com/products/tof-camera/femto-bolt/
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente. «H 120° V 120° (WFOV), H 75° V 65° (NFOV)»; «WFOV 2x2 binned 0.25 - 2.88 m»; «WFOV unbinned 0.25 - 2.21 m»; «NFOV 2x2 binned 0.5 - 5.46 m»; ambiente: «Indoor» nelle specifiche e «Indoor/Semi-Outdoor» nella tabella di confronto con Azure Kinect. Già in f3/fonti.
Usata per: caso limite «Femto Bolt, 120° esatti»: nessun ToF con campo orizzontale ≥ 130° — `f2/01-traduzione/SCHEDE.md` (`requisiti-1`, P1); `f2/04-torneo/TORNEO.md` (parte 1, H-007: «massimo 120° (Femto…)»); `f2/05-selezione/SELEZIONE.md` (H-007).
Usata per: K-012, 0,25–2,88 m contro 0,25–2,21 m: due modi — `f2/01-traduzione/SCHEDE.md` (coda, (b) 12); `f2/03-triage/TRIAGE.md` (K-012); `f2/05-selezione/SELEZIONE.md` (K-012).
Usata per: K-009, Orbbec «Indoor» o «Indoor/Semi-Outdoor» contro Luxonis «<2% outdoors» — `f2/01-traduzione/SCHEDE.md` (`ricercatore-1`); `f2/03-triage/TRIAGE.md` (K-009); `f2/05-selezione/SELEZIONE.md` (K-009).
Note: correzione 5 in testa. Prezzo non verificato oggi. La pagina può cambiare: conviene conservarne una copia con la data.

### orbbec-gemini-335
Tipo: pagina di costruttore o comunicato
Autori: Orbbec
Titolo: Gemini 335 (pagina prodotto)
Sede e anno: Orbbec, pagina prodotto letta il 14-11-2026
Identificativo: manca
Link: https://www.orbbec.com/products/stereo-vision-camera/gemini-335/
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente. «It has a 50mm baseline»; «Depth FOV H90° V65°»; «Spatial Precision: ≤ 1.5% (1280 x 800 @ 2m & 90% x 90% ROI)»; «Depth Range 0.10 - 20m+ (Optimal Range: 0.26 - 3m)»; «Indoor/Outdoor»; IMU. Aperta anche dal ruolo che la cita (avversario, torneo) e già in f3/fonti.
Usata per: errore al limite dichiarato a 4 m: 12 cm; tocca 15 cm a 4,5 m; base 50 mm; «90°×65°, non 87°×58°» — `f2/04-torneo/TORNEO.md` (parte 1, H-001 e «Fonti»); `f2/05-selezione/SELEZIONE.md` (H-001); `f3/H-012/03-metrologo/PIANO_MISURE.md` (critica 9: «Gemini 335 12»).
Usata per: una delle camere candidate, 90°×65° — `f2/01-traduzione/SCHEDE.md` (`lidar-1`); `f3/H-012/01-scene-dinamiche/SOLUZIONE.md` (B1); `f4/H-012/05-correzioni/SOLUZIONE_V2.md` (B1).
Note: l'1,5 % è «Spatial Precision» (RMSE), cioè rumore spaziale a 2 m; i 12 cm a 4 m sono una estrapolazione con z² fatta dall'avversario, non un dato di scheda. Tipo di otturatore non indicato (f3).

### realsense-d455
Tipo: pagina di costruttore o comunicato
Autori: RealSense (già Intel RealSense)
Titolo: RealSense Depth Camera D455 / D455f (pagina prodotto)
Sede e anno: RealSense, pagina prodotto letta il 14-11-2026
Identificativo: manca
Link: https://realsenseai.com/products/real-sense-depth-camera-d455f/
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente. «FOV 87° × 58°»; «Ideal Range .6 m to 6 m»; «Global Shutter»; «The D455 extends the distance between the depth sensors to 95 mm which improves the depth error to less than 2% at 4 m». Aperta anche dal ruolo che la cita (avversario, torneo).
Usata per: D455: 87°×58°, otturatore globale, IMU, 0,6–6 m — `f2/01-traduzione/SCHEDE.md` (`visione-1`, `lidar-1`); `f3/H-012/01-scene-dinamiche/SOLUZIONE.md` (B1); `f4/H-012/05-correzioni/SOLUZIONE_V2.md` (B1).
Usata per: errore al limite dichiarato a 4 m: 8 cm; tocca 15 cm a 5,5 m (da «<2% at 4 m», base 95 mm) — `f2/04-torneo/TORNEO.md` (parte 1, H-001); `f3/H-012/03-metrologo/PIANO_MISURE.md` (critica 9).
Usata per: banda senza dato accanto all'ombra, 9,5 cm con base 95 mm — `f5/02-audit/AUDIT.md` (ipotesi 10).
Note: «<2% at 4 m» è una dichiarazione del costruttore, in condizioni di prova sue (vedi `realsense-d400-accuratezza`: 80 % della regione, risoluzione HD). La presenza dell'IMU oggi non l'ho cercata nella pagina (confermata in f3).

### realsense-confronto-camere
Tipo: pagina di costruttore o comunicato
Autori: RealSense
Titolo: Compare Depth Cameras (tabella di confronto delle camere D400)
Sede e anno: RealSense, pagina letta il 14-11-2026
Identificativo: manca
Link: https://www.realsenseai.com/compare-depth-cameras/
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente, con una riserva. Nel testo estratto ci sono le colonne «D455 / D455f», «D435 / D435i», «D435f / D435if», le righe sugli otturatori (globale e progressivo) e tre celle «69° × 42°»; la conversione in testo perde l'allineamento delle colonne, quindi l'attribuzione di ogni cella al suo modello non è certa. Già in f3/fonti (D435i: 87°×58°, 0,3–3 m, RGB a otturatore progressivo).
Usata per: D435i fra le camere candidate, 87°×58° — `f2/01-traduzione/SCHEDE.md` (`lidar-1`; «classe D435» in `nuvole-punti-2`); `f3/H-012/01-scene-dinamiche/SOLUZIONE.md` (B1); `f4/H-012/05-correzioni/SOLUZIONE_V2.md` (B1).
Usata per: «allineando la profondità all'RGB, sulla D435i il campo scende a circa 69°×42° (non verificato in rete)» — `f5/02-audit/AUDIT.md` (ipotesi 11).
Note: il valore 69°×42° c'è; resta da leggere sulla pagina a occhio che sia la riga del campo RGB della D435i. Le conseguenze dell'audit (suolo visto da 1,65 m, ostacolo invisibile sotto 1,45 m) sono conti suoi, non della fonte.

### realsense-d400-accuratezza
Tipo: pagina di costruttore o comunicato (articolo dell'assistenza)
Autori: RealSense Help Center (articolo firmato Jesus Garcia)
Titolo: Depth accuracy for Intel RealSense D400 Series Cameras
Sede e anno: RealSense Help Center, articolo 360059129453, 12-11-2020 (poi aggiornato)
Identificativo: articolo 360059129453
Link: https://support.realsenseai.com/hc/en-us/articles/360059129453-Depth-accuracy-for-Intel-RealSense-D400-Series-Cameras
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente. Nel torneo era «non aperta (errore 403), solo riassunto»; oggi risponde. Tabella: D420/D430/D435/D435i «up to 2 Meters and 80% ROI, HD Resolution», D455 «up to 4 Meters»: Z-accuracy ≤ 2 %, RMS Error ≤ 2 %, Fill rate ≥ 99 %, Temporal Noise ≤ 1 %. Rimanda alla Tabella 4-9 della scheda della famiglia D400 (non aperta).
Usata per: D435i «≤ 2 % fino a 2 m»; al limite dichiarato 16 cm a 4 m, tocca 15 cm a 3,9 m — `f2/04-torneo/TORNEO.md` (parte 1, H-001 e «Fonti»); `f3/H-012/03-metrologo/PIANO_MISURE.md` (critica 9: «D435i 16»).
Usata per: curva «pessimista» del rumore, «2 % a 2 m» scalato con z² (4 / 9 / 16 cm a 2 / 3 / 4 m) — `f3/H-012/02-validazione/VERIFICA.md` (§4); `f4/H-012/05-correzioni/SOLUZIONE_V2.md` (B1).
Note: la specifica vale fino a 2 m per la D435i: i 16 cm a 4 m sono fuori dall'intervallo dichiarato (estrapolazione dello sciame). Vale per moduli integrati e tarati, sull'80 % della regione.

### realsense-forum-latenza
Tipo: altro (messaggio di un utente in un forum del costruttore)
Autori: un utente del forum; risposta di un moderatore
Titolo: Depth Camera Latency
Sede e anno: RealSense Help Center, sezione Community, D400 Series, 12-04-2024
Identificativo: messaggio 28370679789587
Link: https://support.realsenseai.com/hc/en-us/community/posts/28370679789587-Depth-Camera-Latency
Verifica: dato diverso: i 35 ms sono dell'infrarosso, non della profondità. Pagina aperta oggi (nel torneo: solo riassunto). Testo: «the mean latency for the infrared sensor on my D455 running at 90 fps is 35 ms… am I correct to assume that the depth latency is greater than the infrared latency?». La risposta dice che la profondità è costruita nella camera prima della trasmissione e rimanda allo strumento `rs-data-collect`, senza un numero.
Usata per: latenza del sensore: «circa un periodo (33 ms a 30 fps, lettura incerta di un forum) e 35 ms misurati da un utente a 90 fps» — `f2/04-torneo/TORNEO.md` (parte 1, H-006 (b) e «Fonti»); `f3/H-012/01-scene-dinamiche/PREVISIONI.md` (C2: «una lettura incerta di un forum, non aperta»).
Note: correzione 3 in testa. Una misura di un utente, senza metodo descritto: non è una fonte per un bilancio di latenza. La frase sul «periodo» va citata da `realsense-alta-velocita-d435`.

### intel-000030012
Tipo: pagina di costruttore o comunicato (articolo dell'assistenza)
Autori: Intel
Titolo: non verificato (articolo dell'assistenza Intel sulle superfici trasparenti e le camere RealSense, secondo il torneo)
Sede e anno: Intel Support, articolo 000030012; data non verificata
Identificativo: articolo 000030012
Link: https://intel.com/content/www/us/en/support/articles/000030012.html
Verifica: non raggiungibile. Oggi lo scaricamento diretto dà 403; lo strumento di lettura riceve un 301 verso un indirizzo «404Redirector», cioè con ogni probabilità l'articolo non è più in linea a quell'indirizzo. Nel torneo era visto solo nel riassunto di un motore di ricerca.
Usata per: «l'infrarosso cade sul primo oggetto opaco dietro la superficie trasparente»: premessa fisica del falso «libero» sul vetro — `f2/04-torneo/TORNEO.md` (parte 1, «Fonti», e riga H-008).
Note: la conclusione sul vetro non dipende da questa pagina: nei file è una premessa fisica dichiarata e un limite aperto («Vetro: smentito, limite dichiarato», `SOLUZIONE_V2.md` §7), da decidere con la prova H2 davanti a una porta a vetri. Nei documenti finali la frase va scritta senza citazione, oppure con una fonte nuova da cercare.

### realsense-alta-velocita-d435
Tipo: pagina di costruttore o comunicato (documento tecnico)
Autori: RealSense (già Intel RealSense); autori del documento non letti
Titolo: High-speed capture mode of RealSense Depth Camera D435
Sede e anno: RealSense, documentazione per sviluppatori, pagina letta il 14-11-2026; data e revisione non indicate nel testo letto
Identificativo: manca
Link: https://dev.realsenseai.com/docs/high-speed-capture-mode-of-intel-realsense-depth-camera-d435
Verifica: dato diverso: le cifre ci sono, ma misurano il sistema di prova e non il solo sensore. Pagina aperta oggi (e dal ruolo che la cita, attraverso un'estrazione automatica). Tabella 4, «Measured latencies of each frame rate»: 848×100 a 15 fps 127 ms; 30 fps 95 ms; 60 fps 47 ms; 90 fps 39 ms; 400 fps 25 ms. §4.5: misura fatta con `rs-latency-tool` puntando la camera su uno schermo da 120 Hz; «The GPU adds latency in displaying an image, and the LCD screen has refresh rate and LCD limitations, and USB data packet transport introduces latency… this experiment does not allow us to parse out the latency of the depth camera directly, it does provide a system-level upper limit». E ancora: «capturing motion for a global shutter camera should in worst case introduce a latency of a little over a single frame time».
Usata per: «esposizione → fotogramma nell'applicazione: media 95 ms a 30 fps; 127 a 15; 47 a 60; 39 a 90… che cosa includa la misura: non verificato» — `f3/H-012/02-validazione/VERIFICA.md` (§3c).
Usata per: «le sole voci note sommano circa 155 ms in media» contro la soglia di 150 ms — `f3/H-012/02-validazione/VERIFICA.md` (§3c); `f4/H-012/05-correzioni/SOLUZIONE_V2.md` (§7, R7); `f5/02-audit/AUDIT.md` (ipotesi 3: 0,288 s, 0,72 m); `f4/H-012/09-arbitro/VERDETTO.md` (costo; K-015).
Usata per: «flusso a 60 o 90 fps usando l'ultimo fotogramma» — `f4/H-012/05-correzioni/SOLUZIONE_V2.md` (B8); «i 47 e 39 ms vengono dai modi 848×100» — `f5/02-audit/AUDIT.md` (ipotesi 7).
Note: correzione 2 in testa: scioglie il «non verificato» di `VERIFICA.md`. Una camera (D435), un calcolatore, medie senza percentili, modi 848×100 (il documento dice che questi modi scambiano campo verticale con frequenza; i «circa 12°» dell'audit sono un suo conto, coerente con 58° × 100/480, non una cifra letta). I conti che ne discendono (0,72 m a 2,5 m/s; velocità massima coperta circa 1,4 m/s) usano un limite superiore: sono prudenti, non misurati. Decide la prova H12.

### realsense-taratura-profondita
Tipo: pagina di costruttore o comunicato (documento tecnico)
Autori: RealSense (già Intel RealSense); autori del documento non letti
Titolo: Tuning depth cameras for best performance
Sede e anno: RealSense, documentazione per sviluppatori, pagina letta il 14-11-2026; data e revisione non indicate nel testo letto
Identificativo: manca
Link: https://dev.realsenseai.com/docs/tuning-depth-cameras-for-best-performance
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente. «The depth error scales as the square of the distance away»; «D435 with HFOV=90deg, Xres=848, and baseline=50mm. Both are for subpixel=0.08»; «For a well-textured target you can expect to see Subpixel < 0.1 and even approaching 0.05». La formula è un'immagine: non letta (come dichiarato dal ruolo che la cita). Conto rifatto con σ = z²·s/(f·B), f = 424 px, B = 50 mm, s = 0,08: 1,5 / 3,4 / 6,0 cm a 2 / 3 / 4 m.
Usata per: curva «nominale» del rumore radiale R(z) nelle prove A e B — `f3/H-012/02-validazione/VERIFICA.md` (§4); `f4/H-012/05-correzioni/SOLUZIONE_V2.md` (B1: «1,5 / 3,4 / 6,0 cm (nominale, documento del costruttore)»); `f4/H-012/03-validazione/MISURE.md` (prova B: usa la curva nominale 1,5 / 3,4 / 6,0 cm, senza citare la fonte).
Usata per: base 50 mm della D435i (banda senza dato di 5 cm) — `f5/02-audit/AUDIT.md` (ipotesi 10).
Note: 0,08 pixel è il valore con cui il costruttore traccia una curva teorica su un bersaglio ben tessuto, non una garanzia: è il rumore di un piano interpolato localmente, non quello del centro di una persona che cammina (che è la grandezza R del filtro e va misurata, prova H1). Il documento parla della D435; per la D435i la base è la stessa secondo f3, non riletto oggi.

### realsense-filtri-post
Tipo: documentazione di software
Autori: RealSense (già Intel RealSense)
Titolo: Post-processing filters
Sede e anno: RealSense, documentazione per sviluppatori (SDK librealsense), pagina letta il 14-11-2026; versione dell'SDK non indicata nel testo letto
Identificativo: manca
Link: https://dev.realsenseai.com/docs/post-processing-filters/
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente. Nell'audit era letta solo nel riassunto della ricerca. Filtro temporale: «In cases where the pixel data is missing or invalid the filter uses a user-defined persistency mode to decide whether the missing value should be rectified with stored data»; «Persistency index… when missing pixels will be replace with the last valid value»; predefinito «3 (Valid in 2/last 4)». Riempimento dei buchi: «obtains the four immediate pixel "neighbors"… and selects one of them»; predefinito «1 (Farthest from around)». Anche il filtro spaziale ha un riempimento dei buchi.
Usata per: ipotesi 1, «i filtri dell'SDK cambiano un pixel senza dato in un dato» (persistenza predefinita «valido in 2 degli ultimi 4»; il riempimento copia un vicino) — `f5/02-audit/AUDIT.md` (ipotesi 1); condizione ripresa in `f4/H-012/09-arbitro/VERDETTO.md`; «filtri dell'SDK che riempiono i buchi» — `f3/H-012/02-validazione/VERIFICA.md` (§2, invariante 2).
Note: la pagina dà i valori predefiniti dei filtri quando sono usati; non dice quali filtri siano accesi in un dato programma (il flusso grezzo dell'SDK non li applica da solo; il visualizzatore del costruttore ne accende alcuni: non verificato oggi). La documentazione non è legata a una versione: va controllata su quella installata. Per la Gemini 335 (altro SDK): non verificato, come dice l'audit.

### livox-mid-360
Tipo: pagina di costruttore o comunicato
Autori: Livox
Titolo: Mid-360 — Specs
Sede e anno: Livox, pagina delle specifiche letta il 14-11-2026
Identificativo: manca
Link: https://www.livoxtech.com/mid-360/specs
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente. «Laser Wavelength 905 nm»; «Detection Range (@ 100 klx) 40 m @ 10% reflectivity, 70 m @ 80% reflectivity»; «FOV Horizontal: 360°, Vertical: -7°~52°»; «Frame Rate 10 Hz (typical)»; 200 000 punti/s. Aperta anche dal ruolo che la cita. In f3 era fra i «non controllati».
Usata per: «Livox Mid-360: 360°, 40 m al 10 % a 100 klx, 905 nm»: i 360° si hanno con un LiDAR a scansione, non con tre ToF — `f2/04-torneo/TORNEO.md` (parte 1, H-007 e «Fonti»); `f2/05-selezione/SELEZIONE.md` (§3, F-001: «prezzo non verificato»).
Note: principio di misura e prezzo non sono nella pagina: restano non verificati, come scrive il torneo.

### sunny-mars07a
Tipo: pagina di costruttore o comunicato
Autori: Sunny Optical (identificazione dal solo riassunto del motore di ricerca)
Titolo: Mars07A (camera ToF)
Sede e anno: non verificati
Identificativo: manca
Link: https://www.sunnyaiot.com/en/product/ToF/Mars07A.html (oggi dà 404)
Verifica: vista solo nel riassunto di un motore di ricerca. Il riassunto di oggi attribuisce alla pagina: campo ToF 120° × 56°, 224×109 a 10 fps, 0,1–2,5 m al 90 % di riflettanza, 940 nm. La pagina, aperta direttamente con due strumenti, dà 404.
Usata per: «Camere ToF: massimo 120° (Femto; Mars07A 120°×56°; Helios2 Wide 108°)» — `f2/04-torneo/TORNEO.md` (parte 1, H-007; «Non aperte»).
Note: il torneo non nominava il costruttore; «Sunny Optical» è da confermare. La conclusione (nessuna camera ToF con ≥ 130°) non dipende da questa voce: è una ricerca dichiarata non esaustiva.

### lucid-helios2-wide
Tipo: pagina di costruttore o comunicato
Autori: LUCID Vision Labs
Titolo: Helios2 Wide Time-of-Flight (ToF) IP67 3D Camera (pagina prodotto)
Sede e anno: LUCID Vision Labs, pagina prodotto letta il 14-11-2026
Identificativo: manca
Link: https://thinklucid.com/product/helios2-wide-time-of-flight-tof-ip67-3d-camera/
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente. «wide-angle lens providing a 108º angle of view»; «Lens Field of View 108° x 78° (nominal)»; «4 x VCSEL laser diodes, Class 1, @ 850nm». Nel torneo era vista solo nel riassunto della ricerca.
Usata per: «Helios2 Wide 108°» — `f2/04-torneo/TORNEO.md` (parte 1, H-007).
Note: il torneo non nominava il costruttore né l'indirizzo: li ho trovati io. Portata e comportamento al sole non letti.

### slamtec-rplidar-c1
Tipo: pagina di costruttore o comunicato
Autori: Slamtec
Titolo: RPLIDAR C1 (pagina prodotto e pagina delle specifiche)
Sede e anno: Slamtec, pagine lette il 14-11-2026
Identificativo: manca
Link: https://www.slamtec.com/en/c1/spec
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente. «White: 0.05~12m (70% Reflectivity)»; «Black: 0.05~6m (10% Reflectivity)»; «5KHz»; «8~12Hz, 10Hz (Typical)»; «0.72°»; «40,000lux». Già in f3/fonti (letta là attraverso un riassunto).
Usata per: LiDAR 2D rotante: «360° a 10 Hz, 5000 punti/s, 12 m, 6 m sul nero»; 8 punti su una persona a 5 m, 2 su una gamba — `f2/01-traduzione/SCHEDE.md` (`lidar-2`); smentita della variante al petto (1,7–1,9 punti su una gamba a 5 m, dal passo angolare) — `f2/04-torneo/TORNEO.md` (parte 1, H-003); `f2/05-selezione/SELEZIONE.md` (H-003).
Note: prezzo «70–80 $»: non verificato. I conti dei punti sono dello sciame.

### ldrobot-ld19
Tipo: pagina di costruttore o comunicato (pagina di un rivenditore: wiki Waveshare)
Autori: Waveshare (il sensore è di LDROBOT)
Titolo: DTOF LIDAR LD19
Sede e anno: Waveshare, wiki, pagina letta il 14-11-2026
Identificativo: manca
Link: https://www.waveshare.com/wiki/DTOF_LIDAR_LD19
Verifica: dato diverso: risoluzione angolare «≤1°», non «0,8°». Pagina aperta oggi: «Measuring radius 12m»; «30K Lux anti-glare interference»; «4500Hz measurement frequency»; «Typical measuring range 0.02~12m»; «Sweep frequency 10 Hz»; «Angular resolution ≤1°». «5–13 Hz»: non trovato nelle righe lette. Già in f3/fonti (letta là attraverso un riassunto; 0,8° «non trovata»).
Usata per: «LD19: 0,8°, 5–13 Hz, 12 m»; 8,9 fasci su un pedone a 4 m — `f2/01-traduzione/SCHEDE.md` (`nuvole-punti-2`); «RPLIDAR C1 o LD19, 70–80 $» — `f2/01-traduzione/SCHEDE.md` (`lidar-2`).
Usata per: «Fonti: LD19 tiene 30 klx, non 60» — `f2/05-selezione/SELEZIONE.md` (H-003).
Note: correzione 4 in testa. 0,8° = 360° / 450 punti per giro a 10 Hz: derivato, da dichiarare così. È la pagina di un rivenditore, non la scheda del costruttore (non cercata). Prezzo non verificato.

### unitree-l2
Tipo: pagina di costruttore o comunicato
Autori: Unitree Robotics
Titolo: Unitree 4D LiDAR L2 (pagina prodotto)
Sede e anno: Unitree, pagina prodotto letta il 14-11-2026
Identificativo: manca
Link: https://www.unitree.com/L2
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente. «$419»; «360°×96°»; «Circumferential scanning frequency 5.55Hz (Customizable adjustment)»; 64 000 punti/s; «30m @90% reflectivity»; «Near blind spot 0.05m». In f3 era fra i «non controllati».
Usata per: «Con 420 $ in più: Unitree L2, 3D a 360°, 5,55 Hz» — `f2/01-traduzione/SCHEDE.md` (`lidar-2`).
Note: prezzo di listino del costruttore al 14-11-2026, in dollari, senza spedizione né dazi: può cambiare. La pagina dichiara la tenuta a 100 klx; non verificata da nessuno.

### luxonis-tof
Tipo: documentazione di costruttore
Autori: Luxonis
Titolo: ToF Depth Perception
Sede e anno: Luxonis, documentazione dell'hardware, pagina letta il 14-11-2026
Identificativo: manca
Link: https://docs.luxonis.com/hardware/platform/depth/ToF-depth
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente. «20cm - 5m»; «ToF sensors have a depth error of <1% indoors, <2% outdoors»; «Issues when using multiple ToFs (interference)»; «Limited resolution: 640x480». Già in f3/fonti.
Usata per: K-009, sole non risolto: Luxonis «<2% outdoors» contro Orbbec «Indoor» — `f2/01-traduzione/SCHEDE.md` (`ricercatore-1`); `f2/03-triage/TRIAGE.md` (K-009); `f2/05-selezione/SELEZIONE.md` (K-009).
Note: fonte del costruttore; «outdoors» senza illuminamento dichiarato. Non decide K-009: decide la prova al sole sul sensore posseduto.

### pipewire-conf
Tipo: documentazione di software
Autori: progetto PipeWire
Titolo: pipewire.conf(5) — The PipeWire server configuration file
Sede e anno: documentazione di PipeWire, pagina letta il 14-11-2026; versione del software non indicata nel testo letto
Identificativo: pagina di manuale `pipewire.conf(5)`
Link: https://docs.pipewire.org/page_man_pipewire_conf_5.html
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente. «default.clock.rate = 48000»; «default.clock.quantum = 1024 — Default quantum used when no client specifies one»; «default.clock.quantum-limit = 8192». Aperta anche dal ruolo che la cita.
Usata per: «campioni → scheda audio: ≥ 21,3 ms, un quanto 1024 / 48000, default di PipeWire» — `f3/H-012/02-validazione/VERIFICA.md` (§3c); entra nei «circa 155 ms» di `SOLUZIONE_V2.md` (§7), `AUDIT.md` (ipotesi 3), `VERDETTO.md`.
Note: 1024/48000 = 21,3 ms è un valore predefinito, non una misura; vale solo se il calcolatore della demo usa PipeWire con la configurazione di fabbrica. Un cliente può chiedere un quanto più piccolo. La latenza dell'uscita (cavo, Bluetooth) resta senza fonte, come scrive la verifica.

### ultralytics-yolo26
Tipo: documentazione di software
Autori: Ultralytics
Titolo: Ultralytics YOLO26 (pagina del modello) e file LICENSE del deposito
Sede e anno: Ultralytics, documentazione e deposito `ultralytics/ultralytics`, letti il 14-11-2026
Identificativo: manca
Link: https://docs.ultralytics.com/models/yolo26/ ; https://github.com/ultralytics/ultralytics
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente. Riga YOLO26n, 640: mAP 40,9 (40,1 senza soppressione dei non massimi), CPU ONNX 38,9 ± 0,7 ms, T4 TensorRT 1,7 ± 0,0 ms, 2,4 milioni di parametri. File LICENSE: «GNU AFFERO GENERAL PUBLIC LICENSE Version 3». Già in f3/fonti.
Usata per: «YOLO26n 38,9 ms su CPU, AGPL-3.0» come alternativa nel ramo asincrono — `f2/05-selezione/SELEZIONE.md` (H-006); `f3/H-012/01-scene-dinamiche/SOLUZIONE.md` (B6, §8: «38,9 ± 0,7 ms»); `f4/H-012/05-correzioni/SOLUZIONE_V2.md` (B6, §8). Rischio «AGPL-3.0 (alternativa RF-DETR)» — `f2/01-traduzione/SCHEDE.md` (`visione-1`).
Note: i 38,9 ms sono su una CPU da server (la pagina nomina un Intel Xeon a 2,00 GHz), in ONNX: non sono il tempo su un portatile. Il README di RF-DETR dà per YOLO26-N un AP di 40,3: differenza di protocollo, non controllata. L'AGPL-3.0 impone obblighi sul codice distribuito o offerto in rete: per un prototipo da hackathon conta se il codice viene pubblicato.

### ultralytics-coco-yaml
Tipo: documentazione di software (file di configurazione di un insieme di dati)
Autori: Ultralytics
Titolo: coco.yaml — COCO 2017 dataset (file di configurazione)
Sede e anno: deposito `ultralytics/ultralytics`, ramo `main`, letto il 14-11-2026
Identificativo: `ultralytics/cfg/datasets/coco.yaml`
Link: https://raw.githubusercontent.com/ultralytics/ultralytics/main/ultralytics/cfg/datasets/coco.yaml
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente. 80 classi numerate (contate con `grep`). Ci sono: bicycle, car, fire hydrant, bench, chair, potted plant, dining table. Non ci sono: wall, door, stair, pole. Intestazione AGPL-3.0. Aperta anche dal ruolo che la cita.
Usata per: «0 su 7 categorie d'ostacolo fra le 80 classi COCO»; COCO contiene sedia, panca, tavolo, bicicletta, auto, idrante, pianta in vaso; non muro, porta, gradino, palo — `f2/04-torneo/TORNEO.md` (parte 1, H-006 e «Fonti»); `f2/01-traduzione/SCHEDE.md` (`visione-1`); `f2/05-selezione/SELEZIONE.md` (H-006); `f3/H-012/01-scene-dinamiche/SOLUZIONE.md` (B6, §7).
Note: la lista delle sette categorie è scelta dall'autore dell'idea (lo scrive il torneo). Il file è del ramo principale: può cambiare; per la provenienza va fissato a un commit.

### ultralytics-tracciatori
Tipo: documentazione di software
Autori: Ultralytics
Titolo: Multi-Object Tracking with Ultralytics YOLO (modo «track») e `cfg/default.yaml`
Sede e anno: Ultralytics, documentazione e deposito, letti il 14-11-2026
Identificativo: `ultralytics/cfg/default.yaml`
Link: https://docs.ultralytics.com/modes/track/
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente. Pagina: «OC-SORT, Deep OC-SORT, FastTracker, TrackTrack are available alongside BoT-SORT and ByteTrack»; «Default tracker (TrackTrack)». `default.yaml`, riga 139: `tracker: tracktrack.yaml`. Già in f3/fonti.
Usata per: «rilevatore "nano" con maschere + tracciatore (BoT-SORT o ByteTrack)» nel percorso asincrono — `f2/01-traduzione/SCHEDE.md` (`visione-1`); `f2/03-triage/TRIAGE.md` (H-006).
Note: i file del gruppo non citano questa pagina: la voce documenta da dove vengono i due tracciatori nominati. Il tracciatore predefinito è TrackTrack, non ByteTrack (correzione già di f3). Codice sotto AGPL-3.0.

### roboflow-rf-detr
Tipo: deposito di codice
Autori: Roboflow
Titolo: RF-DETR (README del deposito)
Sede e anno: deposito `roboflow/rf-detr`, ramo `develop`, letto il 14-11-2026 (il ramo `main` dà 404)
Identificativo: manca
Link: https://github.com/roboflow/rf-detr
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente. Tabella: RF-DETR-N, COCO AP50:95 48,4, latenza 2,3 ms, 30,5 milioni di parametri, 384×384, Apache 2.0. Testo: Nano, Small, Medium, Large, tutta la segmentazione e i punti chiave sotto Apache 2.0; Atto, Femto, Pico, XL, 2XL sotto PML 1.0; «YOLOv8, YOLO11 and YOLO26 are released under AGPL-3.0». Già in f3/fonti.
Usata per: «RF-DETR-N: 2,3 ms su T4, AP 48,4, Apache 2.0 (le varianti Atto, Femto, Pico, XL, 2XL sono sotto PML 1.0)» — `f3/H-012/01-scene-dinamiche/SOLUZIONE.md` (B6, §8); `f4/H-012/05-correzioni/SOLUZIONE_V2.md` (B6, §8); `f2/05-selezione/SELEZIONE.md` (H-006); alternativa all'AGPL — `f2/01-traduzione/SCHEDE.md` (`visione-1`).
Note: che i 2,3 ms siano su T4 con TensorRT a mezza precisione lo dice f3; oggi ho letto la tabella, non le condizioni di misura. Nessun tempo su CPU nel README letto: il costo del ramo asincrono su un portatile resta da misurare.

### meta-sam31
Tipo: pagina di costruttore o comunicato
Autori: Meta
Titolo: SAM 3.1: Faster and More Accessible Real-Time Video Detection and Tracking With Multiplexing and Global Reasoning (aggiornamento in testa alla pagina di SAM 3)
Sede e anno: blog di Meta AI; aggiornamento del 27-03-2026 secondo f3 (data non riletta oggi)
Identificativo: manca
Link: https://ai.meta.com/blog/segment-anything-model-3/
Verifica: verificata dal curatore il 14-11-2026: pagina aperta e dato presente. «doubles the processing speed for videos with a medium number of objects, increasing throughput from 16 to 32 frames per second on a single H100 GPU». Già in f3/fonti (letta là attraverso un riassunto).
Usata per: «SAM 3.1 passa da 16 a 32 fps su una H100: non è il calcolo di un hackathon» — `f3/H-012/01-scene-dinamiche/SOLUZIONE.md` (§8).
Note: comunicato del costruttore, non un articolo. Nella stessa pagina c'è la frase sui 30 ms di SAM 3 (vedi `carion2025`).

### gerdsenai-da3-jetson
Tipo: altro (messaggio in un forum di comunità)
Autori: GerdsenAI (secondo f3)
Titolo: non verificato oggi (messaggio sul forum Open Robotics su Depth Anything 3 con TensorRT su Jetson)
Sede e anno: forum Open Robotics, 05-02-2026 (secondo f3)
Identificativo: manca
Link: manca nei file del gruppo (il forum è https://discourse.openrobotics.org; l'indirizzo esatto è in f1)
Verifica: aperta dal curatore in f3 il 14-11-2026 («6,35 → 43+ fps su Jetson Orin NX 16 GB: sì»; variante «small»: assente nel messaggio); oggi non riaperta.
Usata per: «Depth Anything 3 arriva a 43 fps su Jetson Orin NX secondo una fonte di comunità» — `f3/H-012/01-scene-dinamiche/SOLUZIONE.md` (§8).
Note: fonte di comunità, non primaria; non dice quale variante del modello. La soluzione la usa solo per dire che la profondità monoculare resta fuori.

### wikipedia-ricerca-bayesiana
Tipo: altro (voce di enciclopedia: fonte secondaria)
Autori: collaboratori di Wikipedia
Titolo: Bayesian search theory
Sede e anno: Wikipedia in inglese; versione non fissata
Identificativo: manca
Link: https://en.wikipedia.org/wiki/Bayesian_search_theory
Verifica: aperta dal curatore in f3 il 14-11-2026, attraverso un riassunto (p′ = p(1−q)/(1−pq)); oggi non riaperta. La fonte primaria a cui rimanda (Stone, 1975) non è stata aperta da nessuno.
Usata per: l'idea «Il sottomarino perduto»: particelle che nelle celle viste libere pesano (1−Pd) — `f2/01-traduzione/SCHEDE.md` (`creativo-2`); H-016 nel torneo — `f2/04-torneo/TORNEO.md` (parte 3).
Note: nei file del gruppo c'è solo il nome dell'idea. Una voce di enciclopedia non conta come fonte primaria: nei documenti finali va citata come tale o sostituita.

---

## 3. Affermazioni dei file del gruppo che parlano di «fonti» o «schede» senza una fonte identificabile

1. **Prezzi:** «330–417 $» delle camere (`SCHEDE.md`, `lidar-1`), «70–80 $» dei LiDAR 2D (`lidar-2`), prezzo del Livox Mid-360: **non verificati** (solo l'Unitree L2, 419 $, è verificato oggi).
2. **Latenza audio:** sintesi vocale e uscita via cavo o Bluetooth: «nessuna fonte» già nei file (`VERIFICA.md` §3c); confermo che nel gruppo non c'è.
3. **Curva del rumore «del torneo», 5 cm·(z/2)²:** è un'ipotesi dell'avversario, «non da scheda» (lo scrive `TORNEO.md`, parte 2): non è una fonte.
4. **«Portata dimezzata sul nero», «vetro invisibile», «sole pieno»** per le camere stereo (`SCHEDE.md`, `lidar-1`; `nuvole-punti-2`): dichiarati non verificati dagli autori; nessuna fonte nel gruppo.
5. **Velocità del pedone** (1,2–1,4 m/s; v_max 2,5 m/s), **larghezza del corpo 40 cm, altezza del sensore 1,2 m:** ipotesi degli autori, senza fonte.
6. **«Rolling Grid», «log-odds»** (`SCHEDE.md`, `rovesciatore-2`, `nuvole-punti-1`): tecniche nominate senza riferimento; in f3 sono verificati i dati bibliografici di OctoMap (Hornung e altri, 2013) e di Moras e altri (2011), che nei file del gruppo però non compaiono.
7. **Norme e documenti regolatori:** nessuno citato nei file del gruppo.

## 4. Che cosa non ho verificato

- Il testo intero degli articoli citati solo per nome (RED, SR-LSTM, S-GAN, ETH, UCY, COCO, ByteTrack, BoT-SORT, SAM 2, Clopper e Pearson, Kuhn, Kalman, Ristic e altri, Hulgard e Ratcliffe): solo i dati bibliografici.
- Le sedi di pubblicazione di SAM 3, SAMURAI, TAPNext, EdgeTAM, Depth Anything 3, SAM 2, BoT-SORT: citati come prestampe arXiv.
- Le cifre di Lee e altri (ALDE, APE) e il numero dei partecipanti di Martinez e altri.
- La scheda della famiglia D400 (Tabella 4-9), la scheda del costruttore dell'LD19, la revisione più recente delle schede ST (st.com non risponde).
- Le licenze dei depositi SAMURAI e ByteTrack (oggi non rilette).
- Tutto ciò che sta in f7–f10: non letto, e comunque non ancora vagliato dall'arbitro.

## 5. Proposte e dopo

- `fonti-rif2-1`: nei documenti finali la riga su K-010 diventa «due studi discordi: per chi usa il bastone il sonoro costa 22 volte più dell'aptico (Martinez e altri 2014, e l'effetto sparisce nei vedenti bendati); in un altro l'aptico risulta meno intuitivo del sonoro (Lupu e altri 2020, otto persone)». La smentirebbe la lettura del testo intero dei due articoli con un esito diverso dal riassunto.
- `fonti-rif2-2`: nel bilancio della latenza la riga del sensore si chiama «limite superiore del sistema di prova del costruttore (schermo e GPU compresi)», e R7 resta «non risolta» fino alla prova H12. Previsione: la latenza del sensore misurata con H12 sta sotto i 95 ms a 30 fps; la smentisce una misura sopra.
- `fonti-rif2-3`: il risultato di Martinez e altri («not found on blindfolded users») tocca la prova con tre persone bendate prevista per K-010: va scritto fra i limiti di quella prova.
- Dopo: chi unisce i gruppi controlla le chiavi doppie con rif-1, rif-3 e rif-4 (in particolare `cao2023`, `scholler2020`, le schede ST e le pagine RealSense) e tiene, a parità di voce, la verifica più forte.
