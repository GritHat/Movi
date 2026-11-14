# Previsioni — `sciame-rovesciatore`, f9 (audit delle ipotesi nascoste su S3 + S4, S1, S8)

Scritte alle **2026-11-14T15:45:06+01:00** (`date -Is`), prima di scrivere il simulatore `audit_imm.c` e prima di ogni lancio.
Prima di scriverle ho fatto solo conti a mano di ordine di grandezza (nella mia testa e una riga di Python sulla geometria: semi-ombra 0,639 m; tratto senza misura 1,68 m). Di P1, P6, P9 conosco quindi il verso: valgono come conti di controllo, non come prove riuscite.

## La scena (mia, a una dimensione, sulla linea dell'attore)

Pannello largo 1 m a 1,8 m, attore sulla linea a 2,3 m (condizioni della demo, v0.5 §6): ombra sulla linea [−0,639; +0,639] m. Corpo largo 0,40 m. 15 Hz. Ingresso da sinistra a velocità costante (il caso più favorevole all'ipotesi H1). La traccia perde la misura quando il bordo del corpo tocca l'ombra (correzione C6 del nucleo) e la riprende solo a corpo tutto fuori, con Pd = 0,9 per fotogramma. q = 0,2 m²/s³ (nucleo, B4); errore della velocità d'ingresso σ_v = 0,10 m/s (ipotesi mia); pesi iniziali (0,8; 0,2); H2 con α scelto per fermarsi al centro dell'ombra (lettura più favorevole di «tende al centro dell'ombra d'ingresso»). 1000 particelle per ipotesi, 1000 prove per cella, seme fisso.

Due letture dell'aggiornamento dei pesi:
- **A (alla lettera, §2.3 punto 2):** a ogni ciclo μ_i è moltiplicato per la frazione della gaussiana NON ritagliata che cade nelle celle ammesse.
- **B (Bayes corretto con Pd = 1):** le particelle nelle celle «libero» sono tolte una volta per tutte; μ_i è moltiplicato per la quota sopravvissuta.

Due letture delle celle ammesse: **L1** = ombra stimata più le celle occupate dalla parte visibile del corpo (favorevole); **L2** = solo ombra («la massa può esistere solo dentro l'inviluppo delle celle in ombra»).

«Sosta falsa» = in un transito normale, μ2 > 0,5 in almeno un ciclo prima del riaggancio.

## Previsioni

| # | Enunciato | Misura | Soglia di smentita |
|---|---|---|---|
| P1 | Transito a 1,2 m/s, lettura favorevole (B, L1), mondo del nucleo: il ritaglio **regge** | sosta falsa ≤ 10 % | > 25 % |
| P2 | Stesso transito, lettura alla lettera (A, L1): doppio conteggio dell'evidenza | sosta falsa ≥ 50 % | < 20 % |
| P3 | Stesso transito, B con L2 (solo celle in ombra) | sosta falsa ≥ 90 % | < 50 % |
| P4 | Transito lento a 0,5 m/s (3,4 s senza misura), B, L1, q = 0,2 | sosta falsa ≥ 20 % | < 5 % |
| P5 | Maschera d'ombra più stretta di 20 cm con «libero» falso nella striscia, zero esatto (B, L1): le due ipotesi si estinguono (massa residua < 5 % in entrambe) | ≥ 90 % dei transiti | < 50 % |
| P5b | Stessa maschera, ma evidenza negativa solo oltre una fascia di 0,40 m (regola del nucleo) | estinzioni ≤ 5 % | > 20 % |
| P6 | Sosta brusca a metà pannello a 1,2 m/s (attacco 1), B, L1: il modulo fa ciò che promette | μ2 > 0,5 entro 1,0 s dall'arresto in ≥ 90 % | < 70 % |
| P7 | Sosta appena dentro l'ombra (centro a 0,25 m dal bordo d'ingresso) o appena prima dell'uscita: l'etichetta «±σ_eff» non contiene il vero | quota dei cicli fra 0,5 e 3 s dall'arresto con il vero entro media ± σ_eff ≤ 30 % in almeno uno dei due casi | ≥ 60 % in entrambi |
| P8 | Alternativa `rovesciatore-f9-1` (un solo orologio: «non riemerso» oltre il tempo d'uscita calcolato con v − 2σ_v più 3 fotogrammi): pochi falsi e ritardo paragonabile | falsi nei transiti ≤ 5 % a 0,5 e a 1,2 m/s; ritardo mediano sulla sosta a metà pannello non peggiore di 0,5 s rispetto a B | falsi > 10 %, o ritardo peggiore di oltre 0,5 s |
| P9 | (conto) La distribuzione uniforme sul cuneo della demo (pannello di 1 m a 1,8 m, portata 3 m) ha raggio efficace √(σx² + σz²) fra 0,4 e 0,6 m: la regola «previsto finché σ_eff ≤ 0,8 m» non porta mai a «perso» | raggio < 0,8 m | ≥ 0,8 m |
| P10 | Compensazione della latenza (S2) applicata prima del ritaglio (stato a t_now, mappa a t_cap, 155 ms): peggiora la sosta falsa di P1 | aumento ≥ 10 punti | aumento < 3 punti |

Esiti possibili per ciascuna: regge, smentita, non risolta. Ciò che noterò dopo i lanci lo marcherò **[dopo]** nella consegna.

## Che cosa condivide questo controllo con ciò che controlla

Con la preproposta: il testo (la mia lettura del §2.2–2.3) e il modello linguistico. Non il codice (non ne ha). Con il nucleo: i parametri presi da `SOLUZIONE_V2.md` (q, C6, corpo, geometria). Scena, generatore e codice sono miei: una dimensione, bersaglio a velocità costante, nessuna profondità simulata. Vale solo per i difetti di logica della regola, non per quelli del sensore.

## Aggiunta dopo il primo lancio (scritta alle 2026-11-14T15:48:12+01:00, prima del secondo lancio)

Il primo lancio (`risultati_audit_imm.txt`, 21 celle) e' gia' stato visto: P11 e' quindi scritta conoscendo l'esito di P5 (−20 cm: estinzione nel 100 %). Le 21 celle gia' viste restano identiche (le celle nuove sono in coda, stesso seme).

| # | Enunciato | Misura | Soglia di smentita |
|---|---|---|---|
| P11 | Il selettore (S1) passa a una griglia piu' rada mentre la traccia e' nascosta: con celle da 2° (8 cm a 2,3 m) e la regola «libero se una sottocella e' libera», il bordo dell'ombra arretra fino a 8 cm. Con zero esatto (B, L1), transito a 1,2 m/s | sosta falsa ≥ 15 % con −8 cm; estinzioni < 20 % | sosta falsa < 5 % |
| P11b | Stessa prova con −4 cm (regola a maggioranza) | sosta falsa fra 2 e 15 % | fuori dall'intervallo: smentita in un verso o nell'altro |
