# MoVi a lunga portata: modelli di moto e regole (f15/04-moto, sciame-tracciamento)

15 novembre 2026. File: `regole_lunga_portata.json` (parametri), `movi_lp.py` (riferimento, solo numpy), `prove_movi_lp.py` → `risultati.json`, `PREVISIONI.md` (soglie scritte alle 00:02:43, prima del codice).
Comando: `<venv>/bin/python -I -u prove_movi_lp.py` (34,5 s).

## 0. Cambi di stato, regole violate, limiti

- **Niente è provato su un sensore fisico, niente è «validato».** Tutto è conto o simulazione. I sensori del file sono **segnaposto** (ipotesi): vanno sostituiti con le schede scelte dai ruoli dei sensori. I valori di classe nuovi (aerei, droni ad ala fissa, alta velocità, autostrada) sono **ipotesi** senza fonte aperta oggi; quelli ripresi da f14 lo dicono campo per campo. Nessuna pagina di rete aperta, nessun dato scaricato.
- **P4 e P5 smentite alla prima esecuzione** (37 cambi d'identità su 20 semi; 30 scambi all'incrocio). Causa: ogni misura appena fuori porta apriva una traccia doppia. Corretto con la «porta del dubbio» (2.4), aggiunta dopo; rifatte su 40 semi, 20 dei quali nuovi: 0 e 0.
- **P9 smentita:** le prove durano 34,5 s, non «pochi secondi» (soglia 20 s).
- **Regola del «libero» cambiata in corsa** (prima della consegna): la prima stesura cumulava 5 s di passate per ogni classe; per un oggetto veloce è un errore. Ora la finestra è per classe (1.2).
- La taratura della regione di previsione è su **traiettorie generate**, non su dati pubblici: su traiettorie vere è **non verificato**.
- Non realizzato nel riferimento: rete delle vie di rullaggio (si usa la sfera, che sovrastima), maschera del terreno (entra come matrice calcolata fuori), assegnazione ungherese (qui golosa sul costo), misure fuori sequenza oltre 0,5 s (scartate con evento), falsi allarmi nelle prove (non simulati).
- Ambito: solo osservazione e avviso. Nessuna funzione d'ingaggio, puntamento o contrasto.

## 1. Lo spazio: celle distanza–azimut(–elevazione) per sensore

Ogni sensore ha la **sua** griglia polare (`GrigliaPolare`), con i quattro stati di prima: libero, occupato, in ombra, non osservato. Riferimento fisso Est–Nord–Alto.

```
1.1 OMBRA (statica, per sensore)
  cella in_ombra  se il segmento sensore -> centro cella incrocia un ostacolo noto in pianta
                  sotto la sua altezza, o se la maschera del terreno la copre.
1.2 LIBERO (per classe c, con sezione radar rcs_c e velocita' v_max_c)
  W_c(cella) = min(t_cumulo_max, lato_cella / v_max_c)       # oltre, l'oggetto ha cambiato cella
  n          = passate che hanno illuminato la cella in [t - W_c, t], dopo l'ultimo ritorno
  Pc_c       = 1 - (1 - Pd(distanza, rcs_c))^n                # passate indipendenti: IPOTESI
  Pc_c       = minimo di Pc_c sulla cella e sulle 8 vicine    # chi era nella vicina puo' essere entrato
  cella LIBERA per c   <=>  non in ombra  e  Pc_c >= 0,99
  cella LIBERA         <=>  libera per OGNI classe ammessa dallo scenario
  altrimenti, se non in ombra: NON OSSERVATA (l'uscita dice per quale classe: «zona non verificata per <c>»)
  scaduta W_c senza nuova passata: torna NON OSSERVATA.
1.3 OCCUPATO: ritorno nella cella all'ultima passata che l'ha illuminata.
1.4 PIU' SENSORI (stato_fuso): occupato > libero > in ombra > non osservato; «libero» anche se nessun
    sensore basta da solo ma il prodotto dei (1 - Pc_c) dei sensori che vedono la cella e' <= 0,01.
1.5 AFFIDABILITA' PERSA di un sensore: la sua griglia torna tutta NON OSSERVATA.
1.6 La sorveglianza cooperativa NON illumina celle: non crea mai «libero».
```

Pd dalla scheda: `Pd = Pfa^(1/(1+SNR))`, `SNR ∝ rcs / R^n` (bersaglio fluttuante; n = 4 radar e LiDAR su bersaglio piccolo, 2 ottico: ipotesi di modello). La soglia 0,99 e il tetto di 5 passate sono ipotesi.

