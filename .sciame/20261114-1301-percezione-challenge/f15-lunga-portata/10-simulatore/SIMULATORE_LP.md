# Simulatore dei sensori a lunga portata e sua verifica (f15/10-simulatore)

`sciame-validazione`, 15-11-2026 (orologio della macchina; la consegna dice 14). **Tutto è simulazione dalle schede
tecniche o ipotesi dichiarata: niente è provato su un sensore fisico, niente è «validato».** Solo osservazione e
avviso: le camere sono orientate dal radar per *osservare*, nessuna funzione d'ingaggio o di puntamento di mezzi.

## 0. In testa: cambi di stato e regole

- **Simulatore verificato contro il suo modello** (V1–V6 reggono; V3 regge solo dopo aver portato le passate da 4000
  a 20 000, vedi § 3). Verificato vuol dire: il codice fa ciò che il modello dice. **Non** che il modello descriva un
  sensore vero: il 46 % dei campi delle schede è «ipotesi» (02-sensori) e io ne aggiungo altri, elencati in § 2.
- **Scarti dalla consegna, dichiarati.** Il radar 4D gira a 5 Hz invece di 20 Hz, e i LiDAR a 5 Hz invece di 10 Hz, per
  stare nei tempi. I falsi ritorni del radar 4D sono 0,3 per quadro, non 1 come nel JSON: con 1 per quadro i falsi
  avvisi esplodono e il costo pure (la prova di sensibilità è in PROVE § 4). Le sorgenti acustiche e a
  radiofrequenza non sono simulate.
- **Regole.** Ho importato `movi_lp.py` e `frammenti.py` con `-B` e `sys.dont_write_bytecode`, per non scrivere
  `__pycache__` nelle cartelle altrui. Non ho cancellato file. Non ho usato la rete: le schede sono quelle di
  02-sensori, le traiettorie quelle di 01-dati.

## 1. Che cosa fa (`sim_lp.py`, solo numpy)

Dalla **verità** (traiettorie a 0,1 s) e dalla **geometria** ricava le **rilevazioni** di ogni sensore, record per
record: `{t, t_consegna, sensore, salute, ril: [(id vero | None, z, R, extra)]}`.

| Parte | Modello | Da dove |
|---|---|---|
| Linea di vista | segmento sensore–punto contro gli spigoli degli ostacoli estrusi (altezza del poligono) | `scenari.json` |
| Orizzonte radar | d = 4,12 (√h_s + √h_t) km | formula del JSON di 02-sensori |
| Quota minima | radar d'aeroporto cieco sotto 200 m | nota della scheda TERMA (resto del radar: ipotesi) |
| Campo | azimut relativo all'orientamento `az0`, elevazione | schede (orientamenti: miei) |
| Nubi | cilindri verticali, opachi solo per i tipi elencati, con deriva e crescita | `scenari_eventi.json` |
| Pd radar e LiDAR | Swerling 1: Pd = Pfa^(1/(1+SNR)), SNR ∝ σ/R⁴; zero oltre R_max | 02-sensori; LiDAR riferiti al drone (ipotesi) |
| Pd camere | 0,8 dentro la portata pratica per la dimensione del bersaglio (≥ 12 pixel), zero fuori | JSON (portate: conto e ipotesi) |
| Rumore | gaussiano in distanza, azimut, elevazione; camere: distanza al 10 % (ipotesi: triangolazione) | schede, sigma |
| Rivisita | antenna rotante: istante di illuminazione alla frazione di giro dell'azimut | IRIS, SCANTER, aeroporto |
| Doppler | radar 4D: bersaglio con velocità radiale < 0,3 m/s filtrato | ipotesi |
| Falsi allarmi | Poisson per passata, uniformi nel volume coperto | ipotesi (tab. § 2) |
| Latenza | `t_consegna = t + latenza`; cooperativi: posizione vecchia di 0,6 s (ADS-B) e 1 s (Remote ID) | CFR 91.227, 89.310 |
| Cooperativi | presente, assente, intermittente (10 s acceso, 10 spento); Pd per messaggio 0,9 | CFR; Pd: ipotesi |
| Salute | spento (nessun record), pioggia forte (fondo +8 dB, portata × 0,7), abbagliamento (pixel saturi 0,3) | indicatori di 01-effetti |
| Meteo | portata × fattore; la verità usa il nominale, la griglia del nucleo il prudente | `effetti_eventi.json` |
| Non risolti | due ritorni radar entro 2σ in distanza e angolo diventano uno (solo E1–E5) | ipotesi mia |

Sensori del catalogo: radar per droni (Robin IRIS), pannello (EchoGuard), radar del movimento a terra (SCANTER), radar
primario d'aeroporto, radar 4D (ARS 548), LiDAR AT128 e Tele-15, camera EO 300 mm e termica 100 mm, ADS-B, Remote
ID. Ogni voce porta il campo `fonte`.

