# MoVi, video di presentazione: messaggio e arco narrativo (preproduzione)

`sciame-comunicazione` (scheda 54), f17-video/10-messaggio. Cominciato il 2026-11-15T00:22:39+01:00.
Ci sono due file accanto, pronti per Kokoro: `voce_en.txt` (bm_george) e `voce_it.txt` (im_nicola). Un paragrafo
corrisponde a una scena. Sono gli stessi testi delle tabelle del §4.

## 0. Cambi di stato e regole violate

- **Regola violata, poi corretta:** per contare le parole avevo scritto in `voce_en.txt` e `voce_it.txt` due cifre
  di comodo («999 su 1000», «zero su mille»). Le ho sostituite con i segnaposto un minuto dopo. Nessuna cifra
  inventata è rimasta nei file. Lo scrivo perché quei file vanno alla voce sintetica.
- **Non verificato:** le durate. Le ho stimate con le misure di `00-strumenti/STRUMENTI.md`: bm_george a velocità
  1.0 fa 129 parole al minuto, im_nicola 135. Non ho generato l'audio. Prima del montaggio bisogna misurarlo con
  `tempi.json`.
- **Dipendenze dal prototipo.** Secondo `40-eventi/02-regole` le regole EV-A…EV-E non sono ancora realizzate in
  `movi_lp.py`. Le scene 4–6 sono «Simulation» solo se il registro per fotogramma le contiene. Altrimenti sono
  «Schematic», e la voce non cambia. La corsa di decollo della scena 6 chiede la classe nuova `scene-dinamiche-3`.
  Senza questa classe la scena si gira con l'aereo in rullaggio: la frase diventa «An aircraft taxiing. An engine
  fails.»
- Non ho letto la proposta `.tex` né l'allegato: il nucleo a corto raggio viene dalle istruzioni dell'utente (§1, §5).
  Non ho usato la rete.

## 1. Il pubblico

| Chi | Che cosa sa | Con che cosa giudica | Che cosa gli serve dal video |
|---|---|---|---|
| Membri di una società di aerospazio e difesa | Tracciamento, coasting, fusione, radar e sezione radar; riconoscono subito una maturità gonfiata (`03-scenari` §4) | Onestà sul livello di maturità, aderenza alla traccia, idea nuova sopra cose note | Stati espliciti per traccia e per cella, degrado dichiarato, «simulato dalle schede» detto da noi |
| Esterni senza contesto tecnico | Niente | Chiarezza, utilità, se la storia regge | Tre risposte da ricordare, immagini che si capiscono senza voce |

Lo stesso discorso si legge su due livelli. La voce dice le tre risposte con parole comuni («I see it / I don't
see it, here is where it can be / I don't know»). Lo schermo dà al tecnico gli stati del registro (SEEN, NOT SEEN
FOR X s, UNRESOLVED TRACKS, EVENT: CONTACT · INFERRED) e la fonte di ogni cifra.

## 2. Il messaggio

**In una frase (EN).** *MoVi never calls a space empty unless it has looked: when an aircraft or a drone disappears
behind a hangar, in fog or in smoke, it keeps saying where it can be, and says when it can no longer be trusted.*

**IT.** *MoVi non dice mai vuoto uno spazio che non ha guardato: quando un aereo o un drone sparisce dietro un
hangar, nella nebbia o nel fumo, continua a dire dove può essere, e dice quando non ci si può più fidare di lui.*

**Le tre cose che il giurato deve ricordare**

1. **Tre risposte per ogni oggetto:** lo vedo; non lo vedo, ed ecco la zona dove può essere; non lo so. Ciò che non
   è osservato non è mai «vuoto». L'avviso di possibile presenza resta acceso finché un sensore non torna a guardare.
2. **Quando l'evento colpisce, lo dichiara:**
   - con la nebbia, «portata utile ridotta» e «ridondanza assente»;
   - con la fiammata, «affidabilità persa» per ogni sensore colpito;
   - con la collisione, un volume dei detriti che non si restringe da solo e un suolo che resta «non verificato»
     fino all'ispezione.
