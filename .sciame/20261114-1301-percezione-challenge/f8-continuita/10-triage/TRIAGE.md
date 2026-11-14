# Triage dell'estensione f8 (continuità visiva) — `sciame-arbitro`, fase f2

**In testa.** Lavoro dalle 15:47 alle 16:01 del 14 novembre 2026 (`date -Is`). Lunghezza al limite delle quattro pagine. **Consegne:** nove su nove. **Canarini:** reggono (prima riga giusta ovunque; 0 occorrenze del canarino dell'altra corsia nei file delle nove cartelle: `riconta_arbitro.txt`, §1). **Cifre:** 51 su 51 tornano dai file dei risultati (§2): la mia P-arb-3 («almeno una non torna») è **smentita**; P-arb-1, 2 (9 ruoli su 9), 4, 5, 12 reggono; P-arb-6…11 le decide il banco (`PREVISIONI.md`). **Cambio di stato:** «la continuità la porta l'avviso sull'ombra» (mio verdetto, §5.5) regge per l'avviso e l'identità, è **smentita** per il movimento mostrato (F-201). **Scostamenti:** `PREVISIONI.md` con P-arb-1…5 era già in cartella alle 15:42 (un avvio precedente di questo ruolo): adottato; P-arb-6…12 sono scritte dopo la lettura, cieche solo rispetto al banco. Le **ore** sono stime mie **[arb.], non verificate**: nessuna corsia aveva la scadenza. Nessun simulatore altrui rieseguito. Il documento è passato alla v0.6 alle 15:48: la riga «con 24 ore si taglia l'area prevista», citata da tre ruoli, non c'è più (`grep` «si tagli»: 0); la riga 112 marca ancora convergente «circa mezzo secondo». Tutto è **simulazione o conto, a sensore fermo, soggetto puntiforme**.

## 1. Q3 — l'imperativo è rispettato? Parte per parte

| Parte | Stato | Prova (origine) |
|---|---|---|
| B5, strato 2: «metà dell'ombra» e «perso» assorbente | **non rispettato** (9 su 9) | stima nel 35–50 % dei cicli senza osservazione in demo (`MISURE_V2.md`, P4), 8–10 % in sosta; riscritture: 14–69 % (tracciamento, scala demo), 60,8 e 39,8 % (rovesciatore), 42–91 % (inferenza) |
| B4, centro della previsione | **in parte** | batte «fermo» sulla miscela (0,50 contro 2,48 m a 2 s), perde per chi torna (1,78 contro 1,29 m): statistico, kalman |
| B4, precisione dichiarata | **non rispettato** per comportamento e al 50 % («in parte» per tre ruoli: K-212) | media al 90 %: 0,88–0,96; chi torna 0,29–0,77 a 2 s secondo il generatore; il «50 %» contiene 0,63–0,85 |
| Incertezza controllata | **in parte** | limitata e mai su «libero», ma oltre soglia sparisce (kalman, inferenza, ricercatore) |
| Strato 1; invarianti 1–5 e 7 | **rispettato** | cinque ruoli; nessuna proposta lo tocca |
| B3 (C6); B1, B7, B8; invarianti 6, 8, 9 | **in parte** | C6 allunga il buio a 1,07–1,27 s; rumore «da misurare»; solo colore, nessun livello a schermo; manca un decimo invariante (requisiti, visualizzatore) |
| Accettazione (R3, H9) | **non rispettato** | misura l'identità; H9 «regge» con probabilità 1,000 anche se chi torna non è mai coperto (`out_h9.txt`) |
| Verdetto; profili | **non rispettato** | §5.5 e §6.3; `SPECIALIZZAZIONE.md`, riga 83: «si riduce a un istante» (6 ruoli) |
| Sensore in moto | **in parte** (4 ruoli) | con la covarianza di posa 0,88–0,91, senza 0,76–0,82 (kalman); Q5 parte da una media |
| Demo | **non rispettato** (requisiti) o in parte (2 ruoli) | atto 4 «per un attimo»; il buio di 1,1 s non mostra 2–5 s |
| Documento v0.6 | **in parte** | lo dichiara (riga 94); nessuna cifra di precisione |

## 2. Fatti stabiliti in cieco da più ruoli

| F# | Enunciato | Stato | Chi (corsia) |
|---|---|---|---|
| F-201 | Il nucleo non emette una stima a ogni ciclo: in sosta 40,0 / 41,3 / 39,4 / 45 % in quattro codici | sostenuto dai dati | nell'ordine: rovesciatore (B), tracciamento (A), creativo (B), inferenza (A) |
| F-202 | Il cerchio del filtro (q = 0,2) non è tarato per comportamento né al 50 % | sostenuto | sei ruoli, A e B |
| F-203 | Ritagliare non è condizionare: 0,52–0,83 a soggetto nascosto; q ≥ 1 − (1 − p)/G(S) | dimostrato (gaussiana troncata); sostenuto | inferenza, kalman, requisiti (A) |
| F-204 | Il punto a velocità costante finisce su suolo visto libero: 86–88 % a 2 s; 90–94 % a 2–3 s | sostenuto | rovesciatore (B); tracciamento, visualizzatore (A) |
| F-205 | Serve un modo «resta indietro»: senza, chi torna 0,39; una scala unica lascia il 50 % fra 17 e 100 % | sostenuto | tracciamento, kalman (A); rovesciatore, creativo (B) |
| F-206 | Nessuna regione «probabile» copre chi svolta o esce dal lato lontano (14–45 % a 2 s): solo il limite esterno | sostenuto | inferenza, tracciamento (A); creativo (B) |
| F-207 | La taratura conforme per fascia è giusta in media (0,88–0,91), non per comportamento (torna 0,46–0,75), né con altra miscela (0,64–0,80) o geometria (0,63–0,71) | sostenuto | quattro ruoli (A); rovesciatore (B) |
| F-208 | Tarata sul comportamento peggiore ogni classe tarata sta a 0,87–1,00, ma da 1,5–2 s la regione è l'86–90 % dell'ombra | sostenuto | kalman, statistico, ricercatore (A); rovesciatore (B) |
| F-209 | Il controllo 1 è mal posto: la prima misura cade su spazio visto, che il controllo 4 toglie dalla regione | dimostrato per definizione | inferenza (A); rovesciatore (B) |
| F-210 | Trenta prove non separano 0,90 da 0,80 (servono 60–89); con 30 gli errori sono 17,6 e 25,5 % [arb.] | calcolo esatto | statistico, visualizzatore (A); creativo (B) |
| F-211 | Durante il buio, con una camera, la verità non c'è: serve l'occlusione virtuale | proposta in cieco; **non verificata** | requisiti, statistico (A); creativo (B) |
| F-212 | Il salto alla ricomparsa (0,18–1,7 m) non si elimina scegliendo il punto: va mostrato | sostenuto | tre ruoli (A); creativo (B) |

## 3. Q4 — le proposte, per posto

Fascia: **14** = indispensabile nelle 14 ore; **4** = raffinamento; **dopo**. Ore [arb.], non verificate.

| C# | Enunciato (origine) | Classe | Già provato; che cosa condivide con l'idea | Ore · fascia |
|---|---|---|---|---|
| C-001 | Predittore: particelle con modo «sosta», evidenza negativa oltre la fascia (tracciamento-1, inferenza-1) | TESTARE | 3 geometrie × 7 comportamenti × 400: ≥ 0,865 sul percorso; codice e parte dei generatori dell'autore | 5–8 · 14 se vince |
| C-002 | Predittore: miscela di gaussiane non collassata, troncata e rinormalizzata (kalman-1) | TESTARE | 0,94–0,97 su G0, 0,785 su G1 a 5 s; striscia schematica, pesi dell'autore | 5–7 · 4 |
| C-003 = **C-EST** | Predittore: due ipotesi, pesi 0,8 / 0,2 aggiornati con la massa in ombra, ritaglio, «previsto» finché σ_eff ≤ 0,8 m (S3, S4) | TESTARE com'è scritta | **nessuna prova**. Vicine: più modelli con soli pesi cade (sosta 0,41 a 5 s); gaussiana troncata sola: regione vuota in 14–110 casi | 3–5 · secondo il banco |
| C-004 | Predittore: «fronte + scia», 400 percorsi, unione degli scenari (creativo-2) | TESTARE | 99–100 % (1 m), ≥ 96 % (2 m), ≥ 98 % con ombra a −20 cm, 96–100 % su un terzo generatore; l'autore conosceva il generatore | 3–5 · 14 se vince |
| C-005 | Ripiego: centro a velocità costante, raggio da tabella sul comportamento peggiore, ritagliato (ricercatore-1; regione A del rovesciatore) | TESTARE | 87–100 % per cella fino a 3 s, due geometrie; stesso generatore | 1–2 · **14, per primo** |
| — | Soli pesi (sosta 0,41 a 5 s); particelle con «svolta» (0,09; 0,63); ellisse C1 (0,015–0,13); raggio in metri (0–26 %); percorsi v1 (3–9 %); istogramma sotto 1,5 s (0,56–0,62); filtro lasciato correre (F-202) | SMENTITA | ciascuna dal suo autore, con la misura fra parentesi | — |
| C-006 | Tre regioni annidate R50 ⊂ R90 ⊂ R100 = strato 1 intatto (rovesciatore-1, requisiti-2, tracciamento-1) | TESTARE | per costruzione; nessuna prova d'insieme | 1 · **14** |
| C-007 | Massima densità sulla distribuzione rinormalizzata e lisciata (inferenza-1) | TESTARE | 0,895–0,93 contro un oracolo dello stesso codice | con C-001 |
| C-008 | Punto: media condizionata a «ancora nascosto» (inferenza, visualizzatore) | TESTARE | passo massimo 0,11 m, 0 cicli su libero; modello dell'autore | 0,5 · 14 |
| C-009 | Punto ibrido: filtro, poi media (tracciamento) | TESTARE | 0 passi oltre v_max·dt; su celle libere 13,7–25,6 % a 1 s (`fin_V3.txt`, senza fascia) | 1 · 4 |
| C-010 | Taratura: quantile conforme per fascia, massimo sui comportamenti (kalman-2, statistico-1, ricercatore-1) | TESTARE | F-208; mai con l'ombra | 2 più le camminate · 4 |
| C-011 | Taratura per installazione; a schermo la copertura misurata (tracciamento-2, inferenza-1) | TESTARE | 0,88–0,90 su una geometria; trasferimento smentito | 1 · 4 |
| C-012 | La ricomparsa etichetta il comportamento; un contatore che può solo allargare (rovesciatore-2) | TESTARE | 4 errori su 1477; scena facile | 2 · 4 |
| C-013 | «Perso» non assorbente: diventa «previsto ampio»; chiusure solo motivate (otto ruoli) | TESTARE | per costruzione; soglia non misurata (K-202) | 1 · **14** |
| C-014 | Decimo invariante; 6 e 9 riscritti (requisiti-2) | RIFORMULARE dopo K-201, K-203 | lettura | 0,5 · 14 |
| C-015 | Ramo «sensore cieco» per il riaggancio (inferenza-2) | RIFORMULARE: nel nucleo il riaggancio è geometrico (B5, «Ritorno») | 10 su 10 contro 0 su 10 | dopo |
| C-016 | Schermo: segno di taglia fissa, anello vuoto, tratteggio, età, livello in parole, scarto (visualizzatore-1, creativo-3, ricercatore-2, S5) | TESTARE | 18 casi senza rumore; nessuna persona | 2–3 · **14** |
| C-017 | S2, compensazione della latenza | TESTARE | nessuna; 155 ms a 1,2 m/s = 0,19 m [arb.] | 1 · 4 |
| C-018 | Tabellone con intervallo e larghezza (visualizzatore-2, creativo-1) | TESTARE | F-210 | 1–2 · 4 |
| C-019 | Occlusione virtuale (requisiti-1, creativo-1, statistico) | TESTARE | **non eseguita**; non rende il corpo tagliato | 3–4 · **14** |
| C-020 | Scheda stratificata al posto di H9 (statistico-2, kalman-2, tracciamento-2) | TESTARE | smentisce nel 99,9 % dove H9 mai | 1 · 14 |
| C-021 | Demo con ombra larga o sosta; battito sonoro; ventaglio | APERTA (utente) | — | dopo |

## 4. Contraddizioni

| K# | I due enunciati | Domanda binaria · prova |
|---|---|---|
| K-201 | «Perso» sparisce, la regione resta con altro segno (nove ruoli) ↔ C-EST: oltre 0,8 m l'inviluppo scompare, resta la campitura | In soste di 2–4 s e lunghe C-EST emette una regione a livello dichiarato a ogni ciclo? Banco, C1a |
| K-202 | Soglia: metà del cuneo (cinque ruoli; in demo scatta a 1,0–1,47 s) ↔ 80 % dell'ombra (due ruoli: 0 % nel transito a 1,2 m/s, 46 % a 0,8) ↔ metri (tracciamento, C-EST) | In demo, su «prosegue», «metà» scatta prima della ricomparsa in più di metà dei passaggi? Banco, tre soglie sulla stessa uscita |
| K-203 | Il punto non sparisce mai (creativo-3, controllo 1) ↔ si spegne oltre un orizzonte (a 4–5 s 1,39–2,01 m contro 1,10–1,22 di «fermo») ↔ nessun punto (C-EST) | Esiste un punto non peggiore di «fermo» a ogni τ ≤ 5 s? Banco, C2 |
| K-204 | Media condizionata (salto 0,87 m, mai su libero) ↔ ibrido (0,19–0,25 m; su libero 13,7–25,6 %) | L'ibrido tocca celle libere oltre la fascia? Banco, C4 |
| K-205 | Particelle (la miscela «si gonfia»: 7,27 contro 4,07 m² a 3 s) ↔ deterministico (miscela nel 39–51 % della striscia; fronte + scia ≤ 39 %) | Stessa scena: un deterministico tiene ≥ 0,85 sul percorso con area ≤ 1,2 volte le particelle? Banco, C3 |
| K-206 | Più modelli con pesi: no (tracciamento) ↔ sì se troncati (kalman) ↔ C-EST | C-EST tiene ≥ 0,85 su «sosta» a 3 s? Banco |
| K-207 | Scala unica dalle ricomparse (k90 3,58; con 90 % di «prosegue» 0,98) ↔ conforme per fascia ↔ massimo sui comportamenti; σ(t) si trasferisce (93,6–100 %), i livelli no | Una tabella tarata in T tiene ≥ 0,85 per cella sul percorso in L fino a 3 s? Banco |
| K-208 | Il 50 % si mostra (sei ruoli) ↔ «sulle due ipotesi o niente» (ricercatore); misurato 0,56–0,62, 31–42 % a 5 s | Una candidata tiene il «50» fra 0,40 e 0,60 fino a 3 s? Se no: un livello, detto «almeno» |
| K-209 | Controllo 3 come pavimento (statistico) ↔ banda (requisiti, tracciamento) | Scelta di criterio, al coordinatore |
| K-210 | S2 porta sempre lo stato all'uscita ↔ il segno pieno solo dove c'è una misura (invariante 3) | Il segno compensato sbaglia meno anche nei 3 cicli dopo una sosta improvvisa? Braccio S2 |
| K-211 | «Previsto» del nucleo in demo: 0,40–0,53 s (validazione) ↔ 0,67–0,87 ↔ 0,66–1,14 s (emulazioni) | L0 del banco, con C6, dà 0,40–0,53 s? |
| K-212 | «In parte» ↔ «non rispettato» | **Apparente**: stessi numeri; il «51 % su libero» del creativo è il cerchio non ritagliato |

## 5. L'ordine delle candidate

**Compatibili con qualunque predittore:** C-006, C-013, C-016, C-019, C-020; poi C-010 o C-011, C-012, C-018. **In gara per lo stesso posto:** i predittori C-001…C-005; i punti C-008 e C-009; le soglie di K-202.

1. **C-004, fronte + scia.** Unica provata con ombra stretta e terzo generatore; costo più basso fra le regioni vere (0,48 ms, Python); controesempio probabile su corpo largo e livello 50 %.
2. **C-001, particelle con sosta.** La più provata; più codice (ricampionamento, lisciatura, 8 particelle per cella); controesempio certo fuori percorso, probabile con ombra stretta (torneo: 23–55 % di regioni morte).
3. **C-EST.** In gara per mandato dell'utente; poco codice; controesempio probabile (P-arb-6, 7, 8). Se cade, la sua riformulazione è C-002.
- **Radicale:** nessun predittore probabilistico; solo raggiungibile ∩ non visto libero (0 cicli fuori su 115 437), con età e ultimo punto. Nel banco deve reggere al 100 %.
- **Regola della scadenza:** una candidata sostituisce C-005 solo se, a pari copertura sul percorso, la sua R90 è almeno un terzo più stretta.

**Bilancio [arb.].** 42, 56, 70 ore-persona in 14 ore con 3, 4, 5 persone; il nucleo ne chiedeva 54. Il minimo per la continuità (C-005, 006, 013, 016, 019, 020) vale 9–12 ore, una persona. Con 3 persone ci si ferma lì; con 4 entra il predittore vincente; con 5 anche la taratura.

## 6. Protocollo del banco indipendente (`11-misure`)

**Ordine.** Generatore e semi scritti e congelati **prima** di aprire il codice dei predittori; niente copie di `truth()`, `g1`, `traiettoria()`, né dei tassi 0,25 e 0,4 al secondo. Ogni lancio ≤ 120 s.

**Scena.** Sensore fermo, campo 87°, 15 Hz, celle da 0,10 m (non la griglia polare: dichiararlo), pannello fermo. **D** (demo): pannello 1 m a 1,9 m, soggetto a 2,3 m, portata 3 m. **T**: 1 m a 2 m, soggetto a 4 m, portata 6 m. **L**: 2 m, soggetto a 4 m. Fascia 0,20 m. **Bracci:** ombra a −20 cm (senza fascia deve fallire, o il banco è cieco); rilevamento 0,7; corpo largo 0,45 m.

**Soggetto.** In vista ≥ 2 s; 0,3–1,8 m/s; rotta ± 15°. Manovra a un istante uniforme nel tratto nascosto: (1) prosegue; (2) rallenta al 30–60 %; (3) sosta 2–4 s, anche improvvisa (0,2 s); (4) torna dopo 0,3–1 s; (5) svolta 45–90°; (6) esce dal lato lontano; (7) sosta lunga ≥ 6 s. **Quote:** pari per comportamento; miscele per ripesatura: «squadra» 60/10/10/10/5/5, «giurato» 30/10/20/20/10/10.

**Misura.** Rumore 5 cm per asse (braccio 4 / 9 / 16 cm a 2 / 3 / 4 m); rilevamento 0,9; nessun falso allarme; C6 emulata (nessuna misura entro 0,22 m dal bordo dell'ombra).

**Predittori.** L0 nucleo (dal testo di B5); L1 fermo; L2 filtro lasciato correre, anche ritagliato; L3 raggiungibile ∩ non visto; C-005; C-004; C-001 (2000 particelle) con C-008 e C-009; C-EST; C-002 se resta tempo. Ognuno emette punto, R50, R90, R100. Deve fallire: q = 0,01.

**C-EST, due letture.** Smorzamento 0,90 a ciclo (A) o 0,95 (B); Q = q del nucleo; pesi moltiplicati a ogni ciclo per la massa in ombra e rinormalizzati (A), oppure 0,8 e 0,2 per la massa corrente (B); σ_eff = radice della media delle due varianze della miscela ritagliata; ellisse al 95 % = quei momenti per 5,99. I cicli «perso» contano senza regione. **Attacco 1:** D e T, 1,2 m/s, sosta improvvisa a metà pannello per 6 s, 200 semi: rigetto con un ciclo di «previsto» su celle libere oltre la fascia (senza fascia: riportato), o con il peso del transito dominante oltre 0,5 s dopo l'uscita attesa; più la quota dei cicli con il vero nella regione, 0,5–3 s. **Attacco 2**, su tutte: entra uno ed escono due, o uno a velocità tripla, 200 semi: 0 riagganci con identità fuori porta, 0 cicli con R100 tolta a soggetto nascosto. **Attacco 5:** 400 passaggi, su «prosegue» e sulla «squadra»: errore alla ricomparsa nell'ellisse al 95 % in ≥ 90 %. I 30 reali: **non verificato**.

**Numerosità.** Unità: il passaggio; τ = 0,5, 1, 2, 3, 5 s. Taratura: semi 1000–1999, 200 per comportamento, solo D e T. Prova: semi 9000–9999, 400 per comportamento e geometria, toccati una volta; L mai tarata. Celle con n < 30: vuote. Con n = 400 e soglia 0,85 gli errori sono 0,06 e 0,6 % (`riconta_arbitro.txt`, §3); fra 30 e 199 decide Wilson (smentita se il limite superiore < 0,90; regge se l'inferiore ≥ 0,80).

**Soglie, fissate ora.**
- **C1.** (a) Passaggi con un ciclo senza regione dichiarata: **0 su 400**; durata dei vuoti; a parte i cicli senza punto. (b) Passi del punto oltre 0,167 m: **0**; all'indietro oltre 5 cm in < 5 % dei «prosegue». (c) Prima misura nella R90 precedente dilatata di 0,40 m: **≥ 0,90** (anche a 0,30 m); salto mediano e 90º percentile.
- **C2.** Sulla «squadra»: errore mediano **≤ 0,5 m a 1 s, ≤ 1,0 m a 2 s**, non peggiore di L1 e L2 fino a 2 s; nessuna cella oltre 1,5 volte la migliore base. Orizzonte del punto: il primo τ in cui perde con L1.
- **C3.** R90 **≥ 0,85 in ogni cella sul percorso** (1, 2, 3, 4, 7); sulle miscele 0,85–0,97; R50 sulla «squadra» 0,40–0,60. Svolta e lato lontano: riportati; lì R100 **100 %**. Area di R90 in T e L **≤ 0,60 dell'ombra** fino a 3 s. Punteggio comune: −ln(massa dell'anello che contiene il vero / area), masse 0,5, 0,4, 0,1; fuori da R100: 9,21.
- **C4.** Celle di R90, o il punto, su visto libero oltre la fascia: **0 cicli**; R90 ⊆ R100; oltre soglia la regione resta nel 100 %; il ritaglio toglie il vero: 0 passaggi (> 0 nel braccio a −20 cm); quota dei cicli «ampio» con le tre soglie.
- **C6.** Tempo per ciclo e traccia, con 1 e 10 tracce: 95º percentile **≤ 6,7 ms**; oltre 20 ms smentita; righe di codice.

**Falsificatori per l'avversario.** (1) Ombra a −20 e −30 cm con corpo di 0,45–0,60 m. (2) Rilevamento 0,7 e 7–10 cicli mancati dopo la riemersione. (3) Taratura sulla «squadra», prova sul «giurato». (4) Chi inverte tardi, chi è già fermo all'ingresso, chi accelera in ombra. (5) Due tracce pendenti nella stessa ombra. (6) Svolta verso il sensore: R100 non deve mancare. (7) 0,3 e 2,5 m/s. (8) La soglia «metà» in demo. (9) Copertura contata per cicli invece che per passaggi.

## 7. Al coordinatore e all'utente

**Coordinatore.** Correggere il controllo 1 (F-209) e sciogliere K-209 prima del torneo; togliere «convergente» alla riga 112 del documento.

**Utente.** (a) «Visiva»: solo schermo o anche suono? (b) Livelli e soglia di «previsto ampio» (K-202). (c) Il punto può spegnersi se la regione resta (K-203)? La campitura con l'età basta come stima (K-201)? (d) Il ventaglio vale il 97–98 % dell'ombra? (e) Demo con ombra più larga o sosta. (f) Persone e sensore.

**Rifare:** `cd f8-continuita/10-triage; PYTHONDONTWRITEBYTECODE=1 timeout 120 python3 riconta_arbitro.py > riconta_arbitro.txt`.
