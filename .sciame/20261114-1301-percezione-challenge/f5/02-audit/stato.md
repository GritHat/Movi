# stato — audit V2 (sciame-rovesciatore, f5/02-audit)

Avvio lettura: 2026-11-14T14:39:50+01:00. Limite: 25 minuti.

## Previsioni scritte PRIMA dei conti e delle ricerche (2026-11-14T14:43:13+01:00)

- P1 (eta' del «libero» con la latenza): sommando ai 0,13 s dell'invariante 1 i 155 ms di latenza nota (VERIFICA par. 3c), lo spostamento a v_max = 2,5 m/s supera la fascia di 0,40 m. Smentita se resta <= 0,40 m.
- P2 (buchi persistenti): con l'1 % di celle di suolo sempre non valide, piu' della meta' dei settori da 10 gradi (zona 1,24-3 m) contiene almeno un «buco» permanente. Smentita se < 50 %.
- P3 (altezza del pannello): per nascondere una persona di 1,8 m a 2,3 m da una camera a 1,2 m, un pannello a 1,15 m deve essere alto almeno 1,4 m; nessun file della convocazione ne fissa l'altezza. Smentita se un file la fissa o se bastano < 1,2 m.
- P4 (ombra propria): la distanza fra il centro misurato di una persona e la prima cella della sua stessa ombra e' < 0,40 m, quindi il ramo «campo aperto» di B5 alla lettera non scatta mai. Smentita se la distanza supera 0,40 m o se un file esclude l'ombra propria.
- P5 (banda di occlusione stereo): con base 95 mm (D455), pannello a 1,15 m e attore a 2,3 m, la banda senza profondita' accanto all'ombra e' fra 5 e 15 cm. Smentita se < 2 cm.
- P6 (quota del suolo): con la curva pessimista, a 3 m piu' del 1 % dei pixel di suolo supera per rumore la soglia di 0,07 m. Smentita se < 0,1 %.
- P7 (simulatori): nessuno script di f4 genera pixel di profondita'; «libero» vi e' assegnato dalla geometria vera. Smentita se uno script deriva «libero» da una profondita' simulata con errori.
- P8 (fonte): la documentazione del costruttore dice che il filtro temporale con persistenza e il riempimento dei buchi sostituiscono i pixel non validi con valori passati o vicini. Esito possibile: non trovata nel tempo.
- P9 (catena critica): i blocchi in dipendenza seriale B1-B2-B3-B4-B5-B7-B8 sommano piu' di 24 ore. Smentita se <= 24.

## Esiti (2026-11-14T14:46:22+01:00)
P1 regge (0,72 m). P2 regge (83,6 %). P3 regge (1,45-1,50 m; nessun file fissa l'altezza, per grep). P4 regge (0,1 m; nessun file esclude l'ombra propria, per grep). P5 regge (9,5 cm; 5,0 con base 50 mm). P6 regge con la curva pessimista (3,6 %), zero con la nominale. P7 regge per grep su f4 (a03_priorita.py riga 35; comune_f4.py osservabile). P8 regge sul riassunto della ricerca (pagina non aperta). P9 regge (38 ore).
Consegnato: AUDIT.md. Secondo addendum dell'utente letto alle 14:43 e integrato (ipotesi 12, par. 2).
