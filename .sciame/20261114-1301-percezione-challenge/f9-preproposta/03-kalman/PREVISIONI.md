# Previsioni di `sciame-kalman` (f9, 03-kalman) — scritte PRIMA delle prove

Ora di scrittura: 2026-11-14T15:44:44+01:00 (`date -Is`). Nessuno script di questa cartella era stato scritto né lanciato.
Letti prima: contratto f9, addendum, preproposta per intero, SOLUZIONE_V2, VERDETTO, TORNEO (parti 2 e 3), proposta v0.5 (.tex).

## Che cosa provo e con che cosa

- `sim_s3s4.py` (Python puro): scena della demo del nucleo (sensore in 0,0; campo ±43,5°; portata 3 m; anello cieco 1,24 m; pannello largo 1 m a 1,8 m; attore sulla linea a 2,2–2,4 m, 0,5–1,4 m/s; 15 Hz; Pd 0,9; rumore 3 cm; gruppo tagliato dall'ombra non misurato entro 0,2 m dal bordo). Generatore con cinque comportamenti in quota dichiarata: prosegue 50 %, sosta 20 % (in un punto uniforme della corda, non al centro), ritorno 10 %, uscita dal lato lontano 10 %, cambio di passo 10 %. Le quote sono mie e arbitrarie: per questo riporto per comportamento.
- Predittori: (K) cerchio al 95 % del Kalman del nucleo, non ritagliato; (A) preproposta alla lettera, pesi moltiplicati a ogni ciclo per f (massa della gaussiana NON ritagliata fuori dal «libero»), zero sul libero; (B) preproposta, lettura non cumulativa (peso ∝ peso iniziale · f al ciclo corrente); (C) versione corretta `kalman-1`: particelle a modi (transito, sosta, manovra) con transizioni, verosimiglianza 1 − Pd·1[visibile oltre la fascia] con Pd 0,9, fascia 0,40 m, regione = celle a densità più alta fino al 95 %.
- Misure a 0,5 / 1 / 2 / 3 s dall'ultima misura, solo a soggetto davvero nascosto (in ombra o fuori portata).
- `sim_s6s7.py`: Monte Carlo del punto di massimo avvicinamento e della velocità angolare.

Indipendenza: generatore, predittori e criteri sono dello stesso autore (io) e dello stesso modello linguistico; i parametri del generatore (punto di sosta uniforme, quote) non sono quelli dei modelli dei predittori. Niente hardware.

## Previsioni, con la soglia di smentita

- **P-K1 (S4, «±σ_eff»).** Il cerchio di raggio σ_eff (σ_eff = radice della media delle due varianze della miscela ritagliata) attorno alla media della miscela, variante A, contiene il vero in meno del 60 % dei casi nel complesso, a ciascuno dei quattro tempi. **Smentita:** ≥ 68 % a tutti e quattro i tempi.
- **P-K2 (S3, fuori dalle due ipotesi).** Varianti A e B: la regione al 95 % (celle più dense) contiene chi esce dal lato lontano in meno del 50 % dei casi a 3 s, e chi torna indietro in meno del 70 % a 2 s. **Smentita:** ≥ 90 % in uno dei due.
- **P-K3 (S4, doppio conteggio).** Nei transiti «prosegue», all'ultimo ciclo in cui il vero è ancora dentro l'ombra, la variante A ha μ1 < 0,5 in almeno il 30 % dei transiti; la variante B in al più il 10 %. **Smentita:** A < 10 %, oppure B > 30 %.
- **P-K3b (S4, lettura non cumulativa).** Nelle soste, variante B: a 3 s μ1 è risalito sopra 0,5 in almeno il 20 % dei casi con velocità d'ingresso ≥ 1,0 m/s (il «fantasma» ha attraversato il libero ed è rientrato nel non osservato fuori campo). **Smentita:** < 5 %.
- **P-K4 (S4, soglia 0,8 m).** Variante A: σ_eff > 0,8 m in meno del 5 % dei casi a ogni tempo fino a 3 s: la regola «σ_eff ≤ 0,8 m» non fa mai passare a «perso» con il pannello da 1 m. Conto a mano scritto prima: su un segmento lungo L lo scarto tipo massimo è L/2 (0,64 m con 1,28 m d'ombra sulla linea dell'attore); distribuzione uniforme: L/√12 = 0,37 m. **Smentita:** ≥ 20 % a qualche tempo.
- **P-K5 (versione corretta C).** La regione al 95 % contiene il vero in almeno l'85 % dei casi per ciascun comportamento a ciascun tempo (celle con n ≥ 50), anche per il lato lontano e il ritorno. **Smentita:** una cella con n ≥ 50 sotto l'80 %. Non prevedo l'area: la misuro.
- **P-K6 (ombra stimata 20 cm più stretta).** Soste a 2 s: nelle varianti A e B il vero sta in una cella a probabilità zero in almeno il 20 % dei casi; nella C (fascia 0,40 m) la regione al 95 % perde al più 5 punti rispetto all'ombra esatta. **Smentita:** A/B < 5 %, oppure C perde più di 15 punti.
- **P-K7 (S6).** Rotta di collisione vera (distanza minima vera 0), errore di velocità 0,2 m/s per asse, posizione 3 cm: lo scarto tipo del tempo vale R·σ_v/v² entro il ±25 % per v ≥ 1 m/s (0,4 s a 2 m e 1 m/s); la distanza minima stimata ha mediana circa 0,67·R·σ_v/v (0,27 m a 2 m e 1 m/s; 0,81 m a 3 m e 0,5 m/s) e 95° percentile circa 2·R·σ_v/v. Oggetto fermo a 2 m, senza guardia sulla velocità: «distanza minima < 0,5 m con tempo > 0» nel 5–12 % dei cicli. **Smentita:** valori fuori da ±25 % (mediana, scarto) o fuori dall'intervallo 5–12 %.
- **P-K8 (S7).** Con rumore d'angolo 1° per campione a 15 Hz, retta ai minimi quadrati: per separare (5 % falsi, 5 % mancati) la velocità angolare nulla da un attraversamento a 0,3 m/s a 2,3 m (7,5°/s) servono 0,4–0,6 s; da un avvicinamento a 0,5 m/s da 3 m che passa a 0,5 m (1,6°/s) servono 1,3–1,6 s. Dalla velocità del filtro (0,2 m/s) «subito»: non separa attraversamenti sotto circa 0,65 m/s a 2,3 m. **Smentita:** tempi fuori dagli intervalli di più del 30 %.
- **P-K9 (da dove viene 0,2 m/s).** Lo scarto tipo di regime della velocità del filtro del nucleo (q = 0,2 m²/s³, 15 Hz, rumore di posizione 1,5–6 cm) sta fra 0,15 e 0,35 m/s. **Smentita:** fuori dall'intervallo.

## Esiti

(riempiti alle 2026-11-14T16:12:34+01:00; i numeri stanno in `tabelle_s3s4.txt`, `ris_s3s4_*.txt`, `ris_s6s7.txt`, `ris_s4_pesi.txt`, `ris_costi_e_conti.txt`; N = 2000 per comportamento, maschera esatta salvo dove detto)

| Previsione | Esito | Numeri |
|---|---|---|
| P-K1 | **non regge** (falsa a 0,5–2 s, vera a 3 s; la soglia di smentita scritta, ≥ 68 % a tutti e quattro i tempi, non è raggiunta: alla lettera «non risolta») | copertura di ±σ_eff, lettura L1, variante A, tutti i comportamenti: 0,84 / 0,82 / 0,71 / 0,44 |
| P-K2 | **smentita** per il ritorno; al limite per il lato lontano | ritorno a 2 s: A 0,98, B 0,98 (la regione è 7,8–8,1 m²); lato lontano a 3 s: A 0,51, B 0,51 |
| P-K3 | **smentita** sulla lettura L1 | L1: A 112 su 1999 (5,6 %), B 2 su 1999. **[dopo]** su L2: A 760 su 1999 (38,0 %), B 173 (8,7 %) |
| P-K3b | **regge** | L1, B: μ1 > 0,5 a 3 s in 915 soste su 915 (μ1 medio 0,84) |
| P-K4 | **smentita** sulla lettura L1 | σ_eff > 0,8 m: 0 / 0 / 51 / 89 % dei casi a 0,5 / 1 / 2 / 3 s. **[dopo]** su L2: 0 % a ogni tempo, σ_eff medio 0,33 m a 3 s (il conto a mano L/2 = 0,64 m regge) |
| P-K5 | **smentita** | C, regione al 95 %: prosegue a 3 s 0,66 (n = 160); lato lontano 0,42 e 0,21 a 2 e 3 s; cambio di passo a 3 s 0,74. Reggono sosta (0,96 / 0,93) e ritorno (0,97 / 0,94) |
| P-K6 | parte A/B **non regge** (12 % invece di ≥ 20 %; sopra la soglia di smentita del 5 %); parte C **regge** | soste a 2 s, ombra a −20 cm: vero in cella a probabilità zero nel 12,3 % (A, L1); a 0,5 s, tutti i comportamenti: 31,7 %. C: 0,959 → 0,959 |
| P-K7 | **regge** | 2 m, 1 m/s: scarto del tempo 0,44 s (formula 0,40); mediana e 95° percentile della distanza 0,27 e 0,78 m (0,27 e 0,80). Fermo a 2 m: 8,0 % |
| P-K8 | **regge** | 0,53 s (formula e Monte Carlo); da 3 m a 0,5 m/s: 1,60 s (formula), 1,33 s e 1,13 s (Monte Carlo); dal filtro: 0,52–0,78 m/s |
| P-K9 | **regge** a 3,4 e 6 cm (0,18 e 0,22 m/s); a 1,5 cm 0,144 m/s, appena sotto il limite inferiore scritto (0,15) | `ris_s6s7.txt` |
| P-K10 (a) | **regge** | 2 su 2000 (0,1 %) |
| P-K10 (b) | **smentita** | μ1 > 0,5 a 3 s in 589 soste su 894 (65,9 %) con q = 0,2; 14,2 % con q = 0,02 **[dopo]**; 86,3 % con Pd = 1 e senza fascia |

**Notato dopo [dopo].** (1) Nel mio generatore «prosegue» ha una deriva di velocità (0,02 m/s per ciclo e per asse, cioè q vero ≈ 0,006 m²/s³): il 3,7 % dei «prosegue» esce dalla portata o entra nell'anello cieco entro 3 s; pesa solo sulle righe a 3 s (n = 160). (2) Un lancio di `sim_s4_pesi.py` è caduto per un errore mio di shell (argomenti non separati): nessun numero prodotto, rifatto. (3) Due ore scritte a mano nelle note erano sbagliate di pochi minuti: corrette con i valori di `date -Is`.

## Nota scritta alle 2026-11-14T15:48:41+01:00 (`date -Is`), dopo UNA prova di fumo (sosta, N = 60, per tempi ed errori) e prima delle prove vere

La prova di fumo ha mostrato una cosa che non avevo previsto: nella lettura «zero sul solo libero» (quella delle previsioni P-K1…P-K6: la chiamo **L1**) la massa resta su tutto il non osservato (fuori campo, oltre portata, anello cieco) e la regione si allarga a metri quadrati. La preproposta scrive anche «solo dentro l'inviluppo delle celle in ombra»: aggiungo perciò **[dopo]** la lettura **L2** (massa ammessa sulla sola ombra stimata entro la portata; f = quota della gaussiana nell'ombra). Le previsioni restano giudicate su L1 come scritte; i numeri di L2 sono «notati dopo», senza previsione, salvo il conto a mano di P-K4 (scarto tipo massimo L/2), che era scritto prima e riguarda una massa confinata all'ombra, cioè L2. N passa da 400 a 2000 per comportamento (il simulatore è più veloce del previsto).

