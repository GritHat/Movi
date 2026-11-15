# Prototipo MoVi: il modo a lunga portata multisensore (f16/20-lunga-portata)

Scritto da `sciame-sviluppatore` il 15-11-2026, fra le 01:22 e le 01:39 (ore di `date -Is`). **È tutto simulazione:**
i sensori vengono dalle schede tecniche e il moto dagli scenari o da una traiettoria pubblica; le etichette sono
assegnate a mano. Nessuna parte è stata provata su hardware, e nessun risultato va letto come «validato». Il
prototipo fa solo osservazione e avviso.

## 0. In testa: gli esiti e le regole violate

- **Il modo lungo è COSTRUITO.** I comandi sono gli stessi del corto raggio (`movi esegui | tabellone | mostra |
  convalida`) e anche il formato del registro è lo stesso. Ci sono 20 scene `lp_*`, e per ognuna c'è il registro
  completo, un filmato `movi.mp4` e da 5 a 8 PNG in `prototipo/uscite/lp_*/`. Le previsioni sono state scritte alle
  01:23:37, prima delle prove, in `PREVISIONI.md`.
- **L1 regge.** Le misure coincidono con quelle di f15: i cicli del prototipo sono identici campo per campo agli
  esemplari di `f15/10-simulatore/esemplari`. Il confronto copre **17 file su 17** e 2739 cicli (`prove/prova_lunga.py`,
  uscite in `prototipo/uscite/lunga/prova_L1_*.txt`), e vale per tutti e due i chiamanti e per E1–E5.
- **L3 regge.** Togliere le etichette lascia l'avviso identico in **228 cicli su 228** (A1, Wilson 95 % [0,983; 1]).
- **L2 regge.** `convalida` non trova errori nelle 18 scene col chiamante prudente.
- **L5 è smentita alla lettera, poi corretta.** La convalida del corto raggio controlla solo gli avvisi che spariscono,
  e sulle scene «interfaccia» trovava **0** errori. Il motivo è che nel modo lungo una traccia può chiudersi nello
  stesso ciclo in cui smette d'essere vista, cioè prima che compaia un avviso. Era un buco della convalida, e l'ho
  chiuso (§ 2.3). Dopo la correzione ci sono **1** errore in `lp_A1_interfaccia` e **3** in `lp_S1_interfaccia`, e
  ancora 0 nelle scene prudenti.
