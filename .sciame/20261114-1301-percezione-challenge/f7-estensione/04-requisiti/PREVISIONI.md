# Previsioni di `sciame-requisiti` (f7, corsia A) — scritte PRIMA delle prove

Ora di scrittura: 2026-11-14T15:05:58+01:00 (`date -Is`). Nessun conto e nessuna simulazione eseguiti prima di questa ora.

**Che cosa avevo già letto quando ho scritto** (e che quindi toglie valore di previsione ai conteggi): il contratto dell'estensione, la traccia, `promptMare.txt` per intero, gli addendum, il contratto originale, `SOLUZIONE_V2.md`, `SPECIALIZZAZIONE.md`, `ATTACCO_SPECIALIZZAZIONE.md`, `AUDIT.md`, `proposta_sciame.tex`, `VERSIONI.md`. Non avevo letto: `VERDETTO.md`, `QUADRO_DOMINIO.md`, `MOTO_PROPRIO.md`, i PDF.

## A. Conteggi sui testi (valgono come conti, NON come previsioni: i testi li ho già letti)

- A1. Nella traccia (`regole_challenge.md`) le parole `uncrewed`, `drone`, `UAV`, `veicol`, `autopilot`, `sentinell`, `voxel`, `3D`, `tridimension`, `volo` compaiono 0 volte. Smentita: una sola occorrenza.
- A2. In `promptMare.txt` `UAV` o `drone` compaiono almeno 8 volte; `monitoraggio`, `attività`, `ispezione`, `accessibilit`, `disabilit`, `non vedent`, `assistiv` compaiono 0 volte. Smentita: meno di 8 nel primo gruppo, o una occorrenza nel secondo.
- A3. Nel sorgente della proposta (`proposta_sciame.tex`) `uncrewed` compare almeno 5 volte e la parola `monitoraggio` 0 volte; `attività` 0 volte. Smentita: `monitoraggio` o `attività` presenti come ambito.

## B. Lo strato minimo di eventi (previsioni vere: il programma non esiste ancora)

Prova: uno script Python puro (`eventi.py`, seme fissato, `timeout 120`), che contiene (i) un generatore di scena sul piano con la geometria della demo (sensore nell'origine, campo 87°, zona 1,24–3 m, pannello largo 1 m a 1,7 m, attore sulla linea a 2,3 m), che produce per fotogramma a 15 Hz lo stato delle tracce con le regole del nucleo ridotte all'osso (osservato; senza misura accanto all'ombra dell'occlusore → previsto per 0,65 s → perso con possibile presenza; senza misura in campo aperto → non confermato per al più 3 fotogrammi, poi chiusa); (ii) un estrattore di eventi che legge SOLO quel flusso di stati (non la verità); (iii) un oracolo che confronta gli eventi con il copione vero della scena. 200 scene per braccio, velocità 0,5–1,4 m/s, sosta dietro il pannello 0–20 s, probabilità di rilevamento 1,0 e 0,9.

- B1 (copertura). Con rilevamento certo l'estrattore emette tutti gli eventi del copione (ingresso in zona, uscita, scomparsa dietro l'ostacolo, ricomparsa, permanenza in zona non osservata oltre 5 s, affidabilità persa e ritrovata): **0 eventi mancati su tutte le scene**; ritardo dall'istante vero ≤ 0,5 s al 95° percentile per ingresso, uscita, scomparsa, ricomparsa (contando 3 fotogrammi di conferma = 0,2 s). **Smentita:** un evento del copione mancato, o p95 del ritardo > 0,5 s.
- B2 (R4 nello strato eventi). **0 eventi con stato «osservato»** riferiti a una traccia in un fotogramma in cui il soggetto è davvero nascosto o l'affidabilità è persa; in particolare 0 «uscita dalla zona (osservata)» durante la sosta dietro il pannello. **Smentita:** uno solo.
- B3 (braccio che deve fallire). Un estrattore ingenuo, che emette «uscita dalla zona» quando la traccia non è più «osservato» dentro la zona, produce **almeno una «uscita» falsa in ≥ 90 % delle scene con sosta nascosta** in una zona che interseca l'ombra. Se non fallisce, la prova B2 è cieca.
- B4 (rilevamento 0,9). Con un rilevamento mancato su dieci: 0 violazioni di B2; eventi spuri «scomparsa dietro l'ostacolo» in campo aperto: **0** (la regola guarda l'ombra dell'occlusore, non quella propria); scene con almeno un evento spurio di chiusura «non più rilevato» (4 mancati di fila): **≤ 10 %** (attesa mia, a mano: circa 60 fotogrammi visibili × 10⁻⁴ ≈ 0,6 %; con 3 di fila, 5 %). Eventi mancati del copione: ≤ 2 % delle scene. **Smentita:** oltre il 10 % di scene con chiusure spurie, o oltre il 2 % con un evento mancato, o una violazione di B2.
- B5 (costo). Estrattore ≤ 150 righe di Python (senza generatore né oracolo); tempo per fotogramma con 1 traccia e 3 zone: mediana < 0,1 ms, massimo < 2 ms; con 20 tracce e 8 zone: mediana < 1 ms, massimo < 5 ms, cioè < 1,5 % e < 7,5 % del ciclo di 66,7 ms a 15 Hz nel caso peggiore previsto. **Smentita:** oltre 150 righe, o una delle quattro soglie superata.
- B6 (limite atteso, da cercare e non da nascondere). Un evento che il nucleo non può dare: **l'uscita dall'area di chi resta nascosto** (esce dalla portata restando in ombra). Previsione: l'estrattore non emette mai «uscita» in quel caso e lascia aperto «permanenza in zona non osservata» senza fine: 100 % delle scene di quel tipo. È il comportamento voluto (la risposta giusta è «sconosciuto»), ma è un limite del «monitoraggio di attività»: va dichiarato.

