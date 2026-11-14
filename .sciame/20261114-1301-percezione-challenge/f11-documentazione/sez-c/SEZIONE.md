# Sezione C — Prove eseguite e risultati numerici

*Stato al 14 novembre 2026, ore 16:15 (`date -Is`). Autore: `sciame-metrologo`, fase f11. I percorsi sono relativi alla cartella della convocazione, `.sciame/20261114-1301-percezione-challenge/`. Abbreviazioni: `t/` = `f2/04-torneo/`, `a/` = `f4/H-012/01-avversario/`, `v/` = `f4/H-012/03-validazione/`.*

**In testa.**
- **Niente è provato sull'hardware.** Ogni cifra di questa sezione viene da una simulazione, da un conto o dalla lettura di una scheda tecnica; le simulazioni sono tutte a sensore fermo, salvo i conti sul moto del §C.1.8. Nessun fotogramma di una camera vera è stato elaborato da una prova vagliata (`f4/H-012/09-arbitro/VERDETTO.md`, §5, punto 10).
- **Che cosa ho fatto oltre a leggere.** Un controllo di ripetibilità: sette script già consegnati rilanciati senza modifiche, previsione scritta prima (16:12:36), esito **regge** (§C.1.9; `f11-documentazione/sez-c/riprove/`).
- **Scostamenti.** (1) La sezione supera le sei pagine chieste (circa nove, a 6 200 caratteri la pagina): l'inventario con otto voci per prova e la tabella da quaranta righe non ci stanno in meno. (2) Sui file grezzi dei risultati ho ricontrollato con `grep` ventisei righe della tabella C.2 (segnate con *: tornano tutte); le altre cifre le riporto dai rapporti che le citano, e il loro riconteggio sui file è quello dell'arbitro (`VERDETTO.md`, in testa). (3) Non ho riaperto nessuna pagina in rete: lo stato delle fonti è quello scritto nei file. (4) `f2/01-traduzione/SCHEDE.md`, `f6-specializzazione/01-esperto-dominio/` e le consegne delle estensioni f7–f10 non sono letti: di f7–f10 do solo l'elenco (§C.5). Regole violate: nessuna che io sappia.

## C.0 Come leggere

**Stati.** *Dimostrato* (c'è una prova scritta; si dice in quale modello) · *verificato* (controllo esaustivo su un insieme dichiarato) · *sostenuto dai dati in simulazione* · *smentito* (c'è un controesempio) · *non risolto* (si dice che cosa lo deciderebbe) · *non verificato fino all'hardware* · *preliminare, non vagliato* (estensioni f7–f10). «Regge per costruzione» vuol dire che la prova non poteva fallire: vale come controllo del codice, non come dato.

**Sigle interne.** R1–R8: gli otto requisiti della challenge (`CONTRATTO.md`). H-001…H-020: le venti ipotesi nate in f1 (`f2/03-triage/TRIAGE.md`); **H-012** è il ramo scelto. F-001…F-008: fatti stabiliti da più ruoli. K-001…K-018: contraddizioni fra ruoli o fra prove. C1–C12: correzioni nate dai dodici attacchi di f4. A1–A7, B1–B4, P1–P5: misure delle prove di f4. **H0–H13** (senza trattino) sono invece le prove sull'hardware ancora da fare (`f3/H-012/03-metrologo/PIANO_MISURE.md`).

**Termini.** *Pd*: probabilità che il rilevatore veda il soggetto in un fotogramma. *σ*: scarto tipo del rumore. *q*: rumore di processo del filtro di Kalman (quanto il filtro ammette che la velocità cambi), in m²/s³. *Prova χ²*: prova statistica che decide se la velocità stimata è diversa da zero. *Strato 1*: l'avviso «possibile presenza» sull'ombra in cui un soggetto seguito è entrato. *Strato 2*: l'area «probabile» della previsione. *Fascia*: i 0,40 m di cui l'ombra stimata viene allargata. *Ombra a −20 cm*: l'ombra che il sistema stima è più stretta della vera di 20 cm. *Scambio muto*: identità sbagliata senza segnale di «identità ambigua». *Braccio che deve fallire*: una variante della prova costruita per fallire; se non fallisce, la prova è cieca.

