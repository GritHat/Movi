# MoVi · controllo qualità del video EN v1 (`sciame-validazione`, f17-video/51-qa)

Dalle 04:11:00 alle 04:20 circa del 2026-11-15 (`date -Is`). File controllato: `video/consegna/MoVi_pitch_EN_v1.mp4`,
sha256 `0128edff9bb50242309d9fe9377be8486f72fb76416e8931bed5dcd19dea1f3e`. Riferimento delle cifre: `VERDETTO_2C.md`.

## 0. In testa

- **Verdetto: non consegnabile così com'è.** Ci sono 3 difetti di contenuto (D1–D3) contro il verdetto 2c, tutti con
  una correzione di testo che costa poco. Il resto è tecnico o minore.
- **Previsioni:** non le ho scritte prima delle prove. Le soglie sono quelle di ISTRUZIONI §11 e di PIANO §9, fissate da
  altri prima di me.
- **Regole:** ho scritto solo in `51-qa/` (`QA.md` e `strumenti/`) e nello scratchpad, senza cancellare niente. Niente
  git, niente rete, niente sudo. Nessuna violazione.
- **Indipendenza.** Gli strumenti di OCR (tesseract), del verde (`strumenti/verde.py`) e del confronto con i registri
  (`strumenti/registro_per_secondo.py`) sono miei. Condivido con il montaggio i registri `_v3`, `cifre.json` e
  `scene_tempi.js` (la mappa dal tempo del video a quello del registro). Il controllo non coglie quindi un errore nei
  registri o in quella mappa. Nessuna visione né ascolto umani.

## 1. Difetti, in ordine di gravità, con la correzione

| # | Gravità | Difetto | Prova | Correzione |
|---|---|---|---|---|
| D1 | **alta** | La voce della scena 2 dice «It says empty only where it has looked.» senza condizione. È la frase vietata in 2c §4 («non dichiara mai libero ciò che non ha osservato» senza «con la mappa dichiarata, in simulazione»). Con la mappa sbagliata il «vuoto» è falso in 5 casi su 6. In più, A1 n. 8 dà «libero per classi» per 44 fotogrammi con il radar a griglia «persa» (MONTAGGIO §0) | `.srt` cue 9, 00:00:23,342; immagine a 24 s | «In simulation, it says empty only where it has looked, if the site map is right.» (anche in IT e nel `.srt`), poi ricontare Q2 e Q3 |
| D2 | **alta** | Lo schermo della scena 5 scrive «run E1 n. 30, random». 2c §4 vieta «`lp_E1_v3` è il passaggio n. 30 delle misure»: per K-614 non sono la stessa esecuzione (contatto contro separazione, 4972 m contro 2933 m) | OCR dei fotogrammi 70–89 s; `testi.js` chiave `domain.s5` | «run E1 (scene run, not measurement n. 30) · own fragment model» |
| D3 | **media** | «MoVi infers **contact** two point two seconds later; within two seconds in **fifty-one** runs of sixty.» Il 51/60 vale per l'evento di qualunque tipo. Col tipo giusto («contatto») entro 2 s è **50/60** (2c §1, riga E1 entro 2 s) | `.srt` cue 20–21; `testi.js` `s5.e1` | «MoVi infers the event 2.2 s later; within 2 s in 51 runs of 60», oppure tenere «contact» e dire 50 di 60 |
| D4 | media | La scena 8 (corto raggio, `resta_dietro`, «provisional register») porta «SIMULATION». Il 2c (§5) non la elenca fra le scene ammesse come «Simulation», e la consegna lo chiede | fotogrammi 151–158 s | Decisione del coordinatore: «SCHEMATIC», oppure un rinvio scritto al verdetto del corto raggio che ammette il registro |
| D5 | media | Licenze (Q22). I titoli di coda dicono «music, fonts, sources: see description», ma in `video/consegna/` non c'è una descrizione e MONTAGGIO_FINALE non elenca le licenze | `ls video/consegna`; OCR del fotogramma a 168 s | Scrivere `video/consegna/MoVi_descrizione_v1.txt` con: Kokoro-82M, pesi e voci bm_george e im_nicola (Apache-2.0); Inter e JetBrains Mono (OFL 1.1, in `progetto/assets/fonts`); HyperFrames 0.9.48 (Apache-2.0); GSAP, se caricato (licenza standard GreenSock, **non verificato**); tappeto e fruscio generati dal gruppo; schede tecniche pubbliche |
| D6 | media | Parole e ritmo. 350 parole (Q2: ≤ 340). Ritmo sul `.srt`, dalla prima all'ultima parola della scena: 160 · 162 · 132 · 136 · 139 · 139 · 145 · 151 · 100 parole al minuto. Sono 7 scene su 9 oltre 135, e le cifre scritte in lettere gonfiano il conto | conteggio sul `.srt` = `voce_en_detto.txt` (350 = 350) | Togliere circa 10–20 parole nelle scene 1, 2 e 7, oppure registrare una deroga scritta del coordinatore |
| D7 | bassa | La causa dell'«affidabilità persa» è sbagliata nella scena 6. Da 16,0 s a 20,5 s del registro le camere sono «accecato» per «quadri saturi o nube opaca»; lo schermo scrive «health check» già da 16,4 s. «Persa» per il controllo di salute vale solo da 21,0 s | `lp_E2_v3/registro.jsonl` `affidabilita_per_sensore`; fotogrammi 94–98 s | Usare la causa del fotogramma: «saturated frames» fino a 21,0 s del registro |
| D8 | bassa | Q15 (aggiunta del piano): «nessun punto dentro il volume dei detriti». Nella scena 5, dentro il volume, ci sono punti ciano (tracce dei frammenti, «vista» nel registro) e anelli arancio («non vista»). Sono osservazioni del registro e non previsioni, ma la regola letterale è violata | fotogrammi 73–89 s | Decisione: o la deroga scritta («tracce osservate dal registro»), o i frammenti come segni neutri senza riempimento |
| D9 | bassa | Q12: nella scena 2 la parola «EMPTY» compare dentro «UNVERIFIED ZONE» non ancora barrata, per meno di 1 s, prima del tratto | fotogramma a 24 s (foglio 3) | Disegnare «EMPTY» già barrata |
| D10 | bassa | Sovrapposizioni e margini (Q21). Scena 6: «POSSIBLE DEBRIS» copre la scritta «NOT SEEN» della traccia 1 sulla pianta (la console la riporta). Scena 4: «1062 m» è tagliato a destra. Scena 8: «out of sensor view» è tagliato. I primi due sono già noti al montaggio | fotogrammi 96–99, 60 e 157 s | Spostare le etichette, oppure dare la precedenza alle etichette di stato |
| D11 | bassa | La scena 9 (titoli, 159–172 s) non ha l'etichetta d'onestà. È solo testo e marchio, senza immagine di dati | ritaglio dei fotogrammi a 160 e 170 s | Aggiungere «SCHEMATIC», oppure scrivere l'eccezione per i titoli |
| D12 | da verificare | Scena 8 a 151 s: la traccia 1 è «PARTLY SEEN»; il registro dà «vista» a 0,13–0,27 s e «vista_in_parte» da 0,33 s. Lo scarto sta entro il campionamento (circa ±0,5 s) | `resta_dietro/registro.jsonl` | Un fotogramma esatto a 150,81 + 0,33 s |
| D13 | nota | Nella scena 2 la riga «safe indications» viene dalla traccia, ma può leggersi come una promessa di sicurezza | `testi.js` `s2.richiesta` | Valutare «indications for safety» oppure toglierla |

