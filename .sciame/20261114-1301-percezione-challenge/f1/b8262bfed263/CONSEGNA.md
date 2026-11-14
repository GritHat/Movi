Canarino: sciame-canarino-ff229a474629e844

# Consegna — sciame-requisiti, f1, corsia A (conservativa)

## 0. Cambi di stato e regole violate

- **Cambio di stato:** «3 ToF coprono 360°» (idea, punto a) → **smentito** sui 7 sensori controllati (P1), salvo un caso limite.
- **Regola 3, non rispettata in un punto:** la tracciabilità regole → aggiunte l'ho vista leggendo le regole prima di scrivere `PREVISIONI.md`: la riporto come controllo esaustivo, non come previsione.
- **Fonti secondarie:** le pagine ST e RealSense non hanno risposto; quei numeri vengono dal riassunto del motore di ricerca. Solo Orbbec è letta direttamente.
- **P2:** primo lancio fallito (manca `numpy`); rifatto in Python puro, modello e parametri invariati.
- TASK.md dice 40 minuti, il coordinatore 25: ho seguito il limite più stretto.

## 1. Diagnosi: la richiesta e il bisogno

Quattro requisiti su otto (R3, R4, R6, R8) riguardano **sapere che cosa non si sa**, e le regole dicono che «riconoscere un oggetto [...] non basta». Il bisogno è un sistema che resta onesto quando perde la vista, non uno che stima più grandezze. **Verificato** (esaustivo sulle 6 righe, `grep -ic`): le regole hanno 0 occorrenze di 360, massa, accelerazione, classific-, terreno, velocità, mappa, ToF, Kalman, transformer. Nella bozza «massa», «360» e «transformer» non compaiono: vengono solo dalla richiesta dell'utente.

| Aggiunta della squadra | Requisito che serve | Giudizio |
|---|---|---|
| Previsione della posizione fuori vista (e) | R3, R4 | **indispensabile** |
| Velocità (d) | R3 (serve a prevedere), R5 | **indispensabile** |
| Moto proprio dell'utente (b) | R1, solo se il sensore si muove | utile; evitabile con il sensore fermo |
| Classificazione (c) | nessuno; arricchisce il testo di R5 | utile se piatta (persona/altro); gerarchia rinviabile |
| 360° con 3 ToF (a) | nessuno | rinviabile; smentito (P1); tre calibrazioni estrinseche in più |
| Mappa del terreno (b) | R2 solo se «ostacolo» include i dislivelli (D6) | rinviabile: basta una griglia a tre stati |
| Accelerazione (d) | nessuno | rinviabile: entra come rumore di processo |
| Massa (d) | nessuno; non osservabile da profondità o immagine | **escludere** (vincolo del contratto) |
| MLE/MAP, gerarchia, RLS, IMM | nessuno | rinviabili: la bozza stessa li mette in fase 4 (righe 2797–2807, 2942–2944) |
| Catena Kalman → transformer (f) | — | ordine da chiarire: nella bozza il riconoscimento è un ramo parallelo e lento (righe 2609–2613). Agli specialisti |

## 2. Requisiti e criteri di accettazione (tutti indispensabili; soglie = IPOTESI da tarare, non verificate)

