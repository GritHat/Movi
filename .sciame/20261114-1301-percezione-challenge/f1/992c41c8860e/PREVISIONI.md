# Previsioni di sciame-tracciamento (f1, corsia A)

Scritte PRIMA di eseguire qualsiasi simulazione. Ora di scrittura: 2026-11-14T13:05:30+01:00

Oracolo: simulazione numerica su CPU (numpy), scritta da me. Indipendenza dichiarata: la simulazione condivide con le
proposte l'autore e il modello (me); NON condivide il modello di moto, perché la verità simulata manovra (soste e
svolte casuali) mentre il filtro assume velocità costante. Non condivide niente con sensori reali: vale solo per i
difetti di logica e di calibrazione, non per quelli del rilevatore o del sensore.

## tracciamento-1 — «volo cieco» con Kalman a velocità costante e Q gonfiato; orizzonte onesto dichiarato

Impianto: pedone 2D, velocità ~N(1,3; 0,3) m/s, soste con tasso 0,1/s, svolte (fino a ±90°) con tasso 0,2/s; misure a
10 Hz con sigma 0,05 m; 3 s visibile, poi occlusione T in {0,5; 1; 2; 3; 5} s; filtro CV con densità spettrale q.

- P1a. Con q = 0,5 m²/s³ l'errore radiale RMS alla ricomparsa è <= 0,5 m a T = 1 s e >= 1,2 m a T = 3 s.
  Smentita: fuori da queste soglie.
- P1b. Con q = 0,5 la porta al 99% (chi-quadro, 2 gradi di libertà) contiene la ricomparsa in >= 95% dei casi per
  ogni T <= 3 s. Con q = 0,05 (taratura «liscia» tipica) la copertura scende sotto l'80% per T >= 2 s.
  Smentita della proposta: copertura < 90% a qualche T <= 3 s con q = 0,5 (allora CV+Q gonfiato non basta e serve
  altro: IMM o crescita tarata sui dati).
- P1c. L'orizzonte onesto (il T a cui il raggio al 95% dell'errore VERO supera 1,5 m) sta fra 1,5 s e 3 s.
  Smentita: fuori dall'intervallo.

## tracciamento-2 — chiusura delle tracce guidata dalla causa della non-osservazione, non da un tempo fisso

Impianto: 1D laterale a 4 m dal sensore, campo visibile y in [-3,5; 3,5] m, ombra dell'occlusore y in [-1; 1] m,
pedone a 1,3 m/s, 10 Hz, pD = 0,95. Scenari: (i) attraversa l'ombra (occlusione circa 1,5 s); (ii) si ferma
nell'ombra per U(2; 4) s e poi riparte; (iii) sparisce nell'ombra e non riappare.
Politiche: F1 = scadenza fissa 1 s; F5 = scadenza fissa 5 s; OA-media = la traccia sopravvive finché la MEDIA
prevista è in ombra o fuori campo, e muore dopo 0,3 s di media in zona visibile vuota; OA-particelle = filtro di
Bernoulli a particelle, l'evidenza negativa toglie massa solo dove il sensore vede.
Misura: «tenuta» = traccia ancora viva alla ricomparsa (identità conservata).

- P2a. F1: tenuta <= 5% nello scenario (i).
- P2b. OA-media: tenuta >= 95% in (i) ma <= 50% in (ii) (la media esce dall'ombra mentre il pedone è fermo dentro:
  uccisione falsa di un oggetto nascosto, il caso pericoloso per R8).
- P2c. OA-particelle: tenuta >= 90% in (i) e >= 80% in (ii); in (iii) la media mostrata resta in zona visibile per
  meno di 0,5 s in media (niente fantasma dove il sensore vede vuoto).
- Smentita della proposta nella forma a particelle: tenuta OA-particelle < 80% in (ii), oppure OA-media > 80% in (ii)
  (allora la forma semplice basta e le particelle non sono giustificate).

## Esiti

Compilati alle 2026-11-14T13:09:03+01:00, dopo le prove. Comandi: `python3 -I prove/simA.py`, `prove/simA2.py`, `prove/simB.py`,
`prove/simB2.py` (Python puro, semi fissi, meno di 30 s in tutto; eseguite fra le 13:06:46 e le 13:07:52).

| Previsione | Esito | Misura |
|---|---|---|
| P1a (RMS <= 0,5 m a 1 s) | **smentita** di poco | 0,53 m (due esecuzioni, N = 3000 e 6000) |
| P1a (RMS >= 1,2 m a 3 s) | regge | 1,95 m |
| P1b (q = 0,5: copertura >= 95% fino a 3 s) | regge | 98,6% / 98,8% / 99,5% / 99,9% a 0,5 / 1 / 2 / 3 s |
| P1b (q = 0,05: copertura < 80% per T >= 2 s) | **smentita** sulla soglia | 82,4% / 79,4% / 81,5% a 2 / 3 / 5 s; il verso regge (nominale 99%, d2 medio circa 5 contro 2 atteso) |
| P1c (orizzonte onesto fra 1,5 e 3 s) | **smentita** | il raggio vero al 95% supera 1,5 m già a circa 1,2 s (1,21 m a 1,0 s; 1,53 m a 1,2 s; 1,88 m a 1,5 s) |
| P2a (F1 tenuta <= 5% in i) | regge | 0% |
| P2b (OA-media >= 95% in i) | **smentita** | 91% |
| P2b (OA-media <= 50% in ii) | regge | 0% |
| P2c (OA-particelle >= 90% in i, >= 80% in ii, fantasma < 0,5 s) | regge | 100%, 100%, 0,06-0,07 s |
| Smentita di tracciamento-1 (copertura < 90% con q = 0,5) | non avvenuta | minimo 98,6% |
| Smentita di tracciamento-2 (OA-particelle < 80% o OA-media > 80% in ii) | non avvenuta | 100% e 0% |

Riferimento non previsto ma misurato: F5 (scadenza fissa 5 s) tiene 100% in (i), 75-77% in (ii), e in (iii) lascia un
fantasma in zona visibile per 2,03 s in media.

## Notato DOPO (non era previsto, vale come osservazione)

- Con q = 0,5 la sigma dichiarata cresce più in fretta dell'errore vero (d2 medio 1,03 a 0,5 s, 0,54 a 5 s; atteso
  2): la porta è prudente ma larga. A 3 s la sigma dichiarata è 2,41 m, cioè una porta al 99% di raggio circa 7,3 m
  (calcolo: 3,03 x 2,41): con più oggetti in scena non identifica più nessuno. Non misurato con più oggetti.
- In (ii) lo scarto fra la ricomparsa e la particella più vicina è al più 1,09 m (mediana 0,06 m).
- Debolezza dell'oracolo di tracciamento-2: il modello a particelle ha un «modo sosta» e lo scenario (ii) è una
  sosta: modello e verità qui non sono indipendenti. In (iii) la traccia a particelle vive fino al tetto di 10 s.
- numpy non era installato: ho riscritto le simulazioni in Python puro invece di installare pacchetti.
