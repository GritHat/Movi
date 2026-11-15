# MoVi — prototipo simulato (gruppo SDMs)

Un sistema di percezione che **dichiara ciò che non ha osservato**. Di ogni oggetto seguito dice se lo vede, se non
lo vede ma indica una zona dove può essere, o se non lo sa. Tre principi che nessun modulo può scavalcare:
ciò che non è osservato non è mai «libero»; l'avviso di possibile presenza si toglie solo guardando; nessuna
etichetta di classe riduce un avviso.

**Che cosa NON è.** Non c'è nessun sensore fisico: i dati sono simulati dalle schede tecniche o presi da archivi
pubblici. Le etichette di classe sono assegnate a mano da file: il classificatore non è realizzato (lavori futuri).
Niente qui è provato su hardware. Ambito: osservazione, monitoraggio, ispezione, navigazione sicura e avviso;
nessuna uscita è un comando.

**Stato: MODO CORTO COSTRUITO** (15 novembre 2026, `sciame-sviluppatore`). Funzionano: la catena riusata con le
correzioni di f12, la salute del sensore col controllo all'avvio, la regola del «libero» (PR4, dietro interruttore),
il predittore della zona (porto SEMPLIFICATO di sd-1, dietro interruttore, non ancora confrontato col banco in C),
i livelli per settore, gli eventi «osservato»/«dedotto», le etichette a mano, il tabellone «dentro la zona: k su n»,
le tre viste e il filmato. **MODO LUNGO COSTRUITO** (15-11-2026, stesso ruolo): sezione «Modo a lunga portata» qui sotto. Misure e limiti: `.sciame/20261114-1301-percezione-challenge/f16-prototipo/10-corto-raggio/CORTO_RAGGIO.md`.

## Comandi

Da questa cartella. `sh movi.sh …` equivale a `python -m movi …` con l'interprete dello sciame in modo isolato
(`-I`: con `-I` la cartella corrente non è nel percorso dei moduli, e il lanciatore la aggiunge).

    sh movi.sh scene                                             # elenco delle scene d'esempio
    sh movi.sh esegui passa_dietro_e_ricompare --config scene/passa_dietro_e_ricompare.json
                                                                 # scrive uscite/<scena>/registro.jsonl
    sh movi.sh tabellone uscite/<scena>/registro.jsonl           # «dentro la zona: k su n», con Wilson al 95 %
    sh movi.sh mostra uscite/<scena>/registro.jsonl [--filmato]  # tre viste: scena vera, console, settori
    sh movi.sh convalida uscite/<scena>/registro.jsonl           # forma e principi
    sh prova_tutto.sh                                            # prove + tutte le scene con filmato
    PY=… ; $PY -I -B prove/prova_principi.py [rapida]           # principi, salute, etichette, tempo per ciclo
    $PY -I -B prove/misura_corto.py zona_libero b 100 x.json     # un passaggio nuovo del simulatore, misurato
    $PY -I -B prove/riassumi_misure.py uscite/misure             # somma con Wilson al 95 %

## Modo a lunga portata (aerei e droni; poi auto e treni) — CASO CENTRALE

Stessi comandi e stesso registro del corto raggio. Ogni scena è una configurazione in `scene/lp_*.json`:

    sh movi.sh scene | grep lungo                                # elenco
    sh movi.sh esegui lp_A1 --config scene/lp_A1.json --uscita uscite/lp_A1 --celle
    sh movi.sh tabellone uscite/lp_A1/registro.jsonl             # «dentro la zona» e «dentro l'avviso», Wilson 95 %
    sh movi.sh convalida uscite/lp_A1/registro.jsonl             # principi (avviso tolto senza guardare, ecc.)
    sh movi.sh mostra uscite/lp_A1/registro.jsonl --filmato --uscita uscite/lp_A1/viste
    sh prove/scene_lunghe.sh lp_A1                               # i quattro insieme
    $PY -I -B prove/prova_lunga.py [A1,S1,…] [--etichette]       # stessi cicli degli esemplari di f15; etichette

