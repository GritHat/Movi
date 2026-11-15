# Controllo qualità del video v3 (f17-video/72-qa-v3, `sciame-validazione`)

Dalle 06:56:13 alle 07:01 circa del 15-11-2026 (`date -Is`). Oggetto: `video/consegna/MoVi_pitch_EN_v3.mp4`
(sha256 `ac892dbe…82629ab`), `MoVi_pitch_EN_v3.srt` (sha256 `bfce40d7…e1ff48`), `MoVi_registro_cifre_v3.md`,
`CONSEGNA_V3.md`. Il riferimento è `f20-chiusura/20-verdetto/VERDETTO_FINALE.md`. Tutto ciò che il video mostra è
simulato, calcolato, o su traiettorie pubbliche con un sensore simulato: nessun sensore fisico e nessuna prova su hardware.

## 0. In testa: esito, regole, indipendenza

- **Esito: nessun difetto BLOCCANTE.** La durata è 173,856 s (ffprobe, formato; video 173,833 s), sotto i 176,0 s
  con 2,14 s di margine. Ci sono due difetti medi e alcuni bassi (§ 2). Le correzioni proposte non allungano il video,
  oppure lo allungano al più di circa 1 s, e quindi restano sotto i 176,0 s: dopo ogni rifacimento la durata va
  rimisurata.
- **Regola violata (n. 3).** Prima delle misure non ho scritto previsioni con soglia. Le soglie che ho usato sono quelle
  della consegna (176,0 s; verde 0; etichetta sempre presente), fissate da altri prima di me: va dichiarato.
- Non ho cancellato né sovrascritto nulla. Ho scritto solo in `72-qa-v3/`. Niente git, niente sudo, niente rete.
- **Indipendenza.** Con l'autore del video condivido il verdetto, i registri e il modello linguistico. Le mie misure
  sono rifatte da zero sul file finale: ffprobe, ebur128, estrazione dei fotogrammi, OCR con tesseract e un mio
  criterio del verde. In questo modo i difetti di montaggio, di trascrizione e di etichetta sono coperti. Non sono
  coperti invece gli errori già presenti nei registri o nel verdetto.

## 1. Misure (comandi e file in questa cartella)

| Voce | Misura | Esito |
|---|---|---|
| Durata | 173,856 s (formato), audio 173,856, video 173,833 | **regge** (≤ 176,0) |
| Formato | H.264 High, yuv420p, 1920×1080, 30 fps, 5215 quadri, bt709; AAC LC 48 kHz stereo; `moov` a 0x24 (faststart) | regge. L'audio misura 286 kb/s e non i «320» dichiarati: è una nota sul documento, non un difetto |
| Loudness | −14,0 LUFS I, LRA 2,9 LU, picco vero −2,3 dBTP | regge (coincide con CONSEGNA) |
| Etichetta d'onestà | presente in 87/87 fotogrammi campionati ogni 2 s, Wilson [0,958; 1]. La riga «Simulated · … · no physical sensor» compare in tutti i fotogrammi SIMULATION (s1, s3–s6, s8, s9) | regge sul campione, non su ogni quadro |
| Verde | 1/87 fotogrammi (f_033, a circa 65 s): 24 pixel nella vista di quota, dove il ciano e l'ocra si sovrappongono con l'antialias (`verde.py`). Non c'è nessun elemento verde | regge: è un falso positivo del criterio |
| Frasi vietate | .srt EN e IT, OCR di 87 fotogrammi, `index.html`: 0 occorrenze di validated, guaranteed, detect and avoid, threat, target, counter-drone, always, real time, sub-millisecond, intercept, pursue, certif, «16 aircraft», «99 %», EVENT: COLLISION. I «never» sono tutti condizionati (scenari simulati, «with the declared map», «inside the debris volume») | regge |
| Sottotitoli | EN e IT: 30 cue ciascuno, indici e tempi monotoni, nessuna sovrapposizione, ≤ 21 caratteri/s, ultima cue a 170,1 s (`srt_check.py`). Sottotitoli impressi confrontati con l'.srt ai bordi delle cue (26,4/26,9; 110,0/110,5; 122,3/122,8 s): scarto < 0,3 s | regge per impressi ↔ .srt; la voce ↔ .srt **non verificata** (non ascoltata) |
| Licenze nei crediti | Kokoro-82M Apache-2.0, musica propria, Inter e JetBrains Mono OFL | GSAP non è nei crediti a schermo (D5) |

