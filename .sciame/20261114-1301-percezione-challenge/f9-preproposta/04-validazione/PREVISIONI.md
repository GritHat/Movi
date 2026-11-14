# Previsioni — `sciame-validazione`, f9, banco S3 + S4

Scritte alle **2026-11-14T15:45:56+01:00** (`date -Is`), **prima** di scrivere il codice del banco e di ogni lancio.
Ho letto: contratto f9, addendum, preproposta per intero, SOLUZIONE_V2, VERDETTO, il sorgente v0.5, la parte 3 del
torneo (tabelle). Non ho aperto i simulatori di altri né le cartelle f7, f8 e le altre di f9.

## La scena e le letture, fissate prima

- Pianta, sensore fermo in (0,0), campo ±43,5°, 15 Hz. «Libero» solo fra 1,24 m e la portata (3,0 m). Pannello da
  1 m a Z = 1,8 m, soggetto sulla linea Z = 2,3 m (ombra a quella quota: ±0,639 m). Pannello da 2 m: a Z = 2,2 m,
  soggetto a 2,6 m, portata 3,5 m (scelta mia: con 3,0 m il soggetto non avrebbe corsa per essere tracciato).
- Soggetto: disco di raggio 0,20 m. Misura: centro del corpo, solo se tutto visibile (un gruppo tagliato dall'ombra
  non aggiorna: C6 del nucleo), rumore gaussiano 3 cm per asse, Pd = 1 e 0,9. Passo con ondulazione dell'8 % a
  1,8 Hz (non gaussiana). Filtro: velocità quasi costante, q = 0,2 m²/s³, porta al 99 % (9,21).
