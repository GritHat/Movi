# Banco di prova indipendente della continuità visiva — `sciame-validazione`, f8, fase f4

Lavoro dalle 16:00 alle 16:40 del 14 novembre 2026 (`date -Is`). Tutto è **simulazione su CPU**: sensore fermo, pannello fermo, soggetto puntiforme, nessun fotogramma vero. Previsioni scritte alle 16:06, prima di ogni riga di codice (`PREVISIONI.md`, con gli esiti in coda); generatore congelato alle 16:10 (`CONGELATO.txt`), predittori e taratura alle 16:20 (`CONGELATO2.txt`), prima di toccare i semi di prova. Tabelle complete: `risultati/TABELLE.txt` (3631 righe) e `risultati/*.tsv`.

## 0. In testa: cambi di stato, scostamenti, regole violate

- **Cambi di stato.** La regola attuale del nucleo **non rispetta l'imperativo** (F-201 confermato da un quinto codice). **C-EST com'è scritta non lo rispetta** fuori dalla geometria della demo. **C-004 (fronte + scia) regge**, con un parametro in più da tarare. Undici mie previsioni su diciotto sono smentite, in tutto (P-val-3, 4, 8, 14) o in parte (1, 5, 6, 7, 11, 12, 15).
- **Codice toccato dopo la prova.** Alle 16:31 ho aggiunto a `banco.c` il braccio «rumore noto» (R del filtro dalla curva). La copia usata per la prova è `banco_congelato_1620.c`; rifatta la prova T con il codice nuovo, l'uscita è identica riga per riga (`diff`: nessuna differenza). I semi di prova sono quindi stati letti due volte dallo stesso calcolo, e riusati per rilevamento 1 e per i bracci (confronti appaiati).
- **Taratura decisa dopo un fallimento visto.** Sui semi di sviluppo (5000–5059) C-004 con una passata di lisciatura copriva 0,74–0,85: ho reso la lisciatura un parametro e l'ho scelta sui semi di taratura con una regola scritta prima di guardarli (il minimo fra 1 e 4 passate con ogni cella sul percorso ≥ 0,88 in D e T: **3**).
- **Protocollo non rispettato alla lettera.** «In vista ≥ 2 s» non sta nelle geometrie: mediana 1,1 s (D), 1,9 s (T), 1,3 s (L). τ = 0,5 s è il ciclo 8 (0,53 s). Griglia cartesiana da 0,10 m, non polare. In D l'1–3 % dei passaggi è scartato (traccia con meno di 4 misure).
- **Non eseguiti:** corpo largo 0,45 m; C-002; S2 (K-210); i 30 passaggi reali dell'attacco 5; «escono due» solo in una forma (uno sconosciuto fermo nell'ombra che esce per primo).
- Un file di controllo sta nella cartella provvisoria della sessione, fuori dalla mia. Di `sim_v2.py` ho letto `KF1`, `Geo`, `pass_v2`: la mia `dist_wedge` ha la stessa struttura di `Geo.d_est`.

## 1. Che cosa è il banco

`gen.h` (188 righe, mio): una persona con velocità 0,3–1,8 m/s e rotta ± 15°, fluttuazioni lente (6 %, 3°), ondeggiamento del passo (2 cm), **una** manovra a un istante uniforme nel tratto nascosto, raggiunta con un ritardo del primo ordine; sette comportamenti del triage più tre per gli attacchi. Misura: 5 cm per asse, rilevamento 0,9 (e 1; bracci 0,7 e curva 4/9/16 cm), C6 come «nessuna misura entro 0,22 m dall'ombra stimata». `banco.c` (599 righe): filtro del nucleo (q = 0,2) in vista, uguale per tutti; poi i predittori, riscritti dalle sole descrizioni a parole; la valutazione legge le celle emesse e non il loro codice. Semi: sviluppo 5000+, taratura 1000–1199 (D e T), prova 9000–9399 (**400 passaggi per comportamento e geometria**; L mai tarata), attacchi 9500–9899. Unità: il passaggio; la copertura a τ conta i passaggi ancora nascosti a τ e dentro la griglia (chi è oltre la portata è «non osservato»: lo copre solo R100).

