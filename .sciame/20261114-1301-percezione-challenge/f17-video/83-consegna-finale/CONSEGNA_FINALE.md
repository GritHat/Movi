# Consegna finale del video MoVi (f17-video/83-consegna-finale, `sciame-videomaker`)

Lavoro dalle 07:43 alle 07:58 del 15-11-2026 (`date -Is`). Tutto ciò che il video mostra è simulato: nessun sensore
fisico. MoVi osserva e avvisa, nient'altro.

## 0. In testa

- **Consegnati (nuovi, accanto alle versioni precedenti, che restano tutte, v3b e v3c comprese):**

| File (`video/consegna/`) | Durata (ffprobe, formato) | Note |
|---|---|---|
| `MoVi_pitch_EN_final.mp4` | **174,379 s** ≤ 176,0 (dentro 170–175) | sha256 e6a7124d… |
| `MoVi_pitch_IT_final.mp4` | **170,469 s** ≤ 176,0 (dentro 170–175) | sha256 50d0220e…; grafica a schermo in inglese, voce e sottotitoli impressi in italiano |
| `MoVi_pitch_EN_final.srt` | 30 cue, fine 171,229 s | identico a quello della v3c (`cmp`) |
| `MoVi_pitch_IT_final.srt` | 30 cue, fine 167,319 s | per il video IT; 0 errori |
| `MoVi_pitch_IT_sui_tempi_EN_final.srt` | 30 cue | italiano sui tempi del video EN |
| `MoVi_pitch_IT_final_impressi.srt` | — | tempi dei sottotitoli impressi; ha 20 code sovrapposte di ~0,2 s (difetto noto, D7): **non** è il file da consegnare |
| `MoVi_copione_final.md`, `MoVi_registro_cifre_final.md` | — | copione (voce invariata) con i cambi a schermo; registro con chiave, intervallo, stato, fonte |
| `genera_versione_italiana_final.sh` | — | rigenera la versione italiana |

- **Il final è una v3d**: stessa voce e stessi tempi della v3c; cambia solo la grafica. Le durate sono identiche a
  quelle della v3c, come previsto (P1, P2).
- **Regole violate, anche per errore:** nessuna nota. Niente `rm`, niente git, sudo o rete. Ho scritto solo in
  `video/` e in questa cartella.
  - `video/progetto_v3/index.html` è stato rigenerato da `monta_v3d.py`, che prima ne copia la versione in uso in
    `versioni/`. Ora punta alla v3d EN.
  - Ho riscritto in loco un file mio: `genera_versione_italiana_final.sh`, per due commenti, prima di eseguirlo.
- **Indipendenza.** Autore e controllore sono la stessa persona. Gli script di controllo, `controlla.py` e
  `controlli_srt.py`, sono copie di quelli di 81-qa e 80-integrazione. Le cifre vengono da `cifre_v3d.json`, che
  deriva dagli stessi rapporti c1 e dallo stesso verdetto. Il controllo non copre gli errori di quelle fonti.

## 1. Correzioni applicate (tutte a durata zero)

