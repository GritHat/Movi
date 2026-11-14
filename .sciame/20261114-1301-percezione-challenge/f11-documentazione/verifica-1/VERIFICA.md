# Verifica avversaria di `STATO_PROGETTO.md`, parte 1 di 3 — f11 (`sciame-validazione`)

**Oggetto.** `f11-documentazione/unione/STATO_PROGETTO.md`, versione 1 (17:05:19), righe 1–536 su 1609 (`wc -l`): testata, sintesi, legenda, indice, cap. 1, cap. 2, cap. 3 fino al §3.5. Lavoro dalle 17:05:44 alle 17:18 del 14 novembre 2026 (`date -Is`). I percorsi sono relativi a `.sciame/20261114-1301-percezione-challenge/`.

## 0. In testa

**Esito in una riga.** Le cifre sono trascritte bene (circa il 99 % torna), ma ho trovato **4 cifre sbagliate**, **5 cifre a cui manca la condizione che ne cambia la lettura**, **6 cifre il cui file citato non le contiene**, **5 contraddizioni interne** e **due marche di stato applicate a metà** ([prel.] nel cap. 3, «non vagliato dall'arbitro (f6)» nei cap. 1–3). Nessun file citato manca.

**Cambi di stato che propongo** (dettaglio ai punti indicati).
1. «Lato della zona a 2 m: 13 cm / 10 cm» (§3.2): **smentito** da un conto; vale 26 cm / 20 cm (a1).
2. «Nascono F-301…F-311, K-301…K-309» (testata): **smentito** dal file; sono F-301…F-309 e K-301…K-308 (a2).
3. Limiti geometrici di B1 «[DIM]»: da **dimostrato** a **conto** (b1).
4. Le cifre del cap. 3 prese da `f10-dati/` e `f9-preproposta/`: da senza marca a **[prel.]**, non vagliate dall'arbitro (b2).

**Regole e scostamenti miei.** (1) Ho rieseguito due script dello sciame che stampano soltanto (`f10-dati/02-sensori/controlla_parametri.py`, `f10-dati/04-embedded/geometria_sensori.py`), con `python3 -I`, `PYTHONDONTWRITEBYTECODE=1`, `timeout 20`: nessun file scritto. (2) Lunghezza oltre le due pagine: la consegna chiede di essere esaustivi. (3) Nessuna pagina in rete aperta: le fonti esterne **non sono verificate da me** (sono della verifica dei riferimenti); ho controllato solo due righe nelle copie locali delle schede. (4) Gli orari d'arrivo degli addendum (§1.4) non li ho verificati: il documento stesso li dichiara dedotti.

**Indipendenza.** Condivido con gli autori il modello linguistico e i file dello sciame; non ho visto le sezioni d'ingresso né la conversazione. Il controllo vale per gli errori di trascrizione, di stato e di rimando; **non** per gli errori che stanno già nei file d'origine, salvo dove ho rifatto il conto a mano (a1; geometria di B1, B9, §3.4).

**Previsioni** (`PREVISIONI.md`, scritte alle 17:05:44, prima dei controlli). P1 «≥ 90 % delle cifre torna»: **regge** (circa 99 %). P2 «da 3 a 15 affermazioni più forti del file»: **regge** (8). P3 «al più 2 file citati inesistenti»: **regge** (0). P4 «almeno 2 contraddizioni interne»: **regge** (5).

## (a) Cifre sbagliate

| # | Riga | Nel documento | Valore giusto | Prova |
|---|---|---|---|---|
| a1 | 465 (§3.2, tabella VL53) | «Zona in 8×8: … lato a 2 m» 13 cm (VL53L7CX), 10 cm (VL53L8CX) | **26 cm** e **20 cm** | `f10-dati/02-sensori/controlla_parametri.py`, riga 84, calcola `200*tan(passo/2)`: è la **mezza** zona. Lato = 2·2 m·tan(3,75°) = 0,262 m; 2·2·tan(2,81°) = 0,196 m [conto mio]. Controllo: 8 zone da 26 cm fanno 2,1 m, cioè il campo di 60° a 2 m (2,3 m); 8 zone da 13 cm ne farebbero metà. Lo stesso fattore 2 tocca il 4×4, dove lo script stampa 26 e 20 cm (il vero è 53 e 39 cm), cifre che il documento non usa. L'errore è nel file d'origine (`MODELLO_SENSORE.md` §2, f10, **[prel.]**) e la riesecuzione [ries.] lo ristampa uguale. Contraddice il §3.3 del documento (vedi d1) |
| a2 | 20 (testata) | il verdetto di f9 «fa nascere F-301…F-311, K-301…K-309, H-301…H-311» | **F-301…F-309, K-301…K-308**, H-301…H-311 | `f9-preproposta/13-verdetto/VERDETTO_PREPROPOSTA.md`, riga 5 («Nascono F-301…F-309, K-301…K-308, H-301…H-311»); `grep -o` su tutto il file: nessun F-310, F-311, K-309 (file delle 16:36) |
| a3 | 383 (B8, latenza) | «circa 155 ms»: 95 + 22 + almeno 21,3 | le tre voci elencate fanno **138,3 ms**; manca la quarta, «evento → inizio esposizione, 0–33 ms a 30 fps» (media 16,7), che porta a 155 | `f3/H-012/02-validazione/VERIFICA.md` §3c, prima riga della tabella |
| a4 | 161 (§1.4, punto 4) | k* dell'ultima tappa «da 0,33 a 0,38» passando da tre a cinque persone | i due valori valgono **in 24 ore** (a 36 e 48 ore: 0,48 → 0,56 e 0,60 → 0,72); il piano a 14 ore non li dà | `f9-preproposta/11-pianificatore/CONSEGNA.md`, riga 57 **[prel.]** |

## (b) Affermazioni più forti di ciò che il file sostiene, con la riscrittura

- **b1. Riga 229 (B1, limiti geometrici): «[DIM] nel modello geometrico».** I file dicono «conto geometrico» (`f4/H-012/09-arbitro/VERDETTO.md` §3, R2) e «simulazione o conto» (`f4/H-012/01-avversario/CONTROPROVE.md`, in testa); l'altezza di 1,2 m è un'ipotesi. *Riscrittura:* «[CONTO] geometrico (camera ideale, pavimento piano, altezza di 1,2 m ipotizzata)».
- **b2. Cap. 3, righe 456–498 e 517–524: 26 righe citano `f10-dati/` o `f9-preproposta/` senza [prel.]** (contate con `grep`; nel tratto la marca compare 6 volte). La legenda (riga 67) dice che tutto ciò che viene da f7–f10 è [prel.]. Sono, fra le altre: rumore nominale e di limite per camera, distanze minime, IMU, «filtri attivi di norma», 2,7 σ → 1,9 %, lato della zona, bande di 40/20/13 px e 19/10 cm, 2,08 m e 68,2°, 7770 e 4350 lux. *Riscrittura:* una frase in testa al §3.2 («le cifre prese da `f10-dati/02-sensori/` e `f10-dati/04-embedded/` sono [prel.]: non vagliate dall'arbitro»), oppure la marca in ogni riga. L'errore a1 viene proprio da lì.
- **b3. Righe 163, 271, 333, 369, 402: cifre di f6 senza «non vagliato dall'arbitro (f6)»**, che la legenda (riga 69) promette; nel documento la dicitura compare solo alle righe 838–840. Sono: l'ordine da 1,7 milioni (`QUADRO_DOMINIO.md`), 1,18° (`MOTO_PROPRIO.md`), «1–1,6 s», 0,42 m a 0,8 m e «pannello a non meno di 1,7 m» (`ATTACCO_SPECIALIZZAZIONE.md`). *Riscrittura:* aggiungere la dicitura.
- **b4. Riga 487: tre OAK-D Pro W «sarebbero l'unica terna che chiude i 360°».** Il file scrive «l'unico … geometricamente valido **che ho trovato**» (`f1/985ccd9bca46/CONSEGNA.md`, §2). *Riscrittura:* «l'unica terna trovata dal ruolo (ricerca non esaustiva, prezzo visto solo in un riassunto)».
- **b5. Riga 456: «Solo I2C, niente USB» per la «famiglia VL53».** L'esito E10 vale per le schede del VL53L7CX e del VL53L8CX (`f10-dati/04-embedded/PREVISIONI.md`, riga 51); il VL53L5CX non è fra quelle controllate. *Riscrittura:* «L7CX e L8CX: solo I2C (verificato sulle due schede); L5CX: non verificato».
- **b6. Righe 45 e 177: accelerazione, «due calcoli indipendenti».** Sono due ruoli dello stesso modello linguistico (lo dice `f2/03-triage/TRIAGE.md`, legenda), e il valore a 10 Hz usa «±30 mm preso come scarto tipo: ipotesi» (`f1/985ccd9bca46/CONSEGNA.md`, critica 5). *Riscrittura:* «due calcoli di due ruoli diversi (stesso modello linguistico); il valore a 10 Hz poggia su un'ipotesi».
- **b7. Riga 69 (legenda) e righe 35–36 (sintesi): «il tasso vero è ≤ 0,75 %», «limite inferiore 99,25 %».** Sono limiti **al 95 %** (`f4/H-012/03-validazione/MISURE.md`, in testa). *Riscrittura:* aggiungere «al 95 % di confidenza»; alla riga 35 dare anche l'intervallo dei 13 su 4800: 0,27 %, limite superiore 0,43 % (`MISURE_V2_bis.md`, tabella).
- **b8. Riga 49 (sintesi, f7): «tre aggiunte leggere candidate».** Il triage marca «14 h» nove voci (V-001, V-002, V-003, V-011 in forma minima, V-012, V-013, T-001, T-002, T-007: `f7-estensione/10-triage/TRIAGE.md`, righe 19–42) **[prel.]**. *Riscrittura:* «tre aggiunte alla mappa (V-002, V-003, V-012) fra le nove voci che il triage mette nelle 14 ore».

Stati controllati che **tornano**: R8 «dimostrazione condizionata» con le cinque premesse; R1 «sostenuto in simulazione a 2 m»; R5 e R6 «nel solo modello dell'avversario»; R7 «non risolto»; F-002 «dimostrato nel modello del punto materiale»; F-003 «per costruzione»; F-006 e F-007 «sostenuto dai dati (simulazioni)»; «tre ToF: verificato sulle fonti, per i sensori citati»; K-014 «aperta, non decidibile senza hardware»; le nove condizioni del verdetto (riga 439) contro `VERDETTO.md` §4.

## (c) Cifre senza file, o con un file che non le contiene

| # | Riga | Cifra | Che cosa non torna | Dove sta davvero |
|---|---|---|---|---|
| c1 | 517 | «quota massima vista a 3 m: 1,95 m» | in `f10-dati/04-embedded/PREVISIONI.md` non c'è (`grep` su tutta la cartella: 0) | uscita a schermo di `geometria_sensori.py` (rieseguito: 1,95 m), non salvata; e `f7-estensione/10-triage/TRIAGE.md`, F-108 **[prel.]**. Conto mio: 1,2 + 3·tan 14° = 1,948 m |
| c2 | 516 | «a 20°: da 1,04 m» | in `f2/04-torneo/TORNEO_parte1.md` non c'è | `f2/04-torneo/esito_attacchi_parte1.txt`, riga 31 |
| c3 | 469 | «Camera Arducam 240×180 … nessuna scheda controllata» | `f1/985ccd9bca46/CONSEGNA.md` non nomina né Arducam né 240×180 | `f1/dfac83300259/CONSEGNA.md`, riga 18; «non controllata»: `f3/fonti/FONTI_VERIFICATE.md`, scostamento 3 |
| c4 | 498 | Livox Mid-360 «360°×59°, 40 m» | non sono nella previsione P9 di `f1/985ccd9bca46/PREVISIONI.md` (lì c'è solo il prezzo) | tabella di `f1/985ccd9bca46/CONSEGNA.md`, marcati (r) |
| c5 | 107 | «7 frasi su 6 righe (`CONTRATTO.md`)» | il contratto dice solo «6 righe» | «7 frasi»: `f3/H-012/02-validazione/VERIFICA.md` §3a. Ricontato: 7 frasi, 156 parole (`wc -w`, titolo compreso) |
| c6 | 232 | montaggio verticale «ma 58° in orizzontale» (versione 2, §6) | la versione 2, §6, dice solo «suolo da 0,74 m» | `f3/H-012/01-scene-dinamiche/SOLUZIONE.md` §4 |

**Non verificato da me:** gli otto orari d'arrivo degli addendum (riga 144 e seguenti: dedotti); il contenuto delle pagine in rete riaperte da [arch.] e [req.] (righe 163, 383, 384); i prezzi.

## (d) Contraddizioni interne al documento

- **d1. Riga 465 contro riga 503.** Una zona di 13 cm a 2 m (7,5°) darebbe 1,9 zone su una persona larga 0,5 m a 4 m; il §3.3 ne dà 0,95, che è giusto (0,5 m / 0,524 m). Si risolve con a1.
- **d2. Riga 229 contro righe 40 e 516.** Gli stessi limiti (1,24 m, 1,09 m, 2,41 m) sono «[DIM]» in B1, «conto, camera ideale» nella sintesi e «conto geometrico» nel §3.4. Si risolve con b1.
- **d3. Riga 383.** Le tre voci scritte non sommano il totale dichiarato (a3).
- **d4. Riga 292 contro riga 884.** B4 scrive «0,927 / 0,916 / 0,902 a 2 s»; il §4.4, punto 12, dice che 0,902 è la fascia 1,5–2,5 s del terzo generatore (0,890 sull'intero). B4 va corretto o deve rimandare lì.
- **d5. Riga 477.** Gemini 335, fascia ideale «0,26–3 m»: fra i tre file citati nella stessa riga, `f10-dati/02-sensori/parametri_sensori.json` (riga 256) e `MODELLO_SENSORE.md` §1 danno «0,3–3 m» (scheda); 0,26 viene dalla pagina del prodotto (`f3/fonti/FONTI_VERIFICATE.md`). Il §3.8 non lo segnala. Nella stessa tabella (riga 478) l'«errore dichiarato» mescola un RMS (RealSense) e un'accuratezza (Gemini, ±2 %), mentre il «limite di scheda» della Gemini alla riga 480 è calcolato dall'1,5 % di precisione spaziale: va detto.

Segnalo anche, senza contarla: il documento è datato 17:05 ma il controllo «dopo la fotografia» è delle 16:35; vedi e7.

## (e) Che cosa manca di importante rispetto ai file

- **e1. R7, il limite della misura (righe 39, 133, 383, 526).** `f3/H-012/02-validazione/VERIFICA.md` §3c scrive che la misura di R7 «copre solo il terzo tratto» (dal fotogramma al comando audio: 22 ms) e che i 95 ms sono «una camera, medie senza p95». Il documento confronta 155 ms **medi**, dall'evento alla scheda audio, con una soglia sul **95° percentile**, dalla marca di cattura alla chiamata audio: due estremi e due statistiche diversi. Va scritto accanto al confronto.
- **e2. R1 oltre 2 m (righe 38 e 127).** «100 / 85,9 / 26,6 %» da 3 m vale **in avvicinamento**; di traverso da 3 m è 100 % con le tre curve (`f4/H-012/03-validazione/v2_MOB.txt`; `MISURE_V2.md`, P3a: «non chiesto»). Manca «in avvicinamento».
- **e3. Il 28,2 % (righe 334, 418).** È misurato con il pannello da 0,5 m a 1,5 m, su 4,75 m² di libero fra 0,5 e 3 m (`f4/H-012/01-avversario/risultati_a05.txt`, intestazione), non nella geometria corretta della demo (pannello da 1 m a 1,9 m). Lì non è stato rimisurato.
- **e4. Potenza dei criteri di accettazione (tabella del §1.3).** Mancano: «9 su 10» prova solo p > 0,61, e un sistema da 0,75 passa una volta su quattro; «5 su 5» prova solo p > 0,55; per dichiarare ≥ 99 % su R8 servono 300 occlusioni senza errori, 30 sostengono ≥ 90 % (`f3/H-012/02-validazione/VERIFICA.md` §3b). `grep` su tutto il documento: 0 occorrenze. È ciò che dice quanto vale ogni soglia della tabella.
- **e5. B5, riga 330: «i bracci che dovevano fallire sono falliti».** Manca la nota (a) del verdetto: nella lettura «gruppo tagliato = ingresso» due bracci su tre danno 0 su 4800 (`VERDETTO.md`, in testa). Il documento la riporta solo al §4.4, punto 4: serve il rimando. Nella riga di C1 (324) manca anche l'esito della riprova: 2 riagganci sbagliati su 1200 nella scena T (`MISURE_V2.md`, P2b).
- **e6. B2 e R2, ipotesi 11 dell'audit (righe 233, 247, 531).** Mancano: con la curva pessimista, a 3 m, l'85 % delle celle ha almeno un pixel di suolo sopra 0,07 m; con la profondità allineata al colore l'ostacolo di 15 cm è invisibile sotto 1,45 m e «l'accettazione di R2 fra 1,1 e 3 m cade» (`f5/02-audit/AUDIT.md`, ipotesi 11).
- **e7. Testata, «dopo la fotografia».** (i) Di `f8-continuita/12-torneo/TORNEO.md` si cita solo «C-EST: smentita»; lo stesso file, riga 9, propone «**Ciclo di vita del nucleo (B5): smentito**» (la regola «ultima misura a meno di 0,40 m dall'ombra» chiude la traccia all'ingresso): tocca il nucleo, **[prel.]**, non vagliato. (ii) Fra le 16:35 e le 17:05 sono comparsi, e non sono nominati: `f8-continuita/13-soluzione/MODIFICHE_CONTINUITA.md` (16:52), `f7-estensione/13-soluzione/DECISIONE.md` (17:03), gli script di `f10-dati/20-validazione/` (16:49–17:05). Non li ho letti.
- **e8. Riga 228: f = 424 px.** Corrisponde a un campo di 90° su 848 px, non agli 87° dichiarati nella stessa tabella (`VERIFICA.md` §4: «848 px, 90°»; `controlla_parametri.py` stampa «campo dagli intrinseci 90,0 × 59,0 (dichiarato 87 × 58)»). Con 87° il rumore nominale sarebbe circa il 5 % più basso [conto mio]: piccolo, ma va detto.

## (f) Quante cifre ho controllato

Unità: la voce numerica (un valore, o una terna o un intervallo riportati insieme). Conteggio a mano, incerto di qualche unità per blocco.

| Tratto (righe) | Voci controllate | Il valore torna | Note |
|---|---|---|---|
| Testata e sintesi (1–51) | 41 | 39 | a2 (due intervalli di sigle) |
| Legenda e sigle (53–79) | 7 | 7 | — |
| §1.1–1.3 (97–138) | 34 | 34 | citazioni della traccia e 20 parole ricontate con `grep` |
| §1.4–1.5 (140–182) | 35 | 35 | a4 è una condizione mancante; orari non verificati, fuori dal conto |
| §2.1, B1–B3 (186–283) | 66 | 66 | 14 file grezzi riaperti |
| B4–B5 (285–347) | 50 | 50 | d4, e3, e5 |
| B6–B9 (349–407) | 52 | 52 | a3: le voci tornano, la somma no; tre conti di [arch.] rifatti |
| §2.3–2.4 (409–439) | 30 | 30 | somme 54 e 48 rifatte |
| §3.1–3.2 (443–498) | 115 | 113 | a1 (due valori) |
| §3.3–3.5 (500–536) | 62 | 62 | 14 conti geometrici rifatti a mano |
| **Totale** | **circa 490** | **circa 486 (99 %)** | |

Delle voci che tornano: 5 hanno una condizione mancante che ne cambia la lettura (a4, d4, e2, e3, e1), 6 stanno in un file diverso da quello citato (c1–c6), 1 è discordante fra i file citati (d5). **File citati nella mia parte che non esistono: 0.** Righe delle copie locali delle schede ritrovate: 2 su 2 (`f9-preproposta/07-lidar/scaricati/vl53l7cx_ds.txt`, righe 42 e 883). Conti d'altri ruoli rifatti da me e tornati: 1,34 m² su 4,75; 1,49, 1,67 e 1,56 m del pannello; 2,16, 1,24, 1,04, 0,74 m del suolo; 2,41 e 3,79 m; 0,26 e 1,00 m a 0,25 m di quota; 40/20/13 e 21/11/7 px; 19,0 e 10,0 cm; 2,08 m e 68,2°; 1,27 e 0,95 zone; 13 e 12 punti; 1,9 e 1,7 punti.

## Stati proposti

- «Lato della zona a 2 m = 13 / 10 cm»: **smentito** (conto; nel modello geometrico della zona quadrata).
- «F-301…F-311, K-301…K-309»: **smentito** (file).
- «Le cifre della mia parte sono quelle dei file»: **verificato** sull'insieme dichiarato in (f), con le quattro eccezioni di (a).
- «Gli stati della mia parte sono quelli dei file»: **verificato** sugli stati elencati in (b), con le otto eccezioni b1–b8.
- Tutto resta **simulazione, conto o scheda**: niente è provato sull'hardware; ciò che viene da f7–f10 e da f6 non è vagliato dall'arbitro.

## Proposte

- **`validazione-f11-1`: correggere la riga 84 di `controlla_parametri.py`** (`2*200*tan(passo/2)`) e `MODELLO_SENSORE.md` §2, a cura dell'autore di f10. *Previsione:* lo script stampa 26 e 20 cm in 8×8, 53 e 39 cm in 4×4. *La smentisce* una scheda ST che dia un'altra larghezza di zona.
- **`validazione-f11-2`: una colonna «quanto prova» nella tabella del §1.3**, con il limite al 95 % che ogni soglia sostiene (e4). *La smentisce* un ricalcolo binomiale diverso da quello di `VERIFICA.md` §3b.
- **`validazione-f11-3`: controllo automatico delle marche.** Ogni riga che cita `f7-`, `f8-`, `f9-`, `f10-` deve contenere «prel», ogni riga che cita `f6-` la dicitura di f6. *Previsione:* oggi fallisce su almeno 26 + 5 righe nella mia parte. *La smentisce* un `grep` che ne trova meno.

## Dopo

Correggere a1–a4 e b1–b3 prima di portare il documento in `documentazione/`; aggiungere e1, e2 ed e4, che cambiano come si leggono R7, R1 e le soglie; rifare il controllo «dopo la fotografia» all'ora della versione (e7).
