# Torneo dei falsificatori — f8, continuità visiva (`sciame-avversario`, fase f2)

Lavoro dalle 16:00 alle 16:34 del 14 novembre 2026 (`date -Is`). 54 lanci, ognuno entro il suo `timeout 120`. Tutto è **simulazione mia, a sensore fermo, soggetto puntiforme** (salvo il §3.4).

## 0. In testa: cambi di stato, scostamenti, indipendenza

**Cambi di stato proposti.**
- **C-EST com'è scritta: smentita** sui suoi stessi attacchi 1 e 5, su K-201 e su K-206 (§1).
- **Ciclo di vita del nucleo (B5): smentito.** La regola «ultima misura a meno di 0,40 m dall'ombra» chiude la traccia mentre il soggetto entra nell'ombra: nessuno strato 1, nessuna previsione (§2).
- **«R100 = raggiungibile ∩ non visto libero»: smentita** a 3 m/s. R100 deve essere lo strato 1 (§3.1).
- **C-004 (fronte + scia): regge fino a 3 s sul percorso**, da riformulare a 5 s e fuori percorso (§4).
- **C-001 (particelle): smentita oltre 10 s di sosta** (§3.1).
- **S2: da riformulare.** Il segno pieno compensato finisce dentro l'ombra (§3.6).

**Scostamenti.**
- Un lancio esplorativo (T, 200 per comportamento, semi 9000+) è stato visto **prima** di cinque correzioni al simulatore (area sulle sole celle d'ombra; contatore di μ1; C-001 senza lisciatura, come l'autore; ellisse «dichiarata»; opzione `-fixentry`): i semi di prova sono stati toccati due volte.
- Le 20 previsioni (`PREVISIONI.md`, 16:04:13) precedono il codice: 7 reggono per intero, 1 è smentita per intero, 12 sono miste. La ventunesima (`-fixentry2`) è nata dopo aver visto `-fixentry`: scritta prima del suo lancio, smentita sui cicli. I cinque lanci `-fixentry` sono stati rifatti con l'eseguibile finale; gli altri sono identici prima e dopo (impronta controllata su `a1_T`).
- **Non letti:** le consegne di requisiti, kalman, statistico, inferenza, visualizzatore, rovesciatore (note dal triage); `MISURE_V2*.md`, `AUDIT.md`, `VERDETTO.md`. **Non eseguiti:** due soggetti che si incrociano dietro l'ostacolo; K-211. Le **ore** sono stime **non verificate**.

**Indipendenza.** Scena, generatore, sensore, ciclo di vita e predittori sono codice mio (`torneo.c`, `s2.py`). C-004 e C-001 li ho riscritti dopo aver letto `cono2.py` e venti righe di `cont.c`: ne condivido la lettura (celle da 0,25 m, lisciatura, tassi 0,25 e 0,4 al secondo). Favori dichiarati: la libreria di C-004 e la tabella di C-005 vengono dal mio stesso generatore (semi 1000+). Condiviso con tutto: un autore e un modello linguistico, griglia cartesiana da 0,10 m, nessun falso allarme, C6 emulata sul bordo **vero** dell'ombra.

Scene: **D** demo (pannello 1 m a 1,9 m, soggetto a 2,3 m, portata 3 m), **T** (1 m a 2 m, soggetto a 4 m, portata 6 m), **L** (pannello 2 m). τ = tempo dall'ultima misura. Base: 400 passaggi per comportamento e scena, 0,3–1,8 m/s, rilevamento 0,9.

## 1. C-EST (S3 + S4), com'è scritta: smentita

Letture del triage: **A** = smorzamento 0,90 a ciclo, pesi cumulati; **B** = 0,95, pesi 0,8 e 0,2 per la massa corrente. Scelte mie: la massa su celle non osservate (fuori campo, oltre portata) conta come «ancora nascosta», come dice S4.1; regione = massima densità al 90 % della miscela ritagliata; σ_eff = radice della media delle due varianze.

