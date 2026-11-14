# Profili cinematici delle classi e di chi porta il sensore (f14, 01-profili)

Ruolo: esperto di dominio. **Campo in cui parlo:** cinematica di pedoni e veicoli e fattori umani dei tempi di reazione. 14 novembre 2026, 18:33–18:45. Non sostituisce un tecnico della sicurezza: sono valori a priori per un prototipo, non una valutazione del rischio. File accanto: `classi.json`, `profili_portatore.json` (dati e schema), `conti.py` (programma), `conti_uscita.md` e `risultati.json` (uscita completa), `PREVISIONI.md`, `scaricato/` (riassunti da Europe PMC: dati non fidati).

## 0. In testa: cambi di stato e regole violate

- **E7 smentita:** solo **9 velocità su 30** hanno una fonte aperta oggi; 6 sono lette solo nel risultato di una ricerca («non verificato»), **15 sono ipotesi o memoria**. Accelerazioni e frenate sono quasi tutte ipotesi. La tabella delle classi è un **profilo di partenza**, non un riferimento.
- **E6 smentita:** per chi sta fermo la distanza d'avviso di treno e aereo è 13,1 m e 10,8 m, non «oltre 20 m». Avevo confuso lo spazio d'arresto *della classe* (treno 76–92 m, aereo 40–54 m) con la distanza d'avviso *per chi riceve l'avviso*. È l'errore tipico del non addetto, e l'ho fatto io.
- **Modifica dopo il primo conto:** letto il PDF dell'aeroporto di Monaco, ho portato la velocità tipica del mezzo di piazzale da 2,8 a 1,7 m/s; E3 è passata da 11 a 10 classi su 15 (esito invariato).
- **Limite delle letture:** le pagine «aperte» sono lette attraverso lo strumento di lettura automatica, che riassume; ho letto io il testo solo per i riassunti di Europe PMC e per i due PDF (testo estratto in locale). I due PDF li ha salvati lo strumento fuori dalla cartella di consegna, non io.
- **Conflitto da decidere (arbitro):** la V3 finale vieta di dire «drone», «UAV», «in volo», «in movimento»; il requisito chiede la classe «multirotore» e il profilo del velivolo senza equipaggio. Propongo: si nominano **solo come profilo configurato e non provato**.

## 1. Tabella delle classi (valori in `classi.json`; qui l'essenziale)

Fonti: **F** = pagina aperta oggi; **R** = letto in un risultato di ricerca, non verificato; **M** = a memoria, non verificato; **I** = ipotesi. Arresto = v_tip²/(2·dec_tip); fra parentesi con 1,5 s di reazione di chi guida (F3).

