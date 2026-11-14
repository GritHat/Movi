Canarino: sciame-canarino-fe0856355f521597

# Consegna del rovesciatore — f1, corsia B

## 1. Cambi di stato e regole violate

- **Previsioni** (in `PREVISIONI.md`, scritte alle 13:12:50, prove alle 13:14): `rovesciatore-1` **non risolta**, con
  due mie sottoprevisioni **smentite**; `rovesciatore-2` regge su tre misure, **non risolta** sulla quarta.
- **Scostamenti dichiarati:** il rumore di processo di `prova_r1.py` (σ_a = 1 m/s², con 0,5 e 2 come sensibilità)
  l'ho fissato dopo le previsioni e prima di eseguire; alcune misure di `prova_r2.py` sono esplorative, senza
  previsione. Nessun'altra violazione nota.
- **Indipendenza:** scena, parametri e codice delle due simulazioni sono miei. Sono prove di classe 2: valgono
  per coerenza e ordine di grandezza, non come misura sul campo.

## 2. Critiche

1. **La bozza ha un buco su R8.** Il principio c'è (riga 2186: una cella non osservata non è libera) e la cella
   conserva «Last update» (riga 2181), ma nessuna regola lo usa: il log-odds non decade (righe 2208–2225) e le
   tracce scadono (riga 2272). Una cella vista libera e poi nascosta resta libera. L'ho cercato per parole
   sull'intero file (decad, decay, dimentic, forget, età, occlus, obsolet), non con una lettura integrale.
   Simulazione: con la traccia cancellata dopo 1 s, per il **73,5%** del tempo in occlusione il bersaglio sta dove
   il sistema non dichiara più nulla.
2. **La previsione a punto più ellisse (idea «e») è onesta solo se chi è nascosto non manovra.** Fuori
   dall'ellisse al 95%: 0,1% per chi prosegue, 23,8% per chi si ferma, 25,3% per chi torna indietro; in totale
   14,3%. Dopo 2 s l'ellisse (12,1 m²) è più grande dell'ombra intera (11,4 m²) e sbaglia ancora nel 21,1% dei
   passi. La miscela delle manovre (60/25/15) è una mia ipotesi: «non verificato».
3. **Il piano della bozza mette per ultimo ciò che le regole chiedono per primo.** Fase 1 è moto proprio più
   Rolling Grid, l'occlusione arriva in Fase 2 e l'incertezza in Fase 3 (righe 2756–2795). Il testo della
   challenge (riga 3) chiede occlusioni, osservato contro incerto e perdita di affidabilità. In 24–48 ore l'ultima
   fase è quella che salta.
4. **Decidere «mobile» sulla velocità istantanea non regge, nemmeno con il sensore fisso.** Punto fermo a 3 m,
   15 Hz, rumore 3 cm: velocità stimata 0,24 m/s efficaci, 21,6% di «falso mobile» alla soglia di 0,3 m/s. Serve
   lo spostamento su una finestra (finestra non misurata). Senza IMU, come nell'idea in punti: 2,50 m/s, 99,3%.

## 3. Stati proposti

| Enunciato | Stato | Prova |
|---|---|---|
| Vista libera, poi nascosta, resta «libera» nella bozza | Verificato per ricerca di parole sull'intero file; effetto sostenuto dai dati (simulazione) | righe citate; `prova_r2.py` |
| Il Kalman che prosegue è calibrato in occlusione | Non risolto: 14,3% fuori, dipende dalla miscela delle manovre | registrazioni vere con soste dietro un pannello |
| L'insieme raggiungibile non esclude mai il bersaglio | Verificato su 2000 traiettorie simulate, sotto v ≤ v_max (per costruzione) | `prova_r2.py` |
| «Previsto» vale più di «sconosciuto» solo per circa 1 s | Sostenuto dai dati in una sola scena (τ* = 1,2 s) | `prova_r2.py` |
| Il moto proprio è la parte fragile del sensore indossato | Non risolto: vero senza IMU o con δt ≥ 30 ms; a ≤ 10 ms domina il rumore del filtro | misura di δt sul sensore scelto |
| Il sensore fisso dà velocità spurie ≤ 0,05 m/s | Smentito (0,241 m/s) | `prova_r1.py` |

## 4. Proposte

### rovesciatore-2 — il prodotto è la mappa di ciò che non si sa (la più forte delle due)

