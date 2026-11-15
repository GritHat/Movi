# MoVi · COMPONENTI DEL VIDEO — `sciame-videomaker`, f17-video/30-componenti

Cominciato il 2026-11-15T00:42:13+01:00 (`date -Is`). Costruzione dei componenti del `PIANO_VIDEO.md` §6 (22-sintesi), del
progetto HyperFrames in `video/progetto/` e di un animatic muto di tutta la durata. Le cifre dei risultati NON ci sono: il
verdetto (`f15-lunga-portata/30-verdetto/`) non è ancora arrivato.

## 0. Cambi di stato e regole

- **Scritture:** solo in `video/progetto/`, `video/rendering/` e in questa cartella. Nessun file cancellato. I file generati
  (`index.html`, `scene_tempi.*`, `.srt`, `sottotitoli.js`, voce montata) si riscrivono, ma `monta.py` e `rimonta.py`
  copiano prima la versione precedente in `video/progetto/versioni/` con l'ora nel nome. I dati di sviluppo li ho rigenerati
  sul posto una volta (stesso programma, un campo in più), prima di ogni uso.
- **Niente rete, niente git, niente sudo.** HyperFrames gira con il CLI e il Chrome locali di `00-strumenti`, telemetria
  spenta; GSAP e font da file locali; nessun `fetch` (dati come file JS). Non ho eseguito `hyperframes init` (il suo
  scheletro chiama la CDN): `hyperframes.json`, `meta.json` e `package.json` li ho scritti a mano.
- **Fuori cartella**, per effetto del CLI (già registrato in `STRUMENTI.md` §1.2): cache dei fotogrammi in `/tmp` e file di
  stato in `~/.cache/hyperframes`. Non controllato se ne ha scritti altri.
- **Previsione scritta prima del rendering** (00:53): «l'animatic draft di 173 s si rende in meno di 10 minuti e passa lint
  con 0 errori». Smentita se il rendering supera i 900 s del `timeout` o se lint dà errori. Esito nel §5.
- **Indipendenza:** sono lo stesso ruolo che ha scritto il piano (22-sintesi) e la regia. Ho costruito ciò che il piano
  chiede; i difetti del piano che non vedo restano a Q29 (revisione indipendente).

## 1. Struttura del progetto (`video/progetto/`)