## 2. Le voci del controllo (metodo, prova, esito)

| Voce | Metodo e prova | Esito |
|---|---|---|
| Q1 Durata | `ffprobe` formato **172,77 s**; video 172,77, audio 172,77 | **superata** (165–175) |
| Q19 Formato | `ffprobe`: h264 **High**, yuv420p, 1920×1080, 30/1, 5183 fotogrammi; AAC LC 48 kHz stereo, 287 kbps misurati (320k richiesti, la media VBR è più bassa); `crf=18.0` nelle stringhe dell'encoder; `moov` al byte 36, prima di `mdat` (189 939): faststart | **superata** |
| Q18 Loudness | `ffmpeg -af ebur128=peak=true`: **I −14,0 LUFS**, LRA 3,8, picco vero **−2,3 dBTP** | **superata** |
| Q2/Q3 Voce | 350 parole; ritmo per scena sopra | **non superata** (D6) |
| Q20 Sottotitoli | Script di validazione: 45 blocchi EN e 45 IT, numerazione e tempi corretti, 0 righe oltre 42 caratteri, 0 blocchi oltre 2 righe. Testo EN = parlato (350/350 parole uguali). Sincronia: inizio dei blocchi contro la fine dei silenzi della voce (`silencedetect −40 dB`, `voce_montata.wav`). Tutti gli inizi di frase entro 200 ms (mediana 68 ms); i 9 scarti sopra 200 ms sono blocchi di continuazione a metà frase. L'IT accanto al video EN è sincronizzato per paragrafo | **superata** (EN); IT **non verificato** |
| Q4 Testo a schermo | OCR di 173 fotogrammi; righe di cifre una alla volta. Ho contato a vista: la scena 7 ha 3 contatori di circa 25 parole l'uno, con 16 parole come soglia | **non superata, da decidere** (la scena 7 è una pagina di lettura) |
| Q5/Q6 Cifre | Confronto riga per riga di `MoVi_registro_cifre_v1.md`, del `.srt` e dell'OCR con 2c §1, §3 e §4. Tornano: 956/806 m (registro), 0/200 con il radar d'aeroporto, 1062→1041 e 3994→3915 m, «calculation, not independent», 2,2 s (scena), 4,5 e 5,3 km, 90/90 (v2) e 30/30 (v3) con l'innesco ottimista, circa 96 tracce, 46 %, 12/200, 200/200 e 0/171 con la mappa dichiarata completa, A4 200/200 e 50/200 «earlier core, not re-measured», 564/2400 | **non superata** per D3; il resto **superato** |
| Q9 Frasi vietate | grep sul `.srt` EN e IT, sul copione e sull'OCR (validat\*, guarant\*, detect and avoid, threat, target, counter, sees through, predict\*, always, certif\*, real time, zero false, free, clear, safe, military, DEV DATA, segnaposto). Occorrenze: solo «never declared empty, with the site map declared complete» (condizionata), «RELIABILITY LOST» (stato ammesso), «safe indications» (D13). Frasi di 2c §4: D1 e D2 | **non superata** (D1, D2) |
| Q13 Etichette d'onestà | OCR per secondo più ritagli dei buchi dell'OCR (37, 124–125, 150 s). Presenti dove l'OCR mancava. «Simulation» nelle scene 1, 4, 5, 6 e 8; «Schematic» nelle 2, 3 e 7; zona detriti 5 e 6 «SCHEMATIC» | **superata** per le scene 1–8, salvo D4; scena 9 senza etichetta (D11) |
| Q14 Fedeltà ai registri | `strumenti/registro_per_secondo.py`: un fotogramma al secondo nelle scene «Simulation», confrontato con `lp_A1_v3`, `lp_E3_v3`, `lp_E1_v3` e `lp_E2_v3` al fotogramma più vicino. **Coincidono:** le tracce 3 e 26 «SEEN» (la 26 compare a 23 s del registro); «SEEN (RADAR ONLY)» e la portata nella nebbia; i conteggi «POSSIBLE PRESENCE» della scena 5 (14, 26, 33, 34, 32, 34, 34, 30, 29, 32, 31, 32) e della scena 6 (2, 5, 8, 12, 16, 8, 8, 7, 12, 17, 16, 12, 10, 12, 10, 10); le età «NOT SEEN» (2,5/2,7, 2,5/3,7, 4,5 s); l'evento «CONTACT · INFERRED» non prima di 17,5 s del registro; la fiammata e «RELIABILITY LOST» a 16,0 s; il raggio del volume, da 318 a 2138 m | **superata**, salvo D7 e D12 |
| Q15 Previsione e osservazione | Zone tratteggiate o a righe, anelli vuoti con l'età, nessuna sagoma né cono, «WIDE ZONE» per previsto ampio, «TRUTH (SIM.)» in un riquadro a parte | **superata**, salvo D8 |
| Q11 Verde | `strumenti/verde.py` (mio, numpy): 173 fotogrammi, tinta 90–160°, saturazione > 30 %. Al massimo **58 px in tutto** in un fotogramma (109 s), 4 fotogrammi sopra 50 px **in somma**. L'area connessa è ≤ 58 e quindi non verificata sotto 50. Il controllo del montaggio dà un'area massima di 2. A vista: nessun verde | **superata** con riserva (pixel di bordo del ciano) |
| Q33 Lessico d'ingaggio nelle immagini | Fogli 1, 2, 3, 5, 6, 9, 11 e 17: nessun mirino, reticolo o cono puntato. I cerchi concentrici della scena 5 sono i contorni a −2, −4 e −6 s del volume, non bersagli | **superata** |
| Q34 Tempo compresso | «×5 · time compressed» dal secondo 3, insieme al segmento ×5 di `scene_tempi.js` | **superata** |
| DEV DATA | 0 nell'OCR di 173 fotogrammi; 0 nei sorgenti (MONTAGGIO) | **superata** |
| Q23 Volti e marchi | Solo glifi e sagome; marchi solo MoVi e SDMs; nessun nome commerciale di sensore a schermo (OCR) | **superata** |
| Q22 Licenze | si veda D5 | **non superata** |
| Q17 Segnali sonori | Non ascoltato. MONTAGGIO dichiara che nessun suono è legato agli stati | **non verificato** |
| Procedura IT | `genera_versione_italiana.sh` esiste e non cancella (si ferma se l'uscita c'è). La prova in bozza `MoVi_pitch_IT_v1_draft.mp4` è di 172,77 s, h264 1920×1080 30 fps, AAC 48 kHz, −14,0 LUFS e picco −2,1 dBTP. **Delivery non eseguita** | **sostenuto dai dati** (bozza) |

## 3. Stati proposti

- Video EN in 165–175 s, a −14 LUFS, nel formato richiesto: **verificato** (ffprobe, ebur128).
- Stati e conteggi a schermo coincidono con i registri `_v3`: **verificato** su un fotogramma al secondo nelle scene 1, 4,
  5 e 6, salvo D7. Vale solo se la mappa dei tempi di `scene_tempi.js` è giusta.
- Il video dice le stesse cose del verdetto 2c: **smentito** da D1, D2 e D3.

## 4. Dopo

1. Correggere D1–D3 nei modelli della voce, in `testi.js` e in `cifre.json`. Rifare la voce EN e IT, poi rimontare.
2. Far decidere al coordinatore D4, D6, D8 e D11, e scrivere la descrizione con le licenze (D5).
3. Ripetere questo controllo sul v2 con gli stessi script, poi fare una visione e un ascolto umani.
