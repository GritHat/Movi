# Fascicolo 06 — Bibliografia dell'allegato e stato dell'arte

File collegati nella stessa cartella: `allegato.bib` (90 voci), `programmi/` (con `rifai.sh`), `scaricati/` (risposte dei registri, dato non fidato), `prova/` (compilazione di prova).

<!-- INIZIO PARTE I -->
# PARTE I — Contenuto per l'allegato

Simboli: quelli della notazione comune; nessun simbolo nuovo.

## 1. Lavori correlati e stato dell'arte

**Sensori di profondità e loro rumore.** Il sistema usa una camera di profondità a stereo attivo. Per questa famiglia di sensori la documentazione del costruttore dichiara che l'errore di profondità cresce con il quadrato della distanza e traccia la curva teorica con un errore di disparità $\sigma_d = 0{,}08$ pixel su un bersaglio ben tessuto \cite{realsense-taratura-profondita}; la stessa documentazione indica meno di 0,1 pixel per una camera ben tarata \cite{realsense-bkm-taratura}. Le specifiche dichiarate sono un errore non superiore al 2 % fino a 2 m per i modelli D435 e D435i, sull'80 % della regione utile \cite{realsense-d400-accuratezza}, e meno del 2 % a 4 m per il modello con base di 95 mm \cite{realsense-d455}. Una caratterizzazione indipendente su un bersaglio planare bianco fra 0,4 e 2,1 m dà per il rumore assiale un polinomio di secondo grado nella distanza \cite{ahn2019}. Le alternative considerate hanno limiti documentati: i sensori a tempo di volo multizona offrono al più 8 × 8 zone a 15 Hz, oppure 4 × 4 zone a 60 Hz \cite{st-um2884}, con una portata che la luce ambiente riduce (per esempio da 3,5 m al buio a 0,65 m a 5 klx nel modo 4 × 4 di un modello con campo di 60°) \cite{st-vl53l7cx}; l'uso all'aperto delle camere a tempo di volo resta limitato dall'interferenza solare \cite{qiu2023}; un LiDAR 2D rotante economico misura un solo strato orizzontale, a circa 10 Hz e con risoluzione angolare di 0,72° \cite{slamtec-rplidar-c1}. Tutte queste cifre sono dichiarazioni dei costruttori o misure di terzi: non sono misure fatte sul sistema descritto.

**Mappe di occupazione e stato «sconosciuto».** Le griglie di occupazione sono la rappresentazione classica per la percezione dei robot mobili \cite{elfes1989}. OctoMap rappresenta in modo esplicito, oltre allo spazio occupato, anche quello libero e quello sconosciuto \cite{hornung2013}; nella sua realizzazione lo sconosciuto è codificato in modo implicito, come assenza di informazione \cite{octomap}. UFOMap dichiara una rappresentazione esplicita di tutti e tre gli stati \cite{duberg2020}. Le griglie evidenziali trattano l'ignoranza come una sorgente d'incertezza distinta dall'errore di misura \cite{moras2011}, e le griglie dinamiche di occupazione sono state realizzate in tempo reale con un filtro a particelle in parallelo \cite{nuss2018}. Le mappe volumetriche a distanza con segno funzionano in tempo reale su un solo nucleo di CPU \cite{oleynikova2017} o su GPU \cite{millane2024,niessner2013}, e per i veicoli in volo è stata proposta una griglia locale, in un buffer circolare, che si muove con il veicolo \cite{usenko2017}. Rispetto a questi lavori il sistema adotta una mappa polare del suolo, centrata su una camera ferma, con quattro stati: separa cioè lo sconosciuto in «in ombra» $\Omega(t)$ (dietro un ostacolo osservato) e «non osservato», e non aggiorna una probabilità per cella. È una scelta di semplicità: non è stata confrontata sperimentalmente con le librerie citate.

**Seguimento di più oggetti e occlusioni.** Lo schema «rilevamento, filtro di Kalman \cite{kalman1960}, assegnazione ottima \cite{kuhn1955}» è quello di SORT, che dato l'insieme dei rilevamenti aggiorna le tracce a 260 Hz \cite{bewley2016}, e della sua estensione in tre dimensioni \cite{weng2020}; la teoria della stima per il seguimento, con il modello a velocità quasi costante e le porte di associazione, è materia di manuale \cite{barshalom2001}. I perfezionamenti noti agiscono sull'associazione (uso di quasi tutti i rilevamenti, anche a basso punteggio \cite{zhang2022}; compensazione del moto della camera \cite{aharon2022}) e sulla gestione del ciclo di vita delle tracce, isolata come modulo a sé \cite{pang2021}. Durante un'occlusione il filtro, privo di misure, accumula errore \cite{cao2023}: è il punto in cui si colloca questo lavoro. La letteratura segue tre strade. La prima tratta l'occlusione come un problema di previsione a breve termine \cite{khurana2021} o la impara da dati che portano le annotazioni degli oggetti invisibili \cite{tokmakov2021}; i lavori di riferimento riconoscono però che i metodi faticano sotto occlusione pesante \cite{hsieh2023} e che resta un divario notevole rispetto a una vera permanenza dell'oggetto \cite{vanhoorick2023}. La seconda usa l'informazione «negativa», cioè la mancata osservazione là dove il sensore vede \cite{koch2007,wyffels2015,krejci2026}. La terza, nata nella guida automatica, sovrastima con insiemi lo stato di ciò che è nascosto \cite{orzechowski2018} e predice in forma insiemistica tutti i comportamenti ammissibili dei partecipanti rilevati e di quelli potenzialmente nascosti \cite{koschi2021}; il problema affine dell'inseguimento con visibilità considera un evasore imprevedibile, di posizione iniziale ignota e senza limite di velocità \cite{guibas1997}. Il sistema combina la prima e la terza strada: per l'oggetto già seguito mantiene una regione di previsione $\mathcal{R}_\alpha(t)$ dichiarata a un livello $\alpha$; per ciò che non è mai stato visto mantiene un insieme di possibile presenza $\Pi(t)$ costruito sull'ombra con una velocità massima assunta $v_{\max}$. La percezione umana offre un criterio per la resa: l'identità di un oggetto nascosto è mantenuta se scompare e ricompare lungo il bordo fisso dell'occlusore \cite{scholl1999}.

