Canarino: sciame-canarino-ff229a474629e844

# Consegna f1 — sciame-ricercatore, corsia A (stato dell'arte, 14 novembre 2026)

Le fonti sono in `FONTI.md` (F1–F30), con tre marche: **A** aperta davvero, **R** vista solo nel riassunto della
ricerca, **M** solo memoria. Qui ogni numero porta la sua sigla. Le previsioni e gli esiti sono in `PREVISIONI.md`.

## 0. Cambi di stato e regole violate
- **P1 non risolta, P2 regge, P3 regge** (dettaglio in §3). La mia attesa «il ToF cede al sole» è contraddetta da
  una fonte del costruttore (F3): l'ho declassata da fatto a disaccordo.
- Regola 3: le previsioni sono state scritte dopo aver visto quattro riassunti di ricerca (dichiarati in testa a
  PREVISIONI.md), prima delle prove che le decidono.
- Regola 5: il testo estratto dal PDF di F14 è finito nella cartella temporanea della sessione, fuori dalla mia
  cartella di consegna; dal materiale scaricato non ho eseguito niente.
- Metà circa delle fonti è marcata R (non aperta): vale come pista, non come prova, finché il curatore non la apre.

## 1. Diagnosi, con le prove
1. **Tre ToF non danno 360°.** La camera ToF più larga che ho aperto ha 120° x 120°, portata 0,25–2,88 m in quella
   modalità, ambiente dichiarato «Indoor» (F1, A); i ToF multizona economici hanno 60° x 60° e 3,5 m (F2, R). Tre
   da 120° coprono 360° senza sovrapposizione, quindi senza modo di calibrarli fra loro, e più ToF insieme
   interferiscono (F3, A). La bozza stessa propone una sola camera RGB-D (righe 2091–2118).
2. **Sole: le fonti non sono d'accordo.** Luxonis dichiara per il suo ToF «<2% outdoors» e 5 m (F3, A, costruttore);
   Orbbec dichiara «Indoor» (F1, A); una rassegna e una prova sul campo parlano di limiti seri al sole per ToF e
   stereo attivo (F5 e F4, R). Non esiste, fra ciò che ho trovato, un confronto controllato in esterno.
3. **La massa non è osservabile.** Un metodo del 2026 che dichiara di superare i precedenti ha un errore
   percentuale medio di 0,665 (66,5%) e un fattore medio 1,68 su oggetti da catalogo; il riferimento del 2017 ha
   1,066; su un secondo insieme entrambi stanno a 0,98 (F29, A). Nessun lavoro trovato stima la massa di persone o carrelli in scena.
4. **Per prevedere dietro un'occlusione il modello semplice regge.** Sui pedoni di ETH/UCY, a 4,8 s, la velocità
   costante dà errore medio/finale 0,39/0,83 m contro 0,44/0,91 del miglior modello appreso deterministico
   confrontato e 0,32/0,60 di un generativo a 20 campioni (F14, A). Limiti: camere fisse dall'alto, lavoro del
   2020, nessun dato da camera indossata; i modelli più recenti non li ho controllati. Conseguenza pratica:
   l'errore cresce con il tempo (0,83 m in media a 4,8 s), quindi la previsione deve **scadere**. I
   tracciatori classici con Kalman costano poco (oltre 700 FPS su CPU date le rilevazioni: F16, R) e hanno licenza
   MIT (F15, A); il difetto noto è l'errore che si accumula durante l'occlusione (F16, R).
5. **I modelli video con memoria sono promettenti, non provati su hardware modesto.** EdgeTAM: 16 FPS su iPhone 15
   Pro Max, 150,9 su A100, Apache 2.0 (F18, A); SAM 2 piccolo circa 1 FPS sullo stesso telefono (F18, R); il codice
   di SAMURAI non accetta flussi dal vivo (F19, A). Nessuna misura trovata su Jetson o CPU: non verificato.
   Seguono un oggetto indicato, non danno stato 3D né incertezza. La percezione amodale è acerba: «struggle... under
   heavy occlusion», guadagni di 2–3 punti con la messa a punto (F20, A).
6. **Calibrazione: si può fare in poche ore, a posteriori.** Per i rilevatori, Platt e regressione isotonica battono
   i metodi d'addestramento recenti (oltre 7 punti di D-ECE su COCO: F22, A); servono dati propri messi da parte
   (F23, R). Si misura con il diagramma di affidabilità e il D-ECE; per il filtro, con la quota di riapparizioni
   dentro la regione dichiarata (le prove NEES/NIS sono lo standard: M, non verificato oggi).
7. **Feedback: prove scarse e miste.** Quattro motori e pochi motivi direzionali si riconoscono al 93,75% (14
   utenti con disabilità visiva: F6, A); chi usa il bastone non vuole sostituirlo (F6, R). Sonoro contro aptico:
   uno studio dà al sonoro un carico 22 volte maggiore (F7, R, non aperta), un altro trova l'aptico meno intuitivo
   (F8, R). Solo il 22,9% delle valutazioni usa persone con disabilità visiva (F9, R). **Lacuna:** non ho trovato
   studi sulla tolleranza ai falsi allarmi né su un segnale esplicito di «affidabilità persa» (R6).
