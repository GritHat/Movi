# Modifiche al nucleo per la continuità visiva — `sciame-scene-dinamiche`, f8, fase f3

Lavoro dalle 16:39 alle 16:52 del 14 novembre 2026 (`date -Is`); lunghezza al limite delle cinque pagine. **Tutto è simulazione su CPU, a sensore fermo, con soggetto puntiforme: niente è provato sull'hardware.** Sigle dei file, tutti sotto `f8-continuita/`: **B** = `11-misure/BANCO_DI_PROVA.md`; **To** = `12-torneo/TORNEO.md`; **Tr** = `10-triage/TRIAGE.md`; **L** = `13-soluzione/ris/LETTURA.txt` (prova mia); **V2** = `f4/H-012/05-correzioni/SOLUZIONE_V2.md`; **Ve** = `f4/H-012/09-arbitro/VERDETTO.md`. Tre numeri separati da «/» sono le geometrie D (demo: pannello 1 m a 1,9 m, soggetto a 2,3 m) / T (soggetto a 4 m) / L (pannello 2 m). «Sul percorso» = prosegue, rallenta, sosta, torna, sosta lunga.

## 0. In testa

**Cambi di stato.** (1) «La regola del "previsto" del nucleo rispetta l'imperativo»: **smentita** (B §3, quinto codice). (2) **C-EST com'è scritta: smentita** fuori dalla demo (B §4, To §1); restano le regole di disegno S5 e gli attacchi. (3) «C-004 tiene 0,90 sul percorso fino a 3 s»: **regge in T e L, non in D** sui miei semi (0,849: L); enunciato riscritto (§2.1). (4) Regola d'ingresso di B5: **smentita** (To §2), riscritta. (5) Mie previsioni: 6 reggono, 3 smentite (P-sd-2 in D, P-sd-3, P-sd-9 come scritta), 1 mista (`PREVISIONI.md`).

**Scostamenti.** La prova mia (`comp.c`) è il codice del banco copiato, più due regole: condivide generatore, filtro, C-004, taratura, valutatore e modello linguistico; non è cieca (avevo letto B e To); usa semi mai toccati (12000–12399). Una prova di fumo su 60 semi di sviluppo è stata vista prima; nessun parametro ritoccato dopo. La mediana d'insieme di P-sd-6 non l'ho calcolata. Lette solo dal triage le consegne di tracciamento, inferenza, ricercatore e rovesciatore; per titoli `AUDIT.md` e `ATTACCO_SPECIALIZZAZIONE.md`; con ricerca testuale `SPECIALIZZAZIONE.md` e `proposta_sciame.tex`. Il settimo addendum (nel file degli addendum) dice «siamo in 5» e «niente sensori per 5–6 ore»: ragiono per 3, 4 e 5, come chiede la consegna. **Le ore sono stime mie, non verificate.**

## 1. Q3 — l'imperativo è rispettato? Parte per parte

| Parte | Esito | Numero e file |
|---|---|---|
| B1 sensore | in parte | rumore «da misurare» (V2): con 4/9/16 cm e taratura ferma a 5 cm la copertura sul percorso scende a 0,30–0,75 (B §2) |
| B2 griglia (B6 etichetta: non toccata) | rispettato, con una condizione | dà gli stati che limitano la regione; le maschere vanno ricalcolate a ogni ciclo (congelate: regione su celle viste libere in 96 passaggi su 96, To §3.1) |
| B3, regola C6 | in parte | allunga il buio a 1,07–1,27 s (V2 §1), ma è un presupposto: senza, «prosegue» a 1 s 0,65–0,67 (To §3.4) |
| B4 filtro | centro in parte; precisione no | chi torna coperto 0,29–0,77 a 2 s; il «50 %» contiene 0,63–0,85 (Tr §1, F-202) |
| B5, strato 2 e «perso» | **no** | una regione nel 19 / 38 / 33 % dei cicli senza osservazione; passaggi con un vuoto 1958 / 1991 / 1999 su circa 2000; in demo «previsto» 0,67 s e «metà» scatta prima della ricomparsa in 332 transiti su 355 (B §2–3) |
| B5, ingresso nell'ombra | **no** (sicurezza) | 87 passaggi su 2800 con il soggetto nascosto senza traccia pendente; 499 su 600 con l'ombra stimata a −20 cm (To §2) |
| B5, strato 1 | rispettato | contiene il nascosto nel 100 % (B §2; L: 10 883, 11 772 e 13 236 campioni su altrettanti) |
| B7, B8 | in parte | tre colori, nessun livello a schermo; «previsto» sopra «perso» in graduatoria (Tr §1) |
| Invarianti | 1–5 e 7 sì; 6, 8, 9 da riscrivere; manca il decimo | `01-requisiti/CONSEGNA.md` §3 |
| Accettazione (R3, H9) | **no** | misura l'identità; H9 «regge» con probabilità 1,000 anche se chi torna non è mai coperto (`04-statistico`, critica 4) |
| Profili d'uso | **no** | «la durata del previsto… si riduce a un istante» (`SPECIALIZZAZIONE.md`, riga 83) |
| Sensore in moto | in parte, niente provato | con la covarianza di posa 0,88–0,91, senza 0,76–0,82 (`03-kalman/risultati_moto.txt`) |
| Demo (B9) | **no** | atto 4 «per un attimo»; il buio di 1,1 s non mostra 2–5 s (Tr §1) |
| Documenti all'utente | in parte | `proposta_sciame.tex`: la riga 94 lo dichiara; la riga 112 dà ancora «circa mezzo secondo» come confermato; nessuna cifra di precisione |