**Prove (simulazione, radar segnaposto: Pd 0,9 a 5 km su 1 m², 1 Hz, celle da 100 m).** P1: a 4 km dopo 5 passate senza ritorno la cella è «libera» per 20 m² e **«non osservata» per il multirotore da 0,01 m²**. P2: per 0,01 m² il «libero» arriva a 2360 m con 5 passate e a 877 m con una (conto a mano uguale). P3, verificato sulla griglia di prova: 0 celle «libere» fra le mai illuminate, le 200 in ombra e le scadute (12 960 controlli). Due radar, 3 passate ciascuno, a 2,25 km: «non osservato» da soli, «libero» insieme. Portata del «libero» per classe con la finestra W_c: multirotore 2,36 km (5 passate), drone ad ala fissa 2,92 km (3), aereo leggero 5,9 km (2), aereo di linea 10,6 km (2).

## 2. Il seguimento

Stato `[x y z vx vy vz]` con covarianza, nel riferimento fisso. Parametri per classe in `classi` del file.

| classe | modelli (miscela IMM) | q a regime / in manovra (m/s²) | vincolo |
|---|---|---|---|
| multirotore, elicottero | velocità quasi costante, virata ±ω, manovra | 0,5 / 6,9 · 0,3 / 5 | libero 3D |
| drone ad ala fissa, aerei in volo | velocità quasi costante, virata ±ω | 0,1–0,3 | libero 3D |
| aereo in rullaggio | come sopra | 0,1 | rete delle vie se nota, altrimenti libero 2D |
| auto | velocità quasi costante, virata ±ω con ω = a_lat/v (curvatura ≤ a_lat/v²) | 0,3 | libero 2D |
| treno | velocità quasi costante lungo l'ascissa del binario | 0,05 | binario (1 grado di libertà) |
| non classificato | tutti i modelli, parametri dell'inviluppo | 0,5 / a_max dell'inviluppo | libero 3D |

Virata coordinata: ω = a_lat / v nel piano orizzontale, nota per classe, due modelli (sinistra e destra); probabilità di restare nel modello 0,95 per passo (ipotesi). Il vincolo al binario per il filtro è specificato qui ma **non è nel riferimento** (lì il treno usa il modello 3D; il vincolo c'è solo nell'insieme di possibile presenza).

```
2.1 Le misure di tutti i sensori si fondono UNA ALLA VOLTA nell'ordine d'arrivo (Inseguitore.aggiorna):
    per ogni gruppo (stesso sensore, stesso istante):
      prevedi ogni traccia all'istante della misura (mescolamento IMM, poi un passo per modello)
      porta: d2 di Mahalanobis sulla posizione <= 16,27 (chi quadro 3 gdl, 0,999)
      assegna: vicino piu' prossimo globale (nel riferimento: goloso sul costo; ungherese nel prototipo)
      aggiorna ogni modello (forma di Joseph), poi i pesi dei modelli
2.2 Radar, LiDAR, ottico: misura polare -> cartesiana con la covarianza della scheda (Sensore.misura).
2.3 Cooperativa (ADS-B, identificazione a distanza): posizione + velocita' + identificativo. E' una misura
    in piu'. Stesso identificativo = stessa traccia; identificativi diversi non si associano mai.
    Una traccia vista SOLO dalla cooperativa dice «vista (solo cooperativa: non verificata da un sensore)».
    Quando manca: la traccia continua sugli altri sensori; il silenzio della cooperativa non chiude
    niente e non conta come mancato rilevamento (un trasponditore spento non e' un'assenza).
2.4 Porta del dubbio: misura con 16,27 < d2 <= 30,66 da una traccia confermata -> NON apre una traccia;
    evento «misura dubbia»; alla terza in 5 s si apre (puo' essere un secondo oggetto vicino).
2.5 Vita: apertura da misura non assegnata; conferma 2 su 3; tentativa non confermata in 3 s: tolta.
    Chiusura SOLO «non piu' rilevata»: traccia in vista, e Pd cumulata dei mancati rilevamenti (classe
    piu' piccola dello scenario) >= 0,99. In ombra, fuori copertura o con sensore non affidabile non
    si accumula niente: la traccia resta, con l'avviso.
2.6 Fuori sequenza: misura piu' vecchia della traccia di oltre 0,5 s -> scartata con evento.
```

