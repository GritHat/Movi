# ARCHITETTURA del prototipo simulato MoVi — `sciame-architetto`, f16-prototipo/01

15 novembre 2026, 00:01–00:12 (`date -Is`; la consegna dice «14 novembre»: l'orologio era già oltre mezzanotte).
Scheletro: `/home/fede/Scrivania/ed/GitHub/Movi-Hackthon/prototipo`. Previsioni ed esiti: `PREVISIONI.md`, qui accanto.
**Tutto è simulazione, conto o lettura di codice: niente è provato su un sensore fisico, niente è «validato».**

## 0. Cambi di stato e regole violate

- **Previsioni:** arch-P3, P5, P6 reggono. **arch-P2 e arch-P4 smentite al primo lancio** e corrette (sotto, critiche 1 e 2). arch-P1: un fallimento al primo lancio dovuto al carico della macchina, mostrato lanciando l'originale sul posto.
- **Regole.** (a) Ho scritto anche codice vero, non solo firme: `registro.py`, `config.py`, `riuso.py`, la riga di comando e `corto.parametri_da_config`: servivano per provare il formato. (b) Un `rm` di pulizia dentro `prototipo/uscite` è stato negato dal controllo di sicurezza: non l'ho aggirato; restano lì i testi delle prove (cartella esclusa da git) e l'eseguibile `riuso/c/insieme` (escluso da git). (c) Ho letto `f15-lunga-portata/03-scenari/scenari.json` e le firme di `04-moto/movi_lp.py`, file ancora in lavorazione di altri ruoli: solo lettura. Nessuna richiesta alla rete; niente git, niente sudo.

## 1. Critiche al materiale di partenza (ciascuna con la prova)

1. **`python -I -m movi` non può funzionare come scritto nella consegna.** Con `-I` la cartella corrente non è nel percorso dei moduli: «No module named movi» (`prototipo/uscite/03_importa.txt` del primo lancio). Rimedio: `sh movi.sh <comando>`, che aggiunge la cartella in modo esplicito e chiama `runpy`. Stessi argomenti.
2. **La catena ha uno stato di traccia in più di quelli documentati nell'uscita:** `affidabilita_persa` (`inseguimento.py` riga 218: senza misura e la cella dell'ultima misura è «non osservato»). Nel registro diventa «previsto ampio», senza punto.
3. **Senza le correzioni di f12 il pavimento vuoto simulato produce fantasmi:** 66 nascite e 28 conferme in 30 fotogrammi su `d435i_nom__pavimento_vuoto`; con i sette campi «correzioni f12» accesi, 0 e 0 (un lancio per braccio; `prove/prova_registro.py <seq> - senza_correzioni`). I valori di base di `Parametri` sono «tutte spente» (`parametri.py` righe 54–64): chi compone deve accenderle, e il prototipo lo fa da configurazione.
4. **«Ricomparso · identità presunta» oggi non esce sulla sequenza naturale.** Su `pannello_a12__s00` con le correzioni: 0 eventi «riaggancio», 8 «identità ambigua», 3 nascite. La scena mostrerà ciò che il codice fa; non si ritocca.
5. **Il predittore in C non è una libreria:** `insieme.c` (371 righe) e `comp.c` (635) sono banchi con stato globale, generatore di percorsi e `main`. Il nucleo da portare è di 43 righe (162–205) più la libreria dei percorsi.
6. **Le sequenze simulate pesano 1,8 GB** (`du -sh`, 164 voci): non si copiano.

## 2. La decisione

**Requisito che decide la forma:** un solo REGISTRO per due nuclei diversi, da cui si disegna il video e si rifà il tabellone senza rilanciare niente. Tutto il resto segue.

```
 sorgenti.py ──Fotogramma──▶ nucleo.py (interfaccia) ──riga──▶ registro.py ──▶ registro.jsonl ──▶ tabellone.py
  sequenza | simulata |        ├ corto.py  = riuso/catena + libero + eventi + predittore        └─▶ mostra.py
  pubblica | scena_lp          └ lungo.py  = adattatore di movi_lp.py                      (leggono SOLO il registro)
        ▲                           ▲
     config.py (scenario, classi ammesse, profilo del portatore, interruttori)   etichette.py (a mano, da file)
```

