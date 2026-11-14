# CIFRE del capitolo 3 (map) — una riga per cifra, con il file e il paragrafo d'origine

Sigle dei file (tutti sotto `.sciame/20261114-1301-percezione-challenge/`):
**F01** `f13-allegato/01-dimostrazioni/FASCICOLO_DIMOSTRAZIONI.md` · **F05** `f13-allegato/05-costo/FASCICOLO_RAPPRESENTAZIONI_E_COSTO.md` · **F06** `f13-allegato/06-bibliografia/FASCICOLO_BIBLIOGRAFIA.md` · **DISC** `f13-allegato/DISCORDANZE_DEI_FASCICOLI.md` · **LC** `f12-integrazione/03-libero/LIBERO_DELLA_CELLA.md` · **SOL** `f12-integrazione/20-finale/SOLUZIONE_V3.md` · **AT** `f12-integrazione/10-attacco/ATTACCO_V3.md` · **CP** `f12-integrazione/13-statistica/CONTROLLO_PROVE.md` · **VD** `f10-dati/23-verdetto/VERDETTO_DATI.md` · **CI** `f12-integrazione/07-controprova-identita/CONTROPROVA_IDENTITA.md` · **SCH** `f12-integrazione/22-schermo-finale/SCHERMO_E_DEMO.md`.

