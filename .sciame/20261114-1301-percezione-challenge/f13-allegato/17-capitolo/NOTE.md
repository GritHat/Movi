# NOTE al capitolo 7 (`capitolo.tex`) — per chi unisce

## 0. In testa: scostamenti e regole

- **Scrittura fuori dalla cartella di consegna:** per guardare le pagine ho generato delle immagini PNG (`c7-0N.png`, `c7b-0N.png`) nella cartella temporanea della sessione, che risulta condivisa con altri lavori. Nessun altro file scritto fuori da `17-capitolo/`. Niente git, niente sudo, niente rete.
- **Regola dell'ambiente non seguita, per scelta:** l'ambiente chiede di non scrivere file `.md` di rapporto; la consegna chiede `CIFRE.md` e `NOTE.md`: ho seguito la consegna.
- **Nessuna previsione scritta prima** della compilazione (lavoro di composizione; attesa implicita: compila, entro sette pagine).
- **Niente ricalcoli:** le cifre sono trascritte dai fascicoli e dai giudizi, non rifatte dai file grezzi. Ho rifatto a mano solo due conti di controllo (16,5 m/s² = √6·0,03·225; 26 cm = 2·2·tan 3,75°).
- **Lettura parziale:** non ho letto `SOLUZIONE_V3.md` per intero (solo la tabella degli esclusi, §4), né `SCHERMO_E_DEMO.md`, `PROVA_INSIEME.md`, `LIBERO_DELLA_CELLA.md`, i file sull'identità, `CONTROLLO_PROVE.md`, `ATTACCO_V3.md`, i giudizi f4 e f10 (solo una ricerca testuale), i fascicoli 01–04 (solo i passi usati), `PROFILI.md`, `USO_DELLA_CLASSE.md`, `ATTACCO_CLASSIFICAZIONE.md`. Il giudizio complessivo dell'integrazione **non esiste** (cartella `30-arbitro` vuota): le «frasi da non scrivere» le ho prese dai giudizi precedenti.

## 1. Compilazione

- `prova.tex` = preambolo comune (copia identica in questa cartella) + `capitolo.tex` + `allegato.bib` con stile `unsrtnat`. XeLaTeX, BibTeX, XeLaTeX due volte: **0 errori, 0 citazioni indefinite**. Restano indefiniti solo i riferimenti agli altri capitoli (`sec:geo`, `sec:map`, `sec:sti`, `sec:occ`, `sec:val`, `sec:lim`), come previsto.
- **Lunghezza:** il corpo del capitolo finisce nella parte bassa della sesta pagina composta (la bibliografia comincia lì): meno delle sette concesse.
- BibTeX dà 4 avvisi «empty year» (`octomap`, `realsense-taratura-profondita`, `slamtec-rplidar-c1`, `us-49cfr-236-205`) e c'è una riga troppo larga di 72 pt **nella bibliografia** (un indirizzo lungo, righe 576–587 del `.bbl`): sono della bibliografia comune, non del capitolo.
- Nessun pacchetto in più. Le tabelle usano `[H]` (pacchetto `float`, già nel preambolo).
- Il controllo delle parole vietate trova solo `c1` dentro la chiave `slamtec-rplidar-c1` (già segnalato nelle discordanze della bibliografia).

## 2. Scelte che chi unisce deve conoscere

