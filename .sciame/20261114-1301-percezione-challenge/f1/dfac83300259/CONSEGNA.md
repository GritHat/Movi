Canarino: sciame-canarino-ff229a474629e844

# Consegna di sciame-nuvole-punti — f1, corsia A (conservativa)

## 0. Cambi di stato e regole violate

- Cambi di stato: tre previsioni scritte prima (`PREVISIONI.md`, 13:05:43) e provate dopo (13:07:26): reggono tutte.
- Scritture fuori cartella: una, non voluta. Lo strumento di lettura web ha salvato da solo il PDF della scheda ST in
  `~/.claude/projects/…/tool-results/`; l'ho letto con `pdftotext`, senza eseguire niente.
- File in più nella mia cartella: `prova_np.py` (le prove, ripetibili con `python3 -I prova_np.py`) e `stato.md`.
- Le fonti segnate «(ricerca)» le ho controllate nel riassunto del motore di ricerca, senza aprire la pagina.

## 1. Diagnosi, con le prove

1. **«3 ToF = 360°» dipende da quale ToF, e con i più comuni è falso.** Un ToF multizona 8×8 (VL53L5CX: 45°×45°, 63°
   in diagonale, 400 cm, [scheda ST, tabella 2](https://cdn.sparkfun.com/assets/6/e/3/0/6/vl53l5cx-datasheet.pdf),
   letta) dà 135° con tre unità. A 1,2 m da terra una zona copre sul suolo 0,20 m a 1 m e 0,87 m a 3 m: un gradino
   da 15 cm non si separa. Un pedone a 4 m prende 5,4 zone (prova P-np2). Tre camere ToF 240×180
   ([Arducam](https://www.arducam.com/product/time-of-flight-camera-for-raspberry-pi/), ricerca; campo non
   verificato) risolvono il terreno ma coprono circa 174°. Solo tre camere a campo 120°×120°
   ([Femto Bolt](https://www.orbbec.com/products/femto-bolt/), ricerca: 0,25–2,21 m, 15 fps, 418–559 $ l'una)
   chiudono i 360°: fuori dal bilancio ipotizzato. L'interferenza fra più ToF vicini: non verificato.
2. **La regola log-odds della bozza (§4.5, righe 2208–2225), così com'è scritta, dichiara libero ciò che non vede
   più.** In simulazione (pedone che passa dietro un occlusore, 15 Hz) la cella occupata dal pedone esce «libero»
   in 173 casi su 552 mentre è in ombra, e in altri 92 mentre è visibile, per il ritardo dell'accumulo (P-np1a;
   il secondo numero l'ho notato dopo). La bozza ha gli agganci giusti (`lastUpdate`, `flags`, «sconosciuto non è
   libero», riga 2186) ma non la regola che riporta una cella da «libero» a «non osservato». Inoltre L = 0 confonde
   «mai vista» e «vista con prove opposte».
3. **«Libero» deve voler dire suolo visto alla quota attesa, non assenza di ostacoli.** Una buca, una scala in
   discesa, il vetro o una superficie che assorbe non danno ritorni: in una griglia di soli ostacoli diventano
   «libero». Ragionamento geometrico; su dati veri: non verificato. Vetro e specchi vanno all'esperto di sensori.
4. **La griglia 20×20 m fissa nel mondo con ring buffer chiede un'odometria affidabile** (riga 2206), che è il pezzo
   più fragile in 24–48 ore, e arriva a 10 m dall'utente, oltre tre volte la portata utile (D435: ideale 0,3–3 m, 87°×58°,
   [Intel](https://www.intelrealsense.com/compare-depth-cameras), ricerca). Lo strato «osservato ora» non ne ha
   bisogno.
5. **Ai bordi il raggruppamento sbaglia in modo sistematico.** Un oggetto tagliato dall'ombra o dal campo ha il
   baricentro spostato verso la parte visibile (fino a 0,25 m per un pedone): la misura va marcata «tagliata» e
   pesata meno nel filtro. I punti misti sulle discontinuità di profondità vanno scartati col gradiente.
6. **Alternative scartate, col motivo.** Griglia dinamica con velocità per cella
   ([Nuss e altri, 2018](https://arxiv.org/abs/1605.02406), ricerca): filtro a particelle in parallelo, troppo per un
   hackathon. Voxel e octree ([OctoMap](https://www.hrl.uni-bonn.de/papers/hornung13auro-preprint.pdf), ricerca):
   distinguono libero, occupato e ignoto, ma con raggi in 3D e ipotesi di mondo statico. Solo tracce senza mappa:
   non rappresentano il libero né l'ignoto, quindi R4 e R8 cadono per ostacoli fermi e terreno. Griglie evidenziali
   ([Moras e altri, 2011](https://hal.archives-ouvertes.fr/hal-00615303), ricerca): l'idea giusta (l'ignoranza ha
   una sua massa); la proposta 1 ne è la versione discreta.
7. **Massa e accelerazione** non escono dalla geometria: la massa non è osservabile con la profondità;
   l'accelerazione la valuti l'esperto di Kalman.

## 2. Stati proposti

| Enunciato | Stato | Prova e modello |
|---|---|---|
| La log-odds della bozza basta a R8 | **Smentito** | controesempio P-np1a, simulazione 2D senza rumore |
| Tre ToF multizona 8×8 danno 360° e la mappa del terreno | **Smentito** | P-np2 sui dati della scheda ST |
| Tre ToF qualsiasi danno 360° | **Non risolto** | lo decide il modello di sensore che la squadra ha davvero |
| La griglia a quattro stati sta nel periodo di 15 Hz | **Sostenuto dai dati** | 2,0 ms, Python puro, un core Ryzen, scena sintetica; su Raspberry Pi non verificato |
| La proposta 1 dà zero «libero» falsi su dati veri | **Non risolto** | serve una registrazione con verità a mano |

## 3. Proposte

### nuvole-punti-1 — Griglia polare egocentrica a quattro stati; l'ombra governa le tracce

- **Enunciato.** A ogni fotogramma, dall'immagine di profondità, ogni cella (settore di 1°, 0,1 m, fino alla portata
  utile) riceve uno stato: *libero osservato* (suolo visto alla quota attesa, nessun ostacolo), *occupato osservato*
  (primo ritorno del settore fra 0,07 e 2 m di quota), *in ombra* (oltre il primo ritorno), *non osservato* (fuori
  campo, nessun ritorno, suolo mancante). La memoria è l'ultimo stato visto con la sua età: «libero» scade dopo
  τ = margine / velocità massima (0,7 m / 1,4 m/s = 0,5 s); «occupato» resta come *ricordato* finché non è smentito.
  Una traccia la cui posizione prevista cade in ombra o fuori campo è *prevista* (l'assenza di misura è attesa, la
  covarianza cresce, oltre soglia diventa *persa* e si segnala: R6); se cade in *libero osservato* per tre
  fotogrammi è smentita e si chiude. La log-odds resta, facoltativa, come filtro del rumore sullo strato occupato.
- **Guadagno atteso.** R4 e R8 per costruzione (0 «libero» falsi contro 265 su 552 in simulazione); R3 legato alla
  geometria dell'occlusione e non a un timeout; niente odometria per lo strato di sicurezza; 2 ms a fotogramma.
- **Vincoli.** Servono la direzione della gravità (IMU) e l'altezza del sensore. Su rampe e pendenze la «quota
  attesa» chiede un piano locale: senza, il suolo in salita diventa ostacolo (errore dal lato sicuro, ma fastidioso).
  Con la testa che ruota la memoria va compensata col giroscopio, altrimenti scade (lato sicuro). Soglia di 7 cm
  affidabile fino a circa 3 m con stereo (errore calcolato 18 mm a 2 m, 72 mm a 4 m; ipotesi 0,1 px e base 50 mm:
  non verificato sul dispositivo).
- **Chi la può provare.** Avversario (vetro, rampa, oggetto che esce dall'ombra dal lato opposto), esperto di
  validazione (registrazione vera), esperto di tracciamento (le tre regole traccia–cella), tempo reale.
- **Falsificatore più economico.** Fatto: P-np1a e P-np1b, reggono. Il prossimo, cinque minuti su una registrazione
  di profondità di una persona che passa dietro una colonna: previsione 0 fotogrammi con la cella nascosta
  «libero»; smentita con 1 o più.

### nuvole-punti-2 — Una camera di profondità densa frontale al posto dei tre ToF; il 360° non si promette

- **Enunciato.** Il sensore del prototipo è una sola camera di profondità densa (almeno 240×180; meglio RGB-D
  stereo 640×480 della classe D435) inclinata verso il basso, con IMU. Tutto ciò che è fuori dal suo campo esce
  come «non osservato». Se la demo vuole i 360°, li aggiunge un LiDAR 2D
  ([LD19](https://www.waveshare.com/dtof-lidar-ld19.htm), ricerca: 0,8°, 5–13 Hz, 12 m): vede gli elementi mobili su
  un piano (8,9 fasci su un pedone a 4 m), non il terreno.
- **Guadagno atteso.** Terreno risolto fino a 3 m (impronta 1,8 cm contro 87 cm), 7 756 pixel sul pedone a 4 m
  contro 5,4 zone; un solo dispositivo USB da integrare.
- **Vincoli.** Campo di 87°: i lati e il retro sono dichiarati ignoti. Lo stereo soffre su pareti uniformi e al sole
  (non verificato qui: all'esperto di sensori). Se la squadra ha già tre *camere* ToF, una va in avanti per il
  terreno e due ai lati per i soli ostacoli. Se l'ipotesi sull'hackathon è falsa e manca l'hardware di profondità,
  la stessa griglia si dimostra su registrazioni RGB-D (non verificato).
- **Chi la può provare.** Esperto di sensori, esperto hardware di LiDAR, esperto di fusione (se si aggiunge il LiDAR).
- **Falsificatore più economico.** Fatto: P-np2, regge. Sull'hardware, cinque minuti: un gradino da 15 cm a 2 m;
  previsione: due mode nell'istogramma delle quote, distanti più di tre deviazioni standard; smentita se non si
  separano.

## 4. Che cosa propongo dopo

1. Chiedere all'utente quale sensore ToF la squadra possiede o intende comprare: decide la riga «non risolto».
2. Dare la proposta 1 all'avversario e all'esperto di tracciamento per le regole traccia–cella.
3. Raggruppamento: componenti connesse sulle celle occupate (stesso principio di
   [Bogoslavskyi e Stachniss, 2016](https://github.com/PRBonn/depth_clustering), ricerca, nato per LiDAR rotanti:
   trasferimento alle camere di profondità non verificato).