**Cifre a schermo ↔ verdetto, riga per riga** (OCR, `ocr/`). Tutte coincidono con il § 2 e con il blocco JSON del § 8:
- V-1: F6 0/200 [0; 0,019], altre 0/60 [0; 0,060];
- V-2: 60/60 [0,940; 1], «optimistic trigger»;
- V-3: 58/60 [0,886; 0,991];
- V-5: 60/60 [0,940; 1], «10 s threshold set after»;
- V-6: 60/60, 939/939;
- V-10: 60/60, «identity PRESUMED»;
- V-11-PROVA: 57/60 [0,863; 0,983], 2/60 [0,009; 0,114], «not adopted»;
- C-TAR: 0,89 (655/733) [0,87; 0,91], 0,85–0,89, 21–30 s 0,85 [0,81; 0,88], 89,5 % da 4 voli, virata 0,73 (161/221) [0,67; 0,78] L, «cases correlated»;
- F7-CAM: 0/200 [0; 0,019] «without clustered clutter»;
- F7-VOL: 60/60 [0,940; 1] «in the model»;
- F7-CONT: 60/60 ×4 «360-degree radar, not blinded»;
- F7-LIBERO e F7-ID: 0/60 [0; 0,060];
- F7-LIM-FRONTALE: 1/60, 0/60, 43/60 [0,592; 0,815];
- F7R-CIECO: 0/60, 59–60/60, peggiore 59/60 [0,911; 0,997];
- LP-1 e LP-4: 200/200 [0,981; 1];
- HW-CALC: 0,08–1,2 ms «estimate by analogy, not a measurement».

Il limite LP-6 è a schermo. Le cifre tolte (V-4, «16 aircraft», 92–98, latenze in barre) non compaiono.