**Prove.** P4 (aereo a 70 m/s, virata di 15 s, radar 1 Hz + ottico 5 Hz + cooperativa 2 Hz spenta a 30 s; 40 semi): errore quadratico medio 39,9 m col solo radar, 4,4 m con la fusione, migliore in 40 semi su 40; 0 cambi d'identità, una traccia. P5 (due bersagli non classificati che s'incrociano con 100 m di quota di separazione, radar + ottico, 40 semi): 0 semi con scambio, Wilson 95 %: 0–0,088. Entrambe **sostenute dai dati in simulazione, dopo una correzione**; senza falsi allarmi, quindi tracce false: non misurate.

## 3. L'occlusione

```
3.1 INSIEME DI POSSIBILE PRESENZA (e' l'avviso; insieme_presenza):
    centro  = ultima posizione stimata;  tau = tempo dall'ultima misura
    v0      = min(|v stimata| + 3 sigma_v, v_max_inv)
    raggio  = R(tau; v0, v_max_inv, a_max_inv) + 3 sigma_p + w        # w = 50 m (ipotesi)
    R       = v0 tau + a tau^2/2 finche' v < v_max, poi v_max per il tempo che resta
    v_max_inv, a_max_inv = MASSIMO sulle classi ammesse dallo scenario: MAI quelli dell'etichetta.
    gradi di liberta': sfera (3D) sempre; tratto di binario [s_min, s_max] SOLO se lo scenario ammette
    soltanto classi sul binario; vie di rullaggio solo se la rete e' nota (non nel riferimento).
3.2 L'avviso si spegne SOLO guardando (avviso_spegnibile): ogni cella dell'insieme «libera» per ogni
    classe ammessa, con passate SUCCESSIVE alla perdita; oppure l'oggetto e' rivisto. Mai a tempo.
3.3 REGIONE DI PREVISIONE al livello 0,90, per classe (RegionePrevisione): sfera centrata sulla previsione
    a velocita' costante dall'ultima stima; raggio = quantile conforme dell'errore, tarato su traiettorie
    della classe a 1, 2, 5, 10, 30 s, piu' 3 (sigma_p + sigma_v tau). Usa l'etichetta: e' la «zona»,
    non l'avviso.
3.4 PREVISTO AMPIO se: tau oltre l'ultimo orizzonte tarato; o raggio della zona > 0,8 del raggio di 3.1;
    o classe senza taratura (non classificato); o affidabilita' persa. Non torna mai «previsto»
    finche' l'oggetto non e' rivisto.
```

Crescita del raggio raggiungibile, in metri, senza incertezza né fascia (conto, `risultati.json`):

| classe (v_max, a_max) | da fermo 5 / 10 / 30 s | da v_max 5 / 10 / 30 s | regione 0,90 a 5 / 10 / 30 s (simulata) |
|---|---|---|---|
| multirotore (19; 6,9) | 69 / 164 / 544 | 95 / 190 / 570 | 51 / 145 / 569 |
| drone ad ala fissa (40; 5) | 62 / 240 / 1040 | 200 / 400 / 1200 | 44 / 144 / 760 |
| aereo leggero (70; 3) | 38 / 150 / 1283 | 350 / 700 / 2100 | 27 / 93 / 550 |
| aereo di linea in avvicinamento (90; 3) | 38 / 150 / 1350 | 450 / 900 / 2700 | 27 / 93 / 557 |
| aereo in rullaggio (15,4; 1) | 12 / 50 / 343 | 77 / 154 / 462 | 9 / 31 / 178 |
| treno alta velocità (83,3; 0,5), sul binario | 6 / 25 / 225 | tratto 398–416 / 758–833 / 1824–2499 | — |
| auto in autostrada (36,1; 3) | 38 / 150 / 866 | 180 / 361 / 1083 | 27 / 91 / 507 |

Il vincolo al binario riduce l'avviso da una sfera di 2,5 km a un tratto di 675 m a 30 s: vale solo perché il treno non può lasciare il binario, non per l'etichetta. **Prove.** P6: 0 traiettorie simulate fuori dall'insieme su 60 000 (10 classi × 2000 × 3 orizzonti); è una proprietà del conto, entro i limiti v_max e a_max dichiarati. P7: copertura della regione sulla prova, 40 celle classe × orizzonte, n = 2000 ciascuna: limite inferiore di Wilson peggiore 0,8703 (soglia 0,87), tipico 0,885–0,895; verifica la procedura sul generatore, non il mondo. P8, verificato su griglia: il raggio dell'inviluppo non è mai sotto quello di una classe ammessa (0 casi su 27 951). Caso d'insieme: multirotore che passa dietro un capannone → «vista», «non vista da 1 s con zona», «previsto ampio»; dopo 40 s l'insieme ha raggio 3,35 km, il 36 % dei punti campionati è stato riguardato libero e l'avviso resta.

