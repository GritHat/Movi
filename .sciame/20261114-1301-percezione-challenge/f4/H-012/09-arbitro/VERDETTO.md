# Verdetto del ramo H-012 — f4 (`sciame-arbitro`)

**In testa.** Lavoro dalle 2026-11-14T14:56:11+01:00 (`date -Is`). Giudico `f4/H-012/05-correzioni/SOLUZIONE_V2.md` (versione 2). **Verdetto: non «adottabile» nel senso della pipeline; adottabile come progetto di prototipo, con nove condizioni (§4).** **Cambi di stato:** (1) R8 si divide in due enunciati con stati diversi (§1); (2) la riga dell'invariante 1 («0,33 m, meno della fascia») è **smentita**: il conto dell'audit torna (0,288 s · 2,5 m/s = 0,72 m [arb.]); (3) «il pannello da 1 m regge senza C6» è **smentita**: C6 è obbligata; (4) nascono K-013…K-018. **Scostamenti:** tre pagine e ingressi in più (addendum, selezione, audit, fonti), come chiede il coordinatore e non `TASK.md`; nessuna simulazione rieseguita; `f6-specializzazione/` non letto; di `PIANO_MISURE.md`, `ATTACCO.md`, `FONTI_VERIFICATE.md` e della versione 1 lette solo le parti citate; la lunghezza è al limite delle tre pagine (circa 2300 parole). **Regola violata:** nel controllo finale ho lanciato un `git status` (sola lettura, uscita scartata, nessuna modifica), contro il «niente git» della consegna. Tutto è **simulazione o conto, a sensore fermo**.

**Cifre ricontate sui file** (`09-arbitro/riconta_arbitro.py`, sola lettura). 0 falliti su 14 400 in 36 celle (`v2_R8.txt`); 13 su 4800 a −20 cm con Pd 0,9, in 8 celle su 12, e 0 su 9600 a 0 e +20 cm (`v2_R8_pd09.txt`); bracci 4800, 4798, 4789 su 4800; 13 / 3 / 8 / 2 / 6 / 0 e strati accesi 613–686 (`bis_R8a`, `bis_R8b`); 800 su 800, 799 su 799, 17 su 800 (`bis_FURTO.txt`); 2400 su 2400 e 2 su 1200 (`v2_SECOND.txt`); 61,1 e 80,2 → 100 %, «torna» 99 → 47–50 % (`v2_C6.txt`); 400 → 0 su 400 (`v2_WALLP.txt`); 118 su 20 000 (`v2_PD.txt`); 48 celle, 0 passaggi fuori nella lettura (ii) e 4800 nella (i) (`out_A_*.txt`); 9,5–100 → 0,0 %, 15–750 → 0, 45,47 contro 1,01 m², 28,2 %, 100 → 0,0–0,2 % (`risultati_a01`, `a04`, `a05`, `a06a`); 54 ore, 38 in serie. **Tornano, con due note.** (a) «I bracci sono falliti tutti» (`MISURE_V2.md`) vale nella lettura principale; nella lettura «gruppo tagliato = ingresso» due bracci su tre danno 0 su 4800 (`v2_R8_cut.txt`). Nella principale falliscono con «entrata in ombra 0»: cade la regola d'ingresso, non il contenimento. (b) «7198 su 7198» non è stampato in `bis_FURTO.txt`: torna solo il denominatore.

## 1. Verdetto per proprietà

