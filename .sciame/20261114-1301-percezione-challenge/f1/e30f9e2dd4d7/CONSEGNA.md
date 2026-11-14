Canarino: sciame-canarino-fe0856355f521597

# Consegna — sciame-creativo, f1, corsia B (percezione-challenge)

## 1. Cambi di stato e regole violate
- **Una mia previsione è smentita in alto:** la finestra di riemersione del filtro a particelle (P-creativo-2b/3) doveva coprire fra 75 % e 97 %; copre il 100 % ed è larga 6,3 s: inutile come scommessa. La soglia di smentita scritta (< 70 %) non è scattata.
- **P-creativo-3bis è nata dopo** aver visto quell'esito: in `PREVISIONI.md` porta la sua ora (13:14) e la dicitura; è stata scritta prima di eseguire `sim2.py`.
- **Bozza letta solo in parte:** indice dei titoli e righe 2205–2284, 2480–2639, 2821–2945.
- **Fonti:** lette nel testo solo Wikipedia (ricerca bayesiana) e Hulgard e Ratcliffe 2016. Le altre vengono dai riassunti del motore di ricerca: portano «non verificato sul testo». La pagina ST del VL53L5CX è andata in timeout.
- **Indipendenza:** simulazioni, filtri e previsioni hanno lo stesso autore e lo stesso modello. In 2b la «verità» simulata segue un moto che il filtro non conosce. Nessun dato reale, nessun sensore, nessuna persona.
- Prove: `sim.py` (4,4 s) ed `sim2.py`, esiti in `esito_sim.txt` e `esito_sim2.txt`, nella mia cartella. Python puro, 1D, 15 Hz, classe 2.

## 2. Critiche
1. **Il Kalman in coasting mette il «previsto» dove il sensore vede vuoto.** Bersaglio che si ferma dietro un occlusore largo 2 m: dopo 2 s il 98 % della massa di probabilità del Kalman a velocità costante è in celle osservate libere, dopo 3 s il 100 % (100 prove). Tocca il punto (e) dell'idea e la riga 2882 della bozza, che nomina il difetto senza curarlo.
2. **La finestra del solo Kalman è troppo ottimista.** Intervallo nominale al 90 % sull'istante di riemersione: copertura 69,3 % su 400 passaggi (36 rallentamenti su 126, 1 sosta su 34), con σ di accelerazione 0,3 m/s²; altri valori non provati.
3. **Il feedback della bozza tace in tre casi diversi.** Le righe 2554–2574 segnalano a evento e non danno indicazioni «quando il sistema non possiede informazioni sufficienti»: il silenzio vale «libero osservato», «non so» e «sistema fermo». Contro R6 e R8. Prova: il testo.
4. **Tre ToF per 360°: indizio contrario.** Un ToF multizona tipo VL53L5CX avrebbe 45°×45° (63–65° in diagonale): tre coprono 135°. Non verificato sul testo, e non so quale ToF intenda la squadra.

## 3. Stati proposti
| Enunciato | Stato |
|---|---|
| Il Kalman CV in coasting colloca il previsto in zona osservata libera se il bersaglio sosta nell'ombra | Sostenuto dai dati (simulazione 1D) |
| L'aggiornamento per mancato rilevamento confina la massa nell'ombra (99,9 % a 3 s) | Sostenuto dai dati (simulazione 1D, non sul sensore) |
| La finestra del filtro a particelle copre fra 75 % e 97 % | Smentito (100 %, larga 6,3 s) |
| La finestra tarata sulle prove generali copre circa il 90 % con meno di 2,5 s | Sostenuto dai dati (91,7 %, 1,24 s; taratura e prova dalla stessa distribuzione) |
| Lo sguardo a priorità riduce di almeno il 30 % l'errore sul più minaccioso | Sostenuto dai dati (48,4 %), con un costo sugli altri |
| Tre timbri e battito si riconoscono al 90 % | Non risolto: servono 3 persone e 5 minuti |
| Tre ToF multizona coprono 360° | Non risolto: lo decide la scheda tecnica del sensore scelto |

## 4. Proposte
**creativo-1 — «Il libero costa energia»** (segnalamento ferroviario a sicurezza intrinseca; contatore Geiger). R6, R8, R4, R5.
- *Analogia:* il relè di binario diseccitato dà l'aspetto più restrittivo; il «via libera» esiste solo finché arriva energia (49 CFR 236.205, non verificato sul testo).
- *Meccanismo:* entra lo stato per settore (libero osservato, occupato a distanza d, previsto con σ, sconosciuto) con l'età dell'ultimo fotogramma. Esce un canale audio o aptico: battito sommesso ogni 0,5 s solo se il settore davanti è osservato libero e il fotogramma è fresco; occupato = clic nitidi con ritmo ∝ 1/d; previsto = stesso ritmo, suono sfocato, durata ∝ σ; sconosciuto = battito sospeso più ronzio grave. Il battito lo genera un processo separato che si spegne da solo senza dati freschi. Costruzione: un pomeriggio (stima).
- *Perché gli specialisti non ci arrivano:* pensano l'uscita come rilevamento, quindi allarme a evento.
- *Dove si rompe:* un suono continuo copre l'udito ambientale che chi non vede usa (ripiego: vibrazione al polso); assuefazione.
- *Prova e falsificatore:* P-creativo-1. Non eseguita. Vagliano: interfacce, sicurezza, tempo-reale.

