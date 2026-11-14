# Soluzione integrata — ramo H-012, f3 (`sciame-scene-dinamiche`, responsabile)

**In testa.** Nessun cambio di stato: compongo ciò che la selezione ha adottato; non ho eseguito prove. Tutto ciò che segue è **simulazione o scheda, a sensore fermo**: niente è provato su hardware o su pedoni veri. **Scostamenti:** (1) quattro pagine, come chiede il coordinatore, non le due di `TASK.md`; (2) oltre agli ingressi di `TASK.md` ho letto selezione, firme, fonti e, con `grep`, `risultati_main1_parte3.txt`, `risultati_E_parte2.txt` e `scena_parte3.py`; (3) i conti **[resp.]** sono miei, a mano, non verificati; (4) quattro scelte di composizione sono mie e **non provate**: il tetto T_g sull'avviso legato alla traccia, lo strato 1 esteso alle celle non osservate contigue, la tolleranza con cui si legge «contiene alla riemersione», la geometria della demo in scala; (5) le ore sono stime mie. Previsioni per A, B, C: `PREVISIONI.md` (scritte prima; `decide: sì`).

## 1. L'architettura in una riga

Camera stereo attiva ferma → griglia polare a quattro stati ricalcolata a ogni fotogramma → gruppi di punti sopra il suolo → associazione → Kalman a velocità quasi costante → tre stati per traccia (**osservato / previsto / perso**) con due strati durante l'occlusione → tabella di regole → messaggi e schermo. Una rete gira a parte e mette solo un'etichetta. Ordine fissato da F-003: rilevamento → associazione → filtro → decisione.

## 2. I blocchi

**B1. Sensore e montaggio** (H-001 + H-002; correzione: portata e cono cieco dichiarati). Entra la scena, escono profondità e RGB a 30 fps con il contatore di fotogramma; l'elaborazione gira a 15 Hz (la frequenza di tutte le simulazioni). Camera stereo attiva con IMU, quella che la squadra possiede (D455 e D435i 87°×58°, Gemini 335 90°×65°). **Portata dichiarata 0,5–3 m** (al limite di scheda ≤ 9 cm fino a 3 m; a 4 m 8–16 cm: non risolta). Su treppiede a 1,2 m (altezza ipotizzata nel torneo, da misurare), orizzontale, inclinata di 15° in basso. Cono cieco dichiarato: un ostacolo a 1,8 m di quota si vede solo oltre 2,41 m. Costo: 3 ore (supporto, piano del suolo da N fotogrammi all'avvio). Dipende da: decisione 3 dell'utente. Invalidata se: sole pieno, sensore indossato, o campo diverso.

**B2. Percorso critico geometrico e griglia** (H-006 per il percorso, H-008 per gli stati, con le quattro correzioni del torneo; H-009 per la scadenza). Entra la profondità, esce una griglia polare egocentrica (1°, 0,1 m, fino a 3 m). A ogni fotogramma ogni cella è: **libero osservato** (suolo visto alla quota attesa E nessun ostacolo), **occupato osservato** (primo ritorno fra 0,07 e 2 m di quota), **in ombra** (oltre il primo ritorno), **non osservato** (fuori campo, oltre portata, buco, suolo mancante). Memoria: «libero» **mai** ricordato; «occupato ricordato» esce con la sua età e scade a «non osservato» (T = 2 s: valore ipotizzato dall'avversario, non tarato), subito se la cella era di una traccia mobile. Pavimento piano dichiarato. Nessun modello appreso. Calcolo: 2,0 ms a fotogramma per la griglia e 20 ms a 640×480 per il percorso minimo, entrambi in Python puro su scene sintetiche (non è il prototipo). Costo: 6 ore. Invalidata se: rampe (a 5° «occupato» falso dopo 0,80 m), 2° d'errore d'assetto (pavimento «occupato» oltre 2 m), vetro (la cella della lastra risulta «libero»: limite aperto in ogni griglia proposta).

**B3. Rilevamento e regola «mobile»** (H-004 per il rilevamento senza rete; H-010 corretta: R(z) per asse, etichetta su una finestra, velocità minima dichiarata). Entrano le celle occupate, escono gruppi connessi con centro (x, y) e larghezza. **Default:** un gruppo è «mobile» se lo spostamento su una finestra di 1 s supera 5·σ(z)·√2 lungo l'asse radiale o trasversale. Velocità minima vista in avvicinamento: 5·σ_r(z)·√2 al secondo, cioè 0,35 m/s con σ = 5 cm [resp.]. A sensore fermo è facoltativo lo sfondo a mediana di H-005, come controllo incrociato e come verità di riferimento (nastro a terra). Costo: 5 ore. Dipende da: B2; R(z) letto da una scheda. Invalidata se: prova B; sensore in moto senza compensazione (ogni muro diventa «mobile»: F-008).

**B4. Associazione e stimatore** (H-010 e H-012 per il filtro; H-013 per le regole, senza il suo q = 0,5). Kalman lineare [x, y, vx, vy] sul piano del suolo, **q = 0,2 m²/s³**, R(z) per asse. Porta di Mahalanobis al 99 % e assegnazione ungherese, **priorità alle tracce confermate**; una traccia nasce «tentativa» e si conferma con 3 rilevamenti su 5 (regola non attaccata). q si tara sulle innovazioni **alla ricomparsa**, non sul NIS a un passo dei tratti dritti (che sceglie 0,01 e copre 0,71–0,74). Niente stato d'accelerazione (F-004), niente massa (F-002). Costo: 5 ore; calcolo trascurabile (SORT, stessa famiglia: 260 Hz). Dipende da: B3. Invalidata se: due persone tornano insieme dietro il pannello (scambi 0,440: la geometria non dà l'identità, da cui «identità ambigua»); le 30 occlusioni registrate danno meno di 26 riemersioni nella regione (soglia che boccia una taratura buona una volta su cinque).

