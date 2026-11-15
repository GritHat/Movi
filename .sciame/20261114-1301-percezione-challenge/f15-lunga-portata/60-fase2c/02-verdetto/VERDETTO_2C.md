# Verdetto rapido sulle correzioni (fase 2c)

`sciame-arbitro`, 2026-11-15, dalle 03:32 alle 03:40 circa (`date -Is`). Previsioni del riconto scritte prima, alle
03:32:47, in `PREVISIONI.md` (questa cartella). Riconto con codice mio: `riconto_2c.py` e `riconto_scene_v3.py` →
`riconto_2c_esito.txt`. Rileggono i record per passaggio di `01-correzioni` (`riprova_passaggi_v3*.jsonl`,
`passaggi_v3.jsonl`, `cp_X5b_v3_esito.json`) e i registri delle scene `prototipo/uscite/video/*_v3/`.
**Tutto è simulazione dalle schede: nessun sensore fisico, niente è «validato».** Etichette a mano. Solo osservazione
e avviso. **Indipendenza:** il riconto condivide con l'autore i record e le definizioni dei campi (`libero_viol`,
`fuori_avviso`, `ritardo_evento_s`, `ispezionati`). Controlla l'aggregazione e la coerenza fra i file, non la misura.

**Le previsioni del riconto reggono tutte (R1–R6).** Le cifre di CORREZIONI_2C tornano dai file, con due aggiunte mie:
K-614 e il conteggio per tipo di evento (sotto).

## 0. In testa: regole

- **Regole violate dagli altri** (dal loro rapporto): hanno sovrascritto due volte le loro cartelle `uscite/video/*_v3`
  invece di fare versioni nuove accanto. L'esito del primo giro è conservato. Hanno fatto un `mv -n` di un loro file.
  Il numero di processi (al più 6) è **non verificato**. La regola dei 3 s sull'età della traccia d'origine è stata
  scritta **dopo** il pilota sul passaggio 31, quindi lo 0/60 «prima dell'urto» è una correzione mirata e non una
  previsione. Le modifiche al prototipo hanno le copie `.prima_2c`. Nessuna cancellazione dichiarata.
- **Io:** ho scritto solo in `02-verdetto`. Nessuna violazione.

## 1. Cambi di stato rispetto a VERDETTO_2B

| Enunciato | VERDETTO_2B | Ora | Prova (ricontata) |
|---|---|---|---|
| A1 sito, «libero» sul drone non C0 | smentito, 163/171 | **sostenuto dai dati**: 0/171 [0; 0,022] in alta e in min col v3 (ritenuta del ritorno, 5 s). Vale solo **con la mappa dichiarata completa** (ipotesi del simulatore) | `riprova_passaggi_v3.jsonl`. Soglia scritta prima (P2, 03:06): ≤ 2/171 |
| K-613 (legare W_c alla v_max) | decisione del coordinatore | **chiusa.** Da sola è **smentita** (163/171): la causa è la singola passata mancata. La famiglia «sito» resta il caso centrale col v3 completo | `riprova_passaggi_v3_letterale.jsonl` |
| A1, tempestivo | 200/200 | invariato col v3: 200/200 [0,981; 1] in alta e in min. Falsi confermati: mediana 0 | idem |
| A1 min, fuori avviso | 12/200 | **invariato**, 12/200 [0,035; 0,102] (6 «ferma», 6 «rallenta»). K-606 aperto | idem |
| X5 / K-612 (mappa) | riaperto | **chiuso nel predefinito del prototipo** (0/6 «libero», tutti «non osservato»). **Non risolto** con la mappa dichiarata: 5/6 «libero» dietro l'edificio non in pianta. La validazione-3 non è chiamata | `cp_X5b_v3_esito.json` |
| E1, impronta | smentita (mediana 42 km; 36/60 ≥ 10 km) | **sostenuta dai dati**: raggio residuo 3,1–4,5–5,3 km, 0/60 ≥ 10 km | `passaggi_v3.jsonl` |
| E1, «l'impronta si riduce guardando» | non c'era | **non risolto, la prova è vuota**: l'ispezione non ha tolto punti in 0/60 passaggi (0/30 in E2) | idem, `ispezionati[0]` |
| E1 entro 2 s | smentito, 49/60 | **resta smentito**: 51/60 [0,739; 0,919], ritardi 1,2–1,8–2,3 s, nessuno negativo (K-609 non si ripete). Col tipo giusto («contatto») entro 2 s: **50/60**. Due passaggi su 60 sono dedotti come «separazione» | idem |
| E1, evento prima dell'urto | 1/60 | 0/60 [0; 0,060], ma con una regola notata dopo | idem |
| E2, avviso al mezzo | giusto ma non discrimina | invariato: 30/30, il mezzo entra davvero nell'impronta in 30/30. Tracce avvisate: mediana 96 | idem |
| E5, 5 m | 0/30 | 0/30 [0; 0,114] col v3 | idem |
| Scene video | `lp_A1` con 56 celle «libero» nell'avviso | **8 scene _v3: convalida a 0 errori, validatore della controprova a 0 (conteggi vuoti)** | `*_v3/convalida.txt`, `valida_video_controprova.txt` |
| Primi fotogrammi (576 contro conteggi vuoti) | da correggere | **corretto**: il fotogramma 0 di `lp_A1_v3` ha `non_osservato: 576` | `lp_A1_v3/registro.jsonl` |
| Correzione 3 (mappa) | scavalcata nel prototipo | **applicata nel predefinito.** Le scene la dichiarano nell'intestazione | `cp_X5b_v3_esito.json`, intestazioni dei registri |