**(1) Pacchetto** (`prototipo/movi/`, 764 righe con le docstring).

| Modulo | Responsabilità | Stato |
|---|---|---|
| `config.py` | `Configurazione` letta da JSON all'avvio: modo, scenario, sorgente, classi ammesse, profilo di chi porta il sensore (controllati contro `riuso/profili/*.json`), file delle etichette, interruttori, seme. `dichiarazioni()` e `impronta()` | funziona |
| `sorgenti.py` | `Sorgente` (meta, iterazione di `Fotogramma`, `verita(indice)`): `SorgenteSequenza` (formato comune; serve anche la registrazione pubblica già convertita, con origine e licenza in `meta`), `SorgenteSimulata` (catalogo del simulatore), `SorgenteLungaPortata` (`scenari.json`) | firme |
| `nucleo.py` | interfaccia: `intestazione()`, `passo(fotogramma, verita) -> riga`, `griglia_stati()`. Il nucleo non usa mai la verità per decidere | funziona (fabbrica) |
| `corto.py` | compone `Catena.ciclo` → `registro.da_catena` → salute del sensore → `livelli` → eventi → etichette | `parametri_da_config` funziona; il resto firme |
| `lungo.py` | SOLO adattatore di `movi_lp.py` verso l'interfaccia e il registro | firme |
| `predittore_zona.py` | porto in Python di sd-1 con la forma dell'aggancio `fabbrica_predittore` | firme |
| `etichette.py`, `livelli.py`, `eventi_registro.py` | etichette a mano; livello per settore; eventi «osservato» / «dedotto» | firme |
| `registro.py` | il formato, `valida_riga`, `valida_sequenza`, `da_catena`, `Scrittore`, `leggi` | funziona |
| `tabellone.py`, `mostra.py`, `esegui.py`, `scene.py`, `__main__.py` | comandi | `wilson`, `riga_fissa`, `esegui`, `scene`, `convalida` funzionano |