| Fonte | Correzione | Prova |
|---|---|---|
| QA_V3C D1, REVISIONE C1 (verità) | In LIMITS, la riga di prima di c1, «debris warning to the carrier not reliable», diventa tre righe: «radar blinded: carrier warned only with a fix under test (sim.)», «that fix: warning not localised; reacquisition still partial», «that fix: false warnings 11/200 [0.031; 0.096] (sim.)». L'unica cifra è controllata dallo script contro F7R-C1-FALSI | OCR 150–170 s: «not reliable» 0 volte, «fix under test» a 156–166 s (EN) e 152–162 s (IT). Fotogramma `fot_en_controllo/t160.png` |
| QA_V3C D2 | In F7 le tre righe di limite c1 (49/60 e 40/60; 565 m con mediana 8 s; 11/200) compaiono 1,2, 1,8 e 2,4 s dopo «59/59» e restano fino alla fine della scena (circa 12 s invece di 4) | OCR EN: 59/59, 49/60, 565 e 11/200 insieme in tutti i fotogrammi da 126 a 138 s; IT da 124 a 136 s |
| QA_V3C D4 | Nel pannello in pianta la scala si allarga da 470 a 560 m: il drone seguito resta dentro il pannello e la sua etichetta non copre più «CARRIER · MoVi on board» | `t126.png`, `t132.png` |
| REVISIONE C3 | La barra si chiama «position confidence, tracked drone (computed in the model)». Sotto c'è «identity: confirmed / presumed / presumed, doubtful», letta dal registro (campo 8). I valori della barra sono quelli del registro: confidenza 1 fino a 0,5 s di NOT SEEN, poi scende fino a 0,1657 | `t117.png`, `t126.png` |
| REVISIONE C4 | Tolte le sigle: «C-TAR», «min. progressive» (diventa «computed in the model»), «Wilson 95 % per case» (diventa «95 % intervals per case»), «(F5)» (diventa «with optics blinded»), «LP-1 · S» e «LP-4 · S» (diventano «simulation») | OCR: 0 occorrenze |
| REVISIONE C5 | «fixed zone at last sighting · 150 m (for comparison)» sta dentro il pannello | `foglio_a.png` |
| REVISIONE C6 | In s1, dalla domanda (9,9 s), c'è la riga «not observed ≠ clear» | `foglio_a.png` |

**Non applicate.**
- **Voce: D3 («In simulation, …») e C2 («reacquisition is still partial»).** Richiedono di rigenerare la voce e i tempi,
  con il rischio di sforare 175 s. Questi due punti sono già scritti a schermo: l'etichetta SIMULATION, «same seeds ·
  sim.» e la riga sulla riacquisizione.
- **D5 e giurato 9 (in parte):** a 6 s e a 62 s restano le etichette doppie «SEEN».
- **C7:** manca un fermo della croce del vero dentro NOT SEEN in s3.
- **D8:** la riga «spurious identities» non compare a schermo (OCR: 0).
- **«0.9 (optimistic)»:** non l'ho messo, perché nessuna fonte che ho letto dice che la soglia 0,9 sia ottimista. Resta
  «flash trigger optimistic».

## 2. Controlli automatici sui file finali

| Voce | EN final | IT final | Esito |
|---|---|---|---|
| Durata (bloccante, ≤ 176,0 s) | 174,379 s | 170,469 s | **regge** |
| Formato | H.264 High, yuv420p, 1920×1080, 30 fps, bt709; AAC LC 48 kHz stereo; 22,0 MB | uguale; 22,1 MB | regge |
| Loudness | −14,0 LUFS, LRA 2,8 LU, picco −2,4 dBFS | −14,0 LUFS, LRA 3,9 LU, picco −2,1 dBFS | regge |
| Verde (G > 90, G > R+40, G > B+40, un fotogramma ogni 2 s) | al massimo 20 px | al massimo 32 px | regge: pixel sparsi di antialias, 0 fotogrammi oltre 200 px, come nella v3c |
| Etichetta SIMULATION/SCHEMATIC | 87/87 fotogrammi | 85/85 | sostenuto dai dati sul campione |
| Lessico vietato (OCR e .srt) | 0 | 0 | regge. «clear», «never», «mai» e «libero» compaiono solo negati o condizionati (`contesti_lessico.txt`) |
| .srt | 30 cue, 0 errori | 30 cue, 0 errori | regge; `_impressi`: 20 sovrapposizioni (noto) |
| Ordine delle scene | F7 a 110,2–140,0 s, dopo il volo veloce e prima di «Also: the site…» | uguale | regge (`tempi/scene_v3d_*.json`) |

Le uscite sono in questa cartella: `previsioni.txt` (07:45, prima delle misure), `esito_en.txt`, `esito_it.txt`,
`ocr_fot_en.json`, `ocr_fot_it.json`, `contesti_lessico.txt`, `ffprobe_loudness_final.txt`, `controlli_srt.txt`,
`sha256_final.txt` e `fot_en_controllo/`.

