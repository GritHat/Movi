# Video v3, versione finale: consegna (f17-video/71-consegna-v3, `sciame-videomaker`)

Dalle 06:34:57 alle 07:00 circa del 15-11-2026 (`date -Is`). **Tutto ciò che il video mostra è simulato dalle schede,
calcolato, o su traiettorie pubbliche con un sensore simulato.** Nessun sensore fisico, nessuna prova su hardware. Il sistema
osserva e avvisa; nessuna funzione d'ingaggio.

## 0. In testa: esito, cambi di stato, regole

- **Consegnato** `video/consegna/MoVi_pitch_EN_v3.mp4`: **173,856 s** (ffprobe, formato; video 173,833 s, audio
  173,856 s). Il vincolo dell'utente (mai oltre 176,0 s) è rispettato con 2,1 s di margine; la finestra 168–175 s pure.
  La voce non è accelerata (Kokoro velocità 1,0).
- **Formato misurato:** H.264 High, yuv420p, 1920×1080, 30 fps, 5215 fotogrammi, bt709; AAC LC 48 kHz stereo 320 kb/s;
  `moov` in testa (faststart: verificato con i primi byte del file); 22,1 MB.
- **Loudness (ebur128 sul file finale):** −14,0 LUFS integrati, LRA 2,9 LU, picco vero −2,3 dBTP (≤ −1).
  File: `video/rendering/audio_MoVi_pitch_EN_v3/ebur128_finale.txt`.
- **Fotogrammi (1 al secondo, 174):** 0 con verde (criterio G > R+40, G > B+40, G > 90 su più di 20 pixel); 0 senza
  l'etichetta d'onestà in alto a destra; «DEV DATA» e «PENDING» assenti nei sorgenti del video.
  File: `video/rendering/controllo_MoVi_pitch_EN_v3/controllo_fotogrammi_finale.txt`.
- **Previsioni** (`PREVISIONI.md`, 06:39:24, prima delle misure): PV-1 regge (voce 158,8 s); PV-2 regge (173,86 s);
  PV-3 regge (F7 30,3 s); PV-4 regge (−14,0 LUFS, −2,3 dBTP); PV-5 regge (0 fotogrammi); **PV-6 smentita**: la voce IT
  è più corta dell'EN (152,8 contro 158,8 s, −3,8 %), perché im_nicola ha pause fra frasi di 0,05 s.
- **Regole.**
  - Niente `rm`, niente git, niente sudo, niente rete.
  - **Tre file difettosi spostati con `mv -n`, non cancellati.** Due mix finivano a 170,9 s: la voce montata si fermava
    all'ultima parola e `-shortest` tagliava i titoli di coda. Il terzo mostrava «0.84» invece di 0,85 (arrotondamento di
    0,845). Sono in `video/rendering/MoVi_pitch_EN_v3_difettoso_audio_corto_170.9s.mp4`, `…_difettoso2_audio_corto.mp4`
    e `…_prima_correzione_084.mp4`, con le loro cartelle audio.
  - `index.html` di progetto_v3 è stato riscritto da `monta_finale.py`, che prima copia il precedente in `versioni/`.
  - Il motore nuovo è `motore_finale.js`; la v3 della bozza resta.
- **Indipendenza.** Con gli autori condivido i registri, i verdetti, il modello linguistico e il simulatore. Non ho
  ricontato nessuna cifra: le copio dal blocco del verdetto. Il controllo automatico di `cifre_finale.py` copre solo gli
  errori di trascrizione fra il blocco e lo schermo.

## 1. Comando che rifà il video (da `video/progetto_v3`; ogni passo si ferma se l'uscita esiste)

    python3 -I strumenti/cifre_finale.py                       # blocco del verdetto -> cifre_finale.json/.js
    python3 -I strumenti/volo_finale.py                        # registri F1 F3 F4 F5 F7r + curve -> assets/data/volo_finale.js
    # voce: kokoro_tts.py --voce bm_george --lingua en-gb --velocita 1.0 --pausa-frase 0.35 --pausa-paragrafo 0.8
    #       testo video/voce/testi/voce_en_v8_finale.txt -> video/voce/uscite/en_v10_finale_v3/voce_en.wav
    python3 -I strumenti/costruisci_finale.py ../voce/uscite/en_v10_finale_v3/voce_en.wav tempi/scene_finale_en.js --max 176.0
    python3 -I strumenti/monta_finale.py tempi/scene_finale_en.js en
    sh strumenti/rendi_finale.sh delivery ../rendering/<immagine_nuova>.mp4
    python3 -I strumenti/audio_finale.py ../rendering/<immagine>.mp4 ../consegna/<nuovo>.mp4 ../rendering/<cartella_nuova> \
        tempi/scene_finale_en.json ../voce/uscite/en_v10_finale_v3/voce_en.wav --silenzi 115.677