**Scene.** *T* (torneo): pannello a 2 m largo 1 o 2 m, pedone a 4 m, portata 6 m. *D* (demo): pannello a 1,5 m largo 0,5 o 1 m, attore a 2,5 m, griglia fino a 3 m. *DC* (demo corretta): pannello da 1 m a 1,9 m, attore a 2,3 m, ombra di 1,21 m (`v/MISURE_V2.md`). Comportamenti del soggetto dietro il pannello: *prosegue*, *sosta* (2–4 s), *torna* indietro, *lontano* (esce dalla portata restando in ombra). Curve di rumore a 2 / 3 / 4 m: *nominale* 1,5 / 3,4 / 6,0 cm (formula del costruttore [realsense-tuning] https://dev.realsenseai.com/docs/tuning-depth-cameras-for-best-performance , pagina aperta dal ruolo di validazione, formula non letta: `f3/H-012/02-validazione/VERIFICA.md` §4), *pessimista* 4 / 9 / 16 cm, *del torneo* 5 / 11 / 20 cm (`v/MISURE.md`).

**Indipendenza, una volta per tutte.** Tutti i simulatori sono scritti da istanze dello stesso modello linguistico sulla stessa specifica: un difetto della specifica comune sfugge a tutti (`f5/02-audit/AUDIT.md` §2). «Indipendente» qui vuol dire ruolo diverso, codice diverso, semi diversi. Nelle tabelle la colonna «condivide» dice che cos'altro è in comune.

## C.1 Inventario delle prove, in ordine

### C.1.1 f1 — i falsificatori dei nove ruoli (13:04–13:17)

Nove ruoli in corsie cieche; ciascuno ha scritto le previsioni con l'ora prima di provare (`f1/<cartella>/PREVISIONI.md`). **Condividono con ciò che controllano** l'autore e il modello simulato (nel triage: «[aut.], non indipendente»). Python puro, pochi secondi di CPU.

| Ruolo (cartella) · comando | Che cosa misura · modello · N | Risultato | Soglia scritta prima | Esito |
|---|---|---|---|---|
| kalman (`21d3813ca7e1`) · `python3 sim_kalman.py`, 8 s → `risultati.txt` | osservabilità della massa; copertura del cerchio al 95 % dopo un'occlusione; moto proprio. Pedone con salti di velocità, rumore 5 cm (ipotesi dell'autore), 15 Hz | Fisher di (forza, massa) di rango 1 (det/traccia² = 5·10⁻¹⁷); copertura con q = 0,2: 0,94 / 0,92 / 0,90 / 0,92 a 0,5 / 1 / 2 / 3 s (errore tipo 0,008); con q = 0,01: 42 % a 2 s; ostacolo fermo visto in cammino: 1,49 m d'errore senza giroscopio, 0,25 m con; muro «mobile» 0,0 % con traslazione compensata (500 prove), 100 % senza | copertura in [0,88; 0,99], smentita sotto 0,85; > 1 m senza e < 0,3 m con il giroscopio (13:06:28) | **regge** (dieci su dieci). Massa: **dimostrato** nel modello del punto materiale con forza ignota |
| tracciamento (`992c41c8860e`) · `python3 -I prove/simA.py` (anche `simA2`, `simB`, `simB2`) → esiti in `PREVISIONI.md` | porta al 99 % alla ricomparsa; scadenza fissa della traccia contro chiusura «per causa». 1D, un oggetto, ombra nota; N = 3000 per punto | con q = 0,5 la porta contiene la ricomparsa nel 98,6–99,9 % fino a 3 s; scadenza di 1 s: identità 0 %; di 5 s: 75–77 % e fantasma per 2,0 s; chiusura per causa: 100 %, fantasma 0,06–0,07 s; errore al 95 % oltre 1,5 m già a 1,2 s | copertura < 90 % smentisce; tenuta < 80 % con sosta smentisce (13:05:30) | **regge** sulle due soglie; **smentite** 4 previsioni su 11 dell'autore (orizzonte 1,2 s, non 1,5–3 s) |
| rovesciatore (`8f275a60e807`) · `timeout 280 python3 -I prova_r1.py` e `prova_r2.py` → esiti in `PREVISIONI.md` | regola della bozza; ellisse del Kalman con soste e ritorni. 2000 traiettorie (1172 proseguono, 525 sostano, 303 tornano) | traccia cancellata dopo 1 s: per il 73,5 % del tempo in occlusione il bersaglio sta dove il sistema non dichiara nulla; fuori dall'ellisse al 95 %: 14,3 % (0,1 % chi prosegue, 23,8 % chi sosta, 25,3 % chi torna); a sensore fermo velocità spuria 0,241 m/s, 21,6 % di falsi «mobile» a soglia 0,3 m/s | > 20 % previsto, < 5 % smentita; velocità spuria ≤ 0,05 m/s (13:12:50) | 14,3 %: **non risolta**; 73,5 %: **regge**; «≤ 0,05 m/s»: **smentita** |
| nuvole-punti (`dfac83300259`) · `python3 -I prova_np.py` → esiti in `PREVISIONI.md` | «libero» falsi: regola log-odds della bozza contro griglia a quattro stati. 2D senza rumore, 552 casi | bozza: 265 «libero» falsi su 552 (173 in ombra, 92 da visibile); quattro stati: 0. Costo 2,0 ms a fotogramma | tre previsioni (13:05:43) | **regge** (per la griglia: per costruzione) |
| creativo (`e30f9e2dd4d7`) · script `sim.py` (4,4 s), `sim2.py` → `esito_sim.txt`, `esito_sim2.txt` | dove finisce la probabilità di un Kalman senza misure se il bersaglio sosta. 1D, 100 prove; 400 passaggi per la finestra | massa in celle viste libere: 98 % a 2 s, 100 % a 3 s; con l'evidenza negativa (particelle) 0,1 %; finestra di riemersione del Kalman: copre il 69,3 % (nominale 90 %); particelle: 100 % ma larga 6,27 s | finestra fra 75 e 97 %, smentita < 70 % (13:11:50) | massa: **regge**; finestra: **smentita in alto** (inutile perché troppo larga) |
| visione (`c85dbcc51ea6`) · script `calcoli_p2_p3_p4.py` | classi d'ostacolo nel rilevatore pronto; scadenza della previsione; sfocatura | 0 su 7 categorie d'ostacolo fra le 80 classi COCO [ultralytics-coco]; raggio al 95 % oltre 1 m dopo 1,0–1,4 s; accelerazione da differenze: σ ≈ 66 m/s² a 30 Hz | (13:05:40) | **regge**; P5 e P6 (hardware) **non risolte** |
| requisiti (`b8262bfed263`) · nessuno script conservato | parole delle regole; campo dei ToF; finestra del «previsto» | 0 occorrenze di 360, massa, accelerazione, classific-, terreno… nelle regole (esaustivo, `grep`); campo < 130° su 7 sensori; 2σ > 1 m dopo 1,30 / 1,07 / 0,87 s per q = 0,25 / 0,5 / 1,0 | (13:10:16) | **verificato** (parole); **regge** (le altre due; stessa algebra dell'enunciato) |
| lidar (`985ccd9bca46`) e ricercatore (`3fff79e9c3ea`) · letture di schede e articoli | geometria dei ToF; stato dell'arte | tre ToF multizona coprono 180° × 60° [st-vl53l7cx]; velocità costante 0,39 / 0,83 m a 4,8 s contro 0,44 / 0,91 di un modello appreso [scholler2020]; massa dalla visione: errore medio 66,5 % [lee2026] | (13:04:44; 13:10:29) | 360° con tre ToF: **smentito** sui sensori controllati; P10–P11 (prove fisiche) non eseguite |

File dei risultati: nella cartella di ciascun ruolo. Per requisiti la prova P2 non è rifacibile dal file (lo script non c'è).

### C.1.2 f2 — il torneo di falsificazione, tre parti (13:37–13:51)

Tre istanze del ruolo avversario su gruppi disgiunti di ipotesi. **Condividono** con le idee il testo delle schede, il modello linguistico e le schede dei costruttori; nessun codice degli autori, salvo dove indicato. Rapporto: `t/TORNEO.md` (somma di `TORNEO_parte1…3.md`); previsioni in `t/PREVISIONI_parte1…3.md`.

**Parte 1 — sensore, griglia, ambito** (`t/attacchi_parte1.py`, `attacchi2_parte1.py`, 0,4 s; `t/esito_attacchi_parte1.txt`, `esito_attacchi2_parte1.txt`). Conti su schede e uno script di logica. Le previsioni su H-001, H-003, H-004 non erano cieche (dichiarato).

| Ipotesi | Misura | Risultato | Esito |
|---|---|---|---|
| H-001 camera stereo | errore di profondità a 4 m al limite dichiarato (soglia: 15 cm) | Gemini 335 12 cm, D455 8 cm, D435i 16 cm; fino a 3 m ≤ 9 cm | **regge** fino a 3 m; a 4 m **non risolta** |
| H-002 inclinazione | gradino di 15 cm a 2 m; ostacolo a 1,8 m di quota | gradino a 5,4σ; a 15° l'ostacolo alto si vede solo oltre 2,41 m | gradino **regge**; cono cieco in alto: **attacco riuscito** |
| H-003 LiDAR al petto | punti su una gamba a 5 m (soglia 4) | 1,7–1,9 punti; busto copre 127°–155° | **smentita** la variante al petto |
| H-004 ambito | frasi delle regole non coperte | nessuna prescrittiva; tre non prescrittive («riconoscere», «monitoraggio di attività», «mentre la scena continua a cambiare») | da riformulare |
| H-006 percorso geometrico | tempo del percorso minimo, Python puro | 1,2 / 4,7 / 20 ms a 160×120 / 320×240 / 640×480 | regge sul calcolo; latenza totale **non risolta** |
| H-008 griglia a 4 stati | sei casi sulla regola | vetro → «libero» falso; «libero» ricordato 0,5 s con mobile a 3 m/s: 1,50 m contro 0,7 di margine | **smentita** la clausola «0 libero falsi» |
| H-017 battito | sensore che ripete l'ultimo fotogramma | il battito dura tutti i 25 s; con il contatore del sensore si ferma in 0,13 s | **smentita** «si spegne da solo» se l'età è la marca temporale |

**Parte 2 — filtro, identità, demo** (previsioni alle 13:39:12; `cd f2/04-torneo; PYTHONDONTWRITEBYTECODE=1 timeout 120 python3 torneo_parte2.py A` (poi `B C D E`), e `torneo_B2A2_parte2.py A2` (poi `B2`); file `t/risultati_{A,A2,B,B2,C,D,E}_parte2.txt`). Pedone puntiforme, 15 Hz, σ = 5 cm.

| Ipotesi | Misura · N | Risultato | Soglia | Esito |
|---|---|---|---|---|
| H-012 (q = 0,2) | copertura della regione al 95 % su tre generatori non dell'autore; 4000 ricomparse per cella | a 1 s / 2 s: 0,934 / 0,927 (± 0,004); 0,895 / 0,916 (± 0,005); 0,902 ± 0,007; per manovra: sosta 0,92–0,98, torna **0,56–0,66**; con q scelto sui tratti dritti (0,01): 0,738 / 0,710 | sotto 0,85 a 1–2 s smentisce | **regge** (la previsione di smentita dell'avversario è caduta) |
| H-013 (q = 0,5) | scambi d'identità con due persone; 2000 scene per caso | tornano entrambi: scambi 0,440 ± 0,011, muti 0,199; incrocio dietro 2 m: 0,246 ± 0,010, muti 0,238 | ≤ 2 % all'incrocio | «la geometria basta»: **smentita in simulazione** |
| H-018 demo | stessa traccia con pedone a 0,8 m/s; 2000 passaggi | finestra del «previsto» 1,60 s solo con (q 0,2; raggio massimo 1,5 m): 0,811 con 1 m di buio, ≤ 0,004 con 2 m | — | da riformulare |
| H-019 scommessa | finestra tarata sulla squadra, provata su un giurato lento; 200 tarature × 2000 | 0,633 (dev. std 0,071) | 0,75 | sotto soglia; il controllo **copia il codice dell'autore**: da riformulare, non smentita dell'idea |
| H-010 regola «mobile» | χ² a 0,5 m/s a 2 m; muro con rumore che cresce con z²; 500–1000 prove | vista entro 1 s nel 75,4 %; falsi sul muro a 4 m 15,5 % con R fisso, 0,0 % con R(z); con R(z) chi si avvicina a 4 m è visto nell'11,0 % | 90 %; 10 % | da riformulare (K-007) |

Le previsioni di B2 e A2 sono scritte dopo aver visto B e A (dichiarato: la prima B aveva un difetto dell'avversario).

**Parte 3 — la regione «prevista»** (`timeout 120 python3 scena_parte3.py <main1|main2|ombra|k001|falso|vmax|due>`, seme 20261114, al più 29 s; file `t/risultati_*_parte3.txt`). Scena T, Pd 0,9, 100 prove per comportamento.

| Misura | Risultato | Esito |
|---|---|---|
| Sosta a 3 s: la regione contiene il soggetto · quota su celle viste libere (pannello 1 m) | cerchio del Kalman 88 % · 23 %; disco v_max·t ∩ non osservato 100 % · 0 %; particelle con modo «sosta» 100 % · 0,2 % | nessuna famiglia vince (K-002) |
| A 1 s: quota dell'ombra coperta | cerchio 31 %, particelle 35 %, disco **98 %** | il disco garantisce ma non informa |
| H-014: traccia chiusa a persona nascosta | con un fotogramma 10–26 % (20,3 % su n = 300 a 4 m); con tre: 0 % a 4 m, 14 % a 3 m, 53 % a 2,5 m; con ombra a −20 cm 45–50 % | esito misto: da riformulare |
| H-009: bersaglio oltre v_max (2,5 m/s) | contenimento a 0,5 s: 100 / 90 / 10 / 0 / 0 % a 2,0 / 2,4 / 2,6 / 3,0 / 3,5 m/s | regge la previsione; v_max va dichiarata |
| H-015: identità dopo la sosta | senza modo «sosta» 71 % (1 m), 28 % (2 m); con: 100 % e 76 %; con ombra a −20 cm 68 % | scatta la soglia del triage (80 %) |
| H-016: falso «libero» per k fotogrammi | la massa giusta scende sotto il 5 % a k = 4 / 5 / 7 (0,27–0,47 s) | nessuna famiglia regge un falso libero di 0,3 s |
| Due bersagli che tornano (q = 0,2) | Kalman: 74 % di scambi (pannello 1 m), 44 % muti | l'identità con due nascosti va dichiarata «ambigua» |

Limite dichiarato della parte 3: i tre risultati marcati «[dopo]» non avevano previsione; le smentite valgono «da riformulare» perché molte scelte del simulatore sono dell'avversario.

### C.1.3 f3 — prove progettate, conti del metrologo, prova C a mano (14:00–14:18)

- **Soglie delle prove A, B, C** scritte dal responsabile alle 14:00:30 (`f3/H-012/01-scene-dinamiche/PREVISIONI.md`); i dodici attacchi con le previsioni alle 14:09:46 (`f3/H-012/04-avversario/ATTACCO.md`); numerosità e regola di decisione alle 14:13:55 (`f3/H-012/03-metrologo/PIANO_MISURE.md`). Tutto prima dei lanci di f4 (14:23).
- **Regola di decisione.** Si conta il *passaggio* (un seme), non il fotogramma. Con zero fallimenti: su 300 passaggi il tasso vero è ≤ 0,99 %, su 100 solo ≤ 2,95 %, su 20 solo ≤ 13,9 % (`f3/H-012/03-metrologo/conti_metrologo.txt`; `python3 conti_metrologo.py`); su 400, la numerosità poi usata, ≤ 0,75 % (`f3/H-012/02-validazione/VERIFICA.md` §4).
- **Potenza dei criteri per il giorno dell'hackathon** (conto binomiale, stesso file): «26 su 30» promuove una taratura mediocre (quota vera 0,80) nel 25,5 % dei casi; il criterio a due stadi (≥ 28 regge, ≤ 22 smentita, altrimenti altri 30 e ≥ 52 su 60) nel 14,2 %. «9 su 10» passa nel 24 % dei casi con quota vera 0,75. Stato: **dimostrato** nel modello binomiale (passaggi indipendenti).
- **Prova C, a mano** (`f3/H-012/02-validazione/VERIFICA.md` §3): le 7 frasi delle regole hanno tutte un componente (C1 **regge**; tre clausole senza misura); bilancio della latenza: le sole voci note sommano **circa 155 ms** in media contro la soglia di 150 (C2 **non risolta**). Fonti dei tratti: [realsense-highspeed] https://dev.realsenseai.com/docs/high-speed-capture-mode-of-intel-realsense-depth-camera-d435 (95 ms in media a 30 fps; aperta dal ruolo) e [pipewire-conf] https://docs.pipewire.org/page_man_pipewire_conf_5.html (21,3 ms).
- **Rilettura.** 20 numeri del torneo ricontati sui file: 17 tornano, 3 con nota (stesso file, §1).

### C.1.4 f4 — i dodici attacchi alla soluzione (14:23:48–14:29:12)

Rapporto: `a/CONTROPROVE.md`. Modelli dell'avversario: rilevatore «centro della parte visibile», suolo che manca a caso, frase di 2 s, rumore dell'IMU ipotizzato. **Condivide** con la soluzione: modello linguistico, testo della soluzione, numeri del torneo (σ 5 cm, 15 Hz, Pd 0,9, q 0,2), altezza 1,2 m; nessun codice degli autori. Soglie: `ATTACCO.md` (14:09:46). **Rifare:** in `a/`, `PYTHONDONTWRITEBYTECODE=1 timeout 120 python3 <script> [argomento]`, con `a01_riaggancio.py`; `a02_demo.py a2|a6c|a11`; `a03_priorita.py`; `a04_tetto.py`; `a05_contiguita.py`; `a06_centroide.py a|b`; `a07_a08_primo_secondo.py a7|a8`; `a09_a10_a12.py a9|a10|a12`; `correzioni.py a3|a10|a11`. **Nessun attacco ha prodotto un «libero» falso**; ma nessuno script calcola un «libero» da una profondità (§C.1.7, ipotesi 2).

| # | Che cosa attacca · N | Prima | Dopo la correzione | Esito · file |
|---|---|---|---|---|
| 1 | riaggancio rubato da un soggetto mai tracciato · 200 scene per ritardo | sbagliato e muto 9,5–100 % | C1: 0,0 %; costo: riemersioni legittime 100 % fino a 2,3 m, 86,3 % a 2,5 m, 0 % a 2,8 m (N = 300) | regola **smentita e corretta** · `a/risultati_a01.txt` |
| 2 | demo in scala, attore a 3 m · 500 transiti | tracce confermate 0,4 % | C2 (attore ≤ 2,3 m): 100 % | geometria **smentita e corretta** · `a/risultati_a02.txt` |
| 3 | graduatoria dei messaggi e anello cieco | «mobile in avvicinamento» detto nello 0 %; suolo visto solo da 1,243 m; ostacolo di 15 cm invisibile sotto 1,087 m; scatola a 0,8 m: 0 su 5 | C3: 100 / 100 / 99,5 % con suolo valido 1 / 0,99 / 0,95; 65,6 % a 0,80 | **smentita e corretta**; ostacoli bassi vicini: limite che resta · `a/risultati_a03.txt`, `a03_correzione.txt` |
| 4 | tetto di 10 s sull'avviso · soste di 11–60 s | 15–750 fotogrammi di nascosto senza avviso | C4 (nessun tetto, solo l'età): 0 | **smentita e corretta** · `a/risultati_a04.txt` |
| 5 | strato 1 esteso alle celle contigue | copre il 100 % del non osservato (45,5 m² contro 1,01 d'ombra) | C5 (solo il cuneo): 1,01 m²; la fascia resta sul 28,2 % dei 4,75 m² di libero visto | **smentita e corretta**; «metà dell'ombra» **non risolta** (0,8–5,8 s secondo la lettura) · `a/risultati_a05.txt` |
| 6a | muro con una persona che gli passa davanti · 500 passaggi | muro «mobile» nel 100 % | C6 (gruppo tagliato dall'ombra escluso): 0,0–0,2 % | **smentita e corretta** · `a/risultati_a06a.txt` |
| 6b | fusione di due gruppi vicini | a contatto solo a 2 cm (77–97 %) | — | **regge** (previsione dell'avversario smentita) · `a/risultati_a06b.txt` |
| 6c | corpo largo che entra nell'ombra | contenimento 70,8–85,8 % (soglia 85 %) | C6: 100 %, ma il buio sale a 1,07–1,27 s e il «previsto» è vivo alla riemersione nel 9,8–18,8 % | **smentita** nella demo in scala · `a/risultati_a06c.txt` |
| 7 | soggetto visto pochi fotogrammi | con 3 fotogrammi la traccia manca nel 27,1 %; con 4 nel 5,2 % | C7 (garanzia solo da 4 fotogrammi): **non provata** | portata della garanzia **smentita**, da dichiarare · `a/risultati_a07.txt` |
| 8 | finestra della regola «mobile» · 2000 prove | fissa, Pd 0,9: vista entro 1 s nel 79,0 % | C8 (finestra che cresce): 99,9–100 %; falsi da fermo 0,05 % | **smentita e corretta** · `a/risultati_a08.txt` |
| 9 | «libero» senza memoria, suolo valido 0,95 | 11,9 cambi di messaggio al secondo | C9 (3 fotogrammi): 0,00 per direzione, 0,65 per settore; a 0,80 non basta | **smentita e corretta** nel modello a buchi indipendenti · `a/risultati_a09.txt` |
| 10 | affidabilità persa: sensore quasi coperto, urto | nessun segnale in 3 s; dopo 10° d'imbardata i fermi sono «mobili» nel 96–100 % | C10: segnale in 0,13 s e 0,00 s; 0 falsi in 60 s | **smentita e corretta** (rumore dell'IMU ipotizzato) · `a/risultati_a10.txt`, `a10_correzione.txt` |
| 11 | tre stati in voce | frase finita a stato scaduto nel 100 % | C11 (segnali di 0,3 s): 0 % | **smentita e corretta** (durata della frase ipotizzata) · `a/risultati_a11.txt`, `a11_correzione.txt` |
| 12 | copertura delle regole; esclusione dei ToF | la camera vede il 20,0 % del disco di 3 m; tre ToF laterali fino a 2 m aggiungono il 22,2 %; uno in basso copre 0,68 dei 0,98 m² dell'anello cieco | C12: ToF come canale laterale facoltativo, mai «libero» | esclusione **smentita a ragionamento**; cifre dei ToF non riverificate · `a/risultati_a12.txt` |

### C.1.5 f4 — prova A (la composizione) e prova B (regola «mobile») (14:24–14:35)

Rapporto: `v/MISURE.md`. Simulatore nuovo `v/sim_h012.py` (sha256 `c0a94feb…`), seme 5101, corpo di 40 cm, 400 passaggi per cella (zero fallimenti → limite superiore 0,75 % per cella). **Condivide** con la soluzione specifica, modello linguistico, rumore gaussiano bianco, pavimento piano, pannello e sensore fermi, nessun rilevamento falso; **non** codice, semi, traiettorie, forma del corpo e curva di rumore del torneo. **Rifare:** `sh f4/H-012/03-validazione/rifai.sh` (13 lanci, circa 50 s; **riscrive** i file `v/out_*.txt`).

| # | Che cosa misura | Risultato (N) | Soglia scritta prima | Esito |
|---|---|---|---|---|
| A1 | fotogrammi con il nascosto fuori dallo strato 1 | lettura «cuneo più celle contigue»: 0 in 48 celle, 19 200 passaggi; lettura «solo cuneo»: 400 su 400 nelle celle «lontano» | un solo caso smentisce | regge / smentita secondo la lettura; sciolta poi nella versione 2 (§C.1.6) |
| A1, sensibilità | errore d'ombra che rompe il contenimento (1200 passaggi per riga) | corpo 40 cm: −20 cm 0 fuori; −30 cm 107 (8,9 %); −40 cm 1075 (89,6 %). Corpo 60 cm a −30 cm: 399 (33,3 %) | — | il margine oltre −20 cm è **meno di 10 cm** |
| A2 | costo: strato 1 su suolo davvero visibile | 14–41 % in T; 37–68 % in D (1,1–2,3 m²) | descrittiva | costo dichiarato |
| A3 | la riemersione cade nell'area prevista | T: prosegue 95,8–100 %, torna 90,2–92,2 %; D con pannello da 1 m: 97,0–100 %; **D con pannello da 0,5 m: 14,2–16,5 %** (errore tipo ≤ 1,8 punti) | < 85 % smentisce | T regge; D-0,5 m **smentita** |
| A3 bis, A4 | area prevista ancora *mostrata* alla riemersione | T: 0–6,2 %; D: 0–1,5 %; buio medio in T-1 m 1,9 s | previsto 30–70 % | **smentita**: lo strato 2 è quasi sempre già spento |
| A5 | stessa identità al ritorno, una traccia pendente | 100 % in ogni cella; limite inferiore 99,25 % | < 95 % smentisce | **regge** |
| A6 | scambi muti con due bersagli | 0 su 6400 riemersioni; «ambigua» dichiarata nel 94,5–100 % | > 0 smentisce | regge **per costruzione** |
| A7 | rilascio dello strato 1 a soggetto nascosto | cella per cella: nessuno; con la prova del raggio sul punto previsto: 92,5–99,5 % in sosta (T) | un caso smentisce | cella per cella regge (per costruzione); raggio **smentita** |
| B1 | falsi «mobile» su un muro fermo | 0 su 12 000 finestre (limite 0,025 %) con R giusto; con σ creduto la metà: 31 % delle finestre scorrevoli | > 10 % smentisce | **regge**; fragile se σ è sbagliato |
| B2, B3 | pedone a 0,5 m/s visto entro 1 s a 2 m (N = 2000) | di traverso 100 % (limite inferiore 99,85 %); in avvicinamento: spostamento 100 / 100 / 100 %, χ² 100 / 100 / 99,0 % con le tre curve | < 90 % smentisce | **regge** per tutte e due le regole (la previsione «χ² al 70–80 %» è smentita) |
| B4 | lo stesso da 3 e 4 m | da 3 m: spostamento 100 / 10,8 / 0,1 %, χ² 100 / 56,7 / 45,2 %; da 4 m con la nominale 98,5 % e 81,4 % | nessuna | oltre 2 m **non risolta**: decide il rumore vero (K-007) |
| `validazione-1` | media di 3 fotogrammi: velocità minima vista al 90 % da 2 m | 0,380 → 0,278 m/s (curva del torneo); 0,138 → 0,095 (nominale); guadagno 1,31–1,46 | guadagno < 1,3 smentisce | **regge**, per poco |

File grezzi: `v/out_A_*.txt`, `out_SWEEP.txt`, `out_A2.txt`, `out_A6.txt`, `out_WALL.txt`, `out_PED.txt`, `out_V1.txt`, `out_EXTRA.txt`.

### C.1.6 f4 — riprova dell'insieme (versione 2) e anomalia non chiusa (14:42–14:55)

Rapporti: `v/MISURE_V2.md`, `v/MISURE_V2_bis.md`. Simulatore `v/sim_v2.py` (sha256 `dd7a5a1c…`): copia di `sim_h012.py` con le regole della versione 2. Previsioni alle 14:42:18, prima del codice. **Insieme provato:** C1, C4, C5, C6, C8, media di 3, rilascio cella per cella, geometria DC. **Non provati insieme:** C3, C9, C10, C11, graduatoria dei messaggi e uscita in voce. **Rifare:** `sh f4/H-012/03-validazione/rifai_v2.sh` (8 lanci, circa 1 min) e `rifai_v2bis.sh` (4 lanci, il più lungo 64 s); riscrivono `v/v2_*.txt` e `v/bis_*.txt`.

| # | Che cosa misura | Risultato (N, limite al 95 %) | Soglia | Esito · file |
|---|---|---|---|---|
| P1 | passaggi con il centro del nascosto in una cella «libero» (Pd = 1) | 0 su 14 400 in 36 celle (0,75 % per cella); a −20 cm 0 su 4800 (0,06 %) | 0 su 400 | **regge** · `v/v2_R8.txt` |
| P1, bracci | fascia 0 e 0,20 m con ombra a −20 cm; ombra a −40 cm | 400, 399–400, 396–400 falliti su 400 | devono fallire | falliti: la prova non è cieca (ma si veda §C.4, punto 4) |
| **P1 con Pd 0,9** | lo stesso, con un rilevamento mancato su dieci | a −20 cm **13 falliti su 4800** (limite 0,43 %), in 8 celle su 12; a 0 e +20 cm 0 su 9600 | 0 falliti (nessuna previsione scritta) | **smentita**: è l'anomalia K-014 · `v/v2_R8_pd09.txt` |
| P2a | riemersioni riagganciate, una traccia pendente | 100 % in 27 celle (limite inferiore 99,25 %); con Pd 0,9: 99,7–100 % | ≥ 95 % | **regge** · `v/v2_R8.txt` |
| P2b | secondo soggetto mai tracciato | dal bordo del campo 0 su 2400; dal bordo della portata 0 su 1200 (DC), 2 su 1200 (T); **dalla stessa ombra 2400 su 2400** riagganci sbagliati e muti | 0 | DC regge, T **smentita**; stessa ombra: **controesempio** (K-016) · `v/v2_SECOND.txt` |
| P2c | la riemersione cade nel cerchio (N = 2000) | DC senza C6: 61,1 % e 80,2 % (due rilevatori) → con C6 100,0 %; pannello 0,5 m: 20,5 → 99,9 % | ≥ 85 % (regge da 86,4 %, smentita sotto 83,7 %) | con C6 **regge**; senza **smentita** anche con il pannello da 1 m · `v/v2_C6.txt` |
| P2c, «torna» | costo di C6 su chi torna indietro (N = 400) | DC 99 % → 47–50 %; T 91–98,5 % → 62–67 % | nessuna previsione | costo da dichiarare (K-017) · `v/v2_C6.txt` |
| P3a, P3b | regola «mobile» finale; muro con persona davanti | 100 % nei sei casi (N = 2000); muro: con C6 0 su 400, senza 400 su 400 | ≥ 90 %; ≤ 10 % | **regge** a 2 m · `v/v2_MOB.txt`, `v2_WALLP.txt` |
| P4 | che cosa vede la demo (DC, prosegue; mediane a −20 / 0 / +20 cm) | buio 1,13 / 1,07 / 1,07 s; «previsto» 0,40 / 0,47 / 0,53 s; area prevista ancora mostrata alla riemersione **0,5 / 1,2 / 0,8 %**; «perso» 0,67 / 0,60 / 0,47 s | descrittiva (previsto 5–40 %: smentito) | · `v/v2_R8.txt` |
| P5 | tracce vere chiuse per errore in 4 s, Pd 0,9 | 118 su 20 000 (0,59 %) chiudendo al quarto mancato; 1047 (5,24 %) al terzo | descrittiva | · `v/v2_PD.txt` |

**L'anomalia (K-014), tentativo di chiusura** (`v/MISURE_V2_bis.md`; previsioni alle 14:49:49; stessi semi; `v/sim_v2bis.py` importa `sim_v2.py`: stesso codice, non è un controllo indipendente). Meccanismo: con un rilevamento mancato la traccia si chiude prima di entrare nell'ombra, lo strato 1 non nasce, e il soggetto attraversa la striscia di 20 cm che il sistema crede visibile.

| Variante | Falliti a −20 cm su 4800 | Costo |
|---|---|---|
| regola della versione 2 | **13** (riprodotto; riprodotto di nuovo oggi, §C.1.9) | 613–686 strati 1 rimasti accesi a soggetto visibile (12,8–14,3 %) |
| `validazione-4` (la traccia chiusa vicino a un'ombra lascia l'avviso) | 8 (limite 0,30 %); 2 (0,13 %) se la traccia chiusa rinasce | riaggancio 99,92–99,97 % |
| ingresso immediato entro 1 m dall'ombra, con rinascita | 0 (limite 0,06 %) | strati a vuoto 2523–2700; primo riaggancio 50,3–55,0 %: **esclusa** |

Esito: la previsione «0 su 4800 con `validazione-4`» è **smentita**; l'anomalia **non è chiusa**. Secondo l'arbitro (`VERDETTO.md`, §3) il simulatore assegna «libero» per definizione senza calcolare una profondità: il difetto vero è la perdita dell'avviso (a 0 e +20 cm il soggetto resta in celle «in ombra»: 0 su 9600); il «libero» falso esiste solo se la camera dà profondità valide e sbagliate dentro l'ombra vera: **non decidibile senza hardware**. Dopo un riaggancio sbagliato (K-016) il primo soggetto, a −20 cm, finisce in una cella «libero» in 800 su 800 (sosta), 799 su 799 (torna), 17 su 800 (lontano); a 0 e +20 cm mai (`v/bis_FURTO.txt`).

### C.1.7 f5 — audit delle ipotesi nascoste (14:39–14:50)

`f5/02-audit/AUDIT.md`; previsioni P1–P9 alle 14:43:13 in `f5/02-audit/stato.md`. Sono **conti a mano** sui numeri dei file, senza script (non c'è un comando: si rifanno con la calcolatrice); l'autore dichiara di averne scelto il verso in anticipo, quindi valgono come conti, non come prove riuscite. **Condivide** con ciò che controlla i numeri dei file e il modello linguistico.

| Ipotesi nascosta | Conto | Stato |
|---|---|---|
| 1. Un buco di profondità arriva come «nessun dato» | i filtri del costruttore lo riempiono con l'ultimo valore valido o con un vicino [realsense-filtri] https://dev.realsenseai.com/docs/post-processing-filters/ (letto solo il riassunto di ricerca) | **non risolta**; controllo: mano sul sensore, pixel validi sotto il 10 % in 3 fotogrammi |
| 2. «Libero» calcolato da una profondità | nessuno script di f4 genera pixel (`a/a03_priorita.py` riga 35; `a/comune_f4.py`) | «nessun libero falso» vale come **controllo della logica**, non come dato |
| 3. Età del «libero» senza la latenza | 0,13 s + 0,155 s = 0,288 s → **0,72 m** a 2,5 m/s (la versione 2 scriveva 0,33 m); a 1,4 m/s 0,40 m: margine zero | riga dell'invariante 1 **smentita** (K-015) |
| 4. «A meno di 0,40 m da un'ombra» | l'ombra propria comincia a 0,1 m: il ramo «campo aperto» alla lettera non scatta mai | difetto di scrittura (K-018) |
| 5. Altezza del pannello | deve essere alto almeno 1,45–1,50 m; nessun file la fissava | **non risolta**, basta un metro a nastro |
| 6. Buchi del suolo indipendenti | con l'1 % di celle sempre non valide, l'83,6 % dei settori da 10° contiene un buco permanente | **non risolta** (prova H5) |
| 7. Soglie in fotogrammi | all'1 % di fotogrammi saltati: 9 falsi attesi in 60 s; zero falsi ha probabilità 0,012 % | **non risolta**; soglie da riscrivere in secondi |
| 8. Catena dei blocchi | 54 ore-persona in tutto (3+6+6+5+9+4+3+6+12), **38 in fila** | conto di pianificazione |
| 10. Ombra da un punto solo | banda senza dato accanto all'ombra: 9,5 cm con base 95 mm (D455), 5 cm con 50 mm (D435i) | **non risolta** |
| 11. Soglia di quota 0,07 m | curva pessimista, a 3 m: il 3,6 % dei pixel di suolo la supera; con la nominale zero | **non risolta** |
| 9, 12 | avvio con scena non vuota (1,34° d'errore = 7 cm a 3 m); costanti che valgono solo per pedone, sala e sensore fermo (a 10 m/s, 0,288 s sono 2,9 m) | **non risolte** |

### C.1.8 f6 — attacco alla specializzazione e conti sul moto del sensore (14:41–14:54)

**Queste cifre non sono passate dal verdetto dell'arbitro**, che dichiara di non aver letto `f6-specializzazione/` (`VERDETTO.md`, in testa): stato «sostenuto dal modello, non vagliato».

**Attacco alla specializzazione** (`f6-specializzazione/03-avversario/ATTACCO_SPECIALIZZAZIONE.md`; previsioni alle 14:52:45 in `PREVISIONI_in_testa.txt`; `python3 conti_spec.py`, `conti_spec2.py`, meno di 2 s → `risultati_spec.txt`, `risultati_spec2.txt`). Conti geometrici; **condividono** con i testi attaccati camera a 1,2 m, 15°, 58°, griglia, fascia, latenza di 0,155 s.

| # | Che cosa attacca | Risultato | Esito |
|---|---|---|---|
| S1a | messaggio per settori con un soggetto basso e vicino | invisibile fino a 0,72 / 0,62 / 0,43 / 0,23 m d'altezza a 0,5 / 0,6 / 0,8 / 1,0 m: il settore dice «nessun ostacolo fino alla portata» | riga della demo **smentita** |
| S1b | pannello a 1,15 m | 18 settori su 18 dicono «sconosciuto»; con il pannello a 1,70–1,90 m solo 2 | pannello a non meno di 1,7 m |
| S2 | «adattabile» | regole identiche 4 su 9, riscritte 5; blocchi cambiati 6 su 9 | frase **smentita dal testo stesso** |
| S3 | fascia con la latenza (0,288 s) | persona 0,72 m, mezzo 2,31 m, drone 5,48 m; velocità coperta con 0,40 m: 1,39 m/s (0,35–0,69 se i termini si sommano) | tabella della fascia **smentita** |
| S5 | frasi per la giuria | 4 su 7 non reggono alla lettera | riscritte nel file |
| S6b | piano del suolo ristimato con 2° d'errore | scatola di 15 cm letta a 8,0 cm a 2 m, 4,5 cm a 3 m (sotto la soglia di 7 cm) | da riformulare |
| S6c | memoria del «libero» spenta oltre 0,37 m/s | «nessun ostacolo» nell'1,0 % dei fotogrammi con suolo valido al 95 % | non provato in moto |
| S7 | camera a 0,25 m di quota (drone posato) | suolo da 0,26 m; radenza a 3 m di 4,8° (21,8° a 1,2 m) | i numeri valgono solo per 1,2 m |

**Conti sul moto del sensore** (`f6-specializzazione/02-slam/MOTO_PROPRIO.md`; previsioni alle 14:41:38 e 14:42:21 in `PREVISIONI.md`; `PYTHONDONTWRITEBYTECODE=1 timeout 300 python3 bilancio_posa.py > risultati.txt`, 6 s). Modello: gruppo fermo, regola «mobile» del nucleo, 15 Hz, curva nominale; gli errori delle sorgenti di posa sono **ipotesi dell'autore**. **Condivide** con il nucleo la regola «mobile» e le curve di rumore. Previsioni **smentite**: P1, P3, P10, metà di P2 e di P7 (l'autore aveva letto la regola dal testo e non dal codice: la soglia trasversale è un angolo, 1,18°, uguale a ogni distanza); reggono P4, P5, P6, P8, P9, P11.

| Requisito sulla posa perché una soglia del nucleo valga in moto | Valore |
|---|---|
| Q1 imbardata relativa (falsi «mobile» ≤ 10 %) | ≤ 0,87° su 0,87 s, a ogni distanza |
| Q2 errore di velocità trasversale / radiale a 2 m e a 3 m | 3,4 / 5,2 cm/s e 5,2 / 11 cm/s |
| Q3 ritardo fra posa e profondità | 20–30 ms (rotazione a 30°/s); 27 ms (sensore al petto); 5,6 ms (sulla testa) |
| Q4 beccheggio rispetto al suolo a 2 / 3 / 10 / 30 m | 1,68° / 1,02° / 0,32° / 0,13° |
| Giroscopio con 1°/s di deriva, da fermi | falsi 9 % (sulla soglia); con 0,1°/s: 0 |
| Indossato, traslazione non compensata | falsi **100 %**; con odometria visuale-inerziale all'1 %: 0 |
| Drone con 0,1 m/s d'errore di velocità (ipotesi) | falsi 98 % a 2 m, 3 % a 3 m |

Stato: **sostenuto dal modello**; l'errore vero di ogni sorgente di posa è **non risolto**; nessuna soglia del nucleo è provata in moto.

### C.1.9 Controllo di ripetibilità fatto oggi (f11, 16:12–16:14)

Previsione scritta alle 16:12:36, prima dei rilanci (`f11-documentazione/sez-c/riprove/PREVISIONI.md`): «sette script ridanno il file consegnato riga per riga, tempi esclusi; smentita: una riga numerica diversa». Rilanciati senza modifiche, uno alla volta, con `PYTHONDONTWRITEBYTECODE=1 timeout 120 python3 <script> [argomenti] > riprove/Rn.txt`, poi `diff`: `f1/21d3813ca7e1/sim_kalman.py`; `t/scena_parte3.py due`; `a/a01_riaggancio.py`; `v/sim_h012.py A6 400`; `v/sim_v2.py R8 400 0.9`; `f6-specializzazione/03-avversario/conti_spec.py`; `f6-specializzazione/02-slam/bilancio_posa.py`. **Esito: regge**, sette su sette; le sole righe diverse sono tempi di calcolo. Il rilancio di `sim_v2.py` ridà i 13 falliti su 4800. **Condivide tutto** con ciò che controlla (codice, semi, macchina, Python 3.14.10): prova che i numeri sono *ripetibili*, non che il modello è giusto, né che si riproducono altrove.

## C.2 Le cifre principali

L'asterisco accanto al numero di riga dice che ho ritrovato io la cifra nel file grezzo. Stati: **S** = sostenuto dai dati in simulazione (sensore fermo); **D** = dimostrato nel modello indicato; **V** = verificato; **X** = smentito (controesempio in simulazione o conto); **C** = conto o stima, non misura; **NR** = non risolto. Nessuna riga è verificata sull'hardware.

| # | Cifra | Valore (N o intervallo) | Stato | File |
|---|---|---|---|---|
| 1* | Massa: informazione di Fisher di rango 1 | det/traccia² = 5·10⁻¹⁷ | D (punto materiale, forza ignota) | `f1/21d3813ca7e1/risultati.txt` |
| 2 | Massa da un'immagine, letteratura [lee2026] https://arxiv.org/abs/2601.20303 | errore percentuale medio 0,665 | V sulla fonte (dal curatore) | `f3/fonti/FONTI_VERIFICATE.md` |
| 3 | Accelerazione da differenze | σ ≈ 66 m/s² a 30 Hz; 7 m/s² a 10 Hz | C (due conti) | `f2/03-triage/TRIAGE.md`, F-004 |
| 4 | Tre ToF multizona [st-vl53l7cx] https://www.pololu.com/file/0J1992/vl53l7cx.pdf | 180° × 60°, non 360° | V sulla scheda | `f3/fonti/FONTI_VERIFICATE.md` |
| 5* | Campo coperto | camera 20,0 % del disco di 3 m; tre ToF +22,2 % | C | `a/risultati_a12.txt` |
| 6* | Copertura del cerchio «al 95 %», q = 0,2, a 2 s | 0,927 / 0,916 / 0,902 (± 0,004–0,007; N = 4000) | S | `t/risultati_A_parte2.txt` |
| 7 | La stessa, per chi torna indietro | 0,56–0,66 | S (sotto il nominale) | `t/risultati_A_parte2.txt` |
| 8* | Copertura con q scelto sui tratti dritti (0,01) | 0,738 / 0,710 | X (quella taratura) | `t/risultati_A2_parte2.txt` |
| 9 | Velocità costante su pedoni veri, 4,8 s [scholler2020] https://arxiv.org/abs/1903.07933 | 0,39 / 0,83 m (errore medio / finale) | V sulla fonte; camere fisse | `f3/fonti/FONTI_VERIFICATE.md` |
| 10 | Regola della bozza: «libero» falsi | 265 su 552 (173 in ombra, 92 da visibile), contro 0 | S (2D, senza rumore) | `f1/dfac83300259/CONSEGNA.md`, `PREVISIONI.md` |
| 11* | Kalman senza misure, sosta: massa su celle viste libere | 98 % a 2 s, 100 % a 3 s (100 prove) | S (1D) | `f1/e30f9e2dd4d7/esito_sim.txt` |
| 12* | Sensore in moto senza compensazione | 1,49 m d'errore; muro «mobile» 100 % | S (F-008) | `f1/21d3813ca7e1/risultati.txt` |
| 13 | Errore di profondità al limite dichiarato, a 4 m | 8 / 12 / 16 cm (D455 / Gemini 335 / D435i); i 12 cm non sono nell'uscita dello script: conto dell'arbitro | C su schede | `t/esito_attacchi_parte1.txt`; `f2/05-selezione/SELEZIONE.md` |
| 14* | Anello cieco (camera a 1,2 m, 15°) | suolo da 1,243 m; ostacolo di 15 cm invisibile sotto 1,087 m | C | `a/risultati_a03.txt` |
| 15 | Ostacolo a 1,8 m di quota | visibile solo oltre 2,41 m | C | `t/esito_attacchi_parte1.txt` |
| 16 | Griglia, Python puro, 640×480 | 20 ms (non è il prototipo) | S | `t/esito_attacchi2_parte1.txt` |
| 17* | Due persone che tornano, solo Kalman | 74 % scambi, 44 % muti (n = 100: circa ± 9 punti, conto mio) | X (identità con due nascosti) | `t/risultati_due_parte3.txt` |
| 18 | Falso «libero» che uccide l'ipotesi giusta | 4–7 fotogrammi (0,27–0,47 s) | S | `t/risultati_falso_parte3.txt` |
| 19* | Riaggancio rubato | 9,5–100 % → 0,0 % (200 scene per riga) | X, corretto (C1) | `a/risultati_a01.txt` |
| 20 | Attore a 3 m: tracce confermate | 0,4 % → 100 % a ≤ 2,3 m (500) | X, corretto (C2) | `a/risultati_a02.txt` |
| 21 | Avviso tolto dal tetto di 10 s | 15–750 fotogrammi → 0 | X, corretto (C4) | `a/risultati_a04.txt` |
| 22 | Strato 1 esteso | 45,5 m² contro 1,01 m² | X, corretto (C5) | `a/risultati_a05.txt` |
| 23 | Costo della fascia | 28,2 % dei 4,75 m² di libero visto | S (costo aperto) | `a/risultati_a05.txt` |
| 24* | Muro «mobile» con persona davanti | 100 % → 0,0–0,2 % (500); 400 → 0 su 400 | X, corretto (C6) | `a/risultati_a06a.txt`, `v/v2_WALLP.txt` |
| 25* | Garanzia per chi è visto 3 / 4 fotogrammi | traccia assente nel 27,1 % / 5,2 % | S (limite dichiarato) | `a/risultati_a07.txt` |
| 26 | Finestra fissa → che cresce | 79,0 % → 99,9 % (N = 2000) | X, corretto (C8) | `a/risultati_a08.txt` |
| 27 | «Libero» senza memoria | 11,9 cambi/s → 0,00 | X, corretto (C9) | `a/risultati_a09.txt` |
| 28 | Affidabilità persa | nessun segnale → 0,13 s e 0,00 s | X, corretto (C10) | `a/risultati_a10_correzione.txt` |
| 29 | Voce: frase a stato scaduto | 100 % → 0 % | X, corretto (C11) | `a/risultati_a11_correzione.txt` |
| 30* | Nascosto fuori dallo strato 1, Pd = 1 | 0 su 14 400 (0,75 % per cella) | S | `v/v2_R8.txt` |
| 31* | Lo stesso, Pd 0,9 e ombra a −20 cm | 13 su 4800 (≤ 0,43 %) | X (K-014, aperta) | `v/v2_R8_pd09.txt` |
| 32* | Errore d'ombra che rompe lo strato 1 | −30 cm: 8,9 %; −40 cm: 89,6 % (1200) | S (margine < 10 cm) | `v/out_SWEEP.txt` |
| 33* | Identità al ritorno, una persona nascosta | 100 %; limite inferiore 99,25 % (N = 400 per cella) | S | `v/v2_R8.txt` |
| 34* | Secondo soggetto dalla stessa ombra | 2400 su 2400 riagganci sbagliati | X (K-016) | `v/v2_SECOND.txt` |
| 35* | Riemersione nel cerchio, demo corretta | 61,1 % e 80,2 % → 100 % con C6 (N = 2000) | S con C6; X senza | `v/v2_C6.txt` |
| 36* | Costo di C6 su chi torna | 99 % → 47–50 % (N = 400) | S (K-017) | `v/v2_C6.txt` |
| 37 | Pannello da 0,5 m | 14,2–16,5 %; 20,5 % nella riprova | X (non si mostra) | `v/out_A_D_w05.txt`, `v/v2_C6.txt` |
| 38* | Durata del «previsto» nella demo | 0,40–0,53 s (mediana); buio 1,07–1,13 s | S | `v/v2_R8.txt` |
| 39* | Area prevista ancora mostrata alla riemersione | 0,5–1,2 % (demo corretta) | X (tolta dalla promessa) | `v/v2_R8.txt` |
| 40 | Falsi «mobile» sul muro, R giusto | 0 su 12 000 finestre (≤ 0,025 %) | S | `v/out_WALL.txt` |
| 41* | Lo stesso con σ creduto la metà | 31 % delle finestre scorrevoli | S (fragilità) | `v/out_WALL.txt` |
| 42* | Pedone a 0,5 m/s visto entro 1 s a 2 m | 100 % (N = 2000; ≥ 99,85 %) | S | `v/v2_MOB.txt` |
| 43* | Lo stesso da 3 m, in avvicinamento | 100 / 85,9 / 26,6 % secondo la curva | NR (decide il rumore vero) | `v/v2_MOB.txt` |
| 44* | Velocità minima vista da 2 m | 0,095–0,278 m/s secondo la curva | S | `v/out_V1.txt` |
| 45* | Traccia vera chiusa per errore, Pd 0,9, 4 s | 0,59 % (118 su 20 000) | S | `v/v2_PD.txt` |
| 46 | Strati 1 accesi a vuoto, Pd 0,9 | 12,8–14,3 % dei passaggi | S (costo) | `v/bis_R8a.txt`, `bis_R8b.txt` |
| 47 | Spazio percorso in «età + latenza» | 0,72 m a 2,5 m/s (non 0,33) | X (K-015) | `f5/02-audit/AUDIT.md` |
| 48 | Velocità coperta dalla fascia di 0,40 m | circa 1,4 m/s, a margine zero | C | `f5/02-audit/AUDIT.md`; `f6-specializzazione/03-avversario/risultati_spec.txt` |
| 49 | Latenza, voci note | circa 155 ms in media (soglia 150) | NR (R7) | `f3/H-012/02-validazione/VERIFICA.md` |
| 50 | Altezza minima del pannello | 1,45–1,50 m | C | `f5/02-audit/AUDIT.md` |
| 51 | Banda senza dato accanto all'ombra | 9,5 cm (D455), 5 cm (D435i) | C | `f5/02-audit/AUDIT.md` |
| 52 | Lavoro stimato | 54 ore-persona, 38 in fila | C (stima) | `f5/02-audit/AUDIT.md` |
| 53* | «26 su 30» promuove una taratura a 0,80 | 25,5 %; due stadi 14,2 % | D (binomiale) | `f3/H-012/03-metrologo/conti_metrologo.txt` |
| 54 | Soggetto basso nell'anello cieco | invisibile fino a 0,43 m d'altezza a 0,8 m | C, non vagliato | `f6-specializzazione/03-avversario/risultati_spec.txt` |
| 55 | Imbardata tollerata in moto | 0,87° su 0,87 s | C, non vagliato | `f6-specializzazione/02-slam/risultati.txt` |
| 56 | Indossato senza odometria | falsi «mobile» 100 % | C, non vagliato | `f6-specializzazione/02-slam/risultati.txt` |

## C.3 Requisiti e contraddizioni dopo le prove

**Requisiti** (dal verdetto, `VERDETTO.md` §3, con ciò che audit e f6 aggiungono). Nessuna misura di accettazione è stata superata: ogni requisito ha un componente e una misura *prevista*.

| R | Stato |
|---|---|
| R1 elementi mobili | **sostenuto in simulazione a 2 m** (100 %, tre curve; muro: 0 falsi su 400 con C6); oltre 2 m **non risolto**; in moto: non provato |
| R2 ostacoli | solo conto geometrico fra 1,1 e 3 m: **non verificato**; ostacoli bassi sotto 1,09 m invisibili (limite) |
| R3 interruzioni della visibilità | identità **sostenuta in simulazione** con una persona nascosta e pannello fermo; **controesempio** K-016; l'area prevista alla riemersione è tolta dalla promessa (0,5–1,2 %). È il punto che il quarto addendum riapre (estensione f8, in corso) |
| R4 osservato distinto da incerto | **per costruzione, in un solo verso**; in voce **smentito e corretto** (C11, `SOLUZIONE_V2.md` §7); rilevamenti falsi mai simulati; ramo «campo aperto» da riscrivere (K-018) |
| R5 feedback tempestivo | **corretto nel solo modello dell'avversario** (C3, C9); buchi persistenti non provati (audit, 6) |
| R6 perdita di affidabilità | **corretto nel solo modello dell'avversario** (C10: 0,13 s); dipende dai filtri della camera (audit, 1) |
| R7 bassa latenza | **non risolto** (155 ms noti contro 150; prova H12) |
| R8 sicurezza delle indicazioni | «mai libero sul non osservato»: **dimostrazione condizionata**, per costruzione (premesse: quattro stati esaustivi, buco = nessun dato, profondità valida = giusta, pavimento piano, sensore fermo). Garanzia dello strato 1: **controesempio** K-014. Vetro: **smentito**, limite dichiarato |

**Contraddizioni** (`VERDETTO.md` §3; origine in `f2/03-triage/TRIAGE.md` e `f2/05-selezione/SELEZIONE.md`).

| K | In una riga | Stato | Che cosa la decide |
|---|---|---|---|
| K-001 | traccia chiusa mentre la persona è nascosta | risolta in simulazione (nessun tetto, rilascio cella per cella); aperta sul vero | H9, H10 |
| K-002 | forma della regione prevista | risolta in simulazione (due strati); aperta sul vero | H9, H10 |
| K-003 | valore di q | risolta in simulazione (0,2); aperta sul vero | H9, H10 |
| K-004 | quando finisce il «previsto» | **aperta nel numero** («metà dell'area del cuneo» è fissata, non misurata) | — |
| K-005 | sulla sosta: continuità o perdita | decisione dell'utente | — |
| K-006 | memoria delle celle | risolta per composizione; vetro aperto | H2 |
| K-007 | regola «mobile»: spostamento o χ² | **aperta**: a 2 m passano tutte e due | H1, H8 |
| K-008 | applicazione e posa | decisione dell'utente, sciolta in parte dagli addendum | — |
| K-009 | 360° e sole | 360° risolta; sole **aperta** | H3 |
| K-010 | battito o messaggi | **aperta** | persone bendate |
| K-011 | soglie di accettazione | R3 fissata; R7 **aperta** | H12 |
| K-012 | numeri discordi sulle schede | apparente, risolta dalle fonti | — |
| K-013 | strato 1: solo ombra o celle contigue | risolta in simulazione (cuneo; 0 su 14 400) | — |
| K-014 | anomalia Pd 0,9 e ombra a −20 cm | **aperta, non decidibile senza hardware** | «libero» dentro l'ombra vera di un pannello, 150 fotogrammi, soglia 0 |
| K-015 | invariante 1 e latenza | **aperta** (0,72 m a 2,5 m/s) | H12, poi una scelta |
| K-016 | secondo soggetto mai tracciato, stessa ombra | **controesempio in simulazione**; nessuna regola lo esclude | H11; regola nuova |
| K-017 | C6 necessaria contro il suo costo su chi torna | aperta: costo da dichiarare | H9 |
| K-018 | «a meno di 0,40 m da un'ombra» vale sempre per l'ombra propria | **aperta**: difetto di scrittura | camminata in campo aperto |

I fatti F-001…F-008 restano come nel triage e nella selezione: F-002 (massa) dimostrato nel modello del punto materiale; F-005 verificato alla lettera, con la riserva su «riconoscere»; F-008 (moto proprio) mai toccato dal torneo (`f2/05-selezione/SELEZIONE.md` §3).

## C.4 Dove due file dicono cose diverse

1. **Margine dell'invariante 1.** `f4/H-012/05-correzioni/SOLUZIONE_V2.md` §3: 0,33 m, «meno della fascia». `f5/02-audit/AUDIT.md` (ipotesi 3) e `VERDETTO.md`: 0,72 m con la latenza. Vale la seconda; la soluzione non è stata riscritta.
2. **«Il pannello da 1 m regge senza C6».** `SOLUZIONE_V2.md` §5 lo afferma; `v/MISURE_V2.md` (P2c) lo smentisce: 61,1 % e 80,2 % senza C6.
3. **Area prevista ancora mostrata alla riemersione.** `SOLUZIONE_V2.md`: 0–6,2 % (T) e 9,8–18,8 % (con C6, simulatore dell'avversario). `v/MISURE_V2.md`: 0,5–1,2 % nella demo corretta (P4) e 1,6–18,5 % (P2c). Nei file grezzi, con le regole della versione 2: T-1 m 4,8 / 6,5 / 8,8 % (`v/v2_R8.txt`, letto da me), demo corretta 1,6–2,1 % con N = 2000 (`v/v2_C6.txt`). Sono rilevatori, geometrie e numerosità diversi: la cifra dipende dalla scena; in tutti i casi è sotto il 20 %.
4. **«I bracci che dovevano fallire sono falliti tutti».** Vero nella lettura principale (`v/MISURE_V2.md`); nella lettura «gruppo tagliato = ingresso» due bracci su tre danno 0 falliti su 4800 (`v/v2_R8_cut.txt`, nota dell'arbitro). Nella principale falliscono con «entrata in ombra 0»: cade la regola d'ingresso, non il contenimento (lo conferma il mio rilancio, `riprove/R5.txt`).
5. **«7198 su 7198»** (`v/MISURE_V2_bis.md`) non è stampato in `v/bis_FURTO.txt`: torna solo il denominatore (nota dell'arbitro).
6. **χ² a 0,5 m/s a 2 m.** Torneo: 75,4 % (`t/risultati_E_parte2.txt`); validazione: 99,0–100 % (`v/out_PED.txt`). Spiegazione proposta e non verificata: nel secondo simulatore il rumore cala mentre il pedone si avvicina (`v/MISURE.md`).
7. **Falsi «mobile» a soglia fissa.** 21,6 % (`f1/8f275a60e807/PREVISIONI.md`) contro 2,3 % (`t/risultati_E_parte2.txt`): filtri diversi, contraddizione apparente.
8. **Chi torna indietro.** Copertura 0,56–0,66 nel torneo, 90,2–92,2 % nella prova A (rampe a 1 m/s² che allungano il buio), 47–50 % con C6: tre scene diverse, non confrontabili.
9. **Pannello da 0,5 m.** Avversario: contenimento 86,4 % con 1 m d'ombra (`a/CONTROPROVE.md`, C2); validazione: 14,2–16,5 %, poi 20,5 % (fuori dalla fascia 14–17 % che la validazione stessa aveva previsto). Due rilevatori diversi.
10. **Durata del buio nella demo.** 0,60–0,67 s (avversario, corpo coperto a metà ancora rilevato), 1,07–1,27 s con C6, 1,07–1,13 s nella riprova.
11. **Tempo della griglia a 320×240.** 5,1 ms nel file, 4,7 ms in `t/TORNEO.md` (nota della selezione). I «2,0 ms» sono dell'autore di f1 e non stanno in nessun file del torneo.
12. **Copertura «0,902 a 2 s».** È la fascia 1,5–2,5 s del terzo generatore; sull'intero dà 0,890 (`VERIFICA.md` §1).
13. **Attacco 3.** La prima uscita (86,4 / 42,8 / 12,3 %) conteneva un errore dell'avversario ed è stata sovrascritta (95,5 / 51,8 / 21,4 %): la prima non è più verificabile.

## C.5 Ciò che nessuna prova ha ancora toccato

**Il sensore vero.** Rumore del centro di una persona a 2–4 m; maschera d'ombra da una profondità vera (errore oltre −20 cm, banda senza dato ai bordi); pixel a mezz'aria sui bordi del pannello e rilevamenti falsi (un «osservato» falso non è mai stato simulato); vetro, tessuti scuri, sole, pavimento lucido; filtri della camera che riempiono i buchi; fotogrammi persi o ripetuti; rumore correlato o con code; latenza dal fotone al suono. Nessuno script ha mai calcolato un «libero» da una profondità.

**Parti della soluzione mai provate.** Le correzioni C1–C11 tutte insieme (C3, C9, C10, C11, graduatoria dei messaggi e uscita in voce esistono solo nel simulatore dell'avversario); C7 e C12; il criterio a due stadi (solo un conto); lo stato «non confermato» e la regola sull'ultima misura; «metà dell'area del cuneo»; la seconda persona nell'atto 4 della demo; il canale dei ToF (solo un conto d'aree); il ramo asincrono con la rete (nessuna prova); `validazione-5`; l'avvio con persone nel campo; le 54 ore (stima).

**Scene.** Occlusore mobile; una persona che ne nasconde un'altra; occlusore più basso del sensore; due persone nascoste insieme con identità; pavimento non piano, rampe, gradini in discesa; ostacoli sotto 1,09 m; più di due soggetti; oggetti diversi da una persona.

**Persone.** Pedoni veri (30 occlusioni, 20 soste: H9, H10); segnali sonori con persone bendate (K-010); qualunque giudizio di chiarezza del feedback.

**Moto.** Tutto: nessuna soglia del nucleo è provata con il sensore in movimento (veicolo, drone, indossato); i conti di f6 sono requisiti, non prove; l'ombra legata all'occlusore con la parallasse non è mai stata simulata; la quota della camera diversa da 1,2 m.

**Metodo.** La rilettura indipendente della versione 2 manca (`VERDETTO.md` §2); f6 non è passato dall'arbitro; tutti i simulatori condividono modello linguistico e specifica; la ripetibilità è provata solo su questa macchina.

**Estensioni in corso (preliminari, non vagliate dall'arbitro; non riportate qui).** f7 (mappa voxel): prove dei ruoli e triage in `f7-estensione/10-triage/TRIAGE.md`. f8 (continuità visiva): prove dei ruoli e triage in `f8-continuita/10-triage/TRIAGE.md`, che propone di smentire «la continuità la porta l'avviso sull'ombra» per il movimento mostrato. f9 (preproposta esterna): consegne in `f9-preproposta/01…12`. f10 (dati pubblici): alle 16:11 è pronto l'ambiente (`f10-dati/03-infrastruttura/esito_prove.txt`: 0 prove fallite) e la ricognizione degli insiemi di dati (`f10-dati/01-ricercatore/stato.md`: nessun dato scaricato); le cartelle `f10-dati/12-dati-veri/` e `20-validazione/` sono vuote. Quindi, alle 16:15, **nessuna prova ha ancora elaborato un fotogramma di un sensore vero**.

## In coda

**File letti per intero.** `ADDENDUM_UTENTE.md`; `CONTRATTO.md`; `GATE_f1.json`, `GATE_f2.json`, `GATE_f3_H-012.json`, `GATE_f4_H-012.json` (note); `SIGILLI.jsonl`; le nove `f1/*/CONSEGNA.md`; `f2/02-firme/*.md`; `f2/03-triage/TRIAGE.md`; `f2/04-torneo/TORNEO.md`; `f3/H-012/01-scene-dinamiche/PREVISIONI.md`; `f3/H-012/02-validazione/VERIFICA.md`; `f3/H-012/03-metrologo/PIANO_MISURE.md` e `conti_metrologo.txt`; `f4/H-012/01-avversario/CONTROPROVE.md`; `f4/H-012/03-validazione/MISURE.md`, `MISURE_V2.md`, `MISURE_V2_bis.md`, `rifai.sh`, `rifai_v2.sh`, `rifai_v2bis.sh`, `v2_C6.txt`, `v2_SECOND.txt`, `v2_PD.txt`, `v2_WALLP.txt`, `v2_MOB.txt`, `bis_FURTO.txt`; `f4/H-012/05-correzioni/SOLUZIONE_V2.md`; `f4/H-012/09-arbitro/VERDETTO.md`; `f5/02-audit/AUDIT.md` e `stato.md`; `f6-specializzazione/02-slam/MOTO_PROPRIO.md` e `PREVISIONI.md`; `f6-specializzazione/03-avversario/ATTACCO_SPECIALIZZAZIONE.md` e `PREVISIONI_in_testa.txt`.
**Letti in parte.** `f2/05-selezione/SELEZIONE.md` (prime 80 righe); `f3/H-012/04-avversario/ATTACCO.md` (testa e attacchi 1–4); le `f1/*/PREVISIONI.md` (ore ed esiti, con `grep`); `f2/04-torneo/PREVISIONI_parte1…3.md` (ore); `f3/fonti/FONTI_VERIFICATE.md` e `f1/3fff79e9c3ea/FONTI.md` (righe delle fonti citate); `f4/H-012/01-avversario/risultati_a01.txt`, `risultati_a12.txt`; `f4/H-012/03-validazione/v2_R8.txt`; `f10-dati/03-infrastruttura/esito_prove.txt`, `f10-dati/01-ricercatore/stato.md`; le teste dei due `10-triage/TRIAGE.md` di f7 e f8.
**Scritti da me.** `f11-documentazione/sez-c/SEZIONE.md`; `f11-documentazione/sez-c/riprove/PREVISIONI.md` e `R1.txt`…`R7.txt` (con i rispettivi `.err`, vuoti).

**Chiavi di riferimento usate** (nessuna pagina riaperta da me; lo stato è quello dei file dello sciame).

| Chiave | Fonte | Link | Stato nei file |
|---|---|---|---|
| [scholler2020] | Schöller, Aravantinos, Lay, Knoll, «What the Constant Velocity Model Can Teach Us About Pedestrian Motion Prediction», RA-L 5(2), 2020 | https://arxiv.org/abs/1903.07933 | verificata dal curatore (`f3/fonti/FONTI_VERIFICATE.md`) |
| [lee2026] | Lee, Jeong, Hong, Kim, «Physically Guided Visual Mass Estimation from a Single RGB Image», arXiv 2601.20303 | https://arxiv.org/abs/2601.20303 | verificata dal curatore |
| [st-vl53l7cx] | STMicroelectronics, scheda VL53L7CX, DS13865 Rev 6 (copia Pololu) | https://www.pololu.com/file/0J1992/vl53l7cx.pdf | verificata dal curatore |
| [realsense-tuning] | RealSense, «Tuning depth cameras for best performance» | https://dev.realsenseai.com/docs/tuning-depth-cameras-for-best-performance | aperta dal ruolo che la cita (`VERIFICA.md` §4); formula non letta; non nel file del curatore |
| [realsense-highspeed] | RealSense, «High-speed capture mode of the D435» | https://dev.realsenseai.com/docs/high-speed-capture-mode-of-intel-realsense-depth-camera-d435 | aperta dal ruolo che la cita (`VERIFICA.md` §3c); non nel file del curatore |
| [realsense-filtri] | RealSense, «Post-processing filters» | https://dev.realsenseai.com/docs/post-processing-filters/ | vista solo nel riassunto di ricerca (`AUDIT.md`) |
| [pipewire-conf] | PipeWire, pagina di manuale `pipewire.conf(5)` | https://docs.pipewire.org/page_man_pipewire_conf_5.html | citata dal ruolo (`VERIFICA.md` §3c); apertura non dichiarata |
| [ultralytics-coco] | Ultralytics, elenco delle 80 classi COCO (`coco.yaml`) | https://raw.githubusercontent.com/ultralytics/ultralytics/main/ultralytics/cfg/datasets/coco.yaml | aperta dall'avversario del torneo (`t/TORNEO.md`, parte 1) |
