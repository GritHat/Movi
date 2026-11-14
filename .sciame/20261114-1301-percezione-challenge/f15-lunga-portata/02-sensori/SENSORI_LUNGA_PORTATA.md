# Sensori a lunga portata: specifica dell'hardware simulato

`sciame-sensori`, f15-lunga-portata/02-sensori, 15 novembre 2026 (orologio della macchina). Parametri leggibili da
programma: `parametri_lunga_portata.json` (13 sensori, 124 campi con fonte, di cui 57 «ipotesi»; conteggio fatto con
`python3 -I` sul file). **Niente è provato su un sensore fisico: tutto è scheda tecnica, norma, articolo o conto.**

## 1. Cambi di stato e regole violate

- **Smentita sens-P3:** il criterio dei pixel dà 13 km per un drone di 0,3 m, non 1–5 km (vedi § 5).
- **Smentita sens-P4:** una scheda pubblica dichiara 320 m al 10 % (Livox Tele-15), ma con campo di soli 14,5°.
- **Schede non lette:** radar 4D ARS 548 (errore di certificato) e portate dell'EchoGuard (in un'immagine). I loro
  numeri sono «ipotesi», da ricontrollare prima di citarli. L'articolo sul progetto SMART per i treni non si è aperto
  (errore 403): non verificato.
- **Il 46 % dei campi è «ipotesi»** (57 su 124): tutte le probabilità di rilevamento, i falsi allarmi, le latenze e i
  costi. Nessuna scheda aperta oggi li dichiara, salvo i falsi punti del Tele-15 (< 0,01 %).