**B5. Ciclo di vita e i due strati** (H-012 con le riformulazioni i–v; `avversario-3`; H-014 per il rilascio; H-016 per l'evidenza negativa). A ogni ciclo senza misura si legge la griglia sulla posizione prevista: buco → «non osservato», segnale R6; fuori campo o portata → «perso», zona non osservata; ombra → occlusione, e partono due strati.
- **Strato 1, garanzia (R6, R8).** L'ombra in cui la traccia è entrata, con le celle non osservate contigue, dilatata di una **fascia di guardia di 0,40 m** (0,20 d'errore d'ombra + mezzo corpo di 40 cm), è «possibile presenza». Si rilascia solo in tre modi: riaggancio; celle viste libere per **≥ 3 fotogrammi consecutivi** fuori dalla fascia; tetto **T_g = 10 s** (valore di H-015, non attaccato), dopo il quale cade l'avviso legato alla traccia e le celle restano «non osservate». Un timer non produce mai un «libero».
- **Strato 2, informazione (R3, R4, R5).** Cerchio al 95 % del filtro, **ritagliato sulle celle non osservate**, mostrato come «previsto: probabile qui» **finché copre meno di metà dell'ombra** (con il pannello da 1 m: 31 % a 1 s, 62 % a 2 s). Poi lo stato è **«perso»**: resta lo strato 1 e parte il segnale R6. La copertura si dichiara **0,90–0,93**, non 95 %. Il raggio fisso r_max = 1,5 m è tolto: nella geometria della parte 3 del torneo (2 m d'ombra, transito di 1,70 s) teneva l'identità nel 30 % dei transiti.
- **Ritorno.** Un rilevamento al bordo dell'ombra entro v_max·τ + 3σ√2 dall'ultima misura (**v_max = 2,5 m/s**) si riaggancia se nell'ombra pende una sola traccia; se ne pendono due, esce «identità ambigua». Se lo stato era «perso», il riaggancio è dichiarato.

