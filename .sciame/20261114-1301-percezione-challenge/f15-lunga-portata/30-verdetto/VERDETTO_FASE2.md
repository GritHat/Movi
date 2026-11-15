# Verdetto sulla seconda fase: veicoli veloci e sensori a lunga portata (f15, f16)

`sciame-arbitro`, 2026-11-15, dalle 01:39 alle 01:50 (`date -Is`; la consegna dice 14 novembre). Previsioni e soglie
scritte prima dei riconti alle 01:39:08, in `PREVISIONI.md`. Riconto: `riconto.py` → `riconto_esito.txt`, nella
cartella. Il programma rilegge `11-prove/risultati_lp_{interfaccia,prudente}.json`, `risultati_eventi.json` e
`21-statistica/compara.json`, e ricalcola i Wilson con codice mio.
**Tutto è simulazione dalle schede tecniche, conto, o traiettoria pubblica reale con rumore e occlusione simulati.
Nessun sensore fisico, niente è «validato».** Le etichette di classe sono messe a mano. Il lavoro riguarda solo
osservazione e avviso.

**Ricontato e adottato:** T1 e T2 di 11-prove (tempestività, passaggi senza regione, «libero» sull'oggetto), E1–E5,
e le coperture e i «fuori avviso» per mezzo. Ogni k/n ritrovato è uguale, e i Wilson coincidono entro 0,001.
**Non ricontato, e adottato solo con il rinvio al file:** T3 e T4 (precisione, falsi avvisi, costo, ritardi), gli
attacchi X1–X7 (`20-attacco/attacchi_esito.json`, `limite_*.json`), le portate del «libero» (04-moto), L1 e L3 del
prototipo. Di L1 e L3 ho letto le code dei file `prototipo/uscite/lunga/prova_L*.txt`: 17 file su 17 «UGUALE», e
228 cicli su 228 per L3. Il collaudo `f16-prototipo/30-collaudo` era **in corso** mentre scrivevo: non è coperto.

## 1. In testa: cambi di stato rispetto al verdetto d'integrazione

1. **Limite di scala.** Il verdetto d'integrazione diceva: «3 m, tempestivo per calcolo fino a 1,44 m/s» (enunciato
   15). Ora cambia così.
   - **Per i droni e i mezzi di terra lenti: da «fuori portata» a «sostenuto in simulazione da scheda».**
     - Multirotore a 15–21 m/s (A1, radar per droni): avviso tempestivo per l'operatore di sito, che lo chiede a
       806 m. La traccia è confermata a 949 m di mediana (p5 928 m), con 200/200 passaggi [0,981; 1].
     - Aereo in rullaggio (A2, radar di superficie + LiDAR + ADS-B): 147 m richiesti, 200/200.
     - Auto (S1, 13,9 m/s): 67 m richiesti, 200/200.
     - Treno in stazione (S2, 16,7 m/s): 261 m richiesti, solo **186/200 [0,886; 0,958]**. È parziale secondo la mia
       soglia (limite inferiore ≥ 0,90).
     - In sintesi la portata passa da 3 m a circa 1 km (più di due ordini di grandezza) e la velocità da 1,44 a circa
       21 m/s (un ordine di grandezza). La previsione 4 regge per i droni. Per le auto è **non risolta**, perché lo
       scenario arriva al più a 13,9 × 1,2 m/s.
   - **Per gli aerei in volo (70–210 m/s): non provato, e in parte smentito.**
     - A3 non misura la tempestività: lo scenario parte a 2,5 km e ne servono 3,9. Lo 0/200 vale per costruzione.
     - Con v_max 210 m/s (X3) l'operatore di sito ha bisogno di 3410 m, mentre il «libero» del multirotore arriva a
       2360 m: **non tempestivo**.
     - **Treno ad alta velocità** (macchinista, 7,57 km): no, per conto (04-moto § 4).
