# Previsioni di sciame-infrastruttura (f10, preparazione dell'ambiente)

Scritte il **2026-11-14T15:59:07+01:00** (`date -Is`), prima di creare l'ambiente, di scrivere gli script e di
lanciare qualunque prova. A quell'ora le cartelle `ambiente/`, `scaricati/` e `03-infrastruttura/` erano vuote
(`ls`, stessa chiamata). Gli esiti stanno in fondo, aggiunti dopo le prove e tenuti distinti.

| Sigla | Previsione | Misura | Soglia di smentita |
|---|---|---|---|
| infra-P1 | Su Python 3.14.10 di sistema, `numpy`, `scipy`, `opencv-python-headless`, `pillow` e `rosbags` si installano tutti da ruote già compilate, senza compilare niente. | Esito di `uv pip install --only-binary :all:` e `import` di ciascuno. | Smentita se anche uno solo non si installa o non si importa su 3.14 (allora si prova un Python gestito da uv dentro la cartella). |
| infra-P2 | L'installazione non scrive niente fuori da `f10-dati/` (cache di uv compresa). | Data di modifica di `~/.cache/uv` e di `~/.local/share/uv` prima e dopo; `find -newer` su quelle cartelle. | Smentita se compare un file nuovo o modificato fuori da `f10-dati/`. |
| infra-P3 | numpy risolve un sistema lineare 500×500 con residuo relativo < 1e-9 e moltiplica due matrici 1000×1000 in meno di 1 s. | Residuo e tempo misurati. | Smentita se il residuo è ≥ 1e-9 o il tempo ≥ 1 s. |
| infra-P4 | `scarica.sh` scarica la scheda ST VL53L7CX (`https://www.pololu.com/file/0J1992/vl53l7cx.pdf`, già citata in `f3/fonti/FONTI_VERIFICATE.md`) in meno di 60 s; il file è un PDF (primi byte `%PDF`) fra 0,3 e 5 MB; l'impronta annotata coincide con un `sha256sum` rifatto a parte. | Tempo, dimensione, primi byte, due impronte. | Smentita se lo scaricamento fallisce, se il file non è un PDF, o se le impronte differiscono. Se il sito rifiuta la richiesta, l'esito è «non risolta» e si prova un altro file pubblico. |
| infra-P5 | Con un tetto più basso della dimensione del file, `scarica.sh` rifiuta e non lascia nessun file nella cartella (né intero né parziale), sia quando il server dichiara la dimensione sia quando il limite lo impone solo il sistema (`ulimit -f`). | Codice d'uscita ≠ 0 e `ls` della cartella, nei due casi. | Smentita se resta un file o se il codice d'uscita è 0. |
| infra-P6 | Rilanciato sullo stesso file, `scarica.sh` non riscarica: verifica l'impronta ed esce con 0. | Codice d'uscita, messaggio, numero di righe in `PROVENIENZA.md`. | Smentita se riscarica o se duplica la riga. |
| infra-P7 | L'apritore di archivi rifiuta 6 archivi ostili su 6 (percorso con `..`, percorso assoluto, collegamento simbolico, collegamento fisico, file speciale, contenuto oltre il tetto) senza creare niente fuori dalla cartella di destinazione, e apre 2 archivi buoni su 2 (un tar e uno zip). | Codici d'uscita; esistenza dei file «sentinella» fuori dalla destinazione. | Smentita se un archivio ostile passa, se nasce un file fuori, o se un archivio buono è rifiutato. |
| infra-P8 | L'apritore apre un archivio pubblico vero (il sorgente di `rosbags` da PyPI) e l'impronta calcolata da `scarica.sh` coincide con quella pubblicata da PyPI. | Confronto delle due impronte (controllo indipendente dal mio codice: l'impronta la pubblica PyPI). | Smentita se differiscono o se l'archivio non si apre. |
| infra-P9 | Il programma di controllo accetta una sequenza d'esempio valida e rifiuta almeno 10 varianti difettose su 10 (tipo non uint16, forma sbagliata, fotogramma mancante, tempi non crescenti, chiave mancante in `meta.json`, `.npy` con oggetti serializzati, indice della verità inesistente, e altre). | Codici d'uscita su ogni variante. | Smentita se una variante difettosa passa o se la sequenza valida è rifiutata. |

Che cosa queste prove NON dicono: zero errori su 6 archivi ostili e su 10 varianti difettose sono un campione, non una
prova universale; gli archivi ostili e le varianti li ho scritti io, quindi il controllo condivide l'autore con ciò
che controlla (vale solo P8 come controllo con una fonte esterna).

## Esiti

Compilati il 2026-11-14T16:09:25+01:00, dopo le prove (15:59:49 – 16:09). Il testo sopra non è stato toccato.
Per rifare tutto: `bash prova_tutto.sh --rete` (ultimo esito in `esito_prove.txt`, 0 prove fallite).

| Sigla | Esito | Prova |
|---|---|---|
| infra-P1 | **regge** | `crea_ambiente.sh`: 5 pacchetti chiesti su 5 (8 con le dipendenze) installati con `--only-binary :all:` su Python 3.14.10, in 3,5 s; `prova_ambiente.py`: 7 prove su 7. Il ripiego su un altro Python non è servito (e quindi è **non verificato**). |
| infra-P2 | **regge, per l'installazione** | `find ~/.cache/uv ~/.local/share/uv ~/.config/uv -newer <segnale>`: 0 file. Controllo limitato a quelle tre cartelle. Vedi però la nota 1 qui sotto: un'altra prova ha lasciato una traccia fuori. |
| infra-P3 | **regge** | residuo 7,26e-16; prodotto 1000×1000 in 9,1 ms (migliore di 3, tutti i fili), 31,1 ms con un filo solo. |
| infra-P4 | **regge** | 1,36 s; 2 707 367 byte; primi byte `%PDF-1.3`; impronta `b3a6559f…f3f3c8` uguale con `sha256sum` rifatto, e uguale alla copia scaricata da un altro agente (`f9-preproposta/07-lidar/scaricati/vl53l7cx_ds.pdf`: scaricamento indipendente dal mio script). |
| infra-P5 | **regge** | uscita 4 nei due casi (curl 63 con la dimensione dichiarata; errore di scrittura 23 con il solo `ulimit -f`), nessun file rimasto. |
| infra-P6 | **regge** | uscita 0, «GIÀ PRESENTE», una sola voce per file in `PROVENIENZA.md`. |
| infra-P7 | **regge** | 6 ostili previsti su 6 rifiutati, 2 buoni su 2 aperti con contenuto identico e senza bit d'esecuzione (uno era dichiarato 04755). In più, non previsti: altri 8 ostili su 8 e 2 destinazioni non ammesse su 2. Controllo negativo: sullo stesso archivio 1 un estrattore ingenuo la sentinella fuori dalla destinazione la crea. |
| infra-P8 | **regge** | impronta calcolata `2d0df7de…dc0fa4` = impronta pubblicata da PyPI per `rosbags-0.11.9.tar.gz` (350 540 byte); aperto: 170 file, come `tar tzf` (170). |
| infra-P9 | **regge** | `prova_controllo.py`: 4 valide su 4 accettate, 24 difettose su 24 rifiutate, 8 sospette su 8 segnalate. |

### Notato dopo (non era previsto)

1. **Una traccia fuori da `f10-dati/`.** La prima prova del tetto con il solo `ulimit -f` (16:01:58) ha fatto morire
   curl con SIGXFSZ, e il sistema ne ha registrato un'immagine di memoria (`coredumpctl list`: curl, 580,5 kB,
   nell'archivio di sistema). Corretto subito (`trap '' XFSZ` e `ulimit -c 0` in `scarica.sh`); le prove rifatte non
   ne hanno prodotte altre (`coredumpctl list --since 16:02`: nessuna). Quella registrata non la posso togliere senza
   privilegi.
2. I due archivi «oltre il tetto» (6 e 9) sono fermati dalla dimensione **dichiarata**, al primo passaggio; lo zip che
   mente sulla dimensione (14) è fermato dal controllo d'integrità di `zipfile`. Il contatore dei byte scritti, seconda
   barriera, non è scattato in nessuna prova: **non verificato**.
3. OpenCV installato è la **5.0.0**, non una 4.x: chi scrive codice per la 4 controlli le funzioni che usa.
4. Importare `controlla_sequenza` crea `__pycache__/` nella mia cartella: chi importa usi `-B` o
   `sys.dont_write_bytecode = True`.
5. Profondità in centimetri con posa nulla non sono riconosciute dal controllo (lo riconosce solo il confronto con il
   suolo, che vuole la posa).
6. numpy all'avvio occupa tutti i 24 fili per qualche istante (2,1 s di CPU in 0,12 s di orologio): per le misure di
   costo si fissano i fili.
