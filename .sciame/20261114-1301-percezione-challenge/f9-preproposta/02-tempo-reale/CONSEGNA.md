# Consegna `tempo-reale-f9` — S1, S2, attacco 3, bilancio del ciclo (f9, 14 novembre 2026)

## 0. In testa: scostamenti e regole violate

- **Verdetti proposti:** S1 **approvata con correzioni** (resta la forma ridotta; il cambio di risoluzione della griglia in esercizio è **respinto**; le soglie sono **da provare sull'hardware**). S2 **approvata con correzioni**. Attacco 3 **eseguito**: la preproposta, com'è scritta, non lo supera. Nessun cambio di stato sul nucleo.
- **Scostamenti.** (a) P10 è stata scritta dopo la prima prova del selettore, ed è marcata così in `PREVISIONI.md`. (b) Per un errore mio la shell ha provato a eseguire due nomi di file come comandi («command not found», nessun effetto); il testo di `PREVISIONI.md` è stato ripristinato a mano, con nota. (c) L'eseguibile del banco in C sta nella cartella temporanea della sessione. (d) `SOLUZIONE_V2.md`, `VERDETTO.md` e `VERIFICA.md` letti per `grep`, non per intero. (e) Il modello del tempo per ciclo è un'ipotesi mia, non una misura.
- **Previsioni (scritte alle 15:40:57, prove dalle 15:43).** Reggono P1, P2, P3, P6, P7, P9 e, di misura, P10. P4 regge solo nello scenario con le punte (senza punte tutti stanno sotto lo 0,03 %). P5 regge sulla soglia, ma il valore atteso era sbagliato (previsto ≤ 1 cambio al minuto, misurati 6,8–8,6). **P8 è smentita per metà:** in Python puro il ritaglio costa 7,4 ms, non ≥ 20.
- **Indipendenza.** Simulatori, banchi e conti sono miei: condividono con ciò che controllano autore, modello linguistico e il modello del carico. Valgono per i difetti di logica e per gli ordini di grandezza, non per i tempi veri. Macchina delle prove: portatile Ryzen AI 9 HX 370, altri processi attivi; **non è la macchina di destinazione**.

## 1. S1, selettore della configurazione — approvata con correzioni

**Attacco 3, simulazione** (`sim_selettore.py`, 20 semi × 10 min, periodo 66,7 ms, 900 cicli al minuto). Tempo della configurazione piena centrato su 55 ms: deriva lenta σ 2 ms, rumore σ 3 ms, punte sull'1,5 % dei cicli, salti di ±8 ms. La configurazione ridotta costa Δ = 12 ms in meno. Selettore a circa 2 Hz (ogni 8 cicli) sulla media di 15 cicli.

| Variante | Cambi/min | Cicli oltre 66,7 ms | Tempo in piena |
|---|---|---|---|
| A. una soglia (55), nessuna isteresi | 46,7 | 1,81 % (16,3/min) | 75 % |
| B. isteresi proposta (un cambio ogni 2,5 s) | 17,5 | 1,85 % (16,7/min) | 61 % |
| C. due soglie 45 / 55 | 25,8 (Δ = 5: 3,2; Δ = 20: 38,3) | 1,03 % | 57 % |
| C + B | 14,6 | 1,16 % | 55 % |
| D. corretto (sotto) | 0,2 | 0,50 % (4,5/min) | 0,6 % |
| sempre piena / sempre ridotta | 0 / 0 | 3,29 % / 0,50 % | 100 % / 0 % |

**Critiche.**

1. **L'isteresi temporale non ferma l'oscillazione: ne fissa il ritmo.** 17,5 cambi al minuto per sempre (tetto 24), con gli stessi sforamenti di chi non ha isteresi (1,85 contro 1,81 %). Il criterio dell'attacco 3 chiede un meccanismo («deve includere isteresi») e sarebbe formalmente soddisfatto. Va riscritto come esito: al più 2 cambi al minuto con il carico sulla soglia.
2. **La causa è l'anello chiuso:** il selettore misura un tempo che lui stesso cambia. Due soglie reggono solo se il modulo spento costa meno della banda, cioè 10 ms: 3,2 cambi/min con Δ = 5, ma 25,8 con Δ = 12 e 38,3 con Δ = 20. Il rilevatore su CPU citato dal nucleo costa 38,9 ms (`SOLUZIONE_V2.md`, r. 122). La risalita deve usare il **costo previsto della configurazione d'arrivo**, non il tempo di quella attiva.
3. **La media è la misura sbagliata.** La scadenza è per ciclo. Una configurazione «certificata» a 55 ms di media sfora il 3,29 % dei cicli (2,2–7,2 % al variare del rumore da 1,5 a 6 ms). Con media 50 ms e code sul 4 % dei cicli il selettore non reagisce (1,3 cambi/min) e gli sforamenti restano al 2,6 %. Servono il conteggio degli sforamenti e un percentile alto su una finestra.
4. **Le soglie rispetto a 66,7 ms.** 55 ms lasciano 11,7 ms (17,5 % del periodo): bastano solo se il 99° percentile del tempo per ciclo sta sotto, e quel numero non esiste. Fra 45 e 55 ms la tabella non ha riga. «GPU ⇔ meno di 30 ms» confonde una scoperta dell'hardware con un tempo. Nulla dice che cosa accade a uno sforamento.
5. **Cambiare la risoluzione della griglia in esercizio: respinto** (`sim_griglia.py`; strato 1 di 1548 celle, 5,03 m²).
   - Riallocare e azzerare toglie il 100 % della possibile presenza: viola il principio.
   - Ricampionare «al centro» perde 23 celle (0,051 m²) a fattore 2 e 83 (0,200 m²) a fattore 4, tutte sul bordo, cioè nella fascia il cui margine residuo è «meno di 10 cm».
   - Il modo conservativo ne perde 0 e gonfia del 2,2 % (6,3 % a fattore 4), una volta sola se le griglie sono allineate. Se l'origine si sposta, in 10 giri l'area cresce del 35 %.
   - A ogni cambio le storie a 3 fotogrammi ripartono: 0,2 s di mappa «non osservata». Con 17,5 cambi/min sono 3,5 s al minuto (conto).
   - **Non fa risparmiare:** la griglia ha 2640 celle, il costo sta nei 407 040 pixel (§3).
6. **P10, carico a fasi di 60 s (42 / 58 ms).** D risale: 36,4 % del tempo in piena, 1,7 cambi/min, 0,50 % di sforamenti; B: 74,6 %, 11,5 cambi/min, 0,96 %. Nello scenario dell'attacco D coincide con «sempre ridotta»: se la piena sta a 55 ms, la risposta giusta è non usarla.
7. **Non eseguito:** la variante «luce che varia rapidamente». La decide una lampada accesa e spenta a 0,5 Hz per 60 s sull'hardware, contando i cambi.

**Versione corretta (`tempo-reale-f9-1`).**
- **All'avvio:** scoperta dell'hardware; 5 s di fotogrammi veri per ogni configurazione ammessa, con mediana, 99° percentile e massimo. Si sceglie la più ricca con 99° percentile ≤ 55 ms e si registra il costo Δ di ogni modulo.
- **In esercizio una sola leva:** i moduli facoltativi (rete a lato, sensori laterali). Griglia, fasce e stati delle tracce sono fissi per la sessione. Lo strato 1 è tenuto come geometria (intervallo d'angolo, portata, fascia), non come celle.
- **Discesa immediata** con 2 sforamenti negli ultimi 15 cicli, o con il secondo massimo degli ultimi 30 oltre 60 ms. **Risalita** solo dopo 10 s e con 95° percentile su 10 s più Δ sotto 55 ms. Dopo 3 discese in 5 minuti resta ridotta fino al riavvio.
- **Allo sforamento:** coda di profondità 1 con l'ultimo fotogramma, intervallo del filtro dalle marche, soglie in secondi, contatore in uscita. Ogni cambio è scritto a schermo.
- **Nome:** «selettore a regole», non «AI Selector». È una tabella, e il progetto dichiara che nessun modello appreso decide.

## 2. S2, compensazione della latenza — approvata con correzioni

**Simulazione** (`sim_latenza.py`, 500 semi; filtro del nucleo q = 0,2, σ 3,4 cm, 15 Hz, latenza vera 155 ms). Errore della posizione mostrata rispetto al vero nell'istante in cui compare.

| Uscita | 1,4 m/s: media / RMS | 2,5 m/s: media / RMS | Picco all'arresto brusco (1,4 m/s) |
|---|---|---|---|
| non compensata | −0,217 / 0,218 m | −0,387 / 0,388 m | 0,074 m |
| compensata, latenza esatta | 0,000 / 0,034 m | 0,000 / 0,034 m | **0,240 m** (95° perc. 0,294); oltre 0,10 m per 0,33 s |
| latenza sbagliata di ∓30 ms | ∓0,042 / 0,052–0,056 m | ∓0,075 / 0,081–0,084 m | 0,203 – 0,279 m |
| marca d'arrivo (misura solo 22 ms) | −0,186 / 0,188 m | −0,332 / 0,333 m | 0,092 m |

**Errore residuo chiesto, con 30 ms di errore sulla latenza:** 0,042 m a 1,4 m/s e 0,075 m a 2,5 m/s (conto v·δ, confermato dalla simulazione).

**Critiche.**

8. **È corretta nel moto uniforme:** toglie un ritardo sistematico di 0,22 m (0,39 m a 2,5 m/s). Va fatta su una **copia d'uscita**; il filtro interno resta all'istante di cattura.
9. **All'arresto va oltre il vero.** Il picco è 0,24 m (0,42 m a 2,5 m/s; 0,18 m con frenata a 3 m/s²), mentre l'incertezza dichiarata dell'uscita è 5,0 cm: 4,8 volte di meno. La «precisione dichiarata» è falsa nelle manovre, proprio dove conta la sosta.
10. **Non compensa l'età delle celle «libero»,** né gli oggetti senza traccia (prima della conferma, 0,2–0,33 s), né ciò che esce da un'ombra. Il limite dell'audit resta: 0,40 / (0,133 + 0,155) = 1,39 m/s. S2 fornisce solo la latenza misurata da mettere nella formula della fascia, v_max · (età + latenza).
11. **A ogni ciclo o una volta?** Tutte e due. Il tratto dalla marca di cattura alla chiamata d'uscita si misura a ogni ciclo, e per la fascia si usa il suo 95° percentile. I due estremi (dentro il sensore; dalla chiamata al suono o allo schermo, almeno 21,3 ms di audio) si stimano una volta, con il telefono a 240 fps. «t_now» della preproposta ignora il secondo estremo.
12. **Che cosa serve dalla camera.** La marca di metà esposizione nell'orologio dell'ospite. In librealsense è `SENSOR_TIMESTAMP` («middle of sensor's exposure») nel dominio `GLOBAL_TIME` (orologio della camera convertito in quello del sistema): https://github.com/IntelRealSense/librealsense/blob/master/include/librealsense2/h/rs_frame.h (aperta; citazione come la riporta lo strumento di lettura). Su Linux i metadati chiedono un modulo del kernel modificato: https://github.com/IntelRealSense/librealsense/blob/master/doc/frame_metadata.md (aperta; cita nuclei vecchi, lo stato di oggi è non verificato).
13. **Se la marca è quella d'arrivo** si compensano 22 ms su 155: restano 0,19 m a 1,4 m/s e 0,33 m a 2,5 m/s, e l'età dichiarata è falsa (circa 22 ms invece di 155), cioè peggio che non dichiararla. In più il tremolio d'arrivo entra nell'intervallo del filtro: 5 ms su 66,7 sono il 7,5 % della velocità (conto).
14. **Contraddizione interna:** il §2.4 della preproposta scrive «età dato 0 ms» per «visto». Nessun dato ha età zero: va mostrata l'età misurata.

**Versione corretta (`tempo-reale-f9-2`).**
- All'avvio si stampa il dominio della marca. Se non è quello dell'hardware: scarto fisso dichiarato, incertezza allargata e avviso a schermo.
- Si mostra il punto compensato **e** il tratto fra posizione stimata e posizione compensata («striscia di latenza»). Le regole usano l'estremo più prudente.
- Età negativa o oltre 250 ms: «affidabilità ridotta».
- **Previsione:** la striscia allargata di 2σ contiene il vero in almeno il 95 % dei cicli, arresti compresi. **Smentita** se la copertura sugli arresti scende sotto il 90 %. Non simulata.

## 3. Bilancio del ciclo con tutti i moduli accesi

Conto: 10 tracce × 2 ipotesi × 2640 celle = 52 800 valutazioni di una gaussiana per ciclo, nel caso peggiore.

| Stadio (un filo) | C -O2: mediana / 99° / massimo | Python puro, mediana |
|---|---|---|
| due ipotesi, ritaglio, pesi, massimo avvicinamento, volume protetto, macchina a stati; griglia intera | 0,176 / 0,185 / 0,477 ms | 7,4 ms (solo ritaglio e pesi) |
| lo stesso, riquadro a 3σ con σ 0,3 m | 0,056 / 0,069 / 0,093 ms | 2,25 ms |
| proiezione 848×480 sulla griglia (stadio del nucleo) | 2,91 / 2,97 / 3,00 ms | circa 161 ms (stima ×16) |

I moduli della preproposta valgono lo 0,3 % del periodo in C e l'11 % in Python puro: **non sono loro a minacciare i 15 Hz.** Li minaccia lo stadio dei pixel, 16 volte più caro. In Python senza vettorizzazione non sta nel periodo; con numpy è non verificato (non installato). Rifare: `gcc -O2 -o banco banco_ciclo.c -lm && timeout 120 ./banco`; `timeout 120 python3 banco_ciclo.py`.

## 4. Dove la preproposta ha letto male

- **«< 1,1 m»** è una distanza dal sensore (zona cieca vicina: `proposta_sciame.tex`, r. 125 e 189), non un'altezza. Nessuna mappa, nemmeno voxel, la «copre».
- **«Interrompe la previsione a 0,5 s»:** nel nucleo non c'è un timer; «previsto» dura finché il cerchio copre meno di metà del cuneo.
- **«155 ms stimati»:** è la somma delle sole voci note, in media, da un documento su un'altra camera in un altro modo (`VERIFICA.md` §3c). Il requisito è «non risolto».
- **«Preserva i ≥ 15 Hz»:** nel v0.5 i 15 Hz sono «aperto: da misurare» (r. 130).
- **La rete a lato** nel nucleo è asincrona, e se manca la catena non cambia. Spegnerla aiuta solo se contende i processori: non misurato.

## 5. Costo, non verificato, che cosa dopo

- **Ore (stime mie, non verificate).** S1 ridotta: 2 h. S1 completa (sonda del contesto, sei righe, ogni transizione da provare): almeno 8–10 h, **fuori** dal piano a 24 ore. S2: 2 h, più 1 h di misura. **Calcolo per ciclo:** S1 e S2 non misurati a parte; S2 è una previsione per traccia, dello stesso ordine di quelle dentro il banco.
- **Non verificato.**
  - Ogni tempo sulla macchina di destinazione, e la forma vera del tremolio.
  - Il dominio della marca che D455, D435i e Gemini 335 danno sul Linux della squadra; che cosa fa librealsense senza metadati (letto solo il riassunto di una ricerca); la Gemini 335 non è stata controllata.
  - Lo scarto fra la marca e la vera metà esposizione; la latenza d'uscita.
  - La striscia di latenza; D fuori dal mio modello.
- **Dopo, sull'hardware (circa 40 minuti):** 60 s a vuoto e 60 s sotto carico con il tempo di ogni ciclo registrato (decide la soglia di 55 ms e il Δ dei moduli); stampa del dominio della marca; telefono a 240 fps su 20 eventi (decide la latenza e la velocità coperta dalla fascia).

**File, in questa cartella:** `PREVISIONI.md`, i quattro `sim_*.py`, `banco_ciclo.c`, `banco_ciclo.py`, i sei `risultati_*.txt`.
