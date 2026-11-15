# Lettura critica delle tre proposte per il video MoVi (f17-video/20-lettura) — `sciame-lettore`

Iniziata il 2026-11-15T00:30+01:00. Ho letto a freddo, una volta, `10-messaggio/MESSAGGIO_E_ARCO.md`,
`11-marketing/POSIZIONAMENTO_E_LOGO.md`, `12-regia/REGIA_E_SISTEMA_VISIVO.md`, i tre fotogrammi `stile_*_v2.png` e
`video/marchio/tavola_controllo_v2.png`. Poi ho fatto la lettura annotata e il confronto con le regole d'onestà di
`ISTRUZIONI_VIDEO_UTENTE.md` (cercate per parola chiave, non lette per intero) e con gli addendum 11–12.

## 0. Cambi di stato e regole

- Nessuna regola violata. Ho scritto solo questo file. Non ho cancellato niente, non ho usato git né la rete.
- **Indipendenza:** non condivido con gli autori né il testo né le immagini. Condivido le regole d'onestà, quindi non
  posso vedere i difetti che stanno dentro le regole stesse.
- **Limite:** i due giurati sono simulati da me, e i loro giudizi sono previsioni non verificate. Le decide il test
  con persone vere che le proposte stesse indicano (`comunicazione-1`, il test dei cinque secondi).
- Non ho letto `voce_en.txt`: il testo lo prendo dalle tabelle del §4 del messaggio, che dichiara di essere identico
  (non verificato).

## 1. Giurato esterno (nessun contesto)

- **Che cosa capisce in 30 s.** Ha davanti la scena 1 e l'inizio della scena 2. Capisce che un drone sparisce dietro
  un hangar e che lo schermo «dice qualcosa» invece di cancellarlo. Lo capisce perché la domanda «What should the
  screen say now?» è chiara.
  - Il rischio sta nei fotogrammi: la tavola a tre viste porta **25–30 blocchi di testo** in monospazio (pannelli,
    console, fasce, sottotitoli). Il giurato legge i sottotitoli e non guarda la pianta.
- **Dove si perde.**
  1. **I nomi delle cose che non si vedono.** In 3 minuti incontra NOT SEEN, NOT OBSERVED, UNVERIFIED, UNKNOWN,
     POSSIBLE PRESENCE, WIDE ZONE/PREDICTION e POSSIBLE DEBRIS. La voce promette «tre risposte», e lui ne conta sette.
     Il «I don't know» della scena 2 poi non ricompare in nessuna scena: nella tabella degli stati della regia non
     c'è nessuna riga «unknown».
  2. **La scena 8.** Dagli aerei si passa a «a blind person» a 2:30. Il salto non è preparato, e in 11 s legge una
     riga di 16 parole.
  3. **«Warning not timely».** In inglese è innaturale, e non capisce di chi sia l'avviso.
  4. **Il fotogramma B.** Non capisce la linea ambra tratteggiata fra AC1 e V1, né le due zone a righe che si
     sovrappongono (una ambra e una corallo).
- **Che cosa legge come promessa.**
  - «MoVi never calls a space empty unless it has looked»: la legge come «non sbaglia mai».
  - «a warning to the person below» e «The service vehicle is warned»: capisce che MoVi parla con le persone e con i
    mezzi.
  - Tagline «…always declared»: «always» per lui è una garanzia.
- **Che cosa ricorda il giorno dopo.**
  - Il cerchio pieno e il cerchio tratteggiato.
  - «Droni che si scontrano, un motore che fa un lampo, nebbia».
  - «È tutto simulato», perché lo sente due volte.
  - Probabilmente non ricorda le tre risposte nella forma esatta (previsione, non verificata).
- **Aerei e droni con gli eventi.** Li capisce come immagini: le sagome piatte non spaventano, e la stella bianca è
  leggibile come «lampo». Il rischio è l'effetto catalogo: tre incidenti di fila sullo stesso piazzale sembrano un
  «disastro dimostrativo». Mancano la **pioggia**, che l'utente aveva chiesto (addendum 12), e i **detriti come
  scena a sé**.
- **Il logo.**
  - Il wordmark si legge «MoVi»: la «o» tratteggiata è graziosa.
  - Nel simbolo SDMs, il disco e la zona tratteggiata con l'anello dentro sono un buon richiamo, ma solo dopo aver
    visto il video.
  - Da solo, il tratteggio ambra sembra una **rotellina di caricamento** o un sole.
  - Non sa che cosa voglia dire «SDMs», e nessuno glielo dice.

## 2. Giurato tecnico (società di aerospazio)