Costo: 8 ore. Dipende da: B2 (maschera d'ombra), B4. Invalidata se: prova A; un falso «libero» di 0,3 s (nessuna famiglia lo regge); chi torna indietro (coperto nel 56–66 % dal cerchio: lo tiene solo lo strato 1).

**B6. Ramo asincrono di riconoscimento** (H-006; H-011 per le due regole). Entra l'RGB a bassa frequenza, esce l'etichetta **persona / non persona** attaccata a una traccia già esistente, mostrata a schermo. RF-DETR-N (Apache 2.0) o YOLO26n (38,9 ms su CPU, AGPL-3.0). Non crea né chiude tracce, non tocca celle, non decide allarmi; una confidenza mostrata va calibrata a posteriori su una registrazione propria. Escluso lo «sguardo costoso» di H-020: con la classe fuori dal percorso critico manca la risorsa da spartire. Costo: 4 ore, calcolo fuori dal ciclo a 15 Hz. Dipende da: B4 (le tracce). Invalidata se: la giuria chiede classi d'ostacolo (muro, porta, gradino, palo non sono in COCO); se manca, la catena non cambia.

**B7. Logica di decisione** (H-009: tabella di regole; H-010 per la gravità). Entrano griglia e tracce, esce per settore il messaggio più grave: non osservato o buco > mobile in avvicinamento > occupato > previsto > perso con possibile presenza. Gravità = taglia misurata × velocità di avvicinamento. Il sistema dice «nessun ostacolo osservato fino a d metri», mai «via libera». Costo: 2 ore. Dipende da: B2, B5. Invalidata se: l'utente vuole una decisione appresa (nessuna prova la sostiene).

**B8. Feedback e affidabilità persa** (H-004 per i messaggi; H-017 per la freschezza). **Default:** messaggi vocali «direzione, distanza, stato» e schermo a tre colori con il contatore della latenza. Il contatore di fotogramma del sensore viaggia fino all'uscita e non si riscrive mai: senza un fotogramma nuovo, o con tre fotogrammi identici, esce «affidabilità persa» (0,13 s e 0,07 s nella simulazione logica; con la sola marca temporale il segnale non parte mai: 25 s osservati). Costo: 5 ore. Dipende da: B7. Invalidata se: la camera scelta ripete i fotogrammi senza cambiare contatore (non verificato).

**B9. Demo e accettazione** (H-018 corretta; H-019 facoltativa). Cinque atti in circa tre minuti: campo mezzo coperto (R8); ostacolo fermo (R2, R5); attraversamento con latenza a schermo (R1, R5, R7); passaggio dietro il pannello (R3, R4); sosta dietro il pannello o mano sul sensore (R6, R8). Si fissa **la larghezza dell'ombra alla distanza dell'attore**, non quella del pannello: 1 m d'ombra. In scala sulla portata dichiarata: pannello da 0,5 m a 1,5 m, attore a 3 m [resp.: similitudine con la scena simulata, pannello a 2 m e pedone a 4 m; non simulata]. Facoltativa nell'atto 4 la scommessa sigillata di H-019, con tre esiti in tabellone (nella finestra, «ancora dietro», persa) e le soste dentro la taratura. Un secondo passaggio con 2 m d'ombra mostra senza trucchi «perso → riagganciata». Registrazione e riproduzione delle sequenze, 30 occlusioni e 20 soste contate: 10 ore. Invalidata se: l'attore cammina sotto la velocità minima di B3, o il rumore a 3 m supera i 5 cm delle simulazioni. Totale stimato: **circa 48 ore-persona**, entro l'ipotesi di fattibilità del contratto, che resta non verificata.

## 3. Invarianti (da scrivere come asserzioni nel codice)

1. «Libero» esiste solo dove il suolo è visto nel fotogramma corrente; non si ricorda e non si deduce.
2. Buco, fuori campo, oltre portata, ombra: mai «libero».
3. Nessuna uscita «osservato» senza una misura in porta nel ciclo corrente.
4. «Previsto» e «possibile presenza» non si disegnano su celle viste libere oltre la fascia di guardia.
5. Nessun timer e nessun modello appreso produce un «libero», chiude una traccia come «assente» o decide un allarme.
6. Evidenza negativa solo dove la profondità è valida e vede lo sfondo.
7. Oltre la fine del «previsto» la traccia non scade: resta lo strato 1.
8. Ogni uscita porta il contatore di fotogramma del sensore; senza fotogramma fresco esce solo «affidabilità persa».
9. Una grandezza non osservabile (massa, accelerazione) non compare in uscita.

## 4. Scelte in gara: default, alternativa, prova che decide

| Scelta | Default e motivo | Alternativa | Decide |
|---|---|---|---|
| Regola «mobile» (K-007) | spostamento su 1 s: 98,7 % a 0,5 m/s e 0 falsi su 4000, ma **esplorativa**, solo rumore isotropo | χ² con R(z): 0,0 % di falsi, ma 75,4 % entro 1 s a 0,5 m/s e 11,0 % in avvicinamento a 4 m | prova B; poi un muro e una persona lenta a 2 e 4 m |
| Feedback (K-010) | messaggi: la demo ha una giuria che guarda e ascolta, e il battito non ha nessuna prova | battito sommesso sul libero osservato e fresco | tre persone bendate, ≥ 54 stati su 60. Fonti: in due studi l'aptico costa più dell'audio; non decide |
| Montaggio | orizzontale: 87° servono al transito dietro l'ombra, e le simulazioni hanno ±43,5° | verticale (`avversario-1`): suolo da 0,74 m, ostacolo alto da 1,11 m, ma 58° in orizzontale | asta a 1,8 m di quota a 1,2 m di distanza; l'atto 3 dentro 58° |
| Sosta (K-005) | scadenza: la sosta diventa «perso» con possibile presenza (R6) | particelle con modo «sosta» (H-015, H-016): identità 100 % con 1 m, 76 % con 2 m, 68 % con ombra a −20 cm | 20 soste registrate dietro un pannello vero |
| Fine del «previsto» (K-004) | meno di metà dell'ombra coperta (soglia dell'avversario, non provata) | tempo nominale di transito (W + 0,45)/v | prova A, misura A4 |