| Classe | v tip / max (m/s) | acc. tip / max | fren. tip / max (m/s²) | Gradi di libertà, modello di moto | Ingombro l × l × h (m) | Arresto a v_tip (m) |
|---|---|---|---|---|---|---|
| persona a piedi | 1,4 F1,F2 / 2,5 F2 | 1,0 / 3,0 I | 1,5 / 4,0 I | 2 sul piano, quasi olonomo: cambia direzione e si ferma in un passo; velocità quasi costante 2D | 0,5 × 0,6 × 1,75 I | 0,65 |
| persona di corsa | 3,0 / 8,0 I | 2,0 / 4,0 I | 2,0 / 4,0 I | come sopra | come sopra | 2,25 |
| bicicletta | 4,3 F11 / 8,3 I | 1,0 / 2,0 I | 2,0 / 5,0 I | non olonomo, biciclo cinematico, raggio ≥ 2 m I | 1,8 × 0,6 × 1,7 I | 4,6 (11,1) |
| monopattino | 4,2 I / 5,6 F12 | 1,0 / 2,0 I | 2,0 / 4,0 I | non olonomo, raggio ≥ 1,5 m I | 1,1 × 0,5 × 1,8 I | 4,4 (10,7) |
| carrello elevatore | 2,2 R1 / 4,5 R1 | 0,5 / 1,5 I | 0,9 R1 / 2,5 I | non olonomo, sterzo posteriore (la coda spazza), raggio ≈ 2 m I | 3,5 × 1,2 × 2,2 I | 2,7 (6,0); «circa 3 m a 6 km/h» F10 |
| veicolo a guida automatica | 1,0 I / 2,0 F17 | 0,3 F17 / 1,0 R3 | 1,0 / 2,0 I | uniciclo (gira sul posto) o omnidirezionale | 0,8 × 0,58 × 0,3 F17 | 0,5 (0,8) |
| auto o furgone, area di lavoro | 2,8 / 8,3 I | 1,5 / 3,0 I | 3,4 F4 / 6,9 F3 | non olonomo, biciclo, raggio ≈ 5,5 m M | 6,0 × 2,0 × 2,6 I | 1,2 (5,4) |
| auto o furgone, strada urbana | 8,3 I / 13,9 F12 | 1,5 / 3,0 I | 3,4 F4 / 6,9 F3 | come sopra | 4,5 × 1,8 × 1,5 I | 10,1 (22,6) |
| trattore di piazzale con rimorchi | 1,7 F16 / 8,3 F16 | 0,5 / 1,5 I | 1,5 / 4,0 I | non olonomo articolato: i rimorchi tagliano la curva | fino a 15 × 1,6 × 2,0 I | 1,0 (3,5) |
| aereo in rullaggio | 9,0 F6 / 15,4 M | 0,5 / 1,0 I | 1,0 / 3,0 I | non olonomo, raggio ≥ 20 m I; l'ala spazza oltre la traccia delle ruote | 37,6 F8 × 35,8 M × 11,8 M | 40 (54) |
| aereo al traino | 1,4 R5 / 4,2 R2 | 0,2 / 0,5 I | 0,5 / 1,5 I | articolato, grande raggio | 45 × 35,8 × 11,8 I | 2,0 (4,1) |
| treno in arrivo in banchina | 11,0 / 16,7 I | 0,5 / 1,0 I | 0,8 I / 1,5 F7 | **1**, vincolato al binario; non può scartare | 200 × 2,9 × 4,3 I | 76 (92); 250 m da 100 km/h F7 |
| tram a una fermata | 5,6 / 13,9 I | 1,0 / 1,3 I | 1,2 I / 2,5 R8 | 1, binario | 32 × 2,4 × 3,6 I | 13 (21) |
| treno o carri in manovra | 4,2 I / 8,3 M | 0,3 / 0,5 I | 0,5 I / 1,5 F7 | 1, binario; spesso spinto, senza nessuno in testa | 100 × 2,9 × 4,3 I | 18 (24) |
| multirotore in volo lento | 3,0 R4 / 19,0 R4 | 2,0 I / 6,9 R4 | 2,0 I / 6,9 R4 | 3 più l'imbardata, olonomo in 3D | 0,35 × 0,28 × 0,11 M | 2,3 (3,2) |
| **non classificato** | inviluppo | inviluppo | inviluppo | olonomo: il caso peggiore | — | — |

«Non classificato» (etichetta assente, incerta, fuori tassonomia) prende **il massimo** delle classi ammesse nel sito (`classi_ammesse` nel profilo): mai un profilo più lento della regola di base.

