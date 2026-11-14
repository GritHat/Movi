# Analisi dei numeri della continuità visiva — `sciame-statistico`, f8, fase f4

Lavoro dalle 16:52 alle 17:30 del 14 novembre 2026 (`date -Is`). **Tutto è simulazione su CPU, sensore fermo, soggetto puntiforme: niente è misurato su un sensore.** Sigle: **B** = `11-misure/BANCO_DI_PROVA.md`; **M** = `13-soluzione/MODIFICHE_CONTINUITA.md`; **To** = `12-torneo/TORNEO.md`; **Tab n** = sezione n di `ris/TABELLE_STATISTICO_tutti.txt` e `…_griglia.txt` (due denominatori, vedi 0.2). Tre valori separati da «/» = geometrie D / T / L. «Sul percorso» = prosegue, rallenta, sosta, torna, sosta lunga. Intervalli di Wilson al 95 %: **regge** se il limite inferiore supera la soglia, **smentita** se il superiore sta sotto, altrimenti **non risolta**.

## 0. In testa: cambi di stato, scostamenti

1. **«I 400 passaggi di un lancio sono prove indipendenti»: smentita.** In `gen.h` il flusso casuale del seme s+1 è quello del seme s spostato di un numero (1000 uguali su 1000, `ris/prova_semi.txt`). Su dieci blocchi D da 400 semi «prosegue» a 3 s va da 0,726 a 0,977; la varianza fra blocchi è 2,67 volte la binomiale (1,62 con il denominatore di B; massimo 6,0; Tab 4b). Con i semi riparati torna a 0,94 (Tab 4c). **Gli intervalli di B e M sono stretti di 1,3–2,5 volte; le stime restano dentro gli intervalli per blocchi** (D, «prosegue» a 3 s, denominatore «tutti»: 0,882 [0,826–0,938] sui semi originali, 0,899 sui riparati).
2. **«Tre conti che non coincidono» (M, O1 e O2): è una definizione.** B divide per i nascosti *dentro l'area osservata* (`tabelle.py`, riga 176), M per *tutti* i nascosti (`leggi.py`). Stessa cella, «prosegue» a 3 s in D: 86/92 e 101/105 con la prima, 86/98 e 101/119 con la seconda (Fisher p = 0,52). «In D non superata per un millesimo» cade.
3. **`sd-1` «almeno 9 su 10 sul percorso»: regge fino a 2 s, non risolta a 3 s; smentita a 2–3 s in L con camminatori meno regolari della taratura** (§2, §4).
4. **Il contatore «ricomparso dentro la zona» non è la precisione dichiarata** (§6).

