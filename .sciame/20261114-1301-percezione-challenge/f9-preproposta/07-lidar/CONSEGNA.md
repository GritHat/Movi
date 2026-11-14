# sciame-lidar, f9: strategia S9 e attacco 4 della preproposta esterna

14 novembre 2026. Previsioni L1–L13 scritte alle 15:40:23, prima di ogni scheda e di ogni conto: `PREVISIONI.md`
(11 reggono, 2 non risolte, nessuna smentita). Conti: `conti_s9.py` → `risultati_conti_s9.txt`
(`timeout 120 python3 -I conti_s9.py`, deterministico). Marche: **[g]** dato cercato nel testo scaricato
(`scaricati/`); **[r]** letto dallo strumento che riassume le pagine (più debole).

## 0. Scostamenti e regole violate

- **Nessuna misura su un sensore vero:** tutto ciò che segue è scheda, conto o estrapolazione dichiarata.
- Un comando `curl` verso st.com con intestazioni da browser (dopo due timeout) è stato **negato dal controllo dei
  permessi** della sessione; non l'ho aggirato. I documenti ST sono letti nelle copie di Pololu e di GitHub
  (stm32duino): revisioni DS13865 Rev 6, DS14161 Rev 7, UM3038 Rev 2, forse non le ultime. I primi scaricamenti
  usavano l'agente utente generico «Mozilla/5.0».
- Scaricati 17 MB in `07-lidar/scaricati/`, mai eseguiti. Non ho tenuto `stato.md`. File in più oltre la consegna:
  i due script e i loro risultati.
- Indipendenza: condivido modello e ruolo con la consegna f1 (`f1/985ccd9bca46`); vale solo il testo delle fonti.

## 1. Verdetti proposti

**S9 — approvata con correzioni, e in tre parti.**
- Come **canale laterale facoltativo di sola prossimità** (mai «libero», mai tracce): **approvata**, fuori dal taglio
  a 24 ore, come già diceva il v0.5.
- Come **«preallarme» con VL53L7CX e soglia a 0,5 m: respinta.** Controesempio (conto A): a 1,4 m/s restano 0,36 s
  lordi, 0,29 s dopo un campione a 15 Hz, 0,22 s dopo i due campioni che servono (il primo dopo un «nessun bersaglio»
  ha stato 10, fiducia sotto il 50 %, UM3038 §5.5 [3, g]), **0,07 s** dopo i 155 ms di latenza del nucleo; il segnale di 0,3 s
  finisce 0,23 s dopo il contatto. Su grigio 17 % a 5 klx la portata tipica in 8×8 è 0,35 m (minima 0,25 m, tab. 18
  [g]): margine negativo. A 2,5 m/s (v_max del nucleo): negativo.
- Il **rimedio «accensione alternata»: respinto sul VL53L7CX**, e non necessario (critiche 2 e 3).

**Attacco 4, prima metà (diafonia infrarossa) — da provare sull'hardware; la premessa è smentita sulle carte.** Le
due sorgenti non sono la stessa luce: proiettore RealSense D43x/D45x 850 ± 10 nm, 360 mW massimi, campo 90° × 63° [4,
g]; Gemini 335 850 ± 6 nm [5, g]; VL53L7CX e L8CX 940 nm [1][2, g]. La decidono le prove T1–T3 (§4), cinque minuti.

**Attacco 4, seconda metà (tessuto nero) — criterio (b) regge per conto; criterio (a) per costruzione sui buchi, da
provare sull'hardware per le profondità sbagliate.** (b) Una persona in nero (0,5 × 1,7 m) vista tutta come buco toglie
il **6,5 % dei pixel** (13,1 % delle direzioni, 3,7 % delle celle fra 1,24 e 3 m) a 2,5 m e il **25,5 %** (32,3 %) a
1 m: lontano dalla soglia del nucleo (validi sotto il 50 % della taratura per 3 fotogrammi). La supera da sola solo
sotto 0,63 m (0,75 m se larga 0,6 m): lì «affidabilità persa» è l'uscita giusta. Controllo: a 0,4 m il conto dà 73,6 %.
(a) Un buco è già «non osservato» nel nucleo (B2, invariante 2), purché i filtri che riempiono siano spenti (audit f5).

