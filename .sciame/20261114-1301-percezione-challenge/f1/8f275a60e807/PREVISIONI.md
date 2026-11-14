# Previsioni del rovesciatore (f1, corsia B)

Scritte alle **2026-11-14T13:12:50+01:00** (`date -Is`), PRIMA di scrivere ed eseguire le due simulazioni.
Le simulazioni sono in Python puro (numpy non è installato), su CPU, al più cinque minuti ciascuna: prove di classe 2
(simulazione numerica piccola). Indipendenza: modello della scena, parametri e codice sono dello stesso autore
(io); valgono solo come controllo di coerenza interna e di ordine di grandezza, non come misura sul campo.

## P-rovesciatore-1 — «il sensore sta nell'ambiente, non sulla persona»

- **Enunciato sotto prova:** con il sensore indossato, la compensazione del moto proprio è la parte fragile: un
  punto FERMO a 3 m acquista una velocità apparente che lo fa sembrare mobile (falso R1), mentre con il sensore
  fisso no.
- **Misura:** velocità apparente efficace (RMS, m/s) stimata da un Kalman a velocità costante su un punto fermo a
  3 m, 15 Hz, rumore di misura 3 cm, con la testa che oscilla (scansione ±20° a 0,5 Hz più oscillazione del passo
  ±3° a 2 Hz) e la rotazione compensata con un giroscopio perfetto ma con errore di sincronizzazione δt fra
  profondità e IMU: δt = 0, 5, 10, 30 ms, e senza compensazione. Confronto: sensore fisso (stesso filtro).
  Seconda misura: frazione dei fotogrammi con velocità stimata > 0,3 m/s («falso mobile»).
- **Previsione:** RMS ≥ 0,10 m/s a δt = 10 ms; RMS ≥ 0,30 m/s a δt = 30 ms; > 1 m/s senza compensazione; sensore
  fisso ≤ 0,05 m/s. Falso mobile > 10% a 30 ms, < 1% con il sensore fisso.
- **Soglia di smentita:** se a δt = 30 ms (un fotogramma di disallineamento a 30 fps) l'RMS è < 0,10 m/s, il moto
  proprio NON è la parte fragile e il motivo principale del rovesciamento cade (smentita). Se è fra 0,10 e 0,30:
  non risolta. Regge se ≥ 0,30 a 30 ms e fisso ≤ 0,05.
- **Che cosa la simulazione non decide:** la traslazione (richiede odometria visivo-inerziale, non simulata), i
  valori reali di δt dei sensori scelti («non verificato»), il moto reale della testa di un utente.

## P-rovesciatore-2 — «il prodotto è la mappa di ciò che non si sa, non la traccia»

