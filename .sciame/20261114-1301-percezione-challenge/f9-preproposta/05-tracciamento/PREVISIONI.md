# Previsioni — `sciame-tracciamento`, estensione f9 (S11, attacco 2, parere su S3–S4)

Scritte alle **2026-11-14T15:42:24+01:00** (`date -Is`), dopo aver letto contratto, addendum, preproposta, nucleo (SOLUZIONE_V2, VERDETTO, MISURE_V2_bis, TORNEO parte 3) e **prima** di scrivere il codice del generatore e di ogni lancio.

**Il banco (mio, da scrivere): `eventi_sim.py`.** Sensore fermo in (0,0), campo ±43,5°, zona 1,24–3 m; pannello largo 1 m a 1,8 m; attore puntiforme sulla linea a 2,3 m (ombra larga 1,28 m; gruppo «tagliato» entro 0,20 m dal bordo dell'ombra: conta per l'ingresso, non aggiorna il filtro); 15 Hz; rumore 4 cm; Pd 0,9 (braccio a 0,7); Kalman a velocità quasi costante q = 0,2; porta al 99 % (χ² = 9,21); conferma 3 su 5; regole del nucleo B5 (ingresso in ombra se l'ultima misura è entro 0,40 m dall'ombra dell'occlusore; in campo aperto 3 fotogrammi «non confermato» poi chiusa; riaggancio solo entro la fascia dell'ombra d'ingresso con una sola pendente). Due macchine degli eventi sopra lo stesso inseguitore: **«alla lettera»** (la preproposta §4.2 com'è scritta: soglie istantanee, `SOSTA_IN_OMBRA` al primo ciclo con μ2 > 0,5, `RIAPPARIZIONE_CONFERMATA` al primo riaggancio, `USCITA_AREA` = traccia chiusa, `INGRESSO_AREA` = ogni traccia confermata) e **«corretta»** (`tracciamento-1`: isteresi a due soglie e tempo minimo, eventi con stato di conoscenza, uscita solo al bordo del campo, riapparizione confermata 3 su 5 prima di rilasciare, comparsa da ombra distinta dall'ingresso). 400 passaggi per scenario, semi fissati. Unità: il passaggio. Che cosa condivide con ciò che controlla: la specifica (il testo del nucleo e della preproposta) e il modello linguistico; non il codice dei simulatori esistenti (non lo importo).

| # | Previsione | Misura | Regge se | Smentita se |
|---|---|---|---|---|
| P1 | Senza isteresi gli eventi cinematici lampeggiano | passaggi con più di un fronte di `ATTRAVERSAMENTO` o di `AVVICINAMENTO_DIRETTO`, scenari «sosta in vista 3 s» e «avvicinamento diretto» | alla lettera ≥ 30 %; corretta ≤ 2 % | alla lettera < 10 %, oppure corretta > 5 % |
| P2 | «Uscita = traccia chiusa» dichiara uscite false per frammentazione | passaggi con una `USCITA_AREA` emessa mentre il soggetto è dentro la zona (visibile o nascosto), tutti gli scenari, Pd 0,9 e 0,7 | alla lettera: 2–12 % a Pd 0,9 e ≥ 40 % a Pd 0,7; corretta ≤ 0,5 % a Pd 0,9 | alla lettera < 1 % a Pd 0,9, oppure corretta > 2 % |
| P3a | Chi esce dal lato lontano (resta in ombra fino a fine portata) riceve `SOSTA_IN_OMBRA` | passaggi «lato lontano» con l'evento di sosta emesso | ≥ 95 % in tutte e due le macchine (cambia solo il nome: «non riemerso, può aver lasciato l'area») | < 80 %: allora il banco è cieco su questo punto |
| P3b | Soste false nei transiti a velocità costante | transiti (0,5–1,4 m/s) con evento di sosta prima della riemersione | alla lettera 1–10 %; corretta (μ2 > 0,8 per 5 cicli) < 1 % | alla lettera > 20 % o corretta > 3 % |
| P3c | Ritardo della sosta vera | mediana fra l'ingresso in ombra e l'evento, sosta permanente | alla lettera 1,5–2,6 s; corretta 2,5–4,5 s | fuori di oltre 0,5 s dagli intervalli |
| P4 | La porta di Mahalanobis NON ferma lo scambio con un secondo soggetto mai tracciato (K-016) | il primo resta nascosto, un secondo esce dalla stessa ombra 0,5–3 s dopo l'ingresso, a 0,5–1,4 m/s: (i) regola del nucleo: riaggancio sbagliato; (ii) con la porta al 99 % sull'ipotesi di transito: quota ancora in porta (scambio muto) | (i) ≥ 99 %; (ii) 40–80 % | (ii) < 10 % (la porta basterebbe) |
| P5 | La porta respinge i ritorni legittimi precoci, e diventa vuota col tempo | stessa persona: quota di riapparizioni fuori porta, per comportamento | prosegue ≤ 2 %; sosta 2–4 s poi prosegue ≤ 5 %; torna indietro 30–90 %; velocità tripla ≥ 90 % | torna indietro < 10 %, o velocità tripla < 50 % |
| P6 | «Ne entra una, ne escono due» | (controllo per costruzione) la seconda uscita non ha tracce pendenti: alla lettera esce `INGRESSO_AREA`; corretta esce `COMPARSA_DA_OMBRA` e marca «identità ambigua» il riaggancio precedente | 100 % in tutte e due | un solo caso diverso: errore del banco |
| P7 | Occlusioni false | passaggi in cui `OCCLUSIONE_IN_CORSO` è emesso con il soggetto visibile e non tagliato; e quota ancora accesa a fine passaggio (scenario «transito dietro il pannello», Pd 0,9) | alla lettera (1 ciclo mancato) 5–40 %; corretta (3 cicli) < 3 %; residuo acceso a fine passaggio 0,3–5 % in tutte e due (lo eredita dal nucleo: là 12,8–14,3 % con altra geometria) | alla lettera < 2 %, o corretta > 6 % |
| P8 | Un rilevamento falso al bordo del pannello (2 % per ciclo mentre pende una traccia) produce riapparizioni false | sosta permanente (10 s): passaggi con una `RIAPPARIZIONE` emessa a soggetto nascosto, e con lo strato 1 rilasciato a soggetto nascosto | alla lettera ≥ 80 %; corretta (3 su 5 coerenti) ≤ 2 % | alla lettera < 40 %, o corretta > 5 % |