## 2. Critiche

1. **Filtri e verso della diafonia.** *Proiettore → tempo di volo:* la banda del filtro a 940 nm non è nella scheda
   [1, g]; un dipendente ST scrive «940 +/- 10nm is what we are shooting for. But the filter is not absolute» [8, r].
   Il proiettore non è correlato con gli impulsi del sensore: se passa, è **luce di fondo** (meno portata, più
   rumore), non «ostacoli fantasma ai bordi». Limite superiore, se il filtro non respingesse niente (conto F): a 1 m
   0,10–0,24 W/m², cioè il 5–12 % dei 2 W/m² che ST usa per «5 klx»; a 0,5 m il 20–48 %. Con i sensori di lato (assi a
   ±90°: coprono 60°–120°) il campo del proiettore (±45°) **non li tocca**: resta la luce riflessa. *Tempo di volo →
   camera:* gli imager non hanno filtro («Filter Type: None», «Depth Filter: All pass» [4, g]; Gemini 335 «All-Pass»
   [5, g]) e vedono i 940 nm, ma è luce diffusa senza trama: non può creare disparità. Innocuità **non verificata**.
2. **L'accensione alternata non si fa con questi sensori.** Il VL53L7CX non ha ingresso di trigger nella scheda Rev 6
   (B1 è AVDD [1, g]) né nel driver 1.2.3 [6, g]. Alternare con start e stop: almeno 2 fotogrammi per sensore,
   400 ms a giro, **2,5 Hz** (conto E): il margine diventa −0,04 s già prima della latenza. Il VL53L8CX ha il piedino
   SYNC, solo in modo autonomo [6, g][9, r]: non provato qui.
3. **Fra i tre sensori laterali.** ST: ciascuno vede gli altri «as ambient light»; il disturbo compare se si guardano
   in faccia da vicino o puntano allo stesso bersaglio riflettente, come **bersaglio in più con stato non valido**
   [7, r]. Con assi a 60° o più l'uno dall'altro i campi non si sovrappongono. Rimedio: geometria e filtro sullo stato
   (5 e 9), non l'alternanza.
4. **Che cosa danno tre VL53L7CX.** Camera 87° + 3 × 60° = 267° su 360°; con gli assi a ±90° restano **16,5° ciechi
   per lato** fra camera e sensore, proprio da dove entra chi «arriva di fianco». A 5 klx aggiungono l'**1,4 %** del
   disco di 3 m (0,7 % sul grigio), non il 22,2 % scritto nel nucleo, che vale al buio sul bianco. Chi passa a 0,5 m di
   lato entra nel campo della camera a **0,73 m**, dentro l'anello cieco (suolo visto da 1,24 m): il «passaggio di
   consegna» alla traccia frontale non avviene mai nella zona valutata (conto B).
5. **Nero e tempo di volo.** Estrapolando le tabelle 17–18 [1, g] (esponente 0,60 al buio): nero al 5 % in 8×8 →
   **0,38 m al buio, 0,30 m a 5 klx**; a 2,5 m manca un fattore 6,5: il sensore restituisce «nessun bersaglio» (stato
   255), che **non è «libero»**. La soglia di 0,5 m non è raggiunta su una persona in nero nemmeno al buio. La
   riflettività del tessuto a 940 nm è un'ipotesi.
6. **Nero e camera stereo: non verificato.** L'esito atteso sono buchi (profondità 0), ma con un preset denso lo
   stereo può inventare profondità; il costruttore: «false depth, aka. Hallucinations, are much worse than no depth»,
   preset «High Accuracy» [10, r]. Il caso pericoloso è uno solo: un raggio che colpisce le gambe a 0,1–0,2 m di quota
   e riceve la profondità del pavimento retrostante darebbe «suolo visto» a 2,73–3,0 m (conto C). Molti tessuti neri
   riflettono nel vicino infrarosso: senza la camera non si decide (era la mia P10 di f1, mai eseguita).