**Contraddizione nuova.**

| K | Contrasto | Vale | Prova |
|---|---|---|---|
| K-614 | `lp_E1_v3`, dato come «E1 n. 30», contro il record E1 n. 30 di `passaggi_v3.jsonl` | **Non sono la stessa esecuzione.** Coincidono t_b 17,2 s e t_a 15,86 s. Ma il registro dice «contatto», origine [1, 13], R_imp 4972 m e residuo 5246 m; il record dice «separazione», origine [1], 2933 m e 3094 m. La causa è **non verificata** (forse `EVENTI_MAPPA_CERT` o il percorso del prototipo). La scena resta dentro la distribuzione (residuo ≤ 5262 m). L'INDICE dà «circa 5,0 km», cioè R_imp | `lp_E1_v3/registro.jsonl`; `passaggi_v3.jsonl` |

**Non ricontato** (adottato col rinvio al file): `prova_tutto.sh` con esito 0 in 698 s (`prova_tutto_esito.txt`, ultima
riga); le camere entro 3 cicli in E2 col v3 (30/30); il codice del nucleo v3, che non ho riletto.

## 2. Limiti da dire per primi

1. Nessun sensore fisico. Le Pd, i falsi allarmi, le latenze e i 45 m/s e 25 m/s² del drone veloce sono ipotesi.
2. **Il «libero» dipende dalla mappa.** Lo 0/171 vale con la mappa dichiarata completa dal simulatore. Con una mappa
   dichiarata ma sbagliata, il «libero» dietro un edificio non in pianta è falso (5/6). Per questo il prototipo, per
   predefinito, non dichiara la mappa. La validazione-3 non è chiamata.
3. Gli aerei in volo sono fuori dal caso centrale: per loro l'avviso non è tempestivo, ed è dichiarato.
4. L'avviso perde il drone che rallenta o si ferma in circa il 6 % dei passaggi (12/200).
5. Gli eventi improvvisi sono dedotti, entro 2 s in 51/60. La zona dei detriti è di chilometri (circa 4,5) e non si
   riduce guardando. L'avviso non distingue: in E2 avvisa circa 96 tracce. La fiammata è rilevata con un'ipotesi
   ottimista.
6. Il v3 è rimisurato solo su A1, E1, E2 ed E5. A2, A3 e A4 hanno le cifre del v2, e la controprova (100/100) non è
   rifatta col v3. Il prezzo della ritenuta (chiusure tardive) non è misurato.
7. Nelle traiettorie reali ci sono un solo multirotore e un solo ala fissa.

## 3. Affermazioni convergenti (aggiornate, al più dodici)

