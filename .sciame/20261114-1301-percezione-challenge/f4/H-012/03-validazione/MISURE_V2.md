# Riprova dell'insieme, versione 2 — H-012, f4 (`sciame-validazione`)

**In testa.** Lanci fra le 14:44 e le 14:46 del 14 novembre 2026; simulatore `sim_v2.py` (copia di `sim_h012.py` con il codice della versione 2 in coda), seme base 5101. Nessun file già consegnato è stato toccato. Tutto è **simulazione a sensore fermo**.

**Scostamenti.** (1) «Circa 1 m d'ombra» non si ottiene con pannello da 1 m e attore a 2,3 m: metto il pannello a 1,9 m, che dà **1,21 m** (dichiarato prima). (2) Le previsioni qui sotto sono state scritte in testa a questo file prima del codice; poi ho solo aggiunto il resto intorno. (3) Senza previsione: R8 con Pd = 0,9, la lettura «un gruppo tagliato vale da ingresso nell'ombra», l'effetto di C6 su «torna». (4) Letture mie: l'ingresso guarda l'ultima rilevazione, anche tagliata; «tagliato» = l'intervallo angolare del corpo tocca quello del pannello; il secondo soggetto è provato sulle sue prime 3 rilevazioni (prima della conferma 3 su 5); la scena «muro con persona» è mia (muro largo 1,2 m a 2,8 m, persona a 1,6 m). (5) «Sosta» e «torna» in P2c hanno N = 400, non 2000. (6) L'insieme provato è C1, C4, C5, C6, C8, V1, il rilascio nuovo e la geometria nuova; **C3, C9, C10, C11, B7 e B8 non sono nel mio simulatore**.

**Cambi di stato che propongo.** R8 nella regola nuova: **regge** con Pd = 1, **smentita** con Pd = 0,9 e ombra a −20 cm. «Il pannello da 1 m regge senza C6»: **smentita** nel mio rilevatore; C6 diventa necessaria, e costa su «torna». C1: **regge** alla scala della demo, 2 casi su 1200 in T.

**Previsioni, scritte alle 2026-11-14T14:42:18+01:00 (`date -Is`), prima di scrivere il codice della versione 2 e prima di ogni lancio.** Unità: il passaggio. N = 400 per cella (zero fallimenti → limite superiore 0,75 %).

