# PIANO_14_4 — versione finale: 14 + 4 ore, cinque persone (`sciame-pianificatore`, f12, passo 21)

Lavoro dalle 18:23:29 alle 18:32 del 14 novembre 2026 (`date -Is`). Percorsi relativi a `S/` = `.sciame/20261114-1301-percezione-challenge/`. Cartella `S/f12-integrazione/21-piano-finale/`: `PREVISIONI.md` (18:23:59, prima dei programmi; esiti in coda), `piano_finale_mc.py` → `risultati_piano_finale_mc.txt`, `variante_c2.py` → `risultati_variante_c2.txt` (il calendario consegnato), `risultati_primo_lancio.txt`, `rilancio_piano_mc.txt`, `rilancio_rifai_mc.txt`. Si rifà con `timeout 300 ../../f10-dati/ambiente/venv/bin/python -I -B piano_finale_mc.py` e `… -B variante_c2.py` (2 s l'uno). **Tutte le durate sono stime, non misure. Tutto ciò su cui il piano poggia è simulazione, conto o lettura di schede: niente è «validato».**

## 0. In testa: cambi di stato, regole violate, scostamenti

- **«Il minimo dimostrabile chiude entro l'ora 14»: non provato, e tolto come obiettivo di calendario.** Con il calendario finale: **0,43** [0,42; 0,44] nella mia lettura (stime mie, modello leggero), **0,04** [0,036; 0,042] in quella del secondo ruolo (stime sue, modello medio), 0,005 nel suo duro. L'obiettivo diventa una **scala con gelo all'ora 12** (§1): i quattro pioli protetti sono nel tronco all'ora 14 nello **0,99 ↔ 0,82** dei casi (duro: 0,47).
- **Prova sull'identità:** `f12-integrazione/06-identita/IDENTITA_SU_PROFONDITA.md` consegnata (letti §0–§2); **controprova sull'identità non ancora consegnata** (`ls` alle 18:28: in `07-controprova-identita/` c'è il codice, non `CONTROPROVA_IDENTITA.md`). La «stessa identità al ritorno» resta **smentita su profondità realistica e in correzione** (VD, H-404); la correzione sui gruppi è «preliminare, senza controprova».
- **Mie previsioni (7): 3 smentite, 1 smentita di poco, 2 reggono, 1 non risolta** (`PREVISIONI.md`). Ero troppo prudente sui pioli protetti (previsto 0,55–0,85 e 0,25–0,60; usciti 0,99 e 0,82) e sbagliavo il compito critico (è la corsa finale del tabellone, 0,97, non la fila di P2).
- **Scelto dopo aver visto i numeri (due ridisegni, dichiarati):** dopo il primo lancio ho passato il controllo all'avvio (A5) da P1 a P5 e la riga THÖR (THL) da P4 a P1; dopo il secondo ho diviso il disegno (C2) in C2a e C2b. Le stime dei compiti non sono state toccate.
- **Regole e scostamenti.** **Lunghezza: circa 4 800 parole, in gran parte tabelle: stimo sei pagine, una oltre il limite di cinque** (non impaginato: conto delle pagine non verificato). `variante_c2.py` gira senza `-I` (importa il modulo accanto). Il modello «medio» e «duro» è una mia riscrittura delle ipotesi dichiarate dal secondo ruolo, non il suo programma; controllo: con le sue stime e il suo medio ritrovo la sua scala all'ora 14 entro 0,01 (avviso 0,94 / 0,94; identità 0,96 / 0,97; stati 0,56 / 0,57). I suoi due programmi, rilanciati, ridanno 0,460 e 0,262. Letti per intero: contratto d'integrazione, prima stesura, piano rifatto, VD, completezza, attacco, controllo delle prove, discordanze. Solo le teste: prova d'insieme, «libero», identità. **Non letti:** VN, V7, V8, V9, audit, f6, `SOLUZIONE_V3.md`, addendum, `STATO_PROGETTO.md`, `RIFERIMENTI.md`: ne uso ciò che riportano i file letti. Nessuna persona della squadra è stata sentita: i profili sono ipotesi. Niente git, sudo, rete. *Indipendenza:* grafo, stime «mie» e programma hanno lo stesso autore; le stime del secondo ruolo sono sue.

## 1. «Valutazione preliminare», minimo, scala

**Valutazione preliminare (chiusa all'ora 14; dicitura di VD: «provato su profondità simulata dalle schede tecniche e su tracce pubbliche di persone; mai su un sensore della squadra»).**
1. **Tabellone sul tronco gelato**, sensore simulato con verità esatta, una riga per passaggio (così gli intervalli si rifanno per camminatore), semi non usati per tarare. Righe di sicurezza: celle «libero» con un ostacolo sotto (soglia 0); nascosti fuori dall'avviso (0); avvisi caduti senza aver guardato (0). Righe di continuità: passaggi con un vuoto dopo l'ingresso in ombra (0); persona dentro la regione a 1, 2, 3 s come «k su n» con Wilson al 95 % (soglie 0,90; 0,90; 0,85, solo nel dominio: ostacolo largo 2 m, bordo noto, sul percorso, finché resta nascosta); identità al ritorno «come trovata», con risoluzione e geometria. Una riga col tempo per ciclo sulla macchina della demo. Se una soglia cade si mostra la cifra.
2. **Una riga su persone vere:** il predittore mostrato sulle tracce THÖR (cattura del moto, non una camera).
3. **Se il tronco non ha ancora le righe della regione:** la tabella della prova d'insieme (`f12-integrazione/02-prova-insieme/`, `sh rifai.sh`, 241 s) dichiarata «banco di progetto, non il prototipo»: 30 celle su 30 sopra soglia con il pannello da 2 m (limiti peggiori 0,921 fino a 2 s e 0,899 a 3 s); con quello da 1 m «a 1 s circa 9 su 10 (limite 0,87)», poi nessuna cifra.
4. **Se arriva un sensore:** le tre misure del §6. 5. **La demo** in riproduzione dichiarata, e il video di ripiego. Il prototipo osserva e avvisa soltanto: nessuna funzione d'ingaggio o di puntamento, nessuna uscita è un comando.

**Minimo dimostrabile (MD):** punti 1, 2 e 5 con tutti i sei pioli. **La scala** (ordine d'ingresso nel tronco; ciò che non è entrato resta dietro il suo interruttore, spento, e lo schermo lo nomina): ① «libero» dal solo fotogramma → ② avviso che non cade per sola identità → ③ regione disegnata per tutta l'occlusione → ④ identità corretta → ⑤ stati senza vuoti → ⑥ sensore non in salute. **Protetti (mai tagliati): ①–④, lo scheletro, il tabellone base.** **Per le 4 ore:** i pioli rimasti, nell'ordine; righe mancanti; sensore (dopo la prova della posa); `sd-1`; registro; documento.

## 2. Compiti: stime a tre punti (ore di lavoro: mie | del secondo ruolo), chi, dopo che cosa, «fatto»

Profili **ipotizzati**: P1 mappa e sicurezza; P2 previsione; P3 schermo e documento; P4 misura; P5 tronco, identità, sensori. «Fine» = mediana in ore d'orologio: lettura mia (leggero) / lettura del secondo ruolo (medio).

| Id | Compito (origine) | Mie | Sec. ruolo | Chi | Dopo | Fine | «Fatto» quando |
|---|---|---|---|---|---|---|---|
| K0 | Ambiente, 25 prove, una sequenza che scorre, formato gelato (= `fotogrammi.jsonl` di f10) | 0,5/0,75/1,5 | 0,5/1/2,5 | tutti | — | 1,0 / 1,6 | 25 su 25 su ogni macchina, con `03-infrastruttura` accanto (senza: 2 errori su 25) |
| A1 | Rilettura di mappa, geometria, gruppi | 0,5/1/2 | uguale | P1 | K0 | 2,3 / 3,3 | cambia una soglia e rifà le prove |
| A2 | **①** «Libero»: metà impronta, una cella di guardia, margine con la distanza (`nuvole-1`, `03-libero/libero.py`, PR4); via la memoria di 3 fotogrammi (`mappa.py:119`) | 1/2/3,5 | 1/2/4 | P1 | A1 | 4,7 / 6,2 | 0 celle libere sotto un ostacolo sulle 300 condizioni del banco; dominio ±0,5° scritto sullo schermo |
| F9 | **②** L'avviso sopravvive al riaggancio finché le celle non sono viste libere (F-409, `strato_resta` nel diff di `06-identita`); c1 non entra | 1/1,5/3 | 1/2/4 | P1 | A2 | 6,7 / 9,0 | con l'estraneo, 0 avvisi caduti senza aver visto; scritta «un soggetto per ombra»; costo dichiarato (dietro un pannello fermo non si spegne: 140 su 140) |
| A3r | **⑥** Sensore non in salute come stato del sistema; al ritorno «∩ non visto libero» | 0,9/1,5/3 | 1/1,5/3 | P1 | F9 | 8,7 / 11,3 | su `azzeramento_progressivo` nessun «libero»; le tracce continuano in previsione |
| THL | Riga THÖR del predittore mostrato (`20-validazione/banco_thor.py`) | 0,5/1/2 | uguale | P1 | A3r, B2 | 10,1 / 13,7 | k su n a 1, 2, 3 s su 219 tratti |
| B1 | Rilettura: di `comp.c` solo `step_sd` (79 caratteri per riga); il Python lo legge P5 | 1/1,5/3 | 1/2/4 | P2 | K0 | 3,0 / 4,7 | elenco scritto dei punti d'innesto |
| B2 | **③** `sd-0` dietro `fabbrica_predittore` (`catena.py:33`): insieme di celle, pavimento | 1,5/2/4 | 1,5/3/6 | P2 | B1 | 5,8 / 9,3 | la regione esce a ogni ciclo nel file per fotogramma |
| B3p | **⑤** Stati e chiusure: (2) e (4) non chiudono la traccia; c2 solo con un soggetto per ombra | 1/1,5/3 | 1/2/4 | P2 | B2 | 7,9 / 12,2 | 0 passaggi con un vuoto su 30 di fumo |
| C1 | Lettore e schermo: quattro stati, tracce, età | 2/3/6 | uguale | P3 | K0 | 5,0 / 6,1 | una sequenza scorre a 15 Hz |
| SK | **Scheletro**: catena com'è → file → schermo → tabellone | 0,25/0,5/1,5 | uguale | P3 (+P5) | C1, E2 | 5,9 / 7,3 | un comando, di punta a punta |
| C2a | **③** Regione tratteggiata con l'età; contorno pieno solo con misura | 0,75/1/2 | 0,75/1,25/2,25 | P3 | SK | 7,3 / 9,0 | osservato e dedotto distinti a colpo d'occhio |
| C2b | Una sola dicitura («suolo visto libero da 1,3 m a d m», d ≤ 2,6 m), contatore, pioli spenti nominati, origine della sequenza | 1,25/1,5/3 | 1,25/1,75/3,25 | P3 | C2a | 9,4 / 11,6 | nessuna scritta che V3 non produce |
| C3a | **⑥** «Affidabilità persa» a schermo e un suono | 0,5/1/2 | uguale | P3 | C2b | 10,7 / 13,1 | scatta su `azzeramento_progressivo` |
| D1 | Rilettura di simulatore e misure; semi tenuti da parte | 1/1,5/3 | uguale | P4 | K0 | 3,0 / 4,1 | elenco di sequenze e semi |
| E1 | Inventario e istruzioni di registrazione con le tre misure di VD §6 | 0,25/0,5/1 | uguale | P4 | D1 | 3,7 / 4,9 | spedito entro l'ora 5 |
| D2a | Tabellone base sulla catena com'è (`misura_passaggi.py`, `misura_libero.py`) | 1,5/2,5/4,5 | 1,5/2,5/5 | P4 | E1 | 6,8 / 8,9 | stampa le cifre di oggi (0 su 90; 79 su 90; regione 36 su 46) |
| D2b | Righe della regione, una riga per passaggio; scritte prima contro `regione_prevista`, poi su `sd-0` | 1,5/2/4 | 1,5/2,5/5 | P4 | D2a (B2) | 10,0 / 14,4 | il tabellone gira da solo sul tronco |
| E2 | Banco di regressione dai due `rifai.sh` di f10, più 6 sequenze di fumo | 0,5/1/2,5 | uguale | P5 | K0 | 2,5 / 3,5 | un comando, meno di 2 minuti |
| F4 | **④** Identità: correzione **sui gruppi** dal diff di `06-identita` (7 file), più F-402 e F-408; marca «tagliato»; «mobile» a 5·σ·√(2/m), m = 3 | 0,5/1/2,5 | 1,5/3/6 | P5 | E2 | 4,0 / 8,5 | due cancelli a ogni fusione: 0 celle libere nell'ombra vera; scatola a 2 m almeno 9 su 10; continuità almeno 28 su 30 nel dominio |
| B3q | **⑤** Ingresso in ombra (M1, c4); c7 dietro interruttore | 1/1,5/3 | 1/2/4 | P5 | F4 | 6,0 / 11,3 | c7 acceso solo se il pavimento vuoto dà 0 tracce confermate in 30 s |
| A5 | **⑥** Controllo all'avvio: configurazione, filtri spenti, **prova della posa** (10 cm a 2,5 m esce «occupato») | 0,5/1/2 | (mia) | P5 | B3q | 7,3 / 12,8 | con +1° d'errore il sistema non parte |
| PI | Prima corsa di tutto insieme sul tronco gelato | 0,5/1/2 | 0,25/0,75/2 | P2+P5 | tutto | 11,9 / 16,8 | regressione verde con le regole accese |
| TAB | Corsa finale del tabellone, tabella firmata | 0,5/1/2 | 0,25/0,5/1,5 | P4 | PI, D2b, THL | 13,7 / 18,5 | n e intervalli, con la versione |
| PG | Prova generale registrata (video di ripiego) | 0,75 | 0,75 | tutti | — | **13:15–14:00, a tempo chiuso** | la demo scorre due volte |

Fuori dal minimo: `sd-1` (B4, 3/4/7), registro degli eventi (E3, 2/3/5), sequenze pubbliche descrittive, misure sul sensore (E4, 1,5/2,5/5). **Dove le stime non coincidono (K0, A2, F9, B1, B2, B3, D2, F4, PI, TAB) le tengo tutte e due. Per il calendario uso quelle del secondo ruolo con il suo modello medio:** le ha misurate sul posto (`comp.c`: 50 kB in 635 righe), le mie previsioni della prima stesura sono cadute 4 su 9 dal lato ottimista, e un calendario prudente con cancelli fissi non perde niente se va meglio. Solo per F4 la mia (0,5/1/2,5) vale **se la controprova regge**; finché manca vale la sua (1,5/3/6).

## 3. Calendario 5 × 18 (ogni riga è l'ora che finisce a quel numero; lettura prudente; i cancelli in grassetto non si spostano)

| Ora | P1 sicurezza | P2 previsione | P3 schermo | P4 misura | P5 tronco e identità |
|---|---|---|---|---|---|
| 1 | K0 | K0 | K0 | K0 | K0 |
| 2 | K0 → A1 | K0 → B1 | K0 → C1; macchina della demo provata | K0 → D1 | K0 → E2 |
| 3 | A1 | B1 | C1 | D1 | E2 |
| 4 | A1 → A2 | B1 | C1 | D1 | E2 → F4 |
| 5 | A2 | B1 → B2 | C1 | E1: **inventario spedito** → D2a | F4 |
| 6 | A2 | B2 | C1 | D2a | F4; **ramo del sensore deciso** (§6) |
| 7 | A2 → F9 | B2 | C1 → SK | D2a | F4 (aiuta SK) |
| 8 | F9 | B2 | **scheletro di punta a punta** → C2a | D2a | F4 |
| 9 | F9 | B2 | C2a | D2a → **primo tabellone base** | F4 → B3q |
| 10 | F9 → A3r | B2 → B3p | C2b | D2b | B3q |
| 11 | A3r | B3p | C2b | D2b | B3q |
| 12 | A3r → **GELO** | B3p → **GELO** | scaletta con i pioli mancanti | tabellone sul tronco gelato | regressione → **GELO** |
| 13 | difetti bloccanti; THL | difetti bloccanti | C3a, diapositive | **TAB 12:00–13:15** | tempo per ciclo; A5 |
| 14 | **PG 13:15–14:00** | PG | PG | PG | PG |
| 15 | pioli rimasti, nell'ordine ①–⑥ | B3p, poi `sd-1` | C3a, registro se resta tempo | D2b, righe rimaste | A5, poi sensore |
| 16 | come sopra → **GELO FINALE** | idem | idem | idem | idem |
| 17 | regressione, difetti bloccanti | regressione | documento | tabellone finale | video |
| 18 | **PG 2 alle 17:15; consegna** | idem | idem | idem | idem |

Nella mia lettura tutto arriva 1–5 ore prima (colonna «Fine»): chi finisce prende il primo piolo non chiuso, nell'ordine ①–⑥, in coppia. Pause sfalsate, mai P2 e P5 insieme dopo l'ora 6.

## 4. Percorso critico in ore d'orologio (mediane; quota di estrazioni in cui il compito decide la fine)

- **Lettura mia:** K0 0–1,0 → C1 –5,0 → SK –5,9 → C2a –7,3 → C2b –9,4 → PI 10,6–11,9 → TAB 12,4–13,7 → PG –14,5. Quote: TAB 0,97; PI 0,58; schermo 0,36; fila di P1 0,27; tabellone 0,19; P2 0,11; P5 0,07.
- **Lettura del secondo ruolo:** K0 0–1,6 → E2 –3,5 → F4 –8,5 → B3q –11,3 → A5 –12,8 (accanto B1 –4,7 → B2 –9,3 → B3p –12,2) → PI 15,2–16,8 → TAB 17,3–18,5 → PG –19,6. Quote: TAB 0,98; PI 0,65; P5 0,31; P2 0,20–0,26; D2b 0,19; P1 0,16; schermo 0,14.
- **Lettura comune:** decide la coda (prima corsa insieme e tabellone), non un compito di sviluppo; per questo il tabellone gira sul tronco dall'ora 9 e la prova generale parte alle 13:15 comunque. La lettura prudente chiude il minimo intero oltre l'ora 18 (mediana 19,6): **all'ora 18 si consegna la scala, non il minimo.**

## 5. Punti di controllo: regola scritta prima

**Ordine dei tagli:** 1 etichetta «persona» (non si comincia); 2 zone; 3 profilo sonoro (resta un suono); 4 `sd-1`; 5 registro; 6 tabella delle regole estesa; 7 sequenze pubbliche descrittive (resta THL); 8 latenza → una riga di TAB; 9 C2b ridotto alle sole scritte; 10 B3p e B3q dietro interruttore, nominati spenti; 11 A5 solo in riproduzione (**mai** con fotogrammi di un sensore vero).

| Quando | Si guarda | Se no (probabilità: mia / secondo ruolo) |
|---|---|---|
| **minuto 60** | K0: minuto in cui la quinta macchina ha 25 prove verdi e una sequenza che scorre. **È la misura che sceglie la lettura** | entro 60 min: vale la mia; 60–90: quella del secondo ruolo; oltre 90: tagli 4–8 subito |
| fine di B1 | attesa all'ora 2,6 / 3,75 | entro 3,2: MD 0,47–0,66 / circa 0,12. Fra 3,2 e 4,6: tagli 4–8, l'ora 14 mostra la scala. Oltre 4,6: tagli 4–10, P5 affianca P2 su B2 dopo F4 (protetti all'ora 14: 0,97 / 0,43–0,85) |
| 5 | E2 chiuso, inventario spedito, A2 avviato | P4 e P5 chiudono E2 in coppia; nessuna modifica entra senza il banco |
| 8 | scheletro di punta a punta (entro l'ora 8: 0,86 / 0,63) | P5 lascia F4 e lo chiude con P3; C2a non parte senza |
| 10 | B2: la regione esce a ogni ciclo | P5 affianca P2; taglio 10; D2b resta sul predittore che la catena ha già |
| **12** | **gelo:** entra solo ciò che passa il banco. Attesi: «libero» 1,00 / 0,99; avviso 0,99 / 0,85; regione 0,97 / 0,71; identità 1,00 / 0,89; stati 0,95 / 0,32; salute 0,61 / 0,16; tabellone base 0,98 / 0,84; righe della regione 0,63 / 0,13 | ciò che manca sta spento e nominato; righe della regione mancanti → §1, punto 3 |
| 13:15 | prova generale, comunque | la demo si fa con ciò che c'è, dichiarato |
| **16** | gelo finale: protetti 1,00 / 0,93; stati 1,00 / 0,76; salute 0,93 / 0,60; righe della regione 0,95 / 0,56 | ciò che non è nel tronco esce dalla demo e va in «limiti» |
| 17:15, 18 | prova generale 2; consegna | — |

## 6. Rami all'arrivo dei sensori (ora 5–6; tabella di `f10-dati/04-embedded/INVENTARIO_E_DECISIONE.md`)

- **A. Camera di profondità densa** (RealSense D4xx, Orbbec Gemini, OAK-D Pro; L515 o Kinect v1 solo se unica). Resta a casa: **registra e spedisce**, niente flusso dal vivo. Prima di ogni fotogramma: A5 passa davanti a B3q, filtri del costruttore spenti. Poi le tre misure di VD §6: (1) posa e pavimento vuoto, 30 s: 0 tracce confermate, 10 cm a 2,5 m «occupato»; (2) pannello sul suolo segnato col nastro, 150 fotogrammi: celle «libero» nell'ombra vera (soglia 0); (3) **30 passaggi** col metro a terra e la mano sul sensore. **30 su 30 dà un limite di 0,886: non permette «9 su 10»**; si scrive «una installazione, n = 30». Allestimento: pannello alto 1,8 m (VD) e largo 2 m (con 1 m nessuna cifra oltre 1 s), persona a 0,5 m dal pannello (a 0,3 m l'identità corretta dà 0 e 1 su 10). Lavoro di P4 e P5 fra 14 e 16. Se resta tempo: stanza ferma 60 s, e 60 s a vuoto e sotto carico; le prove con tre persone restano fuori, dichiarate.
- **A bis. Sensore in sala con un'ora libera:** due persone che camminano fanno 90–120 passaggi in un'ora (stima dello statistico, **non misurata**): bastano per «più di 8 su 10» (almeno 82 su 94, potenza 0,86), non per distinguere 0,90 da 0,85 (296 passaggi, 3–4 ore).
- **B. Solo altro.** Telefono con LiDAR: profondità registrata come dati, non demo. Webcam: video di verità. LiDAR 2D, radar, ultrasuoni: niente nelle 18 ore.
- **C. Niente.** Il piano non cambia; il punto 4 del §1 resta vuoto e si dichiara. Nel modello il sensore che distrae P5 pesa 0,01 sul minimo: **non decide**.

## 7. Rischi e contromisure

| Rischio | Segnale | Contromisura |
|---|---|---|
| Sottostima comune (ore utili 0,80 invece di 0,88: MD da 0,43 a 0,25) | minuto 60, fine di B1 | la scala: l'ora 14 non dipende dalla chiusura del minimo |
| La controprova sull'identità cade | il suo file, o i due cancelli di F4 | F4 resta spento; lo schermo dice «identità in correzione»; ② non dipende dall'identità |
| La correzione dell'identità tocca il «libero» (98 e 91 celle·fotogramma con la soglia per cella) | cancello «0 celle libere nell'ombra vera» | solo la forma sui gruppi; mai la soglia per cella |
| c7 su profondità realistica accende avvisi che niente spegne (mediana 20 per sequenza di 3 s) | pavimento vuoto, 30 s | c7 spento, scoperti dichiarati (3,97 % senza, 0,10 % con) |
| Posa sbagliata di 1°: 10 cm a 2,5 m «libero» (7 celle su 7); il conto dà il limite a 0,69° (2,5 m · tan e < 0,03 m: rifatto da me) | prova d'ingresso | A5 prima di ogni fotogramma vero; tolleranza 0,5° |
| La prima corsa insieme è lenta (1/2/4 invece di 0,5/1/2: MD da 0,43 a 0,28) | PI non chiusa alle 12:30 | scheletro dall'ora 8, fusioni piccole, TAB sulla versione gelata |
| La regione o le sue cifre mancano al gelo (0,71 e 0,13 nella lettura prudente) | ora 10, ora 12 | C2a prima di C2b; D2b sul predittore esistente; tabella del banco di progetto |
| Una persona manca (4 persone, mie stime, leggero / medio: MD 0,09 / 0,004; protetti all'ora 14: 0,81 / 0,54) | — | tagli 4–10 dall'ora 0; F4 a P1, E2 a P3 |
| Una frase «da non dire» in demo | prova generale | elenco di VD §5 accanto alla scaletta, più: «la previsione non tocca l'avviso»; «99,25 %» (è 99,05 % con Wilson); «regione 83 su 90» senza «soglia 40»; «6,2 ms» per la previsione in Python (rilanciata: 15,9 ms al 95° percentile); una distanza di separazione da norma (non letta) |

## 8. La prima ora, minuto per minuto

| Minuti | Chi | Che cosa apre, rilegge, lancia |
|---|---|---|
| 0–10 | tutti | il §1 e il §5 di questa pagina a voce alta; P5 distribuisce `S/f10-dati/` (ambiente, catena, 1,8 GB di sequenze) |
| 10–35 | tutti | `sh S/f10-dati/03-infrastruttura/crea_ambiente.sh`; da `S/f10-dati/`: `ambiente/venv/bin/python -I -B 10-catena/prove.py` → 25 su 25 (6 s). Ognuno segna il minuto |
| 35–45 | tutti | `ambiente/venv/bin/python -I -B 10-catena/esegui.py <sequenza> <uscita>` su `d435i_nom__pannello_a12__s00`; il `fotogrammi.jsonl` che esce **è** il formato (`03-infrastruttura/formato_sequenza.md`) |
| 45–60 | P1 | apre `f10-dati/10-catena/mappa.py` (riga 119) e `parametri.py` (29–32); rilegge `f12-integrazione/03-libero/LIBERO_DELLA_CELLA.md` §0 e `libero.py` (160 righe, PR4 alla 127); lancia su una copia `sh rifai.sh` (2 min) |
| 45–60 | P2 | apre `f8-continuita/13-soluzione/comp.c`, solo `step_sd`, e `f10-dati/10-catena/catena.py` riga 33; rilegge `MODIFICHE_CONTINUITA.md` (M3); compila `comp.c` con `taratura.txt` accanto |
| 45–60 | P3 | apre `f12-integrazione/05-schermo/SCHERMO_E_DEMO.md` (e `22-schermo-finale/`, se consegnato) e il `fotogrammi.jsonl`; rilegge `11-completezza/COMPLETEZZA.md` §3; stampa a video i quattro stati di un fotogramma; collega la macchina della demo |
| 45–60 | P4 | apre `f10-dati/20-validazione/misura_passaggi.py` e `misura_libero.py`; rilegge VD §4 e §6 e `13-statistica/CONTROLLO_PROVE.md` §5; lancia su una copia `sh 20-validazione/rifai.sh` (durata **non verificata**); al minuto 50 manda la domanda sull'inventario (c'è un iPhone Pro o un iPad Pro? un pannello 1,8 × 2 m?) |
| 45–60 | P5 | apre `f12-integrazione/06-identita/DIFFERENZE.diff` (261 righe) e `DIFFERENZE.md`; rilegge `IDENTITA_SU_PROFONDITA.md` §0 e §5 e la controprova, se c'è; lancia su una copia `sh f10-dati/22-avversario/rifai.sh` e ne fa il primo comando del banco |
| 60 | tutti | due minuti: il minuto di K0 di ciascuno → regola del §5 |

## 9. Simulazione delle durate: programma e risultati accanto

`piano_finale_mc.py` e `variante_c2.py`: grafo del §2; triangolari sulle stime; fattore di squadra e di persona lognormali; ore d'orologio = lavoro / ore utili; 20 000 estrazioni, Wilson al 95 % entro ± 0,007, tre semi (0,421–0,428; 0,037–0,039). *Leggero* (prima stesura): σ 0,12 e 0,20, ore utili 0,78–0,88–0,96. *Medio* e *duro*: le ipotesi del secondo ruolo (ore utili 0,70–0,80–0,90 e 0,62–0,74–0,85; rilettura che non passa nel 20 e 30 %; persona ferma 2 h con probabilità 0,3 e 0,5; attrito; stanchezza dopo l'ora 10; macchina della demo lenta). Non modellati: scambi di compiti, guasti.

| Stime, modello | P(MD entro l'ora 14) | entro l'ora 16 | Mediana / 80° perc. della fine | Protetti ①–④ nel tronco alle ore 12 / 14 / 16 |
|---|---|---|---|---|
| **Mie, leggero** | **0,428** [0,421; 0,435] | 0,71 | 14,5 / 16,9 h | 0,96 / **0,99** / 1,00 |
| Mie, medio | 0,108 | 0,31 | 17,6 / 20,6 h | 0,85 / 0,95 / 0,99 |
| Mie, duro | 0,016 | 0,06 | 22,5 / 27,5 h | 0,54 / 0,73 / 0,86 |
| Secondo ruolo, leggero | 0,214 | 0,48 | 16,1 / 18,9 h | 0,84 / 0,95 / 0,99 |
| **Secondo ruolo, medio** | **0,039** [0,036; 0,042] | 0,15 | 19,6 / 23,1 h | 0,59 / **0,82** / 0,93 |
| Secondo ruolo, duro | 0,005 | 0,03 | 25,1 / 30,9 h | 0,26 / 0,47 / 0,66 |

**Accanto, le cifre del secondo ruolo** (`12-piano-rifatto`, suo programma, suo calendario senza cancello): 0,262 / 0,056 / 0,007; sulla prima stesura con i tagli 0,370 / 0,081 / 0,013 con le mie stime d'allora e 0,055 / 0,007 / 0,001 con le sue. **La prima stesura dava 0,46** con i tagli e 0,29 intera. **Una ipotesi alla volta** (mie, leggero; lancio 2, prima di dividere C2, base 0,424): ore utili del medio 0,25; prima corsa insieme lenta 0,28; F4 a 1,5/3/6 0,34; attrito 0,34; rilettura 0,35; B1 e B2 del secondo ruolo 0,35; persona ferma 0,38; sensore 0,41. K0 preparato prima: 0,51 (mia), 0,073 (secondo ruolo, dove i protetti al gelo passano da 0,59 a 0,75).

**Probabilità di chiusura, con l'intervallo fra le due letture.** Minimo intero entro l'ora 14: **da 0,04 a 0,43** (0,005 nel duro). Pioli protetti nel tronco: al gelo dell'ora 12 **da 0,59 a 0,96**; all'ora 14 **da 0,82 a 0,99**; al gelo finale **da 0,93 a 1,00** (duro: 0,26 / 0,47 / 0,66). Nessuna media: la lettura la sceglie il minuto 60.

## 10. Decisioni dell'utente (tre), con la raccomandazione

1. **L'avviso che sopravvive al riaggancio (F9), o togliere «finisce solo guardando» dal testo e dallo schermo.** Raccomando F9: è la priorità 2, e con c1 l'estraneo fa cadere l'avviso nel 0,91–0,99 dei casi. Costo da accettare: dietro un pannello fermo l'avviso non si spegne più.
2. **Che cosa si promette all'ora 14: la scala col gelo all'ora 12, non «il minimo chiuso»;** l'identità come «in correzione, in un dominio stretto», mai come cifra. Raccomando la scala.
3. **K0 prima dell'ora 0** (ambiente sulle cinque macchine, `f10-dati` copiata, lettura della versione 3), se il regolamento lo ammette (**non verificato**), e la domanda su telefono e pannello subito. Raccomando sì: +0,03…+0,08 sul minimo, +0,16 sui protetti al gelo nella lettura prudente.

## 11. Stati proposti, e che cosa è cambiato rispetto alla prima stesura

**Stati.** «MD entro l'ora 14»: **non provato** (0,04–0,43, stime). «Pioli protetti nel tronco all'ora 14»: **sostenuto solo da una simulazione di stime** (0,82–0,99), calendario scelto dopo. «Con 4 persone non ci sta»: sostenuto (0,09 / 0,004). «Riuso con un'ora di rilettura»: sostenuto per la mappa, smentito per `comp.c`, non verificato per l'ambiente su altre macchine (misure del secondo ruolo). K-108 resta aperta: la decide il minuto 60. **Dopo l'hackathon (una riga):** provare la soglia proporzionale sui gruppi fuori dalla geometria del catalogo.

**Che cosa è cambiato.** (1) Obiettivo: da «minimo chiuso» (0,46) a scala con gelo all'ora 12 e pioli nominati. (2) Entra VD: l'identità (F4, F-401/402/408 sui gruppi) e l'avviso che resta (F9, F-409) sono sul percorso protetto; A4* sparisce. (3) B3b, che aveva un criterio irraggiungibile (estraneo con c1), è sostituito da F9; B3a è diviso fra P2 e P5. (4) «Libero»: non più «un pixel dell'impronta» ma `nuvole-1`; posa a 0,5° con la prova d'ingresso (A5, compito che mancava). (5) Scheletro di punta a punta entro l'ora 8 e tabellone base entro l'ora 9, prima delle modifiche; D2 diviso; C2 diviso, con la regione prima. (6) La riga THÖR torna nel minimo; la latenza diventa una riga del tabellone. (7) Prova generale alle 13:15 a tempo chiuso (la mediana della prima stesura mancava l'ora 14 di un quarto d'ora). (8) Sensore: tre misure di VD, n dichiarato (30 non dice «9 su 10»; 94 dicono «più di 8 su 10»), pannello 1,8 × 2 m. (9) Due letture delle stime, tenute distinte, e una misura al minuto 60 che sceglie. (10) Una sola scaletta e una riga per passaggio nel tabellone; frasi da non dire aggiornate con VD e con le discordanze dei fascicoli.
