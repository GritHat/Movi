Canarino: sciame-canarino-ff229a474629e844

# Consegna `sciame-visione`, f1, corsia A (conservativa)

## 0. Cambi di stato e deviazioni
- **P3: il mio valore atteso era sbagliato.** Avevo scritto che la previsione sotto occlusione «scade» fra 1,5 e 3 s; il calcolo dà 1,0–1,4 s. Le soglie di smentita non sono toccate: l'enunciato regge, il numero è corretto.
- **Deviazioni:** P3 prevedeva numpy (assente): eseguita con la libreria standard. Lo script è nato nello scratchpad della sessione e poi è stato copiato qui (`calcoli_p2_p3_p4.py`). Le pagine in rete sono lette attraverso uno strumento che riassume: i numeri sono quelli riportati, non riletti sull'originale. P5 e P6 non sono eseguibili senza l'hardware: **non risolte**.

## 1. Diagnosi e critiche (ognuna con la prova)
1. **L'ordine «Kalman → vision transformer → decisione» è rovesciato.** Una rete (ViT o CNN) trasforma i pixel in misure (riquadro, maschera, classe); il Kalman consuma misure, non ne produce per la rete. Ordine corretto: sensore → rete + profondità (misura 3D) → associazione → Kalman → decisione. L'unica freccia sensata dal Kalman alla rete è un ritorno: la posizione prevista sceglie la regione o la maschera (così fa SAMURAI dentro SAM 2 [1]). Prova: argomento strutturale più una fonte; non è una misura.
2. **Il «vision transformer» sta in testa alla catena, ed è facoltativo.** Su CPU il riferimento è un rilevatore CNN: YOLO26n 38,9 ms a 640 px in ONNX (1,7 ms su T4), AGPL-3.0 [2]. Un ViT in tempo reale esiste: RF-DETR-N 2,3 ms su T4, Apache 2.0 [3]; su CPU: non verificato. I modelli di fondazione ViT non girano su portatile: SAM 3 30 ms a immagine su H200, video quasi in tempo reale per circa 5 oggetti [4]; SAM 3.1 32 fps su H100 [5]. EdgeTAM: 16 fps su iPhone 15 Pro Max [6]. Vocabolario aperto: YOLOE-26 40,6 AP su LVIS con testo [2]; velocità su CPU: non verificata.
3. **Tre ToF non danno 360°, né una classe (P2: regge).** Multizona 8×8: VL53L8CX 45°×45°, 4 m; VL53L7CX 60°×60° [7]. Tre sensori: 135°–180°; zona larga 0,20–0,26 m a 2 m: presenza sì, classe no. Con tre camere iToF da 120° (Femto Bolt: portata 0,25–2,88 m in modo largo [8]) i 360° chiedono sovrapposizione nulla; interferenza reciproca: non verificata; al sole l'iToF è limitato [9].
4. **Un rilevatore pronto non copre gli ostacoli (P1: regge, 0 su 7).** Muro, porta, gradino, palo, scatola, carrello, cono non sono fra le 80 classi COCO [10]. R2 va coperto dalla geometria; la classe è un attributo in più, e «ostacolo non classificato» è un'uscita valida.
5. **Massa: non osservabile** né dall'immagine né dalla profondità; al più un valore tabellare per classe, da non chiamare stima. **Accelerazione: non utilizzabile fotogramma per fotogramma**: differenza seconda con σ_pos 3 cm a 30 Hz dà σ_a = √6·σ/Δt² ≈ 66 m/s² (calcolo a mano; σ_pos da «< 2 % a 4 m» [11]), contro 1–2 m/s² di un pedone. Osservabili: posizione e velocità, con la loro covarianza.
6. **Reti amodali e tracciatori di punti: fuori dal percorso critico.** Lo stato dell'arte amodale su video è generativo (diffusione [12]) o derivato da SAM 2 [13]; tempi reali: non verificati. Soprattutto, ciò che generano è «previsto», mai «osservato» (R4, R8). R3 chiede la continuità della posizione, non la forma nascosta. TAPNext: 1024 punti a 348 fps, ma su H100 [14].
7. **Quando l'immagine non basta (P4: regge).** Camera sulla testa, rotazione di 120°/s, f ≈ 466 px: sfocatura di 9,8 px a 10 ms e di 32 px a 33 ms; servono circa 2 ms o un otturatore globale (la D455 lo ha su profondità e RGB [17]). Meglio il petto della testa. Poca luce, controluce e profondità non valida devono alimentare R6 con indicatori classici (varianza del laplaciano, frazione di pixel saturi, frazione di profondità valida).
8. **Applicazione.** Per la visione il pezzo più rischioso in 24–48 ore è il moto proprio della camera. La stessa catena serve i due scenari: demo di livello 0 a camera ferma, livello 1 a camera indossata sul petto con moto lento.

## 2. Stati proposti
| Enunciato | Stato |
|---|---|
| 3 ToF multizona coprono 360° | **Smentito** (calcolo sulle schede tecniche) |
| 3 camere iToF coprono 360° in modo utilizzabile | **Non risolto** (interferenza, portata; serve la scheda di sincronizzazione o una prova) |
| Catena Kalman → ViT → decisione | Da invertire: argomento strutturale, **non misurato** |
| Un rilevatore a classi chiuse copre R2 | **Smentito** sulle 7 categorie dichiarate |
| Massa stimabile dai sensori proposti | **Smentito** (non osservabile) |
| Previsione utile quando l'oggetto è nascosto | **Sostenuto da simulazione** per 1–1,5 s; modello di moto assunto, non validato su persone |
| Percorso critico sotto 100 ms su CPU | **Non risolto** (P5) |

