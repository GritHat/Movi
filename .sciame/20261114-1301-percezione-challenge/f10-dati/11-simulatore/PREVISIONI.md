# Previsioni di `sciame-visione` — f10, 11-simulatore

Scritte alle **2026-11-14T16:21:53+01:00** (`date -Is`), prima di scrivere una riga del simulatore e prima di ogni
prova. Lette fino a qui: `CONTRATTO_DATI.md`, `02-sensori/MODELLO_SENSORE.md`, `parametri_sensori.json`,
`VALIDAZIONE_MODELLO.md`, `03-infrastruttura/AMBIENTE.md`, `formato_sequenza.md`, l'inizio di `SOLUZIONE_V2.md`.
Gli esiti (regge / smentita / non risolta) si aggiungono in fondo, senza toccare il testo sopra.

Risoluzione prevista: 424×240 a 15 fotogrammi al secondo (il sensore a 848×480 campionato 1 pixel su 2: il rumore in
metri resta quello a 848×480). Profili: `realsense_d455`, `realsense_d435i`, `orbbec_gemini_335`.

| # | Previsione | Misura | Soglia che la smentisce |
|---|---|---|---|
| visione-P1 | Su parete piana frontale a 1, 2, 3, 4 m il rumore totale simulato ridà σz = k_nominale·z² | scarto tipo del residuo dal piano vero, pixel validi nell'80 % centrale, media su 30 fotogrammi; 3 profili × 4 distanze | una cella su 12 fuori da ±10 % |
| visione-P2 | Lo stesso al livello «limite» (k_limite) | idem, 3 profili × 4 distanze (in memoria se non su disco) | una cella fuori da ±10 % |
| visione-P3 | Il rumore temporale è 0,6 volte il totale | scarto tipo per pixel su 30 fotogrammi, mediana, diviso lo scarto totale | rapporto fuori da 0,55–0,65 in una cella |
| visione-P4 | Sulla parete (diffuso chiaro) i buchi sono lo 0,5 % (nominale) e il 2 % (limite); un buco persiste con probabilità 0,7 | quota di zeri nell'80 % centrale; P(buco a t+1 dato buco a t) | nominale fuori da 0,2–0,9 %; limite fuori da 1–3 %; persistenza fuori da 0,65–0,75 |
| visione-P5 | La banda senza dato al bordo sinistro dell'immagine è larga fx·B/z pixel (nominale); al limite +12,5 px (25 px a 848) | prima colonna valida per riga, mediana, pareti a 1–4 m | differenza dalla formula oltre ±1 px |
| visione-P6 | A sinistra del bordo sinistro del pannello (a 1,8 m, nessuna persona) manca lo sfondo per fx·B·(1/z_pannello − 1/z_sfondo) pixel; a destra del bordo destro niente | (a) uscita solo geometrica: larghezza per riga contro la formula; (b) modello completo: mediana su righe e fotogrammi | (a) meno del 95 % delle righe entro ±1 px, o bordo destro con banda > 0 in più del 5 % delle righe; (b) mediana fuori da ±1,5 px, o mediana a destra > 1 px |
| visione-P7 | La profondità ideale del suolo coincide con la formula dell'infrastruttura (`profondita_del_suolo`, altro autore) | massimo scarto sui pixel del suolo, pavimento vuoto, prima del rumore | scarto > 0,5 mm |
| visione-P8 | La maschera vera dell'ombra e l'immagine ideale sono coerenti: nessun pixel ideale del suolo cade in una cella «in ombra» | pixel del suolo riproiettati sul piano (pannello, cassa), a più di 2,5 cm dal confine dell'ombra | anche un solo pixel |
| visione-P9 | Tutte le sequenze rispettano il formato comune | `controlla_sequenza.py` su ogni cartella | un solo `ERRORE`. Avvisi attesi solo per le pareti a 1 e 2 m (niente suolo in vista con inclinazione 0) e per le sequenze azzerate |
| visione-P10 | Il simulatore sta nei tempi e nello spazio | tempo per fotogramma (un processo); `du -sb sequenze` | oltre 40 ms a fotogramma in media; oltre 2,0·10⁹ byte |
| visione-P11 | Nel caso (a) a 1,2 m/s ogni passaggio ha un tratto del tutto nascosto di 8–14 fotogrammi (0,88 m di ombra piena a 2,3 m: 0,73 s), e la testa (1,7 m) non spunta sopra il pannello (linea di vista a 1,711 m) | fotogrammi con `frazione_visibile` = 0 per passaggio, 30 passaggi | un passaggio fuori da 8–14, o un fotogramma con pixel visibili nel mezzo del tratto nascosto |
| visione-P12 | I filtri del costruttore (persistenza 3 e riempimento «dal vicino più lontano») portano i pixel validi oltre il 99,5 % e riempiono la banda d'occlusione a sinistra del pannello con la profondità dello sfondo | quota di validi con e senza filtri; nella banda vera, quota di pixel riempiti con un valore entro il 10 % dello sfondo | validi < 99,5 %; meno dell'80 % della banda riempito con lo sfondo |

