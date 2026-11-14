# PREVISIONI — sciame-validazione, f10/20-validazione

**Scritte alle 2026-11-14T16:48:19+01:00 (`date -Is`), prima di far girare la catena su qualunque sequenza.**
Fin qui ho solo letto: contratto, `CATENA.md` e il codice della catena, `SIMULATORE.md`, `DATI_VERI.md`,
`AMBIENTE.md`, il nucleo e il verdetto, un `meta.json` e la struttura di un `verita.json` (nessuna profondità).
Gli esiti si aggiungono in fondo, con l'ora; ciò che noto dopo è marcato «dopo».

Unità statistica: la **sequenza** (un passaggio = una sequenza); per THÖR il **tratto nascosto** (finestre non
sovrapposte), con l'intervallo ricampionato per **persona** (9 per file). Intervalli: Wilson al 95 % per le quote.
Esiti: regge / smentita / non decidibile.

## Definizioni delle misure (fissate ora)

- **Ombra vera** (simulato): classi 1 («in ombra») e 3 («impronta») di `verita.json → ombra_suolo`. Una cella polare
  della catena è «tutta in ombra» se tutti i campioni della maschera cartesiana (2,5 cm) che le cadono dentro sono
  di classe 1 o 3; «al bordo» se lo è solo una parte. **K-014 = celle·fotogramma «libero» fra le celle tutte in ombra.**
- **Errore del bordo d'ombra**: per fotogramma e per lato, azimut dell'ultima colonna il cui primo ritorno è il
  pannello meno l'azimut vero dello spigolo (da `ostacoli`), in centimetri alla distanza di 2,4 m; **positivo =
  ombra stimata più larga della vera** (verso sicuro), negativo = più stretta. Solo fotogrammi senza soggetto
  visibile (frazione visibile < 0,02) o senza soggetti.
- **Nascosto**: `frazione_visibile < 0,02` (come chiede il simulatore). **Errore della previsione**: distanza fra la
  `previsione_diagnostica` e la verità, tolto lo scarto sistematico centro misurato − centro vero stimato sui
  fotogrammi interi dello stesso passaggio prima dell'ombra. **Regione al 90 %**: ellisse χ²(2) = 4,605 della
  covarianza dichiarata (la catena dichiara un cerchio al 95 %: riporto tutti e due).
- **Identità alla ricomparsa**: nel primo fotogramma dopo l'ombra con frazione visibile ≥ 0,5 e una traccia
  «osservato» entro 0,5 m dalla verità, quella traccia ha l'identità che il soggetto aveva prima dell'ombra.

## Previsioni e soglie

