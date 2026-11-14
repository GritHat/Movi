# Le convocazioni dello sciame: quattro strategie

**Stato.** Versione 3.1 del 14 novembre 2026: la forma portabile della 3.0 dell'8 novembre. Vale in qualunque
progetto con la sola cartella `sciame/`, e aggiunge il nucleo della percezione, della stima e del movimento con i suoi
sette profili. Generalizza la v2.4.1 dello sciame ETH (la convocazione a grafo) per progetti di ogni tipo, e la amplia
con tre strategie: la convocazione singola, la convocazione completa e la scelta automatica.

| strategia | che cosa fa | quando | quanti agenti | costo |
|---|---|---|---|---|
| **singolo** | un solo specialista, il più adatto | domanda chiara di un campo, compito piccolo, ruolo nominato | 1 | basso |
| **classica** | la pipeline a grafo: contratto, due corsie cieche, triage, torneo, squadre per ipotesi, prove, verdetti | decisione, progetto, difetto, prova, alternative, rischio | 6–15 | medio |
| **completa** | tutto lo sciame insieme in una tornata cieca; il consolidamento entra nella classica | domanda strategica o aperta, molti campi, «tutti i punti di vista» | 54 più la classica | alto |
| **auto** | sceglie il coordinatore fra le tre, e i ruoli | sempre, quando non si sa | secondo la scelta | secondo la scelta |

I blocchi fra i segni `<!-- strategia:… -->` sono il testo che `genera_agenti.py` copia nelle skill di convocazione e
nel catalogo: vanno tenuti completi e brevi. Il resto del documento li spiega e li motiva.

<!-- strategia:singolo -->
## Singolo, in breve

Quando: la richiesta è di un solo campo ed è chiara (una spiegazione, una revisione, una traduzione, un calcolo, un
compito piccolo), oppure l'utente nomina il ruolo.
1. Scegli il ruolo più adatto, dal suo «in breve» e dalle sue parole chiave. Se l'utente ne nomina uno, è quello.
2. Scrivi una consegna completa, perché lo specialista non vede niente altro:
   - la domanda;
   - gli ingressi, compreso il testo della richiesta per intero;
   - il risultato atteso e la sua forma;
   - i limiti e i divieti.
3. Lo specialista lavora e si rilegge con le sue «domande che si pone sempre».
4. Tu controlli il risultato contro la domanda. Se manca qualcosa o c'è un errore evidente, fai una sola ripresa,
   con la richiesta precisa.
5. Rispondi con il risultato, dichiarando ciò che non è verificato.
<!-- /strategia:singolo -->

<!-- strategia:classica -->
## Classica, in breve (la pipeline a grafo, ampliata)

Quando: c'è da decidere, progettare, correggere, dimostrare o misurare; ci sono alternative; un errore costa; c'è un
rischio da controllare. I ruoli di ogni fase vengono dal profilo del compito (tabella «Profili»).

**f0, il contratto (tuo).** Contiene:
- la domanda, una sola;
- il criterio che decide se la risposta è buona: una misura o un controllo, mai un meccanismo;
- gli ingressi;
- i principi e i vincoli del progetto, e le esclusioni;
- la quota di agenti e di tempo, divisa in tre terzi;
- il profilo.

Se la richiesta è ambigua, l'analista dei requisiti la chiarisce. Se il criterio è una misura, il metrologo controlla
che misuri ciò che dice.

**f1, due corsie cieche, in parallelo.** Ciascun ruolo riceve solo la sua consegna e il contratto.
- La corsia A, conservativa, ha uno o due specialisti del profilo: diagnosi, vincoli, due proposte con i
  controesempi possibili.
- La corsia B, divergente, ha il creativo (al più quattro idee tradotte) e il rovesciatore (al più due rovesciamenti).
- Ogni idea porta l'enunciato, il guadagno atteso, i vincoli, chi la può provare e il falsificatore più economico:
  al più cinque minuti, con l'esito atteso scritto prima.
- Le corsie non si leggono fra loro, e tu non leggi niente finché non hanno consegnato tutte.

**f2, traduzione, firme, triage, torneo, selezione.**
1. Un ruolo senza idee in gara (il traduttore del profilo) scrive una scheda per idea:
   - l'oggetto;
   - l'enunciato preciso;
   - il tipo;
   - i rischi;
   - l'ipotesi critica e il controesempio candidato;
   - come la si verifica.

   Niente fusioni: due idee sono la stessa solo se enunciato e tipo coincidono.
