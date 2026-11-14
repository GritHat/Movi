# Torneo, parte 3 — la regione «prevista» (H-009, H-014, H-015, H-016; K-001, K-002, K-005) · `sciame-avversario`

**In testa.** Nessuna idea smentita in via definitiva: propongo **RIFORMULARE per tutte e quattro**, con le correzioni scritte sotto. **Scostamenti:** (1) la previsione P3-9 è stata aggiunta dopo aver visto il primo confronto (è scritto nel file); (2) tre risultati sono «notati dopo», non registrati prima: li marco **[dopo]**; (3) dopo la prima esecuzione ho corretto un'etichetta e aggiunto una misura (massa gaussiana) con un generatore separato: i numeri già visti non sono cambiati (`diff` vuoto sul rifacimento). Non ho aperto gli script degli autori.
**Che cosa condivide ogni controllo con le idee:** il testo delle schede e il modello linguistico. NON il prototipo degli autori: scena, codice e parametri sono miei. È tutto **simulato**: pedone puntiforme (niente corpo largo 40 cm), tratti a velocità costante, rumore isotropo di 5 cm, Pd 0,9, nessun falso allarme, sensore fermo. Sono scelte mie, non degli autori: tassi del modo «sosta» (0,25/s e 0,4/s), esistenza iniziale 0,99 e morte sotto 0,05, cancello «≥ 1 % della massa entro 0,5 m», 250 particelle, regione al 95 % su celle di 0,5 m, q = 0,2. Per questo le smentite valgono come RIFORMULARE, non come verdetto sull'idea.
**Scena.** Sensore in (0,0), campo ±43,5°, portata 6 m; pannello a 2 m, largo 1 m (ombra 7,8 m²) o 2 m (14,7 m²); pedone a 4 m, 1,0–1,5 m/s, 15 Hz. **Attenzione [dopo]:** a 4 m l'ombra del pannello da 1 m è larga **2 m** (non 1 m come nel conto del triage) e il transito normale dura in media **1,70 s**. 100 prove per comportamento; misure solo a soggetto ancora non visibile.

## 1. Le tre regioni sulla stessa scena (sosta 2–4 s; pannello 1 m, fra parentesi 2 m)

Per cella: contiene il vero % · quota in celle viste libere % · quota dell'ombra coperta %.

| Regione | 0,5 s | 1 s | 2 s | 3 s | Traccia chiusa a soggetto nascosto |
|---|---|---|---|---|---|
| (a) cerchio al 95 % del Kalman | 93 · 0,2 · 9 | 88 · 10 · 31 (92 · 0,2 · 18) | 84 · 51 · 62 (94 · 17 · 81) | 88 · 23 · 80 (97 · 18 · 92) | mai: dilaga (raggio 3,8 m a 3 s; massa gaussiana in libere 64 % a 2 s, 37 % a 3 s) |
| (a) + raggio di H-014 | PREVISTO 100 % | PREVISTO 97 % | nessuna regione | nessuna regione | M = 3: 0 %, scade a SCONOSCIUTO a 1,12 s nel 100 %; M = 1: chiusa nel 10–26 % all'ingresso |
| (b) disco ∩ non osservato | 100 · 0 · 45 (24) | 100 · 0 · **98** (60) | 100 · 0 · 100 | 100 · 0 · 100 | mai; «sconosciuto» a 1 s (2 m: a 2 s) |
| (c) particelle senza «sosta» | 93 · 0 · 14 | 85 · 0,4 · 32 | 79 · 0,9 · 55 (81) | 83 · 0,4 · 70 (**64**) | 0 % (esistenza media 0,83) |
| (c) particelle con «sosta» | 95 · 0 · 15 | 96 · 0,3 · 35 (21) | 100 · 0,4 · 52 (62) | 100 · 0,2 · 60 (98 · 0,2 · 68) | 0 % (0,92) |

Altri comportamenti, contenimento a 3 s (1 m / 2 m): **esce dal lato lontano** [dopo]: cerchio 55 / 69, disco 100 / 100, particelle senza sosta 47 / 55, **con sosta 22 / 41** (solo lo 0,2 % della massa in celle viste libere: la regione è sicura di sé e sbagliata). Torna indietro, a 2 s (1 m, n = 26): cerchio 65, senza sosta 35, con sosta 96, disco 100. Prosegue: tutte 100 % a 1 s.
**Identità alla prima ri-rilevazione** (cancello geometrico): prosegue, 1 m (1,70 s): H-014 **0 %**, Kalman con r_max 1,5 m 30 %, disco e particelle 100 %; sosta, 1 m (4,7 s): H-014 0 %, senza sosta 71 %, con sosta 100 %; sosta, 2 m (6,3 s): senza sosta 28 %, con sosta 76 %.

