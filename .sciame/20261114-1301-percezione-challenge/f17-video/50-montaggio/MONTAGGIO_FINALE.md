# MoVi · montaggio finale (`sciame-videomaker`, f17-video/50-montaggio)

Dalle 03:45:03 alle 04:11 del 2026-11-15 (`date -Is`). Previsioni scritte prima delle prove in `PREVISIONI.md` (qui).

**File da guardare:** `video/consegna/MoVi_pitch_EN_v1.mp4` (172,77 s). Accanto, in `video/consegna/`:
- i sottotitoli `MoVi_pitch_EN_v1.srt` e `MoVi_pitch_IT_v1.srt`;
- `MoVi_copione_v1.md` e `MoVi_registro_cifre_v1.md`;
- la procedura italiana `genera_versione_italiana.sh` e la sua prova in bozza, `MoVi_pitch_IT_v1_draft.mp4`.

## 0. In testa: cambi di stato e regole

- **D1, la fase nascosta: va «Schematic».** Il primo passaggio A1 «alta» con una fase nascosta, in ordine di seme, nella
  riprova 2c è il **n. 8** (`riprova_passaggi_v3.jsonl`: nasc_tot 10, fuori_avviso 0).
  - Il suo registro non esisteva. L'ho generato con il prototipo: copia di `lp_A1_v3.json` con passaggio 8 e nucleo v3,
    mappa dichiarata. Uscita in `a1_n8/uscita/`.
  - Convalida: **0 errori**.
  - **Validatore della controprova: NON a 0.** `libero_per_classi_con_griglia_non_affidabile: 44`
    (`a1_n8/uscita/valida_video_controprova.txt`). Dal fotogramma di 37,5 s a quello di 59,0 s, il radar a griglia è
    «persa» (controllo di salute) mentre il registro dichiara ancora «libero per classi» con celle libere (da 26 a 6). Il
    drone è nascosto da 54,5 s.
  - Per questo il momento «drone dietro l'edificio» è **Schematic** (scena 2, «drone behind a building: schematic, not a
    run»). La scena 1 usa `lp_A1_v3` (n. 90) per la tempestività.
  - **Da dare al coordinatore.** È un difetto nuovo, nel nucleo v3 o nel registro. Lo 0/171 non lo smentisce, perché è
    contato su un'altra misura (`libero_viol`). Previsione 1: **smentita** sul validatore.
- **Previsioni 2–4.**
  - 2 regge: voce EN di 151,7 s nella prima resa e di 155,0 s nell'ultima; video di 172,77 s.
  - 3 è **smentita**: l'italiano entra nei tempi inglesi in tutte e 9 le scene.
  - 4 regge: −14,0 LUFS; verde con un'area connessa massima di 2 px di campione; 0 «DEV DATA».
- **Correzione della voce fatta dopo aver guardato.** La frase «In the model, the radar alone still sees the aircraft»
  era smentita dal registro `lp_E2_v3`. Dopo la fiammata, la traccia dell'aereo è «non vista» fino a 9,5 s, a tratti. Ora
  la frase dice «Only the radar is left: in this run it loses the aircraft for seconds at a time, and MoVi says so» (e
  così in italiano).
- **Scritture.** Solo in `video/` e in questa cartella. Niente git, niente sudo, niente rete. Nessun file cancellato.
  - Due sovrascritture, con la copia accanto:
    1. `cifre.json`, la cui v7 è in `progetto/versioni/cifre.20261115-v7-prima-del-2c.json`;
    2. i due modelli `voce_{en,it}_v4.modello.txt`, che sono miei e di oggi: li ho corretti per la frase del radar.
  - I generatori riscrivono `index.html` (copiato in `versioni/`), `testi.js`, `scene_tempi.js` e `assets/data/sottotitoli.js`.
  - Ho fermato con `pkill` una resa EN a metà, per correggere il riquadro della camera. Non ha lasciato file video. Il
    suo log, `rendering/MoVi_pitch_EN_v1.log`, resta.
  - **Il progetto resta nello stato dell'ultima resa (EN).** Dopo la procedura italiana, `index.html` monta l'italiano.
- **Indipendenza.** Regista e controllore sono lo stesso ruolo, sullo stesso codice. Il controllo del verde e dei
  margini è uno script mio della v7. Nessuna visione né ascolto umani.

## 1. Che cosa ho fatto

1. **Cifre.** `cifre.json` v8 viene dal VERDETTO_2C: 15 cifre attive, 14 marcate «superata dal 2c».
   - Tolte: E1-X (1/16), E2-X (0/32), STATO-1 («event rules not yet in the prototype»: falso col v3), CIFRA-V2 (0/600) e
     A7.
   - Nuove: A1-CONF, E3-PORTATA, E1-RIT, E1-ZONA, E2-C, E2-AVV, L-FERMA, L-MAPPA, V-SPEGNE e C0. A1 e A4 sono nella
     forma del 2c.
   - «Free» non compare mai. Il lessico è quello di `voce_util.py`, che li vieta.
2. **Registri veri.** `strumenti/registri_a_js_v9.py` è un adattatore che rinomina i campi senza inventare valori. Le
   regole sono elencate nel file e in ogni `.js`.
   - **Simulation:** scena 1 `lp_A1_v3`, scena 4 `lp_E3_v3`, scena 5 `lp_E1_v3`, scena 6 `lp_E2_v3`, scena 8
     `resta_dietro` (corto raggio, «provisional register»).
   - **Schematic:** scene 2, 3, 7 e 9.
   - Nella scena 5 la zona dei detriti porta «DEBRIS ZONE · SCHEMATIC». Nella scena 6 detriti e avviso al mezzo portano
     «DEBRIS AND VEHICLE WARNING · SCHEMATIC».
   - `lp_A1_ingenua_v3` non è usato.
