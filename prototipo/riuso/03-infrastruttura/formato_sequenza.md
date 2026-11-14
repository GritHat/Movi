# Il formato comune di una sequenza (f10)

Lo usano il simulatore del sensore, il lettore dei dati veri e la catena. Una sequenza è **una cartella**:

```
<sequenza>/
  meta.json            obbligatorio
  tempi.csv            obbligatorio
  profondita/          obbligatoria: 000000.npy, 000001.npy, … (uno per fotogramma)
  verita.json          facoltativo
```

Esempio pronto: `03-infrastruttura/esempio_sequenza/` (31 fotogrammi 160×120, geometria ideale: è un esempio del
formato, **non** un modello di sensore). Controllo di una cartella:

```
f10-dati/ambiente/venv/bin/python -I -B f10-dati/03-infrastruttura/controlla_sequenza.py <sequenza> [--rigoroso] [--tutti]
```

Esce con 0 se la cartella rispetta il formato, con 1 se no (`ERRORE:` dice che cosa), con 2 se l'uso è sbagliato.
Gli `AVVISO:` non fanno fallire (con `--rigoroso` sì): segnalano cose sospette, come un'unità di misura dubbia.

## meta.json

Un oggetto JSON con **esattamente questi nomi** (altre chiavi in più sono ammesse e ignorate dal controllo):

