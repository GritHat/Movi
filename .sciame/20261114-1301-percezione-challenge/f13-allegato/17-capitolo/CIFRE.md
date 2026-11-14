# CIFRE del capitolo 7 (`capitolo.tex`) — origine di ogni cifra

Percorsi relativi a `.sciame/20261114-1301-percezione-challenge/`. Sigle delle fonti:
**F05** = `f13-allegato/05-costo/FASCICOLO_RAPPRESENTAZIONI_E_COSTO.md` (parte I salvo dove è scritto II);
**F06** = `f13-allegato/06-bibliografia/FASCICOLO_BIBLIOGRAFIA.md`; **F01** = `f13-allegato/01-dimostrazioni/FASCICOLO_DIMOSTRAZIONI.md`;
**F02** = `f13-allegato/02-geometria/FASCICOLO_GEOMETRIA.md`; **F03** = `f13-allegato/03-stima/FASCICOLO_STIMA.md`;
**V7** = `f7-estensione/16-verdetto/VERDETTO_ESTENSIONE.md`; **V8** = `f8-continuita/16-verdetto/VERDETTO_CONTINUITA.md`;
**B8** = `f8-continuita/11-misure/BANCO_DI_PROVA.md` (file citato da V8); **V9** = `f9-preproposta/13-verdetto/VERDETTO_PREPROPOSTA.md`;
**SOL** = `f12-integrazione/20-finale/SOLUZIONE_V3.md`; **CL** = `f14-classificazione/03-classificatore/CLASSIFICATORE.md`;
**DIS** = `f13-allegato/DISCORDANZE_DEI_FASCICOLI.md`.
Nessuna cifra è stata ricalcolata da me dai file grezzi: sono trascritte dalle fonti indicate.

## Cifre contestate: quale valore ho scelto

| Cifra | Valori nei file | Scelta | Perché |
|---|---|---|---|
| Sovraccosto dell'octree | «2,2–3,9 su 18 configurazioni» (file d'origine) / 2,2–3,8 senza fusione e 2,3–3,9 con fusione, su 20 configurazioni (F05 II.2 punto 1) | 2,2–3,8 e 2,3–3,9, su 20 | il fascicolo corregge sul file grezzo; lo chiede la consegna |
| Previsione in Python, dieci oggetti | 5,3 / 6,2 ms (F05 §5, V8 riga 6) / 6,4 / 15,9 ms nel rilancio sotto carico (F05 II.1, II.5 punto 4) | entrambe, ciascuna con la sua condizione | nessun file decide; lo chiede la consegna |
| Oggetti sulla registrazione pubblica | «254 tracce» / 254 confermate in 21,3 s e 152 presenti insieme in mediana (F05 II.2 punto 6) | entrambe, dicendo che cosa misura ciascuna | il fascicolo distingue |
| Memoria della griglia densa | 4 byte per voxel (288 000 e 2 304 000) / 8 byte (576 000 e 4 608 000) (F05 II.2 punto 3) | 4 byte, con «il doppio con 8 byte» | come F05 parte I |
| «Libero» creato dal selettore | «14–57 %» (consegna) / 13,8 % e 57,0 % (V9 §1 riga del selettore; SOL §4) | 13,8 % e 57,0 %, attribuite a due simulatori | sono le cifre dei file; «14–57» ne è l'arrotondamento |
| Soste false con i pesi a ogni ciclo | 38,0–97,0 % (V9 §1, riga del ritaglio, due simulatori) / 38–100 % (V9 §3 fatto sui pesi, cinque simulatori; SOL §4) | 38–100 %, «cinque simulatori» | è l'intervallo più largo, sul maggior numero di simulatori |
| Intervallo dell'ellisse al 95 % | «0–7 casi su 10» (V8 §6 punto 7) / 0,28–0,30–0,00 e 0,997–0,71–0,00 (B8 riga 63) | i sei valori di B8 | il riassunto di V8 tace lo 0,997 della geometria con pannello da 1 m |
| Blocchi hash, scena vuota | 736 e 116 / 357 e 76 (F05 II.2 punto 4) | non usata | — |