## 2. Le modifiche (Q4): prima → dopo

### 2.1 Predittore durante l'occlusione — M3 e M4

**Prima:** cerchio del filtro al 95 % ritagliato, spento a metà dell'ombra. **Dopo:** la traccia entrata in un'ombra alimenta un predittore che emette **a ogni ciclo un insieme di celle** (una sola interfaccia, due realizzazioni).

- **`sd-1`, principale: C-004 «fronte + scia» con pavimento.** All'ingresso nascono 400 percorsi residui registrati da camminate dritte, trapiantati su punto e velocità d'ingresso: 200 proseguono (fronte), 200 si congelano a un istante uniforme fra l'ingresso e la propria uscita (scia: chi rallenta, si ferma, torna). Un membro su una cella vista libera oltre la fascia di 0,20 m pesa un decimo a ogni ciclo. Regione = unione delle celle più dense al 90 % dei due scenari, dopo tre passate di lisciatura. **Pavimento:** se non esce nessuna cella, la regione è tutto il «non visto libero» dell'ombra, con il segno «ampio».
- **`sd-0`, ripiego, da costruire per primo:** disco a velocità costante con il raggio da tabella (massimo sui comportamenti sul percorso), ritagliato, con lo stesso pavimento.

| Misura | Nucleo (B) | `sd-0` (L) | **`sd-1` (L)** |
|---|---|---|---|
| Passaggi con un ciclo senza regione | 1958 / 1991 / 1999 | 0 / 0 / 0 | **0 / 0 / 0** su 2716 / 2800 / 2798 |
| R90, minimo sul percorso fino a 3 s | 0,00 | 0,866 / 0,911 / 0,953 | **0,849 / 0,962 / 0,920** |
| idem a 5 s | — | 0,737 / 0,911 / 0,898 | 0,737 / 0,927 / 0,858 |
| Area di R90 / ombra, sul percorso, a 1, 2, 3 s | — | D 1,22 1,54 1,57; T 0,18 1,06 1,23 | **D 0,65 0,89 0,98; T 0,13 0,27 0,35; L 0,07 0,18 0,30** |
| Chi svolta o esce lontano, a 2 s | 0,03 (B) | 0,39–0,98 | 0,31–0,76: lì vale solo R100 |

Stato: **sostenuto dai dati in simulazione**, con tre conti che non coincidono (§2.12, O1–O2). **Enunciato che ne segue:** «per chi resta sul proprio percorso la regione lo contiene in almeno 9 casi su 10 fino a 2 s con ombre larghe (T, L: ≥ 0,96) e fino a 1 s in demo (D: ≥ 0,955); a 3 s fra 0,85 e 0,96 (in D 101 su 119, cioè 0,849, Wilson 0,77–0,90); oltre 3 s il sistema passa ad "ampio"». C-EST (S3, S4) non entra: a 3 s su «sosta» 0,72 e 0,53 in T, 0,14 e 0,00 in L; cicli «perso» in 374–1312 passaggi su 2000 in T; ellisse al 95 % dell'attacco 5: 0,28 / 0,30 / 0,00 (B §4). C-001 (particelle) copre di più con area 1,3–2,8 volte maggiore e cade oltre 10 s di sosta (0,045 a 30 s, To §3.1): dopo l'hackathon.

