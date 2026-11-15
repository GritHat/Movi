# Previsioni e soglie (sciame-kalman, f19-volo/03-confidenza)

Scritte il 2026-11-15T04:38:08+01:00, PRIMA di eseguire qualunque prova. Nessun risultato visto finora in questa cartella.

## P1 — esattezza della formula nel modello gaussiano (calcolato)
Misura: confidenza(τ, regione) per gaussiana contro (a) le forme chiuse (disco centrato 2D: 1−exp(−r²/2σ²); sfera centrata 3D: erf(k/√2) − √(2/π) k e^{−k²/2}) e (b) Monte Carlo 10^6 campioni (seme 20261115) su ellissi/sfere fuori centro e anisotrope.
Soglia di smentita: scarto > 1e-5 dalle forme chiuse, oppure fuori dall'intervallo Monte Carlo al 99,9 % in uno qualunque di 20 casi casuali.

## P2 — tempo t_C dalla cubica (calcolato)
Misura: τ trovato dalla radice della cubica contro ricerca numerica di C(τ)=α. Smentita: scarto > 1e-6 s.

## P3 — affidabilità su dati reali, velocità costante (CV), aerei veloci (v mediana > 60 m/s) e droni, metà di prova divisa per mezzo
Misura: frequenza osservata di «verità dentro la regione al livello α» (α = 0,5; 0,68; 0,9; 0,95; 0,99), per fasce di τ (1–2, 3–5, 6–10, 11–20, 21–30 s), Wilson 95 %.
Previsione: con q tarato sulla metà di taratura, per α = 0,9 l'osservato sta in [0,80; 0,97] in almeno 4 fasce su 5 per gli aerei veloci; per i droni la stessa cosa in almeno 3 su 5. Soglia di smentita: meno fasce di così, o un intervallo di Wilson tutto sotto 0,75 in una fascia con ≥ 50 casi.

## P4 — IMM contro CV (dati pubblici, rumore di sensore simulato)
Previsione: sugli aerei veloci, per τ in 11–30 s, l'IMM (CV + virata coordinata con tasso stimato + accelerazione) riduce l'errore mediano del punto di almeno il 10 % rispetto al CV e l'area della regione al 90 % di almeno il 10 % a copertura non peggiore di 0,03. Smentita: riduzione < 10 % su entrambe le misure, o copertura al 90 % dell'IMM più bassa di quella del CV di oltre 0,03.
Per i droni non faccio una previsione direzionale (moto lento rispetto al rumore del radar a 1500 m): esito descrittivo.

## P5 — dove la formula sbaglia
Previsione: lo scarto più grande fra previsto e osservato sarà nelle fasce lunghe (21–30 s) e nelle virate; l'IMM a miscela sarà meno ottimista del CV in virata. Smentita: lo scarto massimo |osservato−α| in una fascia corta (1–5 s) superiore a quello delle fasce lunghe per entrambi i filtri.
