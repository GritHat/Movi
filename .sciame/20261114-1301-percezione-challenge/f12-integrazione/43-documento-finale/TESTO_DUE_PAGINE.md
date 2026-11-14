<!--
TESTO DEL DOCUMENTO DI DUE PAGINE — versione finale dopo le due letture (sciame-redattore, f12, 43-documento-finale, 14 novembre 2026)
Per chi impagina: il riquadro (righe che cominciano con «>») va in testa, o in un riquadro colorato che non si può saltare; lo schema è nel blocco di codice, una riga per blocco, poi le frecce; le tabelle sono due, di sei e di quattro righe. Il testo del documento finisce alla riga «FINE DEL TESTO»: ciò che segue (correzioni, titoli, discorso, domande) non si impagina.
Ogni cifra ha la sua riga in CIFRE.md, nella stessa cartella.
CAMBI DI STATO: nessuno; niente è «validato». REGOLE VIOLATE: ingressi obbligati non letti per intero (verdetto sui dati, discordanze dei fascicoli, decimo addendum, versione 3, blocco di classificazione: solo le righe cercate; elenco in fondo a CIFRE.md); prova sull'identità e controprova non aperte (cifre prese dal verdetto d'integrazione). Il testo finale non è stato riletto da un lettore senza contesto: C-G non verificato sulla versione finale.
CONTEGGIO: corpo 1255 (prima stesura 1279) · schema 173 (172) · tabelle 348 (333) · riquadro dei limiti 249 (241) · somma delle quattro parti 2025 (2025): il testo non si allunga. Il corpo comprende le marche di stato e i segni di marcatura; lo spazio chiesto (circa 1 100 parole di corpo) resta superato. Ordine dei tagli, se non entra in due pagine: la riga «Ore 5–6» del piano; la frase sull'operatore remoto (§4.4); il secondo capoverso della demo; il §10.
-->

# Un prototipo che dichiara ciò che non ha osservato

**Monitoraggio di attività e oggetti in ambienti aerospaziali e industriali.** Un prototipo progettato per rilevare elementi mobili e ostacoli, gestire le interruzioni della visibilità, distinguere l'osservato dall'incerto e segnalare la perdita di affidabilità [P].

**[S]** provato in simulazione · **[C]** per regola scritta, calcolo o scheda tecnica: non prova che il programma lo faccia · **[P]** in progetto, non provato.

> **Limiti, da leggere per primi**
>
> - Nessun fotogramma di una nostra camera è passato da una prova. Tutto è provato al calcolatore, su profondità simulata dalle schede tecniche e su tracce pubbliche di persone, a sensore fermo, con una persona alla volta.
> - È un progetto di prototipo: le parti sono provate una per una, l'insieme non è mai stato eseguito.
> - Dominio: camera ferma a 1,2 m da terra, al chiuso, fino a 3 m; posa della camera nota (inclinazione entro 0,5°); un ostacolo fermo che nasconde la persona per intero.
> - Non vede: il vetro e ciò che non rimanda segnale; il suolo a meno di 1,24 m davanti e di 1,7 m ai lati; la testa di una persona di 1,70 m a meno di 2,01 m; un ostacolo sospeso (sotto, il suolo risulta libero).
> - Non provati: due persone nella stessa ombra, un ostacolo che si sposta, il sensore in moto, il sole, ogni classe diversa da «persona a piedi».
> - Il classificatore è richiesto, non realizzato, non valutato: le etichette sono messe a mano.
> - Difetto aperto: tolto l'ostacolo e rivisto il suolo, l'avviso non si spegne (10 prove su 10). Si toglie riavviando.
> - Il sistema osserva e avvisa: nessuna uscita è un comando, nessuna funzione d'ingaggio o di puntamento. Nessuna norma di sicurezza letta né applicata. Per una persona non vedente è un avviso di presenza: non sostituisce bastone o cane guida.

## 1 · L'idea

Una persona passa dietro un mezzo fermo: il rischio è che per la macchina che osserva non ci sia più. Di ogni cosa seguita il prototipo dice se **la vede**, se **non la vede ma indica una zona dove può essere**, o se **non lo sa** [P].

