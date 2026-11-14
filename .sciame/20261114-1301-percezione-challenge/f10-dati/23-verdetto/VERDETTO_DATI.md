# Verdetto dell'estensione f10 — dati pubblici e hardware simulato (`sciame-arbitro`)

**In testa.** Lavoro dalle 2026-11-14T17:43:35+01:00 (`date -Is`). Percorsi relativi a `f10-dati/`. **Verdetto: nessuna delle sei ipotesi è validata sul sensore della squadra, che non esiste ancora; due cifre del nucleo cadono, una si corregge, due reggono in un dominio più stretto.** **Cambi di stato:** (1) identità al ritorno «100 %, almeno 99,25 %»: **smentita** su profondità realistica (0 passaggi su 90); (2) muro «mobile» 0,0–0,2 %: **smentita** (79 su 90); (3) q = 0,2: **corretto** verso 0,05–0,1 su pedoni veri; (4) K-014: da «non decidibile senza hardware» a **sostenuta in simulazione a posa esatta**, con quattro controesempi fuori da quel dominio; (5) nascono K-401…K-407. **Identificativi:** serie 4xx (0xx–3xx già usate nei file che posso leggere). **Scostamenti:** di `01`, `02`, `03` e del nucleo ho letto le parti citate; le `PREVISIONI.md` degli altri ruoli non le ho rilette; tre ispezioni con il Python di sistema, su uscite dei ruoli e non su dati scaricati. `04-lidar/` è vuota. Lunghezza al limite delle quattro pagine (circa 3300 parole, in gran parte tabelle). **Regole violate:** nessuna che io sappia (niente git, rete, sudo, GPU). Previsioni A1–A6 scritte alle 17:43:49, prima di aprire i contributi (`23-verdetto/PREVISIONI.md`): 5 reggono, 1 non risolta (A4), nessuna smentita.

