# Previsioni — `sciame-statistico`, f8, fase f4 (analisi dei numeri)

Scritte alle **2026-11-14T16:53:22+01:00** (`date -Is`), PRIMA di aprire un file `.tsv`, `TABELLE.txt`, `LETTURA.txt`, `TORNEO.md` o un sorgente del banco.
**Non sono cieche** rispetto a: `CONTRATTO_CONTINUITA.md`, `04-statistico/CONSEGNA.md`, `10-triage/TRIAGE.md`, `11-misure/BANCO_DI_PROVA.md`, `13-soluzione/MODIFICHE_CONTINUITA.md`, già letti per intero. Sono cieche rispetto ai conteggi grezzi, al torneo e a ogni mio lancio.

| # | Previsione | Misura | Soglia di smentita |
|---|---|---|---|
| P-st-1 | I conteggi della cella peggiore di C-004 fino a 3 s dichiarati dal banco (D 86/92, T 370/386, L 357/380) si ritrovano identici nei file grezzi | conteggio mio dai `.tsv` | anche uno solo diverso di ≥ 1 unità |
| P-st-2 | Con la lettura severa «il limite inferiore di Wilson al 95 % sta sopra 0,85», C-004 (banco) NON regge in tutte le celle sul percorso fino a 3 s: almeno una cella in D è «non risolta» | Wilson per cella, prova_D | smentita se tutte le celle hanno limite inferiore ≥ 0,85 |
| P-st-3 | La differenza fra banco (0,935) e prova delle modifiche (0,849) sulla cella peggiore di D a 3 s è compatibile con il caso una volta contate le celle confrontate: p fra 0,01 e 0,20 nel test esatto a due proporzioni, e le due celle peggiori non sono lo stesso comportamento | test di Fisher sui conteggi grezzi | p < 0,001 (differenza vera) |
| P-st-4 | Su semi miei mai usati (20000 in poi), con il codice delle modifiche ricompilato nella mia cartella, il minimo sul percorso fino a 3 s di `sd-1` in D sta fra 0,85 e 0,92 | lancio mio, n ≥ 800 per comportamento se sta nei 2 minuti | fuori da [0,85; 0,92] |
| P-st-5 | Idem in T e L: minimo fra 0,91 e 0,97 | lancio mio | fuori dall'intervallo |
| P-st-6 | Per dichiarare una copertura vicina a 0,90 con semiampiezza di Wilson ≤ 0,10 servono 35–40 occlusioni per cella dichiarata; nel caso peggiore (p = 0,5) 93–97 | conto esatto | fuori dagli intervalli |
| P-st-7 | Sotto spostamento (i bracci del torneo: altra miscela, altro generatore, ombra spostata, velocità fuori taratura) almeno una cella sul percorso fino a 3 s di C-004 è SMENTITA anche con l'intervallo (limite superiore di Wilson < 0,85) | conteggi del torneo, se ci sono | nessuna cella con limite superiore < 0,85 |
| P-st-8 | Il punteggio logaritmico di C-004 sulla «squadra» in T (−0,19 / 0,97 / 1,40 a 1 / 2 / 3 s) si ricalcola dai grezzi entro 0,02; se i grezzi non portano l'anello per passaggio, esito «non ricalcolabile» | conto mio | scarto > 0,02 |
| P-st-9 | Almeno una soglia o un livello delle modifiche è stato scelto DOPO aver visto i dati di prova (orizzonte 3 s, soglia 80 %, enunciato «fino a 1 s in demo»): lo si legge nei tempi dei file e nelle dichiarazioni | lettura di `PREVISIONI.md` di 13-soluzione contro l'ora dei risultati | smentita se l'enunciato §2.1 era scritto prima del lancio |
| P-st-10 | R50 di `sd-1`/C-004 non è un 50 %: sulla «squadra» in T a 1 s contiene > 0,75; in nessuna geometria sta in 0,40–0,60 a tutti e tre gli orizzonti | conteggi grezzi | smentita se una geometria sta in 0,40–0,60 a 1, 2 e 3 s |