2. **«La prima prova da fare»: eseguita, esito non risolto.** È la regione di previsione dentro la catena, su
   profondità simulata (prototipo f16/10, `RIASSUNTO.txt`).
   - Le garanzie reggono: 0 cicli nascosti senza regione né avviso su 5820 [0; 0,001], e 0 celle «libere»
     nell'ombra vera su 3 062 304.
   - Sui passaggi interi, ciò che è mostrato contiene la persona a 2 s in 59 casi su 84 [0,60; 0,79] e a 3 s in 30
     su 60 [0,38; 0,62]: **smentita**. Il motivo è che la persona esce dai 3 m. Entro i 3 m regge: 59/59 e 30/30.
   - La regione **stretta** dura meno di 0,5 s. Su di essa n vale 0 o 1 a ogni orizzonte: **non risolta** (sv-P4b).
   - Il livello del 90 % non è tenuto: 23 su 39 in a05 e 189 su 227 in d, fotogrammi correlati. Per questo ora il
     registro porta `livello_verificato: false`.
   - A lunga portata la regione è provata fuori dalla catena. Sulle traiettorie si usa `Traccia`, senza
     associazione. Nel simulatore la precisione è **smentita** in S1 (≤ 0,67) e in A3 min a 2 s (32/42).
3. **Nuova smentita di principio, con l'interfaccia di `mancato()` del nucleo.** L'avviso si spegne senza che si sia
   guardata tutta la zona in **564 passaggi su 2400 [0,218; 0,252]**. Con la chiamata «prudente», che è la regola
   corretta e anche quella predefinita del prototipo, sono **0 su 600 [0; 0,006]**: 0 su 50 per riga, ≤ 0,071 per
   riga. Il nucleo `movi_lp.py` (ultima modifica 00:15) **non è stato corretto**. La correzione vive solo nel
   chiamante.
4. **Regole violate.**
   - 02-sensori dichiara di aver **cancellato** due file scaricati per errore. Se è avvenuto dopo il divieto, è una
     violazione: quando sia avvenuto è **non verificato**.
   - Il prototipo ha tenuto 9 processi per circa un minuto.
   - 21-statistica ha corretto sul posto un suo file.
   - Io non ne ho violate, che io sappia: ho scritto solo in `30-verdetto` e non ho usato la rete.

## 2. Per classe e configurazione

Le sigle degli stati: **S** = sostenuto in simulazione da scheda; **T** = su traiettorie pubbliche reali, con rumore
di scheda e occlusione virtuale; **X** = smentito; **N** = non provato. I conti sono per passaggio (n = 200) salvo
dove è detto. I conteggi a cicli o a istanti sono correlati dentro il passaggio (CONTROLLO § 1.1) e qui li riporto
solo come esistenza del difetto.