1. **Livello di prova delle misure di tempo.** Il preambolo non ha una sigla per «misura di tempo al calcolatore»: ho usato [S] (profondità sintetica) e [P] (registrazione pubblica), dicendo nel testo che sono tempi di un portatile. Se si preferisce una sigla a parte, va aggiunta alla legenda del capitolo 1.
2. **«Oggetti seguiti» al posto di «tracce».** Ho scritto «oggetti seguiti» (simbolo n_T) per non confondere con «traccia» nel senso del testo della sfida. Se il capitolo 4 usa «tracce», uniformare.
3. **Nomi delle rappresentazioni e delle letture.** «Lettura a due stati», «decadimento verso il libero», «lettura del fotogramma corrente», «occupazione bayesiana letta come stato corrente»: sono i nomi del fascicolo sul costo; il capitolo 3 dovrebbe usare gli stessi.
4. **La tabella dei controesempi di sicurezza** (sette varianti che ricordano o deducono un «libero»), la definizione della lettura di un punto, la proposizione sul «libero» del fotogramma corrente e la tabella della resa **non sono in questo capitolo**: le ho lasciate al capitolo 3, e qui ne riporto solo tre righe nella tabella delle alternative. Se il capitolo 3 non le contiene, vanno recuperate dal fascicolo sul costo (§4).
5. **La catena con rete neurale** è data come «scelta di progetto: nessuna misura la esclude» con livello [N], perché così dicono i giudizi («nessun controesempio nei file»). Non ho scritto un controesempio che non c'è.
6. **«N non riportata».** Per il selettore (13,8 %, 57,0 %, 200 cambi, 17,5–28 al minuto), per la probabilità d'intrusione (0,16–0,18), per i sensori laterali e per «38–100 %» i giudizi non riportano numerosità né intervalli: nella tabella è scritto. Non ho calcolato intervalli di Wilson nuovi sui conteggi delle alternative (374 su 2 000 e simili), per non introdurre cifre che non stanno nei file: se servono, li calcoli chi cura il capitolo 6.
7. **Il nome delle due geometrie con ombra larga** nelle prove sulla previsione a due ipotesi: dai file so solo che la prima ha il pannello da 1 m e la terza il pannello da 2 m; la seconda l'ho lasciata senza descrizione.
8. **«Le due letture della regola»** della previsione a due ipotesi: una è con i pesi cumulati; l'altra non è descritta nei file che ho letto, e non l'ho descritta.

## 3. Dipendenze da altri capitoli

- **Cap. 2 (`sec:geo`):** campo e portata dei sensori a tempo di volo, zona cieca vicina, il canale laterale di sola prossimità; le tre ragioni per cui quel canale non dichiara «libero».
- **Cap. 3 (`sec:map`):** mappa a quattro stati, lettura di un punto, controesempi delle mappe persistenti, resa del libero.
- **Cap. 4 (`sec:sti`):** proposizione sulla massa, lemma sulla differenza seconda, catena di riferimento, tassonomia e requisiti del classificatore (i «circa 25 tipi»).
- **Cap. 5 (`sec:occ`):** regione di previsione, fascia di guardia, l'enunciato «un'etichetta non riduce mai l'avviso», e l'osservazione sulla probabilità d'intrusione (nel fascicolo delle dimostrazioni sta fra gli enunciati sull'occlusione: se finisce altrove, cambiare il rimando nella tabella delle alternative).
- **Cap. 6 (`sec:val`):** il livello dichiarato della regione; intervalli di Wilson e di Clopper e Pearson (qui non li ricito).
- **Cap. 8 (`sec:lim`):** latenza da un estremo all'altro (qui dico solo «non misurata», senza la somma di 154,8 ms, che ha una discordanza: 95 ms contro 71 ms per il sensore), configurazione all'avvio, sensore in moto, canale d'uscita.

## 4. Lasciato fuori, e perché

