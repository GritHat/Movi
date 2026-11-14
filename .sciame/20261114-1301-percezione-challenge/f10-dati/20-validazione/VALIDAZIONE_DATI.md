# VALIDAZIONE_DATI — f10, `20-validazione` (`sciame-validazione`), 14 novembre 2026, 16:44–17:26

Percorsi relativi a `f10-dati/20-validazione/`. Si rifà con `sh rifai.sh` (i passi, ciascuno con il suo `timeout`).
Previsioni V1–V21 scritte alle 16:48:19, prima di ogni corsa; V22–V24 e la regola per q aggiunte dopo la prima
corsa e prima delle prove che decidono (`PREVISIONI.md`, con gli esiti). Uscite grezze in `uscite/`.

## 0. Cambi di stato, scostamenti, regole violate

- **K-014** («libero» dentro l'ombra vera): da «non decidibile senza hardware» a **sostenuta in simulazione con rumore
  realistico** (0 celle·fotogramma su 2 907 032), **con un controesempio** quando l'ostacolo non è rilevato (2). Sul vero: aperta.
- **Identità alla ricomparsa «100 %, almeno 99,25 %»: smentita** sulla profondità realistica con la catena così com'è
  (0 passaggi su 90). Con una soglia cambiata: 41 su 45 sui passaggi di prova.
- **«Muro mobile 0,0–0,2 %»: smentita** (79 passaggi su 90 con il pannello detto «si muove»).
- **q = 0,2**: su pedoni veri (THÖR) la regione al 90 % copre il 98–100 %: non è troppo piccolo, è troppo grande.
- **Errore dell'ombra ±20 cm**: regge; l'errore è sempre verso il largo (+2…+15 cm).
- *Scostamenti.* (a) La soglia `min_punti_ostacolo = 40` sta **fuori dalla regola di scelta che avevo scritto** (V23): la
  regola sceglieva 20, che fallisce; 40 è marcata «a posteriori», ma è provata su passaggi diversi da quelli di
  taratura. (b) Ho **corretto la mia misura dell'identità dopo la prima corsa** (prima: «stessa» 1 su 30 in a12; dopo:
  0 su 30), dichiarandolo prima di rileggere i numeri. (c) Una corsa sulle sequenze vere è scaduta a 295 s: rifatta con
  un tetto di 120–320 cicli per sequenza; l'uscita della prima non è conservata. (d) Ho importato il simulatore di
  `11-simulatore` e ne ho sostituito **in memoria** `catalogo.passaggio` per aggiungere percorsi; nessun suo file è
  cambiato. (e) Ho cancellato le cartelle intermedie della taratura (rigenerabili) e messo un `.gitignore` qui.
  (f) Lunghezza al limite delle quattro pagine (circa 3200 parole, in gran parte tabelle).
- **Violata per errore:** nel controllo finale ho lanciato `git -C <cartella>` senza sottocomando (stampa solo l'uso:
  nessuna azione). Niente rete, sudo, GPU; `f7`–`f9` non lette; i dati scaricati solo letti (`-I`, senza pickle). Catena: 0 invarianti
  violati su 162 sequenze simulate e sulle vere (V1 regge); non ho corretto nessun file della catena.
- *Indipendenza.* Verità del simulato: geometria del simulatore (altro autore rispetto alla catena, stesso modello
  linguistico); le classi d'ombra le ricalcolo dalla maschera cartesiana. THÖR: indipendente dal filtro. Le sequenze
  vere con persone **non hanno verità indipendente**.

## 1. Da quale sensore viene ogni numero, e che cosa NON dice