| Percorso | Che cos'è |
|---|---|
| `index.html` | composizione radice, **generata** da `strumenti/monta.py`: una tela SVG 1920×1080 in un `.clip` lungo quanto il video, un marcatore `.clip` vuoto per scena (per la timeline dell'anteprima), una sola timeline GSAP in pausa il cui unico tween fa da orologio e chiama `MoViMotore.disegna(t)` |
| `scene/scene.json` | **la scaletta** (piano §2): scene, durate del piano, tipo (`dati`, `schema`, `titoli`), riquadro in metri della pianta, **segmenti** (quale registro disegna quale tratto, da quale tempo di registro, a quale velocità), chiave del dominio; e l'elenco dei registri con il loro **stato** (`sviluppo`, `provvisorio`, `definitivo`) |
| `testi/schermo_en.json`, `schermo_it.json` | tutto il testo a schermo, per chiave, separato dalle scene; lessico del piano §4 (stati, eventi, avvisi, cause, sensori) e righe fisse delle scene; segnaposto `[CIFRA-…]` |
| `assets/js/componenti.js` | i 18 componenti (§2) |
| `assets/js/motore.js` | sceglie scena, segmento e riga di registro dal tempo; impagina i tre pannelli; testi di scena |
| `assets/data/<ID>.js` | registri convertiti (`window.__REG[ID]`), da `strumenti/registri_a_js.py`; `sottotitoli.js` da `rimonta.py` |
| `assets/fonts/`, `assets/vendor/gsap.min.js`, `assets/marchio/` | Inter, JetBrains Mono (OFL, con licenze), GSAP 3.15.0, simbolo SDMs v3b e wordmark MoVi (copie di `video/marchio/`) |
| `dati_sviluppo/*.SVILUPPO.jsonl` | **registri finti** per costruire i componenti (§3); il nome e il campo `dati` li marcano |
| `strumenti/` | `genera_dati_sviluppo.py`, `registri_a_js.py`, `monta.py`, `rimonta.py`, `rendi.sh`, `controlla.sh` |
| `tempi/` | `scene_tempi.json` (scritto da `rimonta.py`), `scene_tempi.js` (da `monta.py`), `voce_montata_{en,it}.wav` (con la voce vera) |
| `sottotitoli/` | `movi_{en,it}.srt`; oggi solo `movi_{en,it}_STIMATI.srt` (tempi stimati) |
| `versioni/` | copie delle versioni precedenti dei file generati |

## 2. Componenti e interfacce

**Interfaccia comune (piano §6):** `C.Nome(riga, intest, opz) -> stringa SVG`, funzione pura.
- `riga` = `registro[floor((t_reg − t0)·fps + 1e-6)]`, con `t_reg = t_reg_segmento + (t_scena − da)·velocita`; si tiene
  l'ultimo stato, gli stati non si interpolano (unica eccezione: le posizioni dentro una riga sono quelle del registro).
- `intest` = riga 1 del registro (sensori, ostacoli, aree, griglie).
- `opz` = `{P (proiettore metri→px, nord in alto), pannello, T (testi della lingua), t (s nella scena), console,
  pannello_movi, occ (riquadri delle etichette già messe), stato_registro, velocita, …}`.
- Un campo **proposto** che non c'è nella riga non disegna niente. Campi proposti usati (oggi solo nei dati di sviluppo):
  `sensori[].portata_utile_m{classe}`, `volumi[]` (forma, `impronta`, `raggi_passati_m`, `t_a`, `tau`), `ritorni[]`,
  `nubi[]` (forma, `opaca_per`), `avvisi_operatore[]` (`codice`, traccia), `eventi[].indizi`, `sistema[]`
  (`NO_REDUNDANCY`, `WARNING_NOT_TIMELY:<classe>`), `zone_non_verificate[]` (forma, causa), `meteo`,
  `verita.fiammata`, `avvisi[].motivo`. **Vanno concordati con l'architetto** (piano §7); i nomi sono una proposta mia.

| # | Componente | Legge | Disegna |
|---|---|---|---|
| 1 | `PiantaArea` | `intest.aree`, `ostacoli` | aree e ostacoli; scala grafica in alto a destra |
| 2 | `Sensori` | `intest.sensori` (id, tipo, pos, `portata_m`, `campo_gradi`); `riga.sensori[].salute, causa, portata_utile_m` | glifi del piano §4 (radar cerchio+arco, EO triangolo vuoto, IR pieno al 50 %, LiDAR rombo, cooperativi quadrato viola); copertura piena tenue; con portata utile: fantasma tratteggiato + utile; con affidabilità persa: contorno grigio tratteggiato intero, glifo barrato, `EO · NOT COUNTED` |
| 3 | `Traccia` | `tracce[]` | disco (vista), mezzo disco, disco sottile (in conferma), anello ambra (non vista, previsto ampio), disco + `?` (ricomparsa); `ID · STATO · X s`; tracce `ambigua` unite da un tratteggio, `UNRESOLVED TRACKS`; `SEEN (RADAR ONLY)` se l'unico sensore è un radar |
| 4 | `Regione` | `tracce[].regione` (cerchio, poligono, settore anulare, celle polari) | tratteggio ambra al 18 %; righe ambra per `previsto_ampio`; mai una sagoma dentro |
| 5 | `PossibilePresenza` | `avvisi[]` (`possibile_presenza`, salvo `motivo: possibili_detriti`) | contorno a righe ocra 45° + `POSSIBLE PRESENCE` |
| 6 | `VolumeDetriti` | `volumi[]`, `ritorni[]` | righe ocra, ultimi 3 raggi passati (tratteggio tenue), impronta a puntini; quadratini `RADAR RETURNS` solo da `ritorni[]` |
| 7 | `Nube` | `nubi[]` | puntini fitti + contorno a trattini + `NOT OBSERVED · SMOKE (EO, IR)` |
| 8 | `BandaAffidabilita` | `sensori[].salute, causa`, `sistema[]`, `affidabilita` | bande in console (corallo per affidabilità persa, grigie per portata ridotta, ridondanza, tempestività); banda di sistema di 120 px sul pannello MoVi se `affidabilita = persa` |
| 9 | `ConsoleTracce` | `tracce[]`, `avvisi[]`, ultimo evento (`contatto`, `separazione`) con `come_lo_so` e `indizi`, `avvisi_operatore[]` | 3 righe di stato, conteggio degli avvisi, riga d'evento, `WARNING TO OPERATOR · …` |
| 10 | `VentaglioSettori` | `settori[]`, `intest.griglie.*.portata_m` | settori a tre livelli dal sensore; `OBSERVED EMPTY · to d m` solo con `mostra_vuoto` |
| 11 | `ZonaNonVerificata` | `zone_non_verificate[]`\* | puntini + `UNVERIFIED ZONE` / `UNVERIFIED · POSSIBLE DEBRIS`. **Non** decodifica ancora `celle.rle` della griglia cartesiana del modo lungo (formato della griglia non fissato) |
| 12 | `Tabellone` | contatori (testi con `[k]`, `[n]`, origine) | righe dei contatori con origine e dominio |
| 13 | `CatenaBlocchi` | `s7.catena` dei testi; `accesi` | blocchi; quelli spenti tratteggiati; classificazione di lato, tratteggiata |
| 14 | `VeritaSim` | `verita.oggetti`, `verita.fiammata`\*, `nubi[]`, `meteo`\* | sagome grigie piatte (aereo, multirotore, persona, mezzo); `out of sensor view` sugli oggetti non visibili; fiammata come ellisse bianca piatta senza punte + `FLASH (3 s) · schematic`; fumo piatto; nebbia come velo; pioggia come righe |
| 15 | `FasceOnesta` | `riga.dichiarazioni.dati` di **ogni** riga; stato del registro | in alto a destra per tutta la scena: `SCHEMATIC` senza riga; `SCHEMATIC · DEV DATA · NOT A RESULT` con dati di sviluppo; `SIMULATION · …` con dati `simulati`/`pubblici` (+ `PROVISIONAL REGISTER` se provvisorio); in alto a sinistra titolo e richiesta della traccia; fascia del dominio, `×N · time compressed`, `last state held` |
| 16 | `ScenaSchema` | testi, tempo della scena | scena 2 (tre segni, `EMPTY` barrato, `POSSIBLE PRESENCE`), scena 7 (limiti uno alla volta, contatori, catena) |
| 17 | `TitoloMarchio` | `assets/marchio` | titolo d'apertura (0–3 s), simbolo SDMs v3b animato in 1,5 s, wordmark, tagline, perimetro, crediti, 0,5 s di nero |
| 18 | `Sottotitoli` | `window.__SUB` (da `rimonta.py`) | fascia bassa, Inter 600 40 px su #0B0F17 all'80 %; con tempi stimati, la scritta magenta `VO GUIDE · ESTIMATED TIMING · NOT FINAL` |

Scena 3 (sensori) è impaginata nel motore (`scena3`) con `PiantaArea` e `Sensori` su un pannello largo; le portate per
classe sono **archi** e non cerchi (due cerchi concentrici attorno al radar si leggerebbero come un bersaglio, Q33), con
`radii not to scale · schematic`.

## 3. Dati di sviluppo

`strumenti/genera_dati_sviluppo.py` (stdlib, deterministico) scrive `R1`, `R3a`, `R3b`, `R3c`, `R1E`, `R2E` in
`dati_sviluppo/*.SVILUPPO.jsonl`, nel formato di `prototipo/movi/registro.py` (modo `lungo`, 30 righe/s, tutti i campi
obbligatori), con `dichiarazioni.dati = "SVILUPPO_NON_RISULTATO"`. Traiettorie da `scenari_eventi.json` (E1, E2, E3); il
piazzale V1 è inventato. **Stati, regioni, portate, volumi, nubi sono regole giocattolo scritte lì, non le regole EV e
non i loro numeri.** Effetti di questa marcatura:
- `FasceOnesta` stampa `SCHEMATIC · DEV DATA · NOT A RESULT` su ogni fotogramma che li usa (verificato sulle istantanee);
- `rimonta.py` avvisa per ogni scena che li usa;
- `monta.py --finale` (e quindi `rendi.sh … delivery`) **rifiuta** il montaggio se un registro in uso è `sviluppo`, se un
  testo o un sottotitolo ha ancora un segnaposto, o se i sottotitoli sono stimati.

La scena 8 usa invece il registro a corto raggio **vero** `prototipo/uscite/resta_dietro/registro.jsonl` (82 righe,
15 fps, 0–5,27 s, `dati: simulati`), marcato `provvisorio` perché il prototipo è ancora in lavorazione: la fascia dice
`SIMULATION · SIMULATED DEPTH CAMERA · PROVISIONAL REGISTER`; dopo 5,3 s di registro si tiene l'ultimo stato e la fascia
del dominio lo dice. Nel registro c'è una seconda traccia (`2`, `non_classificato`, ferma a 1,8 m: con ogni probabilità il
pannello) che il video mostra così com'è: **da chiarire** con l'architetto.