- **L4 regge per `esegui`.** Il tempo va da 9 a 63 s per scena: A1 35,6 s, A3 62,9 s (`durata_esecuzione_s`
  nell'intestazione). Il tempo di `mostra` non l'ho misurato.
- **Regole violate.**
  - Per circa un minuto ho tenuto **9 processi di calcolo** insieme invece di 8: otto prove L1 più la prova L3.
  - Ho modificato file del prototipo scritti dal ruolo del corto raggio, come la consegna permette: `README.md`,
    `prova_tutto.sh`, `riuso/IMPRONTE.txt` (solo aggiunte), `movi/{registro, tabellone, mostra, esegui, config,
    sorgenti}.py` (aggiunte per il modo lungo).
  - Non ho cancellato niente, non ho usato la rete, git o sudo.
- **Non verificato.** `sh prova_tutto.sh` non l'ho lanciato per intero dopo le modifiche: ho eseguito a parte i suoi
  passi nuovi. Non ho riprovato il corto raggio dopo l'aggiunta in `registro.valida_sequenza`, che però agisce solo
  sulle righe con `modo == "lungo"`.

## 1. Che cosa ho fatto

1. **Riuso tale e quale** in `prototipo/riuso/lunga_portata/`, con le stesse cartelle di f15 perché il codice usa
   percorsi relativi. Sono copiati: `movi_lp.py`, `sim_lp.py`, `prove_lp.py`, `eventi_lp.py`, `frammenti.py`, le
   regole, le schede, `scenari.json`, gli effetti, le regole e gli scenari E1–E5, le traiettorie pubbliche con
   `PROVENIENZA.md` e gli esemplari. Le impronte sono in `riuso/IMPRONTE.txt` e `IMPRONTE_TRAIETTORIE.txt`, e
   `sha256sum -c` dà OK.
2. **L'adattatore è `movi/lungo.py`.**
   - Nel codice di f15 simulatore e nucleo girano insieme dentro `passaggio()`. Non li ho separati, perché per farlo
     avrei dovuto modificare quel codice.
   - Li osservo invece con due sostituzioni a tempo d'esecuzione, che tolgo alla fine:
     - `Inseguitore` diventa un sottotipo che registra tracce, avvisi e pianta a ogni `uscite()`. A ogni `mancato()`
       che chiude una traccia annota anche se l'avviso era spegnibile, con `avviso_spegnibile` del nucleo.
     - `SensoreSim` diventa un sottotipo che serve per la visibilità vera.
   - Che le sostituzioni non cambino nulla lo prova L1.
3. **Le condizioni** si scelgono in `sorgente.condizione`: «min» (sensore singolo) o «alta» (multisensore),
   cooperante, perdita di un sensore, pioggia, drone piccolo C0, etichette, comportamento.
   - `prove_lp` le lega all'indice del passaggio (indice % 3, % 10, % 7, % 5). Il prototipo sceglie il primo
     indice che le soddisfa e lo dichiara nel registro.
   - Ne segue che la perdita di un sensore porta sempre il comportamento «indietro» (indice 9) e la pioggia porta
     «vira» (indice 18).
   - Il chiamante prudente è quello predefinito. «interfaccia» si può scegliere per mostrare la falla P2.
4. **Configurazione.** Ho aggiunto `profilo_ricevente`, cioè chi riceve l'avviso, con i profili di
   `regole_lunga_portata.json`.
   - L'intestazione porta la distanza d'avviso dello scenario (A1: 806 m) e quella del conto col profilo
     (`distanza_avviso`, A1: 1490 m). Le due sono diverse, e nella vista si disegna quella dello scenario.
   - Le etichette a mano sono in `etichette/lunga_portata.json`, che è la tabella `CLASSE` di `prove_lp`.
5. **Sorgente «registrazione pubblica»** (`lp_pub_drone`).
   - Il bersaglio di A1 segue il volo vero `cmu_m100_volo100`: CMU, CC BY 4.0, licenza in `PROVENIENZA.md` di
     01-dati, letta oggi da quel ruolo e non da me. Il volo è ruotato e traslato.
   - A metà percorso c'è un **ostacolo VIRTUALE**.
   - Le rilevazioni restano simulate: in 01-dati non ci sono rilevazioni reali.
6. **Le viste (`movi/mostra_lungo.py`).**
   - La pianta mostra: sensori, coperture, ostacoli, celle dello stato fuso (`movi_lp.stato_fuso` alla quota
     indicata, 24×24 celle ogni 2 s), tracce con stato ed età, regione di previsione **tratteggiata**, avviso
     arancione, cerchio della distanza d'avviso richiesta e croce bianca della verità.
   - La console mostra: salute dei sensori, tracce, eventi «osservato» e «dedotto», tabellone.
   - La riga fissa dice «dati simulati | etichette a mano | sensori simulati dalle schede | nessun sensore fisico».
   - Le quote della pianta sono un'ipotesi e servono solo a disegnare.

## 2. Critiche e misure (sempre il passaggio 0 o quello scelto: un passaggio per scena, NON una statistica)

1. **Il cuore del caso centrale (A1, aerei e droni).**
   - Con il solo radar (`lp_A1_sensore_singolo`) il drone resta nascosto per 16 cicli. La zona dichiarata lo contiene
     in 14 cicli su 14 (Wilson [0,78; 1]). L'avviso lo contiene in 14 su 16: nei primi 2 cicli la traccia è ancora
     «vista» (età ≤ 2 s) e quindi senza avviso. f15 non li conta come fuori (`nasc_fuori_avviso` = 0), perché li
     tollera fino a 2,5 s più un periodo.
   - Con quattro sensori (`lp_A1`) il drone **non è mai nascosto a tutti**: 0 cicli. Il pannello vede dietro
     l'edificio.
   - In entrambe le configurazioni la traccia è confermata a 946–960 m dal sito, contro gli 806 m richiesti.
2. **Gli altri scenari (`metriche_del_passaggio`, calcolate dal codice di f15).**

   | Scena | Avviso tempestivo | Oggetto nascosto dentro l'avviso | Dentro la zona |
   |---|---|---|---|
   | A2 | sì (301 m contro 147) | — | — |
   | A3 | **no** (3432 m contro 3932: lo scenario parte a 2,5 km) | 119 su 119 | 76 su 86 [0,80; 0,94] |
   | A4 | sì | 13 su 13 | 6 su 13 |
   | S1 | sì | 62 su 62 | **16 su 55** |
   | S2 | sì | 76 su 76 | 66 su 76 |

   - In S1 f15 conta 4 cicli fuori dall'avviso in 3D. Il mio conto è in pianta e non li vede.
   - La zona debole in S1 è quella già smentita in PROVE § 3.5.
3. **Il buco della convalida.**
   - **Che cosa succede.** In `lp_S1_interfaccia` il nucleo chiude 4 tracce senza aver guardato tutto l'insieme di
     presenza. f15 conta 69 cicli nascosti su 69 senza regione. Eppure la convalida del corto raggio non segnalava
     niente.
   - **La correzione.** In `registro.valida_sequenza`, solo per il modo lungo, ora è un errore anche una traccia che
     sparisce senza un evento «osservato» che la giustifichi.
   - **Le previsioni.** Su ogni scena prudente: 0 errori, e regge. Su A1 e S1 «interfaccia»: ≥ 1 errore, e regge
     (1 e 3).
4. **Le condizioni** (un passaggio ciascuna).
   - **Perdita di un sensore.** Dichiarata: 26 cicli con il sensore «affidabilità persa», l'evento è «osservato».
   - **Pioggia.** Dichiarata dal controllo di salute: 44 cicli.
   - **Mezzo non cooperante e drone C0.** Tempestivi (954 e 949 m).
   - **E2.** L'abbagliamento delle camere è dichiarato per 107 cicli.
   - **E4.** Il nucleo dichiara 49 cicli di «evento_separazione» nel passaggio 0. È un falso evento, coerente con la
     smentita di PROVE § 4 (5 su 60).
5. **Quello che non ho toccato.** Le falle di PROVE restano come sono: «libero» sotto il filtro Doppler, ricentraggio
   su un falso ritorno, falsi avvisi per ora, ritardo E1, evento E2 mai dichiarato. Il prototipo le **mostra**, non le
   corregge.
6. **La pianta.** È un taglio orizzontale a una quota fissa, mentre un oggetto in volo ha una quota sua. A quella
   quota, in A1 con IRIS, la pianta è quasi tutta «non osservato»: è coerente con PROVE § 3.4, dove IRIS non dichiara
   quasi mai libero.

## 3. Stati proposti

- «Il prototipo esegue gli stessi passaggi di f15»: **verificato** sui 17 esemplari, a passaggio 0.
- «Nel modo lungo l'avviso non dipende dalle etichette»: **sostenuto dai dati** (A1, 228 cicli). Non verificato
  sugli altri scenari.
- «Il chiamante prudente non toglie avvisi senza guardare»: **sostenuto dai dati** su 18 scene, un passaggio
  ciascuna. È coerente con PROVE (0 cicli su n = 50 per riga).
- Tutto il resto è simulazione. Su un sensore fisico non è provato niente.

## 4. Proposte

- **sviluppatore-1, nucleo separato dal simulatore.** Si sposta il ciclo di `prove_lp.passaggio` in `movi/lungo.py`.
  Previsione: L1 resta 17 su 17. Lo smentisce un ciclo diverso.
- **sviluppatore-2, avviso anche nei primi 2 s.** La traccia appena non vista porta subito l'insieme di presenza.
  Previsione: «dentro l'avviso» 16 su 16 in `lp_A1_sensore_singolo`. Lo smentisce un ciclo nascosto senza avviso.

## 5. Dopo

1. Lanciare `sh prova_tutto.sh` per intero (non verificato).
2. Rifare la scena `lp_pub_drone` con un aereo in rullaggio (ATL, ODbL).
3. Portare i conti del tabellone in 3D come in f15.
4. Far girare il tabellone su molti passaggi (`prove_lp` con n = 200) invece che su uno.

Codice: `prototipo/movi/{lungo, mostra_lungo}.py`, `prototipo/prove/{prova_lunga.py, scene_lunghe.sh}`,
`prototipo/scene/lp_*.json`.
