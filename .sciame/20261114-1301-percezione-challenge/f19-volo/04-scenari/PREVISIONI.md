# PREVISIONI — f19-volo/04-scenari (sciame-scene-dinamiche)

Scritte il 2026-11-15T04:37:06+01:00, PRIMA di qualunque conto o prova sugli scenari F1–F6.

| # | Previsione | Misura | Soglia di smentita |
|---|---|---|---|
| P1 | F3 (collisione di droni a 100–150 m, 30–45 m/s): il primo frammento senza resistenza tocca terra fra 4,5 e 5,6 s; l'avviso utile deve partire entro 2 s | conto t = sqrt(2h/g) | fuori da [4,4; 5,6] s |
| P2 | F3: con vc = velocità dei droni (fino a 45 m/s) l'impronta prudente (frammenti.impronta, parametri della collisione) supera 1 km | conto | < 1 km |
| P3 | F4 (aereo 120–150 m/s, 300–600 m): l'impronta prudente supera 3 km lungo la rotta | conto | < 3 km |
| P4 | Frammenti simulati con vc dell'aereo o dei droni dentro il volume dichiarato V(tau): quota >= 0,99 (campioni frammento-istante) | eventi_volo.py --prova | < 0,99, oppure Wilson inferiore < 0,98 |
| P5 | Confidenza di posizione in forma chiusa C(tau) = P(chi2_3 <= g^2/sigma^2(tau)) coincide con Monte Carlo (2·10^5 campioni) entro 0,005 per tau in [0, 5] s | eventi_volo.py --conti | scarto > 0,005 |
| P6 | F5: con 3 s di cecità totale degli ottici e due tracce veloci (80 m/s) che si incrociano, la probabilità di scambio d'identità alla riacquisizione dal solo radar è fra 0,05 e 0,4 nel caso peggiore (distanza alla riacquisizione 50 m) | Phi(-d/(sqrt2 sigma)) | fuori da [0,05; 0,4] |
| P7 | F6: nessun falso evento con due aerei a 1000 ft / 3 NM | analisi della regola d'innesco | un evento dichiarato |

Stati attesi: P1–P3 calcolato; P4 simulato; P5 calcolato e controllato in simulazione; P6 calcolato (ipotesi sui parametri); P7 ipotesi (nessuna prova in 35 minuti).
