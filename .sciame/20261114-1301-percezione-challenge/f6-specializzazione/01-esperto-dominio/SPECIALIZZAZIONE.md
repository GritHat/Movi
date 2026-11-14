# Specializzazione: un nucleo, due profili — «sentinella uncrewed» e ausilio all'orientamento (`sciame-esperto-dominio`, f6)

**In testa.** Scritta dalle 2026-11-14T14:39:49+01:00, adeguata al secondo addendum dell'utente alle 14:43. Da adottare solo dopo il verdetto dell'arbitro sul nucleo.

- **Nessuna prova eseguita.** Ciò che eredito dal nucleo è simulazione, a sensore fermo, alla scala di una sala; ciò che aggiungo è **nuovo, non provato**.
- **Lunghezza, misurata** (pandoc e xelatex, A4, corpo 10, margini 1,8 cm): il corpo (§1–§6) occupa circa 3,6 pagine, poco oltre il limite di tre e mezza; gli allegati A, B e C (copertura dei requisiti, regole fisse, tabella dei blocchi) ne aggiungono una. Sono contenuti chiesti dalla consegna, messi in fondo per avvicinare il limite.
- **Due correzioni al mio `QUADRO_DOMINIO.md`:** §2(d), l'ostacolo mobile che nasconde: il nucleo dichiara di non reggerlo; §2(c), la velocità massima nel riaggancio: il nucleo l'ha tolta, e qui entra solo nella fascia.
- **Rimandi:** `V2` = `f4/H-012/05-correzioni/SOLUZIONE_V2.md` (il nucleo); `Q` = `QUADRO_DOMINIO.md` (fonti S1–S38 con i link); **[inf.]** = inferenza mia; **NV** = non verificato. Il moto proprio è in `f6-specializzazione/02-slam/MOTO_PROPRIO.md` (scritto in parallelo, non letto).
- **Parole.** *Griglia*: mappa a celle attorno al sensore (libera, occupata, in ombra dietro un ostacolo, non osservata). *Traccia*: un oggetto seguito nel tempo. *Fascia*: il margine attorno a una zona nascosta. B1–B9 sono i blocchi del sistema (allegato C), R1–R8 i requisiti della challenge (allegato A).

## 1. Un nucleo, due profili

