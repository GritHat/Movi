Canarino: sciame-canarino-ff229a474629e844

# Consegna di sciame-tracciamento — f1, corsia A

## 0. Cambi di stato e regole

- **Quattro mie previsioni su undici sono smentite** (dettaglio in `PREVISIONI.md`, scritte alle 13:05:30, prove dalle
  13:06:46). La più importante: l'orizzonte onesto della previsione puntuale è **circa 1,2 s**, non 1,5–3 s.
- Regole violate: nessuna che io sappia. numpy mancava: ho riscritto le prove in Python puro, senza installare niente.
- Oracolo di tutte le misure: simulazione mia (`prove/simA.py`, `simA2.py`, `simB.py`, `simB2.py`). Condivide con le
  proposte autore e modello; nessun sensore reale, un solo oggetto. Gli stati sotto valgono «in simulazione».

## 1. Diagnosi (critiche, ciascuna con la prova)

1. **La bozza non ha un componente per R3/R4/R6.** Chiude le tracce per tempo («scadenza dei tracciati rimasti non
   osservati troppo a lungo», riga 2272), ha `confidence` e `lastSeenNs` (2241–2245) ma nessuno stato «previsto»
   in uscita; la parola «occlus…» non compare mai nelle righe 1998–3800 (`grep -c -i occlus`: 0).
