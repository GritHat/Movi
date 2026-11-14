# Catena di riferimento (f10, `10-catena`) — comandi e uso

Codice di **validazione** del nucleo (`f4/H-012/05-correzioni/SOLUZIONE_V2.md`), non il prototipo. Python con solo
numpy (scipy serve a una prova). Consegna, letture ed esiti: `CATENA.md`; previsioni ed esiti: `PREVISIONI.md`.

Percorsi relativi a `f10-dati/`. Interprete: `ambiente/venv/bin/python`, sempre con `-I -B` (vedi
`03-infrastruttura/AMBIENTE.md`).

## Comandi

```sh
PY=ambiente/venv/bin/python

# le prove automatiche (25, circa 6 s); una sola: aggiungere per esempio ProvaMappa.test_p04_un_ostacolo
$PY -I -B 10-catena/prove.py

# una sequenza nel formato comune → fotogrammi.jsonl, riassunto.json (e griglie.npz)
$PY -I -B 10-catena/esegui.py 03-infrastruttura/esempio_sequenza 10-catena/uscite/esempio --salva-griglie

# 30 fps portati a 15 Hz, portata 4 m, q diverso, posa imposta a mano
$PY -I -B 10-catena/esegui.py <sequenza> <uscita> --ogni 2 -p portata_m=4.0 -p q=0.5 --posa 1.2,15
```

`esegui.py` esce con 0 (fatto), 2 (uso sbagliato), 3 (un invariante violato: è un difetto della catena, va
segnalato). Usa un filo solo (`OPENBLAS_NUM_THREADS=1`), così i tempi si ripetono. Ogni campo di
`parametri.Parametri` si cambia con `-p nome=valore`.

## I file

| File | Che cosa fa |
|---|---|
| `parametri.py` | tutti i numeri del nucleo e le letture, in una `dataclass`; le tre curve di rumore |
| `sorgente.py` | l'interfaccia `Sorgente` (`meta` più l'iterazione su `(indice, tempo, profondità uint16)`), la cartella nel formato comune, la lista in memoria |
| `geometria.py` | posa (da `meta.json` o stimata: `stima_suolo`), coefficienti per pixel della proiezione sul suolo |
| `mappa.py` | la griglia polare e i quattro stati, con la memoria e l'età; invarianti 1 e 2 |
| `gruppi.py` | gruppi connessi, centro, larghezza, marca «tagliato da un'ombra» |
| `kalman.py` | filtro a velocità quasi costante, R(z), assegnazione ungherese |
| `presenza.py` | strato di possibile presenza, cuneo d'ingresso, regola del riaggancio, **predittore** |
| `inseguimento.py` | tracce, associazione, conferma 3 su 5, «si muove», stati dell'oggetto |
| `catena.py` | il ciclo, l'uscita per fotogramma, invarianti 3, 4, 7, `esegui()` |
| `esegui.py` | riga di comando |
| `scene_a_mano.py`, `prove.py` | le scene minime e le 25 prove; `esito_prove.txt` è l'ultimo esito |
| `uscite/esempio/` | l'uscita sull'esempio dell'infrastruttura (per vedere il formato) |

## Uso da codice (per chi valida)

```python
import sys
sys.dont_write_bytecode = True
sys.path.insert(0, ".../f10-dati/10-catena")
from catena import Catena, esegui
from parametri import Parametri, LIBERO, OCCUPATO, IN_OMBRA, NON_OSSERVATO
from sorgente import SorgenteCartella

sorgente = SorgenteCartella(cartella, ogni=2)
catena = Catena(sorgente.meta, Parametri(q=0.2))      # senza posa in meta.json: passare posa=stima_suolo(...)[0]
for indice, t, prof in sorgente:
    uscita = catena.ciclo(indice, t, prof)            # il dizionario di una riga di fotogrammi.jsonl
    catena.mappa_ciclo.stati                          # (180, 30) uint8: stato di ogni cella
    catena.mappa_ciclo.eta                            # fotogrammi dall'ultima volta vista libera
    catena.possibile_presenza                         # (180, 30) bool
    catena.griglia.cella(x, z)                        # (indice d'azimut, indice di distanza) di un punto, o None
```

Griglia: azimut da −90° a +90° (indice 0 = da −90° a −89°; positivo a destra), distanza da 0 a `portata_m`.
Posizioni in metri nel riferimento di `verita.json`: x a destra, z in avanti.

**Un sensore vero** entra scrivendo una classe con `meta` (le chiavi di `meta.json`) e `__iter__` che dà
`(contatore, tempo in secondi, matrice uint16 in millimetri con 0 = nessun dato)`: la catena non chiede altro.
Vanno spenti i filtri della camera che riempiono i buchi (condizione 1 del verdetto): qui uno 0 è un dato.

**Un predittore diverso** per l'occlusione (quello che sceglie f8) è una classe come
`presenza.PredittoreVelocitaCostante`: `__init__(self, ingresso, par)` riceve lo `StatoIngresso` (identità, istante,
stato e covarianza del filtro all'ingresso, ultima misura, larghezza, celle del cuneo d'ombra);
`passo(self, t, ciclo, griglia)` riceve l'istante, la mappa del ciclo (`ciclo.stati` e il resto) e la griglia, e
restituisce una `Previsione(x, z, p)` con la covarianza 2×2 della posizione. Si innesta con
`Catena(meta, par, fabbrica_predittore=MiaClasse)` o `esegui(..., fabbrica_predittore=MiaClasse)`. Decide ciò che
esce come «previsto», quando si passa a «perso» e lo scarto registrato al riaggancio; non tocca lo strato di
possibile presenza né la regola del riaggancio.

## L'uscita

`fotogrammi.jsonl`, una riga per fotogramma: `indice`, `t`, `contatore_sensore`; `celle` (conteggio per stato);
`libero_per_eta`; `pixel_validi`; `suolo_visto_in_ombra` e `celle_ambigue` (diagnostici); `settori` (ogni 10°:
conteggi nell'ordine non osservato, libero, occupato, in ombra; distanza del primo occupato; celle con possibile
presenza); `gruppi`; `tracce` (stato, età dello stato, `misura_nel_ciclo`, `misura_tagliata`, `ultima_misura`,
`si_muove` — `null` se non valutabile —, posizione, velocità e covarianza `[xx, xz, zz]`; in «previsto» la
`regione_prevista`; in «perso» nessuna posizione; durante l'occlusione `previsione_diagnostica`, che serve solo a
misurare la previsione e non è un'uscita del prototipo); `possibili_presenze` (traccia, età, celle, area, estensione);
`eventi` (`nascita`, `conferma`, `ingresso_in_ombra`, `perso`, `riaggancio` con scarto, raggio al 95 % e `in95`,
`prima_misura_piena`, `identita_ambigua`, `strato_finito`, `chiusura`); `tempo_ciclo_ms`.

`riassunto.json`: posa usata (e se è stimata), parametri, celle per stato (somma sui fotogrammi e frazioni),
diagnostici, eventi per tipo, tracce confermate, tempo per ciclo (media, 95° percentile, massimo; solo
l'elaborazione, con gli invarianti accesi). `griglie.npz` (con `--salva-griglie`): `stati`, `eta_fotogrammi`,
`possibile_presenza` per fotogramma, più `indici`, `tempi`, `azimut_gradi`, `distanza_m`; si legge con
`np.load(..., allow_pickle=False)`.
