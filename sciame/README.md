# Lo sciame di agenti per Claude Code (versione 3.1)

Uno sciame di 54 ruoli specialistici, in otto nuclei, che un coordinatore convoca per una richiesta con una di
quattro strategie: **esperto singolo**, **convocazione classica**, **convocazione completa**, oppure **auto**, quando
la scelta la fa il coordinatore. Il coordinatore è la sessione di Claude Code aperta nel progetto; gli agenti sono i
suoi sottoagenti `sciame-<sigla>`.

**Il setup e l'avvio sono tutti in `sciame.sh`:** `bash sciame/sciame.sh aiuto` li stampa. In breve:

```
bash sciame/sciame.sh installa               # una volta per progetto
bash sciame/sciame.sh singolo  "richiesta"   # esperto singolo
bash sciame/sciame.sh classica "richiesta"   # convocazione classica
bash sciame/sciame.sh completa "richiesta"   # convocazione completa
bash sciame/sciame.sh auto     "richiesta"   # sceglie il coordinatore
```

Dentro Claude Code le stesse convocazioni sono `/sciame-singolo`, `/sciame-classica`, `/sciame-completa` e `/sciame`.

## Le strategie

Sono definite in `PIPELINE.md`; qui c'è ciò che succede in ciascuna.

**Esperto singolo.**
1. Il coordinatore sceglie il ruolo più adatto, o prende quello nominato.
2. Gli scrive una consegna completa: la domanda, gli ingressi, il risultato atteso, i limiti.
3. Lo specialista lavora e si rilegge con le «domande che si pone sempre» della sua scheda.
4. Il coordinatore controlla il risultato contro la domanda, con al più una ripresa.

**Convocazione classica.** È una pipeline a grafo, con un cancello dopo ogni fase.

| fase | che cosa succede |
|---|---|
| f0 | il contratto: una domanda, il criterio che decide, gli ingressi, i vincoli, la quota, il profilo |
| f1 | due corsie cieche in parallelo: la conservativa (gli specialisti del profilo) e la divergente (il creativo e il rovesciatore) |
| f2 | un ruolo senza idee in gara le traduce in schede, gli autori firmano, l'arbitro fa il triage, l'avversario esegue i falsificatori, si scelgono al più tre ipotesi più una radicale |
| f3 | una squadra per ipotesi: soluzione, verifica, piano delle misure, attacco |
| f4 | le prove, dalla più economica: controprove, debugger sulle anomalie, misure |
| f5 | i verdetti per proprietà (correttezza, completezza, efficacia, costo) e la chiusura dell'arbitro |
| f6 | il coordinatore integra ciò che la richiesta permette e ti porta le decisioni |

**Convocazione completa.**
1. Il contratto, come nella classica.
2. La tornata globale: tutti i ruoli salvo l'arbitro, a ondate di cinque, ciechi fra loro, con al più mezza pagina
   ciascuno. Chi non ha niente da dire scrive «non pertinente» in una riga.
3. Il consolidamento dell'arbitro, per nucleo e poi d'insieme: fatti, contraddizioni, idee candidate, domande aperte.
4. Le idee candidate entrano nella classica da f2.

**Auto.** Singolo se la richiesta è chiara e di un solo campo; classica se c'è da decidere o un errore costa; completa
se la domanda è strategica e tocca almeno tre nuclei. In dubbio, la più economica.

Nella classica e nella completa il coordinatore prepara la convocazione con `convoca.py`, che scrive le consegne in
`.sciame/`, tiene cieche le corsie e controlla i cancelli. `python3 -I sciame/convoca.py --help` ne dice i comandi.

## I ruoli

| nucleo | ruoli |
|---|---|
| teorico e formale | formalista, logico, matematico, sistemi-complessi, informazione |
| IA e modelli | llm, generativi, ml, inferenza, machine-intelligence |
| sperimentale e delle misure | linguaggi, prestazioni, ottimizzazione, statistico, metrologo |
| software e sistemi | architetto, sviluppatore, tester, sicurezza, infrastruttura, dati, interfacce, embedded |
| conoscenza e comunicazione | ricercatore, redattore, didatta, traduttore, visualizzatore, esperto-dominio, marketing, videomaker, comunicazione |
| progetto e decisione | requisiti, pianificatore, economista, normativo |
| critico e divergente | avversario, rovesciatore, fonti, arbitro, creativo, debugger, lettore |
| percezione, stima e movimento | visione, kalman, lidar, sensori, nuvole-punti, fusione, slam, tracciamento, scene-dinamiche, tempo-reale, validazione |

Ogni agente si chiama `sciame-<sigla>`. `bash sciame/sciame.sh ruoli` li stampa con il nome intero e i profili.

Il nucleo della percezione, della stima e del movimento:

