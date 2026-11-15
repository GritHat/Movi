# Controllo qualità del video v3c (f17-video/81-qa, `sciame-validazione`)

Lavoro dalle 07:36 alle 07:46 del 15-11-2026 (`date -Is`). Non ho prodotto io il video. Tutto è simulato: nessun
sensore fisico. MoVi osserva e avvisa.

## 0. In testa

- **Nessun difetto bloccante.**
  - EN `MoVi_pitch_EN_v3c.mp4`: **174,379 s** (ffprobe, formato). IT `MoVi_pitch_IT_v3c.mp4`: **170,469 s**. Sono tutte
    e due ≤ 176,0 s e dentro l'obiettivo 170–175 s.
  - Sha256: EN 212cffe058c1714a…, IT f0c4ab5aecc82345…. Sono gli stessi file di INTEGRAZIONE.md.
- **Due difetti medi da correggere prima della consegna.** Si correggono a tempo zero con la stessa riga (§ 1, D1–D2).
- **Regole.**
  - Le previsioni sono in `previsioni.txt`, scritte alle 07:36, prima delle misure.
  - Non ho cancellato né sovrascritto nessun file, e ho scritto solo in questa cartella.
  - Niente git e niente rete.
  - Una violazione minore: ho riscritto in loco il mio `controlla.py`, perché nel python di sistema mancava numpy.
- **Indipendenza.**
  - Condivido con l'autore i rapporti c1 e il verdetto, che sono le fonti delle cifre.
  - Non condivido il codice di controllo: ho estratto i fotogrammi, misurato il verde e fatto l'OCR e la validazione
    dei .srt con strumenti miei. Ho confrontato lo schermo con il registro F7r c1 riga per riga.
  - Non copro gli errori del simulatore né quelli dei rapporti c1.

## 1. Difetti, in ordine di gravità

| # | Gravità | Dove | Difetto e prova | Correzione |
|---|---|---|---|---|
| D1 | **media** | s10 «Limits», EN 152–167 s, IT 148–163 s | Il limite dice «radar blinded: debris warning to the carrier not reliable». È la riga di **prima di c1** (`cifre_v3c.json`, riga 170, `LIMITI[4]`). Contraddice la scena F7 mostrata 15 s prima (59/59 con la correzione). Non coincide neppure con il documento tecnico e la proposta, che dicono «con la correzione c1 59/59 [0,939; 1], ma non localizzato e con 11/200 [0,031; 0,096] falsi avvisi» (`allegato.txt`, righe 534 e 4040; `proposta.txt`, riga 150) | Tempo zero, in una v3d accanto alla v3c: «radar blinded: carrier warning only with a fix under test · not localised · 11/200 false warnings». In IT la grafica è la stessa (inglese) |
| D2 | **media** | F7, limiti c1 | I limiti chiesti dall'addendum 19 restano a schermo troppo poco: «11/200» compare solo a 136–138 s EN (circa 4 s), «565 m» a 134–138 s, «49/60» a 130–138 s (OCR, 1 fotogramma ogni 2 s). La voce dice un solo limite: «the warning does not say where». Il falso avviso (11/200) non è detto in voce e a schermo si legge appena | La riga di D1 lo ripete nei limiti per circa 15 s, a tempo zero. In più, a tempo zero: far comparire le tre righe di limite insieme a «59/59», da 124 s, invece che a scalare |
| D3 | bassa | Voce F7, 124–134 s | La frase permessa (VERIFICA.md, «Frasi per la giuria») comincia con «In simulation» e dice «same seeds». La voce non dice né l'uno né l'altro: «MoVi warns the carrier at once … in fifty-nine of fifty-nine runs, against none without it». L'etichetta SIMULATION e la riga «same seeds · sim.» lo coprono a schermo | Facoltativa: «In simulation, with a fix under test, …». Sono +2 parole, circa +0,6 s, cioè ~175,0 s: resta ≤ 176,0 s, ma è al bordo dell'obiettivo. Se si fa, rimisurare con ffprobe |
| D4 | bassa | F7, EN 126–139 s | «TRACKED DRONE · SEEN · identity presumed, doubtful» copre «CARRIER · MoVi on board» (f068, f070). Il punto del drone seguito è tagliato dal bordo destro del pannello in pianta e in quota, a circa 500 px dalla sua etichetta. È il difetto noto 1 di INTEGRAZIONE | Etichetta ancorata sopra il punto e zoom che tenga il punto dentro il pannello |
| D5 | bassa | s1 (6 s) e F3 (62 s) | La correzione 9 del giurato è fatta solo in parte. A 6 s due etichette «NOT SEEN · region 63/60 m» sono lontane dalle loro regioni. A 62 s ci sono due etichette «SEEN» per ogni punto, e un anello ocra senza etichetta (`fot_en/f004.png`, `f032.png`) | Anticollisione delle etichette con un filo verso l'oggetto. Una sola etichetta per traccia |
| D6 | bassa | Versione IT | La grafica, i titoli e le cifre a schermo sono in inglese: in italiano ci sono solo la voce e i sottotitoli impressi. Le cifre coincidono | Dichiararlo nella consegna («grafica in inglese») oppure accettarlo |
| D7 | bassa | `.srt` | Sui tempi EN, `MoVi_pitch_IT_v3c.srt` arriva a 18,5 caratteri/s, oltre i circa 17 consigliati. `MoVi_pitch_IT_v3c_impressi.srt` ha 20 sovrapposizioni di 0,2 s (difetto già noto). Non ho verificato se i sottotitoli impressi nel video IT vengano da questo file | Consegnare `MoVi_pitch_IT_v3c_video_italiano.srt` (0 errori) con il video IT, e non `_impressi` |
| D8 | bassa | Riga c1 «spurious identities 1/60 → 0/60, not significant» | Le due fonti mettono l'1/60 in celle diverse: CORREZIONE.md in totale/att, sul seme 20261122; VERIFICA.md in vira/att, appaiato sul seme 20261124. Lo schermo non dice la cella. La riga resta vera, perché dice «not significant» | Facoltativa: togliere la riga, perché non è fra le cifre richieste dalla consegna come risultato |