| Fonte | Che cos'è | Che cosa non dice del sensore della squadra |
|---|---|---|
| **Simulato** D435i, D455, Gemini 335 (da scheda), 424×240, nominale e limite; 162 sequenze, 9152 fotogrammi, più circa 190 generate in memoria | verità esatta | niente accoppiamento stereo vero; persone = capsule rigide; posa esatta; **rumore oltre 60° d'incidenza e pixel misti ai bordi sono ipotesi senza misura** (`SIMULATORE.md` §2, §5): da essi dipendono i fantasmi sul pavimento e la fusione col pannello |
| **THÖR** exp1 (taratura), exp3 (prova): cattura del moto a 100 Hz, 9 persone l'uno | solo traiettorie vere (caschi) | niente su rilevamento, ombra, identità; occlusioni create da me |
| **TUM** fr3 walking_static: Kinect v1, a mano, 1,42 m e 8° | posa vera per fotogramma, nessuna verità della scena | altro principio (luce strutturata), altra posa |
| **DepthTrack** human02 (D415 stereo attivo), **Princeton** (Kinect v1), bag RealSense (D435i, D435, SR300) | riquadro annotato o niente; **posa ignota** | solo descrittivo: la posa stimata è implausibile (§3, critica 6) |

## 2. Risultati (unità: la sequenza o il passaggio; intervalli di Wilson al 95 %)

**(1) «Libero» da una profondità realistica** — `uscite/sim*/misura_libero.txt`, `misura_ombra.txt`, `mem_coperto_bordi.txt`, `misure_brevi.txt`

