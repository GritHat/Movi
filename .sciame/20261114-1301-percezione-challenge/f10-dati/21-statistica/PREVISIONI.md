# PREVISIONI — sciame-statistico, f10/21-statistica

**Scritte alle 2026-11-14T17:29:04+01:00 (`date -Is`), prima di ogni mio calcolo.** Fin qui ho letto solo: `CONTRATTO_DATI.md`,
`20-validazione/VALIDAZIONE_DATI.md`, `20-validazione/PREVISIONI.md`, `stato.md`, `rifai.sh` e l'elenco dei nomi
dei file in `20-validazione/uscite/`. NON ho ancora aperto nessuna uscita grezza, né `DATI_VERI.md`, né
`SIMULATORE.md`, né le loro statistiche. Le cifre della validazione le conosco già (è ciò che devo controllare):
le previsioni riguardano quindi (i) se tornano ricalcolate con codice mio, (ii) l'incertezza con l'unità giusta,
(iii) ciò che la validazione non riporta. Esiti: regge / smentita / non risolta. Ciò che noto dopo è marcato «dopo».

Unità statistica: la sequenza (= un passaggio) per il simulato; per THÖR la persona (i tratti della stessa persona
sono correlati); per le registrazioni vere la sequenza. Intervalli: Wilson al 95 % per le quote; ricampionamento
(bootstrap) per sequenza o per persona per mediane e coperture; «regola del tre» (limite superiore 3/N) per gli zeri.

| # | Enunciato | Misura (codice mio, dalle uscite grezze) | Regge se | Smentita se | Che cosa prevedo |
|---|---|---|---|---|---|
| S1 | K-014: «0 su 2 907 032 celle·fotogramma, 135 sequenze» torna | conteggio delle celle «libero» fra le celle tutte dentro l'ombra vera, stati per cella presi dalle uscite della catena, ombra vera da `verita.json` del simulatore | 0 celle e denominatore entro ±2 % | ≥ 1 cella, o denominatore fuori ±2 % | torna (0); ma le 135 sequenze non sono 135 scene indipendenti: prevedo ≤ 40 combinazioni distinte (scena × profilo × livello) e ≤ 6 geometrie d'occlusore distinte |
| S2 | Bordo d'ombra: mediana +6,2, da +2,0 a +14,6 cm, 103 su 103 entro ±20 cm (D435i nominale) | azimut dell'ultima colonna «pannello» meno lo spigolo vero, per fotogramma e per lato, poi per sequenza | mediana entro ±1 cm, estremi entro ±2 cm, quota identica | altrimenti | torna; sui singoli fotogrammi gli estremi sono più larghi dei percentili per sequenza ma restano entro ±20 cm; gli errori sono quantizzati dal passo di 1° (4,2 cm a 2,4 m): al più 4 valori distinti |
| S3 | Rumore del centro, persona ferma (20 semi): 0,36 / 0,99 / 1,25 cm a 2 / 3 / 4 m | mediana sui semi dello scarto tipo radiale, dalle uscite `mem_fermi*` | entro ±10 % | altrimenti | torna; l'intervallo (bootstrap sui 20 semi) della mediana è largo almeno ±30 % |
| S4 | Continuità: 0 su 90 (nucleo), 41 su 45 sui dispari (soglia 40), 28 / 24 / 28 su 30 | conteggio per passaggio | conteggi identici | uno diverso | tornano; ma la «prova» di 40 non è pulita: prevedo che 40 sia stata provata sui dispari DOPO aver visto fallire 20 sugli stessi dispari (due candidati sugli stessi dati di prova), e che l'intervallo per caso (13 su 15) scenda sotto il 65 % |
| S5 | THÖR exp3: copertura della regione al 90 % con q = 0,2: 0,977 / 1,000 / 1,000; q = 0,05: 0,795 / 0,804 / 0,831; 219 tratti, 9 persone | ricalcolo con un filtro mio dalle tracce (se leggibili), altrimenti dal `banco_thor.json` | entro ±0,02 | altrimenti | torna entro ±0,02; con 9 persone l'intervallo per persona a q = 0,05 è largo ≥ 0,10; non si può verificare dai dati che le persone di exp1 e exp3 siano diverse («non verificato») |
| S6 | Quante sequenze vere con profondità e persone, e quante con un'occlusione vera | conteggio dal manifesto e dalle uscite `vere/` | — | — | ≤ 8 sequenze elaborate; ≤ 2 con un tratto nascosto utilizzabile; ≤ 4 tratti; 0 con verità indipendente della posizione. L'identità sul vero resta «2 su 2» → Wilson 34–100 %: non dice niente |
| S7 | Il simulatore somiglia al vero (stesso tipo di sensore: D435i simulato contro bag RealSense D435i/D435; D415 di DepthTrack) | quota di pixel validi per fotogramma; rumore temporale per pixel su scena ferma a 1–3 m; quota di non validi entro 8 px da un salto di profondità contro il resto | «somiglia»: quota di validi entro 10 punti percentuali e rumore entro un fattore 2 | fuori su almeno una coppia confrontabile | **smentita su almeno una coppia**: il vero ha più buchi (validi veri più bassi di oltre 10 punti in almeno una sequenza) e il rumore vero su scena ferma sta entro un fattore 3 ma non 2; le coppie davvero confrontabili (stesso modello, scena ferma, distanza nota) sono ≤ 2 |
| S8 | Scelte fatte dopo i dati oltre a quelle dichiarate in §0 (a)–(f) | lettura di script e uscite | — | — | ne trovo almeno 2 non dichiarate (per esempio: sequenze escluse da un denominatore, tetto ai cicli che taglia il tratto nascosto, «soglia scalata» scelta sulla stessa sequenza vera) |
| S9 | Quante cifre del rapporto non tornano | su ≥ 25 cifre ricalcolate | — | — | ≤ 3 non tornano oltre l'arrotondamento |