| Classe; configurazione | Avviso tempestivo? distanza; sensore | Altro sostenuto | Smentito | Non provato |
|---|---|---|---|---|
| **Droni** (multirotore), A1: IRIS + pannello + EO + Remote ID | **S, sì**: 806 m richiesti, confermata a ~960 m, 200/200 [0,98; 1]. Solo IRIS: uguale, 200/200 | T: su 98 voli di **un** Matrice 100, zona ≥ 9/10 fino a 10 s. Prudente: 0/50 passaggi senza regione | «libero» sull'oggetto con il pannello: 436/19494 istanti (prudente 119/4902). Interfaccia solo IRIS: 64/200 passaggi perdono la regione. X1: un drone che **scatta da fermo** esce dall'avviso a 3–8 s | Pd e sezione radar sono ipotesi (nessuna scheda le dà). Rivisita IRIS 1 s o 2 s (K-604). Passate correlate: con n_eff = 1 il «libero» scende a 0,88 km (X4) |
| Drone C0 (< 250 g), A1 | S: 29/29 [0,88; 1] | — | «libero» sul C0 con il pannello: 340/3306 istanti | X6: il «libero» non verifica il C0 già da circa 250 m |
| Drone, A4 (radar 4D di bordo + AT128 + EO) | **X/parziale**: 149/200 [0,68; 0,80]; solo radar 4D 100/200 [0,43; 0,57] | — | il filtro Doppler perde il drone lento; nel prudente l'avviso perde il mezzo in 134/2025 cicli (min) | — |
| Ala fissa (ALFA, in avaria) | N | — | T: zona ~6/10 a 10 s (1 esemplare, 16 voli) | — |
| **Aerei** in rullaggio, A2: SCANTER + AT128 + ADS-B | **S, sì**: 147 m richiesti, confermata a 303 m, 200/200. Solo SCANTER: **X**, 50/200 [0,20; 0,31] | — | identità: 200/200 scambi, in gran parte un artefatto della metrica (non risolto) | — |
| Aerei in finale, A3: radar d'aeroporto + ADS-B (+ IRIS) | **N** (per costruzione, 0/200) | Il drone sotto 200 m **non è mai visto** dal radar d'aeroporto (0/200 conferme): il caso «sotto la copertura» | precisione a 2 s: 32/42 (radar a 4 s) | MTI non modellato |
| Aerei, traiettorie (43 aerei in prova, ADS-B) | — | **T**: zona ~0,93–0,95 da 2 a 30 s (bootstrap per mezzo, limite inferiore ≥ 0,87) | **avviso con v_max 90 m/s: fuori in 105/722 (2 s) … 167/730 (10 s) casi; in 8–11 aerei su 43**. Correzione non applicata | — |
| **Auto**, S1: 2 × radar 4D + AT128 | **S, sì**: 67 m richiesti, confermata a ~105 m, 200/200 | T: 30 auto US-101, ~0,93 a 2 s e 0,86 a 30 s [bootstrap 0,82; 0,90] | «libero» sull'auto (Doppler): 23 e 30 istanti su 7800 (prudente 20 e 13 su 1950). Prudente fuori avviso 141/2801 cicli. Precisione ≤ 0,67. Falsi avvisi 711–1594 all'ora | caso a più di 17 m/s |
| **Treni**, S2: Tele-15 + radar 4D + AT128 | **parziale**: 261 m, 186/200 [0,89; 0,96] (si ferma o torna indietro prima della conferma) | T: 19 treni, zona ~0,9 | **T: avviso fuori in 61/405 casi a 2 s, in 18 treni su 19** (verità GPS sporca, NIS 1,4·10⁵, passo 3 s: la causa è **non verificata**). Precisione a 20 s 0/20 | alta velocità (7,57 km): no per conto, non simulato |

**Eventi E1–E5** (16 passaggi per E1–E2, 60 o 300 per gli altri; valgono solo per smentire, CONTROLLO § 1.5):

| Evento | Esito |
|---|---|
| E1 collisione fra droni | entro 2 s: **X**, 1/16 (min) e 0/16 (alta); frammenti dentro V: 0,981 contro ≥ 0,999 richiesto |
| E2 avaria con fiammata | camere dichiarate non affidabili: 32/32, entro 3 cicli. Avviso al mezzo: **X**, 0/32 [0; 0,11] |
| E3 nebbia o pioggia | nessuna cella «libera» oltre la portata utile, su 4,2·10⁸ celle-ciclo; 0 tracce perse senza avviso su 1080 cicli. Il conto e il nucleo usano la stessa formula: **non indipendente** |
| E4 fumo e detriti in pista | falsi eventi **X**: 5/60 [0,04; 0,18] |
| E5 passaggio ravvicinato (controllo) | falsi eventi a 5 m **X**: 1/300 [0,001; 0,019] |

## 3. I principi alla nuova scala

1. **Mai «libero» il non osservato.**
   - **Regge per costruzione** sulle celle mai illuminate, in ombra o scadute (04-moto P3: 0 su 12 960), e oltre la
     portata utile con nebbia e pioggia (E3).
   - **Smentito come proprietà dell'uscita** in tre configurazioni simulate: radar 4D (filtro Doppler), pannello
     (ritorno nella cella vicina), e mappa ignota (X5: un edificio non in pianta dà «libero»).
   - **La regola in più**: Pd per classe, con la finestra W_c (04-moto § 1.2). L'uscita dice «libero **per
     ⟨classi ammesse⟩**»; per le altre classi dice «zona non verificata per ⟨classe⟩».
   - **Controesempi che restano:** X4 (passate correlate: 0,263 di mancate contro 0,010 dichiarate), X5 (mappa),
     X6 (classi non ammesse), e il Doppler e la cella vicina (validazione-2, non applicata).
