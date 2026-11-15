# MoVi · Regia e sistema visivo del video (f17-video / 12-regia) — `sciame-videomaker`

Scritto il 15-11-2026 fra le 00:22 e le 00:45 (`date -Is`). Preproduzione: niente qui dipende dalle cifre del verdetto
(`f15-lunga-portata/30-verdetto/VERDETTO_FASE2.md`, che alle 00:22 non esiste); dove servono c'è `[CIFRA: …]`.
Testo del video in inglese, con l'italiano accanto. Fotogrammi di stile in `12-regia/stile/` (sezione 6).

## 0. Cambi di stato e regole violate

- **Arco.** `10-messaggio/MESSAGGIO_E_ARCO.md` non esiste ancora; alle 00:26 è comparsa una prima voce
  (`10-messaggio/voce_en.txt`, `voce_it.txt`). La struttura in scene della sezione 3 **segue l'ordine di quella voce**
  (piazzale → idea → sensori → nebbia → collisione → avaria → limiti → nucleo a corto raggio → chiusura): va
  riconciliata quando l'arco sarà scritto.
- **Regole violate, anche per errore: nessuna cancellazione.** Ho **spostato** (non cancellato) la prima versione del
  sorgente da `stile/progetto/index_v1.html` a `stile/versioni/index_v1.html`, perché il lint di HyperFrames la dava
  come errore («multiple_root_compositions»). I PNG v1 restano accanto ai v2.
- **Scrittura fuori cartella (dal CLI, non da me):** `hyperframes snapshot` scrive la cache dei fotogrammi in `/tmp` e
  lo stato in `~/.cache/hyperframes`, come già annotato in `00-strumenti/STRUMENTI.md` §1.2. Telemetria spenta.
- Nessuna rete usata. Nessuna voce generata, nessun audio ascoltato.

## 1. Critiche al materiale (numerate, con la prova)

1. **Il registro non ha ancora i campi del modo lungo** che il video deve disegnare: volume e impronta dei detriti,
   nube per sensore, portata utile per sensore, «tracce non risolte», «ispezionata da operatore». Prova:
   `f16-prototipo/01-architettura/ARCHITETTURA.md` §2(3) (campi elencati) e §3 («il formato basta al modo lungo:
   **non risolto**»). Proposta di campi nella sezione 5; finché non ci sono, quelle inquadrature sono «Schematic».
2. **Lo stato «previsto» della sceneggiatura attesa non esiste nel registro.** `scenari_eventi.json`, E1, 15–17 s:
   «A e B: 'previsto', identità presunta»; il registro ha `stato ∈ {in_conferma, vista, vista_in_parte, non_vista,
   previsto_ampio, ricomparsa}`. Il video usa **le parole del registro**; serve una decisione dell'arbitro
   (proposta: `non_vista` + regione = «NOT SEEN · X s»; `previsto_ampio` = «WIDE PREDICTION»). Nel fotogramma A ho
   scritto «A · PREDICTED»: è un'etichetta da correggere quando la decisione arriva.
3. **Parole vietate dentro i dati.** `scenari_eventi.json` usa il campo `"bersaglio"` (E1, `avviso`), e
   `SENSORI_LUNGA_PORTATA.md` la colonna «Bersaglio». Nel video non devono affiorare: il componente che legge quel campo
   lo rinomina («warning area»). Lo stesso per i nomi commerciali delle schede (radar e LiDAR di marca): a schermo solo
   la classe del sensore; il nome sta, se serve, nel file delle fonti.
4. **L'effetto della fiammata sul radar non è verificato** (`REGOLE_E_SCENARI_EVENTI.md`, EV-C: «non verificato,
   `01-effetti` non ha fonte»; `EFFETTI_SUI_SENSORI.md` §6: «sì (non verificato)»). La scena dell'avaria mostra «il
   radar resta», quindi deve dirlo a schermo: «flash effect on radar: NOT VERIFIED» (presente nel fotogramma B).
5. **Le istruzioni dell'utente fissano font a pesi che non abbiamo.** §7 chiede JetBrains Mono 600; in locale ci sono
   solo Regular e Bold (`00-strumenti/hyperframes/prova/assets/fonts/`). Uso Bold (700) per le etichette di stato.
6. **Etichette di stato ≥ 28 px e console a destra non stanno insieme** con 440 px di larghezza: nei fotogrammi le
   righe secondarie della console sono a 20–22 px (metadati, non stati) e due righe sforano ancora (sezione 6).