**Che cosa rende il sistema adattabile.** Non cambia mai: i tre stati di una traccia (**osservato, previsto, perso**), lo **strato di garanzia** («possibile presenza» nella zona in cui l'oggetto è sparito, tolta solo guardando, mai da un timer) e le nove regole fisse (allegato B). Cambia solo ciò che sta in questa tabella.

| Parametro di adattamento | Profilo uncrewed (principale) | Profilo assistivo (persone non vedenti) |
|---|---|---|
| Sensore e montaggio | camera di profondità sull'albero di un rover o sull'appoggio di un drone posato; parti del veicolo mascherate. Alla scala reale un LiDAR da 10–40 m (Q, S15): da provare | la stessa camera; nel nucleo sta su un treppiede accanto alla persona ferma. Indossata: da provare |
| Sorgente del moto proprio | nessuna: piattaforma ferma. Poi la posa dell'autopilota o l'odometria (`MOTO_PROPRIO.md`) | nessuna: persona ferma. Poi sensori inerziali e odometria visuale indossati; in moto nessuna soglia vale (V2 §6) |
| Velocità massima per classe e durata del «previsto» | persona 2,5 m/s; mezzo di piazzale 8 m/s (NV); piccolo drone 19 m/s (Q, S19). Fascia da 0,40 a 3,8 m (§3.3); durata da rimisurare | persona 2,5 m/s, fascia 0,40 m, «previsto» per 0,6–0,7 s (V2). Biciclette e monopattini: NV |
| Zona di valutazione | da 1,24 a 3 m nel campo della camera; sotto 1,24 m il suolo non si vede | la stessa. Per chi cammina quel vuoto vicino è il limite più serio: lo copre il bastone |
| Canale d'uscita | schermo dell'operatore remoto (tre stati, età del dato, ritardo) e messaggio per settori a tre valori verso l'autopilota (§3.1) | un segnale sonoro breve (0,3 s) per stato, frase solo a stato stabile (V2); vibrazione: non provata |
| Alla perdita di affidabilità | tutti i settori «sconosciuto»; richiesta di attesa; alla stazione l'ultimo quadro in grigio con la sua età (§3.2) | un segnale dedicato; la persona si ferma e torna al bastone o al cane guida |
| Già provato (simulazione, sensore fermo) | il nucleo comune | il nucleo comune; i segnali brevi, nel modello |
| È un parametro | montaggio, maschera, classi e fascia, settori, soglia del collegamento | montaggio, forma dei segnali |
| Da provare | messaggio per settori, maschera, collegamento, classi veloci, scala del LiDAR, hardware | segnali con tre persone bendate (V2 §6), sensore indossato, hardware |

**Cautela sul profilo assistivo.** È un prototipo dimostrativo: non è un dispositivo medico né di sicurezza e non sostituisce bastone o cane guida. Il regolamento (UE) 2017/745 chiama dispositivo medico ciò che il fabbricante destina, fra l'altro, a «compensation for, an injury or disability» (art. 2, punto 1: https://www.legislation.gov.uk/eur/2017/745/article/2/2020-01-31, pagina aperta, copia non ufficiale). **Se un ausilio all'orientamento vi rientri è non verificato:** lo valuta un esperto regolatorio.

## 2. Il caso d'uso principale

**Una piattaforma uncrewed ferma in osservazione** (rover fermo, o drone posato sulla sua stazione) **sorveglia un varco, un tratto di piazzale o un oggetto in ispezione, con un operatore remoto.** Perché questo:
(1) è il solo caso in cui le prove del nucleo si trasferiscono (sensore fermo); **il volo stazionario resta fuori**, perché un drone in volo oscilla (Q §2a) [inf.]; (2) è il profilo pubblico della società: drone da ispezione con stazione di ricovero e supervisione remota, sorveglianza di perimetri e infrastrutture (Q §1, S7, S8); (3) è il «monitoraggio di attività e oggetti» della challenge.

Restano aperti: la piattaforma che avanza lungo un percorso d'ispezione (§5, tappa 1) e la prevenzione delle collisioni in volo.

## 3. La specializzazione

**In breve.** Restano identici la griglia, la regola «si muove», il filtro e gli stati della traccia. Cambiano il montaggio, la fascia di guardia (per classe) e il canale d'uscita. Si aggiungono la maschera del veicolo, il messaggio per settori, la causa «collegamento» e la richiesta di comportamento prudente. La tabella blocco per blocco è nell'allegato C.

### 3.1 Il messaggio per settori, verso l'autopilota [inf.: nuovo, non provato]

Gli autopiloti aperti ricevono, per settore angolare, una distanza oppure «nessun ostacolo fino alla portata» oppure «sconosciuto» (Q §2e, S23). Proposta: settori di 5° negli 87° della camera, fra 1,24 e 3 m. Sotto 1,24 m il messaggio tace, e lo si dichiara all'avvio: **un veicolo in moto dovrebbe coprire quel vuoto con un altro sensore.**

**Regola unica:** per ogni settore si misura **quanto si estende il «libero» osservato, da 1,24 m in fuori**, nella direzione peggiore.

- estensione nulla (prima cella non libera; settore fuori campo o mascherato; affidabilità persa) → **sconosciuto**: nessun moto in quella direzione;
- fino a d, minore di 3 m → **distanza valida d**: non oltre d;
- fino a 3 m, tutta fresca → **nessun ostacolo fino alla portata**: mai «via libera», perché oltre non si sa.

Che cosa ferma l'estensione, per ciascuno dei quattro stati della griglia e per la «possibile presenza»:

- **libero** (con la sua età): l'estensione continua;
- **occupato**, osservato o ricordato: d è la distanza della cella; l'età va solo allo schermo;
- **in ombra**: sta dietro un «occupato», quindi d è già fissata;
- **possibile presenza** (con la fascia): d è il bordo vicino della fascia, **finché dura l'avviso**;
- **non osservato**, o buco nei dati: d è l'inizio della cella; se è la prima, «sconosciuto».

«Ostacolo a d» e «oltre d non so» danno lo stesso valore: per chi deve fermarsi è lo stesso, e la differenza resta sullo schermo. **Smentita:** un solo settore con un valore maggiore della distanza della sua prima cella non libera.

### 3.2 «Affidabilità persa» e la richiesta [inf.]

Il prototipo **chiede, non comanda**: l'uscita ha un campo «richiesta» che nessun veicolo esegue.

- **Sensore** (immagine mancante o ripetuta; celle valide sotto metà: V2): tutti i settori «sconosciuto»; richiesta: attesa, e avviso all'operatore.
- **Piattaforma mossa** (sensore inerziale oltre 0,5° o 5°/s: V2): tutti «sconosciuto»; richiesta: attesa, e ritarare il suolo.
- **Collegamento** (alla stazione manca un messaggio nuovo da più di 0,5 s): quadro in grigio con la sua età e «dati vecchi»; a bordo decide l'azione già configurata nell'autopilota (Q, S25).
- **Non è affidabilità persa** una traccia «perso» con possibile presenza: i settori tengono la distanza (§3.1); richiesta: verifica dell'operatore.

Gli 0,5 s sono presi per analogia da un autopilota aperto (Q, S18): per un collegamento sono **NV**. Una traslazione senza rotazione non fa scattare il sensore inerziale: **NV**.

### 3.3 Velocità massima, fascia e «previsto» per classe [inf.]

Nel nucleo lo spazio percorso mentre un «libero» invecchia deve stare nella fascia (V2 §3). Propongo: **fascia non minore del maggiore fra (0,20 m d'errore d'ombra + mezza larghezza dell'oggetto) e (velocità massima × età del «libero»)**.

| Classe | Velocità massima | Camera, 15 immagini/s (età 0,13 s) | LiDAR, 10 scansioni/s (età 0,2 s) |
|---|---|---|---|
| persona | 2,5 m/s (V2) | **0,40 m** (il nucleo) | 0,5 m |
| mezzo di piazzale, largo 2 m | 8 m/s (NV) | 1,2 m | 1,6 m |
| piccolo drone | 19 m/s (Q, S19) | 2,5 m | 3,8 m |

- **Alla scala della sala la demo vale solo per la classe «persona»:** una fascia di 1,2 m riempirebbe quasi tutta la zona, larga 1,76 m.
- **Alla scala del veicolo** (10–40 m) la fascia pesa poco, ma il «libero» invecchia di più: va rimisurato.
- **La durata del «previsto» non ha un valore proposto.** La regola (l'area probabile copre meno di metà della zona nascosta) non dipende dalla scala; nel nucleo dura 0,6–0,7 s (V2 §1). Per le classi veloci si riduce a un istante: resta «perso, possibile presenza».
- **Il piccolo drone come bersaglio non è coperto:** la griglia sta sul piano del suolo.

## 4. La demo: «sentinella uncrewed»

La piattaforma sorveglia il varco di un hangar; il portatile a lato è la stazione dell'operatore. **È un modello in scala:** attore entro 2,3 m e pannello da 1 m sono la scala della camera, la sola che ha retto alle prove (V2); il caso reale ha 10–40 m e un furgone al posto del pannello. Le distanze sono in scala, **le velocità no**.

| Atto | Nel racconto | Schermo dell'operatore | Messaggio per settori |
|---|---|---|---|
| 1. Campo mezzo coperto | la sentinella dice ciò che non vede | metà campo «non osservato» | quei settori: sconosciuto |
| 2. Ostacolo fermo oltre 1,1 m | una cassa lasciata nel varco | «occupato», con la distanza | distanza valida lì; altrove «nessun ostacolo fino alla portata» |
| 3. Attraversamento | una persona attraversa | traccia «osservato», in movimento; priorità di rischio di collisione; ritardo | la distanza cambia settore |
| 4. Dietro il pannello, con una seconda persona in vista | passa dietro un mezzo fermo | osservato → «probabile» per un attimo → «possibile presenza» con l'età → stessa identità | quei settori tengono la distanza del bordo della fascia: **mai «nessun ostacolo» a soggetto nascosto** |
| 5. Sosta; mano sul sensore; cavo di rete staccato | chi resta nascosto; il guasto; il collegamento | «perso: possibile presenza, può aver lasciato l'area»; «affidabilità persa»; quadro grigio con l'età | tutti sconosciuto; richiesta: attesa |
| 6. **Facoltativo, NON provato** | la piattaforma avanza piano su un carrello, o una riproduzione | la direzione futura: oggi, dopo 10° di rotazione, gli oggetti fermi risultano «in movimento» nel 96–100 % dei casi (V2 §6) | atteso: «affidabilità persa» se ruota |

**La stessa demo nel profilo assistivo:** gli atti 3–5 con i segnali sonori al posto dello schermo, a persona ferma.

## 5. La strada degli sviluppi

1. **Piattaforma in moto** (per i due profili: veicolo che avanza, sensore indossato). Riusa tutto il nucleo e il messaggio; aggiunge la posa e la compensazione del moto (`MOTO_PROPRIO.md`). **La sblocca:** ruotando di 10°, oggetti fermi dati «in movimento» in non più del 10 % dei casi (oggi 96–100 %) e nessun «libero» falso.
2. **Altri sensori nella stessa griglia.** Aggiunge, per sensore, il rumore e che cosa conta come «buco»: LiDAR per la portata, radar per la velocità, termico solo come etichetta (Q §2b). **La sblocca:** rumore misurato a 10–30 m, e le misure sugli elementi mobili e sulle interruzioni della visibilità (R1 e R3, allegato A) rifatte a quella scala con la fascia del §3.3.
3. **Più veicoli.** Riusa stato ed età della traccia (Q §3, S31); aggiunge riferimento e orologio comuni e una fusione prudente (Q, S36). **La sblocca:** due sensori fermi con viste incrociate: la zona nascosta a uno e vista dall'altro si libera cella per cella, senza un «libero» falso.

## 6. Che cosa dire e che cosa non dire alla giuria (mista)

**A chi non ha il contesto: quattro frasi.**

- *Il problema:* «Chi osserva con una macchina perde di vista le cose: una persona passa dietro un ostacolo, e il rischio è che il sistema si comporti come se non ci fosse più.»
- *Il principio:* «Il nostro sistema dice sempre in quale di tre condizioni si trova, cioè lo vedo, non lo vedo ma so dove può essere, non lo so, e non dichiara mai libero uno spazio che non ha guardato.»
- *Una prova:* «Al computer, in 400 passaggi dietro l'ostacolo per ogni configurazione, ha ritrovato la persona con la stessa identità ogni volta; e in dodici tentativi mirati di ingannarlo non ha mai dichiarato libero uno spazio non visto.» (V2 §1, §7)
- *Un limite:* «Finora è provato solo in simulazione, con il sensore fermo e alla scala di una stanza; non vede il vetro; non è un dispositivo di sicurezza né un dispositivo medico.»

**Al giurato della società: tre agganci.**

- *I sistemi uncrewed:* una sentinella ferma con operatore remoto, cioè osservazione e ispezione; lo stesso nucleo, con un altro profilo, è l'ausilio per persone non vedenti.
- *Un'uscita leggibile da due destinatari:* per l'operatore, tre stati con l'età del dato, come le tracce «in coasting» dei dati di sorveglianza (Q, S31); per l'autopilota, un valore per settore, in cui «sconosciuto» non è «libero»: è il principio con cui gli autopiloti aperti azzerano la velocità verso i settori senza dati (Q, S18).
- *La strada:* piattaforma in moto, altri sensori, più veicoli, ciascuna con la prova che la sblocca.

**Da non dire.**

- «Conforme a» o «compatibile con» una norma: nessuna è stata applicata.
- «Detect and avoid»: nelle norme è il traffico con equipaggio, a chilometri (Q §3). Dire «percezione per la navigazione sicura a corto raggio».
- «Validato su drone», «funziona in movimento», «dispositivo medico», «sostituisce il bastone»: nessuna prova lo sostiene.

**Ambito.** Osservazione, ispezione, navigazione sicura, orientamento assistito. Nessuna funzione d'ingaggio o di puntamento.

## Allegato A. Copertura dei requisiti della challenge nel caso uncrewed

Stati: **E** = ereditato dal nucleo (simulazione, sensore fermo); **N** = nuovo, non provato; **H** = non verificato fino all'hardware.

| Requisito | La misura del nucleo | Stato |
|---|---|---|
| R1 elementi mobili | resta, per la classe «persona» | E; mezzi e scala del veicolo: N |
| R2 ostacoli | resta; in più: la maschera non genera ostacoli | E; maschera N; H |
| R3 interruzioni della visibilità | resta, con **ostacolo fermo** | E; ostacolo mobile: non coperto |
| R4 osservato e incerto | resta; in più: mai «nessun ostacolo» in un settore a soggetto nascosto | E; messaggio N |
| R5 feedback tempestivo | cambia: entro 300 ms dalla prima immagine allo schermo e al messaggio | H; ritardo del collegamento NV |
| R6 affidabilità persa | resta (entro 1 s, 10 prove per causa); in più 10 stacchi del cavo | E; collegamento N |
| R7 bassa latenza | cambia: 150 ms (95° percentile) dalla cattura al messaggio a bordo; cade l'audio | non risolta nel nucleo; H |
| R8 sicurezza delle indicazioni | resta; in più la smentita del §3.1 | E; messaggio N. Vetro: smentito, limite dichiarato |

## Allegato B. Le nove regole fisse, nel linguaggio del dominio

**Identiche al nucleo:** 3 (nessun «osservato» senza misura), 6 (un'assenza si deduce solo dove la profondità è valida), 7 (la possibile presenza finisce solo guardando), 9 (niente grandezze non osservabili: nemmeno «intenzione» o «minaccia»).
**Riscritte:** 1. «Libero» solo dove il suolo è visto nelle ultime 3 immagini, con l'età, e solo se la classe più veloce ammessa non esce dalla fascia in quell'età. 2. Buco, fuori campo, oltre portata, vuoto vicino, ombra, **maschera del veicolo**: mai «libero», e nel messaggio mai «nessun ostacolo». 4. «Previsto» e «possibile presenza» mai su celle libere oltre la fascia **della classe**. 5. Nessun timer e nessun modello appreso produce un «libero», toglie un avviso, **stringe la fascia** o decide un allarme. 8. Ogni uscita, **compresi il messaggio per settori e ciò che arriva alla stazione**, porta il contatore d'immagine del sensore; senza dato fresco esce solo «affidabilità persa».
**Proposta nuova (`esperto-dominio-4`):** nessuna uscita è un comando al veicolo.

## Allegato C. La specializzazione, blocco per blocco

Ciò che la tabella non nomina resta identico al nucleo (V2 §2): la griglia, la regola «si muove», il filtro (i cui parametri valgono per la classe «persona»; per le altre NV).

| Blocco | Cambia | Si aggiunge |
|---|---|---|
| **B1** sensore e montaggio | il treppiede rappresenta l'albero del rover o l'appoggio del drone; quota NV | **maschera del veicolo:** le celle coperte da parti della piattaforma sono «non osservato» [inf.] |
| **B5** stati della traccia e strato di garanzia | **fascia di guardia per classe** (§3.3); **ostacoli che nascondono: solo fermi** | — |
| **B6** etichetta (rete a lato) | classi persona / mezzo / altro (NV) | la classe **non stringe mai** la fascia [inf.] |
| **B7** decisione | «gravità» diventa **priorità di rischio di collisione** | **messaggio per settori** (§3.1) |
| **B8** uscita | la voce diventa lo **schermo dell'operatore** | causa «collegamento»; **richiesta** di comportamento prudente (§3.2) |
| **B9** demo | il racconto (§4) | sesto atto facoltativo |