2. **L'avviso non si toglie se non guardando.**
   - **Regge solo con la chiamata prudente:** 0 passaggi su 600.
   - **Smentito con l'interfaccia del nucleo:** 564 su 2400.
   - **«L'avviso contiene il mezzo»: smentito** anche nel modo prudente, perché un falso ritorno ricentra l'avviso
     (A4 min 134/2025, S1 min 141/2801 cicli). Altri controesempi: v_max degli aerei (traiettorie), lo scatto da
     fermo (X1), i treni (18/19).
   - Il prototipo dà l'avviso con un ritardo di 2 cicli, tollerato da f15 fino a 2,5 s più un periodo (K-608).
3. **Nessuna etichetta riduce l'avviso.**
   - **Regge**: per costruzione l'insieme di presenza usa l'inviluppo dello scenario, non la classe. Nel prototipo
     228 cicli su 228 sono identici con e senza etichette (A1, **un** passaggio, cicli correlati).
   - **Riserva:** dipende dall'**inviluppo dello scenario**, che oggi è sbagliato per gli aerei (90 contro 210 m/s)
     e per i droni veloci (6,9 m/s²).

## 4. Le correzioni obbligate dell'attacco: nessuna applicata

`movi_lp.py` è delle 00:15 e `regole_lunga_portata.json` delle 00:17. Dopo le 01:33 nessun file di f15 è cambiato
(`find -newermt`). Per ciascuna delle otto correzioni:

1. inviluppo (v_max ≥ 210, a_max del drone veloce, tabella § 4): **no**;
2. passate correlate: **no**;
3. mappa degli ostacoli e del disturbo come ingresso di sicurezza: **no**;
4. «libero per ⟨classi⟩», pedoni in `strada`, C0 in `aeroporto`: **no**;
5. validazione-1: **solo nel chiamante** (prototipo, prudente predefinito); 2 e 3: **no**;
6. modello del disturbo strutturato: **no**;
7. divisione per mezzo: **fatta** da 21-statistica (`ridivisione/`, `compara.json`) e adottata qui. Le occlusioni
   vicino agli ostacoli: **no**;
8. rivisita IRIS: **no** (K-604).

## 5. Contraddizioni (K#)

| K | Contrasto | Vale | Prova |
|---|---|---|---|
| K-601 | «122 droni reali» (12-traiettorie) contro 2 esemplari | **2 esemplari** (101 + 21 voli; in prova 114 voli) | CONTROLLO § 0; DATI_PUBBLICI righe 12–13 |
| K-602 | prudente «campione diverso» contro gli stessi semi 0–49 | sottoinsieme **appaiato** (dal codice; il confronto esecuzione per esecuzione è non verificato) | CONTROLLO § 1.2b |
| K-603 | «aeroporto: operatore 1,49 km: sì» contro X3 | **no** con v_max 210 (3410 m > 2360 m) | ATTACCO X3 |
| K-604 | IRIS rivisita 1 s contro «30 rpm» (2 s) | **non risolto**: lo decide la scheda (antenne contrapposte?) | ATTACCO § 2 |
| K-605 | «zona ~0,9» per i treni contro avviso fuori in 18 treni su 19 a 2 s | tutti e due veri; vale **«avviso non garantito per i treni»** finché la verità GPS non è ripulita | `compara.json` (riconto) |
| K-606 | «il modo prudente risolve» contro il «libero» sull'oggetto ancora presente nel prudente | il prudente risolve **solo P2**, non P5 (A1 alta 119/4902, S1 20/1950) | riconto |
| K-607 | file cancellati da 02-sensori, contro il divieto | ora non verificata | SENSORI § 1 |
| K-608 | prototipo «avviso 14/16» contro f15 «0 fuori avviso» | definizioni diverse (tolleranza di 2,5 s); proposta sviluppatore-2 | LUNGA_PORTATA § 2.1 |

## 6. Affermazioni convergenti per i documenti

