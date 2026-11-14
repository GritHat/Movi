# PREVISIONI — sciame-nuvole-punti, f1, corsia A

Scritte PRIMA di eseguire le prove. Ora di scrittura (da `date -Is`, letta subito prima): 2026-11-14T13:05:43+01:00.
Macchina: AMD Ryzen AI 9 HX 370, Python 3.14.10 puro (numpy e scipy assenti: non li installo).

## P-np1a — controesempio alla regola log-odds della bozza (per nuvole-punti-1)

- **Prova:** simulazione 2D in Python puro, griglia polare egocentrica (campo 87°, 1° per settore, celle da 0,1 m
  fino a 6 m), 15 Hz per 6 s. Scena: parete a 5 m; un occlusore largo 0,8 m entra a 2 m dal sensore a t = 1 s e
  resta; un pedone largo 0,5 m attraversa a 4 m a 1 m/s e passa dietro l'occlusore. Verità di riferimento: le celle
  che il pedone occupa davvero.
- **Regola A (bozza §4.5, come scritta):** log-odds aggiornata solo dove un raggio osserva (colpo +0,85, passaggio
  −0,4, limiti ±3,5), nessun decadimento; uscita «libero» se L < −1.
- **Regola B (nuvole-punti-1):** stesso accumulo, ma l'uscita di una cella è «libero» solo se nel fotogramma corrente
  la cella è davanti al primo ritorno del suo settore; dietro il primo ritorno è «in ombra» (non osservato), fuori dal
  campo è «fuori campo».
- **Misura:** numero di coppie (fotogramma, cella) in cui una cella occupata dal pedone è dichiarata «libero»
  (violazione di R8).
- **Previsione:** regola A ≥ 10 violazioni (per tutto il transito in ombra); regola B = 0 violazioni.
- **Soglia di smentita:** regola A = 0 violazioni (la mia critica alla bozza cade), oppure regola B > 0 (la mia
  proposta non ripara).
- **Indipendenza:** simulatore, regole e verità di riferimento li scrivo io, stesso modello: prova che la regola A
  ammette il controesempio, non misura niente su dati veri di un sensore (rumore, punti misti ai bordi).

## P-np1b — costo per fotogramma su CPU (per nuvole-punti-1)

- **Prova:** stesso codice, tempo di un fotogramma con 19 200 misure (immagine di profondità 640×480 sottocampionata
  4×4 a 160×120), tabelle per riga e per colonna precalcolate, classificazione suolo/ostacolo per quota e stato di
  5 220 celle polari (87 × 60). Mediana di 20 fotogrammi, un solo core.
- **Previsione:** ≤ 40 ms per fotogramma in Python puro (limite superiore pessimistico: una versione vettoriale o in
  C++ costa meno, «non verificato» qui).
- **Soglia di smentita:** > 66 ms (il periodo a 15 Hz). In quel caso l'affermazione «la rappresentazione sta nel
  tempo di fotogramma senza ottimizzazioni» cade; se sta fra 40 e 66 ms l'esito è «non risolta».

## P-np2 — che cosa vedono i sensori candidati (per nuvole-punti-2)

- **Prova:** conto geometrico (script) con i dati delle schede tecniche, sensore a 1,2 m da terra. Bersagli: pedone
  0,5 × 1,7 m a 1, 2 e 4 m; impronta sul suolo, lungo la distanza, di un singolo elemento di misura a 1, 2, 3 m.
- **Criteri fissati ora:** «pedone raggruppabile» = almeno 10 elementi sul bersaglio (almeno 5 fasci per un sensore
  a scansione su un piano); «terreno risolto» = impronta di un elemento sul suolo ≤ 0,10 m (la cella della bozza);
  «360°» = somma dei campi orizzontali di 3 unità ≥ 300°.
- **Previsione:**
  1. ToF multizona 8×8, campo 45°×45° (classe VL53L5CX): terreno NON risolto già a 1 m (impronta > 0,10 m); pedone
     raggruppabile a 1 e 2 m, non a 4 m; tre unità coprono ≤ 135°, non 360°.
  2. Camera di profondità 640×480, campo 87°×58° (classe RealSense D435): terreno risolto fino a 3 m (impronta
     ≤ 0,10 m, solo campionamento, rumore a parte); pedone con più di 1 000 pixel a 4 m; una unità copre 87°.
  3. LiDAR 2D a 360°, passo 0,8° (classe LD19 a 10 Hz): 360° sì; terreno non osservabile (un solo piano); pedone a
     4 m con 5–10 fasci.
- **Soglia di smentita:** l'8×8 ha impronta ≤ 0,10 m a ≥ 1 m, o tre unità coprono ≥ 300°; oppure la camera ha
  impronta > 0,10 m a 3 m o meno di 10 pixel sul pedone a 4 m; oppure il LiDAR 2D dà meno di 5 fasci a 4 m.
- **Indipendenza:** il conto è mio; i campi visivi e le risoluzioni vengono dalle schede dei costruttori (da
  controllare in rete: se un dato della scheda è diverso da quello che ho assunto qui, rifaccio il conto e lo dico).

## Esiti (compilati DOPO le prove)

Prove eseguite alle 2026-11-14T13:07:26+01:00 con `python3 -I prova_np.py` (stessa cartella); esiti scritti alle
2026-11-14T13:09:05+01:00.

- **P-np1a: regge.** Regola A: 173 violazioni in ombra su 552 coppie (fotogramma, cella del pedone); regola B: 0.
  *Notato dopo, non previsto:* la regola A sbaglia anche col pedone visibile (92 coppie): la cella era a −3,5 e
  servono tre colpi per risalire sopra −1 (il ritardo noto delle griglie statiche sugli oggetti mobili).
- **P-np1b: regge.** Mediana 2,01 ms, massimo 2,04 ms per fotogramma (19 200 misure, 5 220 celle, Python puro, un
  core). Limite: le tabelle per pixel sono fisse (orientamento costante); con l'orientamento che cambia a ogni
  fotogramma vanno ricalcolate, costo non misurato.
- **P-np2: regge**, con un dato corretto dopo il controllo della scheda.
  1. ToF 8×8: impronta sul suolo 0,20 m a 1 m, 0,45 m a 2 m, 0,87 m a 3 m; pedone 39,9 / 20,3 / 5,4 zone a
     1 / 2 / 4 m; tre unità 135°. La scheda ST conferma 45°×45° (63° in diagonale), 400 cm, 8×8.
  2. Camera 640×480: impronta 0,4 / 1,0 / 1,8 / 3,1 cm a 1 / 2 / 3 / 4 m; pedone 7 756 pixel a 4 m; una unità 87°.
  3. LiDAR 2D: 8,9 fasci sul pedone a 4 m; nessun terreno.
  *Notato dopo:* (a) con una camera ToF 240×180 da circa 58°×45° (conto a mano, campo «70° in diagonale» da un solo
  rivenditore: non verificato) l'impronta a 3 m è circa 4 cm e il pedone a 4 m ha circa 2 500 pixel: il terreno è
  risolto, ma tre unità coprono circa 174°; (b) tre camere ToF a campo largo 120°×120° (Orbbec Femto Bolt) arrivano
  a 360° senza sovrapposizione: la previsione «3 ToF non coprono 360°» vale per i multizona e per le camere a campo
  normale, non per questa classe.
