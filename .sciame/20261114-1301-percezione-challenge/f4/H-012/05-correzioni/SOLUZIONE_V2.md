# Soluzione integrata, versione 2 — ramo H-012, f4 (`sciame-scene-dinamiche`, responsabile)

**In testa.** Scritta dalle 2026-11-14T14:36:04+01:00 (`date -Is`). **Cambi di stato:** della versione 1 cadono sette regole (riaggancio, tetto di tempo, strato 1 esteso, rilascio sul punto previsto, geometria della demo, graduatoria dei messaggi, frasi in voce) e l'invariante 1 è **indebolito** di proposito; due mie previsioni sono smentite (la χ² in avvicinamento a 2 m: 99–100 % contro il 70–80 % previsto; «nessuna regola vede oltre 3 m»: 98,5 % da 4 m con la curva nominale). **Limiti di questa versione:** non ho eseguito prove; le cifre vengono da `CONTROPROVE.md` (avversario) e `MISURE.md` (validazione), e dei file dei risultati ho riaperto solo `risultati_a01.txt` e `risultati_a12.txt`; le correzioni sono provate **una per una, mai insieme** (§9). Tutto è simulazione o scheda, **a sensore fermo**: nessuna riga è verificata sul vero. I conti **[resp.]** sono miei, a mano.

## 1. L'architettura in una riga

Camera stereo attiva ferma → griglia polare a quattro stati → gruppi di punti sopra il suolo → associazione → Kalman a velocità quasi costante → tre stati per traccia (**osservato / previsto / perso**) con due strati durante l'occlusione → tabella di regole su una zona dichiarata → segnali brevi e schermo. Una rete gira a parte e mette solo un'etichetta.