**Letture mie, dove il testo non decide.** *L0:* cerchio al 95 % ritagliato sul cuneo, finché copre meno di metà del cuneo, poi «perso». *C-005:* R90(τ) = massimo dei quantili conformi sui cinque comportamenti sul percorso; R50(τ) = mediana pesata sulla «squadra». *C-004:* 200 + 200 membri, percorsi residui registrati dai «prosegue» di taratura; peso × 0,1 **cumulato** per ogni ciclo su celle viste libere; regione = unione delle celle più dense dei due scenari dopo tre passate 3×3; fantasma = media dello scenario più pesante, al più 0,167 m per ciclo. *C-001:* 2000 particelle, sosta 0,25/s, ripartenza 0,4/s, due lisciature. *C-EST:* smorzamento 0,90 (A) o 0,95 (B); pesi come nel triage; σ_eff ed ellisse dai momenti della miscela ritagliata; qui con la fascia di 0,20 m, e a parte «senza fascia» come è scritta.

## 2. I numeri che decidono (rilevamento 0,9; tre valori = D / T / L)

| Misura (soglia del triage) | L0 nucleo | Filtro ritagliato | C-005 | **C-004** | C-001 | C-EST A | C-EST B |
|---|---|---|---|---|---|---|---|
| Cicli senza osservazione con una regione, % | **19 / 38 / 33** | 97 / 99,5 / 100 | 99,2 / 99,8 / 100 | 99,9 / 100 / 100 | 100 / 100 / 100 | 100 / 97 / 72 | 100 / 72 / 43 |
| Passaggi con un vuoto, su circa 2000 (C1a: 0) | 1958 / 1991 / 1999 | 148 / 70 / 21 | 69 / 46 / 10 | 11 / 9 / 2 | 6 / 4 / 1 | 2 / 374 / 1976 | 2 / 1312 / 1987 |
| … di cui dopo i primi 5 cicli | 1858 / 1707 / 1989 | 111 / 19 / 0 | 37 / 12 / 0 | 2 / 0 / 0 | 2 / 0 / 0 | 2 / 374 / 1976 | 2 / 1312 / 1987 |
| Prima misura entro 0,40 m da R90 (C1c ≥ 0,90) | 0,06 / 0,18 / 0,01 | 0,86 / 0,86 / 0,83 | 0,93 / 0,91 / 0,88 | 0,995 / 0,998 / 0,996 | 1,00 / 0,998 / 1,00 | 0,86 / 0,50 / 0,17 | 0,96 / 0,58 / 0,02 |
| R90: minimo sul percorso fino a 3 s (C3 ≥ 0,85) | 0,00 | 0,74 / 0,81 / 0,91 | 0,89 / 0,90 / 0,96 | **0,935 / 0,959 / 0,939** | 0,946 / 0,993 / 0,998 | 0,65 / 0,35 / 0,02 | 0,93 / 0,01 / 0,00 |
| Celle sul percorso smentite, su 25 (fino a 5 s) | 23 / 15 / 17 | 9 / 4 / 0 | 1 / 0 / 0 | **0 / 0 / 0** | 0 / 0 / 0 | 4 / 11 / 15 | 0 / 10 / 15 |
| Area di R90 / ombra a 2 e 3 s, in T; in L (≤ 0,60) | — | 0,81 1,11; 0,63 1,02 | 1,07 1,23; 0,85 1,13 | **0,27 0,36; 0,18 0,30** | 0,62 0,75; 0,50 0,70 | 0,79 0,57; 0,61 0,32 | 0,90 1,04; 0,61 — |
| R90 a 2 s per «svolta» e «lontano», in T | 0,03 0,03 | 0,87 0,85 | 0,95 0,94 | **0,58 0,54** | 0,79 0,74 | 0,72 0,71 | 0,88 0,90 |
| R50 sulla «squadra» a 1 / 2 / 3 s, in T (0,40–0,60) | — | 0,92 0,86 0,80 | 0,54 0,57 0,57 | 0,85 0,68 0,65 | 0,96 0,87 0,66 | 0,94 0,70 0,27 | 0,93 0,82 0,14 |
| Punteggio logaritmico, «squadra», 1 / 2 / 3 s, T | 0,80 2,52 2,53 | 0,18 1,83 2,59 | −0,13 1,31 1,89 | **−0,19 0,97 1,40** | 0,25 1,38 1,78 | 0,16 1,91 2,69 | 0,11 1,59 2,40 |
| Tempo per ciclo, 95º percentile, 1 e 10 tracce (L), ms | basi insieme: 0,03 e 0,28 | | | 0,16 e 1,42 | 0,20 e 1,98 | quattro varianti: 0,04 e 0,41 | |