- **Regole:** due file scaricati per errore (pagine d'errore in HTML al posto dei PDF) sono stati cancellati dalla mia
  cartella. Il LiDAR spetta all'esperto hardware di LiDAR: qui c'è solo ciò che la consegna chiede. La data
  dell'orologio (15 novembre, 00:01) è un giorno dopo quella della consegna.

## 2. I sensori, in breve

Fonti e campi completi nel JSON; «(i)» segna un'ipotesi. Schede aperte oggi: Robin IRIS, Terma SCANTER 5000, Hesai
AT128, Livox Tele-15, 14 CFR 91.227 e 89.310, OSDaR23 (arXiv:2305.03001), criteri di Johnson.

| Sensore (esemplare) | Portata | Campo | Errore di misura | Rivisita | Costo (i) |
|---|---|---|---|---|---|
| LiDAR a campo largo (Hesai AT128) | 210 m al 10 % | 120° × 25,4° | 0,1° × 0,2°; 3 cm (i) | 0,1 s (i) | 1 k€ |
| LiDAR tele (Livox Tele-15) | 320 m al 10 %, 500 m al 50 % | 14,5° × 16,2° | 2 cm; < 0,03° | 0,1 s | 1 k€ |
| Radar 4D per veicoli (ARS 548) | 300 m (fonte secondaria) | 120° (i) | 0,22 m; 1,2°; 0,1 m/s (i) | 0,05 s (i) | 0,5 k€ |
| Radar per droni (Robin IRIS) | 1,1–7,6 km secondo il drone; strumentata 5 o 12 km | 360° × 60° | 0,6 m; 0,6–0,75°; 1° in elevazione | 1 s | 200 k€ |
| Radar del movimento a terra (Terma SCANTER 5502) | 5 km per 1 m² (i); 9,6 km in avvicinamento | 360°, senza quota | cella di 3 m; 0,29° (conto) | 1 s | 1 M€ |
| ADS-B (14 CFR 91.227) | orizzonte del ricevitore | tutto, solo chi trasmette | < 92,6 m; < 10 m/s | ≤ 1 s; latenza ≤ 2 s | 0,1 k€ |
| Identificazione remota (14 CFR 89.310) | ~1 km (i) | tutto, solo chi trasmette | 30,5 m (95 %); quota 45,7 m | ≤ 1 s; latenza ≤ 1 s | 0,1 k€ |
| Camera EO, 12 MP, 300 mm (i) | drone 13 km, limite geometrico; ~2 km pratica (i) | 2,7° | 1 pixel = 11,5 µrad; **nessuna distanza** | 0,1 s | 5 k€ |
| Camera termica 640 × 480, 100 mm (i) | drone 1,2 km, limite geometrico | 4,4° | 120 µrad; nessuna distanza | 0,1 s | 10 k€ |
| Acustico passivo | 300–500 m al più | 105° (i) | solo direzione | — | 20 k€ |
| Radiofrequenza passivo | 1–5 km in città (non aperta) | 360° | presenza, a volte direzione | — | 30 k€ |

**Radar per droni: scala con la sezione radar.** La scheda IRIS dà portate per classe di drone, senza sezione radar.
Attribuendo 0,01 m² (i) al drone C1 da 0,9 kg visto a 3100 m, R(σ) = 3100 · (σ/0,01)^¼:

| Bersaglio | R dall'equazione | R utile (strumentata 12 km) | Anticipo alla velocità tipica |
|---|---|---|---|
| Multirotore piccolo, 0,01 m² | 3,1 km | 3,1 km | 155 s a 20 m/s |
| Velivolo leggero, 1 m² | 9,8 km | 9,8 km | 163 s a 60 m/s |
| Aereo di linea, 100 m² | 31 km | 12 km | 171 s a 70 m/s |

Controllo di coerenza sulla stessa scheda: le altre tre righe implicano 1,6·10⁻⁴ m² (0,249 kg), 0,02 m² (2,9 kg) e
0,36 m² (52 kg), valori plausibili ma non confrontati con misure. Indipendenza: stessa scheda, stessa ipotesi sul
riferimento. Il drone da 0,249 kg si vede solo entro 1,1 km: 55 s a 20 m/s.

**Probabilità di rilevamento (modello proposto, i).** Swerling 1: Pd = Pfa^(1/(1+SNR)), con SNR ∝ σ/R⁴. Ponendo
Pd = 0,5 alla portata dichiarata e Pfa = 10⁻⁶, SNR di riferimento 18,9 (12,8 dB). Le schede non dicono a quale Pd si
riferisce la loro portata: è l'ipotesi che pesa di più sull'intero modello.

**Cooperativi.** ADS-B: posizione almeno una volta al secondo in volo o in movimento a terra, ogni 5 s da fermo;
NACp < 0,05 miglia nautiche (92,6 m), NIC < 0,2 miglia (370 m), latenza totale ≤ 2 s. Identificazione remota: 100
piedi al 95 %, un messaggio al secondo, latenza ≤ 1 s. Sono norme degli Stati Uniti; quelle europee non sono state
aperte (non verificato). **Chi non coopera non compare**: per il sistema, il silenzio non è un'osservazione.

**Camere.** Criteri di Johnson (50 %): 1, 4 e 6,4 coppie di linee, cioè 2, 8 e 12,8 pixel. Con 300 mm e passo di
3,45 µm (i): drone di 0,3 m rilevato a 13 km, riconosciuto a 3,3 km; aereo di 35 m rilevato ben oltre l'orizzonte.
È un limite superiore geometrico: contrasto, foschia e rivelatore automatico lo riducono, di quanto non è verificato.
La camera non misura la distanza e guarda 2,7°: serve un altro sensore che le dica dove puntare.

**Treni.** OSDaR23 (Amburgo, 2021) monta 3 Tele-15, 1 Pandar64, 2 lidar corti, 6 camere a colori, 3 termiche e un
radar Navtech a 4 Hz, sincronizzati con PTP sull'istante di acquisizione. L'articolo chiede dati «oltre parecchie
centinaia di metri» e riporta la distanza mediana a cui un macchinista vede un ostacolo: da meno di 60 m a più di
750 m. Il lidar a 320 m dà 7,2 s a 160 km/h; la frenata ne chiede circa 44 (1 m/s², i): **sul treno il sistema può
avvisare, non garantire l'arresto**.

## 3. Quale sensore per quale classe e distanza

| Classe | Fino a ~300 m | 0,3–3 km | 3–12 km | Oltre |
|---|---|---|---|---|
| Auto (36 m/s) | LiDAR largo + radar 4D: 5,8–8,3 s | nessuno a bordo | — | — |
| Treno (44 m/s) | LiDAR tele + radar | camera EO e termica (senza distanza) | — | — |
| Drone piccolo (20 m/s) | acustico, radar a pannello | radar per droni; EO puntata; radio e identificazione remota se emette | solo droni > 2,9 kg | — |
| Velivolo leggero (60 m/s) | radar a terra, se è al suolo | radar per droni, ADS-B | radar fino a 9,8 km; ADS-B | ADS-B |
| Aereo di linea (70 m/s) | radar a terra, ADS-B | radar a terra, ADS-B | radar fino a 12 km; ADS-B | ADS-B |

Per aerei e droni, il caso centrale: **radar per droni + ADS-B e identificazione remota + una camera puntata dal
radar**. Il radar vede chi non coopera, i cooperativi danno l'identità, la camera conferma. Nessuno dei tre copre
da solo.

## 4. Che cosa vuol dire «non osservato», sensore per sensore

Il sistema deve dichiarare, per ogni zona e ogni istante, quale di queste cinque cause vale. Nessuna è «libero».

1. **Fuori campo.** LiDAR tele e camere guardano 3–15°; il radar per droni non vede sopra 60° di elevazione; il
   radar a terra non ha quota.
2. **Senza linea di vista.** Dietro un hangar, un aereo fermo, una curva del binario; sotto l'orizzonte radar: con
   antenna a 10 m, un bersaglio al suolo sparisce oltre 13 km, uno a 120 m di quota oltre 58 km (conto).
3. **Sotto la soglia.** È il caso nuovo rispetto alla camera di profondità: la zona è in campo e in vista, ma il
   sensore non vedrebbe *quel* bersaglio. Oltre 1,1 km il radar non vede un drone da 0,249 kg: la zona è «osservata
   per un aereo» e «non osservata per un drone piccolo». **L'osservato dipende dalla classe**, e la classe
   peggiore (la più piccola possibile) decide: nessuna etichetta può ridurre un avviso.
4. **Fra due rivisite.** Con 1 s di rivisita un aereo a 70 m/s si sposta di 70 m, più di cento volte l'errore in
   distanza (0,6 m); con i 4 s dei radar d'aeroporto, 280 m. È la voce dominante dell'incertezza.
5. **Chi non coopera o non emette.** Per ADS-B, identificazione remota e radiofrequenza l'assenza di messaggi non
   osserva niente. Per il radar Doppler: un bersaglio fermo o che attraversa a velocità radiale nulla.

A parte sta la **perdita di affidabilità**: NACp o NIC dell'ADS-B che peggiorano, pioggia forte in banda X, nebbia per
le camere, sole a 100 klx per il lidar. Il dato arriva ma vale meno, e va detto.

## 5. Esito delle previsioni (scritte alle 00:01:05, prima delle schede: `PREVISIONI.md`)

| Previsione | Esito | Prova |
|---|---|---|
| P1: radar a 0,01 m² fra 0,5 e 5 km | regge | scheda IRIS: 1,1–3,7 km per droni da 0,25 a 2,9 kg |
| P2: a 100 m² la portata è limitata dallo strumento | regge | 31 km dal conto contro 12 km strumentati |
| P3: EO rileva 0,3 m entro 1–5 km | **smentita** | 13 km con 2 pixel; e il campo è 2,7°, non ≤ 2° |
| P4: nessun LiDAR oltre 300 m al 10 % | **smentita** | Tele-15: 320 m al 10 % |
| P5: radar 4D ≥ 250 m e ≤ 2° | non risolta | scheda non apribile |
| P6: ADS-B a ~2 Hz, < 93 m | regge in parte | 92,6 m sì; la norma dice «almeno 1 al secondo» |
| P7: fra due rivisite ≥ 70 m | regge | rivisita di 1 s su IRIS e SCANTER |

Notato dopo, non previsto: l'osservato dipende dalla classe (§ 4, punto 3).

## 6. Proposte

- **sensori-1, copertura per classe.** La mappa dell'osservato si calcola per la sezione radar più piccola ammessa
  (0,01 m², o 1,6·10⁻⁴ m² se si ammettono i droni sotto 250 g). *Previsione:* l'area «osservata per un drone
  piccolo» è meno del 10 % di quella «osservata per un aereo» (rapporto dei raggi 3,1/12, al quadrato: 6,7 %).
  *Smentita:* un rapporto sopra il 10 % nel simulatore.
- **sensori-2, avviso dal silenzio cooperativo.** Una traccia radar senza messaggio ADS-B o d'identificazione
  remota associato entro 3 s si dichiara «non cooperante»; non il contrario. *Smentita:* un caso simulato in cui
  l'assenza di messaggi spegne un avviso.
- **sensori-3, zona fra due rivisite.** Il predittore esistente si usa con v_max di classe e T = 1 s: raggio di
  70–100 m per gli aerei. *Smentita:* copertura sotto la precisione dichiarata sui dati pubblici di traiettoria.

## 7. Che cosa propongo dopo

Riaprire le schede dell'ARS 548 e dell'EchoGuard; cercare una misura pubblica della sezione radar di un multirotore
in banda X per togliere l'ipotesi più pesante; chiedere all'esperto hardware di LiDAR di confermare i due LiDAR;
far decidere all'arbitro la Pd di riferimento (0,5 o 0,9), che pesa molto: nel modello Swerling 1 la portata a Pd = 0,9 è il 62 % di quella a Pd = 0,5 (SNR 130 contro 18,9;
rapporto alla potenza ¼).

**Dati scaricati** (`scaricati/`, non fidati, non eseguiti, 6 MB in tutto): `robin_iris_product_sheet_042026.pdf`
e `terma_scanter5000_smr_dec2021.pdf`, materiale dei costruttori, tutti i diritti riservati, tenuti solo per
consultazione e da non ridistribuire.
