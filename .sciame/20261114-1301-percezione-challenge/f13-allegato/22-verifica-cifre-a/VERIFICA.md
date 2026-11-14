# Verifica avversaria delle cifre, capitoli 1–5 dell'allegato tecnico (f13, `sciame-validazione`)

**Esito in tre righe.**
- Voci controllate: circa 690 valori numerici dei capitoli 1–5 e delle loro tabelle (58 intervalli di Wilson ricalcolati; circa 300 valori di conti in forma chiusa rifatti; circa 330 cifre di simulazione o di dati pubblici cercate nei file d'origine). Il totale è una stima a ±10 %: una terna conta tre voci.
- Tornano: tutte salvo 12. Nessuna cifra centrale (coperture, continuità, identità, fascia, dominio per classe) è sbagliata. Nessuna cifra è «non trovata».
- Non tornano o vanno corrette: 12 voci. 4 sono false o non sostenute dal file d'origine, 5 sono giuste ma con la condizione mancante o sbagliata, 3 sono di forma. Le discordanze note dei fascicoli sono tutte recepite con il valore corretto.

Lavoro dalle 19:26:20 alle 19:38 circa del 14 novembre 2026 (`date -Is`), sui file `.tex` di `20-unione/capitoli/` (il PDF non è stato confrontato con i `.tex`).

## 0. In testa: previsioni, regole, indipendenza

- **Previsioni** (scritte in `stato.md` alle 19:26:20, prima di leggere i capitoli).
  - validazione-P1, «almeno una cifra non coincide col file d'origine»: **regge** (correzioni 1, 2, 4).
  - validazione-P2, «almeno un intervallo di Wilson dichiarato differisce dal ricalcolo oltre l'arrotondamento»: **regge** per una voce sola (correzione 3: il limite «1,5 su 10 000» non è di Wilson). Gli altri 57 coincidono all'ultima cifra scritta, due con arrotondamento per eccesso (correzione 11).
  - validazione-P3, «almeno una cifra corretta dalle discordanze compare col valore vecchio»: **smentita**. Nei capitoli 1–5 non ne ho trovata nessuna (elenco al §3).
- **Regola violata per errore:** la consegna dice «niente git»; alle 19:38, in coda all'ultimo comando di controllo, ho eseguito una volta `git --version` (stampa la versione; non legge né scrive il deposito). Nessun altro comando git.
- **Regola dell'ambiente non seguita, per scelta:** l'ambiente chiede di non scrivere file di rapporto `.md`; la consegna chiede questo file. Ho seguito la consegna.
- **Scostamenti.** Ho aperto in sola lettura tre file grezzi fuori dall'elenco della consegna, perché citati nelle parti II dei fascicoli: `f10-dati/20-validazione/uscite/banco_thor.json` e `banco_thor.txt`, `f10-dati/21-statistica/tabelle/thor.txt`, `f10-dati/20-validazione/uscite/misure_brevi.txt` (trovato con una ricerca testuale). Niente git, sudo, rete; scritture solo in questa cartella.
- **Indipendenza.** `wilson.py` e `conti.py` sono miei e non importano niente dal progetto: valgono contro errori di conto e di trascrizione. Condividono con gli autori le formule e i parametri scritti nell'allegato. `cerca.py` confronta l'allegato con i fascicoli, con i file di f12 e f14 e con i verdetti: prova che la cifra è trascritta bene, non che il simulatore che l'ha prodotta è giusto. I file grezzi di f4, f7 e f8 non li ho aperti: per quelli mi fermo ai riconteggi dei fascicoli.

## 1. Correzioni, in ordine di gravità

### A. Falso o non sostenuto dal file d'origine

**1. Capitolo 3, §«Misure su profondità simulata dalle schede tecniche» (`sec:map-schede`), prima frase: «in 135 sequenze con tre forme d'ombra».**
- *Che cosa non torna.* «Tre forme d'ombra» non è sostenuto dal grezzo. Il riconteggio trova quattro valori distinti di celle d'ombra e chi l'ha fatto scrive di non aver approfondito.
- *Prova.* `04-statistica/ricontato.txt` r. 158–159: «valori distinti di celle d'ombra [8, 12, 342, 454]»; `04-statistica/FASCICOLO_VALUTAZIONE.md` r. 304: «Il verdetto dice "3 forme d'ombra"; nei record i valori distinti […] sono 4 […]: non ho approfondito».
- *Testo corretto.*
  > sono 0 su 2\,907\,032 celle·fotogramma, in 135 sequenze (131 con i filtri della camera spenti e 4 con i filtri accesi); per sequenza, 0 su 131 con i filtri spenti (limite superiore di Wilson $2{,}9\,\%$) \prova{S}.

**2. Capitolo 1, Tabella `tab:intro-sintesi`, riga «"Libero" nell'ombra vera»: condizione «131 sequenze».**
- *Che cosa non torna.* Le 2 907 032 celle·fotogramma vengono da 135 sequenze, non da 131. Le 131 sono il denominatore del solo intervallo per sequenza. Il capitolo 3 scrive 135: i due capitoli si contraddicono.
- *Prova.* `04-statistica/ricontato.txt` r. 158–160: «0 su 2 907 032 celle·fotogramma; 135 sequenze (131 + 4 con filtri)», «per sequenza: 0 su 131 -> limite superiore Wilson 0.0285».
- *Testo corretto* (colonne «Condizioni» e «Valore»).
  > da scheda, regola di lettura precedente a quella adottata; 135 sequenze, 131 delle quali con i filtri della camera spenti
  >
  > 0 su $2\,907\,032$ celle\,$\cdot$\,fotogramma; per sequenza, sulle 131 con i filtri spenti, $[0;\,2{,}9\,\%]$. In una serie successiva […]

**3. Capitolo 5, §`sec:occ-classe`, «Livello di prova e limiti»: «0 sequenze su 20 000 […] (limite superiore al 95 %: 1,5 su 10 000)».**
- *Che cosa non torna.* L'allegato dichiara che gli intervalli sono di Wilson al 95 %. Questo non lo è: è il limite a una coda (regola del tre, 3/N). Con Wilson a due code il limite è 1,9 su 10 000. Il testo non dice che la convenzione è diversa.
- *Prova.* `wilson.txt`, ultima riga della tabella: 0 su 20 000, Wilson [0; 0,00019]; 3/20 000 = 0,00015; z²/(N+z²) = 3,8415/20 003,84 = 1,92·10⁻⁴. La cifra 1,5 viene da `f14-classificazione/20-inclusione/BLOCCO_CLASSIFICAZIONE.md` r. 173, che non nomina la convenzione.
- *Testo corretto* (due forme: la prima non introduce cifre nuove).
  > 0 sequenze su 20\,000 con la fascia più stretta che senza etichette (limite superiore al 95\,\% a una coda: 1,5 su 10\,000), e 0 su 20\,000 con un secondo programma \prova{S}

  oppure, con la convenzione del resto dell'allegato:
  > […] (limite superiore di Wilson al 95\,\%: 1,9 su 10\,000) […]

**4. Capitolo 3, §`sec:map-banco`, «Il prezzo in resa»: «lo stato di una cella cambia fino a 6–7 volte al secondo, sempre verso il lato prudente».**
- *Che cosa non torna.* Per la regola adottata il file dà 5,72 cambi al secondo con il 30 % sparso, 2,72 con il 5 % a chiazze e 6,66 con il 30 % a chiazze. Il valore 7,03 è della variante scartata, e con il 5 % sparso. «Sempre verso il lato prudente» non c'è nel file per questa misura: un cambio di stato va nei due versi.
- *Prova.* `f12-integrazione/03-libero/LIBERO_DELLA_CELLA.md` r. 44: «Sfarfallio (cambi per cella al secondo, stanza vuota, k 0,004): 5 % sparso V-017 7,03, `nuvole-1` 0,01; 30 % sparso 5,72; chiazze 5 % 2,72; chiazze 30 % 6,66».
- *Testo corretto.*
  > In una stanza vuota, con $k=0{,}004$, lo stato di una cella cambia $5{,}7$ volte al secondo con il $30\,\%$ di pixel non validi sparsi, $2{,}7$ con il $5\,\%$ a chiazze e $6{,}7$ con il $30\,\%$ a chiazze, contro $0{,}01$ con il $5\,\%$ sparso \prova{S}.

### B. Giusto, ma con la condizione mancante o sbagliata

**5. Capitolo 4, §`sec:sti-riaggancio`, «Risultati in simulazione»: «400 su 400 in ciascuna di 27 configurazioni (limite inferiore di Wilson 99,05 %)».**
- *Che cosa non torna.* Manca la condizione $P_D=1$. Con $P_D=0{,}9$ la quota va dal 99,7 al 100 %. Il conteggio è dedotto da una quota stampata a un decimale.
- *Prova.* `04-statistica/FASCICOLO_VALUTAZIONE.md` r. 205 («$P_D = 1$; 27 configurazioni») e r. 314 («"400 su 400" è dedotto da 100,0 % × 400»); `03-stima/FASCICOLO_STIMA.md` r. 193 («con $p_d = 0{,}9$, da 99,7 a 100 %»).
- *Testo corretto.*
  > Ricomparse legittime riagganciate, con $P_D=1$: 400 su 400 in ciascuna di 27 configurazioni (limite inferiore di Wilson $99{,}05\,\%$); con $P_D=0{,}9$, dal $99{,}7$ al 100\,\%.

**6. Capitolo 4, §`sec:sti-q`, ultima frase: «a 3 s la regione ha un raggio di 3,5 m».**
- *Che cosa non torna.* La copertura della Tabella `tab:sti-thor` è quella della regione al 90 %; 3,49 m è il raggio del cerchio al 95 % (la colonna della tabella lo dice: $r_{0,95}$).
- *Prova.* `f10-dati/20-validazione/uscite/banco_thor.txt`: «copertura 90 % = …; cerchio 95 % = …, raggio mediano …»; `banco_thor.json`, campo `raggio95_mediano` = 3,49 a 3 s; `03-stima/uscite/ricalcoli.txt` r. 80–81: «raggio al 95 % con rincorsa di 1 s […] q = 0.20: 0.31 / 0.75 / 1.96 / 3.49».
- *Testo corretto.*
  > Il sistema mantiene $q=0{,}2$ come scelta prudente, non come taratura: a $3\unita{s}$ il cerchio al 95\,\% ha un raggio di $3{,}5\unita{m}$ e informa poco.

**7. Capitolo 4, §`sec:sti-mobile`, «Regola dei gruppi a celle forti»: «rumore nominale […] scatola di 15 cm a 2 m vista in 190 fotogrammi su 190».**
- *Che cosa non torna.* La riga è introdotta da «rumore nominale», ma 3 delle 19 sequenze della scatola sono al livello degradato.
- *Prova.* `f12-integrazione/06-identita/IDENTITA_SU_PROFONDITA.md` r. 54: «Scatola 15 cm a 2 m vista (190 fot., 19 sequenze, 3 al limite) | … | 190 · 190».
- *Testo corretto.*
  > scatola di 15\,cm a $2\unita{m}$ vista in 190 fotogrammi su 190 (19 sequenze, 3 delle quali al livello degradato del modello di rumore).

**8. Capitolo 5, Tabella `tab:occ-dominio`, riga «Camminatori meno regolari della libreria ($G_3$)».**
- *Che cosa non torna.* La riga usa un denominatore diverso dalle altre («nascosti dentro l'area osservata») e il soggetto è puntiforme; la tabella non lo dice. Mancano i conteggi.
- *Prova.* `04-statistica/FASCICOLO_VALUTAZIONE.md` r. 296: «torna (A7): 323/342, 283/339, 226/282 (denominatore "dentro l'area osservata")»; r. 108 per gli intervalli; r. 131 per il soggetto puntiforme.
- *Testo corretto* (seconda colonna).
  > 323 su 342 / 283 su 339 / 226 su 282 = 0,944 / 0,835 / 0,801 (Wilson a 2 e $3\unita{s}$: 0,792--0,871 e 0,751--0,844); soggetto puntiforme, contati i soli istanti con il soggetto nascosto dentro l'area osservata

**9. Capitolo 4, Tabella `tab:sti-thor`, riga $q=0{,}1$ («0,945 (207; 0,907–0,968) | 0,945 | 0,945»), e la frase «I 207 con $q=0{,}1$».**
- *Che cosa non torna.* La cifra è giusta, ma nel file d'origine è una valutazione fatta a posteriori sulla registrazione di prova, e l'autore scrive che «non conta» come prova. La tabella la mette alla pari delle altre due righe.
- *Prova.* `f10-dati/20-validazione/uscite/misure_brevi.txt` r. 11: «THÖR exp3, q = 0,1 (a posteriori): copertura 90 % a 1/2/3 s [0.945, 0.945, 0.945]»; `f10-dati/20-validazione/VALIDAZIONE_DATI.md` r. 107 e r. 187 («0,945 su exp3 è visto a posteriori: non conta»).
- *Testo corretto* (prima cella della riga, e didascalia).
  > 0,1 (a posteriori)

  e in didascalia, dopo «tratti come indipendenti»:
  > La riga $q=0{,}1$ è stata calcolata dopo aver visto i risultati della registrazione di prova.

### C. Forma

**10. Capitolo 2, §`sec:geo-posa`: «Con $\delta\theta=1^\circ$ l'errore è […] 5,2 cm a 3 m».**
- *Che cosa non torna.* Con la formula esatta \eqref{eq:geo-posa} il valore è 5,25 cm, cioè 5,3; 5,2 è l'approssimazione lineare (5,24). Nella frase seguente «1,99 m» è invece il valore esatto (lineare: 2,01). Le due cifre usano formule diverse.
- *Prova.* `02-geometria/ricalcoli.txt` r. 131 («rho = 3.0 m, 1.0 gradi: 5.25 cm (lineare 5.24 cm)») e r. 134 («da rho = 1.985 m»); `conti.txt`, riga «posa 1°»: 3,5 / 4,9 / 5,3.
- *Testo corretto.*
  > Con $\delta\theta=1^\circ$ l'errore è 3,5 cm a 2 m, 4,9 cm a 2,8 m e 5,3 cm a 3 m (5,2 cm con la sola approssimazione lineare).

  Il «$3+5{,}2=8{,}2\unita{cm}$» del capitolo 3 resta com'è: lì il margine è definito lineare.

**11. Capitolo 1, §`sec:intro-sintesi`, e capitolo 3: limiti superiori «2,9 %» (0 su 131) e «0,016 %» (0 su 24 835).**
- *Che cosa non torna.* Wilson dà 2,85 % e 0,0155 %: arrotondati alla cifra scritta sarebbero 2,8 % e 0,015 %. I fascicoli arrotondano per eccesso, e va detto.
- *Prova.* `wilson.txt`: [0; 0,02849] e [0; 0,00015]; `04-statistica/FASCICOLO_VALUTAZIONE.md` r. 47: «$N = 131$: […] 2,85 %; $N = 24\,835$: […] 0,0155 %».
- *Testo corretto* (in coda alla frase «Gli intervalli fra parentesi quadre sono di Wilson al 95 %»).
  > Gli estremi superiori sono arrotondati per eccesso: $2{,}85\,\%$ è scritto $2{,}9\,\%$ e $0{,}0155\,\%$ è scritto $0{,}016\,\%$.

**12. Capitolo 4, Tabella `tab:sti-mobile`, riga «da 3 m, curva pessimista»: «85,9 % (84,3–87,3)».**
- *Che cosa non torna.* L'intervallo torna solo con 1717 su 2000 (85,85 %); con 85,9 % letto come 1718 su 2000 verrebbe 84,3–87,4. Il file stampa la percentuale, non il conteggio.
- *Prova.* `04-statistica/FASCICOLO_VALUTAZIONE.md` r. 316 («85,85 %; 26,60 % […] letti (percentuali stampate; conteggi dedotti)»); mio conto: 1717/2000, Wilson [0,8425; 0,8731].
- *Testo corretto.*
  > 85,85\,\% (84,3--87,3)

## 2. Avvertenze senza correzione del testo

- **Cifre lette solo da un documento, mai ricontate dal grezzo** (lo dicono i fascicoli; l'allegato le dà senza avvertenza): «87 su 2 800» e «9 su 2 800» del capitolo 5 (`01-dimostrazioni/FASCICOLO_DIMOSTRAZIONI.md` r. 194 e r. 231: «grezzo non trovato»); «193 su 193» dei capitoli 4 e 5 (stessa r. 231); l'errore mediano del punto della Tabella `tab:occ-prima-dopo` (`04-statistica/FASCICOLO_VALUTAZIONE.md` r. 311: «letto dalle righe riassuntive»); «7,8 % contro 24–34 %» del capitolo 1 (r. 318: «letto dal verdetto, non ricontato»); i conteggi della regola «mobile» d'origine (r. 316).
- **Capitolo 3, «43–47 % dei settori»**: nel file la quota sta accanto al solo caso «30 % a chiazze» (`LIBERO_DELLA_CELLA.md` r. 43); l'allegato la attribuisce al «30 % di pixel non validi» in generale. I due file d'origine sono ambigui allo stesso modo: non decido.
- **Capitolo 4, «1,95 s»** (raggio al 95 % oltre 2 m): il mio conto dà 1,945 s, quindi 1,94 o 1,95 secondo l'arrotondamento. Torna.

## 3. Discordanze note dei fascicoli: l'allegato usa il valore corretto?

Sì in tutti i casi che toccano i capitoli 1–5.

| Discordanza | Che cosa scrive l'allegato | Esito |
|---|---|---|
| Dimostrazioni D1, Stima D2 (99,25 % e 99,85 % unilaterali) | 99,05 % e 99,81 %, Wilson | corretto |
| Dimostrazioni D2 (0,33 m «meno della fascia») | 0,33 m come sola età del dato; conto completo nella tabella della fascia | corretto |
| Dimostrazioni D3 (la previsione «non tocca» l'avviso) | forma monotòna, Proposizione `prop:occ-annidamento` (c) | corretto |
| Dimostrazioni D4 (fascia) | 1,85 con τ = 0,150 dichiarato parziale; 1,4 a margine nullo; 1,13 e 0,56 come valore da ritenere | corretto |
| Dimostrazioni D5 (Fisher) | «determinante esattamente 0» | corretto |
| Dimostrazioni D7 (0,375) | 0,375 | corretto |
| Dimostrazioni D9 (peso, non garanzia) | «verificata in simulazione (0 cicli)» | corretto |
| Geometria 1, 2 (focale e campo; 1,24 e 1,22 m) | Osservazione `oss:geo-focale`; 1,243 e 1,221 m; 1,71 m a 43,5° e 1,70 m a 44° | corretto |
| Geometria 3 (testa a 1,70 m) | 2,01 m per 1,70 m; 2,41 m per 1,80 m | corretto |
| Geometria 4 (20,0 % e 20,5 %) | entrambe, con la condizione | corretto |
| Geometria 7 (lato della zona) | 26 e 20 cm | corretto |
| Geometria 10 (campo della Gemini 335) | 90° × 60° e 90° × 65°, con le fonti | corretto |
| Stima D1, Geometria 9 (soglia «mobile») | $k_s\,\sigma\sqrt{2/m}$ | corretto |
| Stima D4 ($\sigma_p$ = 3 cm) | «valore assunto» | corretto |
| Stima D5 (0,00–0,06) | riferito alla regione emessa, per chi prosegue | corretto |
| Stima D6, Valutazione 8 (THÖR, due codici) | entrambe le serie | corretto |
| Valutazione 1 (denominatore) | 826/879 con «corpo puntiforme»; vedi però la correzione 8 | corretto, salvo la riga della correzione 8 |
| Valutazione 3 (83 su 90) | attribuito alla soglia adattata; 36 su 46 ai parametri di partenza | corretto |
| Valutazione 5 (errore del punto fermo) | intervalli fra i lanci: 0,97–1,00 / 1,48–1,54 / 1,59–1,66 | corretto (ricontato su `ricontato.txt` r. 96–113) |
| Valutazione 7 («2 su 1200») | non usata | corretto |
| Costo 2, 7 (rese delle due letture) | distinte: 61,1 % e 87,7 %; 97,1 % e 88,4–91,8 % | corretto |
| Costo 5 (vetro) | 654 su 800 a 2,0 m; 600 su 800 a 1,5 m | corretto |

## 4. Che cosa ho controllato, per capitolo

- **Intervalli di Wilson** (`wilson.py`, `wilson.txt`): 58 voci. 54 coincidono all'ultima cifra scritta; 2 sono arrotondate per eccesso (correzione 11); 1 torna solo con il conteggio 1717 (correzione 12); 1 non è di Wilson (correzione 3).
- **Conti in forma chiusa** (`conti.py`, `conti.txt`), tutti tornano salvo la correzione 10.
  - Capitolo 2: $z_{\min}$ e limiti verticali per profilo; tabelle di $y_{\max}$, di $a_{\min}$, della durata, della banda, del rumore e della quantizzazione; focali; frazione del disco (5,66 m² e 5,79 m², integrazione mia a passo 0,5 mm); ombre; misura di terzi; incidenze; risoluzione laterale; soglie di posa; sensori a tempo di volo e LiDAR.
  - Capitolo 3: 2 610 celle; margini di posa; incrementi della griglia bayesiana; soglie d'inclinazione.
  - Capitolo 4: $\sigma_z$, $\sigma_t$; soglia, $P_{fa}$, limite d'unione, $v_{0,5}$ e $v_{0,9}$; conferma; raggi; tabella di $\sigma_p(\tocc)$ dalla covarianza stazionaria (ricorsione mia); $\sigma_a$; minimi quadrati; binomiale con $N=219$.
  - Capitolo 5: tabella della fascia; ritaglio; $1-e^{-1/2}$; criterio a due stadi (0,999 e 0,026); $d_{\mathrm{serve}}$ e fasce delle 15 classi; i conteggi «3 su 15», «0 su 15», «3 e 10 dopo il contatto», «11 su 15».
- **Cifre di simulazione e di dati pubblici** (`cerca.py`): cercate nei fascicoli e nei loro file di ricalcolo, in `SOLUZIONE_V3.md`, `PROVA_INSIEME.md`, `LIBERO_DELLA_CELLA.md`, `IDENTITA_SU_PROFONDITA.md`, `CONTROPROVA_IDENTITA.md`, `CONTROLLO_PROVE.md`, `ATTACCO_V3.md`, `VERDETTO_INTEGRAZIONE.md` con i suoi riconteggi, nei file di f14 e nei verdetti. Tabelle rilette riga per riga: `tab:intro-sintesi` e seguito, `tab:map-regole`, `tab:map-resa`, `tab:map-varianti`, `tab:sti-mobile`, `tab:sti-profili` (15 classi, comprese le 9 marche di fonte sulle velocità), `tab:sti-thor` (anche sul grezzo), `tab:occ-prima-dopo`, `tab:occ-dominio`, `tab:occ-classi`.

## 5. Che cosa non ho controllato

- I capitoli 6–9, le appendici, il sommario, l'elenco dei simboli; le citazioni e la bibliografia; il PDF contro i `.tex`; le coordinate dei disegni TikZ.
- I file grezzi di f4, f7 e f8 (TSV e testi dei simulatori): mi fermo ai riconteggi dei fascicoli, che condividono con gli autori simulatori e specifica. Nessun simulatore è stato rieseguito.
- Le soglie di riferimento della Tabella `tab:intro-requisiti`: ho ritrovato in `SOLUZIONE_V3.md` (r. 294–300) quelle su elementi mobili, ostacoli, feedback, affidabilità e latenza; non ho cercato le altre (identità 0,95, sicurezza, classificazione).
- Capitolo 4: «scarto tipo di velocità di 2,5 m/s» alla ripartenza dalla misura e la fascia «0,75 m nelle prove d'insieme»; i parametri del predittore del capitolo 5 li ho ritrovati in `SOLUZIONE_V3.md` r. 144–160, ma senza controllarne il codice.
- La correttezza delle dimostrazioni: non è la mia parte.