- **Che cosa capisce in 30 s.** Che è coasting con uno stato esplicito, e che l'assenza di dati non diventa «spazio
  libero». È interessato, ma aspetta di vedere la differenza dal coasting classico. Il video non la dice mai: è
  nelle domande del §9, non in voce.
- **Dove si perde.** Sono incoerenze che nota subito:
  1. **«Only the radar is left: no redundancy» (scena 4)**, mentre a schermo c'è «ADS-B · IN SERVICE» (fotogramma C).
     Va detto che l'aereo non ha transponder, cosa che oggi sta solo nel pannello di verità.
  2. **«EO useful: 23 m».** È collegato con una linea lunga centinaia di metri sulla scala di 500 m, e così sembra la
     lunghezza della linea. Il voice-over parla di un multirotore, ma il fotogramma mostra «light aircraft».
  3. **Il fotogramma A.** «A · PREDICTED» contraddice il lessico (il messaggio §7 vieta «predicts»). I **punti
     bianchi dei frammenti dentro la pianta «as MoVi declares it»** sembrano frammenti osservati. È proprio la
     previsione disegnata come osservazione che la regola vieta, e la regia stessa lo vieta nel §5, componente 6.
  4. **Il fotogramma B.** L'evento si chiama «separation · INFERRED», mentre la voce dice «engine fails»: non è chiaro
     che cosa si sia separato. La scena è E2, ma non viene detto che è scritta a mano.
  5. **Il contatto dedotto dalla sola fusione delle tracce.** Gli chiederà con quale criterio viene dedotto. Il video
     non lo dice, e a schermo basterebbe «inferred from: track merge + spread».
- **Che cosa legge come promessa o garanzia.**
  - «The radar alone still sees the aircraft»: detto in voce senza riserva. La riga «not verified» sta in piccolo
    in console, mentre la voce è il canale forte.
  - «The service vehicle is warned» e «a warning to the person below»: legge un collegamento dati verso il mezzo e
    verso la persona che non esiste (il marketing §1: «in progetto, mai generato»).
  - «stayed inside the declared volume [k of n]»: se il valore arriva da 1 131 692 campioni «nei casi conformi»
    dello stesso autore, senza «in the cases within the model» lo legge come garanzia.
  - «Tracks lost without a warning»: usa «lost», cioè proprio la parola vietata come stato.
  - «No engagement or pointing function» (scena 9): negare l'ingaggio porta comunque l'ingaggio in testa al giurato,
    e la regola chiede di non usarne il lessico.
- **Che cosa ricorda.**
  - Il volume dei detriti che non si restringe e «clears by inspection»: è l'idea più nuova per lui.
  - La banda «RELIABILITY LOST» per sensore.
  - «First, the limits»: lo ricorda come segno di serietà.
- **Aerei e droni con gli eventi: credibile o spettacolare?**
  - **Credibili** la nebbia e l'abbagliamento delle camere, se le cifre sono dette «by calculation».
  - **Al limite** la collisione fra droni d'ispezione a 80 m da una persona, sul piazzale accanto a un aereo in
    rullaggio. Lo scenario stesso è improbabile in un'area operativa. Va detto che è uno scenario di prova scritto,
    e il fotogramma A lo dice già («written by hand»).
  - **Un rischio visivo:** nel fotogramma B il cuneo corallo a righe parte dai sensori e arriva fino all'aereo. Per
    un tecnico della difesa somiglia a un fascio di puntamento o di illuminazione. È un cono rosso puntato su un
    aereo.
  - Allo stesso modo, il simbolo SDMs (un cerchio pieno e un cerchio concentrico tratteggiato) può ricordare una
    mira. Rischio basso, ma da provare.
- **Il logo.** Gli sembra pulito e coerente con la grammatica degli stati. Chiede se «SDMs» sia una sigla. Il colore
  ambra significa «non visto» nel logo, ma nel video lo stesso ambra vale anche per «USEFUL RANGE REDUCED» e «NO
  REDUNDANCY». In più l'ocra #C7841A dei detriti e il #F5A524 a schermo non si distinguono (fotogramma A).

## 3. Incoerenze fra le tre proposte