| Proprietà | Stato | Dominio e file |
|---|---|---|
| **Correttezza**: «ciò che non è visto non è mai libero» (invarianti 2, 5, 9) | **dimostrazione condizionata**, come argomento per costruzione: controllo dell'invariante, non dato | premesse: quattro stati esaustivi, un buco arriva come «nessun dato», profondità valida = giusta, pavimento piano, sensore fermo (`VERIFICA.md` §2). Nessuno script ha calcolato un «libero» da una profondità (`AUDIT.md`, 2) |
| **Correttezza**: garanzia dello strato 1 (chi sparisce resta «possibile presenza») | **evidenza in simulazione** con Pd = 1; **controesempio** con Pd = 0,9 e ombra a −20 cm; margine dell'invariante 1 **smentito** | 0 su 14 400 con i bracci falliti (`MISURE_V2.md`); 13 su 4800 (`MISURE_V2_bis.md`); `AUDIT.md`, 3 |
| **Correttezza** sulla camera vera | **questione aperta** | nessun fotogramma vero elaborato; decide H0–H13 |
| **Completezza** (R1–R8) | **verificata come mappa**, esaustiva sulle 7 frasi delle regole: ogni requisito ha componente e misura; **nessuna misura superata**; R7 aperta; l'applicazione è coperta per lettura | `VERIFICA.md` §3; `SOLUZIONE_V2.md` §7 |
| **Efficacia** | **evidenza in simulazione**, con due controesempi | identità 100 % (limite inferiore 99,25 %) con una traccia pendente; «mobile» 100 % a 2 m (N = 2000); secondo soggetto dalla stessa ombra: sbagliato 2400 su 2400; chi torna: 47–50 % con C6 (`MISURE_V2.md`) |
| **Costo** | **questione aperta** | 54 ore-persona (stima dell'autore), 38 in serie contro 24 (`AUDIT.md`, 8); latenza: 155 ms noti contro la soglia di 150; fascia sul 28,2 % del libero visto; 12,8–14,3 % di strati accesi a vuoto con Pd 0,9 |

## 2. Le quattro verifiche

- **V1, rilettura** (`sciame-validazione`, `f3/H-012/02-validazione/VERIFICA.md`, versione 1): 20 numeri ricontati, 17 tornano, 3 con nota; nove punti in cui il testo affermava più dei file, ripresi dalla versione 2. **Rilettura indipendente della versione 2: manca** (la copre in parte il mio riconteggio).
- **V2, audit** (`sciame-rovesciatore`, `f5/02-audit/AUDIT.md`): dodici ipotesi nascoste. Cambiano il verdetto la **1** (i filtri della camera trasformano un buco in un dato: R8 e R6 sul vero), la **3** (margine dell'invariante 1) e la **12** (il nucleo provato è il profilo «sensore fermo»). Entrano nelle condizioni la 2, 4, 5, 8. L'audit è arrivato dopo la versione 2: **nessuna è nel testo**.
- **V3, controesempi** (`sciame-avversario`, `CONTROPROVE.md`; `MISURE.md`): dodici attacchi. **Cadute:** riaggancio al bordo, attore a 3 m, graduatoria di B7, tetto di 10 s, strato 1 esteso, «mobile» sui gruppi tagliati, finestra fissa, «libero» senza memoria, affidabilità persa, frasi in voce, rilascio sul punto previsto, pannello da 0,5 m. **Corrette con prima e dopo e riprovate insieme da un altro autore:** C1, C2 (con il pannello a 1,9 m), C4, C5, C6, C8, media di 3, rilascio cella per cella. **Con prima e dopo solo nel simulatore dell'avversario:** C3, C9, C10, C11. **Senza riprova:** C7, C12, criterio a due stadi (un conto), «non confermato», «metà dell'area del cuneo», seconda persona nell'atto 4, B7 e B8 nell'insieme.
- **V4, consolidamento:** questo file. Condivido con tutti il modello linguistico e la specifica; nessun codice.

## 3. Requisiti e contraddizioni

| R | Stato dopo le prove |
|---|---|
| R1 | sostenuto in simulazione a 2 m (100 %, tre curve di rumore; muro: 0 falsi su 400 con C6); oltre 2 m non risolto |
| R2 | conto geometrico fra 1,1 e 3 m, nessuna profondità simulata: non verificato; ostacoli bassi sotto 1,09 m invisibili |
| R3 | identità sostenuta in simulazione con una persona nascosta e pannello fermo; controesempio K-016; l'area prevista alla riemersione è tolta dalla promessa (0,5–1,2 %) |
| R4 | per costruzione, in un solo verso; rilevamenti falsi mai simulati; ramo «campo aperto» da ridefinire (K-018) |
| R5, R6 | corrette nel solo modello dell'avversario (C3, C9, C10); buchi persistenti e filtri della camera non provati (audit, 1, 6, 7) |
| R7 | **questione aperta** (H12) |
| R8 | «mai libero sul non osservato»: regge per costruzione. Garanzia dello strato 1: K-014. Vetro: smentito, limite dichiarato |

| K# | Stato | Decide |
|---|---|---|
| K-001, K-002, K-003 | risolte in simulazione (nessun tetto e rilascio cella per cella; due strati; q = 0,2), aperte sul vero | H9, H10 |
| K-004 | **aperta nel numero**: «metà dell'area del cuneo» è fissata, non misurata; il «previsto» dura 0,40–0,53 s | — |
| K-005, K-008 | **decisione dell'utente**; K-008 sciolta in parte dagli addendum | — |
| K-006 | risolta per composizione; il «libero» ora dura 3 fotogrammi (K-015); vetro aperto | H2 |
| K-007 | **aperta**: a 2 m passano tutte e due le regole | H1, H8 |
| K-009, K-010, K-011 | 360° risolta, sole aperta; feedback aperta; R3 fissata, R7 aperta | H3; persone bendate; H12 |
| K-012 | apparente, risolta dalle fonti | — |
| **K-013** strato 1 «sola ombra» contro «con le celle contigue» | **risolta in simulazione**: cuneo tagliato alla griglia; chi esce dalla portata è «non osservato» e l'uscita dice «può aver lasciato l'area» | 0 su 14 400 |
| **K-014** anomalia Pd 0,9 e −20 cm | **aperta, non decidibile senza hardware** | «libero» dentro l'ombra vera |
| **K-015** invariante 1 e latenza | **aperta**: 0,72 m a 2,5 m/s; margine zero a 1,4 m/s | H12, poi una scelta |
| **K-016** secondo soggetto mai tracciato, stessa ombra | **controesempio in simulazione**; nessuna regola lo esclude; le celle restano «in ombra» per costruzione | H11; regola nuova |
| **K-017** C6 necessaria contro il suo costo su chi torna | aperta: costo da dichiarare | H9 |
| **K-018** «a meno di 0,40 m da un'ombra» è sempre vero per l'ombra propria (audit, 4) | **aperta**: difetto di scrittura; i simulatori usano solo l'ombra dell'occlusore | camminata in campo aperto |

**K-014, valutazione.** Il criterio sta in `sim_v2.py`, righe 731–735: il passaggio fallisce se il centro del soggetto senza misura sta in una cella fuori dall'ombra **stimata**, senza avviso entro la fascia. A −20 cm quella striscia sta **dentro l'ombra vera**: la camera non vi vede il suolo. Per l'invariante 1 una cella così è «libero» solo se il sensore vi restituisce una profondità valida e sbagliata. Il simulatore non calcola profondità: assegna «libero» per definizione. Sono quindi due cose.
- **Difetto vero della soluzione**, indipendente dal modello d'errore: con rilevamenti mancati la traccia si chiude prima dell'ombra e lo strato 1 non nasce. A 0 e +20 cm il soggetto sta però in celle «in ombra» (0 falliti su 9600): si perde l'avviso legato alla traccia, non la regola «mai libero».
- **Il «libero» falso** esiste solo se la maschera d'ombra sbaglia verso l'interno con dati validi: né artefatto né difetto provato. L'audit (10) indica su un lato una banda senza dato, cioè il verso sicuro; l'altro lato non è stimato.
- **Decide:** pannello sul suolo segnato col nastro, 150 fotogrammi; celle «libero» dentro l'ombra vera (soglia: 0) e banda non valida sui due lati. In simulazione `validazione-5` può chiudere solo il primo punto.

## 4. Adottabile?

**Adottabile come progetto di prototipo, non come sistema validato.** La regola chiede la correttezza dimostrata o verificata sul dominio d'uso e nessuna K# aperta: il dominio d'uso non è mai stato toccato, e sono aperte, fra le altre, K-014, K-015, K-016, K-018. **È adottabile** l'architettura (catena geometrica, tre stati, due strati, invarianti come regole di logica) come progetto da costruire e provare con il protocollo H0–H13 e le soglie scritte prima. **Non si può dichiarare:** «validato», «R8 garantito», «bassa latenza», una soglia qualunque in moto. **Condizioni obbligate nel documento:**
1. filtri della camera spenti (persistenza, riempimento dei buchi) e autoverifica all'avvio: mano sul sensore, pixel validi sotto il 10 % in 3 fotogrammi, altrimenti il programma non parte;
2. fascia a formula, v_max · (età + latenza) più l'errore d'ombra, oppure velocità massima coperta dichiarata (circa 1,4 m/s con 0,40 m e 155 ms, a margine zero); soglie in secondi;
3. pannello alto almeno 1,5 m e largo 1 m, attore a non più di 2,3 m, **una sola persona dietro il pannello**;
4. profilo «sensore fermo» dichiarato: nessuna soglia vale in moto; il criterio dell'IMU è del profilo;
5. C6 obbligata, con il suo costo;
6. garanzia dichiarata solo per chi è stato visto almeno 4 fotogrammi, con una traccia pendente e l'occlusore fermo;
7. limiti scritti: rilevamenti mancati vicino all'ombra, secondo soggetto, vetro, ostacoli bassi sotto 1,09 m, sole;
8. la regola per l'ombra propria fissata prima del codice (K-018);
9. la dicitura «provato solo in simulazione, a sensore fermo», e mai «via libera».

**Per la specializzazione (addendum).** Regge: il contratto d'uscita (tre stati; non osservato mai libero; invarianti 2, 3, 5, 9 come logica) e il metodo (soglie prima, bracci che devono fallire). **Non regge senza prove nuove** (`AUDIT.md`, 12): fascia, zona e portata (a 10 m/s 0,288 s sono 2,9 m); «libero = suolo visto» (in volo o sull'acqua non c'è); il rilascio «mai» (in moto la parallasse scopre l'ombra); il criterio dell'IMU; i parametri del pedone.

## 5. Che cosa è davvero convergente

1. **Tre stati in uscita, mai mescolati**: visto ora, previsto, perso. *Proposta da più ruoli; ha retto a dodici attacchi.*
2. **Ciò che non è visto non è mai dichiarato libero** (ombra, fuori campo, oltre portata, buchi). *Regge per costruzione; nessun «libero» falso in dodici attacchi e 14 400 passaggi simulati; mai provato su una profondità vera.*
3. **Chi sparisce dietro un ostacolo fermo resta «possibile presenza» finché non lo si rivede**; nessun timer toglie l'avviso. *Simulazione; cade in 13 passaggi su 4800 con rilevamenti mancati e ombra stimata stretta.*
4. **Stessa identità al ritorno con una sola persona nascosta**: 100 %, almeno 99,25 %. *Simulazione; con un secondo soggetto mai visto sbaglia sempre: limite dichiarato.*
5. **La previsione vale circa mezzo secondo**, poi il sistema dice «perso»: la continuità la porta l'avviso sull'ombra. *Misurato in simulazione.*
6. **Decide un percorso di geometria e regole** (rilevamento, associazione, Kalman, tabella); la rete neurale mette solo un'etichetta. *Sostenuta da più ruoli; nessun controesempio nei file.*
7. **Massa e accelerazione non si stimano**; la velocità sì. *Dimostrato nel modello del punto materiale (F-002); due calcoli (F-004).*
8. **Tre ToF non danno 360°** (scheda del costruttore: 180°): restano un canale laterale facoltativo, mai «libero». *Verificato sulle fonti, per i sensori citati.*
9. **Una persona a 0,5 m/s è vista entro 1 s a 2 m**: 100 % con tre curve di rumore. *Simulazione; oltre 2 m decide il rumore vero.*
10. **Nessun fotogramma di una camera vera è stato elaborato**: lo dichiarano tutti i ruoli.

## 6. Prossima prova e decisioni dell'utente

**Prossima prova che cambia la decisione:** su hardware, fuori dalle classi 1–2 di questa convocazione; circa un'ora e quaranta in due [arb.: 65 + 17 + 15 minuti]. H0–H6, più tre controlli (autoverifica dei filtri; celle per stato su 150 fotogrammi della sala vuota; «libero» dentro l'ombra vera del pannello), poi H12. Decide K-014, K-015 e R8 sul vero. In simulazione, classe 2: `validazione-5`.

**Decisioni dell'utente.**
1. **Che cosa si dichiara provato:** il profilo «sensore fermo» (stazione a terra, o veicolo uncrewed fermo che decide se ripartire), con il moto a bordo e l'ausilio indossato come profili «non verificati»; oppure attendere l'hardware.
2. **Velocità coperta o fascia più larga** (K-015): circa 1,4 m/s dichiarati, oppure una fascia maggiore, che mette «possibile presenza» su più suolo visto (oggi il 28,2 %).
3. **Fattibilità:** 54 ore-persona, 38 in serie; con 24 ore si taglia (etichetta, strato 2, ToF). Durata, squadra e camera posseduta non sono mai state verificate.

Controfirma: arbitro
