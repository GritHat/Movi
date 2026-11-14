# AMBIENTE — l'ambiente di lavoro di f10 (sciame-infrastruttura, 14 novembre 2026, 15:57–16:10)

Percorsi relativi a `f10-dati/` = `/home/fede/Scrivania/ed/GitHub/Movi-Hackthon/.sciame/20261114-1301-percezione-challenge/f10-dati/`.
Tutto si rifà con `bash 03-infrastruttura/prova_tutto.sh --rete` (9 s; ultimo esito: `03-infrastruttura/esito_prove.txt`, 0 fallite).

## 0. Cambi di stato e regole violate

- **Violata per errore: una scrittura fuori da `f10-dati/`.** Alle 16:01:58 una prova del tetto di `scarica.sh` ha
  fatto morire curl con SIGXFSZ e il sistema ne ha registrato un'immagine di memoria (580,5 kB nell'archivio di
  `systemd-coredump`; prova: `coredumpctl list`). Corretto nello script e riprovato: nessun'altra
  (`coredumpctl list --since 16:02`). Quella non la posso togliere senza privilegi; contiene solo la memoria
  di curl (l'indirizzo pubblico della scheda e il percorso del file di destinazione).
- Ho letto in sola lettura `../f9-preproposta/07-lidar/scaricati/` (elenco e un'impronta): lo ammette il contratto.
- Nessun `sudo`, nessun git, nessuna GPU, nessuna installazione globale. Stati: «ambiente assente» → **verificato**
  sulle prove elencate (un campione, non una prova universale; vedi §5).

## 1. L'ambiente Python

**Interprete da usare negli script (percorso esatto):**

```
/home/fede/Scrivania/ed/GitHub/Movi-Hackthon/.sciame/20261114-1301-percezione-challenge/f10-dati/ambiente/venv/bin/python
```

Non serve «attivarlo»: si chiama quell'interprete, **sempre con `-I`** (non carica codice dalla cartella corrente né
da quella dello script: serve quando si leggono dati non fidati) e meglio con `-B` (niente `__pycache__`):
`…/ambiente/venv/bin/python -I -B mio_script.py`. Con `-I` uno script non importa i moduli che gli stanno accanto: li
si aggiunge con `sys.path.insert(0, "<cartella propria>")`, mai con una cartella di `scaricati/`.

| Pacchetto | Versione | | Pacchetto | Versione |
|---|---|---|---|---|
| Python (di sistema, `/usr/bin/python3`) | 3.14.10 | | pillow | 13.0.0 |
| numpy | 2.5.4 | | rosbags (legge .bag ROS1 e ROS2, puro Python) | 0.11.9 |
| scipy | 1.18.1 | | dipendenze di rosbags: apsw, lz4, ruamel-yaml | 3.54.1.0, 4.4.5, 0.19.1 |
| opencv-python-headless | **5.0.0.93** (non 4.x) | | uv (solo per creare l'ambiente) | 0.12.1 |

Congelate con le impronte di ogni ruota in `03-infrastruttura/requisiti.txt` (generato da `requisiti.in`). Tutte ruote
già compilate (`--only-binary :all:`): niente è stato compilato, e il ripiego su un altro Python non è servito.

- **Ricreare o riparare:** `bash 03-infrastruttura/crea_ambiente.sh` (rilanciabile: la seconda volta «Checked 8
  packages» e basta; verificato). Cache di uv e Python gestiti restano in `ambiente/` (`UV_CACHE_DIR`,
  `UV_PYTHON_INSTALL_DIR`): `find -newer` su `~/.cache/uv`, `~/.local/share/uv`, `~/.config/uv` dopo l'installazione
  dà 0 file.
- **Tornare indietro:** `rm -rf ambiente/venv` (e `ambiente/cache-uv`). Occupa 721 MB (357 l'ambiente, 359 la cache).
- **Se manca il Python di sistema** (l'ambiente punta a `/usr/bin/python3.14`: un aggiornamento del sistema a un'altra
  versione lo rompe): `rm -rf ambiente/venv`, poi `PYTHON_AMBIENTE=3.13 bash crea_ambiente.sh` scarica un Python in
  `ambiente/python-uv/`. **Non verificato** (non è servito). Ripiego ultimo: Python puro o C, come da contratto.
- **Aggiungere un pacchetto:** una riga in `requisiti.in`, `rm requisiti.txt`, rilanciare `crea_ambiente.sh` e dirlo
  nella propria consegna (le versioni degli altri potrebbero muoversi: controllare il diff di `requisiti.txt`).

**Prova che funziona** (`03-infrastruttura/prova_ambiente.py`, 7 su 7): numpy risolve un sistema 500×500 con residuo
relativo 7,3e-16; prodotto 1000×1000 in 9,1 ms con tutti i fili e 31,1 ms con uno; `.npy` uint16 andata e ritorno
senza pickle; `scipy.ndimage.label`; PNG a 16 bit scritto da opencv e riletto uguale da pillow; rosbags scrive e
rilegge un `.bag` ROS1 con un'immagine `16UC1`.

## 2. La macchina (misure delle 15:57 e 16:09)

- **Processori:** 24 logici (`nproc`), cioè 12 nuclei × 2 fili, AMD Ryzen AI 9 HX 370 (`lscpu`). Carico medio 2,1–2,6:
  altri processi girano. **Memoria:** 30 GiB, 22 disponibili (`free -h`).
- **Disco:** 183 GiB liberi su `/home` (196 064 104 448 byte, `df`), 64 % usato. Il tetto di 6 GB per `scaricati/` è
  del contratto, non del disco. `/tmp` è in memoria (tmpfs, 15 GiB): non metterci sequenze grandi.
- Per le misure di costo (ipotesi 6) fissare i fili, altrimenti numpy e opencv ne usano 24 (`cv2.getNumThreads()` =
  24): `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1` e `cv2.setNumThreads(1)`, e dichiararlo accanto al numero.

## 3. Gli script (tutti in `03-infrastruttura/`)

| Script | Che cosa fa | Uso |
|---|---|---|
| `scarica.sh` | Scarica un file in `scaricati/<nome>/` e annota indirizzo, ora, dimensione e sha256 in `PROVENIENZA.md` accanto. Solo `https`; tempo massimo (≤ 600 s) imposto da curl e da `timeout`; tetto imposto da curl, da `ulimit -f` e da un controllo finale; tetto complessivo di 6 GB; file salvato 0644, mai eseguito; rilanciato non riscarica. | `bash scarica.sh <nome> <indirizzo> <tetto> [--licenza "…"] [--file NOME] [--tempo S] [--riprendi]` — tetto in byte o con K, M, G |
| `apri_archivio.py` | Apre zip e tar (anche gz, bz2, xz, zst) in una cartella **nuova** dentro `f10-dati/`. Rifiuta tutto l'archivio se un percorso è assoluto o contiene `..`, o se c'è un collegamento o un file speciale; tetto ai byte e al numero di file; estrae in `.in-corso` e rinomina alla fine. | `python3 -I apri_archivio.py <archivio> <cartella_nuova> [--tetto 2G] [--salta-collegamenti]` |
| `controlla_sequenza.py` | Verifica il formato comune (`formato_sequenza.md`) e offre i lettori da importare. | `…/venv/bin/python -I -B controlla_sequenza.py <cartella> [--rigoroso] [--tutti]` |
| `crea_esempio_sequenza.py` | Scrive `esempio_sequenza/` (31 fotogrammi 160×120, ideale: esempio del formato, non modello di sensore). | `… crea_esempio_sequenza.py <cartella_nuova>` |

Codici d'uscita e garanzie stanno in testa a ogni script. Le previsioni, scritte alle 15:59:07 prima delle prove, e i
loro esiti sono in `PREVISIONI.md`: **9 su 9 reggono**.

**Prove fatte** (file scaricati per la sola prova in `scaricati/prova-infrastruttura/`, 5,1 MB con l'archivio aperto):
1. `scarica.sh` sulla scheda ST VL53L7CX già citata dallo sciame (<https://www.pololu.com/file/0J1992/vl53l7cx.pdf>,
   aperta: risposta 200): 2 707 367 byte in 1,4 s, `%PDF-1.3`, sha256 `b3a6559f…a8f3f3c8`, uguale a un `sha256sum`
   rifatto e alla copia scaricata da un altro agente in f9. Con tetto 1M: uscita 4 e nessun file rimasto, sia con la
   dimensione dichiarata dal server sia con il solo limite di sistema. Indirizzo inesistente (inventato apposta): 404,
   uscita 5, niente tenuto. Indirizzi `http://` o con credenziali, nomi con `..`: uscita 2.
2. Sorgente di rosbags da PyPI (`rosbags-0.11.9.tar.gz`, 350 540 byte, Apache-2.0 secondo i metadati di PyPI):
   l'impronta calcolata coincide con quella pubblicata da PyPI (`2d0df7de…e5dc0fa4`: controllo con una fonte esterna);
   aperto in 170 file, come conta `tar tzf`; nessun collegamento, nessun file eseguibile.
3. `apri_archivio.py` (`prova_archivi.py`): 14 archivi ostili su 14 rifiutati senza resti né file fuori; 2 buoni su 2
   aperti identici e senza bit d'esecuzione; 2 destinazioni non ammesse rifiutate. Controllo negativo: un estrattore
   ingenuo, sullo stesso archivio, il file fuori lo crea.
4. `controlla_sequenza.py` (`prova_controllo.py`): 4 sequenze valide su 4 accettate, 24 difettose su 24 rifiutate
   (tipo, forma, fotogrammi mancanti o in più, tempi, chiavi di `meta.json`, pickle, file troncato, verità), 8 sospette
   su 8 segnalate (unità, segno dell'inclinazione, altezza, fps, 65535 come «nessun dato»).

## 4. Critiche (a ciò che ho costruito)

1. **Indipendenza.** Archivi ostili e varianti difettose li ho scritti io: i controlli 3 e 4 condividono l'autore con
   ciò che provano. Esterni sono solo l'impronta di PyPI, il conteggio di `tar` e la copia della scheda in f9.
2. **Il contatore dei byte scritti di `apri_archivio.py` non è mai scattato**: gli archivi troppo grandi sono fermati
   prima, dalla dimensione dichiarata. Seconda barriera **non verificata**.
3. **Il tetto di 6 GB è controllato senza blocco fra agenti**: due scaricamenti contemporanei in cartelle diverse
   possono superarlo insieme. `--riprendi` dopo un tempo scaduto: **non verificato** (nessun file abbastanza lento).
4. **L'unità e l'asse della profondità non sono verificabili dal formato**: il controllo avvisa solo sugli errori
   grossolani; centimetri con posa nulla passano. Il confronto con il suolo è descrittivo e condivide la formula con
   l'esempio (stesso autore).
5. **La licenza non la verifica nessuno script**: `scarica.sh` la annota come gliela si dà («DA COMPILARE» se manca).
   Quella della scheda ST l'ho annotata «non verificata».
6. `tempi.csv`: l'intestazione `indice,tempo_s` è una mia precisazione della consegna («una riga per fotogramma»);
   la sua assenza è tollerata con un avviso.

## 5. Che cosa propongo dopo

- Chi scarica dati veri: una cartella per fonte, `--licenza` sempre, archivi aperti solo con `apri_archivio.py`.
- Chi produce sequenze: `controlla_sequenza.py --rigoroso` prima di consegnarle, e l'esito nella consegna.
- Per l'utente, quando arriveranno i sensori: lo stesso formato vale per una registrazione fatta dalla squadra
  (serve solo un lettore che scriva `meta.json`, `tempi.csv` e i `.npy`); l'SDK del sensore andrà aggiunto a
  `requisiti.in` e verificato su Python 3.14 (**non verificato** che esistano le ruote).