## 4. Comandi

```bash
P=/home/fede/Scrivania/ed/GitHub/Movi-Hackthon/video/progetto; cd $P
python3 -I strumenti/genera_dati_sviluppo.py          # solo finché mancano i registri veri
python3 -I strumenti/rimonta.py --stima               # tempi e .srt stimati (animatic); poi rilancia i due passi sotto
python3 -I strumenti/registri_a_js.py                 # registri .jsonl -> assets/data/*.js
python3 -I strumenti/monta.py [--lingua it] [--finale]  # scene_tempi.js, testi.js, marchio.js, index.html
sh strumenti/rendi.sh draft ../rendering/animatic_muto_vN.mp4      # lint + render + ffprobe (non sovrascrive)
sh strumenti/controlla.sh ../rendering/animatic_muto_vN.mp4 ../rendering/controllo_vN 10   # istantanee + Q11
```

**Con la voce vera** (dopo aver tolto o riempito i segnaposto nei testi, piano §3.2):

```bash
V=…/f17-video/00-strumenti/voce
$V/venv-kokoro/bin/python $V/script/kokoro_tts.py --testo voce_en_v3.txt --voce bm_george --lingua en-gb \
  --velocita 1.0 --pausa-frase 0.35 --pausa-paragrafo 0.8 --uscita voce_en.wav        # scrive voce_en.wav.tempi.json
python3 -I strumenti/rimonta.py --voce-en voce_en.wav --testo-en voce_en_v3.txt \
  [--voce-it voce_it.wav --testo-it voce_it_v3.txt] [--guida en]
```