- **H1**: il filtro che prosegue (velocità d'ingresso, Q del nucleo). **H2**: v ← α·v, x ← x + v·dt, P propagata col
  modello smorzato e la stessa Q. **α, lettura L1 (principale):** α = d / (d + |v|·dt), con d la distanza dal punto
  d'ingresso al centro dell'ombra sulla linea di moto: è il solo α per cui H2 «va a zero al centro dell'ombra».
  **L2:** α = 0,90 fisso.
- **Ritaglio:** massa a zero su «libero» e «occupato». **Na (principale):** ammessa su «in ombra» e su ogni «non
  osservato»; **Nb:** solo «in ombra».
- **Pesi.** **W1 (principale, «a ogni ciclo»):** μ_i ← μ_i·f_i, normalizzati, a ogni fotogramma (ricorsivo).
  **W2:** μ_i(t) ∝ μ_i(0)·f_i(t) (dal peso iniziale, non cumulato). f_i = frazione della massa gaussiana di H_i sulle
  celle ammesse.
- **Posizione mostrata:** media della miscela ritagliata. **σ_eff:** radice della traccia della covarianza della
  miscela ritagliata (raggio quadratico medio). **«Previsto»** finché σ_eff ≤ 0,8 m; poi «perso», assorbente.
- **Regione dichiarata:** (i) disco di raggio σ_eff («1σ»); (ii) disco di raggio 2·σ_eff («95 %» letto dall'etichetta
  ±X); (iii) regione di massima densità al 95 % della miscela ritagliata, sulle celle.
- **Ricomparsa:** porta χ² (9,21) contro H1 o H2 non ritagliate; dentro → stessa identità; fuori → traccia nuova, la
  vecchia resta in occlusione con la possibile presenza.
- **Nucleo (confronto):** cerchio al 95 % del filtro ritagliato sul cuneo, mostrato finché copre meno di metà
  dell'area del cuneo; poi «perso» assorbente; riaggancio geometrico entro la fascia di 0,40 m.

## Previsioni (misura · attesa · soglia di smentita)

- **P1 (attacco 1, celle libere).** Con l'ombra esatta, celle «libero» dentro l'area ritagliata: 0 per costruzione
  (controllo, non dato). Ma il disco ±σ_eff attorno alla posizione mostrata tocca celle «libero» in **più del 50 %**
  dei fotogrammi d'occlusione dopo 1 s. *Smentita:* meno del 10 %. Con l'ombra stimata 10 cm più larga del vero,
  area ritagliata su celle davvero libere in **≥ 90 %** dei passaggi. *Braccio che deve fallire:* senza ritaglio,
  area su «libero» nel 100 % dei passaggi; se non fallisce, la prova è cieca.
- **P2 (attacco 1, pesi).** Sosta di colpo a metà pannello, 1,2 m/s. W1: la sosta diventa dominante **prima** del
  tempo in cui il soggetto in transito sarebbe di nuovo tutto visibile (differenza mediana fra −0,4 e 0 s). W2:
  dopo (fra 0 e +0,5 s). *Smentita:* W1 con mediana > 0; W2 con mediana < 0 o > 1 s.
  **Conseguenza prevista sul transito normale («prosegue», 1,2 m/s, Pd = 1):** con W1 la sosta è già dominante al
  fotogramma che precede la prima rilevazione in **≥ 50 %** dei passaggi (falsa sosta); con W2 in **< 10 %**.
  *Smentita:* W1 < 20 %; W2 > 30 %.
- **P3 (regola σ_eff ≤ 0,8 m).** Con il pannello da 1 m e da 2 m, lettura Nb: σ_eff non supera mai 0,8 m (massimo
  < 0,6 m con 1 m): la regola è vuota, **zero** passaggi a «perso». Con Na: «perso» in **meno del 5 %** dei
  fotogrammi d'occlusione entro 3 s, per ogni comportamento. *Smentita:* un «perso» con Nb; oltre il 20 % con Na.
- **P4 (richiesta 2, errore contro incertezza dichiarata).** Il criterio «errore contenuto nell'incertezza dichiarata
  per tutta l'occlusione» **non regge**: almeno un comportamento fra «esce dal lato lontano», «torna indietro»,
  «velocità tripla» ha in almeno una fascia di tempo meno dell'80 % dei casi dentro 2·σ_eff. Atteso: lato lontano a
  2,5–3 s **≤ 20 %**; velocità tripla a 0,5 s **< 30 %**. «Prosegue» con W2: regione al 95 % (iii) ≥ 90 % in ogni
  fascia. Sosta a metà pannello da 1,5 s: ≥ 90 % dentro 2·σ_eff (è il caso che H2 assume). *Smentita:* tutti i
  comportamenti e tutte le fasce ≥ 90 %.
- **P5 (attacco 5, alla ricomparsa, 0,3–1,8 m/s, ≥ 400 passaggi).** Dentro 2·σ_eff: «prosegue» con W1 **< 90 %**,
  con W2 **≥ 90 %**; «torna indietro» **< 90 %** con le due letture; «velocità tripla» **< 50 %**. *Smentita:* W1
  «prosegue» ≥ 95 %; «torna» ≥ 95 %; tripla ≥ 90 %.
- **P6 (attacco 2).** Velocità tripla, v d'ingresso ≥ 0,9 m/s: porta violata in **≥ 60 %** dei passaggi; nasce una
  traccia nuova e la vecchia resta «previsto» dentro l'ombra (oggetto doppio) fino alla fine della prova in **≥ 90 %**
  di quei casi; la possibile presenza resta (per costruzione dello strato 1: controllo). Uno entra e due escono:
  quando esce per primo il mai visto, l'identità passa a lui **senza segnale** in **≥ 30 %** dei casi, e la possibile
  presenza cade con il primo ancora nascosto. *Smentita:* zero scambi muti.
- **P7 (continuità e confronto col nucleo).** Sui passaggi con la traccia entrata in occlusione, la preproposta
  mostra una stima in **≥ 95 %** dei fotogrammi d'occlusione; la regola del nucleo in **< 50 %** (a 1,2 m/s, 1 m).
  Ma la regione al 95 % della preproposta copre **più di metà del cuneo** in ≥ 50 % dei fotogrammi da 1 s in poi
  («prosegue»): è continua ma poco più informativa della possibile presenza. *Smentita:* nucleo ≥ 80 %; copertura
  oltre metà del cuneo in < 20 % dei fotogrammi.
- **P8 (modello smentito ma mostrato).** In «velocità tripla» dopo la porta violata e in «lato lontano», la massa
  grezza che sopravvive al ritaglio (0,8·f1 + 0,2·f2) scende sotto 0,05 mentre lo stato resta «previsto» in almeno
  il 20 % dei fotogrammi oltre 2 s. *Smentita:* mai sotto 0,05. (Incerta: H2 sta ferma nell'ombra e può tenere f2
  alta; la scrivo per registrare il dubbio.)

Esiti possibili per ciascuna: regge, smentita, non risolta. Ciò che noto dopo lo marco **[dopo]**.

---

## Esiti (aggiunti alle 2026-11-14T16:16+01:00, dopo le prove; il testo sopra non è stato toccato)

File: `ris_*.txt` (comando: `sh rifai.sh`). N = 400 per comportamento, seme 20261114 (replica col seme 777).

- **P1: mista.** Regione ritagliata su «libero»: 0 (controllo). Disco ±σ_eff su «libero» dopo 1 s: 49,7 % con Na
  («prosegue», `ris_01`), 0,0–2,2 % con Nb (`ris_03`, `ris_10_*N1*`): **smentita con Nb**. Ombra +10 cm: 400 passaggi
  su 400 (`ris_11`): regge. Braccio senza ritaglio: 399 su 399 (`ris_13`): è fallito, la prova vede.
- **P2: regge**, con un caso non previsto. W1: −0,22 s (Na) e −0,26 s (Nb); W2 con Nb: +0,06 s; **W2 con Na: la sosta non
  diventa mai dominante (0 su 399)**. Falsa sosta sul transito a 1,2 m/s: W1 84,4 % (Na) e 97,0 % (Nb); W2 0,0 % e 2,5 %.
- **P3: smentita.** Nb, pannello da 1 m: 0 passaggi a «perso» su 3600 (regge solo questa parte). Nb, pannello da 2 m:
  «perso» in 66–382 passaggi su 400 secondo il comportamento, 382 su «prosegue» (`ris_09`). Na: 7,1–62,4 % dei
  fotogrammi a «perso», 26,6 % su «prosegue» (`ris_01`).
- **P4: regge l'enunciato, due cifre smentite.** Lato lontano dentro 2σ_eff a 2,5–3 s: 6,0 e 0,0 % (Na), ma 30,3 e 23,1 %
  (W2, Nb): oltre il 20 % previsto. Velocità tripla a 0,5 s: 69 %, non < 30 %. «Prosegue» con W2: regione al 95 % al
  100 % in ogni fascia. Sosta a metà: 100 %.
- **P5: regge.** «Prosegue»: W1 76,4 % (Na) e 49,6 % (Nb); W2 100 %. «Torna»: 41,3–51,4 %. Tripla: 21,2–27,2 %.
- **P6: regge in parte.** Porta violata: 18,5 % a 0,9 m/s, 94,2 % a 1,2, 100 % a 1,8 (`ris_15`): la soglia «≥ 60 % da
  0,9 m/s» non vale a 0,9. Traccia vecchia ancora «previsto» a fine prova: 209 su 209. Scambio muto: 234 su 291 (80 %).
- **P7: regge con Nb, smentita con Na.** Stima mostrata: 99,8 % (Nb), 73,2 % (Na); nucleo 32,2 %. Regione al 95 % oltre
  metà del cuneo da 1 s in poi: 94,8–100 % dei fotogrammi.
- **P8: smentita.** Massa grezza sotto 0,05 con la stima mostrata: 0,0–2,0 % dei fotogrammi.

**[dopo]** (senza previsione): identità a fine prova; confronto con il solo filtro e con il «centro del cuneo»; tempi
di calcolo; braccio «falso libero»; velocità tripla per velocità d'ingresso; il difetto del banco corretto alle 15:58
(le tracce tentative passavano davanti a quelle in occlusione), con tutti i lanci rifatti.