**Che cosa resta del nucleo, detto chiaro.** La macchina a tre stati regge. Cambia il peso: alla scala della demo il buio dura 0,60–0,67 s (1,07–1,27 s con la correzione C6), lo stato «previsto» dura 0,6–0,7 s e alla riemersione lo strato 2 è quasi sempre già spento (ancora mostrato nello 0–6,2 % dei transiti nella geometria del torneo, con 2 m d'ombra, nel 9,8–18,8 % con C6 alla scala della demo). **La continuità la porta lo strato 1**, non l'area prevista: la traccia resta pendente nell'ombra e si riaggancia con la stessa identità (100 % con una sola traccia pendente, N = 400 per cella, limite inferiore 99,25 %). La demo mostra quindi: a schermo, una traccia che diventa per un attimo un'area «probabile», poi un cuneo «possibile presenza» con la sua età, poi la stessa identità che ricompare; in voce, tre segnali brevi diversi.

## 2. I blocchi

**B1. Sensore e montaggio.** Camera stereo attiva con IMU posseduta dalla squadra (D455, D435i: 87°×58°; Gemini 335: 90°×65°), 30 fps, elaborazione a 15 Hz. Su treppiede a 1,2 m (ipotesi), orizzontale, inclinata di 15°. **Portata dichiarata: dove il rumore radiale del centro di una persona resta ≤ 5 cm**, da misurare; le curve usate nelle prove danno a 2 / 3 / 4 m 1,5 / 3,4 / 6,0 cm (nominale, documento del costruttore), 4 / 9 / 16 (pessimista), 5 / 11 / 20 (torneo). Griglia fino a 3 m. **Limiti dichiarati:** suolo visto solo da 1,24 m (anello cieco: 30 % dell'estensione 0,5–3 m); ostacolo di 15 cm invisibile sotto 1,09 m; ostacolo a 1,8 m di quota visto solo oltre 2,41 m. Costo: 3 ore. Invalidata se: sole, sensore indossato.

**B2. Griglia.** Polare egocentrica, 1° × 0,1 m. Stati: **libero** (suolo visto alla quota attesa e nessun ostacolo), **occupato osservato** (primo ritorno fra 0,07 e 2 m di quota), **in ombra** (oltre il primo ritorno), **non osservato** (fuori campo, oltre portata, anello cieco, buco). «Libero» vale se il suolo è visto **in almeno uno degli ultimi 3 fotogrammi**, con la sua età (0,13 s); una cella diventa «buco» dopo 3 fotogrammi non validi di fila; «occupato ricordato» esce con l'età. Pavimento piano dichiarato. Costo: 6 ore; 20 ms a 640×480 in Python puro su scene sintetiche (non è il prototipo). Invalidata se: rampe, vetro (la lastra risulta «libero» in ogni griglia: limite aperto), suolo valido in meno del 95 % dei fotogrammi (a 0,80 le correzioni C3 e C9 non bastano).

**B3. Rilevamento e regola «mobile».** Gruppi connessi di celle occupate, con centro e larghezza. Un gruppo è «mobile» se lo spostamento fra **due misure distanti al più 1 s** (finestra che cresce), ciascuna **media di 3 fotogrammi**, supera 5·σ(z)·√2 lungo un asse. **Un gruppo tagliato da un'ombra non entra nella finestra e non aggiorna il filtro.** Si registra in parallelo la χ² con R(z). **K-007 resta non risolta: la decide il rumore misurato.** A 2 m in avvicinamento passano tutte e due (100 % e 99,0–100 %, N = 2000); da 3 m lo spostamento dà 100 % / 10,8 % / 0,1 % e la χ² 100 % / 56,7 % / 45,2 % secondo la curva. Tengo lo spostamento come scelta provvisoria per un solo motivo misurato: 0 etichette false nel primo secondo di una traccia ferma, contro lo 0,15–2,3 % della χ² (N = 4000). Costo: 6 ore. Invalidata se: misure anomale (con il 2 % la media porta i falsi sul muro al 5,7–14,9 %); σ creduto la metà del vero (31 % delle finestre scorrevoli con un'etichetta falsa).

**B4. Associazione e stimatore.** Kalman [x, y, vx, vy], q = 0,2 m²/s³, R(z) per asse; porta al 99 %, ungherese, priorità alle confermate; conferma con 3 rilevamenti su 5. q si tara sulle innovazioni alla ricomparsa, su 15 passaggi **diversi** da quelli del criterio. Copertura del cerchio intero al 95 %: 0,89–0,93 nel torneo, per miscele con pochi ritorni (0,56–0,66 per chi torna). Niente massa, niente accelerazione. Costo: 5 ore. Invalidata se: due persone tornano insieme (con q = 0,2: 74 % di scambi, 44 % muti: per questo l'identità con due tracce pendenti non si dà mai).

**B5. Ciclo di vita e due strati.** Senza misura si guarda **l'ultima misura**, non il punto previsto:
- a meno di 0,40 m da un'ombra → la traccia è entrata in quell'ombra: partono i due strati;
- in campo aperto → «non confermato» con l'età per al più 3 fotogrammi (non è «osservato» e non si disegna come area), poi traccia chiusa come «non più rilevato»;
- buco → «affidabilità persa».

**Strato 1, garanzia.** È il **cuneo d'ombra dell'occlusore** in cui la traccia è entrata, tagliato alla griglia e dilatato di una fascia di 0,40 m: «possibile presenza», con la sua **età**. Non ha tetto di tempo. Si rilascia solo per riaggancio o **cella per cella**, quando una cella è «libero» per ≥ 3 fotogrammi oltre la fascia (con l'occlusore fermo: mai). Ciò che sta oltre la portata o fuori campo non è strato 1: è «non osservato», mai «libero».
**Strato 2, informazione.** Cerchio al 95 % ritagliato sul cuneo, mostrato come «probabile» finché copre meno di metà dell'**area del cuneo in griglia**. Poi lo stato è **«perso»**, ed è assorbente fino al riaggancio. Con un solo punto di vista il cuneo arriva sempre al bordo della portata: «perso» si dice quindi sempre «possibile presenza, **può aver lasciato l'area**».
**Ritorno.** Si riaggancia solo un rilevamento entro la fascia dell'ombra d'ingresso, a più di 0,40 m da ogni altro bordo del non osservato, con una sola traccia pendente. Altrimenti «identità ambigua», e lo strato 1 resta.
**Portata della garanzia:** vale per chi è stato tracciato (visto ≥ 4 fotogrammi: con 3 la traccia manca nel 27,1 % dei casi, con 4 nel 5,2 %). Un'ombra in cui non è entrato nessuno resta «in ombra».
Costo: 9 ore. Invalidata se: errore della maschera d'ombra oltre −20 cm (a −30 cm l'8,9 % dei passaggi esce dallo strato 1; con un corpo di 60 cm il 33,3 %); occlusore mobile; rilevamenti falsi al bordo del pannello.

**B6. Ramo asincrono.** RGB a bassa frequenza → etichetta persona / non persona su una traccia già esistente, a schermo. RF-DETR-N (Apache 2.0) o YOLO26n (AGPL-3.0). Non crea tracce, non tocca celle, non decide allarmi. Costo: 4 ore; se manca, la catena non cambia.

**B7. Decisione.** Tabella di regole, non appresa. **Zona di valutazione dichiarata: 1,24–3 m dentro il campo.** Anello cieco, fuori campo e oltre portata si dicono una volta all'avvio e non entrano nel messaggio per fotogramma. Dentro la zona, per settore: buco > mobile in avvicinamento > occupato > previsto > perso con possibile presenza > in ombra > «nessun ostacolo osservato fino a d metri». Mai «via libera». Costo: 3 ore.

**B8. Feedback e affidabilità persa.** **In voce un segnale breve per stato (0,3 s)**, diverso per osservato, previsto, perso; la frase «direzione, distanza, stato» solo a stato stabile. Schermo a tre colori con età e contatore della latenza. «Affidabilità persa» esce se: manca un fotogramma nuovo o tre sono identici (0,13 e 0,07 s); **le celle valide scendono sotto metà della taratura per 3 fotogrammi**; **l'IMU si scosta di 0,5° o supera 5°/s**. Il contatore del sensore viaggia fino all'uscita. Per la latenza: flusso a 60 o 90 fps usando l'ultimo fotogramma, suoni preregistrati, uscita via cavo. Costo: 6 ore.

**B9. Demo e accettazione.** Cinque atti: campo mezzo coperto; ostacolo fermo oltre 1,1 m; attraversamento; passaggio dietro il pannello, mentre una seconda persona si muove in vista; sosta o mano sul sensore. **Attore sulla linea a non più di 2,3 m; pannello largo 1 m.** Il pannello da 0,5 m si mostra solo dopo dieci passaggi riusciti sull'hardware. Accettazione sulle registrazioni riprodotte, non dal vivo: protocollo H0–H13 del metrologo (due persone, circa 2 h 40), con H0–H6 nella prima ora. Costo: 12 ore. Totale stimato: **circa 54 ore-persona** (stima mia).

## 3. Invarianti

1. **(riscritto, più debole)** «Libero» esiste solo dove il suolo è stato visto in almeno uno degli ultimi 3 fotogrammi; esce con l'età e non si deduce mai. A v_max = 2,5 m/s in 0,13 s sono 0,33 m [resp.], meno della fascia.
2. Buco, fuori campo, oltre portata, anello cieco, ombra: mai «libero».
3. Nessuna uscita «osservato» senza una misura in porta nel ciclo. **Vale in un solo verso:** un rilevamento falso al bordo del pannello uscirebbe «osservato».
4. «Previsto» e «possibile presenza» non stanno su celle «libero» oltre la fascia.
5. Nessun timer e nessun modello appreso produce un «libero», toglie un avviso o decide un allarme.
6. Evidenza negativa solo dove la profondità è valida, e mai sul punto previsto.
7. Lo strato 1 finisce solo per riaggancio o per celle viste libere.
8. Ogni uscita porta il contatore del sensore. **Necessario, non sufficiente:** servono anche la quota di celle valide e l'IMU.
9. Una grandezza non osservabile non compare in uscita.

## 4. Correzioni: prima → dopo, con il controesempio

File: `a` = `f4/H-012/01-avversario/`, `v` = `f4/H-012/03-validazione/MISURE.md`.

| # | Prima → dopo | Numero che smentiva | Dopo | File |
|---|---|---|---|---|
| C1 | riaggancio al bordo entro v_max·τ → solo entro la fascia dell'ombra d'ingresso | riaggancio sbagliato e muto 9,5–100 % (200 scene per τ) | 0,0 %; costo: legittimi 100 % fino a 2,3 m, 86,3 % a 2,5 m, 0 % a 2,8 m | `a/risultati_a01.txt` |
| C2 | attore a 3 m → a ≤ 2,3 m | tracce confermate 0,4 % (500 transiti) | 100 % | `a/risultati_a02.txt` |
| — | pannello 0,5 m → 1 m | contiene alla riemersione 14,2–16,5 % | 97,0–100 % (a 2,5 m) | `v`, A3 |
| C3 | «non osservato» sempre primo → zona dichiarata, buco dopo 3 fotogrammi | «mobile in avvicinamento» detto nello 0 % | 100 / 100 / 99,5 % (suolo valido 1 / 0,99 / 0,95) | `a/risultati_a03_correzione.txt` |
| C4 | tetto T_g = 10 s → età, nessun tetto | 15–750 fotogrammi di nascosto fuori dallo strato 1 (soste di 11–60 s) | 0 | `a/risultati_a04.txt` |
| C5 | strato 1 con le celle contigue → solo il cuneo | copriva il 100 % del non osservato (45,5 m² contro 1,01) | 1,01 m² | `a/risultati_a05.txt` |
| A7 | rilascio dal raggio sul punto previsto → cella per cella | rilascio a soggetto nascosto 92,5–99,5 % (sosta) | nessuno (per costruzione) | `v`, A7 |
| C6 | gruppo tagliato dall'ombra usato → escluso | muro «mobile» nel 100 % (500 passaggi); contenimento 70,8–85,8 % | 0,0–0,2 %; 100 % | `a/risultati_a06a.txt`, `a06c` |
| C8 | finestra fissa di 1 s → che cresce | visto entro 1 s 79,0 % (Pd 0,9) | 99,9 % | `a/risultati_a08.txt` |
| V1 | misure singole → media di 3 ai due capi | velocità minima 0,380 m/s (curva del torneo) | 0,278 m/s; da 3 m, curva pessimista: 10,8 → 95,0 % | `v`, `validazione-1` |
| C9 | «libero» solo nel fotogramma → 3 fotogrammi | 11,9 cambi/s (suolo valido 0,95) | 0,00 per direzione, 0,65 per settore | `a/risultati_a09.txt` |
| C10 | solo contatore → anche celle valide e IMU | nessun segnale in 3 s con il 10 % di valide, né dopo un urto | 0,13 s e 0,00 s; 0 falsi in 60 s | `a/risultati_a10_correzione.txt` |
| C11 | frasi → segnali di 0,3 s | frase finita a stato scaduto nel 100 % | 0 % | `a/risultati_a11_correzione.txt` |
| M4 | 26 su 30 secco → due stadi (≥ 28 regge, ≤ 22 smentita, altrimenti altri 30 e ≥ 52 su 60) | passa una taratura mediocre (0,80) nel 25,5 % | 14,2 % | `f3/H-012/03-metrologo/PIANO_MISURE.md` |

## 5. Dove due prove tirano in versi opposti

**Strato 1: C5 contro A1.** L'avversario mostra che con le celle contigue lo strato 1 è tutto il non osservato e non informa. La validazione mostra che con il solo cuneo chi esce dalla portata restando in ombra finisce fuori dallo strato 1 in 400 passaggi su 400. **Regola sola:** strato 1 = cuneo tagliato alla griglia (C5); «contenuto» si legge come propone il metrologo (critica 2): fallisce solo un fotogramma in cui il centro del soggetto senza misura sta in una cella che non è né strato 1, né «occupato osservato», né «non osservato». Chi esce dalla portata sta in «non osservato»: non è un fallimento, e l'uscita lo dice («può aver lasciato l'area»). **Previsione, scritta alle 2026-11-14T14:37:51+01:00 prima di ogni nuova prova:** rifacendo A1 con questa lettura e w_min = 0,15 m, 0 passaggi falliti su 400 per cella, anche nel caso «lontano». **La smentisce** un solo fotogramma con il centro in una cella «libero». **Braccio che deve fallire:** fascia a 0 o 0,20 m con l'ombra a −20 cm; se non fallisce, la prova è cieca. Il «regge» atteso vale come controllo dell'invariante, non come dato.

**Pannello da 0,5 m: C2 contro A3.** L'avversario ottiene 100 % di tracce e contenimento 86,4 % con 1 m d'ombra (pannello stretto); la validazione, con un altro rilevatore, 14,2–16,5 %. La causa trovata dalla validazione (il centro della parte visibile rallenta il filtro) è quella che C6 corregge nel simulatore dell'avversario (100 %), ma C6 non è stata riprovata in quello della validazione. **Non scelgo:** la demo usa il pannello da 1 m, che regge senza C6.

**C7, seconda metà, non adottata:** «ogni ombra che tocca un bordo è possibile presenza anche senza traccia». Ogni cuneo tocca il bordo della portata: la regola rimetterebbe l'avviso ovunque e annullerebbe C5. Non è provata. L'ombra senza traccia resta «in ombra», mai «libero».

**Costo che nessuna riga chiude:** la fascia di 0,40 m mette «possibile presenza» sul 28,2 % del libero visto (4,75 m²); lo strato 1 sta su suolo davvero visibile per il 37–68 % alla scala della demo. Il margine oltre −20 cm d'errore è meno di 10 cm.

## 6. Decisioni dell'utente e scelte ancora in gara

| Tema | Default | Altro caso, o prova che decide |
|---|---|---|
| Applicazione e posa | sensore fermo; l'applicazione è coperta **per lettura** | indossato: nessuna soglia vale; dopo 10° d'imbardata i gruppi fermi risultano «mobile» nel 96–100 % |
| Sosta | «perso» con possibile presenza ed età | particelle con modo «sosta»: 76 % con ombra larga |
| Regola «mobile» | spostamento, χ² registrata | rumore del centro di una persona a 2–4 m (H1, H8) |
| Feedback | segnali brevi e schermo | battito: tre persone bendate, ≥ 54 su 60 |
| Montaggio | orizzontale a 15° | verticale: suolo da 0,74 m; oppure un ToF in basso |
| Fine del «previsto» | metà dell'area del cuneo | non risolta: le letture davano da 0,8 a 5,8 s |

## 7. Copertura R1–R8 dopo le prove

| R | Componente | Misura e soglia | Stato |
|---|---|---|---|
| R1 | B3 | 9 su 10 entro 1 s a 0,5 m/s, fino a 2 m in avvicinamento; falsi sul muro ≤ 10 % | **regge in simulazione** a 2 m (100 %, N = 2000; falsi 0 su 12 000 finestre con R giusto); finestra fissa **smentita e corretta** (79,0 → 99,9 %); oltre 2 m **non risolta** |
| R2 | B1, B2 | 5 su 5 entro 15 cm fra **1,1 e 3 m** | **smentita e corretta** nell'ambito (scatola a 0,8 m: 0 su 5); non verificato fino all'hardware |
| R3 | B5 | stessa identità al ritorno, criterio a due stadi su 30 occlusioni; a parte, la quota con «previsto» ancora mostrato | identità: **regge in simulazione** (100 %, limite inferiore 99,25 %); riaggancio **smentito e corretto** (C1); «area prevista ancora mostrata»: **smentita** (0–6,2 %), tolta dalla promessa |
| R4 | B5, B8, invarianti 3, 4 | 0 fotogrammi «osservato» a soggetto nascosto, esclusa la transizione | **per costruzione, in un solo verso**; in voce **smentita e corretta** (C11); rilevamenti falsi: non verificato |
| R5 | B7, B8 | ≤ 300 ms dal primo fotogramma con l'ostacolo alla chiamata audio | **smentita e corretta** nel modello (C3, C9); non verificato fino all'hardware |
| R6 | B8 | segnale entro 1 s, 10 prove per causa; 0 falsi in 60 s | **smentita e corretta** (C10: 0,13 s; rumore dell'IMU ipotizzato); non verificato sulla camera |
| R7 | B2, B8 | p95 ≤ 150 ms dalla marca di cattura alla chiamata audio | **non risolta**: le sole voci note sommano circa 155 ms in media dal fotone alla scheda audio |
| R8 | B2, strato 1 | 0 «libero» su celle non osservate; contenuto nella lettura del §5 | **per costruzione**: nessun «libero» falso in dodici attacchi; 0 fuori su 19 200 passaggi nella lettura estesa; la regola nuova non è riprovata. **Vetro: smentito**, limite dichiarato |
| Applicazione | decisione dell'utente (§6) | orientamento assistito con sensore e utente fermi | coperta **per lettura**, senza misura; il monitoraggio di attività non è coperto |

«Riconoscere»: lo copre B6, per lettura dichiarata. «Mentre la scena continua a cambiare»: solo la seconda persona dell'atto 4, senza misura.

## 8. Idea di partenza → esito, e stato dell'arte

| Idea | Esito | Perché |
|---|---|---|
| 3 ToF a 360° | **corretta** | non danno 360° (tre multizona: 180°, scheda ST), ma servono come **canale laterale facoltativo di sola prossimità, mai «libero»**: la camera vede il 20,0 % del disco di 3 m, tre ToF da 60° fino a 2 m aggiungono il 22,2 %; uno in basso copre 0,68 dei 0,98 m² dell'anello cieco. Non verificato: le cifre dei ToF, l'interferenza, la portata con luce (a 5 klx il VL53L7CX tiene 0,5–0,65 m) |
| Mappa del terreno | **corretta** | griglia locale su pavimento piano dichiarato |
| Classificazione | **corretta** | solo persona / non persona, asincrona |
| Massa, accelerazione | **escluse** | non osservabile (F-002); sotto il rumore (F-004) |
| Velocità | **confermata** | stato del filtro; minima vista 0,095–0,278 m/s da 2 m secondo la curva |
| Previsione fuori vista | **corretta, ridotta** | un'area che dura meno di un secondo; poi «possibile presenza» |
| Kalman → transformer → decision model | **corretta** | rilevamento → associazione → Kalman → regole (F-003) |

Stato dell'arte (fonti in `f3/fonti/FONTI_VERIFICATE.md`). Entra nel ramo asincrono un rilevatore in tempo reale: RF-DETR-N, 2,3 ms su T4, Apache 2.0 (https://github.com/roboflow/rf-detr); YOLO26n, 38,9 ms su CPU, AGPL-3.0 (https://docs.ultralytics.com/models/yolo26/). Entra come schema l'associazione alla SORT / OC-SORT (https://arxiv.org/abs/2203.14360). Restano fuori: SAM 3 (30 ms a immagine su H200) e i modelli video con memoria (TAPNext 187 fps su H100; SAMURAI non lavora dal vivo), per il calcolo e perché un modello appreso qui non decide; la profondità monoculare, perché la profondità è misurata.

## 9. Ciò che la versione 2 afferma senza prova nuova

1. Le correzioni C1–C11 **insieme**: ognuna è provata da sola.
2. Lo strato 1 come cuneo con la lettura del metrologo (§5): previsione scritta, prova non eseguita.
3. La geometria «pannello da 1 m, attore a 2,3 m»: C2 e A3 la toccano da due lati, nessuno l'ha simulata.
4. Finestra che cresce con la media di 3 fotogrammi: provate separatamente.
5. «Non confermato» per 3 fotogrammi in campo aperto e la regola sull'ultima misura: definizioni mie.
6. «Metà dell'area del cuneo» e «perso» assorbente: fissate, non rimisurate.
7. La seconda persona nell'atto 4.
8. Il canale dei ToF: solo un conto d'aree.
9. Le 54 ore-persona.
10. Tutto ciò che dipende dal sensore vero: rumore, maschera d'ombra, vetro, tessuti scuri, sole, rilevamenti falsi al bordo, latenza, feedback con persone bendate.