## 2. Controlli che reggono

| Voce | Esito | Prova |
|---|---|---|
| Durata | **Regge.** EN 174,379 s, IT 170,469 s | ffprobe |
| Formato | **Regge.** H.264 1920×1080, 30 fps; AAC 48 kHz stereo | ffprobe |
| Loudness | **Regge.** EN −14,0 LUFS, LRA 2,8, picco −2,4 dBFS; IT −14,0 LUFS, LRA 3,9, picco −2,1 dBFS | `loudness_qa.txt` |
| Verde (G > 90, G > R+40, G > B+40) | **Regge.** Al massimo 40 px per fotogramma, sparsi: è antialias. 0 fotogrammi sopra 200 px. I «seen» sono ciano | `esito_en.txt`, `esito_it.txt` |
| Etichetta SIMULATION/SCHEMATIC | **Sostenuto dai dati sul campione:** 87/87 EN e 85/85 IT (un fotogramma ogni 2 s) | `ocr_fot_*.json` |
| Lessico vietato | **Regge.** A schermo (OCR) e nei 4 .srt: 0 di validated, guaranteed, detect and avoid, threat, target, counter-drone, always, sub-millisecond, real time, detects the collision, intercept, e delle forme italiane. «never/mai» compare solo condizionato: «In six flight scenarios with the core, MoVi never said clear…», «never clear inside» (la sfera), «never 'clear' on the drone» | `controlla.py`, validazione dei .srt |
| .srt | **Regge.** EN, IT (tempi EN) e IT «video_italiano»: 30 cue, indici e tempi in ordine, 0 sovrapposizioni, fine prima della durata | Script nel § 4 |
| Cifre s1–s7 e s9–s10 contro il verdetto | **Regge.** In `cifre_v3c.json` valore, intervallo e stato coincidono col blocco JSON di VERDETTO_FINALE § 8 per tutte le chiavi del verdetto. L'unica differenza è V-11, a cui si aggiunge solo la nota «F5: near miss at 39 m» (giurato 12). Le cifre dette in voce coincidono: 60/60, 58/60, 60/60 per 10 s, 60/60, 0,85–0,89, 0,73, 200/200 | Confronto automatico |
| Cifre c1 contro i rapporti | **Regge.** 59/59 [0,939; 1] contro 0/59 [0; 0,061] con gli stessi semi; «clear» 0/60 e regione 60/60 (CORREZIONE P5); riacquisizione 49/60 [0,701; 0,894] e 40/60 [0,541; 0,773] sotto 51/60; sfera fino a 565 m, mediana 8 s; 11/200 [0,031; 0,096]. A schermo c'è «fix under test», in voce «a promising path». Non compaiono «risolto», «validato», «riacquisizione entro 2 s» né «zero falsi avvisi» | CORREZIONE.md, VERIFICA.md |
| F7 fedele al registro `registro_F7r_c1_totale.jsonl` | **Verificato sui fotogrammi letti** (EN 112–124 s, IT 110–124 s, più 130, 132 e 138 s a vista). Coincidono il tempo del registro a schermo, il raggio della sfera (184/184,1; 243/242,6; 295/295,2; 335/334,5; IT 301/301,1, 345/345,0, 385/384,6 m), la regione del drone seguito (39/38,9; 139/139,2; 202/201,9 m), la confidenza (barra a circa 0,17 a t = 8,7 s, nel registro 0,1657), lo stato dei sensori e l'avviso acceso. Il centro della sfera è fisso al punto di t0 e scivola indietro di circa 73 m a t = 8,7 s, come nel registro (portatore a 25,5 m/s). Il rallentamento è dichiarato a schermo («playback ×0.3–0.47 (slowed)»). L'avviso parte a 6,0 s e il frammento a 10 m arriva a 7,5 s | `fedelta_F7.txt`; `fot_en/f060`, `f063`, `f066`, `f070` |
| Coerenza con il documento tecnico e la proposta | **Regge**, salvo D1: F7, F7r, c1 (59/59, 11/200, 565 m, 49/60 e 40/60) e confidenza 0,85–0,89 e 0,73 sono uguali. In tutti e tre si dice mai «libero» | `allegato.txt`, `proposta.txt` (pdftotext) |
| Ordine delle scene | **Regge.** F7 (110,2–140,0 s) viene dopo la confidenza sul volo veloce e prima di «Also: the site with taxiing aircraft and drones, and other uses» (140 s) | `tempi/scene_v3c_r2_en.json`, OCR |