**Interruttori** (`config.INTERRUTTORI`, con il motivo scritto accanto): `correzioni_f12` parte **acceso** (critica 3); partono **spenti** `predittore_zona`, `c7_identita_al_ritorno` (SOLUZIONE_V3 §1.1: spente se la prova d'ingresso del rumore non passa), `libero_dal_fotogramma`, `fascia_di_scenario`, `regione_per_classe`. Nessun interruttore tocca i tre principi: li controlla `valida_riga` su ogni riga scritta.

**(2) Riuso senza riscrivere.** Il codice sta in `prototipo/riuso/`, copiato byte per byte (61 file, 1,8 MB con l'esempio; `sha256sum -c riuso/IMPRONTE.txt` è il passo 0 di `prova_tutto.sh`), con i nomi di cartella d'origine dove il codice si cerca per percorso relativo. `movi/riuso.py` lo carica senza toccarlo (importazioni piatte, via `sys.path`). La tabella della provenienza è nel `README.md`. Le 25 prove della catena passano dal nuovo posto.
**Predittore: porto in Python del solo nucleo (43 righe di C), il banco in C resta e si chiama come programma dal tabellone.** Motivo: la catena ha già l'aggancio (`presenza.py` righe 42–56: `passo(t, ciclo, griglia) -> Previsione`); un porto piccolo entra lì, una libreria C chiederebbe di riscrivere il banco. Fino al confronto col banco l'interruttore resta spento e vale `PredittoreVelocitaCostante`, che esiste ed è provato: la prima consegna non dipende dal porto.

**(3) Formato del registro** (`movi/registro.py`, docstring = specifica). Riga 1 intestazione (configurazione intera, dichiarazioni, principi, griglie, riferimento, ostacoli, sensori); una riga per fotogramma; ultima riga riassunto. Metri in pianta, x a destra, y in avanti, quota facoltativa; gradi; secondi.

| Campo | Contenuto |
|---|---|
| `tipo, modo, indice, t` | `fotogramma`; `corto` o `lungo` |
| `dichiarazioni` | dati (simulati o pubblici), etichette (a mano o assenti), regole accese, impronta della configurazione: **in ogni riga** |
| `verita` | `null` oppure oggetti veri con id, classe, posizione, visibile |
| `sensori[]` | id, tipo, `salute` (in_salute, degradato, affidabilita_persa), causa, validi, età del dato |
| `affidabilita` | `ok` o `persa` (stato del sistema) |
| `celle` | griglia, conteggi per stato, `rle` facoltativo (griglia intera), `per_sensore` nel modo lungo |
| `settori[]` | azimut, `livello` (visto_libero_fino_a, attenzione, zona_non_verificata, affidabilita_persa), `d_m`, motivo |
| `tracce[]` | id, classe, `origine_etichetta` (a_mano, assente), `stato` (in_conferma, vista, vista_in_parte, non_vista, previsto_ampio, ricomparsa), `non_vista_da_s`, `identita` (certa, presunta, ambigua), pos, vel, `regione`, sensori |
| `avvisi[]` | `possibile_presenza`, traccia, età, `forma` |
| `eventi[]` | t, tipo, `come_lo_so` (osservato, dedotto), traccia, settore |
| `tabellone` | `dentro_la_zona: {k, n}` cumulato |

Forme di regioni e avvisi: `cerchio`, `poligono`, `settore_anulare`, `celle`. Controlli di principio in `valida_riga`: con affidabilità persa nessuna cella libera o occupata e nessun settore «visto libero»; «visto libero» solo con la distanza; «previsto ampio» senza punto; ogni evento dice come lo si sa. `da_catena` è prudente: senza `livelli.py` nessun settore esce «visto libero».
**Prova:** 0 righe non valide su 286 in cinque sequenze simulate (Wilson 95 %: 0–1,3 %); è una prova di forma, scritta dallo stesso autore dello schema. Peso: 407 kB per 47 fotogrammi senza la griglia intera.

**(4) Comandi.** `sh movi.sh esegui <scena> --config scene/<scena>.json [--uscita …] [--celle]`; `sh movi.sh tabellone <registro>… [--banco "prova geo=T n=400"]`; `sh movi.sh mostra <registro> [--filmato] [--ogni N]` (tre viste a 1920×1080: scena vera, console, settori); in più `convalida` e `scene`. `sh prova_tutto.sh`: impronte, 25 prove della catena, banco in C, importazioni, registro, poi ogni scena (esegui, tabellone, mostra). Oggi 20–27 s, esito 0, undici scene «non ancora costruito» (codice 4, non conta come fallimento).

**(5) Scene d'esempio** (`scene/SCENE.json`).

| Scena | Sorgente | Stato |
|---|---|---|
| `pavimento_vuoto` | `d435i_nom__pavimento_vuoto` | sequenza pronta |
| `passa_dietro_e_ricompare` | `d435i_nom__pannello_a12__s00` | sequenza pronta (critica 4) |
| `resta_dietro` | `d435i_nom__pannello_d__s00` (si ferma dietro il pannello) | sequenza pronta |
| `mano_sul_sensore` | `d435i_nom__sensore_coperto` (coperto da 1,0 a 2,2 s) | sequenza pronta |
| `due_persone` | voce nuova del catalogo con due persone | **da generare** (nel catalogo non c'è) |
| `lp_A1` multirotore dietro un edificio; `lp_A2` aereo in rullaggio dietro un hangar; `lp_A3` aereo in finale e drone sotto la copertura; `lp_A4` portatore in volo stazionario (solo analisi); `lp_S1` auto dietro un camion; `lp_S2` treno dietro un convoglio | `scenari.json` letto alle 00:05 (in lavorazione: rileggere) | da costruire |

**(6) Dichiarato sempre** (riga fissa di `mostra.riga_fissa`, e `dichiarazioni` in ogni riga): «DATI SIMULATI (o: dati pubblici, sensore simulato) — nessun sensore fisico · etichette a mano (classificatore non realizzato, lavori futuri) · regole accese: … · spente: … · config xxxxxxxx». Nell'intestazione anche scenario, profilo di chi porta il sensore e i tre principi.

**Alternative scartate.** (a) Riscrivere la catena come pacchetto con importazioni relative: più pulito, ma tocca codice provato e rompe la provenienza. (b) Un registro per modo: due visualizzatori e due tabelloni. (c) Predittore in C come libreria con `ctypes`: va riscritto il banco per togliere lo stato globale. (d) Portare tutto il banco in Python: 371 righe per rifare ciò che il C fa in secondi.
**Come si torna indietro.** Ogni scelta è locale: l'adattatore di un modo è un file; il predittore è un interruttore; il formato ha `formato: 1` nell'intestazione; `riuso/` si ricopia dall'origine.

## 3. Stati proposti

| Enunciato | Stato |
|---|---|
| La copia del codice riusato è identica all'origine e le sue prove passano | **verificato** (61 impronte; 25 prove; simulazione) |
| Il formato del registro basta al modo corto | **sostenuto dai dati** (0 su 286 righe, cinque sequenze simulate; solo forma) |
| Il formato basta al modo lungo | **non risolto**: `movi_lp.py` è in lavorazione; lo decide la prima scena `lp_A1` scritta e convalidata |
| Il porto del predittore equivale al banco in C | **non risolto**: non scritto; lo decide `prove/prova_predittore.py` |
| Le correzioni di f12 tolgono i fantasmi dal pavimento vuoto | **sostenuto dai dati**, un lancio per braccio, in simulazione |
| I controlli di principio di `valida_riga` coprono i tre principi | **non risolto**: il secondo (l'avviso si toglie solo guardando) chiede un controllo fra righe, non scritto |

## 4. Proposte

- **architetto-1 — controllo fra righe dell'avviso.** Meccanismo: `valida_sequenza` segue ogni avviso; se sparisce senza un evento «osservato» o senza celle rilasciate perché viste, errore. Previsione: 0 avvisi tolti senza guardare sulle scene corte. Smentita: anche un solo caso.
- **architetto-2 — la fascia dalle classi ammesse, mai dall'etichetta.** Meccanismo: `etichette.py` non è importato da chi calcola avvisi, fascia e livelli. Previsione: cambiando il file delle etichette, avvisi e livelli restano identici riga per riga. Smentita: una sola differenza fuori da `classe`, `origine_etichetta` e `regione`.
- **architetto-3 — porto del predittore dietro l'interruttore.** Previsione: quota «dentro la zona» del porto dentro l'intervallo di Wilson al 95 % del banco in C, stessa geometria T. Smentita: fuori dall'intervallo; allora resta il predittore a velocità costante e lo schermo lo dice.

## 5. Dopo

Passo 1 (corto), in quest'ordine: `sorgenti.apri` e `SorgenteSequenza`; `NucleoCorto` con salute del sensore; `livelli`; `mostra`; `tabellone`; architetto-1 e architetto-2; `due_persone`; per ultimo il porto. Passo 2 (lungo): copiare `movi_lp.py` e il simulatore in `riuso/lunga_portata/`, scrivere `lungo.py` e `scene/lp_*.json`, adattare `mostra` alla scala in chilometri.
**Rischi.** Il modo lungo può chiedere campi nuovi al registro (quota, più griglie): si aggiungono, non si rinominano. `prova_tutto.sh` con undici scene e i filmati va rimisurato. La prova di tempo della catena (P16) fallisce quando la macchina è carica: non lanciarla insieme ad altri processi pesanti. Da decidere con l'utente o l'arbitro: che cosa mostra la scena «passa dietro e ricompare» (critica 4).
