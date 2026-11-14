# Selezione dopo il torneo — percezione-challenge, f2/05 (`sciame-arbitro`)

**In testa.** Ramo portante proposto: **H-012**, riformulata. Nessuna H# è smentita per intero; tre clausole sono smentite da controlli che non usano il prototipo dell'autore (H-003 al petto, H-008 «0 libero falsi», H-017 «si spegne da solo»). H-019 scende a RIFORMULARE e non a smentita: il controllo usa una copia del codice dell'autore. H-005, H-011 e H-020 non sono state attaccate (0 righe in `TORNEO.md`): restano alla classe del triage. **Scostamenti miei:** (1) seguo le tre pagine del coordinatore, non le due di `TASK.md`; (2) ho letto anche `regole_challenge.md`, i file dei risultati del torneo e, con `grep`, `sciame/PIPELINE.md`; (3) due conti miei, marcati **[arb.]**; nessuno script scritto. **Cifre ricontate sui file** (`esito_attacchi*_parte1.txt`, `risultati_{A,A2,B2,C,D,E}_parte2.txt`, `risultati_{main1,main2,k001,ombra,falso,due,vmax}_parte3.txt`): quelle che cito tornano, con tre note; gli script non li ho rieseguiti. (a) Tempo a 320×240: il file dà 5,1 ms, `TORNEO.md` 4,7. (b) «Gemini 335: 12 cm» non è nell'uscita dello script; il conto torna (0,015 · 2 m · 4 = 0,12 m [arb.]). (c) **Parte 2 e parte 3 usano due geometrie**: nella 2 «pannello W» è la larghezza del buio alla distanza del pedone; nella 3 il pannello da 1 m a 2 m fa 2 m d'ombra a 4 m. Con q = 0,2 e r_max = 1,5 m l'identità al transito è 0,811–0,998 nella 2 (W = 1 m) e **30 %** nella 3 (`risultati_main1_parte3.txt`, riga 19, `kf15`); la 2 stessa dà 0,544 con W = 2 m a 1,3 m/s. Quindi «H-012 regge» vale per la copertura, non per la clausola r_max fisso. Tutto ciò che segue è simulazione o scheda: nessun sensore, nessun pedone vero, **sensore sempre fermo**.

## 1. Esiti del torneo per H#