8. **Industria e aerospazio.** La sorveglianza di velocità e separazione mette già incertezza di misura e latenza
   nella distanza protettiva (F26, R) e usa tre stati per i voxel (F27, R, brevetto). Negli hangar manca evidenza
   sulla robustezza all'occlusione dinamica e manca un confronto fra soluzioni (F25, A). Una camera **fissa**
   toglie il moto proprio, che nell'indossabile è il rischio tecnico maggiore: è un'inferenza mia, non misurata.

## 2. Proposte
**ricercatore-1 — Geometria prima, un solo sensore frontale, niente massa.**
- *Enunciato:* una camera RGB-D frontale con IMU al posto di tre ToF; ostacoli dalla profondità (R2) in una
  griglia a tre stati libero/occupato/sconosciuto (R8); elementi mobili da un rilevatore leggero più associazione
  di tipo ByteTrack/OC-SORT (R1, R7). Fianchi e spalle escono come «sconosciuto», mai come liberi. La massa si
  toglie: restano ingombro misurato e classe, con il peso tipico della classe dichiarato come ipotesi a priori.
- *Guadagno atteso:* un sensore da calibrare invece di tre; percorso critico su CPU; nessuna grandezza non
  osservabile in uscita. *Vincoli:* campo frontale; comportamento al sole non risolto; licenza del rilevatore da
  controllare (YOLO di Ultralytics è AGPL: M, non verificato oggi; YOLOX è Apache 2.0: F16, R).
- *Chi la prova:* sensori, fusione, avversario. *Falsificatore (5 minuti):* P1, schede tecniche: un ToF con campo
  orizzontale di almeno 130° e almeno 4 m al sole. *Esito:* non risolta (campo: nessuno trovato; sole: disaccordo).
- *Se l'ipotesi di fattibilità è falsa:* senza camera di profondità, demo a camera fissa (§1.8); con più tempo, ToF
  multizona laterali come canale di sola prossimità, separato dalla mappa.

**ricercatore-2 — Occlusione: Kalman a velocità costante con previsione a scadenza; modelli appresi fuori dal
percorso critico.**
- *Enunciato:* ogni traccia ha tre stati in uscita. «Osservato» finché c'è la misura; «previsto» durante
  l'occlusione, con la regione d'incertezza che cresce; «sconosciuto» quando la regione supera una soglia o dopo un
  tempo massimo, e allora parte il segnale R6. I modelli tipo SAM 2 o i trasformatori di visione lavorano solo in
  modo asincrono (classe, riaggancio) e non decidono mai un allarme. Le confidenze si calibrano a posteriori su
  una registrazione propria.
- *Guadagno atteso:* R3, R4 e R6 con una verifica mostrabile: quota di riapparizioni dentro la regione dichiarata
  e tempo fino al segnale di «sconosciuto». La soglia e il tempo massimo NON li fisso: vanno misurati.
- *Vincoli:* la prova F14 viene da camere fisse; con la camera indossata si somma l'errore del moto proprio; una
  svolta dietro l'ostacolo non è prevedibile da nessun modello confrontato.
- *Chi la prova:* kalman, tracciamento, validazione, avversario. *Falsificatore (5 minuti):* P2, Tabella I di F14 e
  velocità dichiarate dei modelli video. *Esito:* regge (a); regge (b) solo come assenza di prova contraria.

## 3. Stati proposti
| Enunciato | Stato | Prova |
|---|---|---|
| Tre ToF coprono 360° con sovrapposizione | Smentito sui sensori aperti (non esaustivo) | F1, F2 |
| Il ToF non regge il sole | Non risolto: fonti discordi; decide una prova al sole | F1, F3, F5 |
| La massa si stima dalla visione con affidabilità utile | Smentito dai dati disponibili | F29 |
| Velocità costante adeguata per occlusioni brevi di pedoni | Sostenuto dai dati (camere fisse) | F14 |
| Modelli video con memoria in tempo reale su hardware modesto | Non risolto: manca la misura | F18, F19 |
| Aptico meglio del sonoro per l'allerta | Non risolto: studi discordi e non aperti | F6, F7, F8 |

## 4. Che cosa propongo dopo
1. Curatore delle fonti: aprire le fonti R, per prime F7, F16, F26. 2. Sensori: cinque minuti al sole con il
sensore vero. 3. Kalman: simulazione numerica per la scadenza della previsione, con e senza errore di moto
proprio. 4. Decidere fra indossabile e camera fissa con il criterio R3: quale demo mostra meglio l'occlusione.
5. Interfacce: una prova con utenti del segnale R6, perché lì la letteratura è vuota.