**creativo-2 — «Il sottomarino perduto»** (ricerca bayesiana, USS Scorpion; nebbia di guerra dei giochi di strategia). R3, R4, R8, R7.
- *Analogia:* cercare in una cella e non trovare sposta la probabilità sulle celle non cercate: p′ = p(1−q)/(1−pq), r′ = r/(1−pq).
- *Meccanismo:* la traccia nascosta diventa 300–1000 particelle (posizione, velocità, modo fermo o in moto). A ogni fotogramma la profondità dice quali celle sono viste libere: lì le particelle pesano (1−Pd). Esce P(ancora nell'ombra) e la regione dove può essere. Regola: il «previsto» non si disegna mai dove si osserva libero.
- *Perché gli specialisti non ci arrivano:* un tracciatore aggiorna le tracce con ciò che rileva; il mancato rilevamento lo usa solo per contare l'età della traccia.
- *Esito:* massa in celle osservate libere a 3 s: Kalman 100 %, particelle con evidenza negativa 0,1 %. Senza evidenza negativa, a parità di modello, 90 %: conta l'evidenza negativa, non il modello del moto. Costo: 1000 particelle a 15 Hz stanno sotto l'1 % di un core (stima dal tempo totale, non un profilo).
- *Dove si rompe:* un falso «libero» (superficie scura o lucida non rilevata) uccide l'ipotesi giusta; in 2D serve la visibilità per raggio; due bersagli che si scambiano nell'ombra.
- *Falsificatore:* P-creativo-2a, regge. Vagliano: tracciamento, kalman, avversario.

**creativo-3 — «La buca dichiarata e la moviola»** (biliardo, VAR, taratura dei meteorologi). R3, R4, R6.
- *Meccanismo:* quando il soggetto entra nell'ombra il sistema sigilla e mostra una scommessa: «riemerge a destra fra 1,6 e 2,9 s». Una seconda camera oltre il pannello mostra alla giuria la verità nascosta; il sistema non la usa. Un tabellone conta scommesse vinte e perse. Terzo passaggio: il soggetto si ferma, e a finestra scaduta il sistema dice «ancora dietro, non lo vedo». Quarto: una mano sul sensore, il battito tace. Quattro passaggi in tre minuti (stima, non provata).
- *La finestra* viene dai quantili 5–95 % del rapporto fra tempo vero e tempo nominale su circa 100 passaggi di prova generale.
- *Perché gli specialisti non ci arrivano:* una demo di tracciamento mostra il riquadro che riappare; qui la previsione si espone prima, e la giuria vede anche quando sbaglia.
- *Esito:* Kalman 69,3 % (0,40 s); particelle 100 % (6,27 s); tarata 91,7 % (1,24 s).
- *Dove si rompe:* un giurato che cammina in modo diverso dalle prove generali; il tabellone lo mostra in pubblico.
- *Falsificatore:* P-creativo-3bis, regge. Vagliano: validazione, statistico.

**creativo-4 — «Il ronzio terminale»** (pipistrello in caccia; fovea e saccade). R7, R5.
- *Analogia:* il pipistrello alza il ritmo dei richiami in avvicinamento, oltre 90 e poi oltre 160 al secondo.
- *Meccanismo:* a ogni ciclo un solo «sguardo costoso» (classificatore su un ritaglio, o modo rapido del sensore) va alla traccia con varianza / tempo al contatto massimo, con un'età massima di guardia per le altre. Entra la lista delle tracce, esce l'indice da guardare. Venti righe.
- *Perché gli specialisti non ci arrivano:* la catena di percezione tratta ogni fotogramma e ogni traccia allo stesso modo, e cerca il risparmio nel modello più piccolo.
- *Esito:* errore sul più minaccioso −48,4 % (da 0,060 a 0,031 m); sugli altri +158 % (da 0,059 a 0,151 m). La guardia non è provata.
- *Dove si rompe:* una minaccia nuova fra le tracce affamate. Il passaggio 8×8 a 15 Hz → 4×4 a 60 Hz del VL53L5CX è non verificato sul testo.
- *Falsificatore:* P-creativo-4, regge. Vagliano: tempo-reale, ottimizzazione, sensori.

## 5. Che cosa propongo dopo
1. La prova con 3 persone bendate (5 minuti): decide creativo-1.
2. L'avversario attacchi creativo-2 con il falso «libero»: è il suo punto debole per R8.
3. Rifare 2a in 2D su un fotogramma di profondità vero.
4. Provare la guardia d'età di creativo-4.

**Fonti.** [Bayesian search theory](https://en.wikipedia.org/wiki/Bayesian_search_theory) (letta) · [Hulgard e Ratcliffe, Sci Rep 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC4746672) (letta) · [49 CFR 236.205](https://www.customsmobile.com/regulations/49/236.205) e [ST UM2884](https://st.com/resource/en/user_manual/um2884-a-guide-to-using-the-vl53l5cx-multizone-timeofflight-ranging-sensor-with-a-wide-field-of-view-ultra-lite-driver-uld-stmicroelectronics.pdf) (non verificate sul testo).