Esiti: in coda, dopo le prove, senza toccare le righe sopra.

## Seconda serie — scritta alle 2026-11-14T16:55:08+01:00, dopo aver letto `TORNEO.md`, `13-soluzione/PREVISIONI.md`, `gen.h` e le intestazioni dei `.tsv`; prima di ogni mio lancio e di ogni mio conteggio

Notato leggendo `gen.h`: i percorsi di libreria di C-004 e i passaggi di prova vengono dallo stesso generatore (fluttuazione della velocità 6 %, della rotta 3°, rotta entro ± 15°). Il torneo ha un generatore suo, ma anche lì la libreria viene dal generatore della prova. **Nessuna prova ha la libreria da un generatore e i passaggi da un altro.**

| # | Previsione | Misura | Soglia di smentita |
|---|---|---|---|
| P-st-11 | **Spostamento mio, taratura ferma.** Copia di `gen.h` con camminatori meno regolari (fluttuazione della velocità 15 % invece di 6 %, della rotta 8° invece di 3°, rotta entro ± 30° invece di ± 15°), `taratura.txt` NON rifatta, semi 30000–30399: `sd-1` perde copertura. «Prosegue» a 2 s in T fra 0,75 e 0,92; il minimo sul percorso fino a 3 s scende sotto 0,85 in almeno una geometria | lancio mio in `codice_spostato/` | «prosegue» a 2 s in T ≥ 0,93 **e** minimo ≥ 0,85 in D, T, L (la taratura regge lo spostamento) |
| P-st-12 | Il mio `comp` ricompilato, sui semi 9000–9399 in D, ridà per C-004 le stesse righe H del banco (stesso codice, stessi semi): 35 righe su 35 identiche in n e in90 | `diff` dei campi | una riga diversa |
| P-st-13 | Riunendo banco, modifiche e semi miei (stesso codice, semi diversi), la cella «prosegue» a 3 s in D di C-004 ha copertura fra 0,86 e 0,91 e l'eterogeneità fra i tre lanci non è significativa (chi quadrato a 2 gradi, p > 0,01) | conteggi riuniti | p < 0,01 o stima fuori |
| P-st-14 | Il contatore dal vivo proposto («ricomparso dentro la zona», cioè prima misura entro 0,40 m da R90) NON misura la copertura dichiarata: nei grezzi vale ≥ 0,98 sul percorso anche nelle celle dove R90 contiene < 0,90, e resta ≥ 0,60 per chi svolta o esce lontano dove R90 a 2 s contiene < 0,60 | `re40/nre` contro `in90/n` | smentita se i due numeri differiscono di meno di 0,05 sul percorso in D a 3 s |

## Terza serie — scritta alle 2026-11-14T17:07:53+01:00, dopo il primo riconteggio (uscite già viste: `ris/TABELLE_STATISTICO_*.txt`, sezioni 0–3) e dopo aver riletto `rng_seed` in `gen.h`; prima della prova che la decide

Letto nel codice, non ancora provato: `rng_seed` mette lo stato a seme × G + costante, e `rng_u64` avanza lo stato di G a ogni chiamata, con lo stesso G. Quindi il flusso del seme s+1 è il flusso del seme s spostato di una chiamata: i 400 passaggi di un lancio (semi consecutivi) leggono finestre scorrevoli degli STESSI numeri casuali. Se è così, i passaggi non sono indipendenti e gli intervalli binomiali con n = 400 sono troppo stretti.

| # | Previsione | Misura | Soglia di smentita |
|---|---|---|---|
| P-st-15 | Con `traj_make` su semi consecutivi, il numero uniforme che dà la rotta del seme s è lo stesso che dà la velocità del seme s+1 (scarto < 1e-9), per 6 semi su 6 | programma mio `prova_semi.c` che include `gen.h` | uno scarto ≥ 1e-9 |
| P-st-16 | **Sovradispersione.** Su 10 blocchi da 400 semi consecutivi in D (banco 9000, modifiche 12000, e otto miei da 40000 a 75000 a passo 5000, lontani fra loro più dei circa 3500 numeri che un passaggio consuma), la varianza fra blocchi della copertura di `sd-1`/C-004 supera quella binomiale: media di chi²/gradi sulle 20 celle sul percorso fino a 3 s fra 1,3 e 4 | chi quadrato di omogeneità a 9 gradi per cella, denominatore «tutti» | media ≤ 1,15: la dipendenza non allarga gli intervalli, e lo scrivo |