7. **Bozza della voce (`voce_en.txt`), due punti da vagliare con chi la scrive** (non è il mio ruolo riscriverla):
   «it never calls empty» va legata alla premessa del modo lungo (Pd cumulata per la classe più piccola ammessa,
   EV-B/EV-E); «it never calls a space empty unless it has looked» è più forte della regola, che chiede anche la Pd
   cumulata. Proposta: «…unless enough sensors have looked».

## 2. Il sistema visivo

### 2.1 Stile e inquadrature fisse

Motion graphics tecnico, fondo scuro, niente slide: ogni scena di dati è la **stessa tavola a tre viste**, ferma,
in cui cambiano solo i dati. Le tre viste stanno sempre allo stesso posto (griglia 1920 × 1080, margini 96/54 px):

| Zona | Rettangolo (px) | Contenuto |
|---|---|---|
| Fascia alta | 0–124 | nome della scena (Inter 700, 38 px) e richiesta della traccia (JB Mono 22 px); a destra il riquadro d'onestà |
| SCENE · SIMULATED TRUTH | x 96–576, y 140–840 | la verità della simulazione, in grigio #8A97A8: sagome piatte, lampo, fumo, frammenti come punti |
| AS MoVi DECLARES IT · PLAN VIEW | x 600–1384, y 140–840 | pianta dall'alto: sensori, coperture, tracce, regioni, avvisi, volumi; ritagliata al pannello |
| OPERATOR CONSOLE | x 1408–1824, y 140–840 | bande di salute per sensore, elenco delle tracce con stato ed età, registro degli eventi |
| Fascia del dominio | y 862–900 | a sinistra lo scenario e l'origine («Simulation · scenario E2 written by hand»), a destra le note |
| Sottotitoli | y 940–1080 | Inter 600 40 px, #E8EDF2 su #0B0F17 all'80 %, 2 righe da 42 caratteri |

Il racconto è la **differenza fra la vista di sinistra (ciò che accade) e quella al centro (ciò che il sistema
dichiara)**. Le scene «Schematic» (idea, sensori, catena, chiusura) usano la stessa griglia senza la vista di verità.

### 2.2 Codifica degli stati: trama e parola prima del colore (adattata da ISTRUZIONI §7)

Contrasti misurati con la formula WCAG sul fondo #0B0F17 (e sul pannello #121826); tinte tutte fuori da 90–160°.

| Stato (registro) | Forma | Parola a schermo (EN) | Italiano | Colore | Contrasto |
|---|---|---|---|---|---|
| `vista` | disco pieno | `SEEN` / `SEEN (RADAR ONLY)` | vista (solo radar) | ciano #3DD6E8 | 10,9:1 |
| `non_vista` + regione | anello vuoto + regione **tratteggiata** (riempimento 18 %), mai una sagoma dentro | `NOT SEEN · 2.4 s` | non vista da 2,4 s | ambra #F5A524 | 9,4:1 |
| `previsto_ampio` | righe diagonali su tutta la regione, anello al centro | `WIDE PREDICTION` | previsto ampio | ambra #F5A524 | 9,4:1 |
| avviso `possibile_presenza` | contorno a righe a 45° | `POSSIBLE PRESENCE` | possibile presenza | ocra #C7841A | 6,2:1 |
| volume dei detriti (evento) | disco/poligono a righe 45° con **punti bianchi** (frammenti) e anelli dei raggi passati; impronta a terra a trattini radi | `POSSIBLE DEBRIS` | possibili detriti | ocra #C7841A | 6,2:1 |
| `ricomparsa` | disco pieno + «?» accanto all'ID | `REAPPEARED · IDENTITY PRESUMED` | ricomparsa, identità presunta | ciano | 10,9:1 |
| `identita: ambigua` | due anelli uniti da una linea tratteggiata | `UNRESOLVED TRACKS` | tracce non risolte | ambra | 9,4:1 |
| non osservato / settore `zona_non_verificata` | **puntini** grigi | `UNVERIFIED ZONE` | zona non verificata | #8A97A8 | 6,5:1 |
| nube (non osservato per alcuni sensori) | puntini fitti + contorno a trattini, **l'elenco dei sensori nella parola** | `NOT OBSERVED · SMOKE (EO, IR)` | non osservato: fumo (EO, IR) | #6B7686 | 4,2:1 (sempre con parola ≥ 26 px) |
| portata ridotta (meteo) | copertura di scheda in tratteggio fantasma; copertura utile piena | `USEFUL RANGE REDUCED` | portata utile ridotta | ambra | 9,4:1 |
| sensore `affidabilita_persa` | glifo barrato, copertura a righe corallo che **non conta**; banda piena in console | `RELIABILITY LOST · cause` | affidabilità persa · causa | corallo #FF6B6B, testo #0B0F17 | 6,9:1 |
| sistema `affidabilita: persa` | banda piena di 120 px sopra la pianta, tutti i settori a puntini | `RELIABILITY LOST` | affidabilità persa | corallo | 6,9:1 |
| `visto_libero_fino_a` | cella piena tenue, solo nel fotogramma corrente e solo dove il registro lo dice | `SEEN FREE TO 2 000 m` | visto libero fino a 2 000 m | #24344A | 1,5:1 voluto |
| ispezione (EV-E) | puntini che restano finché arriva l'evento d'ispezione | `INSPECTED BY OPERATOR` | ispezionata da operatore | #AEB8C5 | 9,6:1 |

