# Controprove sulle modifiche per la continuità visiva — `sciame-avversario`, f8, fase f4

Lavoro dalle 16:52 alle 17:20 del 14 novembre 2026 (`date -Is`). **Tutto è simulazione mia su CPU: niente è provato sull'hardware.** Attaccato: `13-soluzione/MODIFICHE_CONTINUITA.md` (**M**), com'è scritto. File in `14-attacco/`: `att.c`, `rifai.sh`, `ris/<nome>.txt` (nome fra parentesi nel testo), `tempo_py.py`, `PREVISIONI.md`. Tre numeri con «/» = geometrie D / T / L. Unità: il passaggio; 400 semi per comportamento (200000+), libreria da semi 100000+.

## 0. In testa

**Cambi di stato proposti.** (1) Riaggancio con la regola composta (nucleo ∧ M7): **smentito** in demo e con il corpo esteso. (2) Regola 2 del §2.5: **smentita**, è uno stato assorbente. (3) «R90 ≥ 0,85 sul percorso»: **regge** con la maschera esatta (minimo mio 0,876); **smentito** con l'ombra stimata a −10 / −20 cm e il corpo esteso (0,28–0,46) e per chi parte da fermo accanto al pannello (0,11–0,26). (4) Taratura con 30 camminate: **smentita**. (5) Costo per ciclo e strato 1: **reggono**.

**Scostamenti.** Prima delle previsioni (16:58:37) avevo letto `comp.c`, `gen.h` e il campo `C1_riaggancio` dei risultati della soluzione: P-av-1 non è cieca. Una prova di fumo su semi di sviluppo (300000+) è stata vista prima; nessun parametro ritoccato. Dopo il primo giro (codice congelato: `att_congelato_1704.c`) ho aggiunto tre misure e cinque bracci di correzione; `rifai.sh` ha riscritto tutti i file di `ris/` con il codice esteso: **le uscite del primo giro non sono conservate a parte** (campi comuni identici, controllati su `base_T`). L'attacco 4 è **notato dopo**. Due soggetti insieme nella stessa ombra non sono simulati (solo il ramo della regola, nella sessione). Previsioni: 4 reggono, 2 smentite, 7 miste, 1 non eseguita come scritta. Le ore sono stime **non verificate**.