## Quarta serie — scritta alle 2026-11-14T17:11:40+01:00, dopo aver visto la sovradispersione (sezione 4b) e prima di riparare i semi

| # | Previsione | Misura | Soglia di smentita |
|---|---|---|---|
| P-st-17 | **Semi riparati** (copia `codice_semi/gen.h`: lo stato iniziale passa per la funzione di mescolamento, così i semi consecutivi danno flussi diversi; taratura RIFATTA con gli stessi semi 1000–1199, tre passate, nessun altro ritocco). (a) Le coperture restano dentro gli intervalli per blocchi: in D, «tutti», «prosegue» a 3 s fra 0,83 e 0,93; minimo sul percorso fino a 3 s in T ≥ 0,93 e in L ≥ 0,91. (b) La sovradispersione sparisce: su 5 blocchi D da 400 semi, media di chi²/4 sulle celle sul percorso fino a 3 s fra 0,6 e 1,5 | lanci miei in `codice_semi/`, semi 80000+ | (a) un valore fuori; (b) media > 1,5 (la dipendenza non veniva dai semi) |

## Quinta serie — scritta alle 2026-11-14T17:17:40+01:00, dopo aver visto lo spostamento con i semi originali (sezione 5a): è una ripetizione, non una prova cieca

| # | Previsione | Misura | Soglia di smentita |
|---|---|---|---|
| P-st-18 | Lo stesso spostamento (15 %, 8°, ± 30°) con i **semi riparati** e la taratura riparata ferma (`codice_semi_spostato/`, semi 90000–90399) ridà il quadro: in T il minimo sul percorso fino a 3 s resta ≥ 0,90; in L «prosegue» a 3 s sta fra 0,65 e 0,85 con il limite superiore di Wilson sotto 0,85. In D lo spostamento non è interpretabile (a ± 30° chi cammina verso il sensore urta la linea del pannello, a 0,4 m, e chi se ne allontana esce dalla portata di 3 m): lo riporto senza usarlo | lancio mio | T sotto 0,90, o L «prosegue» a 3 s ≥ 0,85 |

## Esiti — scritti alle 2026-11-14T17:23:30+01:00. Prove: `ris/TABELLE_STATISTICO_griglia.txt` e `ris/TABELLE_STATISTICO_tutti.txt` (sezione fra parentesi), `ris/prova_semi.txt`

