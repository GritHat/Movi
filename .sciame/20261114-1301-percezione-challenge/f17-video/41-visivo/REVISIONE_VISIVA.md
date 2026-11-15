# MoVi · REVISIONE VISIVA dell'animatic: `sciame-videomaker`, f17-video/41-visivo

Ho cominciato alle 2026-11-15T01:53:55+01:00 e chiuso alle 02:12 (ora presa con `date -Is`). Il file da guardare è
**`video/rendering/animatic_muto_v6c.mp4`**: 1920×1080, 30 fps, 5203 fotogrammi, 173,43 s, H.264 Constrained Baseline
(qualità draft), 25,9 MB, senza audio. Il lint dà 0 errori e 1 avviso, lo stesso della v5. Accanto restano `v6` (la
prima resa) e `v6b` (le correzioni). La v5 non è stata toccata.

## 0. In testa: cambi di stato e regole

- **Regola non rispettata: «nessun dato di sviluppo nel montaggio».** Le scene 1, 4, 5 e 6 disegnano ancora i registri di
  sviluppo di `dati_sviluppo/`, e l'etichetta d'onestà stampa `SCHEMATIC · DEV DATA · NOT A RESULT`. I registri veri
  `prototipo/uscite/lp_A2`, `lp_E1`, `lp_E2` e `lp_E3` esistono, ma non hanno i campi degli eventi (volumi, nubi,
  fiammata, `portata_utile_m`), girano a 2 righe al secondo e nel piazzale A2 non ci sono droni. Non li ho collegati in
  questi 50 minuti. Sui registri veri le scene degli eventi resterebbero vuote. `prototipo/uscite/video/` non esiste
  ancora (verificato con `ls`). `monta_v6.py --finale` continua a rifiutare il montaggio con dati di sviluppo.
- **Il verdetto §6 n. 12 e §7 n. 4 dice che collisione e detriti (E1, E2) sono smentiti.** Le scene 5 e 6, con la voce
  attuale, li presentano come funzioni che vanno: `EVENT: CONTACT · INFERRED`, `WARNING TO OPERATOR · …`. Le correzioni
  spettano alla fase 2b e a `cifre.json` (`E1-X`, `E2-X`). La revisione visiva non le ha cambiate.
- **Mi sono discostato dal piano §4, perché la consegna lo chiede.** Il piano vuole tagli netti fra le scene: ho messo
  un ingresso a tendina di 0,5 s nelle scene 2–7. Il piano vuole la camera ferma nelle scene di dati: ho messo carrelli
  lenti nelle scene 4, 5 e 6, fermi prima degli stati critici. Ho anche cambiato la griglia a tre colonne.
- **Altri lavori in parallelo.** Durante il lavoro un altro ruolo ha riscritto `cifre.json` (la sua v7, per la voce
  guida) e ha modificato `motore_v6.js` dopo la mia resa v6c. Ho preso entrambi i file così com'erano e non ho rifatto
  la resa su quella versione. Il `voce_{en,it}_cifre.txt` scritto da `monta_v6.py` è superato da `video/voce/`: STATO-1,
  sostituito dentro la frase, lascia una frase doppia.
- **File cancellati:** nessuno. Tutto è nuovo e affiancato ai file esistenti. Niente git, niente sudo, niente rete.

## 1. Che cosa ho cambiato, con prima e dopo

Le tavole sono in questa cartella. `prima_v5_foglio.png` e `dopo_v6_foglio.png` hanno un'istantanea ogni 10 s.
`dopo_v6b_fotogrammi_mirati.png` raccoglie 16 istanti scelti; `dopo_v6c_controllo.png` mostra i secondi 58, 155 e 168.