| Scena | Che cosa |
|---|---|
| `lp_A1` … `lp_A4`, `lp_S1`, `lp_S2` | i sei scenari di `scenari.json` (multisensore «alta», passaggio 0 = esemplare di f15, chiamante prudente) |
| `lp_E1` … `lp_E5` | collisione fra droni con detriti, avaria con fiammata, fumo/nebbia/pioggia, drone nel fumo, passaggio ravvicinato di controllo |
| `lp_A1_sensore_singolo` | sensore singolo (configurazione «min») |
| `lp_A1_non_cooperante` | mezzo non cooperante (niente Remote ID) |
| `lp_A1_perdita_sensore`, `lp_A1_pioggia` | radar principale spento 15 s; pioggia forte sul radar |
| `lp_A1_drone_piccolo` | drone C0 (1,6·10⁻⁴ m²) |
| `lp_A1_interfaccia`, `lp_S1_interfaccia` | chiamante «interfaccia» di f15: mostra la falla P2 (avviso tolto senza guardare) |
| `lp_A1_senza_etichette` | misure senza classe: l'avviso non cambia |
| `lp_pub_drone` | REGISTRAZIONE PUBBLICA: volo vero CMU (CC BY 4.0) con ostacolo VIRTUALE; rilevazioni simulate |

Le condizioni stanno in `sorgente.condizione` (`configurazione` min|alta, `cooperante`, `perdita_sensore`, `pioggia`,
`drone_piccolo`, `etichette` a_mano|nessuna, `comportamento`). Il codice riusato le lega all'indice del passaggio: si
sceglie il primo che le soddisfa e il registro lo dichiara (con il comportamento del bersaglio che ne segue). Chi
riceve l'avviso: `profilo_ricevente` (profili di `regole_lunga_portata.json`); la distanza d'avviso richiesta è quella
dello scenario, il conto col profilo è nell'intestazione.

**Che cosa è simulato.** Tutto: sensori (dalle schede di f15/02-sensori, 46 % dei campi «ipotesi»), rilevazioni,
falsi ritorni, salute, meteo; la verità del moto è scritta a mano (scenari) o, in `lp_pub_drone`, presa da una
traiettoria pubblica con ostacolo virtuale. Etichette a mano dalla verità (`etichette/lunga_portata.json`).
**Che cosa non è provato.** Niente su un sensore fisico; nessuna rilevazione reale (in f15/01-dati non ce ne sono);
le camere orientate dal radar usano l'associazione vera (ottimista); i falsi avvisi del radar 4D e del LiDAR sono
alti (PROVE § 3.7); le falle P4, P5, E1, E2 di PROVE restano. Misure e confronto: `.sciame/…/f16-prototipo/20-lunga-portata/LUNGA_PORTATA.md`.

## Struttura

    movi/            il pacchetto (solo colla e parti nuove)
      config.py        configurazione all'avvio, interruttori delle regole, dichiarazioni
      sorgenti.py      sorgenti intercambiabili: sequenza, simulata, registrazione pubblica, scena a lunga portata
      nucleo.py        interfaccia comune dei due modi
      corto.py         modo a corto raggio: compone il codice riusato
      lungo.py         modo a lunga portata: esegue i passaggi di f15 e li osserva (adattatore)
      mostra_lungo.py  pianta e console dell'operatore del modo lungo
      predittore_zona.py   porto in Python del nucleo del predittore in C (parte spento)
      etichette.py     etichette a mano da file
      livelli.py       livello per settore
      eventi_registro.py   eventi «osservato» / «dedotto»
      registro.py      IL FORMATO: una riga JSON per fotogramma, unico per i due modi
      tabellone.py, mostra.py, esegui.py, scene.py, __main__.py
    riuso/           codice dello sciame copiato TALE E QUALE (non modificare: IMPRONTE.txt lo controlla)
    scene/           una configurazione per scena d'esempio + SCENE.json
    etichette/       etichette a mano
    prove/           prove del prototipo
    uscite/, dati/   prodotti (non in git)

