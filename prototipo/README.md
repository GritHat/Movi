# MoVi — prototipo simulato (gruppo SDMs)

Un sistema di percezione che **dichiara ciò che non ha osservato**. Di ogni oggetto seguito dice se lo vede, se non
lo vede ma indica una zona dove può essere, o se non lo sa. Tre principi che nessun modulo può scavalcare:
ciò che non è osservato non è mai «libero»; l'avviso di possibile presenza si toglie solo guardando; nessuna
etichetta di classe riduce un avviso.

**Che cosa NON è.** Non c'è nessun sensore fisico: i dati sono simulati dalle schede tecniche o presi da archivi
pubblici. Le etichette di classe sono assegnate a mano da file: il classificatore non è realizzato (lavori futuri).
Niente qui è provato su hardware. Ambito: osservazione, monitoraggio, ispezione, navigazione sicura e avviso;
nessuna uscita è un comando.

**Stato: SCHELETRO** (15 novembre 2026). Funzionano: la copia del codice riusato con le sue prove, la configurazione,
il formato del registro con la sua convalida, l'adattatore catena -> registro, la riga di comando. Il resto ha le
firme e le docstring e risponde «non ancora costruito» (codice d'uscita 4).

## Comandi

Da questa cartella. `sh movi.sh …` equivale a `python -m movi …` con l'interprete dello sciame in modo isolato
(`-I`: con `-I` la cartella corrente non è nel percorso dei moduli, e il lanciatore la aggiunge).

    sh movi.sh scene                                             # elenco delle scene d'esempio
    sh movi.sh esegui passa_dietro_e_ricompare --config scene/passa_dietro_e_ricompare.json
                                                                 # scrive uscite/<scena>/registro.jsonl
    sh movi.sh tabellone uscite/<scena>/registro.jsonl           # «dentro la zona: k su n», con Wilson al 95 %
    sh movi.sh mostra uscite/<scena>/registro.jsonl [--filmato]  # tre viste: scena vera, console, settori
    sh movi.sh convalida uscite/<scena>/registro.jsonl           # forma e principi
    sh prova_tutto.sh                                            # prove + tutte le scene (scheletro: 20–27 s)

## Struttura

    movi/            il pacchetto (solo colla e parti nuove)
      config.py        configurazione all'avvio, interruttori delle regole, dichiarazioni
      sorgenti.py      sorgenti intercambiabili: sequenza, simulata, registrazione pubblica, scena a lunga portata
      nucleo.py        interfaccia comune dei due modi
      corto.py         modo a corto raggio: compone il codice riusato
      lungo.py         modo a lunga portata: adattatore di movi_lp.py
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
| `lunga_portata/` (da aggiungere al passo 2) | `f15-lunga-portata/04-moto/movi_lp.py` e simulatore | nucleo multisensore a lunga portata |

I nomi delle cartelle `11-simulatore`, `02-sensori`, `03-infrastruttura` restano quelli d'origine perché il codice
riusato si cerca con percorsi relativi (`simsens.py` riga 28, `genera.py` riga 26, `prove.py` righe 36 e 101).

Le sequenze simulate (1,8 GB) NON sono copiate: le scene puntano a `f10-dati/11-simulatore/sequenze/` o si rigenerano
con `riuso/11-simulatore/genera.py`. Licenza dei dati generati: nessun vincolo (lo dice il loro `meta.json`).

L'architettura e i motivi: `.sciame/20261114-1301-percezione-challenge/f16-prototipo/01-architettura/ARCHITETTURA.md`.
