# Verifica del ramo H-012 — f3 (`sciame-validazione`)

**In testa.** Lavoro dalle 14:05 alle 14:18 del 14 novembre 2026 (`date -Is`). Non sono l'autore della soluzione. **Nessuna simulazione eseguita:** A e B sono solo progettate (§4). **Cambi di stato proposti:** R4 da «per costruzione» a «per costruzione in un solo verso»; R7 resta **non risolto**, ma il tratto del sensore ha ora una fonte; la tabella di B7 e il caso «sensore coperto» di R6 **non sono decidibili così come scritti**. **Scostamenti e regole violate:** (1) la mia previsione per la prova C non è stata scritta prima della ricerca in rete: vale solo quella del responsabile (14:00:30); (2) tre pagine abbondanti e ingressi in più, come chiede il coordinatore e non `TASK.md`; (3) `TORNEO.md`, `TRIAGE.md` e `scena_parte3.py` letti solo con `grep` (dello script le righe 5, 150–165, 171, 245); `SCHEDE.md` non letto; (4) le pagine web sono lette con l'estrazione automatica dello strumento; la formula del rumore è un'immagine, non letta. **Indipendenza:** condivido con gli autori il modello linguistico, la specifica e i file del torneo; nessun codice.

## 1. Rilettura (V1)

**Numeri ricontati sui file di `f2/04-torneo/`: 20; 17 tornano, 3 con nota.** `esito_attacchi_parte1.txt`: 2,41 m; rampa 5° → 0,80 m; assetto 2° → 2,0 m; 5,4σ; 0,13 s / 0,07 s / 25,07 s; 127°–155° (da cui 205°–233°). `esito_attacchi2_parte1.txt`: 20,1 ms; 0,74 e 1,11 m. `risultati_E_parte2.txt`: 0,754; 0,110; 0,9872 e 0,0000 (N = 4000: `torneo_parte2.py`, riga 689). `risultati_A2`: 0,738 / 0,710. `risultati_C`: 1,60 s; 0,811. `risultati_main1_parte3.txt`: 31,5 % e 62,1 %; `kf15` = 30,0 % (riga 19). Particelle 100 / 76,3 / 68,0 % (`main1` r. 47, `main2` r. 55, `ombra` r. 47). 14,4 % (`ombra` r. 55). Torna anche la somma delle ore (48). **Con nota:** (a) 0,902 è la fascia 1,5–2,5 s del generatore G3, non «a 2 s»; G3 intero dà 0,890; (b) 0,440 viene da una prova con q = 0,5 (intestazione di `risultati_B2`), non con il q = 0,2 del ramo; con q = 0,2 `risultati_due_parte3.txt` dà 74 % di scambi, 44 % muti; (c) «2,0 ms per la griglia» non è in nessun file del torneo: è il numero dell'autore, riportato nel triage.