| # | Esito | Numeri |
|---|---|---|
| P-st-1 | **regge**, con la definizione del banco | 86/92, 370/386, 357/380 ritrovati (sez. 2). Con il denominatore delle modifiche la prima è 86/98 |
| P-st-2 | **smentita** con la definizione del banco (20 celle su 20 reggono in D, T, L); regge con quella delle modifiche (D: 19 reggono, 1 non risolta) | sez. 3 |
| P-st-3 | **smentita** nei due capi | Fisher banco–modifiche p = 0,52 («griglia») e 0,56 («tutti»): nessuna differenza, non «fra 0,01 e 0,20»; e la cella peggiore è la stessa («prosegue» a 3 s). La differenza 0,935 contro 0,849 è di definizione (sez. 2, coda) |
| P-st-4 | **regge** | D, semi 20000–21199: minimo fino a 3 s 302/332 = 0,910 («tutti»), 302/329 = 0,918 («griglia») |
| P-st-5 | **regge** | T 445/464 = 0,959; L 746/787 = 0,948 |
| P-st-6 | **regge** | 38 a 0,90 osservato; 93 a 0,50 (sez. 7) |
| P-st-7 | **regge** | torneo: ombra stimata a −20 cm 28/53 = 0,53 [0,40–0,66] e 39/53 = 0,74 [0,60–0,84]; corpo largo senza C6 41/63 = 0,65 [0,53–0,76]; maschere congelate 43/96 (sez. 5c). Lo spostamento di velocità e miscela (a14) resta non risolto: 115/128 = 0,898 [0,834–0,940] |
| P-st-8 | **regge**, ma dalle medie di cella | −0,19 0,97 1,40 ritrovati (sez. 2); i grezzi non portano il punteggio per passaggio: nessun intervallo |
| P-st-9 | **regge** | `MODIFICHE_CONTINUITA.md` §5, punto 7 («scelti da me sui numeri del §2, non tarati»); file dei risultati alle 16:43–16:45, enunciato del §2.1 scritto dopo (file alle 16:52) |
| P-st-10 | **regge** | R50 di C-004, «squadra»: T 0,85 a 1 s; D 0,74 / 0,63 / 0,59; L 0,86 / 0,71 / 0,62 (sez. 3). `sd-1` e `sd-0` non emettono R50 |
| P-st-11 | **mista** | T: «prosegue» a 2 s 258/266 = 0,970, sopra lo 0,75–0,92 previsto (clausola smentita). L: «prosegue» a 3 s 0,748 («tutti»), 0,880 («griglia»). D non interpretabile (vedi P-st-18) |
| P-st-12 | **regge** | 35 righe su 35 identiche in tutti i campi (sez. 0) |
| P-st-13 | **regge** | «tutti»: 489/549 = 0,891, chi²(2) = 3,55, p = 0,17; «griglia»: 489/526 = 0,930, p = 0,30 (sez. 4). Ma su tutte le celle sul percorso i tre lanci sono eterogenei in 19 celle su 75 («tutti») e 11 su 75 («griglia»), contro 3,8 attese: è la sovradispersione di P-st-16 |
| P-st-14 | **regge** | D, sul percorso: contatore 4771/4801 = 0,994 contro copertura a 3 s 0,940 («tutti»); «prosegue» in D: 0,992 contro 0,894. Svolta e lato lontano: contatore 0,977 (D) e 0,719 (T) contro copertura a 2 s 0,43 e 0,52 (sez. 6) |
| P-st-15 | **regge** | 6 coincidenze su 6; 1000 numeri uguali su 1000 fra i flussi dei semi 9000 e 9001 (`ris/prova_semi.txt`) |
| P-st-16 | **regge** | media di chi²/9 sulle 20 celle sul percorso fino a 3 s: 2,67 («tutti»), 1,62 («griglia»); massimo 6,02; «prosegue» a 3 s da 0,726 a 0,977 fra i dieci blocchi (sez. 4b) |
| P-st-17 | (a) **smentita in T di quattro millesimi**, regge in D e L; (b) **regge** | (a) D «prosegue» a 3 s 461/513 = 0,899; T minimo 437/472 = 0,926 (previsto ≥ 0,93); L 711/774 = 0,919. (b) media di chi²/4: 0,94 («tutti»), 1,00 («griglia») (sez. 4c) |
| P-st-18 | **smentita in T**, regge in L | T minimo fino a 3 s 223/257 = 0,868 [0,821–0,904] (previsto ≥ 0,90); L «prosegue» a 3 s 226/312 = 0,724 [0,672–0,771] («tutti»), 226/282 = 0,801 [0,751–0,844] («griglia») (sez. 5a) |

**Notato dopo, senza previsione.** (1) Le due definizioni del denominatore (il banco toglie i nascosti usciti dall'area osservata, le modifiche no). (2) La regola del triage per 30 ≤ n ≤ 199 ammette insieme «regge» e «smentita» e tace fra 200 e 399. (3) Con la taratura rifatta (un'altra libreria di 200 percorsi) una cella si sposta di quattro centesimi (T, «rallenta» a 3 s: 929/960 = 0,968 sui semi originali, 437/472 = 0,926 sui riparati): la copertura dipende anche dalla libreria estratta, e nessuno ha misurato quanto.