| Chiave | Tipo | Significato |
|---|---|---|
| `larghezza`, `altezza` | interi > 0 | dimensioni dell'immagine in pixel (colonne, righe) |
| `fx`, `fy` | numeri > 0 | lunghezze focali in pixel |
| `cx`, `cy` | numeri | centro ottico in pixel (convenzione: il centro del pixel in alto a sinistra è (0, 0)) |
| `fps` | numero > 0 | fotogrammi al secondo nominali |
| `sensore` | testo | nome del sensore vero o del profilo simulato |
| `posa` | oggetto o `null` | se nota: `{"altezza_m": 1.2, "inclinazione_gradi": 15.0}`; altrimenti `null` |
| `origine` | testo | da dove viene: insieme di dati e sequenza (con l'indirizzo), oppure lo script che l'ha generata |
| `licenza` | testo | licenza della fonte (per i dati generati: «nessun vincolo (dati generati)») |

`posa.altezza_m` è l'altezza del centro ottico dal suolo, in metri. `posa.inclinazione_gradi` è l'angolo dell'asse
ottico **sotto** l'orizzontale: positivo verso il basso, fra −90 e 90. Si assume rollio nullo.

## tempi.csv

Prima riga: l'intestazione `indice,tempo_s`. Poi **una riga per fotogramma**: l'indice (0, 1, 2, … senza salti) e il
tempo in secondi (numero decimale, strettamente crescente; l'origine dei tempi è libera). Il lettore di riferimento
tollera l'intestazione assente (il controllo dà un avviso); chi legge con codice proprio deve saltarla.

## profondita/NNNNNN.npy

Un file per fotogramma, nome a sei cifre uguale all'indice. Matrice numpy **uint16** (`<u2`), forma
`(altezza, larghezza)`, valore = profondità **lungo l'asse ottico** (la coordinata Z nel riferimento della camera, non
la distanza lungo il raggio) in **millimetri**; **0 = nessun dato**. Oltre 65,535 m non si rappresenta: si scrive 0.
Si scrive con `np.save(..., allow_pickle=False)` e si legge con `np.load(..., allow_pickle=False)`: un `.npy` con
oggetti serializzati può eseguire codice, e qui i dati non sono fidati. Un fotogramma 640×480 occupa 614 528 byte
(misurato): 30 s a 30 fps sono 0,55 GB.

Punto 3D di un pixel (colonna u, riga v, profondità Z in metri), nel riferimento della camera (x a destra, y in basso,
z lungo l'asse ottico): `Xc = (u − cx)·Z/fx`, `Yc = (v − cy)·Z/fy`, `Zc = Z`.

## verita.json (facoltativo)

```json
{
  "fotogrammi": [
    {"indice": 0, "soggetti": [{"id": "s1", "x": -1.0, "z": 2.5, "visibile": true, "frazione_visibile": 1.0}]},
    {"indice": 1, "soggetti": []}
  ],
  "ostacoli": [
    {"id": "o1", "tipo": "poligono", "vertici": [[-0.3, 1.49], [0.3, 1.49], [0.3, 1.51], [-0.3, 1.51]], "altezza_m": 2.0},
    {"id": "o2", "tipo": "cerchio", "x": 1.0, "z": 2.0, "raggio_m": 0.2, "altezza_m": 1.0}
  ]
}
```

- `fotogrammi`: lista con indici crescenti, ciascuno presente in `tempi.csv`. Può coprire solo una parte dei
  fotogrammi (le annotazioni di un insieme di dati vero sono spesso più rade): un fotogramma assente dalla lista è
  «non annotato», uno presente con `"soggetti": []` è «annotato, nessun soggetto in scena».
- Ogni soggetto: `id` (testo, la stessa identità per tutta la sequenza), `x` e `z` in metri, `visibile` (`true` se il
  sensore ne vede almeno una parte in quel fotogramma, `false` se è nascosto). Facoltativo: `frazione_visibile` fra 0
  e 1 (consigliato nelle scene simulate, così ognuno sceglie la propria soglia). Altri campi sono ammessi.
- **Riferimento di `x` e `z`**: il piano del suolo visto dalla camera. Origine: il punto del suolo sulla verticale del
  centro ottico. `z`: in avanti, cioè la proiezione orizzontale dell'asse ottico. `x`: a destra. Con la posa
  (altezza h, inclinazione t) un punto della camera (Xc, Yc, Zc) va in:
  `x = Xc`, `z = Zc·cos t − Yc·sin t`, `quota = h − Yc·cos t − Zc·sin t`.
  Un suolo piano compare quindi alla profondità `Z = h / (((v − cy)/fy)·cos t + sin t)`.
- La posizione di un soggetto è il **centro della sua impronta sul suolo** (la proiezione del centro del corpo), non il
  punto della superficie più vicino alla camera: una camera di profondità vede la superficie davanti, quindi il centro
  dei punti misurati sta più vicino della verità di circa metà spessore del corpo. Chi confronta ne tiene conto.
- `ostacoli` (per le scene simulate): geometria fissa nello stesso riferimento. Tipi previsti: `poligono` (`vertici`:
  almeno tre coppie [x, z]) e `cerchio` (`x`, `z`, `raggio_m`); `altezza_m` facoltativa. Un tipo diverso dà un avviso.
- Se `posa` è `null` e c'è la verità, chi scrive la sequenza spiega in una chiave in più di `meta.json` (per esempio
  `nota_verita`) come ha ottenuto le posizioni.

## Lettura e scrittura da codice

Gli stessi lettori usati dal controllo si possono importare (così il formato ha una sola realizzazione):

```python
import sys
sys.dont_write_bytecode = True          # per non scrivere __pycache__ nella cartella dell'infrastruttura
sys.path.insert(0, "/home/fede/Scrivania/ed/GitHub/Movi-Hackthon/.sciame/20261114-1301-percezione-challenge/f10-dati/03-infrastruttura")
from controlla_sequenza import leggi_meta, leggi_tempi, leggi_profondita, leggi_verita, scrivi_sequenza, controlla

meta = leggi_meta(cartella)                    # dizionario
indici, tempi = leggi_tempi(cartella)          # lista di interi, vettore float64 (secondi)
prof = leggi_profondita(cartella, 0)           # uint16 (altezza, larghezza), millimetri, 0 = nessun dato
scrivi_sequenza(nuova, meta, tempi, fotogrammi, verita=None)   # nuova deve essere vuota; rifiuta ciò che non è uint16
errori, avvisi, note = controlla(cartella)     # tre liste di testi: valida se errori è vuota
```

Misurato su 300 fotogrammi 640×480 (in `/tmp`, che è in memoria: sul disco sarà più lento): scrittura 0,14 ms e
lettura 0,08 ms a fotogramma; il controllo completo 0,12 s, con `--tutti` 0,32 s.

## Che cosa il controllo NON può dire

- Che la profondità sia davvero lungo l'asse ottico e in millimetri: senza la posa il controllo riconosce solo gli
  errori grossolani (mediana sotto 50, 99° percentile oltre 20 m, 65535 usato come «nessun dato»). Con la posa
  confronta i valori con il suolo piano previsto e avvisa se meno del 2 % dei pixel validi gli è compatibile, o se più
  del 5 % vede oltre il suolo: è un confronto descrittivo, e su una scena vera con poco suolo in vista può avvisare a
  torto. Profondità in centimetri con `posa` nulla **non** vengono riconosciute.
- Che la verità sia giusta, che i parametri della camera siano quelli veri, che le identità siano coerenti.
- Senza `--tutti` i valori si leggono su 50 fotogrammi equispaziati (tipo e forma si controllano su tutti).