Glifi dei sensori (forma, non colore): radar = cerchio con punto; camera EO = triangolo vuoto; termica = triangolo
pieno al 50 %; LiDAR = rombo; cooperativi (ADS-B, identificazione remota) = quadrato viola #A99CFF (8,1:1). Coperture:
contorno #4A5A70 (2,7:1, è un fondo, non uno stato).

**Lessico vietato** (in voce, a schermo, nei nomi dei campi mostrati): target/bersaglio, threat, engage, intercept,
lock, kill, hostile, «lost» come stato, «probable», «clear/go», detect-and-avoid, validated, certified, compliant,
guaranteed. Si dice: observe, monitor, warn, declare.

### 2.3 Come si rappresentano gli eventi senza spettacolarizzarli

- **Collisione fra droni (E1).** Prima della collisione le due tracce si avvicinano fino a fondersi in
  `UNRESOLVED TRACKS` (13,65–15 s, non è un evento). Poi, nella pianta, nessun impatto disegnato: compare la riga
  `EVENT: CONTACT (INFERRED)` e nasce il **volume dei detriti**: un disco a righe ocra con i frammenti come punti
  bianchi, il cui raggio segue `V(τ)` del registro fotogramma per fotogramma (anelli sottili lasciano il raggio a 1 s,
  2 s…: si vede che cresce e non si restringe); l'impronta a terra è un cerchio a trattini radi. La persona dentro
  l'impronta resta `SEEN` e riceve `INSIDE DEBRIS FOOTPRINT`. La verità a sinistra mostra due sagome a croce che si
  toccano e punti grigi: nessun fuoco, nessuna esplosione.
- **Fiammata (E2).** Nella verità: una stella piatta bianca a 15 punte, **senza alone, sfocatura né gradiente**, per
  la sola durata della sorgente (3 s, dal JSON); il fumo è una macchia grigia piatta. Nella pianta: i glifi EO e
  termica si barrano, le loro coperture passano a righe corallo, in console entrano le bande `RELIABILITY LOST · flash
  saturation`; la traccia dell'aereo resta un disco pieno, `SEEN (RADAR ONLY)`. Nessun lampo sullo schermo intero.
- **Nebbia e pioggia (E3).** La copertura ottica **si ritrae**: il ventaglio di scheda resta come tratteggio
  fantasma, quello utile si accorcia con la curva dei dati fino a pochi metri (23 m per l'EO in nebbia fitta, valore
  **per calcolo** di `conti_eventi_esito.txt`, da rileggere a schermo con «calc.»). Il resto del ventaglio diventa
  puntinato `NOT OBSERVED · FOG (EO, IR)`; in basso `NO REDUNDANCY`. La verità è un velo grigio uniforme.