## 5. Decisioni dell'utente: default prudente e che cosa cambia

| Decisione | Default (ha prove) | Nell'altro caso |
|---|---|---|
| 1. Applicazione e posa (K-008) | sensore **fermo** su treppiede; racconto assistivo con l'utente fermo. Il «monitoraggio di attività» industriale non è coperto senza lavoro in più | indossato: giroscopio obbligatorio (1,49 m d'errore senza, 0,25 con: F-008), odometria da comprare, memoria compensata; **nessuna soglia di questo documento è provata** |
| 2. Sosta (K-005) | perdita di affidabilità dichiarata, senza particelle | continuità: particelle, più lavoro, 76 % con l'ombra larga |
| 3. Sensore e 360° (K-009, H-003) | una camera frontale; fuori campo «non osservato». Le regole non nominano i 360° (F-005) | 360°: un LiDAR a scansione su palo (al petto: smentito, 205°–233°); tre ToF multizona danno 180° (scheda ST). Senza camera di profondità: demo su registrazioni RGB-D, non verificato |

## 6. Copertura R1–R8

Stato: **S** = sostenuto dai dati in simulazione; **C** = per costruzione, da controllare come invariante; **NV** = non verificato fino all'hardware. Nessuna riga è dimostrata o verificata sul vero.

| R | Componente | Misura di accettazione e soglia | Stato |
|---|---|---|---|
| R1 mobili | B3 | ≥ 9 su 10 entro 1 s, a 0,5 m/s, alla distanza dichiarata (2 m in avvicinamento); falsi sul muro ≤ 10 % | S, esplorativo; prova B |
| R2 ostacoli | B1, B2 | 5 su 5 entro 15 cm fra 0,5 e 3 m; gradino di 15 cm a 2 m | S da schede (5,4σ); NV su vetro, nero, cono cieco |
| R3 continuità | B5 | 26 riemersioni su 30 nella regione, a ombra fissata; stessa identità con una sola traccia pendente | S (0,90–0,93); l'insieme: prova A |
| R4 osservato / incerto | B5, invarianti 3 e 4 | 0 fotogrammi «osservato» a soggetto nascosto; tre stati distinti in voce e a schermo | C |
| R5 feedback | B7, B8 | ≤ 300 ms dal primo fotogramma con l'ostacolo al comando audio (lettura mia degli estremi) | NV |
| R6 affidabilità persa | B5, B8 | segnale entro 1 s da: fine del «previsto», buco, sensore coperto o fermo | S nella logica (0,13 s); NV sulla camera |
| R7 latenza | B2, B8 | p95 ≤ 150 ms dalla marca di cattura al comando audio; ≥ 15 fotogrammi/s senza GPU | **non risolto** dal fotone al suono: manca la fonte per sensore e audio |
| R8 sicurezza | B2, strato 1, invarianti 1, 2, 5 | 0 «libero» su celle non osservate; strato 1 contiene il nascosto nel ≥ 99 % | C sul non osservato; **vetro: smentito** in ogni griglia, limite dichiarato |

**Lettura di «riconoscere», dichiarata.** Le regole lo nominano una volta, in una frase non prescrittiva che lo presuppone. Lo copre l'etichetta persona / non persona di B6, fuori dal percorso critico. Che le regole non chiedano di riconoscere è una lettura, non un fatto (F-005 ristretto).

