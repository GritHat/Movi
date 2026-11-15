# Video v3 sul volo ad alta velocità: bozza (f17-video/70-video-v3, `sciame-videomaker`)

Dalle 05:37:11 alle 05:51 del 15-11-2026 (`date -Is`). **Tutto ciò che il video mostra è simulato dalle schede,
calcolato, o su traiettorie pubbliche con un sensore simulato.** Nessun sensore fisico, nessuna prova su hardware.

## 0. In testa: cambi di stato e regole

- **Consegnato.** Tre bozze in qualità draft, tutte accanto, nessuna sovrascritta:
  - `video/rendering/MoVi_pitch_EN_v3_bozza.mp4`: la prima, con i difetti del §4 a;
  - `MoVi_pitch_EN_v3_bozza_b.mp4`: corregge il §4 a;
  - **`MoVi_pitch_EN_v3_bozza_c.mp4`: quella da guardare.**
- **Misure della bozza c (ffprobe ed ebur128).** 171,93 s; 1920×1080; 30 fps; 5158 fotogrammi; H.264 Constrained
  Baseline yuv420p; AAC 48 kHz mono; 24,4 MB; −14,7 LUFS integrati, picco −1,4 dBFS.
- **Previsioni (regola 3) violata.** Non ho scritto prima, con l'ora, le previsioni su durata e margini: le misure
  sopra sono notate dopo.
- **Indipendenza.** Uso gli stessi registri, gli stessi verdetti e lo stesso modello linguistico degli autori. Non
  ricontrollo nessuna cifra: le copio dal VERDETTO_VOLO.
- **Scritture.**
  - Ho scritto in `video/progetto_v3` (copia di `video/progetto`, che resta intatto), `video/voce`, `video/rendering`
    e in questa cartella.
  - Nella copia ho sovrascritto `index.html` e `cifre.json` solo dopo averli copiati accanto:
    `index_progetto_v2_copia.html` e `cifre_progetto_v2_copia.json`.
  - Il motore delle bozze a e b resta in `motore_volo_v3_bozza1.js` e `_bozza_b.js`.
  - Niente rm, niente git, niente sudo, niente rete.
