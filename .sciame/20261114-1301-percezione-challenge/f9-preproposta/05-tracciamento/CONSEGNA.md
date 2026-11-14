# Consegna — `sciame-tracciamento`, f9: S11, attacco 2, parere su S3–S4

**In testa: scostamenti e regole violate.** Lavoro dalle 2026-11-14T15:38:50+01:00 alle 16:04 (`date -Is`). (1) Nella seconda tornata di previsioni ho scritto l'ora a mano invece di leggerla (15:53:40; era 15:50:36): corretto subito, annotato nel file. (2) Il primo lancio con traiettorie lisciate aveva un errore mio: file conservato (`ris_pd09_smooth6_ERRATO_…`), rifatto. (3) I bracci `cor2` (cambiato **una volta** dopo un esito) e `cor3` sono aggiunte successive, ciascuna con la previsione scritta prima del lancio (quattro tornate datate in `PREVISIONI.md`); «alla lettera» e «corretta» non sono mai stati toccati (conteggi identici al primo lancio, 20 righe su 20). (4) La misura di P1 era mal posta per la «sosta in vista» (due fronti sono legittimi). (5) Di OC-SORT ho aperto oggi la pagina arXiv (https://arxiv.org/abs/2203.14360) e il README: ORU e «traiettoria virtuale» sì; il PDF non si è aperto, quindi il passo di recupero (OCR) lo cito a memoria, **non verificato oggi**. (6) Lunghezza: circa 2550 parole contando i segni delle tabelle: al limite delle tre pagine, forse poco oltre. Nessun lancio oltre 19 s; niente git; cartelle f7, f8 e le altre di f9 non lette.

**Che cosa vale la prova.** Banco mio, `eventi_sim.py` (Python puro, seme 20261114, dieci scenari, 400 passaggi ciascuno; unità: il passaggio): sensore fermo, pannello di 1 m a 1,8 m, attore **puntiforme** a 2,3 m, 15 Hz, rumore 4 cm, Pd 0,9 (bracci: Pd 0,7; falsi al bordo 2 % per ciclo; soste lisciate), Kalman q = 0,2, porta 99 %, conferma 3 su 5, regole B5 del nucleo. Condivide con ciò che controlla la specifica, l'autore delle correzioni (io) e il modello linguistico, **non** il codice dei simulatori esistenti: i numeri della macchina corretta sono una prova d'esistenza, non una validazione. Su S3–S4 il banco è approssimato: decide f8. Rifare: `sh rifai.sh`; leggere: `python3 estrai.py ris_pd09.txt <chiave>`.

## 1. Verdetti proposti

| Oggetto | Verdetto | Prova |
|---|---|---|
| **S11**, macchina degli eventi | **Approvata con correzioni** (§3, §6). Com'è scritta **non** regge: 4 nomi su 8 affermano più di ciò che il sistema sa, mancano soglie e isteresi, un evento di scena è messo per identità | alla lettera: avvicinamento falso in 171 transiti su 400; occlusione falsa in 177; uscite false 207 su 2800; riapparizione falsa in 386 soste su 400 con falsi al bordo. Corretta (`cor3`): 0; 2; 1 su 2800; 0 |
| **Attacco 2**, regola proposta | **Respinta nella forma, approvata riscritta** (`tracciamento-5`) | la porta di Mahalanobis lascia passare lo scambio in **381 casi su 392** (97,2 %); «completa ri-osservazione dell'ombra» con ostacolo fermo e un punto di vista: **mai** (conto, §5) |
| **S3–S4**, parere | **Approvabili solo con sei precisazioni** (§5); la misura spetta a f8 | tre letture del «peso μ2» danno tre esiti incompatibili (§4, critica 4) |
| Tassi sulla camera vera | **Da provare sull'hardware**: 30 passaggi e 20 soste registrati, eventi contati a mano contro il registro; soglia scritta prima: 0 «uscita» e 0 «riapparso» a soggetto nascosto | — |

## 2. Esiti delle previsioni (21 in quattro tornate, scritte prima; tabella completa in coda a `PREVISIONI.md`)

- **Smentite:** P1 e P2 per la mia macchina «corretta» (l'isteresi sulla velocità del filtro non basta: avvicinamento mancato 60 e attraversamento falso 86 su 400; uscite false 70/2800, 68 delle quali di chi si ferma a 11–14 cm dall'anello cieco e perde la traccia); P3a e P3c con la soglia μ2 > 0,8 (evento emesso solo in 172 e 223 passaggi su 400); P3b (soste false nel transito alla lettera 180/400, attese 1–10 %); P6 come «per costruzione» (392/400); P7 per lo strato a vuoto (79/400, atteso ≤ 5 %); P9; P13.
- **Reggono:** P1 e P2 per «alla lettera» (uscite false 7,4 %; a Pd 0,7 il 23,5 %, non il 40 % atteso); P7 per la corretta; P8; P9bis, P10, P12, P14, P16, P17, P18. **Fuori intervallo, non smentite:** P4 (381/392 contro 40–80 %), P5, P11, P15 con lisciatura.