## 2. Attacchi

| H# | Attacco | Previsione (scritta prima) | Esito con i numeri | Conseguenza |
|---|---|---|---|---|
| H-014 | Sosta: chiusa mentre è nascosto (K-001) | a 4 m < 20 %; a 3 m > 50 % | 4 m: M = 3 0 %, M = 1 20,3 % (n = 300; punto previsto 0–5 cm fuori dall'ombra all'ingresso). 3 m: 56 % / 14 %. 2,5 m: 86 % / 53 %. **Mista** | RIFORMULARE: «chiusa» solo dopo ≥ 3 fotogrammi e fuori da una fascia di guardia attorno al bordo dell'ombra |
| H-014 | Ombra stimata più stretta di 20 cm | M = 1 ≥ 90 %; M = 3 < 30 % | M = 1 **100 %** chiusa all'ingresso; M = 3 **45–50 %** (peggio del previsto: mia previsione smentita) | come sopra: la fascia di guardia deve superare l'errore dell'ombra (più mezzo corpo: non verificato) |
| H-014 | Transito normale contro scadenza a 1 m [dopo] | — | scade a 1,12 s; chi prosegue riemerge a 1,70 s: PREVISTO ancora vivo **0 %** | RIFORMULARE: legare la scadenza all'ombra (o dichiarare che il ritorno è solo per aspetto) |
| H-009 | A 1 s il disco copre l'ombra? | ≥ 50 % (1 m) | **97,8 %** (1 m), 59,8 % (2 m); a 0,5 s 44,5 % / 23,6 %. **Regge la previsione**: «previsto» informa per circa 0,5 s | RIFORMULARE: il disco è la garanzia (R6, R8), non l'informazione (R3, R5) |
| H-009 | Bersaglio più veloce di v_max | ≥ 95 % fino a 2,4; ≤ 20 % da 3,0 | contenimento a 0,5 s: 100 / **90** / 10 / 0 / 0 % a 2,0 / 2,4 / 2,6 / 3,0 / 3,5 m/s; identità a 3,0: 0 %. Regge (a 2,4 manca il margine di rumore) | RIFORMULARE: v_max dichiarata per scenario, più k·σ di margine. Fuori dal disco resta «non osservato», mai libero: R8 tiene |
| H-009 | Ombra sbagliata di ±20 cm | contenimento ≥ 90 % | −20 cm: contiene 83–92 % nella sosta; +20 cm [dopo]: 14,4 % della regione in celle davvero viste libere a 0,5 s | lo «0 % per costruzione» vale solo con l'ombra esatta: fascia di guardia |
| H-015 | Senza modo «sosta» | identità < 80 % | **71 %** (1 m), **28 %** (2 m); con sosta 100 % e 76 %. Regge: il falsificatore del triage scatta | RIFORMULARE: il modo «sosta» è parte dell'enunciato, non un dettaglio; con 2 m non basta (76 %) |
| H-015 | Ombra più stretta di 20 cm | r < 0,5 in ≥ 30 %; identità < 85 % | esistenza < 0,5 entro 6 fotogrammi nel 50–59 %; morta a 3 s nel 23 % (con sosta) e 55 % (senza); identità 68 %. Con +20 cm (cioè una fascia di guardia): 100 %, al prezzo dell'11–14 % della massa su celle libere. Regge | RIFORMULARE: evidenza negativa solo oltre la fascia di guardia |
| H-015, H-016 | Uscita dal lato lontano [dopo] e 1000 particelle (P3-9) | con 1000 resta < 50 % | 22 % → 29 % (1 m): è un errore di modello, non di campionamento. Regge | la regione delle particelle va presentata come «probabile», sopra «tutta l'ombra è possibile presenza» |
| H-016 | Falso «libero» per k fotogrammi | < 5 % a k = 4 / 5 / 7; all'uscita ≤ 3 | campo aperto: massa giusta < 5 % a **k = 4 / 5 / 7** (Pd 0,9 / 0,8 / 0,7), cioè 0,27–0,47 s. All'uscita dall'ombra: < 5 % a **k = 5** (parte dal 17 %); P(in ombra) 0,95–0,99 con il soggetto in vista; riaggancio dopo k = 3: 99–100 %, dopo k = 5: **59–72 %**. H-014: chiusa al 1º o 3º fotogramma; disco: esclude il vero dal 1º. Regge | RIFORMULARE: evidenza negativa solo dove la profondità è valida e vede lo sfondo; un buco è «nessun dato». Nessuna famiglia regge un falso libero di 0,3 s |
| tutte | Due bersagli insieme, da lati opposti | tornano: Kalman ≥ 80 % di scambi | tornano: Kalman **74 % / 61 %** di scambi, di cui **44 % / 10 % senza segnale d'ambiguità**; particelle 48 % / 10 %. Proseguono: Kalman 0 %; particelle 4 % (1 m) ma **79 %** (2 m: il modo sosta trattiene massa al lato d'ingresso). Disco: mai uno scambio (ambiguo 60–100 %, altrimenti giusto). **Mista** | nessuna geometria dà l'identità: va dichiarata «ambigua» quando la misura cade in due regioni |