**Dove la soluzione afferma più di quanto i file sostengono.**
1. **«Copertura 0,90–0,93»** (B5). I file danno 0,890–0,934, sul cerchio **intero** e non su quello ritagliato; 0,56–0,66 per chi torna; 0,000–0,056 per le riemersioni sotto 1,5 s di G3 (n = 157, `risultati_A`). Vale per miscele con pochi ritorni.
2. **Rilascio «≥ 3 fotogrammi».** Nel torneo, con tre fotogrammi, la traccia si chiude a persona nascosta nel 14,0 % a 3 m e nel 53,0 % a 2,5 m (`risultati_k001_parte3.txt`, righe 50 e 82), e nel 45–50 % con l'ombra a −20 cm. Portata dichiarata e demo stanno lì. Che la fascia di guardia lo curi non è in nessun file. Il testo è anche ambiguo: le celle «viste libere fuori dalla fascia» sono già fuori dallo strato 1 (invariante 4); alla lettera la regola non rilascia niente.
3. **§4, regola «mobile».** 98,7 % è una quota di **finestre**, 75,4 % è «entro 1 s dalla prima misura»: due metriche diverse, non confrontabili prima della prova B.
4. **R4 «per costruzione».** L'invariante 3 dà «osservato ⇒ misura in porta», non il verso opposto: un rilevamento falso al bordo del pannello, a soggetto nascosto, esce «osservato». Le simulazioni non hanno rilevamenti falsi (intestazioni della parte 3: solo Pd = 0,9).
5. **B7 non è valutabile.** Se «non osservato» è il messaggio più grave, ogni settore lo emette sempre: il suolo si vede solo da 1,24 m (`esito_attacchi_parte1.txt`, P2b), oltre 3 m è fuori portata, dietro ogni ostacolo c'è ombra. Manca la zona di valutazione, e «in ombra» non ha posto in graduatoria.
6. **Mancato rilevamento in campo aperto** (un fotogramma su dieci): non è «osservato» (invariante 3) e non è «previsto» disegnabile su celle libere (invariante 4). L'uscita di quel ciclo non è definita.
7. **R6, «sensore coperto».** B8 scatta sui fotogrammi fermi o identici; una mano sul sensore dà fotogrammi nuovi, pieni di buchi. Nessuna regola nominata produce il segnale.
8. **T_g contro gli invarianti 5 e 7.** Dopo 10 s cade l'avviso: il settore torna a suonare come un'ombra vuota. Nessun «libero» nasce, ma un timer cambia ciò che l'utente sente. L'invariante 7 vale fino a T_g.
9. **B1 contro B9.** B9 si dichiara invalidata sopra 5 cm di rumore a 3 m; al limite di scheda sono 9 cm (10,4 cm a 3 m al suolo, stesso file, P2), col valore nominale 3,4 cm (§4). Lo decide solo la misura. L'attore a 3 m sta sul bordo della griglia. La «similitudine» di B9 non lo è: 1 m d'ombra contro i 2 m della scena simulata.

B1, B2, B4, B6 reggono rispetto alle premesse dichiarate; B3, B5, B7, B8, B9 con le riserve sopra.

## 2. Che cosa rende corretto ogni invariante

| # | Garantito da | Ipotesi | Caso che lo viola |
|---|---|---|---|
| 1 | costruzione | pavimento piano, assetto noto, profondità valida = giusta | vetro; ostacolo alla quota della testa sotto 2,41 m (suolo visto sotto); primo gradino in discesa; riflessi |
| 2 | costruzione (stati esaustivi) | un buco arriva come «nessun dato» | filtri dell'SDK che riempiono i buchi |
| 3 | costruzione, in un verso | nessun rilevamento falso in porta | bordo del pannello: **misura** |
| 4 | costruzione sull'ombra stimata; **misura** su quella vera | errore d'ombra ≤ 20 cm, corpo ≤ 40 cm | zaino, due persone affiancate |
| 5 | costruzione per il «libero» | T_g dichiarato | sosta oltre 10 s |
| 6 | costruzione, se «vede lo sfondo» = suolo visto | suolo visibile dietro il bersaglio | tessuto scuro: non verificato |
| 7 | costruzione, fino a T_g | occlusore fermo | occlusore mobile: l'ombra d'ingresso non è più definita |
| 8 | costruzione nel software; **misura** sulla camera | contatore affidabile | fotogrammi ripetuti con contatore nuovo; sensore coperto |
| 9 | costruzione (interfaccia) | — | nessuno trovato |

Tutto vale a **sensore fermo**. Sopra v_max cade solo il riaggancio (`risultati_vmax_parte3.txt`: identità 80 % a 2,6 m/s, 0 % a 3 m/s), non lo strato 1.

## 3. Prova C, eseguita a mano

**(a) Regole frase per frase** (7 frasi; con `grep`: «riconoscere» 1 volta; «360», «classific-», «massa», «acceler-» 0).

