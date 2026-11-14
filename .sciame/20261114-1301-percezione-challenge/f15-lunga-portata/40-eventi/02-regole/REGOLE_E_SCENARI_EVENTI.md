# Regole e scenari per gli eventi improvvisi (MoVi, veicoli veloci)

`sciame-scene-dinamiche` (scheda 49), f15-lunga-portata/40-eventi/02-regole, 15 novembre 2026. File accanto:
`regole_eventi.json`, `scenari_eventi.json`, `frammenti.py` → `risultati_frammenti.json` e `frammenti_esito.txt`,
`conti_eventi.py` → `conti_eventi_esito.txt`, `PREVISIONI.md`. Rifare: `timeout 540 python3 -I frammenti.py 10000`
(88 s) e `python3 -I conti_eventi.py`. **Niente è validato: tutto è conto o simulazione, nessun sensore fisico.**
Solo osservazione, monitoraggio e avviso di situazioni d'incidente: nessuna funzione d'ingaggio, puntamento o contrasto.

## 1. Cambi di stato e regole violate

- **Fonti.** Non ho aperto nessuna pagina in rete: ogni valore mio è **ipotesi** (I) o **conto** (C). I valori con
  fonte sono solo quelli ripresi da `02-sensori`, `04-moto` e `01-effetti` (lì con la loro fonte; molte di `01-effetti`
  sono secondarie o ipotesi, come quel file dichiara). La regola «ogni valore porta la sua fonte oppure ipotesi» è
  rispettata nella forma debole.
- **Previsioni.** Scritte prima del primo giro (`PREVISIONI.md`). Poi **ho cambiato la formula dell'impronta e di
  T_c dopo aver visto 4 casi** del primo giro (impronta di 1832 m contro 406 m di gittata simulata): P2 e P3 valgono
  per la formula nuova e non sono più previsioni cieche. Un secondo giro è stato buttato per un errore mio
  (integratore instabile a passo 0,04 s: 4 campioni «fuori» di 10^207 m, non una smentita). I due esiti scartati
  sono conservati accanto.
- **Esiti.** P1 regge (0 campioni fuori dal volume); P2, P3, P5, P6 reggono; **P4 smentita in parte** (par. 3).
- **Compatibilità.** Stessi stati di cella e stesse parole d'uscita di `04-moto/regole_lunga_portata.json`; nomi dei
  sensori di `02-sensori`; formato di `03-scenari/scenari.json` più `eventi`, `nubi`, `aree`, `sceneggiatura_attesa`,
  `misure`. `10-simulatore` non esisteva: nessun controllo con esso. Le regole **non sono realizzate in `movi_lp.py`**:
  sono pseudocodice e parametri; `movi_lp.py` non l'ho eseguito (in questa shell manca numpy).
- **Scoperta sugli scenari:** la classe `aereo_rullaggio` di `04-moto` (v_max 15,4 m/s) **non copre la corsa di
  decollo** di E2 (40–80 m/s): serve una classe nuova, altrimenti la traccia esce dalla porta prima dell'avaria.

## 2. Le regole (estensione di `04-moto`; parametri in `regole_eventi.json`)

Tre cose non cambiano: non osservato non è mai «libero»; l'avviso si toglie solo guardando; nessuna etichetta riduce
un avviso. Aggiungo alla cella un campo `causa` del «non_osservato» (ostacolo, nube, abbagliamento, meteo, fuori
portata, sensore non affidabile, mai guardato): è un'etichetta in più, non uno stato nuovo.

```
a ogni ciclo t:
  per ogni sensore s: salute(s)                              # EV-C; poi EV-D accorcia la portata dichiarata
  per ogni sensore s affidabile: nube(s) = stima_nube(s)     # EV-B
  stato(cella) = stato_fuso(sensori affidabili, Pd per la classe più piccola ammessa, tolte nubi e ombre)
  per ogni coppia o traccia: innesco_evento()                # EV-A
  per ogni evento aperto: V(tau), impronta(tau); nessuna cella dentro diventa «libero» se non con Pd cumulata
                          >= 0,99 per il frammento minimo ammesso (5 cm, 2e-4 m2); a terra: solo ispezione (EV-E)
  per ogni traccia senza misura: «non vista da X s» + insieme di presenza (movi_lp.insieme_presenza) + avviso
```