## 7. Idea di partenza della squadra → esito

| Idea | Esito | Perché |
|---|---|---|
| 3 ToF a 360° | **esclusa** | F-001: tre multizona coprono 135°–180° («three sensors can cover 180° x 60°», scheda ST); a 5 klx il VL53L7CX tiene 0,5–0,65 m. Sostituita da H-001 |
| Mappa del terreno e gradi di libertà | **corretta** | griglia locale a quattro stati su pavimento piano dichiarato (H-008); non è una mappa. Dell'ostacolo si stimano posizione e velocità sul piano; dell'utente niente, perché il sensore è fermo |
| Classificazione | **corretta** | solo persona / non persona, asincrona, mai in un allarme (H-006, H-011): 0 su 7 categorie d'ostacolo in COCO |
| Massa | **esclusa** | F-002: non osservabile. Escluso anche il «peso tipico di classe»: nessuna decisione lo legge |
| Velocità | **confermata** | stato del filtro (H-010); in simulazione 0,2 m/s; la velocità minima vista si dichiara per distanza e direzione |
| Accelerazione | **esclusa** | F-004: σ ≈ 66 m/s² a 30 Hz, sotto il rumore |
| Previsione fuori vista | **confermata, corretta** | un'area, non un punto; orizzonte 1–1,6 s (F-006); poi «perso» con possibile presenza (H-012, H-009) |
| Kalman → vision transformer → decision model | **corretta** | F-003: ordine invertito. Rilevamento → associazione → Kalman → tabella di regole; la rete sta a lato; la decisione non è appresa |

## 8. Dove sta lo stato dell'arte (solo fonti verificate in `f3/fonti/FONTI_VERIFICATE.md`)

- **Entra, nel ramo asincrono:** un rilevatore in tempo reale. RF-DETR-N: 2,3 ms su T4, AP 48,4, Apache 2.0 (le varianti Atto, Femto, Pico, XL, 2XL sono sotto PML 1.0) — https://github.com/roboflow/rf-detr. YOLO26n: 38,9 ± 0,7 ms su CPU, AGPL-3.0 — https://docs.ultralytics.com/models/yolo26/.
- **Entra, come schema:** associazione alla SORT / OC-SORT (l'articolo di OC-SORT descrive il rumore che il Kalman accumula in occlusione) — https://arxiv.org/abs/2203.14360. Sui pedoni la velocità costante regge contro due predittori appresi (RED, SR-LSTM): 0,39 / 0,83 m contro 0,44 / 0,91 a 4,8 s; il generativo S-GAN sta a 0,32 / 0,60, che per l'autore della scheda è il migliore di 20 campioni e non è confrontabile (non riletto) — https://arxiv.org/abs/1903.07933.
- **Fuori, modelli di fondazione e a vocabolario aperto:** SAM 3 dà 30 ms a immagine su una H200, SAM 3.1 passa da 16 a 32 fps su una H100: non è il calcolo di un hackathon, e nessuno dei due può decidere un allarme (invariante 5).
- **Fuori, modelli video con memoria:** SAMURAI non lavora su video dal vivo; TAPNext dà 187 fps su H100; EdgeTAM (16 fps su iPhone 15 Pro Max, Apache 2.0) è il solo candidato leggero, ma l'identità attraverso l'ombra qui la dà lo strato 1.
- **Fuori, profondità monoculare:** Depth Anything 3 arriva a 43 fps su Jetson Orin NX secondo una fonte di comunità; la profondità qui è misurata dal sensore. Sarebbe il ripiego senza camera di profondità: non verificato.

## 9. Non verificato fino all'hardware

Vetro, tessuti scuri e sole pieno; pedoni veri (30 occlusioni, 20 soste); maschera d'ombra dalla profondità vera e corpo in parte coperto; sensore indossato (F-008); latenza dal fotone al suono; fotogrammi ripetuti dalla camera scelta; feedback con persone bendate; prezzi e reperibilità; rumore a 3 m contro i 5 cm isotropi delle simulazioni; le mie quattro scelte di composizione.

## 10. Dopo

Prove A, B, C in f4 con autore diverso dall'avversario. Alla squadra, appena c'è la camera: cinque minuti davanti a una porta a vetri, cinque al sole, poi le 30 occlusioni.
