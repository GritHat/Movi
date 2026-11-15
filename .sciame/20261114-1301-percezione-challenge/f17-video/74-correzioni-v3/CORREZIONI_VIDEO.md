# Correzioni del video v3 → v3b (f17-video/74-correzioni-v3, `sciame-videomaker`)

Dalle 07:02 alle 07:19 del 15-11-2026 (`date -Is`). Tutto ciò che il video mostra è simulato, calcolato o su traiettorie
pubbliche con un sensore simulato: nessun sensore fisico, nessuna prova su hardware.

## 0. In testa

- **Consegna: `video/consegna/MoVi_pitch_EN_v3b.mp4`, durata 174,632 s (ffprobe, formato) ≤ 176,0 s**, margine 1,37 s.
  La v3 resta intatta.
- **Regola violata (n. 3).** Non ho scritto previsioni con soglia prima delle misure. Le soglie usate sono quelle della
  consegna, fissate prima: 176,0 s, −14 LUFS, verde 0, etichetta sempre presente, 0 frasi vietate.
- **Niente cancellato.** Due file di prova sono stati spostati con `mv -n` (§ 3). `progetto_v3/index.html` è stato
  rigenerato da `monta_v3b.py`, che prima lo copia in `versioni/` (`index.20261115-070602.html` e successivo). Il
  motore e gli script sono copie nuove; gli originali restano.
- **Indipendenza.** Autore e controllore coincidono (sono io), con lo stesso verdetto e gli stessi registri. Il controllo
  copre il formato, la durata, il loudness, il verde, le etichette e il lessico. Non copre gli errori dei registri né
  quelli del verdetto. L'ascolto umano non è stato fatto: è **non verificato**.

## 1. Correzioni applicate

| # | Fonte | Correzione | Effetto sulla durata |
|---|---|---|---|
| 1 | QA D1 | In s8 (F7) c'è la legenda «+ truth (simulation only, MoVi does not see it) · ● seen · ◌ not seen», su fondo, sotto il titolo del pannello. L'etichetta del drone è spostata più in basso, per non sovrapporsi | 0 |
| 2 | QA D2, giurato 2 | La voce F7 dice ora: «With the radar undisturbed, the tracked drone stayed inside its region in sixty of sixty simulated runs. With the radar blinded for up to two seconds: at least fifty-nine of sixty, and never a fragment called clear.» (F7-CONT e F7R-CIECO del verdetto) | −3 parole |
| 3 | QA D3 | «an engine failure» diventa «an in-flight failure»; «An engine fails» diventa «An aircraft fails in flight» | +2 parole |
| 4 | QA D5 | I crediti dicono «animation GSAP 3.15 (standard license)» | 0 |
| 5 | giurato 1 (F-806) | La riga d'evento in F7 è «EVENT: nearby collision · inferred (optimistic)». Il testo del verdetto § 8 resta, con l'innesco ottimista detto sulla stessa riga | 0 |
| 6 | giurato 2 (F-805 L) | L'avviso al portatore dice «conservative, not selective · radar blinded: can be late» (non discriminante: 60/60 anche senza frammenti vicini) | 0 |
| 7 | giurato 4 | La voce s7 dice «…eighty-five to eighty-nine times in a hundred, below nine in ten, mostly one route» al posto di «from one to thirty seconds». Le note sotto i grafici passano da 16 px grigie a 18 px bianche (la richiesta era ≥ 20: non raggiunta, per lo spazio) | ≈ 0 |
| 8 | giurato 6 | «The same core» diventa «The same approach works on a site» | 0 |
| 9 | giurato 13 | In F3, «in every simulated run» diventa «in sixty of sixty runs» (V-6) | +1 parola |
| 10 | giurato 10 | Le sigle interne (V-1, C-TAR, F7-CONT…) sono tolte dalle righe a schermo; restano nel registro | 0 |
| 11 | giurato 11 | «limit · with a forward-only radar instead: side/behind collision seen 1/60 and 0/60…» | 0 |
| 12 | giurato 7 (parziale) | Il titolo di s1 è «Fast drones on a collision course» (era «Two fast drones, then contact») | 0 |
| 13 | giurato 3 (parziale) | «fixed zone at last sighting · 150 m (for comparison)». L'innesco ottimista di V-2 resta solo a schermo, come nella v3: aggiungerlo alla voce costava circa 1 s | 0 |
| — | per il tempo | Ho accorciato le code: s7 da 1,5 a 1,2 s, s8 da 2,5 a 2,0 s, s10 da 4,0 a 3,4 s. La voce non è accelerata (Kokoro 1,0). I titoli di coda si sovrappongono alla voce per circa 2,6 s, contro i 2,0 s della v3 | −1,4 s |

Una prima prova (voce `en_v3b`, totale 175,904 s) ha superato il mio limite interno di 175,0 s, quindi ho accorciato le
code. Nella seconda prova il .srt conteneva «under target»: «target» è nell'elenco del lessico vietato del QA, anche se
lì il senso era di obiettivo. Ho rifatto la voce (`en_v3b_r2`) con «below nine in ten».