2. Ogni autore firma le schede delle sue idee: «fedele» oppure «si perde: …», e chi «si perde» ha la sua versione
   come scheda a parte.
3. L'arbitro fa il triage: assegna gli H# con una classe fra TESTARE, RIFORMULARE, APERTA e SMENTITA (solo con una
   prova), e mette in ordine le prime tre.
4. L'avversario esegue il falsificatore di ogni H# TESTARE o APERTA (senza strumenti, lo svolge a ragionamento).
   Una smentita vale per l'idea solo se la decide un controllo che non condivide il prototipo.
5. L'arbitro propone al più tre H# più una radicale, e tu decidi.

**f3, una squadra per H# scelta.** Ogni ramo è indipendente dagli altri.
- Il responsabile scrive la soluzione: passi, invarianti, costo, «dipende da», «invalidata se cambia».
- Un altro ruolo scrive la prova o la verifica.
- Il metrologo scrive il piano delle misure, con le soglie, prima delle prove.
- L'avversario prepara l'attacco.
- Se serve, si stima il costo (analista economico, sistemista delle prestazioni).

**f4, le prove, dalla più economica.** Le classi di prova:
1. a mano, o esaustiva su un caso piccolo (al più cinque minuti);
2. con un oracolo indipendente;
3. una prova realistica;
4. una prova su scala;
5. una prova a pagamento o irreversibile, solo con il sì dell'utente.

La classe k parte solo dopo l'esito della k−1. L'ordine dei compiti:
- prima le controprove dell'avversario;
- poi il debugger sulle anomalie e, se le controprove reggono, le misure;
- poi lo statistico sui numeri.

Un fallimento ferma il ramo e ne conserva il controesempio.

**f5, verdetti e chiusura.**
- Per ogni H#, il dossier con lo stato per proprietà: correttezza, completezza, efficacia, costo.
- Ogni risultato fondante passa quattro verifiche:
  1. la rilettura;
  2. l'audit delle ipotesi nascoste, da un ruolo non coinvolto;
  3. i controesempi;
  4. il consolidamento dell'arbitro.
- L'arbitro chiude solo se ci sono queste tre condizioni:
  - almeno una H# provata;
  - nessuna contraddizione aperta su una conclusione adottata;
  - ogni previsione risolta, o dichiarata non risolta con la prova che la deciderebbe.

**f6, l'integrazione (tua).** Integri solo ciò che la richiesta permette, e porti all'utente al più tre decisioni ad
alta leva.

**Sempre.**
- Un'anomalia va al debugger prima di essere usata.
- Una contraddizione K# va ai due ruoli che la sostengono e all'avversario, con una domanda binaria e al più due
  passaggi.
- Al più cinque agenti alla volta.
- Speso il primo terzo della quota, passi al verdetto con ciò che c'è.
<!-- /strategia:classica -->

<!-- strategia:completa -->
## Completa, in breve (tutto lo sciame, poi la classica)

Quando: la domanda è strategica o aperta, tocca molti campi, chiede tutti i punti di vista, oppure una classica non è
bastata.
1. **f0, il contratto**, come nella classica.
2. **f1 larga, la tornata globale.**
   - Ci sono tutti i ruoli dello sciame, salvo l'arbitro, a ondate di al più cinque.
   - Ognuno è cieco agli altri e ha la stessa consegna: il contratto, e un contributo dal proprio punto di vista di al
     più mezza pagina. Sono da una a tre osservazioni o proposte, ciascuna con la prova o il falsificatore.
   - Un ruolo che non ha niente da dire scrive «non pertinente: …» in una riga, e va bene.
3. **f1c, il consolidamento dell'arbitro.** Prima per nucleo, poi d'insieme:
   - i fatti F#, con lo stato;
   - le contraddizioni K#;
   - le idee candidate, con la loro origine;
   - le domande aperte.

   Non si vota.
4. **L'innesto nella classica.** Le idee candidate entrano in f2 come schede d'ingresso, e da lì si prosegue come
   nella classica: traduzione, firme, triage, torneo, selezione, f3, f4, f5, f6. La corsia A e la corsia B non si
   rifanno: la tornata globale le contiene.
