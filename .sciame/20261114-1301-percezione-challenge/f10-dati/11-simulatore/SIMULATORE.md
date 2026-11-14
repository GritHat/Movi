# Simulatore della camera di profondità — f10, `11-simulatore` (`sciame-visione`), 14 novembre 2026

Percorsi relativi a `f10-dati/11-simulatore/`. Interprete: `../ambiente/venv/bin/python -I -B`.

**In testa.** Il simulatore è **verificato contro il proprio modello**, non contro un sensore: le cifre dicono che il codice fa ciò che dice `parametri_sensori.json`. Di 16 previsioni (`PREVISIONI.md`, scritte prima) 12 reggono e **4 sono smentite**: P2 e parte di P2bis (rumore al limite), **P11** (la testa spunta sopra il pannello), **P12** (soglie sui filtri). Scostamenti: un'ora scritta a mano in `PREVISIONI.md`, corretta subito; quattro sorgenti di librealsense scaricati in `scaricati/` di questa cartella, solo letti; anteprime PNG nella cartella temporanea della sessione; il controllo del formato ha usato molti fili per 27 s; due passi del modello in ordine diverso dal JSON (§2).

## 1. Che cosa genera

File: `simsens.py` (geometria, modello, filtri, verità), `catalogo.py` (scene, percorsi), `genera.py` (scrive le sequenze; `genera.simula(spec)` le dà **in memoria**), `controlli.py`, `riepilogo.py`.
- **Geometria.** Stanza 8 × 7 × 3 m, scatole, persone = capsule (raggio 0,2 m, 1,7 m). Camera a 1,2 m, inclinata di 15° (0° per le pareti). Un raggio per pixel a 424×240, 15 fps: **il sensore a 848×480 campionato 1 pixel su 2**, con il rumore in metri invariato.
- **Modello**, i sette passi del JSON ai due livelli **nominale** e **limite**: buchi geometrici (distanza minima, banda al bordo sinistro, occlusione stereo a sinistra dei bordi verticali); bordi spostati, oggetto vicino ingrossato, pixel misti; rumore in disparità fisso (0,8·s) e temporale (0,6·s), correlato su 5 px, per incidenza e materiale; quantizzazione a 1/32 px e 1 mm; buchi a macchie con persistenza 0,7; riflesso falso sul pavimento lucido.
- **Filtri del costruttore** (variante `__filtri`, stesso seme): temporale (α 0,4, δ 20 mm, persistenza 3) e riempimento «dal vicino più lontano» dell'SDK RealSense, riscritti dai sorgenti aperti oggi (`scaricati/PROVENIENZA.md`).
- **Verità** (`verita.json`): per fotogramma x, z, vx, vz, `visibile`, `frazione_visibile`, pixel della sagoma, visibili e validi; ostacoli; `ombra_suolo`, maschera polare (1° × 0,1 m fino a 4 m) e cartesiana (2,5 cm) a cinque classi: visibile, in ombra, non osservabile, impronta, banda stereo. Indici: `sequenze/INDICE.csv`, `sequenze/PASSAGGI.csv`.

## 2. Parametri e fonte

Tutti da `../02-sensori/parametri_sensori.json`, che dà per ogni chiave la provenienza e il link (le schede **non le ho riaperte io**); i valori usati sono copiati in ogni `meta.json`.

| Grandezza | D455 | D435i | Gemini 335 | Fonte nel JSON |
|---|---|---|---|---|
| Base; fx a 848 px | 95 mm; 424 | 50 mm; 424 | 50 mm; 410,7 | dichiarati: scheda D400 rev. 023, scheda Gemini 330 v1.6 |
| k in σz = k·z², nominale / limite | 0,00199 / 0,0050 | 0,00377 / 0,0100 | 0,0040 / 0,0075 | calcolati dal sottopixel 0,08 e dai limiti di scheda |
| Distanza minima | 0,35 m | 0,195 m | 0,18 m | dichiarata |
| Buchi, nominale / limite | chiaro 0,005 / 0,02; scuro 0,05 / 0,3; nero 0,3 / 0,8; lucido 0,1 / 0,5 | | | dichiarato solo il chiaro; il resto **ipotesi** |
| Bordi | spostamento 1,5 px / 4,3 cm; ingrossamento 2 px; misti 3 px | | | misurati i 4,3 cm (Ahn e altri, 2019); il resto **ipotesi** |
| Oltre 60° d'incidenza | rumore 1/cos / ×5; buchi 0,05 / 0,5 a 75° | | | **ipotesi** |

