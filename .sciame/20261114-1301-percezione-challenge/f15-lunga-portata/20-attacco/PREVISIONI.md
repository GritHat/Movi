# Previsioni dell'attacco (sciame-avversario, f15/20-attacco)

Scritte alle **2026-11-15T01:23:44+01:00** (`date -Is`), prima di ogni programma mio. Esiti: regge / smentita / non risolta.

| # | Attacco | Previsione (l'attacco riesce se...) | Soglia di smentita della previsione |
|---|---|---|---|
| X1 | Drone in volo stazionario che scatta (a = 20–25 m/s², v 45 m/s, ipotesi di un drone da corsa) dietro un ostacolo, scenario `aeroporto_e_droni` | esce dall'insieme di possibile presenza a τ = 2–5 s | la verità resta dentro a ogni τ in [0,5; 30] s |
| X2 | Aereo in decollo a 160–205 m/s (velocità reali di 12-traiettorie), inviluppo attuale 90 m/s | fuori dall'insieme a τ ≥ 2 s | dentro a ogni τ |
| X3 | Distanza d'avviso dell'operatore di sito ricalcolata con v_max 210 m/s (kalman-1) | non tempestivo: d_avv > 2,36 km (portata del «libero» del multirotore) | d_avv ≤ 2,36 km |
| X4 | Sezione radar correlata fra passate (aspetto fisso: bersaglio tenuto per 5 passate, non Swerling 1 da passata a passata) | P(5 passate tutte mancate) alla portata del «libero» > 0,05, cioè ≥ 5 volte il rischio dichiarato 0,01 | ≤ 0,02 |
| X5 | Edificio non in pianta: il mezzo dietro non dà ritorni | la cella del mezzo è «libera» dopo 5 passate | la cella non è «libera» |
| X6 | Scenario `strada` con un pedone o un drone (classi non ammesse) | «libero» dichiarato su celle dove Pd cumulata del pedone (0,5 m²) < 0,99 | nessuna cella del genere entro 300 m |
| X7 | Simulatore al limite: S1 con falsi ritorni del radar 4D a 1 per quadro (valore del JSON) e A1 con IRIS a 5 falsi per giro (uccelli, ipotesi) e sezione radar del drone dimezzata; modo prudente, N = 30 | «fuori avviso» nel modo prudente sale almeno al doppio rispetto ai valori nominali (S1 min 0,050; A1 min 0,007) | rapporto < 1,5 |
| X8 | Otto valori di scheda riaperti | almeno 1 su 8 non coincide con la fonte o non si trova nella pagina | 8 su 8 coincidenti |
| X9 | Frasi: documenti della fase con «rileva X a N km» senza sezione radar, o lessico d'ingaggio | almeno 1 occorrenza in proposta/allegato | 0 occorrenze |