- **Detriti in pista (E2, EV-E).** L'impronta unita alla pista a valle è **puntinata** `UNVERIFIED ZONE · POSSIBLE
  DEBRIS` e non si scioglie mai da sola: resta fino all'evento «ispezionata da operatore», che negli scenari non
  c'è; quindi nel video **resta accesa fino alla fine della scena**.
- **Divieti grafici.** Niente verde, spunte, frecce «vai», semafori; niente bagliori, particelle decorative, scansioni
  rotanti, mirini, reticoli, ologrammi; niente sangue, vittime, volti, loghi o marchi di terzi; niente aerei o droni
  realistici: sagome piatte grigie.

### 2.4 Palette, tipografia, movimento

- **Palette:** fondo #0B0F17; pannello #121826; bordi #24344A; testo #E8EDF2 (16,3:1) e #AEB8C5 (9,6:1); stati come
  in 2.2. Nessun colore fra 90° e 160° di tinta (controllato sui tre fotogrammi: 0 pixel, sezione 6).
- **Tipografia:** Inter (variabile, OFL) per titoli 38–96 px e sottotitoli 40 px; JetBrains Mono Bold (OFL) per
  etichette di stato ≥ 26–28 px e per la console; JetBrains Mono Regular 20–22 px per metadati e righe di fonte. Font
  da file locale (`@font-face` con nomi propri), mai da rete.
- **Movimento:** cambi di stato **istantanei** (0–2 fotogrammi, nessuna dissolvenza fra stati); crescita di regioni,
  volumi e coperture **guidata dai dati**, senza easing aggiunto; **camera ferma** in tutte le scene di dati; un
  carrello lento (≤ 5 % al secondo) solo nelle scene «Schematic». Niente rallentatore: tempi di scenario reali; dove
  serve accelerare (E1 dura 90 s), la fascia lo dice: `×4 · time compressed`.
- **Fasce fisse:** in alto a sinistra nome della scena e richiesta della traccia; **in alto a destra, per tutta la
  durata**, `SIMULATION · SENSORS MODELLED FROM DATASHEETS` (scene di dati) oppure `SCHEMATIC` (scene illustrative);
  in basso a sinistra scenario e origine; nella chiusura `Observes and warns · no output is a command`.
- **Transizioni:** tagli netti fra scene; l'unica transizione motivata è il passaggio dalla verità a tutto schermo
  alla tavola a tre viste (scena 1), con la verità che si restringe nel suo pannello (0,5 s, lineare).

## 3. Le scene (172 s, ordine della bozza di voce)

Parole a 125–135 al minuto: circa 2,1 parole al secondo di parlato, meno le pause. «Dati» = campi del registro per
fotogramma (`ARCHITETTURA.md` §2(3)) o righe della `sceneggiatura_attesa` di `scenari_eventi.json`.

| # | Tempo | Scena | Etichetta | Inquadratura e componenti | Dati | Transizione |
|---|---|---|---|---|---|---|
| 1 | 0:00–0:12 (12 s, ~22 parole) | **Apron** — un drone passa dietro l'hangar | SIMULATION | verità a tutto schermo (piazzale, hangar, due droni, aereo in rullaggio), poi la tavola a tre viste; il disco diventa anello con regione | scenario `lp_A1`/`lp_A2` di `03-scenari/scenari.json`; `tracce[].stato, non_vista_da_s, regione`; `avvisi[]` | taglio d'apertura; restringimento della verità nel suo pannello |
| 2 | 0:12–0:32 (20 s, ~40) | **The idea** — tre risposte; non osservato ≠ libero; titolo MoVi | SCHEMATIC | tre segni grandi al centro (disco, anello+tratteggio, puntini «?»); la parola FREE su una zona puntinata, barrata; titolo e marchio SDMs | nessun dato (illustrazione) | taglio |
| 3 | 0:32–0:50 (18 s, ~36) | **Sensors** — radar, LiDAR, EO, termica, cooperativi; ognuno ha punti ciechi | SCHEMATIC | pianta con i glifi e le coperture che si accendono una alla volta; matrice condizione × sensore (6 × 6) di `EFFETTI_SUI_SENSORI.md` §6 a puntini/pieno | intestazione del registro: `sensori` (tipo, posizione, portata di scheda) | taglio |
| 4 | 0:50–1:10 (20 s, ~40) | **Fog** — portata utile ridotta; solo radar; poi il radar cade | SIMULATION | tavola a tre viste (fotogramma C); ventaglio ottico che si ritrae; banda radar `RELIABILITY LOST` nella variante (c), traccia `NOT SEEN · X s` con regione, `WARNING NOT TIMELY` | E3: `sensori[].salute, causa`, portata utile (campo proposto), `tracce[]`, `avvisi[]`; righe 0–100 s e 100–120 s della sceneggiatura | taglio; **1 s di silenzio** all'ingresso della banda del radar |
| 5 | 1:10–1:36 (26 s, ~50) | **Drones collide** — tracce non risolte, contatto dedotto, volume, avviso alla persona, suolo non verificato | SIMULATION, ×4 dopo i 20 s | tavola a tre viste (fotogramma A); facoltativo 4 s di riquadro E5 «passaggio vicino: nessun evento» | E1: `tracce[].identita` (ambigua → presunta), `eventi[]` (`contatto`, `come_lo_so`), `volumi[]` e `impronta` (proposti), `avvisi[]`, `celle` (0 libere nell'impronta) | taglio |
| 6 | 1:36–2:02 (26 s, ~50) | **Engine failure** — fiammata, camere inaffidabili, il radar tiene l'aereo; fumo non osservato; pista a valle non verificata; il mezzo avvisato | SIMULATION | tavola a tre viste (fotogramma B) | E2: `sensori[].salute` (EO, IR → `affidabilita_persa`, causa), `nubi[]` (proposto), `eventi[]` (`separazione`, dedotto), `settori[]`/celle `zona_non_verificata`, `avvisi[]` per `mezzo1` | taglio; **1 s di silenzio** all'ingresso delle bande EO/IR |
| 7 | 2:02–2:30 (28 s, ~55) | **Limits, then what holds** — tutto simulato, nessun sensore fisico, etichette a mano, catena mai eseguita per intero; decidono regole scritte; tabellone | SCHEMATIC + SIMULATION per i contatori | righe di registro a sinistra (limiti, in voce e a schermo); a destra lo schema a blocchi della catena (classificazione a lato, tratteggiata: «requested · hand labels»); sotto due contatori | `tabellone`; `[CIFRA: frammenti dentro V k/n]`, `[CIFRA: tracce perse senza avviso k/n]` da `VERDETTO_FASE2.md` | taglio |
| 8 | 2:30–2:40 (10 s, ~18) | **Same core, short range** — persona dietro un ostacolo, camera di profondità | SIMULATION · ideal sensor | la console della versione v1.0 a corto raggio (anello, regione, `POSSIBLE PRESENCE`), piccola, con la sua etichetta | registro delle scene `passa_dietro_e_ricompare`, `resta_dietro` (`prototipo/scene/SCENE.json`) | taglio |
| 9 | 2:40–2:52 (12 s, ~16) | **Close** — MoVi, la frase, SDMs, nomi, crediti | SCHEMATIC | marchio SDMs, titolo, «Observes and warns · no output is a command»; nomi; crediti musica e font; 0,5 s di nero | nessuno | dissolvenza al nero (solo qui) |

Facoltativa in riserva (se la voce lo chiede): **E4, colonna di fumo** (18 s) — (a) con radar `SEEN (RADAR)` e per
l'EO `NOT OBSERVED · SMOKE`; (b) solo camere: `NOT SEEN · X s` con regione, poi `REAPPEARED · IDENTITY PRESUMED`.

## 4. Audio

- **Musica:** **tappeto sintetico** `00-strumenti/audio/uscite/tappeto_180s.wav` (numpy, seme 7, Dm9–Bbmaj7–Fmaj7–Am7,
  nessun diritto di terzi, deterministico). Alternativa dopo l'ascolto: «Dreams Become Real», Kevin MacLeod, CC BY 4.0
  (60 BPM, attribuzione nei crediti di coda). Escluso finché non ascoltato: Bartmann (CC0, «Instrumental: No» nella
  pagina). «Ossuary 5 – Rest» scartato per il carattere («Dark, Eerie»): spinge verso il dramma.
- **Ambiente:** un fruscio d'aria basso (rumore filtrato generato con ffmpeg, −26 dB come in `mix.sh`), nessun motore
  o sirena registrati, nessun «boom» alla fiammata né alla collisione.
- **Nessun suono legato agli stati**, nessun bip, nessuna altezza legata all'incertezza. Unica eccezione voluta:
  **1 s di silenzio di musica e ambiente** quando una banda `RELIABILITY LOST` entra in una scena di dati (scene 4 e
  6; la voce, se parla, resta).
- **Mix:** `00-strumenti/audio/script/mix.sh` (ducking con sidechain, musica −14 dB, ambiente −26 dB), loudnorm a due
  passate a **−14 LUFS**, picco vero ≤ −1,5 dBTP; misura con `ebur128=peak=true`. Voce Kokoro `bm_george` (EN); poi
  `im_nicola` (IT) sulla stessa immagine: i tempi per frase di `kokoro_tts.py` (`.tempi.json`) agganciano i tagli.

## 5. Componenti HyperFrames (riusabili, guidati dal registro)

Ogni componente è una funzione pura `draw(riga, opzioni)` chiamata da `drawAt(t)` (via A di `STRUMENTI.md` §2), dove
`riga = registro[floor(t·30)]` (ricampionato tenendo l'ultimo stato, senza interpolare gli stati); una composizione
per scena in `compositions/*.html`. Geometria: metri in pianta → pixel con una trasformazione per scena (`scala_m_px`,
`origine`), dichiarata nella scala grafica in basso.

| # | Componente | Legge (riga per fotogramma, salvo «intestazione») | Disegna |
|---|---|---|---|
| 1 | `PiantaArea` | intestazione: `griglie`, `ostacoli`, aree dello scenario (pista, piazzale, raccordo) | fondo, aree, ostacoli, scala grafica |
| 2 | `Sensori` | intestazione `sensori` (id, tipo, pos, portata di scheda, campo); riga `sensori[].salute, causa`, `portata_utile_m` (proposto) | glifo per tipo, copertura piena/fantasma/a righe corallo |
| 3 | `Traccia` | `tracce[]`: id, classe, `origine_etichetta`, `stato`, `non_vista_da_s`, `identita`, pos | disco/anello/«?»; etichetta `ID · STATE · X s` |
| 4 | `Regione` | `tracce[].regione` (forma: cerchio, poligono, settore_anulare, celle) | tratteggio con riempimento 18 %; righe se `previsto_ampio`; mai una sagoma |
| 5 | `PossibilePresenza` | `avvisi[]`: traccia, età, `forma` | contorno a righe ocra + parola |
| 6 | `VolumeDetriti` | **proposto** `volumi[]`: evento, `t_a`, `tau`, forma in pianta, quota [z_min, z_max], `impronta`; più `verita` per i punti dei frammenti (solo nel pannello di verità) | disco a righe, anelli dei raggi passati, impronta a trattini; i punti bianchi nella pianta sono **solo** ritorni misurati, se il registro li dà |
| 7 | `Nube` | **proposto** `nubi[]`: id, forma, `opaca_per[]`; `celle.per_sensore` con `causa` | puntini fitti + `NOT OBSERVED · SMOKE (sensori)` |
| 8 | `BandaAffidabilita` | `sensori[].salute, causa, eta`; `affidabilita` | una banda per sensore in console; banda di 120 px sulla pianta se `affidabilita = persa` |
| 9 | `ConsoleTracce` | `tracce[]`, `eventi[]` (t, tipo, `come_lo_so`), `dichiarazioni` | elenco ordinato per stato; registro degli eventi con `INFERRED/OBSERVED` |
| 10 | `VentaglioSettori` | `settori[]`: azimut, `livello`, `d_m`, motivo | settori a tre livelli (+ affidabilità persa) attorno al sensore |
| 11 | `ZonaNonVerificata` | `celle` (`rle`, conteggi, causa); evento d'ispezione | puntini; toglie i puntini solo all'evento «ispezionata» |
| 12 | `Tabellone` | `tabellone.dentro_la_zona {k, n}` cumulato; per la fase 2 i contatori del verdetto | contatore che sale passaggio per passaggio, con l'origine scritta sotto |
| 13 | `CatenaBlocchi` | `dichiarazioni` (regole accese/spente) | schema a blocchi; i blocchi spenti tratteggiati con «in design» |
| 14 | `VeritaSim` | `verita` (oggetti, classe, pos, visibile), eventi dello scenario | sagome piatte grigie, lampo piatto per `durata_sorgente_s`, fumo piatto |
| 15 | `FasceOnesta` | `dichiarazioni` (dati simulati, etichette a mano, impronta della configurazione) | fasce fisse della sezione 2.4; il testo dell'etichetta viene dal registro, non dal montaggio |
| 16 | `TitoloMarchio` | nessuno | marchio SDMs (proposta: disco pieno, anello vuoto, quadrato a puntini in fila + «SDMs» in Inter 700; nessun elemento di terzi), titolo MoVi |
| 17 | `Sottotitoli` | `.srt` EN o IT generato dai `.tempi.json` della voce | fascia bassa; oppure impressi con ffmpeg/libass |

**Campi da aggiungere al registro per il modo lungo (proposta per l'architetto, da validare con `valida_riga`):**
`volumi[]`, `nubi[]`, `sensori[].portata_utile_m{classe}`, `sensori[].copertura`, `celle.causa`, `tracce[].risolta`
(o `identita: ambigua` per «tracce non risolte»), `eventi[].tipo ∈ {contatto, separazione, ispezione}`.

## 6. Fotogrammi di stile (resi e guardati)

Sorgente: `stile/progetto/index.html` (HyperFrames 0.9.48; lint 0 errori, 3 avvisi `nested_structure` noti).
Comando: `$HF snapshot --at 0.5,1.5,2.5` con l'ambiente di `STRUMENTI.md` §1.3. Valori **schematici**, non dal
registro: la fascia lo dice («STYLE FRAME · values schematic, not from the log»).

| File | Che cosa mostra | Che cosa ho visto |
|---|---|---|
| `stile/stile_A_collisione_v2.png` | E1: volume dei detriti a righe con punti, impronta, A e B con regione, persona `INSIDE DEBRIS FOOTPRINT`, console | leggibile; i glifi dei sensori toccano la scala grafica; «A · PREDICTED» da rinominare (critica 2) |
| `stile/stile_B_fiammata_v2.png` | E2: lampo piatto e fumo nella verità; EO e termica barrate con banda corallo; aereo `SEEN (RADAR ONLY)`; nube puntinata; pista a valle puntinata; mezzo avvisato | l'etichetta del mezzo è tagliata dal bordo della pianta; «RELIABILITY LOST» sfora la banda di un carattere: accorciare in «EO · RELIABILITY LOST» |
| `stile/stile_C_nebbia_v2.png` | E3a: ventaglio ottico di scheda fantasma, utile 23 m (calc.), resto puntinato, `NO REDUNDANCY`, console | il cuneo utile è piccolissimo a questa scala (è il punto, ma serve il richiamo, presente); verità a velo grigio |

Le versioni v1 (`stile_*_v1.png`) mostrano due difetti corretti nella v2: coperture non ritagliate al pannello e
trame invisibili nei quadri B e C (id dei `pattern` duplicati fra SVG nascosti). Controllo del verde (tinta 90–160°,
saturazione > 30 %): **0 pixel** nei tre PNG v2. Non verificato: leggibilità in movimento e a 720p.

## 7. Stati proposti

- La palette rispetta i contrasti dichiarati e il divieto del verde: **verificato** sui tre fotogrammi (formula WCAG;
  conteggio dei pixel), non sul video.
- Il registro attuale basta per le scene 1 e 8: **sostenuto dai dati** (formato del modo corto, 0 su 286 righe non
  valide, `ARCHITETTURA.md`); per le scene 4–6: **non risolto** (mancano i campi del modo lungo; lo decide la prima
  scena `lp_A1` o E1 scritta e convalidata).
- La tavola a tre viste regge 1080p con etichette ≥ 26 px: **sostenuto dai dati** (tre fotogrammi), con due sforamenti
  da correggere.

## 8. Proposte nuove

- **`creativo-videomaker-1`: il volume che non si restringe come prova visiva.** Meccanismo: anelli sottili lasciati
  ai raggi passati di `V(τ)`. Previsione: un revisore indipendente, a una visione, dice «la zona dei detriti cresce
  e non si restringe» in ≥ 4 casi su 5. Smentita: meno di 4 su 5.
- **`creativo-videomaker-2`: l'etichetta d'onestà letta dal registro.** `FasceOnesta` stampa `dichiarazioni` di ogni
  riga: un'inquadratura senza registro non può avere l'etichetta «Simulation». Smentita: un fotogramma con
  «SIMULATION» la cui scena non ha registro (controllo automatico nel QA).

## 9. Che cosa propongo dopo

1. Riconciliare la sezione 3 con `MESSAGGIO_E_ARCO.md` appena esiste; misurare la voce EN con Kokoro e fissare i tempi.
2. Chiedere all'architetto i campi del modo lungo (sezione 5) e il primo registro E1 o E2; senza, quelle scene escono
   «Schematic».
3. Costruire i componenti 1–5, 8, 9, 15 sul registro della scena `passa_dietro_e_ricompare` (già pronto), poi gli
   altri; animatic a 960 × 540 sulla voce guida.
4. Disegnare il marchio SDMs (componente 16) e farlo vedere alla squadra.