**Fedeltà ai registri** (letture `t`, «NOT SEEN x s · region r m» dell'OCR contro il jsonl allo stesso `t`):
- **F3:** t = 3,1, 21,3 e 24,5 s;
- **F1:** 54,3 s;
- **F4:** 37,6, 40,3, 43,0, 45,7 e 51,1 s;
- **F5:** 40,0, 41,8 e 45,3 s;
- **F7r davanti:** 6,5, 7,0, 7,6, 8,1 e 8,7 s.

Tutte coincidono entro l'arrotondamento. In F7 la «region» a schermo è `insieme_presenza_r_m` (25 → 49 → 87 → 126 m);
anche lo stato dei sensori coincide («radar restored (declared)» da t = 7,6 s, camera satura fino a 8,5 s). Il confronto
è un campione di 18 letture: non è un controllo di ogni fotogramma ogni 2 s, perché l'OCR non legge tutte le scritte
sulle regioni.

## 2. Difetti, in ordine di gravità, con la correzione

1. **Medio: in F7 compaiono le croci «+» della verità senza la loro legenda** (s8, 108,7–139,1 s, 30 s).
   - **Prova:** OCR «truth» 0/15 nei fotogrammi di s8 contro 1 in ogni fotogramma di s3–s6; in f_062 si vede la «+»
     sul drone NON visto.
   - **Rischio:** uno spettatore può leggere la croce come una posizione osservata mentre la scritta dice «NOT SEEN».
   - **Correzione:** aggiungere nel piè del pannello di s8 la riga di s3–s6, «+ truth (simulation only, MoVi does not
     see it)», oppure togliere le croci. La durata non cambia.
2. **Medio: la voce e il .srt della cue 23 dicono «In sixty of sixty simulated runs, the tracked drone stayed inside its
   region» mentre a schermo scorre il passaggio F7r col radar accecato.**
   - Il 60/60 vale per il radar non accecato (S-1); col radar accecato il peggiore è 59/60 (S-6r).
   - La riga a schermo dice «not blinded», ma l'orecchio non la vede. CONSEGNA § 6 lo segnala già.
   - **Correzione:** «With the radar undisturbed, in sixty of sixty…» (+3 parole, circa 1 s, totale stimato 174,9 s:
     da rimisurare, mai oltre 176,0). In alternativa, a durata invariata: «In sixty of sixty simulated runs with an
     undisturbed radar…» al posto di «…, the tracked drone…».
3. **Basso: la cue 9 dice «An engine fails at a hundred and thirty-five metres per second».** Il verdetto (V-2) e lo
   scenario F4 dicono «in-flight failure of an aircraft»: «engine» non è nel blocco.
   - **Correzione:** «An aircraft fails in flight at a hundred and thirty-five metres per second» (stessa lunghezza
     circa).
4. **Basso: s1 è etichettata SIMULATION e mostra le letture del registro F3**, mentre il § 8 del verdetto dice
   «Schematic, nessuna cifra».
   - La deviazione è dichiarata in CONSEGNA ed è più prudente (l'etichetta corrisponde ai dati).
   - **Correzione:** nessuna sul video; basta annotare la deviazione nel registro delle cifre, § 2.
5. **Basso: GSAP (licenza «Standard no-charge», non open source) non compare nei crediti a schermo.** È elencato solo
   in CONSEGNA § 5.
   - Se la licenza chieda l'attribuzione è **non verificato**.
   - **Correzione:** aggiungere «animation: GSAP 3.15 (standard license)» alla riga dei crediti, a durata invariata.
6. **Basso: la riga V-11-PROVA in s5 omette «within 2 s · scanning radar» e «1/60 before impact».** È conforme al
   modello del § 8, ma più povera della frase del § 2.1.
   - **Correzione facoltativa:** «contact rule under test: within 2 s in 57/60 [0.863; 0.983] (scanning radar) · 2/60
     false events · not adopted».
7. **Documentale.**
   - CONSEGNA § 2, s8, dice «regione che cresce (5→54 m)»: è r0,9 del registro, mentre lo schermo mostra l'insieme di
     presenza (25→126 m). Va corretto il testo, non il video.
   - CONSEGNA dice audio a 320 kb/s; la misura è 286 kb/s.
8. **Da sorvegliare (non è un difetto rispetto al verdetto finale).**
   - Esistono i registri `registro_F7r_c1_*.jsonl`, e il commit a6391ff dichiara «avviso al portatore da 0/59 a 59/59».
     Il verdetto finale non li considera (§ 2, F-809).
   - Se l'arbitro adotta c1, diventano superate due righe: in s8 «with the radar blinded it can be late», e in s10
     «radar blinded: debris warning to the carrier not reliable». Non ho letto c1: **non verificato**.
9. **Da sorvegliare.** In s8 la scritta «EVENT: nearby collision · inferred» compare a t = 7,6 s del registro, 1,6 s
   dopo l'inizio della saturazione (6,0 s).
   - Il ritardo non è detto a voce né scritto come cifra, quindi F-806 è rispettato.
   - Il lettore attento lo ricava però dal contatore `t`.
   - Non ho verificato l'istante vero dell'urto nel registro.

## 3. Stati proposti

- Durata ≤ 176,0 s: **verificato** su questo file (sha256 sopra). Va rimisurata dopo ogni correzione.
- Cifre a schermo ↔ verdetto: **verificato** sulle righe lette dall'OCR (insieme dichiarato: 87 fotogrammi).
- Fedeltà ai registri: **sostenuto dai dati**, 18/18 letture, Wilson [0,824; 1]: è un campione, non esaustivo.
- Etichette ed assenza di verde: **sostenuto dai dati** su 87 fotogrammi (insieme alle 174 di CONSEGNA).
- Assenza di frasi vietate: **verificato** su .srt EN/IT e `index.html`; sull'OCR lo stato è sostenuto dai dati.
- Audio (pronuncia, ducking, silenzio all'urto) e sincronia voce ↔ sottotitoli: **non verificato**.

## 4. Che cosa propongo dopo

1. Correggere D1 e D2 (e, se si rifà, anche D3 e D5) in una resa nuova `MoVi_pitch_EN_v3b.mp4` accanto alla v3; poi
   ffprobe: la durata deve restare ≤ 176,0 s.
2. Un ascolto umano dei 174 s.
3. Decidere su c1 (D8) prima di aggiornare le righe di s8 e s10.

Mancano, per il tempo: la lettura di ogni fotogramma di s8 contro tutti i campi del registro (detriti, volume, barra
della confidenza), il controllo del video IT draft e l'OCR delle scritte dentro le regioni.

File: `fotogrammi/` (87 PNG), `ocr/`, `sync/`, `verde.py`, `srt_check.py`.