**Previsione dei pedoni e incertezza tarata.** Su orizzonti brevi il modello a velocità costante è un termine di confronto forte: a 4,8 s, sulla media dei cinque scenari ETH e UCY \cite{pellegrini2009,lerner2007}, ha errore medio e finale di 0,39 m e 0,83 m, contro 0,44 m e 0,91 m del miglior predittore appreso deterministico e 0,32 m e 0,60 m di un modello generativo valutato sul migliore di 20 campioni \cite{scholler2020,gupta2018}; un'analisi più recente conferma che approssima bene la dinamica nella maggior parte dei casi \cite{uhlemann2024}. Quei dati vengono da camere fisse dall'alto, non da un sensore frontale. L'accuratezza non basta: le previsioni probabilistiche vanno valutate per affidabilità e nitidezza \cite{kress2021} con punteggi propri \cite{gneiting2007}, e i predittori addestrati sulla verosimiglianza tendono a distribuzioni troppo o troppo poco sicure \cite{cheraghipouria2026}. La previsione conforme dà regioni con copertura marginale garantita senza ipotesi sulla distribuzione, purché i dati di taratura e di prova siano scambiabili \cite{angelopoulos2021}; è stata applicata alla pianificazione in ambienti dinamici, con regioni su 20 passi e 498 traiettorie di prova su 500 dentro la regione al 95 % \cite{lindemann2023}, resa meno prudente \cite{cleaveland2024} e adattata in linea quando la distribuzione cambia \cite{gibbs2021,dixit2022}. Due limiti noti valgono anche qui: la garanzia è marginale, e una copertura condizionata esatta è impossibile senza ipotesi sulla distribuzione \cite{barber2019}; una probabilità di collisione calcolata con dati peggiori può paradossalmente apparire più bassa \cite{balch2019}, il che motiva l'uso di regioni e insiemi anziché di una sola probabilità. Le frequenze misurate in questo lavoro sono riportate con l'intervallo di Wilson \cite{wilson1927}, raccomandato per le numerosità piccole al posto dell'intervallo normale, la cui copertura è irregolare \cite{brown2001}; dove serve un limite esatto si usa quello di Clopper e Pearson \cite{clopper1934}.

**Sicurezza dei sensori di presenza.** Nella sorveglianza di velocità e separazione dei robot collaborativi la distanza di protezione ha forma lineare, somma dei percorsi dell'operatore e del robot nei tempi di reazione e di arresto e di termini d'incertezza di posizione, con una velocità dell'operatore di 1,6 m/s \cite{marvel2017}. I sistemi 3D industriali di questo tipo classificano i volumi in vuoti, occupati e sconosciuti e trattano come occupato ciò che nessun sensore vede \cite{therobotreport-veo,us-brevetto-11846916}; il segnalamento ferroviario applica lo stesso principio a guasto sicuro, imponendo l'aspetto più restrittivo quando manca l'energia \cite{us-49cfr-236-205}. Il sistema ne riprende due principi: non dichiarare mai libero ciò che non è osservato, e segnalare in modo esplicito la perdita di affidabilità. Non è un dispositivo di protezione certificato, e nessuna conformità a norme di sicurezza delle macchine è rivendicata.

**Ausili per persone con disabilità visiva.** Le rassegne mostrano che efficacia e sicurezza sono la prima preoccupazione degli utenti \cite{xu2023} e che solo il 22,9 % di 70 lavori valuta il dispositivo con persone con disabilità visiva \cite{romlay2021}. Un sistema di avviso con previsione per estrapolazione lineare e soglie a 5 s e 2,5 s è stato provato con sei utenti non vedenti \cite{kayukawa2019}; esistono dispositivi indossabili con sensori di profondità e riscontro aptico \cite{dossantos2025,kozlov2026}. Sul canale d'uscita gli studi sono discordi: per chi usa il bastone il riscontro sonoro ha dato un carico cognitivo 22 volte maggiore di quello aptico, effetto assente nei partecipanti bendati \cite{martinez2014}; in un altro studio, con otto partecipanti, gli stimoli aptici sono risultati meno intuitivi di quelli sonori \cite{lupu2020}; la guida con suono spazializzato regge un compito secondario meglio del linguaggio spaziale \cite{giudice2008}. Il sistema non risolve questa scelta: espone gli stati e l'incertezza in forma indipendente dal canale.