Intervallo della cella peggiore di C-004 fino a 3 s: D 86/92 [0,865–0,970], T 370/386 [0,934–0,974], L 357/380 [0,911–0,959]; a 5 s il minimo è 0,905 (L, «rallenta», 248/274). Codice, in istruzioni C (indicative, compresa la parte comune di lisciatura e ordinamento): C-005 circa 30 con la taratura, C-004 circa 85, C-001 circa 105, C-EST circa 70 per una lettura. **R100 contiene il soggetto nel 100 %** dei passaggi di ogni cella, compresi «svolta» e «lontano»; **0 cicli** con celle di R90 su spazio visto libero oltre la fascia e 0 con R90 fuori da R100, per ogni predittore ritagliato (per costruzione, ricontato dal valutatore). Il raggiungibile ∩ non visto (L3) contiene il nascosto nel 100 %, ma da 2 s è tutta l'ombra con la sua fascia (1,2–1,7 volte l'ombra).

**Il punto** (T, «squadra»; ultima colonna: «prosegue»):

| Punto | Errore mediano a 1 / 2 / 3 / 5 s, m | Peggior rapporto con la migliore base | Passaggi con un passo > 0,167 m | «Prosegue» con un passo indietro | Cicli su celle viste libere | Salto mediano alla ricomparsa |
|---|---|---|---|---|---|---|
| fermo (L1) | 0,97 1,53 1,64 2,04 | — | 0 | 0 % | 41 % | 2,56 m |
| velocità costante (filtro, C-005) | 0,19 0,39 0,67 1,48 | 2,87 | 0 | 0 % | **22 %** | 0,39 m |
| fantasma di C-004 | 0,19 0,51 0,67 1,06 | 1,96 | 0 | **67 %** | 0,03 % | 1,32 m |
| media condizionata (C-008) | 0,17 0,45 0,62 0,96 | 1,82 | 0 | 0,2 % | 0,01 % | 1,12 m |
| ibrido (C-009) | 0,18 0,37 0,53 0,82 | **1,00** | 0 | 14,5 % | 4,3 % (77 % dei passaggi) | 0,38 m |

**Bracci (T), minimo di R90 sul percorso fino a 3 s** per C-005 / C-004 / C-001: rilevamento 1: 0,90 / 0,97 / 0,99; rilevamento 0,7: 0,91 / 0,96 / 0,99; ombra stimata a −20 cm **con** la fascia: 0,835 / 0,970 / 0,990, e il ritaglio toglie il vero in 28 passaggi su 2800; **senza** fascia: 0,81 / **0,68** / 0,83 e 2799 su 2800 (fallisce, come deve: il banco non è cieco); rumore 4/9/16 cm con filtro e taratura fermi a 5 cm: **0,30 / 0,44 / 0,75**; lo stesso con R dalla curva e taratura rifatta: 0,92 / 0,87 / 0,99. Braccio q = 0,01: 14 celle su 20 smentite, ma «prosegue» a 2 s resta 0,99: **su chi prosegue il banco non distingue un filtro troppo sicuro** (i miei «prosegue» sono regolari).