Sono dodici al più, ciascuna nella forma più forte che resta vera.

1. **(Aerei e droni)** «In simulazione, con un radar per droni preso dalla scheda, un drone a 15–21 m/s che passa
   dietro un edificio è stato annunciato all'operatore in tempo (gli servono 806 m, la traccia era confermata a circa
   950 m) in 200 passaggi su 200; l'avviso di possibile presenza è rimasto acceso per tutta l'ombra.» · S (Pd
   ipotetica) · `11-prove/risultati_lp_*.json`.
2. **(Aerei e droni)** «Un radar d'aeroporto non vede un drone sotto la sua copertura (0 conferme su 200 passaggi
   simulati). MoVi non chiama "libero" quello che il sensore non può vedere: dice "zona non verificata per droni".»
   · S, e per costruzione · 11-prove T1, 04-moto § 1.2.
3. **(Aerei e droni)** «Su 43 aerei reali (dati ADS-B pubblici), dopo 2–30 s senza vederli, la zona dichiarata
   conteneva l'aereo in circa 9 casi su 10.» · T · `compara.json`.
4. **(Aerei e droni)** «Sulle piste, con radar di superficie, LiDAR e ADS-B, l'avviso per un aereo in rullaggio
   nascosto da un hangar arriva in tempo (147 m richiesti) in 200 passaggi su 200. Col solo radar, in 50 su 200: un
   sensore solo non basta.» · S.
5. «L'avviso si spegne solo dopo aver guardato **tutta** la zona dove il mezzo può essere. Con questa regola, 0
   passaggi su 600 simulati hanno perso l'avviso. Con la regola ingenua (guardare un punto) ne perdeva 564 su
   2400.» · S.
6. «La portata passa da 3 m a circa 1 km: l'avviso, che con la camera di profondità era tempestivo fino a 1,44 m/s,
   in simulazione lo è fino a circa 21 m/s (droni, auto in città, mezzi di piazzale). Per gli aerei in volo e i treni
   veloci non lo è ancora, e il sistema lo deve dire.» · S e conto.
7. «Quando un sensore cade o la pioggia lo acceca, MoVi lo dice: in 460 casi simulati su 460, entro 5,3 s.» · S.
8. «Con nebbia e pioggia forte MoVi accorcia la portata dichiarata e non chiama mai "libero" ciò che è oltre» (0 su
   4,2·10⁸ celle-ciclo, conto e nucleo con la stessa formula). «Se una fiammata acceca le camere, lo dice in 3
   cicli» (32/32). · S, non indipendente.
9. «Il nome della classe non spegne l'avviso: con e senza etichette l'avviso è identico (228 cicli su 228, un
   passaggio).» · S, e per costruzione.
10. «Lo stesso prototipo, con gli stessi comandi, gira a corto raggio e a lunga portata su 20 scene simulate e
    riproduce ciclo per ciclo le prove dello sciame (17 file su 17).» · verificato (stesso codice: non indipendente).
11. «"Libero" vale solo per le classi dichiarate, con la mappa degli ostacoli data: un ostacolo ignoto, un drone
    sotto i 250 g o un filtro Doppler possono aprire un "libero" falso, e li abbiamo trovati.» · X, dichiarato come
    limite.
12. «Gli eventi improvvisi sono il punto debole: la collisione fra due droni è stata dichiarata entro 2 s in 1
    passaggio su 16, e l'avviso dei detriti al mezzo in pista non è mai partito (0 su 32).» · X.

**Da non dire.**
- «validato», «testato» o «provato su sensori», «funziona su aerei e droni reali», «in tempo reale», «certificabile»,
  «detect and avoid»;
- «122 droni», «97 aerei» (sono tratti), le coperture con due decimali, «0 su 19 494» (cicli);
- «rileva droni a 3, 7,6 o 13 km»;
- «avviso tempestivo per gli aerei»;
- «l'avviso contiene sempre il mezzo»;
- «non dichiara mai libero ciò che non ha osservato» senza «per le classi ammesse, con la mappa data, con passate
  indipendenti»;