**Previsioni.**
- **P1–P2 reggono:** le durate sono invariate.
- **P3 regge:** «not reliable» non c'è più, «fix under test» sì.
- **P4 regge.**
- **P5 regge:** da 126 s sono a schermo tutti e quattro i numeri.

## 3. Licenze

| Materiale | Origine | Licenza |
|---|---|---|
| Voce EN e IT | Kokoro-82M (ONNX, kokoro-onnx), voci sintetiche `bm_george` e `im_nicola`, velocità 1,0; nessuna persona reale | Apache-2.0 (pesi e voci); kokoro-onnx MIT (`00-strumenti/STRUMENTI.md`, righe 249–250) |
| Musica | `tappeto_180s.wav`, generato con numpy per questo video; ambiente: rumore di ffmpeg | opera propria |
| Caratteri | Inter 4.1, JetBrains Mono | SIL OFL 1.1 |
| GSAP | 3.15.0 | GreenSock «Standard no charge license»: gratuita anche per uso commerciale, ma non open source |
| HyperFrames CLI | 0.9.48 (`package.json`) | Apache-2.0 |
| Marchi MoVi e SDMs | dal progetto | del gruppo |

I titoli di coda dicono voce, musica, caratteri e GSAP.

## 4. Come si rigenera

**Italiano**, da zero, voce compresa:

    sh video/consegna/genera_versione_italiana_final.sh delivery <etichetta_nuova>

- Si ferma se un'uscita esiste già.
- Il file `MoVi_pitch_IT_final.mp4` di questa consegna è stato fatto riusando la voce IT della v3c, con lo stesso testo
  `voce_it_v3c.txt`:

      VOCE_ESISTENTE=video/voce/uscite/it_v3c_v3c sh video/consegna/genera_versione_italiana_final.sh delivery final

- **Non verificato:** se Kokoro, rigenerando la voce, dia gli stessi tempi.

**Inglese**, da `video/progetto_v3`:

    python3 -I strumenti/cifre_v3d.py        # solo se manca cifre_v3d.json
    python3 -I strumenti/costruisci_v3d.py ../voce/uscite/en_v3c/voce_en.wav tempi/<nuovo>_en.js --max 175.0
    python3 -I strumenti/monta_v3d.py tempi/<nuovo>_en.js en
    sh strumenti/rendi_finale.sh delivery ../rendering/<immagine>.mp4
    python3 -I strumenti/audio_finale.py ../rendering/<immagine>.mp4 ../consegna/<nuovo>.mp4 ../rendering/<cartella> \
        tempi/<nuovo>_en.json ../voce/uscite/en_v3c/voce_en.wav --silenzi 117.169

File nuovi nel progetto (le versioni v3c restano):
- `strumenti/cifre_v3d.py`, `costruisci_v3d.py` e `monta_v3d.py`;
- `cifre_v3d.json`, `assets/data/cifre_v3d.js` e `assets/js/motore_v3d.js`;
- `tempi/scene_v3d_en.*` e `tempi/scene_v3d_it_final.*`;
- in `video/rendering/`: le immagini `MoVi_pitch_*_v3d_*` e le cartelle audio `audio_MoVi_pitch_*_final`.

## 5. Che cosa nessuno ha verificato

- **L'ascolto umano delle due versioni.** Pronuncia italiana e di «MoVi» e «SDMs», musica sotto la voce, silenzio
  all'urto di F7 (117,2 s EN). Nessuno l'ha ascoltato: né io, né la QA, né il giurato.
- **La comprensione alla prima visione.** Nessun lettore nuovo ha guardato la versione final.
- **I fotogrammi fra un campione e l'altro.** I campioni sono uno ogni 2 s, più 11 fotogrammi letti a vista.
- **La leggibilità delle righe da 18 px su schermi piccoli.**
- **Le cifre c1.** Sono copiate dai rapporti c1, non ricontate da me.