| Frase | Requisito → componente | Misura |
|---|---|---|
| 2 «riconoscere… non basta: un ostacolo può nasconderlo… mentre la scena continua a cambiare» | R3 → B5; «riconoscere» → B6 | 26 su 30; **nessuna misura con la scena che cambia durante l'occlusione** |
| 5 «feedback spaziali chiari e tempestivi quando le condizioni lo consentono… quando necessario» | R5, R6 → B7, B8 | solo «tempestivi»: **«chiari», «spaziali» (direzione) e i segnali falsi di R6 senza misura** |
| 6 «orientamento assistito… oppure monitoraggio» | applicazione → decisione 1 | coperta **per lettura** (sensore e utente fermi) |

Le frasi 1 e 3 sono contesto; la 4 e la 7 danno R1–R4, R7 e R8 (B2–B5, B8), con le misure di (b). Esito di C1 sulla soglia scritta dal responsabile: **regge**. Restano tre clausole senza misura e una frase coperta per lettura.

**(b) Le misure di accettazione.** L'unità è il passaggio, non il fotogramma. Limiti al 95 % calcolati da me (binomiale esatta).

| R | In tre minuti? | Verità di riferimento | Decidibile con le ripetizioni indicate? |
|---|---|---|---|
| R1, 9 su 10 | no: registrazioni; in demo 1–2 passaggi | tacche a terra ogni 0,5 m, metronomo, video annotato (± 33 ms) | debole: prova solo p > 0,61; un sistema da 0,75 passa una volta su quattro |
| R2, 5 su 5 | sì | nastro dalla verticale del sensore (± 1 cm) | prova solo p > 0,55: dimostrazione, non tasso |
| R3, 26 su 30 | no: registrazioni | fili dalla lente ai bordi del pannello, nastro sull'ombra, seconda camera | passa nel 52 % con 0,85 vero, nel 10 % con 0,75. **Non dice se contano le riemersioni da «perso»** (A4 ne prevede il 30–70 %) |
| R4, 0 fotogrammi | sì | seconda camera; «nascosto» = due piedi oltre il nastro | solo escludendo la transizione (corpo di 40 cm a 1 m/s: 6 fotogrammi ambigui) |
| R5, ≤ 300 ms | sì, dai registri | fotogramma RGB annotato | sì; ripetizioni non indicate |
| R6, entro 1 s | sì | video con mano e audio | ripetizioni **non indicate**: propongo 10 per causa, e 0 segnali falsi in 60 s |
| R7, p95 ≤ 150 ms | sì, per fotogramma | la marca di cattura nell'orologio dell'ospite | sì per il tratto interno; no dal fotone al suono |
| R8, ≥ 99 % | no | come R3 | **no:** servono 300 occlusioni senza errori; 30 sostengono ≥ 90 % |

**(c) Bilancio della latenza.**

| Tratto | Valore | Fonte e stato |
|---|---|---|
| evento → inizio esposizione | 0–33 ms a 30 fps | calcolo |
| esposizione → fotogramma nell'applicazione | media 95 ms a 30 fps; 127 a 15; 47 a 60; 39 a 90 | documento del costruttore sulla D435, tabella 4, modi 848×100: https://dev.realsenseai.com/docs/high-speed-capture-mode-of-intel-realsense-depth-camera-d435 . Una camera, medie senza p95; che cosa includa la misura: non verificato |
| fotogramma → comando audio | 22 ms | 20,1 ms del torneo + 2,0 dell'autore, Python su scene sintetiche: non è il prototipo |
| comando → primi campioni (sintesi vocale) | ignoto | nessuna fonte; zero con frasi preregistrate |
| campioni → scheda audio | ≥ 21,3 ms | un quanto 1024 / 48000, default di PipeWire: https://docs.pipewire.org/page_man_pipewire_conf_5.html |
| scheda → suono (cavo, Bluetooth) | ignoto | nessuna fonte trovata |

Le sole voci note sommano **circa 155 ms in media**: sopra 150 ms già senza sintesi né uscita. La misura di R7 copre solo il terzo tratto. **Esito di C2: non risolta**, come previsto dal responsabile; per il sensore una fonte c'è, per l'audio solo un pezzo. In pratica: flusso a 60 o 90 fps usando l'ultimo fotogramma, frasi preregistrate, uscita via cavo.

