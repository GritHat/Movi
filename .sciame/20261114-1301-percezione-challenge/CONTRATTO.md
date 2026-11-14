# Contratto della convocazione percezione-challenge

Strategia: classica. Creato: 2026-11-14T13:01:29+01:00.

## Domanda

Quale architettura di prototipo (sensori, percezione, stima e tracciamento, decisione, feedback) soddisfa meglio i requisiti della challenge in regole_challenge.md ed è realizzabile e dimostrabile in un hackathon?

## Criterio

La risposta è buona se passa questi quattro controlli (sono controlli, non meccanismi: nessuna tecnica è data per buona in partenza).
1. **Copertura delle regole.** Ognuno dei requisiti della challenge è coperto da un componente nominato e da una verifica di accettazione misurabile e mostrabile in una demo:
   - R1 rilevare elementi mobili;
   - R2 rilevare ostacoli;
   - R3 gestire le interruzioni della visibilità (un ostacolo nasconde il soggetto mentre la scena cambia): continuità percettiva;
   - R4 distinguere le informazioni osservate da quelle incerte (previste, non osservate);
   - R5 dare feedback spaziali chiari e tempestivi quando le condizioni lo consentono;
   - R6 segnalare la perdita di affidabilità quando serve;
   - R7 bassa latenza ed efficienza elaborativa;
   - R8 sicurezza delle indicazioni (mai dichiarare libero o sicuro ciò che non è osservato).
2. **Resistenza.** Ogni scelta fondante (sensori, rappresentazione della scena, stimatore e tracciatore, modello di riconoscimento, logica di decisione e feedback) ha retto a un tentativo concreto di controesempio dell'avversario, e le alternative scartate hanno un motivo scritto.
3. **Fattibilità.** Il prototipo si può costruire e dimostrare in un hackathon. IPOTESI DICHIARATA, non verificata (la decide l'utente): 24–48 ore, squadra di 3–5 persone, hardware commerciale reperibile subito (ordine di poche centinaia di euro) o già posseduto, calcolo su portatile con o senza GPU o su una scheda tipo Jetson o Raspberry Pi. Ogni proposta dice che cosa cambia se l'ipotesi è falsa.
4. **Fonti.** Ogni affermazione sullo stato dell'arte (modelli, sensori, dataset, prestazioni) porta la fonte con il link, controllata in rete quando lo strumento c'è; altrimenti porta la dicitura «non verificato». La data di oggi è il 14 novembre 2026: non fidarti della memoria per ciò che è recente.

## Ingressi

- **Le regole della challenge** (testo integrale, è la fonte dei requisiti R1–R8): `/home/fede/Scrivania/ed/GitHub/Movi-Hackthon/regole_challenge.md` (6 righe).
- **La bozza iniziale della squadra** (una lunga conversazione con un assistente, 3800 righe; è un'idea possibile, non un vincolo): `/home/fede/Scrivania/ed/GitHub/Movi-Hackthon/bozza_iniziale/Proposta MLE Matrice Bayesiana (1).md`. La parte più utile è la specifica finale alle righe 1998–2945 («Adaptive Spatio-Temporal Risk Mapping»: navigazione assistiva per non vedenti, RGB-D + IMU, Rolling Occupancy Grid 2.5D in log-odds, Kalman per traccia, classificazione asincrona e gerarchica, MLE/MAP, rischio di collisione, feedback aptico e vocale); le righe 2950–3800 aggiungono albero gerarchico probabilistico, IMM e coerenza fra percorso critico e semantica. Leggila a pezzi, non tutta.
- **La richiesta dell'utente, per intero:** «utilizzando lo sciame con la strategia di convocazione che ritieni più opportuna, analizza il contenuto dei file .md nella cartella bozza_iniziale e sulle regole delineate nel file regole_challenge.md, per il problema proposto nella challenge. Che sia validato e sul quale lo sciame converga. fai un breve pdf di massimo 2 pagine che indichi le idee definite. La nostra idea alla base è usare 3 sensori ToF per coprire 360 gradi di visione e mappare il terreno e i gradi di libertà sia dell'utente che degli ostacoli, che poi dovranno anche essere classificati e per i quali bisognerà anche fare stime su massa, velocità e accelerazione, con previsioni della posizione nel momento in cui si perdano di vista. Un filtro di Kalman applicato poi passerà i dati a un vision trasformer o simili e poi un decision model scegliera cosa fare. Usa i dettagli appena forniti e quelli nei file .md solo come idea possibile, ma valuta qualunque opportunità nello stato dell'arte della computer vision per ottenere lo scopo desiderato, con tutte le possibili proposte dello sciame.»
- **L'idea di partenza della squadra, in punti** (ipotesi da vagliare, non vincolo): (a) 3 sensori ToF per 360° di visione; (b) mappa del terreno e dei gradi di libertà dell'utente e degli ostacoli; (c) classificazione degli ostacoli; (d) stime di massa, velocità e accelerazione degli ostacoli; (e) previsione della posizione quando si perdono di vista; (f) catena filtro di Kalman → vision transformer o simili → decision model.

## Vincoli

- L'idea di partenza e la bozza sono dati da vagliare: si possono confermare, correggere o sostituire, sempre con il motivo e la prova.
- Va considerato tutto lo stato dell'arte utile allo scopo (sensori di profondità e non, rilevamento e segmentazione, tracciamento attraverso le occlusioni, stima dello stato, modelli di fondazione, mappe di occupazione, previsione, incertezza calibrata, feedback), non solo ciò che la bozza nomina.
- La challenge ammette due applicazioni: l'orientamento assistito di persone con disabilità visiva, oppure il monitoraggio di attività e oggetti in ambienti aerospaziali e industriali. La bozza ha scelto la prima; lo sciame può dire quale delle due dà la demo più forte, con il motivo.
- Una grandezza che i sensori proposti non possono osservare non si dichiara stimata: si dice che cosa è osservabile, con quale incertezza, e che cosa no.
- Sicurezza: l'assenza di rilevamento non è mai «via libera»; ciò che è previsto e non osservato va distinto in uscita da ciò che è osservato.
- La consegna finale all'utente è un PDF di al più due pagine: servono poche idee definite e difendibili, non un elenco.

## Esclusioni

- Niente codice del prototipo, niente acquisti, niente modifiche ai file del progetto: si decide l'architettura e come provarla.
- Niente prove di classe superiore alla 2 (a mano o su un caso piccolo; oracolo indipendente: schede tecniche, articoli, un calcolo o una simulazione numerica di pochi minuti su CPU). Niente GPU, niente servizi a pagamento, niente invii di dati a terzi.
- Il PDF lo compone il coordinatore dopo la chiusura.

## Quota

Al più 28 agenti e 90 minuti, in tre terzi: (1) fino a 18 agenti per f1, f2 e f3; (2) 6 per verdetto e risposta; (3) 4 di riserva per riprese e agenti fermati. Al più cinque agenti alla volta. Speso il primo terzo, si passa al verdetto con ciò che c'è.

## Profilo

percezione

## Principi del progetto

- Il criterio prima del meccanismo: nessuna tecnica entra nella soluzione perché è di moda o perché era nella bozza.
- L'incertezza si dichiara sempre: in uscita, «osservato», «previsto» e «sconosciuto» sono tre stati distinti.
- Il prototipo è un ausilio dimostrativo, non un dispositivo di sicurezza: non sostituisce bastone, cane guida o procedure di sicurezza industriale.
- La lingua è l'italiano.
