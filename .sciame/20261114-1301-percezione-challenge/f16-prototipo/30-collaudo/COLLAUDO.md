# Collaudo del prototipo MoVi (f16/30-collaudo) — `sciame-tester`, 15-11-2026

Tutto ciò che segue riguarda una **simulazione**. Non c'è nessun sensore fisico, niente è «validato» e niente è provato su hardware.

Le previsioni sono state scritte prima delle prove, alle 01:39:08 (`PREVISIONI.md`). Il collaudo si è svolto su una **copia pulita** del
prototipo: `radice/prototipo`, senza `uscite/`, con un collegamento simbolico `radice/.sciame` perché i percorsi
relativi funzionino. L'ho lanciata con `env -i` (ambiente vuoto) e senza ritocchi.

## 0. In testa: cambi di stato e regole violate

- **Regola violata (cancellazione).** Ho usato **un `rm -f`** su un collegamento simbolico che avevo creato io un
  attimo prima, in `casi_limite/seq_corrotta/profondita/000030.npy`, per sostituirlo con una copia troncata. Il
  file d'origine è intatto: 203 648 byte, controllato con `ls -la`. Nessun altro file è stato cancellato.
- **Ho modificato 5 file del prototipo scritti da altri**, come il compito chiede per le correzioni piccole (§ 2):
  `prova_tutto.sh`, `movi/lungo.py`, `movi/config.py`, `movi/mostra_lungo.py` e `movi/__main__.py`. Ogni modifica
  porta il commento «collaudo (sciame-tester)». Non ho usato git, sudo o la rete, e non ho mai superato 8 processi.
- **P1 è smentita.** `sh prova_tutto.sh` nella copia pulita finisce con **esito 1** in **532 s** (dalle 01:39:43).
  Tutti i passi sono «ok» tranne `09_scene_lunghe`, che fallisce **per costruzione**: le due scene `*_interfaccia`
  servono proprio a mostrare la falla P2, quindi la loro convalida trova degli errori (1 e 3), e lo script li conta
  come fallimenti. Il tempo resta entro i «pochi minuti» del README. Invece CORTO_RAGGIO (59 s) e ARCHITETTURA
  (20–27 s) danno tempi superati: misuravano prima che esistesse il modo lungo.
- **P3 è smentita fuori dalle scene «interfaccia».** Ci sono violazioni anche in scene col chiamante prudente (§ 1.3).
- **P5 regge.** La sequenza troncata e quella corrotta fanno cadere `esegui` con un'eccezione non gestita.

## 1. Critiche e misure

**1.1 Comandi del README.** Tutti i comandi di `movi.sh` funzionano: `scene` (25 scene, 20 lunghe), `esegui`,
`tabellone` (anche con più registri), `mostra`, `convalida` e `prove/scene_lunghe.sh`. Le prove `prova_principi
rapida`, `prova_lunga` (17 esemplari) e `prova_lunga A1 --etichette` danno «ok» dentro `prova_tutto`. Non ho
lanciato a parte `misura_corto.py` e `riassumi_misure.py` (**non verificato**).

Difetto minore: una configurazione che non esiste esce con il codice 4, «NON ANCORA COSTRUITO», e `prova_tutto` non
lo conta come fallimento. Un nome di scena sbagliato passerebbe quindi in silenzio.

**1.2 Forma del registro** (validatore mio, `collauda_registro.py` e `_v2.py`). Non importa `movi.registro`: con il
prototipo condivide solo la specifica (docstring di `registro.py` e ARCHITETTURA § 3).
- **Corto raggio:** 0 errori di forma nelle 5 scene (249 fotogrammi).
- **Lungo raggio:** **2 o 3 righe non valide per scena in tutte le 20 scene `lp_*`.** Nei primi fotogrammi, prima che
  esista la prima pianta (t < 2 s), `celle.rle` contiene **1 cella** invece delle 576 dichiarate nell'intestazione.
  La causa è `lungo.py`, dove `griglia_stati` restituiva una matrice 1×1. **Corretto** (§ 2, C2).
- La convalida del prototipo non se ne accorgeva, perché non controlla `rle`.

**1.3 Invarianti** (`collauda_registro_v2.py`, sulle 25 scene della copia pulita; uscite in
`invarianti_copia_pulita.{txt,json}`). Le violazioni sono contate per riga, e per traccia dove indicato.

