# Previsioni dell'arbitro (triage f8) — scritte prima di leggere le consegne

Ora: 2026-11-14T15:42:54+01:00. A questo punto ho letto solo la traccia, il contratto f8 e l'elenco dei file (`ls`).

- **P-arb-1 (canarini).** Misura: `grep -c` dei due canarini in tutti i file delle nove cartelle. Previsione: ogni CONSEGNA.md comincia con il canarino della propria corsia; zero occorrenze del canarino dell'altra corsia. Smentita: una prima riga diversa, o almeno un'occorrenza incrociata.
- **P-arb-2 (Q3, il «previsto»).** Previsione: almeno 6 ruoli su 9 dichiarano «non rispettato» il controllo 1 (continuità) per la regola attuale del «previsto» (0,4–0,7 s poi «perso»). Smentita: meno di 6, o un ruolo che la dichiara rispettata con una misura.
- **P-arb-3 (cifre).** Previsione: almeno una cifra riportata in una CONSEGNA.md non torna dal file dei risultati accanto (differenza oltre l'arrotondamento). Smentita: tutte le cifre che ricontrollo (almeno 20) tornano.
- **P-arb-4 (contraddizioni).** Previsione: almeno 4 contraddizioni vere fra ruoli (enunciati incompatibili con numeri), fra cui «particelle o deterministico» e «gonfiamento o conforme». Smentita: meno di 4.
- **P-arb-5 (comportamento peggiore).** Previsione: in almeno 3 consegne indipendenti il comportamento coperto peggio al 90 % è «torna indietro» o «sosta», con copertura sotto 0,80 per il filtro lasciato correre a orizzonte ≥ 2 s. Smentita: il peggiore è un altro in maggioranza, o la copertura è ≥ 0,80.

---

## Ripresa del lavoro — 2026-11-14T15:53:41+01:00

Nota di onestà. Le previsioni P-arb-1…5 qui sopra (ore 15:42:54) erano già in questa cartella quando ho ripreso il compito: le adotto come sono. Il controllo dei canarini (P-arb-1) l'ho lanciato alle 15:48 circa, dopo quell'ora. Le previsioni qui sotto sono scritte **dopo** aver letto le nove consegne e i loro file, e **prima** del mio script di riconteggio (`riconta_arbitro.py`) e, soprattutto, prima del banco di prova indipendente (`11-misure`), che non eseguo io: sono cieche solo rispetto a quel banco.

- **P-arb-6 (C-EST, attacco 1, criterio alla lettera).** Misura: passaggi «sosta improvvisa a metà pannello» in cui almeno un ciclo di «previsto» ha una cella su spazio visto libero. Previsione: con il criterio stretto (qualunque cella libera, senza fascia) C-EST è rigettata in più del 50 % dei passaggi (celle di bordo); con il criterio «oltre la fascia di 0,20 m» 0 cicli. Smentita: criterio stretto pulito in almeno il 95 % dei passaggi, oppure almeno un ciclo oltre la fascia.
- **P-arb-7 (C-EST, la soglia 0,8 m).** Alla scala della demo (ombra di circa 1,4 m²) σ_eff resta ≤ 0,8 m per tutta la sosta in almeno il 95 % dei passaggi (la soglia non scatta mai: nessun «perso», ma una dicitura «±σ» che non è un livello tarato); con l'ombra larga (pannello di 2 m, soggetto a 4 m) «perso» scatta entro 3 s in più del 50 % delle soste lunghe, cioè C-EST lascia un vuoto di stima. Smentita: una delle due metà rovesciata.
- **P-arb-8 (C-EST, attacco 5).** Il raggio «±σ_eff» letto come 1 σ contiene l'errore vero alla ricomparsa in meno del 70 % dei casi sulla miscela; l'ellisse al 95 % della miscela ritagliata contiene almeno il 90 % di chi prosegue e meno del 90 % di chi torna indietro. Smentita: l'ellisse al 95 % tiene ≥ 90 % in ogni comportamento che ricompare con n ≥ 30.
- **P-arb-9 (le candidate in testa).** Almeno una fra C-001 (particelle con sosta) e C-004 (fronte + scia) tiene la regione al 90 % ≥ 0,85 in ogni cella «sul percorso» (prosegue, rallenta, sosta, sosta lunga, torna) con n ≥ 30, nelle due geometrie di prova, con area media ≤ 0,60 dell'ombra nella geometria larga; nessuna candidata tiene 0,85 su «esce dal lato lontano» a τ ≥ 2 s con la regione al 90 % (lo tiene solo il limite esterno, al 100 %). Smentita: nessuna passa sul percorso, oppure una passa sul lato lontano.
- **P-arb-10 (il ripiego più semplice).** Il disco tarato sul comportamento peggiore (C-005) tiene ≥ 0,85 nelle celle tarate, ma dalla fascia τ = 1,5 s in poi occupa almeno l'80 % dell'ombra alla scala della demo. Smentita: sotto l'80 % dell'ombra a 2 s con copertura ≥ 0,85.
- **P-arb-11 (linea di base).** La regola attuale del nucleo, riscritta dal testo, emette una stima in meno del 70 % dei cicli senza osservazione in ogni comportamento alla scala della demo. Smentita: almeno un comportamento ≥ 70 %.
- **P-arb-12 (soglie del protocollo, conto binomiale).** Con n = 400 per cella e soglia «osservato ≥ 0,85», una regione che copre davvero 0,90 è bocciata per errore in meno dell'1 % dei casi e una che copre 0,80 è promossa in meno dell'1 %. Smentita: uno dei due errori ≥ 1 %.

## Esiti — 2026-11-14T16:00:16+01:00

- **P-arb-1: regge.** Nove prime righe giuste, 0 occorrenze incrociate (`riconta_arbitro.txt`, §1; controllo lanciato dopo le 15:42).
- **P-arb-2: regge.** Nove ruoli su nove dichiarano «non rispettato» il controllo 1 per la regola attuale (tabelle Q3 delle nove consegne).
- **P-arb-3: smentita.** 51 cifre su 51 tornano dai file dei risultati (`riconta_arbitro.txt`, §2); in più la cella «12 su 12 fra 96 e 100» del creativo.
- **P-arb-4: regge.** Undici contraddizioni vere (K-201…K-211) e una apparente (K-212); fra le vere «particelle o deterministico» (K-205) e la taratura (K-207).
- **P-arb-5: regge.** Chi torna è il comportamento coperto peggio al 90 % a 2 s per il filtro lasciato correre in statistico (0,536), kalman (0,765), ricercatore (0,291), rovesciatore (44,4 %); notato dopo: dove «esce dal lato lontano» è simulato, è coperto altrettanto male (0,33–0,51).
- **P-arb-12: regge.** n = 400, soglia 340: 0,06 % e 0,61 % (`riconta_arbitro.txt`, §3).
- **P-arb-6…11: non risolte.** Le decide il banco di `11-misure`.