| Tema | Messaggio (10) | Marketing (11) | Regia (12) |
|---|---|---|---|
| Tempi delle scene 2–9 | 2: 0:12–0:38; 3: 0:38–0:55; 4: 0:55–1:13; 5: 1:13–1:36; 6: 1:36–1:56; 7: 1:56–2:30 (34 s); 8: 2:30–2:41; 9: 2:41–2:52 | titolo 0:00–0:04; cartello dei limiti 4 s letto in voce; chiusura 2:44–2:48; titoli di coda 2:48–2:51,5 | 2: 0:12–0:32; 3: 0:32–0:50; 4: 0:50–1:10; 5: 1:10–1:36; 6: 1:36–2:02; 7: 2:02–2:30 (28 s); 8: 2:30–2:40; 9: 2:40–2:52 |
| Titolo d'apertura | nessuno: si apre sul piazzale con la voce | cartello di 4 s, senza etichetta | il titolo sta nella scena 2 |
| Limiti finali | nella scena 7 | un secondo cartello prima dei titoli di coda | nella scena 7 |
| Titoli di coda | nella scena 9, con i nomi | circa 20 righe in 3,5 s, illeggibili | crediti nella scena 9 |
| Frase di chiusura | «It never calls a space empty unless it has looked» | T1 «Seen, unseen, unknown: always declared» | critica 7: «…unless enough sensors have looked» |
| Stato «libero» | OBSERVED EMPTY · class | «seen clear up to d metres» | SEEN FREE TO 2 000 m |
| Non vista | NOT SEEN FOR X s | not seen (zone) / «unseen» | NOT SEEN · 2.4 s |
| Previsto ampio | WIDE ZONE | — | WIDE PREDICTION (e «A · PREDICTED» nel fotogramma A) |
| Ricomparsa | SEEN AGAIN · IDENTITY ASSUMED | — | REAPPEARED · IDENTITY PRESUMED |
| Nube | NOT OBSERVED · CLOUD | — | NOT OBSERVED · SMOKE (EO, IR) |
| Evento | EVENT: CONTACT · INFERRED | — | EVENT: CONTACT (INFERRED) |
| Etichetta d'onestà | in basso a destra, «Simulation»/«Schematic» | il titolo ne è esente | in alto a destra, «SIMULATION · SENSORS MODELLED FROM DATASHEETS» |
| Scena 8 | Schematic (o Simulation · ideal sensor) | — | SIMULATION · ideal sensor |
| Logo SDMs | «disegnati da noi» | già fatto: disco, zona tratteggiata con anello, Inter SemiBold | componente 16 «proposta»: disco, anello, quadrato a puntini, Inter 700, «da disegnare» |
| Colori | — | ambra = non visto | l'ambra vale anche per i sensori degradati; corallo #FF6B6B (rosso) per l'affidabilità persa |

Altre incoerenze:

- **La regola delle 16 parole per schermata** (ISTRUZIONI, regola 3 e controllo Q4) è ripresa nel messaggio §4, ma
  i tre fotogrammi la superano di molto, anche contando solo il testo che non è etichetta di stato.
- **I sottotitoli dei fotogrammi** («Two drones touch. The system does not see the impact…») non coincidono con la
  voce del messaggio §4, mentre il controllo Q20 chiede che coincidano.

## 4. Correzioni in ordine d'importanza, con il testo proposto

1. **Un solo lessico, deciso ora e applicato a tutte e tre le proposte.** Proposta:
   - SEEN;
   - NOT SEEN · X s, con la zona;
   - WIDE ZONE, mai PREDICTED o PREDICTION;
   - SEEN AGAIN · IDENTITY ASSUMED;
   - NOT OBSERVED · cause (sensors);
   - UNVERIFIED ZONE;
   - OBSERVED EMPTY · class (via «clear» e «free»).

   Rinominare «A · PREDICTED» in «A · NOT SEEN 1.1 s · IDENTITY ASSUMED».
2. **Rendere visibile la terza risposta, o non prometterla.** Aggiungere uno stato «UNKNOWN» (i puntini «?» della
   scena 2) in almeno una scena di evento. Per esempio, nella scena 4 dopo la caduta del radar: «LA1 · UNKNOWN ·
   reliability lost». Senza questo, la voce della scena 2 va cambiata in: «For every object, MoVi says: I see it; I
   don't see it, here is where it can be; or I don't know — and it says when it can't be trusted.»
3. **Togliere dalla voce le promesse di comunicazione.**
   - Scena 5: «…and the operator gets a warning for the person below.»
   - Scena 6: «A warning is raised for the service vehicle.»
4. **Riserva in voce sul radar (scena 6):** «In our model, the radar still sees the aircraft — its response to the
   flash is not verified.» (+7 parole; si compensa con il taglio 4 del §10.)
5. **Niente previsione disegnata come osservazione.** Nel fotogramma A, togliere i punti bianchi dalla pianta: i
   frammenti stanno solo nel pannello di verità. Nella pianta va solo il volume a righe.
6. **Niente coni rossi verso un aereo.** Nel fotogramma B, la copertura delle camere accecate diventa un contorno
   grigio a trattini con la parola «EO, IR · NOT COUNTED». Il corallo resta solo nelle bande della console.
