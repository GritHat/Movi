# Scenari e requisiti di distanza e di tempo — veicoli veloci (f15, 03-scenari)

Ruolo: esperto di dominio. **Campo in cui parlo:** sorveglianza aeroportuale e dello spazio aereo a bassa quota, sistemi senza equipaggio, sicurezza dei trasporti. Non sostituisco un professionista abilitato né un'analisi di sicurezza. 15-11-2026, ore 00:01–00:10 (la consegna dice 14-11: l'orologio aveva passato la mezzanotte).
File: `scenari.json` (sei scenari nel formato comune), `conti.py` → `conti_esito.txt` (comando: `python -I conti.py`), `PREVISIONI.md` (scritte alle 00:01:24, prima delle fonti e dei conti).

## 0. Cambi di stato e regole violate

- **Tutto è conto su valori di fonte, di `classi.json` (f14) o d'ipotesi. Niente è provato su un sensore fisico; niente è «validato».** Gli scenari sono nominali, scritti a mano: non sono dati registrati.
- **Smentita esperto-dominio-P5** (treno: d > 500 m): in stazione a 60 km/h vengono 261 m; regge solo in linea a 160 km/h (798 m). Le altre sei reggono (`PREVISIONI.md`).
- Scarto dal piano: 16 pagine cercate, non 12. Aperte con il dato 13 su 16 (81 %, Wilson 95 %: 57–93 %). Non aperte: FAA AC 90-48 (403), EUR-Lex 2019/947 (pagina vuota), SKYbrary (blocco). Nessun file scaricato (pagine lette con lo strumento di lettura; richieste senza nomi né dettagli del progetto).
- La colonna «sensore» della tabella 1 è **a memoria, non verificata**: le portate le decide 02-sensori dalle schede.
- Regole violate: nessuna che io sappia. Tempo usato: circa 10 minuti su 30.

## 1. Gli scenari e la distanza d'avviso

d = v_rel·(latenza + reazione) + spazio di manovra + margine. Stato dei valori: **F** fonte aperta oggi, **C** `classi.json`, **I** ipotesi, **M** a memoria non verificato. Geometrie in metri (x est, y nord, z quota), sensore principale nell'origine: i poligoni e i punti sono in `scenari.json`. Occlusioni calcolate a passi di 0,1 s sul raggio sensore–centro dell'oggetto.