Scelte fissate prima delle prove (non sono previsioni): profilo principale `realsense_d435i` (le curve del nucleo
sono le sue, `MODELLO_SENSORE.md` §6.1); semi derivati dal nome della sequenza; `visibile` = almeno un pixel ideale
del soggetto nell'immagine.

## Aggiunta delle 2026-11-14T16:26:35+01:00 (`date -Is`; prima di ogni prova, a codice non ancora scritto)

(Nota: nella prima stesura di questa riga avevo scritto «16:33» a mano, senza leggerlo dall'orologio: corretto subito
con l'ora stampata da `date -Is` nello stesso comando che ha aggiunto il testo.)

Progettando il passo 4 del modello mi accorgo che al livello «limite» `parametri_sensori.json` moltiplica il
sottopixel per 1/cos(incidenza) anche sotto i 60°. Su una parete frontale l'incidenza del raggio è l'angolo di campo:
nell'80 % centrale il fattore quadratico medio atteso è √(1 + 0,8²/3 + (0,8·0,566)²/3) ≈ 1,13. **Prevedo quindi che
visione-P2, così come è scritta sopra, sia smentita** (rumore sopra k_limite·z² di circa il 13 %), e aggiungo:

| # | Previsione | Misura | Soglia che la smentisce |
|---|---|---|---|
| visione-P2bis | Al livello «limite» il rumore su parete vale k_limite·z² nel 20 % centrale del campo, e 1,13·k_limite·z² sull'80 % centrale | come P1, su due regioni | una cella fuori da ±10 % del valore atteso della sua regione |

## Aggiunta delle 2026-11-14T16:34:54+01:00 (`date -Is`), dopo la prima corsa di `controlli.py modello` (16:34:17)

Notato DOPO la prima corsa (non era scritto prima): la parte «20 % centrale» di visione-P2bis esce da ±10 % in 3 celle
su 12 (da 0,945 a 1,167). Sospetto l'errore di campionamento: la regione ha circa 4000 pixel e il rumore fisso è
correlato su 2,5 px, quindi i campioni indipendenti sono una cinquantina e lo scarto tipo si stima al 10 % circa.
La soglia di P2bis era dunque mal posta; l'esito resta «smentita» per quella parte, e la causa si decide così:

| # | Previsione | Misura | Soglia che la smentisce |
|---|---|---|---|
| visione-P2ter | Con 20 semi diversi del rumore fisso, lo scarto quadratico medio nel 20 % centrale al livello «limite» vale 1,01·k_limite·z² (errore di campionamento atteso 2,2 % per cella) | 12 celle (3 profili × 4 distanze), 20 semi × 6 fotogrammi, varianze mediate fra i semi | una cella fuori da 0,94–1,08 (3 errori tipo) |

## Aggiunta delle 2026-11-14T16:41:24+01:00 (`date -Is`), prima di due controlli nuovi sulle sequenze scritte

| # | Previsione | Misura | Soglia che la smentisce |
|---|---|---|---|
| visione-P13 | La visibilità scritta in `verita.json` (dal lancio dei raggi in 3D) coincide con un conto angolare in pianta fatto a parte: la persona è coperta di lato se il suo settore angolare [θ − asin(r/ρ), θ + asin(r/ρ)] sta dentro quello del pannello, è intera se non lo tocca | 30 passaggi a12 + 30 a05 + 30 b; fotogrammi in cui le due classificazioni (intera / parziale / coperta, con «coperta» = meno di 10 pixel visibili) differiscono | più dell'1 % dei fotogrammi discordi, o un discorde a più di 2 cm dal confine angolare |
| visione-P14 | Rigenerare una sequenza dal catalogo dà gli stessi byte | tre sequenze (una statica, un passaggio, una con i filtri) rigenerate in memoria e confrontate con il disco | un solo pixel diverso |

## Esiti (scritti alle 2026-11-14T16:42:23+01:00; prove: `controlli_modello.txt`, `controlli_semi.txt`, `controlli_disco.txt`, `controllo_formato.txt`, `riepilogo.txt`)

| # | Esito | Cifre |
|---|---|---|
| P1 | **regge** | σ misurato / k_nominale·z² da 0,991 a 1,027 su 12 celle (in memoria e riletto dal disco: uguali) |
| P2 | **smentita** (come previsto alle 16:26) | al limite, 80 % centrale: da 1,120 a 1,169 volte k_limite·z² (il JSON mette 1/cos dell'incidenza anche sotto i 60°) |
| P2bis | **smentita in parte** | 80 % centrale / (1,13·k·z²): da 0,991 a 1,035 (regge); 20 % centrale: da 0,945 a 1,167, 3 celle su 12 fuori da ±10 % |
| P2ter | **regge** | con 20 semi: da 0,990 a 1,031, media 1,009; dispersione fra i semi 4,7 % (con 60 semi: 4,7–5,0 %, massimo 1,15). La parte smentita di P2bis era errore di campionamento più una soglia mal posta; i due semi delle sequenze a 3 m stanno nella coda (1,137 e 1,167) |
| P3 | **regge** | rapporto temporale / totale da 0,587 a 0,624 su 24 celle |
| P4 | **regge** | buchi 0,46–0,58 % (nominale), 1,83–2,17 % (limite); persistenza 0,685–0,737 |
| P5 | **regge** | misurata − formula da +0,08 a +0,97 px (la banda è l'intero superiore di fx·B/z) |
| P6 | **regge** | (a) 100 % delle righe entro ±1 px per i tre profili (mediane attese 7,75 / 4,08 / 3,95 px; a destra 0 %); (b) mediane 7 / 4 / 4 px, a destra 0 |
| P7 | **regge** | scarto massimo 0 mm (stessa formula in doppia precisione) |
| P8 | **regge** | 0 pixel di suolo in ombra su 45 479 (pannello) e 42 817 (cassa); 0 celle d'ombra su pixel di suolo; banda stereo: 0 discordi lontano dal confine, 40–50 sul confine (arrotondamento) |
| P9 | **regge sulla soglia** (0 errori su 162 sequenze); **l'elenco degli avvisi attesi era sbagliato** | 11 avvisi: le 8 pareti a 1 e 2 m (attesi) e 3 sequenze al limite (`d435i_lim__pavimento_vuoto`, `…pavimento_lucido`, `…pannello_a12__s00`: «5–12 % dei pixel vede oltre il suolo», è il rumore del suolo radente al limite); nessun avviso sulle sequenze azzerate |
| P10 | **regge** | 14,0 ms a fotogramma in media (128,3 s per 9152 fotogrammi, un processo); 1 874 040 732 byte |
| P11 | **smentita** | fotogrammi con frazione = 0 da 6 a 12 (previsti 8–14): in 2 passaggi su 30 la testa spunta sopra il pannello (3–7 pixel) quando la persona sta sotto 2,272 m. Avevo trascurato la curvatura della testa: a 2,30 m il margine è 6 mm, non 11. Con la soglia «frazione < 2 %» i fotogrammi nascosti sono 10–12 |
| P12 | **smentita sulle due soglie** | validi dal 97,0 al 99,3 % (previsto ≥ 99,5: la banda al bordo sinistro resta in parte vuota); banda d'occlusione riempita al 100 %, con lo sfondo nel 79,9 % e nel 76,4 % dei pixel (previsto ≥ 80 %), con il pannello nel 4–6 %. Il meccanismo (la banda diventa sfondo) c'è; le mie soglie no |
| C13 | **regge** | 0 pixel diversi su 10 640 fra i filtri in numpy e la trascrizione pixel per pixel |
| P13 | **regge** | 1 fotogramma discorde su 6170 (0,02 %), a 0,05 cm dal confine |
| P14 | **regge** | 0 pixel diversi su 16 790 400 |

Notato DOPO, senza previsione: il riempimento «dal vicino più lontano» fa colare lungo la banda del bordo sinistro la
profondità della parete di fondo (3,57 m dove il suolo vero è a 1,5 m: `d435i_nom__pavimento_vuoto__filtri`, riga 238).
