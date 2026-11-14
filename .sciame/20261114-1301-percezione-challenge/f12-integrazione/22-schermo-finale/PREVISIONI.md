# Previsioni — `sciame-interfacce`, f12, 22-schermo-finale

Scritte alle 2026-11-14T18:26:14+01:00 (`date -Is`), **dopo** aver letto contratto, SCHERMO_E_DEMO (05), ATTACCO_V3, COMPLETEZZA, CONTROLLO_PROVE, PIANO_RIFATTO, VERDETTO_DATI, DISCORDANZE (per intero) e parti di SOLUZIONE_V3, PIANO_14_4, PROVA_INSIEME, LIBERO, IDENTITA: non sono cieche rispetto ai testi. Scritte **prima** di stendere il documento finale e di lanciare i controlli qui sotto.

| # | Previsione | Misura | Soglia di smentita |
|---|---|---|---|
| Q1 | Nel documento finale nessuna frase «da non dire» compare fuori dall'elenco «da non dire → che cosa dire» e fuori dalle citazioni dichiarate | `controlla_frasi.sh` (ricerca testuale su un elenco scritto qui sotto) | almeno 1 occorrenza fuori dall'elenco |
| Q2 | Ogni stato della versione 3 (tabella di COMPLETEZZA §2: 4 stati di cella; possibile presenza; traccia tentativa, osservato, visto in parte, non confermato, ramo C2, previsto, previsto ampio; avviso c7 senza traccia; chiusure 1–5; affidabilità persa; identità ambigua) ha una riga nella tabella dei segni; nessun segno fuori da quell'elenco | conteggio delle righe della tabella dei segni contro l'elenco in `stati_v3.txt` | 1 stato senza riga, o 1 riga senza stato |
| Q3 | Intervalli di Wilson al 95 % ricontati da me: 27/30 → 0,74–0,97; 30/30 → limite 0,886; 46/50 → 0,812; 942/1045 → 0,882; 87/100 → limite fra 0,79 e 0,80 | `conti_finali.py` | uno scarto oltre 0,005 |
| Q4 | La regola «almeno 87 su 100» esclude 0,80 al livello 0,05 (binomiale esatta, una coda) e 86 su 100 no | `conti_finali.py` | P(X ≥ 87 \| 0,80) > 0,05, oppure P(X ≥ 86 \| 0,80) ≤ 0,05 |
| Q5 | Geometria: con la camera a 1,2 m, 15° in basso e campo verticale di 58°, a 2,3 m il bordo alto del campo sta a 1,77 m (± 0,02): un attore più alto ha la testa tagliata. Con il pannello alto 1,8 m a 1,7–1,8 m, a 2,3 m resta nascosto tutto ciò che è sotto 1,95 m o più | `conti_finali.py` (conto in pianta e in alzato, foro stenopeico ideale) | bordo alto fuori da 1,75–1,79 m; quota nascosta sotto 1,95 m |
| Q6 | Ombra del pannello largo 1 m a 1,7–1,8 m sulla linea a 2,3 m: 1,28–1,35 m; l'attore passa 0,5–0,6 m dietro il pannello (dominio della prova sull'identità: almeno 0,5 m) | conto | fuori da quei valori |
| Q7 | Il documento sta in quattro pagine: al più 3 400 parole | `wc -w` | oltre 3 400 |
| Q8 | Durate del copione: gli atti della demo da 5 minuti sommano 300 s, quelli da 3 minuti 180 s | somma in `conti_finali.py` | somma diversa |

**Frasi cercate da Q1** (unione di VN, V7, V8, V9, VD, AS e delle 15 mancanti di COMPLETEZZA A14–A17, più W1–W5 dell'attacco): validato, certificato, garantit, tarato, via libera, nessun ostacolo osservato, bassa latenza, prevede dove sarà, continuità garantita, 100 %, mai dato per libero, solo guardando, mappa 3D, voxel, 360°, ACAS, TA/RA, anti-bird, detect and avoid, minaccia, NOMINAL, HOLD, FAIL-SAFE, preallarme, drone, UAV, in volo, orientamento, dispositivo medico, conforme a, ispezione, Intelligenza Artificiale, massa e accelerazione, riconosce la sosta, si è fermato, è uscito, 30 prove bastano, ellisse al 95, identità mantenuta, soglia 40, 15 Hz, validato su dati veri, dal vivo, in cinque ci sta, adottata, 0,85 m.

**Esiti:** in coda, dopo i controlli.
