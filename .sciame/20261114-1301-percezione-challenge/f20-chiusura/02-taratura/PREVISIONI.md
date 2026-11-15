# Previsioni (sciame-kalman, f20-chiusura/02-taratura), scritte prima di ogni prova

Ora: 2026-11-15T05:37:50+01:00 (date -Is). Nessun calcolo nuovo eseguito prima di questo file.

Metodo previsto: stessi dati, sensore simulato, divisione per mezzo e seme (20261115) di f19-volo/03-confidenza.
Interventi: (a) σ_rif² isotropa sommata al blocco di posizione di ogni regime, scelta sulla sola metà di taratura;
(b) quarto regime IMM «accelerazione longitudinale» (strappo forte lungo la velocità, debole di traverso);
(c) ricalibrazione isotonica del PIT per mezzo, fascia di τ e regime dominante alla perdita (causale), appresa
solo sulla taratura; (d) C a pesi fissati all'istante della perdita, regioni centrate su ciascun regime.

Soglie (metà di prova; copertura della regione al 90 %):
- P-T1 aerei, 1–2 s: copertura in [0,85; 0,95]. Smentita se fuori; sotto 0,80 smentita netta.
- P-T2 aerei in accelerazione (tutte le fasce insieme): copertura ≥ 0,85. Smentita se < 0,85.
- P-T3 scarto medio |prevista − osservata| sulle cinque fasce, aerei: < 0,05 regge; > 0,10 smentita; in mezzo non risolta.
- P-T4 violazioni di monotonia della C a pesi fissati (passo 0,5 s, 0–30 s, tolleranza 1e-9): 0.
- P-T5 area mediana della regione al 90 % degli aerei a 6–10 s ≤ 1,5 × quella dell'IMM attuale (f19).
Previsione mia: P-T1 regge con σ_rif fra 10 e 40 m; P-T2 incerta (n piccolo, 6–38 casi per fascia); P-T3 regge;
P-T4 regge (teorema di Anderson); P-T5 regge.
