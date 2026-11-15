# CORTO_RAGGIO — prototipo MoVi, modo a corto raggio (`sciame-sviluppatore`, f16-prototipo/10)

15 novembre 2026, 00:17–00:40 (`date -Is`; la consegna dice «14 novembre»: l'orologio era già oltre mezzanotte).
Codice: `/home/fede/Scrivania/ed/GitHub/Movi-Hackthon/prototipo`. Previsioni: `PREVISIONI.md`, qui accanto.
**Tutto è simulazione (camera di profondità simulata dalle schede, `riuso/11-simulatore`). Nessun sensore fisico; niente
è «validato». Le etichette di classe sono a mano da file; il classificatore non è realizzato (lavori futuri).**

## 0. Cambi di stato e regole

- **Previsioni:** reggono sv-P1, P2, P3, P6, P7, P8, P9, P10. **Smentite: sv-P5** (riaggancio 11 su 90) **e sv-P4 sui
  passaggi interi a 2 e 3 s** (regge entro 3 m). **Non risolta: sv-P4b** (la regione stretta non arriva mai a 1 s).
- **Regole.** (a) La tabella di `PREVISIONI.md` era già nella cartella all'avvio (00:15:23, prima del nucleo). L'ho
  adottata senza cambiarla. Le definizioni operative le ho aggiunte alle 00:25, prima dei lanci, dopo un solo
  passaggio di prova. (b) Ho cambiato file dello scheletro dell'architetto: `etichette/persone.json`, dove la regola «tutta la
  scena» etichettava anche il pannello e ora la regola è `id_vero: s1`; poi le configurazioni delle scene (ora con
  regione e «libero» accesi) e `SCENE.json`. (c) Campagne a 6 processi (il tetto è 8). (d) Ho cancellato tre mie
  cartelle di prova in `prototipo/uscite`. Non ho usato git, sudo o la rete.

## 1. Che cosa c'è (1 082 righe, `wc -l`, in corto, predittore_zona, livelli, mostra, tabellone e `prove/`)

| Pezzo | File | Riuso |
|---|---|---|
| Catena con le correzioni di f12 (gruppi a celle forti, riaggancio che rifiuta i tagliati, ripartenza del filtro, strato che resta) | `riuso/catena/` (copia byte per byte, `IMPRONTE.txt`) | interruttore `correzioni_f12`, acceso |
| Nucleo corto | `movi/corto.py` | compone tutto; non legge mai la verità per decidere |
| Salute del sensore e controllo all'avvio (§1.9: 0,13 s senza fotogramma, tre identici, pixel validi < metà della taratura per 0,2 s; taratura = mediana dei primi 5 fotogrammi) | `corto.SaluteSensore` | nuovo, dalla regola di SOLUZIONE_V3 |
| «Libero» dal fotogramma, PR4 = `nuvole-1` (metà dell'impronta della cella e delle 8 vicine) | `corto._Libero` → `riuso/libero/libero.py` | interruttore `libero_dal_fotogramma`; può solo TOGLIERE «libero» alla catena |
| Predittore della zona: porto SEMPLIFICATO di sd-1 (400 membri fronte + scia, peso 0,1 sul visto libero, 3 lisciature, 90 %, «ampio» oltre 0,8 dell'ombra o 45 cicli) | `movi/predittore_zona.py` | interruttore `predittore_zona`; ripiego = velocità costante (il disco che cresce, poi tutta l'ombra) |
| Livelli per settore (10°, «visto libero fino a d» da 1,3 m nella direzione peggiore) | `movi/livelli.py` | non riceve etichette |
| Eventi «osservato»/«dedotto» (avviso acceso, tolto guardando, non ricomparso, affidabilità) | `movi/eventi_registro.py` | `riuso/eventi/eventi.py` **non collegato** |
| Etichette a mano da file (`id_vero`, `id_traccia`, zona e tempo), ferme sulla traccia | `movi/etichette.py` | classi controllate contro `classi.json` |
| Registro (formato dell'architettura) + controllo fra righe dell'avviso (architetto-1) | `movi/registro.py` | — |
| Tabellone «dentro la zona: k su n», viste e filmato | `movi/tabellone.py`, `movi/mostra.py` | — |
| Prove | `prove/prova_principi.py`, `misura_corto.py`, `riassumi_misure.py`, `misura_stretta.py` | — |

Interruttori non realizzati nel corto: `c7_identita_al_ritorno`, `fascia_di_scenario`, `regione_per_classe`. Se uno è acceso,
il nucleo si ferma con il codice 4: non fa finta di applicarlo. Lo stato degli interruttori è in OGNI riga del registro
(`dichiarazioni.regole_accese`) e nella riga fissa di ogni immagine.

## 2. Come si lancia (da `prototipo/`)

    sh prova_tutto.sh          # impronte, 25 prove della catena, banco C, registro, principi (rapida), 5 scene con filmato
    sh movi.sh esegui resta_dietro --config scene/resta_dietro.json --uscita uscite/resta_dietro --celle
    sh movi.sh mostra uscite/resta_dietro/registro.jsonl --filmato --uscita uscite/resta_dietro/viste   # movi.mp4, 1920×1080
    sh movi.sh tabellone uscite/resta_dietro/registro.jsonl
    PY=../.sciame/20261114-1301-percezione-challenge/f10-dati/ambiente/venv/bin/python
    $PY -I -B prove/prova_principi.py            # completa: P6–P10, ~2 min
    sh uscite/misure/lancia.sh && $PY -I -B prove/riassumi_misure.py uscite/misure   # 450 passaggi, ~4,5 min a 6 processi

Ultimo `sh prova_tutto.sh` (00:36, dopo l'ultima modifica): **esito 0, 59 s**: 22 passi «ok» e 6 scene `lp_*` «non ancora costruito»
(codice 4). Sorgente simulata: `{"tipo": "simulata", "nome": "d435i_nom__pannello_<caso>__s<k>"}` genera al volo un
passaggio nuovo.

## 3. Misure (soglie scritte prima; braccio principale zona+libero; 150 passaggi nuovi, k = 100…129, casi a12, a05, b, c, d)

Fonte: `RIASSUNTO.txt` e `prova_principi_completa.txt` qui accanto. Un «ciclo» vale 1/15 s.

| # | Misura | Esito | Stato |
|---|---|---|---|
| sv-P1 | cicli a persona nascosta dopo l'ingresso senza regione né avviso | **0 su 5 820** (Wilson 0–0,07 %) | regge |
| sv-P2 | fotogrammi a persona nascosta senza avviso | 2 su 5 822 (0,03 %; 0,01–0,13 %); ritardo massimo 2 cicli (a05) | regge |
| sv-P3 | celle «libero» dentro l'ombra vera interna (codici 1, 3) | **0 su 3 062 304** celle·fotogramma; bordo: 0 | regge |
| sv-P4 | persona dentro ciò che è mostrato, tutti i passaggi | 1 s: 117/118 (95,4–99,9 %); **2 s: 59/84 (59,8–79,0 %)**; **3 s: 30/60 (37,7–62,3 %)** | **smentita** a 2 e 3 s |
| sv-P4 | idem, persona entro 3 m | 1 s 117/118; 2 s 59/59 (93,9–100 %); 3 s 30/30 (88,6–100 %) | regge |
| sv-P4b | dentro la regione STRETTA a 1, 2, 3 s | n = 0 o 1 a ogni orizzonte | **non risolta** |
| sv-P5 | ritorno con riaggancio «presunta» (a12, a05, b) | **11 su 90** (12,2 %; 7,0–20,6 %); «certa» al riaggancio: 0 | **smentita** |
| sv-P6 | tempo per ciclo, un processo, 899 cicli (b, k = 100…109) | mediana 9,4 ms, p95 10,4 ms, massimo 33,5 ms | regge |
| sv-P7 | avvisi tolti senza guardare | 0 in 450 passaggi (tre bracci; Wilson 0–0,85 % per passaggio); il controllo coglie un registro artefatto | regge |
| sv-P8 | etichette tolte: avvisi, settori, celle | 0 righe diverse in 10 passaggi b | regge |
| sv-P9 | pavimento vuoto (catalogo, 30 fotogrammi): tracce confermate, avvisi | 0 e 0 | regge |
| sv-P10 | sensore coperto (catalogo, 1,0–2,2 s) | affidabilità persa dopo 0,133 s, per la regola dei «tre identici»; 0 celle libere o occupate | regge |

**Che cosa vuol dire.** Le garanzie (P1, P2, P3, P7, P10) reggono sui passaggi nuovi e a ogni braccio: l'avviso non manca
a persona nascosta, il «libero» non entra nell'ombra vera, nessun avviso sparisce senza essere guardato. P4 cade solo
dove la persona esce dalla portata: nel caso d, a 3 s, è a più di 3 m in tutti i 30 passaggi. Lì la griglia non esiste.
Il sistema non dichiara niente (né libero né presenza), ma neppure la mostra. È il limite di SCALA dell'addendum, visto
dal codice. Le tre misure di regione sono IDENTICHE nei tre bracci (`base`, `zona`, `zona_libero`): a 3 m la regione
stretta diventa «ampia» prima di 1 s, e da lì vale solo l'ombra. Quindi il predittore, a questa scala, non cambia ciò
che lo schermo mostra a 1, 2, 3 s.

**Notato dopo (non previsto, da confermare):** `misura_stretta.py`, tutti i fotogrammi a persona nascosta con regione
stretta: b 190/190, **a05 23/39 (43–73 %)**, **d 189/227 (77,9–87,6 %)**. I fotogrammi di un passaggio sono
correlati, quindi Wilson è ottimista. Il porto semplificato NON tiene il 90 % dichiarato: il registro ora porta
`livello_verificato: false` e lo schermo lo scrive. Altro: in `due_persone`, per 2 fotogrammi, la traccia della persona
ferma resta «vista» mentre l'altra la copre del tutto. La causa probabile, l'associazione al gruppo di chi copre, è
**non verificata**.

**Indipendenza.** Ho scritto io il nucleo, le misure e il controllo fra righe. Verità, ombra vera e percorsi vengono
dal simulatore dello sciame, lo stesso che ha messo a punto la catena. Le misure valgono solo per i difetti fuori da
questo insieme: non dicono niente su un sensore vero.

## 4. Limiti (che cosa non regge)

1. **Identità al ritorno:** 11 riagganci su 90; di solito nasce una traccia nuova e la vecchia resta «previsto ampio»,
   con identità «ambigua» (critica 4 dell'architetto, ora misurata).
2. **La regione stretta dura meno di 0,5 s** (b: mediana 0,40 s, massimo 0,47 s): a 3 m l'ombra del pannello è piccola, e la soglia
   «ampio» (0,8 dell'ombra) scatta subito. Il porto non è confrontato col banco in C (architetto-3, aperto). La
   libreria dei percorsi è sostituita da cinque manovre con probabilità scelte da me: sono **ipotesi senza fonte**.
3. **«Visto libero fino a d»:** solo 111 settori-fotogramma su 540 sul pavimento vuoto (20,6 %). La metà dei 18
   settori è fuori dal campo (87°), e PR4 lascia buchi alla guardia.
4. Copertura del sensore colta dai «tre identici» (fotogrammi tutti a zero), non dalla regola dei pixel validi: con una
   copertura rumorosa vale solo il ritardo di 0,2 s, **non provato** qui.
5. P9 e P10 usano sequenze del catalogo, non semi nuovi. IMU, piano del suolo e camera in moto restano fuori.
6. `riuso/eventi/eventi.py` (zone e soste) non è collegato.

## 5. Che cosa manca, e dopo

- Confrontare il porto col banco in C (stessa geometria T). Finché non regge, nelle scene va detto «regione non
  verificata», o va spento l'interruttore.
- Riaggancio: misurare perché le regole C1 e F-402 rifiutano 79 ritorni su 90 (motivo per motivo, dall'evento
  `identita_ambigua`) prima di toccarle.
- Una variante con l'ombra più grande (pannello a 1 m, persona a 2,5 m) per dare tempo alla regione stretta.
- Modo lungo (`lungo.py`) per aerei e droni: il formato del registro e `mostra` sono già unici, la scala in km no.
