# MoVi · Valutazione esterna e istruzioni di produzione del video (stato del 14-11, fuoco uncrewed)

Nov 14, 2026 · @Pierfrancesco

## 0 · Come usare questo documento

Questo documento dice allo sciame e all'agente che produce il video quali punti di forza mettere in scena, con quali prove, e come farli vedere. Il video è centrato su una piattaforma uncrewed ferma che sorveglia il varco di un hangar per un operatore remoto. Chi lo esegue non interpreta: applica.

| Destinatario | Sezioni | Che cosa restituisce |
| --- | --- | --- |
| Esame agentico (sciame) | §1, §2 | Una risposta ai cinque punti aperti di §1 (accolto, respinto con motivo, oppure la prova che lo decide) |
| Agente di produzione | Tutto, in ordine | I sette prodotti dell'elenco qui sotto |

**Fonti, in ordine di precedenza**

1. La traccia ufficiale della challenge (testo qui sotto).
2. La proposta dello sciame, versione più recente (oggi v0.9, "testo finale dopo la chiusura dello sciame", 19:42): è la fonte delle frasi rivolte alla giuria e, quando è più recente, anche di cifre e stati.
3. Lo stato del progetto, versione 2 (14 novembre 2026, 17:40): è la fonte di cifre, stati della prova e verdetti.
4. L'elenco dei riferimenti, versione finale (291 voci): è la fonte di ogni citazione esterna. Si cita solo ciò che la voce dà come "pagina aperta e dato presente".
5. Questo documento, per forma, lessico e produzione.
6. Le decisioni della squadra (§2).