**Indipendenza, dichiarata prima.** Generatore, estrattore e oracolo li scrivo io, nello stesso file, con lo stesso modello linguistico e la stessa lettura della specifica: la prova vale come **controllo della logica dello strato eventi**, non come dato sul nucleo né sul sensore vero. L'oracolo usa la verità della scena (posizione vera, occlusione geometrica vera) e non gli stati: è indipendente dall'estrattore solo per quel tratto. Gli stati del nucleo sono una riduzione mia delle regole di `SOLUZIONE_V2.md` §2 (B5), non il nucleo.

## B-bis. Aggiunte delle 2026-11-14T15:09:10+01:00 (dopo i soli conteggi A e la lettura di `VERDETTO.md` e di alcune righe di `QUADRO_DOMINIO.md`; `eventi.py` non esiste ancora e nessuna simulazione è stata lanciata)

Esito dei conteggi A, già noto a quest'ora: A1 regge (0); A2 regge (12 fra `UAV` e `drone`; 0 nel secondo gruppo); A3 **smentita nella prima metà** (`uncrewed` compare 4 volte nel sorgente, non almeno 5) e regge nella seconda (0 `monitoraggio`, 0 `attività`).

- B7 (eventi spuri accanto all'ombra, con rilevamento 0,9). Il verdetto riporta «12,8–14,3 % di strati accesi a vuoto con Pd 0,9»: un rilevamento mancato a meno di 0,40 m dall'ombra apre lo stato «previsto». Previsione: **senza conferma**, in ≥ 50 % delle scene esce almeno una «scomparsa dietro l'ostacolo» spuria (soggetto in vista, dentro la fascia); **con una conferma di 3 fotogrammi (0,2 s)** in ≤ 5 % delle scene. **Smentita:** meno del 50 % nel primo braccio, o più del 5 % nel secondo.
- B8 (sosta osservata, fuori dall'elenco di B1). Una sosta in vista di 4 s in una zona dà l'evento «sosta (osservata)» entro 2 s + 1,5 s dall'arresto vero in ≥ 95 % delle scene con rilevamento certo; nessuna «sosta (osservata)» per la sosta nascosta (lì esce solo «permanenza non osservata»). **Smentita:** meno del 95 %, o una sola «sosta osservata» a soggetto nascosto.
- Scelte di prova fissate ora, prima del lancio: cinque tipi di scena (transito; sosta nascosta 1–20 s; uscita dalla portata restando in ombra; sosta in vista; sensore coperto per 2 s), 40 scene per tipo e per braccio; tre zone dichiarate (due in campo aperto, una «area del mezzo» a cavallo dell'ombra con 0,5 m visibili per lato); il soggetto è un punto (niente corpo largo, niente gruppi tagliati dall'ombra); un evento del copione conta come trovato se esce entro 1,5 s; nelle scene con il sensore coperto non si contano gli eventi attesi fra 0,5 s prima e 1 s dopo la copertura; un'«uscita» conta come falsa se il soggetto vero sta dentro la zona di oltre 0,15 m.

## C. Dopo le prove (scritto alle 2026-11-14T15:22:33+01:00; qui sopra non è stato ritoccato niente)

Lanci: primo lancio 15:10:52 (`risultati_eventi_lancio1.txt`); poi un conteggio di diagnosi senza previsione; poi modifiche allo script (seconda lettura dietro l'argomento `2`, più una riga di conteggio) e due lanci alle 15:12:45 (`risultati_eventi.txt`, che rifà il primo con le stesse cifre, e `risultati_eventi_lettura2.txt`).

| Previsione | Esito |
|---|---|
| A1, A2 | reggono (conti) |
| A3 | prima metà smentita (4, non almeno 5); seconda regge |
| B1 | **smentita**: 103 scene su 200 con un evento mancato (97 uscite dalla zona a 0,13 m dal bordo della portata; 6 ricomparse dopo il sensore coperto). I ritardi reggono: p95 ≤ 0,27 s |
| B2 | regge: 0 violazioni, 0 uscite false, nei tre bracci (600 scene) |
| B3 | regge: braccio ingenuo, uscita falsa in 200 scene su 200 |
| B4 | violazioni: regge (0). «Scomparsa» in campo aperto: smentita (1). Chiusure spurie ≤ 10 %: smentita alla lettera (113 scene; l'oracolo non attendeva la chiusura all'uscita dal campo; 1 su 200 nella seconda lettura). Mancati ≤ 2 %: smentita (52 %; 16 % nella seconda lettura) |
| B5 | regge: 99 righe; 1,0 µs di mediana e 0,15 ms di massimo (1 traccia, 3 zone); 48 µs e 0,27 ms (20 tracce, 8 zone) |
| B6 | regge: 40 su 40 (39 su 40 con rilevamento 0,9) |
| B7 | senza conferma: regge (116 scene su 200, 58 %); con conferma: **smentita** (25 su 200, 12,5 %, contro ≤ 5 %) |
| B8 | regge con rilevamento certo (40 su 40; nessuna sosta «osservata» a soggetto nascosto); con rilevamento 0,9: 32 su 40 al primo lancio, 39 su 40 nella seconda lettura |

**[dopo], senza previsione:** 8 scene su 40 del tipo «sensore coperto» (3 su 40 con rilevamento 0,9) con il soggetto nascosto in portata per almeno 1 s, affidabilità buona e nessuna regione di possibile presenza; 166 ingressi su 482 trovati come «presente» (traccia nata dentro la zona); l'ordine delle voci in una riga di stampa cambia da un lancio all'altro (iterazione di un insieme di stringhe), le cifre no.

**Seconda lettura, che cosa cambia (scritta dopo il primo lancio):** nel nucleo ridotto un rilevamento fuori dalla fascia con una traccia pendente fa nascere una traccia nuova (prima era ignorato: difetto della mia riduzione, non di V2); nell'oracolo un ingresso o un'uscita si attende solo se il soggetto resta in vista per 4 fotogrammi, la chiusura a soggetto fuori vista non conta come spuria, e la «permanenza» ha una banda di 0,5 s attorno alla soglia.