- **Enunciato sotto prova:** la catena della bozza (Kalman a velocità costante che prosegue alla cieca + scadenza
  della traccia + griglia in log-odds senza decadimento) dichiara «non occupato» un luogo dove il bersaglio
  nascosto si trova davvero, per una parte non trascurabile del tempo di occlusione; l'insieme raggiungibile
  (disco di raggio v_max·τ attorno all'ultima posizione osservata, intersecato con la regione NON osservata) non
  lo fa mai, per costruzione, finché v ≤ v_max.
- **Scena:** sensore fisso nell'origine, pannello largo 1,5 m a 2 m, portata 6 m; pedoni a 4 m che attraversano
  l'ombra (larga 3 m a quella distanza) a 1,3 ± 0,2 m/s; dentro l'ombra: 60% proseguono, 25% si fermano (2–6 s),
  15% tornano indietro. 15 Hz, rumore 5 cm. Il rumore di processo q del Kalman è scelto PRIMA di guardare la
  copertura: quello che massimizza la verosimiglianza delle innovazioni sui tratti visibili (come farebbe la
  squadra tarando sul visibile). v_max = 2,5 m/s.
- **Misure:** (M1) frazione dei secondi-bersaglio in occlusione in cui la posizione vera è FUORI dall'ellisse al
  95% del Kalman, nelle varianti: traccia mai cancellata, cancellata dopo 1 s, dopo 3 s (dopo la cancellazione la
  posizione vera conta come non coperta: la cella dell'ombra resta nello stato precedente, «libero»). (M2) lo
  stesso per l'insieme raggiungibile. (M3) il tempo τ* dopo cui l'insieme raggiungibile∩ombra supera il 90%
  dell'area dell'ombra.
- **Previsione:** M1 > 20% (traccia mai cancellata) e > 50% (cancellata dopo 1 s); M2 = 0%; τ* ≤ 1,5 s (cioè
  «previsto» vale più di «sconosciuto» solo per circa un secondo, poi tutta l'ombra va dichiarata sconosciuta).
- **Soglia di smentita:** se M1 (mai cancellata) < 5%, il Kalman che prosegue è onesto e il rovesciamento non ha
  motivo di sicurezza (smentita). Fra 5% e 20%: non risolta. Se τ* > 2 s (a 2 s l'insieme copre meno del 90%
  dell'ombra), è smentita la parte «orizzonte breve».
- **Che cosa la simulazione non decide:** la miscela reale delle manovre (60/25/15 è una mia ipotesi dichiarata,
  «non verificato»); bersagli più veloci di v_max; il costo in falsi allarmi sul campo.

## Esiti

Compilati dopo le prove, fra le 13:15:07 e le 13:16:50 del 2026-11-14 (`date -Is`). Comandi (nella cartella della consegna):
`timeout 280 python3 -I prova_r1.py` (eseguito alle 13:14:28, meno di 1 s) e `timeout 280 python3 -I prova_r2.py`
(13:14:45–13:14:47). Semi fissi: i numeri si riottengono rieseguendo.

**Scelte fatte dopo aver scritto le previsioni ma prima di eseguire (dichiarate):** in `prova_r1.py` il rumore di
processo del Kalman non era fissato nella previsione; ho preso σ_a = 1 m/s² come caso primario e 0,5 e 2 come
sensibilità. In `prova_r2.py` ho aggiunto misure esplorative senza previsione (per manovra, per fascia di τ, area
dell'ellisse, «media prevista in zona visibile»).

### P-rovesciatore-1 — esito: NON RISOLTA (una parte regge, due sottoprevisioni smentite)

| Configurazione (σ_a = 1) | RMS m/s | «falso mobile» (> 0,3 m/s) |
|---|---|---|
| sensore fisso | 0,241 | 21,6% |
| indossato, δt = 0 | 0,241 | 21,6% |
| indossato, δt = 5 ms | 0,250 | 24,4% |
| indossato, δt = 10 ms | 0,275 | 29,7% |
| indossato, δt = 30 ms | 0,469 | 61,5% |
| indossato, senza compensazione | 2,502 | 99,3% |

- Regge: RMS ≥ 0,10 a 10 ms (0,275); RMS ≥ 0,30 a 30 ms (0,469); > 1 m/s senza compensazione (2,50); falso mobile
  > 10% a 30 ms (61,5%). La soglia di smentita (RMS < 0,10 a 30 ms) non è scattata.
- **Smentite:** «sensore fisso ≤ 0,05 m/s» (misurato 0,241) e «falso mobile < 1% con il sensore fisso» (21,6%).
  Con σ_a = 0,5: fisso 0,145 m/s e 1,1%; con σ_a = 2: fisso 0,396 m/s e 55,5%.
- Per la regola scritta prima («regge se ≥ 0,30 a 30 ms E fisso ≤ 0,05») l'esito composto non è «regge».
- Notato DOPO: il rumore di velocità del filtro stesso (0,24 m/s) supera l'effetto del moto proprio fino a
  δt = 10 ms; il contributo del solo disallineamento, tolto in quadratura, è circa 0,07 m/s a 5 ms, 0,13 a 10 ms,
  0,40 a 30 ms (il calcolo senza filtro r·α·δt dà 0,095, 0,19, 0,57). Quindi il vantaggio del sensore fisso sulla
  sola rotazione è netto solo senza IMU o con δt ≥ 30 ms.

### P-rovesciatore-2 — esito: M1 «mai cancellata» NON RISOLTA; le altre tre reggono

q scelto dalla verosimiglianza sui tratti visibili: 0,1 m²/s³ (lo stesso valore anche includendo le innovazioni di
riaggancio). 2000 traiettorie (1172 proseguono, 525 sostano, 303 tornano), 6856 secondi-bersaglio in occlusione.

- M1, traccia mai cancellata: **14,3%** fuori dall'ellisse al 95% (previsto > 20%; smentita < 5%): non risolta.
- M1, traccia cancellata dopo 1 s: **73,5%** (previsto > 50%): regge. Dopo 3 s: 34,5%.
- M2, insieme raggiungibile: **0,00%** (previsto 0%): regge, ma per costruzione (v ≤ 1,8 < v_max = 2,5).
- M3: τ* = **1,2 s** (previsto ≤ 1,5 s): regge. L'ombra entro la portata misura 11,4 m².
- Notato DOPO (esplorativo): fuori dall'ellisse 0,1% per chi prosegue, 23,8% per chi sosta, 25,3% per chi torna;
  per fascia di τ: 2,0% in [0,1) s, 8,9% in [1,2), 21,1% in [2,3), 37,9% in [3,4); l'area media dell'ellisse in
  [2,3) s è 12,1 m², cioè più dell'ombra intera (11,4 m²), e manca comunque il bersaglio nel 21,1% dei passi; la
  media prevista dal Kalman cade in zona VISIBILE (dove il sensore vede vuoto) nel 21,2% dei passi in occlusione.