## 3. Stati che propongo

- **Video v3c conforme ai vincoli bloccanti** (durata, formato, loudness, verde, etichetta, lessico): **verificato**
  sull'insieme dichiarato, cioè i due file, un fotogramma ogni 2 s e i 4 .srt. Fra i fotogrammi campionati è **non
  verificato**.
- **Fedeltà di F7 al registro c1:** **verificato** su 10 fotogrammi letti. Il resto è **non verificato**, perché l'OCR
  non ha letto il tempo in 14 fotogrammi su 32.
- **Coerenza dei limiti con il documento tecnico:** **smentita** per la riga D1.
- **Ascolto umano e pronuncia IT:** **non verificati**.

## 4. Che cosa propongo dopo

1. Fare una v3d, accanto alla v3c, con D1 (e D2, che costa zero secondi). Rimontare con i comandi del § 5 di
   INTEGRAZIONE.md, usando un `cifre_v3d.json` nuovo.
   - **Previsione:** durata invariata, ±0,05 s.
   - **Smentita:** più di 176,0 s, oppure «not reliable» ancora presente all'OCR fra 150 e 170 s.
2. D3 solo se il gruppo accetta di arrivare a circa 175 s.
3. D4 e D5 se avanza tempo: sono a tempo zero.

File in questa cartella: `previsioni.txt`, `controlla.py`, `fot_en/`, `fot_it/`, `ocr_fot_en.json`, `ocr_fot_it.json`,
`esito_en.txt`, `esito_it.txt`, `loudness_qa.txt`, `fedelta_F7.txt`, `allegato.txt` e `proposta.txt`.
