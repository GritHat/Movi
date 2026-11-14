# FONTI — sciame-ricercatore, f1, corsia A (consultate il 14 novembre 2026)

Legenda. **A** = pagina aperta davvero e letta con lo strumento di lettura (che riassume: le citazioni fra «» sono
quelle che lo strumento ha riportato come testuali). **R** = vista solo nel riassunto del motore di ricerca, NON
aperta: da far verificare al curatore delle fonti. **M** = solo dalla mia memoria, non verificato oggi.

## Sensori
- F1 [A] Orbbec Femto Bolt, pagina prodotto: profondità «H 120° V 120° (WFOV), H 75° V 65° (NFOV)»; portata WFOV
  0,25-2,88 m (binned) e 0,25-2,21 m; NFOV 0,5-3,86 / 0,5-5,46 m; ambiente «Indoor». Prezzo non mostrato.
  https://www.orbbec.com/products/tof-camera/femto-bolt/
- F2 [R] ST VL53L7CX: 60° x 60° (90° in diagonale), 4x4 o 8x8 zone, fino a 350 cm. La pagina ST è andata in timeout;
  la portata in luce ambiente non è verificata. https://www.st.com/en/imaging-and-photonics-solutions/vl53l7cx.html
- F3 [A] Luxonis, «ToF Depth Perception»: 640x480, 20 cm-5 m, «<1% indoors, <2% outdoors»; fra i problemi elenca
  «Issues when using multiple ToFs (interference)»; dice che lo stereo attivo soffre al sole. Fonte del costruttore.
  https://docs.luxonis.com/hardware/platform/depth/ToF-depth
- F4 [R] Confronto sul campo di camere stereo (Kiwibot, blog): D435i degradata al sole oltre 2 m, D435f molto
  migliore, OAK-D Pro rumorosa. https://hackernoon.com/thinking-of-buying-stereo-cameras-read-this-product-comparison
- F5 [R] ISPRS Annals 2023: l'uso esterno del ToF resta limitato dall'interferenza solare.
  https://isprs-annals.copernicus.org/articles/X-1-W1-2023/17/2023/

## Ausili per la mobilità e feedback
- F6 [A, solo abstract] Kozlov et al., «GuideTouch: An Obstacle Avoidance Device with Tactile Feedback for Visually
  Impaired», arXiv 2601.13813 (gennaio 2026): due ToF allineati in verticale, quattro attuatori; 92,9% di
  riconoscimento dei motivi primari (22 partecipanti), 93,75% con 14 utenti con disabilità visiva.
  [R] dal testo intero: 28 intervistati, sostituire il bastone è «highly undesirable».
  https://arxiv.org/abs/2601.13813
- F7 [R] Martinez et al., ICCHP 2014: per chi usa il bastone il feedback sonoro dà un carico NASA-TLX 22 volte
  maggiore dell'aptico; l'effetto non c'è nei vedenti bendati. Il PDF ha dato 404: NON aperta.
  https://cvhci.iar.kit.edu/~dkoester/publications/martinezICCHP2014tlx.pdf
- F8 [R] Studio «Sound of Vision» (2020, 8 partecipanti ciechi): stimoli aptici meno intuitivi di quelli sonori; il
  dispositivo aumenta il carico cognitivo. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7602506/
- F9 [R] Romlay et al. 2021, rassegna di 70 articoli: valutazioni con persone con disabilità visiva solo nel 22,9%
  dei casi; l'1,4% arriva alla produzione. https://beei.org/index.php/EEI/article/view/3055
- F10 [R] Xu et al. 2023, IEEE Access, rassegna PRISMA di 89 studi sugli ausili indossabili anti-ostacolo: efficacia
  e sicurezza sono la prima preoccupazione degli utenti. https://doaj.org/article/69f50f5aa56e4c9fb3f54d8d3d05cf83
- F11 [R] Giudice et al. 2008 / Klatzky et al. 2006: la guida con suono spazializzato regge un compito secondario
  meglio del linguaggio spaziale (vedenti bendati).
  https://umaine.edu/vemi/publication/environmental-learning-without-vision-effects-cognitive-load-interface-design
- F12 [R] Occhiali Ally Solos (Envision + Solos): elaborazione su telefono e servizi remoti; gli sviluppatori
  sconsigliano di usarli come strumento principale di navigazione. Stampa, fonte secondaria.
  https://www.gulf-times.com/article/718327/opinion/smart-glasses-and-ai-advances-find-purpose-among-blind-users
- F13 [R, citato dalla bozza] NavWear 2025 (RGB-D + aptico, zaino). https://pubmed.ncbi.nlm.nih.gov/40100749/
- Non trovati e non verificati: Glidance Glide, biped NOA (nessun risultato utile nella ricerca).

## Tracciamento, occlusioni, previsione
- F14 [A, PDF, Tabella I] Schöller, Aravantinos, Lay, Knoll, «What the Constant Velocity Model Can Teach Us About
  Pedestrian Motion Prediction», RA-L / ICRA 2020, arXiv 1903.07933. Numeri in PREVISIONI.md, esito P2(a).
  https://arxiv.org/abs/1903.07933