| | Misura | Soglia proposta | Come si mostra in demo |
|---|---|---|---|
| R1 | passaggi di una persona che diventano traccia mobile entro 1 s | ≥ 9 su 10; ≤ 1 traccia falsa in 2 min di scena ferma | 10 passaggi contati a mano |
| R2 | ostacoli fermi (≥ 30 cm) fra 0,5 e 3 m marcati occupati; errore di distanza | 5 su 5; errore ≤ 15 cm | metro a nastro |
| R3 | identità conservata dietro un pannello; errore alla ricomparsa | stessa traccia ≥ 8 su 10; errore dentro il 2σ dichiarato | passaggi dietro un pannello di ~1 m |
| R4 | ogni elemento in uscita è «osservato», «previsto» o «sconosciuto» | 0 fotogrammi «osservato» a soggetto nascosto; cambio entro 0,3 s | registrazione annotata a mano; tre colori a schermo |
| R5 | messaggio = direzione (settore) + fascia di distanza + stato | ritardo evento → segnale ≤ 300 ms; una persona bendata indica il settore giusto ≥ 9 su 10 | audio dal vivo |
| R6 | segnale distinto se l'occlusione supera T_max, il sensore è coperto o i fotogrammi calano | entro 1 s, 5 su 5; nessuna traccia resta «prevista» oltre T_max (1–2 s, da P2) | mano sul sensore; persona ferma dietro il pannello |
| R7 | latenza acquisizione → uscita (p95), fotogrammi al secondo, CPU | p95 ≤ 150 ms; ≥ 15 al secondo su portatile senza GPU (bozza, righe 2620–2627) | contatore a schermo; cronometro inquadrato |
| R8 | volte in cui l'uscita dice «libero» su un settore non osservato | 0 in tutta la demo, più l'invariante nel codice («libero» esige un'osservazione più recente di Δ) | coprire metà campo: quel settore dice «non osservato» |

Zero errori in demo non provano R8: per questo il criterio chiede anche l'invariante, controllabile per ispezione.

## 3. Ambiguità da sciogliere (**non verificate**; chi risponde; che cosa cambia)

- **D1** durata e squadra (utente): sotto le 24 ore resta solo l'MVP.
- **D2** hardware posseduto, fornito o ammesso, e quali ToF ha in mente la squadra (utente, organizzatori): decide il sensore.
- **D3** criteri e pesi della giuria (organizzatori): decidono l'applicazione e quanto vale la classificazione.
- **D4** prototipo dal vivo o software su video registrati (organizzatori): sui video R5 e R7 si misurano peggio.
- **D5** minuti, spazio e luce della demo (organizzatori): i ToF soffrono la luce solare (non verificato).
- **D6** «ostacolo» include gradini e dislivelli? (organizzatori): solo un sì riporta in ambito la mappa del terreno.
- **D7** il feedback deve essere non visivo? (organizzatori): lo assumo audio, con lo schermo solo per la giuria.

**Applicazione.** «Feedback spaziali» e «sicurezza delle indicazioni» si leggono meglio come indicazioni a una persona: la storia **assistiva** aderisce di più al testo. Il sensore fermo, tipico del monitoraggio industriale, toglie però il rischio maggiore, la compensazione del moto proprio. Propongo lo stesso nucleo per entrambe: storia assistiva con l'utente fermo a un incrocio, e «monitoraggio» come ripiego senza lavoro in più. La preferenza della giuria non è verificata (D3).

## 4. Proposte

**requisiti-1 — «Taglio a otto» (l'MVP).** *Enunciato:* un solo sensore di profondità frontale e fermo copre R1–R8, senza 360°, massa, accelerazione, gerarchia, MLE/MAP e mappa del terreno. La catena: rilevamento geometrico sulla profondità → tracce con Kalman a velocità costante → tre stati per traccia e per settore → audio (direzione, distanza, stato) e schermo a tre colori → contatore della latenza. Fuori dal campo è «non osservato», mai «libero». *Guadagno:* restano le fasi 1–3 della bozza, ridotte, e nessuna calibrazione fra sensori (risparmio in ore: non verificato). *Vincoli:* campo frontale di 87–120°. *Se l'ipotesi di fattibilità è falsa* (più tempo o più hardware): i 360° tornano «utili». *Chi la prova:* avversario (una frase delle regole non coperta), sensori, fusione. *Falsificatore:* P1. **Esito: regge.** Campo orizzontale: VL53L5CX e L8CX 45°, VL53L7CX 60°, Arducam ToF sotto 70° (modello T2: 64°), Femto Bolt 75° e 120°, RealSense D435 e D455 87°. Nessuno ≥ 130°. Caso limite: il Femto Bolt in WFOV, 120° esatti, zero sovrapposizione, portata al più 2,88 m; l'interferenza fra tre ToF affiancati non è verificata.

**requisiti-2 — «Demo del pannello».** *Enunciato:* una scena di ~3 minuti in cinque atti mostra ogni requisito con un numero: (1) campo mezzo coperto → «non osservato» (R8); (2) ostacolo fermo (R2, R5); (3) persona che attraversa, latenza a schermo (R1, R5, R7); (4) passa dietro un pannello di ~1 m → «previsto» → stessa traccia (R3, R4); (5) si ferma dietro il pannello, o si copre il sensore → «affidabilità persa» (R6, R8). *Guadagno:* ogni riga del criterio 1 ha un momento visibile. *Vincoli:* la larghezza del pannello va tarata sul modello del moto. *Chi la prova:* kalman e tracciamento (il valore di q), validazione, interfacce. *Falsificatore:* P2. **Esito: regge.** 2σ supera 1 m dopo T = 1,30 / 1,07 / 0,87 s per q = 0,25 / 0,5 / 1,0 m²/s³; forma chiusa e Monte Carlo concordano entro l'1,1 %. A 1,3 m/s (non verificato) sono 1,1–1,7 m di percorso nascosto: dietro un pannello di 1 m la traccia resta «prevista», una sosta più lunga deve diventare «sconosciuto». Il controllo condivide modello e parametri con l'enunciato: vale per l'algebra, non per un pedone vero.

## 5. Stati proposti e che cosa dopo

- **Verificato:** le regole non nominano nessuna delle aggiunte (6 righe, esaustivo).
- **Smentito:** 360° con 3 ToF e sovrapposizione, sui 7 sensori controllati.
- **Sostenuto da un calcolo, non da una misura:** finestra utile della previsione di 0,9–1,3 s nel modello a velocità costante.
- **Non risolto:** D1–D7, le soglie del §2 e il valore di q per un pedone vero; li decidono le risposte e una prova sul sensore.
- **Dopo:** porre D1–D7 all'utente in un solo messaggio; l'avversario attacchi requisiti-1; kalman e tracciamento fissino q e T_max.

Fonti: [Orbbec Femto Bolt](https://www.orbbec.com/products/tof-camera/femto-bolt/) (letta); [ST VL53L7CX e L8CX](https://www.st.com.cn/resource/en/flyer/vl53l7cx-vl53l8cx-flyer.pdf), [RealSense](https://realsenseai.com/cn/compare-depth-cameras/), [Arducam](https://www.arducam.com/time-of-flight-camera-for-raspberry-pi.html) (dal riassunto della ricerca).