3. **Quanto è solido:**
   - tutto è in simulazione, con sensori modellati dalle schede tecniche pubbliche e nessun sensore fisico;
   - decidono regole scritte, non un modello appreso;
   - le cifre vengono dalle prove simulate e i limiti li diciamo noi, per primi.

Il pitch segue questo ordine: problema (scena 1), idea (2), come lavora (3), prova sugli eventi (4–6), limiti e
cifre (7), estensione (8), richiesta e chiusura (9). La «richiesta» è implicita: chiediamo che si giudichi il principio,
dichiarato al suo livello di maturità.

## 3. L'arco narrativo: nove scene, 172 s

Le etichette restano a schermo per tutta la durata della scena, in basso a destra: «Simulation» o «Schematic».
Le colonne «Parole» e «Voce stimata» si riferiscono all'inglese.

| # | Scena | Inizio–fine | Durata | Parole | Voce stimata | Etichetta | Che cosa capisce lo spettatore alla fine | Richiesta della traccia |
|---|---|---|---|---|---|---|---|---|
| 1 | **Il piazzale.** Hangar, due droni d'ispezione, aereo in rullaggio; vista divisa (a sinistra la verità, a destra ciò che il sistema dichiara). Un drone passa dietro l'hangar: a sinistra la sagoma è mangiata dal bordo, a destra il disco pieno diventa un anello vuoto con la zona tratteggiata e «NOT SEEN FOR 0.8 s» che sale | 0:00–0:12 | 12 s | 22 | 10 s | Simulation (scenario A1/A2) o Schematic | Un oggetto può sparire alla vista; la domanda è che cosa dice lo schermo | Interruzioni della visibilità; monitoraggio in ambienti aerospaziali |
| 2 | **L'idea.** Le tre risposte, una alla volta, sullo stesso drone: SEEN, NOT SEEN + zona, UNKNOWN; l'ombra dell'hangar a puntini «NOT OBSERVED», mai vuota; la banda POSSIBLE PRESENCE che resta | 0:12–0:38 | 26 s | 51 | 24 s | Schematic | Il sistema distingue ciò che ha visto da ciò che suppone, e l'avviso non si spegne da solo | Distinguere osservato e incerto; sicurezza delle indicazioni |
| 3 | **Molti sensori.** Pianta del sito: ventaglio del radar, coni di LiDAR e camere, icona schematica dei sensori cooperativi; ogni sensore disegna la sua ombra; un drone piccolo fuori dalla soglia del radar: «observed for an aircraft · not for a small drone» | 0:38–0:55 | 17 s | 32 | 15 s | Schematic | Nessun sensore copre da solo; il «non osservato» dipende dal sensore e dalla classe; il silenzio di chi non trasmette non prova niente | Rilevare elementi mobili e ostacoli |
| 4 | **Nebbia** (E3). La nebbia entra: i coni delle camere si accorciano, «USEFUL RANGE REDUCED · EO · multirotor», «NO REDUNDANCY · radar only»; poi il radar cade per 20 s: banda RELIABILITY LOST · RADAR, «WARNING NOT TIMELY · all classes»; la traccia del drone diventa anello vuoto con zona | 0:55–1:13 | 18 s | 33 | 15 s | Simulation (E3) o Schematic | Con il meteo il sistema dice quanto vede ancora e quando il suo avviso non arriverebbe in tempo | Segnalare la perdita di affidabilità; feedback tempestivi |
| 5 | **Collisione fra droni** (E1, con E5 come controllo a schermo). Due droni si avvicinano: «UNRESOLVED TRACKS»; contatto: «EVENT: CONTACT · INFERRED»; il volume dei detriti cresce attorno al punto, la persona sul piazzale (sagoma) riceve l'avviso; un drone cade dietro l'hangar: «NOT SEEN FOR X s», mai «gone»; a fine scena il piazzale «UNVERIFIED · POSSIBLE DEBRIS · clears by inspection» | 1:13–1:36 | 23 s | 44 | 21 s | Simulation (E1) o Schematic | Un evento improvviso diventa una zona dichiarata, che non si restringe da sola e che solo un'ispezione scioglie | Interruzioni della visibilità; tempestività; sicurezza delle indicazioni |
| 6 | **Avaria di un motore** (E2, con E4 se c'è tempo). Corsa di decollo; fiammata schematica (area bianca satura, senza fuoco realistico), fumo a trama; bande RELIABILITY LOST · EO · FLASH e RELIABILITY LOST · THERMAL · FLASH; l'aereo resta SEEN (radar); dietro il fumo «NOT OBSERVED · CLOUD»; pista a valle «UNVERIFIED · POSSIBLE DEBRIS»; il mezzo di servizio riceve «UNVERIFIED ZONE ON PATH» | 1:36–1:56 | 20 s | 39 | 18 s | Simulation (E2) o Schematic | Anche quando un sensore è accecato il sistema dice quale, e che cosa resta osservato da chi | Perdita di affidabilità; visibilità estremamente limitata |
| 7 | **Prima i limiti, poi le prove.** Fondo scuro; i limiti compaiono uno per riga, il più importante per primo; poi la catena (sensori → celle → tracce → regole → uscite) e due cifre con la loro origine | 1:56–2:30 | 34 s | 68 | 32 s | Schematic | Sa che cosa è provato, come e dove; i limiti non li scopre da solo | Prototipo; continuità percettiva; efficienza (cifra a schermo) |
| 8 | **Lo stesso nucleo.** La pianta del piazzale si rimpicciolisce fino alla scena a corto raggio: una persona dietro un ostacolo, una camera di profondità, le stesse tre risposte. Riga a schermo: «Also: a presence warning for a blind person · it does not replace a cane or a guide dog» | 2:30–2:41 | 11 s | 21 | 10 s | Schematic (o Simulation · ideal sensor, dai log della v1.0) | L'idea vale a ogni scala; c'è un secondo uso | Accessibilità; continuità |
| 9 | **Chiusura.** La frase del messaggio, il logo MoVi, il logo SDMs (disegnati da noi), i nomi; il perimetro a schermo: «Observes and warns · No output is a command · No engagement or pointing function» | 2:41–2:52 | 11 s | 22 | 10 s | — | Il nome, il gruppo, che cosa fa e che cosa non fa | — |

Totale: 172 s; 332 parole in inglese (le cifre lette contano 3 parole ciascuna); voce stimata circa 155 s più le
pause. L'italiano fa 358 parole, circa 159 s a 135 parole al minuto: entra, ma con meno margine (vedi §9).

## 4. Il testo della voce, inglese con l'italiano accanto

`/` è una pausa breve (circa 0,4 s), `//` una pausa lunga (circa 0,8 s). A schermo vanno al massimo 16 parole per
quadro, etichette escluse.

**Scena 1 · 0:00–0:12**

| EN (voce) | IT (traduzione fedele) |
|---|---|
| An apron. / A hangar. / Two inspection drones. / An aircraft taxiing. // One drone slips behind the hangar. // What should the screen say now? | Un piazzale. Un hangar. Due droni d'ispezione. Un aereo in rullaggio. // Un drone scivola dietro l'hangar. // Che cosa deve dire lo schermo, adesso? |

**Scena 2 · 0:12–0:38**

| EN | IT |
|---|---|
| MoVi declares what it has not observed. // For every object, one of three answers. / I see it. / I don't see it, and here is where it can be. / Or: I don't know. // What it has not observed, it never calls empty. / A possible-presence warning stays on until a sensor looks again. | MoVi dichiara ciò che non ha osservato. // Per ogni oggetto, una di tre risposte. Lo vedo. Non lo vedo, ed ecco dove può essere. Oppure: non lo so. // Ciò che non ha osservato, non lo dice mai vuoto. Un avviso di possibile presenza resta acceso finché un sensore non torna a guardare. |

A schermo, accanto alla zona e in una riga a parte (mai dentro la zona): «Zone precision: [CIFRA-S1] · its domain».

**Scena 3 · 0:38–0:55**

| EN | IT |
|---|---|
| Radar, LiDAR, visible and thermal cameras, and what aircraft and drones broadcast. / All simulated from public data sheets. // Each sensor has blind spots, and MoVi draws them. / A silent transmitter proves nothing. | Radar, LiDAR, camere visibili e termiche, e ciò che trasmettono aerei e droni. Tutto simulato dalle schede tecniche pubbliche. // Ogni sensore ha i suoi punti ciechi, e MoVi li disegna. Un trasmettitore che tace non prova niente. |

A schermo: «Small drone, radar: [CIFRA-S2] · for a radar cross-section of 0.01 m² (assumed)».

**Scena 4 · 0:55–1:13**

| EN | IT |
|---|---|
| Fog rolls in. // The cameras' useful range collapses, and MoVi says so, per sensor, per class. / Only the radar is left: no redundancy. // If the radar drops too: / reliability lost, / warning not timely. | Arriva la nebbia. // La portata utile delle camere crolla, e MoVi lo dice, sensore per sensore, classe per classe. Resta solo il radar: ridondanza assente. // Se cade anche il radar: affidabilità persa, avviso non tempestivo. |

A schermo: «EO, multirotor: [CIFRA-S3] in dense fog (calculation)».

**Scena 5 · 1:13–1:36**

| EN | IT |
|---|---|
| The fog lifts. / Two drones fly close. // Too close to separate: / unresolved tracks. / Then they touch. // Event: contact, / inferred. // A volume where debris can be, which never shrinks on its own, / and a warning to the person below. // The ground stays unverified until inspected. | La nebbia si alza. Due droni volano vicini. // Troppo vicini per separarli: tracce non risolte. Poi si toccano. // Evento: contatto, dedotto. // Un volume dove possono essere i detriti, che non si restringe mai da solo, e un avviso alla persona sotto. // Il suolo resta non verificato finché non è ispezionato. |

A schermo: «Event declared after [CIFRA-S4]» e, piccolo, «Control: drones 5 m apart, no contact · false events [CIFRA-S5]».

**Scena 6 · 1:36–1:56**

| EN | IT |
|---|---|
| An aircraft on its take-off run. / An engine fails. // The flash blinds the cameras: / MoVi marks them unreliable. / The radar alone still sees the aircraft. // Behind the smoke: not observed. / Downstream: unverified, possible debris. / The service vehicle is warned. | Un aereo in corsa di decollo. Un motore ha un'avaria. // La fiammata acceca le camere: MoVi le dichiara non affidabili. Il solo radar vede ancora l'aereo. // Dietro il fumo: non osservato. A valle: non verificato, possibili detriti. Il mezzo di servizio riceve l'avviso. |

A schermo: «Reliability lost in [CIFRA-S6]» e, obbligatoria, «Radar response to the flash: not verified».

**Scena 7 · 1:56–2:30**

| EN | IT |
|---|---|
| First, the limits. // Everything you saw is simulated, from public data sheets. / No physical sensor. / Object classes are labelled by hand. / [STATO-1: The full chain has not yet run end to end.] // What holds: / written rules decide, not a trained model. / In simulation, [CIFRA-V1 k] of [CIFRA-V1 n] simulated fragments stayed inside the declared volume. / Tracks lost without a warning: [CIFRA-V2 k] of [CIFRA-V2 n]. | Prima, i limiti. // Tutto ciò che avete visto è simulato, dalle schede tecniche pubbliche. Nessun sensore fisico. Le classi degli oggetti sono etichettate a mano. [STATO-1: La catena intera non è ancora stata eseguita dall'inizio alla fine.] // Che cosa regge: decidono regole scritte, non un modello addestrato. In simulazione, [CIFRA-V1 k] frammenti simulati su [CIFRA-V1 n] sono rimasti dentro il volume dichiarato. Tracce perse senza avviso: [CIFRA-V2 k] su [CIFRA-V2 n]. |

A schermo, una riga per limite:
- «Simulation only · sensors from data sheets · no physical sensor»;
- «Classifier: required, simulated with hand labels»;
- «Reaction times: assumptions»;
- «Outside the model: fragments faster than assumed can leave the volume»;
- «[CIFRA-S7] per cycle · total delay [STATO-2]».

**Scena 8 · 2:30–2:41**

| EN | IT |
|---|---|
| The core is the one of our short-range version: / a person behind an obstacle, / a depth camera, / the same three answers. | Il nucleo è quello della nostra versione a corto raggio: una persona dietro un ostacolo, una camera di profondità, le stesse tre risposte. |

Il secondo uso va a schermo, non in voce, come nelle istruzioni dell'utente (D4). Se la squadra lo vuole anche in
voce, la frase è «It can also warn a blind person of a presence.» / «Può anche avvisare una persona non vedente di
una presenza.» (+10 parole, circa 4,5 s, da togliere alla scena 7).

**Scena 9 · 2:41–2:52**

| EN | IT |
|---|---|
| MoVi. // It never calls a space empty unless it has looked. // It observes and warns. / No output is a command. // By SDMs. | MoVi. // Non dice mai vuoto uno spazio che non ha guardato. // Osserva e avvisa. Nessuna uscita è un comando. // Di SDMs. |

Pronuncia di «MoVi»: [DA FORNIRE dalla squadra]. Per Kokoro va provata la grafia «Movee» (non verificato).
«SDMs» si legge lettera per lettera, «S-D-M-s» (da provare).

## 5. I segnaposto: quale misura serve

Tutte le misure vengono dal verdetto (`30-verdetto/VERDETTO_FASE2.md`), con la loro origine. Il «valore candidato»
è ciò che oggi sta nei file della fase 2: non entra nel video finché il verdetto non lo conferma.

| Segnaposto | Misura richiesta | Scena, dove | Valore candidato e stato |
|---|---|---|---|
| CIFRA-V1 | Quota di frammenti simulati rimasti dentro il volume dichiarato V(τ), scenari E1 ed E2 nominali (k su n, frammenti oppure campioni temporali: dire quale) | 7, voce | 0 campioni fuori su 1 131 692 nei casi conformi (`40-eventi/02-regole` §3, simulazione nel modello; stesso autore della prova) |
| CIFRA-V2 | Tracce rimaste senza avviso dentro una nube, dietro un ostacolo o dopo un evento, E1–E4 (k su n, con n dichiarato) | 7, voce | Nessuno: gli scenari non sono ancora stati eseguiti |
| STATO-1 | Se la catena intera (sensori simulati → regole → uscite) è stata eseguita dall'inizio alla fine | 7, voce | Oggi no: la frase predefinita dice «not yet» |
| CIFRA-S1 | Precisione dichiarata della zona: copertura della regione al livello 0,90 per classe e orizzonte, con il dominio | 2, schermo | Limite inferiore di Wilson peggiore 0,8703 sul generatore (`04-moto` §3): verifica la procedura, non il mondo |
| CIFRA-S2 | Distanza di primo rilevamento di un drone piccolo con il radar, con la sezione radar ipotizzata | 3, schermo | 3,1 km per 0,01 m² (`02-sensori` §2, calcolo da scheda con ipotesi) |
| CIFRA-S3 | Portata utile della camera EO per un multirotore con nebbia fitta (e con pioggia forte) | 4, schermo | 2000 m con il sereno, 23 m con nebbia fitta, 526 m con pioggia forte (`40-eventi/02-regole` EV-D, calcolo con fattori prudenti) |
| CIFRA-S4 | Ritardo fra il contatto e «evento: contatto (dedotto)» in E1 (mediana e massimo) | 5, schermo | Attesa ≤ 2 s: è una soglia, non un risultato |
| CIFRA-S5 | Falsi eventi nel controllo E5 (k su n ripetizioni) | 5, schermo | Soglia: 0 su 1000; nessun risultato |
| CIFRA-S6 | Cicli fra la fiammata e «affidabilità persa» per EO e termica in E2 | 6, schermo | Soglia ≤ 3 cicli; nessun risultato |
| CIFRA-S7 | Tempo di calcolo per ciclo del prototipo a lunga portata, con la macchina | 7, schermo | Nessuno |
| STATO-2 | Ritardo totale: misurato o no | 7, schermo | Oggi «not measured» |

Se una cifra non arriva, la frase che la contiene si toglie. Non la si sostituisce con un aggettivo. Se manca
CIFRA-V2, la scena 7 chiude su V1 e guadagna circa 4 s. Se mancano sia V1 sia V2, al loro posto si dice: «The test
scenarios are written; their results are pending.» / «Gli scenari di prova sono scritti; i risultati sono in corso.»

## 6. Le parole fisse a schermo, inglese e italiano

I nomi dei campi sono quelli del registro (`ARCHITETTURA.md`, `04-moto` §5, `40-eventi`). La traduzione è
vincolante: voce, schermo e sottotitoli usano la stessa forma.

| Registro (IT) | A schermo (EN) | In voce (EN) |
|---|---|---|
| vista | SEEN · ID | «I see it», «sees» |
| non vista da X s, con zona | NOT SEEN FOR X s | «here is where it can be» |
| previsto ampio | WIDE ZONE | «the zone widens» |
| possibile presenza | POSSIBLE PRESENCE | «possible-presence warning» |
| ricomparsa, identità presunta | SEEN AGAIN · IDENTITY ASSUMED | — |
| non osservato (causa) | NOT OBSERVED · cause | «not observed» |
| zona non verificata | UNVERIFIED ZONE | «unverified» |
| libero (solo dove il registro lo dichiara) | OBSERVED EMPTY · class | «observed empty», mai «empty» da solo come stato |
| affidabilità persa | RELIABILITY LOST · sensor · cause | «reliability lost» |
| portata utile ridotta | USEFUL RANGE REDUCED | «useful range» |
| ridondanza assente | NO REDUNDANCY | «no redundancy» |
| avviso non tempestivo per classe | WARNING NOT TIMELY · class | «warning not timely» |
| tracce non risolte | UNRESOLVED TRACKS | «unresolved tracks» |
| evento: contatto / separazione (dedotto / osservato) | EVENT: CONTACT · INFERRED | «event: contact, inferred» |
| possibili detriti; ispezionata da operatore | POSSIBLE DEBRIS; INSPECTED BY OPERATOR | «until inspected» |
| etichette a mano | HAND LABELS | «labelled by hand» |

## 7. Le frasi che non si dicono

Valgono in voce, a schermo, nei sottotitoli e nei nomi dei file mostrati.

| Non dire (EN / IT) | Perché | Si dice |
|---|---|---|
| validated, certified, compliant with, guaranteed / validato, certificato, conforme, garantito | Niente è provato su un sensore fisico | «in simulation», «by calculation», «inspired by» |
| detect and avoid, DAA, ACAS, TCAS, A-SMGCS, RA, TA | Promettono una funzione e una norma che non abbiamo | «monitoring and warning» |
| threat, target, hostile, intruder, engage, intercept, neutralise, counter-drone, C-UAS, site defence / minaccia, bersaglio, ingaggio | Lessico d'ingaggio: è osservazione | «object», «track», «uncrewed aircraft detection and warning» |
| sees through smoke / fog | Falso: il radar continua a dare ritorni dietro il fumo nel modello, e l'effetto della fiammata sul radar non è verificato | «the radar alone still sees the aircraft» (riferito a E2, con la riga «not verified») |
| predicts where it will be, knows where it is / prevede dove sarà | La zona è una regione dichiarata, non una posizione | «here is where it can be» |
| lost, gone, probably / perso, probabile (come stati) | Il segno non sparisce mai | «not seen for X s», «wide zone» |
| clear, all clear, free, safe to proceed, go / libero, via libera | È la promessa che MoVi rifiuta; niente verde, spunte, frecce | «observed empty», solo dove il registro lo dichiara |
| in real time, low latency (come risultato) | Il ritardo totale non è misurato | «[CIFRA-S7] per cycle; total delay not measured» |
| covers the airspace, detects every drone; una portata senza la sezione radar | Gonfia la maturità; la portata dipende dalla classe | «for a radar cross-section of 0.01 m² (assumed)» |
| the AI decides, the network recognises | Decidono regole scritte; il classificatore è simulato | «written rules decide; classes are labelled by hand» |
| revolutionary, unique, game changer, 100 % safe, market, billions | Retorica senza prova | — |
| Nomi commerciali dei sensori (le schede di `02-sensori`), loghi, livree | Diritti di terzi | il sensore si nomina come classe («drone radar», «long-range LiDAR»); la fonte va nella riga in piccolo, se serve |

**Il mezzo che porta il sensore.** Nel video ogni sensore sta a terra, su un palo o su un edificio. Droni e aerei
sono oggetti osservati, mai piattaforme del sistema. Se una frase nomina un sensore a bordo di un drone o di un aereo
(lo scenario A4 di `03-scenari`), dice anche «analysis only, not simulated» / «solo analisi, non simulato».

**Immagini.**
- Gli incidenti si mostrano come eventi tecnici schematici: area satura per la fiammata, trama per il fumo, punti per
  i frammenti.
- Niente fuoco realistico, niente sangue, niente vittime, niente volti. Le persone sono sagome grigie.
- Niente mirini, reticoli di puntamento, «lock», cerchi rossi attorno a un aereo.
- Niente ologrammi né «scansioni».

## 8. Come si dicono l'incertezza e i limiti senza indebolire il messaggio

1. **L'incertezza è il prodotto, non il suo difetto.** MoVi esiste per dire ciò che non sa. Ogni «not seen», «wide
   zone», «reliability lost» è una funzione mostrata, non una scusa. La voce li dice con lo stesso tono asciutto di
   «I see it». Il registro non cambia né per gravità né per modestia.
2. **Il limite lo diciamo noi, per primi.** La scena 7 apre con «First, the limits», prima delle cifre: la giuria del
   settore lo ascolta come competenza. Il limite che cambia il giudizio (tutto simulato, nessun sensore fisico)
   compare tre volte:
   - in voce nella scena 3;
   - in voce nella scena 7;
   - a schermo per tutta la durata, con l'etichetta «Simulation» o «Schematic».
3. **Ogni cifra con la sua forza.** «In simulation» per ciò che è misurato su scenari simulati, «by calculation» per
   le portate dalle schede, «assumed» per le ipotesi (la sezione radar, i tempi di reazione). Mai «proven» per un
   calcolo. Il dominio sta sulla riga sotto la cifra, non in una nota finale.
4. **Una cifra per frase, letta per intero.** «[k] of [n]», non percentuali arrotondate: il conteggio fa capire
   anche al non tecnico che si è contato.
5. **Limite e forza nella stessa frase, quando sono la stessa cosa.** Il volume dei detriti è largo perché è
   prudente: «which never shrinks on its own». Il suolo non si libera da solo: «until inspected». Sono limiti di
   utilità e garanzie di sicurezza insieme, e così si dicono.
6. **Ciò che è semplificato lo dichiariamo.** Le immagini sono schemi: lo dice l'etichetta. La voce non nomina la
   fisica del modello (punto materiale, vento costante). A schermo resta la riga «Outside the model: fragments faster
   than assumed can leave the volume».
7. **Niente aggettivi al posto delle cifre mancanti.** Se una cifra non arriva, si toglie la frase (§5).

## 9. Domande attese e risposte oneste

| Domanda | Risposta |
|---|---|
| «Qualunque tracciatore fa coasting. Che cosa c'è di nuovo?» | Il coasting stima e poi cancella. MoVi dichiara lo stato all'operatore, la cancellazione non diventa mai «vuoto», e l'avviso si spegne solo se un sensore riguarda. A questo si aggiungono gli eventi: frammentazione, nube, abbagliamento. |
| «Avete provato su un sensore vero?» | No. Tutto è simulato dalle schede e dai dati pubblici. Il passo dopo è rifare gli stessi scenari su registrazioni vere. |
| «Il volume dei detriti non è inutilmente grande?» | Sì, è largo: nel caso nominale fa da 1,9 a 5,2 volte la gittata simulata. È il prezzo della prudenza. Esiste una variante più stretta, con un'ipotesi in più (`40-eventi/02-regole` §3). |
| «E un frammento più veloce di quanto avete ipotizzato?» | Esce dal volume: è un controesempio scritto. Va rivisto con un esperto di frammentazione. |
| «Uno stormo di uccelli fa scattare l'evento?» | Può dare una falsa «separazione»: è un controesempio noto, ed E5 misura i falsi eventi [CIFRA-S5]. |
| «È un sistema anti-drone?» | No. Osserva e avvisa: nessuna uscita è un comando, nessuna funzione d'ingaggio o di puntamento. |

## 10. Se il tempo si dimezza (86 s), o se la voce sfora

**Ordine dei tagli se la voce misurata sfora:**
1. il secondo uso in voce, se c'è;
2. nella scena 3, «A silent transmitter proves nothing» (passa a schermo);
3. nella scena 6, la frase sul mezzo di servizio;
4. nella scena 5, «The fog lifts» (resta un cambio d'immagine);
5. nella scena 8, la voce intera (resta l'immagine con una riga a schermo).

Non si accelera la voce oltre 1.0. La scena 7 non si taglia mai.

**Versione a 86 s:** scene 1, 2 (accorciata a «three answers» e «never calls empty»), 5, 7 (limiti e una cifra), 9.
La nebbia e la fiammata restano un quadro di 3 s ciascuna dentro la scena 5, senza voce.

**Italiano:** con im_nicola a 135 parole al minuto le 358 parole fanno circa 159 s, più le pause. Probabilmente
sfora: si applicano subito i tagli 2 e 3 dell'elenco (non verificato finché non si genera l'audio).

## 11. Stati proposti, proposte, che cosa viene dopo

**Stati.**
- Il messaggio e l'arco sono una proposta di comunicazione, senza prova. Li decide la lettura a voce alta con il
  cronometro e una visione con almeno un non tecnico.
- Le durate sono stimate, non misurate.
- Le cifre sono tutte segnaposto.
- Ogni «valore candidato» del §5 ha lo stato del file da cui viene.

**`comunicazione-1` · Prova del primo ascolto.**
- *Meccanismo:* la frase «three answers» è l'unica astrazione del video, e le scene 4–6 la ripetono con gli stati.
- *Previsione:* almeno 4 spettatori non tecnici su 5, dopo una visione senza pause, ripetono a parole loro le tre
  risposte e il fatto che tutto è simulato.
- *Smentita:* 2 o più spettatori su 5 non le ripetono. In quel caso la scena 2 si rifà prima del montaggio.

**`comunicazione-2` · Il limite prima delle cifre.**
- *Previsione:* un giurato tecnico giudica più credibile la scena 7 con «First, the limits» in apertura che la
  versione con le cifre prima.
- *Smentita:* il confronto A/B con due lettori critici dà il risultato opposto.

**Dopo.**
- Il videomaker misura la voce generata con `tempi.json` contro la colonna «Voce stimata» del §3.
- Il verdetto riempie il §5.
- Il lettore critico controlla il testo con l'elenco del §7.
- La squadra fornisce la pronuncia di «MoVi».