## 3. S11, evento per evento, sugli stati che il nucleo ha

Ogni evento esce con tre marche: **conoscenza** (O = osservato: c'è una misura; D = dedotto da assenza di misura, previsione o geometria), **identità** (propria, presunta, ambigua), **età** dell'ultima misura. Un evento D si scrive al condizionale e non usa mai il colore dell'osservato.

| Evento (nome proposto ← nome del file) | Definizione, soglie, isteresi | Conoscenza; quando è falso; misura |
|---|---|---|
| `INGRESSO_DAL_BORDO` ← `INGRESSO_AREA` | traccia confermata 3 su 5 con la **prima** misura entro 0,5 m dal bordo del campo o della portata. Prima misura entro 0,40 m da un'ombra: `COMPARSA_DA_OMBRA`; altrove: `COMPARSA_IN_CAMPO` (anomalia) | O la comparsa; D «è entrato da fuori». Doppio ingresso per traccia spezzata: 81/400 alla lettera, 6/400 `cor3` |
| `LINEA_ATTRAVERSATA` ← `ATTRAVERSAMENTO` | stessa identità misurata oltre 0,3 m da una parte e poi dall'altra di una linea dichiarata; nessuna velocità | O le posizioni; identità ereditata. Una sola in 395/400 transiti, 0/400 in chi torna; **217/400 false se dall'ombra esce un altro** |
| `AVVICINAMENTO` ← `AVVICINAMENTO_DIRETTO` | velocità **a finestra di 0,5 s** > 0,30 m/s, distanza minima prevista < 0,5 m, distanza che cala oltre 0,3 m/s, per 5 cicli; si spegne oltre 0,8 m o sopra −0,1 m/s per 8 cicli. Solo con misura nel ciclo, mai in «previsto» | O (derivata di misure), ritardo circa 0,8 s. `cor2`: mancati 3/400, falsi 0/400 |
| `OCCLUSIONE_IN_CORSO` | lo strato 1 parte al primo ciclo (la sicurezza non aspetta); l'**evento** dopo 3 cicli senza misura con l'ultima misura entro 0,40 m dall'ombra di un **altro** oggetto (K-018) | O la scomparsa; D «è dietro quell'ostacolo». 2/400 false; strato a vuoto 5/400 (48/400 a Pd 0,7) |
| `NON_RIEMERSO` ← `SOSTA_IN_OMBRA` | tempo senza misura > L / (v d'ingresso − 0,07) + 0,5 s, con i bordi d'uscita visti validi per tutto l'intervallo; agganciato fino alla riapparizione | **sempre D.** Testo: «non riemerso da T s: fermo dietro l'ostacolo **oppure** uscito dal lato non visibile». Emesso in 400/400 soste (mediana 2,53 s), ma anche in 400/400 uscite dal lato lontano e in 95/400 di chi cammina e torna: lì «sosta» sarebbe falso. Falso nel transito 7/400 (11/400 in `cor3`) |
| `RIAPPARSO` ← `RIAPPARIZIONE_CONFERMATA` | 3 rilevamenti su 5 entro la fascia dell'ombra d'ingresso; **solo allora** si rilascia lo strato 1. Identità: **presunta** con una pendente; **ambigua** con due o più; con zero pendenti l'evento è `COMPARSA_DA_OMBRA`, che marca ambigue a ritroso le presunte di quell'ombra | O la comparsa; identità **mai** «confermata». Secondo soggetto: identità sbagliata in 392–393 passaggi su 400 in ogni macchina. Costo: +0,13–0,27 s; 18/400 riagganci mancati con falsi al bordo |
| `USCITA_DAL_CAMPO` ← `USCITA_AREA` | traccia chiusa con l'ultima misura entro 0,5 m dal bordo e posizione estrapolata a 0,5 s fuori zona. Altrimenti `NON_PIÙ_RILEVATO`. Chi sparisce in ombra: mai «uscita», resta «perso, può aver lasciato l'area» | O fino al bordo; D «ha lasciato l'area». `cor3`: 1/2800 (57/2800 a Pd 0,7) |
| `AFFIDABILITÀ_PERSA`, `RIPRESA` | evento **di scena o di settore**, non per identità. Entra con B8 (0,13 s), esce dopo 1 s di fotogrammi validi; mentre è attivo nessun evento D nuovo e nessuna evidenza negativa; alla ripresa le identità in vista diventano presunte | O (del sensore). **Non misurato nel mio banco** |

**Eventi che mancano** («attività e oggetti»): `FERMO_IN_VISTA` con durata; `PERMANENZA_IN_ZONA` e `INGRESSO_IN_ZONA_VIETATA` (O; variante D «possibile presenza in zona» se un'ombra con traccia pendente tocca la zona); `COMPARSA_DA_OMBRA`; `NON_PIÙ_RILEVATO`; un **conteggio** a due numeri («osservati n, possibili m»); `OSTACOLO_NUOVO` e `OSTACOLO_RIMOSSO` rispetto alla mappa presa all'avvio («rimosso» solo se lì ora si vede il suolo). «Oggetto lasciato da una persona» chiede di separare persona e oggetto: fuori dall'hackathon. Solo definizioni: **non provati**.

## 4. Critiche numerate

1. **`tracciamento-c1` — la soglia sulla velocità angolare non separa.** θ̇ = v·d/r². Avvicinamento con 0,3 m di scarto fra 1,35 e 3 m: 0,017–0,23 rad/s; attraversamento a 2,3 m: 0,128–0,61 rad/s [conto mio]. Si sovrappongono: nessuna soglia va bene. Banco: `AVVICINAMENTO_DIRETTO` falso in 171 transiti su 400.
2. **`c2` — la velocità del filtro non serve da soglia.** A regime σ = 0,19 m/s per asse (q = 0,2, rumore 4 cm): chi è fermo ha in media circa 0,24 m/s stimati, sopra ogni «v di sosta» ragionevole. Serve la velocità a finestra, come la regola «mobile» del nucleo.
3. **`c3` — gli eventi ereditano i difetti dell'inseguitore.** Un rilevamento mancato vicino all'ombra lascia lo strato 1 acceso a vuoto in 79 transiti su 400, e una seconda persona prende poi quell'identità (90 passaggi su 400, notato dopo). Alla fermata in vista la traccia si spezza in 132 passaggi su 400 (65 con decelerazione di 0,4 s). Con il recupero sull'ultima osservazione: 5 e 7.
4. **`c4` — «μ2 > θ_stop» non è una definizione.** Tre letture: massa istantanea (142 soste false su 400 transiti); prodotto ciclo per ciclo sulla gaussiana non ritagliata (276 su 400, esplorativa); soglia 0,8 (sosta vera dichiarata solo in 223 su 400).
5. **`c5` — riapparizione al primo rilevamento**: con falsi al bordo, strato 1 rilasciato a soggetto nascosto in 386 soste su 400 (con la conferma 3 su 5: spento per almeno un ciclo in 5 su 400).
6. **`c6` — macchina «per ogni ID»**: lo scambio passa agli eventi a valle (217 linee false su 400); la perdita di affidabilità non è di un'identità.

## 5. Attacco 2 e parere su S3–S4

**La regola proposta rispetto al nucleo.** Il nucleo riaggancia chiunque esca accanto all'ombra d'ingresso se pende una sola traccia, e rilascia lo strato 1: se esce un altro, sbaglia sempre (qui 392 occasioni su 392; nel nucleo 2400 su 2400); le celle restano «in ombra», mai «libero» (misura del nucleo: 7198 su 7198). La regola proposta affida il conflitto alla porta χ²: (a) **non lo vede**: 381 su 392 in porta, perché dopo 1–3 s la porta è larga quanto la zona (σ = 0,26 / 0,73 / 1,34 m a 1 / 2 / 3 s [conto mio]); con l'ipotesi di sosta nella porta, questa accetta tutto (398/398, 346/346); (b) **respinge ritorni veri**: 22,6 % di chi torna indietro, 31 % della stessa persona che esce tre volte più veloce entro 2,5 m/s; (c) «una entra, due escono» lo decide il **conto**, non la cinematica: la seconda uscita non ha tracce pendenti.

**«Completa ri-osservazione dell'ombra»: mai.** Il raggio dal sensore (1,2 m) al suolo a distanza d passa sul piano del pannello a quota 1,2·(1 − 1,8/d): al più 0,48 m entro 3 m, sotto qualunque pannello ammesso [conto mio; coerente con B5: «con l'occlusore fermo: mai»]. La regola alla lettera lascia quindi una possibile presenza **permanente** dopo ogni conflitto, veri ritorni compresi.

**`tracciamento-5`, la regola riscritta.** Dopo un'occlusione l'identità non è mai «sicura»: presunta, ambigua o nuova. Il rilascio dello strato 1 chiede la riapparizione confermata 3 su 5 e il registro dell'ombra in pari (entrati tracciati = usciti). Uscita in più: `COMPARSA_DA_OMBRA` e identità precedenti ambigue. Conflitto: la possibile presenza resta con la sua età e si chiude solo per celle viste libere (occlusore tolto, altro punto di vista) o per **conferma dell'operatore**: un atto, non un timer (estende l'invariante 7: lo decide l'arbitro). Il limite resta dichiarato: uno scambio a conti pari non lo rileva nessuna regola geometrica.

**S3–S4: che cosa va precisato.**
1. **Una traccia, due ipotesi, una identità**: l'identità è della traccia; esce un solo oggetto con la sua miscela; la porta non dà evidenza d'identità (sopra).
2. **Il peso**: probabilità di primo passaggio lungo il percorso (1D), oppure particelle o griglia ritagliate; non massa istantanea né prodotto sulla gaussiana libera (`c4`). La regola a tempo equivalente: 7 falsi su 400, 400 soste su 400.
3. **L'ingresso**: il nucleo non aggiorna il filtro sul gruppo tagliato dall'ombra (C6; 0,2 m prima del bordo nel mio banco); al primo ciclo la media del transito è ancora fuori dall'ombra. «Probabilità zero su ogni cella libera» la ucciderebbe subito: serve la fascia di 0,40 m (invariante 4) e l'evidenza negativa solo a profondità valida, mai sul punto previsto (invariante 6).
4. **Due tracce nella stessa ombra**: i pesi non si aggiornano in modo indipendente (un'uscita ne spiega una sola); si congelano, e ogni uscita è «ambigua» finché il registro non torna in pari. **Non provato** qui; il torneo dava 74 % di scambi, 44 % muti.
5. **«Alla OC-SORT»**: l'articolo corregge il filtro dopo il riaggancio lungo una traiettoria virtuale (ORU, verificato); non ha geometria d'ombra né una regola d'identità all'uscita. Servono due prestiti precisi: velocità dalla traiettoria virtuale al rientro, **con covarianza allargata** (è una media: chi ha sostato esce a un'altra velocità); recupero sull'ultima osservazione in campo aperto (`cor3`). L'identità resta alla regola del nucleo.
6. **`PREVISTO ±X m | conf Z %`**: va detto di che cosa «conf» è la probabilità; non dell'identità.

## 6. Dove la preproposta ha letto male

- «INV-3», «INV-5»: il PDF v0.5 non numera invarianti; nel nucleo quelli citati sono il 7 e il 9.
- «Limite dichiarato Sez. 2.4»: il limite è l'altra persona **mai vista** che esce dalla stessa ombra; due uscite e velocità tripla sono il caso facile, e il rimedio cinematico non tocca il caso dichiarato.
- «con mantenimento ID», «confermata»: il PDF dice «con una sola persona nascosta» e «non distingue due persone che escono dalla stessa ombra».
- `USCITA_AREA`: nel nucleo «perso» è sempre «può aver lasciato l'area»; un'uscita osservata non esiste ancora.
- La fascia di 0,40 m e l'evidenza negativa «solo a profondità valida» stanno nel nucleo, non nel PDF: il lettore non poteva saperlo.

## 7. Proposte, costo, non verificato, dopo

**Proposte (identificativi provvisori).** `tracciamento-1`: la tabella del §3 con le tre marche. `-2`: nei primi 3 cicli senza misura un rilevamento in porta riprende la traccia ovunque (strato a vuoto 79 → 5 su 400). `-3`: `NON_RIEMERSO` a tempo di primo passaggio. `-4`: recupero sull'ultima osservazione (traccia spezzata 132 → 7). `-5`: identità e rilascio (§5). Previsione comune sulle registrazioni vere: nessun evento O a soggetto nascosto, nessun «riapparso» senza marca d'identità; la smentisce un solo caso.

**Costo (stime mie).** Strato degli eventi corretto, circa 150 righe: **4–5 ore** (eventi di base e registro dell'ombra 3 h; avvicinamento 1 h; prova sulle registrazioni 1 h); zone e permanenza +1,5 h; ostacolo nuovo o rimosso +2 h, facoltativo. Recupero sull'ultima osservazione e conferma della riapparizione: +1 h nel blocco B5. Si taglia il ramo dell'etichetta (B6, 4 h): la traccia nomina le «attività», non le classi. Calcolo: inseguitore più eventi 9–14 µs per ciclo in Python puro (indicativo), contro 66,7 ms.

**Non verificato.** Corpo esteso e occlusione parziale: a 2,3 m una persona di 1,75 m sporge 17 cm sopra un pannello di 1,5 m (per nasconderla serve 1,63 m [conto mio]), e non so che cosa ne fa la griglia; due tracce pendenti; falsi in campo aperto; perdita di affidabilità; eventi di zona; ogni tasso sulla camera vera; il passo OCR di OC-SORT.

**Dopo.** (1) f8 rifaccia il peso con il primo passaggio. (2) L'arbitro decida se `-2` e `-4` entrano nel nucleo: toccano B4 e B5 e riducono un costo già misurato (12,8–14,3 %). (3) Sull'hardware: 30 passaggi e 20 soste contati evento per evento.