## 4. L'avviso tempestivo

```
ricevente fermo:    d_avv = v_max_inv (tau_lat + T_r + T_man) + w
ricevente in moto:  d_avv = (v_ego + v_max_inv)(tau_lat + T_r) + v_ego^2/(2 a_fr) + v_max_inv v_ego/a_fr + w
TEMPESTIVO  <=>  portata del «libero» della classe che limita (1.2) >= d_avv
altrimenti: «avviso non tempestivo per <classe>» e oltre quella portata «zona non verificata».
```

Con i profili **ipotetici** del file (tau_lat 1 s, w 50 m) e il radar segnaposto:

| scenario (v_max inviluppo; classe che limita) | portata del «libero» | operatore di sito (T_r 5 s + 10 s) | pilota in rullaggio | pilota remoto di drone | macchinista (83 m/s) |
|---|---|---|---|---|---|
| aeroporto e droni (90 m/s; multirotore) | 2,36 km | 1,49 km: sì | 0,92 km: sì | 0,76 km: sì | — |
| ferrovia (83,3 m/s; multirotore) | 2,36 km | 1,38 km: sì | — | 0,72 km: sì | 7,57 km: **no** |
| strada (36,1 m/s; auto) | 11,0 km | 0,63 km: sì | — | — | — |

Sono conti su valori ipotetici: dicono come si calcola, non che cosa garantisce un sensore. Il treno ad alta velocità chiede oltre 7 km: con quel radar e un drone piccolo fra le classi ammesse l'avviso **non** è tempestivo, e il sistema lo deve dire.

## 5. Le uscite: stesse parole

| parola | quando |
|---|---|
| vista | misura in porta entro 2 s (parametro `eta_vista`) |
| non vista da X s con zona | senza misura; zona = regione 3.3 al livello dichiarato |
| previsto ampio | regola 3.4 |
| possibile presenza | insieme 3.1, acceso da quando la traccia confermata non è più vista; si spegne solo con 3.2 |
| zona non verificata (per classe) | celle «non osservate» o «in ombra» |
| affidabilità persa (per sensore) | la sua griglia è «non osservata»; le tracce rette solo da lui: «previsto ampio» |

Interfaccia: `Inseguitore.uscite(t, regioni)` restituisce per traccia `id, classe, parola, da_s, pos, zona, possibile_presenza, solo_cooperativa`; `GrigliaPolare.stati(t, classi)` e `stato_fuso(...)` per le celle; `Inseguitore.eventi` per il registro. Il chiamante (simulatore o prototipo) deve dire quali tracce erano nel settore senza ritorno: `Inseguitore.mancato(t, sensore, id)`.

## 6. Stati proposti e che cosa viene dopo

- Regola del «libero» con Pd cumulata per classe: **sostenuta dai dati in simulazione** su un modello di Pd da scheda; l'indipendenza fra passate e l'esponente del modello sono ipotesi **non verificate**.
- Insieme raggiungibile contiene il moto entro v_max e a_max: **dimostrato nel modello** (accelerazione e velocità limitate), controllato su 60 000 casi; vale quanto valgono i limiti di classe, che sono ipotesi.
- Regione al 90 %: **non risolta** su dati veri; la decide una taratura su traiettorie pubbliche (ADS-B, registri di volo di droni) con prova su voli tenuti da parte.
- Identità all'incrocio e senza cooperativa: sostenuta in simulazione senza falsi allarmi; **non risolta** con disturbo e con più di due bersagli.
- tracciamento-1 (proposta): scegliere il lato della cella da `v_max × periodo × passate` della classe più veloce. Previsione: con celle da 450 m l'aereo di linea cumula 5 passate e la sua portata del «libero» sale da 10,6 a circa 15,8 km; la smentisce il ricalcolo con `Sensore.portata`.
- Dopo: sostituire i sensori segnaposto con le schede vere; aggiungere i falsi allarmi; rete delle vie di rullaggio; filtro vincolato al binario; portare le prove sotto i 20 s.