7. **Una sola scaletta dei tempi**, quella del messaggio, che la regia allinea. Il titolo d'apertura del marketing
   entra nella scena 2 (0:14–0:18, come nelle ISTRUZIONI). Il cartello dei limiti del marketing si toglie: lo
   sostituisce la scena 7. I titoli di coda si riducono a 3 righe: «MoVi · Team SDMs: [nomi] · Music, voice, fonts:
   see description». I crediti completi vanno nella descrizione del caricamento (licenza CC BY: verificare che
   un'attribuzione fuori dal video sia ammessa, **non verificato**).
8. **Una sola frase di chiusura, senza «always» e senza «never»:** «Seen, not seen, unknown — declared, never
   assumed empty.» In alternativa, con la frase del messaggio corretta come chiede la regia: «It never calls a
   space empty that it has not observed.»
9. **Nebbia coerente (scena 4).**
   - Voce: «Fog rolls in. The cameras now see only metres — MoVi says so, per sensor. This aircraft has no
     transponder: only the radar is left. No redundancy. If the radar drops too: reliability lost — warnings may
     come too late.»
   - A schermo: l'etichetta resta «WARNING NOT TIMELY», e il valore «23 m (calc.)» va accanto al cuneo, senza la
     linea lunga.
   - Aggiungere un quadro di 3 s con la pioggia: «HEAVY RAIN · EO useful [CIFRA-S3b] (calc.)».
10. **Fiammata (scena 6).** Nominare l'evento: in voce «An engine fails with a flash.», a schermo «EVENT: ENGINE
    FAILURE · PARTS MAY SEPARATE (INFERRED)» al posto di «separation».
11. **Scena 7.** «Tracks that disappeared with no warning: [k] of [n].» Dopo V1 aggiungere «within the assumptions of
    the model.» Se V1 è contato in campioni, dire «samples», non «fragments».
12. **Scena 9.** Togliere «No engagement or pointing function». Resta: «Observes and warns · No output is a
    command».
13. **Le 16 parole e i sottotitoli.**
    - Mettere la console in modalità ridotta: 3 righe, con le righe secondarie solo dove la voce le cita.
    - La fascia di dominio sta in una riga sola.
    - Generare i sottotitoli dalla voce, non scriverli a parte.
14. **Scena 8.** Tenere la riga D4, ma anticiparla con un ponte visivo, cioè la stessa console rimpicciolita.
    Accorciarla in: «Same core: presence warning for a blind person · does not replace a cane or guide dog» (16
    parole).
15. **Logo.**
    - Componente 16 della regia: va **usato** il marchio già fatto in `video/marchio/`, non ridisegnato.
    - Test dei cinque secondi con due domande: «che cosa significa?» e «ti ricorda una mira o un caricamento?».
    - Nel titolo d'apertura, sotto il simbolo, la riga «seen · not seen» (non «unseen», per restare nel lessico).
    - Dire una volta che cosa significa SDMs, oppure decidere che non lo si dice.
16. **Colori.** Distinguere l'ambra degli oggetti (non visto) da quello dei sensori degradati: per i sensori, bordo
    a trattini e testo #AEB8C5. Unire l'ocra dei detriti all'ambra, oppure separarli per trama, perché a schermo non
    si distinguono.

## 5. Stati proposti

- «Le tre risposte arrivano al giurato esterno»: **non risolto**. Lo decide `comunicazione-1` (4 su 5).
- «Il video promette più delle prove»: **sostenuto dal testo** per le frasi delle correzioni 3, 4 e 11. Lettura di
  un solo lettore.
- «Fotogramma A conforme alla regola 15 (Q15)»: **smentito**, per i punti bianchi nella pianta.
- «Fotogrammi conformi a Q4 (16 parole)»: **smentito**, conteggio a vista su A, B e C.

## 6. Proposta nuova

**`lettore-1` · Test dei sette nomi.**
- *Meccanismo:* troppi nomi per «non vedo» confondono le tre risposte.
- *Previsione:* dopo una visione, meno di 3 non tecnici su 5 sanno spiegare la differenza fra NOT SEEN e NOT
  OBSERVED. Con il lessico ridotto della correzione 1, almeno 4 su 5 ci riescono.
- *Smentita:* almeno 4 su 5 ci riescono anche senza ridurre il lessico.

## 7. Dopo

1. Il coordinatore fissa il lessico (correzione 1) e la scaletta (7).
2. Il comunicatore applica le correzioni 2–4 e 8–12 alla voce, poi la misura con Kokoro.
3. La regia rifà i fotogrammi A e B (5, 6, 13).
4. Il marketing fa il test del logo (15).
5. Rileggo io la versione corretta, a freddo.
