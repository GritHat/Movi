# Previsioni di sciame-sviluppatore (f10, catena di riferimento)

Scritte il **2026-11-14T16:21:55+01:00** (`date -Is`), prima di scrivere una riga di codice e di lanciare qualunque
prova: a quell'ora `10-catena/` era vuota (`ls`, stessa chiamata). Gli esiti stanno in fondo, aggiunti dopo e tenuti
distinti. Le scene sono matrici di profondità costruite con le formule chiuse di `03-infrastruttura/formato_sequenza.md`
(suolo piano e pannelli verticali di fronte alla camera), senza rumore: 848×480, fx = fy = 424, cx = 423,5, cy = 239,5,
camera a 1,2 m inclinata di 15°, 15 fotogrammi al secondo. Griglia 1° × 0,1 m da −90° a +90°, fino a 3 m (5400 celle).
Parametri del nucleo: fascia 0,40 m, q = 0,2 m²/s³, conferma 3 su 5, porta al 99 %, curva di rumore nominale.

| Sigla | Scena | Previsione | Soglia di smentita |
|---|---|---|---|
| svil-P1 | pavimento vuoto, 5 fotogrammi | 0 celle occupate, 0 in ombra, 0 tracce; le 1496 celle interne (azimut fra −44° e +44°, distanza fra 1,3 e 3 m) tutte «libero»; nessun «libero» sotto 1,2 m (anello cieco) né oltre ±52° (fuori campo) | una cella occupata o in ombra; meno del 99 % delle interne libere; un «libero» nell'anello cieco o fuori campo |
| svil-P2 | nessun dato (tutti 0); poi pavimento per 3 fotogrammi e di nuovo 0 | con tutti 0: 5400 «non osservato», 0 «libero». Dopo il pavimento: «libero» resta uguale per 2 fotogrammi senza dato (età 1 e 2) e scende a 0 al terzo | un «libero» senza suolo negli ultimi 3 fotogrammi; «libero» che cala prima del terzo |
| svil-P3 | pavimento con un buco di pixel a 0 (azimut ±10°, distanza 1,8–2,4 m) | buco fisso: le celle interne al buco (±9°, 1,9–2,3 m) sono «non osservato» in ogni fotogramma, quelle a più di una cella dal buco «libero». Buco che dura 2 fotogrammi: nessuna cella cambia stato (memoria); buco che dura 3 o più: «non osservato» dal terzo | un «libero» dentro il buco fisso; un cambio di stato con il buco di 2 fotogrammi |
| svil-P4 | pannello 0,5 × 1,5 m a 2,05 m, 30 fotogrammi | un gruppo di 14 celle occupate (ammesse 14–16) nell'anello 2,0–2,1 m; centro entro 2 cm da (0; 2,05); larghezza 0,50 ± 0,08 m; dietro, 126 celle in ombra (ammesse 126–144) e 0 «libero»; davanti (azimut ±6°, 1,3–1,9 m) tutto «libero»; una traccia confermata al terzo fotogramma, «osservato» da lì in poi, mai «si muove» | un «libero» dietro il pannello; più di un gruppo; un fotogramma «si muove» |
| svil-P5 | ostacolo basso (0,4 × 0,5 m a 1,6 m): il suolo torna visibile oltre 2,74 m | lettura prudente (predefinita): 0 «libero» dietro l'ostacolo fino a 3 m, e il contatore «suolo visto dentro l'ombra» conta almeno 20 celle. Con l'interruttore «libero dietro l'ostacolo»: le celle fra 2,8 e 3 m (azimut ±6°) diventano «libero» (almeno 22 su 24), quelle fra 1,7 e 2,7 m restano in ombra | un «libero» dietro l'ostacolo nella lettura prudente; un «libero» fra 1,7 e 2,7 m in quella larga |
| svil-P6 | sagoma 0,4 × 1,7 m che attraversa a 2,2 m, da x = −1,5 a +1,5 m a 1 m/s | una sola identità dall'inizio alla fine; confermata al terzo fotogramma; «si muove» entro 0,5 s (fotogramma ≤ 7) e poi sempre; errore del centro ≤ 3 cm dal fotogramma 10; velocità finale 1,0 ± 0,1 m/s in x e 0 ± 0,1 in z | due identità; «si muove» assente dopo il fotogramma 7; errore > 3 cm |
| svil-P6b | la stessa sagoma che passa davanti a un pannello fermo (0,6 m a 2,7 m) | il pannello fermo non è mai «si muove» (C6: il gruppo tagliato dall'ombra non aggiorna il filtro) e tiene la sua identità | un fotogramma «si muove» sul pannello |
| svil-P7 | geometria della demo: pannello 1 × 1,6 m a 1,9 m, sagoma che passa dietro a 2,3 m a 1 m/s | stessa identità dopo l'occlusione; 0 fotogrammi «osservato» a sagoma del tutto nascosta; lo strato di possibile presenza è acceso in tutti i fotogrammi nascosti e contiene la cella del centro vero; «previsto» dura fra 0,2 e 0,8 s e diventa «perso» prima della ricomparsa; lo strato finisce per «riaggancio»; il pannello non è mai «si muove» | identità diversa; un «osservato» da nascosta; centro vero fuori dallo strato |
| svil-P7n | come P7, con la fascia a 0 m (braccio che deve fallire) | l'identità NON si conserva (riaggancio rifiutato, «identità ambigua») | se l'identità si conserva, la prova P7 è cieca sulla fascia |
| svil-P8 | come P7, ma la sagoma si ferma dietro il pannello per 5 s | lo strato resta acceso per tutti i 5 s, con l'età che cresce e lo stesso numero di celle (nessun rilascio, nessun tetto di tempo); stato «perso»; mai «libero» sulla cella del centro vero | strato spento prima della ricomparsa |
| svil-P9 | sagoma in campo aperto che sparisce di colpo (K-018) | nessuno strato di possibile presenza (l'ombra propria non conta); «non confermato» per 3 fotogrammi, poi traccia chiusa «non più rilevato» | uno strato acceso |
| svil-P10 | dopo l'ingresso in ombra spariscono pannello e sagoma (resta il pavimento) | le celle del cuneo si rilasciano e lo strato finisce al terzo fotogramma di pavimento, con motivo «celle libere» | fine prima del terzo fotogramma, o per un altro motivo |
| svil-P11 | assegnazione ungherese | costo uguale alla ricerca esaustiva su 200 matrici casuali fino a 6 × 6, e a `scipy.optimize.linear_sum_assignment` (altro autore) su 200 matrici fino a 12 × 12 | un costo diverso |
| svil-P12 | filtro di Kalman | il predittore in forma chiusa dallo stato d'ingresso coincide con il filtro passo per passo (differenza < 1e-9 dopo 2 s); varianza di posizione dopo t secondi senza misure = P0 + q·t³/3 (da velocità nota) | differenza ≥ 1e-9 |
| svil-P13 | scena P4 con la posa tolta da meta.json | la stima robusta del suolo ritrova l'altezza entro 1 cm e l'inclinazione entro 0,3°; il conteggio delle celle «libero» differisce meno del 2 % | fuori da queste tolleranze |
| svil-P14 | `03-infrastruttura/esempio_sequenza/` (altro autore, 160×120) letta dalla cartella | 31 righe nel file d'uscita, ciascuna JSON valida; 0 invarianti violati; riassunto scritto. A 160×120 molte celle lontane restano «non osservato» (meno di un pixel per cella): non prevedo il numero | meno di 31 righe; un invariante violato |
| svil-P15 | invarianti (braccio che deve fallire) | forzando un «libero» su una cella senza suolo visto, e un «osservato» senza misura, il codice solleva l'errore dell'invariante in tutti e due i casi; in tutte le altre prove: 0 violazioni | un invariante forzato che passa in silenzio |
| svil-P16 | costo | a 848×480, un filo, con gli invarianti accesi: media < 15 ms per ciclo e 95° percentile < 25 ms sulla scena P7 (la lettura del file esclusa) | media ≥ 15 ms o p95 ≥ 25 ms |

Che cosa queste prove NON dicono, già ora: le scene le costruisco io con le stesse formule di proiezione che la catena
inverte (stesso autore, stessa specifica, stesso modello): reggono solo contro errori di logica, non contro un errore
comune nella geometria. Fanno eccezione P11 (scipy), P14 (sequenza di un altro autore) e il confronto del suolo con
`profondita_del_suolo` dell'infrastruttura. Nessuna scena ha rumore, pixel misti o buchi realistici: quelli sono del
simulatore del sensore e dei dati veri.

## Previsioni aggiunte dopo la prima tornata (prima di scrivere e lanciare le prove nuove)

Scritte il **2026-11-14T16:34:08+01:00** (`date -Is`), dopo aver visto gli esiti di svil-P1…P16 e prima di scrivere le prove
P17–P20. Servono a coprire regole che la prima tornata non toccava (il braccio P7n è fallito per la regola
d'ingresso, non per quella di riaggancio). Il pannello della demo è ora alto 1,8 m (vedi l'esito di P7).

| Sigla | Scena | Previsione | Soglia di smentita |
|---|---|---|---|
| svil-P17 | la sagoma entra dietro il pannello e si ferma; al fotogramma 30 una seconda sagoma compare ferma in campo aperto a (1,5; 2,2), lontana 0,9 m dall'ombra | nessun riaggancio e nessun evento «identità ambigua»; la seconda sagoma prende un'identità nuova; la prima traccia resta pendente con lo strato acceso fino alla fine | un riaggancio; la seconda sagoma con l'identità della prima |
| svil-P18 | sagoma sulla linea a 2,7 m (a meno di 0,40 m dal bordo della portata), che passa dietro il pannello e ricompare | nessun riaggancio; almeno un evento «identità ambigua» con motivo «bordo della portata»; alla fine la sagoma ha un'identità diversa e la traccia vecchia resta pendente con lo strato acceso (nucleo, C1: 0 % di riagganci a 2,8 m) | un riaggancio |
| svil-P19 | sagoma ferma a (0; 2,2) per 6 fotogrammi; poi sparisce e al suo posto c'è un buco di pixel a 0 (azimut ±12°, 1,9–2,6 m) per 6 fotogrammi; poi pavimento pieno per 5 | «affidabilità persa» nei 6 fotogrammi del buco (la traccia non si chiude); poi «non confermato» per 3 fotogrammi e chiusura «non più rilevato» al quarto; mai uno strato di possibile presenza | traccia chiusa durante il buco; uno strato acceso |
| svil-P20 | la scena P4 passata da `esegui` con una sorgente in memoria e meta senza posa; l'esempio dell'infrastruttura con `--ogni 2` e `-p portata_m=2.0` | il riassunto dichiara la posa «stimata» (1,2 m ± 1 cm; 15° ± 0,3°); con `--ogni 2` escono 16 righe e la griglia ha 20 anelli | posa non dichiarata come stimata; righe diverse da 16 |

Aggiunta il **2026-11-14T16:37:16+01:00**, prima di scrivere la prova: **svil-P21** (fumo con rumore, non una validazione) — la scena P7
con rumore gaussiano indipendente per pixel (σ = 0,00377·Z², la curva nominale) e il 2 % di pixel a 0 a caso per
fotogramma, seme fisso. Previsione: la catena arriva in fondo senza violare invarianti e senza errori; la sagoma non è
mai «osservato» nei fotogrammi in cui è nascosta. Non prevedo se l'identità si conserva né quanti gruppi falsi nascono:
li riporto. Smentita: un invariante violato, un'eccezione, un «osservato» a sagoma nascosta.

## Esiti

Compilati il 2026-11-14T16:38:58+01:00, dopo le prove (prima tornata alle 16:32:16, ultima alle 16:37:46). Il testo sopra non è stato
toccato. Per rifare: `<ambiente>/venv/bin/python -I -B prove.py` (ultimo esito in `esito_prove.txt`: 25 prove, 0 fallite).
Esiti: **regge**, **smentita**, **non risolta**.

| Sigla | Esito | Prova (numeri da `esito_prove.txt`) |
|---|---|---|
| svil-P1 | **smentita nel numero** | 0 occupate, 0 in ombra, 0 tracce, nessun «libero» sotto 1,2 m né oltre ±52°: reggono. Ma le interne libere sono 1442 su 1496 (96,4 %, soglia 99 %). Causa: un errore mio di geometria nella previsione, non della catena: il bordo vicino del suolo visto è la retta z = 1,22 m, non il cerchio di raggio 1,22 m (a ±44° il suolo si vede solo da 1,69 m). Le 54 celle mancanti sono tutte e sole quelle con z < 1,3 m. Controllo aggiunto dopo: tutte le celle interne oltre la retta sono libere. |
| svil-P2 | **regge** | 5400 «non osservato» con tutti 0; «libero» per fotogramma 1630, 1630, 1630, poi 1630 (età 1), 1630 (età 2), 0, 0 |
| svil-P3 | **regge** | buco fisso: 0 «libero» dentro; buco di 2 fotogrammi: griglie identiche; di 4: «non osservato» dal terzo |
| svil-P4 | **regge** | 14 celle occupate nell'anello 2,0–2,1 m; centro (0,000; 2,050); larghezza 0,4997 m; 126 in ombra; 0 «libero» dietro; confermata al terzo fotogramma; 0 «si muove» su 30 |
| svil-P5 | **regge** | lettura prudente: 0 «libero» dietro, 68 celle con suolo visto dentro l'ombra; con l'interruttore: 24 libere su 24 oltre 2,8 m, 0 fra 1,7 e 2,7 m |
| svil-P6 | **regge** | una identità; «si muove» dal fotogramma 5 (0,33 s); errore massimo sotto 0,05 cm; velocità (1,000; 0,000) m/s |
| svil-P6b | **regge** | pannello fermo con misura tagliata in 15 fotogrammi su 46, mai «si muove», stessa identità |
| svil-P7 | **non risolta com'era scritta; regge con la scena corretta** | Con il pannello alto 1,6 m scritto nella previsione la sagoma non è MAI nascosta (0 fotogrammi su 49): da 1,2 m la camera vede sopra il pannello tutto ciò che a 2,3 m supera 1,684 m. Scena corretta a 1,8 m (cambiata dopo il primo esito): 13 fotogrammi nascosti, 0 «osservato», 4 «previsto» e 9 «perso», centro vero dentro lo strato 13 su 13; «perso» dopo 0,267 s; riaggancio con la stessa identità (errore della previsione 0,17 m, raggio al 95 % 1,12 m); pannello mai «si muove» |
| svil-P7n | **regge, ma per un'altra regola** | con la fascia a 0 l'identità non si conserva; cade però la regola d'ingresso (traccia chiusa al fotogramma 21), non il riaggancio: per questo P17 e P18 |
| svil-P8 | **regge** | strato acceso 88 fotogrammi su 88, sempre 640 celle, età finale 5,8 s, stato «perso», mai «libero» sul centro vero |
| svil-P9 | **regge** | nessuno strato; «non confermato» ×3, chiusura al fotogramma 18 |
| svil-P10 | **regge** | strato finito al fotogramma 27 (terzo di pavimento), motivo «celle libere» |
| svil-P11 | **regge** | 200 su 200 contro la ricerca esaustiva, 200 su 200 contro scipy (dopo aver corretto la prova: passavo interi di numpy a itertools) |
| svil-P12 | **regge** | differenza < 1e-9; q·t³/3 esatto |
| svil-P13 | **regge** | 1,2000 m; 15,000°; rollio 0,000°; «libero» 1490 contro 1490 |
| svil-P14 | **regge** | 31 righe, 0 invarianti violati; celle·fotogramma: 120 270 non osservato, 35 110 libero, 1080 occupato, 10 940 in ombra |
| svil-P15 | **regge** | 2 invarianti forzati su 2 sollevano l'errore; 0 violazioni nelle altre prove |
| svil-P16 | **regge** | media 2,5 ms, 95° percentile 2,9 ms, massimo 4,7 ms (N = 48; fra una tornata e l'altra la media è stata 2,1–2,6 ms) |
| svil-P17 | **regge** | 0 riagganci, 0 «identità ambigua», identità nuova per la seconda sagoma, strato acceso |
| svil-P18 | **regge** | 0 riagganci; 8 eventi «identità ambigua» (bordo della portata); identità 1 → 3; la traccia 1 resta «perso» |
| svil-P19 | **smentita con la prima realizzazione, regge dopo la correzione** | Prima: «non confermato» nei primi 2 fotogrammi del buco, perché la cella dell'ultima misura (occupata fino a un fotogramma prima) usciva «libero» per memoria: bastava il suolo visto nella stessa cella. Ho cambiato la lettura della memoria (vale solo se la cella era stata vista LIBERA): ora «affidabilità persa» ×6, «non confermato» ×3, chiusura al fotogramma 15 |
| svil-P20 | **regge** | posa dichiarata «stimata»; 16 righe con `--ogni 2`; 20 anelli con `-p portata_m=2.0` |
| svil-P21 | **regge** (fumo) | nessun invariante violato; 2 tracce nate e 2 confermate (nessun gruppo falso), identità conservata; in media 1252 libero, 71 occupato, 315 in ombra, 2,1 celle ambigue |

### Notato dopo (non era previsto)

1. **La zona cieca vicina è una striscia, non un anello** (P1): il suolo si vede da z = 1,22 m in avanti; a ±44° vuol dire da 1,69 m di distanza.
2. **Un pannello alto 1,5–1,6 m non nasconde una persona di 1,7 m** dalla camera a 1,2 m (P7): a 1,9 e 2,3 m serve almeno 1,2 + 0,5·1,9/2,3 = 1,61 m (conto mio), e con 1,6 m la prova dà 0 fotogrammi nascosti su 49.
3. **«Libero» per memoria su una cella che era occupata** (P19): con la regola letterale del nucleo capita; sull'esempio dell'infrastruttura erano 23 celle·fotogramma (35 133 → 35 110 «libero»).
4. **Dopo un riaggancio con misura tagliata il filtro resta dov'era** (P8): per 6 fotogrammi la traccia è «osservato» ma la posizione del filtro dista fino a 5,00 m dalla verità (la misura è in `ultima_misura`).
5. **La marca «tagliato» scatta una cella prima** (esempio dell'infrastruttura): misura tagliata dai fotogrammi 3 e fino al 27, dove la verità dà la sagoma visibile per intero. Lì la sagoma, che cammina a 1 m/s, non è mai detta «si muove» (solo 3 misure piene di fila) e passa da «osservato» a «perso» senza un fotogramma di «previsto».
6. Sull'esempio dell'infrastruttura (geometria di un altro autore) il centro esce a 0,4 mm dalla verità al fotogramma 0 (−0,9996 contro −1,0) e l'ostacolo a (0,0; 1,5).
7. **Il riaggancio letterale è fragile a bassa risoluzione** (notato alle 16:40 provando i comandi del LEGGIMI):
   sull'esempio dell'infrastruttura con `--ogni 2` escono 0 riagganci e 5 «identità ambigua» (3 «altro bordo del non
   osservato», per celle mai campionate a 160×120; 2 «bordo della portata»); a passo pieno 1 riaggancio.
8. Pavimento vuoto, stessa posa: 1270 celle libere a 160×120 (fx 84,3) contro 1630 a 848×480 (fx 424); i due campi
   non sono identici, quindi il confronto è indicativo.