### 2.2 Posizione mostrata e regione al livello dichiarato

**Regione:** un solo livello, detto «almeno 9 su 10, sul percorso» (nessuna candidata tiene il 50 %: 0,94 → 0,46, B §3; K-208). **Punto, prima:** la media del filtro, su suolo visto libero nel 22 % dei cicli (B §2). **Dopo, ibrido con attesa** (mio, senza particelle): il punto del filtro finché sta su celle non viste libere; quando cadrebbe su una cella vista libera resta fermo 8 cicli (0,53 s), poi va verso il baricentro dei membri non visti liberi, al più 0,167 m per ciclo, senza mai entrare in una cella vista libera.

| Punto (L; T salvo dove detto) | Errore mediano «squadra» a 1 / 2 / 3 / 5 s, m | «Prosegue» con un passo indietro, D / T / L | Cicli su celle viste libere | Salto mediano alla ricomparsa, «prosegue» |
|---|---|---|---|---|
| filtro (nucleo) | 0,18 0,41 0,72 1,50 | 0 % | 38 367 | 0,37 m |
| fantasma di C-004 | 0,19 0,50 0,72 1,02 | 54 / 68 / 60 % | 71 | 1,35 m |
| **ibrido con attesa** | **0,18 0,39 0,60 0,92** | **18,2 / 4,0 / 3,5 %** | **397** (0 dopo il quinto ciclo; D 13, L 23) | **0,37 m** |

Peggior rapporto con la migliore fra «fermo» e «velocità costante»: 1,22 / 1,00 / 1,01; 0 passi oltre 0,167 m. **Cede:** su chi sosta o torna il salto alla ricomparsa è 1,3–1,4 m in T, e 3,5 m in L su chi torna (va mostrato come scarto, §2.7); in D arretra nel 18 % dei «prosegue»; i cicli su «libero» non sono zero (P-sd-3 smentita).

### 2.3 Taratura e verifica della precisione dichiarata — M6, M8

**Prima:** q tarato su 15 ricomparse, un livello, 26 su 30 alla ricomparsa (H9). **Dopo:**
1. **Taratura per installazione**, su dati separati: il rumore misurato del centro di una persona a 2–4 m entra in R (senza: 0,44; rimisurato: 0,87; B §2); 30 camminate dritte in vista danno la libreria dei percorsi (numero **non verificato**: B §6). Il numero di passate di lisciatura (3) è un parametro tarato: con una sola 0,78–0,83 (B §3).
2. **Verifica con l'occlusione virtuale** (C-019): una copia della catena riceve le misure con un cuneo cancellato a programma; la persona resta visibile e fa da verità a ogni ciclo. **Mai eseguita**; non rende il corpo tagliato dal bordo.
3. **Scheda per comportamento e per tempo** (C-020), unità il passaggio, camminatori diversi da quelli della taratura: 4 comportamenti × 30 passaggi, per cella ≥ 28 dentro regge, ≤ 23 smentita, altrimenti altri 30 e ≥ 54 su 60 (`04-statistico` §4; B §6). 30 passaggi non separano 0,90 da 0,80: a schermo si scrive «27 su 30: fra 0,74 e 0,97», mai «tarato».
4. In simulazione: 400 passaggi per cella, taratura (semi 1000–1199) separata dalla prova, una geometria mai tarata.

### 2.4 Incertezza controllata

La regione sta sempre dentro ombra + fascia: 0 cicli su celle viste libere oltre la fascia e 0 fuori da R100 (B §2, L). **Soglia:** il segno diventa **«previsto ampio»** quando l'area supera l'80 % dell'ombra, quando scatta il pavimento, oltre 3 s senza osservazione, o con profondità o posa degradate. Da lì la regione è tutto il «non visto libero» dell'ombra e l'etichetta dice «è ancora dietro, o ha lasciato l'area». Costo misurato della soglia: «ampio» nel 50,4 % dei cicli in D, 0,0 % in T e L (L); «metà» ne darebbe il 79 % in D (B §5, K-202).

### 2.5 Macchina degli stati — M2