**Dati pubblici.** Le elaborazioni su dati reali usano traiettorie di persone al chiuso con verità di riferimento accurata per la posizione \cite{thor}, sequenze RGB-D a 640 × 480 e 30 Hz con la traiettoria della camera \cite{tum-rgbd}, sequenze RGB-D per il seguimento di un bersaglio \cite{depthtrack,princeton-tracking-benchmark} e registrazioni di esempio di camere a stereo attivo, fatte dal costruttore con esemplari di pre-produzione \cite{realsense-file-di-esempio}. Nessuno di questi insiemi è stato acquisito con il sensore e nella posa del sistema descritto.

## 2. Dati esterni che entrano nei calcoli

**Osservazione 1 (rumore di profondità dello stereo attivo).** Dalla triangolazione $d = f b/\delta$ (con $\delta$ la disparità in pixel) segue, al primo ordine, $\sigma_z(d) = \dfrac{d^2}{f\,b}\,\sigma_d$. Con campo orizzontale di 90° su 848 pixel, $f = 424/\tan 45^\circ = 424$ px; con $b = 0{,}050$ m e $\sigma_d = 0{,}08$ px \cite{realsense-taratura-profondita}: $\sigma_z(2\,\text{m}) = 4 \cdot 0{,}08/21{,}2 = 0{,}0151$ m, $\sigma_z(3\,\text{m}) = 0{,}0340$ m, $\sigma_z(4\,\text{m}) = 0{,}0604$ m. *Livello di prova: verificato per calcolo, a partire da valori dichiarati dal costruttore; non verificato sperimentalmente.*

**Osservazione 2 (curva prudente).** Assumendo l'errore pari al limite dichiarato del 2 % a 2 m \cite{realsense-d400-accuratezza} e la legge quadratica: $\sigma_z(d) = 0{,}04\,(d/2)^2$ m, cioè 4 cm, 9 cm e 16 cm a 2, 3 e 4 m. Oltre 2 m è un'estrapolazione fuori dall'intervallo dichiarato. Per la base di 95 mm il limite dichiarato a 4 m è $0{,}02 \cdot 4 = 0{,}08$ m \cite{realsense-d455}. *Livello: verificato per calcolo.*

**Osservazione 3 (modello misurato da terzi).** Il modello assiale $\sigma_z(d) = 0{,}001063 + 0{,}0007278\,d + 0{,}003949\,d^2$ (metri, incidenza frontale) \cite{ahn2019} dà $\sigma_z(2\,\text{m}) = 0{,}0183$ m, fra la curva nominale (0,0151 m) e quella prudente (0,04 m). Vale fra 0,4 e 2,1 m su una parete bianca: a 3 m è un'estrapolazione. *Livello: verificato per calcolo su un modello misurato da terzi.*

**Osservazione 4 (soglie di porta).** Per un'innovazione $\nu$ gaussiana a due componenti, $\nu^\top S^{-1}\nu \sim \chi^2_2$ e $P(\nu^\top S^{-1}\nu > \gamma) = e^{-\gamma/2}$: $\gamma = -2\ln 0{,}01 = 9{,}21$ lascia fuori l'1 % delle misure corrette, $\gamma = -2\ln 10^{-4} = 18{,}42$ lo 0,01 %. *Livello: dimostrato nel modello lineare gaussiano.*

**Osservazione 5 (numerosità minime con zero insuccessi).** Con $N$ prove tutte riuscite, il limite inferiore esatto unilaterale al 95 % \cite{clopper1934} supera $p_0$ se $p_0^N < 0{,}05$: $0{,}95^{59} = 0{,}0485$ e $0{,}99^{299} = 0{,}0495$, quindi servono 59 prove per $p_0 = 0{,}95$ e 299 per $p_0 = 0{,}99$. *Livello: verificato per calcolo.*

**Osservazione 6 (parametri predefiniti di OctoMap).** Con probabilità di colpo 0,7 e di mancato colpo 0,4 e limiti 0,1192 e 0,971 \cite{octomap}, in logaritmo delle quote: $+0{,}847$, $-0{,}405$, $-2{,}00$, $+3{,}51$. Una cella al limite inferiore torna sopra 0,5 dopo tre colpi consecutivi ($-2{,}00 + 3 \cdot 0{,}847 = +0{,}54$; con due, $-0{,}31$). *Livello: verificato per calcolo.*

## 3. Limiti di validità dello stato dell'arte

Le cifre citate dei sensori sono dichiarazioni dei costruttori nelle loro condizioni di prova. In particolare la latenza di 95 ms a 30 fotogrammi al secondo riportata per una camera della stessa famiglia \cite{realsense-alta-velocita-d435} misura l'intero sistema di prova del costruttore (elaborazione grafica, schermo e trasporto USB compresi): è un limite superiore, non la latenza del sensore. I filtri di post-elaborazione del costruttore possono sostituire un pixel senza dato con un valore memorizzato o copiato da un vicino \cite{realsense-filtri-post}: la distinzione fra «osservato» e «non osservato» vale sul flusso non filtrato. I risultati di letteratura sulla previsione dei pedoni vengono da camere fisse dall'alto; quelli sulla previsione conforme valgono sotto scambiabilità fra taratura e prova. Le norme sulla distanza di separazione non sono state consultate nel testo originale: la forma della distanza di protezione è riportata da una fonte secondaria \cite{marvel2017}.
<!-- FINE PARTE I -->

---

# PARTE II — Provenienza e controlli (per il coordinatore; non entra nell'allegato)