`costruisci_finale.py` esce con il codice 4 se il totale supera 176,0 s: in quel caso si taglia il testo, mai si accelera
la voce.

## 2. Scene (tempi misurati)

| # | Tempo | Contenuto | Etichetta | Dati |
|---|---|---|---|---|
| s1 | 0,0–13,2 | titolo; due droni veloci, tracce perse | SIMULATION (il verdetto dice Schematic: la scena mostra il registro F3, quindi Simulation) | F3 |
| s2 | 13,2–26,1 | tre risposte; «not observed ≠ clear» | SCHEMATIC | — |
| s3 | 26,1–34,1 | F1 | SIMULATION | V-1 |
| s4 | 34,1–54,8 | F4, avaria con detriti a bassa energia | SIMULATION | V-2, V-3 |
| s5 | 54,8–73,1 | F3: avviso, urto, regione mantenuta; «collision not yet declared as an event: region kept»; riga grigia della regola in prova | SIMULATION | V-5, V-6, V-11-PROVA |
| s6 | 73,1–82,8 | F5, ottici accecati; «identity PRESUMED» | SIMULATION | V-10 |
| s7 | 82,8–108,7 | regione che segue la previsione e cresce; C(τ) e r0,9(τ) **dalla curva tarata**; punti per fascia; virata in rosso | SCHEMATIC + PUBLIC TRAJECTORIES | C-TAR-* |
| **s8** | **108,7–139,1 (30,3 s)** | **F7 «scorta»**: vista dal drone portatore; bersaglio veloce più avanti; urto accanto con lampo e fumo (illustrativi, dichiarato), detriti tracciati; radar e camera «UNRELIABLE · saturated»; il bersaglio «NOT SEEN» con la regione che cresce (5→54 m) e la barra della confidenza che scende sotto 0,9; la riacquisizione a t = 8,3 s del registro; volume dei detriti «never clear inside»; avviso al portatore «conservative · with the radar blinded it can be late»; ritmo ×0,27–0,63 dichiarato | SIMULATION + «radar blinded up to 2 s · pessimistic model» + «flash trigger optimistic» | F7-CAM, F7-VOL, F7-CONT, F7-LIBERO, F7-ID, F7R-CIECO, F7-LIM-FRONTALE |
| s9 | 139,1–150,9 (11,8 s, accorciata) | sito: drone dietro l'edificio, aereo in rullaggio, corto raggio, persona non vedente senza cifre | SIMULATION (site) · SCHEMATIC | LP-1, LP-4 |
| s10 | 150,9–173,9 | limiti; tre gradini «from prototype to deployed system», con la stima dell'hardware; titoli e crediti | SCHEMATIC · ESTIMATE | HW-CALC, C-TAR-VIRATA |

L'ordine è quello chiesto: F7 viene subito dopo il volo veloce principale e la curva (s3–s7), e subito prima del sito (s9).
La scena dell'hardware della bozza (s8, 16 s di barre con cifre fuori dal blocco) è tolta. Ne resta una riga di stima nel
secondo gradino di s10.

**Scelte su F7.**
- Ho usato `registro_F7r_davanti.jsonl`, non `registro_F7_*_v2.jsonl`. Nei registri `_v2` il radar non è accecato, e il
  bersaglio non viene mai perso (0 cicli non visti). Il registro F7r invece mostra la perdita, la confidenza che cala e la
  riacquisizione, che la consegna chiede.
- Il verdetto ammette F7r se il validatore dà 0 violazioni: le ho verificate rieseguendo `convalida_volo.py` su tutti
  i registri F7. Ho messo le righe obbligatorie.
- L'evento è mostrato senza istante e senza ritardo (F-806).

## 3. Difetti della bozza c