7. **Notato dopo:** l'atto 1 della demo (metà campo coperta) sta **sulla soglia** del 50 %: con una persona in nero a
   2,5 m i validi scendono al 43,5 % e scatta «affidabilità persa» invece di «sconosciuto» per settore. Va deciso se
   la taratura si fa prima o dopo la copertura.
8. **Ripiego «solo prossimità».** Con la camera guasta il sistema può dire solo: «affidabilità persa; davanti non
   osservato; a sinistra / a destra qualcosa entro X m», dove X è la portata misurata con la luce di quel momento.
   Non può dire «libero», non segue oggetti, non prevede, e il silenzio non significa assenza (nero: 0,3 m). Non è un
   ripiego della funzione: è un avviso residuo.

## 3. Dove la preproposta ha letto male

- **«Cross-talk IR rilevato»** è dato come una condizione che il selettore riconosce: nessuno l'ha misurata, e il
  nucleo la tiene «non verificato» (`SOLUZIONE_V2.md` §8). Nei documenti ST «crosstalk» è il riflesso del **vetro di
  copertura** sul ricevitore [1, g], non il disturbo fra sensori: nome onesto, «interferenza fra sorgenti».
- **«VL53L7CX/L8CX»** come intercambiabili: 60° contro 45°; a 5 klx in 8×8 0,5 m contro 1,55 m; SYNC solo sull'L8CX,
  che chiede anche 1,8 V per il nucleo [2, g].
- **«Early-warning flank guard», «cueing»:** il v0.5 dice «canale laterale di sola prossimità (non provato)». Il
  prestito promette un passaggio di consegna che la geometria esclude (critica 4): nome onesto, «avviso di prossimità
  laterale».
- **«Disabilita T_lat oltre 0,5 m»:** a 5 klx 0,5 m è il tipico sul bianco; sul grigio 17 % 0,35 m, minimo 0,25 m.
- **«< 1,1 m»** nel v0.5 è una **distanza dal sensore** (ostacolo di 15 cm non visto sotto 1,09 m), non una quota. Un
  sensore puntato in basso da 1,2 m d'altezza vede il suolo dell'anello cieco a 1,3 m o più: fuori portata per
  l'L7CX in 8×8 sul grigio (0,8 m al buio). Va montato basso, o serve un L8CX.
- Letto bene: i sensori laterali stanno nell'estensione a 38 ore, come nel v0.5.

## 4. S9 corretta

1. **Nome e uscita:** «avviso di prossimità laterale». Dice solo «presenza a sinistra / a destra entro X m». Nessun
   ritorno → «non osservato». Non crea tracce, non entra nel filtro, non cambia la mappa frontale.
2. **Sensore e modo:** per dare almeno 0,5 s a 1,4 m/s serve rilevare a 1,4 m o più: **VL53L8CX in 4×4 a 30 Hz**
   (grigio 17 % a 5 klx: 1,65 m tipici [2, g]; margine 0,85 s con soglia a 1,5 m). Con i VL53L7CX: 4×4 a 30 Hz, soglia
   a 1,0 m **solo senza luce diurna** (1,4 m al buio sul grigio; margine 0,49 s), altrimenti «canale non disponibile».
   Modo continuo, un bersaglio per zona, stati 5 e 9, due fotogrammi di fila.
3. **Portata dichiarata dalla luce misurata:** X si legge da una tabella tarata sul posto in funzione di
   `ambient_per_spad`, su un bersaglio grigio e uno nero. Niente soglia fissa.
4. **Niente alternanza.** Assi a 60° o più fra loro e fuori dal campo del proiettore; se T1 mostra un danno, il
   rimedio è il puntamento.