**Prima:** osservato → previsto → **perso, assorbente**. **Dopo:** osservato → previsto → previsto ampio; «perso» non è più uno stato. Una traccia in ombra si chiude solo con un motivo dichiarato, elenco chiuso: (1) **riagganciata**: rilevamento dentro la porta, stessa identità; (2) **identità ambigua**: rilevamento fuori porta, o più tracce pendenti nella stessa ombra: nasce una traccia nuova, la vecchia resta «previsto ampio» e l'avviso resta; (3) **ombra vista libera**: tutte le celle del cuneo libere per 3 fotogrammi (regola del nucleo); (4) **affidabilità persa**: la regione si congela come «ampio, non aggiornata»; (5) **fuori dall'area osservata**: i membri sono oltre portata o campo. In campo aperto vale la regola del nucleo (3 fotogrammi). Nessun timer chiude una traccia in ombra.

### 2.6 Ingresso nell'ombra e rapporto con la garanzia — M1, M7

- **M1, riga di B5 riscritta (To §2).** «A ogni ciclo senza misura: se l'ultima misura è a meno di 0,40 m dall'ombra **di un occlusore che non è il gruppo della traccia** (K-018), oppure se il punto previsto sta in tale ombra o entro 0,40 m, la traccia è entrata.» La previsione **accende** l'avviso e non lo toglie mai. Passaggi scoperti: 87 → 9 su 2800; 499 → 16 su 600 a −20 cm. Un vuoto falso di 0,3 s a 0,7 m dall'ombra resta scoperto (136 su 200): limite dichiarato.
- **Lo strato 1 non cambia e non si indebolisce.** R100 è il cuneo più 0,40 m, mai il «raggiungibile» (a 3 m/s manca il soggetto in 138 passaggi su 138, To §3.1). L'evidenza negativa restringe solo R90; il rilascio resta cella per cella. Chi lascia il percorso è coperto solo da R100.
- **M7, porta sul riaggancio (B §6).** La regola geometrica del nucleo resta; in più, un rilevamento a oltre 0,40 m da R90 non riaggancia: «identità ambigua». Sul percorso la prima misura cade entro 0,40 m nel 0,989 / 0,998 / 0,990 dei casi (L); per chi svolta o esce lontano 0,98 / 0,65 / 0,72: lì l'avviso resta acceso a torto, dal lato sicuro.

### 2.7 Visualizzazione e suono — M5

**Prima:** tre colori, area «probabile» per mezzo secondo. **Dopo** (`06-visualizzatore` §3, S5 senza «conf Z%», che non ha definizione):
- un segno di taglia fissa per oggetto: **disco pieno** solo con una misura nel ciclo; **anello vuoto** in «previsto»; **croce** in «previsto ampio». La distinzione è di forma e tratto, non di colore;
- la regione a contorno tratteggiato, tagliata sul bordo dell'ombra; la scia piena dove fu misurata, tratteggiata dove fu prevista;
- **indicatore di precisione:** «PREVISTO · almeno 9 su 10 qui dentro · larga X,X m · non visto da Y,Y s»; in ampio: «PREVISTO AMPIO · dietro l'ostacolo o fuori area · da Y s»;
- alla ricomparsa lo **scarto** fra punto e prima misura resta 0,5 s, in centimetri;
- **tabellone:** nelle 14 ore il contatore «ricomparso dentro la zona: k su n» con l'intervallo; nel raffinamento le righe per comportamento e per tempo, con la larghezza;
- sotto tutto, il cuneo di «possibile presenza» con l'età.

**Suono:** restano i segnali brevi (C11), uno per cambio di stato (previsto, ampio, riagganciato, ambiguo). Il battito continuo (nitido se osservato, soffiato se previsto) è una proposta **non verificata**: dopo l'hackathon. Nessuna persona ha guardato lo schermo o ascoltato un suono.

### 2.8 Misure di accettazione nuove

