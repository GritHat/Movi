# CIFRE del capitolo 1 (Introduzione) — una riga per cifra, con il file e il paragrafo d'origine

Percorsi relativi a `.sciame/20261114-1301-percezione-challenge/`. Sigle dei file:
**F01** `f13-allegato/01-dimostrazioni/FASCICOLO_DIMOSTRAZIONI.md` · **F02** `f13-allegato/02-geometria/FASCICOLO_GEOMETRIA.md` · **F03** `f13-allegato/03-stima/FASCICOLO_STIMA.md` · **F04** `f13-allegato/04-statistica/FASCICOLO_VALUTAZIONE.md` · **F05** `f13-allegato/05-costo/FASCICOLO_RAPPRESENTAZIONI_E_COSTO.md` · **DF** `f13-allegato/DISCORDANZE_DEI_FASCICOLI.md` · **SOL** `f12-integrazione/20-finale/SOLUZIONE_V3.md` · **PI** `f12-integrazione/02-prova-insieme/PROVA_INSIEME.md` · **ST** `f12-integrazione/13-statistica/CONTROLLO_PROVE.md` · **CI** `f12-integrazione/07-controprova-identita/CONTROPROVA_IDENTITA.md` · **BC** `f14-classificazione/20-inclusione/BLOCCO_CLASSIFICAZIONE.md`.

