# Verifica avversaria dell'allegato — citazioni e bibliografia

**Esito in tre righe.**
1. Controllate **138 citazioni** (occorrenze di chiave; 78 chiavi distinte, 13 file) contro `allegato.bib` e contro la mappa «affermazione → chiave»; le **90 voci** del `.bib` nella forma; **52 voci** contro le risposte grezze di Crossref; **41 fonti riaperte oggi in rete** con la frase letta (22 portano una cifra), più `ahn2019` sulla copia già nel progetto.
2. **Tornano 128 citazioni su 138** (chiave presente, frase dentro la mappa, cifra uguale alla fonte dove l'ho riaperta); 52 voci su 52 hanno dati bibliografici coincidenti con il registro, salvo tre differenze di forma.
3. **Non tornano 7 citazioni** (2 non sostenute dalle fonti citate, 5 imprecise) e **3 tornano con riserva**; in più: 3 frasi su dati pubblici senza citazione, 1 capoverso di letteratura senza fonti, 12 voci mai citate, 11 avvisi di BibTeX, 20 voci composte con l'indirizzo stampato due volte.

«Torna», per le 52 citazioni (33 chiavi) la cui fonte non ho riaperto oggi, vuol dire solo «coerente con la mappa»: non è una rilettura della fonte.

## In testa: cambi di stato e regole

**Cambi di stato.**
- **«C = 0,85 m»**: da «non citabile, non riscontrato» a **verificato su fonte secondaria**. Il testo aperto di `marvel2017` (PMC5117641, tabella 5) riporta dalla norma «40 mm < d < 70 mm: 850 mm» per l'avvicinamento perpendicolare (correzione 4). Riserva: l'attribuzione delle righe della tabella è letta su testo estratto dalla pagina.
- **«scenari ripresi da camere fisse dall'alto»**: da «nota dell'elenco» a **non sostenuto dalle fonti citate** (correzione 1).
- **«BibTeX senza avvisi»**: **smentito**, 11 avvisi (correzione 13).
- Licenza CC BY 4.0 di DepthTrack: **riconfermata** oggi sulla scheda Zenodo (API, `license: cc-by-4.0`).

**Regole: scostamenti.**
- **Rete.** La consegna è contraddittoria: «Il tuo controllo» chiede di riaprire in rete almeno 15 fonti, la riga «Regole» dice «niente rete». Ho seguito l'istruzione specifica e il contratto («nelle richieste alla rete solo titoli e identificativi pubblici»). Le richieste (84: 82 in `scaricati/esito_richieste.tsv`, più due lanciate a mano, una a Crossref di prova e una a PMC) contengono solo DOI, identificativi arXiv, indirizzi pubblici dei costruttori e un titolo pubblico; agente utente generico. Servizi toccati: Crossref, arXiv, Europe PMC e PMC, Semantic Scholar, Zenodo, siti dei costruttori e dei rivenditori già nel `.bib`. Se «niente rete» era la regola voluta, questo è uno scostamento da giudicare.
- L'ambiente chiede di non scrivere rapporti `.md`; la consegna chiede questo file: ho seguito la consegna.
- Le previsioni portano l'ora «19:28» scritta a mano; `date -Is` dava 19:26:25 prima e 19:27:52 dopo.
- Scritto solo in `24-verifica-citazioni/`. Niente sudo. **Git:** a lavoro finito ho lanciato per errore un `git status` (sola lettura, nessuna modifica) per controllare di non aver toccato altro: la regola dice «niente git», lo dichiaro. Il materiale scaricato è in `scaricati/`, mai eseguito. `allegato.bib` non è toccato (`cmp` con l'originale: identico).

**Indipendenza.** Con gli autori condivido il modello linguistico, la mappa e i fascicoli; non condivido i programmi (riscritti) né le letture: la parte indipendente sono le pagine riaperte oggi. Per le fonti non riaperte il mio controllo non vale contro un errore già presente nell'elenco dei riferimenti.

**Previsioni (in `programmi/previsioni.txt`, scritte prima dei controlli) ed esiti.**

| | Previsione | Esito |
|---|---|---|
| P1 | ogni chiave citata è nel `.bib` | **regge**: 0 mancanti su 78 |
| P2 | nessuna chiave N regge una cifra o un fatto | **smentita**: `pellegrini2009`, `lerner2007` (correzione 1), `barshalom2001` (correzione 8) |
| P3 | almeno 10 voci mai citate | **regge**: 12 |
| P4 | BibTeX: 0 errori, 0 avvisi | **smentita**: 0 errori, 11 avvisi |
| P5 | nel campione riaperto almeno uno scostamento | **regge**: correzioni 2, 3, 5 |

## Correzioni

### A. Non sostenuto dalla fonte citata

**1. Capitolo 7, «Predittori appresi delle traiettorie» (`07_costo.tex` r. 152): «cinque scenari di pedoni ripresi da camere fisse dall'alto \cite{pellegrini2009,lerner2007}».**
Le due chiavi sono nominali (N): reggono solo «fonti dei dati ETH e UCY». «Camere fisse dall'alto» non è in nessuna delle fonti citate che ho potuto leggere: il riassunto di `lerner2007` su Crossref dice solo «tracked video segments of real pedestrian crowds»; di `pellegrini2009` il registro non dà il riassunto; nel testo di `scholler2020` (arXiv 1903.07933) «birds eye» compare solo a proposito di un altro lavoro. Il fascicolo 06 lo segnala già (II.6, D7). L'allegato ha anche tolto i nomi degli insiemi, cioè l'unica cosa che le due chiavi sostengono. Le sei cifre (0,39/0,83; 0,44/0,91; 0,32/0,60) **tornano** con la tabella I dell'articolo.
Testo corretto:
> `Sull'orizzonte di 4,8 s, sulla media dei cinque scenari degli insiemi pubblici ETH e UCY \cite{pellegrini2009,lerner2007}, il modello a velocità costante ha errore medio e finale di 0,39 m e 0,83 m, contro 0,44 m e 0,91 m del miglior predittore appreso deterministico e 0,32 m e 0,60 m di un modello generativo valutato sul migliore di 20 campioni \cite{scholler2020}; i predittori addestrati sulla verosimiglianza tendono a distribuzioni troppo o troppo poco sicure \cite{cheraghipouria2026}. Il confronto riguarda il punto previsto, non una regione, non comprende occlusioni, e quei dati non vengono da un sensore di profondità frontale.`

Facoltativo, e solo se la cifra entra in `CIFRE.md` (non è nei fascicoli; letta oggi nella stessa tabella): nello stesso articolo la velocità costante con campionamento, valutata anch'essa sul migliore di 20, ha 0,28 m e 0,56 m, meglio del modello generativo.

### B. Impreciso rispetto alla fonte

**2. Capitolo 2 (`02_geometria.tex` r. 303): «scarto quadratico medio non superiore al 2 % a 4 m per la D455 \cite{realsense-d455}».**
La pagina del prodotto, riaperta oggi, dice «improves the depth error to less than 2% at 4 m» e «Depth Accuracy: <2% at 4 m»: non parla di scarto quadratico medio. Lo scarto quadratico medio («RMS Error (or Spatial Noise) ≤ 2%», D455 «up to 4 Meters and 80% ROI, HD Resolution»; D435/D435i «up to 2 Meters») è nella pagina `realsense-d400-accuratezza`, che la mappa indica per questo dato. Mancano anche le condizioni (80 % della regione, risoluzione HD), mentre il sistema lavora a 848 × 480 o 424 × 240. Per la Gemini 335 la fonte dà «≤ 1.5% (1280 x 800 @ 2m & 90% x 90% ROI)»: torna, manca la condizione. I tre valori di k non cambiano.
Testo corretto:
> `Il valore «limite» si ricava dal massimo dichiarato: scarto quadratico medio non superiore al 2 \% fino a 4 m per la D455 e fino a 2 m per la D435i, sull'80 \% della regione utile e a risoluzione HD \cite{realsense-d400-accuratezza} ($k=0{,}02\cdot4/16=0{,}005\unita{m^{-1}}$ e $k=0{,}010\unita{m^{-1}}$; per la D455 la pagina del prodotto indica un errore di profondità inferiore al 2 \% a 4 m \cite{realsense-d455}), e all'1,5 \% a 2 m per la Gemini 335, a 1280 × 800 e sul 90 \% × 90 \% della regione \cite{orbbec-gemini-335} ($k=0{,}0075\unita{m^{-1}}$); per quest'ultima il nominale ($k=0{,}004\unita{m^{-1}}$) è letto da un grafico della scheda.`

**3. Capitolo 8, tabella della latenza (`08_limiti.tex` r. 104, `tab:lim-latenza`): «95 ms … misura pubblicata dal costruttore sull'intero banco di prova».**
La cifra torna (tabella 4 della fonte: «848×100 30fps 95», colonna «Average (ms)»; «captured for a Windows 10 system»; «we cannot measure the Depth Camera latency directly»). Manca la condizione: la misura è nel modo **848 × 100**, non alla risoluzione del sistema; è una latenza dal movimento allo schermo.
Testo corretto della cella «Natura del dato»:
> `misura pubblicata dal costruttore sull'intero banco di prova, dal movimento allo schermo, nel modo $848\times100$ a 30 fotogrammi al secondo \cite{realsense-alta-velocita-d435}: stima per eccesso del solo sensore, non misurata alla risoluzione usata qui; media, senza percentili`

**4. Capitolo 8 (`08_limiti.tex` r. 74): «C somma 0,85 m, valore attribuito alla norma sul posizionamento dei ripari e non riscontrato sul testo».**
È una cifra di letteratura senza fonte. La fonte secondaria già citata la riporta: `marvel2017`, testo aperto su PMC (PMC5117641), tabella 5: avvicinamento perpendicolare, «40 mm < d < 70 mm: 850 mm», «Multiple Separate Beams: 850 mm»; nel testo «the value of C must be at least 850 mm»; la forma «S = vT + C» è attribuita a ISO 13855 e la velocità di 1600 mm/s è confermata. La norma resta non letta.
Testo corretto:
> `La forma «velocità per tempo più costante» è quella della distanza di protezione nella sorveglianza di velocità e separazione; $C$ somma $0{,}85\unita{m}$, valore che la stessa fonte riporta dalla norma sul posizionamento dei ripari per l'avvicinamento perpendicolare con capacità di rilevamento fra 40 e 70 mm \cite{marvel2017} (la norma non è stata consultata nel testo originale), e $0{,}10\unita{m}$ d'incertezza del sensore: il confronto dà un ordine di grandezza e non è una dichiarazione di conformità.`

Che la capacità di rilevamento del sistema stia fra 40 e 70 mm non è verificato: la condizione va lasciata scritta.

**5. Capitolo 2 (`02_geometria.tex` r. 289): «rumore laterale di 4,3 cm, al 90° percentile, sul bordo sinistro del bersaglio \cite{ahn2019}, cioè dal lato previsto».**
La cifra torna (copia dell'articolo nel progetto, `f10-dati/02-sensori/scaricati/ahn.txt`: «σL = 0.0432 m»). La stessa riga dà però «σR = 0.0407 m» per il bordo destro: la differenza è di 2,5 mm, e l'asimmetria che l'articolo descrive a parole («shadowing at the left edge … noticeably worsens») riguarda la rotazione del bersaglio. «Cioè dal lato previsto» fa dire alla cifra più di quanto dica.
Testo corretto:
> `Una misura di terzi su una camera della stessa famiglia descrive un'ombra che peggiora sul bordo sinistro del bersaglio quando questo ruota, cioè dal lato previsto, e riporta un rumore laterale al 90° percentile di 4,3 cm sul bordo sinistro e di 4,1 cm sul destro \cite{ahn2019}: le due cifre sono vicine e non misurano l'ampiezza della banda;`

(Il 4,1 cm è letto oggi nella fonte e non è nei fascicoli: va aggiunto a `CIFRE.md` con questa origine.)

**6. Tre frasi su dati pubblici senza citazione.**
- `04_stima.tex` r. 27: «l'unico dato da una sequenza pubblica reale (altro sensore della stessa famiglia, 288 fotogrammi…)». È la sequenza `human02` di DepthTrack, ripresa con una D415 (`f10-dati/20-validazione/VALIDAZIONE_DATI.md` r. 38 e 80; `uscite/vere/RIEPILOGO.txt`). Testo: `… da una sequenza pubblica reale \cite{depthtrack} (altro sensore della stessa famiglia, 288 fotogrammi, senza verità di riferimento) …`
- `08_limiti.tex` r. 59: «su una registrazione pubblica quella stima sbaglia di 5°». È TUM (`VALIDAZIONE_DATI.md` r. 153; `VERDETTO_DATI.md` r. 43). Testo: `(su una registrazione pubblica \cite{tum-rgbd} quella stima sbaglia di $5^\circ$ \prova{P})`
- `01_introduzione.tex` r. 130, `06_valutazione.tex` r. 284, `08_limiti.tex` r. 171: «7,8 % … contro 24–34 % in registrazioni pubbliche». **Non risolto**: nessun file che ho letto dice da quali registrazioni viene il 24–34 %. Le registrazioni reali elaborate sono otto (`RIEPILOGO.txt`): una TUM, una DepthTrack, tre Princeton, tre file di esempio del costruttore. Lo decide il programma che ha prodotto la cifra. Finché non è deciso la frase resta senza citazione; se vi entrano i file di esempio del costruttore va detto che sono fatti con esemplari di pre-produzione (fascicolo 06, II.6, D1).

**7. Appendice B (`B_riproducibilita.tex` r. 3): l'elenco dei dati pubblici è incompleto.**
Cita `thor`, `tum-rgbd`, `depthtrack`; il progetto ha elaborato anche tre sequenze Princeton e tre file di esempio del costruttore, e il fascicolo 06 (parte I, «Dati pubblici») cita tutte e cinque le fonti. Se una cifra dell'allegato viene da quelle sei sequenze (vedi 6, terzo punto), le due voci vanno citate; se nessuna, vanno tolte dal `.bib` finale (correzione 12). Le licenze sono nelle note del `.bib` per le tre voci citate (CC BY 4.0 ciascuna) e compaiono in bibliografia: torna. Per Princeton la mappa dice «licenza non dichiarata»: va scritto se la voce entra.
Testo, nel caso entrino:
> `I dati pubblici sono traiettorie di pedoni al chiuso con verità di riferimento \cite{thor}, che non contengono profondità, e sequenze di profondità registrate \cite{tum-rgbd,depthtrack,princeton-tracking-benchmark}, fra cui registrazioni di esempio di camere a stereo attivo fatte dal costruttore con esemplari di pre-produzione \cite{realsense-file-di-esempio}.`

**8. Capitolo 7, lavori correlati (`07_costo.tex` r. 160): «la teoria della stima per il seguimento, con il modello a velocità quasi costante e le porte di associazione, è materia di manuale \cite{barshalom2001}».**
Voce nominale: è verificato solo il titolo. Che il manuale tratti le porte di associazione non è stato letto.
Testo corretto: `la teoria della stima per il seguimento è materia di manuale \cite{barshalom2001}.`

**9. Tre citazioni che dicono più della mappa (tornano con riserva).**
- `04_stima.tex` r. 179 e `06_valutazione.tex` r. 288: «posizioni da cattura del moto», «registrati con un sistema di cattura del moto» \cite{thor}. La mappa dà solo «verità di riferimento»; la scheda Zenodo parla di «accurate ground truth» e di un lidar 3D, e ha file chiamati `…_qualisys.bag`: è un indizio, non la frase. Testo prudente: `(persone al chiuso, con posizioni di riferimento accurate)` e `Tracciati di persone in cammino al chiuso, con verità di riferimento per la posizione e senza immagini di profondità \cite{thor}`.
- `03_mappa.tex` r. 166: «un'altra camera di profondità, tenuta in mano \cite{tum-rgbd}». «Tenuta in mano» non è nella mappa e non l'ho trovata nelle due pagine salvate. Testo prudente: `ripresa con un'altra camera di profondità \cite{tum-rgbd}`.

**10. Capitolo 7, «Rete neurale e classificazione» (`07_costo.tex` r. 150): quattro affermazioni di letteratura senza citazione** (insieme COCO; insiemi dedicati a carrelli elevatori e mezzi di piazzale; reti mal tarate; correzioni a posteriori). `NOTE.md` §5 le elenca con dati incompleti. Dati che ho verificato oggi, pronti per il `.bib`:
```bibtex
@inproceedings{lin2014,
  author = {Lin, Tsung-Yi and Maire, Michael and Belongie, Serge and Hays, James and Perona, Pietro and Ramanan, Deva and Doll{\'a}r, Piotr and Zitnick, C. Lawrence},
  title = {{Microsoft COCO: Common Objects in Context}},
  booktitle = {Computer Vision -- ECCV 2014},
  series = {Lecture Notes in Computer Science},
  publisher = {Springer},
  pages = {740--755},
  year = {2014},
  doi = {10.1007/978-3-319-10602-1_48}
}
@inproceedings{guo2017,
  author = {Guo, Chuan and Pleiss, Geoff and Sun, Yu and Weinberger, Kilian Q.},
  title = {{On Calibration of Modern Neural Networks}},
  booktitle = {International Conference on Machine Learning (ICML)},
  year = {2017},
  eprint = {1706.04599},
  archivePrefix = {arXiv}
}
```
`guo2017`: letto il riassunto («modern neural networks … are poorly calibrated»; «temperature scaling … is surprisingly effective»): sostiene la frase. Volume e pagine degli atti non verificati, non scritti. `lin2014`: solo dati bibliografici (Crossref); vale come citazione nominale dell'insieme, non per «80 classi» né per «9 tipi su 25», che è un conto del progetto su un file di terzi. Gli insiemi per carrelli e mezzi di piazzale: **non verificati** (non riaperti).
Testo corretto, dopo l'aggiunta delle due voci:
> `… i rilevatori pronti addestrati sull'insieme pubblico di immagini COCO \cite{lin2014} coprono, secondo un conto fatto sull'elenco delle sue classi, 9 dei circa 25 tipi della tassonomia del \S\ref{sec:sti} (non carrello elevatore, tram, multirotore, carrozzina) e chiedono l'immagine a colori; la letteratura riporta che le reti moderne danno probabilità mal tarate e propone una correzione a posteriori \cite{guo2017}.`

La frase «per carrelli elevatori e mezzi di piazzale esistono insiemi di dati dedicati» va tolta, oppure resta senza citazione e dichiarata non verificata.

**11. Capitolo 4, tabella dei profili (`04_stima.tex` r. 84, `tab:sti-profili`) e capitolo 8 (`08_limiti.tex` r. 93): fonti dichiarate ma non nominate.**
La didascalia dice «fonte pubblica consultata, di terza mano» senza dire quale: per il lettore è un'affermazione di letteratura senza riferimento. Le fonti di `NOTE.md` §5 sono in gran parte voci di enciclopedia: non contano come fonti primarie e non le propongo per il `.bib`. Due primarie hanno dati bibliografici che ho verificato oggi su Crossref, **non il contenuto**:
- Bohannon R. W., «Comfortable and maximum walking speed of adults aged 20–79 years: reference values and determinants», *Age and Ageing* 26(1), 15–19, 1997, DOI 10.1093/ageing/26.1.15.
- Green M., «"How Long Does It Take to Stop?" Methodological Analysis of Driver Perception-Brake Times», *Transportation Human Factors* 2(3), 195–216, 2000, DOI 10.1207/STHF0203_1.

Finché le cifre non sono lette su queste fonti, non si citano. Testo corretto della didascalia:
> `Profili cinematici a priori delle classi: un profilo di partenza, non un riferimento. Origine dei valori: $^{a}$ letto in una fonte pubblica di terza mano, non riscontrato su una fonte primaria e per questo senza riferimento bibliografico; $^{b}$ letto in un risultato di ricerca o riportato a memoria, non verificato; senza marca: ipotesi. Solo 9 velocità su 30 hanno una fonte consultata.`

La frase del capitolo 8 «è la reazione di frenata a sorpresa di un conducente riportata in letteratura, non verificata sulla fonte» è già corretta nel livello: resta com'è, senza citazione.

### C. Forma

**12. Dodici voci del `.bib` mai citate** (`programmi/conteggi.txt`): `gupta2018`, `librealsense`, `luiten2021`, `mercat2019`, `orbbec-femto-bolt`, `orbbec-gemini-330-scheda`, `princeton-tracking-benchmark`, `realsense-d400-scheda`, `realsense-file-di-esempio`, `st-vl53l5cx`, `ufomap-deposito`, `williams1978`. Nessuna frase dei capitoli ne ha bisogno (ricerca di 14 espressioni: 0 riscontri). Con lo stile in uso non compaiono nella bibliografia composta. Vanno tolte dal `.bib` finale, salvo `princeton-tracking-benchmark` e `realsense-file-di-esempio` (correzione 7) e, se si vuole, `gupta2018` come citazione nominale: `un modello generativo \cite{gupta2018} valutato sul migliore di 20 campioni`.

**13. BibTeX: 11 avvisi «empty year»** (`prova_bibtex/bibtex_originale.out`, uguale a `20-unione/b.out`): `realsense-d455`, `realsense-confronto-camere`, `orbbec-gemini-335`, `realsense-taratura-profondita`, `realsense-filtri-post`, `st-um3038`, `slamtec-rplidar-c1`, `ldrobot-ld19`, `octomap`, `us-49cfr-236-205`, `realsense-alta-velocita-d435`. Nel `.bib` le voci senza `year` sono 14 (le altre tre non sono citate).
Correzione provata su una copia (`programmi/correggi_bib_prova.py` → `prova_bibtex/allegato_corretto_prova.bib`): aggiungere `year = {2022}` a `st-um3038` (nel PDF: «© 2022 STMicroelectronics», Rev 2) e `year = {s.d.}` alle pagine senza data. Esito: **0 avvisi, 0 errori**, 78 voci. Effetto collaterale: lo stile aggiunge una lettera alle voci dello stesso autore («s.d.a», «s.d.b»).

**14. Venti voci composte stampano lo stesso indirizzo due volte** (campo `url` più `\url{…}` nella nota): `therobotreport-veo`, `realsense-d455`, `realsense-confronto-camere`, `orbbec-gemini-335`, `realsense-taratura-profondita`, `realsense-filtri-post`, `realsense-bkm-taratura`, `realsense-d400-accuratezza`, `st-vl53l7cx`, `st-vl53l8cx`, `st-um3038`, `slamtec-rplidar-c1`, `ldrobot-ld19`, `tum-rgbd`, `octomap`, `st-um2884`, `us-brevetto-11846916`, `us-49cfr-236-205`, `giudice2008`, `realsense-alta-velocita-d435`. Prova: conteggio sul `.bbl` di `20-unione`. Correzione: nella nota lasciare solo «consultato il 14 novembre 2026». Nella stessa copia di prova: 0 voci con l'indirizzo ripetuto. Accorcia anche la bibliografia, oggi di 6 pagine.

**15. Dati bibliografici: differenze minori** (`programmi/confronto_crossref.tsv`, 52 voci confrontate, 49 coincidono).
- `krejci2026`: titolo nel registro «Multiobject», nel `.bib` «Multi-Object».
- `barshalom2001`: il registro dà 2002 (data in rete); il 2001 dell'edizione a stampa resta da riscontrare sul frontespizio (già D4 del fascicolo 06).
- `guibas1997`, `barber2019`, `kress2021`, `pang2021`, `dixit2022`: la chiave porta un anno diverso dal campo `year` (1999, 2021, 2023, 2023, 2023). Con le citazioni numeriche non si vede; nessuna azione necessaria.
- Schede e norme raggiunte da siti di rivenditori o copie non ufficiali (`st-*`, `orbbec-gemini-330-scheda`, `ldrobot-ld19`, `us-49cfr-236-205`): per una commissione è preferibile l'indirizzo del costruttore o del registro ufficiale. Non ho verificato che quegli indirizzi esistano: è una proposta, non una correzione pronta.
- Il testo scrive «Intel RealSense», la bibliografia ha autore «RealSense»: uniformare.

## Fonti riaperte oggi: ciò che torna

Costruttori (pagine e PDF grezzi): `realsense-taratura-profondita` («depth error scales as the square of the distance»; «D435 with HFOV=90deg, Xres=848, and baseline=50mm … subpixel=0.08»: la fonte dice D435, la tabella dell'allegato lo usa per la D435i); `realsense-bkm-taratura` («Subpixel RMS error of less than 0.1»); `realsense-d455` (87° × 58°, 0,6–6 m, 95 mm); `realsense-confronto-camere` (D435/D435i: 87° × 58°, 0,3–3 m); `realsense-filtri-post` (persistenza predefinita «Valid in 2/last 4»; riempimento predefinito dal vicino più lontano, cioè lo sfondo); `orbbec-gemini-335` (50 mm, H90° V65° fino a 1280 × 800, 0,26–3 m); `st-vl53l7cx` (60° × 60°; 8 × 8 a 15 Hz: 2000 mm al buio e 500 mm a 5 klx, valori tipici, bersaglio bianco, zone interne); `st-vl53l8cx` (8 × 8: 1550 mm a 5 klx, stesse condizioni); `st-um2884` (4 × 4 fino a 60 Hz, 8 × 8 fino a 15 Hz); `st-um3038` (stato 10; «All other statuses are below 50 % confidence level»); `slamtec-rplidar-c1` (0,72°, 10 Hz tipici); `ldrobot-ld19` (4500 Hz, 10 Hz); `octomap` (sorgente: 0,7, 0,4, 0,1192, 0,971; sito: «implicitly encoded»).
Articoli: `bewley2016` (260 Hz); `cao2023`; `zhang2022`; `barber2019`; `gibbs2021`; `cheraghipouria2026`; `kozlov2026` (93,75 % con 14 utenti, 92,9 % con 22: la fonte usa sensori a tempo di volo); `hsieh2023`; `tokmakov2021`; `vanhoorick2023`; `khurana2021`; `balch2019`; `dixit2022`; `aharon2022`; `scholler2020` (tabella I); `lindemann2023` (v2: «498 of the 500 test trajectories», δ = 0,05, T = 20, scambiabilità); `romlay2021` (70; 51,4 %; 22,9 %); `martinez2014` («22 times higher», non nei bendati); `lupu2020` («eight visually impaired subjects»; aptico meno intuitivo); `marvel2017` (1600 mm/s); `brown2001`; `qiu2023`; `nuss2018`; `cleaveland2024`; `niessner2013`; `depthtrack` (licenza).
Riaperte solo in parte: `angelopoulos2021` (riassunto: senza ipotesi sulla distribuzione; «marginale» e «scambiabili» non sono nel riassunto); `kayukawa2019` (riassunto: aeroporto, partecipanti non vedenti; «sei», le soglie di 5 s e 2,5 s e l'estrapolazione lineare **non** sono nel riassunto: restano allo stato dell'elenco).

## Che cosa non ho controllato

- **Non riaperte oggi** (33 chiavi citate, 52 citazioni; valgono solo per coerenza con la mappa): `barshalom2001`, `hornung2013`, `duberg2020`, `moras2011`, `elfes1989`, `oleynikova2017`, `millane2024`, `usenko2017`, `weng2020`, `pang2021`, `kalman1960`, `kuhn1955`, `koch2007`, `wyffels2015`, `krejci2026`, `orzechowski2018`, `koschi2021`, `guibas1997`, `scholl1999`, `uhlemann2024`, `kress2021`, `gneiting2007`, `wilson1927`, `clopper1934`, `therobotreport-veo`, `us-brevetto-11846916`, `us-49cfr-236-205`, `xu2023`, `dossantos2025`, `giudice2008`, `thor` (articolo), `tum-rgbd` (articolo), `pellegrini2009` (testo). Per `duberg2020`, `uhlemann2024`, `koschi2021`, `orzechowski2018`, `oleynikova2017`, `usenko2017`, `kress2021`, `weng2020`, `xu2023` Crossref non dà il riassunto.
- I valori di scheda senza citazione della tabella del capitolo 2 (distanze minime, focale e campo della terza camera, ±3°): non riscontrati; la pagina di confronto dà distanze minime alla risoluzione massima (circa 52 cm e 28 cm), diverse da quelle della tabella, che vengono da un'altra risoluzione.
- Le norme (ISO 13855, ISO/TS 15066): mai lette, come nei fascicoli.
- Il PDF: non ho riletto la bibliografia composta pagina per pagina; ho controllato `.bbl`, `.blg` e sorgenti. Non ho ricompilato con XeLaTeX.
- Le cifre del progetto accanto alle citazioni (219 tratti, 9 persone, 81 ms, 288 fotogrammi…): fuori dal mio controllo, sono dell'altra verifica.
- La correzione del `.bib` è provata solo con BibTeX su una copia: l'aspetto finale di «s.d.a» nel PDF non è stato guardato.

## Cifre lette oggi nelle fonti e non presenti nei fascicoli

| Cifra | Fonte | Dove servirebbe |
|---|---|---|
| 848 × 100 (modo della misura dei 95 ms) | `realsense-alta-velocita-d435`, tabella 4 | correzione 3 |
| 4,1 cm (bordo destro, σR = 0,0407 m) | `ahn2019`, copia nel progetto | correzione 5 |
| 40–70 mm (condizione di C = 850 mm) | `marvel2017`, tabella 5, testo aperto su PMC | correzione 4 |
| 0,28 m e 0,56 m (velocità costante con campionamento) | `scholler2020`, tabella I | correzione 1, facoltativa |
| 80 % della regione, risoluzione HD; 1280 × 800, 90 % × 90 % | `realsense-d400-accuratezza`; `orbbec-gemini-335` | correzione 2 |

## Che cosa propongo dopo

1. Applicare le correzioni 1–5 e 8 (testo pronto) e aggiungere le due citazioni della 6.
2. Far dire al programma d'origine da quali registrazioni viene il «24–34 %», poi chiudere 6 e 7.
3. Decidere fra `s.d.` e l'anno di consultazione per le pagine senza data, applicare 13 e 14 al `.bib` e ricompilare.
4. Leggere Bohannon 1997 e Green 2000 prima di citarli; fino ad allora la didascalia della 11.

## Programmi e dati (in questa cartella)

`programmi/`: `previsioni.txt`; `estrai_cite.py` → `cite_estratte.tsv`, `conteggi.txt`; `controlla_bib.py` → `bib_campi.tsv`; `scarica.sh`, `scarica_2.sh`, `scarica_3.sh` con gli elenchi `elenco_richieste*.tsv`; `in_testo.py`; `cerca.sh`; `confronta_crossref.py` → `confronto_crossref.tsv`; `correggi_bib_prova.py`. `scaricati/`: le risposte grezze, `testo/` con il testo estratto, `esito_richieste.tsv`. `prova_bibtex/`: copia del `.aux` e del `.bib`, uscite di BibTeX prima e dopo; il `.bbl` lì dentro è quello della copia corretta.