- F15 [A] ByteTrack, deposito ufficiale: licenza MIT; «30 FPS running speed on a single V100 GPU» (rilevatore
  compreso). https://github.com/FoundationVision/ByteTrack
- F16 [R] OC-SORT (Cao et al., CVPR 2023): l'errore del Kalman si accumula durante l'occlusione; modulo ORU al
  riaggancio; oltre 700 FPS su una CPU date le rilevazioni; licenza MIT (anche filterpy), YOLOX Apache 2.0.
  https://github.com/noahcao/OC_SORT e https://arxiv.org/abs/2203.14360
- F17 [A, solo abstract] Ravi et al., «SAM 2: Segment Anything in Images and Videos», arXiv 2408.00714: «streaming
  memory for real-time video processing»; nessun FPS né hardware nell'abstract. Licenza: [M] non verificata oggi.
  https://arxiv.org/abs/2408.00714
- F18 [A] EdgeTAM, deposito ufficiale: Apache 2.0; «16 FPS on iPhone 15 Pro Max without quantization»; 150,9 FPS su
  A100. [R] dall'articolo: il SAM 2 più piccolo va a circa 1 FPS sullo stesso telefono.
  https://github.com/facebookresearch/EdgeTAM e https://arxiv.org/abs/2501.07256
- F19 [A] SAMURAI, deposito ufficiale: Apache-2.0; «The existing code doesn't support live/streaming video».
  https://github.com/yangchris11/samurai
- F20 [A, solo abstract] Hsieh et al., «TAO-Amodal», arXiv 2312.12433: «existing methods, even when adapted for
  amodal tracking, struggle to detect and track objects under heavy occlusion»; la messa a punto dà +2,1% e +3,3%.
  https://arxiv.org/abs/2312.12433
- F21 [R] TinySAM 2: 25,6 FPS, hardware non identificato. Il link è quello che la ricerca ha messo accanto al
  riassunto: che sia proprio questo articolo NON è verificato. https://arxiv.org/abs/2605.18013

## Incertezza calibrata
- F22 [A, solo abstract] Kuzucu, Oksuz, Sadeghi, Dokania, «On Calibration of Object Detectors: Pitfalls, Evaluation
  and Baselines», arXiv 2405.20459 ([R] ECCV 2024): i calibratori a posteriori (Platt, regressione isotonica) sono
  «much more powerful and effective than the recent train-time calibration methods»; D-DETR con regressione
  isotonica batte Cal-DETR di oltre 7 punti di D-ECE su COCO. https://arxiv.org/abs/2405.20459
- F23 [R] Munir et al., CVPR 2023: i metodi a posteriori chiedono dati di validazione messi da parte e dipendono
  dall'architettura. https://openaccess.thecvf.com/content/CVPR2023/papers/Munir_Bridging_Precision_and_Confidence_A_Train-Time_Loss_for_Calibrating_Object_CVPR_2023_paper.pdf
- F24 [R] Previsione conforme a due passi per i riquadri di rilevamento. https://arxiv.org/pdf/2403.07263
- [M] Prove di coerenza del filtro (NEES, NIS) come misura standard della calibrazione di uno stimatore: non
  verificato oggi con una fonte.

## Monitoraggio industriale e aerospaziale
- F25 [A, primi 100 000 caratteri] Plastropoulos, Avdelidis, Zolotas, «Techno-economic analysis for smart hangar
  inspection operations through sensing and localisation at scale», The Aeronautical Journal 130(1346), 2026, DOI
  10.1017/aer.2025.10116: «no studies have presented a holistic side-by-side evaluation of MoCap, UWB and
  vision-based solutions»; poca evidenza sulla robustezza alla «dynamic occlusion».
  https://www.cambridge.org/core/product/288076BC0C6F624BBBBD0A752587762E/core-reader
- F26 [R] Sorveglianza di velocità e separazione (ISO/TS 15066): la distanza protettiva si calcola con l'incertezza
  di misura e la latenza. https://mdpi.com/2218-6581/14/4/41
- F27 [R] Brevetto USA 11846916: voxel occupati, non occupati o sconosciuti oltre un'occlusione. È una
  rivendicazione, non un metodo validato. https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11846916
- F28 [R] Rassegna sul rilevamento di detriti (FOD) sulle piste, Remote Sensing 2025: pochi dati, calcolo pesante.
  https://www.mdpi.com/2072-4292/17/2/225/htm

## Massa dalla visione
- F29 [A, HTML] Lee et al., «Physically Guided Visual Mass Estimation from a Single RGB Image», arXiv 2601.20303
  ([R] IJCAI 2026): Tabelle 1 e 2, numeri in PREVISIONI.md, esito P3. https://arxiv.org/html/2601.20303v1
- F30 [R] Standley et al. 2017, image2mass (circa 150 000 prodotti Amazon): l'articolo originale non è stato aperto.

## Ingressi del progetto letti
- regole_challenge.md (per intero); CONTRATTO.md; TASK.md; bozza: indice dei titoli da riga 1998 e righe
  2091-2118, 2348-2376, 2543-2575, 2890-2945 (non tutta).