| Requisito della traccia | Misura | Soglia | Oggi, in simulazione (L) |
|---|---|---|---|
| Gestire le interruzioni | passaggi con un ciclo senza regione prima della ricomparsa o di una chiusura dichiarata | 0 | 0 / 0 / 0 |
| | R90 per comportamento sul percorso e fascia di tempo (≤ 1, 1–2, 2–3 s) | ≥ 0,85 per cella (n ≥ 400); sul sensore la scheda del §2.3 | minimo 0,849 / 0,962 / 0,920: **in D non superata**, per un millesimo |
| | area di R90 / ombra e quota dei cicli «ampio» | riportate sempre | §2.1, §2.4 |
| | errore del punto, «squadra» | ≤ 0,5 m a 1 s, ≤ 1,0 m a 2 s; mai oltre 1,5 volte la migliore base | 0,18–0,22; 0,37–0,41; 1,22 |
| | prima misura entro 0,40 m da R90, sul percorso | ≥ 0,90 | 0,989–0,998 |
| Distinguere osservato e incerto | fotogrammi con il disco pieno senza una misura nel ciclo | 0 | per costruzione; non misurato |
| | cicli di R90 su visto libero oltre la fascia; R90 fuori da R100 | 0; 0 | 0; 0 |
| | punto su celle viste libere dopo il quinto ciclo | 0 | 13 / 0 / 23: **non superata** |
| | R100 contiene il nascosto | 100 % | 100 % |
| Costo | 95º percentile per ciclo, 10 tracce | ≤ 6,7 ms | 0,7–1,4 ms in C (`ris/tempi.txt`) |

R3 (identità) resta, a parte. H9 esce.

### 2.9 Demo riscritta

