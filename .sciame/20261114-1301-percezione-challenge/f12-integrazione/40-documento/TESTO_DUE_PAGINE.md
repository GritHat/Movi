<!--
TESTO DEL DOCUMENTO DI DUE PAGINE — prima stesura dopo il verdetto d'integrazione (sciame-redattore, f12, 40-documento, 14 novembre 2026)
CONTEGGIO (wc -w, da «sh controlla.sh»): corpo 1279 (di cui 36 marche di stato e 43 segni di marcatura: circa 1 200 parole vere, contro le circa 1 100 chieste) · schema 172 · tabelle 333 · riquadro dei limiti 241 · file intero 2184 con questa intestazione. Lo spazio dato è superato: l'ordine dei tagli è in fondo a CIFRE.md.
Per chi impagina: il riquadro (righe che cominciano con «>») va in testa, o in un riquadro colorato che non si può saltare; lo schema è nel blocco di codice, una riga per blocco, poi le frecce; le tabelle sono due, di sei e di quattro righe.
Ogni cifra ha la sua riga in CIFRE.md, nella stessa cartella; in fondo a quel file le modifiche rispetto alla v0.8 e i dubbi per l'autore.
-->

# Un sistema che sa che cosa non vede

**Monitoraggio di attività e oggetti in ambienti aerospaziali e industriali.** Un prototipo progettato per rilevare elementi mobili e ostacoli, gestire le interruzioni della visibilità, distinguere l'osservato dall'incerto e segnalare la perdita di affidabilità [P]. Lo stesso nucleo, con un'altra uscita, avvisa una persona non vedente ferma [P].

**[S]** provato in simulazione · **[C]** per costruzione o per conto · **[P]** in progetto, non provato.

