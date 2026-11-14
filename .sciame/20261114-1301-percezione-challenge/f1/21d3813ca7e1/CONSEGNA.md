Canarino: sciame-canarino-ff229a474629e844

# Consegna di `sciame-kalman` — f1, corsia A (stima dello stato)

## 0. Cambi di stato e scostamenti

- Nessuna regola violata, che io sappia. Scostamenti: `numpy` non è installato, la simulazione è in Python puro
  (non ho installato nulla); della bozza ho letto le righe 2270–2380 e una ricerca per parole chiave sul resto, non
  tutte le righe 1998–2945.
- Previsioni scritte alle 13:06:28 (`PREVISIONI.md`), simulazione eseguita alle 13:08:34: **tutte e dieci reggono**.
  Prova: `cd <questa cartella> && python3 sim_kalman.py | tee risultati.txt` (8 s, semi fissati).
- Indipendenza: la verità simulata non è il modello del filtro (pedone con salti di velocità di Poisson e
  rilassamento, tau 0,4 s), ma condivide con il filtro l'autore, il rumore gaussiano isotropo (5 cm per asse,
  **ipotesi mia, non verificata** su una scheda tecnica) e l'assenza di errori di associazione. I numeri valgono per
  il modello di moto e la taratura, non per il sensore reale.

## 1. Diagnosi (riferimento: 15 Hz, 5 cm, piano del suolo)

1. **L'ordine «Kalman → vision transformer → decision model» è invertito.** Un filtro per ostacolo ha bisogno di una
   misura per ostacolo, che nasce dal rilevamento. Messo prima, può filtrare solo i pixel di profondità (sbava i
   bordi in moto) o il moto proprio. Ordine corretto: sensore → compensazione del moto proprio → rilevamento →
   associazione (porta di Mahalanobis) → filtro per traccia → previsione con covarianza → decisione → feedback. È
   l'ordine che la bozza stessa scrive alle righe 2269–2274, e quello di SORT (Kalman e algoritmo ungherese a valle
   del rilevatore, 260 Hz: <https://arxiv.org/abs/1602.00763>, riassunto letto oggi). La rete semantica resta
   asincrona, fuori dal ciclo veloce. Il filtro non pesa su R7: oltre un milione di passi di filtro in 8 s di Python puro.
2. **La massa non è osservabile.** Dalle sole posizioni si osserva l'accelerazione a = F/m; con la forza ignota
   (pedoni e veicoli si spingono da sé) le coppie (F, m) e (kF, km) danno la stessa traiettoria, e in caduta libera la
   massa si semplifica. Controllo: l'informazione di Fisher di (F, m) ha rango 1 (det/traccia² = 5·10⁻¹⁷).
   **Dimostrato** nel modello del punto materiale con forza ignota. La sostituisce ciò che si osserva: l'ingombro
   (larghezza e altezza dalla profondità) → classe di taglia; gravità ordinale = classe × velocità di avvicinamento.
   Una massa «per classe» è un a priori da tabella e va chiamata così.
3. **Posizione e velocità sì, accelerazione no.** Velocità quasi costante (CV), Q tarata sul NIS: posizione 3 cm,
   velocità 0,18 m/s reali (0,21 dichiarati) per asse; 0,17–0,19 m/s da 10 a 30 Hz, 0,23 con 10 cm. Con
   l'accelerazione costante (CA) l'errore sull'accelerazione è 0,82 m/s² contro 0,67 di valore efficace vero: peggio
   che supporla nulla. A 2 s di occlusione CA sbaglia 2,29 m contro 1,18 m di CV, con raggio al 95% di 5,1 m contro 2,1.