1. **(Caso centrale: sito sorvegliato, droni)** «In simulazione da scheda, un drone a 15–21 m/s sul sito è stato
   annunciato in tempo all'operatore in 200 passaggi su 200, sia nella configurazione alta sia in quella minima. In
   nessuno dei 171 passaggi con un drone non C0 MoVi ha detto "libero" dove il drone era, con la mappa del sito
   dichiarata completa. Quando il drone rallenta o si ferma dietro un edificio, l'avviso l'ha perso per qualche ciclo
   in 12 passaggi su 200, e lo diciamo.» · S, con la mappa come ipotesi · `riprova_passaggi_v3.jsonl`.
2. **(Caso centrale: rullaggio)** «Un aereo in rullaggio nascosto da un hangar, con radar di superficie, LiDAR e
   ADS-B: avviso in tempo in 200 passaggi su 200, mai fuori dall'avviso, mai "libero" sull'aereo. Col solo radar era
   in tempo in 50 su 200.» · S (nucleo v2; la scena v3 ha 0 errori) · riprova A2 della fase 2b.
3. **(Aerei in volo, limite)** «Per gli aerei in volo (fino a 210 m/s) l'avviso non arriva in tempo all'operatore di
   sito, e MoVi lo scrive: "avviso non tempestivo".» · S, caso costruito.
4. «Il "libero" vale solo per ciò che è stato guardato. Se la mappa non è dichiarata, dietro un edificio MoVi dice
   "non osservato" (6 casi su 6). Se è dichiarata ma sbagliata, il "libero" può essere falso, e lo diciamo.» · S,
   casi costruiti · `cp_X5b_v3_esito.json`.
5. «Un radar d'aeroporto non vede un drone sotto la sua copertura. MoVi non lo chiama mai "libero" (0 passaggi su
   200) e scrive "zona non verificata per i multirotori".» · S, e per costruzione.
6. «L'avviso si spegne solo dopo aver guardato tutta la zona dove il mezzo può essere, oppure quando lo si rivede. La
   regola ingenua lo spegneva in 564 passaggi su 2400.» · S (v1 e v2).
7. «Dopo una collisione fra droni MoVi deduce l'evento in 1,2–2,3 s (entro 2 s in 51 passaggi su 60), con una zona
   dei detriti di circa 4,5 km (mai oltre 5,3 km in 60 passaggi). Non chiama mai "libero" dove possono cadere i
   frammenti. Ma la zona non si riduce guardando, e l'avviso non distingue chi è in pericolo.» · S · `passaggi_v3.jsonl`.
8. «Quando un sensore cade, o una fiammata o la pioggia lo accecano, MoVi lo dice: camere dichiarate non affidabili
   entro 3 cicli in tutti i passaggi simulati (90 col v2, 30 col v3).» · S, con l'innesco ottimista.
9. «Fumo, detriti in pista e passaggi ravvicinati non hanno prodotto falsi eventi improvvisi (col fumo 0 su 120 e
   0 su 60; a 5 m 0 su 300 e 0 su 30, più 0 su 30 col v3), né eventi prima dell'urto (0 su 60, regola notata dopo).»
   · S · VERDETTO_2B § 2.8, `passaggi_v3.jsonl` (E5).
10. «Il limite di velocità copre i droni veloci fino a 45 m/s (ipotesi) e gli aerei fino a 210 m/s. Un ritorno radar
    recente vieta il "libero" per 5 s: una sola passata mancata non basta più.» · S · v3, `riprova_passaggi_v3*`.
11. «"Libero" vale solo per le classi dichiarate: i droni sotto i 250 g sono "zona non verificata".» · S.
12. «Il nome della classe non spegne l'avviso.» · per costruzione; v1, non rifatto.

## 4. Da non dire

- Restano: «validato» (e i suoi equivalenti), «in tempo reale», «certificabile», «detect and avoid», «rileva droni a
  N km», «zero falsi allarmi», «122 droni», il lessico d'ingaggio e quello della scheda IRIS, le cifre di
  tempestività per A3, «avviso tempestivo per gli aerei in volo», «l'avviso contiene sempre il drone»,
  «individua chi è minacciato dai detriti», «rileva la fiammata» come capacità del sensore, le mediane 46 e 59 km.