## Nota scritta alle 2026-11-14T15:56:36+01:00 (`date -Is`), DOPO il primo giro completo (cartella `giro1/`, 20 lanci, N = 2000)

Visti i numeri del primo giro, aggiungo due misure **[dopo]**, senza toccare generatore, semi, predittori A, B, C e K (i numeri del primo giro devono tornare identici: lo controllo con `diff`):
1. per la versione C, la regione al 95 % **condizionata a «entro la portata»** e la **quota dichiarata «fuori» (massa nel non osservato)**, da confrontare con la frequenza vera di chi è fuori;
2. un argomento facoltativo per il q delle due ipotesi durante l'occlusione (0,02 invece di 0,2), per separare l'effetto del modello a due ipotesi da quello della covarianza gonfiata.
Sono esplorazioni: non hanno una previsione scritta prima, e nella consegna portano **[dopo]**.

## Previsione P-K10, scritta alle 2026-11-14T16:07:57+01:00 (`date -Is`), prima di scrivere e lanciare `sim_s4_pesi.py`

Dopo il primo giro so che le due letture della regola dei pesi si contraddicono (L1: il «fantasma» resta; L2 cumulativa: H1 muore nei transiti normali). Provo la **verosimiglianza corretta** sulle STESSE due ipotesi della preproposta (H1 a velocità costante, H2 smorzata verso il centro; pesi 0,8 / 0,2; q = 0,2), portando avanti la densità condizionata con 150 particelle per ipotesi: peso della particella × (1 − Pd) se sta nel visibile oltre 0,2 m dal bordo dell'ombra (Pd = 0,9), Λ_i = Σ pesi, μ_i ∝ μ_i·Λ_i.
- **(a)** transiti «prosegue»: μ1 < 0,5 all'ultimo ciclo in cui il vero è in ombra in al più il 19 % dei transiti (la metà del 38 % della lettura L2 cumulativa). **Smentita:** > 30 %.
- **(b)** soste con ingresso ≥ 1,0 m/s: μ1 > 0,5 a 3 s in al più il 5 % (contro il 100 % della lettura L1 non cumulativa). **Smentita:** > 20 %.
Che cosa condivide: generatore, semi, geometria e autore del primo giro.
