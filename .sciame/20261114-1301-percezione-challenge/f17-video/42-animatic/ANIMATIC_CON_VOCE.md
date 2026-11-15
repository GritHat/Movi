# MoVi · animatic con voce (`sciame-videomaker`, f17-video/42-animatic)

Lavoro dalle 02:12:58 alle 02:28 del 2026-11-15 (`date -Is`). Ho letto per intero `PIANO_VIDEO.md`, `VOCE_GUIDA.md`,
`REVISIONE_VISIVA.md` e il codice di montaggio e di disegno (`monta_v6.py`, `rimonta.py`, `motore_v6.js`, le parti di
`componenti_v6.js` che toccavo). Di `STRUMENTI.md` ho letto solo §1.5, §1.6 e §4–5. Il verdetto non l'ho riletto: le
cifre vengono da `cifre.json`, così com'è.

**File da guardare:** `video/rendering/animatic_voce_v2.mp4` (la v1 è accanto).

## 0. In testa: cambi di stato e regole violate

- **Regola violata: «nessun dato di sviluppo nel montaggio».** Le scene 1, 4, 5 e 6 disegnano ancora i registri di
  sviluppo `dati_sviluppo/*.SVILUPPO.jsonl`. La scena 3 prende da R1, che è di sviluppo, la disposizione dei sensori.
  L'etichetta d'onestà stampa `SCHEMATIC · DEV DATA · NOT A RESULT` per tutta la scena.
  - `prototipo/uscite/video/` **non esiste** (verificato con `ls` alle 02:13).
  - I registri lunghi veri (`lp_A1`, `lp_E1…E3`) non hanno i campi degli eventi e girano a 2 righe al secondo. Collegarli
    non stava nei 45 minuti.
  - Per questo l'animatic **non è consegnabile come video finale**: `monta_v7/8.py --finale` lo rifiuta.
