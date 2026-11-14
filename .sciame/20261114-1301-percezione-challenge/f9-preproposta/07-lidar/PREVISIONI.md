# Previsioni di `sciame-lidar`, estensione f9 (S9 e attacco 4)

Scritte alle **2026-11-14T15:40:23+01:00** (`date -Is`), dopo aver letto il contratto, il quinto addendum, la
preproposta, `FONTI_VERIFICATE.md`, la mia consegna di f1 e `SOLUZIONE_V2.md`, e **prima** di aprire qualunque scheda
tecnica o pagina in rete e prima di ogni conto con uno script. Le cifre qui sotto vengono dalla memoria o da un conto a
mente: valgono come previsioni, non come dati.

| # | Enunciato | Misura | Soglia di smentita |
|---|---|---|---|
| L1 | Il proiettore delle camere a stereo attivo (D435i, D455, Gemini 335) emette a circa 850 nm; i VL53L7CX e VL53L8CX a 940 nm. Non sono la stessa lunghezza d'onda: distano almeno 80 nm. | lunghezze d'onda nelle schede dei costruttori | una scheda che dà per una camera 940 nm, o per i VL53 850 nm, o una distanza sotto 50 nm |
| L2 | La scheda ST non pubblica la banda passante del filtro del ricevitore: «il filtro respinge gli 850 nm» resterà **non verificato** sulle carte. | ricerca di «filter», «bandwidth», «nm» nel testo della scheda | la scheda dà larghezza o trasmissione fuori banda |
| L3 | I ricevitori della camera stereo non hanno un filtro stretto: vedono anche i 940 nm (sono sensibili dal visibile al vicino infrarosso). Il verso plausibile del disturbo «tempo di volo → stereo» esiste ma è innocuo: luce diffusa senza trama, che non crea né buchi né profondità false. | scheda RealSense: filtro sugli imager di profondità | la scheda dà un filtro passa-banda stretto a 850 nm sui modelli senza la «f» |
| L4 | Il verso «proiettore → tempo di volo» si manifesta, se c'è, come aumento della luce di fondo contata dal sensore (non correlata con i suoi impulsi), cioè meno portata e più rumore, non «ostacoli fantasma ai bordi del campo». Con i sensori puntati di lato (assi a 90°) i due campi non si sovrappongono affatto. | geometria dei campi (conto); grandezza `ambient_per_spad` nel manuale del driver | il manuale ST o una misura mostrano bersagli falsi da una sorgente continua non correlata |
| L5 | Frequenza massima di misura: 15 Hz in 8×8 e 60 Hz in 4×4, per tutti e due i modelli. Il VL53L8CX ha un piedino di sincronia esterna; per il VL53L7CX non lo so (probabilità che ce l'abbia: 40 %). | schede e manuali del driver | valori diversi nella scheda |
| L6 | L'accensione alternata di tre sensori senza trigger costa: ciascuno misura al più a un terzo della frequenza (5 Hz in 8×8). Realizzabile, ma dimezza o peggio il già scarso margine di preallarme. | conto dai tempi della scheda | il manuale mostra che si alternano tre sensori a 15 Hz ciascuno in 8×8 |
| L7 | Preallarme: 0,5 m / 1,4 m/s = 0,36 s; tolto un periodo di misura (67 ms a 15 Hz) restano 0,29 s; con l'alternanza a 5 Hz restano 0,16 s. In ogni caso meno della somma «latenza del nucleo (circa 0,15 s) + segnale di 0,3 s»: **è un'etichetta, non un preallarme**, per chi cammina a passo normale. | conto | margine utile ≥ 0,5 s con parametri della scheda |
| L8 | Copertura angolare: camera 87° + tre sensori da 60° = al più 267° su 360°; con gli assi a ±90° restano due fessure cieche di circa 16,5° fra camera e sensori laterali, proprio da dove entra chi «arriva di fianco». | conto | nessuna fessura con un montaggio a tre sensori |
| L9 | Tessuto nero opaco (riflettività 3–5 % nel vicino infrarosso): portata del VL53L7CX in 8×8 circa 0,35–0,5 m **al buio**, meno con la luce. A 2,5 m è fuori portata di un fattore 5 o più. La soglia di 0,5 m del preallarme non è garantita nemmeno al buio su una persona vestita di nero. | scala con la radice della riflettività, ancorata ai valori della scheda (bianco 88 %, grigio 17 %) | la scheda dà ≥ 1 m su un bersaglio al 5 % o meno in 8×8 |
| L10 | Camera stereo sul nero a 2,5 m: l'esito tipico sono **buchi** (profondità non valida), non profondità sbagliata, purché i filtri che riempiono i buchi siano spenti; la quota di buchi dipende dal tessuto (molti neri riflettono nel vicino infrarosso) e resterà **non verificato** senza la camera. | fonte del costruttore o articolo, altrimenti dichiarato non verificato | una fonte primaria che quantifica profondità sbagliate (non buchi) sul nero |
| L11 | Una persona in nero (sagoma 0,5 m × 1,7 m) a 2,5 m toglie circa il 6–7 % dei pixel e circa il 13 % delle direzioni; a 1 m circa il 26 % dei pixel e il 32 % delle direzioni. In nessuno dei due casi si scende sotto metà della taratura: il segnale «sensore coperto» non scatta. Scatterebbe da sola solo sotto circa 0,6–0,75 m. | conto geometrico con uno script | quota sopra il 50 % a 1 m o a 2,5 m |
| L12 | Tre VL53L7CX hanno lo stesso indirizzo I2C all'accensione; si gestisce con un piedino (LPn) per sensore e il cambio d'indirizzo via software a ogni avvio, oppure con un multiplatore I2C. Ogni avvio carica un firmware di decine di kB per sensore (secondi, non millisecondi). | scheda e manuale del driver | indirizzo fissato da piedini, o nessun firmware da caricare |
| L13 | Verdetto atteso su S9: **approvata con correzioni** come canale facoltativo di sola prossimità (mai «libero»), **respinta** come «preallarme» e come contenuto del taglio a 24 ore; ore: 6–10 per una persona che non l'ha mai fatto. | l'insieme delle prove sopra | L7 smentita (margine ≥ 0,5 s) e L9 smentita |

Braccio che deve fallire (controllo che il conto non sia cieco): con una soglia a 2 m e un sensore a 15 Hz il margine
deve risultare oltre 1 s; con la sagoma a 0,4 m la quota di direzioni deve superare il 50 %.

## Esiti (compilati dopo le prove)

Vedi in fondo, sezione aggiunta dopo: ciò che sta sopra questa riga non è stato modificato dopo l'ora indicata.

Esiti scritti alle 2026-11-14T15:50+01:00, dopo le schede (cartella `scaricati/`) e i conti (`conti_s9.py`,
`risultati_conti_s9.txt`). **[g]** = trovato con una ricerca nel testo scaricato; **[r]** = letto attraverso lo strumento
di lettura delle pagine, che riassume (più debole).

| # | Esito | Prova |
|---|---|---|
| L1 | **regge** | RealSense D43x/D45x: «Laser Wavelength 850nm ± 10 nm», tab. 3-17 [g]; Gemini 330: «850nm ± 6nm» [g]; VL53L7CX e L8CX: «Infrared emitter 940 nm» [g]. Distanza 90 nm. |
| L2 | **regge** | nella scheda DS13865 Rev 6 «filter» compare solo per il bus I2C [g]; un dipendente ST sul forum: «940 +/- 10nm is what we are shooting for. But the filter is not absolute» [r]. |
| L3 | **regge** per il filtro; l'innocuità resta **non verificata** | D430 e D450: «Filter Type: None»; D435i/D455: «Depth Filter: All pass» [g]; Gemini 335: «All-Pass» [g]; guida RealSense: gli imager «see all light in the visible and IR» [r]. |
| L4 | **regge** sulla geometria (conto); il meccanismo è **sostenuto da una fonte debole** | con gli assi a ±90° il proiettore (90° di campo) e i sensori (60°–120°) non si sovrappongono; ST sul forum: gli altri sensori sono visti «as ambient light» [r]. Corretto dopo: fra due sensori ST uguali può comparire un bersaglio in più, con stato non valido [r]. |
| L5 | frequenze: **regge** (UM3038 tab. 2: 4×4 1–60 Hz, 8×8 1–15 Hz [g]); sincronia L8CX: **regge** (driver 1.3.0 [g]); sincronia L7CX: **non risolta** | scheda Rev 6: nessun piedino SYNC, B1 è AVDD [g]; driver 1.2.3: nessuna funzione [g]; una libreria di terzi elenca la funzione su «B1» [r]. La decide la scheda ST più recente o il sensore in mano. |
| L6 | **regge**, ed è peggio del previsto | senza trigger servono start e stop con almeno 2 fotogrammi per sensore (il primo ha stato 6 o 10, UM3038 tab. 4 [g]): 400 ms a giro, 2,5 Hz per sensore (conto E). |
| L7 | **regge** per la soglia a 0,5 m | 0,36 s lordi; 0,29 s dopo un campione; 0,22 s dopo due; 0,07 s dopo la latenza del nucleo; il segnale di 0,3 s finisce 0,23 s dopo il contatto (conto A). |
| L8 | **regge** | 267° su 360°; fessura di 16,5° per lato con gli assi a ±90° (conto B). |
| L9 | **regge** (estrapolazione, non misura) | nero 5 %: 0,38 m al buio e 0,30 m a 5 klx in 8×8; a 2,5 m manca un fattore 6,5 (conto D, ancorato alle tabelle 17 e 18 [g]). |
| L10 | **non risolta** | nessuna fonte primaria aperta quantifica i buchi sul nero; la guida RealSense dice solo che i buchi valgono 0 e che il preset «High Accuracy» evita le profondità inventate [r]. Decide la prova T4 sulla camera. |
| L11 | **regge** | 6,5 % dei pixel e 13,1 % delle direzioni a 2,5 m; 25,5 % e 32,3 % a 1 m; oltre il 50 % solo sotto 0,63–0,75 m (conto C). |
| L12 | **regge** | indirizzo 0x52 e procedura con LPn: UM3038 §2.3 [g]; firmware «~84 kbytes» (86 016 byte nel driver) [g]. |
| L13 | come previsto | vedi `CONSEGNA.md`. |

Bracci di controllo: soglia a 2 m → 1,36 s (oltre 1 s: il conto non è cieco); sagoma a 0,4 m → 73,6 % (oltre il 50 %).

**Notato dopo, non previsto:** (a) l'atto 1 della demo (metà campo coperta) sta esattamente sulla soglia del 50 %: una
persona in nero a 2,5 m porta i validi al 43,5 %; (b) nei documenti ST «crosstalk» è il riflesso del vetro di copertura,
non il disturbo fra sensori; (c) su un bus a 400 kHz la lettura completa di tre sensori dura 98 ms, più del periodo di
67 ms; (d) a 5 klx tre VL53L7CX aggiungono l'1,4 % del disco di 3 m, non il 22,2 % scritto nel nucleo (che vale al buio
sul bianco); (e) chi passa a 0,5 m di lato entra nel campo della camera a 0,73 m, dentro l'anello cieco; (f) con soglie
di 1–1,5 m (L7CX in 4×4 senza luce diurna, L8CX in 4×4) il margine torna a 0,49–0,85 s: il giudizio «etichetta» vale per
la soglia a 0,5 m, non per l'idea.