**Cifre ricontate sui file** (`23-verdetto/riconta_arbitro.py`, solo json, csv e numpy, nessun codice altrui; uscita in `riconteggio.txt`). Tornano tutte: 162 sequenze simulate e 9152 fotogrammi (indice e file); 8 sequenze vere e 3510 fotogrammi; K-014: 0 su 2 907 032 celle·fotogramma dai record, e **0 su 3 149 352 con una definizione mia** (centro della cella nell'ombra vera, dalle griglie e dalla verità); con soglia 40: 2 più 45 al bordo; bordo d'ombra +2,0 / +6,2 / +14,6 cm, 115 sequenze su 115 e 3742 fotogrammi, al limite 0 su 8; continuità 0 su 90, 41 su 45, 28 / 24 / 28 su 30; pannello «si muove» 79 e 5 su 90; centro nascosto 2939 su 3038, 99 senza avviso, 0 «libero»; regione 83 su 90; THÖR 0,977 / 1,000 / 1,000 su 219 tratti e 9 persone (riletta dal riassunto, non ricalcolata dalle tracce: lo ha fatto lo statistico con un filtro suo, 0,982 / 0,995 / 1,000); costo 6,35 / 18,6 / 105 ms su 9152 cicli; pavimento vuoto 28 / 26 / 0 / 43 tracce; TUM, mediana 58 celle libere su 120 fotogrammi. **Due etichette non tornano, i conteggi sì:** «135 sequenze, filtri spenti» sono 131 più 4 con i filtri (lo dice anche lo statistico); i «45 al bordo in 1 sequenza» stanno in 2 (36 in `scatola15_2p0m`, 9 in `azzeramento_progressivo`). **Lette e non ricontate:** le uscite dell'avversario (coincidono con il suo testo), gli 8 semi su 20 dello statistico, vetro, sensore coperto, tabella degli ostacoli, 81 ms di DepthTrack (sta solo nel riepilogo). *Indipendenza:* condivido con tutti il modello linguistico e la specifica; con la validazione le uscite della catena e la verità del simulatore; non il codice di misura.

## 1. Le sei ipotesi: prima e dopo

| H# | Prima (verdetto del nucleo) | Dopo | Numerosità, intervallo, file |
|---|---|---|---|
| **H-401** «Libero» da una profondità | argomento per costruzione; nessuno script lo calcolava; K-014 non decidibile | **Confermata su profondità simulata da scheda** (D435i, D455, Gemini 335; nominale e limite), **solo a posa esatta e con ostacoli che restituiscono profondità**. **Su registrazioni vere: non decidibile** (TUM, Kinect v1 a mano: nessuna verità d'ombra, N = 0). Al bordo del campo vale a meno di una cella (10 cm). Serve: pannello sul suolo segnato, con il sensore della squadra | 0 su 2 907 032 celle·fot., 135 sequenze ma **3 forme d'ombra**; per sequenza 0 su 131 (limite superiore 2,9 %). `20-validazione/uscite/sim/misura_libero.json`; `21-statistica/tabelle/sim_sim.txt` |
| **H-402** Errore del bordo d'ombra | ±20 cm assunti, mai misurati; peggio a −20 | **Confermata su simulata, al nominale**: da +2,0 a +14,6 cm, mediana +6,2. «Sempre verso il largo» va riformulato (K-404). **Al limite: smentita** per la soglia scritta. **Sul vero: non decidibile** | 115 sequenze su 115 (D435i 103 su 103, 96,4–100 %), un solo pannello e un solo spigolo, passo 4,2 cm; limite 0 su 8, da −65 a +73 cm. `…/sim/misura_ombra.json`; `22-avversario/uscite/a6*.txt` |
| **H-403** Rumore del centro con la distanza | curva nominale 1,5 / 3,4 / 6,0 cm; K-007 aperta | **Non decidibile.** Simulato (capsula rigida: limite inferiore): mediana 0,3 / 0,8 / 1,2 cm, ma a 2 m 8 semi su 20 stanno a 3,7–4,4 cm. Vero: una sequenza (D415), 5,8–6,8 cm, senza verità e scelta fra tre varianti. Serve una posizione vera indipendente (metro a terra) | 20 semi per distanza (22–61 % sopra la nominale a 2 m); 288 fotogrammi di una sequenza. `21-statistica/tabelle/controlli_brevi.txt` |
| **H-404** Previsione durante l'occlusione | identità 100 %; q = 0,2; «previsto» circa 0,5 s; cerchio 0,89–0,93 | **(a) Identità, simulata: smentita com'è** (0 su 90). **Corretta** con una soglia di punti più alta: 41 su 45, valore scelto dopo i dati e legato alla risoluzione (K-403). **(b) Moto di pedoni veri (THÖR, cattura del moto, non una camera): q corretto**, 0,2 copre troppo, il valore calibrato sta fra 0,05 e 0,1. **(c) Su profondità vera: non decidibile** (2 tratti di al più 0,10 s) | (a) 0–4,1 %; 79,3–96,5 %; al limite 0 su 6 (0 su 7 con la persona scura). (b) 219 tratti, 9 persone: copertura 0,977 / 1,000 / 1,000 con 0,2; errore mediano 0,21 / 0,49 / 0,81 m a 1 / 2 / 3 s. `…/sim*/misura_passaggi.json`, `…/banco_thor.json` |
| **H-405** Mobili e ostacoli | «mobile» 100 % a 2 m; muro mobile 0,0–0,2 % | **Ostacoli fermi: confermata su simulata** (cassa 84 su 84; scatola di 15 cm a 2 m 10 su 10). **Falsi «in movimento»: smentita** (pannello 79 su 90; 28 tracce fantasma in 2 s sul pavimento vuoto). **Sul vero: non decidibile** | 79,4–93,0 %; con soglia 40: 5 su 90 (2,4–12,4 %), ma la scatola scende a 3 su 10. `…/sim/misura_ostacoli.txt` |
| **H-406** Costo per ciclo | questione aperta | **Confermata su simulata** (424×240): 6,35 ms di media, 4 cicli su 9152 oltre 66 ms. **Smentita su una registrazione vera affollata** (D415): 81 ms di media con 254 tracce. Un filo di un portatile, **non la scheda di bordo** | `…/sim/*/fotogrammi.jsonl`; `…/vere/RIEPILOGO.txt` |

## 2. Contraddizioni e condizioni del nucleo

| K# | Dopo f10 |
|---|---|
| **K-014** | **In simulazione il «libero» falso con dati validi non compare**, e il verso stretto (−20 cm) nemmeno: 0 fotogrammi sotto −10 cm al nominale. **Controesempi nuovi**: posa sbagliata di 1° (F-404), ostacolo senza ritorno (F-405), filtri accesi (F-406), soglia alta (2 celle·fot.). **Sul sensore vero: aperta.** |
| **K-015** | **Non toccata**: il simulatore ha tempi regolari e nessuna latenza. Dato nuovo: il ciclo passa da 6 a 81 ms quando le tracce sono centinaia. |
| **K-016** | **Controesempio rieseguito sulla catena di riferimento** (scena a mano, senza rumore): l'identità di A passa a B, A è «osservato» per 22 fotogrammi mentre è nascosta e sta fuori dall'avviso per 25. |
| **K-017** | **Aperta e aggravata**: C6 non basta (pannello «si muove» in 79 passaggi su 90) e dopo un riaggancio con misura tagliata il filtro resta fermo, fino a 5,00 m dalla verità. Su chi torna indietro la continuità è 0 su 4 con i parametri del nucleo e 2 su 4 con soglia 40 (`pannello_c`: nei file, non nel rapporto; ricontato; N = 4 non decide). |
| **K-018** | **Risolta come lettura** nella catena (L6: l'ombra non è quella di un gruppo che contiene la misura), verificata su 25 prove sintetiche; non sul vero. |
| **K-003** | **Corretta sul moto vero**: q = 0,2 è prudente; 0,1 dà 0,92–0,95 (visto dopo: da provare su `exp2`). Aperta con la catena su profondità. |
| **K-007** | **Non risolta.** In simulazione lo spostamento regge fino a 3,5 m e cade in avvicinamento da 4,3 m (0 su 20 con i parametri del nucleo, 4 su 20 con soglia 40). La χ² non è stata provata. |

**Contraddizioni fra i contributi (nuove).** **K-401** «la regione copre il 100 %» (mediana) contro 7 passaggi su 90 in cui la verità esce: decide il file, **83 su 90**; si riporta per passaggio. **K-402** K-014 «sostenuta» contro «solo a posa esatta»: compatibili, vale il dominio stretto. **K-403** «soglia 40: 41 su 45» contro «a 848×480: 0 su 10; a 2,1 m: 4 su 10»: la soglia è un rapporto con i pixel, non un numero; la versione proporzionale **non è mai stata eseguita**. **K-404** «errore sempre largo» contro −0,2 cm con un altro spigolo, e «non decidibile» al limite contro la soglia scritta: vale **smentita al limite**, misura contestata dal suo autore (le celle d'ombra vera restano comunque «in ombra» od «occupato»). **K-405** rumore del centro, mediana 0,36 cm contro distribuzione a due gruppi: vale la seconda. **K-406** «28 tracce fantasma» come difetto del sensore contro 3 a +0,5° e 81 a −0,5°: la cifra misura il margine fra tolleranza del suolo (5 cm) e soglia d'ostacolo (7 cm). **K-407** simulatore contro registrazioni: nei buchi il vero sta 3–4 volte oltre il livello «limite» (24–34 % contro 7,8 %): **le cifre al nominale sono ottimistiche**.

**Le nove condizioni.** 1 (filtri spenti, autoverifica): **confermata necessaria** (sensore coperto con i filtri: 989–995 celle «libero» per altri 3 fotogrammi); sulla Gemini l'elaborazione è accesa di norma. 2 (fascia a formula): non toccata. 3 (pannello): **corretta**: 1,5 m non nasconde una persona di 1,7 m, ne servono 1,61, e con 1,6 la testa spunta in 10 passaggi su 90; proposta 1,8 m; «una sola persona» confermata. 4 (sensore fermo): **stretta**: serve la posa nota entro meno di 1°. 5 (C6): non basta. 6 (una traccia pendente, occlusore fermo): la prima è **falsa su profondità realistica** (7–66 tracce fantasma per passaggio); la seconda confermata (21 fotogrammi fuori dall'avviso se il pannello si muove). 7 (limiti): si aggiungono F-404, F-405, F-410. 8 (ombra propria): scritta, è L6. 9 (dicitura): diventa «provato su profondità simulata dalle schede tecniche e su tracce pubbliche di persone; mai su un sensore della squadra».

## 3. Difetti trovati: ingressi obbligati per la soluzione integrata

Le correzioni sono dei ruoli; **«non provata» vuol dire che nessuno l'ha eseguita**.

| F# | Difetto | Caso minimo | Correzione proposta |
|---|---|---|---|
| **F-401** | La persona si fonde col pannello quando le sagome si toccano (pixel misti ai bordi) | 90 passaggi su 90; `python diagnosi.py sim d455_nom__pannello_a12__s00 8 16`, k = 11. Con i bordi spenti la fusione scende a 1 su 10 ma la continuità resta 0 su 10 | soglia di punti proporzionale ai pixel attesi per cella (validazione-6, avversario-2): **non provata** |
| **F-402** | Il riaggancio accetta gruppi tagliati e lo stesso occlusore | stesso caso, k = 23 | rifiutare i tagliati e il gruppo dell'occlusore (validazione-7): non provata |
| **F-403** | Fantasmi del pavimento: «una sola traccia pendente» non è mai vera | `d435i_nom__pavimento_vuoto`: 28 tracce in 2 s (D455: 0) | F-401 più la prova d'ingresso (validazione-9) |
| **F-404** | Con la posa sbagliata un ostacolo basso è «libero» | scena a mano: 10 cm a 2,55 m, +1°: 7 celle su 7; simulato: scatola di 15 cm a 2 m, +2,5°: 9 fotogrammi su 10 | prova d'ingresso della posa (avversario-1): un oggetto di 10 cm a 2,5 m deve uscire «occupato». La stima dai primi 5 fotogrammi sbaglia di 5° su TUM |
| **F-405** | Un ostacolo che non restituisce profondità è «libero» | palo di 3 cm a 2,05 m con i pixel a 0: piede «libero» 6 fotogrammi su 6 | nessuna proposta: limite da dichiarare, come il vetro (420 celle·fot. su 420) |
| **F-406** | I filtri del costruttore tengono vivo il «libero» | sensore coperto, variante `__filtri` | condizione 1 |
| **F-407** | «Libero» per memoria su una cella che era occupata | 23 celle·fot. sull'esempio | **corretto** nella catena (L3) |
| **F-408** | Dopo un riaggancio tagliato il filtro non si aggiorna | prova P8 della catena: 5,00 m per 6 fotogrammi | ripartire dalla misura con R gonfiato (sviluppatore-1): non provata |
| **F-409** | Al riaggancio lo strato si spegne anche se nell'ombra resta qualcuno; il riaggancio registra «errore 0,18 m, dentro il 95 %» anche quando l'associazione è sbagliata | scena A3 | lo strato resta finché le celle non sono viste libere (avversario-3): non provata. **q non si tara sulle innovazioni alla ricomparsa** (B4 del nucleo): premierebbe gli scambi |
| **F-410** | Ostacolo sospeso vicino: non visto, e sotto è «libero» | `sospeso_2p0m`: 97,5 % | limite da dichiarare |
| **F-411** | La regione dichiarata non informa, e la previsione a velocità costante sbaglia su chi si ferma | caso b: 3,78 m oltre 3 s; raggio 3,5 m a 3 s | q = 0,1 e regione ritagliata sul cuneo (validazione-8): non provata; il predittore lo sceglie f8 |
| **F-412** | Le soglie di punti sono assolute | 848×480 con soglia 40: 0 su 10; con 160: 10 su 10 | come F-401 |
| **F-413** | L'«anello cieco» è una striscia: a ±44° il suolo si vede solo da 1,69 m | prova P1 della catena | ridisegnare la zona di B7 |

## 4. Che cosa la squadra guadagna per le 14 ore

- **Ambiente** pronto e ricreabile: `ambiente/venv` (Python 3.14, numpy, scipy, opencv, rosbags), `03-infrastruttura/crea_ambiente.sh`, versioni congelate.
- **Formato comune** delle sequenze e controllo: `03-infrastruttura/formato_sequenza.md`, `controlla_sequenza.py`. Simulatore, registrazioni pubbliche e sensore futuro entrano nella catena per la stessa porta.
- **Catena di riferimento**: `10-catena/` (dieci moduli con solo numpy, 25 prove in 6 s, `esegui.py`, invarianti come controlli, innesto del predittore). È il punto di partenza del prototipo, con i difetti F-401…F-413 noti.
- **Sensore simulato**: `11-simulatore/` (tre profili da scheda, due livelli, filtri del costruttore, verità esatta; 162 sequenze, 1,9 GB, più la generazione in memoria). **Avvertenza:** è verificato contro il proprio modello, non contro un sensore, ed è ottimistico sui buchi (K-407).
- **Dati veri**: `12-dati-veri/` (8 sequenze, 2 tracce THÖR, convertitori). Servono a provare il lettore, il costo e il moto dei pedoni; non il «libero» né l'identità.
- **Banco di regressione**: `sh 20-validazione/rifai.sh` e `sh 22-avversario/rifai.sh`. Le soglie di oggi: 0 «libero» in ombra; continuità 0 su 90 (da portare a 29 su 30 per caso); pannello «si muove» 79 su 90; 28 tracce sul pavimento vuoto; scatola a 2 m 10 su 10; più le quattro scene d'attacco (posa, ostacolo muto, due persone, occlusore mobile).
- **Registrazione dal sensore**: `04-embedded/registra_sequenza.py`. Formato verificato; **mai provato su un dispositivo vero**.

**Per il coordinatore, prima di un commit:** `scaricati/` (3,9 GB) non ha un `.gitignore`, e Princeton e i file di esempio RealSense non dichiarano una licenza: non vanno nel deposito.

**Tabella di decisione per l'inventario** (da `04-embedded/INVENTARIO_E_DECISIONE.md`; i tempi sono stime dell'autore, nessun dispositivo collegato).

| Se nell'inventario c'è | Che cosa si fa |
|---|---|
| RealSense D435, D435i, D455, D415; Orbbec Gemini, Astra 2, Femto; OAK-D Pro | **sorgente principale**; primo fotogramma in 15–40 minuti, poi i dieci minuti di registrazione del §4 di quel file |
| L515, Kinect v1, Astra prima serie, OAK-D senza proiettore | solo se è l'unica (1–2 ore); con Kinect v1 e Astra il suolo si vede da 1,55–1,62 m: la zona di valutazione va riscritta |
| Azure Kinect, Kinect v2 | raffinamento, o niente (1–4 ore, può fallire) |
| iPhone Pro (dal 12) o iPad Pro (dal 2020) di uno dei cinque | **profondità vera registrata subito**, senza aspettare; dati, non demo |
| solo webcam, ToF multizona, LiDAR 2D, radar, ultrasuoni, IMU | nessuna sorgente per il nucleo (senza suolo visto non nasce «libero»): si resta sul simulato; la webcam fa da video di verità |
| il sensore resta a casa | registra e spedisce; la demo è la riproduzione delle sequenze, dichiarata come tale |

## 5. Per il documento finale (giuria mista)

1. **Il sistema non dichiara mai «libero» ciò che sta nell'ombra di un ostacolo**: 0 casi su 2,9 milioni di controlli (una cella in un fotogramma), con tre forme d'ombra. *Provato su profondità simulata dalle schede tecniche di tre camere, con la posizione della camera nota; non su un sensore vero.*
2. **Chi sparisce dietro un ostacolo fermo non finisce mai su una zona detta libera, e nel 97 % dei fotogrammi sta dentro l'avviso di «possibile presenza»** (2939 su 3038). *Stesso stato; una persona alla volta.*
3. **L'ombra che il sistema stima dietro un ostacolo dista meno di 20 cm da quella vera.** *Profondità simulata, condizioni nominali, un pannello.*
4. **Su persone vere che camminano, la zona prevista contiene la persona nel 98–100 % dei casi fino a 3 secondi; l'errore tipico è 0,2 m dopo 1 s e 0,8 m dopo 3 s.** *Provato su tracciati pubblici di 9 persone registrati con cattura del moto (THÖR), non con una camera di profondità, e con misure buone fino all'ultimo istante.*
5. **Abbiamo trovato prima di costruire dove il progetto cede**: con il rumore realistico la stessa identità al ritorno non regge (0 su 90) e si recupera correggendo una soglia (41 su 45). *Simulato, a una sola risoluzione.*
6. **Il ciclo di calcolo costa in media 6 ms su una CPU da portatile**, e tutto è rifacibile con un comando. *Scene simulate; su una scena vera affollata sale a 81 ms.*

**Da NON dire:** «validato su dati veri» o «sul sensore» per libero, ombra, identità, rumore; «identità mantenuta al 100 %»; «mai libero dove c'è un ostacolo» senza «a posa nota e se l'ostacolo risponde»; «soglia 40» senza la risoluzione; «errore di 0,2 m a 1 s» come prestazione del prototipo (0,32–0,52 m con misure peggiori; circa 1 m a 2 s per chi si ferma, N = 12); «bassa latenza» o «15 Hz»; qualunque cifra su sole, pavimento lucido, due persone, sensore in moto.

## 6. Prossima prova e decisioni

**Senza sensore (subito):** eseguire F-401 e F-402 sulle sequenze esistenti, a 424 e a 848 pixel. Criterio scritto dai ruoli: continuità almeno 28 su 30 **e** scatola a 2 m vista almeno 9 volte su 10. Se cade, la continuità dell'identità resta smentita anche in simulazione.

**Con il sensore, le prime tre misure** (soglie già scritte da validazione-9, avversario-1, statistico-2):
1. **Posa e pavimento vuoto, 30 s**: 0 tracce confermate; un oggetto di 10 cm a 2,5 m esce «occupato»; pixel validi sul suolo fra 2 e 3 m. Decide F-403, F-404 e la portata del «libero».
2. **Pannello sul suolo segnato col nastro, 150 fotogrammi**, poi altre quattro forme d'ostacolo: celle «libero» dentro l'ombra vera (soglia 0) e banda senza dato sui due lati. Decide K-014 e H-402.
3. **30 passaggi dietro il pannello con un metro a terra, più la mano sul sensore**: continuità 29 su 30; rumore del centro contro il metro; filtri davvero spenti. Decide H-403, H-404 e la condizione 1.

**Decisioni dell'utente.**
1. **Telefono e inventario:** chiedere ora ai cinque se c'è un iPhone Pro o un iPad Pro (profondità vera subito), e dire se il sensore di casa può arrivare in sala: senza, la demo è una riproduzione dichiarata.
2. **Dati con occlusioni lunghe:** ammettere `http://` per il solo archivio di Friburgo (2,81 GB, tre Kinect fermi, visibilità annotata), che lo scaricamento a regola ha rifiutato. Fra le fonti raggiungibili senza browser né richiesta è la sola con tratti nascosti lunghi di persone e profondità vera (quanti: non verificato).
3. **Che cosa promettere:** la continuità dell'identità come «in correzione» (oggi 0 su 90), oppure tacerla finché F-401 non passa; e q = 0,2 (prudente, regione larga 3,5 m a 3 s) contro 0,1 (più stretta, non ancora provata su dati nuovi).

Controfirma: arbitro