- La colonna «lettura di 18 settori» della tabella dei tempi (larghezza della tabella); i tempi in C della previsione sotto carico (0,67 e 5,9 ms: sono un rilancio di controllo).
- Del fascicolo sul costo §4: tutto ciò che è sicurezza del «libero» (vedi 2.4); il vetro (654 su 800 a 2 m, 600 a 1,5 m) e l'errore di 1°: capitoli 3 e 8.
- Del fascicolo sul costo §7: i requisiti di posa per il sensore in moto (5,2 cm; 0,375 m/s): capitolo 8.
- Alternative minori dei giudizi non chieste dalla consegna: rotta convergente come modulo a sé (è la stessa grandezza del massimo avvicinamento), compensazione della latenza sul segno, livelli d'allarme com'erano scritti, soglia sul pixel per cella, dicitura «nessun ostacolo osservato». Stanno nella tabella degli esclusi della soluzione finale (§4).
- Dei lavori correlati del fascicolo 06: le specifiche d'errore delle camere (2 % a 2 m e a 4 m, σ_d), che sono dati del capitolo 2; gli intervalli statistici (capitolo 6); il capoverso sui dati pubblici (capitolo 6 o appendice B). Tolta `gupta2018` (citazione nominale accanto a una cifra).
- Le citazioni nominali (`pellegrini2009`, `lerner2007`, `koch2007`, `wyffels2015`, `krejci2026`, `elfes1989`, `barshalom2001`) reggono solo frasi di attribuzione, mai una cifra.

## 5. Fonti da aggiungere alla bibliografia (stato dell'arte dei classificatori)

Nessuna è in `allegato.bib`: le frasi del capoverso «Rete neurale e classificazione» sono **senza citazione**. Dati come stanno in `f14-classificazione/03-classificatore/CLASSIFICATORE.md` §3 (non riaperti da me).

| Fonte | Dati | Che cosa sosterrebbe | Stato in quel file |
|---|---|---|---|
| Elenco delle classi COCO | file `coco.yaml` del deposito Ultralytics, `https://raw.githubusercontent.com/ultralytics/ultralytics/main/ultralytics/cfg/datasets/coco.yaml` | 80 classi; 9 tipi della tassonomia presenti; assenti carrello elevatore, tram, multirotore, carrozzina | verificato su quel file, non sull'articolo di COCO (che andrebbe citato al suo posto: dati bibliografici **non verificati**) |
| LOCO | deposito `https://github.com/tum-fml/loco`; ICMLA 2020 | insieme di dati per carrelli elevatori e logistica (RGB, non profondità) | letto il deposito; autori e titolo dell'articolo non riportati |
| Apron Dataset | deposito `https://github.com/apronai/apron-dataset`; ACCV 2022 Workshops, pp. 147–163 | mezzi di piazzale, 43 categorie; dati a richiesta, uso non commerciale | letto il deposito |
| Guo et al., 2017 | `https://arxiv.org/abs/1706.04599` | le reti moderne sono tarate male; correzione a posteriori (scala di temperatura) | letto il riassunto; titolo e sede non riportati |
| Hendrycks e Gimpel, 2016 | `https://arxiv.org/abs/1610.02136` | probabilità massima come linea di base per il fuori distribuzione | letto il riassunto (non usata nel capitolo) |

Non usate nel capitolo, presenti in quel file: RF-DETR e YOLO26 (latenze dichiarate su altre macchine), Gupta et al. 2014 e PointNet (sola profondità), Ristic, Gordon, Bessell 2004, Chiu et al. 2020, arXiv 2410.13616 (cinematica), TIDE (tipi d'errore).

## 6. Dubbi

1. La retta tempo–oggetti seguiti (0,33 + 0,30 n_T) e l'estrapolazione a 152 sono un'elaborazione non vagliata da un secondo lettore (lo dice il fascicolo): nel capitolo è scritto «l'estrapolazione non è stata verificata». Se la si vuole più prudente, togliere la riga dei 50 ms.
2. La dimostrazione del lemma sul tetto dei passi di raggio è dell'autore del fascicolo e attende una seconda lettura; l'ho trascritta, sostituendo «piano della griglia» con «superficie di separazione».
3. «Profondità simulata dalle schede tecniche» per le 162 sequenze della tabella del tempo per ciclo: il fascicolo dice solo «profondità simulata 424 × 240»; ho usato la dicitura prescritta dalla consegna. Da confermare con il capitolo 6.
4. Il conto «0,75 s a 4 m/s, 0,27 s per la conferma» viene dal file sul classificatore, un solo autore.