## 4. Progetto delle prove A e B (congelato alle 14:18; le eseguo in f4)

**Scena.** Piano del suolo, sensore fermo all'origine, campo 87°, 15 Hz, q = 0,2. Geometria T (confrontabile col torneo): pannello a 2 m largo 1 o 2 m, pedone sulla linea a 4 m. Geometria D (demo): pannello a 1,5 m largo 0,5 o 1 m, attore a 2,5 e a 3 m, griglia fino a 3 m. **Corpo:** disco di 40 cm (nel torneo era un punto), rilevabile se sono visibili almeno 3 colonne da 1°; la misura è il centro della parte visibile, più il rumore. **Ombra vera:** l'intervallo angolare del pannello. **Ombra stimata:** i due bordi spostati di −20, 0, +20 cm alla distanza del pedone. **Comportamenti:** v uniforme fra 0,8 e 1,4 m/s, rampe di 1 m/s²; prosegue; sosta di 2–4 s in un punto uniforme dell'ombra; torna indietro; esce dal lato lontano restando in ombra.

**Rumore R(z).** Radiale σ_r = z²·s / (f·B), con f = 424 px (848 px, 90°), B = 50 mm, s = 0,08, dal documento del costruttore («The depth error scales as the square of the distance away»; «Both are for subpixel=0.08»; «D435 with HFOV=90deg, Xres=848, and baseline=50mm»): https://dev.realsenseai.com/docs/tuning-depth-cameras-for-best-performance . Dà 1,5 / 3,4 / 6,0 cm a 2 / 3 / 4 m. Seconda curva, pessimista: «2 % a 2 m» scalato con z² (4 / 9 / 16 cm). Terza, per confronto: 5 cm·(z/2)² del torneo. Laterale: z·1°/√12.

**Ripetizioni.** 400 passaggi per cella, 24 celle in A (4 × 2 × 3). Con zero fallimenti il limite superiore al 95 % è 0,75 % per cella: sotto l'1 % che il 99 % richiede (ne servono almeno 300). Per le soglie all'85–90 % l'errore tipo è 1,8 %: una stima entro ± 3,5 punti dalla soglia è «non risolta». Seme base 5101.

**Definizioni operative.**
- **Nascosto:** N1 = centro del corpo nell'ombra vera (quella del responsabile); N2 = soggetto in campo e in portata, senza misura associata per ≥ 3 fotogrammi di fila.
- **Contiene (strato 1):** la cella del centro è nello strato 1. Falsificatore dell'arbitro: un fotogramma N1 fuori. Falsificatore mio, a parte: un fotogramma N2 con il centro fuori e nessuna cella del corpo «occupato osservato».
- **Visto libero:** cella che il sistema classifica «libero» in quel fotogramma; contro la verità, cella davvero visibile e vuota.
- **Contiene alla riemersione (strato 2):** tre esiti sul totale delle riemersioni: contenuta con lo strato 2 mostrato; contenuta ma stato «perso»; non contenuta. Solo il primo vale per R3.
- **Rilascio (A7):** una cella esce dallo strato 1 se è «libero» per ≥ 3 fotogrammi e dista più di g dall'ombra stimata in quel momento. **Pendente (A6):** traccia non riagganciata con la stessa ombra d'ingresso.