## 3. Le risposte

**La regola attuale del nucleo rispetta l'imperativo? No.** Emette una regione nel 19–38 % dei cicli senza osservazione; quasi ogni passaggio ha un vuoto (1991 su 2000 in T); a 2 s il suo «95 %» contiene il soggetto nello 0,01–0,06 dei casi, perché non c'è più. In demo (D, con C6) il «previsto» dura 0,67 s in mediana (quartili 0,60–0,73) e «metà dell'ombra» scatta prima della ricomparsa in 332 transiti su 355. Lo strato 1 regge (R100: 100 %).

**Quale candidata lo rispetta.** **C-004**, per la regione: stima a ogni ciclo, copertura sul percorso ≥ 0,935 fino a 3 s e ≥ 0,905 fino a 5 s in tre geometrie (una mai tarata), regione fra un quinto e un terzo dell'ombra in T e L, miglior punteggio fra candidate e basi da 1 s in poi, 0,16 ms. (Il braccio q = 0,01, che deve fallire, ha un punteggio migliore a 1–2 s: −1,34 e 0,71 in T. Il punteggio del triage premia la regione stretta su una miscela con il 60 % di «prosegue»: da solo non decide, va letto con la copertura per cella.) Passa la regola della scadenza: a pari copertura la sua R90 è il 25–29 % di quella di C-005 (T), il 58–63 % in D. C-001 copre di più (≥ 0,946) con un'area 1,3–2,8 volte maggiore e più codice: non passa la regola. **C-005** copre (≥ 0,89) ma da 2 s è tutta l'ombra, e lascia vuoti nel 0,5–3,5 % dei passaggi (il disco non tocca più l'ombra): vale come ripiego, con un pavimento.

**Dove C-004 cede.** (1) Chi lascia il percorso: 0,58 e 0,54 a 2 s, 0,42–0,49 a 5 s: lì vale solo R100. (2) Il suo punto: torna indietro nel 55–67 % dei «prosegue» e salta di 1,3 m alla ricomparsa. (3) R50 non è un 50 % (0,94 → 0,46): un solo livello, detto «almeno 90 %, sul percorso». (4) La taratura non segue un rumore diverso se R non si rimisura (0,44). (5) Senza fascia e con l'ombra a −20 cm: 0,68. (6) In demo l'ombra è 1,36 m²: da 2 s la regione ne è il 90–100 %; lì dice «è ancora dietro», non «dove». (7) Alla lettera C1a è smentita: vuoti di un ciclo all'ingresso nello 0,1–0,6 % dei passaggi, e in D 2 passaggi su 1958 con un vuoto lungo (il soggetto esce dalla portata prima dell'ombra: per B5 sarebbe una chiusura motivata). (8) Con una sola passata di lisciatura il minimo è 0,78–0,83 (semi di taratura): il 99–100 % dell'autore non si rifà senza quel parametro.

## 4. C-EST e i tre attacchi della preproposta

**Com'è scritta, C-EST è smentita in T e L e regge in D.** La soglia σ_eff ≤ 0,8 m riporta il difetto del nucleo, spostato a circa 2 s: passaggi con cicli «perso» 374 e 1312 su 2000 in T (letture A e B), 1976 e 1987 in L, 2 in D. Su «sosta» a 3 s (K-206): 0,95 e 1,00 in D, **0,72 e 0,53 in T, 0,14 e 0,00 in L**. La lettura A (pesi cumulati) lascia il transito troppo presto: «prosegue» a 3 s 0,38 in T; il suo centro arretra nel 92 % dei «prosegue» (T). Senza fascia, com'è scritta: minimo 0,62 (D), 0,18 (T).