- **Nuove o aggiornate:**
  - «MoVi non dichiara mai libero ciò che non ha osservato» senza «con la mappa dichiarata, in simulazione»;
  - «il v3 elimina il "libero" falso» (vale con la mappa giusta: 5/6 con la mappa sbagliata);
  - «l'impronta si restringe guardando» (0/60);
  - «E1 entro 2 s» e «sempre» (51/60; `lp_E1_v3` è a 2,2 s);
  - «avvisa solo i mezzi in pericolo» (circa 96 tracce in E2);
  - «tutte le correzioni sono applicate» (6, 7 e 8 no);
  - le cifre del v3 per A2, A3 e A4 (non rimisurate);
  - `lp_A1_ingenua_v3` come contrasto;
  - «`lp_E1_v3` è il passaggio n. 30 delle misure» (K-614).

## 5. Le scene del video (`prototipo/uscite/video/INDICE.md`, versioni _v3)

| Scena | Verdetto | Motivo |
|---|---|---|
| `lp_A1_v3` | **«Simulation»** | Scelta a caso col seme dichiarato prima (n. 90). Validatore a 0, 11 293 celle «libero» mostrate (la prova non è vuota), 7 tolte. È coerente con 0/171. In sovrimpressione: «mappa dichiarata completa (ipotesi)». **Ma non ha una fase nascosta**: non mostra il drone dietro l'edificio. Per quel momento, `lp_A1` (n. 33, v2) resta solo «Schematic» (decisione D1) |
| `lp_A1_ingenua_v3` | «Simulation», **da non usare** | Col v3 non fa contrasto. Il contrasto resta `lp_A1_ingenua` (v1), «Simulation» con la scritta «regola ingenua (v1)», come in VERDETTO_2B |
| `lp_A2_v3` | **«Simulation»** | 0 e 0, coerente con 200/200 (misura v2). Nessuna cella «libero»: il validatore controlla il vuoto |
| `lp_A3_v3` | **«Simulation»** | 0 e 0. «Zona non verificata» va presa dal registro. Nessuna cifra di tempestività |
| `lp_E1_v3` | **«Simulation»** per l'evento dedotto («contatto», 2,2 s dopo l'urto, scritto a 17,5 s) e per l'avviso; **la zona dei detriti solo «Schematic»** | Il passaggio è a caso e il ritardo è onesto (fuori dai 2 s, va detto). Il residuo è 5,2 km, vicino al massimo, e K-614 è aperto. Che il visore v3 disegni i detriti è **non verificato** |
| `lp_E2_v3` | **«Simulation» solo per le camere non affidabili**; detriti e avviso al mezzo solo «Schematic» | L'innesco è ottimista e l'impronta contiene il mezzo |
| `lp_E3_v3` | **«Simulation»** | La riduzione di portata è piccola (1041 m contro 1062 m) e non indipendente: va detto |
| `lp_E4_v3` | **«Simulation»** | Nessun falso evento, coerente con 0/60 e 0/30 |

## 6. Decisioni per il coordinatore e che cosa resta aperto

1. **D1 (coordinatore):** per la scena centrale «drone dietro l'edificio», rigenerare A1 col v3 su un passaggio scelto
   a caso **fra i 22 con fase nascosta**, col seme scritto prima, e passarlo dai due validatori. Oppure mostrare
   `lp_A1_v3` senza quel momento.
2. K-614: rieseguire E1 n. 30 col percorso del prototipo e con quello della misura, e confrontare tipo e raggio.
3. Rimisurare col v3 A2, A3, A4 e la controprova di A1 (n = 100). Il prezzo della ritenuta: falsi confermati e
   chiusure tardive. Previsione di CORREZIONI: mediana ≤ 1, smentita se ≥ 3.
4. La validazione-3 della mappa nel simulatore, poi cp_X5b con la mappa dichiarata.
5. K-606 (12/200 fuori avviso); l'ispezione dell'impronta con T_c per punto; le correzioni 6–8.