**Conti a mano fatti prima (non misure).** σ di posizione del filtro senza misure, da solo rumore di processo: √(q·t³/3) = 0,26 m a 1 s, 0,73 m a 2 s, 1,34 m a 3 s, 2,07 m a 4 s: la porta al 99 % (3,03 σ) a 3 s vale ±4 m lungo il moto, più dell'intera zona. Uscita a velocità tripla (3,6 m/s) da un tratto nascosto di 1,68 m: riemerge a 0,47 s, quando il transito previsto è a 0,56 m e σ ≈ 0,1 m: innovazione ≈ 1,1 m, cioè oltre 10 σ.

**Che cosa NON provo (dichiarato prima).** Corpo esteso; due soggetti visibili che si incrociano; rilevamenti falsi in campo aperto; occlusore mobile; sensore in moto; eventi di zona (permanenza, zona vietata, oggetto lasciato o rimosso): per questi do solo la definizione. Il modulo a due ipotesi di S3–S4 è approssimato: μ2 = 0,2 / (0,2 + 0,8·f), con f la massa gaussiana del transito ancora in zona non vista (quadratura fissa); non è il banco di f8.

---

## Seconda tornata — scritta alle 2026-11-14T15:50:36+01:00 (`date -Is`; nella prima stesura avevo scritto a mano 15:53:40, sbagliando: corretto subito), DOPO il primo lancio (`ris_pd09.txt`, 15:47:58) e PRIMA di modificare il codice e di ogni altro lancio

Il primo lancio ha mostrato tre cose che non avevo previsto: (a) la velocità del filtro (q = 0,2, rumore 4 cm) ha σ ≈ 0,19 m/s per asse a regime, quindi le soglie cinematiche sulla velocità del filtro sbagliano anche con l'isteresi (macchina «corretta», avvicinamento diretto: 60 mancati e 86 «attraversamento» falsi su 400); (b) la formula μ2 = 0,2 / (0,2 + 0,8·f) con la gaussiana libera non fa crollare μ1 (la massa «riattraversa» il visto e si rifugia nel non osservato): la sosta permanente è dichiarata solo in 223 passaggi su 400 in 10 s; (c) le soste e le ripartenze del mio generatore sono istantanee, e l'inseguitore perde la traccia (frammentazione in 132–146 passaggi su 400 nella «sosta in vista»). Aggiungo quindi, dichiarandoli come **aggiunte successive**:

- **braccio `cor2`** = «corretta» + (i) velocità **a finestra** per gli eventi cinematici (differenza fra due medie di 3 misure distanti circa 1 s, come la regola «mobile» del nucleo), tempi minimi 5 e 8 cicli; (ii) evento `NON_RIEMERSO` **a tempo e a evidenza negativa**: emesso quando il tempo senza misura supera L / (v_ingresso − 0,07) + 0,5 s, con L la corda del cuneo dilatato lungo la direzione d'ingresso e v_ingresso ≥ 0,3 m/s; agganciato fino alla riapparizione;
- **opzione `SMOOTH=6`**: traiettorie lisciate con media mobile di 0,4 s (soste e ripartenze non istantanee), per la sensibilità;
- contatori in più: soste «alla lettera» emesse solo dopo che il soggetto è davvero nascosto; porta divisa per velocità d'uscita nella «tripla» (entro o oltre la v_max di 2,5 m/s del nucleo); variante **ricorsiva** del peso (sopravvivenza s ← s·(1 − 0,9·(1 − f)), evento a μ2 > 0,5) solo per vedere quanto cambia: esplorativa, senza previsione.

| # | Previsione (seconda tornata) | Regge se | Smentita se |
|---|---|---|---|
| P9 | `cor2`, avvicinamento diretto | `AVVICINAMENTO_DIRETTO` mancato ≤ 3 % e `ATTRAVERSAMENTO` falso ≤ 3 % | uno dei due > 8 % |
| P10 | `cor2`, transito: `AVVICINAMENTO_DIRETTO` falso | ≤ 1 % (alla lettera era 255 eventi su 400 passaggi) | > 5 % |
| P11 | `cor2`, `NON_RIEMERSO`: falsi nel transito a velocità costante | < 1 % | > 3 % |
| P12 | `cor2`, `NON_RIEMERSO` emesso | sosta permanente ≥ 99 %, mediana del ritardo 1,8–3,5 s; lato lontano ≥ 99 %; sosta di 2–4 s poi prosegue ≥ 70 % | sosta permanente < 95 % |
| P13 | con `SMOOTH=6` la frammentazione nella «sosta in vista» scende | passaggi con traccia spezzata: da 132–146 a < 20 su 400; uscite false «alla lettera» sotto il 2 % sul totale | resta > 60 su 400 |
| P8 (ripetuta) | resta com'è scritta sopra; la provo ora con pf = 0,02 | | |

---

## Terza tornata — scritta alle 2026-11-14T15:53:35+01:00 (`date -Is`), DOPO il secondo lancio (`ris_pd09_cor2_prima_versione.txt`) e PRIMA di modificare il codice

Esito visto: P9 smentita nella prima versione di `cor2` (avvicinamento mancato in 52 passaggi su 400, «attraversamento» falso in 54): la finestra di circa 0,9 s più 5 cicli arriva tardi per chi cammina veloce, e alla fermata la direzione della velocità è rumore. Nel transito `cor2` emette `ATTRAVERSAMENTO` solo 178 volte su 400 passaggi (il tratto visibile prima del pannello dura meno della finestra). Cambio `cor2` **una sola volta** (codice precedente conservato in `eventi_sim_v2.py`):
1. finestra più corta (circa 0,5 s: medie delle misure a 0–3 e a 7–11 cicli indietro);
2. le condizioni d'accensione di `AVVICINAMENTO_DIRETTO` e `ATTRAVERSAMENTO` chiedono anche la velocità istantanea a finestra > 0,30 m/s;
3. evento nuovo, **geometrico e senza velocità**: `LINEA_ATTRAVERSATA` quando la stessa identità (anche presunta) è stata misurata oltre 0,3 m da una parte e poi oltre 0,3 m dall'altra della linea dichiarata (qui l'asse del sensore, x = 0).

| # | Previsione (terza tornata) | Regge se | Smentita se |
|---|---|---|---|
| P9bis | `cor2` rivista, avvicinamento diretto | mancato ≤ 5 %, `ATTRAVERSAMENTO` falso ≤ 5 % | uno dei due > 10 % |
| P14 | `LINEA_ATTRAVERSATA`: esattamente una nel transito; nessuna in «torna» | transito ≥ 97 % dei passaggi con una sola; «torna» falsi ≤ 1 % | transito < 90 %, o «torna» > 5 % |
| P15 | `LINEA_ATTRAVERSATA` nella «sosta in vista» (traccia spezzata alla fermata istantanea) | una sola nel 80–92 % senza lisciatura; ≥ 97 % con `SMOOTH=6` | < 70 % senza lisciatura |

---

## Quarta tornata — scritta alle 2026-11-14T15:56:15+01:00 (`date -Is`), dopo i lanci `ris_pd09.txt` (cor2 rivista) e `ris_pd09_smooth6.txt`, PRIMA di aggiungere il braccio `cor3`