| # | Enunciato | Misura | Regge se | Smentita se | Che cosa prevedo |
|---|---|---|---|---|---|
| V1 | Nessun invariante scatta | codice d'uscita / `InvarianteViolato` sulle 162 simulate e sulle 8 vere | 0 | ≥ 1 | 0 |
| V2 | **K-014**: nessun «libero» dentro l'ombra vera, filtri spenti | celle·fotogramma «libero» tutte in ombra, sequenze con pannello o cassa, tre profili, nominale e limite | 0 | ≥ 1 | 0 al nominale; 0 anche al limite (incerto); al bordo ≤ 1 % delle celle·fotogramma di bordo |
| V3 | Con i **filtri del costruttore** accesi nasce «libero» dove il sensore non ha dato | «libero» nelle celle di classe 4 (banda stereo) e 1/3, coppie con e senza filtri | — | — | con i filtri > 0 in classe 4 in almeno una coppia; in classe 1/3 resta 0 (incerto) |
| V4 | Il sensore coperto non lascia «libero» | celle «libero» dal 3° fotogramma tutto a zero in poi (`sensore_coperto`, `azzeramento_progressivo`); metà coperta: «libero» negli azimut coperti dal 3° fotogramma | 0 | ≥ 1 | 0 |
| V5 | Vetro | `vetro_sfondo`: stato delle celle dell'impronta della lastra e del cuneo dietro; `vetro_buco`: «libero» nelle celle tutte dietro la lastra | — | — | `sfondo`: la lastra non è mai «occupato» e dietro è «libero» in ≥ 90 % dei fotogrammi (limite dichiarato, confermato); `buco`: 0 «libero» dietro |
| V6 | Persona vestita di scuro | traccia confermata e cella del centro vero mai «libero» a soggetto visibile; `scuro`, `nero`, `lim scuro` | traccia in 5 su 5; 0 fotogrammi | meno; ≥ 1 | regge (il nero con più buchi, ma tracciato) |
| V7 | Pavimento vuoto: copertura e falsi | quota di celle di classe 0 (entro 3 m) dette «libero», per fascia 1,3–2 e 2–3 m; celle·fotogramma «occupato» su pavimento vuoto; tracce confermate fantasma | falsi occupati 0 e 0 tracce | ≥ 1 traccia confermata | **D435i e Gemini al nominale: smentita** (rumore fisso oltre 2 m → celle occupate false persistenti, 0,1–5 % delle celle fra 2 e 3 m, e almeno una traccia fantasma); D455: regge; «libero» 2–3 m: 60–90 % (D435i nom.), ≥ 90 % (D455), < 30 % al limite |
| V8 | **Errore del bordo d'ombra entro ±20 cm** (ipotesi delle simulazioni idealizzate) | per sequenza, 5° e 95° percentile sui fotogrammi, per lato | in ≥ 95 % delle sequenze il 5°–95° sta entro ±20 cm | altrimenti | regge al nominale: mediana entro ±5 cm, 5°–95° entro ±10 cm, lato sinistro più largo di qualche cm (banda stereo, ingrossamento); al limite entro ±20 cm |
| V9 | Rumore del centro di una persona **ferma** (D435i nominale, simulato) a 2 / 3 / 4 m | scarto tipo nel tempo del centro del gruppo, radiale e trasversale, 20 semi per distanza | — | — | radiale < 1 / < 2 / < 4 cm (sotto la curva nominale 1,5 / 3,4 / 6,0: il centro media molti pixel); trasversale < 1 cm |
| V10 | Regola «si muove», falsi su oggetti fermi a 2 / 3 / 4 m | sequenze (persona ferma; scatola) con almeno un `si_muove = true`, su 20 per distanza | ≤ 10 % (soglia R1 del nucleo) | limite inferiore dell'intervallo > 10 % | 0 su 20 a ogni distanza |
| V11 | Persona a 0,5 m/s vista «si muove» entro 1 s dalla prima misura, a 2 / 3 / 4 m | passaggi con `si_muove = true` entro 1 s dalla nascita della traccia; attraversamento e avvicinamento; 20 per cella | ≥ 9 su 10 (R1) | limite superiore dell'intervallo < 90 % | attraversamento: regge a 2, 3, 4 m; avvicinamento: regge a 2 e 3 m, **smentita a 4 m** (soglia 42 cm contro 50 cm di spostamento in 1 s, meno la media di 3) |
| V12 | Identità alla ricomparsa, passaggi simulati (a12, a05, b: 30 l'uno; D435i nominale) | passaggi con la stessa identità | ≥ 28 su 30 (criterio del nucleo) | ≤ 22 su 30 | **smentita su a12** (riaggancio letterale L8 fragile con il rumore realistico: celle non osservate entro 0,40 m); idealizzato: 100 % |
| V13 | Errore della previsione alla ricomparsa (q = 0,2), simulato | distanza previsione − prima misura piena, per passaggio | — | — | a12: mediana < 0,3 m; a05: < 0,3 m; b (sosta di 3 s): > 1 m nella maggior parte; «fermo all'ultima posizione» peggio su a12 (≈ 1 m) e meglio su b |
| V14 | Copertura della regione al 90 % dichiarata, simulato | quota dei fotogrammi nascosti (per passaggio) e dei passaggi alla ricomparsa con la verità dentro l'ellisse | 0,85–0,97 | fuori | a12 e a05: > 0,97 (regione troppo larga: smentita nel verso innocuo); b: < 0,5 (smentita nel verso pericoloso) |
| V15 | **q = 0,2 su pedoni veri (THÖR, prova su exp3)**: la regione al 90 % è calibrata a 1, 2, 3 s | copertura per tratto nascosto, rincorsa di 1 s a 15 Hz, rumore di misura 2 cm | 0,85–0,97 a tutti e tre gli orizzonti | < 0,85 (pericoloso) o > 0,97 (troppo larga) | **> 0,97 a 1 s; ≥ 0,90 a 2 e 3 s**: q = 0,2 non è troppo piccolo; il q tarato su exp1 esce fra 0,05 e 0,2 |
| V16 | Errore della previsione su pedoni veri (THÖR exp3), q = 0,2 | mediana dell'errore a 1 / 2 / 3 s | — | — | 0,1–0,3 / 0,3–0,8 / 0,6–1,5 m; «fermo»: peggio a ogni orizzonte (≈ 1 m per secondo); velocità costante senza rumore di processo: errore entro ±20 % del filtro, copertura della sua regione < 0,5 a 2 s |
| V17 | Ostacoli per scena | cella «occupato» entro 15 cm dall'ostacolo vero, in ≥ 9 fotogrammi su 10 | sì | no | cassa: sì; `sospeso_2p8m`: sì; `scatola15_2p0m`: sì; `sospeso_2p0m`: **no, e sotto è «libero»** (limite dichiarato: visto solo oltre 2,41 m); `scatola15_0p8m`: no, e la sua cella è «non osservato» (0 «libero») |
| V18 | Pannello fermo mai «si muove» | passaggi con una traccia sul pannello detta «si muove» | ≤ 10 % | limite inferiore > 10 % | ≤ 2 % (idealizzato: 0,0–0,2 %) |
| V19 | Costo su questa macchina (un filo; non è la scheda di bordo) | media e 95° percentile per ciclo | p95 ≤ 66 ms (15 Hz) | p95 > 66 ms | media < 5 ms a 424×240, < 10 ms a 640×480, < 25 ms a 1280×720 |
| V20 | Dati veri, descrittivo | la catena passa le 8 sequenze; la stima del suolo dove la posa manca | — | — | 0 invarianti; la stima del suolo fallisce o dà una posa implausibile in ≥ 2 delle 7 senza posa; TUM (posa per fotogramma): mediana 50–600 celle «libero» a 3 m |
| V21 | Identità sui tratti nascosti veri (DepthTrack ×3, Princeton ×1) | stessa identità prima e dopo | — | — | non decidibile (N = 4, tratti di 0,03–0,17 s, verità non indipendente); lo registro |

Bracci che devono fallire: per V2, le coppie con i filtri (V3); per V12, la stessa misura con
`min_celle_altro_bordo` grande (regola del bordo spenta), che deve far risalire l'identità; per V15, q = 0,01, che
deve dare una copertura sotto 0,85.

## Aggiunte dopo la prima corsa (scritte alle 2026-11-14T16:56:20+01:00, prima delle corse che decidono)

Notato **dopo** la prima corsa della catena sulle 162 simulate (non era previsto): (a) il gruppo della persona si
**fonde con quello del pannello** quando le due sagome si toccano nell'immagine (celle ponte fatte di pixel misti);
(b) lungo il raggio dello spigolo del pannello nascono **gruppi fantasma** di 1–5 celle, marcati «tagliato», e la
traccia pendente vi si **riaggancia a soggetto nascosto**; (c) i fantasmi sul pavimento (previsti in V7) fanno decine
di tracce pendenti. La mia misura dell'identità (V12) sceglieva la traccia «prima» dall'ultimo fotogramma utile e
contava «stessa» anche dopo un riaggancio falso: la correggo PRIMA di leggere altri numeri (identità «prima» = la
più frequente sui fotogrammi interi; esito «continuità pulita» = stessa identità alla ricomparsa **e** nessun
riaggancio né fotogramma «osservato» mentre il soggetto è nascosto).

| # | Enunciato | Misura | Soglia | Previsione |
|---|---|---|---|---|
| V22 | Le celle ponte sono pixel misti | passaggi a12 rigenerati in memoria con l'interruttore «bordi» spento (D435i nominale, 10 passaggi): passaggi con fusione persona–pannello prima dell'ombra | — | con i bordi spenti la fusione sparisce in ≥ 8 su 10; con i bordi accesi c'è in ≥ 8 su 10 |
| V23 | Due soglie della catena (letture L1 e L4, non numeri del nucleo) tolgono fantasmi e ponti | `min_punti_ostacolo` ∈ {3, 8, 20, 40} × `min_celle_gruppo` ∈ {1, 3}; **taratura** su: scene vuote dei tre profili, `scatola15_2p0m`, `sospeso_2p8m`, `cassa_persona`, passaggi PARI di a12, a05, b; **prova** sui passaggi DISPARI | scelta: la coppia con 0 tracce fantasma sulle scene vuote al nominale, scatola e sospeso ancora visti in ≥ 9 fotogrammi su 10, e la più alta quota di «continuità pulita» sui pari; a parità, la soglia più bassa | vince `min_punti_ostacolo` = 20 o 40; sui dispari la continuità pulita su a12 sale da < 20 % a ≥ 70 %, ma resta sotto 28 su 30 |
| V24 | Sensore coperto **con i filtri del costruttore accesi** | `sensore_coperto` rigenerato in memoria con i filtri: celle «libero» dal 3° fotogramma coperto in poi | 0 | **> 0: smentita** (la persistenza del filtro temporale tiene vivo il dato; è la condizione 1 del verdetto) |

## Regola per tarare q su THÖR (scritta alle 2026-11-14T17:14:14+01:00, prima di aprire le tracce)

Banco: tracce a 15 Hz, finestre non sovrapposte di 4 s per persona (1 s di rincorsa con misure rumorose, σ = 2 cm
per asse, R del filtro uguale; poi 3 s senza misure), filtro `kalman.py` della catena. Griglia di q: 0,01; 0,05;
0,1; 0,2; 0,5; 1; 2; 5 m²/s³. **Si sceglie su exp1_run1 il q che rende minima la media, su 1, 2 e 3 s, di
|copertura dell'ellisse al 90 % − 0,90|; lo si prova su exp3_run1** (altre persone? non verificato: stessi
esperimenti, giorni e ruoli diversi secondo la fonte, non riaperta). Intervalli: ricampionamento per persona
(2000 repliche). Sottoinsieme «in cammino»: velocità media nella rincorsa > 0,3 m/s. Sensibilità: σ = 0,5 e 5 cm.