**Scostamenti.** Previsioni in `PREVISIONI.md` (cinque serie con l'ora): non cieche rispetto a B, M e triage, letti prima; dalla terza serie nascono da uscite già viste. Su 18: 12 reggono, 1 regge solo dalle medie di cella, 1 smentita (P-st-3), 4 miste (P-st-2, 11, 17, 18). Oltre al riconteggio ho fatto 30 lanci (il più lungo 68 s) con il codice di M copiato (`codice/`, `IMPRONTE.txt`): **condivido generatore, filtro, predittori, valutatore e modello linguistico**; miei sono statistiche, semi, spostamento e riparazione dei semi. Due file provvisori nella cartella provvisoria della sessione. Conteggi del torneo ricostruiti da quote a tre decimali (± 1). Effetto dei semi in T e L stimato su tre lanci (1,5). Lo spostamento è uno solo, scelto da me. `rifai.sh` non rieseguito per intero. Della preproposta letti i §2 e §5; cartella f9 non letta.

## 1. Le cifre di B e di M tornano?

**38 su 38**, ciascuna con la definizione del suo file (Tab 2): di B celle peggiori (86/92, 370/386, 357/380), minimo a 5 s, punteggi, R50, vuoti del nucleo; di M minimi (101/119, 252/262, 357/388), aree, 0 vuoti, R100, «ampio» 50,4 %. Tornano le cifre di C-EST (Tab 9). Il mio eseguibile ridà le righe di B (35 su 35). **Non tornano come lettura** O1 e O2 di M e gli intervalli (0.1, 0.2).

## 2. Per comportamento e per tempo (ciò che le medie nascondono)

`sd-1`, **semi riparati, taratura rifatta** (`codice_semi/`; 2000 passaggi per comportamento in D, 800 in T e L; Tab 4c, 8). Quota dei nascosti dentro la regione; in D denominatore «tutti» (prudente). Semiampiezza sul percorso ≤ 0,03 fino a 3 s, ≤ 0,055 a 5 s.

| Comportamento | 1 s | 2 s | 3 s | 5 s |
|---|---|---|---|---|
| prosegue | 0,980 / 0,995 / 0,990 | 0,940 / 0,964 / 0,960 | **0,899** / 0,968 / 0,924 | **0,787** / 0,929 / 0,902 |
| rallenta | 0,988 / 0,991 / 0,996 | 0,959 / 0,959 / 0,959 | 0,935 / 0,926 / 0,919 | 0,866 / 0,891 / 0,856 |
| sosta | 0,985 / 0,991 / 0,989 | 0,965 / 0,977 / 0,959 | 0,956 / 0,968 / 0,939 | 0,915 / 0,917 / 0,879 |
| torna | 0,985 / 0,993 / 0,987 | 0,972 / 0,969 / 0,956 | 0,977 / 0,976 / 0,935 | 0,965 / 0,922 / 0,906 |
| sosta lunga | 0,991 / 0,991 / 0,993 | 0,970 / 0,973 / 0,971 | 0,961 / 0,966 / 0,948 | 0,951 / 0,955 / 0,911 |
| **svolta** | 0,864 / 0,871 / 0,941 | **0,567 / 0,541 / 0,698** | 0,451 / 0,383 / 0,517 | 0,352 / 0,197 / 0,285 |
| **lato lontano** | 0,771 / 0,839 / 0,920 | **0,320 / 0,448 / 0,665** | 0,131 / 0,262 / 0,466 | 0,019 / 0,133 / 0,232 |
| area regione / ombra | 0,72 / 0,12 / 0,06 | 0,95 / 0,24 / 0,16 | 1,00 / 0,31 / 0,27 | 1,00 / 0,38 / 0,38 |
| nucleo di oggi, prosegue | 0,03 / 1,00 / 0,99 | 0,01 / 0,00 / 0,06 | 0,02 / 0,00 / 0,00 | 0,01 / 0,00 / 0,00 |

- **La media nasconde chi lascia il percorso.** Sulla miscela «squadra» T e L danno 0,92–0,94 a 2 s e 0,90–0,92 a 3 s (denominatore di B), con svolta e lato lontano a 0,32–0,70: lì vale solo R100 (100 %: 54 400, 23 409, 26 322 campioni).
- **In D, con il denominatore di B,** «prosegue» vale 0,985 / 0,975 / 0,960 / 0,926: la differenza sono i passaggi usciti dalla portata di 3 m senza essere rivisti (33 su 513 a 3 s). E da 2 s la regione è tutta l'ombra («ampio» nel 60 % dei cicli): lì la copertura non dice dove.
- **Il ripiego `sd-0`** tiene 0,85 in ogni cella fino a 3 s (minimo 456/513 = 0,889 [0,859–0,913]), ma a 0,5–1 s vale 0,89–0,95 su sosta e ritorno e da 2 s occupa 0,8–1,6 volte l'ombra: per lui «almeno 85 su 100», non «9 su 10».
- **Al 50 %:** `sd-1` e `sd-0` non dichiarano il livello; quello di C-004 conteneva 0,91–0,93 a 0,5 s e 0,50–0,58 a 3 s. **Punteggio** («squadra», T, 1 / 2 / 3 s; basso è meglio): nucleo 0,81 2,54 2,54; `sd-0` 0,32 2,27 2,45; `sd-1` 0,12 1,07 1,44. Il braccio q = 0,01, che deve fallire, fa −1,38 0,60 1,76 coprendo 0,91 0,77 0,65: **il punteggio premia la regione stretta e da solo non decide**.

## 3. Le soglie fissate prima (triage §6)

| Soglia | Esito (semi riparati) |
|---|---|
| C1a, 0 passaggi con un vuoto | nucleo **smentita** (9715 su 9735; 3981 su 4000; 3997 su 3999); `sd-1`, `sd-0` **regge**: 0 su 13 638 / 5600 / 5597 (quota vera ≤ 0,07 %) |
| C3, R90 ≥ 0,85 per cella sul percorso fino a 3 s | `sd-1` e `sd-0` **regge** in 60 celle su 60, con i due denominatori; nucleo **smentita** da 2 s. A 5 s: D «prosegue» 174/221 = 0,787 [0,729–0,836] **smentita** («tutti»); T e L «rallenta» **non risolta** |
| «Almeno 0,90» (la frase a schermo) | `sd-1` **regge** in 45 celle su 45 fino a 2 s; a 3 s 12 su 15, tre **non risolte** (0,899; 0,926; 0,919) |
| C3, miscele fra 0,85 e 0,97 («squadra», denominatore di B) | **smentita per eccesso** a 0,5–1 s (0,976–0,999); **regge** a 2–3 s (0,90–0,96) |
| C3, R50 fra 0,40 e 0,60 | C-004 **smentita** (0,77–0,93 fino a 1 s); `sd-1`, `sd-0`: un livello solo, come previsto da K-208 |
| C3, area ≤ 0,60 dell'ombra in T e L | `sd-1` **regge** (0,03–0,31); `sd-0` **smentita** da 2 s (0,79–1,21) |
| C4; R100 al 100 % | **regge**: 0 cicli di R90 su visto libero oltre la fascia, 0 fuori da R100 |
| Attacco 5 su C-EST (≥ 0,90) | **smentita** (0,28 / 0,30 / 0,00; 0,71 e 0,00), salvo la lettura B in D (354/355) |

**Scelte dopo i dati.** (a) Orizzonte di 3 s e soglia dell'80 % di «ampio»: scelti da M sui numeri della prova (lo dichiara, §5.7). (b) L'enunciato per geometria di M è nato sui semi 12000; sui miei regge come «≥ 0,94», non «≥ 0,96» (T 0,959, L 0,956 a 2 s). (c) Il denominatore è cambiato fra B e M senza dirlo. (d) M applica a n = 119 la regola per n = 400; con quella del triage per n < 200 la cella è «non risolta» ([0,774–0,902]); quella regola ammette insieme «regge» e «smentita» e tace fra 200 e 399. (e) Il torneo ha letto due volte i semi di prova (To §0). Nessun comportamento escluso dopo; la lisciatura è stata scelta sui semi di taratura con una regola scritta prima (B §0).

## 4. Taratura, indipendenza, spostamento

**Insiemi separati: sì** (taratura 1000–1199, prove da 9000; a circa 3500 numeri per passaggio, per calcolo, i flussi non si toccano). **Generatore non dell'autore: sì. Ma in nessuna prova la libreria di C-004 viene da un generatore e i passaggi da un altro** (B §7, To §0). E la libreria è un campione: rifatta, sposta una cella di quattro centesimi (T, «rallenta» a 3 s: 0,968 → 0,926); quanto pesi è **non verificato**. Minimo sul percorso, denominatore di B (Tab 4c, 5):

| Prova | fino a 1 s | fino a 2 s | fino a 3 s |
|---|---|---|---|
| Semi riparati, stesso generatore | 0,985 / 0,991 / 0,987 | 0,967 / 0,959 / 0,956 | 0,958 / 0,926 / 0,919 |
| **Mio spostamento:** velocità 15 % (non 6), rotta 8° (non 3), ± 30° (non 15); taratura ferma | 0,965 / 0,962 / 0,944 | 0,960 / 0,906 / **0,835** [0,79–0,87] | 0,936 / 0,871 / **0,801** [0,75–0,84] |
| Torneo, base (altro codice e generatore) | — | — | 0,898 [0,80–0,95] / 0,934 / 0,937 |
| Torneo, 0,8 m/s con soste (T) | — | — | 115/128 = 0,898: non risolta |
| Rumore 4 / 9 / 16 cm con R ferma; rifatta (B, T) | — | — | 61/140 = 0,44; 337/386 = 0,87 |
| Ombra stimata a −20 cm (To, T; B con fascia: 0,97) | — | — | 0,53–0,74: smentita |
| Corpo largo senza C6; con C6 (To, T) | — | — | 0,65; 0,965 |

**Regge in ogni prova «9 su 10 fino a 1 s».** A 2 s dipende da quanto i camminatori veri somigliano alla libreria, dal rumore rimisurato e dalla maschera dell'ombra.

## 5. La riga per la giuria

> «In simulazione, chi resta sul proprio percorso (prosegue, rallenta, si ferma, torna) sta dentro la zona tratteggiata in almeno 9 casi su 10 fino a 2 secondi senza essere visto, e in almeno 85 su 100 fino a 3; chi svolta o si allontana è coperto solo dall'avviso sull'ombra. Sul sensore la cifra è quella del tabellone: dentro k su n.»

Limite inferiore peggiore fino a 2 s: 0,922. Non vale con rumore o maschera non tarati sull'installazione; con camminatori meno regolari in ombre larghe scende a 8 su 10.

## 6. Sull'hardware

- **± 0,10 chiede 38 occlusioni** se ne escono dentro 9 su 10 (51 a 0,85; 93 nel caso peggiore; Tab 7). L'ampiezza dipende dall'esito: con **50 per riga** si chiude entro ± 0,10 nell'88 % dei casi se il vero è 0,90 (60 se è 0,85). Una riga è un comportamento; con l'occlusione virtuale la stessa camminata dà 1 s e 2 s.
- **Nelle 14 ore:** 2 righe × 50 («prosegue»; «si ferma o torna») = 100 camminate, 35–40 minuti in due (stima mia, **non verificata**). **Nelle 4 ore:** le altre righe e un camminatore fuori dalla taratura. Passaggi della stessa persona si somigliano: con correlazione 0,2 e dieci a testa, 40 ne valgono 14. La cifra descrive «queste persone, questa stanza». Il sensore arriva non prima di 5–6 ore (settimo addendum): fino ad allora il tabellone gira sul sensore simulato, e lo scrive. Tabellone, scheda e camminate valgono circa 2 ore-persona (stima, **non verificata**): stanno nel piano con 3, 4 o 5 persone.
- **Il tabellone, perché non inganni.** (1) «Dentro k su n» con l'intervallo, mai una percentuale sola; sotto n = 10 solo i conteggi. (2) L'evento è **la persona dentro la regione a 1 s e a 2 s**, con l'occlusione virtuale. La «prima misura entro 0,40 m» è un'altra grandezza: con l'ombra stimata a −20 cm senza fascia segna 1216/1244 = 0,977 mentre la cella peggiore vale 0,68 (B, braccio T); con `sd-0` segna 0,89–0,95 dove la copertura è 0,93–0,99; vede però un filtro troppo sicuro (0,56–0,65; Tab 10). Resta come controllo, in una riga sua. (3) I cicli «ampio» a parte. (4) Il comportamento si dichiara **prima** della camminata. (5) n fissato prima, nessun azzeramento, taratura esclusa, scarti contati; accanto, la larghezza della regione. (6) «Almeno 0,80» solo con 46 su 50; 30 su 30 dice «almeno 0,89», non «sempre».

## 7. Stati proposti

| Enunciato | Stato |
|---|---|
| Il nucleo di oggi rispetta i controlli 1 e 3 | **smentito** (regione nel 19 / 38 / 33 % dei cicli; copertura 0,00–0,12 da 2 s) |
| `sd-1`: ≥ 0,85 per cella sul percorso fino a 3 s; ≥ 0,90 fino a 2 s | **sostenuto dai dati**: simulazione, tre geometrie, passaggi indipendenti |
| Lo stesso con camminatori diversi dalla libreria | **smentito** a 2–3 s in L; **sostenuto** fino a 1 s |
| `sd-1` a 3 s al livello 0,90, e a 5 s | **non risolto** (cella peggiore a 5 s: 0,79–0,89) |
| C-EST (S3, S4) com'è scritta; ampiezza degli intervalli di B e M | **smentite** (§3; 0.1) |
| Copertura su persone e sensore veri | **non risolto**: 50 occlusioni per riga |

## 8. Proposte, con la fascia

- **`statistico-3`, una definizione e una regola.** Denominatore «nascosti dentro l'area osservata» (l'unico misurabile con l'occlusione virtuale), a parte chi esce dall'area; esito con il limite di Wilson. *Previsione:* O1 e O2 spariscono. *La smentisce* una cella che cambia esito a pari definizione. **Indispensabile nelle 14 ore** (un quarto d'ora).
- **`statistico-4`, il tabellone del §6.** *Previsione:* sul sensore, in almeno un braccio (maschera o rumore non tarati) contatore e copertura a 2 s distano più di 0,10. *La smentisce* uno scarto sotto 0,05 in ogni braccio con 50 camminate. **14 ore** (mezz'ora dentro M5 e M6: è la «valutazione realistica della precisione»).
- **`statistico-5`, la frase a schermo per tempo:** «almeno 9 su 10» fino a 2 s, «almeno 8 su 10» fino a 3 s, poi «ampio». *Previsione:* sul sensore nessuna riga smentisce il valore scritto. *La smentisce* una riga con il limite superiore sotto il valore scritto. **14 ore** (una stringa).
- **`statistico-6`, libreria da almeno due persone a tre andature.** *Previsione:* lo spostamento del §4 in L risale sopra 0,88 a 2 s. *La smentisce* un valore sotto 0,85. **Non eseguita.** Registrazione nelle **14 ore** (sono le stesse 30 camminate), prova nelle **4 ore**.
- **`statistico-7`, riparare `rng_seed`** (una riga, `codice_semi/gen.h`) prima di ogni nuovo lancio del banco. **Dopo l'hackathon**, salvo nuovi lanci.

**Dopo.** All'arbitro: fissare il denominatore e riscrivere O1 e O2. Con il sensore: rumore, poi le due righe da 50. **Rifare:** `sh rifai.sh` (30 lanci ≤ 68 s l'uno, poi `riconta.py griglia` e `tutti`).