**Le definizioni del responsabile sono eque?**
- **«Nascosto» (A1):** fedele al testo dell'arbitro, ma con errore ≤ 20 cm e fascia di 40 cm l'esito è deciso dalla geometria (margine 20 cm) prima di simulare. Contare «a parte» i corpi in parte visibili e non rilevati toglie gli unici casi vicini al bordo: **favorisce la soluzione.** Li conto dentro (N2). Aggiungo la parte informativa: l'errore d'ombra oltre il quale il contenimento scende sotto il 99 %, da −50 a +50 cm a passi di 10, con corpo di 40 e di 60 cm.
- **A2 (b), «0,60 m dal bordo vero»:** somma l'errore alla fascia; la soglia coincide col caso peggiore della costruzione e non può fallire. **Sposta la soglia.** La tengo come controllo del codice, e misuro il costo: area dello strato 1 su suolo davvero visibile, in m² e in quota.
- **A3, tolleranza di 0,40 m:** equa (mezzo corpo, errore d'ombra e un passo di moto fanno 0,35 m, conto mio); riporto anche 0,20 m. **Non equa la miscela:** la soglia dell'85 % è valutata solo su «prosegue» e sulla miscela 60/15/10/15, mentre a pesi uguali il responsabile stesso prevede 0,78–0,88. Fisso ora: esito per comportamento e sulle due miscele.

**Prova B.** Muro fermo a 2, 3, 4 m: 12 000 finestre da 1 s per distanza. Pedone a 0,5 m/s, di traverso e in avvicinamento, da 2, 3, 4 m: 2000 passaggi. Una sola metrica per le due regole, stessi semi: tempo dalla prima misura alla prima etichetta «mobile», soglia 1,0 s più un fotogramma. Spostamento sulle misure grezze, con σ(z) al capo più lontano della finestra. Tre curve di rumore; filtro con R giusto, poi con σ creduto la metà e un terzo del vero; a parte, 2 % di misure anomale. **Mie previsioni (14:18, a calcolo, prima della prova; senza misure anomale):** in avvicinamento da 2 m lo spostamento regge con tutte e tre le curve (≥ 95 %); da 3 m regge con la nominale e cade con le altre due (< 30 %); da 4 m solo con la nominale, sul filo (70–95 %). Falsi sul muro: ≤ 0,1 % con R giusto, 1–5 % con σ creduto la metà, > 10 % con un terzo. Mi smentisce un valore fuori da queste fasce.

**Che cosa condivide il mio simulatore con quelli del torneo:** la specifica (comportamenti, 15 Hz, q, soglie χ², v_max, T_g), il modello linguistico che lo scrive, il rumore gaussiano, l'ombra come intervallo angolare. Non condivide codice, semi, generatore delle traiettorie, forma del corpo, curva del rumore. È cieco ai difetti della specifica comune.

## 5. Ciò che le classi 1–2 non decidono, in ordine d'importanza per la demo

1. **Errore vero della maschera d'ombra, corpo in parte coperto** (strato 1 e rilascio): 30 occlusioni con fili e nastro sull'ombra vera e seconda camera; distanza massima fra bordo stimato e nastro.
2. **Rilevamenti falsi al bordo del pannello** (R4): cinque minuti di scena ferma col pannello; zero tracce confermate.
3. **Rumore del centro di una persona che cammina a 2–3 m** (R1): muro per 60 s, poi persona a 0,5 m/s sulle tacche.
4. **Latenza dal fotone al suono:** telefono a 240 fps su evento e altoparlante, 20 eventi; si dichiarano mediana e massimo, non il p95.
5. **Sensore coperto, cavo staccato, fotogrammi ripetuti** (R6): dieci volte per causa.
6. **Sala della demo:** vetro, abiti scuri, sole dalle finestre; cinque minuti ciascuno.
7. Feedback con persone bendate (K-010); sensore indossato (F-008).

## 6. Proposte e dopo

- `validazione-1`: nella regola «mobile», media di 3 fotogrammi ai due capi della finestra: il rumore della differenza scende di √3. Previsione: velocità minima vista ridotta di circa 1,7 volte; la smentisce la prova B con un guadagno sotto 1,3.
- `validazione-2`: segnale R6 quando la quota di pixel di profondità validi scende sotto una soglia per N fotogrammi. Previsione: copre «sensore coperto»; la smentiscono dieci prove con la mano sul sensore.
- `validazione-3`: B7 valutata su una zona dichiarata (per esempio 1,24–3 m nel campo), con «in ombra» in graduatoria. Previsione: su scena libera nessun settore dice «non osservato»; si prova a mano su tre scene.

**Dopo.** Il responsabile scioglie le critiche 2, 5, 6, 7: sono definizioni, e senza di esse A7 e R5 non si misurano. Io eseguo A e B in f4 con questo progetto, senza cambiarlo.