- **Capovolge:** «rilevo, traccio, classifico, poi decido» e «prevedo la posizione di chi sparisce».
- **Dalla demo all'indietro.** La giuria deve vedere cinque momenti: visibile; dietro il pannello con «previsto»
  che si allarga; fermo dietro il pannello con «ombra sconosciuta, non confermo libero»; mano sul sensore con
  «affidabilità persa»; riaggancio con la latenza a schermo. Bastano un sensore di profondità, la mappa di
  visibilità, un tracciatore e l'uscita a tre stati. Classificazione, massa, accelerazione, vision transformer,
  modello di decisione appreso, 360° e Rolling Grid escono dal percorso critico.
- **Che cosa si costruisce.** Una griglia in pianta, a celle di 10 cm, con lancio dei raggi a ogni fotogramma.
  Ogni cella ha uno stato e un'età: osservata ora (libera o occupata), prevista, sconosciuta. Una cella non
  rivista torna sconosciuta per età, non per log-odds. Per una traccia persa, «previsto» è il disco v_max·τ
  attorno all'ultima osservazione, intersecato con le celle non osservate: dove il sensore vede vuoto l'oggetto
  non c'è. Quando il disco riempie l'ombra si passa a «sconosciuto»: è il segnale di R6, senza soglie tarate. Il
  Kalman resta per la velocità sul visibile e come stima migliore nel primo secondo. La decisione è una tabella di
  regole sui tre stati. Il fuori campo è un'occlusione permanente dichiarata: un solo sensore basta a partire, e
  i tre sensori riducono lo sconosciuto invece di essere un prerequisito.
- **Guadagna:** R3, R4, R6 e R8 con un solo meccanismo; R7 (geometria su CPU: costo non misurato).
- **Perde:** R5 è più prudente (dopo circa 1 s dice «sconosciuto» anche per chi prosegue, dove il Kalman aveva
  ragione nel 99,9% dei passi); niente classi da mostrare; la garanzia cade oltre v_max, che va dichiarato per
  applicazione.
- **Esito del falsificatore:** soglia di smentita non scattata (14,3% contro 5%), previsione non raggiunta (20%).
- **Fonti** (titolo, autori e link visti nei risultati di ricerca; testi non riletti): Koschi e Althoff,
  [Set-based prediction of traffic participants considering occlusions and traffic rules](https://mediatum.ub.tum.de/1575358),
  IEEE T-IV 2020; Orzechowski, Meyer, Lauer,
  [Tackling Occlusions & Limited Sensor Range with Set-based Safety Verification](https://arxiv.org/pdf/1807.01262).
  Il trasferimento da veicoli a pedoni e ausili è mio: «non verificato».

### rovesciatore-1 — prima il sensore fermo, poi indossato

- **Capovolge:** «il sensore sta sulla persona» e l'ordine delle fasi.
- **Che cosa si costruisce.** Lo stesso nucleo su un sensore fisso su treppiede, nell'applicazione industriale
  ammessa dalle regole (riga 5): sfondo di profondità come mediana di N fotogrammi, mobili per differenza (R1),
  ostacoli e ombre dallo sfondo (R2), nastro a terra come verità di riferimento. Il sensore indossato viene dopo,
  con l'utente fermo e la sola rotazione compensata; l'odometria si compra, non si scrive (prodotto «non
  verificato»).
- **Guadagna:** prove di accettazione misurabili e ripetibili (criterio 1); niente odometria nel percorso critico.
- **Perde:** il racconto assistivo e il senso dei 360°. Il gradimento della giuria è «non verificato»: le regole
  non danno criteri di punteggio.
- **Esito:** il motivo «il moto proprio è fragile» regge solo senza IMU o con δt ≥ 30 ms (0,47 contro 0,24 m/s);
  a ≤ 10 ms no. La traslazione non è simulata. La proposta resta per la verità di riferimento, non per il rumore.

**Se l'ipotesi sull'hackathon è falsa.** Meno tempo o niente hardware: `rovesciatore-2` si mostra su
registrazioni o sulla scena simulata. Più tempo: sensore indossato e tre sensori.

## 5. Che cosa propongo dopo

1. All'avversario: rompere `rovesciatore-2` con due bersagli che si incrociano nell'ombra, uno più veloce di v_max,
   un'ombra che tocca il bordo del campo.
2. Al metrologo: misurare δt fra profondità e IMU sul sensore scelto (cinque minuti davanti a un muro) e la
   finestra di spostamento che separa fermo da mobile.
3. All'arbitro: decidere se la critica 1 entra come requisito («una cella non rivista non resta libera»).

File accanto a questo: `PREVISIONI.md`, `prova_r1.py`, `prova_r2.py`.