**Letture mie dove il JSON è ambiguo:** rumore fisso attaccato all'immagine (chi si muove prende tutta σz, come in `MODELLO_SENSORE.md` §6.5); i 4,3 cm usati come scarto tipo (nella fonte sono un 90° percentile); occlusione calcolata dopo lo spostamento dei bordi, buchi decisi prima del rumore. **Ipotesi mie:** andatura (velocità ±8 %, oscillazione di 2 cm), sfocatura da moto, copertura e azzeramento.

## 3. Controlli (`controlli_*.txt`, `controllo_formato.txt`, `riepilogo.txt`)

| Controllo | Cifre |
|---|---|
| **Rumore su parete** a 1 / 2 / 3 / 4 m, 80 % centrale (P1) | D455 2,0 / 8,1 / 17,7 / 32,1 mm (attesi 2,0 / 7,9 / 17,9 / 31,8); D435i 3,8 / 15,0 / 34,5 / 60,8 (3,8 / 15,1 / 34,0 / 60,4); Gemini 4,0 / 15,9 / 36,6 / 64,8 (4,0 / 16,0 / 36,0 / 64,0) |
| Al **limite** (P2, P2bis, P2ter) | 1,12–1,17 volte k_limite·z² nell'80 % centrale (il JSON mette 1/cos dell'incidenza: atteso 1,13); 0,990–1,031 nel 20 % centrale, su 20 semi |
| Temporale / totale; buchi; persistenza (P3, P4) | 0,587–0,624; 0,46–0,58 % e 1,83–2,17 %; 0,685–0,737 |
| **Banda al bordo sinistro**, parete a 1 m (P5) | 21 px (formula 20,1), 11 (10,6), 11 (10,3); al limite +12,5 px |
| **Banda d'occlusione al pannello** (P6) | sola geometria: 100 % delle righe entro ±1 px; attese 7,75 / 4,08 / 3,95 px, misurate 7 / 4 / 3; a destra 0. Modello completo: 7 / 4 / 4 |
| Suolo contro la formula dell'infrastruttura (P7); ombra contro immagine (P8) | scarto 0 mm; 0 pixel di suolo in ombra su 45 479 |
| Visibilità contro un conto angolare in pianta (P13); rigenerazione (P14) | 1 fotogramma discorde su 6170; 0 pixel diversi |
| Filtri contro la trascrizione del sorgente (C13) | 0 pixel diversi su 10 640; **non confrontati con l'SDK vero** |
| Formato (P9); tempo e spazio (P10) | 162 su 162 senza errori, 11 avvisi (8 pareti senza suolo in vista, 3 al limite); 14,0 ms a fotogramma; **1,874 GB** |

Indipendenza: stesso autore e stesso JSON del simulatore; a parte stanno solo la formula del suolo e le formule chiuse.

## 4. Le sequenze — `sequenze/<profilo>_<nom|lim>__<scena>[__sNN][__filtri]/`: 162 cartelle, 9152 fotogrammi