Lo stato del progetto (17:40) è anteriore alla v0.9: dove i due differiscono vale la v0.9, e il conflitto va nel rapporto di §11. Tutto ciò che lo stato del progetto marca "\[prel.\]" (non vagliato dall'arbitro) può entrare nel video solo come progetto, mai come risultato.

**Come leggere le istruzioni**

- "Deve" e "non deve" sono vincolanti. Tutto ciò che non è marcato "facoltativo" è obbligatorio.
- Un dato mancante diventa `[DA FORNIRE: …]`, che compare nell'elenco dei segnaposto e mai nel video consegnato.
- Numeri all'italiana: virgola decimale, spazio per le migliaia (14 400).

**Consegna dell'agente di produzione**

1. Registro delle cifre e delle decisioni applicate (§5, §2).
2. Sceneggiatura finale (§9), con parole e durata per scena.
3. Animatic sulla voce guida.
4. Video finale MP4 (§7).
5. Sottotitoli: file `.srt` e sottotitoli impressi.
6. Rapporto di controllo qualità (§11).
7. Elenco dei segnaposto residui: se non è vuoto, il video non si consegna.

**Traccia ufficiale della challenge**

> Le tecnologie di Computer Vision e Intelligenza Artificiale permettono di interpretare ambienti dinamici e trasformare immagini in informazioni utili. Tuttavia, riconoscere un oggetto o un soggetto in movimento non basta: un ostacolo può nasconderlo temporaneamente, mentre la scena continua a cambiare. Questo problema accomuna sistemi per l'accessibilità e soluzioni di osservazione e ispezione nei settori Aerospace & Industry, dove tempestività e affidabilità sono essenziali.
>
> La sfida è ideare e sviluppare un prototipo capace di rilevare elementi mobili e ostacoli, gestire interruzioni della visibilità e distinguere le informazioni osservate da quelle incerte. Il sistema dovrà fornire feedback spaziali chiari e tempestivi quando le condizioni lo consentono, segnalando invece la perdita di affidabilità quando necessario.
>
> I team potranno applicare la soluzione all'orientamento assistito di persone con disabilità visiva oppure al monitoraggio di attività e oggetti in ambienti aerospaziali e industriali. L'obiettivo è dimostrare continuità percettiva, bassa latenza ed efficienza elaborativa, senza rinunciare alla sicurezza delle indicazioni.

## Registro delle modifiche v0.6 → v0.9

Le versioni 0.7, 0.8 e 0.9 cambiano il progetto più di tutte le precedenti messe insieme. La continuità visiva ora è provata in simulazione su sensore ideale, ma non ancora su profondità simulata. La grammatica a schermo è decisa nella proposta stessa. Quasi tutte le cifre sono nuove, e sono cambiati anche il titolo e la legenda. Il fuoco uncrewed e le regole di disegno di questo documento restano; il copione è riscritto. La tabella riassume le tre versioni; dove la 0.8 diceva altro, vale la 0.9.

| # | Che cosa cambia | Dove nella v0.9 | Effetto qui |
| --- | --- | --- | --- |
| N1 | Titolo nuovo: "Un prototipo che dichiara ciò che non ha osservato". Legenda nuova: **S** provato in simulazione; **C** per regola scritta, calcolo o scheda tecnica ("non prova che il programma lo faccia"); **P** in progetto, non provato | Intestazione | D1; §5 |
| N2 | Continuità visiva, S su sensore ideale: 0 interruzioni su 23 402 passaggi. Precisione: almeno 9 su 10 fino a 2 s e 85 su 100 fino a 3 s, con ostacolo largo 2 m e bordo dell'ombra noto; con il pannello da 1 m della demo almeno 87 su 100 a 1 s, poi "ancora dietro". **Su profondità simulata la regola non è nel programma:** il segno "previsto" manca in 2 983 fotogrammi su 4 552 | §1, §3 | V17 riscritto; atto 2; scena 6 |
| N3 | Grammatica a schermo decisa dalla proposta: disco pieno (vista); anello vuoto con zona tratteggiata e tempo da cui non è vista (nascosta); "previsto ampio", tutta l'ombra, al posto di "perso"; "ricomparso · identità presunta" | §3 | §4; §7 |
| N4 | Principio di sicurezza con le sue premesse: mai "libero" il non osservato, **se l'inclinazione è nota entro 0,5° e l'ostacolo rimanda segnale**. "Libero" nel solo fotogramma corrente. L'avviso non si spegne né per il tempo né per mano di chi guarda | §1, §2 | V14 e V15 chiusi; §3; §4 |
| N5 | Architettura: configurazione (classi ammesse, profilo di chi porta il sensore), controllo all'avvio, salute del sensore che scavalca tutto, registro degli eventi. La rete "persona / non persona" è sostituita da un classificatore su più classi **richiesto e non realizzato**: oggi etichette a mano, che non possono spegnere né restringere un avviso | §2 | §4; scena 5 |
| N6 | Cifre: escono 14 400 passaggi, 13 su 4800, 400 su 400 in 27 configurazioni, 12 attacchi e 7 regole, 2000 passaggi. Entrano: 9 000 fotogrammi senza "suolo visto libero" sopra un ostacolo; 0 su 4 324 fotogrammi senza avviso su profondità simulata; identità 176 su 180 con una correzione, sempre "presunta"; 6 ms e 81 ms per ciclo; affidabilità persa in 0,13 s; portata utile fino a 1,44 m/s con 1 s di reazione, 0,92 m/s con un operatore remoto | §3, §4, §6 | §5; scena 6 |
| N7 | Limiti "da leggere per primi", ora più lunghi: l'insieme non è mai stato eseguito; suolo non visto a meno di 1,24 m davanti e 1,7 m ai lati; testa di una persona di 1,70 m non vista a meno di 2,01 m; sotto un ostacolo sospeso il suolo risulta libero; difetto aperto: tolto l'ostacolo, l'avviso non si spegne (10 prove su 10); nessuna norma letta né applicata; nessuna funzione d'ingaggio o di puntamento | Limiti | §5 (L); scene 6 e 8 |
| N8 | Caso uncrewed esplicito: "veicolo terrestre senza equipaggio fermo", P "configurato, non provato"; il messaggio per un autopilota è P "mai generato"; se l'affidabilità cade, i settori dicono "zona non verificata" | §7 | D15; §3 regola 26; atti 1 e 4 |
| N9 | Demo in cinque atti nuovi: pavimento vuoto; passa dietro il pannello e ricompare; resta dietro e torna (l'avviso non si spegne); mano sul sensore; il tabellone "quante volte la persona nascosta era dentro la zona". Pannello alto 1,8 m e largo 1 m, adulto a passo lento. **La frase sulla prova scelta dal giurato non c'è più** | §8 | V20 chiuso; scene 4 e 8 riscritte |
| N10 | Piano 14 + 4 ore: sei gradini, ognuno dietro un interruttore (libero, avviso, zona, identità, stati, salute del sensore); all'ora 12 si congela e lo schermo nomina ciò che manca. Primi quattro gradini all'ora 14: 0,82–0,99; tutti e sei con tabellone e demo: 0,04–0,43 (stime) | §9 | V18 chiuso; nuovo V21 |
| N11 | Da non dire (v0.8): "prevede dove sarà", "continuità garantita", "mappa 3D", "in volo" | — | §3, regola 15; §4 |
| N12 | Idee scartate con le cifre: mappa voxel, 80 505 falsi su 146 901; due ipotesi di moto con pesi, persona in transito data per ferma nel 38–100 % dei transiti | §5 | Facoltativo, scena 5 |
| N13 | Restano validi, dallo stato del progetto e dai riferimenti: i ponti col dominio (autopiloti aperti, sorveglianza aerea, sicurezza industriale) e le regole di disegno dell'incertezza | — | §5 (fonti); §7 |

## 1 · Valutazione esterna: i punti di forza da mettere in scena (v0.9)

Verdetto: la v0.9 è la versione più forte. La continuità visiva, che era l'obiettivo mancato, ora è provata in simulazione su sensore ideale; ogni affermazione porta lo stato S, C o P; i limiti si leggono per primi. Il video ne mostra sette punti di forza, uno per scena. Restano quattro punti aperti, e solo due sono bloccanti.

**I sette punti di forza**

| # | Punto di forza | Prova e suo stato nella v0.9 | Come si vede | Scena |
| --- | --- | --- | --- | --- |
| P1 | **Dichiara ciò che non ha osservato.** Di ogni persona seguita dice se la vede, se indica una zona dove può essere, o se non lo sa | "Suolo visto libero" non è mai uscito sopra un ostacolo: 300 condizioni, 9 000 fotogrammi, due volte (S, camera ideale). Mai "libero" il non osservato, con l'inclinazione nota entro 0,5° e un ostacolo che rimanda segnale (C) | Schermo diviso: la verità a sinistra, ciò che il sistema dichiara a destra | 2, 4 |
| P2 | **Parla già la lingua dei sistemi senza equipaggio.** Un veicolo terrestre senza equipaggio fermo è un profilo configurato (P) | Autopiloti aperti: senza dati in una direzione, lì la velocità è zero \[227\], e il messaggio per settori ha un valore "sconosciuto" \[229\]; sorveglianza aerea: traccia "in coasting" con età \[172\]; sicurezza industriale: il non visto è "treated as occupied" \[284\] | Il ventaglio dei settori attorno al rover; l'etichetta della traccia con l'età | 3, 4 |
| P3 | **Non perde mai di vista una persona nascosta.** A ogni fotogramma un segno e una zona; l'avviso sull'ombra resta acceso | Su sensore ideale, 0 interruzioni della zona su 23 402 passaggi (S). Su profondità simulata, una persona nascosta entro 3 m non è mai rimasta senza avviso: 0 fotogrammi su 4 324, e 0 nella replica (S) | L'anello vuoto con la zona tratteggiata e il tempo che sale; l'ombra in POSSIBILE PRESENZA | 4, atti 2 e 3 |
| P4 | **Una precisione dichiarata, con il suo dominio.** La zona non promette: dice quanto regge | Almeno 9 su 10 fino a 2 s e 85 su 100 fino a 3 s (sensore ideale, ostacolo largo 2 m, bordo noto, persona sul suo percorso); con il pannello da 1 m della demo almeno 87 su 100 a 1 s, poi "ancora dietro" (S) | Una riga a schermo con la cifra e il suo dominio; il tabellone alla chiusura | 4 atto 2, 8 |
| P5 | **Non si spegne da solo e non comanda.** L'avviso non si toglie per il tempo né per mano di chi guarda; se il sensore è coperto lo dice | Avviso: regola scritta (C). Affidabilità persa in 0,13 s (S, rumore ipotizzato); i settori dicono "zona non verificata"; "nessuna uscita è un comando" | Il ventaglio tutto puntinato e la banda AFFIDABILITÀ PERSA | 4, atti 3 e 4 |
| P6 | **Dice dove cede, con le cifre.** Le idee scartate hanno il loro numero | Chi svolta o esce dal lato lontano: circa 6–8 su 10 a 2–3 s; bordo dell'ombra stimato: 3–5 su 10 a 1 s; su profondità simulata il segno "previsto" manca in 2 983 fotogrammi su 4 552 (S). Mappa voxel scartata: 80 505 falsi su 146 901 (S) | Righe di registro, la più scomoda in corallo | 6 |
| P7 | **Leggero, e deciso da regole scritte.** Nessun modello appreso può togliere un avviso | 6 ms per ciclo su un portatile, un solo filo, su scene simulate; 81 ms su una registrazione pubblica affollata (S). La velocità costante regge contro i predittori appresi per i pedoni \[85\] | La catena che si accende; la classificazione a lato, "etichette a mano" | 5 |

**Quattro punti aperti che toccano il video**

| ID | Punto | Che cosa serve dallo sciame | Bloccante |
| --- | --- | --- | --- |
| V6 | Mancano i log delle simulazioni per disegnare la demo | I log dei quattro atti, fotogramma per fotogramma, su sensore ideale e su profondità simulata | Sì |
| V21 | All'ora 12 il programma si congela: i gradini non pronti (stime: tutti e sei con tabellone e demo fra 0,04 e 0,43) non devono comparire nel video come funzioni presenti | L'elenco dei gradini accesi al congelamento | Sì, per il montaggio finale |
| V17 | Su profondità simulata la regola della zona non è ancora nel programma | Il risultato della "prima prova da fare" | No: il video mostra il sensore ideale, dichiarato, e dice il dato mancante |
| V7 | "MoVi" non compare nella proposta | Il nome | No: vale il predefinito |

V14 (premesse della garanzia), V15 (finestra del "libero"), V18 (piano dei tagli) e V20 (altezza del pannello) sono chiusi dalla v0.9.

## 2 · Decisioni della squadra

Ogni decisione ha un valore predefinito: se la squadra non risponde, l'agente applica quello e lo scrive nel rapporto di §11. Fa eccezione D9 (i nomi nel titolo di coda).

| ID | Decisione | Predefinito se nessuna risposta |
| --- | --- | --- |
| D1 | Nome e sottotitolo | "MoVi", con il titolo della v0.9 come sottotitolo: "Un prototipo che dichiara ciò che non ha osservato" |
| D2 | La cifra di precisione a schermo | "Almeno 9 su 10 fino a 2 s" con il suo dominio scritto sotto (sensore ideale, ostacolo largo 2 m, bordo noto); alla chiusura il tabellone "dentro k su n" come misura sul posto |
| D3 | Riprese reali | Nessuna prima della demo: tutto \[SIMULAZIONE\] e \[ILLUSTRAZIONE\], dai log (V6). Con una camera, la demo usa un pannello alto 1,8 m e largo 1 m e un adulto a passo lento |
| D4 | Secondo profilo (persona non vedente ferma) | Una riga a schermo nella scena 8, nessuna frase in voce |
| D5 | Perimetro d'uso | Le parole della v0.9, a schermo nella scena 8: "Osserva e avvisa: nessuna uscita è un comando. Nessuna funzione d'ingaggio o di puntamento." |
| D6 | Voce narrante | Voce umana di un membro della squadra; in alternativa voce sintetica neutra, mai una voce che imita una persona reale |
| D7 | Strumento | Grafica generata da codice (Remotion o Motion Canvas) e ffmpeg |
| D8 | Sottotitoli | Italiano; inglese facoltativo |
| D9 | Nomi nel titolo di coda | Nessun predefinito: `[DA FORNIRE: nomi e ruoli]` |
| D10 | Che cosa si dichiara provato | La legenda della v0.9: S in simulazione, C per regola o calcolo, P in progetto. Niente è provato su una camera |
| D12 | Gradini non pronti al congelamento (V21) | Il video mostra il progetto completo. Ogni gradino spento all'ora 12 diventa "in progetto" nella scena che lo mostra, oppure la scena si taglia |
| D13 | Continuità: quale simulazione | I log su sensore ideale, con l'etichetta "Simulazione · sensore ideale"; la voce dice il dato mancante su profondità simulata. Se la prima prova su profondità simulata passa, si usano quei log |
| D14 | Tempo per produrre il video | Pipeline completa; con meno di 4 ore si disegnano dai log solo gli atti 2 e 3 |
| D15 | La piattaforma in scena | Un veicolo terrestre senza equipaggio fermo (rover), con la camera su un albero a 1,2 m da terra, inclinata di 15° in basso, al varco di un hangar; a schermo "configurato, non provato". Niente drone, né in volo né posato |
| D16 | L'ostacolo in scena | Un mezzo di rampa fermo largo 2 m, perché è la geometria in cui vale la cifra di D2; la sagoma segue l'ostacolo dei log. Una riga ricorda che la demo usa un pannello da 1 m, dove la zona localizza per circa 1 s |

## 3 · Regole assolute

Ogni regola è una condizione di consegna: un video che ne viola una non si consegna. Il controllo di §11 le verifica tutte. L'effetto visivo non autorizza nessuna eccezione.

**Tempo e testo**

1. Il video completo, titoli inclusi, dura fra 165 e 175,0 secondi. Il target è 172 s.
2. La voce non supera le 340 parole, a 125–135 parole al minuto.
3. Ogni schermata ha al massimo 16 parole di testo, etichette di stato escluse.
4. Italiano, con sottotitoli sempre attivi.

**Verità dei contenuti**

5. Ogni cifra viene dal registro di §5, con la sua formulazione. Nessuna cifra nuova, nessun calcolo, nessun arrotondamento che cambi il senso.
6. Ogni prestazione dice la sua origine: "in simulazione" o "al calcolatore".
7. Una volta in voce e una a schermo: provato solo al calcolatore, a sensore fermo, una persona alla volta; le parti una per una, l'insieme mai eseguito; nessun fotogramma di una nostra camera è passato da una prova.
8. Solo i componenti della proposta più recente, con i nomi di §4.
9. Mai "via libera", né detto né suggerito: niente verde, spunte, frecce "vai", semafori.
10. LIBERO compare solo dove i log lo dichiarano. In voce si dice "suolo visto libero" oppure "nessun ostacolo osservato fino a d metri", mai "libero" da solo.
11. La cifra di continuità su sensore ideale (F3) non compare mai senza, subito dopo, il dato su profondità simulata (F4); la cifra di precisione (F5) mai senza il suo dominio.

**Onestà delle immagini**

12. Ogni inquadratura è \[RIPRESA REALE\], \[SIMULAZIONE\] (dai log) o \[ILLUSTRAZIONE\] (schema); le ultime due portano la dicitura "Simulazione" o "Schema" per tutta la durata.
13. Nelle inquadrature \[SIMULAZIONE\] posizioni, stati e tempi vengono dai log. Senza log, l'inquadratura diventa \[ILLUSTRAZIONE\].
14. Una simulazione non passa mai per una ripresa.

**Tono**

15. Vietati in voce e a schermo: validato, certificato, conforme a, compatibile con, garantito, garantisce, funziona in movimento, bassa latenza (come risultato), detect and avoid, RA, TA, ACAS, fail-safe, minaccia, bersaglio, drone in volo stazionario, in volo, prevede dove sarà, continuità garantita, mappa 3D, "perso" e "probabile" come stati, rivoluzionare, disruptive, magico, game changer, unico al mondo, 100 % sicuro, mercato, miliardi, startup.
16. Niente retorica sulla disabilità; si dice "persona non vedente".
17. Niente ordini, clienti, fatturati, nessun riferimento al committente.

**Diritti**

18. Niente loghi di terzi. I nomi dei sistemi e delle norme citati compaiono solo nella riga di fonte, in piccolo; i sensori si nominano come classe.
19. Volti riconoscibili solo con consenso scritto; altrimenti sagome.
20. Musica, font, effetti e modelli 3D solo con licenza, registrata nel rapporto.

**Previsione**

21. La continuità si dice per quello che è nella v0.9: provata in simulazione su sensore ideale (S), non ancora nel programma su profondità simulata.
22. La previsione si disegna con le regole di §7 e non deve mai sembrare un'osservazione.
23. Nessuna cifra di precisione della previsione senza il suo metodo di verifica.

**Caso uncrewed**

24. Ogni frase, in voce o a schermo, che nomina la piattaforma senza equipaggio dice anche "ferma" oppure "non provato" (regola dello stato del progetto, §8.1).
25. L'ambito si dice con le parole della traccia ("monitoraggio di attività e oggetti in ambienti aerospaziali e industriali"): "drone", "UAV" o "veicolo" non sono l'ambito.
26. I sistemi del dominio si citano come ispirazione ("è il principio di…", "ispirato a"), mai come conformità. Il valore per settore verso un autopilota si mostra sempre con "in progetto, mai generato"; il veicolo con "configurato, non provato": oggi il sistema dichiara e chiede, l'autopilota comanda.
27. Gli stati della v0.9 si dicono con le formule di §5: S "in simulazione", C "per regola" o "per calcolo", P "in progetto". Una cosa C non si dice mai "provata".

## 4 · Lessico bloccato (v0.9)

Voce, schermo e sottotitoli usano solo questi termini, nella stessa forma. La grammatica degli stati viene dalla v0.9 (§3 della proposta).

**Stati e uscite**

| Livello | Stato | Significato nella v0.9 | A schermo | In voce |
| --- | --- | --- | --- | --- |
| Mappa del suolo | Libero | Suolo visto nel solo fotogramma corrente, senza memoria | SUOLO VISTO LIBERO | "suolo visto libero", mai "libero" da solo |
| Mappa del suolo | Occupato | Ostacolo misurato | OCCUPATO | "occupato" |
| Mappa del suolo | In ombra | Dietro un ostacolo | IN OMBRA | "ombra" |
| Mappa del suolo | Non osservato | Fuori campo, oltre portata, vicino al sensore, buchi | NON OSSERVATO | "non visto" |
| Persona | Vista | C'è una misura adesso | disco pieno · ID | "la vede" |
| Persona | Nascosta | Anello vuoto e zona tratteggiata, con il tempo da cui non è vista | anello vuoto · zona · "non vista da X s" | "indica una zona dove può essere" |
| Persona | Previsto ampio | Oltre il limite della precisione dichiarata, la zona diventa tutta l'ombra; il segno non sparisce | PREVISTO AMPIO | "la zona si allarga a tutta l'ombra" |
| Ombra | Possibile presenza | L'ombra in cui la persona è sparita, più una fascia di 0,40 m; non si spegne per il tempo né per mano di chi guarda | POSSIBILE PRESENZA | "l'avviso di possibile presenza" |
| Persona | Ricomparsa | La persona torna visibile; il numero di traccia è sempre presunto | RICOMPARSO · IDENTITÀ PRESUNTA | "ricomparsa, identità presunta" |
| Rilevamento | Mobile | Un gruppo di celle che si sposta | MOBILE | "si muove" |
| Settore | Tre livelli | "suolo visto libero da 1,3 m a d metri", "attenzione", "zona non verificata" | gli stessi | "zona non verificata" |
| Settori verso un autopilota | Messaggio per settore | P, mai generato | "verso un autopilota · in progetto, mai generato" | "un autopilota, lì, non avanzerebbe" |
| Salute del sensore | Affidabilità persa | Sensore coperto, urtato o fermo; scavalca tutto | AFFIDABILITÀ PERSA · causa | "affidabilità persa" |
| Registro | Eventi | Ogni evento "osservato" o "dedotto" (P, mai eseguito) | OSSERVATO / DEDOTTO | — |

**Nomi dei componenti**

- configurazione (classi ammesse nel sito, profilo di chi porta il sensore); controllo all'avvio; salute del sensore
- camera di profondità frontale, ferma; mappa del suolo a quattro stati; rilevamento geometrico; inseguimento con filtro di Kalman; zona prevista e avviso; regole scritte; uscita: schermo, suoni brevi, registro
- classificazione su più classi: "richiesta, non realizzata; etichette a mano"
- veicolo terrestre senza equipaggio, fermo; operatore remoto; tabellone "dentro k su n"

**Al posto di**

| Non dire | Si dice |
| --- | --- |
| libero, via libera, Go | suolo visto libero; suolo visto libero da 1,3 m a d metri |
| perso, probabile, sosta | previsto ampio; possibile presenza |
| prevede dove sarà, vede dietro gli ostacoli, sa dove è | indica una zona dove può essere |
| continuità garantita | zero interruzioni su sensore ideale, in simulazione |
| stessa identità | identità presunta |
| la rete neurale riconosce, l'AI decide | decidono regole scritte; le etichette, oggi, sono a mano |
| conforme a, compatibile con, validato, certificato | ispirato a; provato in simulazione |
| detect and avoid | percezione per la navigazione sicura a corto raggio |
| RA, TA, ACAS, minaccia, bersaglio | attenzione; zona non verificata |
| drone, in volo, in movimento (per il sensore), mappa 3D | veicolo terrestre senza equipaggio fermo; a sensore fermo |
| UAV, drone o veicolo come ambito | monitoraggio di attività e oggetti in ambienti aerospaziali e industriali |
| orientamento, dispositivo medico | avviso di presenza per una persona non vedente ferma; non sostituisce bastone o cane guida |

## 5 · Registro delle cifre e delle fonti di forza (v0.9)

In voce entrano solo F2, F3, F4 e i limiti marcati "voce". Il resto va a schermo dove la tabella lo indica, o resta fuori. Tutte le cifre delle versioni fino alla 0.6 che la v0.9 non riporta (14 400 passaggi, 13 su 4800, 400 su 400, 12 attacchi, 2000 passaggi) sono escluse.

**Come si formula ogni stato (legenda della v0.9)**

- **S, provato in simulazione:** "in simulazione", dicendo su quale sensore ("ideale" o "profondità simulata").
- **C, per regola scritta, calcolo o scheda tecnica:** "per regola", "per calcolo". Mai "provato": non prova che il programma lo faccia.
- **P, in progetto, non provato:** "in progetto", "configurato, non provato", "mai generato".
- **Fonte esterna:** "è il principio di…", "ispirato a…".

**Cifre del progetto**

| # | Cifra (v0.9) | Stato | Formulazione | Uso |
| --- | --- | --- | --- | --- |
| F1 | "Suolo visto libero" non è mai uscito sopra un ostacolo: 300 condizioni, 9 000 fotogrammi, due volte; con 1° d'errore d'inclinazione cede | S, camera ideale | "Mai 'suolo visto libero' sopra un ostacolo · 9 000 fotogrammi · camera ideale" | Schermo, scena 2 |
| F2 | Ciò che non è osservato non è mai dichiarato libero, se l'inclinazione è nota entro 0,5° e l'ostacolo rimanda segnale | C | Voce: "per regola, ciò che non osserva non lo dichiara mai libero". Schermo: le due premesse | Voce e schermo, scena 2 |
| F3 | Zona a ogni fotogramma: 0 interruzioni su 23 402 passaggi | S, sensore ideale | Voce: "zero interruzioni della zona in oltre ventitremila passaggi". Schermo: "0 su 23 402" | Voce e schermo, scena 6 |
| F4 | Su profondità simulata la regola della zona non è ancora nel programma: il segno "previsto" manca in 2 983 fotogrammi su 4 552 | S | Voce: "il segno manca ancora in due fotogrammi su tre: è la prima prova da fare". Schermo: "2 983 su 4 552". Sempre subito dopo F3 | Voce e schermo, scena 6 |
| F5 | Dentro la zona almeno 9 su 10 fino a 2 s e 85 su 100 fino a 3 s (sensore ideale, ostacolo largo 2 m, bordo dell'ombra noto, persona sul suo percorso); con il pannello da 1 m almeno 87 su 100 a 1 s, poi "ancora dietro" | S | Schermo: "Dentro la zona: almeno 9 su 10 fino a 2 s" e sotto il dominio | Schermo, atto 2 |
| F6 | Su profondità simulata, una persona nascosta entro 3 m non è mai rimasta senza avviso: 0 fotogrammi su 4 324, replica 0 | S | Schermo: "Mai senza avviso · 0 su 4 324 fotogrammi · profondità simulata" | Schermo, atto 3 |
| F7 | Dove cede: chi svolta o esce dal lato lontano, circa 6–8 su 10 a 2–3 s; bordo dell'ombra stimato, 3–5 su 10 a 1 s; persona persa prima dell'ostacolo, avviso non nato in 24 passaggi su 23 402 | S | Righe di registro | Schermo, scena 6 |
| F8 | Identità al ritorno sempre "presunta": 176 su 180 con una correzione che parte spenta (adulto solo, a 0,5 m dal pannello, entro 2,6 m); un'altra persona dalla stessa ombra prende il numero 19 volte su 20, ma l'avviso resta | S | "Ricomparso · identità presunta" | Schermo, atto 2 |
| F9 | 6 ms per ciclo su un portatile, un solo filo, su scene simulate; 81 ms su una registrazione pubblica affollata; ritardo totale non misurato | S; ritardo P | Schermo: "6 ms per ciclo (scene simulate) · ritardo: da misurare" | Schermo, scena 5 |
| F10 | Affidabilità persa segnalata in 0,13 s | S, rumore ipotizzato | Schermo: "0,13 s · simulazione" | Facoltativo, atto 4 |
| F11 | La portata di 3 m avvisa in tempo chi si avvicina fino a 1,44 m/s con 1 s di reazione; con un operatore remoto (1,8 s) fino a 0,92 m/s; veicoli no | C, calcolo con ipotesi | Schermo: "Con un operatore remoto: in tempo fino a 0,92 m/s · il passo sì, i veicoli no (calcolo)" | Schermo, scena 7 |
| F12 | Idee scartate: mappa voxel, 80 505 "liberi" falsi su 146 901; due ipotesi con pesi, transito dato per sosta nel 38–100 % | S | Righe brevi | Facoltativo, scena 5 |
| F20 | Scatola di 15 cm a 2 m vista 10 volte su 10; pannello fermo dato per mobile 0 volte su 140 con una correzione che parte spenta | S | Schermo, se c'è tempo | Facoltativo, atto 1 |
| F21 | Geometria della demo con una camera: pannello alto 1,8 m e largo 1 m, adulto a passo lento | P | Riga a schermo nell'atto 2 (D16) | Schermo |

**Fonti esterne (tutte "pagina aperta e dato presente")**

| # | Fonte | Che cosa dice | Uso |
| --- | --- | --- | --- |
| F13 | Autopiloti aperti, prevenzione delle collisioni \[227\] | "If there is no sensor data in a particular direction, velocity in that direction is restricted to 0"; la regione di un sensore guasto è "treated as uncovered" | Scena 3, a schermo in italiano: "Nessun dato in una direzione: lì la velocità è zero"; riga di fonte "PX4 Autopilot, Collision Prevention" |
| F14 | Autopiloti aperti, messaggio per settori \[229\] | Un valore apposito vuol dire "sconosciuto", un altro "nessun ostacolo" | Atto 1: la barra dei settori usa la stessa idea a tre valori; riga di fonte "PX4 ObstacleDistance" |
| F15 | Sorveglianza aerea, dati di traccia \[172\] | Traccia "in coasting" quando l'ultimo aggiornamento è più vecchio di una soglia; età e accuratezza stimate | Scena 3 e atto 2: l'etichetta della traccia porta l'età ("non vista da X s"); riga di fonte "EUROCONTROL ASTERIX CAT062 (ed. 1.18)" |
| F16 | Radar navali, norme di prestazione \[179\] | Per una traccia persa, "last position should be clearly indicated on the display" | Facoltativo, scena 3 |
| F17 | Sicurezza dei robot in fabbrica \[284\] | Ciò che nessun sensore vede è "treated as occupied"; fonte di parte | Facoltativo, scena 3 |
| F18 | Schöller e altri 2020 \[85\] | Per i pedoni, a 4,8 s, velocità costante 0,39 / 0,83 m contro 0,44 / 0,91 del miglior predittore appreso deterministico | Facoltativo, scena 4 ("perché un modello semplice") |
| F19 | Cao e altri 2023 \[11\] | Il filtro di Kalman accumula errore durante un'occlusione | Base del disegno: l'incertezza che cresce si mostra, non si nasconde |

**Limiti da dire (obbligatori, dalla sezione "Limiti, da leggere per primi" della v0.9)**

| # | Limite | Dove |
| --- | --- | --- |
| L1 | Nessun fotogramma di una nostra camera è passato da una prova; tutto al calcolatore, a sensore fermo, una persona alla volta | Voce e schermo, scena 6 |
| L2 | Progetto di prototipo: parti provate una per una, insieme mai eseguito | Voce, scena 6 |
| L3 | Dominio: camera ferma a 1,2 m, al chiuso, fino a 3 m, inclinazione nota entro 0,5°, un ostacolo fermo che nasconde la persona per intero | Schermo, fasce fisse |
| L4 | Non vede il vetro né ciò che non rimanda segnale; il suolo a meno di 1,24 m davanti e 1,7 m ai lati; la testa di una persona di 1,70 m a meno di 2,01 m; sotto un ostacolo sospeso il suolo risulta libero | Voce ("non vede il vetro"), il resto a schermo, scena 6 |
| L5 | Non provati: due persone nella stessa ombra, un ostacolo che si sposta, il sensore in moto, il sole, ogni classe diversa da "persona a piedi" | Voce ("due persone nella stessa ombra"), il resto a schermo, scene 6 e 7 |
| L6 | Il classificatore è richiesto, non realizzato: le etichette sono messe a mano | Voce, scena 5 |
| L7 | Difetto aperto: tolto l'ostacolo e rivisto il suolo, l'avviso non si spegne (10 prove su 10); si toglie riavviando | Schermo, scena 6 |
| L8 | Osserva e avvisa: nessuna uscita è un comando; nessuna funzione d'ingaggio o di puntamento; nessuna norma di sicurezza letta né applicata | Schermo, scena 8 |
| L9 | Per una persona non vedente è un avviso di presenza: non sostituisce bastone o cane guida | Schermo, scena 8 |
| L10 | Veicolo senza equipaggio: configurato, non provato; messaggio per l'autopilota: in progetto, mai generato | Schermo, scena 3 e atto 1 |
| L11 | Ritardo totale non misurato | Voce, scena 6 |

## 6 · Requisiti della traccia → scene (v0.9)

Ogni richiesta della traccia ha almeno una scena, un punto di forza (§1) e lo stato che la v0.9 le dà. Se una scena viene tagliata, la richiesta deve restare coperta altrove.

| La traccia chiede | Scene | Punto di forza | Che cosa si vede | Stato nella v0.9 |
| --- | --- | --- | --- | --- |
| Monitoraggio di attività e oggetti in ambienti aerospaziali e industriali | 1, 3 | P2 | Il varco di un hangar, un veicolo terrestre senza equipaggio fermo, un operatore remoto | Profilo P, configurato, non provato |
| Rilevare elementi mobili e ostacoli | 4, atti 1 e 2 | P1 | Celle OCCUPATO; il gruppo MOBILE | S (F20) |
| Gestire le interruzioni della visibilità; continuità percettiva | 1, 4 atti 2–3, 6 | P3, P4 | Anello vuoto, zona tratteggiata con il tempo, PREVISTO AMPIO, POSSIBILE PRESENZA | S su sensore ideale; P su profondità simulata (F3, F4) |
| Distinguere l'osservato dall'incerto | 2, 4 | P1 | Disco pieno solo con una misura; zona tratteggiata con l'età | C (regole di disegno); registro P |
| Feedback chiari e tempestivi; latenza; efficienza | 4 atto 1, 5 | P2, P7 | I settori a tre livelli; 6 ms per ciclo | S per il calcolo; ritardo P, nessuna prova con persone |
| Segnalare la perdita di affidabilità | 4, atto 4 | P5 | Banda AFFIDABILITÀ PERSA; ogni settore "zona non verificata" | S in 0,13 s; P su una camera |
| Sicurezza delle indicazioni | 2, 4 atto 3, 6, 8 | P1, P5, P6 | Mai "libero" il non visto; l'avviso che non si spegne; dove cede | C, con le due premesse (F2) |
| Prototipo | 6, 8 | P4, P6 | Le etichette d'onestà; il tabellone sul posto | Limiti L1 e L2 |
| Accessibilità (altro ambito della traccia) | 8 | — | Una riga a schermo | P (L9) |

## 7 · Linguaggio visivo: la piattaforma, l'operatore, l'incertezza

Il video si regge su tre viste, sempre allo stesso posto: la scena com'è, ciò che vede l'operatore, il ventaglio dei settori attorno al veicolo. Il racconto è la differenza fra la prima e le altre due: a sinistra la persona c'è, a destra il sistema dice onestamente che cosa ne sa.

**Formato di consegna**

| Voce | Valore |
| --- | --- |
| Risoluzione | 1920 × 1080, 16:9, progressivo, 30 fps costanti |
| Video | H.264 High, yuv420p, CRF 18, MP4 con `faststart` |
| Audio | AAC-LC 48 kHz stereo, 320 kbps |
| Durata | Da 165,0 a 175,0 s, misurata con `ffprobe` |
| Margini | 96 px ai lati, 54 px sopra e sotto |
| Sottotitoli | Fascia bassa di 140 px; Inter 600 da 40 px, #E8EDF2 su #0B0F17 all'80 %; al massimo 2 righe da 42 caratteri; anche come `.srt` |
| Sorgenti | Progetto dell'animazione, log usati, tracce audio separate |

**Le tre viste**

- **SCENA (sinistra, 50 %).** L'hangar visto dall'alto, con una prospettiva leggera: pavimento con la segnaletica di rampa, il mezzo fermo largo 2 m, il veicolo terrestre senza equipaggio fermo con la camera sul suo albero (D15, D16). Tutto dalla verità della simulazione. La persona è sempre visibile, come sagoma grigia #8A97A8; quando passa dietro il mezzo, il bordo la "mangia" un pezzo alla volta e la restituisce allo stesso modo, mai a dissolvenza.
- **CONSOLE DELL'OPERATORE (destra, 50 %).** La mappa del suolo vista dalla camera e, sotto, l'elenco delle tracce come in una console di sorveglianza: "ID 1 · vista" (disco pieno), poi "ID 1 · non vista da 0,8 s" (anello vuoto e zona tratteggiata), poi "ID 1 · PREVISTO AMPIO · POSSIBILE PRESENZA · 4,2 s", poi "ID 1 · RICOMPARSO · IDENTITÀ PRESUNTA". Il tempo sale in tempo reale, come per una traccia in coasting (F15). Valori dai log.
- **VENTAGLIO DEI SETTORI.** Sopra il veicolo, in entrambe le viste, un settore per direzione con uno dei tre livelli della v0.9: "suolo visto libero da 1,3 m a d metri", "attenzione", "zona non verificata" (a puntini). In un angolo: "Verso un autopilota · in progetto, mai generato" (L10). È la stessa idea del messaggio per settori degli autopiloti aperti (F14).
- **Fasce fisse.** In alto il nome dell'atto e la richiesta della traccia. In basso a sinistra il dominio (L3): "Simulazione · camera ferma a 1,2 m · al chiuso · fino a 3 m". In basso a destra l'etichetta "Simulazione · sensore ideale", "Simulazione · profondità simulata" oppure "Schema".

**Codifica degli stati: trama e parola prima del colore**

Ogni stato si riconosce senza colore, dalla trama e dalla parola; il colore viene terzo. Contrasti calcolati sul fondo #0B0F17.

| Stato | Forma | Parola | Colore | Contrasto | Comportamento |
| --- | --- | --- | --- | --- | --- |
| SUOLO VISTO LIBERO | Cella piena tenue | SUOLO VISTO LIBERO (al primo apparire) | #24344A | 1,5:1, voluto | Solo nel fotogramma corrente, come nei log |
| OCCUPATO | Cella piena | OCCUPATO | #E8EDF2 | 16,3:1 | Come nei log |
| IN OMBRA / NON OSSERVATO | Puntini con "?" | IN OMBRA / NON OSSERVATO | #2E3A4C su #05070B | — | Come nei log |
| Persona vista | Disco pieno | ID | #3DD6E8 | 10,9:1 | Solo con una misura nel fotogramma |
| Persona nascosta | Anello vuoto e zona tratteggiata, riempimento al 20 % | "non vista da X s" | #F5A524 | 9,4:1 | A ogni fotogramma; mai una sagoma dentro |
| PREVISTO AMPIO | Righe diagonali su tutta l'ombra, con l'anello al centro | PREVISTO AMPIO | #F5A524 | 9,4:1 | Il segno non sparisce |
| POSSIBILE PRESENZA | Contorno a righe dell'ombra più 0,40 m | POSSIBILE PRESENZA | #C7841A | 6,2:1 | Non si spegne per il tempo né per mano di chi guarda |
| RICOMPARSO | Disco pieno con un punto interrogativo piccolo accanto all'ID | RICOMPARSO · IDENTITÀ PRESUNTA | #3DD6E8 | 10,9:1 | Per 2 s dopo la ricomparsa |
| ZONA NON VERIFICATA (settore) | Puntini | ZONA NON VERIFICATA | #8A97A8 su #05070B | 6,5:1 | Come nei log |
| AFFIDABILITÀ PERSA | Banda piena di 120 px | AFFIDABILITÀ PERSA · causa | #FF6B6B, testo #0B0F17 | 6,9:1 | Scavalca tutto; resta finché resta la causa |

**Come si disegna l'incertezza: nove regole fondate sulla ricerca**

| # | Regola | Perché |
| --- | --- | --- |
| 1 | Mai la sagoma della persona dentro la zona, e mai un cono attaccato al segno | Un cono d'incertezza viene letto come l'oggetto che si allarga \[36\]; con un cono il 70 % dice che l'oggetto cresce, con un insieme di esiti il 39 % \[73\] |
| 2 | Se i log danno più esiti, pochi percorsi possibili animati uno alla volta dentro la zona | Gli esiti animati battono le barre d'errore \[34\]. Solo se i log li contengono |
| 3 | La zona si disegna tratteggiata | Il tratteggio è preferito a sfocatura, grigio e tratto a mano \[10\] |
| 4 | La persona sparisce e ricompare lungo il bordo del mezzo, mai a dissolvenza | Si segue un oggetto attraverso un'occlusione solo se scompare e ricompare lungo un bordo fisso \[84\] |
| 5 | Forma e parola prima del colore; il segno non sparisce mai durante l'occlusione | v0.9, §3: "il segno non sparisce" |
| 6 | Oltre il limite della precisione dichiarata la zona diventa tutta l'ombra, PREVISTO AMPIO, senza salti | v0.9, §3 |
| 7 | Alla ricomparsa la zona resta ferma 1 s e la posizione vera compare con un segno bianco; se cade fuori, "fuori dalla zona". È ciò che il tabellone conta | La precisione si mostra contata, non promessa |
| 8 | L'incertezza non si traduce in altezza di un suono | \[100\] |
| 9 | Nessuna cifra accanto alla zona: la cifra di F5 sta in una riga a parte, con il suo dominio | Regole 11 e 23 |

**Sette momenti d'effetto**

1. **Il buio dell'hangar (scena 1).** Hangar in penombra; l'unica luce è il ventaglio dei settori del veicolo fermo, che si accende settore per settore.
2. **"È sparita" (scena 1, poi atto 2).** Il bordo del mezzo mangia la sagoma; a destra il disco pieno diventa un anello vuoto con la sua zona tratteggiata, e il tempo comincia a salire.
3. **Tre domini, una regola (scena 3).** Tre pannelli stilizzati affiancati: i settori di un autopilota con "sconosciuto", un'etichetta di traccia "in coasting · età", una cella di fabbrica "non vista = occupata". Poi i tre si fondono nel ventaglio del veicolo. Ogni pannello porta la sua riga di fonte.
4. **"Lì non si avanza" (atto 1).** Fuori dal suolo visto, i settori passano a puntini ZONA NON VERIFICATA; un vettore di velocità tratteggiato, marcato "autopilota · in progetto", si accorcia fino a zero verso di loro.
5. **L'ombra che non si spegne (atto 3).** La zona si allarga a tutta l'ombra; il tempo sale oltre i 4 s; la persona a sinistra è ferma dietro il mezzo; l'avviso resta acceso finché lei non riemerge.
6. **La mano sul sensore (atto 4).** Tutto il ventaglio passa a ZONA NON VERIFICATA, entra la banda corallo, musica e ambiente tacciono per 1 s.
7. **Il tabellone (scena 8).** Un contatore "dentro la zona: k su n" sale passaggio dopo passaggio, dai log; sotto, "alla demo si conta sul posto".

**Divieti grafici**

- Niente verde, spunte, frecce "vai", semafori.
- Niente bagliori, particelle decorative, ologrammi, "scansioni": promettono capacità che il sistema non ha.
- Niente drone in volo, niente mappe 3D o voxel.
- Niente loghi, icone stock, elenchi puntati a schermo.

**Tipografia e movimento**

- Titoli Inter 700 da 64–96 px; testo Inter 600 da almeno 40 px; etichette di stato JetBrains Mono 600 maiuscolo da almeno 28 px.
- I cambi di stato sono istantanei (al massimo 2 fotogrammi); la zona cresce con la curva dei log, senza easing aggiunto.
- Camera ferma nella scena 4; nelle scene 1, 3 e 8 un carrello lento, al massimo 5 % al secondo.
- Niente rallentatore: con l'ostacolo da 2 m la zona si vede per 2–3 s in tempo reale.

## 8 · Audio

Nel profilo di monitoraggio il sistema non emette suoni: parla all'operatore con la console e, in progetto, all'autopilota con un valore per settore. Il video quindi non ha segnali di stato. Ogni suono che lo spettatore potrebbe scambiare per un'uscita del sistema è vietato.

**Voce**

- 48 kHz / 24 bit, mono, stanza senza eco, microfono a 15–20 cm; passa-alto a 80 Hz, riduzione del rumore leggera, de-esser, compressione 3:1, niente riverbero.
- 125–135 parole al minuto. Se una scena sfora si taglia secondo §9, non si accelera.
- Le cifre si leggono come nel copione ("quattordicimila quattrocento"). "Kalman" con l'accento sulla prima sillaba. "MoVi": `[DA FORNIRE: pronuncia]`.

**Ambiente e musica**

- Un tono d'ambiente d'hangar, basso e continuo, solo con licenza: dà il luogo senza effetti.
- Musica ambient minimale, al massimo 90 BPM, senza voci né crescendo epici; 18 dB sotto la voce quando parla, 10 dB nelle pause.
- Atto 4: musica e ambiente tacciono per 1 s quando entra la banda di affidabilità persa.
- Nessun "bip", nessun suono legato ai cambi di stato, nessuna altezza di tono legata all'incertezza \[100\].

**Mix**

- Loudness integrata −14 LUFS, picco reale non oltre −1,0 dBTP, misurati con `ffmpeg -af ebur128=peak=true`.
- Tracce separate (voce, ambiente, musica) consegnate con i sorgenti.

## 9 · Sceneggiatura e storyboard (v0.9)

Il copione è vincolante: 336 parole, circa 155 s di voce su 172 s di video, 3 s di margine sotto il limite. Si cambia solo per una nuova versione della proposta (§12), una decisione della squadra (§2) o il taglio per tempo, nell'ordine dato in fondo. La demo segue i cinque atti della v0.9: i primi quattro nella scena 4, il quinto (il tabellone) in chiusura.

**Timeline**

| Scena | Inizio–fine | Durata | Parole | Punto di forza | Etichetta |
| --- | --- | --- | --- | --- | --- |
| 1 · L'hangar | 0:00–0:14 | 14 s | 28 | problema | \[SIMULAZIONE\] |
| 2 · L'idea | 0:14–0:37 | 23 s | 48 | P1 | \[ILLUSTRAZIONE\] |
| 3 · Tre domini, una regola | 0:37–0:55 | 18 s | 36 | P2 | \[ILLUSTRAZIONE\] |
| 4 · Atto 1, pavimento vuoto | 0:55–1:07 | 12 s | 25 | P1, P2 | \[SIMULAZIONE\] |
| 4 · Atto 2, passa e ricompare | 1:07–1:22 | 15 s | 30 | P3, P4 | \[SIMULAZIONE\] |
| 4 · Atto 3, resta dietro | 1:22–1:36 | 14 s | 28 | P3, P5 | \[SIMULAZIONE\] |
| 4 · Atto 4, mano sul sensore | 1:36–1:46 | 10 s | 18 | P5 | \[SIMULAZIONE\] |
| 5 · La catena | 1:46–1:58 | 12 s | 24 | P7 | \[ILLUSTRAZIONE\] |
| 6 · Prove e limiti | 1:58–2:29 | 31 s | 65 | P6 | \[ILLUSTRAZIONE\] |
| 7 · La strada | 2:29–2:37 | 8 s | 12 | — | \[ILLUSTRAZIONE\] |
| 8 · Il tabellone | 2:37–2:52 | 15 s | 22 | P4 | \[SIMULAZIONE\] |
| **Totale** |  | **172 s** | **336** |  |  |

### Scena 1 · L'hangar (0:00–0:14)

**Voce:** "In un hangar, una persona passa dietro un mezzo fermo. Per il veicolo senza equipaggio, fermo al varco, è sparita. \[pausa 0.5s\] Che cosa deve dire, quando smette di vedere?"

**Immagine:** momenti d'effetto 1 e 2 (§7), sulla sola vista SCENA a tutto schermo. Fotogramma fermo alle 0:09.

**Testo a schermo:** 0:00–0:05 "Monitoraggio di attività e oggetti · ambienti aerospaziali e industriali". 0:10–0:14 "Che cosa dice un sistema quando smette di vedere?" In piccolo: "Veicolo senza equipaggio · fermo · configurato, non provato".

### Scena 2 · L'idea (0:14–0:37)

**Voce:** "MoVi è un prototipo che dichiara ciò che non ha osservato. \[pausa 0.3s\] Di ogni persona che segue, dice se la vede, se non la vede ma indica una zona dove può essere, o se non lo sa. \[pausa 0.3s\] E per regola, ciò che non osserva non lo dichiara mai libero."

**Immagine:** lo schermo si divide in scena e console. Titolo "MoVi · Un prototipo che dichiara ciò che non ha osservato" (0:14–0:18). Poi i tre segni quando la voce li descrive: disco pieno, anello vuoto con zona tratteggiata, zona a puntini "?". Sull'ultima frase la parola LIBERO compare su una zona puntinata e viene barrata.

**Testo a schermo:** "la vede" · "indica una zona" · "non lo sa"; poi "Non osservato ≠ libero" con sotto le premesse di F2: "se l'inclinazione è nota entro 0,5° e l'ostacolo rimanda segnale". Facoltativo: F1.

### Scena 3 · Tre domini, una regola (0:37–0:55)

**Voce:** "È il linguaggio dei sistemi senza equipaggio. Negli autopiloti aperti, una direzione senza dati non è libera: lì la velocità va a zero. Nella sorveglianza aerea, una traccia non più vista resta, con la sua età."

**Immagine:** momento d'effetto 3, con le righe di fonte (F13, F15; facoltativi F16 e F17).

**Testo a schermo:** "Ispirato a: autopiloti aperti · sorveglianza aerea · sicurezza industriale"; alla fusione "MoVi lo porta alla scala di un varco". In basso: L10.

### Scena 4 · La demo, quattro atti (0:55–1:46)

Schermo diviso con le tre viste di §7, camera ferma, tutto dai log (V6), con l'etichetta "Simulazione · sensore ideale" (D13).

**Atto 1 · Pavimento vuoto (0:55–1:07).** Voce: "Pavimento vuoto: per ogni settore, il suolo visto libero fino a una distanza. Dove non vede, dice: zona non verificata. Un autopilota, lì, non avanzerebbe." Immagine: momento d'effetto 4. Facoltativo: F20.

**Atto 2 · Passa e ricompare (1:07–1:22).** Voce: "Una persona passa dietro il mezzo. Il disco pieno diventa un anello vuoto, con una zona tratteggiata e il tempo da cui non è vista. \[pausa 0.3s\] Al ritorno: ricomparsa, identità presunta." Immagine: momento d'effetto 2, regole 1–4 e 7 di §7. Testo: F5 con il suo dominio; in piccolo F21.

**Atto 3 · Resta dietro (1:22–1:36).** Voce: "Ora resta dietro. La zona si allarga a tutta l'ombra, e l'avviso di possibile presenza non si spegne: né per il tempo, né per mano di chi guarda." Immagine: momento d'effetto 5; poi la persona riemerge. Testo: F6.

**Atto 4 · Mano sul sensore (1:36–1:46).** Voce: "Una mano copre il sensore: affidabilità persa. Ogni settore dice zona non verificata. Il sistema avvisa, non comanda." Immagine: momento d'effetto 6. Facoltativo: F10.

### Scena 5 · La catena (1:46–1:58)

**Voce:** "Decidono regole scritte, non un modello appreso. La classificazione è richiesta: oggi le etichette si mettono a mano, e nessuna può spegnere un avviso."

**Immagine:** lo schema della v0.9 da sinistra a destra (configurazione → sensore con controllo all'avvio → mappa del suolo → rilevamento → inseguimento → durante l'occlusione → regole → uscita), con la salute del sensore sopra tutto e la classificazione a lato, tratteggiata, con la scritta "richiesta · etichette a mano". **Testo:** F9; facoltativo F12.

### Scena 6 · Prove e limiti (1:58–2:29)

**Voce:** "È provato solo al calcolatore, a sensore fermo, una persona alla volta: le parti una per una, l'insieme mai eseguito. Su sensore ideale, zero interruzioni della zona in oltre ventitremila passaggi; su profondità simulata il segno manca ancora in due fotogrammi su tre. È la prima prova da fare. \[pausa 0.3s\] Non vede il vetro; due persone nella stessa ombra: non provato. Il ritardo è da misurare."

**Immagine:** righe di registro, in quest'ordine: L1 e L2; F3 ("0 interruzioni su 23 402 · sensore ideale"); F4 ("2 983 fotogrammi su 4 552 senza segno · profondità simulata"), in corallo; F7 (dove cede); L4, L5 e L7 in piccolo; L11.

### Scena 7 · La strada (2:29–2:37)

**Voce:** "Il prossimo passo: il sensore in moto, più persone, un classificatore vero."

**Immagine:** tre tappe stilizzate, ciascuna con "si sblocca con una prova". **Testo:** F11.

### Scena 8 · Il tabellone (2:37–2:52)

**Voce:** "Alla demo, la precisione si conta sul posto: la mostra il tabellone. \[pausa 0.5s\] MoVi. Un prototipo che dichiara ciò che non ha osservato."

**Immagine:** momento d'effetto 7, dai log; poi il titolo; dalle 2:48 il titolo di coda (D9) e `[DA FORNIRE: nome della challenge]`; mezzo secondo di nero.

**Testo a schermo:** 2:43–2:48, in fascia bassa, su due schermate: L8 (D5); poi "Stesso nucleo, altra uscita: avviso di presenza per una persona non vedente ferma · in progetto" con L9.

### Se la voce non entra nei tempi

1. Atto 1: "Un autopilota, lì, non avanzerebbe." (5 parole); resta il vettore a schermo.
2. Scena 7 intera (12 parole); le tappe restano a schermo.
3. Atto 3: "né per il tempo, né per mano di chi guarda" (10 parole); resta a schermo.

Non si tagliano mai: L1, L2, F3 con F4, il principio di F2, "identità presunta", l'atto 4. La voce non va oltre le 135 parole al minuto.

## 10 · Pipeline di produzione

Esegui i passi in quest'ordine. Un passo con un cancello non si supera finché il cancello non è superato.

1. **Leggi le fonti.** Traccia, proposta più recente (oggi v0.9), questo documento, risposte dello sciame a §1 e della squadra a §2. Annota ogni conflitto fra le fonti; se la proposta e lo stato del progetto differiscono, vale la proposta. Leggi lo stato del progetto e l'elenco dei riferimenti solo per le voci citate in §5. Cancello: V6 (log) ha una risposta; per il montaggio finale anche V21 (gradini al congelamento).
2. **Compila il registro.** Ricava dalla proposta più recente il registro di §5 (cifra, stato S/C/P, formulazione, uso) e confrontalo con quello di questo documento. Le differenze vanno gestite come in §12.
3. **Fissa le decisioni.** Per D1–D16 scrivi il valore applicato e la sua fonte (squadra oppure predefinito).
4. **Prepara i dati.** Dai log in `.sciame/20261114-1301-percezione-challenge/` estrai una sequenza per ciascuno dei quattro atti della scena 4, più la scena 1 e il tabellone della scena 8, con la geometria di D15 e D16. Ogni sequenza contiene, fotogramma per fotogramma a 30 fps: posizione vera della sagoma, stato delle celle della mappa, tracce con ID e stato (vista, non vista da X s, previsto ampio, ricomparso), zona prevista, contorno di possibile presenza, livello di ogni settore del ventaglio, cause di affidabilità persa, e per il tabellone l'esito "dentro / fuori dalla zona" di ogni passaggio. Se i log hanno un'altra frequenza, ricampiona tenendo l'ultimo stato, senza interpolare gli stati. Cancello: se manca il log di un atto, quell'atto diventa \[ILLUSTRAZIONE\] e lo scrivi nel rapporto; il tabellone senza log non va in onda.
5. **Riprese, solo dopo la demo (D3).** Se il video si produce dopo l'hackathon, usa le registrazioni della demo solo per le inquadrature davvero registrate, accanto alla vista per l'operatore registrata nello stesso istante, con l'etichetta \[RIPRESA REALE\].
6. **Voce guida.** Registra o sintetizza una voce guida dal copione di §9 e misura la durata di ogni scena. Se una scena sfora, applica i tagli di §9 nell'ordine dato.
7. **Animatic.** Monta lo storyboard statico sulla voce guida, con i tempi definitivi. Cancello: durata fra 165 e 175 s; testo a schermo conforme a §3 (regole 3, 9, 15, 27) e a §4.
8. **Animazione.** Costruisci come componenti riusabili, guidati dai dati: le tre viste di §7 (scena, console dell'operatore con l'elenco delle tracce, ventaglio dei settori a tre livelli), la zona con le nove regole di §7, il contorno di possibile presenza, i tre pannelli della scena 3, il tabellone; modelli semplici di hangar, rover e mezzo di rampa, senza marchi e con licenza; banda di affidabilità persa; catena della scena 5. Render a 1920 × 1080, 30 fps.
9. **Voce definitiva.** Registra secondo §8 e allinea al fotogramma i cambi di stato citati in voce.
10. **Audio.** Musica e tono d'ambiente con licenza, nessun segnale di stato (§8), mix a −14 LUFS e picco reale entro −1,0 dBTP.
11. **Sottotitoli.** Genera il file `.srt` dalla voce definitiva (al massimo 2 righe da 42 caratteri) e imprimili nel video con lo stile di §7.
12. **Esporta.** Per esempio: `ffmpeg -i video.mov -i mix.wav -map 0:v -map 1:a -vf "subtitles=MoVi_pitch.srt" -c:v libx264 -profile:v high -pix_fmt yuv420p -crf 18 -r 30 -c:a aac -b:a 320k -ar 48000 -movflags +faststart MoVi_pitch_v0.9.mp4`
13. **Controllo qualità.** Esegui §11 per intero. Se una voce fallisce, correggi e riesegui tutto il controllo, non solo quella voce.
14. **Consegna.** Nomi dei file, con la versione della proposta usata:
    - `MoVi_pitch_v0.9_AAAAMMGG.mp4`
    - `MoVi_pitch_v0.9.srt`
    - `MoVi_registro_v0.9.md` (registro delle cifre e delle decisioni applicate)
    - `MoVi_copione_v0.9.md` (sceneggiatura finale con parole e durate)
    - `MoVi_animatic_v0.9.mp4`
    - `MoVi_QA_v0.9.md` (rapporto di §11, con licenze e segnaposto residui)
    - `sorgenti/` (progetto dell'animazione, log usati, tracce audio separate)

## 11 · Controllo qualità prima della consegna

Il video si consegna solo se tutte le 32 voci sono superate. `MoVi_QA_v0.9.md` riporta ogni voce con esito, metodo e prova (fotogramma, comando o riga del `.srt`).

| # | Controllo | Metodo | Criterio di superamento | Esito |
| --- | --- | --- | --- | --- |
| Q1 | Durata | `ffprobe -v error -show_entries format=duration -of csv=p=0 file.mp4` | Fra 165,0 e 175,0 s |  |
| Q2 | Parole della voce | Conteggio sul copione finale | Al massimo 340 |  |
| Q3 | Ritmo | Parole diviso durata della voce, per scena | Al massimo 135 parole al minuto in ogni scena |  |
| Q4 | Testo a schermo | Un fotogramma per schermata | Al massimo 16 parole, etichette di stato escluse |  |
| Q5 | Cifre | Voce, schermo e `.srt` confrontati con §5 | Ogni cifra è nel registro v0.9, con il suo stato S, C o P, e usa la sua formulazione |  |
| Q6 | Cifre escluse | Ricerca di ogni cifra di voce, schermo e .srt che non sia in §5 | Assenti |  |
| Q7 | F3 con F4; F5 con il dominio | Voce e schermo della scena 6; schermo dell'atto 2 | F4 segue F3 subito, in voce e a schermo; F5 non compare mai senza la riga del dominio (§3, regola 11) |  |
| Q8 | Limiti dichiarati | Ricerca nel `.srt` e revisione a schermo | L1, L2, L6, L11 e le parti in voce di L4 e L5 in voce; L3, L7, L8, L9 e L10 a schermo |  |
| Q9 | Termini vietati | Ricerca nel `.srt` e nel testo a schermo (§4 e §3, regola 15) | Zero occorrenze |  |
| Q10 | Nomi degli stati | Confronto con §4 | Disco pieno, anello vuoto con "non vista da X s", PREVISTO AMPIO, POSSIBILE PRESENZA, RICOMPARSO · IDENTITÀ PRESUNTA, MOBILE; settori con i tre livelli; nessun "perso", "probabile" o "in movimento" |  |
| Q11 | Niente verde | Un fotogramma al secondo, analisi dei pixel | Nessuna area superiore a 50 pixel con tinta fra 90° e 160° e saturazione oltre il 30 % |  |
| Q12 | "Libero" | Confronto con i log | SUOLO VISTO LIBERO solo dove i log lo dichiarano e solo nel fotogramma corrente; mai su una zona non osservata |  |
| Q13 | Etichette d'onestà | Revisione inquadratura per inquadratura | Ogni inquadratura \[SIMULAZIONE\] o \[ILLUSTRAZIONE\] ha la dicitura per tutta la sua durata |  |
| Q14 | Fedeltà ai log | Nei quattro atti, nella scena 1 e nel tabellone, un fotogramma al secondo confrontato con i log | Stati, ID, età, zone, settori e conteggi del tabellone coincidono; la geometria è quella di D15 e D16 |  |
| Q15 | Disegno della previsione | Revisione degli atti 2 e 3, fotogramma per fotogramma durante l'occlusione | Le nove regole di disegno dell'incertezza di §7 rispettate: nessuna sagoma né cono, tratteggio, sparizione lungo il bordo, trama e parola prima del colore, verifica alla ricomparsa |  |
| Q16 | Etichetta del sensore | Confronto con D13 e con lo stato di F3 e F4 nel registro | Ogni inquadratura della demo dice "sensore ideale" o "profondità simulata"; la continuità della zona si mostra solo su "sensore ideale" |  |
| Q17 | Segnali sonori | Ascolto e forma d'onda della traccia segnali | Nessun suono legato ai cambi di stato o all'incertezza in tutto il video |  |
| Q18 | Loudness | `ffmpeg -i file.mp4 -af ebur128=peak=true -f null -` | Integrata −14 LUFS ± 1; picco reale non oltre −1,0 dBTP |  |
| Q19 | Formato | `ffprobe -show_streams` | 1920 × 1080, 30 fps, yuv420p, H.264, AAC a 48 kHz |  |
| Q20 | Sottotitoli | Validazione del `.srt` e controllo a campione del sincrono | File valido; scarto entro 200 ms; al massimo 2 righe da 42 caratteri |  |
| Q21 | Margini | Sovrapposizione della griglia di sicurezza | Nessun testo fuori dai margini di §7 |  |
| Q22 | Licenze | Elenco nel rapporto | Musica, font ed effetti con licenza e fonte |  |
| Q23 | Consensi | Elenco nel rapporto | Ogni volto riconoscibile ha un consenso scritto; altrimenti sagome |  |
| Q24 | Segnaposto | Ricerca di `[DA FORNIRE` nel video, nel `.srt` e nei titoli | Zero |  |
| Q25 | Committente | Ricerca nel `.srt` e a schermo | Nessun riferimento a ordini, clienti o al committente |  |
| Q26 | Decisioni | Rapporto | D1–D16 registrate con il valore e la fonte |  |
| Q27 | Conflitti | Rapporto | Ogni conflitto fra le fonti è registrato, con la scelta fatta e chi l'ha fatta |  |
| Q28 | Versione unica | Confronto del registro con la proposta usata | Tutte le cifre e i termini vengono dalla stessa versione (oggi v0.9) |  |
| Q29 | Revisione indipendente | Un agente che non ha prodotto il video lo guarda per intero, con la traccia accanto | Risponde sì a quattro domande: in 30 s si capisce che cosa fa il sistema? Ogni richiesta della traccia è riconoscibile? Nessuna frase promette più di quanto il registro permette? Una previsione si distingue sempre da un'osservazione? |  |
| Q30 | Funzioni tagliate | Confronto del video con i gradini al congelamento (V21) | Nessuna funzione assente dalla demo compare nel video, né in voce né a schermo |  |
| Q31 | Caso uncrewed | Ricerca di "senza equipaggio", "uncrewed", "piattaforma" nel .srt e a schermo | Ogni frase sul veicolo dice "fermo" o "configurato, non provato"; nessun mezzo in volo né in moto; il messaggio per l'autopilota porta sempre "in progetto, mai generato" (§3, regole 24–27) |  |
| Q32 | Fonti esterne | Confronto delle righe di fonte con F13–F19 e con l'elenco dei riferimenti | Ogni affermazione su un sistema del dominio ha la sua riga di fonte; tutte le fonti sono "pagina aperta e dato presente"; nessun "conforme" |  |

## 12 · Protocollo per le versioni successive

A ogni nuova versione della proposta (v0.4 e successive) il video si aggiorna solo dove la proposta è cambiata, e un video non mescola mai cifre di due versioni diverse.

1. **Confronta** la nuova versione con quella usata nell'ultimo video, voce per voce: architettura, stati, cifre (valore e stato C/P/S), origine delle prove, limiti, atti della demo, profili, decisioni aperte.
2. **Scrivi il registro delle modifiche in testa al documento, al posto di quello precedente**, una riga per modifica: che cosa cambia · sezione della proposta · sezioni di questo documento toccate · scene toccate.
3. **Aggiorna prima** §4 (lessico e mappa degli stati), §5 (registro) e §6 (requisiti). Poi riscrivi solo le scene toccate di §9 e ricontrolla tempi e parole.
4. **Rispetta i passaggi di stato:**
   - Una cifra che passa da P a C, o da criterio a misura, può diventare un risultato, con la sua origine.
   - L'origine passa da "al calcolatore" a "sul sensore vero" solo se la proposta lo dice per quella cifra.
   - L1 cambia solo quando la proposta riporta prove sul sensore vero o con persone, e solo per quelle prove.
   - Un'inquadratura passa da \[SIMULAZIONE\] a \[RIPRESA REALE\] solo se è stata davvero registrata.
5. **Togli** dal video ogni cifra, componente o limite che la nuova versione non contiene più, anche se era nel video precedente.
6. **Chiudi i punti di §1.** Per ogni punto V aperto a cui lo sciame ha risposto, aggiungi in quella tabella l'esito (accolto, respinto, verificato) e la versione in cui è arrivato.
7. **Dopo la prima ora con l'hardware o dopo la demo**, applica le conseguenze previste:
   - Latenza o cicli al secondo misurati → l'atto 3 può mostrare il ritardo con "sensore vero"; F8 e il criterio dei 15 cicli al secondo (F12) diventano risultati o restano aperti, secondo la misura; L5 si aggiorna.
   - Prove davanti al vetro e al sole → aggiorna L2 e L7 con l'esito misurato.
   - Mano sul sensore e autoverifica all'avvio → il criterio di affidabilità persa (F12) diventa un risultato se il segnale arriva entro 1 s.
   - Rumore di profondità misurato → aggiorna F10 (portata dichiarata) e F5 oltre i 2 m. Pannello sul pavimento segnato col nastro → la prova di V14 sul sensore vero.
8. **Riesegui** il controllo di §11 per intero e consegna i file con la nuova versione nel nome.

A ogni nuova versione dello stato del progetto o dell'elenco dei riferimenti: ricontrolla F1–F12 sullo stato, F13–F19 sull'elenco (una fonte che perde "pagina aperta e dato presente" esce dal video), e i cinque punti aperti di §1. Se un punto di forza di §1 perde la sua prova, esce dal video insieme alla scena che lo porta.

In caso di dubbio su una modifica, l'agente di produzione non decide: registra il dubbio e lo chiede allo sciame.