**Obiettivo principale: la continuità visiva.** Finché l'ostacolo nasconde una persona già vista per almeno 4 fotogrammi, lo schermo mostra a ogni fotogramma un segno e una zona [S su sensore ideale: 0 interruzioni su 23 402 passaggi; P nella prova più vicina a una camera: §3].

**Principio di sicurezza.** Ciò che non è osservato non è mai dichiarato libero, se l'inclinazione è nota entro 0,5° e l'ostacolo rimanda segnale [C]. L'avviso di «possibile presenza» non si spegne per il tempo né per mano di chi guarda: dietro un ostacolo fermo resta acceso. Lo decidono regole scritte: nessun modello appreso può toglierlo [C].

## 2 · Come funziona

```
SCHEMA A BLOCCHI (una riga per blocco, poi le frecce)
B0  Configurazione all'avvio: classi ammesse nel sito; profilo di chi porta il sensore (oggi: fermo)
B1  Sensore: camera di profondità frontale, ferma; controllo all'avvio
B2  Mappa del suolo a 4 stati: libero · occupato · in ombra · non osservato
B3  Rilevamento geometrico: gruppi di celle occupate; che cosa è mobile
B4  Inseguimento: associazione e filtro di Kalman
B5  Durante l'occlusione (blocco in evidenza): zona prevista · avviso di possibile presenza · riaggancio
B6  Regole: una tabella scritta, nessun modello appreso
B7  Uscita: schermo · segnali sonori brevi · registro degli eventi
B8  Salute del sensore: «affidabilità persa»
B9  Classificazione (a lato, tratteggiato): oggi etichette a mano
FRECCE PIENE: B0 -> B1 -> B2 -> B3 -> B4 -> B5 -> B6 -> B7 ; B2 -> B5 (ombra e «libero» del fotogramma) ; B8 -> B6 (scavalca tutto)
FRECCE TRATTEGGIATE: B4 -> B9 ; B9 -> B7 (testo sotto la traccia) ; B9 -> B5 (può solo allargare l'avviso: spento nel prototipo)
```

Una camera di profondità (misura la distanza di ogni punto) sta ferma, inclinata di 15° in basso. Ogni fotogramma diventa una mappa del suolo dall'alto, a celle di 1° × 0,1 m fino a 3 m, in quattro stati: libero, occupato, in ombra (dietro un ostacolo), non osservato. «Libero» si legge nel solo fotogramma corrente, senza memoria [C].

Un filtro di Kalman, che stima posizione e velocità, segue i gruppi di celle occupate. Quando una persona seguita entra in un'ombra nascono la **zona prevista** e l'**avviso**, che copre l'ombra più una fascia di 0,40 m. La previsione può accendere l'avviso, mai spegnerlo [C]. La zona con la cifra (§3) viene da 400 percorsi di camminatori simulati, lo stesso generatore delle prove. Nelle 14 ore lo schermo mostra prima un disco, senza cifra; la zona con la cifra è un lavoro delle ultime 4 ore [P].