3. **Voce.** Kokoro bm_george 1.0, `voce/uscite/en_v6_finale/` (`genera_voce_v2.sh`, copia di `genera_voce.sh` sui
   modelli v4).
   - Durata 155,0 s; 350 parole EN e 343 IT, oltre il Q2 del piano (≤ 340).
   - I tempi sono rimontati da `costruisci_scene_v9.py`: ogni stato del registro cade sulla frase che lo cita. L'evento
     «contact» arriva a 0,6 s dall'inizio di «MoVi infers contact». Le camere sono non affidabili 0,3 s prima della fine di
     «…with a flash».
   - Durate delle scene: 13,5 · 23,5 · 14 · 18,5 · 20,5 · 23,81 · 35,5 · 10 · 13,56 = **172,87 s**.
4. **Etichette e colpo d'occhio.** In basso c'è una sola riga di cifre alla volta, sopra i sottotitoli. In alto a destra
   c'è una colonna fissa per le scritte schematiche e per i raggi letti dal registro. Il dominio sta in alto a sinistra.
   - Fiammata: lampo che satura la camera, con «EO CAMERA · SCHEMATIC IMAGE» e «SATURATED», e la banda «RELIABILITY
     LOST» in quel fotogramma (16,0 s del registro). Il glifo del radar non è barrato.
   - Detriti: il volume a righe cresce (raggio dal registro, da 318 a 1943 m), con i contorni di 2, 4 e 6 s prima.
     L'impronta è a puntini, «UNVERIFIED».
   - Nebbia: due cerchi, la portata nominale e quella dichiarata.
   - Collisione: etichette solo sulle tracce 1, 2 e 4. I frammenti sono punti.
   - I limiti stanno al più 3 per schermata.
5. **Mix** (`audio_v9.py`): tappeto sintetico a −14 dB con sidechain e fruscio a −26 dB. Nessun suono legato agli
   stati. Silenzio di 1 s a 93,64 s, all'ingresso di «RELIABILITY LOST · EO/IR».
6. **Esportazione:** resa `delivery`, poi una codifica libx264 High CRF 18 yuv420p, AAC 320k e faststart.
7. **Italiano:** `sh video/consegna/genera_versione_italiana.sh [delivery|draft]`. Fa la voce im_nicola, rimonta (ogni
   scena dura almeno quanto in EN), imprime i sottotitoli IT e usa lo stesso mix.
   - Provata una volta in `draft`: 172,77 s, −14,0 LUFS, picco −2,1 dBTP.
   - **Nessuna scena sfora**: la voce IT è più corta della EN in 8 scene su 9. Nessun taglio necessario.

## 2. Controlli sul file EN

| Controllo | Esito | Prova |
|---|---|---|
| Durata | **172,77 s** (immagine 172,90 s; `-shortest` taglia all'audio) | ffprobe |
| Formato | H.264 **High**, yuv420p, 1920×1080, 30/1; AAC LC 48 kHz stereo, 320k richiesti (media misurata 287 kbps); `moov` prima di `mdat` | ffprobe, lettura dei byte |
| Loudness | **I = −14,0 LUFS**, LRA 3,8, **picco vero −2,3 dBTP**, loudnorm lineare | `rendering/audio_MoVi_pitch_EN_v1/ebur128_finale.txt` |
| Verde | 173 fotogrammi: al massimo 8 px di campione, area connessa massima 2 (circa 8 px a 1080p, soglia 50) | `rendering/controllo_MoVi_pitch_EN_v1_q11_q21.txt` |
| Margini | pixel chiari nella cornice di 16 px (vedi sotto) | stesso file |
| «DEV DATA» | 0 nei 12 sorgenti caricati da `index.html`; 0 «SVILUPPO» nei dati; `monta_v9 --finale` è passato | grep |
| Termini vietati | 0 nei due `.srt` | grep |
| Istantanee | 22 su tutte e 9 le scene, guardate sul foglio; 6 a piena risoluzione nella bozza | `rendering/controllo_MoVi_pitch_EN_v1/foglio.png` |

Dettagli sui margini:
- In 159 fotogrammi la cornice ha pixel chiari: l'etichetta d'onestà a y = 12, una cosa già nota.
- Nella scena 8, «out of sensor view» resta tagliato al bordo destro (1019 px): non l'ho corretto.

**Non verificati:**
- il silenzio di 1 s, costruito nel filtro ma non misurato, perché la voce lo copre;
- l'ascolto;
- la sincronia dei sottotitoli IT nel video EN, che è per paragrafo;
- la leggibilità sul telefono.

**Restano piccole sovrapposizioni** fra le etichette delle tracce e il volume (scene 5–6) e fra la colonna di destra e
l'etichetta «SEEN» (scena 6). Nella scena 4 l'etichetta «1062 m» è tagliata a destra.

## 3. Stati proposti

| Enunciato | Stato |
|---|---|
| Il video EN sta in 165–175 s ed è a −14 LUFS | **Verificato** (ffprobe, ebur128) |
| Nessun dato di sviluppo nel finale | **Verificato** sui sorgenti caricati e sui registri |
| Il registro A1 n. 8 passa la controprova | **Smentito** (44 fotogrammi) |
| L'italiano sta nei tempi inglesi | **Sostenuto dai dati** (una prova draft) |

## 4. Che cosa propongo dopo

1. Al coordinatore: esaminare A1 n. 8 («libero» con il radar a griglia «persa»). La prova che lo decide è
   `valida_video.py` su tutti i 22 passaggi con una fase nascosta.
2. Una visione e un ascolto umani delle scene 5 e 6, e la scelta della pronuncia di «MoVi».
3. `sh video/consegna/genera_versione_italiana.sh delivery` per l'italiano definitivo.