4. **In occlusione la previsione vale 1–2 s.** Il raggio al 95% di CV supera 1 m dopo 1,2 s, 1,5 m dopo 1,6 s, 2 m
   dopo 2 s (cresce come q·t³/3). Oltre, «previsto» non informa più: è R6. OC-SORT lo dice per i tracciatori: senza
   misure gli errori del Kalman si accumulano (<https://arxiv.org/abs/2203.14360>, riassunto letto oggi).
5. **Q scelta a occhio viola R8.** Con q = 0,01 (traccia liscia) il cerchio al 95% contiene la verità solo nel 42%
   dei casi a 2 s. Con q tarato (0,2 m²/s³) la copertura è 0,94 / 0,92 / 0,90 / 0,92 a 0,5 / 1 / 2 / 3 s.
   *Notato dopo:* è sotto il 95% nominale (errore tipo 0,008), benché NIS = 1,95 e NEES = 3,3 su 4 da visibile: il NIS
   a un passo non garantisce la copertura a più secondi. Con 4q la copertura sale a 0,997 ma il raggio raddoppia.
6. **Moto proprio: il giroscopio è obbligatorio, l'odometria dipende.** Ostacolo fermo, portatore a 1,2 m/s, testa
   ±30° a 0,5 Hz: senza compensazione la distanza di passaggio prevista sbaglia di 1,49 m; con il solo giroscopio
   (bias 1°/s) di 0,25 m. La traslazione serve solo a distinguere fermo da mobile (R1): senza, ogni muro risulta
   «mobile» il 100% del tempo; con essa (errore 10%) lo 0%. Con un sensore fisso (applicazione industriale) il
   problema sparisce.
7. **Non simulato, non verificato:** il centroide di un oggetto che entra in occlusione si sposta verso la parte
   ancora visibile e sporca la velocità proprio prima della previsione; il rumore reale cresce con la distanza ed è
   correlato; la porta che si allarga in occlusione favorisce gli scambi d'identità. Sono problemi di rilevamento e
   associazione, non di filtraggio. IMM non provato: la bozza stessa lo rinvia (riga 2346).

## 2. Stati proposti

| Enunciato | Stato |
|---|---|
| La massa si stima dalle misure di posizione | **Smentito** (dimostrazione al punto 2) |
| Catena «Kalman → ViT → decisione» | Da correggere: argomento e fonte, nessuna misura |
| CV con Q tarata sul NIS dà una covarianza credibile fino a 3 s di occlusione | **Sostenuto dai dati** (un solo modello di pedone simulato; copertura 0,90–0,94) |
| Stimare l'accelerazione migliora la previsione | **Smentito** nella simulazione |
| Serve compensare la rotazione di chi indossa i sensori | **Sostenuto dai dati** (simulazione) |
| q = 0,2 m²/s³ vale per pedoni e sensore reali; IMM utile | **Non risolto**: lo decide la taratura su sequenze registrate |

## 3. Proposte

**`kalman-1` — Catena riordinata, stimatore minimo, niente grandezze non osservabili.**
*Enunciato.* Un Kalman lineare CV per traccia, stato [x, y, vx, vy] sul piano del suolo, in un riferimento
stabilizzato in rotazione dal giroscopio (e in traslazione, se c'è odometria); a valle di rilevamento e associazione,
a monte della decisione. Niente massa e niente accelerazione. «Mobile» è una prova sulla covarianza
(v'·Pv⁻¹·v > 9,21, chi quadrato al 99%), non una soglia fissa. La gravità viene da classe di taglia e velocità di
avvicinamento.
*Guadagno atteso.* Velocità a 0,2 m/s; un pedone a 1,2 m/s dichiarato mobile in 0,20 s (mediana); un ostacolo
fermo dichiarato mobile nello 0,0% del tempo (500 prove); soglia di regime a circa 0,62 m/s (3,03 × 0,205, calcolo):
sotto, la prova non scatta.
*Vincoli.* Serve una IMU con le marche temporali allineate alla profondità. Se il tempo è poco: sensore fisso o
portatore fermo, e la compensazione si toglie.
*Chi la può provare.* Fusione (allineamento IMU), tracciamento (associazione), avversario.
*Falsificatore (5 min).* Simulato: previsto errore > 1 m senza compensazione e < 0,3 m con il giroscopio; esito
1,49 e 0,25 m, **regge**. Sul prototipo: da fermi, riprendere un muro ruotando la testa per 30 s; smentita se il
muro risulta «mobile» per più del 10% del tempo a rotazione compensata.

**`kalman-2` — La covarianza predetta è il segnale di R4 e R6, accettata solo con la copertura alla ricomparsa.**
*Enunciato.* Tre stati per traccia: «osservato» (aggiornata in questo ciclo, innovazione in porta); «previsto» (sola
predizione, si comunica l'area al 95% e non un punto); «perso» quando il raggio al 95% supera r_max (proposta:
1,5 m, cioè circa 1,6 s) o l'innovazione alla ricomparsa è fuori porta: la zona torna «non osservata», mai «libera».
Q si tara sul NIS e si accetta solo se, su 30 occlusioni registrate di 1–2 s, la misura alla ricomparsa cade nel
cerchio al 95% almeno 26 volte.
*Guadagno atteso.* R3, R4, R6 e R8 hanno una prova di accettazione numerica, fattibile senza verità di riferimento
(nella simulazione, con q tarato, la copertura sulla misura segue quella sulla verità entro 0,01 da 1 s in su). Il criterio 26/30
passa nel 91% dei casi con copertura vera 0,92, nel 10% con 0,75, mai con 0,42 (calcolo binomiale).
*Vincoli.* Un'ora di registrazioni con una persona che passa dietro un pannello; più sequenze, non una.
*Chi la può provare.* Validazione, statistico, tracciamento.
*Falsificatore (5 min).* Simulato: prevista copertura in [0,88; 0,99], esito 0,90–0,94, **regge** (smentita sotto
0,85). Sul prototipo: le 30 occlusioni; meno di 26 dentro smentisce la taratura.

## 4. Che cosa propongo dopo

1. Chiedere all'esperto di sensori il rumore reale del ToF in funzione della distanza e rifare S1–S2 con quello.
2. Far attaccare all'avversario il punto 7 (centroide in occlusione parziale, scambio d'identità alla ricomparsa).
3. Provare un limite fisico al raggio (v_max·t) accanto a q·t³/3, e l'IMM solo se la copertura reale non regge.
