# Addendum dell'utente al contratto (ricevuto durante f3, il 14 novembre 2026)

Il `CONTRATTO.md` non si tocca (è legato al cancello f0). Questo file registra, per intero, un'indicazione arrivata dall'utente a convocazione in corso.

## Il messaggio dell'utente, per intero

«la società mare group, che ha proposto la sfida, è specializzata nella areospace e difesa, nello specifico hanno avuto un contratto per veicoli uncrewed a ottobre 2026. Specializza il sistema attuale, nel momento in cui ha avuto l'approvazione dello sciame, per i sistemi uncrewed, lasciando aperte le possibilità per ulteriori sviluppi futuri.»

## Come lo legge il coordinatore

- **Ordine:** prima si chiude la validazione del sistema attuale (rami f3, f4, f5: il nucleo provato a sensore fermo). Solo dopo l'approvazione dello sciame il sistema si specializza.
- **Che cosa decide:** scioglie in parte la decisione 1 della selezione (K-008, applicazione): fra le due applicazioni ammesse dalla challenge si sceglie «osservazione e ispezione nei settori Aerospace & Industry», declinata sui sistemi uncrewed (veicoli senza equipaggio: aerei, terrestri, di superficie). L'applicazione assistiva resta uno sviluppo possibile, non il bersaglio.
- **Vincoli della specializzazione:** il nucleo approvato (stati osservato / previsto / perso, i due strati durante l'occlusione, gli invarianti) non si cambia senza prova; ciò che la specializzazione aggiunge e che non è provato si dichiara «non verificato». Gli sviluppi futuri restano aperti: l'architettura deve dire dove si innestano (altri sensori, altre piattaforme, più veicoli, l'applicazione assistiva).
- **Ambito:** percezione per osservazione, ispezione, consapevolezza della scena e navigazione sicura (rilevare ed evitare). Niente funzioni d'ingaggio o di puntamento: non sono nella challenge e restano fuori.
- **Non verificato:** i dati sulla società e sul contratto sono riferiti dall'utente; vanno controllati in rete su fonti pubbliche prima di finire nel documento, oppure riportati come «riferito dall'utente».

---

# Secondo addendum dell'utente (ricevuto durante f4, il 14 novembre 2026)

## Il messaggio dell'utente, per intero

«non appena possibile rendi chiaro per lo sciame che i due principali ambiti di applicazione sono veicoli uncrewed e non vedenti (ambito medico). Con possibilità di applicazione su entrambi gli ambiti e con focus particolare di use case nel primo. Il sistema deve essere adattabile e la presentazione diretta ad una giuria mista, che include sia membri di mare group (che hanno contesto completo) che esterni e che quindi devono poterne apprezzare la validità anche senza avere accesso a tutte le informazioni.»

## Come lo legge il coordinatore (sostituisce, dove differisce, la lettura del primo addendum)

- **Due ambiti, non uno.** (1) Veicoli e sistemi uncrewed: è il **caso d'uso principale**, quello su cui si costruisce la demo e il racconto. (2) Ausilio all'orientamento di persone non vedenti (ambito medico-assistivo): è il **secondo ambito**, da mostrare come applicazione dello stesso sistema, non come sviluppo remoto. Sono le due applicazioni che la challenge stessa ammette.
- **Un nucleo, due profili.** Il sistema deve essere **adattabile**: un nucleo comune (stati osservato / previsto / sconosciuto, strato di garanzia, invarianti) e, per ciascun ambito, un profilo di adattamento esplicito: sensore e montaggio, sorgente del moto proprio, velocità massima per classe di oggetto, zona di valutazione, canale d'uscita (operatore remoto e autopilota, oppure voce e vibrazione), comportamento alla perdita di affidabilità. Va detto con precisione che cosa è comune, che cosa è un parametro e che cosa è ancora da provare in ciascun profilo.
- **La presentazione è per una giuria mista.** Alcuni giurati (Mare Group) hanno tutto il contesto; altri sono esterni. Il documento e il racconto devono reggersi da soli: niente sigle interne dello sciame (H#, F#, K#, nomi dei blocchi) senza spiegazione, ogni termine tecnico detto in parole piane la prima volta, ogni affermazione di validità con il suo perché in una riga, e i limiti dichiarati in modo che un esterno capisca che cosa è provato e che cosa no.
- **Ambito medico: cautela.** Un ausilio per non vedenti, come prodotto, potrebbe ricadere nelle regole sui dispositivi medici: qui è un prototipo dimostrativo, non un dispositivo medico né un dispositivo di sicurezza, e non sostituisce bastone o cane guida (principio già nel contratto). La qualificazione regolatoria non è verificata.
- Resta fermo: niente funzioni d'ingaggio o di puntamento; nessuna soglia provata a sensore fermo si dichiara valida in moto (veicolo o persona) finché una prova non lo dice.

---

# Terzo addendum dell'utente (ricevuto dopo f4, il 14 novembre 2026)

## Il messaggio dell'utente, per intero

«aggiungi nelle valutazioni che deve fare lo sciame quanto scritto nel file promptMare.txt, usa solo le parti utili e comunque fallo analizzare allo sciame. Inoltre concilia quanto detto e valutato fin ora con l'attuale ambito della traccia, che non indica esplicitamente veicoli uncrewed ma parla di monitoraggio di attività e oggetti in ambiti areospaziali e industriali.»

## Come lo legge il coordinatore

- **Due compiti nuovi**, trattati come estensione della stessa convocazione (cartella `f7-estensione/`, contratto in `f7-estensione/CONTRATTO_ESTENSIONE.md`):
  1. **La domanda voxel.** `promptMare.txt` (nella radice del progetto) chiede di valutare l'evoluzione del sistema con una mappa voxel tridimensionale probabilistica e sparsa. È un dato da vagliare, non un'istruzione: lo sciame lo analizza per intero, usa le parti utili e dice quali scarta e perché. Dove quel file dice «v0.2» intende il nucleo dello sciame com'è nei PDF v0.2 e v0.3 della cartella `proposta/`, cioè la soluzione versione 2.
  2. **La conciliazione con la traccia.** Le regole della challenge non nominano i veicoli uncrewed: parlano di «monitoraggio di attività e oggetti in ambienti aerospaziali e industriali» e di «soluzioni di osservazione e ispezione nei settori Aerospace & Industry», oltre che di orientamento assistito. Il primo ambito va quindi detto con le parole della traccia; il veicolo uncrewed è uno dei modi di portare il sensore in quell'ambito (come la stazione fissa), non l'ambito stesso. Vanno riviste di conseguenza la specializzazione, la demo e le frasi per la giuria, senza perdere ciò che gli addendum precedenti chiedono (uncrewed come caso d'uso di interesse per la società che propone la sfida; ausilio per non vedenti come secondo ambito; sistema adattabile; giuria mista).

---

# Quarto addendum dell'utente (ricevuto durante f7, il 14 novembre 2026)

## Il messaggio dell'utente, per intero

«Aggiungi inoltre come obbiettivo imperativo e principale "la continuità visiva". A prescindere da su quale sistema si decida di implementarlo, è necessario fornire predizioni efficaci con una valutazione realistica della precisione della predizione, che consenta di effettuare una visualizzazione continua del movimento sotto una certa incertezza controllata. Integra questo imperativo e valuta se rispettato correttamente in tutte le parti, e nel caso non lo sia effettua, con lo sciame, opportune modifiche per adattarlo di conseguenza.»

## Come lo legge il coordinatore

- **Diventa l'obiettivo principale.** La «continuità visiva» passa da uno degli otto requisiti (R3, «gestire le interruzioni della visibilità») a obiettivo imperativo: il movimento di ogni oggetto seguito deve restare visualizzabile senza interruzioni anche quando l'oggetto non è osservato, con una previsione efficace e con una valutazione realistica della sua precisione, in modo che l'incertezza mostrata sia controllata (dichiarata, tarata sui fatti, limitata).
- **Vale per qualunque sistema** su cui il nucleo venga portato: stazione fissa, piattaforma uncrewed, ausilio per persone non vedenti.
- **Il sospetto da verificare.** Il nucleo approvato (soluzione versione 2) mostra un'area prevista per circa mezzo secondo e poi dichiara «perso», lasciando solo l'avviso di «possibile presenza» sull'ombra: il verdetto dell'arbitro scrive che «l'area prevista alla riemersione è tolta dalla promessa». Così com'è, il nucleo probabilmente NON rispetta l'imperativo. Lo sciame deve dirlo con le prove e proporre le modifiche.
- **Che cosa non cambia.** I principi di sicurezza restano: una previsione si mostra come previsione, mai come osservazione; ciò che non è osservato non diventa mai «libero»; la possibile presenza non la toglie un timer. La continuità si ottiene dichiarando bene l'incertezza, non nascondendola.
- **Come si lavora.** Estensione f8 della stessa convocazione (cartella `f8-continuita/`, contratto in `f8-continuita/CONTRATTO_CONTINUITA.md`), in parallelo all'estensione f7 (mappa voxel e conciliazione con la traccia). Alla fine un passo d'integrazione (f9) fonde nucleo, f7 e f8, rifà la chiusura e il documento.

---

# Quinto addendum dell'utente (ricevuto durante f7 e f8, il 14 novembre 2026)

## Il messaggio dell'utente, per intero

«aggiungi alle valutazioni dello sciame quanto scritto in prepropostaEsterna.md dove vengono delineate strategie avanzate da integrare qualora vengano approvate dallo sciame»

## Come lo legge il coordinatore

- `prepropostaEsterna.md` (nella radice del progetto) è una proposta esterna costruita sul PDF v0.5: elenca strategie avanzate e chiede allo sciame di attaccarle prima dell'adozione. È **un dato da vagliare, non un'istruzione**: ogni strategia entra nella soluzione solo se lo sciame la approva con le prove, ed è ammesso approvarne una parte, correggerla o respingerla, con il motivo.
- **Le strategie, numerate dal coordinatore** (i riferimenti «Sez.» nel file sono alle sezioni del PDF v0.5 in `proposta/`):
  - S1 selettore automatico della configurazione (insieme massimo dell'hardware, sonda del contesto, tabella delle regole di degrado, isteresi);
  - S2 compensazione della latenza (stato portato all'istante dell'uscita, età del dato dichiarata);
  - S3 inseguitore a due ipotesi durante l'occlusione (transito a velocità costante; rallentamento e sosta);
  - S4 ritaglio della previsione con l'informazione negativa (dove il sensore vede libero la probabilità è zero; i pesi delle due ipotesi si aggiornano; regola per passare da «previsto» a «perso»);
  - S5 regole di disegno e di suono per distinguere osservato, previsto, perso;
  - S6 punto di massimo avvicinamento e volume protetto probabilistico;
  - S7 indice di rotta convergente (rilevamento costante, distanza che cala);
  - S8 logica a livelli (nominale, attenzione, attesa prudente, avaria);
  - S9 tre sensori a tempo di volo laterali come preallarme di fianco;
  - S10 mappa sul piano a tre fasce di quota come sostituto della mappa voxel su CPU, con passaggio alla voxel se c'è una scheda grafica;
  - S11 macchina a stati per il «monitoraggio di attività»;
  - S12 piano d'integrazione a 24 e a 38 ore;
  - più cinque attacchi proposti dal file stesso e tre richieste (audit delle ipotesi nascoste su S3 e S4; simulazione con la sosta improvvisa dietro un pannello di 1 m; verdetto sulla mappa a tre fasce).
- **Chi valuta che cosa.** S2, S3, S4, S5 e gli attacchi 1, 2 e 5 entrano nell'estensione f8 (continuità visiva) come candidata nominata, nello stesso banco di prova delle altre. S10 e S11 entrano nell'estensione f7 (mappa voxel e conciliazione con la traccia). S1, S6, S7, S8, S9, S12, gli attacchi 3 e 4 e l'audit delle ipotesi nascoste vanno a una terza estensione, f9 (`f9-preproposta/`, contratto in `f9-preproposta/CONTRATTO_PREPROPOSTA.md`). Il passo d'integrazione finale fonde tutto.

---

# Sesto addendum dell'utente (ricevuto durante f7, f8 e f9, il 14 novembre 2026)

## Il messaggio dell'utente, per intero

«come imperativo per lo sciame è la deadline: l'intero progetto e valutazione preliminare deve concludersi in 14 ore, per poi passare al raffinamento e la conclusione finale nelle 4 ore successive.»

## Come lo legge il coordinatore

- **È un vincolo imperativo, e sostituisce l'ipotesi non verificata del contratto** («24–48 ore»): la squadra ha **14 ore di orologio** per costruire il prototipo e farne la valutazione preliminare (le prime prove sull'hardware), poi **4 ore** per il raffinamento e la conclusione finale (correzioni, demo, presentazione). In tutto 18 ore.
- **Che cosa cambia.** Il nucleo da solo era stimato dallo sciame in circa 54 ore-persona, di cui 38 in fila: in 14 ore non ci sta senza tagli e senza lavoro in parallelo. Ogni scelta delle estensioni in corso (mappa in tre dimensioni o a fasce, previsione continua, strategie della preproposta esterna) va quindi pesata anche sulle ore: a parità di prove vince la più semplice da costruire, e per ogni componente si dice se è **indispensabile nelle 14 ore**, se va **nelle 4 ore di raffinamento**, o se è **dopo l'hackathon**.
- **Che cosa non cambia.** I due obiettivi non negoziabili restano la continuità visiva (obiettivo principale) e la sicurezza delle indicazioni; il taglio si fa sul resto.
- **Ancora da confermare con l'utente:** quante persone lavorano (lo sciame pianifica per 3, 4 e 5) e quale sensore la squadra possiede.
- Il lavoro dello sciame sta comunque ben dentro questi tempi: la convocazione è cominciata alle 13:01 del 14 novembre 2026.

---

# Settimo addendum dell'utente (ricevuto durante f7, f8 e f9, il 14 novembre 2026)

## Il messaggio dell'utente, per intero

«Inoltre mano a mano che le proposte e le informazioni vengono validate, inserite nel progetto, rimosse o cambiate valuta se fare commit sul repository locale e procedi con il farle. Nel progetto siamo in 5, non abbiamo sensori al momento ma posseggo alcuni sensori a casa che posso fornire da remoto tra 5-6 ore. Non so tuttavia se sono utili per lo scopo. Farò più tardi un inventario e te lo invierò ma tu procedi usando simulazioni senza sensori veri basate sul materiale disponibile online e i datasheet pubblici. Usa anche hardware simulato e/o dataset pubblici sui rilevamenti di sensori diversi e altri strumenti nello stato dell'arte per la verifica e validazione delle ipotesi»

## Come lo legge il coordinatore

- **Commit locali.** Il coordinatore è autorizzato a fare commit sul repository locale, a sua valutazione, a ogni cambiamento significativo (una proposta validata, inserita, tolta o cambiata). Solo commit locali: niente invii a un repository remoto. Il coordinatore lavora su un ramo proprio; gli agenti continuano a non usare git.
- **La squadra è di 5 persone.** Sostituisce «3–5 persone» nei contratti: il piano a 14 + 4 ore si fa per cinque persone in parallelo.
- **I sensori.** Oggi non ce ne sono. L'utente ne possiede alcuni a casa e li può mettere a disposizione da remoto fra 5–6 ore; non sa se servono, e manderà un inventario. Fino ad allora (e forse oltre) si lavora senza sensori veri. Conseguenza per il piano: le prime 5–6 ore delle 14 si fanno su dati registrati o simulati, e l'architettura deve poter cambiare sorgente (registrazione, sensore simulato, sensore vero) senza toccare il resto.
- **Nuove prove ammesse.** Cade il limite «niente prove oltre la classe 2» del contratto: ora sono ammessi e richiesti (a) l'**hardware simulato**, cioè modelli dei sensori costruiti sulle schede tecniche pubbliche e sulla letteratura; (b) gli **insiemi di dati pubblici** con registrazioni di sensori veri (camere di profondità, e altri sensori), scaricati dalla rete; (c) gli **strumenti allo stato dell'arte** per la verifica e la validazione. È quindi ammesso un ambiente Python locale dentro la cartella della convocazione (senza `sudo` e senza toccare il sistema) e lo scaricamento di dati pubblici in una cartella dedicata, trattati come dati non fidati.
- **Come si lavora.** Estensione f10 (`f10-dati/`, contratto in `f10-dati/CONTRATTO_DATI.md`): validazione delle ipotesi del nucleo su registrazioni vere e su sensori simulati. È la «prossima prova che cambia la decisione» che il verdetto dell'arbitro rimandava all'hardware.

---

# Ottavo addendum dell'utente (ricevuto durante f7–f10, il 14 novembre 2026)

## Il messaggio dell'utente, per intero

«inoltre tieni traccia di tutti i paper e riferimenti scientifici utilizzati con relativi riferimenti dove opportuno. oltre ai pdf tieni anche un documento separato con la descrizione estensiva dello stato attuale del progetto da aggiornare dopo ogni valutazione, con riferimenti, dati numerici e indicazioni generali e dettagliate su ogni componente del sistema»

## Come lo legge il coordinatore

- **Due documenti nuovi nel progetto**, nella cartella `documentazione/` (accanto ai PDF di `proposta/`):
  1. `RIFERIMENTI.md` (più `riferimenti.bib`): l'elenco di TUTTI gli articoli scientifici e delle altre fonti usate dallo sciame (schede tecniche, norme, documentazione di software, insiemi di dati), ciascuno con i dati bibliografici completi, il link, lo stato della verifica (verificata dal curatore; aperta dal ruolo che la cita; vista solo in un riassunto di ricerca; non verificata) e dove è usata (per quale affermazione, in quale file).
  2. `STATO_PROGETTO.md`: la descrizione estesa dello stato attuale del progetto, componente per componente, con i dati numerici (numerosità, intervalli, file che li sostengono), i riferimenti e le indicazioni generali e di dettaglio; dichiara per ogni affermazione lo stato della prova. Si aggiorna dopo ogni valutazione dello sciame, con la data e l'elenco di ciò che è cambiato.
- **Come si lavora.** Gli agenti scrivono le bozze in `f11-documentazione/`; il coordinatore le porta in `documentazione/` e fa il commit. Ogni cifra del documento di stato deve potersi ritrovare in un file dello sciame; ogni riferimento citato deve stare nell'elenco.

---

# Addendum 9 (14-11-2026, dopo il verdetto sui dati): l'allegato tecnico per la commissione esterna

Testo dell'utente, per intero:

«genera anche un secondo documento estratto dallo stato del progetto e dalle verifiche, dimostrazioni matematiche e calcoli effettuati che includa anche citazioni e riferimenti bibliografici, per descrivere tutta la parte tecnica relativa al progetto senza i riferimenti allo stato di lavoro e alla suddivisione interna. Deve essere quello da allegare alla versione finale per la valutazione dalla commissione esterna.»

## Come lo legge il coordinatore

- **Un documento nuovo**, `allegato_tecnico/allegato_tecnico.pdf` (con il sorgente LaTeX e il file della bibliografia accanto): la relazione tecnica del progetto, da allegare al documento di due pagine nella versione finale. Lettore: una commissione esterna che valuta nel merito.
- **Che cosa contiene:** il problema e i requisiti in forma misurabile; il sensore e la geometria d'osservazione; la rappresentazione dello spazio; rilevamento, associazione e stima dello stato; la gestione dell'occlusione e la previsione con la sua precisione; il metodo di valutazione; i risultati con numerosità e intervalli; il costo di calcolo; le alternative considerate e perché escluse; le condizioni di validità e i limiti. Con le dimostrazioni e i calcoli per esteso (in appendice quelli lunghi) e con le citazioni bibliografiche in forma accademica.
- **Che cosa NON contiene:** lo stato dei lavori («in corso», «in correzione», versioni), il piano e le ore, la suddivisione interna (sciame, fasi, ruoli, sigle interne H#, K#, F#, percorsi dei file di lavoro), la cronaca. Resta invece, perché è contenuto tecnico e non stato dei lavori, il livello di prova di ogni risultato (dimostrato in un modello dichiarato; verificato in simulazione, con numerosità e intervallo; misurato su dati pubblici; non verificato sperimentalmente) e l'elenco dei limiti: la commissione deve poter distinguere ciò che è dimostrato da ciò che è solo simulato.
- **Come si lavora.** Estensione f13: prima i fascicoli tecnici (dimostrazioni, calcoli, stima, statistica, costo, bibliografia), ciascuno ricalcolato da chi lo scrive; poi, quando la soluzione versione 3 e il verdetto d'integrazione sono chiusi, la stesura dei capitoli, la verifica avversaria (dimostrazioni, cifre, citazioni, assenza di riferimenti interni), la lettura da commissario esterno e la versione finale. Ogni cifra dell'allegato deve stare in un file dello sciame; ogni citazione deve stare nell'elenco dei riferimenti con stato «verificata» per ciò che le si fa dire.

---

# Addendum 10 (14-11-2026, durante la correzione della soluzione versione 3): la classificazione come componente fondamentale e il profilo di chi porta il sensore

Testo dell'utente, per intero:

«introduci una componente fondamentale nella classificazione: ci sarà un modello che si occuperà della classificazione (anche se solo simulato ora come ora, dato che nei tempi richiesti non era fattibile ne ragionevole chiederlo) e che non si occuperà solo di assegnare etichette persona/non persona, ma che identificherà vari tipi di veicoli e altri ostacoli in movimento, come aerei, auto, treni, ecc... Al momento limitatamente a questo progetto e al modo in cui verrà presentato le labels verranno assegnate manualmente nei test e verrà esplicitato che è richiesto un classificatore su classi e tipologie diverse con consapevolezza anche di velocità e gradi di libertà. Inoltre deve tenere presente anche delle capacità del veicolo (nel caso specifico analizzato uncrewed) o della persona che utilizza il sistema, includendo anche per esso stime sulla velocità, tempi di reazione, accelerazione e gradi di libertà (per l'oggetto o soggetto su cui è montato non c'è bisogno di classificazione ma solo di una configurazione iniziale deterministica). Aggiorna lo stato e informa lo sciame di questa specifica, con una breve valutazione e inclusione di questo requirement.»

## Come lo legge il coordinatore

- **Requisito nuovo, da includere (non da ridiscutere):** il sistema ha un componente di **classificazione** degli oggetti seguiti su più classi e tipologie (persona; veicoli di tipo diverso, per esempio auto, mezzi di piazzale, treni, aerei; altri ostacoli in movimento), non più la sola etichetta persona / non persona. Ogni classe porta un **profilo cinematico**: velocità tipica e massima, accelerazione, gradi di libertà (come può muoversi: in ogni direzione, lungo una traiettoria vincolata, con un raggio di sterzata minimo).
- **Stato dichiarato del classificatore:** in questo progetto e nella presentazione il modello è **simulato**; nelle prove le etichette sono **assegnate a mano**. Va scritto in modo esplicito che il sistema *richiede* un classificatore su classi e tipologie diverse, consapevole di velocità e gradi di libertà, e che qui non è realizzato né valutato.
- **Profilo di chi porta il sensore** (il veicolo senza equipaggio, nel caso analizzato; oppure la persona che usa il sistema): nessuna classificazione, ma una **configurazione iniziale deterministica** con velocità, tempi di reazione, accelerazione (frenata) e gradi di libertà. Serve a decidere quanto presto un avviso è utile.
- **Che cosa deve valutare lo sciame, in breve:** dove la classe e il profilo entrano nella catena (velocità massima per la fascia di guardia e per l'insieme di possibile presenza; modello di moto e regione di previsione; soglie d'avviso in funzione del profilo di chi porta il sensore); che cosa succede alla sicurezza con un'etichetta sbagliata o assente; che cosa del dominio provato (camera ferma, fino a 3 m) regge per classi veloci; come dichiararlo senza promettere ciò che non c'è.
- **Nota di coerenza con ciò che lo sciame aveva stabilito:** «nessuna rete decide un'indicazione» e «l'etichetta sta a lato» vanno riconciliate con questo requisito, non cancellate in silenzio: la regola di sicurezza («ciò che non è osservato non è mai libero»; l'avviso si toglie solo guardando) non può dipendere da un'etichetta. Massa e accelerazione restano non stimabili dalle misure: con le classi entrano come **valori a priori della classe**, non come stime.
- Resta il vincolo: solo osservazione, monitoraggio, ispezione, navigazione sicura e avviso.

---

# Addendum 11 (14-11-2026, sera): seconda fase — veicoli veloci, prototipo simulato, video

Indicazioni dell'utente (riassunte dai suoi tre messaggi, che restano nella conversazione):

- **Autori:** Ignazio Crocchiolo, Federico Dellini, Danilo Amalfitano, Emanuele Ciotola, Pierfrancesco Amendola. **Gruppo: SDMs. Progetto: MoVi.** Le 71 pagine dell'allegato vanno bene.
- **Decisioni chiuse:** il classificatore è da supporre esistente e lasciato ai lavori futuri; qui è solo simulato, con etichette a mano. L'avviso resta acceso e solo lo sguardo lo toglie. Nessun sensore vero: inventario vuoto. L'archivio di Friburgo si ignora.
- **Seconda fase di test, più rapida:** sensori più performanti, anche di altissima tecnologia, o del tutto diversi, per e su auto, treni e aerei, che permettano rilevamenti a velocità e distanze adeguate; sempre con hardware simulato dalle schede e dati pubblici (auto, treni, aerei, droni e altri mezzi volanti senza pilota). Dove i dati pubblici mancano: simulazione dalle schede, dichiarata.
- **Il caso centrale diventa quello dei veicoli veloci, in particolare aerei e droni:** cambia l'impianto della presentazione e del video.
- **Prototipo:** lo produce lo sciame, simulato, senza hardware, riusando tutto il codice scritto finora; usa i segnali dell'hardware virtuale, i dati pubblici, le schede dei sensori e i risultati delle prove; simula più condizioni e il sistema proposto, multisensore; può servire al video.
- **Video:** poco meno di 3 minuti, 16:9 a 1080p, motion graphics; strumento a scelta dello specialista fra HyperFrames (installato), Remotion e Motion Canvas; prima versione con voce sintetica di qualità in inglese, con la possibilità di generare dopo un'alternativa in italiano; musica con licenza libera; logo del gruppo creato dallo sciame; niente slide. Linee guida nel file dell'utente `…/uploads/…/2f4fda74-Markdownlfes.md` (copiato in `f17-video/ISTRUZIONI_VIDEO_UTENTE.md`), da applicare dopo una passata convergente dello sciame con tre nuovi specialisti (pubblicità e marketing, videomaker, comunicazione), adattandole al nuovo caso centrale.
- **Tempo:** tutto entro 10 ore d'orologio. Workflow con più agenti in parallelo autorizzati.
- **Regolamento:** controllato dal coordinatore. Non ho trovato il testo dell'edizione 2026; quello dell'edizione speciale 2025 (stessi organizzatori) non ha regole sull'uso di strumenti automatici, chiede che il progetto sia originale e non violi diritti di terzi, e fissa per il video pitch un massimo di 4 minuti, pena l'esclusione.

---

# Addendum 12 (15-11-2026): eventi improvvisi e visibilità degradata

Testo dell'utente: «No, il nuovo obbiettivo e scopo restano i veicoli veloci e il video deve mostrare queste situazioni, ad esempio in scenari con detriti, condizioni meteo sfavorevoli che limitano la visione o anche a seguito di danni dovuti a esplosioni di motori e danni in volo ad esempio nel caso di droni vicini che collidono lasciando detriti, situazioni improvvise altamente impulsive e fiammate che rendono la visibilità estremamente limitata.»

Lettura del coordinatore: il file di istruzioni del video non è vincolante alla lettera; ne restano le regole di onestà. Le interruzioni della visibilità da mostrare e da provare comprendono eventi improvvisi (collisione fra droni con detriti, avaria di un motore con fiammata e fumo, detriti a terra) e il meteo (nebbia, pioggia). Entrano nella seconda fase come scenari E1–E5 (`f15-lunga-portata/40-eventi`), nel prototipo e nel video. Restano situazioni da osservare e segnalare: nessuna funzione d'ingaggio o di contrasto.

---

# Addendum 13 (15-11-2026, notte): autorizzazione a decidere in autonomia

Testo dell'utente: «Per qualunque scelta da fare durante la notte ti do l'autorizzazione a prenderla autonomamente, e questo include tutto tranne l'eliminazione dei files che invece non deve essere fatta in nessun caso».

Lettura del coordinatore: decido da solo e annoto ogni scelta. Nessun file si cancella: le versioni nuove vanno in file nuovi o accanto a una copia della precedente. Gli agenti ricevono il divieto nelle consegne.

---

# Decisione del coordinatore (15-11-2026, 01:55), sotto l'autorizzazione notturna: K-603

L'arbitro della seconda fase lascia all'utente se il caso centrale si dice «sito sorvegliato da droni» (tempestivo in simulazione) o «aeroporto con gli aerei in volo nell'inviluppo» (con v_max 210 m/s non tempestivo). Decido: **caso centrale = un sito aerospaziale sorvegliato (piazzale, area di prova, varco di un hangar) con droni e aerei in rullaggio**, dove l'avviso è tempestivo in simulazione (A1, A2); gli **aerei in volo** e i treni veloci si mostrano come limite dichiarato («non ancora tempestivo: serve un sensore a portata maggiore»), con l'inviluppo corretto a 210 m/s. Motivo: è la forma più forte che resta vera, ed è coerente con «aerei e droni» chiesto dall'utente.

Fase 2b (in corso): le correzioni obbligate dell'attacco nel nucleo (nuova versione accanto alla vecchia), la rilevazione degli eventi E1–E2, e la riprova di A1, A2, E1, E2 nel prototipo.

Violazioni del divieto di cancellare segnalate dagli agenti: il ruolo dei sensori ha cancellato due file scaricati per errore (non è verificato se prima o dopo il divieto); il collaudatore ha cancellato con `rm -f` un collegamento simbolico creato da lui un attimo prima (il file d'origine è intatto). Nelle consegne successive il divieto è ripetuto in testa.

---

# Addendum 14 (15-11-2026, notte): risultati incoraggianti, volo ad alta velocità come caso centrale, perdita di confidenza, hardware dedicato

Testo dell'utente, per intero:

«Essendo presentazione e video basati su un prototipo, anche dati incoraggianti come 51/60 nel caso di collisioni sono considerati buoni e possono essere inclusi nel video, basta che opportunamente documentati nel documento tecnico con l'indicazione che non copriamo ancora tutti i casi (poco realistico con 1 giorno di tempo) ma che tuttavia già con i test svolti nel poco tempo che abbiamo avuto ci sono stati riscontri molto positivi e incoraggianti. Non serve usare solo dati e risultati ottenuti con il 100% di confidenza ma è sufficiente che siano supportati da una solida base matematica e che siano abbastanza vicini a un risultato sicuro, con l'indicazione nel documento tecnico che spieghi i limiti e la necessità di migliorare alcune cose (se possibile quali e come) in maniera chiara. Rivaluta in maniera rapida tutto quanto stabilito e ottenuto nei test sia degli oggetti lenti/nucleo vicino sia in quelli ad alta velocità con droni e aerei (in questi si più preciso nella rivalutazione e, tramite opportune modifiche, includi anche gli scenari di volo ad alta velocità sia per aerei che droni con condizioni di collisione, detriti e e eventi improvvisi altamente impulsivi, per i quali indica nel documento tecnico gli attuali limiti e aree di miglioramento necessarie per passare da una proposta a un sistema effettivamente attuato. Conduci, parallelamente, con lo sciame un opportuna revisione dei risultati sui casi in questione, apporta le modifiche necessarie per migliorare ulteriormente la stima, e nei casi dove la continuità si perde offrire una stima esatta della perdita di confidenza nel tempo, e rendili il caso centrale mostrato nel video di presentazione accompagnati da una breve sezione sul caso attualmente scelto come centrale su aerei e droni in rullaggio e altri casi di applicazione del sistema. Se necessario utilizza strumenti e sensori nello stato dell'arte e stima la velocità di elaborazione di unità di elaborazione di altissimo livello, esistenti o, eventualmente, costruite appositamente per ottimizzare via hardware le prestazioni, garantendo tempi di risposta nettamente inferiori con previsioni in tempo utile, basandoti sulle tempistiche e indici di miglioramento ottenuti da sviluppi analoghi di hardware dedicato anche per compiti differenti ma che presentino simile ottimizzazione hardware tagliando i tempi, come ad esempio i recentissimi chip per modelli linguistici che riescono a produrre token a velocità alcuni ordini di grandezza superiori rispetto ad hardware generico.)»

## Come lo legge il coordinatore

- **Criterio di presentazione:** un risultato si può presentare come «incoraggiante» se ha una base matematica solida (modello dichiarato, derivazione o stima con intervallo) ed è vicino al risultato sicuro (per esempio 51/60 con il suo intervallo), PURCHÉ nel documento tecnico ci siano il limite, il dominio e che cosa migliorare e come. Le frasi restano vere: «in 51 prove simulate su 60», non «sempre». Resta vietato presentare come provato su hardware ciò che è simulato.
- **Caso centrale nuovo:** volo ad alta velocità di aerei e droni, con collisione, detriti ed eventi improvvisi altamente impulsivi. Il sito con droni e aerei in rullaggio diventa una sezione breve, con gli altri usi (corto raggio, persona non vedente).
- **Perdita di continuità:** dove la continuità si perde, una stima esatta (in forma chiusa o con il suo metodo di calcolo e la sua verifica) della confidenza in funzione del tempo.
- **Stato dell'arte e hardware dedicato:** sensori allo stato dell'arte e stime di tempi di elaborazione con unità dedicate (esistenti o progettate apposta), per analogia documentata con acceleratori dedicati (per esempio i chip per modelli linguistici); sono stime, dichiarate come tali.
- Il montaggio finale del video in corso è stato fermato (i suoi file restano) e riparte sul caso nuovo.