## II.0 Cambi di stato e regole violate

- **Cambi di stato di fonti (solo sul dato che ho letto oggi, 14-11-2026, 18:00–18:04).** Da «verificata in parte» a **verificata per il dato indicato**: `kalman1960`, `kuhn1955`, `luiten2021`, `barber2019` (riassunti nelle risposte grezze di Crossref); `gibbs2021` (pagina degli atti NeurIPS, testo grezzo); `guibas1997` (riassunto della versione di rivista del 1999 su Crossref); `zhang2022` (pagina arXiv, letta con lo strumento che riassume: grado [r], più debole); `thor` (scheda Zenodo grezza: titolo, sei autori, licenza, descrizione, 48 file; i 100 Hz NON sono nella descrizione: restano letti solo dal file); `tum-rgbd` (pagina grezza: Kinect, 30 Hz, 640×480, cattura del moto a 100 Hz, **licenza CC BY 4.0 trovata** — nell'elenco era «non verificata»; la sequenza `fr3/walking_static` 24,83 s nella pagina di scaricamento; il fattore 5000 non è in queste due pagine). Da «aperta dal ruolo» a **verificata in parte**: `realsense-file-di-esempio` (vedi discordanza D1). `ahn2019`: i nomi per esteso dei cinque autori sono confermati da Crossref.
- **Restano «in parte»** (dati bibliografici riconfermati oggi su Crossref, contenuto non letto da me): `clopper1934`, `koch2007`, `wyffels2015`, `krejci2026`, `moras2011`, `hornung2013`, `nguyen2012`, `hetzel2024`.
- **Non riuscite:** registro arXiv (429 e poi tempo scaduto), due pagine Springer (rinvio a una pagina di autorizzazione), iso.org per ISO 13855 (403).
- **Regole.** Scritto solo in `f13-allegato/06-bibliografia`. Niente git, niente sudo. Nelle richieste solo DOI, identificativi e indirizzi pubblici. Il materiale scaricato è in `scaricati/`, separato dai programmi, mai eseguito. Scostamenti: (a) la parte I cita 19 chiavi che stanno in `RIFERIMENTI.md` ma **non** in `documentazione/riferimenti.bib` (schede, programmi, dati) e 4 chiavi nuove: stanno in `allegato.bib`; (b) alcune citazioni sono «nominali» (la fonte è citata per ciò che dice il titolo o il riassunto, non per una cifra): sono marcate N nella mappa; (c) `hornung2013` e `moras2011` hanno stato di testa «in parte» nell'elenco, ma la frase usata è stata trovata nel riassunto da un curatore oggi: le cito solo per quella frase; (d) la mappa completa è qui in parte II, perché porta gli stati di verifica.
- **Una regola dell'ambiente di esecuzione non seguita, per scelta:** l'ambiente chiede di non scrivere file di rapporto `.md`; la consegna chiede questo fascicolo come file, ed è l'ingresso del passo che compone i capitoli: ho seguito la consegna.
- **Lettura parziale dell'elenco.** Ho letto per intero il §0 e, delle 291 voci, titolo, sede e stato; i campi «Verifica», «Usata per» e «Note» li ho letti solo per le 108 candidate, e troncati (600, 230 e 230 caratteri): un dettaglio oltre il taglio può mancare.
- **Indipendenza.** Condivido con i curatori precedenti il modello linguistico e il ruolo; non i programmi (riscritti) né le conversazioni. La parte indipendente sono le risposte grezze dei registri.

## II.1 Previsioni (scritte alle 18:00:11 in `programmi/previsioni.txt`, prima dei controlli) ed esiti

| | Previsione | Esito |
|---|---|---|
| P1 | almeno 16 voci su circa 22 riaperte rispondono | **regge**: 19 voci su 20 hanno avuto risposta (23 DOI su 23 con codice 200; 5 pagine su 5; fallite arXiv, Springer, ISO) |
| P2 | Crossref conferma `kalman1960`, `kuhn1955`, `clopper1934` | **regge**: autore, rivista, volume, fascicolo, pagine, anno coincidono |
| P3 | `bibtex` con stile `plain`: 0 errori, 0 avvisi | **regge** al primo giro registrato: 90 voci nel `.bbl`, 0 avvisi, 0 errori; 3 giri di `pdflatex` senza errori (9 pagine) |
| P4 | i cinque DOI delle voci nuove risolvono | **regge**, con una riserva notata dopo: per il libro di Vovk e altri il registro non dà gli autori |
| P5 | fra 70 e 95 citabili su 108 candidate | **regge**: 86 |

## II.2 Conteggi

- Voci dell'elenco: 291. **Selezionate** (candidate, `programmi/candidate.txt`): **108**. **Citabili**: **86** (`programmi/citabili.txt`). **Escluse**: **22** (§II.4).
- **Voci nuove** in `allegato.bib`: **4** (`wilson1927`, `brown2001`, `barshalom2001`, `elfes1989`). Totale del file: **90** (34 article, 24 inproceedings, 19 misc, 12 manual, 1 book).
- **Riaperte oggi**: 20 voci dell'elenco (9 alzate a «verificata per il dato», 1 da «aperta dal ruolo» a «in parte», 1 completata nei nomi, 8 riconfermate solo nei dati bibliografici, 1 non raggiunta) più 6 DOI di voci nuove.
- Controllo di `allegato.bib` con `programmi/controlla_bib.py`: 90 voci, graffe 969/969, 0 chiavi doppie, 0 campi obbligatori mancanti, ogni voce ha DOI o arXiv o URL o ISBN, ogni pagina web ha la data di consultazione, 0 parole interne, 86 chiavi uguali a quelle dell'elenco.

## II.3 Mappa «affermazione → chiave» (solo voci citabili)

Stato: V = «verificata» nell'elenco per il dato; V* = alzata oggi da me; C = «dato diverso» nell'elenco, qui con la frase corretta; N = citazione nominale (dati bibliografici verificati, la frase regge sul titolo o sul riassunto; non usare per cifre); P = stato di testa «in parte», frase trovata nel riassunto.

**Sensori e schede**

| Chiave | Frase che la fonte sostiene | Stato |
|---|---|---|
| `realsense-d400-scheda` | proiettore a 850 nm, 360 mW massimi; imager senza filtro («All pass»). Base stereo e RMS: non ricontrollati, non citarli da qui | V |
| `realsense-d455` | campo 87° × 58°, intervallo ideale 0,6–6 m, otturatore globale, base 95 mm, errore «less than 2% at 4 m» | V |
| `realsense-confronto-camere` | D435i: 87° × 58°, 0,3–3 m (riserva: attribuzione delle colonne letta su testo estratto) | V |
| `realsense-d400-accuratezza` | D435/D435i: accuratezza ed errore RMS ≤ 2 % fino a 2 m, sull'80 % della regione, risoluzione HD; D455 fino a 4 m | V |
| `realsense-taratura-profondita` | «depth error scales as the square of the distance»; curva teorica con 0,08 px, campo 90°, 848 px, base 50 mm | V |
| `realsense-bkm-taratura` | camera ben tarata: errore RMS di sottopixel < 0,1; nessuna post-elaborazione predefinita nell'SDK | V |
| `realsense-alta-velocita-d435` | 95 ms a 30 fps (127 a 15, 47 a 60, 39 a 90): latenza dell'**intero sistema di prova**, limite superiore, non del sensore | C |
| `realsense-filtri-post` | filtro temporale con persistenza (predefinito «valido in 2 degli ultimi 4»); riempimento dei buchi che copia un vicino | V |
| `orbbec-gemini-330-scheda` | proiettore a 850 nm, imager «All-Pass» | V |
| `orbbec-gemini-335` | campo 90° × 65°, base 50 mm, intervallo ottimale 0,26–3 m, precisione spaziale ≤ 1,5 % a 2 m | V |
| `orbbec-femto-bolt` | tempo di volo: 120° × 120°, 0,25–2,88 m nel modo largo raggruppato (ambiente: pagina «Indoor», scheda «Indoor/Semi-Outdoor») | V |
| `st-um2884` | VL53L5CX: 4 × 4 da 1 a 60 Hz, 8 × 8 da 1 a 15 Hz (Tabella 2) | V |
| `st-vl53l5cx` | campo 45° × 45° (63° in diagonale), fino a 400 cm, fino a 60 Hz | V |
| `st-vl53l7cx` | campo 60° × 60°, fino a 350 cm; 4 × 4 a 30 Hz: 3,5 m al buio, 0,65 m a 5 klx; 8 × 8 a 15 Hz: 2,0 m e 0,5 m | V |
| `st-vl53l8cx` | campo 45° × 45°, 400 cm; a 5 klx 2,85 m (4 × 4) e 1,55 m (8 × 8) | V |
| `st-um3038` | il primo campione dopo «nessun bersaglio» ha stato 10, fiducia sotto il 50 % | V |
| `ldrobot-ld19` | 12 m, 4500 Hz, 10 Hz, risoluzione «≤ 1°», tenuta alla luce **30 klx** (non 60); lo 0,8° è derivato (360°/450) | C |
| `slamtec-rplidar-c1` | 12 m sul bianco, 6 m sul nero, 5 kHz, 10 Hz tipici, 0,72°, 40 klx | V |
| `librealsense` | marca temporale a metà esposizione calcolata dal dispositivo | V |

**Rumore, mappe**

| Chiave | Frase | Stato |
|---|---|---|
| `ahn2019` | σ_z = 0,001063 + 0,0007278·z + 0,003949·z² (+ termine angolare); parete bianca 0,4–2,1 m; rumore laterale 4,3 cm al bordo sinistro | V |
| `qiu2023` | l'uso all'aperto delle camere a tempo di volo resta limitato dall'interferenza solare (due camere) | V |
| `hornung2013` | «explicitly represents not only occupied space, but also free and unknown areas». NON citare per «mondo statico» | P |
| `octomap` | sconosciuto codificato in modo implicito; parametri 0,7 / 0,4 / 0,1192 / 0,971 nel sorgente | V |
| `duberg2020` | rappresentazione esplicita dei tre stati (riassunto). I «2 Hz a 2 mm» NON sono nell'articolo | C |
| `ufomap-deposito` | «real-time (2 Hz) at 2 mm voxel size» (README) | V |
| `oleynikova2017` | «runs in real-time on a single CPU core» | V |
| `millane2024` | fino a 177× nella ricostruzione della superficie, su GPU | V |
| `niessner2013` | fusione volumetrica a frequenze di tempo reale su hardware grafico comune | V |
| `nuss2018` | griglia dinamica con filtro a particelle in parallelo (dati laser e radar da veicolo) | V |
| `moras2011` | approccio «credibilist»: l'incertezza nasce da ignoranza ed errori (riassunto HAL) | P |
| `usenko2017` | griglia di occupazione in un buffer circolare 3D che si muove con il drone | V |
| `williams1978` | origine della mappa d'ombra in grafica (solo titolo; analogia) | N |

**Seguimento**

| Chiave | Frase | Stato |
|---|---|---|
| `bewley2016` | Kalman più algoritmo ungherese; 260 Hz per il solo tracciatore, dati i rilevamenti | V |
| `zhang2022` | associa quasi tutti i riquadri, anche a basso punteggio; 30 FPS su una GPU V100 | V* [r] |
| `cao2023` | senza misure l'errore del filtro si accumula durante l'occlusione; oltre 700 FPS su CPU dati i rilevamenti | V |
| `aharon2022` | compensazione del moto della camera e stato del filtro più accurato (riassunto) | V |
| `weng2020` | combinazione di filtro di Kalman 3D e algoritmo ungherese (citare IROS 2020) | V |
| `pang2021` | quattro parti, fra cui la gestione del ciclo di vita | V |
| `luiten2021` | HOTA bilancia rilevamento, associazione e localizzazione in una sola metrica | V* |
| `kalman1960` | equazione ricorsiva per la covarianza dell'errore di stima ottima; filtro lineare ottimo | V* |
| `kuhn1955` | metodo «ungherese» per il problema di assegnazione | V* |

**Previsione e statistica**

| Chiave | Frase | Stato |
|---|---|---|
| `scholler2020` | a 4,8 s, media di cinque scenari: velocità costante 0,39/0,83 m; RED 0,44/0,91; SR-LSTM 0,45/0,94; S-GAN 0,32/0,60 (migliore di 20) | V |
| `uhlemann2024` | la velocità costante approssima bene la dinamica nella maggior parte dei casi | V |
| `mercat2019` | veicoli (non pedoni): RMSE a 1–5 s del Kalman a velocità costante 0,75/1,81/3,16/4,80/6,70 m | V |
| `angelopoulos2021` | copertura marginale; condizione di scambiabilità | V |
| `lindemann2023` | taratura indipendente (basta la scambiabilità); 498 su 500 al 95 %, δ = 0,05, T = 20 (frasi nella prestampa arXiv v2). Il tipo di prova non è nel campo «Verifica»: non scritto | V |
| `dixit2022` | variante adattiva con osservazioni ritardate, in simulazione | V |
| `cleaveland2024` | regioni conformi su più passi non prudenti | V |
| `gibbs2021` | copertura sul lungo periodo senza scambiabilità, a prescindere dal processo che genera i dati | V* |
| `barber2019` | la copertura condizionata esatta è impossibile senza ipotesi sulla distribuzione (riassunto; enunciato del teorema non letto) | V* |
| `gneiting2007` | punteggi propri (punteggio d'energia, punteggio dell'intervallo) | V |
| `cheraghipouria2026` | la verosimiglianza negativa tende a distribuzioni troppo o troppo poco sicure | V |
| `kress2021` | valutazione per affidabilità, nitidezza, accuratezza; orizzonte 2,52 s | V |
| `gupta2018` | nome del metodo S-GAN (le cifre vengono da `scholler2020`) | N |
| `pellegrini2009`, `lerner2007` | fonti dei dati ETH e UCY secondo l'elenco dei riferimenti di `scholler2020` | N |
| `clopper1934` | limiti di confidenza esatti per la binomiale (titolo; testo non letto) | N |

**Occlusione**

| Chiave | Frase | Stato |
|---|---|---|
| `khurana2021` | occlusione come previsione a breve termine; +11,4 % e +5,0 % di F1 | V |
| `tokmakov2021` | «ground truth annotations for invisible objects» (che i dati siano sintetici non è nella frase verificata: non scritto) | V |
| `vanhoorick2023` | «a considerable performance gap» | V |
| `hsieh2023` | i metodi faticano sotto occlusione pesante (prestampa) | V |
| `scholl1999` | servono indizi di scomparsa e comparsa lungo contorni fissi ai bordi dell'occlusore | V |
| `koch2007`, `wyffels2015` | uso dell'informazione negativa nel seguimento (titolo) | N |
| `krejci2026` | seguimento consapevole dell'occlusione con probabilità di rilevamento attesa (titolo) | N |
| `orzechowski2018` | lo stato degli ostacoli nascosti è sovrastimato con intervalli | V |
| `koschi2021` | previsione insiemistica dei partecipanti rilevati e potenzialmente nascosti; IEEE T-IV 6(2):249–265, **2021** | C |
| `guibas1997` | evasore imprevedibile, di posizione ignota, arbitrariamente veloce (riassunto della versione di rivista del 1999, che è la voce nel `.bib`) | V* |
| `balch2019` | dati di qualità peggiore sembrano ridurre il rischio di collisione (principio; satelliti) | V |

**Sicurezza, ausili, dati**

| Chiave | Frase | Stato |
|---|---|---|
| `marvel2017` | forma lineare della distanza di protezione, v_H = 1,6 m/s (fonte secondaria sulla norma) | V |
| `therobotreport-veo` | volumi vuoti, occupati, sconosciuti; ciò che non è visto è trattato come occupato (fonte di parte) | V |
| `us-brevetto-11846916` | voxel occupati, non occupati, sconosciuti oltre un'occlusione (rivendicazione di brevetto) | V |
| `us-49cfr-236-205` | aspetto più restrittivo a relè diseccitato (copia non ufficiale; analogia) | V |
| `kayukawa2019` | estrapolazione lineare, soglie 5,0 s e 2,5 s, «six blind users», in un aeroporto. «Nessuna incertezza in uscita» è una lettura del progetto: non scritta | V |
| `xu2023` | 89 studi; efficacia e sicurezza prima preoccupazione | V |
| `romlay2021` | 70 articoli: 51,4 % simulazione, 24,3 % bendati, 22,9 % con disabilità visiva, 1,4 % in produzione | V |
| `dossantos2025` | RGB-D e aptico in uno zaino; dieci partecipanti bendati | V |
| `kozlov2026` | 93,75 % con 14 utenti con disabilità visiva; 92,9 % con 22 senza (non confondere) | V |
| `martinez2014` | per chi usa il bastone il **sonoro** dà un carico 22 volte maggiore dell'aptico; non nei bendati | C |
| `lupu2020` | otto partecipanti; stimoli aptici meno intuitivi di quelli sonori | C |
| `giudice2008` | suono spazializzato contro linguaggio spaziale con compito secondario (partecipanti bendati) | V |
| `thor` | traiettorie di persone al chiuso con verità di riferimento; CC BY 4.0; file `Exp_1_run_1`, `Exp_3_run_1` presenti. 100 Hz: non nella scheda | V* |
| `tum-rgbd` | Kinect, 30 Hz, 640 × 480, verità da cattura del moto a 100 Hz, CC BY 4.0; `fr3/walking_static` 24,83 s | V* |
| `depthtrack` | RealSense 415, 640 × 360, 30 fps, PNG a 16 bit; CC BY 4.0 | V |
| `princeton-tracking-benchmark` | profondità PNG a 16 bit; licenza non dichiarata | V |
| `realsense-file-di-esempio` | registrazioni non compresse e non filtrate, fatte con esemplari di pre-produzione; `stairs.bag` è di una D435 | in parte, alzata oggi |

Voci nuove: `wilson1927` (N: dati bibliografici su Crossref, testo non letto), `brown2001` (V*: nel riassunto «we recommend the Wilson interval or the equal-tailed Jeffreys prior interval for small n»), `barshalom2001` (N: titolo, autori, editore, ISBN su Crossref), `elfes1989` (N: titolo e dati su Crossref; nome di battesimo non nel registro, lasciato «A.»).

## II.4 Non citabili (22), con il motivo

| Chiave | Motivo |
|---|---|
| `iso-13855`, `iso-ts-15066`, `iso-10218-2`, `iec-60825-1`, `iso-3691-4` | norme a pagamento mai lette; iso.org ha risposto 403 anche oggi. Conseguenza: **C = 0,85 m e la «confluenza» nella 10218-2 non si citano**; la parte I rinvia a `marvel2017` e lo dice |
| `adamides2025` | l'affermazione non è nel riassunto; testo non raggiungibile |
| `nguyen2012` | solo dati bibliografici (riconfermati oggi, pp. 524–530); «assiale e laterale» non letto |
| `zhang2023` | solo dati bibliografici; non serve |
| `rossi2025` | dato diverso; prove fra 4 e 16 m all'aperto, fuori dall'intervallo dell'allegato |
| `hetzel2024` | cifre nel corpo, non rilette (oggi: capitolo LNCS, ECCV 2024 Workshops, pp. 135–152, 2025) |
| `klatzky2006` | contenuto non letto; l'affermazione regge su `giudice2008` |
| `luiten-trackeval`, `rlabbe-filterpy`, `bonxai`, `openvdb`, `rosbags` | programmi: non sostengono un'affermazione tecnica dell'allegato (`rosbags` è anche solo «aperta dal ruolo») |
| `thor-magni`, `bonn-rgbd-dynamic`, `drow`, `frog`, `friburgo-rgbd-people`, `zenodo-tof-vl53l5cx` | insiemi esaminati e non usati nelle elaborazioni |

Proposte nuove **non** messe nel `.bib`: Vovk, Gammerman, Shafer, *Algorithmic Learning in a Random World*, Springer 2005, DOI 10.1007/b106715 (il DOI risolve al titolo; gli autori non sono nel registro e la pagina Springer non si è aperta: **non verificata**); Bernardin e Stiefelhagen, metriche CLEAR MOT, EURASIP JIVP 2008, DOI 10.1155/2008/246309 (dati bibliografici verificati; serve solo se l'allegato usa MOTA).

## II.5 Provenienza delle cifre della parte I e ricalcoli (`programmi/ricalcoli.py`)

| Parte I | File d'origine | Mio ricalcolo |
|---|---|---|
| Oss. 1: 1,5 / 3,4 / 6,0 cm | `f4/H-012/05-correzioni/SOLUZIONE_V2.md` (B1); elenco, voce `realsense-taratura-profondita` | **torna**: 0,0151 / 0,0340 / 0,0604 m |
| Oss. 2: 4 / 9 / 16 cm; 8 cm a 4 m | `f3/H-012/02-validazione/VERIFICA.md` §4; `f2/04-torneo/TORNEO.md` | **torna** |
| Oss. 3: 1,83 cm a 2 m | `f10-dati/02-sensori/MODELLO_SENSORE.md` righe 18 e 90 | **torna**: 0,01831 m |
| Oss. 4: 9,21 e 18,42 | elenco, voce `kalman1960` (nota); `SOLUZIONE_V2.md` | **torna**: 9,2103 e 18,4207 |
| Oss. 5: 59 e 299 | `f3/H-012/03-metrologo/PIANO_MISURE.md` parte 1 | **torna**: 0,04849 e 0,04954 (con 58 e 298: 0,0510 e 0,0500, non bastano) |
| Oss. 6: tre colpi | `f7-estensione/01-matematico/CONSEGNA.md` | **torna**: +0,542 dopo tre, −0,305 dopo due |
| cifre di letteratura (0,39/0,83; 498/500; 22,9 %; 260 Hz; 95 ms; …) | campi «Verifica» di `documentazione/RIFERIMENTI.md` | copiate dal campo «Verifica», non dai file che citano; non rilette oggi salvo le voci di §II.0 |

## II.6 Discordanze

- **D1, file di esempio.** La pagina `doc/sample-data.md` letta oggi (2751 caratteri) elenca `outdoors.bag` (D415), `stairs.bag` (D435), `depth_under_water.bag`, `d435i_sample_data.zip`; **non** contiene `D435i_Depth_and_IMU_Stands_still.bag` né `structured.bag`, che l'elenco le attribuisce (stanno sotto un altro indirizzo dello stesso servizio). La pagina avverte che i file sono fatti con **hardware di pre-produzione** e «are not official marketing material»: va detto dove si usano come dati di stereo attivo.
- **D2.** `documentazione/riferimenti.bib` non contiene 19 delle chiavi citabili (ha solo 13 schede): la consegna dei capitoli («chiavi di riferimenti.bib») va letta come «chiavi dell'elenco»; il file da usare è `allegato.bib`.
- **D3.** `guibas1997`: nel `.bib` d'origine è il contributo del 1997 (convegno e volume non letti); in `allegato.bib` la voce, con la stessa chiave, è la versione di rivista del 1999, l'unica di cui ho letto il riassunto. `barber2019` e `gibbs2021` portano ora la sede a stampa (2021) con la chiave vecchia.
- **D4.** `barshalom2001`: Crossref dà la data in rete 4-1-2002; l'anno 2001 dell'edizione a stampa è a memoria (ISBN 9780471416555 nel registro). Da ricontrollare sul frontespizio.
- **D5.** OctoMap: l'articolo dice che lo sconosciuto è rappresentato «explicitly», il sito che è «implicitly encoded». Non è una contraddizione (lo sconosciuto è l'assenza di un nodo), ma la parte I le tiene distinte.
- **D7.** Due frasi della parte I poggiano sul campo «Note» dell'elenco e non sul campo «Verifica»: «camere fisse dall'alto» per i dati ETH e UCY (`scholler2020`) e la somma dei termini della distanza di protezione (`marvel2017`: la formula non è stata ricontrollata simbolo per simbolo). L'intervallo 0,4–2,1 m di `ahn2019` l'ho riscontrato oggi nella copia dell'articolo salvata nel progetto (riga 216: «0.4 m to 2.1 m», bersaglio piano bianco, angoli da 0° a 75°).
- **D8.** La chiave `slamtec-rplidar-c1` contiene «c1», che somiglia a una sigla interna: è la chiave dell'elenco (il nome del prodotto), lasciata com'è; un controllo automatico sulle sigle deve escludere le chiavi dentro \cite.
- **D6.** Lo stato «verificata» dell'elenco non è uniforme (riassunto, strumento che riassume, testo intero): per `zhang2022`, `aharon2022`, `us-brevetto-11846916`, `giudice2008`, `us-49cfr-236-205` la lettura è passata dallo strumento che riassume.

## II.7 Che cosa può cambiare con l'integrazione in corso; che cosa manca

- Se la soluzione finale cambia sensore (base, campo, risoluzione), l'Osservazione 1 va rifatta con i nuovi $f$ e $b$; se cambia le soglie di porta o le numerosità, le Osservazioni 4 e 5. Se usa altri insiemi di dati o programmi, servono voci nuove; se rinuncia ai file di esempio del costruttore, `realsense-file-di-esempio` esce.
- Manca: la lettura delle norme (ISO 13855, ISO/TS 15066, IEC 61496 — quest'ultima non è citata in nessun file del progetto e non ha una voce); il testo di `clopper1934`, `wilson1927`, `koch2007`, `wyffels2015`; la frequenza di THÖR da una fonte scritta; il fattore di scala 5000 di TUM dalla pagina dei formati; i numeri di pagina di `gibbs2021`.
- Proposta `fonti-13-1`: nei capitoli, ogni \cite marcata N in questa mappa regga solo una frase di attribuzione, mai una cifra. Previsione: una ricerca delle \cite accanto a un numero trova 0 chiavi N; la smentisce un solo caso.

## II.8 Come rifare

`bash programmi/rifai.sh` (senza rete: rilegge l'elenco, rigenera `allegato.bib`, lo controlla, lancia `bibtex`, rifà i conti, controlla le parole vietate e le citazioni della parte I); `bash programmi/rifai.sh --rete` riapre anche i registri (`programmi/scarica.sh`, esiti in `scaricati/esito_richieste.tsv`).