## 3. Le contraddizioni

- **K-001 — sì, ma non nella geometria nominale.** Con la regola alla lettera (un fotogramma) la traccia è chiusa a persona nascosta nel 10–26 % dei casi già all'ingresso; con tre fotogrammi 0 % a 4 m (scade prima, a 1,12 s), 14 % a 3 m, 53 % a 2,5 m, 45–50 % se l'ombra è sbagliata di 20 cm. Le particelle non chiudono mai con l'ombra esatta; con −20 cm muoiono nel 23–55 %. Resta aperta sul vero: serve un pannello reale con il corpo largo (prova: 20 soste registrate, contare le chiusure).
- **K-002.** A 3 s di sosta contengono il soggetto senza toccare celle libere il **disco** (100 %, 0 %) e le **particelle con sosta** (98–100 %, 0,2 %); il cerchio no (23 % dell'area e 37 % della massa in libere; 51 % e 64 % a 2 s). A 1 s coprono meno di metà dell'ombra il **cerchio** (31 % / 18 %) e le **particelle** (35 % / 21 %); il disco no (98 % / 60 %). Nessuna famiglia vince sulle due domande in tutti i comportamenti: le particelle perdono chi esce dal lato lontano (22–41 %).
- **K-005.** Con le regole dell'ellisse sulla sosta la traccia scade (H-014 a 1,12 s; r_max 1,5 m: 0 % di identità): si mostra R6. L'identità tenuta (R3) si ottiene solo con particelle, modo «sosta» e fascia di guardia: 100 % (1 m), 76 % (2 m), 68 % con ombra a −20 cm. La scelta resta dell'utente; il dato nuovo è che con il pannello da 1 m a 2 m e il pedone a 4 m anche il transito normale supera la scadenza.

## 4. Proposta `avversario-3` (da vagliare, NON provata come insieme)

Due strati sempre accesi, niente particelle nel percorso critico:
1. **Garanzia (R6, R8):** maschera d'ombra dalla profondità, dilatata di una fascia di guardia (≥ 20 cm più mezzo corpo); tutta l'ombra legata alla traccia è «possibile presenza» finché le sue celle non sono viste libere per ≥ 3 fotogrammi. Mai un timer, mai una chiusura sul solo punto. È il disco di H-009 senza il raggio che cresce.
2. **Informazione (R3, R4, R5):** cerchio del Kalman ritagliato sulle celle non osservate, mostrato come «probabile» finché copre meno di metà dell'ombra (qui fra 1 e 2 s: 31 % a 1 s, 62 % a 2 s); poi resta solo lo strato 1.
3. Ritorno: se nell'ombra pende una sola traccia la si riaggancia; se due, «identità ambigua» dichiarata.
Particelle con sosta solo se la demo vuole R3 su soste oltre 1,5 s. **Previsione:** contenimento dello strato 1 ≥ 99 % e 0 % in celle libere con errore d'ombra fino a 20 cm; strato 2 al 77–100 % a 1 s (misurato sul cerchio non ritagliato). **Smentita:** un caso con soggetto nascosto fuori dallo strato 1, o strato 1 su celle viste libere oltre la fascia.

## 5. Controesempi aperti e dove ho cercato

Cercato: 4 comportamenti × 2 pannelli, distanza 2,5–4 m, ombra ±20 cm, Pd del modello 0,7–0,9, velocità 2,0–3,5 m/s, 250 e 1000 particelle, due bersagli. **Non cercato (non verificato):** corpo esteso e occlusione parziale; sensore in moto; falsi allarmi; vetro; rumore che cresce con la distanza; tetto di 10 s di H-015; chi esce dal lato lontano lascia l'ombra «possibile presenza» senza fine. Il contenimento del disco al 100 % è per costruzione (v ≤ v_max): non è una prova.

**Rifare:** `cd <questa cartella>; timeout 120 python3 scena_parte3.py <main1|main2|ombra|k001|falso|vmax|due>` (seme base 20261114; `NP3=1000` per P3-9; il più lungo 29 s di CPU). File: `scena_parte3.py`, `PREVISIONI_parte3.md`, `risultati_{main1,main2,ombra,k001,falso,vmax,due,main1_np1000}_parte3.txt`, `stato_parte3.md`.