**Classificazione.** Il sistema richiede un classificatore su più classi (persone, veicoli di tipo diverso, altri ostacoli mobili), ciascuna con velocità, accelerazione e gradi di libertà. Qui nessun modello è in esecuzione: le etichette le mettiamo a mano [P]. Nessuna etichetta produce un «libero», toglie o restringe un avviso [C; sulla sola fascia 0 violazioni su 20 000 sequenze, mai sull'intero programma]. Chi porta il sensore (oggi: fermo) ha un profilo fisso, dichiarato all'avvio: velocità, tempo di reazione, frenata [P].

## 3 · La continuità visiva

**Che cosa si vede.** Persona visibile: disco pieno. Nascosta: anello vuoto e zona tratteggiata, con il tempo da cui non è vista. Oltre il limite della precisione dichiarata la zona diventa tutta l'ombra, «previsto ampio»: il segno non sparisce [C]. Al ritorno: «ricomparso · identità presunta» [P].

**La cifra e il suo dominio.** Su sensore ideale (la persona è un punto, con 5 cm di rumore), con un ostacolo largo 2 m, il bordo dell'ombra noto e la persona sul proprio percorso, finché resta nascosta è dentro la zona in almeno 9 casi su 10 fino a 2 s e in almeno 85 su 100 fino a 3 s [S]. Con il pannello da 1 m della demo: almeno 87 su 100 a 1 s; poi lo schermo dice solo che è ancora dietro [S].

**Dove cede.** Chi svolta o esce dal lato lontano: circa 6–8 casi su 10 a 2–3 s. Bordo dell'ombra stimato e non dato: 3–5 su 10 a 1 s [S]; su una camera il bordo va stimato, e lì non diamo cifre. Chi parte da fermo, due persone, oltre 3 s: nessuna cifra, resta l'avviso [C]. Persona persa di vista prima dell'ostacolo: l'avviso può non nascere (24 passaggi su 23 402 con la regola che lo cura, che parte spenta; 928 senza) [S]. **Su profondità simulata, la prova più vicina a una camera, la regola della zona non è ancora nel programma:** a persona nascosta il segno «previsto» manca in 2 983 fotogrammi su 4 552, circa due su tre [S]. Prima prova da fare.

## 4 · Che cosa è provato, e come

1. [S] «Suolo visto libero» non è mai uscito sopra un ostacolo (camera ideale, cioè profondità calcolata dalla geometria: 300 condizioni, 9 000 fotogrammi, due volte). Con 1° d'errore d'inclinazione cede.
2. [S] Su profondità simulata, una persona nascosta entro 3 m non è mai rimasta senza avviso (0 fotogrammi su 4 324; replica: 0).
3. [S] Il numero di traccia al ritorno (a schermo «identità») è sempre «presunto»: coi parametri di partenza reggeva 0 volte su 90; con una correzione che parte spenta, 176 su 180 (94–99 %), solo per un adulto solo, a 0,5 m dal pannello, entro 2,6 m. Un'altra persona che esce dalla stessa ombra prende il numero (19 volte su 20); l'avviso resta.
4. [C] I 3 m di portata bastano ad avvisare in tempo chi si avvicina fino a 1,44 m/s, con 1 s di reazione (ipotesi): il passo normale sì; veicoli, treni e aerei no. Con un operatore remoto (1,8 s): 0,92 m/s. La fascia di 0,40 m copre chi è nascosto fino a 1,13 m/s.

## 5 · Idee scartate, nostre ed esterne, e perché

- **Tre sensori a tempo di volo per 360°.** Coprono 180° [C].
- **Stimare massa e accelerazione.** Da queste misure non si ricavano [C]. Con le classi: solo intervalli a priori.
- **Catena filtro → rete → decisione.** Il filtro consuma misure, non le produce: rilevamento → associazione → aggiornamento del filtro → regole [C].
- **Mappa di volume a cubetti (voxel).** A sensore fermo non dà più del fotogramma corrente; le varianti che ricordano un «libero» sbagliano: 80 505 falsi su 146 901 [S].
- **Due ipotesi di moto con pesi.** Danno per ferma una persona che transita, nel 38–100 % dei transiti [S].

## 6 · I requisiti della traccia

| La traccia chiede | Che cosa fa il prototipo | Stato |
|---|---|---|
| Rilevare elementi mobili e ostacoli | Gruppi di celle occupate; «mobile» chi si sposta | [S] scatola di 15 cm a 2 m: 10 su 10. Pannello fermo dato per mobile 79 volte su 90; 0 su 140 con una correzione che parte spenta, nel suo dominio |
| Gestire le interruzioni della visibilità; continuità percettiva | Zona a ogni fotogramma; avviso sull'ombra | [S] su sensore ideale; [P] su profondità simulata |
| Distinguere l'osservato dall'incerto | Disco pieno solo con una misura; zona tratteggiata con l'età; registro «osservato» o «dedotto» | [C] regole di disegno; [P] registro mai eseguito |
| Feedback chiari e tempestivi; latenza; efficienza elaborativa | Un livello per settore: «attenzione», «zona non verificata», «suolo visto libero da 1,3 m a d metri» | [S] calcolo su un portatile, un solo filo: 6 ms per ciclo in media su scene simulate, 81 ms su una registrazione pubblica affollata; [P] ritardo non misurato, nessuna prova con persone |
| Segnalare la perdita di affidabilità | Controllo all'avvio; segnale se il sensore è coperto, urtato o fermo | [S] segnale in 0,13 s (rumore ipotizzato); [P] su una camera |
| Sicurezza delle indicazioni | Mai «libero» il non osservato; l'avviso non si toglie se non guardando | [C] a inclinazione nota entro 0,5° e se l'ostacolo rimanda segnale |

## 7 · Un nucleo, più profili

| | Monitoraggio di un varco o di un'area di lavoro | Avviso di presenza per una persona non vedente ferma |
|---|---|---|
| Dove sta il sensore | Stazione fissa, o veicolo terrestre senza equipaggio fermo [P: configurato, non provato] | Treppiede accanto alla persona |
| Uscita | Schermo e registro per l'operatore; messaggio per un autopilota: [P], mai generato | Segnali sonori di 0,3 s: [P], mai provati con persone |
| Se l'affidabilità cade | Lo dichiara; i settori dicono «zona non verificata» | Segnale dedicato; la persona torna al bastone |
| Non provato | Sensore in moto, oltre 3 m, esterni | Persona che cammina |

**Identico nei due profili:** le tre risposte su ciò che è seguito, i quattro stati della cella, il principio di sicurezza [P].

## 8 · La demo

Cinque atti, cinque minuti: (1) pavimento vuoto; (2) una persona passa dietro il pannello e ricompare; (3) resta dietro e torna: l'avviso non si spegne; (4) una mano copre il sensore: «affidabilità persa»; (5) il tabellone: quante volte la persona nascosta era dentro la zona [P].

Senza sensore, il caso più probabile: sequenze simulate e registrazioni, dichiarate sullo schermo. Con una camera: pannello alto 1,8 m e largo 1 m, un adulto a passo lento [P].

## 9 · Il piano: 14 + 4 ore, cinque persone

- **Ore 0–12.** Sei gradini, ognuno dietro un interruttore: «libero», avviso, zona, identità, stati, salute del sensore. All'ora 12 il programma si congela; lo schermo nomina ciò che manca [P].
- **Ore 5–6.** Se arriva una camera: posa, pavimento vuoto, pannello sul suolo segnato, 30 passaggi [P].
- **Ore 12–18.** Tabellone e prova generale entro l'ora 14; poi i gradini rimasti e le etichette a mano. Stime, non misure: i primi quattro gradini all'ora 14 con probabilità 0,82–0,99; tutti e sei, con tabellone e demo, 0,04–0,43 [C].

## 10 · Dopo l'hackathon: aperti, non promessi

Sensore in moto, più persone per ombra, sensori laterali, un classificatore vero, prove con persone non vedenti.

<!-- FINE DEL TESTO -->

---

# Fuori dal documento: note del redattore (non si impaginano)

## (a) Correzioni dei lettori: applicate e non applicate

Sigle: **E** lettore esterno (`41-lettore-esterno/LETTURA.md`, §C), **T** lettore tecnico (`42-lettore-societa/LETTURA.md`, §3), **VI** verdetto d'integrazione, **V3** soluzione versione 3, **BL** blocco di classificazione, **DF** discordanze dei fascicoli.

**Applicate (19 su 23, alcune in parte).**
- **E1.** Il ripiego è detto in chiaro: nelle 14 ore un disco senza cifra, la zona con la cifra nelle ultime 4 ore (V3 §1.6; VI §5.11; piano, riga dell'ora 15). Tolta l'altra focale dal riquadro: restano 1,24 m e 1,7 m, coerenti col campo di 58° (DF, geometria 2; VI §5.15); la coppia 1,22 / 1,69 m (f = 424 px) resta in CIFRE.md.
- **E2.** L'obiettivo del §1 porta ora «vista per almeno 4 fotogrammi» e le due marche: [S] su sensore ideale con la numerosità, [P] su profondità simulata. Tolto «meno di 6,4 su 10 000» (resta in CIFRE.md). *Non applicata la parte sulle frecce dello schema:* la consegna le chiede.
- **E3, E4.** «Dove cede» riscritto: «a 2–3 s» aggiunto; detto che su una camera il bordo va stimato e che lì non si danno cifre (VI K-215, K-404, §5.11); il segno «previsto» che manca in 2 983 fotogrammi su 4 552 è detto con «circa due su tre» (conto mio: 0,655). Tolto «quattro regole su nove».
- **E5, T2.** Principio di sicurezza con le due premesse (inclinazione, ostacolo che rimanda segnale) e col costo nella stessa frase; «regole scritte, nessun modello appreso» portato dal §2 al §1 (VI aff. 3, 9, 14). *In parte:* «per il nome» non è nel §1 (il lettore esterno non sa ancora che cos'è): l'indipendenza dall'identità sta nel §4.3 («l'avviso resta»). Nel riquadro «tolto l'ostacolo e rivisto il suolo, l'avviso non si spegne», senza «dovrebbe», per spazio.
- **E6.** «24 su 23 402 con la regola che lo cura, che parte spenta; 928 senza»; «una correzione che parte spenta» due volte (VI §5.13); la replica senza la seconda cifra.
- **E7, E8, T13.** Legenda di [C] riscritta; «sensore ideale» definito nel §3 e «camera ideale» nel §4.1 (VI §3; `03-libero/PREVISIONI.md`, riga 9); «profondità simulata» è detta «la prova più vicina a una camera». La definizione sta nel testo e non nella legenda di [S], perché [S] copre tre banchi diversi.
- **E10, T11.** Titolo: «Un prototipo che dichiara ciò che non ha osservato» (il vetro è un controesempio a «sa che cosa non vede»: V3 §1.2). «d metri»; «registrazione pubblica»; «oggi: fermo».
- **T1.** «400 percorsi di camminatori simulati, lo stesso generatore delle prove» (verdetto sulla continuità, riga 31).
- **T3.** «Veicolo terrestre senza equipaggio fermo [P: configurato, non provato]» (VI K-509; BL §3).
- **T4, in parte.** «Nessuna norma di sicurezza letta né applicata» (DF; BL). *Non* «non è una funzione di sicurezza»: nessun verdetto lo dice in questa forma (lo nota lo stesso lettore).
- **T6, in parte.** Aggiunto «con un operatore remoto (1,8 s): 0,92 m/s» (BL §3; conto rifatto da me: 2,05 m / 2,222 s). Lasciati fuori per spazio «stazione fissa» e il caso a 1,5 s (1,07 m/s).
- **T8.** «Su un portatile, un solo filo» (verdetto sui dati, riga 16).
- **T10.** «Posa della camera nota (inclinazione entro 0,5°)»: VI dice «posa», V3 §1.3 «errore d'inclinazione»; le riporto entrambe.
- **T12.** «Numero di traccia» al posto di «nome»; a schermo resta la scritta «identità presunta».

**Non applicate.**
- **E7, seconda parte** («in più di metà dei casi» al posto di 80 505 su 146 901): i due lettori tirano in direzioni opposte; fuori dalle prime dieci righe vince l'esattezza per il tecnico, che indica quella cifra come la sola che parla del sensore in moto.
- **E9** (chilometri all'ora): tolti per spazio. «(scheda del costruttore)» invece è tolta, perché la legenda di [C] ora nomina la scheda tecnica.
- **T5** («più largo del necessario, per prudenza»): superata. Il punto sui tracciati pubblici di 9 persone è stato **tolto** per spazio (era terzo nell'ordine dei tagli della prima stesura); «per prudenza» non è in nessun verdetto. La cifra resta in CIFRE.md come «non scritta».
- **T7** (le due domande aperte sul sensore in moto): tolte per spazio, per rimettere nel riquadro la riga sulla persona non vedente; restano buone per il pitch, come domande e non come promesse.
- **T9** («come un autopilota, non può controllare a vista ciò che riceve»): è un argomento, non un'affermazione dei verdetti, e allunga le prime dieci righe.

**Modifiche mie, non chieste dai lettori.** (1) «La previsione non lo restringe mai» → «La previsione può accendere l'avviso, mai spegnerlo» (DF D3: la forma vera è la monotonia). (2) Tolta la seconda frase del sottotitolo (primo taglio previsto dalla prima stesura): il secondo profilo compare nell'ultima riga del riquadro e nel §7. (3) Geometria della demo ridotta a pannello e passo. (4) Tolti dal piano «30 s», «150 fotogrammi», «documento e video».

**Dubbi di contenuto per l'autore.** (1) V3 §3 vieta «una cifra per chi svolta»; VI aff. 8 la dà («circa 6–8 su 10»): il testo segue VI, che è posteriore, e la dà solo sotto «Dove cede». (2) «Oggetto basso vicino» e «ostacolo più basso di 1,65 m» (VI §5.15) non sono nel riquadro, per spazio. (3) Restano i dubbi 1–3 e 6 della prima stesura (`40-documento/CIFRE.md`): le etichette a mano nelle ultime 4 ore e «non si toglie se non guardando» presuppongono le opzioni (a) di VI §9, che l'utente non ha ancora scelto. (4) Con «tracce pubbliche di persone» nel riquadro (dicitura obbligata: VI §5.1) e senza più il punto sui 9 pedoni, il testo non dice che cosa è stato provato su quelle tracce.

## (b) Tre titoli alternativi

1. Visto, nascosto, non so: tre risposte al posto di una
2. Continuità visiva dietro un ostacolo, con l'incertezza dichiarata
3. Dietro l'ostacolo: un segno, una zona, un avviso

## (c) Il discorso da un minuto

Una persona passa dietro un mezzo fermo. Il rischio è che, per la macchina che osserva, non ci sia più. Di ogni cosa che segue, il prototipo dice se la vede, se non la vede ma può essere in una zona, o se non lo sa. Finché la persona è nascosta lo schermo tiene un segno, una zona e un avviso; e per regola nessuna previsione e nessuna etichetta possono spegnerlo. Tutto è provato al calcolatore, mai su una nostra camera. In simulazione, con un ostacolo largo due metri, il bordo dell'ombra noto e la persona sul suo percorso, è nella zona in almeno nove casi su dieci fino a due secondi. Dove cede, lo diciamo noi. Il classificatore è richiesto e qui manca: le etichette sono messe a mano.

*(130 parole. Cifre: due metri, nove su dieci, due secondi: tutte nel §3 del documento.)*

## (d) Le cinque domande più probabili della giuria

1. **Funziona su una camera vera?** Non lo sappiamo: nessun fotogramma di una nostra camera è passato da una prova. Sulla prova più vicina, la profondità simulata, l'avviso regge (0 fotogrammi su 4 324) e la zona non è ancora nel programma (manca in 2 983 fotogrammi su 4 552).
2. **Alla demo vedremo la zona «da 9 su 10» o il disco senza cifra?** Nelle 14 ore il disco, senza cifra; la zona con la cifra è un lavoro delle ultime 4 ore. E col pannello da 1 m della demo la cifra sarebbe «almeno 87 su 100 a 1 s», non 9 su 10.
3. **Un avviso che non si spegne non diventa inutile?** È il costo che abbiamo scelto: dietro un ostacolo fermo resta acceso, perché non si spegne se non guardando. C'è anche un difetto aperto: tolto l'ostacolo resta acceso (10 prove su 10) e oggi si toglie riavviando.
4. **Quanto è grande la zona che contiene la persona?** L'area media non è contata: non risolto. Sappiamo solo che quando la zona supera l'80 % dell'ombra lo schermo la chiama «previsto ampio» e non dà cifre (V3 §1.6; cifra non scritta nel documento).
5. **E su un veicolo in moto, o con veicoli al posto delle persone?** Non provato: tutto è a sensore fermo e con persone a piedi. Il classificatore è richiesto e non realizzato; per conto, 3 m di portata bastano fino a 1,44 m/s, e veicoli, treni e aerei restano fuori.