> **Limiti, da leggere per primi**
>
> - Nessun fotogramma di una nostra camera è passato da una prova. Tutto è provato al calcolatore, su profondità simulata dalle schede tecniche e su tracce pubbliche di persone, a sensore fermo, con una persona alla volta.
> - È un progetto di prototipo: le parti sono provate una per una, l'insieme non è mai stato eseguito.
> - Dominio: camera ferma a 1,2 m da terra, al chiuso, fino a 3 m; posa (posizione e inclinazione della camera) nota entro 0,5°; un ostacolo fermo che nasconde la persona per intero.
> - Non vede: il vetro e ciò che non rimanda segnale; il suolo a meno di 1,24 m davanti e di 1,7 m ai lati (1,22 m e 1,69 m con l'altra focale usata nei conti); la testa di una persona di 1,70 m a meno di 2,01 m; un ostacolo sospeso (sotto, il suolo risulta libero).
> - Non provati: due persone nella stessa ombra, un ostacolo che si sposta, il sensore in moto, il sole, ogni classe diversa da «persona a piedi».
> - Il classificatore è richiesto, non realizzato, non valutato: le etichette sono messe a mano.
> - Difetto aperto: tolto l'ostacolo, l'avviso resta acceso (10 prove su 10). Oggi si toglie riavviando.
> - Il sistema osserva e avvisa: nessuna uscita è un comando, nessuna funzione d'ingaggio o di puntamento. Non sostituisce bastone o cane guida.

## 1 · L'idea

Una persona passa dietro un mezzo fermo. Il rischio è che la macchina che osserva si comporti come se non ci fosse più. Di ogni cosa seguita il prototipo dice se **la vede**, se **non la vede ma indica una zona dove può essere**, o se **non lo sa** [P].

**Obiettivo principale: la continuità visiva.** Per tutta l'occlusione, cioè finché l'ostacolo nasconde la persona, lo schermo mostra a ogni fotogramma un segno e una zona, con una precisione dichiarata insieme al suo dominio [S, su sensore ideale].

**Principio di sicurezza.** Ciò che non è osservato non è mai dichiarato libero. L'avviso di «possibile presenza» non si toglie se non guardando [C].

## 2 · Come funziona

```
SCHEMA A BLOCCHI (una riga per blocco, poi le frecce)
B0  Configurazione all'avvio: classi ammesse nel sito; profilo di chi porta il sensore
B1  Sensore: camera di profondità frontale, ferma; controllo all'avvio
B2  Mappa del suolo a 4 stati: libero · occupato · in ombra · non osservato
B3  Rilevamento geometrico: gruppi di celle occupate; che cosa è mobile
B4  Inseguimento: associazione e filtro di Kalman
B5  Durante l'occlusione (blocco in evidenza): zona prevista, sempre · avviso di possibile presenza · riaggancio
B6  Regole: una tabella scritta, nessun modello appreso
B7  Uscita: schermo · segnali sonori brevi · registro degli eventi
B8  Salute del sensore: «affidabilità persa»
B9  Classificazione (a lato, tratteggiato): oggi etichette a mano
FRECCE PIENE: B0 -> B1 -> B2 -> B3 -> B4 -> B5 -> B6 -> B7 ; B2 -> B5 (ombra e «libero» del fotogramma) ; B8 -> B6 (scavalca tutto)
FRECCE TRATTEGGIATE: B4 -> B9 ; B9 -> B7 (testo sotto la traccia) ; B9 -> B5 (può solo allargare l'avviso: spento nel prototipo)
```

Una camera di profondità (misura la distanza di ogni punto) sta ferma, inclinata di 15° verso il basso. Ogni fotogramma diventa una mappa del suolo vista dall'alto, a celle di 1° × 0,1 m fino a 3 m, in quattro stati: libero, occupato, in ombra (dietro un ostacolo), non osservato. «Libero» si legge nel solo fotogramma corrente, senza memoria [C].

Un filtro di Kalman, che stima posizione e velocità, segue i gruppi di celle occupate. Quando una persona seguita entra in un'ombra nascono la **zona prevista**, ricavata da 400 percorsi registrati di persone (il ripiego, che entra per primo, è un disco a velocità costante, senza cifra), e l'**avviso**, che copre l'ombra più una fascia di 0,40 m. La zona sta dentro l'avviso; la previsione non lo restringe mai [C].

**Classificazione.** Il sistema richiede un classificatore su più classi (persone, veicoli di tipo diverso, altri ostacoli mobili), ciascuna con velocità, accelerazione e gradi di libertà. Qui nessun modello è in esecuzione: le etichette le mettiamo a mano [P]. Nessuna etichetta produce un «libero», toglie o restringe un avviso: può solo allargarlo [C; sulla sola fascia 0 violazioni su 20 000 sequenze, mai sulla catena intera]. Chi porta il sensore ha un profilo fisso, dichiarato all'avvio: velocità, tempo di reazione, frenata, gradi di libertà [P].

## 3 · La continuità visiva

**Che cosa si vede.** Persona visibile: disco pieno. Nascosta: anello vuoto e zona tratteggiata, con il tempo da cui non è vista. Oltre il limite della precisione dichiarata la zona diventa tutta l'ombra, «previsto ampio»: il segno non sparisce [C]. Al ritorno: «ricomparso · identità presunta» [P].

**La cifra e il suo dominio.** In simulazione, su sensore ideale: 0 interruzioni su 23 402 passaggi, meno di 6,4 su 10 000 [S]. Con un ostacolo largo 2 m, il bordo dell'ombra noto e la persona sul proprio percorso, finché resta nascosta è dentro la zona in almeno 9 casi su 10 fino a 2 s e in almeno 85 su 100 fino a 3 s [S]. Con il pannello da 1 m della demo: almeno 87 su 100 a 1 s; poi lo schermo dice che è ancora dietro, senza una cifra [S].

**Dove cede.** Chi svolta o esce dal lato lontano: 6–8 casi su 10 [S]. Bordo dell'ombra stimato, non noto: 3–5 su 10 a 1 s [S]. Chi parte da fermo, due persone, oltre 3 s: nessuna cifra. In questi casi resta l'avviso [C]. Persona persa di vista prima dell'ostacolo: l'avviso può non nascere (24 passaggi su 23 402) [S]. **Sulla profondità simulata la regola non è ancora innestata:** lì, a persona nascosta, la traccia non è nello stato «previsto» in 2 983 fotogrammi su 4 552 [S]. È la prima prova da fare.

## 4 · Che cosa è provato, e come

1. [S] «Suolo visto libero» non è mai uscito sopra un ostacolo (300 condizioni, 9 000 fotogrammi, due lanci, camera ideale). Con 1° d'errore d'inclinazione cede.
2. [S] Su profondità simulata, una persona nascosta entro 3 m non è mai rimasta senza avviso (0 fotogrammi su 4 324; 0 su 3 608 in una replica). Il costo: dietro un ostacolo fermo l'avviso resta acceso.
3. [S] Il nome al ritorno è sempre «presunto». Coi parametri di partenza reggeva 0 volte su 90; con la correzione 176 su 180 (94–99 %), solo per un adulto, da solo, a 0,5 m dal pannello, entro 2,6 m. Un'altra persona che esce dalla stessa ombra prende il nome (19 volte su 20); l'avviso resta.
4. [S] Su tracciati pubblici di 9 persone vere (cattura del moto, non una camera) il filtro copre la persona nel 98–100 % dei casi fino a 3 s.
5. [C] I 3 m di portata bastano ad avvisare in tempo chi si avvicina fino a 1,44 m/s (reazione di 1 s: ipotesi): il passo normale sì; veicoli, treni e aerei no. La fascia di 0,40 m copre chi è nascosto fino a 1,13 m/s.

## 5 · Che cosa abbiamo scartato, e perché

- **Tre sensori a tempo di volo per 360°.** Coprono 180° (scheda del costruttore) [C].
- **Stimare massa e accelerazione.** Da queste misure non si ricavano [C]. Con le classi entrano solo come intervalli a priori.
- **Catena filtro → rete → decisione.** Il filtro consuma misure, non le produce. Ordine adottato: rilevamento → associazione → aggiornamento del filtro → regole [C].
- **Mappa di volume a cubetti (voxel).** A sensore fermo non dà più del fotogramma corrente; le varianti che ricordano un «libero» sbagliano: 80 505 falsi su 146 901 [S].
- **Due ipotesi di moto con pesi.** Danno per ferma una persona che transita, nel 38–100 % dei transiti [S].

## 6 · I requisiti della traccia, uno per uno

| La traccia chiede | Che cosa fa il prototipo | Stato |
|---|---|---|
| Rilevare elementi mobili e ostacoli | Gruppi di celle occupate; «mobile» chi si sposta | [S] scatola di 15 cm a 2 m: 10 su 10. Pannello fermo dato per mobile 79 volte su 90; 0 su 140 con la correzione, nel suo dominio |
| Gestire le interruzioni della visibilità; continuità percettiva | Zona a ogni fotogramma; avviso sull'ombra | [S] su sensore ideale; [P] su profondità |
| Distinguere l'osservato dall'incerto | Disco pieno solo con una misura; zona tratteggiata con l'età; registro «osservato» o «dedotto» | [C] regole di disegno; [P] registro mai eseguito |
| Feedback chiari e tempestivi; latenza; efficienza elaborativa | Un livello per settore: «attenzione», «zona non verificata», «suolo visto libero da 1,3 m a d m» | [S] calcolo: 6 ms per ciclo in media su scene simulate, 81 ms su una registrazione vera affollata; [P] ritardo non misurato; nessuna prova con persone |
| Segnalare la perdita di affidabilità | Controllo all'avvio; segnale se il sensore è coperto, urtato o fermo | [S] segnale in 0,13 s; [P] su una camera |
| Sicurezza delle indicazioni | Mai «libero» il non osservato; l'avviso non si toglie se non guardando | [C] a posa nota entro 0,5° e se l'ostacolo rimanda segnale |

## 7 · Un nucleo, più profili

| | Monitoraggio di un varco o di un'area di lavoro | Avviso di presenza per una persona non vedente ferma |
|---|---|---|
| Dove sta il sensore | Stazione fissa, o veicolo senza equipaggio fermo | Treppiede accanto alla persona |
| Uscita | Schermo e registro per l'operatore. Messaggio per settori verso un autopilota: [P], mai generato | Segnali sonori di 0,3 s: [P], mai provati con persone |
| Se l'affidabilità cade | Lo dichiara; i settori dicono «zona non verificata» | Segnale dedicato; la persona torna al bastone |
| Non provato | Sensore in moto, oltre 3 m, esterni | Persona che cammina |

**Identico nei due profili:** le tre risposte su ciò che è seguito, i quattro stati della cella, il principio di sicurezza, quattro regole su nove [P].

## 8 · La demo

Cinque atti in cinque minuti: (1) pavimento vuoto; (2) una persona passa dietro il pannello: disco, poi anello e zona, poi «ricomparso»; (3) resta dietro e torna: l'avviso non si spegne; (4) una mano copre il sensore: «affidabilità persa»; (5) il tabellone: «dentro la zona k volte su n» [P].

Il caso più probabile è senza sensore: sequenze simulate e registrazioni, dichiarate su una riga fissa dello schermo; il giurato sceglie la sequenza. Con una camera in sala: pannello alto 1,8 m e largo 1 m, a 1,8 m dal sensore; un adulto a 2,3 m, a 0,5 m/s; al chiuso [P].

## 9 · Il piano: 14 + 4 ore, cinque persone

- **Ore 0–12.** Sei gradini, ognuno dietro un interruttore: «libero», avviso, zona, identità, stati, salute del sensore. All'ora 12 il programma si congela; lo schermo nomina ciò che manca [P].
- **Ore 5–6.** Se arriva una camera di profondità, tre misure: posa e pavimento vuoto per 30 s; pannello sul suolo segnato, 150 fotogrammi; 30 passaggi. Se non arriva, il piano non cambia [P].
- **Ore 12–18.** Tabellone e prova generale entro l'ora 14; poi i gradini rimasti, le etichette a mano, documento e video. Stime, non misure: i primi quattro gradini pronti all'ora 14 con probabilità fra 0,82 e 0,99; tutti e sei, con tabellone e demo, fra 0,04 e 0,43 [C].

## 10 · Dopo l'hackathon: aperti, non promessi

Sensore in moto; più persone nella stessa ombra; sensori laterali; un classificatore vero; prove con persone non vedenti. Per nessuno c'è oggi una prova.