## 3. Proposte
### `visione-1` — Geometria prima, semantica a lato; la rete misura, il Kalman stima
- **Enunciato.** Una camera RGB-D frontale (tipo D455: 87°×58°, otturatore globale, IMU [11][17]). Percorso critico a ogni fotogramma: profondità → piano del suolo → punti sopra il suolo → griglia a tre stati (libero osservato, occupato osservato, sconosciuto: mai visto o senza ritorno) → misure 3D. Percorso asincrono: rilevatore «nano» con maschere e tracciatore (BoT-SORT o ByteTrack [15]) per gli elementi mobili; classe e identità si attaccano alle tracce. Ordine: rete → associazione → Kalman → decisione.
- **Guadagno atteso.** R2 senza classi; R1 con classi note (persona, veicolo); R7 senza GPU (circa 25 Hz il solo rilevatore, dato pubblicato); R8 per costruzione: «sconosciuto» non è «libero».
- **Vincoli.** Interni o ombra; 0,6–6 m; vetro e superfici nere restano «sconosciuto»; fuori dagli 87° è «non osservato» (eventuali ToF multizona laterali: sola presenza). AGPL-3.0, oppure RF-DETR in Apache 2.0.
- **Chi la prova.** `sciame-tempo-reale` (P5), `sciame-nuvole-punti` (suolo e griglia), `sciame-avversario` (vetro, oggetti bassi).
- **Falsificatore (5 min).** P1 eseguita: regge. P5 sul portatile: smentita oltre 80 ms. Con la camera: 5 oggetti fuori da COCO; atteso 5 su 5 dalla profondità e al più 1 su 5 dal rilevatore.
- **Se l'ipotesi di fattibilità è falsa** (niente camera di profondità): webcam e profondità monoculare (Depth Anything 3 small: 6 fps in PyTorch e 43 con TensorRT su Orin NX, dati della comunità [16]); le distanze diventano «stimate» e va dichiarato.

### `visione-2` — L'occlusione è uno stato della traccia, deciso dalla profondità, con scadenza
- **Enunciato.** Ogni traccia esce come OSSERVATO, PREVISTO o SCONOSCIUTO. Quando manca il rilevamento si guarda la profondità lungo il raggio verso la posizione prevista: più vicina della previsione (meno un margine) → c'è un occlusore → PREVISTO, solo predizione, ellisse che cresce; uguale o più lontana → la previsione è contraddetta → traccia chiusa; non valida → SCONOSCIUTO. PREVISTO scade quando il raggio al 95 % supera 1 m (P3: 1,0–1,4 s per un pedone); poi la zona dietro l'occlusore è «possibile presenza», mai libera. Al ritorno: cancello di Mahalanobis più aspetto (ReID di BoT-SORT [15]). Nessuna rete amodale o generativa.
- **Guadagno atteso.** R3, R4, R6, R8 al costo di una lettura di profondità per traccia. In demo: riquadro pieno → ellisse tratteggiata → zona «?» → riaggancio con la stessa identità. Misure: identità conservata su N passaggi, errore al ritorno dentro l'ellisse al 95 %, tempo di riaggancio.
- **Vincoli.** Profondità allineata all'RGB; occlusori trasparenti o sottili; camera ferma o moto proprio compensato; chi si ferma dietro il pannello scade a SCONOSCIUTO (voluto).
- **Chi la prova.** `sciame-kalman` (rumore di processo, coerenza), `sciame-tracciamento` (riassociazione, scambi d'identità), `sciame-avversario` (due persone che si incrociano dietro il pannello).
- **Falsificatore (5 min).** P3 eseguita: soglie non toccate. P6 con la camera: 20 passaggi, smentita a 15 o meno stati giusti.
- **Se l'ipotesi è falsa** (niente profondità): prova di visibilità con le maschere (la regione prevista cade sotto la maschera di un altro oggetto); più debole.

## 4. Che cosa propongo dopo
Eseguire P5 e P6 nella prima ora dell'hackathon; far fissare a `sciame-kalman` il rumore di processo su passaggi registrati; chiedere a `sciame-sensori` la decisione sui ToF laterali; usare SAM 3 solo fuori linea per le annotazioni di riferimento, e solo se l'utente concede una GPU.

## Fonti
[1] https://arxiv.org/abs/2411.11922 · [2] https://docs.ultralytics.com/models/yolo26/ · [3] https://github.com/roboflow/rf-detr · [4] https://arxiv.org/html/2511.16719v2 · [5] https://ai.meta.com/blog/segment-anything-model-3/ · [6] https://arxiv.org/abs/2501.07256 · [7] https://www.pololu.com/product/3419 e https://www.st.com/resource/en/datasheet/vl53l8cx.pdf · [8] https://www.orbbec.com/products/femto-bolt/ · [9] https://isprs-annals.copernicus.org/articles/X-1-W1-2023/17/2023/ · [10] https://raw.githubusercontent.com/ultralytics/ultralytics/main/ultralytics/cfg/datasets/coco.yaml · [11] https://store.intelrealsense.com/buy-intel-realsense-depth-camera-d455.html · [12] https://arxiv.org/abs/2412.04623 · [13] https://arxiv.org/abs/2604.20748 · [14] https://arxiv.org/abs/2504.05579 · [15] https://docs.ultralytics.com/modes/track/ · [16] https://discourse.openrobotics.org/t/release-gerdsenais-depth-anything-3-ros2-wrapper-with-real-time-tensorrt-for-jetson/52364 · [17] https://www.adorama.com/in82635dsd45.html (otturatore globale; la pagina Intel [11] dà campo, portata ed errore)