| Dove nel capitolo | Cifra | Origine |
|---|---|---|
| 3.1 | celle 1° × 0,1 m fino a 3 m; campo 87°; N_c = 87·30 = 2 610 | F05 §2 (griglia polare); SOL §1.2 parametri |
| 3.1 | h = 1,2 m, θ = 15° | SOL §1.1 parametri; LC §1 |
| 3.1 | camera simulata 320 × 240; circa 12 pixel per cella a 2 m e 4 a 3 m | LC §1 e §2 («Perché cadono») |
| Def. stati | occupato: almeno 3 pixel validi a quota 0,07–2,0 m | SOL §1.2 riga 1; LC §3 riga 1 |
| eq. margine | m(z) = 0,03 + 3·k·z² | LC §1; SOL §1.2 riga 3 |
| Def. regola | metà dell'impronta (almeno 1); 8 celle vicine con n > 0 | SOL §1.2 righe 4–5; LC §3 |
| Parametri | k = 0,004 nominale, 0,0100 al limite; inclinazione entro 0,5°; memoria 0 fotogrammi | SOL §1.2 parametri; LC §3 |
| Lemma posa | a 3 m: 0,5° → 3·0,00873 = 2,6 cm; 3 cm e 1° → 8,2 cm; 5 cm e 2° → 15,5 cm | F01 §2, Lemma 1 |
| Lemma posa | 114 su 200 e 162 su 200 senza margine; 0 su 200 col margine teorico; 1 su 200 con 10 cm dove ne servono 15,5 | F01 §2, Lemma 1 |
| 3.3 fine | oggetto di 10 cm sopra 0,07 m se errore < 0,69° a 2,5 m e < 0,57° a 3 m; con 1°: 5,6 e 4,8 cm | SOL §1.1 «Stato» |
| Oss. (iii) | 150 fotogrammi, finestra 0,20 s; 537 su 88 418; margine 0,33 m (1,4 m/s) → 0 errori, 0,4 % del libero | F01 §2 «Che cosa la proposizione non dice» |
| 3.4 insieme | 87° × 58°; griglia 87 × 30; 10 scene; 2 valori di k; 5 regimi (5 %, 30 %, chiazze 20 × 20 px); errori 0, ±0,5°, ±1°; 500 condizioni × 30 = 15 000 fotogrammi, due volte | LC §1 |
| Tab. regole | 7 200 fotogrammi = 240 condizioni (8 scene × 2 k × 5 regimi × 3 errori) | LC §2, intestazione della tabella |
| Tab. regole | 932 (899); 1 732 (1 742); 163 (179); 98 (126); 6 (9); 0 (0) | LC §2, colonna «Fotogrammi con violazione» |
| Tab. regole | distanze 1,3 / 1,3 / 1,3 / 3,0 / 3,0 / 3,0 m, uguali per i due k | LC §2, colonna della soglia d'uscita |
| 3.4 sicurezza | 15 648 celle libere dentro un corpo (punto a 0,20 m) | LC §0 punto 1 e §2 |
| 3.4 sicurezza | 0 su 9 000 fotogrammi, 10 scene, 300 condizioni, due generazioni | LC §2 («0 su 9 000 + 9 000»); SOL §1.2 «Stato»; CP §3 |
| 3.4 sicurezza | corpo che non rimanda segnale: 0 su 900; regola a un pixel 900 su 900 | LC §0 punto 3 e §2 «Scene in più» |
| 3.4 sicurezza | scatola da 10 cm a 2,6–2,9 m: 0 su 900 | LC §2 «Scene in più» |
| 3.4 sicurezza | seconda esecuzione: 0 su 9 000 (0 su 7 200, 0 su 900, 0 su 900) | AT riga P1 e «Dove ho cercato senza rompere» |
| 3.4 sicurezza | limite superiore al 95 %: 0 su 300 → 1,3 %; 0 su 10 → 28 % | CP §3 |
| Tab. resa | 89,3 / 89,3 / 86,0 / 85,0 / 64,1 % (metà impronta) e 86,8 / 86,8 / 62,6 / 78,3 / 45,4 % (regola adottata) | LC §2 «Resa del libero vero» |
| Tab. resa | distanze 3,0 m (5 % sparsi), 1,5 m (30 % sparsi), 3,0 m (5 % chiazze), 1,4 m (30 % chiazze) | LC §2 riga della soglia (5 % sparsi) e «Distanza per settore» |
| 3.4 prezzo | guardia: 2,5 punti, 23 punti, 19 punti | LC §2 «Prezzo della guardia» |
| 3.4 prezzo | 6–7 cambi al secondo con buchi fitti; 0,01 col 5 % sparso | LC §3 («Nel ritaglio») e §2 «Sfarfallio» |
| 3.4 fine | «sconosciuto» nel 43–47 % dei settori; 1,4–1,5 m | LC §2 «Distanza per settore» |
| 3.4 fine | k 0,0100 a +0,5°: 80,6 % e 2,4 m; a +1°: 33,7 % e 1,6 m; k 0,004 a −1°: 82,4 % e 2,3 m | LC §2 «Inclinazione» |
| Contr. inclinazione | −1°: 150 fotogrammi su 300, 503 celle; 146 su 300 nella seconda esecuzione; ±1° sulle 8 scene di base: 0 su 4 800 | LC §2 «Inclinazione»; AT riga P2 |
| Contr. vetro | lastra 1 × 2 m a 2,0 m: 654 su 800; a 1,5 m: 600 su 800 | F01 §2 «Fuori dalle ipotesi»; DISC (costo, punto 5) |
| Contr. muto | palo di 3 cm a 2,05 m: piede «libero» 6 fotogrammi su 6 | VD tabella dei controesempi, riga dell'ostacolo senza ritorno |
| Altri limiti | ostacolo sospeso: 374 celle | LC §3 «Nell'uscita»; SOL §1.2 |
| Altri limiti | barra di 1 cm a 0,8 m di quota e 2,0 m: 4,7–7,3 % (7–11 su 150); 2 cm o più: 0 su 150 | AT riga P4 |
| Altri limiti | oggetto alto 0,35 m a 0,5–0,8 m o 0,60 m a 0,3–0,6 m: 0 pixel, d = 3,0 m | AT riga P3; SOL §1.2 |
| 3.6 | 0 su 2 907 032 celle·fotogramma; 135 sequenze; tre forme d'ombra; 0 su 131, limite 2,9 %; tre camere | VD §1 riga sul «libero» e «Cifre ricontate» (131 + 4 con i filtri) |
| 3.6 | regola precedente con memoria di tre fotogrammi | SOL §1.2 «Controesempi e limiti» |
| 3.6 | 5 celle·fotogramma su 3 992 186, 381 sequenze; 4 al limite (scatola a 2 m), 1 al nominale (scatola a 2,8 m) | CI righe 9 e 50 |
| 3.6 | +1°, 10 cm a 2,55 m: 7 celle su 7 (scena a mano); +2,5°, scatola 15 cm a 2 m: 9 fotogrammi su 10 | VD tabella dei controesempi, riga della posa |
| 3.6 | filtri accesi, sensore coperto: 989–995 celle per altri 3 fotogrammi | VD «Le nove condizioni», 1; SOL §1.1 |
| 3.6 | gruppi di 6 fotogrammi: 50,8 % e 3,0 m; 15,9 % e 2,2 m; 21 % fuori margine; 0,1 % (pavimento lucido) | LC §2 «Fotogrammi…», tabella e punti (a)–(b) |
| 3.6 | sequenza pubblica: 0,0–0,1 %; 37 % dei pixel legge più vicino | LC §2, tabella e punto (c) |
| Contr. memoria | 3 fotogrammi; 2Δ = 0,133 s a 15 Hz; 0,33 m a 2,5 m/s; 1 186 punti; 87 su 87; 58 su 90 (0,64; 0,54–0,74) | F01 §2, Osservazione 1 |
| Prop. log-odds | 0,7; 0,4; 0,1192; 0,971; ln(0,7/0,3) = 0,847; −2,000; 3 colpi; 0,2 s a 15 Hz | F05 §4, Proposizione 2; F06 §2 Oss. 6 |
| Tab. varianti | 80 505 su 146 901 (54,8 %); 830 su 897 (92,5 % [90,6; 94,1]); 132 su 134 (98,5 % [94,7; 99,6]); 5 553 su 16 851 (33,0 %), 40 scatole, 14 fotogrammi; 71 006 punti, 147 su 147; 2 096 su 6 648 (31,5 %), 4 × 4, 5 cm; 44 su 87 (50,6 % [40,3; 60,8]) | F05 §4, Tabella 3 |
| 3.7 lettura | intorno 3 × 3; 5 cm; 0 su 321 [0; 1,18]; 0 su 900 [0; 0,43]; 10 condizioni × 90; 208 000 punti a 5 cm | F05 §4, Definizione 1 e «Contro queste…» |
| 3.7 rese | 97,1 % (88,4–91,8 %); 61,1 % (55,7–57,9 %) e 87,7 % (79,4–83,1 %); 3,6 % e 8,0 % | F05 §4, Tabella 4 |
| 3.8 | settori di 5 azimut; da 1,3 m; una cella = 0,1 m; d ≤ 2,6 m = portata − 0,40 m | SOL §1.2 riga 7, §1.10, «Convenzioni» (w = 0,40 m); LC §3 |
| 3.8 | 9 settori su 17; 8 laterali «sconosciuto» | LC §3 «Nell'uscita»; SOL §1.10; SCH riga del livello per settore |

