# PREVISIONI — prova d'insieme della continuità (C-C), `sciame-validazione`, f12

Scritto alle **2026-11-14T17:51:12+01:00** (`date -Is`), PRIMA di compilare e di lanciare qualunque prova. A quest'ora ho letto: il contratto
d'integrazione, il verdetto V8, `MODIFICHE_CONTINUITA.md`, `CONTROPROVE_MODIFICHE.md`, `att.c` e il suo `rifai.sh`,
tre righe di `ris/base_T.txt` e `tempo_C.txt` di f8 (per il tempo dei lanci). Non sono cieco rispetto ai risultati di
f8 riportati in quei documenti. Nessun lancio mio è stato fatto.

## Definizioni fissate prima

- **Unità:** il passaggio. Semi nuovi, mai usati in f8 (f8: 1000–1199, 12000–12399, 100000+, 200000+, 300000+);
  miei: prova 7 000 000 000 + 1 000 003·s, libreria 9 000 000 000 + 1 000 003·s, con un mescolatore diverso.
- **Insieme provato:** M1–M8 come in `att.c` più c1 (0,75 m dall'ombra d'ingresso; in D senza margine dalla portata),
  c2 (le pendenti ambigue non bloccano il riaggancio), c3 nella forma simulabile (gruppo «tagliato» deciso sul bordo
  VERO dell'occlusore, come lo vedrebbe l'immagine, non sulla maschera stimata), c4 (entrata dopo due cicli senza
  misura), c5 (sotto 0,3 m/s subito «ampio»), c7 (traccia chiusa o non confermata con l'ultima misura entro 0,75 m da
  un'ombra accende l'avviso).
- **Vuoto:** un ciclo, con la traccia entrata nell'ombra e non chiusa, senza regione emessa.
- **Scoperto:** un ciclo con il corpo tutto nascosto dentro l'area osservata, senza traccia pendente nell'ombra e senza
  avviso acceso (c7 compresa). Conto anche i passaggi mai confermati prima dell'ombra (f8 li scartava).
- **Fuori dall'area d'avviso:** corpo tutto nascosto e (avviso spento, oppure centro fuori da R100 = cuneo stimato + 0,40 m).
- **Precisione, misura primaria:** all'istante esatto 1, 2, 3 s dall'ultima misura, corpo tutto nascosto, dentro l'area
  osservata, segno «previsto» (non «ampio»): il centro sta in una cella di R90. Secondaria (confrontabile con f8): lo
  stesso su tutti gli istanti, R90 grezza anche se il segno è «ampio». Terza: la regione mostrata (in «ampio» è tutta l'ombra).
  Una cella si dichiara solo con almeno 400 passaggi; sotto, «numerosità insufficiente», con il suo n.
- **Limite inferiore:** Wilson, 95 % a due code.

## Soglie del contratto (C-C) e previsioni

| # | Misura | Soglia (regge se) | Smentita se | Previsione mia |
|---|---|---|---|---|
| P1 | (a) passaggi con un vuoto dopo l'ingresso, 3 geometrie × rilevamento 0,9 e 0,7 × puntiforme ed esteso | 0 | ≥ 1 | regge (0) |
| P2 | (a) passaggi scoperti (traccia chiusa prima dell'ombra), con c7 | 0 | ≥ 1 | **cade**: resta qualche passaggio (1–3 cicli fra la misura mancata e la chiusura); con c7 meno di un decimo di quelli senza c7 |
| P3 | (b) sul percorso (prosegue, rallenta, si ferma, torna, sosta lunga), maschera esatta, corpo esteso, rilevamento 0,9: limite di Wilson ≥ 0,90 a 1 e 2 s e ≥ 0,85 a 3 s, in ogni cella con n ≥ 400 | tutte le celle | almeno una cella sotto | **cade in D a 2 o 3 s** in almeno una cella (misura secondaria); regge in T e L |
| P4 | (b) a parte: svolta, esce dal lato lontano, parte da fermo | nessuna soglia: si dichiara la cifra | — | svolta e lontano sotto 0,70 a 2 s; parte da fermo sotto 0,50 a 1 s nella regione grezza, sopra 0,90 nella regione mostrata con c5 |
| P5 | (c) K-215: corpo esteso, ombra stimata −10 cm e −20 cm, T, «prosegue»: regione a 1 s | ≥ 0,85 (V8 §7) | < 0,85 | senza c3 **cade** (0,3–0,6); con c3 simulata regge (≥ 0,90) |
| P6 | (d) estraneo mai visto che esce dalla stessa ombra, c1 attiva: avvisi rilasciati con il soggetto ancora nascosto | 0 | ≥ 1 | **cade**: identità sbagliata in oltre metà dei casi in ogni geometria (oltre 0,9 in D); c2 com'è scritta NON lo ripara (salva solo i casi in cui la porta rifiuta l'estraneo) |
| P7 | (d) c1 allarga il riaggancio all'estraneo rispetto alla regola prima di c1 | — | — | sì, di almeno 5 punti in almeno una geometria |
| P8 | (e) nascosti fuori dall'area d'avviso, tutti gli istanti, tutte le prove | 0 | ≥ 1 | **cade** per gli stessi cicli di P2; 0 con l'avviso acceso e il centro fuori da R100 |
| P9 | (e) la chiusura «fuori dall'area osservata» con la regola «non toglie l'avviso»: nascosti senza avviso dopo la chiusura | 0 | ≥ 1 | regge (0); se togliesse l'avviso, scoperti in D in oltre 50 passaggi su 400 di «sosta lunga» (forma debole: punto del filtro fuori area); la forma scritta (tutti i membri fuori) non scatta mai con sd-1 |
| P10 | (f) identità al ritorno con C6 e c1: riagganci su ricomparse, sul percorso | ≥ 0,95 per geometria | < 0,90 | regge in T e L; in D fra 0,90 e 0,99 |
| P11 | (g) costo del predittore, dieci tracce, C, 95º percentile | ≤ 6,7 ms | > 6,7 ms | regge (0,5–1,5 ms) |
| P12 | semi: su 1000 coppie di semi vicini, flussi uguali a meno di uno spostamento | 0 | ≥ 1 | regge (0) |

Esiti possibili: regge, smentita, non risolta. Ciò che noto dopo i lanci lo marco «notato dopo».