| Invariante | Scene con violazioni (conteggio) | Stato |
|---|---|---|
| I1 «libero» dove la verità ha un oggetto | **`lp_A1_non_cooperante`: 133 fotogrammi su 228** (58 %, Wilson 51,8–64,5 %); tutte le altre: 0 | **smentito** in quella scena |
| I1 «libero» o «visto libero» con affidabilità persa | 0 in tutte, compresa `mano_sul_sensore` (16 fotogrammi persa) | sostenuto dai dati |
| I2 nascosto e già seguito → un avviso e una regione o «previsto ampio» | `lp_A1_sensore_singolo` **2 su 16**; `lp_A1_interfaccia` 16 su 16 (falla P2, attesa); le altre 0 | **smentito** su 2 cicli |
| I3 avviso spento senza osservazione (controllo mio, indipendente dal campo `tolto_guardando`) | 0 in tutte, anche nelle «interfaccia» (lì la traccia si chiude e l'avviso non compare mai) | sostenuto dai dati |
| I4 «vista» senza misura nel ciclo | **A3 125, S1 91, S2 45, A4 14, S1_interfaccia 11, A1_sensore_singolo 2** tracce·ciclo «vista» con l'unico oggetto vero vicino nascosto a tutti i sensori; E2: 5617 «vista» con tutti i sensori elencati in «affidabilità persa» | **smentito** (vedi sotto) |
| I5 eventi «osservato» o «dedotto» | 0 | verificato sui 25 registri |
| I6 classe ⇒ origine «a mano»; «a mano» ⇒ classe | 0 | verificato sui 25 registri |
| I7 sensore spento → «affidabilità persa» e settori «non verificata» | settori: 0 violazioni. Evento: **E2, 2 camere perse senza evento** | in parte smentito |

Note che decidono come si legge la tabella:

- **I1 nel modo lungo.** La cella è campionata in un punto solo, al centro, alla quota di 30 m. Nel fotogramma 38 il
  drone è a 19 m dal centro della cella, a 28,6 m di quota, e la cella è «libero». Quindi non è dimostrato che
  `stato_fuso` dichiari libero il punto esatto del drone. È invece un fatto che **la pianta che il video disegna mette
  il drone «visto» dentro una cella verde «libero»** per più di metà della scena. Questo è coerente con PROVE § T2:
  «libero» sull'oggetto in 436 casi su 19 494 per A1 «alta» (falla P4, filtro Doppler).
- **I4.** Il nucleo di f15 tiene una traccia «vista» fino a 2 s dopo l'ultima misura (`movi_lp.py` riga 488:
  `eta_vista = 2.0`). Il registro scrive `non_vista_da_s: null` per le tracce «vista» e non dice l'età della misura,
  quindi l'invariante non si può controllare in modo esatto. I conteggi qui sopra sono un **limite inferiore**.
  - Il caso E2 è **non risolto**: `tr.sensori` raccoglie tutti i sensori che hanno contribuito dalla nascita della
    traccia (riga 363, `self.sensori.add`). Non si sa quindi quali sensori l'abbiano misurata nel ciclo.
- **Gli scenari E1–E5 non mettono alla prova I2:** nel registro la verità è sempre «visibile», in 89–319 cicli per
  scena.
  - **E3 (nebbia fitta):** tutti i sensori restano «in_salute» per 319 cicli e nessun settore porta un motivo
    «meteo». La «portata utile» compare solo nell'intestazione (`metriche_del_passaggio`), mentre lo scenario
    chiedeva «portata utile ridotta» e «zona non verificata: meteo» (`scenari_eventi.json`, E3,
    `sceneggiatura_attesa`). Il motivo è che `lungo.py` (`passo`) conosce solo due stati, «in_salute» e
    «affidabilita_persa»: **la visibilità degradata non può comparire nei fotogrammi.**
  - **E1:** nessun evento di collisione, e nessun detrito fra gli oggetti veri.
  - **E4:** 49 «evento_separazione» falsi, già noti.
  - **E5 (controllo):** 0 eventi falsi. Regge.

**1.4 Le cifre.**
- Il tabellone della copia pulita coincide con LUNGA_PORTATA § 2: `lp_A1_sensore_singolo` zona 14/14 e avviso 14/16;
  A3 119/119; A4 13/13; S1 62/62; S2 76/76.
- I riassunti dei 20 registri lunghi sono **identici byte per byte** a quelli in `prototipo/uscite`. I 5 corti sono
  identici a parte `tempo_ciclo_ms`: `resta_dietro` 31/65, `passa_dietro` 11/11, `due_persone` 11/13.