| Attacco | Esito | Numeri |
|---|---|---|
| 1a, «previsto» su celle libere | **regge** con la fascia di 0,20 m (0 cicli); senza fascia tocca celle viste libere nel 25–86 % dei cicli | `ris/a1_*.txt` |
| 1b, peso del transito dominante oltre l'uscita attesa + 0,5 s | **rigetto.** B: 191 passaggi su 198 (T), 174 su 202 (D). A: 12 su 198 (T), ma **174 su 202 in D**: μ1 scende a 0,14 a 2 s e risale a 0,97 a 5 s | idem |
| 1c, vero dentro la regione (sosta a metà pannello) | A in T: 0,98 / 0,93 / 0,93 a 2 / 3 / 5 s. A in D: 0,88 / 0,70 / **0,00**. B: 0,66 a 2 s in T (0,02 in D), poi 0,00 | idem |
| 5, prima misura nell'ellisse al 95 % (341–350 «prosegue») | **rigetto.** Ellisse dichiarata (stato ancora «previsto»): A 0,320 (T), 0,777 (D), 0,000 (L); B 0,484, 0,669, 0,000. Contando anche le ellissi dopo «perso»: A 0,566 in T; B 1,000 | `ris/base_*.txt`, §4 |
| K-201, una regione a ogni ciclo | **no.** Cicli nascosti senza regione: A 23–31 % (T), 24–49 % (D), 58–68 % (L); B 27–66 % | idem, §2 |
| K-206, «sosta» a 3 s ≥ 0,85 | **no.** A 0,531 (T), 0,460 (D), 0,000 (L); B 0,000 | idem, §1 |
| Errore dentro l'incertezza dichiarata da 0,5 a 3 s | **no** oltre 2 s: «perso» nel 95 % dei «prosegue» a 3 s (T e D), nel 100 % in L | idem, §6 |

**Perché cade.** Con i pesi cumulati (A) la stessa evidenza si rimoltiplica a ogni ciclo: quando H1 esce dal campo osservato smette di perdere peso, mentre H2, ferma in un'ombra stretta, continua a perderne, e in D vince il fantasma che se n'è andato. Con i pesi non cumulati (B) il transito resta sopra 0,7 per sempre. La soglia σ_eff ≤ 0,8 m scatta fra 2 e 3 s in ogni scena, anche nella demo: da lì C-EST non mostra più una regione. È il difetto del nucleo, spostato di 1,5 s.

**Che cosa resta di C-EST:** le regole di disegno S5 e l'elenco degli attacchi. La sua riformulazione corretta (troncare e rinormalizzare, non solo pesare) è C-002, che non ho provato.

## 2. Il nucleo perde la traccia all'ingresso (sicurezza, indipendente dal predittore)

B5 decide «è entrato nell'ombra» dall'ultima misura (entro 0,40 m). C6 toglie le misure negli ultimi 0,22 m. Restano 0,18 m, cioè 1,5 cicli a 1,8 m/s: un rilevamento mancato e la traccia è «in campo aperto», chiusa dopo 3 fotogrammi come «non più rilevato». Il soggetto è dietro il pannello senza traccia pendente, senza possibile presenza, senza previsione. `SOLUZIONE_V2.md` §9 lo dichiarava: le correzioni non sono mai state provate insieme.

Misura: passaggi con almeno un ciclo a soggetto nascosto senza traccia pendente (fra parentesi i cicli).

| Caso (passaggi) | Regola di oggi | Punto previsto guardato alla chiusura (`-fixentry`) | Guardato a ogni ciclo senza misura (`-fixentry2`) |
|---|---|---|---|
| Base, rilevamento 0,9, T (2800) | 87 (8486); D 111, L 113 | 18 (531) | **9 (522)** |
| Rilevamento 0,7, T (600) | 72 (6898) | 20 (984) | 11 (975) |
| Ombra stimata −20 cm, T (600) | **499 (73 314)**; D 194 | 163 (4395) | 16 (4243) |
| Corsa a 3 m/s, L (400) | 119 (7542); D 172 | 108 (369) | 3 (211) |
| Vuoto falso di 0,3 s a 0,7 m dall'ombra, D a 1,2 m/s (200) | 200 (10 209); a 0,5 / 0,9 / 1,2 m: 197 / 148 / 35 | 138 (6968) | 136 (6912): **non basta** |

