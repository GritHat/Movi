# Previsioni — sciame-avversario, f8 (continuità visiva), torneo f2

Scritte alle **2026-11-14T16:04:13+01:00** (`date -Is`), dopo la lettura di contratto, triage, preproposta (§2, §5),
`SOLUZIONE_V2.md`, consegne di creativo, ricercatore, tracciamento; **prima** di scrivere una riga del simulatore e
prima di ogni lancio. Ho letto `cono2.py` (creativo) e le righe 200–208 di `cont.c` (tracciamento) per sapere che cosa
implementare: i predittori li riscrivo io, il generatore delle traiettorie è mio.

Sigle: D = pannello 1 m a 1,9 m, soggetto a 2,3 m, portata 3 m; T = pannello 1 m a 2 m, soggetto a 4 m, portata 6 m;
L = pannello 2 m, soggetto a 4 m. R90 = regione dichiarata al 90 %; R100 = limite esterno. τ = tempo dall'ultima misura.
«Sul percorso» = prosegue, rallenta, sosta, torna, sosta lunga. Soglia comune del triage: R90 ≥ 0,85 per cella.

| Id | Attacco | Misura | Previsione | Smentita se |
|---|---|---|---|---|
| avv-1 | Attacco 1 della preproposta su C-EST (sosta improvvisa a metà pannello, 1,2 m/s, 200 semi, D e T) | (a) cicli «previsto» con celle della regione su libero oltre la fascia; (b) semi con μ1 > 0,5 oltre 0,5 s dopo l'uscita attesa; (c) vero dentro la regione, τ 0,5–3 s | (a) 0 con la fascia, > 50 % dei semi senza fascia; (b) lettura A (pesi cumulati): < 5 % dei semi; lettura B (0,8 e 0,2 per la massa corrente): ≥ 50 % in T, ≥ 30 % in D: **rigetto di B**; (c) fra 0,6 e 0,9 | (a) un ciclo con la fascia; (b) B sotto il 10 % in T; (c) ≥ 0,95 |
| avv-2 | C-EST, K-201: sosta lunga in T | quota dei cicli nascosti senza regione («perso») fra 3 e 6 s | ≥ 50 % in T (σ_eff supera 0,8 m), 0 % in D (l'ombra in portata è piccola) | T sotto il 10 % |
| avv-3 | Attacco 5 su C-EST, 400 «prosegue» 0,3–1,8 m/s | prima misura dentro l'ellisse al 95 % (momenti della miscela ritagliata × 5,99) | < 0,90 in almeno una fra D e T, per tutte e due le letture (atteso 0,5–0,85) | ≥ 0,90 in D e in T |
| avv-4 | K-206: C-EST su «sosta» a 3 s | R90 (massima densità al 90 % della miscela ritagliata) contiene il vero | < 0,85 in almeno una geometria e lettura | ≥ 0,85 ovunque |
| avv-5 | Banco di base, T, 200 per comportamento | R90 per comportamento e τ | C-004 e C-001 ≥ 0,85 sul percorso fino a 3 s; tutte e due < 0,5 a 2 s su «lato lontano»; C-005 (raggio del comportamento peggiore) ≥ 0,85 sul percorso ma area ≥ 0,8 dell'ombra da 2 s | una delle due sotto 0,80 sul percorso (n ≥ 100), o sopra 0,8 sul lato lontano |
| avv-6 | Sosta di 30 s (T) | R90 a 10, 20, 30 s | C-004 ≥ 0,95 (la scia è congelata); C-001 **sotto 0,85** a 30 s (la nube degenera col ricampionamento) | C-001 ≥ 0,90 a 30 s; C-004 < 0,90 |
| avv-7 | Corsa a 3 m/s (L, D), v_max del sistema 2,5 m/s | il vero nascosto dentro R100 = raggiungibile ∩ non visto libero; dentro lo strato 1 (cuneo) | il raggiungibile **manca** il soggetto in L in ≥ 20 % dei passaggi; il cuneo 100 % | raggiungibile 100 % |
| avv-8 | Secondo soggetto mai visto esce dalla stessa ombra mentre il primo è fermo dentro (T) | passaggi in cui la traccia è riagganciata all'estraneo e la possibile presenza cade a soggetto nascosto | regola del nucleo («Ritorno»: entro la fascia dell'ombra d'ingresso, una sola pendente): **100 %** quando l'estraneo esce per primo; con una porta sulla regione R90 (dilatata 0,45 m): 20–60 % | nucleo sotto il 90 %; nessuna porta sotto il 5 % |
| avv-9 | Uscita a velocità tripla (T) | riagganci con identità con la porta su R90 / ellisse | C-EST (ellisse 95 %) e C-004, C-001 riagganciano < 50 %: resta una pendente e un avviso permanente (sicuro, ma falso) | ≥ 80 % riagganci |
| avv-10 | Ombra stimata −20 e −30 cm, sosta appena dentro il bordo (già fermo all'ingresso), T | passaggi con il vero nascosto fuori da R100 (fascia 0,20 m) e fuori dallo strato 1 (fascia 0,40 m); R90 | −20 cm: R100 ≥ 0,98; −30 cm: R100 con fascia 0,20 manca in ≥ 5 % dei passaggi; strato 1 a 0,40 regge; R90 di C-004 e C-001 < 0,85 a −30 cm | −30 cm senza alcun mancato |
| avv-11 | Rilevamento 0,7 e 7–10 cicli mancati dopo la riemersione, con «vuoto» falso (cella vista libera) | cicli a soggetto visibile non rilevato in cui nessuna regione (neanche R100) lo contiene | ≥ 90 % di quei cicli per tutte le candidate (tutte ritagliano sul libero): la figura resta nell'ombra mentre il soggetto è fuori | < 50 % |
| avv-12 | Vuoto falso di 0,3 s in campo aperto, 0,5–0,9 m prima dell'ombra (D, 1,2 m/s) | passaggi in cui il soggetto entra nell'ombra **senza traccia pendente** (regola del nucleo: chiusura dopo 3 fotogrammi in campo aperto; conferma 3 su 5) | ≥ 50 % dei passaggi con il vuoto in quella finestra: nessuno strato, nessuna previsione | < 10 % |
| avv-13 | Corpo largo 0,45 m, C6 spenta (centro della parte visibile) contro C6 accesa | velocità d'ingresso stimata / vera; R90 su «prosegue» a 1 s | C6 spenta: rapporto mediano < 0,75; C-004 e C-001 sotto 0,85 a 1 s su «prosegue»; C6 accesa: ≥ 0,90 | rapporto ≥ 0,9 a C6 spenta |
| avv-14 | Spostamento della distribuzione: C-005 tarata su «prosegue» a 1,3 ± 0,15 m/s, provata su 0,8 m/s con 20 % soste e 12 % ritorni (T) | copertura vera del «90 %» a 2 e 3 s | 0,60–0,78; con la tabella del comportamento peggiore ≥ 0,88 ma area ≥ 0,8 dell'ombra; C-004 e C-001 (senza taratura della miscela) ≥ 0,85 | tabella «prosegue» ≥ 0,85 |
| avv-15 | Continuità che inganna | cicli nascosti con R90 piccola (≤ 25 % dell'ombra) e il vero a più di 0,5 m da R90 | su «lato lontano» e «svolta»: > 10 % dei cicli per C-EST, C-004, C-001; ≈ 0 per C-005 col raggio peggiore | < 2 % per tutte |
| avv-16 | Ostacolo che si muove (0,4 m/s, T), maschere congelate all'ingresso contro ricalcolate | cicli con celle di R90 su visto libero oltre la fascia; il vero nascosto fuori dallo strato 1 congelato quando il pannello accompagna il soggetto | congelate: > 50 % dei passaggi con R90 su libero; soggetto dietro un pannello che si muove con lui: fuori dal cuneo congelato nel 100 % | 0 passaggi |
| avv-17 | S2 (K-210): segno «visto» portato avanti di 155 ms | (a) errore rispetto al vero all'istante dell'uscita, in vista, moto regolare; (b) nei 3 cicli dopo una sosta improvvisa; (c) passaggi in cui il segno pieno compensato cade in una cella d'ombra | (a) compensato migliore (≈ 0,05–0,10 m contro ≈ 0,19); (b) compensato **peggiore**; (c) ≥ 30 % dei passaggi a 1,2 m/s senza C6, 0 con C6 (0,22 m > 0,19 m) | (b) compensato migliore; (c) 0 senza C6 |
| avv-18 | K-202 in D su «prosegue» | passaggi in cui R90 supera metà del cuneo prima della ricomparsa | C-005 (raggio peggiore): > 50 %; C-004: < 20 % | — |
| avv-19 | K-208: livello 50 % | R50 sulla miscela «squadra», τ ≤ 3 s | nessuna candidata fra 0,40 e 0,60 a tutti i τ | una dentro 0,40–0,60 a ogni τ |
| avv-20 | K-203: punto contro «fermo» | errore mediano del punto (mediana dei membri, media delle particelle) contro l'ultima misura, per τ ≤ 5 s, miscela «squadra» | nessun punto è non peggiore di «fermo» a ogni τ per ogni comportamento: perde su «torna» da 2 s | un punto mai peggiore |

**Due soggetti che si incrociano dietro l'ostacolo:** non prevedo di eseguirlo se il tempo non basta (il nucleo dichiara
già che con due pendenti l'identità non si dà): lo scriverò come «non eseguito».

**Indipendenza, dichiarata prima.** Generatore, scena, predittori: tutto codice mio, scritto ora, un solo autore e un
solo modello linguistico. Soggetto puntiforme salvo avv-13; sensore fermo; griglia cartesiana da 0,10 m (non la polare del
nucleo). Condivido con le candidate la lettura del loro testo: un mio errore di lettura è possibile e lo dichiaro dove
scelgo. Le letture di C-EST sono quelle del triage (§6): A = smorzamento 0,90 a ciclo, pesi cumulati; B = 0,95, pesi
0,8 e 0,2 per la massa corrente.

---

# Esiti (scritti alle 2026-11-14T16:25 circa, dopo i lanci; il testo sopra non è stato toccato)

Notato dopo, non previsto: (i) il ciclo di vita del nucleo chiude la traccia in campo aperto mentre il soggetto entra
nell'ombra (3,1–4,0 % dei passaggi di base); (ii) in C-EST lettura A il peso del transito **risale** quando H1 esce dal
campo osservato; (iii) σ_eff supera 0,8 m anche in D, perché la miscela ritagliata si allarga sul non osservato.

| Id | Esito | Numeri (file in `ris/`) |
|---|---|---|
| avv-1 | (a) regge; (b) A: smentita (T 12/198, D 174/202); B: regge, rigetto (T 191/198, D 174/202); (c) T smentita verso l'alto (0,93–1,00), D regge (0,70–0,88) | `a1_T.txt`, `a1_D.txt` |
| avv-2 | T smentita di poco (41–42 % «perso» a 3–5 s, attesi ≥ 50); D smentita (63,5 % a 3 s, 100 % a 5 s, atteso 0) | `base_T.txt`, `base_D.txt`, §6 |
| avv-3 | regge sull'ellisse dichiarata (A 0,320 T, 0,777 D; B 0,484 T, 0,669 D; L 0,000); smentita per B sull'ellisse calcolata anche da «perso» (1,000) | `base_*.txt`, §4 |
| avv-4 | regge: «sosta» a 3 s A 0,531 (T), 0,460 (D), 0,000 (L); B 0,000 | `base_*.txt` |
| avv-5 | regge sul percorso (C-004 ≥ 0,898, C-001 ≥ 0,962 fino a 3 s) e per C-005W (area 0,97–1,00 da 2 s); smentita in parte sul lato lontano (C-001 0,62 in T; in L 0,75 e 0,81) | `base_*.txt` |
| avv-6 | regge: a 30 s C-004 0,944 (T) e 0,988 (D); C-001 0,045 e 0,036 | `a6_sosta30_*.txt` |
| avv-7 | regge: raggiungibile manca in 138 passaggi su 138 (L); strato 1: 0 (1 ciclo in D: cella di bordo del campo) | `a7_corsa_*.txt` |
| avv-8 | nucleo: regge (347/357 = 97 %); porte su R90: smentita (C-004 95 %, C-001 99 %, C-005W 96 %); ellisse dichiarata di C-EST 25 % e 8 % | `a8_estraneo_T.txt` |
| avv-9 | smentita per C-004 (0,72) e C-001 (0,82); regge per C-EST (0,33 e 0,32) | `a9_altri_T.txt` |
| avv-10 | regge in parte: a −30 cm (D) il raggiungibile manca in 19 passaggi su 129, lo strato 1 in 0; C-004 0,67–0,70, C-001 no (0,88–1,00). Non previsto: la traccia si chiude nell'83 % dei passaggi a −20 cm (T) | `a10_*.txt` |
| avv-11 | regge: 98–99 % dei 1945 cicli fuori da ogni R90; lo strato 1 ne contiene il 49–53 % | `a11_miss8_T.txt` |
| avv-12 | regge: 197, 200, 148, 35 passaggi su 200 a 0,5 / 0,7 / 0,9 / 1,2 m | `a12_*.txt` |
| avv-13 | rapporto: smentita di poco (mediana 0,79–0,81, 10º percentile 0,50–0,54); C-004 regge (0,65–0,67 a 1 s); C-001 smentita in D (0,93) | `a13_*.txt` |
| avv-14 | a 2 s smentita (0,874); a 3 s 0,429, sotto la mia fascia; tabella peggiore e C-004, C-001: regge | `a14_*.txt` |
| avv-15 | regge solo per C-004 sul lato lontano (10,7 % dei cicli, 130 passaggi su 400); C-001 0,7 %, C-EST 2,3 %: smentita | `base_T.txt`, §2 |
| avv-16 | regge: maschere congelate, R90 su libero in 96 passaggi su 96; fuori dal cuneo congelato 91 su 100 (attesi 100) | `a16_*.txt` |
| avv-17 | (a) regge; (b) regge; (c) senza C6 regge (371–396 su 400); con C6 smentita (31 e 188 su 400 a 1,2 e 1,8 m/s) | `a17_s2.txt` |
| avv-18 | C-005W regge (0,99); C-004 smentita (0,91, attesi < 0,20) | `base_D.txt`, §4 |
| avv-19 | regge: nessuna fra 0,40 e 0,60 a ogni τ ≤ 3 s | `base_T.txt`, §7 |
| avv-20 | smentita in parte: il fantasma di C-004 batte «fermo» fino a 3 s in ogni comportamento sul percorso; perde a 5 s su «torna» in D (1,01 contro 0,70 m) | `base_*.txt`, §8 |

## Previsione aggiunta alle 2026-11-14T16:29:54+01:00, prima del lancio (variante nata dopo aver visto i numeri di `-fixentry`)

**avv-21.** La riga di B5 riscritta guarda il punto previsto solo al momento della chiusura (dopo 3 fotogrammi): restano fino a 3 cicli scoperti per passaggio. Variante `-fixentry2`: il punto previsto si guarda **a ogni ciclo senza misura**. Misura: cicli nascosti senza traccia pendente. Previsione: base T sotto 150 (da 576, erano 8486 senza correzione); ombra a −20 cm (T) sotto 500 (da 4676); corsa a 3 m/s (L) sotto 100 (da 485). Smentita se una delle tre non scende almeno della metà rispetto a `-fixentry`.

**Esito di avv-21 (16:30:49): smentita sui cicli, regge sui passaggi.** Cicli scoperti: base T 522 (attesi < 150), ombra a −20 cm 4243 (attesi < 500), corsa 211 (attesi < 100): solo la corsa scende di oltre metà. I cicli rimasti stanno in pochi passaggi dove la traccia era già persa prima (non confermata, o chiusa lontano dall'ombra). I **passaggi** con almeno un ciclo scoperto scendono invece a 9 su 2800, 16 su 600 e 3 su 400 (da 54, 297 e 119 con `-fixentry`). File `ris/a21_*.txt`.

**Nota (16:33).** Aggiungendo `-fixentry2` ho cambiato di una riga anche `-fixentry` (l'occlusione parte nello stesso ciclo, non in quello dopo) e ho rilanciato i suoi cinque file con l'eseguibile finale: cicli scoperti 531 (base T), 4395 (−20 cm), 369 (corsa); passaggi 18, 163, 108. I riferimenti «576, 4676, 485» scritti nella previsione avv-21 venivano dall'eseguibile precedente. Con i riferimenti nuovi nessuna delle tre scende di almeno metà (corsa: da 369 a 211, il 43 % in meno): **smentita sui cicli in tutte e tre**. Sui passaggi: 18 → 9, 163 → 16, 108 → 3. I lanci senza `-fix…` sono identici prima e dopo (stessa impronta dell'uscita di `a1_T`, tempi esclusi).