Fonti aperte oggi: F1 [Preferred walking speed](https://en.wikipedia.org/wiki/Preferred_walking_speed) (1,10–1,65 m/s; 1,4 nelle guide britanniche); F2 [Bohannon 1997, PMID 9143432](https://europepmc.org/article/MED/9143432) (230 soggetti; comodo 1,27–1,46, massimo 1,75–2,53 m/s); F3 [Braking distance](https://en.wikipedia.org/wiki/Braking_distance) (1,5 s medi NHTSA, 2,5 s AASHTO, attrito 0,7 → 6,9 m/s²); F4 [Stopping sight distance](https://en.wikipedia.org/wiki/Stopping_sight_distance) (3,4 m/s², NCHRP 400); F6 [Taxiing](https://en.wikipedia.org/wiki/Taxiing) (16–19 nodi); F7 [Emergency brake (train)](https://en.wikipedia.org/wiki/Emergency_brake_(train)) (1,5 m/s²); F8 [A320 family](https://en.wikipedia.org/wiki/Airbus_A320_family) (37,6 m; letta in parte); F10 [Adaptalift](https://www.adaptalift.com.au/articles/2013-02-01-forklift-speed-limits-and-braking-in-the-warehouse); F11 [Bicycle performance](https://en.wikipedia.org/wiki/Bicycle_performance) (15,5 km/h a Copenaghen); F12 [Monopattino elettrico](https://it.wikipedia.org/wiki/Monopattino_elettrico) (20 km/h; strade urbane a 50 km/h; la legge non è aperta); F16 [regole dell'aeroporto di Monaco, PDF](https://www.munich-airport.de/_b/0000000000000008368639bb5e302e6f/traffic-safety-rules-2016.pdf) (30 km/h; passo d'uomo, al più 6 km/h, presso gli aerei parcheggiati: un solo aeroporto); F17 [scheda MiR250, PDF](https://www.hartfiel.com/wp-content/uploads/2024/04/MiR250-Specs.pdf) (2,0 m/s; 0,3 m/s²; 97 kg). Le fonti R (carrelli 5 e 10 mph; classi UE dei droni 19 m/s e 3 m/s in modalità lenta; traino a passo d'uomo; tram 2,5 m/s²) hanno il link in `classi.json`. Norme non lette: ISO 3691-4, ISO 13855, EN 13452, regolamento UE 2019/945 (la pagina non si è aperta). Wikipedia è una fonte di terza mano: per l'allegato servono le primarie (curatore).

## 2. Tabella dei profili di chi porta il sensore (configurazione iniziale deterministica)

| Profilo | v_ego (m/s) | T_r (s) | a_fr (m/s²) | Gradi di libertà | Arresto proprio v·(τ+T_r)+v²/2a (m) | Sensore in moto |
|---|---|---|---|---|---|---|
| stazione fissa (avviso a una persona vicina) | 0 | 1,0 I | — | 0 | 0 | no: **è il dominio provato** |
| veicolo terrestre lento, arresto automatico | 1,0 I (massimo 1,6 F9) | 0,3 I | 1,5 I | x, y, imbardata; a ruote differenziali: 2, non olonomo | 0,79 | sì |
| multirotore in volo stazionario | 0 | 0,3 I | 3,0 I (massimo 6,9 R4) | 4 | 0 | sì (oscilla) |
| multirotore in volo lento | 3,0 R4 | 0,3 I | 3,0 I | 4 | 2,86 | sì |
| persona non vedente che cammina col bastone | 1,0 I (F15, R10: più lenta dei vedenti, nessuna cifra letta) | 1,0 I | 1,0 I (arresto in uno o due passi R9) | 2 più l'imbardata, quasi olonomo | 1,66 | sì |
| persona non vedente ferma | 0 | 1,0 I | — | come sopra | 0 | quasi (il busto si muove) |
| operatore remoto di un veicolo lento | 1,0 I | 1,8 = 1,5 R6 + 0,3 di collegamento I | 1,5 I | come il veicolo | 2,29 | sì |

Tempi di reazione, che cosa ho letto: reazione **semplice** a un suono circa 0,16 s e a uno stimolo visivo circa 0,19 s in età universitaria (F5, [Mental chronometry](https://en.wikipedia.org/wiki/Mental_chronometry)); arresto del cammino a 1,3 m/s su un segnale luminoso con 0,375–0,825 s disponibili, peggio le anziane (F14, [Cao 1998, PMID 10200400](https://europepmc.org/article/MED/10200400): percentuali non lette); frenata di chi guida 0,70–0,75 s se attesa, 1,25 s inattesa, 1,5 s a sorpresa (R6, Green 2000: non verificato). Il robot: 1,6 m/s, 1,1 × 0,5 × 0,84 m, 32,5 kg (F9, [About Spot](https://dev.bostondynamics.com/docs/concepts/about_spot)). **Non ho trovato una misura del tempo di reazione di una persona non vedente a un avviso sonoro o tattile mentre cammina: T_r = 1,0 s è un'ipotesi di progetto**, la stessa del fascicolo di geometria; il campo ragionevole è 0,5–1,5 s. Il tempo semplice a uno stimolo tattile e il ritardo di un collegamento: non verificati.

## 3. Che cosa ne segue: distanza d'avviso e portata

d_avv = (v_classe + v_ego)·(τ + T_r) + v_ego²/(2·a_fr) + margine, con τ = 0,155 s (stimata, non misurata), margine = w = 0,40 m, avvicinamento frontale, la classe non frena. Comando: `…/f10-dati/ambiente/venv/bin/python -I -B conti.py CARTELLA`. Valori in metri, **a v_tip / a v_max**; in grassetto ciò che sta nei 3 m.

| Classe | stazione fissa o persona ferma | veicolo terrestre lento | multirotore lento | non vedente che cammina | operatore remoto |
|---|---|---|---|---|---|
| ostacolo fermo | **0,4** | **1,2** | 3,3 | **2,1** | **2,7** |
| persona a piedi | **2,0** / 3,3 | **1,8** / **2,3** | 3,9 / 4,4 | 3,7 / 4,9 | 5,4 / 7,6 |
| persona di corsa | 3,9 / 9,6 | **2,5** / 4,8 | 4,6 / 6,9 | 5,5 / 11,3 | 8,6 / 18,3 |
| bicicletta | 5,4 / 10,0 | 3,1 / 5,0 | 5,2 / 7,0 | 7,0 / 11,6 | 11,1 / 18,9 |
| monopattino | 5,2 / 6,9 | 3,1 / 3,7 | 5,2 / 5,8 | 6,9 / 8,5 | 10,9 / 13,6 |
| carrello elevatore | **2,9** / 5,6 | **2,2** / 3,2 | 4,3 / 5,3 | 4,6 / 7,2 | 7,0 / 11,5 |
| veicolo a guida automatica | **1,6** / **2,7** | **1,6** / **2,1** | 3,7 / 4,2 | 3,2 / 4,4 | 4,6 / 6,6 |
| auto, area di lavoro | 3,6 / 10,0 | **2,5** / 5,0 | 4,5 / 7,0 | 5,3 / 11,6 | 8,2 / 18,9 |
| auto, strada urbana | 10,0 / 16,4 | 5,0 / 7,5 | 7,0 / 9,6 | 11,6 / 18,1 | 18,9 / 29,9 |
| trattore di piazzale | **2,4** / 10,0 | **2,0** / 5,0 | 4,0 / 7,0 | 4,0 / 11,6 | 6,0 / 18,9 |
| aereo in rullaggio | 10,8 / 18,2 | 5,3 / 8,2 | 7,4 / 10,3 | 12,4 / 19,8 | 20,3 / 32,8 |
| aereo al traino | **2,0** / 5,2 | **1,8** / 3,1 | 3,9 / 5,2 | 3,7 / 6,9 | 5,4 / 10,9 |
| treno in banchina | 13,1 / 19,7 | 6,2 / 8,8 | 8,3 / 10,9 | 14,8 / 21,3 | 24,2 / 35,3 |
| tram a una fermata | 6,9 / 16,4 | 3,7 / 7,5 | 5,8 / 9,6 | 8,5 / 18,1 | 13,6 / 29,9 |
| treno in manovra | 5,2 / 10,0 | 3,1 / 5,0 | 5,2 / 7,0 | 6,9 / 11,6 | 10,9 / 18,9 |
| multirotore lento | 3,9 / 22,3 | **2,5** / 9,8 | 4,6 / 11,9 | 5,5 / 24,0 | 8,6 / 39,8 |

**Lettura.**
1. **Coperto dal dominio provato** (camera ferma, 3 m): il pedone a passo normale verso una stazione fissa o una persona ferma, 2,02 m; il limite è **2,25 m/s** = (3 − 0,40)/1,155. Già il passo svelto massimo (2,5 m/s, F2) chiede 3,29 m. Per conto rientrano a velocità tipica anche carrello (2,94 m: 6 cm di margine, e v_tip è R1), veicolo a guida automatica, trattore di piazzale a passo d'uomo, aereo al traino: **nessuno di questi è provato**, e a v_max escono tutti tranne il veicolo a guida automatica.
2. **Fuori portata** già a velocità tipica: 10 classi su 15. Un'auto a 8 m/s percorre 3 m in 0,37 s e chiede 9,6 m; auto urbana 10,0–16,4 m; treno in banchina 13,1–19,7 m; aereo in rullaggio 10,8–18,2 m. **Portata che servirebbe:** circa 5–6 m per carrello e traino, 10 m per le aree di lavoro e di piazzale a 30 km/h, 16–20 m per strada urbana, banchina e rullaggio, oltre 22 m per un multirotore non limitato. Una camera di profondità da 3 m non è il sensore di queste classi.
3. **Chi si muove paga il proprio arresto.** Il non vedente che cammina a 1,0 m/s usa 1,66 m per fermarsi: restano i 3 m solo per un ostacolo fermo (2,06 m) o per chi gli viene incontro a meno di **0,82 m/s**; un pedone normale chiede 3,67 m. L'operatore remoto (T_r 1,8 s) copre solo l'ostacolo fermo (2,69 m). Il multirotore a 3 m/s non copre nemmeno l'ostacolo fermo (3,26 m): servono v_ego ≤ 2,8 m/s. Il veicolo con arresto automatico è il profilo migliore (classi fino a 3,98 m/s), **ma tutti i profili in moto sono fuori dal dominio provato**: sono conti.
4. **Fascia di guardia per classe** (stesso conto della V3: v_max × 0,355 s): w = 0,40 m copre 1,13 m/s; servirebbero 0,89 m per la persona a 2,5 m/s, 1,60 m per il carrello, 2,95 m a 30 km/h, 4,9–5,9 m per auto urbana, tram, treno e aereo: più della portata. Per le classi veloci l'insieme di possibile presenza riempie tutto il campo: l'indicazione onesta è «non verificato», non una regione.
5. **Gradi di libertà.** Servono a dare forma alla regione **prevista** (R90): corridoio per i non olonomi (un'auto a 2,8 m/s con raggio 5,5 m in 1 s scarta di lato al più r·(1 − cos(v·t/r)) = 0,70 m, contro 2,8 m del disco), striscia lungo il binario per treno e tram, sfera per il multirotore. **Non devono mai restringere l'avviso (R100)**: un pedone etichettato «treno» si muoverebbe fuori dalla striscia.
6. **Etichetta sbagliata** (stazione fissa, v_max): auto detta «persona» → avviso a 3,29 m invece di 9,99 m, **6,70 m in meno**; carrello detto «veicolo a guida automatica» → 2,89 m in meno. L'inviluppo protegge dall'etichetta *incerta*, non da quella *sicura e sbagliata*.

## 4. Massa

Massa e accelerazione non sono stimabili dalle misure (già stabilito): con le classi entrano come **intervalli a priori della classe**, non come stime. Ordini di grandezza con fonte: robot d'ispezione 32,5 kg (F9); veicolo a guida automatica 97 kg a vuoto, 347 kg a pieno carico (F17); trattore per grandi aerei fino a 54 t (F13, [Pushback](https://en.wikipedia.org/wiki/Pushback_(aviation))); famiglia A320 68–93,5 t al decollo (F8); multirotore 0,9 kg (R4, non verificato). Per persona, bicicletta, carrello, auto, treno e tram non ho aperto una fonte: `massa_kg` è `null`.

## 5. Schema dei file

`classi.json`: `schema` (campi e unità), `fonti` (codice → cosa, link, stato), `classi[]` con `id, nome, contesto, v_tip, v_max` (m/s), `a_tip, a_max, dec_tip, dec_max` (m/s²), `T_r_classe` (s), `gdl`, `olonomo` (true, false, «quasi»), `modello_moto`, `raggio_min` (m), `ingombro` [l, l, h] (m), `massa_kg` [min, max] o null, `fonti` (campo → codice). `profili_portatore.json`: `parametri_comuni` (τ, margine, portata, età del dato, tenuta), `profili[]` con `id, v_ego, v_ego_max` (m/s), `T_r, T_collegamento` (s), `a_fr, a_fr_max, a_max` (m/s²), `gdl, olonomo, canale_avviso, sensore_in_moto, classi_ammesse[]`, `fonti`. Sette profili d'esempio. Il programma li legge e ricalcola tutto: cambiando un valore cambia la tabella.

## 6. Stati proposti, proposte, e dopo

**Stati.** «I 3 m bastano per le classi veloci»: **smentito** per conto (10 classi su 15 già a v_tip). «Il pedone a passo normale verso un sensore fermo è nel dominio»: **sostenuto da un conto** (τ stimata, T_r ipotesi), non dai dati. Le due tabelle: **ipotesi con fonti parziali** (9 velocità su 30 con fonte aperta). T_r della persona non vedente: **non risolto** (lo decide una prova con persone, o un articolo che la misuri). Previsioni: E1–E5 reggono, E6 ed E7 smentite. Indipendenza: tabelle, programma e previsioni hanno lo stesso autore e lo stesso modello; le fonti non sono state rilette dal curatore.

**Proposte.**
- `esperto-dominio-1`, regola del massimo. La velocità usata per fascia, insieme di possibile presenza e d_avv è max(base della V3, v_max dell'etichetta); senza etichetta o con fiducia bassa: inviluppo di `classi_ammesse`. Previsione: nessuna etichetta, giusta o sbagliata, riduce l'avviso sotto quello della V3 senza etichette. Smentita: un solo fotogramma in simulazione, con etichette sbagliate iniettate, in cui l'avviso è più piccolo.
- `esperto-dominio-2`, controllo all'avvio. Dalla configurazione il sistema calcola d_avv dell'inviluppo; se supera la portata dichiara a schermo, una volta, «classe X: oltre la portata, avviso non tempestivo». Previsione: con stazione fissa e sola persona a piedi dichiara il limite a 2,25 m/s. Smentita: un profilo con d_avv > 3 m che parte senza la dichiarazione.
- `esperto-dominio-3`, i gradi di libertà agiscono solo su R90, mai su R100 né sul «libero». Smentita: una cella che passa a «libero» o esce dall'avviso per effetto del modello di moto di una classe.

**Dopo.** Curatore: aprire le primarie (ISO 3691-4, ISO 13855:2024, regolamento UE 2019/945, Green 2000, Clark-Carter 1986, un manuale di carrello, un regolamento di manovra ferroviaria). Simulatore: iniettare etichette sbagliate per `esperto-dominio-1`. Arbitro: sciogliere il conflitto sulle parole (§0). Da dire alla giuria: «le classi veloci sono configurate e dichiarate fuori portata; il prototipo è provato in simulazione per il pedone a passo normale e sensore fermo». Da non dire: «copre veicoli, treni, aerei»; «avviso tempestivo» per una classe oltre 2,25 m/s.
