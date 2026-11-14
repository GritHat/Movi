# Previsioni di `sciame-slam` — scritte PRIMA della simulazione `bilancio_posa.py`

Ora di scrittura (`date -Is`): 2026-11-14T14:41:38+01:00. Lo script a quest'ora non esiste ancora.

Modello comune (ipotesi mie): 15 Hz; gruppo fermo a distanza r; rumore del centro per asse sigma(z) = 0,00375·z² m
(curva nominale del nucleo: 1,5 cm a 2 m, 3,4 cm a 3 m) per la camera; 5 cm a 10 e a 30 m per un LiDAR (ipotesi,
non verificata). Regola «mobile» del nucleo: due medie di 3 fotogrammi distanti al più 1 s, soglia 5·sigma·radice(2)
per asse. Errore di posa = spostamento apparente r·d_psi + d_t nel riferimento d'odometria.

| # | Misura | Previsione | Soglia di smentita |
|---|---|---|---|
| P1 | errore d'imbardata relativo su 1 s che porta al 10 % i falsi «mobile» su un gruppo fermo, regola NON modificata | 2,6° a 2 m; 1,7° a 10 m; 0,57° a 30 m (conto: 6·sigma/r) | valore misurato fuori da ±25 % |
| P2 | regola con la soglia allargata dalla sigma di posa in quadratura, sigma onesta | falsi ≤ 1 % a ogni errore provato; ma a 10 m con 1°/s un pedone a 1,2 m/s è visto «mobile» in meno del 50 % delle finestre | falsi > 1 %, oppure pedone visto ≥ 50 % |
| P3 | ritardo posa–profondità tollerato dalla regola «mobile» (falsi ≤ 10 %) in una rotazione di 30° a 30°/s con partenza e arresto bruschi | 2 m: circa 80 ms (60–100); 10 m: circa 57 ms (40–70); 30 m: circa 19 ms (12–25) | fuori dall'intervallo |
| P4 | errore di beccheggio che rende «occupato» il 10 % delle celle di suolo a distanza r (quota 0,07 m), sensore a 1,2 m | 1,6–1,9° a 2 m; 1,0–1,3° a 3 m; 0,3–0,4° a 10 m; 0,10–0,13° a 30 m; il 50 % a asin(0,07/r): 2,0° / 1,34° / 0,40° / 0,134° | fuori dall'intervallo |
| P5 | scostamento non modellato e (in unità della sigma per asse dell'area prevista) che porta la copertura del cerchio al 95 % da 0,92 a 0,90, e a 0,85 | 0,90 a e ≈ 0,4 sigma (0,25–0,55); 0,85 a e ≈ 0,7 sigma (0,55–0,9) | fuori dall'intervallo |
| P6 | solo giroscopio, bias residuo 0,1°/s e fattore di scala 1 %, rotazione di 30° in 1 s, sincronia perfetta | falsi «mobile» ≤ 1 % a 2 e 3 m; ≤ 10 % a 30 m | falsi oltre |
| P7 | giroscopio NON tarato (bias 1°/s, la cifra di F-008), finestra di 1 s | a 2–3 m falsi ≤ 10 % (1° < 2,6°); a 30 m falsi > 50 % | il contrario |

Esiti possibili: regge, smentita, non risolta. Ciò che noto dopo va in MOTO_PROPRIO.md sotto «notato dopo».

## Aggiunta per il profilo indossato (secondo addendum), scritta alle 2026-11-14T14:42:21+01:00, sempre prima dello script

Modello (ipotesi mie): persona che cammina a 1,2 m/s; testa ±30° a 0,5 Hz (la cifra di F-008; velocità di punta 94°/s)
oppure busto ±8° a 1 Hz; beccheggio dell'andatura ±3° a 2 Hz; rimbalzo verticale ±2,5 cm a 2 Hz.

| # | Misura | Previsione | Soglia di smentita |
|---|---|---|---|
| P8 | indossato, imbardata dal giroscopio ma traslazione NON compensata, muro fermo a 2–3 m | «mobile» falso ≥ 95 % (1,2 m in 1 s contro una soglia di 0,1–0,25 m) | < 95 % |
| P9 | indossato con odometria visuale-inerziale (1 % della distanza, 0,1°/s), sincronia perfetta | falsi ≤ 1 % a 2 e 3 m | > 1 % |
| P10 | ritardo posa–profondità tollerato (falsi ≤ 10 %) con la testa a ±30°, 0,5 Hz | 2 m: 14 ms (10–18); 3 m: 21 ms (15–26) | fuori dall'intervallo |
| P11 | suolo a 3 m con rimbalzo di ±2,5 cm non compensato: errore di beccheggio che dà il 10 % di celle «occupato» | circa 0,7° (0,5–0,9), contro 1,0–1,3° senza rimbalzo | fuori dall'intervallo |