- **Comando che rifà il video** (da `video/progetto_v3`; si ferma se l'uscita esiste):

      python3 -I strumenti/volo_a_js_v3.py            # registri F1 F3 F4 F5 -> assets/data/volo_v3.js
      python3 -I strumenti/costruisci_v3.py ../voce/uscite/en_v9_volo_v3/voce_en.wav tempi/scene_v3_en.js
      python3 -I strumenti/monta_v3.py tempi/scene_v3_en.js
      sh strumenti/rendi_v3.sh draft ../voce/uscite/en_v9_volo_v3/voce_en.wav ../rendering/<nome_nuovo>.mp4

- **Voce EN.** Kokoro `bm_george`, en-gb, velocità 1,0 (non accelerata), dal testo
  `video/voce/testi/voce_en_v7_volo.txt`: 354 parole, 164,3 s. La v6 (366 parole, 171,8 s) era troppo lunga e resta
  accanto.
- **Testo IT** accanto, `voce_it_v7_volo.txt` (366 parole): non sintetizzato e non misurato.
- **Sottotitoli EN:** `video/progetto_v3/tempi/scene_v3_en.srt`, sui tempi misurati della voce.

## 1. Scene con i tempi (bozza c)

| # | Tempo | Che cosa mostra | Etichetta | Registro / dato |
|---|---|---|---|---|
| s1 | 0:00–0:14 | titolo; due droni veloci che convergono, tracce perse, regioni che crescono | Simulation | F3, t 14–28 s |
| s2 | 0:14–0:27 | tre risposte: vedo, non vedo ma ecco dove, non so; «not observed ≠ clear» | Schematic | — |
| s3 | 0:27–0:39 | F1: aereo in avvicinamento e drone non cooperante, avviso di prossimità | Simulation | F1, 44–88 s |
| s4 | 0:39–1:02 | F4: avaria con detriti a bassa energia; evento a 30,2 s; EO e IR «reliability lost»; volume V e impronta | Simulation | F4, 27–55 s |
| s5 | 1:02–1:21 | F3: avviso, urto, tracce perse, regioni mantenute; «collision not yet recognised as an event: region kept» | Simulation | F3, 0,5–42 s |
| s6 | 1:21–1:30 | F5: ottici ciechi, «RADAR ONLY · identity PRESUMED» | Simulation | F5, 37,5–46 s |
| s7 | 1:30–2:00 | **scena chiave:** zona fissa contro regione che cresce; C(τ), r0,9(τ), verifica su 16 aerei reali; formula | Schematic, con «computed in the model · checked on ADS-B with a simulated sensor» | `prove_confidenza.json`, VERDETTO §3 |
| s8 | 2:00–2:16 | barre della latenza (CPU contro dedicato, 10 e 40 Hz) e riquadro del calcolo | Schematic, con «estimates by analogy, no measurement» | `latenza.json`, VERDETTO §4 |
| s9 | 2:16–2:28 | sito: drone dietro l'edificio, spegnimento solo guardando, altri usi | Schematic | VERDETTO §2.2–2.3 |
| s10 | 2:28–2:52 | limiti; «from prototype to deployed system» su tre gradini; marchio MoVi, SDMs, crediti | Schematic | VERDETTO §2, §4 |

## 2. Cifre usate (tutte da `video/progetto_v3/cifre.json`, con stato e fonte)

| Chiave | A schermo o in voce | Intervallo | Stato | Fonte |
|---|---|---|---|---|
| V-1 | mai «clear» dove c'era l'oggetto o un frammento | 0/200 [0; 0,019]; 0/60 [0; 0,060] | sim. | VERDETTO §2.1 |
| V-2 | evento in 0,1–0,4 s, camere non affidabili entro 3 cicli, con «optimistic trigger» | 60/60 [0,940; 1] | sim. | §2.1 |
| V-3 | detriti a bassa energia nel volume: 58/60; i peggiori 96 % e 74 % | [0,886; 0,991] | sim. | §2.1 |
| V-4 | avviso prima del primo frammento a terra (≥ 5,7 s a bordo, ≥ 0,25 s all'operatore) | 60/60 [0,940; 1] | sim., ip. | §2.1 |
| V-5 | avviso di prossimità ≥ 10 s; 16 s in questo passaggio; soglia scritta dopo | 60/60 [0,940; 1] | sim. | §2.1, INDICE F3 |
| V-6 | punto vero e frammenti nella regione: 939/939 campioni | 60/60 [0,940; 1] | sim. | §2.1 |
| V-11 | collisione non ancora riconosciuta come evento (limite) | 0/60 [0; 0,060] | sim. | §2.1 |
| V-7 | nessun falso evento | 0/200 [0; 0,019]; 0/60 [0; 0,060] | sim. | §2.1 |
| V-10 | regione per ogni traccia; identità «presunta» (scambio 0,47–0,63: limite) | 60/60 [0,940; 1] | sim. | §2.1 |
| CONF-REALI | 0,71 [0,67; 0,74] L; 0,92 [0,89; 0,94]; 0,95 [0,92; 0,97]; 0,98 [0,96; 0,99]; 0,96 [0,94; 0,98] | Wilson, casi correlati (ottimista) | pub. | §3 |
| CONF-ESEMPIO | r0,9 da 11 a 1039 m in 30 s; C della zona fissa di 300 m a ≈ 0 a 5 s | — | calc. | `prove_confidenza.json` |
| CONF-FORMULA | σ²(τ) e C(τ) | — | dim. nel modello | §3 |
| LAT-* | ≈ 700, 620 e 170 ms (primo avviso, caso peggiore); dedicato 0,08–1,2 ms; Python 0,09–11 ms (p95 55 ms, misurato in software) | — | ip., calc. da ip. | `latenza.json`, §4 |
| LP-1, LP-2, LP-11 | 200/200 [0,981; 1] ×2; 0/171 [0; 0,022] con la mappa dichiarata; 0/600 [0; 0,006] | | sim. | §2.2 |
| F1-AVVISO, F4-IMPRONTA | 33 s (passaggio 0); R 6,8 km (passaggio 0) | un esemplare | sim. | INDICE.md |

**Frasi da non dire (§5).** Ho cercato con grep, nella voce, in `cifre.json` e nel motore:
- validat, real time, certif, detect and avoid, always, tested, sub-millisecond, under a millisecond: 0 occorrenze;
- «uncontained» compare solo come NP («not proven», 0/10);
- «target» è stato tolto (diventa «goal»).

La voce dice «about a millisecond: an estimate by analogy»: non dice «sotto il millisecondo» (l'intervallo è
0,08–1,2 ms). Niente lessico d'ingaggio, nessun volto, nessun marchio di terzi.

## 3. Segnaposto aperti

1. **F3 e la regola di contatto (D1).** Oggi lo schermo dice «collision not yet recognised as an event: region kept ·
   0/60 [0; 0.060] · limit».
   - La variante è pronta in `cifre.json` → `V-11.testo_variante_D1`: «collision recognised as an event in {N} of 60
     simulated runs [lo; hi] · false events in F6 {k}/200».
   - Quando arriva `f20-chiusura/01-contatto` (oggi vuota), la variante si usa **solo** con il registro nuovo della
     scena e con F6 0/200.
   - Nella voce va cambiata la frase della scena 5.
2. **Curva tarata.** `f20-chiusura/02-taratura/curva_video.json` non c'è ancora.
   - La scena 7 usa l'esempio IMM di `prove_confidenza.json` (calcolato) e la tavola §3 del verdetto.
   - Una riga magenta a schermo segna `[PENDING: calibrated curve …]`.
3. **Voce italiana e versione IT del video:** non fatte.
4. **Fonti dell'analogia hardware** (Taalas HC1 «dato del produttore», Cerebras): segnate «da riaprire» (D5). Non le
   ho aperte.

## 4. Difetti visti (un fotogramma ogni 4 s, in `fotogrammi_bozza*/`)

**a. Bozza 1, corretti nella b:**
- regioni piene e opache, che coprivano tutto;
- scala sovrapposta alla legenda;
- la zona che cresce usciva dal pannello nella scena 7;
- sottotitoli lunghi tagliati ai bordi;
- punti reali schiacciati in cima al grafico.

**b. Bozza b, corretto nella c:** un punto ciano sotto il velo ocra appariva verdastro. Ora le tracce viste si
disegnano sopra le regioni.

**c. Aperti nella bozza c:**
1. In F5 e in F3 tardi, le regioni enormi delle tracce perse da decine di secondi (fino a 9 km, dato vero) velano di
   ocra il pannello: serve un limite al velo, oppure le tracce vecchie in grigio.
2. Scena 7:
   - la nota a piè di pagina è tagliata a destra;
   - la C(τ) della zona fissa è disegnata a segmenti fra i τ calcolati (0, 1, 2, 5, 10 …): fra 2 e 5 s la discesa
     reale non è lineare;
   - la curva va rifatta dal file tarato.
3. In F4 il volume V cresce fino a r 2,6 km (dato del registro) e copre mezza pianta. L'impronta di 6,8 km è fuori
   dal quadro: c'è solo la scritta.
4. In F3 le etichette dei droni dopo l'urto si accavallano un poco, e non c'è un segno visivo dell'urto. È voluto:
   il registro non ha l'evento.
5. **Non risolto.** V-5 dice «fra 18 e 20 s prima dell'urto» su 60 passaggi, ma il registro del passaggio 0 dà
   l'avviso 15,79 s prima del punto previsto. A schermo ho messo «≥ 10 s in 60/60 · 16 s in this run». La prova che
   lo decide è il riconto di `ritardo/anticipo` per passaggio in `passaggi_volo_v3i.jsonl`.
6. Le camere in F5 restano «RELIABILITY LOST» dopo i 3 s di cecità: è ciò che dice il registro, ma la voce dice
   «for three seconds». Va controllato se il ripristino è modellato.
7. Audio mono, solo voce (niente musica). La scena 6 dura 8,9 s ed è densa. La scena 10 dura 24 s.
8. Non ho ascoltato l'audio: l'ho solo misurato.

## 5. Che cosa propongo dopo

1. Al ritorno di 01-contatto e di 02-taratura: aggiornare `cifre.json` (versione nuova accanto), la frase della
   scena 5 e la scena 7, rigenerare la voce e rendere la bozza d.
2. Correggere i difetti c1–c3, poi rendere in qualità standard.
3. Sintetizzare la voce IT (`im_nicola`) e misurare i margini. Il testo IT è 3 % più lungo: forse servono tagli.