«Ricalcolato» = intervallo di Wilson al 95 % rifatto da me dai conteggi (16 intervalli, tutti coincidenti con il file all'ultima cifra scritta). Le cifre NON sono state ricontate dai file grezzi: sono copiate dai file qui sotto.

## §1.1 Il problema

| Cifra nel capitolo | Origine | Nota |
|---|---|---|
| punto fermo all'ultima misura: 1,48–1,54 m in mediana a 2 s; punto previsto 0,37–0,39 m; N 2077–2115 | F04 §6.3, riga «Errore mediano del punto mostrato» | una disposizione, miscela di comportamenti, modello ideale. Contestata in DF (da F04, II.2 n. 5: 0,97 / 1,53 / 1,64 contro 0,98 / 1,49 / 1,66): ho usato l'intervallo del fascicolo, che contiene entrambe |
| h = 1,2 m; θ = 15°; portata 3 m | SOL §1.1 «Parametri»; F02 §2 | scelti |

## §1.2 Tabella dei requisiti

| Cifra | Origine | Nota |
|---|---|---|
| 0,5 m/s, entro 1 s, 9 su 10, fino a 2 m | SOL §3, tabella dei requisiti, riga «elementi mobili» | |
| entro 15 cm; 5 su 5; fra 1,1 e 3 m | SOL §3, riga «ostacoli» | |
| almeno 4 misure prima della scomparsa | F04 §1 (passaggio valido) | |
| livello 1 − α = 0,90; τ ∈ {0,5; 1; 2; 3} s | F04 §1, Definizione 2 | |
| ℓ⁻ > 0,90 fino a 2 s; ℓ⁻ > 0,85 a 3 s | PI §1 riga b; F04 §6.3 (riepilogo per soglia) | |
| identità ≥ 0,95 sul percorso | PI §1 riga f | |
| 0 uscite «osservato» a soggetto nascosto | SOL §3, riga «osservato distinto dall'incerto» | |
| ≤ 300 ms | SOL §3, riga «feedback tempestivo» | non verificato |
| entro 1 s; 0 falsi in 60 s | SOL §3, riga «perdita di affidabilità» | |
| 95º percentile ≤ 150 ms | SOL §3, riga «latenza» | non risolta |
| Δ = 1/15 s = 66,7 ms | F04 §1, Definizione 8 | |
| soglie 0 della sicurezza | F04 §1, Definizione 5; SOL §3, ultima riga | |
| riga «classificazione»: 0 «libero» in più, 0 avvisi ridotti, nessun livello più basso | BC §5, invariante sulla prova differenziale | mai eseguita sulla catena |

## §1.5 Tabella di sintesi

| Cifra | Origine | Nota |
|---|---|---|
| rumore 5 cm; P_D; 424 × 240; tre camere | F04 §6, condizioni comuni | |
| «libero» della cella: 300 condizioni × 30 fotogrammi, due lanci; errore entro 0,5°; 0 celle; [0; 1,3 %] per condizione | ST §3 e §4 («Libero»); `f12-integrazione/03-libero/LIBERO_DELLA_CELLA.md` §0 n. 4, §1 | ricalcolato (0 su 300: 1,26 %). Regola scelta dopo il primo lancio: vedi NOTE |
| 0 su 2 907 032 celle·fotogramma; 131 sequenze; [0; 2,9 %] | F04 §6.1, riga «Celle libero dentro l'ombra vera» | ricalcolato (0 su 131: 2,85 %) |
| fascia 0,40 m; età 0,133 s; latenza 0,155 s; Δ = 0,067 s; 1,13 m/s; 0,56 m/s con 0,20 m | F01 §8 (tabella); SOL §1.7 | DF (da F01, D4): le due cifre sono l'applicazione della formula, non stanno nei file precedenti; SOL le adotta. Scelte queste, non «1,4 m/s» (età + latenza, margine zero) né 1,85 m/s (senza età). Ricalcolato: 0,40/0,355 = 1,127; 0,20/0,355 = 0,563 |
| continuità: 0 su 23 402; 12 combinazioni × 5 comportamenti; 6000 camminatori distinti; 6,4 su 10 000 | PI §1 riga a1; ST §0 (dicitura 1); SOL §1.6 «Continuità» | scelto «6,4», non «1,7» di PI: ST corregge (semi riusati fra i lanci). Ricalcolato (0 su 6000: 0,064 %) |
| premessa mancata: 24 su 23 402 | PI §1 riga a2; ST §1 controllo 2 | |
| con corpo puntiforme: 0 su 24 835; [0; 0,016 %] | F04 §6.1 e §6.2 (13 638 + 5600 + 5597, semi indipendenti) | ricalcolato |
| copertura: 30 combinazioni su 30; 2125/2279 (0,921); 1754/1922 (0,899); 608–2359 casi | ST §2 (tabella, righe T e L) e §4; SOL §1.6 «Precisione» | ricalcolato |
| pannello 1 m: 942/1045 (0,882); 0,87 su cinque | ST §2 (riga D) e §0 (dicitura 2) | ricalcolato |
| con corpo puntiforme: 826/879 a 2 s (0,922) | F04 §6.3, riepilogo per soglia, prima riga | ricalcolato. F04 («45 celle su 45», tre disposizioni, puntiforme) e PI/ST («30 su 30» con ostacolo largo 2 m, corpo esteso; cade col pannello da 1 m) non concordano e differiscono per il corpo: riportate entrambe con la condizione |
| fuori dominio: 0,13–0,70 a 2 e 3 s; N 538–1791 | F04 §6.3, tabella «Fuori dal dominio», righe «chi svolta» e «chi esce dal lato lontano» | corpo puntiforme |
| fuori dominio: 0,57–0,79, corpo esteso, ostacolo largo 2 m | SOL §7, tabella «Dove cede», prima riga; ST §2 «Segnale, non spiegato» | differenza con F04 non risolta nei file: riportate entrambe |
| bordo stimato 10–20 cm più stretto: 0,30–0,46 a 1 s | PI §0 n. 4 e §1 riga c; SOL §1.6 | |
| avviso non acceso: 29 su 95 399 | PI §2 (riga 65); SOL §1.7 e §7 | |
| 15 su 2000 con ombra più stretta di 0,20 m | SOL §1.7 «Con l'avviso davvero acceso»; SOL §7 | |
| identità, ideale: 10 711/10 757; 9228/9240; 6772/6967; 0,994; 0,998; 0,968 | PI §1 riga f; ST §1 controllo 2 | ricalcolato |
| identità, profondità simulata: 0 su 90, [0; 4,1 %] | F04 §6.4, seconda riga | ricalcolato |
| 176 su 180, [94; 99 %]; soggetto a 0,5 m dietro il pannello | CI §0 (primo e secondo punto); SOL §1.8 | scelta la cifra a 424 px; a 848 px 174 su 180 [93–98]. Non la «41 su 45» di F04 §6.4 (soglia a 40 punti, variante esclusa da SOL §4) |
| secondo soggetto: 19 casi su 20 | CI §0 «L'estraneo» | con le modifiche; l'avviso resta (0 fotogrammi fuori su 264) |
| traiettorie pubbliche: 219 tratti, 9 persone, q = 0,2; 0,977 / 1,000 / 1,000; [0,948; 0,990] | F04 §6.7 | DF (da F03, D6; da F04, n. 8): un secondo conto dà 0,982 / 0,995 / 1,000. Scelta la prima, come F04 |
| regola «mobile»: 100 %, N = 2000, ℓ⁻ = 99,81 % | F04 §6.5, prima riga | DF (da F03, D2): 99,81 è Wilson; i file precedenti davano 99,85 (limite unilaterale esatto) |
| pannello fermo «in movimento»: 79 su 90 [79,4; 93,0 %]; 5 su 90 | F04 §6.5 | |
| ostacoli: 84 su 84 (cassa 1 m a 1,68 m); 10 su 10 (scatola 15 cm a 2,0 m); 0 su 10 (a 0,8 m; vetro) | F04 §6.5, righe «Ostacolo fermo visto entro 15 cm» | una sequenza ciascuno |
| «osservato» a soggetto nascosto: 8 passaggi su 90; 1 su 140 | SOL §2, invariante 3; SOL §1.8 | senza intervallo nel capitolo (Wilson, calcolato da me: 4,6–16,6 % e 0,1–3,9 %) |
| σ_p = 3 cm; 15 Hz; 16,5 m/s²; 0,67 m/s² | F03 §4, Lemma 2 | ricalcolato (√6 · 0,03 · 15² = 16,53). DF (da F03, D4): 3 cm è un valore assunto |
| costo: 9152 cicli; media 6,35 ms; 95º percentile 18,6 ms; 4 cicli oltre 66,7 ms; 81 ms su 320 cicli | F04 §6.8; F05 §5, Tabella 5 | |
| latenza: 155 ms | F02 §8, Tabella 10; SOL §1.10 | DF (da F02, n. 8): circa 131 ms con un altro dato del costruttore (71 ms); scelta 155, somma delle medie con 95 ms |
| affidabilità persa: 0,13 s; 0 falsi in 60 s | SOL §1.9 «Stato»; SOL §3 | simulazione, rumore inerziale ipotizzato |
| classe e avviso: 0 su 20 000 e 0 su 20 000 | BC §0 e §7 | sulla sola fascia |
| 1,44 m/s; portata 3 m; reazione 1,0 s; 3 classi su 15; 0 su 15 | BC §6; F02 §7 (1,439) | ricalcolato ((3 − 0,95)/1,425 = 1,439) |

## §1.6 Riquadro e sommario

| Cifra | Origine | Nota |
|---|---|---|
| pixel senza dato: 7,8 % contro 24–34 % | F04 §6.6 «Che cosa il risultato non dice»; SOL §7 | |
| posa entro 0,5°; fino a 3 m; almeno 4 fotogrammi; nessuna cifra oltre 3 s | SOL §7 «La forma più forte che resta vera» e «Dove cede» | |
| sommario: 2 m; 0 su 23 402; 9 su 10 fino a 2 s; 85 su 100 fino a 3 s; 3 m | SOL §7 nn. 1–2; ST §4 | |