`rimonta.py` divide i testi con la **stessa regola** di `kokoro_tts.py` (paragrafi su riga vuota, frasi su `.!?…`), si
ferma se una frase del `.tempi.json` non coincide col testo, mette ogni paragrafo all'inizio della sua scena + 0,4 s,
allunga la scena se il paragrafo non entra (`durata = max(piano, 0,4 + paragrafo + 0,6)`; mai accelerare), allunga
l'ultimo segmento di registro, controlla la copertura dei registri e la durata totale (165–175 s), scrive
`tempi/voce_montata_en.wav` (un `atrim`+`adelay` per paragrafo), gli `.srt` (≤ 2 righe da 42 caratteri; tempo diviso per
caratteri dentro la frase) e rilancia `registri_a_js.py` e `monta.py`. Senza `--voce-it` l'italiano esce con tempi
**stimati** sulla finestra della scena. Provato **solo** in modalità `--stima`: con un WAV vero non è stato eseguito
(non verificato).

Il mix (musica, ambiente, −14 LUFS) e l'esportazione finale restano quelli di `STRUMENTI.md` §5 (`mix.sh`, `loudnorm`,
`libx264`), con la voce montata come ingresso.

## 5. L'animatic muto

**File da guardare: `video/rendering/animatic_muto_v5.mp4`.** Il file `animatic_muto_v1.mp4` chiesto dalla consegna c'è,
ma è il primo rendering, con i difetti sotto; v2–v4 sono i passaggi intermedi. Nessuno è stato cancellato. Accanto a
ogni file ci sono il registro del rendering (`.log`) e la cartella `controllo_vN/` (ffprobe, un'istantanea ogni 10 s,
fogli 3×3, conteggio del verde).

