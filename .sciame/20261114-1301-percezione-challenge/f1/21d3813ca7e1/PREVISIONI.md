# PREVISIONI di sciame-kalman (f1, corsia A)

Scritte alle **2026-11-14T13:06:28+01:00**, prima di scrivere ed eseguire `sim_kalman.py` (nessun numero della simulazione era noto).
Prova: simulazione Monte Carlo in Python puro (numpy non è installato), semi fissati, al più 5 minuti su CPU.
Indipendenza dichiarata: la verità simulata NON è il modello del filtro (pedone con velocità desiderata che salta a
istanti di Poisson e rilassamento del primo ordine, tau = 0,4 s, velocità al più 2 m/s); condivide con il filtro
l'autore, il rumore di misura gaussiano isotropo e l'assenza di errori di associazione. Vale quindi solo per i difetti
del modello di moto e della taratura, non per sensore reale, associazione, sincronizzazione.
Riferimento: 15 Hz, sigma_z = 5 cm per asse, ostacolo sul piano del suolo (2D).

## kalman-1 (ordine della catena, moto proprio, prova «mobile» sulla covarianza)

- **Pv-1a** Ostacolo fermo, portatore che cammina a 1,2 m/s e ruota la testa di ±30° a 0,5 Hz. Filtro nel riferimento
  del sensore senza compensazione: errore RMS sulla distanza di passaggio prevista (CPA) > 1,0 m e ostacolo dichiarato
  «mobile» > 90% del tempo. **Smentita** se CPA RMS < 0,5 m (il giroscopio non servirebbe).
- **Pv-1b** Con la sola rotazione compensata dal giroscopio (rumore 0,5 gradi/s, bias 1 grado/s): CPA RMS < 0,3 m; ma
  l'ostacolo fermo risulta «mobile» > 90% del tempo (velocità relativa = meno la velocità del portatore).
  **Smentita** se CPA RMS > 0,5 m.
- **Pv-1c** Con rotazione e traslazione compensate (velocità del portatore nota con errore del 10%): «mobile»
  dichiarato < 10% del tempo con la prova chi quadrato al 99% sulla velocità stimata (v' Pv^-1 v > 9,21).
  **Smentita** se > 25%.
- **Pv-1d** Un pedone a 1,2 m/s è dichiarato «mobile» dalla stessa prova in un tempo mediano < 1,0 s dall'apertura
  della traccia. **Smentita** se > 1,5 s.
- **Pv-5** Velocità: sigma_v dichiarata di regime fra 0,10 e 0,50 m/s per asse; errore RMS reale entro ±30% della
  dichiarata. **Smentita** se fuori.
- **Pv-6** Massa: la matrice d'informazione di Fisher di (F, m) da misure di posizione di un punto materiale con forza
  ignota ha rango 1 (|det|/traccia^2 < 1e-12): massa non osservabile. È un risultato analitico; il calcolo è solo
  un controllo.

## kalman-2 (la covarianza predetta come segnale R4/R6; copertura alla ricomparsa)

- **Pv-2a** Velocità quasi costante, q tarato sul NIS (media più vicina a 2) su semi di taratura separati: la verità
  cade nel cerchio al 95% del filtro alla ricomparsa dopo 0,5 / 1 / 2 / 3 s di occlusione con frequenza in
  [0,88; 0,99] per ogni durata. **Smentita** se una durata scende sotto 0,85 (la covarianza non dice il vero:
  serve un altro modello o un margine). Esito «non risolto» se fra 0,85 e 0,88.
- **Pv-2b** Con q «ottimista» (0,01 m^2/s^3, traccia liscia): copertura a 2 s < 0,70. **Smentita** se >= 0,85.
- **Pv-3** Con q tarato il raggio al 95% supera 1,5 m dopo un'occlusione fra 1,0 e 2,5 s: l'orizzonte utile della
  previsione è di 1–2 s, poi la traccia va dichiarata «persa». **Smentita** se fuori da [0,7; 3,5] s.
- **Pv-4** Accelerazione costante (jerk tarato sul NIS): errore RMS dell'accelerazione stimata >= 0,6 volte il
  valore efficace dell'accelerazione vera (non utilmente stimabile), e l'errore RMS di previsione a 2 s di occlusione
  è >= 0,9 volte quello del modello a velocità costante (non migliora). **Smentita** se RMSE(a) < 0,4 volte, oppure
  se l'errore a 2 s è < 0,9 volte.

Esiti possibili per ciascuna: regge, smentita, non risolta.

## Esiti (aggiunti alle 2026-11-14T13:10:33+01:00, dopo la prova; il testo sopra non è stato modificato)

Prova eseguita alle 2026-11-14T13:08:34+01:00, uscita in `risultati.txt`.

| Previsione | Soglia di smentita | Esito misurato | Stato |
|---|---|---|---|
| Pv-1a | CPA RMS < 0,5 m | 1,49 m; «mobile» 100% | regge |
| Pv-1b | CPA RMS > 0,5 m | 0,25 m; «mobile» 100% | regge |
| Pv-1c | «mobile» > 25% | 0,0% | regge |
| Pv-1d | mediana > 1,5 s | 0,20 s (95%: 0,27 s) | regge |
| Pv-5 | sigma_v fuori [0,10; 0,50] o scarto > 30% | dichiarata 0,205, reale 0,181 m/s (−12%) | regge |
| Pv-6 | rapporto >= 1e-12 | 5,4e-17 | regge |
| Pv-2a | copertura < 0,85 | 0,936 / 0,917 / 0,903 / 0,920 | regge |
| Pv-2b | copertura >= 0,85 | 0,417 a 2 s | regge |
| Pv-3 | fuori [0,7; 3,5] s | 1,60 s | regge |
| Pv-4 | RMSE(a) < 0,4 volte, o errore a 2 s < 0,9 volte | 1,22 volte; 1,94 volte | regge |

Notato dopo (non era previsto): la copertura con q tarato sta sotto il 95% nominale (0,90–0,94) benché NIS e NEES
da visibile siano coerenti o prudenti; il q tarato è lo stesso (0,2) a 10, 15 e 30 Hz, ma la griglia è grossolana;
lo 0,0% di Pv-1c dipende anche dal fatto che q = 0,2 rende il filtro prudente su un ostacolo fermo.