| # | Misura | Soglia | Esito atteso (mio) |
|---|---|---|---|
| P1 | R8, regola nuova: passaggi con il centro del soggetto senza misura in una cella «libero»; 4 comportamenti × errore −20 / 0 / +20 cm; geometria demo corretta (pannello 1 m a 1,9 m, attore a 2,3 m: 1,21 m d'ombra) e T; fascia 0,40; w_min 0,15 | 0 falliti su 400 per cella | **regge**: 0. A 0 e +20 cm per costruzione. A −20 cm rischio dichiarato: l'ultima misura è il centro della parte visibile, a 0,28–0,32 m dall'ombra stimata: margine 8 cm sulla regola d'ingresso |
| P1-bracci | fascia 0 e 0,20 con −20 cm; −40 cm con fascia 0,40 | devono fallire | falliti in ≥ 90 % dei passaggi in tutti e tre |
| P2a | riemersioni legittime riagganciate (C1), una traccia pendente; = identità giusta | ≥ 95 % | demo: ≥ 99 % a 0 e +20 cm, ≥ 95 % a −20 cm; T: uguale |
| P2b | secondo soggetto mai tracciato: entra dal bordo del campo o della portata | 0 riagganci sbagliati | 0 su 400 (per costruzione della seconda clausola di C1) |
| P2b-limite | secondo soggetto mai tracciato che esce dalla stessa ombra | nessuna regola lo esclude | riaggancio sbagliato e muto in ≥ 95 % |
| P2c | «contiene alla riemersione» (prima misura usata dal filtro nel cerchio al 95 %), mio rilevatore a 3 colonne, «prosegue» | ≥ 85 % | D pannello 0,5 m: senza C6 14–17 % (ripetizione), con C6 ≥ 95 %. Demo corretta: 90–100 % senza, ≥ 95 % con |
| P3a | «mobile» finale: visto entro 1 s a 0,5 m/s da 2 m, di traverso e in avvicinamento, tre curve | ≥ 90 % | ≥ 99 % in tutti e sei i casi |
| P3b | muro fermo con una persona che gli passa davanti: passaggi con almeno un'etichetta falsa | ≤ 10 % | con C6 ≤ 2 %; **braccio senza C6: ≥ 80 %** |
| P4 | demo corretta, «prosegue»: durata di «previsto»; quota ancora mostrata alla riemersione; tempo in «perso» | descrittive | mediana di «previsto» 0,4–0,9 s; mostrato 5–40 %; «perso» 0,2–0,8 s |
| P5 | Pd 0,9, attraversamento di 4 s senza pannello: tracce vere chiuse per errore | descrittiva | 0,3–1 % se si chiude al quarto mancato di fila; 4–6 % se al terzo |

## Esiti

| # | Esito (N, limite al 95 %) | Verdetto |
|---|---|---|
| P1 | 0 passaggi falliti su 400 in tutte le 36 celle (demo corretta, T-1 m, T-2 m; 14 400 passaggi); limite 0,75 % per cella. A −20 cm: 0 su 4800 (limite 0,06 %). Uguale con la lettura «gruppo tagliato = ingresso» | **regge**; a 0 e +20 cm per costruzione, a −20 cm è una misura |
| P1, Pd 0,9 (senza previsione) | a −20 cm **13 passaggi falliti su 4800** (da 0 a 3 per cella, 8 celle su 12); a 0 e +20 cm 0 falliti, con 0–4 tracce chiuse per cella. Causa: la traccia viene chiusa da «non confermato», o perde le ultime rilevazioni, prima di entrare nell'ombra: nessuno strato 1, e il soggetto sta nella striscia che il sistema crede libera | **smentita** la soglia «0 falliti» |
| P2a | riagganciate 100 % in tutte le 27 celle con riemersione (N = 400; limite inferiore 99,25 %); con Pd 0,9: 99,7–100 % | **regge** |
| P2b | dal bordo del campo: 0 su 2400. Dal bordo della portata: demo 0 su 1200 (limite 0,25 %); **T 2 su 1200**, tutti e due a +20 cm (a 6 m il rumore radiale è 13,6 cm e porta una delle prime tre rilevazioni oltre 0,40 m dal bordo) | demo **regge**; T **smentita** (la mia previsione cade in quella cella) |
| P2b-limite | dalla stessa ombra: riaggancio sbagliato e muto in **2400 su 2400** | limite confermato: nessuna regola lo esclude |
| P2c | «Prosegue», N = 2000. Pannello da 0,5 m, 3 colonne: 20,5 % senza C6 → 99,9 % con. **Demo corretta: 61,1 % (3 colonne) e 80,2 % (w_min) senza C6 → 100,0 % con.** T: 99,4 → 100 %. Ancora mostrato alla riemersione: 1,6–18,5 % | con C6 **regge**; senza C6 **smentita** anche con il pannello da 1 m (61,1 e 80,2 % stanno sotto 83,7 %). Mie previsioni: «90–100 % senza C6» smentita; 20,5 % sta fuori dalla fascia 14–17 % |
| P2c, «torna» (senza previsione) | con C6 il contenimento di chi torna **scende**: demo 99 % → 47–50 %; T 91–98,5 % → 62–67 %; pannello da 0,5 m 99 % → 40 % (N = 400). Il filtro non vede più la frenata attraverso il gruppo tagliato. Miscela 70/18/12 nella demo: 94 % con C6, 86 % (w_min) o 73 % (3 colonne) senza | costo di C6, da dichiarare |
| P3a | 100 % nei sei casi (N = 2000; limite inferiore 99,85 %). Fermo: 0 etichette false su 4000 nel primo secondo. Da 3 m in avvicinamento (non chiesto): 100 / 85,9 / 26,6 % | **regge** a 2 m |
| P3b | con C6: 0 su 400 con le tre curve (limite 0,75 %). Senza C6: 400 su 400 | **regge** |
| P4 | demo corretta, «prosegue», a −20 / 0 / +20 cm: buio 1,13 / 1,07 / 1,07 s; «previsto» 0,40 / 0,47 / 0,53 s; ancora mostrato alla riemersione **0,5 / 1,2 / 0,8 %**; «perso» 0,67 / 0,60 / 0,47 s (mediane). In sosta «perso» dura 4,6–4,8 s | descrittiva; la mia fascia 5–40 % è smentita |
| P5 | chiuse per errore 118 su 20 000 (0,59 %) al quarto mancato di fila; 1047 (5,24 %) al terzo | dentro le fasce previste |

**I bracci che dovevano fallire sono falliti tutti.** Fascia 0 con −20 cm: 400 su 400 in ogni cella. Fascia 0,20 con −20 cm: 399–400 su 400. Ombra a −40 cm con fascia 0,40: 396–400 su 400. Muro senza C6: 400 su 400. La prova non è cieca.

**Che cosa vede la demo.** Dietro il pannello da 1 m la persona sparisce per circa 1,1 s: per mezzo secondo c'è l'area «probabile», poi «perso» per altro mezzo secondo, poi la stessa identità. L'area prevista è ancora accesa alla riemersione in un transito su cento.

## Che cosa l'insieme non prova

- Le correzioni C3, C9, C10, C11 e i blocchi B7 e B8 insieme alle altre: non sono simulati qui.
- La garanzia con rilevamenti mancati: con Pd = 0,9 a −20 cm cade in 13 passaggi su 4800, e una traccia su 170 si chiude da sola in quattro secondi.
- Un secondo soggetto che esce dalla stessa ombra: riagganciato sempre, con l'identità sbagliata.
- Errore della maschera d'ombra oltre −20 cm, rilevamenti falsi al bordo del pannello, rumore correlato, occlusore mobile, sensore indossato: fuori dal modello.
- Il mio «torna» frena a 1 m/s²; il simulatore condivide con la soluzione la specifica, il rumore gaussiano e il modello linguistico che li ha scritti.

**Proposta `validazione-4` (non provata).** Una traccia chiusa da «non confermato» a meno di 1 m da un'ombra lascia lo strato 1 su quell'ombra invece di sparire. Previsione: i 13 falliti scendono a 0. La smentisce la stessa corsa con Pd = 0,9.

## Per rifare tutto

```
sh /home/fede/Scrivania/ed/GitHub/Movi-Hackthon/.sciame/20261114-1301-percezione-challenge/f4/H-012/03-validazione/rifai_v2.sh
```

Otto lanci in sequenza sotto `timeout 120`; il più lungo dura 22 s, il totale circa un minuto. Risultati in `v2_*.txt` nella stessa cartella.