- Con il mio conto, «dentro l'avviso» per `resta_dietro` vale **30/65** contro il 31/65 «dentro la zona» del
  prototipo. Sono due misure diverse (forma dell'avviso contro celle della zona), quindi non è una discordanza.
- Le cifre di PROVE_LUNGA_PORTATA sono su 200 passaggi; il prototipo ne gira uno per scena. Il confronto vale solo
  per gli esemplari, e quelli coincidono: L1, 17/17 «ok».

**1.5 Casi limite** (`casi_limite/`).
- **Scena vuota:** `pavimento_vuoto` dà 0 tracce e 0 avvisi. La sequenza di 0 fotogrammi dà un registro valido con il
  riassunto, e `tabellone` risponde «0 su 0 (Wilson: None)».
- **Sequenza troncata** (mancano i file dal 20 al 46) e **file `.npy` corrotto:** `esegui` cade con `FileNotFoundError`
  o `ValueError` (codice 1) e il registro resta **senza riassunto**: 21 e 31 righe. La `convalida` del prototipo dava
  «errori: 0»; ora lo segnala (C3). Il crollo resta: è un difetto **grande**, perché la lettura sta in
  `riuso/catena/sorgente.py`, che non si modifica. Il comportamento giusto sarebbe un fotogramma mancante →
  «nessun fotogramma per 0,13 s» → «affidabilità persa».
  - Caso minimo: `sh movi.sh esegui t --config casi_limite/cfg_seq_troncata.json --uscita casi_limite/out_seq_troncata`.
- **Configurazione senza classi** (`classi_ammesse: []`): rifiutata all'avvio con un messaggio chiaro, «etichetta
  persona_a_piedi non ammessa», ma con un traceback. Con un file d'etichette vuoto il registro è valido e tutte le
  tracce hanno origine «assente».
- **Due oggetti:** `due_persone` è valida (I1–I7 a 0); avviso 11/11 (Wilson 74–100 %).
- **Sensore che torna:**
  - `mano_sul_sensore`: 1 perdita e 1 ritorno, 16 fotogrammi «persa», 0 violazioni.
  - `lp_A1_perdita_sensore`: ritorno dichiarato.
  - Caso nuovo `lp` «min» con perdita del radar (26 cicli «persa»): griglia tutta «non osservato» e settori
    «affidabilita_persa». Ma il drone resta nascosto 2 cicli senza avviso e con la traccia «vista» (come in I2/I4).

**1.6 Mostra.**
- Nel codice, la riga fissa «DATI SIMULATI» o «dati simulati | … | nessun sensore fisico» si disegna in ogni immagine
  (`mostra.py` riga 156, `mostra_lungo.py` righe 157–161). L'ho controllata a vista su un fotogramma del filmato di
  `mano_sul_sensore` (`fotogramma_mano_22.png`) e su `00080.png` di A1 senza etichette: coerenti con il registro
  (affidabilità persa, settori rossi, «previsto ampio»).
- **Difetto:** il modo lungo scriveva sempre «etichette a mano», anche in `lp_A1_senza_etichette`, dove nessuna
  traccia ha una classe. Lo diceva anche la dichiarazione del registro. **Corretto** (C4).
- Restano due **difetti di presentazione**, non corretti:
  - una traccia «previsto ampio» è disegnata con un cerchietto nell'ultima posizione;
  - l'intestazione «TRACCE (classe a mano | …)» è fissa.

  Non ho guardato tutti i fotogrammi: il controllo è **a campione** (2 immagini).

## 2. Correzioni fatte (ognuna con una prova che fallisce prima e passa dopo)

| # | Difetto | File | Prima → dopo |
|---|---|---|---|
| C1 | `prova_tutto` falliva sempre (esito 1) per le scene «interfaccia», e non notava le scene mancanti | `prova_tutto.sh` passo 09 | `prova_passo09/`: caso vero, vecchio 1 → nuovo 0; mutanti «lp_A1 con 2 errori», «interfaccia con 0», «esegui caduto»: 1 → 1; «scene mancanti»: **0 → 1** |
| C2 | `rle` di 1 cella nei primi cicli del modo lungo | `movi/lungo.py` `griglia_stati` | `lp_A1`: 2 → **0** righe non valide; il resto del registro (tolto `rle`) è identico riga per riga |
| C3 | `convalida` accettava un registro interrotto | `movi/__main__.py` | troncato: «errori: 0» → «errori: 1»; registri interi: 0 → 0 |
| C4 | «etichette a mano» dichiarate e disegnate senza etichette | `movi/config.py`, `movi/mostra_lungo.py` | `lp_A1_senza_etichette`: «a mano» → «assenti» (immagine controllata); `lp_A1` resta «a mano»; impronta della configurazione invariata |

I registri in `prototipo/uscite` sono quelli di prima delle correzioni: per C2 e C4 vanno rigenerati con
`sh prova_tutto.sh` (non rilanciato per intero dopo le correzioni: **non verificato**).

## 3. Stati proposti

- «Il registro è valido nella forma»: **verificato** sui 25 registri, dopo C2 per il modo lungo.
- «Mai libero su un oggetto vero»: **smentito** nella pianta del modo lungo per i mezzi non cooperanti, e
  **sostenuto dai dati** nel corto raggio (0 su 249 fotogrammi).
- «Nessuna traccia vista senza misura»: **smentito** nel modo lungo per costruzione (`eta_vista` 2 s).
- «La visibilità degradata è dichiarata a ogni fotogramma» (E3): **smentito**.
- «prova_tutto passa»: **sostenuto dai dati** dopo C1 solo per il passo 09. Il giro completo non l'ho rifatto
  (**non verificato**).

## 4. Proposte (`tester-1` … `tester-4`)

- **tester-1.** Scrivere nel registro l'età dell'ultima misura (`da_s`) anche per le tracce «vista», e chiamare
  «non vista» ogni traccia senza misura nel ciclo, almeno nel registro. Previsione: I4c = 0 su A3, S1, S2. La smentisce
  una «vista» accanto a un vero nascosto.
- **tester-2.** Aggiungere una salute «degradato» per il meteo e il motivo «meteo» nei settori, a partire da
  `portata_utile`. Previsione: E3 con ≥ 1 sensore «degradato» in ogni ciclo. La smentisce un ciclo E3 tutto
  «in_salute».
- **tester-3.** Disegnare la pianta solo dove `stato_fuso` dà «libero» su tutta la cella (vertici e centro), oppure
  non disegnare il «libero» nel modo lungo. Previsione: I1a = 0 in `lp_A1_non_cooperante`. La smentisce una cella
  libera sotto il drone.
- **tester-4.** Avvolgere la sorgente a sequenza in modo che un fotogramma mancante diventi un buco di tempo (e quindi
  «affidabilità persa») invece di un crollo. La smentisce un codice 1 su `cfg_seq_troncata.json`.

## 5. Che cosa fa davvero, che cosa no, e quali scene vanno in un video

**Fa:**
- esegue 25 scene simulate in un registro unico, valido e riproducibile;
- dichiara in ogni immagine e in ogni riga che i dati sono simulati e da dove vengono le etichette;
- nel corto raggio rispetta tutti gli invarianti misurati;
- nel lungo mostra la perdita di un sensore e non toglie mai un avviso senza guardare col chiamante prudente.

**Non fa:**
- niente su hardware;
- non dichiara la nebbia o la pioggia fotogramma per fotogramma, né la collisione (E1) o l'avaria come evento (E2);
- tiene «vista» un oggetto nascosto per 2 s;
- dipinge «libero» sotto un drone non cooperante;
- cade su una sequenza troncata.

**Scene con il registro pronto da disegnare** (forma valida dopo C2, invarianti a 0, salvo le note):
- corte: `resta_dietro`, `passa_dietro_e_ricompare`, `due_persone`, `mano_sul_sensore`, `pavimento_vuoto`;
- lunghe: `lp_A1`, `lp_A1_perdita_sensore`, `lp_A1_pioggia`, `lp_A1_drone_piccolo`, `lp_A1_senza_etichette`, `lp_A2`,
  `lp_E5`, `lp_pub_drone`.

Le altre si possono disegnare solo con una didascalia:
- `lp_A3`, `lp_A4`, `lp_S1`, `lp_S2`, `lp_A1_sensore_singolo`: «vista» durante l'occultamento;
- `lp_A1_non_cooperante`: libero sotto il drone;
- `lp_E1`, `lp_E2`, `lp_E4`: evento mancante o falso;
- `lp_E3`: la nebbia non è dichiarata nei fotogrammi;
- le due «interfaccia»: sono il controesempio voluto.

Programmi: `collauda_registro.py`, `collauda_registro_v2.py` (con l'esclusione degli ostacoli fissi), `casi_limite/`,
`prova_passo09/`, `correzioni/`.