**ffprobe di v5:** h264 Constrained Baseline (qualità `draft`), yuv420p, 1920×1080, 30/1 fps, 5203 fotogrammi,
**173,433 s**, 14,9 MB, senza audio. Lint: 0 errori, 1 avviso (`nested_structure_needs_subcomposition`: il progetto usa
una sola tela SVG e non le sottocomposizioni). Tempo di rendering: 52–68 s su cinque passate.

**Previsione (00:53): regge.** 0 errori di lint; rendering in circa 1 minuto, entro i 900 s.

**Che cosa contiene:** 9 scene, con i tempi **stimati** da `rimonta.py --stima` (173,42 s), etichetta d'onestà per
tutta la durata, titolo e richiesta della traccia, dominio, `×4 · time compressed` nella scena 5, `last state held` nella
8, segnaposto magenta (`[CIFRA-S2]`, `S3`, `S3b`, `V1`, `V2`, `V3`, `S7`, `[STATO-1]`, `[k]`, `[n]`), sottotitoli EN
stimati con la scritta magenta `VO GUIDE · ESTIMATED TIMING · NOT FINAL`, apertura con wordmark e chiusura con il simbolo
v3b animato, i crediti e 0,5 s di nero.

**Difetti trovati guardando le istantanee, e correzioni:**

| Versione | Difetto | Correzione |
|---|---|---|
| v1 | verità a tutto schermo vuota nella scena 1 (0–5 s): la `clipPath` `VS` era definita due volte e valeva la prima, piccola | tolta la definizione doppia (v2) |
| v1 | etichette tagliate dal bordo del pannello (`DRON…`, `MEZZO1 · SE…`); etichette sovrapposte nelle scene 5 e 6 | etichette tenute dentro il pannello e spostate in basso se occupate (v2); nella scena 5 a ×4 restano sovrapposizioni parziali sotto le righe ocra |
| v1 | `inferred from: …` usciva dalla console; scala grafica sovrapposta alle righe di testo (scene 5 e 8) | testo a capo; scala in alto a destra; righe con fondo (v2) |
| v2 | pixel verdastri (Q11) dove il disco ciano tocca le righe ambra | alone scuro attorno al disco (v3): da 8 a 6 pixel |
| v3 | `EMPTY` barrato in **corallo**, che il piano riserva alle bande dell'affidabilità persa | barra bianca #E8EDF2 (v4) |
| v4 | «Free cells inside footprint» (piano §2): «free» è un termine vietato (Q9) | «Cells marked OBSERVED EMPTY inside footprint: [CIFRA-V3] · in simulation» (v5). **Scelta mia, da confermare:** cambia il testo del piano |

**Controlli su v5:**
- **Q11, verde:** 173 fotogrammi (1 al s, ridotti a 480×270): al più 4 pixel isolati per fotogramma, tutti nella
  scena 5 dove ciano e ambra si toccano (colori misti della codifica 4:2:0). Nessuna area grande, ma il conteggio non è 0:
  **non risolto** per il file finale. Lo deciderebbe lo stesso controllo sulla resa `delivery`.
- **Q9, termini vietati:** cercati sul testo a schermo EN e sull'`.srt` EN stimato. Resta «lost» nella voce («reliability
  is lost»), che il lessico ammette (`RELIABILITY LOST`). L'italiano non l'ho cercato.
- **Q13, etichette d'onestà:** presenti in tutte le 17 istantanee guardate; `SIMULATION` solo nella scena 8, l'unica con
  un registro del prototipo. È un controllo a vista, non quello automatico che il piano chiede.
- **Non controllati:** Q4 (parole per schermata), contrasto, Q21 margini (a vista: il testo sta nella griglia), Q33 a
  fotogramma pieno per ogni scena, il determinismo di questo progetto (provato solo in `STRUMENTI.md`).