| # | Problema nella v5 (misurato sul codice) | v6c |
|---|---|---|
| 1 | La vista MoVi era 784×690 px (26 % dello schermo); verità e console occupavano 480 e 416 px | La vista MoVi è **1380×900 = 59,9 %** dello schermo. Console 468×560 a destra in alto, verità in un riquadro di 468×300 sotto (`TRUTH (SIM.)`) |
| 2 | Etichette delle tracce a 24 px, console a 19–20 px, bande a 19 px, dominio a 20 px, titolo a 34 px | Etichette di stato a **30 px**. Console e bande a **28 px**, con il testo a capo. Avvisi e dicitura d'onestà a 28 px, titolo della scena a 40 px. Testi delle scene 2, 3 e 7 fra 36 e 64 px; testi fissi della scena 4 a 36 px, della 8 a 36 px |
| 3 | Dischi con raggio 10 px, anello 11 px, glifi dei sensori di 20 px, trame fini | Disco r 17 px, anello r 18 px con tratto 6, glifi ×1,7. Trame più larghe: righe ocra di 20 px, puntini di 14 px |
| 4 | Camera ferma | Fotogrammi chiave in `scene_v6.json` (`camera`), interpolazione morbida, poi camera **ferma**. Scena 4: avvicinamento fra 0 e 10 s, fermo prima del guasto del radar. Scena 5: avvicinamento fra 0 e 5 s, fermo da 5 a 14 s (contatto), poi si allarga fra 14 e 16 s perché il volume cresce, e resta fermo. Scena 6: avvicinamento fra 0 e 3,5 s, fermo prima della fiammata. Scene 2 e 3: carrello di 4–6 % sull'intera scena (≤ 5 %/s, piano §4) |
| 5 | Elementi che comparivano di colpo | Ingressi progressivi: dissolvenza con salita di 24 px, segni che crescono dal centro, `EMPTY` barrato da una linea che si disegna, fascia `POSSIBLE PRESENCE` che si stende, catena a blocchi con i collegamenti tracciati, archi della scena 3 che si disegnano. Nella scena 2, dal 14° s, i tre segni salgono e si rimpiccioliscono per lasciare posto alla fila dei segni d'avviso (nella v6 si sovrapponevano: corretto nella v6b) |
| 6 | Tagli netti | Tendina di 0,5 s nelle scene 2–7, con un filo grigio sul bordo. Nella scena 1 la verità si restringe nel riquadro (0,8 s, morbido) e la vista MoVi entra in dissolvenza. Ponte della console nella 8. Dissolvenza al nero di 0,8 s nella 9 |
| 7 | Apertura: solo il wordmark | Simbolo SDMs v3b che si anima (disco, poi l'ellisse tratteggiata che si disegna), wordmark, titolo a 52 px, riga SDMs · The Big Hack 2026 a 28 px. Fra 0 e 3 s |
| 8 | Chiusura: crediti da 20 a 30 px | Simbolo ×3,2, wordmark 360×150, tagline a 54 px, perimetro a 34 px, filetto che si disegna. Poi `MoVi · Team SDMs · The Big Hack 2026` a 40 px, i cinque nomi a 34 px, crediti a 26 px |
| 9 | Fiammata: un'ellisse piccola solo nella verità | Riquadro **`EO CAMERA · SCHEMATIC`** nella vista: il bianco piatto satura in 3 fotogrammi, compare `SATURATED` e sotto una banda corallo `RELIABILITY LOST · EO`. Il radar resta e l'aereo è `SEEN (RADAR ONLY)`. Nessuna punta né bagliore |
| 10 | Nube e volume con trame fini | Nube a puntini fitti più grandi con contorno a trattini da 4 px. Volume dei detriti a righe ocra, che cresce con il registro, **senza punti** (i quadratini compaiono solo da `ritorni[]`) |
| 11 | Banda di sistema `RELIABILITY LOST` a 32 px | A 48 px, sui 120 px di altezza |
| 12 | Cifre dentro i testi | `cifre.json`: unico file delle cifre, con testo inglese e italiano, stato e fonte. `monta_v6.py` sostituisce i segnaposto a schermo solo se lo stato è `sostenuto` o `verificato`; una riga che comincia con `[STATO-…]` viene sostituita per intero. Gli altri segnaposto restano magenta |

**Righe ancora sotto i 36 px, di proposito:**
- righe di fonte e di dominio, a 22 px (il piano §4 le vuole fra 20 e 22 px);
- `inferred from …`, a 22 px;
- contatori della scena 7, a 30 px in mono: righe lunghe;
- riquadro della classificazione, a 26 px;
- testo dentro il riquadro della verità, fra 20 e 24 px.

## 2. Controlli (stati)

- **Superficie della vista ≥ 60 %:** verificato sul codice: 1 242 000 / 2 073 600 = 59,9 %. Il 60 % pieno non è
  raggiunto per 0,1 punti.
- **Leggibilità:** l'ho controllata a vista su 16 fotogrammi mirati della v6b e su 3 della v6c, ridotti a 640 o 960 px di
  larghezza. Si legge tutto. Non l'ho misurata sul file a 1080p né con una persona esterna.
- **Q11, niente verde:** sulla v6 il massimo è **8 pixel** in un fotogramma a 480×270 (nella v5 erano 4). Pixel isolati
  dove il ciano tocca le trame ambra. Sulla v6c **non verificato**.
- **Q13, etichetta d'onestà:** presente in tutte le istantanee guardate, sulla nuova testata, per tutta la scena. Il
  lampo porta la parola `SCHEMATIC` dentro il riquadro.
- **Q33, mirini:** a vista nessun mirino, reticolo o cono puntato. Restano la regione attorno a un disco e il simbolo SDMs
  v3b, già approvato. Il controllo indipendente non è stato fatto.
- **Verità separata e previsione tratteggiata:** il riquadro della verità resta separato; le regioni restano tratteggiate
  o a righe.
- **Non controllati:** il rendering in italiano (righe più lunghe, con un rischio di sbordare a 28 px nella console), il
  determinismo e la sincronia con la voce vera.

## 3. Difetti che restano

1. Scena 6: `EO · NOT COUNTED` e `IR · NOT COUNTED` cadono in basso a sinistra, sotto la fascia dei sottotitoli.
2. Riquadro della verità: `out of sensor view` è tagliato dal bordo.
3. Scena 4: l'etichetta della pioggia tocca i glifi dei sensori.
4. Scena 5 a ×4: le etichette si sovrappongono in parte sotto le righe ocra, come nella v5.

## 4. Che cosa propongo dopo

1. **Collegare i registri veri, in `scene_v6.json`.**
   - Scena 6: `lp_E2`, dichiarando che non ha la fiammata disegnata, quindi riquadro e nube resterebbero `SCHEMATIC`.
   - Scena 1: `lp_A1`, quando arriva `prototipo/uscite/video/INDICE.md`.
   - Prima va adattato `registri_a_js.py` alle 2 righe al secondo.
2. **Rifare le scene 5 e 6 secondo il verdetto §8:** niente cifre di E1 come successo, e `E2-X` al posto dell'avviso al
   mezzo.
3. **Q11 e Q21 sulla resa `delivery`**, e un rendering italiano di controllo.