**EV-A, frammentazione.** *Innesco «separazione»*: ≥ 3 ritorni nuovi, confermati (2 passate o 2 sensori), entro 2 s
dentro V attorno a una traccia. *Innesco «contatto»*: distanza fra due tracce ≤ somma dei mezzi ingombri + 3σ **e**
almeno uno fra: ≥ 3 ritorni nuovi; residuo fuori porta per 2 passate (accelerazione oltre l'inviluppo); una delle due
non più rilevata in vista. La sola fusione di due tracce dà «tracce non risolte», non un evento. L'evento nasce
**«dedotto»** e diventa «osservato» quando un sensore in salute risolve ≥ 3 ritorni distinti per 2 passate; l'avviso è
lo stesso nei due casi. Le tracce d'origine proseguono «previsto», identità presunta, classe sospesa; i frammenti non
hanno classe né identità.

*Volume.* p₀ = ultimo stato comune osservato (istante t_a), τ = t − t_a, v_c,i = ultime velocità delle tracce
d'origine, |u| ≤ Δv velocità relativa del frammento, vento |w_h| ≤ W, |w_z| ≤ W_z, v_up = max(max_i v_cz,i + Δv + W_z, 0),
τ* = min(τ, (v_up + √(v_up² + 2g(z₀ + r₀)))/g):

- pianta S(τ) = ⋃_i segmento [p₀, p₀ + v_c,h,i·τ*] ingrossato di **r(τ) = W·τ + (Δv + W)·τ* + r₀**;
- quota z ∈ [max(0, z₀ − r₀ + min(min_i v_cz,i − Δv, −W_z)·τ − gτ²/2), z₀ + r₀ + W_z·τ + v_up·s − g·s²/2], s = min(τ, v_up/g);
- r₀ = 3σ_p + mezzo ingombro + a_max·(t_b − t_a)²/2;
- impronta finale: disco attorno a p₀ di raggio R_imp = max su v_t ≥ v_t,min di [W·T(v_t) + gittata nell'aria] + r₀ +
  20 m di rimbalzo; T_c = T(v_t,min) (formule nel JSON e in `frammenti.py`). Durante l'evento l'impronta è S(τ) ∩ disco.

*Prova (modello: punto materiale, resistenza isotropa opposta alla velocità relativa all'aria con coefficiente
costante qualunque, vento costante, v_c costante fra t_a e l'evento).* Sia r = v − w. In orizzontale ṙ_h = −k|r|·r_h:
la direzione non cambia e il modulo non cresce, quindi lo spostamento nell'aria è λ·r_h(0)·τ con λ ∈ [0, 1] e
x_h = p₀ + wτ + λ(v_c + u − w)τ, che sta nel segmento ingrossato di Wτ + (Δv + W)τ. In verticale, dove r_z ≤ 0 vale
ṙ_z ≥ −g, quindi r_z ≥ min(r_z(0), 0) − gt; dove r_z ≥ 0 vale ṙ_z ≤ −g. Integrando si hanno i due estremi di quota.
**Dimostrato nel modello** per τ ≤ τ*. Il taglio a τ* (la resistenza non allunga la gittata), T(v_t) e R_imp sono
**sostenuti dal calcolo, non dimostrati**. Fuori dal modello: raffiche (provate, par. 3), portanza e autorotazione
dei pezzi piatti, corrente ascendente dell'incendio, rotolamento.

*Invariante:* V e impronta non si restringono mai da sole; nessuna cella dentro è «libero» senza Pd cumulata per il
frammento minimo. *Controesempi:* (1) frammento più veloce di Δv (punta d'elica: 100 m/s, C; disco di turbina:
centinaia di m/s, a memoria): esce; (2) frammento più leggero di v_t,min: è ancora in volo a T_c (par. 3, P6);
(3) collisione senza frammenti risolvibili e senza cambio di moto: evento mancato; (4) stormo di uccelli che si apre
attorno a un drone: falsa «separazione»; (5) carico rilasciato di proposito: «separazione» vera ma non incidente.

**EV-B, nube.** Per sensore: nube(s) = celle fra il primo ritorno anomalo e lo sfondo atteso dalla mappa, su 3 cicli,
più 10 m. Dentro **e dietro** la nube lungo il raggio la cella è «non_osservato (nube)» per s; la trasparenza è il
campo `osservato_dietro` **prudente** di `01-effetti` (solo i radar vedono dietro il fumo). Combinazione: `stato_fuso`
sui soli sensori affidabili. Una traccia che entra in celle non osservate da tutti passa a «non vista da X s» con zona
e avviso, come dietro un ostacolo. La nube si toglie solo quando lo sfondo torna visibile per 5 s; le celle tornano
«libero» solo con la Pd cumulata. *Invariante:* nessuna traccia attiva sparisce dentro una nube senza avviso.
*Controesempi:* fumo sottile che attenua senza far perdere lo sfondo (Pd più bassa di quella dichiarata); cielo
senza sfondo dietro (la camera non ha un riferimento: la nube in quota non si stima dallo sfondo); il fronte del
fumo dà al LiDAR ritorni veri, da non scambiare per un oggetto.

**EV-C, abbagliamento.** Indizi e soglie di `01-effetti` (pixel saturi > 5 % EO, > 2 % termica; caduta dei ritorni
LiDAR > 30 %; fondo radar +6 dB). Entro 3 cicli: «affidabilità persa: sensore, causa»; le sue passate non contano
dall'inizio dell'indizio (retrodatato); ricalcolo sugli altri; se nessuno resta, tutto è «zona non verificata».
Ripristino: 10 quadri buoni **e** un riferimento fisso rivisto; le celle ripartono da «non_osservato». *Invariante:*
un sensore non affidabile non contribuisce a nessun «libero». *Controesempi:* guasto che lascia l'immagine plausibile
(quadro congelato): le soglie usano i dati del sensore stesso e non lo vedono; effetto della fiammata sul radar:
**non verificato** (`01-effetti` non ha fonte).

**EV-D, meteo.** R_utile(s, condizione, classe) = fattore **prudente** di `01-effetti` × portata per Pd cumulata 0,99
in 5 passate (radar: 0,922 × portata di scheda, C); per le camere, se il fattore è < 1, vale la portata limitata dal
contrasto. Uscite: «portata utile ridotta»; distanza del «libero» per classe; se è minore della distanza d'avviso di
`04-moto`: «avviso non tempestivo per <classe>»; se il «libero» poggia su un solo sensore: «ridondanza assente».
La condizione è la peggiore fra bollettino e salute dei sensori. *Invariante:* la portata dichiarata non si allunga
mai da sola. *Controesempio:* banco di nebbia locale che il bollettino non dà e che sta oltre i riferimenti fissi.

| m (C, `conti_eventi_esito.txt`) | radar droni | EO | termica | «libero» senza radar | avviso a 1490 m senza radar |
|---|---|---|---|---|---|
| multirotore, sereno | 2858 | 2000 | 1200 | 2000 | sì |
| multirotore, pioggia forte | 2000 | 526 | 353 | 526 | **no** |
| multirotore, nebbia fitta | 2801 | 23 | 15 | 23 | **no** |
| aereo leggero, nebbia fitta | 4900 | 23 | 15 | 23 | **no** |

Con nebbia, neve o pioggia forte tutto regge sul **solo radar**: se cade, l'avviso non è tempestivo per nessuna
classe (354 m servono anche per il solo multirotore).

**EV-E, detriti a terra.** L'impronta, unita su pista alla striscia a valle fino al punto d'arresto, resta «zona non
verificata: possibili detriti» finché non è ispezionata. Con i sensori di `02-sensori` **non si scioglie mai**: il
radar del movimento a terra non vede i detriti, il LiDAR tele arriva a 115 m per 5 cm (`01-effetti`). La scioglie
un'ispezione a vista o un sensore dedicato; il sistema scrive «ispezionata da operatore», non «osservato libero».
*Invariante:* 0 celle «libero» nell'impronta prima dell'ispezione. *Controesempio:* pezzi che rotolano (una ruota)
oltre i 20 m di margine.

## 3. Il simulatore dei frammenti e i suoi risultati

`frammenti.py` (solo libreria standard, semi fissi): punti materiali, resistenza quadratica, velocità limite
log-uniforme fra v_t,min e 40 m/s (E1) o 80 m/s (E2), direzione isotropa, vento costante o a raffiche ogni 0,48 s,
passo 0,04 s con sottopassi. Si controlla ogni 0,5 s se il frammento sta dentro V(τ). **Indipendenza:** stesso autore
e stesso modello fisico della prova; vede gli errori di algebra e di codice, non gli errori del modello.

| Parametri (tutti I) | Δv | W | W_z | v_t,min | T_c | impronta R_imp | gittata massima simulata |
|---|---|---|---|---|---|---|---|
| E1 collisione a 80 m, nominale | 40 | 10 | 1 | 3 m/s | 65 s | 756 m | 405 m |
| E1, prudente | 120 | 15 | 2 | 3 | 130 s | 4249 m | 1191 m |
| E2 avaria a 40 m/s in pista, nominale | 60 | 10 | 1 | 5 | 12 s | 1639 m | 452 m |
| E2, prudente | 100 | 15 | 2 | 5 | 17 s | 3770 m | 725 m |

| Caso (10 000 frammenti; P6: 2000) | campioni fuori da V | dentro V | a terra entro T_c | cadute nell'impronta |
|---|---|---|---|---|
| P1 conforme, uniforme e sul bordo (8 casi) | 0 su 1 131 692 | 100 % | 100 % | 100 % |
| P5 raffiche entro i limiti (4 casi) | 0 su 646 957 | 100 % | 100 % | 100 % |
| P4 Δv vera 1,5 volte (4 casi) | 88, 7, 86, 21 | 99,83–99,997 % | 99,8–100 % | 100 % |
| P6 più leggeri di v_t,min (4 casi) | 0 | 100 % | 64, 74, 97, 94 % | 81, 81, 99,8, 96 % |

Letture. (1) Nei casi conformi **0 campioni fuori**: zero errori su 12 casi non sono una prova universale; la prova
è quella scritta, e vale nel modello. (2) **P4 smentita in parte:** avevo previsto 80–99,9 % dentro; è 99,96 %,
99,997 %, 99,83 %, 99,97 %. L'inviluppo ha più margine del previsto perché la resistenza frena subito i pezzi
leggeri: bene per la sicurezza, male per l'utilità. (3) **L'impronta è molto larga:** da 1,9 a 5,2 volte la gittata
simulata; col caso prudente copre l'intero aeroporto (3,8–4,2 km). È il prezzo della resistenza trascurata e del
vento come margine. Una variante «stretta» (velocità limite massima 40 o 80 m/s, ipotesi in più) dà 680, 1988,
1093 e 1650 m, sempre col 100 % delle cadute dentro. (4) I primi secondi contano di più: a 1 s il volume nominale di
E1 ha raggio 63 m e quota 32–120 m; a 2 s 123 m e tocca il suolo; a 5 s 303 m. (5) **P6:** i frammenti sotto
v_t,min restano in volo oltre T_c (fino a 130–260 s) e cadono fuori dall'impronta fino al 19 %: per loro la zona è
«non verificata» senza limite calcolato, e va detto.

## 4. Gli scenari (`scenari_eventi.json`: geometria, eventi, sceneggiatura attesa, misure)

| | Che cosa succede | Che cosa deve dichiarare MoVi | Misure (soglie scritte prima di ogni prova) |
|---|---|---|---|
| **E1** | Due multirotori (8 e 6,7 m/s) collidono a t = 15 s a 80 m di quota e 286 m dal radar, sopra un piazzale con una persona; A prosegue irregolare e atterra duro a 31 s, B cade in circa 6 s; 60 frammenti | 13,65–15: «tracce non risolte» (sotto 20 m: I); entro 17: «evento: contatto (dedotto)», V e impronta, avviso alla persona; A e B «previsto», identità presunta; B a terra: «non vista da X s», mai «non più rilevata»; a fine scenario piazzale «zona non verificata; la scioglie: ispezione a vista» | ritardo ≤ 2 s (il primo pezzo può toccare terra in 4,0 s); ≥ 99,9 % dei frammenti dentro V; 0 celle libere nell'impronta; 0 tracce perse senza avviso |
| **E2** | Aereo in corsa di decollo, avaria a t = 15,7 s a x = 600 m e 40 m/s: fiammata (3 s; EO cieca fino a 20,7, termica fino a 28,7), fumo, 100 frammenti, arresto a x = 1000 a 40,2 s; un mezzo di servizio va verso il raccordo a x = 900 | entro 3 cicli: «affidabilità persa» per EO e termica; aereo «vista» dal solo radar; entro 2 s: «evento: separazione (dedotto)»; pista da x = 600 a valle «zona non verificata»; avviso al mezzo «zona non verificata sul percorso»; a fine scenario nessun «libero» fra x = 580 e 1020 | cicli per l'affidabilità persa ≤ 3; ritardo ≤ 2 s; 0 celle libere su impronta e pista a valle; avviso al mezzo prima di 140 m (C) |
| **E3** | (a) aereo leggero senza trasmettitore su un sentiero di 3° con nebbia fitta; (b) multirotore con pioggia forte; (c) in più il radar cade per 20 s | «portata utile ridotta» per sensore e classe; «ridondanza assente» (regge il solo radar); in (c): «affidabilità persa: radar», traccia «non vista da X s» con zona, «avviso non tempestivo per tutte le classi»; il silenzio dell'ADS-B non chiude né libera niente | portata dichiarata uguale al conto entro il 5 %; 0 celle libere oltre la portata utile; dichiarazione nel primo ciclo utile |
| **E4** | Multirotore a 12 m/s attraversa una colonna di fumo di 25 m di raggio (dentro da 17,3 a 21,6 s); (a) con radar, (b) solo camere | (a) «vista (radar)», per EO «non osservato, causa nube»; (b) «non vista da X s» con zona e avviso, poi «vista, identità presunta» entro 2 quadri dall'uscita; l'interno della nube resta «non_osservato» | 0 tracce perse senza avviso; 0 celle libere dentro o dietro la nube per l'EO; 0 eventi (una nube non è una frammentazione) |
| **E5** | Controllo: come E1 ma 5 m di separazione in quota, nessun urto | «tracce non risolte» fra 13,65 e 16,35 s, poi due tracce «vista» con identità **presunta**; nessun evento, nessun volume | 0 falsi eventi su 1000 ripetizioni (limite superiore al 95 %: 0,3 %); da ripetere a 2, 1 e 0,5 m |

Nella sceneggiatura i ritardi sono **attese**, non risultati: nessuno scenario è stato fatto girare su un sistema.

## 5. Stati proposti, proposte nuove e passi successivi

- **Dimostrato (nel modello del par. 2):** inviluppo V(τ) per τ ≤ τ*. **Sostenuto dal calcolo:** taglio a τ*, T_c,
  R_imp; tenuta con raffiche. **Smentito in parte:** la mia previsione P4. **Non risolto:** tutte le regole di
  innesco (EV-A), la stima della nube (EV-B) e i ritardi: nessuna è stata eseguita; le deciderebbe il simulatore di
  `10-simulatore` con gli scenari E1–E5. **Non verificato:** ogni valore dei frammenti (numero, masse, velocità).
- `scene-dinamiche-1` **Impronta a due livelli nel video.** Meccanismo: mostrare il volume dimostrato dei primi
  secondi (quello che conta per chi è sotto) e l'impronta larga come zona di chiusura. Previsione: in E1 nominale
  l'avviso alla persona parte entro 2 s e il volume la copre prima dei 4,0 s. Smentita: un frammento simulato tocca
  terra fuori dal volume o prima dell'avviso.
- `scene-dinamiche-2` **Soglia di E5 trovata, non scelta.** Meccanismo: ripetere E5 a separazione decrescente e E1
  con sempre meno frammenti visibili. Previsione: esiste una fascia in cui i falsi eventi restano sotto l'1 % e gli
  eventi veri sono dichiarati entro 2 s in più del 90 % dei casi. Smentita: le due curve non lasciano fascia: allora
  l'innesco «contatto» va rifatto.
- `scene-dinamiche-3` **Classe «aereo in corsa di decollo»** in `04-moto` (v_max circa 80 m/s, vincolo di pista).
  Previsione: senza, in E2 la traccia è persa prima di t = 15,7 s. Smentita: la traccia regge con la classe attuale.
- **Dopo:** far realizzare EV-A…EV-E in `movi_lp.py` da chi lo mantiene; far rivedere Δv e v_t,min a un esperto di
  frammentazione con una fonte aperta; far attaccare EV-A dal generatore avversario (uccelli, rilascio di un carico).
