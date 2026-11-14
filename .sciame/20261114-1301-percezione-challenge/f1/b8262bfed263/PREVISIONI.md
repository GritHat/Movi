# PREVISIONI — sciame-requisiti, f1, corsia A

Scritte PRIMA delle prove. Ora di registrazione: 2026-11-14T13:10:16+01:00

## P1 (per requisiti-1: il taglio dell'ambito esclude i 360° con 3 ToF)

- **Enunciato messo alla prova:** «3 sensori ToF coprono 360° di visione» (idea di partenza, punto a).
- **Misura:** campo visivo orizzontale (HFOV) dichiarato nella scheda tecnica o pagina del produttore di sensori di
  profondità reperibili per un hackathon: ST VL53L5CX, ST VL53L7CX, ST VL53L8CX, Arducam ToF camera, Orbbec Femto Bolt
  (NFOV e WFOV), Intel RealSense D435/D455 (stereo, come confronto). Soglia geometrica: 360°/3 = 120° per sensore
  senza sovrapposizione; 130° con 10° di sovrapposizione per fianco.
- **Previsione (dalla memoria, non verificata al momento della scrittura):** nessuno dei sensori che riesco a
  controllare ha HFOV >= 130°; al più uno (Femto Bolt in WFOV) arriva a 120° esatti. Quindi 3 sensori lasciano buchi
  angolari o zero sovrapposizione.
- **Soglia di smentita:** l'enunciato della squadra REGGE (e la mia esclusione è smentita) se almeno 2 dei sensori
  controllati hanno HFOV >= 130°. Se riesco a controllare meno di 3 schede: NON RISOLTA.
- **Indipendenza:** l'oracolo sono le schede dei produttori (indipendenti da me e dalla bozza); condivide con la
  previsione solo l'elenco dei sensori, scelto da me (difetto possibile: un sensore grandangolare che non conosco).

## P2 (per requisiti-2: la demo con occlusione breve mostra R3, R4 e R6 nello stesso passaggio)

- **Enunciato messo alla prova:** «con un modello a velocità quasi costante (quello della bozza, righe 2292–2306) la
  previsione di un pedone nascosto resta utile per un tempo T dell'ordine di 1–2 s, poi l'incertezza impone di
  dichiarare la perdita di affidabilità»: cioè in una demo di pochi minuti si vedono tutti e tre gli stati
  (osservato, previsto, sconosciuto).
- **Misura:** T = tempo dall'inizio dell'occlusione al quale 2·sigma della posizione prevista supera 1,0 m (mezza
  larghezza di un corridoio), calcolato in forma chiusa e ricontrollato con una simulazione Monte Carlo (CPU, < 1
  min). Parametri (IPOTESI mie, non verificate su fonti): densità spettrale dell'accelerazione q in {0,25; 0,5; 1,0}
  m^2/s^3; sigma iniziali 0,05 m in posizione e 0,2 m/s in velocità.
- **Previsione:** T fra 0,8 e 2,0 s per tutti e tre i valori di q.
- **Soglia di smentita:** smentita se per almeno un q risulta T < 0,5 s (la previsione non copre nemmeno un pannello
  di 60 cm: R3 non mostrabile) oppure T > 5 s (la perdita di affidabilità non scatta mai in una demo breve: R6 non
  mostrabile con la sola crescita della covarianza). Forma chiusa e Monte Carlo devono concordare entro il 10 %.
- **Indipendenza:** forma chiusa e simulazione condividono il modello del moto e i parametri (stesso autore, stesso
  modello): il controllo vale per gli errori di algebra, NON per l'aderenza del modello a un pedone vero.

## Non conta come previsione

La tracciabilità «nessuna frase delle regole chiede 360°, massa, accelerazione, classificazione, terreno» l'ho vista
leggendo le regole (6 righe) prima di scrivere questo file: è un controllo esaustivo su un insieme dichiarato, non
una previsione.

## Esiti

Registrati alle 2026-11-14T13:14:37+01:00, dopo le prove.

- **P1: REGGE** (la previsione; l'enunciato della squadra «3 ToF = 360°» è smentito sui sensori controllati).
  HFOV letti: VL53L5CX 45° (65° diagonale), VL53L8CX 45° (65° diagonale), VL53L7CX 60° (90° diagonale), Arducam ToF
  70° diagonale (modello 240x180) e 64° orizzontale (modello T2), Orbbec Femto Bolt 75° (NFOV) e 120° (WFOV),
  RealSense D435/D455 87°. Sensori controllati: 7; con HFOV >= 130°: 0; con HFOV = 120°: 1 (Femto Bolt WFOV, portata
  al più 2,88 m nel modo a celle accorpate; 15 fotogrammi al secondo alla risoluzione piena 1024x1024). Provenienza: Orbbec letta direttamente
  (https://www.orbbec.com/products/tof-camera/femto-bolt/); ST, RealSense e Arducam dal riassunto del motore di
  ricerca, perché st.com è andato in timeout e intelrealsense.com non si è risolto: fonte secondaria.
- **P2: REGGE.** T (2 sigma > 1,0 m): q=0,25 -> 1,30 s (Monte Carlo 1,30 s); q=0,5 -> 1,07 s (1,08 s); q=1,0 -> 0,87 s
  (0,88 s). Tutti dentro 0,8-2,0 s; scarto massimo fra forma chiusa e Monte Carlo 1,1 %. Sigma a 2 s: 0,91 / 1,22 /
  1,68 m; a 3 s: 1,62 / 2,21 / 3,06 m.
  Deviazione dall'esecuzione prevista: primo lancio fallito per `numpy` assente; rifatto in Python puro con 4000
  campioni e passo 0,02 s. Modello, parametri, misura e soglie invariati.

## Notato dopo (non era scritto prima)

- Il valore q=1,0 dà T=0,87 s, vicino al bordo inferiore della previsione (0,8 s): con un q più alto la previsione
  sarebbe caduta. I valori di q restano ipotesi mie, non verificate su dati di pedoni.
- Tre Femto Bolt in WFOV darebbero 360° esatti senza sovrapposizione: è il solo caso limite, e l'interferenza fra tre
  ToF affiancati non è verificata.