| H# | Classe dopo il torneo | Numero che decide (file) | Posto nella soluzione integrata |
|---|---|---|---|
| H-001 | regge fino a 3 m; a 4 m non risolta; «3–6 m» da riformulare | al limite dichiarato 8–16 cm a 4 m, 18–36 cm a 6 m (`esito_attacchi_parte1.txt`, P1; schede in comune con l'autore) | **adottata**: camera stereo attiva + IMU, portata dichiarata 0,5–3 m; un buco è «nessun dato» |
| H-002 | RIFORMULARE | gradino 5,4σ: regge; a 15° l'ostacolo a 1,8 m si vede solo oltre 2,41 m (P2b) | **adottata, fusa con H-001**: inclinazione e cono cieco dichiarati; montaggio verticale (`avversario-1`) in gara, §4 |
| H-003 | smentita la variante al petto (vale per l'idea: schede e ipotesi dell'avversario, niente dell'autore) | 1,7–1,9 punti su una gamba a 5 m (< 4); 127°–155° coperti dal busto (P3) | **esclusa** dal ramo; su palo solo se l'utente vuole i 360° (§6). Fonti: LD19 tiene 30 klx, non 60 |
| H-004 | RIFORMULARE | nessuna frase prescrittiva scoperta; tre non prescrittive, fra cui «riconoscere» (1 occorrenza, ricontata) | **adottata** (ambito e soglie), con persona / non persona fuori dal percorso critico o lettura dichiarata |
| H-005 | RIFORMULARE (triage; non attaccata) | il suo 21,6 % non si riproduce con il filtro della parte 2: 2,3 % (`risultati_E`) | **facoltativa**: posa su treppiede; dipende dalla decisione 1 |
| H-006 | regge con riserva | 0 su 7 in COCO (lista dell'autore); percorso minimo 20 ms a 640×480, non è il prototipo; «≤ 80 ms» non risolta | **adottata**: percorso critico geometrico, rete in asincrono. Fonti: YOLO26n 38,9 ms su CPU, AGPL-3.0; RF-DETR-N Apache 2.0 |
| H-007 | RIFORMULARE il motivo | camere ToF: al più 120° (ricerca non esaustiva; fonti, P1: regge) | **assorbita da H-006**; il «peso tipico di classe» è **escluso**: nessuna decisione lo legge |
| H-008 | smentita la clausola «0 libero falsi» (vale: script e casi dell'avversario); il nucleo regge | vetro → «libero»; mobile a 3 m/s: 1,50 m contro 0,7 di margine; fantasma a 60 s (P8, PK6) | **adottata** con quattro correzioni: «libero» mai ricordato; «occupato ricordato» con l'età; suolo locale o piano dichiarato; chiusura della traccia tolta (va a H-012) |
| H-009 | RIFORMULARE | a 1 s il disco copre il 97,8 % dell'ombra (1 m), 59,8 % (2 m); con ombra a +20 cm il 14,4 % è su celle libere | **radicale, adottata come strato di garanzia** (§4); v_max dichiarata con margine |
| H-010 | RIFORMULARE | χ² a 0,5 m/s: 75,4 % entro 1 s; falsi sul muro a 4 m 15,5 % con R fisso, 0,0 % con R(z); con R(z) chi si avvicina a 4 m è visto nell'11,0 % (`risultati_E`) | **adottata** come stimatore sul visibile, con R(z) per asse e velocità minima dichiarata; la regola «mobile» è **in gara** (K-007) |
| H-011 | RIFORMULARE (triage; non attaccata) | fonti: 0,39/0,83 contro RED 0,44/0,91 confermati; nella stessa tabella S-GAN 0,32/0,60 sta sotto: «regge» vale contro RED e SR-LSTM (non riletto da me) | **adottata in due regole**: i modelli appresi non decidono mai un allarme; calibrazione a posteriori. Le soglie vengono da H-012 |
| H-012 | **regge** sulla copertura; clausola r_max fisso RIFORMULARE (nota c) | q = 0,2 su tre generatori non dell'autore: 0,927 / 0,916 / 0,902 a 2 s; q dal NIS sui tratti dritti = 0,01 → 0,738 / 0,710 (`risultati_A`, `_A2`) | **ramo portante** (§4) |
| H-013 | RIFORMULARE; «la geometria basta» smentita in simulazione | tornano entrambi: scambi 0,440; incrocio dietro 2 m: 0,246, muti 0,238 (`risultati_B2`); q = 0,5 dà 1,20 s | **adottate le regole**: priorità alle confermate, tentativa 3 su 5 (non attaccata), «identità ambigua». **Escluso** q = 0,5 |
| H-014 | RIFORMULARE (esito misto) | scade a 1,12 s, il transito dura 1,70 s: PREVISTO vivo 0 %; chiusa a persona nascosta 10–26 % con un fotogramma, 45–50 % con ombra a −20 cm | **adottata la sola prova del raggio** come regola di rilascio (≥ 3 fotogrammi, fuori dalla fascia di guardia). **Esclusa** la scadenza a 1 m |
| H-015 | RIFORMULARE | senza «sosta» 71 % / 28 % (< 80); con «sosta» 100 % / 76 %; ombra a −20 cm 68 %; esce dal lato lontano: 22 / 41 % | **facoltativa**, solo se la decisione 2 chiede R3 sulle soste |
| H-016 | RIFORMULARE | falso «libero» di 4 / 5 / 7 fotogrammi (0,27–0,47 s) porta la massa giusta sotto il 5 % | **facoltativa** con H-015; adottato per tutti il vincolo «evidenza negativa solo dove la profondità è valida» |
| H-017 | smentita la clausola «si spegne da solo» se «fresco» = marca temporale (vale: non esiste un prototipo); il resto APERTA | battito per 25 s a percezione ferma; 0,13 s con il contatore di fotogramma (P17) | **adottata la regola di freschezza** (contatore del sensore fino all'uscita) per R6; il battito è **in gara** con i messaggi (K-010) |
| H-018 | RIFORMULARE | finestra 1,60 s solo con (0,2; 1,5 m); a 0,8 m/s: 0,811 con 1 m di buio, ≤ 0,004 con 2 m (`risultati_C`) | **adottata** (demo): si fissa la larghezza dell'ombra alla distanza dell'attore, non quella del pannello |
| H-019 | RIFORMULARE (0,633 < 0,75, ma il controllo copia `approach()` e il filtro dell'autore: non è smentita dell'idea) | tarata sulla squadra, provata sul giurato lento con soste: 0,633; finestra larga 2,52 s se tarata largo (`risultati_D`) | **facoltativa** dentro l'atto 4 di H-018, con tre esiti in tabellone e soste nella taratura |
| H-020 | RIFORMULARE (triage; non attaccata) | nessuna prova nuova | **esclusa**: con la classe fuori dal percorso critico manca la risorsa da spartire |

## 2. Contraddizioni K#

| K# | Stato | Prova, o ciò che la deciderebbe |
|---|---|---|
| K-001 | risposta «sì» in simulazione; **aperta sul vero** | chiusa a persona nascosta: 10–26 % (un fotogramma); con tre: 0 % a 4 m, 14 % a 3 m, 53 % a 2,5 m. Decide: 20 soste registrate dietro un pannello vero |
| K-002 | **aperta**: nessuna famiglia vince | a 3 s contengono senza toccare celle libere disco e particelle con sosta, non il cerchio (a 2 s 51 % dell'area su celle libere); a 1 s informano cerchio e particelle, non il disco. La composizione che le unisce non è provata come insieme (§5, prova A) |
| K-003 | **risolta in simulazione**: q = 0,2 | 0,902–0,927 a 2 s (soglia 0,85); q = 0,1 al limite (0,839); q = 0,5 troppo largo. Sul vero: 30 occlusioni registrate |
| K-004 | **risolta nel verso, aperta nel numero** | il «previsto» deve durare quanto il transito più lento: nessuna soglia fissa lo fa con 2 m d'ombra (nota c). Va legato all'ombra. Aperto: corpo largo, buio di (W + 0,45)/v |
| K-005 | **decisione dell'utente** (2) | con l'ellisse la sosta scade (R6); l'identità (R3) solo con particelle, modo «sosta» e fascia: 100 % / 76 % |
| K-006 | **risolta per composizione**, a ragionamento e su uno script; non su registrazioni | «libero» = suolo visto ora, mai ricordato (H-008); «occupato» con l'età, scade a «sconosciuto» (H-009). Il vetro rompe tutte e due: resta aperto |
| K-007 | in parte **apparente** (filtri diversi: 21,6 % contro 2,3 %), in parte **aperta** | la χ² non vede il lento che si avvicina; lo spostamento su 1 s (98,7 %; 0 falsi su 4000) è esplorativo, notato dopo, solo con rumore isotropo. Decide la prova B, poi un muro e una persona lenta a 2 e 4 m |
| K-008 | **decisione dell'utente** (1) | dato nuovo: tutte le prove sono a sensore fermo |
| K-009 | 360°: **risolta** per i sensori citati; sole: **aperta** | scheda ST del VL53L7CX: «three sensors can cover 180° x 60°»; discordanza vera fra costruttori (Luxonis «<2% outdoors», Orbbec «Indoor» o «Indoor/Semi-Outdoor»). Decide: cinque minuti al sole |
| K-010 | **aperta**, fuori dalle classi 1–2 | servono persone bendate. Fonti: in due studi l'aptico costa più dell'audio; non decide fra battito e messaggi |
| K-011 | R3: **fissata**; R7: **aperta** | R3: 26 riemersioni su 30 nella regione, a ombra fissata; il 26/30 boccia una taratura buona (0,895) una volta su cinque. R7: 80 e 150 ms non dicono da dove a dove |
| K-012 | **apparente, risolta dalle fonti** | Femto Bolt 2,88 e 2,21 m, VL53L7CX 3,5 e 2,0 m: due modi di funzionamento ciascuno |

## 3. Fatti F# aggiornati

- **F-001** rafforzato: lo scrive la scheda ST (180° con tre sensori). Con tre camere iToF da 120°: ancora non risolto. I 360° li dà un LiDAR a scansione, non tre ToF (prezzo non verificato).
- **F-005** ristretto: resta **verificato alla lettera** sui termini elencati; «riconoscere» compare una volta, in una frase non prescrittiva che lo dà per presupposto. La conseguenza «le regole non chiedono di riconoscere» passa a **non risolto**: è una lettura, da dichiarare.
- **F-006** precisato: con q = 0,2 la finestra del «previsto» è 1,60 s (`risultati_C`); la copertura tiene anche a 3 s (0,93), ma con raggio 3,63 m: copre senza informare. Resta sostenuto solo da simulazioni.
- **F-007** rafforzato da una quinta scena, non degli autori (parte 3).
- **F-008** non toccato dal torneo: nessuna prova con il sensore in moto. **F-002, F-003, F-004** invariati (F-002: fonte confermata; il «fattore 1,68» è derivato).

## 4. Selezione

| | H# | Informazione attesa | Costo | Probabilità di un controesempio |
|---|---|---|---|---|
| 1, **portante** | **H-012** | 1ª: chiude K-002 e K-004 e porta R3, R4, R6 | 2º: riuso di `scena_parte3.py`, più il corpo largo | 1ª: l'insieme non è mai stato provato |
| 2 | **H-010** | 2ª: R1 non ha ancora una regola che regga (K-007) | 1º: uno script | 2ª: chi si avvicina a 4 m: 11,0 % |
| 3 | **H-004** | 3ª: ambito e soglie; tiene la copertura di R1–R8 | 1º: a mano | 3ª: nessuna frase prescrittiva scoperta |
| radicale | **H-009** | regge R8: mai «libero» sul non osservato | dentro la prova A | bassa sul contenimento (per costruzione), alta sul rilascio |

**Perché H-012 è il ramo portante.** È l'unica della sua famiglia che ha retto su generatori non dell'autore; i suoi tre stati sono l'uscita che R3, R4 e R6 chiedono; le altre H# si agganciano a lei senza cambiarne l'enunciato. **Riformulazione obbligata:** (i) il «95 %» si dichiara 0,90–0,93; (ii) q si tara sulle innovazioni alla ricomparsa; (iii) il cerchio si ritaglia sulle celle non osservate; (iv) oltre r_max la traccia non «scade»: resta lo strato di garanzia; (v) la fine del «previsto» si lega all'ombra.

**Le due proposte del torneo.** `avversario-3` è una riformulazione congiunta: lo strato di garanzia è H-009 riformulata (il disco senza il raggio che cresce), con il rilascio di H-014 riformulata e il «libero» di H-008; lo strato d'informazione è H-012 con le correzioni (iii)–(v); l'«identità ambigua» è la correzione di H-013. **Non provato:** l'insieme (lo dichiara l'autore); lo strato 2 ritagliato (il 77–100 % a 1 s è sul cerchio intero); la fascia «20 cm più mezzo corpo»; il rilascio, perché chi esce dal lato lontano lascia l'ombra «possibile presenza» senza fine; la soglia «metà dell'ombra», scelta dall'avversario; sensore in moto, falsi allarmi, rumore che cresce con la distanza. `avversario-1` è una riformulazione di H-002 (e di H-001, stesso sensore). **Non provato:** l'asta vera a 1,8 m; se 58° in orizzontale bastano alla demo (a 4 m sono 4,43 m di scena contro 7,59 [arb.]); l'altezza di 1,2 m; su treppiede il problema cambia.

**Restano in gara, senza vincitore.** Regola «mobile»: χ² con R(z) contro spostamento su 1 s. Feedback: battito contro messaggi. Montaggio: orizzontale contro verticale. Sosta: scadenza contro particelle.

## 5. Che cosa il ramo portante deve provare in f4

- **A. La composizione come insieme** (simulazione su CPU, autore diverso dall'avversario, previsione scritta prima): quattro comportamenti × due ombre, **corpo largo 40 cm**, errore d'ombra ± 20 cm. Soglie: strato 1 contiene il nascosto nel ≥ 99 % e sta su celle viste libere per lo 0 % oltre la fascia; strato 2 ritagliato contiene alla riemersione nel ≥ 85 %; il rilascio ha una durata finita e dichiarata. La smentisce un solo nascosto fuori dallo strato 1.
- **B. R1 e ciclo di vita con rumore che cresce con la distanza:** stesso filtro, R(z) da una scheda (fonte indipendente). Soglie: falsi «mobile» sul muro ≤ 10 % a 4 m; pedone a 0,5 m/s visto entro 1 s nel ≥ 90 % alla distanza dichiarata, anche in avvicinamento. Decide K-007.
- **C. Copertura e latenza, a mano:** tabella R1–R8 → componente → misura di accettazione, con la lettura di «riconoscere» scritta; bilancio della latenza con gli estremi nominati e una fonte per il sensore e per l'audio. Se manca la fonte, R7 resta «non risolto» e si dichiara.

**Resterà «non verificato» fino all'hardware:** vetro, tessuti scuri e sole; pedoni veri (30 occlusioni, 20 soste); maschera d'ombra dalla profondità vera; sensore indossato in moto (F-008); latenza dal fotone al suono; fotogrammi ripetuti dalla camera scelta; feedback con persone bendate (K-010); prezzi e reperibilità.

## 6. Decisioni che spettano all'utente

1. **Applicazione e posa** (K-008): assistiva o industriale; sensore fermo o indossato. Solo il sensore fermo ha prove.
2. **Che cosa mostra la demo sulla sosta** (K-005): perdita di affidabilità dichiarata (nessuna particella) oppure continuità (particelle con «sosta»: più lavoro, 76 % con l'ombra larga).
3. **Sensore, 360° e ipotesi di fattibilità** (K-009, H-003): quale sensore la squadra possiede; se i 360° servono (le regole non li nominano; tre ToF multizona ne danno 180°); durata, squadra e bilancio, che nessuno ha verificato.

Controfirma: arbitro