| Difetto | Esito |
|---|---|
| c1 velo ocra delle regioni enormi | corretto: velo solo sotto 260 px, tracce perse da > 10 s in grigio |
| c2 nota tagliata, C a segmenti, curva da rifare | corretto: curva tarata a passi di 0,5 s, nota su tre righe |
| c3 volume F4 che copre mezzo pannello | attenuato (velo 0,15); il volume resta grande perché il dato è grande |
| c4 etichette accavallate in F3 | attenuato (passo 36 px); non del tutto risolto |
| c5 «16 s in this run» contro V-5 | tolto: la console dice solo «PROXIMITY WARNING» |
| c6 «for three seconds» in F5 | tolto dalla voce e dal titolo |
| c7 audio mono, senza musica | corretto: stereo, tappeto sintetico, ambiente, silenzio di 1 s all'urto di F7 |
| c8 audio non ascoltato | **ancora non verificato**: misurato, non ascoltato |
| nuovo: accelerazione non dichiarata | corretto: «playback ×N (accelerated/slowed)» in ogni scena da registro |
| nuovo: etichetta coperta dal titolo d'apertura e assente nei crediti | corretto: è sempre visibile (misurato su 174 fotogrammi) |

## 4. Versione italiana

- Procedura: `video/consegna/genera_versione_italiana_v3.sh [draft|…|delivery] [etichetta]`. Fa la voce im_nicola, il
  rimontaggio sui tempi italiani, i sottotitoli italiani impressi e il mix. Alla fine rimette l'`index.html` inglese.
- **Prova draft (una volta, riuscita, 06:55):** `video/rendering/MoVi_pitch_IT_v3_draft.mp4`.
  - Durata 168,795 s, dentro il limite di 176 s. La voce im_nicola dura 152,8 s.
  - −14,0 LUFS e picco vero −2,1 dBTP.
  - Sottotitoli italiani impressi, visti su un fotogramma a 120 s.
  - Registro della corsa: `MoVi_pitch_IT_v3_draft.esecuzione.log`.
  - Le scritte dei pannelli restano in inglese.
- `MoVi_pitch_IT_v3.srt`: sottotitoli italiani sui tempi del video **inglese**, frase per frase. Le frasi sono 30 in
  entrambe le lingue, controllate dallo script.
- Il file `_impressi.srt` della procedura segue invece i tempi della versione italiana.

## 5. Materiali e licenze

| Materiale | Origine | Licenza |
|---|---|---|
| Voce EN e IT | Kokoro-82M ONNX, voci `bm_george` e `im_nicola`: sintetiche, nessuna persona reale | Apache-2.0 (STRUMENTI § 3.5) |
| Musica | `tappeto_180s.wav`, generato con numpy per questo video | opera propria |
| Ambiente | rumore marrone di ffmpeg | — |
| Caratteri | Inter 4.1, JetBrains Mono | SIL OFL 1.1 |
| GSAP | 3.15.0 | Standard no-charge license (non open source) |
| Marchi | MoVi, SDMs, dal progetto | del gruppo |

**Simulato o illustrativo, a schermo:**
- tutte le scene da registro (SIMULATION);
- in F7 il lampo e il fumo sono disegnati («flash and smoke: drawn for illustration»);
- la vista di s7 è uno schema («motion compressed»);
- le croci «+» sono la verità del simulatore, che MoVi non vede.

## 6. Che cosa manca e che cosa propongo

- **Non verificato:**
  - l'ascolto dell'audio, cioè pronuncia di «MoVi» e «SDMs», ducking e silenzio all'urto;
  - la leggibilità delle righe di 18 px sui piccoli schermi.
- `hyperframes lint` segnala 1 errore: ci sono più file html con `data-composition-id` nelle copie in `versioni/`. È lo
  stesso errore della bozza, e la resa è comunque completa.
- La voce EN di F7 dice «the tracked drone stayed inside its region» (F7-CONT, radar non accecato) mentre si vede il
  passaggio col radar accecato. La riga a schermo dice «360-degree radar, not blinded», e la frase seguente della voce è
  F7R-CIECO.
- Proposta: un ascolto umano dei 174 s; poi, se serve, la resa «delivery» della versione italiana con
  `genera_versione_italiana_v3.sh delivery finale`.