## Esiti (scritti alle 2026-11-14T17:39:15+01:00; cifre e file in ANALISI_DATI.md e in `tabelle/`)

| # | Esito | Cifra |
|---|---|---|
| S1 | **regge** sul conteggio; il denominatore torna **esatto solo sommando le 4 sequenze con i filtri** | 0 celle; 2 841 026 (131 sequenze, filtri spenti) + 66 006 (4 con i filtri) = 2 907 032. Con la mia definizione a 9 punti: 0 su 2 741 202 (−5,7 %: fuori dalla mia tolleranza, per la definizione). Combinazioni distinte 26 (≤ 40: regge); geometrie d'ombra 3 (≤ 6: regge) |
| S2 | **regge** | +6,2 / +2,0 / +14,6; 103 su 103; 4 livelli (+2,0; +6,2; +10,4; +14,6). «Estremi più larghi sui fotogrammi»: smentita (erano già sui fotogrammi) |
| S3 | **non risolta** come ricalcolo (i valori per seme non sono conservati); replica con semi nuovi: a 3 m fuori dal ±10 % | 0,34 / 0,84 / 1,18 contro 0,36 / 0,99 / 1,25; intervallo largo oltre ±30 %: regge (a 2 m: 0,24–3,81) |
| S4 | conteggi: **regge**; «40 provata sui dispari dopo il fallimento di 20 sui dispari»: **smentita in parte** (40 era già la migliore sui pari, 39 su 45); limite inferiore per caso sotto il 65 %: regge (62,1 %) | 0 su 90; 41 su 45; 28 / 24 / 28 |
| S5 | q = 0,2: **regge**; q = 0,05 a 1 s: **smentita alla lettera** (0,836 contro 0,795: oltre ±0,02), spiegata dal seme del rumore (0,790–0,836 su 20 semi); larghezza ≥ 0,10: regge (0,13) | vedi `tabelle/thor.txt` |
| S6 | **regge**, salvo i tratti (5, non ≤ 4) | 8 sequenze; 3 con tratti nascosti (5 tratti, 0,03–0,70 s); identità decidibile in 2 tratti di 1 sequenza; 0 con verità indipendente |
| S7 | pixel validi: **regge** (il vero ha 21–39 punti in meno); rumore «non entro un fattore 2»: **smentita** per il D435 (0,83–1,45), regge per il D415 (1,6–4,3, limite superiore) | `tabelle/confronto_profondita.txt`, `controlli_brevi.txt` |
| S8 | **regge** | quattro scelte non dichiarate (ANALISI_DATI.md §3) |
| S9 | **regge** | 3 cifre su oltre 30 |

Notato **dopo** (non previsto): a 2 m, con le soglie del nucleo, lo scarto del centro di una persona ferma è bimodale
(12 semi a 0,2–0,4 cm, 8 a 3,7–4,4 cm); la «mediana 1,00» della copertura nasconde 7 passaggi su 90 in cui la verità
esce dalla regione dichiarata; la variante «maschera a 2,4 m» della misura del bordo (`bordo_maschera`) è mia e scritta dopo.