5. **Prove in cinque minuti** (previsione scritta ora: nessun effetto oltre le soglie nel montaggio laterale).
   **T1**, sensore vittima: parete opaca a 0,4 m dentro il campo del proiettore, 8×8 a 15 Hz, blocchi di 30 s A-B-A-B
   con proiettore spento e a 360 mW; diafonia presente se la mediana di `ambient_per_spad` sale più di 3 scarti o del
   10 %, dannosa se le zone valide calano di più di 2 su 64 o la distanza mediana si sposta più dell'1 %; poi nel
   montaggio vero. **T2**, camera vittima: parete bianca a 1 m, sensore acceso e spento; soglia: 1 punto di
   riempimento o 10 % di rumore sul piano. **T3**, fra sensori: due affiancati sulla stessa parete e poi montati;
   conta dei bersagli in più. **T4**, nero: persona in nero a 1 e a 2,5 m, filtri spenti, preset predefinito e «High
   Accuracy», 150 e 360 mW; quota di pixel validi nella sagoma, scarto dal metro, e **0 celle «libero» dietro la
   sagoma in 100 fotogrammi**; la quota globale non deve far scattare «affidabilità persa».

## 5. Costo

- **Ore:** circa **9 ore-persona** per chi ha già usato l'I2C (un sensore 2; tre con gli indirizzi 1,5; ponte seriale
  verso il PC 1,5; soglia dalla luce 1,5; montaggio e taratura su tre bersagli 1,5; uscita e T1–T3 1), più
  l'hardware: tre schedine, un microcontrollore con almeno 100 kB di memoria di programma (il firmware da caricare è
  di 86 016 byte per sensore a ogni avvio [6, g]), tre piedini per LPn. **T4 da sola: 1 ora, e serve comunque.**
- **Stesso indirizzo (0x52):** procedura ST (UM3038 §2.3 [3, g]): LPn basso sugli altri, `set_i2c_address()` su uno
  alla volta, a ogni accensione; oppure un multiplatore I2C. Bus a 1 MHz: a 400 kHz il firmware chiede 5,8 s per tre e
  la lettura completa 98 ms per tre, più del periodo di 67 ms (ridotta: 40 ms).
- **Calcolo per ciclo:** 6,9 µs sul PC in Python puro (`costo_ciclo.py`, misura indicativa), cioè niente.
- **Che cosa si taglia:** niente dal nucleo. S9 entra per ultima nell'estensione a 38 ore e cade per prima.

## 6. Non verificato

Banda e reiezione del filtro a 940 nm; potenza ottica dei VL53; sincronia sul VL53L7CX (una libreria di terzi elenca la
funzione su «B1» [11, r], la scheda Rev 6 no); tempi di start e stop; riflettività dei tessuti a 850 e 940 nm; buchi o
profondità sbagliate sul nero; portata oltre 5 klx (le schede non caratterizzano il sole); somma degli emettitori di
classe 1 verso lo stesso occhio; revisioni più recenti delle schede ST.

**Fonti (aperte oggi).** [1] https://www.pololu.com/file/0J1992/vl53l7cx.pdf · [2]
https://www.pololu.com/file/0J2029/vl53l8cx.pdf · [3]
https://www.pololu.com/file/0J1993/um3038-a-guide-to-using-the-vl53l7cx-timeofflight-multizone-ranging-sensor-with-90-fov-stmicroelectronics.pdf
· [4] https://www.realsenseai.com/wp-content/uploads/2026/03/RealSense-D400-Series-Datasheet-Mar-2026.pdf · [5]
https://download.kamami.pl/p1203693-Gemini-330-series-Datasheet-V1.6.pdf · [6] https://github.com/stm32duino/VL53L7CX
e https://github.com/stm32duino/VL53L8CX · [7]
https://community.st.com/t5/imaging-sensors/will-multiple-tof-sensors-vl53l-series-specifically-in-close/m-p/61090 e
https://community.st.com/t5/imaging-sensors/vl53l5cx-mutual-influence-of-multiple-sensors/td-p/197217 · [8]
https://community.st.com/imaging-sensors-49/vl53l5cx-emitter-940nm-light-11515 · [9]
https://community.st.com/imaging-sensors-49/external-trigger-155090 · [10]
https://dev.realsenseai.com/docs/tuning-depth-cameras-for-best-performance · [11]
https://components.espressif.com/components/grrtzm/v53l7cx-library/versions/1.0.6/examples/example_02_get_set_params