## Cifre contestate: che cosa ho scelto

1. **Rese della lettura per punto** (DISC, costo, punto 2): tenute distinte. A un fotogramma 61,1 % e 3,6 %; con conferma 87,7 % e 8,0 %; 97,1 % è di entrambe senza pixel non validi. Nessuna di queste è la resa della regola della cella (86,8 %…45,4 %, LC).
2. **Vetro** (DISC, costo, punto 5): 654 su 800 a 2,0 m e 600 su 800 a 1,5 m, entrambe con la distanza.
3. **Scatola a −1°**: 150 su 300 (LC, primo lancio), 145 (LC, semi nuovi), 146 (AT). Ho scritto 150 e 146, ciascuna con la sua esecuzione; il 145 e le celle «455» di LC restano fuori.
4. **«Libero» nell'ombra su profondità simulata**: 0 su 2 907 032 (VD) contro 5 su 3 992 186 (CI). Nessun file decide: riportate entrambe, con la condizione (regola precedente con memoria; non risolto se sia la regola o il bordo della maschera). Lo «0 su 3 149 352» con la seconda definizione (VD) non è riportato.
5. **«2 su 10 000» per fotogramma** (LC §2): non scritto; CP §3 lo esclude (fotogrammi non indipendenti). Scritto il limite per condizione (1,3 %) e per scena (28 %).
6. **Soglia di 2,7 m**: non scritta come prestazione (CP: «2,7 m» non si può scrivere su un sensore); scritti 3,0 m (modello ideale), 2,4 m (k al limite, +0,5°), 2,2 m (modello al limite su profondità simulata).