## Provenienza del codice riusato (`riuso/`)

Copiato il 15-11-2026 da `.sciame/20261114-1301-percezione-challenge/`, senza cambiare un byte
(controllo: `cd riuso && sha256sum -c --quiet IMPRONTE.txt`).

| In `riuso/` | Origine | Che cos'è |
|---|---|---|
| `catena/*.py`, `esito_prove.txt` | `f12-integrazione/06-identita/catena/` (corregge `f10-dati/10-catena/`) | catena di riferimento: mappa a quattro stati, gruppi, inseguimento, possibile presenza; 25 prove |
| `11-simulatore/{simsens,catalogo,genera}.py` | `f10-dati/11-simulatore/` | simulatore della camera di profondità dalle schede |
| `02-sensori/parametri_sensori.json` | `f10-dati/02-sensori/` | parametri dei sensori (dalle schede tecniche) |
| `03-infrastruttura/{controlla_sequenza.py, formato_sequenza.md, esempio_sequenza/}` | `f10-dati/03-infrastruttura/` | formato comune delle sequenze |
| `libero/libero.py` | `f12-integrazione/03-libero/` | regola del «libero» della cella dal solo fotogramma |
| `eventi/eventi.py` | `f7-estensione/04-requisiti/` | registro degli eventi |
| `c/insieme.c`, `c/leggi.py` | `f12-integrazione/02-prova-insieme/` | banco in C del predittore della zona (prova d'insieme) |
| `c/comp.c`, `c/gen.h` | `f8-continuita/13-soluzione/` | banco in C di confronto dei predittori (origine di sd-1) |
| `profili/{classi.json, profili_portatore.json}` | `f14-classificazione/01-profili/` | profili di classe e di chi porta il sensore (valori a priori) |
| `lunga_portata/04-moto/{movi_lp.py, regole_lunga_portata.json}` | `f15-lunga-portata/04-moto/` | nucleo multisensore a lunga portata e regole |
| `lunga_portata/10-simulatore/{sim_lp, prove_lp, eventi_lp, movi_lp_import}.py`, `esemplari/` | `f15-lunga-portata/10-simulatore/` | simulatore dei sensori, passaggi A1–A4/S1/S2 ed E1–E5, esemplari di confronto |
| `lunga_portata/02-sensori/parametri_lunga_portata.json` | `f15-lunga-portata/02-sensori/` | schede dei sensori (con fonte e ipotesi) |
| `lunga_portata/03-scenari/scenari.json` | `f15-lunga-portata/03-scenari/` | scenari A1–A4, S1, S2 |
| `lunga_portata/40-eventi/…` | `f15-lunga-portata/40-eventi/` | effetti, regole e scenari E1–E5, `frammenti.py` |
| `lunga_portata/01-dati/traiettorie/`, `PROVENIENZA.md` | `f15-lunga-portata/01-dati/` | traiettorie pubbliche (licenze in PROVENIENZA.md; impronte in `IMPRONTE_TRAIETTORIE.txt`) |

I nomi delle cartelle `11-simulatore`, `02-sensori`, `03-infrastruttura` restano quelli d'origine perché il codice
riusato si cerca con percorsi relativi (`simsens.py` riga 28, `genera.py` riga 26, `prove.py` righe 36 e 101).

Le sequenze simulate (1,8 GB) NON sono copiate: le scene puntano a `f10-dati/11-simulatore/sequenze/` o si rigenerano
con `riuso/11-simulatore/genera.py`. Licenza dei dati generati: nessun vincolo (lo dice il loro `meta.json`).

L'architettura e i motivi: `.sciame/20261114-1301-percezione-challenge/f16-prototipo/01-architettura/ARCHITETTURA.md`.