| Gruppo | Cartelle | N |
|---|---|---|
| taratura | `parete_{1,2,3,4}m`, `pavimento_vuoto`, `pannello_vuoto` per `d455_nom`, `d435i_nom`, `g335_nom`, `d435i_lim` | 24 |
| (a) | `d435i_nom__pannello_a12__s00…s29` (1,2 m/s), `…a05__s00…s29` (0,5 m/s): pannello 1 × 1,6 m a 1,8 m, persona a 2,3 m; passaggi pari da sinistra, dispari da destra | 60 |
| (b) | `d435i_nom__pannello_b__s00…s29`: sosta di 3 s dietro | 30 |
| (c), (d) | `…pannello_c__s00…s03` (torna indietro), `…pannello_d__s00…s03` (si allontana nell'ombra fino a 4,2 m) | 8 |
| limite e altri profili | `d435i_lim`: a12 ×4, b ×2; `d455_nom`, `g335_nom`: a12 ×3, a05 ×1, b ×1 (stessi percorsi) | 16 |
| altre (`d435i_nom`) | `cassa_persona__s00`; `sospeso_2p0m` (0 pixel), `sospeso_2p8m` (1398); `scatola15_0p8m` (0 pixel), `scatola15_2p0m` (266); `vetro_sfondo`, `vetro_buco`; `pannello_a12_scuro`, `_nero`, `_alta185` (×2); `sensore_coperto`, `sensore_mezzo_coperto`, `azzeramento_progressivo`; `pavimento_lucido` (anche `lim`); `d435i_lim__pannello_a12_scuro__s00` | 19 |
| filtri | `d435i_nom__{pavimento_vuoto, pannello_vuoto, pannello_a12__s00, pannello_a12__s01, pannello_b__s00}__filtri` | 5 |

**Ridotto per stare in 2 GB:** metà risoluzione, 15 fps, rincorse corte (7–12 fotogrammi interi prima dell'ombra), 4 passaggi per (c) e (d), pochi al limite: gli altri si generano in memoria.

## 5. Che cosa il modello NON riproduce

Niente accoppiamento stereo vero (nessun errore da trama, superfici ripetitive, luce ambiente); niente distorsione né errori di taratura (**la posa è esatta**); persone rigide senza arti, pavimento piano, stanza vuota; tempi regolari, senza latenza né fotogrammi persi; filtri della Gemini ignoti; decimazione e filtro spaziale assenti. I parametri che decidono «libero» oltre 2 m (incidenza, buchi sul suolo) sono **ipotesi senza misura**.

## 6. Critiche, stati, proposte

1. **La geometria della demo è sul filo.** Una persona di 1,70 m a 2,30 m dietro il pannello di 1,60 m ha 6 mm di margine (conto mio): sotto 2,27 m la testa spunta. Nei dati spunta in 2 passaggi su 30 (a12), 6 su 30 (a05), 2 su 30 (b), fino a 7 pixel; con 1,85 m restano in vista fino a 365 pixel (`PASSAGGI.csv`). **Chi valida usi `frazione_visibile < 0,02`, non `visibile`**: così i fotogrammi nascosti sono 10–12 (a12). Stato: **dimostrato** nel modello a capsula; sul vero, da misurare.
2. **I filtri fanno ciò che K-014 teme**: la banda d'occlusione è riempita al 100 %, con lo sfondo nel 76–80 % dei pixel, e lungo il bordo sinistro cola la profondità della parete di fondo (3,57 m dove il suolo è a 1,5 m). Stato: **sostenuto in simulazione**.
3. **Suolo fra 2 e 3 m** (D435i): al nominale validi il 96,7 %, residuo 78 mm; al limite validi il 73,8 %, e il 25,7 % di questi oltre il suolo di più del 10 %. L'ipotesi 1 dipende da parametri non misurati: **non risolto**.
4. Dietro il pannello la banda d'occlusione verso la persona vale 1,4 cm (D435i) e 2,6 cm (D455), non i 19 cm del caso 1 m contro 3 m (conto mio: B·0,5/1,8).

**Proposte.** *visione-1:* ogni ipotesi si prova ai due livelli, generando in memoria i passaggi al limite; la smentisce un esito che cambia fra i due. *visione-2:* pannello alto almeno 1,8 m nella demo; la smentisce un attore di 1,85 m che resta coperto con 1,6 m. *visione-3:* all'arrivo del sensore, parete a 1, 2, 3 m, suolo e un bordo verticale sostituiscono le ipotesi. **Non fatto:** la coppia IR con accoppiamento semiglobale (passo 2 dell'esperto di sensori).