| | Scena (sensore; ostacolo; moto) | Occlusione | Chi riceve l'avviso; tempi | v_rel | d richiesta | Sensore che la può dare (M) |
|---|---|---|---|---|---|---|
| **A1** | palo a 10 m; edificio 80×40×15 m a 300 m; multirotore piccolo a 15 m/s (max 21 F1), da 990 m, scende a 12 m e passa dietro | 8,0 s; entra a 440 m, esce a 375 m | operatore di sito: latenza 1 s (I), reazione 5 s (I), 30 s per mettere in sicurezza l'area (I), margine 50 m (I) | 21 m/s | **806 m** (38 s) | radar di sorveglianza per piccoli bersagli + ottico o termico per la conferma; ricevitore d'identificazione remota se il mezzo coopera |
| **A2** | palo a 25 m; hangar 60×60×18 m; aereo in rullaggio a 9,0 m/s (C, F6) sulla via dietro l'hangar; mezzo a 8,3 m/s (C) che la attraversa; persona a 1,4 m/s | aereo: 17,1 s; esce a 63 m dal punto d'incrocio | conducente del mezzo e operatore di sito: 1 s (I) + 2,5 s (F9, presa dalla strada: I sul piazzale); frenate 1,0 e 1,5 m/s² (C) = 63 m; margine 23 m (mezza apertura alare M + 5 m I). Via torre e radio: 10 s (I) | 17,3 m/s | **147 m**; via torre **277 m** | radar di superficie o lidar a lunga portata su palo; multilaterazione e ADS-B per chi coopera |
| **A3** | radar a 10 m presso la soglia; fascia di alberi ed edifici alta 25 m a 1,1–1,2 km; aereo in finale a 70 m/s (cat. C: 121–141 nodi F2) su sentiero a 3° (F3); multirotore a 2,5 km che scende da 120 m a 30 m sull'asse | il drone sparisce a t = 11,4 s (sotto 43 m circa) e resta nascosto; l'aereo è allora a 2,7 km da lui e lo raggiunge a t = 50 s | operatore di torre che avverte l'equipaggio: 4 s (M) + 10 s (I) + 12,5 s (M: AC 90-48, non aperta); 10 s perché la riattaccata separi (I); margine 610 m (M) | 91 m/s | **3,9 km** (43 s; per confronto, il TCAS avvisa a 40 s e ordina a 25 s: F4) | solo radar di sorveglianza con copertura bassa, più i cooperativi (ADS-B per l'aereo, identificazione remota per il drone); nessuna camera né lidar |
| **A4** *(solo analisi)* | sensore su un multirotore in volo stazionario a 30 m, posa supposta nota; edificio alto 45 m; altro multirotore a 15 m/s | 5,5 s; entra a 158 m, esce a 109 m | pilota remoto: 0,5 s (I) + 3 s (I), scarto di 10 m in 2 s (I), margine 10 m (I). Sistema di bordo: 0,4 s (I) | 21 m/s | **126 m**; di bordo **60 m** | radar a onde millimetriche o lidar di bordo; ottico |
| **S1** | palo a 6 m all'incrocio; camion fermo 16,5×2,6×4 m; auto a 13,9 m/s (C) | 3,2 s; esce a 10 m dal punto d'incrocio | conducente: 0,1 s (I) + 2,5 s, frenata 3,4 m/s² (F9) = 28 m, margine 2 m (I). Di bordo: 0,5 s (I), 6,9 m/s² (C) | 13,9 m/s | **67 m**; di bordo **24 m** | radar a 77 GHz o lidar su palo |
| **S2** | sensore a fine banchina; convoglio fermo 200×3×4,3 m; treno in ingresso a 16,7 m/s (C) sul binario dietro; variante b: linea a 44,4 m/s verso una galleria | 23,3 s: si ferma ancora nascosto (l'avviso resta acceso) | personale e macchinista: 1 s (I) + 3 s (I); frenata di servizio 0,8 m/s² (C) = 174 m; margine 20 m (I). b: 600 m d'emergenza da 160 km/h (F10) | 16,7; b 44,4 m/s | **261 m**; b **798 m** | radar o lidar a lunga portata lungo linea; il segnalamento resta la protezione vera |

**Tre cose che il dominio insegna da questa tabella.**
1. **La camera a 3 m non entra in nessuno scenario** (d minima 24 m): serve un altro ordine di grandezza, da 10² m sul piazzale a 10³–10⁴ m in avvicinamento.
2. **L'occlusione cade dentro la distanza d'avviso.** In A1 il drone riappare a 375 m con 18 s di volo, e all'operatore ne servono 38; in A2 l'aereo esce a 63 m dall'incrocio contro 147 richiesti; in A3 il drone sparisce con l'aereo a 2,7 km contro 3,9. Un sistema che avvisa solo quando rivede arriva tardi: **l'avviso deve partire prima e restare acceso durante l'occlusione.** È il principio di MoVi, e a questa scala diventa necessario, non solo prudente. (Notato dopo i conti, non previsto.)
3. **L'errore tipico del non addetto:** leggere la portata di scheda come distanza d'avviso. La portata vale per una sezione radar o una riflettività dichiarata; un multirotore piccolo ha una sezione radar dell'ordine di 0,01 m² (M), e la linea di vista bassa è tagliata dagli ostacoli (in A3 tutto ciò che vola sotto 43 m circa a 2,5 km è in ombra).

Limiti degli scenari: ostacoli estrusi, bersaglio puntiforme (un aereo lungo 37,6 m (F: classi.json F8) spunta prima del suo centro: l'occlusione parziale non è modellata); velocità costanti a tratti; niente vento, pioggia, riflessioni multiple o uccelli; i tempi di reazione fuori dalla strada sono quasi tutti ipotesi e pesano molto (in A1 il 78 % di d viene dai 30 s ipotizzati).

## 2. «Possibile presenza» e «zona prevista» a questa scala

Raggio dell'insieme raggiungibile senza osservazioni, r = v_max·t (inviluppo: quello che usa la regola di sicurezza), da `conti_esito.txt`:

| Classe (v_max) | forma | 5 s | 10 s | 30 s |
|---|---|---|---|---|
| persona a piedi (2,5 m/s C) | disco | 12 m | 25 m | 75 m |
| mezzo di piazzale (8,3 C) | disco | 42 m | 83 m | 249 m |
| aereo in rullaggio (15,4 C) | corridoio sulla via di rullaggio | 77 m | 154 m | 462 m |
| auto urbana (13,9 C) | corsie | 70 m | 139 m | 417 m |
| multirotore piccolo (21 F1; salita 8 m/s F1) | sfera 3D | 105 m | 210 m | 630 m |
| treno in linea (44,4) | segmento sul binario | 222 m | 444 m | 1332 m |
| aereo in finale (72,5 F2) | tubo sul sentiero | ±26 m lungo il sentiero | ±51 m | ±154 m |

- **Chi è vincolato si prevede bene, chi è libero no.** Treno e aereo in finale vanno veloci, ma su una linea: la «zona prevista» è un tratto stretto, e l'incertezza è quasi solo lungo il percorso. Il multirotore è lento al confronto, ma in 10 s può essere ovunque in una sfera di 210 m: oltre pochi secondi la «zona prevista» non dice più nulla di utile e resta, onesta, la sola **«possibile presenza»** sull'intero insieme raggiungibile.
- La zona prevista vale se l'etichetta è giusta; **l'avviso no**: con etichetta assente o dubbia si usa l'inviluppo della classe più veloce plausibile. Nessuna etichetta riduce un avviso.
- Dopo 30 s l'insieme di un multirotore copre un sito intero: in pratica l'avviso si toglie solo **tornando a guardare** il volume (un altro sensore, un altro punto di vista), ed è la ragione operativa del multisensore.

## 3. Che cosa esiste già nel dominio (ispirazione; **nessuna dichiarazione di conformità**)

- **Tracce mantenute senza aggiornamenti («coasting»).** I tracciatori radar predicono la posizione di una traccia non aggiornata e la cancellano dopo M mancate conferme (tipicamente 3) o quando la covarianza supera una soglia (F5). MoVi fa la stessa cosa ma **dichiara** lo stato all'operatore e non trasforma la cancellazione in «libero». Il termine «coasted» è d'uso nel settore: nella pagina aperta non compare (M).
- **Sorveglianza di superficie e allarmi d'incursione.** ASDE-X e ASSC fondono radar di superficie, multilaterazione, ADS-B e radar terminali, e danno all'operatore allarmi visivi e sonori (F6). Le luci di stato della pista sono automatiche, **consultive**, indipendenti dalle autorizzazioni; nella prova di Boston, su 8 298 movimenti, oltre il 98 % d'accordo con le istruzioni del controllo (F7). Modello utile: avviso a più destinatari, la decisione resta all'uomo.
- **Separazione e volumi protetti.** Minime radar di 3 miglia nautiche in terminale e 5 in rotta, 1000 piedi in verticale (F8); il TCAS protegge un volume che dipende da quota e velocità e ragiona **in tempo** (40 s, 25 s), non in distanza (F4). Suggerisce di esprimere anche le soglie di MoVi in secondi al punto d'incontro.
- **Identificazione remota dei droni.** Trasmissione di identità, posizione, quota, direzione e velocità su Wi-Fi e Bluetooth (ASTM F3411; in Europa prEN 4709-002), obbligo negli USA dal 16-9-2023 (F11). Per MoVi è un sensore **cooperativo**: conferma chi collabora, e il suo silenzio non prova un'assenza.
- **Categoria aperta e U-space.** Sotto 120 m dal suolo; 30 m dalle persone non coinvolte in A2, 150 m in A3 (F12); servizi U-space d'identificazione di rete, geo-consapevolezza, autorizzazione al volo e informazioni di traffico, regolamento (UE) 2021/664 (F13). Il tetto di 19 m/s per la classe C1 è **a memoria, non verificato** (EUR-Lex non letto).

## 4. Le parole, davanti a una giuria con membri di aerospazio e difesa

- **Da usare:** sorveglianza, monitoraggio, consapevolezza della situazione, traccia, traccia mantenuta senza osservazione, occlusione, copertura e ombra del sensore, sensore cooperativo e non cooperativo, fusione di più sensori, avviso all'operatore, «possibile presenza», «zona prevista», «non osservato», integrità dell'informazione, degrado dichiarato, uomo nel ciclo di decisione, supporto alla decisione, mezzo senza equipaggio, «simulato dalle schede tecniche».
- **Da evitare:** bersaglio, minaccia, intruso ostile, ingaggio, puntamento, inseguimento per il puntamento, contrasto, neutralizzazione, abbattimento, disturbo, intercettazione, «anti-drone», «C-UAS», «difesa del sito» (dire: «rilevazione e avviso di mezzi senza equipaggio»). Nel codice e nei file il nemico lessicale è «target»: usare «oggetto» o «traccia».
- **Da non promettere:** «detect and avoid», «ACAS», «TCAS», «A-SMGCS», «conforme a», «certificabile», «separazione garantita», «copre lo spazio aereo», una portata senza la sezione radar, «rileva tutti i droni», «in tempo reale», «validato». Una giuria del settore riconosce subito un livello di maturità gonfiato: dire «concetto dimostrato in simulazione» vale più di ogni aggettivo.
- **La frase che regge:** «MoVi non dice mai che uno spazio è libero se non l'ha guardato; quando un mezzo sparisce dietro un ostacolo, l'operatore continua a vedere dove può essere».

## 5. Stati proposti

| Enunciato | Stato |
|---|---|
| La portata di 3 m non serve nessuno dei sei scenari (d ≥ 24 m) | sostenuto dai conti (modello: formula di §1, valori F, C e I) |
| In A1, A2, A3 e S1 l'occlusione cade dentro la distanza d'avviso | sostenuto dai conti, su geometrie scelte da me: **non generale** |
| Le distanze d'avviso di A1, A3, A4 | **non risolto**: dipendono da tempi di reazione ipotizzati; li deciderebbe una fonte di fattori umani o una prova con operatori |
| Quale sensore copre quale d | **non verificato**: lo decide 02-sensori dalle schede |
| Oltre 5–10 s la zona prevista di un multirotore non è informativa | sostenuto dal conto (r = 105–210 m); la soglia utile è un'ipotesi |

## 6. Proposte e passo successivo

- **esperto-dominio-1: soglie in secondi.** Meccanismo: l'avviso scatta quando il tempo al punto d'incontro dell'insieme raggiungibile scende sotto latenza + reazione + manovra del destinatario (profilo di chi riceve). Previsione: una sola soglia in tempo dà avvisi tempestivi in A1–S2, una soglia in metri no. Smentita: uno scenario dove la soglia in tempo avvisa più tardi di quella in metri tarata su di esso.
- **esperto-dominio-2: il cooperativo conferma, non libera.** ADS-B e identificazione remota entrano come sensori che possono solo aggiungere presenze. Smentita: una regola della catena in cui il loro silenzio toglie un avviso.
- **esperto-dominio-3: A3 come scena del video**, con l'ombra del radar disegnata (sotto 43 m a 2,5 km) e l'avviso che resta acceso per 38,6 s fino al passaggio dell'aereo.
- **Dopo:** 04-moto genera `verita.csv` da `scenari.json` (raccordi con a_max); 02-sensori riempie la colonna del sensore; un curatore apre AC 90-48, il regolamento 2019/947 e ASTM F3442 per sostituire le voci M.

## Fonti (aperte il 15-11-2026 salvo dove detto)

F1 [DJI Mavic 3](https://en.wikipedia.org/wiki/DJI_Mavic_3): Mavic 3E, 75,6 km/h, salita 8 m/s, 0,915–1,05 kg. · F2 [Aircraft approach category](https://en.wikipedia.org/wiki/Aircraft_approach_category): C = 121–141 nodi; Boeing 737-700 130 nodi. · F3 [Instrument landing system](https://en.wikipedia.org/wiki/Instrument_landing_system): 3°; categoria I 60 m (letti i primi 100 000 caratteri). · F4 [TCAS](https://en.wikipedia.org/wiki/Traffic_collision_avoidance_system): 40 s e 25 s; volume protetto (letti i primi 100 000 caratteri). · F5 [Radar tracker](https://en.wikipedia.org/wiki/Radar_tracker). · F6 [Airport surface detection equipment](https://en.wikipedia.org/wiki/Airport_surface_detection_equipment). · F7 [Runway status lights](https://en.wikipedia.org/wiki/Runway_status_lights). · F8 [Separation (aeronautics)](https://en.wikipedia.org/wiki/Separation_(aeronautics)). · F9 [Stopping sight distance](https://en.wikipedia.org/wiki/Stopping_sight_distance): 2,5 s; 3,4 m/s². · F10 [Emergency brake (train)](https://en.wikipedia.org/wiki/Emergency_brake_(train)): 1,5 m/s²; 250 m da 100 km/h, 600 m da 160 km/h. · F11 [Remote ID](https://en.wikipedia.org/wiki/Remote_ID). · F12 [EASA, categoria aperta](https://www.easa.europa.eu/en/domains/drones-air-mobility/operating-drone/open-category-low-risk-civil-drones). · F13 [U-space](https://en.wikipedia.org/wiki/U-space). · C: `f14-classificazione/01-profili/classi.json` (con le sue fonti F3, F4, F6–F8). · **Non aperte:** [FAA AC 90-48D](https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC_90-48D_CHG_1.pdf) (403), [EUR-Lex 2019/947](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:02019R0947-20220404) (vuota), [SKYbrary, See and avoid](https://skybrary.aero/articles/see-and-avoid) (blocco).
Wikipedia è una fonte secondaria: i numeri vanno ricontrollati sulle fonti primarie prima di citarli in un documento ufficiale. Le pagine sono state lette attraverso un modello che le riassume: le citazioni non sono state ricontrollate sul testo grezzo.