<!-- /strategia:completa -->

<!-- strategia:auto -->
## Auto, in breve (la scelta del coordinatore)

Scegli prima di lanciare agenti, e scrivi la scelta in una riga in testa alla risposta, per esempio: «Sciame: auto,
scelta classica, profilo codice (c'è da scegliere fra due correzioni).»
- **singolo:** la richiesta è chiara, di un solo campo, e un errore si vede e costa poco; oppure chiede una
  spiegazione, una traduzione, una revisione, un riassunto, un calcolo.
- **classica:** c'è da decidere, progettare, correggere, dimostrare o misurare; ci sono alternative; un errore costa;
  c'è un rischio da controllare.
- **completa:** la domanda è strategica o aperta, tocca almeno tre nuclei, chiede tutti i punti di vista, oppure una
  classica precedente non è bastata.

In dubbio fra due strategie, scegli la più economica che soddisfa il criterio di successo. Mai la completa per una
richiesta di poche righe con una risposta verificabile.

I ruoli sono quelli del profilo, più quelli le cui parole chiave compaiono nella richiesta.
<!-- /strategia:auto -->

<!-- profili -->
## Profili per tipo di compito

| profilo | per | f1, corsia A | f1, corsia B | f2, traduce | f3, per H# | f4, per H# |
|---|---|---|---|---|---|---|
| `codice` | scrivere o cambiare codice | architetto, sviluppatore | creativo, rovesciatore | logico | sviluppatore (soluzione), tester (verifica), avversario | avversario, debugger, tester |
| `difetto` | bug, errori, anomalie | debugger, sviluppatore | rovesciatore | logico | debugger (causa), tester (test che fallisce prima), avversario | avversario, debugger, prestazioni se è lentezza |
| `architettura` | progetto di un sistema, scelte tecniche | architetto, requisiti | creativo, rovesciatore | logico | architetto (soluzione), sicurezza, ottimizzazione, avversario | avversario, prestazioni, economista |
| `prova` | matematica, logica, correttezza | formalista, matematico | rovesciatore | logico | formalista (prova), logico (rilettura), avversario | avversario |
| `dati` | analisi, statistica, misure, esperimenti | statistico, metrologo | creativo, rovesciatore | logico | dati (soluzione), metrologo (piano), statistico, avversario | avversario, debugger, statistico |
| `ia` | modelli, prompt, agenti, addestramento | llm, ml | creativo, rovesciatore | logico | llm o ml (soluzione), metrologo, sicurezza, avversario | avversario, statistico, debugger |
| `ricerca` | stato dell'arte, confronti | ricercatore, esperto-dominio | creativo, machine-intelligence | logico | ricercatore (sintesi), fonti, avversario | fonti, avversario |
| `scrittura` | testi, documenti, lettere | redattore, esperto-dominio | creativo, rovesciatore | requisiti | redattore (testo), lettore, fonti, avversario | lettore, fonti |
| `studio` | spiegare, imparare, ripassare | didatta, esperto-dominio | creativo, visualizzatore | redattore | didatta (spiegazione), visualizzatore, lettore | lettore, avversario |
| `decisione` | scegliere fra opzioni, acquisti, investimenti | requisiti, economista | rovesciatore, creativo | logico | economista (confronto), normativo, pianificatore, avversario | avversario, statistico |
| `piano` | progetti, organizzazione, calendari | pianificatore, requisiti | rovesciatore | logico | pianificatore (piano), economista, avversario | avversario |
| `sicurezza` | rischi, privacy, permessi | sicurezza, infrastruttura | rovesciatore, creativo | logico | sicurezza (contromisure), normativo, avversario | avversario, debugger |
| `dispositivo` | hardware, firmware, tablet, protocolli | embedded, infrastruttura | creativo, rovesciatore | logico | embedded (procedura), sicurezza, metrologo, avversario | avversario, debugger, metrologo |
| `interfaccia` | UX, pannelli, flussi, testi d'interfaccia | interfacce, requisiti | creativo, rovesciatore | logico | interfacce (proposta), lettore, redattore, avversario | lettore, avversario |
| `percezione` | rilevare, segmentare e riconoscere da immagini e nuvole di punti | visione, nuvole-punti | creativo, rovesciatore | logico | visione (soluzione), validazione, metrologo, avversario | avversario, debugger, validazione, statistico |
| `movimento` | scene che cambiano con il movimento: oggetti mobili, cambiamenti, eventi | scene-dinamiche, slam | creativo, rovesciatore | logico | scene-dinamiche (soluzione), validazione, tracciamento, metrologo, avversario | avversario, debugger, validazione, statistico |
| `stima` | stimatori dello stato, filtri di Kalman, fusione delle misure | kalman, fusione | rovesciatore, creativo | logico | kalman (soluzione), matematico, metrologo, avversario | avversario, debugger, statistico |
| `tracciamento` | seguire più oggetti nel tempo: associazione, identità, previsione | tracciamento, kalman | creativo, rovesciatore | logico | tracciamento (soluzione), validazione, metrologo, avversario | avversario, debugger, statistico |
| `localizzazione` | moto proprio, odometria, SLAM, mappe | slam, kalman | creativo, rovesciatore | logico | slam (soluzione), fusione, metrologo, avversario | avversario, debugger, statistico |
| `sensori` | scelta, montaggio, sincronizzazione e calibrazione di LiDAR, camere, radar, unità inerziali | lidar, sensori | rovesciatore, creativo | logico | lidar (soluzione), fusione, metrologo, avversario | avversario, debugger, metrologo |
| `latenza` | percezione in tempo reale: latenza, sincronizzazione dei flussi, calcolo a bordo | tempo-reale, prestazioni | creativo, rovesciatore | logico | tempo-reale (soluzione), ottimizzazione, metrologo, avversario | avversario, debugger, prestazioni |
| `video` | video di presentazione di un progetto: messaggio, sceneggiatura, montaggio, voce | videomaker, comunicazione | creativo, marketing | redattore | videomaker (video), comunicazione (messaggio e parlato), lettore, fonti, avversario | lettore, fonti, avversario |
| `generale` | tutto il resto | logico, machine-intelligence | creativo, rovesciatore | formalista | secondo il caso, metrologo, logico (prova), avversario | avversario, debugger, statistico |

Valgono in tutti i profili:
- in f2, le firme degli autori, il triage e la selezione dell'arbitro, il torneo dell'avversario;
- in f4, il debugger su ogni anomalia di qualunque fase;
- in f5, l'arbitro per la chiusura.

Il traduttore non deve avere idee in gara: se è già in corsia A, traduce il formalista, o il logico se il formalista è
in gara. Si aggiunge ogni ruolo le cui parole chiave compaiono nella richiesta, entro la quota. L'esperto di dominio
ha nella consegna il campo in cui parla.

Nei profili della percezione (`percezione`, `movimento`, `stima`, `tracciamento`, `localizzazione`, `sensori`,
`latenza`) il responsabile di f3 è il primo ruolo indicato. Se il compito è di un altro campo (una nuvola di punti nel
profilo `percezione`, una camera nel profilo `sensori`), lo cambi con `seleziona --responsabile`.

Nel profilo `video` il lettore critico guarda il video come chi lo riceve, e il curatore delle fonti verifica ogni
cifra e ogni affermazione che compare sullo schermo o nel parlato: ciò che non ha una prova si toglie, o si dice
come atteso.
<!-- /profili -->

---

## Perché quattro strategie

Lo sciame ETH conosceva due modi.
- **Le tornate di v1**: tutti i ruoli sulla stessa domanda, e un arbitro che legge tutto. Erano costose: un solo punto
  aperto faceva rifare la tornata a tutti.
- **La convocazione a grafo di v2**: poche ipotesi separate, fermate presto quando cadono, con cancelli controllabili.

Le due servono a cose diverse, e nella maggior parte delle richieste quotidiane non serve nessuna delle due: basta lo
specialista giusto.
- **Singolo:** per le richieste piccole, una sola consegna ben scritta allo specialista giusto vale più di uno sciame.
- **Classica:** è la v2 resa generale. Separa le ipotesi, le mette alla prova dalla più economica e dichiara che cosa
  è provato.
- **Completa:** è la tornata globale di v1, senza voto. Serve quando non si sa ancora dove guardare, e il suo
  risultato non è una conclusione: entra nella classica come materiale da vagliare.
- **Auto:** fa la scelta al posto dell'utente, con le regole scritte sopra, e la dichiara.

## Principi che non si negoziano

- **Il criterio prima del meccanismo.** Il contratto dice come si riconosce una buona risposta, mai quale soluzione
  adottare.
- **Le prove prima delle conclusioni.** Le regole del `PREAMBOLO.md`: stati distinti, previsioni con l'ora prima delle
  prove, numeri con il file.
- **L'indipendenza per classe d'errore.** Ogni controllo dichiara che cosa condivide con ciò che controlla. Solo un
  controllo che non condivide il difetto lo può escludere. Un modo comune (due controlli che sbagliano allo stesso
  modo) si chiude sulla classe, non sul singolo testimone.
- **Le previsioni congelate.**
  - Si scrivono prima della prova che le decide, con l'ora e la soglia.
  - Se cambia la premessa (versione, dati, configurazione), la previsione resta, segnata «premessa cambiata», e prova
    il modello, non il meccanismo.
  - Una prova decide solo se parte dopo la registrazione.
- **Le scritture.**
  - Gli agenti scrivono solo nello spazio della convocazione.
  - Integra il coordinatore, e solo ciò che la richiesta permette.
  - Le azioni irreversibili, a pagamento o verso l'esterno le decide l'utente.
- **La convergenza non si forza.** Una soluzione incompleta si dichiara con le cause. Un'accettazione per difetto
  (finito il tempo, si prende ciò che c'è) non è un «non risolto»: è una decisione mancante, e si dichiara.

## La strategia classica nei dettagli

Il grafo è f0 → f1 → f2 → un ramo f3 → f4 per ogni H# scelta → f5 → f6. Le dipendenze sono fra file e cancelli, non
fra nomi di ruoli: un compito parte appena i suoi ingressi sono congelati. I rami delle H# non si aspettano fra loro;
solo f5 aspetta tutti i rami.

### I cancelli

Ogni fase finisce con un cancello, che il coordinatore approva dopo aver letto i file. Con i file lo controlla
`convoca.py cancello`, che lega con lo sha256 i file della fase: un file cambiato dopo
l'approvazione rende il cancello non valido. Un cancello non si approva perché i file esistono.

| cancello | condizioni |
|---|---|
| G0 | contratto completo: domanda, criterio, ingressi, vincoli, quota, profilo |
| G1 | consegne di tutte le corsie (o «non consegnato» dopo due arresti), nessun canarino di una corsia nell'altra, la foto delle letture fatta prima di leggere |
| G2 | firme degli autori prima del sigillo del triage, sigillo prima del torneo, selezione solo fra gli H# del triage, controfirma dell'arbitro |
| G3 (per H#) | soluzione, verifica, piano delle misure e previsioni congelati; le soglie raggiungibili e con una prova che le possa decidere |
| G4 (per H#) | controprove prima di ogni costo; classi in ordine; previsioni sigillate prima delle loro prove; le anomalie spiegate o dichiarate; dossier completo |
| G5 | le condizioni di chiusura dell'arbitro e le quattro verifiche dei risultati fondanti |

### La cecità delle corsie

- Ogni corsia scrive in una cartella dal nome casuale. La mappa delle cartelle la conosce solo il coordinatore.
- Ogni consegna comincia con il canarino della sua corsia: G1 rifiuta se il canarino di una corsia compare nell'altra.
  Il canarino scopre una copia, non una lettura.
- Appena le corsie hanno consegnato, prima di leggere, `convoca.py fotografa` registra per ogni file se è stato letto
  dopo l'ultima scrittura. È un indizio, non una prova.
- Gli agenti sono tutti lo stesso utente: i permessi non impediscono di leggere, quindi la cecità sta
  nelle consegne, nei canarini e nella disciplina del coordinatore.
- Senza file (gli agenti senza strumenti), la cecità è data dal fatto che ogni agente riceve solo la sua consegna.

### La sentinella

Nelle classiche con almeno due rami, in f2, f3 e f4 lavora un ruolo non convocato, estratto a caso. Ha venti minuti in
sola lettura e consegna:
- un presupposto condiviso, messo alla prova con un controllo esterno;
- le cifre e gli identificativi del dossier, ricontati dai file.

Un suo K# entra solo con un file. Serve a trovare ciò che nessun profilo avrebbe convocato.

### Le anomalie: il debugger

- **Che cos'è un'anomalia:**
  - un esito che contraddice una previsione;
  - un tempo o una memoria fuori scala rispetto a un caso vicino;
  - una divergenza fra due implementazioni o con un oracolo;
  - un errore, un «non deciso» o un valore di difetto che nessuno spiega.
- **Va al debugger** prima di entrare in un verdetto, con i soli file coinvolti, il sintomo con la cifra e il caso
  vicino che funziona.
- **Il debugger consegna** la causa provata: una riproduzione minima che fallisce prima della correzione e passa dopo.
  Consegna anche la classe del difetto, dove altro può esserci e la correzione con il suo test.
- **Senza causa provata** l'anomalia resta «non spiegata», e non sostiene nessuna affermazione.

### Le contraddizioni: i cicli locali

- Una K# va ai due ruoli che la sostengono e all'avversario, con i soli file coinvolti, una domanda binaria e la prova
  che la decide. Se è un'anomalia del codice, il terzo è il debugger.
- Si fanno al più due passaggi; poi la K# resta APERTA, con il costo dell'esperimento decisivo.
- Se tocca una conclusione adottata, l'adozione si sospende e la K# va all'utente.

### L'audit delle ipotesi nascoste (dalla regola AIN dello sciame ETH)

Si applica a ogni **risultato fondante**, cioè a un enunciato su cui poggia una certificazione, un'adozione o una
chiusura. Le quattro verifiche sono distinte:

| | verifica | chi | che cosa |
|---|---|---|---|
| V1 | la rilettura | un ruolo non autore | la validità dei passaggi rispetto alle premesse dichiarate |
| V2 | l'audit delle ipotesi nascoste | un ruolo non coinvolto né nella costruzione né in V1 (di norma il rovesciatore o un'istanza nuova del debugger) | le condizioni necessarie non dette: versioni, rappresentazioni dei dati, codifiche, cache e stato, ordine delle chiamate, bordi, domini vuoti, limiti operativi, differenze fra la teoria e il comportamento del sistema |
| V3 | i controesempi | un avversario non autore | casi minimi e limite, test metamorfici e differenziali, con le previsioni prima |
| V4 | il consolidamento | l'arbitro | lo stato, fra cinque: dimostrazione incondizionata; dimostrazione condizionata, con le premesse e il dominio; evidenza sperimentale, con l'insieme esaminato; controesempio certificato; questione aperta |

L'indipendenza è per istanza: un'istanza nuova di un ruolo, che non ha letto i giudizi degli altri, conta come
indipendente. Un audit negativo («nessuna ipotesi nascosta trovata») è un requisito procedurale, non una garanzia.

### Il dossier

Ogni H# ha un ID stabile (H-001) e un dossier dal modello `SCHEDA_IPOTESI.md`, che l'arbitro completa con il verdetto,
campo per campo, con i rimandi ai file del ramo. Un campo vuoto si scrive «manca».

## La strategia completa nei dettagli

- **Le ondate.** Al più cinque agenti alla volta, nucleo per nucleo, in quest'ordine:
  1. il nucleo critico (senza l'arbitro);
  2. i nuclei del profilo;
  3. gli altri.

  Ogni agente vede solo la propria consegna.
- **La consegna** è la stessa per tutti, cambia solo il ruolo: il contratto, la richiesta, e «dal tuo punto di vista:
  al più tre osservazioni o proposte, ciascuna con la prova o il falsificatore; se il tuo campo non c'entra,
  "non pertinente" e perché, in una riga».
- **Il consolidamento dell'arbitro** si fa per nucleo e poi d'insieme. Contiene:
  - i fatti con lo stato;
  - le contraddizioni;
  - le idee candidate con l'origine (ruolo e file);
  - le domande aperte;
  - i ruoli da chiamare nelle fasi seguenti.
- **L'innesto.** Le idee candidate diventano schede d'ingresso di f2, e i loro autori le firmano come nella classica.
  Il traduttore deve essere un ruolo senza idee fra le candidate: di norma un'istanza nuova del logico.
- **I costi.** Una completa costa quanto una tornata di v1 più una classica. Per questo «auto» la sceglie solo nei casi
  scritti sopra.

## Risorse

- **La quota.** Il contratto fissa il numero di agenti e il tempo, e li divide in tre terzi:
  1. le fasi fino a f3;
  2. verdetto e risposta;
  3. una riserva per riprese e agenti fermati.

  Speso il primo terzo, si passa al verdetto con ciò che c'è.
- **I tempi massimi** di riferimento: singolo 15 minuti, classica 60, completa 120 (undici ondate, poi la classica).
  Li fissa il contratto, e l'utente può fermare in ogni momento.
- **Gli agenti** sono al più cinque alla volta. Un agente fermato si rilancia con la sua sola consegna e il suo
  `stato.md`; dopo due arresti la sua consegna è «non consegnata».
- **I processi pesanti** vanno uno alla volta per agente, con `timeout`. GPU e servizi a pagamento solo con il sì
  dell'utente.

## Come si svolge nei diversi ambienti

- **In un progetto, con i file.** Il coordinatore è la sessione di Claude Code aperta nella radice del progetto, e
  gli agenti sono i suoi sottoagenti `sciame-<sigla>`.
  - La convocazione sta in `.sciame/<AAAAMMGG-HHMM>-<nome>/` dentro il progetto.
  - `sciame/convoca.py` prepara lo scheletro e controlla i cancelli.
  - I documenti completi sono in `sciame/`.
- **Senza shell o senza scritture.** Le fasi sono le stesse. Le consegne stanno nei prompt, le risposte degli agenti
  sono le consegne, e i cancelli li controlla il coordinatore con le condizioni scritte sopra.
- **Con un modello raggiunto per API,** che non lancia agenti: un programma proprio fa il coordinatore, una chiamata
  per ruolo, con i testi di `sciame/catalogo.json` (`ISTRUZIONI_COORDINATORE.md` dice quali chiamate). Le fasi f3 e
  f4 sono condensate: niente esecuzioni, solo critiche e verifiche a ragionamento.
- **L'isolamento.** Gli agenti lavorano con i permessi della sessione che li lancia. Dove un compito esegue codice non
  fidato, installa pacchetti o tocca un dispositivo, la sessione va aperta in un ambiente isolato (un contenitore,
  una macchina a perdere): lo sciame non lo fa da sé.

## Dossier e consegne

- Le consegne non dicono «esamina il progetto». Danno:
  - gli ingressi, con il percorso assoluto o il testo;
  - il file d'uscita;
  - la prova minima, la soglia e il tempo;
  - la classe massima di prova;
  - i divieti e il destinatario.
- Gli ID provvisori portano il prefisso del ruolo (`creativo-2`); gli H#, F# e K# definitivi li assegna l'arbitro.
- La risposta all'utente comincia con una riga «Sciame: <strategia>. Ruoli: <ruoli>.». Poi viene il risultato, con
  gli stati di ciò che afferma, gli aperti e al più tre decisioni che spettano a lui.

## Che cosa cambia

**Rispetto alla 3.0.**
- **È portabile.** Tutto sta nella cartella `sciame/` del progetto: i documenti, il catalogo, `convoca.py`,
  `genera_agenti.py` e `sciame.sh`, che installa e avvia. Gli agenti e le skill di convocazione si generano in
  `.claude/`, per Claude Code. Non servono contenitori, né un programma che faccia da tramite.
- **Il nucleo della percezione.** Undici ruoli (schede 41–51) e sette profili: `percezione`, `movimento`, `stima`,
  `tracciamento`, `localizzazione`, `sensori`, `latenza`.
- **`convoca.py`.** Il comando `ruoli` e l'opzione `--responsabile` di `seleziona`.
- **La presentazione di un progetto** (aggiunta del 14 novembre 2026). Tre ruoli nel nucleo della conoscenza e della
  comunicazione (schede 52–54: marketing, videomaker, comunicazione) e il profilo `video`.

**Rispetto alla v2.4.1 dello sciame ETH.**
- **I contenuti.** Non ci sono più la semantica, la cascata, il motore e le famiglie di quel progetto. Al loro posto
  ci sono i principi che il contratto di ogni convocazione dichiara.
- **I profili.** Coprono progetti di ogni tipo; quelli di allora erano cinque, propri di quel progetto.
- **I cancelli.** Restano G0–G5, controllati da `convoca.py` nella forma generale: i file legati con lo sha256, le
  corsie cieche con i canarini, i sigilli e la selezione solo dal triage.
- **Le strategie nuove.** Singolo, completa e auto.