- **Sincronia:** voce e immagine non coincidono (esempio: a 85 s il sottotitolo dice «Event: contact, inferred» prima
  dell'evento nei dati di sviluppo). È atteso con tempi stimati e dati finti. Il registro E1 vero e il `.tempi.json`
  devono accordarsi: nella scena 5, `t_reg` del segmento va scelto in modo che l'evento cada sulla frase.

## 6. Che cosa manca

1. **Registri veri** (piano §7): R1 (`lp_V1_piazzale`), R3a/b/c, R1E, R5 (riquadro di E5: **non costruito**), R2E, e Rc
   congelato. Con i campi proposti del §2 concordati con l'architetto. Finché mancano, le scene 1, 4, 5, 6 dicono
   `DEV DATA · NOT A RESULT` e non possono andare nel video finale.
2. **Cifre e stati dal verdetto** (piano §3.2): CIFRA-S2, S3, S3b, V1, V2, V3, S7 e STATO-1 sono segnaposto magenta a
   schermo e nella voce; la scena 7 mostra le tre righe dei contatori tutte con `[k] of [n]`.
3. **Voce:** non generata. Con i tempi stimati la scena 1 vuole 12,98 s (piano: 12), la 2 27,29 s, la 6 20,07, la 7
   30,08: totale **173,42 s** (stima, dentro 165–175). L'italiano stimato sfora le scene 5, 6 e 7 (applicare i tagli del
   piano §2). Tutto da rifare sul `.tempi.json` vero.
4. **Musica, ambiente, mix, sottotitoli impressi, esportazione `delivery`:** non fatti.
5. **Non costruiti o semplificati:** riquadro E5 nella scena 5; il «bordo che mangia» la sagoma nella verità (qui la sagoma
   resta, a metà opacità, con `out of sensor view`); la regola 7 (segno bianco della posizione vera alla ricomparsa); la
   decodifica `rle` delle celle del modo lungo; il carrello lento delle scene 2, 3, 7; il silenzio di 1 s (audio).
6. **Rendering in italiano:** non fatto; le righe italiane sono più lunghe e vanno controllate (Q4, Q21).
7. **Da decidere con altri ruoli:**
   - i nomi dei campi proposti (§2), con l'architetto;
   - la seconda traccia del registro corto (§3);
   - il testo di CIFRA-V3 (§5);
   - se nella scena 5 a ×4 il volume deve riempire il pannello (con i registri veri cambierà la scala:
     va scelto il riquadro `vista` in `scene/scene.json`).

## 7. Stati proposti

| Enunciato | Stato |
|---|---|
| I 18 componenti del piano §6 esistono e disegnano da un registro nel formato di `registro.py` | **Verificato** sull'insieme dichiarato: 6 registri di sviluppo e 1 corto vero, 17 istantanee guardate. Non verificato su registri lunghi veri: non esistono |
| Il disegno dipende solo dal tempo | **Sostenuto** dal codice (niente orologio, niente caso, niente rete). Il confronto md5 di due passate uguali **non è stato fatto** su questo progetto |
| Animatic: 1080p30, 173,4 s, lint pulito | **Verificato** (ffprobe, lint) |
| `rimonta.py` rimonta le scene sulla voce vera | **Non risolto**: provato solo con `--stima`. Lo deciderebbe una corsa con un WAV di Kokoro e il suo `.tempi.json` |
| Q11 (niente verde) sul video | **Non risolto**: al più 4 pixel isolati per fotogramma su v5 |

## 8. Che cosa propongo dopo

1. L'architetto produce R1 e R1E con i campi del §2 (oppure dice i suoi nomi, e io adeguo i componenti). In
   `scene.json` si cambia `file` e `stato`, poi si rilanciano `registri_a_js.py` e `monta.py`.
2. Si genera la voce guida EN con le frasi delle cifre tolte, poi si lancia `rimonta.py --voce-en …` e si rende un
   animatic v6 sonoro di sola voce.
3. All'arrivo del verdetto si riempiono i segnaposto, si lancia `monta.py --finale` (che deve passare), si rende in
   `delivery`, si fa il mix di `STRUMENTI.md` §5 e si passa a Q29.