- **Attacco 1** (200 semi; D e T): cicli di «previsto» su celle libere **0** (regge, per costruzione); transito dominante oltre 0,5 s dopo l'uscita attesa: lettura A 1 e 0 passaggi su 200, lettura B 1 e **89**; vero dentro la regione fra 0,5 e 3 s: 0,99–1,00. Lo scenario scelto è favorevole: a 1,2 m/s l'ipotesi smorzata della lettura A si ferma dopo 0,72 m, quasi a metà pannello in D. Con soste a un punto qualunque e altre velocità valgono i numeri sopra.
- **Attacco 5.** Prima misura nell'ellisse al 95 % dichiarata, su «prosegue»: A **0,28 / 0,30 / 0,00**, B 0,997 / **0,71 / 0,00**; sulla «squadra» B 0,95 / 0,63 / 0,00. Smentita, salvo la lettura B in D. Per confronto la porta del filtro del nucleo dà 1,000 su «prosegue» (troppo larga) e 0,44–0,57 su «torna».
- **Attacco 2** (200 semi). *Velocità tripla:* la regola geometrica del nucleo riaggancia 123 su 197 (D) e 193 su 200 (T) senza guardare la cinematica; la porta del filtro ne lascia passare 176 su 200; R90 di C-004 dilatata di 0,40 m solo 11 su 200 (29 su 197 in D): come porta, **segnala il conflitto**. *Entra uno, escono due:* lo sconosciuto esce per primo in 193 casi su 199 (T); il nucleo gli dà l'identità del primo in **193 su 193** (136 su 182 in D) e rilascia l'avviso con il primo ancora nascosto. Le celle restano «in ombra», mai «libero»; cade l'avviso. Nessuna porta lo evita (C-004: 158 su 193).

## 5. Soglie del triage, K e stati

| Soglia | Esito |
|---|---|
| C1a, 0 passaggi con un vuoto | L0, C-EST **smentita**; C-005 **smentita** (37 e 12 dopo 5 cicli); C-004, C-001 **smentita alla lettera**, 0 dopo 5 cicli in T e L |
| C1b, passi e arretramenti | **regge** per C-008 in T e L (in D un passaggio con un passo lungo); **smentita** per il fantasma, l'ibrido, C-EST A |
| C1c ≥ 0,90 | **regge** C-004, C-001; C-005 no in L (0,88) |
| C2, 0,5 m a 1 s e 1,0 m a 2 s | **regge** per i punti della tabella (0,17–0,19 e 0,37–0,51 m in T); «non peggiore del filtro a 2 s»: regge l'ibrido, no C-008 (0,45 contro 0,39) |
| C3, R90 ≥ 0,85 sul percorso | **regge** C-004, C-001; C-005 regge fino a 3 s; L0, C-EST **smentita** |
| C3, miscele 0,85–0,97 | **smentita** per eccesso: C-004 e C-001 a 0,5–1 s (0,98–1,00), C-005 da 2 s (0,98–0,99) |
| C3, R50 0,40–0,60 | **regge** solo C-005 dove è tarata (D, T); in L 0,53–0,69 |
| C3, area ≤ 0,60 in T e L | **regge** solo C-004 |
| C4, 0 cicli di R90 su libero; R90 ⊆ R100 | **regge**; «il punto mai su libero»: **smentita** per tutti (C-008: 18 cicli) |
| C4, il ritaglio non toglie il vero | **smentita** di poco: 22/2737 (D), 1/2800 (T), 0 (L), per 0,20 contro 0,22 m |
| C6 ≤ 6,7 ms | **regge in C** (tutti insieme, dieci tracce: 3,98 ms); in Python **non verificato** |