Esiti visti: P9bis, P14, P15 reggono senza lisciatura (3 e 0 su 400; 395 su 400 e 0 falsi; 346 su 400). **P13 smentita**: con soste lisciate su 0,4 s la traccia si spezza ancora in 65 passaggi su 400 nella «sosta in vista» (soglia di smentita: più di 60). Scostamento: il primo lancio con `SMOOTH=6` aveva un errore mio (la media mobile fermava il soggetto prima della fine della traiettoria): file conservato come `ris_pd09_smooth6_ERRATO_coda_non_allungata.txt`, corretto e rilanciato.

Aggiungo un braccio **`cor3`** = `cor2` + **recupero sull'ultima osservazione** (il secondo passo d'associazione di OC-SORT, «observation-centric recovery», portato sul piano): una traccia confermata rimasta senza misura in porta si associa al rilevamento libero più vicino alla sua **ultima misura valida**, entro 2,5 m/s × tempo trascorso + 0,15 m; la velocità riparte dalla traiettoria virtuale fra le due misure. `cor2` resta com'è.

| # | Previsione (quarta tornata) | Regge se | Smentita se |
|---|---|---|---|
| P16 | `cor3`, «sosta in vista» senza lisciatura: traccia spezzata | ≤ 10 passaggi su 400 (da 132); `LINEA_ATTRAVERSATA` una sola ≥ 97 % | > 40 su 400 |
| P17 | `cor3`, avvicinamento diretto: uscite false | ≤ 5 su 400 (da 68) | > 20 |
| P18 | `cor3` non peggiora l'identità | «ne escono due»: `COMPARSA_DA_OMBRA` ≥ 385 su 400; transito: riapparizioni mancate ≤ 6 | `COMPARSA_DA_OMBRA` < 360 |

---

## Esiti — scritti alle 2026-11-14T16:02:24+01:00 (`date -Is`), dopo tutti i lanci (`ris_pd09.txt`, `ris_pd09_smooth6.txt`, `ris_pd09_pf002.txt`, `ris_pd07.txt`)

| # | Esito con i numeri |
|---|---|
| P1 lampeggio senza isteresi | **regge** per «alla lettera» (400 e 381 su 400 con più fronti); **smentita** per la mia «corretta»: l'isteresi sulla velocità del filtro non basta (avvicinamento mancato 60, attraversamento falso 86 su 400) |
| P2 uscite false | «alla lettera» 207/2800 = 7,4 % (**regge**; a Pd 0,7 23,5 %, sotto il 40 % previsto); «corretta» 70/2800 = 2,5 % (**smentita**: 68 sono chi si ferma a 11–14 cm dall'anello cieco e perde la traccia). Il meccanismo non è quello previsto: è la traccia spezzata alla fermata |
| P3a, P3b, P3c sosta | lato lontano: evento emesso 400/400 (**regge**) ma con μ2 > 0,8 solo 172/400 (**smentita**); soste false nel transito: alla lettera 180/400, 142 contando solo a soggetto nascosto (**smentita**, attese 1–10 %); corretta 2/400; sosta vera con μ2 > 0,8: solo 223/400 in 10 s (**smentita**) |
| P4 la porta non ferma lo scambio | regola del nucleo: riaggancio sbagliato in 392 occasioni su 392 (392 passaggi su 400: sotto il 99 % scritto); ancora in porta **381/392** (attese 40–80 %: la porta è più vuota del previsto) |
| P5 ritorni legittimi fuori porta | prosegue 0/398; sosta 2–4 s 0/397 (**reggono**); torna indietro 90/398 = 22,6 % (atteso 30–90); velocità tripla 236/346 = 68 % (atteso ≥ 90): 31 % entro la v_max di 2,5 m/s, 94 % oltre. **Fuori dai miei intervalli, non smentite** |
| P6 «ne escono due» | alla lettera `INGRESSO_AREA` falso 400/400; corretta 392/400 e 391 marche retroattive: **non è «per costruzione»** (8 casi persi per rilevamenti mancati nella fascia) |
| P7 occlusioni false | alla lettera 177/400 (44 %; atteso 5–40) e strato acceso a vuoto a fine passaggio **79/400** (atteso ≤ 5 %: **smentita**; il nucleo misurava 12,8–14,3 %); corretta 2/400 e 5/400 (**regge**) |
| P8 falsi al bordo | **regge**: 386/400 contro 0/400 |
| P9–P18 (tornate successive) | P9 **smentita** (52 e 54 su 400), P9bis regge (3 e 0); P10, P12, P14, P16, P17, P18 reggono; P11 1,75 % (attesa < 1 %, soglia 3 %: non risolta); P13 **smentita** (65/400 spezzate anche con decelerazione di 0,4 s); P15 regge senza lisciatura (346/400), non con (370/400 contro ≥ 97 %) |