## Una riga per cifra

| Dove (capitolo.tex) | Cifra | Fonte e paragrafo |
|---|---|---|
| §7.1 simboli | T = Δ = 1/15 s = 66,7 ms | F05 simboli; §3 punto 4 |
| §7.1 (i) | celle 1° × 0,1 m fino a 3 m; campo 87°; N_c = 87·30 = 2 610 | F05 §2, prima rappresentazione |
| §7.1 (iv) | blocchi 8³ | F05 §2, quarta |
| §7.1 (v) | profondità 6 a 10 cm e 7 a 5 cm; 8 byte per nodo | F05 §2, quinta |
| §7.1 (vi) | fasce 0,15–0,60, 0,60–1,60, 1,60–2,0 m; 30 livelli da 10 cm; 12 byte per colonna | F05 §2, sesta |
| Tab. complessità | tutte le espressioni; «nove pixel» | F05 tabella 1 |
| Lemma voxel | 6×4×3 m; 60·40·30 = 72 000; 120·80·60 = 576 000; 288 000 e 2 304 000 byte; c = 4 e 8; 160 e 1 200 blocchi | F05 lemma 1 |
| Lemma passi | n_x+n_y+n_z−2; 128 N_r e 258 N_r | F05 lemma 2 |
| dopo il lemma | 46,8 e 94,1 passi per raggio; «otto volte» | F05 lemma 2, riga del livello di prova |
| Lemma sparsa | 0,9490; 0,5543; 27; 18,9 m³; 26,3 %; 72 m³; 3,8 | F05 lemma 3 |
| §7.2 condizioni | Ryzen AI 9 HX 370; 5,16 e 3,29 GHz; quattro e otto nuclei; gcc 16.2.1, -O2; 640×480; 87°×58°; h 1,2 m; θ 15°; 6 m; 0,0025 d²; 1,2 %; tre scaffali, venti oggetti; 300 fotogrammi; 16 557 e 264 709 raggi | F05 §3 «Impianto» |
| Tab. tempi, riga polare | 10 788; 1,5 MB; 0,03/0,04; 0,42/0,55; 0,37/0,40 | F05 tabella 2 |
| Tab. tempi, riga immagine | 2 457 600; 0,51/0,52; 0,51/0,52; 0,74/0,88; 0,51/0,53 | F05 tabella 2 |
| Tab. tempi, colonne di bit | 28 800; 115 200; 1,30/1,34; 2,47/2,55; 19,5/20,0; 37,4/38,4 | F05 tabella 2 |
| Tab. tempi, tre fasce | 48 000; 192 000; 3,29/3,37; 6,23/6,41; 44,5/45,7; 85,5/97,6 | F05 tabella 2 |
| Tab. tempi, densa | 288 000; 2 304 000; 2,03/2,08; 4,21/4,35; 22,4/22,8; 44,5/49,1 | F05 tabella 2 |
| Tab. tempi, hash | 159 744–241 664; 763 904–1 515 520; 3,02/3,12; 6,71/7,45; 32,6/47,9; 72,4/76,4 | F05 tabella 2 |
| Tab. tempi, octree | 163 264–377 856; 1 004 672–2 691 008; 5,02/5,39; 11,2/12,1; 72,2/75,7; 161/171 | F05 tabella 2 |
| Figura | 0,40; 0,53; 38,4; 49,1; 76,4; 97,6; 171; 66,7 | sono i 95° percentili della colonna «k = 1, 5 cm» di F05 tabella 2 |
| Constatazione 1 | 0,03–0,6 ms; 0,5 ms + 5,9 ns; 636 µs per 108 000 punti; 2–4 ms; un raggio su 16; 45–67 ms; 44,5/49,1; 65,2/67,4; 1,49 | F05 §3 punto 1 |
| Constatazione 2 | 20 configurazioni; 1,39–1,76; 2,2–3,8; 2,3–3,9; 99 %; 33–84 %; 2 304 000 − 763 904 = 1 540 096; 1,54 MB; 117–131 % | F05 §3 punto 2 (octree: valore corretto, vedi sopra) |
| Constatazione 2 | rapporto 1,2–3,0 con profondità fino a 6 m | F05 lemma 3, ultima frase |
| Constatazione 3 | 10 cm; 19 200 raggi; 102 ms; 2,0 ms; 1,6 ms | F05 §3 punto 3 |
| Constatazione 4 | 12,8 ms; 20,4 ms; 74 %; 67,4 ms | F05 §3 punto 4 |
| dopo l'elenco | ±10 % in 29 su 32; 8 byte; 33,3 milioni di passi; 88,9 ms; 2,67 ns; 2,6 ns | F05 §3, ultimo capoverso |
| §7.3 previsione | 0,6–1,4 ms; dieci; 5,4 ms con 120; 8,2 %; 0,05 ms a oggetto; 1 500 e 150 cicli; 5,3 e 6,2 ms; 6,7 ms | F05 §5 primo capoverso |
| §7.3 previsione | 6,4 ms e 15,9 ms sotto carico | F05 II.1 riga «Previsione»; II.5 punto 4 |
| Tab. catena, riga 1 | 424×240; 162 sequenze; 9 152; 6,35; 18,6; 105,0 | F05 tabella 5 |
| Tab. catena, riga 2 | soglia da 3 a 40; 9 152; 0,95; 1,28; 7,7 | F05 tabella 5 |
| Tab. catena, riga 3 | 848×480; 48; 2,5; 2,9; 4,7 (non ricalcolata: F05 II.1) | F05 tabella 5 |
| Tab. catena, riga 4 | 640×360; 320; 81; 152; 383 | F05 tabella 5 |
| dopo la tabella | 4 su 9 152; 66 ms; 0,04 % [0,02; 0,11]; 21,3 s; 254; 152 | F05 §5 |
| dipendenza da n_T | 0,9 (0–2); 2,6 (6–10); 5,3 (11–20); 8,1 (21–40); 17,6 (41–80); 34,0 (oltre 80); 0,33 + 0,30 n_T; 1,7·10⁻⁴; 50 ms; 81 ms; mediana 2 e 17; 0,95 ms | F05 §5 «Perché il costo dipende…» (elaborazione dell'autore del fascicolo, non vagliata: F05 II.0 c) |
| riquadro | 1,49; circa 50 volte | F05 §6 punti 1 e 2 |
| Tab. alternative, tempo di volo | 60°×60°; 3·60° = 180°; sei per 360°; 26 cm a 2 m; 0,5 m a 5 klx in 8×8 | F02 §6 (testo e tabella); F06 II.3 voce `st-vl53l7cx` |
| Tab. alternative, massa | rango 1 | F01 §5, proposizione sulla massa |
| Tab. alternative, accelerazione | √6 σ_p/Δ²; 16,5 m/s² a 15 Hz; σ_p = 3 cm assunto; 0,67 m/s²; 2 s; 2,29 m e 1,18 m; 1 500 prove; 5 cm | F03 §4 |
| Tab. alternative, voxel | 1,39–1,76; 1,54 MB; 2,2–3,8; 44,5/49,1 | F05 §3 |
| Tab. alternative, «libero» ricordato | 80 505 su 146 901 (54,8 %); 830 su 897 (92,5 % [90,6; 94,1]); 5 553 su 16 851 (33,0 %); 0 | F05 tabella 3, righe 1, 2, 4 |
| Tab. alternative, tre fasce | 0,15 m; 30,6 %; 0,0 % col 5 %; 32 celle; 10 cm; 0 su 2 610; 3,4–6,4 contro 2,1–4,4 ms | F05 §4 «La mappa a tre fasce» |
| Tab. alternative, due ipotesi | 38–100 %, cinque simulatori | V9 §3, fatto sui pesi moltiplicati a ogni ciclo; SOL §4 |
| Tab. alternative, due ipotesi | 374 e 1 312 su 2 000; 1 976 e 1 987 su 2 000 | V8 §3 (prima riga della tabella); B8 riga 60 |
| Tab. alternative, selettore | 13,8 %; 57,0 %; 200 cambi in 10 minuti; 17,5–28 al minuto; quattro simulatori | V9 §1 riga del selettore; §3 fatto sull'isteresi |
| Tab. alternative, intrusione | 0,16–0,18 a 2 s; 0 a 9 cm | V9 §1 riga del massimo avvicinamento; F01 osservazione sulla probabilità d'intrusione |
| Tab. alternative, laterali | 1,4 m/s; 0,07 s; 0,5 m; 0,73 m | V9 §1 riga dei sensori laterali |
| «Mappe volumetriche» | 0,7; 0,4; 0,1192; 0,971; ⌈2,000/0,847⌉ = 3; 0,2 s; 15 Hz | F05 proposizione 2; F06 §2 osservazione 6 |
| «Mappe volumetriche» | k ≤ s f/d_max; f = 337 px; 6 m; k ≤ 2 e k ≤ 5 | F05 §4, dopo la tabella 3 |
| «Mappe volumetriche» | 2,0 m; (2,0 − h)/tan(58°/2 − θ) = 0,8/tan 14° = 3,21 m | F05 §4 «La mappa a tre fasce» |
| «Mappe volumetriche» | 0,84 → 0,88 ms; 20×20×5 m; 16·10⁶ voxel; 128 MB; 8 byte | F05 §7 |
| «Due ipotesi» | 0,8 m; 0 su 3 600; pannello 1 m | V9 §1 riga del ritaglio (c); §3 fatto sulla soglia |
| «Due ipotesi» | 0,28/0,30/0,00; 0,997/0,71/0,00; pannelli da 1 m e 2 m | B8 riga 63; geometrie: V8, «Cifre ricontate» |
| «Due ipotesi» | 39,3 % | V9 §1 riga del disegno |
| «Due ipotesi» | 76,4 % [70,7; 81,3]; 90–95 %; 100 %; 46,6 % | V9 §2, attacco sulla taratura |
| «Due ipotesi» | 28 % e 7 % a 2 e 3 s | V9 §1 riga delle due ipotesi |
| «Rete neurale» | 3 m; 0,75 s a 4 m/s; 4 cicli; 0,27 s | CL §5, requisito sul tempo della prima etichetta |
| «Rete neurale» | 9 tipi su circa 25 | CL §3 «Che cosa ne segue»; `f14-classificazione/20-inclusione/BLOCCO_CLASSIFICAZIONE.md` riga 37 |
| «Predittori appresi» | 4,8 s; cinque scenari; 0,39/0,83; 0,44/0,91; 0,32/0,60; migliore di 20 | F06 §1 «Previsione dei pedoni»; II.3 voce `scholler2020` |
| Lavori correlati, sensori | 0,4–2,1 m; 8×8 a 15 Hz; 4×4 a 60 Hz; 10 Hz; 0,72° | F06 §1 «Sensori di profondità» |
| Lavori correlati, seguimento | 260 Hz | F06 §1 «Seguimento» |
| Lavori correlati, taratura | 20 passi; 498 su 500; 95 % | F06 §1 «Previsione dei pedoni» |
| Lavori correlati, sicurezza | 1,6 m/s | F06 §1 «Sicurezza» |
| Lavori correlati, ausili | 22,9 % di 70; 5 s e 2,5 s; sei utenti; 22 volte; otto partecipanti | F06 §1 «Ausili» |