K-201 no (in T e L). K-202 sì: 93,5 %; con C-004 la regione supera metà dell'ombra nel 7 % dei cicli in T e nel 79 % in D: la soglia «ampio» va data in metri o per installazione. K-203 **sì**: baricentro e ibrido non superano 1,07 volte la migliore base. K-204 sì. K-205 sì (area 0,44–0,48 delle particelle). K-206 no in T e L. K-207 sì per la geometria (0,958 in L), **no per il rumore**. K-208 no, salvo C-005 dove è tarata. K-210 **non risolta**. K-211: 0,67 s, non 0,40–0,53.

## 6. Proposte, con le ore [val., stime mie non verificate; squadra di 5]

- **validazione-1, la composizione che il banco sostiene.** *14 ORE, indispensabile (6–8 ore-persona):* «perso» non assorbente e R100 intatta; regione = C-005 con il pavimento «se il disco non tocca l'ombra, R90 = ombra»; punto = filtro finché sta su celle non viste libere, poi baricentro con passo limitato; registro per ciclo. *14 ORE se una persona è libera dall'ora 6 (4–5 ore), altrimenti DOPO:* C-004 dietro la stessa interfaccia (un insieme di celle), tre passate, un livello. *DOPO:* C-001. *Non adottare:* C-EST com'è; della preproposta resta l'etichetta di S5 senza «conf Z%», che non ha definizione. **Previsione:** con il pavimento i vuoti di C-005 dopo 5 cicli vanno a 0 e la copertura non scende. **La smentisce** un passaggio con un vuoto, o una cella sotto 0,85.
- **validazione-2, il riaggancio non toglie l'avviso da solo.** Porta = R90 dilatata di 0,40 m; fuori porta «identità ambigua» e l'avviso resta. Copre la velocità tripla (94,5 %), **non** «escono due» (82 % dentro la porta): quello resta un limite da dichiarare. *14 ORE (1 ora).*
- **validazione-3, taratura e accettazione sul sensore.** *4 ORE:* misurare il rumore, mettere R, registrare 20–30 camminate dritte per la libreria o la tabella (numero **non verificato**). Accettazione per comportamento con l'occlusione virtuale: 54 dentro su 60 per cella (passa nel 3 % dei casi se il vero è 0,80, nel 97 % se è 0,95; conto binomiale).

## 7. Che cosa il banco condivide con le candidate, e quindi non esclude

La **specifica**: i sette comportamenti sono quelli per cui le candidate sono nate (la scia di C-004 è «si ferma sul percorso»). Il **rumore** gaussiano, bianco, noto al filtro; nessun valore anomalo, nessun falso rilevamento, nessun buco di profondità. Il **soggetto puntiforme**: niente corpo tagliato, niente occlusione parziale; l'errore della maschera solo come −20 cm uniformi. **Sensore e pannello fermi**, una traccia pendente, percorsi che attraversano a ± 15°. Il **filtro d'ingresso** del nucleo, comune a tutti. La **libreria** di C-004 viene dal mio stesso generatore. Lo **stesso modello linguistico** ha scritto candidate, protocollo e banco: una lettura sbagliata comune non si vede.

## 8. Dopo, e come rifare

1. Torneo: attaccare C-004 con corpo largo, due tracce nella stessa ombra, chi accelera in ombra. 2. Provare il pavimento di C-005 e il punto ibrido senza i 3 cicli su libero. 3. Sul sensore: rumore, poi la scheda per comportamento.

**Rifare** (in questa cartella; ogni lancio ≤ 55 s, uno alla volta): `sh rifai.sh`, cioè `gcc -O2 -o banco banco.c -lm`; `./banco tara`; `./banco prova T 0.9 0 0.20 0 9000 400 0123456 T09` (geometria, rilevamento, errore dell'ombra, fascia, curva, primo seme, numero, comportamenti, etichetta); `./banco tempo L 10`; `python3 tabelle.py > risultati/TABELLE.txt`. Impronte: `CONGELATO3.txt`.