- «dichiara le collisioni entro 2 s»;
- «zero falsi allarmi» (si va da 3,8 a 1594 all'ora);
- qualunque lessico d'ingaggio o di contrasto, compresa la fonte e il lessico della scheda IRIS («counter-drone»,
  «drone threat»);
- qualunque cifra di tempestività per A3.

## 7. Limiti da dire per primi

1. Nessun sensore fisico. Il 46 % dei campi delle schede è un'ipotesi: tutte le Pd, i falsi allarmi e le latenze.
2. Con il limite di velocità attuale l'avviso perde gli aerei veloci (in 8–11 aerei reali su 43). La correzione a
   210 m/s non è fatta, e con essa l'operatore aeroportuale non è più avvisato in tempo.
3. Il «libero» è smentito con il radar 4D e con il pannello, e vale solo per le classi e la mappa dichiarate.
4. Collisione e detriti (E1, E2) sono smentiti, e i falsi avvisi sono troppi.
5. Un solo multirotore e un solo ala fissa reali; 30 auto, 19 treni e 43 aerei in prova, in cinque luoghi e
   giornate.
6. Tutte le correzioni dell'attacco sono ancora da fare.

## 8. Che cosa cambia nei documenti e nel video

- **Documento di due pagine** (`proposta_sciame.tex`, riga 129):
  - la frase «1,44 m/s … veicoli, treni e aerei no» diventa l'affermazione 6;
  - il caso centrale diventa il drone dietro l'edificio (affermazioni 1, 2, 5) e il rullaggio (4);
  - nella stessa pagina vanno i limiti 1–4.
- **Allegato tecnico:**
  - capitolo nuovo `10_lunga_portata.tex`, con queste parti:
    1. sensori da scheda, con la tabella dei valori «ipotesi»;
    2. griglia polare e «libero» per classe (W_c, Pd);
    3. avviso tempestivo per ricevente;
    4. prove simulate A1–A4, S1, S2 (prudente contro interfaccia);
    5. traiettorie pubbliche, divisione per mezzo;
    6. eventi E1–E5;
    7. attacco X1–X7 e correzioni;
  - da aggiornare: `08_limiti.tex` (§ 7 qui), `01_introduzione.tex` (la scala), `A_parametri.tex` (le schede),
    `B_riproducibilita.tex` (`rifai.sh` dura 35 minuti, più `ridividi.py`).
- **Video:**
  - scena principale: `lp_A1` (drone nascosto, avviso acceso, che si spegne solo guardando);
  - contrasto: `lp_A1_interfaccia`, «la regola ingenua lo perde»;
  - limite onesto: `lp_A3` (drone sotto la copertura, «zona non verificata»);
  - visibilità degradata: `lp_E2` (camere accecate, dichiarate);
  - la riga fissa resta «dati simulati | etichette a mano | nessun sensore fisico»;
  - niente cifre di E1 come successo.

## 9. Decisioni dell'utente e prossima prova

- **Decisione dell'utente (K-603).** Il caso centrale si dice come «sito sorvegliato da droni», con l'inviluppo dei
  droni: è tempestivo. Oppure come «aeroporto», con gli aerei nell'inviluppo: con v_max 210 non è tempestivo, e va
  detto. L'arbitro non sceglie.
- **Prossima prova che cambia la decisione.**
  - Applicare le correzioni 1, 2 e 5 (inviluppo corretto; n_eff = 1 per le passate correlate; validazione-1 nel
    nucleo e validazione-2), poi rifare A1 e A2 nel modo prudente con **n = 200** e un record per passaggio
    (statistico-1).
  - **Previsione** (per conto, 04-moto § 4 con ATTACCO X3–X4): con l'inviluppo dei droni (v_max 21) A1 resta
    tempestivo, perché 806 m < 880 m di «libero» con n_eff = 1. Con l'inviluppo aeroportuale (210 m/s) non lo è.
    Il «libero» sull'oggetto con il pannello passa a 0.
  - **Smentita:** A1 con l'inviluppo dei droni sotto 190/200, oppure un solo passaggio con il mezzo fuori
    dall'avviso.