| agente | di che cosa risponde |
|---|---|
| `sciame-visione` | visione artificiale: rilevamento, segmentazione, flusso ottico, profondità, geometria a più viste |
| `sciame-kalman` | stima dello stato: filtri di Kalman (lineare, esteso, unscented, a stato d'errore), particelle, lisciatori, coerenza |
| `sciame-lidar` | hardware dei LiDAR: principio di misura, scansione, portata, tempo per punto, artefatti, sicurezza ottica, montaggio |
| `sciame-sensori` | camere, radar, unità inerziali, GNSS, camere a eventi: rumore, deriva, sincronizzazione |
| `sciame-nuvole-punti` | nuvole di punti: correzione del movimento, suolo, raggruppamento, registrazione, rilevamento 3D, occupazione |
| `sciame-fusione` | fusione e calibrazione: estrinseche, ritardi, sistemi di riferimento, architettura della fusione |
| `sciame-slam` | moto proprio e mappa: odometria visiva, inerziale e LiDAR, SLAM, chiusura dei cicli |
| `sciame-tracciamento` | più oggetti nel tempo: associazione, vita delle tracce, modelli di moto, identità, previsione |
| `sciame-scene-dinamiche` | che cosa si muove o è cambiato quando anche chi osserva si muove: moto proprio tolto, oggetti mobili, confronto fra passaggi |
| `sciame-tempo-reale` | la catena nel tempo disponibile: latenza, marche temporali, code, calcolo a bordo |
| `sciame-validazione` | come si prova che funziona: verità di riferimento, dati, scenari, simulazione, metriche |

I profili dicono quali ruoli lavorano in ogni fase della classica. Quelli della percezione:

| profilo | per | corsia conservativa | responsabile della soluzione |
|---|---|---|---|
| `percezione` | rilevare, segmentare e riconoscere da immagini e nuvole di punti | visione, nuvole-punti | visione |
| `movimento` | scene che cambiano con il movimento: oggetti mobili, cambiamenti, eventi | scene-dinamiche, slam | scene-dinamiche |
| `stima` | stimatori dello stato, filtri di Kalman, fusione delle misure | kalman, fusione | kalman |
| `tracciamento` | seguire più oggetti nel tempo | tracciamento, kalman | tracciamento |
| `localizzazione` | moto proprio, odometria, SLAM, mappe | slam, kalman | slam |
| `sensori` | scelta, montaggio, sincronizzazione e calibrazione dei sensori | lidar, sensori | lidar |
| `latenza` | percezione in tempo reale | tempo-reale, prestazioni | tempo-reale |

Gli altri sedici (`codice`, `difetto`, `architettura`, `prova`, `dati`, `ia`, `ricerca`, `scrittura`, `studio`,
`decisione`, `piano`, `sicurezza`, `dispositivo`, `interfaccia`, `video`, `generale`) sono nella tabella di `PIPELINE.md`.

## I file di questa cartella

| file | che cosa contiene |
|---|---|
| `sciame.sh` | il setup e l'avvio: installa, avvia le convocazioni, controlla, rigenera, rimuove |
| `AGENTI.md` | le schede dei 54 ruoli e i confini fra ruoli vicini: la fonte unica degli agenti |
| `PREAMBOLO.md` | le regole che ogni agente legge prima di lavorare; le «regole in breve» finiscono dentro ogni agente |
| `PIPELINE.md` | le quattro strategie, le fasi, i cancelli, i profili per tipo di compito |
| `ISTRUZIONI_COORDINATORE.md` | che cosa fa il coordinatore |
| `SCHEDA_IPOTESI.md` | il modello del dossier di un'ipotesi |
| `convoca.py` | prepara una convocazione e ne controlla i cancelli |
| `genera_agenti.py` | genera il catalogo, gli agenti e le skill |
| `catalogo.json`, `VERSIONE` | generati: i ruoli, i profili e i testi, per `convoca.py` e per chi orchestra da sé |

Fuori da questa cartella lo sciame ha solo ciò che se ne genera: `.claude/agents/sciame-*.md` e
`.claude/skills/sciame*/SKILL.md`.

## Modificare lo sciame

Le schede e i documenti sono la fonte unica: gli agenti e le skill non si modificano a mano. Dopo una modifica,
`bash sciame/sciame.sh rigenera`.

- **Un ruolo nuovo** è una scheda in `AGENTI.md`, sotto il suo nucleo, con il titolo `### N. Nome — \`sciame-sigla\`` e
  le righe **In breve**, **Nucleo** e **Parole chiave**. I numeri sono in fila.
- **Un profilo nuovo** è una riga della tabella di `PIPELINE.md`, con le sigle dei ruoli in ogni colonna.
- **I testi delle skill** vengono dai blocchi fra i segni `<!-- … -->` di `PIPELINE.md` e di
  `ISTRUZIONI_COORDINATORE.md`.

`sciame.sh` porta in fondo i documenti di fabbrica: `installa --forza` li rimette, e mette da parte quelli modificati.

## Da dove viene

Lo sciame viene da quello del progetto «Decodifica vincolata con budget di token» (lo «sciame ETH» delle righe
**Origine** nelle schede: 21 ruoli, pipeline v2.4.1). La 3.0 l'ha reso valido per progetti di ogni tipo, con 40 ruoli
e quattro strategie. La 3.1 lo rende portabile e aggiunge il nucleo della percezione, della stima e del movimento.
