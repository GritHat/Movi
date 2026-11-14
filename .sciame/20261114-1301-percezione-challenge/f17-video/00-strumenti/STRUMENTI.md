# Catena di strumenti per il video (f17-video / 00-strumenti)

Provata il 15 novembre 2026 su: Linux 7.3 (CachyOS), Node 26.13.1, ffmpeg n9.0.2, Ryzen AI 9 HX 370 (24 processori), RTX 5070 Ti Laptop 12 GB, senza sudo.
Radice di tutti i percorsi relativi: `.sciame/20261114-1301-percezione-challenge/f17-video/00-strumenti/` (qui sotto `$D`).

Legenda: **[misurato]** = eseguito e controllato qui; **[fonte]** = riportato dalla documentazione o dalla pagina d'origine, non verificato qui; **[stima]** = estrapolazione.

## 0. In breve

| Parte | Scelta | Stato |
|---|---|---|
| Animazione | HyperFrames 0.9.48 (CLI in locale, Chrome senza interfaccia in locale, GSAP in locale) | rendering vero riuscito, bit-identico su due passate |
| Dati per fotogramma | file JS/JSON con uno stato per fotogramma, disegnato in funzione del solo tempo (SVG + GSAP `onUpdate`, oppure canvas + evento `hf-seek`) | provate entrambe le vie |
| Voce | Kokoro-82M (ONNX, CPU): `bm_george` in inglese, `im_nicola` in italiano; ripiego Piper (`en_GB-cori-high`, `it_IT-paola-medium`) | 15 file generati e misurati, nessun ascolto |
| Musica | 2 brani CC BY 4.0 (Kevin MacLeod, 50–60 BPM) + 1 CC0 (John Bartmann, voce da escludere con l'ascolto) + tappeto sintetico di 180 s (numpy) | scaricati e misurati |
| Sottotitoli, mix, esportazione | ffmpeg (libass con Inter, sidechaincompress, loudnorm a due passate, libx264) | −14,0 LUFS, −1,5 dBTP; H.264 High yuv420p, AAC 48 kHz, faststart |

Remotion NON è stato installato né provato: il ripiego era previsto solo se HyperFrames non avesse reso, e ha reso al primo tentativo.

## 1. HyperFrames

### 1.1 Che cosa è installato e dove

| Cosa | Dove | Versione | Licenza |
|---|---|---|---|
| CLI `hyperframes` (npm) | `hyperframes/cli/node_modules/` | 0.9.48 (la stessa fissata dal plugin in `~/.claude/plugins/marketplaces/hyperframes/plugin.json`) | Apache-2.0 |
| GSAP (npm) | `hyperframes/cli/node_modules/gsap/`, copiato in `prova/assets/vendor/gsap.min.js` | 3.15.0 | «Standard no charge license» di GreenSock (gratuita anche per uso commerciale, NON open source; testo: gsap.com/standard-license) **[fonte]** |
| Chrome headless shell | `hyperframes/browser/chrome-headless-shell/linux-152.0.7977.30/…/chrome-headless-shell` (261 MB) | 152.0.7977.30 (quella fissata dal CLI) | Chromium, BSD e simili |
| Inter | zip in `hyperframes/scaricati/inter/Inter-4.1.zip`; file usati in `prova/assets/fonts/` (`InterVariable.woff2`, `Inter-Regular.ttf`, `Inter-SemiBold.ttf`) | 4.1, da github.com/rsms/inter (release ufficiale) | SIL OFL 1.1 (testo in `prova/assets/fonts/Inter-LICENSE-OFL.txt`) |
| JetBrains Mono | zip in `hyperframes/scaricati/jbmono/JetBrainsMono-2.304.zip`; `JetBrainsMono-Regular.woff2`, `-Bold.woff2` in `prova/assets/fonts/` | 2.304, da github.com/JetBrains/JetBrainsMono (release ufficiale) | SIL OFL 1.1 (`JetBrainsMono-OFL.txt`) |

Progetti di prova: `hyperframes/prova` (6 s, completo), `hyperframes/prova-canvas` (3 s, canvas + `hf-seek` + `fetch`), `hyperframes/prova-lunga` (30 s, per i tempi). Generatore dei dati finti: `hyperframes/script/genera_stati.mjs`.

### 1.2 Scostamenti dalle istruzioni del plugin (voluti) e tracce fuori cartella

- Il plugin chiede di lanciare il CLI con `node <PLUGIN>/skills/hyperframes/scripts/plugin-cli.mjs`, che esegue `npx hyperframes@0.9.48` dalla cartella home (cache npm globale). Per il vincolo «solo nella cartella» ho installato la stessa versione con `npm i` in `hyperframes/cli` e uso il binario locale. `doctor` lo riconosce («project-local install»).
- Le skill chiedono un segnale di telemetria a ogni avvio (`hyperframes events --skill=…`): NON eseguito. Tutti i comandi girano con `HYPERFRAMES_NO_TELEMETRY=1` (`telemetry status` → «disabled») **[misurato]**.
- **Scrittura fuori cartella non voluta:** al primo `render` il CLI ha scaricato da sé il suo Chrome 152 in `~/.cache/hyperframes/chrome` (non usa il Chrome 154 già presente in `~/.cache/puppeteer`, che `doctor` pure elenca). L'ho copiato in `hyperframes/browser/`, ho verificato che `HYPERFRAMES_BROWSER_PATH` lo usa, poi ho tolto la copia in cache con `hyperframes browser clear`. Senza quella variabile il CLI lo riscarica in `~/.cache`.
- Restano fuori cartella, creati dal CLI e non rimossi: `~/.hyperframes/{config.json,install-state.json,running}`, `~/.cache/hyperframes/{history,locks}` (1,6 MB), `~/.local/state/hyperframes/previews/*.log`, cache dei fotogrammi in `/tmp/hyperframes-extract-cache-1000`.
- Lo scheletro di `init` carica GSAP da `cdn.jsdelivr.net` e i font «Inter»/«JetBrains Mono» chiamati per nome fanno scaricare al compilatore i pesi mancanti da Google Fonts in `~/.cache/hyperframes/fonts` **[fonte: references/format.md]**. Evitato: GSAP da file locale e `@font-face` con nomi propri (`InterLocale`, `JBMonoLocale`) che puntano a `assets/fonts/`.
- npm ha bloccato lo script di post-installazione di `esbuild` (politica `allowScripts`); nessun effetto osservato su lint, anteprima e rendering.

### 1.3 Comandi che hanno funzionato

```bash
D=/home/fede/Scrivania/ed/GitHub/Movi-Hackthon/.sciame/20261114-1301-percezione-challenge/f17-video/00-strumenti
# installazione
mkdir -p $D/hyperframes/cli && cd $D/hyperframes/cli && npm init -y && npm i hyperframes@0.9.48 gsap@3.15.0 --no-fund --no-audit
# ambiente (sempre)
export HYPERFRAMES_NO_TELEMETRY=1 HYPERFRAMES_SKIP_SKILLS=1 HYPERFRAMES_NO_UPDATE_CHECK=1
export HYPERFRAMES_BROWSER_PATH=$D/hyperframes/browser/chrome-headless-shell/linux-152.0.7977.30/chrome-headless-shell-linux64/chrome-headless-shell
HF=$D/hyperframes/cli/node_modules/.bin/hyperframes
$HF doctor                                   # Node, ffmpeg, Chrome: ok
# progetto
cd $D/hyperframes && $HF init prova --skip-skills --non-interactive
# font (depositi ufficiali)
curl -sSL -o scaricati/inter/Inter-4.1.zip https://github.com/rsms/inter/releases/download/v4.1/Inter-4.1.zip
curl -sSL -o scaricati/jbmono/JetBrainsMono-2.304.zip https://github.com/JetBrains/JetBrainsMono/releases/download/v2.304/JetBrainsMono-2.304.zip
unzip -o -j -q scaricati/inter/Inter-4.1.zip web/InterVariable.woff2 LICENSE.txt extras/ttf/Inter-Regular.ttf extras/ttf/Inter-SemiBold.ttf -d prova/assets/fonts/
unzip -o -j -q scaricati/jbmono/JetBrainsMono-2.304.zip fonts/webfonts/JetBrainsMono-Regular.woff2 fonts/webfonts/JetBrainsMono-Bold.woff2 OFL.txt -d prova/assets/fonts/
cp cli/node_modules/gsap/dist/gsap.min.js prova/assets/vendor/
# ciclo di lavoro (dentro il progetto)
cd prova
$HF lint                                     # durante la scrittura
$HF check --json                             # cancello completo (NON eseguito qui: solo lint)
$HF snapshot --at 1,3                        # PNG in .hyperframes/artifacts/snapshots/<id>/
$HF preview --background --no-open           # anteprima: http://127.0.0.1:3002/#project/prova (risposta 200)
$HF preview --status ; $HF preview --stop
$HF render --quality looks --fps 30 -o renders/prova_looks.mp4      # draft | looks | delivery
```

Se il Chrome locale andasse perso: togliere `HYPERFRAMES_BROWSER_PATH`, lanciare `$HF browser ensure` (scarica in `~/.cache/hyperframes/chrome`), ricopiarlo in `hyperframes/browser/`.

### 1.4 Come si scrive una composizione (dalle skill, verificato sul progetto di prova)

- `index.html` è un documento normale; la radice ha `data-composition-id`, `data-start="0"`, `data-duration` (durata del video), `data-width="1920"`, `data-height="1080"`, `data-fps="30"`.
- Ogni elemento a tempo: `class="clip"`, `data-start`, `data-duration` (secondi); visibile in `[inizio, inizio+durata)`. L'ordine di pittura è lo `z-index`.
- Una sola timeline GSAP in pausa per composizione, registrata DOPO i tween: `window.__timelines["main"] = tl`. Tween a secondi assoluti, con `fromTo`.
- Si animano i figli di un `.clip`, non il `.clip`; trasformazioni solo via GSAP (niente `transform` CSS sullo stesso elemento).
- Vietati: `Date.now()`, `Math.random()` senza seme, timer, `requestAnimationFrame` come orologio, `repeat: -1`, richieste di rete. Tutto ciò che si vede è funzione del tempo della timeline.
- Per un film vero: una scena per file in `compositions/*.html` (contenuto dentro `<template>`, radice `#root`), montata da `index.html` con `data-composition-src`; stesso id per ospite, radice della scena e chiave della timeline (altrimenti 45 s di attesa per scena). Il progetto di prova è a file unico e per questo dà 5 avvisi `nested_structure_needs_subcomposition` (0 errori).
- Audio: `<audio id="…" class="clip" src="assets/…" data-start data-duration data-volume="1">` (anche `data-fade-in/out`, `data-media-start`); senza `id` resta fuori dal mix. Il rendering lo mette nell'MP4 come AAC 48 kHz stereo.
- Senza timeline (canvas, WebGL): `data-no-timeline` sulla radice e disegno nell'evento `hf-seek` (vedi §2).

### 1.5 Rendering di prova **[misurato]**

File: `hyperframes/prova/renders/prova_looks.mp4` — titolo animato (opacità, traslazione, sfocatura), esagono SVG che percorre una traiettoria ruotando, testo in Inter e in JetBrains Mono da file locali, pannello SVG guidato dal JSON, traccia audio (tono 220+330 Hz generato con ffmpeg). Fotogrammi 3, 90 e 179 estratti e guardati: font giusti, «frame 090» al fotogramma 90.

ffprobe: H.264 High, yuv420p, 1920×1080, 30/1 fps, 180 fotogrammi, 6,000 s, ~929 kb/s; AAC LC 48 kHz stereo ~193 kb/s; 849 kB. Audio: presente, non muto (volumedetect: media −33,8 dB, massimo −30,1 dB, coerente con il tono di prova volutamente basso).

| Prova | Durata video | Qualità, lavoratori | Tempo dichiarato dal CLI | di cui cattura | s di calcolo per s di video |
|---|---|---|---|---|---|
| `prova_looks.mp4` | 6 s | looks, 6 | 9,2 s | 4,1 s | 1,53 |
| `prova_looks_2.mp4` (macchina carica: installazioni della voce in corso) | 6 s | looks, 6 | 26,5 s | 15,8 s | 4,4 |
| `prova_delivery.mp4` | 6 s | delivery, 6 | 9,2 s | 4,1 s | 1,53 |
| `prova_draft_w12.mp4` | 6 s | draft, 12 | 6,7 s | 4,9 s | 1,1 |
| `prova-lunga/renders/lunga.mp4` (carico medio 26) | 30 s | delivery, auto | 14,0 s | 11,3 s | 0,47 |
| `prova-canvas/renders/canvas.mp4` (macchina carica; senza `data-no-timeline`) | 3 s | draft | 27,3 s | 14,1 s | 9,1 |
| `prova-canvas/renders/canvas2.mp4` (macchina carica; con `data-no-timeline`) | 3 s | draft | 25,3 s | 15,4 s | 8,4 |

- Modalità riportata dal CLI: «beginframe capture · hardware gpu» (la via veloce).
- I tempi oscillano molto perché nel frattempo giravano le prove della voce e dell'audio; il costo fisso (avvio, compilazione, audio) è 2–5 s a macchina libera.
- **[stima]** 172 s (5160 fotogrammi) con scene di questa complessità: da 1,5 a 4 minuti. Scene pesanti (molti nodi SVG, sfocature, ombre) costano di più: non misurato.
- **Determinismo [misurato]:** due rendering della stessa composizione danno gli stessi 180 fotogrammi decodificati (stesso md5 dell'elenco `framemd5`).

```bash
ffprobe -v error -show_entries stream=codec_name,profile,pix_fmt,width,height,r_frame_rate,nb_frames,sample_rate,channels,bit_rate,duration -of default=nw=1 renders/prova_looks.mp4
for f in prova_looks prova_looks_2; do ffmpeg -v error -i renders/$f.mp4 -map 0:v -f framemd5 - | grep -v '^#' | awk '{print $NF}' | md5sum; done
```

### 1.6 Audio, sottotitoli e voce secondo HyperFrames

- **Voce:** la via gratuita in locale è `hyperframes tts` (Kokoro sul dispositivo; chiede `pip install kokoro-onnx soundfile`, `doctor` lo dà «non installato»). Le altre vie NON sono state usate: HeyGen «Voice Turbo» (accesso con account, 3 minuti al mese nel piano gratuito, poi crediti), clonazione e altre voci HeyGen (a pagamento), Gemini TTS (chiave API). La skill media-use dice di chiedere l'accesso a HeyGen prima di usare gli strumenti locali: ignorato per vincolo della consegna. Kokoro è provato a parte (§3), fuori da HyperFrames, e il WAV entra come `<audio>`.
- **Musica ed effetti:** catalogo HeyGen (account), generazione (crediti), Openverse (CC BY), MusicGen locale: nessuno usato. Musica propria in `assets/` (§4).
- **Sottotitoli:** HyperFrames non ha un comando «captions»: si parte dai tempi parola per parola (`hyperframes transcribe`, che vuole whisper.cpp o Parakeet: `doctor` dà whisper-cpp «non trovato», e la sua installazione chiede di compilare) e si scrivono gruppi di parole come elementi a tempo in una composizione con `data-track-kind="captions"`. Per questo video il testo è già noto: conviene scrivere l'SRT dal copione e dai tempi della voce, e imprimerlo con ffmpeg (§5) oppure generare da quello stesso SRT gli elementi a tempo. `transcribe` NON provato.
- **Mix:** HyperFrames mescola gli `<audio>` con volume e dissolvenze; non misura i LUFS in modo confrontabile (`doctor`: «loudness numbers are only comparable on 8.0.1», qui ffmpeg 9.0.2). Consiglio: rendere il video muto o con audio di servizio, fare il mix finale con ffmpeg (§5) e riunire.

## 2. Disegno guidato dai dati **[misurato]**

Funziona in due modi; in entrambi lo stato disegnato dipende solo dal tempo `t` → indice `i = floor(t·fps + 1e-6)`.

**Via A (consigliata): dati come file JS locale + SVG + un tween GSAP che fa da orologio.** Nessun `fetch`, quindi nessuna attesa asincrona; resta modificabile nell'anteprima. File: `hyperframes/prova/index.html`.

```html
<script src="assets/data/stati.js"></script>   <!-- window.__STATI = {fps:30, n:180, frames:[{f,t,objs:[{id,x,y,poly:[[x,y]…],label}]}…]} -->
<div id="data" class="clip" data-start="0" data-duration="6"><svg viewBox="0 0 1000 480"><g id="objs"></g></svg></div>
<script>
  const tl = gsap.timeline({ paused: true });
  const S = window.__STATI, NS = "http://www.w3.org/2000/svg", layer = document.getElementById("objs"), nodes = new Map();
  function node(id) { /* crea una volta <g><polygon/><text/></g> per id e lo tiene in nodes */ }
  function drawAt(t) {
    const fr = S.frames[Math.min(S.n - 1, Math.max(0, Math.floor(t * S.fps + 1e-6)))], seen = new Set();
    for (const o of fr.objs) { const n = node(o.id); seen.add(o.id); n.g.style.display = "";
      n.p.setAttribute("points", o.poly.map(q => q.join(",")).join(" ")); n.tx.textContent = o.label; /* x, y */ }
    for (const [id, n] of nodes) if (!seen.has(id)) n.g.style.display = "none";   // oggetti spariti
  }
  const clock = { t: 0 };
  tl.to(clock, { t: 6, duration: 6, ease: "none", onUpdate: () => drawAt(clock.t) }, 0);
  drawAt(0);
  window.__timelines["main"] = tl;
</script>
```

Il file dei dati si produce dal JSON del simulatore con una riga (`"window.__STATI = " + JSON.stringify(doc) + ";"`, vedi `script/genera_stati.mjs`). Misure: 180 stati = 71 kB, 900 stati = 365 kB (3 oggetti per fotogramma).

**Via B: canvas 2D + evento `hf-seek` + `fetch` del JSON locale.** File: `hyperframes/prova-canvas/index.html`. La radice vuole `data-no-timeline` (senza: errore di lint `missing_timeline_registry` e, da documentazione, 45 s di attesa; il rendering riesce comunque). Il caricamento asincrono va dichiarato:

```js
window.__hf = window.__hf || {}; window.__hf.buildReady = window.__hf.buildReady || {};
window.__hf.buildReady["dati"] = Promise.all([fetch("assets/data/stati.json").then(r => r.json()), document.fonts.load("16px JBMonoLocale")])
  .then(([d]) => { S = d; renderAt(0); });
window.addEventListener("hf-seek", (e) => renderAt(e.detail.time));   // renderAt disegna tutto il fotogramma da t
```

Reso: 90 fotogrammi, il fotogramma 45 mostra «frame 045» e i tre poligoni con le etichette. Adatta a migliaia di primitive per fotogramma (nuvole di punti). Nota: il `fetch` di un file del progetto ha funzionato nel rendering, benché il contratto dica «niente richieste di rete». Con `data-no-timeline` aggiunto: lint 0 errori, rendering rifatto (`canvas2.mp4`, 25,3 s) con fotogrammi identici al primo (stesso md5). In entrambe le passate la cattura è stata lenta (90 fotogrammi in 14–15 s, contro 900 in 11 s della via A): la macchina era carica, ma è possibile che la via canvas sia di suo più lenta; da rimisurare a macchina libera.

Non verificato: file di dati di decine di MB (un video di 172 s con molti oggetti), interpolazione tra stati a frequenza diversa da 30 Hz (si fa in `drawAt`), prestazioni con centinaia di nodi SVG.

## 3. Voce sintetica locale

`V` = `voce/` in questa cartella; i comandi si lanciano da `$V`. Nessun ascolto: i giudizi vengono da misure (ffmpeg, controllo con riconoscimento vocale) e dalle fonti.

### 3.1 Installato e dove

| Cosa | Dove | Versione | Peso |
|---|---|---|---|
| Kokoro-82M via ONNX | `voce/venv-kokoro/` (Python 3.12, uv) | kokoro-onnx 0.6.1, onnxruntime 1.32.0 (CPU), espeakng-loader 0.2.4, phonemizer 3.6.0 | 163 MB |
| Modello Kokoro | `voce/modelli/kokoro/kokoro-v1.0.onnx`, `voices-v1.0.bin` (54 voci, tra cui `if_sara`, `im_nicola`) | v1.0 | 338 MB |
| Piper | `voce/venv-piper/` (eseguibile `venv-piper/bin/piper`, espeak-ng incluso) | piper-tts 1.8.0 | 180 MB |
| Voci Piper | `voce/modelli/piper/*.onnx` + `.onnx.json` + `.MODEL_CARD` (9 voci) | | 711 MB |
| Controllo con ASR | `voce/venv-asr/` | faster-whisper 1.2.1, modello `small` su CPU | 444 MB |
| Script | `voce/script/kokoro_tts.py`, `piper_tts.sh`, `misura.sh`, `asr_controllo.py` | | |
| Testi, uscite, fonti | `voce/testi/`, `voce/uscite/` (WAV, `misure.txt`, `tempi.txt`, `asr.txt`), `voce/fonti/` (VOICES.md e README di Kokoro), `voce/modelli/sha256.txt` | | |

```bash
uv venv --python 3.12 venv-kokoro && uv pip install --python venv-kokoro/bin/python kokoro-onnx soundfile
uv venv --python 3.12 venv-piper  && uv pip install --python venv-piper/bin/python piper-tts
uv venv --python 3.12 venv-asr    && uv pip install --python venv-asr/bin/python faster-whisper
curl -fLO https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx   # e voices-v1.0.bin
curl -fLO https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_GB/cori/high/en_GB-cori-high.onnx   # più .onnx.json e MODEL_CARD
```

### 3.2 Comandi esatti (provati): WAV 48 kHz mono 16 bit da un file di testo

Kokoro (scelta consigliata):

```bash
# inglese
venv-kokoro/bin/python script/kokoro_tts.py --testo testi/prova_en.txt --voce bm_george --lingua en-gb \
  --velocita 0.95 --pausa-frase 0.35 --pausa-paragrafo 0.8 --uscita uscite/voce_en.wav
# italiano
venv-kokoro/bin/python script/kokoro_tts.py --testo testi/prova_it.txt --voce im_nicola --lingua it \
  --velocita 1.0 --pausa-frase 0.35 --pausa-paragrafo 0.8 --uscita uscite/voce_it.wav
```

- **Velocità:** `--velocita` (1.0 normale; misurato con bm_george: 129 parole/min a 1.0, 119 a 0.9 con pausa 0,6 s).
- **Pause:** lo script sintetizza una frase alla volta e inserisce silenzi esatti: `--pausa-frase` fra le frasi, `--pausa-paragrafo` fra i paragrafi (riga vuota); un paragrafo fatto della sola riga `[pausa 1.5]` inserisce quel silenzio (misurato: 1,50 s).
- **Tempi per frase:** scrive `<uscita>.tempi.json` (inizio, fine, testo di ogni frase): serve per i sottotitoli e per agganciare le scene.
- **Livello e formato:** picco normalizzato a −3 dBFS, 0,15 s di silenzio in testa e in coda, ricampionamento 24→48 kHz con soxr. Verificato con ffprobe: pcm_s16le, 48000 Hz, mono.
- **Determinismo:** due esecuzioni danno lo stesso SHA-256.

Piper (ripiego):

```bash
script/piper_tts.sh en_GB-cori-high    testi/prova_en.txt uscite/voce_en_piper.wav 1.0 0.35
script/piper_tts.sh it_IT-paola-medium testi/prova_it.txt uscite/voce_it_piper.wav 1.1 0.35
```

Quarto argomento `--length-scale` (maggiore di 1 rallenta), quinto `--sentence-silence` in secondi. Dentro: `piper -m … -i testo -f tmp.wav --length-scale … --sentence-silence …`, poi `ffmpeg -af "volume=-3dB,adelay=150:all=1,apad=pad_dur=0.15,aresample=48000:resampler=soxr:precision=28" -ar 48000 -ac 1 -c:a pcm_s16le`. Ogni riga del file è un enunciato.

Misure e controllo: `script/misura.sh uscite/voce_en.wav 42` e `venv-asr/bin/python script/asr_controllo.py en testi/prova_en.txt uscite/voce_en.wav`.

### 3.3 Frasi di prova (`testi/prova_en.txt` 42 parole, `testi/prova_it.txt` 43 parole)

- EN: «The sensor array scans the road 30 times per second. At 120 metres, a vehicle travelling at 90 kilometres per hour is detected in under 50 milliseconds. Four cameras and 2 radar units then fuse their measurements into a single, continuous track.»
- IT: «La schiera di sensori esplora la strada 30 volte al secondo. A 120 metri, un veicolo che viaggia a 90 chilometri orari viene rilevato in meno di 50 millisecondi. Quattro telecamere e 2 radar fondono poi le loro misure in un'unica traccia continua.»

### 3.4 Misure **[misurato]** (CPU, 24 processori; velocità 1.0, pausa frase 0,35 s)

Tutti i file: 48 kHz mono pcm_s16le, 0 campioni saturi, testa 0,15–0,29 s, coda 0,15–0,49 s, nessun attacco o finale tagliato. «Errori ASR» conta le parole trascritte diverse dal testo, comprese le varianti di grafia (meters/metres, km); tra parentesi gli errori veri.

| File | Durata | Parole/min | Generazione | LUFS | Pausa interna max | Errori ASR |
|---|---|---|---|---|---|---|
| kokoro_en_af_heart | 16,98 s | 148 | 6,8 s | −20,6 | 0,45 s | 1/42 (0) |
| kokoro_en_am_michael | 18,47 s | 136 | 8,1 s | −24,9 | 0,63 s | 1/42 (0) |
| kokoro_en_bm_george | 19,50 s | 129 | 7,9 s | −20,6 | 0,46 s | 1/42 (0) |
| kokoro_en_bf_emma | 16,15 s | 156 | 6,2 s | −20,3 | 0,45 s | 1/42 (0) |
| kokoro_en_bm_fable | 18,22 s | 138 | 7,4 s | −24,7 | 0,47 s | 0/42 |
| piper_en_GB-cori-high | 16,20 s | 156 | 3,4 s (processo intero) | −17,8 | 0,61 s | 0/42 |
| piper_en_US-ljspeech-high | 16,92 s | 149 | 3,3 s | −20,7 | 0,44 s | 1/42 (0) |
| piper_en_US-norman-medium | 15,62 s | 161 | 1,8 s | −22,0 | 0,57 s | 2/42 (1) |
| piper_en_GB-alan-medium | 19,58 s | 129 | 1,8 s | −18,9 | 0,60 s | 2/42 (0) |
| piper_en_US-ryan-high (solo confronto) | 15,71 s | 160 | non misurato | −18,2 | 0,36 s | 1/42 (0) |
| piper_en_US-lessac-high (solo confronto) | 16,21 s | 155 | non misurato | −19,1 | 0,54 s | 1/42 (0) |
| kokoro_it_if_sara | 16,49 s | 156 | 8,2 s | −19,5 | 0,48 s | 2/43 (0) |
| kokoro_it_im_nicola | 19,09 s | 135 | 8,6 s | −19,9 | 0,81 s | 3/43 (0) |
| piper_it_paola-medium | 14,42 s | 179 | 1,2 s | −18,5 | 0,61 s | 6/43 (1–2) |
| piper_it_riccardo-x_low | 15,96 s | 162 | 1,3 s | −16,4 | 0,69 s | 8/43 (circa 4) |

- Kokoro: generazione pari a circa 0,4 volte la durata su CPU; per 172 s di voce **[stima]** 70–85 s di calcolo.
- I numeri sono letti correttamente nelle due lingue (l'ASR ritrova tutte le cifre con ogni voce).
- Piper rallentata peggiora: cori a 1.15 → 3/42 errori, paola a 1.2 → 10/43.
- Piper non è deterministico (due esecuzioni uguali: 15,95 e 16,26 s): generare una volta e conservare il file.

### 3.5 Licenze

| Elemento | Licenza | Fonte | Uso in video pubblico |
|---|---|---|---|
| Pesi e voci Kokoro-82M v1.0 | Apache-2.0 | huggingface.co/hexgrad/Kokoro-82M (il README dice: addestrato solo su audio permissivo o sintetico) | Sì, attribuzione non obbligatoria |
| kokoro-onnx | MIT | github.com/thewh1teagle/kokoro-onnx (ONNX dalle release `model-files-v1.0`) | Sì |
| onnxruntime | MIT | PyPI | Sì |
| phonemizer, espeak-ng | GPL-3.0 | PyPI | Sì: la GPL riguarda il programma, non l'audio prodotto |
| piper-tts 1.8.0 | GPL-3.0-or-later | github.com/OHF-voice/piper1-gpl | Sì, come sopra |
| en_GB-cori-high, en_US-norman-medium | dati LibriVox, pubblico dominio | MODEL_CARD in rhasspy/piper-voices | Sì |
| en_US-ljspeech-high | LJ Speech, pubblico dominio | MODEL_CARD | Sì |
| it_IT-paola-medium | CC0 | MODEL_CARD | Sì |
| it_IT-riccardo-x_low | M-AILABS, «See URL» | MODEL_CARD | Non verificata; qualità bassa (16 kHz) |
| en_GB-alan-medium | «See URL» | MODEL_CARD | Incerta: evitare |
| en_US-ryan-high, en_US-hfc_male | CC BY-NC-SA 4.0 | MODEL_CARD | **No** |
| en_US-lessac-high | licenza Blizzard 2013, restrittiva | MODEL_CARD | **No** |

### 3.6 Che cosa dicono le fonti sulla qualità **[fonte]**

- README di Kokoro: 82 milioni di parametri, «comparable quality to larger models».
- `voce/fonti/VOICES.md`, voto complessivo: af_bella A−, bf_emma B−, am_michael C+, bm_george C, bm_fable C, if_sara C, im_nicola C. Le voci italiane e le maschili britanniche sono addestrate su pochi minuti di audio, quindi meno rifinite delle femminili americane. Il voto di af_heart non è stato trovato nel file.
- Piper: livelli x_low, medium, high, a 22,05 kHz (riccardo a 16 kHz).

### 3.7 Raccomandazione

- **Inglese: Kokoro `bm_george`** (`--lingua en-gb`, velocità 0.95–1.0): 129 parole/min, il passo da documentario. Alternative: `bf_emma` (voto B− nelle fonti) o `af_heart`; ripiego Piper `en_GB-cori-high` (0 errori, licenza pubblico dominio).
- **Italiano: Kokoro `im_nicola`** (`--lingua it`, velocità 1.0): 135 parole/min, nessun errore vero all'ASR; alternativa `if_sara` a velocità 0.9. Ripiego Piper `it_IT-paola-medium` (CC0) con length-scale ≤ 1.1.
- Motivi: licenza Apache su pesi e voci, uscita deterministica, stesso script nelle due lingue con i tempi per frase, intelligibilità migliore in italiano. Limite: le voci scelte hanno voto C nelle fonti; vanno ascoltate sul copione vero prima di decidere.

### 3.8 Problemi incontrati

1. `sentence_pause`/`clause_pause` di kokoro-onnx agiscono solo fra blocchi oltre 510 fonemi: su testi corti non fanno nulla. Risolto sintetizzando frase per frase.
2. `if_sara` esce oltre il fondo scala (picco grezzo 1,22–1,29, 161 campioni saturi). Risolto normalizzando il picco a −3 dBFS prima della conversione a 16 bit.
3. Piper normalizza a 0 dBFS e il ricampionamento saturava 2–6 campioni. Risolto con `volume=-3dB` prima di `aresample`.
4. faster-whisper 1.2.1 fallisce con la PyAV installata (`metadata_errors`). Aggirato decodificando con ffmpeg.
5. La macchina non ha `bc` e usa la virgola decimale: `misura.sh` imposta `LC_ALL=C`.

## 4. Musica e ambiente

`R` = questa cartella (`00-strumenti`), `A` = `$R/audio`.

### 4.1 Brani scaricati (in `audio/musica/<cartella>/`) **[misurato: durata, formato, livelli; fonte: licenza, BPM]**

| Brano | Autore | Licenza | Durata e formato (ffprobe) | BPM | I / picco (ebur128) |
|---|---|---|---|---|---|
| `macleod-dreams-become-real/Dreams Become Real.mp3` | Kevin MacLeod | CC BY 4.0 | 410,07 s, MP3 256 kb/s, 44,1 kHz stereo | 60 (dichiarato) | −24,4 LUFS / −9,4 dBFS |
| `macleod-ossuary-5-rest/Ossuary 5 - Rest.mp3` | Kevin MacLeod | CC BY 4.0 | 235,78 s, MP3 256 kb/s, 44,1 kHz stereo | 50 (dichiarato) | −18,1 LUFS / −2,4 dBFS |
| `bartmann-above-the-clouds/above-the-clouds-master.mp3` | John Bartmann | CC0 1.0 | 244,02 s, MP3 ~339 kb/s, 48 kHz stereo (copertina mjpeg incorporata) | non dichiarato, non stimato | −14,0 LUFS / 0,0 dBFS |

- **Kevin MacLeod.** BPM e strumenti dal catalogo `https://incompetech.com/music/royalty-free/pieces.json` («Piano, Synths», «Calming, Somber» il primo; «Synths», «Calming, Dark, Eerie, Relaxed» il secondo). La pagina `https://incompetech.com/music/royalty-free/licenses/` dice «Creative Commons — Free. Requires that you credit the music» e rimanda a `creativecommons.org/licenses/by/4.0/`.
  - File: `https://incompetech.com/music/royalty-free/mp3-royaltyfree/Dreams%20Become%20Real.mp3` e `.../Ossuary%205%20-%20Rest.mp3`.
  - Attribuzione per i titoli di coda: «"Dreams Become Real" Kevin MacLeod (incompetech.com). Licensed under Creative Commons: By Attribution 4.0 License. http://creativecommons.org/licenses/by/4.0/» (lo stesso con "Ossuary 5 - Rest"). È la formula standard del sito; il generatore di crediti della pagina (JavaScript) non è stato letto.
  - Entrambi finiscono con una coda di silenzio (4,2 s e 3,6 s); nessun silenzio interno oltre 2 s.
- **John Bartmann.** Pagina: `https://freemusicarchive.org/music/John_Bartmann/100-ambient-atmospheric-soundtracks-straylight-drones-collection/above-the-clouds-master`, che riporta «is licensed under a CC0 1.0 Universal License»; Wikimedia Commons conferma con `{{cc0}}` su `File:John_Bartmann_-_above-the-clouds-master.ogg`. Nessuna attribuzione dovuta.
  - File: `https://files.freemusicarchive.org/storage-freemusicarchive-org/tracks/AWFdDYMxTG14bTSgfwC71CvpsDPaLdAVU1UzwZx2.mp3`.
  - **Assenza di voce NON verificata.** La pagina FMA segna «Instrumental: No»; lo stesso valore compare su altri quattro brani dell'album, quindi sembra un valore predefinito, ma senza ascolto non si può dire. Va ascoltato prima dell'uso.
  - È masterizzato forte (picco 0 dBFS): nel mix va abbassato di circa 10 dB in più rispetto ai brani di MacLeod.
- **SHA-256 (inizio…fine).** Bartmann `d13c13de…754f`, Dreams `a8ea5df5…71b0`, Ossuary `895d3f3e…3bd4`.
- **Fonti scartate.** freepd.com è chiuso («Site Closed»); la ricerca di archive.org dava errore del servizio; scottbuckley.com.au rispondeva 406 a curl; upload.wikimedia.org rispondeva 429 (per questo il brano CC0 viene da FMA, che è la fonte originale).

### 4.2 Tappeto sintetico (nessun diritto di terzi) **[misurato]**

- **numpy (consigliato):** `audio/script/tappeto.py` → `audio/uscite/tappeto_180s.wav`.
  - `uv run --no-project --with numpy python $A/script/tappeto.py $A/uscite/tappeto_180s.wav 180 7` (uscita, durata in secondi, seme).
  - Progressione Dm9 – Bbmaj7 – Fmaj7 – Am7, 15 s per accordo con dissolvenza incrociata di 6 s, tre voci scordate per nota, LFO lenti, rumore filtrato, dissolvenza di 4 s in entrata e 8 s in uscita. Deterministico a parità di seme.
  - 180,000 s, PCM 16 bit, 48 kHz stereo, −18,6 LUFS, picco −6,0 dBFS. Tempo: circa 3 minuti (script non ottimizzato).
- **Solo ffmpeg:** `audio/uscite/tappeto_ffmpeg_180s.wav`, bordone statico su re (meno interessante). 180,000 s, 48 kHz stereo, −26,7 LUFS, picco −17,5 dBFS, generato in 45 s.

```bash
ffmpeg -y -f lavfi -i "aevalsrc='0.20*sin(2*PI*73.42*t)*(1+0.3*sin(2*PI*0.05*t))+0.14*sin(2*PI*110.1*t)*(1+0.3*sin(2*PI*0.07*t+1))+0.12*sin(2*PI*146.9*t)+0.10*sin(2*PI*174.7*t)*(1+0.4*sin(2*PI*0.03*t+2))+0.08*sin(2*PI*220.2*t)*(1+0.4*sin(2*PI*0.04*t))|0.20*sin(2*PI*73.50*t)*(1+0.3*sin(2*PI*0.05*t+0.5))+0.14*sin(2*PI*109.9*t)*(1+0.3*sin(2*PI*0.06*t))+0.12*sin(2*PI*146.7*t)+0.10*sin(2*PI*174.5*t)*(1+0.4*sin(2*PI*0.035*t+1))+0.08*sin(2*PI*261.7*t)*(1+0.4*sin(2*PI*0.045*t+2))':s=48000:d=180" -af "volume=-12dB,aecho=0.8:0.7:900|1300:0.35|0.25,lowpass=f=2500,atrim=0:180,afade=t=in:d=4,afade=t=out:st=172:d=8" -c:a pcm_s16le tappeto_ffmpeg_180s.wav
```

Senza `volume=-12dB` prima di `aecho` il segnale satura a 0 dBFS; senza `atrim` la coda dell'eco allunga il file a 181,3 s.

## 5. Sottotitoli, mix, esportazione **[misurato]**

ffmpeg n9.0.2 ha `subtitles`/`ass` (libass 0.17.5), `loudnorm`, `ebur128`, `sidechaincompress`, `libx264`, `h264_nvenc` e `aac` nativo (niente libfdk).

Materiale di prova, in `audio/uscite/` salvo dove indicato: `prova_video.mp4` (testsrc2 1920×1080, 30 fps, 20 s); `audio/script/prova.srt` (tre battute, con accenti italiani); voce `voce/uscite/kokoro_en_bm_george.wav` (18,5 s, 48 kHz mono); musica Dreams Become Real; ambiente `tappeto_180s.wav`.

### 5.1 Imprimere il file .srt con uno stile

```bash
ffmpeg -y -i prova_video.mp4 -vf "subtitles=filename=$A/script/prova.srt:fontsdir=$R/hyperframes/prova/assets/fonts:force_style='FontName=Inter,FontSize=14,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BackColour=&H80000000,BorderStyle=1,Outline=1.2,Shadow=0.6,Alignment=2,MarginV=22'" -c:v libx264 -crf 18 -pix_fmt yuv420p -an prova_sottotitoli.mp4
```

- Il registro di libass conferma il font: `fontselect: (Inter, 400, 0) -> Inter-Regular`, dai TTF in `hyperframes/prova/assets/fonts`.
- Accenti resi correttamente: fotogrammi di controllo `fot_sub_14s_ritaglio.png` e `fot_finale_8s.png`.
- Le misure di `force_style` per un .srt sono in unità di una tela alta 288 righe: a 1080p i pixel sono valore × 3,75. FontSize=14 → circa 52 px; 22 → circa 82 px (troppo grande); MarginV=22 → circa 82 px dal bordo.
- Colori in formato `&HAABBGGRR`, con AA=00 opaco.
- Gli avvisi «Error opening memory font '…OFL.txt'» sono innocui (libass prova a leggere come font i file di licenza nella cartella).
- `prova_sottotitoli.mp4` è la prima prova con FontSize=22; lo stile consigliato (14) è quello impresso in `finale_prova.mp4`.

### 5.2 Mix con ducking e normalizzazione a −14 LUFS

Script: `audio/script/mix.sh VOCE MUSICA AMBIENTE DURATA_S USCITA.wav [RITARDO_VOCE_MS]`.

```bash
bash $A/script/mix.sh $R/voce/uscite/kokoro_en_bm_george.wav "$A/musica/macleod-dreams-become-real/Dreams Become Real.mp3" $A/uscite/tappeto_180s.wav 20 $A/uscite/mix_prova.wav 500
```

Passata 1, premix (`-filter_complex`):

```
[0:a]aresample=48000,aformat=channel_layouts=stereo,highpass=f=70,adelay=500:all=1,apad,atrim=0:20,asplit=2[v][chiave];
[1:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:20,volume=-14dB,afade=t=in:d=2,afade=t=out:st=17:d=3[m];
[m][chiave]sidechaincompress=threshold=0.02:ratio=8:attack=15:release=700:makeup=1[md];
[2:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:20,volume=-26dB,afade=t=in:d=2,afade=t=out:st=17:d=3[a];
[v][md][a]amix=inputs=3:normalize=0:duration=longest[mix]
```

Passata 2, misura: `-af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null -`

Passata 3, correzione: `-af "loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=…:measured_TP=…:measured_LRA=…:measured_thresh=…:offset=…:linear=true,aresample=48000" -c:a pcm_s24le`

Misura finale: `ffmpeg -i mix_prova.wav -af ebur128=peak=true -f null -`

- Premix: I = −20,88 LUFS, TP = −7,32 dBTP, LRA 2,8.
- Dopo la correzione: **I = −14,0 LUFS, picco vero −1,5 dBTP**, LRA 1,6 LU, 20,000 s, 48 kHz stereo, 24 bit.
- Avvertenza 1: il guadagno necessario (+6,9 dB) avrebbe portato il picco oltre −1,5 dBTP, quindi loudnorm è con ogni probabilità passato alla modalità dinamica (LRA sceso da 2,8 a 1,6); `normalization_type` non è stato stampato per confermarlo. Per restare in lineare: un limitatore prima (per esempio `alimiter=limit=0.45` sulla voce) oppure un obiettivo più basso.
- Avvertenza 2: con il brano di Bartmann (10 dB più forte) `volume=-14dB` sulla musica va portato a circa −24 dB.

### 5.3 Esportazione finale

```bash
ffmpeg -y -i prova_video.mp4 -i mix_prova.wav -vf "subtitles=…(come in 5.1)" -map 0:v:0 -map 1:a:0 -c:v libx264 -profile:v high -level:v 4.2 -preset slow -crf 18 -pix_fmt yuv420p -r 30 -colorspace bt709 -color_primaries bt709 -color_trc bt709 -c:a aac -b:a 320k -ar 48000 -ac 2 -movflags +faststart -shortest finale_prova.mp4
```

ffprobe su `audio/uscite/finale_prova.mp4`:

- Video: h264, profilo High, livello 4.2, yuv420p, 1920×1080, 30/1 fps, 20,000 s.
- Audio: AAC LC, 48 kHz stereo. Bitrate misurato **285 kb/s, non 320**: l'encoder AAC nativo tratta `-b:a` come obiettivo e resta sotto quando il materiale è semplice.
- Faststart confermato: ftyp (0), moov (posizione 40), mdat (22788).
- Loudness del file finale: I = −14,0 LUFS, picco −1,5 dBTP (la codifica AAC non ha spostato le misure).
- Tempo: 8,2 s per 20 s di video (preset slow); testsrc2 è un caso sfavorevole (9,2 Mb/s).
- Con il video vero: l'ingresso è l'MP4 di HyperFrames (già H.264 CRF 16 in `looks`); per non ricodificare due volte conviene rendere da HyperFrames con `--quality delivery` o `--format png-sequence` e fare qui l'unica codifica finale (non provato).

## 6. Raccomandazione sullo strumento di animazione

**HyperFrames**, per un video di 172 s guidato da dati:

- qui funziona tutto e subito (installazione 4 s, rendering 6 s in 9 s, 30 s in 14 s), con uscita già H.264 High yuv420p 1080p30 e fotogrammi identici a ogni passata;
- la composizione è HTML, CSS e SVG: i registri del simulatore si disegnano con poche righe (§2) e una squadra di cinque può dividersi le scene in file separati (`compositions/*.html`);
- lint, istantanee e anteprima locale danno un ciclo di correzione rapido; licenza Apache-2.0.

Riserve: prodotto giovane (0.9.x) e spinto verso i servizi HeyGen (account, crediti, telemetria attiva se non la si spegne, scritture in `~/.cache` e `~/.hyperframes`); GSAP è gratuito ma non libero; le skill impongono un processo (storia, SPEC, revisione) pensato per film generici.

Alternative, NON provate qui **[fonte]**: **Remotion** (React; maturo, ottimo per dati; licenza propria: gratuito per singoli e per organizzazioni fino a 3 persone, a pagamento oltre — con una squadra di 5 va verificato prima); **Motion Canvas** (TypeScript, MIT; animazioni procedurali a generatori, editor proprio; meno adatto a impaginare testo e a ricevere HTML/SVG già pronti; stato di manutenzione da verificare). Ripiego consigliato se HyperFrames desse problemi su scene pesanti: Remotion, riusando la stessa funzione `drawAt(t)`.

## 7. Ciò che NON è stato verificato

- **Audio:** nessun ascolto di voci, musica, ducking; assenza di voce nel brano di Bartmann e suo BPM; pronuncia di sigle e termini del copione vero; il testo esatto dell'attribuzione generata da incompetech; la modalità effettiva (lineare o dinamica) di loudnorm nella seconda passata; il mix su 172 s con la voce vera; la licenza delle voci Piper riccardo e alan; Kokoro su GPU e altri motori (pacchetto `kokoro` con PyTorch, XTTS, F5, Chatterbox).
- **Bitrate AAC:** chiesto 320 kb/s, ottenuto 285 kb/s con l'encoder nativo (resta sotto l'obiettivo su materiale semplice); libfdk_aac non è disponibile.
- **Tracce fuori cartella dalle prove audio e voce:** il modello Whisper `small` era già nella cache `~/.cache/huggingface`; la cache di uv è quella predefinita dell'utente.

- Ascolto di qualunque audio e visione del video in movimento: controllati solo fotogrammi singoli e misure.
- Un rendering di 172 s e scene pesanti; `hyperframes check` completo (layout, contrasto), `transcribe`, `tts` integrato, sottocomposizioni in file separati, transizioni, rendering con `--gpu` (NVENC) e in Docker.
- Remotion e Motion Canvas (nessuna installazione).
- I termini esatti della licenza di GSAP e di Remotion: riportati dalle loro pagine, non riletti ora.