**Riga riscritta (B5).** «A ogni ciclo senza misura: se l'ultima misura è a meno di 0,40 m da un'ombra, **oppure se il punto previsto sta in un'ombra o entro 0,40 m**, la traccia è entrata in quell'ombra.» Usa la previsione solo per **accendere** un avviso, mai per toglierlo (l'invariante 6 e la correzione A7 restano). I cicli che restano scoperti stanno in pochi passaggi dove la traccia era già persa prima dell'ombra (mia previsione sui cicli: smentita). Costo: mezz'ora. **Indispensabile nelle 14 ore.** Il vuoto falso di 0,3 s resta un limite da dichiarare.

*Avvertenza.* L'83 % dipende dalla mia emulazione di C6 sul bordo vero. Se C6 lavora sulla maschera stimata, il difetto diventa quello del §3.4.

## 3. Attacchi alle candidate (C-004, C-001, C-005W = tabella sul comportamento peggiore)

### 3.1 Fuori dal modello

| Caso | C-004 | C-001 | C-005W | Limite esterno |
|---|---|---|---|---|
| Lato lontano, R90 a 2 / 3 s (T) | 0,49 / 0,30 | 0,62 / 0,47 | 0,93 / 0,91 | strato 1: 1,000 |
| Svolta, 2 / 3 s (T) | 0,64 / 0,51 | 0,77 / 0,73 | 0,99 / 0,99 | 1,000 |
| Svolta verso il sensore, 2 / 5 s (T, n = 177 / 156) | 0,51 / 0,13 | 0,60 / 0,49 | 0,99 / 0,89 | 1,000 |
| Sosta di 30 s: 10 / 20 / 30 s (T, n = 89) | 0,97 / 0,94 / 0,94 | 0,99 / **0,32 / 0,045** | 1,00 | 1,000 |
| Corsa a 3 m/s con sosta, 1 / 2 / 3 s (L) | 0,97 / 0,96 / 0,95 | 0,97 / 0,98 / 0,99 | 0,80 / 0,53 / **0,14** | raggiungibile (2,5 m/s): mancato in **138 passaggi su 138**; strato 1: 0 |
| Inverte tardi, 3 / 5 s; accelera, 3 s | 0,93 / 0,80; 0,86 | 0,99 / 0,98; 1,00 | 1,00 | 1,000 |

- **Sosta di 30 s.** La nube di C-001 riparte (0,4 al secondo), esce e muore: a 30 s la regione è il 4 % dell'ombra e contiene il soggetto nel 4,5 % dei casi. È la «continuità che inganna» più netta trovata. Riga riscritta: «C-001 vale fino a 10 s; poi "previsto ampio" su R100».
- **Estraneo (attacco 2).** Un secondo soggetto mai visto esce dalla stessa ombra mentre il primo è fermo dentro: su 357 casi la regola «Ritorno» del nucleo riaggancia l'estraneo, e toglie la possibile presenza, in **347 (97 %)**. Una porta su R90 dilatata di 0,45 m non aiuta (C-004 339, C-001 353, C-005W 344); l'ellisse di C-EST ne lascia passare 89 e 29 solo perché è quasi sempre spenta. **Nessuna candidata lo ripara:** limite da dichiarare («la garanzia vale per un soggetto per ombra»).
- **Uscita a velocità tripla (n = 187).** Entro la porta: C-004 0,72, C-001 0,82, C-005W 0,89, C-EST 0,33. Chi resta fuori porta lascia un avviso permanente: sicuro, ma falso.
- **Ostacolo che si muove col soggetto.** Con le maschere ricalcolate a ogni ciclo tutto regge (strato 1 al 100 %; C-004 0,74 e C-001 0,93 a 5 s). Con le maschere **congelate all'ingresso** (come in `cono2.py`): R90 su celle viste libere in 96 passaggi su 96, soggetto fuori dal cuneo congelato in 91 su 100, copertura a 5 s 0,02–0,04. Riga da aggiungere: «maschere e cuneo si ricalcolano a ogni ciclo».

### 3.2 Base: copertura e area

| | C-004 | C-001 | C-005W |
|---|---|---|---|
| Minimo sul percorso fino a 3 s (T / D / L) | 0,934 / 0,898 / 0,937 | 0,983 / 0,962 / 0,972 | 0,996 / 0,986 / 0,997 |
| Minimo sul percorso a 5 s | 0,73 (T, n = 41) / 0,74 / 0,80 | 0,98 / 0,87 / 0,88 | 0,95 / 0,90 / 0,95 |
| Area di R90 sull'ombra a 1 e 2 s, T | 0,16 e 0,35 | 0,21 e 0,58 | 0,56 e 1,00 |
| idem, D (demo) | 0,60 e 0,81 | 0,71 e 0,97 | 0,99 e 1,00 |
| idem, L | 0,08 e 0,27 | 0,11 e 0,47 | 0,33 e 0,97 |
| Miscela «giurato» a 2 / 3 s (T) | 0,884 / 0,809 | 0,925 / 0,887 | 0,990 / 0,984 |
| Costo per ciclo e traccia, in C: media / massimo | 36–47 µs / 0,5 ms | 87–96 µs / 1,2 ms | 3–7 µs / 0,1 ms |

- Il «90 %» di C-004 e C-001 vale **sul percorso**; con il 20 % di svolte e uscite lontane vale 0,81–0,89 a 3 s.
- C-001 copre al 98–100 % dove dichiara 90: è larga 1,2–1,7 volte C-004 senza guadagno sul percorso.
- C-005W da 2 s è tutta l'ombra: tarata, e non informativa.

### 3.3 Taratura sotto spostamento della distribuzione

Tabella tarata su chi prosegue a 1,3 m/s: sul suo dominio copre 0,964 / 0,948 / 0,904 a 0,5 / 1 / 2 s. Su chi cammina a 0,8 m/s con 20 % di soste e 12 % di ritorni il «90 %» vale **0,874 a 2 s, 0,429 a 3 s, 0,005 a 5 s** (chi sosta: 0,71 / 0,24 / 0,006; `ris/a14_shift_T.txt`). La tabella del comportamento peggiore tiene 1,00 con area 1,00, ma cede fuori dalle velocità di taratura (0,14 a 3 m/s). C-004 (0,99 / 0,94 / 0,91) e C-001 (≥ 0,99) non dipendono dalla miscela.

### 3.4 Sensore

- **Corpo largo 0,45 m senza C6** (si misura il centro della parte visibile). Velocità d'ingresso stimata / vera: mediana 0,79–0,81, decimo percentile 0,50. «Prosegue» a 1 s: C-004 **0,67 (T), 0,65 (D)**; C-001 0,85 e 0,93. Con C6: 0,99 e 1,00. **C6 è un presupposto di C-004.**
- **Ombra stimata −20 cm** (T, con la riga del §2): C-004 «prosegue» a 2 / 3 s 0,93 / 0,74 con `-fixentry` e 0,77 / 0,53 con `-fixentry2`; C-001 0,98 / 0,94. Il raggiungibile con fascia 0,20 m manca in 99 passaggi su 584; lo strato 1 (0,40 m) in 0. **Non risolto:** il mio simulatore segna «libere» le celle dove il corpo tagliato è ancora visibile, e lì i membri di C-004 muoiono; sul vero quelle celle sono «occupato osservato». Lo decide una prova con il corpo esteso nella griglia. A −30 cm (D), fermo appena dentro il bordo: C-004 0,67–0,70 (n = 33), C-001 0,88–1,00. A +20 cm: le tre ≥ 0,97.
- **8 cicli mancati dopo la riemersione**, con cella vista vuota: su 1945 cicli il soggetto visibile sta in una R90 nell'1–2 %; lo strato 1 lo contiene nel 49–53 %. Per mezzo secondo lo schermo disegna la regione nell'ombra mentre la persona è fuori. Nessuna candidata lo ripara: tutte ritagliano sul «libero».

### 3.5 La continuità che inganna

- **Regione piccola, soggetto altrove** (R90 ≤ 25 % dell'ombra e vero a più di 0,5 m): C-004 sul lato lontano nel 10,7 % dei cicli (130 passaggi su 400, T), verso il sensore nel 20,4 % (57 su 200); C-001 in sosta lunga (62 passaggi su 100); C-005W 0,0–1,9 %.
- **Regione su spazio visto vuoto:** 0 cicli oltre la fascia, per costruzione, per tutte; dentro la fascia la toccano nel 92–100 % dei cicli. Il **punto** a velocità costante di C-005 sta su celle libere oltre la fascia nel 5–30 % dei cicli; il fantasma di C-004 nello 0,5–2,9 %.
- **Sicurezza:** nessuna candidata scrive «osservato» o «libero», né tocca lo strato 1. Le rotture trovate stanno nel nucleo (§2; estraneo) e in S2. Con rilevamento 0,7 le coperture non cambiano (≥ 0,93): il danno è quello del §2.

### 3.6 S2, compensazione della latenza (K-210; `ris/a17_s2.txt`, 400 passaggi per riga)

- Moto regolare a 1,2 m/s: errore mediano 0,186 m senza compensazione, **0,030 m** con.
- Tre cicli dopo una sosta improvvisa: 0,040 m senza, **0,178 m** con (0,271 a 1,8 m/s); sorpasso mediano 0,22 m.
- Ingresso nell'ombra: il segno pieno compensato cade **dentro l'ombra** in 393 passaggi su 400 senza C6; con C6 in 31 (1,2 m/s) e 188 (1,8 m/s).
- **Riga riscritta:** «il segno pieno resta sulla misura, con l'età; la posizione compensata è un segno tratteggiato "ora", mai disegnato su celle d'ombra».

### 3.7 Contraddizioni decise dai conti

| K | Esito |
|---|---|
| K-201 | C-EST non emette una regione a ogni ciclo (§1) |
| K-202 | In D, su «prosegue», R90 supera **metà** del cuneo prima della ricomparsa in 0,91 (C-004), 0,95 (C-001), 0,99 (C-005W) dei passaggi: «metà» spegne tutto anche qui. L'80 %: 0,37 / 0,51 / 0,95 |
| K-203 | Il fantasma di C-004 non è peggiore di «fermo» fino a 3 s sul percorso (torna a 3 s: 0,51–0,64 contro 0,79–2,05 m); a 5 s in D perde (1,01 contro 0,70 m). Alla ricomparsa di chi torna salta di 1,35–2,83 m |
| K-205, K-207 | Sì: C-004 tiene ≥ 0,898 con area 0,6–0,85 volte C-001; la tabella tarata in D e T tiene ≥ 0,93 in L fino a 3 s |
| K-206 | No (§1) |
| K-208 | Nessuna tiene il «50» fra 0,40 e 0,60: C-004 0,93 / 0,88 / 0,68 / 0,54 a 0,5 / 1 / 2 / 3 s; C-001 0,88 / 0,91 / 0,78 / 0,66. Un solo livello, detto «almeno» |
| K-210 | Il compensato sbaglia di più dopo una sosta (§3.6) |

## 4. Chi è sopravvissuto meglio

**C-004, fronte + scia**, con questi limiti da dichiarare:

1. **Enunciato riscritto.** «Per chi resta sul proprio percorso R90 lo contiene in almeno 0,90 dei casi fino a 3 s; a 5 s 0,73–0,87 per chi cammina piano. Chi svolta o esce dal lato lontano è coperto solo da R100 (R90 lì vale 0,13–0,84 da 2 s).»
2. Vuole **C6**, un'ombra stimata entro circa 10 cm alla profondità del soggetto e maschere ricalcolate a ogni ciclo.
3. Nella demo la regione è il 60 % dell'ombra a 1 s e l'81 % a 2 s: la soglia di «previsto ampio» non può essere «metà». Il punto vale fino a 3 s.
4. R100 è lo strato 1 (cuneo + 0,40 m), mai il raggiungibile.

Per la regola della scadenza: C-004 è più stretta di C-005W di oltre un terzo in T e L a ogni τ, e in D fino a 1 s (0,60 contro 0,99); in D da 2 s no (0,81 contro 1,00). C-005W inoltre chiede passaggi di taratura con soste e ritorni e la verità dietro il pannello: sull'hardware vuol dire l'occlusione virtuale (C-019). C-004 chiede solo camminate dritte.

| Componente | Fascia | Ore (stima, non verificata) |
|---|---|---|
| Riga di B5 riscritta (§2) | **indispensabile nelle 14 ore** | 0,5 |
| «Perso» → «previsto ampio»; R100 = strato 1; maschere a ogni ciclo | **14 ore** | 1 |
| C-004 con C6 (nel mio C: 45 righe più la libreria) | **14 ore**; con 3 persone solo dopo le tre righe sopra | 3–5 |
| Ripiego se C-004 non entra: disco da tabella fino a 1 s (`tab_D.txt`, `tab_T.txt`: 0,24 m a 0,5 s), poi «ampio» | **14 ore**, in alternativa | 1 |
| S2 riscritta; un solo livello «almeno 90 % sul percorso» | **4 ore di raffinamento** | 1 |
| C-001; S3 e S4 di C-EST; ventaglio; due soggetti per ombra | **dopo l'hackathon** | 5–8 l'una |

## 5. Che cosa propongo dopo

1. All'attacco della soluzione: C-004 **con** la riga di B5 riscritta, corpo largo nella griglia, ombra a −20 cm e rilevamento 0,7 **insieme** (qui uno alla volta); due soggetti che si incrociano e C-002, non eseguiti.
2. Sull'hardware, per primi: la distanza dell'ultima misura dal bordo dell'ombra (decide il §2) e i cicli mancati alla riemersione (§3.4). **Non verificato** finché non c'è la camera.

**Rifare:** `cd f8-continuita/12-torneo; sh rifai.sh` (ogni lancio con `timeout 120`, semi fissati); `timeout 120 python3 s2.py > ris/a17_s2.txt`. Letture: `python3 riassunto.py ris/base_T.txt [c90|c50|area]`, `corto.py`, `estrai.py`. Previsioni ed esiti: `PREVISIONI.md`.