**Che cosa il controllo condivide con M.** La specifica (le regole a parole, la lettura di C-004 di `comp.c`), le geometrie, la griglia da 0,10 m, il filtro, il rumore gaussiano noto, il modello linguistico. **Non condivide:** il codice, il generatore (decelerazioni costanti, ondulazione del passo, curva), il corpo esteso (disco da 0,45 m, misura = baricentro della parte visibile), C6 calcolata sulla maschera **stimata** (gruppo «tagliato» se un punto visibile è entro una cella dall'ombra stimata), il ciclo di vita e il riaggancio eseguiti per intero. Fuori: falsi rilevamenti, buchi di profondità, sensore vero.

## 1. Gli attacchi

| # | Attacco | Esito | Conseguenza |
|---|---|---|---|
| 1 | **Riaggancio composto.** M7 tiene la regola «Ritorno» del nucleo (misura entro 0,40 m dall'ombra, a più di 0,40 m da portata e campo); C6 allontana la prima misura valida | «Prosegue» riagganciati: corpo esteso **102/273, 306/397, 250/332 (0,37 / 0,77 / 0,75)** (`base_*`); puntiforme come il banco 0,68 / 0,98 / 0,96 (`punto_*`). **Nei dati stessi della soluzione** (`13-soluzione/ris/prova_*.tsv`, `C1_riaggancio`): 212/331, 336/345, 207/232. La porta M7 sbaglia 0–2 volte; cade la regola del nucleo: in T per la distanza (90), in D per il margine dalla portata (136) e la distanza (61). Il §2.8 misura solo M7 | **Smentita**; riscritta, c1 |
| 2 | **Stato assorbente:** sessione di 120 passaggi sul percorso (la scheda 4 × 30) con la regola 2 del §2.5 | Prima «ambigua» al passaggio **1 (D) e 4 (T)**; poi riagganci **0 su 66 e 0 su 100**; «previsto ampio» pendenti alla fine **87 / 117 / 95** (`sess_*`): con l'occlusore fermo nessuna chiusura le toglie. 120 pendenti: 5,4 ms al 95º percentile in C, sul limite di 6,7 (`tempo_C`) | **Smentita**; riscritta, c2 |
| 3 | **Tutto insieme** (A-sd-1, A-sd-2): T, corpo esteso, ombra stimata −20 cm, rilevamento 0,7, M1 + `sd-1` | R90 su «prosegue» **0,37 a 1 s (136/364), 0,28 a 2 s (43/152)**; gli altri sul percorso 0,51–0,55 e 0,59–0,70 (`tutto_T`). A −10 cm: 0,46 e 0,37. Maschera esatta: 0,98 e 0,92. Puntiforme a −20 cm: 0,99 e 0,95: **il banco non lo vede**. Causa: fra corpo tagliato e ombra stimata restano due celle «libere», C6 non scatta, il baricentro della parte visibile frena il filtro. R100: 0 fuori. Con rilevamento 0,7 e maschera esatta: **scoperti 130 passaggi su 1581 (8,2 %)** (`tutto_T_e0_pd07`; M: 9 su 2800 a 0,9) | A-sd-2 **smentita**; c3, c7 |
| 4 | **Parte da fermo accanto al pannello** (notato dopo): fermo 10 s a 0,33–0,40 m dall'ombra, poi entra | R90 a corpo tutto nascosto **15/141, 21/134, 14/54 (0,11 / 0,16 / 0,26) a 1 / 2 / 3 s** in T; 0,21 / 0,52 / 0,69 in D; puntiforme 0,28 / 0,24 / 0,42 (`fermo_*`). La regione resta sul bordo d'ingresso con scritto «9 su 10», la persona è 1–2 m più in là | §2.1 da riformulare, c5 |
| 5 | **False entrate:** per M1 basta un rilevamento mancato entro 0,40 m dall'ombra | Fermo in piena vista 10 s: **4,7 false entrate a passaggio** (1881 su 400), 9 cambi di stato in mediana contro 4 (21 con rilevamento 0,7). Transiti normali: 92 passaggi su 400 (T), 54 eventi dopo la riemersione | M1 da riformulare, c4 |
| 6 | **Che cosa crede l'osservatore** | Il corpo è **in parte visibile nel 45 / 36 / 21 % dei cicli «previsto»** di un transito normale. «Sbircia» (fermo 5 s a cavallo del bordo): 69 %, mai «osservato», «ampio» prima della ricomparsa in 395 su 395. La regione lo contiene (0,98): la mia previsione (< 0,60) è smentita | Disegno da riformulare, c6 |
| 7 | **Demo: «ampio» prima della ricomparsa** (soglia dell'80 %, area contata come in `comp.c`, fascia compresa) | In D **269/273 «prosegue»** (271/279 fra 0,8 e 1,5 m/s; puntiforme 333/359); tempo mediano all'«ampio» **1,00 s** (nucleo: 0,67 s). Poi la regione è 2,32 m² contro 1,34 d'ombra e la croce sbaglia quanto un segno fisso al centro dell'ombra (0,45 contro 0,41 m; in T, su chi non prosegue, 0,71–0,77 contro 0,63–0,74) | Il segno è continuo; la promessa in demo da riformulare, c8 |
| 8 | **Taratura fuori distribuzione** (T, «prosegue», a 2 e 3 s) | 200 percorsi, stessi camminatori: 0,93 e 0,91. **30 camminate: 0,88 e 0,82**; 30 di calmi su vivaci: **0,73 e 0,67**; 200 di vivaci su vivaci: 0,93 e 0,93, con area 0,32 e 0,49 dell'ombra contro 0,24 e 0,35. Curva dolce a 3 / 6 / 10 °/s: 0,90 / 0,87 / 0,73 a 2 s in T, **0,84 / 0,68 / 0,43 a 3 s in L** | «30 camminate» **smentita**; c9 |
| 9 | **Il punto ibrido** | «Prosegue» con un passo indietro: **29 / 13,5 / 15 %** (M: 18 / 4 / 3,5). Prima misura oltre 0,40 m da R90: ≤ 1 % (regge) | Da dichiarare |
| 10 | **«A prescindere dal sistema»:** maschera ruotata dall'errore d'imbardata (T) | Tremolio di 1° per ciclo (7 cm a 4 m): «prosegue» 0,85 / 0,76 / 0,72 a 1 / 2 / 3 s; 2°: 0,77 / 0,56 / 0,40; scostamento fisso di 3°: 0,64 e 0,53; a 6° **scoperti 267 su 1537**. R100: 0 fuori | In moto R90 **cade**; resta lo strato 1 |

**Dove ho cercato senza rompere.** Strato 1: 0 passaggi con il centro nascosto fuori da R100 in 156 celle di prova (63 file), anche a −20 cm e a 6°. Cicli senza regione: 0. Costo: Python puro 0,6 ms per traccia e ciclo, 1,8 ms con 3 tracce, 5,3 ms (95º: 6,2) con 10 (`tempo_py`); C 0,61 ms con 10: A-sd-7 regge, la mia previsione contraria è smentita. Copertura con maschera esatta e corpo esteso, minimo sul percorso fino a 3 s a corpo tutto nascosto: 0,876 / 0,926 / 0,902, sopra 0,85 e sotto lo «0,96» del §2.1. Un «libero» nato dalla previsione: non trovato, ma nel mio codice è escluso per costruzione. La chiusura 5 del §2.5 non è eseguita.

## 2. Stati proposti

- M7 com'è scritta, regola 2 del §2.5, «30 camminate», A-sd-2: **smentite**.
- Enunciato del §2.1: **sostenuto dai dati** solo con maschera entro pochi centimetri, velocità d'ingresso oltre 0,3 m/s, rotta entro 3 °/s, libreria di circa 200 percorsi dei camminatori giusti.
- M1: **da riformulare**. Strato 1, costo: **reggono**. Sensore in moto: R90 **smentito** già a 1°–2° di tremolio.

## 3. Correzioni obbligate, in ordine (bracci provati DOPO, sugli stessi semi: indizi, non conferme)

| # | Riga riscritta | Prova mia | Ore, fascia |
|---|---|---|---|
| c1 | «Riaggancia la prima misura non tagliata entro 0,40 m da R90 **e entro 0,75 m dall'ombra d'ingresso**; in demo senza il margine dalla portata» | T 398/399, L 332/338; D 136/274 con il margine, **275/277 senza** (`dopo_rh075_*`). **Non provato contro l'estraneo** | 0,5; **14 ore** |
| c2 | «Le pendenti ambigue di un'ombra si fondono in un solo avviso con contatore ed età, senza predittore né croce; non impediscono il riaggancio della traccia più recente; le azzera l'operatore o l'ombra vista libera» | Con c1: D 69/69 riagganci, 0 pendenti; T 112/113, 2 pendenti (`dopo_sess_corr_*`) | 1; **14 ore** |
| c3 | «Un gruppo è tagliato se in immagine confina con un bordo di profondità più vicino, non se tocca celle d'ombra» | **Non provato** | 1–2; **14 ore**, col sensore |
| c4 | «Entrata dopo **due** cicli senza misura; subito solo se il gruppo è tagliato» | False entrate 92 → 7 passaggi su 400; fermo 1881 → 217; scoperti a rilevamento 0,7: 130 → 131 (`dopo_*_m1n2`) | 0,25; **14 ore** |
| c5 | «Sotto 0,3 m/s d'ingresso il segno è subito "ampio"» | Chi parte da fermo, regione mostrata: 0,22 / 0,28 / 0,41 → 0,65 / 0,82 / 0,91: **non basta a 1 s**. «Fermo negli ultimi 2 s → ampio»: non provato | 0,25; **14 ore** |
| c6 | «Il gruppo tagliato si disegna a contorno pieno, "visto in parte", senza velocità; non è una misura» | Non provato | 0,5; **14 ore** |
| c7 | «Una traccia chiusa o non confermata con l'ultima misura entro 0,75 m da un'ombra accende l'avviso, senza previsione» | **Non provato** | 0,5; **14 ore** (sicurezza) |
| c8 | «Soglia di "ampio" sulle sole celle d'ombra; in demo: previsione localizzata per circa 1 s, poi "è dietro"; in "ampio" niente croce» | Attacco 7 | 0,25; **14 ore** |
| c9 | «Libreria di almeno 200 percorsi dei camminatori della prova; "sul percorso" = rotta entro 3 °/s» | 200 contro 30: +5–9 punti | 1 in due; **raffinamento** |
| c10 | «Evidenza negativa solo su celle libere in tutti gli ultimi 3 fotogrammi; in moto la regione è "ampio"» | **Non provato** | **dopo l'hackathon** |

Nelle 14 ore: circa 5 ore-persona in più, quasi tutte righe di regole.

## 4. Da scrivere «non provato»

Sensore vero, falsi rilevamenti, buchi di profondità. C6 sulla maschera vera. Il riaggancio allargato contro un estraneo. Due soggetti insieme nella stessa ombra. Le righe c3, c6, c7, c10. La chiusura 5 e il suo effetto sull'avviso. numpy. Le ore.

## 5. Dopo, e come rifare

1. Rifare gli attacchi 1–5 con c1–c5 insieme, su semi nuovi, da un'altra istanza. 2. Sul sensore, per primi: l'errore della maschera al bordo del pannello (decide l'attacco 3) e la distanza della prima misura valida dall'ombra (decide c1).

**Rifare:** `cd f8-continuita/14-attacco; sh rifai.sh` (63 file, ogni lancio con `timeout 120`, circa 4 minuti in tutto, semi fissati). Impronta del primo giro: `CONGELATO.txt`.