- **Atto 4, passa dietro il pannello:** l'anello e la regione avanzano lungo il pannello, tagliati dal bordo; alla ricomparsa lo scarto e il contatore.
- **Atto 5, si ferma dietro:** il fronte si estingue (l'uscita è vista libera), la scia resta; a 3 s o all'80 % il segno passa ad «ampio» con l'età; quando torna, riaggancio.
- **Atto 5 bis, pannello virtuale:** un giurato cammina in vista dietro un cuneo cancellato a programma; a schermo la persona vera e il suo anello, e il tabellone si riempie.
- **Da dire alla giuria:** in demo l'ombra è 1,36 m² e la regione ne è il 65 % a 1 s e l'89 % a 2 s (L): da 2 s dice «è ancora dietro», non «dove».

### 2.10 Invarianti riscritti

- **3.** Il disco pieno esce solo con una misura in porta nel ciclo; una previsione non esce mai come osservazione, né compensata per la latenza dentro un'ombra (To §3.6).
- **4.** Regione prevista e «possibile presenza» mai su celle «libero» oltre la fascia; R90 ⊆ R100.
- **6.** L'evidenza negativa restringe solo la regione prevista, dove la profondità è valida; non rilascia mai lo strato 1.
- **8.** Ogni uscita porta il contatore del sensore, l'età dall'ultima osservazione e il livello dichiarato.
- **9.** Posizione e regione previste non sono grandezze osservate: escono solo con il loro stato; massa e accelerazione restano fuori.
- **10 (nuovo).** Per ogni traccia confermata entrata in un'ombra, a ogni ciclo fino a una chiusura dell'elenco del §2.5, il sistema emette un punto, una regione a livello dichiarato e l'età. Oltre soglia cambia segno, non sparisce.

### 2.11 Costo per ciclo e ore di lavoro

**Per ciclo (C, un filo, macchina condivisa; `ris/tempi.txt`):** C-004 0,08–0,15 ms per traccia e 0,6–1,3 ms con dieci (95º percentile); pavimento e punto ne aggiungono 0,005–0,008 e 0,05–0,07. In Python **non verificato** (l'autore di C-004 misurava 0,48 ms per ciclo e 4,3 ms all'ingresso).

| Componente | Ore | Fascia |
|---|---|---|
| M1 riga d'ingresso di B5 | 0,5 | **indispensabile nelle 14 ore** (sicurezza) |
| M2 stati, chiusure motivate, R100 = strato 1, maschere a ogni ciclo | 1 | **14 ore** |
| M3 interfaccia «insieme di celle», `sd-0`, pavimento, punto ibrido | 2 | **14 ore**, per primo |
| M4 C-004 dietro la stessa interfaccia | 3–5 | **14 ore** con 5 persone; con 4 solo se una è libera dall'ora 6; con 3 nel raffinamento, e resta `sd-0` |
| M5 disegno nuovo e contatore | 2–3 | **14 ore** |
| M6 occlusione virtuale, registro per ciclo, scheda | 4–5 | **14 ore**: è la valutazione preliminare |
| M7 porta sul riaggancio | 1 | **14 ore** |
| M8 rumore misurato, libreria da 30 camminate, scheda 4 × 30 | 2 in due (dentro le ore di B9) | **14 ore**, all'arrivo del sensore; il secondo stadio nel raffinamento |
| Tabellone completo; S2 riscritta (segno tratteggiato «ora», mai in ombra: compensare porta l'errore da 0,19 a 0,03 m nel moto regolare, ma da 0,04 a 0,18 m dopo una sosta improvvisa, To §3.6) | 2–3 | **4 ore di raffinamento** |
| C-001, C-002, S3 e S4 di C-EST, ventaglio, battito, due soggetti per ombra, sensore in moto | 5–8 l'uno | **dopo l'hackathon** |

**Bilancio.** Nucleo V2: 54 ore-persona. Tagli: etichetta B6 (−4), «mobile» fine e associazione a più tracce (−4), frasi e graduatoria (−2), strato 2 vecchio (−1), prove H7–H13, pannello da 0,5 m e seconda persona (−6): restano 37. La continuità ne aggiunge 15,5 (con M4), l'integrazione 4: **56,5, o 52,5 con il solo `sd-0`**. In 14 ore: **5 persone** 70 ore-persona, ci sta; **4 persone** 56, ci sta con `sd-0` e M4 al limite; **3 persone** 42, **non ci sta** nemmeno con il solo `sd-0`: mancano circa 10 ore, e che cosa tagliare ancora lo decide l'utente. Predittore, disegno e scheda dipendono solo da «stato della traccia all'ultima misura» e «maschera del non visto libero»: si sviluppano dall'ora 0 su un sensore simulato, in parallelo a sensore, griglia e rilevamento.

### 2.12 Dove due prove tirano in versi opposti (non scelgo)

- **O1. C-004 in demo fino a 3 s:** 0,935 (B: 86 su 92), 0,898 (To), 0,849 (L: 101 su 119). Gli intervalli si toccano fra 0,865 e 0,902. Dichiaro «9 su 10» in demo solo fino a 1 s; decide la scheda sull'installazione.
- **O2. C-004 a 5 s:** ≥ 0,905 (B) contro 0,73–0,80 (To) e 0,74 / 0,93 / 0,86 (L). Per questo l'orizzonte del livello è 3 s.
- **O3. Uscita a velocità tripla dentro la porta:** 5,5 % (B: 11 su 200) contro 72 % (To §3.1, n = 187). La porta vale solo come segnale, sicuro in entrambi i casi.
- **O4. Ombra stimata a −20 cm:** C-004 0,970 con la fascia (B) contro 0,74 a 3 s, e **0,53 insieme alla riga M1** (To §3.4). **Non risolto:** decide una prova con il corpo esteso nella griglia (A-sd-2).
- **O5. C-EST, attacco 1, peso del transito:** lettura A 1 e 0 passaggi su 200 (B) contro 174 su 202 in D (To). Non cambia l'esito: cade su K-201, K-206 e sull'attacco 5.
- **O6. Semplicità contro larghezza:** `sd-0` costa 2 ore ma da 2 s è tutta l'ombra; `sd-1` 3–5 ore in più e resta al 27–35 % in T. Stessa interfaccia, ripiego per primo.

## 3. «A prescindere dal sistema»

- **Identico** su stazione fissa, piattaforma in moto e ausilio indossato: l'interfaccia (dentro: stato della traccia all'ultima misura e maschera del «non visto libero» a ogni ciclo; fuori: celle, punto, età, livello, stato); la macchina degli stati e le chiusure; gli invarianti; le misure del §2.8 (quote e rapporti); la grammatica del disegno; il registro e la scheda.
- **Parametro:** libreria dei percorsi per classe di oggetto, v_max, fascia, cella, numero di membri, passate di lisciatura, soglia e orizzonte di «ampio», attesa del punto, R del sensore.
- **Da riprovare in moto** (niente è provato): maschere e cuneo ricalcolati a ogni ciclo in un riferimento fermo sul mondo (con l'ostacolo in moto e maschere ricalcolate lo strato 1 tiene al 100 %, C-004 0,74 a 5 s: To §3.1); i membri dilatati con l'incertezza dell'**incremento** di posa (r·σ_ψ + σ_t), perché senza quel termine la copertura scende a 0,76–0,82 sotto 1 s (`03-kalman`); scostamento non modellato entro 9 cm a 0,67 s, 15 cm a 1 s, 39 cm a 2 s (`MOTO_PROPRIO.md`, Q5); con la posa persa la regione passa ad «ampio» e non si restringe; la taratura rifatta in moto. Per l'ausilio indossato il canale è il suono: non verificato.

## 4. Condizioni del verdetto toccate

- **§5.5** («la previsione vale circa mezzo secondo») e **R3** («area prevista tolta dalla promessa», 0,5–1,2 %): riscritte. La regione c'è a ogni ciclo, con il livello dichiarato fino a 1–3 s secondo l'ombra, poi «ampio».
- **Condizione 2, velocità coperta (K-015):** non toccata per il «libero». La previsione è provata fra 0,3 e 1,8 m/s; a 3 m/s C-004 tiene 0,95–0,97 e la tabella 0,14 (To §3.1), in una sola prova.
- **Condizione 5 (C6, K-017):** C6 diventa presupposto anche della previsione. Il suo costo su chi torna (cerchio: 47–50 %) non si ritrova nella regione nuova: «torna» 0,95–1,00 fino a 3 s (L), con C6 emulata sul bordo vero.
- **Condizione 6:** vale anche per la previsione: tracce con almeno 4 misure, un soggetto per ombra, occlusore fermo.
- **Condizione 7 (K-016, secondo soggetto):** **non riparata**. Il nucleo dà allo sconosciuto l'identità del primo in 193 casi su 193 (B) e 347 su 357 (To); nessuna porta lo evita (158 su 193). Le celle restano «in ombra», cade l'avviso. Va scritto: «la garanzia vale per un soggetto per ombra».
- **Condizione 8 (K-018):** la riga M1 nomina l'occlusore «diverso dal gruppo della traccia».
- **K-014:** M1 la riduce in simulazione (499 → 16 su 600); sul sensore resta aperta.

## 5. Senza prova, cedimenti, previsioni

**Affermato senza prova.**
1. M1 insieme a `sd-1`: mai eseguiti insieme; a −20 cm tirano in versi opposti (O4).
2. Corpo esteso, occlusione parziale, falsi rilevamenti, buchi di profondità: mai simulati.
3. L'occlusione virtuale come misura: mai eseguita.
4. Il disegno e i segnali: nessuna persona li ha provati.
5. Le ore, e il costo in Python.
6. Due tracce nella stessa ombra; ostacolo in moto; sensore in moto.
7. L'orizzonte di 3 s e la soglia dell'80 %: scelti da me sui numeri del §2, non tarati.
8. Che C6 lavori sulla maschera stimata come sul bordo vero.

**Dove la previsione cede (da dichiarare).**
1. Chi svolta o esce dal lato lontano: R90 0,31–0,76 a 2 s; vale R100.
2. In demo da 2 s la regione è quasi tutta l'ombra.
3. A 5 s: 0,74–0,93.
4. Un rumore diverso da quello tarato: 0,44.
5. Rilevamenti mancati per mezzo secondo dopo la riemersione: la regione resta in ombra con la persona fuori (To §3.4).
6. Il secondo soggetto.
7. Il vuoto falso prima dell'ombra.
8. Il punto arretra nel 18 % dei «prosegue» in demo e salta di 1,0–3,5 m su chi torna.

**Previsioni per l'attacco** (scritte alle 16:48:57, `PREVISIONI.md`, seconda serie).
- A-sd-1: M1 con `sd-1` in T, sul percorso ≥ 0,90 fino a 3 s; smentita sotto 0,85.
- A-sd-2: corpo di 0,45 m nella griglia, −20 cm e rilevamento 0,7 insieme: ≥ 0,85 a 1 e 2 s; smentita sotto 0,80 a 2 s o con un passaggio fuori da R100.
- A-sd-3: nessun vuoto in nessun braccio.
- A-sd-4: con 5 cicli concessi, 0 cicli del punto su «libero» dopo il quinto.
- A-sd-5: in demo, semi nuovi, «prosegue» ≥ 0,93 a 1 s e 0,80–0,93 a 3 s.
- A-sd-6: due tracce pendenti: nessuna identità al ritorno.
- A-sd-7: Python, ≤ 6,7 ms con 3 tracce; smentita oltre 20 ms.
- A-sd-8: sosta di 30 s: in «ampio» il nascosto è dentro nel 100 % dei cicli.

**Rifare** (in `13-soluzione`, ogni lancio ≤ 60 s): `sh rifai.sh`. Impronta del codice: `CONGELATO.txt`.