2. **La scadenza a tempo fisso fallisce nei due versi.** Simulato: 1 s tiene l'identità nello 0% dei passaggi dietro
   un pannello di 2 m; 5 s la tiene nel 75–77% se il pedone si ferma 2–4 s, e lascia un fantasma per 2,0 s dove il
   sensore vede vuoto. Il valore di 1 s non è arbitrario: `track_buffer: 30` fotogrammi è il predefinito di ByteTrack
   in Ultralytics ([bytetrack.yaml](https://raw.githubusercontent.com/ultralytics/ultralytics/main/ultralytics/cfg/trackers/bytetrack.yaml), letto oggi per intero).
3. **I tracciatori pronti danno l'associazione, non la continuità dichiarata.** Ultralytics ne offre oggi sei
   (BoT-SORT, ByteTrack, OC-SORT, Deep OC-SORT, FastTracker, TrackTrack; il predefinito è TrackTrack; la
   re-identificazione è spenta in partenza: [documentazione](https://docs.ultralytics.com/modes/track/), letta oggi).
   Lavorano nel piano immagine. Che non espongano covarianza né tracce «previste» in uscita: non verificato.
   OC-SORT nasce proprio dall'errore che il Kalman accumula in occlusione ([arXiv 2203.14360](https://arxiv.org/abs/2203.14360)).
   Licenza AGPL-3.0 (intestazione del file): da portare all'analista normativo.
4. **I modelli grandi non servono qui.** SAM 3 regge il tempo quasi reale per circa 5 oggetti su una GPU H200
   ([arXiv 2511.16719](https://arxiv.org/abs/2511.16719), da riassunto di ricerca): fuori dall'ipotesi portatile o
   Jetson. I tracciatori appresi di fine corsa (es. MATR su [DanceTrack](https://arxiv.org/abs/2111.14690)) chiedono
   addestramento: prestazioni attuali non verificate. Lo schema da copiare è AB3DMOT, Kalman 3D più ungherese
   ([arXiv 2008.08063](https://arxiv.org/abs/2008.08063)); SimpleTrack isola la gestione della vita delle tracce come
   modulo a sé ([arXiv 2111.09621](https://arxiv.org/abs/2111.09621)).
5. **La catena «Kalman → vision transformer → decisione» è nell'ordine sbagliato per il tracciamento.** Il filtro
   consuma rilevamenti: sensore → rilevamento → posizione 3D in un riferimento fisso (moto proprio tolto) →
   associazione → Kalman → vita delle tracce → decisione. Senza riferimento fisso una rotazione dell'utente sembra
   moto dell'oggetto (non misurato qui).
6. **Massa e accelerazione.** La massa non entra in nessuna porta né previsione: al tracciatore non serve. In
   simulazione la velocità costante con rumore gonfiato basta a calibrare la porta; l'IMM della bozza (3315–3460)
   non è necessario per la copertura. Se stringa la regione: non risolto.
7. **HOTA e IDF1 non sono la misura giusta per la demo.** Chiedono sequenze annotate
   ([HOTA, arXiv 2009.07736](https://arxiv.org/abs/2009.07736); [TrackEval](https://github.com/JonathonLuiten/TrackEval)).
   In 24–48 ore si misura una scena a copione (§5).

## 2. Stati proposti

| Enunciato | Stato |
|---|---|
| Velocità costante con q = 0,5 m²/s³: la porta al 99% contiene la ricomparsa fino a 3 s | sostenuto dai dati (98,6–99,9%, N = 3000 per punto, pedone che si ferma e svolta) |
| Taratura «liscia» q = 0,05: incertezza dichiarata troppo stretta | sostenuto dai dati (copertura 79–89% contro 99% nominale) |
| Orizzonte onesto 1,5–3 s | **smentito**: errore vero al 95% oltre 1,5 m già a circa 1,2 s |
| Basta una scadenza fissa | **smentito** (punto 2) |
| Basta guardare se la media prevista è in ombra | **smentito**: 91% in transito, 0% se il pedone si ferma |
| Evidenza negativa sulla massa d'incertezza | sostenuto dai dati, indipendenza debole (il modello ha un modo «sosta» come lo scenario) |
| Identità corretta con due o più oggetti che si incrociano dietro l'ostacolo | non risolto: lo decide la prova 5c |

## 3. Proposta `tracciamento-1` — ciclo di vita a quattro stati con orizzonte dichiarato

- **Enunciato.** Ogni traccia è in uno di quattro stati, e lo stato esce insieme alla posizione:
  **tentativa** (rilevamento non associato; non genera indicazioni proprie, l'ostacolo resta comunque nella mappa di
  occupazione); **confermata** (3 rilevamenti su 5: «osservato»); **in volo cieco** (nessuna misura: previsione a
  velocità costante con q circa 0,5, etichetta «previsto», raggio al 95% che cresce); **persa** (raggio oltre 1,5 m
  o tetto di tempo: niente più posizione, solo «zona incerta», mai «libero»). Riaggancio: porta di Mahalanobis al 99%
  e assegnazione ungherese; se in porta c'è più di un candidato decidono classe, dimensione e aspetto; se non
  decidono, identità nuova e lo si dice.
- **Guadagno atteso.** R3, R4 e R6 hanno un componente nominato; costo di calcolo trascurabile (R7).
- **Vincoli.** Riferimento fisso; q e i due tetti vanno ritarati su camminate vere; a 3 s la porta ha raggio circa
  7,3 m (calcolo da sigma 2,41 m), quindi con più oggetti la sola geometria non identifica.
- **Chi la prova.** sciame-kalman (coerenza su registrazioni vere), sciame-validazione, sciame-avversario.
- **Falsificatore (fatto, 3 s di CPU).** `prove/simA.py`: smentita se copertura < 90% a T ≤ 3 s. Esito: minimo
  98,6%, regge. Smentite invece le mie soglie su orizzonte ed errore a 1 s (0,53 m contro ≤ 0,5).

## 4. Proposta `tracciamento-2` — chiudere per causa, non per tempo

- **Enunciato.** Per ogni traccia non osservata si chiede alla mappa di profondità perché: (a) davanti alla
  posizione prevista c'è una superficie più vicina → **nascosto**, l'esistenza non cala; (b) fuori campo o portata
  → **fuori campo**; (c) profondità non valida → **sensore cieco**, si segnala la perdita di affidabilità (R6);
  (d) il sensore vede attraverso e non c'è niente → evidenza negativa. Il conto va fatto sulla massa d'incertezza
  (filtro di Bernoulli, circa 200 particelle per traccia in volo cieco), non sul punto medio.
- **Guadagno atteso.** Simulato: identità tenuta nel 100% dei transiti e delle soste (contro 0% e 75–100% delle
  scadenze fisse), fantasma in zona visibile 0,06–0,07 s (contro 2,0 s).
- **Vincoli.** L'ombra reale viene da una profondità rumorosa; serve un tetto (10 s) dopo cui la traccia diventa
  «zona incerta»; il modo «sosta» va giustificato.
- **Chi la prova.** sciame-avversario (ombra sbagliata di 20 cm, due oggetti), sciame-nuvole-punti, sciame-validazione.
- **Falsificatore (fatto, 20 s di CPU).** `prove/simB.py`: smentita se tenuta < 80% con sosta, o se il punto medio
  da solo supera l'80%. Esito: 100% e 0%, regge.

## 5. Demo che misura R3 e R4, e che cosa mostrare

Pannello largo 2 m a 2 m dal sensore, persona che attraversa a 4 m, 20 ripetizioni per variante, sensore fermo.
- **5a transito, 5b sosta di 2–4 s dietro il pannello:** stessa identità alla ricomparsa in almeno 18 su 20;
  ricomparsa dentro il raggio dichiarato in almeno 18 su 20; nel registro nessun fotogramma «osservato» senza misura.
- **5c due persone che si incrociano dietro il pannello:** si contano gli scambi d'identità (previsione: è il caso
  che rompe la sola geometria).
- **5d la persona esce da dietro il pannello senza riapparire:** mai «libero»; dopo il tetto, «zona incerta».
- **All'utente:** osservato → direzione e distanza; previsto (fino a circa 1,2 s) → segnale diverso, che si allarga;
  oltre → «qualcosa di nascosto a sinistra, non lo vedo da N secondi».

## 6. Che cosa propongo dopo

1. Decidere 5c con due oggetti in simulazione (10 minuti) prima di promettere l'identità negli incroci.
2. Scegliere il rilevatore sapendo che al tracciatore servono posizioni a terra a 10 Hz o più con sigma nota.
3. Applicazione: con il sensore fisso (monitoraggio industriale) il moto proprio non c'è e la demo è più solida;
   indossato, l'odometria diventa il primo rischio del tracciamento. Giudizio non misurato: lo decidono
   sciame-slam e l'utente.
4. Se l'ipotesi 24–48 ore è falsa per difetto: resta `tracciamento-1` con scadenza per causa sul punto medio e si
   dichiara il limite della sosta; con più tempo, taratura di q su dati veri e re-identificazione per aspetto.