- **Previsioni, scritte alle 02:16 prima della resa** (non in un file: le riporto qui com'erano):
  1. durata 173,0 ± 0,1 s;
  2. −14 ± 1 LUFS, picco ≤ −1,0 dBTP;
  3. verde ≤ 8 pixel per fotogramma a 480×270.

  Esiti: la 1 regge (173,000 s); la 2 regge; la 3 regge (massimo 2 pixel di campione).
  Notato solo dopo: nella v1 loudnorm era passato in modalità **dinamica**; nella v2 è **lineare**.
- **Scritture.** Solo in `video/` e qui. Tutti file nuovi: `scene/scene_v7.json`, `assets/js/{componenti,motore}_v{7,8}.js`,
  `strumenti/{monta_v7,monta_v8,audio_v7,audio_v8,controlla_v7}.py`, `strumenti/{rendi_v7,rendi_v8,istantanee_v7}.sh`,
  `testi/schermo_{en,it}_v7_extra.json`, `sottotitoli/movi_{en,it}_v7.srt`, i file in `rendering/`.
  - Sono stati **riscritti dai generatori**, con la copia precedente in `progetto/versioni/`: `index.html`, `testi/testi.js`,
    `tempi/scene_tempi.js`, `assets/marchio/marchio.js`, `assets/data/{sottotitoli,R*}.js`. I `R*.js` non hanno copia: si
    rigenerano.
  - Effetto da sapere: **ora `index.html` monta la v8**. Chi rilancia `rendi_v6.sh` lo riscrive in v6.
  - Una sola sovrascrittura di un mio file: `componenti_v7.js`, che il mio primo innesto aveva rotto (resa 1 fallita:
    `CUE is not defined`). Prima l'ho ricopiato dalla v6; la copia rotta sta nella scratchpad.
  - Nessun file cancellato (resta anche la cartella vuota `rendering/audio_v1`). Niente git, niente sudo, niente rete.
- **Indipendenza.** Regista e controllore sono lo stesso ruolo, sullo stesso codice. Il controllo del verde e dei margini
  è un mio script. Nessun ascolto né visione umana.

## 1. Che cosa ho fatto

**Durate** (scene 1–9, in s): 12,5 · 21 · 16 · 21 · 22 · 20 · 36,5 · 10 · 14 = **173,0 s**. Sono quelle proposte da
`VOCE_GUIDA` §3, con due ritocchi: la scena 2 ha 1 s in meno, la scena 9 ne ha 0,5 in più per i titoli. La voce è quella
di `video/voce/voce_guida_en_v4.wav` (bm_george, 1.0), mai accelerata. Ogni paragrafo comincia a `inizio scena + voce_da`
(0,4 s; 0 nella scena 1; 0,6 nella scena 9).

**Cambi di stato agganciati alla parola.** Gli istanti della parola sono stimati in proporzione ai caratteri dentro la
frase misurata in `.tempi.json`. Errore atteso: ±0,3 s, non misurato.

| Scena | Parola | Stato a schermo | Come |
|---|---|---|---|
| 1 | «behind the hangar» (8,4 s) | D2 `NOT SEEN` (R1 t = 5,23) | R1 tenuto fermo fino a 3,17 s |
| 2 | «I see it», «I don't see it», «I don't know», «unverified», «never empty», «possible-presence» | i tre segni, `UNVERIFIED ZONE`, `EMPTY` barrato, `POSSIBLE PRESENCE` | a 4,3 · 5,7 · 8,6 · 12,4 · 13,2/13,9 · 14,7 s (`cue`) |
| 3 | elenco dei sensori, «blind spots» | glifi ogni 1,1 s da 0,4 s; archi a 10,6 s | `cue` |
| 4 | «reliability is lost» (14,71 s) | banda `RELIABILITY LOST · RADAR` (R3c t = 100) | R3c da 9,71 s, t_reg 95; nebbia 0–3,5 s, pioggia 3,5–9,71 s |
| 5 | «unresolved tracks» (4,4 s), «contact» (6,7 s) | `UNRESOLVED TRACKS` a 4,17 s, `EVENT: CONTACT · INFERRED` a 6,7 s | R1E t_reg 9,5; ×4 dopo 14 s |
| 6 | «with a flash» (3,4 s) | lampo, bande `RELIABILITY LOST · EO/IR` (R2E t = 15,7) | t_reg 12,3; camera ferma da 3,0 s |
| 7 | ogni limite detto | una riga a schermo per limite, a 2,1 · 5,7 · 10,7 · 13,3 · 16,7 · 20,7 s; a 23,06 s («What holds») i limiti si spengono ed entrano i risultati: A1, A4 e V2 a 23,6 · 26,6 · 31,9 s | `cue` |
| 9 | «MoVi», tagline, «It observes» | wordmark 0,6 s, tagline 1,8 s, perimetro 5,7 s, titoli di coda 8,6 s | `cue` |

**Musica e mix** (`strumenti/audio_v8.py`):
- tappeto sintetico del piano §8, a −14 dB con sidechain sulla voce;
- fruscio d'aria (rumore marrone, passa-basso 600 Hz, −26 dB);
- **1 s di silenzio** di musica e ambiente a 64,21 s e a 95,9 s, cioè all'ingresso di RELIABILITY LOST nelle scene 4 e 6,
  con rampe di 40 ms;
- nessun altro evento sonoro.

**Sottotitoli.**
- I `.srt` EN e IT stanno in `video/sottotitoli/movi_{en,it}_v7.srt`. Gli EN sono **impressi** nella pagina (Inter 600 da
  40 px, fascia bassa).
- **L'EN viene dal testo detto**: le frasi di `.tempi.json` coi loro tempi veri, a loro volta generate da `cifre.json`.
- **L'IT viene da `uscite/it_v5_1.0`.** Ogni frase italiana sta nella finestra della voce inglese della sua scena, in
  proporzione alla sua durata nella voce italiana. La sincronia è per paragrafo, non per parola.

**Cifre a schermo:** tutte da `cifre.json`.
- `righe_schermo` è ora applicato: `null` toglie la riga; una chiave la sostituisce col testo della cifra. Nella scena 7
  ci sono anche `@L-46` e `@L-VOLO`.
- Sono ammessi solo gli stati `sostenuto`, `verificato` e `limite`.
- Segnaposti rimasti in `testi.js`: **0**.

**Comandi** (da `video/progetto/`), con il nome di uscita nuovo a ogni resa:
1. `sh strumenti/rendi_v8.sh looks ../rendering/<x>_immagine.mp4 en`
2. `python3 -I strumenti/audio_v8.py ../rendering/<x>_immagine.mp4 ../rendering/<x>.mp4 ../rendering/audio_<x>`
3. `python3 -I strumenti/controlla_v7.py ../rendering/<x>.mp4`
4. `sh strumenti/istantanee_v7.sh ../rendering/<x>.mp4 ../rendering/controllo_<x>`

La resa dell'immagine prende 78 s.

## 2. Controlli (v2; la v1 dà gli stessi valori, salvo dove è detto)

| Controllo | Esito | Prova |
|---|---|---|
| Q1 durata | **173,000 s**, 5190 fotogrammi | ffprobe |
| Q19 formato | H.264 High, yuv420p, 1920×1080, 30/1; AAC LC 48 kHz stereo; 37,8 MB; faststart | ffprobe; il video è copiato dalla resa `looks` (CRF 16), una sola codifica |
| Q18 loudness | **I = −14,0 LUFS**, LRA 3,0 LU, **picco vero −2,3 dBTP**, loudnorm `linear` | `rendering/audio_v2/ebur128_finale.txt`, `loudnorm_passata2.json`. v1: −14,0 LUFS e −1,5 dBTP, ma `dynamic` |
| Q11 verde | 173 fotogrammi (1/s): al massimo **2 pixel** di campione a 960×540, area connessa massima 1 (circa 4 px a 1080p, soglia 50); 10 fotogrammi con almeno un pixel. Pixel isolati nelle scene 5–6, dove il ciano tocca l'ocra | `rendering/controllo_voce_v2_q11_q21.txt` |
| Q21 margini | Nessun testo tagliato dal bordo. Pixel chiari nella cornice di 16 px: sono il riquadro dell'etichetta d'onestà a y = 12 e la parte alta dei titoli di scena. Stanno dentro la «fascia alta 0–124» del piano, ma **fuori dal margine di 54 px**. Già noti, non toccati: `EO · NOT COUNTED` sotto i sottotitoli (scena 6) e `out of sensor view` tagliato nel riquadro della verità | `controllo_voce_v2/margini/striscia.png` |
| Q9 termini vietati | 0 occorrenze nei `.srt` EN e IT e in `testi.js` | `grep -inw` |
| Q20 sottotitoli | 50 cue in EN, 51 in IT; nessuna riga oltre i 42 caratteri; il testo EN è identico a quello detto. Scarto ≤ 200 ms: **non misurato** | awk |
| Q13 etichetta d'onestà | presente in tutte le 20 istantanee guardate | `controllo_voce_v2/foglio.png` |
| Istantanee | 20, una o più per scena, ai momenti chiave; guardate tutte, sul foglio a 640 px | `rendering/controllo_voce_v{1,2}/` |

**Non verificati:**
- il silenzio di 1 s: è costruito nel filtro, ma non l'ho misurato sul mix, dove la voce copre;
- l'ascolto, cioè sincronia e mix «a orecchio»;
- Q3 per scena;
- la resa in italiano;
- la leggibilità a 1080p con un estraneo.

## 3. Registri usati per ogni scena

| Scena | Registro | Vero? |
|---|---|---|
| 1 | R1 = `dati_sviluppo/R1.SVILUPPO.jsonl` | **no**: sviluppo |
| 2, 7, 9 | nessuno: schema e titoli | — |
| 3 | intestazione di R1 (sviluppo) | **no** |
| 4 | R3a, R3b, R3c (sviluppo) | **no** |
| 5 | R1E (sviluppo) | **no** |
| 6 | R2E (sviluppo) | **no** |
| 8 | Rc = `prototipo/uscite/resta_dietro/registro.jsonl` (corto raggio, 15 righe/s, etichetta `PROVISIONAL REGISTER`) | **sì**, l'unico |

Nessun registro di `prototipo/uscite/lunga` o `lp_*` è montato.

## 4. Revisione del regista sulla v1, in ordine d'importanza

1. **Onestà e dati.** Le scene 1 e 4–6 mostrano dati di sviluppo. Le scene 5 e 6 mostravano
   `WARNING TO OPERATOR · PERSON IN FOOTPRINT / UNVERIFIED ZONE ON VEHICLE PATH`, che il verdetto non sostiene (E2-X: 0 su
   32). → **v2: quegli avvisi tolti; a schermo E1-X (scena 5, a 12,9 s, con «Our weak point») ed E2-X (scena 6, a 15 s),
   presi da `cifre.json`.** Restano i registri di sviluppo: si risolve solo con `prototipo/uscite/video/`.
2. **Scena 7: un numero falso sullo schermo.** I contatori «contavano» da 0, e l'istantanea mostrava `0 of 590 simulated
   passes`, mentre la voce diceva «six hundred». → **v2: niente conteggio; la cifra compare intera.** Ho anche tolto la
   sovrapposizione: le righe dei limiti si spengono quando entrano i risultati.
3. **Banda `RELIABILITY LOST` sotto i sottotitoli** (scena 4, il momento chiave): la parola si leggeva a metà. → **v2: la
   banda di sistema sta in alto nella vista**, e il fondo dei sottotitoli è più coprente (0,93).
4. **Mix in modalità dinamica** nella v1. → **v2:** guadagno fisso e limitatore prima di loudnorm, che ora è lineare.
5. **Non corretto: densità.**
   - Le scene 5 (×4) e 6 hanno troppe etichette sovrapposte dentro le trame ocra, e il contatto non si «vede» al primo colpo.
   - La scena 7 supera le 16 parole per schermata (6 righe di limiti).
   - Proposta: una riga di console per evento; nella scena 7 al più 3 limiti per schermata.
6. **Non corretto: ritmo.**
   - Scena 1: R1 resta fermo per 3,17 s, mentre il titolo è sullo schermo.
   - Scena 4: la pioggia arriva 3 s dopo che la voce l'ha nominata (la voce dice «Fog, then heavy rain» in 2 s).
   - Scena 6: le bande arrivano con «flash», 4 s prima di «marks them unreliable»; la parola che cita lo stato è in ritardo
     sull'immagine.
   - Proposta: spezzare la frase 1 della scena 4 o riscrivere il registro E3 con la pioggia più corta.
7. **Non corretto: leggibilità.**
   - Il riquadro della verità (468×300) è troppo piccolo per capire la scena 1, che deve agganciare chi guarda.
   - I testi da 22 px nel riquadro e nelle righe di dominio non si leggono su un telefono.
8. **Non corretto: la chiusura.** Le 5 righe dei titoli entrano 5,4 s prima del nero, ma con voce sopra: il tempo di
   lettura dei nomi non è verificato.

## 5. Stati proposti

| Enunciato | Stato |
|---|---|
| La durata dell'animatic con voce è in 165–175 s | **Verificato** (ffprobe: 173,000 s) |
| Loudness −14 LUFS e picco ≤ −1 dBTP | **Verificato** sul file v2 (ebur128) |
| Nessun verde oltre la soglia | **Verificato** su 173 fotogrammi, uno al secondo (non su tutti) |
| I cambi di stato cadono sulla parola che li cita | **Sostenuto dai dati** sui tempi delle frasi; posizione della parola stimata, errore non misurato |
| L'animatic usa registri veri | **Smentito** per le scene 1 e 3–6; vero solo per la scena 8 |
| I sottotitoli IT sono sincroni | **Non risolto**: lo sono per paragrafo; per frase lo deciderebbe un controllo visivo con un lettore italiano |

## 6. Che cosa propongo dopo

1. All'arrivo di `prototipo/uscite/video/INDICE.md`: si aggiungono i registri a `scene_v7.json`, con il loro stato, e si
   ricalcolano `t_reg` e `da` con la regola del §1, cioè lo stato del registro sulla parola.
2. Un ascolto e una visione umani della v2, di 5 minuti, sulle scene 4, 5 e 6.
3. I punti 5–7 del §4, in una v3.
4. La resa italiana, con `rendi_v8.sh … it` e la voce `it`.