## Esiti (scritti alle 2026-11-14T17:24:15+01:00; cifre e file in VALIDAZIONE_DATI.md)

| # | Esito | Cifra |
|---|---|---|
| V1 | **regge** | 0 invarianti su 162 simulate (anche con soglia 40) e sulle vere elaborate; la stima del suolo solleva un errore su `realsense_stands_still` (non è un invariante) |
| V2 | **regge** con i parametri del nucleo; **smentita** con `min_punti_ostacolo` = 40 | 0 celle·fotogramma su 2 907 032 (135 sequenze); con soglia 40: 2 (e 45 al bordo), dietro la scatola di 15 cm non più rilevata |
| V3 | **smentita** (la mia previsione): nessuna differenza misurabile nella banda | classe 4: 49 e 49; celle diverse fra le coppie 0,09–0,21 % |
| V4 | **regge** | 0 «libero» dal 3° fotogramma a zero; metà coperta: 0 dal 3° |
| V5 | **regge** (limite confermato) | `vetro_sfondo`: impronta «libero» 420 su 420, dietro 1794 su 1800; `vetro_buco`: dietro 0 «libero» su 1800 |
| V6 | **smentita** con i parametri del nucleo (traccia rubata come per i chiari), **regge** con soglia 40 al nominale | cella del centro mai «libero» (0 su 9152 fotogrammi); continuità pulita 0 su 4 → 4 su 4; al limite 0 su 1 |
| V7 | **smentita** per D435i e Gemini, **regge** per D455 (come previsto) | tracce fantasma sul pavimento vuoto: 28 / 26 / 0; al limite 43 |
| V8 | **regge** al nominale; al limite **non decidibile** con i parametri del nucleo (pannello a pezzi), regge con soglia 40 | nominale: da +2,0 a +14,6 cm, 103 su 103; limite con soglia 40: da +2 a +14,6, 8 su 8 |
| V9 | **regge** | 0,13 / 0,36 / 0,69 cm radiale (soglia 40); 0,36 / 0,99 / 1,25 con i parametri del nucleo |
| V10 | **regge** | persona 0 su 20 a 2, 3, 4 m; scatola 0 su 20 a 2 m, 1 su 20 a 3 m |
| V11 | **regge** in attraversamento; **smentita** in avvicinamento da 4,3 m (come previsto) | 20 su 20; 4 su 20 (soglia 40), 0 su 20 (nucleo) |
| V12 | **smentita** (come previsto, ma per un'altra causa: fusione e fantasmi, non le celle non osservate) | 0 su 30 (a12, a05, b) |
| V13 | regge solo con soglia 40 | a12 0,18 m; a05 0,22; b 4,20 (fermo: 1,7 / 1,7 / 1,7) |
| V14 | a12, a05: **regge la previsione** (> 0,97); b: **smentita la previsione** (copre 1,00: la regione è più grande della stanza) | mediana 1,00 |
| V15 | **regge la previsione**: q = 0,2 copre troppo | 0,977 / 1,000 / 1,000; q tarato 0,05 → 0,795 / 0,804 / 0,831 |
| V16 | **regge** | 0,21 / 0,49 / 0,81 m; fermo 0,91 / 1,79 / 2,62; senza rumore di processo 0,18 / 0,45 / 0,76, copertura 0,16 / 0,10 / 0,09 |
| V17 | **regge**, salvo `sospeso_2p0m` «visto» 7 su 10 per fantasmi del pavimento | cassa 84 su 84; sospeso 2,8 m 10 su 10; scatola 2 m 10 su 10; sotto il sospeso a 2 m «libero» nel 97,5 % |
| V18 | **smentita** con i parametri del nucleo; regge con soglia 40 | 79 su 90; 5 su 90 |
| V19 | **regge** sul simulato e su 7 vere; **smentita** su DepthTrack con i parametri del nucleo | p95 18,6 ms (simulato); 152 ms (DepthTrack, 4 m) |
| V20 | **regge** | pose implausibili o fallite in almeno 3 su 7; TUM mediana 58 celle «libero» |
| V21 | **non decidibile** (come previsto) | 2 tratti su 2 con la stessa identità (soglia scalata), 0 su 2 con i parametri del nucleo |
| V22 | **regge** | fusione 10 su 10 → 1 su 10 con i bordi spenti |
| V23 | **smentita** nella regola dichiarata (la coppia scelta, 20 e 1, dà 0 su 45 sui dispari); fuori regola, soglia 40: 41 su 45 | vedi rapporto |
| V24 | **regge la previsione** (smentito lo «zero») | 3 fotogrammi su 16 con 989–995 celle «libero» |