## 2. Ipotesi aggiunte da me (oltre a quelle di 02-sensori)

LiDAR come bersaglio «equivalente» con esponente 4, riferito al drone piccolo: 150 m (AT128) e 230 m (Tele-15) a Pd 0,9.
IRIS: campo in elevazione da −2° a 58°, latenza 0,1 s. Radar d'aeroporto: 60 km per 1 m², σ 50 m e 0,1°. Falsi ritorni
per passata: IRIS, SCANTER, aeroporto 0,5; pannello 0,05; radar 4D 0,3; LiDAR 0,05; camere 0,05. Sezioni radar: mezzo
10 m², persona 0,5 m²; **drone C0 1,6·10⁻⁴ m²** (conto di 02-sensori dalla scheda IRIS). Camere orientate da un
rilevamento radar dello stesso oggetto negli ultimi 5 s, e l'associazione usa la verità: è **ottimista**.

## 3. Verifica contro il modello (`verifica_simulatore.json`, soglie in PREVISIONI.md, scritte alle 00:20:40)

Comando: la prima riga di `rifai.sh` (circa 10 s).

| Prova | Che cosa | Esito |
|---|---|---|
| **V1 Pd** | 5 sensori × 6 fasce (0,3–1,5 della portata di riferimento), 2000 passate per fascia: rilevamenti generati dal simulatore contro la Pd del modello | **30 fasce su 30** dentro Wilson 95 %. Es. IRIS a 3100 m: 968 su 2000 contro 0,4997; a 4650 m: 103 su 2000 contro 0,0541. **Regge** |
| V1, al primo giro | il radar 4D dava 0 su 2000 in tutte le fasce | il bersaglio di prova era **fermo**: il filtro Doppler lo toglieva. Il modello faceva ciò che dice; ho rifatto con 5 m/s radiali. *Notato dopo* |
| **V2 rumore** | 4000 misure a metà portata, errore proiettato sulla direzione radiale | rapporto sigma ottenuta su dichiarata: distanza 1,002–1,013; azimut 0,992–1,003. **Regge** (al primo giro, misurando la norma, SCANTER dava 18,5: era l'errore trasversale della sua σ_el di 0,3 rad, non un errore del simulatore) |
| **V3 falsi** | 20 000 passate per sensore | IRIS 0,5016 [0,490; 0,510]; SCANTER 0,4938; radar 4D 1,0033 [0,986; 1,014] (con λ = 1); LiDAR 0,0997 e 0,0987. **Regge**. Con 4000 passate il radar 4D dava 1,040 fuori dall'intervallo: con 5 prove una uscita a 2,5 σ è attesa nel 6 % dei casi; non risolto se fosse caso, ma a 20 000 regge |
| **V4 geometria** | 500 prove per caso | rilevamenti dietro l'ostacolo 0, oltre l'orizzonte 0, sotto la quota minima 0, fuori campo 0. **Regge** |
| **V5 cooperativi** | 1001 passate | presente 0,902 (atteso 0,9); assente 0; intermittente 0,443 (atteso 0,45). **Regge** |
| **V6 semi** | `SeedSequence(20261115, spawn_key=(scenario, configurazione, passaggio))`; la verità ha la sua chiave (scenario, 0, passaggio) ed è **appaiata** fra le due configurazioni | in PROVE § 1: semi distinti e prime estrazioni distinte su tutti i passaggi |

**Indipendenza.** La geometria, il rumore, i falsi allarmi e la salute sono scritti qui e non vengono dal nucleo. In comune
col nucleo restano la formula di Pd (Swerling 1) e i numeri delle schede, e l'autore della prova è lo stesso del
simulatore. Le fasce di V1 usano gli stessi flussi casuali per sensori diversi, quindi le righe si somigliano: le
fasce non sono indipendenti fra un sensore e l'altro. **Non coperto:** cammini multipli, clutter strutturato,
uccelli, fluttuazione correlata fra una passata e l'altra, occlusione parziale (il bersaglio è un punto). Su questi il
simulatore non dice niente.

## 4. Esemplari per il prototipo e il video

`esemplari/<scenario>_alta_0_<chiamante>.json` (A1–A4, S1, S2) ed `esemplari/E1…E5_alta_0.json`: sensori con la
fonte, ostacoli, verità, tutte le rilevazioni con salute e latenza, e le uscite del nucleo ciclo per ciclo (parola,
posizione, raggio della possibile presenza, zona). È sempre il passaggio 0: comportamento nominale, cooperativo
presente, configurazione ad alte prestazioni.

Rifare: `sh rifai.sh` (tempo misurato in PROVE § 1).