**Non applicate (restano):**
- QA D6, la riga V-11 più ricca: per non aggiungere «within 2 s» accanto al 48/60 di F-803.
- Giurato 5: l'immagine per V-1 in s3 e «six scenarios with the core».
- Giurato 7: l'apertura con il lampo.
- Giurato 8: la legenda delle regioni piene.
- Giurato 9: le etichette tagliate dal bordo.
- Giurato 12: la riga V-11 («2/60 false events»: non ho verificato in quale prova).
- QA D8: c1 non è adottato dal verdetto, quindi le righe di s8 e s10 restano come sono.
- Documentale: CONSEGNA_V3 § 2 (5→54 m) e i 320 kb/s dichiarati (la misura è 283 kb/s).
- `MoVi_copione_v3.md` e `MoVi_registro_cifre_v3.md` non sono aggiornati alla v3b.
- La versione IT v3b del video: c'è solo il .srt IT v3b.

## 2. Controlli sul file finale (comandi in questa cartella)

| Voce | Misura | Esito |
|---|---|---|
| Durata | 174,632 s (formato e audio); 5238 quadri a 30 fps | **regge** (≤ 176,0) |
| Formato | H.264 High, yuv420p, 1920×1080, 30 fps, bt709; AAC LC 48 kHz stereo, 283 kb/s; `moov` in testa (faststart); 22,1 MB (`ffprobe_v3b.txt`) | regge |
| Loudness | −14,0 LUFS I, LRA 2,8 LU, picco vero −2,3 dBTP (`video/rendering/audio_MoVi_pitch_EN_v3b/ebur128_finale.txt`) | regge |
| Verde | 1/87 fotogrammi (f_042, 83 s): 28 px dove il punto «last seen» ciano incontra il cerchio ocra, per l'antialias (`ritaglio_f042.png`). Non c'è nessun elemento verde | regge: falso positivo del criterio, come in QA_V3 |
| Etichetta d'onestà | 87/87 fotogrammi (uno ogni 2 s): 83 letti dall'OCR, 4 controllati a vista (`etichette_mancanti_ocr.png`) | sostenuto dai dati sul campione |
| Frasi vietate | `controlli_srt.py` su .srt EN e IT v3b: 0 occorrenze; i due «never» / «mai» sono condizionati. OCR di 87 fotogrammi: 0 occorrenze di validat, target, threat, intercept, always, real time, certif, guarant | regge |
| Sottotitoli | EN e IT: 30 cue, tempi monotoni, ≤ 21 car/s, ultima cue a 171,48 s. Il .srt IT ha i tempi del video EN v3b, frase per frase | regge |
| Lettura a piena risoluzione | 124 s (legenda F7, riga d'evento), 171 s (crediti con GSAP) | regge. **Difetto basso:** in F7 la parola «(optimistic)» tocca l'etichetta «0.9» della barra |

Sha256: in `sha256_v3b.txt`. Il video ha 96c01c44…09eb4f.

## 3. File

**Consegnati** (`video/consegna/`): `MoVi_pitch_EN_v3b.mp4`, `MoVi_pitch_EN_v3b.srt`, `MoVi_pitch_IT_v3b.srt`.

**Progetto** (`video/progetto_v3/`):
- `assets/js/motore_v3b.js`;
- `strumenti/costruisci_v3b.py` e `strumenti/monta_v3b.py`;
- `tempi/scene_v3b_r2_en.{js,json,srt}` (finale) e `tempi/scene_v3b_en.*` (prima prova);
- `index.html`, che ora punta alla v3b.

**Voce:**
- `video/voce/testi/voce_en_v3b_r2.txt` (finale) e `voce_en_v3b.txt` (prova);
- `video/voce/uscite/en_v3b_r2/` (finale) e `en_v3b/` (prova).

**Prove intermedie** (`video/rendering/`):
- `MoVi_pitch_EN_v3b_immagine.mp4` (prima prova, 174,53 s);
- `MoVi_pitch_EN_v3b_r2_immagine.mp4`;
- `audio_MoVi_pitch_EN_v3b/`;
- `MoVi_pitch_EN_v3b_prova1_con_target.srt` e `MoVi_pitch_IT_v3b_prova1.srt`, spostati con `mv -n`.

**Comando per rifare il video** (da `video/progetto_v3`):

    python3 -I strumenti/costruisci_v3b.py ../voce/uscite/en_v3b_r2/voce_en.wav tempi/scene_v3b_r2_en.js --max 175.0
    python3 -I strumenti/monta_v3b.py tempi/scene_v3b_r2_en.js en
    sh strumenti/rendi_finale.sh delivery ../rendering/<immagine_nuova>.mp4
    python3 -I strumenti/audio_finale.py ../rendering/<immagine>.mp4 ../consegna/<nuovo>.mp4 ../rendering/<cartella_nuova> \
        tempi/scene_v3b_r2_en.json ../voce/uscite/en_v3b_r2/voce_en.wav --silenzi 116.614

La voce si fa con `kokoro_tts.py --voce bm_george --lingua en-gb --velocita 1.0 --pausa-frase 0.35 --pausa-paragrafo 0.8`.

## 4. Dopo

1. Un ascolto umano dei 174,6 s: la pronuncia, la musica sotto la voce e il silenzio all'urto (116,6 s).
2. Se c'è tempo, una correzione da zero secondi: spostare a destra l'etichetta «0.9» in F7, oppure accorciare la riga
   d'evento.
3. Aggiornare il copione e il registro delle cifre alla v3b. Se serve, rifare la versione IT con
   `genera_versione_italiana_v3.sh`, adattato a `costruisci_v3b`.