| Misura | Cifra | Esito |
|---|---|---|
| Celle «libero» **tutte dentro l'ombra vera** (K-014), filtri spenti, 3 profili, 2 livelli | **0 su 2 907 032** celle·fot., 135 sequenze (per sequenza: 0–2,8 %); al bordo 0 su 356 736. Controllo che deve fallire (ombra vera ruotata di 12°): 1024 | **regge** |
| Lo stesso con `min_punti_ostacolo` = 40 | **2** celle·fot. (e 45 al bordo) in 1 sequenza su 135: `scatola15_2p0m`, cella (90, 23), fotogrammi 1–2 | **smentita** in quella variante |
| «Libero» su celle del tutto non osservabili per la verità (fuori campo) | 1,1 (D455), 2,4 (D435i), 23 (Gemini; D435i al limite) celle per fotogramma, **mai a più di una cella** dall'osservabile | smentita in senso stretto: vale «a meno di 10 cm» |
| Celle per stato, pavimento vuoto (5400 celle): libere / occupate / in ombra | D455 1604 / 0 / 0; D435i 1568 / **19** / 15; Gemini 1628 / 17 / 25; D435i limite 502 / **585** / 471 | — |
| Suolo visibile detto «libero», 1,3–2 m e 2–3 m | nominale 100 % e 95–100 %; limite 66,5 % e **4,7 %**; pavimento lucido 98,8 % e 52,4 % | portata utile del «libero» al limite: 2 m |
| **Falsi ostacoli sul pavimento vuoto** → tracce confermate | D435i 28 in 2 s, Gemini 26, **D455 0**; limite 43 in 1,3 s | **smentita** per D435i e Gemini (dipende dall'ipotesi sull'incidenza) |
| Sensore coperto, azzeramento progressivo, metà coperta | 0 «libero» dal 3° fotogramma senza dato (3 sequenze) | **regge** |
| Sensore coperto **con i filtri del costruttore accesi** | 989–995 celle «libero» per altri 3 fotogrammi (5 in tutto, 0,33 s), con tracce «osservato» | **smentita**: la condizione 1 del verdetto è necessaria |
| Filtri accesi su scene normali (5 coppie) | 0,09–0,21 % di celle diverse; K-014 resta 0 | nessun effetto misurabile a 1° |
| Vetro | `sfondo`: «libero» 420 su 420 sull'impronta e 1794 su 1800 dietro; `buco`: dietro 0 «libero», ma la cella della lastra «libero» 323 su 420 | limite dichiarato, **confermato** |
| Persona scura o nera | cella del centro vero mai «libera»: 0 su 9152 fotogrammi (tutti i soggetti) | regge |
| **Vero**, TUM (Kinect): «libero» per fotogramma | mediana **58** celle con la posa vera per fotogramma; **0** con la posa mediana (6° di scarto); suolo stimato dai primi 5 fotogrammi: 1,56 m e 19,5° contro 1,38 m e 14,5° veri | K-014 **non decidibile** (nessuna verità d'ombra) |

**(2) Errore del bordo d'ombra** (cm a 2,4 m; + = stimata più larga) — `misura_ombra.txt`. Nominale, 115 sequenze e 3742
fotogrammi (D435i 103, D455 6, Gemini 6): mediana +6,2, minimo +2,0, massimo +14,6 su entrambi i lati; D435i **103 su 103**
(96,4–100 %) entro ±20 cm, D455 e Gemini 6 su 6; **0 fotogrammi sotto −10 cm**. Nessuna asimmetria fra i lati a questa risoluzione (banda
stereo di 4 px, meno di 1°). Limite (8 sequenze): con i parametri del nucleo il pannello è visto a pezzi (primi ritorni
fantasma davanti: misura non valida, da −65 a +73), ma le celle d'ombra vera restano al 100 % «in ombra» od «occupato»;
con soglia 40: da +2 a +14,6, 8 su 8. **Regge**; il verso stretto (−20 cm) non compare.

**(3) Rumore del centro e regola «si muove»** — `mem_fermi.txt`, `mem_lenti.txt`, `misura_passaggi.txt`, `vere/RIEPILOGO.txt`

| | 2 m | 3 m | 4 m |
|---|---|---|---|
| Curva nominale usata dal nucleo (radiale) | 1,5 cm | 3,4 | 6,0 |
| Simulato D435i, persona ferma, 20 semi: radiale, mediana (massimo) | 0,36 (7,0) | 0,99 (5,6) | 1,25 (10,4) |
| lo stesso con soglia 40; trasversale | 0,13; 0,16 | 0,36; 0,29 | 0,69; 0,43 |
| Falsi «si muove»: persona ferma / scatola di 15 cm | 0 su 20 / 0 su 20 | 0 su 20 / 1 su 20 | 0 su 20 / — |
| Persona a 0,5 m/s vista entro 1 s, attraversando | 20 su 20 (83,9–100 %) | 20 su 20 (soglia 40) | 20 su 20 (soglia 40) |

In moto (90 passaggi, 2,3–2,9 m): 0,2 cm radiale e trasversale; scarto sistematico −16,5 cm (la superficie davanti).
**In avvicinamento da 4,3 m: 4 su 20** (8–42 %) con soglia 40, **0 su 20** con i parametri del nucleo (ritardo mediano
2,97 s; 34 % delle misure «tagliate» dalle ombre dei fantasmi); sotto 3,5 m è detta «si muove» nel 100 % dei fotogrammi
(soglia 40). Non misurato: attraversamento a 3 e 4 m con i parametri del nucleo. **Vero, descrittivo** (nessuna verità;
include il moto del corpo; posa stimata): persona che cammina, D415, sotto 3 m: **5,8–6,8 cm radiale**, 2,0–2,2
trasversale (288 fotogrammi, una sequenza); Kinect: 1,4–3,5 cm. *Esito:* la regola regge in simulazione fino a 3,5 m e
cade a 4 m in avvicinamento; **K-007 resta aperta**: il solo dato vero sta sopra la curva nominale e sopra i 5 cm della
portata dichiarata, e il simulato (capsula rigida) è un limite inferiore.

**(4) Previsione durante l'occlusione** — (a) simulato D435i nominale, 30 passaggi per caso — `misura_passaggi.txt`, `taratura_*.txt`

| Caso | Continuità pulita¹, parametri del nucleo | soglia 40: prova (dispari); tutti | Centro nascosto in «possibile presenza» (soglia 40) | Errore alla prima misura dopo: nucleo / fermo / retta² | «Previsto» dura |
|---|---|---|---|---|---|
| a12 (1,2 m/s, nascosto 0,73 s) | **0 su 30** (0–11,4 %) | 13 su 15; 28 su 30 | 328 su 328 | 0,18 / 1,71 / 0,14 m | 0,40 s |
| a05 (0,5 m/s, 1,7 s) | 0 su 30 | 13 su 15; 24 su 30 | 793 su 793 | 0,22 / 1,68 / 0,20 | **0,00 s** |
| b (sosta di 3 s, 4,3 s) | 0 su 30 | 15 su 15; 28 su 30 | 1917 su 1917 | **4,20** / 1,73 / 4,04 | 0,40 s |

¹ stessa identità alla ricomparsa, nessun riaggancio né fotogramma «osservato» a soggetto nascosto; «tutti» comprende i 15 passaggi pari usati per tarare. ² retta ai minimi
quadrati sulle ultime 8 misure piene. Prova: **41 su 45** (79,3–96,5 %); con il criterio del nucleo sui 30: a12 e b
reggono (28), a05 chiede altri 30 (24). Al limite: 0 su 6 anche con soglia 40. Errore contro il tempo dal primo fotogramma
nascosto (soglia 40, mediana): a12 0,08 / 0,11 / 0,12 m a 0,25 / 0,5 / 0,75 s (fermo 0,62 / 0,93 / 1,17); b 0,09 / 0,17 /
0,42 / 0,67 / 1,34 / 2,54 / 3,78 m fino a oltre 3 s (fermo 0,62–0,94). Regione al 90 %: mediana **1,00** in ogni caso,
anche in b. Con i parametri del nucleo il centro nascosto sta in «possibile presenza» in 2939 fotogrammi su 3038, «in
ombra senza avviso» in 99, **mai «libero»**; «osservato» a soggetto nascosto in 8 passaggi su 90 (0 con soglia 40).

(b) **pedoni veri, THÖR exp3**: 219 tratti di 3 s, 9 persone, rincorsa di 1 s, σ = 2 cm — `banco_thor.txt`

| q (m²/s³) | Copertura della regione al 90 % a 1 / 2 / 3 s (IC per persona) | Raggio al 95 % | Errore mediano (90° percentile) |
|---|---|---|---|
| **0,2 (nucleo)** | 0,977 (0,94–1,00) / 1,000 / 1,000 | 0,75 / 1,96 / 3,49 m | 0,21 (0,46) / 0,49 (1,11) / 0,81 (1,89) m |
| 0,05 (tarato su exp1: 0,855 / 0,881 / 0,877) | 0,795 (0,72–0,86) / 0,804 (0,75–0,87) / 0,831 (0,78–0,90) | 0,41 / 1,02 / 1,80 | 0,19 / 0,44 / 0,72 |
| 0,1 (a posteriori) | 0,945 / 0,945 / 0,945 | 0,55 / 1,41 / 2,50 | — |
| 0,01 (deve fallire) | 0,534 / 0,521 / 0,516 | | |

Fermo all'ultima posizione: 0,91 / 1,79 / 2,62 m. Velocità costante senza rumore di processo: 0,18 / 0,45 / 0,76 m, ma la
sua regione copre 0,16 / 0,10 / 0,09. Con σ fra 0,5 e 5 cm la copertura cambia al più di 0,07. *Esito:* q = 0,2 **copre
troppo** (soglia 0,85–0,97: fuori, nel verso innocuo); il q tarato copre troppo poco sull'altra metà; il valore
calibrato sta fra 0,05 e 0,1. (c) Tratti nascosti veri con profondità: DepthTrack, 2 tratti di 1–3 fotogrammi: stessa
identità 2 su 2 con la soglia scalata, 0 su 2 con i parametri del nucleo; Princeton: nessuno utilizzabile. **Non risolta.**

**(5) Elementi mobili e ostacoli** (simulato D435i nominale; «visto» = cella occupata entro 15 cm) — `misura_ostacoli.txt`

| Scena | Parametri del nucleo | Soglia 40 |
|---|---|---|
| Cassa alta 1 m a 1,7 m; persona accanto | 84 su 84 | 84 su 84 |
| Scatola di 15 cm a 2,0 m | 10 su 10 | **3 su 10** (20 semi: 2 su 20 a 2 m, 0 su 20 a 3 m) |
| Scatola di 15 cm a 0,8 m | 0 su 10; impronta «non osservato» 340 su 340, 0 «libero» | uguale |
| Ostacolo sospeso (quota 1,8–2,0 m) a 2,8 m | 10 su 10 | 10 su 10 |
| Ostacolo sospeso a 2,06 m | il sensore non lo vede; **sotto è «libero» nel 97,5 %** (i «7 su 10» sono fantasmi del pavimento) | 0 su 10; «libero» 97,6 % |
| Pannello fermo detto «si muove» | **79 passaggi su 90** (79–93 %) | 5 su 90 (2,4–12,4 %) |

Sul vero: non decidibile (nessuna verità); DepthTrack: 6 identità sul bersaglio in 21 s, 58 con i parametri del nucleo.

**(6) Costo** — un filo, AMD Ryzen AI 9 HX 370: **non è la scheda di bordo** — `misure_brevi.txt`, `vere/RIEPILOGO.txt`

| Dati | Media | 95° | Massimo |
|---|---|---|---|
| Simulato 424×240, 9152 cicli, parametri del nucleo | 6,35 ms | 18,6 | 105 (4 cicli oltre 66 ms) |
| lo stesso con soglia 40 | 0,95 | 1,28 | 7,7 |
| TUM 640×480; scale 1280×720 | 2,6–3,1; 9,0–10,9 | 3,8; 15,9 | 6,2; 18,5 |
| DepthTrack 640×360, portata 4 m, parametri del nucleo (254 tracce in 21 s) | **81** | **152** | **383** |
| lo stesso con soglia scalata (91) | 20–24 | 39–49 | 168 |

## 3. Critiche, con il caso minimo

1. **La persona si fonde col pannello** quando le sagome si toccano: 90 passaggi su 90 (D455 e Gemini compresi). Causa:
   celle ponte fatte di pixel misti; con i bordi spenti nel simulatore 10 su 10 → 1 su 10 (V22). Caso:
   `python diagnosi.py sim d455_nom__pannello_a12__s00 8 16` (k = 11: un gruppo solo, 100 celle, largo 1,42 m).
2. **Riaggancio su un fantasma dello spigolo a soggetto nascosto**: stesso caso, k = 23 (`misura_tagliata: true`, frazione
   visibile 0); poi la traccia della persona è «osservato» sul pannello. La regola C1 ammette i gruppi «tagliati» e il
   pannello stesso, che sta sempre «entro la fascia»: l'occlusore può prendersi l'identità. È la condizione
   d'invalidazione scritta in B5 («rilevamenti falsi al bordo del pannello»): qui si avvera.
3. **I fantasmi del pavimento rendono falsa «una sola traccia pendente»**: 7–66 tracce fantasma per passaggio.
4. **La soglia 40 è un baratto, non una soluzione**: perde la scatola di 15 cm e riapre K-014. Nessuna coppia provata
   dà insieme continuità, scatola e zero fantasmi (`taratura_tara.txt`). I 6 fallimenti di a05 non sono diagnosticati.
5. **La regione dichiarata non informa**: copre il 100 % anche chi si ferma, perché a 3 s ha un raggio di 3,5 m.
6. **La posa decide il «libero»**: 5 cm di tolleranza a 3 m sono 1° d'inclinazione. La stima del suolo dai primi 5
   fotogrammi sbaglia di 19 cm e 5° su TUM, dà un rollio di −31° su DepthTrack e fallisce su `realsense_stands_still`.
7. **La mia misura**: tolgo uno scarto sistematico stimato sugli stessi passaggi; l'identità «prima» e «dopo» sono
   scelte a maggioranza; le sequenze vere sono troncate.

## 4. Confronto con le cifre idealizzate del nucleo

| Idealizzato | Qui | |
|---|---|---|
| Identità al ritorno 100 % | 0 su 90; 41 su 45 con soglia 40; 0 su 6 al limite | **cambia** |
| Muro «mobile» 0,0–0,2 % | 88 %; 5,6 % con soglia 40 | **cambia** |
| Nessun «libero» falso; nascosto mai fuori dallo strato 1 (0 su 14 400) | 0 su 2,9 milioni; 0 fotogrammi «libero» su 3038 nascosti | **confermato**, a meno di una cella al bordo e dell'ostacolo non rilevato |
| Ombra ±20 cm, peggio a −20 | da +2 a +15 cm | confermato, più stretto |
| Cerchio al 95 %: copertura 0,89–0,93 | 1,00 (simulato); 0,99–1,00 (THÖR) | **cambia**: troppo largo |
| «Si muove» entro 1 s a 2 m: 100 % | 20 su 20 attraversando; da 4 m in avvicinamento 0–4 su 20 | confermato a 2 m |
| σ del centro 1,5 / 3,4 / 6,0 cm | 0,1–1,3 cm simulato; circa 6 cm vero (descrittivo) | **non decidibile** |
| 2,5 ms per ciclo a 848×480 | 1–6 ms a 424×240; 81 ms su una scena vera affollata | **cambia** |

## 5. Stati proposti

- K-014: **sostenuta dai dati simulati** con i parametri del nucleo; **controesempio** se un ostacolo basso non è rilevato;
  sul sensore vero **non risolta** (decide il pannello sul suolo segnato col nastro).
- Identità al ritorno, falsi sul fermo, R4 («0 osservato a soggetto nascosto»): **smentite** sulla catena così com'è;
  **sostenute** al nominale con soglia 40; al limite **smentite** (N = 6).
- q = 0,2: **sostenuto dai dati veri** come prudente; «regione calibrata»: **smentita**. K-007: **non risolta**.
- Costo «15 Hz»: sostenuto su scene pulite; **smentito** su una scena vera con molte tracce, su questa macchina.

## 6. Proposte

- **validazione-6.** Soglia di punti per «occupato» proporzionale ai pixel attesi per cella alla sua distanza, non fissa.
  *Meccanismo:* le celle ponte e i fantasmi hanno pochi punti rispetto a una superficie piena. *Previsione:* continuità
  ≥ 28 su 30 in a12 **e** scatola a 2 m vista in ≥ 9 su 10. *La smentisce:* una delle due sotto soglia.
- **validazione-7.** Il riaggancio rifiuta i gruppi «tagliati» e il gruppo dell'occlusore. *Previsione:* 0 riagganci a
  soggetto nascosto sui passaggi del D455 (oggi 3 su 3 in a12). *La smentisce:* uno solo, o la continuità che scende.
- **validazione-8.** q = 0,1 e regione ritagliata sul cuneo. *Previsione:* copertura 0,90–0,97 su una registrazione
  THÖR mai usata (exp2). *La smentisce:* un valore fuori. (0,945 su exp3 è visto a posteriori: non conta.)
- **validazione-9.** Prova d'ingresso del sensore della squadra (5 minuti): 30 s di pavimento vuoto, 0 tracce
  confermate; un pannello con una persona accanto, 0 gruppi fusi. *La smentisce:* una traccia o una fusione.

## 7. Che cosa propongo dopo, e che cosa non è provato

Decidere validazione-6 e -7 prima di scrivere il prototipo: senza, la continuità visiva non regge su una profondità
realistica. **Non provato:** tutto sul sensore della squadra; persone articolate; due persone; occlusore mobile; sensore
in moto; il livello limite oltre 16 sequenze; la previsione su pedoni veri *con* la catena (THÖR non ha profondità);
il predittore di f8 (si innesta in `comune.PredittoreCheRegistra`).
